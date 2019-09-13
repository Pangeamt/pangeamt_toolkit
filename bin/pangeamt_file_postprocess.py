#!/usr/bin/env python
import os
import json
import argparse
from pangeamt_toolkit.processors import Pipeline

def _get_parser():
    # Postprocess a file using the main pipeline config
    parser = argparse.ArgumentParser(description='Postprocess file.')
    parser.add_argument('config', help='Path to config file.')
    parser.add_argument('src_file', help='Path to src file.')
    parser.add_argument('tgt_file', help='Path to tgt file.')
    return parser

def main(args):
    with open(args.config, 'r') as c_file:
        config = json.load(c_file)
        processors = get_processors(config)

    pipeline = Pipeline(processors, config['src_lang'], config['tgt_lang'])

    pipeline.postprocess_file(args.src_file, args.tgt_file)

def get_processors(config):
    processors = config['pipeline_config']
    if config['tgt_lang'] in ['ja', 'zh', 'tw']:
        for i, processor in enumerate(processors):
            if processor['name'] == 'tokenize':
                processors.pop(i)
                return processors
    return processors

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.realpath(args.config)))

    main(args)
