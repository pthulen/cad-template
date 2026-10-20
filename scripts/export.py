"""Build every variant in variants.yaml and write print/CAD files.

    uv run python scripts/export.py                 # all variants
    uv run python scripts/export.py --variant small # just one

Writes exports/<variant>/<part>.step / .stl / .3mf plus
<part>.front.svg / .top.svg / .iso.svg line-drawing previews.
"""

import argparse
import shutil
from pathlib import Path

from build123d import *

from design.model import build
from design.params import load_variants

EXPORT_DIR = Path(__file__).resolve().parent.parent / "exports"

# Camera positions for the SVG previews: (where the eye is, which way is up).
VIEWS = {
    "front": ((0, -1, 0), (0, 0, 1)),
    "top": ((0, 0, 1), (0, 1, 0)),
    "iso": ((1, -1, 1), (0, 0, 1)),
}

# Fixed STEP timestamp so re-exporting an unchanged design gives
# byte-identical files (otherwise every export looks like a change).
STEP_TIMESTAMP = "2000-01-01T00:00:00"


def export_svg(part: Part, path: Path, direction, up) -> None:
    # Look at the part's centre from far away along `direction`.
    centre = part.bounding_box().center()
    eye = centre + Vector(direction).normalized() * 1000
    visible, hidden = part.project_to_viewport(eye, viewport_up=up, look_at=centre)

    svg = ExportSVG(margin=5)
    svg.add_layer("hidden", line_color="gray", line_type=LineType.ISO_DOT)
    svg.add_layer("visible", line_weight=0.3)
    svg.add_shape(hidden, layer="hidden")
    svg.add_shape(visible, layer="visible")
    svg.write(path)


def export_part(part: Part, out_dir: Path, name: str) -> None:
    export_step(part, out_dir / f"{name}.step", timestamp=STEP_TIMESTAMP)
    export_stl(part, out_dir / f"{name}.stl")

    mesher = Mesher()  # 3MF: the format Bambu Studio prefers
    mesher.add_shape(part, part_number=name)
    mesher.write(out_dir / f"{name}.3mf")

    for view, (direction, up) in VIEWS.items():
        export_svg(part, out_dir / f"{name}.{view}.svg", direction, up)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--variant", help="only export this variant")
    args = parser.parse_args()

    variants = load_variants()
    if args.variant:
        if args.variant not in variants:
            parser.error(f"unknown variant {args.variant!r}; choose from {sorted(variants)}")
        variants = {args.variant: variants[args.variant]}

    rows = []
    for variant, params in variants.items():
        out_dir = EXPORT_DIR / variant
        shutil.rmtree(out_dir, ignore_errors=True)  # no stale files from renamed parts
        out_dir.mkdir(parents=True)
        for name, part in build(params).items():
            export_part(part, out_dir, name)
            size = part.bounding_box().size
            rows.append(
                (
                    variant,
                    name,
                    f"{size.X:.1f} x {size.Y:.1f} x {size.Z:.1f}",
                    f"{part.volume / 1000:.2f}",
                )
            )

    headers = ("variant", "part", "bounding box X x Y x Z (mm)", "volume (cm3)")
    widths = [max(len(str(r[i])) for r in [headers, *rows]) for i in range(len(headers))]
    for row in [headers, tuple("-" * w for w in widths), *rows]:
        print("  ".join(str(cell).ljust(w) for cell, w in zip(row, widths)))
    print(f"\nWrote files to {EXPORT_DIR}")


if __name__ == "__main__":
    main()
