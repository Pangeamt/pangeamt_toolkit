from sacremoses import MosesPunctNormalizer as _MosesNormalizer
from pangeamt_toolkit.processors import ProcessorBase

class MosesNormalizerProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('norm')

    def initialize(self):
        self._mn_src = _MosesNormalizer(self.src_lang)
        if self.tgt_lang:
            self._mn_tgt = _MosesNormalizer(self.tgt_lang)
        else:
            self._mn_tgt = None

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
