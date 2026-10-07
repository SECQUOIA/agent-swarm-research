# Sol prewriting audit: conditional recourse, native integers, flow, TU, and component algebra

Date: 2026-10-05. Reviewer: Sol. This is a new analytical audit of the saved source proofs. It does not rerun their optimization diagnostics or establish publication priority.

**Decision.** The audited results can support a submission manuscript under their stated oracle, representation, curvature, and fixed-feasibility contracts. I found no substantive mathematical blocker. Several distinctions are essential to a correct paper: all residual coordinate restrictions must be solvable; core-only noise needs either uniform strong residual convexity or the flow/TU optimal-face certificate; general nonlinear boundary-flow/TU precision is parameter dependent; and expanded algebraic output must preserve a shared root within each component. Older reviews and companion wording contain superseded algebraic bounds and output terminology. Those should not be copied into the manuscript.

The source collection is substantial but can be organized around one proof chain: conditional values give a sparse core search, restricted recourse certifies global containment or excludes competitors, and an exact closure or small-core solve completes the sampled instance. The continuous and discrete boundary arguments require different closure certificates. Their common search does not make their assumptions interchangeable.

**Sources read.** I read the assigned recourse, flow, TU, low-rank integer, local-error, and rank-separation notes; the relevant supporting multiplier and active-stratum notes; the current component primitive-limit solver; both strong-field component notes; the existing exact-arithmetic recourse section; and the applicable independent reviews, including the constant-base transfer and explicit-budget reviews. Source references below are relative to this review.

**1. Common core search and exact oracle contracts.**

Let the domain be a product of a continuous core box and one residual feasible set that is fixed independently of the core. For a rational fixed core, the query objective must include the actual sampled linear coefficients. The residual problem may change costs with the core, but it may not change feasibility, supplies, balances, right-hand sides, or native bounds except through an explicitly requested restriction. The input is an explicit rational polynomial of fixed total degree. Promised certificates, their sizes, and their verification costs belong in the input length.

The required conditional interfaces are distinct:

| Result | Required conditional oracle | Exact returned object |
| --- | --- | --- |
| Quadratic continuous recourse | Exact global rational minimizer and value on every rational residual subbox, including infeasibility | Rational full optimizer and value |
| Polynomial continuous recourse | A rational feasible completion and rational interval of prescribed width on every rational residual subbox | Usually a unique strongly convex patch minimizer; rare algebraic fallback |
| Native integer recourse | Exact rational optimal value and integral minimizer on every tightened integer coordinate box, including infeasibility | One integral label and one algebraic core tuple; rational for quadratic slices |
| Core-only flow/TU | Exact separable convex integer minimization under every tightened interval, including modified derivative costs | One integral label and one algebraic core tuple |

An unrestricted conditional optimizer is insufficient for the first three interfaces. A local stationary point, a feasible upper value, a heuristic global value, or an approximate value without a certified lower endpoint is insufficient. A general rational integer polytope does not supply any of these oracles merely by being finitely described.

At fixed residual noise, the true conditional value satisfies upper coordinate curvature \(L\): for each core coordinate, subtracting \(L v_i^2/2\) makes every fixed-residual objective concave in that coordinate, and their infimum is concave. The same value minus the core linear noise is independent of the entire core-noise vector. This argument requires fixed residual feasibility.

For dyadic side \(h\), coordinate interpolation gives correction \(e=kLh^2/8\). Exact queries retain all optimal core cells, give an incumbent gap at most \(e\), and give a \(2e\)-near-optimal true corner in every retained cell. Approximate queries with width \(e\), evaluated before the final retention decision, give the corresponding bounds \(2e\) and \(4e\). Adaptive oracle choices do not enter the probability calculation: they imply events stated using the true deterministic conditional value.

For a fixed core grid tuple, comparing both neighboring points cancels all other core-noise terms. The interval for its \(i\)th noise coefficient therefore depends on the tuple and residual noise, but not on another core coefficient. Its length is at most \(Lh(1+k/2)\) for exact recourse and \(Lh(1+k)\) for approximate recourse. Independence is consequently available. Summing interior points adds at most one atom term per coordinate when \(M h\ge1\); the two original endpoints contribute two more choices. This proves the saved factors

\[
Q_{\rm exact}=\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k,
\qquad
Q_{\rm approx}=\left[3+\frac{(1+k)L}{2\sigma}\right]^k.
\]

Cell incidence, children, and corners give \(8^k\) times this count per level. Only children of retained cells are generated. The paper must not describe preliminary enumeration of the full fine grid. The case \(k=0\) is direct recourse for exact integer/quadratic interfaces; polynomial continuous localization uses the explicitly stated empty-core accuracy convention.

The common state factor is numerical. Binary encoding alone does not control \(L/\sigma\). Unit core coordinates are part of the model; affine rescaling changes the physical noise and curvature. A supplied curvature bound may be much sharper than a coefficient-sum bound, but verifying its certificate must be charged.

See [exact box recourse](../../../research-20261002/new-direction/smoothed-box-stable-recourse.md), [polynomial box recourse](../../../research-20261002/new-direction/smoothed-polynomial-box-recourse.md), and [native integer recourse](../../../research-20261002/new-direction/smoothed-native-integer-recourse.md).

