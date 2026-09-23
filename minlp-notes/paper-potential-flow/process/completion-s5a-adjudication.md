# Stage 5a adjudication

The lead read the entire frozen section, all five independent reports in full, the complete author report, the new diagnostic, and all nine check outputs. All five reviewers found no major issue and explicitly accepted the new fixed-measurement extension to independent polynomial-law cycle polytopes with local capacities. The lead agrees. Reviewers remained independent, did not edit the manuscript, and checked the frozen hash before and after their reviews.

## Accepted corrections

1. **Minor: absolute coefficients in scalar-value refinement** (r1, r3, r4, r5). In the proof of `thm:a-design-independent`, the additive value stopping rule must use `sum_C |gamma_C| width(I_C)`, not signed coefficients times widths. This is a local arithmetic-bound omission; the theorem, exact scenario construction, and polynomial refinement cost remain unchanged. Give an explicit valid bound and say how rational enclosure representatives are evaluated.
2. **Minor: zero nominations in the independent-cycle proof** (r1, r2, r5). The root theorem requires a nontrivial bracket, so dispatch `B=0` before invoking it. All flows and reference circulations are then zero; test capacities directly and obtain rational admissible parameter points by LP. This also handles the connected edgeless case. No additional structural argument is needed.
3. **Minor source improvement** (r2, r3, r4; lead verified). The full Ferrez–Fukuda–Liebling author manuscript is available at `https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf`. The lead checked its April 29, 2004 revision date and read Section 3, PDF pages 4–6. Update the bibliography's stale access comment and URL, retain the published 2005 metadata, and identify the author version. The current restrained predecessor statement is correct and need not be expanded into an unverified firstness claim.

There are no rejected substantive criticisms. Original Mignotte access limitations are transparently recorded; the exact factor inequality was checked in a primary research restatement and its use was verified directly. BPR's original univariate isolation passage was additionally inspected in rendered/OCR form by reviewers. These source limits do not create an unsupported theorem in the manuscript.

All accepted changes are minor and do not require a repeated five-reviewer round unless correction or lead verification reveals a major issue. A distinct correction agent must apply every accepted repair before acceptance.

Status: accepted. The separate correction agent applied all three repairs. The lead read the full fix report, inspected the actual proof and bibliography edits, and verified all 15 current input hashes against the clean Paper A build record, including zero overfull boxes. No correction introduced a major issue; no repeat round is required. Stage 5b may now begin.
