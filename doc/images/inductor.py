from svg_schematic import Schematic, Inductor, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'inductor.svg'):
        l = Inductor(name='L1', value='1μH')
        Label(C=l.p, name='p', loc='e', kind='dot', color='blue')
        Label(C=l.n, name='n', loc='w', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
