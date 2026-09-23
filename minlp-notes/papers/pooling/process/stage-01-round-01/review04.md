# Stage 1, round 1 — reviewer 04

## Scope and method

I read the entire `sections/01-foundations.tex`, independently checked the displayed arguments, and compared the shortest-path and endpoint-specification arguments with `results/pooling-triviality-polynomial.md` and `results/pooling-facial-quality-integrality.md`. My assigned emphasis was the shortest-path sign criterion, the `K+1` witness, signed costs, scaling, zero-capacity deletion, and encoding. I did not inspect other reviewer reports or edit the manuscript.

## Findings

### 1. Major: the endpoint-specification equivalence needs an upper-bound-only hypothesis

**Location:** `sections/01-foundations.tex:641–672`, especially the specification of the special case at lines 641–642 and the claimed equivalence at lines 647–658.

The subsection starts with arbitrary polyhedral product regions and the global model permits lower quality bounds. The special case restricts input qualities and *upper* quality bounds, but does not exclude lower quality bounds or other product-quality inequalities. Under the stated hypotheses, the asserted disjunction is insufficient, and the stated MILP is not exact.

A counterexample even stays inside the preceding facial class. Take two input qualities `0,1`, one pool, one product requiring quality exactly `1` (lower and upper quality bounds both `1`), unit upper bounds everywhere, and zero lower flow bounds. The product region cuts out the face `{1}` of `C=[0,1]`. Send one unit from the quality-zero input through the pool to the product. Here `S=0`, so the displayed disjunction and MILP permit the flow, but its product quality violates the lower bound. Thus merely reading “special case” as a special case of facial regions does not resolve the issue.

**Proposed correction:** explicitly assume that these product specifications consist *only* of coordinatewise upper bounds in `{0,1}`, with no nonredundant lower bounds and no additional quality inequalities. Lower **flow** bounds may remain. This restores the proof as written. Alternatively, separately develop the corresponding endpoint lower-bound disjunctions, but that extension is unnecessary for the present claim.

### 2. Minor: apply the reconstruction lemma after scaling, or explicitly invoke its uncapacitated version

**Location:** `sections/01-foundations.tex:314–318` (shortest-path converse).

The unscaled path mixture need not satisfy the capacities, whereas Lemma `s1:single` is stated for the LP retaining upper capacities. The argument currently calls that lemma before scaling. The mathematical construction is sound because reconstruction does not depend on capacities, but the lemma's hypotheses are not literally met at the invocation.

**Proposed correction:** first scale the routed mixture to satisfy every arc and node capacity, then apply Lemma `s1:single`; or explicitly say that the uncapacitated version of the same reconstruction applies. When giving the scale at lines 327–329, one can specify `min({1} union {U_r/a_r : a_r>0})`, where `a_r` is the unscaled load of a retained capacity row. Zero-load rows impose no restriction.

## Positive verification findings

- Destination disaggregation uses the head's absorption fraction correctly. Incoming pool mass scales uniformly, outgoing component mass agrees by recursion, and all arc and node upper bounds survive coordinatewise domination.
- The single-product projection argument correctly relies on acyclicity (and subsequently on the separate cyclic reconstruction lemma), rather than assuming arbitrary multicommodity flows are physical.
- Negative arc costs do not invalidate shortest paths on a DAG. Every path's cost is at least the minimum path cost for its source and destination, so the forward sign inequality is valid for signed costs.
- Zero arc or node upper capacity forces the associated nonnegative loads to zero. Because this subsection explicitly has zero lower flow bounds and homogeneous quality constraints, deleting that support is safe. Every remaining capacity used by a positive load is strictly positive, making common positive scaling valid.
- A compact feasible mixture LP has an optimal vertex. On its support, the active upper and lower rows for a coordinate are dependent, so their rank is at most `K`; adding normalization gives support at most `K+1`. This argument covers coincident bounds, dependent attributes, and `K=0`.
- Path lengths and rational path costs are polynomially encoded. Rational LP vertices have polynomial encoding by determinant bounds; sums of at most polynomially many rational path weights and the capacity-to-load scaling ratios preserve this property. Reconstruction can be expressed as a polynomial-size rational triangular system, so it also has polynomial-size rational output.
- The uncapacitated conic-hull argument and the counterexample to reimposing capacities after convexification are valid.
- I checked the cyclic SCC reconstruction, source-free circulation case, destination absorption argument, and signed-cycle/path criterion and found no mathematical defect in them under the stated algebraic steady-state semantics.
- I also checked the affine-rank reduction, physical rank-one cost distinction, facial integrality proof and converse, faciality recognition LP, and fixed-dimensional face enumeration without identifying another defect.

## Verdict and limits

**Major findings present:** one missing essential hypothesis in the endpoint-specification statement; the principal shortest-path sign theorem and sparse-witness result are mathematically sound. One local proof-order correction is also recommended.

This is a proof review of the assigned stage, not a complete literature-priority audit or a certification of publication acceptance. I did not check bibliography records against external primary sources, compile the LaTeX, or review later manuscript stages. No computational experiments were needed for the algebraic arguments or the explicit counterexample above.
