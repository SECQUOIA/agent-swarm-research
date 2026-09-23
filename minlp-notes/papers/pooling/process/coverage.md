# Pooling manuscript coverage map

This is the final coverage inventory for the completed pooling manuscript. All six authoring stages and both whole-paper review rounds are closed; the final round has no accepted findings. See [status.md](status.md) and [the final adjudication](whole-round-02/adjudication.md). Historical “PASS” labels were not used as proof. Canonical results and duplicated investigation drafts were compared mathematically; stronger theorems do not erase distinct restrictions or certificate guarantees.

## Coherent manuscript stages

1. Foundations: physical variants, homogeneous zero-flow semantics, threshold/feasibility, bit/representation conventions, rank-one block identity, acyclic and cyclic profitable-flow/conic tools, facial integrality.
2. Algebraic complexity and certificates: ETR completeness and bounded-data/one-pool variants, algebraic degree, fixed-parameter linear-fiber NP certificates.
3. Restricted hardness and approximation: local/all-degree-two hardness, tolerance extension, two-pool positive-product reduction/FPTAS, bypass copy circuits, single-upper-quality/constant-data refinements, five-exception feasibility boundary.
4. Structural exact algorithms: full fixed-core/block theorem, bypass vertex integrity and quality rank, planar boundary projection and bounded attachments/objective support.
5. Contract algorithms: conservation and fixed products, quality-scaled cuts, fixed-rank and arbitrary-quality exceptions, common capacities, two quality vectors; generic path-support results and their precise scope.
6. Synthesis: theorem comparison, remaining boundaries, physical path complexity obstructions, related rank-one convexification/low-rank cost results and common-factor/network-simplex context, sources and conclusions.

Full proofs of genuinely pooling developments belong in the paper or appendices. Adjacent standalone programs receive an accurate scoped discussion and explicit references to their separate repository results; reproducing unrelated full conic-lower-bound or power-flow papers would not make a coherent pooling manuscript.

## Canonical results and necessary general theorems

