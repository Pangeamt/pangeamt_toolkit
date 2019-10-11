#!/usr/bin/env python

from pangeamt_toolkit import Pangeanmt, Pipeline
import os
import json
import shutil
import argparse
import subprocess
import pandas as pd

class Engine:
    def __init__(self):
        with open('config.json', 'r') as file:
            self._config = json.loads(file.read())

        self._src_pipeline = Pipeline(self._config['pipeline_config'],\
            self._config['src_lang'], self._config['tgt_lang'])

        self._tgt_pipeline = Pipeline(self._config['pipeline_config_tgt'],\
            self._config['tgt_lang'])

    # Returns a trained model
    def train_from_table(self, table):
        p = Pangeanmt('.')

        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(table.shape[0]):

            # The attribute iat gets the value at [x, y]
            src = table.iat[i, 0]
            tgt = table.iat[i, 1]

            src_prep = self._src_pipeline.preprocess_str(src)
            tgt_prep = self._tgt_pipeline.preprocess_str(tgt)

            p.train(src_prep, tgt_prep)

        return p

    def translate_from_table(self, p, table, index):

        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(table.shape[0]):

            # The attribute iat gets the value at [x, y]
            seg = table.iat[i, 0]

            seg_prep = self._src_pipeline.preprocess_str(seg)

            translation = p.translate([seg])

            tgt = (' ').join(translation[0].tgt)
            tgt = self._src_pipeline.postprocess_str(tgt)

            table.iat[i, index] = tgt

def _get_parser():
    parser = argparse.ArgumentParser(description='Try different learning rates'\
        ' to find the best.')
    parser.add_argument('dir', help="Path to extended model.")
    parser.add_argument('xlsx_file', help='Xlsx file to work with.')
    return parser

def main(args):
    # Loads the file
    xl_file = pd.ExcelFile(args.xlsx_file)

    for sheet in xl_file.sheet_names:
        # Parses the content of the sheet to a pandas DataFrame.
        table = xl_file.parse(sheet)




if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()

    main(args)
