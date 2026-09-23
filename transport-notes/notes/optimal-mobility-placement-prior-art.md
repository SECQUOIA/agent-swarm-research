# Prior-art audit: optimal placement of a surface mobility budget

Audit date: 2026-09-06. The candidate supplied for review is the minimization

\[
J(D)=\langle1,[-\partial_sD(s)\partial_s+k(s)]^{-1}1\rangle,
\qquad D\ge0,\quad\int D(s)\,ds=M.
\]

This note audits novelty only. The proposed explicit optimizer is being verified independently; its reproduction below does not certify it.

The general optimization method has a close precedent in **optimal reinforcement and minimum compliance**. Fixed total conductivity, an \(L^\infty\) gradient dual, and conductivity supported where the optimal gradient saturates are established. The plausible new contribution is the exact design law near a quadratic exchange minimum and its consequence for singular channel dispersion. I found no exact match for the stated profile or its \(M^{-1/5}\) asymptotic in the accessible literature searched.

## Proposed result and comparisons

For \(k(s)=as^2\) on the whole line, the proposed optimizer is

\[
R=\left(\frac{80M}{3a}\right)^{1/5},\qquad y=|s|/R,
\]

\[
D_*(s)=\frac{aR^4}{8}y(1-y)^2(1+2y)\quad(0\le y<1),
\qquad D_*(s)=0\quad(y\ge1).
\]

Its proposed resolvent solution is \(h_*=(9-8y)/(aR^2)\) inside the active interval and \(h_*=1/(as^2)\) outside, giving

\[
J_{\min}=\frac{12}{aR}=12(3/80)^{1/5}a^{-4/5}M^{-1/5}.
\]

The corresponding claimed dual is

