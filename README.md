# Research output of AI agent swarms

This repository holds the research corpus described in the paper
[AI Agent Swarms as Researchers: Progress, Challenges, and Open
Questions](https://arxiv.org/abs/2609.35719) by Sergey Gusev and David E.
Bernal Neira. To cite this work, see [Citation](#citation). The paper's
research inventory (Appendix C) lists the potential papers and proposed
experimental programs in the corpus, with IDs such as M1 or Q12. The
[inventory below](#research-inventory) is the current version of that list and
links to the drafts.

## What this is

At tag `paper-v1` (commit `84c6be7`), the version the paper describes, the
folders contain only material written by AI agents during the runs described in
the paper: notes, checks, code, review records, Lean proofs, and paper drafts.
This snapshot holds the agents' output as of 25 September 2026. The authors
of the paper have not edited it and, except where the paper says otherwise,
have not verified its claims. It contains no scientific input from the authors;
their part in producing it was limited to the process and editorial
instructions described in the paper. The drafts are not final papers: the
authors intend to take them further.

The runs continue, and later versions of this repository may add topics and
results, some with the authors' scientific input.

## Folders

| Folder | Field |
|---|---|
| `minlp-notes` | Mixed-integer nonlinear programming |
| `qipm-notes` | Quantum interior-point methods |
| `thermo-notes` | Molecular thermodynamics |
| `transport-notes` | Transport theory |
| `aggregation-kinetics-notes` | Aggregation kinetics |
| `catalysis-notes` | Heterogeneous catalysis (proposed experimental programs) |

## Research inventory

The tables list research topics and manuscript candidates, together with eight
proposed experimental programs. **Main contribution** describes the contribution
claimed in the files, including material limits and negative findings. It does
not establish novelty or publication priority. Several topics share a manuscript;
topic rows are not a count of distinct papers.

This inventory reflects the committed MINLP source snapshot
[`5eb57659d`](https://github.com/sergey-gusev94/minlp-notes/tree/5eb57659d910b196d5e0774729cc4d1fa15d0fa9)
of 6 October 2026 and the existing snapshots of the other fields. The MINLP
transfer retains original results, proofs, code and reviews, with external
literature copies omitted and private metadata redacted. See the
[third-party notices](THIRD_PARTY_NOTICES.md) for retained third-party licenses.

The paper's Appendix C describes tag `paper-v1`. M23–M51 were added after
that snapshot, and several earlier topics now have manuscripts or revised
titles. Existing IDs are retained. For the original inventory, see
[this README at `paper-v1`](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/README.md#research-inventory).

The power-flow and MINLPLib PDFs were rebuilt from the retained sources on
6 October 2026.
“Full paper” describes a manuscript artifact, not submission, acceptance or
publication. Reviews in the corpus are reviews by other research agents;
they are not journal peer review. Authors' checking and submission declarations
remain incomplete where the local release records say so.

### Mixed-integer nonlinear programming

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| M1 | Sharp gaps for positive multilinear relaxations | Exact gap constructions and sharp leading growth with degree and dimension for positive multilinear terms; termwise envelopes can have unbounded joint gaps. | [Full paper](minlp-notes/paper-multilinear-gap/main.pdf) | Done |
| M2 | Verified bounds for positive cubic relaxation gaps | A universal 31/12 upper bound, optimality within a specified fixed-law mixture, and exact lower witnesses; the exact cubic supremum remains open. | [Full paper](minlp-notes/paper-cubic-gap/main.pdf) | Done |
| M3 | Checkable lower bounds for convex mixed-integer nonlinear optimization through rational outer approximations | Rational outer-approximation cuts and independently replayable lower-bound certificates, with complete and partial verdicts kept distinct. | [Full paper](minlp-notes/paper-certified-minlp/main.pdf) | Done |
| M4 | Convex relaxation gaps and spatial certificates in nonlinear optimization | An integrated account of envelope gaps, sparsity and physical-box laws, conic lift limits, and spatial certification under specified relaxation oracles. | [Full paper](minlp-notes/paper-relaxation-limits/main.pdf) | Partial |
| M5 | Integer dimension in convex mixed-integer approximation of nonlinear graphs | Sharp precision laws for integer dimension, rank-based lower bounds, and compact rational formulations nearly matching arbitrary convex lifts. | [Full paper](minlp-notes/paper-integer-dimension/build/main.pdf) | Partial |
| M6 | Rounding switching controls under a hard switch budget: sharp minimax bounds and exact algorithms | Sharp small-budget minimax values, exact finite-grid algorithms, switch-preserving grid transfer, and certified coarsening; the general exact formula remains open. | [Full paper](minlp-notes/paper-switching-control/main.pdf) | Partial |
| M7 | Sparse convex hulls for network flows coupled to a simplex | Exact sparse hulls, observation-sensitive compression, structural separators, and coefficient-size boundaries for network–simplex products. | [Full paper](minlp-notes/paper-network-simplex/main.pdf) | Partial |
| M8 | Topology, uncertainty, and precision in passive potential-flow optimization | Structural exact and additive algorithms under nomination/resistance uncertainty, arithmetic and discrete-uncertainty barriers, and checkable original-network error certificates. | [Full paper](minlp-notes/paper-potential-flow/complexity/main.pdf) | Partial |
| M9 | The complexity of pooling: algebraic barriers and structural algorithms | Existential-real completeness and restricted hardness, alongside exact algorithms for small nonlinear cores, structured bypasses, and contracted flows. | [Full paper](minlp-notes/papers/pooling/main.pdf) | Not applicable |
| M10 | Exact feasibility of resistive and AC power networks | Existential-real completeness under strong graph/data restrictions, solution-preserving universality, and quantitative residual and reactive-stability boundaries. | [Full paper](minlp-notes/paper-power-flow/build/main.pdf); [sources and build instructions](minlp-notes/paper-power-flow/README.md) | Not applicable |
| M11 | Structured bilevel optimization with many follower variables: global responses, accuracy, and structural boundaries | Exact compressed global follower responses, near-optimal-response robustness, certified screening, and accuracy-bit algorithms under fixed structural dimensions. | [Full paper](minlp-notes/paper-structured-bilevel/paper.pdf) | Possible |
| M12 | Globally certified measurement selection with correlated errors | Relative locality and spectral approximation guarantees, exact rational design certificates, and latent-anchor relaxations for correlated measurement errors. | [Full paper](minlp-notes/paper-correlated-measurements/build/main.pdf) | Partial |
| M13 | Radial and point separation for perspective outer approximation of convex generalized disjunctive programs | A computational comparison of radial and point separation for established perspective outer approximation, with corrected implementation and qualified performance claims. | [Full paper](minlp-notes/paper-lbesh/main.pdf) | Not applicable |
| M14 | Quadratic aggregation: certificates, finite descriptions, and approximation | Trivial-hull aggregation certificates, sharp finite-description results and infinite-ray obstructions, with SDP lifts and quantitative finite-aggregation accuracy bounds. | [Full paper](minlp-notes/paper-quadratic-aggregation/paper.pdf) | Partial |
| M15 | Exact convex hulls for a reciprocal factor shared by many variables | Explicit many-leaf reciprocal-anchor hulls, exact rational separation and constructive decompositions, including an integer-anchor extension. | [Notes only](minlp-notes/results/common-factor-reciprocal-anchor-full-hull.md) | Done |
| M16 | Ill-posed heat-exchanger network instances in MINLPLib | Identifies an unbounded guarded LMTD expression in heatexch_gen1/2/3; numerical ill-posedness evidence is confined to heatexch_gen1. | [Notes only](minlp-notes/notes/research-20260912b-closeout.md) | Not applicable |
| M17 | Convex envelopes of two-variable monomials with real exponents on a wedge | Envelope formulas extending positive-exponent results to negative and mixed-sign exponents, with separate zero-exponent and degree-zero boundary cases. | [Notes only](minlp-notes/results/monomial-wedge-envelopes-real-exponents.md) | Possible |
| M18 | Sparse indicator quadratics: exact complexity and smoothed separator messages | Near-identity bandwidth-two hardness, exponential exact-message descriptions, and complete smoothed message dictionaries under spectral and treewidth bounds. | [Full paper](minlp-notes/paper-sparse-indicator-quadratics/paper.pdf) | Not applicable |
| M19 | Convex envelopes of univariate functions of a linear form | A convex-order envelope characterization and valid cuts for general lower-semicontinuous ridge functions, with restricted simplex/order extensions; timing evidence needs repair before publication. | [Notes only](minlp-notes/research-20260922/ridge-envelopes/theory.md) | Possible |
| M20 | Local rates, stalling, and finite certificates for iterated optimization-based bound tightening | Local contraction and stall theory plus finite certificates of remaining tightening benefit; the tested adaptive policy reduced auxiliary LPs without a net solve-time benefit. | [Full paper](minlp-notes/paper-adaptive-obbt/main.pdf) | Possible |
| M21 | Joint relaxation of several nonlinear terms in one variable | Certified curve-hull cuts linking all univariate terms of one variable; substantial gains on selected water models, mixed or unfavorable broader solver results. | [Notes only](minlp-notes/research-20260922/curve-hulls/report.md); related manuscript M40 | Not applicable |
| M22 | Separable concave terms on few linear rows | Identifies concave-term row hulls with classical constant-capacity flow covers, extends their scope, and supplies interval DP and root-cut experiments; easy and unequal-width cases show smaller or adverse gains. | [Notes only](minlp-notes/results/row-hull-separable-concave.md) | Possible |
| M23 | Encoding and calibration of exact norm penalties in mixed-integer convex optimization | Doubly exponential penalty encoding examples, fixed-quadratic-count upper bounds, and polynomial-factor calibration inapproximability; no generic solver speedup is claimed. | [Full paper](minlp-notes/paper-exact-penalties/main.pdf) | Partial |
| M24 | Exact optimization of convex quadratic and second-order cone programs with a small Hessian span | Small Hessian-span algebraic precision and exact optimization, including unbounded mixed-integer models; stronger common-range restrictions yield fixed-parameter bounds. | [Notes only](minlp-notes/research-20260927/hessian-span-main-results.md) | Not applicable |
| M25 | Exact arithmetic in polynomial optimization: values, optimizers, and certificates | Separates value, point, comparison and representation complexity: convex-quartic PosSLP classifications, constructive point oracles, structured constrained algorithms, and output-size barriers. | [Full paper](minlp-notes/paper-exact-arithmetic/main.pdf); incorporates M26 | Partial |
| M26 | Irrational minimizers and certificate coefficient fields for strongly convex quartics | Explicit irrational zero minimizers and exponentially large optimizer/SOS fields despite short rational convexity certificates, with compact shared-root representations. | [Full paper, within M25](minlp-notes/paper-exact-arithmetic/main.pdf); [topic synthesis](minlp-notes/research-20260927/exact-convex-quartic-complexity.md) | Partial |
| M27 | Quantitative sparse sum-of-squares hierarchies and large private convex recourse | Bag-uniform ordinary-module convergence, sharp sparse rate examples, inverse-square versus inverse-order private-recourse rates, and exact rational certificate extensions; earlier public inverse-square rates are credited. | [Full paper](minlp-notes/paper-sparse-sos/delivery/sparse-sos.pdf) | Possible |
| M28 | Phase transitions of perspective branch-and-bound in random sparse regression | Sharp root-exactness and linear-tree thresholds, unchanged by specified stronger lifts, plus conflict-clique lower bounds; a published exactness statement is corrected. | [Full paper, within M29](minlp-notes/paper-bb-complexity/main.pdf) | Not applicable |
| M29 | Instance-dependent certification complexity in branch-and-bound | Relates fixed-relaxation certificate size to near-optimal geometry and multiscale covers, with propagation, decomposition, face-integral and random-model extensions; certificate size is distinct from runtime. | [Full paper](minlp-notes/paper-bb-complexity/main.pdf) | Possible |
| M30 | Relaxation-intrinsic lower bounds for integer branch-and-bound: class number, random closest-vector problems, and MIMO detection | Convex-piece class-number bounds and exponential or superpolynomial certification lower bounds for stated continuous/box relaxations, contrasted with easier search and stronger SDP relaxations. | [Full paper, within M29](minlp-notes/paper-bb-complexity/main.pdf) | Not applicable |
| M31 | Competitive branching points for spatial branch-and-bound | A Lean-verified four-competitive one-dimensional rule and higher-dimensional limits of node-local rules; tested practical changes stay within seed noise. | [Full paper, within M29](minlp-notes/paper-bb-complexity/main.pdf) | Partial |
| M32 | Separating split inequalities for integer quadratic programming is NP-complete | Strong NP-completeness of integer-QP split-inequality separation, resolving the inspected Burer–Letchford question; related binary families are treated in M35. | [Notes only](minlp-notes/research-20260928b/side-results/split-separation-np-complete.md) | Not applicable |
| M33 | A priori integrality-gap bounds for shortest paths in graphs of convex sets | Explicit structural gap bounds for graph-of-convex-set shortest-path relaxations, with assumptions and limits for motion-planning applications. | [Notes only](minlp-notes/research-20260928b/gcs/a-priori-gap-bounds.md) | Possible |
| M34 | Quadratic hulls on boxes: valid inequalities and semidefinite representability | Exact counterexamples, an order-five SDP inequality family and edge-contact classification, plus the sharp finite-SDP-lift dimension boundary; full three-variable family completeness remains open. | [Full paper](minlp-notes/paper-box-quadratic-hulls/main.pdf) | Possible |
| M35 | The separation complexity of hypermetric and binary quadratic inequalities | Strong NP-completeness under metric and strict-SDP promises, short certificates, rank/threshold algorithms and gap-zero classification; general positive-SDP gap separation remains open. | [Full paper](minlp-notes/paper-binary-separation/main.pdf) | Not applicable |
| M36 | Limits and guarantees for quadratic intersection cuts | Unrestricted corner benchmarks, restricted bilinear-orbit and closure obstructions, scaled-depth guarantees, implied minors and successive-round evidence; no general solver-cut prescription is established. | [Full paper](minlp-notes/paper-quadratic-intersection-cuts/paper.pdf) | Possible |
| M37 | Decomposition-aware global optimization: certified coordinate grids, conditional recourse, and structural limits | Curvature-corrected grids and min-marginal filtering give replayable lower bounds and growth-dependent exact/accuracy-bit algorithms, with recourse extensions and matching structural limits. | [Full paper](minlp-notes/paper-decomposition-aware/main.pdf) | Possible |
| M38 | Constructing separator certificates for sparse global optimization | Constructive affine separator certificates on arbitrary tree decompositions under quadratic growth, including certified inexact solves, exact rational realization and contracting nonlinear dynamics. | [Full paper](minlp-notes/paper-separator-certificates/main.pdf) | Possible |
| M39 | Smoothed exact global optimization beyond convexity | Expected exact algorithms under specified finite rational perturbation laws for low-negative-inertia, sparse polynomial and small-core recourse models; every draw is solved correctly and practical performance is unestablished. | [Full paper](minlp-notes/paper-smoothed-global/main.pdf) | Not applicable |
| M40 | Certified support cuts for shared nonlinear expressions and quadratic blocks | Joint-hull obstructions for overlapping moments, exact constrained-star/small-polytope support, and certified original-variable SCIP cuts; broad benchmark results favor native SCIP. | [Full paper](minlp-notes/paper-certified-support-cuts/main.pdf) | Possible |
| M41 | Rigorous certificates for open MINLPLib instances and an audit of listed dual bounds | Instance-specific primal/dual certificates and a model-semantics audit distinguish exact closures, tiny-row-violation points, sampled evidence and invalid listed dual bounds. | [Full paper](minlp-notes/paper-open-minlplib/main.pdf); [supplement](minlp-notes/paper-open-minlplib/supplement.pdf); [build/status record](minlp-notes/paper-open-minlplib/artifact/RELEASE.md) | Not applicable |
| M42 | Single-tree spatial bounds versus decomposition certificates on sparse problems | Exponential termwise-relaxation trees at a unique nondegenerate path minimum contrast with width-sensitive decomposition certificates; adaptive localization is proved on paths, while general trees and stronger split-robust rates remain open. | [Notes only](minlp-notes/research-20260929/theory-face-exact/face-exact-exponential.md); [adaptive path theorem](minlp-notes/research-20260929/theory-decomposition/adaptive-matching.md); [chain boundaries](minlp-notes/research-20260929/theory-robust-lb/robust-chains.md) | Possible |
| M43 | Vertex binarization for separable concave optimization | Encodes the classical vertex property as a status-binary cardinality constraint, giving linear node counts on a targeted exponential family; random-instance results are unfavorable. | [Notes only](minlp-notes/results/separable-vertex-binarization.md) | Possible |
| M44 | Arithmetic and convergence limits of feasibility-based bound tightening | PosSLP-hard constant-accuracy limiting bounds and doubly exponential iteration lower bounds for specified primitive contractors; the primitive convergence construction has Lean coverage. | [Notes only](minlp-notes/results/fbbt-monotone-system-hardness.md); [iteration theorem](minlp-notes/results/fbbt-doubly-exponential-convergence.md) | Partial |
| M45 | Coordinate dependence and scope limits of disjunctive epigraph relaxations | An unbounded-gap two-ball example becomes exact after an orthogonal coordinate change; corrected P-split and scaling-disjunction claims retain classical overlap and counterexamples. | [Notes only](minlp-notes/notes/common-factor-p-split-rotation-gap.md); [scaling-disjunction results](minlp-notes/results/scaling-disjunctions-hull.md) | Possible |
| M46 | Graph-constrained switching-control rounding | Topology-dependent rounding rates and quantitative relay-mass transitions for graph-restricted switching, extending the unrestricted-control topic under explicit application assumptions. | [Notes only](minlp-notes/research-20260928/applications/graph-constrained-rounding.md) | Possible |
| M47 | Certified benchmark bounds from spectral and geometric structure | Exact finite dual bounds for 18 open nuclear instances and targeted classical-theorem applications to geometric benchmarks; optimality remains unresolved for the nuclear family. | [Notes only](minlp-notes/research-20260922/benchmark-observations/nuclear-bounds.md); [follow-up](minlp-notes/research-20260922/nuclear-global/assessment.md) | Not applicable |
| M48 | Discrete calibrations for control transcriptions and bang-bang switches | Stagewise global certificates, smooth-to-discrete transfer and a switch-curvature window law, with singular-arc and multidimensional boundaries; local calibration existence does not establish global transfer. | [Notes only](minlp-notes/research-20260929/theory-calibration/scouting.md); [bang-bang synthesis](minlp-notes/research-20260929/theory-bangbang/report.md); [window law](minlp-notes/research-20260929/theory-bangbang/window-exactness.md) | Possible |
| M49 | Consistency relaxations on tree decompositions: split classes and bands of exact splits | For one separator, the gap is twice the distance to the band of exact splits; tree bounds, affine-split exactness criteria and kink approximation laws distinguish established duality from new scoped identities. | [Notes only](minlp-notes/research-20260929/theory-consistency/consistency-relaxations.md) | Possible |
| M50 | Analytic singularities and branch-and-bound certificate complexity | Face-integral characterizations connect fixed-relaxation certificate counts to real log canonical thresholds and learning coefficients; boundary faces are essential and constants depend on the instance and dimension. | [Full paper, within M29](minlp-notes/paper-bb-complexity/main.pdf); [topic note](minlp-notes/research-20260929/rlct/rlct-node-complexity.md) | Possible |
| M51 | Moments, region geometry, and recursive relaxations for sparse indicator quadratics | Exact support-count moments and scalar/planar region bounds, with strict-diagonal-dominance recursion; these removed appendices need standalone definitions before becoming a separate note. | [Notes only; possible companion note](minlp-notes/paper-sparse-indicator-quadratics/companion/README.md) | Possible |


### Quantum interior-point methods

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| Q1 | Objective sublevels and central-path Hessian conditioning | Relates every barrier Hessian spectrum to objective-sublevel geometry, with sharp conditioning laws and LP/SDP examples. | [Full paper](qipm-notes/conditioning-paper/main.pdf) | Partial |
| Q2 | The cost of following the central path | Proves sharp extra step costs for staying near the central path, compared with shorter feasible routes in the barrier metric. | [Full paper](qipm-notes/central-path-cost/main.pdf) | Partial |
| Q3 | Access models and right-hand-side mass in Newton solves | Shows how spectral clusters, right-hand-side mass and matrix-versus-factor access change Newton-solve costs beyond condition number. | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q4 | Winner-take-all condensation in block log-determinant SDPs | Derives exact trace-condensation thresholds and links winner mass to Hessian conditioning and quantum state-preparation cost. | [Summary document](qipm-notes/paper/main.pdf) | Possible |
| Q5 | Accuracy curves for hidden-block state conversion | Bounds hidden-block state-preparation queries as functions of accuracy, winner mass and block count; distinguishes vector from averaged output. | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q6 | Condition-one linear programs with hard loading and recovery | Constructs sparse LPs with condition-one reduced Newton systems whose original-coordinate loading or recovery still needs linear queries. | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q7 | Limits of parity-gadget lower-bound constructions | Proves scale, incidence and multiplier obstructions for specified parity gadgets, identifying the assumptions a stronger construction must escape. | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q8 | Loading and recovery hardness for semidefinite programs | Constructs intrinsic SDP loading/recovery lower bounds and accuracy tradeoffs despite condition-one reduced Newton geometry. | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q9 | Trade-offs between preconditioning and state interfaces | Accounts for setup, solve and recovery together; proves preconditioning and reusable-state interfaces can transfer rather than remove query costs. | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q10 | Conditional speedups for sparse quantum interior-point methods | Gives conditional direction reuse, equilibration, face repair and compressed-output algorithms, including optimal block-angular query scaling. | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q11 | A correction to the complexity analysis of the quantum central path method | Corrects the quantum central-path method simulator-norm and clock analyses, with explicit counterexamples and corrected speed tradeoffs. | [Summary document](qipm-notes/paper/main.pdf) | Done |
| Q12 | Curvature, support certificates, and barrier complexity of conic lifts | Bounds cone-factor dimensions, support-certificate ranks and barrier parameters, and derives resource and metric tradeoffs for conic lifts. | [Full paper](qipm-notes/conic-lift-complexity/main.pdf) | Possible |
| Q13 | Classical and quantum query complexity of scalar Newton quantities | Separates classical and quantum costs of estimating scalar Newton quantities under explicit access models; gives structured classical algorithms. | [Full paper](qipm-notes/scalar-newton-paper/main.pdf) | Not applicable |
| Q14 | The quantum cost of unit-normalized spectral shifting | Proves sharp accuracy-dependent query laws for unit-normalized spectral shifting and matrix-versus-factor oracle separations. | [Full paper](qipm-notes/spectral-shift-paper/main.pdf) | Not applicable |
| Q15 | Exponential-cone scenario compression for entropic risk | Compresses one-factor entropic-risk scenarios into a small exponential-cone program with explicit approximation and optimization certificates. | Notes only | Not applicable |

### Molecular thermodynamics

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| TD1 | Finite reservoirs at phase coexistence: full-state accuracy and phase correlations | Proves optimized full-state reservoir-size thresholds at coexistence and shows canonical subsystem marginals can retain shared-bath phase correlations. | [Full paper](thermo-notes/paper-finite-reservoirs/main.pdf) | Not applicable |
| TD2 | Survival-conditioned thermodynamic integration | Distinguishes endpoint from interior survival conditioning, with an exact spectral force potential and bounds on endpoint path dependence. | Notes only | Possible |
| TD3 | Interfacial tension from bulk response in nonlocal double-parabola models | Gives interfacial-tension certificates from bulk response and moment-matched ambiguity examples in a specified nonlocal variational model. | Notes only | Not applicable |
| TD4 | Capacity certificates for reversible nucleation kinetics | Bounds reversible-diffusion capacity using conditional transport resistance, quantifying a correction to projected nucleation kinetics. | Notes only | Not applicable |

### Transport theory

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| TP1 | Designing surface transport under uncertain kinetics: moment thresholds and measurement precision | Proves optimal mobility-design moment thresholds and measurement-precision crossovers under uncertain kinetic defects, including finite-bulk transfer. | [Full paper](transport-notes/paper-uncertain-mobility/main.pdf) | Not applicable |
| TP2 | Kinetic defects in adsorbing channels | Derives singular dispersion laws, exact surface/bulk separation and localized mobility-placement improvements for slow exchange in adsorbing channels. | Notes only | Not applicable |

### Aggregation kinetics

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| AK1 | Sampling-law separation and finite nonlinear corrections in additive coagulation–fragmentation | Proves separation of number and mass sampling, finite nonlinear path corrections and inverse-identification bounds in additive coagulation–fragmentation. | [Full paper](aggregation-kinetics-notes/paper-additive-coagulation/main.pdf) | Not applicable |
| AK2 | Survival under unobserved sister-type dependence in multitype branching | Bounds survival over unobserved sister-type couplings and gives uniform near-critical corrections; basic envelope results have established precedents. | Notes only | Possible |

### Heterogeneous catalysis: proposed experimental programs

| ID | Working title | Main contribution | Write-up / status | Lean |
|---|---|---|---|---|
| CA1 | Physical water management in Fischer–Tropsch synthesis | Proposes tests separating water storage, transport and exposure history to predict useful physical-additive protection in Fischer–Tropsch synthesis. | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA2 | Steam compatibility of cyclic oxides in chemical looping | Proposes steam/CO2 timing tests to distinguish prevention from recovery of cyclic-oxide degradation and quantify useful oxygen-delivery retention. | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA3 | Catalyst demand in polymer ethenolysis | Proposes history-dependent tests predicting sustained polymer ethenolysis output and fresh-sodium demand, beyond established rescue chemistry. | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA4 | Nickel and the useful life of promoted silver epoxidation catalysts | Proposes matched Ni/no-Ni promoted-Ag tests separating fresh selectivity, retention and operating-policy effects on useful ethylene-oxide output. | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA5 | Tungsten coordination and retention in sugar conversion | Proposes a causal coordination–retention relationship linking sugar cleavage to tungsten export; a consequential intervention remains unselected. | Notes only | Not applicable |
| CA6 | Product-rich liquid Ti-zeolite epoxidation | Proposes a product-rich Ti-zeolite epoxidation test against a calibrated solvent/reaction-network baseline, with closure if that baseline suffices. | Notes only | Not applicable |
| CA7 | Oxygen fate and self-cleaning in zirconia-catalyzed styrene production | Proposes oxygen/carbon-balance tests linking zirconia site recovery to sustained styrene output; self-cleaning itself is established prior art. | Notes only | Not applicable |
| CA8 | Acid-site assays and zeolite aging | Proposes tests of whether inserted acid-site assays change later zeolite aging and how that affects prediction of useful catalytic function. | Notes only | Not applicable |

### Supporting investigations and program status

The MINLP tables include the developed paper candidates and substantial
notes-only programs. Broader continuation reports collect their proofs,
implementation boundaries, failed attempts and open questions:
[September 22](minlp-notes/research-20260922/README.md),
[September 25](minlp-notes/research-20260925/README.md),
[September 27](minlp-notes/research-20260927/README.md),
[September 28](minlp-notes/research-20260928/README.md),
[branch-and-bound continuation](minlp-notes/research-20260928b/README.md),
[September 29 synthesis](minlp-notes/research-20260929/SYNTHESIS.md),
[October 1 cut families](minlp-notes/research-20261001/CLOSEOUT.md),
[October 2 theory](minlp-notes/research-20261002/CLOSEOUT.md),
[decomposition](minlp-notes/research-20261002-decomposition/README.md),
[earlier joint convexification](minlp-notes/research-20261002-convexification/README.md),
[arithmetic](minlp-notes/research-20261003-arithmetic/README.md),
[adaptive OBBT](minlp-notes/research-20261003-adaptive-obbt/CLOSEOUT.md), and
[current joint convexification](minlp-notes/research-20261003-convexification/README.md).
Their experiment populations and historical checks remain distinct. The
reported OBBT and broad support-cut studies do not establish a solver speedup;
the reports recommend native SCIP for those tested settings.

Other retained investigations include
[dynamic PSD fiber-scale maintenance](qipm-notes/workbench/active/2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md)
(notes, a scoped online-service lower bound),
[thermodynamic scouting and known-result recoveries](thermo-notes/research/results-summary.md),
and [aggregation antecedents and downgraded directions](aggregation-kinetics-notes/research/RESULTS.md).
These are supporting topics, not additional complete manuscripts.

All catalysis entries are proposed tests rather than completed experiments.
CA1 is the first feasibility priority, CA2 a development reserve, and CA5 an
exploratory hold; the remaining programs are bounded or conditional studies.
Closed negative screens and these priorities remain in the
[catalysis research records](catalysis-notes/research/).

### Status values

**Write-up**

- *Full paper*: a complete, compiled manuscript present in the repository;
  no submission or external peer-review status is implied.
- *Summary document*: part of the long document that collects the quantum
  interior-point results, which the authors asked for instead of separate
  papers.
- *Program document*: a chapter of the document that ranks the proposed
  catalysis programs.
- *Notes only*: the results exist only as the agents' notes and checks.

**Lean**

- *Done*: the main mathematical results are proved in Lean, with no unproved
  steps; software and experiments are not covered.
- *Partial*: some of the results are proved in Lean, but not all.
- *Possible*: not done, but the main claims are mathematical statements that
  could be formalized with current libraries; this is a judgement, not a check.
- *Not applicable*: the main claims rest on numerical evidence, experiments, or
  modelling assumptions, or require a framework that current formal libraries
  do not provide, such as complexity classes, quantum query models, or limit
  theorems for stochastic processes.

## Citation

If you use this repository or refer to its contents, please cite the paper:

> Sergey Gusev and David E. Bernal Neira. AI Agent Swarms as Researchers:
> Progress, Challenges, and Open Questions. arXiv:2609.35719, 2026.
> https://arxiv.org/abs/2609.35719

```bibtex
@misc{gusev2026swarms,
  title         = {{AI} Agent Swarms as Researchers: Progress, Challenges, and Open Questions},
  author        = {Gusev, Sergey and Bernal Neira, David E.},
  year          = {2026},
  eprint        = {2609.35719},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CY},
  url           = {https://arxiv.org/abs/2609.35719}
}
```

## License

Original repository material is released under the [MIT License](LICENSE).
Redistributed third-party benchmarks and software retain their own licenses;
see [third-party notices](THIRD_PARTY_NOTICES.md).
