# Independent review: finite-grid smoothing and exact bit complexity

Date: 2026-09-22. This review checks the proposed finite-grid extension of
[the scalar-message investigation](research-20260922-next-frontier.md) and
the previously reviewed
[exact block dynamic program](review-20260922-smoothed-block-dp.md).
It reconstructs the atomic-noise argument and the bit-cost argument. It does
not establish publication priority.

**Conclusion.** The proposed finite-grid envelope bound is correct. Together
with the reviewed dynamic program, it gives an exact algorithm with polynomial
expected bit complexity under the stated fixed graph and conditioning
parameters, rational input, and an inverse-polynomial perturbation scale.
The algorithm must keep one support representative for each identical full
quadratic formula. Deduplicating support labels alone is insufficient in the
presence of atomic noise. The proof below also removes an unnecessary term
from the auxiliary continuous-jitter estimate.

## 1. Precise envelope statement

Let `Z` be a nonempty subset of `{0,1}^m`, and let each deterministic
univariate quadratic `q_z` be `L`-Lipschitz on an interval `I` of positive
length `T`. Constants and affine functions are allowed as quadratics. Suppose
the independent noises satisfy the interval-mass bound

```
P(xi_i in J) <= phi |J| + tau
```

for every bounded closed interval `J`. Define

```
V(t) = min_(z in Z) [q_z(t)+xi dot z].
```

Count the maximal open pieces of the envelope after merging adjacent pieces
with the same polynomial formula and treating identical formulas as one.
Ignore formulas attaining the envelope only at an isolated point. Let this
count be `K`. The claim is

```
E K <= 1 + 2m phi L T + 4m 2^m tau.                 (1)
```

For `m=0`, the envelope has one formula and the bound holds directly.
Neither bounded penalty magnitudes nor convexity of the support quadratics
is required. A zero-length interval is handled separately by direct evaluation.

For a noise uniform on the `N>=2` equally spaced points of `[-sigma,sigma]`,
with both endpoints included and `sigma>0`, a closed interval of length `ell`
contains at most `ell (N-1)/(2sigma)+1` grid points. Therefore

```
P(xi_i in J) <= |J|/(2sigma) + 1/N.
```

Thus (1) gives the proposed constants `phi=1/(2sigma)` and `tau=1/N`.

## 2. Continuous jitter and monotonic arcs

Couple the noises with independent `U_i`, uniform on `[-1,1]`, and replace
`xi_i` by `xi_i^delta=xi_i+delta U_i`, where `delta>0`. These new noises have
densities and remain independent. Their interval-mass bound is still

```
P(xi_i^delta in J) <= phi |J| + tau.                (2)
```

Indeed, condition on `U_i` and apply the original bound to the translated
interval `J-delta U_i`. No enlargement of the interval is needed. The weaker
bound with an extra `2 phi delta` is also valid but unnecessary.

Fix a coordinate `i` for which both support classes are nonempty. Condition
on every perturbed noise except `xi_i^delta`, and set

```
h_i(t) = min_(z_i=0) [q_z(t)+sum_(j!=i) xi_j^delta z_j]
       - min_(z_i=1) [q_z(t)+sum_(j!=i) xi_j^delta z_j].
```

An envelope of `k` distinct full quadratic formulas has at most `2k-1` open
pieces. Identical formulas can be discarded first; the usual order-two
envelope bound then applies. The two classes together contain at most `2^m`
formulas. Taking the union of their breakpoints gives at most
`2^(m+1)-3` quadratic pieces for `h_i` when both classes are present. Splitting
each quadratic piece at its possible interior stationary point gives fewer
than `2^(m+2)` monotonic arcs. The slightly weaker count `2^(m+2)` is enough.

On a nonconstant monotonic arc, a prescribed level has at most one preimage.
The probability that the independent level `xi_i^delta` belongs to the closed
image interval of this arc is at most `phi` times the image length plus `tau`,
by (2). Flat arcs require separate treatment: hitting the constant value has
probability zero because `xi_i^delta` has a density. There are only finitely
many such arcs after conditioning. Shared endpoints can be counted more than
once, which only weakens the upper bound. Both class envelopes are
`L`-Lipschitz, so `h_i` is `2L`-Lipschitz and

