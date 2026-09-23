# Conditioned box followers: approximation source audit

Date: 2026-09-05. Bounded source assessment of
[the promoted conditioned-box result](../results/bilevel-conditioned-box-additive-algorithm.md),
read in its completed investigation version. The author reports two passing
independent proof reviews before promotion.
This note is not an independent mathematical verification.

## Candidate scope and defensible distinction

Fix the leader dimension `r`. The follower minimizes
`.5 z^T Q z + (c+Dx)^T z` over `[0,1]^N`, where `Q` is rational positive
definite and `x` belongs to a nonempty explicitly described rational polytope
inside `[0,1]^r`. The upper objective is `a^T z(x)+b^T x`.
The proposed algorithm obtains additive error `epsilon ||a||_1` in time
polynomial in rational input length, the numerical condition number
`kappa_2(Q)`, and `1/epsilon`, with exponent depending on `r`.

The proposed distinguishing step partitions parameter space by simple
saturation slabs. Coordinates outside their slabs are fixed at box endpoints.
Inside each cell, the remaining cost rows range over intervals controlled by
`Q`, even if the original entries of `c,D` are very large. A maximum-volume
row basis then gives a fixed-dimensional response net. Optimizing `b^T x`
exactly over each small cell avoids a grid resolution proportional to `||b||`.

Approximate response maps, sensitivity estimates, and basis normalization are
established. The candidate claim worth investigating is the combined global
bilevel guarantee with polynomial dependence on conditioning and no numerical
dependence on `c,D,b` beyond their encoding lengths. In particular, do not call
the algorithm strongly polynomial: its stated dependence includes numerical
conditioning and inverse accuracy. A fixed-dimensional polynomial bound is
also not automatically fixed-parameter tractability in `r`.

## Closest path approximation theorems

