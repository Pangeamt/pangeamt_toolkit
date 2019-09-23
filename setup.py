from setuptools import setup
import sys
# This is a change
try:
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name = 'pangeamt_toolkit',
    scripts = ['bin/pangeamt_file_postprocess.py', 'bin/pangeamt_train.py',
        'bin/pangeamt_file_preprocess.py', 'bin/pangeamt_preprocess.py',
        'bin/pangeamt_translate.py', 'bin/pangeamt_multi_bleu.perl',
        'bin/pangeamt_build_server.py', 'bin/pangeamt_files_preprocess.py',
        'bin/pangeamt_norm_tok_preprocess.py', 'bin/pangeamt_find_best_learning.py',
        'bin/pangeamt_truecase_preprocess.py'],
    versioning='distance',
    setup_requires='setupmeta'
)
