# -*- coding: utf-8 -*-
"""
This module contains the tool of plonecommunity.mobi
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('plonecommunity', 'app', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='plonecommunity.app',
      version=version,
      description="plonecommunity.mobi site source code",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='mFabrik Research Oy',
      author_email='mikko.ohtamaa@twinapex.com',
      url='http://mfabrik.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonecommunity', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'five.grok',
                        'gomobiletheme.basic'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'plonecommunity.app.tests.test_docs.test_suite',
      paster_plugins = ["ZopeSkel"],
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone        
        """
      )
