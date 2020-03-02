from svg_schematic import Schematic, Gate, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'gate.svg'):
        u = Gate(kind='inv', name='U')
        Label(C=u.i,  name='i',  loc='w', kind='dot', color='blue', w=2)
        Label(C=u.o,  name='o',  loc='e', kind='dot', color='blue', w=2)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
