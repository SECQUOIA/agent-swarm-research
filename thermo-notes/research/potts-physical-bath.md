# An exact microscopic finite-reservoir benchmark at a first-order transition

Current complete treatment: [LaTeX paper and reproduction bundle](../paper-finite-reservoirs/README.md). The paper adds the pure-spin extension and optimized physical boundary calibration while retaining the exact Gamma/Beta benchmark below.

Date: 2026-09-06. Status: formulas, finite-N calculations and the microscopic theorem have passed independent review. Novelty remains provisional. This is a mean-field model with an extensive interphase barrier. It verifies a microscopic finite-bath mechanism but does not test short-range droplet or interface physics. See the [microscopic theorem review](verification/potts-microscopic-theorem-review.md).

## Model and the question answered

Take N three-state Potts spins with occupation numbers `n_1+n_2+n_3=N` and Hamiltonian

\[
U_N(n)=-\frac{J}{2N}\sum_{i=1}^3 n_i^2,\qquad J>0.
\]

Add `2aN` independent quadratic momentum degrees of freedom, with `a>0` fixed and `2aN` integral along the chosen size sequence. Their canonical kinetic energy has Gamma distribution of shape `A=aN` and rate `beta`. The total subsystem energy is `E=U_N+K`.

At the established first-order transition `beta J=4 log 2`, the spin system has one disordered phase and three color-related ordered phases. Their density vectors are `(1/3,1/3,1/3)` and the three permutations of `(2/3,1/6,1/6)`. The ordered phases all have the same energy. Thus there are **two** distinct energy peaks, not four.

The kinetic degrees make this a continuous-energy benchmark: the disordered spin-potential energy alone fluctuates on an O(1) scale, and kinetic energy restores positive O(N) variance in both phases. **They are not required for the reservoir exponent.** The stronger theorem needs nondegeneracy in only one phase; ordered spins already have positive variance on the sqrt(N) scale. The [current manuscript](../paper-finite-reservoirs/sections/microscopic.tex), thm:mf-bath, proves the iff result for pure spins a=0, and the boundary law permits the degenerate disordered Gaussian measure.

Couple this system weakly and additively to an isolated reservoir with density of states `omega_B(B) proportional B^c 1_{B>0}`, `c>0`, at total composite energy `mathcal E`. The question is whether **some choice of total energy** can reproduce the canonical subsystem law at the transition. The answer is

\[
\boxed{\exists\mathcal E_N:\operatorname{TV}(Q_N,P_N)\to0
\quad\Longleftrightarrow\quad c_N\gg N^{3/2}.}
\tag{1}
\]

Here `P_N,Q_N` can denote either the complete subsystem state laws or their total-energy laws: their Radon–Nikodym ratio depends on total energy alone, so the two total-variation distances are exactly equal. This statement does not concern dynamical convergence.

## Exact finite-N reduction

The canonical probability of an occupation triple is

\[
P_N(n)=\frac1{Z_N}\frac{N!}{n_1!n_2!n_3!}e^{-\beta U_N(n)}.
\tag{2}
\]

Integrating kinetic energy and the bath exactly gives

\[
Q_N(n)\propto\frac{N!}{n_1!n_2!n_3!}
[\mathcal E-U_N(n)]_+^{A+c}.
\tag{3}
\]

Conditional on n, the canonical K law is `Gamma(A,beta)`, and the finite-bath law is

\[
\frac K{\mathcal E-U_N(n)}\mid n\sim\operatorname{Beta}(A,c+1).
\tag{4}
\]

The exponent `A+c` follows from the beta integral of `K^(A-1)(mathcal E-U-K)^c`; it is not `A+c-1`.

These identities permit exact summation over occupation triples and analytic CDF evaluation. The computation groups color permutations with multiplicities 1, 3 or 6, then aggregates identical potential energies. The remaining errors are floating-point and special-function errors; there is no Monte Carlo error or energy-histogram approximation.

## Total-variation calculation without binning energy

The full-state likelihood ratio has the form

\[
\frac{dQ_N}{dP_N}(E)
=\frac{e^{\beta E}(\mathcal E-E)^c_+}{M_N}.
\]

