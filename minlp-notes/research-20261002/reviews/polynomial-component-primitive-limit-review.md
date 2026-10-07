# Independent review of the joint critical-limit component solver

Date: 2026-10-02. Result: passed for the stated explicit fixed-degree
rational-polynomial model on a nonempty bounded closed product box.
Read the entire actual
[component construction](../new-direction/polynomial-component-primitive-limit.md)
afresh, together with the relevant
[earlier fallback construction](../new-direction/polynomial-exact-fallback-construction.md).
No substantive mathematical or bit-complexity gap was found. The author
added the explicit closed-box qualifier and a constructive exact-tie
comparison after this review requested those clarifications.

This review concerns the deterministic component theorem and its output
interface. It does not promote a full strong-field polynomial theorem or
make an originality claim.

## 1. The candidate list is complete on every input

The face equations have leading monomials `x_i^a`, with coefficient one,
and every remaining monomial has strictly smaller total degree. Their
pairwise coprime leading monomials give a Groebner basis. The standard
monomials form a basis over `Q[z]` and after each finite specialization of
`z`; the quotient dimension is exactly `N=a^r`. Neither radicality nor
generic input coefficients are needed.

Over an algebraic closure of `Q(epsilon)`, this finite quotient has at
most `N` geometric solutions, counted with local algebra multiplicity.
Algebraic Puiseux expansions describe the finitely many branches near
`epsilon=0`. Any exceptional nonzero parameter specializations can be
avoided when taking a sequence tending to zero. The proof uses existence
of these expansions; the algorithm does not compute them.

Perturbed minimizers exist by compactness. Uniform convergence of the
perturbed objective makes every subsequential limit an original
minimizer. A subsequence uses one original face and one algebraic branch.
It is a bounded branch because the box is bounded. A zero-dimensional
face is already covered by the vertex candidates. The limiting point
may reach the boundary of its selected face, so the inclusive closed-face
test in the algorithm is necessary and correct.

## 2. One enumerated form passes the extraction tests

A branch that diverges has a nonzero leading-pole vector. A linear form
avoiding that vector cannot turn the branch into a bounded projection.
The moment curve turns each such avoidance condition into a nonzero
polynomial in `t` of degree at most `r-1`. The same degree bound applies
to separating each pair of distinct bounded limits. Therefore the
displayed count

\[
 1+(r-1)\left(N+\binom N2\right)
\]

really guarantees one good integer form, including `r=1`.

The characteristic polynomial is the product of projected coordinates
with their local multiplicities. This remains true for a nonradical
quotient: the nilpotent part does not change the eigenvalues or their
algebraic multiplicities. For a good form, taking the leading power in
`z` gives the stated product over bounded vector limits; every divergent
branch contributes only a nonzero scalar factor to its leading term.
There is no cancellation of this leading product.

The normalization power `K` is constant on a full neighborhood in the
independent linear-form coefficients, since all leading-pole projections
remain nonzero there. Coefficients of higher powers of `z` vanish on
this neighborhood and hence vanish as coefficient polynomials.
Consequently differentiation in an independent coefficient commutes with
extracting the coefficient of `z^K`, and every derivative has `z` degree
at most `K`. The algorithm correctly differentiates in the independent
coefficient direction before substituting the moment-curve form.

Writing the leading polynomial as
`C product_v(T-lambda^T v)^{mu_v}` proves that
`G=gcd(p,p')` divides each good-form coordinate numerator. After division
by `G`, the derivative of `C` contributes zero at a root. The other
terms give `B_i(alpha)/A(alpha)=v_i`. The denominator is nonzero there:
distinct limits are separated and the positive multiplicities remain
nonzero in characteristic zero. The identity `gcd(A,P)=1` also follows
directly from the multiplicities of the roots of any nonconstant `p`.

The degree and divisibility rejection tests for bad forms are essential;
they are present in the actual algorithm. A bad form that passes them
can supply spurious points, but the exact feasibility filter makes those
points harmless. At least one good form reconstructs every bounded
critical limit. Real projected roots correspond to real vector limits
for that form by separation and complex conjugation. Together with
Section 1, this proves exact minimization on every rational input,
including ties and positive-dimensional original stationary sets.

