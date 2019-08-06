import os
from pangeamt_toolkit.pangeanmt.extended_model.config import Config

class ExtendedModel:
    def __init__(self, model_dir):
        self._model_dir = os.path.abspath(model_dir)
        self._config = Config(self._model_dir)


    def get_model_dir(self):
        return self._model_dir
    model_dir = property(get_model_dir)

    def get_config(self):
        return self._config
    config = property(get_config)
