# Prior-art audit: optimal disorder moments and a change of design scale

Literature audit, 2026-09-07. This note assesses [risk-sensitive-mobility.md](risk-sensitive-mobility.md). Its subject is novelty, not an independent certification of the mathematical proof. The source note currently establishes matching orders and leaves general sharp constants and limiting optimizers open.

## Assessment

No inspected primary source contains the proposed `q=8/5` threshold or its critical logarithm for the random cosine killing problem. No general theorem was found whose assumptions and conclusion directly imply all three small-budget orders. The claim remains plausibly original at the level of this singular operator and design problem.

There are substantial precedents beyond expected-compliance optimization. General risk measures have already been incorporated into optimal conductivity design, with homogenization and stationarity theory. Resource-constrained spatial design has also long been known to change heavy tails when the objective penalizes large losses. Rare bifurcations producing moment-dependent powers are established. These facts narrow the contribution to the particular transition, the logarithmic correction, and the uniform lower and constructive upper bounds that establish them.

## Statement being compared

For one deterministic mobility field selected before observing `c`, define

\[
\Phi_q(M)=\inf_{D\ge0,\,\int D=M}
\mathbb E_c\left[\langle1,
[-\partial_sD(s)\partial_s+(c+\cos s)^2]^{-1}1\rangle^q\right],
\qquad c\sim\mathrm{Uniform}[-2,2].
\]

The proposed result on the circle of length `2π` is

\[
\Phi_q(M)\asymp
\begin{cases}
M^{-q/4},&0<q<8/5,\\
M^{-2/5}[\log(1/M)]^{7/5},&q=8/5,\\
M^{(2-3q)/7},&q>8/5.
\end{cases}
\]

Constants implicit in `asymp` may depend on fixed `q`, but not on `M`. This is an unrooted moment. Taking its `q`th root changes the displayed powers and leaves the minimizing designs unchanged. Orders `q>1` penalize large responses through convex loss; `q<1` should not be called risk aversion merely because the objective is a moment. The functional is not the usual exponential criterion sometimes called risk-sensitive control.

The formal fixed-shape allocation is

\[
D(s)/M\propto|\sin s|^{-\alpha_q},
\qquad \alpha_q=(6q-4)/(q+4).
\]

Its integrability fails at `q=8/5`. The source note replaces it with budget-dependent rounded profiles. Above the threshold, profiles centered at the two known fold locations have radius of order `M^(1/7)` and algebraic tails that regularize ordinary roots elsewhere. A compactly supported fold patch alone would leave a positive measure of offsets with infinite response.

## Closest general theorem: risk-averse conductivity design

