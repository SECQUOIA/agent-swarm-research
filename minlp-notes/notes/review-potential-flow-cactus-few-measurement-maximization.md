# Independent audit: convex maximization through a fixed number of cactus flow measurements

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-few-measurement-maximization.md) gives the stated additive guarantee and rational resistance output in `N^{O(k)}` bit time, polynomial in requested accuracy bits, for fixed measurement dimension. No correction is required. The underlying zonotope method is classical; novelty is a separate question.

## Cactus geometry and scenario realization

The candidate uses the [reviewed cactus flow-region theorem](../results/potential-flow-cactus-flow-region-and-optimization.md) within its precise scope: fixed balanced rational nominations, independent positive interval or explicitly listed finite resistance sets, and no operating constraints filtering scenarios. Cycle blocks have fixed effective nominations and disjoint resistance coordinates. Their circulations vary independently, and both circulation extrema are realized by rational input resistance endpoints.

Consequently the interval flow region is the affine image of the circulation box, while the finite flow region has that same convex hull. Applying rational `R` preserves these statements. Bridge resistances may be assigned any allowed rational values because bridge flow is fixed. Combining separately selected cycle endpoint scenarios is therefore a feasible original resistance scenario, not merely a point in a relaxation.

## Rational sign cones despite algebraic lengths

After translating the box, the projected generators are positive multiples of the rational directions `a_C=RZ_C`. Multiplication by a positive circulation width changes no separating hyperplane. No common number field for these widths is needed to enumerate the directions.

The incremental sign-cone algorithm is correct. For a finite set of homogeneous strict inequalities, a feasible vector has a positive minimum slack, so positive rescaling makes every slack at least one. Conversely, the latter system implies all strict inequalities. Rational LP therefore tests each sign extension exactly and supplies a representative of polynomial bit length. At fixed ambient dimension the number of retained patterns at each insertion is polynomial. Repeated, opposite, or linearly dependent directions create infeasible sign combinations or subdivide existing cones within this bound.

Every projected vertex has a normal cone with nonempty interior in the ambient measurement space. This remains true when the zonotope has lower-dimensional affine span: its normal cone contains the orthogonal complement of that span together with a full-dimensional cone in the span. A generic point in its interior avoids every nonzero rational generator hyperplane. It uniquely chooses the required endpoint of each positive-length segment. Zero-length segments impose no restriction on the vertex, so retaining their hyperplanes only subdivides possible normal directions. The algorithm need not detect zero algebraic lengths at all. It only discards exactly zero rational direction vectors.

The point case is also covered. If no nonzero direction remains, one empty sign pattern and an arbitrary endpoint scenario suffice. Otherwise even zero-length generators produce only polynomially many patterns, all mapping to the same point when every segment is degenerate.

Convexity places a maximum at a projected vertex. For finite sets, every required vertex is attained by an original endpoint scenario, while every original measurement lies in the projected convex hull. This proves candidate-list completeness without enumerating all circulation-box corners.

## Additive comparison and encoding

The physical flow bound `|x_e|<=B=sum_v |b_v|` is valid and conservative. Thus every measurement lies in `[-T,T]^k` with the stated rational `T`. The rational baseline `Rx0` is summed exactly; only the individual circulation endpoints need approximation.

For a dense polynomial `g`, summing absolute derivative coefficients against powers of `T+1` gives a valid bound on each partial derivative throughout the enlarged box. It does not require convexity on that enlarged box: differentiability and the derivative bound suffice for evaluation error. Convexity is needed only on the promised box containing the actual zonotope.

If the degree is `d`, the derivative bound has bit length polynomial in the coefficient encoding and `d log(T+1)`. Under dense encoding with fixed `k`, this is polynomial in input length. The same applies to exact evaluation of `g` at rational approximate measurements. Sparse binary-exponent encoding would not provide this bound and is correctly excluded.

Each circulation error at most `delta` causes measurement error at most `M delta`. The choice

```
delta <= min(1/(1+M), epsilon/(8kL(1+M)))
```

keeps the approximate point and the segment joining it to the true point inside the enlarged box. The mean-value bound is at most `kLM delta<=epsilon/8`. Approximation of each separately encoded quadratic root requires polynomial work in its input size and `log(1/delta)`. The latter is polynomial in the total input and requested accuracy bits, even if the rational coefficients and circulation offsets have large numerical magnitudes.

Let `v*` be the value of a best enumerated candidate and `vhat` the true value of the selected one. Comparing the rational estimates gives `vhat>=v*-epsilon/4`. Since the list contains a global maximizer, this is stronger than the stated epsilon guarantee. There is no multiplication of the error by the number of candidates: each candidate is estimated independently to the same uniform tolerance.

The returned resistance vector is its precomputed exact rational endpoint scenario. Approximating circulation values is used only for comparison; it does not perturb the chosen physical law or require rational physical flows. This distinction avoids both an unnecessary feasibility-recovery step and exact comparison of independent radical sums.

The cases `B=0`, vanishing measurement directions, constant `g`, and rank-zero quadratic terms are handled directly as described. An epsilon larger than one poses no problem; the input encoding still governs arithmetic, and the minimum in the tolerance definition remains valid.

## Fixed-rank positive-semidefinite quadratic objective

A rational PSD matrix admits a rational pivoted LDL decomposition using only positive pivots until its rank is exhausted. A zero diagonal entry in a PSD residual has a zero row and column, so zero residual directions can be discarded. Rational elimination and its determinant bounds preserve polynomial bit length.

For fixed rank `r`, this represents the quadratic part as `r` nonnegative rational multiples of squares of rational linear forms. Adding `d^T x` as one additional measurement gives a convex quadratic polynomial in at most `r+1` variables. The constant term has no effect on the scenario choice. Thus the specialization is valid and requires no square roots in the measurement matrix. The result is for convex maximization; it makes no finite-set convex-minimization claim.

## Source and computational check

I directly read Onn and Rothblum, *Convex Combinatorial Optimization*, Lemmas 2.1--2.2 on printed page 4 and the surrounding projected-vertex discussion. These establish the classical fixed-dimensional zonotope enumeration mechanism and supporting generic normals. The present proof independently handles algebraic segment lengths through rational directions and additive evaluation. [Primary manuscript](https://arxiv.org/pdf/math/0309083).

I reran the provided [checker](../code/potential_flow_mpd/cactus_few_measurement_checks.py): all 18 projected convex quartic examples passed, comparing 286 sign cones against 1,512 exhaustive endpoint scenarios. Its LP cone tests use floating-point arithmetic, and its objective comparisons use high precision; those checks supplement the exact geometric and bit-complexity proof rather than certify the rational LP implementation.
