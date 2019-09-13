import neologdn as _neologdn
from pangeamt_toolkit.processors import ProcessorBase

class JapaneseNormalizerProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('janorm')

    def preprocess(self, seg):
        seg.src = _neologdn.normalize(seg.src, repeat=1)

    def preprocess_str(self, str):
        return _neologdn.normalize(str, repeat=1)
