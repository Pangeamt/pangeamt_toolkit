from distutils.core import setup
setup(
  name = 'pangeamt_toolkit',
  packages = ['pangeamt_toolkit'],
  version = '1.6',
  license='MIT',
  description = 'PANGEAMT-TOOLKIT',
  author = 'PANGEAMT',
  author_email = 'a.cerda@pangeanic.es',
  url = 'https://github.com/Pangeamt/pangeamt_toolkit',
  download_url = 'https://github.com/Pangeamt/pangeamt_toolkit/archive/1.6.tar.gz',
  install_requires=[
            'Click',
            'joblib',
            'PyYAML',
            'sacremoses',
            'six',
            'tqdm',
            'subword-nmt',
            'mecab-python3',
            'jieba'
      ]
)
