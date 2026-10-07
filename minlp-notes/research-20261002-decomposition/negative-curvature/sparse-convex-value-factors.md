# Sparse search with exact convex value factors

Date: 2026-10-02. Status: a complete oracle composition theorem. This is a
companion to [affine convex recourse](affine-convex-recourse.md), covering
changing active sets. It does not provide its positive-curvature
cancellation without additional structure.

The retained nonlinear vector may have arbitrarily many coordinates.
The condition is bounded interaction width **after** private convex
blocks have been eliminated, together with growth and a bound on the
direct retained-coordinate curvature. Exact local convex solves replace
explicit piecewise-quadratic value functions.

## 1. Statement

Let `z` lie in a rational product box `Z`. For each `t`, let `y_t` lie
in its own nonempty bounded rational polytope `Y_t`; the private vectors
are disjoint. With rational data and `C_t` positive semidefinite, consider

\[
 F(z,y)=q_0(z)+\sum_t\left[
  \tfrac12y_t^TC_ty_t+y_t^TD_tE_tz+c_t^Ty_t\right].       \tag{1}
\]

Here `q_0` is a rational quadratic. Any quadratic terms involving only
`z` are included in `q_0`. The matrices `E_t` select attachment
coordinates. The feasible sets of the private blocks do not depend on
`z`, and there are no constraints joining distinct blocks. Their
dimensions may grow with the input.

Suppose a supplied tree decomposition on the retained variables has bags
of size at most `p`, and each attachment scope and each factor of `q_0`
fits in a bag. Let `I` include this decomposition and all rational data.
Assume a unique global optimizer `(z*,y*)` and global full-vector growth

\[
 F(z,y)-F^*\ge g\big(\|z-z^*\|^2+\|y-y^*\|^2\big),\quad g>0.       \tag{2}
\]

Let `H_0` be the Hessian of `q_0`. If some diagonal is positive, put
`L=max_i(H_0)_ii` and `kappa=max(1,L/g)`.

**Theorem.** There is a deterministic exact algorithm returning an
expanded rational optimizer in `f(p,kappa)(I+1)^C` bit operations.
A feasible rational point with a checkable additive gap at most `2^-q`
requires `f_1(p,kappa)(I+q+1)^C_1`. The polynomial exponents are
absolute. Neither `g` nor `kappa` is required as input. Certificate
validity does not rely on (2).

If every diagonal of `H_0` is nonpositive, endpoint DP with two retained
states per coordinate solves the problem exactly, without (2) or
uniqueness. With no retained variables, independent convex solves suffice.

This is an oracle extension of the existing
[filtered-grid theorem](../../research-20261002/new-direction/pruned-coordinate-grid.md).
It is not a claim that conditional convexity preserves an arbitrary
original decomposition. The attachment scopes and residual decomposition
are verified explicitly.

## 2. Value oracle and curvature

Define

\[
 \psi_t(v)=\min_{y\in Y_t}\left[
          \tfrac12y^TC_ty+y^TD_tv+c_t^Ty\right],\qquad
 V(z)=q_0(z)+\sum_t\psi_t(E_tz).                     \tag{3}
\]

Every rational query `v` is a convex rational QP with a fixed nonempty
bounded feasible polytope. Exact convex-QP optimization returns its value
and a rational attaining point in polynomial bit time. A local value
certificate consists of that point and rational nonnegative polyhedral
KKT multipliers; stationarity, feasibility, and complementarity verify
optimality because `C_t` is PSD. Singular Hessians, tied minimizers, and
lower-dimensional private polytopes are allowed. The exact oracle and
height facts are the same ones used in the
[existing convex-modulator theorem](../../research-20261002/new-direction/convex-modulator-qp.md).

For a fixed `y`, the dependence on `v` is affine. Consequently `psi_t`
is concave on all of its parameter space. Therefore

\[
 s\longmapsto V(z_1,\ldots,s,\ldots,z_n)-Ls^2/2
 \quad\hbox{is concave}.                            \tag{4}
\]

The private Hessians and the sizes of the cross coefficients do not enter
this upper-curvature constant. They still enter the input encoding and
the convex solves. No smoothness, fixed active face, or explicit list of
pieces is used. Formula (4) does not apply when private constraints depend
on the retained coordinates: a changing feasible set may create an upward
kink.

Private blocks are independent once `z` is fixed, so
`V(z)=min_y F(z,y)` and `min V=F*`. A reduced optimizer lifts to an
original optimizer, proving uniqueness of `z*`. Evaluating (2) at any
conditional optimizer gives

\[
 V(z)-F^*\ge g\|z-z^*\|^2.                          \tag{5}
\]

This bound does not require a Lipschitz response map. It also holds if
the conditional response is nonunique away from `z*`.

## 3. Why the approximate filtered solver still applies

The interpolation, corrected grid, min-marginal filtering, contraction,
and state-count arguments in the filtered-grid proof use only (4), (5),
and a sparse finite table of exact factor values. They do not use
quadraticity elsewhere. In particular, independent unbiased rounding of
retained coordinates preserves feasibility of `Z`, and gives the same
upper rounding error. A local oracle at every table state supplies the
value factors in (3). The two-pass tree DP then computes the corrected
grid minimum and coordinate min-marginals exactly.

The existing bound of

\[
 K\le100\theta^{-1}\lceil\log_2(n+2)\rceil          \tag{6}
\]

grid nodes per retained coordinate remains valid after filtering, with
the same capped trial scheme for unknown growth. Here `n=dim(z)` and
the successful trial has `theta^-1=O(sqrt(kappa))`. At each stage there
are at most `O((N+T)p K^p)` table operations and at most
`O(T K^p)` local convex-QP evaluations, where `N` is the number of bags
and `T` the number of private blocks. Constant-scope blocks need only one
evaluation. Reusing values is optional for this bound.