**2. Continuous exclusion and convex closure.**

The sound localization argument uses a bound \(G\) on the core gradient one-norm over the original real domain, uniform over the support of the sampled noise. It follows that every conditional value over every fixed residual subset is \(G\)-Lipschitz in core infinity distance. The proof evaluates a conditional minimizer at the other core point and then reverses the comparison; it does not require residual convexity.

Let \(c\) be the incumbent core corner in the retained hull \(D\), let \(z\) be its feasible residual completion, and let \(P\) be the residual patch of radius \(r\) centered at \(z\). The closed restrictions \(x_i\le z_i-r\) and \(x_i\ge z_i+r\), when their raw thresholds lie strictly between the original endpoints, cover the complement of \(P\). A restriction at an original endpoint must be omitted when clipping made that side of the patch equal to the endpoint. Adding a singleton there could include a valid active optimizer and defeat the intended gap. Closed artificial-boundary slabs are otherwise correct and conservative.

For exact recourse, \(V_{\rm out}(c)-V(c)>2G\operatorname{diam}_\infty D\) certifies that every conditional optimizer at every core in \(D\) lies in \(P\). For approximate recourse, replace the excluded value by a certified lower endpoint and the incumbent by its feasible upper value. The inequality then remains sound. This certificate excludes all competing conditional minimizers, including tied ones. An excluded feasible upper value cannot substitute for the lower endpoint.

Uniform strict derivative signs permit fixing a continuous coordinate only at an original bound contained in its current interval. Such tests preserve every global optimizer contained in the product patch. Fixing an artificial patch endpoint without that condition is unsound. A zero derivative at a contained optimum cannot pass a strict uniform sign test.

For quadratics, the Hessian is constant, and an exact PSD test with positive modulus on the remaining principal block certifies a convex QP. For general polynomials, a rational midpoint Hessian and a rational Hessian-variation bound certify a positive modulus over the whole remaining box. The saved row-sum definitions bound the needed Euclidean operator norms: symmetry converts the Hessian row-sum bound to an operator bound, and the third-derivative row sums bound Hessian variation in infinity distance. The midpoint gradient test includes both variation from the optimizer to the midpoint and the additional box-radius error.

The stopping proof is valid: full point growth bounds the incumbent's distance and every retained cell's corner distance; adding one cell width bounds the hull. At the saved cutoff, excluded points are at least \(3r/4\) from the optimizer, while the incumbent is at most \(r/4\) away. The approximate lower gap is at least \(7g_0r^2/16\), and the cross-core comparison costs at most \(g_0r^2/4\). All original active coordinates with sufficiently large gradients are fixed. Two-sided directions in the point-growth inequality give Hessian at least \(2g_0I\) on the true remaining free face, and variation then makes the explicit Hessian test pass. All tests are sound without assuming that the probabilistic good event occurred.

Residual convexity, rather than residual strong convexity, suffices for the approximate conditional oracle. Weak convex optimization on a capped epigraph, followed by clipping to the rational query box, gives feasible rational near-minimizers even for thin boxes and flat minima. More usefully for the proof record, convexity gives the directly checkable tangent lower endpoint

\[
\ell=f(y)+\min_{x\in B}\nabla f(y)^T(x-y),\qquad u=f(y).
\]

The endpoint linear minimization is explicit. If the feasible \(y\) has sufficiently small objective error, a segment smoothness bound forces \(u-\ell\le\eta\). The saved choice of objective accuracy \(\min(\eta/2,\eta^2/(8K_f))\) is sufficient. A verifier checks feasibility, value, gradient, the endpoint linear minimum, and the requested interval width using the supplied convexity proof. No positive residual modulus is hidden in this recourse argument.

Ordinary polynomial continuous output is an exact implicit answer: the unique constrained minimizer of a specified rational strongly convex polynomial on a specified rational patch. It is not an expanded coordinate list. Its descriptor has polynomial length, and its coordinate/value evaluation is polynomial in the requested bits using the positive modulus. The global pruning proof has only an expected size bound. Rare same-draw fallback may have exponentially large algebraic output, with polynomial expected contribution. Expanded degree may be large even on an ordinary draw; compact patch output does not claim otherwise.

The forest corollary is sound conditional on the established exact rational forest-QP oracle. Fixing core coordinates changes only residual linear terms; restricting boxes, deleting fixed coordinates, and affine interval rescaling preserve the residual forest interaction graph. This is a feedback-vertex-set composition, not a theorem parameterized by treewidth alone. The manuscript must cite and verify the actual Turing-model forest algorithm rather than replace that interface by an informal real-arithmetic solve.

**3. Core-only continuous noise: strong residual convexity and zero multipliers.**

Uniform residual strong convexity supplies a unique selector \(s(v)\), with Lipschitz constant \(H=M_1/\mu\). The variational-inequality proof works with boundary residual minimizers. Projected growth \(g_V\) lifts to full point growth with

\[
g_F=\min\{g_V/(1+2H^2),\mu/4\}.
\]

The original \(L\) still controls the state count. Large mixed derivatives and \(1/\mu\) affect bit precision through their encodings and derived cutoff constants; they do not become extra numerical factors in that count. Under qualitative residual interiority, the full remaining Hessian follows directly from growth after active core coordinates are fixed. There is no need for a numerical residual distance from the original endpoints, and a valid returned patch may touch them.

