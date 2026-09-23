# Stage 1, round 1: reviewer 06

Reviewed `sections/01-foundations.tex` in full, with special attention to cyclic SCC decomposition, forward and backward chains, reconstruction, source-free circulations, and conditioning. I did not edit the manuscript or inspect other review reports.

## Findings

### R06-1 — Major as stated: endpoint formulation needs an upper-only quality hypothesis

**Location:** lines 641–672, particularly the scope sentence at lines 641–642 and the equivalence at lines 647–658 (`s1:endpoint-or`).

The model allows ordinary lower and upper quality specifications. The special-case sentence restricts input attributes and product upper bounds, but does not exclude nonredundant lower quality bounds or additional product inequalities. The claimed equivalence and exact MILP therefore omit constraints admitted by the stated hypotheses.

For a concrete example, take one input of quality zero, one pool, and one product; every arc and node has unit upper capacity and zero lower flow bound. Give the product quality interval `[1/2,1]`. Its upper bound is in `{0,1}` and the input quality is in `[0,1]`. All quantities `D` and `S` in the displayed formulation are zero, so its disjunctions permit unit flow. Physical quality feasibility permits only zero delivery. This also satisfies the preceding facial assumption if that is intended to carry over: `C={0}` and `C intersect R` is the empty face. Charging minus one on the outlet makes the proposed MILP optimum differ from the physical optimum.

**Correction:** explicitly require that the only quality specifications are the stated upper bounds (equivalently, any lower bounds are redundant on the input-quality hull). The existing proof then establishes the claimed formulation and certificates. This is an essential hypothesis with a short repair, rather than a problem with the intended upper-only result.

### R06-2 — Minor: define the absorption fractions on removed components and product nodes

**Location:** lines 441–452, cyclic sign and hull proof.

The forward chain and its absorption probabilities are defined on the remaining active pools. The subsequent formula `f^j_uv=f_uv h_j(v)` is applied to the original arc set, which includes removed circulation components and product heads. The acyclic lemma supplies the product convention by analogy, but does not supply values on the removed cyclic classes. The mathematical construction is sound; its definition is incomplete as written.

**Correction:** before applying the formula, set `h_j=0` on the removed classes and all inactive pools, and set `h_j(j')=1[j=j']` at products. Then the equality `f=f^0+sum_j f^j` is literally defined on every arc. The repository's recirculation source note already states the removed-class convention explicitly.

## Verification of the assigned focus

- **SCC classification:** summing conserved nonnegative flows over a pool component equates external inflow and outflow. An SCC with no external inflow is isolated. Likewise, a terminal positive-support SCC with no product outlet is isolated. No nonterminal SCC can feed such an isolated terminal SCC, so removing all the terminal circulation SCCs leaves every remaining active pool with a positive-flow path to a product. This does not rely on paths in the original zero-augmented graph.
- **Backward reconstruction:** row `v` of the normalized internal matrix has entries `f_uv/F_v`, so row deficiency is exactly positive incoming boundary flow. The backward graph reverses the SCC and remains strongly connected. Every state can reach a deficient row; choosing finitely many exit paths gives the uniform finite-step exit probability used in the proof. The geometric-series inverse follows. Boundary coefficients are nonnegative and sum to one: the constant-one boundary problem has constant-one solution by conservation, so the reconstruction is a convex average.
- **Rational bit complexity:** after isolated classes are removed, the full active-pool system is block triangular with nonsingular SCC diagonal blocks. Its coefficients and input-quality right-hand sides have polynomial rational length. Determinant bounds for this one global system establish polynomial rational output length, avoiding an unjustified multiplication of per-component bounds. Rational Gaussian elimination supplies the corresponding polynomial-time construction. No numerical condition-number bound is needed for exact rational arithmetic.
- **Forward decomposition:** absorption gives the harmonic identity for outgoing flow. Using the head multiplier scales every incoming quality contribution to a pool by the same factor, and the harmonic identity equates that scaled incoming total with the component's outgoing total. Product `j` retains its original incoming arc flows and quality mass. The closed circulation part has disjoint active pool support and can be merged into a designated product component without violating mixing or capacities.
- **Sign and hull:** constant qualities realize arbitrary pool circulations; negative cycles can be scaled to every positive retained capacity. In the absence of negative cycles, path-and-cycle decomposition removes only nonnegative-cost circulations, preserves withdrawals and delivery, and gives the shortest-path mixture necessity. Reconstruction handles a cyclic union of chosen paths in the converse. The `J=empty`, `I=empty`, zero-delivery, and isolated-cycle cases are accounted for. Cone scaling requires the stated positive-capacity support and zero lower bounds, both retained here.
- **Compactness:** source-fed active components have source-derived qualities; isolated classes can be assigned zero without changing delivered composition. A common box containing zero and all input qualities therefore preserves every feasible flow projection. With finite flow bounds, the closed bounded lift proves attainment even as supports change.
- **Conditioning example:** direct substitution gives determinant `epsilon`, exact solution `(lambda,lambda)`, and residual `(epsilon,0)` after adding one to both qualities. The manuscript's conclusion is correctly limited to absolute residuals and concentration error.

I also checked the rank-one margin identity, destination LP equivalence, support-size argument, uncapacitated hull equality and capacity counterexample, facial compatibility/integrality proof, nonfacial fractional-optimum construction, LP faciality recognition, and fixed-dimension face enumeration. I found no additional mathematical defect in those arguments under their bounded-flow conventions.

## Sources and limits

Consulted the manuscript, `notes/pooling-recirculation-investigation.md`, `notes/pooling-endpoint-quality-structure.md`, and the locally stored Boland–Kalinowski–Rigterink full text for the cited cyclic-formulation context. I did not use an earlier review's verdict as evidence. I did not perform a comprehensive novelty search, resolve the publication-version history of the cited cyclic uniqueness lemma, review later paper stages, or compile the manuscript. No external-review acceptance is implied.

**Verdict: major findings present**, specifically the omitted upper-only hypothesis in R06-1. The cyclic arguments have no identified major mathematical defect; R06-2 is a local definition repair.
