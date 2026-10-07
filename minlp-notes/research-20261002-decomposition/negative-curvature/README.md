# Negative curvature: completed extensions and remaining scope

The second phase adds [integrated affine and convex recourse solvers](../completion/recourse.md)
and [curvature cancellation across piecewise responses](../completion/theory/piecewise-recourse/piecewise-curvature.md).
The latter can remove stiff curvature even when no global affine selector
exists, without overlaying the private partitions. These remain restricted
results with explicit private-block and curvature assumptions. Diagnostic
implementation descriptions below refer to the first release.

Date: 2026-10-02. The continuation proves two usable sparse-recourse
extensions and a complete affine-response recognition rule. **The general
algorithm parameterized only by original width and `nu/g` remains open.**
The additional structural and curvature assumptions below are essential.

## Completed results

1. [Certified affine convex recourse](affine-convex-recourse.md) removes
   arbitrarily stiff private PSD quadratic blocks exactly. Rational KKT
   identities certify the elimination, residual attachment scopes preserve
   a supplied decomposition, and full-vector growth transfers in the metric
   `I+sum B_t'B_t`. The existing filtered-grid theorem then gives exact
   parameterized optimization with residual width and residual coordinate
   curvature divided by growth. A checkable residual diagonal bound gives
   a `nu/g` corollary. The explicit ladder family has unbounded negative
   inertia and arbitrarily large original positive curvature at fixed
   residual width and conditioning.

2. [Affine-selector recognition](adversary/affine-selector-recognition.md)
   decides whether a private convex box-QP has any globally affine optimal
   response on its parameter box. It requires one exact central convex QP
   and one rational LP. The central gradient is common to every central
   optimizer, so its signs determine a sufficient KKT pattern even for
   singular Hessians and nonunique conditional optima. The procedure returns
   a polynomial-length rational certificate when one exists. A supplied
   partition into private blocks is still required.

3. [Sparse convex value factors](sparse-convex-value-factors.md) retain
   changing-active-set private convex QPs as exact local value oracles.
   Concavity of each value factor supplies the required upper-curvature
   bound without enumerating its pieces. The retained vector can have
   arbitrarily many coordinates. The proof includes rational arithmetic,
   unknown-growth filtering, certificate checking, and exact recovery from
   the original quadratic problem's rational-height bound. The controlling
   curvature is the direct retained quadratic diagonal. Certified affine
   blocks can be removed first to improve that diagonal.

Independent reviews found no substantive gap:
[affine reduction](adversary/affine-convex-recourse-review.md),
[recognition](reviews/affine-selector-recognition-review.md), and
[value factors](adversary/sparse-convex-value-factors-review.md).
These are research-agent reviews, not external peer review. The reductions
use classical KKT, parametric-QP, convex-oracle, and sparse-DP ingredients;
publication priority is not established.

## Boundaries checked

The [bit-serial conditioning audit](adversary/bounded-coefficient-hardness-conditioning.md)
shows that the existing bounded-coefficient width-two hardness construction
can have `nu/g>=4B`, even with a unique optimum. Increasing its positive
square penalties does not remove that obstruction. This is a limitation
of that particular reduction, not a tractability theorem or a hardness
proof at bounded `nu/g`. Its
[independent review](adversary/bit-serial-independent-review.md) checks the
source matching and the conditioning proof.

The [submodularity source correction](adversary/current-submodularity-boundary.md)
records that the early general submodular-QP SDP claim was corrected in
the current source version. It cannot serve as a general polynomial-time
recourse oracle. The existing
[unique-optimum scalar-message obstruction](../../research-20261002/new-direction/unique-message-growth-obstruction.md)
already rules out complete scalar-message enumeration at fixed width and
bounded `nu/g`; this continuation does not rediscover it as a new result.

## Targeted verification actually run

```sh
python3 -B research-20261002-decomposition/negative-curvature/check_affine_convex_recourse.py
python3 -B research-20261002-decomposition/negative-curvature/adversary/check_affine_selector_recognition.py
python3 -B research-20261002-decomposition/negative-curvature/adversary/check_bit_serial_conditioning.py
```

The first command passed eight affine certificates, 1,518 elimination
identities, five invalid-certificate rejections, 1,440 growth checks,
18 matrix cases, 13,320 changing-active-set local oracle checks, and
540 corner interpolation checks. Its
[saved output](check_affine_convex_recourse-results.json) records the scope.

The recognition command passed 15 fixtures: 11 affine selectors accepted
and four nonaffine responses rejected. Its reference enumeration covered
32 active patterns, and 205 exact KKT checks passed. The diagnostic uses
supplied verified central optimizers and a small exact Fourier–Motzkin
routine; it does not implement a production polynomial-time convex-QP or
LP backend. Its note records the rejected initial diagnostic backend and
the final successful runs.

The conditioning command passed 106 constructions, 954 weight cases,
and 11,332 residual checks, including `B=2^200`. Exact rational arithmetic
was used. Targeted Python AST, whitespace, and local-link checks also
passed. The theoretical algorithms are not claimed to be production
implementations; separate solver work evaluates actual affine condensation
on the stated family.

Only this topic's checks were run. No project-wide verification or CI
inspection was performed.
