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

    train_paths = [f'{args.data}/train.norm.tok.truecase.bpe.{lang}',
    f'{args.data}/train.norm.tok.truecase.{lang}',
    f'{args.data}/train.norm.tok.{lang}',
    f'{args.data}/train.norm.{lang}', f'{args.data}/train.{lang}']

    dev_paths = [f'{args.data}/dev.norm.tok.truecase.bpe.{lang}',
    f'{args.data}/dev.norm.tok.truecase.{lang}',
    f'{args.data}/dev.norm.tok.{lang}',
    f'{args.data}/dev.norm.{lang}', f'{args.data}/dev.{lang}']

    test_paths = [f'{args.data}/test.norm.tok.truecase.bpe.{lang}',
    f'{args.data}/test.norm.tok.truecase.{lang}',
    f'{args.data}/test.norm.tok.{lang}',
    f'{args.data}/test.norm.{lang}', f'{args.data}/test.{lang}']

    paths = [train_paths, dev_paths, test_paths]

    for path_group in paths:
        for path in path_group:
            if os.path.isfile(path):
                print(f"Started processing {path.split('/')[-1]}")
                pipeline.preprocess_file(path)
                print(f"Finished processing {path.split('/')[-1]}")
                break
            else:
                pass

to_join = []

for lang in langs:
    p = Process(target=process, args=(lang, pipelines,))
    p.start()
    to_join.append(p)

for p in to_join:
    p.join()
