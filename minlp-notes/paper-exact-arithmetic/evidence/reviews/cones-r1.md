# Actual-manuscript review: algebraic cone arithmetic

Date: 2026-10-05. Reviewer scope: the cone portion of Appendix L and the actual Appendix J interfaces it calls. This is a fresh manuscript proof reconstruction, not approval inherited from the source-note audit.

## Verdict

The internal cone proofs pass analytic reconstruction, but the latest displayed Khachiyan–Porkolab bound requires correction or a different precisely justified contract. I found no unresolved mathematical gap in the field model, compressed projection, uniform exact gap, rational reduction, canonical witness field, selected-embedding recovery, mixed-integer composition, or known-level corollaries conditional on a valid integer-witness bound. Two minor display/count corrections found during this review were sent through root and are now corrected in the manuscript.

The external Khachiyan–Porkolab contract remains a source gate at this review cutoff. During review, the manuscript replaced the original charged-degree-exponent form with a separate product of dimension factors. The new formula still has a counterexample for variable atomic degree; see Finding 5. I sent the counterexample to root for Luna's exact primary-source reread. This conditional analytic pass does not clear that source gate or constitute final submission approval.

Reviewed Appendix L hash after rereading its corrections:

    02b04f22e1a1b89380a06c55902dcefb37a8d766f1f26f7ed3e6bc322087f0f8

Reviewed Appendix J hash:

    21361c5eb3eefa2f4decf1ae3c6b3a08755ba1cb59a4d77873a08f341d4aae4a

The hashes identify the exact files at the review cutoff. Later edits need a scoped reread.

## Actual reconstruction

**Charged input field and Hessian parameter.** The cone setting defines a dense primitive irreducible polynomial, a rational isolator selecting one real root, and explicit power-basis vectors for all coefficients. Every vector, scalar entry and field datum counts in \(L\), so \(D\le L\). The field degree is allowed to vary. The text distinguishes a chosen real embedding from a field having exactly one real embedding.

The parameter is the \(K\)-span of the continuous Hessians
\[
 2(A_{ix}^{\mathsf T}A_{ix}-c_{ix}c_{ix}^{\mathsf T}).
\]
Flattening and the nonzero-minor rank criterion establish equality with the real span at the selected embedding. This does not confuse that rank with the rational span of algebraic matrices. Every squared row retains its affine cone sign. No native-PSD theorem is invoked for these potentially indefinite Hessians.

**Internal nonconvex algebraic inputs.** I read the genericity, small-perturbation, multiplier reduction, common-field, and field-radius/boxed-value proofs in the first portion of actual Appendix L because the cone argument depends on them. The generic bad incidences are proper: values and gradients are freely adjustable, and the displayed quadratic example makes both KKT determinants nonzero. The cumulative degree and integer-grid argument gives one polynomial-bit perturbation tuple on the finite collection of original charts. It is not constructed by the decision algorithm.

At a selected perturbed minimizer, independent active gradients justify ordinary KKT necessity. The nonsingular multiplier Hessian permits adjugate elimination; the separate nonsingular bordered determinant makes
\[
 -(\det M)^2GM^{-1}G^{\mathsf T}
\]
nonsingular. The field proof keeps local coefficient sums at archimedean places and maxima at finite places, obtaining polynomial logarithmic norm before determinant expansion. It does not sum heights over an expanded exponential monomial list.

Appendix J **lem:qc-elimination** is applicable because its hypotheses are algebraic regularity, nonzero output denominator and finite ordered output limits. Its statement imposes no convexity. For one original parameter the manuscript supplies the valid dummy-inner-parameter specialization. The actual J proof deforms to a finite quotient, removes permanent undefined-output factors by lowest-\(\zeta\) coefficient extraction, and then extracts deformation and ordered parameter coefficients. These operations retain the selected finite output and do not increase local norms.

The common-field lemma fixes one limiting tuple before varying linear outputs. Coordinate algebraicity and a relative primitive element give \([K(w^*):K]\le\Lambda\); no coordinate-degree product is used. Product-formula root bounds and Mahler measure give absolute coordinate minimal-polynomial coefficient bounds. The bounded primitive-element combination, trace pairing and discriminant separation give one short absolute representation. Thus the actual field-radius and boxed-value lemma supports the conic radius and residual gap.

