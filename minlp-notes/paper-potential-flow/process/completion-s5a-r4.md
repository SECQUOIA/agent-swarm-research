# Independent S5a review — reviewer 4

The section is mathematically sound subject to one minor correction to the wording of an error bound. I found no major issue. In particular, the new fixed-measurement maximization theorem for independent polynomial-law cycle polytopes, with the stated rational local capacities, is supported by the proof. It does not rely on transferring the quadratic finite-set algorithm without justification.

Initial and final SHA-256 of `complexity/sections/08-design.tex`:

`85ea7d7942ab63a9a94d4a91dd10b9e3b30b736982a4f58c6a2af52007807295`

Both hashes match the supplied frozen source. All line numbers below refer to this source. I changed no manuscript source and ran no manuscript build.

## Findings and verdict

### Minor R4-1: use absolute coefficients in the scalar-value error bound

**Location:** lines 353–355, proof of `thm:a-design-independent`.

The instruction to refine until “the sum of its rational coefficient times its enclosure width” is below the error should say the **absolute value** of each coefficient. The coefficients `gamma_C` are signed. For example, coefficients 1 and -1 and equal positive enclosure widths give a signed sum of zero, although the two contribution errors can add. A signed sum therefore does not certify the claimed additive precision.

**Concrete correction:** replace the instruction with

`sum_C |gamma_C| width(I_C) < epsilon`,

where `I_C` encloses the selected endpoint, and evaluate using any rational point in each enclosure. Alternatively, require every width to be at most `epsilon/[2(1+sum_C |gamma_C|)]`. The earlier quadratic flow-box theorem already uses this latter kind of absolute-coefficient bound. The change is minor because the correct bound has the same polynomial encoding and refinement complexity and does not change the theorem or scenario construction.

**Major findings:** none.

**Verdict:** accept after the minor correction above. The explicit new polynomial-law/local-capacity extension passes. The source-access limitations recorded below limit the scope of my literature verification; they do not reveal an unresolved mathematical obstruction.

## Coverage and mathematical checks

### Exact monotone-root optimization

I read the complete statement and proof of `thm:a-design-root`, including both optimization directions and the arithmetic recovery argument.

The rational threshold LP equivalences have the right weak inequalities. At a root of a convex combination of parameter vertices, the affine combination of their balance values is zero. This supplies vertex roots on both sides and establishes attainment without assuming differentiability or a uniformly positive derivative. Strict increase gives the quasilinear level-set assertion. In particular, an optimizer need not be found by enumerating the vertices.

The active-row argument remains valid when the H-polytope is lower dimensional: a vertex without a full-rank set of active normals would admit small displacements of both signs. Clearing rows gives the stated determinant bound, including when parameter dimension grows. The common denominator for all polynomial pieces has polynomial bit length. Substitution at a rational vertex gives height at most `(t+1) Delta P_0`; dense degree and the explicitly listed piece count control its encoding.

Strict increase excludes a specialized constant polynomial on every positive-width piece. The product of two vertex-piece polynomials covers comparisons between different vertices and different pieces. Passing to its primitive squarefree part handles repeated roots, shared roots, and repeated factors. I checked the factor-height and discriminant argument independently: Cauchy's radius bound and the nonzero integral discriminant give a reciprocal exponential separation whose logarithm is polynomial in dense input. The displayed `sigma` is more conservative than needed and is valid. Degree zero is excluded by the promises.

For the maximum, the lower bisection endpoint satisfies the true threshold test even when the optimum is at the initial bracket endpoint. Minimizing the balance at that endpoint produces a vertex root in the final bracket, which must coincide with the maximal vertex root once the width is below `sigma`. The dual argument for the minimum uses the upper endpoint and has the correct sign. Equality does not require a strict-root-separation claim between equal roots.

Sequential coordinate minimization takes faces of the original polytope. Thus the bounds on the original vertices also bound the intermediate coordinate optima; there is no uncontrolled iteration of LP encoding bounds. Once the vertex is recovered, breakpoint evaluation selects the unique root or a rational breakpoint zero. Squarefree univariate isolation gives degree at most `D`. The argument uses numerical dense degree, not a binary exponent. It correctly excludes moving breakpoints and nonmonotone branch selection.

### Passive laws, local intervals, and rational profiles

I checked the general-law existence argument against the earlier existence, block, and cactus-cycle lemmas. A primitive of a continuous strictly increasing zero-normalized law is strictly convex and has the stated positive linear lower bound outside `[-1,1]`. The energy is coercive on the conservation affine space. Its stationarity condition supplies potentials, including for a rank-deficient incidence matrix. No surjectivity or superlinear growth is required.

