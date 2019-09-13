from sacremoses import MosesPunctNormalizer as _MosesPunctNormalizer
from pangeamt_toolkit.processors import ProcessorBase

class PunctProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('punct')

    def initialize(self):
        self._mpn = _MosesPunctNormalizer(self.src_lang)

    def preprocess(self, seg):
        seg.src = self._mpn.normalize(seg.src)

    def preprocess_str(self, str):
        return self._mpn.normalize(str)
