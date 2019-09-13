import jieba as _jieba
from pangeamt_toolkit.processors import ProcessorBase

class JiebaTokenizerProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('tok')

    def tokenize(self, str, escape=None):
        """ Applies jieba tokenization to str
        """
        return list(_jieba.cut(str))

    def detokenize(self, str_array):
        """ Joins str_array
        """
        return ('').join(str_array)

    def preprocess(self, seg):
        seg.src = self.tokenize(seg.src)

    def preprocess_str(self, str):
        return self.tokenize(str)

    def postprocess(self, seg):
        seg.tgt = self.detokenize(seg.tgt)

    def postprocess_str(self, str):
        return self.detokenize(str)
