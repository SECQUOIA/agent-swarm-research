# Stage 3 adjudication and acceptance

The root read the full author report, source diff, package builder and delivery
documentation, all five complete independent reports, and the recorded evidence.
The frozen stage contains 102 files; every frozen and corresponding active hash
matched at acceptance. No manuscript or archive correction is required.

| Report | Major | Minor | Root disposition |
|---|---:|---:|---|
| stage3-review1.md | 0 | 0 | Accept standalone reading, scope preservation, and delivery checks. |
| stage3-review2.md | 0 | 0 | Accept computational contracts and fair-baseline analysis. |
| stage3-review3.md | 0 | 0 | Accept complete input closure and independently rebuilt artifacts. |
| stage3-review4.md | 0 | 0 | Accept numerical narrative and full extracted-study reproduction. |
| stage3-review5.md | 0 | 0 | Accept fresh-environment installation and independent full reproduction. |

The F0/no-defect numbered entries are affirmative checks, not open issues. No
reviewer requested an optional edit. There are no valid findings to assign to
a correction author, and no major issue requiring another Stage 3 review round.

The stage preserves all 66 formal environments and every accepted mathematical
section. Its prose explains current comparators without omitted historical
measurements, retains unfavorable runtime outcomes, and distinguishes exact
certificates from numerical answers. Reviewer 2's deliberately tiny violation
illustrates that the general numerical status must not be treated as exact
membership; the existing text and API state precisely that limitation. It is
not an unreported certification defect.

The delivery source builds without repository inputs, and both extracted ZIPs
support their documented commands. Reviewers independently checked payload and
artifact hashes, main.pdf equality, anonymous metadata, and same-toolchain byte
reproducibility. Reviewer 5 installed pinned dependencies in a fresh environment
and exercised the standard-library API without site packages. Reviewers 4 and 5
ran the complete study from actual extracted supplements, in addition to the
root's isolated accepted-source full run. Their 5,750 case-record comparisons
and the root's 5,754 comparisons (also including top-level protocol leaves)
agree on unchanged non-timing results. Timing variability is not interpreted as
a scientific discrepancy or a new performance claim.

The root also screened the layout of all fifty pages and inspected selected
computational pages in detail; see stage3-root-reading.md and visual-check.json.
No concrete presentation defect emerged. Finite executable checks supplement
the mathematical audit and do not establish arbitrary-instance correctness.

Stage 3 is accepted. The standalone candidate now proceeds to five fresh,
independent whole-manuscript reviews before final acceptance. Routine review-status
updates to README/PROCESS/STATUS follow this adjudication; manuscript content,
code, canonical measurements and delivery artifacts remain unchanged.
