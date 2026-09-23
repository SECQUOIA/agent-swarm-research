# Stage 3, round 1: independent review 4

Verdict: **0 major findings, 0 minor findings.** No repair is required for the frozen LP application section.

I read all of `sections/06-lp-application.tex`, the September 4 sparse-LP source note, and `audit/stage3-author.md`. I checked the relevant primary references and the earlier mathematical results used in the transfer. I did not inspect peer reports or edit the manuscript. A full introduction is outside this review stage.

## LP geometry and predictor

The orthonormal basis construction is valid under the stated small-delta assumptions. The factor has singular values 1 and sqrt(t), and its nullspace is spanned by the public vector q_0. Orthogonality to the strictly positive q_+ proves that q_0 has both signs, so the feasible line intersects the orthant in a compact, nontrivial segment. The objective derivative along this segment is cos(theta)/sqrt(3)>0.

The primal and dual feasibility conventions are consistent with exact centrality at x=s=1, y=0, mu=1. Eliminating the predictor equations gives H_t*Delta y=A_t*1 with the displayed positive sign. Both the explicit dual direction and the public primal direction follow. The squared support overlap is (8/9)(1+delta), which stays in (0,1) under delta<1/8 and is bounded away from zero.

The text correctly explains that the LP feasible set and primal predictor do not depend on t. The lower bound is for the normalized dual direction in this representation, not for obtaining useful primal progress or solving the LP.

## Oracle scope and state bounds

The complete normal, factor, and RHS unitaries are specified. The factor completion is unitary on the row/column singular-vector pairs and has the stated action on the column null vector. Its rectangular compression and output space are unambiguous. Public padding adds no hidden parameter information.

The contract withholds the numerical entries, hidden parameter, and exact RHS norm. This last exclusion is necessary: the displayed norm would reveal t. Counted access to B_t and its inverse remains available in both state models, and its endpoint operator distance is O(delta), so it does not invalidate either hybrid bound.

The endpoint target trace distance and all three endpoint oracle estimates are correct. The hybrid argument applies to bounded-query adaptive algorithms after purification, including coherent query-type choices and discarded registers. It establishes the claimed total-query lower bounds with RHS calls included.

The amplitude-estimation constructions have success probabilities t^2 and t, respectively. The clipping inequalities give the stated additive O(delta) parameter error with O(delta^(-1)) normal queries or O(delta^(-1/2)) factor queries. A fixed number of repetitions suffices at fixed epsilon_0. The derivative of the target-state angle is bounded by 1/(4delta), and convexity of trace distance includes all bad estimation outcomes in the unconditional output density operator. No favorable-event conditioning or uncounted reflection about an unknown prepared state is used.

## Compiler transfer and bypasses

Replacing the varying normal-oracle sector by the periodic sine family gives a bounded trigonometric polynomial for every designated output entry, even when circuit gates mix eigenspaces. The low-interval lower bounds therefore transfer. Excluding B_t from the compiler contract is explicit and avoids an unsupported polynomial-degree induction for its entries.

The public fixed projectors do yield the zero-query coarse tier at K>=G_0. All positive tiers, threshold equalities, and the stated joint law follow from the earlier low-continuum lower bounds and singleton-high-band upper constructions. The hidden continuum remains essential to exact impossibility; the known-t exceptions are correctly explained.

The factor bypass is valid with two queries and normalization one. The row-space version of the even polynomial 1-s^2 gives I_R-A_t*A_t^T; the column nullspace does not contribute an extra output eigenvalue. The independent public-projector compression identity verifies the same construction directly. Neither formulation claims two-query optimality.

The exact-entry formulas reveal t, and finite digital precision can provide the fixed-error state estimate with a constant number of value queries when bit and arithmetic costs are treated separately. The normalization-two LCU shortcut is also valid. These are appropriately identified as changes to the input or output contract, not exceptions to the stated analog-query theorems.

## Attribution and interpretation

[BHMT Theorem 12](https://arxiv.org/pdf/quant-ph/0005055) gives the quoted amplitude-estimation error and success probability. Its counted uses of the preparation and inverse support both upper bounds.

[Orsucci–Dunjko, Sections 1.4, 4.3, and 5.4–5.5](https://quantum-journal.org/papers/q-2021-11-08-573/pdf/) support the attributed factor improvement, support-overlap caveat, normalized-complement requirement, and specialized digital construction for diagonally dominant matrices. The manuscript does not present those generic ideas as new. In particular, it uses its own direct estimation proof for the sharper fixed-error orders instead of claiming an overlap-free generic solver theorem.

[Gilyén et al., Corollary 18](https://arxiv.org/pdf/1806.01838) supports the real even singular-value transformation, with the left-space application obtained by reversing the input/output projectors. The projector construction independently removes any ambiguity about that orientation.

The contribution statement is limited to the explicit central LP realization, the specified state-access comparison, and the compiler transfer with its coarse-tier correction. The section clearly excludes unconditional sparse-input, full LP-solver, and end-to-end QIPM lower bounds. I found no claim exceeding the proved oracle results.

## Independent numerical check

Using the qipm interpreter, I evaluated both endpoints for rho in {1.01,2,5,20} and delta in {10^(-3)/rho,10^(-5)/rho,10^(-7)/rho}: 24 instances. I checked the normal equation, predictor feasibility, public primal-direction formula, both full-oracle unitarities, RHS norm, support overlap, projector-compression complement, endpoint state distance, and all endpoint oracle inequalities. The maximum identity residual was approximately 1.44e-15; all endpoint inequalities passed. This was a floating-point diagnostic in addition to the analytic review, not a proof certificate. No manuscript artifact was changed.

Required repairs: none.

Counts: **0 major, 0 minor**.
