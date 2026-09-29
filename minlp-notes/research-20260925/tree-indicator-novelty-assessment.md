# Independent novelty and significance assessment of the star results

**Publication comparison update.** The completed
[primary-source audit](publication-star-priority-review.md) now includes
the existing `(n,k)` compatibility hierarchy, a closely related planar
inverse-square-root parent-outcome bound, global LP approximation results,
and an earlier gap for a different star relaxation. The current
[publication assessment](publication-star-assessment.md) is the consolidated
claim and evidence index. The earlier discussion below is preserved as a
record of the development; it should be read with these later comparisons.

**Completion addendum from the root.** The later
[quantitative note](star-subset-accuracy-lower.md) and its
[independent proof review](star-subset-accuracy-review.md) strengthen the
accuracy conclusion below. Using `2k` leaves against subsets of size `k`
gives real and polynomially encoded rational examples with additive and
relative gap bounded below by an absolute constant times `k^-2`.
The old `N^-3` certificate described below concerns the earlier
all-proper-subset choice. It is not the strongest completed bound.
This addition gives no constant relative gap, stronger-overlap hierarchy
bound, runtime lower bound, or new priority claim for planar geometry.

Date: 2026-09-25. This is an adversarial literature and scope review, not an
independent proof certificate. It examines the
[exploration](tree-indicator-exploration.md),
[moment examples](tree-indicator-moment-gluing.md),
[explicit arbitrary-order construction](star-hierarchy-specker-gap.md),
[uniformly conditioned construction](star-uniform-condition-subset-gaps.md),
its [short-arc review](star-short-arc-uniform-review.md) and
[rational refinement review](star-rational-uniform-review.md), and the
[face result](../notes/research-20260925-star-epigraph-faces.md).

The strongest candidate contribution is the transfer from incompatible scalar
second moments to a strict gap in the **original** positive-definite quadratic
indicator star epigraph, including rational, polynomially encoded families
with dimension-independent spectral bounds. The construction provides this
transfer at every fixed
leaf-group size. Quantum incompatibility, its failure to be determined
by small subfamilies, and generic conversion of incompatibility witnesses
into other optimization objectives are established prior results. The local
findings should not be presented as discoveries of those phenomena.

No equivalent optimization theorem was identified in the primary sources
examined below. That is limited evidence, not an originality proof. The
projection argument and uniform-conditioning refinement appear to be useful
mathematical additions. The refinement removes the initial family's
near-singularity limitation. The results still do not resolve the
compact-formulation question or establish comparable consequences for
optimization complexity.

## Exact claim being assessed

For each fixed positive integer \(k\), the short-arc note constructs a
star with \(k+1\) leaves satisfying
\(I/24\prec Q\prec3I\), and a point below its true closed convex hull.
The point passes the following relaxation: each group of at most
\(k\) leaves has a joint decomposition into positive-semidefinite \(2\times2\)
matrices, and different groups share the total center matrix \(M\) and the
single-leaf matrices \(M_i\). Its leaf cost comes from exact conditional
quadratic minimization. The note supplies star coefficients, original means,
and a strictly positive lower bound on the projected gap. Every proper
subfamily has an actual finite scalar-law realization. The construction
therefore survives replacing closure-only local moment feasibility by actual
local measure feasibility. The original mean vectors have uniformly bounded
Euclidean norm, and leaf activity means remain in a fixed compact subinterval of
\((0,1)\), as proved in the independent short-arc review.

The rational refinement supplies the same conclusion with rational
\(Q,x,z\), a rational feasible relaxation point, and a rational separating
inequality. It gives

\[
 \tfrac1{39}I\prec Q\prec12I,\qquad \kappa_2(Q)<468,
\]

and total encoding length \(O(N^2\log N)\) for \(N\) leaves and the displayed
data and witness. A polynomial-time exact rational construction is proved.
The actual local scalar atom locations need not be rational. The
[rational proof review](star-rational-uniform-review.md) separately verifies
these claims and an explicit gap certificate of at least
\(1/[58320(N-1)^3]\).

