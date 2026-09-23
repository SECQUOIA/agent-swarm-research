# Stage 1, round 1 — review01

Reviewed manuscript: `sections/01-foundations.tex` (672 lines at review time).
Focus: physical model equivalence, flow and quality bounds, zero throughput, and empty sets.

## Major finding M1: endpoint formulation omits an essential restriction on product specifications

**Location:** lines 641–672, especially the special-case definition at 641–642 and the equivalence at 647–658.

The section permits lower and upper quality bounds, and the facial subsection explicitly permits arbitrary rational polyhedral product regions. The purported special case restricts input qualities to `[0,1]` and product *upper* bounds to `{0,1}`, but does not remove lower quality bounds or other product inequalities. Under those stated conditions, the support disjunctions do not characterize quality feasibility, and the resulting MILP need not be exact.

**Counterexample:** take two inputs with scalar qualities 0 and 1, one pool, one product, and only the two feed arcs and the pool outlet. Set all flow upper bounds to 1 and lower flow bounds to 0. Give the product lower and upper quality bounds both equal to 1. This satisfies the stated endpoint hypotheses; its product region also cuts out the face `{1}` of the input hull `[0,1]`. A unit flow from the quality-zero input through the pool has `D=0` and `S=0` and passes every displayed support/MILP condition, but violates the product lower quality bound. Charging -1 on that feed and 0 elsewhere makes the proposed MILP optimum -1, whereas the physical optimum is 0.

**Correction:** explicitly restrict this specialization to product specifications consisting only of coordinate upper bounds in `{0,1}` (any coordinate lower bound must be redundant, for example 0). State that no additional polyhedral quality inequalities are present. The present proof, branch count, MILP, and certificate statements then work. An extension handling nonredundant endpoint lower bounds would need additional exclusions/disjunctions and is unnecessary for this repair.

This is a missing essential hypothesis, rather than an optional explanatory improvement. The source `results/pooling-facial-quality-integrality.md` has similarly compressed wording in its endpoint subsection, so copying that wording is not sufficient to discharge the issue.

## Minor finding m1: state the finite-flow assumption where bounded optimization is used

**Locations:** lines 49–50, 125–127, 187–190; the bounded-branch argument in the facial theorem and the final cyclic attainment argument use the same convention.

The global wording says arcs and node totals “may have finite rational lower and upper bounds.” This can mean that a variable may have no upper bound. The text then uses attained finite optima, bounded lifts, and flow polytopes without always repeating the finite-flow assumption. In particular, bounding pool qualities alone does not make the lift bounded. A single bypass with no flow upper bound and cost -1 illustrates the distinction: the quality box is bounded but the flow problem is unbounded, and the displayed minimum is not attained.

The surrounding discussion and the source models clearly intend finite capacities for the capacitated problems, so I treat this as a local scope ambiguity rather than a separate substantive theorem failure.

**Correction:** set a global convention that all capacitated instances have finite rational effective upper bounds on every arc flow, unless explicitly removed to define `S` and the cones. Alternatively repeat that hypothesis at each bounded optimization theorem. Move “with finite flow bounds” into the premise of the bounded-lift sentence. The existing source files explicitly use finite bounds.

## Verification performed

- Read the entire assigned stage and checked its mathematical arguments, without inspecting other reports in this review round.
- Reconstructed standard-pool averaging, homogeneous zero-flow semantics, and affine-rank substitution. Inactive pools, empty input sets in DAGs, rank-zero qualities, and rank-one zero matrices are handled correctly under the declared model.
- Checked destination disaggregation using head multipliers, exact single-product LP projection, cost-sign and product-count bounds, sparse shortest-path witnesses, polynomial rational reconstruction, and the uncapacitated conic-hull identity. Empty product sets and zero-capacity deletion are treated consistently under zero lower flow bounds.
- Checked cyclic reconstruction via the backward substochastic matrix; isolated positive circulations cannot have positive external flow by conservation. Checked the absorption decomposition and the merge of isolated circulation components used for the product-count bounds. The examples concerning singularity and residuals are algebraically correct.
- Checked both directions of the facial characterization, including empty product faces and zero-throughput pools; checked the rational nonfacial witness, network integrality argument, recognition LP, and fixed-dimensional face enumeration. The lower-bound check on excluded arcs is explicitly present in the algorithm.
- Cross-checked the canonical facial and profitable-flow results and the recirculation investigation for the assumptions relevant to these arguments. Historical PASS labels were not used as proof evidence.

## Verdict and limits

**Verdict: major findings present (M1), plus one minor clarification (m1).** Apart from these points, I found no additional mathematical defect in this stage. This review does not establish literature priority, verify all bibliographic metadata against published originals, cover later manuscript stages, or guarantee exhaustive correctness or external acceptance.
