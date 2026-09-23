# Second independent audit of the weighted arc-flow cactus characterization

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS**, with the author’s clarification that separate monotonicity means monotonicity of each one-variable section after all other resistances are fixed. Its direction can depend on those fixed values. The author also made compact resistance sets explicitly nonempty. The [candidate](potential-flow-weighted-arc-cactus-characterization.md) establishes the stated universal hull characterization on connected simple graphs. This is a mathematical audit; publication priority is not assessed.

## 1. Positive direction on cacti

For fixed balanced nominations, each bridge flow is a fixed cut sum. A cycle block sees fixed effective nominations obtained by summing the original nominations in the attached components. Those sums do not depend on resistances or on the internal physical states of the attachments. Orient a cycle consistently. Conservation gives `x_e=q+d_e`, with rational offsets when nominations are rational, and cycle consistency is the single strictly increasing equation

```
H_beta(q)=sum_e beta_e(q+d_e)|q+d_e|=0.
```

Every cycle has one such independent scalar variable and a disjoint set of edge resistances. Therefore every linear arc-flow objective decomposes into a constant plus an affine function of each independent cycle circulation.

For one varied resistance `beta_e`, the value of `H_beta(-d_e)` is independent of that resistance. The unique root lies on the same side of `-d_e` for every positive value, or equals it for every value. Thus the sign of the corresponding physical flow is invariant along this one-variable section. Increasing `beta_e` changes the equation at its previous root with that fixed sign, and strict increase of `H_beta` determines the direction of root movement. Every affine function of that circulation is accordingly monotone or constant along the section. The argument includes zero flows and needs no differentiability at zero.

Physical states depend continuously on positive resistances by strict convex energy minimization and uniqueness. A product of nonempty compact subsets of `(0,infinity)` is compact and has positive attained lower endpoints. Over its interval hull, move an optimizer one coordinate at a time to an endpoint preserving its optimal value. The needed monotonicity direction is allowed to change after other coordinates are moved. All final endpoints belong to their original sets, so both extrema agree. This proves the two positive implications.

The clarified direction scope is necessary. On a consistently oriented triangle take offsets `(-1,0,1)` and objective equal to the middle flow `q`. At outer resistances `(4,1)`, the root is positive, so increasing the middle resistance decreases `q`. At outer resistances `(1,4)`, the root is negative, so increasing the middle resistance increases `q`. These settings fit one common positive box. Thus a direction fixed globally across the whole box would be a stronger and false assertion, although each section is monotone and the hull property holds.

## 2. The explicit obstruction and subdivision

The exact theta calculations were independently verified in the [rank-two audit](review-potential-flow-weighted-arc-cycle-rank-hardness-second.md). At the three stated rational resistance settings, the flows and objective values are exact. The interior value is `-9/2`, while both endpoint values are `-37/8`, leaving advantage `1/8`. All selected edge flows are positive at these three settings.

A noncactus block is biconnected and is not a single cycle. Choose a cycle in it. If it has a chord, that chord and the two cycle paths form a theta subdivision. Otherwise an off-cycle component exists and must meet the cycle at two distinct vertices; a unique attachment would be an articulation of the block. A path through that component and the two cycle paths also form a theta subdivision. Thus every connected noncactus simple graph contains the required three internally disjoint paths.

Simplicity allows at most one of these paths to be a direct edge. Consequently the other two have distinct internal vertices that can serve as `0` and `1`; the theta endpoints serve as `2` and `3`. Splitting paths there realizes the four outer resistance totals, and zero internal nominations preserve the constant flow within each segment.

For a subdivided uncertain path, giving all but one edge total resistance `d=theta_L/2` and the last edge resistance `theta-d` realizes all three desired totals while keeping every component resistance positive. The endpoints and interior parameter values are shifted by the same rational constant. Segment resistance totals can be divided equally among their edges, requiring only polynomial rational encoding length. The two selected objective edges carry exactly `a` and `q` in the isolated subdivision.

## 3. Restoring all remaining edges

The comparison flow with `a=q=9/8`, other outer flows `(3,23/8,1)`, and zero flow on all extra edges satisfies the full graph's conservation equations at all three resistance settings. It need not satisfy pressure equations to bound the minimum convex energy. Its maximum energy, at `theta_U`, is exactly `91657/16<6000`. Every actual extra-edge flow therefore satisfies

```
R|x_e|^3/3<6000,  so  |x_e|<=(18000/R)^(1/3)=u.
```

The only positive nominations are four and three. Passive flow cannot contain a directed positive-flow cycle, since potentials strictly decrease along such a cycle. Flow decomposition therefore bounds every physical edge flow by seven, independently of the large restoration resistance.

