# Sol complete-proof review: continuous and integer recourse, r1

Date: 2026-10-05. Snapshot: evidence/snapshots/complete-proof-draft-r1/. Scope: frozen sections/07-recourse.tex, sections/08-integer.tex, appendices/E-recourse.tex, and appendices/F-integer.tex, with the relevant frozen model, count, finite-tail, and fallback interfaces. This is a mathematical review before final integration, not final journal readiness approval.

**Decision.** The complete appendices support the intended recourse results. I verified the new joint critical-limit solver, the continuous core-only release argument, the all-tied-flow certificate and TU transfer, and their finite-law budgets. I found no additional defect that defeats a theorem's intended feasible-instance result. The frozen draft still has known localized statement and output mismatches, so I do not approve this snapshot as publication ready. Two additional local issues are recorded below: the flow model needs explicit nonemptiness, and the marginal-potential necessity proof should cover short cycles on parallel arcs.

“Verified” below means that the actual frozen proof establishes the stated mathematical claim under its declared oracle and classical-tool premises. It does not mean that bibliography identities or classical theorem locators have been independently researched. Those remain with the authorized literature workflow. “Not verified as frozen” marks a false, incomplete, or mismatched displayed contract, even where its intended proof is sound and the repair is already accepted.

I read BRIEF.md, independent-review-brief.md, integration-contract.md, integration-decisions.md, prewrite-recourse-sol.md, early-integer-interfaces-sol.md, root-recourse-early.md, fallback-shared-root-sol.md, and integer-lattice-generalization-sol.md. Those records identify known integration items; the checks here rely on the frozen scientific proofs themselves.

**Snapshot identity.** The following SHA-256 values were computed from the reviewed files and agree with the frozen manifest.

| File in the snapshot | SHA-256 |
| --- | --- |
| manifest.json | d9ca80c5c376344069ed0fec75fac23470b5bdbb85b89a424e8ff9a9a07462c7 |
| sections/02-model.tex | 143bedfa0aa700a84f0d912a0a7534a76126d2283ba8909defa30325006638f3 |
| sections/03-counting.tex | f54a72dca58da3d71595a1e4159ad9c356555ba5ffa88b670fada18778535f83 |
| sections/07-recourse.tex | f16775e24756b7703e0eb2df4840481d339222d99839773ac76ecd2341fb04c5 |
| sections/08-integer.tex | efccbe1a347fe47320e949445996ff1eaff7b7a6d675ec0d94581d5e71158fa2 |
| appendices/A-finite-noise.tex | 83943cf612ac484347b25ed583433c3c7abf1d120d5a73a4097d99c642784a7c |
| appendices/E-recourse.tex | 192afd2810e89e27d3cfeec1647ec2fcb3edebf5bffa9ab9cb1a2284b4101926 |
| appendices/F-integer.tex | 83a7b58a4b8a74f0c66af58af59163536f87ec1dccc63c6a9bc693fd7ac4e798 |

All locations below are relative to this immutable snapshot, not the live manuscript.

**1. Additional local findings.**

**N1 — Moderate model omission: flow feasibility must be explicit.** The flow setup at sections/08-integer.tex:256–265 does not expressly require its integer flow set \(Y\) to be nonempty or expressly inherit definition def:rec:instance's nonemptiness. Both thm:int:flow-interior at 283–295 and thm:int:flow-boundary at 370–383 refer to this flow model and promise an attaining flow. Appendix F:538–549 and 735–741 start by computing an optimal flow.

If nonemptiness is not inherited, a directed single-arc network with \(0\le z\le1\) and a required supply of two units has \(Y=\emptyset\). Take \(k=1\), \(\phi(v)=v^2\), \(f_a(v,z)=0\), \(L=2\), and any positive rational noise width. The convexity and curvature premises hold. The interiority premise that every optimal core is interior is vacuous. No optimal-flow output exists. The TU theorem at sections/08-integer.tex:418 does explicitly require nonemptiness.

