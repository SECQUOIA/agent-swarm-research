# Bounded source assessment: coupled separable convex output precision

Date: 2026-09-05. Scope: [the multivariate separable candidate](convex-separable-vector-curvature-rank-precision.md). No exhaustive priority claim is made.

The source distinctions from the [single-input curvature-rank assessment](convex-vector-curvature-rank-novelty.md) apply unchanged. Awerbuch and Kleinberg's barycentric spanners supply the bounded-coordinate basis primitive; parity-based integer obstructions come from mixed-integer convex representability; scalar segmentation and the circuit compiler have their own source records. Those ingredients are credited rather than presented as new.

The additional construction is classical separable interpolation in its upper representation: one grid per input coordinate, and sums of the corresponding univariate interpolants. No novelty is claimed for separable programming or for using shared coordinate values in several outputs. The proposed comparison argument is different: one output basis spans all coordinate curvature blocks, and a rank-scaled product packing bounds the integer count against the minimum for the original coupled vector graph.

Focused searches combined separable vector approximation, simultaneous convex piecewise-linear approximation, and barycentric spanners with mixed-integer graph precision. They returned adjacent separable-programming and PWL approximation literature, but no checked source stating the uniform bounds against all convex integer lifts with an additive term `O(n log r+n)` independent of output count and polynomial degree. This absence is limited evidence.

The precise claimed contribution is the joint guarantee: arbitrary signed dense convex summands, shared nonlinear dependence across outputs, rational construction polynomial in input and precision encoding, and comparison with the unrestricted convex-lift integer minimum. The unconditional-facet version controls a coupled error budget and yields output-independent linear-in-input-dimension overhead for weighted l1 error.

The result is not a new general multivariate approximation method. Its proof excludes mixed multivariate polynomial terms and does not prove that the rank overhead is necessary. A future literature review should look for integer-dimension guarantees, not count any existing separable interpolation construction as either a complete match or a new ingredient.
