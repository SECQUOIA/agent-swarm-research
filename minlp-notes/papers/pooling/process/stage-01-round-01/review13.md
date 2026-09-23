# Stage 1, round 1 — reviewer 13

Reviewed `papers/pooling/sections/01-foundations.tex` in full. Focus: small counterexamples, degenerate quality data, disconnected support, absent inputs/products, positive lower bounds, and affine rank zero. The substantive findings below follow from direct mathematical checking; no numerical tolerance is involved.

## R13-1 — Major: endpoint formulation needs an upper-only quality hypothesis

**Location:** lines 641–672, especially the asserted equivalence at lines 647–651 and the exact formulation claim at lines 660–669.

The stated conditions are that input qualities belong to `[0,1]` and product **upper** bounds belong to `{0,1}`. They do not exclude lower quality bounds. Lower bounds are explicitly part of the surrounding model, including this subsection's general polyhedral product regions. Under these stated conditions the disjunction does not characterize quality feasibility, even when the product region cuts out a nonempty face.

**Exact counterexample:** There are two inputs of scalar qualities `0` and `1`, one pool, and one product. Include both feeds and the pool outlet, with all upper flow bounds equal to one. Require product quality exactly one, so its lower and upper quality bounds are both one. Its feasible quality region intersects `C=[0,1]` in the face `{1}`. The flow `y_0=1`, `y_1=0`, `v=1` obeys ordinary conservation and capacities. It has `D=0` and `S=0` because no product has upper bound zero. Hence it satisfies every displayed endpoint disjunction and its proposed binary formulation. But its delivered mass is zero and its delivered flow is one, violating the lower specification `m >= t`.

The defect also changes optimization. Give the zero-quality feed cost `-1` and every other arc cost zero. Every physical feasible flow has zero zero-quality feed and therefore cost zero. The proposed formulation has optimum `-1`. This example still works if the product has an exact positive demand of one: the true instance is feasible using the quality-one input, but the proposed formulation chooses the wrong input.

**Correction:** State explicitly that this special case has *only upper product quality specifications*, with no additional lower bounds or cross-quality constraints. Equivalently, allow additional specifications only if they are redundant on the corresponding upper-bound-defined region. The simplest repair is the upper-only restriction. It preserves the given proof, branch count, binary count, and certificate claims. Do not silently convert lower specifications to new attributes while retaining the original value of `K` or the same endpoint hypothesis.

**Severity rationale:** This is a missing essential hypothesis in an asserted exact formulation, with a false feasible flow and wrong optimum under the current statement. It is local to the endpoint specialization; it does not invalidate the preceding general facial theorem.

## R13-2 — Minor: state the effective finite-capacity convention explicitly

**Location:** model lines 49–50; compactness lines 125–127; use of `min` at lines 187–190; universal flow integrality theorem and proof, especially lines 550–567.

The phrase that arc and node totals “may have finite rational lower and upper bounds” can mean optional bounds, including an absence of any effective upper bound. Later claims invoke a bounded feasible set, a finite source upper-bound sum, and an attained optimum. The source result `results/pooling-facial-quality-integrality.md`, Model, states directly that arc and vertex bounds are finite.

If absent effective upper bounds are permitted, a single unrestricted bypass of negative cost and compatible quality has unbounded objective; the universal assertion that every feasible instance has an integral optimal flow then needs qualification. I regard this as a minor convention ambiguity because the manuscript repeatedly indicates that the capacitated model is intended to be bounded, and separately defines its uncapacitated cone.

**Correction:** Add one global sentence that every capacitated instance has finite rational bounds implying a finite bound on every actual arc flow, while the explicitly introduced uncapacitated sets are exceptions. Alternatively state finite effective flow bounds in every optimum theorem. It is unnecessary to require all potentially redundant node and arc bounds to be supplied individually.

## Checks without findings

- At zero pool throughput and zero product delivery, nonnegative incidence flows vanish; arbitrary inactive pool qualities and incompatible zero-demand product qualities therefore cause no hidden quality constraint. Positive lower flow bounds are correctly retained when deleting unavailable arcs or choosing facial branches.
- With no inputs, an acyclic conserved network carries zero flow. With no products, the same is true in an acyclic network; in a cyclic network only pool circulations remain. The manuscript explicitly distinguishes these cases.
- The rank-zero affine reduction is sound: every positive delivered blend has the common input quality, so incompatible products must have delivery zero. Duplicate input qualities and a zero-dimensional input hull do not obstruct face recognition or face enumeration.
- Destination disaggregation uses the **head** multiplier. This preserves all incoming quality masses at a pool by one common factor and leaves the selected product's incoming streams unchanged. Its zero-throughput and disconnected-support cases are valid under zero lower flow bounds.
- The single-product LP equivalence and shortest-path scaling remain valid with node capacities: every component is coordinatewise dominated, and every retained capacity is positive. An empty reachable-input set yields an infeasible normalized mixture LP as stated.
- The conic identity uses only positive scaling into the capacitated set after zero-capacity deletion. The example showing why capacities cannot generally be reimposed after convexification satisfies the listed unit feed/outlet and node bounds.
- In a positive-flow terminal pool strongly connected component having no product exit, conservation excludes external inflow; it is therefore an isolated circulation. The remaining support is absorbed at products. The backward substochastic reconstruction matrix has a deficient row in every nonisolated component and is invertible. These statements survive disconnected circulations and a graph whose original, unused arcs connect the circulation to an input and product.
- The facial theorem's forward and converse proofs handle empty faces, repeated input points, inactive pools, positive lower bounds, and bypasses. A nonfacial region's witness mixture yields a strictly negative objective on forbidden feeds, whereas unit integral throughput must select one allowed input. The bounded-pool enumeration includes `C` and treats `d=0` separately.

## Verdict and limits

**Major findings present:** R13-1. R13-2 is a minor clarification assuming the intended finite-capacity convention.

I checked the entire stage's mathematical arguments, with the cases listed above, and compared the facial source result's model and endpoint specialization. I did not verify bibliographic priority or every cited literature formulation, compile the manuscript, inspect other reports in this review round, or audit later stages. This report is not a claim of exhaustive correctness or external-review acceptance.
