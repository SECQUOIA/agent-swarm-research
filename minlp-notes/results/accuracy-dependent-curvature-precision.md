# An accuracy-dependent curvature measure for scalar graph precision

Date: 2026-09-05. Status: independently reviewed finite theorem.

For a convex twice continuously differentiable scalar function with
nondecreasing second derivative, a truncated curvature density characterizes
the number of chord intervals to a universal constant factor. Consequently
its logarithm characterizes the minimum integer count up to an absolute
constant. Unlike raw curvature arclength, the measure adapts to the requested
error tolerance.

This note is a finite theorem. It does not yet prove a polynomial-time
random-access algorithm for the metric quantiles, or a multivariate
whole-formulation extension.

## Statement

Let `f in C²([0,1])`, with `g=f''>=0` nondecreasing. For `epsilon>0`, define

```
A(x)=sqrt(g(x)/epsilon),
rho_epsilon(x)=min(A(x),(1-x)A(x)^2),
M_epsilon=integral_0^1 rho_epsilon(x) dx.
```

Let `N_epsilon` be the smallest number of intervals in a partition of
`[0,1]` such that each chord of `f` has vertical error at most `epsilon`
on its entire interval. Then

```
N_epsilon<=2M_epsilon+1,
M_epsilon<=24N_epsilon.                                (1)
```

Let `p_conv` and `p_bin` be the whole-graph approximation minima, at absolute
error `epsilon`, for arbitrary convex integer lifts and binary linear lifts.
The finite lifts may have real coefficients and unrestricted continuous size.
Then

```
log2(1+M_epsilon)-log2(49)<=p_conv<=p_bin
 <=log2(1+M_epsilon)+2.                                (2)
```

Thus (2) is a finite true-minimum benchmark to an absolute additive
constant. Efficient computation of its integral and quantiles is a separate
question; no polynomial-time computational model is assumed or proved here.

Positive polynomials with nonnegative coefficients on powers of degree at
least two satisfy all stated curvature assumptions. Arbitrary affine terms
do not change the density or chord errors.

## Interval mass controls its Taylor remainder

Fix an interval `[a,b]` and write

```
m=integral_a^b rho_epsilon(t) dt,
E=integral_a^b (b-t) A(t)^2 dt.
```

The normalized endpoint Taylor remainder is `E`. We claim

```
E<=m²+(3/2)m.                                         (3)
```

Split the interval into the sets where `z(t)=(b-t)A(t)` is below one and
at least one. On the first set,

```
(b-t)A(t)^2<=min(A(t),(1-t)A(t)^2)=rho_epsilon(t).
```

Its contribution to `E` is at most `m`.

For a point `t` in the second set, monotonicity gives `A(s)>=A(t)` for
`s>=t`, and `1-s>=b-s`. Therefore

```
m>=integral_t^b min(A(t),(b-s)A(t)^2) ds
  =z(t)-1/2.
```

This integral identity uses `z(t)>=1`. It gives `z(t)<=m+1/2`.
On this second set, `(1-t)A(t)>=1`, so `rho_epsilon(t)=A(t)`. Its
contribution to `E` is at most `(m+1/2)m`. This proves (3).

If `m<=1/2`, then `E<=1`. The chord error on `[a,b]` is no larger than
its endpoint Taylor remainder

```
f(b)-f(a)-f'(a)(b-a)=epsilon E,
```

because the function is convex and lies above its left-end tangent. Thus
any interval carrying density mass at most one half is admissible.
Partition the total mass into pieces of that size. Zero-density intervals
can be included without cost; if all mass is zero the function is affine.
This proves the first inequality in (1).

## A telescoping potential bounds the total mass

Now suppose an interval `[a,b]` has chord error at most `epsilon`. Its
midpoint Jensen gap `J` is also at most `epsilon`. Put `ell=b-a` and
`c=(a+b)/2`. The right half of the midpoint gap satisfies

```
J>=(1/2)integral_c^b (b-t)g(t)dt>=g(c)ell²/16.
```

The left part of its endpoint Taylor remainder obeys

```
integral_a^c (b-t)g(t)dt <=3g(c)ell²/8<=6J.
```

The right part is at most `2J`. Hence its normalized endpoint Taylor
remainder has the bound

```
E<=8.                                                (4)
```

Define the nonnegative potential

```
chi(x)=(1-x)A(x).
```

For every interval, regardless of admissibility, one has

```
integral_a^b rho_epsilon(t)dt
 <=chi(b)-chi(a)+2E+2sqrt(2E).                         (5)
```

To prove it, write `d=1-b`. First suppose `ell<=d`. Monotonicity gives
`m<=ell A(b)`. Thus

```
m-[chi(b)-chi(a)]
 <=2ell A(a)-(d-ell)[A(b)-A(a)]
 <=2ell A(a)<=2sqrt(2E),
```

where the last step uses `E>=ell²A(a)²/2`.

If `ell>d`, split at `b-d`. On the left part, `b-t>=d`, so

```
rho_epsilon(t)<=(1-t)A(t)^2<=2(b-t)A(t)^2.
```

Its integral is at most `2E`. The right part has length `d` and density
at most `A(b)`, so its integral is at most `dA(b)=chi(b)`. Therefore

