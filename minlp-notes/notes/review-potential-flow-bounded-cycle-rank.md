# Independent review: MPD with bounded cycle rank in each block

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed candidate: [potential-flow-block-cycle-rank-investigation.md](potential-flow-block-cycle-rank-investigation.md).

**Verdict: PASS for the quadratic-law theorem.** The localized objective perturbation resolves the flat-adjoint-path obstruction and supplies polynomially many faces of bounded dimension for each fixed block cycle-rank bound. The algebraic optimization and rational output arguments then give the stated certified additive guarantee. The proposed extension to other edge laws is outside this verdict. Novelty and practical computational performance are not certified.

## First localize to one block

The original objective-terminal block path can be isolated exactly by aggregating each attached component's independent load intervals into its unique core attachment. No flow or potential bounds are present, so the aggregate totals determine the core flow and every balanced aggregate nomination can be disaggregated. This is the same valid argument as in the cactus case and does not require cycle blocks.

For the law-smoothed original objective, the auxiliary electrical current has only the objective terminals as source and sink. Each block on their block-cut path carries one unit between its two distinct boundary vertices. In a biconnected non-bridge block, every other electrical potential lies strictly between those boundary potentials. To see the necessary strictness, suppose an internal vertex attained the upper boundary value. Harmonicity with positive conductances would propagate that value along a path to the lower boundary avoiding the upper boundary vertex; two-vertex-connectivity guarantees such a path. This is a contradiction. The minimum argument is the same. Bridge blocks have no internal vertices.

The open electrical potential ranges of consecutive blocks are therefore disjoint and ordered. The linear-programming balance multiplier forces all loads strictly earlier than the selected block to upper bounds and all loads strictly later to lower bounds. A multiplier equal to an articulation potential leaves only that articulation potentially free outside any chosen neighboring block; including it as a block endpoint handles the case. Extreme multipliers give fully saturated patterns. The finite-face smoothing limit remains valid on arbitrary graphs.

It is essential that the additional internal-source perturbation is introduced **after** selecting such a block face. Perturbing the global objective first could change the global electrical block ordering. The current candidate correctly optimizes each selected local block separately, with rational shifted endpoint intervals and fixed outside drops.

## Suppression counts

Let a non-bridge biconnected block have cycle rank `r_H=m-n+1`. Its minimum degree is at least two, so

```
sum_v(deg(v)-2)=2r_H-2
```

bounds the number of vertices of degree at least three by `2r_H-2`. Adding the two distinct local objective terminals gives `|K|<=2r_H`.

Every remaining vertex has degree two and lies on a unique maximal path with endpoints in `K`. A separate degree-two cycle cannot remain disconnected from `K` because the block is connected; the rank-one cycle case is cut into two paths by the two inserted terminals. Suppression preserves connectedness and cycle rank. Its edges are precisely these maximal paths, giving

```
p=r_H+|K|-1<=3r_H-1.
```

Parallel kernel edges are expected and cause no difficulty. On a simple original biconnected graph a path returning to its same sole marked endpoint would create an articulation, unless the graph were a cycle; in that exceptional case the two terminals already prevent such a path. The formulas also work for ordinary parallel-edge blocks. Self-loops, if allowed in a network convention, carry zero passive flow and can be deleted before forming the block decomposition.

## Perturbed path sensitivities

At each local nomination, the smoothed physical equations have a positive-definite reduced Laplacian derivative. Differentiating the perturbed objective therefore yields the displayed adjoint equation with source `delta>0` at every unmarked path-internal vertex. The sink term at the fixed exit makes the source vector balanced.

Orient one maximal path in either direction and define `j_i=(h_i-h_{i+1})/R_i`. At an internal vertex the outgoing electrical flows are `j_i` and `-j_{i-1}`, so

```
j_i-j_{i-1}=delta>0.
```

The sign in the candidate is correct. Thus the currents strictly increase. Negative current means the next potential is larger; positive current means it is smaller. The potential sequence rises strictly and then falls strictly, with either phase possibly empty. At most one edge has zero current, so the only possible plateau consists of two adjacent vertices at the maximum.

Every level is attained at at most two vertices: one on each strict flank, or the two peak-plateau vertices. The strict upper-level set is one interval of vertices. These statements hold without assuming different endpoint potentials; the equal-endpoint case was precisely the unperturbed obstruction. They also hold on paths with no internal vertices, where there is no path-internal nomination to control.

## Finite face enumeration

At a perturbed maximum over the local balanced box, its derivative linear functional is maximized at the same point. Linear-programming optimality supplies one multiplier `lambda`. Values above it force upper bounds and values below it force lower bounds. Consequently every path's internal nominations have the lower–upper–lower pattern with at most one free pivot at each boundary. If the strict upper interval is empty and the maximum equals `lambda`, a one-vertex peak or two-vertex plateau supplies one or two free pivots. Entirely upper or entirely lower paths and monotone paths are included.

A threshold can occupy a vertex or a gap, so choosing the two ordered boundaries takes quadratically many choices in the path length. Coincident boundaries are allowed to encode a single free peak, and adjacent free boundaries encode the plateau. One may harmlessly enumerate additional bound patterns of this form that no adjoint realizes: each resulting face is still a subset of the original feasible nomination box. There are at most three states per marked vertex, and at most `2p+|K|<=8r_H-2` free coordinates in total.

Multiplying the path choices and the `3^|K|` marked-vertex choices gives `n^{O(r_H)}` candidates. This is polynomial for each fixed rank bound and supports the stated XP-type claim; it does not establish fixed-parameter tractability.

The rational balance equation and box bounds can be checked directly for every candidate. A face with no free coordinates is tested for balance and then evaluated as a fixed nomination. A face with at least one free coordinate can eliminate one coordinate using balance; the resulting dimension is at most `8r_H-3`. Bridge blocks are handled separately and never use these rank-positive dimension formulas.

