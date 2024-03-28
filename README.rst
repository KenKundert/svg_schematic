SVG Schematic
=============

.. image:: https://pepy.tech/badge/svg_schematic/month
    :target: https://pepy.tech/project/svg_schematic

.. image:: https://img.shields.io/readthedocs/svg_schematic.svg
   :target: https://svg_schematic.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/v/svg_schematic.svg
    :target: https://pypi.python.org/pypi/svg_schematic

.. image:: https://img.shields.io/pypi/pyversions/svg_schematic.svg
    :target: https://pypi.python.org/pypi/svg_schematic/


:Author: Ken Kundert
:Version: 1.2.0
:Released: 2022-06-03


This package allows you to create simple SVG schematics and block diagrams 
without a mouse.  Instead, you build the schematic using Python to instantiate 
and place the symbols and wires.


Simple Example
--------------

Here is a simple example that demonstrates the package. It generates the 
schematic of a shunt RLC circuit::

    from svg_schematic import Schematic, Resistor, Capacitor, Inductor, Wire
    from inform import Error, error, os_error

    try:
        with Schematic(filename='rlc.svg'):
            r = Resistor(name='R', orient='v')
            c = Capacitor(W=r.E, name='C', orient='v')
            l = Inductor(W=c.E, name='L', orient='v|')
            Wire([r.p, l.p])
            Wire([r.n, l.n])
    except Error as e:
        e.report()
    except OSError as e:
        error(os_error(e))

When run, it produces the following schematic:

.. image:: doc/images/Golden/rlc.svg
    :width: 35 %
    :align: center


Installation
------------

Requires Python3. Works best with Python3.6 or newer.

You can download and install the latest
stable version of the code from `PyPI 
<https://pypi.org/project/svg-schematic/>`_ using::

    pip3 install --user svg_schematic

You can find the latest development version of the source code on
`Github <https://github.com/KenKundert/svg_schematic>`_.


Documentation
-------------

You can find documentation at `ReadTheDocs 
<https://svg-schematic.readthedocs.io>`_.


Issues
------

Please ask questions or report problems on
`Github Issues <https://github.com/KenKundert/svg_schematic/issues>`_.


Contributions
-------------

Contributions in the form of pull requests are welcome.

I tend to create symbols as I need them.  If you create missing symbols, please
consider contributing them back to the project.
