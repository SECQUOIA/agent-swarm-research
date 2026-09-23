# Independent documentation and paper review

Reviewer: the topic 28 source-inventory agent. Date: 2026-09-22.

`COVERAGE.md` maps all C01–C12 obligations to actual declarations in the ten
owned modules. The reviewer read the final consequence, SDP, and boundary
declarations and the earlier closed-system and Shor interfaces. Actual HHC,
the exact block witness, all SDP cases, and the source coordinate count are
present. The map distinguishes implementation and semantic review from
pending final machine checks.

`paper-quadratic-aggregation/sections/91-formal-consequences.tex` accurately
states the closed-system, Shor, and exact SDP equivalences and assumptions.
The unconditional Shor characterization retains strict feasibility. The
AHC-dependent hull equivalences are kept distinct. The section defines the
actual block PSD constraint and explains the proved covariance equivalence;
it does not replace the projection or either hull by a closure.

The shorter Lemma 4 proof matches `strict_shor_alternative` and
`exists_strict_shor_slack`. Open-set separation, rank-one scaling, and strict
feasibility give the claimed contradiction without assuming a closed PSD
image. The SDP paragraph faithfully describes compactness, infeasibility,
attained maxima of both signs, upper-triangular coordinates, and the exact
`n(n+1)+2n` count. It excludes numerical solver certification.

The examples have the exact coefficients in `Boundary.lean`. The first does
not claim the additional BDS-good-aggregation result; the second correctly
states that the Shor projection is proper and strictly larger than the hull.
Their actual HHC proofs use the formal two-form argument and linear-image
factorization as described.

One packaging issue was found in the initial `formal-consequences.tex`: it
included `90-formal-verification.tex`, whose theorem and lemma references
depend on `02-certificate.tex`, without including that certificate section.
This was reported to the coordinator and fixed by including the certificate
section before the core formal account. The reviewer then inspected the
corrected wrapper and the successful nine-page build output. A targeted
scan of the final LaTeX log found no warnings, unresolved references or
citations, or overfull/underfull boxes. No paper packaging issue remains
from this review.

Section 91 is written as the final formal account. Its verification wording
is justified only after successful targeted checks are recorded; this review
does not preempt those results or manuscript stage review. Topic 27's
eleven-module, 178-declaration count remains its historical core count, not
the count for this extension. The full BDS hull theorem, general classical
criteria, additional examples, solvers, and novelty remain excluded.

This review ran no Lean or LaTeX build. Targeted Python checks passed for
local links in all thirteen current package Markdown files, presence of
all twelve claim rows, and occurrence of mapped declaration names in the
owned sources. The reviewer also scanned the coordinator's final LaTeX
log as described above. The actual build commands and final machine-check
results belong in the coordinator's verification record.
