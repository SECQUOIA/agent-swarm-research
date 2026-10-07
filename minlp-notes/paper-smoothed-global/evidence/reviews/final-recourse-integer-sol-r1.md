# Final independent recourse and integer review, integrated mathematical draft R1

The assigned mathematical scope is sound after one local normalization correction. I found no defect that invalidates the continuous recourse, native integer recourse, flow/TU, strong-field, or newly generalized lattice optimizer theorems. The joint critical-limit solver has a complete constructive proof, and the new fixed-degree piecewise-polynomial lattice proof is complete. This is an independent mathematical review of the frozen sources, not approval based on an author report or build.

The frozen text still has one false subsidiary statement: Appendix F claims an integer value resultant before clearing the rational root polynomial's denominator. Finding V1 below gives a counterexample and a repair that preserves all degree, height, work, and output bounds. The root accepted the repair during this review and reports that it is in the live manuscript. I did not inspect or approve that live edit, and the frozen R1 remains unchanged. Publication approval for this scope therefore requires checking that repair and the pending external source identities. No subject-defeating obstruction was found.

**Snapshot and scope.** I used only scientific TeX in evidence/snapshots/integrated-mathematical-draft-r1. I read both assigned sections and both appendices completely, and read the relevant frozen model, local-count, mesh, growth-tail, finite-tail, fallback, shared-root, and uniform-resolution proofs. The scientific comparison paragraphs were checked at their stated mathematical scope; verification of the external companion and literature identities remains with the assigned literature lead.

I read the manuscript brief and independent-review brief, integration contract and decisions, root-integration-to-final-math, the earlier scope and recourse reviews, the Opus editorial disposition and partial mathematical record, and the listed author supplements. Those records identify expected repairs and dependencies; none substitutes for checking the frozen proof.

A scoped Python hash check matched all 20 manifest files and all recorded line counts. The manifest itself has SHA256 c439935acba1b1adeb5d883e3718b1416f71ca45839ab672f5545060343d92cf. Its capture time is 2026-10-06T03:49:31.635993+00:00. The principal audited hashes are:

| Frozen file | SHA256 |
| --- | --- |
| sections/02-model.tex | 0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63 |
| sections/03-counting.tex | 9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049 |
| sections/07-recourse.tex | 6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b |
| sections/08-integer.tex | 27809e4472aa7e53c36e8a211bf91d348f5e25c651d74f75936e9d5df7e3f573 |
| appendices/A-finite-noise.tex | 4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd |
| appendices/E-recourse.tex | e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f |
| appendices/F-integer.tex | c561d9401b3cc15e9072ab7bffe843f6205a894886fba219a8ee02150a472ef0 |

Locations below refer to these frozen files. E and F abbreviate the respective appendices; S7 and S8 abbreviate the two assigned sections. An interval of lines identifies the proof passage, not a claim to have checked the live manuscript.

