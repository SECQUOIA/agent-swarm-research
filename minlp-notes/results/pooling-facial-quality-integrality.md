# Facial output specifications characterize universal pooling flow integrality

Date: 2026-09-05. Status: independent mathematical review PASS.
The [closing source assessment](../notes/supporting-results-source-closeout.md)
retains qualified priority; no broad novelty claim is made.

For fixed input quality vectors, requiring each output blend to lie on a
face of their convex hull guarantees an integral optimal flow for every
network with integer capacities and every linear cost. A nonempty nonfacial
specification destroys this universal guarantee already with one pool and
one output. The face condition is recognizable by linear programming.
For fixed numbers of pools and quality coordinates, enumerating faces gives
an exact polynomial-time algorithm that allows arbitrary direct arcs.

## Model

The network has inputs `I`, pools `L`, and outputs `J`; its arc set is
contained in `(I×L) ∪ (L×J) ∪ (I×J)`. Pool-to-pool arcs are excluded.
Arc and vertex flow bounds are finite, costs are rational and linear, and
quality blending is linear. Integer bounds are needed only for the
integrality statements; the algorithm also permits rational bounds.

## The integrality characterization



Let the fixed rational input quality vectors be `λ_1,...,λ_m∈R^k`, put
`C=conv{λ_i}`, and let each output's allowed quality region `R_j` be a
closed rational polyhedron (it can express upper/lower bounds or linear
cross-quality specifications). Define `F_j=C∩R_j`. Empty sets and `C` itself
are included among the faces for this statement.
Regions constrain positive-throughput blends. If `R_j={q:A_j q≤b_j}`,
the corresponding flow constraints are the homogenized inequalities
`A_j (quality mass)≤b_j (throughput)`, so zero throughput imposes no
quality requirement.

**Theorem 1 (sufficiency).** If every `F_j` is a face of `C`, every standard pooling network
on these input qualities and output specifications with integer flow bounds
has an integral optimal flow for every rational linear objective. More
strongly, the projected feasible flow set is a finite union of integral
network flow polytopes.

**Proof.** A face has the following established defining property: when a
convex combination of points of `C` belongs to that face, every point with
positive weight in that combination belongs to the face. At a positive-flow
output `j`, its blend belongs to `F_j`. Hence every contributing pool
quality belongs to `F_j`, and, applying the same property at that pool,
every input with positive flow into it belongs to `F_j`. Direct positive
input-output flows must also have input quality in `F_j`.

Conversely, if every positive input-to-pool arc and positive pool-to-output
arc pair `(i,l),(l,j)` satisfies `λ_i∈F_j`, and every positive direct arc
satisfies the same membership, then the reconstructed pool and output blends
satisfy their specifications. Convexity of the faces is enough for this
direction. An empty `F_j` simply forces all incoming output flows to zero.

Thus feasible supports are characterized by finitely many incompatible arc
pairs. Fix any compatible allowed arc set (its flows may be zero). Every
network flow on that arc set is
quality-feasible after reconstructing qualities, because no incompatible
pair can become positive. The feasible flows with this support restricted
are therefore an ordinary network flow polytope. The union over compatible
supports gives exactly the pooling projection. Integer capacities and lower
bounds make each such polytope integral. Finitely many bounded branches also
ensure that an optimum is attained. This proves Theorem 1. □

**Theorem 2 (necessity for a uniform guarantee over networks).** For one fixed
output region `R`, if nonempty `F=C∩R` is not a face of `C`, there is a
standard network using those input qualities, one pool, one output, all
vertex and arc upper bounds one, and costs only zero and minus one, for
which no integral flow is optimal. Thus the face property exactly
characterizes the universal integral-optimum guarantee over topologies and
linear objectives for the fixed input cloud and allowed output regions.

**Proof.** Since the nonempty convex set `F` is not a face, there are
`x,y∈C` and `0<θ<1` with `q=θx+(1-θ)y∈F` and at least one endpoint, say
`x`, outside `F`. Expand `x,y` as convex combinations of the input vectors.
At least one input vector outside `F` has positive weight in the expansion
of `x`; otherwise convexity of `F` would put `x` in `F`. Therefore `q` has
an input-mixture representation with positive total mass on forbidden inputs
`i` with `λ_i∉F`.

