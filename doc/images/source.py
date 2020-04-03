from svg_schematic import Schematic, Source, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'source.svg'):
        s = Source(kind='empty', name='Ve')
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='vdc', name='Vd', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='idc', name='Id', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='sine', name='Vs', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='sum', name='S', yoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='mult', name='M', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='cv', name='Vc', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='ci', name='Ic', C=s.C, xoff=150)
        Label(C=s.p, name='p', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.n, name='n', loc='w', kind='dot', color='blue', w=2)

        s = Source(kind='sum', name='S', yoff=300)
        Label(C=s.N, name='N', loc='n', kind='dot', color='blue', w=2)
        Label(C=s.NE, name='NE', loc='ne', kind='dot', color='blue', w=2)
        Label(C=s.E, name='E', loc='e', kind='dot', color='blue', w=2)
        Label(C=s.SE, name='SE', loc='se', kind='dot', color='blue', w=2)
        Label(C=s.S, name='S', loc='s', kind='dot', color='blue', w=2)
        Label(C=s.SW, name='SW', loc='sw', kind='dot', color='blue', w=2)
        Label(C=s.W, name='W', loc='w', kind='dot', color='blue', w=2)
        Label(C=s.NW, name='NW', loc='nw', kind='dot', color='blue', w=2)


except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
