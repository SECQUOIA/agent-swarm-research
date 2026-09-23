# Second independent audit of weighted optimization at fixed global rank and support

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-fixed-support-global-rank.md) establishes polynomial bit-time exact algebraic optimization for fixed total cycle rank and fixed objective support, with independent continuous resistance intervals and a balanced nomination box. The potential perturbation, returning paths, compact limiting argument, and mapping to the reviewed fixed-core theorem are valid. No new novelty assessment is supplied here.

## 1. Pruning and the bounded path skeleton

Removing a zero-objective leaf and adding its nomination interval to its neighbor's interval preserves the attainable objective set. For a fixed original nomination, the retained graph sees the summed nomination; conversely every feasible sum can be disaggregated between the original intervals. The removed leaf's potential does not enter the objective, and its drop can always be reconstructed after choosing any permitted resistance. This does not contract potentials or impose equality of potentials at the removed edge's endpoints.

The repeated operation preserves total rank and objective support. If `c!=0` and `sum c=0`, at least two nonzero objective vertices remain. Every remaining leaf is one of these objective vertices. For actual rank `r'` and leaf count `l`,

```
sum_{deg(v)>=3}(deg(v)-2)=2r'-2+l.
```

Thus at most `2r'+p-2` vertices branch. Marking all of them and all objective vertices gives `s<=2r'+2p-2`. Suppressing the remaining degree-two zero-objective vertices preserves the rank of the connected multigraph, so its number of edges, counted as paths, is `P=s-1+r'<=3r'+2p-3`. Parallel paths and paths returning to their own marked endpoint are permitted. An unmarked cycle component disconnected from the marks cannot arise in a connected graph with nonzero objective support. The `c=0` case is correctly handled before applying these counts.

## 2. The perturbation acts on potentials

For fixed `rho>0`, the smoothed law has derivative `beta_e(2|x_e|+rho)>0`. Its inverse is continuously differentiable. With a normalized potential, the conservation equations therefore have an invertible reduced Laplacian Jacobian, so the physical potential is continuously differentiable in balanced nominations. For a weighted potential objective with balanced coefficient vector `c_delta`, its nomination gradient modulo constants is the electrical adjoint solving `L_rho h=c_delta`.

The candidate uses

```
c_delta=c+delta sum_{v unmarked}(e_v-e_v0).
```

This is exactly the coefficient vector obtained by adding the specified potential differences to the objective. It puts source `delta` at every internal path vertex, while all compensating sources are at a marked reference vertex. Adding nominations to the objective instead would not establish this property; the written perturbation is correct.

For a consistently ordered path, conservation at an internal vertex gives `j_i-j_(i-1)=delta`, with `j_i=(h_i-h_(i+1))/R_i`. Since all `R_i>0`, increasing currents produce an initial increasing segment of potential values, followed by a decreasing segment, with at most one zero-current edge. A horizontal level therefore contains at most two internal vertices, including the possible two-vertex plateau at the maximum. Coincident path endpoints do not affect this recurrence. In a returning path, the two boundary values happen to coincide, and the same conclusion holds.

## 3. Face completeness and removal of perturbations

At a maximizer over the box intersected with balance, the polyhedral normal cone gives a common scalar multiplier `lambda`. Values of the adjoint above it force upper nominations, and those below it force lower nominations. This necessary condition does not require concavity or strict feasibility. A fixed nomination coordinate can take either endpoint status because its two endpoint values coincide.

On a path, the strict unimodal structure gives a contiguous upper-status segment, with lower-status segments on either side, except for at most two coordinates at level `lambda`. The proposed enumeration includes those free coordinates, one-crossing patterns, constant endpoint patterns, and adjacent free coordinates at the maximum plateau. One can implement a deliberately redundant enumeration by choosing up to two free indices and the endpoints of the upper segment among the remaining indices. This has polynomially many choices per path. Leaving all marked coordinates free therefore gives `N^{O(P)}` closed faces and at most

```
s+2P<=8r'+6p-8
```

