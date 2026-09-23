# Stage 4, round 1 — reviewer 06

I reviewed the entire `papers/pooling/sections/04-structural-algorithms.tex`, with additional attention to graph recognition, affine rank, dimension counts, elementary cases, and the scopes of the different algorithms. The manuscript and frozen snapshot both have SHA-256 `1ac2f2edead7ed519c97dec65e299412b7c10eb6709e1978ebdf2d2611c6bbe7`.

**Actionable findings: none.** I found no unsupported inference requiring a correction in this stage. The following records the main checks and their limits; it is not an assertion of exhaustive correctness.

## Fixed-core theorem and its basic pooling mappings

At `s4:fixed-core` (lines 19–257), I checked local vertex completeness in the ambient dimension, including singleton and lower-dimensional blocks. Explicit finite boxes ensure that nonempty blocks have vertices. The active-normal argument justifies enumerating square nonsingular subsystems even without full-dimensional feasible sets.

Candidate feasibility and support comparisons use the signs of both denominators. The retained sign conditions determine a maximizing candidate in each block without enumerating their Cartesian product; disconnected realizations do not affect this choice. The squared-denominator formula has the correct signs. Its degree grows with the number of blocks, but the number of variables remains fixed, so expanded monomial counts and coefficient lengths remain polynomial. The universal support formula correctly rejects an empty block, includes the zero support direction, and characterizes attainment of an exact aggregate-and-objective vector. Quantifier order is preserved.

Compactness supplies attainment. The joint optimality formula contains only a fixed number of variables even after its bound variables are renamed. Its algebraic sample puts the core and objective in one polynomial-degree field. The recovery LP then has coefficients in this field, rather than a collection of unrelated extensions. A bounded feasible recovery polyhedron has a vertex in the same field; determinant and field arithmetic bounds support polynomial encoding of all recovered blocks.

The added core-bound argument for aggregate slacks also works. For a nonempty compact coordinate projection, every finite endpoint must be a root of a nonzero polynomial in its eliminated univariate formula. Otherwise all signs would be constant in a neighborhood, contradicting the endpoint property. A Cauchy bound therefore supplies a polynomial-bit rational box. The treatment of an empty core and `r=0` avoids applying this endpoint argument where it is inapplicable. Interval arithmetic with the local boxes supplies bounded scalar slacks without increasing any fixed dimension beyond a constant. The zero-block padding covers no blocks and application blocks with no coordinates.

At `s4:fixed-inputs` and `s4:fixed-qualities` (lines 284–368), I checked both physical mapping directions, lower and upper product specifications, distribution of inlet costs, missing arcs, and inactive pools. The first construction has at most `mp` core fractions, local dimension `p+m`, and at most `2(p+mp+m)` aggregate inequalities. The second has `pK` core qualities, local dimension at most `p`, and `p(K+1)` balance equations plus pool intervals. A fixed number of bypass flows can be moved into its core with all their withdrawal, delivery, mass, and cost contributions retained. The general theorem's padding handles `p=0`; empty inputs are separately checked before taking input-quality extrema.

The discrete-block subset-sum example and independent-radical output obstruction at `s4:core-limits` distinguish limitations of the theorem from approximation hardness. The multiquadratic orbit argument supports the stated degree `2^N`.

## Structural decomposition, rank, and all specializations

At `s4:vertex-integrity` (lines 406–559), the graph hypothesis can be recognized by the proposed fixed-size enumeration. A fixed pair `(c,h)` implies integrity at most `c+h`; conversely a fixed integrity bound supplies fixed deletion and component-size bounds. Recognition failure is correctly separated from infeasibility. The algorithm needs only this definition, not an unproved graph algorithm or a supplied deletion certificate.

Arc ownership is exhaustive and exclusive. A bypass either has both endpoints deleted, exactly one deleted endpoint, or both endpoints in a single remaining component. Thus every undeleted input or product has all its incident flows in its component block. For a component containing `i` inputs and `j` products, its coordinate count is at most

`p(i+j) + c_I j + c_J i + ij`.

This is bounded by `ph+ch+h^2`, and for `h=1` by `p+c`. The exact core count before loose upper bounds is at most

`pt + p(c_I+c_J) + c_I c_J + c_J(t+1)`.

It is bounded by the manuscript's `pt+pc+c^2+c_J(t+1)`. After adding scalar slacks, the aggregate count is at most `p(t+1)+c_J(t+1)+2p+2c_I`. No attribute-dependent aggregate rows remain hidden in this count.

The affine-coordinate balance identity follows from mass balance and independence of the columns of the rational basis matrix. Coordinate extrema bound every active average. Inactive pools may use an arbitrary boxed coordinate vector because their nonnegative incident flows vanish. No product-specification rank assumption is used.

In particular, the deleted-product totals at `s4:covered-totals` are necessary and correctly formed. They identify total delivery and all `t` coordinate masses. The original mass vector is consequently `lambda_0*tau_j+B*M_j`, which verifies both signs in `s4:covered-quality`. Arbitrarily many original specification rows now belong to the core. The bounds `|M_js| <= A_s H_j` remain valid for signed affine coordinates. Their rational encoding is polynomial. Both mapping directions preserve every arc bound, external contract, pool bound, and original arc cost.

