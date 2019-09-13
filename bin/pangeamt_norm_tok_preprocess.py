#!/usr/bin/env python

import os
import json
import argparse
from multiprocessing import Process
from pangeamt_toolkit.processors import Pipeline

def _get_parser():
    parser = argparse.ArgumentParser(description='Preprocess file.')
    parser.add_argument('data', help="Path to data folder")
    parser.add_argument('src', help='Src lang')
    parser.add_argument('tgt', help='Tgt lang')
    return parser

# Builds a config for applying only norm and tok
def _config_builder():
    return [
        {
            'name': 'normalizer'
        },
        {
            'name': 'tokenize'
        }
    ]

def _process(path, lang, pipelines):
    pipeline = pipelines[lang]
    complete_path = f'{path}/train.{lang}'
    if os.path.isfile(complete_path):
        print(f"Started processing {complete_path.split('/')[-1]}..")
        pipeline.preprocess_file(complete_path)
        print(f"Finished processing {complete_path.split('/')[-1]}..")
    else:
        raise Exception(f'Missing {complete_path} file')

def main(args):

    config = _config_builder()

    pipeline_src = Pipeline(config, args.src)

    pipeline_tgt = Pipeline(config, args.tgt)

    pipelines = {args.src: pipeline_src, args.tgt: pipeline_tgt}

    to_join = []
    langs = [args.src, args.tgt]
    for lang in langs:
        p = Process(target=_process, args=(args.data, lang, pipelines,))
        p.start()
        to_join.append(p)

    for p in to_join:
        p.join()

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()

    main(args)