**V1: minor exact-output normalization defect.** At F:57–61 the algorithm constructs \(P=p/\gcd(p,p')\) over \(\mathbb Q[T]\). F:67 invokes the value comparison lemma before F:68 clears the denominator of the returned \(P\). Nevertheless F:264–265 asserts
\[
\operatorname{Res}_T(P(T),q_0W-h(T))\in\mathbb Z[W].
\]
The resultant can have rational coefficients.

For \(f(y)=y^3-3y\) on \([-3/2,3/2]\), take \(d=3,D=4\). On the full face the normalized equation is
\[
y^3+(3z/4)y^2-3z/4=0.
\]
The one-coordinate characteristic polynomial is \(T^3+(3z/4)T^2-3z/4\), so the leading coefficient is \(p=(3/4)(T^2-1)\). With the usual monic rational gcd, \(G=1\), and \(P=(3/4)(T^2-1)\). The coordinate map is \(r_y=T\), the value map is \(r_f=-2T\), and
\[
\operatorname{Res}_T(P,W+2T)=(3/4)(W^2-4)\notin\mathbb Z[W].
\]
Both finite limits are feasible, and \(y=1\) is the unique box minimizer. Thus this example uses a genuine kept point; it is not an issue confined to rejected projections.

Clear a positive common denominator of \(P\) immediately after forming \(p/G\), before modular maps and the value lemma are used. Its roots and quotient ideal are unchanged, so the maps remain valid; \(A^{-1}\bmod P\) uses the same ideal. Alternatively clear the resultant's positive denominator before root isolation and auxiliary output. Either repair costs polynomial degree/height work. The shared-root value identity, exact order/equality comparisons, and the optimizer proof are unaffected. Only the integer-coefficient assertion is not verified as written. The corrected cubic example above is the counterexample used in this report.

**Earlier repairs are present in R1.** The following findings from the previous frozen review are closed at the indicated actual locations.

| Earlier item | Integrated proof checked |
| --- | --- |
| K1: common-root coordinate and value output | S8:64–90 and F:259–287 return \(r_f=f(r)\bmod P\) at the stored coordinate root; the separate value isolator is auxiliary. V1 concerns its integer normalization only. |
| K2: deformation at zero | S8:92–104 restricts the original deformation statement to symbolic/nonzero epsilon. F:35 and F:75–97 use normalized equations, whose finite \(z=0\) specialization is valid. |
| K3: hidden poles and compatible limits | S8:105–134 and F:137–256 require a good form for recovery, reject unsuitable algebraic data, test every candidate for feasibility, and select a convergent fixed-face subsequence. |
| K4: affine empty zero sets | S8:498–507 and F:866–896 state and prove separate nonempty-zero-set and empty-zero-set bounds. |
| K5: TU input scope | S8:514–530 explicitly requires fixed-degree rational polynomial costs, convexity on each native real interval, fixed nonempty TU feasibility, and the curvature/encoding premises. |
| K6: rational marginal heights | S8:267–280 and F:550–554 state the rational marginal bit-length premise before deriving polynomial-length potentials. |
| K7: point, value, and gap precision | S8:64–90, 370–384, 599–631 and F:316–327, 1000–1015 refine Euclidean point distance, value width, and feasible objective gap separately and use the logarithmic dimension allowance. |
| K8: certified empty core | S7:195–229 and E:150–190 retain the positive \(4^{-j}\) allowance when \(k=0\). E:361–374 uses that allowance in stopping. |
| K9: impossible restrictions and direct branches | S8:195–206 recognizes impossible restrictions and uses \(+\infty\); F:403 covers a singleton residual set. S8:570–571 and 683–684 cover all-fixed strong fields and zero-row lattice problems directly. |
| K10: generic fallback shared root | A:439–674 contains the tensor shared-root conversion, canonical tuple selection, and base-only enlarged multiplier. S3:539–601 and E:61–72 use the corrected format. |
| N1: initial flow feasibility | S8:296–318 explicitly inherits fixed nonempty residual feasibility and provides a pre-sampling feasibility solve. |
| N2: short residual cycles | F:543–549 covers two-cycles on distinct arcs and one-arc loops, as well as the convex two-cycle formed by both residual copies of one arc. |

The additional earlier certificate distinctions are also present: certificate encoding enters \(I\), checking is charged separately; the SOS specialization certifies the residual Hessian form, rather than the objective; general certified recourse does not silently assume residual convexity.

**Joint critical-limit solver.** I independently rechecked F:25–368, including the parts most exposed to elimination and output errors.

The pure powers \(y_i^{D-1}\) are monic leading terms under every degree-compatible monomial order. The remaining derivative terms have smaller total degree. The coprime-leading-monomial criterion proves the quotient basis for every finite normalized \(z\), and every normal-form recursion strictly decreases total degree. The memoized cutoff \(r(D-2)+1\) covers multiplication of each quotient basis monomial by each coordinate. It does not enumerate exponentially many reduction paths.

Simultaneous triangularization of the commuting multiplication matrices gives joint zero vectors, with multiplicities, over the Puiseux field even when the quotient is nonradical. For a generic linear form every vector pole is visible. The normalized leading coefficient is therefore
\[
C(\lambda)\prod_{v\in\mathcal L}(T-\lambda^{\mathsf T}v)^{\mu_v}.
\]
Comparison with the polynomial dependence on \(z\) forces the total pole valuation to be an integer. The identity then extends from the complement of the pole hyperplanes to all independent form coefficients. A form that hides a pole need not have the intended limit interpretation; the correctness proof does not grant it that interpretation.

Differentiation in each independent form coefficient, followed by division by \(\gcd(p,p')\), cancels exactly \(\mu_v-1\) copies of each projected limit. The derivative of \(C\) retains a factor at that limit and vanishes there after division. The remaining denominator is nonzero, since \(\mu_v\ne0\) in characteristic zero and distinct good projections are separated. The modular inverse recovers every coordinate of the same vector. The finite moment-form list avoids at most \(N+\binom N2\) nonzero polynomial conditions, each of degree at most \(r-1\), so it contains a good form.

The real critical-limit lemma at F:201–223 uses evaluation vectors and every rational form. It does not presume that a convergent real sequence has already been assigned to one Puiseux branch. Polynomial density forces the entire limiting vector to equal a bounded joint limit. Compactness and uniform convergence of the deformed objectives then recover an original box minimizer on a fixed face. Every other kept candidate is checked for box membership, so a bad form cannot produce an infeasible value below the optimum.

Value substitution at F:259–287 returns \(f(r)\bmod P\) in the same root. The value resultant is nonzero and has degree at most \(\deg P\); V1 supplies the missing integer normalization. Isolating a squarefree product of two value polynomials compares two candidate values, including equality, without forming the joint field of all candidates. Re-isolating the winner removes unnecessary comparison precision.

The dimension dependence is \(c_d^k\), with defining polynomial degree at most \((D-1)^k\). Normal-form parameter degrees, determinant interpolation, gcds, modular inverses, value composition, resultant construction, separation and refinement have fixed polynomial dependence on the explicit coefficient length. The explicit F:330–368 ledger has ample slack for these routines; its \(U^{5010}\) bound fits the displayed exponent 10000. The label-enumeration factor in the mixed version is multiplicative, and a fixed enlarged implementation constant is selected before the strong-field weights or fallback budgets are chosen.

This is a degree bound for an isolated-root representation, not a bound requiring a minimal polynomial. Heights and isolating endpoints retain polynomial dependence on sampled coefficient bits. The generic tensor fallback is different: it can multiply separate scalar degrees, but those are already bounded by a base-only exponential. It does not replace this constant-base component solver.

**Continuous recourse and core-only release.** E:119–201 proves the common search with fixed residual feasibility. Conditioning on the residual noise leaves independent core coefficients. Adaptive retained cells are charged to true near-optimal nodes of a deterministic grid; the proof does not condition on survival. Exact and certified modes give their respective \(Q_{\rm ex}\) and \(Q_{\rm ap}\) through the appropriate neighbor allowances. The empty-core convention is now consistent throughout.

E:205–247 proves exclusion and closure globally. The coordinate slabs cover every residual point outside the patch, and each slab value is a global restricted minimum or a certified lower bound. Original endpoints omit unnecessary slabs. The full core-hull Lipschitz allowance is used. Every sign fixing is justified on the same containing box and fixes an original bound; simultaneous fixing is sound. The subsequent Hessian test proves a unique patch minimizer only after global containment has been established.

E:251–279 constructs the tangent certificate using residual convexity alone. The weak convex optimizer supplies a feasible near-minimizer; a segment toward the endpoint minimizer of the tangent yields the required tangent gap. A residual strong-convexity modulus is unnecessary for this value oracle. Conversely, the core-only patch theorem expressly requires a uniform residual modulus; qualitative strict convexity or point growth of the core does not replace it.

For core-only noise, E:497–580 proves the Lipschitz selector, differentiable conditional value, growth lift, and finite-law active-core tail. E:582–660 constructs the active-stratum boundaries and their gradient images. The three-block description has the stated format bound; coefficient sizes do not enter the analysis-only degree. The cube-jitter calculation includes every atom, including atoms on exceptional sets.

The release proof at E:662–741 handles several weak or zero multipliers simultaneously. On a stable two-sided ball in the free core face, a zero nonnegative multiplier has zero gradient; a small one satisfies the displayed quadratic gradient bound. The mixed block has squared norm at most \(\mu g/2\). The Schur complement gives a positive released block, and restoring eliminated residual coordinates gives the stated \(\nu\). E:789–813 fixes active core normals first. A zero-dimensional core face is handled by the residual modulus directly, so no two-sided argument is incorrectly applied to an active core normal.

Both continuous samplers are chosen in the order base-only fallback multiplier, thresholds, stopping depth, and \(M\). All sampled/query bits and certificate checks are charged. The rare branch solves the same draw and returns one common-root fallback tuple. Ordinary patch descriptors remain compact while the global proof record has an expected, rather than every-draw polynomial, size bound.

**Native integers, flows, and TU systems.** Native coordinate restrictions at F:391–415 cover every competing feasible label, including under coupled residual inequalities. Empty restrictions and the singleton case are explicit. Full point growth and integer unit separation force the incumbent label at the selected cap; completion solves its entire core slice exactly. The implicit alternative adds its own active-core event instead of assuming that event follows from label exclusion.

The exact convex integer oracle at S8:242–254 and F:517–532 is restricted to separable fixed-degree rational costs convex on the entire real native interval, with TU constraints and all tightened bounds. Tangent extensions permit the cited scaling algorithm to query outside an interval while retaining convexity and polynomial-length rational evaluations. Exact optimal extreme points of the required linear programs are charged. This is not an oracle for arbitrary nonseparable integer convexity, arbitrary matrices, or a continuous value approximation rounded to integers. Feasibility is decided by the first exact TU linear program. The external scaling theorem's identity remains a literature dependency.

The marginal-potential argument covers all permitted short cycles. Potentials have polynomial bit length because rational unit marginals do, not merely because their real magnitudes are bounded. Network chart families and TU active-basis chart families are fixed before sampling; the selected chart belongs to that family even though the algorithm selects it adaptively.

The deterministic grid corollary is correct. On the cell containing an optimal core, curvature-corrected corners give a lower bound
\[
\min_{G_m}\ell-\frac{kL}{8m^2}\le f^*.
\]
At a grid point minimizing the lower answers, its feasible upper answer is at most that lower answer plus \(\eta\). The smallest returned upper answer consequently has certified gap at most \(kL/(8m^2)+\eta\). No residual label is rounded, and exact flow calls give \(\eta=0\).

F:672–695 proves proximity by TU conformal circuits with entries in \(\{0,\pm1\}\). A nearest tightened feasible point cannot allow a whole conformal circuit to remain in every minimizer interval; charging its multiplicity to a violated endpoint bounds the total distance by \(n_R\sum_i\operatorname{dist}(z_i,I_i)\). This is enough for the mixed-derivative loss in F:697–735.

The optimal-face certificate handles the full set of tied flows. At a center all adjusted scalar minimizer intervals contain an optimal feasible flow. Identities along the core face and positive first outside differences make the same tightened flow set optimal throughout that face. Inward derivatives are minimized over that whole set. For an interval containing at least three integer minimizers, scalar convexity and equal values make the polynomial affine on the interval. Inward differentiation of nonnegative residual curvature produces convex derivative costs; two-point intervals use linear interpolation and singleton intervals substitution. Thus every derivative minimum has the promised exact separable TU oracle.

Normal-margin analysis conditions on free-face noise. Normal noise is constant on that face, so the canonical face minimizer and its tied-flow set are independent of the conditioned normal coefficient. At a unique globally optimal core, every tied smooth branch is itself globally minimal there and has nonnegative inward derivatives. This justifies the all-tied-flow margin event. The vertex face, empty chart zero sets, and identically zero chart restrictions have the required separate treatment.

The general nonlinear boundary sampler needs a positive chart-value margin, not merely a distance-to-zero event. F:754–780 supplies it by a two-block elimination and a coefficient-height lower bound. Its parameter function enters bit length. In contrast, the affine margin proof supplies both the nonempty-zero-set distance estimate and the empty-zero-set rational vertex estimate, giving polynomial sampling bits in the bilinear case.

TU duals are bounded at a vertex of the slope-inequality polyhedron after fixed coordinates and dependent rows are removed. Every remaining native interval supplies an inequality for its column; full row rank makes the polyhedron pointed. A nonsingular active transpose-TU basis, with possible unit rows, has inverse entries \(0,\pm1\). Its symbolic multiplier map therefore has the stated degree and base coefficient bounds. The bounded-inequality slack reduction preserves TU, fixed feasibility, the objective and core derivatives, and has polynomial-length finite slack bounds.

**Strong fields and global output.** F:964–1016 correctly uses derivative enclosures computed before sampling. The events that coordinates remain unpinned depend on their own coefficients and are independent. Recomputing enclosures after pinning is neither needed nor used. The frozen S8:614–620 antecedent for “bad events” could be clearer because the previous sentence describes the complementary pinning event; F's proof and the \(q_i\) definition make the intended unpinned event unambiguous. The root reports a live wording clarification, which is not needed for the frozen mathematical argument.

Every surviving monomial lies in one connected component because its original support is a clique. The expected component cost is weighted by the actual algebraic and native-label factors \(\prod_{i\in C}a_i\). Summing connected sets gives the displayed denominator \(1-4\Delta_+\beta\). This retains numerical capacity dependence for native coordinates and the large proved \(c_d\) for nonquadratic continuous components; it is not an unweighted percolation estimate.

Point errors, value widths, and feasible objective gaps are allocated separately with the logarithmic component allowance. No flat-component gap is used as a substitute for distance to the stored optimizer. All-fixed instances are evaluated directly. The law can be any stated grid size, but \(q_i(M)\) and \(\beta(M)\) must be recomputed at that size. Endpoint grids are not nested, so arbitrary subcriticality is not monotone in resolution. The supplied sufficient strong-noise inequalities are monotone and do imply the stated bounded denominator.

The output has one root per component. Its total value is a rational constant plus a sum of component values, with enclosure refinement. It does not include a low-degree single-root representation of the whole sum or efficient exact sign/equality tests for that sum. S8:644–648 and model:364–377 state this correctly. The final general summary at S8:773–775 would be clearer if “share one root” explicitly said “within a completion or component”; the formal component theorem and model already give the correct limitation. This is an optional wording clarification, not a mathematical blocker.

**Independent audit of the generalized lattice theorem.** The fixed-degree piecewise-polynomial extension is fully proved at S8:652–717 and F:1020–1127.

At a rational auxiliary query, the objective separates into convex scalar functions \(\psi_j(t)=g_j(t)-\alpha(T^{\mathsf T}a)_jt\). Midpoint convexity gives nondecreasing forward differences on consecutive integers even when a unit step crosses several rational knots. Each difference evaluates the actual pieces at both integer arguments; the algorithm does not extrapolate the piece at the first argument. Continuity makes knot values consistent. Binary search for the first nonnegative difference, or the upper endpoint if none exists, yields an exact integer minimizer; neighboring signs certify it by telescoping. Negative labels, ties, affine/constant pieces, singleton intervals, nonsmooth knots and \(k=0\) are all covered.

Completing the square gives
\[
Z_\xi(a)+C_\xi
 =\min_x\left[F_\xi(x)+\frac{\alpha}{2}
       \left\|a-Tx+\frac{\xi}{\alpha}\right\|^2\right].
\]
The box contains \(Tx^*-\xi/\alpha\) for every original optimizer, so the auxiliary optimum equals the original optimum minus \(C_\xi\). Every attaining integer witness at a corner has original value at most the auxiliary value plus \(C_\xi\). This witness inequality is the correct bridge from auxiliary error to original gap.

Balanced equal-part meshes preserve nesting and avoid tiny clipped endpoint gaps. Only refined coordinates require the balance comparison. A zero, dependent, or constant row is allowed: positive row noise makes its auxiliary width positive. The independent perturbation coordinates are the rows \(\xi_i\), rather than the dependent original coefficients \(T^{\mathsf T}\xi\). The resulting count is exactly \(H_{\rm rat}\), with no extra number-of-labels factor.

The denominator budget is taken from expanded original coefficients, before auxiliary values are used. With \(Q=Q_{\rm den}\), each unary value at an integer belongs to \(Q^{-1}\mathbb Z\); the quadratic correction belongs to \((2Q^3)^{-1}\mathbb Z\); and row-aligned noise contributes \([Q^2(M-1)]^{-1}\mathbb Z\). Thus every original value lies in \([D_0(M-1)]^{-1}\mathbb Z\), with \(D_0=2Q^3\). Rational knots select a piece and add no evaluation denominator. The auxiliary squared-noise denominator \((M-1)^2\) is irrelevant.

At \(J=\log_2M\), the original incumbent gap is bounded by
\[
E_J\le \frac{k\alpha s^2}{8M^2}
 \le \frac{1}{8D_0M}
 <\frac{1}{D_0(M-1)}.
\]
The gap is a nonnegative multiple of the original lattice spacing, so it is zero on every draw. No genericity, uniqueness, residual-label margin, or rare fallback is used.

The complete expanded lists are charged in \(I\). Their denominator product, row endpoint sums, positive widths and selected \(M\) have polynomial encoding length. Fixed degree bounds integer-power and rational evaluation lengths. Piece lookup, binary searches, exact differences, and convexity validation have fixed polynomial bit exponents independent of \(k\). Query denominators do not accumulate across the possibly many visited cells: a new query comes from base data and mesh indices, and an incumbent is selected by comparison. Native integer bounds control every returned label's bit length. Output length is polynomial on every draw.

A larger common \(M\) also works, but \(J\) must be reset to its new \(\log_2M\). The curvature error then decays quadratically while original lattice spacing decays linearly; the sufficient inequality improves. Keeping the old cap while changing \(M\) would not prove termination. Model:195–231, S8:755–768 and A:765–776 include the reset. The deterministic listed-label comparison at S8:728–739 uses the lifted dimension \(k+1\), so its \(O(n^k)\) binary zonotope bound has the correct exponent.

**Precision and shared interfaces.** Three distinct closure precision regimes survive integration:

1. Ambient continuous recourse, ambient native integer recourse, core-only strongly convex continuous recourse, interior flow, and bilinear flow/TU have polynomial sampling bits.
2. General nonlinear core-only flow/TU at arbitrary core faces has \(f_d(k)\operatorname{poly}_d(I)\) sampling bits, due to the chart-value margin's coefficient-height budget.
3. Strong fields accept every supplied grid size, with their work controlled by the actual \(q_i(M)\), label counts and derivative variation. They are a strong-noise result, not an arbitrary-small-noise closure theorem.

The lattice route independently has polynomial sampling bits and exact deterministic lattice termination. These statements distinguish sampling precision from later \(q\)-bit evaluation, which refines the stored output for the same draw.

The tensor conversion in A:439–583 is complete. Squarefree scalar quotients form a reduced Cartesian tensor algebra. Moment forms separate every complex tuple, and squarefreeness of the characteristic polynomial is an exact test. Characteristic coefficient derivatives and a modular inverse recover all coordinates. Rational sums of refined source isolators select the designated tuple; canonical elimination has already selected the same optimizer and value in every scalar formula. The conversion does not pair unrelated optimizer coordinates. Its product degree is base-exponential independent of added coefficient bits; matrix, interpolation, inverse, separation and refinement work have absolute polynomial exponents.

For this generic fallback, the value identity must hold at the selected root, and need not hold modulo the whole Cartesian polynomial. That is correctly distinguished from the component solver's stronger remainder identity. The enlarged base multiplier is selected before thresholds and sampling and includes conversion. Every \(B\operatorname{poly}_d(I+b+q)\) claim preserves the separation between base degree and added height.

The input-length resolution proposition correctly fixes the format constants and oracle implementation. Grid atomic errors improve with larger \(M\); the lattice cap is reset. Nonlinear boundary flow/TU can use a common envelope for a supplied \(K\ge k\), but then sampling, output and work depend on \(K\). Taking \(K=I\) is not an actual-small-\(k\) FPT guarantee. The proof does not claim that parameter-dependent precision is necessary. The Gaussian support schedule recomputes its box and cap and solves its support/accuracy inequality; this review checks that interface, not the separate quadratic closure proofs. Arbitrary compact semialgebraic descriptions do not automatically have polynomial-logarithmic widths, and arbitrary oracle programs do not share one polynomial exponent. These qualifications appear in the frozen statement and proof.

The P1 comparison is now appropriately narrow. S7:514–526 acknowledges the companion cubic full selected-point result and the already-known quartic core-noise point obstruction. S7:556–572 correctly observes that the uniform residual modulus supplies a rank-\(k\) quadratic convexifier, and that its scale can be \(T^2/\mu\) while the direct count retains \(L/\sigma\). The companion supplied-convexifier comparison is limited to cubics convexified on the feasible polytope, or fixed-degree objectives convexified on all of \(\mathbb R^n\). No necessity claim for a residual modulus or absence of every convexifier is made. The source identity, precise external theorem correspondence, and priority remain pending the literature audit.

**Result-by-result status.** “Verified” means I verified the frozen argument under its expressly stated classical tools and oracle/certificate contracts. It does not certify those sources' bibliographic identity. “Verified subject to V1” means the mathematical argument and bounds are verified, but the auxiliary integer-polynomial implementation must make the explicit normalization correction. “Not verified literally” identifies the false subsidiary integer-coefficient claim rather than a missing optimizer proof.

| Section 7 result | Proof location | Status |
| --- | --- | --- |
| lem:rec:value | E:121–137 | Verified. |
| prop:rec:search | E:145–195 | Verified, including certified \(k=0\). |
| lem:rec:exclusion | E:205–223 | Verified. |
| lem:rec:closure | E:225–247 | Verified. |
| thm:rec:qp | E:283–444 | Verified under exact convex QP and face tools. |
| cor:rec:forest | E:446–458 | Verified reduction and bit contract under the stated forest-QP tool. |
| lem:rec:convex-oracle | E:251–279 | Verified under weak convex optimization; convexity suffices. |
| thm:rec:poly | E:283–444; A:439–674 | Verified with the integrated common-root fallback and empty-core allowance. |
| prop:rec:rank | E:460–487 | Verified for positive semidefinite fixed quadratic corrections. |
| thm:rec:core-only | E:743–816 | Verified, including weak multipliers, core faces and same-draw fallback. |
| prop:rec:tube | E:582–660 | Verified under the stated QE and algebraic-tube tools. |
| prop:rec:release | E:662–741 | Verified for simultaneous release, including zero multipliers. |

| Section 8 result | Proof location | Status |
| --- | --- | --- |
| thm:int:solver | F:25–368 | Verified subject to V1; optimizer, common-root maps and constant-base budgets are proved. |
| cor:int:mixed-solver | F:374–383 | Verified subject to V1 in its comparison/output routine. |
| thm:int:native | F:391–475 | Verified subject to V1 in algebraic completion; rational quadratic case verified directly. |
| cor:int:native-implicit | F:477–515 | Verified ordinary branch; algebraic fallback subject to V1. |
| prop:int:hs | F:517–532 | Verified at its stated separable convex rational TU scope under the scaling and exact LP tools. |
| lem:int:potentials | F:534–555 | Verified, including rational marginal heights and short cycles. |
| cor:int:grid | F:559–572 | Verified, with error \(kL/(8m^2)+\eta\). |
| thm:int:flow-interior | F:608–670 | Verified stopping, sampler and work; algebraic tests/completion subject to V1. |
| lem:int:proximity | F:672–695 | Verified for TU systems and networks. |
| thm:int:face | F:697–752 | Verified, including exact minima over all tied flows. |
| thm:int:flow-boundary | F:806–864 | Verified with parameter-dependent precision; algebraic tests/completion subject to V1. |
| cor:int:bilinear | F:866–897 | Verified polynomial-bit improvement; algebraic completion subject to V1. |
| thm:int:tu | F:901–960 | Verified with explicit inherited polynomial model; algebraic completion subject to V1. |
| cor:int:tu-ineq | F:953–960 | Verified finite-slack reduction; inherits the same V1 qualification. |
| thm:int:strong-field | F:964–1016 | Verified component decomposition, weighted work and joint refinement; nonquadratic component auxiliary outputs subject to V1. |
| thm:int:lowrank | F:1020–1127 | Verified in full for the stated fixed-degree convex piecewise-polynomial native integer model. |

| Supporting result | Proof location | Status |
| --- | --- | --- |
| lem:app:rec:stopping | E:346–399 | Verified, including positive certified empty-core error. |
| lem:app:rec:lift | E:497–542 | Verified. |
| lem:app:rec:core-tails | E:544–580 | Verified under finite-tail and nonsingular-zero tools. |
| lem:int:quotient | F:75–97 | Verified for normalized equations. |
| lem:int:triangular | F:106–124 | Verified. |
| lem:int:leading | F:137–164 | Verified as a polynomial identity before specialization. |
| lem:int:recovery | F:170–199 | Verified for good forms. |
| lem:int:limits | F:201–223 | Verified without assigning a sequence to a prior branch. |
| lem:int:forms | F:225–237 | Verified. |
| lem:int:values | F:259–281 | Not verified literally: integer-resultant claim needs V1. Value identity, nonzero resultant and exact comparison proof verified. |
| lem:int:cost | F:289–328 | Verified; clearing the missing denominator fits the bound. |
| lem:int:budget | F:330–368 | Verified with the stated implementation and slack. |
| lem:int:label | F:391–415 | Verified, including singleton residual sets. |
| lem:int:native-stop | F:417–436 | Verified. |
| lem:int:face-general | F:697–735 | Verified. |
| lem:int:margin | F:754–780 | Verified, including empty zero sets and \(q=0\). |
| lem:int:normal | F:782–804 | Verified, including canonical face selection and all tied flows. |
| lem:int:affine-margin | F:866–882 | Verified in both zero-set cases. |
| lem:int:tu-dual | F:905–941 | Verified after fixed-coordinate and rank preprocessing. |

These tables cover all 47 formal results in the assigned sections and appendices. The five examples were checked separately: ex:rec:feasibility at E:820–827, ex:rec:star and its variant at E:829–857, ex:rec:fiber and its strictly convex variant at E:859–880, ex:rec:weak and ex:rec:two-sided at E:882–894. Their displayed values, Hessian obstructions and multiplier behavior are verified. They distinguish fixed from changing feasibility, global from local rounding error, strict from strong convexity, weak residual multipliers, and one-sided active core directions correctly.

The relevant shared results have the following interface status: lem:count:interval, thm:count:local, cor:count:levels, lem:count:rounding and thm:count:cells are verified for their use here; the growth-tail proof at A:238–325 and finite-tail proof at A:356–422 are verified; rare-fallback accounting is verified; lem:count:shared-root and thm:count:fallback are verified; cor:count:universal-law and prop:model:uniform are verified for the assigned grid, lattice, strong-field and parameter-dependent routes. Their Gaussian support interface is verified, while the separate Gaussian quadratic optimizer proofs are outside this review's scope.

**Checks performed and remaining handoff.** I used scoped cat, rg, nl with sed, and sed reads of the named immutable sources and evidence records. A Python script checked SHA256 and line counts for the 20-file manifest and extracted every theorem, lemma, proposition, corollary and example in the assigned four TeX files; it found 47 formal results and five examples. The normalization counterexample and all proof inequalities were checked analytically. A report-only check after writing passed for final newline, trailing whitespace, math delimiter pairing, hash matches and complete result-label coverage.

No literature research, optimization experiment, delegation, TeX mutation, build, project-wide verification, CI inspection or commit was performed. The only file authored by this review is this report.

The remaining mathematical handoff is to verify the accepted V1 normalization in a focused immutable revision. The two noted summary/antecedent wording clarifications are nonblocking. Bibliographic identity and external source correspondence remain pending the serialized literature audit. After those tasks and the other independently assigned scopes are resolved, the root can make a full-manuscript submission decision; this report does not supply that broader approval.

