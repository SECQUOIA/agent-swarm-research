# Stage 2, round 1 — independent review 3

## Verdict

**No major mathematical issues found.** The new short-range sufficiency argument resolves the previous missing inward-tail control. The restricted-contour derivative argument, as supplied here, is sufficient for the claimed small exponential moment of the actual spin energy. In particular, it does not require a twice differentiable minimum cutoff or an identification of bond count with spin energy.

I reviewed `sections/microscopic.tex`, checked its dependence on the stage-1 criteria, and consulted the saved primary-source texts listed below. I did not read another fresh review, edit the manuscript, or delegate.

## Minor issue

**Qualify the scope of the random-cluster interpretation citation in the restricted-derivative proof.** The proof says that the exact random-cluster interpretations of the contour-interior sums are given in Section 3.8 of Borgs–Chayes–Helmuth–Perkins–Tetali. That section explicitly says that the contour partition functions do not in general equal ordinary random-cluster partition functions, because interfaces are excluded, and gives the identification for suitable simply connected interiors that embed in the infinite lattice. The manuscript allows every torus contour, including large interiors, in this step.

The proof remains valid through the alternative matching-label representation already cited in BCT equations (6.13)–(6.14). Its summation set is fixed, its summands are positive, and their logarithmic derivatives have the required geometric bounds regardless of whether the interior embeds in the infinite lattice. This is therefore an attribution/clarity correction, not a missing mathematical hypothesis. Explicitly state that the proof uses those matching-label sums for general torus interiors, and that Section 3.8 supplies ordinary random-cluster interpretations only when its geometric assumptions hold. A short explanation that the total contour area inside an interior is bounded by a constant times its available edges would make the uniform derivative bound especially transparent.

## Checks and derivations

### 1. Positive phase measures and cited finite-volume inputs

I checked the following locations in `sources/bct2012.txt`:

- Equations (6.4)–(6.5) give the positive partition `Z = q Z_ord + Z_dis + Z_tunnel`, including the ordered multiplicity.
- Lemma 6.1 gives the tunneling probability bound `exp[-c beta L^(d-1)]` for every fixed `d >= 2`, and coexistence ordered probability approaching `q/(q+1)`.
- Lemma 5.7 gives both `m_gamma >= 2 diam(gamma)` and `|Int gamma| <= m_gamma diam(gamma)/2`, with diameter at most `L` by definition.
- Equations (6.13)–(6.22) provide the positive matching-label sums and the exact activity ratios used in the manuscript.
- Appendix A explicitly states that its inputs apply on both sides of coexistence whenever (A.1) holds. For sufficiently large fixed `q`, this includes a fixed real neighborhood of coexistence.
- Equations (A.3)–(A.8) give the minimum cutoff, the convergence margin, and the finite-volume truncated free-energy estimate. Lemma A.1(i) gives the diameter criterion for an inactive cutoff.

I also checked Appendix B.1 and Section 3.8 of `sources/bchpt2022.txt`. Appendix B.1 supports the disordered stable-side use; Section 3.8 requires the qualification identified above. The normalization `Z_RC = exp(-beta dN) Z_spin` is correct independently of these contour conventions.

### 2. Restricted derivatives: the central new argument

The elementary derivative estimate is adequate even without phase stability inside a contour. For a positive matching-label sum `S = sum exp(F_j)`, the summand bounds `|F_j'| + |F_j''| <= C V_gamma`, where `V_gamma = O(|Int gamma| + m_gamma)`, imply

`|(log S)'| <= C V_gamma`,

`|(log S)''| <= C(V_gamma + V_gamma^2)`.

Since `V_gamma = O(m_gamma^2)`, the activity-ratio derivatives satisfy `|(log K)'| <= C m_gamma^2` and `|K''| <= C m_gamma^4 K`. No variance estimate for an interior physical phase is being assumed here: the coarse bound by the square of the available volume is enough.

The exponential cluster majorant absorbs all these polynomial factors. The quoted convergence criterion has a strict margin at sufficiently large `q`, so multiplying activities by a fixed `exp(rho m_gamma)` is legitimate. The fixed torus has finitely many individual contour types, while the cluster series can have repeated polymers; the bound on total cluster size covers the latter as well.

Before removing cutoffs, a minimum of the two smooth positive branches is locally absolutely continuous. Almost everywhere its first derivative is a branch derivative, hence is bounded by `C m_gamma^2 K'`. Integrating the differentiated cluster series against the uniform majorant correctly proves a volume-uniform Lipschitz bound for `-N^(-1) log Z'_i`, and hence for its limiting free energy. This step does not differentiate the nonsmooth minimum twice.

The Lipschitz estimate gives `a_i(beta) <= C |beta-beta_c|`. Because every torus contour has diameter at most `L`, all cutoffs are inactive throughout a suitably small interval of width `eta/L`. Only then are second derivatives taken. The smooth original activities coincide with the truncated ones throughout that interval and retain the same majorant, so the second derivative of the log partition function is `O(N)` there. I found no circular appeal to the desired physical-energy fluctuation bound.

