# QCQP multiplicity thresholds: resolved in later literature

Status: literature resolution, not a new theorem. Investigated 2026-09-04 by
`review_scaling_characterization`. The elementary alternative proof and strict-feasibility
example below were independently checked by `review_fbbt`; they are retained as
explanatory material.

## What happened to the open question

The local paper [[wang2021-on-the-tightness-of-sdp]] p.30, Remark 14, conjectured
sharpness of three sufficient multiplicity thresholds: `k >= m+2` for the full
epigraph hull, `k >= m+1` for its optimal face, and `k >= m` for objective value.

The later paper by the same authors already improves the full hull threshold to
`k >= m`. See Wang and Kılınç-Karzan, *On semidefinite descriptions for convex hulls
of quadratic programs*, Operations Research Letters 54 (2024), 107108,
[DOI](https://doi.org/10.1016/j.orl.2024.107108),
[primary PDF, Section 4.1 and Remark 5, pp.8–9](https://arxiv.org/pdf/2403.04752).
The PDF identifies itself as arXiv:2403.04752v2, 20 March 2024. The v1 HTML puts
the application in Appendix B.2 instead, so section numbering must be tied to the
version. The PDF's Remark 5 expressly states the improvement over the previous
`m+2` hull bound and Beck's value result.

The displayed formulation in the 2024 paper uses inequalities. For mixed equality
and inequality constraints, the alternative proof below applies Beck's explicit
mixed-constraint theorem with `m` equal to the total number of constraints; it
does not replace each equality by two inequalities.

Consequently, under the original feasibility and positive-definite Lagrangian
assumption, all three guarantees hold at `k >= m`. Optimal-face exactness follows
from full hull exactness: in a finite convex decomposition of a point at the
minimum epigraph height, every positive-weight component must have that height.
The original Proposition 2, p.22, already gives value-gap examples at `k=m-1`.
Thus the threshold common to all three guarantees is sharp. This research target
should not be treated as an unresolved conjecture or a new discovery here.

## A short alternative route from value exactness

The following argument was developed during the search before the 2024 resolution
was located. It may be useful for transferring other objective-uniform exactness
results to hull exactness; no novelty is asserted.

Let `F` be the nonempty QCQP feasible set and

\[
D=\{(x,t):x\in F,\ q_0(x)\le 2t\}.
\]

Write `q_i(x)=x^T A_i x+2b_i^T x+c_i`. Suppose there are multipliers
`gamma_i`, nonnegative on inequality constraints, such that

\[
A_0+\sum_i\gamma_i A_i\succ0.
\]

The Lagrangian `q_0+sum gamma_i q_i` is a coercive quadratic and is bounded above
by `q_0` on `F`. Therefore constants `a>0,b` exist with

\[
t\ge a\|x\|^2-b\qquad ((x,t)\in D). \tag{1}
\]

**Closedness of the finite hull.** Translate `t` so that (1) reads
`t>=a||x||^2`. Represent each term of a convergent sequence in `conv(D)` by at
most `N+2` points of `D`, using Carathéodory. Extract a subsequence on which all
weights converge. Bounded average heights imply bounded `lambda_j t_j` and
`lambda_j ||x_j||^2`. A component whose weight tends to zero therefore satisfies
`lambda_j x_j -> 0`. For positive limiting weights, the component points are
bounded and have subsequential limits in the closed set `D`. Extract also limits
of each `lambda_j t_j`. The vanished components leave only nonnegative vertical
slack. The positive limiting weights sum to one; increase the height of any one
of their epigraph points by that slack divided by its positive weight. This
represents the limit as a finite convex combination
in `D`, proving that `conv(D)` is closed.

Assume now all Hessians have a common form `A_i=I_k tensor bar(A_i)` and `k>=m`.
For every `v` and `epsilon>0`, the objective

\[
v^Tx+\epsilon q_0(x)/2
\]

has the same repeated-block structure. Multiplying the original multipliers by
`epsilon/2` preserves the positive-definite Lagrangian condition. Hence Beck's
Corollary 4.4 applies to this perturbed problem: its QCQP and standard Shor SDP
values agree. This corollary explicitly permits both equality and inequality
constraints. See [Beck, *Quadratic Matrix Programming*, SIAM J. Optim.17 (2007),
Corollary 4.4, p.1236](https://www.tau.ac.il/~becka/14.pdf).

For completeness, these equalities of supporting values force full hull
exactness without assuming that all separating hyperplanes have positive
epigraph coefficient. If `z` in `D_SDP` were outside the closed convex hull,
strict separation would give `v^Tx+beta t >= eta` on `D` but a strict violation
at `z`. Upward closure forces `beta>=0`. If `beta>0`, the perturbed-value
exactness just proved is a contradiction. If `beta=0`, use the uniform bound
`t>=-b`: for sufficiently small `epsilon>0`,

\[
v^Tx+\epsilon t\ge\eta-\epsilon b\quad\text{on }D
\]

still strictly separates `z`. This again contradicts perturbed-value exactness.
Thus `conv(D)=D_SDP`.

## Sharpness with all inequalities and strict feasibility

For any integer `k>=1`, consider the `k`-variable QCQP with `m=k+1` constraints

\[
\min\left\{-\|x\|^2-2\sum_{j=1}^k x_j:
\ \|x\|^2\le1,\ x_j\le0\ (j=1,\ldots,k)\right\}. \tag{2}
\]

All Hessians are scalar multiples of `I_k`, so the quadratic eigenvalue
multiplicity is exactly `k` (the total dimension is `k`). Taking multiplier `2`
on the ball constraint gives the positive definite aggregated Hessian `I_k`.
The original feasible set has a strict feasible point: set every coordinate to
`-eta` for sufficiently small positive `eta`.

Put `r=||x||`. Feasibility gives `0<=r<=1` and

\[
-\|x\|^2-2\sum_jx_j=-r^2+2\|x\|_1
\ge-r^2+2r\ge0,
\]

with equality only at `x=0`. Thus the original optimum is uniquely attained at
zero and has value zero. In the Shor relaxation the objective is
`-tr(X)-2sum_j x_j`, with `tr(X)<=1`, `x<=0`, and `X>=xx^T`; its value is at
least `-1`. The choice `x=0`, `X=I_k/k` attains `-1`. Moreover, the lifted SDP
has a strictly feasible point: take `x=-eta*1` and `X=xx^T+tau I_k`, with
positive `eta,tau` satisfying `k eta^2+k tau<1`.

This elementary variant of the original sharpness construction shows that the
gap at `k=m-1` persists with only inequalities, nonempty feasible interior, and
strict primal SDP feasibility. Its smallest instance is one variable and two
inequalities. It is explanatory material, not a claim of a new counterexample
class.

## Search record and boundaries

The search checked the original paper, Beck's 2007 primary PDF, the 2021 INFORMS
tutorial, the 2024 paper above, the earlier preprint *A geometric view of SDP
exactness in QCQPs and its applications*, and bibliographic leads to the 2025
paper *Extending Exact SDP Relaxations of Quadratically Constrained Quadratic
Programs*. Exact keyword searches alone initially missed the 2024 result because
its QMP application does not use the phrase “quadratic eigenvalue multiplicity.”
Reading the application section resolved the question. Do not infer an open
problem from the continued availability of the older conjecture.