```
m-[chi(b)-chi(a)]<=2E+chi(a)
 <=2E+2ell A(a)<=2E+2sqrt(2E).
```

This also covers `b=1`, where the right part has zero length. It proves
(5). By (4), an admissible interval has mass at most
`chi(b)-chi(a)+24`. Sum this inequality over an optimal partition.
The potentials telescope, with `chi(1)=0` and `chi(0)>=0`, giving
`M_epsilon<=24N_epsilon`. This proves the second half of (1).

## Comparison with arbitrary convex integer lifts

At most `2^p` parity supports cover the exact scalar graph's input domain.
Any two endpoint graph points in one support have midpoint Jensen error
at most `epsilon`; the same is true after closure by continuity. Replace
each support by its span interval. For a convex function, the chord gap
as a function of the interpolation parameter is concave and zero at both
endpoints. Its maximum is at most twice its midpoint value. Thus each
span interval has chord error at most `2epsilon`.

These finitely many intervals cover `[0,1]`. They can be trimmed to a
partition using at most the same number of intervals, with each partition
piece contained in one covering interval. Chord error cannot increase on
a subinterval, so

```
N_(2epsilon)<=2^p.
```

Pointwise, `rho_epsilon<=2rho_(2epsilon)`, because its square-root branch
scales by `sqrt(2)` and its linear branch by two. Applying (1) at doubled
accuracy gives

```
M_epsilon<=2M_(2epsilon)<=48N_(2epsilon)<=48*2^p.
```

Since `p>=0`, this yields the lower bound in (2).

For the upper bound, use an admissible partition with at most `2M_epsilon+1`
pieces. The band from each chord minus `epsilon` to that chord contains
all exact graph points in its interval and admits only the prescribed
error. The finite Hamming-distance disjunction uses `ceil(log2 N_epsilon)`
binaries. As `N_epsilon<=2M_epsilon+1<=2(1+M_epsilon)`, this proves the
upper bound in (2).

## Computational and research boundary

Raw arclength fails uniformly at coarse tolerance, as recorded in the
[explicit obstruction](../notes/curvature-arclength-precision-obstruction.md).
The linear branch of the present density can merge many individually
small curvature contributions. For example,

```
M_epsilon<=epsilon^(-1)integral_0^1(1-x)f''(x)dx
 =epsilon^(-1)[f(1)-f(0)-f'(0)],
```

which remains bounded at fixed tolerance for the normalized positive
polynomial obstruction family.

For a dense positive polynomial, the branch crossings solve
`(1-x)² f''(x)=epsilon`. The linear branch has an elementary polynomial
integral, while the other branch requires certified integration of a
positive algebraic function. This note does not supply a polynomial-time
quantified implementation of those integrals and their inverse quantiles;
the later [certified compiled-quantile construction](compiled-curvature-quantile-precision.md)
supplies it for densely encoded positive rational polynomials (see below).
The [compiled indexed-knot principle](../notes/compiled-rational-knot-formulations.md)
would produce a compact rational formulation if such a random-access
algorithm, with the necessary error slack, were established. Sparse huge
degrees require separate care.

This note does not prove a multivariate separable analogue: the potential
argument here is one-dimensional and telescopes over an interval partition,
whereas arbitrary convex lifts in higher dimension have general parity
supports. The note does not assume that this scalar argument automatically
gives a product covariance or supporting-scalarization theorem. The later
[separable extension](separable-convex-graph-linear-dimension-precision.md),
described below, covers scalar sums and independent outputs by a different
argument; neither result covers arbitrary coupled multivariate outputs.

The [bounded source audit](../notes/accuracy-dependent-curvature-precision-novelty.md)
credits existing accuracy-dependent local mesh integrals, convex regression
secant moduli, and the chord/midpoint comparison. It found no matching explicit
minimum density with a finite constant-factor interval count under monotone
curvature, or the resulting whole-formulation integer benchmark. Publication
priority remains unestablished.

The [first independent audit](../notes/review-accuracy-dependent-curvature-precision.md)
and [second independent audit](../notes/review-accuracy-dependent-curvature-precision-second.md)
both passed, including the raw-arclength obstruction and the separate scalar
two-bit corollary. The [checker](../code/quadratic_rank/check_accuracy_dependent_curvature.py)
passed 140 exact Taylor/midpoint identities and 420 branch-split numerical
interval-mass/potential checks. Numerical integrals are supporting evidence;
the theorem uses the analytic proof above. The first reviewer also checked
2,160 exact mass/potential stress cases and 48 concave-gap refinements.

The [finite scalar two-bit comparison](../notes/scalar-convex-graph-two-bit-gap.md)
holds for every continuous convex scalar function, without monotone curvature,
but has no efficient partition-computation claim.

For a densely encoded positive rational polynomial, the
[certified compiled-quantile construction](compiled-curvature-quantile-precision.md)
now supplies the computational step: it constructs a polynomial-size rational
MILP with `p_out<=p_conv+7`. The generic C² finite theorem above remains
independent of those stronger input and computational assumptions.


The [separable extension](separable-convex-graph-linear-dimension-precision.md)
uses scalar interval packings and Jensen-gap superadditivity to compare
multivariate scalar sums and independent outputs with every convex integer lift.
It gives finite `O(r)` gaps for continuous convex summands and polynomial
rational constructions for dense positive polynomials.
