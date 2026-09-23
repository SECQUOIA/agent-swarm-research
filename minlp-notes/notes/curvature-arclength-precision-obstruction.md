# Raw curvature arclength does not uniformly characterize graph precision

Date: 2026-09-05. Status: independently reviewed supporting obstruction.

An accuracy-independent curvature integral cannot replace the coefficient-sum
benchmark by itself, even for one positive polynomial on the unit interval.
It can grow without bound while a fixed number of integers suffices at a fixed
absolute tolerance.

Use the family

```
f_M(x)=(1/M)sum_(j=1)^M x^(2^j),
mathcal L_M=integral_0^1 sqrt(f_M''(x)) dx,
epsilon=1/16.
```

The following bounds hold:

```
mathcal L_M>=sqrt(M)/(4sqrt(2)),
p_conv<=p_bin<=4.                                     (1)
```

The upper is for finite real-coefficient linear formulations. Therefore
`log2(1+mathcal L_M/sqrt(epsilon))` can overestimate the true minimum integer
count by an unbounded amount. This does not dispute high-accuracy asymptotic
interpolation results for a fixed function, which have a different order of
quantifiers.

For the curvature lower bound, take `k=2^j` and the disjoint layer

```
I_j=[1-1/k,1-1/(2k)],      j=1,...,M.
```

On this layer the selected monomial contributes curvature at least
`k^2/(8M)`, by the same elementary bound as the reviewed
[allocation degree-gap example](positive-polynomial-allocation-degree-gap.md).
Its length is `1/(2k)`. Consequently

```
integral_(I_j) sqrt(f_M''(x)) dx >=1/(4sqrt(2M)).
```

Summing over the `M` disjoint layers proves the first inequality in (1).
For the upper bound, `f_M` is continuous, strictly increasing, convex, and
has range `[0,1]`. Partition that range into 16 equal pieces and use its
inverse images as knots. Each chord has error at most `1/16`, because both
the function and chord stay between their two endpoint heights. The bands
from chord minus `1/16` to chord cover the exact graph and admit only the
prescribed error. The 16 bands use four cell-index binaries in the finite
Hamming-distance formulation.

Any new curvature-sensitive benchmark must therefore include an accuracy-
dependent truncation or another way to merge many individually small
curvature contributions. A possible hybrid density is

```
min(sqrt(f''(x)/epsilon), (1-x)f''(x)/epsilon).
```

This density is analyzed in the separate
[accuracy-dependent curvature theorem](accuracy-dependent-curvature-precision.md),
which proves a finite characterization under nondecreasing curvature. Its
efficient integration and quantile computation remain separate questions.
The obstruction (1) applies to raw arclength, not to every adaptive measure.

The [first curvature audit](review-accuracy-dependent-curvature-precision.md)
and [second curvature audit](review-accuracy-dependent-curvature-precision-second.md)
both checked this supporting result and passed.
