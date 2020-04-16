# SVG Schematics by Ken Kundert
# encoding: utf8


# Description {{{1
"""
*SVG Schematic* is a Python library can be used to create schematics using SVG.
"""
__version__ = '1.0.0'
__released__ = '2020-04-16'


# License {{{1
# Copyright (C) 2018-20 Kenneth S. Kundert
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
from svgwrite import Drawing
from math import sqrt, atan2, pi
from inform import Error, plural


# Utilities {{{1
# shift() {{{2
def shift(point, dx, dy):
    """Shifts a given point in both the x and y directions."""
    return (point[0] + dx, point[1] + dy)

# shift_x() {{{2
def shift_x(point, dx):
    """Shifts a given point in the x direction."""
    return (point[0] + dx, point[1])

# shift_y() {{{2
def shift_y(point, dy):
    """Shifts a given point in the y direction."""
    return (point[0], point[1] + dy)

# with_x() {{{2
def with_x(p1, a2):
    """Returns the first argument (a coordinate pair) with the x value replaced with
    the second argument."""
    try:
        # second argument is a coordinate pair, use its x value
        return (a2[0], p1[1])
    except TypeError:
        # second argument is a number, use it
        return (a2,    p1[1])

# with_y() {{{2
def with_y(p1, a2):
    """Returns the first argument (a coordinate pair) with the x value replaced with
    the second argument."""
    try:
        # second argument is a coordinate pair, use its y value
        return (p1[0], a2[1])
    except TypeError:
        # second argument is a number, use it
        return (p1[0], a2)

# midpoint() {{{2
def midpoint(p1, p2):
    """Returns the point midway between two points."""
    return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)

# midpoint_x() {{{2
def midpoint_x(p1, p2):
    """Returns the point midway between two points."""
    return ((p1[0] + p2[0])/2, p1[1])

# midpoint_y() {{{2
def midpoint_y(p1, p2):
    """Returns the point midway between two points."""
    return (p1[0], (p1[1] + p2[1])/2)

# offsets_to_coordinates() {{{2
def offsets_to_coordinates(dest, x_offsets=None, y_offsets=None):
    # deprecated
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
            min_x = self.sch_min_x - self.sch_left_pad - self.sch_line_width
            min_y = self.sch_min_y - self.sch_bottom_pad - self.sch_line_width
            width = self.sch_max_x + self.sch_right_pad + self.sch_right_pad - min_x + 2*self.sch_line_width
            height = self.sch_max_y + self.sch_top_pad + self.sch_bottom_pad - min_y + 2*self.sch_line_width
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
    def __init__(
        self, points, kind='plain', line_width=None, color='black', **extra
    ):
        schematic = self.sch_schematic
        assert schematic, 'no active schematic'
        lw = schematic.sch_line_width if line_width is None else line_width

        # update bounds
        for x, y in points:
            self._update_bounds(x, y, x, y)

        # add the beginning and end points as attributes.
        self.b = points[0]
        self.e = points[-1]
        self.m = midpoint(self.b, self.e)

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
            stroke_width=lw, stroke=color, stroke_linecap='round', **extra
        )
        wire.add(line)
        schematic.add(wire)


