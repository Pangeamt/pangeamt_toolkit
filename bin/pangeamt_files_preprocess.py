#!/usr/bin/env python

import json
import argparse
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('config', help="Path to config file")
parser.add_argument('data', help="Path to data folder")
parser.add_argument('src', help='Src lang')
parser.add_argument('tgt', help='Tgt lang')

args = parser.parse_args()

langs = [args.src, args.tgt]

with open(args.config, 'r') as config_file:
    config = json.load(config_file)
    pipelines = {
            args.src: Pipeline(config['pipeline_config']),
            args.tgt: Pipeline(config['pipeline_config_tgt'])
        }

for lang in langs:
    pipeline = pipelines[lang]
    mods = 'norm.tok.truecase.bpe'
    paths = {
        f'{args.data}/train.{lang}': f'{args.data}/train.{mods}.{lang}',
        f'{args.data}/dev.{lang}': f'{args.data}/dev.{mods}.{lang}',
        f'{args.data}/test.{lang}': f'{args.data}/test.{mods}.{lang}'
    }
    for path in paths:
        print(f'Started processing {path.split('/')[-1]}')
        pipeline.preprocess_file(path, paths[path])
        print(f'Finnished processing {path.split('/')[-1]}')
