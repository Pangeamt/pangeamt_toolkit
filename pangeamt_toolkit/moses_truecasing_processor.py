from sacremoses import MosesTruecaser as _MosesTruecaser
from sacremoses import MosesDetruecaser as _MosesDetruecaser
from pangeamt_toolkit.seg_case import Seg_case

class MosesTruecasingProcessor:

    def __init__(self, model):
        self._mtr = _MosesTruecaser(model)
        self._mdr = _MosesDetruecaser()

    def preprocess(self, seg):
        """ Checks if the seg.src string is writen in lowercase, uppercase
            or both, and writes the casing to seg.src_case then it applies
            the MosesTruecaser.
        """
        if seg.src.isupper():
            seg.src_case = Seg_case.UPPER
        elif seg.src.islower():
            seg.src_case = Seg_case.LOWER
        else:
            seg.src_case = Seg_case.MIXED

        seg.src = (' ').join(self._mtr.truecase(seg.src))

    def postprocess(self, seg):
        """ Modifies seg.tgt according to seg.src_case.
        """
        if seg.src_case == Seg_case.UPPER:
            seg.tgt = seg.tgt.upper()
        elif seg.src_case == Seg_case.LOWER:
            seg.tgt = seg.tgt.lower()
        else:
            seg.tgt = (' ').join(self._mdr.detruecase(seg.tgt))
