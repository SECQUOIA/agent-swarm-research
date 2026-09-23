# Exact dense quadratic bilevel optimization from certified surrogate cells

Date: 2026-09-06. Status: independently reviewed research theorem, quantitative
corollary, and exact-arithmetic proof of concept. The
[first review](../notes/review-bilevel-reopened-approximate-structure.md) and
[second review](../notes/review-bilevel-reopened-approximate-structure-second.md) pass
the exact-recovery theorem and the explicit perturbation-neighborhood
corollary. The first review also independently proves the adopted
weak-closure screening refinement. The perturbation enclosure and
safe-screening ingredients are classical
in spirit. The candidate contribution is their combination with a supplied
fixed-rank surrogate to obtain an exact global algorithm parameterized by the
number of coordinate statuses that cannot be certified on each surrogate cell.
No claim is made that a small matrix perturbation alone ensures this parameter
is small, or that an appropriate surrogate can always be found.

## Model and intended use

The leader chooses `x` in a nonempty compact rational polytope
`X subset R^r`. The true follower is

```
z(x) = argmin { (1/2)z^T Q z + (c+Cx)^T z : 0 <= z <= 1 },
Q = Q^T > 0.
```

All data are rational. The leader minimizes an affine function of `(x,z(x))`
and may impose any finite list of rational affine inequalities or equalities
in `(x,z(x))`. There is no upper-constraint margin assumption.

Supply a surrogate Hessian

```
Qhat = Diag(d) + U H U^T > 0,
d_i > 0, H = H^T, U in Q^(N x k).
```

The surrogate uses the same box and the same affine linear cost. Write its
response as `y(x)`, and let `E=Q-Qhat`. The true `Q` may be dense and its
interaction rank need not be bounded. No norm bound on `E` is required for
correctness. Small residuals help screening, not validity.

The [fixed-rank cellwise-LP corollary](../notes/bilevel-fixed-rank-quadratic-corollary.md)
constructs at most `N^{O(r+k)}` closed rational polytopes `P_j` in coordinates
`v=(x,w)`, where `w=U^T y`. Each `P_j` includes the affine surrogate consistency
equations, projects into `X`, has an affine formula `y_j(v)`, and together the
polytopes cover the complete surrogate response graph over `X`. Empty cells
are discarded. Lower-dimensional cells and duplicate descriptions are harmless.
Explicit aggregate bounds make every `P_j` compact.

The algorithm below works for **any supplied finite rational polyhedral cover**
with these properties, including a rational subdivision of these cells. Its
cost then depends on the actual number and description sizes of the cover
polytopes. Refinement is optional and has no unconditional size guarantee.

## 1. A directional response enclosure

Fix a leader and abbreviate `a=c+Cx`, `y=y(x)`, `z=z(x)`,
`e=z-y`, `p=Ey`, and `ghat=Qhat y+a`. Then

```
e^T Q e + p^T e <= 0.                                      (1)
```

Indeed, the two follower variational inequalities give
`(Qz+a)^T(y-z)>=0` and `(Qhat y+a)^T(z-y)>=0`. Their difference is exactly
`e^TQe+p^Te<=0`. Positive definiteness yields the ellipsoid

```
(e + (1/2)Q^{-1}p)^T Q (e + (1/2)Q^{-1}p)
    <= (1/4)p^TQ^{-1}p.                                   (2)
```

For every signed output vector `b`, including a signed leader-objective row,

```
-(1/2)b^TQ^{-1}p - (1/2)sqrt((b^TQ^{-1}b)(p^TQ^{-1}p))
 <= b^T(z-y) <=
-(1/2)b^TQ^{-1}p + (1/2)sqrt((b^TQ^{-1}b)(p^TQ^{-1}p)).     (3)
```

This follows by completing the square and Cauchy--Schwarz in the `Q` norm.
It is an exact support calculation for (2), not an assertion that every point
of that ellipsoid is a possible follower response. Box restrictions and the
individual variational inequalities can tighten it further.

These enclosures require the exact surrogate response. A floating-point
surrogate solve cannot simply be substituted without a residual correction.

## 2. Uniform, exactly checkable screening on a whole cell

On a nonempty cover polytope `P`, `y(v)` and `p(v)=Ey(v)` are affine. Compute

