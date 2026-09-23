# Source audit: power-law resistance regions

Date: 2026-09-05. Bounded primary-source assessment of
[the extension candidate](potential-flow-power-law-region-convexity-extension.md).
This note assesses attribution and scope, not the complete mathematical proof.

No matching universal characterization was located in the inspected sources:
for each fixed `p>0`, `p!=1`, on connected simple graphs, the attainable flow
region under independent positive resistance intervals and fixed balanced
nominations is universally convex exactly on cacti; normalized potential
and joint regions are universally convex exactly on trees. The meaningful
extension is the common classification across all these nonlinear power
exponents, with explicit local curvature obstructions. Classical energy,
tree/cycle, topology, and uncertainty arguments must receive credit.

## Direct antecedents

Aßmann, Liers, Stingl, and Vera,
[Deciding Robust Feasibility and Infeasibility Using a Set Containment Approach](https://arxiv.org/pdf/1808.10241),
Corollary 4.3, Lemma 4.6, Proposition 4.9, and Lemma 4.10, supplies directly
relevant tree and single-cycle descriptions for fixed nominations and
uncertain pressure-loss coefficients. Fixed tree flows and one cycle
circulation are established mechanisms. Independent cactus blocks yield
an affine product of scalar intervals by a short extension of this
structure. The checked results do not give the proposed full graph
classification for every fixed nonlinear power exponent.

Duffin, [Topology of Series-Parallel Networks](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf)
(1965), particularly Section 5 and Theorem 4, is a foundational source for
topological properties of monotone nonlinear circuits. Cite it for that
tradition; neither topology-based sign reasoning nor nonlinear circuit
reduction is a new principle here.

Brandenberg and Stursberg,
[Extremal Solutions for Network Flow with Differential Constraints](https://link.springer.com/article/10.1007/s10957-025-02792-4)
(2025), Definitions 1.1–1.2 and Theorem 3.1, is an especially close graph
antecedent. It characterizes universal nondegeneracy using cacti and a
diamond obstruction. Its edge elasticities are fixed, its constitutive law
is linear, and its region varies nomination and flow bounds. That region
is already a polyhedron on every graph. The present theorem instead varies
resistances while fixing nominations and asks whether the resulting
nonlinear state image is convex. The shared cactus/diamond structure
deserves explicit comparison; the statements are not interchangeable.

## Wang–Hasler: what was actually accessible

The primary EPFL manuscript
[Convexity of Resistive Circuit Characteristics](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download)
by Changlu Wang and Martin Hasler remains inaccessible through direct
retrieval. Search indexing exposed its complete abstract and portions of
its introduction and conclusion, but not a checked complete theorem set.
The abstract specifies scalar branch current or voltage as a function of
a source value, under convex/concave resistor characteristics. The
conclusion on manuscript page 21 proposes extending its approach to
parameters other than source values. These checked excerpts distinguish
its stated main problem from resistance-image convexity. They do not
justify asserting that no theorem inside it can be relevant. In particular,
convexity of a scalar transfer function and convexity of its vector graph
are different properties.

The separate Hasler–Wang paper *Parameter tolerances in non-linear resistive
circuits: worst case analysis based on monotonicity*, NOLTA 1993,
pages 841–846, remains unread. Its citation is confirmed in reference 2 of
Pastore's [DC tolerance analysis of electronic circuits by polyhedral circuits](https://arts.units.it/retrieve/e2913fde-d2e2-f688-e053-3705fe0a67e0/2869823_10.1002-cta.2098-PostPrint.pdf).
This is still a material priority gap. The current audit did not locate an
open copy. Do not describe it as covering source variation only: that
description belongs to the other Wang–Hasler manuscript's indexed abstract.

## Interpretation and limitations

The distinction between componentwise scalar curvature, marginal ranges,
convex hull equality, and convexity of the entire attained region should
be explicit. A convex energy for each fixed resistance vector guarantees
a well-defined physical state; it does not guarantee a convex image as the
parameters vary. Likewise, an exact convex relaxation for a different flow
model does not establish convexity of this state image.

The finite restoration argument establishes existence of rational witness
data. It currently gives neither a uniform polynomial encoding bound nor
an exact arithmetic algorithm for arbitrary real exponents. The exponent
is fixed; this is not a theorem with a binary-encoded variable exponent.
The linear exponent `p=1` is excluded and is not classified by the stated
curvature witnesses. Positive directions can remain valid more broadly,
but they do not establish the omitted converses. Simple graphs and
normalization of one potential are material assumptions.

Recommended positioning: a qualitative extension of the repository's
quadratic state-region boundary to every fixed non-Ohmic positive power,
building on classical nonlinear circuit topology and tree/cycle tolerance
analysis. The new part to evaluate is the common converse classification
and its restricted physical witnesses. No matching theorem was found in
the inspected open primary sources; an unqualified first-result claim is
not supported, particularly while the 1993 tolerance paper remains unread.

The earlier [weighted-objective source audit](potential-flow-weighted-objective-hierarchy-novelty.md)
contains additional comparisons with linear circuit tolerance geometry.
