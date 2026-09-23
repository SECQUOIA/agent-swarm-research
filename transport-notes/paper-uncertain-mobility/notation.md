# Manuscript notation ledger

This ledger fixes notation for the completed manuscript and its staged and whole-manuscript reviews. Coordinator decisions and accepted snapshots are recorded in the [review ledger](reviews/README.md), with whole-manuscript findings in the [final adjudication](reviews/final/round-01/adjudication.md). If a symbol changes, update this ledger and every affected section together.

| Symbol | Meaning and restriction |
|---|---|
| Ω, Γ, s | Fixed bounded cross-section, connected closed one-dimensional wall, and wall arclength. Specify regularity in Stage 1. |
| A, P | Bulk area and wall length. Use no other quantity named A. |
| K | Constant adsorption affinity; dimensional length before nondimensionalization. |
| κ | Uniform positive lower bound on the integrated desorption rate, `∫Γ k≥κ`; render `\kappa`. |
| δ_* | Fixed sufficiently small bump-width factor in the shell proofs of Sections 03 and 04; render `\delta_*`. It is distinct from the rate anchor κ. |
| kω(s), kc(s) | Nonnegative desorption rate; adsorption rate is Kk. General realization ω or scalar offset c. |
| c, kc(s) | Canonical dimensionless ensemble: `c∼Uniform[-2,2]`, density `1/4`, `kc(s)=(c+cos s)²` on `Γ=R/(2πZ)`. |
| ξ_1, ξ_2 | Independent standard Gaussian amplitudes in the separate counterexample `g(s)=ξ_1 cos s+ξ_2 sin s`, `k=g²`; neither is the bulk area A. |
| u(y), V | Fixed bulk longitudinal velocity and stationary mean tracer velocity. Longitudinal wall advective drift is zero; reversibility refers only to the transverse process. |
| Z=A+KP | Equilibrium normalization. |
| χ=KV²/Z | Physical prefactor multiplying the scalar surface response. Reserve χ for this quantity; the notes often call it B. |
| Db, Dbˣ, Dsˣ | Bulk transverse, bulk axial, and surface axial molecular diffusivities. Any assumed relation between surface axial diffusion and D must be explicit. |
| D(s), M=∫ΓD | Tangential mobility field and its per-observation integral budget. Use nondimensional M in asymptotics. |
| d(s), ε | Normalized mobility shape and constant mobility, respectively. Uniform budget-M mobility is ε=M/P. |
| Hk,D, ak,D | Surface operator/form, with specified realization when needed. Render the form `\mathfrak a_{k,D}`. |
| Jk(D) | Extended scalar response defined by smooth variational tests; Jc(D) abbreviates the cosine ensemble. |
| h | Surface source solution: an L² inverse for positive-background D; for degenerate finite-response D, the Riesz representative in the scalar energy completion. |
| e_D, V_D, W | Smooth surface derivative preform and its minimal closure domain when closable; W is the separate completion in the reaction-plus-derivative energy for a finite-response Schur identity. |
| mathscr A_D, π | Nonnegative self-adjoint transverse generator and normalized stationary bulk–wall measure. |
| p, ρ | Bulk and wall concentration in the physical forward equations. |
| Dflow, Rbulk | Flow-induced dispersion and nonnegative bulk remainder: Dflow=χJ+Rbulk when justified. Render the remainder `\mathcal R`. |
| Y, Fq(M;Y), Gq(M;Y) | Observed information, scalar policy optimum over all nonnegative L¹ fields, and full-bulk optimum over closable physical fields. The observation law may depend on M. Y_t denotes the stationary transverse process separately. |
| Pq(M) | Predetermined scalar moment optimum: one D selected before c is observed. Render `\mathcal P_q`. |
| O(M) | Exact-observation scalar mean optimum. Render `\mathcal O`, not the order-bound symbol `O(·)`. |
| Q(M,Δ) | Equal-bin scalar mean optimum. Render `\mathcal Q`; reserve the energy-form notation `\mathfrak a` for its distinct purpose. |
| q, αq=(6q−4)/(q+4) | Fixed positive moment order and cosine grading exponent. Generic upper trials use max(0,αq). |
| mathscr J(W), mathscr J_I^D(W), mathscr J_I^N(W) | Unit-mobility source-response suprema on the real line and on an interval with Dirichlet or free endpoint traces. Render the function as `\mathscr J`; its whole-line source is an energy-dual functional. |
| C0 | Harmonic integrated inverse constant, πΓ(1/4)/(2Γ(3/4)). |
| Cpair(μ) | Whole-line quartic unfolding response; render `\mathcal C_{\rm pair}`. Do not use the same C for a concentration variable and this function. |
| mathscr J_a^quad(D), b_* | Whole-line quadratic placement response and the saturated absolute slope of its explicit optimal source field. Render `\mathscr J_a^{\rm quad}` and `b_*`; `a` is local quadratic curvature and `m` is its mass budget. |
| Cpl | Exact local quadratic-placement coefficient, 12(3/80)^(1/5). |
| Kq, Kcrit, Kobs, Kcoarse | Scalar asymptotic coefficients, with K distinguished from subscripted coefficients. |
| B(x,y), Γ(x) | Euler beta and gamma functions; render beta as `\Bfun` and do not use plain B for a physical factor. |
| r, R, ℓ, t, μ | Root distance, fold cutoff radius, local diffusion/placement width, signed distance in offset from a fold, and scaled fold parameter. Define each locally; no simultaneous conflicting use within a proof. |
| Δ=4/N, τ=Δ/M^(1/5) | Equal offset-bin width and scaled resolution, with integer N≥1. Bin endpoints are `-2+jΔ`, `j=0,…,N`; only the bin index is observed. Δ is not the Laplace operator unless its arguments make that distinction explicit. |
| Fcenter(η) | Unit-budget whole-line uncertain-center value, rendered `\mathcal F_{\rm ctr}(\eta)`; η is spatial uncertainty divided by placement width. |
| T_z(ν), H(τ) | Quadratic smooth-test response with center z and finite measure ν, rendered `\mathscr T_z`; exact global precision-crossover coefficient rendered `\mathcal H`. The measure is only a compactness device. Stage 06 proves the local value has an L1 minimizer and is continuous; no profile uniqueness or monotonicity in η is asserted. |
| V(M,I), c_I, a_I, η_I | Conditional scalar optimum in offset bin I, its midpoint, curvature `a_I=1-c_I²`, and scaled root uncertainty `η_I=2^(1/5)(Δ/M^(1/5))a_I^(-3/10)`. The allocation `m=M/2` follows from exact reflection symmetry for each bin. |
| W=Δ+M^(2/7) | Fold-bin parameter-neighborhood size in Section 06, explicitly local to that proof; distinct from the energy-completion space W of Section 01. |
| mathscr J_mu(nu), mathscr I_q(nu), S_q | Stage 03 scalar smooth-test quartic response for a finite measure nu, its parameter-integrated qth power, and its unit-mass L1 infimum. Render `\mathscr J_\mu`, `\mathscr I_q`, and `\mathcal S_q`. Measures are a compactness device, not a physical diffusion coefficient. The canonical supercritical coefficient `2^((11q-12)/7) S_q` passed the [Stage 03 review](reviews/stage-03/acceptance.md). |
| beta_q=(3q−2)/7, b_0=1/2 | Supercritical mass exponent and the cosine fold coefficient. The separate local abbreviation beta=q/4 in the tangent certificate is explicitly scoped there. |
| a_R | Amplitude of a normalized graded trial; avoids the bulk-area notation A. |
| g(s,c), I, varpi(c) | Generic C4 squared-rate family, compact parameter interval, and bounded parameter density in Section 04. Render density `\varpi` to distinguish it from bulk concentration p. |
| Jc^g, Pq^g(M), Gq^g(M) | Generic-family scalar response, predetermined scalar moment optimum, and physical full-bulk moment optimum. |
| delta_F(s), n_f | Arclength distance to the finite known fold-site set and its nonzero cardinality in Section 04. |

Use `∼` only for a proved ratio tending to one, `≍`/`\asymp` for two-sided positive constant bounds, and `O`, `o` with the limiting variables and fixed parameters stated. Moments are unrooted. A qth root changes exponents and coefficients; it does not change minimizers. Logarithms require a nondimensional argument.
