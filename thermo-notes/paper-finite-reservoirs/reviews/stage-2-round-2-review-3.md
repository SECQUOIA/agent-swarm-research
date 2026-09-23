# Stage 2, round 2 — independent review 3

## Verdict

**No major or minor issues found in the revised stage.** The new source-convention clarification and the expanded derivative proof are scientifically sufficient. The short-range threshold theorem now uses one consistent finite-volume contour construction, and its deductions do not depend on identifying that construction with the later modified one.

I independently rechecked the frozen `sections/microscopic.tex`, its stage-1 dependencies, and the relevant saved primary-source passages. I did not read another round-2 report, modify the manuscript, or delegate.

## Reassessment of the corrected short-range proof

### Consistent positive phase convention

The revised manuscript expressly adopts the BCT definitions of contours, interiors, exteriors, compatibility, restricted sums, and phase events. I checked BCT Definitions 4.1–4.4 and 5.4, the phase partition in (6.4)–(6.5), and the matching-label sums and activity representations in (6.13)–(6.22). The manuscript's ordered factor `q`, the tunneling event, and its temperature-independent events agree with those definitions. The statement that the later BCHPT convention is different is accompanied by an explicit refusal to identify the finite-volume events, so no estimate is silently transferred between the conventions.

### Stable-side identification within BCT

The stable-side identification added in this round is valid. Appendix A's assumptions hold on a fixed neighborhood of coexistence for sufficiently large fixed `q`. BCT Lemma A.3 identifies positive spontaneous magnetization with `a_o=0`. Therefore the disordered branch minimizes below coexistence and the ordered branch above it. Continuity forces equality at coexistence.

On the full torus, BCT A.1(ii) bounds either positive restricted partition function above by `exp[-N min(f_o,f_d) + O(N exp(-bL))]`, because there is no exterior boundary and the remaining maximand is at most one. The lower bound (A.9) applies to a minimizing branch. I rechecked (6.26)–(6.27): their interface-network estimate depends on the Appendix A bounds, the interface-counting bound, and the displayed inequality `q <= exp(2d kappa+d)`, but not on the ordered branch being the minimizer. That inequality has a fixed margin in a sufficiently small neighborhood of the large-q transition, since `beta_c=(log q)/d+O(q^(-1/d))`. Thus extending this particular estimate to the neighborhood is justified. Taking the thermodynamic limit in the positive partition decomposition gives the physical minimum free energy. Combining this with the exact random-cluster normalization gives the asserted equality with the appropriate stable BKMS branch, with no assertion about metastable continuation away from that side.

### Matching-label derivative bounds

The added summand formula records all temperature dependence explicitly:

`F_Gamma = -e_o n_o - e_d n_d - kappa M + c_Gamma log q`.

The configuration index and its integers are independent of temperature. Its ordered-component multiplicity has zero temperature derivative. The geometric bound on total internal contour intersections is valid for compatible matching contours in BCT's cube construction: only a bounded number of intersections can be assigned to one edge, and relevant edges are controlled by interior vertices and the bounding contour. This bound does not require a simply connected interior or an embedding into the infinite lattice.

Consequently `|F'_Gamma|+|F''_Gamma|=O(V_gamma)`, where `V_gamma=O(|Int gamma|+m_gamma)=O(m_gamma^2)`. Applying the exact positive-sum identities gives first log derivatives of order `m_gamma^2` and second log derivatives of order `m_gamma^4`. The conversion from log derivatives to `K_i''` adds a squared first derivative of the same order, so the displayed activity estimates follow.

The argument is now explicitly based on matching-label sums for general torus interiors. It no longer imports the ordinary random-cluster interpretation from BCHPT Section 3.8 beyond that source's geometric scope, resolving the source issue identified in the preceding round.

### Cluster differentiation and cutoff removal

The strengthened cluster majorant is supported by BCT (A.5)–(A.6); sufficiently large `q` leaves room for a fixed exponential factor in total contour size. It absorbs the polynomial factors arising from first and second derivatives, including repeated-polymer clusters.

The minimum cutoff is used only for an almost-everywhere first derivative and a Lipschitz estimate. Integrating that derivative against the uniform cluster majorant is legitimate. The finite-volume free energies have a common Lipschitz constant; their pointwise limits inherit it. Thus `a_i(beta)=O(|beta-beta_c|)`. The diameter cutoff criterion removes every cutoff in a real interval of width proportional to `L^(-1)`, after which the original smooth positive activities can be differentiated twice. This proves the `O(N)` restricted log-partition second derivative without differentiating the minimum twice or presupposing Gaussian energy tails.

The stable-side finite difference used to identify the first derivative has size proportional to `N^(-1/2)`, which lies inside that interval for every fixed `d>=2`. Its two errors are `O(sqrt(N))` and `O(N^(3/2) exp(-bL))`. The latter is negligible. Accuracy `O(sqrt(N))` is exactly sufficient for the subsequent centered exponential moment.

### Bond fluctuations, conditioning, and physical spin energy

The revised text correctly says that the derivatives of the **logarithm** of the fugacity partition function are the conditional bond mean and variance. With `beta'(lambda)=p` and `beta''(lambda)=p(1-p)`, its second lambda derivative is `p^2 F''+p(1-p)F'`, hence `O(N)`. The conditional bond exponential moment follows by two real finite differences and the center estimate.

The binomial noise estimate is first established given spins, without phase conditioning. Its unconditional exponential moment remains bounded after conditioning on a bond phase event because that event has probability bounded below. The manuscript does not assume conditional binomial structure after imposing the event. Cauchy–Schwarz then transfers the bond moment to the actual spin energy. This supplies the exact physical-energy hypothesis of the positive-decomposition theorem.

The exceptional mass cost is `exp[-b L^(d-1)]`, while the largest reservoir amplification has logarithm `o(L^(d/2))` under `c_N >> N^(3/2)`. This comparison holds throughout the claimed dimension range, including the equality of exponents at `d=2`. Projection from the auxiliary spin–bond space gives the correct physical subsystem marginal.

## Stagewide consistency

The arbitrary-tuning necessity proof still uses actual spin-energy midpoint phases, not the positive contour decomposition used for sufficiency. The one-sided transform argument is adequate for weak conditional Gaussian limits, and the independent-set variance bound passes through the stable thermodynamic branches to give strictly positive phase variances. The stage-1 two-scale theorem therefore applies without imposing the secant calibration on necessity.

I also rechecked the mean-field part. The occupation Hessians and phase prefactors, the ordered nonzero energy variance, the global lattice Gaussian bound, the boundary-strip argument, and the positive conditional exponential moments are consistent. The pure-spin case has a degenerate disordered `sqrt(N)` fluctuation but a nondegenerate ordered one, which is sufficient under stage 1. The Gamma addition, continuous density bound, Beta conditional law, and finite-sum total-variation evaluation remain valid. Neither microscopic proof assumes that local weak limits alone supply inward tail control.

## Checks performed

This review used direct analytic checks and saved primary-source inspection of BCT's phase definitions, Appendix A, equations (6.26)–(6.27), and the BKMS partition input. No numerical calculation was used as a substitute for the required uniform estimates. I found no remaining source-convention mismatch, invalid differentiation, hidden signed measure, missing physical-energy transfer, or dimensional restriction beyond those stated.
