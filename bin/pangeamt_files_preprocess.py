#!/usr/bin/env python

import yaml
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('processors', help="Path to yml processors file")
parser.add_argument('data', help="Path to data folder")
parser.add_argument('src', help='Src lang')
parser.add_argument('tgt', help='Tgt lang')

args = parser.parse_args()

langs = [args.src, args.tgt]

for lang in langs:
    processors_file = f'{args.processors}.{lang}.yml'
    with open(processors_file, 'r') as p_file:
        processors = yaml.safe_load(p_file)

    pipeline = Pipeline(processors)
    mods = 'norm.tok.truecase.bpe'
    paths = {
        f'{args.data}/train.{lang}': f'{args.data}/train.{mods}.{lang}',
        f'{args.data}/dev.{lang}': f'{args.data}/dev.{mods}.{lang}',
        f'{args.data}/test.{lang}': f'{args.data}/test.{mods}.{lang}'
    }
    for path in paths:
        pipeline.preprocess_file(path, paths[path])
