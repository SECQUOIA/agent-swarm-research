# Whole-manuscript round 1 adjudication

The root read all five complete fresh referee reports, their reasoning and
validation limits, after the complete candidate was frozen. Every reviewer read
the whole manuscript independently and recommended acceptance. No reviewer
identified a required major or minor scientific correction.

| Report | Required major | Required minor | Optional suggestion |
|---|---:|---:|---|
| final-review1.md | 0 | 0 | R1-O1: shorten repeated qualifications. |
| final-review2.md | 0 | 0 | None. |
| final-review3.md | 0 | 0 | None. |
| final-review4.md | 0 | 0 | R4-O1: shorten repeated qualifications. |
| final-review5.md | 0 | 0 | R5-O01: illustrate observation-sensitive compression. |

Affirmative A/C/E assessment IDs in the reports record checks, not open findings.
The root agrees with the scientific assessment: proofs handle the essential
zero-weight, lower-dimensional, equality-flow, coordinate-section, and encoding
conditions; prior-work attributions are precise; and computational conclusions
retain the correct numerical, synthetic, and component-relaxation scope.

## Editorial adjudication

R1-O1 and R4-O1 are not adopted. The cited qualifications appear beside distinct
results and in independently readable introduction/conclusion summaries. They
prevent materially different misreadings: extension size versus extension
complexity, rational scaling versus integer normalization, projected coefficients
versus auxiliary multipliers, and a component hull versus a new coupled hull.
Replacing them broadly with cross-references would weaken local clarity. The
reviewers identify no specific inaccurate or dispensable sentence; reviewer 3
also notes the protective role of these repetitions. They remain optional style
preferences, not unresolved defects.

R5-O01 is adopted as a minor accessibility improvement. The existing K4 example
already proves the claim. A two-panel diagram can make its mechanism immediate
without adding a new result: first observe 13 and 14, leave the unobserved edges
12,23,24,34 with one cycle, and select 24 as the one completion edge outside
spanning tree 12,23,34. Adding observation 24 gives precisely the existing example,
whose unobserved edges form that tree and whose residual count is zero.
All arcs are oriented from the smaller vertex to the larger one. Distinct line
styles must remain intelligible in grayscale, and the caption must identify
one fixed observed label j. This is exposition of the already proved individual
completion proposition, not a new dimension or extension-complexity claim.

A separate correction author will add this figure, integrate a short reference,
rebuild the anonymous artifacts, and verify that mathematics/code/data remain
unchanged. The root will inspect the actual figure, source diff, clean build,
and archive manifests before final acceptance. No major issue was found, so
another five-reviewer round is not required by the agreed protocol.

Status: scientific review accepted; final minor presentation correction pending.

## Final acceptance

The separate correction author completed R5-O01 as recorded in
[final-corrections.md](final-corrections.md). The root inspected the complete
source diff and the rendered diagram, including its edge sets, directions,
spanning tree, cycle counts, label scope, and grayscale legend. The root accepted
the correction. All 33 formal results and 33 proofs remain byte-identical to
the reviewed complete candidate; the computational supplement is unchanged.

The root independently extracted and built the final source archive. The build
was clean and its PDF byte-identical to both delivered PDF copies. All archive
payload and input hashes passed, as did anonymity and private-path checks.
The root screened all 50 final pages in rendered contact sheets and inspected
the diagram page separately at higher resolution; no clipping, overlap, or
unintended blank page was found. Evidence is in `final-root-evidence/`.

The final change was the accepted minor illustration only, so the agreed
protocol does not require a repeated five-reviewer round. All accepted findings
are resolved. The manuscript and standalone delivery are accepted internally;
external journal acceptance and exhaustive priority are not implied.

Final status: complete, with no outstanding accepted major or minor issues.
