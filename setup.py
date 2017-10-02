#
#   Copyright 2017 Intel Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#    
'''setup for databench
'''

from setuptools import setup, find_packages
from codecs import open
from os import path


long_description = '''XXX databench long desc
'''

try:
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
        version = f.read()[:-1]
except FileNotFoundError:
    version = '0.0.0'


download_url = 'https://github.com/Data-Bench/data-bench-python/archive/{}.tar.gz'

setup(name='databench',
      version=version,
      description='data model',
      long_description=long_description,
      url='https://github.com/Data-Bench/data-bench-python',
      download_url=download_url.format(version),
      author="Erik O'Shaughnessy",
      author_email="erik.oshaughnessy@intel.com",
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries'
                   ':: Python Modules',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6'],
      keywords='',
      packages=find_packages(exclude=['contrib']),
      test_suite='databench.tests',
      install_requires=[],
      extras_require={},
      package_data={},
      data_files=[],
      )
