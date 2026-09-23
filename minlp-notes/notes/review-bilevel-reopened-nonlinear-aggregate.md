# Independent review of nonlinear aggregate accuracy-bit optimization

Date: 2026-09-06. Reviewer: independent `existing_proof_audit` agent.
Reviewed: [candidate theorem](bilevel-reopened-nonlinear-aggregate.md),
Sections 1–10, building on my
[fresh existing-core review](review-bilevel-reopened-existing-core.md).

**Verdict: PASS.** The nonlinear aggregate certificate, nonlinear branch
cover, rational recovery across branch boundaries, and full error ledger
are correct under the stated assumptions. I found no substantive gap.
The author incorporated two minor clarity suggestions: dispatching the
empty-follower case and explicitly defining the normalized local costs.
This verdict does not establish publication priority or practical solver
performance.

## Model, constants, and aggregate certificate

A positive sum of strictly convex local costs remains strictly convex
after adding a convex aggregate cost. Convexity in the aggregate is
needed only for feasible leaders and aggregates in `W`: every actual
box response has its aggregate there, and all candidate auxiliary
aggregates are restricted to `W`. Positive definiteness of the aggregate
Hessian is unnecessary. It may be singular everywhere or vanish at
particular points.

The active-normal argument for bounded resource multipliers applies to
the full differentiable objective. It does not require separability.
Absolute coefficient bounds after aggregate normalization bound the
gradient and Hessian with polynomial encoding. Numerical powers of
`R` affect their bit length polynomially in the numerical degree. The
resource feasibility polytope and Hoffman constant are unchanged because
the feasible follower set is unchanged.

For the frozen-gradient box response, write `a=grad phi(x,w)` and
`a_q=grad phi(x,Uq)`. Its variational inequality and convexity give

```
F_x(z*) >= F_x(q) + lambda^T(Cq-b)
                       + (a_q-a)^T U(z*-q).
```

The resource multiplier sign in this inequality is correct. The last
term is bounded below by `-D rho`, since
`||a_q-a||inf<=L_phi rho` and
`||U(z*-q)||_1<=sum_i ||U_i||_1`. Repairing `q` and applying the
local-cost Bregman modulus proves the stated response bound. The
aggregate adds a nonnegative Bregman divergence; no new curvature
constant is needed.

Exact aggregate consistency and complementarity yield the complete
convex follower KKT conditions. Uniqueness then identifies the response.
Conversely every true optimum has a bounded multiplier and its true
aggregate. This proves the compact-subsequence continuity argument and
upper-objective attainment.

## Nonlinear inverse branches

The inverse arguments are polynomials in exactly `r+s+k` normalized
variables. Their degrees and coefficient encodings are polynomial after
composition, because both the ambient dimension and the variable count
of the supplied aggregate polynomial are fixed.

Realizable sign conditions of all breakpoint pullbacks suffice to
enumerate the branch vectors. At a sample in a sign condition, the order
of each inverse argument relative to every breakpoint is fixed. Therefore
the same branch vector is valid throughout that sign condition.
A zero sign at a breakpoint may use either neighboring branch.

Replacing the sign condition by the closed validity inequalities for its
chosen branches may enlarge its domain. This is harmless: every added
point still satisfies each chosen branch's error guarantee. The resulting
domains cover the normalized polytope, and their number is polynomial by
the fixed-dimensional sign-condition bound. They need not be connected
or rational polyhedra. This construction does not enumerate exponentially
many arbitrary combinations and does not require an algebraic-cell
closure algorithm.

The surrogate feasible sets are compact, so algebraic minimizers exist
whenever they are nonempty. At an actual optimal leader and exact
certificate, inverse approximation places the point in a surrogate
feasible set with the prescribed residual allowances. Consequently the
winning surrogate value is bounded above by `OPT+||c||_1 eta`.
Fixed-dimensional optimization retains polynomial bit complexity,
including the duplicated variables for global comparison.

