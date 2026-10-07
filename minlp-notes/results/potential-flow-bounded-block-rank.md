# Polynomial additive potential optimization with bounded cycle rank in every block

Date: 2026-09-05. Status: passed [first independent mathematical review](../notes/review-potential-flow-bounded-cycle-rank.md) and [second independent mathematical review](../notes/review-potential-flow-bounded-cycle-rank-second.md). A root proof review was also reported, but no separate record of it is retained; the two linked reviews are the documented independent reviews. A [separate bounded novelty audit](../notes/potential-flow-bounded-cycle-rank-novelty.md) found no matching open-literature theorem. These are internal research checks, not external peer review, and novelty remains provisional.

This extends the [cactus theorem](potential-flow-cactus-additive-optimization.md) to interacting cycles, including arbitrarily subdivided theta and K4 blocks, while allowing arbitrarily many such blocks.

## Theorem

Fix a positive integer `r`. On connected passive quadratic flow networks in which every biconnected block has cycle rank at most `r`, maximum potential difference over a nonempty balanced rational nomination box admits a certified additive optimal-value interval and a rational epsilon-optimal nomination in time polynomial in the input bit length and requested precision bits. The polynomial exponent may depend on `r`. This is a fixed-parameter-value polynomial guarantee (an XP-type dependence), not a claim of fixed-parameter tractability `f(r) poly(n)`.

Broader constitutive-law extensions are separate research and are not included in this reviewed quadratic theorem.

There are no flow-capacity or potential bounds in the MPD subproblem. Source and sink in the objective may be arbitrary vertices; all signed nomination intervals may be shifted. Exact equality-sensitive threshold comparison is not claimed.

## One active block on an arbitrary graph

Aggregate branches away from the `s-t` block path as before. The one-block saturation lemma does not need every block to be a cycle. For a smoothed electrical adjoint, internal vertices of a biconnected block lie strictly between its entrance and exit values. The strong maximum principle and two-vertex-connectivity prove strictness. Consecutive blocks have ordered, disjoint open ranges. A single balance multiplier therefore leaves all free nominations in one block, with every earlier core vertex at its upper bound and every later core vertex at its lower bound. The smoothing/compactness limit gives the same existential face statement for the original quadratic law.

Fix one such selected active block, with entrance `a` and exit `c`. Outside effective nominations and all other block drops are constants. The local objective is `F=pi_a-pi_c`; local nomination bounds are rational, shifted at `a,c` by fixed outside totals, and their sum must be zero. We can optimize this local subproblem separately.

## Suppression topology

Let `H` be a biconnected non-bridge block, with `m` edges, `n` vertices, and cycle rank `r_H=m-n+1<=r`. All vertices have degree at least two. Define the topological core `K` to contain all vertices of degree at least three, plus the two distinct objective terminals `a,c`.

Since

```
sum_v (deg(v)-2)=2r_H-2,
```

there are at most `2r_H-2` vertices of degree at least three, and `|K|<=2r_H`. Every other vertex belongs to the interior of one maximal path with endpoints in `K` and all internal vertices of degree two. Suppressing these interiors preserves cycle rank. The number `p` of maximal paths is

```
p=r_H+|K|-1<=3r_H-1.
```

Parallel paths are allowed in the suppressed graph. In the rank-one case, `K={a,c}` and the two paths are the cycle's two terminal branches. Bridge blocks require no suppression and have only two vertices.

## A small perturbation forces unimodal adjoints on every long path

The unperturbed adjoint can be constant along a degree-two path whose endpoint adjoint values coincide. If that constant equals the KKT multiplier, first-order optimality alone leaves every internal nomination free. Perturb the **objective**, in addition to the law smoothing, to prevent this flat-path degeneracy:

```
phi_e,rho(x)=beta_e(x|x|+rho x),
F_delta,rho(b)=pi_a-pi_c
               +delta sum_{v not in K}(pi_v-pi_c),
rho>0, delta>0.
```

Every potential here is from the smoothed physical solution at the same nomination. The perturbation vanishes uniformly over the compact nomination polytope as `delta,rho` tend to zero: physical flows remain uniformly bounded by total possible positive injection, and every normalized potential is uniformly bounded by summing edge drops along a path.

Let `h_c=0` and let `h` be the adjoint derivative of `F_delta,rho`. Then

```
L h = e_a-e_c+delta sum_{v not in K}(e_v-e_c),
L = B diag(1/[beta_e(2|x_e|+rho)]) B^T.
```

