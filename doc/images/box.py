from svg_schematic import Schematic, Box, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'box.svg'):
        b = Box(name='4 bit', value='Flash')
        Label(C=b.pi, name='pi', loc='w', kind='dot', color='blue')
        Label(C=b.i, name='i', loc='w', kind='dot', color='blue')
        Label(C=b.ni, name='ni', loc='w', kind='dot', color='blue')
        Label(C=b.po, name='po', loc='e', kind='dot', color='blue')
        Label(C=b.o, name='o', loc='e', kind='dot', color='blue')
        Label(C=b.no, name='no', loc='e', kind='dot', color='blue')

        b = Box(name='𝘻⁻¹', w=1, h=1, C=b.C, xoff=150)
        Label(C=b.i, name='i', loc='w', kind='dot', color='blue')
        Label(C=b.o, name='o', loc='e', kind='dot', color='blue')

        s = Box(name='4 bit', value='Flash', yoff=150)
        Label(C=s.N, name='N', loc='n', kind='dot', color='blue', w=2)
        Label(C=s.NE, name='NE', loc='ne', kind='dot', color='blue', w=2)
        Label(C=s.E, name='E', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.SE, name='SE', loc='se', kind='dot', color='blue', w=2)
        Label(C=s.S, name='S', loc='s', kind='dot', color='blue', w=2)
        Label(C=s.SW, name='SW', loc='sw', kind='dot', color='blue', w=2)
        Label(C=s.W, name='W', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.NW, name='NW', loc='nw', kind='dot', color='blue', w=2)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
