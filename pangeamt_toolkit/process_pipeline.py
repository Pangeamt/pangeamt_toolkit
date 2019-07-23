import yaml as _yaml
from pangeamt_toolkit.seg import Seg

class Pipeline:
    def __init__(self, config):
        with open(config, 'r') as file:
            self._config = _yaml.safe_load(file)
        self._processes = []
        for process in self._config:
            klass_name = self._config[process]['class']
            path = self._config[process]['path']
            args = self._config[process]['args']
            mod = __import__(path, fromlist=[klass_name])
            klass = getattr(mod, klass_name)
            processor = klass(**args)
            self._processes.append(processor)

    def preprocess(self, seg):
        for process in self._processes:
            process.preprocess(seg)

    def postprocess(self, seg):
        processes = self._processes[::-1]
        for process in processes:
            process.postprocess(seg)
