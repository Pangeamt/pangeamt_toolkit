from sacremoses import MosesTokenizer as _MosesTokenizer
from sacremoses import MosesDetokenizer as _MosesDetokenizer
from pangeamt_toolkit.mecab_tokenizer_processor import MecabTokenizerProcessor\
    as _Mecab
from pangeamt_toolkit.jieba_tokenizer_processor import JiebaTokenizerProcessor\
    as _Jieba

class GeneralTokenizerProcessor:

    def __init__(self, src_lang, tgt_lang):
        if src_lang == 'ja':
            self._mtk = _Mecab()
        elif src_lang == 'ch':
            self._mtk = _Jieba()
        else:
            self._mtk = _MosesTokenizer(lang=src_lang)

        if tgt_lang == 'ja':
            self._mdk = _Mecab()
        elif tgt_lang == 'ch':
            self._mdk = _Jieba()
        else:
            self._mdk = _MosesDetokenizer(lang=tgt_lang)

    def preprocess(self, seg):
        """ Applies the MosesTokenizer to seg.src
        """
        seg.src = (' ').join(self._mtk.tokenize(seg.src, escape=False))

    def postprocess(self, seg):
        """ Applies the MosesDetokenizer to seg.tgt
        """
        seg.tgt = self._mdk.detokenize(seg.tgt.split(' '))
