# Stage 8, round 1: independent whole-manuscript review 02

**Verdict:** Accept. I found no major issue and no minor issue requiring correction in the frozen manuscript. This is an independent scientific review, not a guarantee about an eventual journal's editorial decision or an assertion that no future research extension exists.

**Frozen source:** `process/snapshots/stage08-round01`; manifest SHA256 `d487e138b70585e03d5affa52a23e03631a30a45165651ddbe9d286162643231`. I recomputed the manifest hash and all 31 listed file hashes successfully. I read all seven sections, all four appendices, the abstract and bibliography in full. I did not consult other reviewers' reports or use previous acceptance decisions as evidence of correctness. I did not edit manuscript files, archived measurements or their provenance.

## Scope and independent findings

### Section 1: setting, contributions and literature

The introduction explains why a tractable follower oracle does not make the induced global upper optimization tractable, and identifies the compressed response dimension as the relevant structural restriction. It distinguishes one jointly optimizing follower from independent agents. The five contribution paragraphs agree with the subsequent theorem assumptions. They do not present the classical multiplier arrangement, conic support reduction, global comparison, convex envelope or fixed-dimensional elimination tools as new.

The fixed numerical degree convention is visible before the technical development and is maintained in the exact and approximation claims. Growing local row counts are correctly separated from fixed shared rows. Common-field output is defined, including the important distinction between one jointly selected output and a compositum of separately selected adverse witnesses. Pessimistic feasibility remains universal before adverse objective selection. These distinctions are preserved across the paper.

I independently checked the newly added Wu and Xiao–Chen comparisons against the actual primary sources, as detailed below. They support the manuscript's qualified novelty statement rather than overturning its specified theorem classes. The paper gives enough concrete comparison to make the importance and the precise claimed additions assessable. The comparison table explicitly avoids claiming that the paper subsumes every cited model.

### Section 2: exact quadratic compression

I checked local KKT necessity over possibly degenerate polyhedra, the conic support reduction modulo equality normals, nonsingularity of the block KKT systems, and the positive square-denominator representation. Validity tests include all original rows. Choosing a valid local formula by a jointly realizable sign condition is sound because the local effective quadratic is strictly convex. This is the key step avoiding an exponential Cartesian product of local statuses.

The product-denominator expansion is polynomial in the numerical degree in fixed compressed dimension; its growing degree does not contradict the bit bound. The global comparison includes every global optimum among feasible KKT candidates and therefore rejects nonglobal candidates without requiring sufficiency of nonconvex KKT. Quantifier copies remain fixed in number, including after upper optimization. The closed-graph/attainment proof uses fixed normals exactly where a uniform Hoffman bound is available.

I also checked moving local ranks, the determinant guards, nonattainment examples, the pessimistic worst-value and infimum predicates, the constant-Hessian degree refinement, and the supplied diagonal-plus-fixed-rank LP specialization. The constant-degree conclusion follows from the polynomial-count-independent output degree bound in the cited Basu–Pollack–Roy theorem, which I independently consulted. No unchecked matrix decomposition is being assumed to be discoverable.

### Section 3: robust measurements and screening

The measurement-fiber threshold is correct in both directions. In particular a thresholded feasible fiber KKT candidate is already a cost-near-optimal response; it need not be globally optimal on that fiber for soundness. The nominal value still requires global comparison. Eliminating one criterion's adverse variables before conjoining the upper rows preserves the fixed dimension when the number or combined measurement rank of the rows grows.

The robust attainment proof uses strict follower convexity, fixed normals and the positive-budget interpolation argument, with a separate zero-budget case. The positive-budget counterexample and Max-Cut transfer are consistent with these restrictions.

