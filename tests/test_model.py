"""Checks every variant in variants.yaml is printable.

pytest finds functions named test_*. @pytest.mark.parametrize runs each test
once per (variant, part), so a failure names exactly which one broke.
"""

import warnings

import pytest
from build123d import Mesher

from design import printer
from design.model import build
from design.params import Params, load_variants

VARIANTS = {"default": Params(), **load_variants()}

# Build every part once up front; geometry is the slow bit.
PARTS = {
    (variant, name): part
    for variant, params in VARIANTS.items()
    for name, part in build(params).items()
}


@pytest.fixture(params=list(PARTS), ids=lambda key: f"{key[0]}-{key[1]}")
def part(request):
    return PARTS[request.param]


def test_variants_file_has_variants():
    assert len(VARIANTS) > 1, "variants.yaml defines no variants"


def test_is_single_valid_solid(part):
    # More than one solid means a feature floats free of the body.
    assert len(part.solids()) == 1
    assert part.is_valid


def test_has_volume(part):
    assert part.volume > 0


def test_fits_on_bed(part):
    size = part.bounding_box().size
    assert size.X <= printer.BED_X
    assert size.Y <= printer.BED_Y
    assert size.Z <= printer.BED_Z


def test_meshes_watertight(part):
    # The slicer gets a triangle mesh (STL/3MF), not the exact CAD shape.
    # Mesher raises if the mesh is invalid and warns if it has holes; the
    # warning is turned into a failure so a leaky mesh is never released.
    with warnings.catch_warnings():
        warnings.filterwarnings("error", message="3mf mesh is not manifold")
        Mesher().add_shape(part)


def test_sits_on_bed(part):
    # Built in print orientation: the lowest point is exactly on z=0.
    assert part.bounding_box().min.Z == pytest.approx(0, abs=1e-6)


@pytest.mark.parametrize("variant", list(VARIANTS))
def test_min_walls(variant):
    for name, thickness in VARIANTS[variant].wall_checks().items():
        assert thickness >= printer.MIN_WALL, (
            f"{name} = {thickness} mm is below the {printer.MIN_WALL} mm minimum wall"
        )
