# Polynomial additive optimization of quadratic potential difference on cacti

Date: 2026-09-05. Status: passed [first independent mathematical review](../notes/review-potential-flow-cactus-approximation.md) and [second independent mathematical review](../notes/review-potential-flow-cactus-approximation-second.md). A root proof review was also reported, but no separate record of it is retained; the two linked reviews are the documented independent reviews. A [separate bounded novelty audit](../notes/potential-flow-cactus-approximation-novelty.md) found no matching open-literature theorem. Novelty remains provisional; these reviews are not external peer review.

**Main theorem.** For a connected cactus with positive rational resistances, quadratic passive potential law, finite rational signed nomination intervals, and a nonempty balanced nomination polytope, maximum potential difference between any two distinct vertices admits additive approximation in polynomial bit time. Given rational `0<epsilon<=1`, the algorithm returns a certified rational interval of width at most `epsilon` containing the optimum and a feasible rational nomination within additive `epsilon` of it. Its running time is polynomial in input binary length and `log(1/epsilon)`.

The physical equations are `B x=b` and `pi_u-pi_v=beta_e x_e|x_e|`. Feasible nominations satisfy `l_v<=b_v<=u_v` and `sum_v b_v=0` exactly. All edge flows are determined by the unique passive solution and may have either sign. No additional flow capacities, potential bounds, compressors, or switches are imposed in this MPD subproblem. The theorem does not promise rational physical flows or potentials, and does not decide equality-sensitive booking feasibility exactly. [Exact threshold comparison already captures Square-Root Sum](potential-flow-cactus-square-root-sum.md).

The principal structural result is that after aggregating branches away from the objective-terminal block path, one optimum belongs to a polynomially enumerable family of faces with at most two free loads, both in one cycle. Fixed-dimensional algebraic optimization and controlled numerical evaluation of the other blocks then give the algorithm.

## All unsaturated loads can be localized to one block

**Lemma 1.** On a passive quadratic cactus with independent finite interval loads `l_v<=b_v<=u_v` and a nonempty balanced nomination polytope `sum b_v=0`, there is an MPD-maximizing nomination with the following form. First aggregate every component off the `s-t` block path into its attachment vertex, adding its load intervals. Then choose one block on that path. Every core vertex strictly before that block is at its aggregated upper load bound; every core vertex strictly after it is at its aggregated lower bound. Only vertices in the selected block can remain unsaturated. A block is a bridge or a cycle; the entire selected block's vertex set is left free.

Here "before" and "after" mean the natural order of blocks from `s` to `t`; the selected block's entrance and exit are included among its free vertices. There are only linearly many such faces of the nomination polytope. This does not say every optimizer has the form, and does not imply exact polynomial bit complexity.

**Aggregation justification.** Assign each vertex outside the union of the blocks on the `s-t` block-cut-tree path to its unique attachment vertex on that union. For any core vertex, feasible totals of its assigned original loads fill the sum interval `[sum l_v,sum u_v]`. There are no shared variables between groups. Given the totals, the flows on the core depend only on those totals by conservation and uniqueness. Conversely every selection of group totals can be distributed inside its intervals, and the original network has a unique passive flow. Thus the objective and attainable core-load vectors are preserved exactly. Potential or flow bounds would invalidate this argument; none are imposed here.

**Proof.** Replace each edge law by

```
phi_e,rho(x)=beta_e (x|x|+rho x),   rho>0.
```

For a fixed positive `rho`, its derivative is strictly positive. Normalize physical potentials at `t`. The objective `F_rho(b)=pi_s-pi_t` is continuously differentiable on balanced loads. Its derivative in any balanced direction `d` is `h^T d`, where

```
L h=e_s-e_t,    h_t=0,
L = B diag(1/phi'_e,rho(x_e)) B^T.
```

Here `B` is the vertex-edge incidence matrix. This follows by differentiating conservation expressed as flows in inverse potential differences, and using symmetry of `L`. All conductances in this linear electrical network are positive.

At any global maximizer of the smooth objective over the balanced box, first-order optimality gives a scalar `lambda` such that

```
h_v>lambda implies b_v=u_v,
h_v<lambda implies b_v=l_v.                 (7)
```

No nonlinear constraint qualification is required: the first-order condition says that the same point maximizes the linear functional `h^T b` over its feasible polytope, and linear-programming duality yields (7). Coordinates with equal lower and upper bounds need no special treatment.

