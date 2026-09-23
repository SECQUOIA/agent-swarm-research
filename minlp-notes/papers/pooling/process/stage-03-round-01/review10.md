# Stage 3, round 1 — review 10

Reviewed the complete frozen `sections/03-restricted-hardness.tex` (lines 1–1286), with special attention to constant-data binary arithmetic, normalized Matsui coefficients, physical copy composition, two actual feeds, and the threshold compiler. I followed `process/reviewer-protocol.md`, did not edit the manuscript, and did not inspect another report from this review round or use subagents. The reviewed section has SHA-256 `2d8f3082b7fce0a5da15fac5a3f4d20e44bafbe6b3cf209831e25a0c4b7f44a3`.

## Finding 1 — minor: a generator upper bound is attained

**Location:** `sections/03-restricted-hardness.tex:1066`, in the proof of `s3:constant-thm`; compare the correctly non-strict generator bound at lines 630–634.

The displayed chain uses

\[
V_i<u_0+s p^{2n}<3P_4.
\]

Its first strict inequality is false for one of the unrestricted simplex generators used to define these coefficients. Take the generator `w = s e_h` where `h` is the coordinate `s_{nn}`. Then every `r_i` is zero, so `X=0`, while `Y=s p^{2n}`. Consequently the corresponding coefficient is exactly

\[
V_i=u_0+s p^{2n}.
\]

The generator need not lie in the constrained source polytope: these are explicitly the unrestricted generators on which the affine coefficient vector is evaluated. Thus source constraints do not remove this equality case.

**Correction:** replace only the first `<` in that chain by `\le`. The second strict inequality remains valid, and still proves `D_0 V_i < 3p^{8n} < K`. This is a local arithmetic error with no effect on positivity of `b_i`, the dyadic normalization, or either strong NP-completeness theorem. It is not a missing hypothesis or an invalid reduction.

## Checks supporting the remainder of the review

- **Orientation and degree boundary (lines 19–150):** checked the occurrence-splitting implication cycle, saturation of each private weight-two triangle, both subdivision directions, both physical placements of endpoint loads, the local cost lower bound and equality cases, omitted-pool-capacity recovery without an integrality claim, the PARTITION specialization, and elimination of pools with a degree-one side.
- **All degrees two and tolerance (lines 152–340):** checked that cleanup decreases each physical flow and preserves strict flow and dirty intake separately; that mode fixing leaves an integral bipartite flow problem; and that the mode conflict graph, double-subdivision identity, constructive recovery, factor-three transfer, and merged lax constraints agree. Signed mode rewards preserve the same cleanup argument. Integer arc bounds, when present, can be included in each mode's integral edge bound. The positive-tolerance loss is bounded by `2n(eta+delta/eta)` and gives the stated constants after `delta=eta^2`. The displayed K4 flow obeys the shared capacities and has profit `3+2delta`; integral unit flows are zero-tolerance feasible for `delta<1`.
- **Positive-product source (lines 342–417):** checked the active-basis determinant separation, cancellation above the largest fractional index, retained factor `p^(2k-1)`, strict large-parameter bound, concavity extension, product identity, yes-case bound, positivity, and polynomial coefficient lengths. The manuscript's small-parameter counterexample agrees with the report's actual statement. The repaired proof does not rely on the false arbitrary-parameter estimate.
- **Two-pool reduction and FPTAS (lines 419–548):** checked LP preprocessing and the safe cut, affine simplex embedding, cancellation of anchor quality in every row attribute, inactive throughput, the radial extension, threshold equivalence, and tree topology. The FPTAS includes the unconstrained zero grid point, preserves a witness in the selected LP, handles zero optimum, and uses polynomial-length rational LP solutions. Its representation requirement and restriction to this objective family are explicit.
- **Physical copying and penalty (lines 550–959):** checked the four-port equations, distinct port occurrences and source identities, bounded-coefficient homogeneous rows, full and half averaging, padding and singleton rows, separate closed cycles, their summed nonnegative residuals, mixed positive conversion endpoint qualities, full/half coupling, and complement-flow source splitting. The projection-normal proof gives the stated coarse Hoffman constant. Restoring the final copy polytope, repairing primary feasibility radially, and bounding both intake rewards and relocated private-input rewards give the stated exact penalty identity. The zero-intake contracted point used here remains available because these rows are homogeneous.
- **Constant-data arithmetic and exact projection (lines 967–1041):** derived each gate from its physical source equation. Expanding the LSB-first recurrence gives the coefficient `sum_k c_k/2^(L-k)=c/2^L`; every recurrence value remains in the box. Clearing rational denominators has polynomial bit cost. For signed rows, moving negative terms and the signed constant to opposite sides leaves nonnegative partial sums, each strictly below two under the displayed power-of-two scaling. Empty sides use zero. Both extension and recovery work after degree reduction, and a privately supplied designated coordinate port adds no constraint. All required flow and quality values lie in the claimed finite sets.
- **Two feeds, threshold, completion, and five exceptions (lines 1043–1264):** apart from Finding 1, checked the generator normalization, integrality of `b_i`, dyadic `rho_i`, equations for `T,h,ell`, and the quality-mass identity `ell+33h=sum_i a_i x_i`. Only the two conversion sources feed the pool, and their positive endpoint qualities permit the closed-cycle proof even at zero flow. The physically compiled affine threshold excludes zero intake and is equivalent in both directions to the source product test. Completion attains its known upper bound exactly when every positive contract holds, and the common economic offset cancels by total conservation. Slack comparisons and grouped complementary mates impose precisely the original gate equations; splitting supply-four sources is valid. All ordinary output quality bounds are tight before being changed to equalities. Omitting standalone designated coordinate ports leaves exactly the two private conversion fillers, anchor, and two primary outputs as the five possible exceptions.

## Dependencies, sources, and limits

I read the relevant Stage 1 endpoint disjunction and Stage 2 fixed-parameter certificate argument, including the outlet-fraction formulation with arbitrary attribute count. Their hypotheses cover the membership assertions used here. I also compared the arithmetic and construction with `results/pooling-constant-data-two-feed-np-completeness.md`, `notes/pooling-constant-data-two-feed-hardness.md`, `results/pooling-two-pools-two-outputs-hardness.md`, and the weighted extension in `notes/pooling-all-degrees-two-investigation.md`; their status lines were not treated as proof.

I read `literature/AGENTS.md` before the literature. I read the local Matsui METR95-13 text, Sections 2–3, and inspected original PDF pages 3–4 to verify the defective printed estimate and its hypotheses. I read and inspected original pages 25–26 of the Chlebik–Chlebikova author manuscript: the proper edge-three-coloring and preservation of the independent-set gap are explicitly present. I checked the local source passages for Haugland's published Section 6, Haugland–Hendrix Section 4.5, and Baltean-Lugojan–Misener Remark 4.6 against the limited historical claims made here. This was not a new comprehensive priority search.

As supplemental checks, an independently written exact-rational calculation passed 810 signed rational-row cases, including empty rows, with explicit denominator clearing and every intermediate box bound. A separate exact calculation evaluated every simplex generator at `n=5,6,7`; all required normalized coefficient bounds held, and the equality in Finding 1 occurred in each case. These finite checks supplement the symbolic arguments. I did not run a complete Matsui-derived physical network, perform an independent global solver audit, inspect the final typeset PDF, or reprove all external complexity results from their original foundations.

**Verdict: minor findings only.** One local strict-inequality correction is needed; I found no major defect within the scope checked.
