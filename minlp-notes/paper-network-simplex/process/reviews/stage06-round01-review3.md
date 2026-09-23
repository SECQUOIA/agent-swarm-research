# Stage 6, round 1 — independent reviewer 3

**Verdict: no major issues; two minor issues require correction.** The revised
computational interpretation is supported by the frozen data, and independent
checks found no mathematical or implementation failure in the changed exact
oracle or strengthened formulations. Both findings concern reproducibility,
not the validity of the current measurements or theoretical results.

Reviewed the frozen `process/snapshots/stage06-round01`, including all of
`sections/08-computation.tex`, its five tables, bibliography, main file, README,
and its interfaces with the accepted mathematical sections. Also read the
changed flat-chain implementation, tests and API documentation; strengthened
baseline implementation and tests; measurement generator; table generator;
stage author record; computational baseline plan; and validation manifest.
No other current-round reviews were consulted. No manuscript or production
code was edited. Executable evidence and a private build are under
`verification/reviewer3/stage06-round01/`.

## Findings

### S06-R1-R3-01 — Minor: the printed reproduction command has two continuation backslashes

**Location:** frozen `sections/08-computation.tex:328`, inside `verbatim`.

There are two literal trailing backslashes on the benchmark-command line.
`verbatim` preserves both. In a shell, the first escapes the second; the newline
therefore ends the command instead of continuing it. The benchmark parser
reports that `--output` is missing, and the next line tries to execute a command
named `--output`.

I extracted and executed exactly the first two printed lines with the working
SciPy interpreter on `PATH`. The exit status was 127, with precisely those
errors; see `command-probe.txt`. This did not run or overwrite the benchmark.
The manuscript README has the correct single-backslash form.

**Required correction:** use one literal backslash in the LaTeX verbatim block,
or print the command on one line. Check the resulting PDF command, not just
whether LaTeX builds. This is minor because the generator itself works and the
correct invocation is already available elsewhere.

### S06-R1-R3-02 — Minor: the table generator does not verify the claimed complete case grid

**Locations:** frozen `sections/08-computation.tex:332–333` and
`verification/stage06-tables.py:10–12`, with the corresponding claim in the
stage author record.

The generator checks that the three lists contain 16, 3 and 3 cases and that
stored summaries agree with raw records. It does not check distinct case keys
or equality with the required Cartesian grid of lengths, weight regimes and
feasibility classes. Nor does it check the required membership label counts
or optimization-case identities. Thus its current checks establish list
lengths, not that the full case grid is present.

An isolated probe replaced the final flat case by a duplicate of the first,
leaving 16 cases and every timing summary internally consistent. The generator
returned `PASS` and rendered tables although the 512-gadget interior infeasible
case was missing. See `grid-probe/result.txt`; the deliberately altered input
and generated outputs are retained only in that private probe directory.

**Required correction:** explicitly check unique case keys against the expected
16 flat combinations, membership counts `{16,128,1024}`, and the three intended
optimization identities, preferably also checking the intended method set in
each case. Alternatively narrow the textual verification claim, though the
explicit checks are small and better preserve the intended reproducibility
contract.

This is minor: my independent check confirms that the actual frozen dataset
contains the complete intended grid and that all currently reported numbers
are correct. The issue is the stated scope of the automated guard, not missing
or fabricated experimental evidence.

## Mathematical and implementation assessment

### Exact flat-chain oracle

The implementation correctly groups globally unobserved labels, retaining all
original simplex-domain checks. The residual grouped profile is eliminated,
with the full positive normal and negative full normal representing its two
bounds. Local categories A, B, T and U generate the reduced endpoint system
from the accepted theory. Observed bypass entries fix the appropriate explicit
profile coordinates. Product nonnegativity and zero-normal rows are handled
before circuit separation.

The one- and two-label branches use the correct interval and interval-sum
conditions and direct recovery. The general branch enumerates all independent
normal bases, rather than imposing a false equality on the sum of explicit
profiles. Exact elimination and the boundedness of the profile system justify
vertex recovery even when the feasible set is lower dimensional. The positive
circuit construction uses exact rational nullspaces and primitive integer
multipliers.