On a cactus core, the electrical unit `s-t` current traverses each block in series. Across every bridge, `h` strictly decreases. Across every cycle, its two entrance-to-exit branches both carry positive electrical current, so `h` strictly decreases along both branches. Therefore each block's interior `h` values lie strictly between its entrance and exit values, and the ranges of consecutive blocks are ordered, intersecting only at shared endpoints. If `lambda` lies between `h_s` and `h_t`, select a block whose closed range contains it. Equation (7) gives the asserted saturation outside this block. If `lambda>h_s`, all vertices are at lower bounds; if `lambda<h_t`, all are at upper bounds. In the all-lower case choose the first block: there are no earlier vertices, and all later vertices are at lower bounds. In the all-upper case choose the last block. Both cases have the asserted form. Equality at `h_s` or `h_t` is handled by the first or last block.

It remains to pass to `rho=0`. The feasible load polytope is compact. Uniformly over it, a spanning-tree routing provides a bounded feasible flow. Energy minimization for the smoothed law uses

```
E_rho(x)=sum_e beta_e (|x_e|^3/3+rho x_e^2/2).
```

For `0<rho<=1`, comparison with the bounded routing and the positive cubic term uniformly bounds every optimizing flow. If `rho_k->0` and `b_k->b`, every convergent subsequence of the optimal flows minimizes the original energy at `b`: compare against a feasible test flow for `b`, corrected along a spanning tree by the vanishing imbalance `b_k-b`. Original strict convexity makes this limit unique. Recovering normalized potentials by adding edge drops along a fixed tree then proves continuity in this joint limit. In particular `F_rho` converges uniformly to `F_0` on the compact nomination polytope, by the usual subsequence contradiction argument.

Choose smoothed maximizers as `rho` decreases to zero. Their limits are original maximizers by uniform convergence. Since there are finitely many selected-block faces, a subsequence uses one fixed face; the face is closed, so its limiting maximizer has the asserted saturation pattern.

**Consequence.** MPD is the maximum over the selected-block faces. The next step refines each cycle face to at most two free loads, so the apparent dependence on the number of internal vertices disappears from the continuous dimension.

## Polynomial bit complexity of additive optimization

### Polynomially many one-dimensional nomination faces

The electrical sensitivity in the smoothed proof strictly decreases along each of the two branches of a cycle block. A common multiplier `lambda` can therefore equal `h` at at most one vertex on each branch. Values in distinct blocks have disjoint open ranges. If `lambda` equals an articulation value, it equals no other core vertex's value. Consequently there is a maximizing nomination with at most two unsaturated core loads; if there are two, they belong to the same cycle, one in the interior of each entrance-to-exit branch.

More precisely, on each branch, all vertices before the threshold are at upper bounds, all after it at lower bounds, and there is at most one free pivot vertex. A threshold between adjacent vertices leaves the entire branch saturated. The locations of the two thresholds, including vertex and gap locations, have `O(k^2)` possibilities for a `k`-vertex cycle. Bridge blocks and singleton thresholds at `s`, `t`, or an articulation yield only linearly many additional patterns. Include all-lower and all-upper patterns when they satisfy balance; they are also covered by the first/last-block cases. Every earlier core vertex is upper-saturated and every later vertex is lower-saturated. Thus at most `O(n^2)` faces suffice. These faces depend only on the graph order and the load bounds, not on resistances or unknown sensitivities.

The smoothing/compactness limit preserves one of these finitely many closed faces. The balance equation eliminates all but at most one scalar nomination parameter `z`. Its feasible range is a rational closed interval, found by intersecting the bounds on the one or two pivots. Each retained face consists entirely of feasible nominations; every such nomination has a unique physical flow. At least one retained face contains a global optimum.

### Separating the active block from constant contributions

On a face with two free pivots, their sum is fixed by balance. Their common cycle therefore has a fixed total load, even as `z` changes. Every other block has fixed local loads, including the total contribution from all downstream/upstream attached groups. Conservation and uniqueness imply that its flow and its contribution to `pi_s-pi_t` are fixed. Thus the objective is

```
F(z)=C+g(z),
```

where `C` is a sum of fixed-block drops and `g` is the drop across the one variable cycle. If there is at most one pivot, balance fixes every load and the entire objective is constant.

For a fixed-load cycle, choose a spanning path and express all flows as `x_e=c_e+sigma_e w` with rational `c_e` and `sigma_e` equal to `+1` or `-1`. Its loop equation is

```
sum_e sigma_e beta_e x_e |x_e|=0.
```

