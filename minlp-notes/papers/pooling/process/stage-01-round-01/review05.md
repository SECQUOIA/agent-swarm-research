# Stage 1, round 1 — reviewer 05

Focus: conic/convex hulls, closure, finite formulations, homogeneous versus bounded hulls, and counterexamples. I reviewed the entire stage independently and did not read other reviewer reports.

## Findings

### R05-1 — Major: endpoint formulation omits the upper-bound-only hypothesis

**Location:** `sections/01-foundations.tex`, lines 641–670, especially the hypotheses at 641–642 and the equivalence at 647–658.

The general model permits lower quality specifications, and this subsection has expressly returned to rational polyhedral product specifications. Merely requiring all input qualities to lie in `[0,1]` and all product *upper* bounds to lie in `{0,1}` does not exclude a nontrivial lower quality bound. The displayed disjunction and MILP ignore such bounds, so the asserted equivalence is false under the stated hypotheses. This remains a defect even if the paragraph is read as inheriting the faciality hypothesis.

**Counterexample:** use two inputs of qualities 0 and 1, one pool, one product with exact quality 1 (lower and upper specification both 1), all feed/outlet/node upper bounds 1, and zero lower flow bounds. Its allowed quality set `{1}` is a face of `[0,1]`. Send one unit from the quality-0 input through the pool to the product. For the sole pool/quality pair, `D=0` and `S=0` (there are no products with upper bound zero). Hence the support disjunction and stated MILP admit this flow, yet the product's lower specification is violated. Assigning negative cost to the quality-0 feed also makes the omitted condition change the optimum.

**Proposed repair:** state explicitly that this special case has *only coordinatewise upper quality specifications*, or that every lower bound is redundant on `[0,1]`, and no additional polyhedral quality constraints. This is a short but essential hypothesis repair; the existing proof is valid for that class. If lower endpoint restrictions are intended too, they require separate complementary disjunctions and an updated count.

## Positive verification of the assigned focus

- Checked the destination decomposition head multiplier, domination under node and arc capacities, source/product balance, and the unchanged quality at the selected destination.
- Checked both directions of single-product projection, including zero flow, and the sign/approximation directions for negative costs.
- Checked every containment in `conv(S)=cone(S)=sum_j C_j=cone(P)`: zero and scaling closure yield `conv(S)=cone(S)` without a closure operation; positive remaining capacities justify scaling each finite flow into `P`; nonnegative capacities plus zero lower bounds are essential and are present in the subsection.
- Checked polynomial formulation size: one arc-flow copy per destination and its quality rows gives polynomial size even when the quality dimension is part of the input. A projection of this polyhedral cone is polyhedral, so the claimed closedness does not assume that a general conic hull is closed.
- Checked the bounded-hull counterexample at lines 374–381. A common active pool cannot deliver positive flow to both incompatible exact-quality products; each remaining product capacity is one, so total delivery is at most one in `conv(P)`. The two-unit pure-flow sum satisfies every stated capacity and belongs to `conv(S)` (equivalently, average twice each pure flow). Thus the counterexample establishes precisely the claimed strict distinction.
- Checked cyclic reconstruction through positive-support SCCs, deficient backward transition rows, and the separation of isolated circulations. Terminal SCCs without product outlets have no external incoming flow by conservation. Removing them leaves an absorbing product-reaching support. The cyclic hull proof and negative-cycle alternative are sound under the explicitly stated algebraic steady-state interpretation.
- Checked why adding the input/zero quality box preserves every cyclic flow projection and provides compactness when flow bounds are finite: all externally fed components have source-derived qualities, while the isolated components may use zero.
- Checked the faciality sufficiency/converse, the rational recognition LP, and the fixed-dimensional face enumeration argument. No additional defect was found in these arguments.

## Sources checked

Read the full manuscript stage and the local source proofs in `results/pooling-triviality-polynomial.md` and `results/pooling-facial-quality-integrality.md`. Their status labels were not treated as proof evidence. The endpoint source itself likewise leaves the upper-only convention implicit; the manuscript's broader explicit model makes stating that restriction necessary.

## Verdict and limits

**Major findings present:** R05-1 is an essential missing hypothesis with an explicit counterexample. No hull or cyclic proof defect was found.

This is a mathematical review of this stage and the listed local source proofs. I did not independently verify external literature priority, the bibliography against publisher records, later stages, or compilation. The review does not establish exhaustive correctness or guarantee external acceptance.
