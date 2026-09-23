# Route to a short-range Potts finite-reservoir theorem

Date: 2026-09-07. **Current status: the isolated-copy necessity-and-sufficiency theorem is proved** for every fixed spatial dimension d>=2 and sufficiently large fixed q, including plain spins. See [the manuscript theorem](../paper-finite-reservoirs/sections/microscopic.tex), label thm:sr-bath, and [the full positive-contour proof](../paper-finite-reservoirs/appendices/short-range-proof.tex). Its source conventions and energy transfer completed two five-reviewer rounds in [Stage 2](../paper-finite-reservoirs/WORKFLOW.md).

The body below records the earlier two-dimensional route and obstacles that were resolved. Necessity-only and missing-tail statements describe that historical stage, not the current result. The completion proves restricted-partition derivatives in a cutoff-free 1/L window, then transfers moments from bond count to actual spin energy using the conditional binomial law. No signed remainder is treated as a probability measure.

## 1. Target microscopic statement

Use the nearest-neighbor ferromagnetic q-state Potts model on the two-dimensional periodic square of side `L`, with `N=L²` and fixed sufficiently large integer `q`. Fix units so that

\[
U_N(\sigma)=-\sum_{\langle x,y\rangle}\mathbf1_{\sigma_x=\sigma_y}.
\]

Set `E_N=U_N`; no auxiliary kinetic variables are needed. The q ordered colors share one energy density; the disordered phase has a different density. There are two energy phases. An optional continuous extension adds independent quadratic momenta giving `K_N~Gamma(aN,βc)`, with fixed `a>0` and integral number `2aN` of quadratic degrees of freedom, and uses `E_N=U_N+K_N`. Section 4 retains this extension as a smoothing construction.

The desired conclusion at coexistence is

\[
\exists\mathcal E_N:\operatorname{TV}(P_N,Q_{N,\mathcal E_N})\to0
\quad\Longleftrightarrow\quad c_N/N^{3/2}\to\infty,
\]

where the reservoir density of states is `U_B^{c_N}1_{U_B>0}`, `c_N>0`. Full-state and total-energy total variation agree because the Radon–Nikodym derivative is a function of total energy alone. An optional independent kinetic term does not change the spin coexistence temperature or latent spin-energy difference.

## 2. What the primary sources actually supply

**Borgs, Kotecký, Miracle-Solé, “Finite-size scaling for Potts models,” J. Stat. Phys. 62 (1991), 529–551.** Theorem 1 in the open author manuscript supplies two **six-times differentiable** metastable free energies, a strictly positive latent heat, an exponentially accurate two-term periodic partition expansion, and controlled low-order temperature derivatives. It does not assert analyticity of those functions. Its discussion of a two-Gaussian energy histogram describes an earlier approximation, not a proved local limit theorem. Relevant locations: printed manuscript pp.10–11 for Theorem 1 and p.16 for the Gaussian-ansatz discussion (PDF page indices 9–10 and 15). [Open author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Finite-Size-Scaling-for-Potts-Models.pdf).

