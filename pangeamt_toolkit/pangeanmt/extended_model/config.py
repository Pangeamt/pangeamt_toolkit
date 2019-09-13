from __future__ import unicode_literals
import json
import os
from onmt.opts import train_opts as _train_opts, translate_opts as _translate_opts, model_opts as _model_opts
from onmt.utils.parse import ArgumentParser



class Config:
    SRC_LANG = 'src_lang'
    TGT_LANG = 'tgt_lang'
    ONLINE_LEARNING = 'online_learning'

    def __init__(self, model_dir):

        # Model dir
        self._model_dir = model_dir

        # Get pt file
        model_files = []
        for file in os.listdir(f'{self._model_dir}/translation_model'):
            if file.endswith(".pt"):
                model_files.append(os.path.join(model_dir,'translation_model', file))
        if len(model_files) != 1:
            msg = f"Extended model {self._model_dir} sould have one .pt file. {len(model_files)}"
            raise ValueError(msg)
        model_file = model_files[0]

        # Load config from file
        config_path = os.path.join(model_dir, "config.json")

        # Load config from json file
        with open(config_path) as f:
            config = json.load(f)

        # Langs
        self._src_lang = config[self.SRC_LANG]
        self._tgt_lang = config[self.TGT_LANG]

        # Online learning
        if  self.ONLINE_LEARNING in config:
            self._online_learning = _OnlineLearningConfig(config[self.ONLINE_LEARNING])
        else:
            self._online_learning = _OnlineLearningConfig()

        # Create a parser for train and translate options
        parser = ArgumentParser(description='pangeanmt options',  conflict_handler='resolve')

        # Parser for translate options
        _translate_opts(parser)

        # Parser for training options
        _train_opts(parser)

        # Parser for model options
        _model_opts(parser)

        # --src argument is not used
        parser.add_argument('--src', '-src', required=False,
                            help="This argument isn't used!")

        # --data argument is not used
        parser.add_argument('--data', '-data', required=False,
                            help="This argument isn't used!")

        # --seed Overwrite default
        parser.add_argument('--seed', '-seed', required=False, default=829,
                            help="Seed")

        # Create opts from config
        args = ['--model', model_file]
        for k, v in config['opts'].items():
            args.append('--'+ k)
            if v is not None:
                if k == 'model':
                    v = os.path.join(model_dir, v)
                args.append(str(v))
        self._opts = parser.parse_args(args)

    def get_src_lang(self):
        return self._src_lang
    src_lang = property(get_src_lang)

    def get_tgt_lang(self):
        return self._tgt_lang
    tgt_lang = property(get_tgt_lang)

    def get_opts(self):
        return self._opts
    opts = property(get_opts)

    def get_online_learning(self):
        return self._online_learning
    online_learning = property(get_online_learning)


class _OnlineLearningConfig:
    ACTIVE = 'active'
    STEPS = 'steps'
    def __init__(self, opts=None):
        if opts is None:
            self._active = False
            self._steps = 0
        else:
            self._active = opts[self.ACTIVE]
            self._steps = opts[self.STEPS]

    def get_active(self):
        return self._active
    is_active = property(get_active)

    def get_steps(self):
        return self._steps
    steps = property(get_steps)
