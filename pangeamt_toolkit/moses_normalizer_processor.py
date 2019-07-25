from sacremoses import MosesPunctNormalizer as _MosesNormalizer

class MosesNormalizerProcessor:

    def __init__(self, src_lang, tgt_lang):
        self._mn_src = _MosesNormalizer(lang=src_lang)
        self._mn_tgt = _MosesNormalizer(lang=tgt_lang)

    def preprocess(self, seg):
        """ Applies the MosesNormalizer to seg.src
        """
        seg.src = self._mn_src.normalize(seg.src)

    def postprocess(self, seg):
        """ Applies the MosesNormalizer to seg.tgt
        """
        seg.tgt = self._mn_tgt.normalize(seg.tgt)
