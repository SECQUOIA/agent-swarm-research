# A positive phase-decomposition criterion for reservoir convergence

Date: 2026-09-06. Status: a sufficient-condition lemma supporting the short-range investigation, approved in [independent review](verification/phase-decomposition-review.md). This is not a claim that a particular short-range model satisfies the hypotheses.

The physical two-phase theorem currently uses a pointwise density envelope in the energy valley. A positive decomposition into phase laws offers an alternative that can fit contour arguments more naturally. An approximation to a partition function alone is insufficient: the decomposition here concerns positive probability measures and energy fluctuations within each component.

Let a canonical energy law admit

\[
 P_N=w_{-,N}P_{-,N}+w_{+,N}P_{+,N}+\delta_N R_N,
 \qquad w_{-,N}+w_{+,N}+\delta_N=1,
\]

with all terms nonnegative. The phase centers E_-,N and E_+,N have gap Δ_N∼ℓN, ℓ>0. Assume that for some fixed η>0 and M<∞,

\[
 \sup_{N,i\in\{-,+\}}\mathbb E_{P_{i,N}}
 \exp\left[\eta\frac{|E-E_{i,N}|}{\sqrt N}\right]\le M.\tag{1}
\]

No local limit theorem or density is needed for the sufficiency statement. Phase labels may be defined on an enlarged positive probability space, provided (1) concerns the actual exchanged energy, not an auxiliary bond count or another observable.

Use the physical bath ω_B(U)∝U^(c_N), c_N>0, and choose composite energy to balance residual log-weight at the two centers:

\[
 \mathcal E_N=E_{-,N}+\frac{\Delta_N}{1-e^{-\beta\Delta_N/c_N}}.
\]

Let h_N(E)=βE+c_N log(𝓔_N-E), with value -∞ above its cutoff, and subtract its common phase-center value. Suppose

\[
 \frac{c_N}{N^{3/2}}\to\infty,
 \qquad
 \delta_N\exp\left(C\frac{N^2}{c_N}\right)\to0\tag{2}
\]

for a sufficiently large fixed C depending on β and an upper bound for Δ_N/N. Then the normalized reweighted law converges to P_N in total variation.

## Proof

Concavity and endpoint calibration imply h_N≤0 outside the phase interval. Within it, curvature comparison gives max h_N≤CN²/c_N. The tangent at either phase center gives the global upper bound, including points outside the interval and below the bath cutoff,

\[
 h_N(E)\le h_N'(E_{i,N})(E-E_{i,N})
 \le\epsilon_N\frac{|E-E_{i,N}|}{\sqrt N},
 \qquad\epsilon_N=O(N^{3/2}/c_N)\to0.\tag{3}
\]

On every fixed standardized phase window h_N converges uniformly to zero; the cutoff lies far outside those windows. Equation (1) makes standardized phase energies tight. Thus e^(h_N) converges to one in phase probability. Equations (1) and (3) also make these weights uniformly integrable: for large N, e^(2h_N)≤exp[η|E-E_i,N|/√N]. Consequently E_(P_i,N)|e^(h_N)-1|→0 for each phase.

On the remaining positive component,

\[
 \delta_N\mathbb E_{R_N}|e^{h_N}-1|
 \le\delta_N\left[1+\exp(CN^2/c_N)\right]\to0.
\]

Summing the components gives E_(P_N)|e^(h_N)-1|→0. Its normalization tends to one, which proves total-variation convergence.

## Scaling consequences and limits

If δ_N≤exp(-s_N), with s_N→∞, a simple sufficient condition is

\[
 c_N\gg\max\{N^{3/2},N^2/s_N\}.\tag{4}
\]

If s_N≥b√N for a fixed b>0, the N^(3/2) condition alone suffices. For a two-dimensional torus N=L², an exponentially small exceptional-event probability exp(-bL) therefore tolerates the largest reservoir amplification at this scale. In higher dimensions an exp(-bL) estimate alone is weaker; surface-order exp[-bL^(d-1)] again suffices for d≥2.

Equation (4) is a sufficient criterion, not a sharp necessity claim based only on exceptional mass. A rare component may sit near the endpoints where bath amplification is small. Treating its entire mass with the global maximum is deliberately conservative.

If the phase laws also have positive local Gaussian limits with positive limiting phase weights, the existing local concavity necessity proof supplies c_N≫N^(3/2). Under the exp(-b√N) exceptional bound, the criterion then yields an iff statement. Independent extensive kinetic energy can turn weak conditional spin-energy CLTs into local limits for total energy by convolution; it cannot repair an incorrect phase decomposition or replace the required conditional exponential moments.

This criterion avoids interpreting a small signed partition-function error as a small probability error. The outstanding short-range task is to establish the positive phase laws and (1) for the actual energy in a primary rigorous model.

## General fluctuation scales

The same proof works for a phase separation Δ_N and a within-phase scale s_N, where s_N→∞ and s_N=o(Δ_N). Replace (1) by a uniform bound on E exp[η|E-E_i,N|/s_N]. Then the sufficient conditions are

\[
 c_N\gg\Delta_Ns_N,\qquad
 \delta_N\exp(C\Delta_N^2/c_N)\to0.
\]

The tangent bound becomes h_N≤O(Δ_Ns_N/c_N)|E-E_i,N|/s_N, and the remaining proof is unchanged. In particular, δ_N≤exp(-bΔ_N/s_N) for a fixed b>0 makes c_N≫Δ_Ns_N sufficient. If at least one conditional weak fluctuation limit has two distinct support points, the [two-scale chord argument](reservoir-support-classification.md) makes it necessary as well. This supplies a non-Gaussian version of the two-phase threshold under an explicit positive-decomposition hypothesis.