```
sum_(nonflat arcs) length(image arc)
  = total variation(h_i on I) <= 2LT.
```

Consequently the conditional expected number of level hits is at most

```
2 phi L T + 2^(m+2) tau.
```

Every tie between distinct minimizing supports differs in some coordinate,
and is a level hit for the corresponding `h_i`. Summing over coordinates
bounds the expected number of tie points. This count is finite almost surely.
Between tie points, the minimizing support is constant. Hence the perturbed
piece count satisfies (1), uniformly in `delta>0`. The argument applies to
the full deterministic support family. It does not condition on a family
randomly selected by an earlier pruning step.

## 3. Lower semicontinuity at an atomic realization

Fix an original noise realization, possibly with persistent ties. Group its
support polynomials into classes of identical formulas. Select one interior
sample point from each of the `K` maximal distinct-formula envelope pieces.
The points can avoid every root of the differences of nonidentical formulas.
At each selected point, its winning formula class is then strictly below
every other class. Finiteness of the family and of the sample points gives a
positive common gap whenever a competing class exists.

The perturbation changes each support value by at most `m delta`, uniformly
in `t`. Therefore, for sufficiently small `delta`, every minimizer at a
selected point still belongs to its original winning formula class. This
holds for every choice of the bounded jitter variables, not merely with high
probability. Consecutive selected points came from different winning formulas.
Those formulas cannot differ by a nonzero constant: if they did, the higher
one could never win. Their difference therefore has a nonconstant part,
which additive jitter cannot remove. Thus the perturbed winning formulas at
consecutive selected points remain distinct. The perturbed envelope has at
least `K` formula pieces.

Along any sequence `delta_j` decreasing to zero, use the same original noise
and jitter variables. The preceding argument gives

```
K <= liminf_j K_(delta_j).
```

Fatou's lemma and the uniform continuous-jitter bound prove (1) for the
original atomic noises. There is no need to claim that support counts are
lower semicontinuous. They need not be the correct quantity when several
supports give the same polynomial.

## 4. Application to the exact block dynamic program

Keep the assumptions and allocation conventions of the reviewed algorithm:
positive diagonal entries between `d` and `D`, row diagonal dominance margin
`rho<1`, linear coefficients bounded by `C`, and biconnected blocks of size
at most the fixed constant `b`. For `C>0`, put

```
M=C/[2d(1-rho)],  I=[-M,M],  T=2M,  L=2rho D M.
```

Subtracting the boundary vertex's own terms leaves every full conditional
support quadratic `L`-Lipschitz on `I`. The invariant-interval and Schur
complement proofs from the previous review are unchanged by atomic noise:
the noises affect support intercepts, not continuous stationarity equations.

Choose one common grid size that is a power of two and satisfies

```
N >= 4n 2^n.
```

For every message with `m<=n` internal indicators,
`4m 2^m/N<=1`. Its expected number of formula pieces is consequently at most
`2+2n phi LT`. The expected number of retained distinct formulas plus the
inactive alternative is at most

```
A_grid = 3 + 2n phi LT = 3 + 8n phi rho D M^2.
```

At each pruning step, keep one complete support and reconstruction pointer
per identical full polynomial. This is exact: equal full support values are
interchangeable for every scalar boundary value. Descendants connect to the
rest of the graph only through that boundary, so selecting one representative
loses neither feasibility nor an optimal value. Supports touching only at an
isolated boundary value remain unnecessary by continuity.

Tie handling and representative selection must be deterministic functions
of the message's own subtree data. Then sibling message sizes are still
independent, because their noise sets are disjoint. The previously reviewed
first-moment construction argument gives the same coarse expected operation
bound with `A_grid` in place of the continuous bound:

```
O_b(n^2 A_grid^(b-1)).
```

