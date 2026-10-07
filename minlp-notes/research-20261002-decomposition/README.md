# Decomposition-aware global optimization

This continuation develops topic 1 into an integrated technical report,
certified reference solvers, comparative experiments, and proved extensions.
The [program](PROGRAM.md) records the authorized scope. The
[second completion phase](completion/README.md) closes the implementation
gaps identified after the first report and adds further results. General
research questions remain open where the results require extra assumptions.

Start with the [integrated report](document/main.pdf), its
[source and coverage map](document/README.md), and the
[solver instructions](solver/README.md). The report develops the core proof
and explains how the extensions fit together. Companion notes contain
the detailed constructions and review records.

| Workstream | Completed result | Material boundary |
| --- | --- | --- |
| [Sparse solvers](solver/README.md) | Rational corrected grids, general tree messages, pruning, unknown-conditioning trials, automatic decomposition, and exact rational QP output | Width and coefficient size can make tables and proof replay expensive; decomposition is heuristic |
| [Comparative experiments](completion/benchmarks/README.md) | Preserved first-release ablations and new frozen-source comparisons, independent exact references, separate solve/replay costs, and full public inputs | Bounded evidence; resource failures and incompatible inputs are retained |
| [Rational optimization](completion/rational-oracles.md) | Reusable exact LP and convex box-QP routines with primal, dual, infeasibility, and unboundedness certificates | Implemented simplex and active-face enumeration are capped and do not establish polynomial runtime |
| [Integrated recourse](completion/recourse.md) | Automatic certified affine recognition, substitution and lifting, minimum-cut recourse, and changing-active-set convex factor evaluation | Requires accepted private-block or residual structure; original-model certificates verify every reduction |
| [Piecewise convex responses](completion/theory/piecewise-recourse/piecewise-curvature.md) | Reduced curvature bounds across changing active sets without a global partition overlay; scalar constructor and verifier | General theorem takes explicit covered partitions; automatic construction can be exponential |
| [Mixed submodular recourse](completion/submodular-recourse.md) | Exact convex value queries and finite Lovasz-extension cutting planes with verifiable lower bounds | Sign-compatible interactions and a PSD continuous block; implemented method is not polynomial-time general submodular minimization |
| [Coupled constraints](completion/constrained-solver.md) | Reusable TU-fiber solver, full/equality-direction curvature, exact nonunique recovery, and union filtering | Width-XP rather than width-FPT; explicit labels, initial mesh costs, and verified TU structure |
| [Optimal sets](completion/optimal-sets.md) | Actual unknown-growth discovery on the diagonal-certificate class and compact endpoint full-set descriptions | Full-set descriptions are class-specific; efficient arbitrary unknown optimal sets remain open |
| [Polynomial factors and boundary output](completion/polynomial-boundary.md) | Explicit sparse polynomial grids and automatic boundary reduction to an exact rational point or implicit strongly convex patch | Sufficient interval tests may be inconclusive; the implemented bounded restart search has no FPT runtime claim |

The [conditional-moment example](negative-curvature/convex-energy/conditional-moment-gap.md)
shows why preserving convex energy and matching local separator moments
does not by itself supply the desired negative-curvature error bound.
It has a unique optimum and a bounded negative-curvature/growth ratio.
The [hardness-reduction audit](negative-curvature/adversary/bounded-coefficient-hardness-conditioning.md)
separately shows why an existing sparse-hardness construction does not
settle the bounded-ratio question. These are specific limitations, not
hardness proofs for the general target.

The [primary-source comparison](literature/source-ledger.md) distinguishes
classical ingredients from the compositions developed here. In particular,
endpoint rounding, graph cuts, submodular minimization, affine parametric
QP, TU integrality, and diagonal Lagrangian certificates are established
tools. No publication-priority claim follows from this continuation.

Each workstream records its targeted commands, actual results, and
independent research-agent review. The [current integration review](completion/reviews/integration/REVIEW.md)
checks consistency across the notes, implementation, experiments, and
report. This is internal mathematical and software review, not journal
peer review. Finite diagnostics support the algebra and implementation;
the proofs carry the universal claims.
The [first-release review](reviews/integration-review.md) remains available
for the historical artifacts.

The first-release [benchmark findings](solver/extra-benchmarks/FINDINGS.md) cover 74 bounded
runs. All 56 rational certificates replayed successfully. Both geometric
variants met tolerance on all 13 small configurations; uniform grids did
so on 11. A 256-variable path and both full QPLIB instances reached resource
limits. The affine-recourse comparison demonstrates the benefit of the
certified reduction on its designed family. These outcomes support the
components and expose their practical limits at that release. The
[second-phase results](completion/benchmarks/RESULTS.md) measure the completed
implementations using new source snapshots; they do not retroactively alter
the earlier records.

The starting point is the October 2
[corrected-grid and min-marginal algorithm](../research-20261002/new-direction/pruned-coordinate-grid.md),
its [polynomial extension](../research-20261002/new-direction/polynomial-pruned-grid-extension.md),
and the [sparse smoothed theorem](../research-20261002/new-direction/smoothed-sparse-polynomial.md).
The September 29 [decomposition results](../research-20260929/closing-research-results.md)
provide earlier certificates, limitations, and application evidence. The
new work must use the later results when they supersede those earlier
questions.

The remaining general questions are an algorithm parameterized only by
width and negative-curvature/growth, a general local-error interface for
sparse messages, width-FPT optimization under coupled constraints, efficient
discovery and representation of arbitrary unknown optimal sets, and a
polynomial boundary-output guarantee under point growth alone. The one-draw
exact smoothed TU extension also remains open. Exact rational quadratic
recovery itself does not require uniqueness: the remaining optimal-set
question concerns useful complexity and representation guarantees. The
restricted results identify usable cases and precise obstacles; they do
not close those broader questions.

Existing dirty files and running experiments belonging to other topics are
outside this continuation. Their initial paths are recorded in
[baseline-status.txt](baseline-status.txt). Only targeted local checks are
used; no project-wide verification or CI inspection is part of this work.