At every internal vertex of every maximal degree-two path, the adjoint source is exactly `delta>0`.

Write one path as `v_0,...,v_k`, oriented from `v_0` to `v_k`, and let `R_i>0` be its electrical resistance. Define the oriented electrical current on edge `v_i v_{i+1}` by

```
j_i=(h_{v_i}-h_{v_{i+1}})/R_i.
```

The internal-node equation is

```
j_i-j_{i-1}=delta>0.                       (1)
```

Thus the currents strictly increase along the path. Since the sign of `h_{v_i}-h_{v_{i+1}}` is the sign of `j_i`, the adjoint values first strictly increase, then strictly decrease. One or both phases may be empty. At most one edge can have zero current, and therefore a plateau can consist of at most two adjacent vertices, at the maximum.

In particular every real level `lambda` is attained at no more than two vertices of the path. The strict upper-level set `{v_i:h_{v_i}>lambda}` is an interval in path order. The same conclusions hold when considering only path-internal vertices.

## Polynomially many bounded-dimensional nomination faces

At a perturbed optimum, a scalar balance multiplier `lambda` yields

```
h_v>lambda -> b_v=u_v,
h_v<lambda -> b_v=l_v.
```

On each maximal path, internal nominations therefore have the pattern

```
lower bounds / optional free pivot / upper bounds
             / optional free pivot / lower bounds,           (2)
```

where the middle upper segment may be empty or extend to an endpoint. A peak plateau at level `lambda` leaves its two adjacent vertices free and the upper segment empty. A purely monotone sequence is included. Thus at most two internal vertices per path are free, and the possible patterns are enumerable in `O(k_path^2)` choices, by selecting the two boundaries (including vertex and gap locations) of the upper interval. Core vertices are independently lower-saturated, upper-saturated, or free; there are at most `3^{|K|}` choices.

Combining paths gives `n^{O(r)}` faces. Each has at most

```
|K|+2p <= 8r_H-2
```

free nominations. Impose the exact rational balance equation and discard infeasible faces. Every retained face is a subset of the local nomination polytope.

Choose any sequence `delta,rho ->0` and a maximizer of each perturbed local problem. Compactness gives a convergent subsequence; uniform convergence makes the limit optimal for the original local problem. There are only finitely many faces of form (2), so a further subsequence belongs to a single closed face. Its limit remains in that face. Hence at least one original optimum belongs to the enumerated family. Neither a perturbation size nor a genericity assumption is needed in the algorithm: perturbation is used only to prove existence of an optimal face.

## Fixed-dimensional polynomial optimization

Bridge blocks can be solved directly: after conservation their through-flow and potential drop are monotone in the single free nomination parameter, so the optimum is an interval endpoint. The dimension formulas in this section concern non-bridge blocks (`r_H>=1`). Faces with no free nominations are constant physical-flow problems and bypass nomination elimination. For every other retained face, parameterize it using all but one of its free nomination coordinates; the last follows from balance. There are at most `8r_H-3` independent nomination coordinates. Choose a spanning tree of the active block and a fundamental cycle basis. Every flow is an affine function of these nomination coordinates and `r_H` circulation coordinates. The total dimension is at most `9r_H-3`, a constant for fixed `r`.

Each edge-flow zero set is an affine hyperplane. Enumerate the polynomially many cells and faces of this arrangement in fixed dimension. On each cell, the quadratic potential law is polynomial. Impose the `r_H` fundamental-cycle equations, the rational nomination bounds, and the cell inequalities. The local potential difference is a quadratic polynomial, so adding a rational objective threshold yields a fixed-dimensional degree-two semialgebraic decision problem.

All physical flows have absolute value at most a rational global bound `B`. In a fundamental-cycle basis normalized on the non-tree edges, each circulation coordinate equals the corresponding non-tree-edge flow, because the tree routing is zero there. Thus `[-B,B]` bounds these coordinates. Nomination bounds already bound the other variables. All polynomial coefficients and bounds have polynomial bit length. Fixed-dimensional real algebraic decision and sampling, followed by binary search, give a certified local optimum interval and an algebraic near-optimal nomination in polynomial bit time for fixed `r`.

## Inactive blocks and rational recovery

A fixed-load block has at most `r` circulation coordinates and no free nominations. The same hyperplane arrangement and polynomial equations give a fixed-dimensional physical-flow system with a unique solution. Its normalized potentials and block drop are algebraic numbers of degree bounded as a function of `r`, with polynomial coefficient bit lengths. Approximate each constant drop to prescribed precision and sum intervals, instead of performing exact radical comparison.

