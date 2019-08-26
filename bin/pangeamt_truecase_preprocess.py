#!/usr/bin/env python
import json
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('truecase_model', help='Path to truecase model.')
parser.add_argument('src_file', help='Path to src file.')

args = parser.parse_args()

processors = [{
        'name': 'truecase',
        'args': [args.truecase_model]
    }]

pipeline = Pipeline(processors)

print(f'Started truecasing of {args.src_file}')
pipeline.preprocess_file(args.src_file)
print(f'Finished truecasing of {args.src_file}')
