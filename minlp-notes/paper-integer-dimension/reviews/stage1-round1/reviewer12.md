# Stage 1, round 1 — reviewer 12

Primary lens: primary-source attribution, bibliography, novelty wording, and imported theorem hypotheses.

Major findings: 0
Minor findings: 2

I found no major mathematical defect in the completed stage. This is a bounded independent review, not a claim of certainty or an exhaustive priority search. The two findings below concern a source locator and notation. Neither overturns a theorem.

## Snapshot and coverage

I computed SHA-256 hashes from the working files and compared all five with `snapshot.json`. All matched:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I read the entire 1,206-line stage, the bibliography, process/protocol, coverage inventory, and macros/main file. I independently followed the mathematical proofs throughout: parity closure; bounded and common-recession disjunctions; exact square and product bounds; fractional allocation; indefinite determinant bound; inertia and continuous epigraph formulation; principal compression; real symmetric shrinking; covariance and Hall/permanent bounds; matrix-evaluation oscillatory lower bound; smooth upper constructions; Legendre tubes; and positive perspective transfer.

Original-source comparison concentrated on `results/quadratic-system-noncommutative-rank-complexity.md`, `results/smooth-map-local-rank-integer-complexity.md`, and `results/constant-hessian-rank-smooth-precision.md`, with the associated rank/novelty investigations. This was not a second complete reading of every original result or every audit indexed in `coverage.md`. Earlier review labels were not treated as evidence of validity. Stage 2's rational quantitative theorem remains a preview: I checked its stated external algorithmic prerequisites, not the unwritten full bit-bound proof.

Primary material inspected includes cached GGOW, Fortin–Reutenauer, Nicola, and Wolff texts; the local Lubin and Beach manuscripts; IQS's arXiv v6 text; Volčič's published Section 2.1; and both published Beach article pages. The original Hörmander PDF URL failed with HTTP 500, so I verified the stated analytic theorem against Wolff's Theorem A and the manuscript's own proof instead. I did not independently retrieve original McCormick or Boyd texts, inspect the final rendered PDF, or conduct an exhaustive historical novelty search.

## Findings

1. **MINOR — Incomplete exact locator for the capacity characterization.** Location: `sections/01-foundations.tex:529–541`, the citation to GGOW Theorems 1.4 and 1.17 immediately preceding equations `eq:shrunk`, `eq:evaluation`, and `eq:capacity`.

   The first two locators support the shrinking and matrix-evaluation characterizations. Neither named theorem states the capacity equivalence. In the cached published GGOW text, Theorem 1.4 lists singularity, evaluation, shrinking, rank-decreasing, and invariant-theoretic conditions; Theorem 1.17 states free-field/inner-rank/decomposability equivalences. Capacity is defined later, in Definition 2.6, and its positivity connection is discussed in Sections 1.5–1.6 and subsequent operator-scaling sections. Thus the mathematical statement is supported by the paper, but the precise citation purporting to cover all three results is incomplete.

   **Repair:** separate the capacity citation or expand the locator to its actual discussion and explicitly credit Gurvits for that connection. The GGOW Section 1.5 discussion itself attributes this capacity ingredient to Gurvits. It would also improve historical attribution to name Fortin–Reutenauer for the maximum-deficiency formula, as GGOW's discussion immediately before Theorem 1.17 does. This is a citation/attribution repair, not a missing mathematical hypothesis or proof gap. [GGOW published paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).

2. **MINOR — Literal commas appear where the Taylor-error bound needs multiplication.** Location: `sections/01-foundations.tex:974`, `:977`, and `:993`, in the proof of `thm:smooth-ranks`.

   The source has `C_0,2^{-T}` three times, including the tolerance selection `2C_0,2^{-T}\le\eps`. The comma is ordinary mathematical punctuation, not a multiplication or spacing command. The surrounding proof clearly establishes `C_0 2^{-T}` and requires `2C_0 2^{-T}\le\eps`.

   **Repair:** replace these three occurrences by `C_0\,2^{-T}` (and retain the leading factor 2 in the tolerance condition). The argument is otherwise valid: each potentially nonzero Hessian term has the required sum of coordinate exponents, and convexity of each cell intersection keeps the Taylor segment in the domain.

## Checks supporting the assessment

The imported algebra is used with compatible fields and hypotheses. The complex free-field pencil is Hermitian under the involution fixing variables and conjugating scalars, as stated in [Volčič, Section 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1). The Schur-complement principal-pivot argument respects multiplication order. The real descent uses supermodularity and conjugation, and the orthogonal-space construction then supplies a congruence-compatible zero pattern rather than assuming independent row/column changes are valid input changes.

IQS Theorem 1.5 gives the rational maximum-deficiency witness and polynomial intermediate/final data size, while Lemma 5.3 gives field-extension invariance. Those support the prerequisites stated in the rational preview. Calling the source a revised 2018 manuscript is consistent with the inspected v6 version. [IQS v6](https://arxiv.org/html/1512.03531).

Nicola Definition 1.1 and the following paragraph explicitly give affine fibers of the gradient under constant Hessian rank. The paper derives the needed local identity itself and correctly bounds the entire polyhedral tube. Wolff Theorem A states the mixed-Hessian nondegeneracy estimate with smooth compact amplitude; the manuscript supplies those hypotheses locally and gives a valid integration-by-parts/Schur proof. No boundary regularity of contact sets is needed.

The published Beach author order is Beach, Burlacu, Bärmann, Hager, Hildebrand, matching both bibliography entries; the older local combined manuscript has a different order and should not be used to “correct” the published metadata. The volume, page ranges, and substantive sawtooth/disaggregation attributions match the published records. [Part I](https://link.springer.com/article/10.1007/s10589-023-00543-7), [Part II](https://link.springer.com/article/10.1007/s10589-024-00554-y).

I executed an independent SymPy check of all six squared difference products in the four-point width obstruction, the cross-product identity `sum H_j^2 = 2 I_6`, and the displayed rank-three Hessian of the degree-four smooth example. All passed. I also manually recomputed the indefinite and covariance finite constants and the scaling in the oscillatory contact-volume inequality. These checks supplement the proofs; they do not certify the general theorems.

The stage avoids unsupported first-in-literature wording and distinguishes established ingredients from the resulting formulation consequences. A later introduction should still include the close scalar approximation precedents identified in the repository's source investigation; the present review does not establish external priority.
