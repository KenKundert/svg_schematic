from svg_schematic import Schematic, BJT, Label
from inform import Error, error, os_error

try:
    with Schematic(
        filename = 'orient.svg',
        background = 'none',
    ):
        q11 = BJT(orient='v')
        l11 = Label(N=q11.S, name="orient='v'")
        q12 = BJT(W=q11.E, xoff=50, orient='v|')
        l12 = Label(N=q12.S, name="orient='v|'")
        q13 = BJT(W=q12.E, xoff=50, orient='v-')
        l13 = Label(N=q13.S, name="orient='v-'")
        q14 = BJT(W=q13.E, xoff=50, orient='v|-')
        l14 = Label(N=q14.S, name="orient='v|-'")
        q21 = BJT(N=l11.S, yoff=25, orient='h')
        l21 = Label(N=q21.S, name="orient='h'")
        q22 = BJT(N=l12.S, yoff=25, orient='h|')
        l22 = Label(N=q22.S, name="orient='h|'")
        q23 = BJT(N=l13.S, yoff=25, orient='h-')
        l23 = Label(N=q23.S, name="orient='h-'")
        q24 = BJT(N=l14.S, yoff=25, orient='h|-')
        l24 = Label(N=q24.S, name="orient='h|-'")
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
