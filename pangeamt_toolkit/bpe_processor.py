from subword_nmt.apply_bpe import BPE as _BPE
from subword_nmt.apply_bpe import read_vocabulary as rv
from re import sub as _sub
import codecs as _codecs


class BPEProcessor:

    def __init__(self, bpe_codes, bpe_vocab=None, bpe_threshold=None):
        if bpe_vocab:
            _vocab = \
                rv(_codecs.open(bpe_vocab, encoding='utf-8'), bpe_threshold)
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'),\
                vocab=_vocab, vocab_threshold=bpe_threshold)
        else:
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'))

    def preprocess(self, seg):
        '''Apply BPE to seg.src
        '''
        seg.src = self._bpe.segment(seg.src)

    def postprocess(self, seg):
        '''Remove BPE from seg.tgt
        '''
        seg.tgt = _sub("(@@ )|(@@ ?$)", '', seg.tgt)
