try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

setup(
    name='svg_schematic',
    version='0.1.0',
    description='svg schematics',
    author="Ken Kundert",
    license='GPLv3+',
    zip_safe=True,
    py_modules='svg_schematic'.split(),
    install_requires='svgwrite'.split(),
)
