# Root validation of the integrated manuscript

Initial full-manuscript validation, 2026-09-08. This records the root's
checks alongside the five independent final reviews; it does not replace
their assessment or certify the review cycle complete.

- Read the completed abstract, introduction, conclusion, figure captions,
  README, figure script and bibliography additions. Before author handoff,
  requested and verified two precision repairs: a lower bound applies to
  every admissible sequence while a matching upper bound concerns an
  available sequence; the decrement transfer requires `0<=beta<1/2`.
- Independently evaluated the stable metric-profile formula against
  adaptive integration of its velocity at 112 points from -30 to 80.
  Maximum relative discrepancy was approximately 6.78e-12. This checks
  numerical evaluation, not a global theorem by sampling.
- Independently reopened the primary ADLNV2025 text and the AGV2022
  record, and read the published ABGJ2018 introduction and Theorems A/B
  at printed pages 140–142. Requested inclusion of that foundational
  tropical lower-bound source; verified its publication metadata against
  the author-hosted primary PDF. The final introduction distinguishes its
  neighborhood iteration result from this paper's metric ratio.
- Rendered all 50 pages and inspected every page in five contact sheets.
  Inspected pages 1, 4, 34, 35, 42 and 49 at higher resolution for abstract,
  figure labels and captions, the movement comparison table, long rational
  expressions, and bibliography. Found no clipping, overlapping text,
  unreadable labels, or malformed expressions. The ordinary figure-only
  page and final short bibliography page are acceptable float/pagination
  choices, not correctness or submission blockers.
- Verified all final PDF fonts are embedded, including TrueType fonts
  in the vector figures; no Type3 bitmap fonts are present.
- Ran the new integrated `conda run -n qipm --live-stream make verify`
  target successfully. Exact Fraction certificates and every numerical
  diagnostic passed: weighted profiles/order checks, scalar inequalities,
  96 independently solved radial centers, primal–dual KKT/progress,
  arbitrary auxiliary fibers, packed Hessians, integer dimension bound,
  and linked-tree identities. The maximum reported radial tangent
  discrepancy was 1.23e-9. These diagnostics accompany complete proofs.
- The synthesis author separately verified a fresh build containing only
  manuscript sources and included figures. Its log and the integrated log
  are clean. Root has not repeated that unchanged standalone build.

At this point five final independent reports are pending. Their findings
must be assessed, all valid issues repaired by a different agent, and any
valid major issue followed by another five-reviewer round.

## Root finding for the final repair pass

Minor precision issue in the introduction's second paragraph: saying
the minimum number of moves is comparable to metric distance should
explicitly allow integer rounding. At arbitrarily small positive distance
one still needs at least one move, so a purely multiplicative statement
would fail. Add “up to integer rounding” or the equivalent qualification.
The actual foundation theorem already contains the correct ceiling;
no proof or bound changes are needed.

## Resolution after the five final reviews

The pending-review statements above record the earlier validation state.
All five final round-1 reports are now complete; root read and assessed
each and found no valid major issue. Separate repair agent `stage1_fixer`
resolved the root's rounding finding and all other accepted minor findings:
the abstract and introductory spectral result now specify the standard
logarithmic/log-determinant barriers; PDF title, author, subject, and
keywords are populated; and the introduction and bibliography include
the precisely scoped Dadush–Ma–Natura–Végh STOC2026 comparison.
The literature ledger records primary-source support and access history.

Final repair validation: the qipm `make` build succeeded and produced
49 pages. Its final log contains no warnings, undefined references or
citations, or overfull/underfull boxes. `pdfinfo` confirms the exact title
“The Cost of Following the Central Path,” author “Sergey Gusev,” and
the requested subject and keywords. The new bibliography entry resolves
in `main.bbl`. The only removed artifact was the generated
`scripts/__pycache__` inside this paper folder; `.gitignore` now excludes
such caches. Mathematical scripts and figures were unchanged and their
earlier passing checks were not repeated. The completed repair is ready
for root's final inspection before delivery.

## Final root inspection and delivery

Root inspected every repaired passage, the new primary-source comparison
and bibliography entry, the populated PDF metadata, and the clean final
log. Re-rendered and inspected all 49 pages after the changed pagination;
no clipping, overlap, malformed figure/table, or pagination defect was
found. All accepted issues are resolved. The staged review process and
full-manuscript review are complete, with no unresolved mathematical or
production issue identified by these checks. The final deliverable is
`main.pdf` with its standalone TeX, bibliography, figures, data, scripts,
README, and review record in this directory.