**Exact projection and integer radius.** The manuscript includes every active affine subset and every pivot-row/pivot-column rank chart, guarded by the nonzero pivot minor and all nonpivot consistency equations. It explicitly includes rank-zero and zero-dimensional charts. The lifted affine normals are polynomial in \(z\) of degree at most one and constants of degree at most two.

The generic perturbation choice is pointwise in real \(z\), selected from one uniform finite integer grid. Uniformity concerns the grid and degree bounds; the text does not incorrectly assert a single perturbation generic for all \(z\). All grid points enter the Boolean disjunction. Each atom has polynomial degree and individual coefficient bits, even though the disjunction may be exponentially large. Chart and stationarity denominators are cleared by even powers under nonvanishing guards.

The prefix keeps the one radius outside the universal parameter:
\[
 \exists R>0\ \forall\delta>0\
 \exists(\varepsilon,\lambda_1,\ldots,\lambda_h).
\]
For forward validity, a fixed original feasible lift stays feasible in outward bands, and comparison bounds the uniformly coercive perturbed minimizers. For reverse validity, take \(\delta=1/j\); the encoded points stay in one fixed ball, and their band errors vanish. The finite grid's polynomial values are uniformly bounded on that ball, even if the chosen grid point changes. A convergent subsequence satisfies the exact original lifted equations and every affine row at the same \(z\). Thus the formula describes \(Y\) itself, including when \(Y\) is nonclosed. The \(h=0\) affine case is also accounted for.

The field-generator variable is put with \(R\) in the outer existential block after field arithmetic is reduced modulo the input polynomial. Positive rational common denominators preserve signs. The selected-root equation and isolator force the intended embedding. Block dimensions are exactly \(2,1,h+1\); there is one generator coordinate, while the varying degree \(D\) is charged in the atoms.

The initially reviewed Khachiyan–Porkolab paragraph stated the witness bound in the form
\[
 b_*d_*^{O(t_*^4)\prod_j O(n_j)}.
\]
That form charges quantified dimensions in the degree exponent and would support the displayed radius if externally justified. The latest file instead displays \(b_*d_*^{O(t_*^4)}\prod_j n_j^{O(n_j)}\), which does not supply a valid uniform bound for arbitrary atomic degree and dimensions with absolute constants; Finding 5 gives a concrete obstruction. Its independence claim is correctly only atom-count independence. The rest of the use is sound: it adds the fixed-zero integer coordinate for feasibility and uses only the witness bound, not the formula-size-dependent algorithm. Given a valid charged contract, a uniform continuous box meets every nonempty original fiber inside the resulting integer box. The boxes preserve existence, rather than every point of the unbounded original set.

**Uniform gap and outward rounding.** The residual maximum contains zero, every squared cone row, every cone sign, every affine inequality, and both signs of each equality. Compactness makes its minimum attained. Its epigraph adds no continuous Hessian direction, and the rational upper bound makes a nonempty compact boxed quadratic problem. Integer substitution has uniformly bounded encoding size for fixed \(t,h\), so one original-system gap \(\Delta\) works for every boxed integer assignment.

The rational coefficient accuracy is sufficient for all scalar affine errors and cone-vector errors. The derivative estimate on the input isolator has polynomial bit length, even when its magnitude is large. Dense root refinement therefore delivers the required precision.

With \(\eta=\Delta/(256T)\), \(\epsilon=\Delta/(256T^2)\), and \(s_i=\widehat t_i+2\eta\), every exact original point lifts, including the apex. Conversely \(|s_i-t_i|\le3\eta\), the lift forces \(s_i\ge0\), and hence \(-t_i\le3\eta\). Absolute squared-norm and squared-right-side errors give
\[
 q_i\le3\epsilon(T+3\eta)^2+
       \eta(2T+\eta)+3\eta(2T+3\eta)
 \le66\Delta/256<\Delta/2.
\]
This calculation never assumes the original true \(t_i\) is nonnegative. Affine and sign residuals are also below \(\Delta/2\), so the exact gap forces a nonempty original fiber. Rounded Hessians can have a larger span; the manuscript correctly applies no span theorem to them.

