# Protocol: campaign 4 (fixed 2026-10-03, before any campaign-4 run)

Campaign 4 answers the first referee round. It adds comparators and
samples that campaigns 1-3 lacked. Earlier campaigns and the post hoc
row-direction diagnostic (`v3d/README-diagnostic.md`) remain separate
records. Every run below is reported.

## Code

A new snapshot of the campaign-3 code with two additions, both off by
default so that the frozen behaviour is unchanged:

1. `Config.row_directions` (bool, default False): when True, the
   separator first tries, for each source side, the direction whose
   block-variable coefficients equal that side's affine coefficients
   (the exact support of the whole row), then the frozen remainder-only
   direction. This is the post hoc variant of `v3d`.
2. `run_instance(..., scip_params=None)`: SCIP parameters set on the model
   before solving, in every mode alike.

## Modes

| Mode | Separator | Limits | SCIP parameters |
|---|---|---|---|
| baseline | none | - | defaults |
| all, auto | frozen | frozen | defaults |
| all-diag | frozen | campaign-3 all-diag | defaults |
| all-diag-mech | frozen | mechanism (n blocks, 4n cuts, n per callback, 10 callbacks, 20n support calls, 60 s) | defaults |
| frozen-wide | frozen | wide (n blocks, 16n cuts, 4n per callback, 10 callbacks, 40n support calls, 60 s) | defaults |
| rowdir-wide | row_directions | wide | defaults |
| all-diag-rowdir | row_directions | campaign-3 all-diag | defaults |
| baseline-novarlocks | none | - | `constraints/nonlinear/checkvarlocks = 'd'` (no implicit-discreteness presolve) |
| baseline-extra | none | - | SCIP's nonconvex separators that are off by default switched on: edge-concave cuts, intersection cuts for quadratics, interminor cuts, RLT with hidden products |
| *-noaggr | as named | as named | `presolving/donotaggr = TRUE`, `presolving/donotmultaggr = TRUE` |
| gurobi | Gurobi 13.0.3, NonConvex=2, one thread, MIPGap 1e-4 | - | - |

The exact SCIP parameter names and values are recorded in the snapshot and
in every record.

## Parts

- **C2 (path family, the 20 campaign-3 instances).** Root runs (node limit
  1, 120 s) and full runs (300 s) in modes baseline-novarlocks,
  baseline-extra, frozen-wide; full runs in mode gurobi. The analytic
  pair-hull bound (0 on every instance, Theorem 6.2) is reported alongside.
- **C3 (path family, fresh instances).** The mechanism generator of
  `mechanism-protocol.md` with seeds 5-9 for each n in {10, 20, 40, 80}
  (20 new instances, never run before). Root and full runs in modes
  baseline, all-diag-mech, rowdir-wide, baseline-extra; full runs in mode
  gurobi. This is the prospective test of the post hoc finding.
- **B2 (structure sample, the 30 campaign-3 Part-B models, root only).**
  Modes baseline-noaggr, all-noaggr, all-diag-noaggr,
  all-diag-rowdir-noaggr and baseline-extra; node limit 1, 60 s.
- **D (larger structured models).** Pool: cached MINLPLib models with
  more than 120 and at most 1000 variables, not convex by the library
  metadata, with at least one quadratic or polynomial function, OSiL file
  below 2 MB, and not used in campaigns 1-3. Scan: import and discovery as
  in campaign 3 Part S (60 s discovery deadline, 120 s hard limit).
  Qualifying: admitted and at least one block that the frozen `auto` rule
  admits. Screening: baseline, seed 0, 60 s; a model is *hard* if it is
  not solved. Selection: the first 20 hard qualifying models by SHA-256
  of `convexification-hard-v4:` + name (all if fewer). Root runs (node
  limit 1, 120 s): baseline, all, all-diag, all-diag-rowdir,
  baseline-extra. Full runs (300 s, seed 0): baseline, all, auto,
  baseline-extra.
- **S (star oracle scale).** Random constrained stars with k in {10, 100,
  1000, 10000} leaves and 2k center-leaf rows (fixed generator and seeds);
  time of the inherited oracle and of an O((m+k) log(m+k)) reference sweep;
  exact agreement of the two values. No solver involved.

## Metrics and analysis

As in campaign 3: solved counts, shifted geometric means (shift 1 s) and
median per-run time ratios over commonly solved runs, root and final bound
comparisons at relative tolerance 1e-4, root gap closed against the known
optimum (path family) or the best known bound (D), replay of every
recorded cut with tampering controls, and the independent original-model
check of every incumbent (Gurobi incumbents included). For all cut modes
of campaigns 3 and 4, the separator funnel (support calls, certification
outcomes, row-binding rejections by cause, rounding rejections, cuts
added) and the time decomposition (separator callback versus SCIP time
excluding the callback) are reported.

## Execution

At most six single-threaded worker processes; modes of one job run back to
back in rotated order. The host is shared; timings are descriptive.

## Amendment 1 (2026-10-03, before any campaign-4 run)

Two parts are added at the request of the first review round. They were
specified before any campaign-4 run was started.

- **C4 (path family with a binding coupling row).** The 20 instances of
  C3, with the coupling row replaced by `sum_i y_i <= c`, where
  `c = floor(64 * 0.5 * sum_i y_i*) / 64` and `y_i*` is the
  smallest minimizer in y of copy i alone (the midpoint of the closest pair
  of A_i and C_i). The row binds, so the block minima no longer give the
  optimum, and cuts in directions other than the rows are needed.
  Reference values: (i) the optimum, from a convex MIQP reformulation
  (one binary per choice of the nearest points of A_i and C_i) solved by
  Gurobi 13.0.3 with MIPGap 1e-9, one thread; (ii) the best root bound
  that aggregated cuts on the blocks (x_i, y_i, z_i) can give,
  `min sum_i conv(phi_i)(y_i)` subject to the coupling row and
  `0 <= y_i <= 1`, where `phi_i(y) = dist(y, A_i)^2 + dist(y, C_i)^2`
  (the closure of Theorem 4.2 for one row per block), computed by
  bisection on the multiplier of the coupling row with the exact convex
  envelopes of the piecewise quadratic `phi_i`. Root runs (node limit 1,
  120 s) and full runs (300 s) in modes baseline, frozen-wide,
  rowdir-wide and baseline-extra; full runs in mode gurobi. Metrics: root
  gap closed relative to the optimum and relative to bound (ii), solved
  counts, times.
- **U (what certification buys; offline, no solver).** For every recorded
  cut of the MINLPLib parts of campaigns 3 and 4 (A, B, B2, D) and for a
  fixed random sample (seed 0) of 1,000 cuts of the path-family parts, the
  support constant that an uncertified floating-point pipeline would use
  is computed in binary64 for the recorded binary64 direction, in two
  variants: (U1) the minimum over the separator's own sample set; (U2) the
  better of (U1) and SLSQP local minimizations (SciPy, from the three best
  samples, on the block box and affine domain rows). Each is compared
  exactly with the certified support value. A cut is *invalid* if the
  uncertified constant exceeds the certified value, and *materially
  invalid* if the excess exceeds `1e-6 * max(1, |value|)`. For each
  materially invalid cut, the eliminated row with the uncertified constant
  is evaluated at every recorded incumbent of the same model (all of which
  passed the independent primal check); a violation above
  `1e-6 * max(1, ||c||_1)` means the uncertified cut would have removed a
  feasible point. Also reported: the number of exported rows whose
  binary64 coefficients differ from the exact eliminated row, and the
  size of the bound correction.
