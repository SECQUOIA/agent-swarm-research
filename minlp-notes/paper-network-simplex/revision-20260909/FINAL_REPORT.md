# Anonymous submission manuscript — final report

The September 9 revision of *Sparse convex hulls for network flows coupled to a
simplex* is complete. The standalone manuscript has 50 pages, with empty author
and affiliation fields. No external submission has been made.

- [Submission PDF](../delivery/submission.pdf)
- [Standalone LaTeX source](../delivery/latex-source.zip)
- [Computational supplement](../delivery/computational-supplement.zip)
- [Build and reproduction instructions](../delivery/README.md)

## Substance of the revision

The introduction now separates established convexification tools from the
paper's structural contributions: observation-sensitive compression, separation
and recovery for specified graph classes, and coefficient obstructions in actual
product coordinates. The literature review checks local sources and additional
primary literature, including recent related work. Novelty statements identify
precise outputs and retain appropriate qualifications. The
[literature audit](literature-audit.md) records comparisons and source evidence.

The mathematical audit examined all 33 formal results and their proofs. It
expanded the three-label positive-circuit classification proof and clarified the
coordinates returned by recovery. A new diagram explains how observing one more
product eliminates a residual cycle coordinate. Assumptions and limits remain
explicit, including rational coefficient scaling, the scope of compression
minimality, and the difference between exact certificates and numerical checks.

The computation section presents supported comparisons without development
chronology or an unsupported runtime counterfactual. It retains negative runtime
results and the limitations of synthetic measurements. The delivery archives
include their own instructions, dependencies, interfaces, and hash manifests;
neither requires internal review records or the repository's literature folder.

## Review and verification

The required process produced 20 independent reports: five after each of three
completed author stages, followed by five fresh reviewers of the complete paper.
The root read and adjudicated every report. Separate correction work resolved
the two distinct required minor findings in stage 1 and the adopted optional
diagram suggestion after the final review. No accepted major finding required
a repeat round. All accepted findings are resolved. The adjudications are
[stage 1](stage1-adjudication.md), [stage 2](stage2-adjudication.md),
[stage 3](stage3-adjudication.md), and [whole manuscript](final-adjudication.md).

Verification combined proof reading, independently written exact checks,
regression tests, comparison with numerical LPs, and complete benchmark
reproduction. The root's full benchmark rerun reproduced 5,754 non-timing values
within the recorded numerical tolerances; canonical measurements were preserved.
Reviewers also reproduced the full study from the extracted supplement.

The final source archive builds cleanly in a separate directory and produces
the delivered PDF byte for byte with the documented toolchain and fixed-time
environment. All 50 pages were screened visually. Archive integrity, anonymous
metadata, and private-path checks passed. The final illustration left all 33
formal results, 33 proofs, code, tables, and computational data unchanged.
The [final validation record](final-validation.json) binds the accepted snapshot,
artifacts, reports, and supporting evidence to their hashes.

Internal acceptance does not establish exhaustive priority or guarantee external
journal acceptance. The manuscript states its mathematical and computational
scope explicitly; no accepted review issue remains open.
