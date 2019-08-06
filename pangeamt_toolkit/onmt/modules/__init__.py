"""  Attention and normalization modules  """
from pangeamt_toolkit.onmt.modules.util_class import Elementwise
from pangeamt_toolkit.onmt.modules.gate import context_gate_factory, ContextGate
from pangeamt_toolkit.onmt.modules.global_attention import GlobalAttention
from pangeamt_toolkit.onmt.modules.conv_multi_step_attention import ConvMultiStepAttention
from pangeamt_toolkit.onmt.modules.copy_generator import CopyGenerator, CopyGeneratorLoss, \
    CopyGeneratorLossCompute
from pangeamt_toolkit.onmt.modules.multi_headed_attn import MultiHeadedAttention
from pangeamt_toolkit.onmt.modules.embeddings import Embeddings, PositionalEncoding
from pangeamt_toolkit.onmt.modules.weight_norm import WeightNormConv2d
from pangeamt_toolkit.onmt.modules.average_attn import AverageAttention

__all__ = ["Elementwise", "context_gate_factory", "ContextGate",
           "GlobalAttention", "ConvMultiStepAttention", "CopyGenerator",
           "CopyGeneratorLoss", "CopyGeneratorLossCompute",
           "MultiHeadedAttention", "Embeddings", "PositionalEncoding",
           "WeightNormConv2d", "AverageAttention"]
