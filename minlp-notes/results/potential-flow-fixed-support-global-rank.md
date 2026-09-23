# Exact weighted potential optimization at fixed global cycle rank and objective support

Date: 2026-09-05. Status: verified by two independent full mathematical audits; the focused source comparison found no matching combined guarantee. The proof combines the reviewed positive-source adjoint perturbation with the reviewed fixed-core theorem. The proposed extension is joint nomination and resistance optimization for a weighted objective whose support is fixed.

## Theorem and scope

Fix integers `r,p`. Let `G` be a connected simple graph of global cycle rank at most `r`. Under the common quadratic laws

```
Ax=b,   A^T pi=(beta_e x_e|x_e|)_e,
```

let nominations range over a nonempty rational box intersected with `sum b=0`. Let each resistance range independently over a positive closed rational interval. For a rational vector `c` with `sum c=0` and at most `p` nonzero entries, the exact maximum and minimum of `c^T pi`, together with an algebraic optimizing nomination and resistance scenario, can be computed in polynomial bit time for fixed `r,p`.

The running-time exponent may depend on `r,p`; no fixed-parameter tractable bound is claimed. Global rank is essential to this proof. Additional operating constraints do not filter the nomination/resistance scenarios. Discrete resistance sets are excluded: even support three and global rank one permit NP-hard weighted optimization under independent two-point choices. The [tree theorem](potential-flow-fixed-support-weighted-tree.md) gives the stronger rational-output and finite-resistance conclusions when `r=0`.

## 1. Prune objective-free pendant trees

If a leaf `v` has `c_v=0`, remove its incident edge and merge its nomination interval into that of its neighbor. The remaining network sees the original nomination sum at that neighbor. The leaf contributes no objective coefficient, and its edge drop contributes nothing to `c^T pi`; therefore this operation preserves the set of attainable objective values. Every aggregate nomination can be disaggregated within the original intervals. The removed resistance can take any allowed value. Repeat until no such leaf remains.

These operations preserve global cycle rank and do not increase objective support. If `c=0`, the objective is identically zero and the problem is immediate. Otherwise the remaining graph has at least two vertices with nonzero `c`, and every leaf belongs to that support. Write `l<=p` for its number of leaves. The degree identity

```
sum_v (deg(v)-2)=2r'-2
```

for the actual remaining rank `r'<=r` shows that the number of vertices of degree at least three is at most `2r'+l-2`.

Mark every nonzero-`c` vertex and every vertex of degree at least three. There are at most

```
s<=2r'+2p-2
```

marked vertices. Every unmarked vertex has degree two and coefficient zero. Suppress all unmarked vertices into maximal paths. The resulting connected multigraph on marked vertices can have parallel edges or loops even though the original graph is simple. Its number of paths is

```
P=s-1+r'<=3r'+2p-3.                              (1)
```

A path that returns to the same marked vertex is allowed. The perturbation argument below treats it just as an ordered path with coincident endpoint values.

## 2. Smoothed laws and a positive source at each unmarked vertex

First fix a resistance vector `beta`. For `rho>0`, use the smoothed law

```
g_e^rho(x)=beta_e(x|x|+rho x).
```

Choose one marked reference vertex `v0`. For `delta>0`, optimize the perturbed potential objective

```
F_delta,rho(b)=c^T pi^rho(b)
              +delta sum_{v unmarked}(pi_v^rho(b)-pi_v0^rho(b)).       (2)
```

The perturbation is a sum of POTENTIAL differences. It is not a sum of nominations. Its nomination gradient has the electrical adjoint `h` solving

```
L_rho h=c+delta sum_{v unmarked}(e_v-e_v0),
```

where the edge differential resistances are

```
R_e=beta_e(2|x_e|+rho)>0.
```

Every internal vertex of every suppressed path therefore has adjoint source exactly `delta>0`.

Orient a path as `v_0,...,v_k`, and let its electrical edge currents be

