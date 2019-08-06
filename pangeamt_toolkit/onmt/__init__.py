""" Main entry point of the ONMT library """
from __future__ import division, print_function

import pangeamt_toolkit.onmt.inputters
import pangeamt_toolkit.onmt.encoders
import pangeamt_toolkit.onmt.decoders
import pangeamt_toolkit.onmt.models
import pangeamt_toolkit.onmt.utils
import pangeamt_toolkit.onmt.modules
from pangeamt_toolkit.onmt.trainer import Trainer
import sys
import pangeamt_toolkit.onmt.utils.optimizers
#optimizers.Optim = pangeamt_toolkit.onmt.utils.optimizers.Optimizer
#sys.modules["onmt.Optim"] = pangeamt_toolkit.onmt.utils.optimizers

# For Flake
__all__ = ['pangeamt_toolkit.onmt.inputters',
    'pangeamt_toolkit.onmt.encoders', 'pangeamt_toolkit.onmt.decoders',
    'pangeamt_toolkit.onmt.models', 'pangeamt_toolkit.onmt.utils',
    'pangeamt_toolkit.onmt.modules', "Trainer"]

__version__ = "0.9.1"
