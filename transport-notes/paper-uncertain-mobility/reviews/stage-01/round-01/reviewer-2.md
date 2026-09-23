# Independent review: stage 01, round 01, reviewer 2

Date: 2026-09-07. Reviewed frozen snapshot `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`. Independently recomputed every hash listed in `snapshot.json`; all matched. Read the complete Stage 1 LaTeX section, author handoff, notation ledger, claim inventory, plan, entry point/preamble, and bibliography. No other review report in this round was read, and no manuscript source was edited.

## Verdict

**No major or minor issue found. Accept Stage 1.** This verdict concerns M1–M4 and their present supporting arguments. It does not approve the later local asymptotics, optimization constants, information-resolution theorem, or novelty claims, which have not yet been drafted.

## Independent mathematical and scientific checks

### Physical signs, equilibrium, and units

I integrated the bulk transverse equation and checked that its boundary contribution is `Db∫Γ∂n p = -∫Γ(Kkp-kρ)`, exactly the negative of the integrated wall gain. The equilibrium pair `(p,ρ)=(constant,K×constant)` therefore has no transverse exchange or diffusive flux. Normalization gives bulk mass `A/Z`, surface mass `KP/Z`, and, with the now explicit zero axial wall drift, `V=∫Ωu/Z`.

Independently integrating the coupled backward energy by parts gives the boundary coefficient `Db∂n f+Kk(fΓ-v)`, hence `Db∂n f=Kk(v-fΓ)`. Dividing the wall form by its measure weight K gives wall generator `(Dv')'+k(fΓ-v)`. These factors and signs agree with the forward model after using wall density `ρ/K` relative to the reversible measure.

The physical prefactor has dimension `[χ]=L/T²`; multiplying the response `[J]=LT` yields diffusivity `L²/T`. Scaling `s=ell_ref s'`, `k=k_ref k'`, and `D=k_ref ell_ref² D'` gives `J_phys=(ell_ref/k_ref)J'`. The stated conversion of a dimensionless scalar leading coefficient is therefore correct. All small-budget powers/logarithms subsequently refer to fixed dimensionless units.

### Weighted forms and the physical policy class

The manuscript correctly separates the always-defined smooth-test scalar functional from coefficients admitting actual closed transverse dynamics. The positive-floor closability proof does not silently require an upper bound on D: `v_n'` converges to zero in ordinary L², while the weighted derivatives have an L² limit, and a common almost-everywhere subsequence identifies that limit as zero because D is finite almost everywhere. The same argument identifies the derivative in the closure.

The anchored inequality follows by controlling the constant part through `∫k≥κ` and the oscillatory part through periodic Poincaré. It yields coercivity `a≥c min(m,1)||v||²`, not a coefficient-independent coercivity claim. Positivity of the inverse and both test identities `a[h]=∫h` and `∫kh=P` are justified. The contraction argument is adequate for the positive-floor lemma and extends to the closable derivative form used in the coupled construction.

For the coupled form, the bounded trace map and bounded k make the exchange energy continuous in the product norm. Its nonnegative addition preserves closedness; common normal contractions decrease all three terms. The state space is explicitly the disjoint union of the closed bulk and the adsorbed wall, so smooth pairs need not agree on the two copies of the boundary. They are a valid dense continuous core. The reference measure has full support there; the constant belongs to the domain and has zero energy, giving conservativity. The gauge argument proves a gap only with a positive floor, as stated. Degenerate designs are not incorrectly declared ergodic.

