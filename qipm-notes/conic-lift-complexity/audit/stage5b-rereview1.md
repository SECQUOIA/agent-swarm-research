# Independent Stage 5B rereview 1

Outcome: **No valid major or minor issues found.**

I read the applicable instructions and all five assigned sections end to end: `12a-resource-ledgers.tex` (381 lines), `12b-work-contracts.tex` (208 lines), `12c-newton-comparisons.tex` (822 lines), `12d-query-output.tex` (515 lines), and `12e-active-compilers.tex` (535 lines). I consulted the relevant manuscript dependencies and primary sources below. I did not read previous or current review reports, root checks, an assessment, or the correction-author report. I made no manuscript edits.

## Added temporal and scale results

- **Exact reusable quantum output, 12c lines 382–400.** The contract specifies fixed numerical strings and exact compute–copy–uncompute behavior on the backing workspace, including its correlations with retained registers. This is strong enough to extract each epoch's values without changing the maintainer's subsequent computation. It excludes consumable quantum advice. Joint correctness covers every committed value and epoch, which is the guarantee needed by the finite-output reduction.
- **Fresh updates, `newt:dynamic-scale`, lines 402–475.** The public base and hidden zero/one-coordinate updates give strictly positive slacks (1/s) and (2/s). The relative-error intervals are disjoint exactly for the asserted range. Thresholding the committed labels gives (Tb) independent presence bits. The Kronecker-sum star adversary has norm (Tb\sqrt{s-1}), while each coordinate filter has norm one. Thus superposed epoch access and persistent workspace do not avoid the bound. The randomized product-distribution argument correctly charges expected distinct queries on the no-mark branch before summing. Known-cardinality exact search followed by verification supplies the claimed zero-error upper bound without a joint-success logarithm.
- **Margins, lines 414–418 and 469–474.** Replication changes the number of candidates to (s/k-1=\Theta(s/k)). The stated range includes the endpoint (s/k=2), where one candidate remains. This gives the claimed dependence on the smaller slack, and the update has at most (k) changed coordinates.
- **Universal service, `newt:scale-service`, lines 477–511.** A permissible client reading distinct basis labels gives the lower bound for \(\sum_t\min(r_t,b)\) independent searches. For the upper bound, exact search can be controlled by the source label; deterministic verification and uncomputation yield a clean coherent value interface. Precomputing all sources gives the alternative branch. Zero-invocation epochs require no work. The text correctly distinguishes this universal client guarantee from a particular downstream algorithm's structured calls.
- **Fixed-path caching, `newt:fixed-scale`, lines 527–563.** Stationarity gives \(\rho+\tau^2\rho^2/4=1\), its displayed positive root, and the displayed center. The Hessian eigenvalue ratio is \(2/\rho-1=\sqrt{1+\tau^2}\), including the zero-force limit. Fixed objective norms can be reused. The text explicitly excludes interpreting independent fresh batches as the trajectory of one fixed conic program and retains the necessary embedding/output requirements for any iteration-count multiplication.

## Other mathematics and resource contracts

I rederived the exact off-center Hessian quotient and reduced gradient in 12c. In the transfer proof, the potentially indefinite diagonal test matrix causes no problem: its congruence with the residual is positive semidefinite. Exact allocation makes the middle trace equal to the centered Gram form. Inverting the resulting bounds gives the claimed linear factors. The two-column example attains both spectral endpoints and the condition factor; its two normalized-state distances are correct. Approximate allocations introduce precisely the additional factors stated.

The integer resource ledgers, packing counts, nullity envelopes, Hölder constant, and continuous aspect ratios in 12a are consistent. The work theorem in 12b uses the same exposed rank for curvature and movement, preserves the reference scale, and treats fresh writes and preprocessing as separate premises. I checked the path formulas and checkpoint costs against their movement dependency.

The centered Newton equivalence, signed Lorentz augmentations, graph counts, regularization estimate, and exact-arithmetic replacement conditions in 12c are consistent. The precision and sign-recovery reductions in 12d preserve their access and output contracts. Their movement bounds are simultaneous requirements rather than unjustified products. The exact-body decoders, essential-constraint witnesses, fixed-objective decoding thresholds, and matched-gap entropy metrics in 12e are consistent with the stated query models.

As supplementary checks, an independent script using the specified qipm interpreter verified the order-ledger formula for all (R=2,\ldots,30), (N=1,\ldots,500), and both explicit dimension-ledger formulas. It also checked the allocation Gram bounds and quotient inequalities on 200 randomly generated feasible PSD residuals and 1,000 directions. These checks supplement the algebraic review.

## Primary-source checks

- [Ambainis–Childs–Le Gall–Tani, Theorems 3–4](https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf): the nonnegative spectral adversary theorem applies to finite-valued functions, and the direct-sum statement supports the committed-output reductions.
- [Brassard–Høyer–Mosca–Tapp, Theorems 4 and 16](https://arxiv.org/pdf/quant-ph/0005055): known-success exact amplification and the zero-versus-known-cardinality promise support the zero-error search upper bounds and coherent uncomputation construction.
- [Fürer–Hoppen–Trevisan, Corollary 3](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/LIPIcs.ESA.2025.116/LIPIcs.ESA.2025.116.pdf): the supplied compact bipartite decomposition supports the stated quadratic-width exact field-operation solve without a positive-diagonal premise.

No correction is requested.
