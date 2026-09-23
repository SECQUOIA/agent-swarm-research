# Independent audit of sparse network–simplex universality

Date: 2026-09-04. Reviewer: common-factor audit agent, independent of the network-simplex author.

Scope: [Sparse network–simplex hulls: universality at simplex dimension two](common-factor-network-simplex.md). The written coordinate-section theorem, facet-restriction lemma, coefficient obstruction, and integer-flow consequence pass this audit. Transportation universality is a classical input; this audit does not certify novelty of the bilinear application.

## 1. The classical input supplies the required coordinates

De Loera–Onn's Theorem 1.1 gives coordinate-erasing representations of bounded nonnegative rational standard-form polytopes by three-layer transportation polytopes. Its definition of representation is stronger than an arbitrary affine map. The explicit final injection in Section 3.3 places every represented coordinate in layer one; composing the earlier coordinate injections retains this property. This was checked in the [primary paper](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf), printed pages 807 and 816.

A bounded polytope initially given by inequalities can be put in nonnegative equality form with slacks. Retaining just the coordinates of the original variables then gives the desired coordinate projection. Clearing denominators before introducing those slacks allows integer standard-form data without rescaling the original coordinates; the paper's construction supplies integer margins.

Appending the new row and column is valid: zero cross-pair margins force all cross entries to zero, and the new corner has its three entries fixed to one. It is an independent fixed block and increases all layer totals by one. Thus `B>0` and both explicit simplex coordinates, as well as the implicit third weight, are strictly positive at the section.

## 2. The network section is exactly the transportation projection

The simplex convention is essential and correctly stated: two explicit coordinates satisfy `y_1,y_2>=0`, `y_1+y_2<=1`. It has three vertices and gives three disaggregated layers. An equality simplex with only two vertices would not supply the three-layer construction.

The disaggregated hull formula is exact. A layer flow in `lambda_k Xi` is obtained by scaling a feasible value-`B` flow by `lambda_k`; conversely, a graph point can be expanded over the three simplex vertices while retaining its original flow. Grouping these terms gives the layer flows. The zero-weight case causes no division problem because the corresponding bounded nonnegative layer flow is zero.

Fixing internal flow totals to `U_ij`, all boundary flows to total row/column margins, and the observed layer-one/two boundary products to their layer margins gives all three families of transportation line sums. The third layer margins follow by subtraction. The designated internal observations remain precisely the selected first-layer entries.

The perspective capacity constraints do not add restrictions. Each internal entry is bounded by the total mass of its layer, and each boundary margin has the same bound. Equivalently, in this acyclic single-source/single-sink network a nonnegative flow of value `D_k` uses at most `D_k` on every arc. Hence the uniform bound `B lambda_k=D_k` is redundant. The converse reconstruction from any feasible transportation table satisfies conservation, fixed totals, and every scaled capacity.

The hidden internal products are absent from the definition of the sparse ambient hull. Therefore, after the sparse hull is defined, fixing all other original coordinates leaves a genuine coordinate section with only the designated product coordinates free. There is no subsequent projection in the facet argument. This distinction is necessary: the same conclusion would not follow for facets of the full-product extended hull.

## 3. Facets of the section force original coefficient ratios

For the triangular section with free coordinates `(p,q)`, every affine-hull equation of the ambient hull has zero coefficients on both of those coordinates. Otherwise its restriction would be a nontrivial equation satisfied by a two-dimensional triangle.

Restrict any finite inequality description to the section. At an interior point of the sloping triangle edge, at least one restricted nonconstant inequality must be active. Finitely many strictly satisfied inequalities cannot create a boundary there. Every active nonconstant valid inequality at that point has its normal proportional to `(1,M)`. Applying this observation to a relative facet description proves the claimed ambient facet coefficient ratio.

This proof also establishes invariance under adding affine-hull equations. For every integer representative of the facet normal, the nonzero `p` coefficient has magnitude at least one and its `q` coefficient is `M` times larger. Primitive normalization therefore still leaves some absolute coefficient at least `M`.

Polynomial construction size in the bit length of `M=2^k` justifies the superpolynomial numerical-magnitude claim: every polynomial in the output model length is bounded by a polynomial in `k`, while the necessary coefficient is at least `2^k`. This is compatible with polynomial bit lengths and with the polynomial-size extended hull. It does not establish large extension complexity or NP-hard continuous separation.

## 4. Unit capacities strengthen the coefficient obstruction

For the coefficient-ratio corollary, scale every flow and observed product coordinate by `1/B`. The ambient network then has value one and every arc has capacity one. The transportation section is uniformly scaled to `P/B`; in the triangle case its sloping inequality becomes

```
p + M q <= 1/B.
```

The coefficient ratio is unchanged. Thus the coefficient obstruction already holds for the unit-flow, unit-capacity version of the shallow DAG. This avoids confusing the obstruction with large numerical capacity coefficients in the original network description. The exact coordinate-section universality theorem can retain capacity `B`; its normalized form represents the uniform scaling `P/B` instead.

The source's integer margins are needed for the draft's integer-coordinate statement, but not for this normalized ratio obstruction. The normalized ambient flow polytope still has integral vertices because it is a unit-flow network polytope with integer capacities and balances.

## 5. Integer-flow and aggregation claims

With integer capacities and balances, the network flow polytope is integral. Expanding the simplex at its three vertices and decomposing each flow into integral network vertices proves that the sparse bilinear hull is the convex hull of integer-coordinate points. Restricting the original arc flows to integers before convexification therefore leaves this hull unchanged. A coordinate section need not be integral, which is consistent with the fractional vertices of the encoded triangle.

The draft correctly stops short of a bound on individual EC&R aggregation multipliers. Large primitive facet coefficients do not alone imply large real aggregation weights under an arbitrary normalization: small differences of bounded real weights may give a very small nonzero coefficient, which becomes large elsewhere after primitive rescaling. A claim about bounded integer aggregate weights could potentially use coefficient counting when all generating product coefficients are bounded, but it requires a precise definition of the generators, reuse of rows, and normalization. Those details are not supplied by transportation universality itself.

No mathematical correction was required. The unit-capacity refinement and the need to keep aggregation-multiplier claims separate were communicated to the author.