**Borgs, Chayes, Helmuth, Perkins, Tetali, “Efficient sampling and counting algorithms for the Potts model on Z^d at all temperatures.”** For large q, §§3.3–3.4 define disjoint positive random-cluster events for ordered exterior, disordered exterior, and tunneling configurations. Equations (44)–(46) retain the ordered multiplicity q. Lemma 4.1 bounds the tunneling probability by `exp(−bL^(d−1))`; Lemma 4.4 gives contour-weight decay at coexistence. These are genuine positive-measure estimates, stronger for this purpose than a signed partition remainder. [Open version, arXiv:1909.09298v3](https://arxiv.org/html/1909.09298).

The latter paper attributes its tunneling and contour estimates to Borgs, Chayes, Tetali, **“Tight bounds for mixing of the Swendsen–Wang algorithm at the Potts transition point,”** PTRF 152 (2012), 509–557. Its contour analysis is the next source to audit in detail, especially Lemmas 6.1 and 6.3 and Appendix A. [Primary preprint](https://arxiv.org/abs/1011.3058).

A search result for **Garet, “Central limit theorems in Random cluster and Potts Models,”** concerns very-low-temperature cluster/magnetization fluctuations. It does not directly establish the required ordered/disordered *energy* CLTs at coexistence; it should not be substituted for that missing theorem. [Primary preprint](https://arxiv.org/abs/math/0308190).

Only the first two full texts were inspected in detail during this bounded task. The other sources are explicitly identified as leads or nonmatching results.

## 3. Real-temperature partition estimates can yield the phase energy CLTs

This section is a derivation from the real partition expansion, not a claim that the source states a CLT. It avoids assuming analytic continuation or a positive measure associated with a metastable exponential term.

Write the audited expansion in dimensionless free-energy notation `ψ_i(β)=βf_i(β)`:

\[
Z_N(\beta)=q e^{-N\psi_o(\beta)}+e^{-N\psi_d(\beta)}
+O(e^{-bL})e^{-N\min_i\psi_i(\beta)}.
\tag{A}
\]

It is understood uniformly for real β in a neighborhood of coexistence. At `βc`, `ψ_o=ψ_d`; define `u_i=ψ_i'(βc)` with `u_o<u_d`, and `σ_i²=−ψ_i''(βc)`. The original theorem's smoothness is more than enough for the following second-order expansions. Additive Hamiltonian conventions change `ψ_i` and `u_i` by common affine terms and leave the argument unchanged.

First evaluate `Z_N(βc+t/N)/Z_N(βc)` for fixed real `t`. Since the spin energy density is bounded, convergence of these Laplace transforms proves

\[
U_N/N\Rightarrow w_o\delta_{u_o}+w_d\delta_{u_d},
\quad w_o=\frac q{q+1},\quad w_d=\frac1{q+1}.
\]

Define **actual spin events** by the energy midpoint,

\[
A_{o,N}=\{U_N/N<(u_o+u_d)/2\},\qquad
A_{d,N}=A_{o,N}^{c}.
\]

Their probabilities tend to `w_o,w_d` by the preceding weak limit. They are independent of β once the coexistence energies are fixed.

For `s>0`, the stable ordered term dominates (A) at `βc+s/sqrt(N)`. Therefore

\[
\mathbb E_{\beta_c}\exp\left[-s\frac{U_N-Nu_o}{\sqrt N}\right]
\longrightarrow w_o\exp(\sigma_o^2s^2/2).
\tag{B}
\]

The contribution from `A_d,N` to the left side is at most `exp[−s(u_d−u_o)sqrt(N)/2]`, by its energy threshold. Thus (B) is also the Laplace-transform limit of the positive ordered subprobability measure. The disordered phase has the analogous transform with the opposite sign, using `βc−s/sqrt(N)`.

For completeness, a one-sided transform limit plus the known phase mass is sufficient. Fix `s0>0` and exponentially tilt the ordered subprobability measure by `exp(−s0 x)`. Ratios of (B) at `s0−t` and `s0` give its moment-generating function on an interval around zero, hence convergence to the corresponding tilted Gaussian. Undoing the tilt on compact sets gives vague convergence of the original subprobability measures. Their total masses converge to the mass `w_o` of the recovered Gaussian, so no mass escapes and convergence is weak. This proves

\[
\frac{U_N-Nu_i}{\sqrt N}\ \bigg|\ A_{i,N}
\Rightarrow\mathcal N(0,\sigma_i^2).
\tag{C}
\]

The limiting transforms alone allow a vanishing variance. For the present nearest-neighbor model, however, the following elementary bound proves that both `σ_i²` are strictly positive without kinetic energy.

### 3.1. Positive spin-phase variances from conditional independence

Take `L≥3` and a compact inverse-temperature interval `I⊂(0,∞)` with upper endpoint `βmax`. The square torus has maximum degree four, so it contains an independent vertex set `S` with `|S|≥N/5`. Condition on every spin outside S. The remaining spins are independent. If `n_{x,a}` is the number of neighbors of x having color a, then

\[
U_N=U_{\mathrm{outside}}-\sum_{x\in S}n_{x,\sigma_x},
\qquad
p_{x,a}=\frac{e^{\beta n_{x,a}}}{\sum_{b=1}^q e^{\beta n_{x,b}}}
\ge \frac{e^{-4\beta_{\max}}}{q}.
\]

The nonnegative integers `n_{x,a}` sum to four. When `q>4`, at least one count is zero and at least one is positive. Thus two possible local energy values differ by at least one. The variance identity

\[
\operatorname{Var}_{p_x}(n_{x,a})
=\sum_{a<b}p_{x,a}p_{x,b}(n_{x,a}-n_{x,b})^2
\]

and conditional variance decomposition give, uniformly in `β∈I`,

\[
\operatorname{Var}_\beta(U_N)
\ge\mathbb E_\beta\operatorname{Var}(U_N\mid\sigma_{S^c})
\ge v_*N,\qquad
v_*=\frac{1}{5q^2e^{8\beta_{\max}}}>0.
\tag{C1}
\]

Consequently `p_N(β)=N^{-1}log Z_N(β)` satisfies `p_N''≥v_*`. The functions `p_N(β)−v_*β²/2` are convex, and their pointwise thermodynamic limit is convex. On each open stable side of coexistence that limit equals `−ψ_i(β)−v_*β²/2`. Because the metastable free energies are C², `−ψ_i''≥v_*` there and continuity extends the inequality to coexistence from the corresponding side. Therefore

\[
\boxed{\sigma_o^2,\sigma_d^2\ge v_*>0.}
\tag{C2}
\]

The local variance estimate needs only `q>4`; the phase decomposition used elsewhere still requires the sufficiently large fixed q of the cited theorem. This argument does not infer a phase variance directly from the order-N² coexistence variance. It first passes the uniform strong-convexity inequality to each stable thermodynamic branch. It proves nondegeneracy of the weak limits in (C), without claiming convergence of phase second moments or a spin local limit theorem.

This argument establishes conditional **weak** energy fluctuations, not inward exponential-moment control. The distinction is essential for finite-bath sufficiency.

## 4. Optional kinetic smoothing for continuous local limits

Let

\[
X_{i,N}=(U_N-Nu_i)/\sqrt N\mid A_{i,N},\qquad
Y_N=(K_N-aN/\beta_c)/\sqrt N.
\]

The standardized Gamma density `g_N` converges uniformly to the centered Gaussian density of variance `a/βc²`. This follows directly from Stirling's formula on compact intervals, with the gamma tails controlling the supremum outside expanding intervals. Equivalently, one may prove it by Fourier inversion of the explicit Gamma characteristic function.

If `X_{i,N}⇒Normal(0,σ_i²)`, the density of `X_{i,N}+Y_N` is

\[
f_{i,N}(z)=\int g_N(z-x)\,d\mu_{i,N}(x).
\]

Uniform convergence of `g_N`, weak convergence of `μ_i,N`, and bounded uniform continuity of the limiting Gaussian kernel imply uniform convergence of `f_i,N` on compact sets. Tightness supplies the tails; hence the convergence is also in `L¹` over the whole line. Therefore the full canonical energy density has the needed local limits at

\[
e_i=u_i+a/\beta_c,\qquad
v_i=\sigma_i^2+a/\beta_c^2>0,
\]

with the two positive phase weights above.

Section 3 alone, together with the independently reviewed arbitrary-total-energy concavity argument, proves **plain spin-only short-range necessity** `c_N≫N^(3/2)` under the published theorem audited below. Positive nondegenerate conditional weak limits suffice: no kinetic smoothing, interfacial-tail theorem, or spin local central limit theorem is needed. This section supplies an optional continuous version of the model.

## 5. A sufficient positive-measure criterion weaker than sub-Gaussian tails

Here is a precise lemma that would close sufficiency. It can use either actual spin events or phase events in an enlarged spin–bond probability space.

Assume a positive decomposition into ordered/disordered phase events and a remainder `R_N`, such that

\[
P_N(R_N)\le C e^{-bL},\qquad
P_N(A_{i,N})\to w_i>0,
\]

and, for some fixed small `δ>0`,

\[
\sup_N\mathbb E\left[
\exp\left(\delta\left|\frac{U_N-Nu_i}{\sqrt N}\right|\right)
\mid A_{i,N}\right]<\infty.
\tag{D}
\]

If kinetic variables are included, their Gamma law satisfies the analogous bound, so (D) holds for the total centered energy as well. In the plain model, use `E=U` and `e_i=u_i`. The phases must also concentrate on the stated fluctuation scale; (D) already implies tightness, while (C) supplies their precise local limits if needed.

Choose the exact endpoint-balancing physical bath. Let its residual log-weight, after subtracting the common endpoint value, be `h_N`, with endpoints `Ne_o,Ne_d`. Its global maximum obeys

\[
\sup_E h_N(E)=O(N^2/c_N)=o(L)
\]

when `c_N≫N^(3/2)`. Hence the unnormalized contribution of `R_N` is at most `C exp[−bL+o(L)]→0`. This estimate is valid because `R_N` is a positive-measure event.

For each phase, concavity and the tangent at its endpoint give the global upper bound

\[
h_N(E)\le |h_N'(Ne_i)|\,|E-Ne_i|
\le\varepsilon_N\left|\frac{E-Ne_i}{\sqrt N}\right|,
\quad \varepsilon_N=O(N^{3/2}/c_N)\to0.
\]

On fixed fluctuation windows `h_N→0` uniformly. Bound (D) makes the exponentials uniformly integrable, and therefore the phasewise expectation of `|exp(h_N)−1|` tends to zero. The remainder estimate and normalization complete TV convergence.

A global sub-Gaussian bound is thus unnecessarily strong. Uniform small exponential moments of standardized phase energy are sufficient and compatible with two-dimensional droplet tails. One-sided outward moments, obtained in section 3, are insufficient: the bath gains weight in the inward direction between the phases.

## 6. Former sufficiency gap, now resolved in the manuscript

The positive random-cluster decomposition controls tunneling mass, but its phase events depend on auxiliary bonds. Under the Edwards–Sokal joint law this is a legitimate positive decomposition, and bath reweighting can be performed on that enlarged space. Projecting to spins preserves the desired conclusions. However, the physical energy is the spin Hamiltonian, **not the number of occupied random-cluster bonds**.

In particular, differentiating a phase-restricted random-cluster partition function with respect to β also differentiates the β-dependent bond kernel. It cannot be silently identified with the conditional moment-generating function of spin energy under the phase event. That identification needs an additional argument, a spin-based positive restriction, or a source theorem directly controlling the physical energy observable.

Peierls contour-weight bounds alone also do not give (D) in one line. A contour's enclosed volume can be much larger than its perimeter. At coexistence, mesoscopic opposite-phase droplets are precisely the events that make a Gaussian tail implausible. A viable contour proof should track their total volume and show that a physical-energy tilt of magnitude `δ/L` can be absorbed into the contour cost, then control derivatives or centered cumulants of the resulting positive restricted partition function. The geometric estimate `volume≤C L × perimeter` suggests that sufficiently small `δ` is admissible on a two-dimensional torus, but recursive interiors and the physical spin/bond correspondence still need to be handled.

An alternative is a direct energy-tail bound on actual midpoint-conditioned spin phases of the form

\[
P\{|U_N-Nu_i|\ge x\mid A_{i,N}\}
\le C\exp\left[-b\min\{x^2/N,\sqrt{x}\}\right]
\]

over the relevant interior range, with any additional exponentially small macroscopic-contour term. Such an estimate would imply (D) for sufficiently small fixed δ, but it has not been located and verified here for the exact coexistence-conditioned periodic Potts measure.

The original six-derivative partition theorem must not be promoted to a uniform complex-temperature analytic theorem. Nor may an exponentially small scalar partition error be called an exponentially small distributional TV error. Those shortcuts would skip the principal remaining work.

## 7. Historical next-step assessment

Retain the model as the preferred short-range target. Necessity is now certified as the corollary below; label the full iff claim provisional. The remaining next step is to audit the positive contour estimates in the 2012 mixing paper for a physical-energy version of (D), or prove that lemma using its contour machinery. If that step requires a substantial new Pirogov–Sinai analysis, present it as a real remaining theorem rather than hiding it in “standard phase decomposition.”

The current outcome is useful even without immediate closure: it replaces an unnecessary spin LCLT and global sub-Gaussian requirement by two weaker, explicit tasks, identifies a genuine positive remainder estimate, and pinpoints the remaining inward-tail and observable-transfer gap.


## 8. Closed necessity gate: precise source audit and corollary

Audit completed 2026-09-07. The open author manuscript of Borgs, Kotecký and Miracle-Solé, *Finite-size scaling for Potts models*, corresponds to J. Stat. Phys. **62** (1991), 529–551, DOI [10.1007/BF01017971](https://doi.org/10.1007/BF01017971). The manuscript carries a June 1990 preprint date; that is distinct from the 1991 publication date. Page references below use its **printed** pagination.

The following source details were checked in the extracted text and visually on pp.6, 10, and 11:

- Equation (6), p.6, uses exactly `H=−JΣδ(σ_i,σ_j)` on a periodic cube with `dL^d` nearest-neighbor bonds. The text sets `J=1` before (7). Thus the route's physical spin Hamiltonian and its canonical partition ratios match the source directly.
- Theorem 1(i)–(iii), pp.10–11, states the six-times differentiable free energies, the stable branch on each side, a latent-energy gap bounded below, and the two-term partition bound. The preceding equation (16), p.9, is extended to all real physical inverse temperatures; it is not restricted to the narrow `L^(−d)` rounding window.
- Appendix (A.9)–(A.14), pp.28–29, constructs uniformly controlled contour activities and explains temperature-independent derivative bounds on `β≥1`. It supplies no reason to impose `|β−βc|=O(L^(−d))` on Theorem 1. For sufficiently large fixed q one can take a compact neighborhood of βc within this range.

In particular, the precise local real-temperature form needed here is: for fixed `d=2` and sufficiently large fixed q, there exist a compact interval `I` containing βc in its interior and constants `C,b>0`, independent of β in I and large integer L, such that

\[
\left|Z_L(\beta)-q e^{-N\psi_o(\beta)}-e^{-N\psi_d(\beta)}\right|
\le Cq^{-bL}e^{-N\min\{\psi_o(\beta),\psi_d(\beta)\}},
\quad N=L^2,\quad \beta\in I.
\tag{E}
\]

Here `ψ_i=βf_i`, `ψ_o(βc)=ψ_d(βc)`, `ψ_d′(βc)−ψ_o′(βc)>0`, and each `ψ_i` is six-times differentiable. This is Theorem 1 restricted to a compact real interval, with its big-O constant made explicit. [Audited primary manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Finite-Size-Scaling-for-Potts-Models.pdf).

For every fixed real t and fixed positive s, all three sequences `βc+t/N`, `βc+s/sqrt(N)`, and `βc−s/sqrt(N)` eventually lie in I. The latter two have displacement `s/L`, which is larger than the `L^(−2)` rounding scale, but remains in the real-temperature range of (E). On the ordered side, dividing by the dominant ordered exponential leaves an error `O(q^(−bL))`; the disordered side is identical. Centering the physical-energy transform changes this by a bounded factor from the second-order Taylor expansion, so no exponential error is lost. Thus equation (A), exactly as used in section 3, is justified by the published theorem. No analytic continuation has been inferred.

**Corollary — microscopic short-range necessity.** Fix `d=2` and sufficiently large integer q. Consider the plain nearest-neighbor periodic Potts model with `J=1` on square tori of side L, `N=L²`, and physical energy `E_N=U_N`. Let `P_N` be its canonical law at βc. The same conclusion holds if independent quadratic momenta are optionally added as in section 4. For any `c_N>0` and total-energy sequence `mathcal E_N` defining a normalized physical-bath marginal,

\[
Q_N(d\omega)=
\frac{e^{\beta_c E_N(\omega)}
[\mathcal E_N-E_N(\omega)]_+^{c_N}}
{\mathbb E_{P_N}\{e^{\beta_c E_N}
[\mathcal E_N-E_N]_+^{c_N}\}}P_N(d\omega),
\]

one has

\[
\boxed{\operatorname{TV}(P_N,Q_N)\longrightarrow0
\quad\Longrightarrow\quad c_N/N^{3/2}\longrightarrow\infty.}
\tag{F}
\]

**Proof.** The audited estimate (E) and the independently reviewed one-sided-Laplace argument give two positive phase probabilities approaching `q/(q+1)` and `1/(q+1)`, and conditional weak spin-energy CLTs at `Nu_o` and `Nu_d`, separated by `N(u_d−u_o)`. The conditional-independence argument (C1)–(C2) makes both Gaussian variances strictly positive already for spin energy. In the optional kinetic extension the phase means and variance coefficients acquire the additional terms `aN/βc` and `a/βc²`. If TV tends to zero, its likelihood ratio tends to one in probability under each phase law. Four fixed separated standardized intervals around each center have positive limiting probability; selecting good likelihood points there and using concavity gives

\[
\sqrt N\left[\beta_c-
\frac{c_N}{\mathcal E_N-Ne_i}\right]\to0,
\qquad e_i=u_i\quad\text{(plain spin model)}.
\]

The feasible-domain cutoff cannot remove such intervals under TV convergence. Subtracting reciprocal endpoint bath inverse temperatures yields

\[
\frac{N(e_d-e_o)}{c_N}=o(N^{-1/2}),
\]

and `e_d−e_o=u_d−u_o>0` proves (F). The conclusion applies equally to full-state and total-energy TV because the likelihood is energy-measurable. This is a deduction from the cited published finite-size theorem, not an independently re-proved contour theorem. ∎

The corollary proves only necessity. It does not assert that the physical reservoir can reproduce the periodic short-range law whenever `c_N≫N^(3/2)`, and it does not establish inward exponential moments or distributional estimates from a signed partition error. Those remain the sufficiency tasks in sections 5–6.
