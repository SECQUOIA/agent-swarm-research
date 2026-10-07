# Stage 3b, round 1: independent review 3

## Verdict

No major issues found. The threshold/XOR endpoint construction and its objective-gap transfer are correct, the composition citations cover partial functions and the specified query models, and the reuse section does not incorrectly multiply movement counts by fresh input costs. Two minor fixes are listed below.

Read both complete new sections, the Stage 3b author record, and the relevant Section 7 interfaces. I did not read other reviewers' reports and made no manuscript edits.

## Findings and exact repairs

1. **Minor normalization slip in the elementary hard-ray proof.** In `sections/09-reuse.tex:117-119`, after setting `M=A/sqrt(8)`, the text says the exact solution is one on the first tree and H on the second. Those are entries of `A^{-1}e`; entries of `M^{-1}e` are sqrt(8) times those values. All normalized-state, condition-number, query and reuse conclusions remain valid, since this is a public common factor. **Repair:** say “The solution A^{-1}e is one ...; M^{-1}e is its public sqrt(8) multiple, with the same normalized state.” Also make “row and column sums” at line 128 “absolute row and column sums” to state the matrix norm bound unambiguously.

2. **Minor indexing clarification for the requested trajectory outputs.** In `sections/08-temporal.tex`, the LP setup declares checkpoints `0<=j<=B` and then defines D_j using eta_{j-1}, without stating that increments have `1<=j<=B`. The SOCP predictor setup and theorem likewise do not explicitly give the index range for “all” P_j/Lambda_j. The later multiplier-span formula indicates the intended range is `1<=j<=B`. **Repair:** add those ranges at the defining equations and say “all B increments” / “all B predictor decrements.” This avoids an undefined eta_{-1} or an unintended collection of all integer-scale diagnostics.

## Threshold, endpoint, and access checks

- The low threshold branch uniquely selects r=t=0 for each fixed z because `2Jr-t>=Jr`; then its positive z coefficient selects z=1. The high branch has `d=phi-c>=1/J`, so r=dz already permits t=z; the remaining objective coefficient is strictly positive and selects z=t=1. The r<=2 cap is inactive at either optimum. Both objective-gap inequalities hold for every feasible point, not just near the optimizer.
- The equality `M_i y_i=z_i e` and linear readout give `q_i=z_i Phi_i` without a product of optimization variables. The readout coefficients, including 1/h, are public. The proof correctly declines to infer a condition bound for the compiled equality system from the old M blocks.
- The four XOR inequalities are precisely the tetrahedral Boolean-XOR hull; they imply all three coordinates lie in [0,1], project onto the whole square of the two inputs, and uniquely determine the output for Boolean inputs. Thus adding them does not alter independent threshold optimization.
- The stated strict relative feasible point satisfies every threshold and XOR inequality strictly. There are 8B+4(B-1) scalar logarithms, so 12B-4 is a valid certified barrier parameter. All auxiliary inverse histories and accumulator variables are uniquely determined at the optimizer.
- The XOR Lipschitz induction is correct: the facets imply both `|p_i-p_{i-1}|<=t_i` and `|p_i-(1-p_{i-1})|<=1-t_i`. Summing the local threshold objective losses proves `|p_B-P*|<=tau/min(theta_i)`.
- The public-rounding correction works: `||tilde b-b||<=Delta/(10R)` perturbs each implicit amplitude by at most Delta/10, so the effective half-gap is 0.9 Delta. A perturbed high amplitude can exceed one, but its `d=tilde Phi-c` remains less than one; the exact same uniqueness/gap argument therefore applies with the new constants. Keeping the old J would indeed not be justified at the old high boundary.
- Full SQ simulation survives all added rows and columns: each old magnitude pattern is input-independent, each new incidence has public magnitude, and readout chains prevent dense columns. New objective and right-hand-side vectors are public. Hidden signs remain individually recoverable from known entries for the coherent upper.
- Equal objective weights give a constant approximate-optimizer gap, while geometric weights require a gap proportional to Gamma^{-B}. The text correctly does not claim that the XOR-coupled barrier retains the separate-block central-path formula.

## Composition and primary-source checks