The breakpoints at which an edge flow vanishes are rational and can be sorted. On each interval the equation is a polynomial of degree at most two. It has a unique global root by strict monotonicity, which can be isolated with polynomial-size rational data and represented as an algebraic number of degree at most two. Each fixed-block drop is consequently algebraic of degree at most two. It can be approximated to prescribed absolute precision in polynomial bit time. Summing approximations to the linearly many block drops, each to error `epsilon/(16n)`, gives a certified approximation to `C`; exact comparison of their sum is not required.

### Fixed-dimensional optimization on the active cycle

On the active cycle, choose a spanning path. Its tree-routing flow is affine in the nomination parameter `z`; adding one circulation `w` gives

```
x_e(z,w)=c_e+d_e z+sigma_e w
```

with rational coefficients of polynomial encoding length. The lines `x_e(z,w)=0` partition the plane into `O(k^2)` cells and their lower-dimensional faces. Enumerate their closures, retaining each feasible sign pattern. On each cell, the loop equation is a degree-at-most-two polynomial equality, the interval bound on `z` and the cell sign conditions are linear inequalities, and the active potential difference `g(z,w)` is a polynomial of degree at most two. Zero-flow edges cause no ambiguity: both polynomial pieces give zero on their shared boundary.

For clarity, intersect each cell with a rational compact box containing all feasible physical flows and circulations. Let `B=sum_v max(|l_v|,|u_v|)`. Every physical flow has absolute value at most `B`: orient each nonzero edge along its physical flow, observe that the potential strictly decreases on it, and decompose the resulting acyclic flow into paths from injections to withdrawals. Its total injection is at most `B`. Spanning-tree routings also have absolute values at most `B`. Hence `|w|<=2B` suffices for a cycle circulation normalized to have entries `+1` or `-1`. All nomination parameters already have rational finite bounds.

Exact feasibility of the above system with one further inequality `g(z,w)>=r`, for rational `r`, is a fixed-dimensional semialgebraic decision problem: two real variables, fixed degree, and polynomially many rational constraints of polynomial encoding length. The standard fixed-dimensional algorithms run in polynomial bit time. A rational objective bound follows from `|x_e|<=B`: every path drop has absolute value at most `M=B^2 sum_e beta_e`. Binary search between `-M` and `M`, with these exact decision calls, returns an interval of any desired rational width around the active-block optimum using a number of calls polynomial in input length and `log(1/epsilon)`.

After adding the certified constant intervals, maximize the resulting lower and upper bounds over all faces. If every face interval has width at most `epsilon`, taking the maximum of its lower endpoints and the maximum of its upper endpoints gives an MPD interval of width at most `epsilon`. The exact SRS barrier survives in the absence of an additive tolerance.

### A Lipschitz bound and rational nomination output

The returned nomination can be rational even though its physical flow and potentials need not be rational. The following quantitative bound, supplied by the independent reviewer, certifies rounding of the nomination parameter.

Let `b,c` be two balanced feasible core nominations and set

```
B=sum_v max(|l_v|,|u_v|).
```

Fix any simple `s-t` path `P` in the core and define the rational constant

```
C=2B sum_{e in P} beta_e.
```

Then

```
|F_0(b)-F_0(c)| <= C ||b-c||_1.             (8)
```

To prove this, first use the smoothed law. Every physical edge flow has absolute value at most `B`, because its nonzero-flow orientation is acyclic and total positive injection is at most `B`. The electrical derivative resistance is therefore

```
r_e=beta_e(2|x_e|+rho)<=beta_e(2B+rho).
```

The derivative potential `h` has minimum `h_t=0` and maximum `h_s`, by the electrical maximum principle. Its range `h_s-h_t` is the effective resistance of this derivative network. Electrical energy minimization, tested against a unit flow along `P`, gives

```
0<=h_v<=h_s<=sum_{e in P}r_e
               <=(2B+rho)sum_{e in P}beta_e.
```

Integrate the directional derivative `h^T(c-b)` along the line segment between `b` and `c`, which remains in the balanced box. Its absolute value is bounded by the last display times `||b-c||_1`. Uniform convergence of smoothed objectives, already proved above, permits `rho` to decrease to zero and proves (8). This argument applies to any connected graph; the cactus structure is needed for the face reduction.

On a face with two pivots, moving the nomination parameter `z` by at most `eta` moves their loads by opposite amounts, so the load-vector change has l1 norm at most `2 eta`. If `C>0`, choose

```
eta<=epsilon/(8C).
```