free nominations. Balance and any forced affine equalities can only decrease this dimension. The family is independent of resistances and of both perturbation parameters.

Here is an explicit justification of the uniform limit. The sign of a passive edge flow agrees with its potential drop, so the directed graph of positive flows is acyclic. Flow decomposition then bounds each physical flow by the total positive nomination, uniformly over bounded balanced nominations and `0<=rho<=1`. The energy is

```
E_rho(x)=sum_e beta_e (|x_e|^3/3+rho*x_e^2/2).
```

For a convergent sequence `(b_k,rho_k)->(b,0)`, these flow bounds give convergent subsequences of physical flows. To compare a feasible competitor at `b` with those at `b_k`, add a fixed linear right-inverse image of `b_k-b`. Passing the energy minimization inequalities to the limit identifies each limit as the unique minimizer of `E_0` at `b`. Thus physical flow depends continuously on `(b,rho)` down to zero. Normalized potentials follow continuously by summing edge drops along a spanning tree. Compactness of the nomination domain makes convergence to `rho=0` uniform.

For `rho<=1`, normalized potentials also have a uniform bound from sums of `beta_e(B^2+B)` along paths. Hence the extra objective term is bounded in magnitude by a constant times `delta`. The two perturbations can tend to zero jointly at any rate. No effective perturbation size is required.

A sequence of perturbed maxima has a subsequence on one fixed enumerated closed face, then a convergent subsequence by compactness. Uniform objective convergence makes the limit an original maximum in that face. For joint optimization, first fix the resistance vector from an attained joint maximum. The fixed-resistance argument finds an equally good nomination in the same resistance-independent family. It is unnecessary to differentiate the resistance choices or prove one universal optimizer across all resistance vectors.

## 4. Fixed-core optimization and exact witnesses

On each face, parameterize the feasible nomination affine space by its `O(r+p)` free coordinates. Degenerate faces can be parameterized in their actual rational affine hull. With a spanning-tree particular flow having zero chord coordinates and a fundamental cycle matrix `C`, every flow has the form `x=x0(z)+Cq`. There are exactly `r'` circulation coordinates, so the core dimension remains fixed.

The flow-sign hyperplanes give polynomially many cells at fixed dimension. Their closed versions cover the bounded core; sign choices at zero flow yield the same zero edge drop. On one cell, let `p_e` be the signed quadratic equal to `x_e|x_e|`. The physical equations beyond conservation are exactly

```
C^T (beta_e p_e)_e=0.
```

There are `r'` such aggregate equations. They guarantee that the edge drops are a potential gradient. Choose a rational tree-supported vector `w` with `Aw=c`, putting zero weight on chords. Then the weighted objective is `sum_e w_e beta_e p_e`, as asserted. This explicitly supplies the weights in the candidate's objective representation.

Each resistance is one scalar bounded polyhedral leaf. Its cycle coefficients and objective coefficient are degree-two rational polynomials in the core. The number of aggregate equations is fixed. The [reviewed fixed-core theorem](../results/fixed-core-block-polyhedral-optimization.md) therefore applies with scalar block dimension, fixed core dimension, fixed aggregate dimension, and degree two. Its hypotheses cover empty cell subproblems and singleton resistance intervals. No convexification of discrete resistance choices is involved or permitted.

The proposed bounds are valid: `|x_e|<=B`, each `q` is its corresponding chord flow, and free nominations inherit finite rational bounds. The bound `B^2 ||c||_1 sum_e beta_e^upper` contains the weighted objective range. All bounds have polynomial binary length. Core boxes and closed sign/nomination constraints are compact; beta intervals are compact; thus algebraic optimization attains its result.

The fixed-core theorem supplies a common polynomial-degree algebraic representation for the winning core, objective, and recovered resistance leaves. Comparing competing algebraic values pairwise does not require combining the fields of all candidates: retain the winning original representation. Greedy disaggregation of pruned nomination intervals uses comparisons and arithmetic in that same field. Removed leaf flows and all original potentials then follow from conservation and the quadratic laws. A polynomial number of such operations retains polynomial representation size. The theorem's algebraic output, rather than a rational-output promise in the presence of cycles, is appropriate.