I checked every item of `s4:structural-corollaries` (lines 561–589): fixed attribute count bounds affine rank; a vertex cover leaves singleton components; bounded components include an unbounded matching; no bypasses give singleton components; a fixed number of distinct profiles bounds affine rank; and a fixed input set is a bypass vertex cover with rank at most its cardinality minus one. The last rank inequality is used only after the empty-input case has been separated. No-pool instances are blending LPs regardless of graph structure. Rank-zero instances with inputs have one common quality vector, so mixing disappears after conservation even when the pool count grows.

The distinction from degree and treewidth at lines 591–598 is sound. A path has maximum degree two and treewidth one, but deleting `c` vertices leaves at most `c+1` path components. If each has at most `h` vertices, its original size is at most `c+(c+1)h`. Thus neither degree nor treewidth bounds vertex integrity for arbitrarily long paths. Conversely, fixed integrity permits arbitrarily large stars through a fixed deleted hub and does not impose bounded degree. The manuscript does not claim fixed-parameter tractability with a uniform exponent.

## Planar paths, retained objectives, and feasibility boundary

At `s4:polygon-composition` and `s4:path-projection` (lines 609–773), I checked the clamped-envelope identity, convexity of the two compositions, and the piece-count argument. Inner convex or concave level sets have at most two boundary points, including a flat extremal interval. Each outer knot therefore adds only a constant number of subdivision points. Taking the maximum of convex piecewise-affine functions uses no more than the sum of their supporting lines. The resulting linear row bound fits the stated loose constant.

The separate Fourier–Motzkin construction provides a finite polynomial candidate system whose coefficients use only a constant number of operations on child rows. Redundancy removal preserves this bound; segment and point descriptions also use only a constant number of row-intersection operations per coefficient. Balanced composition turns both row and coefficient recurrences into polynomial bounds. Lifting chooses a midpoint in the intersection of two nonempty closed bounded slices. Its divisions are by rational row coefficients, so it introduces no field extension and has polynomial affine-coefficient growth along the balanced tree.

At `s4:bounded-attachments` (lines 791–895), the count `4a` includes at most `a` pool flows, `2a` distinct incident bypasses, and `a` fractions. Shared attachments and bypasses between attachments are not double-counted. Removing unusable pools retains external-node requirements. After removing attachment vertices, a boundary-connected component cannot be a cycle and has at most two retained boundary arcs. Local rows involve only neighboring scalar flows with constant rational quality coefficients. The one-boundary dummy construction, detached LP components, isolated vertices, and a path returning to the same attachment all preserve the original constraints. The specialized thirteen-coordinate count is valid with two feeds and two outlets.

At `s4:fixed-support` and `s4:equality-support` (lines 902–980), cutting at designated actual flows preserves node relations and bounds the retained dimension by `4a+s`. A cycle cut once correctly yields `R(x,x)`. Closed additional constraints preserve compactness and attainment. The supplied equality identity preserves objective values throughout the feasible set; merely hypothesized active inequalities would not suffice. The revenue example counts price changes, rather than distinct prices.

At `s4:degree-boundary` (lines 987–1026), the positive total-degree restrictions imply the required bypass-degree restriction. For the negative branch I checked accepted stage 3 through `s3:physical-threshold` and the point immediately before `s3:completion`. The threshold is already implemented by physical linear circuits; it survives removal of the later economics. Restoring the exact source and collector contracts retains the fixed flow alphabet and degree restrictions. The source coefficients occur in circuit topology, supporting strong hardness of the contracted feasibility problem. Accepted `s2:pooling-np` applies to one pool and one scalar quality. Zero-lower-bound feasibility and unrestricted dense-cost optimization remain explicitly distinct.

These scopes do not conflict: fixed integrity supports unrestricted arc costs, while bounded attachments with degree-two bypasses allows unbounded paths and arbitrary quality rank but retains only feasibility information and fixed-support objectives. Fixed pool count alone does not bound the attachment interface, and polynomial endpoint feasibility does not preserve a dense accumulated cost.

## Sources, coverage, and verification limits

I read all three canonical arguments named in the round instructions and compared the relevant vertex-cover, affine-rank, path-projection, and bounded-attachment precursor notes. I also consulted the indicated historical proof, mapping, and source audits as context, without treating their PASS labels or finite checks as proof. The scope promised by the stage-4 coverage entries is present in the manuscript.

I checked the relevant local primary texts for Basu–Pollack–Roy's Theorem 1.3.1 and Sections 3.1.3–3.2, Adler–Beling's common-extension dependence and Section 5 Remark 1, the cited fixed-source pooling algorithms, Haugland's final open-question wording, Baltean-Lugojan–Misener's Assumption 2.2, fixed-dimensional Minkowski addition, block LP linking rows, and TVPI resultant projection. I additionally extracted the original PDF pages for Basu–Pollack–Roy's quantifier-elimination bound, Adler–Beling's rational computation remark, and Haugland's printed page 214. These support the distinctions used in this stage. In particular, the final Haugland question concerns a bounded pool count together with a bound on inputs, products, or qualities; the stage identifies which positive branches it addresses and the separate accepted stage-3 negative branch.

This was a mathematical and encoding review. I did not implement the quantifier-elimination or algebraic LP algorithms, rerun numerical experiments without a new concern, compile the manuscript, or independently repeat the entire accepted stage-3 gadget review. I did not conduct an exhaustive search for later or differently named prior results. Those limits do not amount to findings against the scoped source comparisons here. No manuscript file was edited, no other current-round report was inspected, and no subagent was spawned.

**Final verdict: no findings.**
