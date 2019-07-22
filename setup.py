from distutils.core import setup
setup(
  name = 'pangeamt_toolkit',
  packages = ['pangeamt_toolkit'],
  version = '0.5',
  license='MIT',
  description = 'PANGEAMT-TOOLKIT',
  author = 'PANGEAMT',
  author_email = 'a.cerda@pangeanic.es',
  url = 'https://github.com/Pangeamt/pangeamt_toolkit',
  download_url = 'https://github.com/Pangeamt/pangeamt_toolkit/archive/0.5.tar.gz',
  install_requires=[            # I get to this in a second
            'Click',
            'joblib',
            'PyYAML',
            'sacremoses',
            'six',
            'tqdm'
      ]
)
