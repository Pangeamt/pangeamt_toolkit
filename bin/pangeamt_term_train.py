#!/usr/bin/env python

from pangeamt_toolkit import Pangeanmt, Pipeline
import os
import json
import shutil
import argparse
import subprocess
import pandas as pd
from pangeamt_toolkit import Seg

class Engine:
    def __init__(self):
        with open('config.json', 'r') as file:
            self._config = json.loads(file.read())

        self._src_pipeline = Pipeline(self._config['pipeline_config'],
            self._config['src_lang'], self._config['tgt_lang'])

        self._tgt_pipeline = Pipeline(self._config['pipeline_config_tgt'],
            self._config['tgt_lang'])

    # Returns a trained model
    def train(self, p, src_text, tgt_text):
        res = {'src_prep': [], 'tgt_prep': []}
        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(len(src_text)):
            if ((i + 1) % 10 == 0):
                print(f'Trained with {i+1} segments.')
            # The attribute iat gets the value at [x, y]
            src = src_text[i]
            tgt = tgt_text[i]

            src_prep = self._src_pipeline.preprocess_str(src)
            tgt_prep = self._tgt_pipeline.preprocess_str(tgt)

            p.train(src_prep, tgt_prep)

        return p

    def translate(self, p, src_text, tgt_text):
        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        translations_post=[]
        for i in range(0,len(src_text),30):
##        for i in range(len(src_text)):
##            seg = Seg(src_text[i])
            if ((i + 1) % 30 == 0):
                print(f'Translated {i+1} segments.')
            if i+30 <= len(src_text):
               segs = src_text[i:i+30]
            else:
               segs = src_text[i:] 
            
            segs_prep = []
            for seg in segs:
                segs_prep.append(self._src_pipeline.preprocess_str(seg))
##            self._src_pipeline.preprocess(seg)

            translations = p.translate(segs_prep)
##            translation = p.translate(seg_prep)
            for trans in translations:
                tgt = (' ').join(trans.tgt)
                tgt = self._src_pipeline.postprocess_str(tgt)
                translations_post.append(tgt)            
##            translation_post = (' ').join(translation[0].tgt)
        return translations_post
##        return translation_post

def _get_parser():
    parser = argparse.ArgumentParser(description='Vocab learning')
    parser.add_argument('dir', help="Path to extended model.")
    parser.add_argument('src_file', help='Source file to work with.')
    parser.add_argument('tgt_file', help='Target file to work with.')
    parser.add_argument('i', help='Number of times the model learns.')
    return parser

def main(args):
    # Loads the file
    with open(args.src_file, "r") as src_file: 
       src_text = []
       for line in src_file:
          src_text.append(line.strip())    
    with open(args.tgt_file, "r") as tgt_file: 
       tgt_text = []
       for line in tgt_file:
          tgt_text.append(line.strip())    
    print('Files correctly loaded.')

    os.chdir(args.dir)

    e = Engine()
    p = Pangeanmt('.')

    print('Correctly loaded model.')

    print('Translating without training.')
    first_trans = e.translate(p, src_text, tgt_text)
    
    with open(args.dir+"/transformer/firsttrans", "w") as firsttrans_file:
        for line in first_trans:
            firsttrans_file.write(line+"\n")

    for step in range(1, int(args.i)+1):
        print(f'Training... step: {step}')
        p = e.train(p, src_text, tgt_text)
        p.save_model(args.dir+"/model_step"+str(step))

        print(f'Translating... step: {step}')
        result = e.translate(p, src_text, tgt_text)
        with open(args.dir+"/transformer/trans"+str(step), "w") as trans_file:
            for line in result:
                trans_file.write(line+"\n")

    print('Finished.')

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()

    main(args)
