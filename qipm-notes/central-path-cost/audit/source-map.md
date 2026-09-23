# Source map and staged development plan

Scope: a standalone mathematical paper on the cost of centrality in a specified Hessian metric, with primal–dual completion as an essential distinction. This is an author audit, not manuscript text. All paths below are relative to the repository `notes/` directory. Repository status labels are evidence of earlier review, not substitutes for checking proofs.

## Stages and review contract

1. **Foundations and exact metric benchmark.** Definitions, prior geometric work, Dikin conversion, exact box/matrix-ball/Jordan-interval distance, scaled product allocation and construction. Files: `sections/01-foundations.tex`, `sections/02-exact-distance.tex`. Theorem proofs are complete in this stage. The abstract is explicitly a stage-one abstract and is replaced in stage 5.
2. **Sharp standard centrality and finite sequences.** Exact central velocity, effective spectral rank and decay profiles, Gamma-r upper bound and extremizing profiles, exact same-accuracy scalar dilation, dyadic multiscale family, arbitrary-label metric-tube/decrement lower bound, unequal factor scales. Resolve all constants and finite-input conventions.
3. **Dependence on the barrier.** Fixed scalar profiles, differential envelope and C_sc; canonical cube barriers; facet-regular coupling; exact-optimal dense and radial coupled barriers; dyadic discrete persistence. Include proof of any new matching coupled upper bound only after independent review.
4. **Primal–dual completion and formulation dependence.** General orthogonal speed identity and gap-set lower bound with exact attribution; effective-support counterexamples; three distinct movement scales on the same box LP. Include exposed-support-rank and dimension-only movement statements with complete proofs if used; explain which parts concern choice of formulation rather than centrality.
5. **Synthesis.** Final introduction, contribution statements, literature comparison, coherent theorem roadmap, conclusions, publication metadata, complete proof and cross-reference audit. Perform the user's five-independent-reviewer full-manuscript cycle after integration.

After each author stage the root dispatches five independent reviewers, assesses every criticism, assigns all valid repairs to a different author, repeats five-way review following any major criticism, and resolves remaining valid minor criticisms before proceeding. No stage is certified by this source map alone.

## Primary mathematical sources and inclusion decisions

All named dated files in the following table are in `workbench/active/`.

