from sacremoses import MosesPunctNormalizer as _MosesPunctNormalizer

class PunctProcessor:

    def __init__(self, lang):
        self._mod = 'punct'
        self._mpn = _MosesPunctNormalizer(lang)

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    def preprocess(self, seg):
        seg.src = self._mpn.normalize(seg.src)

    def preprocess_str(self, seg):
        return self._mpn.normalize(str)

    def postprocess(self, seg):
        seg.tgt = seg.tgt

    def postprocess_str(self, str):
        return str