| File | Stage | Disposition |
|---|---:|---|
| `results/pooling-triviality-polynomial.md` | 1 | Destination decomposition, single-product LP projection, polynomial profitable-flow test, shortest-path sparse witness, output-count approximation, exact uncapacitated conic hull; established formulation ingredients explicitly credited. |
| `results/pooling-facial-quality-integrality.md` | 1 | Necessary and sufficient facial condition for universal integral optima; recognition LP, bounded-pool/quality face enumeration, endpoint disjunction/MILP. Integral-optimum statements require feasibility. |
| `results/pooling-existential-theory-of-reals.md` | 2 | Manuscript at `s2:etr-complete`, `s2:bounded`, `s2:variants`, `s2:algebraic-witness`: full gadgets and chain refinement, rational flow bijections, both directions, field/degree consequence. Algebraic transfer narrowed to compact basic-closed singleton source route; one-upper-attribute ETR boundary retained open. Stage 2 closed after 15 full reviews and checked minor repairs. |
| `results/pooling-one-pool-bypass-existential-reals.md` | 2 | Manuscript at `s2:one-pool-etr`: full normalization, attributes/pins, saturation, both directions, capacities, dense polynomial encoding and bijection. Unrestricted attributes distinguished from fixed-quality NP scope. Stage 2 closed after 15 full reviews and checked minor repairs. |
| `results/pooling-one-quality-degree-two-hardness.md` | 3 | Manuscript: `s3:co`, `s3:local-degrees`, `s3:orientation`. Self-contained occurrence-splitting, degree-three orientation and bipartite subdivision; both layer placements, omission of pool capacities, PARTITION/private-layer corollaries, LP degree-one boundary. Endpoint certificate proves strong NP-completeness for threshold decision with upper output quality specifications only in {0,1}. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-all-degrees-two.md` | 3 | Manuscript: `s3:all-two-thm`, `s3:weighted`, `s3:tolerance`. Full cleanup and integral replacement, independent-set identity/recovery, factor-three approximation transfer, merged-lax exactly-two degrees, and signed weighted integer-capacity/multigraph rainbow extension, retaining physical arc capacities in mode bounds. These families use upper output quality specifications only. Strong NP-completeness for zero-tolerance threshold decision uses the stage-1 endpoint certificate. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-two-pools-two-outputs-hardness.md` | 3 | Manuscript: `s3:matsui`, `s3:two-pools`, `s3:two-pool-value`. Full corrected positive-product source proof, preprocessing/simplex encoding, physical objective identity, tree and single-bypass forms, normalizations/economics, omitted capacities/exact demands, and fixed-outlet-fraction NP membership. Ordinary hardness only. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-one-pool-bypass-np-completeness.md` | 3 | Manuscript: `s3:copy-lemma`, `s3:row-copy`, `s3:base-bypass`. Full four-port conversion, port allocation, bounded-coefficient cone universality, explicit source generator bounds, physical objective identity and fixed-quality NP membership; exact scalar or two upper attributes. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-one-pool-upper-bounds-np-completeness.md` | 3 | Manuscript: `s3:cycles`, `s3:hoffman`, `s3:upper-only`. Complete one-upper-quality cycle/splitting proof and explicit polynomial-bit error-bound/penalty, radial outlet repair, exact optimum shift, distinct economic-objective repair and normalization. Ordinary NP-completeness. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-constant-data-two-feed-np-completeness.md` | 3 | Manuscript: `s3:linear-circuits`, `s3:constant-thm`. Full binary signed-row realization, completed rational LP projection theorem, source dyadic normalization, two actual feeds/outlets, fixed alphabets/degrees, threshold circuit and contract-completion economics. Strong NP-completeness; no approximation gap inferred. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-five-exception-feasibility-hardness.md` | 3 | Manuscript: `s3:five-thm`. Full slack comparisons, complementary-port grouping, supply-two/four source splitting, exact ordinary products, five-exception audit, constant data and redundant pool bound, strong feasibility NP-completeness. Positive contracts retained. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `results/pooling-bypass-structure-algorithm.md` | 4 | Manuscript: `s4:vertex-integrity`, `s4:structural-corollaries`. Full exact affine-rank compression, arc ownership, covered-product mass totals, bounded aggregate rows, compactness, inactive-pool semantics, decomposition recognition, and algebraic optimizer recovery. Includes fixed-quality/vertex-cover, bounded components/matching, fixed distinct profiles, no-bypass/rank, fixed-input, and elementary LP cases. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `results/pooling-degree-two-boundary-projection.md` | 4 | Manuscript: `s4:polygon-composition`, `s4:path-projection`, `s4:bounded-attachments`, `s4:two-two-feasibility`, `s4:fixed-support`, `s4:equality-support`, `s4:degree-boundary`. Full planar envelope/composition and balanced bit/lifting proofs, arbitrary-quality 4a multi-pool core and 13-variable specialization, fixed retained-coordinate objectives/closed constraints, equality-reduced costs and price-change example, strong product-degree-three feasibility boundary. Dense aggregate and unbounded-attachment limits explicit. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `results/pooling-fixed-product-contracts-algorithm.md` | 5 | Manuscript: `s5:fixed-products`, `s5:boundary-masses`, `s5:boundary-identities`. Full local intake elimination, conserved vector masses, 4r core, detached-component and zero-flow proof, restrictive common bounds, standard economics and designated-cost scope; arbitrary quality count/rank retained. Stage 5 closed after 15 full reviews and checked minor repair. |
| `results/pooling-quality-scaled-path-flow.md` | 5 | Manuscript: `s5:conservation`, `s5:cuts`, `s5:quadratic-field`, `s5:fixed-boundary`. Full signed scaling and all output degeneracies, connected interval-node cuts and candidate expansion, quadratic-field recovery, boundary shifting, scalar/rank-one compression, redundant common-bound scope. Stage 5 closed after 15 full reviews and checked minor repair. |
| `results/pooling-contract-exceptions-algorithm.md` | 5 | Manuscript: `s5:quality-chart`, `s5:fixed-rank`, `s5:arbitrary-exceptions`. Full scalar and fixed-rank chart dependency, ambient-rank polynomial chart family, every residual quality equation, two-dimensional active ordinary-product space, exceptional-only fraction branch, strict cells and attainable-value optimization, designated costs; redundant common bound retained. Stage 5 closed after 15 full reviews and checked minor repair. |
| `results/pooling-contracted-common-capacity-algorithm.md` | 5 | Manuscript: `s5:clamp`, `s5:box-base`, `s5:restrictive-capacity`, `s5:throughput-optimization`. Full symbolic binary path/cycle minimization, classical box-base normalization/submodularity/greedy proof, support interpolation and arbitrary common interval. Added exact minimum/maximum throughput and linear pool-throughput cost corollary. Polynomial-degree common-field witnesses; no dense arc-cost claim. Stage 5 closed after 15 full reviews and checked minor repair. |
| `results/pooling-two-source-qualities-convex-feasibility.md` | 5 | Manuscript: `s5:two-vector-theorem`, `s5:two-vector-extensions`. Full two-full-vector compression, variable-supply/class-total scaling and physical equivalence, restrictive common upper bound, shared rank-one convex QP, exact strict-interior procedure, polynomial rational recovery, exact-source and additional signed outlet-resource rows. Zero outlet/common lower bounds and feasibility-only scope explicit. Stage 5 closed after 15 full reviews and checked minor repair. |
| `results/fixed-core-block-polyhedral-optimization.md` | 4 | Manuscript: `s4:fixed-core`, `s4:core-limits`, `s4:fixed-inputs`, `s4:fixed-qualities`. Complete general theorem: local candidate validity, support sign enumeration, squared-denominator clearing with growing degree, fixed-variable formula, compact optimization, common-field LP recovery, and computed polynomial-bit core/slack boxes. All pooling corollaries and discrete/nonlinear-leaf limits retained. Source/product historical comparison updated against accepted stage 3. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `results/fixed-parameter-linear-fibers-np-membership.md` | 2 | Manuscript at `s2:fiber-np`, `s2:pooling-np`, `s2:no-bypass-np`: full basis-index verifier, bit/degree/interpolation proof, all pool*quality/rank and pool*product parameterizations, fixed pool/input consequence, and established one-pool no-bypass NP certificate. No polynomial-algorithm inference. Stage 2 closed after 15 full reviews and checked minor repairs. |
| `results/rank-one-low-rank-costs.md` | 6 | Manuscript: Full proofs at s6:rank-theorem, s6:rank-one-cost and s6:oracle: projected-box enumeration, slice edges, common-total rational functions, zero total, quadratic-field reconstruction, fixed-attribute physical Lagrangian costs and perturbation guarantee; established low-rank box methods credited. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/rank-one-row-column-hardness.md` | 6 | Manuscript: s6:related, citation s6:margin-note: general-matrix strong hardness, rational threshold certificates, quadratic optima and FPT in smaller matrix dimension. Additive physical cost distinction; full unrelated reduction omitted. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/rank-one-zero-lower-hardness.md` | 6 | Section 6.7 (`s6:related`), citation `s6:zero-lower-note`: strong general-cost threshold hardness with all row and column margin lower bounds zero and upper bounds one, integer matrix costs, and a negative threshold. Additive physical cost distinction retained; adjacent penalty proof cited. Exact finite checker: `code/rank_one_zero_lower/verify_penalty.py`; retained root run: `papers/pooling/verification/logs/whole-round01-zero-lower-penalty.txt`. Added for whole-paper round 1 finding M1; checked in the complete round 2 with no accepted findings. |
| `results/rank-one-correlation-face-conic-lower-bounds.md` | 6 | Manuscript: s6:related, citation s6:face-note: face atoms and elementary selection proof, exact LP/SOC/fixed PSD-block/unrestricted PSD distinctions; separate conic lower-bound program cited. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/rank-one-correlation-face-stability.md` | 6 | Manuscript: s6:related, citation s6:stability-note: entrywise l1 outer sandwich, A_m=m(184m+6), exponential LP size at eta<=1/A_m; uniform objective metric and limits. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/rank-one-approximate-sdp-lower-bound.md` | 6 | Manuscript: s6:related, citation s6:approx-sdp-note: eta<=1/(2A_m), exp(Omega((m/log m)^(2/13))) total PSD order; distinct shifted quadratic slack mechanism and objective-specific limits. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/common-factor-fixed-linking-optimization.md` | 6 | Manuscript: s6:related, citation s6:common-factor-note: finite boxes/products, fixed linking rows, scalar-dependent bounded-LP bases, signed/integer extensions; oracle versus hull distinction. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/common-factor-integer-anchor-hull.md` | 6 | Manuscript: s6:related, citation s6:integer-anchor-note: consecutive integer scalar interval, mean-preserving rounding and telescoping avoid enumeration; no extra leaf/product coupling. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/common-factor-reciprocal-anchor-hulls.md` | 6 | Manuscript: s6:related, citation s6:anchor-faces-note: individual one-leaf hulls can have incompatible common-factor distributions. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/common-factor-reciprocal-anchor-full-hull.md` | 6 | Manuscript: s6:related, citation s6:anchor-full-note: positive scalar interval, box leaves, call-envelope distribution and polynomial rational separation; extra product/linking restrictions excluded. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/network-simplex-universality.md` | 6 | Manuscript: s6:related, citation s6:network-universality-note: compact extended hull versus sparse original-space coordinate-section/coefficient universality at simplex dimension two; transportation source credited; no pooling inference. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/network-simplex-parallel-path-hull.md` | 6 | Manuscript: s6:related, citation s6:network-parallel-note: equality-balance parallel-path blocks, exact subset cuts and unit flow/product coefficients; not all series-parallel graphs. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/network-simplex-cycle-theta-hull.md` | 6 | Manuscript: s6:related, citation s6:network-cycle-note: one/two-dimensional circulation blocks, equality balance and slack-arc topology qualifications; no physical mixing inference. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `results/ac-power-flow-existential-reals.md` | 6 | Manuscript: s6:related, citation s6:power-note: resistive gadgets and qualified real-angle AC transfer are separate applications; full power-flow theorems omitted. Stage 6 closed after 15 full reviews and checked minor repairs. |

## Distinct investigations, refinements, and superseded routes

| File | Stage | Disposition |
|---|---:|---|
| `notes/pooling-recirculation-investigation.md` | 1 | Distinct reviewed cyclic extension: algebraic pure circulations, absorption decomposition, exact single-product LP, sign/conic hull, singular mixing/conditioning. Do not publicly allege final-journal defect without checking final version. |
| `notes/pooling-positive-tolerance-extension.md` | 3 | Manuscript: `s3:tolerance`, `s3:tolerance-example`. Full cleanup loss and gap constants for fixed positive rational tolerance in the upper-only output quality family; added exact K4 example showing integral optimality fails at every tolerance in (0,1/2]. No endpoint NP certificate asserted here. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-positive-product-subfamily-approximation.md` | 3 | Manuscript: `s3:fptas`. Full ceil(1/epsilon)+1 LP grid argument, zero grid/zero optimum, rational bit bounds and physical reconstruction. Requires supplied subfamily representation; no general pooling FPTAS. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-bypass-degree-four-hardness.md` | 3 | Manuscript: `s3:half`. Full-port four-source average and padded tree, exact projection, capacities and size retained before the stronger half-port refinement. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-bypass-degree-three-hardness.md` | 3 | Manuscript: `s3:half`. Full/half formulas, mixed-chain links, three-port average, signed children/zero padding, root dyadic capacities, degree and size audit. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-bypass-linear-universality.md` | 3 | Manuscript: `s3:linear-circuits`. Earlier incomplete binary route replaced by a complete constant-data representation proof for arbitrary rational rows on bounded signals. No unchecked earlier scope asserted. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-single-upper-quality-cycles.md` | 3 | Manuscript: `s3:cycles`. Separate full/half closed cycles, residual summation, mixed positive conversion qualities, explicit full/half coupling and input-degree-two collector substitution. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-upper-flow-only-penalty-hardness.md` | 3 | Promoted duplicate incorporated at `s3:hoffman`, `s3:upper-only`; full explicit penalty proof retained. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-constant-data-two-feed-hardness.md` | 3 | Promoted duplicate incorporated at `s3:linear-circuits`, `s3:constant-thm`. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-one-pool-bypass-copy-hardness.md` | 3 | Promoted duplicate incorporated at `s3:copy-lemma`, `s3:row-copy`, `s3:base-bypass`. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-two-pools-two-outputs-investigation.md` | 3 | Promoted duplicate incorporated at `s3:matsui`, `s3:two-pools`; source arithmetic independently repaired in `s3:corrected-matsui-gap`. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-all-degrees-two-investigation.md` | 3 | Main upper-only quality threshold-decision proof at `s3:all-two-thm`; distinct upper-only weighted integer-capacity/rainbow extension at `s3:weighted`, strengthened to signed linked mode rewards and retaining physical arc bounds; upper-only tolerance family at `s3:tolerance`. Earlier MAX-2-SAT route not needed. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-fixed-exception-hardness-refinement.md` | 3 | Promotion pointer; final full proof at `s3:five-thm`. Stage 3 closed after two rounds of 15 full reviews and checked repairs. |
| `notes/pooling-bypass-vertex-cover-algorithm.md` | 4 | Manuscript: `s4:vertex-integrity`, `s4:structural-corollaries` (i). Distinct fixed-quality vertex-cover specialization retained explicitly, including unbounded hub bypasses, sharper singleton block dimension p+c, fixed deletion-set enumeration, and bounded-component extension. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-quality-rank-extension.md` | 4 | Manuscript: `s4:quality-coordinates`, `s4:covered-totals`, `s4:covered-quality`. Affine-rank precursor fully incorporated; arbitrary covered-product specification rows moved into core through fixed many total/coordinate masses. Exact rational rank, unrestricted specification vectors, rank-zero and fixed-profile cases explicit. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-degree-two-boundary-projection.md` | 4 | Promotion pointer covered by full endpoint proof at `s4:polygon-composition`, `s4:path-projection` and bounded-attachment/retained-objective consequences. Degenerate polygons, repeated cycle endpoints, exact algebraic affine lifts, and dense-aggregate exclusion retained. Stage 4 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-degree-two-bypass-investigation.md` | 6 | Manuscript: Full proofs at s6:path-realization and s6:price-response: tangent and original smaller-interval directions, ordinary revenues, uniform lower-bound removal; s6:response-size and s6:ports prove explicit-degree and coordinate-projection limits. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-degree-two-vertex-forcing.md` | 6 | Manuscript: Full proofs at s6:vertex-forcing, s6:local, s6:integer-lift, s6:lp-hull and s6:alphabet-geometry: interface/economics, isolated optima, strict perturbation, integer dimension, compact hull and optimizer, general supplies; throughput counterexample retained. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/degree-two-fixed-quality-alphabet-investigation.md` | 6 | Manuscript: Full relay and contract-removal proof at s6:price-response; three-quality nonlinear family at s6:alphabet-geometry with duplicate-source economics and nonlinear contracts retained. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/klee-minty-rank-one-slab-hardness.md` | 6 | Manuscript: Full abstract proof at s6:certificate and s6:slab-hardness: SUBSET SUM rounding, nonempty compactness, NP certificate and fixed-coefficient padding; no physical weighted-slab realization. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/parametric-path-lp-obstructions.md` | 6 | Manuscript: Known shadow credited at s6:telescoping; tangent alternative, state-message and line-factor proofs at s6:response-size, linear-size exact recurrence; description versus evaluation distinction. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/parametric-path-lp-investigation.md` | 6 | Manuscript: Merged at s6:telescoping and s6:response-size: original source direction retained, self-contained tangent alternative, short recurrence; no generic polynomial elimination inference. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/one-parameter-path-projection-investigation.md` | 5 | Manuscript: `s5:quasipoly-path`. Full balanced parameterized Fourier--Motzkin/minor-sign selection, empty and lower-dimensional fibers, row/cell recurrences, degree/height and common-field recovery. Distinct general quasipolynomial result retained; no dense aggregates or multidimensional additive-overlay inference. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/parametric-affine-strip-path-projection.md` | 5 | Manuscript: `s5:strip`, `s5:distance-test`. Full gain normalization, exact distance inequalities and lift, signed/zero gains, arbitrary tree orientation and reciprocal factors, polynomial dense encoding, fixed total cycle-rank projection, infimum-versus-attainment distinction. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/parametric-path-cut-clamp-investigation.md` | 5 | Manuscript: `s5:clamp`, `s5:restrictive-capacity`. Promoted symbolic recurrence and completed support-capacity development proved in full; binary submodular energy scope distinguished from generic path programs. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/parametric-path-cut-box-truncation-source.md` | 5 | Manuscript: `s5:box-base`. Full nonempty-base specialization, submodularity, normalization, signed cost greedy proof. Explicit primary attribution to Shioura--Shakhlevich--Strusevich Theorems 1–2 and equation (11), printed p.192. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-all-product-contracts-quasipolynomial.md` | 5 | Manuscript: `s5:conservation`, `s5:capacity-counterexample`, `s5:quasipoly-path`, `s5:quadratic-field`. Conserved mass/vector-quality identities and explicit T=1/[q(2-q)] common-capacity counterexample retained. Obsolete physical quasipolynomial upper bound subsumed by polynomial scaling; distinct generic projection proved separately. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-bounded-contract-exceptions-algorithm.md` | 5 | Manuscript: `s5:quality-chart`, `s5:fixed-rank`, `s5:exception-balances`, `s5:exception-profit`. Complete scalar boundary core (1+5s), quadratic connected-cut projection, actual conservation, strict-cell objective union and field recovery; designated cost endpoints retained. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-fixed-rank-contract-exceptions-algorithm.md` | 5 | Manuscript: `s5:quality-chart`, `s5:fixed-rank`, `s5:directions`, `s5:residual-quality`. Full affine-rank compression, chart coverage, singular-vector LPs, nonzero/zero residual coefficients, all-quality preservation and polynomial candidate-cut clearing. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-contract-exceptions-arbitrary-qualities.md` | 5 | Promotion pointer incorporated in full at `s5:arbitrary-exceptions`, with substantive dependencies at `s5:quality-chart` and `s5:fixed-rank`. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-fixed-product-contracts-algorithm.md` | 5 | Promotion pointer incorporated in full at `s5:fixed-products`. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-quality-scaled-path-flow.md` | 5 | Promotion pointer incorporated in full at `s5:quadratic-field`, including `s5:fixed-boundary`. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-two-source-qualities-convex-feasibility.md` | 5 | Completed investigation pointer incorporated at `s5:two-vector-theorem`, with strengthened variable supplies and additional resource/exact-source statements at `s5:two-vector-extensions`. Stage 5 closed after 15 full reviews and checked minor repair. |
| `notes/pooling-unbounded-attachments-investigation.md` | 6 | Manuscript: s6:open: parameter-cell and aggregate obstacles, failed helper-pool counterexample, contracted/two-vector/common-capacity resolutions; s6:slab abstract warning; unrestricted classification open. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-single-quality-bypass-investigation.md` | 6 | Manuscript: s6:open closes unrestricted one-pool/one-quality threshold question by accepted stage-3 theorems. Introduction and s6:open retain subdivision/capacity distinctions; structural proposals map to stage 4. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/pooling-endpoint-quality-structure.md` | 1 | Earlier endpoint/facial development promoted to facial result; duplicate. |
| `notes/pooling-triviality-investigation.md` | 1 | Source assessment for sign/conic result; attribution, not an additional theorem. |
| `notes/fixed-parameter-lp-np-membership.md` | 2 | Earlier basis-certificate development promoted to supporting result. |
| `notes/rank-one-parametric-linear-programs.md` | 6 | Manuscript: Full two-LP sign-disjunction proof at s6:parametric, including zero signal, rational recovery, objective/RHS hypotheses, source rank-two comparison; no pooling path inference. Stage 6 closed after 15 full reviews and checked minor repairs. |
| `notes/fixed-core-convex-leaf-arithmetic-barrier.md` | 6 | Manuscript: Full singleton Square-Root Sum reduction at s6:parametric; exact common-field arithmetic caveat, not NP-hardness or approximation obstruction. Stage 6 closed after 15 full reviews and checked minor repairs. |

## Mathematical and source issues identified at intake

- One quality with two-sided specifications, two coordinates with upper-only specifications, and one coordinate with upper-only specifications are distinct restriction classes. The final one-upper-quality ETR route remains incomplete; copy hardness proves NP-completeness in a different fixed-parameter setting, not ETR completeness.
- General degree-two bypass feasibility with unrestricted attachments is not settled by endpoint projection: forgotten mass/quality aggregates remain. Exponential support curves do not establish algorithmic hardness.
- Lower-free feasibility is trivial in these homogeneous models; positive profit thresholds cannot be silently called feasibility hardness.
- Restrictive common capacity is handled for fully contracted scalar/rank-one degree-two networks, and an upper bound for two source-quality vectors; this does not remove the redundant-capacity hypothesis of arbitrary-quality bounded exceptions.
- The two-quality-vector result excludes positive pool/outlet lower bounds and arbitrary variable-cost optimization. Its source intervals extension is part of the final result.
- The exact contracted quality-scaled witness can use one quadratic field; common-capacity and general contract-exception algorithms promise polynomial algebraic representations, not the same quadratic-degree bound.
- The rank-one margin hardness objective is arbitrary in input-product matrix coordinates. Physical feed/outlet costs are additive row/column costs. State this mismatch before drawing connections.
- `code/pooling_degree_two/irrational_example.py` has a known prose transcription error found by root: the displayed j1 bound omits division by `(1+b)`. Correct is `b(3/4+b/2)/(1+b)<=1/4`, yielding `2b^2+2b-1<=0` and `(sqrt(3)-1)/2`. A restricted-family calculation is not by itself a global optimum proof.
- `literature/papers/dey2015-analysis-of-milp-techniques-for/fulltext.md` is a slide deck, despite article metadata. Root retrieved the actual open article to `/tmp/pooling-paper-sources/dey-gupte-article.pdf` and `.txt`. Use the article for article theorem locators.
- `literature/papers/boland2016-new-multi-commodity-flow-formulations/` stores the June 2015 manuscript as its open artifact. A closed-circulation counterexample invalidates a blanket invertibility claim in that manuscript. The foundations explain the mathematical exception without asserting a defect in the unchecked final journal text.
- Universal integral-optimum statements must be conditioned on nonempty feasible flow sets. Deleting incompatible arcs in a network branch requires rejecting positive lower bounds on those arcs.
- Primary priority assessments are provisional. Results based on destination disaggregation and one-output rounding explicitly credit existing formulations; ordinary supporting LP, network integrality, real algebra, Hoffman cuts, and submodular base-polyhedron facts must be attributed as established tools.

## Source, review, and history files

The following relevant files are audit/history evidence or related-program supporting notes. They are not independent theorem claims and must not be counted as additional developments. Their concrete corrections must be checked when writing the associated result. Files are listed individually so the inventory remains auditable.

- `notes/audit-rank-one.md` — internal review: Independent audit of the row-and-column rank-one results.
- `notes/bilinear-graph-binary-complexity-novelty.md` — source/priority audit: Literature audit: precision versus integer dimension for bilinear graphs.
- `notes/candidate-directions-2026-09-05.md` — history or adjacent supporting investigation: Candidate research directions (brainstorm, 2026-09-05).
- `notes/candidate-directions.md` — history or adjacent supporting investigation: Candidate research directions (brainstorm output, 2026-09-04).
- `notes/common-factor-anchor-novelty.md` — source/priority audit: Independent novelty audit: a convex anchor and common-factor products.
- `notes/common-factor-investigation.md` — history or adjacent supporting investigation: Common-factor products with linking constraints.
- `notes/common-factor-literature-audit.md` — source/priority audit: Literature audit for the common-factor results.
- `notes/common-factor-network-parallel-paths.md` — history or adjacent supporting investigation: Parallel-path network investigation.
- `notes/common-factor-network-positive.md` — history or adjacent supporting investigation: Positive network–simplex investigation.
- `notes/common-factor-network-simplex.md` — history or adjacent supporting investigation: Network–simplex investigation.
- `notes/common-factor-p-split-balls.md` — history or adjacent supporting investigation: Exact basic P-split relaxation for two translated balls.
- `notes/common-factor-p-split-correction.md` — history or adjacent supporting investigation: P-split Theorem 6: counterexample and a geometric repair.
- `notes/common-factor-p-split-rotation-gap.md` — history or adjacent supporting investigation: An unbounded coordinate effect in the basic P-split relaxation.
- `notes/constructive-minlp-new-direction.md` — history or adjacent supporting investigation: Constructive direction: fixed core with many polyhedral output blocks.
- `notes/fixed-core-block-optimization-novelty.md` — source/priority audit: Novelty audit: fixed nonlinear core and polyhedral blocks.
- `notes/log.md` — history or adjacent supporting investigation: Research log.
- `notes/new-directions-investigation.md` — history or adjacent supporting investigation: Investigation: unconditional conic complexity of a pooling rank-one hull.
- `notes/open-problems-from-literature.md` — source/priority audit: Open problems and conjectures mined from the literature base (2026-09-04).
- `notes/pooling-constant-data-two-feed-hardness-novelty.md` — source/priority audit: Source audit: constant-data pooling with two pool feeds.
- `notes/pooling-degree-two-novelty.md` — source/priority audit: Novelty audit: one-quality pooling with bounded degrees.
- `notes/pooling-existential-reals-novelty.md` — source/priority audit: Prior-literature audit: ∃R-completeness of the pooling problem.
- `notes/pooling-fixed-pools-qualities-source-audit.md` — source/priority audit: Fixed pools and qualities: source discrepancy and constructive direction.
- `notes/pooling-fixed-quality-np-membership-novelty.md` — source/priority audit: Prior-literature audit: NP membership with fixed pool-quality dimension.
- `notes/pooling-quality-scaled-contracts-novelty.md` — source/priority audit: Quality-scaled fixed-contract pooling: bounded source assessment.
- `notes/pooling-single-quality-bypass-novelty.md` — source/priority audit: Novelty audit: one pool with fixed qualities and unrestricted bypasses.
- `notes/pooling-two-pools-two-outputs-novelty.md` — source/priority audit: Novelty checks for the two-pool/two-output hardness candidate.
- `notes/pooling-two-source-qualities-convex-feasibility-novelty.md` — source/priority audit: Two source-quality vectors: focused source comparison.
- `notes/power-flow-existential-reals-novelty.md` — source/priority audit: Prior-literature audit: ∃R-completeness of resistive and AC power-flow feasibility.
- `notes/rank-one-conic-novelty.md` — source/priority audit: Equivalent-object novelty screening for the rank-one conic results.
- `notes/rank-one-cost-rank-investigation.md` — history or adjacent supporting investigation: Investigation of low-rank costs for rank-one flow blocks.
- `notes/reopened-run-status.md` — history or adjacent supporting investigation: Reopened run: status of work (updated 2026-09-05, evening).
- `notes/research-closeout.md` — history or adjacent supporting investigation: Research closeout and verification record.
- `notes/research-continuation-assessment.md` — history or adjacent supporting investigation: Assessment of the 2026-09-05 research continuation.
- `notes/research-continuation-closeout.md` — history or adjacent supporting investigation: Closure of the continued research program.
- `notes/research-open-thread-audit.md` — history or adjacent supporting investigation: Audit of existing research threads at closure.
- `notes/research-status.md` — history or adjacent supporting investigation: Final research assessment.
- `notes/review-common-factor-integer.md` — internal review: Independent audit of the integer reciprocal-anchor hull.
- `notes/review-common-factor-network-parallel-paths.md` — internal review: Independent audit: parallel-path network blocks.
- `notes/review-common-factor-network-positive.md` — internal review: Independent audit of cycle/theta network–simplex hulls.
- `notes/review-common-factor-network-simplex.md` — internal review: Independent audit of sparse network–simplex universality.
- `notes/review-common-factor-novelty-reductions.md` — internal review: Check of the common-factor novelty reductions.
- `notes/review-common-factor-p-split-balls.md` — internal review: Independent audit: exact basic P-split relaxation of two balls.
- `notes/review-common-factor-p-split-rotation-gap.md` — internal review: Independent audit: unbounded coordinate dependence of basic P-split.
- `notes/review-common-factor-root.md` — internal review: Root review of reciprocal-anchor hull results.
- `notes/review-common-factor.md` — internal review: Independent audit of the common-factor investigation.
- `notes/review-existential-reals-closeout.md` — internal review: Closeout audit: pooling and power-flow existential-real completeness.
- `notes/review-fixed-core-block-optimization-second.md` — internal review: Second independent review: fixed core with small polyhedral blocks.
- `notes/review-fixed-core-block-optimization.md` — internal review: Independent review of fixed-core block optimization.
- `notes/review-fixed-parameter-lp-np-membership-second.md` — internal review: Second independent review: NP membership with fixed real parameters.
- `notes/review-fixed-parameter-lp-np-membership.md` — internal review: Independent review: NP membership for fixed-parameter linear fibers.
- `notes/review-fixed-quality-alphabet-reset.md` — internal review: Independent review: fixed-quality-alphabet bypass reset.
- `notes/review-network-simplex-universality.md` — internal review: Independent audit of network–simplex universality.
- `notes/review-one-parameter-path-projection-second.md` — internal review: Second independent audit: one-parameter bounded planar path projection.
- `notes/review-one-parameter-path-projection.md` — internal review: Independent review: one-parameter polygon-path projection.
- `notes/review-parametric-affine-strip-path-projection.md` — internal review: Independent review: affine-strip path projection.
- `notes/review-parametric-affine-strip-tree-cycle-rank.md` — internal review: Independent review: affine strips on trees and fixed total cycle rank.
- `notes/review-parametric-path-cut-clamp.md` — internal review: Independent review of polynomial binary-path cut values.
- `notes/review-parametric-path-cut-pooling-capacity-extension.md` — internal review: Independent audit: contracted pooling with a common capacity interval.
- `notes/review-parametric-path-cut-pooling-capacity-second.md` — internal review: Second review: common pool-capacity interval via path cuts.
- `notes/review-pooling-all-degrees-two-second.md` — internal review: Second independent review: pooling with all degree bounds two.
- `notes/review-pooling-all-degrees-two.md` — internal review: Independent review: all four pooling degree bounds at most two.
- `notes/review-pooling-all-product-contracts-quasipolynomial.md` — internal review: Independent review: all-product-contract pooling feasibility.
- `notes/review-pooling-all-product-contracts-second.md` — internal review: Second independent review: fully contracted pooling with unbounded attachments.
- `notes/review-pooling-bounded-attachments-second.md` — internal review: Second audit: fixed total number of pool attachments.
- `notes/review-pooling-bounded-attachments.md` — internal review: Independent review: fixed total pool-incident arcs.
- `notes/review-pooling-bounded-contract-exceptions-benders.md` — internal review: Independent second audit: bounded contract exceptions.
- `notes/review-pooling-bounded-contract-exceptions-second.md` — internal review: Independent audit: scalar pooling with bounded contract exceptions.
- `notes/review-pooling-bypass-degree-four-second.md` — internal review: Second independent review: degree-four bypass refinement.
- `notes/review-pooling-bypass-degree-four.md` — internal review: Independent review: degree-four bypass hardness.
- `notes/review-pooling-bypass-degree-three-second.md` — internal review: Review of the degree-three half-port construction.
- `notes/review-pooling-bypass-degree-three.md` — internal review: Independent review: degree-three bypass construction.
- `notes/review-pooling-bypass-structure-second.md` — internal review: Second independent review: pooling with controlled bypass structure.
- `notes/review-pooling-bypass-vertex-cover.md` — internal review: Independent review: pooling with controlled bypass structure.
- `notes/review-pooling-constant-data-two-feed-second.md` — internal review: Second review: constant-data hardness with two pool feeds.
- `notes/review-pooling-constant-data-two-feed.md` — internal review: Independent review: constant-data hardness with two pool feeds.
- `notes/review-pooling-contract-exceptions-arbitrary-qualities-benders.md` — internal review: Independent audit: removing the quality-rank restriction.
- `notes/review-pooling-contract-exceptions-arbitrary-qualities-second.md` — internal review: Independent audit: arbitrary qualities with bounded contract exceptions.
- `notes/review-pooling-degree-three-refinement.md` — internal review: Referee review: degree-three refinement (Lemma 2 and Theorem 3).
- `notes/review-pooling-degree-two-boundary-projection-second.md` — internal review: Independent second audit: degree-two bypass feasibility.
- `notes/review-pooling-degree-two-boundary-projection.md` — internal review: Independent review: bounded path endpoint projection.
- `notes/review-pooling-degree-two-hardness.md` — internal review: Referee review: one-quality pooling with degree-two pools is strongly NP-hard.
- `notes/review-pooling-degree-two-independent.md` — internal review: Independent verification: one-quality pooling with degree-two pools.
- `notes/review-pooling-degree-two-price-response-second.md` — internal review: Second review: upper-only blending-path price response.
- `notes/review-pooling-degree-two-price-response.md` — internal review: Independent review: an upper-bound blending path with exponential price response.
- `notes/review-pooling-degree-two-vertex-forcing-second.md` — internal review: Second review: degree-two physical vertex forcing.
- `notes/review-pooling-degree-two-vertex-forcing.md` — internal review: Independent review: degree-two physical vertex certificate.
- `notes/review-pooling-existential-reals-1.md` — internal review: Referee report 1: `results/pooling-existential-theory-of-reals.md`.
- `notes/review-pooling-existential-reals-2.md` — internal review: Referee report 2: `results/pooling-existential-theory-of-reals.md`.
- `notes/review-pooling-existential-reals-bounded.md` — internal review: Referee report: Theorem 1′ (bounded data and degrees) in `results/pooling-existential-theory-of-reals.md`.
- `notes/review-pooling-facial-quality-structure.md` — internal review: Independent review: endpoint and facial pooling specifications.
- `notes/review-pooling-feasibility-output-degree-boundary.md` — internal review: Independent review: the output-degree feasibility boundary.
- `notes/review-pooling-fixed-exception-hardness-benders.md` — internal review: Independent audit: strong hardness with five contract exceptions.
- `notes/review-pooling-fixed-exception-hardness-degree-two-agent.md` — internal review: Independent full audit: five-exception pooling hardness.
- `notes/review-pooling-fixed-exception-hardness-refinement.md` — internal review: Audit of the proposed fixed-exception degree-three hardness refinement.
- `notes/review-pooling-fixed-product-contracts-second.md` — internal review: Second audit: exact product contracts remove dense pool balances.
- `notes/review-pooling-fixed-product-contracts.md` — internal review: Independent review: fixed product contracts and unbounded pool feeds.
- `notes/review-pooling-fixed-rank-contract-exceptions-benders.md` — internal review: Independent second audit: fixed affine quality rank.
- `notes/review-pooling-fixed-rank-contract-exceptions-second.md` — internal review: Independent audit: fixed affine rank and bounded contract exceptions.
- `notes/review-pooling-one-pool-bypass-copy-second.md` — internal review: Second independent review: one-pool bypass copy hardness.
- `notes/review-pooling-one-pool-bypass-copy.md` — internal review: Independent review: one-pool bypass-copy hardness.
- `notes/review-pooling-one-pool-existential-reals-A.md` — internal review: Referee report A: `results/pooling-one-pool-bypass-existential-reals.md`.
- `notes/review-pooling-one-pool-existential-reals-B.md` — internal review: Review B: one pool with bypass arcs is ∃R-complete.
- `notes/review-pooling-quality-rank-extension.md` — internal review: Independent review: affine input-quality rank.
- `notes/review-pooling-quality-scaled-path-flow-second.md` — internal review: Independent second audit: quality-scaled path flows.
- `notes/review-pooling-quality-scaled-path-flow.md` — internal review: Independent review: quality-scaled contracted pooling.
- `notes/review-pooling-recirculation.md` — internal review: Independent audit: pooling with recirculation.
- `notes/review-pooling-single-upper-quality-cycles-second.md` — internal review: Second review: copy cycles with one upper quality.
- `notes/review-pooling-single-upper-quality-cycles.md` — internal review: Independent review: scalar upper-quality copy cycles.
- `notes/review-pooling-triviality-second.md` — internal review: Independent audit: profitable flow in acyclic generalized pooling.
- `notes/review-pooling-triviality.md` — internal review: Independent audit: polynomial pooling triviality.
- `notes/review-pooling-two-pools-two-outputs-hardness.md` — internal review: Independent review: two pools and two outputs are enough for hardness.
- `notes/review-pooling-two-pools-two-outputs-second.md` — internal review: Second independent review: two pools and two outputs.
- `notes/review-pooling-two-source-qualities-convex-feasibility-benders.md` — internal review: Independent audit: two source qualities and arbitrary bypass topology.
- `notes/review-pooling-two-source-qualities-convex-feasibility-second.md` — internal review: Independent audit: two source qualities and arbitrary bypass topology.
- `notes/review-pooling-two-source-qualities-source-intervals-independent.md` — internal review: Independent audit: two source qualities with source supply intervals.
- `notes/review-pooling-upper-flow-only-penalty-second.md` — internal review: Second review: eliminating lower flow bounds by a penalty.
- `notes/review-pooling-upper-flow-only-penalty.md` — internal review: Independent review: exact penalty removes lower flow bounds.
- `notes/review-power-flow-existential-reals-A.md` — internal review: Review A: `results/ac-power-flow-existential-reals.md`.
- `notes/review-power-flow-existential-reals-B.md` — internal review: Review B: `results/ac-power-flow-existential-reals.md`.
- `notes/review-power-flow-existential-reals-C.md` — internal review: Review C: corrected Theorem 2 and Section 1 of `results/ac-power-flow-existential-reals.md`.
- `notes/review-rank-one-cost-rank.md` — internal review: Independent audit of fixed interaction-rank optimization.
- `notes/supporting-results-source-closeout.md` — source/priority audit: Closing source checks for two supporting results.

## Computational evidence inventory

Each directory below contains physical-network checks or exact algebra checks associated with the corresponding stage. Source code and retained output are evidence of the tested finite cases, not proof of every parameterized theorem. A fresh run must distinguish exact certificates from floating-point solver comparisons. All files in these directories are listed, including retained outputs that a text search for “pooling” would miss.

### `code/pooling_existential_reals/` (primarily stage 2)

- `code/pooling_existential_reals/bounded_build_and_check.py`
- `code/pooling_existential_reals/build_and_check.py`
- `code/pooling_existential_reals/check_bounded_exact.py`
- `code/pooling_existential_reals/one_pool_build_and_check.py`
### `code/pooling_degree_two/` (primarily stage 3)

- `code/pooling_degree_two/check_degree_three_gadget.py`
- `code/pooling_degree_two/check_degree_three_output.txt`
- `code/pooling_degree_two/independent_check.py`
- `code/pooling_degree_two/independent_check_output.txt`
- `code/pooling_degree_two/irrational_example.py` — exact physical data and completed global optimum proof included in stage 2 at `s2:tiny-irrational`; original docstring's missing throughput denominator corrected in the manuscript, original script unchanged.
- `code/pooling_degree_two/max2sat_output.txt`
- `code/pooling_degree_two/max2sat_reduction.py`
- `code/pooling_degree_two/random_degree_two.py`
- `code/pooling_degree_two/random_degree_two_output.txt`
- `code/pooling_degree_two/random_degree_two_output_seed1.txt`
- `code/pooling_degree_two/verify_output.txt`
- `code/pooling_degree_two/verify_reduction.py`
### `code/pooling_all_degrees_two/` (primarily stage 3)

- `code/pooling_all_degrees_two/check_merged_lax_output.txt`
- `code/pooling_all_degrees_two/check_output.txt`
- `code/pooling_all_degrees_two/check_output_seed1.txt`
- `code/pooling_all_degrees_two/check_reduction.py`
- `code/pooling_all_degrees_two/independent_review.py`
### `code/pooling_two_pools_two_outputs/` (primarily stage 3)

- `code/pooling_two_pools_two_outputs/check_output.txt`
- `code/pooling_two_pools_two_outputs/check_reduction.py`
- `code/pooling_two_pools_two_outputs/independent_review.py`
- `code/pooling_two_pools_two_outputs/independent_review_output.txt`
### `code/pooling_bypass_copy/` (primarily stage 3)

- `code/pooling_bypass_copy/check_constant_data.py`
- `code/pooling_bypass_copy/check_constant_data_arithmetic_review.py`
- `code/pooling_bypass_copy/check_copy_reduction.py`
- `code/pooling_bypass_copy/check_degree_four.py`
- `code/pooling_bypass_copy/check_degree_three.py`
- `code/pooling_bypass_copy/check_fixed_exception_hardness.py`
- `code/pooling_bypass_copy/check_matsui_dyadic_normalization.py`
- `code/pooling_bypass_copy/check_output.txt`
- `code/pooling_bypass_copy/check_structure_mapping_review.py`
- `code/pooling_bypass_copy/check_upper_penalty.py`
- `code/pooling_bypass_copy/check_upper_quality.py`
- `code/pooling_bypass_copy/constant_data_independent_edge_cases.txt`
- `code/pooling_bypass_copy/constant_data_independent_review_output.txt`
- `code/pooling_bypass_copy/constant_data_output.txt`
- `code/pooling_bypass_copy/degree_four_independent_review_output.txt`
- `code/pooling_bypass_copy/degree_four_output.txt`
- `code/pooling_bypass_copy/degree_three_independent_review_output.txt`
- `code/pooling_bypass_copy/degree_three_output.txt`
- `code/pooling_bypass_copy/fixed_exception_hardness_output.txt`
- `code/pooling_bypass_copy/independent_constant_data_review.py`
- `code/pooling_bypass_copy/independent_degree_four_review.py`
- `code/pooling_bypass_copy/independent_degree_three_review.py`
- `code/pooling_bypass_copy/independent_edge_cases_output.txt`
- `code/pooling_bypass_copy/independent_penalty_bound_review.py`
- `code/pooling_bypass_copy/independent_review.py`
- `code/pooling_bypass_copy/independent_review_output.txt`
- `code/pooling_bypass_copy/independent_upper_quality_review.py`
- `code/pooling_bypass_copy/matsui_dyadic_normalization_output.txt`
- `code/pooling_bypass_copy/split_inputs_independent_review_output.txt`
- `code/pooling_bypass_copy/split_inputs_penalty_independent_review_output.txt`
- `code/pooling_bypass_copy/upper_penalty_independent_review_output.txt`
- `code/pooling_bypass_copy/upper_penalty_output.txt`
- `code/pooling_bypass_copy/upper_quality_independent_review_output.txt`
- `code/pooling_bypass_copy/upper_quality_output.txt`
- `code/pooling_bypass_copy/upper_quality_penalty_independent_review_output.txt`
- `code/pooling_bypass_copy/upper_quality_penalty_output.txt`
- `code/pooling_bypass_copy/upper_quality_split_inputs_output.txt`
- `code/pooling_bypass_copy/upper_quality_split_inputs_penalty_output.txt`
### `code/pooling_bypass_paths/` (primarily stage 5)

- `code/pooling_bypass_paths/all_product_contracts_output.txt`
- `code/pooling_bypass_paths/check_all_product_contracts.py`
- `code/pooling_bypass_paths/check_boundary_projection_review.py`
- `code/pooling_bypass_paths/check_box_divergence_support_review.py`
- `code/pooling_bypass_paths/check_box_rank_support_second.py`
- `code/pooling_bypass_paths/check_fixed_product_contracts.py`
- `code/pooling_bypass_paths/check_fixed_rank_chart_algebra.py`
- `code/pooling_bypass_paths/check_fixed_rank_scaled_cuts.py`
- `code/pooling_bypass_paths/check_path_cut_clamps.py`
- `code/pooling_bypass_paths/check_quality_scaled_cuts.py`
- `code/pooling_bypass_paths/check_shadow.py`
- `code/pooling_bypass_paths/check_two_quality_convex_feasibility.py`
- `code/pooling_bypass_paths/check_vertex_forcing.py`
- `code/pooling_bypass_paths/fixed_product_contracts_output.txt`
- `code/pooling_bypass_paths/fixed_rank_scaled_cuts_output.txt`
- `code/pooling_bypass_paths/quality_scaled_cuts_output.txt`
- `code/pooling_bypass_paths/shadow_output.txt`
- `code/pooling_bypass_paths/vertex_forcing_output.txt`
### `code/parametric_path_lp/` (primarily stage 6)

- `code/parametric_path_lp/check_affine_strip_projection_review.py`
- `code/parametric_path_lp/check_rank_one_slab.py`
- `code/parametric_path_lp/exact_diagonal_follower_check.py`
- `code/parametric_path_lp/exact_fixed_alphabet_check.py`
- `code/parametric_path_lp/exact_physical_penalty_check.py`
- `code/parametric_path_lp/exact_rank_one_slab_check.py`
- `code/parametric_path_lp/exact_shadow_check.py`
- `code/parametric_path_lp/exact_strict_local_check.py`
- `code/parametric_path_lp/physical_vertex_forcing_check.py`
- `code/parametric_path_lp/rank_one_slab_output.txt`

### Other supporting code

- `code/common-factor-anchor-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/common-factor-network-positive-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/common-factor-network-simplex-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/common-factor-p-split-balls-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/common-factor-parallel-paths-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/common-factor-verify.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.
- `code/verify-rank-one-costs.py` — related rank-one/common-factor discussion; execute only if used for a substantive new manuscript claim.

