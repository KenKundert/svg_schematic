from svg_schematic import Schematic, Switch, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'switch.svg'):
        s = Switch(kind='spst', name='φ₁')
        Label(C=s.i, name='i', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.ot, name='ot', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.o, name='o', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.ob, name='ob', loc='e', kind='dot', color='blue', w=2)

        s = Switch(kind='spdt', name='φ₂', C=s.C, xoff=150)
        Label(C=s.i, name='i', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.ot, name='ot', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.o, name='o', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.ob, name='ob', loc='e', kind='dot', color='blue', w=2)
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
