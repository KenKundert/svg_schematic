from svg_schematic import Schematic, Pin, Wire, shift_x, shift_y
from inform import Error, error, os_error

try:
    with Schematic(filename = 'pin.svg'):
        Wire([(0, -25), (0,175)], color='cyan')
        p = Pin(kind='none', name='none', value='none value')
        Wire([shift_x(p.C, -50), shift_x(p.C, 50)])
        p = Pin(kind='dot', name='dot', C=p.C, yoff=50, value='dot value')
        Wire([shift_x(p.C, -50), shift_x(p.C, 50)])
        Wire([shift_y(p.C, -25), shift_y(p.C, 25)])
        p = Pin(kind='in', name='in', C=p.C, yoff=50)
        Wire([p.C, shift_x(p.C, 25)])
        p = Pin(kind='out', name='out', C=p.C, yoff=50)
        Wire([p.C, shift_x(p.C, -50)])
except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
