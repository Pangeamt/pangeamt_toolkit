from __future__ import unicode_literals
import os
import re
import torch
from shutil import copytree, ignore_patterns
from onmt.utils.parse import ArgumentParser
from onmt.model_builder import build_base_model
from onmt.utils.optimizers import Optimizer
from onmt.trainer import build_trainer
from onmt.translate import GNMTGlobalScorer
from onmt.models import ModelSaver
from onmt.translate.translator import Translator as Translator
import onmt.model_builder
import onmt.translate.beam
import onmt.inputters as inputters
import onmt.decoders.ensemble
from onmt.inputters.text_dataset import  TextDataReader
from pangeamt_toolkit.pangeanmt.translation import Translation
from pangeamt_toolkit.pangeanmt.attention_matrix import AttentionMatrix


class Pangeanmt:
    SEED = 829

    def __init__(self, config):
        # Config
        self._config = config

        # Model
        self._model = config.model

        # Get the model options
        model_path = self._model.config.model_path
        checkpoint = torch.load(
            model_path,
            map_location=lambda storage, loc: storage)
        self._model_opts = ArgumentParser.ckpt_model_opts(checkpoint['opt'])
        ArgumentParser.update_model_opts(self._model_opts)
        ArgumentParser.validate_model_opts(self._model_opts)

        # Extract vocabulary
        vocab = checkpoint['vocab']
        if inputters.old_style_vocab(vocab):
            self._fields = inputters.load_old_vocab(
                vocab, "text", dynamic_dict=False
            )
        else:
            self._fields = vocab

        # Train_steps
        self._train_steps = self._model_opts.train_steps

        # Build openmmt model
        self._opennmt_model = build_base_model(
            self._model_opts,
            self._fields,
            self._config.use_gpu(),
            checkpoint,
            self._config.gpu_id)

        # Translator
        self._translator = Translator(
            self._opennmt_model,
            self._fields,
            TextDataReader(),
            TextDataReader(),
            gpu=self._config.gpu_id,
            min_length=self._config.min_length,
            max_length=self._config.max_length,
            beam_size=self._config.beam_size,
            replace_unk=self._config.replace_unk,
            copy_attn=self._model_opts.copy_attn,
            global_scorer= GNMTGlobalScorer(0.0, -0.0, 'none', 'none'),
            seed=self.SEED
        )

        if self._model.config.online_learning.is_active:
            # Optim
            optimizer_opt = type("", (), {})()
            optimizer_opt.optim = 'sgd'
            optimizer_opt.learning_rate = self._model.config.online_learning.learning_rate
            optimizer_opt.train_from = ''
            optimizer_opt.adam_beta1 = 0
            optimizer_opt.adam_beta2 = 0
            optimizer_opt.model_dtype = 'fp32'
            optimizer_opt.decay_method = 'none'
            optimizer_opt.start_decay_steps = 100000
            optimizer_opt.learning_rate_decay=1.0
            optimizer_opt.decay_steps = 100000
            optimizer_opt.max_grad_norm=5
            self._optim = Optimizer.from_opt(self._opennmt_model, optimizer_opt, checkpoint=None)

            trainer_opt = type("", (), {})()
            trainer_opt.lambda_coverage = 0.0
            trainer_opt.copy_attn=False
            trainer_opt.label_smoothing=0.0
            trainer_opt.truncated_decoder=0
            trainer_opt.model_dtype='fp32'
            trainer_opt.max_generator_batches=32
            trainer_opt.normalization='sents'
            trainer_opt.accum_count=[1]
            trainer_opt.accum_steps=[0]
            trainer_opt.world_size=1
            trainer_opt.average_decay=0
            trainer_opt.average_every=1
            trainer_opt.dropout= 0
            trainer_opt.dropout_steps=0,
            trainer_opt.gpu_verbose_level=0
            trainer_opt.early_stopping=0
            trainer_opt.early_stopping_criteria=None,
            trainer_opt.tensorboard=False
            trainer_opt.report_every=50
            trainer_opt.gpu_ranks=[]
            if self._config.gpu_id != -1:
                trainer_opt.gpu_ranks= [self._config.gpu_id]

            self._trainer = build_trainer(
                trainer_opt,
                self._config.gpu_id,
                self._opennmt_model,
                self._fields,
                self._optim)
        else:
            self._trainer = None

    def translate(self, srcs):
        # Set model mode to eval
        self._opennmt_model.eval()
        self._opennmt_model.generator.eval()

        dataset = inputters.Dataset(
            self._fields,
            readers=([self._translator.src_reader]),
            data=[("src", srcs)],
            dirs=[None],
            sort_key=inputters.str2sortkey[self._translator.data_type],
            filter_pred=self._translator._filter_pred
        )

        data_iter = inputters.OrderedIterator(
            dataset=dataset,
            device=self._translator._dev,
            batch_size=self._config._batch_size,
            train=False,
            sort=False,
            sort_within_batch=False,
            shuffle=False
        )

        # Translation builder
        translation_builder = onmt.translate.TranslationBuilder(
            dataset,
            self._fields,
            1,      # NBest
            True,   # replace_unk,
            False,
            "",     # Phrase table
        )

        results = []
        for batch in data_iter:
            batch_data = self._translator.translate_batch(
                batch,
                dataset.src_vocabs,
                True
            )
            translations = translation_builder.from_batch(batch_data)
            for translation in translations:
                # Get tokens
                src_tokens = translation.src_raw
                tgt_tokens = translation.pred_sents[0]

                # Create src in tgt from tokens
                src = ' '.join(src_tokens)
                tgt = ' '.join(tgt_tokens)

                # Create attention matrix
                attention_matrix = AttentionMatrix(
                    src_tokens,
                    tgt_tokens,
                    translation.attns[0].tolist()
                )
                # Score
                score = translation.pred_scores[0].item()

                # Create a translation object
                t = Translation(
                    src,
                    tgt,
                    attention_matrix,
                    score
                )
                # Append to result
                results.append(t)
        return results

    # Train
    def train (self, src, tgt):
        # Check if online learning is active
        if not self._model.config.online_learning.is_active:
            msg = f'Online learning is not active'
            raise ValueError(msg)

        for _ in range(self._model.config.online_learning.steps):
            # Set model mode to train
            self._opennmt_model.train(True)
            # self._model.generator.train()

            # Create the dataset
            src_reader = inputters.TextDataReader()
            tgt_reader = inputters.TextDataReader()

            srcs = [src]
            tgts = [tgt]

            dataset = inputters.Dataset(
                self._fields,
                readers=[src_reader, tgt_reader],
                data=[("src", srcs), ("tgt", tgts)],
                dirs=[None, None],
                sort_key=None,
                filter_pred=None
            )

            # Create batches
            batches = inputters.OrderedIterator(dataset, batch_size=1, device=self._translator._dev)

            # Update train steps
            self._train_steps += 1

            # Train the model.
            self._trainer.train(
                batches,
                self._train_steps,
                save_checkpoint_steps=None,
                valid_iter=None,
                valid_steps=None)

    def save_model(self, new_model_dir):
        new_model_dir = os.path.abspath(new_model_dir)
        if os.path.isdir(new_model_dir):
            if not os.listdir:
                os.rmdir(new_model_dir)
            else:
                msg = f"{new_model_dir} already exists"
                raise ValueError(msg)
        copytree(self._model.model_dir, new_model_dir, ignore=ignore_patterns('*.pt'))
        model_filename = os.path.basename(self._model.config.opts.models[0])
        model_filename_base = re.sub('_[0-9]*\.pt$', '', model_filename )
        base_path = os.path.join(new_model_dir, model_filename_base)
        model_saver = ModelSaver(
            base_path,
            self._model,
            self._model_opts,
            self._fields,
            self._optim,
            keep_checkpoint=-1
        )
        model_saver.save(self._train_steps)
