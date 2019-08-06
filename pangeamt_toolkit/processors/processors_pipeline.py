import yaml as _yaml
from re import sub as _sub

class Pipeline:

    def __init__(self, processors):
        """ processors is a list of dicts from the general config file
            with this structure:
                {
                    'name': processor's shortname,
                    'args': [list of the processor's args]
                }
        """
        self._processes = []
        for process in processors:
            processor = self._PROCESSORS[process['name']]
            klass_name = processor['class']
            path = processor['path']
            args = process['args']
            mod = __import__(path, fromlist=[klass_name])
            klass = getattr(mod, klass_name)
            processor = klass(*args)
            self._processes.append(processor)

    def preprocess(self, seg):
        for process in self._processes:
            process.preprocess(seg)

    def preprocess_str(self, str):
        for process in self._processes:
            try:
                str, _ = process.preprocess_str(str)
            except:
                str = process.preprocess_str(str)
        return str

    def preprocess_file(self, src_path, tgt_path):
        with open(src_path, 'r') as src_file:
            with open(tgt_path, 'w+') as tgt_file:
                for line in src_file.readlines():
                    line = self.preprocess_str(line)
                    line = _sub('.', '.\n', line)
                    if line[-1:] == '\n':
                        tgt_file.write(line)
                    else:
                        tgt_file.write(line + '\n')


    def postprocess(self, seg):
        processes = self._processes[::-1]
        for process in processes:
            process.postprocess(seg)

    def postprocess_str(self, str):
        processes = self._processes[::-1]
        for process in processes:
            str = process.postprocess_str(str)
        return str

    def postprocess_file(self, src_path, tgt_path):
        with open(src_path, 'r') as src_file:
            with open(tgt_path, 'w+') as tgt_file:
                for line in src_file.readlines():
                    line = self.postprocess_str(line)
                    tgt_file.write(line + '\n')

    _PROCESSORS = {
        'tokenize':{
            'class': 'GeneralTokenizerProcessor',
            'path': 'pangeamt_toolkit.processors.general_tokenizer_processor'
        },

        'moses_tokenize':{
            'class': 'MosesTokenizerProcessor',
            'path': 'pangeamt_toolkit.processors.moses_tokenizer_processor'
        },

        'jieba_tokenize':{
            'class': 'JiebaTokenizerProcessor',
            'path': 'pangeamt_toolkit.processors.jieba_tokenizer_processor'
        },

        'mecab_tokenize':{
            'class': 'MecabTokenizerProcessor',
            'path': 'pangeamt_toolkit.processors.mecab_tokenizer_processor'
        },

        'truecase':{
            'class': 'MosesTruecasingProcessor',
            'path': 'pangeamt_toolkit.processors.moses_truecasing_processor'
        },

        'normalizer':{
            'class': 'MosesNormalizerProcessor',
            'path': 'pangeamt_toolkit.processors.moses_normalizer_processor'
        },

        'bpe':{
            'class': 'BPEProcessor',
            'path': 'pangeamt_toolkit.processors.bpe_processor'
        }
    }