Repair: say that the flow model is a core–recourse instance with nonempty \(Y\), or run one exact feasibility LP and return an infeasibility result before applying the optimization theorem. Integral network feasibility makes the latter polynomial in the binary input. This is a scope omission, not a limitation for feasible flow instances. If the root treats nonemptiness as an already explicit inherited global premise, only the cross-reference clarification is needed.

**N2 — Minor missing proof case: parallel-arc short cycles.** Appendix F:493–496 proves necessity of potentials by discussing simple residual cycles of length at least three and then the two-cycle formed by both copies of one original arc. A two-cycle using two different original arcs, which is allowed with antiparallel or parallel residual arcs, is not explicitly covered. A self-loop is also omitted if the network definition permits one.

Repair the sentence to cover every residual simple cycle that uses at most one copy of each original arc: augmenting one unit is feasible and changes the objective by exactly the cycle cost, so optimality makes that cost nonnegative. The only special cancellation case is the pair of forward and backward copies of the same original arc, whose cost is nonnegative by convexity. This also handles one-arc loops. The theorem is correct; its proof needs this short case completion.

**2. Known pending items, distinguished from new findings.**

These are already in the early reports or integration contract. They remain visible in the frozen snapshot. The complete appendices repair several proof mechanisms even where the main prose has not caught up.

| Item | Exact frozen location | Assessment and required integration |
| --- | --- | --- |
| K1: shared-root value output | sections/08-integer.tex:69–74; model at sections/02-model.tex:265–269 | The solver statement still gives the value only through its own isolator. Appendix F:249–265 actually constructs \(h(T)/q_0=f(r(T))\bmod P\). Return this map at the stored root and retain the value isolator as auxiliary data. The proof already supplies the correction. |
| K2: deformation at zero | sections/08-integer.tex:83–87 | “Every value of \(\varepsilon\)” is false at zero. Say symbolic or nonzero \(\varepsilon\). Appendix F:34–36 uses the normalized \(z=1/\varepsilon\) equations; its quotient lemma, which allows every finite \(z\), is correct. |
| K3: arbitrary projections and convergence | sections/08-integer.tex:88–96 | The projection statement needs a good form and the convergence statement needs a convergent subsequence. Appendix F:57–64, 160–246 now supplies the rejection, recovery, feasibility, and compactness arguments. |
| K4: affine empty zero sets | sections/08-integer.tex:408–410 | The unqualified distance inequality is false for empty zero sets and must use nonzero linear coefficients in its nonempty case. Appendix F:795–817 correctly proves and uses both cases. |
| K5: TU inherited input model | sections/08-integer.tex:417–424 | Explicitly inherit the fixed-degree rational polynomial, core box, curvature, scale, and encoding premises of the flow model. Appendix F:504–507 uses that intended model; it does not justify arbitrary unencoded convex costs. |
| K6: potential bit lengths | sections/08-integer.tex:229–238; Appendix F:497–499 | The real certificate is correct for general convex scalar costs; polynomial bit length additionally requires polynomial-length rational unit marginals. That premise holds in all actual polynomial applications. |
| K7: precision terminology | sections/08-integer.tex:483–484; Appendix F:929–931 | The stated feasible objective-gap evaluation alone does not establish distance to the stored optimizer, as the model's \(q\)-bit evaluation requires. Add component point-distance refinement with an \(O(\log(n+1))\) allowance, or name the weaker evaluation explicitly. The interior-flow statement at 283–295 should also state its available refinement bound. |
| K8: certified empty core | sections/07-recourse.tex:193–204; Appendix E:138–143 | The common proposition still sets \(\varepsilon_j=2E_j=0\) for \(k=0\) while using oracle accuracy \(4^{-j}\). Define \(\varepsilon_j=4^{-j}\) in that case, or separate it from the positive-core proposition. Appendix E:352–358 independently uses the correct \(h^2\) incumbent error in the empty-core stopping proof. |
| K9: small exceptional cases | sections/08-integer.tex:165–169, 454–466, 533–537 | Impossible label restrictions should be recognized before the ordered-bounds oracle call and assigned \(+\infty\); the minimum of an empty list is \(+\infty\). The all-fixed strong-field case and zero-row lattice case need their direct branches before maxima are taken. Appendix F:359 and 982 give the intended conventions or branches. |
| K10: generic fallback format | sections/03-counting.tex:524–529; Appendix A:428–492; Appendix E:61–68 | The frozen fallback still returns separate scalar isolators. The accepted tensor conversion in fallback-shared-root-sol.md has not appeared in the frozen proof. It must be integrated and its base-only multiplier included before selecting the recourse samplers. |

