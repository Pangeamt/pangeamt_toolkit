#!/usr/bin/env python

import os
import json
import argparse
from multiprocessing import Process
from pangeamt_toolkit.processors import Pipeline

parser = argparse.ArgumentParser(description='Preprocess file.')
parser.add_argument('data', help="Path to data folder")
parser.add_argument('src', help='Src lang')
parser.add_argument('tgt', help='Tgt lang')

args = parser.parse_args()

langs = [args.src, args.tgt]

def config_builder(lang):
    return [
        {
            'name': 'normalizer',
            'args': [lang]
        },
        {
            'name': 'tokenize',
            'args': [lang]
        }
    ]

src_config = config_builder(args.src)
pipeline_src = Pipeline(src_config)

tgt_config = config_builder(args.tgt)
pipeline_tgt = Pipeline(tgt_config)

pipelines = {args.src: pipeline_src, args.tgt: pipeline_tgt}

def process(lang, pipelines):
    pipeline = pipelines[lang]
    path = f'{args.data}/train.{lang}'
    if os.path.isfile(path):
        print(f"Started processing {path.split('/')[-1]}..")
        pipeline.preprocess_file(path)
        print(f"Finished processing {path.split('/')[-1]}..")
    else:
        raise Exception(f'Missing {path} file')

to_join = []
for lang in langs:
    p = Process(target=process, args=(lang, pipelines,))
    p.start()
    to_join.append(p)

for p in to_join:
    p.join()
