# SVG Schematics by Ken Kundert
# encoding: utf8


# Description {{{1
"""
*SVG Schematic* is a Python library can be used to create schematics using SVG.
"""
__version__ = '0.3.0'
__released__ = '2018-02-21'


# License {{{1
# Copyright (C) 2016-2018 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


# Imports {{{1
from svgwrite import Drawing, cm, mm
from math import sqrt


# Utilities {{{1
# shift() {{{2
def shift(point, dx, dy):
    # shifts a given point in both the x and y directions
    return (point[0] + dx, point[1] + dy)

# shift_x() {{{2
def shift_x(point, dx):
    # shifts a given point in the x direction
    return (point[0] + dx, point[1])

# shift_y() {{{2
def shift_y(point, dy):
    # shifts a given point in the y direction
    return (point[0], point[1] + dy)

# with_x() {{{2
        # second argument is a number, use it
        # second argument is a number, use it
def with_x(p1, a2):
    # returns the first argument (a coordinate pair) with the x value replaced with
    # the second argument.
    try:
        # second argument is a coordinate pair, use its x value
        return (a2[0], p1[1])
    except TypeError:
        # second argument is a number, use it
        return (a2,    p1[1])

# with_y() {{{2
def with_y(p1, a2):
    # returns the first argument (a coordinate pair) with the x value replaced with
    # the second argument.
    try:
        # second argument is a coordinate pair, use its y value
        return (p1[0], a2[1])
    except TypeError:
        # second argument is a number, use it
        return (p1[0], a2)

# offsets_to_coordinates() {{{2
def offsets_to_coordinates(dest, x_offsets=None, y_offsets=None):
    x = y = 0
    if x_offsets:
        for k, v in x_offsets.items():
            x += v
            dest[k + '_x'] = x
    if y_offsets:
        for k, v in y_offsets.items():
            y += v
            dest[k + '_y'] = y


class Schematic(Drawing): # {{{1
    # Only one schematic is allowed at any one time.
    sch_LINE_WIDTH = 1
    sch_FONT_SIZE = 18
    sch_FONT_FAMILY = 'sans-serif'
    sch_DOT_RADIUS = 4
    sch_BACKGROUND = 'white'
    sch_OUTLINE = 'none'
    sch_schematic = None

    # constructor {{{2
    def __init__(self, filename, *args, **kwargs):
            # A design decision was made to only support one schematic at a
            # time. This allows us to instantiate components without indicating
            # which schematic they belong to.
            # Could instead support multiple schematics, allowing you to pass in
            # which schematic you want into each component, but instead have a
            # global default schematic.  In that way you could support 'with
            # Schematic():'. Then, the only global attribute schematic would
            # support would be sch_schematic. The others would become instance
            # attributes.
        # Attributes that start with sch_ are the ones we are adding to the
        # Drawing data structure, the prefix is used to avoid name clashes.
        Schematic.sch_schematic = self
        self.sch_min_x = 9999
        self.sch_min_y = 9999
        self.sch_max_x = -9999
        self.sch_max_y = -9999
        self.sch_font_size = kwargs.pop('font_size', Schematic.sch_FONT_SIZE)
        self.sch_font_family = kwargs.pop('font_family', Schematic.sch_FONT_FAMILY)
        self.sch_line_width = kwargs.pop('line_width', Schematic.sch_LINE_WIDTH)
        self.sch_dot_radius = kwargs.pop('dot_radius', Schematic.sch_DOT_RADIUS)
        self.sch_background = kwargs.pop('background', Schematic.sch_BACKGROUND)
        self.sch_outline = kwargs.pop('outline', Schematic.sch_OUTLINE)
        pad = kwargs.pop('pad', 0)
        self.sch_left_pad = kwargs.pop('left_pad', 0) + pad
        self.sch_right_pad = kwargs.pop('right_pad', 0) + pad
        self.sch_top_pad = kwargs.pop('top_pad', 0) + pad
        self.sch_bottom_pad = kwargs.pop('bottom_pad', 0) + pad
        super().__init__(filename, *args, **kwargs)

        # add a group for the background, must do it now so it ends up at the
        # bottom of the layer stack
        if self.sch_background != 'none' or self.sch_outline != 'none':
            self.sch_background_group = self.g(id='bkgnd')
            self.add(self.sch_background_group)

    # _update_bounds() {{{2
    def _update_bounds(self, min_x, min_y, max_x, max_y):
        if self.sch_schematic.sch_min_x > min_x:
            self.sch_schematic.sch_min_x = min_x
        if self.sch_schematic.sch_min_y > min_y:
            self.sch_schematic.sch_min_y = min_y
        if self.sch_schematic.sch_max_x < max_x:
            self.sch_schematic.sch_max_x = max_x
        if self.sch_schematic.sch_max_y < max_y:
            self.sch_schematic.sch_max_y = max_y

    # set_active_schematic() {{{2
    @classmethod
    def set_active_schematic(cls, schematic):
        cls.sch_schematic = schematic

    # close() {{{2
    def close(self, min_x=None, min_y=None, width=None, height=None):
        "Saves and closes schematic"
        # the arguments are deprecated, use padding when creating schematic
        # instead.
        if width is None:
            min_x = self.sch_min_x - self.sch_left_pad
            min_y = self.sch_min_y - self.sch_bottom_pad
            width = self.sch_max_x + self.sch_right_pad - min_x
            height = self.sch_max_y + self.sch_top_pad - min_y
        assert width > 0 and height > 0, "no components in schematic."
            # may also fail if components do not update bounds

        if self.sch_background != 'none' or self.sch_outline != 'none':
            self.sch_background_group.add(
                self.rect(
                    (min_x, min_y), (width, height),
                    fill = self.sch_background,
                    stroke = self.sch_outline, stroke_width=1,
                )
            )

        self.viewbox(min_x, min_y, width, height)
        self.save(pretty=True)
        self.sch_schematic = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            # don't close and therefore write the file if there is an exception
            self.close()


