# Independent audit of network–simplex universality

Date: 2026-09-04. Reviewer: `review_extension`. Status: the coordinate-section theorem and facet-ratio consequence pass. The unit-capacity strengthening below also passes. Literature priority remains unestablished.

Reviewed [the candidate](common-factor-network-simplex.md) independently. The substantive obstruction is an arbitrarily large ratio between two **product-coordinate** coefficients, even with unit capacities and unit source–sink flow. An unrestricted claim about large coefficients with arbitrary capacities would be much weaker and partly immediate.

## Transportation source and designated coordinates

The primary [De Loera–Onn paper](https://math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf), Theorem 1.1, gives a polynomial-time coordinate representation of a bounded nonnegative standard-form rational polytope by a three-layer line-sum transportation polytope. The additional layer assertion requires its construction, rather than just the theorem statement: Section 3.3, printed page 816, explicitly maps every incoming coordinate to layer 1. Composing that map with earlier coordinate embeddings proves that all original coordinates can be designated in layer 1. Clearing denominators in the initial equations preserves the coordinates and permits integer margins. Introducing inequality slacks and then retaining only the original coordinates gives the required projection for a bounded inequality-described polytope.

The extra independent corner with three entries equal to one is valid. Cross-block entries vanish because their cross-layer margins are zero, and the new row and column margins force the corner entries. No original feasible point or designated coordinate changes. This ensures positive layer totals without losing the source's polynomial construction bound.

## Exact network realization

Let `D_k` be the three layer totals and `B=sum D_k`. In the four-layer acyclic network, a flow of value `B` can use at most `B` on any arc, so the common capacity `B` introduces no additional restriction. The same holds after scaling: a flow of value `D_k` satisfies the scaled capacities `B lambda_k=D_k`.

The disaggregated formulation is exact by decomposition at the simplex's three vertices. Conversely, each scaled flow divided by its positive mixture weight is a feasible network flow; zero-weight scaled polytopes contain only zero. This verifies both directions without assuming a factorization of the aggregate products.

On the proposed section, aggregate interior flows give the cross-layer margins. Observed boundary products fix row and column sums in layers 1 and 2. Aggregate boundary flows then determine the corresponding layer-3 margins by subtraction. Conservation gives exactly the table equations. Every feasible table produces a feasible disaggregation, because nonnegative table entries and boundary sums cannot exceed their layer totals.

All flow coordinates, both simplex coordinates, and every observed boundary product are fixed. The only remaining original coordinates are the designated interior products. The other table entries exist only as witnesses in the extended formulation: they are not coordinates of the sparse hull being sectioned. Therefore the result is a genuine coordinate section of that sparse hull, with no further projection needed after taking the section. It would not justify the same facet conclusion for the complete-product hull.

The construction uses `rc+r+c` arcs and `2(r+c)+|J|` observed products, plus two simplex coordinates. These counts, and the encoding lengths of the margins and section values, are polynomial in the input description. Arbitrary nonnegative polytopes are represented without rescaling in the capacity-`B` version.

## Facet restriction

The facet lemma is correct, including the affine-hull qualification. Restrict a finite inequality description and affine-hull equations to the coordinate plane. A full-dimensional triangle in that plane implies that every affine-hull equation restricts to an identity. At an interior point of the sloping triangle edge, some nonconstant restricted inequality must be tight: otherwise all finitely many nonconstant inequalities remain satisfied in a neighborhood, contradicting that this is a boundary point. Its supporting line is necessarily the edge's line.

It follows that at least one facet of the original sparse hull has coefficients `a_q=M a_p`, with `a_p` nonzero, on the two free product coordinates. Adding any affine-hull equation leaves these two coefficients unchanged. Consequently every integer representative of that facet has an absolute coefficient at least `M`; imposing primitivity does not weaken the conclusion. This argument uses a section and does not make the generally invalid inference that a facet of a projection must already be a facet before projection.

## Unit-capacity strengthening and the trivial-capacity distinction

Apply the invertible scaling

```
x' = x/B,    z' = z/B,    y' = y.
```

It maps the candidate hull exactly onto the same sparse network–simplex construction with **unit capacities and unit total flow**. The bilinear identities remain `z'_(e,k)=x'_e y_k`. The section representing

```
p >= 0, q >= 0, p+M q <= 1
```

becomes

```
p' >= 0, q' >= 0, p'+M q' <= 1/B.
```

Its sloping normal is still `(1,M)`. Thus the same restriction lemma forces coefficient ratio `M` in a unit-data hull. The section constants may be rational; that has no effect on the facet inference. Full universality after this normalization represents the uniformly scaled target `P/B`, rather than the original `P` verbatim.

This qualification matters. Already the one-simplex-variable hull of `z=xy`, `0<=x<=U`, `0<=y<=1`, has a McCormick facet `z<=Uy`; numerical coefficient `U` is encoded directly by the capacity. Such an example makes unrestricted large-coefficient claims with arbitrary capacities unsurprising. Here both distinguished coefficients belong to product coordinates, and the unit normalization removes large capacities entirely. No assertion about individual EC&R multipliers follows without specifying and analyzing their normalization separately.

For `M=2^k`, the source construction and the network description have size at most a fixed polynomial in `k`. Normalization does not increase this size and replaces all capacity and supply magnitudes by one. A necessary integer facet coefficient is at least `2^k`, which exceeds every polynomial in these model description lengths along the family. This concerns numerical magnitudes. It is not a superpolynomial lower bound on their encoding lengths.

## Remaining scope

The primary [Khademnia–Davarnia preprint](https://arxiv.org/pdf/2302.14151), Appendix equation (25), already supplies the extended hull formulation. Its Proposition 1 and Example 2 support the stated distinction between the one-variable aggregation structure and higher-dimensional behavior. The construction therefore does not yield new polynomial-time optimization, computational hardness of separation, or an extension-complexity lower bound. It also makes no claim for bounded treewidth or planar networks.

Integral network data give an integral hull by expanding at simplex vertices and then decomposing each flow into integral flow vertices. In the normalized network these flows are source–sink path incidence vectors, so the sparse hull is a 0/1 polytope. Rational coordinate sections of an integral hull can have fractional vertices; the transportation sections cause no integrality contradiction.

The transfer is mathematically sound. Its research value should be assessed as a structural application of classical transportation universality, with the original-product-coordinate and unit-capacity qualifications retained. This audit does not establish that the transfer itself is absent from the literature.

## Follow-up source and computational checks

The author subsequently reported 300 minimum/maximum support comparisons on 150 random tables in `code/common-factor-network-simplex-verify.py`. The comparison assembles the normalized sparse hull from its explicit `3rc` path/simplex vertices and compares its fixed-coordinate slice with a direct transportation LP. All comparisons passed. This is useful independent-formulation evidence for the network realization; it does not test the full universality construction or enumerate the asserted large facets. I did not rerun this separate author check.

The author's additional marginal-polytope connection is correct. A normalized distribution over `(row,column,layer)` determines all pairwise margins through the aggregate interior flows and boundary products; simplex and aggregate boundary coordinates add only redundant margins. The designated interior products retain selected full-table cells. Thus the sparse hull is a selected-cell augmentation of a familiar three-way marginal polytope. [Rinaldo's thesis](https://www.stat.cmu.edu/~brian/720-2007-source/nice%20materials/rinaldo-thesis.pdf), Section 4.3, studies the corresponding no-three-factor-effect marginal cone; Proposition 4.3.3 records a complete collapsing description when one table dimension is two, while the surrounding discussion shows that the general case is more complicated. This known statistical interpretation strengthens the need for a cautious novelty claim. It is not, by itself, a contradiction of the proved transfer.
