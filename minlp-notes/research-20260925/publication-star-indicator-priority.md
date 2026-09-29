# Publication audit: indicator-quadratic prior results

Date: 2026-09-25. This is a primary-source scope and priority audit for
[the quantitative star theorem](star-subset-accuracy-lower.md) and
[the moment-to-epigraph transfer](tree-indicator-moment-gluing.md).
It is not a new proof audit. No source examined below states the same
quantitative lower bound for the specified subsetwise moment relaxation.
That finding does not establish originality or cover all related literature.

## Closest exact formulations and algorithms

**Choi, Fattahi, Han, Gómez, and Lozano (24 August 2026).**
[*Convexification of mixed-integer quadratic optimization via decision
diagrams*, arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1),
Section 7.2, Theorem 2 and Corollary 1, establish an exact SOCP lift with
size \(O(n^{\ell+1})\) when the positive-definite Hessian support is a rooted
tree with \(\ell\) leaves. The paragraph after Remark 1 explicitly identifies
exponential size for stars. This is not a uniform polynomial-size star hull
theorem. Section 8, Definition 13, Theorem 4 and Corollary 3 provide small
approximate diagrams under volume-growth and boundary-size bounds. A star
has a radius-one neighborhood containing all vertices; the text explicitly
uses stars as an example where dimension-independent volume-growth
parameters fail. Uniform spectral conditioning alone therefore does not
invoke their approximation guarantee. These exact and approximate global
constructions do not identify the local relaxation studied here.

