# Prior search: rational singleton spectrahedra with corank one

Date: 2026-09-28. This is a source audit for the two-parameter pencil in
[the three-quadratic construction](few-quadratic-unbounded-degree.md).
It supplements [the existing ellipsoid audit](three-ellipsoid-degree-prior-audit.md).
It is not an independent proof review of that construction.

The inspected sources do not give the full statement under investigation:
for every irreducible rational polynomial with exactly one real root
$\alpha$, a rational pencil in two scalar variables whose feasible set is
$\{(\alpha,\alpha^2)\}$ and whose unique feasible matrix has corank one.
This search does not establish novelty. In particular, arbitrary-degree
singleton spectrahedra and irrational Gram spectrahedra have older
constructions; their parameter counts and ranks must be kept in the
comparison.

## An explicit historical question

Christopher Hillar's March 2010 BIRS talk, *Rational Sums of Squares and
Applications*, asks on slide 18 which algebraic numbers can be represented
by finite rational spectrahedra with a prescribed number of variables. It
states that the one-variable case was unresolved at the time and credits
Laurent for realization when both matrix size and variable count may vary.
The slide's final illustrative formula is imprecise, so the reliable
historical evidence is its preceding verbal question. The slide was
inspected visually, in addition to text extraction.
[Primary slides, inspected mirror](https://staff.math.su.se/shapiro/ProblemSolving/hillarbirstalk20100302.pdf).

This is evidence that fixed-variable realization was an explicit research
question in 2010. It is not evidence that any part of that question remains
open today. Searches using the title, author, finite spectrahedra,
singleton spectrahedra, algebraic-number realization, and fixed-variable
pencils did not locate a subsequent arithmetic classification.

## The one-variable obstruction has established spectral antecedents

Liang, Li, and Bai, *Trace minimization principles for positive
semi-definite pencils*, Linear Algebra and its Applications 438 (2013),
3085–3106, define a PSD Hermitian pencil by the existence of a real
parameter at which its matrix is PSD. Singular pencils are explicitly
allowed. Lemmas 3.2–3.3 reduce such a pencil to a pencil with nonsingular
coefficient matrix and a constant PSD block. Lemma 3.8(2), printed page
3095, states that its finite eigenvalues are all real. The accompanying
canonical form includes the common zero block. This is directly relevant
to a rational one-variable singleton's algebraic conjugates, including the
case in which the unreduced determinant vanishes identically.
[Primary author PDF](https://web.cs.ucdavis.edu/~bai/publications/lianglibai13.pdf).

For the nonsingular-coefficient case, that paper's footnote 6 on printed
page 3087 credits Kovač-Striko and Veselić (1995), Proposition 4.1, and
Gohberg, Lancaster, and Rodman (1983), Theorem 5.10.1. Those earlier
originals were not independently inspected in this search. Li's later
survey restates the all-real-eigenvalues conclusion as Theorem 3.1.
[Author survey](https://bpb-us-e1.wpmucdn.com/websites.uta.edu/dist/7/5059/files/2021/06/li2015.pdf).

Nguyen and Nguyen's 2023 preprint *Positive semidefinite interval of matrix
pencil and its applications for the generalized trust region subproblems*
classifies singleton and interval parameter sets through congruence and
Jordan structure. Theorem 1 treats simultaneously diagonalizable pencils
with nonsingular coefficient matrix, including the singleton case;
subsequent theorems handle other cases. Its inspected statements concern
real symmetric matrix pairs, not rational realization of prescribed number
fields. Thus it is a structural predecessor, not a verified answer to the
two-variable arithmetic target.
[Primary preprint](https://arxiv.org/pdf/2302.14352).

## Number fields in rational sum-of-squares theory

Hillar's *Sums of squares over totally real fields are rational sums of
squares*, Theorem 1.4, proves descent of a rational polynomial's SOS
representation from a totally real number field to the rationals. Theorem
1.5 extends the statement to commutative rational algebras. These theorems
concern coefficients of an SOS decomposition, not merely entries of a PSD
matrix at one chosen real embedding. The distinction prevents applying
the descent statement to an arbitrary rational affine pencil without
additional hypotheses.
[Primary preprint](https://arxiv.org/pdf/0704.2824).

Capco and Scheiderer, *Two remarks on sums of squares with rational
coefficients*, Theorems 2.2 and 2.5, refine norm-form constructions using
totally imaginary fields and Galois conditions to obtain real SOS forms
that are not rational SOS. Their introduction also records Laplagne's
negative answer to descent over odd-degree extensions, using
$\mathbb Q(\sqrt[3]2)$. Corollary 3.5 gives singleton Gram spectrahedra
for strictly positive ternary sextics on the SOS boundary. These facts
reinforce that singleton Gram spectrahedra and arithmetic obstructions
are established topics. They do not supply a fixed two-parameter,
arbitrary-degree, corank-one realization theorem.
[Primary preprint](https://arxiv.org/pdf/1905.13282).

The Laurent finite-variety representation, Laplagne's explicit irrational
singleton, and the SPECTRA square-root singleton are compared in the
earlier ellipsoid audit. In particular, Laurent's power-basis construction
has rank one rather than corank one. A spectrahedral representation also
does not by itself provide three native convex quadratic inequalities:
principal minors can have high degree, and squaring a general SOC
inequality can produce an indefinite quadratic polynomial.

## Further sources and limits

Jiang and Sturmfels, *Bad projections of the PSD cone*, Section 4, studies
the algebraic computation of spectrahedral rank for rational matrix
spaces and the equations $X\in L$, $Y\in L^\perp$, $XY=0$. Its inspected
examples and results do not give the prescribed two-variable singleton
construction. Here “bad” concerns nonclosed linear images of the PSD cone.
[Primary preprint](https://arxiv.org/pdf/2006.09956).

Kolmogorov, Naldi, and Zapata, *Certifying solutions of degenerate
semidefinite programs*, Theorem 1.1 in the April 2025 revision, obtains an
isolated real solution of an auxiliary polynomial system from a
sufficiently accurate approximation to a maximum-rank feasible matrix.
It allows irrational feasible matrices. This is a certification theorem,
not a family realizing prescribed algebraic numbers in two LMI variables.
[Primary preprint](https://arxiv.org/pdf/2405.13625).

Searches also covered corank-one singleton pencils, rational spectrahedral
cones with irrational rays, real embeddings, rational Gram matrices, and
unique real conjugates. Searches on “rational quartic spectrahedra” need
care: that literature can use “rational” for a rationally parametrizable
algebraic boundary, rather than rational entries in the defining pencil.
No equivalence between the target and the inspected results was verified.

Verification used primary PDFs, targeted text extraction, and visual
inspection of Hillar's slide 18. No mathematical computation or solver
experiment was needed for these source comparisons. The targeted document
check, run through an inline `python - <<'PY'` command, verified final
newline, trailing whitespace, control characters,
balanced display-math delimiters, and the two relative Markdown links.
No project-wide or CI checks were run.
