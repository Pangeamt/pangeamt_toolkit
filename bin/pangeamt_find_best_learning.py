#!/usr/bin/env python

from pangeamt_toolkit import Pangeanmt, Pipeline
import os
import json
import shutil
import argparse
import subprocess

class Engine:
    def __init__(self, in_file, ref_file):
        with open('config.json', 'r') as file:
            self._config = json.loads(file.read())

        self._src_pipeline = Pipeline(self._config['pipeline_config'],\
            self._config['src_lang'], self._config['tgt_lang'])

        self._tgt_pipeline = Pipeline(self._config['pipeline_config_tgt'],\
            self._config['tgt_lang'])

        self._in_file = os.path.join('data', in_file)
        self._ref_file = os.path.join('data', ref_file)


    # Returns trained model
    def train(self):
        p = Pangeanmt('.')

        with open(self._in_file, 'r') as src_file:
            with open(self._ref_file, 'r') as tgt_file:
                for seg in src_file:
                    #try:
                    src = self._src_pipeline.preprocess_str(seg)

                    tgt_seg = tgt_file.readline()
                    tgt = self._tgt_pipeline.preprocess_str(tgt_seg)

                    p.train(src, tgt)
                    #except:
                    #    print('Something went wrong.')
        return p

    def translate_file(self, p, output_file):
        with open(self._in_file, 'r') as in_file:
            with open(output_file, 'w+') as out_file:
                for seg in in_file:
                    seg = self._src_pipeline.preprocess_str(seg)

                    translation = p.translate([seg])

                    tgt = (' ').join(translation[0].tgt)
                    tgt = self._src_pipeline.postprocess_str(tgt)

                    out_file.write(f'{tgt}\n')

    def gen_config(self, alpha):
        lr = self._config['opts']['learning_rate']

        os.rename('config.json', f'{lr}_config.json')

        self._config['opts']['learning_rate'] = alpha

        with open('config.json', 'w+') as config_file:
            config_file.write(json.dumps(self._config))


def _get_parser():
    parser = argparse.ArgumentParser(description='Try different learning rates'\
        ' to find the best.')

    parser.add_argument('dir', help="Path to extended model.")
    parser.add_argument('src_file', help='Which file to translate.')
    parser.add_argument('ref_file', help='Reference file when training.')
    parser.add_argument('learning_rate', help='Initial learning rate.')
    parser.add_argument('increment', help='Amount to increment each iteration.')
    parser.add_argument('max_learning_rate', help='Last learning rate to eval.')
    return parser

def main(args):
    os.chdir(args.dir)
    e = Engine(args.src_file, args.ref_file)
    p = Pangeanmt('.')
    best_learning_rate = (0, 0)
    print('Translating with the base model...')
    e.translate_file(p, os.path.join('data','base_translation.txt'))
    with open(os.path.join('data','base_translation.txt'), 'r') as file:
        out = subprocess.check_output(params, stdin=file).decode('utf-8')
        print(out)
    shutil.copy('config.json', 'backup_config.json')
    alpha = args.learning_rate
    while alpha <= args.max_learning_rate:
        print(f'Training with learning rate = {alpha}')
        e.gen_config(alpha)
        p = e.train()
        print('Translating file.')
        output_file = os.path.join('data', f'{alpha}_{args.src_file}.txt')
        e.translate_file(p, output_file)
        _ref_file = os.path.join('data', args.ref_file)
        params = ['pangeamt_multi_bleu.perl', _ref_file]
        with open(output_file, 'r') as file:
            out = subprocess.check_output(params, stdin=file).decode('utf-8')
            print(out)
            bleu = float(out.split(' ')[2])
            if bleu > best_learning_rate[0]:
                best_learning_rate = (bleu, alpha)

    print(f'Best learning rate: {best_learning_rate[0]},'\
        f'with BLEU: {best_learning_rate[1]}')

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()

    main(args)