Positive flows after reorientation strictly decrease potential, so their directed support is acyclic. A source-to-sink decomposition bounds each flow magnitude by the total positive nomination, and hence by the looser bound `B=sum |b_v|` used here. Bridge flows and effective cycle nominations depend only on conservation. The consistently oriented cycle coordinate can be chosen as an actual reference-edge flow, so its root lies in `[-B,B]` without an offset correction to that bracket.

Reversing an input edge changes its law to `-g_e(-x;theta)`; this works for nonodd laws and preserves the affine parameter form. Translated breakpoints are fixed rational numbers. Expanding each translated dense polynomial requires powers of rational offsets and binomial coefficients with polynomial bit length; the construction forms a union of partitions and sums of polynomials, not a product of all edge laws. A cactus cycle basis makes the individual scalar consistency equations sufficient globally.

The root map is continuous on its compact parameter domain. Strict signs around a root give the required stability, and the common bracket handles endpoint roots. Its image is an interval because the parameter polytope is connected. Independent cycle parameters then give the full product of these intervals. This argument also covers constant root maps and zero-length intervals.

For rational target circulation, the two rational LP balance optima straddle zero exactly when the target is attainable. The displayed convex combination has the correct coefficient and preserves the affine constant term. When the two LP values agree they are both zero. The rational numerator and denominator lengths are polynomial, and no division by physical edge flow occurs. Thus zero flows cause no interpolation failure.

Rational capacities become scalar clipping values. Comparing each algebraic endpoint with each rational clipping value is a univariate exact comparison. A clipped endpoint either retains an existing rational original profile or is rational and has an interpolation profile. An irrational singleton must inherit an original endpoint because rational clipping cannot create a new irrational value. Combining the stored profiles therefore satisfies tight capacities exactly. Linear objective optimization selects endpoints according to rational coefficient signs; it requires no comparison between sums of unrelated algebraic roots. The scalar-value approximation needs the minor absolute-value correction above. Exact scalar comparison is correctly separated from exact scenario output.

### Global parameter correlations and capacities

The inequalities `H_C(a_C,theta)<=0<=H_C(b_C,theta)` are equivalent to both weak circulation bounds. Reversing an arc or a negative circulation coefficient reverses the scalar bound correctly. Constraints with zero circulation coefficient, as well as bridge bounds, are constant tests. Conjoining the affine inequalities with a bounded rational global parameter polytope is precisely one rational linear feasibility problem.

For robust validation the lower-bound maximum must be nonpositive and the upper-bound minimum nonnegative. A strict failure gives a rational LP optimizer that is a genuine violating original scenario. Equality is accepted. Individual arc extrema follow from the root theorem over the original or capacity-filtered parameter polytope and rational shifts/sign changes. The zero-nomination case and the edgeless connected graph are handled before requiring a nondegenerate root bracket.

The theorem does not assume that the globally correlated flow image is convex or a box. The later product-box algorithms are expressly restricted to independent cycle polytopes. I found no unintended transfer of independent attainability to global correlations.

### Convex minimization and the Lipschitz extension

I checked the extension lemma as a mathematical construction, not only its citation. Extending the cube-restricted function by positive infinity makes its perspective convex on the appropriate perspective domain. The derivative in the perspective variable is at least one because of the stated choice of `M`. Hence minimizing that variable selects `t(z)`. The proof's support inequality follows by multiplying the cube support inequality by the positive perspective variable. The multiplier `K` is positive and has the claimed upper bound. At cube-boundary points, choosing zero as a subgradient of `t` is valid; outside the cube a signed maximal-coordinate vector works, including ties. The support argument at two points yields the stated global Lipschitz constant. All queries and subgradients are rational with polynomial encoding.

For the surrogate-box construction, an inner interval lies in the exact feasible interval and projection into it moves a circulation by at most `eta`. If the two rational inner endpoints cross, the true interval has width below `2 eta`; freezing at `L_C^+` gives the stated forward comparison bound, and replacing it with the stored exact `L_C` moves each affected edge by at most `eta`. Disjoint supports justify the total `2m eta` and `m eta` one-norm bounds. Every surrogate flow lies in the expanded flow box where the gradient bounds and promised convexity of `f` apply.

All fixed surrogate coordinates are removed, including rational intervals of zero width. The remaining positive widths have polynomial rational encoding, so rescaling to the cube does not require an inverse physical condition number. Evaluation of `f(Tz+a)` and its gradient by composition avoids a needless multivariate expansion. The displayed bounds for `V`, `G`, and the extension are sufficient. Cube convexity is used only on the cube; the explicitly constructed extension supplies the global hypothesis of the cited ellipsoid theorem.

I verified Dadush's exact theorem formulation: it returns a rational point in the convex body, not merely a point in an outer neighborhood. The cube has the required known center and inner/outer radii, and exact rational evaluation is stronger than the requested approximate rational value oracle. Thus the final returned cube point gives rational retained circulations that can be realized exactly. Frozen cycles use exact endpoint profiles. The loss budget is `3m G_f eta+epsilon/2 <= 11 epsilon/16`. Capacities hold for the recovered physical flow even when the frozen surrogate itself violates them. The quadratic corollary follows directly.

