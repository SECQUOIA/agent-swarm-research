# Stage 2, round 1 — reviewer 13

Primary lens: repository coverage, dependencies, original audits, and consistency across stages.

Major findings: 0

Minor findings: 1

## Snapshot and actual review coverage

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, the stage task and lenses, `PROCESS.md`, `reviews/PROTOCOL.md`, the bibliography and coverage inventory. I rechecked its stage-1 dependencies: graph-containment conventions, affine transformations, compact parity contacts, residual-product formulations, covariance-volume bounds, principal compression, symmetric shrinking, the finite capacity bound, and the rational-rate preview. I had read the entire stage-1 manuscript in its first review round; this review does not claim a new complete audit of every corrected stage-1 proof.

Independently computed SHA-256 hashes match all six frozen entries:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

I compared statements, scope qualifications, and selected proof passages from the thirteen stage-2 canonical results with the manuscript. I read the new covariance-certificate source and root audit, the commuting-covariance source, and relevant original algorithm, body-oracle, input-quotient, block, diagonal, forest, feature, and correction records. These comparisons supplement independent reconstruction of the manuscript arguments; I did not rely on the existing PASS labels.

Primary-source checks used the supplied text cache: IQS Theorem 1.5 and Lemma 5.3; GGOW Theorem 2.18; Zhang–Sra Corollary 8 and its proof; Criscitiello–Boumal Proposition I.1; GLS1981 Definition (5) and Theorem (3.1); and DPV Theorem B.5. I did not independently audit the complete bibliographic history or publication priority, every supporting note, or later-stage mathematics. No literature knowledge-base files were used. I did not compile the PDF or run formulation solvers.

Executed checks found no broken inventory links, undefined citation keys, or undefined cross-reference labels across stages 1–2. All thirteen canonical stage-2 coverage rows point to existing manuscript labels. A content search across `notes/` found no additional directly relevant mathematical/audit omission comparable to the prior round's missing audit records. I also executed the exact one-dimensional symbolic counterexample below; SymPy returned `9 - 4*sqrt(2)` and confirmed that it is not rational.

## Overall assessment

I found no major mathematical defect in the full stage checked. The finite covariance law, rational nc-rank rate, rational finite construction, body and input reductions, structured positive bounds, and hardness arguments fit together coherently. The manuscript now supplies the promised proof of the stage-1 rational-rate preview and preserves the distinct finite-accuracy developments instead of collapsing them into the rank asymptotic. The sole finding concerns a local rationality assertion in the new certificate proposition; its real-valued inequality and the explicitly rational-input construction theorems are unaffected.

## Finding

1. **MINOR — the rational-residual sentence needs rational problem data, not only rational witnesses.** Location: `sections/02-quadratic-finite.tex:143–146`, Proposition `prop:covariance-certificate`; also its grouped extension at lines 682–685. The section permits real Hessians. It states that rational `P, mu, S` make `tr(PRPR)` an exactly computable rational number, but `R=-P^{-1}+2 sum_j mu_j H_j P H_j+S` still depends on the Hessians.

   A counterexample within the proposition's real-data hypotheses is `n=m=1`, `H=2^(1/4)`, `eps=2`, `P=1`, `mu=1`, and `S=0`. The covariance is feasible since `E(P)=sqrt(2)<=4`. All three listed certificate inputs are rational, yet

   ```
   R = -1 + 2 sqrt(2),
   tr(PRPR) = 9 - 4 sqrt(2),
   ```

   which is irrational. For certified evaluation of the entire right side, the tolerance data must also be rational or provided with an adequate certified evaluation model, because they enter `c`. The grouped variant additionally needs rational budget matrices.

   **Type and impact:** missing qualification in a computational side assertion. The mathematical residual identity and determinant-gap inequality remain valid for real data. I rate this minor because adding the qualification restores the intended rational certificate, and the rational construction theorems already assume rational problem data.

   **Suggested repair:** replace the sentence by “For rational Hessians, tolerances, and certificate data `P, mu, S`, the slack and residual square are exactly computable rational numbers; certified scalar logarithm and square-root intervals bound the right side.” Add rational budget matrices when referring to the grouped extension. The same omission occurs in `notes/covariance-determinant-optimality-certificates.md` and is not resolved by its existing root audit; it should be recorded in the manuscript correction log rather than accepted from the source unchanged.

