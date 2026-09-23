# Reservoir convergence from the support of the energy limit

Date: 2026-09-07. Status: theorem independently proved by two reviewers; see [the standalone proof check](verification/three-support-bath-review.md) and [the shared-bath review](verification/shared-bath-review.md). This strengthens the earlier three-phase theorem by removing all local Gaussian, density, and moment assumptions. Its novelty remains provisional within the finite-reservoir audit; the necessity proof is a specific strict-concavity argument, while quadratic sufficient bounds have established predecessors.

## Theorem

Let P_N be a canonical state law at a fixed inverse temperature β>0, with real-valued energy E_N. Suppose there are centers a_N and scales b_N→∞ for which

\[
 X_N=\frac{E_N-a_N}{b_N}\ \Rightarrow\ X,
\]

where the limiting probability law has at least three distinct points in its support. The limit can be discrete, continuous, or mixed. No moments or density are assumed.

Couple the subsystem to an exact bath with surface density of states U^(c_N)1_(U>0), c_N>0. Its marginal at a tunable composite energy T_N is

\[
 \frac{dQ_N}{dP_N}
 =\frac{e^{\beta E_N}(T_N-E_N)_+^{c_N}}{Z_N},
\]

with the numerator interpreted as zero above the cutoff. Then

\[
 \boxed{\quad
 \exists\,T_N:\ \|Q_N-P_N\|_{\rm TV}\to0
 \quad\Longleftrightarrow\quad \frac{c_N}{b_N^2}\to\infty.
 \quad}\tag{1}
\]

Energy units are fixed. In dimensional comparisons the relevant combination is β²b_N²/c_N. Since the likelihood depends only on energy, full-state and energy-law total variation agree.

## Sufficiency uses only tightness

Set T_N=a_N+c_N/β and remove the constant log-weight at E=a_N. For y=β(E-a_N)/c_N the relative weight is

\[
 W_N(E)=e^{c_N y}(1-y)^{c_N}\mathbf1_{y<1}.
\]

The inequality log(1-y)≤-y gives 0≤W_N≤1 globally. Since X_N is tight and c_N≫b_N²,

\[
 \log W_N
 =-\frac{\beta^2b_N^2X_N^2}{2c_N}
 [1+o_{P_N}(1)]\to0
\]

on the event below the cutoff, whose probability tends to one. Thus W_N→1 in probability. Bounded convergence gives E_P W_N→1 and E_P|W_N-1|→0; normalization proves TV convergence. Heavy tails do not invalidate this argument, because the bath weight never exceeds one under this calibration.

## Necessity from three typical energies

Assume some sequence T_N achieves TV convergence. Choose three ordered, disjoint, bounded continuity intervals of the limiting X law, each with positive probability and with strictly positive gaps. With probability bounded below, E_N lies in each corresponding translated and rescaled interval.

TV convergence means the normalized likelihood R_N=dQ_N/dP_N converges to one in P_N-probability. Consequently one can select an energy e_i,N in each interval for which

\[
 \log R_N(e_{i,N})\to0,\qquad i=1,2,3.
\]

These energies are below the bath cutoff, because their likelihood is positive. Let

\[
 \Delta_N=e_{3,N}-e_{1,N}=\Theta(b_N),\qquad
 \theta_N=\frac{e_{2,N}-e_{1,N}}{\Delta_N}\in[\delta,1-\delta]
\]

for a fixed δ>0. Define

\[
 q_N=\log\frac{T_N-e_{1,N}}{T_N-e_{3,N}}>0.
\]

Equality of the two endpoint log likelihoods in the limit gives

\[
 c_Nq_N=\beta\Delta_N+o(1).\tag{2}
\]

The linear energy term and log normalization cancel from the middle-point chord gap. Its exact value is

\[
 c_N f_{\theta_N}(q_N)\to0,\qquad
 f_\theta(q)=\log[(1-\theta)e^q+\theta]-(1-\theta)q.
\tag{3}
\]

Uniformly for θ∈[δ,1-δ] and q>0,

\[
 f_\theta(q)\ge C_\delta\min\{q^2,q\}.\tag{4}
\]

Indeed f(0)=f'(0)=0, and

\[
 f_\theta''(q)=\frac{\theta(1-\theta)e^q}
 {[(1-\theta)e^q+\theta]^2}
\]

has a uniform positive lower bound for 0≤q≤1. Twice integrating gives the quadratic bound there. Convexity and f(0)=0 imply that f(q)/q is nondecreasing, extending the bound linearly for q≥1.

