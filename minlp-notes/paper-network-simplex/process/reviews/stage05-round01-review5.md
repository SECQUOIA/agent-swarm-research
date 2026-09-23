# Stage 5, round 1 — independent review 5

## Verdict

**No major issues found. One minor terminology inconsistency needs correction.** All three new sections are mathematically sound, including the reduced-profile formulation, five-test oracle, sixteen-circuit classification, and sharp three-versus-four observed-label threshold. The new balance-equation repairs correctly distinguish bypass-flow coefficients from the invariant free product coefficients in the obstruction sections.

## Findings

1. **R5-S05-01 — minor: use “coordinate affine subspace” for the arbitrary-dimensional transfer.** Location: `sections/05-universality.tex`, lines 22–24, Theorem 7.1: “a coordinate plane ... except p observed products.” Section 6.6 explicitly defines a coordinate plane as fixing everything except **two** coordinates, and Lemma 6.7 uses that definition. The transfer theorem has arbitrary `p`, so it generally uses a `p`-dimensional coordinate affine subspace, not the defined coordinate plane. Replace the phrase accordingly; retain “coordinate plane” for the two-coordinate applications of the coefficient-transfer lemma. This is a local terminology correction, not a gap in the construction or its coefficient corollary.

No other necessary correction was identified.

## Universality and coefficient-transfer review

- Checked the imported theorem against the repository's De Loera–Onn full text, including Theorem 1.1, its coordinate-erasing representation definition, the first-layer injection in Section 3.3, and the coefficient-reduction step preserving original coordinates. The first-layer property used here is present in the cited construction. The manuscript also properly credits the pre-existing bitransportation universality and two-commodity interpretation.
- Introducing slack variables gives a bounded standard-form extension because the slacks are affine functions of the bounded original variables. Clearing equation denominators does not scale away the retained variable coordinates.
- Checked the zero-cross-cell padding and corner layer margins: it appends a unique entry of one in every layer and makes all three totals positive without changing the designated old coordinates.
- Checked the four-layer network realization in both directions. Fixing aggregate interior entries gives the two-dimensional margins; the observed boundary products provide the first two layer margins; the third follows by subtraction. Conversely the nonnegative tables supply valid state flows, and each state arc flow is at most its total on this acyclic source–sink network.
- All original coordinates except the designated products are explicitly fixed. Thus this is a genuine coordinate section of the sparse hull, not an unsupported claim that arbitrary facets survive deleting additional original product coordinates.
- The normalization scales all flow and product coordinates together, preserves the slope ratio, and leaves only unit incidence/capacity/balance/simplex data in the original model. Section-fixing constants are correctly distinguished from original model data.
- The two-coordinate local-section lemma applies to the sloping edge after normalization and proves a necessary ratio in every finite original-coordinate description, invariant under adding affine-hull equations. The polynomial-size-in-`log M` construction gives superpolynomial numerical coefficient magnitudes; no superpolynomial bit length, separation hardness, or extension-complexity conclusion is asserted.
- The unit-flow path argument correctly makes these ambient hulls 0/1 polytopes, without falsely asserting that their fractional sections are integral.

## Series–parallel constructions

- Checked every step of the balanced-incidence lemma, including the profile inequality, positive balancing combination, explicit inverse-matrix correction, preservation of total profile mass, and the open-neighborhood estimates. The prescribed neighborhood keeps observed entries strictly below their profiles and permits the one-entry reduction in the selected row. All state arc bounds, bypass entries, aggregates, and observations are satisfied on the claimed half-plane side.
- Recomputed the four-state, seven-observation example and the elementary arbitrary-ratio family, including graph sizes, aggregate coordinates, and coefficient ratio. The smaller example really uses all four observed labels and therefore supports the later sharp label-count threshold.
- Checked the scalar-composition failure: the perturbed gadget can adjust its own profile while preserving its aggregate and observations, but this is incompatible with a common profile across gadgets. The negative result is preserved and correctly delimited.
- Checked the Fibonacci incidence matrix, exact column count and number of ones, balancing weights, homogeneous-kernel proof of invertibility, formula for the sum of the weights, and invertibility of the complement. Both designated cells are observed after taking the complement.
- Checked the graph and observation counts, cycle rank, planarity, width-two decomposition, and encoding length. The model has linear-size lists with logarithmic-size indices and unit numerical data; the Fibonacci weights used in the proof do not become hidden large data in the model. The fixed section coordinates also have logarithmic encoding length.
- Checked the simple maximum-degree-three transformation. Splitting joins and subdividing the second arc of each pair gives `3N` vertices and `4N` arcs, preserves the cycle rank and the observed coordinates, and has unique flow/state-flow extensions. Fixing the newly introduced original flow coordinates preserves exactly the same two-free-product section. The claims do not rely on an unsupported facet-projection principle.

## New reduced-profile and threshold results

**Exact profile system.** The four observation classes give precisely the stated interval of possible aggregate first-arc flows. Nonnegative observed values are an essential precheck and are present. The common profile reconstructs every gadget and the bypass, and zero weights force their complete state flows to zero.

