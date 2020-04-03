from svg_schematic import Schematic, Box, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'box.svg'):
        b = Box(name='4 bit', value='Flash')
        Label(C=b.i, name='i', loc='w', kind='dot', color='blue')
        Label(C=b.o, name='o', loc='e', kind='dot', color='blue')

        b = Box(name='𝘻⁻¹', w=1, h=1, C=b.C, xoff=150)
        Label(C=b.i, name='i', loc='w', kind='dot', color='blue')
        Label(C=b.o, name='o', loc='e', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