I also checked the external theorem identification through primary open sources. [Li and Ying](https://arxiv.org/pdf/1701.02411), including their introductory identification of FOT Theorem 3.1.6 and Section 3.4, supports the Hamza citation. The associated-process use of FOT Theorem 7.2.1 is consistent with the primary application at [arXiv:1308.0234](https://arxiv.org/pdf/1308.0234). Neither citation is being used to bypass the concrete form checks supplied here.

### Stationary variance and variational representation

For a stationary centered additive velocity, the double covariance integral reduces to `Var X_t=2∫_0^t(t-r)<g,e^(-r A)g>π dr`, giving precisely the displayed division by `2t`. Reversibility makes the covariance a Laplace transform of the nonnegative spectral measure. For each λ≥0, `(1-r/t)_+` increases with t, so the integrated spectral kernel increases; its limit is `1/λ` for λ>0 and infinity at λ=0. Thus the extended coefficient follows from particle variance, including possible zero modes, without an unproved central limit theorem or an assumed inverse in L².

The source in unnormalized variables is `F=∫Ω(u-V)f-KV∫Γv`; both the source and the energy acquire the same factor `1/Z` in L²(π). Consequently the full variational formula has `Z Dflow` on its left, as written. Setting `f=0, v=-Vφ` then yields `K V² J/Z=χJ`, with no lost factor of two. The independent axial Brownian-driver argument correctly gives the molecular average and zero covariance with the advective part. Stationary initialization is explicit throughout.

### Schur identity, including finite response without an L² corrector

For fixed bulk trace b, the surface optimization is

`K[2<kb-V,v>-a[v]-∫kb²]`.

Its positive-floor maximum expands as `K V² J - 2 K V∫kh b - K S(b)`, where `S(b)=∫kb²-<kb,H^-1 kb>≥0`. Adding the bulk source and gradient yields the displayed load, remainder, and signs. The identities `∫Ω(u-V)=KPV` and `∫kh=P` make the load annihilate constants; shifting both b and the trial surface field proves `S(b+a)=S(b)`. The gauge is therefore valid. Choosing zero bulk field proves nonnegativity of the remainder.

The finite-J extension is also complete. In the scalar energy completion W, the source is bounded exactly when J is finite. The image `T(v)=sqrt(k)v` is a contraction into L², so `w=sqrt(k)T(h)` is well-defined in L² even if h itself has no L² representative. For the bulk trace forcing, `|∫kbv|≤||sqrt(k)b||₂ a[v]^(1/2)` gives a Riesz representative z_b. Symmetry gives `<z_b,h>_a=∫wb`. Completing the square in W is therefore legitimate. The surface residual is nonnegative already on its dense smooth core and remains so after completion; the infima over smooth tests, V_D, and W coincide by energy density. In particular, no infinite expressions are subtracted. Finally, the L² bound on w and the bulk trace/Poincaré inequalities bound the remainder's load by a constant times `||∇f||₂`, proving finiteness. This addresses the main potential no-floor gap rather than assuming it away.

### Uniform logarithmic remainder

Independently recovered `J≤C/m`, `||h'||₂≤C/m`, and `||h||∞≤C/m` for `0<m≤1`. Since w is nonnegative with integral P, its Fourier coefficients satisfy `w_hat(0)=1` and `|w_hat(n)|≤1`. With the stated normalization, Parseval is `∑|w_hat(n)|²=P^(-1)||w||₂²≤||w||∞`. The low frequencies in the H^(-1/2) norm sum harmonically; the high frequencies cost at most `C||w||∞/N`. Choosing N comparable to `1+||w||∞` gives the logarithm with no hidden derivative or upper-mobility dependence.

The final estimate pairs `w-1` with a trace in H^(1/2), controls the constant trace and bulk terms in the mean-zero gauge, drops the nonnegative surface penalty, and maximizes `2ax-Db x²` to obtain `a²/Db`. This squares the H^(-1/2) norm and therefore preserves the logarithmic order. Connected-wall, fixed positive Db, and fixed-unit restrictions are correctly retained.

### Measurability and optimized moment comparison

For smooth tests all coefficient dependence is continuous in the L¹ topology because test values and derivatives are bounded. Countable C¹-dense smooth cores give the same suprema even for unbounded integrable coefficients, proving joint extended Borel measurability. The physical response can be represented by this countable smooth supremum on the ambient coefficient space and identified on the closable subclass; the proof does not need that subclass itself to be Borel. Policies are actual Borel maps and no expectation–pointwise-infimum interchange is made. A uniform positive design ensures finite policy values uniformly over the anchored rate family.

The mixed design has exactly the original per-observation budget and retains the same information. Since its quadratic form dominates `(1-θ)a_D`, the quotient gives `J(Dθ)≤J(D)/(1-θ)`, including nonclosable original scalar competitors. This closes the apparent mismatch between scalar and physical admissibility. The physical lower bound follows from class inclusion in the correct direction.

For q≥1, Minkowski acts on the qth root of the moment; for 0<q<1, subadditivity acts on the unrooted moment. The displayed inequalities use these distinct forms correctly. Taking θ=M requires only the stated logarithmic growth condition, not regular variation or existence of minimizers.

Finally, the cosine root bump has numerator of order ell² and denominator at most `C(M/ell²+ell³)`. Setting `ell=M^(1/5)` gives the claimed pointwise `M^(-1/5)` lower bound for every admissible field, so it remains valid for every observation law. The retained event has probability 1/4. The resulting errors are `M^(1/5)log(1/M)` for q≥1 and `M^(q/5)log(1/M)^q` for q<1; the mixture's O(M) error is smaller in both cases.

## Completeness and clarity

The section supplies all Stage 1 prerequisites without relying on unpublished repository notes. Its technically difficult points—scalar versus physical fields, stationary variance versus a central limit theorem, and energy versus L² correctors—are expressly distinguished. The functional-analysis discussion is lengthy for transport readers, but it is sufficiently explained and the accepted plan already permits moving technical material to an appendix during final synthesis. That future editorial placement is not a present defect.

The no-floor identity is stronger than the floor-based transfer needs, but it resolves a real class/domain issue and is within the requested scope. Restrictions concerning zero mean velocity, vanishing bulk diffusivity, unanchored families, or fabrication constraints are stated rather than implicitly swept into the theorem. No currently actionable mathematical or editorial correction was identified.
