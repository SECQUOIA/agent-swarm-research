# Independent second audit of the monotone polynomial inverse construction

Date: 2026-09-05. Verdict: **PASS**. The accuracy-input clarification
below has been incorporated into the candidate. This audit independently checked the full proof of
[the candidate lemma](certified-monotone-polynomial-inverse-approximation.md)
and its stated transfer to the existing separable bilevel algorithm.
It does not establish publication priority.

## Accuracy input

For a literally arbitrary rational tolerance, running time must include
the encoding length of that rational. A value close to one can have a
long numerator and denominator even though `log(1/eta)` is small. The clean
statement takes an accuracy integer `B`, uses `eta=2^(-B)`, and is polynomial
in `B`. Equivalently, include the rational tolerance's encoding in input
length. This is a specification correction, not a mathematical obstruction
to the claimed accuracy-bit bound.

## Proof audit

The Lagrange interpolation estimate is valid for signed coefficients.
At each interpolation node, monotonicity bounds the shifted polynomial
between zero and its increment `mu`. Every numerator factor is at most
one in absolute value on the unit interval. The reciprocal denominator
sum is `(D/h)^D 2^D/D!`. Evaluating at both endpoints bounds their difference
one by twice this quantity times `mu`. The weaker displayed estimate
therefore follows. The chosen `delta` has polynomial bit length and
forces inverse variation below `e` on every target interval of length
at most `delta`, including intervals containing stationary inverse points.

The critical-value projection is finite for `D>1`: `g'` has at most `D-1`
distinct complex roots, hence its real and imaginary equations have only
finitely many real pairs `(u,v)`. Adding the real part of `g(u+iv)` adds
one variable, not a variable for every root. Dense expansion into three
real variables has polynomially many monomials and polynomial coefficient
encoding. Fixed-dimensional real quantifier elimination and univariate
isolation consequently have polynomial bit complexity. Coincident real
parts, repeated critical points, and nonreal critical values do not
invalidate this argument. Exact algebraic comparisons handle the
restriction to `[-1,2]`.

Padding each isolating interval by `rho` leaves every enclosed real part
at least `rho` behind its boundary. Merging intervals preserves this
property at the exposed boundaries. The total excluded length is at most
`delta`; isolated endpoint intervals are included in that accounting.
Thus constant approximations on the excluded components are uniformly
accurate even at a real stationary inverse. In a retained gap, omitted
critical real parts outside `[-1,2]` are farther away than the proposed
distance lower bound. There is no assumption that the dangerous critical
values themselves are real.

For a left-half panel of width at most `(x-a+rho)/32`, its half-width is
at most `d(tau)/64`; the reflected argument gives the right half. Geometric
growth by `33/32` gives polynomially many panels. Repeated multiplication
and addition increase rational bit length only polynomially, since the
number of steps and initial endpoint encodings are polynomially bounded.

Exact sign bisection finds a rational response center to the stated
target accuracy: the coefficient bound `L` controls the forward error
from a short response interval. The shift to the rational target
`t0=g(z0)` consumes only `d/64` of the critical-distance margin. Hence
`g'(z0)` cannot vanish. The radius-`d/4` disk, with room to enlarge it,
contains no critical value. A proper polynomial map restricts to a finite
unramified covering above such a disk; each component over a simply
connected disk is a single holomorphic inverse branch. Properness rules
out escape to infinity during continuation. On the real segment between
the center and panel points, this branch is the increasing unit-interval
inverse. Interior zeros of `g'` elsewhere do not affect it.

The disk stays inside `|t|<2`, and the displayed Cauchy root bound controls
every complex solution of `g(z)=t`, so it controls the selected branch.
Its logarithm has polynomial input size even for small leading
coefficients. The panel-to-disk radius ratio is at most `1/8`. Using the
weaker ratio `1/2`, the tail after degree `q` is at most `M*2^(-q)`,
which is at most `eta/4` for the proposed choice. The stated `eta/2`
bound is conservative.

For the common-denominator assertion, consider a term of degree `n`
in the `h`th power of the inverse series, with positive indices summing
to `n`. Induction gives its denominator as a divisor of
`A_1^(2n-h)` and a numerator divisible by `Q^n`. The outer division by
`A_1` produces exponent `2n-h+1 <= 2n-1`. Multiplication by an integer
power of `A_1` therefore gives the proposed common denominator even when
the forward coefficients have arbitrary signs. Cauchy's magnitude bound
then bounds the resulting numerator. Intermediate truncated products
have at most exponentially many compositions in the truncation order;
the logarithm of that count is linear in the order. Their magnitudes and
common denominators consequently have polynomial bit length as well.
This closes both final-output and intermediate-arithmetic complexity.

The clipping pieces and a half-open convention at breakpoints define a
single rational piecewise-polynomial output. Both neighboring formulas
satisfy the accuracy guarantee at a shared endpoint. Normalizing an
arbitrary strictly increasing rational polynomial marginal uses a
positive rational endpoint difference and preserves encoding length.
In fixed leader dimension, affine preimages of the rational breakpoints
give polynomially many cells, with polynomial-degree rational objective
surrogates. The existing rational leader recovery remains applicable.
The claim retains an affine upper objective and excludes additional
response-dependent upper constraints; inverse approximation alone does
not justify exact feasibility for those constraints.

## Independent exact diagnostics

The new [standard-library checker](../code/bilevel_bounded_power/check_monotone_inverse_second.py)
uses exact `Fraction` arithmetic. It tests two polynomials
`((2z-1)^D+1)/2`, with `D=3,5`, whose inverses have interior stationary
singularities, and three normalized signed cubics whose critical points
are nonreal Gaussian rationals. The latter critical values have real
part exactly `1/2` and a nonzero imaginary part; they include a small
positive derivative near the center and a large coefficient scale.

The checker independently obtains inverse coefficients from the Lagrange
coefficient formula, then verifies their exact composition into the
forward polynomial, the claimed denominator divisibility, and Cauchy
bounds. Separate exact rational bisection encloses inverse values at
panel endpoints and midpoints. Its completed run reports:

```
PASS: 15504 exact panels; 20 Taylor centers;
236 denominator/Cauchy checks; 60 certified inverse enclosures;
80 modulus checks; 3 nonreal critical-value pairs
```

The checks verify panel geometry across complete rational subdivisions
for these examples. They supplement the proof; they do not replace the
general critical-value isolation algorithm or its complexity theorem.