## Coverage and dependency reconciliation

The following is a coverage assessment, not additional findings:

| Source development | Manuscript treatment checked |
| --- | --- |
| Unequal-tolerance covariance determinant law | `thm:finite-covariance` retains explicit `A_n,B_n`, polynomial continuous size, the arbitrary-domain volume term, edge LP reduction, and operator/Frobenius comparison. |
| Rational nc-rank construction | `thm:rational-ncrank` proves rational bases and normalization, exact depth allocation, polynomial coefficient lengths, and the explicit denominator lower bound. The capacity scaling is correctly `D_H^(-2r)`, and zero rank is separated. |
| Rational finite-accuracy construction | `thm:rational-finite` supplies the exact penalty, polynomial metric radius, locally inexact recurrence on stored iterates, normalized gradient accuracy, fresh rounding, exact feasibility repair, and rational grid conversion. |
| Rational matrix functions | `lem:rational-jacobi` gives exact rational orthogonality and reconstruction, off-diagonal contraction, and common-denominator accounting. The later matrix-function bounds require no eigenvalue gap. |
| Correlated/grouped budgets | `thm:grouped-covariance` retains singular and overlapping budgets, shared-error control, direct rational double sums, zero-energy branch detection, and explicit unmeasured directions. |
| Total absolute error | `thm:l1-covariance` retains the PSD Grothendieck factor, normalized correlation optimization, feasible rational correlation repair, and certified upper energy values. The hardness discussion correctly does not claim that a separate-component reduction proves hardness for one total-absolute-error budget. |
| General symmetric error bodies | `thm:general-quadratic-body` retains the effective nonlinear output image, exact equality of minima, strong oracle and radius requirements, removal of the rounding center, and explicit rational output representation. |
| Common nonlinear input rank | `thm:input-quotient` preserves affine terms varying along fibers, the rational zonotope oracle, exact LDL-based normalization, and the domain-volume loss. This parameter remains distinct from nc-rank. |
| Positive blocks and unconditional budgets | `thm:block-psd` and `lem:block-logdet-oracle` retain first-moment positivity, product determinant bounds, block-size and intrinsic block-rank overheads, a direct product-cone algorithm, and the independent convex logdet-oracle route. |
| Diagonal positive Hessians | `cor:diagonal-psd` retains the explicit `5r+1` rational overhead and the separate scalar log-coordinate algorithm. Its original-axis qualification is explicit. |
| Independent integer features | `thm:integer-features` retains the actual minor determinant, row-length loss, primitive-row conversion, overlap allowance, and the requirement that the representation is supplied. |
| Forest Laplacians | `cor:forest-precision` retains the exact normalized volume `2^(-r) product_c n_c`, active-edge removal, isolated vertices, and `6r+1` overhead. It does not silently extend the proof to cyclic features. |
| Hardness | `lem:zero-count-maxcut` and `thm:count-hardness` retain zero recognition, positive-optimum amplification, fixed unit tolerances, general-integer parity, and the power-sublinear scope. They distinguish construction-time count guarantees from solving the resulting MILP. |
| Supporting counterexamples and certificates | The commuting-Hessian reduction and water-filling formula, covariance-benchmark `n log n` gap, thin-domain obstruction, and new residual certificate all have explicit locations. The newly added certificate includes multiplier convexity and the correlated extension, subject to the finding above. |

The original algorithm audits' two concrete corrections are preserved: the selected branch gradient is approximated to `nu/n` before multiplication by `n`, and rational formulation theorems require rational quadratic coefficients, including affine coefficients. The prior unresolved spectral-computation import is now replaced by the complete rational Jacobi argument. The strong-oracle requirement, polynomial separator output length, and known radius assumptions are stated explicitly. In particular, I checked the actual GLS1981 weak-optimization definition: it compares the returned objective with every point of the body, so the manuscript's full-optimum comparison is supported by that cited version.

The additional source and audit for the covariance certificate are both present in the inventory. The audit omissions identified in my stage-1 report are now mapped. I found no further substantive stage-2 coverage omission in this bounded search. Stages 3–4 remain appropriately pending, and their absent proofs are not stage-2 findings.

No manuscript, bibliography, original research, or other reviewer report was edited.