The stronger changing-residual-face theorem removes residual interiority. Its new argument has two indispensable parts. First, on each closed original core face, define residual active-set boundaries in the relative topology of that closed face and add the ordinary affine-box boundary separately. The selector is continuous and semialgebraic. These sets and their free-gradient images are compact, have dimension at most one less than the face dimension, and are fixed before sampling. The saved three-block KKT formula gives a base-computable algebraic degree enclosure. A singular-algebraic tube estimate and exact grid jitter bound include every atom on the exceptional image. A union over original faces is valid; no conditioning on an adaptively selected face occurs. Zero-dimensional faces have no tangential transition event and are handled directly.

Second, on a two-sided stable tangential ball, active residual multipliers are nonnegative but may vanish. If \(K_3\) bounds a multiplier's Hessian, nonnegativity and Taylor expansion give \(\|\nabla\lambda_i\|^2\le2K_3\lambda_i\) for multipliers below \(K_3\eta^2/2\). Eliminate the already interior residual variables. The reduced core Hessian is at least \(2gI\); the reduced residual block is at least \(\mu I\). Releasing every active bound below

\[
\theta=\min\{K_3\eta^2/2,\mu g/(4mK_3)\}
\]

costs at most \(\mu g/2\) in combined squared cross norm. This is a simultaneous Frobenius-norm estimate, not a sum of losses after incompatible sequential eliminations. Completing the square after restoring the eliminated coordinates gives the saved positive modulus

\[
\nu=\min\left\{\mu/2,
\frac{\min(g,\mu/2)}{1+2H^2}\right\}.
\]

The derivative calculation is correct: implicit second derivatives are bounded by \(B_3(1+H)^2/\mu\), and the multiplier Hessian by \(B_3(1+H)^3\). Taking \(B_3=nT\) is safe, albeit conservative. Extra sound fixings leave a principal matrix and preserve the modulus. The algorithm does not identify the stable branch or classify weak multipliers; it fixes detectable strict signs and checks the Hessian on the remaining box.

Applying the multiplier estimate in an unfixed one-sided core normal direction would be invalid. The theorem applies it after active core coordinates have been fixed, in the free tangent coordinates of the true core face. At a core vertex, residual strong convexity supplies the remaining modulus directly. Identically zero residual multipliers are permitted and cannot pass the strict sign tests.

This proof does not extend to mere residual PSD, qualitative strict convexity, or a unique residual minimizer without a uniform modulus. The rotating-fiber note supplies exact, easy counterexamples to the full-Hessian closure mechanism. Those examples are not hardness results for exact optimization. Also, the strong-residual class itself admits a fixed rank-at-most-\(k\) core quadratic convexifier of scale \(M_1+M_1^2/\mu\). Its contribution is preserving the original \(L/\sigma\), not proving the absence of such a convexifier.

The restricted interior theorem is a useful explanatory antecedent, but its algorithmic scope is subsumed by the changing-face theorem. The paper can give its short growth-lift argument before the stronger theorem without presenting it as an independent larger capability. See [strong interior recourse](../../../research-20261002/new-direction/core-only-noise-strong-recourse.md), [changing faces](../../../research-20261002/new-direction/core-only-noise-boundary-recourse.md), [active-stratum tube](../../../research-20261002/new-direction/core-noise-active-stratum-tube.md), and [small multipliers](../../../research-20261002/new-direction/small-residual-multiplier-curvature.md).

**4. Native integer labels and exact small-core completion.**

For any integral incumbent label \(z\), the union of \(z'_i\le z_i-1\) and \(z'_i\ge z_i+1\), over all residual coordinates, is exactly the feasible residual set minus \(z\). Linear coupling among labels does not change this identity. The \(2r\) tightened-bound queries therefore exclude every competing residual label. Infeasible restrictions have value infinity. A strict gap greater than \(2G\operatorname{width}_\infty D\) proves that this same label is the unique conditional winner throughout \(D\), including all its boundary points.

Full point growth plus the unit distance between different integer labels forces this certificate at the saved base-only cutoff. There is no supplied label-gap promise and no need for a separate reduced-cost or active-gradient failure event. After the label certificate, the slice with that label over the entire original continuous core box contains a global optimizer. It is a subset of the original feasible domain, so its exact minimum is the original global minimum. Solving the whole slice is valid even if its optimizer set is tied, singular, or positive dimensional. Global lexicographic selection is not promised; a deterministic candidate order suffices.

The fallback enumerates feasible native labels and solves each small core exactly. It retains only the winning label's algebraic representation. Pairwise univariate value comparisons avoid forming the compositum of all labels. Returning or refining the winning representation does not inherit the number of fallback labels or their pairwise separation. If temporary comparisons produced unnecessarily fine isolating intervals, re-isolate the selected root in its own polynomial before output.

The growth-tail scalar-section formula has two quantified point blocks. Expanding native integer membership has exponentially many atoms but only polynomial logarithmic format length. Its fixed-block section bound is \(2^{\operatorname{poly}_d(I)}\), not doubly exponential in the binary native widths. This expansion is analysis only; ordinary search does not materialize it. Coordinate widths enter the continuous-noise growth bound and the cutoff, but their logarithms are polynomial in the input.