Rounding `z` to a rational point in its feasible rational interval within distance `eta` then loses at most `epsilon/4` in objective. The required precision has polynomial bit length. Refine an algebraic isolating interval for `z` and choose a rational point inside the distance allowance and the nomination interval. Endpoint cases are harmless, since those endpoints themselves are rational. If `C=0`, the objective is constant zero. Distribute each rational aggregated group total among its original rational intervals greedily; this produces an exactly balanced rational nomination in the original network.

To select a face, compute its optimal-value interval to width at most `epsilon/4` and select a face with the greatest lower endpoint. Its exact optimum is within `epsilon/4` of the global optimum. Sample an algebraic feasible local point within `epsilon/4` of that face optimum, then use (8) to lose at most another `epsilon/4` during rational nomination rounding. The total loss is below `epsilon`. The claimed output is a rational nomination and a certified optimal-value interval; it is **not** a rational tuple of physical flows and potentials. Those values can be irrational.

### Real algebraic subroutine source

The complexity and output claims use fixed dimension, fixed polynomial degree, and binary rational coefficients. A primary source is Saugata Basu's [survey on algorithms in real algebraic geometry](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf): Theorem 2.18 gives quantifier-elimination bounds including intermediate integer bit sizes, while Theorem 3.6 and its following corollary provide algebraic sample-point algorithms and coefficient bounds. With at most two variables in each active-cycle feasibility system (or a fixed additional objective variable when needed), these bounds are polynomial in the number of polynomials and their coefficient bit lengths. Rational coefficients may first be cleared by positive denominators with polynomial bit growth. This invokes an established subroutine; the new result is the network reduction that makes its dimension fixed independently of the cactus size.

### Relationship to earlier sensitivity and robustness results

The electrical sensitivity identity is established. Misra, Vuffray, and Chertkov, [*Maximum Throughput Problem in Dissipative Flow Networks with Application to Natural Gas Systems*](https://arxiv.org/abs/1504.02370), Lemma 1(a), equation (19), identifies potentials as the gradient of the conjugate energy; Lemma 1(b), equation (21), identifies its Hessian with the inverse grounded weighted Laplacian. The adjoint representation used here follows from that identity. The contribution is the global cactus threshold-face reduction, including the zero-flow smoothing limit, and its use to obtain polynomial bit complexity for additive approximation. Neither the energy principle nor the weighted-Laplacian derivative is claimed as new.

Vuffray, Misra, and Chertkov's [robust monotonicity paper](https://arxiv.org/abs/1504.00910) fixes terminal potentials and permits corresponding terminal injections to adjust. This is different from optimizing a terminal potential difference over the full balanced nomination box used here. The independent novelty audit checks that distinction rather than treating all robust-flow models as equivalent.

### Reproducible numerical evidence

[`code/potential_flow_mpd/cactus_nomination_faces.py`](../code/potential_flow_mpd/cactus_nomination_faces.py) implements exact rational off-path aggregation, interval disaggregation, and the polynomial face enumeration. Its numerical routine searches each one-dimensional face and compares with an independent seven-start SLSQP search over the full balanced nomination box. It does not implement fixed-dimensional real algebraic optimization and is not a certified global solver.

On 2026-09-05, the deterministic 20-instance run used two cycle blocks, a bridge, an attached off-path cycle, four different objective-terminal pairs, arbitrary balanced shifts of interval loads, and rational resistances. It checked 32 feasible faces, including two nondegenerate one-dimensional faces. The largest amount by which a full-space numerical objective exceeded the face search was `1.09e-7`; this is within the numerical comparison tolerance `2e-5`. Exact rational balance/bounds checks, original/core objective agreement after interval disaggregation, and the Lipschitz bound checks passed. The maximum recorded physical residual was `1.21e-12`.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/cactus_nomination_faces.py`. These small numerical checks support the combinatorial reduction and implementation; the theorem rests on the independent analytical reviews and the cited real-algebraic algorithms.

## Significance and literature scope

The single-cycle polynomial algorithm of Labbé, Plein, Schmidt, and Thürauf already combines structural nomination restrictions with fixed-dimensional real algebraic geometry. The present theorem extends additive optimization across arbitrarily many cactus blocks and allows arbitrary shifted rational nomination intervals. Thürauf's 2022 general-network hardness paper explicitly proposes cactus classification and approximate MPD for tolerance booking checks as further directions. The 2026 overview still lists nonlinear cactus MPD complexity as open. The [novelty audit](../notes/potential-flow-cactus-approximation-novelty.md) compares these primary sources and the later April 2026 network-design paper. This result answers the additive-approximation problem, with polynomial dependence on precision bits; it does not classify exact multi-entry cactus decision complexity.