## 5. Boundaries

The argument uses total cycle rank to bound the number of circulation variables and path segments globally. Bounded rank per block does not provide that fixed-dimensional core. The candidate's final discussion correctly identifies the obstruction from inactive blocks whose boundary loads depend on shared free nominations. The proof also requires independent continuous resistance intervals and the complete nomination-box scenario set, without additional physical feasibility filtering. Changing `c` to `-c` establishes the minimum statement.

## 6. Separate consequence: arbitrary-support tree threshold decisions are in NP

The stronger rational-witness conclusion on trees remains true when objective support grows, even though the polynomial optimization algorithm does not. Consider the decision problem asking whether some balanced nomination in a finite rational box and some independent allowed resistance choices attain `c^T pi>=K`. Allowed choices may be closed positive rational intervals, explicit nonempty finite rational sets, or a mixture of these across edges.

Tree flows are linear rational functions of nominations. For each nomination, every resistance can be moved to its allowed maximum or minimum according to the sign of `w_e x_e|x_e|`, without decreasing the objective. Thus it suffices to consider endpoint resistance choices. Select a closed flow-sign cell containing a global maximizer. This cell has a polynomial-size rational linear description even though the number of possible cells can be exponential. Its objective after endpoint selection is a rational quadratic polynomial of polynomial encoding length over a bounded rational polytope.

A rational quadratic polynomial attaining its maximum on a rational polytope has a polynomial-size rational maximizing point in arbitrary dimension. This is classical rational-QP witness theory due to Vavasis (1990), explicitly restated in Section 2.2, Theorem 3, of Del Pia, Dey, and Molinaro's [primary preprint](https://arxiv.org/pdf/1407.4798). The original paper's [publisher abstract](https://www.sciencedirect.com/science/article/pii/002001909090100C) confirms the NP-membership result; its full text was not needed for this audit.

The tree proof also gives a direct bounded-polytope derivation. At a global maximizer, choose an independent basis of active normals of its minimal face. Stationarity and those active equalities form a rational linear feasibility system of polynomial encoding length. Every feasible solution of that same system has the same quadratic objective, by the two-solution calculation in the [tree audit](review-potential-flow-fixed-support-weighted-tree-second.md). A polynomial-bit rational feasible solution exists. In growing dimension the system need not be found efficiently; its existence is enough for a certificate-size bound.

Consequently a polynomial-size rational nomination and allowed endpoint resistance vector attain the global maximum. Their tree cut flows and normalized quadratic potentials are rational of polynomial size. A verifier checks nomination bounds, balance, allowed resistances, conservation, edge laws, and the threshold entirely with exact rational arithmetic. This proves NP membership for arbitrary-support tree threshold decisions, including equality at the threshold. Applying it to `-c` also handles minimum thresholds.

Combining membership with the independently reviewed [fixed-resistance, degree-three tree hardness construction](potential-flow-weighted-nomination-tree-hardness.md) establishes NP-completeness of the broader tree maximum-threshold problem. The special hardness family remains valid; this extends the membership side to arbitrary weighted objectives and joint interval/finite resistance choices. It does not imply polynomial-time optimization, strong NP-hardness, or the same membership theorem when additional pressure or flow feasibility constraints are imposed.

I separately reread the added section titled “The full tree class is NP-complete” in that hardness note. Its direct stationary-affine-set proof is valid: intersecting the affine stationarity equations with the original bounded polytope gives a nonempty rational polytope, whose rational vertex has polynomial bit size and the same objective as the original optimum. The same maximizing witness certifies a **strict** violation of an upper bound. The claimed robust-bound coNP-completeness also preserves its inequality direction: with bound `K-1/4`, a yes Subset-Sum instance has maximum `K` and violates the bound, while a no instance has maximum at most `K-1/2` and satisfies it. Thus the universal upper-bound predicate is in coNP and is coNP-hard by the complement of the reviewed Subset-Sum reduction.