The optional implicit variant gives a sharper ordinary processing bound through original core-bound signs and a local Hessian test. It adds a core active-gradient failure event. It is a valid alternative output contract, rather than a prerequisite for the expanded-output theorem. Its current prose still calls the replaced algebraic factor \(A_d(k)\); use \(c_d^k\) in the manuscript. The older native review's claim that output does not use one common primitive root is superseded by the current solver and scoped transfer review. Its old Renegar parameter factor does not justify the current constant-base claim by itself.

**5. Flow and TU optimal-face certificates.**

For separable convex integer flow costs at a rational core, current unit residual marginals and node potentials with nonnegative reduced costs give a compact global optimality certificate. An alternative flow's signed difference is a nonnegative integral residual circulation. Discrete convexity bounds its actual cost change below by the sum of the displayed unit marginal costs, and potentials cancel. Negative-cycle absence is also necessary. This is a certificate; repeatedly augmenting one unit is not asserted to be a polynomial-time algorithm.

The exact conditional algorithm is the established separable-convex integer TU oracle. The paper must cite its exact scaling/LP result, count the fixed-degree rational evaluation costs, require an optimal extreme-point LP solution where the source requires one, and use convex tangent extensions beyond native endpoints if its internal evaluation grids leave those intervals. Tightening coordinate bounds preserves the class. Numerical capacities enter through binary lengths and logarithmic scaling; they are not enumerated in ordinary oracle calls. Conditional convexity throughout the native real interval is a valid supplied premise or needs a checkable certificate.

Under core-only noise, persistent integer ties can make full point growth vanish. A certificate for a single flow on a full retained core hull cannot handle general boundary optima. The two-parallel-arc example has constant projected growth but distinct flows winning in different inward directions on every origin box, on a noise event of probability \(1/16\). More noise bits do not reduce that event. This defeats that certificate plus rare label-enumeration fallback, not core-only smoothing itself.

For an interior core optimum, polynomial residual potentials suffice. Shortest paths from an added zero-cost source admit a tight arborescence even with zero-cost cycles; choose that tree by graph search in the tight-edge graph rather than cyclic predecessor pointers. The tree's symbolic marginal sums give base-only polynomial potentials. Exact non-strict sign tests accept identities and persistent ties. Analysis uses a finite family over every label and every possible tree. A connected hull avoiding all nonidentity chart zeros has constant signs. The exceptional gradient image must include cross-label pairs: the chart's defining label and the attaining fixed-flow slice at the global core need not agree.

The arbitrary-boundary theorem uses all conditional optimal flows. Potentials at a face point \(c\) make each scalar adjusted cost minimal on an integer interval \(I_a\). The tightened feasible set \(Y_0\) is exactly the full conditional optimum set at \(c\); potential sums are constant over feasible flows, so equality in the sum of nonnegative scalar gaps holds precisely on these intervals. Binary search of monotone differences finds their endpoints without enumerating capacities.

Inward derivative minimization over \(Y_0\) is another exact convex flow problem. On a singleton interval substitute the value. On two consecutive integer values use their affine interpolation. On an interval with at least three integers, convexity and equality at three minimizing adjusted costs imply affinity of the original scalar cost at \(c\) across the entire interval. Differentiating its zero scalar second derivative in a feasible inward core direction gives a nonnegative second derivative of the inward derivative cost. The two-point interpolation is essential: a derivative may otherwise be concave between those tied integers.

For every feasible label \(z\), there is \(\bar z\in Y_0\) with

\[
\|z-\bar z\|_1\le r\sum_a\operatorname{dist}(z_a,I_a).
\]

Choose a nearest \(\bar z\), conformally decompose \(z-\bar z\) into simple cycles, and charge each cycle multiplicity to an interval-blocking arc. If a cycle had no such arc, its unit change toward \(z\) would remain in \(Y_0\) and reduce the chosen distance. Conformality bounds the total charge to an arc by its interval violation, and each cycle uses at most \(r\) arcs. This proves the factor \(r\), including parallel arcs and self-loops.

Uniform within-interval identities require at most \(d+1\) distinct integer representatives per arc, or all if there are fewer. Polynomial tree potentials have core degree at most \(d-1\), since a native unit difference reduces total degree by one. Consequently the adjusted scalar cost has total degree at most \(d\), so those representatives suffice. Substitute singleton tangential coordinates before testing the identities. Only original residual arcs need uniform tests; artificial source-arc inequalities are unnecessary for flow optimality.

The first outside adjusted marginals yield a lower gap \(\mu\sum_a\operatorname{dist}(z_a,I_a)\). Combined with the proximity bound, mixed derivative bound \(K\), and core Hessian bound \(H\), the saved tests

\[
\mu\ge rKT_1,
\qquad \beta-HR-(H/2)T_\infty>0
\]

make every off-face point worse than its feasible face projection. Here \(\beta\) minimizes each inward derivative over all flows in \(Y_0\), not the flow initially returned. Both clauses are essential: a losing flow can become optimal off the face unless its outside-cost penalty is controlled. A passing certificate fixes that core face for every global optimizer in the retained hull and supplies one fixed flow whose whole-core slice attains the global optimum. Trying all \(3^k\) original faces eliminates any need to guess the true face.

