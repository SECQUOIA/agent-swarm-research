# Independent review: pooling with controlled bypass structure

Date: 2026-09-05. Reviewer: `benders_property`, independent of the mapping's author. Reviewed [the fixed-quality mapping](pooling-bypass-vertex-cover-algorithm.md), the fixed-core theorem it invokes, and the integrated draft at `/tmp/pooling-bypass-structure-algorithm.md` before promotion. The affine-rank portion has a [separate review](review-pooling-quality-rank-extension.md).

**Verdict: pass.** The stated exact polynomial bit-time corollary follows from the reviewed fixed-core theorem for fixed pool count, quality count, and bypass vertex integrity. No substantive error was found. This is a mathematical reduction review, not an independent literature-priority claim or practical implementation assessment.

## Coverage of variables and constraints

Let deleted inputs and outputs be `A,B`; every remaining vertex belongs to exactly one component. A bypass has both endpoints deleted, exactly one deleted endpoint, or both endpoints in one remaining component. The last case cannot cross components by definition. Thus the core and component blocks partition all arc variables exactly once. This uses the standard model's single flow variable for each permitted input-output pair, as the draft explicitly specifies.

For a remaining input, all pool arcs and all bypasses incident to it are in its component block. Its throughput bounds are therefore local. The same argument places every remaining output's throughput and quality constraints in its block, including bypass inflow from deleted inputs. Fixing pool qualities makes these constraints linear in local flows.

The remaining constraints are exactly pool mass, pool quality, pool throughput, deleted-input throughput, and deleted-output throughput/quality. The displayed aggregate equations have the correct signs: transferring the deleted flows to the right side reconstructs the original balance equations. In a deleted-output upper quality constraint, both the core pool-outflow term and the deleted-input bypass term change sign on transfer; the draft does so. The lower quality form reverses the quality differences and otherwise keeps the same placement. Both senses are preserved.

Every individual arc bound follows its unique variable owner. Every cost coefficient follows its arc too. Thus no arc bounds, throughput lower bounds, output specifications, or cost terms are omitted.

## Dimension, degree, and compactness

The core has at most `pK + p(cI+cJ) + cI*cJ` coordinates. A component with at most `h` vertices has at most `ph` pool arcs, `ch` bypasses to deleted vertices, and `h^2` internal bypasses. These bounds are deliberately loose but valid. Singleton components sharpen the block dimension to `p+c`.

The aggregate count `p(1+K)+2p+2cI+2cJ(1+K)` counts all remaining equations and both sides of each throughput or quality interval. Adding one bounded scalar slack per inequality preserves this row count and increases maximum block dimension only to at least one. Coefficients are affine in core qualities, and right-hand sides contain at most quality-times-flow products, so degree two suffices.

Finite flow boxes and coordinatewise input-quality bounds make the core and local variables bounded. Interval arithmetic gives polynomial-bit slack bounds even with an unbounded number of components. Empty local polytopes are permitted by the fixed-core theorem. At zero pool throughput, nonnegative mass balance forces every incident pool flow to zero, so arbitrary boxed pool quality cannot leak artificial quality mass. A pool without incoming arcs therefore causes no exception. The no-input case has zero flow everywhere and can be checked directly.

## Algorithmic and scope checks

For fixed deletion bound `c`, enumerating all subsets of size at most `c` and inspecting the remaining connected components is polynomial. The equivalence with a fixed vertex-integrity bound is correct, including the convention that the largest remaining component has size zero if none remains. Failure to find a suitable set is correctly separated from optimization infeasibility.

All dimensions and polynomial degrees required by the fixed-core theorem are bounded by the fixed parameters. The number of local rows and blocks may grow, which that theorem explicitly allows. Exact algebraic optimizer recovery is inherited from that theorem; the mapping neither introduces discrete leaves nor an additional arithmetic representation assumption.

The integrated draft retains these properties after its quality-rank extension. Its elementary no-pool case is a blending LP. Its rank-zero case fixes every positive-flow pool to the common source quality, leaving a linear model even with unrestricted bypasses or pool count. Inactive pools do not invalidate either observation.

The review is based on exact algebraic identities and a complete constraint audit. No implementation of the global real-algebraic algorithm was tested or implied.
