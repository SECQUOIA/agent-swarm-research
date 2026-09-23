# Reviewer 01 — stage1-round1

Primary lens: adversarial end-to-end mathematical validity and counterexamples.

Major findings: 0
Minor findings: 2

## Snapshot and coverage

I checked the following SHA-256 values with `sha256sum`; all match `reviews/stage1-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I read all 1,206 lines of the mathematical stage, the process and review instructions, the bibliography, macros, main file, and coverage inventory. I compared the proof chains against all nine stage-1 canonical result files, concentrating on their corresponding mathematical sections, and inspected the parity/epigraph/width and smooth-map supporting notes. I also inspected the second noncommutative-rank audit and constant-rank audit after independently reconstructing those proofs; their verdicts were not used as proof.

Primary-source checks used the cached GGOW published text (Theorems 1.4, 1.17, 2.18, the capacity discussion in Section 1.5, and Section 2), Wolff's Theorem A on printed pages 50–51, Nicola's Definition 1.1 and following paragraph, and the local original-source extraction of Lubin–Vielma–Zadik's Lemma 4.1. I read `literature/AGENTS.md` before accessing that package. I did not conduct an exhaustive publication-priority search or independently verify every bibliographic entry. The rational uniform bit bounds are explicitly deferred to stage 2; this review does not certify their later proof or the IQS algorithmic locator. I did not compile or visually inspect the PDF.

## Overall assessment

I found no major mathematical failure in the completed stage. The main quadratic-system theorem has a coherent lower/upper proof: principal compression preserves the requisite matrix-space rank; compact parity contacts admit the covariance bound; the capacity or independent Hall/permanent argument controls their volume; real descent and symmetric shrinking give an allocation with total exponent r/2; and the binary prefix construction implements that allocation with the advertised graph containment and error. The principal-compression argument correctly keeps multiplication order over the division ring.

The smooth lower bound also withstands the principal adversarial concern: it controls highly anisotropic contacts without replacing the quadratic argument by an unjustified small perturbation. The matrix-evaluation phase has the stated mixed Hessian, the small-support TT* argument gives the required operator estimate, and tensorization cancels the evaluation dimension from the volume exponent. The constant-rank upper proof controls entire polyhedral tubes in original coordinates and handles the box boundary through its neighborhood hypothesis.

I checked the finite constants, signs, and endpoint conventions for squares, products, scalar indefinite quadratics, covariance certificates, one-sided inertia, the cross-product example, and positive perspectives. No counterexample emerged from these checks. This is a bounded mathematical review, not a certainty claim.

## Findings

1. **MINOR — typographical corruption of the Taylor remainder bound.** Location: `sections/01-foundations.tex`, lines 974, 977, and 992, in the proof of `thm:smooth-ranks`. The text contains `C_0,2^{-T}` and `2C_0,2^{-T}`. These render literal commas between factors; the displayed estimate and error-budget instruction should be products. The surrounding proof and the corresponding source result make the intended bound unambiguous, so this is a notation error rather than a proof gap. Replace these by `C_0\,2^{-T}` and `2C_0\,2^{-T}` (or ordinary juxtaposition).

2. **MINOR — capacity characterization needs its own source locator.** Location: lines 529–541, especially the single citation to GGOW Theorems 1.4 and 1.17 preceding `eq:capacity`. The cited theorems provide the singularity/matrix-evaluation and rank/decomposability characterizations. Their statements do not themselves give the positive-capacity equivalence. The GGOW primary text explicitly credits that fact to Gurvits in Section 1.5, immediately before Section 1.6, and discusses capacity in Section 2. The mathematical fact is supported by the source, and the manuscript additionally proves an independent qualitative energy route, so this is an incomplete attribution locator, not a false theorem or substantive missing proof. Split the citations: keep Theorems 1.4 and 1.17 for rank/evaluation/shrinking, and add GGOW Section 1.5 and the relevant capacity discussion for positivity, preferably naming Gurvits as the source of that equivalence.

## Independent executed checks

- Solved the manuscript's continuous folding LP using SciPy/HiGHS for depths 1 through 6 and 65 uniformly spaced inputs at each depth: all 390 optima agreed with the exact folding sequence to tolerance 1e-8. This checks the claimed projection behavior, not merely the feasibility of the proposed sequence.
- Used exact SymPy algebra for the four-point width obstruction: all six squared difference products equal `(sqrt(5)-2)^2`, confirming the stated absolute products and obstruction to constant four.
- Manually recomputed the covariance fourth-moment expansion, determinant/volume rearrangements, and the scalar and cross-product finite constants.

No manuscript files were changed and no subagents were spawned.
