# What stable fluctuations determine about unstable growth

Date: 2026-09-06. Status: mathematics independently verified; core reconstruction is a rediscovery. The [prior-art audit](verification/stabilized-saddle-prior-art.md) derives equation (1) exactly from published restrained-correlation/Grote–Hynes formulas. Finite-observation bounds and sharp limits of correlation-time summaries are retained as modest results, with novelty unconfirmed. No novelty claim is made for reconstructing friction or barrier growth from restrained trajectories.

## Question and scope

A confined cluster can be a stable equilibrium object even though the corresponding open-system cluster is a saddle. Can its equilibrium fluctuation record determine the saddle's unstable growth rate without fitting one relaxation time? The result below answers a precisely restricted version: a reversible harmonic system with the **same mobility matrix** before and after removing a known quadratic stabilizer.

Actual confinement can change diffusion, hydrodynamic response, and unresolved memory. Thermodynamic correspondence alone does not imply this dynamical assumption. The positive growth eigenvalue is also only a local ingredient of a nucleation-rate prefactor. It does not determine a barrier height, basin population, recrossing correction outside the harmonic regime, or an absolute rate by itself.

## Exact local model and reconstruction

Let H_c and M be symmetric positive definite matrices. Stable fluctuations satisfy

\[
 dx_t=-MH_c x_t\,dt+\sqrt{2\beta^{-1}M}\,dW_t.
\]

The measured coordinate is z=u^T x, with centered equilibrium correlation

\[
 C(t)=\beta^{-1}u^Te^{-MH_ct}H_c^{-1}u.
\]

Remove a stabilizer k z²/2, k>0, so H_o=H_c-kuu^T. Set q=kβC(0). The open Hessian has one strictly negative eigenvalue exactly when q>1, by congruence with I-k(H_c^{-1/2}u)(H_c^{-1/2}u)^T.

For q>1 the open dynamics has exactly one positive growth eigenvalue λ. It is the unique positive solution of

\[
 \boxed{ k\beta\left[C(0)-\lambda\int_0^\infty
 e^{-\lambda t}C(t)\,dt\right]=1. } \tag{1}
\]

To prove this, write A=M^(1/2)H_cM^(1/2)>0 and v=M^(1/2)u. Similarity transforms the open drift to -A+kvv^T. The determinant lemma gives k v^T(A+λI)^(-1)v=1. The spectral theorem gives

\[
 \beta C(t)=v^Te^{-At}A^{-1}v
 =\sum_j b_j e^{-a_jt},\qquad b_j\geq0,\quad a_j>0,
\]

and hence

\[
 \beta[C(0)-\lambda\widetilde C(\lambda)]
 =\sum_j\frac{b_ja_j}{a_j+\lambda}.
\]

The last expression decreases strictly from βC(0) to zero. This proves existence and uniqueness. Modes with b_j=0 are unobserved and do not enter this rank-one instability.

Equation (1) retains all relaxation modes present in the measured correlation. It requires neither a single-exponential fit nor an explicit inversion for a memory kernel. That computational form is convenient; its equivalence to known restrained-trajectory methods must be acknowledged.

## Optimal information bounds from two usual time scales

Define