**Explicit rational Lorentz lift.** I reconstructed the two-coordinate triple construction, angle comparisons, exact folding, slack monotonicity, apex behavior and tree composition. A delegated independent read-only audit reconstructed this same distinct subproof and the rounding calculation; it found no proof-level defect.

The triples satisfy the Pythagorean identity. The first angle is at least \(\pi/4\), the second is exactly half the first, and subsequent angles lie between half and the whole preceding angle. Thus exact reflections fold into the terminal angle. Choosing absolute-value slacks at equality preserves norm and gives inner inclusion. Added slack can only increase norm, while the terminal angular row and \(c_J=b_J+1\) give outer factor \(1+\delta\). At \(s=0\), norm monotonicity excludes any nonzero original vector.

A balanced padded tree has fewer than \(2d\) internal vertices. Its accumulated factor is \((1+\epsilon/(2k))^k\le\exp(\epsilon/2)\le1+\epsilon\). Stage count and coefficient size are polynomial in cone dimension and logarithmic inverse tolerance. The displayed exact stopping tests need only rational and integer arithmetic.

**Final integer solver and exact fiber.** The constructed linear system is rational and introduces only continuous auxiliaries. Its integer dimension is still \(t\), while its continuous dimension may grow. The manuscript invokes Lenstra Section 5 with this precise mixed-integer contract, rather than an algebraic-coefficient MILP algorithm or Appendix D's integer-point separation interface. The linear solution's continuous coordinates are explicitly not asserted to satisfy the original cones.

For full point recovery, the returned polynomial-bit \(z\) is substituted in the original exact field system. The field and continuous Hessians remain unchanged. Recovery takes place in that exact fiber, whose input size is polynomial for fixed \(t,h\). Canonical selection is within that fiber, without claiming a global minimum-norm mixed-integer point.

**Canonical continuous field and selected embedding.** The unknown auxiliary box strictly contains the canonical lift. Compact perturbed minimizers have only that lift as a cluster point by uniqueness of the minimum-norm cone point. Hence every artificial box row is eventually inactive. The subsequent original chart/support and KKT coefficients contain no unknown box endpoint.

Every \(K\)-linear output uses that same limiting tuple, giving relative joint degree \(\Lambda\) and absolute degree \(D\Lambda\). The point's original-input height bound prints a box containing the canonical point itself. A box merely meeting the feasible set is not used as a substitute.

The norm-sublevel cone has squared Hessian \(8I\), so queries have span at most \(h+1\) and stay in the original input field. Norm bisection and the projection inequality place all points in the selected slice within \(\tau/4\) of the canonical point. Closed coordinate bisection preserves nonemptiness, and the resulting midpoint has coordinate error below \(\tau\). Restarting from the original box for each request ensures one fixed tuple is approximated.

Appendix J **thm:qc-recovery** is correctly applied to \((\alpha,x^*)\), with absolute degree bound \(D\Lambda\). I reread its moment-curve primitive search, recognition height accounting, degree-drop norm multiplicities, interpolation and derivative coordinate reconstruction. The source input-generator coordinate preserves the field map and selected embedding. The manuscript verifies the input polynomial and isolator at \(b_0(\beta)\), then every original row and cone sign using **lem:qc-sign**. Those checks certify feasibility and embedding; canonicality follows from the algorithm.

The proper-extension example is correct: the two cones force \(x=\sqrt3\), while \(y=\sqrt2\) retains \(K=\mathbb Q(\sqrt2)\). The squared-Hessian span is one and the absolute output field has degree four.

The continuous degree and total representation length are \(L^{O(h+1)}\); recovery time is conservatively \(L^{C_h}\). The mixed-integer statement claims polynomial time for fixed \(t,h\) and charges substituted integer length, without transferring that sharper continuous output exponent to the original mixed input.

**Known levels, strict denominator and classifications.** The algebraic threshold corollary starts with rational original cone data and uses the one field \(\mathbb Q(\theta)\). Scalar extension preserves the original rational matrix rank; the affine threshold adds no Hessian direction. Radius and gap include the level from the outset. A true supplied finite infimum is attained exactly when a point with \(f\le\theta\) exists.

