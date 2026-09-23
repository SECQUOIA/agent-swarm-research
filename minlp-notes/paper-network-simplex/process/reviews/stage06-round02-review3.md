# Stage 6, round 2 — independent reviewer 3

**Verdict: no major issues; one new minor implementation regression.** The
missing fixed-weight baseline control is now implemented correctly for the
nonempty-arc networks used in the study, and the revised practical conclusions
follow from the corrected data. All four accepted round-1 minor issues are
resolved. The remaining finding concerns the new branch on an empty arc set;
it does not affect any reported measurement or mathematical result.

I reviewed the complete corrected frozen stage at
`process/snapshots/stage06-round02`, the changed baseline and tests, the
measurement and table generators, and their interfaces with the exact and
compressed implementations. I read the requested round-1 adjudication,
correction record, correction validation and updated validation manifest.
I did not consult another round-2 report, coordinate findings, or edit shared
manuscript/code/data. All new evidence is confined to
`verification/reviewer3/stage06-round02/`.

## Finding

### S06-R2-R3-01 — Minor: fixed-weight optimization now fails on a valid empty-arc graph

**Location:** `code/network_simplex_benchmarks/strong_baselines.py:73–77`,
the unconditional `linprog` call in the new fixed-weight branch.

If `E=0`, the substituted model has zero flow variables. SciPy rejects its empty
objective vector before checking feasibility. This is a regression from the
archived round-1 fixed-weight implementation for `m>0`, which still had the
fixed simplex columns. The public `Instance` representation does not exclude
an empty arc set, and such a network is also within the manuscript's bounded
equality-flow setting.

Concrete valid instance:

```python
instance = Instance([], np.zeros(1), 2, [], np.zeros(0))
result = optimize_ef(instance, [1, 2],
                     y_fixed=[Fraction(1, 3)] * 2, merge=False)
```

There are no flow or product coordinates, the zero balance is satisfied, and
this fixed-weight problem has the unique original point `(1/3,1/3)` and objective
`1`. Both `merge=False` and `merge=True` instead raise `ValueError` from
`linprog`. The archived round-1 implementation returns status 0, objective 1,
and the correct original point in both cases.

I reproduced this against both actual versions, loading the old implementation
under a private module name. See `check_empty_graph.py` and `empty-graph.json`.

**Required correction:** handle the zero-column fixed-weight model directly:
check its balance right-hand sides and substituted constant inequalities,
then return the appropriate feasible/infeasible status, constant objective and
original-point reconstruction, with consistent timing/model metadata. Include
a focused empty-arc test covering a feasible instance and an inconsistent
balance or fixed-y-only row. Explicitly rejecting empty networks would need
to be documented as an API restriction, but preserving the former valid case
is the simpler correction.

**Severity:** minor. This is a local degenerate-input regression in the
benchmark interface, not a false formulation or a failure on the measured
instances. It does not alter the revised performance interpretation.

## Assessment of the major correction

The new fixed-weight branch implements the direct disaggregation

`A f^j = lambda_j b`, `0 <= f^j <= lambda_j u`

with positive state flows only and native variable bounds. It does not retain
fixed y columns or variable-weight capacity rows. Grouping globally unobserved
labels before deleting zero groups is valid: their normalized flow domain and
all observed product contributions coincide, while their individual fixed y
values are retained in objective constants and row constants.

For any original row with coefficients `(a_x,a_y,a_z)`, the branch creates the
state-flow coefficient `a_x` in every retained state, adds `a_z` in the
corresponding observed state, and moves `a_y * y_fixed` to the right-hand side.
An observed zero-weight state has identically zero products, so dropping its
flow block and its product coefficients is correct. The objective mapping
uses the same substitutions and restores the fixed y objective constant.
Original-point reconstruction includes every original y and every observed z,
including zeros in omitted states.

This joint LP remains valid with mixed x/y/z side rows and with the aggregate
budget. Independent state optimization is separately identified as applying
only without coupling. The free-weight branch retains the original y
variables and semantics. Solver failures remain distinct from infeasibility.
All of these arguments apply to arbitrary directed incidence matrices; they
do not require the benchmark block structure.

I tested the new branch against directly enumerated original hull vertices,
not just another state-flow matrix builder. The checks include free and fixed
weights, zero weights, sparse observed labels, nonzero original y costs, and
three dense mixed x/y/z inequalities. The new positive-state model agreed
with those independent formulations. The zero-column issue above is the only
failure found.

## Status of the earlier minor corrections

1. **Printed command:** resolved. The private PDF contains one continuation
   backslash. I extracted its complete command block and passed it to Bash
   with Python replaced by an argument-printing function. Bash produced the
   intended benchmark arguments and the separate table-generator invocation.
   Evidence: `shell-command-check.txt`.
2. **Observation sorting:** resolved. The manuscript now excludes the
   constructor's `O(|O| log |O|)` comparison sorting from its fixed-observed-label
   linear-in-length implementation statement. Tuple-normal overhead remains
   disclosed. The theoretical grouped-input bound is unchanged.
3. **Three-label recovery:** resolved. The text now clearly uses 16 circuits
   for three-label separation and inverse bases for recovery starting at three
   labels. It agrees with `_reduced_bases` and the exact implementation. The
   historical author record is identified as such, and the correction record
   explains the change.
4. **Complete grid and methods:** resolved. The table generator now verifies
   ordered unique flat keys, the three membership counts, optimization names
   and order, method coverage, rotations, expected statuses and timing-summary
   fields before rendering tables. My old duplicate-case probe is rejected.
   Ten independent corruption probes were rejected before any table output:
   duplicate flat case; missing membership case; wrong membership label count;
   wrong optimization order; missing warmup, run or summary method; wrong
   rotation; wrong status; and corrupt timing median. Evidence:
   `check_controls.py`, `control-checks.json`, and `mutations/`.