This is stronger than finding an incompatible auxiliary tuple. A tuple can
be excluded from a lift while its projection remains representable by other
tuples. The explicit objective identity in the note excludes that escape:
the joint-compatibility witness is a lower bound on every true representation
with the specified original means, while the local tuple violates the bound.

The [general transfer theorem](tree-indicator-moment-gluing.md#transferring-any-local-moment-incompatibility-to-a-star-epigraph)
now has a written proof and a separate
[independent proof review](tree-indicator-projection-transfer-review.md).
For fixed center mean and interior leaf masses, every tuple passing the
specified local tests but outside the full joint cone can, after appropriate
indicator complementations and perturbation, be detected by some
positive-definite star objective and suitable original leaf means. This
review has read that final statement and its proof, but supplies a literature
assessment rather than another proof audit. The explicit short-arc family
adds spectral bounds that the general transfer does not supply.

The quantifiers matter. The construction allows the quadratic and original
means to depend on \(k\). It does not prove failure for every star, for a
single fixed quadratic at all orders, or for all hierarchies called moment
relaxations. At the full leaf set the defined compatibility system is exact
for the closed joint moment cone.

In particular, for \(k\ge3\), the construction does not assert that chosen
group decompositions induce the same joint matrices on every group
intersection. Individual compatibility of overlapping groups does not supply
such an assertion. A relaxation adding these identifications, or adding
higher powers of the center variable, requires a separate lower bound.

## Closest optimization results

The following sources were examined in local full text. Open primary links
are provided for reproduction.

| Source and inspected part | Established result and distinction |
| --- | --- |
| Choi, Fattahi, Han, Gómez, and Lozano, [*Convexification of Mixed-Integer Quadratic Optimization via Decision Diagrams*, arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1), Section 7.2, Theorem 2, Corollary 1, and the paragraph after Remark 1 | Their exact SOCP formulation has size \(O(n^{\ell+1})\) for a rooted tree with \(\ell\) leaves. They explicitly state exponential size for stars and distinguish polynomial-time optimization on trees. This supplies exact global formulations outside the local construction being refuted; it does not establish a uniformly polynomial star formulation. The abstract alone is insufficient to determine the leaf dependence. |
| Bhathena, Fattahi, Gómez, and Küçükyavuz, [*A parametric approach for solving convex quadratic optimization with indicators over trees*](https://doi.org/10.1007/s10107-025-02222-3), scalar parametric construction and complexity result | Exact tree optimization is already polynomial, with quadratic running time. The star face proof uses a simpler special case of the same scalar piecewise-quadratic mechanism. Neither the face note nor the gap theorem improves this algorithm. An objective-dependent minimization representation is different from one conic lift for all objectives. |
| Liu, Fattahi, Gómez, and Küçükyavuz, [*A Graph-based Decomposition Method for Convex Quadratic Optimization with Indicators*](https://arxiv.org/abs/2110.12547), introduction and path formulation discussion | Exact compact path formulations are established. Consequently the two-leaf star example, which is a path, can only show failure of the particular local relaxation. It cannot establish a lower bound on unrestricted formulations. |
| Wei, Atamtürk, Gómez, and Küçükyavuz, [*On the convex hull of convex quadratic optimization problems with indicators*](https://arxiv.org/abs/2201.00387), introduction and principal-inverse representation | The hull can be represented using the convex hull of embedded principal inverses and a PSD epigraph condition. The paper already warns that convexifying low-dimensional terms can remain weak globally. The local notes' inverse-mixture calculations are applications of this theory. Their explicit star gaps and all-orders quantifier are the candidate additions. |
| Han, Gómez, and Atamtürk, [*2x2 convexifications for convex quadratic optimization with indicator variables*](https://arxiv.org/abs/2004.07448), Sections 1, 2, 4, 5 and conclusion | Bivariate hulls and the named `OptPairs` relaxation are established, as are comparisons with optimal perspective, Shor SDP, and rank-one relaxations. The proposed leaf-group hierarchy is not automatically identical to `OptPairs`. The paper's variable-sign assumptions and retained lifted entries must be matched before claiming dominance or a gap for that named relaxation. |
| Liu, Atamtürk, Gómez, and Küçükyavuz, [*Polyhedral analysis of quadratic optimization problems with Stieltjes matrices and indicators*](https://doi.org/10.1007/s10107-025-02272-7), Sections 2–4 and exactness discussion | The paper distinguishes the full inverse polytope from its upper monotone relaxation. Its exactness result has sign qualifications on the linear continuous objective. Turning a star into a Stieltjes matrix does not remove those qualifications or identify its relaxation with the current hierarchy. The signs of prescribed means are not a substitute for checking the signs of the exposing objective. |
| Bhathena, Fattahi, Gómez, and Küçükyavuz, [*Solving Convex Quadratic Optimization with Indicators Over Structured Graphs*, arXiv:2603.02103](https://arxiv.org/abs/2603.02103), introduction, model assumptions, and local paper record | More recent exact dynamic programming exploits treewidth, volume growth, and a margin condition. Those conditional algorithmic guarantees do not establish the missing uniform compact hull representation, and the star gaps do not challenge them. |

The uniform-conditioning refinement also warrants checking Section 8 of the
Choi et al. decision-diagram paper. Definition 13, Theorem 4, Corollary 3,
and Proposition 9 combine spectral control with volume-growth and boundary
conditions for approximate diagrams. Stars violate a dimension-independent
volume bound already at radius one, as the paper explicitly notes. Uniform
conditioning alone therefore does not activate those approximation results.

The closest named families are therefore perspective/decomposition
relaxations, optimal pair convexification, sparse moment relaxations, and
matrix-valued local marginal relaxations. A paper should define the proposed
hierarchy explicitly before using those names. It should not infer a
comparison solely because all formulations use small PSD matrices.

Lasserre's [*Convergent SDP-Relaxations in Polynomial Optimization with
Sparsity*](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf)
was also examined. Its convergence theorem concerns a compact semialgebraic
set, suitable positivity assumptions, increasing relaxation order, and a
running-intersection sparsity condition. The proof uses compatible marginal
measures. Matching finitely many moments is a weaker condition. The present
star result is consistent with that distinction and does not disprove sparse
hierarchy convergence. The unbounded center and the fixed degree-two
truncation must remain visible in comparisons.

## Closest quantum results

Bluhm and Nechita, [*Joint measurability of quantum effects and the matrix
diamond*](https://arxiv.org/html/1807.01508), Sections 3 and 5, provide the
existing compatibility framework: binary PSD effects admit one positive
parent decomposition with the desired marginals. Congruence normalization
of \((M,M_i)\) yields precisely that framework over real \(2\times2\)
matrices. Describing this as scalar second-moment compatibility is useful for
optimization readers, but the underlying cone is not new.

Andrejic and Kunjwal, [*Joint measurability structures realizable with qubit
measurements: incompatibility via marginal surgery*](https://arxiv.org/html/2003.00785),
Section III.2 and Corollary 8, establish an \(N\)-Specker family for every
\(N\ge3\): every proper subfamily is compatible, while the full family is
not. Their planar construction can be rotated into the real Pauli plane.
The construction and compatibility interval used in the explicit star note
are prior results. The new claim must concern the positive-definite
quadratic and its original epigraph, not arbitrary-order incompatibility
alone. The case of two effects is elementary.

Carmeli, Heinosaari, and Toigo, [*Quantum Incompatibility
Witnesses*](https://arxiv.org/html/1812.02985v2), Theorems 1–2, are especially
important for the general transfer. Every incompatibility witness
has a finer witness implemented by state discrimination; a tight witness
has a detection-equivalent implementation. Their proof adjusts coefficients
by identity shifts and positive rescaling. The text treats pairs explicitly
and states that finite collections are handled similarly. Thus separating
incompatibility and translating the separator into a useful objective is
already a general method. A star realization would add a particular,
restricted classical quadratic optimization representation, not the general
idea of witness conversion.

Skrzypczyk, Šupić, and Cavalcanti, [*All sets of incompatible measurements
give an advantage in quantum state
discrimination*](https://arxiv.org/html/1901.00816), Equation (5) and the dual
formulation in the appendix, prove a quantitative statement for arbitrary
finite measurement collections: one plus generalized incompatibility
robustness equals the largest relative discrimination advantage. Thus even
a quantitative operational interpretation of the separating witness is
prior work. A quantitative star theorem would need to establish the
additional restrictions imposed by its quadratic objective.

Grinko and Uola, [*On compatibility of binary qubit
measurements*](https://arxiv.org/html/2407.07711), Theorems 1–2 and Section VI,
give a complete criterion for finite unbiased families, a necessary condition
for biased families, and an SOCP implementation with \(2^{N-1}\) terms. They
also refute a conjectured planar criterion in the Andrejic–Kunjwal paper.
That conjecture concerns a particular polygonal walk and is distinct from
the proved regular \(N\)-Specker family. The local proof should rely on the
proved family or its own justified convex-hull perimeter argument, not on
the refuted conjecture.

Porto, Designolle, Pokutta, and Quintino, [*Measurement incompatibility and
quantum steering via linear programming*](https://arxiv.org/html/2506.03045v3),
Sections 3.4–3.5 and the planar application in Section 4, give convergent LP
approximations by discretizing the quantum state space. For fixed dimension
and outcomes, their complexity is polynomial in the number of measurements
and inverse requested error. Their planar application uses a circle
approximation. This is important prior for any proposed computational use of
the connection: practical compatibility approximations already exist and
could be translated, but their robustness error is not automatically a bound
on a star epigraph objective.

An independent literature subreview checked the quantum statements above,
especially the witness-conversion theorem and the distinction between
general compatibility constructions and restricted star costs. This is a
second literature assessment, not an independent proof of the optimization
transfer.

## What adds insight, and what remains routine

The useful step is that the star cost has enough freedom to expose the
compatibility defect despite projection. Its negative coefficients of
\(r_i=\mathbb E[X^2Z_i]\), positive center variance coefficient, and
quadratic perspective dependence on \(s_i=\mathbb E[XZ_i]\) are restrictive.
They prevent a bare invocation of separation from proving the epigraph gap.
Choosing the couplings and leaf means to match a homogeneous witness, and
retaining a strictly positive Schur complement, directly addresses that
restriction. The explicit construction also supplies a quantitative strict
gap instead of relying only on an existential separator.

The ingredients themselves are standard: positive-cone separation,
complementing a binary outcome, scalar square completion, perspective
tangency, and a small coercive perturbation. A careful reviewer could view
the general transfer theorem as a short representation lemma combining
these ingredients. Its strength would come from a clear statement that is
reusable outside the displayed regular family, rather than from technical
length. The written transfer lemma improves the case for a reusable
contribution, but does not alone justify a broad solver-complexity claim. The short-arc
refinement does additional work: choosing polygon tangent differences whose
total coupling weight stays fixed keeps the Schur complement uniformly
positive. Arbitrary strict incompatibility alone does not guarantee that
the resulting star has such spectral bounds.

The rational refinement is a meaningful qualification of that result: the
obstruction exists in the usual finite rational input model, can be generated
with polynomially many bits, and has an inverse-polynomial displayed margin.
It is stronger than simply approximating an irrational example without
controlling the approximation precision. Rational circle parameters, exact
chord identities, and dyadic choices of the couplings implement this step.
These arithmetic devices are not themselves a separate conceptual advance.
Nor does polynomial encoding imply a computational hardness result.

The face result has a lower novelty ceiling. Its threshold counting is an
elementary specialization of existing tree parametric theory. The explicit
union-of-cubes description and extension to all bounded faces clarify why
an auxiliary correlation-polytope face cannot be transferred directly. That
is a useful obstruction to an incorrect lower-bound strategy. It should
remain a supporting structural result unless a new consequential application
is found.

## Significance and practical implications

The all-orders projected gap gives a principled warning for formulation
design. Increasing the number of leaves considered by an independent local
compatibility check to any fixed constant cannot make this construction
uniformly exact, even when the support graph is a star and the quadratic's
eigenvalues lie in a fixed positive interval. Thus a level guaranteeing
exactness cannot depend only on treewidth, diameter, and a bound on this
spectral condition number for the specified scheme. The center degree grows
with the example size, so a level depending on maximum degree is outside
this conclusion. Acyclic sparsity and bounded curvature do not eliminate
the need to represent the center law consistently across leaves.

This could guide stronger relaxations, adaptive choice of leaf groups, or
compatibility cuts. These are plausible applications, not proved performance
benefits. No solver implementation, runtime improvement, practical gap
distribution, or numerical stability result follows from the current
construction.

The original regular-family note becomes poorly conditioned as its size
increases. That limitation is superseded by the short-arc construction and
must not be stated as a limitation of the strengthened result. The new
displayed gap certificate is \(\Theta(N^{-3})\) for the equally spaced
short-arc family. This is the asymptotic size of a proved **lower bound**;
it does not prove that the actual projected gap is at most that order or
tends to zero. No dimension-independent relative gap is established.
Consequently the theorem does not show that modest leaf-group sizes are
poor approximations in applications.

An elementary comparison further limits the approximation interpretation.
If \(\lambda I\preceq Q\preceq\Lambda I\), and \(h_Q(x,z)\) denotes the true
closed-hull height, then

\[
 \lambda\sum_i x_i^2/z_i\ \le h_Q(x,z)\le
 \Lambda\sum_i x_i^2/z_i.
\]

Use the closed-perspective convention and set the fixed center indicator to
one. The lower bound follows from the spectral bound and conditional
Cauchy–Schwarz. For the upper bound, choose independent binary indicators
and set each active coordinate to its prescribed mean divided by its activity
probability. Applying the upper spectral bound gives the displayed value.
Thus bounded conditioning already gives a constant-factor perspective
comparison for pure epigraph heights. It gives no such ratio guarantee after
adding an arbitrary affine objective.

The following stronger questions remain consequential:

1. Can compatible overlap marginals or higher center moments yield a compact
   exact star formulation? The current construction does not decide this.
2. Can bounded-order compatibility give dimension-independent approximation
   guarantees under conditioning assumptions? Quantum noise bounds alone are
   insufficient until translated into objective and original-variable error.
3. Can one prove an unconditional size lower bound for the original curved
   hull, or construct a uniform polynomial conic lift? Small bounded faces
   and local hierarchy gaps settle neither alternative.

No claim of polynomial optimization of fixed-dimensional compatibility
should be based only on the standard exponential parent representation.
Its dual tests positivity over a zonotope in the fixed-dimensional vector
space of symmetric matrices. Polynomial vertex enumeration of such
zonotopes already supplies a generic route to a separation oracle. The
primary fixed-dimension background includes Ferrez, Fukuda, and Liebling,
[*Solving the fixed rank convex quadratic maximization in binary variables
by a parallel zonotope construction
algorithm*](https://doi.org/10.1016/j.ejor.2003.04.011). Applying this observation
to compatibility is an inference in this review, not a theorem attributed
to that paper. An improved special-purpose oracle would still need a precise
bit-complexity and novelty comparison.

## Search and verification record

The review inspected the local full texts identified above and the linked
primary quantum papers. Search phrases included combinations of quadratic
indicators, star/tree convex hulls, moment and hierarchy relaxations, sparse
moment marginal gluing, joint measurability, operational witnesses, planar
qubit compatibility, and zonotopes. Searches also checked the newer
decision-diagram result and the more recent unbiased-qubit characterization
instead of treating older apparent open questions as unresolved.

No source was found in this search stating the same explicit
positive-definite-star projected hierarchy gap. This does not exclude an
equivalent result under disjunctive optimization, truncated vector moments,
or conic marginal hierarchies. The `OptPairs` relation and any stronger
overlap hierarchy remain unclassified here.

This review ran targeted file reads, text searches, and an inline Python
check that this review file contains no unexpected control characters. It
did not run mathematical verification scripts, project-wide checks, or CI
inspection.
It relies on the separate exact examples, explicit proof notes, and
independent proof reviews for correctness. A delegated significance reviewer
also ran `python research-20260925/verify_star_rational_uniform.py`: all eight
instances and 1,020 exact sign-pattern PSD checks passed. This review read
that script and its result rather than rerunning it. The general transfer,
short-arc construction, and rational refinement have written independent
reviews; this assessment does not
substitute for them or strengthen their formal verification status.
