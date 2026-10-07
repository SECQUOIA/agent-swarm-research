# Early Sol interface review of the integer section

Date: 2026-10-05. Scope: sections/08-integer.tex and its current integration interfaces. This is an early targeted review, not the full manuscript review. Appendix F was absent when the checks below were made; the available appendices were A, C, E, and G. The inspected live section had SHA-256 7e460d708db99cdaf10278727ccc0ea8db1048c3423364f976392cf814aeff89 at the hash check. Authors may revise the live file afterward, so the theorem labels and quoted claims below are the stable issue anchors.

**Decision.** The section is not yet ready for publication. Its main structural interfaces match the audited source development, but several present claims need correction, and Appendix F is still required to verify the deterministic solver, effective budgets, finite-law cutoffs, and flow/TU compositions in the manuscript itself. I found no defect that defeats the subject. Missing Appendix F is a pending proof dependency, rather than evidence that the intended theorems are false.

I read BRIEF.md, independent-review-brief.md, integration-contract.md, integration-decisions.md, the earlier prewrite-recourse-sol.md audit, the fallback-shared-root-sol.md development, and the actual integer section. I also checked the current core–recourse definition used by the native theorem. The source audit is background for this report; it does not substitute for an unwritten manuscript proof.

**1. Present corrections.**

**I1 — Major output mismatch; already recorded by the root.** At sections/08-integer.tex:69–74, theorem thm:int:solver claims the model's algebraic format but gives the value only through its own defining polynomial and isolator. The model requires the coordinates and value as rational polynomial maps of the same isolated root. This mismatch propagates to the native, flow/TU, and component theorems when they invoke the solver.

Repair: form the explicit rational composition

\[
V(T)=f(r_1(T),\ldots,r_k(T))\pmod P
\]

after substituting fixed coordinates, and return \(V(\theta)\) as the value map. Its degree can be reduced below \(\deg P\), and fixed input degree makes the coefficient height and construction cost polynomial in the existing univariate degree/height bounds. Keep the separate value polynomial and matched isolator as auxiliary data for comparisons. A resultant alone without the common-root value map does not meet the displayed format. This is the integration-contract correction, not a newly discovered obstruction.

The general fallback conversion has a different role: it can convert canonical scalar isolators within \(2^{\operatorname{poly}_d(I)}\) work, but Cartesian degree products cannot justify this solver's \(c_d^k\) bound. Appendix F must retain the joint critical-limit construction.

**I2 — False specialization statement; already recorded by the root.** At sections/08-integer.tex:83–87, the stationary equations are said to have the pure-power leading monomials “for every value of \(\varepsilon\).” This fails at \(\varepsilon=0\), where the deformation term disappears and the original stationary set can be positive dimensional.

Repair: say “over the symbolic parameter field, and after every nonzero specialization of \(\varepsilon\)” or write the normalized equations in \(z=1/\varepsilon\). The limit \(\varepsilon\to0\) belongs to the branch analysis, not to the constant-dimension specialization claim.

**I3 — False unqualified projection statement.** At sections/08-integer.tex:88–94, the leading characteristic coefficient is said to vanish exactly at projections of finite critical limits. This is true for a projection that exposes every escaping branch and separates finite vector limits, not for an arbitrary form in the deterministic list.

A direct counterexample needs no experiment. Take \(f(x,y)=y\), degree \(d=1\), and \(D=2\). The deformed full-face stationary equations are

\[
2\varepsilon x=0,\qquad 1+2\varepsilon y=0.
\]

The only branch is \((x,y)=(0,-1/(2\varepsilon))\), which has no finite vector limit. For \(\lambda=(1,0)\), the characteristic polynomial is \(T\), whose leading coefficient in \(1/\varepsilon\) has the root zero. Thus the asserted exact zero-set description fails for this form. Its derivative in the independent \(y\)-coefficient has higher \(z\)-degree than the characteristic polynomial, so the source construction correctly rejects it.

