# cad-template

Template for one 3D-printable product designed in Python with
[build123d](https://build123d.readthedocs.io/). The example design is a box with
a friction-fit lid in two size variants.

## Quickstart

```sh
brew install uv            # once per machine, if `uv --version` fails
uv sync                    # creates .venv with the pinned Python 3.14 and all dependencies
uv run pytest              # checks every variant builds and fits the printer
uv run python scripts/export.py   # writes exports/<variant>/...
```

`uv sync` is the equivalent of `npm ci`: it reads `uv.lock` and installs exactly
those versions. uv downloads its own Python, so Homebrew's Python is not used.

## View the model in VS Code

1. Open the folder in VS Code and install the recommended extensions
   (Python and OCP CAD Viewer). VS Code will prompt you.
2. **Make sure the interpreter is `.venv`.** `.vscode/settings.json` already
   points at `.venv/bin/python`. If the status bar shows a Homebrew Python, run
   *Python: Select Interpreter* and choose `./.venv/bin/python`. Otherwise OCP
   CAD Viewer can't find build123d.
3. Open the OCP CAD Viewer panel (its icon in the sidebar), then open
   `design/model.py` and run it (the ▶ button, or `uv run python design/model.py`).
   The default box appears with its lid in place.

Edit a number in `design/params.py` and re-run to see it change.

## Where things live

| File | What it's for |
| --- | --- |
| `design/params.py` | Every dimension a customer might change, with defaults |
| `variants.yaml` | Named sizes that override those defaults |
| `design/model.py` | The geometry; start here to learn |
| `design/printer.py` | **Your** printer's measured tolerances and bed size |
| `design/features.py` | Helpers: magnet pockets, insert holes, chamfers, labels |
| `scripts/export.py` | Writes STEP (CAD), STL/3MF (slicer) and SVG previews |
| `tests/test_model.py` | Each variant is one valid solid, fits the bed, walls thick enough |
| `slicer/` | Bambu Studio project files |
| `notes/` | Design notes, test-print log, changelog (Obsidian-friendly) |

## Export

```sh
uv run python scripts/export.py                  # every variant
uv run python scripts/export.py --variant small  # one variant
```

Files land in `exports/<variant>/` (ignored by git) and a size/volume summary
is printed. Load the `.3mf` into Bambu Studio.

## Release

Releases are built by GitHub Actions, so the published files always come from
a tested commit.

1. Add a section to `notes/CHANGELOG.md`, e.g. `## [1.0.0] - 2026-11-01`.
2. Commit, then tag and push:

   ```sh
   git tag v1.0.0
   git push origin main v1.0.0
   ```

3. The release workflow runs the tests, exports every variant and creates a
   GitHub Release with files named `<variant>-<part>.<ext>` and the changelog
   section as the notes.

The git tag is the product version; `version` in `pyproject.toml` isn't used.

## Starting a new product from this template

1. On GitHub: **Use this template** → create a repository, then clone it.
2. Rename `name` in `pyproject.toml`, rewrite `design/model.py` and
   `design/params.py`, and update `variants.yaml`.
3. Pick a licence in `LICENSE.md` and fill in `notes/DESIGN.md`.

## Updating dependencies

Versions are pinned so a design rebuilds identically years later. Upgrade on
purpose, then re-run the tests and compare exports:

```sh
uv lock --upgrade && uv sync && uv run pytest
```
