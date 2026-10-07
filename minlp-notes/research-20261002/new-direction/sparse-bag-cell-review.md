# Independent review of sparse bag-cell pruning and exact closure

Date: 2026-10-02. Reviewed the complete
[author draft](sparse-bag-cell-smoothed-qp.md), with emphasis on the
deterministic algorithm, sparse DP, and exact closure. The probability and
finite-noise schedule have a
[separate review](sparse-bag-cell-noise-review.md). No external search or
additional agents were used for this review.

**Verdict.** No substantive gap was found in the deterministic algorithm or
closure argument. Aligned cell unions have the special rounding property
the proof needs, despite being coupled across bags. The gradient and PSD
tests are valid on every continuous-box instance, independently of growth
or noise. Quantitative growth and strict complementarity control when those
sound tests succeed; they are not assumptions accepted by the tests.

## 1. Common partitions are essential

Every bag must use the same coordinate partition at a given level. A cell
is a product of adjacent intervals in those common partitions. The proposed
grid, anchored at each original lower bound with step `h_j=s2^-j` and a
possibly clipped last interval, has this property. It is nested, and each
coordinate interval splits into at most two children.

Refinement must use the next common partition. In particular, the last
clipped interval need not be split at its own midpoint. Generating children
from the common dyadic grid preserves alignment without constructing all
coordinate grid nodes explicitly.

Closed cells can overlap at boundaries. This is harmless and is useful for
attaining minima. A global grid node lies in an adjacent-interval bag cell
exactly when its bag tuple is a corner of that cell. Therefore the local
corner whitelist describes precisely the global grid nodes in the physical
intersection of the bag-cell unions. It does not introduce spurious physical
assignments. Separator consistency and running intersection supply one
global coordinate assignment.

## 2. Independent rounding preserves all whitelists

Take a physical point in the current intersection of bag-cell unions. In
each bag, select any containing cell. A coordinate strictly between grid
nodes lies in one unique partition interval. Both rounding endpoints thus
belong to every selected bag cell containing that coordinate. A coordinate
already at a grid node stays fixed. Different bags may select cells on
different sides of that boundary without causing a conflict.

Consequently every independent rounding outcome is an allowed full grid
assignment. The same argument preserves any specified containing bag cell,
which is necessary for the conditional lower bound. It also covers a
physical feasible set that lies entirely on a shared cell boundary.

For the quadratic, independence and preservation of coordinate means give

```
E[F(Y)]-F(x) = (1/2)sum_i H_ii Var(Y_i)
             <= n L h_j^2/8 = E_j.
```

Off-diagonal terms have zero expected error, and negative diagonal terms
only improve the inequality. This uses the summed objective's diagonal
curvature, not a sum over its factor occurrences.

Arbitrary coupled constraints would not have this closure under rounding.
The result here follows from the common aligned-cell geometry.

## 3. Conditional bounds, witnesses, and retained optimizers

Let `m_j` be the minimum over allowed full grid assignments, and let
`m_B(v)` be the exact min-marginal for an entire bag row. If the current
physical domain contains every original optimizer, rounding an optimizer
shows `m_j<=f*+E_j`.

For a candidate bag cell `C`, set

```
q_C=min_{v a corner of C}m_B(v),
LB_C=q_C-E_j.
```

Rounding any current feasible point whose bag tuple lies in `C` stays in
`C` and is globally allowed. Its expected objective is at least `q_C`, so
`LB_C` is a valid conditional lower bound. If no corner extends to a full
allowed assignment, `q_C=+infinity`; rounding proves that the physical
intersection with that cell was empty as well.

Maintain a monotone feasible incumbent `U_j<=m_j`. Retaining exactly the
cells with `LB_C<=U_j` preserves every original optimizer, including one
lying on several cell boundaries. Equality must be retained. Refining all
retained cells leaves their physical union unchanged, so induction applies
at the next level.

Each retained cell has a finite minimizing corner and a full grid witness
`y` attaining that corner's min-marginal. This is a single consistent
assignment, with

```
F(y)=q_C<=U_j+E_j<=f*+2E_j.
```

No independent choices of per-bag minimizers are combined in this argument.
The saved incumbent need not remain in the retained physical domain: it is
still feasible for the original box and remains a valid upper bound.

## 4. Sparse DP work and certificate history

For each bag, deduplicate its cell corners into a sparse list of allowed
rows. A directed tree message stores the minimum by separator tuple.
Processing one row requires only lookup and addition of incoming messages
on its separator keys, followed by updating its outgoing key. It does not
require a Cartesian product of neighboring row lists.

Both message directions give each bag-row min-marginal as its local factor
value plus all incoming messages. Missing keys represent infinity. A
rerooting implementation must not subtract infinity from infinity; it can
recompute the bounded number of incoming terms, or keep finite sums and
infinity counts.

With `R_t` allowed rows at bag `t`, the direct work is proportional to
`sum_t(1+deg(t))R_t`, apart from bag indexing, factor evaluation, sorting,
and bit arithmetic. Binarizing the decomposition to maximum degree three
before running the algorithm gives the stated linear dependence on the
total number of rows. Its copied bags and their row lists must be included
in that total. A common-denominator rational grid also keeps separator-key
and table-entry bit lengths polynomial in the input length and level.