class Tile(Schematic): # {{{1
    UNIT_WIDTH = 50
    UNIT_HEIGHT = 50
    COORDINATE_OFFSETS = dict(
        C = (0, 0),
        N = (0, -1/2),
        NW = (-1/2, -1/2),
        W = (-1/2, 0),
        SW = (-1/2, 1/2),
        S = (0, 1/2),
        SE = (1/2, 1/2),
        E = (1/2, 0),
        NE = (1/2, -1/2),
    )

    # constructor {{{2
    def __init__(self):
        schematic = self.sch_schematic
        assert schematic, 'no active schematic'
        lw = schematic.sch_line_width
        w, h = size = self.size
        x0, y0 = self.center
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

        # Text goes in its own layer so it is always on top, and so that won't
        # get rotated such that it always remains right side up.
        text = self.text = schematic.g(id='text')
        schematic.add(text)

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
            str(text),
            insert = position,
            font_family = schematic.sch_font_family,
            font_size = schematic.sch_font_size,
            fill = 'black',
            **kwargs
        )
        self.text.add(text)

    # set_coordinates() {{{2
    # finds the center and sets principle components as attributes
    def set_coordinates(
        self, kwargs, pins=None, orient='', rotate='', h=2, w=2, extra=False
    ):
        w = w*Tile.UNIT_WIDTH
        h = h*Tile.UNIT_HEIGHT
        self.size = (w, h)

        # scale the pins to w & h
        # self.pins is used internally, center and orientation are normalized
        self.pins = {k: (w*v[0], h*v[1]) for k, v in pins.items()}

        # rotate and flip pins about normalized center
        pins = {}
        for name, loc in self.pins.items():
            x, y = loc
            if rotate and rotate in orient:
                x, y = y, -x
            if '|' in orient:
                x = -x
            if '-' in orient:
                y = -y
            pins[name] = x, y

        # scale the principle coordinates (C, N, NE, E, SE, ...)
        offsets = {k: (w*v[0], h*v[1]) for k, v in self.COORDINATE_OFFSETS.items()}

        # combine pins with principle components
        offsets.update(pins)

        # identify the location names in kwargs and compute the center
        location_names = offsets.keys() & kwargs.keys()
        if location_names:
            loc_name = location_names.pop()
            if location_names:
                raise Error(
                    'too many location specifiers:',
                    ', '.join(specified_names),
                    culprit=self.class_name()
                )
            # compute the center
            offset = offsets[loc_name]
            loc = kwargs.pop(loc_name)
            x0, y0 = loc[0] - offset[0], loc[1] - offset[1]
        else:
            #raise Error('location not specified.', culprit=self.class_name())
            x0, y0 = 0,0

        # get offsets specified in kwargs
        if 'off' in kwargs:
            xoff, yoff = kwargs.pop('off')
        else:
            xoff = kwargs.pop('xoff', 0)
            yoff = kwargs.pop('yoff', 0)
        x0 += xoff
        y0 += yoff
        self.center = (x0, y0)

        # translate pins and principle components and add as attributes
        self.__dict__.update({
            k:(v[0]+x0, v[1]+y0) for k, v in offsets.items()
        })

        # return unused kwargs if requested
        if extra:
            return kwargs

        # otherwise complain about any unused kwargs
        if kwargs:
            raise Error(
                'unknown {}:'.format(plural(kwargs).format('argument')),
                ', '.join(kwargs.keys()),
                culprit=self.class_name()
            )

    # name() {{{2
    def class_name(self):
        return self.__class__.__name__


