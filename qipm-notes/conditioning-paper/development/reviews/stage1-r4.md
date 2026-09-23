# Stage 1 independent review — reviewer 4

Decision: **No major issues.** One minor planning issue should be fixed before the numerical stage. This review concerns the scope, evidence audit, bibliography, and buildable scaffold; it does not treat deliberately unwritten sections as defects.

## Checks and assessment

I read `development/scope-and-literature.md`, `bibliography.bib`, `main.tex`, `README.md`, and `Makefile`; checked the original Section 3 containment, chord, and width arguments; and checked the active degenerate-LP endpoint note and local Freund package. I independently opened the primary Xiong–Freund preprint, its arXiv record, the author's current research page, and Springer's Nesterov book metadata.

The scope is comprehensive for the selected mathematical topic while excluding distinct oracle-complexity and iteration-distance research for defensible reasons. In particular, including the newer degenerate-LP result is necessary and correctly attributed as a classical corollary. The weak/hard spectral decomposition and coordinate-dependence boundaries belong in this paper. The long quantum access package does not need to be reproduced to make the geometry paper complete.

The proposed difference-body theorem is mathematically plausible, rather than an obviously false strengthening. For a local-unit displacement, orient it downhill and apply Dikin containment; the displacement or its negative is then a difference of two points in the same sublevel set. Asymmetric containment puts every sublevel point within a fixed local-norm radius of the center, giving the other difference-body inclusion. An interior ball homothetically contracted toward an optimizer then gives the proposed largest-eigenvalue upper bound. The required closures, common gap interval, fixed metric, and fixed barrier are expressly listed as proof obligations. These observations support proceeding to full authoring and proof review; they do not replace that review.

The candidate all-barrier weak-projector rate also has a credible route: equal-gap Loewner comparison controls the hard component of any bounded-eigenvalue eigenvector by O(g). Orthogonality of the objective to the face tangent yields the claimed order for its weak projection. The sharper logarithmic-barrier order and oscillatory perturbation witness appropriately remain unverified candidates. The final paper must distinguish the norm of a weak projection from its squared mass.

The literature positioning is materially stronger than the old manuscript. Xiong–Freund §5.1, Fact 5.2 and Remark 5.1 explicitly use the same containment argument to bound sublevel diameter using a central-path Hessian eigenvalue. The planned paper correctly recognizes this as direct antecedent and does not claim to introduce geometric conditioning. The fixed-primal-gap, tangent-Hessian difference-body/Loewner formulation appears distinguishable from those displayed statements, but the planned qualified novelty language and further comparison are essential.

Primary sources checked:

- [Xiong–Freund, July 15, 2024 preprint](https://optimization-online.org/wp-content/uploads/2024/06/arXiv_0715.pdf), PDF pages 32–34: confirms the stated containment/Hessian precedent and subsequent rescaling analysis.
- [arXiv record](https://arxiv.org/abs/2406.01942): confirms version 3 dated July 15, 2024 and supplies no journal reference. The preprint bibliography entry is justified. The [author's research page](https://zikaixiong.github.io/research.html) does not provide grounds to invent journal publication details for this title.
- [Springer Nesterov metadata](https://link.springer.com/book/10.1007/978-3-319-91578-4): confirms the 2018 second edition, volume 137, and DOI. This metadata check does **not** verify Theorem 5.3.8; the explicit pending proof/source obligation remains necessary.

The audit accurately identifies the local Freund (2003) package as unread and metadata-only. It does not pretend that a bibliographic entry verifies a theorem. The bibliography and scaffold make no unsupported final novelty claims.

## MINOR R4-1: make the numerical reproduction deliverable explicit

**Location:** “Netlib survey and window-solver experiments” inventory row and Stage 5 completion plan.

**Issue:** The plan correctly requires reproduced results, data transformations, and precision limits, but does not explicitly require a portable command and provenance record for the selected numerical results. The parent scripts and data paths can otherwise leave the new directory dependent on mutable repository artifacts. This is a small planning gap, not a defect in numerical evidence that has not yet been authored.

**Suggested fix:** Add a Stage 5 obligation to provide a reproduction manifest or README identifying the exact commands, software versions, random seeds where used, source-data locations/checksums, transformations, and generated output files supporting each retained table/figure. State whether reproduction intentionally requires the parent repository or bundle the small required scripts in the new directory. Preserve numerical failures and accuracy cutoffs in machine-readable outputs as well as manuscript discussion.

## Outcome

No major issue warrants another five-reviewer cycle for Stage 1 on the basis of this review. Address R4-1 in the plan, then proceed to theorem authoring. The strong candidate extensions must still receive their scheduled full mathematical review.
