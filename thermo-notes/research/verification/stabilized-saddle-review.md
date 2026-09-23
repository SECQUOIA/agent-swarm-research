# Independent review: unstable growth from a stabilized harmonic saddle

Reviewer: `capacity_review`. Date: 2026-09-06.

**Verdict:** the scalar reconstruction equation, unique positive root, two moment bounds, and finite-time covariance brackets are correct for a reversible overdamped harmonic diffusion whose mobility is unchanged when the restraint is removed. Both moment endpoints remain optimal even when both moments are prescribed simultaneously. The finite-rank extension is a matrix resolvent statement. The basic restrained-correlation reconstruction has close established Grote–Hynes antecedents and should not be claimed as new without a more specific distinction.

## 1. Exact root and its uniqueness

Assume finite-dimensional symmetric positive definite `H_c,M`, nonzero `u`, positive `k`, and `beta=1/(k_B T)`. The stabilized equilibrium diffusion is

\[
dx=-M H_c x\,dt+\sqrt{2\beta^{-1}M}\,dW,
\quad H_o=H_c-ku u^T.
\]

Define `A=M^(1/2)H_c M^(1/2)` and `v=M^(1/2)u`. The open deterministic drift is similar to the negative of `A-kvv^T`. In an eigenbasis of `A`, with eigenvalues `a_i>0` and coordinates `v_i`, the stabilized correlation is

\[
C(t)=\beta^{-1}\sum_i\frac{v_i^2}{a_i}e^{-a_i t}
=\sum_i w_i e^{-a_i t},\quad w_i\ge0.
\]

Thus it is completely monotone. Its Laplace transform obeys

\[
\chi(\lambda):=\beta\left[C(0)-\lambda\int_0^\infty e^{-\lambda t}C(t)dt\right]
=v^T(A+\lambda I)^{-1}v.
\]

The determinant lemma gives

\[
\det(A-kvv^T+\lambda I)
=\det(A+\lambda I)[1-k\chi(\lambda)].
\]

Since `chi` is continuous and strictly decreasing from `beta C(0)` to zero, a positive root of `k chi(lambda)=1` exists and is unique exactly when

\[
q:=k\beta C(0)=k u^TH_c^{-1}u>1.
\]

This is also precisely the condition that `H_o` have one negative eigenvalue. At `q=1` there is a zero mode; at `q<1` the open Hessian remains positive definite. Rank-one subtraction cannot create more than one negative direction.

The reconstructed `lambda` is the positive eigenvalue of the linearized deterministic drift. It is not by itself a full escape rate; barrier weights and other ingredients remain necessary.

## 2. Correlation-time and initial-slope bounds

Let

\[
c=C(0),\quad I=\int_0^\infty C(t)dt,\quad S=-C'(0),
\quad \tau=I/c,\quad \bar a=S/c.
\]

The normalized covariance weights `p_i=w_i/c` form a probability distribution over the relaxation rates. Then

\[
\chi(\lambda)/(\beta c)
=\mathbb E\frac{a}{a+\lambda}
=\mathbb E\frac1{1+\lambda/a}.
\]

Concavity in `a` and convexity in `1/a` give

\[
\frac1{1+\lambda\tau}
\le\frac{\chi(\lambda)}{\beta c}
\le\frac{\bar a}{\bar a+\lambda}.
\]

Evaluating at the root proves

\[
\boxed{\frac{q-1}{\tau}\le\lambda\le(q-1)\bar a.}
\]

The lower bound becomes zero if the integrated correlation diverges; the upper bound requires a finite initial slope. In the present finite-dimensional positive definite model both are finite. Also `S=beta^{-1}u^T M u`, which provides a useful normalization check. Single-exponential correlations saturate both inequalities.

### Simultaneous-moment sharpness

These two bounds cannot be universally improved using only `q`, `bar a`, and `tau`, even when both moments are fixed. Suppose `bar a tau>1`. For any `l in (0,1/tau)`, put

\[
h=\frac{\bar a-l}{1-\tau l},\qquad
p=\frac{h-\bar a}{h-l}.
\]

The two-point distribution with mass `p` at `l` and `1-p` at `h` has exactly

\[
\mathbb E[a]=\bar a,\qquad\mathbb E[1/a]=\tau.
\]

As `l` decreases to zero, `p` decreases to zero and `h` tends to `bar a`; for every positive Laplace argument the susceptibility converges to the single-rate susceptibility at `bar a`. Hence the root tends to the upper endpoint `(q-1)bar a`, while the vanishing slow component retains the excess inverse moment.

