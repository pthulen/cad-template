"""Measured constants for MY printer. All values in millimetres.

Every tolerance and fit gap in the design comes from here, so when you change
printer, nozzle or filament you retune this one file and every model follows.

Values marked TODO are typical starting points, not measurements. Print a
tolerance test (e.g. a peg-in-hole gauge) and replace them with what you measure.
"""

# --- Nozzle and slicing (match your Bambu Studio process settings) ---
NOZZLE = 0.4  # TODO confirm: installed nozzle diameter
LINE_WIDTH = 0.42  # TODO confirm: extrusion line width set in the slicer
LAYER_HEIGHT = 0.2  # TODO confirm: default layer height you print at

# Thinnest wall worth printing: two full perimeters.
MIN_WALL = 2 * LINE_WIDTH

# --- Fits. Gap PER SIDE between two mating printed parts ---
CLEARANCE_SLIP = 0.2  # TODO measure: parts slide together by hand (lids, sliders)
CLEARANCE_PRESS = 0.1  # TODO measure: parts must be pushed in and stay put (magnets, pins)

# Printed holes come out smaller than modelled. This is added to the
# DIAMETER of every round hole made through design/features.py.
HOLE_COMPENSATION = 0.2  # TODO measure: modelled 10.0 hole minus measured hole

# --- Build volume (Bambu Lab P1S and P2S are both 256 x 256 x 256) ---
# P2S figure verified against Bambu's P2S FAQ (wiki.bambulab.com), Oct 2026.
BED_X = 256.0
BED_Y = 256.0
BED_Z = 256.0

# --- Heat-set inserts: modelled hole diameter keyed by thread size ---
# TODO confirm against your inserts' datasheet (these suit common
# CNC Kitchen / Ruthex style inserts). HOLE_COMPENSATION is NOT added to
# these: the insert supplier's figure is already the hole to model.
INSERT_HOLES = {
    "M2": 3.2,
    "M2.5": 3.6,
    "M3": 4.0,
    "M4": 5.6,
    "M5": 6.4,
}
