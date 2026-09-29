# Prior results for finite mixed-integer convex semialgebraic values

Date: 2026-09-28. Status: primary-literature comparison and independent
geometric check, with [fresh adversarial review](generic-convex-mixed-value-prior-review.md).
This note evaluates the scope of the theorem in
[the multiple-integer frontier](unbounded-misocp-multiple-integer-frontier.md).
It does not replace that theorem's proof or its
[adversarial review](multiple-integer-bounded-forms-review.md).

## 1. Assessment and exact question

No equivalent quantitative theorem was found in the primary sources
examined below. This is a qualified search result, not a novelty claim.
The strongest direct predecessor is Khachiyan--Porkolab (2000), including
its geometric dimension reduction and algebraic affine-hull treatment.
The qualitative slice argument is a consequence of classical
lattice-free geometry. Its ingredients, and the removal of atom count
from coefficient-sensitive continuous bounds, should not be presented as
new.

The proposed quantitative addition concerns a convex upward closed set
\(E\subseteq\mathbb R^k\times\mathbb R\), described by arbitrary
Boolean combinations of integer polynomial atoms of degree at most
\(d\ge2\) and individual coefficient bit length at most \(H\ge1\).
There are \(m\) atoms. For

\[
 \theta=\inf\{t:(z,t)\in E,\ z\in\mathbb Z^k\}\in\mathbb R,
\]

the proposed conclusion bounds the minimal-polynomial degree by
\(d^{G(k)}\), its coefficient bit length by
\((H+1)d^{G(k)}\), and, if attained, the bit length of some optimal
integer vector by the latter bound. The infimum need not be attained;
neither \(E\) nor its integer-coordinate projection need be closed.
The bounds are independent of \(m\). A formula with quantified real
variables is first reduced using degree and height bounds that depend on
the quantified dimensions. This does not assert an algorithm independent
of formula length.

The meaningful distinction from a pure integer objective is that a
minimizing sequence can have unbounded integer coordinates and a finite
limit strictly below every individual integer fiber's infimum.
Optimizing an additional *integer* objective coordinate only rounds the
value and does not supply its algebraic degree or height.

## 2. Closest quantitative and geometric predecessor

Khachiyan--Porkolab, *Integer Optimization on Convex Semialgebraic Sets*,
Discrete & Computational Geometry 23 (2000), 207--224, is the main
comparison. The complete primary text is also stored under
`literature/papers/khachiyan2000-integer-optimization-on-convex-semialgebraic/`.

Theorem 1.1, p. 208, gives a small optimal integer vector for minimization
of an integer coordinate over \(Y\cap\mathbb Z^k\), with size bounded
in terms of input degrees, coefficient lengths and quantified dimensions,
independently of the number of atoms. Theorem 1.2 gives an algorithm whose
running time does depend on the atom count. Neither statement treats a continuous
objective coordinate with integer escape and an unattained finite limit.

Two proof ingredients are especially close. Theorem 3.1(ii), p. 215,
places a full-dimensional convex semialgebraic set with no interior
integer point in a slab with a controlled integral normal. In Theorem
3.4, p. 220, algebraic affine equations are expanded in a common number
field to produce rational equations containing the integer points.
These are direct predecessors of the proposed bounded-form and
deficient-dimension reductions. The paper also treats algebraic
polyhedral coefficients in fixed total dimension; handling algebraic
coefficients by itself is not new.
[Primary PDF](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)

