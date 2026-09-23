# Stage 5, round 1 — root assessment

The root read all five independent review reports in full, the completed
stage author report, the full new section and appendix, and the relevant
canonical and note-only sources. The reviewed 13-file snapshot is
`process/snapshots/stage05-round01`; manifest SHA256:
`c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5`.

## Disposition

All five reviewers found no major mathematical issue. Reviewers 01 and 03
requested no correction. Reviewer 02 identified a citation-locator issue;
reviewer 04 identified a small source-coverage omission; reviewer 05 suggested
keeping one proposition statement together. Root accepts all three as minor
corrections. No major issue requires a repeat five-reviewer round.

| ID | Review | Root decision and required correction |
| --- | --- | --- |
| S5-1 | R02-S05-01 | Accepted minor. In section 05's first Sugishita–Carvalho citation, use Theorem 1 and Section 4 (PDF numbering). Root visually inspected the original v2 PDF page 3 retained by reviewer02 and confirmed Theorem 1. The current 2.1 is the HTML rendering's numbering; attribution is substantively correct. No bibliography change is needed. |
| S5-2 | R04 coverage finding | Accepted minor. Add the positive-objective multiplicative consequence immediately after the dense constant-gap proof and record its source/label in coverage.md. Root read investigation Section 8 and checked both inequalities. With H>=0 and optimum 0 versus >=2, 1+H excludes a ratio strictly below 3. With s=n+m, 1+2^s H has yes optimum 1 and no optimum >=1+2^(s+1); polynomial input length in s makes every fixed polynomial ratio smaller than the gap eventually. Handle the finitely many smaller source sizes separately. Require an exactly bilevel-feasible output, retain polynomial binary encoding, and state that scaling loses bounded upper coefficients and does not prove strong hardness or a result for approximate followers. This is an elementary consequence of the already reviewed theorem, not a new hardness premise. |
| S5-3 | R05 optional pagination | Accepted minor for readability. Keep the complete short statement of prop:single-power-output together. Root viewed PDF pages 43–44 and confirmed the split separates its anchor/sparse-upper qualifications from the two examples. Use a local robust pagination adjustment, as in earlier accepted stages; later final pagination will still be checked. |

No reviewer criticism is rejected. No known mathematical correction remains
outside this list. All later-stage computation/contact and synthesis tasks
remain assigned; their absence is not treated as current acceptance.

## Independent assessment of the substantive results

Root agrees with the five proof audits for reasons recorded in
`stage05-root-reading.md`, not because of their acceptance labels. In particular,
the dense relative-coordinate error estimate controls the small upper readout;
the conditioned oracle's rational denominator bound and numerical K dependence
are compatible; the bounded-core closure step is sound; the padded path proof
uses strict full-cube optimality by containment; and the single-power lower
bounds concern explicit rational output length. Primary attributions and
finite exact diagnostics support their specified scope, not priority or
production solver superiority.

## Gate status

Pending separate correction of S5-1 through S5-3 and root verification of the
complete diff and build. Stage 6 must not start until that correction is
accepted. The final complete manuscript will still receive five independent
whole-manuscript reviews under the user's process.

## Correction verification and acceptance

Root read the full separate correction report and both complete file diffs.
S5-1 uses the visually verified PDF numbering. S5-2 contains both full
positive-objective gap arguments, the finite-small-source-size qualification,
and the exact-feasibility/coefficient restrictions; root independently checked
the inequalities and polynomial encoding. S5-3 uses a local samepage block
without changing the proposition. The insertion also correctly replaces the
newly ambiguous phrase “last proof” with the dense theorem reference.

Root verified all thirteen frozen hashes and confirmed that only the section
and coverage file changed before the acceptance-status update. A fresh LIVE
latexmk build succeeded at 63 pages, with no final warnings, undefined
references/citations or box warnings. All accepted issues are closed.
Stage 5 is accepted; no major issue requires a repeat round.