I checked the sign of the three-label bypass repair against the manuscript
convention: the code returns the negative weighted right-hand side as a
`<=0` cut and removes `sign * balance(gadget)`. Its search for an incident
`a`-arc coefficient has the sign needed for both exceptional cases. The repair
preserves evaluation after the original flow precheck and preserves validity
on the entire hull. The supplied tests exercise both exceptions with exact
vertex validity. Independent random checks also found only unit flow/product
coefficients whenever at most three labels were observed.

Compact recovery correctly divides a grouped default flow among all unused
original states by their weights. Zero group weight implies all its original
weights vanish, so the normalized-flow interface cannot divide by a zero
default weight. The no-observation case returns the original feasible flow as
the shared default. Dense compatibility accessors appropriately incur dense
output work. Production exact interfaces import no scientific-package solver.
The paper and API documentation disclose tuple-normal and sorting overhead
rather than claiming the uniform bitmask implementation bound.

### Strengthened baselines and coupling

The optimization baseline retains every original `y`, including the original
objective coefficient and all added-row coefficients on globally unobserved
labels. Its sparse weight map represents each observed state separately and
a default of weight one minus their total. Substituting the aggregate sum and
observed state flows in objectives and added rows is correct. The original
simplex inequalities remain, so preserving an arbitrary original-coordinate
row does not invalidate global merging.

For membership, removing exactly zero-weight states and verifying their
observations is correct. With two positive states, intersecting the bounds
for `f` and `x-f`, together with both sets of observations, gives precisely
the stated single network feasibility system. The second balance follows from
the aggregate equation. The numerical aggregate-balance tolerance is disclosed;
these LP answers are not represented as exact certificates. Solver failures
are distinguished from successful numerical infeasibility.

The fixed-weight independent-network objective formula follows directly from
disaggregation and linearity. Unobserved labels have identical costs and can
share a solve. A common aggregate budget couples these independent choices;
the paper correctly treats the budget experiment as the intersection of the
component hull with the added row. It makes no claim that this is automatically
the convex hull of the additionally constrained product graph.

Beyond the supplied tests, my independent checker directly enumerates the
path–simplex hull vertices on small flat graphs. It uses the resulting
convex-combination LP as a separate formulation, and compares full and globally
merged baselines with free and fixed weights, both without added rows and with
three mixed `x/y/z` rows. This checks the coordinate substitutions against a
model that uses neither disaggregated network constraints nor compression.

### Scope and modeling example

The scope table agrees with the inspected interfaces: the bounded-rank code is
identified as a verification prototype; general compressed LP membership is
numerical; the specialized oracles return exact cuts or decompositions.
The inspected Farkas-recovery routine accepts cuts only after nonnegative
multiplier checks, exact auxiliary cancellation, and strictly positive exact
violation. Its four statuses have the meanings described in the paper.

The two-supplier transportation interpretation has the claimed underlying
parallel-path structure. Traversing the second supplier arc in reverse gives
opposite signed changes on the two arcs of each path, exactly as demanded by
demand conservation. The theta specialization with three demand nodes and the
larger-path transportation formulation are correctly within the preceding
results. Common capacities and balances, and the limitation of subsequently
adding outer constraints, are explicit.

## Data, fairness and reproducibility checks

1. **Frozen identities.** Independently recomputed all 82 manifest hashes;
   every value matched. This includes the actual production algorithms,
   historical reference, raw data, manuscript and tables.
2. **Raw records.** Checked all 515 timed method runs, expected statuses,
   rotated method order, timing-component consistency, stable model sizes and
   optimization objective agreement. Independently recomputed all 483 stored
   minimum/median/maximum timing fields. All matched exactly.
3. **Tables.** Ran a private copy of the table generator against a private copy
   of the actual frozen JSON. All five generated table files were byte-identical
   to the frozen manuscript tables. Independently checked the actual complete
   case grid, in addition to the generator's weaker count assertions.