Lovasz's maximal lattice-free-set theorem supplies the nonquantitative
slab statement. Convenient primary proofs are Basu--Conforti--Cornuejols--
Zambelli, revised May 2010 author version, Theorem 2, pp. 2--3, Theorem
10, p. 8, and containment Corollary 20, p. 15; and Averkov (2011),
Theorems 1--2, p. 1. A full-dimensional maximal lattice-free set is a
polyhedron with rational linear recession space, hence has a nonzero
integral linear form bounded on it. Lower-dimensional maximal sets can
be irrational affine hyperplanes. The full-dimensional qualification is
essential.
[BCCZ primary PDF](https://www.andrew.cmu.edu/user/gc0v/webpub/lattice-free-May2010.pdf),
[Averkov primary PDF](https://arxiv.org/pdf/1110.1014)

## 3. The qualitative slice consequence

The following argument was independently reconstructed during this
audit. No inspected source stated this exact conclusion, but its proof
uses the classical theorem just cited.

**Qualitative consequence.** For any convex upward closed epigraph
\(E\), with nonempty mixed-integer domain and finite mixed-integer
infimum \(\theta\), there is an affine lattice slice
\(z=z_0+Ty\), where \(z_0,T\) are integral and the columns of \(T\)
are a lattice basis, such that the continuous infimum on this slice
equals \(\theta\). The dimension of \(y\) may be zero. No
semialgebraicity is required for this existence statement.

Here is a proof outline recording the relevant qualifications. Fix a
finite cap \(V>\theta\). If its strict projected sublevel \(C_V\)
has deficient affine dimension, replace the ambient space by the rational
affine hull of \(C_V\cap\mathbb Z^k\). This hull is proper and has
an integer point and an integral lattice basis; restricting to it
preserves the mixed-integer infimum. Apply this preprocessing at every
stage.

In full dimension, let \(\alpha\) be the continuous infimum. If
\(\alpha=\theta\), stop. Otherwise choose
\(\alpha<U<\theta\). The set \(C_U\) is full-dimensional: combine
a point below \(U\) with a sufficiently small fixed fraction of
\(C_V\). It contains no integer point. Its closure remains
lattice-free because a full-dimensional convex set and its closure have
the same interior. Classical maximal lattice-free geometry gives a
nonzero integral form \(a\) bounded on \(C_U\). The same convex
interpolation, with a fixed point strictly below \(U\), shows that
\(a\) is bounded on \(C_V\). A mixed-integer minimizing sequence in
\(C_V\) therefore takes only finitely many integral values of
\(a^Tz\). One slice \(a^Tz=b\) preserves a minimizing subsequence.
Restrict to it and repeat. At most \(k\) reductions are possible.

For rational semialgebraic \(E\), this qualitative consequence already
implies that every finite mixed-integer infimum is real algebraic. It
also gives a dimension-dependent algebraic degree bound: rational affine
substitution preserves atom degrees regardless of coefficient size, and
one-block real quantifier elimination bounds the degree of the endpoint
polynomial in terms of those degrees and the remaining dimension. The
selected slice may have uncontrolled coefficients, so this argument
does not bound the value's height. The proposed coefficient-sensitive
theorem controls the slice without putting the unknown \(\theta\)
into its input. The height and small integer-assignment conclusions
require that additional quantitative proof and novelty assessment.

## 4. Results that appear broader until their hypotheses are checked

**Koppe's survey and Bank et al.** Section 6.2 of Koppe's 2010 survey
starts with a mixed-integer formulation. Nevertheless, Theorem 6.3,
pp. 16--17, explicitly optimizes over \(F\cap\mathbb Z^n\), as do
the relevant following algorithmic statements. Its cited Bank--Heintz--
Krick--Mandel--Solerno (1993) Theorem 2, p. 301, bounds a radius preserving
the optimum of integer-coefficient globally quasiconvex polynomial
optimization over an entirely integer domain. Inspection of that primary
theorem resolves the possible ambiguity in the survey heading. It does
not bound a possibly unattained real mixed-integer value.
[Survey](https://arxiv.org/pdf/1006.4895),
[Bank et al. primary PDF](https://www.numdam.org/item/BSMF_1993__121_2_299_0.pdf)

**Older mixed-integer attainment and boundedness.** Bank--Mandel's
parametric results, and Obuchowska's 2008 boundedness results, are
substantive predecessors for rational globally quasiconvex polynomial
systems, including native positive-semidefinite quadratic inequalities.
The repository's earlier primary-source audits explain their stability,
recession, and decomposition hypotheses. They do not cover an arbitrary
convex semialgebraic epigraph, which may have an unattained finite
mixed-integer value. A conic description cannot simply be replaced by a
globally quasiconvex polynomial system after squaring its rows.
[Attainment audit](mixed-integer-attainment-prior.md),
[boundedness audit](succinct-unboundedness-prior.md),
[Obuchowska publisher page](https://link.springer.com/article/10.1007/s00186-007-0196-3)

**Exact conic values with bounded integer variables.** Friberg's 2016
thesis explicitly computes a pair consisting of the value and its
attainment status. Theorem 5, p. 41, proves finite termination of its
branch-and-bound Algorithm 3 under Assumption 1, which requires exact
relaxation value/attainment computation and extraction of a possibly
fractional assignment of the integer coordinates attaining that pair.
Formulation (4.1), p. 39, bounds every integer
variable between finite integer endpoints. Thus finite termination and
recognition of conic nonattainment are established ideas. The theorem
does not handle escape of unbounded integer assignments or give the
arithmetic bounds sought here.
[Primary thesis](https://backend.orbit.dtu.dk/ws/portalfiles/portal/125210367/main.pdf)

## 5. Duality and continuous algebraic optimization

Baes--Oertel--Weismantel, *Duality for mixed-integer convex minimization*,
Theorem 7, p. 9, gives an exact multiplier dual under compactness and a
mixed-integer Slater condition. The following remark, p. 10, expressly
discusses dropping assumptions and replacing minimum/maximum by
infimum/supremum. It would therefore be inaccurate to exclude the entire
paper merely because a primal infimum is unattained. Its certificates and
duality statements do not give the proposed algebraic degree/height
bound or an integral affine slice preserving the value.
[Primary PDF](https://arxiv.org/pdf/1412.2515)

Moran--Dey--Vielma, Proposition 4.5, pp. 5--6, proves continuous versus
mixed-integer unboundedness equivalence when a convex set contains a
mixed-integer point in its interior. Kocuk--Moran (2019), Theorem 2.12,
p. 5 of the final author version, extends a related finiteness property
using Dirichlet convex sets. These proofs use lattice-free geometry, and
their subadditive-duality results are relevant even without primal
attainment. The finiteness property compares whether an objective is
bounded; it does not equate finite values or provide their algebraic
encoding bounds.
[Moran--Dey--Vielma primary PDF](https://www2.isye.gatech.edu/~sdey30/paper_conic_duality_siam_v9.pdf),
[Kocuk--Moran final author PDF](https://research.sabanciuniv.edu/id/eprint/37541/2/ExtendedDualFINAL.pdf)

Continuous algebraic value bounds are also established. Jeronimo--
Perrucci--Tsigaridas (2013), Theorem 1, p. 2, bounds the degree and
separation from zero of a polynomial minimum on a compact connected
component. Its Theorem 12, p. 11, allows a noncompact domain with a
compact minimizer set. El Hilany--Tsigaridas (2024), Theorem 1,
pp. 4--5, addresses continuous finite infima for a class with smooth
complete-intersection hypotheses. These are continuous results.
[JPT primary PDF](https://arxiv.org/pdf/1112.0544),
[El Hilany--Tsigaridas primary PDF](https://arxiv.org/pdf/2407.17093)

In particular, independence from atom count is not itself a new
continuous phenomenon. Basu--Mishra, Handbook chapter 37, p. 990,
explicitly explains how the number of distinct integer polynomials of
bounded degree and coefficient size absorbs a logarithmic atom-count
term into a bound of the form \(H d^{O(k)}\). This observation concerns
description bounds, not running time or the integer-infimum reduction.
[Primary chapter](https://www.csun.edu/~ctoth/Handbook/chap37.pdf)

## 6. Search and verification record

The search covered convex semialgebraic integer optimization, algebraic
mixed-integer objective values, unattained mixed-integer conic infima,
bounded linear forms/barrier cones, rational affine slices, maximal
lattice-free sets, Dirichlet sets, and mixed-integer duality. Two agents
independently searched the arithmetic-value and lattice-free literature.
The root audit rechecked the decisive KP, Koppe/Bank, Friberg, duality,
and atom-count statements in the primary documents.

The original Bank--Mandel 1988 theorem text was not obtained in this
search. Accessible book previews contain introductory material rather
than all theorem pages. Related 1987 primary results and later
attributions are documented in the earlier local attainment audit; no
unread 1988 theorem is asserted here to resolve the present question.
The earlier local audit, rather than a new successful PDF download, is
the source for the detailed Obuchowska comparison.

The strongest defensible positioning is therefore: a proposed
coefficient-sensitive extension of classical convex semialgebraic
integer dimension reduction to a continuous objective, including
unattained finite infima. Establishing publication-level originality
still requires expert comparison with older parametric integer
optimization and any equivalent value-encoding formulations. An
unsuccessful search does not settle that question.

Targeted verification consists of the primary theorem inspections above,
the independent qualitative argument in Section 3, and a Python check of
this file's final newline, trailing whitespace, control characters,
balanced inline/display math delimiters, and five relative Markdown links.
That check passed. No project-wide checks or CI inspection were performed.
