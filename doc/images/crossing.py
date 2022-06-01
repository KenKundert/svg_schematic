from svg_schematic import Schematic, Crossing, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'crossing.svg'):
        c = Crossing()
        Label(C=c.pi, name='pi', loc='w', kind='dot', color='blue')
        Label(C=c.ni, name='ni', loc='w', kind='dot', color='blue')
        Label(C=c.po, name='po', loc='e', kind='dot', color='blue')
        Label(C=c.no, name='no', loc='e', kind='dot', color='blue')

        c = Crossing(C=c.C, w=2, h=2, xoff=150)
        Label(C=c.pi, name='pi', loc='w', kind='dot', color='blue')
        Label(C=c.ni, name='ni', loc='w', kind='dot', color='blue')
        Label(C=c.po, name='po', loc='e', kind='dot', color='blue')
        Label(C=c.no, name='no', loc='e', kind='dot', color='blue')

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
