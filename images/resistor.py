from svg_schematic import Schematic, Resistor, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'resistor.svg'):
        r = Resistor(name='Rs', value='50Ω')
        Label(C=r.p, name='p', loc='e', kind='dot', color='blue')
        Label(C=r.n, name='n', loc='w', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
