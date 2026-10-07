# Literature assessment of the completed continuation

Date: 2026-10-02. This is a focused comparison of the saved mathematical
claims with primary sources. It is not a publication-priority clearance
or an independent proof review. The [source ledger](source-ledger.md)
records exact locators and access limits; the
[bibliography](checked-references.bib) supplies the checked metadata.

The continuation develops useful conditional results, algorithms, and
certificates. It does not settle the unrestricted sparse negative-curvature
problem, arbitrary unknown optimum-set discovery, or all degenerate
boundary cases. Most new material is an explicit composition of established
optimization ingredients with the preceding October 2 corrected-grid
framework. That is a useful contribution when its interface, bit complexity,
and certificate are proved; it is not evidence that the ingredients or the
underlying tractable classes were previously unknown.

## Comparison of the saved claims

| Result in this continuation | Established ingredients | Defensible scope of the added result and remaining limits |
| --- | --- | --- |
| [Affine convex recourse](../negative-curvature/affine-convex-recourse.md) and [selector recognition](../negative-curvature/adversary/affine-selector-recognition.md) | Fixed-active-set affine primal/multiplier maps and quadratic value functions are classical parametric QP; Bemporad et al. give explicit primary statements. PSD KKT identities and Schur elimination are established. | Checks a globally valid affine selector, tracks residual factor scopes, transfers growth in the induced metric, and applies the existing sparse algorithm after removing stiff convex energy. Residual width and a useful reduced-curvature bound are explicit requirements. The central-QP/LP recognition construction is presented as an algorithmic composition without a priority claim. No exact antecedent for that whole-box recognizer was established by this focused audit; it does not recognize arbitrary compact piecewise recourse. |
| [Exact sparse convex value factors](../negative-curvature/sparse-convex-value-factors.md) | An infimum of affine functions is concave; exact rational convex QP, KKT witnesses, finite-label elimination, and the preceding corrected-grid theorem are established. | Allows changing active sets without enumerating complete value functions, using private fixed-domain convex blocks attached to small retained scopes. The retained dimension can grow. Its parameter is direct retained-coordinate curvature divided by growth; conversion to negative curvature requires the stated additional bound. Parameter-dependent private domains or new fill edges are outside the argument. |
| [Submodular endpoint recourse](../conditional-messages/note.md) and [concave coordinates with a convex block](../conditional-messages/mixed-submodular-recourse.md) | Coordinatewise concavity permits endpoints. KZ gives binary pairwise graph cuts. Bunton–Tabuada and Gómez–Han establish closely related continuous-value-function/SFM compositions. Iwata–Fleischer–Fujishige explicitly give greedy-base mixtures as compact certificates. | Supplies rational residual-box oracles, exact local certificates, and composition with the earlier core-search theorem. The mixed oracle requires both favorable cross signs and a PSD continuous block; integer coordinates are covered only in the endpoint block. The exact finite-noise result is inherited from the earlier all-continuous closure theorem. The implemented mixed diagnostic is not a general SFM implementation. |
| [TU filtering and exact recovery](../constraints/tu-filtered-grid.md) | TU box integrality and correlated corner rounding are classical. Bienstock–Muñoz already give bounded-width constrained polynomial approximation. Exact DP min-marginals and rational QP height arguments are also established. | Completes deterministic feasible filtering and exact recovery for integral TU continuous fibers and explicit finite integer labels. It preserves constraints exactly and obtains an accuracy-bit rate under point growth. It is XP/fixed-width polynomial, not width-FPT: the retained-state bound contains `sqrt(n_c L/g)`, and the initial mesh may cost a capacity or denominator factor. Curvature need only be bounded on the kernel of supplied exact equality rows; this refinement does not justify ignoring unknown active inequalities. |
| [Endpoint optimum-set certificate](../degeneracy/endpoint-optimal-set.md) | Endpoint optimization, finite tree DP, and nonnegative Bellman/message reparameterizations are classical (Del Pia–Khajavirad, Dechter, Wainwright et al.). | The explicit interpolation identity converts finite DP residuals into a compact description of every optimum of a coordinatewise concave mixed-box QP. This class needs no growth constant or uniqueness. It is not a general algorithm for representing all optimal sets of an indefinite QP. |
| [Unknown-growth diagonal-certificate discovery](../degeneracy/unknown-growth-diagonal-class.md) | The acceptance test is the classical box Lagrangian sufficient condition, exactly Li–Wu–Quan Corollary 2, equation (14). Luo–Sturm supplies existential quadratic growth toward a QP optimum set. | Composes finite-budget candidate generation with an independent, exact acceptance certificate and returns the full optimal set in the promised diagonal-certificate class. No growth constant or optimizer is supplied. Runtime still depends on the actual conditioning ratio; “growth-free runtime” would be incorrect. The promise is essential, and the note does not extend this KKT argument to interior integer optima. |
| [Boundary active-face discovery](../degeneracy/boundary-active-face.md) | Interval monotonicity, endpoint fixing, active-set principles, and convex patch certification are established. | Uses the preceding global containment algorithm to discover a certified face and supplies a dovetailed search with an explicit strict-complementarity precision term `B_gamma`. That term can be exponential in input length; the result does not remove all boundary-conditioning dependence or prove termination at every weakly complementary optimum. |
| [Conditioning of the recent width-two reduction](../negative-curvature/adversary/bounded-coefficient-hardness-conditioning.md) | Del Pia–Khajavirad's strong NP-hardness construction has bounded integer coefficients and width two. | The displayed specialization proves `nu/g >= 4B`, even with a unique optimum, and survives positive square reweighting. Thus that construction does not establish hardness at bounded `nu/g`. It excludes neither a different hardness reduction nor a future positive algorithm. |
| [Conditional moment gap](../negative-curvature/convex-energy/conditional-moment-gap.md) | PSD completion and the distinction between moments and representing measures are classical; sparse SDP formulations with additional products are prior work. | The explicit four-variable family keeps width, uniqueness, and `nu/g` controlled while disproving the proposed local-moment cell-width error bound. It does not refute Khajavirad's stronger extended formulations, selective refinement, or arbitrary higher-order moment methods. Proof-review status is maintained in the theorem note. |

