# Stage 1, round 1 — reviewer 14

## Scope and method

I independently read all of `sections/01-foundations.tex`, the reviewer protocol, and the stage-1 coverage assignments. I compared the manuscript with `results/pooling-triviality-polynomial.md`, `results/pooling-facial-quality-integrality.md`, `notes/pooling-recirculation-investigation.md`, `notes/pooling-endpoint-quality-structure.md`, and `notes/pooling-triviality-investigation.md`. I checked the mathematical arguments directly and did not use historical PASS labels or other current reports as evidence.

## Findings

### 1. Major scope defect: endpoint formulation does not explicitly exclude other quality restrictions

**Location:** `sections/01-foundations.tex:641–672`, especially the hypothesis at lines 641–642 and the claimed equivalence at lines 647–652.

The surrounding subsection explicitly allows rational polyhedral product regions, and the general model permits lower as well as upper quality bounds. The endpoint paragraph only imposes that input values lie in `[0,1]` and that every product **upper** bound is zero or one. Those properties alone do not imply its disjunction, exact MILP, or network-branch conclusions: nontrivial lower quality bounds or additional polyhedral quality inequalities have not been excluded.

For a concrete counterexample, use one input with quality zero, one pool, and one product, unit upper capacities and zero flow lower bounds. Give the product lower quality bound `1/2` and upper quality bound `1`. These data meet the paragraph's stated hypotheses. Sending one unit through the pool satisfies every displayed disjunction (`D=0`, `S=0`) and the proposed network constraints, but violates the lower product quality bound. Thus the asserted equivalence is false for the literal stated class.

The intended upper-only special case is mathematically sound. The earlier endpoint note describes specifications as requiring the minimum contaminant level or imposing no restriction; this intended scope should become an explicit manuscript hypothesis. Because this is an essential hypothesis of an exact formulation, I classify it as major under the review protocol, despite the short repair.

**Proposed correction:** Start the paragraph with: “Now suppose the product quality constraints consist only of coordinate upper bounds, every input attribute lies in `[0,1]`, and every such bound belongs to `{0,1}`.” State that nontrivial lower or additional cross-quality specifications are excluded (redundant lower bounds can remain). Keep lower **flow** bounds allowed, with the existing check when a branch forces an arc to zero. Under this corrected scope, the proof and all following conclusions are valid.

### 2. Minor: dual-cone sentence reverses the positive answer

**Location:** `sections/01-foundations.tex:370–372`.

“The profitable-flow test asks whether `c` belongs to its dual cone” leaves the answer direction contrary to the problem's definition. Membership means that **no** negative-cost flow exists; profitable flow is equivalent to nonmembership. The surrounding theorem is correct and makes the intended relation recoverable, so this is an exposition defect rather than a theorem defect.

**Proposed correction:** “No profitable flow exists exactly when `c` belongs to the dual cone …” or “Profitable flow exists exactly when `c` lies outside the dual cone …”.

## Coverage assessment

I found no material omitted stage-1 development in the assigned source families. The manuscript includes destination decomposition with the correct head multiplier; exact single-product LP projection; both product-count approximation inequalities; shortest-path sign testing, sparse witnesses and bit bounds; the exact uncapacitated cone and the counterexample to imposing capacities afterward; cyclic algebraic semantics, absorption and isolated circulations, exact cyclic single-product reconstruction, the cyclic cone/sign extension and the conditioning example; facial necessity and sufficiency, the recognition LP, bounded-pool/affine-dimension face enumeration, and the endpoint MILP/certificate result. Model, rank-one-block and affine-rank conventions also appear.

The integral convex-hull consequence of the facial union and the positive recognition-LP witness are not separately stated, but both are immediate from proofs already included. I do not regard their absence as a material coverage gap. Omitting a public accusation about the final journal version of the cyclic uniqueness lemma is appropriate: the manuscript preserves the mathematical counterexample and its relevance without asserting an unverified publication defect.

## Substantive checks that passed

- Destination components preserve the same pool quality because the multiplier is applied at the head, and preserve all upper throughputs by coordinatewise domination. Positive lower flow requirements are correctly excluded here.
- Single-product reconstruction and aggregate-quality cancellation are valid, including zero delivery in the acyclic case.
- The `K+1` support argument counts independent quality rows, and rational LP/triangular-system reconstruction provides polynomial bit length. The scaling argument needs only strictly positive retained capacities, as stated.
- The cone proof establishes finite conic hull equality, not merely closure; its polyhedral lift and capacity counterexample are correct.
- Closed terminal positive-support SCCs have no external inflow by conservation. Removing them leaves an absorbing routing chain, while the backward component matrices used for reconstruction are substochastic with escape. The rational-system and compactness arguments are sound.
- Facial compatibility removes nonlinear quality conditions branch by branch. Node splitting retains integer bounds; the nonfacial negative-cost counterexample is valid and has a rational witness.
- Faciality recognition tests representations, not only whether an allowed-input hull intersects the region. Face enumeration using independent active facet normals is valid in fixed affine dimension, including the zero-dimensional case. Positive lower bounds on omitted arcs are explicitly checked.

## Verdict and limits

**Verdict: major findings present**, confined to the missing explicit upper-only hypothesis in the endpoint specialization; one additional minor correction is warranted. After the scope repair, I found no invalid proof in the stage.

This review establishes no priority claim and does not independently audit the cited final journal versions or bibliography metadata. I did not review later manuscript stages, compile the paper, or test algorithms computationally. These limits do not affect the explicit counterexample or the direct proof checks above.