| Repository development | Content to retain | Stage and decision |
|---|---|---|
| `2026-09-04-spectral-ball-low-rank-objective-path.md` | Exact path, effective-rank velocity, accuracy and singular-weight distribution, geometric/polynomial decay, numerical-rank tails, distance, water filling, determinant-profile limitation | Stages 1–2. This is the long derivation source; later short notes supersede its older same-accuracy constant and label assumptions. |
| `2026-09-04-spectral-ball-sharp-subgeodesicity.md` | Gamma-r same-endpoint bound; same-accuracy factor; multiscale sharpness; arbitrary/backward labels; growing tubes; Newton decrement and feasible primal–dual residual conversion | Stage 2, core. Treat all contracts as theorem hypotheses. |
| `2026-09-04-jordan-spectral-interval-distance-centrality-tax.md` | All EJA types; scaled distances; common and unequal scales; activation order and exact fixed-scale-profile supremum | Stages 1–2. Include unequal-scale frontier, rather than silently restricting the general statement to equal scales. |
| `2026-09-04-exact-scalar-centrality-dilation.md` | Definition of c_star, attainment, strict rational enclosure, exact-coordinate same-accuracy comparison | Stage 2, with reproducible rational certificate. The numerical value alone is not a proof. |
| `2026-09-04-spectral-rho-geodesic-shortcut-algorithm.md` | Scalar endpoint search and explicit shortest path; charged spectral frame; limitations under affine constraints | Stage 1 geometric construction; stage 5 interpretation. Quantum hidden-sign appendices are outside this paper's mathematical objective. |
| `2026-09-04-sparse-box-lp-geodesic-centrality-tax.md` | Two-sparse-row box LP, dyadic weights, bit length, matched discrete primal centrality gap | Stages 2 and 4. Use the dyadic convention consistently when discussing encoding length. |
| `2026-09-04-sharp-separable-centrality-tax.md` | Fixed normalized scalar barrier; ordered-velocity condition; endpoint sharpness; profile-uniform C_sc; dyadic finite-sequence result; failure without monotonicity | Stage 3. For the nonmonotone example the scalar profile and parameter vary with r: nu_A=Theta(A^2); do not imply a fixed-profile contradiction to NN2008. |
| `2026-09-04-canonical-box-barriers-do-not-remove-centrality-tax.md` | Universal and entropic factorization; positive-branch speed monotonicity; product tax | Stage 3. Credit universal/entropic constructions to their primary literature. Product factorization is an elementary specialization. |
| `2026-09-04-genuinely-coupled-symmetric-box-barrier-tax.md` | First coupled examples; asymptotic facet construction | Stage 3 source history. Prefer the stronger exact-parameter/facet-regular results below, retaining any distinct example only if it explains a necessary hypothesis. |
| `2026-09-04-facet-regular-coupling-box-centrality-tax.md` | Persistence under convex coupling with bounded first/second derivatives on a full signed facet collar | Stage 3. This establishes a lower bound on the worst ratio, not a universal matching upper bound for this whole class. |
| `2026-09-04-exact-optimal-dense-coupled-box-barrier-tax.md` | Exact cube parameter for dense coupling; symmetry and boundary behavior | Stage 3. Compare with the fully signed-permutation-invariant radial construction; retain distinct assumptions/results. |
| `2026-09-04-exact-optimal-hyperoctahedral-box-barrier-tax.md` | F=U-lambda log(c-||x||²), lambda>=1, c-r>=4lambda, exact parameter r, arbitrarily loose additive certificate, lower ratio Gamma_r | Stage 3. Repository theorem only proves supremum >=Gamma_r; do not write a matching global upper bound without new proof. |
| `2026-09-04-exact-optimal-hyperoctahedral-box-discrete-tax.md` | Dyadic input, arbitrary labels, tubes/decrement, explicit noncentral route | Stage 3. Matched exhibited orders do not by themselves prove a uniform supremum upper bound for coupled barriers. |
| `2026-09-04-sparse-box-primal-dual-completion-tax.md` | Same family: Theta(r sqrt(log r)), Theta(r log r), Theta(r^(3/2)); arbitrary feasible dual certificate; direct slack lower bound and central upper path | Stage 4, core. Distinguish primal accuracy eps from full gap 2eps and fix starting dual point. |
| `2026-09-04-primal-dual-speed-splitting-product-ball-counterexample.md` | General whitened orthogonal projections; constant total speed; sparse support and all-positive perturbation; effective objective support; geometric weights (§8) | Stages 2 and 4. Classical total-speed identity receives attribution, new role is explicit allocation/counterexamples. |
| `2026-09-04-barrier-independent-primal-dual-dikin-lower-bound.md` | Any feasible endpoint of small gap for arbitrary LHSC cone barrier; active-face restrictions; failed parameter-only primal projection | Stage 4. Closely verify endpoint-set inference against NT2002 analytic-center/convexity statements; do not call the same-central-endpoint theorem new. |
| `2026-09-04-dimension-only-arbitrary-cone-primal-dual-movement.md` | Slack rank D+1, Psi_d parameter bound, coupled-barrier product-cone consequence | Stage 4 formulation subsection or self-contained appendix. Retain as an all-barrier contrast, not a centrality penalty. |
| `2026-09-04-spectral-ball-dikin-iteration-lower-bound.md` | Spectral determinant/rank-profile lower certificate and normalized sharp examples | Stage 2 corollary of exact allocation. The exact distance is stronger; avoid presenting redundant estimates as separate main contributions. |
| `2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md` | Support-idempotent determinant contraction, exact norm sqrt(Q), objective-gap lower bound with scale Delta_c | Stage 4 formulation subsection/appendix. This is the closest formulation-aware extension of primal distance. |
| `2026-09-04-spectrahedral-principal-minor-dikin-contraction.md` | Matrix specialization of the support-minor contraction | Stage 4 proof aid; subsumed by Jordan statement. |
| `2026-09-04-grouped-ball-short-step-iteration-lower-bound.md`, `2026-09-04-norm-tree-short-step-iteration-lower-bound.md`, `2026-09-04-psd-packing-geodesic-iteration-lower-bound.md` | Restricted-barrier examples showing grouping does not automatically reduce movement; ancestor/barrier-height certificates | Stage 4 concise examples under the general contraction theorem; reprove any quoted quantitative instance. Not separate centrality theorems. |
| `2026-09-04-selection-free-symmetric-cone-exposed-rank-frontier.md` and earlier Hermitian/PSD2/sequential variants | Exact minimum exposed rank for fixed cone dictionaries, topology/selection-free lift theory | Closely related but a distinct standalone paper. Here explain the conditional role of support rank; do not import a large topological theorem without its proof. State any numerical minimax only if its derivation is included or a public citable paper exists. |
| `2026-09-04-selection-free-exposed-rank-premium-counterexample.md` | Counterexample to a naive rank premium without selection assumptions | Stage 4 scope warning if formulation-frontier claims are mentioned. It rules out unqualified extensions, not the fixed-support-rank distance theorem. |
| `2026-09-04-arbitrary-factor-q2-lorentz-barrier-rigidity.md`, `2026-09-04-arbitrary-factor-wide-cap-hermitian-barrier-rigidity.md` | Exact restricted-barrier lift rigidity | Exclude proofs: a different primary question. Their unresolved narrow-cap seams must not become implicit assumptions of this paper. |
| `2026-09-04-symmetric-cone-exposed-rank-query-readout-boundary.md`, Hermitian/readout counterparts, product-ball/disk readout notes, `2026-09-04-psd-packing-work-iteration-composition.md` | Quantum state, query, output and resource-composition distinctions | Outside paper's result scope. Retain only concise interpretation that bounded movement and query cost are different resources; never multiply lower bounds without an independent composition theorem. |