The root's additional continuous-recourse wording fixes remain at sections/07-recourse.tex:90–93 (certificate size versus verification work), 402–404 (the residual Hessian needs the sum-of-squares certificate, rather than the objective), and 437–439 (the general certified oracle need not arise from a convex residual objective). They do not invalidate the intended continuous theorem.

The quartic lattice statement is a proved restricted result, not a failed fixed-degree theorem. The accepted fixed-degree and explicitly listed piecewise-polynomial extension is still absent from this snapshot. B10's standalone conditional-count bridge and X16's standalone flow-core deterministic-error bridge also remain integration/coverage tasks rather than proof defects in the present results. The shared core search provides their required inequalities.

**3. Joint critical-limit solver: independent proof verification.**

I verified Appendix F:25–345 directly. Its construction avoids the degree product from separate-coordinate elimination and is not relying on the generic fallback conversion.

The equations \(g_i=y_i^a+(z/D)\partial_i f_\Phi\), with \(a=D-1\), have monic, pairwise coprime pure-power leading monomials in every degree-compatible order. The derivative degree is at most \(d-1<a\). Buchberger's coprime criterion proves the quotient basis and every finite \(z\)-specialization in lem:int:quotient, including \(z=0\). This is distinct from the invalid original \(\varepsilon=0\) specialization in K2.

Memoized reduction at Appendix F:45–51 and 87–89 is valid: every reduction strictly lowers total degree, and \(R=r(a-1)+1\) covers multiplication of every basis monomial by every coordinate. It computes all required multiplication matrices over \(\mathbb Q[z]\) without enumerating reduction paths. Simultaneous triangularization in lem:int:triangular gives common zeros with quotient multiplicities, even for a nonradical algebra.

The leading-coefficient argument at Appendix F:120–158 correctly distinguishes bounded vector branches from poles. For generic \(\lambda\), every pole contributes its full leading valuation, while bounded branches contribute their projected limits. Consequently

\[
c_\kappa(\lambda,T)=C(\lambda)
  \prod_{v\in\mathcal L}(T-\lambda^{\mathsf T}v)^{\mu_v}.
\]

The generic calculation forces \(\kappa\) to be an integer and then extends as a polynomial identity in independent form coefficients. A bad specialized form can hide a pole; the proof never uses the generic factorization for such a form. The deterministic list has more entries than the union of the at most \(N\) pole-hiding and \(\binom N2\) collision conditions, each a nonzero polynomial of degree at most \(r-1\). Thus lem:int:forms covers complex poles and complex limit collisions.

