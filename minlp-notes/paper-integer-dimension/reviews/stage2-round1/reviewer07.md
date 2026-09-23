# Stage 2 round 1 — reviewer 07

Primary lens: grouped PSD budgets, the total-absolute-error SDP, normalized gradients, weak optimization, and exact rational repair.

Major findings: 0
Minor findings: 1

I found no major mathematical defect in the full stage. The grouped and total-absolute-error covariance laws, their dimension-independent constants, and their rational oracle reductions withstand the checks below. One gradient formula needs an explicit change of notation or basis to agree with the algorithm it invokes. This assessment is not formal verification or a publication-priority judgment.

## Snapshot and coverage

All six SHA-256 hashes matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I read the stage task, lenses, process and protocol, the entire 1,546-line stage-2 section, bibliography, and coverage inventory. I rechecked the relevant stage-1 definitions, parity and closure mechanism, shared residual products, principal compression, symmetric shrinking, covariance lemma, capacity bound, and rational-rate preview. The whole earlier stage was also read in my stage-1 review; this round focuses on its current dependencies.

I independently reconstructed the full stage's mathematical chain: finite covariance bounds and constants; geodesic convexity and determinant certificate; commuting reduction; rational rank construction and capacity scaling; Jacobi contraction and matrix-function error bounds; inexact projected recurrence and rational repair; grouped and total-absolute-error budgets; effective output image and input quotient; logdet allocation oracle; PSD block, diagonal, integer-feature, and forest refinements; domain obstruction; and Max-Cut amplification. Every stage-2 canonical and substantive supporting row has an identifiable location in the section. I did not independently compare every one of those rows against its complete original source file.

For deeper source comparison I read the full original grouped-budget and total-absolute-error results, the block-logdet oracle note, and the relevant rational-geodesic-construction sections. I checked primary-source text directly for GLS1981 Definition (5) and Theorem (3.1), IQS Theorem 1.5 and Lemma 5.3, Zhang–Sra Corollary 8 and its proof, Criscitiello–Boumal Proposition I.1 and metric convention, DPV Theorem B.5, and GGOW's integral capacity theorem (also checked in the preceding review). The [Briët–de Oliveira Filho–Vallentin primary record](https://arxiv.org/abs/0910.5765) confirms the cited metadata and the classical PSD approximation ratio; I checked the manuscript's short Gaussian-sign proof directly rather than relying on its attribution alone.

I did not compile or inspect the PDF, implement the complete geodesic or GLS algorithm, recheck every bibliography entry, or conduct a comprehensive novelty search. Existing audit labels were not used as mathematical evidence.

## Finding

1. **MINOR — grouped-gradient formula changes coordinate frames without saying so.** Location: `sections/02-quadratic-finite.tex`, lines 648–650 and 661–678, proof of `thm:grouped-covariance`, compared with the tangent convention at lines 470–475 and the update at lines 501–508.

   Line 650 defines `M_j = diag(sqrt(lambda)) U^T H_j U diag(sqrt(lambda))`, the scaled Hessian in the eigenbasis of `P`. Lines 665–667 then call `N_l(P)/E_l(P)`, formed from those same `M_j`, the half-log gradient, and invoke the original-coordinate algorithm unchanged. In that algorithm's isometric tangent frame the scaled Hessian is instead `P^(1/2) H_j P^(1/2)`. The displayed numerator is conjugate to the required one by `U`, rather than literally equal to it.

   A concrete check takes `P=diag(1/4,1/2)`, the coordinate-swap matrix `U`, ordered eigenvalues `(1/2,1/4)`, `H=diag(1,0)`, and one group `W=[1]`. The line-650 matrices give normalized gradient `diag(0,1)`. The actual gradient of `(1/2) log E(P)=log P_11` in the frame used by the update is `diag(1,0)`. Thus the omitted convention matters to a direct implementation, although the positivity, trace, and norm statements remain invariant.

   **Repair:** At the start of the computational paragraph, reset `M_j=P^(1/2)H_jP^(1/2)`, preferably using a fresh symbol to distinguish it from the grid matrices. The original `results/quadratic-ellipsoidal-output-precision.md` explicitly makes this reset. Alternatively, state that the displayed gradient is in the `U` basis and use `U N_l(P) U^T/E_l(P)` in the existing update. This is a local notation/frame defect with an immediate repair, not a false grouped-covariance theorem or a missing convergence argument.

## Verification details

The grouped fourth-moment argument legitimately sums nonnegative discarded terms after a conceptual PSD factorization. It requires no rational factorization in the algorithm. The shared symmetric residual matrix yields the claimed whole-budget error `E_l(P)/64`; controlling outputs separately would not suffice, but that is not what this proof does. An identically zero measured energy is detected exactly by `E_l(I)=0`, and the common monomial representation cancels its quadratic part exactly.

The total-absolute-error lower proof has the correct factors: the sign-combination covariance energies are at most `16 epsilon^2`, and the PSD Grothendieck factor makes the SDP value at most `8 pi epsilon^2 < 36 epsilon^2`. The upper proof maximizes the common residual estimate over signs and therefore controls the full l1 norm.

GLS1981 Definition (5), printed page 172, gives distance at most `rho` to the actual body and additive objective loss at most `rho` against its full optimum, precisely the interface used here. The correlation body has the required rational interior and outer balls. A point within `rho` gives minimum matrix eigenvalue at least `-sqrt(2) rho`; adding `2 rho I` and renormalizing the diagonal is consequently an exact rational feasibility repair. With `rho=nu/[4(m+1)]`, its objective loss is smaller than `nu tr Gamma`, so both the certified upper value and the near-active logarithmic branch are valid. The positive lower bound on the repaired value also controls the normalized gradient denominator.

The block-logdet hypograph has a valid explicit interior ball, and its rational tangent separators use only approximate scalar logarithms with a safe upper offset. The central-ball repair is an exact convex-combination argument, not an assumption that a weakly feasible point is feasible. Its determinant loss and polynomial precision dependence check out. The block and quotient constructions retain the domain-volume losses needed for the stated overheads.

The rational nc-rank proof now discharges the stage-1 preview: its bases have polynomial height from the imported IQS interface and rational elimination; capacity scales by the essential power `D_H^(-2r)`; and the rational box slice has the stated denominator-based volume lower bound. The finite algorithm's recurrence accounts for error at each stored iterate, avoiding an unsupported long-run exact-trajectory approximation.

Executed checks, after inspecting the scripts:

- `python code/quadratic_rank/check_ellipsoidal_errors.py`: passed 20 exact correlated-budget factorization, shared-error, and fourth-moment cases.
- `python code/quadratic_rank/check_l1_errors.py`: passed 24 exact shared l1 error cases and 30 rational correlation feasibility/upper-bound repairs.
- An independent inline SymPy check verified the coordinate-frame example in finding 1 and the exact conjugation repair.

These finite checks supplement the general proofs; they do not implement or validate the imported optimization algorithms. No manuscript, bibliography, original research, or other review report was changed.