## Supersession, corrections, and genuinely open boundaries

- `workbench/active/2026-09-04-research-closure-summary.md` is the latest high-level closure ledger. Its status claims do not settle priority.
- `workbench/active/2026-09-04-sparse-qipm-frontier.md` records the derivation/supersession chain. `2026-09-04-targeted-literature-screen-sparse-conic-qipm.md` records a targeted, explicitly non-exhaustive screen.
- Prefer c_star<69/50 to the older kappa_0=1.391010896... same-accuracy certificate. Do not claim uniqueness of the maximizer defining c_star; the theorem needs neither uniqueness nor a closed form.
- C_sc≈1.831856423 is sharp for the stated relaxed differential-envelope problem at its safe scale, not proved globally optimal for the fixed smooth scalar-barrier minimax.
- The general separable logarithmic tax needs the stated scalar monotonicity property. Do not erase that assumption under the phrase "arbitrary scalar barrier".
- The general facet-regular theorem preserves a lower bound. It does not prove a bound for every optimal, every coupled, or every symmetric cube barrier.
- The root supplied `audit/root-radial-upper.md` during Stage 1 as a proposed NEW uniform upper bound for the explicit radial coupled family. Stage 3 subsequently developed the proposal into the manuscript's endpoint and same-accuracy theorems; all five independent Stage 3 reviewers examined the completed proof and found no major issue. Minor Stage 3 precision repairs are recorded in `audit/workflow.md`.
- Later discrete proofs remove both start/end-label assumptions and label monotonicity. Use actual endpoint accuracy and analytic-center initialization to force progress. Growing-tube statements need their quantitative radius restrictions.
- The exact water-filling problem supersedes determinant rank-profile bounds as a characterization: there are profiles with positive exact distance while every determinant-profile positive part vanishes.
- NT2002's product theorem does not give parameter-only primal lower bounds. The explicit speed-splitting counterexamples are mandatory context for any barrier-independent statement.
- `research-archive/2026-09-research-cycle/superseded-corrected/` contains withdrawn/corrected oracle and central-Hessian statements. Those are not sources for the current geometric theorems. The large `paper/` concerns conditioning/access/readout; its quantum-specific claims are not imported into this paper simply because they involve central points.
- Open lift seams and unrestricted quantum runtime questions are not unfinished proofs in the present paper; exclude them from its theorem hypotheses and avoid promising their resolution as part of centrality geometry.

## Stage 1 implementation decisions

- Metric assertions allow arbitrary positive factor scales; self-concordant chord counts require scales >=1.
- For matrix balls use the real Hessian even over C. The Hermitian dilation contributes two copies of g''=b''/2. Repeated and zero singular values are handled almost everywhere, rather than assumed absent.
- Ordered spectra give contraction; equality for arbitrary non-coordered endpoints is NOT inferred from a zero/weak spectral lower bound. Center-to-point and coordered common-frame equality suffice.
- The weighted allocation theorem pools heterogeneous factors while retaining one common scale within each factor. This extends the explicitly written common-scale repository formula with the same proof and supplies the later unequal-scale setting.
- The unique object asserted is the scalar allocation. Ambient frame representations at repeated values need no uniqueness theorem.
- The generic chord count, product rule, and scalar coordinate change are explicitly attributed to classical geometry. No novelty claim is made at stage 1 before full literature synthesis.

## Stage 2 implementation and resolved details

