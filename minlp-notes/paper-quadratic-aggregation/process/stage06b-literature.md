# Stage 6b literature and scope audit

Date: 2026-09-22. This audit covers the supplementary development for many
constraints in a three-dimensional homogeneous matrix span.

## Primary sources inspected

Read the relevant passages of the local BDS primary author manuscript,
then checked the downloaded arXiv v2 PDF/extraction and freshly opened
[BDS arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2).
The correct version-specific locators are Proposition **2.22** for the
three-dimensional-span `2m` bound, Proposition 9.1 for positive semidefinite
improvement, and Proposition 9.6 for pair-support endpoint reduction.
The repository note and its earlier independent review use Proposition
2.21, correctly for the earlier v1 author PDF but not for the paper's
chosen v2. The appendix consistently uses v2.

BDS already works with the pointed three-dimensional matrix cone, whose
facets have two extreme generators, and already counts two good cuts per
facet. Proposition 9.6 uses goodness relative to the *full* original
feasible set. This distinction is retained in the proof. The appendix
does not import a claim that hull commutes with subsystem intersection.
It uses only the two-endpoint conclusion, not any additional claim about
which determinant roots identify those endpoints.

The known three-form convexity theorem used to establish HHC is the same
Polyak (1998), Theorem 2.1, already inspected and cited in the main text:
three forms on a real space of dimension at least three with a signed
positive definite combination have a convex joint image. Restriction to
each homogeneous hyperplane preserves that definite combination, and the
original many-form image is a linear image of the three basis-form image.
Thus the BDS strict full-hull theorem applies with all its hypotheses.

Freshly opened [BD arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1)
and read the locally downloaded Section 8 text. Proposition 8.6 is the
three-generator antecedent of the directional exit argument. Proposition
8.10 is a two-bound for a three-generator problem under its no-infinity
and regularity hypotheses. Its proof does not establish the corresponding
statement for arbitrary many-ray polyhedral cones. The manuscript now
gives an explicit counterexample to that proposed extension, while
preserving all the corresponding closed-set geometric hypotheses.

Searches for `"quadratic" "aggregations" "2m" "span"` and
`"quadratic aggregations" "polyhedral cone" "four"` retrieved the BDS
author manuscript, related thesis material repeating the facet argument,
and irrelevant results. No search absence is treated as proof of priority.
The manuscript makes no claim of a first general polyhedral-cone theorem
or of an optimal many-generator count. No new bibliography entry is
needed: the primary antecedents are already cited in the manuscript.

## Independent development and exact boundary

Read the current research note and its independent review, then independently
verified the coordinator's augmented-ellipsoid construction recorded in
`stage06b-root-development.md`. Adding the two negative coordinate-square
rows changes the strict feasible set, preserves its ordinary hull, and
leaves its weak feasible set unchanged. The new cone has exactly `m+2`
extreme rays and contains the negative of the entire PSD cone in the
three-dimensional span. Nevertheless every strict aggregation description
requires all `m` original ellipsoid rays; the same is true for every
finite weak description. The old rows give matching descriptions.

This resolves the proposed general-cone **two-bound** shortcut negatively.
It does not disprove an unconditional `2k-2` bound. The manuscript's general
upper bound is the established `2k`; its improved bound is explicitly
conditional, and the optimal general count is not asserted. No theorem
depends on a conjectural topological extension or incomplete investigation.
The directional refinement and explicit examples are presented as supporting
observations rather than major novelty claims.

No managed literature collection, external repository, or formal source was
modified. Primary PDFs remain outside the submission sources.
