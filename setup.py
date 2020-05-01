from distutils.core import setup
setup(
  name = 'mxklabs',
  packages = ['mxklabs', 'mxklabs.data', 'mxklabs.dimacs'],
  version = '0.0.6',
  description = 'A selection python code written for mxklabs projects that may be useful elsewhere.',
  author = 'Mark Kattenbelt',
  author_email = 'mark.kattenbelt@gmail.com',
  url = 'https://github.com/mxklabs/mxklabs-python',
  download_url = 'https://github.com/mxklabs/mxklabs-python/tarball/0.0.6',
  keywords = ['mxklabs', 'mxklabs.data', 'mxklabs.sat', 'DIMACS', 'SAT',
              'satisfiability', 'CNF', 'circular', 'buffer', 'persistent'],
  classifiers = [],
  include_package_data=True,
  install_requires=[
    'asn1tools'
  ]
)