The fractional corollary now explicitly requires rational original cone data and rational affine \(f,d\), fixing the source-note scope ambiguity. Its reciprocal cone has residual \(4-4ds\) and sign \(d+s\ge0\), so it forces \(d,s>0\); every \(d>0\) admits \(s=1/d\). Adding the scalar \(s\) appends zeros to the old Hessians and contributes at most one new continuous Hessian direction. Recovering a point on \(f-\theta d=0\) and discarding \(s\) gives an optimizer at the known attained value.

The final paragraphs correctly distinguish unknown-value computation from a supplied-value interface; P at fixed continuous span or fixed \(t,h\); NP for supplied bounded integer domains and fixed \(h\); and the absence of an NP conclusion for arbitrary unbounded integer dimension. No FPT runtime is asserted.

## Findings, repair status and source gates

1. **Resolved display typo.** The Pythagorean triple formula contained a literal “quad” in math mode. The current version has the intended spacing command and was reread.
2. **Resolved vertex count.** The original padded-tree sentence claimed fewer than \(2d\) vertices. The current text says “internal vertices,” which is the correct count and the set of vertices carrying lifts.
3. **Resolved prewrite scope finding.** The optional fractional recovery corollary now explicitly assumes rational original cone data. No missing compositum is required.
4. **Optional clarity only.** The lift's construction time for an arbitrary rational tolerance should conventionally include that tolerance's binary input length. Its output-size dependence on \(d+\log(1/\epsilon)\) is valid. The actual tolerance constructed by the cone algorithm has polynomial encoding length, so this wording does not affect the theorem's proved runtime.
5. **Required repair: latest KP bound still needs charged degree dependence.** The file at the recorded hash displays \(b\,d^{O(t^4)}\prod_j n_j^{O(n_j)}\). This cannot be a uniform theorem for its stated arbitrary first-order convex-set model with absolute big-O constants. Take one free coordinate \(z\) and one existential block \(x_1,\ldots,x_m\), with equations \(x_1=2\), \(x_{i+1}=x_i^d\), and \(z=x_m\). The convex projection is the singleton \(\{2^{d^{m-1}}\}\); all atomic degrees are at most \(d\), and maximum coefficient bit length is constant. Its integer coordinate requires at least \(d^{m-1}\) bits. The displayed bound is only \(d^C m^{C'm}\) for absolute constants \(C,C'\). Fix \(m>C+1\) and let \(d\) grow: it cannot cover this witness. Repeated squaring alone would not expose this remaining issue because \(m^{O(m)}\) can cover \(2^m\). A valid contract must charge quantified dimensions in the dependence on degree, assume a fixed degree with the appropriate constants, or use some other explicit safe bound. Root was sent this counterexample after the latest source relay and is pursuing the exact primary-source gate through Luna. The conic application needs only a valid polynomial bound at its charged compressed blocks; it does not require the overstrong general display.
6. **Source provenance.** Canonical keys KhachiyanPorkolab2000, Lenstra1983 and Kocuk2021 were confirmed through root. The internal review performed no external source research. Geometric degree, recognition and univariate-arithmetic imports remain under the paper's shared Luna source verification; this review checks their actual use and internal interfaces.

The only required mathematical/source-contract repair at this cutoff is Finding 5. The internal projection, rounding, and witness arguments need no repair.

## Verification record

I read BRIEF, the root decisions and integration records, the prewrite audit, the full actual cone portion, its internal generic/field inputs, the relevant finite-infimum box-inactivity argument, and the actual J elimination/recovery/sign proofs. The author report **authoring/further-arithmetic.md** appeared during this review and was read. It records the exact separate-product KP formula relayed by Luna; that provenance does not remove the counterexample in Finding 5.

Targeted read-only commands used rg, cat and sed for discovery and inspection, and sha256sum for the exact manuscript versions. A scoped git diff of the new appendix returned no tracked diff; it was not used as proof or saved-file verification. No builds, tests, experiments, mathematical scripts, CAS runs, project-wide verification, or CI inspection were performed.

The direct scoped check

    rg -n '[[:blank:]]+$' paper-exact-arithmetic/evidence/reviews/cones-r1.md

returned no trailing-whitespace matches (exit status 1). The final hash reread confirmed the recorded L and J versions and the latest KP display. These are document/version checks, not mathematical verification or CI results.