```
eta_P = max { p(v)^T Q^{-1}p(v) : v a vertex of P }.         (4)
```

This is also the maximum over all of `P`: the quadratic is convex and every
point of a compact polytope is a convex combination of its vertices. The
quantity is rational. In fixed ambient dimension `r+k`, enumerate vertices
with rational linear algebra in polynomial time, even when `P` has smaller
affine dimension. In particular this step does not solve a general
high-dimensional convex-quadratic maximization problem.

Define affine centers and constant half-widths

```
s_i(v) = y_i(v) - (1/2)(Q^{-1}p(v))_i,
R_i = (1/2)sqrt((Q^{-1})_ii eta_P),
t_i(v) = ghat_i(v) + (1/2)p_i(v),
S_i = (1/2)sqrt(Q_ii eta_P).
```

Applying (3) with `b=e_i` and `b=Q e_i` gives, throughout `P`,

```
s_i(v)-R_i <= z_i(x) <= s_i(v)+R_i,                        (5)
t_i(v)-S_i <= (Qz(x)+a(x))_i <= t_i(v)+S_i.                (6)
```

Assign a status to coordinate `i` if any of these sufficient tests passes:

| Status | Meaning throughout `P` | Sufficient test |
| --- | --- | --- |
| `L` | `z_i=0` | `min_P t_i > S_i`, or `max_P s_i + R_i <= 0` |
| `U` | `z_i=1` | `max_P t_i < -S_i`, or `min_P s_i - R_i >= 1` |
| `F` | `(Qz+a)_i=0` | `min_P s_i > R_i` and `max_P s_i < 1-R_i` |

The gradient sign tests for `L` and `U` are **strict**: a zero gradient does
not identify a bound. The coordinate enclosure tests can be weak because
the true follower belongs to the box. The `F` certificate implies strict
interiority on this cell, but subsequent LPs use weak box inequalities.

All affine minima and maxima are rational LP values, or can be computed
directly over the vertices already enumerated for (4). Square roots need not
be approximated: for rational `A` and nonnegative rational `B`, test
`A>sqrt(B)/2` by `A>0` and `4A^2>B`; analogous weak and negative comparisons
handle the other cases. Thus screening uses rational arithmetic and sign
tests only. Coordinates failing all tests are **ambiguous**. Write their
number as `t_P` and let `t=max_P t_P`.

For a nonempty valid cell conflicting status certificates cannot occur.
The tests are sufficient, not necessary. Stronger sound certificates can be
used without changing the next theorem.

**A useful closure refinement.** The following weaker boundary conditions
also certify `F`:

```
min_P s_i >= R_i,   max_P s_i <= 1-R_i,
max_P s_i > R_i,    min_P s_i < 1-R_i.                     (10)
```

Indeed, the affine lower slacks `s_i-R_i` and `1-R_i-s_i` are nonnegative
and not identically zero. Each is strictly positive on the relative interior
of `P`. Equation (5) makes the true response strictly interior there, hence
its gradient is zero. Strongly convex box-QP responses are continuous in
`x` (also following directly from their variational inequalities), so the
zero gradient extends to all of `P`. This works for lower-dimensional cells.
Similarly, `min_P t_i>=S_i` together with `max_P t_i>S_i` certifies `L`,
and `max_P t_i<=-S_i` together with `min_P t_i<-S_i` certifies `U`.
One cannot drop the respective nonidentity/strict-somewhere conditions.

In particular, if `E=0`, (10) recognizes a surrogate interior region on its
closed cell even when its closure includes clipping boundaries. Artificial
ambiguity from merely closing such a cell need not cause enumeration.

## 3. Exact global algorithm with a verifiable ambiguity parameter

**Theorem.** For the model above, a cover of `M` rational polytopes in fixed
dimension `r+k`, and sound coordinate certificates with at most `t`
ambiguous coordinates on each polytope, exact bilevel feasibility and a
rational global optimizer can be obtained with at most `M 3^t` rational
recovery linear programs and polynomial-time rational preprocessing per
program. Screening can use the existing vertices, so no additional LP calls
are required for its affine extrema.
The explicitly computable certificates in Section 2 provide such a `t`
without an oracle. Starting from the supplied fixed-rank surrogate gives
bit complexity

