# Source comparison: uniform rational monotone-polynomial inverses

Date: 2026-09-05. Scope: the already-started extension in
[the supporting lemma](certified-monotone-polynomial-inverse-approximation.md).
This is a bounded literature comparison, not a proof of priority.

The construction is best positioned as a supporting bit-complexity lemma
for the bilevel results. Polynomial inverse approximation, formal reversion,
analytic continuation and geometric refinement near singularities all have
substantial prior literature. The candidate distinction is the combined
uniform guarantee: polynomial total rational representation and construction
time in dense degree, coefficient encoding and accuracy bits, including
interior stationary points. Do not claim a new general method for inverting
polynomials or a new series-computation theorem.

## Direct polynomial-inverse approximation predecessor

Rida T. Farouki, *Convergent inversion approximations for polynomials in
Bernstein form*, Computer Aided Geometric Design 17 (2000), 179–196,
[DOI and publisher abstract](https://doi.org/10.1016/S0167-8396(99)00046-1).
Bibliography was checked against the [author's publication list](https://faculty.engineering.ucdavis.edu/farouki/publications/);
the published article's text was read through an
[open indexed mirror](https://www.scribd.com/document/373920033/rerwe).

Sections 1–3 already discuss power-series reversion, its limited convergence
radius, Bernstein inverse approximation, and an explicit Legendre
least-squares algorithm. Section 2 uses `f'(t)>0` on the whole unit interval.
Section 3 counts arithmetic operations in input and approximation degrees;
its stopping error is an integral squared error. The local lemma instead
supplies a uniform error guarantee and a bound polynomial in accuracy bits
for the complete rational piecewise representation, allowing zero derivatives.
The paper does not state that combined guarantee. The distinction is not
whether an inverse is approximated symbolically rather than evaluated by
pointwise root finding: that distinction is already explicit in Farouki.

## Series computation already has polynomial bit complexity

P. G. Walsh, *A polynomial-time complexity bound for the computation of the
singular part of a Puiseux expansion of an algebraic function*, Mathematics
of Computation 69 (2000), 1167–1182,
[DOI](https://doi.org/10.1090/S0025-5718-00-01246-1).
The publisher PDF returned HTTP 403; the published text, including
Theorem 1 and its following paragraph, was read through an
[open mirror](https://paperzz.com/doc/7111378/a-polynomial-time-complexity-bound-for-the-computation-of...).

Theorem 1 bounds bit operations polynomially in both degrees and logarithmic
coefficient height for a Puiseux singular part. The following paragraph
also explains polynomial-time computation of any requested number of terms.
Therefore the local rational reversion calculation is an elementary special
case of established algebraic-series arithmetic. What still requires the
local proof is selecting polynomially many rational real panels and their
uniformly sufficient Taylor orders to cover the complete clipped response.
No new polynomial-bit series algorithm is claimed.

## Other established ingredients

Basu, Pollack and Roy's [quantifier-elimination paper](https://citeseerx.ist.psu.edu/document?doi=dab8ba1c3d90aeebd7ce0fb1cc999c43839aeaab&repid=rep1&type=pdf)
and their [book resources](https://www.math.purdue.edu/~sbasu/) supply the
fixed-variable real-algebraic computations. Only three real variables are
needed for the critical-real-part projection. Holomorphic local inversion,
monodromy, proper polynomial covering and Cauchy estimates are classical.
The elementary interpolation lower bound is a Remez-type growth estimate,
and the geometric panel refinement is a standard approximation strategy.

The source search included combinations of monotone polynomial inverse,
piecewise polynomial approximation, algebraic functions, bit complexity,
Puiseux computation and geometric meshes. No inspected source states the
same full uniform rational construction or its fixed-dimensional bilevel
consequence. This limited negative search finding supports keeping the
lemma and examining the resulting optimization theorem; it does not certify
that the standalone lemma is unpublished, nor establish a publication claim
for the collection of classical ingredients.
