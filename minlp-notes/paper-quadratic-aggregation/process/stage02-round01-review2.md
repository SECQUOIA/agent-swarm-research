# Stage 2, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

I independently reviewed the complete stage 2 proof and formal account,
including the classical-result attribution and the precise conjecture being
resolved. I did not read the other current reviewers' reports, edit manuscript
source, run Lean, or run broad repository checks.

## Mathematical assessment

The main proof is complete and its treatment of the potentially vanishing
coefficient pair is sound.

- AHC's unbounded-level definition is equivalent to the increasing-sequence
  definition by the stated recursive selection. HHC implies it for every
  nonzero normal. The proof only needs the positive unbounded levels along
  one supporting normal, as the manuscript explicitly explains.
- The common-negative-direction lemma is valid uniformly across finitely
  many constraints. The supporting-halfspace argument legitimately uses
  openness of the ordinary convex hull; it does not confuse that hull with
  its closure. Hyperplane exclusion correctly covers `t=0` and both signs
  of nonzero `t`.
- The image/negative-orthant separation requires no closedness of the image.
  Coordinatewise unboundedness of the negative orthant proves nonnegative
  separating coefficients, and zero in the image forces separation level
  zero. Normalization is legitimate because the separator is nonzero.
- Finite-cone closedness is proved using a minimal-support representation
  and finitely many linearly independent subfamilies. This avoids the false
  general assertion that every linear image of a closed cone is closed.
- Strict feasibility yields the required **upper** bound on the constant.
  The constant's nonnegative square coefficient ensures replacement in the
  sweep inequality has the correct direction. The original sweep inequality
  at the nonzero normal rules out a zero nonconstant coefficient pair before
  normalization.
- Normalized pairs lie in the closed coefficient cone and on the unit
  sphere, hence have a unit limit in that cone. Linearity of the substituted
  constant bound makes both perturbation terms vanish for each fixed test
  vector. One common coefficient subsequence suffices for all test vectors.
  The limit quadratic part is PSD, and actual nonnegative weights follow
  from cone membership. No bounded rescaled weights or bounded original
  constant-to-pair ratio is assumed.
- The easy implication establishes properness for both a nonzero PSD
  quadratic part and a zero quadratic part with nonzero slope. It remains
  valid for the empty feasible set, so the stated absence of either
  hypothesis in this direction is justified.
- The single-constraint discussion covers negative curvature, nonconstant
  convex quadratics or affine functions, and negative constants under the
  theorem's nonemptiness setting. No overlooked low-dimensional restriction
  appears in the main theorem.

The quantitative alternative is also correct. The uniform cone lemma needs
closedness and positive scaling, not convexity. The product-cone distance
identity follows from orthogonal diagonalization and leaves the linear
component unchanged. Combining its upper eigenvalue estimate with the
positive cone-separation bound forces a strictly negative minimum
eigenvalue for every nonzero coefficient pair. Discarding the negative
constant term gives precisely the displayed sweep-level bound. Finally,
the separate simplex subsequence yields a nonzero trivial convex
aggregation whose constant is strictly negative, so the bound applies
eventually and contradicts unbounded levels. This completes the older
argument rather than merely sketching its essential missing step.

## Attribution and novelty

The theorem resolves exactly the BDS v2 Conjecture 3.3 certificate question
checked in stage 1, while extending its standing dimension conventions and
replacing HHC by AHC. The previously settled no-PSD-multiplier and diagonal
cases remain credited in the setting. The new proof handles the case in
which a simplex limit could be a negative constant. The manuscript does
not present ordinary separation, finite-cone closedness, cone compactness,
the two-form case, or the general SDP/aggregation relationship as new.

The stage makes no additional literature-priority assertion beyond the
precise conjecture resolution. It does not claim that the weaker hypothesis
has already been proved strictly weaker, or that convex certificates recover
the whole hull. Those distinctions are consistent with the later-stage
coverage plan. I found no new citation or source-version mismatch.

## Formal correspondence and scope

The formal headline has the original strict feasible set and ordinary
`convexHull`, with only nonemptiness and `AsymptoticHC` as hypotheses;
the HHC specialization invokes the proved implication. The actual model
has symmetric real matrices, real vectors and constants, nonnegative
nonzero certificate weights, PSD quadratic aggregation, and a nonzero
quadratic or linear coefficient. Thus it matches the manuscript rather
than a weaker surrogate statement.

The code derives sweep weights from the geometric hypotheses, eliminates
the constant using the strict feasible point, takes a unit limit in the
actual coefficient cone, and recovers genuine weights. Closedness and
the limiting certificate are proved internally rather than supplied as
headline assumptions. Its choice of an entrywise maximum matrix norm and
product maximum norm does not affect the finite-dimensional compactness
argument. The separately checked cone-geometry result matches the general
uniform-distance lemma; the manuscript correctly excludes the spectral
formula and quantitative alternative from formal coverage.

The 11-module / 178-declaration checks, pinned toolchain, allowed axiom
set, and kernel-replay limits are accurately bounded by the coordinator's
record and manifest. The section does not imply verification of examples,
consequences, the frontier result, literature claims, or the whole paper.
The separate wrapper reuses the proof and account consistently. The pending
portable formal-source supplement is explicitly assigned to stage 5 in
`FORMAL-VERIFICATION.md`, so it is not misrepresented as already packaged.

## Checks actually performed

- Read the author report, current setting and full certificate section,
  formal section, wrappers, formal packaging note, current bibliography,
  coverage plan, coordinator formal-check record, and verification manifest.
- Read the actual Lean `Model`, `Headline`, `DefinitionsSequence`,
  `SweepBounds`, `LimitCompactness`, `Coefficients`, and `ConeGeometry`
  sources, plus the final unbounded-certificate theorem in `Hyperplanes`.
  These inspections checked semantic correspondence and the delicate proof
  interfaces; they were not independent executions of Lean.
- Re-derived the sign changes, nonzero normalization argument, coefficient
  limit, distance identity, and quantitative constant directly from the
  manuscript rather than treating a successful formal build as coverage
  of the unformalized alternative proof.
- Used a targeted `rg` scan of both current LaTeX logs for `Warning`,
  `Overfull`, `Underfull`, and `undefined`: no matches. I did not rerun the
  already passing builds or the coordinator's targeted Lean checks.
- Reused the direct predecessor's primary-text/version comparison already
  performed in my stage 1 review. No new external literature claim was
  introduced in stage 2 that required a new online lookup.

This verdict accepts stage 2 only. It does not pre-approve any later
consequence, application, frontier construction, or submission packaging.
