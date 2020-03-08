"""
Draw a 5th Order Low Pass Passive Filer with Maximally Flat Envelope Delay

Use the following parameters:
    Fo = 1MHz   -- 3dB corner frequency
    Rref = 50Ω  -- termination impedance

Design equations:
    Omega0 = 2*π*Fo
    Lscale = Rref/Omega0
    Cscale = 1/(Rref*Omega0)

    Rs = 1.0000 * Rref   "Ω"
    C1 = 0.2715 * Cscale "F"
    L2 = 0.6541 * Lscale "H"
    C3 = 0.8892 * Cscale "F"
    L4 = 1.1034 * Lscale "H"
    C5 = 2.2873 * Cscale "F"
"""

from svg_schematic import (
    Schematic, Capacitor, Dot, Ground, Inductor, Label, Resistor, Pin, Source, Wire
)
from inform import Error, error, os_error
from quantiphy import Quantity
from math import pi

Quantity.set_prefs(map_sf=Quantity.map_sf_to_greek, prec=2)
globals().update(
    Quantity.extract(__doc__, predefined={'π': pi})
)

try:
    with Schematic(filename = 'mfed.svg', line_width=2, background = 'none'):

        vin = Source(name='Vin', value='1 V', kind='sine')
        Ground(C=vin.n)
        rs = Resistor(name='Rs', value=Rref, n=vin.p, xoff=25)
        Wire([vin.p, rs.n])
        c1 = Capacitor(name='C1', value=C1, p=rs.p, xoff=25)
        Ground(C=c1.n)
        l2 = Inductor(name='L2', value=L2, n=c1.p, xoff=25)
        Wire([rs.p, l2.n])
        c3 = Capacitor(name='C3', value=C3, p=l2.p, xoff=25)
        Ground(C=c3.n)
        l4 = Inductor(name='L4', value=L4, n=c3.p, xoff=25)
        Wire([l2.p, l4.n])
        c5 = Capacitor(name='C5', value=C5, p=l4.p, xoff=25)
        Ground(C=c5.n)
        rl = Resistor(name='Rl', value=Rref, p=c5.p, xoff=100, orient='v')
        Ground(C=rl.n)
        out = Pin(name='out', C=rl.p, xoff=50, w=2)
        Wire([l4.p, out.t])
        Label(S=c3.N, yoff=-50, name=f'{Fo} LPF', loc='s')
        Dot(C=c1.p)
        Dot(C=c3.p)
        Dot(C=c5.p)
        Dot(C=rl.p)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

