from sacremoses import MosesTokenizer as _MosesTokenizer
from sacremoses import MosesDetokenizer as _MosesDetokenizer
from MeCab import Tagger as _Tagger

class MecabTokenizerProcessor:

    def __init__(self):
        self._tok = _Tagger('-Owakati')

    def tokenize(self, str, escape=None):
        """ Applies mecab tokenization to str
        """
        t = self._tok.parse(str).split(' ')
        #print(t, '\n', t[:-1])
        return t[:-1]

    def detokenize(self, str_array):
        """ Joins str_array
        """
        return ('').join(str_array)

    def preprocess(seg):
        seg.src = self.tokenize(seg.src)

    def postprocess(seg):
        seg.tgt = self.detokenize(seg.tgt)
