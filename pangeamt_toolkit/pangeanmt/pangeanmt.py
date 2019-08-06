from __future__ import unicode_literals
import os
import re
import torch
from shutil import copytree, ignore_patterns
import pangeamt_toolkit.onmt.inputters as inputters
from pangeamt_toolkit.onmt.inputters.dataset_base import Dataset
from pangeamt_toolkit.onmt.inputters.text_dataset import TextDataReader
from pangeamt_toolkit.onmt.inputters.inputter import OrderedIterator
from pangeamt_toolkit.onmt.utils.parse import ArgumentParser
from pangeamt_toolkit.onmt.model_builder import build_base_model
from pangeamt_toolkit.onmt.utils.misc import use_gpu
from pangeamt_toolkit.onmt.utils.optimizers import Optimizer
from pangeamt_toolkit.onmt.trainer import build_trainer
from pangeamt_toolkit.onmt.translate import GNMTGlobalScorer
from pangeamt_toolkit.onmt.models import ModelSaver
from pangeamt_toolkit.pangeanmt.extended_model.extended_model import ExtendedModel
from pangeamt_toolkit.pangeanmt.onmtx_translator import OnmtxTranslator



class Pangeanmt:
    def __init__(self, model_dir):

        # Model dir
        self._model_dir = os.path.abspath(model_dir)
        if not os.path.isdir(self._model_dir):
            msg = f"{model_dir} doesn't exists'"
            raise ValueError(msg)

        # Extended model
        self._extended_model = ExtendedModel(model_dir)

        # Config
        self._config = self._extended_model.config

        # Options
        self._opts = self._config.opts

        # Get the model options
        model_path = self._opts.models[0]
        checkpoint = torch.load(
            model_path,
            map_location=lambda storage, loc: storage)
        self._model_opts = ArgumentParser.ckpt_model_opts(checkpoint['opt'])
        ArgumentParser.update_model_opts(self._model_opts)
        ArgumentParser.validate_model_opts(self._model_opts)

        # Train_steps
        self._train_steps = self._model_opts.train_steps

        # Extract vocabulary
        vocab = checkpoint['vocab']
        if inputters.old_style_vocab(vocab):
            self._fields = inputters.load_old_vocab(
                vocab, self._opts.data_type, dynamic_dict=self._model_opts.copy_attn
            )
        else:
            self._fields = vocab

        # Build model
        self._model = build_base_model(
            self._model_opts,
            self._fields,
            use_gpu(self._opts),
            checkpoint,
            self._opts.gpu)

        if self._opts.fp32:
            self._model.float()

        #Translator
        scorer = GNMTGlobalScorer.from_opt(self._opts)

        self.translator = OnmtxTranslator.from_opt(
            self._model,
            self._fields,
            self._opts,
            self._model_opts,
            global_scorer=scorer,
            out_file=None,
            report_score=False,
            logger=None,
        )

        # Create trainer
        self._optim = Optimizer.from_opt(self._model, self._opts, checkpoint=checkpoint)

        device_id = -1 # TODO Handle GPU
        self.trainer = build_trainer(
            self._opts,
            device_id,
            self._model,
            self._fields,
            self._optim)


    def translate(self, srcs):
        # Set model mode to eval
        self._model.eval()
        self._model.generator.eval()

        # Translate
        translations = self.translator.translate(
            src=srcs,
            batch_size=self._config.opts.batch_size,
        )
        return translations


    def train (self, src, tgt):
        online_learning = self._config.online_learning
        # Check if online learning is active
        if not online_learning.is_active:
            msg = f'Online learning is not active'
            raise ValueError(msg)

        for _ in range(online_learning.steps):
            # Set model mode to train
            self._model.train(True)

            # Create the dataset
            src_reader = TextDataReader()
            tgt_reader = TextDataReader()

            srcs = [src]
            tgts = [tgt]

            dataset = Dataset(
                self._fields,
                readers=[src_reader, tgt_reader],
                data=[("src", srcs), ("tgt", tgts)],
                dirs=[None, None],
                sort_key=None,
                filter_pred=None
            )

            # Create batches
            batches = OrderedIterator(dataset, batch_size=1)

            # Update train steps
            self._train_steps += 1

            # Train the model.
            self.trainer.train(
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
        copytree(self._extended_model.model_dir, new_model_dir, ignore=ignore_patterns('*.pt'))
        model_filename = os.path.basename(self._extended_model.config.opts.models[0])
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
