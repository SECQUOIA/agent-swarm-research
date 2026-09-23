# Independent audit: fixed-support weighted flow optimization at fixed global cycle rank

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently reviewed
[the fixed-support/global-rank candidate](potential-flow-fixed-support-global-rank.md).
The face argument and the exact fixed-core encoding establish its stated
polynomial bit-time maximum/minimum and scenario-recovery theorem for
fixed global cycle rank and objective support. The perturbation mechanism
and fixed-core algorithm are previously reviewed imports. This review
checks their combination, including returning paths, zero flows,
continuous resistance optimization, and witness recovery. It does not
certify literature novelty.

## Pruning and the bounded graph of paths

Removing a zero-objective leaf preserves every attainable objective value.
For a given leaf and neighbor, the merged nomination is their sum, whose
possible values form the exact Minkowski sum of their two intervals.
Conversely, every value in that sum can be split within the two original
intervals. On the remaining graph the flow equations see exactly this
merged nomination. The removed edge can carry the leaf's assigned net
nomination with any permitted resistance, determining its potential from
the neighbor without changing the rest of the network. Its objective
coefficient is zero. Repeating this argument also handles pendant trees
with nonzero nominations and uncertain resistances.

When `c` is nonzero and sums to zero, at least two supported vertices
remain. All remaining leaves are supported. The degree identity gives

```
sum_(deg(v)>=3)(deg(v)-2)=2r'-2+l,
```

so the number of branching vertices is at most `2r'+l-2`. Marking these
vertices and all objective support gives `s<=2r'+2p-2`. Unmarked vertices
have degree two and coefficient zero. There cannot be a disconnected
cycle consisting only of unmarked vertices because the remaining graph
is connected and has marked vertices.

Suppressing maximal paths therefore gives a connected multigraph with
`P=s-1+r'<=3r'+2p-3` edges, counting parallel edges and loops. A loop is
precisely a path returning to the same marked vertex. No simplicity
assumption is imposed on the suppressed graph. The original graph may
remain simple as stated.

## Adjoint shape, including returning paths

For `rho>0`, each differential resistance
`R_e=beta_e(2|x_e|+rho)` is positive. The smoothed state map is
differentiable on the balanced nomination subspace. Differentiating the
flow equations gives the weighted Laplacian adjoint for the objective.
The perturbation in the candidate is a sum of potential differences,
so its source is positive `delta` at every unmarked vertex. A sum of
nominations would not give this same argument; the written perturbation
uses the correct quantity.

Along an oriented suppressed path the adjoint currents satisfy
`j_i-j_(i-1)=delta`. Their signs change at most once, from negative to
positive. Since the next adjoint difference is `-R_i j_i`, adjoint values
strictly increase and then strictly decrease, with at most one zero
edge difference. A plateau can have only two adjacent vertices and occurs
at the maximum. Every horizontal level consequently contains at most two
internal vertices.

The derivation is local and still applies when the two path endpoints are
the same marked vertex. Equal endpoint values impose
`sum_i R_i j_i=0`; they do not invalidate the current increments. For a
concrete exact check, unit resistances and adjoint values
`(0,2,3,3,2,0)` give currents `(-2,-1,0,1,2)`, positive source one at
every internal vertex, equal endpoints, and exactly two vertices at the
maximum level. This also confirms the need to allow a two-vertex plateau.

At a maximum over the nomination box and balance hyperplane, the
polyhedral normal-cone conditions provide one scalar balance multiplier.
Adjoint values strictly above it force upper nominations and values
strictly below it force lower nominations. At most two internal vertices
of each path can have adjoint value equal to the multiplier. All others
have the lower/upper/lower pattern associated with a unimodal sequence.
Equal lower and upper nomination bounds create no extra free coordinate.

Enumerating all such closed box faces is polynomial when `P` is fixed:
each path requires only a constant number of cut positions and at most
two free indices. Leave the marked nominations free and intersect with
balance. This yields at most `s+2P<=8r'+6p-8` free coordinates. Faces
need not have full dimension or contain interior nomination points.

## Removing the perturbations

For completeness, the continuity step can be made explicit. The physical
flow minimizes

```
sum_e beta_e (|x_e|^3/3+rho*x_e^2/2)
subject to Ax=b.
```

This objective is strictly convex, including at `rho=0`, and has a unique
feasible minimizer. Physical nonzero flows follow strictly decreasing
potentials and hence have no directed cycle. A flow decomposition bounds
every edge magnitude by total positive nomination, uniformly in `rho`
and in positive resistance choices. In particular the candidate's `B`
is a valid common bound.

To pass optimality along `b_k->b`, compare an arbitrary flow feasible at
`b` with that flow plus a fixed linear right inverse of incidence applied
to `b_k-b`. These feasible comparison flows converge. A bounded
subsequence of the physical minimizers then passes the energy inequalities
to the limit and is identified by strict convexity with the limiting
physical flow. The same argument permits resistance variation. Potentials
normalized at the reference vertex follow continuously by summing edge
drops along a spanning tree.