There are `O(poly(I)+q)` stages for gap `2^-q`. The elementary bound
`ceil(log_2(n+2))^p <=(C p)^p(n+2)` absorbs the logarithm to the power
`p` into a parameter factor times a polynomial input factor. This is the
same reason the original filtering theorem has an input exponent
independent of width.

There is one arithmetic detail beyond the polynomial-factor case.
Different active sets may give different denominators in the oracle
values; a single common denominator for all possible active sets is not
assumed. At stage `j`, each grid coordinate has bit length polynomial
in `I+j+mu K`, where `theta=2^-mu`. The exact convex oracle therefore
returns a value and primal/dual certificate of uniformly polynomial bit
length in these quantities. Every DP message entry is a sum of at most
the input number of factor values and unary corrections along a selected
assignment. Its denominator bit length is at most the sum of those
individual bit lengths. Thus all table values still have polynomial
encoding length. There is no sum over every table state in this bound;
minimization selects one candidate sum. This proves the stated
approximate bit complexity.

To check a recorded grid certificate, verify each queried local QP
value using its KKT certificate, then verify the ordinary finite-tree
messages and filtering history. To lift an incumbent, solve the private
QPs at its retained coordinates. The resulting original vector is
feasible and has exactly objective `V(z)`. This also handles a saved
incumbent that differs from the current corrected-grid minimizer.

## 4. Exact output uses the original quadratic problem

One must not apply a quadratic rational-height theorem directly to the
nonsmooth value function `V`. Instead, the **original** problem (1) is a
rational quadratic over a bounded rational polytope. Its unique optimum
is rational with a computable polynomial-bit height bound, by the
minimal-face KKT argument in the existing convex-modulator theorem.
Compute universal denominator bounds `R` for the coordinates of its
optimizer and `Q` for its optimum value, with `log R,log Q=poly(I)`.

Run the certified approximate solver at accuracies `epsilon=2^-q` for
`q=1,2,4,8,...`. Once the certified original-value interval has width
at most `1/(4Q^2)`, isolate its unique denominator-at-most-`Q` rational;
the original rational-height bound guarantees this is `F*`. Reconstruct
each retained coordinate in the radius `1/(4R^2)` window around the
retained incumbent. There is at most one denominator-at-most-`R`
rational in such a window. If any is absent, continue refining.

For a reconstructed candidate `z`, check its box membership and call the
exact local convex oracles to obtain a feasible original lift. Accept
only if its original rational objective equals the isolated `F*`.
Premature reconstruction is harmless. Equality is checked against the
optimum isolated by the independent grid bound, not against a guessed
growth estimate or a rounded floating-point value.

By (5), reconstruction succeeds as soon as

\[
 \epsilon\le\min\{1/(4Q^2),\ g/(32R^4)\}.           \tag{7}
\]

Indeed the retained incumbent is then within
`1/(sqrt(32)R^2)<1/(4R^2)` of `z*`. The required accuracy exponent is
`poly(I)+O(log(kappa))`, since `L` is positive rational input data and
`g>=L/kappa`. The doubling scheme preserves the parameterized bound.
All original coordinates are returned by the exact convex oracle at
the accepted retained vector. Its local KKT certificate plus the grid
value interval and rational-height bound certifies the original optimum.
Neither the nonsmooth value function's pieces nor their boundaries are
reconstructed. This proves the exact theorem.

## 5. What this adds to the negative-curvature direction

The theorem permits arbitrarily many retained coordinates, overlapping
attachment scopes, and active-set changes inside each private block.
Its complexity uses only the direct retained diagonal `L`, rather than
the private block curvature. It gives a `nu/g` corollary if a rational
`beta` with `nu<=beta<2nu` is computed for the original full Hessian and
the checkable condition `L<=C beta` holds with a class-wide constant `C`.
This condition is not automatic.

For a stiff square `M(y-z)^2`, the direct retained diagonal is `2M`,
even though its exact value factor cancels that curvature entirely when
`y=z` is feasible. The companion affine certificate identifies and
performs that cancellation. One may first condense certified affine
blocks, then leave other private convex blocks as value factors. The
same theorem applies to the resulting direct quadratic and remaining
scopes. Thus the two reductions combine without enumerating active sets.

These are standard exact convex recourse, concavity of an infimum of
affine functions, and sparse DP mechanisms. Their conditioned
filtered-grid composition and original-QP exact recovery are the claims
proved here. No publication-priority or practical speedup claim is made.

## 6. Targeted check

The changing-active-set portion of
[the exact checker](check_affine_convex_recourse.py) checks clipped convex
responses and KKT values at rational parameters, then independently
averages values at all corners of selected retained boxes and checks the
upper interpolation inequality with the direct quadratic curvature. The
response crosses lower-bound, interior, and upper-bound regimes. This
tests the additional factor-oracle contract; the existing filtered-grid
implementation and its DP tests are not duplicated here. The proof above,
not finite sampling, supplies the general oracle-composition theorem.

The targeted command actually run was

```sh
python3 -B research-20261002-decomposition/negative-curvature/check_affine_convex_recourse.py
```

It passed 13,320 exact local oracle checks and 540 corner interpolation
checks, in addition to the companion affine checks. Its
[saved output](check_affine_convex_recourse-results.json) records these
counts and the diagnostic scope.

The [independent review](adversary/sparse-convex-value-factors-review.md)
checked the proof, polynomial arithmetic, original-problem rational
recovery, and unconditional acceptance test. It independently reran the
expanded checker with the same passing counts. This is research-agent
review; it does not establish publication priority or solver performance.

No project-wide verification or CI inspection was run.
