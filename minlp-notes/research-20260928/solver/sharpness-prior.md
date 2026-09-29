# Prior-work audit for the fixed quadratic sparse lower bound

Date: 2026-09-28. This is an independent source and significance audit of
[quadratic-sharpness.md](quadratic-sharpness.md), with comparison to
[sparse-kernel-rounding.md](sparse-kernel-rounding.md). It does not certify
priority or replace the separate proof review.

The strongest claim still supported by this audit is a **fixed quadratic
example with a sharp inverse-square sparse hierarchy gap**, despite a
degree-four dense certificate. Sparse nonattainment itself, its explanation
by nonpolynomial separator functions, and the duality between moment
matching and uniform polynomial approximation all have direct precedents.
Those ingredients must not be described as new.

## The precise candidate distinction

The candidate has two bags `{x,y}` and `{y,z}`, with
`x,z in [0,1]`, `y in [-1,1]`, and

\[
f=x^2-2xy+y^2+z^2+2yz.
\]

Its fiber optima cancel through `h(y)=(max(y,0))^2`. The note proves that
the exact-local-measure relaxation with separator moments through degree
`n` has value `-2E_n(h)`. It then constructs matching actual measures with
objective at most `-c/n^2`. This supplies a lower bound for every local
preordering relaxation using only those separator moments, independently
of local positivity truncation. The companion rounding theorem supplies
the matching upper bound for the stated sparse box preordering.

The candidate improvement over the closest obstruction below is therefore
the objective degree, the nonsmooth separator, and the resulting matching
quantitative exponent. The elementary Fejer witness is a proof device for
this comparison; the audit has not established a new approximation theorem.

## Closest primary sources

