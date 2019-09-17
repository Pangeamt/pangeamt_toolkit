from sacremoses import MosesDetruecaser as _MosesDetruecaser
from sacremoses import MosesTruecaser as _MosesTruecaser
from pangeamt_toolkit.processors import ProcessorBase
from pangeamt_toolkit.seg import SegCase
import re

class MosesTruecasingProcessor(ProcessorBase):

    def __init__(self, model=None):
        super().__init__('truecase')
        if model:
            self._mtr = _PangeaMTTruecaser(model)
        else:
            self._mtr = None
        self._mdr = _MosesDetruecaser()

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

################################################################################

class _PangeaMTTruecaser(_MosesTruecaser):

    def __init__(self, load_from=None, is_asr=None, encoding="utf8"):
        self.SKIP_LETTERS_REGEX = re.compile(u"[{}{}{}]".format(
            self.Lowercase_Letter, self.Uppercase_Letter, self.Titlecase_Letter
        ))

        self.XML_SPLIT_REGX = re.compile("(<.*(?<=>))(.*)((?=</)[^>]*>)")

        self.SENT_END = {".", ":", "?", "!"}
        self.DELAYED_SENT_START = {
            "(",
            "[",
            '"',
            "'",
            "&apos;",
            "&quot;",
            "&#91;",
            "&#93;",
        }

        self.encoding = encoding

        self.is_asr = is_asr
        if load_from:
            self.model = self._load_model(load_from)

    def _load_model(self, path):
        with open(path, 'r') as file:
            best = {}
            known = {}
            for line in file:
                line = line.strip().split()
                most_rep = 0
                for i in range(0, len(line), 2):
                    try:
                        word = line[i]
                        count = int(line[i+1].split('/')[0].strip('()'))
                        if count > most_rep:
                            most_rep = count
                            best[word.lower()] = word
                        known[word] = count
                    except:
                        pass
        return {'best': best, 'known': known}
