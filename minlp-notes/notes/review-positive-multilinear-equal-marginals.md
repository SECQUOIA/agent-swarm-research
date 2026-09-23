# Independent review of the equal-marginal gap characterization

Date: 2026-09-04. Target:
[`results/positive-multilinear-equal-marginals.md`](../results/positive-multilinear-equal-marginals.md).
This is an independent agent review, not external peer review.
The reviewed theorem concerns positive multilinear polynomials on the unit cube,
evaluated at a vector whose coordinates all equal `u`, with `0<u<1`.

**Mathematical verdict:** The proposed exact finite-dimension characterization and
its dimension-free limit are correct. They imply that a termwise/convex-hull gap
ratio above two requires unequal coordinate marginals. The proof is a direct
combination of exchangeable subset rounding and discrete convexity. This review
does not make an independent literature-novelty claim.

## Exact finite dimension

Fix `n≥2`. For `2≤d≤n`, let `l=floor(nu)`, `θ=nu−l`, and define

\[
q_{n,d}=\frac{(1-\theta)\binom ld+\theta\binom{l+1}d}{\binom nd},
\qquad T_d=\min\{u,(d-1)(1-u)\}.
\]

Binomial coefficients with an upper nonnegative integer smaller than the lower
integer are zero. Choose a random integer `K∈{l,l+1}` with mean `nu`, then choose
a uniformly random `K`-element subset of the `n` coordinates. Each coordinate has
mean `u`; every fixed degree-`d` monomial has expectation `q_{n,d}`. This is one
common binary distribution for the entire polynomial, not a different coupling
chosen separately for each monomial.

For any positive multilinear polynomial with nonzero nonlinear part, its concave
envelope at this point is `u` times its total nonlinear coefficient, plus its
affine contribution. One common threshold attains all monomial upper envelopes
simultaneously. Applying the subset distribution gives hull gap at least
`Σ_e a_e(u−q_{n,|e|})`, while the termwise gap is `Σ_e a_e T_|e|`. Therefore

\[
\frac{\operatorname{tbtgap}f}{\operatorname{chgap}f}
\le \max_{2\le d\le n}\frac{T_d}{u-q_{n,d}}.
\]

Affine terms contribute no gap and may be removed. For multilinear polynomials,
vertex distributions suffice to calculate the envelopes: independently round
fractional coordinates conditional on the fractional point, preserving all
multilinear expectations and coordinate means.

For each fixed `d`, the complete degree-`d` polynomial has binary value
`binom(K,d)`. Its second forward differences are `binom(K,d−2)≥0`, so its
piecewise linear interpolation on integer counts is convex. Every distribution
with `E K=nu` therefore has expected cost at least the adjacent-integer
interpolation at `nu`. The subset construction attains that value with the
prescribed individual means. Consequently the displayed maximum is the exact
worst ratio in dimension `n`, attained by one complete uniform hypergraph
polynomial with unit coefficients.

## Comparison with independent rounding

Independent Bernoulli coordinates produce `K∼Binomial(n,u)` and monomial
expectation `u^d`. Discrete convexity gives `q_{n,d}≤u^d`. In fact the inequality
is strict for every `d≥2`, `n≥d`, and `0<u<1`: the binomial distribution has
positive probability at every integer count, and the convex piecewise linear
function `binom(K,d)` is not affine on the entire count interval. Its expectation
strictly exceeds its value at the mean. Thus `q_{n,d}<u^d<u`, and every denominator
in the finite theorem is positive.

Writing `k=d−1`, the comparison gives

\[
\frac{T_d}{u-q_{n,d}}
<\frac{\min\{1,k(1-u)/u\}}{1-u^k}.
\]

Let `t=k(1-u)/u`. Bernoulli's inequality yields
`u^(−k)=[1+(1−u)/u]^k≥1+t`, so `1−u^k≥t/(1+t)`. Hence

\[
\frac{\min\{1,t\}}{1-u^k}
\le\min\{1,t\}\frac{1+t}{t}\le2.
\]

The last expression equals two only at `t=1`, and equality in the preceding
Bernoulli step requires `k=1`. Thus the dimension-free upper expression equals
two only at `u=1/2`, `k=1`. Every fixed finite-dimensional ratio is strictly
below two, including at one-half.

## Exact dimension-free supremum and maximizing degrees

For fixed `d`, as `n→∞`, the adjacent counts divided by `n` converge to `u`, and
`q_{n,d}→u^d`. The complete degree-`d` polynomials therefore approach the preceding
bound. Taking the supremum over dimensions gives exactly

\[
M(u)=\max_{k\ge1}\frac{\min\{1,k(1-u)/u\}}{1-u^k}.
\]

Set `r=u/(1-u)`. Below `r`, the objective is proportional to
`k/(1−u^k)`, which increases strictly: `(1−u^k)/k` is `(1−u)` times the decreasing
average of `1,u,…,u^(k−1)`. Above `r`, the objective is `1/(1−u^k)`, which decreases
strictly. Hence only `max(1,floor r)` and `max(1,ceil r)` need be checked. This also
proves the maximum is attained at a finite integer degree. In particular,
`M(u)<2` unless `u=1/2`, while `M(1/2)=2` is approached by complete graphs of
increasing order. For a fixed maximum degree `D≥2`, restrict the same maximum to
`1≤k≤D−1`; the same fixed-degree limit argument applies.

## Independent arithmetic checks

Using exact rational arithmetic, the reviewer checked all `u=p/q` with
`2≤q≤30`, `1≤p<q`, all `2≤n≤24`, and all `2≤d≤n`: 120,060 finite `(u,n,d)` cases.
Every case satisfies `0≤q_{n,d}<u^d<u` and strict ratio below two. The same rational
means were used to compare all candidate integers `1≤k≤90` against the two
floor/ceiling candidates; the optimizer formula and equality characterization
passed. These checks supplement the general proof rather than replacing it.


## Final text and primary-source check

The final result text was read in full. Its finite-dimensional formula, unrestricted
supremum, convergence in dimension, floor/ceiling degree rule, and even-dimensional
midpoint example all agree with the independent derivation above. The only requested
clarifications were to exclude an identically zero nonlinear part from the ratio
optimization and state `2≤D≤n` for a degree restriction. The gap inequality itself
also holds for affine polynomials, whose two gaps are zero.

The reviewer independently opened [Sherali's original 1997
paper](https://math.ac.vn/uploads/files/9701245.pdf). Equation (13), printed page 252,
is the convex-envelope formula for the complete degree-`d` polynomial on the whole
unit cube. Theorem 3, printed page 253, proves that formula. Substitution of
`Σx_i=nu` gives the adjacent-count interpolation used here. This supports the
result's explicit classification as a classical consequence, rather than a new
elementary-symmetric envelope theorem.