```
3^t (N + m + input_bit_length)^{O(r+k+1)},                  (7)
```

where `m` counts the explicit leader-polytope and upper constraints. This is
polynomial for fixed `r,k,t`, and fixed-parameter exponential in `t` for fixed
`r,k`. No bound on the number of certified `F` coordinates is needed.

**Proof.** Work on one cover polytope `P`. Keep all certified statuses and
enumerate `L,F,U` for the ambiguous coordinates. Each completed assignment
partitions the indices into `L,F,U`; set `z_L=0`, `z_U=1`, and solve

```
z_F(x) = -Q_FF^{-1}(c_F + C_F x + Q_FU 1).                (8)
```

Every principal submatrix of the positive definite rational `Q` is positive
definite and invertible. Equation (8) is an affine rational formula, even
when there are many free coordinates and dense couplings among them. For
empty `F`, omit the equation. Substitute this formula and impose

```
v in P,
0 <= z_F(x) <= 1,
(Qz(x)+c+Cx)_L >= 0,
(Qz(x)+c+Cx)_U <= 0,
all leader upper constraints at (x,z(x)).                 (9)
```

The objective and all constraints are rational affine in `v`; hence (9) is
an LP in at most `r+k` coordinates. It has an attained optimum whenever
nonempty, because `P` is compact.

Every feasible LP point satisfies the complete box KKT conditions for the
true positive definite follower, so it gives its unique exact response.
Conversely, take any feasible true leader-response pair and a cover cell
containing its surrogate graph point. Every certified status holds there.
Each ambiguous coordinate has at least one compatible status: use `F` if
its gradient is zero, `L` if at the lower bound with positive gradient, and
`U` if at the upper bound with negative gradient. Thus at least one
enumeration includes this pair. Degenerate bound points with zero gradient
may also appear in multiple LPs; overlaps lose no solutions. Minimizing over
all nonempty LPs gives the exact bilevel optimum. If every LP is empty, the
original bilevel problem is infeasible.

Rational inversion, affine substitutions, LP, and fixed-dimensional vertex
enumeration have polynomial bit complexity. There are at most `3^{t_P}`
LPs on each cell. Combining with the surrogate-cell count proves (7).

**Interpretation.** A dense problem need not be replaced by the approximate
surrogate when the latter gives enough information to certify most statuses.
Only the uncertain statuses are enumerated; the recovered response and all
upper constraints use the true Hessian. This is a sufficient tractability
certificate, not a worst-case polynomial algorithm for dense followers.

## 3a. A computable neighborhood in which ambiguity is bounded

The preceding parameter is not just an unexplained promise. A positive
rational perturbation radius can be computed around any surrogate whose
vertices have bounded clipping-transition multiplicity.

Use the original closed surrogate cells, retaining their nominal coordinate
labels `L,F,U`. At a vertex `v`, call coordinate `i` a **transition coordinate**
if `y_i(v)` is `0` or `1` and `ghat_i(v)=0`. Let `q` be the maximum number of
such coordinates at a vertex of any nonempty original cell. This includes
vertices arising from surrogate consistency equations and the leader
polytope; no general-position assumption is implicit.

Triangulate every cell using only its existing vertices. All these simplices
form a finite closed cover of the surrogate response graph. The affine
dimension of each cell is at most `r`: its projection onto `x` is injective,
because a fixed `x` has one surrogate response and one aggregate `w`. An
injective projection on a polytope is injective on its affine hull, as can be
seen in a relative-interior neighborhood. Consequently every simplex has at
most `r+1` vertices.

For a simplex `T`, let `J_T` be the union of its vertices' transition
coordinates. Then `|J_T| <= (r+1)q`. If `i` is outside `J_T`, its nominal
cell label gives a strictly positive margin at every vertex:

```
L: ghat_i(v);
U: -ghat_i(v);
F: both y_i(v) and 1-y_i(v).
```

The label is fixed on the containing original cell. If any displayed margin
were zero at a vertex, that coordinate would be in `J_T`. Let `sigma` be the
minimum of all these margins over all simplices and all their coordinates
outside `J_T`. It is a positive rational number; if the list is empty, set
`sigma=1`. By affine interpolation these same margins are at least `sigma`
throughout each simplex.

