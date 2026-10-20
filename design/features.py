"""Small reusable features that already account for design/printer.py.

Hole helpers return a *tool* solid: a cylinder whose top sits at z=0 and which
extends DOWN to z=-depth. Move it to the surface you want to cut and subtract:

    part -= Pos(10, 0, top_z) * features.insert_hole("M3", depth=5)
"""

from pathlib import Path

from build123d import *

from design import printer

# Font file committed to the repo so labels come out identical on every
# machine (macOS and the Linux CI runner have different system fonts).
LABEL_FONT = Path(__file__).parent / "fonts" / "AtkinsonHyperlegible-Bold.ttf"

# ISO 273 "medium" clearance hole diameters for metric screws (mm).
SCREW_CLEARANCE = {
    "M2": 2.4,
    "M2.5": 2.9,
    "M3": 3.4,
    "M4": 4.5,
    "M5": 5.5,
}


def _hole(diameter: float, depth: float) -> Part:
    """Cylinder from z=0 down to z=-depth."""
    return Cylinder(diameter / 2, depth, align=(Align.CENTER, Align.CENTER, Align.MAX))


def magnet_pocket(diameter: float, depth: float) -> Part:
    """Pocket for a press-fit disc magnet of the given nominal size."""
    hole_d = diameter + 2 * printer.CLEARANCE_PRESS + printer.HOLE_COMPENSATION
    return _hole(hole_d, depth)


def insert_hole(size: str, depth: float) -> Part:
    """Hole for a heat-set insert, e.g. insert_hole("M3", depth=5)."""
    return _hole(printer.INSERT_HOLES[size], depth)


def clearance_hole(screw: str, depth: float) -> Part:
    """Hole a screw passes through freely, e.g. clearance_hole("M3", depth=10)."""
    return _hole(SCREW_CLEARANCE[screw] + printer.HOLE_COMPENSATION, depth)


def base_chamfer(part: Part, size: float) -> Part:
    """Chamfer every edge of the face sitting on the bed (the lowest Z).

    The first layers get squashed outward ("elephant's foot"); a small chamfer
    hides that and makes the part sit flat and look crisp.
    """
    # group_by(Axis.Z) sorts edges into groups by height; [0] is the lowest.
    bottom_edges = part.edges().group_by(Axis.Z)[0]
    return chamfer(bottom_edges, size)


def embossed_label(text: str, size: float, depth: float | None = None) -> Part:
    """Raised text lying in the XY plane, centred on the origin, rising +Z.

    size is the font size in mm (capitals come out about 0.7 * size tall).
    depth defaults to two perimeter widths, which suits text on a vertical
    wall; for text on a top face, use a multiple of printer.LAYER_HEIGHT.
    Place it with a Plane, e.g. `Plane.XZ * label` puts it on a front face.
    """
    if depth is None:
        depth = 2 * printer.LINE_WIDTH
    return extrude(Text(text, size, font_path=str(LABEL_FONT)), depth)
