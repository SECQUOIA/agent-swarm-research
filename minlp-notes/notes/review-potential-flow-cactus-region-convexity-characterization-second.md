# Second independent audit of attainable-state convexity classifications

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-region-convexity-characterization.md) correctly proves universal convexity of resistance-attainable flow regions exactly on cacti, and of normalized potential or joint-state regions exactly on trees, for connected simple graphs under quadratic passive laws. The converse uses the reviewed one-coordinate obstructions plus a valid injectivity argument. No new restoration estimate or computational claim is needed.

## 1. Deletion identity and strictness

The varied edge `e=(u,v)` is cyclic, so deleting it leaves the graph connected. If its flow is `q`, the remaining network's nomination is exactly `b-q(e_u-e_v)` under the stated incidence convention. This remains balanced for every real q and has a unique passive physical flow and normalized potential.

For `q2>q1`, let `delta x` and `delta pi` denote differences of the two remaining-network states. Their nomination difference is the nonzero vector `-(q2-q1)(e_u-e_v)`, so `delta x` cannot be zero. Strict increase of each edge law gives

```
0<sum_f (g_f(x_f(q2))-g_f(x_f(q1))) delta x_f
  =delta pi^T A_remaining delta x
  =-(q2-q1)(P(q2)-P(q1)).
```

Thus P is strictly decreasing. The minus sign in the candidate is correct. Different additive normalizations of individual potentials would not affect P, though one fixed reference is convenient for the vector-state argument.

The full state satisfies `P(q)-beta_e q|q|=0`. Its left side is strictly decreasing in q. Existence follows from existence of the full passive state; uniqueness also follows directly from this strict decrease. Its sign at q zero is P(0), independent of the varied resistance.

If P(0) is zero, q is zero for every resistance. The remaining network then has unchanged nominations b, and its entire normalized state is fixed. Its endpoint drop is zero, so it also satisfies the deleted edge law at every resistance value. Hence the full state is constant, as claimed.

Otherwise q never vanishes. For beta2 greater than beta1, substituting the old root into the new equation gives `(beta1-beta2)q|q|`, strictly nonzero with known sign. Root comparison proves strict monotonicity of q in beta: it decreases when q is positive and increases when q is negative. This is a one-variable argument with all other resistances held fixed.

Continuity of the physical solution follows from strict convex energy minimization on bounded parameter ranges and uniqueness. Therefore a nondegenerate resistance interval maps bijectively and continuously onto the interval between its two own-edge flow values. A fixed resistance interval or the constant-state case yields a singleton and causes no difficulty.

## 2. Convex graph over a scalar coordinate

Every remaining-network flow coordinate is determined by q, so the full attainable flow set contains exactly one point with each own-edge coordinate q in its range. If this set is convex, it contains the segment between its two endpoint states. That segment itself contains exactly one point at each intermediate q. Since these values exhaust the full parameter range, uniqueness at each q forces the entire attainable set to equal the segment.

This step uses injectivity of a linear coordinate projection, not just the fact that the parameter set is one-dimensional. A general continuous curve need not have this property. Once the set is the segment, every linear objective is bounded above by its endpoint maximum and below by its endpoint minimum.

The inherited noncactus obstruction varies an edge of a selected theta subdivision. That edge remains on a cycle after subdivision and after extra edges are restored. Its strict interior objective advantage excludes the constant-state case. The proposed flow convexity converse therefore applies to every noncactus graph in the stated class.

## 3. Convexity on cacti and quantifiers

For a cactus, fixed nominations give fixed bridge flows and independent scalar circulation intervals on the cycle blocks. The entire interval-attainable flow region is their affine box image, hence convex, including lower-dimensional cases. The inherited constructive region theorem supplies precisely the required independence and continuity.

The characterization is universal over nomination vectors and resistance boxes. It does not say that every box on a noncactus graph has a nonconvex region. Zero nominations, fixed boxes, or a varied edge with zero own-edge flow can give singleton regions even there. One explicit nonconvex witness for each noncactus graph is sufficient for the converse, and the cited obstruction provides it with positive rational data and four nonzero nominations.

