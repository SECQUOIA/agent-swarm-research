# Prior-art audit: implicit exact output from a sparse convex patch

Date: 2026-10-02. This focused audit compares
[`implicit-convex-patch-certificate.md`](../new-direction/implicit-convex-patch-certificate.md)
and its paired
[`implicit-optimum-precision-obstruction.md`](../new-direction/implicit-optimum-precision-obstruction.md)
with the strongest relevant sources already read in the local literature
collection. It is not a discovery-saturation result or a novelty proof.

## The claims and their boundary

The positive result uses certified global pruning to retain every original
optimizer in a rational mixed box, fixes the integer labels, and verifies
that the polynomial restricted to the remaining continuous box has Hessian
at least `tau I` everywhere. Its unique constrained minimizer is then an
exact optimizer, represented by the rational patch and its polynomial KKT
system. The representation has length and construction cost
`f_d(p, κ) poly(I)`, and supports certified position and value approximation
to `q` bits in `f_d(p, κ) poly(I+q)` work. This requires pointwise global
quadratic growth plus a comparable positive lower bound on the full
continuous Hessian at the optimizer. The latter follows from point growth at
an interior continuous optimum but is an additional condition at a boundary
optimum.

The paired negative result is narrower: a specified degree-four,
width-two, uniformly strongly convex family forces exponentially long
ordinary-binary endpoints if one certificate must be a rational
axis-aligned rectangle on which a weak active-bound derivative sign holds
at every free-coordinate point. The exact derivative range is used, so
interval overestimation is not the cause. This does not lower-bound all
interval or implicit certificates. The convex-patch construction is an
explicit alternative on this family: its rational patch may touch original
bounds, and its proof checks uniform Hessian positivity rather than uniform
active-gradient signs.

## Interval search and convexification

