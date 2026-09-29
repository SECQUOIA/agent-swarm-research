# Fresh exact review of the degree-23 linkage example

Date: 2026-09-28. Status: no mathematical defect found in the stated
negative example or in its cube-plus-external-point obstruction.
The reviewer did not construct the example or its checker. This review
does not establish a general degree bound or priority.

Reviewed files:

- [Main note](degree23-linkage-negative-example.md).
- [Python checker](check_degree23_linkage.py).
- [Singular checker](check_degree23_linkage.sing).
- Section 2 of [the flat-direction note](quartic-zero-degree-adversarial.md).

## Exact algebra and the inferences behind it

The five displayed quadrics have a homogeneous ideal of dimension one
in a polynomial ring of dimension six. Since they are five generators
of height five, they form a regular sequence. Thus the computed degree
32 is the degree of a proper projective complete intersection, not an
affine count that has silently lost points at infinity. The checker
also verifies its complete-intersection Hilbert numerator.

The residual is formed by the ideal quotient `G = C:R`, where `R`
contains the linear generator `x5`. The checker explicitly verifies
both homogeneous saturation of `G` and `R`, the reverse quotient
`C:G = R`, and saturation of `G` with respect to `x5`. It separately
checks that `G + (x5)` has dimension zero as a homogeneous affine-cone
ideal. Its projectivization is therefore empty. Saturation alone would
not have justified this last conclusion; the additional check matters.

The affine computation dehomogenizes `C`, rather than `G`. This is
valid: localization commutes with ideal quotient here, and `x5` belongs
to `R`, so `R` becomes the unit ideal after inverting `x5`. Consequently
`C` and `G` have the same ideal in the chart `x5=1`.

The affine quotient has dimension 23. Its lexicographic basis has the
specified degree-23 polynomial in `t=x4` and leading monomials
`x3,x2,x1,x0` for its four other members. These data justify the field
claim. More directly, the irreducible eliminant gives an injective
map from its degree-23 field into the affine quotient; equal vector
space dimensions make this an isomorphism. Thus the field conclusion
does not depend on an unverified interpretation of numerical roots or
on the precise display of the four shape polynomials.

The reduction modulo 293 preserves degree 23. Since 23 is prime, the
verified Frobenius identity and absence of a linear factor imply
irreducibility: all irreducible factor degrees divide 23, and the
Frobenius polynomial is squarefree. Exact root counting gives three
real embeddings. Characteristic zero makes all 23 geometric residual
points distinct. The Jacobian has rank five at all nine specified
residual points; these and the field points account for the entire
degree 32. This proves reducedness of the projective intersection.

The sixth quadric identity is correct, and its values on the eight
cube points are positive. The six quadrics are independent; the
computed Hilbert numerator gives exactly six quadratic relations.
The checker verifies the actual homogeneous ideal equality
`(C,g) = G intersect I_b`, not just equality of degrees or supports.
Since `G` is saturated and its affine chart is a separable field,
and it has no points outside that chart, it is reduced. Its
intersection with the distinct rational point ideal is therefore a
reduced, saturated degree-24 scheme. The claimed extra quadratic base
point is established scheme-theoretically.

## General obstruction and affine charts

I inspected the residual-scheme definition and Theorem 1.2 of
[Gold, Little, and Schenck](https://arxiv.org/pdf/math/0311129), which
states the Cayley--Bacharach identity attributed to
Davis--Geramita--Orecchia. Its shift is four for five quadrics in
projective five-space. The two dimension differences in the main note
are both one, using `H_R(2)=8` and `H_A(2)=7`. Their containment hence
is equality. The alternate argument with `q*x4^2` is also valid:
this degree-four polynomial vanishes on every point except possibly
the external point, where `x4` is nonzero. Reducedness of the proposed
complete intersection is explicitly assumed in this general claim.

In a rational affine chart containing one point of the degree-23
closed point, every conjugate is in the chart: a nonzero value of the
rational chart-defining linear form is a nonzero field element and
stays nonzero under all embeddings. The chart coordinates generate
the same field, by the rational inverse projective coordinate change.
Thus an affine external point is a distinct real common zero of all
rational quadratic factors. If the external point is at infinity,
their leading quadratic parts vanish in its nonzero rational direction.

The imported convex reduction is sound. The zero directions of the
convex homogeneous quartic form are exactly its translation-invariant
directions, hence a rational linear subspace. Positivity of the full
Hessian forces the cubic part to be invariant there too. The remaining
dependence in those directions is quadratic, with a positive definite
constant fiber Hessian. Its minimizer is rational affine. Substitution
preserves rational quadratic factors, global convexity, the singleton
zero, its coordinate field, and a positive definite Hessian by the
Schur complement. In `m<=4` remaining variables, independent quadratic
gradients give the isolated-point Bezout bound `2^m<=16`, contradicting
degree 23. When no variables remain, the zero is rational.

I requested the last dimension-dependent wording: the initial text
said four independent residuals even when fewer than four variables
remain. The author corrected it, and I rechecked the corrected
argument. This was a wording defect, not a failure of the reduction.
An extra point at infinity alone would not exclude an arbitrary
nonconvex affine SOS singleton; the main note correctly retains the
global convexity and regularity assumptions.

## Targeted verification actually run

The following command passed, including after the explicit
degree-preservation assertion was added to the Python checker:

```sh
SINGULARPATH=/tmp/degree23-singular/usr/share/singular/LIB \
LD_LIBRARY_PATH=/tmp/degree23-singular/usr/lib/x86_64-linux-gnu \
python research-20260927/check_degree23_linkage.py \
  --singular /tmp/degree23-singular/usr/bin/Singular
```

It reported the degree counts 32, 23, and 24; both saturation tests;
the ideal equalities; the specified affine shape eliminant; and
`DEGREE23_LINKAGE_PASS`. The only diagnostic was Singular's warning
that an optional dynamic acceleration library was unavailable.

A separate one-off Python heredoc independently recomputed the
univariate certificates without SymPy polynomial operations. It used
integer coefficient arithmetic modulo 293 for the Frobenius and gcd
tests, and `fractions.Fraction` Euclidean remainders for the Sturm
sequence. The sequence had degrees `23,22,...,0`; its sign variations
at negative and positive infinity were respectively 13 and 10. Both
the independent irreducibility test and the count of three real roots
passed. This supplementary script was not retained; the retained
checker remains the reproducible verification entry point.

These checks trust the exact arithmetic and computer algebra systems;
they are not formally checked proof certificates. The universal
Cayley--Bacharach and convexity arguments were reviewed symbolically,
not established by these example computations. No Lean proof,
project-wide verification, or CI inspection was performed. The
broader small-odd-residual theorem in the separate residual-obstruction
note is outside this fresh review's scope.
