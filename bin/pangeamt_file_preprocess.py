#!/usr/bin/env python
import json
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('config', help='Path to config file.')
parser.add_argument('src_file', help='Path to src file.')

args = parser.parse_args()

with open(args.config, 'r') as c_file:
    config = json.load(c_file)
    processors = config['pipeline_config']

pipeline = Pipeline(processors)

pipeline.preprocess_file(args.src_file)
