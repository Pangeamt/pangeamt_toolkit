from sacremoses import MosesTruecaser, MosesDetruecaser
from seg.seg import Seg
from seg.seg_case import Seg_case

class Truecase_process:

    def __init__(self, config):
        self._mtr = MosesTruecaser(config['model'])
        self._mdr = MosesDetruecaser()

    def preprocess(self, seg):
        if seg.src.isupper():
            seg.src_case = Seg_case.UPPER
        elif seg.src.islower():
            seg.src_case = Seg_case.LOWER
        else:
            seg.src_case = Seg_case.MIXED

        seg.src = (' ').join(self._mtr.truecase(seg.src))

    def postprocess(self, seg):
        if seg.src_case == Seg_case.UPPER:
            seg.tgt = seg.tgt.upper()
        elif seg.src_case == Seg_case.LOWER:
            seg.tgt = seg.tgt.lower()
        else:
            seg.tgt = (' ').join(self._mdr.detruecase(seg.tgt))