The center estimate only needs accuracy `O(sqrt(N))`. A stable-side finite difference of size `eta/(2 sqrt(N))` lies inside the inactive-cutoff interval for every `d >= 2`. Its error from the second derivative is `O(sqrt(N))`, while the finite-volume contour correction contributes `O(N^(3/2) exp(-bL))`, which is negligible for every fixed dimension. The stable-side branch equality is enough; equality of the two metastable constructions on their unstable sides is not needed.

### 3. Natural bond parameter and transfer to the actual energy

For `lambda = log(exp(beta)-1)`, I obtain `beta'(lambda)=p` and `beta''(lambda)=p(1-p)`. Thus, if `F(beta)=log[exp(d beta N) Z_i(beta)]`,

`dF/dlambda = p F'`,

`d^2F/dlambda^2 = p^2 F'' + p(1-p) F'`.

The restricted fixed-event representation is exactly a positive sum of `exp(lambda B) q^k`, apart from the constant ordered color multiplicity. These derivatives are therefore the conditional mean and variance of the occupied-bond count. The crude bound on `F'` is `O(N)`; combined with the proved `F''` estimate, it gives the required `O(N)` bond variance in a two-sided window of width proportional to `N^(-1/2)`. Centering at `-pNu_i` instead of the exact mean costs only a bounded exponential factor. Taylor's theorem at both signs supplies the claimed absolute exponential moment.

The Edwards–Sokal transfer then uses a genuinely additional estimate. Given spins, `B` is binomial with `M=-U` trials, so `D=B-pM` has a uniformly bounded exponential moment on the `sqrt(N)` scale. Conditioning this unconditional estimate on a positive-probability bond phase event is valid by division by the event probability; it does not incorrectly assume that the conditional distribution remains binomial after phase conditioning. Both phase probabilities have positive limits because `q` is fixed. The inequality

`|U-Nu_i| <= p^(-1)(|B+pNu_i| + |D|)`

and Cauchy–Schwarz give precisely the physical-energy moment bound required by stage 1. This resolves the bond/spin distinction correctly.

### 4. Exceptional mass and arbitrary tuning

For `c_N >> N^(3/2)`, the logarithm of maximal secant bath amplification is `o(sqrt(N)) = o(L^(d/2))`. The tunneling cost is a fixed positive multiple of `L^(d-1)`. Since `d-1 >= d/2` exactly for `d >= 2`, including equality in dimension two, the exceptional reweighted mass tends to zero throughout the claimed dimension range. A prefactor in the tunneling bound has no effect. The positive phase measures may be defined in the spin–bond extension because the likelihood depends on the actual spin energy alone, and projecting the reweighted measure produces the correct physical spin marginal.

For necessity, I checked the one-sided transform argument against the real-temperature partition expansion in BKMS Theorem 1. Exponential tilting supplies a neighborhood-of-zero moment-generating-function limit; untilting gives vague convergence, and the independently known phase masses restore weak convergence. This does not assume a complex-temperature extension or bound individual signed terms by probabilities. The independent-set variance lower bound is valid, and its passage through the stable thermodynamic branches yields positive conditional phase variances. The stage-1 necessity theorem then applies to every admissible total-energy choice, rather than merely to the secant choice used for sufficiency.

### 5. Mean-field realization

I checked the direct minimum classification, including exclusion of a boundary minimum, exclusion of two equal larger coordinates by a negative exchange variation, the three scalar stationary roots, and the Hessians. The phase prefactor ratio is `sqrt[2(3-b)/(6-b)]`, and the ordered energy variance obtained from the tangent gradient and inverse Hessian is `J^2/[6(3-b)]`. The disordered spin energy has zero limiting variance on the `sqrt(N)` scale, but the necessity theorem only requires one phase to be nondegenerate. Thus extending the threshold theorem to `a=0` is valid.

The global occupation bound follows from the strict rate gap outside neighborhoods of the four minima; the boundary type bound supplies the missing Stirling prefactor after sacrificing part of that gap. The Voronoi partition then gives the stated uniform exponential moment, without an exceptional phase component. The Gamma addition preserves this bound. The interior density estimate follows from the quadratic upper bound on the Gamma log density and the Lipschitz spin-energy map, with the lattice sum canceling the occupation prefactor. I found no reliance on a global Gaussian-mixture ansatz.

Finally, integration of `K^(A-1)(T-U-K)^c` produces exponent `A+c` and Beta parameters `(A,c+1)`, as stated. The finite-sum CDF formulas and the interval-of-positive-log-likelihood total-variation formula are correct. The pure-spin case is appropriately handled by sums rather than shape-zero Gamma/Beta distributions.

## Verification limits

This review consisted of analytic rederivation and inspection of the cited saved primary sources. I did not run a new numerical calculation because the principal new short-range theorem rests on uniform analytic estimates, and a finite numerical experiment would not validate those estimates. No substantive defect or missing hypothesis was found in that theorem or the mean-field sufficiency proof.
