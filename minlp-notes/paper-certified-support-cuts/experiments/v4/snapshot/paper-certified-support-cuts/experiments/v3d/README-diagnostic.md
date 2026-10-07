# Post hoc diagnostic: the row direction (written 2026-10-03, after campaign v3 Part C)

This directory is a copy of `../v3/` whose snapshot differs in two places.
It is a diagnostic conceived after the Part C results of campaign v3 were
seen, and it is reported separately from the prospective campaigns.

## Why

In Part C of campaign v3 the separator improved the root bound of every
mechanism instance but closed only 8-43% of the root gap, although the
exact support of each block in the direction of its own row equals the
block minimum, and the n cuts t_i >= min D_i together make the root bound
equal to the optimum. Inspection of the recorded cuts showed why:

1. The separator's "single-row" directions set the block-variable
   coefficients a to zero, so they bound only the nonlinear remainder of a
   row, not the row function. The row's affine terms in the block variables
   are eliminated afterwards, which gives a valid but weaker cut. The
   comment in the code says the intent was the exact support of the row.
2. With `max_cuts_per_round = n`, the first blocks in the fixed order take
   up to four cuts each, so later blocks receive no cut in a round, and the
   total cap 4n is reached after four rounds.

## What differs

- `snapshot/research-20261003-convexification/solver/integration.py`
  (`RowSeparator._directions`): for each source side, first the direction
  (a, lambda) = (affine coefficients of the block variables in that side,
  e_j), i.e. the exact support of the whole row, then the original
  remainder-only direction. Nothing else changes; certification, elimination,
  export, row checks and replay are unchanged.
- `v3_worker.py` and `make_jobs.py` (copies in the snapshot): a further mode
  `all-diag-mech-wide` with max_cuts_per_round = 4n, max_cuts = 16n,
  max_support_calls = 40n (other limits as `all-diag-mech`).

Modes in `runs/partC-rowdir`: baseline (rerun, same SCIP), all-diag-mech
(variant code, original diagnostic limits), all-diag-mech-wide (variant code,
wide limits). Same instances, limits and hardware rules as Part C.
Hand tests before the run (not part of the results): n=10 seed 4 and n=40
seed 0 were solved at the root node in mode all-diag-mech-wide.
