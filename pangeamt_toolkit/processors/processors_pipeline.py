import os
import yaml as _yaml
from re import sub as _sub

class Pipeline:

    def __init__(self, processors, src_lang=None, tgt_lang=None):
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
            try:
                args = process['args']
            except:
                args = []
            mod = __import__(path, fromlist=[klass_name])
            klass = getattr(mod, klass_name)
            processor = klass(*args)
            if src_lang:
                processor.src_lang = src_lang
            if tgt_lang:
                processor.tgt_lang = tgt_lang
            processor.initialize()
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

    def preprocess_file(self, src_path, tgt_path=None):
        if tgt_path:
            with open(src_path, 'r') as src_file:
                with open(tgt_path, 'w+') as tgt_file:
                    for line in src_file:
                        line = self.preprocess_str(line)
                        if line[-1:] == '\n':
                            tgt_file.write(line)
                        else:
                            tgt_file.write(line + '\n')
        else:
            src_path_list = src_path.split('/')
            src_mods = src_path_list[-1].split('.')[1:-1]
            src_name_raw = src_path_list[-1].split('.')[0]
            src_lang = src_path_list[-1].split('.')[-1]
            path = ('/').join(src_path_list[:-1])
            for process in self._processes:
                if process.mod not in src_mods:
                    src_mods.append(process.mod)
                    tgt_path = f"{path}/{src_name_raw}.{('.').join(src_mods)}."\
                        f'{src_lang}'
                    self._preprocess_file(process, src_path, tgt_path)
                    src_path = tgt_path
                else:
                    pass


    def _preprocess_file(self, process, src_path, tgt_path):
        if os.path.exists(tgt_path):
            pass
        else:
            with open(src_path, 'r') as src_file:
                with open(tgt_path, 'w+') as tgt_file:
                    for line in src_file:
                        try:
                            line, _ = process.preprocess_str(line)
                        except:
                            line = process.preprocess_str(line)
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
                for line in src_file:
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
        },

        'placeholder':{
            'class': 'PlaceholderProcessor',
            'path': 'pangeamt_toolkit.processors.placeholder_processor'
        },

        'punct':{
            'class': 'PunctProcessor',
            'path': 'pangeamt_toolkit.processors.punct_processor'
        },

        'japanese_normalizer':{
            'class': 'JapaneseNormalizerProcessor',
            'path': 'pangeamt_toolkit.processors.japanese_normalizer_processor'
        },
    }
