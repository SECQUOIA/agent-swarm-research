# Stage 4, round 1 — reviewer 10

Reviewed the entire `papers/pooling/sections/04-structural-algorithms.tex` (lines 1–1042), independently of the other reports in this round. The manuscript and frozen snapshot both have SHA-256 `1ac2f2edead7ed519c97dec65e299412b7c10eb6709e1978ebdf2d2611c6bbe7`.

**Findings: none.** I found no major or minor defect requiring correction. The following records the substantive checks underlying that conclusion; it is not an exhaustive correctness guarantee.

## Fixed-core theorem and pooling mappings

At lines 66–155, the active-normal argument supplies complete candidate vertex lists even for singleton and lower-dimensional blocks. Determinant signs together with residual and cross-product signs correctly decide candidate validity and score order. A realizable sign condition fixes the tie-broken maximizing tuple without requiring connectedness. Counting realizable conditions in the fixed joint core/support space avoids the exponential product of basis choices. I checked the cleared identity

`F_sigma/H_sigma = u^T w - sum_j n_j/delta_j`.

The squared product is positive precisely on the retained condition. Singular candidates cannot enter through cleared-denominator boundary points because the sign conjunction remains in the formula. The degree grows with the number of blocks, but the fixed number of variables gives polynomial dense expansion size and coefficient length.

At lines 157–230, universal support membership is equivalent to attaining the specified aggregate and objective vector in the compact convex Minkowski sum. Empty blocks make the formula false, including at support direction zero. The quantifier order is correct. The optimality formula duplicates only a fixed number of variables. Compactness follows from the compact core and closed constraints inside the global block boxes, even if the syntactic description of the compact core uses strict atoms. The common univariate sample places all core/value coordinates in one polynomial-degree field. Recovery is a bounded LP over that field; it does not combine independently generated fields. Coordinate boxes supply full column rank, and a recovered vertex uses field linear algebra without adjoining roots.

The computed-core-box extension at lines 232–249 is justified: a nonempty compact coordinate projection has boundary endpoints, and each endpoint must meet a nonzero polynomial root in its quantifier-free univariate description. Fixed-dimensional elimination and Cauchy bounds give polynomial-bit rational bounds. Interval arithmetic then bounds the fixed number of aggregate slacks. The discrete-leaf and square-root-sum exclusions at lines 261–278 have the stated scopes.

I checked both directions of the fixed-input and fixed-quality mappings at lines 282–368, including inlet costs, lower quality rows, missing arcs, zero throughput, and preservation of adjacent external-node contracts during pool removal. Unlimited qualities increase row counts without increasing the relevant fixed dimensions. Bounded bypass flows can be moved into the concentration core as stated.

For lines 417–589, the affine-rank equations are equivalent to all physical balances by mass conservation and column independence. Arc ownership is exhaustive and unique, including edges crossing the deletion set. The covered-product total and coordinate-mass variables correctly move an unbounded number of specification rows into the core. Their bounds remain valid for signed coordinate qualities. I checked the aggregate signs, counts, costs, compactness, recognition procedure, and the rank-zero/no-pool special cases. None requires a rank bound on product specification vectors.

## Planar projection, attachment construction, and recovery

At lines 609–714, clipping by the shared-coordinate projection makes every remaining slice usable. The lower-envelope identity follows from the three positions of the feasible interval relative to the minimizing plateau. The two compositions are convex, and the level-preimage count bounds their affine pieces linearly in the two children’s row counts. Taking a maximum adds supporting-line lists. Reflection gives the upper envelope. Empty, vertical, singleton, and coincident-envelope cases are covered.

One-variable Fourier–Motzkin elimination gives the exact rational projection; its coefficient arithmetic has bounded depth. Removing redundant rows, or describing a degenerate segment from its extreme points, preserves the universal coefficient-bit bound. At lines 731–770, balanced composition converts the constant-factor size and bit recurrences into polynomial bounds. Lifting intersects nonempty compact intervals. Each selected midpoint is a rational affine expression in the two parent endpoints, so the balanced lift stays in the supplied common field with polynomial total encoding.