This count includes arithmetic, exact comparisons, and quadratic-root
operations. The case `C=0` still reduces to zero continuous variables and
independent choices of negative indicator penalties.

## 5. Bit costs and the exact interpretation of polynomial time

Assume `Q,c,lambda,sigma` are rational input data whose numerators and
denominators have at most `B` bits. Use rational bounds to construct `I`.
Fixed rational parameter bounds suffice, or compute `d=min_i Q_ii`,
`D=max_i Q_ii`, `C=max_i |c_i|`, and
`rho=max_i sum_(j!=i)|Q_ij|/Q_ii` directly from the rational data. These
computed quantities have polynomial encoding size and preserve every fixed
uniform bound assumed in the runtime statement. A uniform grid draw
uses exactly `log_2 N=O(n+log n)` independent random bits, by drawing an integer
`k` uniformly from `0,...,N-1` and setting

```
xi_i = -sigma + 2sigma k/(N-1).
```

Every perturbed penalty therefore has polynomial bit length. The following
facts bound the cost of every operation uniformly over all grid outcomes.

1. Each retained full quadratic is the exact Schur-complement value for a
   support of the original rational problem. Clearing the original input
   denominators requires only polynomially many bits. Determinant formulas
   and the usual determinant magnitude bound show that every coefficient of
   every such support quadratic has bit length polynomial in
   `n,B,log N`. Principal matrices are nonsingular by strict diagonal
   dominance. The estimate holds even for supports not retained.
2. Use reduced rational arithmetic. A fixed-size block elimination and a
   vertex sum of at most `n` message contributions have polynomial-size
   intermediate numerators and denominators. These operations cannot create
   an unbounded tower of coefficient bit lengths, because the resulting
   full support coefficients have the preceding uniform determinant bound.
3. Each envelope breakpoint is an endpoint of `I` or a real root of the
   difference of two rational full quadratics. It is therefore a real
   algebraic number of degree at most two with polynomial-size defining
   coefficients. Store it by those coefficients and its root choice or an
   isolating interval. Comparing two such roots, deciding equality, and
   evaluating a quadratic sign on an overlap interval all take polynomial
   bit work. This can be done by fixed-degree root isolation or exact sign
   tests using a bounded number of squarings. Do not propagate arbitrary
   arithmetic expressions in old algebraic endpoints through later Schur
   complements: the complements act only on rational coefficients.
4. Support labels and backpointers have polynomial size. Once a root support
   is selected, solve its rational positive definite principal linear system
   to reconstruct a rational continuous optimizer. Penalty noise does not
   enter this linear system. Both the solution and the perturbed objective
   value have polynomial bit size.

Thus the expected bit cost is the displayed expected operation bound times
a polynomial in `n,B,log N`. For fixed `b,d,D,C,rho`, this is polynomial in
the input size and `1/sigma`. It is a polynomial expected Turing runtime in
the encoded input size when `1/sigma` is polynomially bounded in that size.
An exponentially small `sigma` specified with few bits does not satisfy this
last interpretation. The distinction must remain explicit.

The result optimizes the sampled finite rational perturbation exactly. It
does not, by itself, recover the original unperturbed optimizer. Nor does it
extend the scalar-separator construction to arbitrary bounded-treewidth
graphs.

## Verification record

This review independently reconstructed the monotonic-arc count, the atomic
interval-mass estimate, the continuous-jitter coupling, the lower
semicontinuity argument, formula representative pruning, sibling independence,
and rational/algebraic bit-size bounds. A temporary exact `Fraction` script,
run as `python /tmp/check_grid_smoothing_review.py`, checked 52,266 rational
grid-interval cases for `2<=N<=32`, and 5,150 atomic-budget cases for
`1<=n<=100` and `0<=m<=n`. All passed. These calculations test endpoint and
integer-rounding details; they do not establish the general envelope theorem
or algorithmic bit bound. Those conclusions rest on the written arguments.
No Lean proof, project-wide test, or new priority search was performed.