Compute rational matrix bounds and an integer dimension bound

```
m = 1 / ||Qhat^{-1}||_infinity > 0,
L = ||Qhat||_infinity,
R = ceil(sqrt(N)),
eps_0 = min { m/2,
              sigma / [4 R max(1/m, 1+L/m)] }.             (11)
```

For symmetric matrices the induced infinity norm bounds the spectral norm,
so `lambda_min(Qhat)>=m` and `||Qhat||_2<=L`.

**Corollary.** Every rational symmetric `Q` with
`||Q-Qhat||_infinity <= eps_0` is positive definite, and its exact bilevel
problem is solved by the theorem with at most `(r+1)q` ambiguous coordinates
on every simplex. The resulting algorithm is polynomial-time for fixed
`r,k,q`; it computes exact rational optima and handles all the original
affine response-dependent upper constraints.

**Proof.** Write `eps=||E||_infinity<=m/2`. Then `Q` has minimum eigenvalue
at least `m/2`. Equation (1), the box bound `||y||_2<=sqrt(N)<=R`, and
Cauchy--Schwarz yield the standard sensitivity estimate

```
||z-y||_2 <= 2 eps R/m.                                   (12)
```

The true gradient minus the surrogate gradient is `Qhat(z-y)+Ez`. Since
`z` also lies in the unit box,

```
||Qz+a-ghat||_2
 <= L ||z-y||_2 + eps R
 <= 2 eps R (1+L/m).                                     (13)
```

The choice (11) makes both bounds at most `sigma/2`. Every nominal `L`
coordinate outside `J_T` therefore has a strictly positive true gradient,
every nominal `U` coordinate has a strictly negative true gradient, and
every nominal `F` coordinate has true response in
`[sigma/2,1-sigma/2]`. These are sound whole-simplex certificates. Only
coordinates in `J_T` need enumeration. The main theorem applies.

Fixed-dimensional polytope vertex enumeration and vertex triangulation give
polynomially many rational simplices with polynomial-size descriptions, and
all margins and the radius have polynomial bit length. The polynomial degree
can increase under triangulation: a coarse bound is a sum of `V_P^{r+1}`
possible vertex tuples, with `V_P` the vertex count of a cell. No claim is
made that this corollary keeps the original arrangement exponent unchanged.

**Scope.** This is a radius around the supplied instance; it can be very
small. Neither `q<=r` nor a useful numerical lower bound on `eps_0` is
automatic. Large simultaneous transition multiplicity and tiny margins
explain why small unrestricted coupling remains compatible with the
repository's near-identity hardness theorem. The dense perturbation within
this radius can have arbitrary rank and signs.

## 4. Useful approximate certificates when screening leaves many coordinates

For any output `b`, define on cell `P`

```
q_b(v) = b^T y(v) - (1/2)b^TQ^{-1}p(v),
rho_b = (1/2)sqrt((b^TQ^{-1}b)eta_P).
```

Then `q_b-rho_b <= b^Tz <= q_b+rho_b`. Using outward rational upper bounds
on each `rho_b` gives rational LP bounds. For an upper row
`a_j^Tx+b_j^Tz <= h_j`, the inner sufficient condition is
`a_j^Tx+q_bj+rho_bj <= h_j`, while the outer necessary condition is
`a_j^Tx+q_bj-rho_bj <= h_j`. An equality can be represented by two rows.

Minimize the lower objective enclosure over the outer LPs to obtain a
certified lower bound on the true optimal value. Minimize the upper objective
enclosure over the inner LPs to obtain a certified upper bound and a leader
that is feasible for the true follower. A true-follower solve with an exact
KKT certificate at any such leader can improve the upper bound. If all outer
LPs are empty, the true problem is infeasible; empty inner LPs alone imply
nothing about true feasibility. An outer lower bound is valid even when its
minimizer is infeasible for the true problem.

This sandwich is conventional robustification of a sound response enclosure;
it is a useful fallback, not the main novelty claim. It handles signed
objective coefficients without replacing them by an unstated monotonicity
assumption. It also does not establish small objective loss without a
reported finite gap between the actual computed bounds.

## 5. Boundaries and negative findings

