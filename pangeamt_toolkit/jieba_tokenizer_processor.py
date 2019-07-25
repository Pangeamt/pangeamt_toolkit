import jieba as _jieba

class JiebaTokenizerProcessor:

    @staticmethod
    def tokenize(str, escape=None):
        """ Applies jieba tokenization to str
        """
        return list(_jieba.cut(str))

    @staticmethod
    def detokenize(str_array):
        """ Joins str_array
        """
        return ('').join(str_array)

    @staticmethod
    def preprocess(seg):
        seg.src = JiebaTokenizerProcessor.tokenize(seg.src)

    @staticmethod
    def postprocess(seg):
        seg.tgt = JiebaTokenizerProcessor.detokenize(seg.tgt)
