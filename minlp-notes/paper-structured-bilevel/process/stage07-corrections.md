# Stage 7 round 1 corrections

Date: 2026-09-09. Separate correction agent: `stage07_corrections`.
No delegation, review of other stages, or acceptance decision was performed.
All three accepted minor issues in `assessments/stage07-round01.md` are closed.

## Corrections and primary-source checks

**S7-1 — response-exponent lineage.** Section 1 now credits Wu, Gong, Hao
and Liu, *Bilevel Optimization with Lower-Level Uniform Convexity: Theory and
Algorithm*, ICLR 2026. The paragraph preceding Proposition C.4 makes the
comparison precise: their exponent `1/(p-1)` yields `1/P` when `p=P+1` for
an unconstrained uniformly convex follower with a leader-Lipschitz lower
gradient. The present contribution retains that exponent for moving affine
resource right-hand sides with an effective rational constant of polynomial
encoding length. The complete global rational-bit theorem remains distinct.

I read the actual [primary manuscript](https://arxiv.org/abs/2603.00027v1),
model (1), Assumption 3.2(i),(iii), Lemma 4.2 and Appendix B.1, using the
PDF already retrieved by reviewer02 and independently checking the primary
arXiv metadata. The PDF identifies the four authors and ICLR 2026 publication.
Its proof uses the uniform growth inequality, the other optimizer's
optimality, and Lipschitz variation of the lower gradient, then divides by
the response displacement. The manuscript addition imports no stationarity
rate. Although the source cites Bonnans--Shapiro, I did not inspect that
original proposition and have made no assertion about its scope.

**S7-2 — model terminology.** The exact contribution paragraph now says
“number of follower variables.” The statement concerns the total dimension
of one jointly optimizing follower. No mathematical statement changed.

**S7-3 — global first-order lineage.** Section 1 now credits Xiao and Chen,
*Unlocking Global Optimality in Bilevel Optimization: A Pilot Study*,
ICLR 2025, for global convergence of penalty-based bilevel gradient descent
under their joint or blockwise Polyak--Łojasiewicz conditions and accompanying
assumptions, with approximate lower optimality. It distinguishes the present
fixed-structure rational-bit guarantees without suggesting that all
first-order work is limited to stationarity.

I downloaded and read the actual [published paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/4574ac9854d4defe3bf119d07b817084-Paper-Conference.pdf),
including Definition 2, Section 3, Assumption 1 and Theorem 1. Definition 2
compares against all responses within its lower-value tolerance. Theorem 1
requires smoothness, a lower PL condition and the specified penalty
landscape conditions; its blockwise alternative additionally assumes that
the penalty's minimizing lower set is independent of the leader. The concise
comparison therefore includes the accompanying assumptions and imports no
unchecked iteration rate or claim that PL alone is sufficient. Author names,
title and conference year are on the published PDF. The bibliography keeps
that exact PDF target as a descriptive “Published paper” hyperlink: printing
the full URL initially produced loose bibliography spacing, which the shorter
label resolves. The arXiv metadata for 2408.16087 was also checked, but the
bibliography points to the inspected published version. OpenReview access
returned a browser challenge and supplied no result used in the comparison.

The coverage record identifies all three corrections. The qualified novelty
passage still concerns the complete theorem classes and specified outputs;
no new priority claim was introduced.

## Preservation and verification

The baseline is the frozen `stage07-round01` snapshot, manifest SHA256
`8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6`.
Exactly four of its 31 files changed: `sections/01-foundations.tex`,
`appendices/c-quantitative-bounds.tex`, `references.bib`, and
`process/coverage.md`. The other 27 files match byte for byte, including all
executable sources and recorded data. Appendix C from the response-modulus
proposition through its end also matches byte for byte. Only the preceding
literature paragraph changed. All proofs, solver versions, measurements and
their provenance are preserved. No timing rerun is warranted by these prose
and bibliography changes.

Evidence is under `verification/stage07-corrections/`:

- `changes.diff` is the exact four-file unified diff, SHA256
  `3d01a9d4d157110231dd7e7c2534b6962dd567884e9f759dc70d163d668f9e81`.
- `manifest.json` records every before/after changed-file hash, the 17 isolated
  manuscript-input hashes and both primary PDF hashes. Its SHA256 is
  `2e0db5a42bdbeb2a23de2c73866c4caa705029b4db674e1acaadd644e254af78`.
- `standalone/` contains only those 17 manuscript inputs plus locally generated
  build outputs. After deleting its prior build directory, the command
  `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
  completed successfully. The final log has no warnings, undefined citations
  or references, or overfull/underfull boxes. `build.log` preserves the clean
  multipass run. `build-check.json` records the checks and final PDF hash.
- The clean PDF has 78 pages and SHA256
  `a100b85548d1509da4b143818fc507c7dc449520fcb8bb064371dbd10eb843a0`.
  I rendered and inspected affected contribution page 2, related-work pages
  4--5, Appendix C page 68 and bibliography pages 77--78. Text, equations and
  citations fit and are readable; the final bibliography entry naturally
  continues onto page 78. No arbitrary page-count target was imposed.

The downloaded papers are verification evidence, not manuscript dependencies
or submission assets. I did not modify root assessments, STATUS, snapshots,
or any stage 8 record. No edits remain for this correction assignment. Root
verification/acceptance and the separately required full-manuscript review
remain to be completed by the parent process.
