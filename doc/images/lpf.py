from svg_schematic import (
    Schematic, Capacitor, Ground, Inductor, Resistor, Pin, Source, Wire
)
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'lpf.svg',
        background = 'none',
    ):
        vin = Source(name='Vin', value='1 V', kind='sine')
        Ground(C=vin.n)
        rs = Resistor(name='Rs', value='50 Ω', n=vin.p, xoff=25)
        Wire([vin.p, rs.n])
        c1 = Capacitor(name='C1', value='864 pF', p=rs.p, xoff=25)
        Ground(C=c1.n)
        l2 = Inductor(name='L2', value='5.12 μH', n=c1.p, xoff=25)
        Wire([rs.p, l2.n])
        c3 = Capacitor(name='C3', value='2.83 nF', p=l2.p, xoff=25)
        Ground(C=c3.n)
        l4 = Inductor(name='L4', value='8.78 μH', n=c3.p, xoff=25)
        Wire([l2.p, l4.n])
        c5 = Capacitor(name='C5', value='7.28 nF', p=l4.p, xoff=25)
        Ground(C=c5.n)
        rl = Resistor(name='Rl', value='50 Ω', p=c5.p, xoff=100, orient='v')
        Ground(C=rl.n)
        out = Pin(name='out', C=rl.p, xoff=50, w=2)
        Wire([l4.p, out.t])
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

