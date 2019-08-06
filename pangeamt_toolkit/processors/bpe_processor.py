from subword_nmt.apply_bpe import BPE as _BPE
from subword_nmt.apply_bpe import read_vocabulary as _rv
from re import sub as _sub
import codecs as _codecs


class BPEProcessor:

    def __init__(self, bpe_codes, bpe_vocab=None, bpe_threshold=None):
        if bpe_vocab:
            _vocab = \
                _rv(_codecs.open(bpe_vocab, encoding='utf-8'), bpe_threshold)
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'),\
                vocab=_vocab)
        else:
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'))

    def preprocess(self, seg):
        '''Apply BPE to seg.src
        '''
        seg.src = self._bpe.segment(seg.src)

    def preprocess_str(self, str):
        return self._bpe.segment(str)

    def postprocess(self, seg):
        '''Remove BPE from seg.tgt
        '''
        seg.tgt = _sub("(@@ )|(@@ ?$)", '', seg.tgt)

    def postprocess_str(self, str):
        return _sub("(@@ )|(@@ ?$)", '', str)
