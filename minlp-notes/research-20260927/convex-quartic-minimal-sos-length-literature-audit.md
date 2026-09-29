# Literature audit for the convex quartic SOS-length bound

Date: 2026-09-28. Scope: primary-source comparisons for the claim that a
globally convex quartic with a zero having positive definite Hessian needs
at least $n+1$ polynomial squares. This is a bounded literature search, not
a priority assessment. The theorem note was not edited during this audit.

No equivalent theorem was found in the portions examined. The degree
argument has direct antecedents; the examined sources did not supply the
convexity-based reduction that precedes it.

1. **Martin Ames Harrison, *Quadratic Convexity and Sums of Squares* (2013).**
   The [full dissertation](https://web.math.ucsb.edu/~martin/dissertation.pdf)
   was retrieved; access is therefore not limited to the catalog abstract.
   Examined Sections 2.1 and 2.3, Chapter 3, and Chapter 4, with a full-text
   search for related terminology. Proposition 2.1.4, printed page 17,
   identifies SOS length with minimum positive semidefinite Gram-matrix
   rank. Theorem 3.2.10, page 47, gives full Jacobian row rank somewhere for
   a quadratic map whose image is convex and spans its codomain.
   Proposition 3.3.1, page 49, relates convexity of the image of a
   coefficient map parametrizing squares to a Pythagoras-number bound.
   Pages 50–52 concern maximum and typical lengths of homogeneous forms.
   These statements concern convexity of an image in coefficient space,
   rather than convexity of the polynomial as a function of its variables.
   They give no evident obstruction to the square case $m=n$ in the
   theorem under review.

2. **Claus Scheiderer, *Sum of squares length of real forms* (2016).**
   Examined the introduction and Sections 1–2 of
   [arXiv:1603.05430v1](https://arxiv.org/abs/1603.05430v1), using the local
   PDF text already in the sources directory. Theorem 1.12 and Corollary
   1.13 give upper bounds using a real zero's multiplicity. After
   homogenizing a polynomial in $n$ variables from the present theorem,
   the resulting form has $n+1$ variables, degree four, and a projective
   zero of multiplicity two. Theorem 1.12 then gives the upper bound
   $n(n+1)/2$ for $n\ge2$. In two affine variables, Corollary 1.13 gives
   length at most three. None of these is the claimed universal lower
   bound; combined with it, the two-variable case has length exactly three.

3. **G. Khimshiashvili, *Remarks on Homogeneous Endomorphisms* (2016).**
   Examined Section 2, printed pages 26–29, of the
   [primary paper](https://viam.science.tsu.ge/publishing/proceedings/vol66/Khimshiashvili.pdf).
   Corollary 1 on page 28 states the odd-dimensional degree-zero property
   and even regular-fiber cardinality for homogeneous quadratic
   endomorphisms. Proposition 1 on page 29 states properness and equality
   of degree with the leading part when that part is nondegenerate.
   These are direct overlap with the theorem note's final degree step.
   They do not establish that convexity of a squared norm permits the
   flat-direction reduction. This comparison does not validate the
   paper's other, stronger assertions about degree spectra or algebraic
   multiplicities; those assertions are unnecessary here.

4. **G. Khimshiashvili, *Remarks on Quadratic Mappings* (2019).**
   Examined the [publisher abstract and references](https://doi.org/10.1007/s10958-019-4146-4).
   They describe properness, degree, and fibers of quadratic maps,
   including arbitrary-dimensional endomorphisms. The full article was
   not retrieved. It remains a source for further comparison, although
   the available abstract does not state a convex SOS-length result.

5. **Radu-Alexandru Dragomir and Yurii Nesterov, *Convex quartic problems:
   homogenized gradient method and preconditioning*.** Examined Sections
   1–2 of [arXiv:2306.17683v2](https://arxiv.org/pdf/2306.17683v2), dated
   April 2024. Their convex objectives are a quartic form plus a linear
   term. Quadratic least-squares objectives motivate convex subproblems
   through a difference-of-convex decomposition. Proposition 2.1 bounds
   the homogeneous quartic part when its residual quadratic forms are
   positive semidefinite. This is relevant context for quadratic
   least-squares objectives, but gives no lower bound on their number
   of residuals under the present zero and Hessian assumptions.

6. **Bachir El Khadir, *On Sum of Squares Representation of Convex Forms
   and Generalized Cauchy-Schwarz Inequalities*.** Examined the
   introduction and main-result discussion in the
   [author's preprint](https://optimization-online.org/wp-content/uploads/2019/09/7380.pdf).
   Theorem 1.1 proves that convex quaternary quartic forms are SOS. It
   concerns existence of representations, not the lower bound on their
   length considered here. The introduction also explicitly notes that
   homogenization preserves the SOS property but need not preserve
   convexity, so its homogeneous convexity hypothesis cannot simply be
   applied to the homogenization in item 2.

Searches covered combinations of “convex quartic,” “SOS length,” “number
of squares,” “nondegenerate zero,” “regular zero,” “quadratic least
squares,” “proper quadratic map,” and “homogeneous quadratic
endomorphism.” Search results and abstracts were used to locate primary
texts, not to infer that an unexamined paper contains no matching result.
No project tests or CI checks were run for this literature-only audit.
