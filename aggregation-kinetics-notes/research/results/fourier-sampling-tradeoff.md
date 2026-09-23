# Sampling error versus coagulation bias in a Fourier ratio

Date: 2026-09-07. Status: supporting application of [the nonlinear Fourier factorization](fourier-identification.md), with [independent full written review](../reviews/fourier-identification-proof.md) complete. Hoeffding concentration, quotient regularization, and balancing approximation with noise are established techniques. No new statistical method or optimal rate is claimed.

## 1. Observation model

At times t and t+h, h>0, observe n independent sizes drawn from the corresponding deterministic continuum number laws η_t and η_(t+h). Assume the samples at the two times are independent as well. This is an ideal sampling model. Particles in one finite coagulating population are generally dependent; the result is not asserted for that setting.

Fix a real frequency k in the interval of the preceding factorization theorem. Write

\[
 A=\phi_t(k),\quad B=\phi_{t+h}(k),\quad R_t=B/A,
 \quad r=-\operatorname{Re}\psi(k)\ge0,
 \quad \delta=\omega-r>0.
\]

Let Â and B̂ be the empirical averages of exp(ik log X) from the two samples, and put R̂=B̂/Â when Â≠0. Suppose that for t≥t_0 the proven deterministic bounds take the form

\[
 |A|\ge\frac c2e^{-rt},\qquad
 |R_t-e^{h\psi(k)}|\le K e^{-\delta t},
\tag{1}
\]

where c>0 and K<∞. Such constants exist at every sufficiently small fixed frequency. They depend on the model and initial law. An implementable uniform guarantee would need known bounds on them.

## 2. A simultaneous concentration bound

Each real or imaginary part of exp(ik log X) lies in [−1,1]. Hoeffding's inequality and a union bound over the four empirical components imply

\[
 \mathbb P\bigl(|\widehat A-A|>\varepsilon
 \text{ or }|\widehat B-B|>\varepsilon\bigr)
 \le8e^{-n\varepsilon^2/4}.
\]

Thus, for a desired failure probability α∈(0,1), both complex errors are at most

\[
 \varepsilon_n=2\sqrt{\frac{\log(8/\alpha)}n}
\tag{2}
\]

with probability at least 1−α. No logarithmic moments are needed because the sampled observables are bounded.

On this event, if |Â|>ε_n, the exact identity

\[
 \widehat R-R_t
 =\frac{\widehat R(A-\widehat A)-(B-\widehat B)}A
\]

gives the directly observable sampling-error certificate

\[
 \boxed{\quad
 |\widehat R-R_t|
 \le\frac{\varepsilon_n(1+|\widehat R|)}
 {|\widehat A|-\varepsilon_n}.\quad}
\tag{3}
\]

This bounds error to the exact finite-time ratio. The model bias in (1) must still be added when estimating exp(hψ(k)). The strict denominator condition matters; if it fails, (3) provides no certificate.

## 3. A sufficient observation-time balance

If ε_n≤(c/4)e^(−rt), then (1) and concentration give |Â|≥(c/4)e^(−rt). Also |R_t|≤1+K. Using

\[
 \widehat R-R_t
 =\frac{\widehat B-B-R_t(\widehat A-A)}{\widehat A}
\]

therefore proves, with probability at least 1−α,

\[
 \boxed{\quad
 |\widehat R-e^{h\psi(k)}|
 \le K e^{-\delta t}
 +\frac{4(2+K)}c\varepsilon_n e^{rt}.\quad}
\tag{4}
\]

The first term decreases with observation time, while the second may increase. For ε_n<1, choose

\[
 t_n=\frac{\log(1/\varepsilon_n)}\omega.
\tag{5}
\]

Because δ+r=ω, both terms in (4) are constant multiples of ε_n^(δ/ω). For sufficiently large n, t_n≥t_0 and the denominator condition holds: ε_n e^(rt_n)=ε_n^(δ/ω)→0. Thus

\[
 |\widehat R-e^{h\psi(k)}|
 \le\left[K+\frac{4(2+K)}c\right]
 \varepsilon_n^{\delta/\omega}
\tag{6}
\]

with probability at least 1−α. At fixed confidence this is an upper bound of order n^(−δ/(2ω)), reached at an observation time of order (log n)/(2ω). Choosing time in this way is a sufficient balance for this certificate, not a minimax-optimality result or an optimal experimental design theorem. At r=0 the sampling term does not grow with time, and the displayed balance remains sufficient but need not be the best choice.

The constants in (5) depend on unknown kinetics unless supplied by prior class bounds or a separate estimate. This note does not resolve that adaptation problem. It also does not pass from error in one Fourier ratio to recovery of the full daughter law, which would require further inversion and stability assumptions.

## 4. Why this is separate from finite-population validity

The appearance of a logarithmic observation time does not validate a finite-reactor estimator. The [finite-population analysis](finite-population-breakdown.md) shows that some continuum observables can already fail at logarithmic times in population size. Here n counts independent samples from a specified continuum law, not interacting particles evolving in one finite vessel. Any connection between those two limits requires a propagation-of-chaos or observation argument appropriate to the statistic; none is assumed implicitly.