At lines 800–900, I checked the `4a` and thirteen-coordinate bounds, multiple pools, shared attachments, unusable pools, and arbitrary attribute count. Every nonattachment node has rational rows in at most two bypass flows. Deleting attachments leaves at most two retained boundary arcs per incident component. A cycle meeting one attachment has two distinct retained arc coordinates, even though both touch the same attachment. Independently feasible detached components can be combined because every coupling row remains at an attachment or a pool in the core. This proves exact projection and physical recovery, rather than a relaxation.

## Assigned emphasis: objectives and excluded aggregate scopes

At lines 906–943, retaining a designated arc cuts the chain at a coordinate, preserving both adjacent node relations. For a detached cycle with one retained arc, the exact condition is `R(x,x)`; both endpoint occurrences must be identified with that same scalar variable. Multiple cuts give ordinary segments. Added polynomial rows may couple the retained coordinates arbitrarily because their total number is fixed. Closed added constraints preserve compactness, and continuous fixed-degree objectives attain their optima. Sampling and lifting preserve every objective coordinate. Excluding strict additional constraints from the attainment statement is appropriate.

At lines 945–965, the supplied rational identity `c = E^T gamma + d` yields `c^T f = gamma^T e + d^T f` on every feasible flow. Its assumed polynomial encoding makes verification and constant-shift calculation polynomial. The requirement that `Ef=e` hold throughout the feasible set is essential and stated. This is not an assertion that arbitrary dense costs admit such a reduction.

At lines 967–980, the price-change example is an exact identity for source rows with two bypass arcs summing to the prescribed supply. Production costs for these sources are constant, and the remaining revenue coefficients are consecutive differences. The conclusion counts the total number of changes, not distinct revenue values. Attachment contributions are already retained. This example concerns the displayed economic objective, not arbitrary routing costs.

At lines 1030–1042, the exclusions are material and correct. Two endpoint values do not encode a dense interior aggregate or unrestricted interior cost. A fixed pool count also does not bound the number of attachment coordinates. No algorithm for either broader scope follows from this projection argument.

## Degree boundary and sources

For lines 985–1028, I checked the positive branch’s bypass-degree implication and the negative branch against accepted stage 3, especially lines 1051–1163. Before contract completion, the physical circuit already enforces the source threshold and both directions of source feasibility. Removing economics while preserving contracts therefore preserves hardness. The two actual feeds/outlets, input degree two, product degree three, finite numerical alphabets, and polynomial topology encoding survive. Stage 2’s fixed pool-quality linear-fiber certificate applies with one scalar parameter and permits positive contracts, giving the required NP upper bound.

I read all three required canonical result files, the distinct vertex-cover and affine-rank precursors, the attachment investigation and its limitations, and relevant historical fixed-core, path-projection, and attachment audits. Historical PASS labels and finite experiments were not used as proof. I checked the stage-1 model/encoding dependencies and the stage-2 certificate proof used here.

After reading `literature/AGENTS.md`, I consulted local primary-source texts for Basu–Pollack–Roy (Theorem 1.3.1, bit-size convention, sampling/sign enumeration), Adler–Beling (Section 5, Remark 1), the cited Haugland and Boland results, Baltean-Lugojan–Misener Assumption 2.2, and the block-LP/TVPI antecedents. I also extracted the relevant pages directly from the original BPR, Adler–Beling, and final Haugland PDFs. Their stated scopes support the manuscript’s comparisons. In particular, the general algebraic LP implementation is a cited algorithmic ingredient, and the manuscript does not present it as a new proof. The final Haugland question has the stated fixed-pool parameter branches; its earlier fixed-source/terminal hardness allows the pool count to grow.

## Verdict and verification limits

**Verdict: no findings.** No manuscript correction is requested by this report.

This was a proof, mapping, encoding, and bounded primary-source audit. I did not implement quantifier elimination, algebraic LP recovery, or the full path algorithm, and I did not rerun previously passing finite experiments without a new concern. Root handles compilation. I did not re-prove every accepted stage-3 source gadget or conduct an exhaustive search for prior formulations of the structural theorems. The stated literature comparisons were checked; universal priority and external-review acceptance are outside this verdict.
