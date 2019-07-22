import yaml
from pangeamt_toolkit.seg import Seg
from pangeamt_toolkit.bpe_process import BPE_process
from pangeamt_toolkit.truecasing_process import Truecase_process
from pangeamt_toolkit.tokenize_process import Tokenize_process

class Pipeline:
    def __init__(self, config):
        self._processes = {
            'bpe': BPE_process,
            'truecase': Truecase_process,
            'tokenize': Tokenize_process
        }
        with open(config, 'r') as file:
            self._config = yaml.safe_load(file)
        for process in self._processes:
            if process in self._config:
                constructor = self._processes[process]
                params = self._config[process]
                self._processes[process] = constructor(params)
            else:
                raise Exception(f'{process} process not defined')

    def preprocess(self, seg):
        try:
            self._processes['tokenize'].preprocess(seg)
            self._processes['truecase'].preprocess(seg)
            self._processes['bpe'].preprocess(seg)
        except:
            raise Exception('Error')

    def postprocess(self, seg):
        try:
            self._processes['bpe'].postprocess(seg)
            self._processes['truecase'].postprocess(seg)
            self._processes['tokenize'].postprocess(seg)
        except:
            raise Exception('Error')
