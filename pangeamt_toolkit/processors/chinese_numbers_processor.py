import re as _re
from pycnnum import cn2num as _cn2num
from pangeamt_toolkit.processors import ProcessorBase


class ChineseNumberProcessor(ProcessorBase):

    def __init__(self):
        super().__init__('cnnum2ar')

    @staticmethod
    def _get_numbers(text):
        return set(_re.findall(r'[十百千万亿一二三四五六七八九]+', text))

    @staticmethod
    def cn2ar(text):
        for seq in ChineseNumberProcessor._get_numbers(text):
            text = text.replace(seq, str(_cn2num(seq, numbering_type="mid")))
        return text

    def preprocess(self, seg):
        seg.src = ChineseNumberProcessor.cn2ar(seg.src)

    def preprocess_str(self, str):
        return ChineseNumberProcessor.cn2ar(str)
