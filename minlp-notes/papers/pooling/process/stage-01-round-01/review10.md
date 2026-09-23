# Stage 1, round 1 — reviewer 10

## Verdict

**Major findings present:** one essential missing hypothesis in the endpoint-specification special case. The intended upper-bound-only result is valid; the manuscript currently states a broader equivalence that is false. No other mathematical defect was found in the assigned section.

## Finding 1 — explicitly restrict the endpoint case to upper-bound-only specifications

- **Severity:** major (missing essential hypothesis, with a direct counterexample).
- **Location:** `sections/01-foundations.tex`, lines 641–658 (the endpoint case and equivalence), propagated to lines 660–672 (network enumeration, exact MILP, and certificate verification).
- **Issue:** The preceding subsection permits rational polyhedral product regions, while the basic model permits both lower and upper quality bounds. The endpoint paragraph says only that input attributes lie in `[0,1]` and product **upper** bounds lie in `{0,1}`. Neither condition excludes additional lower quality bounds or other product-region rows. The displayed disjunction sees none of those constraints.
- **Counterexample:** Use one input of scalar quality zero, one pool, and one product, with only the two feed/outlet arcs. Set every upper flow bound to one and every lower flow bound to zero. Require product quality in `[1,1]`. This obeys the stated input and upper-quality restrictions; indeed the product intersection with the input hull is empty, which the subsection explicitly counts as a face. The unit feed/outlet flow satisfies conservation and every capacity. Here `D=0` because no input quality is positive, and `S=0` because the product upper bound is one. Thus the claimed disjunction and its MILP accept this unit flow, but its product mass is zero and it violates the lower inequality `t <= m`. If the outlet has cost `-1`, the claimed MILP optimum is `-1` and the physical optimum is zero.
- **Correction:** Begin the special case with an explicit restriction such as: “Assume now that product specifications consist only of coordinatewise upper quality bounds in `{0,1}`, with all input attributes in `[0,1]`; lower quality bounds are absent or redundant, and no additional product-region inequalities are imposed.” Carry this scope into the final NP statement. The existing proof, disjunction, big-M rows, and certificate argument then work without additional mathematical development. If broader endpoint lower bounds are intended, add the symmetric exclusions for lower bounds one and account for their disjunctions; merely preserving arbitrary lower-quality rows would not leave ordinary network branches.

## Independently checked arguments

I read the entire assigned stage, not just the endpoint paragraph, and checked the following directly rather than treating repository review status as evidence:

1. The nonnegative rank-one correspondence, including zero throughput and recovery from matrix margins. Feed/outlet costs induce `C_ij=a_i+b_j`; the manuscript correctly warns that arbitrary matrix costs define a broader model. Bypasses do not change the per-pool correspondence.
2. The destination decomposition uses the head multiplier correctly; incoming quality balances and outgoing flow conservation scale consistently. Coordinatewise domination preserves upper flow capacities, while the zero-lower-bound assumption is essential and stated.
3. Single-product aggregate quality projection, the cost-sign equivalence, the product-count averaging inequalities, and rational reconstruction via a triangular linear system.
4. Shortest-path mixtures, their capacity scaling, and the `K+1` support bound from active-row rank. No sparsity claim about arbitrary pooling feasibility is inferred.
5. The uncapacitated conic-hull identities and the stated example showing failure of reimposing capacities after convexification.
6. The cyclic SCC reconstruction and absorption arguments, including isolated circulations, rational linear-system encoding, and the separate zero-product case. The steady-state circulation semantics are explicit.
7. Facial support compatibility, integral network branches, nonface fractional-improvement construction, recognition LP, and fixed-dimension face enumeration.
8. Under the corrected upper-bound-only scope, the endpoint disjunction is exact: nonnegative zero quality mass excludes every positive-quality feed to a pool serving a strict product. The finite throughput bound controls both sums in the binary formulation. For integer flow bounds an optimal branch vertex is integral and has polynomial encoding; for rational bounds a rational optimal branch vertex gives the corresponding polynomial certificate. A rational objective threshold is checked directly and does not require the threshold row to preserve network integrality.

## Sources and verification limits

I compared the relevant arguments with `results/pooling-facial-quality-integrality.md`, `notes/pooling-endpoint-quality-structure.md`, the model and margin reduction in `results/rank-one-low-rank-costs.md`, and the initial decomposition/projection arguments in `results/pooling-triviality-polynomial.md`. The source endpoint presentation has the same implicit upper-bound-only convention; it should be made explicit in this manuscript because the surrounding model is broader.

I did not inspect any other report in this manuscript review round, edit the manuscript, run a LaTeX build, or conduct a publication-priority audit. No numerical experiment is needed for the counterexample or the support arguments above. Later stages, bibliography completeness, and external acceptance remain outside this review.