class Wire(Schematic): # {{{1
    '''Add wire to schematic.

    Wires should be given first so they are on the lowest layers.

    Args:
        points (list of pairs): the x,y coordinates of the wire vertices.
        kind (str): choose from ...
            'plain': points are connected with straight lines of any angle
            '|-': lines are constrained to follow Manhattan geometry,
                two line segments are inserted between each point if needed,
                the first segment is vertical.
            '-|': lines are constrained to follow Manhattan geometry,
                two line segments are inserted between each point if needed,
                the first segment is horizontal.
            '|-|': lines are constrained to follow Manhattan geometry,
                three line segments are inserted between each point if needed,
                the first is vertical and second falls at the midpoint.
            '-|-': lines are constrained to follow Manhattan geometry,
                three line segments are inserted between each point if needed,
                the first is horizontal and second falls at the midpoint.
        line_width (num): the line width
        color (str): you can change the color to help with debugging
    '''
    def __init__(self, points, kind='plain', line_width=None, color='black'):
        schematic = self.sch_schematic
        assert schematic, 'no active schematic'
        lw = schematic.sch_line_width if line_width is None else line_width

        # update bounds
        for x, y in points:
            self._update_bounds(x, y, x, y)

        # add the beginning and end points as attributes.
        self.b = points[0]
        self.e = points[1]

        # preprocess points to add corners when manhattan geometry is requested
        if kind != 'plain':
            prev = points[0]
            new_points = [prev]
            for i, p in enumerate(points[1:]):
                if p[0] != prev[0] and p[1] != prev[1]:
                    if kind == '|-':
                        new_points.append((prev[0], p[1]))
                    elif kind == '-|':
                        new_points.append((p[0], prev[1]))
                    if kind == '|-|':
                        ymid = (p[1] + prev[1])/2
                        new_points.append((prev[0], ymid))
                        new_points.append((p[0], ymid))
                    elif kind == '-|-':
                        xmid = (p[0] + prev[0])/2
                        new_points.append((xmid, prev[1]))
                        new_points.append((xmid, p[1]))
                new_points.append(p)
                prev = p
            points = new_points

        # draw wire
        wire = schematic.g(id='wire')
        line = schematic.polyline(
            points, fill='none',
            stroke_width=lw, stroke=color, stroke_linecap='round'
        )
        wire.add(line)
        schematic.add(wire)


class Tile(Schematic): # {{{1
    UNIT_WIDTH = 50
    UNIT_HEIGHT = 50

    # constructor {{{2
    def __init__(self, center, w=2, h=2):
        schematic = self.sch_schematic
        assert schematic, 'no active schematic'
        lw = schematic.sch_line_width
        w = w*Tile.UNIT_WIDTH
        h = h*Tile.UNIT_HEIGHT
        size = self.size = (w, h)
        x0, y0 = center
        self._update_bounds(x0 - w/2, y0 - h/2, x0 + w/2, y0 + h/2)

        # Create bounding box
        # Everything should fit within the bounding box.  It is not really
        # necessary, but it may make abutting and alignment easier in graphic
        # editors.
        bounding_box = schematic.rect(
            insert=(-w/2, -h/2),
            size=size,
            stroke='none',
            fill='none',
        )

        # Create groups that act as layers and attach to schematic
        symbol = self.symbol = schematic.g(id='symbol')
        symbol.add(bounding_box)
        schematic.add(symbol)

        # Text goes in its own layer so it is always on top and so that won't
        # get rotated so text will always be right side up.
        text = self.text = schematic.g(id='text')
        schematic.add(text)

        # Principal coordinates {{{2
        self.add_coordinates(center, dict(
            c = (0, 0),
            n = (0, -h/2),
            nw = (-w/2, -h/2),
            w = (-w/2, 0),
            sw = (-w/2, h/2),
            s = (0, h/2),
            se = (w/2, h/2),
            e = (w/2, 0),
            ne = (w/2, -h/2),
        ))

    # add_text() {{{2
    def add_text(self, text, position, alignment):
        # alignment is combination of vertical and horizontal alignment keys
        # vert: u=upper or top, m=middle, l=lower or bottom
        # horiz: l=left, m=middle, r=right
        schematic = self.sch_schematic

        # implement text alignment
        v, h = alignment
        kwargs = {}
        vert_alignments = dict(u='top', m='central', l='bottom')
        if v in vert_alignments:
            #kwargs['alignment_baseline'] = vert_alignments[v]
            # alignment baseline does not seem to work in inkview
            offset = dict(u=0.8, m=0.4, l=0)[v]
            position = shift(position, 0, offset*schematic.sch_font_size)
        horiz_alignments = dict(l='start', m='middle', r='end')
        if h in horiz_alignments:
            kwargs['text_anchor'] = horiz_alignments[h]

        # add the text
        text = schematic.text(
            text,
            insert=position,
            font_family=schematic.sch_font_family,
            font_size = schematic.sch_font_size,
            fill='black',
            **kwargs,
        )
        self.text.add(text)

    # map_pins() {{{2
    def map_pins(self, pins, center, orientation='', rotate=''):
        transformed = []
        for pin in pins:
            x = pin[0]
            y = pin[1]
            if rotate in orientation:
                x, y = y, -x
            if '|' in orientation:
                x = -x
            if '-' in orientation:
                y = -y
            transformed.append((x + center[0], y + center[1]))
        return transformed

    # add_coordinates() {{{2
    def add_coordinates(self, center, coordinates):
        # translate the components and then add them as attributes to self.
        self.__dict__.update({
            k:(v[0]+center[0], v[1]+center[1]) for k, v in coordinates.items()
        })

