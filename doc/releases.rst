Releases
--------

**Latest development release**:
    | Version: 1.0.1
    | Released: 2020-07-13

**1.0 (2020-04-16)**:
    - reorganized documentation into a formal manual.

**0.7 (2020-03-02)**:

    Moves almost fully to relative placement of components.

    - add ability to place a component by specifying location of its pins or principle coordinates.
    - add ability to add offsets when placing components.

    *This version is incompatible with previous versions.*

    - location of component must be specified with named argument.
    - ``orientation`` arguments have been renamed to ``orient``.
    - terminal array (``t``) has been removed

    You can upgrade previous schematics to this version by:

    - adding ``C=`` to leading argument of all components.
    - replacing ``orientation`` with ``orient`` in the argument lists of all components.
    - replacing use of ``t`` with the actual names of the pins.


**0.6 (2019-09-03)**:
