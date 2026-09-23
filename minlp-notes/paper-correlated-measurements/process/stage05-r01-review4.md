# Stage 5 independent review 4

Reviewer scope: robust designs, fixed physical grids, separator certificates,
common feasible families and incumbents, normalization, exact arithmetic,
numerical failures, timing, negative findings, and coverage. The frozen
manuscript and supplement were not edited. Missing integrated introduction and
conclusion are the stated Stage 6 work and are not findings here.

## Assessment

No major issue found. One minor implementation-description correction is
needed. The robust and grid/separator comparisons examined support the claims
made in the computational section. The manuscript makes unusually useful
separations between mathematical bounds, exact certificate evaluation,
floating-point search, and diagnostic model validation; it does not hide the
counterexamples to uniform empirical superiority.

## Finding

### R4-M1 — minor: distinguish the nuisance witness grid from the bridge regression grid

`appendices/computational-models.tex:85–87` says separator certificates use
“reference, nuisance-coefficient, feature, score and final-log grids”
`10^8, 10^12, 10^18, 10^8, 10^12`, respectively. The nuisance minimizer matrix
`G` is actually rounded with `nearest`, which uses `reference_grid=10^8`:
`supplement/legacy/certify_latent_separator.py:119–131`. The `10^12`
`coefficient_grid` is used by `IntegerIntervalScores` for local bridge
regression coefficients, not for rounding `G`.

Remedy: say explicitly that the reference matrix and nuisance witness use the
`10^8` grid, bridge regression coefficients use `10^12`, features `10^18`,
scores `10^8`, and final logarithms `10^12`. This is a prose correction only;
the saved certificates and theorem accepting arbitrary rational `G` are valid.
No legacy data or numerical output should be changed.

## Independent checks

I authored and ran `verification/stage05-review4/check.py`, which imports no
historical producer, certifier, or supplement helper. It uses direct SymPy
selected-covariance inverses, exact rational arithmetic, and a separately
implemented atanh logarithm series with an explicit remainder. Its saved
`results.json` records a complete pass in approximately 6.57 seconds on this
run.

- For all three robust certificate records, compared the exact scenario data
  to the numerical proposal's source model, checked cardinality and the
  attributed incumbent, and recomputed the selected covariance information
  determinant for each of the three scenarios. Recomputed all three individual
  reference incumbent determinants for each record as well: 18 direct
  determinant checks in total. Each true log value lies in its saved bound.
- Reconstructed each robust standardized lower endpoint from selected
  scenario lower bounds minus individual optimum upper bounds. Reconstructed
  each standardized upper endpoint from SPD reference matrices, exact
  nonnegative normalized scenario weights, exact tangent constants, the saved
  shared integer price, and individual optimum lower bounds. The three final
  rational intervals match exactly. The shared price itself is not replaced
  with separate scenario prices.
- Independently confirmed exact adjacent-correlation nesting and all shared
  sensitivity rows for the 48-, 96-, and 192-point fixed physical models.
  The displayed correlations `256/625`, `16/25`, `4/5`, the common `1/800`
  variance components, and cardinality 16 are consistent with the records.
- Recomputed all five separator incumbent information determinants directly
  from their selected covariance, independently of the bridge filtering code.
  Recomputed all five anchor prior terms as
  `trace(W G^T K_AA^{-1} G)` and matched their exact saved rational values.
- For the archived `n=48,b=8` separator, formed the full Gaussian conditional
  covariance `D=R-K_:A K_AA^{-1} K_A:` and adjusted sensitivities `F+HG`
  directly. Exhaustively evaluated all 1,530 nonempty local block patterns
  with direct exact covariance inverses. For each block and count, verified
  that the independently computed maximum is bounded by the stored integer
  score; a separate count DP confirms that the full exact support is bounded
  by the saved shared integer price. This checks the actual full count-feasible
  family, including the final unanchored block, without using the certifier's
  innovation recursions or integer interval implementation.
- Inspected robust dense proposal and exchange code: the dense fractional
  search starts uniformly, its own rounding is polished independently, and
  scenario weights are normalized before recomputing top-k support. Numerical
  local-optimum status is attached to a completed neighborhood of the returned
  incumbent. Compared the published fixed-offset scores, continuous gaps,
  reference generation costs, polishing costs, and accounted totals with JSON.
- Checked determinant-root guarantee conversions. The polished 96-point
  exact endpoints imply approximately 97.17378025% worst-scenario efficiency
  and 99.61779895% of the optimal robust efficiency, consistent with the
  manuscript's downward displays. The 48-point relative guarantee is
  approximately 99.71622889%, also consistent.
- Inspected the original fixed-grid and refined-transfer records. Primary
  96/192 memory runs are first-price timeouts with full-selection upper bounds;
  the 96-point L=12 run is separate. Reported numerical gaps and accounted
  pipeline times match. Separator generation, shared heuristic work and exact
  certification are distinguished, and the 192-point b=16 total exceeds 30 s.
- Inspected `process/coverage.md` and the computational appendix. The relevant
  robust nominal/original/polished/dense branches, smaller separator probes,
  nonnested partitions, grid diagnostics and failures have explicit
  dispositions. The theoretical spectral algorithms are not falsely presented
  as the empirical solvers. The new matched hierarchy test uses one full
  feasible family, and its mixture lower bounds are not confused with integer
  incumbent values.

## Scientific framing and limitations of this review

The three robust scenarios are finite and stipulated; the paper does not
claim a guarantee over a continuous parameter region. Exact decimal inputs
are distinguished from validated physical derivatives. Raw fixed-offset
positive fractional values are distinguished from unknown-optimum
standardized discrete values, which cannot exceed zero. The manuscript
compares upper bounds directly when incumbent values differ. It acknowledges
that calendar bounds are tighter on some grids, all large separator rows miss
the .01 target, and block sizes 12 and 16 are not a nested hierarchy.

I inspected the supporting robust and separator theory and the computational
literature framing but did not repeat a full Stage 4 proof review or a new
external novelty search. Stage 5 adds no broad new priority claim. I did not
rerun historical solver timings, which are expressly single shared-machine
observations, or independently enumerate the large b=12/16 supports. The
latter are covered here by exact selected-information/anchor-prior checks,
code inspection, and the independent exhaustive b=8 support calculation;
the full archived certificate replay is an additional distinct validation
layer, not a substitute for these checks.