- Added `sections/03-sharp-centrality.tex`, `03a-distribution.tex`, `03b-discrete.tex`, and `appendix-scalar-certificate.tex`. The current integrated draft is 20 pages. Later stage inputs remain intentionally absent.
- Centrality theorem uses arbitrary positive scales and explicit activation order. It covers arbitrary central subarcs, exact fixed-order supremum, finite cumulative-mass envelope, adjacent-exchange extrema, and the coordinatewise c_star accuracy comparison. Ties may be ordered arbitrarily for a valid bound; exact supremum allows strict thresholds. No global sharpness claim for c_star times Gamma.
- Unified exact-rank/nuclear-tail/L2-tail schedules under exact velocity and Q1/Q2 distribution formulas. Numerical-rank corollary explicitly assumes normalized max weight and 0<epsilon<=1. Decay statements explicitly require the finite truncation to contain the epsilon-dependent lower-bound index.
- NEW simple strengthening: exact allocation removes the determinant certificate's factor two. The old inverse-sqrt coordinate family defeats even this stronger certificate for sufficiently large rank. Root supplied the simplified uniform proof using B_r>=2(sqrt(r+1)-1); no asymptotic Stirling argument is necessary.
- Discrete theorem uses only the exact dyadic family requested, rounded cumulative rational exponents. A fixed cutoff floor(r^(2/3)) has threshold gaps >=log2, giving per-step clipped progress O(C sqrt(1+C)) even for growing tubes and jumps across clipping boundaries. Actual initialization and accuracy force progress. Label -infinity is explicitly permitted to include analytic-center initialization for a zero-radius exact-central tube.
- The unequal-scale discrete comparison explicitly starts at z0=0 and separately assumes reference-parameter crossing. It does not inherit the equal-scale output-forced label claim without proof. Objectives/scales in this construction are not claimed input-efficient.
- Conic residual transfer requires restriction up to an additive constant, not an arbitrary affine barrier offset. Its pullback explicitly equals grad F-w/mu under AB=0 and B*c=-w. Primal spectral embedding and arbitrary off-frame iterates are handled through the already-proved contraction and trace inequality.
- Both scalar c_star bounds have complete rational proofs. `scripts/verify_scalar_certificate.py` uses only Fraction, factorial and finite positive-series bounds. The script independently verified every displayed arithmetic margin and radical enclosure. It does not approximate transcendental values to certify inequalities.
- `scripts/verify_standard_geometry.py` is a numerical cross-check (not a proof): 80 random weighted-prefix profiles with all 120 five-channel order permutations, weighted sharpness convergence, and 401 scalar error/speed comparisons all passed. Weighted ratio approached 1.2734824164 at M=1000 against exact prefix target 1.2748644299.
- Root independently computed dyadic central lengths and endpoint distances at ranks 16,64,256,1024, consistent with the stated orders. This is supporting validation, not used by a proof.

## Stage 3 implementation and additional development