## Data, provenance and fairness audit

- Independently recomputed **all 100 current manifest hashes** and **all 83
  archived hashes**. Every value matched. The archive genuinely retains the
  old data and measured sources; it was not overwritten by the correction.
- Verified exact JSON equality of the old and new `flat`, `membership` and
  `cold` records. Every original optimization objective vector, fixed weight,
  extra row, case identity and dimension is unchanged; optimum values agree
  within the stated numerical tolerance. The revision's archived-data SHA256
  matches the actual source JSON.
- Compared the actual function ASTs for `membership_ef`,
  `optimize_independent_states`, `_finish` and `_rational`: they are unchanged
  from the archive. The exact flat-chain source is byte-identical as well.
  All seven accepted mathematical section files are byte-identical to round 1.
- Independently checked **515 timed method records**, rotations, statuses,
  component/total consistency, model sizes and optimization objective agreement.
  Recomputed **all 483 timing-summary fields** from raw records. All matched.
- Generated all five tables in a private copy. They are byte-identical to the
  corrected snapshot. Current full optimization sizes are `(m+1)E=5547` on the
  sparse/budget instances and `65*111=7215` on the all-labels-observed instance.
  Global merging gives `12*43=516` for the first two and the same 7215 for the
  last. The unchanged compressed counts, 255/222 and 495/367, remain correct.
  Sparse input row/nonzero counts correctly exclude native variable bounds;
  for example the full sparse case has `129*28=3612` balance rows and
  `129*86=11094` matrix entries, versus 336/1032 after global merging.
- Independently reran **all three optimization cases and all 16 case/method
  combinations**, each with a fresh audited warmup and one timed repetition,
  using the saved objective vectors, weights and rows. Statuses, model sizes,
  objectives and cut counts matched the corrected records. This also reruns
  the generator's exact reconstructed-flow and budget checks and numerical
  cut-support audits. My one-repeat timings are retained only as reproduction
  evidence, not substituted into the manuscript or used to infer speed.
- The official rerun performs five rotated repetitions for every method in
  each optimization case. It neither mixes old and new methods within a
  comparison nor substitutes a reviewer's timings. The manuscript and README
  disclose that membership and cold-library records come from the earlier run.
  Audit costs are outside timed work; total times include the work described
  in the table captions. No host isolation or warm-start advantage is implied.

Evidence: `check_data.py`, `data-checks.json`, the private `build/`,
`reproduce_optimization.py`, `reproduced-optimization.json` and its log.

## Revised interpretation and whole-stage integration

The updated sparse-case comparison is appropriately weaker: global merging
has lower median total time (4.25 ms) than initial compression (4.82 ms),
with overlapping ranges. In the budget control the corresponding medians are
4.33 and 5.84 ms. These claims match the raw values. The all-labels-observed
control still distinguishes local graph compression from global missing-label
removal: full/global both retain 7215 flow variables and have roughly 30 ms
medians, versus 10.16 ms for initial compression with 495 variables.

The manuscript does not treat size reduction as a universal speed guarantee.
Observed elimination is smaller but slower in these records; repeated cuts
are slower than the joint LPs; and the strengthened boundary-face membership
baseline defeats the earlier long-chain timing interpretation. Unchanged
interior timing ranges and exact-versus-numerical output distinctions remain
accurately reported. Fixed-y independent-network optimization is acknowledged
as elementary, with its multiple-call overhead measured separately.

The complete computation section still agrees with the accepted mathematics:
the canonical flat-chain input restriction, three-label coefficient guarantee,
compact default recovery, numerical general compressed membership, explicit
Farkas certificate statuses, and bounded-rank prototype limitation are clear.
The two-supplier interpretation has the required parallel-path underlying
graph and opposite signs on the two supplier arcs of a path. The common domain
assumptions and the limitation of intersecting the component hull with an
outer budget are maintained. No industrial validation, persistent-callback
advantage, exact numerical optimality, or new general separation theorem is
claimed. The main file and unchanged bibliography introduce no new conflict;
the SciPy and HiGHS citations retain the metadata checked against their
primary project citation pages in round 1.

## Tests and build actually performed

- Combined supplied suite: **22 tests passed**.
- Independent vertex checker rerun against the changed code: **100 models**,
  **800 membership comparisons**, **540 optimization comparisons**,
  **125 exact decompositions**, and **3,227 exact cut evaluations at hull
  vertices**. All passed. This includes both decomposition-inclusive and
  membership-only exact queries and up to four observed labels.
- New empty-arc regression probe: both full and merged fixed-weight branches
  raise, while both archived versions return the expected objective and point.
- Ten private table corruption probes rejected before output; valid tables
  regenerate identically.
- Private LaTeX build: **45 pages**, no warnings, overfull/underfull boxes,
  undefined citations or references. The PDF command was separately parsed
  by Bash as described above.

## Limits and disposition

Numerical agreement with explicit vertex hulls is not a proof of exact LP
optimality. Exact flow and cut checks establish the specific witnesses and
small-instance certificates tested; the manuscript's proofs supply the general
guarantees. I did not remeasure industrial instances, repeat all unchanged
historical audits, or independently re-prove every unchanged earlier section.
I verified their identities and relevant interfaces and reran the changed-code
and complete optimization checks most directly affected by this correction.
No speed inference is drawn from my one-repeat reproduction.

**Disposition:** the major fixed-weight-control finding and all four prior
minors are resolved. Correct S06-R2-R3-01 before closing the stage. This review
identifies no major issue requiring another five-reviewer cycle.
