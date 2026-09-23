# A path-sign refinement of weighted global-rank optimization

Date: 2026-09-05. Status: [independent closing audit PASS](review-potential-flow-weighted-sign-path-decomposition.md), retained as a supporting corollary with no separate priority claim. This directly extends the perturbation in the [verified global-rank/support theorem](../results/potential-flow-fixed-support-global-rank.md); it is not a claim that the underlying adjoint method is new.

## Corollary

Use the same connected quadratic passive network, arbitrary rational balanced nomination box, independent positive resistance intervals, and rational zero-sum weighted potential objective `c^T pi`. Prune zero-objective leaves as in the verified theorem. Suppose there is a nonempty marked set `K` containing every vertex whose degree differs from two, such that on each maximal path with internal vertices outside `K`, the internal coefficients of `c` are either all nonnegative or all nonpositive. Returning paths are permitted. For a pure cycle choose at least one marked reference vertex; split further where needed to meet the sign condition.

If global cycle rank `r` and `k=|K|` are fixed, exact weighted potential optimization and an algebraic optimizing scenario are polynomial-time computable. Objective support need not be fixed. The same result applies when such a marked set is explicitly provided as part of the input; its graph and sign conditions are directly verifiable.

## Structural proof

After suppression, there are `P=k-1+r_actual<=k-1+r` maximal paths. Assign each path a sign `sigma=+1` if its internal objective coefficients are all nonnegative, and `sigma=-1` if they are all nonpositive. Either choice is allowed on an all-zero path. Internal vertices belong to unique maximal paths. Choose a marked reference vertex `v0` and use the perturbed potential objective

```
F_delta,rho(b)=c^T pi^rho(b)
 +delta sum_{v outside K} sigma_path(v) (pi_v^rho(b)-pi_v0^rho(b)).
```

The law smoothing is the same positive-derivative quadratic smoothing as in the verified theorem. The adjoint source at an internal path vertex is `c_v+delta sigma_path(v)`, which is strictly positive or strictly negative throughout that path. Directed adjoint currents therefore strictly increase or strictly decrease along it. Adjoint potentials have a single peak or a single valley, with at most a two-vertex plateau at the extremum.

At a box-and-balance optimum, each horizontal KKT level meets at most two internal vertices per path. On positive-source paths, endpoint nominations follow lower/upper/lower order, apart from at most two free coordinates. On negative-source paths, they follow upper/lower/upper order. Marked nominations are left free. Enumerating these closed patterns gives `N^{O(P+k)}` faces, each with at most

```
k+2P=3k+2r-2
```

free nominations. The family is independent of resistance values and perturbation sizes.

All limiting and algorithmic steps are identical to the verified theorem: uniform convergence on the compact domain, a fixed closed-face subsequence, joint resistance transfer by holding an optimizing resistance vector fixed, all `r` circulation variables in one core, flow-sign cells, and exact fixed-core optimization with scalar resistance leaves. The sign of the perturbation at the marked reference is unrestricted and does not affect internal-path current monotonicity. If the objective is identically zero, handle it directly.

## Relation to earlier parameters

Marking all nonzero objective coefficients and all branching vertices gives the fixed-support theorem as a special case. The present condition can be much weaker: long path segments may contain arbitrarily many positive objective coefficients, or arbitrarily many negative coefficients, without introducing new marked vertices.

On a general skeleton, a suitable set can be found by splitting each original degree-two path whenever the nonzero coefficient sign changes; zero coefficients can be assigned to either neighboring sign segment. One may mark extra vertices rather than minimize `k`; optimization of the decomposition parameter itself is not required for the stated guarantee.

This parameter differs from the [tree cut-direction parameter](potential-flow-weighted-tree-sign-pattern.md). The latter can remain small even when the coefficient signs alternate many times, because it depends on cumulative cut weights. The present refinement instead uses source signs to control adjoint currents when cycles are present.

## Limits and completed verification

The finite-resistance version remains excluded when cycles are present. Global rank remains essential to the available algebraic optimizer. This note does not solve the varying-algebraic-function problem for bounded rank per block.

The [closing independent audit](review-potential-flow-weighted-sign-path-decomposition.md) verifies negative-source valleys, zero-coefficient segments, returning paths, reference compensation, and the unchanged compactness/fixed-core arguments. For minimization, apply the maximum argument to `-c`, reversing path signs and endpoint patterns. The [parent source comparison](potential-flow-fixed-support-global-rank-novelty.md) supplies the prior structural context; no independent novelty claim is made for this refinement.
