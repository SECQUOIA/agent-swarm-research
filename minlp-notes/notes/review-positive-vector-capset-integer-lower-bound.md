# Independent audit of the cap-set graph-contact bound

Date: 2026-09-05. Verdict: PASS on
[the cap-set application](positive-vector-capset-integer-lower-bound.md).

The earlier two-thirds graph-contact obstruction excludes equal residues
modulo three. For three distinct residues with sum zero, the uniform
barycenter of their exact lifted graph witnesses has integer coordinates.
Putting one third of the mass on the smallest selected input gives the
same `2177/2144` error lower bound, because the other two selected inputs
each have the required Bernoulli lower estimate. This is a valid contradiction
for every integer dimension, auxiliary size, and ordering of residues.

In characteristic three, a solution to `a+b+c=0` with two equal entries has
all entries equal. Thus the distinct contact residues form exactly the
progression-free set required by Ellenberg--Gijswijt Theorem 4 with
`q=3` and all three coefficients one. I directly checked that theorem in
the [primary paper](https://arxiv.org/html/1605.09223); it gives the stated
factor-three monomial count at degree threshold `2p/3`.

For `0<t<1`, summing `t^(sum alpha_i-2p/3)` over the permitted multi-indices
and then over all of `{0,1,2}^p` yields the claimed finite Chernoff bound.
Differentiation gives `4t^2+t-2=0`, with unique minimizer
`(sqrt(33)-1)/8` in `(0,1)`. The explicit constant and the weaker rational
base `14/5` both check. The original paper's Corollary 5 also states the
corresponding base below `2.756`.

The small-dimensional consequence uses `cap(1)=2`, rather than the weaker
prefactor-three exponential estimate, so the exact `M=3` count is valid.
The note correctly makes no binary/general gap claim from this improved
lower bound and credits the finite-field theorem as imported. No correction
was required.
