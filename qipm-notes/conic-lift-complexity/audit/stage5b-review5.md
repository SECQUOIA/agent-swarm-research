# Independent Stage 5B review 5

Reviewed all of `12a-resource-ledgers.tex`, `12b-work-contracts.tex`, `12c-newton-comparisons.tex`, `12d-query-output.tex`, and `12e-active-compilers.tex` end to end, with the relevant rank, compression, barrier, and movement dependencies. No manuscript edits were made. No other Stage 5B review, author report, or root check report was consulted.

**Assessment:** I found no valid major mathematical error in these five sections. The distinction between geometric resources, movement, charged work, query access, and output is maintained consistently. I found one nonblocking completeness issue against a directly relevant repository source. It does not invalidate an existing theorem.

## Finding 1: The dynamic scale-maintenance result is absent from the access discussion

**Severity:** Minor completeness/scope issue; not a correctness error. If this theorem has deliberately been deferred to another stage, an explicit disposition is sufficient.

**Location:** `sections/12c-newton-comparisons.tex:373–388`, especially the one-snapshot noncomposition discussion at lines 379–388; related discussion at `sections/12b-work-contracts.tex:193–208`.

**Repository source:** `notes/workbench/active/2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md`, result statement and Sections 1–4, including Section 2.1.

The manuscript includes the static radial-scale lower bound, the distinction between a compiled interface and one online evaluation, the exact scale-update identity, and the warning against multiplying a static query lower bound by an iteration count. The source also proves the positive theorem specifying when a temporal direct sum is justified. That theorem is missing here.

For $T$ fresh independent batches on $b$ sources of dimension $s$, a service that commits all scales after each batch, with relative error below $1/3$ and joint success at least $2/3$, can require $\Theta(Tb\sqrt{s})$ quantum or $\Theta(Tbs)$ randomized queries. Each update can be zero or one-sparse under hidden-support coordinate access. The source also gives the replicated-block margin version and the universal-service tradeoff

\[
 Q=\Theta\!\left(\sqrt{s}\sum_t\min\{r_t,b\}\right),\qquad
 R=\Theta\!\left(s\sum_t\min\{r_t,b\}\right).
\]

This is directly relevant to the section's access boundary: the text currently states the missing premise but does not present the repository's example satisfying it. The proof is the same tensor-sum star adversary already used in the static proposition, now indexed by epoch and source. The hard trajectory resets to the same public base between fresh updates; it is not asserted to be the Newton trajectory of a fixed program.

**Proposed correction:** Add a short proposition after the static discussion, or explicitly defer it. Preserve its precise output contract: classical committed scale records, or a reusable source-independent value interface whose values can be read without consuming its backing workspace. Require fresh independent update data and joint correctness. State that explicit sparse-list updates are easy by the displayed scale identity, that one raw-oracle-backed coherent evaluation has no factor $b$, and that this result gives no generic lower bound for a fixed-instance QIPM trajectory. The general invocation tradeoff can be deferred if space is limited; the basic fresh-batch theorem would close the immediate presentation gap.

## Independent mathematical checks

- **Resource ledgers:** Rechecked the total-order concentration argument, the residual order formula, $F_4,F_5$, grouped Schur counts, packing counts, free-coordinate optimum, nullity envelope, Hölder constant and exponent range, and width-four optimum. An independent dynamic program checked $V_R(N)$ for $2\leq R\leq30$, $1\leq N\leq500$, and $F_4,F_5$ through $N=500$. Exhaustive nullity enumeration checked $2\leq R\leq7$, $1\leq L\leq4$, and every budget in those ranges. All passed.
- **Work composition:** Rechecked that the curvature rank is the aggregate certificate rank used in the exposed-minor distance theorem. The fresh-charge premise is explicit and necessary. The packed path, residual scale, central speed, output reconstruction, and fixed-sign state reuse argument agree with the stated models.
- **Sharp off-center theorem:** Independently derived the residual Hessian and its constrained minimum. With $E(\theta)=\sum_a\theta_aE_a$, positivity of $E(\theta)DE(\theta)$, commutation of $D^0$ and $E(\theta)$, and exact source allocations give
  \[
  \mu M_0\preceq M(D)\preceq LM_0.
  \]
  This is valid even for indefinite $E(\theta)$. Inversion gives the claimed first-power Hessian transfer. The eliminated gradient also checks. The two-column example simultaneously attains both relative eigenvalue endpoints and the condition factor. The inexact-allocation corollary uses the correct weakened bounds. I additionally checked 500 randomly generated strictly feasible instances with heterogeneous source multiplicities and correlated residuals; both the allocation-Gram and quotient inequalities passed.
- **Sparse Newton systems:** Rechecked the one-hub and two-hub identities, positive downdated base, regularization estimate, graph counts, stated treewidth witnesses, and CGLS residual estimate. The separation of exact field operations from square-root arithmetic and numerical stability is appropriate.
- **Query/output reductions:** Rechecked the sign-recovery entropy argument, central-point formulas, precision rescalings, checkpoint constants, all-sign decoding thresholds, independent-search adversaries, scaled Hessian condition bound, and packed-barrier distance estimates. The distinction between an optimum value and a solution observable is retained.
- **Active compilers:** Rechecked essential-constraint witnesses, neighboring-factor contacts, fixed-objective decoding spacing, barrier parameters and lengths, entropy aggregation including the perspective boundary, and matched-gap metric lengths. The exact reusable output requirement is strong enough for the decoding lower bounds and is stated explicitly.

## Attribution checks

The following primary references support the uses checked here:

- [Brassard–Høyer–Mosca–Tapp, *Quantum Amplitude Amplification and Estimation*](https://arxiv.org/pdf/quant-ph/0005055), Theorems 4 and 16: known-success exact amplification and exact zero-versus-known-cardinality search. The cited theorem numbers are correct.
- [Ambainis–Childs–Le Gall–Tani, *The Quantum Query Complexity of Certification*](https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf), Theorems 3–4: finite-output spectral adversary and its direct sum. These support the marked-position argument.
- [Fürer–Hoppen–Trevisan, *Fast Gaussian Elimination for Low Treewidth Matrices*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf), Corollary 3: the supplied compact bipartite-tree-decomposition linear-system bound. The manuscript's row/column-copy reduction supplies the required graph and does not assume diagonal pivots.
- [Vanderbei, *Symmetric Quasi-Definite Matrices*](https://vanderbei.princeton.edu/tex/myPapers/sqd6.pdf): the exact $LDL^T$ existence statement under every symmetric permutation. The manuscript appropriately does not promote it to an unconditional stability claim.
- [Lee–Yue, *Universal Barrier Is n-Self-Concordant*](https://pubsonline.informs.org/doi/10.1287/moor.2020.1113): the parameter-two existence statement for the planar body.

These checks establish support for the stated ingredients, not a priority claim for every formulation-specific consequence. The manuscript generally marks that boundary well. I did not rebuild the shared manuscript: this review changed no TeX, and a build would add no mathematical confidence to the checks above.
