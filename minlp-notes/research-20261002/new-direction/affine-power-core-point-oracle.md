# Full point output with an explicit affine-power convexifier

Date: 2026-10-02. Status: complete, with a
[fresh independent review](../reviews/affine-power-core-point-review.md)
finding no substantive gap. This is an explicit-certificate extension of the
[cubic completion](cubic-core-full-point-oracle.md). Scalar uniform
convexity and the Hoffman bound are classical ingredients. The broader
[globally convex polynomial theorem](globally-convex-polynomial-point-oracle.md)
has also passed independent review, making this a concrete certificate
class with a separate direct proof. No priority claim is made here.

Fix a degree bound `d>=2`. Let `P` be a nonempty bounded rational
polytope in continuous coordinates `x=(v,z)`, with `v in [0,1]^k`
and a supplied rational bounding box. Supply the exact representation

```
G_alpha(x)=F_0(x)+(alpha/2)||v||^2
 = b+ell'x+(1/2)x'Qx+sum_j w_j(a_j'x-b_j)^(p_j),       (1)
```

where `alpha>=0`, `Q` is rational PSD, `w_j>0` is rational, and each
`p_j` is even with `2<=p_j<=d`. Zero-weight terms may be discarded.
All data, rational noise half-width `sigma>0`, and the representation
belong to the input length `I`.
Equality of the fixed-degree polynomials and PSD of `Q` are verifiable
in polynomial time. Thus (1) is a concrete convexity certificate,
not a promise of recognizing every convex polynomial.

For core noise `F_c=F_0-c'v` drawn from the fixed finite law of the
[coupled selected-core oracle](coupled-polytope-core-oracle.md), let
`a` be the lexicographically first optimal core and `S_a` its global
optimal fiber. There is an evaluator returning a rational feasible
point within `2^-q` of the minimum-original-Euclidean-norm point of
`S_a`, with expected work

```
f_d(k)(1+alpha/sigma)^k poly_d(I+q).                    (2)
```

One random work factor governs every precision query and every atom
is correct. The same law is used for all queries. The conclusion is
point-distance Cauchy output, not exact active labels or short expanded
algebraic coordinates. The zero-core case is deterministic polynomial
minimum-norm evaluation of (1). With `alpha=0`, the selected-core
interface can use the sharper
[jointly convex theorem](joint-convex-core-point-oracle.md), giving
ordinary expected polynomial work even when all coordinates are selected.

## 1. Scalar curvature and a rational description of the optimal fiber

For even `p>=2` and real `s,t`,

```
t^p-s^p-p s^(p-1)(t-s) >= 2^(2-p)|t-s|^p.             (3)
```

Indeed the monotonicity inequality for `|t|^(p-2)t` is
`(u^(p-1)-v^(p-1))(u-v)>=2^(2-p)|u-v|^p`.
It follows by minimizing the integral of `(p-1)|t|^(p-2)` over an
interval of prescribed length at its centered position. Integrate
the corresponding inequality for the derivative of `t^p` along the
segment from `s` to `t`; the factor `p` cancels the integral of
`theta^(p-1)`. This proves (3), including the quadratic case.

Assume `k>=1`. Set `beta=alpha+1` and

```
T_a(x)=F_c(x)+(beta/2)||v-a||^2.
```

This is convex because it equals `G_alpha+||v||^2/2` plus an affine
function. Its minimum is `f*=min_P F_c`, and its optimizer set is
exactly `S_a`. For `y in S_a`, write `u=x-y` and
`Delta=T_a(x)-f*`. Constrained first-order optimality, (3), and the
quadratic Bregman identity give

```
Delta >= (1/2)u'Q u+sum_j w_j 2^(2-p_j)|a_j'u|^(p_j),
Delta >= (beta/2)||v-a||^2.                            (4)
```

Let `E` denote the coordinate-selection matrix `Ex=v`. Then

```
S_a={x in P: Q(x-y)=0, a_j'(x-y)=0 for all j,
                  ell'(x-y)=0, E(x-y)=0}.              (5)
```

Necessity follows from (4); after the quadratic and power terms and
the core agree, objective equality forces the linear row to agree.
Conversely these equalities preserve all terms in (1) and the core,
so they preserve global optimality. The coefficient matrix in (5)
is rational and known. Its possibly irrational right-hand side is
used only in analysis. This is the key protection against an unknown
irrational core appearing in the error-bound matrix.

## 2. Explicit polynomial-bit error constants

Choose rational bounds

```
R>=max(1,sup_P ||x||_2),
M=max(1,max_i sum_l |Q_il|),
B_j>=max(1,sup_P |a_j'x-b_j|),
C_j=max(1,2^(p_j-2)/w_j),
K_j=w_j p_j B_j^(p_j-1),
N=k(beta+sigma).
```

The supplied coordinate box gives `R,B_j` directly. For `Delta<=1`,
equation (4), PSD of `Q`, and `p_j<=d` imply

```
||Q u||_2 <= 2M Delta^(1/d),
|a_j'u| <= C_j Delta^(1/d),
||E u||_2 <= 2 Delta^(1/d).                            (6)
```

For example, `||Qu||^2<=M u'Qu<=2M Delta`; roots and coefficients
are overbounded rationally in (6). Powers of `Delta` can be weakened
to `1/d` because `0<=Delta<=1`.