class Resistor(Tile): # {{{1
    '''Add resistor to schematic.

    Args:
        orient (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the resistor name
        value (str): the resistor value
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the resistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(self, orient='h', name=None, value=None, nudge=5, **kwargs):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(p=(1/2, 0), n=(-1/2, 0)), orient, 'v')
        super().__init__()

        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        dx = 5
        dy = 10
        undulations = 6
        p = self.pins['p']
        n = self.pins['n']

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-w/2+dr, -2*lw),
            size = (w-2*dr, 4*lw),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Resistor {{{2
        path = [n]
        x = -dx*undulations
        for i in range(undulations):
            path.append((x, 0))
            path.append((x+dx, dy if i % 2 else -dy))
            x += 2*dx
            path.append((x, 0))
        path.append(p)
        squiggle = schematic.polyline(
            path, fill='none',
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(squiggle)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'v' in orient:
            if name:
                self.add_text(name, shift(self.center, 1.5*dy, -nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, 1.5*dy, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(self.center, 0, -2*dy), 'lm')
            if value:
                self.add_text(value, shift(self.center, 0, 2*dy), 'um')


class Capacitor(Tile): # {{{1
    '''Add capacitor to schematic.

    Args:
        orient (str):
            'v' = vertical (default),
            'h' = horizontal,
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the capacitor name
        value (str): the capacitor value
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the capacitor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(self, orient='v', name=None, value=None, nudge=5, **kwargs):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(p=(0, -1/2), n=(0, 1/2)), orient, 'h')
        super().__init__()

        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        gap = 15
        dgap = 5
        c_width = 40
        p = self.pins['p']
        n = self.pins['n']

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
            start=p, end=(0, -gap/2),
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(top_lead)
        bottom_lead = schematic.line(
            start=(0, gap/2-dgap), end=n,
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
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'h' in orient:
            if name:
                self.add_text(name, shift(self.center, gap, -nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, gap, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(self.center, nudge, -gap), 'll')
            if value:
                self.add_text(value, shift(self.center, nudge, gap), 'ul')


class Inductor(Tile): # {{{1
    '''Add inductor to schematic.

    Args:
        orient (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the inductor name
        value (str): the inductor value
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the inductor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(self, orient='h', name=None, value=None, nudge=5, **kwargs):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(p=(1/2, 0), n=(-1/2, 0)), orient, 'v')
        super().__init__()

        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        xinc = 20
        xdec = -5
        ypeak = 15
        ytrough = -10
        undulations = 4
        p = self.pins['p']
        n = self.pins['n']

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
        coil.push('M', n)
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
        coil.push('L', p)
        symbol.add(coil)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'v' in orient:
            if '|' in orient:
                just, x_nudge = 'r', ytrough-nudge
            else:
                just, x_nudge = 'l', -ytrough+nudge
            if name:
                self.add_text(name, shift(self.center, x_nudge, -nudge), 'l'+just)
            if value:
                self.add_text(value, shift(self.center, x_nudge, nudge), 'u'+just)
        else:
            if name:
                self.add_text(name, shift(self.center, 0, -ypeak), 'lm')
            if value:
                self.add_text(value, shift(self.center, 0, ypeak), 'um')


class Diode(Tile): # {{{1
    '''Add diode to schematic.

    Args:
        orient (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the diode name
        value (str): the diode value
        nudge (num): offset used when positioning text (if needed)
        color (str): color of symbol
        C, N, NE, E, SE, S, SW, W, NW, a, c (xy location):
            Use to specify the location of a feature of the diode.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(self,
        orient='h', name=None, value=None, nudge=5, color='black', **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(a=(0, -1/2), c=(0, 1/2)), orient, 'h')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        dh = 35  # diode height
        dw = 40  # diode width
        a = self.pins['a']
        c = self.pins['c']

        # Concealer {{{2
        concealer = schematic.rect(
            insert = (-2*lw, -h/2+dr),
            size = (4*lw, w-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(concealer)

        # Diode {{{2
        top_lead = schematic.line(
            start=a, end=(0, -dh/2),
            fill='none', stroke_width=lw, stroke=color, stroke_linecap='round'
        )
        symbol.add(top_lead)
        bottom_lead = schematic.line(
            start=(0, dh/2), end=c,
            fill='none', stroke_width=lw, stroke=color, stroke_linecap='round'
        )
        symbol.add(bottom_lead)
        cathode = schematic.line(
            start=(-dw/2, dh/2), end=(dw/2, dh/2),
            fill='none', stroke_width=lw, stroke=color, stroke_linecap='round'
        )
        symbol.add(cathode)
        anode = schematic.polygon(
            [(0, dh/2), (-dw/2, -dh/2), (dw/2, -dh/2)],
            fill='none', stroke_width=lw, stroke=color, stroke_linecap='round'
        )
        symbol.add(anode)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'h' in orient:
            if name:
                self.add_text(name, shift(self.center, dh/2+nudge, -nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, dh/2+nudge, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(self.center, nudge/2, -dh/2-nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, nudge/2, dh/2+nudge), 'ul')


class BJT(Tile): # {{{1
    '''Add BJT to schematic.

    Args:
        kind (str): choose from 'npn' or 'pnp' (or just 'n' or 'p')
            if kind is '' the arrow is not shown.
        orient (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the fet name
        value (str): the fet value
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, c, b, e (xy location):
            Use to specify the location of a feature of the transistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='npn', orient='v', name=None, value=None,
        nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        is_pnp = kind[0:1].lower() == 'p'
        if is_pnp:
            pins = dict(c=(1/2, 1/2), b=(-1/2, 0), e=(1/2, -1/2))
        else:
            pins = dict(c=(1/2, -1/2), b=(-1/2, 0), e=(1/2, 1/2))
        self.set_coordinates(kwargs, pins, orient, 'h')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        arrow_height = 12
        arrow_width = 30
        c = self.pins['c']
        b = self.pins['b']
        e = self.pins['e']
        if is_pnp:
            c, e = e, c

        # Concealers {{{2
        # These are use to hide wiring that pass under component.
        ce_concealer = schematic.rect(
            insert = (w/2-2*lw, -h/2+dr),
            size = (4*lw, h-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(ce_concealer)
        # b_concealer = schematic.rect(
        #     insert = (-w/2+dr, -2*lw),
        #     size = (w-2*dr, 4*lw),
        #     stroke = 'none',
        #     fill = schematic.sch_background,
        # )
        # symbol.add(b_concealer)

        # Transistor {{{2
        channel = schematic.polyline(
            [   c,   # collector
                (w/2, -3*h/8),
                (0,   -h/4),
                (0,    h/4),
                (w/2,  3*h/8),
                e,   # emitter
            ],
            fill='none', stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(channel)
        base = schematic.line(
            start=(0, -3*h/8), end=(0,  3*h/8), fill ='none',
            stroke_width=3*lw, stroke='black', stroke_linecap='square'
        )
        symbol.add(base)
        base_lead = schematic.line(
            start=b, end=(0, 0), fill='none',
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(base_lead)
        if kind:
            arrow_x0 = w/4
            rotate_arrow=180*atan2(1/8, 1/2)/pi
            if is_pnp:
                arrow_y0 = -h/4
                arrow_left = arrow_x0+arrow_width/2
                arrow_right = arrow_x0-arrow_width/2
                rotate_arrow=-rotate_arrow
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
            arrow.rotate(rotate_arrow, center=(0, arrow_y0))
            symbol.add(arrow)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'h' in orient:
            if '-' in orient:
                name_just, value_just = 'um', 'lm'
                offset, nudge = h/2, nudge
            else:
                name_just, value_just = 'lm', 'um'
                offset, nudge = -h/2, -nudge
            if name:
                self.add_text(name, shift(self.center, 0, nudge), name_just)
            if value:
                self.add_text(value, shift(self.center, 0, offset-nudge), value_just)
        else:
            if '|' in orient:
                xjust, xnudge = 'r', -nudge
            else:
                xjust, xnudge  = 'l', nudge
            if name:
                if value:
                    just = 'l' + xjust
                else:
                    nudge = 0
                    just = 'm' + xjust
                self.add_text(name, shift(self.center, xnudge, -nudge), just)
            if value:
                self.add_text(value, shift(self.center, xnudge, nudge), 'u'+xjust)


class MOS(Tile): # {{{1
    '''Add MOS to schematic.

    Args:
        kind (str): choose from 'nmos' or 'pmos' (or just 'n' or 'p')
            if kind is '' the arrow is not shown.
        orient (str):
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis
            '|' = flip about vertical axis
        name (str): the fet name
        value (str): the fet value
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, d, g, s (xy location):
            Use to specify the location of a feature of the transistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='n', orient='v', name=None, value=None, nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        is_pmos =  kind[0:1].lower() == 'p'
        if is_pmos:
            pins = dict(d=(1/2, 1/2), g=(-1/2, 0), s=(1/2, -1/2))
        else:
            pins = dict(d=(1/2, -1/2), g=(-1/2, 0), s=(1/2, 1/2))
        self.set_coordinates(kwargs, pins, orient, 'h')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        w, h = self.size
        lw = schematic.sch_line_width
        dr = max(2*lw, schematic.sch_dot_radius)
        arrow_height = 12
        arrow_width = 30
        d = self.pins['d']
        g = self.pins['g']
        s = self.pins['s']
        if is_pmos:
            d, s = s, d

        # Concealers {{{2
        # These are use to hide wiring that pass under component.
        ds_concealer = schematic.rect(
            insert = (w/2-2*lw, -h/2+dr),
            size = (4*lw, h-2*dr),
            stroke = 'none',
            fill = schematic.sch_background,
        )
        symbol.add(ds_concealer)
        # g_concealer = schematic.rect(
        #     insert = (-w/2+dr, -2*lw),
        #     size = (w-2*dr, 4*lw),
        #     stroke = 'none',
        #     fill = schematic.sch_background,
        # )
        # symbol.add(g_concealer)

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
        if kind:
            arrow_x0 = w/4
            if is_pmos:
                arrow_y0 = -h/4
                arrow_left = arrow_x0+arrow_width/2
                arrow_right = arrow_x0-arrow_width/2
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
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'h' in orient:
            if '-' in orient:
                name_just, value_just = 'um', 'lm'
                offset, nudge = h/2, nudge
            else:
                name_just, value_just = 'lm', 'um'
                offset, nudge = -h/2, -nudge
            if name:
                self.add_text(name, shift(self.center, 0, nudge), name_just)
            if value:
                self.add_text(value, shift(self.center, 0, offset-nudge), value_just)
        else:
            if '|' in orient:
                xjust, xnudge = 'r', -nudge
            else:
                xjust, xnudge  = 'l', nudge
            if name:
                if value:
                    just = 'l' + xjust
                else:
                    nudge = 0
                    just = 'm' + xjust
                self.add_text(name, shift(self.center, xnudge, -nudge), just)
            if value:
                self.add_text(value, shift(self.center, xnudge, nudge), 'u'+xjust)


class Amp(Tile): # {{{1
    '''Add amplifier to schematic.

    Args:
        kind (str): choose from ...
            'se' (single-ended),
            'oa' (opamp), and
            'da' (diffamp)
            'comp' (comparator)
        orient (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the amplifier name
        value (str): the amplifier value (currently unused)
        w (num), h (num) : the width and height.
        C, N, NE, E, SE, S, SW, W, NW, pi, i, ni, po, n, no. (xy location):
            Use to specify the location of a feature of the amplifier.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='oa', orient='h', name=None, value=None, w=2, h=2, **kwargs
    ):
        # Initialization and parameters {{{2
        pins = dict(
            i =  (-1/2,  0),
            pi = (-1/2, -1/4),
            ni = (-1/2,  1/4),
            o =  ( 1/2,  0),
            po = ( 1/2,  1/4),
            no = ( 1/2, -1/4),
        )
        self.set_coordinates(kwargs, pins, orient, 'v', w=w, h=h)
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        sign_size = 14
        nudge = 5

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
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)


        # Text {{{2
        if name:
            if 'v' in orient:
                nudge = -h/8 if '-' in orient else h/8
                self.add_text(name, shift(self.center, 0, nudge), 'mm')
            else:
                nudge = w/8 if '|' in orient else -w/8
                self.add_text(name, shift(self.center, nudge, 0), 'mm')
        #if value:  ignore for now
        #    self.add_text(value, shift(self.center, -half/4, nudge), 'um')


class Gate(Tile): # {{{1
    '''Add gate to schematic.

    Args:
        kind (str): choose from: 'inv', 'buf', 'nand', 'and', 'nor', 'or',
            'xor', and 'xnor' (only inv is currently implemented).
        orient (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the amplifier name
        value (str): the amplifier value (currently unused)
        C, N, NE, E, SE, S, SW, W, NW, i, o (xy location):
            Use to specify the location of a feature of the gate.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='inv', orient='h', name=None, value=None, **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(i=(-1/2, 0), o=(1/2, 0)), orient, 'v')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        nudge = 5
        r = 8
        inv_x = 55
        inv_y = 70

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
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if name:
            if 'v' in orient:
                nudge = -h/8 if '-' in orient else h/8
                self.add_text(name, shift(self.center, 0, nudge), 'mm')
            else:
                nudge = w/8 if '|' in orient else -w/8
                self.add_text(name, shift(self.center, nudge, 0), 'mm')
        #if value:  ignore for now
        #    self.add_text(value, shift(self.center, -half/4, nudge), 'um')


class Ground(Tile): # {{{1
    '''Add ground to schematic.

    Args:
        orient (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the ground name
        value (str): the ground value (currently unused)
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, t (xy location):
            Use to specify the location of a feature of the ground.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='oa', orient='v', name=None, value=None, nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(t=(0, 0)), orient, 'h', w=1, h=1)
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        lw = schematic.sch_line_width
        terms =[(0, 0)]
        scale = 0.4

        # Ground {{{2
        ground = schematic.polyline(
            [   ( 0,   0),
                ( scale*w, 0),
                ( 0,   scale*h),
                (-scale*w, 0),
                ( 0,   0),
            ], fill=schematic.sch_background,
            stroke_width=lw, stroke='black', stroke_linecap='round'
        )
        symbol.add(ground)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if name:
            x_nudge = y_nudge = 0
            if 'h' in orient:
                x_nudge = -nudge if '|' in orient else nudge
                just = 'mr' if '|' in orient else 'ml'
            else:
                y_nudge = -nudge if '-' in orient else nudge
                just = 'lm' if '-' in orient else 'um'
            self.add_text(name, shift(self.center, x_nudge, y_nudge), just)
        #if value:  ignore for now
        #    self.add_text(value, shift(self.center, -half/4, nudge), 'um')


class Source(Tile): # {{{1
    COORDINATE_OFFSETS = dict(
        C = (0, 0),
        N = (0, -1/4),
        NW = (-0.70711/4, -0.70711/4),
        W = (-1/4, 0),
        SW = (-0.70711/4, 0.70711/4),
        S = (0, 1/4),
        SE = (0.70711/4, 0.70711/4),
        E = (1/4, 0),
        NE = (0.70711/4, -0.70711/4),
    )

    '''Add source to schematic.

    Args:
        kind (str): choose from:
             'empty', 'vdc', 'idc', 'sine', 'sum', 'mult',
            'cv' (controlled voltage) or 'ci' (controlled current)
        orient (str): choose from:
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the source name
        value (str): the source value
        color (str): color of symbol
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the source.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    def __init__(
        self, kind='empty', orient='v', name=None, value=None, color='black',
        nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(p=(1/2, 0), n=(-1/2, 0)), orient, 'v')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        assert self.size[0] == self.size[1]
        size = self.size[0]
        r = size/4
        dr = 5*size/16  # the 'radius' of diamond without elongation
        elong = size/16
        lw = schematic.sch_line_width
        sign_size = 14
        arrow_width = 5

        # Source {{{2
        if kind in ('cv', 'ci'):
            source = schematic.polygon(
                [   (0, -dr-elong),
                    (dr-elong, 0),
                    (0, dr+elong),
                    (-dr+elong, 0),
                ],
                fill=schematic.sch_background,
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            src_t = (0, -dr-elong)
            src_b = (0,  dr+elong)
        else:
            source = schematic.circle(
                center=(0, 0), r=r, fill=schematic.sch_background,
                stroke_width=lw, stroke=color
            )
            src_t = (0, -r)
            src_b = (0,  r)
        symbol.add(source)
        if kind not in 'sum mult'.split():
            # do not add leads to summer and multiplier
            pos_lead = schematic.line(
                start=src_t,
                end=(0, -size/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(pos_lead)
            pos_lead = schematic.line(
                start=src_b,
                end=(0, size/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(pos_lead)

        if kind in ('vdc', 'cv'):
            minus = schematic.line(
                start=(-sign_size/2, r/2),
                end=(sign_size/2, r/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(minus)
            plus_ew = schematic.line(
                start=(-sign_size/2, -r/2),
                end=(sign_size/2, -r/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(plus_ew)
            plus_ns = schematic.line(
                start=(0, -r/2+sign_size/2),
                end=(0, -r/2-sign_size/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(plus_ns)
        elif kind in ('idc', 'ci'):
            arrow = schematic.polygon(
                [   (0, -3*r/4),
                    (0, r/4),
                    (arrow_width, r/4),
                    (0, 3*r/4),
                    (-arrow_width, r/4),
                    (0, r/4),
                ],
                fill=color,
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(arrow)
        elif kind == 'sine':
            sine = schematic.path(
                fill='none', stroke_width=lw, stroke=color,
                stroke_linecap='round'
            )
            # use Bezier path to draw sine wave
            sine.push('M', (-12*r/16, 0))
            sine.push('C', [
                (-9*r/16, -r/2), (-3*r/16, -r/2), (0, 0), # positive half cycle
                (3*r/16, r/2), (9*r/16, r/2), (12*r/16, 0), # negative half cycle
            ])
            symbol.add(sine)
        elif kind == 'noise':
            randwave = [
                (-1, -0.76),
                (-0.96, -0.29),
                (-0.92, 0.19),
                (-0.88, 0.62),
                (-0.84, -0.8),
                (-0.8, -0.71),
                (-0.76, 0.35),
                (-0.72, 0.54),
                (-0.68, 0.87),
                (-0.64, 0.02),
                (-0.6, -0.42),
                (-0.56, 0.59),
                (-0.52, 0.08),
                (-0.48, -0.87),
                (-0.44, 0.34),
                (-0.4, 0),
                (-0.36, -0.55),
                (-0.32, 0.77),
                (-0.28, -0.41),
                (-0.24, 0.66),
                (-0.2, -0.42),
                (-0.16, -0.1),
                (-0.12, 0.25),
                (-0.08, -0.95),
                (-0.04, 0.52),
                (0, 0.9),
                (0.04, 0.98),
                (0.08, -0.79),
                (0.12, 0.43),
                (0.16, -0.4),
                (0.2, -0.92),
                (0.24, 0.82),
                (0.28, -0.42),
                (0.32, 0.1),
                (0.36, 0.52),
                (0.4, 0.85),
                (0.44, -0.97),
                (0.48, 0.48),
                (0.52, 0.18),
                (0.56, 0.94),
                (0.6, 0.91),
                (0.64, 0.19),
                (0.68, -0.26),
                (0.72, -0.47),
                (0.76, 1),
                (0.8, 0.7),
                (0.84, -0.67),
                (0.88, 0.1),
                (0.92, -0.84),
                (0.96, 0.78),
                (1, -0.95),
            ]
            noise = schematic.polyline(
                [(3*r*x/4, r*y/3) for x, y in randwave ],
                fill='none',
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(noise)
        elif kind == 'sum':
            line = schematic.line(  # vertical line
                start=(-r/2, 0), end=(r/2, 0),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(line)
            line = schematic.line(  # horizontal line
                start=(0, -r/2), end=(0, r/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(line)
        elif kind == 'mult':
            line = schematic.line(  # northwest-southeast line
                start=(-0.71*r/2, -0.71*r/2), end=(0.71*r/2, 0.71*r/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(line)
            line = schematic.line(  # northeast-southwest line
                start=(0.71*r/2, -0.71*r/2), end=(-0.71*r/2, 0.71*r/2),
                stroke_width=lw, stroke=color, stroke_linecap='round'
            )
            symbol.add(line)
        elif kind != 'empty':
            raise NotImplementedError(kind)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'h' in orient:
            symbol.rotate(-90)

        # Principal coordinates {{{2
        # override those set in Tile

        # Text {{{2
        if 'h' in orient:
            if name:
                self.add_text(name, shift(self.center, r+nudge, -nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, r+nudge, nudge), 'ul')
        else:
            if name:
                self.add_text(name, shift(self.center, nudge, -r-nudge), 'll')
            if value:
                self.add_text(value, shift(self.center, nudge, r+nudge), 'ul')


class Pin(Tile): # {{{1
    '''Add pin to schematic.

    Args:
        kind (str): choose from: 'dot', 'in', 'out', 'none'
            'dot' a solid dot, can specify name and value
            'in' a hollow dot, name on the left, no value
            'out' a hollow dot, name on the right, no value
            'none' is used to place name and value with no other marker
        orient (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the pin name
        value (str): the pin value (unused for in and out pins)
        w (num): the width of the tile (multiples of unit width)
        h (num): the height of the tile (multiples of unit height)
        color (str): color of symbol
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW (xy location):
            Use to specify the location of a feature of the pin.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''
    DEFAULT_KIND = 'out'

    def __init__(
        self, kind=None, orient='v', name=None, value=None, w=1, h=1,
        color='black', nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, dict(t=(0, 0)), orient, 'v', w=w, h=h)
        super().__init__()
        schematic = self.sch_schematic
        symbol = self.symbol
        r = schematic.sch_dot_radius
        lw = schematic.sch_line_width
        if kind is None:
            kind = self.DEFAULT_KIND

        # Pin {{{2
        if kind != 'none':
            if kind == 'in':
                cx = -r
            elif kind == 'out':
                cx = r
            else:
                cx = 0
            pin = schematic.circle(
                center = (cx, 0), r=r,
                fill = color if kind == 'dot' else schematic.sch_background,
                stroke_width = lw,
                stroke = color,
            )
            symbol.add(pin)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        #if '|' in orient:
        #    symbol.scale(-1, 1)
        #if '-' in orient:
        #    symbol.scale(1, -1)
        #if 'h' in orient:
        #    symbol.rotate(-90)

        # Text {{{2
        x_nudge = r+nudge
        if kind == 'out' and name:
            self.add_text(name, shift(self.center, 2*r+nudge, 0), 'ml')
        elif kind == 'in' and name:
            self.add_text(name, shift(self.center, -(2*r+nudge), 0), 'mr')
        else:
            if '|' in orient:
                x_nudge, just = -x_nudge, 'r'
            else:
                just = 'l'
            if name:
                self.add_text(name, shift(self.center, x_nudge, -nudge), 'l' + just)
            if value:
                self.add_text(value, shift(self.center, x_nudge, nudge), 'u' + just)

class Dot(Pin): # {{{1
    DEFAULT_KIND = 'dot'

class Label(Tile): # {{{1
    '''Add label to schematic.

    Args:
        kind (str): choose from 'plain', 'arrow', 'arrow|', 'slash', 'dot'
        orient (str): orient of the symbol
        name (str): the label
        value (str): ignored
        loc (str): label location
            choose from 'c', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'
        w (num): the width of the tile (multiples of unit width)
        h (num): the height of the tile (multiples of unit height)
        color (str): color of the marker
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the resistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''

    def __init__(
        self, kind='plain', loc='c', orient='h', name=None, value=None, w=1, h=1,
        color='black', nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        self.set_coordinates(kwargs, {}, orient, 'v', w=w, h=h)
        super().__init__()
        schematic = self.sch_schematic
        symbol = self.symbol
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
                ], fill=color, stroke='none'
            )
            symbol.add(arrow)
            y_nudge += arrow_height/2
        elif kind == 'arrow|':
            arrow = schematic.polygon(
                [   (0, 0),
                    (-arrow_width, arrow_height/2),
                    (-arrow_width, -arrow_height/2),
                ], fill=color, stroke='none'
            )
            symbol.add(arrow)
            y_nudge += arrow_height/2
        elif kind == 'slash':
            slash = schematic.line(
                start = (-slash_len/2, slash_len/2),
                end = (slash_len/2, -slash_len/2),
                stroke_width = lw,
                stroke = color,
            )
            symbol.add(slash)
            y_nudge += slash_len/2
        elif kind == 'dot':
            dot = schematic.circle(
                center = (0, 0), r=r,
                fill = color if kind == 'dot' else schematic.sch_background,
                stroke_width = lw,
                stroke = color,
            )
            symbol.add(dot)
            y_nudge += r
            x_nudge += r

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if name:
            loc = loc.lower()
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
            self.add_text(name, shift(self.center, dx, dy), just)

class Box(Tile): # {{{1
    '''Add box to schematic.

    Args:
        orient (str): choose from ...
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
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the resistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''

    def __init__(
        self, orient='h', name=None, value=None, nudge=5, line_width=None,
        background=None, w=2, h=1.5, **kwargs
    ):
        # Initialization and parameters {{{2
        pins = dict(
            i =  (-1/2,  0),
            pi = (-1/2, -1/4),
            ni = (-1/2,  1/4),
            o =  ( 1/2,  0),
            po = ( 1/2, -1/4),
            no = ( 1/2,  1/4),
        )
        extra = self.set_coordinates(kwargs, pins, orient, 'v', w=w, h=h, extra=True)
        super().__init__()
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
            **extra
        )
        symbol.add(box)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if value:
            if name:
                self.add_text(name, shift(self.center, 0, -nudge), 'lm')
            self.add_text(value, shift(self.center, 0, nudge), 'um')
        else:
            if name:
                self.add_text(name, shift(self.center, 0, 0), 'mm')

class Switch(Tile): # {{{1
    '''Add switch to schematic.

    Args:
        kind (str): the switch type, choose from 'spst' and 'spdt'
        orient (str): choose from ...
            'v' = vertical,
            'h' = horizontal (default),
            '-' = flip about horizontal axis,
            '|' = flip about vertical axis
        name (str): the pin name
        value (str): the pin value (unused for in and out pins)
        dots (bool): whether the dots should be drawn
        nudge (num): offset used when positioning text (if needed)
        C, N, NE, E, SE, S, SW, W, NW, p, n (xy location):
            Use to specify the location of a feature of the resistor.
        off (xy location), xoff (real), yoff (real):
            Specify the offset from the specified location.
    '''

    def __init__(
        self, kind='spst', orient='h', name=None, value=None, dots=False,
        nudge=5, **kwargs
    ):
        # Initialization and parameters {{{2
        pins = dict(i=(-1/2, 0), o=(1/2, 0), ot=(1/2, -1/4), ob=(1/2, 1/4))
        self.set_coordinates(kwargs, pins, orient, 'v')
        super().__init__()
        symbol = self.symbol
        schematic = self.sch_schematic
        w, h = self.size
        r = 3
        lw = schematic.sch_line_width
        i = self.pins['i']
        o = self.pins['o']
        ot = self.pins['ot']
        ob = self.pins['ob']
        sep = h/2
        gap = w/2

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
        if dots:
            l_pole = schematic.circle(
                (-gap/2, 0), r=r, fill='black',
                stroke_width=lw, stroke='black',
            )
            symbol.add(l_pole)
        l_lead = schematic.line(
            start=i, end=(-gap/2, 0),
            stroke_width=lw, stroke='black',
        )
        symbol.add(l_lead)
        if kind == 'spdt':
            if dots:
                t_pole = schematic.circle(
                    (gap/2, -sep/2), r=r, fill='black',
                    stroke_width=lw, stroke='black',
                )
                symbol.add(t_pole)
            t_lead = schematic.line(
                start=ot, end=(gap/2, -sep/2),
                stroke_width=lw, stroke='black',
            )
            symbol.add(t_lead)
            if dots:
                b_pole = schematic.circle(
                    (gap/2, sep/2), r=r, fill='black',
                    stroke_width=lw, stroke='black',
                )
                symbol.add(b_pole)
            b_lead = schematic.line(
                start=ob, end=(gap/2, sep/2),
                stroke_width=lw, stroke='black',
            )
            symbol.add(b_lead)
        else:
            if dots:
                r_pole = schematic.circle(
                    (gap/2, 0), r=r, fill='black',
                    stroke_width=lw, stroke='black',
                )
                symbol.add(r_pole)
            r_lead = schematic.line(
                start=o, end=(gap/2, 0),
                stroke_width=lw, stroke='black',
            )
            symbol.add(r_lead)

        # Orientation and translation {{{2
        # The transformation operations are performed by SVG in reverse order.
        symbol.translate(self.center)
        if '|' in orient:
            symbol.scale(-1, 1)
        if '-' in orient:
            symbol.scale(1, -1)
        if 'v' in orient:
            symbol.rotate(-90)

        # Text {{{2
        if 'v' in orient:
            if '|' in orient:
                hjust = 'r'
                nudge = -nudge
            else:
                hjust = 'l'
            offset = gap/2+r if '-' in orient else -gap/2-r
            if value:
                dy = offset+nudge
                self.add_text(value, shift(self.center, nudge, -dy), 'u'+hjust)
                just = 'l'+hjust
            else:
                dy = 0
                just = 'm'+hjust
            if name:
                self.add_text(name, shift(self.center, nudge, -dy), just)
        else:
            if '-' in orient:
                vjust = 'l'
                nudge = -nudge
            else:
                vjust = 'u'
            if value:
                dx = gap/2+r+nudge
                self.add_text(value, shift(self.center, dx, nudge), vjust+'l')
                just = vjust + 'r'
            else:
                dx = 0
                just = vjust + 'm'
            if name:
                self.add_text(name, shift(self.center, -dx, nudge), just)
