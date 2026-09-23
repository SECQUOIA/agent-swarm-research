# Independent audit: certified positive-polynomial inverse approximation

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** I independently checked the complete
[analytic and rational construction](certified-positive-polynomial-inverse-approximation.md)
and its transfer to the reviewed bounded-power bilevel algorithm. The
relative inverse disk, rational centers, coefficient encoding, branch
count, and accuracy-bit complexity are valid.

The author corrected the remainder inequality (4) from strict to non-strict
so that it also holds at `w=0`. The boundary estimate remains at most `5/6`
of the comparison function and is strictly smaller than that function.
No radius, error bound, or complexity claim changes. This review covers the
corrected version and does not certify literature priority.

## Normalization and endpoint branches

The coefficient sum `G` is positive, and rational normalization by `G`
has polynomial bit complexity. For the normalized polynomial,

```
z^P <= g(z) <= z,
g(z) <= z g'(z) <= P g(z),
0 <= g'(z) <= P   on [0,1].
```

Each inequality follows term by term, including zero coefficients and
nominal degree bounds larger than the actual degree. Since some coefficient
is positive, `g` is strictly increasing on the nonnegative real axis and
`g'(z)>0` for every `z>0`. Vanishing derivative at zero is allowed.

After the stated reduction of tolerance to at most `1/2`, `m>=1` and
`K=Pm`. For a positive target below `2^(-K)`, the inverse is at most
`t^(1/P)<=2^(-m)<=eta`. Thus the constant-zero branch is valid on the
entire lower region, including negative targets. The constant-one branch
is exact at and above the saturation threshold. Returning to the original
target multiplies all breakpoints by the positive rational `G`.

## Complex inverse neighborhood

For every derivative monomial, the relative displacement
`|w|/z_0<=1/(4P)` gives the binomial majorant in (3). The positive real
weights add without cancellation. The bound
`exp(1/4)-1<1/3` is strict, also when `P=1`, where the derivative
variation is zero. Hence the derivative is nonzero throughout the closed
response disk.

Integration along the straight segment gives the corrected non-strict
remainder bound. On its boundary, `z_0 g'(z_0)>=t_0` implies that the
allowed target displacement is at most half the linear term's magnitude.
The remainder plus target displacement is therefore at most `5/6` of
that magnitude. Rouché's theorem gives exactly one zero, counting
multiplicity, inside the response disk for every target in the closed
target disk.

The derivative bound makes these roots simple. Local analytic inverses
therefore agree wherever their target neighborhoods overlap, because the
root in the fixed response disk is unique. This produces one analytic
inverse throughout the target disk. The uniform boundary margin also
permits a slightly larger target disk: for example an extra target radius
`g'(z_0)r_z/12` still leaves the perturbation below the linear magnitude.
Thus use of Cauchy bounds at radius `R_t` itself is justified.

The inverse values remain in the disk about `z_0`, giving
`|Z|<z_0+z_0/(4P)<=5/4<2`. For real targets, conjugation and uniqueness
make the root real; its disk keeps it positive. Monotonicity on the positive
axis identifies it with the desired inverse. If the target is at most one,
this root cannot exceed one, because `g(1)=1` and `g` is increasing.

