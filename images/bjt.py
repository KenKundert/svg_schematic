from svg_schematic import Schematic, BJT, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'bjt.svg'):
        q = BJT(kind='npn', name='Qn')
        Label(C=q.c, name='c', loc='n', kind='dot', color='blue')
        Label(C=q.b, name='b', loc='w', kind='dot', color='blue')
        Label(C=q.e, name='e', loc='s', kind='dot', color='blue')

        q = BJT(kind='pnp', name='Qp', C=q.C, xoff=150)
        Label(C=q.e, name='e', loc='n', kind='dot', color='blue')
        Label(C=q.b, name='b', loc='w', kind='dot', color='blue')
        Label(C=q.c, name='c', loc='s', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