**Residual elimination.** Since the residual state belongs to every `U_i`, eliminating its profile changes both gadget endpoints into positive subset normals. The resulting universe consists of positive subset rows, negative singleton rows, and the one negative full row. The signs and right-hand sides in the residual and endpoint formulas are correct. Zero normals remain separate scalar checks.

**General fixed-state theorem.** Checked the positive-circuit/Farkas characterization, determinant bound on primitive weights, affine branch expansion, and selection of valid cuts. Nonsingular normal-basis enumeration recovers a profile even when its feasible set is lower dimensional. The interval filling procedure then constructs all state flows. The stated arithmetic cost includes the subset-mask handling and does not hide a repeated dense-normal copy per observation. Determinants, inverse-basis candidates, interval filling, and positive-weight normalization have polynomial rational encoding lengths.

**Two explicit states.** The five tests are exactly the feasibility conditions for the two intervals and their sum interval. The explicit feasible-profile choice satisfies all endpoints. The product-occurrence argument is needed in addition to unit circuit weights and is correct. In particular, the negative full row's compulsory bypass coefficient cancels enough of the possible positive-singleton contributions to keep every flow/product coefficient unit.

**Three explicit states.** Independently checked the four circuit forms and their counts `7+5+3+1=16`. The one weight-two circuit doubles only the negative full row, which has no product coordinate. The stated circuit-incidence exclusions prevent repeated same-sign occurrences of any product. The only remaining coefficient exceptions are bypass coefficients `-2` for the singleton partition and `+2` for the three-pair circuit. In the first case the selected upper endpoints come from distinct gadgets; in the second case the selected lower endpoints do. Adding or subtracting one selected gadget balance therefore repairs the bypass coefficient while canceling that gadget's first-arc coefficient and introducing a unit second-arc coefficient. No product coefficient changes, and validity and violation are preserved after the original flow precheck.

Both numerical repair examples are correct, including their exact negative circuit values and separate McCormick feasibility. The four-state obstruction then rules out a unit description, and its product ratio cannot be repaired with affine equations. This establishes the advertised sharp threshold for this flat topology.

**Observed-label reduction.** Merging all globally unobserved labels with the residual is exact on this single-block graph. It changes only simplex-weight expressions, preserves flow/product coefficients, and allows shared normalized default-flow storage with linear additional bookkeeping in the total number of labels. The `a=0` case is correctly separated as `P x Delta_m`; zero merged weight causes no division by zero. No theorem is extended to arbitrary nested series–parallel graphs.

## Independent exact executable evidence

I wrote two scripts in the assigned verification directory without importing author implementation code:

- `check_profile.py` independently enumerates the reduced normal circuits. It confirms normal counts `2,6,11`, circuit counts `1,5,16`, and largest weights `1,1,2` for one, two, and three explicit states. It also reproduces the old full signed-subset counts `1,5,41`. Across all gadget observation patterns for two and three states, **4,336 exact coefficient-bound checks** verify that circuit branch choices cannot create nonunit product or first-arc coefficients. Bypass occurrence checks isolate exactly the two exceptional three-state configurations from the proof. Both repair examples pass exact arithmetic and McCormick checks.
- `check_fibonacci.py` independently constructs the matrices for `q=3,...,12`, verifies invertibility, balancing, complement identities, and observation counts, and constructs full state-flow witnesses from the inverse-matrix formulas. It checks **50 exact feasible witnesses** and **40 exact support obstructions**, through coefficient ratio `F_12=144`. It also independently constructs and checks the counts and maximum degree of ten corresponding simple graphs.

Both scripts passed; their JSON outputs are retained next to them. These finite checks supplement the general proofs and do not test the production separator implementation or implement the imported universality algorithm.

## Source coverage and integration

Compared the new sections with the three relevant result files: `network-simplex-universality.md`, `network-simplex-series-parallel-coefficient-growth.md`, and `network-simplex-flat-chain-fixed-states.md`, plus the direct universality source cited above. The substantive constructions, coefficient conclusions, small and dense precursors, sparse complement improvement, simple-graph extension, fixed-state profile formulation, determinant argument, and negative scalar-composition result are represented. The reduced-profile oracle and sharp three-state threshold genuinely strengthen the old 41-circuit/two-explicit-state presentation; they do not merely relabel it.

One optional source-coverage addition for final integration would be a short statement that for integral network balances and capacities, restricting the original arc flows to integers before convexification gives the same hull, by network integrality and simplex-vertex disaggregation. The universality source notes this broader classical observation. The present 0/1 claims are already correct and sufficient for all new obstructions, so I do not classify the omission as a mathematical defect.

## Build, presentation, and limitations

The private snapshot build produced a **38-page PDF** with no final LaTeX warnings, unresolved references/citations, or overfull/underfull boxes. Visually inspected pages **26 and 36**, covering the universality transfer and the delicate three-state repairs. Displays and prose are legible and remain within the margins. The new proofs explain the distinction between observed-state information, total flow, and invariant product coefficients sufficiently for readers.

This review does not establish literature priority, audit all bibliography metadata against publishers, or validate future benchmark claims. It reviews the imported theorem's stated scope and coordinate injection but does not reproduce its full deep construction. I did not read other current-round reports, coordinate findings, spawn agents, edit manuscript sources, or build in the shared snapshot.