I checked the primary [DLMF section 1.10](https://dlmf.nist.gov/1.10),
including its Rouché statement, Taylor framework, and local inverse theorem
in section 1.10(vii). The hypotheses used here match those statements.
The quantitative radii are derived in the candidate rather than imported
from an unspecified conditioning theorem.

## Rational centers and panel coverage

There are `K` dyadic target intervals and exactly `32P` panels per
interval. This gives `32P^2 m` polynomial branches before any optional
merging. Their rational breakpoints have polynomial encoding length.
The half-width of a panel is at most `tau/(64P)`.

Exact bisection of `g(z)=tau` to response width `tau/(64P^2)` needs
`K+O(log P)` iterations. Its midpoint is strictly positive and no larger
than one. The derivative bound on `[0,1]` gives

```
|g(z_0)-tau| <= tau/(64P),
t_0 >= (63/64)tau.
```

The written bounds are conservative because the midpoint's response
error is at most half the bracket width. Combining this center displacement
with the panel half-width yields

```
|t-t_0| <= tau/(32P),
|t-t_0|/R_t <= 16/63 < 1/2.
```

Thus every closed panel lies in the certified inverse disk. The computed
center is the exact rational response to the exact rational target
`t_0=g(z_0)`. The construction changes the expansion center, not the
underlying inverse function. No irrational Taylor coefficient is computed
or approximated.

Every bisection comparison is exact evaluation of a rational polynomial.
Its bit length is polynomial in the original coefficient length, numerical
`P`, and `m`. The bound does not require a positive lower bound on `g'`
near zero or a numerical condition-number estimate.

## Exact reversion and coefficient bit bounds

Expanding at rational `z_0` gives nonnegative rational coefficients with
positive linear coefficient. Clearing their denominators produces the
stated integers `A_h` and positive integer `D` with polynomial bit length.
The formal substitution recurrence (8) is valid: a degree-`n` coefficient
in a power of order at least two cannot involve the unknown `c_n`.
Its solution is the Taylor series of the analytic local inverse.

I independently checked the denominator induction. A product of `h`
earlier inverse coefficients contributing to degree `n` has numerator
factor `D^n` and denominator `A_1^(2n-h)`. Multiplication by
`a_h/a_1=A_h/A_1`, followed by conversion to denominator
`A_1^(2n-1)`, introduces the integer factor `A_1^(h-2)`.
Hence

```
c_n = D^n N_n / A_1^(2n-1),   N_n integer,
```

including `n=1`, where `N_1=1`.

The analytic bound gives `|c_n|<=2R_t^(-n)`. Since `D>=1`, the
identity also bounds the integer numerator `N_n` by
`2R_t^(-n) A_1^(2n-1)`. Its logarithm is polynomial in the stated
parameters. Both `log(1/R_t)` and the input bit lengths of `A_1,D`
are polynomially bounded. Multiplying back by `D^n` does not change
this conclusion. Zero coefficients cause no difficulty.

This is a bit bound, not just an arithmetic-operation count. Truncated
products involve polynomially many coefficient operations; the number
of compositions contributing to a degree-`n` coefficient has logarithm
`O(n)`. Products have denominators involving only bounded powers of the
same integers. Intermediate numerator and denominator lengths therefore
remain polynomial even if the final coefficient has cancellation.
Ordinary-power expansion of `(t-t_0)^n` and later rescaling by `G` also
preserve polynomial encoding.

## Uniform error and branch boundaries

With `q=m+3`, the half-radius bound and Cauchy coefficients give tail error

```
2 sum_(n=q+1)^infinity 2^(-n) = 2^(1-q) <= eta/4.
```

This applies at both endpoints of every closed panel. Adjacent polynomial
branches need not agree exactly, but either branch approximates the true
response within the stated tolerance. At the lower truncation endpoint,
the constant zero and the neighboring Taylor branch both satisfy the
global `eta` guarantee. The same is true at saturation with the constant
one branch. No continuity claim for the piecewise approximation is needed.
Each branch degree is `O(m)` and the total output size is polynomial.

## Bilevel transfer

The proposed follower costs are strictly convex in each coordinate because
their marginal polynomial is strictly increasing. Their unique minimizers
are exactly the clipped inverses, with normalization by each marginal's
coefficient sum. The normalization keeps every target affine in the leader.

The replacement approximation has polynomially many rational breakpoints
and degree `O(log(1/eta))`, so its affine threshold preimages create only
polynomially many cells in fixed leader dimension. Lower-dimensional cells,
constant tests, and cell closures are handled as in the reviewed predecessor.
Every selected branch remains valid on the closed cell, so disagreements
between neighboring approximations do not affect the uniform error ledger.

With signed affine upper coefficients, weighting the local response error
by their absolute values gives the same objective guarantee. Fixed-dimensional
polynomial optimization applies to the expanded cell polynomial, whose
number of monomials and coefficient lengths remain polynomial. I reopened
[Basu's primary-author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf)
for the stated fixed-variable algebraic framework; no unbounded number of
follower variables is introduced into those polynomial optimization calls.

The predecessor's rational leader recovery uses convex combinations of
rational cell vertices and rounds their weights. It remains feasible in
the selected cell and only needs the logarithm of the cell polynomial's
explicit derivative bound, which is polynomial here. Final response values
at the rational leader can be enclosed by exact bisection in response space;
this does not require derivative conditioning. The original objective and
value error ledger therefore remains valid.

This transfer retains fixed leader dimension, a rational leader polytope,
and an affine objective in the responses. It does not establish exact
feasibility of extra response-dependent constraints or exact signs of
arbitrary sums of algebraic responses.

## Independent exact checks

I saved [an independent checker](../code/bilevel_bounded_power/check_positive_inverse_second.py).
It computes inverse jets using the Lagrange coefficient formula, separately
from the candidate's substitution recurrence, and checks their composition
back into the original polynomial. Exact rational bisection supplies
reference inverse intervals.

The checker passed:

- 159 rational expansion centers near the upper, middle, and lowest
  dyadic layers;
- 1,119 exact denominator-identity and Cauchy-bound checks;
- 477 certified inverse-value enclosures at panel endpoints and midpoints.

Cases include degree one, pure powers with a vanishing derivative at zero,
missing coefficients, and coefficient ratios involving `2^(-100)` and
`2^(-90)`. All checks are exact rational certificates rather than numerical
root comparisons. They supplement the general analytic and bit proofs.
The degree dependence is polynomial in numerical `P`; no sparse
binary-exponent complexity claim is made.
