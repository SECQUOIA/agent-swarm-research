# Core-only smoothing for bilinearly coupled convex integer flows

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/smoothed-bilinear-core-flow-review.md),
including a separate arithmetic check and exact affine-margin diagnostics.
It uses the arbitrary-boundary flow theorem, with a sharper affine chart
margin and cheaper certificate tests.

Consider

```
F_gamma(v,z)=phi(v)+sum_a psi_a(z_a)+v'Bz+gamma'v,
v in [0,1]^k,    z in Y,                                 (1)
```

where `Y` is a nonempty bounded integral network-flow set with binary-encoded
supplies and capacities. The rational matrix `B` is arbitrary. The explicit
rational polynomials `phi` and `psi_a` have fixed degree at most `d>=2`,
and each `psi_a` is convex on its native real interval. The core polynomial
may be nonconvex. Supply `L>0` with `partial_ii phi<=L` on the unit core
box. Include the valid model premises and rational `sigma>0` in the base
input length `I`.

The [general boundary theorem](smoothed-boundary-core-flow.md) applies to
this model. Here its stronger original work bound can be recovered: one
base-computable finite rational noise law, perturbing **only** `gamma`,
has `log M=poly_d(I)` and exact expected bit work

```
[8^k [3+(1+k/2)L/(2sigma)]^k+c_d^k] poly_d(I).             (2)
```

Core optima may lie on any face. Arbitrarily many tied flows may persist.
Every draw is solved exactly, using the same-draw fallback on exceptional
atoms. Output and `t`-bit refinement have bounds `c_d^k poly_d(I)` and
`c_d^k poly_d(I+t)` on every draw. Quadratic `phi` permits rational outputs.
The sampler uses the same endpoint-inclusive uniform grid as the general
theorem; no residual objective coefficient is perturbed.

The numerical curvature in (2) is determined by `phi`. Neither `B` nor
the capacities increases it. Those quantities still enter the input length,
the exact flow work and the base precision budget. This statement would
not be true for general nonlinear core/flow coupling: for example, a term
`v_i^2 z_a^2` can force `L` to grow quadratically with a native capacity.

## 1. Every flow chart is affine in the core

After fixing an integer flow, its forward marginal on arc `a` is

```
psi_a(z_a+1)-psi_a(z_a)+(B'v)_a.
```

Reverse marginals are affine as well. Shortest-path tree potentials are
therefore affine functions of `v`. Every adjusted unit marginal, every face
restriction, and every first outside-interval marginal in the
[optimal-flow face certificate](flow-optimal-face-certificate.md) is affine.
There is a base polynomial bound `H_0` on the numerator and denominator
bit lengths of their coefficients. Native labels have binary length bounded
by the input; fixed-degree evaluations and sums of at most `s` tree arcs
preserve that bound.

Within-interval identities are affine coefficient checks. The minimum of
an affine polynomial on a rational box is obtained by selecting one endpoint
per coefficient sign, in polynomial bit work. Thus none of these certificate
tests needs an algebraic box solver. For a core normal `i`, the derivative
cost on a flow is

```
s_i partial_i phi(c)+s_i gamma_i+s_i (Bz)_i.
```

Minimizing it over all tied flows is a linear-cost flow problem with
tightened arc bounds. The deterministic face certificate, including its
losing-flow penalty and proximity bound, is otherwise unchanged.

## 2. A polynomial-bit margin for affine charts

Let `p(x)=a+b'x` be a nonzero affine polynomial on `[0,1]^q`, `q<=k`,
whose rational coefficients have numerator and denominator bit lengths
at most `H_0`. Write `Z={p=0} intersect [0,1]^q`.

Suppose `Z` is nonempty and `p(x)>0`. A vertex minimizing `p` has value
at most zero. Move from `x` toward that vertex, one coordinate at a time,
stopping when `p` first reaches zero. Coordinates with zero coefficient
need not move. Along every moved coordinate, the value decreases at rate
at least

```
b_min=min_(i:b_i!=0) |b_i|>=2^(-H_0).
```

The total path length in the one-norm is at most `p(x)/b_min`. Its endpoint
belongs to `Z`; Euclidean distance is no larger than that path length.
The case `p(x)<0` uses a maximizing vertex. Hence

```
|p(x)|>=b_min dist(x,Z).                                 (3)
```

If `Z` is empty, `p` has a constant strict sign on the cube and its minimum
absolute value is attained at a vertex. A common denominator for its at
most `q+1` rational coefficients is at most `2^((q+1)H_0)`, so that positive
vertex value is at least `2^(-(q+1)H_0)`. This also handles nonzero constant
polynomials and vertex faces.

Use the general theorem's `delta<=1/4`. At distance at least `delta/2`
from `Z`, one uniform choice is therefore

```
mu_0=2^(-(k+1)H_0) delta/2.                              (4)
```

Its ordinary rational encoding has polynomial length in `I`. The argument
does not replace a small coefficient by a coefficient-free margin. It
explicitly pays for its binary height, which is enough to restore
polynomial precision.

## 3. Cutoff, work and output

The general theorem's facewise exceptional gradient images still involve
the possibly nonlinear core polynomial `phi`. Its analysis-only
fixed-dimensional elimination bound is unchanged. Only its logarithm
enters the algebraic tube coefficient and the initial `delta` budget, and
that logarithm is polynomial in `I`.

Replace the general value-margin bound by (4), and keep its three failure
events, normal margin, cutoff and finite-law construction. Now

```
J, log M=poly_d(I).
```

All ordinary flow queries and affine chart tests have polynomial bit cost.
Trying at most `3^k` faces per level is absorbed by the first term of (2);
the expected corrected-grid count remains exactly the same. The final
fixed-flow objective is `phi` plus a rational linear term and a constant.
One call to the reviewed constant-base polynomial box solver costs
`c_d^k poly_d(I)`, additively. The rare same-draw fallback contributes
polynomial expected work, while retaining a single winning small-core
representation. This proves (2) and the stated all-draw output bounds.

The result is exact for the sampled objective. Its deterministic
optimal-flow face certificates remain valid without randomness, but the
expected work theorem uses the specified finite core-noise law. The
[flow prior audit](../prior-art/smoothed-boundary-core-flow-prior.md) records
the classical flow and parametric ingredients; no publication-priority
claim is made for this corollary.

## Verification

The base flow certificate and its boundary search have separate exact
diagnostics and independent reviews. The [completed corollary review](../reviews/smoothed-bilinear-core-flow-review.md)
approved the restricted-cube affine margin, restored work/output bounds,
and quadratic-core rational specialization. A separate reviewer checked
the arithmetic transfer. Distinct exact checks passed 125 distance
inequalities and 50 empty-zero-set vertex bounds. Their executed command
and limitations are recorded in the review. No new generic algebraic solver
or full-law experiment is asserted here, and no project-wide checks were run.
