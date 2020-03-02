from svg_schematic import (
    Schematic, Label, Resistor, Wire
)
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'wires.svg',
        background = 'none',
    ):
        r11 = Resistor(orient='h')
        r12 = Resistor(orient='h', n=r11.p, off=(50,50))
        Wire([r11.p, r12.n], kind='plain')
        Label(name="kind='plain'", C=r12.C, off=(100, -25))


        r21 = Resistor(orient='h', C=r11.C, yoff=100)
        r22 = Resistor(orient='h', n=r21.p, off=(50,50))
        Wire([r21.p, r22.n], kind='|-')
        Label(name="kind='|-'", C=r22.C, off=(100, -25))

        r31 = Resistor(orient='h', C=r21.C, yoff=100)
        r32 = Resistor(orient='h', n=r31.p, off=(50,50))
        Wire([r31.p, r32.n], kind='-|')
        Label(name="kind='-|'", C=r32.C, off=(100, -25))

        r41 = Resistor(orient='h', C=r31.C, yoff=100)
        r42 = Resistor(orient='h', n=r41.p, off=(50,50))
        Wire([r41.p, r42.n], kind='|-|')
        Label(name="kind='|-|'", C=r42.C, off=(100, -25))

        r51 = Resistor(orient='h', C=r41.C, yoff=100)
        r52 = Resistor(orient='h', n=r51.p, off=(50,50))
        Wire([r51.p, r52.n], kind='-|-')
        Label(name="kind='-|-'", C=r52.C, off=(100, -25))

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))

