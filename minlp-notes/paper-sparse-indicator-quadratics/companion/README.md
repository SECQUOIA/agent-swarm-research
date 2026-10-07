# Companion material removed from the manuscript

These sections were appendices of the sparse indicator quadratics manuscript
until 2026-09-30. They were removed so that the paper stays focused on exact
separator messages, the hardness result, and the message-size lower bound.
They are kept here as source for a possible separate note.

- `sections/moments.tex`: all fixed moments of active-support counts, a
  companion affine-rank gap estimate, expected connected-region counts, and an
  exact subdivision labeled with every tied support.
- `sections/geometry.tex`: sharper scalar and planar region bounds under
  continuous perturbations, and a discrepancy transfer to finite grids.
- `sections/recursive.tex`: direct recursive algorithms under strict diagonal
  dominance (block recursion and a fixed-width CAD recursion).
- `checks/check_extensions.py`: exact finite checks for the atomic moment
  tails and discrepancy endpoints.

The sections are not built on their own. They use the manuscript's macros and
refer to its labels (for example `eq:intervalmass`, `lem:count`,
`thm:dictionary`, `thm:main`, and `eq:certificate`), so a standalone note would
need to restate those definitions. Run the checker with:

```sh
python3 -B companion/checks/check_extensions.py
```
