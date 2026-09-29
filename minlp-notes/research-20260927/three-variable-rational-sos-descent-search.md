# Three-variable rational SOS descent: the successful obstruction

Date: 2026-09-28. Status: search record; the resulting theorem and exact
certificate are in the [main note](ternary-rational-sos-convex-counterexample.md).
No separate novelty claim is made here.

The four-variable construction suggested searching for a rational
quartic perturbation with zero first derivative at an algebraic point
but outside the span of products of rational vanishing quadratics.
That mechanism is unnecessary in three variables. A missing square
inside the product span gives a much smaller example.

For the cyclic quintic point

\[
 p=(a^{-1},a,a^{-3}),\qquad a^5=2,
\]

the rational quadratic vanishing space has dimension five, with basis

\[
 1-xy,\quad x^2-yz,\quad y^2-2z,\quad z^2-x/2,\quad xz-y/2.
\]

Let \(W\) be the span of their pairwise products, and let \(V\)
be the rational quartics whose value and all first derivatives vanish
at \(p\). Exact linear algebra gives

\[
 \dim W=15,\qquad \dim V=35-20=15,
 \qquad W=V.
\]

Here the first-jet map has four components, each expanded over the
basis \(1,a,a^2,a^3,a^4\), and has rank twenty. Thus no
perturbation in \(V\setminus W\) exists for this point.
This computation does not classify all quintic embeddings.

The decisive observation is that the first four quadratics already
support a rational SOS quartic with a positive definite Hessian Gram
matrix. Its polynomial Gram on the full five-dimensional vanishing
space has a zero final row and column. Subtracting a small positive
multiple of the fifth quadratic squared makes that polynomial Gram
indefinite while preserving strict Hessian positivity. In this example
the fifteen products are independent, so a different Gram on the same
vanishing space cannot repair the negative direction.

The final construction needs no small symbolic perturbation parameter:
integer residuals \(r_i\) twice the five displayed quadratics give

\[
 F=(4r_0+5r_1+3r_2+9r_3)^2
      +r_0^2+r_1^2+r_2^2+r_3^2-r_4^2.
\]

Its Hessian certificate is already positive definite. An independent
reviewer simplified the no-SOS proof further: the coefficient functional
\(2[z]+4[y^2]\) is nonnegative on squares in the vanishing space
and evaluates to \(-4\) on this polynomial. The main note gives the
proof, the exact coefficient-field obstruction, and the relevance to
optimization certificates.

The search used numerical eigenvalues only to select simple constants.
An initial exact candidate used dyadic approximations with denominator
\(2^{12}\). A second search found coefficients corresponding to
denominator four and rational center \((3/4,1,1/2)\), yielding the
small integer expression above. All final claims are checked using
rational arithmetic in the
[retained checker](check_ternary_rational_sos_convex_counterexample.py).
No numerical positive-definiteness claim is part of the proof.

The targeted command

```text
python research-20260927/check_ternary_rational_sos_convex_counterexample.py
```

passed. A separate inline `python -` calculation reduced all quartic
monomials and their first derivatives modulo \(a^5-2\), and verified
the rank-twenty first-jet map used above. No project-wide checks or CI
inspection were run.
