# Stage 6, round 2 — independent review 2

**Verdict: no major issues; one minor implementation regression to correct.**

I reviewed the corrected frozen Stage 6 manuscript and its external artifacts,
read the round-1 adjudication and correction records, and inspected the new
fixed-weight branch. I did not read another round-2 report, coordinate reviewer
judgments, edit shared manuscript/code, or spawn agents.

## Enumerated findings

1. **R2-S6R2-01 — minor: fixed-weight optimization now fails on a valid graph with no arcs.**
   In `code/network_simplex_benchmarks/strong_baselines.py:41–85`, the new
   fixed-weight branch passes an empty objective vector to `linprog` when
   `E=0`. SciPy rejects this input rather than solving the resulting constant
   problem. For example:

   ```python
   instance = Instance([], np.array([0.]), 2, [], np.array([]))
   optimize_ef(instance, [2., 3.],
               y_fixed=[Fraction(1, 3), Fraction(1, 4)], merge=False)
   ```

   The flow domain is the singleton empty flow, the fixed simplex vector is
   feasible, and the optimum is `17/12`. The corrected builder instead raises
   `ValueError: Invalid input for linprog: c must be a 1-D array ...`. The same
   regression occurs with `merge=True`. The archived round-1 builder returns
   status 0 and the correct value in both modes, so this is a regression caused
   by deleting all fixed-y columns, not a pre-existing limitation. The free-y
   branch also continues to support this input.

   Handle the zero-flow-variable case directly, checking the remaining balance
   equations and constant additional rows, preserving the objective constant
   and original-point reconstruction. Include both a feasible constant problem
   and an infeasible constant additional row in the regression check. This is
   **minor** because it is a local degenerate-input repair, the mathematical
   formulation is correct, and none of the recorded benchmark instances has
   zero arcs. No benchmark rerun or new major-review cycle is warranted for
   that repair alone.
2. **No major findings.** The accepted major missing-control issue is resolved.
   The strengthened fixed-y full/global baseline has the required algebra and
   the official optimization cases have been rerun and interpreted accordingly.

## Resolution of previous findings

The printed reproduction command now contains one literal continuation
backslash. The observation-sorting qualifier is explicit and matches the code.
The manuscript correctly distinguishes three-label circuit separation from
inverse-basis recovery starting at three labels. I inspected the strengthened
table guard: it now enforces the intended unique ordered flat keys, membership
label counts, optimization names, expected methods, rotations, statuses, and
stored timing summaries. These corrections resolve the previously accepted
minor issues.

## New fixed-weight baseline: algebra and independent verification

The branch groups globally unobserved labels before deleting exactly zero
weights. Each retained state has its own native bounds `0 <= f <= lambda*u`
and balance block. No aggregate x columns, product columns, fixed y columns,
or variable-weight capacity rows are retained. Original x contributions are
tiled across the state flows, and only active observed products are inserted
into their corresponding flow coordinates.

Fixed original y terms are subtracted from each additional row's right-hand
side and added back to the objective value. Observations whose state weight is
zero contribute zero, including during original-point reconstruction. The
original y vector is returned intact even for globally unused labels. This is
valid for arbitrary coupled x/y/z rows as well as the aggregate budget. It is
one joint LP; no unjustified independent-state minimization is applied with
coupling. The free-y branch retains every original y column and its objective
and row contributions, and remains algebraically unchanged.

The positive-state membership and two-state `f,x-f` reductions are unchanged
and retain the numerical/exact distinctions already reviewed. The revised
baseline does not turn a floating-point LP status or objective into an exact
certificate.

I expanded my independent vertex-mixture test to cover the new fixed-weight
branch with interior weights, zero residual weight, zero observed weights,
one positive globally unused label, and all explicit weights zero. Its
reference LP uses convex combinations of enumerated graph-point columns, not
a disaggregation row builder. It includes free y, nonzero costs on all original
y coordinates, and three dense coupled x/y/z rows. All 240 full/global
optimization comparisons, 48 fixed-y independent-network objective comparisons,
and 384 membership comparisons passed. Numerical objective tolerance was
`1e-7`. The separate zero-arc probe above is the only failure I identified.

## Manuscript and experimental interpretation

The revised description explains native fixed-weight bounds, the y objective
constant, additional-row substitution, positive-state filtering, and preservation
of the free-weight interface. Its model counts now agree with the implementation:
5,547 versus 516 state-flow variables in the sparse full/global comparison,
and 7,215 for both full/global models in the all-labels-observed control.

The interpretation now recognizes global merging's smaller median total time
on both sparse optimization cases, while disclosing the overlapping timing
ranges in the uncoupled sparse case. It retains the local-compression advantage
in the all-labels-observed control and does not claim that the smallest
formulation is necessarily the fastest. The repeated-cut, independent-network,
and observed-elimination negative comparisons remain visible.

The optimization-only rerun has explicit mixed provenance: flat, many-label
membership, and cold-library records are retained unchanged; all methods in
the same three optimization cases receive new warmups and five rotated runs.
Original objective vectors, fixed weights, and coupled rows were preserved.
The text still correctly distinguishes the budget-intersected component hull
from the hull of an additionally constrained graph. The exact oracle and
compressed numerical certificate semantics remain accurately described.

## Checks actually performed

- Ran `verification/reviewer2/stage06-round02/check_baselines.py`, producing
  `baseline-result.json`: 240 optimization comparisons, 48 independent-state
  comparisons, and 384 membership comparisons, all passed. This extends my
  own previous independent reference, with the additional fixed-weight strata.
- Ran `verification/reviewer2/stage06-round02/check_empty_network.py`, producing
  `empty-network-result.json`. It loads the preserved round-1 builder under
  a private module name and reproduces the new zero-arc regression in both
  full and global modes against the archived successful result.
- Reran the full combined test command:

  ```sh
  PYTHONPATH=code /workspace/local-home/miniconda3/envs/minlp-notes/bin/python -m unittest network_simplex.test_separator network_simplex.test_flat_chain network_simplex_benchmarks.test_strong_baselines -q
  ```

  All 22 tests passed.
- Verified all **100** current artifact hashes and independently recomputed
  all **483** timing summaries from raw records.
- Checked byte-for-byte JSON equality of retained flat, membership, and cold
  records against the round-1 archive; checked preservation of all three
  optimization objectives, fixed weights, additional rows, names, and optimum
  values to `1e-7`. Results: `data-result.json`, PASS.
- Reinspected the revised tables, corrected manuscript passages, baseline
  source, and table-validation guard. The unchanged flat oracle remains
  consistent with its accepted mathematical interfaces.

## Limitations

I did not rerun the entire five-repetition benchmark grid, independently prove
numerical optimality, or compile a private PDF. The vertex-combination checks
are numerical LP comparisons built on exact combinatorial flow enumeration;
they do not certify floating-point optimizers exactly. The zero-arc issue is
outside the measured workload and can be corrected locally without changing
its scientific interpretation. All other retained conclusions from my full
round-1 review remain unchanged.
