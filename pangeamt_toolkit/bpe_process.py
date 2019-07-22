from pangeamt_toolkit.apply_bpe import BPE
from pangeamt_toolkit.seg import Seg
from re import sub
import codecs


class BPE_process:

    def __init__(self, config):
        bpe_codes = config['bpe_codes']
        bpe_vocab = config.get('bpe_vocab', None)
        bpe_threshold = config.get('bpe_threshold', None)
        if bpe_vocab:
            self._bpe = BPE(codecs.open(bpe_codes, encoding='utf-8'),\
                vocab=codecs.open(bpe_vocab, encoding='utf-8'),\
                vocab_threshold=bpe_threshold)
        else:
            self._bpe = BPE(codecs.open(bpe_codes, encoding='utf-8'))

    def preprocess(self, seg):
        '''Apply BPE to seg.src'''
        seg.src = self._bpe.segment(seg.src)

    def postprocess(self, seg):
        '''Remove BPE from seg.tgt'''
        seg.tgt = sub("(@@ )|(@@ ?$)", '', seg.tgt)
