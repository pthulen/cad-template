# CLAUDE.md

One repo = one 3D-printable product, possibly with several size variants.
Python CAD with build123d, managed by uv. See README.md for commands.

## Layout

- `design/params.py`: `Params` dataclass, every customer-facing dimension.
- `design/model.py`: `build(params) -> dict[part name, Part]`, one entry per printed part.
- `design/printer.py`: measured printer constants (tolerances, bed size, inserts).
- `design/features.py`: reusable printer-aware helpers (holes, pockets, chamfers, labels).
- `variants.yaml`: named variants overriding `Params` fields.
- `scripts/export.py`: writes `exports/<variant>/<part>.{step,stl,3mf}` and SVG previews.
- `notes/`: Obsidian-friendly markdown (YAML frontmatter, no HTML).

## Conventions

- Units are millimetres everywhere.
- +Z is up, and every part is built in the orientation it will print in
  (largest flat face on the bed, sitting on z=0).
- All tolerances and fit gaps come from `design/printer.py`; never hard-code
  clearances in `model.py`.
- Every dimension a customer might want changed lives in `params.py`, not inline.
  New thickness params that must be printable go in `Params.wall_checks()`.
- Prefer build123d algebra mode for simple parts and builder mode when selectors
  make it clearer; be consistent within a file. (`model.py` currently uses algebra mode.)
- Labels use the committed font via `features.embossed_label`, never system fonts,
  so geometry is identical on macOS and CI.
- Dependencies are pinned in `uv.lock`; add them with `uv add`, never pip.

## After changing geometry

1. `uv run pytest`
2. `uv run python scripts/export.py`
3. Tell the user to check it in OCP CAD Viewer (run `design/model.py`).

## Working with the user

The user is a JS/Node developer learning Python and CAD.

- When asked for help, explain the approach before writing code.
- Don't silently rewrite whole models; make focused changes and say what changed.
- Explain any non-obvious Python or CAD idiom in a comment.
