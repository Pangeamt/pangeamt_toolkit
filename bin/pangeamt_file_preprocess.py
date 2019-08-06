#!/usr/bin/env python
import yaml
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('processors', help='Yml file that contains the processes.')
parser.add_argument('src_file', help='Path to src file.')
parser.add_argument('tgt_file', help='Path to tgt file.')

args = parser.parse_args()

with open(args.processors, 'r') as p_file:
    processors = yaml.safe_load(p_file)

pipeline = Pipeline(processors)

pipeline.preprocess_file(args.src_file, args.tgt_file)
