# Stage 6b, round 1, independent reviewer 5

Date: 2026-09-22. Recommendation: **pass**. I found no major or minor issue
requiring a change. I did not read another reviewer's current report and
made no manuscript changes.

## Mathematical audit

I independently checked the directional facet proof. Strict feasibility
excludes every nonzero nonnegative combination evaluating to zero at the
fixed feasible lift; this establishes the pointed cone and compact polygon
section. Its dimension is three because the generators span the stated
space. Retaining its extreme generators preserves both the strict feasible
set and the cone of available matrices. Restriction of a positive definite
combination to each homogeneous hyperplane stays positive definite; its
dimension is at least three. Thus the three-form convexity result supplies
HHC for a basis, and taking a linear image supplies HHC for all rows.

The exit parameter is well-defined because a positive definite direction
cannot belong to the coefficient cone. Facets with nonnegative direction
evaluation cannot obstruct the forward move. At the minimum over the
negative facets, the improved matrix remains in the cone and reaches a
selected facet. The possibility that the improved matrix vanishes is
correctly excluded by the one-negative-eigenvalue condition, including the
zero-step case. Nonnegative representations of the original and improved
matrices give exactly the signed coefficient increment required by PSD
improvement. The direction of domination and both inclusions in the
resulting hull equality are correct. Pair-support reduction is explicitly
relative to the full feasible set. The argument does not replace it by a
two-row subsystem. Perturbing a PSD matrix outside the negative coefficient
cone by a small positive definite matrix correctly leaves one facet
functional positive, yielding the conditional count.

For the ellipsoid family, I checked the determinant sign, the full
three-dimensional span, positive definiteness of each leading part, and the
boundary witness identity. Each witness has precisely one zero original
row and every other row strictly negative. This establishes indispensability
of that exact multiplier ray for strict descriptions, even infinite ones.
It also exposes the corresponding matrix ray. For finite weak descriptions,
local strict slack plus a radial outward perturbation proves necessity;
shrinking toward the strictly feasible origin proves the matching weak
representation. The restriction to finite weak families is essential and
is stated correctly.

For the augmented construction, both added rows are strictly negative at
every old witness. The midpoint perturbation proves the convex hull remains
U despite the strict feasible set changing. The constant coefficients show
that the two new rays are extreme, and witness exposure preserves the m
old extreme rays, giving exactly k=m+2. I checked the displayed identity
producing -E3 and the characterization of PSD matrices in this diagonal
three-dimensional span. Consequently the complementary cone inclusion is
correct. The same witnesses retain exactly the required m old aggregation
rays, while those m rows provide the matching good description. The weak
set is unchanged, compact, has the asserted interior and regularity, and
has no nonzero feasible direction at infinity. Thus the counterexample
really does retain the relevant closed-set geometric hypotheses.

The conclusion is appropriately limited: this refutes a constant two-cut
extension to arbitrary polyhedral cones, while its k-2 lower bound does
not refute an unconditional 2k-2 upper bound. The final cautions about
subsystem hull intersections and addition of inertia-constrained matrices
are correct. The inertia example has one negative eigenvalue for each
summand and two for the sum.

## Literature and exposition

I inspected the local primary BDS v2 passages containing Proposition 2.22,
Proposition 9.1 and Proposition 9.6, including their proofs. The cited
hypotheses match their uses. The manuscript relies only on the endpoint
reduction conclusion, not the unnecessary determinant-root assertion.
I freshly opened the [BDS v2 primary page](https://arxiv.org/html/2210.01722v2)
and verified its version identifier. I also inspected the local BD v1
Propositions 8.6 and 8.10 and their proofs and freshly opened the
[BD v1 primary page](https://arxiv.org/html/2405.18282v1).
The appendix accurately credits the prior facet method and limits the
three-generator antecedent to its actual scope. It does not mistake an
unsuccessful literature search for proof of novelty. Its modest framing
as supporting observations and examples is appropriate.

The distinctions among coefficient matrices, multipliers, strict sets,
ordinary hulls, and finite weak descriptions are sufficiently explicit.
The change from U to V is acknowledged and proved harmless for the hull;
there is no silent identification of the two feasible sets. I found no
missing hypothesis or ambiguous bound needing correction.

## Actual targeted checks

- Read the entire appendix, stage author report, stage literature report,
  snapshot, source research note, and exact-check script.
- Ran `python3 paper-quadratic-aggregation/supplement/check_three_dimensional_span.py`.
  It passed the polynomial coefficient identities and 1,235 exact rational
  witness evaluations. I inspected the code; these finite checks are
  correctly presented as supplements to the universal proofs.
- Recomputed SHA-256 hashes for all 12 files listed in
  `stage06b-author-snapshot.json`; all matched.
- Read the primary-source passages specified above and freshly opened both
  version-specific primary pages.

No project-wide checks, CI inspection, Lean rerun, or manuscript edit was
performed. I did not repeat the author's LaTeX build because the audited
source snapshot matched and this review made no source changes.
