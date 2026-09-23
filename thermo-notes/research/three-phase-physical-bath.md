# Three distinct phase energies need a quadratically large thermal reservoir

Date: 2026-09-06. Status: independently verified physical-bath theorem derived after the exact Gaussian classification; novelty remains provisional. It concerns restoration of an entire canonical energy distribution by choosing the total energy of an isolated composite. Only the bath temperature/total energy is adjustable; the Hamiltonian and other conjugate fields are fixed. See the [independent proof review](verification/three-phase-physical-review.md).

**Stronger result, 2026-09-07:** the Gaussian and density assumptions below are unnecessary for the quadratic threshold. The [support-classification theorem](reservoir-support-classification.md) proves the same iff result whenever the scaled energy converges weakly to a law with at least three support points, without moment or tail assumptions. This earlier proof is retained as a valid specialized derivation.

## Statement

Let a sequence of canonical energy densities at inverse temperature `beta>0` have three phase peaks at
`E_{1,N}<E_{2,N}<E_{3,N}`, with
`(E_{2,N}-E_{1,N})/N -> l_1>0` and `(E_{3,N}-E_{2,N})/N -> l_2>0`.
Assume, on every fixed standardized window,

\[
\sqrt N\,p_N(E_{i,N}+\sqrt N z)\to w_i\phi_{v_i}(z)
\quad\text{in local }L^1,
\]

with all `w_i,v_i>0` and `sum w_i=1`. The three variances need not be equal. The local limits imply that the canonical mass concentrates in the union of these phase neighborhoods. No interfacial-tail envelope is assumed.

Use a physical reservoir with density of states
`omega_B(U) proportional U^{c_N} 1_{U>0}`, with `c_N>0`, so its surface-entropy heat capacity is `k_B c_N`. The exact subsystem marginal is

\[
q_N(E)\propto p_N(E)e^{\beta E}(\mathcal E_N-E)^{c_N}
\mathbf1_{E<\mathcal E_N}.
\]

**Theorem.** There exists a total-energy sequence `mathcal E_N` with
`TV(p_N,q_N)->0` if and only if

\[
\boxed{c_N/N^2\longrightarrow\infty.}
\tag{1}
\]

This strengthens the two-phase `N^(3/2)` requirement and does not rely on a Gaussian law between the phase peaks. The same conclusion holds for finitely many phase peaks including three distinct scalar energy densities, provided their positive local weights sum to one and the total span of all phase centers remains O(N), for example when every `E_{i,N}/N` has a finite limit.

## Necessity

Write `h_N(E)=beta E+c_N log(mathcal E_N-E)` on its feasible domain, with the normalization included as `h_N-log Z_N`. If TV tends to zero, the local positive density limits imply
`h_N(E_i+sqrt(N)z)-log Z_N ->0` in measure on every fixed z interval. Concavity then gives local uniform convergence on interior compact subsets, including the phase-center values, and convergence of interior slopes. Thus

\[
h_N(E_{i,N})-\log Z_N\to0,
\qquad \sqrt N h_N'(E_{i,N})\to0.
\tag{2}
\]

This concavity step is proved in [the two-phase physical-bath note](finite-bath-physical-extension.md), section 4. It also handles arbitrary total-energy tuning. TV convergence forces the feasible domain eventually to contain each fixed phase window.

The endpoint slopes imply

\[
\frac{c_N}{\mathcal E_N-E_{i,N}}=\beta+o(N^{-1/2}).
\]

Using the first and third phases already forces `c_N>>N^(3/2)` by subtraction of reciprocal inverse temperatures. Consequently throughout the interval between them,

\[
-h_N''(E)=\frac{c_N}{(\mathcal E_N-E)^2}
=\frac{\beta^2}{c_N}[1+o(1)]
\]

uniformly. Let `theta_N=(E_2-E_1)/(E_3-E_1)`. Strong concavity gives the chord gap

\[
h_N(E_2)-(1-\theta_N)h_N(E_1)-\theta_Nh_N(E_3)
\ge\frac{\beta^2[1+o(1)]}{2c_N}
(E_2-E_1)(E_3-E_2).
\tag{3}
\]

The left side tends to zero by (2). Both energy differences are of order N. Therefore `N^2/c_N->0`, proving necessity. No linear change in inverse temperature affects this chord gap.

## Sufficiency without a valley hypothesis

Let `Delta_N=E_3-E_1` and choose the exact endpoint-balancing total energy

\[
\mathcal E_N=E_1+
\frac{\Delta_N}{1-e^{-\beta\Delta_N/c_N}}.
\]

Subtract the common endpoint log-weight from `h_N`. For `c_N>>N^2`, curvature is uniformly `O(1/c_N)` between the endpoints, so

\[
0\le h_N(E)\le O(N^2/c_N)=o(1)
\quad(E_1\le E\le E_3).
\]

The log-weight is also uniformly o(1) on every fixed standardized phase window, including the small portions outside the extreme centers. Concavity makes it nonpositive outside `[E_1,E_3]`, so it cannot amplify exterior canonical tails. Since the canonical probability outside the phase windows tends to zero as their standardized width increases,

\[
\int p_N|e^{h_N}-1|\to0.
\]

Normalization then proves TV convergence. Unlike the two-phase `N^(3/2)` theorem, this proof does not need a droplet-tail envelope: the stronger bath scale makes the log-weight uniformly small across the whole coexistence interval.

## Interpretation and limits

Three **distinct phase energies** matter, not three order-parameter labels. For example, the three ordered colors of the zero-field three-state mean-field Potts model have equal energy; together with its disordered phase they give only two energy peaks and do not activate this three-energy obstruction.

At a fixed triple point, changing additional fields or interaction parameters may cancel phase-weight distortions that temperature alone cannot. Such adjustments change the allowed control problem and fall outside (1). Likewise this is a probability distribution over finite-system phases, not a claim about simultaneous spatial fractions in a macroscopic vessel.

The reservoir power-law exponent defines the surface-entropy heat capacity; for an f-dimensional quadratic bath it equals f/2−1, while canonical heat capacity uses f/2. This finite constant distinction does not change the power N².

The mathematical ingredients are elementary concavity and an established exact finite-bath marginal. The potentially useful result is the unavoidable reservoir-size distinction after optimal temperature tuning, now without equal phase variances or Gaussian interfacial assumptions. Related Gaussian-ensemble and designed-coexistence literature is discussed in [the prior-art audit](verification/multiphase-reservoir-prior-art.md). No separate novelty claim is established by this derivation alone.
