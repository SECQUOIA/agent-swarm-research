# Independent review of the frequency-two envelope oracle

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed, with the routine preprocessing and bit-bound details below made explicit.

Reviewed [the algorithmic result](../results/positive-multilinear-frequency-two-optimization.md). The reduction gives polynomial-time exact evaluation of the scalar convex envelope and a supporting affine minorant for rational unit-cube data. It uses classical matching and rational linear programming; this audit does not establish novelty.

## Binary oracle

For a binary failure vector `Z=1-X`, a positive monomial is one precisely when none of its incident failure edges is selected. Thus its coefficient is an uncovered-vertex penalty. The identity in equation (1), including the constant `-sum lambda_i`, is correct. Single-incidence variables use zero-penalty dummy leaves. Unused variables can be optimized separately; affine terms can be absorbed into the linear objective before constructing the graph.

Every strictly negative-cost edge belongs to an optimum: adding it lowers edge cost and cannot raise any nonnegative uncovered penalty. Fix all such edges to one, add their costs to the constant, and replace their endpoints' penalties by zero. Removing these edges from the remaining decision set then preserves the objective for every remaining edge choice. A fixed edge's endpoints may still occur in other edges; they must not be deleted from the graph.

The hub construction is exact. Any selected original edge set can be completed by the penalty edges for its uncovered vertices and the free hub-mate edge. Conversely, retaining the original edges from an augmented cover can incur only penalties whose hub edges were already paid for. Nonnegative costs justify discarding redundant penalty edges in this comparison. The mate vertex forces the zero-cost hub edge, so the hub itself imposes no additional restriction. Parallel edges cause no difficulty; minimum-cost edge cover can also keep only the cheapest remaining edge between each pair. Isolated original vertices are covered by their penalty edges.

An independent exhaustive calculation compared the original signed-cost prize-collecting objective against the augmented edge-cover objective on 150 seeded small instances. All optimal values agreed exactly using integer arithmetic. Cases included negative and zero costs, zero penalties, parallel edges, and isolated vertices. This checks the reduction, not the internal implementation of a matching algorithm.

The primary [Networks article](https://onlinelibrary.wiley.com/doi/full/10.1002/net.22261) explicitly gives the classical weighted-edge-cover reduction to weighted matching using transformed weights `mu(u)+mu(v)-w(uv)`. The present reduction reaches its ordinary nonnegative-cost setting.

## Exact rational envelope computation

The distribution LP and dual are correct. Separation at `(eta,lambda)` minimizes `f(v)-lambda^T v` over binary vectors. If its minimum is below `eta`, an attaining binary vector returns an explicitly violated dual inequality; otherwise the candidate satisfies every dual inequality.

The polynomial-bit assertion can be justified without assuming the dual is bounded. Its constraint normals `(1,v)`, as `v` ranges over the cube vertices, span the full `(n+1)`-dimensional space. Hence its recession cone contains no line. The primal is feasible and bounded at every cube point, including its boundary, so the dual has a nonempty optimal face. This face contains a dual vertex. Each vertex solves `n+1` independent tight equations with a nonsingular 0/1 matrix and right-hand sides `f(v)`.

Write `A=sum a_e` after removing affine terms. Cramer's rule gives a sufficient coordinate bound

```
B = max{1, (n+1)! A}.
```

Indeed, the determinant is a nonzero integer, and the numerator determinant has at most `(n+1)!` terms, each with magnitude at most `A`. Thus a box `|eta|,|lambda_i|<=B` retains an optimal dual vertex. This bound has polynomial encoding length. A common denominator for the rational coefficients has bit length at most the sum of their input denominator lengths; applying the same determinant argument after clearing denominators gives polynomial encoding lengths for exact optimal coordinates. The usual rational separation-to-optimization theorem therefore applies with polynomial dimension, coefficient complexity, and oracle running time. No enumeration of the exponentially many dual constraints is needed.

The returned affine minorant supports the convex envelope at the query point and globally underestimates the polynomial because its vertex inequalities extend throughout the cube by multilinearity. The explicit concave envelope supplies upper separating pieces. Together with coordinate bounds this separates the scalar graph hull. The result does not imply a polynomial-size formulation of the full lifted multilinear polytope, nor does it assert extension to arbitrary positive lower bounds.
