from svg_schematic import Schematic, Resistor, Capacitor, Inductor, Wire, shift_y
from inform import Error, error, os_error

try:
    with Schematic(filename = "rlc.svg"):
        r = Resistor(name='R', orient='v')
        c = Capacitor(C=r.C, xoff=100, name='C', orient='v')
        l = Inductor(C=c.C, xoff=100, name='L', orient='v|')
        Wire([r.p, c.p, l.p], kind='-|-')
        Wire([r.n, c.n, l.n], kind='-|-')

    with Schematic(filename = "rlc1a.svg"):
        r = Resistor(name='R', orient='v')
        c = Capacitor(W=r.E, name='C', orient='v')
        l = Inductor(W=c.E, name='L', orient='v|')
        Wire([r.p, c.p, l.p], kind='-|-')
        Wire([r.n, c.n, l.n], kind='-|-')

    with Schematic(filename = "rlc1b.svg"):
        r = Resistor(name='R', orient='h')
        c = Capacitor(n=r.p, name='C', orient='h|')
        l = Inductor(n=c.p, name='L', orient='h')

    with Schematic(filename = "rlc2.svg"):
        r = Resistor(name='R', orient='v')
        c = Capacitor(C=r.C, off=(100,25), name='C', orient='v')
        l = Inductor(C=c.C, xoff=100, name='L', orient='v|')
        Wire([r.p, c.p, l.p], kind='-|-')
        Wire([r.n, c.n, l.n], kind='-|-')

    with Schematic(filename = "rlc3.svg"):
        r = Resistor(name='R', orient='v')
        c = Capacitor(C=r.C, xoff=100, name='C', orient='v')
        l = Inductor(C=c.C, xoff=100, name='L', orient='v|')
        Wire([r.p, shift_y(r.p, -12.5), shift_y(c.p, -12.5), c.p])
        Wire([c.p, shift_y(c.p, -12.5), shift_y(l.p, -12.5), l.p])
        Wire([r.n, shift_y(r.n, 12.5), shift_y(c.n, 12.5), c.n])
        Wire([c.n, shift_y(c.n, 12.5), shift_y(l.n, 12.5), l.n])

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