class Resistor(Tile): # {{{1
    '''Add resistor to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the resistor name
        value (str): the resistor value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(self, center, orientation='h', name=None, value=None, nudge=5):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        h, w = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        dx = 5
        dy = 10
        undulations = 6
        t0 = (w/2, 0)
        t1 = (-w/2, 0)

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-w/2+dr, -2*lw),
            size = (w-2*dr, 4*lw),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Resistor {{{2
        path = [t1]
        x = -dx*undulations
        for i in range(undulations):
            path.append((x, 0))
            path.append((x+dx, dy if i % 2 else -dy))
            x += 2*dx
            path.append((x, 0))
        path.append(t0)
        squiggle = schematic.polyline(
            path, fill='none',
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(squiggle)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([t0, t1], center, orientation, 'v')
        self.p, self.n = self.t

        # Text {{{2
        if 'v' in orientation:
            if name:
                self.add_text(name, shift(center, 1.5*dy, -nudge), 'll')
            if value:
                self.add_text(value, shift(center, 1.5*dy, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(center, 0, -2*dy), 'lm')
            if value:
                self.add_text(value, shift(center, 0, 2*dy), 'um')


class Capacitor(Tile): # {{{1
    '''Add capacitor to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str):
            'v' = vertical (default),
            'h' = horizontal,
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the capacitor name
        value (str): the capacitor value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(self, center, orientation='v', name=None, value=None, nudge=5):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        h, w = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        gap = 15
        dgap = 5
        c_width = 40
        t0 = (0, -h/2)
        t1 = (0, h/2)

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-2*lw, -h/2+dr),
            size = (4*lw, w-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Capacitor {{{2
        top_lead = schematic.line(
            start=t0, end=(0, -gap/2),
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(top_lead)
        bottom_lead = schematic.line(
            start=(0, gap/2-dgap), end=t1,
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(bottom_lead)
        top_plate = schematic.line(
            start=(-c_width/2, -gap/2), end=(c_width/2, -gap/2),
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(top_plate)
        bottom_plate = schematic.path(
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        # use Bezier path to draw curved bottom plate
        bottom_plate.push('M', (-c_width/2, +gap/2))
        bottom_plate.push('c', [
            (c_width/4, -1.5*dgap), (3*c_width/4, -1.5*dgap), (c_width, 0)
        ])
        symbol.add(bottom_plate)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([t0, t1], center, orientation, 'h')
        self.p, self.n = self.t

        # Text {{{2
        if 'h' in orientation:
            if name:
                self.add_text(name, shift(center, gap, -nudge), 'll')
            if value:
                self.add_text(value, shift(center, gap, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(center, nudge, -gap), 'll')
            if value:
                self.add_text(value, shift(center, nudge, gap), 'ul')


class Inductor(Tile): # {{{1
    '''Add inductor to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the inductor name
        value (str): the inductor value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(self, center, orientation='h', name=None, value=None, nudge=5):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        h, w = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        xinc = 20
        xdec = -5
        ypeak = 15
        ytrough = -10
        undulations = 4
        t0 = (w/2, 0)
        t1 = (-w/2, 0)

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-w/2+dr, -2*lw),
            size = (w-2*dr, 4*lw),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Inductor {{{2
        x = -xinc*(undulations/2 - 0.5)
        coil = schematic.path(
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        coil.push('M', t1)
        coil.push('L', (x, 0))
        curve = []
        for i in range(undulations):
            curve += [
                x,           -ypeak,
                x+xinc,      -ypeak,
                x+xinc,      0,
                x+xinc,      -ytrough,
                x+xinc+xdec, -ytrough,
                x+xinc+xdec, 0,
            ]
            x += xinc+xdec
        coil.push('C', curve[:-6])
        coil.push('L', t0)
        symbol.add(coil)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([t0, t1], center, orientation, 'v')
        self.p, self.n = self.t

        # Text {{{2
        if 'v' in orientation:
            if '|' in orientation:
                just, x_nudge = 'r', ytrough-nudge
            else:
                just, x_nudge = 'l', -ytrough+nudge
            if name:
                self.add_text(name, shift(center, x_nudge, -nudge), 'l'+just)
            if value:
                self.add_text(value, shift(center, x_nudge, nudge), 'u'+just)
        else:
            if name:
                self.add_text(name, shift(center, 0, -ypeak), 'lm')
            if value:
                self.add_text(value, shift(center, 0, ypeak), 'um')


class Diode(Tile): # {{{1
    '''Add diode to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the diode name
        value (str): the diode value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(self, center, orientation='h', name=None, value=None, nudge=5):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        h, w = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        dh = 35  # diode height
        dw = 40  # diode width
        t0 = (0, -h/2)
        t1 = (0, h/2)

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-2*lw, -h/2+dr),
            size = (4*lw, w-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Capacitor {{{2
        top_lead = schematic.line(
            start=t0, end=(0, -dh/2),
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(top_lead)
        bottom_lead = schematic.line(
            start=(0, dh/2), end=t1,
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(bottom_lead)
        cathode = schematic.line(
            start=(-dw/2, dh/2), end=(dw/2, dh/2),
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(cathode)
        anode = schematic.polygon(
            [(0, dh/2), (-dw/2, -dh/2), (dw/2, -dh/2)],
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(anode)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([t0, t1], center, orientation, 'h')
        self.a, self.c = self.t

        # Text {{{2
        if 'h' in orientation:
            if name:
                self.add_text(name, shift(center, dh/2+nudge, -nudge), 'll')
            if value:
                self.add_text(value, shift(center, dh/2+nudge, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(center, nudge/2, -dh/2-nudge), 'll')
            if value:
                self.add_text(value, shift(center, nudge/2, dh/2+nudge), 'ul')


class MOS(Tile): # {{{1
    '''Add MOS to schematic.

    Args:
        kind (str): choose from 'n' or 'p'
        center (pair): the x,y coordinates of the center of the tile
        orientation (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the fet name
        value (str): the fet value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(
        self, center, kind='nmos', orientation='v', name=None, value=None,
        nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        h, w = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        arrow_height = 12
        arrow_width = 30
        d = (w/2, -h/2)
        g = (-w/2, 0)
        s = (w/2, h/2)

        # Concealers {{{2
        # These are use to hide wiring that pass under component.
        ds_concealer = schematic.rect(
            insert = (w/2-2*lw, -h/2+dr),
            size = (4*lw, h-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(ds_concealer)
        g_concealer = schematic.rect(
            insert = (-w/2+dr, -2*lw),
            size = (w-2*dr, 4*lw),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(g_concealer)

        # FET {{{2
        channel = schematic.polyline(
            [   d,   # drain
                (w/2, -h/4),
                (0,   -h/4),
                (0,    h/4),
                (w/2,  h/4),
                s,   # source
            ],
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(channel)
        oxide = schematic.line(
            start=(0, -3*h/8), end=(0,  3*h/8), fill ='none',
            stroke_width=2*lw, stroke='black', stroke_linecap='square'
        )
        symbol.add(oxide)
        gate = schematic.line(
            start=(-w/8, -h/4), end=(-w/8, h/4), fill='none',
            stroke_width=lw, stroke='black', stroke_linecap='square'
        )
        symbol.add(gate)
        gate_lead = schematic.line(
            start=g, end=(-w/8, 0), fill='none',
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(gate_lead)
        arrow_x0 = w/4
        if 'p' in kind:
            arrow_y0 = -h/4
            arrow_left = arrow_x0+arrow_width/2
            arrow_right = arrow_x0-arrow_width/2
            d, s = s, d
        else:
            arrow_y0 = h/4
            arrow_left = arrow_x0-arrow_width/2
            arrow_right = arrow_x0+arrow_width/2
        arrow_top = arrow_y0-arrow_height/2
        arrow_bottom = arrow_y0+arrow_height/2
        arrow = schematic.polygon(
            [   (arrow_left, arrow_top),
                (arrow_right, arrow_y0),
                (arrow_left, arrow_bottom)
            ], fill='black', stroke='none'
        )
        symbol.add(arrow)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([d, g, s], center, orientation, 'h')
        self.d, self.g, self.s = self.t

        # Text {{{2
        if 'h' in orientation:
            if '-' in orientation:
                name_just, value_just = 'um', 'lm'
                offset, nudge = h/2, nudge
            else:
                name_just, value_just = 'lm', 'um'
                offset, nudge = -h/2, -nudge
            if name:
                self.add_text(name, shift(center, 0, nudge), name_just)
            if value:
                self.add_text(value, shift(center, 0, offset-nudge), value_just)
        else:
            if '|' in orientation:
                xjust, xnudge = 'r', -nudge
            else:
                xjust, xnudge  = 'l', nudge
            if name:
                if value:
                    just = 'l' + xjust
                else:
                    nudge = 0
                    just = 'm' + xjust
                self.add_text(name, shift(center, xnudge, -nudge), just)
            if value:
                self.add_text(value, shift(center, xnudge, nudge), 'u'+xjust)


class Amp(Tile): # {{{1
    '''Add amplifier to schematic.

    Args:
        kind (str): choose from ...
            'se' (single-ended),
            'oa' (opamp), and
            'da' (diffamp)
            'comp' (comparator)
        center (pair): the x,y coordinates of the center of the tile
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the amplifier name
        value (str): the amplifier value (currently unused)
    '''
    def __init__(
        self, center, kind='oa', orientation='h', name=None, value=None
    ):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        h, w = self.size
        lw = schematic.sch_line_width
        sign_size = 14
        nudge = 5
        vin  = (-w/2,  0)
        pin  = (-w/2, -h/4)
        nin  = (-w/2,  h/4)
        out  = ( w/2,  0)
        pout = ( w/2,  h/4)
        nout = ( w/2, -h/4)
        terms = [out, pin, nin]

        # Amp {{{2
        amp = schematic.polygon(
            [   ( w/2,  0),
                (-w/2, -h/2),
                (-w/2, +h/2),
            ], fill=schematic.sch_background,
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(amp)
        if kind in 'oa da comp'.split():
            minus = schematic.line(
                start=(-w/2+nudge, h/4),
                end=(-w/2+nudge+sign_size, h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(minus)
            plus_ew = schematic.line(
                start=(-w/2+nudge, -h/4),
                end=(-w/2+nudge+sign_size, -h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ew)
            plus_ns = schematic.line(
                start=(-w/2+nudge+sign_size/2, -h/4+sign_size/2),
                end=(-w/2+nudge+sign_size/2, -h/4-sign_size/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ns)
        else:
            terms = [out, vin]
        if kind == 'da':
            minus = schematic.line(
                start=(-2*sign_size+nudge, -h/4),
                end=(-sign_size+nudge, -h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(minus)
            plus_ew = schematic.line(
                start=(-2*sign_size+nudge, h/4),
                end=(-sign_size+nudge, h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ew)
            plus_ns = schematic.line(
                start=(-3*sign_size/2+nudge, h/4+sign_size/2-1),
                end=(-3*sign_size/2+nudge, h/4-sign_size/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ns)
            p_out_lead = schematic.line(
                start=(0, h/4),
                end=(w/2, h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(p_out_lead)
            n_out_lead = schematic.line(
                start=(0, -h/4),
                end=(w/2, -h/4),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(n_out_lead)
            terms = [pout, nout, pin, nin]
        if kind == 'comp':
            comp = schematic.polyline(
                [   (w/8-nudge,  h/8),
                    (w/8,        h/8),
                    (w/8,       -h/8),
                    (w/8+nudge, -h/8)
                ],
                fill='none',
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(comp)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'v')

        # Text {{{2
        if name:
            if 'v' in orientation:
                nudge = -h/8 if '-' in orientation else h/8
                self.add_text(name, shift(center, 0, nudge), 'mm')
            else:
                nudge = w/8 if '|' in orientation else -w/8
                self.add_text(name, shift(center, nudge, 0), 'mm')
        #if value:  ignore for now
        #    self.add_text(value, shift(center, -half/4, nudge), 'um')


class Gate(Tile): # {{{1
    '''Add gate to schematic.

    Args:
        kind (str): choose from: 'inv', 'buf', 'nand', 'and', 'nor', 'or',
            'xor', and 'xnor' (only inv is currently implemented).
        center (pair): the x,y coordinates of the center of the tile
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the amplifier name
        value (str): the amplifier value (currently unused)
    '''
    def __init__(
        self, center, kind='oa', orientation='h', name=None, value=None
    ):
        # Initialization and parameters {{{2
        super().__init__(center)
        symbol = self.symbol
        schematic = self.sch_schematic
        h, w = self.size
        lw = schematic.sch_line_width
        nudge = 5
        r = 8
        inv_x = 55
        inv_y = 70
        i  = (-w/2, 0)
        o  = ( w/2, 0)
        terms = [o, i]

        # Gate {{{2
        assert kind == 'inv'
        gate = schematic.polygon(
            [   ( inv_x/2-r,  0),
                (-inv_x/2-r, -inv_y/2),
                (-inv_x/2-r, +inv_y/2),
            ], fill=schematic.sch_background,
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(gate)
        ball = schematic.circle(
            center=(inv_x/2, 0), r=r, fill=schematic.sch_background,
            stroke_width=lw, stroke='black',
        )
        symbol.add(ball)
        in_lead = schematic.line(
            start=(-w/2, 0), end=(-inv_x/2-r, 0),
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(in_lead)
        out_lead = schematic.line(
            start=(w/2, 0), end=(inv_x/2+r, 0),
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(out_lead)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'v')

        # Text {{{2
        if name:
            if 'v' in orientation:
                nudge = -h/8 if '-' in orientation else h/8
                self.add_text(name, shift(center, 0, nudge), 'mm')
            else:
                nudge = w/8 if '|' in orientation else -w/8
                self.add_text(name, shift(center, nudge, 0), 'mm')
        #if value:  ignore for now
        #    self.add_text(value, shift(center, -half/4, nudge), 'um')


class Ground(Tile): # {{{1
    '''Add ground to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the ground name
        value (str): the ground value (currently unused)
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(
        self, center, kind='oa', orientation='v', name=None, value=None, nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center, 1, 1)
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        terms =[(0, 0)]

        # Ground {{{2
        ground = schematic.polyline(
            [   ( 0,   0),
                ( w/2, 0),
                ( 0,   h/2),
                (-w/2, 0),
                ( 0,   0),
            ], fill=schematic.sch_background,
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(ground)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'h')

        # Text {{{2
        if name:
            x_nudge = y_nudge = 0
            if 'h' in orientation:
                x_nudge = -nudge if '|' in orientation else nudge
                just = 'mr' if '|' in orientation else 'ml'
            else:
                y_nudge = -nudge if '-' in orientation else nudge
                just = 'lm' if '-' in orientation else 'um'
            self.add_text(name, shift(center, x_nudge, y_nudge), just)
        #if value:  ignore for now
        #    self.add_text(value, shift(center, -half/4, nudge), 'um')


class Source(Tile): # {{{1
    '''Add source to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        kind (str): choose from: 'empty', 'vdc', 'idc', 'sine', 'sum', 'mult'
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the source name
        value (str): the source value
        nudge (num): offset used when positioning text (if needed)
    '''
    def __init__(
        self, center, kind='empty', orientation='v', name=None, value=None,
        nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center, 2, 2)
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        size = self.size[0]
        r = size/4
        lw = schematic.sch_line_width
        sign_size = 14
        t0 = (0, -size/2)
        t1 = (0,  size/2)

        # Source {{{2
        source = schematic.circle(
            center=(0, 0), r=r, fill=schematic.sch_background,
            stroke_width=lw, stroke='black'
        )
        symbol.add(source)
        if kind not in 'sum mult'.split():
            # do not add leads to summer and multiplier
            pos_lead = schematic.line(
                start=t0,
                end=(0, -r),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(pos_lead)
            pos_lead = schematic.line(
                start=t1,
                end=(0, r),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(pos_lead)
        else:
            t0 = (0, -r)
            t1 = (0,  r)

        if kind == 'vdc':
            minus = schematic.line(
                start=(-sign_size/2, r/2),
                end=(sign_size/2, r/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(minus)
            plus_ew = schematic.line(
                start=(-sign_size/2, -r/2),
                end=(sign_size/2, -r/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ew)
            plus_ns = schematic.line(
                start=(0, -r/2+sign_size/2),
                end=(0, -r/2-sign_size/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(plus_ns)
        elif kind == 'idc':
            arrow = schematic.polygon(
                [   (0, -3*r/4),
                    (0, r/4),
                    (nudge, r/4),
                    (0, 3*r/4),
                    (-nudge, r/4),
                    (0, r/4),
                ],
                fill='black',
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(arrow)
        elif kind == 'sine':
            sine = schematic.path(
                fill='none', stroke_width=lw, stroke='black',
                stroke_linecap='round'
            )
            # use Bezier path to draw sine wave
            sine.push('M', (-12*r/16, 0))
            sine.push('C', [
                (-9*r/16, -r/2), (-3*r/16, -r/2), (0, 0), # positive half cycle
                (3*r/16, r/2), (9*r/16, r/2), (12*r/16, 0), # negative half cycle
            ])
            symbol.add(sine)
        elif kind == 'sum':
            line = schematic.line(  # vertical line
                start=(-r/2, 0), end=(r/2, 0), fill='black',
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(line)
            line = schematic.line(  # horizontal line
                start=(0, -r/2), end=(0, r/2), fill='black',
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(line)
        elif kind == 'mult':
            line = schematic.line(  # northwest-southeast line
                start=(-0.71*r/2, -0.71*r/2), end=(0.71*r/2, 0.71*r/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(line)
            line = schematic.line(  # northeast-southwest line
                start=(0.71*r/2, -0.71*r/2), end=(-0.71*r/2, 0.71*r/2),
                stroke_width=lw, stroke='black', stroke_linecap='round'
            )
            symbol.add(line)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins([t0, t1], center, orientation, 'h')

        # Principal coordinates {{{2
        # override those set in Tile
        self.add_coordinates(center, dict(
            c = (0, 0),
            n = (0, -r),
            nw = (-0.707*r, -0.707*r),
            w = (-r, 0),
            sw = (-0.707*r, 0.707*r),
            s = (0, r),
            se = (0.707*r, 0.707*r),
            e = (r, 0),
            ne = (0.707*r, -0.707*r),
        ))

        # Text {{{2
        if 'h' in orientation:
            if name:
                self.add_text(name, shift(center, r+nudge, -nudge), 'll')
            if value:
                self.add_text(value, shift(center, r+nudge, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(center, nudge, -r-nudge), 'll')
            if value:
                self.add_text(value, shift(center, nudge, r+nudge), 'ul')


class Pin(Tile): # {{{1
    '''Add pin to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        kind (str): choose from: 'dot', 'in', 'out', 'none'
            'dot' a solid dot, can specify name and value
            'in' a hollow dot, name on the left, no value
            'out' a hollow dot, name on the right, no value
            'none' is used to place name and value with no other marker
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the pin name
        value (str): the pin value (unused for in and out pins)
        w (num): the width of the tile (multiples of unit width)
        l (num): the height of the tile (multiples of unit height)
        nudge (num): offset used when positioning text (if needed)
    '''
    DEFAULT_KIND = 'out'

    def __init__(
        self, center, kind=None, orientation='v', name=None, value=None,
        w=1, l=1, nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center, w, l)
        schematic = self.sch_schematic
        symbol = self.symbol
        r = schematic.sch_dot_radius
        lw = schematic.sch_line_width
        if kind is None:
            kind = self.DEFAULT_KIND
        terms =[(0, 0)]

        # Pin {{{2
        if kind != 'none':
            pin = schematic.circle(
                center = (0, 0), r=r,
                fill = 'black' if kind == 'dot' else schematic.sch_background,
                stroke_width = lw,
                stroke = 'black',
            )
            symbol.add(pin)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'h' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'h')

        # Text {{{2
        x_nudge = r+nudge
        if kind == 'dot':
            if '|' in orientation:
                x_nudge, just = -x_nudge, 'r'
            else:
                just = 'l'
            if name:
                self.add_text(name, shift(center, x_nudge, -nudge), 'l' + just)
            if value:
                self.add_text(value, shift(center, x_nudge, nudge), 'u' + just)
        elif kind == 'out' and name:
            self.add_text(name, shift(center, r+nudge, 0), 'ml')
        elif kind == 'in' and name:
            self.add_text(name, shift(center, -(r+nudge), 0), 'mr')

class Dot(Pin): # {{{1
    DEFAULT_KIND = 'dot'

class Label(Tile): # {{{1
    '''Add label to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        kind (str): choose from 'plain', 'arrow', 'slash', 'dot'
        orientation (str): orientation of the symbol
        name (str): the label
        value (str): ignored
        loc (str): label location
            choose from 'c', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'
        w (num): the width of the tile (multiples of unit width)
        l (num): the length of the tile (multiples of unit width)
        nudge (num): offset used when positioning text (if needed)
    '''

    def __init__(
        self, center, kind='plain', loc='c', orientation='h', name=None, value=None, w=1, l=1,
        nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center, w, l)
        schematic = self.sch_schematic
        symbol = self.symbol
        terms =[(0, 0)]
        lw = schematic.sch_line_width
        arrow_height = 12
        arrow_width = 30
        slash_len = 12
        r = schematic.sch_dot_radius
        x_nudge = nudge
        y_nudge = nudge

        # Symbol {{{2
        if kind == 'arrow':
            arrow = schematic.polygon(
                [   (arrow_width/2, 0),
                    (-arrow_width/2, arrow_height/2),
                    (-arrow_width/2, -arrow_height/2),
                ], fill='black', stroke='none'
            )
            symbol.add(arrow)
            y_nudge += arrow_height/2
        elif kind == 'slash':
            slash = schematic.line(
                start = (-slash_len/2, slash_len/2),
                end = (slash_len/2, -slash_len/2),
                stroke_width = lw,
                stroke = 'black',
            )
            symbol.add(slash)
            y_nudge += slash_len/2
        elif kind == 'dot':
            symbol = schematic.circle(
                center = (0, 0), r=r,
                fill = 'black' if kind == 'dot' else schematic.sch_background,
                stroke_width = lw,
                stroke = 'black',
            )
            symbol.add(symbol)
            y_nudge += r
            x_nudge += r

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)

        # Text {{{2
        if name:
            dx = dy = 0
            v_just = h_just = 'm'
            if 'n' in loc:
                dy = -y_nudge
                v_just = 'l'
            if 's' in loc:
                dy = y_nudge
                v_just = 'u'
            if 'e' in loc:
                dx = x_nudge
                h_just = 'l'
            if 'w' in loc:
                dx = -x_nudge
                h_just = 'r'
            just = v_just + h_just
            self.add_text(name, shift(center, dx, dy), just)
        self.t = self.map_pins(terms, center)

class Box(Tile): # {{{1
    '''Add box to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the pin name
        value (str): the pin value (unused for in and out pins)
        w (num): the width of the box (multiples of unit width)
        h (num): the height of the box (multiples of unit height)
        nudge (num): offset used when positioning text (if needed)
        line_width (num): the line width
        background (str): color of interior of box
    '''

    def __init__(
        self, center, orientation='h', name=None, value=None, w=2, h=1.5,
        nudge=5, line_width=None, background=None
    ):
        # Initialization and parameters {{{2
        super().__init__(center, w, h)
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width if line_width is None else line_width
        terms = [(w/2, 0), (-w/2, 0)]

        # Box {{{2
        fill = schematic.sch_background if background is None else background
        box = schematic.rect(
            insert = (-w/2, -h/2),
            size = self.size,
            fill = fill,
            stroke_width = lw,
            stroke = 'black',
        )
        symbol.add(box)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'v')

        # Text {{{2
        if value:
            if name:
                self.add_text(name, shift(center, 0, -nudge), 'lm')
            self.add_text(value, shift(center, 0, nudge), 'um')
        else:
            if name:
                self.add_text(name, shift(center, 0, 0), 'mm')

class Switch(Tile): # {{{1
    '''Add switch to schematic.

    Args:
        center (pair): the x,y coordinates of the center of the tile
        kind (str): the switch type, choose from 'spst' and 'spdt'
        orientation (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the pin name
        value (str): the pin value (unused for in and out pins)
        w (num): the width of the box (multiples of unit width)
        h (num): the height of the box (multiples of unit height)
        nudge (num): offset used when positioning text (if needed)
    '''

    def __init__(
        self, center, kind='spst', orientation='h', name=None, value=None,
        nudge=5
    ):
        # Initialization and parameters {{{2
        super().__init__(center, 2, 2)
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        sep = self.UNIT_HEIGHT
        gap = self.UNIT_WIDTH
        r = 3
        lw = schematic.sch_line_width

        # Concealer {{{2
        # These are use to hide wiring that pass under component.
        concealer = schematic.rect(
            insert = (-gap/2, -sep/2-2*lw),
            size = (gap, sep+4*lw),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Switch {{{2
        switch = schematic.line(
            start=(-gap/2, 0), end=(gap/2, -sep/2),
            stroke_width=lw, stroke='black',
        )
        symbol.add(switch)
        l_pole = schematic.circle(
            (-gap/2, 0), r=r, fill='black',
            stroke_width=lw, stroke='black',
        )
        symbol.add(l_pole)
        tl = (-w/2, 0)
        l_lead = schematic.line(
            start=tl, end=(-gap/2, 0),
            stroke_width=lw, stroke='black',
        )
        symbol.add(l_lead)
        if kind == 'spdt':
            symbol.add(l_pole)
            t_pole = schematic.circle(
                (gap/2, -sep/2), r=r, fill='black',
                stroke_width=lw, stroke='black',
            )
            symbol.add(t_pole)
            tt = (w/2, -sep/2)
            t_lead = schematic.line(
                start=tt, end=(gap/2, -sep/2),
                stroke_width=lw, stroke='black',
            )
            symbol.add(t_lead)
            b_pole = schematic.circle(
                (gap/2, sep/2), r=r, fill='black',
                stroke_width=lw, stroke='black',
            )
            symbol.add(b_pole)
            tb = (w/2, sep/2)
            b_lead = schematic.line(
                start=tb, end=(gap/2, sep/2),
                stroke_width=lw, stroke='black',
            )
            symbol.add(b_lead)
            terms=[tt, tb, tl]
        else:
            r_pole = schematic.circle(
                (gap/2, 0), r=r, fill='black',
                stroke_width=lw, stroke='black',
            )
            symbol.add(r_pole)
            tr = (w/2, 0)
            r_lead = schematic.line(
                start=tr, end=(gap/2, 0),
                stroke_width=lw, stroke='black',
            )
            symbol.add(r_lead)
            terms=[tr, tl]

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(center)
        if '|' in orientation:
            symbol.scale(-1, 1)
        if '-' in orientation:
            symbol.scale(1, -1)
        if 'v' in orientation:
            symbol.rotate(-90)
        self.t = self.map_pins(terms, center, orientation, 'v')

        # Text {{{2
        if 'v' in orientation:
            if '|' in orientation:
                hjust = 'r'
                nudge = -nudge
            else:
                hjust = 'l'
            offset = gap/2+r if '-' in orientation else -gap/2-r
            if value:
                dy = offset+nudge
                self.add_text(value, shift(center, nudge, -dy), 'u'+hjust)
                just = 'l'+hjust
            else:
                dy = 0
                just = 'm'+hjust
            if name:
                self.add_text(name, shift(center, nudge, -dy), just)
        else:
            if '-' in orientation:
                vjust = 'l'
                nudge = -nudge
            else:
                vjust = 'u'
            if value:
                dx = gap/2+r+nudge
                self.add_text(value, shift(center, dx, nudge), vjust+'l')
                just = vjust + 'r'
            else:
                dx = 0
                just = vjust + 'm'
            if name:
                self.add_text(name, shift(center, -dx, nudge), just)


# Tests {{{1
if __name__ == '__main__':
    from math import ceil, sqrt

    class TestCase:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    # cases {{{2
    cases = [
        TestCase(
            component = Resistor,
            name = 'R{l}',
            value = '50Ω',
        ),
        TestCase(
            component = Capacitor,
            name = 'C{l}',
            value = '50μF',
        ),
        TestCase(
            component = Inductor,
            name = 'L{l}',
            value = '50μH',
        ),
        TestCase(
            component = Diode,
            name = 'D{l}',
            value = '10',
        ),
        TestCase(
           component = MOS,
            name = 'Mn{l}',
            value = '10',
            xoff = -50,
            yoff = 0,
            kwargs = dict(kind = 'nmos'),
        ),
        TestCase(
            component = MOS,
            name = 'Mp{l}',
            value = '10',
            xoff = -50,
            yoff = 0,
            kwargs = dict(kind = 'pmos'),
        ),
        TestCase(
            component = Amp,
            name = 'A{l}',
            kwargs = dict(kind = 'se'),
        ),
        TestCase(
            component = Amp,
            name = 'OA{l}',
            kwargs = dict(kind = 'oa'),
        ),
        TestCase(
            component = Amp,
            name = 'DA{l}',
            kwargs = dict(kind = 'da'),
        ),
        TestCase(
            component = Ground,
            name = 'G{l}{o}',
        ),
        TestCase(
            component = Source,
            name = 'U{l}',
            value = '50',
            kwargs = dict(kind = 'empty'),
        ),
        TestCase(
            component = Source,
            name = 'V{l}',
            value = '5V',
            kwargs = dict(kind = 'vdc'),
        ),
        TestCase(
            component = Source,
            name = 'I{l}',
            value = '5μA',
            kwargs = dict(kind = 'idc'),
        ),
        TestCase(
            component = Source,
            name = 'V{l}',
            value = '5μA',
            kwargs = dict(kind = 'sum'),
        ),
        TestCase(
            component = Source,
            name = 'V{l}',
            value = '5μA',
            kwargs = dict(kind = 'mult'),
        ),
        TestCase(
            component = Pin,
            name = 'Vx',
            value = '0V',
            kwargs = dict(kind = 'dot'),
        ),
        TestCase(
            component = Pin,
            name = 'out',
            kwargs = dict(kind = 'in'),
        ),
        TestCase(
            component = Pin,
            name = 'in',
            kwargs = dict(kind = 'out'),
        ),
        TestCase(
            component = Label,
            name = 'n',
            kwargs = dict(loc = 'n'),
        ),
        TestCase(
            component = Label,
            name = 'ne',
            kwargs = dict(loc = 'ne'),
        ),
        TestCase(
            component = Label,
            name = 'e',
            kwargs = dict(loc = 'e'),
        ),
        TestCase(
            component = Label,
            name = 'se',
            kwargs = dict(loc = 'se'),
        ),
        TestCase(
            component = Label,
            name = 's',
            kwargs = dict(loc = 's'),
        ),
        TestCase(
            component = Label,
            name = 'sw',
            kwargs = dict(loc = 'sw'),
        ),
        TestCase(
            component = Label,
            name = 'w',
            kwargs = dict(loc = 'w'),
        ),
        TestCase(
            component = Label,
            name = 'nw',
            kwargs = dict(loc = 'nw'),
        ),
        TestCase(
            component = Label,
            name = 'c',
            kwargs = dict(loc = 'c'),
        ),
        TestCase(
            component = Box,
            name = 'box',
            value = 'value',
        ),
        TestCase(
            component = Switch,
            name = 'Sw',
            value = 'value',
        ),
        TestCase(
            component = Switch,
            name = 'Sw',
            value = 'value',
            kwargs = dict(kind = 'spdt'),
        ),
        TestCase(
            component = Gate,
            name = 'U',
            value = 'value',
            kwargs = dict(kind = 'inv'),
        ),
    ]
    value_is_orientation = True

    def make_grid(cases): # {{{2
        K = len(cases)
        sqrt_k = ceil(sqrt(K))
        k = 0
        for i in range(sqrt_k):
            for j in range(sqrt_k):
                yield i, j, cases[k]
                k += 1
                if k == K:
                    return

    # create schematic {{{2
    schematic = Schematic(
        filename = "schematic.svg",
        debug = True
    )

    # run each case {{{2
    for i, j, case in make_grid(cases):
        def instantiate(case, dx, dy, orientation):
            component = case.component
            name = getattr(case, 'name', 'U{l}')
            value = getattr(case, 'value', '500U')
            xoff = getattr(case, 'xoff', 0)
            yoff = getattr(case, 'yoff', 0)
            if 'h' in orientation:
                xoff, yoff = yoff, -xoff
            if '|' in orientation:
                xoff = -xoff
            if '-' in orientation:
                yoff = -yoff
            if dy == 0:
                location = 'l' if dx < 0 else 'r'
            else:
                assert dx == 0
                location = 't' if dy < 0 else 'b'
            name = name.format(l=location, o=orientation)
            if value_is_orientation:
                value = orientation
            else:
                value = value.format(i=1),
            kwargs = dict(
                center = (X0 + xoff + 100*dx, Y0 + yoff + 100*dy),
                orientation = orientation,
                name = name,
                value = value
            )
            if hasattr(case, 'kwargs'):
                kwargs.update(case.kwargs)
            c = component(**kwargs)

            # draw terminals if they exist
            if hasattr(c, 'terms'):
                d = 5
                for i, t in enumerate(c.terms):
                    schematic.add(schematic.line(
                        (t[0]-d,t[1]-d), (t[0]+d,t[1]+d),
                        stroke='black', stroke_width=1
                    ))
                    schematic.add(schematic.line(
                        (t[0]+d,t[1]-d), (t[0]-d,t[1]+d),
                        stroke='black', stroke_width=1
                    ))
                    schematic.add(schematic.text(
                        str(i),
                        insert=t,
                        font_family=schematic.sch_font_family,
                        font_size = schematic.sch_font_size,
                        fill='black',
                    ))

        X0 = 200 + 800*i
        Y0 = 200 + 400*j
        wire = schematic.rect(
            insert = (X0-100, Y0-100),
            size = (200, 200),
            stroke_width = 1,
            stroke = 'magenta',
            fill = 'none'
        )
        schematic.add(wire)

        instantiate(case, -1, 0, 'v')
        instantiate(case, 0, -1, 'h')
        instantiate(case, 1, 0, 'v|')
        instantiate(case, 0, 1, 'h-')

        X0 = 600 + 800*i
        wire = schematic.rect(
            insert = (X0-100, Y0-100),
            size = (200, 200),
            stroke_width = 1,
            stroke = 'magenta',
            fill = 'none'
        )
        schematic.add(wire)

        instantiate(case, -1, 0, 'v-')
        instantiate(case, 0, -1, 'h|')
        instantiate(case, 1, 0, 'v-|')
        instantiate(case, 0, 1, 'h-|')

    # close schematic {{{2
    # determine size of schematic
    I = J = 0
    for i, j, case in make_grid(cases):
        I = max(i, I)
        J = max(j, J)
    schematic.viewbox(0, 0, 800*(I+1), 400*(J+1))

    # color background
    bkgnd = schematic.rect(
        insert = (0,0),
        size = (800*(I+1), 400*(J+1)),
        fill = 'green',
        fill_opacity = 0.1
    )
    schematic.add(bkgnd)

    schematic.close()
