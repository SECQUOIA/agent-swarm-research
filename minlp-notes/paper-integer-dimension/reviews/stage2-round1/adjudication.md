# Stage 2, round 1: root adjudication

All fifteen independent reports are complete. Root read every report in full and checked each concrete finding against the frozen manuscript. All six frozen inputs remained identical throughout review. There are zero reported or accepted major findings and eight reported minor findings, consolidated into five accepted actions. No concrete finding is rejected. Reports without findings are bounded reviews, not proof by consensus.

| Action | Reviewers | Accepted correction | Root judgment |
| --- | --- | --- | --- |
| A1 | 01, 04 | Rename the rotated input interval widths in the finite covariance proof, preserving visible outputs w_j. | The same symbol currently denotes fixed input widths and variable outputs. This is a local notation collision, not a failure of the residual construction. |
| A2 | 02, 05, 10 | Replace “Its variation” in the logdet interior-ball argument by an explicit bound on the objective change. | The gradient norm bound gives absolute objective change at most (8N/delta) sigma <= 1/4. It does not bound gradient variation by 1/4. The existing margin proof needs only the objective bound, so this is a local expository repair. |
| A3 | 07 | Define fresh original-coordinate matrices for the computational grouped gradient. | Grid matrices M_j use the eigenbasis, while the rational-finite algorithm uses the original-coordinate isometric tangent frame. Use Mhat_j=P^(1/2) H_j P^(1/2) in N and its square identity. Orthogonal conjugation preserves every claimed norm, trace and positivity property; no new convergence argument is needed. |
| A4 | 13 | Qualify exact rational certificate evaluation by rational Hessians, tolerances, witnesses, and (for the grouped extension) budget matrices. | With H=2^(1/4), epsilon=2 and P=mu=1,S=0, the feasible real-data residual square is 9-4 sqrt(2), despite rational witnesses. The real certificate inequality and rational-input algorithms remain valid. The computational side assertion needs a local scope qualification. Preserve the original research note and record its inherited omission in the correction log. |
| A5 | 06 | Define E(A)={z:z^T A z<=1} at its first use. | The metric-matrix convention is essential for the scaling and later LDL normalization. Both arguments are correct under this convention; the missing definition is expository. |

## Gate

Corrections are pending a separate correction agent and root inspection. No next stage may begin yet. Since no major issue was accepted, the user’s stage protocol does not require another fifteen-reviewer round after these local corrections. If root inspection exposes a substantive new issue, reopen review. The final whole-paper round will review all corrected material again.

## Final root gate decision

Gate passed. The separate correction agent implemented A1–A5 and stopped editing. Root inspected the entire diff and report, independently verified the relevant counterexamples and frame conjugation, and confirmed a clean up-to-date 41-page build with 125 labels and 22 bibliography entries resolving. All frozen archived sources and accepted dependencies remain intact. The corrected section hash is `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3`. No unresolved accepted issue or new substantive issue remains in this stage. Stage 3 may begin.
