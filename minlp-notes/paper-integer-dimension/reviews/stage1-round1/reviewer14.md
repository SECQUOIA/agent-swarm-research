# Reviewer 14 — stage 1, round 1

Primary lens: reader comprehension, mathematical exposition, terminology, and organization, with independent checks of the complete stage's mathematics.

Major findings: 0
Minor findings: 2

The stage has a coherent proof chain, and I did not identify a false theorem or a material unsupported step in the material reviewed. The distinctions between integer dimension, linear description size, rational encoding, and optimization time are particularly useful. The distinction between parity contacts and convex sections is stated at the point where readers need it. The quadratic, smooth, constant-rank, and perspective results retain their different hypotheses and conclusions. The two findings below concern a repeated typesetting error and an unnecessarily implicit sharp depth choice.

1. **MINOR — Typesetting error in the smooth upper proof.** Location: `sections/01-foundations.tex:974`, `:977`, and `:992`, proof of Theorem 4.3 (`thm:smooth-ranks`); visible on compiled PDF page 14. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas where multiplication is intended. In particular, the instruction `2C_0,2^{-T} <= epsilon` is not a well-formed scalar inequality. The preceding Taylor argument supplies the intended product estimate, and the original smooth-map result writes it correctly, so this is not a substantive proof gap. Replace the three commas with spacing commands: `C_0\,2^{-T}` and `2C_0\,2^{-T}`.

2. **MINOR — State the precision depth that gives the claimed one-sided coefficient.** Location: `sections/01-foundations.tex:470–472`, proof of the one-sided inertia law (`thm:inertia`). The proof says only that `L=O(1+log(1/epsilon))` is chosen to meet the error inequality. This states the logarithmic order but leaves the sharp coefficient `k_-/2` implicit: many such depths meet the inequality with a larger leading coefficient. The immediate repair is to put `A=sum c_j+sum d_j` and choose `L=max{0,ceil((1/2)log_2(A/(4 epsilon)))}`, as in the original one-sided result. Then state `k_-L=(k_-/2)log_2(1/epsilon)+O(1)`. This is a local exposition/justification omission with an explicit valid choice, not evidence that the theorem is false.

No major findings were identified within the verification limits below; this does not claim certainty or external peer review.

## Reviewed snapshot and hashes

I read `PROCESS.md`, `reviews/PROTOCOL.md`, the stage task and lens instructions, the complete `sections/01-foundations.tex` (lines 1–1206), `coverage.md`, `macros.tex`, `main.tex`, and `references.bib`. SHA-256 checks against `reviews/stage1-round1/snapshot.json` all matched:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

## Mathematical and source coverage

I reconstructed the following arguments directly from the manuscript:

- Closure of parity classes without measurable witness selections; arbitrary integer ranges; preservation under affine slices; binary code disjunctions, including the common recession-cone case.
- Strong-convexity diameter constants, square attainment, McCormick residual error, the product area/width estimates, the four-point width obstruction, and the unequal-edge LP allocation.
- The indefinite determinant/volume estimate and its finite constant; signed-square upper bounds; epigraph inertia, continuous folding, the exact one-product convex-lift count, and the LP face-count argument.
- Hermitian principal compression over a division ring; real descent of maximal shrinking; orthogonal block structure; covariance expansion and volume comparison; the capacity determinant estimate and independent Hall/permanent argument; shared-prefix construction and its row/variable count.
- The squared-Hessian certificate, cross-product example, and the interaction-graph comparison of coefficients.
- The local oscillatory `TT*` argument, real matrix evaluations, the Cartesian-power contact-volume estimate, principal slices, the global Taylor upper bound, and the fixed-degree bit-product compiler.
- The constant-rank Legendre chart, whole-tube error estimate, finite chart covering including the boundary, and the perspective row homogenization and slice bounds.

I compared corresponding proof passages in all nine stage-1 canonical result files listed in `coverage.md`. This was a focused comparison of proof passages, not a complete reread of every historical result file. I also read the supporting parity/epigraph/width note, the nonquadratic investigation, and the constant-rank and perspective audits. Their prior verdicts were not used as mathematical evidence.

After reading `literature/AGENTS.md`, I checked the retrieved primary text of Lubin–Vielma–Zadik's Lemma 4.1, GGOW Theorems 1.4 and 1.17 and relevant capacity discussion, Nicola Definition 1.1 and its following paragraph, and Wolff's Theorem A on printed pages 50–51. These support the corresponding uses in the stage. I read the bibliography but did not independently verify every bibliographic field or every external source, and this report makes no new priority judgment. In particular, the detailed rational bit-complexity preview remains a stage-2 proof obligation, as explicitly stated in the manuscript and inventory; I did not treat it as a missing stage-1 proof.

## Executed checks and limits

- Ran a Python SHA-256 comparison for all five frozen files: all matched.
- Extracted the existing 18-page compiled PDF with `pdftotext` and checked the smooth theorem/proof on page 14; this confirms the comma errors survive compilation. I did not perform a complete visual page-layout audit or rebuild the manuscript.
- Executed independent exact SymPy checks of the rank-three polynomial example's Hessian at `(1,1,1,1)`, all six products in the four-point width example, the Hessian of `x^2/t`, and the cross-product identity `sum_j H_j^2=2I_6`. All checks passed. These checks supplement the proofs and do not replace them.
- No manuscript, bibliography, or original-research files were edited. No subagents were used. Later-stage mathematical results and the completeness of all 173 historical supporting notes were not independently audited.
