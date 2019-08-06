"""Module defining decoders."""
from pangeamt_toolkit.onmt.decoders.decoder import DecoderBase, \
    InputFeedRNNDecoder, StdRNNDecoder
from pangeamt_toolkit.onmt.decoders.transformer import TransformerDecoder
from pangeamt_toolkit.onmt.decoders.cnn_decoder import CNNDecoder


str2dec = {"rnn": StdRNNDecoder, "ifrnn": InputFeedRNNDecoder,
           "cnn": CNNDecoder, "transformer": TransformerDecoder}

__all__ = ["DecoderBase", "TransformerDecoder", "StdRNNDecoder", "CNNDecoder",
           "InputFeedRNNDecoder", "str2dec"]