For TU equalities, replace shortest paths by the compact adjacent-slope dual system. The piecewise-linear integer interpolant has the same optimum over the real TU polytope because each integer-cell intersection is integral. LP duality supplies a multiplier satisfying the one-sided slope inequalities at the integral optimum. After dropping consistent dependent rows and fixed columns, the dual has no lines. TU minors bound every dual vertex by \(mV\); an added pre-draw box of radius \(mV+1\) allows a polynomial-bit vertex computation. Extract an independent active basis from the original boxed inequalities, not artificial lexicographic minimization equalities. Its inverse has entries \(0,\pm1\), so retaining that basis symbolically gives base-height charts. Artificial multiplier-box inequalities need not hold uniformly afterward; the original adjusted marginals provide the certificate.

TU unit circuits replace cycles in the proximity proof. Minimal-support kernel vectors in an orthant are circuits; TU makes their primitive nonzero entries \(\pm1\). Subtract maximal integral multiples conformally and charge interval-blocking coordinates exactly as above. The same factor \(r\) and derivative argument follow. This extension relies on TU; neither the compact dual nor the unit-circuit proof applies to arbitrary integer matrices.

Bounded TU inequalities reduce by explicit finite slacks: \(s_i=b_i-C_i z\), with \(0\le s_i\le b_i-\min_{[\ell,u]}C_i z\). The matrix \([C\ I]\) is TU. Projection is a bijection, zero slack costs preserve core curvature, and all new bounds have polynomial bit length. Introducing unbounded slacks would fail the finite-domain proof. A negative displayed slack upper bound proves infeasibility, but nonnegative bounds do not by themselves prove feasibility; the original exact oracle still detects it.

See [interior flow](../../../research-20261002/new-direction/smoothed-interior-core-flow.md), [flow face certificate](../../../research-20261002/new-direction/flow-optimal-face-certificate.md), [arbitrary core faces](../../../research-20261002/new-direction/smoothed-boundary-core-flow.md), [bilinear flow](../../../research-20261002/new-direction/smoothed-bilinear-core-flow.md), and [TU recourse](../../../research-20261002/new-direction/smoothed-core-tu-recourse.md).

**6. Precision and output contracts that must remain separate.**

| Family | Sampling precision before the draw | Expected initial work | Output caveat |
| --- | --- | --- | --- |
| Continuous quadratic exact recourse | \(\log M=\operatorname{poly}(I)\) | \(8^kQ_{\rm exact}\operatorname{poly}(I)\) | Rational optimizer and value on every draw |
| Continuous polynomial approximate recourse | \(\log M=\operatorname{poly}_d(I)\) | \(8^kQ_{\rm approx}\operatorname{poly}_d(I)\) | Ordinary compact patch; rare large algebraic fallback |
| Core-only uniformly strong continuous recourse, including changing faces | \(\log M=\operatorname{poly}_d(I)\) | \(8^kQ_{\rm approx}\operatorname{poly}_d(I)\) | Same implicit/exceptional distinction |
| Native integer exact recourse with all-coordinate noise | \(\log M=\operatorname{poly}_d(I)\) | \([8^kQ_{\rm exact}+c_d^k]\operatorname{poly}_d(I)\) | Winning label's shared-root core output has \(c_d^k\operatorname{poly}_d(I)\) size on every draw |
| Interior core-only flow | \(\log M=\operatorname{poly}_d(I)\) | \([8^kQ_{\rm exact}+c_d^k]\operatorname{poly}_d(I)\) | Persistent flow ties permitted; verified all-noise interiority premise |
| Arbitrary-boundary nonlinear core-only flow/TU | \(\log M\le f_d(k)\operatorname{poly}_d(I)\) | \(f_d(k)Q_{\rm exact}\operatorname{poly}_d(I)\) | Output/refinement have \(f_d(k)\) bounds |
| Bilinear core-only flow/TU | \(\log M=\operatorname{poly}_d(I)\) | \([8^kQ_{\rm exact}+c_d^k]\operatorname{poly}_d(I)\) | \(L\) is curvature of the core polynomial; coupling enters input bits and precision |

In every case the polynomial exponent is independent of \(k\). One fixed law is chosen from base data and used on every draw, including ties and degeneracy; no rejection or resampling is allowed. Compute the fallback budget before the good-event thresholds, the level cutoff before \(M\), and then \(M\). The fallback's remaining dependence on sampling and requested precision bits must be a polynomial of fixed exponent. This order removes the circular reconstruction risk.

The arbitrary-boundary nonlinear flow/TU distinction is substantive. An algebraic tube controls distance from a chart zero set, not the positive value of a chart away from that set. The scalar threshold formula for the minimum squared value away from zeros has two quantified blocks in at most \(k\) variables each. Elimination bounds the coefficient **bit lengths** of its endpoint polynomial by \(E_d(k)\operatorname{poly}_d(I+\operatorname{bits}\delta)\), where \(E_d(k)=(k+1)^{O_d(k^2)}\). A reciprocal Cauchy bound then gives a rational positive value margin with that many bits. Empty zero sets, nonzero constants, empty away-from-zero sets, and vertex faces require their stated separate cases. The strict scalar threshold describes the open ray above the squared minimum; its boundary is still an algebraic root.