```
j_i=(h_{v_i}-h_{v_{i+1}})/R_i,   0<=i<k.
```

At an internal vertex,

```
j_i-j_{i-1}=delta>0.                             (3)
```

Thus the currents strictly increase, and the successive potential differences `h_{v_{i+1}}-h_{v_i}=-R_i j_i` first can be positive and later negative. The adjoint values are unimodal: they increase and then decrease, with either phase possibly empty. At most one current vanishes, allowing at most a two-vertex plateau at the maximum. Every horizontal level meets at most two internal vertices. This remains true for a returning path with equal endpoint values.

## 3. A finite family with only O(r+p) free nominations

At a maximum of the differentiable objective (2) over the nomination box and balance equation, the polyhedral normal cone yields a scalar `lambda` with

```
h_v>lambda => b_v=u_v,
h_v<lambda => b_v=l_v,
l_v<b_v<u_v => h_v=lambda.
```

Fixed coordinates with equal lower and upper bounds cause no problem. On any suppressed path, the internal endpoint pattern is consequently

```
lower ... lower, upper ... upper, lower ... lower,
```

apart from at most two free coordinates at level crossings. The two free coordinates can be adjacent at a two-vertex maximum plateau. All-upper, all-lower, monotone one-crossing, and zero/one-free-coordinate cases are included.

Enumerate every closed path face with this pattern and zero, one, or two free internal coordinates. Leave all marked nominations free. There are `N^{O(P)}` such faces, and each has at most

```
s+2P<=8r'+6p-8                                  (4)
```

free nomination coordinates. The family depends on topology and nomination bounds, not on resistances, `rho`, or `delta`. Intersect each face with balance and discard infeasible faces.

To remove the analytic perturbations, take a sequence `(delta,rho)->(0,0)` and corresponding perturbed maxima. Passive flows satisfy a uniform bound from total possible positive nomination, independently of `delta,rho`. For `0<rho<=1`, potentials normalized at `v0` are uniformly bounded by sums of `beta_e(B^2+B)` along paths. Strict convex energy minimization gives continuity of the physical state as `rho->0`; compactness then makes the convergence uniform over the nomination domain. Thus (2) converges uniformly to `c^T pi` as both parameters tend to zero.

A convergent subsequence of perturbed maximizers lies on one fixed member of the finite closed face family. Its limit is an original maximizer and belongs to the same face. Zero physical flows therefore do not invalidate the face conclusion. No algorithm chooses a perturbation size; perturbation is used only in this existence proof.

For joint optimization, select a joint maximizer `(b*,beta*)`, which exists on the compact nomination/resistance domain. Hold `beta*` fixed and replace `b*` by an equally good fixed-resistance nomination on the preceding graph-only face family. This preserves the joint maximum. Hence the same finite family is complete for the joint problem without differentiating with respect to resistance variables.

## 4. Exact optimization on each face

On a face, at most `d=O(r+p)` nomination coordinates are free. Eliminate balance when a free coordinate exists; handle a fixed feasible nomination separately. A spanning-tree flow representation gives

```
x=x0(z)+Cq,
```

where `z` comprises the free nomination coordinates and `q` comprises all `r'` chord circulations. Both the particular flow `x0` and every edge flow are rational affine functions of this fixed-dimensional core.

Partition core space into flow-sign cells. At fixed core dimension there are polynomially many such cells. On a closed cell, each signed edge law is

```
beta_e p_e(z,q),
```

with rational quadratic `p_e`. There are `r'` cycle equations, each a sum of these scalar-resistance terms. Expressing normalized potentials along a fixed spanning tree writes the weighted objective as another such aggregate,

```
F(z,q,beta)=sum_e w_e beta_e p_e(z,q),             (5)
```

for rational weights `w_e`. Every resistance interval is one independent scalar polyhedral leaf. Nomination, sign-cell, and balance constraints involve only the fixed-dimensional core.

