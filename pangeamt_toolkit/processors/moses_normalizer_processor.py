from sacremoses import MosesPunctNormalizer as _MosesNormalizer

class MosesNormalizerProcessor:

    def __init__(self, src_lang, tgt_lang=None):
        self._mod = 'norm'
        self._mn_src = _MosesNormalizer(lang=src_lang)
        if tgt_lang:
            self._mn_tgt = _MosesNormalizer(lang=tgt_lang)
        else:
            self._mn_tgt = None

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    def preprocess(self, seg):
        """ Applies the MosesNormalizer to seg.src
        """
        seg.src = self._mn_src.normalize(seg.src)

    def preprocess_str(self, str):
        return self._mn_src.normalize(str)

    def postprocess(self, seg):
        """ Applies the MosesNormalizer to seg.tgt
        """
        seg.tgt = self._mn_tgt.normalize(seg.tgt)

    def postprocess_str(self, str):
        return self._mn_tgt.normalize(str)
