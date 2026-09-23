# Independent review: Stage 01, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Reviewed snapshot: `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`. I checked all nine file hashes against `snapshot.json`; all matched. I read the model section in full, the author handoff, notation ledger, bibliography, entry point, and applicable stage plan. I did not read other reviewers' reports or coordinate conclusions.

## Overall assessment

**No major issue found. Two minor corrections are requested below.** The central results M1–M4 are supported by coherent arguments under the stated rate, geometry, stationarity, and positive-mean-prefactor assumptions. In particular, the separation of the unrestricted scalar problem from the class of closable physical forms is meaningful and is successfully bridged by the budget-preserving positive-floor mixture. I do not certify any Stage 02 asymptotic or later measurable exact-observation optimization by this review.

## Independent mathematical checks

### Physical normalization and reversible realization

Integrating the forward bulk equation over the cross-section gives boundary loss `-K k p_Gamma + k rho`; this cancels the exchange term in the wall equation. The wall-to-bulk stationary density ratio is K. The total transverse reference mass is `Z=A+KP`, and the centered velocity has zero mean because `int_Omega(u-V)=KPV` and the wall contribution is `-KPV`.

The backward boundary condition also has the correct sign: integration by parts in `D_b int grad f grad F + K int k(v-f_Gamma)(V-F_Gamma)` yields boundary coefficient `D_b partial_n f + Kk(f_Gamma-v)`. Setting it to zero gives the condition printed in the manuscript. Dividing the energy by Z while using `L^2(pi)` leaves the physical backward generators unchanged; no extra factor of Z or K enters the wall diffusion term.

The dimensional response has units LT. Hence `chi_phys J_phys` has units `L^2/T`, and the dimensional conversion factor for a canonical scalar formula is indeed `chi_phys ell_ref/k_ref`.

### Weighted forms and process construction

The positive-floor closability proof is valid even for unbounded integrable D: an energy-Cauchy derivative sequence is Cauchy in ordinary L2, distributional differentiation identifies its unweighted limit, and simultaneous almost-everywhere subsequences identify the weighted limit. The proof establishes the inclusion of the minimal closure in H1; it does not incorrectly identify that closure with every H1 function having finite weighted energy.

The anchored inequality follows from the constant/mean-zero decomposition with constants depending only on the declared rate anchor and upper bound. Its coercivity consequence gives the L2 inverse for each positive floor. The contraction argument establishes the required positivity and permits the constant test, so both `J=int h` and `int kh=P` follow.

For any closable D, the trace term is continuous on the product of bulk H1 and the surface closure, and the nonnegative energy controls both separate derivative energies. This proves closedness of the coupled form, rather than merely boundedness of its extra term. Normal contractions decrease the exchange term as well as the derivative terms. The use of the disjoint union state space is appropriate: a dissolved particle at the geometric boundary and an adsorbed particle at that same location are different states, and their two function values are not required to agree. Smooth independent pairs are dense in the product form norm and uniformly dense in continuous pairs. Thus regularity and the cited process construction apply. The constant pair is in the domain and has zero energy; in this finite-measure setting it belongs to the generator kernel, proving conservativity of the stationary process.

The positive-floor gap argument is also valid. Subtraction of the bulk mean fixes a common additive constant, bulk Poincare controls the trace, the exchange term controls `int k v^2` up to that trace term, and the anchored surface estimate closes the product norm. Passing to the pi-mean-zero representative can only reduce the norm. No irreducibility or spectral gap is illicitly inferred for all degenerate designs.