The reviewed [fixed-core block-polyhedral optimization theorem](../results/fixed-core-block-polyhedral-optimization.md) applies directly: fixed core dimension and fixed aggregate count, scalar interval leaves, rational polynomials of degree two. If needed, include the objective value as one additional core coordinate. It computes the exact algebraic optimum and an algebraic witness in polynomial bit time.

For explicit compact bounds, let

```
B=sum_v max(|l_v|,|u_v|).
```

Every physical flow has magnitude at most `B`; in a fundamental-cycle representation each chord circulation equals its chord flow and can be bounded by `B`. Free nominations inherit their rational box bounds. A safe potential-objective bound is `B^2 ||c||_1 sum_e beta_e^upper`. These bounds have polynomial binary length. Handle `B=0` directly. Thus the fixed-core theorem's compactness and encoding assumptions hold.

There are polynomially many faces and cells for fixed `r,p`. Compare their exact algebraic optima pairwise and keep one winner. All algebraic coordinates of that winning core and leaf witness can be kept in its polynomial-size algebraic representation; no sum of independent block fields is formed. Disaggregate pruned nominations within their original intervals in that same field. Removed edge flows and all normalized potentials are then recovered from conservation and the edge laws.

Changing `c` to `-c` proves the minimum case. Exact outputs may be irrational when cycles remain; the rational-output strengthening is specific to the separate tree theorem.

## 5. Why bounded block rank alone does not follow

The [2026-09-06 joint weighted cactus theorem](potential-flow-joint-weighted-cactus-accuracy-bits.md)
now resolves the cactus case through a new nomination-face reduction and an
accuracy-controlled representation of the local value functions. The following
obstruction explains the limitation of the original proof; the general
noncactus bounded-block-rank algorithm remains unresolved.

A tempting extension would retain fixed objective support while bounding only rank per block. The adjoint block-cut structure suggests that only a bounded number of blocks need contain free nominations. This does not yet prove an algorithm. If several active blocks exchange total nominations, inactive blocks between them have effective boundary loads depending on those totals. Their pressure contributions are algebraic functions of the shared core, rather than algebraic constants. The reviewed one-active-block proof does not optimize sums of these varying functions. A polynomial-time additive optimizer would require an additional controlled representation or approximation theorem, including precision and optimizer recovery; this note claims none.

## Independent verification and source limits

Both [the first independent audit](../notes/review-potential-flow-fixed-support-global-rank.md) and [the second independent audit](../notes/review-potential-flow-fixed-support-global-rank-second.md) passed. They checked pruning, returning paths, the potential-source perturbation, uniform compact limits, joint resistance face transfer, all fixed-core dimensions and bounds, and algebraic witness recovery.

The perturbation mechanism is inherited from the [reviewed bounded-block-rank proof](potential-flow-bounded-block-rank.md), and the fixed-core optimization machinery is also a preceding result. The [focused source audit](../notes/potential-flow-fixed-support-global-rank-novelty.md) found no equivalent exact guarantee combining uncertain nominations, resistance intervals, fixed global rank, and fixed objective support. It credits prior potential-flow sign arrangements, joint uncertainty models, and structural fixed-dimensional methods. The plausible new part is the combined nomination-face extension; the search is not an exhaustive novelty clearance.

## Reproducible structural checks

[`fixed_support_global_rank_checks.py`](../code/potential_flow_mpd/fixed_support_global_rank_checks.py) checked 12 subdivided graphs: single cycles, two cycles joined by a bridge, and cycles attached to a terminal path. It verified 48 suppressed paths, including four returning paths, 506 exact-level or sampled threshold patterns, and 36 balanced-direction finite-difference checks of the perturbed weighted objective against the electrical adjoint. All topology counts and at-most-two-free-coordinate patterns passed. Maximum current-increment error was `5.72e-14`, nomination-gradient error `7.76e-9`, and physical residual `1.22e-12`. These checks target the new weighted/global-skeleton scope; they do not implement the exact real-algebraic optimizer.
