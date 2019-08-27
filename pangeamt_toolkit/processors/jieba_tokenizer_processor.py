import jieba as _jieba

class JiebaTokenizerProcessor:

    def __init__(self):
        self._mod = 'tok'

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

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

    def preprocess_str(self, seg):
        return self.tokenize(str)

    def postprocess(self, seg):
        seg.tgt = self.detokenize(seg.tgt)

    def postprocess_str(self, str):
        return self.detokenize(str)
