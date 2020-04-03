from svg_schematic import Schematic, Diode, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'diode.svg'):
        d = Diode(name='D1')
        Label(C=d.c, name='c', loc='e', kind='dot', color='blue')
        Label(C=d.a, name='a', loc='w', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
