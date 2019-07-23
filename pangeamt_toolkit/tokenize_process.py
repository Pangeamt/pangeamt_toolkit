from sacremoses import MosesTokenizer as _MosesTokenizer
from sacremoses import MosesDetokenizer as _MosesDetokenizer
from pangeamt_toolkit.seg import Seg

class Tokenize_process:

    def __init__(self, src_lang, tgt_lang):
        self._mtk = _MosesTokenizer(lang=src_lang)
        self._mdk = _MosesDetokenizer(lang=tgt_lang)

    def preprocess(self, seg):
        """ Applies the MosesTokenizer to seg.src
        """
        seg.src = (' ').join(self._mtk.tokenize(seg.src, escape=False))

    def postprocess(self, seg):
        """ Applies the MosesDetokenizer to seg.tgt
        """
        seg.tgt = self._mdk.detokenize(seg.tgt.split(' '))
