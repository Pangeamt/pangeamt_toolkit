from sacremoses import MosesTokenizer, MosesDetokenizer
from pangeamt_toolkit.seg.seg import Seg

class Tokenize_process:

    def __init__(self, config):
        self._mtk = MosesTokenizer(lang=config['src_lang'])
        self._mdk = MosesDetokenizer(lang=config['tgt_lang'])

    def preprocess(self, seg):
        seg.src = (' ').join(self._mtk.tokenize(seg.src, escape=False))

    def postprocess(self, seg):
        seg.tgt = self._mdk.detokenize(seg.tgt.split(' '))
