# Second independent audit: positive polynomial inverse approximation

Date: 2026-09-05. Reviewer: quadratic_weighted_precision.
Status: **PASS** for the analytic and rational bit-complexity lemma and its
stated transfer to affine-objective bilevel optimization in fixed leader
dimension. No correction is required.

Reviewed the full [candidate](certified-positive-polynomial-inverse-approximation.md),
its exact checker, and the linked
[bounded-power algorithm](bilevel-bounded-power-accuracy-bit-algorithm.md).
This review does not assert novelty or practical running time.

## Analytic radius and coverage

After normalization, the bounds `z^P<=g(z)<=z` and
`g(z)<=z g'(z)<=P g(z)` hold term by term. They include missing low-degree
terms and `P=1`. Strict monotonicity holds on the whole unit interval,
despite a possible zero derivative at the origin. The zero branch below
`2^(-Pm)` has the stated error, including negative targets.

For `|w|<=z0/(4P)`, the derivative majorant follows by expanding every
positive-coefficient derivative monomial. Its relative change is less
than `exp(1/4)-1<1/3`. The integrated bound is non-strict, including at
`w=0`. On the boundary, the nonlinear remainder and target displacement
together are at most `5/6` of the linear term. Rouché therefore supplies
exactly one root, counted with multiplicity, throughout the closed target
disk of radius `t0/(8P)`. The derivative bound excludes critical points.
Local analytic inverses agree by uniqueness; the strict boundary margin
also extends the construction past that closed target disk. Thus Cauchy's
coefficient bound at the displayed radius is justified. The real branch
is positive and unique and agrees with the real inverse; real targets at
most one cannot have this positive root above one.

The classical statements match the directly checked
[NIST DLMF Section 1.10](https://dlmf.nist.gov/1.10): Taylor expansion and
Cauchy's coefficient integral, Rouché's theorem, and local analytic
inversion. The candidate supplies the quantitative disk bounds itself.

There are exactly `32P` panels in each of `Pm` dyadic bands. Their
half-width is at most `tau/(64P)`. Rational response bisection to width
`tau/(64P^2)` gives the claimed, conservatively rounded target-center
error. Consequently the displaced panel satisfies

```
max_panel |t-t0| / (t0/(8P)) <= 16/63 < 1/2.
```

This check includes the first retained panel, the last panel at one, and
centers shifted in either direction. No assumption that the chosen
response center is the exact inverse of the panel midpoint is needed.
The dyadic panels cover the entire retained interval without gaps. Either
branch is valid at each common endpoint; the constant branches also meet
the required global error at the truncation and saturation thresholds.

## Exact reversion and bit lengths

Writing the shifted derivative coefficients with a common positive
integer denominator is legitimate and preserves polynomial bit length.
If the rational response center has `O(Pm+log P)` bits, taking its powers
up to degree `P`, multiplying the input rational coefficients, and
summing the resulting terms still requires polynomially many bits.

The coefficient recurrence is triangular: a term of degree `n` in a
power with at least two zero-constant factors cannot involve `c_n`.
The displayed denominator induction is correct:

```
c_n = D^n N_n / A1^(2n-1),       N_n integer.
```

For a product of `h` coefficients with total index `n`, the denominator
power is `2n-h`. Multiplication by `A_h/A1` and conversion to the common
denominator multiply its integer numerator by `A1^(h-2)`, a nonnegative
integer power. This also covers zero higher shifted coefficients.

There is no unproved assumption that repeated exact rational operations
automatically have polynomial height. Here `t0>=63*2^(-Pm)/64` gives
`log(1/R_t)=O(Pm+log P)`, and Cauchy's bound gives
`|c_n|<=2 R_t^(-n)`. Together with the explicit denominator, these bound
the final integer numerators polynomially. Intermediate truncated
products also have polynomial height: they contain at most `n` factors
of already bounded height, and each coefficient sums at most
exponentially many compositions, whose count has only `O(n)` bits.
The calculation uses polynomially many truncated convolutions, rather
than enumerating those compositions. Cancellation therefore causes no
uncontrolled intermediate precision requirement.

With `q=m+3`, the geometric tail is `2^(1-q)<=eta/4`.
Expansion into ordinary target powers and undoing the rational target
normalization preserve polynomial height. The total construction is
polynomial in the coefficient encoding, numerical `P`, and accuracy bits.
It makes no corresponding claim for sparse binary degrees.

## Bilevel transfer

The follower marginal is strictly increasing, so each separable box
follower has the unique clipped-inverse response asserted in the note.
The new approximation has the exact interface used in the reviewed
bounded-power proof: polynomially many rational breakpoints, polynomial
branch degree and height, and a uniform absolute response error.

Affine preimages of these breakpoints give polynomially many cells in
fixed leader dimension, including lower-dimensional cells. Each selected
branch remains valid on its closed cell. Substitution into an affine
upper objective leaves a polynomial number of monomials in fixed
dimension. The prior fixed-dimensional real-algebraic minimization and
rational simplex-weight recovery apply with the same objective-error
budget. Evaluating the final follower responses by rational bisection
also remains polynomial in numerical degree and requested accuracy bits.
No exact sign oracle for a sum of algebraic responses is introduced.
Additional response-dependent upper constraints remain outside this
argument, as stated by the author.

## Reproducible checks

Inspected and reran
[the supplied exact checker](../code/bilevel_bounded_power/check_positive_polynomial_inverse.py):
90 rational Taylor reversions, 450 certified inverse comparisons, and
360 Gaussian-rational derivative-disk inequalities passed. The largest
tested coefficient encoding was 2,894 bits.

Additional independent stress calculations used degrees 2, 7, and 31,
coefficient ratio `2^200`, and the first, middle, and final dyadic bands.
All 27 endpoint/midpoint inverse enclosures passed, as did the exact
shifted-panel radius and reversion identities. These finite tests
supplement the all-input proof; they do not implement or validate the
real-algebraic optimization backend by themselves.