Recovery at Appendix F:170–192 differentiates in independent coordinate directions, rather than just in the moment parameter. Division by \(G=\gcd(p,p')\) cancels exactly \(\mu_v-1\) copies of each distinct projected limit. At \(\alpha_v=\lambda^{\mathsf T}v\),

\[
(p'/G)(\alpha_v)\ne0,\qquad
(b_i/G)(\alpha_v)=v_i(p'/G)(\alpha_v).
\]

The contribution from the derivative of \(C\) vanishes at the remaining simple root. Characteristic-zero multiplicities do not disappear. The modular inverse therefore returns all coordinates of one limit from one root. A real root yields real coordinates because the recovery maps are rational.

Lemma lem:int:limits does not silently assume that real critical-point sequences already belong to a fixed convergent Puiseux branch. Its evaluation-vector argument gives the characteristic equation for each real critical point. Taking the normalized leading limit for every rational form and using polynomial density forces the entire limiting vector to equal a member of \(\mathcal L\). This is a useful complete argument.

The correctness proof at Appendix F:233–246 takes a convergent subsequence of deformed minimizers on the compact box, passes to a fixed face, and uses uniform objective convergence to obtain an original global minimizer. A good enumerated form recovers it. Bad forms need not correspond to original critical limits, but all accepted reconstructed points are explicitly checked for box membership before comparison, so they cannot beat the true optimum incorrectly.

Value composition and comparisons at Appendix F:249–265 are also sound. The resultant of \(P(T)\) and \(q_0W-h(T)\) is nonzero and has degree at most \(\deg P\). Matching the selected value to its isolated root requires only polynomially many separation and evaluation bits. Isolating the squarefree product of two value polynomials decides equality as well as strict order without constructing a common field. Within the winning component, the value map \(h/q_0\) is already available and must be retained for K1. Clearing coefficient denominators makes the returned \(P\) an integer polynomial without changing roots or coordinate maps.

**Cost and output bounds.** Appendix F:274–330 keeps dimension in exponential factors and coefficient length in a fixed polynomial. The number of memoized monomials is at most \(2^{Dr}\), matrix dimension is \(N=(D-1)^r\), normal-form parameter degree is \(O_d(r)\), and normal-form coefficient length is \(O_d(r(H+\log(s+1)))\). The moment coefficients need only polynomially many bits in \(r\). Determinants use tensor interpolation in three variables; their number, degree, and coefficient heights are polynomial in \(N,H,r\) with absolute exponents. Modular inverses, objective composition of fixed degree, resultants, isolation, comparison, and refinement preserve that form.

The explicit ledger has enough slack: its \(U^{5010}\) estimate, for \(U=2^{Dk}(H+q+d+2)\), is bounded by the displayed \(C_d2^{10000Dk}(H+q+1)^{10000}\). The specified integer, determinant, interpolation, subresultant, and Sturm routines are all polynomial in their explicitly bounded input lengths. Enlarging the effective constant once for mixed-label comparisons is allowed; the same enlarged constant must be used in the component weights before noise is specified. There is no \(H^k\), noise-bit-dependent degree, or hidden \(c^{k^2}\) conversion in this proof.

The root polynomial degree is at most \((D-1)^k\), while coefficient and endpoint bit lengths can be \(c_d^k\operatorname{poly}_d(H)\). This is a representation-degree bound, not an assertion that the polynomial is minimal or that its coefficient heights are independent of the sampled bits. Arbitrary refinement is \(c_d^k\operatorname{poly}_d(H+q)\). Coordinatewise tolerances need the usual extra \(O(\log(k+1))\) bits for the theorem's Euclidean point-distance statement; the polynomial bound absorbs them.

Corollary cor:int:mixed-solver correctly retains only the winning label and re-isolates its roots in their own polynomials. Comparison precision for discarded competitors therefore does not inflate the winner's output. No part of this proof gives efficient exact comparisons for a sum of unrelated component values.

**4. Continuous recourse and active-stratum release.**

The conditional-value proof at Appendix E:114–129 uses fixed residual feasibility exactly where required. Minimization preserves upper coordinate curvature because the indexing residual set does not change along the coordinate segment. It also preserves the uniform core Lipschitz bound on every queried closed restriction. No residual convexity is used there.

The search proof at Appendix E:138–190 charges adaptive retained cells to true near-optimal points of a deterministic full grid. Conditioning on residual noise leaves independent core coefficients. The exact and certified interval lengths are respectively \(L(1+k/2)h\) and \(L(1+k)h\), giving the stated \(Q_{\rm ex}\) and \(Q_{\rm ap}\), including the finite atom term when \(M\ge2^J\). The \(k=0\) discrepancy is K8; it does not affect this positive-core argument.

The slab proof at Appendix E:195–211 excludes every residual point outside the patch and uses certified lower values with the full core-hull width. It omits slabs when the patch reaches an original endpoint. The sign and Hessian proofs at 214–235 fix only contained original bounds; all fixings hold simultaneously for every global optimizer. A positive Hessian test produces a unique globally optimal patch minimizer because global containment was established first.

The convex oracle proof at Appendix E:240–267 needs residual convexity, not a strong modulus. Its tangent bound is checkable by rational evaluation and endpoint choices. The smoothness argument uses \(K_f\ge1\), takes a feasible segment toward the tangent minimizer, and makes the tangent gap at most the requested accuracy. The general theorem remains relative to its supplied certified oracle; the tangent certificate is the concrete convex specialization.

The ambient stopping proof at Appendix E:342–385 is correct, including its special \(k=0\) incumbent allowance \(h^2=4^{-J}\). Growth gives patch containment; the slab margin exceeds the Lipschitz allowance; all nonzero active gradients are fixed; two-sided growth on the remaining original face gives Hessian at least \(2g_0I\). The base-selected thresholds and finite-law tails at 276–299 and 388–425 make fallback probability at most \(1/(2B)\). Thus the empty-core theorem has a sound intended stopping proof even though its shared search proposition still needs K8.

For core-only noise, lem:app:rec:lift at Appendix E:479–518 correctly proves a unique Lipschitz residual selector, differentiable conditional value, and full-growth lift. The active-set boundary construction at 558–616 is closed and semialgebraic. Its image has dimension at most \(q-1\); the fixed-block formulas use a one-variable middle universal block, which is why the \(O_d(n^3)\) exponent claimed there is sufficient. The polynomial product contains each exceptional image, and the cube-jitter proof at 618–635 accounts for every grid atom.

The release proof at Appendix E:638–713 is complete. Stable residual status gives a smooth stationary branch for the strictly interior residual coordinates. Each active multiplier is a nonnegative smooth function on a two-sided ball in the free core directions, with Hessian bound \(K_\lambda\). Zero multipliers have zero gradient. Small positive multipliers satisfy

\[
\|\nabla\lambda_i(a)\|^2\le2K_\lambda\lambda_i(a),
\qquad
\|B\|^2\le2n_RK_\lambda\theta\le\mu g/2.
\]

The first Schur complement has core block at least \(2gI\), residual block at least \(\mu I\), and controlled mixed block. Restoring eliminated residual coordinates gives the displayed \(\nu I\) bound on the full released block. The proof permits releasing many weak or zero multipliers simultaneously, not only one at a time.

At Appendix E:764–781 all active core normals are fixed before applying this release lemma. The \(q=0\) optimal core face is handled separately by the residual modulus. The remaining Hessian test has slack because \(\nu\ge4g_*\). This resolves the one-sided core-boundary obstruction and does not infer a residual multiplier margin from the tube event.

The rank-separation proof at Appendix E:442–468 is correct for fixed positive semidefinite quadratic corrections. It does not conflict with the rank-\(k\) convexifier available under a uniform residual modulus. The examples at 792–866 correctly illustrate changing feasibility, grid rounding error, flat and strictly convex residual fibers without a modulus, and weak residual multipliers.

**5. Integer, flow, TU, and component compositions.**

Native label exclusion at Appendix F:354–372 covers all competing labels by the coordinate restrictions even under coupled feasibility. The stopping constants at 375–391 use full point growth and integer unit separation; a growth-only event suffices for expanded completion. The implicit alternative at 433–464 correctly adds a core active-gradient event and uses the winning label's slice only. All restrictions require exact global values and attaining labels, not feasible upper values.

The exact separable-convex integer oracle bridge at Appendix F:467–481 has the needed scope: fixed integral TU feasibility, finite native intervals, explicit fixed-degree rational scalar costs convex on the whole real interval, arbitrary tightened integer bounds, and rational linear terms. Tangent extensions preserve convexity and permit rational evaluations outside native bounds. The cited scaling routine requires exact optimal extreme-point LP solutions, which the proof expressly includes. Capacities enter its running time through binary lengths and logarithmic scaling; repeated unit augmentation is not claimed to be the oracle.

The flow chart family at Appendix F:518–536 is fixed before sampling and includes every feasible label and structurally valid tree. Shortest paths with zero-cost cycles still have a tight spanning arborescence reachable from the added source: choose one by graph search in the tight subgraph rather than relying on a predecessor tie rule. Chart coefficients have base-polynomial length because labels and path lengths do. Cross-label gradient images are included in the exceptional set at 552–565; a chart from one label is not incorrectly paired only with that label's gradient.

The interior-flow stopping argument at Appendix F:577–592 uses projected core growth, not full point growth on tied flows. Every flow attaining the value at an interior optimal core gives a stationary smooth slice. The Hessian bound transfers proximity of the core to a chart zero set into proximity of the noise to its gradient image. On the good event the entire retained hull misses the zero sets. Identically zero reduced costs pass; each other chart has a constant positive sign on the connected hull. The base choices at 567–575 make the fallback contribution polynomial with polynomial sampling bits.

The proximity proof at Appendix F:601–623 is sound for TU systems. A conformal minimal-support kernel vector is a circuit with entries \(0,\pm1\); subtracting integer multiples gives an integral conformal decomposition. Each circuit leaving the closest optimal-face point must violate one tied interval at its endpoint. Charging multiplicity to that endpoint gives \(\|z-\bar z\|_1\le n_R\sum_i\operatorname{dist}(z_i,I_i)\).

The optimal-face proof at Appendix F:637–663 keeps both terms needed to control competitors. Adjusted costs are constant on tied integer intervals and have first outside penalties. The derivative minimum is over every feasible tied flow. The proximity factor \(n_R\) multiplies the mixed derivative allowance for losing labels. Taylor's inequality then gives a strictly positive outward-normal penalty under (b) and (c), so no global optimizer is lost when the core is fixed to its original face.

The derivative oracle at Appendix F:670–679 is valid. Equality at three integer points plus real convexity makes the adjusted cost constant on the entire interval. The inward derivative has nonnegative second derivative there because the original scalar Hessian is nonnegative on the feasible core side and vanishes at the face. Two-point intervals use affine interpolation and singletons are substituted. The resulting derivative minimization is within the exact separable-convex TU/flow oracle's scope. Checking at most \(d+1\) representative integers suffices for the required polynomial identities.

Boundary stopping at Appendix F:735–792 correctly has three distinct events. The canonical restricted-face optimizer and its entire tied-flow set are independent of the normal noise coefficients, so the minimum inward derivative is a fixed offset plus one normal coefficient. The chart zero-set event uses only the free coefficients on each face. The value-margin lemma at 683–708 covers both nonempty and empty zero sets through a two-block formula for the positive minimum. Its coefficient-bit bound is \(f_d(k)\operatorname{poly}_d(I)\), which is correctly charged to \(J\), \(b\), and all sampled query data. The algorithm does not pretend that a distance tube alone gives a polynomial-length value margin.

The affine lemma at Appendix F:795–810 gives the sharper empty-set vertex bound and the nonempty-set path bound. The bilinear proof correctly replaces the general margin by a polynomial-length one and replaces derivative and outside-margin minimizations by linear flow and endpoint calculations. Thus the three regimes remain distinct:

| Regime | Sampling bits proved by the appendix |
| --- | --- |
| Ambient native recourse; interior core-only flow | \(\operatorname{poly}_d(I)\) |
| General nonlinear boundary flow/TU | \(f_d(k)\operatorname{poly}_d(I)\) |
| Bilinear boundary flow/TU | \(\operatorname{poly}_d(I)\) |

TU dual existence and the bounded vertex at Appendix F:834–869 are correct. After fixed columns and dependent rows are removed, every positive-width column supplies an adjacent-slope inequality, so full row rank excludes lines in the nonempty dual polyhedron. Its active basis has a TU inverse and its vertex coordinates are bounded by \(m\bar V\). The algorithm retains the basis symbolically; chart coefficients therefore depend on base labels and base marginals, not on the sampled rational core query. Artificial box rows choose a bounded dual vertex but are not substituted for original marginal inequalities. The conformal circuit proof and all-tied derivative argument transfer. The finite slack construction at 884–888 is a bijection, preserves TU, and adds zero-cost, zero-coupling coordinates without changing \(L\).

The strong-field proof at Appendix F:893–934 correctly uses pre-draw derivative enclosures. Bad-site events remain independent. Monomial supports are cliques, so substituting pinned bounds really separates the components. The weighted connected-set sum uses the true component algebra cost \(\prod_{i\in C}a_i\); an unweighted site estimate would not suffice. Every atom is solved exactly, and component value enclosures are added without expanding a global primitive element. K7 concerns only the claimed meaning of later point evaluation.

The lattice proof at Appendix F:939–982 correctly uses exact scalar forward differences, a semiconcave auxiliary envelope, unequal-width balanced meshes, original feasible witnesses, and one common grid denominator. It uses the original objective lattice \(1/[D_0(M-1)]\), rather than the auxiliary values or shift, which can have squared denominators. Its predetermined error is strictly below that lattice spacing. Row-range/noise magnitudes remain explicit in \(H_{\rm rat}\); binary capacity encoding is not advertised as an expected polynomial bound by itself.

**6. Status of every result in the assigned sections.**

The location in the middle column is the actual proof. An entry marked “not verified as frozen” is not a rejection of the intended result; the final column states the local dependency. “Verified under cited tool” means that I verified the manuscript's reduction and arithmetic contract but did no independent literature search.

| Result | Frozen proof location | Status |
| --- | --- | --- |
| lem:rec:value | E:114–129 | Verified. |
| prop:rec:search | E:138–184 | Not verified as frozen for certified \(k=0\): K8. Verified for \(k\ge1\) and exact mode. |
| lem:rec:exclusion | E:195–211 | Verified. |
| lem:rec:closure | E:214–235 | Verified. |
| thm:rec:qp | E:272–426 | Verified under exact convex QP and quadratic-face tools. |
| cor:rec:forest | E:428–439 | Verified reduction and bit interface under the cited forest-QP tool. |
| lem:rec:convex-oracle | E:240–267 | Verified under weak convex optimization. |
| thm:rec:poly | E:272–426 | Not verified as the full frozen shared-root fallback contract: K10. Intended theorem and separate empty-core stopping proof verified; K8 and the noted premise wording need integration. |
| prop:rec:rank | E:442–468 | Verified. |
| thm:rec:core-only | E:715–787 | Not verified as the full frozen fallback format: K10. Core-only stopping, bit budgets, and ordinary patch proof verified. |
| prop:rec:tube | E:558–635 | Verified under the stated QE and algebraic-tube tools. |
| prop:rec:release | E:638–712 | Verified, including simultaneous zero multipliers. |
| thm:int:solver | F:25–330 | Not verified as frozen output wording: K1–K3. Actual joint solver proof and effective degree/height/work/refinement bounds verified. |
| cor:int:mixed-solver | F:337–345 | Verified computation and comparison proof; shared-root output inherits K1. |
| thm:int:native | F:394–430 | Verified stopping and expected-work proof; frozen output interface inherits K1 and restriction conventions need K9. |
| cor:int:native-implicit | F:433–464 | Verified ordinary implicit proof and extra event; fallback interface inherits K1. |
| prop:int:hs | F:467–481 | Verified reduction and bit contract under the stated exact scaling and LP tools. |
| lem:int:potentials | F:484–499 | Not verified as an unqualified rational bit statement: K6. Optimality characterization verified with short-cycle completion N2. |
| thm:int:flow-interior | F:538–598 | Verified feasible-instance stopping and polynomial-bit budget. Frozen full contract needs N1, K1, and the explicit refinement interface in K7. |
| lem:int:proximity | F:601–623 | Verified for networks and TU systems. |
| thm:int:face | F:637–680 | Verified under the exact scalar/TU oracle contract. |
| thm:int:flow-boundary | F:735–792 | Verified feasible-instance stopping and parameter-dependent-bit budget. Frozen full contract needs N1 and K1. |
| cor:int:bilinear | F:795–825 | Verified polynomial-bit proof; frozen prose needs K4 and its output inherits K1. |
| thm:int:tu | F:830–888 | Not verified as an unrestricted displayed model: K5. Intended fixed-degree transfer proof verified; output inherits K1. |
| cor:int:tu-ineq | F:884–888 | Verified finite-slack reduction under the intended nonempty fixed-degree TU premises; inherits K5 and K1. |
| thm:int:strong-field | F:893–934 | Verified exact component optimization and weighted expectation. Not verified as the model's point-distance evaluation contract: K7; output/empty case need K1/K9. |
| thm:int:lowrank | F:939–982 | Verified quartic positive-row theorem; displayed zero-row setup needs K9. Fixed-degree extension remains pending integration. |

**Status of appendix lemmas.**

| Result | Frozen location | Status |
| --- | --- | --- |
| lem:app:rec:stopping | E:335–385 | Verified, including its separate empty-core error allowance. |
| lem:app:rec:lift | E:479–518 | Verified. |
| lem:app:rec:core-tails | E:520–555 | Verified under the finite-tail and nonsingular-zero tools. |
| lem:int:quotient | F:69–90 | Verified for normalized equations. |
| lem:int:triangular | F:100–117 | Verified. |
| lem:int:leading | F:131–157 | Verified as a polynomial identity in independent form coefficients. |
| lem:int:recovery | F:164–192 | Verified for good forms. |
| lem:int:limits | F:195–216 | Verified. |
| lem:int:forms | F:219–230 | Verified. |
| lem:int:values | F:249–265 | Verified; retain the computed value map for K1. |
| lem:int:cost | F:268–300 | Verified with the Euclidean precision allowance stated in this report. |
| lem:int:budget | F:303–330 | Verified elementary ledger; use one final enlarged constant consistently. |
| lem:int:label | F:354–372 | Verified; its \(+\infty\) convention is explicit. |
| lem:int:native-stop | F:375–391 | Verified. |
| lem:int:face-general | F:626–663 | Verified. |
| lem:int:margin | F:683–708 | Verified, including empty zero sets and vertex faces. |
| lem:int:normal | F:711–732 | Verified; no conditioning on a selected random flow. |
| lem:int:affine-margin | F:795–810 | Verified. |
| lem:int:tu-dual | F:834–869 | Verified. |

**Verification record.** I performed scoped source reads with cat, sed, nl, and rg; calculated the listed hashes with sha256sum; and checked the inequalities, algebraic identities, oracle reductions, and probability budgets analytically. A report-only Python check passed: all 46 result-status rows are present, 98 inline and 3 display math delimiter pairs match, whitespace and control-character checks pass, and all seven inspected source hashes plus the manifest hash match the report and frozen manifest. No live TeX, snapshot, historical note, or other report was edited. No compilation, literature research, optimization diagnostic, saved experiment, project-wide verification, CI inspection, commit, or delegation was performed.
