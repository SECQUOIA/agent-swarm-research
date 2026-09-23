# Stage 1 independent review 2

Verdict: no major issue found in the revised introduction or bibliography. Two minor exposition/attribution corrections are recommended before closing this stage. Neither changes a mathematical result. This is a review of the Stage 1 claims against the supporting manuscript and primary literature, not a claim to have completed the later proof-by-proof gadget audit.

## Scope and independent verification

I read the complete frozen introduction and bibliography, the author report and literature audit, the complete AC and algebraic sections, the main numerical results and proofs, and the structural/reduction statements and supporting construction discussion. I did not consult other Stage 1 reviewer reports or rely on historical PASS verdicts.

I independently inspected primary local texts for Gan–Low/model context, Jeeninga et al. (model, signed demands, Theorem 3.22), Bienstock–Verma (model and hardness), Lehmann et al. (model and star reduction), Farivar–Low (angle-recovery theorem), Jafarpour et al. (winding-cell and uniqueness theorems), Lavaei–Low (Appendix B Case 2), Abrahamsen–Miltzow (Theorem 1, Definition 4, Corollary 2), Jeronimo et al. (Example 13 and polynomial-minimum context), Bienstock–Muñoz (Theorem 7 and Corollary 8), and Bienstock–Del Pia–Hildebrand (rational and approximate certificates). Fresh web searches used power-flow/existential-real and resistive/universality combinations; they did not identify a closer matching theorem. Search failure is not evidence of exhaustive priority. I also checked the primary arXiv records for the new Delabays, Mareček, and Bienstock–Del Pia–Hildebrand entries.

Useful source locations independently checked:

- `literature/papers/jeeninga2023-dc-power-grids-with-constant/fulltext.md`, model around lines 109–165 and Theorem 3.22 around 663–683.
- `literature/papers/lehmann2016-ac-feasibility-on-tree-networks/fulltext.md`, Section II and Theorem 1.
- `paper-power-flow/revision-20260907/sources/farivar-low.txt`, Theorem 2 around lines 483–514. Published primary source: <https://smart.caltech.edu/papers/relaxconvex2parts.pdf>.
- `paper-power-flow/revision-20260907/sources/jafarpour.txt`, Theorem 3.6 around 985–1002 and Theorem 4.1 around 1217–1223. Primary preprint: <https://arxiv.org/abs/1901.11189v4>.
- `paper-power-flow/build/source-cache/lavaei-low.txt`, Appendix B Case 2 around 1032–1055.
- `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv/fulltext.md`, printed pages 3–4. Primary version: <https://arxiv.org/abs/1912.08674v1>.
- `literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/fulltext.md`, Theorem 7/Corollary 8 around 103–107. Primary version: <https://arxiv.org/abs/1501.00288v15>.
- `paper-power-flow/build/source-cache/jeronimo-minimum.txt`, Example 13 around 639–651.
- Metadata and broad scope: <https://arxiv.org/abs/1512.04266>, <https://arxiv.org/abs/1412.8054v2>, <https://arxiv.org/abs/2011.08347>.

## Minor findings

1. **Bounded structure should qualify the general network-optimization approximation claim.** Locator: frozen `sections/00-introduction.tex:219–222`. The sentence says Bienstock–Muñoz “give LP approximation schemes for polynomial network optimization and bounded-treewidth AC optimal power flow.” Grammatically, the bounded-treewidth qualification applies only to AC. Theorem 7's useful polynomial-size guarantee depends on treewidth and the number of local variables/constraints, with exponent `O(Delta omega)`; it is not a general unrestricted-network approximation guarantee. The citation locator is correct and the exact-versus-scaled distinction is correct, so this is a scope ambiguity rather than a major false scientific comparison. Suggested correction: “give LP approximation schemes for polynomial network optimization under bounded-treewidth and bounded-local-dimension hypotheses, including AC optimal power flow, with scaled feasibility and optimality tolerances.” Alternatively state that their sizes depend exponentially on the structural parameters and preserve the simpler existing sentence for the AC corollary.

2. **Make explicit that the rational-equivalence definition agrees with the cited preprint when explaining its overly broad statement.** Locator: frozen `sections/00-introduction.tex:197–201`. “Unavailable under the rational equivalence used here” can suggest that the difference is the current paper's stronger definition. Abrahamsen–Miltzow Definition 4 likewise requires both coordinate maps to be rational functions (integer coefficients there versus rational coefficients here makes no difference). The manuscript's compact basic-closed invariant and three-quadrant argument support the correction under that same globally defined rational-map interpretation. Because this passage identifies a limitation in a named predecessor's theorem, remove the potential definitional escape: for example, “With rational equivalence understood through globally defined rational coordinate maps, as in Definition 4 of that preprint, Proposition ... and the three-quadrant example rule out that broader scope.” Then retain the conjunction-only, independently proved replacement. This is attribution precision; I found no defect in the invariant or three-quadrant proof.

## Confirmed substantive points

The central restricted resistive completeness statement matches Theorem `thm:structural`, including simultaneous restrictions and finite data depending on a fixed girth requirement. The introduction correctly distinguishes cycles of large girth from trees and does not conflate NP-hardness with a proved separation of NP and existential-real complexity.

The physical-model comparisons are accurate. Jeeninga et al. explicitly allow signed power demands and exclude independent operational voltage limits; fixed-source injection restrictions are also absent. Gan–Low relaxation exactness is presented with hypotheses, rather than as an unconditional Turing tractability assertion. The Bienstock–Verma lossless/fixed-magnitude/reactive-unconstrained scope and Lehmann fixed-magnitude star scope match their primary texts. The paper makes no improper claim of subsuming either model.

The winding attribution is materially improved and correct. Farivar–Low's criterion is modulo `2 pi`; the manuscript's selected short differences require zero real cycle sums. Jafarpour et al. already formulate winding cells and at-most uniqueness for monotone flow maps. The new text properly credits this and confines its additional claim to explicit rational polynomial encoding and complexity transfers. The manuscript's crossing-rule proof handles unequal magnitudes, negative rational cosines, and the axes consistently; no branch-boundary contradiction was found on inspection. The equal-angle energy argument uses the stronger real-lift hypothesis and does not inherit the unrestricted implication suggested by Lavaei–Low Appendix B Case 2. Principal winding examples remain expressly excluded from that implication.

The algebraic, residual, and certificate summaries agree with the stated results. Topological universality is separated from rational equivalence; source-to-network solution preservation is the electrical contribution. JPT's repeated-power example establishes the known general double-exponential separation scale. The new residual claim is restricted to the ordinary fixed-data bounded-degree electrical family and is not silently transferred through planarization. The gap promise and exact voltage box are stated; no NP certificate for unpromised exact feasibility is claimed.

## Optional preference, not a required correction

An explicit reference to Abrahamsen–Miltzow Corollary 2 near the algebraic-field discussion would give especially direct credit for the source arithmetic field-of-definition consequence. The introduction already credits bounded arithmetic universality and identifies the electrical realization as the contribution, so its absence is not a novelty overclaim.

No manuscript files were edited and no build was performed. The changes are prose/bibliography only, and the frozen theorem-to-introduction alignment was the relevant verification for this review.
