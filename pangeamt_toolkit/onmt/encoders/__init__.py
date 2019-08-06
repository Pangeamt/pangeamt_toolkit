"""Module defining encoders."""
from pangeamt_toolkit.onmt.encoders.encoder import EncoderBase
from pangeamt_toolkit.onmt.encoders.transformer import TransformerEncoder
from pangeamt_toolkit.onmt.encoders.rnn_encoder import RNNEncoder
from pangeamt_toolkit.onmt.encoders.cnn_encoder import CNNEncoder
from pangeamt_toolkit.onmt.encoders.mean_encoder import MeanEncoder
from pangeamt_toolkit.onmt.encoders.audio_encoder import AudioEncoder
from pangeamt_toolkit.onmt.encoders.image_encoder import ImageEncoder


str2enc = {"rnn": RNNEncoder, "brnn": RNNEncoder, "cnn": CNNEncoder,
           "transformer": TransformerEncoder, "img": ImageEncoder,
           "audio": AudioEncoder, "mean": MeanEncoder}

__all__ = ["EncoderBase", "TransformerEncoder", "RNNEncoder", "CNNEncoder",
           "MeanEncoder", "str2enc"]