**Bhathena, Fattahi, Gómez, and Küçükyavuz (online 2 May 2025; issue July
2026).** [*A parametric approach for solving convex quadratic optimization
with indicators over trees*, Mathematical Programming 218,
291–336](https://link.springer.com/article/10.1007/s10107-025-02222-3),
Theorem 2, gives an exact algorithm with \(O(n^2)\) time and memory for a
positive-definite tree-supported quadratic, arbitrary continuous linear
costs, and separable indicator costs. Nonpositive indicator costs can be
fixed on, as the introduction explains. Thus optimizing on stars is already
tractable in this setting. The algorithm uses objective-dependent scalar
parametric functions; its conclusion is not one objective-independent
polynomial-size conic hull formulation. The local result must not be framed
as a computational-hardness result or a barrier to all exact algorithms.

**Wei, Atamtürk, Gómez, and Küçükyavuz (arXiv v2, 27 November 2022;
journal 2024).** [*On the convex hull of convex quadratic optimization
problems with indicators*, arXiv:2201.00387v2](https://arxiv.org/html/2201.00387v2),
Theorem 1, represents the positive-definite indicator hull using one PSD
epigraph block and the convex hull of embedded principal inverses. The
auxiliary variable count is quadratic, but the polytope description can
have exponentially many inequalities. Theorem 3 gives the corresponding
original-variable conic inequality description. The introduction and
Section 4 discussion of decomposition methods explicitly recognize that
exact convexification of component quadratics can be weak globally.
Neither that general observation nor applying the principal-inverse
formula is new here. The candidate addition is the specified arbitrary-order
subsetwise obstruction, quantitative projected gap, and simultaneous
rational-data and conditioning bounds.

**Bhathena, Fattahi, Gómez, and Küçükyavuz (2 March 2026).**
[*Solving convex quadratic optimization with indicators over structured
graphs*, arXiv:2603.02103v1](https://arxiv.org/abs/2603.02103v1),
Theorem 1 and Definition 5, give exact dynamic programming bounds depending
on treewidth, volume growth, conditioning and a margin parameter. This
extends algorithmic scope beyond trees under explicit structural promises.
It does not give the subsetwise moment hierarchy considered in the local
theorem, and the growing star degree prevents using its volume assumptions
with fixed parameters merely from the local spectral bounds.

**Lee, Gómez, and Atamtürk (22 July 2026).**
[*Convexification of multi-period quadratic programs with indicators*,
Mathematical Programming](https://link.springer.com/article/10.1007/s10107-026-02379-5),
Theorems 1–2 and Sections 3–4, provide polynomial-size exact hull
formulations for positive-definite factorizable and block-factorizable
matrices. These matrices have tridiagonal or block-tridiagonal inverses;
the block version uses one indicator for each continuous block. The result
also yields SOCP formulations and shortest-path algorithms. Its structural
assumption is on a factorization of the Hessian, not arbitrary tree support
of the Hessian. A general indicator star is consequently not covered just
because it is a tree. This newer published formulation should be included
when explaining why existing exact structured formulations do not settle
the compact-star question.

## Prior path results and an earlier star-gap example

The focused companion review of the primary PDFs found the following
additional relevant distinctions.

**Liu, Fattahi, Gómez, and Küçükyavuz (arXiv 2021; journal 2023).**
[*A graph-based decomposition method for convex quadratic optimization
with indicators*, arXiv:2110.12547v1](https://arxiv.org/abs/2110.12547v1),
Proposition 2 gives an \(O(n^2)\)-time, \(O(n)\)-memory algorithm for the
tridiagonal case. Propositions 5–6 give its exact epigraph hull and an
explicit SDP formulation. Section 3, Example 1, already uses a four-node
star to illustrate a gap produced by dropping an edge-square term. In the
[published primary PDF](https://par.nsf.gov/servlets/purl/10334386), this
is Equation (21), with the term \(0.4(x_2-x_4)^2\) removed. That
relaxation is different from shared first and second moments with locally
exact pattern decompositions. Nevertheless, no statement such as
“the first relaxation gap on a star” is justified. The new claim must name
the local relaxation and its quantitative all-orders guarantee.

**Pang and Han (arXiv 2021; SIAM Journal on Optimization 33(2), 899–920,
2023).** [*Some strongly polynomially solvable convex quadratic programs
with bounded variables*, arXiv:2112.03886](https://arxiv.org/abs/2112.03886),
Equation (2.1) concerns continuous box-constrained QP. Proposition 2.1
states a pivot bound under the positive-definite n-step-vector condition;
Theorem 6.1 and Lemma 6.2 address the positive-semidefinite comparison-matrix
class. Section 6.1 obtains \(O(n^2)\) complexity for the tridiagonal case.
This is continuous optimization, motivated by its use inside sparse
selection algorithms. It neither convexifies indicator stars nor analyzes
the local moment construction considered here.

## Necessary publication qualifications

1. Define the hierarchy explicitly. In particular, different leaf subsets
   share only the center moment matrix and singleton matrices; they need
   not agree on joint pattern matrices for larger intersections. The result
   is not a lower bound for every sparse moment, SOS, or marginal hierarchy.
2. Separate auxiliary incompatibility from the original epigraph gap.
   The square-completion and separating-cut argument is essential because
   another auxiliary representation could otherwise repair the projection.
3. Existing tree optimization algorithms and path hulls remain valid. The
   construction cannot imply hardness of star optimization or a general
   conic-extension lower bound.
4. Do not claim the elementary polygon approximation exponent is new.
   Novelty must concern its restricted indicator-quadratic realization and
   all simultaneous quantitative bounds.
5. The main source comparisons remain consistent with the accepted theorem.
   No newly identified prior result requires withdrawing it. The available
   evidence supports a qualified contribution claim, not a priority proof.

## Search and verification record

The audit read the local full texts of the two Bhathena papers and the Choi
paper, checked their primary arXiv or publisher versions, read Wei's current
arXiv HTML, and inspected the current Lee–Gómez–Atamtürk publisher text.
A separate agent inspected the primary Pang–Han and Liu et al. PDFs.
Additional searches combined indicator quadratic optimization with star
hulls, local moments, subset relaxations and joint measurability. Those
searches returned no direct equivalent theorem; their negative outcome is
not used as a novelty proof. No mathematical test, project-wide check, or
CI inspection was performed for this literature-only audit.

Bibliographic corrections: the Choi paper's author order is **Choi,
Fattahi, Han, Gómez, Lozano**. Wei's current arXiv version is **v2**, not
v3. The tree algorithm paper was first published in **2025** but appears
in the **2026** journal volume; either date needs to be identified clearly.