- Small `||Q-Qhat||` does not force `t` to be small: many coordinates can lie
  at or near clipping thresholds together. The dense near-identity hardness
  result in this repository remains fully compatible with this theorem.
- A cell with a surrogate switching boundary may contain different true
  active sets even for an arbitrarily small perturbation. Reusing its
  surrogate active set without screening or rechecking true KKT conditions
  is unsound. Enumeration on the ambiguous coordinates handles shifted
  switching points exactly.
- A floating-point approximate QP response does not give the stated exact
  cell certificate without additional residual analysis or rational KKT
  recovery. The implementation must distinguish its exact checks from
  numerical evidence.
- Good screening does not imply a practical advantage over every standard
  global method. Dense rational linear algebra and a high-dimensional
  surrogate arrangement can dominate the cost.
- The method does not discover a good diagonal-plus-low-rank approximation,
  and no universally effective refinement strategy is established.

A concrete conservatism example is `Qhat=I`, `Q=I+(eps/N)11^T`,
`c=0`, `C=-1`, and `X=[0,1]`, for any positive small `eps`. The true response
is simply `z_i=x/(1+eps)`. The constant cell-wide ellipsoid radii can leave
every coordinate ambiguous on `[0,1]`, even though all true gradients are
zero throughout that interval. The script verifies this for `N=6` and
`eps=1/1000`. Thus the screening parameter measures the chosen certificate,
not intrinsic problem difficulty.

An inexpensive optional improvement is to try a complete guessed status
assignment first. Recover its affine true response by (8), then check every
true KKT inequality at every vertex of the cover cell. If all pass, affine
interpolation certifies that assignment throughout the cell; uniqueness
then gives the exact response there without any enumeration. This resolves
the example above. Failure of this sufficient whole-cell test does not
justify discarding that assignment on a smaller part of the cell.

## 6. Source comparison

The literature search on 2026-09-06 used combinations of "quadratic
programming", "safe screening", "variational inequality", "ellipsoid",
"bilevel", "low rank", and "active set". Sources checked include:

