# Removing a translation symmetry by coordinate faces

Date: 2026-10-02. Status: both algorithms and their bounds passed an
[independent adversarial review](../reviews/gauge-face-review.md), including
targeted exact-arithmetic checks. No external prior-art search or originality
claim is made. This note gives a precise alternative to covering a continuous
optimal set with coordinate anchors.

## Result and assumptions

Let `X=product_i[a_i,b_i]` be a continuous box, with fixed variables removed,
`n>=2`, and `s=max_i(b_i-a_i)>0`. Assume the factorization and upper coordinate
curvature bound `L>0` of [the grid theorem](../geometric-dp/theorem.md).
The supplied tree decomposition has bags of size at most `p`.

Assume translation invariance along the all-ones vector:

    F(x+t 1)=F(x) whenever both points belong to X.

Assume the optimal set is one translation orbit intersected with the box,

    S=(s0+span{1}) intersect X,

and global growth holds in distance to this set:

    F(x)-f* >= g dist(x,S)^2,     g>0.

Neither `s0` nor any point of `S` is supplied. Translation invariance is a
structural assumption, not a conclusion inferred from observed flatness.

Under these assumptions, a sequence of coordinate-face grid solves gives
accuracy `eps` with table work

    O((N+number of factors) n C^p theta^(-p) (J+1)^(p+1)),

where

    theta^2 <= min{1/(4n), g/(8Ln)},
    J=max{0,ceil((1/2)log2(7Ln s^2/(8 eps)))}.

Thus a continuous interval of optima does not force polynomial dependence on
`1/eps`. The construction preserves the original factor sparsity. Its costs
include `n` face solves per stage and a factor of `n` in the permitted ratio
`L/g`. In particular, this is not a uniform FPT claim in bag size with a
polynomial input exponent independent of that size.

## The face cover

Write `Q_j={x in X:x_j=a_j}`. For any `x in X`, subtract
`min_i(x_i-a_i)` from every coordinate. The resulting point stays in `X`,
belongs to at least one `Q_j`, and has the same objective value. Consequently,

    min_X F = min_j min_Q_j F.

Fixing one coordinate only restricts existing factors and removes a variable;
it introduces no interactions. Each face inherits upper coordinate curvature
at most `L`, and its decomposition has bag size at most `p`.

Define the affine gauge map and its linear part by

    A_j(x)=x+(a_j-x_j)1,       T_j=I-1 e_j^T.

The exact Euclidean operator norm of `T_j` is `sqrt(n)`. One proof is that
`T_j^T T_j` has nonzero eigenvalues `n` once and `1` with multiplicity `n-2`.
The map annihilates translations: `T_j 1=0`.

## Synchronized algorithm

Start from any feasible `z_-1`. At stage `k=0,1,...`, let `h_k=s 2^-k`.
For every face `j`:

1. Form `c_k^j=projection_Q_j(A_j(z_(k-1)))`. Projection is coordinate
   clipping, with coordinate `j` fixed to `a_j`.
2. Build the geometric grids of the grid theorem on that face, centered at
   `c_k^j`, with parameters `h_k,theta`.
3. Solve its corrected grid objective exactly, obtaining `LB_k^j`, a feasible
   minimizer `y_k^j`, and correction `D_k^j(y_k^j)`.

Select a face attaining the smallest `LB_k^j`, and set `z_k=y_k^j` and
`LB_k=LB_k^j`. Stop when `F(z_k)-LB_k<=eps`.

Every face lower bound is valid for its face. The face-cover identity makes
their minimum a valid lower bound for the original problem. Therefore

    LB_k <= f* <= F(z_k),       F(z_k)-LB_k=D_k^j(z_k).

## Aggregate estimate and proof

Put `r_k=dist(z_k,S)`. For the selected face `j`, choose nearest points
`s_new,s_old in S` to `z_k,z_(k-1)`, respectively. Their difference is a
multiple of `1`, so

    T_j(z_k-z_(k-1))
      =T_j((z_k-s_new)-(z_(k-1)-s_old)).

Because `z_k in Q_j`, projection onto `Q_j` cannot increase its distance
from the proposed center. Also `A_j(z_k)=z_k`. It follows that

    ||z_k-c_k^j||
      <= ||z_k-A_j(z_(k-1))||
      <= sqrt(n)(r_k+r_(k-1)).

This argument uses separate closest optima. The generally false inequality
`||z_k-z_(k-1)||<=r_k+r_(k-1)` is not needed.

The grid mesh estimate, with `n` as an upper bound on the number of free
coordinates, now gives

    D_k^j(z_k)
      <= L n h_k^2/4 + (Ln theta^2/2)(r_k^2+r_(k-1)^2).

