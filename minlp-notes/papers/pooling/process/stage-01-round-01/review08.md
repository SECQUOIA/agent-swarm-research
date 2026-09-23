# Stage 1, round 1 — review 08

## Scope

I independently read all of `sections/01-foundations.tex`, with detailed verification of the facial characterization, its quantifiers, the bounded circulation representation, total unimodularity, recognition LP, face enumeration, and the endpoint formulation. I cross-checked the mathematical arguments against `results/pooling-facial-quality-integrality.md`, `notes/pooling-endpoint-quality-structure.md`, and `results/pooling-triviality-polynomial.md`. I did not read other reviewers' reports or change the manuscript.

## Findings

### R08-1 — Major: endpoint formulation lacks the essential upper-only specification hypothesis

**Location:** `sections/01-foundations.tex:641–672`, especially lines 641–642 (hypotheses), 647–658 (equivalence), and 660–669 (exact MILP and certificate claim).

The general model permits lower quality bounds, and the facial subsection permits arbitrary rational polyhedral product regions. Merely requiring that input attributes lie in `[0,1]` and product **upper** bounds lie in `{0,1}` does not remove lower quality bounds or other quality constraints. Consequently the asserted equivalence and exact formulation are false under the stated hypotheses.

A counterexample survives even an implicit requirement that the product region remain facial. Take scalar input qualities 0 and 1, one pool, and one product with lower and upper quality both 1. Use feed/outlet arcs and unit flow capacities. Here `C=[0,1]` and `F={1}` is a face. The claimed endpoint disjunction has `S=0`, because the product upper bound is 1, and therefore permits one unit from the quality-0 input through the pool to the product. That flow violates the lower quality bound. The asserted exact MILP permits the same invalid flow by choosing `b=0`.

**Correction:** State that this special case has only coordinate upper quality specifications, with all lower quality bounds absent or redundant and no additional cross-quality restrictions. For example: “For the following special case, product regions consist only of coordinate upper bounds in `{0,1}`, and all input attributes lie in `[0,1]`.” Retain lower **flow** bounds, which do not cause this problem. Alternatively extend the disjunctions to lower endpoint constraints, but that requires additional definitions and is unnecessary for the stated source result.

This is a missing essential hypothesis rather than a defect in the disjunctive argument once that hypothesis is supplied.

### R08-2 — Minor: make the global finite-bound convention explicit

**Location:** `sections/01-foundations.tex:49–50`, and the use of boundedness/source upper bounds at lines 529–532 and 553–567.

“May have finite rational lower and upper bounds” can mean that some flow quantities have no upper bound. The facial theorem later asserts a union of **polytopes**, an attained optimum for every rational objective, and a return-arc bound equal to the sum of source upper bounds. These assertions require bounded flow, and that requirement is explicit in the source result but not quite explicit in this stage's global convention. A bypass with unrestricted flow, accepted quality, and negative unit cost would have no attained finite optimum.

**Correction:** State once that each instance has finite rational upper bounds on all arc flows, explicitly given or implied by its finite node capacities; or state finite arc and vertex bounds as the convention except in expressly uncapacitated hull constructions. If source bounds need not be supplied, the return arc can instead be bounded by the sum of finite arc upper bounds. The intended bounded theorem and its integrality argument are sound.

### R08-3 — Minor: the same product-indexed symbol denotes two different kinds of data

**Location:** `sections/01-foundations.tex:42–43` and `51–53`.

`b_j` denotes the vector right-hand side of a product-region inequality and, ten lines later, the scalar exact product demand. This can make a model combining exact flow contracts with polyhedral quality regions ambiguous.

**Correction:** Use a different symbol for the exact demand, such as `d_j`, and write `t_j=d_j`, `m_j=d_j B_j`.

## Verified arguments

- Facial sufficiency correctly applies the face property first at products and then at pools. Compatibility of each positive feed–outlet pair and each bypass is both necessary and sufficient, including empty product faces and zero throughput.
- Fixing a compatible allowed support leaves only ordinary flow constraints. Node splitting and a return arc give an integral bounded circulation formulation when the stated finite integer bounds are enforced. Projection preserves integrality. Lower bounds on excluded arcs must be enforced as zero conflicts; the later algorithm explicitly says this.
- Nonfaciality produces positive mass on an input outside the product region. The one-pool, one-product unit-capacity construction then has a negative-cost fractional feasible flow while every integral feasible flow costs zero. This proves the advertised universal-over-networks converse; it does not prove a per-instance converse or computational hardness, as the manuscript correctly explains.
- The recognition LP characterizes faces without facet enumeration. Its converse works for any segment witness by expanding its endpoints into input mixtures.
- Minimal faces of active pool qualities retain all positive feeds and all used outlets. Fixed-dimensional facet enumeration followed by intersections of at most `d` independent active facet hyperplanes gives polynomially many faces. The fixed `p,d` algorithm and its treatment of arbitrary bypasses are sound.
- I also checked the destination-decomposition head multiplier, single-product reconstruction, cost-sign and relaxation inequalities, shortest-path mixture construction and support bound, conic-hull scaling argument, and the capacitated counterexample. No defect was found in those arguments under their stated bounded acyclic assumptions.
- The cyclic SCC reconstruction, isolated-circulation treatment, absorption-probability decomposition, negative-cycle criterion, and residual counterexample are mathematically consistent with the algebraic steady-state semantics specified in the stage.

## Verdict and limits

**Major findings present:** R08-1 is an essential missing hypothesis in the endpoint formulation. R08-2 and R08-3 are minor precision/exposition repairs.

The mathematical verification covers this stage and the identified source proofs. I did not independently establish publication priority, inspect every cited primary paper, compile the assembled paper, or review later stages. No claim of exhaustive correctness or external-review acceptance is made.
