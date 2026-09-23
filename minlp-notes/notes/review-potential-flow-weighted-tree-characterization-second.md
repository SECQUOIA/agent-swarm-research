# Second independent review: trees and universal weighted-potential hulls

Date: 2026-09-05. Verdict: **PASS** for the characterization in
[the candidate note](potential-flow-weighted-potential-tree-characterization.md).
This review verifies the mathematics and its quantitative graph
extension. It does not establish separate literature priority.

## Quantifiers and the tree direction

The graph is finite, connected, and simple. Nominations are fixed and
balanced throughout each resistance optimization. All edge laws are
`beta*x*abs(x)` with strictly positive resistance. There are no added
physical flow or potential bounds. The objective is any zero-sum
linear combination of node potentials, so it is independent of the
potential gauge. The statement is universal in these data, not a claim
that every individual objective fails on every cyclic graph.

On a tree, conservation determines each edge flow from the nomination
on one side of its cut, independently of resistance. Summing potential
drops along tree paths makes every such objective affine in the
resistances, with fixed coefficients. Both separate monotonicity and
endpoint-hull equality follow directly, including zero flows and zero
objective coefficients.

More generally, the implication from separate monotonicity to endpoint
equality does not require one direction of monotonicity to work across
all fibers. Start at a maximum on the compact interval box and replace
coordinates successively by endpoints that do not lower its value.
The resulting corner is in the product of the original uncertainty
sets and still attains the maximum. The minimum argument is identical.
Continuity of the fixed-nomination physical solution in positive
resistances ensures attainment: the unique energy minimizer varies
continuously on a compact positive box, and normalized potentials
follow continuously by integrating edge laws. Thus the two displayed
positive implications are valid under either usual interpretation of
separate coordinate monotonicity.

## Triangle and subdivisions

The proposed triangle flow `(q+2,q-1,q)` has conservation vector
`(2,-3,1)`. For `-1/2<q<0`, the cycle equation is
`(q+2)^2-(q-1)^2-theta*q^2=6q+3-theta*q^2=0`.
The weighted objective equals
`-5(q+2)^2-7(q-1)^2=-105/4-12(q+1/4)^2`.
The stated three rational pairs `(theta,q)` satisfy this equation
exactly. Their middle-versus-endpoint value gap is `3/16`.

Every simple cycle has three distinct branch vertices. Subdividing
its three connecting paths preserves constant flow along each path
because all new nominations are zero. The law on such a path depends
on the sum of its resistances, including for negative flow. Dividing
each fixed total resistance one across its path therefore preserves
the two fixed triangle laws.

On the uncertain path with more than one edge, the fixed resistances
sum to `d=8/3` and the selected uncertain edge has value `theta-d`.
Its smaller endpoint is `8/3>0`, and its interior and larger values
are also positive. Thus exactly one actual resistance coordinate is
uncertain. It is important to subtract `d`; keeping its value at
`theta` would alter the triangle equation. Paths with one edge use
`d=0`. All subdivision coefficients have polynomial binary length.

## Restoring every extra edge

The trial cycle flow with `q=-1/4`, extended by zero on every extra
edge, is conservation-feasible on the full graph, irrespective of
whether it is physical at the chosen resistance setting. Its energy
is `(468+theta)/192<4` at each of the three settings. Convex energy
minimization therefore bounds every extra physical edge flow by
`u=(12/R)^(1/3)` when its resistance is `R`.

The full physical flow has no directed cycle of nonzero flow: the
potential would strictly decrease around such a cycle. Its standard
path decomposition consequently bounds every flow magnitude by the
total positive injection, which is three. Restrict the physical state
to the selected cycle and define `b'` as the divergence of those cycle
flows. This is a balanced nomination, and each of its coordinates
has magnitude at most six because it sums two cycle-edge flows.
The restricted potentials and flows satisfy every cycle law and
conservation with `b'`; uniqueness makes them exactly the isolated
cycle's physical state at `b'`. No approximation is used in that
identification.

At cycle vertices, the difference from the original nomination is the
divergence of extra-edge flows. Each extra edge has at most two cycle
endpoints, so `||b'-b||_1<=2m*u`. Chords, paths through extra vertices,
and dangling edges are all covered by this same incidence count.
Both nominations lie in the balanced box `[-6,6]` on the cycle. Since
the number of cycle vertices is at most `m`, the reviewed nomination
Lipschitz bound may use the conservative flow bound `B=6m` for that
whole box, including the segment between `b` and `b'`.

Apply that bound on each of the two fixed paths of total resistance
one. The objective decomposition `F=-5*(pi0-pi1)+7*(pi1-pi2)` gives

```
|F(b')-F(b)| <= (5+7)*2*(6m)*||b'-b||_1
              <= 288*m^2*u.
```

The uncertain path need not have small resistance: it is not used
for either path sum in this estimate. The nomination Lipschitz theorem
applies to the whole cycle and permits zero physical edge flows, so
there is no hidden differentiability assumption at zero.

For `R=12*(10000*m^2)^3`, the radius is exactly
`u=1/(10000*m^2)`. The error at each scenario is at most
`288/10000=18/625<3/64`. Subtracting two such errors from the original
`3/16` gap leaves more than `3/32`. The actual interior value on the
restored graph therefore exceeds both values at the two endpoint
settings. Taking a two-point set on that one coordinate, with all
other resistances fixed, violates endpoint-hull equality. The same
strict peak violates separate monotonicity directly.

The chosen integer `R` is polynomial in `m` and has logarithmic bit
length. All other resistance values and the fixed nomination/objective
coefficients also have polynomial rational encoding. The proof does
not delete or contract any edge in the final counterexample.

## Exact independent support and scope

[check_weighted_tree_characterization_second.py](../code/potential_flow_mpd/check_weighted_tree_characterization_second.py)
passed 192 exact subdivided physical cycle states, checking edge-law
closure, conservation, objective, positivity, and the energy trial.
Its 144 negative controls confirmed that omitting the fixed-path
subtraction destroys the claimed cycle law. It also checked the exact
restoration constants for 98 graph sizes. These tests use rational
arithmetic only. The general restoration claim rests on the energy
and sensitivity proof above; no potentially ill-scaled numerical
large-resistance solve is used as a substitute.

The result concerns universal weighted-potential objectives with fixed
nominations and nonlinear quadratic resistance uncertainty. It neither
classifies nomination uncertainty nor proves a corresponding boundary
for fixed Ohmic laws. It does not assert the tree equivalence for
multigraphs with two-edge cycles: on two vertices every zero-sum
objective is proportional to the sole potential difference. Other
pairwise-potential and arc-flow classifications, and the separate
discrete-resistance hardness construction, are not needed to prove
this equivalence.
