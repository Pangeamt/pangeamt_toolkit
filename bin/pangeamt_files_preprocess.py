#!/usr/bin/env python

import os
import json
import argparse
from multiprocessing import Process
from pangeamt_toolkit.processors import Pipeline

# Parallel preprocess of train, dev and test files.

def _get_parser():
    parser = argparse.ArgumentParser(description='Preprocess file.')
    parser.add_argument('config', help="Path to config file")
    parser.add_argument('data', help="Path to data folder")
    parser.add_argument('src', help='Src lang')
    parser.add_argument('tgt', help='Tgt lang')
    return parser

def _load_pipelines(config, src_lang, tgt_lang):
    # Loads the main config for the source files and the secondary config
    # for the target files
    with open(config, 'r') as config_file:
        config = json.load(config_file)
        print('Loading pipelines..')
        pipelines = {
                src_lang:\
                    Pipeline(config['pipeline_config'], config['src_lang'],\
                        config['tgt_lang']),

                tgt_lang:\
                    Pipeline(config['pipeline_config_tgt'], config['tgt_lang'])
            }
        print('Pipelines loaded..')
    return pipelines

def _process(lang, pipelines):
    pipeline = pipelines[lang]
    files = ['train', 'dev', 'test']
    for file in files:
        path = f'{args.data}/{file}.{lang}'
        # Checks if the file exists
        if os.path.isfile(path):
            print(f"Started processing {path.split('/')[-1]}")
            pipeline.preprocess_file(path)
            print(f"Finished processing {path.split('/')[-1]}")
        else:
            pass

def main(args):
    langs = [args.src, args.tgt]
    to_join = []

    # loads the pipelines
    pipelines = _load_pipelines(args.config, args.src, args.tgt)

    for lang in langs:
        # Creates and spawns a process to parallelise the preprocess
        p = Process(target=_process, args=(lang, pipelines,))
        p.start()
        to_join.append(p)

    # Waits for all the processes to finish
    for p in to_join:
        p.join()

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.realpath(args.config)))

    main(args)
