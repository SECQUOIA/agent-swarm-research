# Independent formula and implementation review: Potts spins with a physical bath

Date: 2026-09-06. Reviewer: `ensemble_scout`, independent of the main derivation and implementation.

**Decision:** the proposed occupation sums, phase parameters, integrated bath weights, conditional kinetic distributions and CDF calculation of energy total variation are correct. Independent explicit-spin enumeration and direct energy-density quadrature agree with the implementation. One terminology correction is necessary: Gamma shape \(A=aN\) corresponds to \(2aN\) quadratic degrees of freedom, not \(aN\).

The benchmark is a mean-field microscopic model with an extensive coexistence valley. It does not validate short-range droplet assumptions. A separate review addresses whether the finite-bath theorem can nevertheless be proved for this model itself.

## 1. Hamiltonian and phase parameters

For three spin colors and occupation vector \(n=(n_1,n_2,n_3)\), \(\sum n_i=N\), use

\[
 U(n)=-\frac{J}{2N}\sum_{i=1}^3n_i^2,
 \qquad M(n)=\frac{N!}{n_1!n_2!n_3!}.
\]

This convention includes the self-interaction constant. Removing self interactions adds \(J/2\) to every energy; that changes energy origins and total-energy calibration, but not canonical spin probabilities or the latent-energy difference. The implementation consistently uses the stated self-interaction convention with \(J=1\).

At \(\beta_tJ=4\log2\), the disordered vector \((1/3,1/3,1/3)\) coexists with the three permutations of \((2/3,1/6,1/6)\). The phase energies per spin are

\[
 u_+=-J/6,\qquad u_-=-J/4,\qquad u_+-u_-=J/12.
\]

