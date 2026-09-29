# Prior audit: one unrestricted PSD quadratic numerator

Date: 2026-09-28. Status: focused primary-source audit. This compares the
proposed [quadratic-over-affine value theorem](common-range-quadratic-fractional.md) and its
[optimizer construction](common-range-quadratic-fractional-witness.md).
It does not certify those proofs or establish priority.

The strongest fractional comparator is Chandrasekaran--Tamir (1984):
exact algebraic values and attainment decisions for continuous convex
quadratic fractional optimization over polyhedra are established results,
including unbounded domains. Del Pia supplies the strongest inspected
fixed-integer-dimension threshold algorithm. No inspected source states
the proposed full mixed-integer theorem, even its polyhedral special
case, but that limited search finding is not a novelty claim.

The proposed claim is exact optimization of \(q_0(z,x)/d(z,x)\), where
\(q_0\) has a rational jointly PSD Hessian of arbitrary rank and \(d\)
is rational affine and positive on the real feasible domain. The native
domain consists of rational SOC or PSD quadratic constraints and affine
rows. The parameter is the integer dimension \(k\) and the cross-aware
common continuous range \(\rho\) of the native constraints, excluding
the numerator. The requested output includes infeasibility, unboundedness
below, exact finite algebraic value, attainment, and a full optimal point,
in \(f(k,\rho)N^C\) bit operations with absolute \(C\).

