# Stage 3, round 1, review 04

Reviewed the entire frozen `sections/03-restricted-hardness.tex`, lines 1–1286, independently, with particular attention to the corrected Matsui source. Read `process/reviewer-protocol.md` and `literature/AGENTS.md`. No manuscript edits were made and no other current reviewer reports were inspected.

## Finding

**R04-1 — Minor: state the bound on the signed summand.** Location: `sections/03-restricted-hardness.tex`, lines 381–382, proof of `s3:matsui`.

The sentence says that each remaining term “has magnitude bounded below by” a negative number. A lower bound on a magnitude is vacuous here and is not the bound used in the subsequent sum. The intended signed bound is correct: for `(i,j) != (k,k)` with both indices at most `k`, one has `i+j <= 2k-1` and `s_ij-r_i r_j >= -1`, so

`p^(i+j)(s_ij-r_i r_j) >= -p^(2k-1)`.

Delete “has magnitude” and write “is bounded below by,” or display the signed bound above. This is a local wording defect; the following inequality and the theorem are supported by the available constraints.

## Focused verification

- **Active vertex denominator, lines 369–375.** A vertex has `N=n+n²` independent active rows even when the polytope is not full dimensional. The coefficient entries and right sides are integral. Hadamard gives denominator at most `N^(N/2)`, so the much coarser reciprocal `h=(n³)^(-n³)` bounds every fractional coordinate away from both endpoints. The argument depends on the number of variables, not an unproved bound on the total number of rows. Arbitrarily many input matrix rows cause no difficulty.
- **Largest fractional index, lines 377–387.** Any binary factor makes its McCormick product exact, including all terms with an index above `k`. The retained diagonal contributes at least `p^(2k)h/2`. All other surviving terms have the signed lower bound stated in R04-1. Therefore `D >= p^(2k-1)(ph/2-n²)`. Here `ph=n^(n³(n-3))`, so the bracket exceeds one for `n>=5`, and `k>=1` gives `D>p`. No factor of `p` is discarded while its multiplier may be negative.
- **No case and concavity, lines 387–390.** In a no instance every vertex has fractional `r`. Since `Y-X²` is a linear function minus the square of a linear function, it is concave in the full `(r,s)` vector. Finite convex decomposition into vertices therefore preserves the strict lower bound `D>p`. The empty-polytope case is separated correctly.
- **Product gap, positivity, and encoding, lines 392–405.** Direct expansion gives `UV-K=(Y-p)²+4p^(4n)(D-p)`. A binary yes point has `D=0` and the displayed square bound makes the product strictly below `K`; a no point makes it strictly above `K`. The lower bound on `V` is positive since `p^n>2n+1`, and `U` is positive directly. Computing the integer powers and expanded coefficients takes polynomial time and `O(n^5 log n)` bits per largest coefficient. Zero-column padding preserves the binary feasibility answer.
- **Report counterexample, lines 408–416.** Read the local Matsui METR95-13 extraction, pages 2–7, and visually checked original PDF pages 3–4 and 6–7. Theorem 2.1 on original page 3 actually states the unrestricted positive-integer-`p` lower bound `p² epsilon/2-pn²`. At `n=5,p=2,epsilon=1/4`, the proposed half-valued point obeys all its hypotheses, with `X=31`, `Y=682`, hence `D=-279`, whereas the printed bound is `-99/2`. The invalid scale-dropping step appears on original page 4. The manuscript correctly confines this observation to the report and independently supplies the required large-parameter argument. An independent exact-arithmetic calculation confirmed these numbers; finite checks of the large-parameter bracket for `n=5,...,19` only supplement the symbolic argument.
- **Downstream factor normalization, lines 630–641 and 1057–1075.** Generator coefficient bounds, the power-of-two choice of `D_0`, positivity of every `b_i`, and the dyadic `rho_i` formulas follow from the source bounds. The normalized factors preserve the product. Large values are encoded in polynomial-size circuits rather than falsely claimed to have constant physical magnitude.

## Remaining stage audit

Checked both directions and physical degrees in the orientation reduction, its private-triangle and subdivision refinements, the two edge-cost realizations, and the stated capacity-removal and Partition specializations. Checked the LP boundary for pools with one inlet or one outlet.

Checked pure-mode cleanup, bipartite matching integrality, the independent-set identity and constructive recovery, merging the lax outputs, the weighted extension, the positive-tolerance cleanup loss and gap transfer, and the explicit nonintegral `K_4` point. Read the Chlebík–Chlebíková author manuscript's Section 5(A), pages 25–26, in the local extraction: it explicitly constructs an edge-three-colored three-regular graph and preserves the independent-set gap, as required here.

Checked the two-pool simplex embedding, enforcement of every linear row at a positive-throughput outlet, maximal radial throughput, both directions of the product threshold equivalence, tree topology, and the represented-family FPTAS. Checked that the invoked Stage 2 certificate statement permits the stated bounded pool/product or bounded pool/attribute parameters, bypasses, exact contracts, and linear arc costs.

Checked the copy and conversion equations, bounded-coefficient rows, full/half averages, separate closed-cycle saturation arguments, and complementary-flow source splitting. Checked the explicit polyhedral error bound through independent active normals and singular values, the polynomial-bit constant, the radial repair after projection, and the exact-penalty objective including the separate private-input reward argument.

Checked binary multiplier order, signed rational-row compilation and intermediate signal bounds, two-feed reconstruction, physical threshold circuit, the fixed quality alphabet, completion objective and economic offsets, and the resulting strong-hardness encoding claim. Checked the five-exception construction's slack equations, grouping of complementary ports, exact collector contracts, and exception count. These proofs distinguish exact threshold attainment from any quantitative approximation or tolerance gap.

## Limits and verdict

This review did not rebuild the manuscript, reprove Stage 2's general certificate theorem, or independently audit every historical attribution in the final scope subsection. The original final journal version of Matsui was not inspected; the verified source was the explicitly cited METR95-13 report. No claim of exhaustive correctness or external-review acceptance is made.

**Verdict: minor findings only.** R04-1 is a wording correction. No major mathematical finding was identified in the stage.
