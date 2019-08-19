import jieba as _jieba

class JiebaTokenizerProcessor:

    @staticmethod
    def tokenize(str, escape=None):
        self._mod = 'tok'
        """ Applies jieba tokenization to str
        """
        return list(_jieba.cut(str))

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    @staticmethod
    def detokenize(str_array):
        """ Joins str_array
        """
        return ('').join(str_array)

    @staticmethod
    def preprocess(seg):
        seg.src = JiebaTokenizerProcessor.tokenize(seg.src)

    @staticmethod
    def preprocess_str(seg):
        return JiebaTokenizerProcessor.tokenize(str)

    @staticmethod
    def postprocess(seg):
        seg.tgt = JiebaTokenizerProcessor.detokenize(seg.tgt)

    @staticmethod
    def postprocess_str(str):
        return JiebaTokenizerProcessor.detokenize(str)