For bilinear coupling, every chart is affine. If its zero set in the cube is nonempty, moving toward a minimizing or maximizing vertex gives \( |p(x)|\ge b_{\min}\operatorname{dist}(x,Z)\), with \(b_{\min}\ge2^{-H_0}\). If no zero occurs, the minimum absolute vertex value is at least \(2^{-(k+1)H_0}\). This restores polynomial-bit margins and sampling length. The multivariate gradient-image elimination remains an analysis-only \(E_d(k)\) format bound; the faster constant-base optimizer does not shrink that image format.

For the normal-margin event, choose the canonical restricted-face core minimizer using only the free noises. Normal noises add constants on that face, so the minimizing core and its whole optimal-flow set are independent of any tested normal coefficient. The minimum inward derivative is \(b+s_i\gamma_i\). A union over fixed faces and normal coordinates gives the saved finite-grid interval bound without conditioning on the random winning label.

**7. Joint critical-limit solver and strong-field composition.**

I directly checked [the polynomial component solver](../../../research-20261002/new-direction/polynomial-component-primitive-limit.md), [strong-field polynomial composition](../../../research-20261002/new-direction/strong-field-component-polynomial.md), [its arithmetic-budget review](../../../research-20261002/reviews/strong-field-polynomial-budget-review.md), and [strong-field QP](../../../research-20261002/new-direction/strong-field-component-qp.md). The current constant-base proof is materially stronger than the older coordinate-by-coordinate fallback and can support the recourse completion claims.

On a continuous face of free dimension \(r\), choose even \(D>d\), put \(a=D-1\), and deform by \(\varepsilon\sum_i x_i^D\). After \(z=1/\varepsilon\), the monic stationary equations have leading monomials \(x_i^a\). Their coprime leading monomials give a Gröbner basis after every finite specialization. The quotient dimension is \(N=a^r\), including nonradical ideals. Memoizing monomial normal forms of total degree at most \(r(a-1)+1\) controls the number of table entries by a constant-base exponential, rather than the number of reduction paths by an input-size power depending on \(r\). Reduction degree decreases, coefficient path lengths are \(O_d(r)\), and heights are polynomial in the input bits and \(r\).

Multiplication matrices yield characteristic polynomials of linear forms and their independent coefficient derivatives. Enumerating moment-curve forms avoids all pole-hiding directions and separates all distinct finite vector limits: each forbidden condition is a nonzero polynomial in the integer form parameter of degree at most \(r-1\), and the number of conditions is at most \(N+\binom N2\). At least one of the \(1+(r-1)(N+\binom N2)\) forms is good. Algebraic Puiseux branches and local multiplicities supply the finite-limit factorization; no expansions are computed online.

For a good form, the leading \(z\)-coefficient of the characteristic polynomial is \(C(\lambda)\prod_v(T-\lambda^Tv)^{\mu_v}\). The leading \(z\)-degree is locally constant in the independent form coefficients. Differentiation therefore commutes with extracting that coefficient. Dividing both the coefficient derivative and \(p'\) by \(\gcd(p,p')\), and inverting the resulting derivative modulo the squarefree part, gives coordinate maps at every finite projected root. Multiple branches with the same finite vector limit are handled by their nonzero characteristic-zero multiplicities.

The degree and divisibility rejection tests are necessary for bad forms. A bad form that nevertheless produces a reconstructed feasible tuple is harmless: no feasible point can have value below the true global minimum. Compact minimizers of the deformed objectives have a subsequence on one original face and one bounded stationary branch, so at least one original global minimizer appears among the reconstructed limits or vertices. Selecting the least original value is therefore correct for singular and positive-dimensional original stationary sets.

Only three interpolation variables are used for determinants: the deformation variable, the scalar characteristic variable, and one coefficient-direction variable. No dense polynomial in \(r\) independent form variables is constructed. Quotient matrices, forms, interpolation, gcds, signs, root isolation, and pairwise value comparisons are polynomial in \(N\), coefficient height, and requested bits, with absolute exponents. Summing over \(3^k\) faces gives \(c_d^k\operatorname{poly}_d(H+q)\). The explicit conservative \(c_d=2^{10000D}\) budget is consistent with the saved query ledger and effective elementary routines. The manuscript may use an effective fixed \(c_d\) and provide this loose implementation ledger in an appendix; it must not infer a predetermined base from an unspecified claim of polynomial time.

Every coordinate of a selected candidate is a rational polynomial map of the same isolated real root \(\alpha\). Thus

\[
[\mathbb Q(x_1,\ldots,x_r,f(x)):\mathbb Q]\le\deg P\le(D-1)^r.
\]

The displayed \(P\) need not be irreducible or minimal. Separate nonzero defining polynomials for each coordinate and the value follow from resultants and have degree at most \(N\); matching uses the same selected root and cannot mix optimizers. Their coefficient heights and isolating endpoint lengths are bounded by \(c_d^k\operatorname{poly}_d(H+q)\). Minimal defining polynomials exist with the same type of degree/height bound by univariate factor bounds, but computing or returning minimal polynomials is unnecessary and is not the stated contract.