The preceding [unique-optimum message obstruction](../../research-20261002/new-direction/unique-message-growth-obstruction.md)
already supplies the fixed-width, well-conditioned exponential complete-message
example. It is inherited work, not a second newly discovered theorem in this
continuation. Mairal–Yu is relevant earlier evidence of complete parametric
representation growth, but does not by itself prove this project's stronger
fixed-width and growth properties. A large complete message also does not
imply that one selected conditional query is hard.

## Source versions that affect the conclusions

The corrected [Burer–Natarajan–Willemsen v3](https://arxiv.org/abs/2504.03996v3)
proves exactness of its proposed continuous-submodular SDP only through
dimension three and supplies a dimension-four gap. Its earlier
all-dimensional interpretation must not be used as a residual oracle.
The continuation's endpoint and mixed PSD-block assumptions avoid that
invalid inference. The primary note and this audit preserve the warning;
unrelated historical files were not edited.

The recent [Del Pia–Khajavirad v1](https://arxiv.org/abs/2609.35595v1)
was checked directly: forest QP has an exact strongly polynomial algorithm,
while unit-box QP is strongly NP-hard at width two with bounded coefficients.
Neither statement fixes a curvature/growth ratio. The endpoint/core
decompositions in that paper are also relevant prior, so a generic claim
that such decompositions are newly introduced would be unjustified.

For the mixed-submodular comparison, use
[Gómez–Han 2209.13161v2](https://arxiv.org/abs/2209.13161v2).
The separate 2507.00442 record is a withdrawn duplicate. The convex-QP
oracle and exact rational LP dual recovery are supported by their own
primary results, rather than by informal claims that any approximate
continuous optimizer is an exact set-function oracle.

## Verification performed for this audit

Primary PDF passages and current arXiv version records were read for the
claims in the ledger. Searches were confined to the topic and its immediate
comparators. Crossref metadata was queried for Vavasis 1990 and
Iwata–Fleischer–Fujishige 2001; original Vavasis full text remained
unavailable and is marked accordingly. The audit does not assign a checked
original theorem locator to that citation.

The final local checks are recorded in [validation.txt](validation.txt).
They check only this literature directory: relative Markdown targets,
duplicate bibliography keys and balanced braces, and whitespace. These
checks do not re-prove the mathematics or replace the workstreams' exact
diagnostics and independent reviews. No project-wide verification or CI
inspection was run.