Make all inputs adjacent to a single unit-capacity pool, which has a single
unit-capacity output with region `R`. Give intake arcs from forbidden inputs
cost `-1`, and all other arcs cost zero. The mixture just constructed, at
unit throughput, is feasible and has strictly negative cost. An integral
feasible flow can use either zero throughput or one unit from just one
input. Any input used in the latter case must have `λ_i∈F`, so every
integral feasible flow has cost zero. Hence no integral flow is optimal.
All constraints are rational linear constraints after eliminating the one
pool's quality; the existence of the displayed strict improvement also
implies existence of a rational feasible strict improvement. □

The quantifier in Theorem 2 is over network topologies and objectives; it does
not say every existing network with a nonfacial specification has a
fractional optimum. A disconnected output, for example, can be irrelevant.
The counterexample network is itself polynomially solvable (it has only one
pool-to-output arc). The characterization concerns integrality, not a
polynomial-versus-NP-hard dichotomy. In fact the facial class contains the
reviewed strongly NP-hard endpoint family.

**Simple boundary example.** For scalar input qualities `0,1` and a sole
output bound `0<δ<1`, `F=[0,δ]` is not a face of `[0,1]`. Unit capacities
and cost `-1` on dirty intake give optimum `-δ`, achieved with clean intake
`1-δ` and dirty intake `δ`; every integral feasible flow has cost zero.
This explains why the reviewed positive-tolerance hardness result does not
inherit the zero-tolerance integer-optimum identity.


## Polynomial recognition and a constructive consequence

The face condition can be recognized by one LP per output without computing
the facets of the input quality hull. First label input `i` forbidden for
output `j` when `λ_i∉R_j`. On the input simplex solve

```
maximize  Σ_{i forbidden for j} w_i
subject to w≥0, Σ_i w_i=1, Σ_i λ_i*w_i ∈ R_j.
```

If this LP is infeasible, `F_j` is empty. Otherwise its maximum is zero
exactly when `F_j` is a face. The forward implication is the face property.
For the converse, a zero maximum means every mixture in `F_j` uses only
allowed inputs, so `F_j=conv{λ_i:λ_i∈R_j}`. If an interior point of a
segment with endpoints in `C` lies in `F_j`, expand both endpoints into
input mixtures; a forbidden input in either expansion would give positive
objective, which is impossible. Hence both endpoints belong to `F_j`,
proving the face property. A positive LP solution is directly the
fractional-improvement witness in Theorem 2.

There is also an elementary exact algorithm for fixed numbers of pools `p`
and quality coordinates `k` under facial specifications, **including an
arbitrary direct input-output arc graph**. Enumerate the nonempty faces `H`
of `C`. Choose a face `H_l` for each pool, retain input arc `(i,l)` only when
`λ_i∈H_l`, retain output arc `(l,j)` only when `H_l⊆F_j`, and retain only
compatible direct arcs. Solve the resulting min-cost network flow problem
for every tuple of face choices and take the best result.

This enumeration is exact. Given any feasible pooling flow, let `H_l` be the
smallest face of `C` containing the quality of active pool `l`. Every input
with positive flow into that pool belongs to `H_l` by the face property.
If the pool sends positive flow to `j`, its quality belongs to `F_j`, and
minimality gives `H_l⊆F_j`. Hence the original flow is retained in at least
one enumerated network. Conversely every flow in an enumerated network is
feasible because each pool's blend lies in its selected face and every
receiving output face contains it. Inactive pools can be assigned any face.

For fixed `k`, this is polynomial time in the input size. A deliberately
loose elementary count suffices. In the affine hull of `C`, let `d≤k` be
its dimension. Each facet is determined by `d` affinely independent input
points; enumerate these subsets and check the supporting side. There are at
most `m^d` candidates. Every proper nonempty face is the intersection of at
most `d` facet hyperplanes with `C`: take active facet normals spanning the
orthogonal complement of that face's affine hull. Enumerating these choices
gives at most `m^(d²)` descriptions, including duplicates, plus `C` itself.
For `d=0`, only the single nonempty face `C` exists. Face containment can be
checked on the input points lying in the face, which generate it. Thus at
most `(1+m^(k²))^p` network problems suffice, a polynomial for fixed `p,k`.
This loose bound is not advertised as optimal. Rational capacities also
work for the algorithm; integrality of the recovered flow additionally
requires integer flow bounds.