## Two limiting parameters

The perturbation is an existence device, not a numerical algorithm step. For every fixed `delta,rho>0`, compactness provides a perturbed maximizer. Passive flow acyclicity bounds every smoothed flow by total positive injection. The local nomination intervals are finite, so a fixed rational bound controls all flows and all normalized potential differences uniformly for `rho<=1`.

The law-smoothed objective converges uniformly to the original objective as `rho` tends to zero. The energy-minimization argument proving this does not depend on cactus structure: correct comparison flows by a tree routing of the vanishing nomination change, pass the minimizing inequality to the limit, and use strict convexity. The added objective term is bounded uniformly by `delta` times a fixed finite number of bounded potential differences. Thus the two-parameter perturbed objectives converge uniformly to the original local objective along any sequence `delta,rho ->0`.

A convergent subsequence of their maximizers is therefore an original maximizer. A further subsequence belongs to one fixed member of the finite enumeration. That member is a closed nomination face, so the limiting optimizer remains in it. No strictly positive limiting conductance, nonzero physical flow, distinct limiting sensitivity values, perturbation rate, or genericity hypothesis is required.

## Physical equations in fixed dimension

After face parametrization, a spanning-tree routing is affine in the free nomination coordinates. Add a fundamental cycle basis normalized to have coefficient one on its own non-tree edge and zero on the other non-tree edges. There are `r_H` circulation coordinates, bringing the total dimension to at most `9r_H-3` for non-bridge blocks.

For a connected graph, conservation plus orthogonality of the edge-drop vector to a cycle-space basis is equivalent to existence of node potentials. Thus imposing the `r_H` fundamental-cycle equations is sufficient; no additional hidden physical constraints remain. On each sign cell the edge drops and objective are quadratic polynomials in these coordinates.

The zero-flow hyperplanes have polynomially many cells and lower-dimensional faces in fixed dimension. Identically zero flow expressions and coincident hyperplanes can be discarded or treated as fixed zero signs. Polynomial pieces agree at zero-flow boundaries, so using closed cells is safe. Every feasible point of the resulting systems is a physical flow for a nomination in the chosen face, and every physical point is covered.

The compact circulation bound is particularly simple with the chosen basis. The tree-routing component is zero on non-tree edges, so each circulation coordinate equals the physical flow on its own non-tree edge. Physical flow is bounded by a rational global nomination bound `B`; therefore `[-B,B]` is valid. The other coordinates have rational finite nomination bounds. All coefficients have polynomial encoding length, being rational sums and fixed-degree operations on input data.

Exact semialgebraic decision and feasible-point sampling are polynomial in bit complexity when dimension and degree are fixed. Rational objective bisection needs polynomially many calls in input size and requested precision because `B^2 sum beta_e` bounds every path-drop magnitude. The [Basu author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf), Theorem 2.18 and the sampling consequence following Theorem 3.6, provides the standard operation and bit-size bounds used here. Those source bounds were independently checked during the earlier cactus review.

## Fixed blocks and sums of algebraic constants

An inactive fixed-load block has at most `r` circulation coordinates and a unique physical solution. The same sign-cell systems and algebraic sampling yield a representation of algebraic degree bounded as a function of `r`, with polynomial coefficient bit length. This remains valid if the complex algebraic zero set is positive-dimensional: fixed-dimensional real sampling does not require a nonsingular isolated complex root. Uniqueness identifies its real physical sample. Every local normalized potential and block drop is a polynomial expression in the sampled coordinates and remains in the same bounded-degree algebraic field.

Different blocks can yield unrelated algebraic fields. The algorithm correctly approximates their drops separately and sums certified rational intervals, rather than constructing one common primitive element or performing exact sum comparison. The number of blocks and candidate active faces is polynomial for fixed `r`, so this preserves the bit complexity.

## Rational output and precision accounting

The global Lipschitz bound proved in the cactus review uses only positive-conductance sensitivity, the electrical maximum principle, and a path resistance bound. It therefore applies to the present general graph. On the selected face, only `q=O(r)` original core nomination coordinates vary. Isolate each coordinate of an algebraic near-optimal sample in a rational interval of width at most `eta`, keeping the fixed coordinates at their exact rational bounds. Intersect these intervals with the rational nomination bounds and exact balance hyperplane.

The intersection contains the algebraic sample and is a nonempty rational polytope. Rational linear programming returns a rational point of polynomial encoding length. Each changed coordinate differs from the sample by at most `eta`, so the one-norm difference is at most `q eta`. Taking `eta<=epsilon/(4Cq)`, with `C` the positive Lipschitz constant, limits rounding loss to `epsilon/4`. The zero-load case, where `C=0`, is immediate. The nomination may then be disaggregated rationally into its original independent intervals without changing the core objective.

A complete precision budget can allocate `epsilon/4` each to selecting an active face by its certified optimal-value interval, choosing an algebraic local near-optimal sample, and rational nomination rounding. The combined loss is less than `epsilon`. Computing each face's interval to width at most `epsilon/4` also produces a global optimum interval of that width by maximizing all lower and all upper endpoints. This is stronger than the requested width `epsilon` and does not require exact comparison of algebraic constant sums.

The rational output is the nomination vector. Physical flows and potentials can be irrational, and the theorem does not promise a rational tuple satisfying their equations.

## Review boundaries

The second reviewer independently checked the path-shape argument and reported 6,772 exact rational path checks with no failure. This first review supplies the general proof checks and did not use those computations as a substitute for them. The explicit bridge and zero-free-coordinate cases should be retained in the final exposition. No substantive mathematical defect was found in the quadratic theorem; the broader edge-law extension and novelty require their own audits.