As `l` increases to `1/tau`, `h` diverges and `p` tends to one; the root tends to the lower endpoint `(q-1)/tau`, while the vanishing fast component retains the excess mean rate. Continuity and strict monotonicity of the root justify the limits. Every member of either sequence is a valid two-mode positive definite OU system: choose `M=I`, `H_c=diag(l,h)` and `u_i=sqrt(beta c p_i a_i)`. Thus the limits are realizable without a formal signed spectral measure. If `bar a tau=1`, the spectral rate is constant and the root is already exact.

## 3. Exact finite-window certificates

Suppose the exact covariance is known on `[0,T]`. Set

\[
\chi_T(\lambda)=\beta\int_0^T e^{-\lambda t}[-C'(t)]dt
=\beta\left[c-\lambda\int_0^T e^{-\lambda t}C(t)dt-e^{-\lambda T}C(T)\right].
\]

The nonnegative tail measure `-C'(t)dt` has total mass `C(T)`. Therefore

\[
\boxed{\chi_T(\lambda)\le\chi(\lambda)
\le\chi_T(\lambda)+\beta e^{-\lambda T}C(T).}
\]

Both envelope functions are decreasing and continuous for positive `lambda`; the upper envelope is strictly decreasing and starts at `beta c`. The root of `k` times the upper envelope equal to one is an upper bound `lambda_+`. If `k beta[c-C(T)]>1`, the lower envelope has a positive root `lambda_-`, and `lambda_-<=lambda<=lambda_+`. Otherwise set `lambda_-=0`. The susceptibility envelope width is exactly `beta exp(-lambda T) C(T)`; this is not the same as the width in root position, which also depends on the susceptibility slope.

These are deterministic statements about the exact covariance. An empirical autocorrelation curve, uncertain normalization, numerical quadrature, and finite sampling require additional controlled error bounds before calling the resulting roots certified. Complete monotonicity must follow from the model, not be inferred from an approximately decreasing measured curve.

### Stronger envelopes from the endpoint slope or a known gap

Complete monotonicity provides a simple improvement. Define

\[
a_T=-C'(T)/C(T).
\]

The residual susceptibility is

\[
\chi(\lambda)-\chi_T(\lambda)
=\beta e^{-\lambda T}C(T)
\mathbb E_T\frac{a}{a+\lambda},
\]

where `E_T` uses covariance weights reweighted by `exp(-aT)`. Jensen therefore gives

\[
\chi(\lambda)\le\chi_T(\lambda)+
\beta e^{-\lambda T}C(T)\frac{a_T}{a_T+\lambda}.
\]

This upper envelope is tighter than treating all tail loss as an atom at `T`. If all coupled rates have a proven lower bound `a_min>0`, then

\[
\chi(\lambda)\ge\chi_T(\lambda)+
\beta e^{-\lambda T}C(T)\frac{a_{\min}}{a_{\min}+\lambda}.
\]

Each strengthened envelope remains decreasing, so the same root comparison applies. The known-gap lower envelope starts at `beta c`, and therefore always gives a positive lower root when `q>1`.

## 4. Finite-rank restraints

Let `H_o=H_c-U K U^T`, where `K` is positive definite and `U` has independent columns. Let the matrix covariance of `z=U^Tx` be `C_U(t)`, set `V=M^(1/2)U`, and define

\[
B(\lambda)=\beta K^{1/2}
\left[C_U(0)-\lambda\int_0^\infty e^{-\lambda t}C_U(t)dt\right]K^{1/2}
=K^{1/2}V^T(A+\lambda I)^{-1}V K^{1/2}.
\]

Then positive growth rates solve

\[
\det[I-B(\lambda)]=0.
\]

The number of positive growth rates, counted with multiplicity, equals the number of eigenvalues of `B(0)` larger than one. This follows from inertia of a low-rank update or from its Schur complement. Since `B'(lambda)` is negative definite when `U` has full column rank, its ordered eigenvalues are strictly decreasing to zero. Each branch initially above one crosses once. Thus an index-one open saddle again gives one unique positive growth rate, characterized by `lambda_max(B(lambda))=1`.

The matrix covariance and its negative derivative are positive semidefinite spectral mixtures. The finite-window inequalities hold in Loewner order with `C(T)` replaced by `C_U(T)`. Congruence with `K^(1/2)` and comparison of ordered eigenvalues then yield index-one root bounds. This requires full matrix cross-correlations; individual coordinate autocorrelations generally lose the coupling information.

## 5. What must stay unchanged dynamically

The proof holds when the open and stabilized systems differ only by the specified Hessian update, with the same `M`. A finite heat bath, particle reservoir, thermostat, or feedback device can also change kinetic coefficients or introduce memory. Its equilibrium curvature does not determine those changes.

A one-dimensional counterexample makes the limitation exact. Take `H_c=h>0`, `k>h`, and stabilized mobility `m_c`. Its observed covariance is `C(t)=beta^{-1}h^{-1}exp(-m_c h t)`, and the reconstruction gives `lambda=m_c(k-h)`. If the actual open system has mobility `m_o`, its actual growth rate is `m_o(k-h)`. The ratio can be any positive number while the stabilized data and both Hessians remain fixed. Thus an uncontrolled bath change makes the desired growth rate unidentifiable from these data.

If all hidden variables are retained in a larger reversible overdamped harmonic system and only the rank-one restraint is changed, projecting those variables out introduces memory but does not invalidate the full-system proof. The measured scalar covariance remains completely monotone and already contains that memory. This is distinct from asserting that a physically different reservoir preserves the same projected memory kernel.

For a linear equilibrium generalized Langevin model whose entire friction kernel is genuinely unchanged, the response identity can still hold. In an overdamped convolution formulation with dynamic stiffness `H_c+s Gamma_hat(s)`, equilibrium regression gives

\[
\beta[C_U(0)-s\widehat C_U(s)]
=U^T[H_c+s\widehat\Gamma(s)]^{-1}U.
\]

This supplies the same low-rank root equation. However, more general memory or inertial models need not have completely monotone position correlations. The Jensen and finite-window certificates proved above must not be exported to oscillatory correlations without a new argument. Adding inertia is a material change in assumptions.

## 6. Independent numerical checks and prior art

A separate numerical calculation tested 200 random five-dimensional positive definite pairs `(H_c,M)`, random restraint directions, and `q` between `1.01` and `6`. The scalar secular roots matched the directly diagonalized unstable eigenvalues to maximum relative error `3.09e-13`. Every case satisfied both moment inequalities, the finite-window envelopes at three positive Laplace arguments, and the endpoint-slope upper improvement. This supports the algebra; the preceding proofs establish the results.

The primary study [*A computational study of barium blockades in the KcsA potassium channel based on multi-ion potential of mean force calculations and free energy perturbation* (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3787775/) estimates a Laplace-domain friction from dynamics harmonically restrained at the barrier and then solves a Grote–Hynes reactive-frequency equation, explicitly attributing the friction reconstruction method to Straub et al. (1988). This is direct prior art for the core restrained-dynamics workflow. The compact covariance formula is consistent with that established response calculation. Novelty, if any, must be assessed for the finite-window certificates, sharp information limits, or a distinct application rather than for reconstructing barrier dynamics from stabilized dynamics in general.

## 7. Follow-up review of the finite-grid certificate

Equation (5) of `research/stabilized-saddle-kinetics.md` is correct. For `0=t_0<...<t_n=T`, let `Delta C_i=C(t_i)-C(t_(i+1))`. Since `chi/beta` is the Laplace transform of the positive measure `-dC`, moving the mass in each time bin to its right or left endpoint gives

\[
\beta\sum_i\Delta C_i e^{-\lambda t_{i+1}}
\le\chi(\lambda)\le
\beta\left[\sum_i\Delta C_i e^{-\lambda t_i}+C(T)e^{-\lambda T}\right].
\]

The lower function tends to zero at infinity. The upper function tends to `beta Delta C_0`, because its first-bin mass is placed at time zero. For `q>1`, its equation `k chi_grid,+ = 1` therefore has a finite root **if and only if** `k beta Delta C_0<1`. If `k beta Delta C_0>=1`, including equality, this particular upper-root bound is `+infinity`. The lower-root convention is unchanged: use zero unless `k beta[C(0)-C(T)]>1`.

The claimed maximum-mesh-width bound on the susceptibility gap is also correct: each bin contributes at most `Delta C_i[1-exp(-lambda Delta t)]`, and the remaining tail contributes `C(T)exp(-lambda T)`.

There is a qualification to the phrase that the grid supplies no finite upper bound. It is the displayed mass-placement envelope that fails; complete monotonicity can yield additional bounds from the same grid. For example, for all `a,t>0`,

\[
\frac{a}{a+1/t}<1-e^{-at}.
\]

Averaging over the positive relaxation spectrum gives

\[
\chi(1/t)<\beta[C(0)-C(t)].
\]

Consequently, if `k beta[C(0)-C(t)]<=1`, then the actual growth root satisfies `lambda<1/t`. In particular, at the first-bin equality `k beta Delta C_0=1`, this supplies a finite upper bound even though Equation (5)'s upper envelope has no finite root. This is an additional safe inequality, not a claim of an optimal finite-grid inference procedure.

## 8. Exact extension to nonlinear mean-field feedback

The same root equation extends beyond harmonic microscopic physics in a different, precisely defined problem: linear instability of a McKean–Vlasov equilibrium under feedback through its mean observable. This does **not** justify applying it to an arbitrary single-particle nonlinear barrier.

Let the reference process be an ergodic reversible overdamped diffusion with normalized invariant density `rho`, generator

\[
L=\beta^{-1}\rho^{-1}\operatorname{div}(\rho M\nabla),
\qquad A=-L\ge0
\]

on `L^2(rho)`. The potential defining `rho` may be fully anharmonic. For definiteness assume smooth coefficients and sufficient confinement or appropriate reflecting conditions for the stated reversible generator and perturbation. Choose an observable `z` with `mean_rho z=0`, finite nonzero variance, and `z` in the operator domain of `A`; these sufficient conditions make the following rank-one perturbation well-defined. Centering is essential; geometric symmetry of the potential is not.

Consider a density `p_t` driven by the additional mean-field potential

\[
V_{\rm feedback}[p](x)=-k m[p]z(x),
\qquad m[p]=\int z p.
\]

Its nonlinear Fokker–Planck equation is

\[
\partial_t p=L^*p-k m[p]\operatorname{div}(pM\nabla z).
\]

Because `m[rho]=0`, the reference density is a stationary solution for every `k`. Set `p=rho(1+f)` with `mean_rho f=0`. Reversibility gives `L^*(rho f)=rho Lf`, and `div(rho M grad z)=beta rho Lz`. Linearization is therefore

\[
\boxed{\partial_t f=-Af+k\beta\langle z,f\rangle_\rho Az.}
\]

For an eigenmode with positive growth `lambda`,

\[
f=k\beta\langle z,f\rangle_\rho(A+\lambda)^{-1}Az.
\]

A nonzero unstable mode must couple to `z`, and its scalar dispersion relation is

\[
1=k\beta\langle z,A(A+\lambda)^{-1}z\rangle_\rho
=k\beta[C(0)-\lambda\widehat C(\lambda)],
\qquad C(t)=\langle z,e^{-At}z\rangle_\rho.
\]

The spectral theorem supplies a positive spectral measure on relaxation rates. Ergodicity and centering remove mass at zero, so `C(t)` tends to zero even if a spectral gap is absent. The susceptibility strictly decreases from `beta Var_rho(z)` to zero. Thus `q=k beta Var_rho(z)>1` gives precisely one positive growth eigenvalue. For `q<=1` there is no positive root; at equality `f=z` is a neutral mode. Absence of a positive root should not be called exponential stability when the reference operator has no gap.

No additional complex unstable roots occur. For a nonreal argument `s` in the right half-plane, the imaginary part of the susceptibility is

\[
\operatorname{Im}\chi(s)
=-\beta\operatorname{Im}(s)\int\frac{a}{|a+s|^2}\,d\mu_z(a),
\]

which cannot vanish unless `Im(s)=0`. Uncoupled modes retain the reference operator's nonpositive spectrum.

Every positive-spectral-measure certificate above therefore applies to this mean-field linear instability. In particular,

\[
-C'(0)=\langle z,Az\rangle_\rho
=\beta^{-1}\langle\nabla z^TM\nabla z\rangle_\rho,
\]

and the moment, finite-window, endpoint-slope, and finite-grid arguments carry over whenever their required integrals exist. Their mathematical justification is reversibility and linear-response feedback, rather than harmonicity of the microscopic potential.

The nonlinear equation is the gradient flow of

\[
\mathcal F[p]=\beta^{-1}\int p\log(p/\rho)
-\frac k2\left(\int z p\right)^2.
\]

Its quadratic variation at `rho` is `beta^{-1}<f^2>-k<z,f>^2`, reproducing the threshold `q=1`. This is also the mean-field interaction obtained from many reference particles coupled by `-k(\sum_i z_i)^2/(2N)` in the appropriate large-system limit. Establishing that limit or proving a particular nonlinear bifurcation requires its own hypotheses; the present conclusion concerns the linearized density equation.

A microscopic potential subtraction `-k z(x)^2/2` is a different problem. It changes the individual-particle reference drift throughout state space and generally changes its stationary distribution. The rank-one feedback operator derived here does not describe that subtraction outside the harmonic setting. Likewise, the correlation in this calculation is the **reference process with its mean feedback held at the stationary value**, not the fully self-consistent collective fluctuation covariance.

This extension has explicit prior art. [Lucarini, Pavliotis and Zagli, *Response theory and phase transitions for the thermodynamic limit of interacting identical systems* (2020)](https://doi.org/10.1098/rspa.2020.0688), [open author PDF](https://www.ma.imperial.ac.uk/~pavl/RSPA-2020-0688_Proof_hi.pdf), derive a self-consistent linearized McKean–Vlasov operator in Equation (2.4) and equilibrium correlation-response relations in Section 5. Their treatment includes anharmonic Desai–Zwanzig systems. The extension above is a verified specialization and a broader setting for the proposed certificates, with no novelty claim for the dispersion relation or mean-field mechanism.
