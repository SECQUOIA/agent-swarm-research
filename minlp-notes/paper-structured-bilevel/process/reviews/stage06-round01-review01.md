# Independent review 01: stage 6, round 1

Recommendation: accept. I found no actionable major or minor issue in this stage. The full original-coordinate baseline has the claimed completeness under its checked restriction, and the compressed solver preserves original contacts and distinguishes pessimistic nonattainment correctly. The measurements and their limitations are consistent with the supplied records.

## Scope and source integrity

I reviewed the frozen `process/snapshots/stage06-round01`, verified all 30 manifest entries, and verified manifest SHA-256 `b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`.

I read all of Section 6 and every new Python file, checked the integration, bibliography, README and coverage, and inspected the data through complete parsing, regeneration and comparison. Dependencies inspected include the original scalar solver, full convex quadratic solver, screening/MILP implementation, screening and recovery routines, relevant generators, canonical scalar algorithm and computation material, and historical timing data. The author's report and logs were evidence to examine, not proof authority. I did not read other current reports or root conclusions, delegate, or edit manuscript or official measurement files.

My isolated copy is `verification/stage06-review01/repo/paper-structured-bilevel`, with a repository-code dependency link to the actual checked source. Outputs and audit records are under `verification/stage06-review01`.

## Mathematical and implementation assessment

### Convex certification and aligned sweep

The active-status construction in `subsec:convex-implementation` and `prop:convex-certified-path` is correct. Positive definiteness gives invertible free principal systems. The implementation constructs rational affine responses, verifies their box/KKT conditions on closed intervals, and checks exact coverage. Endpoint tests suffice for affine inequalities, including singleton price domains and degenerate zero gradients. Substituting the upper objective and rows reduces the full upper task to rational quadratic optimization on closed intervals.

The small-system solve uses `I+SH`, with no inverse of `H`; the determinant argument remains valid for singular or indefinite `H` when the supplied total Hessian is positive definite. The operation count has the stated dependence on population and rank and correctly excludes validation of the positive-definiteness assumption. I inspected the exact validation and dense fallback in `quadratic_solver.py`.

The generic numerical routine only proposes statuses. Its exact reconstruction, queried-price membership, segment verification and final coverage checks prevent an unsuccessful numerical proposal from becoming a certified path. Recovery and segment-cap failures are expressly allowed. The manuscript does not turn this proposal procedure into a guaranteed polynomial algorithm.

For the complete aligned sweep, the effective-price map is strictly increasing even for negative rank-one coefficients when the full Hessian is positive definite. Signed loadings, zero loadings, grouped breakpoints and tails are handled consistently in the formulas and code. Maintaining the objective and upper-row weighted sums supports the stated arithmetic count without storing an original-coordinate vector for every interval. The timing description correctly identifies a fused sweep and upper solve.

### Scalar compression, contacts and bit complexity

The fiber reduction in `lem:scalar-fiber-pieces` is exact because the local separable cost is strictly convex on every nonempty aggregate fiber. Signed loadings do not destroy monotonicity of the multiplier-to-aggregate map: its slope is the sum of squared loadings divided by positive local curvature. Flat multiplier intervals and tails give singleton aggregates, while nondegenerate intervals give the stated affine allocations and rational quadratics. The bound of at most `2N-1` nondegenerate pieces and the singleton-aggregate case are correct.

For `thm:nonconvex-atlas`, endpoints, convex-piece stationary points and linear-piece flat intervals exhaust the possible global minima. Comparing their original tilted values is sufficient and necessary. Candidate-domain endpoints, quadratic crossings and flat prices form a polynomial-size partition with polynomial coefficient lengths. Rational sampling between distinct quadratic cuts needs polynomial bit length. Identical winning value polynomials on an open price cell have identical aggregate derivatives; unique fiber allocation therefore gives a single original response there.