\[
 \tau_{\rm int}=\frac{\int_0^\infty C(t)\,dt}{C(0)},
 \qquad a_{\rm init}=-\frac{C'(0)}{C(0)}.
\]

Then

\[
 \boxed{ \frac{q-1}{\tau_{\rm int}}
 \leq\lambda\leq(q-1)a_{\rm init}. }\tag{2}
\]

Normalize the b_j to a probability law on relaxation rates a. Equation (1) becomes E[a/(a+λ)]=1/q. Concavity in a gives the upper bound by Jensen's inequality. Convexity of 1/(1+λτ), with τ=1/a, gives the lower bound. Equality in either bound requires a single observed relaxation rate.

Thus inserting an integrated correlation time into a single-relaxation approximation **underestimates** the unstable growth rate in this model. The estimate based on the initial decay gives an upper bound. These claims need reversibility and overdamped harmonic dynamics; oscillatory inertial correlations need different arguments.

Both endpoints are sharp even when both time-scale summaries are specified. Let A=a_init, T=τ_int, with AT>1. For any l in (0,1/T), choose

\[
 h=\frac{A-l}{1-Tl},\qquad
 p=\frac{h-A}{h-l}.
\]

The correlation C(t)/C(0)=p e^(-lt)+(1-p)e^(-ht) has exactly E[a]=A and E[1/a]=T. As l decreases to zero its root tends to (q-1)A; as l increases to 1/T its root tends to (q-1)/T. Every interior member is realized by a two-dimensional positive definite harmonic model. Unless AT=1, the endpoints are limiting values, not attainable equalities. Therefore no universally tighter bounds follow from these two summaries alone without additional spectral information.

## Bounds from a finite correlation record

Assume first that the exact population correlation is known on [0,T]. Define

\[
 \begin{aligned}
 \chi_-(\lambda;T)&=\beta\left[C(0)-\lambda\int_0^T e^{-\lambda t}C(t)\,dt-e^{-\lambda T}C(T)\right],\\
 \chi_+(\lambda;T)&=\beta\left[C(0)-\lambda\int_0^T e^{-\lambda t}C(t)\,dt\right].
 \end{aligned}\tag{3}
\]

Since 0≤C(T+s)≤C(T), these bracket the susceptibility in (1). Both are nonnegative and decreasing: integration by parts writes χ_- as β∫_0^T e^(-λt)[-C'(t)]dt, and χ_+=χ_-+βe^(-λT)C(T).

The positive root of kχ_+=1 is an upper bound λ_+. If kβ[C(0)-C(T)]>1, the positive root of kχ_-=1 gives a lower bound λ_-; otherwise use λ_-=0. Their susceptibility gap is exactly

\[
 \chi_+-\chi_-=\beta e^{-\lambda T}C(T).\tag{4}
\]

The unknown long tail is exponentially discounted at the unstable rate. Root-width convergence additionally depends on the slope of susceptibility near the root; equation (4) alone is not a uniform eigenvalue-error bound.

### A finite grid suffices

Suppose only exact values C_i=C(t_i) are available, with 0=t_0<...<t_n=T and ΔC_i=C_i-C_(i+1)≥0. No interpolation or derivative estimate is needed. The decreasing correlation implies

\[
 \boxed{\quad
 \beta\sum_{i=0}^{n-1}\Delta C_i e^{-\lambda t_{i+1}}
 \leq\chi(\lambda)\leq
 \beta\left[\sum_{i=0}^{n-1}\Delta C_i e^{-\lambda t_i}+C_n e^{-\lambda T}\right].
 \quad}\tag{5}
\]

Indeed χ/β is the Laplace transform of the positive measure -dC(t). Its mass in [t_i,t_(i+1)] is ΔC_i; move that mass to either endpoint and bound the remaining tail mass C_n between zero and its value at T. These functions decrease and provide root bounds as above when their roots exist. If kβΔC_0≥1, this particular upper envelope supplies no finite upper root and its bound is +∞. That is a limitation of the envelope, not necessarily of all information in the grid. Complete monotonicity gives the additional implication kβ[C(0)-C(t)]≤1 ⇒ λ<1/t, because a/(a+1/t)<1-exp(-at) for every a>0. A known finite initial slope also supplies the upper bound in (2).

For maximum spacing Δt, the grid susceptibility gap is at most

\[
 \beta(1-e^{-\lambda\Delta t})[C(0)-C(T)]
 +\beta e^{-\lambda T}C(T).
\]

These are bounds for exact correlations. A simulation estimate is noisy and generally violates complete monotonicity. Plugging empirical values into (3) or (5) does not create a confidence guarantee. A statistical application needs valid simultaneous correlation uncertainty bounds and must propagate them through the inequalities. That inference problem is not solved here.

## An explicit failure of a one-time-scale estimate

For C(t)/C(0)=p e^(-a_s t)+(1-p)e^(-a_f t), the exact λ is the positive root of

\[
 \lambda^2+[a_s+a_f-q(pa_s+(1-p)a_f)]\lambda
 -(q-1)a_sa_f=0.\tag{6}
\]

If q(1-p)>1 and a_s tends to zero with p fixed in (0,1), λ tends to a_f[q(1-p)-1]>0, while the integrated-time estimate (q-1)/τ_int tends to zero. A small slow component can therefore make this standard estimate arbitrarily poor. This is a local harmonic counterexample; it does not say that slow modes are irrelevant in general. If q(1-p)<1 the actual instability itself slows to zero.

## Literature and verification gates

The relation between stabilized trajectories and barrier kinetics is established. An immediately relevant application is C. N. Rowley and B. Roux, *A computational study of barium blockades in the KcsA potassium channel based on multi-ion potential of mean force calculations and free energy perturbation* (2013), [open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3787775/). It obtains a frequency-dependent friction from restrained velocity correlations and evaluates a Grote–Hynes reactive frequency, citing earlier work. The relationship to (1) is being audited separately.

The new confined-cluster paper by Li and colleagues, *Computing Nucleation Rates from Confined Equilibria: The Critical Cluster Equivalence Principle* (2026), [DOI](https://doi.org/10.1021/jacs.6c09002), motivates the practical question but does not by itself justify transferring mobilities or memory kernels between physical baths. Its precise kinetic assumptions need inspection before making any comparison or criticism.

The [independent mathematical review](verification/stabilized-saddle-review.md) verifies the scalar, finite-window, and grid statements. It also proves a matrix-restraint extension and an exact extension to linear instability of anharmonic mean-field systems; the latter has established response-theory precedents. Those extensions do not establish a result for removing a quadratic term from an arbitrary individual nonlinear system.

The reproducible [check](verification/check_stabilized_saddle.py) compared 250 random positive definite harmonic systems with direct drift diagonalization; maximum relative error was 3.58×10^(-13). All moment and finite-grid inequalities held. A two-mode example with rates (0.0001,1), weights (0.1,0.9), and q=2 gives exact growth 0.800045, while the integrated-time estimate is 0.0009991. Exact correlation values through time 5 at spacing 0.05 give grid bounds [0.765285,0.843523], despite a residual correlation of 0.106. These are population calculations, not statistical confidence intervals. Results are in [JSON](verification/stabilized-saddle-results.json).

The audit also identifies previous correlation-integral bounds from an initial record (Ceccato–Frezzato, 2019) and sharp extrapolation of noisy completely monotone data (Brown–Grabovsky, 2024). These substantially limit the novelty of generic finite-window arguments. The exact comparison to the former's main inequalities remains incomplete because the core text was inaccessible. This direction is retained for its clear information limits; it currently does not support a claim of a major new kinetic method.
