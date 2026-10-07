# Opus whole-paper review, round 1 — INTERIM

**Status: interim working record, 2026-10-05 21:20 UTC. Not the final report.**
The final report will replace this file after the final reread of the files
that changed during review. Until then, nothing below is a final verdict.

Why an interim file exists: four delegated read-only Opus proof checks
(Appendix E degree bounds; G–H fields and certificates; I recourse; J–K
contrasts and boundaries) terminated without reporting, three on an account
session rate limit and one on an output-length limit. None of their content is
used here. I am reconstructing those appendices myself. This file preserves
the completed part of the review in case my own session is interrupted.

## Completed so far (my own reconstruction)

Read in full and reconstructed: abstract, Sections 00–11 (first snapshot),
Appendices A, B, C, D, F, and E except its degree-bound and five-variable
subsections. Main-text arguments of Sections 08–10 were also checked.
Details will be in the final report. I found **no mathematical error** in
these proofs. The adaptive single-sign compiler (`thm:posslp-closure`), the
separation lemma, the Newton circuit and non-gradient warm start, the
certified-quartic lower bounds (cube-root and quaternion compilers and both
realizations), `lem:quartic-realization` with exact canonical-Gram covariance,
`thm:global-point` (exponent `1/D`, effective constant), `thm:cubic-point`,
the constrained, integer-list and unambiguous-certificate proofs, the power-
coordinate and cyclic constructions, and the height, moment, interior-Gram
and circuit-Gram proofs all check.

## Findings recorded so far (to be rechecked against the current files)

Required precision repairs (no theorem is false):

1. Abstract recourse sentence: say that the selected optimizer is that of the
   randomly tilted instance, correct on every draw; the unperturbed instance
   is not solved.
2. `sections/03-upper.tex`, related-work paragraph: "classification ...
   including equality" overstates the section (equality has only the upper
   bound; the lower bounds cover order tests for certified quartics/cubic
   maps).
3. `sections/03-upper.tex`: Allender et al. are credited with a "reduction" of
   Square Root Sum to PosSLP; their result is membership in `P^PosSLP`; the
   many-one form comes from `thm:posslp-closure`(b).
4. `sections/00-introduction.tex`: Slot–Steurer–Wiedmer Theorem 1.1/
   Corollary 1.2 are described without the degree/encoding premise that
   Section 02 and the abstract state.
5. Appendix L (Q13–Q14) was added to `main.tex` during this review after the
   brief excluded it. It needs its own review and consistent introduction,
   organization, abstract, and coverage text. This review does not cover L.
6. Source gates for Luna: the Tarasov–Vyalyi basis contract behind
   `rem:models-socp`; the description of Slot–Steurer–Wiedmer v1 Appendix C
   (Section 06 says a convex sextic; the literature review mentions a cubic
   singleton and Lemma C.3).
7. Low: `thm:reductions-min-sign` uses `u_0>0` citing the compiler display,
   which states only `(xi_e-1)^2>0` (the appendix proves `xi_e>1`).

Optional items (notation overloads of `L`, `Lambda`, `N`, `k`; local
"exponential in the dimension" qualifiers; imported-results table citations;
duplicated lemmas; length and splitting) will be listed in the final report.

## Remaining work before the final report

- Reconstruct Appendix E five-variable degree-21 and degree-bound proofs,
  Appendix G constructions, Appendix H radial finiteness and radial bounds,
  Appendix I recourse chain, and Appendices J–K high-priority results.
- Reread every file changed since 20:19 UTC (all sections, Appendices A, D,
  E, G, J, `references.bib`, `main.tex`) and recheck each finding above.
- Record final hashes and the scoped document check.