- Added `sections/04-barrier-dependence.tex`, `04a-coupled-barriers.tex`, and `appendix-barrier-profiles.tex`; extended the scalar certificate appendix/script. Integrated author draft is 34 pages. All five independent Stage 3 reviews are complete, with no major issue; the separate repair agent addressed all root-approved minor findings. See `audit/workflow.md` for the assessment and validation record.
- Normalized scalar theorem explicitly assumes standard self-concordance on the whole interval, positive Hessian, an interior analytic center, full positive gradient range, and positive-branch squared gradient norm at most one. Its proof establishes monotone unit-limit velocity and integrable step tails. Sharpness is for every fixed profile. The general closest-endpoint allocation uses existence and necessary KKT, NOT unproved convexity or uniqueness.
- Complete relaxed scalar envelope proof includes branch integration, dependence on the initial envelope value, exact piecewise formulas, C_sc<2, and a reconstructed admissible piecewise differentiable envelope. NEW root/author development proves that this envelope constant has a unique maximizing radius through opposite branch curvatures. This uniqueness concerns C_sc, NOT c_star. No claim of a globally sharp fixed-smooth-profile arclength minimax is made.
- The nonmonotone family is globally smooth from its explicit cosh definition; no unprovided smoothing/extension is needed. Full endpoint blow-up, gradient range, nu_A=Theta(A^2), and disjoint-window sharpness at sqrt(r) are proved.
- The exact dyadic family already used in the manuscript works for every fixed normalized scalar profile. The new corollary retains actual initialization/accuracy, arbitrary backward labels, and growing metric tubes; constants depend on the scalar profile. It does not promise a finite-arithmetic barrier oracle.
- Canonical cube factors and entropic parameter-one properties are proved and explicitly credited as elementary/prior specializations. Positive spectral-support transfer derives the trace Hessian by polynomial approximation and uses spectral contraction. It does not infer standard self-concordance of arbitrary spectral lifts from scalar self-concordance.
- Facet-regular proof covers a full signed facet collar, not only a vertex neighborhood. NEW root/author extension observes that its analytic-center-to-center lower construction immediately gives the same-accuracy lower bound by choosing the actual terminal gap and using strict objective monotonicity. The theorem supplies no matching upper bound for arbitrary facet-regular couplings.
- Dense rank-one quadratic and radial family parameter-r proofs are complete. The latter requires lambda>=1 and c-r>=4lambda, with c varying when claiming an unbounded additive sum-certificate overestimate. Castro–Cuesta diagonal parameter-preserving regularization is explicitly prior work.
- NEW radial development independently checked and included: global U''<=F''<=11U''/8; 0<=a'<=1/4; logarithmic effective-coordinate speeds in [7/10,5/4]; ordered auxiliary velocities. These prove a uniform endpoint bound sqrt(11/8)*(25/14)*Gamma_k and a same-accuracy bound with an additional (5/4)c_star. Active support k replaces ambient r in the upper bound, including inactive coordinates and off-active-subspace shortcuts. The prefactors are not claimed sharp.
- NEW full-family discrete strengthening: same exact dyadic data, same eps_r, all allowed radial lambda,c (even varying with r), growing tubes delta=o(r^(2/3)), and unrestricted actual-F route. Stop at T+log(5/4) to ensure accuracy. Uniform shifted-threshold speeds and the direct prefix bound force initial/terminal progress. This extends the earlier lambda=1 source with input-dependent gap scale.
- The vertex-singular c=r,lambda=1 example is retained concisely because its parameter r+1 and unused regularizing coordinate explain a boundary of the facet assumption; its distinct Gamma_(r-1) lower bound is proved.
- Added every-c_star-maximizer localization and stationary equation. Exact arithmetic verifies 4611/5000<v_star<9701/10000 and43/50<x_star<943/1000, plus all three elasticity exclusions. No c_star uniqueness claim.
- `scripts/verify_barrier_dependence.py` solves radial centers independently by nested bisection, checks their Hessian implicit derivatives against finite differences, metric/gradient/speed inequalities, three central-arc integrals, and the numerical scalar envelope. All 96 center checks passed; largest relative tangent error1.220053776769947e-9. This is supporting numerical validation, not a proof certificate. The extended Fraction script passed every exact displayed margin.
- Final author build had no undefined references/citations, overfull/underfull boxes, or LaTeX warnings. The incomplete abstract/author and future stage inputs are intentionally left to stage5 integration.

## Stage 4 implementation and completed independent review

