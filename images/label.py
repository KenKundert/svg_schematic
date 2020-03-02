from svg_schematic import Schematic, Label, Wire, shift_x, shift_y
from inform import Error, error, os_error

try:
    with Schematic(filename = 'label.svg'):
        Wire([(0, -25), (0,225)], color='blue')
        l = Label(kind='plain', name='plain', loc='se', w=3)
        Wire([shift_x(l.C, -50), shift_x(l.C, 50)])
        l = Label(kind='arrow', name='arrow', C=l.C, yoff=50, loc='se', w=3)
        Wire([shift_x(l.C, -50), shift_x(l.C, 50)])
        l = Label(kind='arrow|', name='arrow|', C=l.C, yoff=50, loc='se', w=3)
        Wire([shift_x(l.C, -50), shift_x(l.C, 50)])
        l = Label(kind='slash', name='slash', C=l.C, yoff=50, loc='se', w=3)
        Wire([shift_x(l.C, -50), shift_x(l.C, 50)])
        l = Label(kind='dot', name='dot', C=l.C, yoff=50, loc='se', w=3)
        Wire([shift_x(l.C, -50), shift_x(l.C, 50)])
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
