# Traveling deformation, zero solvent throughput, and bounded dispersion

Status: candidate physical corollary, derived 2026-09-06 and independently validated by the reviewer recorded in [review-traveling-channel.md](review-traveling-channel.md). The novelty audit found substantial prior mathematical overlap; do not advertise the exact spectral formula or monotonicity method as new. All exact claims below concern the specified conservative one-dimensional transport model. They are not claims of exactness for an arbitrary three-dimensional moving channel.

## Why pursue this direction

The local soft-hydraulics agenda proposes selective solute drift under zero mean fluid flux. A conservation constraint sharply limits this possibility for passive dissolved tracers. A more promising target is an arbitrary-amplitude theorem for dispersion controlled by a traveling deformation. The principal candidate is monotonicity in squared wave speed, with exact shape-dependent bounds and a unique suppression-to-enhancement crossover.

Relevant fit: Purdue's [Narsimhan profile](https://engineering.purdue.edu/ChE/people/ptProfile?resource_id=169352) includes fundamental transport, colloids, and non-Newtonian fluids; the [Purdue soft-matter proposal](https://engineering.purdue.edu/Engr/Research/GilbrethFellowships/ResearchProposals/2025-26/particles-polymers-and-compliant-boundaries-at-the-intersection-of-fluid-mechanics-and-soft-matter-) explicitly includes compliant boundaries and channel deformation for sorting particles.

## Model and assumptions

Let `A(x,t)>0` be the area of a channel, or the mobile pore volume per unit axial length. Let `q(x,t)` denote its solvent volume flux. For passive concentration `c` per mobile fluid volume, assume

\[
A_t+q_x=0,\qquad (Ac)_t+(qc)_x=(ADc_x)_x,\tag{1}
\]

where `D>0` is constant. There is no adsorption, reaction, selective wall permeability, solute exclusion, thermodynamic force, or independent solid-bound transport. The spatial domain is an infinite periodic channel, interpreted through its periodic cell and lifted particle displacement. Smooth strictly positive periodic coefficients ensure ellipticity and a unique invariant cell law. Finite reservoirs and spatially localized forcing require separate analysis.

Equation (1) is the leading Fickian long-wave model, before substantial Taylor shear dispersion. Constant `D` can describe rapid transverse mixing or a plug-flow approximation. A speed-dependent Taylor coefficient cannot simply be substituted into the monotonicity proof below.

## Conservation constraint: no selective asymptotic drift

For any space-time periodic geometry satisfying (1), the total cell volume `V=∫_0^L A dx` is constant. The cell density of a single tracer is `ρ=A/V`, since `c=1/V` solves (1). Thus its asymptotic laboratory drift is

\[
U_{\rm eff}=\frac1{VT}\int_0^T\!\int_0^L q(x,t)\,dx\,dt.\tag{2}
\]

For completeness, writing the density equation for `ρ=Ac` gives the Itô drift `b=q/A+D A_x/A`; the contribution `∫ D A_x/V dx` vanishes. Formula (2) is the invariant-cell drift, hence the long-time drift of a localized packet under standard ergodicity. The coefficient `D` does not appear.

Uniform `c` is not merely a formal solution: for `w=c-c̄`, with `c̄` the conserved cell-volume weighted mean,

\[
\frac d{dt}\frac12\int_0^L A w^2dx=-D\int_0^L A w_x^2dx.
\]

A weighted Poincaré inequality gives exponential cell mixing when `A` is bounded above and away from zero. Species may have different dispersion and different transient centroid shifts, but zero time-averaged solvent throughput gives zero asymptotic drift for every such dissolved species. This conclusion does not rule out enhanced clearance to absorbing boundaries or transport with sorption, excluded-volume effects, permeation, or nonuniform external forces.

This constraint is likely a known consequence of conservative homogenization, not a standalone novelty claim. It should prevent misleading interpretations of a finite-time bolus shift as persistent pumping.

## Traveling area with zero mean throughput

Specialize to

\[
A(x,t)=A(\xi),\quad \xi=x-vt,\quad A(\xi+L)=A(\xi),
\quad \bar A=L^{-1}\int_0^L A(\xi)d\xi.
\]

Mass conservation fixes `q=vA+C`. Choose