Equation (2) gives c_Nq_N=Θ(b_N)→∞. Equations (3)–(4) therefore force q_N→0. They then imply c_Nq_N²→0. Combining this with (2) yields Δ_N²/c_N→0, and hence b_N²/c_N→0. This proves necessity for every positive bath exponent and every admissible total-energy tuning.

The argument does not require likelihood convergence at a preselected phase center. It selects typical energies with good likelihood and uses an exact chord identity, so discrete energies and non-Gaussian limits cause no difficulty.

## Why two support points are exceptional

For an exactly two-atom energy law supported at e_1<e_2, any positive c can reproduce the complete law exactly. Set Δ=e_2-e_1 and

\[
 T=e_2+\frac{\Delta}{e^{\beta\Delta/c}-1}.
\tag{5}
\]

Then βe_1+c log(T-e_1)=βe_2+c log(T-e_2); both atom weights are multiplied by the same factor. Their probabilities are unchanged. Thus a two-point limiting law cannot, by itself, imply a quadratic bath-size requirement.

Real two-phase systems have fluctuations within their phase peaks. Resolving those fluctuations supplies the additional obstruction and can give the intermediate N^(3/2) scale. For example, an extensive phase separation Δ_N∼N and nondegenerate phase widths √N give that scale under the reviewed local assumptions. This is consistent with (1): the energy limit at scale N has exactly two support points, so (1) deliberately does not apply.

## Consequences and claim boundaries

- A nondegenerate ordinary Gaussian energy limit on scale b_N=√N gives the familiar condition c_N≫N, now as a necessary and sufficient full-law statement under arbitrary total-energy tuning.
- Three or more macroscopic energy phases on scale b_N=N give c_N≫N² using only macroscopic phase concentration and positive limiting weights. The earlier Gaussian assumptions for this case were unnecessarily strong.
- A continuous non-Gaussian energy limit at a critical scale b_N gives c_N≫b_N² under the same theorem. Establishing that energy limit for a physical model is a separate task; no new critical exponent is claimed here.
- Two independent two-phase systems have three total-energy support points. This gives a quadratic joint-law requirement and leads to the distinct shared-bath phenomena in [the correlation note](shared-bath-phase-correlations.md).

These statements refine the accuracy of a specified physical bath in a strong probability metric. They do not equate full-law accuracy with agreement of thermodynamic potentials or local observables. They also do not extend to baths with arbitrary nonconcave entropy, independently adjustable chemical fields, or interactions that modify the subsystem Hamiltonian.

The same proofs apply to a specified target sequence β_N→β>0, using β_N in each bath calibration. This permits a finite-size equal-phase-weight temperature sequence. It does not allow the bath to change the target law after the accuracy criterion is chosen.

The [existing prior-art audit](verification/physical-reservoir-novelty-audit.md) documents general quadratic sufficient bounds and quantitative conditioning results. The narrower candidate here is the matching necessity after all thermal calibrations, using only three support points of a weak energy limit. A failed literature search does not establish priority.

## A two-scale necessity corollary without Gaussian assumptions

The chord bound can also retain its dependence on unequal spacings. Uniformly for all 0<θ<1 and q>0,

\[
 f_\theta(q)\ge\frac{\theta(1-\theta)}{2e}
 \min\{q^2,q\}.\tag{6}
\]

For 0≤q≤1 the displayed second derivative is at least e^(-1)θ(1-θ); twice integration gives the bound. Convexity again extends it to q≥1.

Suppose two positive-mass canonical phases are separated by Δ_N, and within at least one phase the energy centered at its phase location, divided by s_N, has a weak limit with at least two distinct support points. Assume s_N→∞ and s_N=o(Δ_N). The other phase must remain concentrated on a scale o(Δ_N). No local density limit is required.

Select two good-likelihood energies from separated fluctuation neighborhoods in the first phase and one from the other. Their outer gap is Θ(Δ_N), one inner gap is Θ(s_N), and θ(1-θ)=Θ(s_N/Δ_N). Equations (2)–(3) and (6) give a vanishing chord gap bounded below by a positive constant times

\[
 \min\{\Delta_Ns_N/c_N,s_N\}.
\]

Since s_N diverges, TV convergence requires

\[
 \boxed{c_N\gg\Delta_Ns_N.}\tag{7}
\]

Thus the N^(3/2) necessary scale needs only nondegenerate weak fluctuations on scale √N, not Gaussian densities. An independent [review](verification/shared-bath-review.md) verifies the uniform chord estimate and corollary. Sufficiency still needs control of the amplified interphase region; the [positive-decomposition criterion](phase-decomposition-reservoir-criterion.md) provides one route. The pure nearest-neighbor Potts application in [the short-range note](short-range-potts-route.md) uses a uniform variance bound to establish nondegenerate spin fluctuations without adding kinetic variables.
