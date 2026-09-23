# Vertex binarization of separable nonconvex programs with few linking rows

Date: 2026-09-21. Status: proofs written by the root agent; literature check
by a separate research agent completed. The
[independent review](../notes/review-separable-vertex-binarization.md) found
the mathematics correct and the first computational section inconsistent with
its data; this version incorporates every finding, as listed in
[the experiment record](../notes/separable-vertex-binarization-experiments.md).
Computational evidence is mixed and is reported in full below.

## Summary

The repository proves that spatial branch-and-bound needs `2^Omega(n)` nodes
on `min sum x_i(1-x_i), sum x_i = k+1/2, x in [0,1]^n`, for every separable
relaxation and also with [SDP+RLT](spatial-bb-sdp-rlt-exponential-lower-bound.md)
or [fixed-degree sum-of-squares](spatial-bb-product-domain-exponential-lower-bound.md)
node relaxations. This note gives a reformulation that removes the blow-up on
that family and records where it does and does not help in practice.

- **Structure (classical).** A separable piecewise convex/concave program with
  linear constraints has an optimal solution in which the variables lying
  strictly inside a concave piece have linearly independent constraint
  columns. At most `rank(A)` variables are in that state. The vertex argument
  is textbook; the special cases with one constraint are published several
  times (see [Literature](#literature)).
- **Reformulation (apparently new as a solver device).** Binary states
  "at a breakpoint", "in a non-concave piece", "strictly inside a concave
  piece", with the constraint `sum(interior indicators) <= rank(A)`. Breakpoint
  states make the objective exactly linear in binaries.
- **Separation (proved).** On the lower-bound family the reformulated model is
  solved by branch-and-cut with `2n+1` nodes and two Chvátal–Gomory cuts per
  node, against `2^Omega(n)` nodes for spatial branch-and-bound on the
  original model.
- **Computation.** On an asymmetric version of the family, Gurobi 13 and
  SCIP 10 time out at `n = 24` on the original model. On the reformulated
  model Gurobi solves `n = 400` in 0.5 s and SCIP solves `n = 120` in about
  2 s; BARON gains little. SCIP solves the *symmetric* original family
  through symmetry handling, which the lower bounds do not cover. On random
  concave-knapsack and power-cost instances, which the solvers already solve
  in seconds, the reformulation is **slower**, often by orders of magnitude.
  It is a targeted device, not a default.

## Setting

```
(P)   min  sum_{i=1..n} f_i(x_i) + c'y
      s.t. A x + B y  (<=, =, >=)  b,     l <= x <= u,
           y in Y = { y : D y <= d, y_j integer for j in J }.
```

`A` has `m` rows. Each `f_i : [l_i, u_i] -> R` comes with breakpoints
`l_i = beta_i0 < ... < beta_iK_i = u_i`, and a subset of the pieces
`[beta_i,j-1, beta_ij]` is tagged *concave*: `f_i` is concave on each tagged
piece. Nothing is assumed about untagged pieces. Assume (P) has an optimal
solution.

## Theorem 1 (vertex form)

Let `(x*, y*)` be optimal for (P). There is an optimal `(x°, y*)` such that

1. `x°_i = x*_i` whenever `x*_i` lies in no tagged piece;
2. otherwise `x°_i` lies in a tagged piece that contains `x*_i`;
3. the set `P = { i : x°_i is strictly inside its tagged piece }` has linearly
   independent columns `{A_i : i in P}`. In particular `|P| <= rank(A_C) <= m`,
   where `C` is the set of variables that have a tagged piece.

*Proof.* Let `N` be the set of `i` for which `x*_i` lies in a tagged piece and
choose one such piece `I_i` for each `i in N`. Define the polytope

```
Q = { z in prod_{i in N} I_i :  A_N z  (<=,=,>=)  b - A_{-N} x*_{-N} - B y* }.
```

`Q` contains `x*_N` and is bounded. `phi(z) = sum_{i in N} f_i(z_i)` is
concave on `Q`. Every point of `Q` is a convex combination of vertices, so a
concave function attains its minimum over `Q` at a vertex `v`, and
`phi(v) <= phi(x*_N)`; no continuity is needed. Put `x° = (v, x*_{-N})`.
It is feasible with objective at most that of `x*`, hence optimal. At the
vertex `v` of `Q` in `R^N` the active constraints have rank `|N|`. The
coordinates outside `P` contribute active bounds; the remaining rank `|P|`
must come from the rows of `A` that are active at `v`, restricted to the
columns in `P`. Hence those columns are linearly independent, already on the
active rows; `|P| <= rank(A_C)` is the weaker statement used below. QED.

*Remarks.* (a) The statement is about *some* optimal solution. The
cardinality constraint below is an optimality-based restriction, in the same
class as symmetry-breaking constraints, and must not be combined blindly with
other optimality-based reductions. (b) If the continuous part of `y` has
only bounds and rows of `[A B]` as constraints, and the resulting polyhedron
is pointed, the continuous variables may be moved into the polytope instead
of being fixed. The columns of `x_P` together with the columns of the
continuous `y` strictly between their bounds are then independent. This is
stronger but needs status binaries for `y`; general rows `D y <= d` would
have to be added to the row set. (c) Suppose there are `r` additional
constraints `sum_i q_ki(x_i) <= b_k` whose terms are concave on the tagged
pieces. Starting from an optimal point in the relative interior of a face of
`Q` of dimension larger than `r`, pick a direction in that face orthogonal to
one supergradient `sigma_k` of each of the `r` functions at that point. By
concavity `q_k(x + t v) <= q_k(x) + t sigma_k'v = q_k(x)` for every `t`, so
the whole line stays feasible for these constraints, and the concave
objective does not increase towards one of its two ends. Moving to
the end reduces the face dimension; iterating gives an optimal point in a
face of dimension at most `r`, hence `|P| <= rank(A_C) + r`. This is a count
only; no independence statement is claimed.

## Corollary 2 (second-order form; Hager–Pardalos–Roussos–Sahinoglou)

Let `f` be `C^2` near a local minimizer `x*` of `f` over `{A x (<=,=,>=) b,
l <= x <= u}`. Let `F` be the set of variables strictly between their bounds
and `R` the active rows. If `S` is a subset of `F` with `H_SS = grad^2_SS f(x*)`
negative definite, the columns `{(A_R)_i : i in S}` are linearly independent.

*Proof.* Otherwise some `d != 0` supported on `S` has `A_R d = 0`. Both `d`
and `-d` are feasible directions, so `grad f(x*)'d = 0` and the second-order
necessary condition gives `d'Hd >= 0`, contradicting `d_S' H_SS d_S < 0`. QED.

This is the index-set form of the inertia count of Hager et al. (1991): at
least `s` constraints are active when the Lagrangian Hessian has `s` negative
eigenvalues. For box constraints it is the known rule "`f_ii < 0` implies
`x_i` at a bound". It holds at every local minimizer and for nonseparable
`f`, but needs strict concavity and smoothness. We record it as a corollary
and do not use it computationally.

## Reformulation

For a tagged piece `j` of variable `i` with length `L = beta_ij - beta_i,j-1`:
binaries `d` (piece selected), `u` (at the upper end), `t` (strictly inside),
and a continuous offset `s`:

```
u + t <= d,     0 <= s <= L t,
x_i contribution:  beta_i,j-1 d + L u + s,
cost contribution: f(beta_i,j-1) d + (f(beta_ij) - f(beta_i,j-1)) u + g(s),
g(s) = f(beta_i,j-1 + s) - f(beta_i,j-1).
```

For an untagged piece: `d` and an offset `o in [0, L d]`, with cost
`f(beta_i,j-1 + o) - f(beta_i,j-1)(1 - d)`. One piece per variable is
selected, and `sum t <= rank(A_C)`. The `x_i` are eliminated by substituting
their affine expressions into the linking rows.

**Exactness.** Every feasible point of the reformulation maps to a feasible
point of (P) with equal cost. Theorem 1 gives an optimal solution of (P) that
is representable. Hence the optimal values agree.

**A modelling detail that matters.** Keeping explicit `x_i` variables with
defining equalities, instead of substituting them into the linking rows,
stops Gurobi from closing the gap: the symmetric family at `n = 60` then
stops at bound `0` after 20 s, against `0.1 s` after substitution
(`side_checks/explicit_x_check.py`).

## Theorem 3 (separation on the lower-bound family)

For `P_n: min sum x_i(1-x_i), sum x_i = k + 1/2, x in [0,1]^n`, the
reformulation has binaries `u_i, t_i`, offsets `0 <= s_i <= t_i`,
`u_i + t_i <= 1`, `sum t_i <= 1`, the row `sum (u_i + s_i) = k + 1/2`, and
objective `sum g_i` with `g_i = s_i(1-s_i)` relaxed by its chord on the
current bounds of `s_i`. The following branch-and-cut proves the optimal value
`1/4` with `2n+1` nodes.

Branch on `t_1, t_2, ...` in order. In the node `t_j = 1` all other `t_i`
and `s_i` vanish and `u_j = 0`, so the row reads
`sum_{i != j} u_i + s_j = k + 1/2` with `0 <= s_j <= 1`. Rounding
`sum u_i <= k + 1/2` gives `sum u_i <= k`, hence `s_j >= 1/2`. Rounding
`sum u_i >= k - 1/2` gives `sum u_i >= k`, hence `s_j <= 1/2`. The chord
of `g_j` on the original interval `[0, 1]` is identically `0`, so the
argument needs bound tightening: the two cuts fix the bounds of `s_j` to
`[1/2, 1/2]`, the chord is rebuilt on the new bounds and equals `1/4`, and the
node is pruned against the incumbent value `1/4` (for instance
`x = (1,...,1,1/2,0,...,0)`). In the final node all `t_i = 0`, the row is
`sum u_i = k + 1/2`, and the same two rounding cuts prove infeasibility. QED.

By the repository's lower bounds, every spatial branch-and-bound tree for the
original `P_n` with separable, SDP+RLT, or fixed-degree SOS node relaxations
has `2^Omega(n)` leaves when `k` is linear in `n`. The separation is between
two solution methods for the same problem, with three qualifications.

1. The lower bounds cover box branching with the stated node relaxations.
   They exclude symmetry exploitation, and `P_n` is fully symmetric: SCIP's
   symmetry handling solves the original `P_30` in 11 nodes. The experiments
   therefore use the asymmetric family `P_n^w` with costs
   `c_i x_i(1-x_i)`, `c_i = 1 + i/n`. The separable and SDP+RLT lower bounds
   extend to it: for `1 <= c_i <= 2` a weighted node bound is at most twice
   the unweighted one, so a tree that proves tolerance `eps` for `P_n^w`
   proves tolerance `1/8 + eps/2 < 1/4` for `P_n`. The SOS variant was not
   checked. Theorem 3 holds for `P_n^w` with optimal value `min_i c_i / 4`
   and pruning by bound in every node `t_j = 1`.
2. The repository's lower-bound notes already record a non-separable clique
   cut that closes the root gap of the original `P_n`. The lower bounds are
   about relaxation classes, not about every conceivable cut.
3. The upper bound uses integer rounding cuts and bound tightening, which
   have no counterpart in the lower-bound model.

The result does not say that (P) becomes easy: with general weights
`sum a_i x_i = b` the problem contains subset sum.

## Computational evidence

Code: [`code/vertex_binarization`](../code/vertex_binarization/README.md).
Full tables, the setup, solver errors and side checks are in
[the experiment record](../notes/separable-vertex-binarization-experiments.md).
Every cell is a single run; the machine was shared, so only large
differences are meaningful.

Findings, in the order in which they limit the claim:

1. **Random instances: the reformulation hurts.** On random concave-knapsack
   and power-cost instances (`n <= 100`, `m <= 5` dense rows) the original
   model is solved in at most 30 s and usually under 1 s. The reformulated
   model is slower in almost every cell. With `m = 5` it reaches the 60 s
   limit with BARON from `n = 25` or `50`, with SCIP from `n = 50` or `100`,
   and with Gurobi at `n = 100`.
2. **Asymmetric lower-bound family: exponential gain with Gurobi, large gain
   with SCIP, little with BARON.** Original model: Gurobi and SCIP reach the
   120 s limit from `n = 24`, BARON from `n = 18`, all with dual bound `0`.
   Reformulated: Gurobi solves `n = 400` in 0.5 s; SCIP solves up to
   `n = 120` in about 2 s and fails at `n = 400`; BARON solves only
   `n <= 18`. The gain depends on the solver's integer cuts.
3. **Symmetric family.** SCIP solves the original model instantly through
   symmetry handling (11 nodes at `n = 30`; a timeout with
   `misc/usesymmetry = 0`). The lower bounds do not cover symmetry
   exploitation, and the symmetric family is not evidence for the
   reformulation with SCIP.
4. **Sigmoid and quartic families.** The reformulation reduces the gaps of
   SCIP and BARON on sigmoids and of Gurobi on quartics, but does not solve
   the instances. The
   [univariate envelope handler](composite-univariate-envelopes.md) does.
5. **Box-constrained nonconvex QP (`m = 0` rule).** No benefit with Gurobi on
   six `spar` instances, and one instance became 20 times slower.
6. **Solver errors.** One Gurobi run on a reformulated quartic instance and
   three BARON runs on original power-cost instances report `optimal` with
   wrong values. They are documented in the experiment record and are not
   counted as solved.

## Literature

Checked by a separate agent on 2026-09-21; full texts of several sources
were not accessible, and an unsuccessful search does not establish novelty.

- Vertex optimality of concave minimization: Falk–Soland (1969), Horst–Tuy.
- One constraint: Moré–Vavasis (1991, concave knapsack); Vavasis (1992);
  Ginsberg (1974), Ağralı–Geunes (2009), Duijzer et al. (2018) for S-curves;
  Zhan et al. (2015) for economic dispatch with valve points ("singular
  points, small convex regions, and one slack unit"); Malaguti et al. (2019).
- General `m`, for the *convexified* problem and as an error bound:
  Aubin–Ekeland (1976), Udell–Boyd (2016).
- Second-order count: Hager–Pardalos–Roussos–Sahinoglou (1991); box case:
  Hansen et al. (1993), Vandenbussche–Nemhauser (2005), Burer–Chen (2011).
  Yıldırım (2025) reviews KKT-based global QP and lists second-order
  conditions only for box constraints.
- Closest reformulation: SC-MINLP of D'Ambrosio–Lee–Wächter (2009, 2012)
  binarizes convex and concave intervals and refines secants on concave
  ones. It has no breakpoint state and no cardinality constraint.
- No earlier exponential lower bound for continuous spatial branch-and-bound
  on this family was found; Udell–Boyd use `x(x-1)` in a hardness reduction.

Claim: to our knowledge this is the first use of the vertex property as a
cardinality constraint on status binaries in a general-purpose reformulation,
and the first proved exponential separation between spatial branch-and-bound
and such a reformulation. The structural theorem itself is not claimed.

## Limitations

- Useful only when `rank(A_C)` is small relative to the number of nonconvex
  variables, and only when the original model actually suffers from the
  lower-bound mechanism. We have no detection rule for the latter.
- Gains depend on the solver's integer cutting planes; BARON shows none.
- A piece is tagged concave only when ball arithmetic encloses `f''` in the
  nonpositive reals; floating-point evaluation of `f` itself is not verified.
- The budget uses a floating-point rank. An underestimate would make the
  model invalid; nearly dependent columns need an exact rank.
- Side variables `y` are implemented but not covered by tests.
- Economic dispatch with valve points has this structure with `m = 1`, but
  the published adaptive MIQP method already certifies the 40-unit case in
  about two seconds, so no speed claim is made there.