For rational nomination output, retain the Lipschitz bound from the cactus theorem, which in fact holds on every connected graph:

```
|F(b)-F(c)| <= [2B sum_{e in P} beta_e] ||b-c||_1
```

for any fixed simple `s-t` path `P`. The selected active face has `O(r)` free coordinates. Refine rational isolating intervals for its algebraic nomination to sufficiently small width; intersect those intervals with the original rational box and exact balance hyperplane. This rational polytope contains the algebraic sample, so rational linear programming finds a rational point with the required l1 proximity. Disaggregate original nomination groups rationally. The usual precision budget gives a feasible rational epsilon-optimal nomination and an epsilon-width optimal-value interval.

## Established ingredients and contribution

The new point beyond the cactus theorem is the positive-internal-source adjoint perturbation: it replaces potentially flat paths by unimodal paths and bounds the number of free nominations in terms of block cycle rank. The weighted-Laplacian derivative has an explicit antecedent in Misra, Vuffray, and Chertkov (2015), Lemma 1, equations (19) and (21); [primary preprint](https://arxiv.org/abs/1504.02370). Spanning-tree circulation coordinates, topological path suppression, electrical maximum principles, and fixed-dimensional real algebraic algorithms are established tools. The [novelty audit](../notes/potential-flow-bounded-cycle-rank-novelty.md) records the precise distinction and the closest low-cycle probabilistic-flow literature.

The real algebraic calls use fixed dimension, fixed polynomial degree, and polynomially many rational coefficients. Basu's [author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf), Theorem 2.18, includes quantifier-elimination bit-size bounds, and Theorem 3.6 with its following corollary gives algebraic sampling and coefficient bounds. These provide polynomial bit complexity for each fixed rank bound. The algebraic solver need not be numerically practical.

## Why bounded treewidth or one feedback vertex does not suffice

The following limitation is a consequence of an existing reduction, credited to Thürauf, rather than a new independent hardness construction. In *Deciding the feasibility of a booking in the European gas market is coNP-hard* (2022), Section 4, Figure 2, the underlying graph has vertices `s,t,z_i^+,z_i^-` and edges `s-z_i^+`, `z_i^+-t`, and `z_i^+-z_i^-`. Its main block is `K_{2,n}` and has cycle rank `n-1`. [Open author manuscript](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf).

This graph has treewidth at most two: use bags `{s,t,z_i^+}` in a path, with each leaf bag `{z_i^+,z_i^-}` attached to its corresponding bag. It is series-parallel as an undirected graph. Deleting `s` leaves a tree, so its feedback-vertex number is one for `n>=2`.

The cited Lemma 4.3 gives MPD at least one for a yes Partition instance; Lemma 4.17 gives MPD below a rational threshold `T(K)<1` for a no instance. Its equation (3) constructs `T(K)` using a fixed number of rational operations and maxima involving `K,n`, so its binary encoding length is polynomial in the Partition input size. Let `g=1-T(K)>0`. An optimal-value interval of width `g/4` distinguishes these cases by comparison with `(1+T(K))/2`; the requested number of precision bits is polynomial in the Partition input size.

Therefore, unless `P=NP`, the present polynomial-in-input-and-precision guarantee cannot hold on all graphs of treewidth two, all series-parallel graphs, or all graphs with feedback-vertex number one. There is no conflict with the theorem: the hardness instances place unbounded cycle rank inside a single block. This distinguishes a bound on independent cycles per block from a bound on vertices whose deletion breaks cycles.

## Reproducible checks

[`code/potential_flow_mpd/block_rank_checks.py`](../code/potential_flow_mpd/block_rank_checks.py) checks suppression topology, smoothed physical-flow and adjoint derivatives, positive-source current increments, unimodal threshold-face coverage, and an exact two-vertex maximum plateau. Its deterministic run on 2026-09-05 passed 18 subdivided theta and K4 blocks, including objective terminals originally of degree two, with 105 maximal paths and 911 sampled/exact-level threshold patterns. The maximum current-identity error was `2.03e-14`, the maximum balanced-direction finite-difference error for the nonlinear perturbed objective was `3.9e-9`, and the maximum physical residual was `6.85e-13`.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/block_rank_checks.py`. The plateau check uses exact integers: adjoint values `0,2,3,3,2,0` generate currents `-2,-1,0,1,2`, so every internal increment is one and the maximum has exactly two adjacent vertices. These checks support the novel local mechanism; they do not implement or replace the real-algebraic global optimization proof.
