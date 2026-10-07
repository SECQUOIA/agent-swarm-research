# Primary sources for the decomposition continuation

Date: 2026-10-02. This ledger records sources checked for this continuation.
It distinguishes established ingredients from the claims being developed in
the other workstreams. It is a focused comparison, not publication-priority
clearance. Page numbers below count physical PDF pages unless a printed
page number is also given.

## Sources and the claims they support

| Source and primary text | Checked statement and location | Consequence for this continuation |
| --- | --- | --- |
| Del Pia and Khajavirad, *Treewidth and the complexity of box-constrained quadratic programs*, [arXiv:2609.35595v1](https://arxiv.org/abs/2609.35595v1), submitted September 28, 2026; [local primary PDF](../../literature/papers/pia2026-treewidth-and-the-complexity-of/original.pdf) | Theorem 1, p. 4: exact continuous box QP on a forest takes `O(n²)` arithmetic operations and comparisons, with polynomial-size intermediate representations. Theorem 3, p. 20: strong NP-hardness at interaction treewidth two, even with integral `Q,c`, `max|Qij|<=5`, and `max|ci|<=4`, for objective `x'Qx+c'x` on the unit box. Theorem 2, p. 18: quartic minimization is strongly NP-hard even when the interaction graph is a path. | Neither small width nor bounded numerical coefficients alone settles the continuation's targets. These hardness statements do not impose a bounded curvature/growth ratio. Forest conditional optimization is established prior work. |
| Same source, Theorem 4, p. 27, and Theorem 6, pp. 35–38 | Variables with nonpositive square coefficients admit an endpoint optimum. Theorem 4 combines logarithmic treewidth and attachment size for the resulting binary components, polynomial optimization of positive-diagonal components after arbitrary linear-cost changes, and constant interaction rank. Theorem 6 uses a different component organization. | Claims about a continuous core and discrete residual must acknowledge these decompositions. A graph-cut residual uses submodularity rather than a bound on residual treewidth; it is an alternative oracle class, not a new endpoint reduction. |
| Bhathena, Fattahi, Gómez, and Küçükyavuz, *Solving Convex Quadratic Optimization with Indicators Over Structured Graphs*, [arXiv:2603.02103v1](https://arxiv.org/abs/2603.02103v1); [local primary PDF](../../literature/papers/bhathena2026-solving-convex-quadratic-optimization-with/original.pdf) | A positive-definite quadratic with binary support indicators is solved by exact parametric DP. Definition 5, p. 24, imposes a `(k,eta)` margin on nearly tied support patterns. Theorem 1, p. 25, also assumes polynomial volume growth and depends on conditioning. Corollary 1, p. 27, specializes to linear volume growth. Fixed structural, margin, and conditioning parameters give linear dependence on dimension. | Exact sparse quadratic-message DP and condition-dependent pruning are established. Its support-indicator margin and graph-growth assumptions are not the global quadratic-growth premise of the corrected-grid method. It does not establish unrestricted compact message representations. |
| Bienstock and Muñoz, *LP Formulations for Polynomial Optimization Problems*, [primary preprint](https://arxiv.org/abs/1501.00288), [DOI](https://doi.org/10.1137/15M1054079); [local primary PDF](../../literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/original.pdf) | Theorem 4, p. 2 of the checked preprint: for polynomially constrained mixed binary/continuous optimization of degree `pi` and constraint-intersection width `omega`, an LP of size `O((2pi/epsilon)^(omega+1) n log(pi/epsilon))` gives scaled feasibility and objective tolerances. Theorem 7 also treats underlying network sparsity with additional degree/local-size parameters. | Sparse constrained polynomial approximation is established. The TU continuation must be compared as a restricted class that preserves feasibility exactly and gains an accuracy-bit rate from growth. It is not an improvement for the full constrained class in this source. |
| Chervet, Grappe, and Robert, *Principally Box-integer Polyhedra and Equimodular Matrices*, [primary preprint and PDF](https://arxiv.org/abs/1804.08977) | Theorem 4.4, p. 11, restates the Hoffman–Kruskal characterization: an integral matrix `A` is TU exactly when `{x:Ax<=b}` is fully box-integer for every integral `b`. Definitions of box integrality and dilates are on pp. 2–3. Theorem 4.5 concerns the broader, different property of principal box integrality. | After dyadic scaling, a feasible cell with TU constraints is a convex hull of feasible cell corners. Mean-preserving correlated rounding is a direct use of this established property. No new TU integrality theorem is claimed. Principal box integrality alone should not silently replace the precise dilation condition used in a proof. |
| Kolmogorov and Zabih, *What Energy Functions Can Be Minimized via Graph Cuts?*, [author primary PDF](https://pub.ista.ac.at/~vnk/papers/KZ-PAMI-graph_cuts.pdf), [DOI](https://doi.org/10.1109/TPAMI.2004.1262177); [local primary PDF](../../literature/papers/kolmogorov2004-what-energy-functions-can-be/original.pdf) | Theorem 4.1, p. 4 / journal p. 150: a unary-plus-pairwise binary energy is graph-representable exactly when each pair satisfies `E00+E11<=E01+E10`. Lemma 3.2 gives exact minimization by an s–t cut; the construction is on pp. 4–5. | Submodular endpoint recourse is a classical graph-cut algorithm. Fixing a core changes unary terms and restricting residual intervals rescales pairwise terms without changing their favorable signs. The continuation can contribute a certified recourse implementation and composition with core search. |
| Del Pia, *Rational Jacobi Rotations and the Complexity of Approximating Mixed Integer Quadratic Programming*, [arXiv:2607.29386v1](https://arxiv.org/abs/2607.29386v1); [local primary PDF](../../literature/papers/pia2026-rational-jacobi-rotations-and-the/original.pdf) | Theorem 1, pp. 1–2: for fixed integer dimension and fixed number of negative Hessian eigenvalues, a rational MIQP known to be bounded below admits an epsilon-approximate feasible point, or infeasibility detection, in time polynomial in the input and `1/epsilon`. The approximation is the source's range-relative notion. Rational near-diagonalization avoids assuming an exact irrational eigenbasis. | Few negative directions are already an established approximation parameter. The sparse target instead permits negative inertia to grow and seeks exact or arbitrary-precision certification controlled by width and negative-curvature/growth ratio. A real spectral decomposition alone is insufficient for a Turing-time proof. |
| Luo and Sturm, *Error Bounds for Quadratic Systems*, [publisher record](https://doi.org/10.1007/978-1-4757-3216-0_16); [local primary PDF](../../literature/papers/luo2000-error-bounds-for-quadratic-systems/original.pdf) | Theorem 3.3, pp. 11–12: for a quadratic `q` and polytope `P` with nonempty zero set `S`, `dist(x,S)<=c|q(x)|^(1/2)` on `P` for some constant `c`. Convexity and a fixed sign are not required. | Applying the theorem to `q=F-min_P F` gives quadratic growth toward the entire optimum set of a bounded continuous QP. The constant is existential. This does not provide a growth-independent efficient algorithm, an efficiently known growth constant, or a compact representation of all optimizers. |
| Bemporad, Morari, Dua, and Pistikopoulos, *The explicit linear quadratic regulator for constrained systems*, [author primary PDF](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf), [DOI](https://doi.org/10.1016/S0005-1098(01)00174-1); [local primary PDF](../../literature/papers/bemporad2002-the-explicit-linear-quadratic-regulator/original.pdf) | Theorem 2, p. 6 / printed p. 8, obtains affine primal and multiplier maps for a fixed independent active set of a strictly convex parametric QP; primal feasibility and multiplier signs determine its region. Theorem 4, p. 8 / printed p. 10, gives a continuous piecewise-affine optimizer and piecewise-quadratic value. | A supplied globally valid affine recourse map is a one-region use of established parametric QP. The continuation's additional questions are the exact PSD identity, retained factor scopes, transferred growth metric, and reduced curvature. The [2003 corrigendum](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp-corrige.pdf) corrects Example 7.1's terminal weight, not these theorem statements. |
| Li, Wu, and Quan, *Global optimality conditions for nonconvex minimization problems with quadratic constraints*, [open primary article](https://link.springer.com/article/10.1186/s13660-015-0776-3), [primary PDF](https://link.springer.com/content/pdf/10.1186/s13660-015-0776-3.pdf) | Corollary 2 in Section 3.2, equation (14), states the box-QP certificate: nonnegative complementary multipliers, `grad F(s)+diag(lambda)(2s-l-u)=0`, and `H+2diag(lambda)` PSD imply global optimality. The paper also attributes a related diagonal sufficient condition to Jeyakumar–Rubinov–Wu (2006). | The continuation's `D=2diag(lambda)` acceptance test is exactly this established Lagrangian certificate. A new algorithmic claim must concern its use after finite-budget candidate generation, treatment of unknown growth, or representation of the full optimum set. No new global-optimality condition is claimed. |
| Wainwright, Jaakkola, and Willsky, *MAP Estimation Via Agreement on Trees: Message-Passing and Linear Programming*, [author primary PDF](https://willsky.lids.mit.edu/publ_pdfs/179_pub_IEEE.pdf), [DOI](https://doi.org/10.1109/TIT.2005.856938) | Proposition 1, p. 6 / printed p. 3702, relates a tight decomposed bound to a shared optimal configuration. Section V develops message reparameterization, local optimality, and exactness on trees. The proof of Proposition 1 uses nonnegative subproblem gaps. | Local nonnegative residuals, telescoping messages, and agreement of optimal local states are established. Interpolating such a finite certificate to describe all continuous optima of a coordinatewise concave box QP is the specific proposed composition. The source does not itself state that continuous optimum-set formula. |
| Araya, Trombettoni, and Neveu, *Exploiting Monotonicity in Interval Constraint Propagation*, [primary proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/7541), [DOI](https://doi.org/10.1609/aaai.v24i1.7541); [local primary PDF](../../literature/papers/araya2010-exploiting-monotonicity-in-interval-constraint/original.pdf) | Definition 3 and Proposition 1, p. 2: monotonicity permits endpoint substitution and a sharper interval extension, exact when every variable is monotone. | Fixing a sign-certified active coordinate is standard. The continuation should claim only the growth-driven arrival at such a region, the role of the strict-complementarity margin, and the remaining-face convex certificate. |
| Burer, Natarajan, and Willemsen, *On the Semidefinite Representability of Continuous Quadratic Submodular Minimization With Applications to Pricing and Moment Problems*, [arXiv:2504.03996v3](https://arxiv.org/abs/2504.03996v3), [primary PDF](https://arxiv.org/pdf/2504.03996v3) | Theorem 1, p. 12: the proposed SDP is exact for submodular quadratics in dimension at most three. Example 4, p. 14, gives a four-variable gap; p. 3, footnote 2, leaves higher-dimensional complexity open. The introduction, pp. 2–3, separately records polynomial solvability of coordinatewise concave, submodular quadratics by binary endpoint reduction. | **Version warning:** this corrected v3 must not be cited as a general exact SDP oracle for continuous submodular box QP. The continuation's graph-cut residual retains coordinatewise concavity. Sign restrictions only on off-diagonal coefficients are insufficient for that endpoint argument. |
| Mairal and Yu, *Complexity Analysis of the Lasso Regularization Path*, [primary ICML 2012 PDF](https://icml.cc/2012/papers/202.pdf), [arXiv record](https://arxiv.org/abs/1205.0079) | Theorem 1, p. 5, gives a worst-case path with exactly `(3^p+1)/2` linear segments for `p` predictors. | Exponentially long complete parametric representations are established even in convex optimization. Any new Bellman-message obstruction must identify its additional fixed-width and conditioning properties. This source alone does not establish those properties or a hardness result for one queried optimum. |

## Additional checks for the final compositions

| Source and primary text | Checked statement and location | Consequence for this continuation |
| --- | --- | --- |
| Dechter, *Bucket elimination: A unifying framework for reasoning*, [author manuscript](https://ics.uci.edu/~csp/r48b.pdf), [publisher](https://doi.org/10.1016/S0004-3702(99)00059-4) | Theorem 11, p. 36 of the 51-page author manuscript, states exact cost-network elimination and recovery, exponential in adjusted induced width. | Finite-label tree DP, including recovery of an optimal labeling, is classical. The claimed advance must lie in the continuous correction, retained-label bound, or certificate composition. |
| Bunton and Tabuada, *Joint Continuous and Discrete Model Selection via Submodularity*, [primary JMLR PDF](https://jmlr.org/papers/volume23/21-0166/21-0166.pdf), JMLR 23(329):1–42 (2022) | Theorem 4, p. 9, applies Topkis's partial-minimization principle to submodular value functions. Corollary 6, p. 11, gives polynomially many discrete oracle calls. Section 4.2, pp. 11–12, discusses convex continuous oracles and explicitly distinguishes discretization error. | Composing continuous minimization and discrete submodular optimization is established. Its support-map model differs from the continuation's fixed concave endpoints. The broad introductory continuous-optimization language must not replace the precise oracle assumptions. |
| Gómez and Han, *Convex Submodular Minimization with Indicator Variables*, [arXiv:2209.13161v2](https://arxiv.org/abs/2209.13161v2), [primary PDF](https://arxiv.org/pdf/2209.13161v2) | Lemma 1 and Theorem 1, p. 12, give partial-minimization submodularity and indicator-box value functions. Theorem 2, p. 14, handles a lifted sign formulation. Section 5 treats efficient extreme-base evaluations. | This is direct prior for convex recourse plus submodular minimization and extreme-base computations. The continuation's rational concave/PSD-block oracle is an explicit composition with a different box interface, not a claimed new general tractable class. The duplicate arXiv:2507.00442 was withdrawn; cite the current 2209.13161v2 record. |
| Iwata, Fleischer, and Fujishige, *A Combinatorial Strongly Polynomial Algorithm for Minimizing Submodular Functions*, [author primary PDF](https://www.opt.mist.i.u-tokyo.ac.jp/~iwata/papers/sfm.pdf), [DOI](https://doi.org/10.1145/502090.502096) | Lemma 2.1, p. 5 / printed p. 765, gives the base-polytope min–max identity. The following paragraph explicitly describes a compact proof using a convex combination of extreme bases; equation (2.2), p. 6 / printed p. 766, gives greedy extreme bases. | The mixed-oracle certificate's greedy-base mixture is classical, including its role as a compact proof. The continuation adds exact convex-QP witnesses for queried chain values and checks the rational bit and residual-box contract. |
| Grötschel, Lovász, and Schrijver, *Geometric Algorithms and Combinatorial Optimization*, [author primary PDF](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf), [publisher](https://doi.org/10.1007/978-3-642-97881-4); [local PDF](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/original.pdf) | Theorem 6.4.9, printed p. 179 / PDF p. 191, equates strong separation and strong optimization for well-described rational polyhedra. Lemma 6.5.15, printed pp. 186–187 / PDF pp. 198–199, recovers a basic optimal dual solution using returned oracle inequalities with a known encoding bound. | These exact rational results justify constructing a polynomial-size greedy-base mixture through the separated LP. Weak convex optimization alone would not justify the exact certificate. |
| Kozlov, Tarasov, and Khachiyan, *The polynomial solvability of convex quadratic programming*, [primary Russian article](https://www.mathnet.ru/eng/zvmmf5189), [English DOI](https://doi.org/10.1016/0041-5553(80)90098-1); [local primary PDF](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/original.pdf) | The formulation and exact algorithm are on pp. 1–2; rational bounds and point recovery are on pp. 3–5. Positive-semidefinite matrices may be singular. Rational input follows by clearing denominators with polynomial encoding growth. | Supplies exact rational continuous convex-QP values and optimizers, including nonunique cases, for the mixed submodular oracle. It does not cover integer coordinates in the convex block. |

For the convex-energy limitation, the checked primary comparator is
Khajavirad, *Tight semidefinite programming relaxations for sparse
box-constrained quadratic programs*,
[February 12, 2026 preprint](https://optimization-online.org/wp-content/uploads/2026/02/paper.pdf).
Section 3, Theorem 3, pp. 9–10, builds SDP constraints incorporating
products from the reformulation-linearization technique. Sections 4–5
give exactness and polynomial-size conclusions under additional graph
conditions. The continuation's counterexample tests the explicitly stated
local-moment interface; it does not refute those stronger formulations.

Vavasis, *Quadratic programming is in NP*, Information Processing Letters
36(2):73–77 (1990), DOI
[10.1016/0020-0190(90)90100-C](https://doi.org/10.1016/0020-0190(90)90100-C),
is included in the companion bibliography for historical attribution.
Its bibliographic metadata was checked against the publisher's Crossref
deposit. The original full text was unavailable; no original theorem or
page locator is asserted here. Current rational-height arguments should
remain explicit rather than being replaced by that unread citation.

## Earlier audits that remain part of the source comparison

The continuation inherits its corrected-grid theorem and several source
comparisons from the earlier October 2 work. These are internal audit
records, not substitutes for primary references in a paper:

- [Corrected geometric grids](../../research-20261002/prior-art/geometric-grid-prior.md):
  interval DP for OPF, continuous DPOP, adaptive Max-Sum, and trajectory
  corridor refinement. It separates classical geometric refinement from
  the global correction and growth argument.
- [Min-marginal pruning](../../research-20261002/prior-art/minmarginal-prior.md):
  exact conditional energies, bounds tightening, adaptive state resolution,
  and the specific contraction needed for the accuracy-independent state
  count. The old audit's experiment counts are historical, not the current
  implementation's results.
- [Box-stable recourse](../../research-20261002/prior-art/smoothed-box-stable-recourse-prior.md):
  the exact rational residual-box contract, finite perturbation model,
  expected core-cell count, and exact same-draw fallback.
- [TU separable-convex recourse](../../research-20261002/prior-art/tu-equality-separable-convex-prior.md):
  established TU interpolation, exact separable-convex optimization, and
  circuit arguments. This differs from globally optimizing a coupled
  indefinite objective over TU continuous fibers.
- [Set-valued grids](../../research-20261002/prior-art/optimum-set-grid-audit.md)
  and [convex-polynomial error bounds](../../research-20261002/prior-art/convex-polynomial-error-bounds-prior.md):
  existing growth and adaptive multi-minimum results, including limits of
  coordinate grids and unknown quantitative constants.
- [Implicit convex patches](../../research-20261002/prior-art/implicit-convex-patch-prior.md):
  interval verification, alphaBB, finite KKT branching, sparse polynomial
  relaxations, and exact implicit representations.

## Second-phase compositions and implementations

The [completion phase](../completion/README.md) adds implementations and
three further arguments without changing the prior-art attribution above.
General bounded rational QP exactness is not claimed as a newly decidable
problem. The [exact-output proof](../completion/exact-output.md) establishes
that the actual filtered-grid, stationary-face, and separation procedure
terminates even with a nonunique optimal set; it does not establish an
efficient general bound. The [TU union extension](../completion/theory/nonunique-tu-exact.md)
composes feasible rounding and set growth to control states when coordinate
projections of the optimum set are finite.

The [piecewise recourse extension](../completion/theory/piecewise-recourse/piecewise-curvature.md)
uses classical parametric-QP regions and KKT maps. Its specific argument
combines locally verified curvature, downward derivative jumps, unchanged
factor scopes, and sparse filtered search without a global partition
overlay. Its separating family shows why a global affine selector is an
unnecessarily restrictive premise for that composition. Neither the local
regions nor piecewise-affine QP optimizers are claimed as new.

The implemented mixed-submodular solver uses the established Lovasz
extension and greedy bases; the rational LP uses classical simplex. Their
exact certificate interfaces are engineering contributions here. Their
finite implementations do not inherit the polynomial worst-case bounds of
the cited oracle algorithms. No additional publication-priority claim is
made for these compositions or implementations.

## Access, status, and limits

The arXiv records for the three 2026 papers above were checked online in
this continuation; the displayed versions were v1. Their mathematical
statements were checked against primary PDF text, not just the abstracts.
The TU source and graph-cut theorem were also opened from primary public
PDFs. Existing local primary PDFs supplied the other theorem checks.

An inconsistent historical placeholder remains in the Bienstock–Muñoz
package: its metadata says `read`, but a body sentence still says
`unread`. This audit used the actual PDF. No source package or central
knowledge-base file was edited to repair that unrelated metadata issue.

The Burer–Natarajan–Willemsen record was checked specifically at v3. Its
arXiv submission history dates this version August 31, 2026; the PDF title
page says revised September 2026. Both identify the same limited exactness
statement and counterexample. The existing local package currently records
that correction accurately. Historical prose elsewhere that treated this
source as unrestricted exact continuous-submodular recourse is not an
accepted premise of this continuation. Those unrelated files were not
edited.

No paywalled theorem was inferred from an abstract. The old affine-repair
audit's Robertson–Cheng–Scott comparison uses Cheng's openly available
dissertation for theorem verification, not an assumed reading of the
paywalled journal article. None of the current claims requires a new
claim about that inaccessible article.

Searches covered adaptive treewidth optimization, negative curvature,
conditional quadratic messages, graph-cut and mixed submodular residuals,
box-integral rounding, and quadratic optimum-set error bounds. No
absence-of-results claim follows from those searches. The final scoped
comparisons are in the [continuation audit](continuation-audit.md).