I checked the external theorem numbering against the primary open discussion [Li and Ying](https://arxiv.org/pdf/1701.02411): its discussion of Hamza's theorem explicitly identifies FOT Theorem 3.1.6. The book citation is consistent with this use. The manuscript proves the positive-floor case it actually needs for the comparison, so it does not rely on an unstated version of Hamza's criterion to construct its regularized policies.

### Stationary variance and the finite-response Schur completion

For a reversible stationary process, the covariance is the nonnegative spectral transform of the centered velocity. I recalculated the time integral:

`b_t(lambda)=1/lambda-(1-exp(-lambda t))/(t lambda^2)` for `lambda>0`, and `b_t(0)=t/2`.

It is increasing in t and has the stated extended limit. Thus the physical stationary variance coefficient exists without a central limit theorem or an assumed gap. In particular, an atom at zero legitimately gives an infinite coefficient rather than being silently removed by centering the global stationary mean.

The Schur factors and signs check directly. For fixed bulk trace b, the surface linear forcing is `kb-V`; its completed quadratic contributes `KV^2 J`, cross term `-2KV int kh b`, and negative quadratic residual `-K S_D(b)`. The identities `int_Omega(u-V)=KPV` and `int kh=P` make the bulk load invariant under addition of a constant, and shifting the surface minimization variable proves the same invariance for S. After division by Z the scalar prefactor is `KV^2/Z`.

The finite-J extension is a substantive improvement over an informal inverse notation and is valid. Finite J makes the source bounded in the reaction-plus-derivative energy seminorm and zero on its null space. Completion gives its Riesz representative h. The map `v -> sqrt(k)v` is energy bounded, so its extended image is well defined even when h is not an L2 function. Bounded k makes `w=sqrt(k)(sqrt(k)h)` an L2 function. A trace load `int kbv` is energy bounded with squared dual norm at most `int kb^2`; therefore the completed square and the nonnegative residual remain finite. Smooth density in the original closure and in the energy completion justifies equality of the infima, without subtracting infinite expressions. Finally bulk Poincare and the L2 trace estimate bound the resulting load and hence the remainder. I found no gap in the assertion that finite scalar response implies finite full response for a physically admissible coefficient at fixed bulk data.

### Logarithmic remainder

I checked each exponent and normalization in the proof. Coercivity gives `J<=C/m`, the energy identity gives `||h'||_2<=C/m`, and one-dimensional H1 control gives `||h||_infinity<=C/m`. Positivity and `int w=P` are essential: with the specified Fourier normalization they give `|w_hat_n|<=1` and `sum |w_hat_n|^2<=||w||_infinity`. Low frequencies then contribute a harmonic sum and the high frequencies contribute at most `C||w||_infinity/N`. Choosing `N` proportional to `2+||w||_infinity` gives the claimed logarithm. Trace duality and maximization of `2ax-D_b x^2` produce a remainder of the same logarithmic order. There is no dependence on a derivative or upper bound of D hidden in this chain.

### Policies, measurability, and comparison

The countable-test argument works because a single countable C1-dense smooth core approximates each smooth test with convergence of its derivative uniformly; D is integrable and each fixed rate is bounded. The same applies to smooth bulk–wall pairs. The resulting countable supremum is Borel on the larger coefficient space and agrees with the physical quantity on closable designs. Measurability of the set of closable weights is not needed for composition with a policy whose values are all in that set.

The uniform policy gives finite objectives under the uniform rate assumptions. Consequently a sequence approaching each infimum exists by the definition of infimum; no pointwise measurable minimizer selection is being assumed. Mixing any such scalar policy with `theta M/P` preserves its observation, Borel property, and exact per-observation budget. The energy inequality uses the full reaction term correctly: `a(D_theta)=(1-theta)a(D)+theta a(M/P)`. Thus the inverse quotient inequality, logarithmic remainder bound, and distinct q>=1/q<1 expectation inequalities are valid. Choosing theta=M proves the ratio without an extra regular-variation assumption.

For the all-information corollary, the root bump has squared source of order `ell^2`, mobility cost at most `M ell^(-2)`, and reaction cost of order `ell^3`. The choice `ell=M^(1/5)` yields the pointwise bound `J>=c M^(-1/5)` for every competitor. The event `|c|<=1/2` has probability 1/4, independently of information. The stated uniform moment-ratio errors follow, with the mixture error O(M) smaller than either displayed error for every fixed positive q.

## Findings requiring minor corrections

### R1-01 — State finite molecular-diffusion assumptions explicitly

- **Severity:** minor.
- **Location:** `sections/01-model-transfer.tex`, lines 233–241, equation `eq:molecular`; initial PDE at lines 23–30 is also affected.
- **Issue:** The optional axial Brownian contribution is introduced without mathematical assumptions on `D_b^x` and `D_s^x`. The conditional-mean-zero and finite variance calculation requires nonnegative coefficients and, for the finite contribution displayed here, `D_b^x<infinity` and `D_s^x in L1(Gamma)`. The assumptions on tangential D do not automatically impose these requirements on an independently specified axial coefficient.
- **Remedy:** State `0<=D_b^x<infinity` and `0<=D_s^x in L1(Gamma)` before constructing the axial stochastic integral or giving its finite variance. If these may depend on realization/policy, state the uniform boundedness condition exactly where a common bounded molecular contribution is used in the concluding transfer remark. This does not alter the flow-only theorem or isotropic case, since `D_s^x=D` already has fixed finite integral.

### R1-02 — Explicitly cover the zero eigenspace in the variational proof

- **Severity:** minor proof clarification.
- **Location:** `sections/01-model-transfer.tex`, lines 251–257, explanation following `eq:full-variational`.
- **Issue:** The sentence asserting that spectral cutoffs of `lambda^(-1)g` give the reverse inequality “including an infinite value” omits the case where infinity is caused by mass at lambda=0. Positive-frequency cutoffs alone cannot recover that component. Such a case is allowed here, for example a degenerate wall with a positive-measure trapped region. The alternative resolvent route mentioned just above is sufficient to repair this, so this is not a flaw in the theorem or Schur conclusions.
- **Remedy:** Add the zero-mode branch explicitly: if `g_0=E_A({0})g` is nonzero, the trials `w_n=n g_0` have zero energy and objective `2n||g_0||_pi^2 -> infinity`; otherwise use positive-frequency cutoffs. Alternatively give the resolvent integrand `(lambda+2 epsilon)/(lambda+epsilon)^2`, which tends monotonically to `1/lambda` including infinity at zero. Either is a one- or two-sentence complete repair.

## Build and scope

`latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex` returned success and reported the frozen PDF up to date. No scientific numerical calculation is needed for this stage's analytic claims. This review does not substitute for the later clean build, full PDF inspection, literature audit, or full-manuscript review.

**Recommended disposition:** accept Stage 01 after the two valid minor corrections have been made by the separate fixer and checked by the coordinator. No repeat five-reviewer round is required by this review alone, because no major issue was identified.