For dense screening, I checked the variational inequalities, completing the square, directional centers for response and true gradient, strict versus weak status tests, and the relative-interior extension to closed cells. The recovered free submatrix is SPD even when the set of certified free coordinates grows. Failed whole-cell guesses are not incorrectly used to exclude assignments on a subcell. The bound `M 3^t` is explicitly a recovery-LP count; the transition-neighborhood proof and all preprocessing qualifications are appropriately retained. The negative performance evidence does not undermine mathematical soundness, and the paper does not imply that a small perturbation automatically makes the displayed tests effective.

### Section 4 and Appendices B–C: accuracy-bit theorem (special depth)

I independently followed the inverse-approximation construction in Appendix B rather than assuming a numerical inverse oracle with adequate bit complexity.

* The interpolation proof gives the stated uniform increment lower bound even for signed coefficients and interior flat points. The clipped-inverse implication includes targets outside the marginal range.
* The critical-value calculation includes the real parts of **all complex** critical values. A real-only critical-value construction would not justify the analytic disks; the present construction does not make that mistake. The padded union has total length at most the prescribed bad tolerance. For every complementary gap, retained and omitted real parts give the claimed distance bound.
* The geometric panel progression has logarithmically many steps in inverse padding radius. A rational response center, rather than a rational approximation to an irrational target inverse used as though exact, gives a rational Taylor center and rational coefficients. The proper-polynomial covering argument justifies one holomorphic inverse branch on the entire critical-value-free disk. The branch agrees with the monotone real inverse along the relevant segment.
* The Cauchy tail and root bound give a polynomial truncation order. The recurrence and denominator formula are correct; integer denominator exponents grow linearly with order. Intermediate convolutions can be computed without enumerating exponentially many compositions. I checked exact inverse composition and the stated denominator identity on signed examples, including an interior derivative zero and nonreal critical points.
* The separate positive-coefficient Rouché argument uses nonnegativity in the derivative-disk estimate and is not silently applied to signed marginals.

For Section 4, the resource projection is a support-function test on a fixed-dimensional pointed arrangement. The effective multiplier and repair bounds in Appendix C are coarse but have polynomial encoding. Equality resources represented by opposite inequalities and degenerate feasible faces are included. The residual certificate's signs, complementarity allowance and aggregate-gradient error are correct.

The nonlinear branch recovery is especially important. The construction uses closed **validity intervals** of the selected inverse branches, not an unjustified operation of weakening strict inequalities in a nonlinear cell. Rational recovery takes place in the rational base polytope. It compares true clipped responses across potential branch changes; it never evaluates the old approximation outside its branch's validity. The transferred complementarity estimate includes the large negative slack bound for inactive resource rows. The allowance ledger `4 S eta`, `5 k Lambda S eta`, `4 A_U eta` is sufficient for the stated response accuracy.

Explicit monomial substitution preserves polynomial size in the fixed compressed dimension, with degree product `d_h d_a`; the aggregate-gradient argument degree is included. The upper Lipschitz constants are taken on the enlarged response box and allow signed coefficients. The minimization and rational recovery errors fit strictly inside the requested global additive tolerance. Exact membership of the recovered leader in the follower-feasible rational polytope is preserved.

I checked all upper-feasibility variants: the outer procedure's empty surrogate certifies original infeasibility, whereas a returned outer point alone does not; the inner procedure gives exact original upper feasibility but does not decide original infeasibility when empty. The posterior lower bound needs the inner point to establish original feasibility. The supplied tightening modulus, convex reduced-constraint anchor and follower-independent reserve interpolation each supply their own necessary extra assumption. The isolated-optimum and irrational-only-feasibility examples correctly show why these assumptions cannot be omitted.

For the sharp `1/P` modulus, I checked the common-active-row correction, gradient orthogonality and division into the two displacement cases. Moving affine right-hand sides are included through the rational row-space correction. It is not enough simply to count active patterns, because one can recur; the proof instead bounds connected components of each pattern's parameter set. Reciprocal-square lifts handle strict inequalities, and the hypersurface component bound applies without requiring compact lift variables. The number of variables and degree upper bounds are sufficient, and the resulting exponentially large numerical constant still has polynomial binary length. The segment subdivision plus continuity then gives the uniform pairwise bound. The power marginal establishes sharpness. The claimed extension beyond Wu's unconstrained result is precisely the moving-resource and effective-encoding conclusion, not priority for the exponent itself.