\[
q(\xi)=v[A(\xi)-\bar A],\tag{3}
\]

so the time-averaged flux through every fixed section is zero. This condition may require an imposed mean opposing pressure load; it is not generally the zero-pressure-drop peristaltic experiment. The theorem applies to prescribed traveling geometry with that flux, independent of how the shape or pressure load is implemented.

Define `a=A/Ā` and the volume coordinate

\[
s=S(\xi)=\int_0^\xi a(z)dz,\qquad S(\xi+L)=S(\xi)+L.
\]

In this coordinate equation (1) becomes

\[
c_t=v c_s+\partial_s[d(s)c_s],\qquad d(s)=D a(\xi(s))^2.\tag{4}
\]

The density in `s` is proportional to `c`, and its invariant distribution is uniform. The lifted laboratory coordinate `x` differs from `s+vt` by the bounded periodic function `ξ-S(ξ)`. Consequently their asymptotic diffusivities agree. The moving-coordinate backward generator and mean velocity are

\[
\mathcal L_v f=(d'-v)f'+df'',\qquad U_s=-v.
\]

All following averages `⟨·⟩_s` are normalized uniform `s`-averages.

## Exact cell problem and energy identity

Let `χ_v` be the unique mean-zero periodic solution of

\[
-(d\chi_v')'+v\chi_v'=d'.\tag{5}
\]

The standard martingale corrector gives

\[
D_{\rm eff}(v)=\left\langle d(1+\chi_v')^2\right\rangle_s.
\tag{6}
\]

Multiplying (5) by `χ_v` and integrating yields

\[
\langle d(\chi_v')^2\rangle_s=-\langle d\chi_v'\rangle_s,
\]

because the drift term is skew. Therefore

\[
D_{\rm eff}(v)=\langle d\rangle_s-
\langle d(\chi_v')^2\rangle_s.\tag{7}
\]

The upper bound follows immediately. Cauchy-Schwarz applied to (6), using `⟨1+χ'⟩=1`, gives the harmonic lower bound. In the physical area coordinate,

\[
\boxed{\frac{D}{\bar A\langle A^{-1}\rangle_x}
\ \le D_{\rm eff}(v)\le\
\frac{D\langle A^3\rangle_x}{\bar A^3}.}\tag{8}
\]

At `v=0`, `d(1+χ_0')` is constant, so the lower bound is attained exactly. The upper bound is approached as `|v|→∞` within model (1). If `A` is nonconstant, the upper bound cannot be attained at any finite `v` because zero corrector dissipation would force `d'=0` in (5).

## Monotonicity theorem and spectral representation

On the mean-zero periodic Hilbert space, define

\[
\mathcal A=-\partial_s d\partial_s,\quad B=\partial_s,
\quad C=\mathcal A^{-1/2}B\mathcal A^{-1/2},
\quad g=\mathcal A^{-1/2}d'.
\]

The operator `𝒜` is positive self-adjoint and `C` is bounded, compact, and skew-adjoint. From (5), with `h=𝒜^{1/2}χ_v`,

\[
(I+vC)h=g.
\]

The energy in (7) consequently is

\[
\|h\|^2=\langle g,(I-v^2C^2)^{-1}g\rangle.
\]

Writing `T=-C²≥0`, spectral calculus yields a finite positive measure `μ_g` with

\[
\boxed{D_{\rm eff}(v)=\langle d\rangle_s-
\int_{[0,\infty)}\frac{d\mu_g(\lambda)}{1+v^2\lambda}.}\tag{9}
\]

`C` has trivial kernel: `Cz=0` implies `∂_s𝒜^{-1/2}z=0`; the mean-zero condition then gives `z=0`. Thus the measure has no atom at zero. Dominated convergence proves the high-speed endpoint asserted above. For nonconstant `d`, `g≠0` and its spectral measure is nonzero on positive `λ`, so `D_eff` is strictly increasing as a function of `v²`.

Equation (9) also shows that `D_eff(√r)` is an increasing concave function of `r≥0`; all higher derivative signs alternate. The deficit from its high-speed bound is a Stieltjes function of `r`. This gives stronger constraints on admissible data fits than monotonicity alone.

By strict Jensen inequalities, the lower endpoint is below `D` and the upper endpoint is above `D` for every nonconstant area. Continuity and strict monotonicity therefore establish one and only one finite positive crossover speed `v_*` such that `D_eff(v_*)=D`. Reversing wave direction leaves dispersion unchanged even for an asymmetric shape.

## Small-amplitude consistency check

For `A=Ā[1+ε cos(kξ)]`, `|ε|≪1`, direct perturbation gives

\[
\frac{D_{\rm eff}}D=1+\frac{\epsilon^2}{2}
\frac{3v^2-D^2k^2}{v^2+D^2k^2}+O(\epsilon^4),\tag{10}
\]

where the even remainder follows because changing `ε` to `-ε` is a phase translation. Thus `v_*=Dk/√3+O(ε²)`, the static limit is `1-ε²/2`, and the high-speed limit is `1+3ε²/2`. The suppression/enhancement mechanism itself is already present in perturbative work; the candidate novelty is the arbitrary-amplitude global theorem and its spectral constraints.

## Physical validity of large speed

The limit `|v|→∞` is a mathematical endpoint of (1). At fixed transverse dimension `h`, the leading cross-sectional mixing approximation eventually fails. A physically meaningful plateau requires the distinguished regime

\[
1\ll \frac{|v|L}{D}\ll (L/h)^2
\]

up to shape-dependent factors: wave variation must remain slow compared with transverse diffusion. Neglect of Taylor dispersion can require a stronger condition, roughly `u h/D≪1` for the relevant velocity amplitude; because `u` scales with `v` at fixed shape, a safe regime is `1≪|v|L/D≪L/h`. Long slender channels can have a nonempty such interval. Near closure or extreme area contrast changes these conditions. The exact theorem does not establish monotonicity of the full three-dimensional Taylor dispersion at unrestricted frequency.

## Closest located prior art and outstanding novelty checks

1. [Marbach and Alim, Physical Review Fluids 4, 114202 (2019)](https://wigglylab.marbach.fr/documents/PRF_2019_Marbach.pdf), *Active control of dispersion within a channel with flow and pulsating walls*. Their conservative moving-area equation is directly relevant; they analyze entropic reduction, shuttle dispersion, and Taylor dispersion for pulsating channels. Their reported mean drift is an accompanying mean fluid flux, so it does not contradict (2). The full PDF must be checked for any arbitrary-shape bound or global monotonicity statement before novelty is claimed.
2. [Jha et al., arXiv:2604.05592 (2026)](https://arxiv.org/abs/2604.05592), *Taylor dispersion in a soft channel*. Abstract inspected: pressure-coupled Winkler channel, steady and pulsatile transport, increased velocity and dispersion. Generic soft-channel dispersion is already an occupied direction.
3. [*Interactions enhance dispersion in fluctuating channels via emergent flows*, JFM (2023)](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/interactions-enhance-dispersion-in-fluctuating-channels-via-emergent-flows/3C2985E5FF19C76632A4D767C412A3AB). Open page inspected: distinguishes compressible ideal-gas tracers and incompressible solvent, and analyzes sinusoidal boundaries. Its incompressible transport formulas are a necessary comparison.
4. [*Colloidal transport phenomena in dynamic, pulsating porous materials* (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10706601/). Open page located; relevant general cell-problem formulation, not yet read in full.
5. General nonreversible-diffusion asymptotic-variance theory uses the same positive/skew decomposition as (9). The spectral argument alone should not be described as new mathematics. The transport transformation, area-moment bounds, arbitrary-amplitude crossover uniqueness, and experimental restrictions together are the candidate contribution.

## Further novelty audit: substantial mathematical prior overlap

[Guérin and Dean, *Force-induced dispersion in heterogeneous media*, Physical Review Letters 115, 020601 (2015)](https://arxiv.org/pdf/1507.04607), Appendix B, Eq. B12 on PDF page 6, already gives an exact positive Lorentzian Fourier sum for a periodic diffusivity under constant applied force. Eq. B13 gives the high-force endpoint. Their stochastic drift is `κ′+βFκ`, whereas ours is `d′−v` after volume transformation. A resistance-coordinate change connects these families; the explicit sum is therefore at least a close transformed version of existing theory. The paper also suggests reconstructing a spatial diffusivity from force-dependent dispersion; the loss of Fourier phases limits such reconstruction.

[Guérin and Dean, *Kubo formulas for dispersion in heterogeneous periodic nonequilibrium systems*, PRE 92, 062103 (2015)](https://arxiv.org/html/1509.02733v1), section VII, treats arbitrary one-dimensional periodic drift and diffusivity by exact integral formulas. This already covers the transformed channel model. [Duncan, Lelièvre, and Pavliotis, J. Stat. Phys. 163, 457–491 (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4939425/) supplies the general positive/skew operator method used in (9), including reduction of asymptotic variance with increasing irreversible drift.

The [2019 Marbach–Alim paper](https://wigglylab.marbach.fr/documents/PRF_2019_Marbach.pdf), PDF pages 12 and 26–27, uses a small sinusoidal area modulation and obtains (10) as the non-Taylor part of Eq. F9. Appendix F obtains zero drift after moving-frame subtraction for that intermediate flux convention, then adds a mean inlet current in F12. The nonzero final drift must therefore not be compared with a strictly zero-throughput model without matching the inlet convention. [Wang, Dean, Marbach, and Zakine, JFM (2023)](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/interactions-enhance-dispersion-in-fluctuating-channels-via-emergent-flows/3C2985E5FF19C76632A4D767C412A3AB), Eq. 2.24, explicitly reproduces (10), while section 2.3.2 uses zero mean pressure drive, which permits peristaltic volume transport.

The remaining candidate contribution is a compact arbitrary-amplitude application to loaded traveling channels, with physical area bounds, unique crossover, identifiability limits, and shape-design consequences. No claim of publishability or exhaustive literature clearance is made.

## Direct numerical check

A second-order central-difference solve in the original traveling coordinate used `L=2π`, `D=1`, `A=1+0.55 cos ξ+0.17 sin 2ξ`, and 2,400 periodic grid points. Define `w=1+χ_x′` in that coordinate; it satisfies `D(Aw)′−vw=−vA`, `⟨w⟩=1`, and `D_eff=D⟨Aw²⟩/Ā`. The direct matrix solve confirmed the independently derived volume-coordinate bounds and monotonicity:

| Wave speed | Effective diffusivity |
| ---: | ---: |
| 0 | 0.8081769052 |
| 0.1 | 0.8165667294 |
| 0.3 | 0.8759087926 |
| 1 | 1.1616063670 |
| 3 | 1.4107122280 |
| 10 | 1.4865508905 |
| 100 | 1.4969891015 |

The exact endpoint bounds are `0.8081769052` and `1.4971`. The computed mean of `w` differed from 1 by less than `5×10⁻¹⁵`. This is a consistency check, not a replacement for the proof or independent mesh convergence.

## Exact inverse counterexample: different channels, identical full speed response

The independent review simplifies (9) to an explicit Fourier formula. Set

\[
\mathcal T=\int_0^L\frac{ds}{d(s)},\quad
r(s)=\int_0^s\frac{du}{d(u)},\quad
d(s(r))=\sum_{n\in\mathbb Z}d_n e^{2\pi inr/\mathcal T}.
\]

Then

\[
D_{\rm eff}(v)=\frac L{\mathcal T}
+\frac{\mathcal T}L\sum_{n\ne0}|d_n|^2
\frac{v^2}{v^2+(2\pi n/\mathcal T)^2}.\tag{11}
\]

One derivation sets `g=d(1+χ′)`; its equation is `g_r−vg=−vd`, so each nonzero Fourier mode is solved independently. Parseval's identity gives (11). The `n=0` mode equals `L/𝒯`.

Thus the whole speed-response curve contains Fourier magnitudes and no Fourier phases. Importantly, the nonlinear coordinate transformation back to a channel must preserve the same molecular diffusivity and physical period. The following construction meets those constraints exactly.

Work in dimensionless units and choose any molecular diffusivity `D>0`. On a resistance-coordinate circle of length 12, let `b(r)` be a nonnegative smooth bump supported on `|r|<δ`, where `0<δ<1/2`, with one strict maximum. Periodize it with period 12. Choose `η>0` and the two sets

\[
P=\{0,1,4,6\},\qquad Q=\{0,1,3,7\}.
\]

For `E=P,Q`, define

\[
f_E(r)=1+\eta\sum_{j\in E}b(r-j).
\]

The bumps have disjoint supports. Therefore `f_P` and `f_Q` have identical distributions of values and identical moments of every function of `f`. In particular define their common moments `m_1=⟨f_E⟩_r` and `m_{1/2}=⟨√f_E⟩_r` and set

\[
\alpha=D(m_{1/2}/m_1)^2,\qquad d_E(r)=\alpha f_E(r),
\quad L=12\alpha m_1.
\]

Define the physical axial coordinate and normalized area by

\[
\xi_E(r)=\sqrt D\int_0^r\sqrt{d_E(u)}\,du,
\qquad a_E(\xi_E(r))=\sqrt{d_E(r)/D}.
\tag{12}
\]

The coordinate is a smooth increasing bijection, and

\[
\xi_E(12)=12\sqrt{D\alpha}\,m_{1/2}=L,
\quad \int_0^L a_E(\xi)d\xi=\int_0^{12}d_E(r)dr=L.
\]

Thus both physical channels have the same period and the same mean normalized area 1. Any desired physical mean area `Ā` can multiply both `a_E` without changing the normalized transport formulas.

The ordered cyclic difference counts of both point sets are exactly

\[
(N_0,N_1,\ldots,N_{11})=(4,1,1,1,1,1,2,1,1,1,1,1).
\]

Hence

\[
\left|\sum_{j\in P}e^{-2\pi i n j/12}\right|^2
=\left|\sum_{j\in Q}e^{-2\pi i n j/12}\right|^2
\]

for every integer `n`. Convolution with the identical bump preserves this equality, so `|(d_P)_n|=|(d_Q)_n|` for all `n`. Equation (11) now proves

\[
\boxed{D_{{\rm eff},P}(v)=D_{{\rm eff},Q}(v)
\quad\hbox{for every real }v.}\tag{13}
\]

Both channel drifts are zero. Their static diffusivities and high-speed plateaus also coincide.

The physical area distributions also coincide: for every integrable function `F`,

\[
\int_0^L F(a_E(\xi))d\xi
=\sqrt D\int_0^{12}F(\sqrt{d_E(r)/D})\sqrt{d_E(r)}dr.
\]

The right side depends only on the common distribution of `d_E`. Consequently every area moment agrees. If local lubrication hydraulics has `q=−K(A)p_x` for a specified positive conductance function `K`, both shapes also require the same pressure drop for the zero-throughput traveling protocol and dissipate the same hydraulic power:

\[
\Delta p_E=-v\int_0^L\frac{A_E-\bar A}{K(A_E)}d\xi,
\qquad
\mathcal P_E=v^2\int_0^L\frac{(A_E-\bar A)^2}{K(A_E)}d\xi.
\]

Here `Δp=p(L)−p(0)` and `𝒫=∫q(−p_x)dx`; these are the axial hydraulic contributions, not a calculation of the full actuation energy of a deforming wall. Equality follows from the shared area histogram. Thus those additional global hydraulic measurements do not distinguish the two shapes either, within the same local-conductance model.

These physical channels are not translates or reflections. The cyclic gaps between bump centers in resistance coordinate are `(1,3,2,6)` for `P` and `(1,2,4,5)` for `Q`. Under (12), each gap is multiplied by the same baseline factor `√(Dα)` and receives the same bump correction. The two gap multisets remain different, so no translation or reflection can identify the physical geometries.

The homometric point sets are classical, not a new combinatorial discovery: see [Amiot and Sethares, *An Algebra for Periodic Rhythms and Scales*, Example 9](https://sethares.engr.wisc.edu/paperspdf/AlgofScales.pdf). The transport consequence is a rigorous limit on inverse use of dispersion measurements: even an exact response at all wave speeds, known molecular diffusivity, known period, and known mean area cannot identify channel shape. Additional data must contain spatial phase information. Merely extending the speed sweep cannot fix this nonuniqueness.

The same phase obstruction applies directly to the constant-force diffusivity reconstruction suggested below Eq. B12 of Guérin–Dean (2015). A claim that the *power spectrum* can be recovered is plausible under ideal data; unique reconstruction of the *field* does not follow. Novelty is limited to making this inverse-transport obstruction explicit and preserving all physical channel constraints; phase retrieval and homometry are established subjects. Independent verification of this new subsection remains pending.
