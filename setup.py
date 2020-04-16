try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
from textwrap import dedent

with open('README.rst') as f:
    readme = f.read()

setup(
    name = 'svg_schematic',
    version = '1.0.0',
    description = 'svg schematics',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    url = 'https://svg_schematic.readthedocs.io',
    download_url = 'https://github.com/kenkundert/svg_schematic/tarball/master',
    author = "Ken Kundert",
    author_email = 'quantiphy@nurdletech.com',
    license = 'GPLv3+',
    zip_safe = False,
    py_modules = 'svg_schematic'.split(),
    install_requires = 'svgwrite inform'.split(),
    python_requires = '>=3.6',
    keywords = 'svg schematic latex'.split(),
    classifiers = dedent('''
        Development Status :: 5 - Production/Stable
        Intended Audience :: Science/Research
        License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
        Natural Language :: English
        Operating System :: POSIX :: Linux
        Programming Language :: Python :: 3.6
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: 3.8
        Topic :: Utilities
        Topic :: Scientific/Engineering
    ''').strip().split('\n'),
)
