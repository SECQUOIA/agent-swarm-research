# Stage 6, round 1 — independent reviewer 4

Snapshot: `process/snapshots/stage06-round01`; external changed implementation
and benchmark files were checked against `verification/stage06-validation.json`.

## Verdict

**No major issues. One minor reproduction-command defect must be fixed.**
The changed flat-chain oracle implements the accepted theorems correctly in
the cases audited, including both three-label coefficient repairs, arbitrary
observations, sparse global labels, and recovery with positive residual profile.
The computational text distinguishes exact certificates from numerical evidence
and reports the strengthened baselines' negative findings appropriately.

## Enumerated findings

1. **R4-S06-01 — Minor: invalid shell continuation in the manuscript.**
   Location: `sections/08-computation.tex`, the `verbatim` block in
   “Reproduction,” first command line. The frozen source has **two literal
   backslashes** after `network_simplex_benchmarks.paper_stage06`. In a verbatim
   block they are printed as two; the shell interprets them as a literal
   backslash argument, not as continuation of the next line. Consequently the
   first command lacks its required `--output` argument and the next line is
   treated as a separate command. Replace the pair with one literal backslash,
   or put the command on one line. The README already uses one correctly.
   This is a one-character documentation repair with no effect on the retained
   data or scientific conclusions.

## Exact oracle and theorem-to-code audit

I read all of `flat_chain.py`, its changed tests and API documentation, and
the implemented-scope and certificate paragraphs of the computation section.

Observation validation rejects malformed, Boolean, fractional, and out-of-range
model indices. Deduplication precedes category construction, so repeated input
pairs do not mistakenly create a doubly observed category. Labels observed
only on the bypass still enter the reduced profile. Original flow bounds,
every gadget balance, every original simplex weight, the simplex sum, and
observed nonnegativity are checked exactly before reduction.

The row builder has the accepted signs: `R_i` subtracts observed `a_i` cells
and adds only singly observed `b_i` cells; its complementary row is `t-R_i`.
Both observed cells impose the same singleton equality, and bypass observations
impose `w_j=lambda_j-z_hj`. The residual profile gives the positive and
negative full normals, not an equality on the explicit coordinates. Zero rows
are checked separately. Minimum-row selection keeps its exact affine source,
so a negative circuit sum produces a valid original-coordinate cut with the
same strict rational violation.

At one observed label the grouped interval lower endpoint is feasible after
the single circuit test. At two labels the five circuits are specified
directly, and recovery is the accepted interval/sum formula; neither library
enumeration routine is needed. At three labels, the possible magnitude-two
bypass coefficient is repaired with a gadget whose `x_a` coefficient has
the matching sign. The sign convention is correct for the code's
`constant + terms <= 0` cuts, which is the negative of the manuscript's
nonnegative circuit certificate. The selected balance cancels `x_a`, creates
one unit `x_b` coefficient, and preserves violation after the flow precheck.
The theorem ensures such a gadget exists for either exception.

`_reduced_bases` enumerates every nonsingular basis of the reduced normal
system. It does not reuse the historical basis helper's full-profile equality.
The recovered residual is `t-sum(explicit profile)`, and every group is checked
against its weight. Greedy gadget filling then produces the required exact
aggregate and observed entries. Zero-weight groups vanish without division.
The compact decomposition normalizes by group weight; each unused positive
original label correctly receives the same normalized default flow. Its dense
compatibility accessors multiply by the original weight and therefore recover
the former weighted-state meaning. The zero-observed-label case returns the
aggregate as the common normalized default.

The implementation's sorting and tuple-normal costs are disclosed instead of
being silently identified with the theorem's bit-mask construction count.
The manuscript correctly limits the bounded-rank code to a verification
prototype and the flat interface to the canonical unit-data topology.

## Baseline and measurement audit

I read `strong_baselines.py`, its tests, and `paper_stage06.py` as well as
the frozen tables, README, author record, and validation manifest.

The optimization builders retain every original `y` variable and its objective
and added-row coefficient. Eliminating `x,z` by state-flow substitution maps
aggregate coefficients to every state and observed-product coefficients only
to the correct observed state. Global merging changes only unused flow copies;
it does not remove unrelated `y` terms. The fixed-weight independent network
baseline has the correct state-specific cost and shares one solve among
globally unobserved labels. The aggregate-budget case correctly disables that
separability and compares the intersection of the hull with the common row.

