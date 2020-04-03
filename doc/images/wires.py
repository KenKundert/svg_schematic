from svg_schematic import Schematic, Label, Resistor, Wire, with_x
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'wires.svg',
        background = 'none',
        line_width = 2,
    ):
        r11 = Resistor(orient='h')
        r12 = Resistor(orient='h', n=r11.p, off=(50,50))
        w = Wire([r11.p, r12.n], kind='plain')
        c = with_x(w.m, r12.E)
        Label(name="kind='plain'", C=c, xoff=25, loc='e', w=5)

        r21 = Resistor(orient='h', C=r11.C, yoff=100)
        r22 = Resistor(orient='h', n=r21.p, off=(50,50))
        w = Wire([r21.p, r22.n], kind='|-')
        c = with_x(w.m, r22.E)
        Label(name="kind='|-'", C=c, xoff=25, loc='e', w=5)

        r31 = Resistor(orient='h', C=r21.C, yoff=100)
        r32 = Resistor(orient='h', n=r31.p, off=(50,50))
        w = Wire([r31.p, r32.n], kind='-|')
        c = with_x(w.m, r32.E)
        Label(name="kind='-|'", C=c, xoff=25, loc='e', w=5)

        r41 = Resistor(orient='h', C=r31.C, yoff=100)
        r42 = Resistor(orient='h', n=r41.p, off=(50,50))
        w = Wire([r41.p, r42.n], kind='|-|')
        c = with_x(w.m, r42.E)
        Label(name="kind='|-|'", C=c, xoff=25, loc='e', w=5)

        r51 = Resistor(orient='h', C=r41.C, yoff=100)
        r52 = Resistor(orient='h', n=r51.p, off=(50,50))
        w = Wire([r51.p, r52.n], kind='-|-')
        c = with_x(w.m, r52.E)
        Label(name="kind='-|-'", C=c, xoff=25, loc='e', w=5)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

