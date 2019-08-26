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
def _config_builder(lang):
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

    langs = [args.src, args.tgt]

    src_config = _config_builder(args.src)
    pipeline_src = Pipeline(src_config)

    tgt_config = _config_builder(args.tgt)
    pipeline_tgt = Pipeline(tgt_config)

    pipelines = {args.src: pipeline_src, args.tgt: pipeline_tgt}

    to_join = []
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