- `[[brody2023-a-strong-xor-lemma-for]] p.2`: Theorem 1.1 explicitly applies to partial Boolean functions and uses worst-input **expected** randomized query complexity. The cited lower bound is `bar R_epsilon(XOR_B o g^B)=Omega(B bar R_{epsilon/B}(g))`; the matching upper follows by the stated elementary per-block low-error algorithm and a union bound. The manuscript's constant-error conversion to worst-case cost is sound: truncate using the worst-input expected bound, then amplify worst-input success. It does not amplify an average success bias on a single arbitrary input distribution.
- `[[buhrman2007-robust-polynomials-and-quantum-algorithms]] p.3 and p.13`: the coherent subroutine model includes indexed calls and reverses, and Corollary 3 gives O(B) times the one-instance bounded-error quantum query cost for joint Boolean recovery. This supports the endpoint parity upper and the two loose-accuracy trajectory uppers. It does not imply arbitrary real-valued recovery; the manuscript explicitly keeps the stronger numerical outputs separate.
- Quantum parity lower bounds apply after fixing each inner block to two public instances with opposite answers: a source query is then simulable by a constant number of outer selecting-bit queries. The needed classical endpoint product is supplied by the strong XOR theorem, rather than incorrectly inferred from joint recovery alone.
- The elementary random-target direct-sum proof is sound. Under independent filler inputs, the assembled input is independent of the random target block I, so every adaptively selected queried block equals I with probability 1/B on average. Public nonuniform block sampling does not change this. Truncation loses at most 1/12 and leaves 7/12, above the chosen hard-distribution threshold 9/16.

## Trajectory and raw-parity checks

- Checked the LP rho formula, nonnegative telescoping increment kernel and leakage bounds. At Gamma=2^20 the stated decoding margins, 0.21h Boolean representative error and h/100 numerical error are valid. The approximate-centering error uses the full readout norm at most sqrt(BK), and differences of two approximate centers only cost the corresponding constant factor.
- Checked the SOCP radial Hessian, residual under the small relative multiplier update, exact predictor function f, derivative bounds and geometric tails. The 0.075 xi gap at Gamma>=256 and the tighter 0.036 xi midpoint contract at Gamma=2^20 have the advertised slack. The fixed-k positive gap Delta_k is positive because alpha_k=beta_k/2.
- Checked the dynamic norm derivative lower bound and the charged setup-plus-answers interpretation. Supplying exact later iterate norms for free would defeat that lower bound, which is explicitly acknowledged.
- In the raw-parity construction, the literal endpoint carrier is H times a_B, not a sum whose interval could conceal the bits. Both the final-checkpoint 1/32 error and the transition margin 13/16 follow from the rho tail bound at Gamma=256.
- The raw-parity objective gap controls `1-a_B` with the factor `2 Gamma^{-B}`. Equal weights remove the small gap but also the separated scales. The unnormalized final sum is within 1/32 of an integer sum of signs and therefore reveals parity after rounding; normalization by B changes the needed accuracy to order 1/B. Duplicate sign occurrences correctly refer to the same fixed source input.
- None of these final-output arguments requires an algorithm to construct every intervening iterate. The final paragraphs correctly distinguish Boolean-function composition from temporal freshness and from geometric movement.

## Reuse checks

- Verified the augmented KKT equations, their unique solution and common normalized ray; projection onto the x register has probability at least one half. The one-dimensional signed-chain comparator has values 3 and 1, with disjoint relative intervals precisely for error below 1/2; its terminal optimizer coordinate is indeed always one.
- The barrier-gradient norm and the two-affine-factor chord calculation prove the displayed bounded-Dikin movement bound. Pullback through the equality map preserves the reduced barrier metric. This only counts movements under the stated geometric contract.
- Apart from finding 1, the hard-ray matrix has the claimed sparsity, Theta(L) dimension and condition number, a constant-weight parity-measuring leaf subspace, and a valid width-three KKT tree decomposition. Reading its signs once allows all subsequent public scalar rescalings without new source queries.
- Verified exact-span refresh counting, all robust residual acceptance/rejection constants, and the QR-volume proof with normalized approximate columns. The condition in the numerical-width theorem implies the claimed contradiction at 2r refreshes. The stronger l1-stability refinement is correctly tied to exact versions of the already selected checkpoints.
- Verified the holomorphic Chebyshev width bound and both strictly complementary QP counterexamples: the unnormalized predictor coordinates are linearly independent, and the squared normalized coordinate in dimension two has the stated nonremovable pole approaching the real interval.
- The low-rank certification example only supplies coordinate queries; an exact RHS norm would reveal the search bit, as the text notes. The dense-output sign-vector argument correctly combines coordinate rounding, a Hamming-ball bound and the degree-Q state-space dimension from the polynomial query expansion. It proves an explicit-output cost, not a repeated fresh-query cost for an already acquired vector.

## Validation

`/workspace/local-home/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/checks/check_temporal_identities.py` passes the kernel, threshold/XOR, sparse KKT and rank/volume diagnostics. The analytic checks above supply the proof assessment; finite examples alone would not establish the claims.