On its feasible domain the log ratio is strictly concave and has its maximum at `E*=mathcal E-c/beta`. The set where it exceeds one is therefore an interval `(E_L,E_R)`, intersected with subsystem support if necessary. Consequently

\[
\operatorname{TV}(P_N,Q_N)
=Q_N(E_L<E<E_R)-P_N(E_L<E<E_R).
\tag{5}
\]

Both probabilities are weighted sums of the shifted Gamma and scaled Beta CDFs from (2)–(4). The interval endpoints follow from a scalar root solve. The code uses a centered log-likelihood and `log1p`/`expm1` to reduce cancellation in a large bath.

Independent direct integration of the density difference at small N agrees with (5), and explicit enumeration of all `3^N` spin configurations for `N=1,...,8` agrees with occupation aggregation. See [formula review](verification/potts-bath-formula-review.md) and [independent numerical checker](verification/check_potts_finite_bath.py).

## Phase fluctuations and limiting weights

Write `b=beta J=4 log 2` and

\[
r=\sqrt{\frac{2(3-b)}{6-b}},\quad
w_-=\frac{3r}{1+3r},\quad w_+=\frac1{1+3r}.
\]

The minus phase is ordered, with lower energy. The energy centers and variances per N are

\[
e_-=-J/4+a/\beta,\qquad e_+=-J/6+a/\beta,
\qquad \ell=e_+-e_-=J/12,
\]

\[
v_-=\frac a{\beta^2}+\frac{J^2}{6(3-b)},\qquad
v_+=\frac a{\beta^2}.
\tag{6}
\]

The canonical weights follow from the multinomial saddle prefactor and Hessian determinant at the four minima. The ordered potential variance follows by applying the delta method to the occupation CLT. At the disordered point, the first derivative of `U/N` vanishes on the simplex, so its contribution at scale sqrt(N) is zero. The independent Gamma term contributes `a/beta^2` to both variances. These fluctuation ingredients are established mean-field/Laplace theory, not novel thermodynamics.

For `J=1,a=1/2`, the values are
`w_-=0.52967711`, `w_+=0.47032289`, `v_-=0.79792933`, `v_+=0.06504278`.

## Why the physical-bath theorem's assumptions hold in this model

Let p denote the spin-density vector on the compact probability simplex. Its canonical rate potential is

\[
I(p)=\sum_i p_i\log p_i-\frac{\beta J}{2}\sum_i p_i^2.
\]

At the stated transition its four global minima are interior and nondegenerate; the complete minimum classification and conditional CLTs are established in the cited primary literature. Compactness and a local quadratic expansion imply

\[
I(p)-I_{\min}\ge c_0\operatorname{dist}(p,\mathcal M)^2
\]

for some positive c_0, where M is the finite minimum set. On a fixed interior portion of the simplex, Stirling bounds give an occupation probability at most
`C/N * exp[-cN dist(p,M)^2]`. Outside that portion, the rate potential has a strictly positive gap; the polynomial prefactors and number of states can be absorbed into a smaller exponential bound.

For any fixed compact total-energy-density interval, the available kinetic energy obeys `0<K<=N k_max`. Its Gamma density has maximum `O(N^(-1/2))` and log curvature

\[
\frac{d^2}{dK^2}\log f_K(K)=-\frac{aN-1}{K^2}\le-\frac{c_1}N
\]

on that interval for large N. Its mode is `aN/beta-1/beta`, an O(1) distance from its mean. It follows that

\[
f_K(K)\le\frac C{\sqrt N}
\exp[-c_2(K-aN/\beta)^2/N].
\]

The spin energy density `u(p)` is Lipschitz. In a neighborhood of a minimum p_i, writing `k=E/N-u(p)` gives

\[
|p-p_i|^2+(k-a/\beta)^2
\ge c_3\{|E/N-e_i|^2+|p-p_i|^2\}.
\]

Multiply the occupancy and kinetic bounds and sum the two-dimensional occupation lattice. The lattice Gaussian sum is `O(N)`, canceling the occupation prefactor `1/N`. Contributions outside minimum neighborhoods are exponentially small. Therefore, on the coexistence energy interval,

