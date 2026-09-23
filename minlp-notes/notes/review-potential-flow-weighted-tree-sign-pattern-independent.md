# Independent audit: objective cut-flow direction parameter on trees

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**Verdict: PASS.** The strengthening in [the candidate](potential-flow-weighted-tree-sign-pattern.md) follows from the previously audited tree argument. No correction is required. This review checks mathematical correctness; it does not establish literature novelty or promote the candidate.

## Model and contraction

The result retains the quadratic signed law, positive rational resistance intervals or finite sets, a rational nomination box intersected with balance, and a rational zero-sum weighted potential objective. Reversing an edge reverses both its physical flow and objective cut flow. The product `w_e beta_e x_e |x_e|` is invariant, so orienting every retained edge to make `w_e>0` is valid. This reasoning uses the signed quadratic law specified by the candidate.

Zero-weight contraction uses the cut representation of the objective. It does not assert equal physical potentials inside a contracted cluster. Retained edge flows depend only on the cluster nomination sums, and their objective weights depend only on the cluster objective sums. The image of independent intervals under each cluster sum is exactly the summed interval. Rational disaggregation and physical recovery therefore remain valid. The contracted graph is still a tree, possibly with larger vertex degrees.

## Direction paths and threshold faces

An unmarked vertex has one incoming and one outgoing retained edge, hence undirected degree two. Suppressing these vertices produces a tree on the `k` marked vertices and exactly `k-1` paths. Every path is consistently directed. The internal objective coefficient can be nonzero because consecutive positive cut-flow magnitudes can differ; this does not affect the argument.

For a fixed resistance vector, smoothing gives

```
h_tail-h_head = beta_e (2|x_e|+rho) w_e > 0.
```

Thus the nomination gradient strictly decreases along every directed path. No lower bound on the positive cut weights is needed: smoothing is used to prove existence of a face containing an optimum, not as a numerical approximation algorithm.

The normal cone of the balanced box supplies one common multiplier `lambda`. A coordinate with gradient larger than `lambda` is at its upper bound; one with smaller gradient is at its lower bound. Strict order permits at most one free internal coordinate on each path. Frozen coordinates are compatible with either endpoint designation. If a coordinate with gradient equal to `lambda` is itself at an endpoint, the closed pivot face still contains it.

Leaving all marked coordinates free is valid and simplifies the family. A path with `L` internal vertices has `L+1` cut choices and `L` pivot choices. The product over the `k-1` paths is `N^{O(k)}`. Each face has at most `k+(k-1)=2k-1` free coordinates; shared marked endpoints are counted once. A nontrivial retained tree has `k>=2`. The no-edge case is treated separately.

For each fixed resistance vector, uniform convergence of the smoothed objective on the compact nomination domain and a subsequence in a finite family of closed faces give an unsmoothed optimizer in the same family. The family is independent of resistance values. Holding a resistance vector from a joint optimizer fixed therefore proves completeness for joint optimization as well.

## Exact optimization and complexity

The remaining steps are inherited from [the independently audited fixed-support argument](review-potential-flow-fixed-support-weighted-tree-independent.md): independent resistance endpoint selection, rational flow-sign cells, and exact quadratic optimization by active-face stationarity and linear feasibility. They apply unchanged with a nomination dimension bounded by `2k-1`.

The product of the face count, sign-cell count, and active-face count remains `N^{O(k)}`. Rational coefficient heights and recovery retain polynomial bit bounds. Growing objective support causes no hidden omission: its coefficients are part of the input size, and objective cut sums and their signs are computed exactly. This is an XP statement, not an FPT statement.

## Support comparison and paths

Let `p'` be the support size after contraction; `p'<=p`. Every retained leaf has nonzero objective coefficient, so the number of leaves is at most `p'`. The number of branching vertices is at most `p'-2`. Every marked nonbranching vertex also has nonzero coefficient: this is immediate at a leaf, and at a degree-two source or sink both nonzero currents have the same incidence sign. Consequently `k<=p'+(p'-2)<=2p-2` whenever a retained edge exists.

On a left-to-right path the cut weights are the cumulative left objective sums. After contracting zero-weight edges, a sign change makes the intervening vertex a source or sink; equal consecutive signs make it unmarked. There are exactly two endpoint marks and one mark per sign change. Therefore `k=t+2`, including `k=2` for a nonzero constant-sign sequence. The all-zero sequence belongs to the separate zero-objective case. The polynomial-time conclusion for arbitrary support with constant-sign cut weights is correct.

## Additional mechanism checks

Independently exercised the existing fixed-support checker with the new, smaller directed mark sets. Four path objectives were used: `(1,2,-1,-2)`, `(2,-1,3,-4)`, `(-1,-2,1,2)`, and `(2,-4,1,-2,3)`. Every objective coordinate is nonzero. Their directed mark counts are respectively `2,2,2,3`.

With nomination bounds `[-1,2]` and independent positive resistance intervals, all 1,818 stationary candidates across flow-sign cells agreed with the threshold family, and resistance endpoint choices agreed with exhaustive corner comparisons. These use floating-point stationarity calculations and are supplementary mechanism checks, not substitutes for the exact proof. The structural and bit-complexity conclusions above do not depend on those calculations.
