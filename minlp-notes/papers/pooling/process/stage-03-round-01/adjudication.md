# Stage 3, round 1: root adjudication

Root read all 15 complete independent reports. Ten report no findings, four report minor findings, and one reports a major finding. The reviewed source is the frozen snapshot with SHA-256 `2d8f3082b7fce0a5da15fac5a3f4d20e44bafbe6b3cf209831e25a0c4b7f44a3`. No later stage has begun.

## Accepted major finding

**M1 — Missing upper-only quality hypothesis in two NP-completeness statements (R15.1).** Accepted as major. Foundations permits arbitrary lower and upper quality specifications. The local-degree and all-four-degree-two theorem statements constrain the upper specifications but do not exclude additional lower quality restrictions. Their hardness constructions use only upper specifications, and their endpoint certificate explicitly requires that scope. Thus the literally stated full-class membership claim is unsupported. This is an essential hypothesis even though the intended reductions need no change. State upper quality restrictions only in both theorem statements and in the introductory certificate scope. Make the intended restriction explicit in the weighted-family statement as well; the tolerance result inherits the corrected all-degree-two family. Do not weaken or alter the accepted foundations.

## Accepted minor findings

**m1 — Physical arc bounds in weighted mode edges (R02, R14, R15.2).** Accepted. A retained mode edge must have capacity equal to the minimum of its pool capacity and its two physical arc bounds, ignoring absent arc bounds. The minimum is integral, so the existing integrality proof applies. This local proof omission does not invalidate the proposition. Reviewer 02 independently checked 48 signed-capacity cases, including separate restrictive arc bounds.

**m2 — Signed summand wording in Matsui proof (R04).** Accepted. Replace the claim about a magnitude being bounded below by a negative number with the actual lower bound on the signed summand. The corrected displayed inequality already uses the valid signed estimate.

**m3 — Attained generator bound (R10).** Accepted. In the constant-data proof, replace `V_i < u_0+s p^{2n}` by `V_i <= u_0+s p^{2n}`. The unrestricted generator for `s_nn` attains equality. The following strict bound below `3P_4` and every required normalization conclusion remain valid.

**m4 — Name threshold decision (R15.3).** Accepted. Both initial NP-completeness statements should say “pooling threshold decision,” since their zero-flow feasibility problem is trivial. This is a statement clarification of the proof's existing objective threshold.

No reported finding was rejected. Other reviewers' no-finding verdicts do not override the specific scope defect. Root independently checked the model/certificate mismatch and the three local mathematical corrections.

## Required next action

A separate repair agent will implement M1 and m1–m4, update the affected coverage descriptions, and record exact changes. After root checks the repair and build, a fresh round of 15 reviewers must review the entire corrected stage. Stage 4 remains pending that round's adjudication.