### Bounded-data Max-Cut construction

For `n>=1`, the described chain can be made with `3n` distinct triangle vertices and `n-1` bridges, hence `4n-1` edges. Entry and exit vertices are distinct; an internal entry or exit has two triangle edges and one bridge, so maximum degree is three. There are no parallel edges or shared triangle edges. The first entry and last exit are the only nonzero nominations, of magnitudes one. Every intermediate cut enforces unit through-flow.

The two alternate-path resistances sum to four. Equating its potential drop to the direct-edge drop gives `beta_i x_i^2=4(1-x_i)^2` with the physical root `x_i=2/(2+sqrt(beta_i))`. The full resistance interval gives precisely `[1/3,2/3]`. Each choice of direct flow is independent across triangles because potential offsets across blocks are free to adjust. The direct and alternate flows are positive throughout, so the unsigned quadratic expressions used in this computation agree with the passive laws.

The objective is a convex quadratic on the full edge-flow space, with zero coefficients for the unused edges. Under `z_i=3x_i-1`, its restriction is the usual sum of squared binary differences. A coordinate-by-coordinate endpoint argument shows that a cube maximum has a binary maximizer. At that maximizer the objective is an integer cut size.

The two resistance endpoints are rational and yield rational physical flows. They certify both integer-threshold attainment and violation of a half-integer bound. The restricted-family NP and coNP memberships consequently do not depend on a conjecture about exact sums of algebraic numbers. Strong hardness is justified: every physical numeric datum is constant, and the expanded quadratic coefficients and threshold have polynomial magnitude, so unary encoding remains polynomial. An additive value error of at most one quarter determines the unique nearest integer optimum. The text correctly states a value-approximation contract for the unnormalized displayed objective.

As a diagnostic, I used Python `Fraction` arithmetic to enumerate all simple labeled Max-Cut graphs on one through five vertices and all binary assignments. All **33,866** endpoint assignments satisfied both the triangle drop equation and exact objective/cut equality. This check is finite supporting evidence; the preceding symbolic identities and reduction establish the general result.

### Fixed measurements, new extension, and fixed rank

The continuous model first obtains the exact capacity-clipped independent circulation box, with rational original profiles for both endpoints. This uses the new polynomial-root theorem with its degree and bit bounds; quadratic formulas are not assumed. The finite quadratic model instead obtains the convex hull of its attainable Cartesian product. The earlier theorem proves that each endpoint has an original finite-set realization. The proof keeps these two sets distinct.

For either model, projection has rational directions `a_C=R Z_C`. Algebraic endpoint differences change segment lengths and the translated center but do not change the nonzero rational generator hyperplanes. Every strict sign pattern is feasible precisely when its finitely many signed inner products can all be scaled to at least one. Therefore rational LP feasibility is an exact implementation. Feasible rational polyhedra have polynomial-size rational points even when these particular sign-region polyhedra are unbounded. The incremental arrangement algorithm keeps only realizable full-dimensional patterns at every stage; its region bound in fixed dimension prevents exponentially many surviving patterns. Repeated and dependent normals are harmless.

A vertex of a lower-dimensional polytope still has an ambient full-dimensional open set of exposing directions. Choosing one away from the finite union of nonzero-generator hyperplanes selects the appropriate endpoint for each positive-length segment. Zero-length segments can subdivide the arrangement without changing the candidate point. Zero directions can be ignored. This proves complete vertex coverage, including a point zonotope. It does not require constructing or comparing algebraic normal vectors.

A convexity box containing the finite attainable set also contains its convex hull, so maximizing a convex function over that hull gives the same maximum as over the finite original scenarios: the candidate vertices are attainable. No finite-set capacity clipping is claimed. In the continuous case, local capacities have already been incorporated before candidate enumeration, and every stored endpoint profile is exactly feasible. Globally correlated capacities and constraints coupling distinct cycle circulations remain outside this argument.

For candidate comparison, physical flow bounds imply `|Rx|_infinity<=T_0`. Independently refining each selected circulation to error `delta` gives coordinate measurement error at most `M_0 delta`. The enlarged box accommodates the whole segment between a true and approximated measurement. The derivative bound on that box requires polynomial evaluation only, not convexity outside the promised box. The chosen `delta` gives value error at most `epsilon/8` per candidate, and selecting the largest rational estimate costs at most two such errors. Returning the stored original profile rather than the approximate circulation preserves exact feasibility. Polynomial endpoint degree, coefficient bits, requested precision, rational sums, and dense objective evaluation together give the stated `N^{O(k)}` bound. A common compositum of algebraic fields is unnecessary.

