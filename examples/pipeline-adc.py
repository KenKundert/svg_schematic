#!/usr/bin/env python3

from svg_schematic import (
    Schematic, Amp, Box, Label, Pin, Source, Wire,
    midpoint, shift_x, shift, with_x, with_y,
)
from inform import Error, error, os_error

try:
    with Schematic(filename = 'pipeline-adc.svg', line_width=2):

        # Stage 1
        i = Pin(kind='in', name='in')
        s1 = Box(NW=i.t, off=(25,-62.5), w=10.5, h=4.5, background='lightgray')
        Label(C=s1.SE, loc='nw', name='Stage 1')
        adc = Box(W=i.t, off=(75,100), name='2 bit', value='Flash')
        dac = Box(i=adc.o, xoff=50, name='2 bit', value='DAC')
        sh = Box(C=with_x(i.t, midpoint(adc.C, dac.C)), name='SAH')
        sum = Source(W=with_x(i.t, dac.E), xoff=25, kind='sum', orient='h|')
        Label(C=sum.W, loc='nw', name='+')
        Label(C=sum.S, loc='se', name='−')
        amp = Amp(i=sum.E, xoff=25, kind='se', name='4×')
        Wire([i.t, sh.i])
        Wire([sh.o, sum.W])
        Wire([sum.E, amp.i])
        Wire([shift_x(i.t, 50), adc.i], kind='|-')
        Wire([adc.o, dac.i])
        Wire([dac.o, sum.S], kind='-|')

        # Stages 2, 3, 4
        s2 = Box(N=dac.S, off=(25,75), name='Stage 2')
        s3 = Box(W=s2.E, xoff=50, name='Stage 3')
        s4 = Box(W=s3.E, xoff=50, name='4 bit', value='Flash')
        Wire([s2.o, s3.i])
        Wire([s3.o, s4.i])
        Wire([
            amp.o,
            shift_x(amp.o, 50),
            shift(s1.SE, 25,25),
            shift(s2.NW, -25, -25),
            shift_x(s2.W, -25),
            s2.W,
        ])

        # Error correction
        ec = Box(NW=s2.SW, off=(-75, 50), name='Digital Error Correction', w=9, h=1)
        out = Pin(t=shift_x(ec.o, 50), kind='out', name='out', w=2)
        Wire([ec.o, out.t])
        Label(C=shift_x(ec.E, 25), kind='slash', loc='s', name='10')

        w1 = Wire([midpoint(adc.o, dac.i), with_y(midpoint(adc.o, dac.i), ec.N)])
        w2 = Wire([s2.S, with_y(s2.S, ec.N)])
        w3 = Wire([s3.S, with_y(s3.S, ec.N)])
        w4 = Wire([s4.S, with_y(s4.S, ec.N)])
        Label(C=w1.e, yoff=-25, kind='slash', loc='w', name='2', nudge=8)
        Label(C=w2.e, yoff=-25, kind='slash', loc='w', name='2', nudge=8)
        Label(C=w3.e, yoff=-25, kind='slash', loc='w', name='2', nudge=8)
        Label(C=w4.e, yoff=-25, kind='slash', loc='w', name='4', nudge=8)

except Error as e:
    e.report()
except OSError as e:
    error(os_error(e))