1. **Nie, Qu, Tang, and Zhang, “A characterization for tightness of the
   sparse Moment-SOS hierarchy,” Mathematical Programming 215 (2026),
   369–405; online 2025; preprint 2024.**
   [Primary article](https://link.springer.com/article/10.1007/s10107-025-02223-2),
   Theorems 3.1–3.2, Assumption 4.1, and Example 6.7.
   Their three-variable, two-bag quartic on a box is dense-exact but has
   no nonnegative polynomial bag decomposition. Its fiber minima force
   a rational separator. The local rational example in
   [prior-independent.md](prior-independent.md) is a rediscovery of this
   mechanism; that note now gives the exact affine objective relation and
   the necessary domain caveat. Example 6.7 gives no inverse-square lower
   rate. A rational function analytic on the interval cannot automatically
   supply the new nonsmooth approximation obstruction.

2. **Grimm, Netzer, and Schweighofer, “A note on the representation of
   positive polynomials with structured sparsity” (2007).**
   [Open author manuscript](https://www.math.uni-konstanz.de/~grimm/sparse.pdf),
   Lemma 3 and its proof. Under running intersection and strict positivity
   on a product of compact sets, they approximate a continuous separator
   fiber minimum by a polynomial to obtain positive bag polynomials.
   Strict positivity permits approximation slack. The candidate examines
   the zero-margin obstruction and measures its cost; the separator
   construction is established.

3. **Korda, Magron, and Rios-Zertuche, “Convergence rates for
   sums-of-squares hierarchies with correlative sparsity” (2024 online;
   2025 volume).**
   [Primary article](https://link.springer.com/article/10.1007/s10107-024-02071-6),
   Theorem 6 and Section 3. Their sparse preordering guarantee has exponent
   `2/(w+3)` for fixed data and largest bag size `w`. Their proof already
   controls separator approximation and applies sparse Jackson operators.
   See [kernel-prior.md](kernel-prior.md) for the cone and degree-convention
   comparison. The new pair of candidate theorems would replace that
   exponent by two and show that two is optimal for the same fixed-bag
   framework. This paper is an upper-bound benchmark, not a matching
   lower-bound precedent located by the audit.

4. **Han, Jiao, and Weissman, “Local moment matching: A unified
   methodology for symmetric functional estimation and distribution
   estimation under Wasserstein distance,” COLT 2018.**
   [Primary proceedings paper](https://proceedings.mlr.press/v75/han18b/han18b.pdf),
   Lemma 25, printed pages 23–24. It states explicitly that the maximal
   difference of integrals of a continuous function over probability laws
   sharing the first `n` moments is twice its degree-`n` best uniform
   polynomial approximation error. Their interval is written with a
   positive left endpoint; an affine translation gives the candidate's
   interval, preserving degree and moment agreement. Thus Proposition 1
   uses classical duality in an optimization-specific construction. The
   abstract Hahn–Banach/Riesz argument is not an original contribution.

5. **Baldi and Slot, “Degree bounds for Putinar's Positivstellensatz on
   the hypercube,” SIAM Journal on Applied Algebra and Geometry 8 (2024),
   1–25.**
   [Primary current preprint](https://arxiv.org/html/2302.12558v3),
   Theorem 4 and Section 2.4. Their degree lower bound for
   `(1-x_1^2)(1-x_2^2)+epsilon` in the dense box quadratic module is
   `Omega(epsilon^(-1/8))`, giving an `Omega(r^-8)` hierarchy gap for the
   corresponding fixed polynomial. It is a different obstruction: the
   polynomial is already in the dense preordering at degree four. The
   candidate instead loses strength by restricting bags, even after all
   products of box inequalities are allowed locally. Neither lower bound
   subsumes the other.

6. **Laurent and Slot, “An overview of convergence rates for sum of
   squares hierarchies in polynomial optimization” (2026).**
   [Open published chapter](https://ir.cwi.nl/pub/36052/36052.pdf),
   Section 4.1, printed page 172. It distinguishes sharp upper-density
   rates from the less understood lower hierarchies and identifies closer
   quantitative lower bounds, including Schmudgen-type examples, as a
   research direction. This supports the significance of a sharp sparse
   example. It does not imply that the candidate resolves the dense
   question: the candidate's dense bound is exact. The survey's dense
   Putinar upper-rate discussion predates the later 2026 improvement
   recorded in [kernel-prior.md](kernel-prior.md).

7. **Khajavirad, “Tight semidefinite programming relaxations for sparse
   box-constrained quadratic programs,” February 2026 manuscript.**
   [Primary open report](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_003.pdf),
   introduction, Lemma 4, and Section 6. The paper strengthens SDP
   relaxations by combining them with reformulation-linearization
   constraints and proves exact representability under graph conditions.
   Its stated sufficient condition excludes three positive diagonal nodes
   with two connecting edges, which the candidate has. Its gluing lemma
   also requires no positive diagonal terms on the overlap. Thus it does
   not imply exactness of the candidate's two-bag hierarchy. These results
   nevertheless rule out describing the candidate as a limitation of
   every sparse SDP formulation: different lifts and additional monomials
   can carry information absent from the prescribed bags.

8. **Zheng and Fantuzzi, “Sum-of-squares chordal decomposition of
   polynomial matrix inequalities” (2021 preprint version).**
   [Primary text](https://arxiv.org/html/2007.11410v2), Proposition 2.1,
   Example 2.2, and Theorem 2.2. The paper gives a globally positive
   definite polynomial matrix on a three-node path with no polynomial
   positive semidefinite clique decomposition, and establishes
   decompositions after a suitable SOS multiplier. This is another direct
   precedent for the distinction between polynomial and rational clique
   representations. Its counterexample uses behavior at infinity and
   polynomial matrix coefficients. Scalarization increases the total
   degree, so it is not the candidate's scalar quadratic compact-box
   example. The source does not give the candidate's hierarchy rate.

## Additional delegated cross-check

A fresh child auditor inspected **Nie and Demmel, “Sparse SOS relaxations
for minimizing functions that are summations of small polynomials”
(2009)**, [primary preprint](https://arxiv.org/abs/math/0606476),
Examples 3.5 and 3.8 and Corollary 3.6 in the open preprint; final
published numbering was not checked. Example 3.8 is a quadratic gap
using three pair bags without running intersection. It does not establish
the candidate's two-bag, running-intersection phenomenon. Corollary 3.6
gives equality in the unconstrained quadratic setting under running
intersection; the candidate's interval restrictions are essential.
Example 3.5 is a different quartic gap at a specified order. This paragraph
records the child's primary-text inspection, rather than a second full
reading by the author of this note.

## Significance and limits

Assuming the independent proof checks pass, the strongest consequence is
a precise explanation of what finite separator information can cost:
arbitrarily strong local positivity cannot eliminate this gap while the
overlap information remains fixed. It is particularly informative that
quadratic objective smoothness does not prevent a separator value function
from having the approximation behavior that forces the gap.

This is a limitation of the specified hierarchy, not optimization
hardness. The three-variable problem is explicitly solvable. Its zero
set contains a continuum of minimizers, and no generic convergence or
typical solver-performance claim follows. The matching exponent concerns
the sparse box preordering; it does not prove a matching upper bound for
the weaker sparse quadratic module, or a lower bound for dense
preorderings. With linear endpoint generators the dense certificate can
be written at degree two as `(y-x+z)^2+2xz`; the degree-four statement in
the candidate uses the standard quadratic interval generators. Generator
conventions should remain explicit.

Possible solver responses include separator partitioning, richer overlap
features, or adding the missing joint bag. Their practical value requires
separate analysis and experiments. In particular, a rational feature
basis does not exactly represent the piecewise polynomial `y_+^2` on the
whole interval without a domain split.

## Search and verification record

Searches covered sparse finite convergence, nonnegative polynomial bag
decomposition, rational separator functions, continuous graphical-model
moment constraints, sharp sparse Schmudgen rates, degree lower bounds,
and sparse box quadratic SDP formulations. Exact-polynomial and
positive-part queries were also tried. The primary sources above were
read at the stated locations. The existing source audits supplied the
broader kernel context. The exact identity involving the rational prior
was checked by a targeted Python/SymPy script: both the affine objective
residual and transformed dense SOS residual were zero. No project-wide
verification or CI inspection was performed.

No identical fixed quadratic inverse-square example was located in the
inspected sources. That negative search result does not prove novelty.
Before making a priority claim, check further citation descendants of
Nie–Qu–Tang–Zhang and Korda–Magron–Rios-Zertuche, older approximation
results for truncated powers, and polynomial-message formulations in
continuous graphical models. The present defensible wording is a
candidate sharp sparse bound with a carefully delimited comparison to
known results.
