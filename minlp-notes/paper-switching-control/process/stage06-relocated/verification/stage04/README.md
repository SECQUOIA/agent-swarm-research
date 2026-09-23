# Stage 4: finite-grid minimax verification

Run from the paper directory (or the root of a relocated copy):

```sh
python verification/stage04/run_checks.py
```

Python 3 and its standard library suffice. Do not use `python -O`: the entry
points in the runner and new checkers reject disabled assertions. Historical
checkers must also be run without `-O`. The runner verifies every bundled original
artifact against `verification/reference/origin-manifest.json`, runs the four
exact checks, writes local logs, and writes `check-summary.json`. Frozen snapshots
exclude logs; the summary and all inputs needed to regenerate the checks are
included. Run log-writing commands on a copy of an immutable snapshot.

- `check_finite_formula.py` reconstructs 172 rational extremizers and evaluates
  every one-switch schedule using the original absolute discrepancy. It also
  checks scaling, all three-mode residues through 12 cells, the five-mode
  nine-cell example, the failed nonuniform simplification, and extreme rational
  inputs. These checks supplement the analytic formula and elimination proof.
- `check_floor_chambers.py` directly generates the mathematically characterized
  floor transitions, checks their incoming/outgoing edges, and computes minimum
  switch counts with the nine-entry recursion. It enumerates every history
  through seven cells. It verifies that the only six exceptional seven-cell
  histories are exactly the mode permutations of the printed history, and
  checks the three repair words coordinate by coordinate. It also enumerates
  all 2187 seven-cell words to verify the exact 4/3 instance optimum and the
  104 feasible chamber words. These finite checks are dependencies of the
  five-, six-, and seven-cell minimax proofs, together with the manuscript's
  realizability, boundary, and repair arguments.
- The unchanged historical `small_grid_boundary.py` and independently written
  `check_small_grid_review.py` provide separate five-cell coverage checks. The
  latter enumerates all 14,400 candidate floor histories against all 243 words.

The theorem proof does not require numerical optimization. Optional historical
LP audits can be reproduced with installed NumPy and SciPy:

```sh
python verification/stage04/run_checks.py --with-lp-audits
```

`check_finite_math_review.py` independently assembles full-control LPs retaining
all modes and cells. `check_finite_grid_review.py --skip-milp` includes 99
additional formula-versus-rational-certified-LP comparisons, compressed
extremizer checks, and input validation. Floating-point solutions are only
certificate discovery aids; every accepted compressed LP bound is checked as a
rational primal/dual certificate. The separately assembled full-control LP
comparison is numerical corroboration. Certificate discovery may fail if
rational reconstruction fails; it is not a complete exact LP solver. The direct
closed formula has no such numerical dependency.

`source-record.md` records the primary-source locators and downloaded PDF hash.
The publisher PDF is not redistributed.
