"""The product geometry: a box with a friction-fit lid.

build(params) returns {part name: Part}, one entry per separately printed
part, each already in its print orientation and sitting on z=0 (the bed).

Run this file directly (VS Code "Run Python File", or
`uv run python design/model.py`) to see the default variant in OCP CAD Viewer.

This file uses build123d's *algebra mode*: shapes are ordinary values that
you combine with operators, a bit like composing immutable objects in JS:
    a + b   union (glue together)
    a - b   subtract (cut b out of a)
    Pos(x, y, z) * shape   a moved copy of shape
"""

from build123d import *

from design import features, printer
from design.params import Params

# Align.MIN on Z means "the shape's bottom sits at z=0"; X and Y stay centred.
ON_BED = (Align.CENTER, Align.CENTER, Align.MIN)


def build_base(p: Params) -> Part:
    outer_w = p.inner_width + 2 * p.wall
    outer_d = p.inner_depth + 2 * p.wall
    outer_h = p.floor + p.inner_height

    # A solid block, then hollow it out from the floor upward. The cavity is
    # 1 mm taller than needed so it pokes out of the top: cutting with exactly
    # coincident faces can leave a paper-thin skin, so CAD users overshoot.
    shell = Box(outer_w, outer_d, outer_h, align=ON_BED)
    cavity = Pos(0, 0, p.floor) * Box(
        p.inner_width, p.inner_depth, p.inner_height + 1, align=ON_BED
    )
    base = shell - cavity

    # Chamfer the bed-side edges BEFORE adding the label, so the helper only
    # sees the simple rectangular bottom face.
    base = features.base_chamfer(base, p.chamfer)

    if p.label:
        # Plane.XZ is a vertical plane facing -Y (the front). offset() pushes
        # it out to the front face; on that plane local "up" is world +Z.
        front_face = Plane.XZ.offset(outer_d / 2)
        label = features.embossed_label(p.label, p.label_size)
        base += front_face * Pos(0, outer_h / 2) * label

    return base


def build_lid(p: Params) -> Part:
    outer_w = p.inner_width + 2 * p.wall
    outer_d = p.inner_depth + 2 * p.wall

    # Printed upside down: the flat top plate on the bed, the plug pointing up.
    plate = Box(outer_w, outer_d, p.lid_thickness, align=ON_BED)

    # The plug is a hollow rim that slides inside the box walls. It is smaller
    # than the opening by the slip clearance on each side; that gap comes from
    # printer.py, never hard-coded here.
    gap = printer.CLEARANCE_SLIP
    plug_w = p.inner_width - 2 * gap
    plug_d = p.inner_depth - 2 * gap
    rim_outer = Box(plug_w, plug_d, p.lid_lip_height, align=ON_BED)
    rim_inner = Box(
        plug_w - 2 * p.lid_lip_wall, plug_d - 2 * p.lid_lip_wall, p.lid_lip_height, align=ON_BED
    )
    rim = rim_outer - rim_inner

    lid = plate + Pos(0, 0, p.lid_thickness) * rim
    return features.base_chamfer(lid, p.chamfer)


def build(p: Params) -> dict[str, Part]:
    """All printed parts for one variant, keyed by file name."""
    if p.lid_lip_height >= p.inner_height:
        raise ValueError("lid_lip_height must be less than inner_height")
    return {"base": build_base(p), "lid": build_lid(p)}


if __name__ == "__main__":
    # Imported here, not at the top, so tests and export don't need the viewer.
    from ocp_vscode import show

    p = Params()
    parts = build(p)

    # For viewing, flip the lid over and sit it on the box as it would be
    # used. Rot(180, 0, 0) turns it upside down about X; Pos lifts it so the
    # plate rests on the rim. (Exports keep the print orientation.)
    rim_top = p.floor + p.inner_height
    lid_closed = Pos(0, 0, rim_top + p.lid_thickness) * Rot(180, 0, 0) * parts["lid"]

    show(parts["base"], lid_closed, names=["base", "lid"], alphas=[1.0, 0.6])