The PSD fixed-rank corollary is valid with rational `LDL^T`: rational square-root factors are unnecessary because the rational positive diagonal factors become coefficients in the measurement-space quadratic. A zero pivot in a PSD Schur complement has a zero row and column. Adding the linear objective as one measurement handles the affine term without assuming that it lies in the range of `Q`. Rank zero also works. The corollary preserves the continuous/finite capacity distinction of its parent theorem.

## Literature and dependency audit

I read the supplied review instructions and the user-provided global AGENTS instructions. No additional AGENTS file was present on the worktree's ancestor path. I also read `literature/AGENTS.md` before using the local primary packages. I did not read author, lead, check/build, adjudication, correction, peer-review, or historical review content. I did not consult historical mathematical reports after my pass either. No agents were spawned.

Earlier manuscript material read for the dependencies includes the existence and uniqueness proof, block decomposition and cactus-cycle proofs, the polynomial-law representation and validation proposition, the prescribed-flow realization theorem and reduction, and the entire quadratic cactus flow-box theorem, including its finite-set and square-root-sum distinctions. I inspected the bibliography entries cited by Section 8.

Primary checks were as follows:

- The original local Onn–Rothblum arXiv PDF, pp. 4–6, was checked through a fresh `pdftotext` extraction as well as its local extracted text. Lemmas 2.1–2.3, Algorithm 2.5, and Theorem 2.6 support the classical enumeration framework and the cited locators. The section's explicit rational sign-cone implementation supplies its own treatment of algebraic lengths. [Original source](https://arxiv.org/abs/math/0309083).
- The original local Aßmann–Liers–Stingl–Vera PDF, pp. 20–21 of arXiv:1808.10241v1, was freshly extracted to verify Proposition 4.9, Lemma 4.10, and Proposition 4.11. Its balance function has the opposite sign convention, consistent with its decreasing scalar equation. The interval-to-halfspace mechanism is properly credited. [Original source](https://arxiv.org/abs/1808.10241v1).
- The original local Del Pia–Dey–Molinaro PDF, manuscript dated October 10, 2018, p. 2, was freshly extracted. Section 1.1 gives the binary Max-Cut formulation used as predecessor. Its general MIQP membership theorem is not being used to assert membership for arbitrary algebraic network performance. [Author manuscript record](https://arxiv.org/abs/1407.4798).
- Dadush's thesis, Theorem 2.5.9 on printed p. 48, was checked in the author PDF together with the computational-model context. Its global Lipschitz/value-oracle assumptions and rational point-in-body conclusion match the use here. [Primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf).
- Boyd–Vandenberghe Sections 3.2.5–3.2.6, printed pp. 87–89, were checked in the author-hosted book for partial minimization and perspective convexity. The rational global extension is proved in the manuscript rather than attributed to those general preservation rules. [Primary book](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf).
- Agrawal–Boyd Section 3 and the Section 2 discussion support scalar-threshold bisection and quasilinear/linear-fractional context. Megiddo Section 2 supports exact recovery by parametric linear-objective optimization; it is appropriately treated as a predecessor, not as the dense-polynomial theorem being proved here. [Agrawal–Boyd](https://web.stanford.edu/~boyd/papers/pdf/dqcp.pdf), [Megiddo](https://theory.stanford.edu/~megiddo/pdf/rational.pdf).
- I located and read the relevant parts of the primary Ferrez–Fukuda–Liebling author manuscript, revised April 29, 2004, including the introduction and Section 3's enumeration/fixed-rank statements. This confirms the stated direct predecessor. The bibliography's comment about failed full-text retrieval need not remain an access limitation: a readable author copy is available. It need not change the published 2005 metadata. [Primary manuscript](https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf).

Two source limitations remain. The Mignotte 1974 JSTOR endpoint did not expose usable article text. I independently checked the factor-bound argument through the standard Mahler-measure derivation, and the weaker height inequality sufficient for the displayed `H_s` is also explicitly restated in Hinek–Stinson's primary research note, Theorem 1. I did not verify the complete original 1974 article. [Hinek–Stinson note](https://cacr.uwaterloo.ca/techreports/2006/cacr2006-15.pdf). The local Basu–Pollack–Roy original and existing extracted text have badly corrupted text encoding; a fresh `pdftotext` extraction did not provide a reliable locator audit for univariate root isolation. I therefore do not claim a fresh verification of the cited book's detailed univariate complexity proof. The use here is the standard dense univariate isolation/refinement primitive, with the degree, coefficient, separation, and query precision bounds separately checked above.

No broad priority search was undertaken. The section's restrained contribution statement is consistent with the primary predecessors I checked: the classical mechanisms are credited, while the specific arithmetic and rational recovery guarantees are demonstrated in the text. Scratch PDF extracts and the finite exact-arithmetic diagnostic were kept outside the worktree under `/tmp/s5a-r4`; only this assigned report was written in the repository.
