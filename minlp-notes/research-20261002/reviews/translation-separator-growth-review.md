# Review of the translation-separator dimension bound

Date: 2026-10-02. Reviewed
[translation-separator-growth.md](../new-direction/translation-separator-growth.md)
after its finite-difference proof and algorithmic caveats were written.

## Verdict

The bound

    n <= max{4p,8p^2 L/g}

is valid under the stated assumptions. I found no mathematical gap in the
biased-rounding argument, separator construction, component additivity,
distance estimate, or treatment of an empty separator. No twice
differentiability, convexity, or invariant off-box extension is needed.

This is a dimension obstruction. The note correctly distinguishes it from
a proved fixed-parameter algorithm in bit accuracy and makes no originality
claim. I did not perform an external literature search.

## Checks of the proof

A point strictly inside the feasible shift interval is strictly inside
every coordinate interval. Choosing `t` sufficiently small makes all
`-t/+kt` sign patterns feasible, as well as the component perturbation and
its translated counterpart. Their equality uses only feasible-pair
translation invariance. The argument does not require a uniform positive
lower bound on this available `t`: it cancels from the final inequality.

The weighted-centroid proof supplies components of size at most `n/2`.
Every variable outside the centroid bag has its entire bag subtree in one
remaining tree component, so its assigned unit weight is counted there.
When `n>4p`, accumulating graph components until reaching `n/4` cannot
exceed `3n/4`. There are enough outside vertices to do so.

No factor spans two components after removing the separator. Subtracting
the value of each factor at the optimum proves both component identities
exactly, even if individual factors are not nonnegative. It is the total
objective increment of each feasible component perturbation that is
nonnegative. Thus discarding components gives the required upper bound.

For separator size `k>=1`, a perturbation with probabilities `k/(k+1)` and
`1/(k+1)` at `-t` and `kt` has mean zero and variance `kt^2`.
Applying the one-coordinate semiconcavity inequality conditionally, then
averaging, costs `Lkt^2/2` per separator coordinate. Independence is enough
to preserve these moments during the successive coordinate roundings.
The expectation is at most `Lk^2t^2/2` in total.

All outcomes have nonnegative objective increment. The all-minus outcome
has probability `(1+1/k)^(-k)>1/3`; retaining it yields the stated bound
`3Lk^2t^2/2`. The non-strict probability bound used in the theorem is safe.
For `k=0`, translation gives a zero total increment directly, contradicting
positive growth of the nontrivial component union. No undefined probability
or division by zero is used in that case.

Distance to the optimal segment is at least distance to its full affine
line. The latter squared distance is
`t^2 |A|(n-|A|)/n`, whose minimum over the stated size range is
`3nt^2/16`. Combining this with the separator increment gives
`3gn/16 <= 3Lk^2/2`, hence exactly `n<=8k^2 L/g`. The separate `n<=4p`
case and the substitution `k<=p` give the displayed theorem.

## Scope and attempted counterexamples

The positive-length assumption cannot simply be dropped. For any even
`n=2m`, take the unit box and the unary-factor objective

    F(x)=sum_(i<=m) x_i + sum_(i>m) (1-x_i).

This objective is translation invariant because its slopes sum to zero.
Its unique optimum is `x*=(0,...,0,1,...,1)`, whose translation line meets
the box only at that point. Moreover,
`F(x)-f*=sum_i |x_i-x*_i| >= ||x-x*||^2`, so `g=1`, while `L=1` is a
valid upper coordinate-curvature bound and the factorization has `p=1`.
Arbitrarily large `n` contradicts the proposed dimension bound if the
positive-length assumption is removed. The obstruction is precisely the
loss of an interior optimum.

For smooth graph energies, the argument has the form of a separator test
for a Poincare inequality: move a large component union while paying only
for separator coordinates. The finite-difference proof establishes the
claim without identifying a Hessian at the optimum. This comparison does
not settle prior art.

Bounding dimension by parameters does not alone prove an algorithm with
uniform polynomial dependence on requested accuracy bits. A uniform-grid
cost `eps^(-O(n))` still fails that criterion. The source explicitly makes
the algorithmic consequence conditional on a separate refinement and
arithmetic result; that qualification is appropriate.

## Targeted checks actually run

The local commands were:

- `rg --files research-20261002/new-direction | rg 'translation-separator-growth|finite'`
- `rg --files research-20261002/new-direction | rg 'translation-separator-growth'`
- `cat research-20261002/new-direction/translation-separator-growth.md`
- One inline `python3 - <<'PY' ... PY` calculation using exact
  `fractions.Fraction` arithmetic, described below. It passed.

The exact calculation checked the mean, variance, and probability bound for
each integer `k=1,...,100`. It also used the nonconvex sparse quartic energy
on nine unit-box variables, with an edge between indices at distance one
or two, optimum `x*=(1/2,...,1/2)`, separator `{3,4}` in zero-based indexing,
and `t=1/32`. The remaining components are `{0,1,2}` and `{5,6,7,8}`.
Its valid curvature bound is `L=8`.

The calculation exhaustively enumerated the four `-t/+2t` separator
outcomes. It checked their feasibility, exact component additivity,
translation equality, the expectation bound, the all-minus-event bound,
and the distance estimate for the three-vertex component. The output was:

    PASS: 100 exact biased-rounding laws; sparse quartic separator decomposition, 4 sign corners, expectation bound, all-minus bound, and orbit-distance estimate

These finite checks support the algebra; the argument above establishes
the general statement. No project-wide verification, CI inspection,
performance measurement, or external search was run.
