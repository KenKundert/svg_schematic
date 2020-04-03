from svg_schematic import Schematic, Capacitor, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'capacitor.svg'):
        c = Capacitor(name='C1', value='1.2pF')
        Label(C=c.p, name='p', loc='n', kind='dot', color='blue')
        Label(C=c.n, name='n', loc='s', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