4. **Model counts.** Verified full optimization size `m+(m+1)E` and global size
   `m+(a+1)E` against every optimization record. The sparse case therefore has
   5,675 versus 644 variables; its 207 original coordinates plus 48 initial
   auxiliaries give 255, with 33 eliminated to leave 222. The all-labels control
   has 367 original coordinates plus `16*4*2=128` initial auxiliaries, giving
   495; observation elimination removes all 128. Full/global both give 7,279.
   Flat positive-state counts equal `q(2L+1)` and the two-state reduction has
   `2L+1` variables, including infeasible cases rejected by its flow equations.
5. **Fresh complete-grid execution.** Ran the generator independently with the
   full grid and one repetition, retaining its full warmup and exact/numerical
   audits. All 103 case/method warmups reproduced the original statuses and
   sizes; optimization objectives and cut counts also matched. Original inputs,
   objective vectors, budget row, reference and unconstrained resource values
   matched. This is a reproduction check, not a new timing estimate or evidence
   for additional speed claims.
6. **Budget construction.** The retained exact reference resource value is
   strictly below the budget, which is strictly below the reconstructed
   unconstrained resource value. Every formulation receives that same row.
   The fresh run reproduced it exactly.
7. **Fairness.** Build and solve work is included consistently in total time;
   separator/reconstruction work in the cut loop is separately recorded but
   included in its total. Exact audits and numerical cut-support optimization
   run outside timed components. Recovery-inclusive exact queries are measured
   separately, rather than inferred by subtracting independent times.
   Libraries are warmed explicitly and their cold costs are reported apart
   from the two-label workload, which does not build a library.
8. **Interpretation.** The negative boundary-face result, advantage from global
   label merging, all-labels-observed control, overlap of infeasible interior
   timing ranges, and slower repeated-cut loop are all consistent with the
   raw numbers and tables. No universal speed, industrial performance,
   persistent-solver or exact numerical-optimality claim is made. Input sparse
   matrix byte counts are properly distinguished from peak memory and factors.

Evidence: `check_data.py`, `data-checks.json`, private `build/`,
`reproduced-grid.json`, `reproduced-grid.log`, and `reproduction-check.json`.

## Tests, primary sources and build actually checked

- Reran the specified combined unit suite: **21 tests passed**.
- Independent vertex-based script `check_vertices.py`: **100 models**, including
  zero weights, absent observations, bypass observations, up to four observed
  labels, and sparse observed labels among eight original labels;
  **800 baseline membership comparisons**;
  **540 optimization comparisons**;
  **125 exact decompositions**; and **3,227 exact cut evaluations at hull
  vertices**. All passed. Numerical vertex-hull membership was also compared
  with both decomposition-inclusive and membership-only exact decisions.
- Checked the new bibliography against the official
  [SciPy citation page](https://scipy.org/citing-scipy/) and the
  [HiGHS project citation information](https://highs.dev/). The paper titles,
  authors cited, venues, years, volume/page information and DOIs agree.
  The HiGHS project itself recommends the Huangfu–Hall article used here.
- Private `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` build
  passed: **45 pages**, without warnings, overfull/underfull boxes or undefined
  references. Extracting the PDF text confirms that the doubled backslash in
  finding 01 survives into the printed reproduction instructions.

## Limits and disposition

Finite numerical comparisons do not prove exact LP optimality or general
implementation correctness. Exact cut checks over all enumerated hull vertices
are global validity certificates for those small instances, and exact recovered
flows establish membership for their particular queries. The manuscript's
mathematical arguments remain the basis for the general guarantees.

I did not rerun every historical audit, independently re-prove all unchanged
sections 01–07, or perform a new industrial benchmarking study. I inspected
relevant earlier results and interfaces, reran the new unit suite and complete
benchmark grid, and added independent vertex formulations specifically to test
the changed code. I do not infer performance significance from my single-repeat
reproduction or treat the shared host as isolated.

**Disposition:** resolve S06-R1-R3-01 and S06-R1-R3-02. No further substantive
revision or major-issue review cycle is indicated by this review.