**Neumaier, “Complete Search in Continuous Global Optimization and
Constraint Satisfaction,” Acta Numerica 13 (2004), DOI
[10.1017/S0962492904000194](https://doi.org/10.1017/S0962492904000194).**
This is a broad, rigorous account of interval branch-and-bound, propagation,
convex relaxations, and verification. Its standard global-search certificate
combines valid lower bounds and feasible upper bounds over boxes; interval
derivatives and KKT signs can also prune or reduce domains. It supplies the
methodological background for both the candidate's sound pruning records and
the rectangle sign test. It also records worst-case exponential search,
poor behavior near degeneracy, and finite termination only in special
settings. It does not give an `f(p,κ) poly(I)` total bound or an exact
implicit optimizer representation. Primary locators: box branch-and-bound,
pp. 33–35; interval verification, pp. 63–65; limitations and open questions,
pp. 68–70. [[neumaier2004-complete-search-in-continuous-global]]

**Araya, Trombettoni, and Neveu, “Exploiting Monotonicity in Interval
Constraint Propagation,” AAAI 2010, DOI
[10.1609/aaai.v24i1.7541](https://doi.org/10.1609/aaai.v24i1.7541).**
Their monotonicity-based interval extension can be sharp when repeated
variables are monotone, and interval-Newton narrowing has logarithmic
dependence on requested interval precision. This is a strong comparator for
the exact-range derivative calculation: in the obstruction example the
active derivative is monotone in each of its two coordinates, so the
corner evaluation is already the exact range. A precision logarithmic in
`1/a_n` is still exponential in the path length because
`a_n=2^{-(4·2^n-2)}`. The result does not show that every exact certificate
must refine such a rectangle; the patch theorem avoids that test entirely.
Primary locators: monotonicity extension, pp. 1–2; method and interval
Newton loop, pp. 3–5. [[araya2010-exploiting-monotonicity-in-interval-constraint]]

**Adjiman, Dallwig, Floudas, and Neumaier, “A global optimization method,
αBB, for general twice-differentiable constrained NLPs—I. Theoretical
advances,” Computers & Chemical Engineering 22(9), 1998, DOI
[10.1016/S0098-1354(98)00027-1](https://doi.org/10.1016/S0098-1354(98)00027-1).**
The αBB method builds valid convex underestimators using Hessian bounds and
performs spatial branch-and-bound; it has convergence guarantees to
arbitrarily accurate global solutions. This is the closest convexification
and local-box closure precedent. The candidate instead prunes to a box that
contains every global optimizer, then verifies convexity of the *original*
restricted objective and returns its exact constrained minimizer as an
implicit representation. αBB does not provide the candidate's sparse
tree-DP, quantitative growth-conditioned bit count, or exact KKT patch
output. Primary locators: αBB underestimator and Hessian test, §§2–3,
pp. 2–9; finite `ε`-convergence statement, abstract and §2.
[[adjiman1998-a-global-optimization-method-bb]]

**Burer and Vandenbussche, “A finite branch-and-bound algorithm for
nonconvex quadratic programming via semidefinite relaxations,” Mathematical
Programming 113(2), 2008, DOI
[10.1007/s10107-006-0080-6](https://doi.org/10.1007/s10107-006-0080-6).**
Their Theorem 3.3 proves finite, correct global branch-and-bound for
nonconvex QP, using branching on KKT complementarity and SDP relaxations.
It is a direct precedent for exact global KKT-driven search. Its finite
termination does not come with the candidate's parameterized node/bit bound;
the paper treats a quadratic objective and SDP subproblems, not sparse
fixed-degree polynomial factors plus a verified convex patch. It therefore
precludes a broad claim that finite exact global optimization or KKT-based
branching is new, but not the stated conditioned patch result. Primary
locators: finite branching and SDP method, §§2–3; Theorem 3.3, local PDF
pp. 10–12 (printed pp. 269–271).
[[burer2008-a-finite-branch-and-bound]]

## Sparse polynomial and treewidth methods

**Bienstock and Muñoz, “LP Formulations for Polynomial Optimization
Problems,” SIAM Journal on Optimization 28(2), 2018, DOI
[10.1137/15M1054079](https://doi.org/10.1137/15M1054079), arXiv:1501.00288.**
Their treewidth-based LP approximations cover mixed-integer polynomially
constrained models and show that sparse polynomial optimization has strong
approximation precedents. The general formulation size scales as
`(2π/ε)^(ω+1) n log(π/ε)` for degree `π` and width `ω`; their exact bounded-
treewidth reformulation is for a finite binary CSP. The candidate is more
restricted in its feasible-set geometry, but under a quantitative growth
and curvature condition it has logarithmic dependence on accuracy and an
exact implicit optimizer description. It does not yield a compact LP or
handle the general polynomial constraints of their model. Primary locators:
Theorems 4 and 9, pp. 2–5; tolerance and width dependence, pp. 24–25.
[[bienstock2018-lp-formulations-for-polynomial-optimization]]

**Del Pia and Khajavirad, “Treewidth and the complexity of box-constrained
quadratic programs,” arXiv:2609.35595 (2026).** Their exact forest dynamic
program is a close sparse global-optimization comparator for quadratic
objectives. They also prove strong NP-hardness at treewidth two for box QP,
and for quartic box minimization even on a path. The hardness results show
that structural width alone is insufficient for a broad polynomial
optimization claim. They do not establish hardness under the candidate's
global growth and full-Hessian condition, nor do they supply an exact
implicit optimizer output under that promise. Primary locators: forest
algorithm, pp. 3–4; quartic path hardness, p. 18; width-two QP hardness,
pp. 20–24. [[pia2026-treewidth-and-the-complexity-of]]

The exact pruned-grid arithmetic and min-marginal pruning used here are
already developed in the local
[`pruned-coordinate-grid.md`](../new-direction/pruned-coordinate-grid.md)
and extended to fixed-degree polynomial factors in
[`polynomial-pruned-grid-extension.md`](../new-direction/polynomial-pruned-grid-extension.md).
Thus the convex-patch theorem should not be framed as inventing sparse
global pruning or semiconcave grid correction. Its added step is a
checked local Hessian certificate after global retention and integer-label
recovery.

## What “exact implicit output” means

Polynomial KKT equations for a strongly convex box problem are standard; so
are real-algebraic representations such as an isolating interval or a
univariate representation with a Thom encoding. Basu's real-algebraic
geometry survey describes these standard exact representations and their
dimension-sensitive algorithms. They do not supply this theorem's global
optimization proof or its treewidth-and-conditioning bit bound. The
candidate's exact object is deliberately not an expanded minimal polynomial:
it is a rational polynomial KKT system whose unique solution is certified
by (i) a global pruning trace showing that the retained patch contains every
global optimizer and (ii) an exact rational Hessian certificate showing the
restricted objective is strongly convex throughout the patch. The KKT
system alone would not establish either fact. [[basu2014-algorithms-in-real-algebraic-geometry]]

The full-Hessian condition is a real limit, not a formatting technicality.
At a boundary optimum, pointwise quadratic growth does not imply a positive
full Hessian; even when that Hessian is positive, its smallest eigenvalue
may be exponentially small while point growth and upper coordinate
curvature stay moderate. The example in §7 of the candidate note also has
an easy globally certifiable active-face elimination, so it limits this
particular patch strategy rather than all implicit representations. The
paired rectangular-sign obstruction makes the complementary point: exact
whole-box KKT-sign tests can require long endpoints, while a correlated
implicit proof or a strongly convex patch can avoid those endpoints.

## Assessment

The audited sources already contain all of the main ingredients at a broad
level: spatial branch-and-bound, interval KKT signs, convex underestimators,
finite KKT branching, sparse polynomial LP approximations, and exact
tree-decomposition algorithms for special quadratic cases. The focused
contribution to assess is their composition into a compact exact optimizer
representation with an input-size bound parameterized by bag width and the
growth/curvature ratio, plus arbitrary-precision evaluation. The rectangle
lower bound is only for the specified independent-coordinate active-sign
certificate. The patch theorem supplies a reviewed escape for the example
under its stronger full-Hessian condition; neither result excludes other
global or implicit certificate forms.

All sources cited here have readable primary text in the existing local
packages. No new literature candidate was identified, and no literature-KB
files were changed.
