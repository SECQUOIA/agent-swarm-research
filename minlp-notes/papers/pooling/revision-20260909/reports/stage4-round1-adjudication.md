# Stage 4 round 1 adjudication

Root read all five complete independent reports (review1 through review5), including their proof coverage, evidence, findings and stated limits. All five found no major mathematical defect. Root agrees: the proposed changes below do not change a theorem, repair a false proof, or require new development. Root's full analytical and source audit is in root-stage4.md. Stage acceptance remains pending the separate correction pass and root verification.

## Accepted corrections

1. **Minor attribution (R1 O1):** cite published Jalilian–Kocuk Lemma 1 beside the Appendix B one-free-margin pattern. Preserve the complete argument and distinguish the subsequent arithmetic/certificate conclusions. Root checked published Lemma 1 and Theorem 2 directly.
2. **Minor attribution (R5 R5-1):** cite Dey–Kocuk–Santana Theorem 4, Appendix A.3 Proposition 12 beside the Appendix C nonpolyhedral two-by-two example. Root checked the original: swapping rows and setting a=1-q identifies the valid subinterval a in [0,1/2]. Preserve the manuscript's correct q in [1/2,1]; do not import the source's overly broad printed parameter range.
3. **Minor scope (R4 R4-1):** qualify the synthesis opening's few-mixing-variable explanation as applying to the one- and two-pool reductions. The all-two construction has growing pool count and a different pure-mode mechanism.
4. **Minor precision (R4 O1):** describe the negative answer to BKR's broad two-pool question as its bounded-product case; preserve the explicit growing input/attribute qualification. This avoids overstating which choices of their unspecified bounds are settled.
5. **Minor precision (R2 O1):** say total entrywise l1 error in the synthesis approximate-hull summary. The formal theorem already has this norm; the summary should not suggest a maximum-entry error bound.
6. **Minor source cleanup (R2 O2, R4 O2):** remove the two uncited bibliography entries s6:deloera2006 and s6:khademnia2024v2 and their stale adjacent comparison comment. Neither is a manuscript dependency.
7. **Minor documentation (R3 M1):** replace README's blanket published-results wording by cited primary literature, including identified preprints. The status of the source evidence must be accurate.
8. **Minor convention (R3 O2):** explicitly declare positive m,n before Appendix B's double-centering definition.
9. **Packaging precision (R3 O1):** supply a short submission README with only portable build instructions and mark the workspace README's checks/process links as repository evidence. The final source archive will use the short README and exclude all internal reports and literature PDFs.
10. **Reproducibility (R3 O3):** record exact inspected LRS and BFPS original-PDF hashes, source URL/version description and theorem/equation locators in an internal source-version manifest. No new mathematical citation or copied literature is needed in the submission archive.

No reported issue is rejected as mathematically false; optional scholarly/documentation improvements above are accepted as useful within the user's requested diligence. Review coverage and finite checks do not establish exhaustive priority or formal proof certification. No accepted finding is major, so the required process does not call for another Stage 4 five-reviewer round after these corrections. The separate whole-manuscript five-reviewer stage remains mandatory.

## Acceptance

Root read the complete separate correction report and full source diff, checked all ten repairs against this adjudication, independently compared all compiled inputs with the clean build, and confirmed Sections 1–5 remain unchanged from stage3-accepted. Root inspected rendered pages 95 and 97 for the new attributions and preserved parameter range; earlier root inspection covered the introduction, scope table, interface, and bibliography. The 104-page isolated build is clean with 39 cited bibliography entries and no missing/unused/duplicate keys. All accepted minor issues are resolved. Stage 4 is accepted, frozen in stage4-accepted/, and the same complete source is frozen in whole-round1/ for five independent complete-manuscript reviews.
