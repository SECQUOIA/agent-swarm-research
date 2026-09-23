# Stage 6, round 1 — independent review 2

**Verdict: no major issues; accept after two minor corrections.**

Reviewed the frozen Stage 6 manuscript, the author and validation records, the
changed flat-chain implementation, strong baseline builders and tests, and the
benchmark generator. I checked all 82 external artifact hashes before drawing
conclusions. I did not read other current-round reports, coordinate reviewers,
edit manuscript or implementation files, or spawn agents.

## Enumerated findings

1. **R2-S6-01 — minor: the printed reproduction command has two backslashes.**
   At `sections/08-computation.tex:328`, the `verbatim` line ends with two literal
   backslash characters. In a shell, these encode a literal backslash argument;
   they do not continue the command to the next line. The following `--output`
   line consequently becomes a separate command. Replace the pair with one
   backslash, or print the whole command on one line. Because this is verbatim,
   LaTeX escaping is not needed. This is a local reproduction-instruction defect;
   it does not invalidate the already recorded run.
2. **R2-S6-02 — minor: qualify the implementation's linear-time statement by its observation sorting.**
   `sections/08-computation.tex:45–47` says the implemented cost remains linear
   in chain length at fixed observed-label count. However,
   `code/network_simplex/flat_chain.py:207–210` forms
   `tuple(sorted(set(valid)))`, costing up to `O(|O| log |O|)` comparisons. At
   fixed observed-label count, `|O|` can still grow linearly with chain length.
   The implementation README already states this sorting cost. Qualify the
   manuscript sentence with “apart from observation sorting,” and state the
   sorting bound or refer to that proviso. The row construction and online
   queries do have the claimed fixed-parameter linear behavior. This is a local
   complexity qualification, not a defect in the mathematical theorem or a need
   to change the implementation or rerun benchmarks.
3. **No major findings.** I found the new baseline algebra, global state merging,
   fixed-weight factorization, coupled-row mapping, and implemented reduced
   profile oracle correct in their stated domains. The revised performance
   interpretation is supported by the recorded data and appropriately qualified.

## Baseline algebra and implementation

In `strong_baselines.py:32–87`, the state-weight matrix W retains a separate
column for every original simplex coordinate while only observed labels enter
its active-state rows. The default has weight one minus the sum of observed
weights. Together with the original simplex constraint, this is exactly global
state merging. Unobserved original y coefficients are retained in the objective
and in every additional row; they are not silently assigned the default label's
objective. Substituting each original x as the sum of all grouped state flows,
and each observed z as its own observed-state flow, gives the correct objective
and additional-row mappings. The aggregate flow balances follow because all
state weights sum to one.

The fixed-y independent-state builder uses cost `c_x+c^j` for each observed
label and `c_x` for the merged unobserved state. It scales each optimized network
flow by that state's weight and adds every original y objective through the
reconstructed original point. This verifies equation (independent-network-
objectives), including nonzero costs on unobserved y coordinates and zero-weight
states. Additional coupling rows correctly disable this shortcut in the
benchmark driver.

For point membership, exact input arithmetic checks the simplex, bounds, and
zero weights. The aggregate balance test is explicitly numerical. A single
positive grouped state is checked directly; zero observed states were already
forced to zero. With two positive states, the bounds
`max(0,x-mu*u) <= f <= min(lambda*u,x)` correctly encode both state capacities.
Second-state observations become `f_e=x_e-z_e`, and conflicting first/second
observations are intersected on the same interval. Its balance follows from
the aggregate balance, with the numerical tolerance caveat clearly disclosed.
For more states, block balance, aggregate, and active-observation rows are
assembled with correct ordering. Removing a state only when its rational weight
is exactly zero is appropriate.

The code distinguishes statuses 0 and 2 from failures and does not present a
numerical feasibility answer as an exact membership certificate. Its exact
prechecks do not change that distinction. I found no sign inconsistency in the
outgoing-minus-incoming baseline convention or its adapters to the production
incoming-minus-outgoing models.

## Flat-chain implementation

The constructor merges only globally unobserved labels. Local gadget categories
are then formed within that global list, with one unobserved default column.
The residual substitution, two endpoint rows, and bypass observation equations
match Section 7. Zero normals receive a separate scalar check.