Unrestricted direct arcs are permitted because face states remove all
quality constraints before each network solve. This is a separate constructive
consequence from the general fixed-core/block approach, whose fixed-pool and
fixed-quality application requires controlling direct input-output coupling.

## Endpoint quality bounds: a compact exact formulation

As a special case, normalize each input quality to `[0,1]` and require every
output upper bound to be either zero or one. Input qualities may be any
rational values in the interval. Such output regions cut out faces of the
input quality hull. Let `p` and `k` denote the pool and quality counts.


For a pool `l` and quality `k`, define

```
D_lk = Σ_{i: λ_ik>0} x_il,
S_lk = Σ_{j: μ_jk=0} y_lj.
```

After eliminating the pool quality variables, the quality constraints are
equivalent to

```
D_lk = 0 OR S_lk = 0                 for every l,k,
```

and deletion of every direct arc `(i,j)` having `λ_ik>0, μ_jk=0` for some
quality `k`.

Necessity: pool quality is nonnegative. A strict output's quality inequality
is a sum of nonnegative terms bounded above by zero. Every pool sending it
positive flow therefore has zero quality `k`, forcing all positive-quality
input flows into that pool to vanish. Every incompatible direct flow must
also vanish.

Sufficiency: reconstruct each active pool's qualities by weighted averages
of its intakes. A strict output receiving positive flow from a pool has
`S_lk>0`, hence `D_lk=0`, and that pool's reconstructed quality is zero.
Allowed direct flows also have zero quality. Outputs with bound one accept
every reconstructed quality. Inactive pools can be assigned any bounded
quality. The argument applies coordinate by coordinate.

### Consequences

1. The projected feasible flow set is a union of at most `2^(pk)` ordinary
   network flow polytopes. Fix one side of every disjunction, delete the
   resulting forbidden arcs, and use usual node splitting for vertex
   capacities. The remaining flow problem has no quality constraints.
   Selecting the cheapest network-flow optimum over all branches is exact.
2. If all flow bounds are integers, every nonempty branch is an integral
   network flow polytope. There is an integral optimal flow for every linear
   objective, and the convex hull of the projected feasible flow set is an
   integral polytope. Pool qualities at integer flows may still be fractional
   when pool capacities exceed one. Integer flow does not imply that all
   pools use one input.
3. The decision version with integer bounds is in NP: an integral flow with
   polynomial encoding length is a certificate, and the support disjunctions
   can be checked directly. Combined with the reviewed all-degree-two
   reduction, this restricted endpoint-specification family is strongly
   NP-complete. This says nothing about NP membership for arbitrary pooling.
4. An exact MILP uses at most one binary `z_lk` per disjunction. With finite
   throughput upper bound `C_l`, impose
   `D_lk≤C_l(1-z_lk)` and `S_lk≤C_l z_lk`, together with ordinary network
   flow constraints and incompatible-direct-arc deletions. No quality
   discretization or nonlinear approximation is involved.

The exponential factor is in `pk`, while the network solves have polynomial
bit complexity for unrestricted input/output counts. In particular two pools
and one quality require at most four min-cost flow solves under these endpoint
specifications. This is a special constructive case, not a claim about
general fixed-pool pooling complexity.


## Standard tools, novelty, and verification

The face property, description of faces by active supporting inequalities,
and integrality of bounded network flow polytopes are standard. The
proofs above provide the needed face arguments explicitly. Background
sources include Chaitanya Swamy's [polyhedral theory course record](https://www.math.uwaterloo.ca/~cswamy/courses/co652/)
for faces and active inequalities, and Dimitri Bertsekas's
[*Network Optimization*](https://web.mit.edu/dimitrib/www/netbook_Full_Book_NEW.pdf),
Section 5.5, for integral min-cost flows and total unimodularity.

The potential contribution is the necessary-and-sufficient pooling
interpretation, its recognition LP, and its consequences for exact network
formulations. Searches for pooling, facial specifications, and quality-based
integrality did not locate this characterization. These searches are limited,
and absence from prior literature is not claimed. The geometric reasoning
is elementary and may be implicit in existing compatibility models.

[Independent review](../notes/review-pooling-facial-quality-structure.md): PASS
for the endpoint disjunction, facial sufficiency and necessity, recognition
LP, rational counterexample construction, and face-enumeration algorithm.
The reviewer independently checked all proof steps. No computational test
is claimed for these structural theorems.
