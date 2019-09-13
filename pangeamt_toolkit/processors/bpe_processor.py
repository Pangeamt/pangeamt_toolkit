from subword_nmt.apply_bpe import BPE as _BPE
from subword_nmt.apply_bpe import read_vocabulary as _rv
from re import sub as _sub
import codecs as _codecs
from pangeamt_toolkit.processors import ProcessorBase

class BPEProcessor(ProcessorBase):

    def __init__(self, bpe_codes, bpe_vocab=None, bpe_threshold=None,\
            bpe_glossaries=None):
        super().__init__('bpe')
        if bpe_glossaries == None:
            _glossaries = []
        else:
            _glossaries = [self._parse_glossary(i) for i in bpe_glossaries]
        if bpe_vocab:
            _vocab = \
                _rv(_codecs.open(bpe_vocab, encoding='utf-8'), bpe_threshold)
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'),\
                vocab=_vocab, glossaries=_glossaries)
        else:
            self._bpe = _BPE(_codecs.open(bpe_codes, encoding='utf-8'))

    def _parse_glossary(self, str):
        return str.encode('utf-8').decode('utf-8')

    def preprocess(self, seg):
        '''Apply BPE to seg.src
        '''
        seg.src = self._bpe.process_line(seg.src)

    def preprocess_str(self, str):
        return self._bpe.process_line(str)

    def postprocess(self, seg):
        '''Remove BPE from seg.tgt
        '''
        seg.tgt = _sub("(@@ )|(@@ ?$)", '', seg.tgt)

    def postprocess_str(self, str):
        return _sub("(@@ )|(@@ ?$)", '', str)