\[
p_N(E)\le\frac C{\sqrt N}\sum_{i\in\{-,+\}}
\exp[-c_4(E-Ne_i)^2/N].
\tag{7}
\]

This bound is stronger than the droplet-tail envelope required by the general two-phase theorem. The conditional spin CLT convolved with the Gamma density local limit gives the positive local Gaussian energy limits with weights and variances (6). Applying the physical-bath theorem proves (1). The argument uses the actual microscopic measure, not a replacement by a Gaussian mixture throughout its valley.

## Finite-size results

The reservoir was calibrated by equal residual log-weights at the two limiting phase energies:

\[
\mathcal E_N=Ne_-+
\frac{N\ell}{1-e^{-\beta N\ell/c_N}}.
\]

For `J=1,a=1/2`, exact energy-law TV distances were:

| N | c=0.5 N^(3/2) | c=2 N^(3/2) | c=N^(7/4) | c=N^(5/4) |
|---:|---:|---:|---:|---:|
| 300 | 0.09790 | 0.02945 | 0.01472 | 0.16856 |
| 1000 | 0.10999 | 0.03094 | 0.01135 | 0.25456 |
| 3000 | 0.13684 | 0.03605 | 0.00991 | 0.44885 |
| 6000 | 0.14454 | 0.03698 | 0.00850 | 0.60743 |
| 12000 | 0.14834 | 0.03730 | — | — |

The two boundary-scale limits predicted from (6) and the general physical-bath crossover are respectively `0.15739` and `0.037986`. Finite-N corrections are visible, particularly in the smaller bath. These calculations use a particular calibrated total energy; the theorem's necessity applies to **all** total-energy choices.

![Exact energy-law error for different bath growth rates](verification/potts-bath-scaling.png)

The figure is also available as a [standalone PDF](verification/potts-bath-scaling.pdf); `verification/plot_potts_bath.py` reproduces it and computes the boundary-scale limits.

The `N=12000` calculation sums 12,006,001 color-permutation orbits and aggregates 4,255,699 distinct potential energies with nonzero numerical canonical weight. Extremely small underflowed weights are omitted; the independent small-N checks and stable formulas support the reported precision, but no interval-arithmetic enclosure has been performed.

The implementation now bounds the possible posterior mass of omitted underflowed classes using their canonical mass bound and the global maximum likelihood ratio. It rejects parameters if that bound exceeds 10^(-12), since strong reweighting can otherwise revive numerically invisible classes. The upper likelihood-root bracket adapts toward the bath cutoff and reports failure if float64 cannot resolve the crossing. The independent density/enumeration checks pass after these changes.

Reproduce with `python research/verification/potts_finite_bath.py`. Default sizes cover the first four rows; `--sizes 12000` computes the last size. The command writes its requested run to `potts-finite-bath-results.json`; preserve an earlier result file before running a replacement size selection if both are wanted.

## Sources and novelty boundaries

- Gandolfo, Ruiz and Wouts, *Limit Theorems and Coexistence Probabilities for the Curie–Weiss Potts Model with an external field*, [arXiv:0811.2735](https://arxiv.org/abs/0811.2735): conditional fluctuations and coexistence probabilities are established.
- Costeniuc, Ellis and Touchette, *Complete Analysis of Phase Transitions and Ensemble Equivalence for the Curie–Weiss–Potts Model*, [arXiv:cond-mat/0410744](https://arxiv.org/abs/cond-mat/0410744), J. Math. Phys. 46, 063301 (2005): canonical/microcanonical macrostate equivalence is established and differs from the full-distribution TV question.
- Griffin, Matty and Swendsen (2017), [arXiv:1608.05455](https://arxiv.org/abs/1608.05455): finite thermal reservoirs and first-order Potts histogram comparisons are prior art; the present computation uses a different model and probability metric.

The exact Gamma/Beta integrals are standard. The candidate result is the sharp optimized physical-reservoir size requirement for this complete microscopic law, together with the broader two/three-phase distinction. The model is a transparent benchmark, not a claim of a new Potts phase transition. A targeted prior-art check of this specific finite-reservoir scaling remains necessary.
