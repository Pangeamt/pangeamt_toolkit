from sacremoses import MosesTruecaser as _MosesTruecaser
from sacremoses import MosesDetruecaser as _MosesDetruecaser
from pangeamt_toolkit.seg import SegCase

class MosesTruecasingProcessor:

    def __init__(self, model=None):
        self._mod = 'truecase'
        if model:
            self._mtr = _MosesTruecaser(model)
        else:
            self._mtr = None
        self._mdr = _MosesDetruecaser()

    def get_mod(self):
        return self._mod
    mod = property(get_mod)

    def preprocess(self, seg):
        """ Checks if the seg.src string is writen in lowercase, uppercase
            or both, and writes the casing to seg.src_case then it applies
            the MosesTruecaser.
        """
        if seg.src.isupper():
            seg.src_case = SegCase.UPPER
        elif seg.src.islower():
            seg.src_case = SegCase.LOWER
        else:
            seg.src_case = SegCase.MIXED
        if self._mtr:
            seg.src = (' ').join(self._mtr.truecase(seg.src))
        else:
            seg.src = seg.src

    def preprocess_str(self, str):
        if self._mtr:
            if str.isupper():
                return (' ').join(self._mtr.truecase(str)), SegCase.UPPER
            elif str.islower():
                return (' ').join(self._mtr.truecase(str)), SegCase.LOWER
            else:
                return (' ').join(self._mtr.truecase(str)), SegCase.MIXED
        else:
            if str.isupper():
                return str, SegCase.UPPER
            elif str.islower():
                return str, SegCase.LOWER
            else:
                return str, SegCase.MIXED

    def postprocess(self, seg):
        """ Modifies seg.tgt according to seg.src_case.
        """
        if seg.src_case == SegCase.UPPER:
            seg.tgt = seg.tgt.upper()
        elif seg.src_case == SegCase.LOWER:
            seg.tgt = seg.tgt.lower()
        else:
            seg.tgt = (' ').join(self._mdr.detruecase(seg.tgt))

    def postprocess_str(self, str, casing=None):
        if casing == SegCase.UPPER:
            return str.upper()
        elif casing == SegCase.LOWER:
            return str.lower()
        else:
            return (' ').join(self._mdr.detruecase(str))
