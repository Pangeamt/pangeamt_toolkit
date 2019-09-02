from distutils.core import setup
setup(
    name = 'pangeamt_toolkit',
    packages = ['pangeamt_toolkit', 'pangeamt_toolkit.onmt',
        'pangeamt_toolkit.onmt.encoders', 'pangeamt_toolkit.onmt.decoders',
        'pangeamt_toolkit.onmt.inputters', 'pangeamt_toolkit.onmt.models',
        'pangeamt_toolkit.onmt.utils', 'pangeamt_toolkit.pangeanmt',
        'pangeamt_toolkit.pangeanmt.extended_model',
        'pangeamt_toolkit.pangeanmt.request_handler', 'pangeamt_toolkit.seg',
        'pangeamt_toolkit.processors', 'pangeamt_toolkit.onmt.modules',
        'pangeamt_toolkit.onmt.translate'],
    scripts = ['bin/pangeamt_file_postprocess.py', 'bin/pangeamt_train.py',
    'bin/pangeamt_file_preprocess.py', 'bin/pangeamt_preprocess.py',
    'bin/pangeamt_translate.py', 'bin/pangeamt_multi_bleu.perl',
    'bin/pangeamt_build_server.py', 'bin/pangeamt_files_preprocess.py',
    'bin/pangeamt_norm_tok_preprocess.py', 'bin/pangeamt_truecase_preprocess.py'],
    version = '2.27',
    license='MIT',
    description = 'PANGEAMT-TOOLKIT',
    author = 'PANGEAMT',
    author_email = 'a.cerda@pangeanic.es',
    url = 'https://github.com/Pangeamt/pangeamt_toolkit',
    download_url = 'https://github.com/Pangeamt/pangeamt_toolkit/archive/2.27.tar.gz',
    install_requires=[
        'aiohttp==3.5.4',
        'async-timeout==3.0.1',
        'attrs==19.1.0',
        'certifi==2019.6.16',
        'chardet==3.0.4',
        'Click==7.0',
        'ConfigArgParse==0.14.0',
        'future==0.17.1',
        'idna==2.8',
        'idna-ssl==1.1.0',
        'jieba==0.39',
        'joblib==0.13.2',
        'mecab-python3==0.996.2',
        'multidict==4.5.2',
        'neologdn==0.4',
        'numpy==1.17.0',
        'PyYAML==5.1.1',
        'requests==2.22.0',
        'sacremoses==0.0.33', # 0.0.22
        'six==1.12.0',
        'subword-nmt==0.3.6',
        'torch==1.1.0',
        'torchtext==0.4.0',
        'tqdm==4.32.2',
        'typing-extensions==3.7.4',
        'urllib3==1.25.3',
        'uvloop==0.12.2',
        'yarl==1.3.0'
    ]
)
