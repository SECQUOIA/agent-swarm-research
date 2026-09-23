# Exact block solver for weighted resistance design on a cactus

Date: 2026-09-06. Implementation: [`exact_weighted_cactus.py`](../code/potential_flow_mpd/exact_weighted_cactus.py). Status: implemented with exact arithmetic; both the [independent arithmetic and schema review](review-potential-flow-exact-weighted-cactus-arithmetic.md) and the [optimization audit](review-potential-flow-reopened-joint-weighted.md#implementation-audit-exact-fixed-nomination-block-solver) passed. The algorithm implements the fixed-nomination result in [the joint weighted cactus theorem](../results/potential-flow-joint-weighted-cactus-accuracy-bits.md).

## Scope and result

The solver optimizes independent positive rational resistance intervals on a fixed-nomination cactus supplied as independent cycle and bridge blocks. The objective is a weighted sum of edge potential drops. Optional rational flow intervals filter scenarios. Both maximum and minimum are supported. It returns an **exact optimal rational resistance profile**, separate quadratic encodings for each optimal cycle circulation and objective contribution, and a certified rational interval for their total objective.

The input is already a block decomposition: every cycle has a coherent orientation and flows `x_e=q+ell_e` with supplied rational offsets `ell_e`; bridge flows are fixed. This implementation does not accept a graph and nominations, compute a block decomposition, or verify that an external graph-to-block conversion was correct. It is an exact block solver, not a verifier of the full original-network mapping. Its input arrays can represent any valid fixed-nomination cactus after that conversion.

For a graph with oriented incidence matrix `A`, a gauge-invariant weighted potential objective `c^T pi` can be represented by edge weights `w` with `A w=c`, because `c^T pi=w^T A^T pi`. A rational spanning-tree flow for `c` supplies such weights. Every cycle's offsets arise from a rational particular flow for the fixed balanced nomination. Reorient both the particular flow and objective edge weight when converting an original edge to the coherent cycle orientation. These are instructions for a future graph wrapper, not operations currently performed or validated by this module.

## Usage and exact input format

Run the supplied example from the repository root:

```
python code/potential_flow_mpd/exact_weighted_cactus.py \
  code/potential_flow_mpd/exact_weighted_cactus_example.json --bits 40
```

Only Python's standard library is required. The input object accepts exactly `sense`, `cycles`, and `bridges`, and must explicitly supply at least one of the two block lists. `sense` is `max` by default or `min`. An explicit empty pair of block lists has zero objective. Unknown keys and duplicate JSON keys are rejected. Rationals are JSON integers or strings such as `"3/2"`; floating-point and boolean numbers are rejected.

Each cycle object requires equal-length arrays `offsets`, `weights`, `lower`, and `upper`, of length at least two. The latter two arrays are the resistance bounds, satisfying `0<lower<=upper`. Optional `flow_lower` and `flow_upper` arrays specify rational flow bounds; a null element denotes an absent bound. An omitted or null optional array leaves all its bounds absent. Each bridge object requires rational `flow`, `weight`, `lower`, and `upper`, and accepts optional rational or null `flow_lower` and `flow_upper` scalars.

The public Python functions are `solve_cycle(...)` and `solve_cactus(problem,bits=40)`. A malformed input raises `ValueError` or an ordinary rational-conversion error; a valid infeasible optimization problem returns `None` from `solve_cycle` or `{"status":"infeasible"}` from `solve_cactus`. Later blocks are still validated if an earlier block is infeasible. `bits` must be a nonnegative integer and controls the total objective-interval width `2^-bits`; it does not affect the exact resistance profile.

Each quadratic output object denotes

```
rational + sqrt_coefficient * sqrt(radicand).
```

All three entries are rational strings and the radicand is nonnegative. Rational perfect-square radicands are simplified using integer square roots, without integer factorization. Different block terms retain separate radicands. The result does not construct a common number field and does not claim a polynomial-time exact comparison of the global objective with a rational threshold.

## Finite exact optimization

On each rational circulation interval with fixed edge signs, the one-row resistance LP has a dual threshold among the finitely many edge objective weights. Untied resistance coordinates take a bound, and tied coordinates need only fill one aggregate equality. Their smallest and largest possible conservation sums are quadratic polynomials of circulation. The threshold's objective is also quadratic.

The solver enumerates rational sign and capacity boundaries, roots of the two aggregate-feasibility quadratics, and the rational stationary point of the objective quadratic. Flat objectives require only boundary candidates. Feasibility and objective comparisons are exact. For rational circulation the tied aggregate is filled using rational arithmetic. An irrational circulation candidate is a root of an aggregate-feasibility boundary, so all tied coordinates can take the corresponding resistance endpoints; the result remains rational. Every improving witness is rechecked against all resistance bounds, capacities, the physical cycle equation, and the reconstructed original weighted objective.

Independent cycles optimize separately, and each bridge selects the favorable resistance bound. The solver does not enumerate exponentially many resistance-box vertices. For a cycle with `m` edges there are `O(m)` sign panels, `O(m)` thresholds per panel, and a constant number of candidates per threshold, with `O(m)` exact arithmetic per candidate. This gives polynomial arithmetic and bit complexity, consistent with the fixed-nomination theorem; constants and practical scaling remain an implementation question.

## Exact quadratic arithmetic and value intervals

A local candidate is stored as `a+b sqrt(d)` with rational coefficients. Arithmetic within a candidate expression uses its stored radicand. Adding or multiplying two nonrational expressions with different stored radicands is deliberately unsupported, even if they happen to generate the same field. Comparison supports arbitrary stored radicands.

To compare candidates, their difference is `U+V`, where `U=a+b sqrt(d)` and `V=c sqrt(e)`. The sign of each part is determined by rational squared-magnitude comparisons. When their signs oppose, comparing their magnitudes reduces to the sign of

```
U^2-V^2 = a^2+b^2 d-c^2 e + 2ab sqrt(d),
```

which has only one radical. This avoids constructing degree-four number fields. Each radical also has an exact dyadic interval from integer square roots of scaled rational numerators. The interval precision accounts for the radical coefficient and the number of blocks, so the sum's reported interval has width at most `2^-bits`.

## A necessary interior resistance

The example's first cycle has

```
ell=(0,0,3,0), w=(2,-1,-3,0),
beta_lower=(1,1,1,1), beta_upper=(4,3,4,5).
```

Its exact maximum is `-12`, attained at `q=-1` and `beta=(1,2,1,1)`. This interior resistance is necessary. On the entire physical circulation range `[-3,0]`, threshold `lambda=-1` gives the dual upper bound

```
D(q)=-6(q+1)^2-12 <= -12.
```

Equality fixes `q=-1`, and the strict untied choices fix the first, third, and fourth resistances to one; conservation then fixes the second resistance to two. No resistance-box vertex is optimal. This checks a behavior that endpoint-scenario enumeration would miss.

The second cycle in the example has exact optimum `-15+sqrt(72)` and irrational optimal circulation `-1+sqrt(72)/6`, while its selected resistance profile is rational `(3,1,1)`. The bridge contributes `-9/2`, so the full example has exact total objective `-63/2+sqrt(72)`.

## Verification evidence and limitations

The author check script [`exact_weighted_cactus_checks.py`](../code/potential_flow_mpd/exact_weighted_cactus_checks.py) passed 1,200 independent high-precision quadratic comparisons with exact interval checks, and 1,531 independently solved physical profiles across 45 random cycle cases, including 15 with capacity filters. It checks both extrema, the exact interior-resistance example, irrational endpoint recovery, all-zero and flat objectives, infeasibility, a singleton capacity, and an 80-bit multiblock objective interval.

The independent optimization reviewer additionally checks pinned rational circulations against exhaustive rational LP vertex enumeration, which is distinct from the implementation's dual-threshold rule. The [separate arithmetic and schema audit](review-potential-flow-exact-weighted-cactus-arithmetic.md) passed 88 exact cancellation, radical-equality, and interval controls; constructed a two-cycle-plus-bridge graph to check both extrema and orientation/gauge invariances; rejected 24 malformed inputs; and checked the strict JSON CLI under `python -S` and `python -S -O`. This verifies the supplied block-input behavior, without implementing a general graph mapper.

These tests accompany the proof of candidate completeness; sampling alone does not establish global optimality. The returned JSON is exact solver output with physical witness checks, not a standalone independently verifiable optimality-certificate format. No approximation is used to choose the resistance profile. The full joint load-and-resistance accuracy-bit algorithm remains theoretical; this implementation solves its useful fixed-nomination subproblem completely in the stated block-input scope.
