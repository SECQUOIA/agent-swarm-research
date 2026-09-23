# Root notes for the later PDLC stage

The current `results/four-aggregation-strict-pdlc.md` supersedes the earlier
projective-chart proof. Its improved argument works in every n>=1, handles
dependent triples by independent positive definite perturbations, and uses
the already accepted negative-direction lemma to make every inward
perturbed nonstrict system bounded and free of points at infinity.
Do not reproduce the longer superseded chart argument unnecessarily.

The root independently read the updated proof on 2026-09-22. The ratios
f_i/g_i provide a single continuous function whose generic sublevels have
the needed regularity. The determinant-minor polynomial has a nonzero
cubic leading coefficient, so independence fails at only finitely many
parameters. The fixed-cardinality limit still requires the negative-cone
orientation argument to preserve strict validity; mere nonstrict limiting
validity would not suffice.

The root freshly inspected [BD arXiv v1](https://arxiv.org/html/2405.18282v1),
Theorem 1.4 and its proof at the end of Section 8. The statement retains
PDLC, nonempty interior, regularity of the nonstrict set, and no points
at infinity. The proof explicitly treats n=1,2 using Proposition 8.7 and
n>=3 using Proposition 8.10; the other hyperbolicity-cone case uses 8.6.
Thus the all-dimensions input is supported by the inspected primary text.
The published author eprint failed fresh retrieval for the root. Preserve
version-specific locators; the old arXiv Section 8 is published Section 7.

The root also read the complete thesis extraction's Theorem 5.0.5 and
its references to Propositions 5.3.12 and 5.3.13. Its statement omits
the infinity condition, whereas those proof dependencies explicitly require
it. This discrepancy must qualify priority discussion; do not claim the
stronger regular theorem was never previously stated. The new proof uses
only the fully qualified BD theorem and addresses arbitrary strict systems.
The thesis text is `/tmp/dunbar-thesis-priority.txt`; its original-PDF
retrieval still fails, and damaged inequality glyphs are documented in
`notes/review-20260922-pdlc-priority.md`.

The later author and five reviewers must independently verify the current
all-dimensions proof, sharpness witnesses, oriented SOC closure and precise
relationship to BDS Conjecture 3.2 before accepting this manuscript stage.

During stage 6, the coordinator freshly reopened BD arXiv v1 Theorem 1.4, its final proof, and Proposition 3.15's proof in Section 8. The inspected text supports both the all-dimensions input and credit for the earlier negative-eigenvector limiting argument for a fixed feasible set. The coordinator also ran `python3 code/research_20260922/check_four_aggregation_pdlc.py`: all four exact witness slack vectors, the signed PDLC identity, and strict feasibility passed. This finite algebraic check does not verify the universal transfer argument.