Restrict the full physical flow to the selected theta subdivision and let `b'` be its induced nomination. It is balanced. Each selected vertex has selected degree at most three, giving `|b'_v|<=21`. The original nomination is also in this box. A theta subdivision with `m_theta` edges has `m_theta-1` vertices, so its total absolute-coordinate bound satisfies `B<=21m` with `m=|E(G)|`. The changed nominations are exactly the boundary contribution of omitted edges; summing absolute incidence contributions gives `||b'-b||_1<=2m u`.

The restricted flow and restricted potentials are precisely the selected network's physical state at nomination `b'`. This follows because they still satisfy every selected edge law and conservation at `b'`; uniqueness then identifies them. It is therefore legitimate to compare selected-network states at `b'` and `b`.

## 4. Direct verification of the single-edge estimate

The pressure Lipschitz bound used in the candidate can be obtained directly here. Between the two selected-network states, choose the quadratic secant resistance

```
r_i=beta_i [x'_i|x'_i|-x_i|x_i|]/(x'_i-x_i)
```

when the flows differ, and set `r_i=2B beta_i` otherwise. Both states have flows in `[-B,B]`, so `0<r_i<=2B beta_i`. Their differences solve the positive-resistance linear electrical system with nomination difference `b'-b`.

For the endpoints of a selected edge `e`, the corresponding unit electrical adjoint has potential oscillation equal to its effective resistance. That effective resistance is at most the single-edge resistance `r_e`, because the edge itself is an available path. Pairing this adjoint with the balanced nomination difference gives the conservative bound

```
|delta(pi_tail-pi_head)|<=2B beta_e ||b'-b||_1.
```

Quadratic strong monotonicity gives `|s|s-|t|t` in absolute value at least `|s-t|^2/2`. Applying the physical law on the same edge yields

```
|delta x_e|^2
 <=(2/beta_e)|delta(pi_tail-pi_head)|
 <=4B||b'-b||_1<=168m^2 u.
```

This derivation confirms that the edge resistance cancels. No hidden lower bound on the individual resistance of a long subdivision segment is required. It also avoids an assumption about positive law derivatives at zero flow.

The weighted objective error is bounded by `(9+5)sqrt(168m^2u)`. With the stated integer `R`, `u=1/(10^9m^2)` and its squared bound is

```
196*168/10^9=1029/31250000<1/1024.
```

Thus each of the three objective values changes by less than `1/32`. The restored interior scenario exceeds both endpoints by more than `1/8-2/32=1/16`. Every restored resistance is finite and positive. The integer `R` has `O(log m)` bits, and every other resistance and subdivision parameter has polynomial rational encoding length.

## 5. Quantifiers, conclusions, and arithmetic scope

The restored construction uses the same fixed nominations and linear objective at both endpoints and the interior of a single uncertain resistance. All other resistances are fixed. An interior value strictly exceeding both endpoints makes that scalar section nonmonotone. Choosing the uncertain set to contain just those two endpoints also makes its maximum strictly smaller than the interval-hull maximum. Hence every noncactus violates both universal properties, completing their equivalence with the cactus condition.

The construction uses only four nonzero nominations and two objective edges; subdivision and restoration introduce no additional operating constraints or uncertain coordinates. Orientations are representational: selected edges can be oriented as in the displayed construction, with objective signs transformed if a different orientation convention is retained.

For compact attainable flow sets, agreement of extrema for every linear objective is equivalently agreement of their convex hulls by standard support-function separation. This is a structural statement. Independent cactus cycles can have optima in different algebraic fields, and the proof does not give polynomial exact comparison of their sum. The candidate expressly retains this arithmetic limitation. No such sum is involved in the single-theta obstruction.

## Reviewed positive-coefficient counterexample

The author’s proposed corollary with coefficients `(9,5)` also passes. On the selected isolated theta subdivision, choose an edge in segment `0->3` and an edge in the uncertain cross path. Their objective `9x_03+5x_23` equals the original objective plus 36 and has the same interior advantage `1/8`. Restore extra edges using the same construction and apply the established per-edge error bound directly to these two selected edges. The absolute coefficient sum is still fourteen, so each scenario changes by less than `1/32` and the restored advantage is still greater than `1/16`.

One must use this direct error comparison: after restoring extra edges incident to vertex zero, the identity `x_02+x_03=4` need not remain exact. No such identity is needed for the corollary. The selected flows at the three base settings are positive, and their minimum, `1/32` on the cross edge, exceeds the restoration flow error `sqrt(168/10^9)`. They remain positive in all three restored witness scenarios. Thus the universal obstruction can use positive objective coefficients and positive selected flows.