**The continuous polyhedral base case is old.**
[Chandrasekaran and Tamir, *Optimization problems with algebraic
solutions: Quadratic fractional programs and ratio games*, Mathematical
Programming 30 (1984), 326--339](https://www.math.tau.ac.il/~atamir/opt_84.pdf),
[DOI 10.1007/BF02591937](https://doi.org/10.1007/BF02591937), assume a
nonempty rational polyhedron, a convex quadratic numerator nonnegative
on it, and a concave quadratic denominator positive throughout it
(p. 327). An affine denominator is included. Section 3 constructs an
integer polynomial and isolating interval for the value in polynomial
time. Page 334 removes the initial attainment assumption and explicitly
gives polynomial-time infimum representation and attainment decision.
Page 338 explains polynomial-time reduction to a minimal polynomial.

This is exact algebraic computation, not an approximation theorem.
The proof uses parametric QPs, algebraic separation, and rational queries
without enumerating all pieces. For affine denominators, pp. 330--331
credit an earlier piecewise-quadratic algorithm. I inspected pp. 326--334
and 338--339, but not that earlier paper or a separate full-coordinate
output guarantee. Nonnegative numerator is a literal hypothesis;
arbitrary-sign classification requires an additional reduction. No
integer variables occur in this result.

The elementary example

\[
             \min_{x\ge1}\frac{x^2+2}{x}=2\sqrt2,
             \qquad x_*=\sqrt2,
\]

therefore illustrates an established phenomenon. Its derivative is
\(1-2/x^2\), which changes sign at \(\sqrt2\). Adding unconstrained
integer variables leaves the value unchanged. In particular, rational
polyhedral data and \(\rho=0\) do not imply a rational fractional
optimum. A rationale based only on rational optimal values of ordinary
convex QPs would be incorrect.

**The fixed-integer-dimension threshold oracle is also prior work.**
[Del Pia, *Convex quadratic sets and the complexity of mixed integer
convex quadratic programming*, arXiv v2](https://arxiv.org/html/2311.00099v2),
Proposition 4, solves feasibility for a rational polyhedron intersected
with one rational PSD quadratic inequality in FPT time parameterized by
the number of integer variables. Continuous dimension and quadratic rank
are unrestricted. Theorem 3 exactly optimizes a convex quadratic over
a mixed-integer polyhedron, including infeasibility and unboundedness.
Its Section 4.4 proof uses rational optimal-value bounds. These statements
and the proofs' scope were inspected.

For every rational \(t\), the ratio threshold is exactly
\(q_0-t d\le0\), a PSD quadratic row with the same Hessian as
\(q_0\). Thus Proposition 4 directly covers rational thresholds when
the domain is a polyhedron and positivity is promised on it. It does
not itself supply a finite algebraic fractional-value bound, attainment
test, or recovery at an irrational threshold. Theorem 3 does not state
fractional optimization. The proposed unbounded mixed-integer composition
must prove those additional steps; citing binary search alone is
insufficient.

**A perspective transformation does not directly settle the mixed case.**
This is a reduction check, not a literature claim. On a polyhedron
\(Aw\le b\), set \(s=1/d(w)>0\) and \(y=sw\). The transformed
objective is the convex perspective

\[
 s q_0(y/s)=\frac{y^TQ_0y}{2s}+a_0^Ty+c_0s,
\]

with affine constraints \(Ay\le bs\) and the denominator normalization.
But the original integer coordinates require
\(y_z/s\in\mathbb Z^k\). Replacing this by \(y_z\in\mathbb Z^k\)
changes the feasible set; keeping integer \(z\) introduces the bilinear
equalities \(y_z=sz\). Consequently the elementary continuous
transformation is not a direct reduction to Del Pia's rational
mixed-integer convex QP model. This obstruction does not prove that no
other reduction exists.

[Letchford, Ni, and Zhong, *Bi-perspective functions for mixed-integer
fractional programs with indicator variables*, Mathematical Programming
190 (2021), 39--55](https://link.springer.com/article/10.1007/s10107-020-01519-9),
provides relevant perspective-based mixed-integer reformulation work.
Its introduction and stated results concern convex envelopes and cuts
for fractional problems with indicators, supported by computational
experiments. They do not state the fixed-\(k\), unbounded-integer,
exact-algebraic theorem under comparison.

**The conditional QP charts and minimum-norm selection have established
predecessors.**
[Spjøtvold, Tøndel, and Johansen, *Unique Polyhedral Representations of
Continuous Selections for Convex Multiparametric Quadratic Programs*,
ACC 2005, pp. 816--821](https://skoge.folk.ntnu.no/prost/proceedings/acc05/PDFs/Papers/0149_WeB08_6.pdf),
Equation (1) and Theorem 1, treat fixed-Hessian, fixed-matrix QPs with
affine parameters and piecewise affine optimizer selections. Section IV
allows singular PSD Hessians; Lemma 3 uses a secondary strictly convex
QP to select the least-norm optimizer. Proposition 1 uses constancy of
the quadratic gradient over an optimal set. These passages were
inspected. The exposition assumes a full-dimensional parameter domain
and discards lower-dimensional regions in Remark 1, so the proposed
all-degeneracies chart proof remains necessary.

The quartic degree count follows by substituting quadratic parameter
monomials into classical affine solution pieces, then into the quadratic
numerator. It should be attributed as a consequence of parametric-QP
structure. The new theorem, if proved, concerns the use of these
potentially exponentially many charts only for coefficient and degree
bounds, followed by an FPT algorithm that does not enumerate them.
The rational-threshold oracle, small canonical output, and constructive
recovery are separate obligations.

**Other fractional and fixed-dimensional results have different scope.**
[Zhong and You, *Globally convergent exact and inexact parametric
algorithms for solving large-scale mixed-integer fractional programs and
applications in process systems engineering* (2014)](https://www.sciencedirect.com/science/article/abs/pii/S0098135413003396),
uses general mixed-integer fractional objectives and root-finding
algorithms. The accessible primary introduction and formulation specify
a nonempty compact bounded feasible region and positive denominator.
The abstract's word “exact” does not establish symbolic algebraic output
or FPT bit complexity. Only the publisher's abstract, introduction, and
section excerpts were accessible in this audit; no stronger negative
claim about its full text is made.

[Hildebrand and Köppe, *A new Lenstra-type Algorithm for Quasiconvex
Polynomial Integer Minimization with Complexity* \(2^{O(n\log n)}\)](https://arxiv.org/pdf/1006.4661)
has an exact quasiconvex polynomial optimization theorem, but its
Equation (1) requires every optimization coordinate to be integral.
It does not directly describe a free continuous algebraic optimum.
The detailed theorem and output-bound comparison is in the existing
[quasiconvex prior audit](quasiconvex-mixed-value-prior.md).

The same audit records Espinoza--Fukasawa--Goycoolea's primary result for
mixed-integer **linear** fractional programs on possibly unbounded
rational polyhedra, including asymptotic solutions. It is a relevant
nonattainment predecessor, but not a quadratic-numerator theorem.
Likewise an approximation scheme with runtime polynomial in
\(1/\epsilon\) is not a polynomial-time exact-algebraic algorithm merely
because arbitrarily small tolerances are allowed. Results fixing the
total number of continuous and integer variables also do not establish
the proposed bound, which leaves continuous dimension unrestricted.

The defensible significance statement is therefore a precise complexity
extension: one full-rank convex quadratic numerator, many native
quadratic or conic constraints controlled by \(\rho\), and unrestricted
integer domains controlled by \(k\), together with exact value and output.
The continuous polyhedral exact-value and attainment claims, the
rational-threshold reduction, and the parametric-QP ingredients should
not be presented as new individually. Whether the fixed-\(k\)
polyhedral fractional corollary already follows from another published
theorem remains a literature question after this focused search.
No claim is made that every unattained mixed-integer polyhedral value
is rational, or that every attained one has degree at most two.

Verification and search record: searches covered “quadratic fractional”
with “fixed parameter”, “fixed dimension”, “polynomial time”, “integer
variables”, “Lenstra”, and “Del Pia”, plus the identified primary citation
chains. Source inspection used the web primary texts and local
`curl`, `pdftotext -layout`, `pdftoppm`, and `tesseract`; the scanned 1984
attainment passage on printed p. 334 was also inspected as an image.
The PDF and OCR files are temporary audit aids under
`/tmp/quadratic-fractional-prior/`, not repository artifacts.
`git diff --check -- research-20260927/common-range-quadratic-fractional-prior.md`
passed. A targeted Python `Path.is_file()` check confirmed all local
Markdown links. No project-wide verification or CI inspection was
performed.
