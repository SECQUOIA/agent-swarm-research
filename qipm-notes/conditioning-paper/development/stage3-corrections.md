# Stage 3 correction record

Correction agent: `stage1_fixer`, distinct from `stage3_examples_author`.
Date: 2026-09-07. All five `reviews/stage3-r[1-5].md` reports were read.
The coordinating author accepted two minor findings; no major issue was found.

## Corrections

1. Replaced “barrier parameter” by “central-path parameter” before the
   formula for μ in `07-fractional-sdp.tex`. Audited the same terminology
   across all authored sections: the remaining “barrier parameter” uses
   concern ν or bounded families of ν. No mathematical formula changed.
2. Added the Sremac–Woerdeman–Wolkowicz comparator to the final prior-work
   discussion and bibliography. The paragraph identifies the external path,
   distinguishes iterate spectra from the reduced-Hessian operator, and
   preserves the existing narrow qualified claim about the explicit constants.

## Primary-source checks

Read the [August 2019 manuscript](https://optimization-online.org/wp-content/uploads/2019/08/7334.pdf):
path definition (4.1) and Assumption 4.1 on p.12; (4.2) and Corollary 4.3
on p.13; Theorem 4.4 on p.14; Theorem 4.7 on p.15.

The [publisher record](https://epubs.siam.org/doi/10.1137/19M1289327)
verifies SIOPT 31(1), 812–836 (2021). Also read the matching portions of
the [author-hosted published article](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/errorbndsMP2021.pdf):
pp.824–827, same equation/theorem numbers. The published Theorem 4.4
contains the equivalence cited in the manuscript; the 2019 version states
only its degree-greater-than-one implication. The published version therefore
supplies the citation basis.

The inspected assumption is a bounded, nonempty, nonzero spectrahedron of
positive singularity degree with surjective equality map. Theorem 4.7
concerns separated diagonal blocks after orthogonal transformation; we do
not strengthen it to an unchecked complete Hessian eigenvalue classification.
No theorem duplication or path equivalence is asserted. Downloaded copies
were used only in `/tmp`; the literature corpus was not changed.

## Verification

`make -C conditioning-paper` succeeds. The final log contains no undefined
references/citations, warnings, or overfull/underfull boxes. Only terminology,
prior-work exposition, bibliography and internal records were changed; the
previously reviewed mathematical proofs and constants are unchanged.
Original paper and `central-path-cost/` remain untouched. The stage is ready
for the coordinating author's check without another five-reviewer round.