The incremental insertion code agrees with the contact-preservation argument. It retains crossings with the current envelope, domain endpoints and isolated contacts even when cells with the same winner merge. Final reconstruction compares all original candidates at retained cuts and explicitly adds globally optimal flat intervals. A final distinct-response tie could not have lain strictly above an earlier envelope when its later branch was inserted. Identical polynomials do not create an unrecorded distinct response on an open common domain. The conservative polynomial cut and processing bounds are consistent with this implementation.

The upper solver correctly clips open response cells by closed upper rows, retains feasible singleton intersections inside them, considers revenue stationary points and endpoint limits, and includes an interior sample for constant revenue. Endpoint attainment is determined relative to the original open cell. At a cut, optimism optimizes over each feasible original component; pessimism checks every endpoint of every component for every row and uses the least revenue. The code prefers an attained candidate when its value equals a previously recorded limit. These rules give the asserted feasibility, supremum and attainment conclusions.

The output-field claim is properly local to each selected optimizer or limiting pair. Open-cell stationary prices and row boundaries are rational; flat prices are rational; the remaining outputs are rational functions of one quadratic price. Comparing cuts from different quadratic fields does not require constructing a common field for the entire atlas. I found no hidden growing-dimensional elimination or output-degree assumption in the polynomial bit-complexity argument.

The conjugacy proof and original-contact equality are valid. The convex envelope preserves the tilted optimal value but may introduce false choices. Both worked jump examples and their attainment assertions check algebraically. The figure accurately depicts the first example. The strictly local, nonglobal KKT example is also correct.

### Complete original-coordinate baseline

I audited `prop:original-face-baseline` against all of `original_faces.py`. The restriction is that every nonempty principal minor is nonzero; the program checks all of them before enumeration and rejects singular cases. The positive-definiteness tests on each free submatrix use the appropriate leading principal minors of that submatrix.

At any global minimizer, its minimal box face has a positive-semidefinite free Hessian by the second-order necessary condition. The nonzero determinant makes it positive definite, so its unique stationary point is among the enumerated affine candidates. Fixed coordinates need no gradient sign; the code handles this explicitly. The original bounds and bound-gradient inequalities supply exact validity intervals. The dense quadratic substitution in the code gives the original objective coefficients, independently of fiber allocation or compressed values.

The baseline compares all value crossings on overlapping validity intervals, including crossings above the lower envelope, and separately reconstructs all endpoint winners. Thus it retains every global response and every tie. Under the restriction, there cannot be a missing continuum of minimizers: each minimal face contributes at most one stationary point at a fixed price. The independent upper code has the same mathematical task but uses separate implementation of interval clipping, revenue candidates, universal row tests and endpoint flags. I found no import or call to compressed allocation, envelope or upper-optimization code in the baseline.

The complexity is exponential in population, as stated: all minors, at most `3^N` statuses and pairwise comparisons among retained faces. The older singular-face argument preserves a fixed-price global value by moving along a flat null direction to a smaller face. The manuscript correctly explains why this does not recover all flat minimizers or solve the continuous leader task. The new baseline's stronger restriction is not silently applied to the compressed solver.

### Screening and scientific interpretation

The stated binary formulation has the correct lower/upper activity implications and includes zero-gradient bounds. Its explicit big-M bound is valid over the full leader and follower boxes. Positive definiteness makes the real-arithmetic KKT reformulation exact. The implementation's numerical MILP result is separately identified as numerical, including its reported gap, feasibility violation and tighter-tolerance follow-up.

The exact screening path uses whole-cell certificates and rational original KKT recovery. Dense inversion, certification, recovery and final verification are included in the appropriate reported costs; `M 3^t` is not represented as total runtime. The negative screening timing conclusion is supported for all reported archived and fresh cases. The manuscript does not infer a global guarantee merely from verification of one returned point.

The repeated-type scaling identity is correct and explains the constant fiber-piece count in the large repeated-type experiment. The heterogeneous, repeated-type and convex-sweep families are explicitly separated. The original pairwise compressed comparator, fixed-price oracle and new original-coordinate full-task comparator are not conflated. The small full-task results have mixed timing winners, which the prose reports accurately.

