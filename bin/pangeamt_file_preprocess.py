#!/usr/bin/env python
import json
import argparse
from pangeamt_toolkit.processors import Pipeline

# Preprocess a single file. The output file's name is composed with the
# name mods from the processors. Loads main config.

def _get_parser():
    parser = argparse.ArgumentParser(description='Preprocess file.')
    parser.add_argument('config', help='Path to config file.')
    parser.add_argument('src_file', help='Path to src file.')
    return parser

def main(args):
    # Loads the main pipeline config from the config file
    with open(args.config, 'r') as c_file:
        config = json.load(c_file)
        processors = config['pipeline_config']

    pipeline = Pipeline(processors, config['src_lang'], config['tgt_lang'])

    pipeline.preprocess_file(args.src_file)

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.realpath(args.config)))

    main(args)