Alphonse, Kunštek and Vrdoljak, *Optimal design with uncertainties: a risk-averse approach* (2026), study risk functionals of elliptic responses for mixtures of two conducting materials. They establish relaxed existence through homogenization and derive first-order conditions, with CVaR-based numerical compliance examples. Equations (1)–(2) fix two positive conductivities `0<α<β`; randomness enters the forcing. Section 2 imposes assumptions on the risk functional, including convexity. This is a close general framework, but it does not include the present unrestricted `L¹` mobility class with zero baseline, random vanishing reaction field, or the singular small-budget limit. Its existence and stationarity results therefore do not directly yield the stated powers or logarithm. [Open full text](https://arxiv.org/html/2602.19869v1), [WIAS preprint 3262](https://www.wias-berlin.de/preprint/3262/wias_preprints_3262.pdf).

Buttazzo and Maestre, *Optimal Shape for Elliptic Problems with Random Perturbations* (2010 preprint; 2011 publication), provide the earlier expected-cost conductivity framework with random forcing. Theorem 4, equation (16), gives the expected state-adjoint gradient sensitivity, reducing to the expected squared gradient for compliance. Thus balancing spatially averaged gradient costs against a material budget is established. [Open paper](https://arxiv.org/pdf/1002.2770).

Buttazzo, Oudet and Velichkov, *A free boundary problem arising in PDE optimization* (2015), give the mass-constrained reinforcement and gradient-constraint duality used in the deterministic local design. This is an established source of the variational structure rather than a collision with the risk-order transition. [Open paper](https://arxiv.org/pdf/1506.00141). Additional expected-compliance and information-timing precedents are documented in [robust-design-prior-art.md](robust-design-prior-art.md).

## Close physical concept: optimized tolerance changes heavy tails

Newman, Girvan and Farmer, *Optimal design, robustness, and risk aversion* (2002), solve a spatial forest-fire design model with a prescribed distribution of ignition locations and a resource cost for firebreaks. Equations (1)–(5) derive the allocation and power-law loss distribution. Equations (15)–(18) then replace average loss by nonlinear expected utility under a fixed resource constraint. Risk aversion changes the large-loss tail. This directly precedes the general claim that changing risk preference changes the allocation and resulting extreme-event statistics. It uses local patch sizes and geometric resource costs, not a diffusion-resolvent response. It does not state the current threshold or logarithmic budget law. [Open paper](https://arxiv.org/pdf/cond-mat/0202330), [published article](https://doi.org/10.1103/PhysRevLett.89.028301).

This precedent should appear in a broader physics introduction. It prevents presenting the contrast between average performance and protection against rare large responses as a newly discovered engineering principle. The mathematical result here supplies a different, explicitly specified transport mechanism and its resource asymptotics.

## Rare bifurcations and moment transitions are established

Berry, Keating and Schomerus, *Universal twinkling exponents for spectral fluctuations associated with mixed chaology* (2000), derive parameter-averaged spectral moment powers by balancing the enhanced response near a bifurcation against its shrinking parameter-space volume. Equations (18)–(19) make that competition explicit. Their operator statistics are oscillatory quantum spectral fluctuations; they do not optimize a spatial diffusivity. [Open author paper](https://www.lorentz.leidenuniv.nl/beenakkr/mesoscopics/fulltext/schomerus00.pdf).

Keating, Ozorio de Almeida, Prado, Sieber and Vallejos, *Periodic orbit bifurcations and scattering time delay fluctuations* (2007), apply the same principle to time-delay moments in open quantum systems. This strengthens the transport-related precedent for moment-dependent rational powers. It supplies no conductivity-design threshold. [Open paper](https://arxiv.org/pdf/nlin/0701025). Further comparisons with squared potentials, localization landscapes and noisy saddle nodes are in [random-barrier-prior-art.md](random-barrier-prior-art.md).

## What follows from elementary allocation, and what does not

For a regular fixed shape, the local quadratic-well law formally reduces the problem to

\[
M^{-q/4}\int w_q(s)d(s)^{-q/4}\,ds,
\qquad w_q(s)=|\sin s|^{1-3q/2},\qquad\int d=1.
\]

The general identity

\[
\inf_{\int d=1}\int wd^{-p}
=\left(\int w^{1/(p+1)}\right)^{p+1}
\]

when the displayed integral is finite is elementary Hölder allocation. Substituting `p=q/4` predicts `α_q` and the `8/5` integrability threshold. Therefore neither the power-law shape nor discovery of its integrability limit is, alone, a strong theorem-level novelty claim.

At criticality the spatial scales contribute comparable terms. If `N` disjoint scales share budget `M`, minimizing `Σ m_j^(-2/5)` gives `N^(7/5)M^(-2/5)`. With `N` of logarithmic order, this predicts the critical logarithm. That finite-dimensional allocation step is elementary too. The nontrivial content is deriving valid shell response bounds for the original operator, ensuring disjointness and budget accounting, and producing a matching globally admissible design. Existing general risk-design existence or stationarity theorems do not provide those estimates.

Above criticality the local dimensional balance is also straightforward once the appropriate fold model is identified: a region of radius `R` carrying budget `M` has diffusivity of order `M/R`; balancing its diffusion operator against quartic killing gives `M/R³∼R⁴`, hence `R∼M^(1/7)`. The response is of order `R^(-3)` and the offset layer has width `R²`, giving `R^(2-3q)`. Proving that every design obeys the matching lower bound remains essential; dimensional reasoning alone cannot rule out other allocations.

## Wording about localization needs care

The order theorem and the successful concentrated trial fields do not establish the limiting shape of exact minimizers or concentration of all order-optimal designs. A simple counterexample to the latter claim is to take a successful design using budget `M/2` and add a uniform field using the remaining `M/2`. Monotonicity of compliance ensures this combined design retains the proved optimal order, while half its normalized mobility remains diffuse.

Thus it is sound to describe the threshold as failure of the integrable fixed-shape allocation and the onset of an effective design construction concentrated near folds with nonzero tails. A claim that all optimal normalized mobilities converge to point masses needs an additional sharp compactness or rigidity theorem. The exact profiles and sharp constants above the threshold remain open in the current note.

## Recommended originality claim

Subject to independent correctness review, a defensible claim is: optimization over unrestricted mobility fields shifts the disorder-moment transition for an explicit reversible transport model from `4/3` to `8/5`, and at the new threshold the optimum has the critical factor `[log(1/M)]^(7/5)`. Matching upper and lower bounds identify all three orders despite arbitrary budget-dependent spatial structure.

Do not claim a new general method of risk-aware design, a new power-law allocation identity, or a general theorem that risk aversion causes localization. The physical and mathematical mechanisms have close predecessors; the specific singular transport law is the part not found in the inspected literature.

The search covered general risk measures in elliptic design, compliance moments, conductivity and reinforcement, optimized tolerance, critical allocation exponents, concentration in optimal design, and bifurcation-dominated moment laws. Failure to find an exact match is not proof of global originality. All conclusions remain restricted to this compact scalar ensemble; finite-bulk transfer, fixed fabrication constraints, and other random-field distributions require separate analysis.
