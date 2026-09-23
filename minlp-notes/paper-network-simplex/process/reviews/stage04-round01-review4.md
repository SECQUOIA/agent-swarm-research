# Stage 4, round 1 — independent reviewer 4

Snapshot: `process/snapshots/stage04-round01`.

## Verdict

**No major issues. One minor scientific-clarity correction is recommended
before closing the stage.** The general bounds, new constructive recovery,
new five-product K4 section, and coefficient-necessity argument pass this audit.

## Enumerated findings

1. **R4-S04-01 — Minor: distinguish changed balance data from a different
   reference for the same polytope.** Location: the final sentence of
   Remark `rem:seven-product-k4`, beginning “Changing the reference on 01 ...”.
   This explanation attributes the change from a point support face to an edge
   to changing a reference flow. For a *fixed* balance vector, changing the
   reference merely translates the cycle-coordinate polytope and cannot change
   the dimension of a support face. Here the two displayed constructions also
   have different balance vectors, because changing only `v_01` changes `Av`.
   The calculations themselves are correct, and the different balances are
   displayed earlier, so this is a local wording repair, not a theorem error.
   Please explicitly attribute the face change to the altered balance data
   represented by that reference vector, rather than leave the impression that
   the result comes from a coordinate choice. For example: “The altered balance
   data in the five-product construction, represented by `v_01=1/4`, make ...”.

## Mathematical audit

**Local circuits.** For an extreme nonnegative dependence, any independent
dependence on its positive support permits two-sided perturbation; thus the
dependence space is one-dimensional. A dependence on a proper subset would
give such an independent perturbation. Therefore the support is a matroid
circuit of size at most `s+1`. Its cofactor coefficients are nonzero unit
minors, and positivity selects all `+1`. Farkas completeness follows by
generation of the pointed nonnegative kernel cone by extreme rays. An
opposite-normal pair is itself a positive circuit, so no larger minimal
circuit contains both normals of one observation. This justifies the unit
product coefficients after branch selection.

**Edge and objective libraries.** The cofactor direction of `s-1` independent
rows is ternary and primitive. Appending any row of `M` gives its scalar
product as a unit incidence-derived minor. Consequently `Md` is also ternary.
At an edge's relative interior, all tight rows, including affine-hull rows,
have nullspace equal to its one-dimensional direction space; lower-dimensional
states are therefore included. Coordinate directions make the arrangement
chambers pointed. Their extreme rays arise from `s-1` independent direction
hyperplanes, so the prescribed library covers them. Hadamard bounds its
primitive coordinate entries by `H_s`.

The support functions are linear on each chamber because the maximizing vertex
cannot change without an edge becoming orthogonal to the objective. Continuity
extends this to chamber closures. Nonnegative ray combinations then give every
support inequality, including for lower-dimensional sums. The stated empty
sum convention is consistent.

**Support duals and the stronger bound.** The signed coordinate rows ensure
dual feasibility. Reducing an optimal nonnegative dual support along dependencies
and completing independent support rows to a basis gives the claimed finite
formula even for degenerate primal domains. A nonsingular row basis is
unimodular. More importantly, `B^{-T}h` is the primitive integer normal of
the independent ternary vectors `Bd_i`; this proves the *same* `H_s` bound
on multipliers, rather than an unjustified triangle-inequality bound. Bases
cannot contain opposite normals, so individual observed products are not
counted twice in a support branch. Product labels separate states, and chord
coordinates separate aggregate flow coefficients.

**Separation complexity.** The signed normal, direction, ray, circuit, and
basis subset counts give `2^{O(s^2)}` parameter work; multiplying ray and
basis counts preserves that order. State initialization and scans respect
`sum_B a_B <= |O|`. Fundamental-cycle construction costs `O(r|E|)` and is
absorbed. The support minimum's active basis and endpoint choices give an
affine majorant valid on every hull point with the same candidate violation.
The normalization and rational-bit caveats are stated correctly.

**New no-LP recovery.** The inequalities on `-h` describe exactly
`Q_i intersect (t - suffix sum)` with the correct signs. This polytope is
nonempty and bounded. At any vertex, tight normals span the full ambient
space, also when the polytope is lower-dimensional. Thus enumerating normal
bases and testing their intersections finds a feasible point. The new normal
list has `2^{O(s^2)}` rows; selecting `s` of them gives `2^{O(s^3)}` work
and storage including the row tests. Sequential subtraction preserves suffix
membership and the final zero remainder.

The encoding argument also passes: an initial common denominator can cover all
state endpoints, supports, and aggregate coordinates. Each selected basis adds
only the bit length of one parameter-sized determinant to a common denominator
of the current remainder. There are only `a_B+1` selected steps. Rejected
bases are evaluated from the same remainder and do not recursively multiply
each other's denominators. Feasible state vectors and remainders are bounded
by the input domain; rejected candidates multiply bounded-size right-hand
sides by fixed inverse bases. No exponential bit growth in the number of
states is hidden here.

**New five-product K4.** I independently recomputed the incidence balances,
aggregate flow, observation equations, all state deviations, and the stated
open-neighborhood bounds. The first state is `(p,q,p)`, the second is
`(s,-s,0)`, and the residual support in direction `(1,1,1)` is at most
`1/3`. Since the aggregate support value is `1/3`, necessity is exactly
`2p+q>=0`. The proposed `s=q/2` gives the displayed residual arc vector;
its fourth coordinate is strictly in `(3/16,11/48)`, and all other bounds
hold in the stated neighborhood. Thus this is a genuine locally full
two-coordinate half-plane with only five observed products and two explicit
simplex variables. I also checked the older seven-product witness rather
than assuming its correctness.

**Section-to-facet transfer.** The local half-plane contains two-dimensional
interior in the coordinate plane, so every affine equation valid on the hull
restricts to an identity. At a local boundary point some nonconstant restricted
inequality must be tight; feasibility on both tangent directions forces its
normal to be the claimed positive multiple. This applies to a relative facet
description and survives adding valid equations. Therefore the ratio-two
necessity concerns the actual original products and establishes sharpness of
the integer coefficient bound `H_3=2`.

## Checks actually performed

I compared the stage against `results/network-simplex-bounded-rank-hull.md`.
The older result is covered, the previously missing direct recovery is now
proved, and the old K4 construction remains available as a variant. No
current-stage material omission was identified.

An independent Fraction script, with no repository implementation imports,
is retained at `verification/reviewer4/stage04-round01/check_k4_recovery.py`.
It passed the following checks:

- K4 libraries: 7 edge directions, 18 rays, 128 normal bases; every transformed
  edge is ternary and every nonnegative support multiplier is an integer at
  most two;
- 2,472 recovery bases when duplicate normals are retained in the concatenated
  normal list, followed by exact successful recovery for 33 state polytopes,
  including point and lower-dimensional states;
- 488 exact feasible state-flow witnesses on a 961-point rational grid for the
  **new five-product construction**;
- 473 exact exclusions on the other grid points, using the independently
  checked residual support certificate `C_12-C_03=(1,1,1)`.

The output is in `check_k4_recovery.json`. These finite checks supplement,
rather than replace, the general proof review.

A private LaTeX build completed successfully in
`verification/reviewer4/stage04-round01/build`; the final log has no warning,
undefined-reference, overfull, or underfull matches.

## Limitations

I did not independently repeat the literature search or test general-rank
runtime. The script uses rank three; the general `H_s` and parameter-complexity
claims were checked from their proofs. I read no other current-round reports,
edited no manuscript sources, and spawned no agents.
