# Independent review of the completion report

The added mathematical arguments and implementation claims were checked
against their companion proofs, current source contracts, and saved evidence.
No unresolved mathematical or scope issue was found in the reviewed material.
This is a research-agent review, not journal peer review or a publication
priority assessment.

## Mathematical review

- The candidate-denominator acceptance rule uses the actual feasible value's
  reduced denominator, not an unjustified denominator bound on every feasible
  objective. The strict separation threshold is correct.
- The finite exact-recovery proof for nonunique mixed-box QPs correctly
  extends the original height bound to nonprincipal stationary minors. A
  common vertex denominator bounds the sum of selected endpoint slacks.
  The slack minimum then proves that all extra endpoint snaps can hold
  simultaneously. The selected stationary system has constant optimal
  objective even when singular. Compactness and unconditional refinement
  give finite sufficient resource limits, without an efficient complexity
  bound for arbitrary unknown optimal sets.
- The piecewise recourse proof controls both within-piece curvature and
  downward derivative jumps. It includes local partition and KKT witness
  encoding in its input size, preserves factor scopes, and does not assume
  that a short multidimensional partition can be constructed efficiently.
  Exact output uses the original rational QP's height bound.
- The nonunique TU extension preserves feasible corner rounding on unions
  of cells. Its bound for at most `r` optimal values in each continuous
  coordinate is distinct from exact termination for optimal continua.
  The report retains the width-dependent exponent, initial capacity cost,
  and original-constraint recovery assumptions. Premature stationary
  recovery is guarded by equality with the isolated global optimum value.

Two minor corrections requested during review were applied: direct
evaluation handles the zero-dimensional case before defining `1/(4nR)`,
and the exact wrapper's configurable initial precision is distinguished
from its actual resource-limit options.

## Implementation and scope review

The report and coverage map distinguish these points correctly:

- Rational stationarity and reconstruction generate candidates; only
  original-model feasibility and a valid global exactness test accept them.
- Simplex, convex-QP active-face search, and the mixed submodular
  cutting-plane implementation are exact capped reference methods. They
  are not described as implementations with the theoretical polynomial
  oracle complexity. Cached submodular proof size follows the query budget.
- The convex value-factor checker independently verifies local PSD/KKT
  witnesses but reuses the finite-tree engine. Its implemented private sets
  are boxes. Scalar curvature construction is explicitly capped and
  requires the stated positive-definite, nonfixed input; unsupported blocks
  keep the direct safe bound.
- Affine preprocessing and discovered cores carry checked original-model
  transformations. Partition discovery and decomposition selection are
  heuristics, and elimination fill belongs to the residual width.
- The polynomial boundary output may be an implicit description of an
  irrational optimizer. Weak derivative clamps preserve at least one
  optimizer, not necessarily the whole optimal set. The implemented
  restart search is not assigned the theoretical bit-step dovetail rate.
- General negative-curvature parameterization, width-FPT coupled
  optimization, and efficient discovery of arbitrary unknown optimal sets
  remain open. Finite exact output does not resolve those stronger targets.

## Evidence review

The historical 74-run measurements remain explicitly attached to the
first-release source snapshots. They are not represented as reruns of the
completed implementation.

A separate direct JSON audit of the six new main lanes recomputed:

| Quantity | Count |
| --- | ---: |
| Configurations | 73 |
| Completed certifications, including one infeasibility proof | 61 |
| Valid retained certificate replays | 72 |
| Exact-reference enclosures | 54 |
| Exact values certified | 29 |

The summed solver-plus-checker subprocess time is
47.676004819892114 seconds. Every aggregate row exactly matches its
individual result file, and every reported reference enclosure passes
an exact rational comparison. Partial-bound replay is not counted as
successful completion; the invalid TU input is a refusal, not a proof
of infeasibility. Archived pilots and superseded exploratory runs are
excluded.

The saved topic-level test output reports 158 tests passed in 4.114
seconds. All 35 source hashes in its manifest matched the current files
when checked. This review inspected that output and binding rather than
rerunning the tests. Module-specific independent reviews supply their
additional mathematical and adversarial checks.

The separately frozen extension records add 11 configurations, seven
completed requests, ten valid replays, eight numeric reference enclosures,
and two implicit-optimizer containment checks. Their aggregate entries
match all 11 individual result files. All 21 solver/checker subprocesses
exit successfully, and their summed time is 1.584291205057525 seconds.
One symmetric-quartic boundary search remains inconclusive without an
exact-output certificate; the table-limited, cut-limited, and unsupported
signed-class cases retain checked bounds.

The combined figures are therefore 84 configurations, 82 valid replays,
68 completed requests, 14 checked incomplete or unsupported bounds, and
two outcomes without certificates. The reference checks comprise 62
numeric enclosures and two implicit-patch containments. These totals
agree with `combined-summary.json` and with the final report text.

Direct inspection of the underlying proof records also confirmed the
report's two constrained comparisons, scalar recourse state/query counts,
decomposition widths, and separated solve/replay timings. In particular,
the native-integer polynomial's pre-acceptance gap is exactly `1/24`,
strictly below its coefficient-lattice spacing `1/18`. Its fixed rational
coordinate is included before the lattice denominator is computed.
The report distinguishes designed structural fixtures from unplanted
random cases, numerical enclosures from implicit optimizer descriptions,
and public metadata screening from executed solver runs. It makes no
competitive-performance claim from these bounded diagnostics.

## Checks performed

This review used targeted file reads, source/API comparisons, direct
Python JSON/rational aggregate checks, and SHA-256 manifest comparisons.
It did not rerun solver experiments, duplicate module test suites, run
project-wide verification, or inspect CI status or logs. Report compilation,
link resolution, and PDF rendering are recorded by the report owner in
[VERIFICATION.md](../VERIFICATION.md).