Within a component, different candidate values can be compared by squarefree isolation of the product of two value polynomials, or gcd methods. Equal values have the same root identifier, so ties do not cause indefinite interval refinement. This is not a sign algorithm for arbitrary sums of unrelated algebraic numbers.

The strong-field probability argument is sound. Before sampling, derivative intervals enclose each original coordinate derivative throughout the continuous hull. Outside the corresponding closed bad interval, strict monotonicity pins that coordinate at its original bound for every global optimizer, including native integer coordinates. Equalities remain bad. Each bad event depends only on its own original noise coefficient, so the Bernoulli sites are independent. Recomputing the intervals adaptively would lose this independence and is not needed.

After pinning, every surviving monomial is contained in one connected component of the induced primal graph. A displayed monomial support must induce a clique; a factor-incidence graph would not give this conclusion. For a component, the work weight is the product of \(c_d\) over its continuous vertices and native label counts over its integer vertices. The elementary connected-set count gives

\[
\mathbb E\sum_C A(C)\le
\frac{\sum_i a_iq_i}{1-4\Delta_+\max_i(a_iq_i)}
\]

when the denominator is positive. Exact probabilities can be computed by rational grid-index counting. The sufficient strong-noise regime pays for derivative variation, graph degree, and native label counts; those numerical quantities have not disappeared. A huge integer interval requires correspondingly stronger noise for this argument, unlike the polynomial-bit convex-flow recourse oracle. Correctness remains valid when the subcritical condition fails, but that calculation then gives no expected polynomial bound.

The exact global output retains one shared-root representation per independent component, rational pinned coordinates, and a sum of component value expressions. It has an expected construction/output bound, not a polynomial size bound on every draw. A global primitive element or expanded minimal polynomial of the sum may have degree exponential in the number of small components. Such an expansion, or a general exact sign/equality test for unrelated algebraic sums, must not be promised. Rational value enclosures and feasible points with a prescribed total objective gap are obtained by assigning each component \(1/n\) of the requested error, adding only \(O(\log n)\) precision bits.

QP component enumeration is complete on every atom: at a continuous minimizer on a smallest free face, a singular PSD free Hessian would give a flat direction reaching a smaller face. Hence either the free block is nonsingular or the point is a vertex. Feasible stationary saddles among the extra candidates are harmless. All candidates and the final QP optimizer/value have polynomial rational bit length on every draw.

**8. Native low-rank integer theorem, rank separation, and limitations.**

The [low-rank integer theorem](../../../research-20261002/new-direction/smoothed-integer-low-rank.md) is a separate exact recovery mechanism. Its domain is a product of native integer intervals, its convex part is separable univariate quartics, and its noise is \(T^Td\), generally correlated in the original coordinates and supported on the supplied row subspace. It does not use independent noise in every original coordinate or the flow/TU oracle.

The auxiliary square-completion identities and witness gap transfer are correct. Exact discrete recourse uses monotone forward differences and binary search; its cost is logarithmic in native interval width. At the prescribed final level, the feasible original objective gap is smaller than the original value lattice spacing \(1/[D_0(M-1)]\). One common \(M\) is essential. Auxiliary values and the square-completion shift can have \((M-1)^2\) denominators, but their lattice is never used. The original feasible value lattice has only one sampling-denominator factor, allowing the same base-computed \(M\) to control finite-grid atoms and exact termination. All ties are allowed and there is no growth event or rare fallback.

The mesh inequality used for the neighbor count applies to interior grid coordinates, which necessarily have more than one subdivision. An unrefined narrow coordinate has only its endpoints and contributes no interior comparison. State this condition if reproducing that calculation. The numerical row-range/noise factors remain explicit. Binary bounds alone do not imply polynomial work. Coupled integer constraints and continuous quartic coordinates are outside this exact lattice theorem. Fixed-rank binary and explicitly listed-label zonotope/Minkowski baselines must be credited rather than presented as new consequences.

The [rank-separation family](../../../research-20261002/new-direction/polynomial-recourse-rank-separation.md) has degree five, one core coordinate, and dense convex quartic recourse. At the core boundary \(t=0\), residual Hessian is zero while the core/residual cross block spans the residual space as \(z\) varies. A fixed PSD quadratic correction \(K\) that makes the full objective convex must therefore have positive definite residual block \(K_{zz}\), so \(\operatorname{rank}K\ge m\). The kernel argument is correct, using continuity from the interior and the spanning vectors \(\nabla P(e_i)=4(e_i+\mathbf1)\). It excludes fixed small-rank PSD quadratic correction, not every difference-of-convex representation, and supplies no hardness result. A one-coordinate entropy correction with singular boundary derivative can convexify this family at a scale depending on the coupling. Preserve that caveat. This separation must not be attributed to the uniformly strong-residual class, which has a rank-\(k\) quadratic convexifier.