Write `T_a` using the quadratic matrix `Q+E'E` and linear slope
`ell-E'(beta a+c)`. The difference of its quadratic values is at
most `R(||Qu||+||Eu||)` in absolute value. The `j`th power difference
is at most `K_j|a_j'u|`, and `||beta a+c||<=N`. Hence

```
|ell'u| <= C_lin Delta^(1/d),
C_lin=1+R(2M+2)+sum_j K_j C_j+2N.
```

Let `A_*` stack the rows of `Q`, all `a_j'`, `ell'`, and `E`, and set
`C_res=2M+sum_j C_j+C_lin+2`. Then
`||A_*u||<=C_res Delta^(1/d)`.

Write `P={x:C_P x<=b_P}`, in ambient dimension `n>=1`. Clear all
denominators of `A_*` and `C_P` by a positive integer `D`, and let
`C>=1` bound the absolute entries of both integer matrices. The
[polyhedral Hoffman bound](convex-cubic-polytope-point-oracle.md#4-the-affine-slice-and-the-general-polytope-hoffman-constant)
is uniform in the equality right-hand side, including redundant rows
and lower-dimensional domains. Therefore

```
dist(x,S_a) <= Gamma Delta^(1/d),
Gamma=max(1,(nC)^(n-1) D C_res),    0<=Delta<=1.        (7)
```

Every displayed constant is rational, computable in polynomial time,
and has polynomial binary length for fixed `d`. Only the known noise
support enters the constants; they are uniform over every selected
core and every atom. Large numerical weights or small positive weights
affect precision bits, not a numerical condition parameter in (2).

## 3. Short-core completion and a fixed full-point selector

Put `epsilon=2^-q` and choose

```
tau=epsilon^(2d-2)/(2^(3d) R^d Gamma^d),
eta=tau epsilon^2/8,
delta=tau epsilon^2/(32 beta k).                        (8)
```

Let `p` be the minimum-norm point of `S_a` and let `x_tau` minimize
`T_a+tau||x||^2`. Comparison with `p` gives `||x_tau||<=||p||<=R`
and unregularized gap at most `tau R^2<=1`. For the nearest point
`s in S_a` and `e=||s-x_tau||`, (7) yields

```
e^d/Gamma^d <= T_a(x_tau)-f* <= 2R tau e,
||x_tau-p||^2 <= 2R e.
```

Thus `e<=(2R tau Gamma^d)^(1/(d-1))<=epsilon^2/(8R)`
and `||x_tau-p||<=epsilon/2`. The zero-distance case is immediate.

Request core-oracle error at most `delta/2`, then round to a dyadic mesh
with Euclidean rounding error at most `delta/2` and clip to the unit box.
This supplies a short rational `b in [0,1]^k` with `||b-a||<=delta`.
Minimize the explicit convex polynomial

```
G_alpha(x)+(1/2)||v||^2-(beta b+c)'v+tau||x||^2
```

over `P` to feasible objective gap `eta`. Replacing `b` by `a`
changes values uniformly by at most `beta sqrt(k) delta`, so the
returned point's gap for the exact regularized target is at most
`eta+2 beta sqrt(k) delta<=tau epsilon^2/4`. Strong convexity of
the norm penalty gives the remaining point distance `epsilon/2`.

All requested precision lengths are `poly_d(I)+O_d(q)`. As in the
cubic bridge, round the core oracle's output to a short dyadic vector
before completion, including on its exact fallback branch. Completion
does not require consuming an exponentially long algebraic record.
The core oracle's single random work factor is therefore inherited by
the full-point evaluator. An objective-gap certificate can be added by
tightening point accuracy using a coefficient gradient bound and calling
the same-law value oracle.

For the deterministic zero-core case, repeat (4)--(7) without `E`,
the completion penalty or the noisy tilt. The rational slice uses only
`Q`, the affine-form normals and `ell`. Use only `tau` and `eta` from (8); `delta` is neither defined nor needed
when `k=0`. The same regularization argument then approximates the global
minimum-norm optimizer in polynomial time.
Singleton domains and zero ambient dimension are handled directly.

## Scope and verification

This explicitly represented class includes quartic and higher even-power
terms with dense rational affine forms and arbitrary rational linear
coupling in `P`. It does not cover every polynomial convex on a box.
In particular the reviewed quartic point-extraction constructions are
not automatically positive affine-power decompositions. The weights and
affine forms are fixed rational data, not functions of other decision
variables. The representation is a sufficient certificate,
not a decomposition algorithm.

The same limitation on physical core normalization as in the coupled
value theorem applies. Exact boundary labels and expanded algebraic
output are not consequences. The result is a concrete certificate class
of the reviewed globally convex polynomial point theorem.

The independent actual-file review passed the scalar bound, rational
optimizer slice, explicit error constant, canonical rate and fixed-law
composition. Its two precision/zero-core wording clarifications are
applied. The reviewer did not duplicate the diagnostic below.
The distinct exact diagnostic
[check_affine_power_point_bounds.py](check_affine_power_point_bounds.py)
was run with `python3 -B research-20261002/new-direction/check_affine_power_point_bounds.py`.
It passed 2,500 scalar Bregman inequalities, 16 rational root bounds
including 101-bit small weights, and 252 completion budgets through
80-bit requests. It tests the new scalar and precision constants, not
a general convex solver or the inherited core-search algorithm. Source
questions were routed to the literature reviewer. Scoped local-link, fence, whitespace, control-character and checker
syntax checks passed, as did a topic-only `git diff --check`. No new
research directions, index edits or project-wide checks are part of
this work.
