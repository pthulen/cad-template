"""Every dimension a customer might want changed, with sensible defaults.

variants.yaml overrides these per size variant; anything a variant doesn't
mention keeps the default below. All lengths are millimetres.
"""

from dataclasses import dataclass, fields, replace
from pathlib import Path

import yaml

VARIANTS_FILE = Path(__file__).parent.parent / "variants.yaml"


# frozen=True makes instances read-only, so a build can't accidentally
# mutate the parameters it was given.
@dataclass(frozen=True)
class Params:
    inner_width: float = 60.0  # mm, usable space inside along X
    inner_depth: float = 40.0  # mm, usable space inside along Y
    inner_height: float = 25.0  # mm, floor to rim, inside
    wall: float = 2.0  # mm, side wall thickness
    floor: float = 1.6  # mm, base floor thickness (8 layers at 0.2)
    lid_thickness: float = 1.6  # mm, lid top plate
    lid_lip_height: float = 5.0  # mm, how far the lid's plug reaches into the box
    lid_lip_wall: float = 1.2  # mm, thickness of the plug's rim
    chamfer: float = 0.4  # mm, chamfer on edges touching the bed
    label: str = "BOX"  # text embossed on the front wall; "" for none
    label_size: float = 8.0  # mm, font size of the label

    def wall_checks(self) -> dict[str, float]:
        """Thicknesses that must be at least printer.MIN_WALL (checked by tests)."""
        return {
            "wall": self.wall,
            "floor": self.floor,
            "lid_thickness": self.lid_thickness,
            "lid_lip_wall": self.lid_lip_wall,
        }


def load_variants(path: Path = VARIANTS_FILE) -> dict[str, Params]:
    """Read variants.yaml into {variant name: Params}."""
    data = yaml.safe_load(path.read_text()) or {}
    allowed = {f.name for f in fields(Params)}
    variants = {}
    for name, overrides in data.items():
        overrides = overrides or {}
        unknown = set(overrides) - allowed
        if unknown:
            raise ValueError(f"variants.yaml: {name!r} has unknown params {sorted(unknown)}")
        variants[name] = replace(Params(), **overrides)
    return variants