\[
\sup_h\left[2\int h\,ds-\int k(s)h(s)^2\,ds-M\|h'\|_\infty^2\right].
\]

The exact profile is a compactly supported, quartic mobility function with a zero at the center as well as at the outer endpoints. This distinguishes it from the elementary uniform-mobility oscillator calculation. Its physical admissibility must be discussed through the divergence-form diffusion model and the allowed degeneracy of \(D\).

The uniform-mobility comparison requires a **finite perimeter \(P\)**, where \(D=M/P\). There is no nonzero spatially uniform diffusivity with finite total budget on the whole line. A finite-domain localization theorem would justify comparing the small-budget laws \(M^{-1/5}\) and \(M^{-1/4}\). The former diverges more slowly as \(M\to0\); it is not a claim that the whole-line optimizer beats a finite-budget constant function on that same line.

## Closest mathematical precedent

**Buttazzo, Oudet, and Velichkov (2015), “A free boundary problem arising in PDE optimization.”** Their problem allocates nonnegative reinforcement \(\theta\) with fixed \(\int\theta=m\), minimizing compliance for conductivity \(1+\theta\). Proposition 4.1 gives the dual energy with \((m/2)\|\nabla u\|_\infty^2\). Equation (4.5) gives \(|\nabla u|\le c\) everywhere and equality on the support of reinforcement. Section 5 relates this to classical elastic-plastic torsion and provides explicit radial examples. The inspected formulation contains a baseline gradient energy, not the candidate's quadratic reaction term \(\int k h^2\), and uses bounded domains. Nevertheless, the duality and saturated-gradient design principle are direct precedents, not a prospective discovery here. [Open primary manuscript](https://arxiv.org/pdf/1506.00141).

**Bouchitté and Buttazzo (2001), “Characterization of optimal shapes and masses through Monge-Kantorovich equation,” J. Eur. Math. Soc. 3, 139–168.** This is an older foundation for optimal mass distribution and its equivalence, in scalar problems, to mass transport. The 2015 paper explicitly identifies its zero-background-conductivity counterpart with this work. The primary article is openly available. It supports citing an established transport-density interpretation of optimal conductivity rather than claiming a new principle of allocating mobility. I did not locate the quadratic-killing example in the inspected material. [Publisher article](https://ems.press/journals/jems/articles/123), [open full text](https://ems.press/content/serial-article-files/31487?nt=1).

**Buttazzo and Varchon (2005), “On the optimal reinforcement of an elastic membrane.”** This work optimizes a nonnegative *potential* or boundary stiffening term under a mass constraint. Its optimality condition caps the state amplitude, with saturation on the reinforcement support. It is a neighboring problem, not the same design variable: the current candidate holds the killing potential fixed and chooses the derivative coefficient. Avoid conflating these two meanings of “reinforcement.” [Author repository](https://cvgmt.sns.it/paper/1320/), [open manuscript](https://citeseerx.ist.psu.edu/document?doi=8d6dd97dc3d11138d72eca5739be24655ef48c91&repid=rep1&type=pdf).

## Cooling-fin precedent: fixed material plus a loss term

**Alexandersen and Sigmund (2021), “Revisiting the optimal thickness profile of cooling fins: A one-dimensional analytical study using optimality conditions.”** Their one-dimensional cooling-fin equation has a selectable conduction coefficient and a distributed convection loss. The fixed-volume optimum has constant temperature slope, finite optimal extent, and a polynomial thickness profile; it reproduces an older Duffin solution. Thus the combination of a loss term, limited conducting material, and explicit saturated-slope design also has a concrete engineering precedent. Their source is imposed at the base and their loss coefficient differs from the present distributed forcing and quadratic killing. I found no exact equivalence to the profile above. [Open author manuscript](https://joealexandersen.com/onewebmedia/research/conferences/ITherm2021/ITherm2021_revised.pdf), [institutional bibliographic record](https://orbit.dtu.dk/en/publications/revisiting-the-optimal-thickness-profile-of-cooling-fins-a-one-di/), [DOI](https://doi.org/10.1109/ITherm51669.2021.9503196).

Fin optimization with internal heat generation and variable heat-transfer coefficients has a large older literature. Search-accessible primary papers identify variational extensions beyond uniform loss and base forcing. Full inspection of those older extensions remains a gap; a broad assertion that no one has solved variable-conductivity design with reaction would be indefensible. One useful entry point is the literature discussion in [“Optimal design of a fin in steady-state”](https://www.sciencedirect.com/science/article/pii/S0307904X19305694).

## Related diffusion optimization with a different objective

**Jafarizadeh (2018), “Optimal Diffusion Processes,” IEEE Control Systems Letters 2, 465–470.** Optimizes convergence rate for a prescribed stationary distribution and average local variance. This gives a direct precedent for allocating spatial diffusivity while retaining equilibrium. Its objective is spectral-gap maximization, not the present resolvent-weighted dispersion/compliance. A 2024 arXiv posting is openly available; the underlying journal publication is from 2018. [Open manuscript](https://arxiv.org/abs/2412.20934), [DOI](https://doi.org/10.1109/LCSYS.2018.2843172).

**Bénichou et al. (2010), “Optimal reaction time for surface-mediated diffusion.”** Establishes optimization of surface/bulk search through the desorption rate in confinement. It is useful application context but does not optimize a spatial mobility field with a total-integral constraint. [Primary manuscript](https://arxiv.org/abs/1005.1522).

I found no adsorption or chromatography source with the particular fixed-budget spatial-mobility optimization near a smooth kinetic zero. Broader adsorption/surface-diffusion precedents and remaining historical access gaps are recorded in [singular-exchange-prior-art.md](singular-exchange-prior-art.md).

## Recommended novelty statement

| Claim | Status supported by this audit |
|---|---|
| Fixed-budget diffusivity optimization is a new mathematical framework | Not supportable. |
| The squared \(L^\infty\) gradient dual is new | Not supportable; direct reinforcement precedent. |
| Optimal conductivity is concentrated on maximal-gradient regions | Established design structure. |
| Polynomial profiles and compact active support are new in diffusion-with-loss design | Not supportable in general; cooling-fin precedent. |
| The explicit quartic optimizer for uniform source and quadratic killing is new | No matching result located; plausible new exact example, correctness pending independent review. |
| The small-budget \(M^{-1/5}\) transport law improves on uniform \(M^{-1/4}\) placement in a finite heterogeneous channel | Plausible substantive contribution if a localization theorem and physical design assumptions are proved. |

The most defensible framing is an exact application and extension of established optimal-reinforcement methods to a singular adsorption-transport problem. Stronger impact would come from a theorem that transfers the local optimum to a finite channel, treats several exchange minima, and states the consequences of a positive background diffusivity or a realizable upper bound. The exact whole-line example alone is likely a useful theoretical result, but the literature audit does not establish a new general optimization principle or certify publication novelty.
