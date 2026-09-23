# Stage 4, round 1: independent review 4

Verdict: **0 major findings, 0 minor findings.** I found no required repair in the new presentation, attribution, figure, or submission package.

I read the abstract, introduction, conclusion, reproducibility appendix, README, Makefile, figure and packaging scripts, bibliography, final source ledger, literature record, and Stage 4 author audit. I inspected the overview figure and compared the new result summaries with the mathematics reviewed in earlier stages. I did not inspect peer review reports or modify manuscript sources or supplied artifacts. This is the requested presentation/attribution review, not the subsequent fresh full-proof review.

## Literature and novelty

The framing identifies the closest direct motivation correctly: Orsucci–Dunjko already discuss normalized complement construction, the limitation of LCU normalization, and specialized stronger-access constructions. The introduction explicitly avoids claiming discovery of that obstacle or resolution of the separate sparse-value construction problem. Its factor-access and support-overlap discussion is consistent with the primary passages checked during Stage 3.

I independently checked the new close comparisons against primary sources:

- [Dong–Larsen–Lin–Sarkar](https://arxiv.org/pdf/2608.30937), especially the constrained feasible set, fitting-set distinction, and discussion of boundary feasibility, supports the introduction's characterization. The manuscript appropriately distinguishes an analytic shrinking-interval threshold law from their constrained-minimax numerical design and retraction methods.
- [Sarkar–Yoder](https://arxiv.org/pdf/2111.07182), Definition 1.1 and its density conclusion, supports the statement about constraints outside the approximation interval and endpoint compatibility. The manuscript does not claim that exterior constraints are a new subject.
- [Laneve](https://quantum-journal.org/papers/q-2026-03-13-2025/pdf/), particularly the polynomial state-conversion discussion and Theorem 4.5/Corollary 4.9, supports the attribution of QSP/adversary feasibility connections. The new text does not present the general polynomial-query viewpoint as original.
- [Somma–de Wolf](https://arxiv.org/abs/2608.24493) supports the stated distinction in output tasks and the presence of guide-overlap, dimension, and sum-of-squares hypotheses. Its lower bounds are not imported into the shift task.
- The [APS publication page for King et al.](https://journals.aps.org/prl/abstract/10.1103/m3fj-m4rm) confirms PRL 136, 110601, published 17 March 2026, and the DOI used in the bibliography. Its sum-of-squares amplification context matches the brief comparison.

The historical constrained-approximation references are used at the broad subject level; the paper does not infer the absence of an exact antecedent from unavailable full text. QSVT/GQSP implementation, amplification, sign approximation, exterior Chebyshev, Fejér–Riesz, generic factor advantages, and amplitude estimation are clearly identified as prior tools. The final originality sentence is qualified and limited to the exact shift thresholds, equality-attaining constructions, and optimal query exponents. That is a defensible scope given the cited comparisons; this review does not certify universal priority.

## Consistency with the proved results

The abstract and introduction preserve the positive-K conditions, the general c<1 versus c=1 coarse distinction, exact threshold equality, and the restriction of the parity comparison to one definite-parity transform. They correctly state the even plateau, the concrete matched exponent 5/6, and the odd logarithmic factor. The degree-six witness is only an upper bound on F_3.

The intermediate comparison retains the upper-tier margin and declines to assert a uniform multiplicative optimum. The conclusion identifies the remaining intermediate factor, higher even thresholds, and synthesis precision as open questions. The LP overview distinguishes the dual state from the public primal predictor, counts RHS state access, makes the compiler matrix-only, states the zero-query coarse exception, and excludes an LP/QIPM solver lower bound. Reuse is explicitly charged per application of the oracle circuit.

The final source ledger agrees with those corrections and strengthened results. I found no unsupported restoration of a superseded source-note claim.

## Figure and reproducibility

The figure's boundary markers select the correct cheaper tier. Its left panel stops before the next undisplayed threshold. Its right panel lies in a proved range: G_1<1/32, F_3<1/32, and F_1=F_2=1/24. The overlapping even/unrestricted curves above 1/24 are shown without changing their powers. The odd logarithm and coarse logarithmic exception appear in the figure or caption. The scripts use the stationary-equation solver and do not represent sampled feasibility as a proof.

The archive passed its CRC check, contains the intended 18 files, and every archived file exactly matched the current source or required artifact. There were no duplicate LaTeX labels or undefined references. The reported Python/NumPy/SciPy/Matplotlib versions match qipm.

I extracted the archive to `/tmp/spectral-stage4-review4-rb9yhun3` and ran `make`, `make figures`, and `make` under qipm. All three completed successfully; the final LaTeX log had no warnings or overfull/underfull boxes. The source archive is independent of development audits, local literature, and repository data. Regeneration occurred only in the temporary extraction, leaving the frozen artifacts untouched.

Required repairs: none.

Counts: **0 major, 0 minor**.
