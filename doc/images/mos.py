from svg_schematic import Schematic, MOS, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'mos.svg'):
        m = MOS(kind='n', name='Mn')
        Label(C=m.d, name='d', loc='n', kind='dot', color='blue')
        Label(C=m.g, name='g', loc='w', kind='dot', color='blue')
        Label(C=m.s, name='s', loc='s', kind='dot', color='blue')

        m = MOS(kind='p', name='Mp', C=m.C, xoff=150)
        Label(C=m.s, name='s', loc='n', kind='dot', color='blue')
        Label(C=m.g, name='g', loc='w', kind='dot', color='blue')
        Label(C=m.d, name='d', loc='s', kind='dot', color='blue')

        m = MOS(kind='', name='M', C=m.C, xoff=150)
        Label(C=m.d, name='d', loc='n', kind='dot', color='blue')
        Label(C=m.g, name='g', loc='w', kind='dot', color='blue')
        Label(C=m.s, name='s', loc='s', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
