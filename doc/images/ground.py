from svg_schematic import Schematic, Ground, Label
from inform import Error, error, os_error

try:
    with Schematic(filename = 'ground.svg'):
        g = Ground()
        Label(C=g.t, name='t', loc='n', kind='dot', color='blue')
        # Label(C=g.N, name='N', loc='n', kind='dot', color='blue')
        # Label(C=g.NE, name='NE', loc='ne', kind='dot', color='blue')
        # Label(C=g.E, name='E', loc='e', kind='dot', color='blue')
        # Label(C=g.SE, name='SE', loc='se', kind='dot', color='blue')
        # Label(C=g.S, name='S', loc='s', kind='dot', color='blue')
        # Label(C=g.SW, name='SW', loc='sw', kind='dot', color='blue')
        # Label(C=g.W, name='W', loc='w', kind='dot', color='blue')
        # Label(C=g.NW, name='NW', loc='nw', kind='dot', color='blue')
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
