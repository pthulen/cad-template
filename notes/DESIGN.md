---
title: Design notes
product: Parametric box with friction-fit lid
status: draft
tags: [design, cad]
---

# Design notes

## Problem

What is this product for, and who uses it? One or two sentences.

*Example: a small box with a lid that stays shut in a pocket but opens one-handed.*

## Requirements

- Must hold: ...
- Must fit inside: ...
- Lid stays on when the box is shaken, comes off by hand.
- Prints without supports on a Bambu P1S/P2S.

## Key measurements

Things measured with calipers that the design depends on. Record the tool and
the date so you can trust them later.

| What | Measured (mm) | Notes |
| --- | --- | --- |
| Example: largest item to store, length | 0.0 | calipers, YYYY-MM-DD |

## Decisions

Each decision with the reason, so future you doesn't undo it by accident.

- **Lid is a plug that fits inside the walls**, not a cap over the outside: the
  box keeps a flat outer profile and the fit gap comes from
  `printer.CLEARANCE_SLIP`.
- **Lid printed upside down** (top plate on the bed): flat top face, no supports.
- **Label embossed on the front wall** rather than the lid top: text on the
  bed-side face would need to be engraved, and raised text on a vertical wall
  prints cleanly.
