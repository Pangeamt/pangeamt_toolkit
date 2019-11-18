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

        self._src_pipeline = Pipeline(self._config['pipeline_config'],
            self._config['src_lang'], self._config['tgt_lang'])

        self._tgt_pipeline = Pipeline(self._config['pipeline_config_tgt'],
            self._config['tgt_lang'])

    # Returns a trained model
    def train_from_table(self, p, table):
        res = {'src_prep': [], 'tgt_prep': []}
        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(table.shape[0]):
            if ((i + 1) % 10 == 0):
                print(f'Trained with {i+1} segments.')
            # The attribute iat gets the value at [x, y]
            src = table.iat[i, 0]
            tgt = table.iat[i, 1]

            src_prep = self._src_pipeline.preprocess_str(src)
            tgt_prep = self._tgt_pipeline.preprocess_str(tgt)

            res['src_prep'].append(src_prep)
            res['tgt_prep'].append(tgt_prep)

            p.train(src_prep, tgt_prep)

        return p, res

    def no_train_translate_from_table(self, p, table):
        res = {'original': []}
        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(table.shape[0]):
            if ((i + 1) % 10 == 0):
                print(f'Translated {i+1} segments.')
                # The attribute iat gets the value at [x, y]
            seg = table.iat[i, 0]

            seg_prep = self._src_pipeline.preprocess_str(seg)

            translation = p.translate([seg_prep])

            tgt = (' ').join(translation[0].tgt)
            tgt = self._src_pipeline.postprocess_str(tgt)

            res['original'].append(tgt)
        return res

    def translate_from_table(self, p, table, j):
        res = {f'tgts_{j}': []}
        # Shape returns the dimensions of the DataFrame, so shape[0] is the
        # number of rows.
        for i in range(table.shape[0]):
            if ((i + 1) % 10 == 0):
                print(f'Translated {i+1} segments.')
            # The attribute iat gets the value at [x, y]
            seg = table.iat[i, 0]

            seg_prep = self._src_pipeline.preprocess_str(seg)

            translation = p.translate([seg_prep])

            tgt = (' ').join(translation[0].tgt)
            tgt = self._src_pipeline.postprocess_str(tgt)

            res[f'tgts_{j}'].append(tgt)
        return res

def _get_parser():
    parser = argparse.ArgumentParser(description='Vocab learning')
    parser.add_argument('dir', help="Path to extended model.")
    parser.add_argument('xlsx_file', help='Xlsx file to work with.')
    parser.add_argument('i', help='Number of times the model learns.')
    return parser

def main(args):
    # Loads the file
    xl_file = pd.ExcelFile(args.xlsx_file)
    for sheet in xl_file.sheet_names:
        # Parses the content of the sheet to a pandas DataFrame.
        table = xl_file.parse(sheet)

    xl_writer = pd.ExcelWriter(args.xlsx_file, engine='xlsxwriter')
    print('Correctly loaded the table.')

    os.chdir(args.dir)

    e = Engine()
    p = Pangeanmt('.')

    print('Correctly loaded model.')

    print('Translating without training.')
    first_trans = pd.DataFrame(e.no_train_translate_from_table(p, table))

    final_table = [first_trans]

    for step in range(1, int(args.i)+1):
        print(f'Training... step: {step}')
        p, preps = e.train_from_table(p, table)

        print(f'Translating... step: {step}')
        result = pd.DataFrame(e.translate_from_table(p, table, step))
        final_table.append(result)

    final_table.insert(0, pd.DataFrame(table))
    final_table.insert(1, pd.DataFrame(preps))

    df = pd.concat(final_table, axis=1, sort=False)

    df.to_excel(xl_writer, sheet_name='Sheet1', index=False)

    xl_writer.save()
    print('Finished.')

if __name__ == "__main__":
    parser = _get_parser()
    args = parser.parse_args()

    main(args)
