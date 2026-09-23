# Stage 4B author handoff

Stage4A was complete before this author stage began. Stage4B was written
by `/root/stage4b_author` with four bounded helpers on disjoint files:

- `whole_rows`: 09a-whole-rows.tex, arbitrary-body whole rows, minimum
  dimension, normalized-base and recession-height theorems.
- stage author: 09b-face-sharing.tex, local/global face sharing and sharp
  shared-square models.
- `balance`: 09c-balance-slices.tex, all-EJA connected balance sections and
  exact count/dimension/barrier consequences.
- `lp_power`: 09d-lp-power.tex, norm-ball frontiers and newly developed
  weighted-geometric-mean/general Euclidean-output curvature bound.
- `spectral_chordal`: 09e-spectral-chordal.tex, spectral contact/whole-row
  bounds, classical barriers with exact arbitrary-barrier lower certificates,
  completion cones and identical reduced geometries.

All five files are integrated in main.tex before the single appendix
marker. New bibliography entries are merged without duplicate keys.
Detailed per-source dispositions were appended to source-map.md, including
previous Stage2 deferrals, the extra bounded-face-sharing-sharp-models
source, and curvature-saturation-nonrigidity. Each helper's audit records
primary-source checks, exact mathematical scope, and proof reconstruction.
The stage author read every helper draft independently and checked its
proofs, formulas and cross-section dependencies before integration.

## Development beyond transcription

- General Euclidean power-cone curvature capacity is proved as m+k-2 via a
  compact affine section and the positive weighted-variance/spherical
  Hessian. The scalar m-1 bound is compared carefully to Wang and
  Blanco–Martínez-Antón, with no scalar priority claim or denominator-bound
  extrapolation.
- The N=2 p-ball/power-cone exception now has a full projective local
  boundary proof, including the separate Lorentz-versus-flat-axis case.
- The long normalization source's abstract epigraph construction is
  replaced by the already verified escaping PSD disk, whose exact recession
  ray now disproves any projection-preserving affine normalization.
- Heterogeneous whole-row grouping has a complete strong NP-completeness
  reduction with explicit input-size scope.
- Ambient shared spectral parameter optimality is proved for arbitrary
  coupled barriers with explicit tensorized recession certificates; it is
  not inferred merely by adding factorwise optima or using an LH-only bound.
- The balance proof treats Albert idempotent coordinates directly and keeps
  the alternate classical moment of a different signature distinct.
- A short rejected-log example from the long connected-extremes note is
  retained with exact derivatives 13/4 and 25; its verification is elementary
  and independent of the positive barrier-optimality theorem.

## Corrections to source metadata and scope

Krokhmal–Soberanis DOI10.1016/j.ejor.2009.03.053 belongs to
*Risk optimization with p-order conic constraints: A linear programming
approach*, EJOR201(3)(2010)653–671. The source note had a different title.
Optimization Online PDF7776 is the old-titled *Towards practical generic
conic optimization*, whose final publication is Coey–Kapelevich–Vielma,
*Solving Natural Conic Formulations with Hypatia.jl*, IJOC34(5)(2022)
2686–2699, DOI10.1287/ijoc.2022.1202. It is not their separate
*Performance enhancements* paper. Coey's 2022 thesis explicitly verifies
the complex spectral barrier formula. MOSEK's verified version and access
date are retained; its year is marked n.d. rather than invented.

No exact split-row interpolation at face cap f>1 is asserted. No
unrestricted capped PSD-lift frontier is inferred. Global C1 selection
results remain distinct from arbitrary definable lifts. Ambient arbitrary
barrier parameters, restricted standard barriers and intrinsic slice
parameters are not conflated. The matrix barriers and completion formulas
are attributed as classical. Comparisons between matched-dimension balance
families concern different bodies.

## Explicit remaining routing

Stage4C owns nonsymmetric barrier premiums, characteristic functions,
conditioned approximation and compiler boundaries. Stage5 owns canonical
balance central-path formulas, the distinct spectral bounded-Dikin movement
theorem, and the shared-model movement consequences. Exact formulas and
source obligations are recorded in helper audits and were sent to root.
No stage is silently marked complete for a deferred result.

## Validation

`conda run -n qipm --live-stream make -C conic-lift-complexity` succeeds.
The integrated manuscript is 80 pages. Final main.log and main.blg contain
no warnings, overfull/underfull boxes, unresolved citations or references,
or multiply defined labels. A direct label/key audit also found no duplicate
labels, duplicate bibliography keys, or unresolved reference targets.
Build output is saved in stage4b-build.log; final clean log is copied to
stage4b-final-latex.log. Existing source notes, literature packages, other
manuscripts and formal/ were not modified. No packages were installed.

This is the author-stage completion only. The mandatory five independent
reviewers, root assessment, separate fixing agent and any repeated major-
issue review cycle remain to be performed by root before closing Stage4B.

## Revision after the first five independent reviews

The separate correction author implemented root's accepted findings;
see `stage4b-assessment.md` and `stage4b-corrections.md`. In particular,
the source-level total sharing bound is strengthened to m_i-2, excluding
the previously discussed one-unit sharing bonus. The full-row product-ball
bound is further strengthened to R>=kp+1 under a strict cap by aggregating
dual maps and applying the joint-cover theorem. Uniform face budgets are
combined with these bounds explicitly. The spectral result now states the
stronger unweighted capacity budget. Dimension caps are explicitly integer.
This scientific revision requires a second five-reviewer pass before the
stage can be closed; the original validation above describes the author
handoff, while the correction log records the revised build.