Giesen, Jaggi and Laue, *Approximating Parameterized Convex Optimization
Problems*, ESA 2010, later ACM Transactions on Algorithms 9(1), 2012,
[author manuscript](https://www.m8j.net/math/approxPaths.pdf), study
one-parameter convex optimization over a simplex. Definition 1 uses a relative
primal-dual gap, and Lemma 2 gives a parameter-change certificate. Their
specialized bounds include geometric quantities and parameter endpoints; for
example, Corollary 10 retains the kernel geometry and `c_min`. This is prior
for certified approximation of an entire response path, but the guarantee is
not the candidate's uniform response norm or arbitrary affine upper objective.

Giesen, Jaggi and Laue, *Regularization Paths with Guarantees for Convex
Semidefinite Optimization*, AISTATS 2012,
[primary full paper](https://proceedings.mlr.press/v22/giesen12/giesen12.pdf),
Theorem 6, gives at most
`ceil(2 L gamma (t_max-t_min)/((gamma-1) epsilon))` pieces when the objective
gradient is `L`-Lipschitz in the scalar parameter. The paper's error is a
duality-gap guarantee. Its explicit coefficient `L` matters: direct application
to a linearly parameterized objective retains the magnitude of its parameter
direction. This theorem does not supply the proposed saturation-based removal
of that numerical dependence.

Giesen, Laue, Mueller and Swiercy, *Approximating Concavely Parameterized
Optimization Problems*, NIPS 2012,
[primary full paper](https://papers.neurips.cc/paper_files/paper/2012/file/bdb106a0560c4e46ccc488ef010af787-Paper.pdf),
provides a stronger nearby result for scalar parameters. Lemma 4 and Theorem 5
bound the size of an additive follower-objective approximation path by

```
sqrt((b-a) (h'_-(a)-h'_-(b)) / epsilon),
```

where `h` is the optimal-value function. The class includes objectives affine
in the parameter, so it includes scalar versions of the candidate follower.
However, the slope variation in this bound can contain the magnitude of
`D`; the displayed `O(1/sqrt(epsilon))` shorthand is not a uniform bound over
all rational problem data. Strong convexity can convert follower-objective
error into response error, but does not by itself remove this slope factor.
The paper also develops an algorithm conditional on a suitable step-size
oracle. Do not claim the first polynomial-accuracy scalar path approximation.

Mairal and Yu, *Complexity Analysis of the Lasso Regularization Path*, ICML
2012, [primary full paper](https://arxiv.org/pdf/1205.0079), §4,
Proposition 3, gives an approximate path with a bound involving
`log(lambda_infinity/lambda_1)/sqrt(epsilon)`. Definition 1 measures relative
duality gap. The same paper establishes exponentially complicated exact
paths. These results already show that exact path complexity and useful
approximation complexity can differ sharply. They do not state the present
general affine-cost box-QP, fixed-multileader, global upper-objective theorem.

## Earlier response-norm approximation and basis normalization

Bemporad and Filippi, *Suboptimal Explicit MPC via Approximate Multiparametric
Quadratic Programming*, CDC 2001,
[author-hosted full paper](https://cse.lab.imtlucca.it/~bemporad/publications/papers/cdc01-sub-mpqp.pdf),
§4.6, Theorem 4, supplies an a priori uniform optimizer-error bound by choosing
the relaxation of dual feasibility using `Q^-1` and the active constraint
matrix. The paper approximates multiparametric QP solutions by relaxing KKT
conditions while retaining primal feasibility. Thus uniform response-norm
approximation has direct process-control precedent. The checked paper does
not establish the candidate's polynomial bound on total regions and bit
operations in terms of fixed parameter dimension and conditioning.

The maximum-volume basis argument is classical. Awerbuch and Kleinberg,
*Adaptive Routing with End-to-End feedback: Distributed Learning and Geometric
Approaches*, STOC 2004,
[author-hosted full paper](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf),
§2.3, Definition 2.1 and Proposition 2.2, prove that a determinant-maximizing
basis is a barycentric spanner: every point has expansion coefficients in
`[-1,1]`. Proposition 2.4 gives an approximate-spanner algorithm using a linear
optimization oracle. The candidate's finite row set and fixed rank permit
direct enumeration, but the determinant replacement proof should be credited
as this established normalization argument.

## Recent bilevel work and limits of this search

For the exact inner solver, the classical source is Kozlov, Tarasov and
Khachiyan, *Polynomial solvability of convex quadratic programming*, Doklady
248(5), 1049–1051 (1979), [primary bibliographic record](https://www.mathnet.ru/eng/dan43059).
The fuller English publication is *The polynomial solvability of convex
quadratic programming*, USSR Computational Mathematics and Mathematical
Physics 20(5), 223–228 (1980),
[publisher page](https://www.sciencedirect.com/science/article/pii/0041555380900981).
Its abstract explicitly states polynomial work in binary input length. The
1979 full-text link returned an access error, so this audit verifies the
attribution and primary abstract, not the original theorem's full wording.
The candidate's separate principal-linear-system argument establishes the
polynomial encoding of its unique rational response.

Chen, Ji and Zhang, *On the Condition Number Dependency in Bilevel
Optimization*, [arXiv version 4, August 2026](https://arxiv.org/abs/2511.22331v4),
studies oracle complexity of stationarity in nonconvex–strongly-convex bilevel
optimization. The abstract explicitly identifies stationarity as the target;
this is not a global approximation theorem for the present nonsmooth response
map. This comparison is based on its primary abstract, not a full theorem audit.

Sankaranarayanan and Vatsalya, *Proximity-based approximation algorithms for
integer bilevel programs*, [primary abstract](https://arxiv.org/abs/2412.15940),
also reports additive upper-objective bounds involving conditioning, but for
integer followers via proximity and flatness. That mechanism and domain differ
from continuous box followers. No claim about all its technical variants is
made here.

The bounded search found no theorem matching all the candidate restrictions
and coefficient-independent complexity guarantee. The saturation reduction
is the point on which a novelty claim should rest, together with the exact
handling of the leader's linear term. The existing approximation-path and MPC
results above must remain visible in any final presentation.