The membership baseline detects zero weights with exact input arithmetic and
checks their observed values. For two positive states, the interval intersection
is exactly `max(0,x-mu*u) <= f <= min(lambda*u,x)`, with second-state
observations translated to `x-z`. Conflicting observations tighten both sides
and are rejected. For more states the sparse balance, aggregate, and observed
equations have the correct shapes and right-hand sides. Solver statuses other
than 0 and 2 are errors. Its aggregate-balance tolerance, numerical LP answers,
and direct-check semantics are disclosed, so no exact-membership claim is
being inferred from this baseline.

The benchmark timer separates model setup from query/solve work. Exact
membership and decomposition-inclusive calls are separately timed; the latter
is not obtained by subtracting unrelated totals. Warmup audits occur outside
the reported timed components. They verify exact decompositions or exact
flat-path cut maxima, while optimization cut-support checks are explicitly
numerical. Rotated method order and all five raw runs are retained. The text
does not imply that medians of different components add to the median total.

The reported interpretation fits the evidence: global merging explains much
of the original sparse-instance advantage; the all-labels-observed control
exposes additional local compression; the improved boundary-face LP baselines
overturn the earlier flat-chain speedup. The overlapping interior ranges and
shared-host limitation prevent a universal runtime claim. Numerical optimum
comparisons, exact reconstructed component membership, original model size,
sparse-matrix bytes, and peak-memory claims are kept distinct.

## Independent checks actually performed

- Verified all **82 frozen SHA256 entries** against the current external files;
  none differed.
- Independently recomputed **483 timing summaries** from the raw five-run
  records, covering **515 timed method runs in 22 cases**. All stored minima,
  medians, and maxima matched. The result is saved as
  `verification/reviewer4/stage06-round01/data-check.json`.
- Reran the changed flat-oracle and strong-baseline unit suites: **15 tests
  passed**. The log is `target-tests.txt` in the same evidence directory.
- Wrote a fresh independent graph/path audit in `check_oracle.py`, importing
  the production interface under test but no existing repository verifier.
  It generated arbitrary observations, exact convex mixtures, zero weights,
  perturbed observations and aggregate flows, and sparse labels among larger
  original simplex lists. Final results were **157 oracle queries**, including
  **66 exact decompositions** and **91 exact globally valid violated cuts**.
  Cut validity was checked directly on all relevant complete path/simplex
  vertices, totaling **3,693 vertex checks**. Every feasible decomposition was
  checked against original state bounds, balances, aggregate flows, observations,
  and compatibility-array semantics.
- The fresh audit compared **156 decisions** with an independently assembled
  LP over complete path/simplex mixtures. It also made **624 comparisons** with
  the strengthened membership baseline across full/global merging and enabled/
  disabled two-state reduction. All agreed; only LP statuses 0 and 2 were
  accepted as outcomes.
- Explicit fresh cases exercised both three-label repairs, an interior residual
  with three observed labels sparsely numbered among 23 original labels, and
  the four-label ratio-two obstruction after sparse renumbering. A separate
  2,000-label case with only two observed labels succeeded while both parameter
  library accessors were patched to raise if called. The JSON summary is
  `check_oracle.json`.
- Built a private copy of the full frozen manuscript successfully with
  `latexmk`; its final log has no warning, undefined-reference, overfull, or
  underfull matches.

The path LP comparisons are numerical corroboration. The decomposition and
cut-validity checks use exact rational arithmetic and cover the complete finite
vertex set for their tested flat graphs.

## Limitations

I did not rerun the full timing study or independently optimize every reported
objective with an exact rational LP solver. The manuscript makes no exact
optimality claim for those numerical experiments. I inspected the general
compressed-certificate semantics and interface rather than re-auditing its
unchanged implementation line by line. The fresh implementation checks exercise
at most four observed labels; the higher-parameter claim rests on the accepted
finite-circuit proof and the audited general enumeration code. I read no other
current-round reports, edited no manuscript or production source, and spawned
no agents.