## Rational recovery across branch boundaries

The nonlinear domains may contain no rational point. Preserving them
during output rounding would be a real error; this proof explicitly
preserves only `Q_0=X' times [0,1]^(s+k)`. Its vertices are rational,
including when `X'` is lower dimensional. A containing rational simplex
and rounded barycentric weights give the stated exact membership and
precision in polynomial bit complexity.

The original branch polynomial is not evaluated outside its valid
domain in the error proof. Instead the true clipped inverse controls the
response change. For a marginal of degree `d<=P`, a response displacement
of at least `eta` requires argument displacement at least
`(G_i/2)(eta/(2d))^d`. For `eta<=1/2` this is at least the proposed
common `alpha`. Clipping cannot decrease the argument displacement
required for that response displacement. The polynomial argument
Lipschitz constant and the strict rounding-distance bound therefore give
the claimed response change.

I independently recomputed the residual transfer:

- Resource error grows from `2S eta` by at most `S eta` from response
  change and `S eta` from the right-hand side, giving `4S eta`.
- Aggregate error grows from `2A eta` by at most `A eta` from response
  change and `A eta` from the aggregate coordinate, giving `4A eta`.
- Complementarity starts at `2k Lambda S eta`. Changing the true residual
  contributes at most `2k Lambda S eta`; changing the multiplier against
  the old residual contributes at most `k Lambda S eta`.

The last term needs an **absolute** bound on the old resource residual,
because an inactive row can have a large negative slack. The proof
includes the valid bound `Ebar` and the corresponding multiplier
precision. Thus its `5k Lambda S eta` estimate covers inactive rows,
rather than relying only on the one-sided feasibility tolerance.

All required rational precisions have polynomial bit length. Singular
nonlinear branch boundaries and vanishing marginal curvature do not
require a positive interior radius or an inverse derivative bound.

## Final ledger and leader-response stability

The selected tolerance makes the repair term at most `tau/2` and the
growth-bound term at most `tau/2`. The true recovered response is
therefore within `tau` of the frozen-gradient response. Comparing it
with the surrogate value at the **original** algebraic point incurs two
additional inverse approximation errors and the direct leader objective
change. Their sum is at most `7 epsilon/64`. Combined with the upper
bound on the winning surrogate value and exact leader feasibility, this
proves both output claims with room for its rational value approximation.

Section 10's leader-response modulus also passes. Apply Hoffman repair
in both directions between the two feasible follower polytopes, compare
the two optimal costs using the two repairs and the leader-parameter
Lipschitz bound, and obtain a gap of at most
`2(T_x+L K B_b) Delta`. The Bregman growth estimate and the first repair
distance give exactly the displayed modulus. Fixed resource normals
remain essential.

## Independent exact diagnostic

[The independent checker](../code/bilevel_reopened/nonlinear_aggregate_review.py)
uses only standard-library rational arithmetic. It passed:

- Five certified irrational nonlinear branch boundaries and ten rational
  recovered auxiliary points on opposite sides of those boundaries.
- Twenty exact complementarity-transfer terms, including multiplier
  changes against negative inactive-row slack.
- Twenty quartic-aggregate cases whose local and aggregate Hessians
  vanish at the exact optimum.

For the branch test,
`F_x(z)=z^2/2-xz+z^4/4`, `x=17/64`, has the exact optimum `z=1/4`.
The auxiliary boundary is `w^3=1/64+eta^4`. The checker certifies that
the defining rational is not a rational cube, brackets the boundary
exactly, and checks rational recovery on either side. This directly
exercises the reason the proof must allow nonlinear branch crossings.
The true response is computed from rational polynomial identities; no
numerical optimizer or original implementation is used.

These finite cases supplement the proof. They do not implement
quantifier elimination, the complete inverse approximation, or global
bilevel optimization. Run with
`python code/bilevel_reopened/nonlinear_aggregate_review.py`.