The explicit one- and two-label branches avoid all library construction. The
three-label repair selects a gadget whose a-flow coefficient has the sign
required by the proved exceptional circuit; in those cases the selected
endpoint rows come from distinct gadgets, so subtracting the appropriate flow
balance preserves every unit coefficient. Larger cases use all full-rank bases
of the reduced normal list and do not incorrectly anchor the explicit profile
sum to the total branch flow.

Recovery reconstructs grouped weighted flows and stores their shared default.
A normalized original-state `flow(j)` divides by the corresponding group weight;
for an unused label this gives the common normalized default flow. The weighted
compatibility accessors apply the original weight/group-weight ratio. A positive
original weight cannot belong to a zero-weight group. The no-observation branch
returns the aggregate flow as the common default and retains all global weights.
These interfaces agree with the accepted observed-label merger.

## Benchmark and manuscript assessment

I checked the benchmark generator's method dispatch, state counts, complete
flat case grid, two-positive-state control, all-labels-observed control, coupled
budget mapping, and original-coordinate reconstruction audits. Each measured
case has a warmup and five rotated runs. Exact certificate audits occur outside
the measured components. Recovery-inclusive exact queries are separately timed
rather than inferred from membership-only times. The cut-support checks in
optimization are numerical and are labeled as such.

The budget is built from the exact reconstructed unconstrained point and a
feasible reference. The driver supplies the same row to every joint formulation
and checks it again on the reconstructed output. The paper correctly describes
this as intersecting the component hull with a budget, not convexifying the
budget-constrained graph exactly.

The table conclusions accurately acknowledge the strong baselines: global
merging explains much of the many-label improvement, simple LPs beat the exact
flat oracle on the large boundary cases, and there is no universal runtime
ordering. The all-labels-observed comparison isolates local graph compression
from the global merger. Matrix byte counts are not represented as process peak
memory. The two-supplier interpretation is valid because its underlying graph
is a set of parallel length-two paths with reversed traversal on the second
supplier's arcs; it is clearly a modeling illustration rather than empirical
industrial validation.

## Independent checks actually performed

1. Wrote and ran
   `verification/reviewer2/stage06-round01/check_baselines.py`. Its reference
   formulation uses convex combinations of explicitly enumerated graph points:
   every integer feasible flow on a small integral network paired with every
   simplex vertex. It does not use a disaggregation-row builder. The flow
   polytope is generated by these integer points because the incidence system
   is integral. Across 12 independently generated networks with loops,
   parallel arcs, and an isolated vertex, comparisons covered:
   - 96 optimization results against full/global strong baselines, with free
     and fixed y, nonzero costs on every original coordinate, and three dense
     coupled x/y/z rows where applicable;
   - 12 independent-state fixed-y objectives;
   - 384 membership results covering global merging, both two-state settings,
     zero states, globally unused labels, and perturbed observations.
   All passed. These LP classifications and objective comparisons are numerical,
   with objective tolerance `1e-7`. Results: `baseline-result.json`.
2. Reran the complete combined unit command:

   ```sh
   PYTHONPATH=code /home/sgusev/miniconda3/envs/minlp-notes/bin/python -m unittest network_simplex.test_separator network_simplex.test_flat_chain network_simplex_benchmarks.test_strong_baselines -v
   ```

   All 21 tests passed. This includes exact cut/decomposition checks, the new
   inverse-basis regression, both three-label repairs, and failure-status tests.
3. Independently recomputed 483 stored timing summaries from the raw run records,
   checked expected statuses and the 16/3/3 case counts, and verified all 82
   external hashes. All passed; results are in `data-result.json`.
4. Inspected the literal reproduction-command bytes; the double backslash in
   R2-S6-01 is present in the frozen TeX, not an artifact of tool display.

## Limitations

I did not rerun the full five-repetition benchmark grid, certify numerical LP
optimality exactly, compile a private PDF, or independently retrieve every
software citation. Earlier accepted mathematics was checked where it interfaces
with these algorithms, not re-reviewed in full. The measurements are shared-host
results and support the stated implementation comparison only. The two required
changes are local prose/instruction corrections; no major revision is requested.