## Data, provenance and verification

All 60 final records have zero worker exit status. I checked the 20 method/instance groups, each with repetitions 0, 1 and 2, the repeated exact values and attainment flags, all reported table medians, screening statuses/certificates and numerical discrepancies. Regenerating all three LaTeX tables in the isolated copy reproduces the frozen files byte for byte. Regenerating the full convex/screening prepared-input archive also reproduces it byte for byte, and the scalar generator reproduces every archived scalar instance. Results are in `data-audit.json`, `table-regeneration.log` and `input-regeneration.log`.

The two measured wrapper hashes differ from the final wrappers exactly as documented. I checked the archived measured originals against their recorded hashes and inspected their diffs: directory creation, untimed prepared-input archival and hash-list additions do not change the timed worker algorithms. The solver and dependency hashes match the measurement record. The compressed solver differs from its historical source only in the two declared rational fast paths and associated documentation. I also checked the profile totals and quoted historical timings against their actual files. Metadata evidence is in `metadata-audit.json`.

The isolated full-task checker passed all 18 supplied adversarial/seeded cases, both upper semantics, response-set comparisons on the independent face partition, attained-witness checks and the singular/flat exceptions. Its output is retained in `full-task-check.log`.

I additionally tested a distinct flat-response capacity case: `d=(1,1)`, `c=(-1,-1/2)`, `u=(1,1)`, `h=1/2`, `gamma=1`, unit boxes and prices `[0,1]`, with `w<=1`. At price `3/4` the whole fiber interval `[1/2,3/2]` is globally optimal. The optimistic result is value `3/4`, attained at aggregate one and response `(3/4,1/4)`; the pessimistic supremum is `3/8`, unattained with limiting aggregate `1/2`. The compressed implementation returns exactly these outcomes and the original-face baseline rejects the singular principal minor. This exercises a feasible interior point of a flat contact interval and a different pessimistic limiting value, beyond the manuscript's strict jump example.

A second independent instance with `d=(1,2)`, `c=(-1,-1/2)`, `u=(1,1)`, `h=4/5`, `gamma=1` and prices `[0,2]` exercises quadratic cuts in distinct fields, including `3/4+sqrt(15)/20` and `7/10+sqrt(6)/10`. The two complete solvers agree under the capacity row for both semantics. These results are retained in `independent-boundaries.json`.

The isolated LaTeX build succeeded with 73 pages and no warnings, undefined references/citations or overfull/underfull boxes in its final log. I rendered and viewed the frozen contact figure. Build evidence is in `build-check.log` and the isolated `build/main.log`.

## Sources and review limits

I checked the relevant active-region and optimizer statements in Bemporad et al., Theorems 2 and 4, printed pages 8 and 10, in the [open original](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf). The manuscript uses the optimizer mechanism without importing an unjustified convexity assertion for its parameter-dependent follower value.

I inspected the allocation precedent in Kiwiel's [open report](https://rcin.org.pl/Content/139441/PDF/RB-2002-77.pdf), and the convex-envelope discussion in Moehle et al., Section 6.3 and Appendix B, in the [published open paper](https://web.stanford.edu/~boyd/papers/pdf/portf_constr_lcso.pdf). Gardiner–Lucet's [publisher abstract](https://link.springer.com/article/10.1007/s11228-010-0157-5) supports the narrow statement that piecewise-quadratic envelope algorithms already exist. I did not access its subscription full text or rely on it for the original-contact or rational-bit proof.

I did not rerun the entire timing suite or replace official measurements. The review verifies the recorded protocol, source provenance, data, summaries and targeted executable contracts; it does not reproduce historical hardware conditions or establish statistical speed guarantees. Finite tests do not prove the general algorithms, and the symbolic backend is not a general QE implementation. No such broader conclusion is claimed in the manuscript. The final synthesis and whole-manuscript gate remain stage 7 work.
