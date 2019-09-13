from sacremoses import MosesTokenizer as _MosesTokenizer
from sacremoses import MosesDetokenizer as _MosesDetokenizer
from pangeamt_toolkit.processors import MecabTokenizerProcessor\
    as _Mecab
from pangeamt_toolkit.processors import JiebaTokenizerProcessor\
    as _Jieba
from pangeamt_toolkit.processors import ProcessorBase

class GeneralTokenizerProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('tok')

    def initialize(self):
        if self.src_lang == 'ja':
            self._mtk = _Mecab()
        elif self.src_lang in ['zh', 'tw']:
            self._mtk = _Jieba()
        else:
            self._mtk = _MosesTokenizer(lang=self.src_lang)

        if self.tgt_lang == 'ja':
            self._mdk = _Mecab()
        elif self.tgt_lang in ['zh', 'tw']:
            self._mdk = _Jieba()
        elif self.tgt_lang:
            self._mdk = _MosesDetokenizer(lang=self.tgt_lang)
        else:
            self._mdk = None

    def preprocess(self, seg):
        """ Applies the MosesTokenizer to seg.src
        """
        seg.src = (' ').join(self._mtk.tokenize(seg.src, escape=False))

    def preprocess_str(self, str):
        return (' ').join(self._mtk.tokenize(str, escape=False))

    def postprocess(self, seg):
        """ Applies the MosesDetokenizer to seg.tgt
        """
        if self._mdk:
            seg.tgt = self._mdk.detokenize(seg.tgt.split(' '))
        else:
            pass

    def postprocess_str(self, str):
        if self._mdk:
            return self._mdk.detokenize(str.split(' '))
        else:
            return str
