try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
from textwrap import dedent

with open('README.rst') as f:
    readme = f.read()

setup(
    name='svg_schematic',
    version='0.2.0',
    description='svg schematics',
    long_description=readme,
    url='https://github.com/kenkundert/svg_schematic',
    download_url='https://github.com/kenkundert/svg_schematic/tarball/master',
    author="Ken Kundert",
    author_email='quantiphy@nurdletech.com',
    license='GPLv3+',
    zip_safe=True,
    py_modules='svg_schematic'.split(),
    install_requires='svgwrite'.split(),
    keywords='svg schematic latex'.split(),
    classifiers=dedent('''
        Development Status :: 5 - Production/Stable
        Intended Audience :: Science/Research
        License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
        Natural Language :: English
        Operating System :: POSIX :: Linux
        Programming Language :: Python :: 3.6
        Topic :: Utilities
        Topic :: Scientific/Engineering
    ''').strip().split('\n'),
)