Joint continuity on the compact nomination domain times `rho in [0,1]`
gives uniform convergence as `rho->0`. The normalized potential bound
also makes the extra potential-sum perturbation vanish uniformly as
`delta->0`. Thus limits of perturbed maximizers are genuine original
maximizers. The face family is finite and closed, so a subsequence lies
in one face and its limit stays there. This handles zero-flow edges
without differentiation at the nonsmooth limit. No numerical perturbation
size or precision-dependent face enumeration is required.

For the joint problem, continuity on the compact nomination/resistance
domain gives a maximizing scenario. Holding its resistance vector fixed
and applying the face result supplies an equally good nomination on one
of the same graph-defined faces. There is no need for a derivative with
respect to resistances, and face completeness is uniform in their values.

## Exact fixed-core formulation

On a selected feasible face, all but a bounded number of nominations are
fixed at rational bounds. Eliminate their one balance equation when there
is a free coordinate. A rational spanning-tree particular flow and a
fundamental cycle basis give

```
x=x0(z)+Cq,
```

where `z` has bounded dimension and `q` has dimension `r'`. Choose the
particular flow to be zero on chords and the cycle basis to be the identity
on chord coordinates. Then each `q` coordinate is an actual chord flow,
so `|q|<=B` is a valid bound for every physical state. Fixed or zero free
nomination dimensions cause no exception.

All edge flows are affine rational functions of this fixed-dimensional
core. Enumerating their realizable sign patterns is polynomial. On each
closed sign cell, choose the corresponding signed quadratic
`p_e=+x_e^2` or `p_e=-x_e^2`. At a zero edge both choices agree with the
physical law. Identically zero edge forms cause no difficulty. Closed
cells cover boundary configurations without adding nonphysical signed
laws.

The cycle constraints are exactly

```
C^T diag(p_e(z,q)) beta=0.
```

They are necessary and sufficient for the edge-drop vector to belong to
`im(A^T)`, since the columns of `C` span `ker(A)`. Thus every feasible
point of this encoding has consistent potentials and is the unique
physical flow for its encoded scenario. There are `r'` aggregate
equations, irrespective of the number of edges.

Integrating potentials along a fixed spanning tree gives rational weights
`w_e` such that the objective is `sum_e w_e p_e(z,q) beta_e`. Every
resistance is a separate scalar interval block. Its core-dependent
aggregate and objective coefficients have degree two; the block bounds
are finite positive rational numbers. The core's nomination, balance,
sign, and circulation bounds are closed rational linear conditions in a
fixed number of variables. These are precisely the assumptions of the
reviewed fixed-core/polyhedral-block theorem. Adding an objective-value
core coordinate is optional and changes dimensions only by a constant.

The rational objective bound `B^2 ||c||_1 sum_e beta_e^upper` is valid by
spanning-tree integration and has polynomial bit length. Cases `B=0` and
`c=0` can be handled directly. For fixed `r,p`, the number of faces and
cells is polynomial, so applying the exact algorithm to all of them and
selecting the best value is polynomial in total input bit length.

## Witness recovery and arithmetic size

The fixed-core theorem returns its winning core and resistance leaves in
one polynomial-degree algebraic representation. Comparing candidate
optima from different cells requires only ordinary comparisons of
polynomial-size real algebraic numbers; it does not require accumulating
a compositum of all losing candidate fields.

Reverse each leaf-pruning operation. If an aggregate value is `a` and the
two stored intervals were `[l_1,u_1]` and `[l_2,u_2]`, select any element
of

```
[l_1,u_1] intersect [a-u_2,a-l_2]
```

and assign its complement to the other component. The interval is
nonempty by the original Minkowski-sum construction. Taking its lower
endpoint uses only affine arithmetic and comparison in the same field.
Repeating recovers every original nomination. Removed resistances can
be rational interval endpoints. Removed edge flows follow from
conservation; all potentials follow from signed quadratic drops along
a spanning tree. These operations remain in the winning field and have
polynomial total encoding and computation cost. Returning suppressed
paths were never discarded from the edge-level formulation and require
no additional root extraction.

Changing `c` to `-c` gives the minimum theorem with the same support
parameter. Exact rational output is not asserted for cyclic instances.
The result correctly restricts this proof to bounded global cycle rank;
bounded rank per block alone leaves potentially many varying algebraic
pressure contributions outside the fixed-core encoding.

## Reproduced checks and review boundaries

I reran
`code/potential_flow_mpd/fixed_support_global_rank_checks.py` with the
repository's designated Python environment. It passed 12 graphs, 48
suppressed paths including four returning paths, 506 threshold levels,
and 36 balanced-gradient checks. Maximum errors were approximately
`5.72e-14` for current increments, `7.75e-9` for adjoint gradients, and
`1.21e-12` for physical residuals. These checks support the topology and
analytic identities; they do not implement the exact algebraic optimizer.

The cited discrete-resistance and tree comparisons are separate reviewed
results, not consequences newly proved in this audit. No substantive
defect remains in the continuous-resistance global-rank theorem.