## Dependency and completion rules

- Stage 1 supplies homogeneous zero-flow semantics, affine quality compression, compactness conventions, and the physical rank-one identity to all later stages.
- Stage 2 NP membership uses the full fixed-dimensional semialgebraic verifier lemma; never replace it by an unsupported claim that rational pooling data yield rational optimal flows.
- Stage 3 copy circuits depend on exact source/terminal contract logic; removal of these contracts requires its own penalty/completion proof. The five-exception theorem uses final constant-data gadgets, not an unverified abstract circuit substitution.
- Stage 4 uses the fixed-core/block projection theorem for independent blocks. Degree-two path projection is a separate argument with a fixed retained boundary, not a direct consequence of fixed graph degree.
- Stage 5 arbitrary-quality exceptions depend on the detailed fixed-dimensional quality-chart and connected-cut construction in precursor notes. Common-capacity handling depends on the bounded-divergence support theorem and symbolic path minimization. Two quality vectors use a separate convex reduction.
- Stage 6 must distinguish explicit representation lower bounds, isolated-optimum geometry, and NP-hardness. The compact hull of the isolated-optimum example is a material positive result.
- Historical failed arguments remain useful as precise limitations. They must not be promoted into established hardness or tractability claims. Any unresolved claim essential to a selected theorem must either be proved during the writing process or explicitly removed/narrowed and reported.