The [local-error interface](../../../research-20261002/new-direction/local-error-recourse-interface.md) is a valid warning and sufficient conditional principle, not a general sparse message-passing algorithm. A bag-local interpolation budget cannot replace the global discretization error of grid min-marginals. Outside error changes with the bag state and does not cancel under normalization. The saved nonconvex star and uniformly positive-definite star demonstrate this at treewidth one. The latter is a deterministic coherent-grid example, not a smoothed runtime lower bound, and ordinary global convex optimization already solves it. Exact or globally certified conditional recourse can remove that outside error; current grid messages do not meet the required interface.

**9. Existing-paper overlap and source classification.**

The existing [exact-arithmetic recourse section](../../../paper-exact-arithmetic/sections/10-recourse.tex) already supplies core-only-noise Cauchy names for values and one selected core under residual convexity on a product box, and under a supplied convexifier on coupled polytopes. It also gives full selected-point evaluators with extra convexifier or cubic structure, and explains why approximate-core substitution can select the wrong residual limit. Its selectors are lexicographically least core followed by least residual norm. The new exact global-completion results generally return a deterministic optimizer without that canonical selector. Do not silently inherit the old selector promise.

The old paper's value/core theorem tolerates arbitrary flat residual fibers; the new continuous core-only full-Hessian closure requires uniform strong residual convexity. The new all-coordinate polynomial theorem can use only residual PSD because residual perturbations provide the full growth/active-gradient event. These are compatible but materially different contracts. Reuse the conditional value, convex evaluation, fixed-law transfer, and same-draw fallback foundations self-containedly. Avoid presenting those established internal foundations as newly proved capabilities of the new submission.

The source statuses for manuscript planning are:

| Source group | Treatment |
| --- | --- |
| Exact box recourse and polynomial approximate box recourse | Complete under the stated restricted-oracle contracts |
| Core-only strong interior recourse | Complete restricted antecedent; explanatory special case of changing-face theorem |
| Core-only changing faces, active-stratum tube, small-multiplier lemma | Complete composition and supporting lemmas; strong residual modulus remains essential |
| Native integer recourse | Complete with current common-root solver and constant-base transfer; older review's algebraic scope partly superseded |
| Native implicit closure | Complete alternative output contract; replace stale \(A_d(k)\) notation |
| Interior core-only flow | Complete under all-noise interiority; sharper literal bound remains useful |
| Flow optimal-face certificate and arbitrary-boundary flow/TU | Complete deterministic and probabilistic chain; charge parameter-dependent precision |
| Bilinear flow/TU | Complete sharper corollaries with affine margins |
| Joint critical-limit solver and polynomial strong fields | Complete current algebraic dependency and composition |
| QP strong fields | Complete rational specialization; closing prose saying no polynomial extension is asserted is historical and superseded by its separate successor |
| Low-rank native integer product boxes | Complete exact lattice theorem under its different perturbation law |
| Local-error conditional interface | Complete counterexamples and sufficient interface; incomplete as a general sparse solver |
| Rank-separation and rotating-fiber notes | Complete structural/certificate limitations; no computational hardness claims |
| Single-flow boundary obstruction | Complete strategy-specific obstruction; resolved by the later optimal-face certificate, not invalidated by it |
| Approximate convex recourse | Complete growth-conditional approximation antecedent; not by itself a new unconditional smoothed exact mixed-domain theorem |
| Earlier separate-coordinate fallback | Sufficient for loose rare-event fallback; superseded for constant-base component work |

**10. Dependencies and authoring requirements.**

The manuscript needs self-contained proofs of the sparse corrected-core search, both restricted-region certificates, global containment before local closure, the flow/TU optimal-face certificate, the weak-multiplier release argument, and the joint critical-limit construction. The tail/fallback/convex-evaluation foundations can be stated once and reused with explicit predicates and bit-format checks. The flow/TU and strong-field branches must refer to their actual exact oracle and component-work interfaces at every restriction; they must not appeal to an unnamed optimizer.

Primary references still need the literature workflow's confirmation and accurate locators for rational convex weak optimization and exact QP, the exact forest QP oracle, the separable-convex TU scaling oracle, fixed-block elimination with separate height dependence, the singular-algebraic tube theorem, algebraic Puiseux branches and quotient multiplicities, and exact univariate isolation/sign/refinement algorithms. TU circuit and flow charging arguments are self-contained here, but classical attribution is appropriate. I did no literature searches or ingestion.

The paper should separate \(c_d^k\) computational component cost from \(E_d(k)\) analysis-only elimination format and from a base-only fallback factor \(B\). It should separate ordinary descriptor size, every-draw algebraic output size where established, expected proof-trace size, initial construction, and later \(q\)-bit evaluation. It should name the actual perturbed objective and avoid claiming exact recovery of the unperturbed optimum. Existing finite diagnostics support particular mechanisms only; they do not implement general GLS, H&S flow/TU scaling, general algebraic sign testing, or full finite-law experiments. No new performance claims follow from this audit.

**Verification performed in this audit.** Source reads and analytical derivations above are the mathematical verification. No saved experiment was rerun. An inline report-only Python check passed local links, paired math delimiters and fences, trailing whitespace, and absence of escaped control characters. The same check was saved and run as python3 -B paper-smoothed-global/verification/recourse/check_prewrite_report.py: it passed 20 local links, 174 inline math pairs, and nine display pairs. No project-wide verification, CI inspection, source-note edits, commits, or delegation were performed.