### Section 5 and Appendix D: structural and arithmetic boundaries

I followed the dense SAT construction's base-gradient margin and auxiliary feedback estimates, the continuous rounding gap, and the NP certificate from a stationary box pattern. The near-identity construction separately tracks scaled coordinate error rather than relying on a small absolute residual. Its exponentially small separation has polynomial bit length; the resulting exact/accuracy-bit hardness is compatible with the inverse-error grid theorem. No strong-hardness conclusion is inferred from bounded coefficients.

For the cost grid, saturation removes large incentive offsets from the numerical range, the maximum-volume row basis bounds all cost-direction combinations, and the direct leader term is minimized in each grid set. The exact projected-gradient/continued-fraction oracle has a valid denominator bound and an iteration count polynomial in the stated condition parameter. The absence of response-dependent upper rows is explicit.

The growing-leader parameterized classification is attributed to its source. I checked the manuscript's rescaling/duplication transfer, the independent mixed-radix rounding argument, the bounded-core arrangement construction and its closure justification. The leader-path Subset Sum reduction and distance-message identities distinguish a weak-hardness gap from an exponential explicit-message example.

For the follower path I checked endpoint enumeration, the telescoping identity, parabolic exposure, strict quadratic response inequality and fixed-coefficient padding. The nonconvex quadratic upper row is indispensable and is repeatedly disclosed; the slab-only problem is not claimed hard. Appendix D's sparse-shadow factor argument concerns an unextended two-variable quantifier-free description and does not imply a pointwise oracle lower bound. Equal-gain strips have the correct gain-sign reversal, zero-edge treatment at the original head, all-pairs difference constraints and recovery; fixed **total** cycle rank controls retained dimension.

The curvature, sparse-degree, rational-output and radical-field obstructions have the claimed scopes. The two-power and one-power lower bounds follow from a positive rational leader requiring denominator exponential in the numerical power. The root-sum argument proves exponential field degree and embeds a comparison problem whose exact complexity is left open; it does not label that problem NP-hard.

### Section 6: algorithms and evidence

I read the scalar construction, all completeness and upper-optimization proofs, both contact examples and all protocol/results prose. The convex piece certificates require exact coverage. The aligned sweep allows signed loadings and a negative coupling coefficient only when the full Hessian is SPD. The nonconvex fiber proof covers zero loadings, fixed boxes, flat pieces, isolated price contacts and both signs of the tariff coefficient. Candidate comparison is on original values. The incremental contact argument retains every potentially distinct final response. Convexification is used for values only unless the original-contact equality is checked.

I additionally read the independent face-baseline implementation and the full-task correctness checker. The baseline's nonzero-principal-minor restriction is enforced, and the paper does not use its value-only predecessor as evidence of full-response completeness. I ran the 18-instance full-task check in an isolated copy, including all response-set comparisons and direct returned-witness checks. It passed, including singular-minor rejection and compressed flat/fixed/singleton cases. I independently recomputed all 14 rows of full-task and scalar-scaling timing medians from the raw JSON; they agree with the frozen tables. I checked that all 60 recorded worker exit codes are zero. I did not rerun a timing campaign or overwrite raw data.

The experimental conclusion is suitably limited: small original-coordinate comparisons, larger repeated populations separated from heterogeneous instances, and screening slower than the tested numerical comparator once preprocessing is included. Numerical MILP gap zero is not treated as an exact certificate.

### Appendix A and Section 7: recovery and integration

The fixed-core support construction includes every local vertex needed for support, even in lower-dimensional polytopes, and invalid moving determinants are guarded. Support inequalities exactly characterize the compact Minkowski sum. Keeping additional feasible support tuples at the selected leader is safe; the shared-weight Carathéodory recovery preserves all block measurements in the selected field. It is not used to mix nonconvex follower optima.