Growth and the valid global lower bound give `g r_k^2<=D_k^j(z_k)`. Under
the displayed bound on `theta`, moving the current-error term to the left
yields

    r_k^2 <= (4L/(15g)) n h_k^2 + r_(k-1)^2/15.

Set `B=max{1,4L/(11g)}`. The initial estimate `r_-1^2<=n s^2` and induction,
exactly as in the grid theorem, imply

    r_k^2 <= B n h_k^2.

Also `r_(k-1)^2<=4B n h_k^2`, including at stage zero, so

    D_k^j(z_k) <= (L/4)[1+10n theta^2 B]n h_k^2.

If `B=1`, then `n theta^2 B<=1/4`. Otherwise it is at most `1/22`.
Consequently,

    F(z_k)-LB_k <= 7Ln h_k^2/8.

This proves the stopping level and table-work bound. Each face has at most
`C theta^-1(k+1)` grid values per free coordinate. Sum the `n` face costs
over stages through `J`.

## A second implementation: update only the selected face

When `eps` and an admissible `theta` are fixed, only the face currently
attaining the smallest lower bound needs to be updated. This variant gives
a separate direct termination proof and can reuse the other face results.

Use

    h=sqrt(eps)/(2sqrt(Ln)),
    theta<=min{1/2, sqrt(g/(nL))/2},
    R=sqrt(eps)/(sqrt(L)theta).

Initialize every face center at the lower corner `a`, and compute its grid
solve. Repeatedly select the face with smallest stored lower bound. Stop if
its correction is at most `eps`; otherwise recenter that face at its returned
point and recompute just its grid solve.

For analysis define the canonical optimal-orbit representative

    s^(j)=s0+(a_j-s0_j)1.

It need not belong to `X`; the algorithm never needs it. For `x in Q_j`,
the identity `x-s^(j)=T_j(x-s)` for every `s in S` proves

    F(x)-f* >= (g/n)||x-s^(j)||^2.

Write `r=||c^j-s^(j)||`, `d=||y-s^(j)||`,
`A=sqrt(Ln)h/2=sqrt(eps)/4`, `b=sqrt(L)theta/2`, and
`lambda=b/sqrt(g/n)<=1/4`. A selected solve satisfies

    sqrt(g/n)d <= sqrt(D(y)) <= A+b(d+r).

If `D(y)>eps`, this implies `r>R` and `d<r/2`. Hence every failed solve
halves the selected face center's distance to its fixed reference.

For any optimum `s in X`, its coordinate slacks `s_i-a_i` lie in `[0,s]`.
Their pairwise differences show `||a-s^(j)||<=sqrt(n)s`. Therefore, with

    m=max{0,ceil(log2(sqrt(n)s/R))},

there are at most `n m` failed selections and at most `n+n m` actual grid
solves. No favorable growth around the minima of nonoptimal faces is assumed.
A reference outside the box simply cannot keep attracting selected feasible
points indefinitely. For per-face coordinate count
`q0=O(1+theta^-1 log(1+theta s/h))`, table work is

    O((N+number of factors) n(1+m) q0^p).

The synchronized version has the simpler direct correspondence to the
existing theorem; the selected-face version can save repeated solves.

## Scope and obstruction to a naive quotient

For `F(x)=x^T Hx/2+q^T x+constant`, the structural identities
`H1=0` and `q^T1=0` certify translation invariance on all of Euclidean space.
However, a positive-length optimal translation orbit in a nondegenerate box
contains a full-box interior minimizer: any point strictly between the orbit
segment's endpoints has every coordinate strictly inside its interval. For
a quadratic objective, an interior minimizer forces `H` to be positive
semidefinite. An indefinite quadratic can therefore satisfy the assumptions
only when its optimal orbit intersects the box in a single point. The
continuous-manifold result does not establish new nonconvex QP capability.
Its nonconvex scope includes higher-degree objectives.

For example, on `[0,1]^2`, let `t=x_1-x_2` and

    F(x)=t^2-t^4/2.

The optimal set is the full diagonal. Since `|t|<=1` and
`dist(x,S)^2=t^2/2`, global growth holds with `g=1`. Upper coordinate
curvature is at most `L=2`, because each diagonal Hessian entry is
`2-6t^2`. The Hessian eigenvalues are `0` and `4-12t^2`; the latter is
negative when `|t|>1/sqrt(3)`. Thus the objective is nonconvex, although its
Hessian is not strictly indefinite. The theorem gives polylogarithmic
accuracy dependence despite the interval of coordinate projections of `S`.
This two-variable example also has an elementary one-dimensional quotient;
it illustrates the assumptions rather than a difficult solver instance.

