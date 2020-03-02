#!/usr/bin/env python3

from svg_schematic import (
    Schematic, shift_x, shift_y, Amp, Box, Ground, Label, Pin, Source, Wire
)

with Schematic(
    filename = 'receiver.svg',
    font_size = 12,
    font_family = 'sans',
    outline = 'none',
    pad = 20,
    line_width = 2,
) as schematic:

    # Input from horn antenna
    rf_in = Pin(kind='in', name='L-band Horn', w=3)
    Label(C=rf_in.C, yoff=15, loc='w', name='fc=1420MHz', w=3.5, nudge=14)
    Label(C=rf_in.C, yoff=30, loc='w', name='BW=15MHz', w=3.5, nudge=14)

    # First preamp
    rf_preamp1 = Amp(i=rf_in.t, xoff=25, kind='se', name='RF Preamp1')
    Label(C=rf_preamp1.S, loc='s', name='A>=26dB')
    Wire([rf_in.t, rf_preamp1.i])

    # Second preamp
    rf_preamp2 = Amp(i=rf_preamp1.o, xoff=25, kind='se', name='RF Preamp2')
    Label(C=rf_preamp2.S, loc='s', name='A>=26dB')
    Wire([rf_preamp1.o, rf_preamp2.i])

    # RF band-pass filter
    rf_bpf = Box(i=rf_preamp2.o, xoff=25, name='RF BPF')
    l = Label(C=rf_bpf.S, loc='s', name='fc=1380MHz')
    Label(C=l.S, name='BW=320MHz')
    Wire([rf_preamp2.o, rf_bpf.i])

    # First RF amplifier
    rf_amp1 = Amp(i=rf_bpf.o, xoff=25, kind='se', name='RF Amp1')
    Label(C=rf_amp1.S, loc='s', name='A<=20dB')
    Wire([rf_bpf.o, rf_amp1.i])

    # Second RF amplifier
    rf_amp2 = Amp(i=rf_amp1.o, xoff=25, kind='se', name='RF Amp2')
    Label(C=rf_amp2.S, loc='s', name='A<=20dB')
    Wire([rf_amp1.o, rf_amp2.i])

    # RF mixer
    rf_mixer = Source(W=rf_amp2.o, xoff=25, kind='mult')
    Label(C=rf_mixer.N, loc='n', name='DSB')
    Wire([rf_amp2.o, rf_mixer.W])

    # RF local oscillator
    rf_lo = Source(
        p=rf_mixer.S, yoff=50, kind='sine',
        name='fo=1230MHz', value='P=10dBm'
    )
    Ground(t=rf_lo.n)
    Wire([rf_mixer.S, rf_lo.N])

    # IF band-pass filter
    if_bpf = Box(i=rf_mixer.E, xoff=25, name='IF BPF')
    l= Label(C=if_bpf.S, loc='s', name='fc=190MHz')
    Label(C=l.S, name='BW=22MHz')
    Wire([rf_mixer.E, if_bpf.i])

    # IF amplifier
    if_amp = Amp(i=if_bpf.o, xoff=25, name='IF Amp')
    Label(C=if_amp.S, loc='s', name='A=20dB')
    Wire([if_bpf.o, if_amp.i])

    # IF mixer
    if_mixer = Source(W=if_amp.o, xoff=20, kind='mult')
    Label(C=if_mixer.N, loc='n', name='SSB')
    Wire([if_amp.o, if_mixer.W])

    # IF local oscillator
    if_lo = Source(
        p=if_mixer.S, yoff=50, kind='sine',
        name='fo=190MHz', value='P=10dBm'
    )
    Ground(t=if_lo.n)
    Wire([if_mixer.S, if_lo.p])

    # Baseband low-pass filter
    bb_lpf = Box(i=if_mixer.E, xoff=25, name='BB LPF')
    Label(C=bb_lpf.S, loc='s', name='BW=2MHz (var)')
    Wire([if_mixer.E, bb_lpf.i])

    # Analog-to-digital converter
    adc = Box(i=bb_lpf.o, xoff=25, name='ADC')
    Label(C=adc.S, loc='s', name='Fclk=var')
    Wire([bb_lpf.o, adc.i])

    # Output
    bb_out = Pin(t=adc.o, xoff=50, kind='out', name='out', w=1.5)
    w = Wire([adc.o, bb_out.t])
    Label(C=w.m, kind='slash', loc='s', name='8')
