# Independent review: Stage 01, round 01, reviewer 5

Reviewer: `paper_reviewer_5`. Date: 2026-09-07.

**Verdict: no major issue found; two minor clarifications should be corrected before acceptance.** The mathematical comparison and its physical interpretation withstand the checks below. This verdict concerns Stage 01 only.

## Snapshot and independence

I verified every hash in the frozen manifest against the current files. The reviewed snapshot is `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`. I read the model section, author handoff, notation, bibliography, and scaffold/dependency material. I did not read any other report in this round or coordinate with another reviewer.

## Independent mathematical checks

- **Conservation and reversibility.** Integration of the bulk equation gives the negative of the wall exchange gain. Integrating the symmetric energy by parts independently gives the backward boundary condition `D_b ∂_n f=Kk(v−f_Γ)` and wall generator `(Dv′)′+k(f_Γ−v)`. The equilibrium weights and factors `K/Z` therefore agree with the forward equations. The constant-forcing identity is `∫Ω(u−V)=KPV`, as required for the common-constant gauge.

- **Dimensions.** The scalar response has dimensions length times time, the budget has dimensions length cubed divided by time, and `χ` has dimensions length divided by time squared. The stated conversion of a canonical scalar constant to physical diffusivity is consistent.

- **Weighted forms.** A positive floor allows the derivative-Cauchy argument used in the manuscript, even if `D` is unbounded above. Smooth functions have finite energy because `D` is integrable. The separate closure and energy-completion spaces are necessary and correctly distinguished. The product form is closed because the bounded-rate trace term is continuous in its product norm. Its compact disjoint-union state space has a fully supported reference measure, and smooth pairs supply regularity. The model does not impose equality between the two copies of the wall.

- **Coercivity and stationary variance.** The anchored wall estimate follows by writing `v=bar(v)+(v−bar(v))`; its constants can indeed be uniform over the stated rate class. Combining it with the bulk mean-zero gauge controls the mean-zero product norm under a positive floor. The finite-time covariance formula has the correct factor of two, and its spectral integrand increases with time even in the zero-eigenvalue case. The manuscript carefully claims a stationary variance limit rather than an unproved central limit theorem.

- **Schur completion.** Maximizing the surface variable gives `K[⟨kb−V,H^{-1}(kb−V)⟩−∫kb²]`. Its linear term is `−2KV∫(kh)b`, so the load sign and prefactor in the remainder are correct. For a degenerate but finite-response design, the extension `v↦sqrt(k)v` has norm at most one from the reaction-plus-derivative energy space to wall L². Consequently `w=sqrt(k)(sqrt(k)h)` obeys `||w||₂²≤k_max J`, making the bulk trace load bounded. This independently confirms that the finite-response extension gives a finite remainder without silently requiring an L² corrector.

- **Logarithmic estimate.** From `J≤C/m` one gets `||h′||₂≤C/m` and `||kh||∞≤C/m`. Positivity and fixed mass give `|ŵ_n|≤1`. The H^(-1/2) low-mode sum is logarithmic; the tail is bounded by `C||w||∞/N`. Taking `N` of order `1+||w||∞` gives the stated logarithm. Squaring the trace-load norm in the bulk quadratic supremum retains this logarithmic order, rather than its square. No derivative or upper bound for `D` enters.

- **Policies and optimal values.** Countable C¹-dense smooth cores give jointly Borel response functions; no measurable minimizer is needed. The scalar-to-physical inclusion and positive-floor mixture work in the correct directions. The mixture keeps the budget exactly fixed, and the quotient inequality gives the factor `(1−θ)^{-1}`. Minkowski for `q≥1` and subadditivity for `q<1` yield the displayed finite-budget comparisons. Choosing `θ=M` proves the asymptotic without assuming regular variation.

- **Observation-uniform bound.** For a bump of width `ell=M^(1/5)`, the numerator is of order `ell²`, while the two denominator costs are bounded by `M/ell²` and `ell³`; both scale as `M^(3/5)`. This yields `J≥cM^(−1/5)` for every admissible field, including spiky ones. The selected offset interval has probability `1/4`. The resulting error exponents and the claim that the mixture error `O(M)` is smaller are correct for each fixed positive `q`.

## Findings

### R5-01 — Minor: specify axial-diffusivity assumptions

**Location:** `sections/01-model-transfer.tex`, lines 233–241, equation `eq:molecular`; also the physical model's initial assumptions.

**Reason:** The model defines the rough tangential coefficient precisely but never explicitly requires `D_b^x` to be finite and nonnegative or `D_s^x` to be nonnegative and integrable. Those are the conditions needed for the stationary Brownian addition to have the stated finite second moment and for the conditional stochastic-integral argument as written. Calling them diffusivities conveys nonnegativity physically, but does not supply the missing integrability condition. This does not affect any theorem about `D_flow`; the isotropic case already has the needed integrability because `D∈L¹`.

**Remedy:** State `D_b^x∈[0,∞)` and `D_s^x∈L¹_+(Γ)` when invoking the molecular addition. Briefly note that stationary expected integrated diffusivity is then finite, so the stochastic integral is square integrable and the covariance vanishes as claimed. For ensemble comparisons retain the existing requirement that the molecular contribution be uniformly bounded.

### R5-02 — Minor: distinguish the zero-mode test from inverse spectral cutoffs

**Location:** `sections/01-model-transfer.tex`, lines 254–258, the explanatory proof of `eq:full-variational`.

**Reason:** The sentence saying that spectral cutoffs of `λ^{-1}g` give the reverse inequality “including an infinite value” needs a zero-mode qualification. Positive-spectrum cutoffs prove divergence from a nonintegrable positive spectral tail, but they do not capture an atom at `λ=0`. The identity itself remains correct: the preceding resolvent-regularization alternative includes that case, and the stationary spectral formula already handles it explicitly. This is a local exposition gap, not a defect in the theorem or its method.

**Remedy:** Add that if the orthogonal projection `g_0` onto the kernel is nonzero, the test `w=t g_0` has zero energy and linear gain `2t||g_0||²`, which tends to infinity. Then apply inverse spectral cutoffs on the positive spectral subspace. Alternatively give the regularized inverse test explicitly, which covers both cases at once.

## Citation and build checks

I inspected the primary open papers [Li and Ying, *On symmetric one-dimensional diffusions*](https://arxiv.org/pdf/1701.02411), particularly its discussion of Hamza's theorem, and [Gim and Trutnau's Dirichlet-form application](https://arxiv.org/pdf/1308.0234), which identifies the cited FOT process-correspondence theorem numbers. These support the use and identification of the standard results; they do not independently verify the manuscript's new transfer theorem.

A fresh build into an isolated temporary directory used `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=<temporary directory> main.tex`. It exited with status 0, produced an eight-page PDF, and left no warning, overfull-box, or underfull-box notice in the final log. No manuscript source was edited during review. Full-manuscript visual inspection and later literature/novelty review remain separate obligations.