- Liu, Zhao, Wang and Ye (2014), [Safe Screening with Variational Inequalities
  and Its Application to Lasso](https://proceedings.mlr.press/v32/liuc14.html),
  including the [open paper](https://proceedings.mlr.press/v32/liuc14.pdf).
  This directly precedes the use of variational inequalities to enclose
  solutions and eliminate coordinates. We do not claim that principle.
- Ndiaye, Fercoq and Salmon (2021), [Screening Rules and its Complexity for
  Active Set Identification](https://arxiv.org/abs/2009.02709),
  [open paper](https://arxiv.org/pdf/2009.02709). This develops a general
  screening/identification framework and complexity analysis; screening
  and optimality-based status identification are established concepts.
- Yang et al. (2024), [A Safe Screening Rule with Bi-level Optimization of
  nu Support Vector Machine](https://arxiv.org/html/2403.01769v1), especially
  Sections 2--3. This is a close application precedent combining box-bound
  status screening and variational inequalities for SVM parameter tuning.
  Its auxiliary bilevel screening formulation is not the above exact global
  affine-leader optimization theorem based on a low-rank surrogate cover
  and a verified per-cell ambiguity parameter.
- The existing [fixed-rank corollary](../notes/bilevel-fixed-rank-quadratic-corollary.md)
  credits classical parametric and resource-allocation cell methods. Affine
  recovery from a fixed quadratic active set is also classical; equation
  (8) is not claimed to be new.

The candidate contribution is therefore narrow: **a verifiable route from a
tractable surrogate response cover to exact global dense quadratic bilevel
optimization with an exponential factor only in the uncertified statuses**.
No identical theorem was found in the sources above. This is a bounded
open-literature search, not proof of publication priority.

The subsequent [independent literature audit](../notes/bilevel-reopened-literature-audit.md#exact-dense-quadratic-optimization-after-certified-status-screening)
checks closer antecedents in detail:

- Dantas and Gribonval (2019), [Stable safe screening and structured
  dictionaries for faster L1 regularization](https://arxiv.org/pdf/1812.06635v3),
  already use an approximate structured model to screen the original dense
  model safely. Sections III--IV are direct precedents; surrogate-based
  safe screening itself is not a new contribution here.
- Arnström and Axehill (2020), [A Unifying Complexity Certification Framework
  for Active-Set Methods for Convex Quadratic Programming](https://arxiv.org/pdf/2003.07605v2),
  analyze entire parameter regions and certify active-set-method complexity.
  Their working-set-sequence partition has a different target from this
  supplied-surrogate-cover global bilevel algorithm.

The audited distinction remains the exact `M 3^t` global recovery theorem
and its computable, geometry-dependent perturbation neighborhood. The
nearby-model screening principle and uniform parameter-region analysis
must be attributed to the earlier work.

## 7. Reproducible checks and computational limits

The companion script is
[`approximate_structure_checks.py`](../code/bilevel_reopened/approximate_structure_checks.py).
The [recorded output](../code/bilevel_reopened/approximate_structure_checks.json)
comes from the final successful run of

```
python code/bilevel_reopened/approximate_structure_checks.py
```

It uses exact SymPy rational arithmetic; scalar leader LPs are solved by
interval intersection. The final run took about 2.7 seconds in this workspace.
It checks:

- Three dense five-coordinate instances against all 243 true status
  assignments each, with signed objectives and signed upper inequalities.
- 117 exact directional enclosures at 13 leader points.
- Singleton cells, zero-gradient bound degeneracy, and the weak-closure
  `F` certificate for six coordinates touching both clipping boundaries.
- A shifted switching point from surrogate `1/2` to true `11/20`, with
  exact constrained leader `187/250`; feasible exact upper equalities and
  infeasible upper inequalities.
- A signed-objective sandwich with true optimum `-1/5`, lower bound
  `-22461311/83886080`, and feasible upper bound `-11093121/83886080`.
  The equality example has an empty robust inner approximation despite
  true feasibility, confirming the stated limitation.
- The conservative-screening example above, including a direct exact
  all-free KKT certificate on the whole cell.

Dense synthetic examples illustrate the recovered status count:

| `N` | Surrogate cells | Maximum ambiguous coordinates | Completed cell/status LPs | Computed guaranteed perturbation radius |
| --- | --- | --- | --- | --- |
| 8 | 13 | 2 | 105 | `1/672` |
| 12 | 20 | 2 | 168 | `5/1408` |
| 20 | 33 | 2 | 285 | `1/1520` |

All three examples have vertex transition multiplicity `q=1`; their dense
perturbations lie within the computed radius. The corollary's independent
norm certificates verify every coordinate outside the two endpoint-transition
sets. Every returned solution has exact true KKT verification. The large
naive alternative `3^20` is only an enumeration count; it is not a benchmark
against modern QP or global bilevel solvers.

The independent first-review script uses separately written code and reports
24 random cases, 61 cells, 549 screened recovery assignments versus 3213
complete assignments, and 918 exact directional checks. It also checks a
separate eight-coordinate quantitative-neighborhood example. The second
review independently checks 20 further four-coordinate cases, including
exact upper equalities and indefinite residuals. The review files link their
scripts and saved outputs. Neither imports the author's implementation.

All theorem, corollary, closure-refinement, and stated arithmetic verification
obligations are complete. The general multi-dimensional cover and
triangulation arguments have mathematical review; the implementation is
explicitly a scalar-leader, diagonal-surrogate proof of concept.

An [independent dense KKT MILP comparison](../notes/bilevel-reopened-screening-computation.md)
subsequently tested `N=8,12,20,40`. The numerical MILP was faster on every
case: screened exact times were `0.098,0.296,0.933,17.569` seconds, versus
`0.024,0.038,0.156,0.404` seconds for the default numerical solves. All exact
outputs passed independent rational true-KKT and upper-feasibility checks.
The default `N=8` MILP had a roughly `3.4e-7` objective/feasibility discrepancy;
a targeted tighter-tolerance rerun resolved it to near machine precision. Both
records are retained. At `N=40`, four ambiguous coordinates and 2,304 completed
assignments made exact recovery the dominant cost. These results support the
mechanism and document negative speed evidence, not a computational advantage.

Representative application data, surrogate-rank/error sensitivity, and broader
solver comparisons remain empirical opportunities outside the verified theorem.