The final restricted grid alone is not a certificate over the original
domain. Retain the pruning history or allow a checker to recompute it. A
point first lost at stage `j` belongs to at least one deleted bag cell and
has objective greater than `U_j`. Monotonicity puts every such lower bound
above the final incumbent. The final grid lower bound `m_J-E_J` applies on
the retained domain, while the saved conditional bounds cover all removed
regions. This justifies global bounds and the invariant that all original
optimizers remain.

For the smoothed counting argument, a retained witness also gives a valid
comparison with the original-domain conditional minimum. Its existence is
not affected by the adaptive whitelist. The probability bound itself is
reviewed separately.

## 5. Original-bound gradient fixing is sound

For each coordinate, take each containing bag's retained projection hull,
then intersect these intervals. Their product `Q_j` contains every original
optimizer. It need not contain every retained cell, and the proof does not
require that stronger property.

Each gradient component is affine, so its exact range on `Q_j` is obtained
by choosing interval endpoints according to coefficient signs. If its lower
range endpoint is strictly positive, every original optimizer must have
that coordinate at its original lower bound. Otherwise a small decrease
would be feasible in the original continuous box and decrease the
objective. A strictly negative upper range endpoint similarly forces the
original upper bound.

This is first-order optimality on the original box. It does not require a
feasible path through the retained cell unions. It also does not permit
fixing a coordinate to an artificial hull endpoint. Recorded equations can
be accumulated because each holds at every original optimizer. Intersecting
the closure hull with those already justified equations and repeating the
gradient tests is sound for the same reason.

The same rule cannot be transferred directly to integer variables: a local
derivative sign does not provide a feasible infinitesimal integer move.
The reviewed closure is continuous.

## 6. PSD closure and its sufficient stopping condition

The recorded original-bound equations define an original box face containing
all global optimizers. If the principal Hessian on its unfixed coordinates
is PSD, the restricted problem is a convex box QP. Solving it exactly gives
the original global optimum. Rational PSD checks and convex-QP KKT
conditions make this final step independently checkable. No growth constant
or probability event is part of its acceptance rule.

For the sufficient stopping analysis, suppose the optimizer is unique,
point growth is at least `g0>0`, and active gradients are strictly
complementary with signed magnitude at least `tau>0`: positive at a lower
bound and negative at an upper bound. A retained cell witness satisfies

```
||y-x*|| <= h_j sqrt(nL/g0)/2.
```

Every coordinate in that cell is within one additional cell width of the
witness. Thus every retained projection, and also `Q_j`, is within

```
r_j=h_j[1+sqrt(nL/g0)/2]
```

coordinatewise distance of `x*`. Let `M` bound the maximum absolute Hessian
row sum. Gradient variation throughout `Q_j` is at most `M r_j`. If this
is at most `tau/2`, every active coordinate is correctly forced.

The remaining coordinates are interior at `x*`. Perturbing them within the
original box and using point growth gives the stronger quantitative fact

```
H_free,free >= 2g0 I.
```

In particular, the remaining Hessian is PSD, so closure succeeds. The
author's conservative rational bound `r_j<=(2+nL/g0)h_j` and terminal
condition are sufficient. An empty free set is immediate. This analysis
does not assert closure on tied or degenerate draws; the separately
described exact fallback covers those cases.

## Targeted exact verification

The command actually run was

```
python3 -B research-20261002/new-direction/check_sparse_bag_cells.py
```

The [checker](check_sparse_bag_cells.py) implements sparse separator-key
messages in both directions, exact bag min-marginals, backtracking, cell
pruning, original-bound gradient fixing, and the PSD closure test.
Independent exhaustive allowed-node assignments check the sparse DP.
Exact active-face enumeration supplies a small-instance global-QP oracle
and verifies the convex closure value; it is not presented as the search
algorithm or as a polynomial-time convex solver implementation.

The [results](sparse-bag-cell-check-results.json) record five instances and
16 stages, including unequal rational widths with clipped cells, nonconvex
boundary optima, flat and disconnected ties, positive-diagonal nonconvex
ties, and a branching decomposition. All assertions passed:

- 2,295 bag min-marginals matched exhaustive computation over 12,212 allowed
  assignments, drawn from 34,348 examined assignments;
- 2,807 rounded atoms preserved every whitelist;
- 392 retained-cell witnesses met the `2E_j` objective bound;
- 951 removed cells preserved all enumerated optimal vertices and the
  additional interior samples of flat optimal sets;
- two nonconvex cases reached exact closure after original-bound fixing,
  and a convex flat case closed immediately; the returned face solutions
  satisfied their exact convex KKT signs and equations.

A separate boundary fixture has opposite closed cells whose intersection
forces the shared coordinate to the common boundary. It checked four
globally infeasible bag rows, four feasible full assignments, and four
rounding outcomes that correctly kept the boundary coordinate fixed.

The checker was rerun after matching the author's intersection-of-hulls
construction and adding the boundary and KKT checks. The finite examples
make no expectation, performance, or novelty claim. No project-wide
verification or CI inspection was performed.
