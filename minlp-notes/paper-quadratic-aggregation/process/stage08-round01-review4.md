# Stage 8, round 1, independent whole-manuscript review 4

Verdict: **clean; no major or minor correction requested.**

I independently read `main.tex`, every included section (00–10), both
appendices, the bibliography, the current coverage map, the package README,
and the formal-verification scope account. I assessed the arguments rather
than relying on earlier review verdicts. My emphasis was consistency across
the three main developments, the local-certificate application, and the
precision of the prior-work and contribution statements.

## Mathematical assessment

- The certificate proof preserves an actual nonzero coefficient pair by
  normalizing in the finitely generated coefficient cone after eliminating
  the constant. Its strict-feasibility hypothesis is used at the right
  point. The AHC condition, the HHC implication, and the quantitative
  alternative have consistent dimensions and quantifiers.
- The closed-system consequences distinguish properness from full hull
  exactness. The Shor proof correctly uses the closure of the cone image,
  its interior, and the quadratic mixing identity. I checked both stated
  nonclosed-projection examples, including the compact four-row example.
  The ordinary-HC, strict-feasibility, and strip examples do demonstrate
  the distinct failures claimed.
- The Gram-fiber proof accounts for odd square size, disconnected
  orthogonal groups, rank-deficient factors, and the exceptional 1-by-1
  case. The fidelity identity supplies concavity in the required argument;
  the hyperplane-image formula has the correct direction of inequality.
- The two-ball system's inertia calculation, unique active rays, strict
  and closed hull formulas, and lifts agree. I checked the two-point
  construction for all r ≥ 2 directly: perpendicularity to b u − a v
  produces the common gamma, the two roots have opposite signs, all three
  strict inequalities hold, and the displayed unequal weights recover the
  original point. The analytic quartic-arc argument justifies the stronger
  countable-strict obstruction and only a finite-weak obstruction, exactly
  as stated.
- The approximation section is consistently restricted to good
  aggregations. The radial correction and the finite-grid pigeonhole
  lower bound have the stated constants. Interior multipliers are allowed
  by the latter proof. The support-gap identity and the one-objective
  separation argument explain why this is not a runtime lower bound.
- The strict PDLC transfer uses genuinely inward positive perturbations,
  excludes the countable bad sublevels and finite dependence parameters,
  deletes globally nonpositive inequalities before strictification, and
  retains the orientation of the limiting negative component. Neither a
  loss of strict validity nor an unsupported closure interchange is hidden
  in the limit. The sharpness example and oriented SOC closure are
  consistent with the theorem's dimension qualifications.
- In Appendix A I checked the estimator identities, positive-definite
  aggregate, tangent x+y ≤ 7/20, diagonal-dominance interval, two affine
  margin formulas, and normalized optimum 1/35. The linear program is an
  exact formulation of the stated restricted selection problem. The
  treatment of equality weights, conditional rows, pure bilinear rows,
  and the comparison with the Shor lift is appropriately limited.
- In Appendix B the normalized cone section really is a compact polygon.
  The selected-facet shift uses nonnegative representations at both ends,
  so the cited PSD-improvement input applies. I checked the ellipsoid
  witnesses, exposed rays, added negative-coordinate rays, and the
  negative-orthant identity. The complementary-cone counterexample
  refutes the proposed constant bound without claiming to refute 2k−2.

## Sources and novelty

I consulted the actual locally available primary texts
`/tmp/quadratic-paper-literature/bdsv2.txt`, `bd.txt`, and `kt.txt`.
In particular:

- BDS v2 Propositions 9.1 and 9.6 support the Appendix B improvement and
  pair-support reduction under the assumptions checked in the manuscript;
  its Proposition 2.22 is correctly credited for the existing 2k bound.
- Blekherman–Dunbar's stated regular nonstrict four-bound has the
  no-points-at-infinity qualification retained by the paper's external
  input. The paper credits the original four-bound and sharpness example
  rather than claiming either as new.
- Kojima–Tunçel Theorem 4.2 actually states the unqualified projection
  equality discussed here, and its proof uses an unqualified sum-of-dual-
  cones identity. The manuscript's compact counterexample and closure
  qualification are therefore substantive, not a misreading of a theorem
  already stated with closure.

I also ran fresh web searches for the HHC certificate conjecture, infinite
HHC aggregation, and strict four-aggregation results. The primary source
results included the BDS author manuscript
<https://www2.isye.gatech.edu/~sdey30/HHC.pdf> and Dunbar's dissertation
<https://etd.library.emory.edu/downloads/2j62s637x?locale=en>. The latter
confirms the stronger regular nonstrict statement already acknowledged by
the manuscript. These searches did not identify a competing resolution
omitted from its qualified novelty claims. This is evidence from a
literature search, not a proof of universal priority.

The introduction and detailed comparisons consistently credit Dines,
Polyak, the existing SDP/QMP convexification theory, squared-fidelity
identities, classical convex duality, and the familiar inverse-square
approximation exponent. The claimed additions are precise. No empirical
solver improvement, general recognition algorithm, or complexity bound is
asserted without proof.

## Presentation and verification claims

The main exposition is self-contained relative to its explicitly stated
classical and published inputs. Definitions of convex certificates versus
good aggregations, original versus lifted variables, and ordinary versus
closed hulls remain consistent throughout. The application and many-row
extensions are sensibly placed in appendices rather than obscuring the
three central results.

The formal scope statement distinguishes the 2n+1 paper characterization
from the larger formal coordinate test and distinguishes the stronger
paper lower constant from the formal lower bound. It expressly excludes
the nonformalized new results. I inspected the portable verification
manifest: it records 909 owned declarations and explicitly distinguishes
imported dependencies, targeted checks, and uninspected CI. I did not
rerun the entire formal project as part of this independent reading.

I checked the final PDF metadata (42 pages), inspected the rendered first
page, and searched the final main build log for warnings, overfull boxes,
and undefined references; none were reported by that search. The title,
abstract, and initial exposition render clearly. Author and affiliation
metadata are intentionally absent and the README identifies that final
author-supplied submission step. The manuscript does not claim external
journal peer review or guaranteed acceptance.

No manuscript edits were made. No project-wide verification or CI checks
were run.
