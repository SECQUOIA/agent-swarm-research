# Geometry and lower-bound review

The review target was the complete uncommitted `paper-exact-penalties/`
folder after its first six-page build: source, PDF, bibliography, coverage
map, and exact checks. The repository baseline was
`fe439d5c885e3efd7f9fc4b1392eaffca7cfcf6f`. The lead supplied the following
independent review outcomes; the raw Claude report is retained in
`evidence/reviews/stage1-claude.txt` relative to this paper folder.

| Review | Scope and outcome |
| --- | --- |
| Codex `s1_review_whole` | Full target, proofs, PDF and source coverage. No findings; reran the exact script and rendered all six pages. |
| Codex `s1_review_geometry` | Section 2 and Appendix A. No substantive finding; suggested naming the unaffected source Theorem 14. |
| Codex `s1_review_lower` | Independently rederived Section 3 and read/reran the exact script. No findings. |
| Codex `s1_review_sources` | Five retained primary citations, coverage and metadata. No findings. |
| Codex `s1_review_clarity` | Reader precision across the target and PDF. One minor finding: the numerator bit statement needs “at least.” |
| Fresh Claude session | One Fable whole-target review and three Opus focused reviews, followed by lead verification within that session. No blocking mathematical error; seven positioning, citation and packaging findings plus minor wording issues. |

The task lead accepted the source Example 13 correction, the more precise
statement of Theorem 14, the growing-dimension qualification, the prior
nonconvex zero-multiplier overlap, the Beck locator correction, published
bibliographic metadata with inspected versions retained, accurate script
labels/counting, and coverage paths and heading locators. These are now
incorporated. The minor encoding wording, denominator notation, complete
constraint-index count, convex-slice Slater qualification and abstract
convexity description were also corrected. No theorem or proof changed.

The lead rejected the suggestion to remove calibration from the title:
calibration is part of the authorized complete manuscript, and its theorem
section is deliberately outside this first review boundary. The title is
therefore retained. Additional historical citations for each elementary
supporting proof were not judged necessary; the manuscript already identifies
the geometry as classical and cites the directly relevant primary work.

The reviewer-created images were moved from `/tmp/s1-review-whole-*.png`
into `evidence/reviews/stage1-rendered/` and are ignored by Git. No other
external files were moved or removed. The raw Claude report is unchanged.
Reviews did not certify exhaustive priority, rerun Lean, inspect CI, or
perform project-wide verification. The accepted changes were localized
clarifications and were checked directly by rebuilding and rerunning the
modified exact script; the validation record gives the results.
