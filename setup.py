try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

setup(
    name='schematic',
    version='0.0.0',
    description='svg schematics',
    author="Ken Kundert",
    license='GPLv3+',
    zip_safe=True,
    py_modules='schematic'.split(),
    install_requires='svgwrite'.split(),
)
