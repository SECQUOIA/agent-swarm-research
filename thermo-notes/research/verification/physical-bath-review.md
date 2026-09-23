# Independent review of the physical finite-bath extension

Date: 2026-09-06. Reviewer: independent subagent `review_physical_bath`.

Reviewed [Finite-bath accuracy with droplet and interfacial tails](../finite-bath-physical-extension.md), including its completed three-dimensional crossover section. This report records a mathematical review, not an independent literature-clearance decision.

## Verdict

The conditional sufficiency theorem, curvature-based necessity theorem, exact constant-heat-capacity corollary, finite-error crossover in dimensions at least three, and stated two-dimensional capillarity minimization are correct under their explicit hypotheses. The minor regularity and endpoint-limit clarifications identified during review have been incorporated and checked. These results establish consequences of assumptions on the canonical density. They do not establish those assumptions for a microscopic fluid or lattice model.

The main proof risk was amplification of intermediate canonical states. The uniform tail assumption and the comparison with both Gaussian and droplet costs address that risk. A local Gaussian approximation alone would not support the conclusions.

## 1. Sufficiency and its assumptions

Let the gap satisfy \(\Delta_N/N\to\ell>0\). Secant calibration and concavity imply that \(h_N\ge0\) inside the gap and \(h_N\le0\) outside it. The curvature upper bound gives

\[
h_N(E)\le\frac{K\kappa_N}{2}
(E-E_{-,N})(E_{+,N}-E)
\le C\kappa_NNx.
\]

For \(x\ge R\sqrt N\), its ratios to the two canonical costs are bounded by

\[
\frac{C\kappa_NN^{3/2}}{R},\qquad
C\kappa_NN^{3/2}N^{1/2-\alpha}.
\]

Both tend to zero when \(\kappa_NN^{3/2}\to0\) and \(\alpha\ge1/2\). The resulting tail integral tends to zero after taking \(N\to\infty\) and then \(R\to\infty\), using

\[
e^{-a\min(u,v)}\le e^{-au}+e^{-av}.
\]

On each fixed phase window, the residual log-weight tends uniformly to zero. Exterior tails cannot gain mass. These facts prove the asserted weighted-L1 convergence, normalization limit, and TV convergence.

The following restrictions matter:

- The curvature upper bound and feasible bath domain must cover **every fixed** standardized phase neighborhood. One prescribed neighborhood of width \(R_0\sqrt N\) leaves a nonzero limiting Gaussian tail and is insufficient.
- Both limiting phase weights must be positive and sum to one; both variances must be finite and positive.
- The uniform interior envelope is an additional assumption. A fixed-energy interfacial large-deviation principle and a local central limit theorem do not imply the required mesoscopic control.
- For physical baths with an energy cutoff, setting \(h_N=-\infty\) outside the feasible domain is appropriate.

The completed note explicitly includes these restrictions.

## 2. Necessity without a valley hypothesis

TV convergence and the positive local Gaussian limits imply that

\[
f_{i,N}(z)=h_N(E_{i,N}+\sqrt N z)-\log Z_N
\]

converges to zero in Lebesgue measure on every fixed bounded interval. Local L1 convergence of the reference densities suffices for this transfer of measures: their limiting density has a positive minimum on each such interval.

An elementary derivative argument avoids any unstated convex-analysis theorem. Choose points

\[
a_N\in[-2,-3/2],\quad b_N\in[-1,-1/2],\quad
c_N\in[1/2,1],\quad d_N\in[3/2,2]
\]

where the four values of \(f_{i,N}\) tend to zero. Convergence in measure guarantees such choices. Concavity yields

\[
\frac{f_{i,N}(d_N)-f_{i,N}(c_N)}{d_N-c_N}
\le f'_{i,N}(0)\le
\frac{f_{i,N}(b_N)-f_{i,N}(a_N)}{b_N-a_N}.
\]

