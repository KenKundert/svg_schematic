from svg_schematic import Schematic, Resistor, Box, Label
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'tile1.svg',
        background = 'none',
    ):
        b = Box(w=2, h=2, background='lightgray')
        r = Resistor(C=b.C)
        Label(C=r.C, name='C', loc='s', kind='dot', color='blue')
        Label(C=r.N, name='N', loc='n', kind='dot', color='blue')
        Label(C=r.NE, name='NE', loc='ne', kind='dot', color='blue')
        Label(C=r.E, name='E', loc='e', kind='dot', color='blue')
        Label(C=r.SE, name='SE', loc='se', kind='dot', color='blue')
        Label(C=r.S, name='S', loc='s', kind='dot', color='blue')
        Label(C=r.SW, name='SW', loc='sw', kind='dot', color='blue')
        Label(C=r.W, name='W', loc='w', kind='dot', color='blue')
        Label(C=r.NW, name='NW', loc='nw', kind='dot', color='blue')

        b = Box(C=b.C, xoff=200, w=2, h=2, background='lightgray')
        r = Resistor(C=b.C, orient='v')
        Label(C=r.C, name='C', loc='e', kind='dot', color='blue')
        Label(C=r.N, name='N', loc='n', kind='dot', color='blue')
        Label(C=r.NE, name='NE', loc='ne', kind='dot', color='blue')
        Label(C=r.E, name='E', loc='e', kind='dot', color='blue')
        Label(C=r.SE, name='SE', loc='se', kind='dot', color='blue')
        Label(C=r.S, name='S', loc='s', kind='dot', color='blue')
        Label(C=r.SW, name='SW', loc='sw', kind='dot', color='blue')
        Label(C=r.W, name='W', loc='w', kind='dot', color='blue')
        Label(C=r.NW, name='NW', loc='nw', kind='dot', color='blue')

    with Schematic(filename='tile2.svg', background='none'):
        b = Box(background='lightgray', w=2, h=2)
        r = Resistor(C=b.C)
        Label(C=r.p, name='p', loc='n', kind='dot', color='blue')
        Label(C=r.n, name='n', loc='s', kind='dot', color='blue')

        b = Box(C=b.C, xoff=200, background='lightgray', w=2, h=2)
        r = Resistor(C=b.C, orient='v')
        Label(C=r.p, name='p', loc='n', kind='dot', color='blue')
        Label(C=r.n, name='n', loc='s', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

