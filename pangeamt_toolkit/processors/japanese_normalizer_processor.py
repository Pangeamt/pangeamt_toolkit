import neologdn as _neologdn

class JapaneseNormalizerProcessor:

    def __init__(self):
        self._mod = 'janorm'

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    def preprocess(self, seg):
        seg.src = _neologdn.normalize(seg.src, repeat=1)

    def preprocess_str(self, str):
        return _neologdn.normalize(str, repeat=1)

    def postprocess(self, seg):
        seg.tgt = seg.tgt

    def postprocess_str(self, str):
        return str