Both bounds tend to zero. Thus \(\sqrt N h_N'(E_{i,N})\to0\) at both phases. Integrated lower curvature across the gap then forces \(\kappa_NN^{3/2}\to0\), independently of the linear tilt and of the canonical valley.

Regularity clarification resolved: the primary note now explicitly assumes twice continuous differentiability in sections 3 and 4. This justifies integration of the curvature without an unaccounted singular contribution. The four-point secant proof above has also been incorporated into section 4 and checked against this report.

## 3. Exact physical reservoir

For \(\omega_B(U)\propto U^{c_B}\mathbf1_{U>0}\), the proposed total energy

\[
\mathcal E_N=E_{-,N}+
\frac{\Delta_N}{1-e^{-\beta\Delta_N/c_B}}
\]

equalizes the residual log-weight at the two endpoints exactly. If \(c_B\gg N^{3/2}\), its curvature is \(\beta^2/c_B[1+o(1)]\) uniformly on the required interval and neighborhoods, proving sufficiency.

For arbitrary total-energy choices, TV convergence implies

\[
\sqrt N\left[\beta-rac{c_B}{\mathcal E_N-E_{i,N}}\right]\to0.
\]

The bath inverse temperatures at both endpoints are consequently \(\beta+o(N^{-1/2})\), so their reciprocal difference gives

\[
\frac{\Delta_N}{c_B}=o(N^{-1/2}).
\]

This proves necessity. If a bath cutoff excludes a bounded standardized portion of a phase window, TV convergence already fails; therefore applying the local derivative argument does not silently overlook a cutoff exception.

The note correctly distinguishes the power-law exponent's surface-entropy heat capacity from the canonical heat capacity of a finite quadratic reservoir. Their finite offset does not change the asymptotic exponent.

## 4. Finite-error crossover for dimensions at least three

At \(c_B/N^{3/2}\to\gamma\in(0,\infty)\), exact secant calibration gives the local limits

\[
h_N(E_{i,N}+\sqrt N z)\to b_i z,
\qquad b_-=\frac{\beta^2\ell}{2\gamma},\quad b_+=-b_-.
\]

The local second-order term vanishes because \(N/c_B\to0\). For interior tails, the Gaussian-cost ratio becomes small by choosing \(R\) large, while the droplet-cost ratio tends to zero since \(\alpha>1/2\). Exterior tails remain unamplified. These observations justify normalization and full TV convergence to the two separate tilted Gaussian contributions; there is no missing intermediate mass.

The normalization \(Z_\gamma=\sum_iw_i e^{b^2v_i/2}\), weights \(w_i e^{b^2v_i/2}/Z_\gamma\), means \(b_iv_i\), and unchanged variances are correct. In particular, endpoint balancing does not generally balance integrated phase weights when the variances differ.

For equal variances \(v\), the asserted distance

\[
2\Phi\!\left(\frac{\beta^2\ell\sqrt v}{4\gamma}\right)-1
\]

is correct for arbitrary positive original phase weights. It describes the specified secant-calibrated physical bath, not optimization over all total energies.

## 5. Two-dimensional rate and capillarity calculation

The tilted rate must be normalized by subtracting the minimum of the unnormalized cost. The completed note does so. Interior cost strictly below both endpoint costs implies TV tends to one when the reference law concentrates at the endpoints. Equality of leading costs does not determine limiting probabilities.

Endpoint-limit clarification resolved: section 7 now explicitly requires \(E_{i,N}/N\to e_i\), in addition to the gap limit in section 2. This supplies the endpoint limits needed for its fixed macroscopic coexistence interval.

For the stated isotropic square-torus model,

\[
I(\theta)=\tau\min\{2\sqrt{\pi\theta},2,
2\sqrt{\pi(1-\theta)}\},
\]

the inequality \(I(\theta)\ge8\tau\theta(1-\theta)\) is valid, with equality precisely at \(0,1/2,1\). The droplet comparison follows from

\[
8\sqrt\theta(1-\theta)\le\frac{16}{3\sqrt3}<2\sqrt\pi.
\]

Consequently \(\gamma_*=\beta^2\ell^2/(16\tau)\) is correct. Below this capacity coefficient the central slab is the unique minimizing fraction; above it the endpoints minimize. At equality there are three leading-rate minima, whose actual weights require prefactors and subleading corrections. This is a conditional capillarity-model result, not a microscopic theorem or a universal anisotropic coefficient.

## 6. Novelty and remaining work

This review establishes mathematical consistency of the conditional results. It does not certify novelty or publishability. The bath reweighting mechanism and droplet-versus-Gaussian cost competition are established background; the possible contribution is their use to obtain distribution-level capacity requirements and the dimension-dependent boundary behavior under explicit assumptions.

The [existing prior-art review](ensemble-prior-art.md) records unresolved literature access and comparison work. A microscopic example satisfying the density hypotheses, or a controlled density-of-states study with separately checked phase and valley behavior, remains necessary to establish the application beyond this conditional class. Numerical agreement alone would not prove the uniform envelope.
