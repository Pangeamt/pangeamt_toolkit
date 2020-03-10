#!/usr/bin/env python

import os
import sys
from glob import glob
import xml.dom.minidom as xml

from pangeamt_nlp.multilingual_resource.tmx.tmx import Tmx
from pangeamt_nlp.multilingual_resource.tmx.tmx_reader_bilingual import (
    TmxReaderBilingualText
)


path = sys.argv[1] if len(sys.argv) == 2 else '.'

os.chdir(path)

source_directory = glob('tmx/')

if len(source_directory) == 0:
    print('tmx directory does not exist')
    exit()

try:
    os.mkdir('bilingual')
except Exception:
    print("Directory bilingual already exists")
    pass

os.chdir(source_directory[0])

files = glob('*.tmx')

for file in files:

    tmx = Tmx(file)

    doc = xml.parse(file)

    header = doc.getElementsByTagName("header")[0]
    src_lang = header.getAttribute("srclang")

    tuv = doc.getElementsByTagName("tuv")[1]
    tgt_lang = tuv.getAttribute('xml:lang')

    src_ext = src_lang.split('-')[0]
    tgt_ext = tgt_lang.split('-')[0]

    reader = TmxReaderBilingualText(src_lang=src_lang, tgt_lang=tgt_lang)
    read = tmx.read(reader)
    file_name = file[:-4]
    with open(f'../bilingual/{file_name}.{src_ext}', 'w', encoding='utf-8') as src_file, \
            open(f'../bilingual/{file_name}.{tgt_ext}', 'w', encoding='utf-8') as tgt_file:

        while True:
            try:
                src, tgt = next(read)
                src = src.replace('\n', ' ')
                tgt = tgt.replace('\n', ' ')
                src_file.write(src.strip() + '\n')
                tgt_file.write(tgt.strip() + '\n')
            except StopIteration as e:
                print(e)
                break

print("Process ended")
