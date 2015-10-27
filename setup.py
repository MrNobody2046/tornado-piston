#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages


scripts = []
version = 0.2

setup(
    name="tornado-piston",
    version=version,
    packages=find_packages(),
    scripts=scripts,
    include_package_data=True,
    zip_safe=False,
    # include_package_data = True,    # include everything in source control
    # exclude_package_data = { '': ['README.txt'] },
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['tornado'],
    # packages=['src'],
    package_data={
        'doc': ['*.txt'], 'xml': ['*.xml', 'relax/*.rnc'],
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="Kenny Zhang",
    author_email="sphy@foxmail.com",
    description='The mini-framework based on Tornado, make easier to setup a data api',
    license="BSD",
    keywords="tornado api restfull",
    url="https://github.com/philoprove/tornado-piston",
    classifiers = [
        'Development Status :: Alpha',
        'Framework :: Tornado',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
    # could also include long_description, download_url, classifiers, etc.
)