A sparse graph family is

    F(x)=sum_{ij in E} [(x_i-x_j)^2-(x_i-x_j)^4/2],
    x in [0,1]^n,

for a connected graph with `n>=2`. Its optimal set is the diagonal, upper
coordinate curvature is at most twice the maximum degree, and growth holds
with `g=lambda_2/2`, where `lambda_2` is the smallest positive eigenvalue of
the unweighted graph Laplacian. These facts follow from
`F(x)>=sum_{ij in E}(x_i-x_j)^2/2` and orthogonal projection onto the
diagonal by the coordinate mean. The family is nonconvex: set one coordinate
to one and all others to zero; its second derivative in that coordinate is
minus four times its degree, and remains negative at nearby interior points.
This supplies graph-structured examples, while
retaining the explicit dependence on spectral conditioning.

Directly changing variables to coordinate differences would usually replace
the product box by coupled feasibility constraints. For example, on
`[0,1]^3`, the quotient coordinates `u=x_2-x_1`, `v=x_3-x_1` satisfy
`|u|<=1`, `|v|<=1`, and `|u-v|<=1`: their domain is a hexagon, not a box.
On a path in `[0,1]^n`, edge differences are feasible exactly when the range
of their prefix sums, including the zero prefix, is at most one. Equivalently,
every contiguous sum of edge differences must lie in `[-1,1]`. Requiring only
each prefix sum to lie in `[-1,1]` is insufficient. The face construction
avoids introducing these constraints by retaining the original coordinates
and restricting factors.

This does not imply that every difference formulation destroys sparsity.
With one fixed anchor, write `u_i=x_i-x_anchor` and keep the common shift
`t=x_anchor`, so the box constraints become `a_i<=u_i+t<=b_i`. Under the
stated within-box invariance, the quotient objective is well-defined on
feasible fibers. Evaluating it as `F(u,0)` can leave the original box and
requires an additional extension that is translation invariant there.
The quadratic identities above supply such a global extension. When a
globally invariant extension with the supplied factorization is available,
anchor-zero restriction
preserves the objective's sparse factorization, and adding the single shift
variable to every original bag increases bag size by at most one.
Eliminating `t` creates pairwise quotient feasibility inequalities;
retaining it leaves a flat direction and coupled constraints. Neither form
is a product-domain instance of the original grid theorem, even though both
are natural formulations for a general constrained solver. The theorem here
supplies the rate for coordinate-face solves, not a claim that elementary
gauge elimination or face fixing is new.

The factor `n` in the Euclidean gauge estimate is sharp: on the hyperplane
`x_j=0`, a vector with all other coordinates equal has squared norm `n`
times its squared distance from `span{1}`. This obstructs removing that
factor merely by tightening the same universal norm calculation. It is not
an algorithmic lower bound or proof that better curvature-aware gauges are
impossible.

This result is restricted to a supplied global affine symmetry and a single
optimal orbit. It does not handle an arbitrary curved optimal manifold,
several quotient optima, or general mixed integer gauges. Unknown-growth
search can repeat the synchronized algorithm with decreasing `theta` and
the same known stopping level `J`; the first admissible trial succeeds.

## Verification record

The [independent review](../reviews/gauge-face-review.md) checked both proofs,
including selection of nonoptimal faces, infeasible canonical references,
the zero-refinement case, solve counts, sparsity, and the revised scope.
It found no counterexample to either algorithm.

The review ran targeted inline Python checks using `fractions.Fraction`,
full geometric grids, actual adjacent-interval penalties, and exhaustive
corrected-grid minimization:

- Two-dimensional synchronized runs passed 96 stages, 192 face solves, and
  2,264 grid vertices, including four selections of nonoptimal faces.
- Nine two-dimensional selected-face cases passed 22 actual solves and
  346 grid vertices.
- A three-dimensional selected-face run passed five actual solves and
  3,989 exhaustive assignments, including a failed selection whose canonical
  reference was outside the box.

Assertions checked lower bounds, certificates, contraction and gap estimates,
strict halving, failure radii, termination, and solve-count bounds. The review
also checked explicit counterexamples to unqualified anchor-zero evaluation
and insufficient path-prefix feasibility tests. An initial harness failed
with an endpoint-indexing error before mathematical assertions ran; the
corrected harness produced the two-dimensional results above. The linked
review records the commands, data, and check limitations.

These finite rational examples support the algebra; they do not replace the
proofs or establish solver performance. No project-wide verification, CI
inspection, or external literature search was run for this result.