- Added `sections/05-primal-dual.tex`, `sections/06-formulation.tex`, and `sections/appendix-formulations.tex`; integrated author PDF45pages. At author handoff the five independent reviews were pending. All five have since completed with no major issue; a separate repair agent addressed both root-approved minor findings and validated the build. Stage 4 is complete, subject to the later full-manuscript review; `audit/workflow.md` retains the historical handoff and review record.
- General negative-pairing conjugate convention, whitened projection split, Schur activity, primal/dual objective progress and convergent integrated gap allocation are fully derived and explicitly classical. The entire feasible gap-set theorem is explicitly attributed to NT2002 Theorem5.1(c), Theorem5.2 and Corollary5.1; proof includes the central supporting-hyperplane calculation. Ambient intermediate affine infeasibility is permitted for its lower bound.
- Product-ball homogenization uses the published NN1994 spectral-norm-cone restriction (printedp199 Proposition5.4.6(i)), not an illicit subtraction rule or new barrier claim. Exact ambient k+1 versus restricted k parameters and Hildebrand's cone lower bound (with k=1 orthant case separate) are stated. One-support and accuracy-dependent all-positive objectives demonstrate the precise primal projection limitation. Existing distribution/decay section is cross-referenced rather than repeated.
- SAME dyadic family, exact epsilon, standard-form costs and signs; start is the finite fullcenter eta=1, terminal eta=exp(T). Four movement rows have fixed endpoint versus whole-gap-set contracts explicit. Direct logarithmic dual-slack bound applies to every feasible terminal certificate. Primal central lower count uses the previously proved discrete potential, not arc length alone. Endpoint shifts and encoding B=Theta(r²) are proved.
- Weighted support-minor theorem includes exact Qalpha and determinant scale with alpha powers. Quadratic representation, trace/determinant AM--GM, arbitrary inactive fibers, approximate starts and bounded rounds are proved; fullcone asymptotic sharpness is separated from affine-slice lower bounds. Hauser–Güler classification receives its proper attribution. General lift topological and certificate-selection frontiers are excluded as planned.
- Dimension-only operational cone bound uses the root's simpler compactness argument M>=D+1. Product interior orthant section proves the charge even for coupled barriers; exact integer Psi envelope and classical primal–dual movement conversion are included. No primal metric conclusion is inferred from a parameter bound.
- Concrete grouped paraboloid and arbitrary real PSD columnpacking results use complete log-residual/determinant contraction; competitor completion variables remain free. Hadamard partial minimization proves the center, differentiated stationarity proves speed, and the speed limit proves exact restricted parameterH. This subsumes the older tube-only grouped theorem. All-parameter arc formulas subsume its older asymptotic normtree comparison.
- Normtree result includes positive Lorentz sheet, every internal node at leasttwo children, all-residuals-equal center, exact shape-independent speed, path-independent barrier-height lower bound, matched central route and heterogeneous entropy scale. Exact reduced parameter2b-2/2b-1 is proved in full. NEW proof repair beyond transcription: root-leaf sharpness uses an explicit ambient trial direction with root/selectedleaf entries1 and fixed descendants, avoiding the source's unquantified Schur-decoupling limit; all-internal sharpness uses the corresponding root-only trial direction. Root-cap combinatorial optimization and intrinsic-barrier floor concern formulation optimization rather than centrality and are not imported.
- All concrete matching chord orders are qualified uniformly for0<epsilon<=k/4; exact central arc formula holds all0<epsilon<k. Approximate starts/round caps are included through a single generic conversion.
- `scripts/verify_primal_dual_formulations.py` independently solves80 random full differentiated KKT systems; checks objective progress, orthogonality and Schur activity; verifies log-stable dyadic signs/terminal accuracy/full speeds at ranks4,16,64,256; checks80 dense support-minor arbitrary inactive fibers and finite-difference PSD Hessians; exhausts1100 Psi cases; and verifies four normtree shapes plus100 root Schur inequalities. All passed. It is a diagnostic, not a proof certificate.

## Final synthesis artifacts

Stage 5 adds `sections/00-introduction.tex`, `sections/07-conclusion.tex`,
complete front matter, and four primary finite-sequence literature
references. The earlier geometric prior-work subsection moved from the
foundations into the introduction; its exact NN2008 comparison and label
are preserved. No established theorem statement or proof was changed by
the synthesis author. The paper identifies Sergey Gusev as author based
on the existing `paper/main.tex`, without inventing affiliation or contact
metadata.

`figures/flattened-path.pdf` illustrates the existing exact box metric
with weights (1,exp(-6)) and terminal logarithmic parameter8.
`figures/dyadic-lengths.pdf` and `data/dyadic-lengths.csv` illustrate the
existing dyadic family at ranks8 through1024, starting at parametereta1.
`make_figures.py` constructs exact integer exponents and evaluates three
specified distances/lengths; the endpoint distance is explicitly not the
accurate-target optimum. All files are generated from formulas contained
in the paper and have no external repository dependency.

`README.md` describes standalone building, exact rational certificates,
numerical diagnostics, figure data and scope. The Makefile's optional
`verify` and `figures` targets retain configurable `PYTHON`; the local
repository requires the qipm interpreter. The author handoff does not
certify the subsequent mandatory five-reviewer full-manuscript review.

## Completed full-manuscript review and final artifacts

The final author-handoff statements above describe the state before review.
All five independent final round-1 reviews have now completed; root assessed
every report and found no valid major issue. The separate repair agent
resolved every accepted minor finding: standard-barrier scope in front
matter, integer rounding for generic movement counts, PDF metadata, and a
precise STOC2026 trust-region literature comparison. The mathematical
theorems, proof constants, verification scripts and figure data are unchanged.

The final qipm build produces a clean 49-page standalone PDF with resolved
references/citations and verified title, author, subject and keyword metadata.
Only generated Python caches inside this folder were removed, and future
caches are ignored. `audit/workflow.md` records all five reports, assessment,
repairs and completion; `audit/root-final-validation.md` preserves root's
independent checks and the final-resolution note. All five stages and the
integrated review cycle are complete, with root's final delivery inspection
remaining after this repair handoff.
