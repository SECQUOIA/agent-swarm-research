# Independent review: relative power graph obstruction

Date: 2026-09-05. Reviewer: binary_formulation_review.
Target: `notes/relative-power-graph-integer-obstruction.md`.
Conclusion: PASS. The statement for q>1 is correct for every finite
nonnegative relative tolerance and any finite integer dimension.

## Mathematical audit of the convex-power statement

For any q>1 and finite epsilon, an integer M satisfying
M^(q-1)>2^q(1+epsilon) exists. Among M^p+1 selected exact graph lifts,
two integer vectors have equal residues modulo M. Their difference
divided by M is integral even for negative or unbounded integer values.
Therefore the convex combination with weights 1/M and 1-1/M is feasible
for the original mixed-integer lift.

The geometric sequence gives x/y<=1/M. Its projected input satisfies
0<u<=2y/M<=1, and its projected output is at least y^q/M. Thus the
relative ratio is at least M^(q-1)/2^q, strictly exceeding 1+epsilon.
This uses only the upper output requirement; allowing arbitrarily large
underestimation does not resolve the contradiction.

The proof requires no closure or measurability, and no limit lift at
x=0. Including the endpoint cannot help, because restriction to positive
inputs already produces the finite witness. The proof includes p=0,
where any two graph points have the unique empty residue vector.

The statement about [a,1] with a>0 and epsilon>0 is correct: an absolute
error target epsilon a^q gives the required relative error. The note
correctly excludes zero error from this recovery statement and correctly
distinguishes epigraph-only representations from the graph requirement.

## Source comparison

The local primary package was read directly:
[[lubin2022-mixed-integer-convex-representability]] p.12, Lemma 4.1.
Its proof groups integer graph lifts by parity, then uses convexity and
an integral midpoint. The present proof uses the same finite congruence
principle modulo M and a different rational convex weight. The note
correctly treats this as a supporting consequence rather than a new
integer-dimension method. The source's closed-lift convention is stronger
than the closure-free assumptions actually needed by this finite argument.

Targeted searches for relative power graph MICP approximation and residue
obstructions did not locate this precise statement. This limited negative
search does not establish priority. The source link and method attribution
were added to the supporting note.

## Added concave-power threshold

The q in (0,1) proposition was derived here, checked by the parent agent,
and added at the parent's request. Its normalization and exponents are
correct: choose M so M^(q-1)+M^(-q)<1-epsilon, then use geometric ratio
x/y<=M^(-2). The same integral convex combination has

```
v/u^q <= M^(q-1)+M^(-q)<1-epsilon.
```

This excludes every finite integer dimension when epsilon<1. For
 epsilon>=1, the hypograph slab 0<=w<=x^q is convex, contains the exact
graph, and has relative error at most one. The boundary epsilon=1 is
therefore attained with zero integers, not merely a limiting threshold.

## Optional broader growth condition

The q>1 proof also works for a positive differentiable function f on
(0,a] satisfying a uniform elasticity bound

```
x f'(x)/f(x) >= q_0 > 1.
```

Integrating the logarithmic derivative gives
`f(t y)<=t^(q_0) f(y)` for `0<t<=1`; the same condition makes f
increasing. Select x/y<=1/M and interpolate as in the power proof.
Then u<=2y/M and

```
v/f(u) >= f(y)/(M f(2y/M)) >= M^(q_0-1)/2^(q_0).
```

Choosing M sufficiently large gives the same impossibility for every
finite upper relative tolerance. This is a direct sufficient-condition
extension, not a necessary-condition characterization or a novelty claim.

## Truncated-domain supporting corollary

At the parent's request, the note now also records the order of integer
dimension on [a,1] for fixed q>1 and epsilon>0. The lower bound counts
N+1 admissible geometric inputs, N=floor(log_M(1/a)); all residues must
be distinct, giving M^p>=N+1. The contradictory interpolated input stays
in [a,1] because it is between its two selected inputs.

The binary upper uses geometric intervals with ratio at most
rho=(1+epsilon)^(1/q). The rectangle [l,u] times [l^q,u^q] contains
each graph segment and gives output ratio between 1/(1+epsilon) and
1+epsilon; both relative errors are at most epsilon. Thus no secant or
nonlinear lower constraint is needed. The number of intervals is
ceil(log(1/a)/log rho), and their logarithmic binary encoding yields
the upper order log log(1/a). All displayed counts and truncation at
the lower endpoint have been checked. The claim is only an order bound
with q,epsilon-dependent constants, not a matching leading coefficient.

## Independent scope check: products and fixed perspective scales

Date: 2026-09-05. Additional reviewer: `benders_review`. Verdict: PASS.
This check concerns only the affine-restriction corollaries in Scope;
it uses the already reviewed convex-power theorem.

For the product graph on `[0,1]^d`, intersecting a proposed convex lift
with `x_1=...=x_d=t` is an affine restriction. It adds no integer
coordinates, preserves convexity, and retains an exact graph lift for
every `0<t<=1`. Its output target is `t^d`; the proposed relative bound
becomes `|w-t^d|<=epsilon*t^d`. Taking `q=d>=2` gives the stated
contradiction. Bilinear multiplication is the case `d=2`. Only the
upper half of the error bound is needed.

For `w=x^2/s`, fix an admissible constant `s=s0>0` and set `W=s0*w`.
Both the slice and output transformation are affine, and
`|w-x^2/s0|<=epsilon*x^2/s0` is exactly
`|W-x^2|<=epsilon*x^2`. Thus the square theorem applies with unchanged
integer count. No new binary choice or integer encoding is introduced
by either operation.

These restrictions require the original domain to contain the selected
slice with numerator approaching zero, for example `0<x<=1` at the
fixed positive scale. The geometric inputs used in the proof would
also suffice. A domain bounded away from numerator zero, a product
domain without the diagonal sequence, or a perspective domain without
the fixed positive-scale slice is not covered by these corollaries.
Epigraph-only formulations are likewise outside the upper-relative-error
requirement. These are scope restrictions, not additional assumptions
on closure or the size of the continuous lift.
