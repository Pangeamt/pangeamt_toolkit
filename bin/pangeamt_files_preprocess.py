#!/usr/bin/env python

import os
import json
import argparse
from multiprocessing import Process
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
    print('Loading pipelines..')
    pipelines = {
            args.src: Pipeline(config['pipeline_config']),
            args.tgt: Pipeline(config['pipeline_config_tgt'])
        }
    print('Pipelines loaded..')

def process(lang, pipelines):
    pipeline = pipelines[lang]

    files = ['train', 'dev', 'test']

    for file in files:
        path = f'{args.data}/{file}.{lang}'
        if os.path.isfile(path):
            print(f"Started processing {path.split('/')[-1]}")
            pipeline.preprocess_file(path)
            print(f"Finished processing {path.split('/')[-1]}")
        else:
            pass

to_join = []

for lang in langs:
    p = Process(target=process, args=(lang, pipelines,))
    p.start()
    to_join.append(p)

for p in to_join:
    p.join()
