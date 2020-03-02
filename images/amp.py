from svg_schematic import Schematic, Amp, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'amp.svg'):
        a = Amp(kind='se', name='As')
        Label(C=a.pi, name='pi', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.i,  name='i',  loc='w', kind='dot', color='blue', w=2)
        Label(C=a.ni, name='ni', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.po, name='po', loc='e', kind='dot', color='blue', w=2)
        Label(C=a.o,  name='o',  loc='e', kind='dot', color='blue', w=2)
        Label(C=a.no, name='no', loc='e', kind='dot', color='blue', w=2)

        a = Amp(kind='oa', name='Ao', C=a.C, xoff=200)
        Label(C=a.pi, name='pi', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.i,  name='i',  loc='w', kind='dot', color='blue', w=2)
        Label(C=a.ni, name='ni', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.po, name='po', loc='e', kind='dot', color='blue', w=2)
        Label(C=a.o,  name='o',  loc='e', kind='dot', color='blue', w=2)
        Label(C=a.no, name='no', loc='e', kind='dot', color='blue', w=2)

        a = Amp(kind='da', name='Ad', C=a.C, xoff=200)
        Label(C=a.pi, name='pi', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.i,  name='i',  loc='w', kind='dot', color='blue', w=2)
        Label(C=a.ni, name='ni', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.po, name='po', loc='e', kind='dot', color='blue', w=2)
        Label(C=a.o,  name='o',  loc='e', kind='dot', color='blue', w=2)
        Label(C=a.no, name='no', loc='e', kind='dot', color='blue', w=2)

        a = Amp(kind='comp', name='Ac', C=a.C, xoff=200)
        Label(C=a.pi, name='pi', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.i,  name='i',  loc='w', kind='dot', color='blue', w=2)
        Label(C=a.ni, name='ni', loc='w', kind='dot', color='blue', w=2)
        Label(C=a.po, name='po', loc='e', kind='dot', color='blue', w=2)
        Label(C=a.o,  name='o',  loc='e', kind='dot', color='blue', w=2)
        Label(C=a.no, name='no', loc='e', kind='dot', color='blue', w=2)
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