The conclusion reflects the proved results and scopes. It separates global upper hardness, explicit representation size and pointwise follower evaluation, and accurately describes the computational limitations. The manuscript is mathematically standalone. Its mathematical LaTeX build does not require internal notes, process records or external literature files. Some computational reproduction scripts intentionally use the accompanying repository's older algorithms/data, as disclosed in the README; this does not create a missing mathematical dependency in the paper.

## Primary literature independently consulted

1. [Wu et al., arXiv:2603.00027v1](https://arxiv.org/html/2603.00027v1), model (1), Assumption 3.2, Lemma 4.2, and Appendix B.1, equations (17)–(21). The response exponent follows from uniform growth and the leader-Lipschitz lower gradient. The manuscript's attribution is accurate; the global approximation theorem here is not a stationarity guarantee.
2. [Xiao and Chen, published ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/4574ac9854d4defe3bf119d07b817084-Paper-Conference.pdf), Definition 2, Sections 2.2–3.2 and Theorem 1. The global guarantee is about a penalty problem under its PL and accompanying assumptions, with approximate lower optimality. The manuscript correctly acknowledges this global result instead of describing all first-order literature as stationarity-only.
3. Local **original PDF** of Hochbaum and Shanthikumar (1990), Sections 1.2–1.3 and Theorem 1.1. I made my own text extraction. It does approximate the solution vector with logarithmic accuracy dependence and numerical subdeterminant dependence. The manuscript now credits exactly that; no objective-gap-only misdescription remains.
4. Local **original PDF** of Jeyakumar et al. (2016), Theorem 2.3 and its proof. The feasible follower set is independent of the leader, and the solution-set estimate is one-sided at a fixed reference leader with degree/dimension-dependent exponent. The Appendix C comparison is accurate.
5. Local **original PDF** of Basu, Pollack and Roy (1996), Theorem 1.3.1. The output polynomial degree is independent of the number of predicates, supporting the constant-Hessian refinement. The paper separately controls the total variable count and bit encodings.

I also conducted fresh searches for separable polynomial bilevel optimization with fixed shared dimension and inverse/accuracy-bit global guarantees. They did not reveal a directly subsuming theorem. This bounded search supports only the stated qualified comparison, not a proof of absence of earlier work. I did not independently retrieve and reread every bibliography item, and I make no such claim.

## Reproducible checks and limits

Evidence is under `verification/stage08-review02/`:

- `hash-check.txt`: the manifest and all 31 file hashes verified.
- `standalone/build/main.pdf`, `build-output.txt`: an independent 78-page build, with no final warning, undefined-reference/citation or overfull-box message. I visually inspected the first page from `front.png`.
- `checks-output.txt`: all 18 complete-task cases plus singular/flat/fixed/singleton and iterator regressions passed.
- `accuracy-checks.py`, `accuracy-output.txt`: exact increment and both-orientation Bregman inequalities on 408 rational intervals; order-12 inverse-series composition and denominator identities for three increasing marginals, including signed coefficients with an interior flat point and with nonreal critical points. These are diagnostics, not a replacement for the analytic proof.
- `data-check.txt`: 60 successful worker records and all 14 full-task/scaling table rows independently recomputed.
- `hochbaum.txt`, `jeyakumar.txt`, `bpr.txt`: my own primary-PDF extractions used above.

My initial build command was launched from the repository root and failed only because there is no root `main.tex`; the corrected command in the isolated source directory built successfully. The full-task checker was supplied the actual repository path for its disclosed old-solver comparison import, while all generated check outputs remained inside this review's isolated copy.

This review is not machine-checked formal verification of every proof, exhaustive testing of every implementation input, a new benchmark campaign, or a complete all-literature priority search. Within the complete manuscript reading and independent depth checks described above, **major issues: none; minor issues requiring correction: none**.
