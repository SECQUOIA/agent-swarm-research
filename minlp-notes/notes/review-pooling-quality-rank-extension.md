# Independent review: affine input-quality rank

Date: 2026-09-05. Reviewer: `benders_property`, independent of the extension's author. Reviewed [the quality-rank note](pooling-quality-rank-extension.md) and the integrated draft at `/tmp/pooling-bypass-structure-algorithm.md`, together with the [bypass mapping review](review-pooling-bypass-vertex-cover.md).

**Verdict: pass.** Fixed affine rank of the rational source-quality data can replace fixed attribute count in the structural pooling theorem. The covered-output throughput and coordinate-mass variables are essential to the stated aggregate-dimension argument and are included correctly. No condition on the rank of the output specification vectors is needed.

## Exactness of quality compression

The reference `C_0` is an actual source vector. Thus the span of `C_i-C_0` has dimension equal to the affine dimension of the source profiles. A rational independent basis gives unique coordinates `a_i`, with polynomial encoding length by rational linear algebra. This is exact rank, not an approximate factorization.

Write `B` for the matrix with these independent basis columns, so `C_i=C_0+B a_i` and represented pool quality is `Q=C_0+B q`. The original pool quality residual satisfies the identity

```
sum_i C_i y_i - Q sum_j v_j
 = C_0 (sum_i y_i - sum_j v_j)
   + B (sum_i a_i y_i - q sum_j v_j).
```

Mass balance eliminates the first term. Independence of the columns of `B` makes zero original quality residual equivalent to zero coordinate residual. Positive throughput forces `q` to be the actual average of input coordinates; hence its coordinatewise source bounds are valid. Zero throughput forces all incident flows to zero and permits an arbitrary boxed coordinate vector. Requiring even an inactive pool's quality to lie in this affine representation therefore does not exclude any feasible flow or change a cost value.

For every nondeleted output, substituting `C_0+Bq` in each original attribute inequality leaves a local inequality with coefficients affine in the core. All attributes are retained, so compression does not weaken output specifications. Unbounded attribute count increases the number of rows, not local dimension.

## Deleted outputs and parameter counts

For each deleted output, the defining equations make `T_j` its total incoming flow and `M_j` the sum of incoming flow times the appropriate coordinate vector. Consequently its total original quality mass is exactly `C_0*T_j+B*M_j`. The upper inequality becomes `(C_0a-U_ja)T_j+sum_s b_sa M_js<=0`; the lower inequality has the opposite coordinate sign. This verifies both displayed formulas, including the affine offset. Arbitrary output specification rows can now reside in the core domain without adding aggregate dimensions.

Only `cJ(t+1)` aggregate definitions are needed for these totals. Adding pool balances and throughput intervals and deleted-input intervals yields exactly the upper bound

```
k <= p(t+1) + cJ(t+1) + 2p + 2cI.
```

Core dimension is at most `pt+pc+c^2+cJ(t+1)`; maximum block dimension remains `max(1,ph+ch+h^2)`. The defining equations for coordinate masses contain only core bilinear terms and linear block terms. Degree two still suffices. The number of core inequalities may grow with the number of attributes, as allowed by the fixed-core theorem.

The bound `|M_js|<=A_s H_j` is valid even when input coordinates are negative: every incoming coordinate lies in `[-A_s,A_s]`, all flows are nonnegative, and their total is at most `H_j`. Both these mass bounds and throughput bounds have polynomial bit length. No convex-hull description of the source-coordinate vectors is needed; pool balances already impose the correct average whenever there is flow.

The added totals are determined by the flows and pool coordinates, introduce no new attainable objective values, and preserve the common algebraic field used for optimizer recovery. Expanding back to all original attributes is rational linear arithmetic and remains polynomial in output size.

## Integration and edge cases

The integrated draft combines the two mappings without changing their constraints or parameter dependencies. It treats absent inputs before defining affine rank. With no pools, the original model is an LP. With rank zero and nonempty sources, all source qualities coincide and every positive-throughput pool shares that vector, so fixing all pool qualities to it yields an equivalent LP. Both claims hold without a bypass-structure bound.

The optional statement about a fixed number of design binaries is correctly conditional on preserving the core/block form; it does not admit unbounded discrete local choices. Novelty of this pooling corollary remains a separate literature question, and ordinary affine coordinate compression itself should not be claimed as novel.
