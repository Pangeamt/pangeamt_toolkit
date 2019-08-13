#!/usr/bin/env python
import json
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Postprocess file.')
parser.add_argument('config', help='Path to config file.')
parser.add_argument('src_file', help='Path to src file.')
parser.add_argument('tgt_file', help='Path to tgt file.')

args = parser.parse_args()

with open(args.config, 'r') as c_file:
    config = json.load(c_file)
    processors = config['pipeline_config_tgt']

pipeline = Pipeline(processors)

pipeline.postprocess_file(args.src_file, args.tgt_file)
