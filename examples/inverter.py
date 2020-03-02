#!/usr/bin/env python3

from svg_schematic import Schematic, MOS, Ground, Gate, Label, Pin, Wire, midpoint
from inform import Error, error, os_error

try:
    with Schematic(filename = 'inverter.svg', line_width=2, background='none'):

        # transistor version
        mp = MOS(kind='p')
        mn = MOS(N=mp.S, kind='n')
        vin = Pin(C=midpoint(mp.g, mn.g), xoff=-50, kind='in', name=r'$V_{\rm in}$', w=2)
        vout = Pin(C=midpoint(mp.d, mn.d), xoff=50, kind='out', name=r'$V_{\rm out}$', w=2)
        Label(C=mp.s, loc='n', name=r'$V_{\rm dd}$')
        Ground(C=mn.s)
        Wire([vin.t, mp.g], kind='-|')
        Wire([vin.t, mn.g], kind='-|')
        Wire([vout.t, mp.d], kind='-|')
        Wire([vout.t, mn.d], kind='-|')

        # gate version
        inv = Gate(N=mn.S, yoff=25, kind='inv')
        vin = Pin(t=inv.i, xoff=-25, kind='in', name=r'$V_{\rm in}$', w=2)
        vout = Pin(t=inv.o, xoff=25, kind='out', name=r'$V_{\rm out}$', w=2)
        Wire([inv.o, vout.t])
        Wire([inv.i, vin.t])

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