The brief generalization of the positive argument to connected compact independent edge-law parameter domains is also valid under its stated continuity assumption. A scalar cycle image of a connected set is an interval, and disjoint block parameters preserve independence. This observation is structural; the main negative-direction characterization remains within the quadratic scope.

## 4. Normalized potentials and joint states

On a tree, flows are fixed by conservation. Edge drops are linear functions of their individual resistances, and normalized potentials are linear combinations of those drops. Thus the potential region and the joint region `(fixed flow, potential)` are affine images of the resistance box and are convex.

On a graph with a cycle, the inherited weighted-potential obstruction again varies one cyclic edge and supplies a strict interior advantage. The deletion argument gives a nonconstant strictly monotone q and a strictly decreasing P(q). The linear potential functional `pi_u-pi_v` therefore maps the potential curve bijectively onto an interval.

For each q, all normalized potentials are uniquely determined by the connected remaining network. Since P is injective, there is exactly one normalized potential vector at each terminal-drop value. The convex-graph argument above applies with this drop as its scalar coordinate. A convex potential region would be the endpoint segment and could not have the inherited linear objective's strict interior advantage. Hence the potential region is nonconvex.

The joint region projects linearly onto that nonconvex potential region. A convex joint region would have convex projection, so the joint region is also nonconvex. This projection argument has the correct direction. Changing the chosen potential reference is a linear bijection between normalized potential spaces and preserves convexity, so the characterization does not depend on the reference vertex.

The weighted-potential source obstruction explicitly uses one edge of a simple cycle, retains that cycle during restoration, and uses a zero-sum objective. Its objective value and interior advantage therefore survive any normalization. Simplicity is material to that inherited theorem; the present candidate correctly does not extend the tree classification to two-vertex parallel-edge multigraphs.

## 5. Exact base-gadget controls

The two reviewed base obstructions also show nonconvexity directly, independently of the abstract scalar-graph argument. For the flow theta, averaging the two endpoint states gives `a=q=37/32`, `x_21=3`, `x_31=1`, and `x_03=4-a`. Its outer-cycle pressure residual is

```
a^2+9-[(4-a)^2+2]=8a-9=1/4.
```

Thus the midpoint is conserved but cannot be a physical state for any choice of the cross resistance.

For the potential triangle, normalize `pi_0=0`. At its endpoint circulations `q=-3/8` and `q=-1/8`, the pairs `(pi_1,pi_2)` are respectively `(-169/64,-3/4)` and `(-225/64,-9/4)`. Their midpoint is `(-197/64,-3/2)`. The remaining-network drop satisfies `pi_2=-6q-3`, so this midpoint would force `q=-1/4`; its actual first potential is then `-49/16=-196/64`, a contradiction. These exact controls agree with both claimed geometric boundaries.

For arbitrary supergraphs the inherited strict objective gaps and the deletion/injectivity proof are still required; the base midpoint calculations alone do not establish restoration. No new estimate is being assumed for that step.

## Scope

This audit checked both relevant promoted obstruction theorems and verified that their varied edges, strict gaps, fixed nominations, and positive-data restrictions match the new argument. The result is geometric. It adds no exact polynomial comparison of independent algebraic sums and makes no classification claim for fixed linear Ohmic laws. Source novelty remains separate. No correction is required.

## Addendum: strictly positive interval widths

The existential positive-width thickening corollary also passes. Let S be the compact old attainable region, choose two points of S and a point z on their segment outside S, and put `delta=dist(z,S)>0`. Joint continuity of the normalized physical state on a compact positive-resistance neighborhood is uniform. Therefore sufficiently small positive thickening of every fixed resistance coordinate produces a new attainable region contained within distance less than delta/2 of S. To see this directly, map each new parameter back to the old box by coordinate projection; the parameter distance tends uniformly to zero with the thickening width.

The old box remains contained in the new one. The two selected states therefore remain attainable, while z remains unattainable. The enlarged region is nonconvex. Widths can be chosen positive and rational and below the original minimum resistance, preserving positive rational input data. This argument applies separately to the flow, normalized-potential, and joint-state images. It is only an existential strengthening of the topology characterization; it supplies no polynomial bound for a suitable width and makes no new computational claim.