Repair: qualify the finite-limit factorization by a good form; state the higher-\(z\)-degree and gcd-divisibility rejection tests before allowing a bad form to contribute reconstructed feasible points. The scalar \(\gcd(p,p')\) reduction is needed for nonradical quotients and repeated finite limits. The sentence that “the others can only add feasible candidates” needs the feasibility filter explicitly: the algebraic extraction of a bad form can fail and must not be treated as automatically valid. Replace unqualified convergence of all deformed minimizers by the compactness statement that a convergent subsequence has an original global minimizer as its limit. These repairs preserve the theorem and its stated algorithm.

**I4 — False affine margin statement when the zero set is empty.** At sections/08-integer.tex:411–413, the displayed inequality

\[
|p(x)|\ge b_{\min}\operatorname{dist}
            (x,Z(p)\cap[0,1]^q)
\]

is stated without the nonempty-zero-set condition. For \(p\equiv1\), the zero set is empty, its distance is \(+\infty\), and the inequality is false. Nonconstant examples such as \(p(x)=1+x\) have the same problem.

Repair: give two cases. If the zero set in the cube is nonempty, the path toward a suitable vertex proves the distance inequality with \(b_{\min}\) the minimum absolute nonzero linear coefficient. If it is empty, the strict-sign affine polynomial has minimum absolute value at a vertex. With at most \(q+1\) rational coefficients of height \(H_0\), a common denominator bounds this positive vertex value below by \(2^{-(q+1)H_0}\). Handle nonzero constants and vertex faces in this second case. Identically zero charts are discarded from the exceptional zero-set family and pass non-strict certificate tests. These separate cases are required to justify polynomial precision for bilinear flow and TU recourse.

**I5 — Underspecified transfer to TU systems.** At sections/08-integer.tex:420–427, theorem thm:int:tu supplies TU and scalar convexity but does not expressly carry over the flow model's explicit rational fixed-degree input, unit core box, supplied core upper-curvature \(L>0\), noise width, fixed residual feasibility, or counted certificate lengths. Those premises are necessary for both its output and its \(Q_{\rm ex}\) bound. The theorem refers to the flow conclusion, not explicitly to its complete input hypotheses.

Repair: begin with “Use the same core, polynomial, curvature, and encoding premises as in the flow model, and replace its residual network set by ...” or state the premises directly. The bounded-inequality corollary should inherit them. This is an interface clarification in the intended global polynomial model, not a counterexample to the intended TU result. Total unimodularity alone does not provide the claimed interface for arbitrary nonlinear convex objectives or succinct objective encodings.

**I6 — Marginal-potential bit claim needs its rational encoding premise.** At sections/08-integer.tex:222–231, lemma lem:int:potentials quantifies over convex scalar functions and then promises shortest-path potentials “of polynomial bit length.” The characterization by real potentials is valid for real convex costs, but the bit conclusion requires polynomial-length rational current marginal costs. That condition holds in the actual fixed-degree rational applications; it is not a consequence of convexity alone.

Repair: state that the bit claim applies when the residual marginal costs are rational and have polynomial encoding length, as in the preceding polynomial model. Shortest-path paths then sum at most \(s\) marginal values, with rational polynomial length. The lemma is an optimality certificate, not a polynomial bound for repeated unit augmentation; the following paragraph correctly preserves that distinction.

**I7 — Evaluation language needs alignment with the model.** At sections/08-integer.tex:483–484, theorem thm:int:strong-field calls a feasible point with objective gap \(2^{-q}\) a \(q\)-bit evaluation. The model defines \(q\)-bit point evaluation using Euclidean distance to the represented optimizer as well as a value enclosure. Objective gap alone gives no point-distance conclusion for a flat or singular component.

Repair: either call this “certified objective-gap evaluation,” or also promise distance \(2^{-q}\) to the stored optimizer. The stronger version is available through the algebraic component maps: ask each of at most \(n\) components for point error \(2^{-q}/(n+1)\), clip continuous approximations to its box, retain integer labels, and separately assign each component gap/value width \(2^{-q}/n\). Combining the components adds only \(O(\log(n+1))\) precision bits and gives the same expected work form. Do not infer distance from the gap without this algebraic refinement step.

The interior-flow theorem at sections/08-integer.tex:286–298 also omits an explicit refinement bound, though its intended shared-root solver gives \(c_d^k\operatorname{poly}_d(I+q)\). Add that statement if, as the brief requires, the theorem is to state its later evaluation contract.

**I8 — Small edge and integration cases.** The low-rank setup at sections/08-integer.tex:533–537 does not exclude \(k=0\), but then \(s=\max_iw_i\) is undefined. State \(k\ge1\) after handling \(k=0\) by direct separable integer optimization. The strong-field definitions similarly need the all-fixed-coordinate case before taking \(\beta=\max_i a_iq_i\); direct constant evaluation or the convention \(\beta=0\) suffices.

For the label certificate at sections/08-integer.tex:158–164, explicitly assign \(+\infty\) to impossible coordinate restrictions and to the minimum of an empty restriction list. A restriction beyond an original bound can be recognized as empty before invoking the oracle, whose defined input requires ordered tightened bounds. This makes singleton residual sets and empty residual coordinate lists unambiguous.

The sentence at sections/08-integer.tex:454 that previous results “need small noise” overstates their assumptions. They allow arbitrary positive \(\sigma\) and expose a numerical curvature/noise dependence; the strong-field result adds a lower bound on noise. Write that distinction directly.

The low-rank theorem still covers quartic polynomial unaries only. That is a valid restricted theorem. The fixed-degree piecewise-polynomial extension requested in the integration contract is still pending integration, rather than a false statement in the current theorem.

**2. Interfaces that agree with the intended contracts.**

The following checks can be made from the actual section and its present definitions, without treating Appendix F as written.

The native oracle at definition def:int:native requires exact optimal values and attaining integral labels on arbitrary tightened integer coordinate bounds, including infeasibility, with an input-polynomial exponent independent of \(k\). The residual set is fixed independently of the core. Its queried values are rational because the core is rational and residual labels are integral. This is the right exact interface; it is stronger than one unrestricted conditional solve.

The coordinate restriction union in the native certificate is exactly \(Y\setminus\{z_j\}\), even with coupled residual constraints. A uniform core Lipschitz bound and the strict threshold \(2G w_\infty(\mathcal H_j)\) then exclude every competing label throughout the hull. Optimizing the selected label over the entire original core box is sound because that feasible slice contains a global optimizer. Neither convexity nor uniqueness of the selected slice is required for this deterministic step. Returning only the winning label's root representation also correctly avoids inheriting the fallback enumeration count in the final output.

The H&S oracle proposition correctly limits its concrete scope to separable costs convex on each native real interval, fixed integral TU feasibility, rational fixed-degree evaluation, and tightened bounds. It does not promise an oracle for arbitrary nonseparable integer convex optimization. Its scalar tangent extension addresses evaluations outside native endpoints. The capacity dependence of such a scaling oracle is through binary lengths/logarithmic scaling, rather than ordinary enumeration of labels. Appendix F must still supply the exact LP/extreme-point and bit-evaluation bridge to the cited theorem.

The full optimal-flow interval argument explains why one queried flow and its potentials describe all tied optima at the face point. The deterministic face certificate uses every tied flow's minimum inward derivative and a separate losing-flow marginal penalty. Both clauses appear in the theorem; dropping either would be unsound. Two-point tied intervals use affine derivative interpolation, so the text does not incorrectly infer affinity from equality at only two integers. These are the correct interfaces for the later exact convex-flow derivative calls.

The strong-field setup computes the derivative enclosures before sampling, retains threshold equalities in the bad events, and uses the original primal graph with each monomial support a clique. These choices make bad-site independence and exact component separation valid. Its component format preserves one shared root within each component and explicitly declines general exact comparisons of sums of unrelated algebraic component values. That limitation is correct and must survive integration.

The low-rank lattice setup uses one common \(M\) for all aligned marginal laws. It distinguishes the original objective lattice, whose denominator is linear in \(M-1\), from auxiliary values and the square-completion shift, which can have \((M-1)^2\) denominators. It does not rely on uniqueness or a growth event and correctly promises no fallback. Numerical row-range/noise ratios remain explicit, so binary interval encoding alone is not claimed to give polynomial work.

**3. Precision regimes: correctly distinguished in the present statements, proofs still pending.**

| Theorem group | Current sampling statement | Interface assessment |
| --- | --- | --- |
| Ambient native recourse and interior core-only flow | \(b=\operatorname{poly}_d(I)\) | Correct intended scope; core-only interiority is an all-noise premise used for the expected-work argument |
| General nonlinear boundary flow/TU | \(b\le f_d(k)\operatorname{poly}_d(I)\) | Correctly charges the nonlinear chart value-margin precision |
| Bilinear boundary flow/TU | \(b=\operatorname{poly}_d(I)\) | Correct sharper scope after the empty-zero-set margin case in I4 is restored |

The summary table and the theorem statements distinguish these regimes. The text correctly says that a geometric tube bound controls distance, while the general polynomial value margin requires a coefficient-height estimate. It also keeps the bilinear core curvature equal to that of \(\phi\); capacity and coupling magnitudes enter through their bit lengths and precision, rather than enlarging \(L\). The example \(v_i^2z_a^2\) correctly explains why nonlinear coupling can enlarge the numerical curvature.

There is no verification yet in Appendix F of these sampling claims. The pending proof must keep a computational constant-base solver budget separate from the analysis-only multivariate elimination format. A fast exact core minimizer does not give a constant-base description of gradient images. The general nonlinear value-margin coefficient *bit length* can be \(f_d(k)\operatorname{poly}_d(I)\), which explains the weaker sampler bound; it must not silently be replaced by \(\operatorname{poly}_d(I)\).

Strong fields and the aligned lattice theorem sit outside this three-group recourse comparison. The strong-field theorem is correct for any specified finite \(M\) as an exact deterministic procedure, and its useful expectation needs the stated weighted subcritical condition; a base-chosen least \(M\) satisfying the sufficient condition has polynomial bit length. The aligned lattice theorem explicitly chooses its polynomial-bit \(M\) from its original objective denominator and the auxiliary widths. Neither route needs a rare-event fallback.

**4. Appendix F obligations not yet verified in manuscript text.**

These are pending proof checks, not failures inferred from an unwritten appendix.

1. For thm:int:solver and lem:int:budget: finite nonzero-parameter quotient completeness; memoized normal forms rather than input-monomial branching; a good moment form that exposes all escaping branches and separates finite limits; rejection tests and multiplicity cancellation; common-root objective composition; candidate feasibility; exact ties; and an effective pre-draw \(c_d\) that bounds construction, comparisons, output, and arbitrary refinement. New coefficient bits must have a polynomial exponent independent of \(k\).
2. For thm:int:native and cor:int:native-implicit: exact hull/incumbent constants, unit integer-label separation, growth-only cutoff for expanded completion, the extra active-gradient event for implicit completion, and label-enumeration fallback \(B\operatorname{poly}_d(I+b+q)\) with base-only \(B\). Re-isolation of the winning label's own roots must give the every-draw output bound without carrying the examined-label count.
3. For prop:int:hs and the derivative oracle calls: the cited source requires an optimal extreme-point LP solution; arbitrary points on an optimal LP face need not be integral. Account for rational fixed-degree evaluation, tangent extensions, integer infeasibility, tightened bounds, and modified two-point/singleton/long-interval derivative costs. Do not replace the exact scaling oracle by repeated unit augmentation.
4. For thm:int:flow-interior: shortest-path tree extraction in the presence of zero-cost cycles, a pre-draw chart family, cross-label gradient images, non-strict identity acceptance, projected rather than full point growth, an explicit algebraic tube coefficient, and the finite-grid atom term.
5. For lem:int:proximity and thm:int:face: conformal cycle charging with factor \(n_R\), the complete Taylor/losing-flow inequality, inward-derivative convexity on long tied intervals, \(d+1\) representative identity tests, original rather than artificial residual-arc inequalities, and original core-face compatibility.
6. For thm:int:flow-boundary and cor:int:bilinear: the canonical restricted-face optimizer's independence of normal noise, minimization over the whole tied-flow set, the three failure events, the two-block value-margin formula, empty zero sets and vertex faces, and pre-draw ordering \(B\), margins, cutoff, then \(M\). Preserve parameter-dependent bits in the nonlinear case and the affine bound in the bilinear case.
7. For thm:int:tu and cor:int:tu-ineq: preprocessing of fixed columns and dependent rows, the compact dual's existence and a bounded exact vertex, extraction of a TU active basis, symbolic chart height independent of sampled query coordinates, conformal unit circuits, and finite slack bounds with their exact projection bijection.
8. For thm:int:strong-field: weighted connected-set counting with the true component-work base, rather than an unweighted site argument; no adaptive derivative recomputation; every-atom component algebra; expected proof/output costs; and coordinated point/value accuracy across independent components. A generic \(2^{\operatorname{poly}(\text{component size})}\) solver would not support the weighted expectation.
9. For thm:int:lowrank: the unequal-width nested mesh, the neighbor-count estimate only for coordinates with interior grid positions, original witness gap transfer, the original lattice denominator, and the shared final choice \(J=\log_2M\). The unit-core search cannot be applied to unequal auxiliary widths without either the stated general mesh or a accounted-for rescaling.

A complete source proof and earlier review support each intended chain, but the submission cannot cite those private records as its essential proof. Publication readiness for these items remains pending the actual Appendix F and its targeted review.

**Verification performed.** I read the actual section and the named evidence/contract files; checked the present theorem definitions, output interfaces, noise and numerical scope; and derived the two counterexamples in I3 and I4 analytically. Commands run were scoped reads and searches using cat, sed, nl, rg, and sha256sum. A report-only inline python3 check passed: 74 paired inline math delimiters, 3 paired display math delimiters, no trailing whitespace, and no control-character escapes. No TeX edit, compilation, literature search, optimization experiment, project-wide verification, CI inspection, or delegation was performed.
