Examples
========

Charge Pump (charge-pump.py)
----------------------------

This example has a transparent background and so all wires terminate at 
terminals rather than passing underneath components. The labels are intended to 
be rendered by Latex.
It sets ``line_width`` to 2 give the schematic a heavier look.

.. include:: charge-pump.py
    :literal:

.. image:: Golden/charge-pump.svg
    :width: 80%
    :align: center


Inverter (inverter.py)
----------------------

This example has a transparent background and so all wires terminate at 
terminals rather than passing underneath components. The labels are intended to 
be rendered by Latex.
It sets ``line_width`` to 2 give the schematic a heavier look.

.. include:: inverter.py
    :literal:

.. image::  Golden/inverter.svg
    :width: 30%
    :align: center


Inverting Amplifier (inverting.py)
----------------------------------

This schematic uses ``line_width = 1`` give the schematic a lighter look.
It uses a 16 point serif font.

.. include:: inverting.py
    :literal:

.. image::  Golden/inverting.svg
    :width: 50%
    :align: center


Non-Inverting Amplifier (noninverting.py)
-----------------------------------------

This schematic uses ``line_width = 1`` give the schematic a lighter look.

.. include:: noninverting.py
    :literal:

.. image::  Golden/noninverting.svg
    :width: 40%
    :align: center


Oscillator (oscillator.py)
--------------------------

This example has a transparent background and so all wires terminate at 
terminals rather than passing underneath components. The labels are intended to 
be rendered by Latex.
This schematic uses ``line_width = 2`` give the schematic a heavier look.

.. include:: oscillator.py
    :literal:

.. image::  Golden/oscillator.svg
    :width: 40%
    :align: center


Passive Low Pass Filter (mfed.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example uses `QuantiPhy 
<https://quantiphy.readthedocs.io/en/latest/index.html>`_ to compute the values 
for the components in a low pass filter and then constructs the schematic using 
those values.  It sets ``line_width`` to 2 and employs dots at wire junctions to 
give the schematic a heavier look.

.. include:: mfed.py
    :literal:

.. image::  Golden/mfed.svg
    :width: 80%
    :align: center


Pipelined ADC (pipeline-adc.py)
-------------------------------

This block diagram has a white background and so could route wires under 
components rather than wiring to terminals, but it largely does not.
It uses ``line_width = 2`` give the diagram a heavier look.

.. include:: pipeline-adc.py
    :literal:

.. image::  Golden/pipeline-adc.svg
    :width: 100%
    :align: center


Receiver (receiver.py)
----------------------

This block diagram has a white background and so could route the wires 
underneath the components, but does not.
It uses ``line_width = 2`` give the diagram a heavier look.
It looks small because it is quite wide, and it is scaled to fit the page.

.. include:: receiver.py
    :literal:

.. image::  Golden/receiver.svg
    :width: 100%
    :align: center


Network Map (network-map.py)
----------------------------

This is another block diagram.

.. include:: network-map.py
    :literal:

.. image::  Golden/network-map.svg
    :width: 75%
    :align: center
