# Stage 5 independent adversarial review

I reviewed the frozen Stage 5 sources against `snapshot.json`; all recorded hashes matched. I read the Fourier section, observation-design appendix, abstract/introduction, discussion, integration files, added references, coverage map, and author report. I checked the accepted solution definition, bounded-test log equation, and half-moment estimate used by the new proofs. I did not read other current-round reports, contact other reviewers, change manuscript or supplement files, or run a shared build. This report concerns Stage 5 and its use of accepted prerequisites, not the separate whole-manuscript review.

**Result: 0 MAJOR issues and 1 MINOR issue.** The new theorem statements and their proofs withstand the adversarial checks below. One explanatory claim about the daughter endpoint overstates the identification limitation.

1. **S5-ADV-01 — MINOR: excluding an atom at daughter ratio one is not essential to structural identification under both daughter constraints.**

   **Location:** `sections/fourier-identification.tex:211–215`, following `thm:fourier-identification`; also the “strictly smaller daughter boundary” description in `development/COVERAGE.md:55`.

   The sentence “Strictly smaller daughters are essential” is too strong in this setting. An atom at one contributes zero directly to the exponent, but the simultaneous constraints `B((0,1])=2` and `∫θ B(dθ)=1` determine that atom indirectly. The following displayed mass identity already contains the missing information.

   To see this without any logarithmic moment assumption, allow the endpoint one and write

   \[
   \nu=\sigma(\log)_\#B=\nu_-+a\delta_0,
   \qquad \nu_-:=\nu|_{(-\infty,0)}.
   \]

   The one-sided uniqueness argument determines `ν_-` from the exponent on an interval. Since the zero atom contributes nothing to `1-e^y`, the two daughter constraints give

   \[
   \sigma=\int_{(-\infty,0)}(1-e^y)\nu_-(\mathrm dy),
   \qquad a=2\sigma-\nu_-((-\infty,0)).
   \]

   Thus `σ`, the zero atom, and the full `B` are still uniquely determined whenever `σ>0`. Equivalently, two candidate full jump measures with the same exponent differ by `cδ_0`; their total-mass constraints give `c=2Δσ`, while their exponential-moment constraints give `c=Δσ`, forcing both differences to vanish. For a concrete admissible expected daughter measure, `B=(1/2)δ_1+(3/2)δ_{1/3}` has both required moments, and its visible jump measure `(3σ/2)δ_{log(1/3)}` recovers `σ` and the missing atom by these formulas.

   **Suggested fix:** delete the necessity claim, or limit it explicitly to uniqueness for arbitrary finite jump measures without the daughter normalizations: an unrestricted zero-jump atom is invisible, which is why the bare lemma is stated on the open negative half-line. The manuscript can keep its current strictly smaller daughter model and theorem; no extension theorem is required. Adjust the coverage description accordingly. This is a minor defect because the actual structural-identification theorem on `(0,1)` remains correct.

The following checks produced no additional defects:

- **Fourier factorization and uniqueness.** The nonlinear forcing bound has the stated normalization and exponential rate. Bounded oscillatory tests require no initial or daughter log moments. Uniform convergence near zero supplies a continuous nonvanishing amplitude even for heavy initial log tails. The lower-half-plane sign and damping in `lem:one-sided` are correct; continuity at the boundary suffices for reflection across a zero boundary segment. The anchored continuous logarithm removes phase aliasing locally. Intersecting two candidate neighborhoods is sufficient for structural uniqueness. The zero-selection case correctly leaves the unused daughter law unidentified.
- **Structural identification versus sampling.** The variation-norm counterexample preserves both daughter constraints and has variation exactly four. It proves precisely the stated discontinuity, without asserting instability in every weaker topology. The four-component Hoeffding union bound gives `8 exp(-n ε²/4)`, and both quotient identities give the stated constants. At `t_n=log(1/ε_n)/ω`, the bias and amplified noise both have order `ε_n^(δ/ω)`; the signal condition eventually holds because `δ>0`. The zero-attenuation case is included. The manuscript distinguishes the observable finite-time sampling certificate from deterministic bias, pointwise exponent recovery from full noisy daughter inversion, and independent continuum samples from dependent physical particles.
- **Preparation constraints and tomography.** The affine-shell argument uses the strictly positive feasible point, full row rank, and `h≠0` correctly. The formula for `A_0`, the residual in the row space, and the sign of the skew correction all check out, including the zero-dimensional shell when `r=q`. The rank bound is only necessary. The continuum two-constraint family is expressly conditional, and its closed count equation is correct. Both dilution gauges, the nonnegative-parameter boundary qualification, all reconstruction identities, the finite-grid measurement count on an open unrestricted parameter set, and the deterministic error constants are correct. The finite-difference time balance is subject to the stated curvature window and endpoint qualifications.
- **Independent arithmetic checks.** Read-only Python checks reconstructed the shell representation for 720 random cases covering `1≤r≤q≤8`, including full-rank shells. The maximum absolute residual was about `1.3×10^-10`. Independent random-grid checks reproduced the kernel, linear-rate, and unknown-source tomography formulas to floating-point precision. These checks supplement the algebraic derivations rather than establish them. The accepted numerical supplement was not rerun.

The new literature positioning is appropriately narrow. The two-time quotient and distinguished logarithm are present in [Garnier, Section 2.2](https://arxiv.org/html/2405.10588v1). The independent log-size samples and Fourier denominator regularization are present in [Hoang et al., Sections 3.1.1–3.1.4](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf). The cited transform equations are present in [Doumic–Escobedo, equations (12)–(14)](https://arxiv.org/pdf/1510.03588). The asymptotic inverse setting is supported by [Doumic–Escobedo–Tournus (2018)](https://ems.press/content/serial-article-files/16864), and the short-time setting by their [2024 article](https://www.numdam.org/articles/10.5802/ahl.207/). The aggregation–fragmentation daughter-estimation comparison is supported by the [Mirzaev–Byrne–Bortz preprint](https://arxiv.org/pdf/1510.01355), with the published reference confirmed on the [author’s publication page](https://www.colorado.edu/amath/david-bortz/research-and-publications). The finite-stochastic/mean-field comparison is supported by the cited [D’Orsogna–Lei–Chou article](https://www.math.ucla.edu/~tchou/pdffiles/JCP_LEI.pdf). The classical-mixture context is supported by the [Brown–Donev–Bissett accepted manuscript record](https://research.manchester.ac.uk/files/27268202/POST-PEER-REVIEW-PUBLISHERS.PDF). Publisher access to the older McCoy–Madras article failed during this review; I therefore do not claim to have independently rechecked its full introduction or the older Patil/Lage proofs. This access limitation is not evidence of an attribution error.

No optional stylistic changes are requested. **Final count: 0 MAJOR, 1 MINOR. Recommendation: accept Stage 5 after correcting S5-ADV-01.**
