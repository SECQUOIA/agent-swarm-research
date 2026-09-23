# Stage 5A concrete movement author record

Authored `sections/11c-concrete-movement.tex` only (plus this audit).
No main, bibliography, or existing section changes were made.

The section has seven pages in an isolated LaTeX build. The build completed
without errors or overfull boxes; unresolved cross-references in that isolated
build are expected and must be checked in the integrated manuscript.

## Source dispositions

- `central-path-cost/sections/06-formulation.tex`: the all-EJA minor theorem is
  referenced through the separately authored movement theorem. Grouped,
  cross-packed, and unweighted norm-tree endpoint and central-path formulas
  are reproduced self-contained and explicitly credited to
  `CentralPathCompanion`. No new-priority claim is made for these formulas.
- `2026-09-04-grouped-ball-short-step-iteration-lower-bound.md`: retained generic
  concave-slack and barrier-height lemmas; whole accurate-set distance from
  every exact central reference; variable-step movement budget and forced
  large chord; exact arc and bounded-chord construction; separate tube
  parameter-increment theorem, including explicit constants and final
  accuracy-to-parameter conversion. The old late-path asymptotic is subsumed
  by the exact profile. The tube proof extends to the identical-source tree
  profiles because it uses only exact speed and gap identities plus standard
  self-concordant comparisons.
- `2026-09-04-psd-packing-geodesic-iteration-lower-bound.md`: retained arbitrary
  cross-packing, off-diagonal completion freedom, the blockwise determinant
  logarithm distance inequality, Hadamard endpoint proof, nonzero central
  reference, heterogeneous group/weight entropy scale, and one-factor
  order-(s+k) specialization. Exact standard parameter H follows from its
  upper gradient bound and central gradient norm tending to H. No unsupported
  universal arbitrary-barrier optimum H is asserted for all cross-packings.
- `2026-09-04-one-factor-psd-packing-short-step-lower-bound.md`: one-factor
  endpoint result is subsumed by the preceding arbitrary cross-packing
  statement and generic movement conversion. A dedicated paragraph extends
  the one-column-per-ball specialization, including the central and tube
  formulas, to real, complex, and quaternionic fields with the conventions
  and exact intrinsic one-column parameter already proved in Section 7.
- `2026-09-04-norm-tree-short-step-iteration-lower-bound.md`: retained positive
  sheet, telescoping, center, finite-accuracy parameter sharpening, uniform
  order, heterogeneous entropy scale, exact central route, and feasible
  chord discretization. Extended explicitly to fixed node weights >=1:
  q_v=omega_v q, W=sum omega, subtree sum Omega_v, and exact speed W(1-W/D).
  This extension is elementary stationary analysis, not an algorithmic
  claim. The new all-objective sharp distance coefficient is being developed
  separately by the main Stage 5A author, using consistent alpha_v notation.
- `2026-09-04-norm-tree-reduced-barrier-parameter.md`: exact unweighted
  parameter is cited through the earlier reviewed theorem; no duplicate
  parameter proof.
- `2026-09-04-hermitian-balance-slice-sharp-frontier.md`, Section 6: retained
  all-EJA exposed rank rho-1, center, full-slice stationary path, exact gap
  relation, exact central arc, lower minor scale (rho-1)/rho, and bounded
  additive difference between arbitrary-path lower bound and central route.
  Distinguishes this fixed standard metric from arbitrary optimal barriers.
- `2026-09-04-spectral-norm-product-sharing.md`, Section 6, and
  `2026-09-04-bounded-face-sharing-sharp-models.md`, end of Section 6: retained
  real/complex spectral determinant contraction, exact reduced parameter,
  exact central profile, sharp leading distance, and literal invariance
  under shared grouping and fixed-identity chordal stars. The vector-row
  specialization covers product balls. Earlier sections contain the cone
  parameter and reduced-oracle identity proofs.

## Independent checks during authorship

- Re-derived weighted tree stationarity along every internal edge, verified
  root and subtree determinant identities, and differentiated the scalar
  profile to obtain the exact squared logarithmic speed.
- Re-derived the arc primitive by y=r/sqrt(1+r^2); checked its coefficient
  at r=0 and its leading logarithmic coefficient at r=1.
- Checked weighted AM--GM powers against the center q_v=omega_v/W and the
  source-gap allocation e_a=epsilon W_a/sum W_a.
- Checked the tube proof's dual norm directions: backward norm transfer
  costs (1-R)^(-1), tube comparison supplies the lower factor 1-rho, and
  the residual bound rho/(1-rho)^2 is a valid conservative bound.
- Verified the balance full-slice gradient is precisely -e/a, including
  off-diagonal moment constraints and all EJA factors; integrated the
  central diagonal metric and checked both logarithmic endpoint constants.
- Verified the spectral singular-value deficit has the correct inequality
  direction, determinant AM--GM exponent, full stationary gradient, and
  identity of the reduced metric under the earlier chordal construction.

## Citation and integration requirements

The only citation key added in this file is the existing
`CentralPathCompanion`. The fixed minor estimate uses
`thm:movement-minor`. Other cross-references point to reviewed existing
Sections 7 and 9. Main author should place this file immediately before
the new all-objective norm-tree distance section. The tube subsection may
be moved to an appendix in final editorial packaging without dropping its
separate per-round parameter conclusion.