## 3. The matrix and extraction costs have a constant base

The memoization bound uses

\[
 R=r(a-1)+1,\qquad
 \#\{x^\beta:|\beta|\le R\}=\binom{ar+1}{r}\le c_d^r.
\]

Each reduction replaces a power `x_i^a` by terms of lower total degree,
so all recurrence dependencies have already been computed. The table
stores vectors of `N` polynomials in `z`, each of degree at most `R`.
If an integer `C` clears the derivative coefficients including `1/D`,
all entries can use the common denominator `C^R`. Its logarithm is
polynomial in `H,r`. Each path has at most `R` steps, and the logarithm
of the possible path count is `O(R log(s+1))`; this only adds polynomial
coefficient length. The algorithm never enumerates those paths.

For a fixed form and coordinate direction, the determinant uses only
`z,T,u`. A rectangular interpolation grid has at most
`(RN+1)(N+1)^2` nodes. Each rational determinant, its sampled entry
heights, and interpolation have polynomial bit work in `N,H,r`.
The coefficient heights are controlled by determinant and interpolation
bounds of the same form. The sampled `t` and its coordinate powers have
polynomial bit length in `r`. No exponent of `H` depends on `r`.

Polynomial gcd, exact division and modular inversion preserve polynomial
degree and coefficient-height bounds; subresultant or Sylvester-matrix
bounds justify the extended Euclidean step. There are only
`O(rN^2)` forms and `O(rN^3)` candidate roots per face. Univariate real
root isolation and exact signs at isolated roots have absolute
polynomial bit bounds in their degree and coefficient length. Summing
over original faces, and then enumerating native integer labels, gives
the stated continuous and mixed bounds.

A separate arithmetic reader checked the complete actual Sections 5--6
and independently approved these denominator, interpolation and height
arguments.

## 4. Exact values and output do not recreate a coordinate product

Every reconstructed coordinate is a polynomial of one root `alpha`,
with degree below `deg P<=N`. Fixed total degree of the original
objective gives an objective composition of degree at most `d(N-1)`
and polynomial coefficient height. Its value resultant is nonzero:
over the roots of `P` it is, up to a nonzero scalar, a product of the
nonzero linear polynomials `q_1 Z-H_1(alpha)`. Its degree in `Z` is at
most `N`.

Univariate separation bounds for the squarefree value polynomial, plus
a derivative bound for the composition, identify the value associated
with an isolated `alpha` at polynomial precision. To compare two
candidates including a tie, one may isolate the squarefree product of
their two value polynomials or use their polynomial gcd. Equal values
then have the same root identifier. These are polynomial operations in
the two degrees and heights; they require no product of `r` independent
coordinate field degrees.

The optimizer representation has constant-base exponential size. Its
root and coordinate polynomials permit additional point and value
precision within the same type of bit bound. Clipping rational
coordinate approximations to the original box preserves feasibility
and cannot increase their coordinate errors. A rational gradient bound
for the explicit objective on that box turns a point-error bound into
a certified value gap. Native integer labels are retained exactly.

For separate components, one representation per component and a symbolic
sum of exact values give the claimed structured output and refinement.
This interface does not assert efficient exact comparison of arbitrary
sums from different collections of algebraic components. Such a claim
is unnecessary for minimizing an already separated additive objective,
and the actual note does not make it.

## Verification scope

This was an independent completed-file mathematical and bit-complexity
review. The final closed-box, tie-comparison and diagnostic-status text
was also read after the author's updates. A targeted inline Python check
of the construction and this review passed local link resolution,
balanced display delimiters, trailing whitespace and sequential equation
tags. No optimization fixtures were run by this reviewer; the author's
separate exact small-quotient diagnostic is recorded in the construction
with its limited scope. No external search, project-wide verification or
CI inspection was performed.
