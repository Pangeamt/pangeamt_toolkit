class ProcessorBase:

    def __init__(self, mod):
        self._src_lang = None
        self._tgt_lang = None
        self._mod = mod

    def initialize(self):
        pass

    def preprocess(self, seg):
        seg.src = seg.src

    def preprocess_str(self, str):
        return str

    def postprocess(self, seg):
        seg.tgt = seg.tgt

    def postprocess_str(self, str):
        return str

    def get_src_lang(self):
        return self._src_lang
    def set_src_lang(self, src_lang):
        self._src_lang = src_lang
    src_lang = property(get_src_lang, set_src_lang)

    def get_tgt_lang(self):
        return self._tgt_lang
    def set_tgt_lang(self, tgt_lang):
        self._tgt_lang = tgt_lang
    tgt_lang = property(get_tgt_lang, set_tgt_lang)

    def get_mod(self):
        return self._mod
    def set_mod(self, mod):
        self._mod = mod
    mod = property(get_mod, set_mod)
