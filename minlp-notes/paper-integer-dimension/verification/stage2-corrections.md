# Stage 2 corrections after round 1

The separate correction agent implemented all five actions in the root adjudication. The manuscript edit is confined to `sections/02-quadratic-finite.tex`. I compared it with the frozen source, inspected the relevant reports, and reread the affected proof passages. No major issue or repair requiring a new theorem arose. This report does not decide the stage gate.

| Action | Implemented correction and mathematical check |
| --- | --- |
| A1 | Renamed all six occurrences of the fixed rotated input width in the finite covariance upper proof to `Delta_i`, including the grid depths, residual scale, and count bound. The visible output remains `w_j`. The later integer-feature widths have their own explicit definition and were left unchanged. Direct references to the grid use its equation label, so no additional width replacement was needed. |
| A2 | Replaced the ambiguous variation sentence by the explicit objective estimate `abs(g(P)-g(P_0)) <= (8N/delta) sigma <= 1/4`. The segment from the center stays in the stated ball, so integrating the independent-coordinate gradient bound gives precisely the estimate needed for the hypograph margin. No gradient-variation assertion remains. |
| A3 | Introduced `Mhat_j=P^(1/2) H_j P^(1/2)` for the original-coordinate isometric tangent frame. Both factors in the double-sum numerator and the square-factorization identity now use this symbol. The explicit conjugation `Mhat_j=U M_j U^T` distinguishes it from the eigenbasis grid matrices and preserves the trace, PSD, and norm claims. |
| A4 | The certificate's exact rational evaluation now assumes rational Hessians, tolerances, and certificate data. It explicitly covers both the slack and residual square. The grouped extension additionally requires rational budget matrices. The real-data inequality is unchanged. The same missing rational-data qualification occurs in `notes/covariance-determinant-optimality-certificates.md` and was not caught by its existing root audit; this inherited omission is recorded here, and the original note and audit were preserved. |
| A5 | Defined `E(A)={z:z^T A z<=1}` at first use. Under this metric convention, multiplying `A` by `beta_d^2=d(d+1)^2` gives the inner ellipsoid, and the later `A=LDL^T` normalization uses the same convention. |

Validation completed:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`, run from the paper directory: exit 0, 41 pages, 559379 bytes. The final log has no warning, overfull, underfull, or undefined-reference messages.
- `python verification/check_manuscript.py`, run from the paper directory: exit 0; 125 labels and 22 bibliography entries, with no duplicate labels/keys or unresolved references/citations.
- `python paper-integer-dimension/verification/check_covariance_certificate.py`, run from the repository root: all 80 cases passed, including 40 exact signed-diagonal stationarity cases and 40 nonoptimal rational covariances.
- `python code/quadratic_rank/check_ellipsoidal_errors.py`, run from the repository root: all 20 exact correlated-budget gradient factorization, shared residual, and fourth-moment cases passed.
- An independent inline SymPy calculation used `P=diag(1/4,1/2)`, the coordinate-swap matrix `U`, and `H=diag(1,0)`. It checked `Mhat=U M U^T` exactly, the corrected normalized gradient `diag(1,0)`, and the prior eigenbasis gradient `diag(0,1)`. A second exact calculation checked that the real-data example has residual square `9-4 sqrt(2)`, which is irrational. These are local algebra checks, not a new general algorithm test.
- SHA-256 comparison confirmed that all six archived frozen inputs still match the round-1 snapshot and that the five live inputs other than the corrected section are unchanged. No original research, bibliography, coverage, main file, macros, accepted stage-1 section, or frozen review artifact was edited.

Final hashes:

| File | SHA-256 |
| --- | --- |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `build/main.pdf` | `b6ea4524b35e7212428b21bf54f24d73f53dbc0398c23b875e4c51874688ab6a` |

The finite checks supplement the surrounding mathematical arguments. I did not conduct a new full-stage review, formal verification, or visual PDF audit. Editing stopped after this report; root inspection remains pending.

Root subsequently inspected the complete patch and this report, confirmed preserved inputs and a clean up-to-date build, and passed the stage gate. See the round adjudication for the final decision.