Independent checks: the ordered-to-minority stationarity equation is \(\log4=\beta J/2\); the ordered entropy is lower by \((\log2)/3\), while the ordered energy is lower by \(J/12\), giving coexistence at \(\beta J=4\log2\). Global identification of these equilibrium states is established in Costeniuc, Ellis and Touchette, [*Complete Analysis of Phase Transitions and Ensemble Equivalence for the Curie-Weiss-Potts Model*](https://arxiv.org/abs/cond-mat/0410744), section III, theorem 3.1, equations (3.1) and (3.5). The retrieved preprint's Hamiltonian in section II matches the factor \(1/(2N)\) used here.

Let the independent kinetic density of states be

\[
 \omega_K(K)=K^{A-1}/\Gamma(A),\quad K>0,
\]

with multiplicative energy-independent constants suppressed. For actual independent classical quadratic degrees of freedom, their number is \(f=2A\). Taking \(A=aN>0\) gives a canonical Gamma law of shape \(A\), rate \(\beta\), mean \(A/\beta\), and variance \(A/\beta^2\). It does not move the spin transition temperature because its partition factor is common to all configurations.

The thermodynamic phase centers of total energy are therefore correctly

\[
 E_-=-JN/4+A/\beta,\qquad E_+=-JN/6+A/\beta.
\]

These are asymptotic phase centers. Finite-size conditional means and peak locations can differ by subleading terms; exact sums need not force those finite-size quantities to equal these formulas.

## 2. Canonical and finite-bath configuration weights

Define

\[
 Z_{\rm conf}=\sum_n M(n)e^{-\beta U(n)},\qquad
 R_n=\mathcal E-U(n).
\]

The canonical occupation probability is

\[
 P(n)=M(n)e^{-\beta U(n)}/Z_{\rm conf},
 \qquad K\mid n\sim\mathrm{Gamma}(A,\mathrm{rate}\ \beta).
\]

For a physical reservoir \(\omega_B(U_B)\propto U_B^c\mathbf1_{U_B>0}\), integrate over kinetic energy:

\[
 \int_0^{R_n}\frac{K^{A-1}}{\Gamma(A)}(R_n-K)^c\,dK
 =R_n^{A+c}\frac{\Gamma(c+1)}{\Gamma(A+c+1)}.
\]

The factor outside \(R_n^{A+c}\) is independent of occupation. Thus

\[
 Q(n)=\frac{M(n)R_n^{A+c}\mathbf1_{R_n>0}}
 {\sum_mM(m)R_m^{A+c}\mathbf1_{R_m>0}},
\]

and

\[
 \frac{K}{R_n}\mid n\sim\mathrm{Beta}(A,c+1).
\]

The exponent is \(A+c\), and the second beta shape is \(c+1\). Replacing either by \(A+c-1\) or \(c\) would be incorrect. The code uses the correct values.

## 3. Likelihood ratio and its normalization

The ratio of total-energy densities is

\[
 \frac{q(E)}{p(E)}
 =\frac{e^{\beta E}(\mathcal E-E)^c}{\mathcal M}
 \mathbf1_{E<\mathcal E},
\]

where, with
\(Z_f=\sum_nM(n)R_n^{A+c}\mathbf1_{R_n>0}\),

\[
 \boxed{\log\mathcal M
 =\log\Gamma(c+1)-\log\Gamma(A+c+1)
 +\log Z_f-\log Z_{\rm conf}+A\log\beta.}
\]

This was derived independently by integrating the exact subsystem density of states. It agrees with the implementation after subtracting the reference log-weight at \(E_-\).

The implementation uses \(B=\mathcal E-E_-\), \(s_n=E_--U(n)\), and a numerically improved conditional factor

\[
 \log z_n=-\beta s_n
 +A\log(\beta B)+\log B(A,c+1)-\log\Gamma(A)
 +(A+c)\log(1+s_n/B).
\]

Multiplying by the canonical occupation probabilities and normalizing is algebraically identical to the direct power-law occupation sum. The use of `log1p` avoids subtracting two large logarithms when the bath is large.

The secant-calibrated total energy is also correct:

\[
 \mathcal E=E_-+\frac{E_+-E_-}{1-e^{-\beta(E_+-E_-)/c}}.
\]

It equalizes the *unnormalized residual energy weight* at the two specified phase centers. It need not equalize integrated phase probabilities.

## 4. Why two CDF evaluations give total variation

Inside the bath support the log-likelihood ratio is

\[
 L(E)=\beta E+c\log(\mathcal E-E)-\log\mathcal M,
\]

with

\[
 L''(E)=-c/(\mathcal E-E)^2<0,
 \qquad E_{\max}=\mathcal E-c/\beta.
\]

Consequently the set \(q>p\) is an interval, intersected with the subsystem energy support. Let its boundaries be \(r_-,r_+\). Then

\[
 d_{\rm TV}(p,q)
 =Q(r_-<E<r_+)-P(r_-<E<r_+).
\]

The needed exact CDFs are

\[
 F_P(e)=\sum_nP(n)\,P\!\left(A,\beta(e-U(n))_+\right),
\]

where the second \(P\) denotes the regularized lower incomplete gamma function, and

\[
 F_Q(e)=\sum_{n:R_n>0}Q(n)
 I_{\mathrm{clip}((e-U(n))/R_n,0,1)}(A,c+1).
\]

The canonical probability above the bath cutoff is included automatically by this signed-interval identity. The CDF approach does not discard that tail. If a mathematical likelihood root lies below the subsystem ground-state energy, the clipped CDF formulas correctly assign no probability there.

The current upper root bracket is adequate for the tested large positive capacities. As a general-purpose routine for arbitrarily tiny \(c\), its fixed `0.999999` distance toward the cutoff would need an adaptive bracket or explicit cutoff endpoint, because a crossing can approach the cutoff more closely. This is not a detected failure in the reported parameter range.

## 5. Independent implementation checks

The independent script [check_potts_finite_bath.py](check_potts_finite_bath.py) imports the implementation only as the object under test. Its reference calculations use different enumeration and integration routes:

- It explicitly enumerates all \(3^N\) labeled spin states for \(N=1,\ldots,8\), comparing the canonical partition function and potential-energy probabilities with the symmetry-reduced occupation enumeration. The largest probability difference is approximately \(3.3\times10^{-16}\).
- It constructs finite-bath probabilities directly on those labeled spin states, using the power-law integrated weight, and compares configuration TV and the ordered probability. All checks pass at tolerance \(2\times10^{-12}\).
- For \(N=12\), it enumerates every labeled-color occupation triple without symmetry reduction, builds the Gamma/Beta **densities**, and integrates their absolute difference by adaptive quadrature. This checks the implementation's CDF/root method through a different numerical observable.
- It verifies the exact energy-density likelihood ratio and both forms of the normalization independently.

At bath exponent \(c=50\):

| Kinetic shape | TV from direct density quadrature | TV from implementation's CDFs |
|---:|---:|---:|
| \(A=6\) | 0.0865823732895 | 0.0865823732803 |
| \(A=12\) | 0.103077226815375 | 0.103077226815387 |

The maximum tested likelihood-ratio discrepancy is below \(8.3\times10^{-14}\). Machine-readable results are in [potts-bath-independent-check-results.json](potts-bath-independent-check-results.json).

The underlying formulas are exact finite sums and analytic integrals. The reported evaluations still use floating-point arithmetic and special-function routines. The code discards canonical energy classes that underflow to zero; for a general very strong reweighting one must check that discarded classes cannot acquire significant bath weight. No such failure was found in these checks or indicated by the tested large-bath scaling regime. A claim of arbitrary-parameter numerically certified exactness would be stronger than what was tested.

## 6. Independent local fluctuation checks

Writing \(b=\beta_tJ=4\log2\), the potential-energy variance divided by \(N\), conditional on a disordered phase neighborhood, tends to zero: the gradient of \(u(x)=-J\sum x_i^2/2\) vanishes along the simplex tangent at \((1/3,1/3,1/3)\), so its leading fluctuations are quadratic and order one.

At an ordered minimum, parameterize the dominant fraction by \(r=x_1\), with the minority fractions equal at the saddle. The rate curvature is

\[
 H_r=\frac32(3-b),\qquad u'(2/3)=-J/2.
\]

Therefore the ordered potential variance per spin is

\[
 v_{U,-}=\frac{J^2}{6(3-b)}.
\]

Adding the independent kinetic contribution gives the correct total-energy variances

\[
 v_- =\frac{a}{\beta_t^2}+\frac{J^2}{6(3-b)},
 \qquad v_+=\frac{a}{\beta_t^2}>0.
\]

A Laplace prefactor check gives the amplitude ratio of **one** ordered minimum to the disordered minimum as

\[
 r_0=\sqrt{\frac{2(3-b)}{6-b}}.
\]

The aggregate ordered coexistence probability tends to \(3r_0/(1+3r_0)\), with disordered probability \(1/(1+3r_0)\). The threefold color degeneracy must be included once; the exact all-occupation or orbit-weighted sums already include it. The canonical phase weights need not be one half or three quarters.

These calculations agree with the parent's independently derived coefficients. Their literature novelty is not claimed: the Curie-Weiss-Potts transition, conditional CLTs and coexistence prefactors have established prior treatments. The candidate research contribution is the sharp finite **physical reservoir** requirement and its relation to the full energy law.
