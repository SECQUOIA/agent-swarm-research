# A compound-Poisson approximation and Gaussian log-size limit

Date: 2026-09-06. Status: independently verified candidate theorem; see [the proof review](../reviews/log-size-poisson-proof.md). The [literature audit](../reviews/log-size-limit-literature.md) found no directly matching nonlinear transport bound in the open sources inspected. Pure fragmentation central limit theorems and compound-Poisson processes are established theory; the candidate contribution is the explicitly bounded effect of persistent nonlinear coagulation. The search does not certify publication priority.

## Model and conclusion

Use the mass-conserving weak solution class from [the fractional-moment note](invisible-kinetics-extension.md), with

\[
 K(x,y)=\lambda(x+y),\qquad S=b=\lambda m,
 \qquad \int n_t=N>0,\quad \int x\,n_t(dx)=m>0.
\]

Sizes are nondimensionalized by a fixed reference size. Assume the daughter measure is self-similar: a parent x produces expected daughters xθ with θ distributed according to a fixed measure B on (0,1), where

\[
 B((0,1))=2,\qquad \int\theta B(d\theta)=1.
\]

Let Θ have probability law B/2. No log-moment assumption is needed for the main coupling theorem. Define the number-normalized log-size law

\[
 \rho_t=(\log)_\#n_t/N,
 \qquad H_0=\int\sqrt{x}\,n_0(dx),
 \qquad \kappa=3-2\sqrt2.
\]

Let Z_0 have law ρ_0. Independently let J_t be Poisson with mean 2bt and let Y_j be independent copies of log Θ. The comparison law is

\[
 \bar\rho_t=\operatorname{Law}\left(Z_0+\sum_{j=1}^{J_t}Y_j\right).
\]

For arbitrary probability laws α,β on the real line, define W_1(α,β)=inf E|X−Y| over their couplings, allowing +∞. On laws with finite first moments this is the usual Wasserstein metric. A finite cross-distance can also exist when both laws lack first moments.

**Theorem 1 (uniform finite-cost coupling).** There is a coupling of Z_t with law ρ_t and barZ_t with law barρ_t satisfying Z_t≥barZ_t almost surely, with

\[
 \boxed{\quad
 W_1(\rho_t,\bar\rho_t)
 \le A_0(1-e^{-2\kappa bt}),\qquad
 A_0=\frac{H_0^2}{2\kappa mN}\le\frac1{2\kappa}.
 \quad}
\tag{1}
\]

The error bound is uniform for all time. In fact ρ_t stochastically dominates the comparison law, and

\[
 W_1(\rho_t,\bar\rho_t)
 =\frac\lambda N\int_0^t\iint x\log(1+y/x)\,n_s(dx)n_s(dy)\,ds.
\tag{1b}
\]

Thus the distance is nondecreasing and tends to a finite offset. It is a distance in log size, not a bound on raw-size moments, density ratios, or extreme mass tails. The constant need not be small, but after centering and dividing log size by √t the error is at most A_0/√t.

## Proof of the transport bound

For a bounded Lipschitz function φ on the log axis, symmetry of the additive kernel rewrites coagulation exactly as

\[
 \lambda\iint x[\phi(\log(x+y))-\phi(\log x)-\phi(\log y)]\,n_t(dx)n_t(dy).
\]

The last term equals −b∫φ(log y)n_t(dy). Combining it with the fragmentation loss and gain, then dividing by N, gives

\[
 \frac d{dt}\langle\phi,\rho_t\rangle
 =2b\left\langle\mathbb E[\phi(\cdot+Y)-\phi(\cdot)],\rho_t\right\rangle
 +\langle\phi,R_t\rangle,
\tag{2}
\]

where R_t is the finite signed measure specified by

\[
 \langle\phi,R_t\rangle
 =\frac\lambda N\iint x[\phi(\log(x+y))-\phi(\log x)]\,n_t(dx)n_t(dy).
\tag{3}
\]

It has mass zero and total variation at most 2λm=2b. For any φ with Lipschitz constant at most one,

\[
 |\langle\phi,R_t\rangle|
 \le\frac\lambda N\iint x\log(1+y/x)\,n_t(dx)n_t(dy)
 \le\frac\lambda N H(t)^2.
\tag{4}
\]

The last step uses log(1+r)≤√r. For completeness, the derivative of log(1+r)−√r is −(√r−1)²/[2√r(1+r)]≤0, and its right limit at zero is zero. The independently proved moment estimate gives H(t)≤H_0e^{−κbt}.

The first term of (2) generates the convolution semigroup P_t of the compound-Poisson sum, acting on test functions. This process is well defined without moments of Y: it has finitely many finite-valued jumps at each finite time. The semigroup preserves Lipschitz constants by applying the same random shift to two arguments. The bounded-test variation-of-constants identity is

\[
 \langle\phi,\rho_t-\bar\rho_t\rangle
 =\int_0^t\langle P_{t-s}\phi,R_s\rangle\,ds.
\]

Apply this identity to bounded functions of Lipschitz constant one, use (4), and integrate the exponential bound. It follows directly by the bounded backward test for the linear jump generator; no first absolute log moment of R_s in total variation is assumed.

For every bounded continuous increasing φ, equation (3) gives R_sφ≥0. Poisson convolution preserves monotonicity, so the same identity gives ρ_tφ≥barρ_tφ. Hence ρ_t stochastically dominates barρ_t. Couple the two laws through their quantiles, obtaining Z_t≥barZ_t. For clip_L(z)=max(−L,min(z,L)), the nonnegative difference clip_L(Z_t)−clip_L(barZ_t) increases to Z_t−barZ_t. Its expectation is bounded by the integrated estimate above. Monotone convergence proves a finite-cost coupling and (1) without any individual first moments.

There is also an exact cost identity. In the Duhamel formula with clip_L, every paired increment inside R_s P_{t-s}clip_L is nonnegative and increases to log(x+y)−log x; the independent Poisson shift cancels in that limit. Monotone convergence therefore identifies the limiting expected coupling cost with the right side of (1b). Conversely every coupling has E|X−Y| at least |E clip_L(X)−E clip_L(Y)| because clip_L is one-Lipschitz. Taking L→∞ proves that the quantile coupling achieves the infimum defining W_1. This establishes (1b) even if neither law has a mean. These refinements were proposed and independently derived by the inverse-direction reviewer.

### When ordinary first log moments are finite

If E|Y| and ∫|log x| n_0(dx) are finite, the positive log moment is at most m/N because (log x)_+≤x. For the negative part, use φ_L(z)=min{(−z)_+,L}. The coagulation remainder is nonpositive since every shift in (3) is upward. The jump part increases this test by at most 2b E|Y|. Therefore

\[
 \int(-z)_+\rho_t(dz)
 \le\int(-z)_+\rho_0(dz)+2bt\mathbb E|Y|.
\]

Monotone convergence justifies this assertion without initially assuming that the log moment remains finite. Both comparison laws then belong to the ordinary finite-first-moment Wasserstein space. No assumption on ∫x|log x| n_0(dx) is needed: the remainder is estimated through paired displacements, not the first moments of its two separately written positive measures. ∎

## Gaussian limit and deterministic speed

Assume ν_2=E(Y²)<∞, and put μ=EY<0. If Z_t denotes a random variable with the one-time law ρ_t, then

\[
 \frac{Z_t-2b\mu t}{\sqrt t}
 \ \Longrightarrow\ \mathcal N(0,2b\nu_2),
\tag{5}
\]

For finite E|Z_0|, this convergence also holds in the ordinary W_1 metric. Under that same initial-moment assumption,

\[
 W_1\big(\operatorname{Law}(Z_t/t),\delta_{2b\mu}\big)
 \le\frac{A_0+\mathbb E|Z_0|}{t}
       +\sqrt{\frac{2b\nu_2}{t}}.
\tag{6}
\]

To prove (5), the centered compound-Poisson characteristic function is

\[
 \exp\{2bt[\mathbb E e^{iuY/\sqrt t}-1-iu\mu/\sqrt t]\}
 \longrightarrow \exp(-bu^2\nu_2).
\]

Its centered second moment is 2bν_2, ensuring uniform integrability of the first absolute moment, hence W_1 convergence. The independent initial variable Z_0/√t tends to zero in W_1 under the assumed first moment. Equation (1), scaled by √t, transfers the limit to ρ_t. Equation (6) follows from the same coupling bound and Cauchy–Schwarz for the centered compound-Poisson sum.

The weak convergence in (5) and convergence in probability of Z_t/t to 2bμ still hold without any initial log-moment assumption. For bounded Lipschitz tests of the centered scaled variable, the paired-displacement Duhamel bound is A_0/√t (or A_0/t for the speed limit). The initial Z_0 is finite almost surely because sizes are positive and finite, so Z_0/√t→0 in probability. Slutsky's theorem and bounded-Lipschitz convergence give the result. The W_1 convergence and bound (6) retain the finite initial first-log-moment assumption.

These are statements about one-time population distributions. They do not assert an almost-sure law along a tagged particle trajectory or convergence of stochastic sample paths.

For equal splitting, Θ=1/2 deterministically, so

\[
 \mu=-\log2,\qquad \nu_2=(\log2)^2.
\]

The typical number-weighted log size travels at speed −2b log2, with Gaussian fluctuations of variance 2b(log2)²t. This is compatible with constant arithmetic mean size m/N because a vanishing number fraction carries the large-size mass. With monodisperse initial data and equal splitting, the pure-fragmentation reference stays on a lattice in log size. Coagulation need not preserve that lattice, but the nonlinear size law remains atomic on the countable set of positive dyadic rational multiples of the initial size, which is closed under addition and halving. No local limit theorem or pointwise Gaussian density claim is made.

For a deterministic unequal split with fractions r and 1−r, the speed is b log(r(1−r)), and the Gaussian variance rate is b[(log r)²+(log(1−r))²].

## A finite correction to geometric-mean growth

In this section assume E|Y| and E|Z_0| are finite. The identity test φ(z)=z is legitimate by the displacement estimate above. Define

\[
 a(t)=\frac\lambda N\iint x\log(1+y/x)\,n_t(dx)n_t(dy).
\]

Then 0≤a(t)≤(λ/N)H_0²e^{−2κbt}, and

\[
 \mathbb E Z_t=\mathbb E Z_0+2b\mu t+\int_0^t a(s)\,ds.
\tag{7}
\]

Thus E Z_t−2bμt has a finite limit, differing from E Z_0 by a number in [0,A_0]. The geometric mean size has an exact exponential rate 2bμ and a finite positive prefactor.

Let η_t=n_t/N be the number probability measure in raw size and π_t=x n_t/m its mass probability measure. Their relative entropy is

\[
 D_{\rm KL}(\eta_t\Vert\pi_t)=\log(m/N)-\mathbb E Z_t.
\]

Consequently this divergence grows at asymptotic rate −2bμ, with a finite additive correction. This identity is a standard change of weighting; its use here quantifies the separation of the two sampling laws.

## Transfer of other scaling limits

More generally, let c_t be any deterministic centering and let a_t→∞ be any positive scaling. The coupling theorem gives

\[
 \mathbb E\left|\frac{Z_t-c_t}{a_t}-\frac{\bar Z_t-c_t}{a_t}\right|
 \le A_0/a_t.
\]

Consequently any weak scaling limit of the reference compound-Poisson laws transfers to the nonlinear PBE. This includes stable-law limits when the jump law meets the corresponding classical domain-of-attraction assumptions; this note does not assert such assumptions for an arbitrary B or supply a new stable-limit theorem. The contribution is that nonlinear coagulation creates no additional diverging log-scale error in this model.

## Boundaries and research status

- Parent-size-dependent daughter fractions need not yield a translation-invariant reference process. The present proof does not cover them.
- The global mass-conserving weak solution class is assumed as in the preceding note; this is not an existence theorem.
- The comparison law alone does not preserve arithmetic mean size. W_1 in log size permits large differences in exponential moments and therefore cannot replace the full PBE for mass-tail predictions.
- The constant in (1) is a convenient uniform certificate, not claimed optimal. The sharp half-moment differential constant does not make every downstream estimate sharp.
- Pure fragmentation multiplicative limits, Poisson convolution, and Duhamel contraction are known tools. The novelty question is the uniform nonlinear-coagulation displacement estimate and the resulting long-time limit in this critical, count-conserving PBE.

Initial primary-source search leads include [Bertoin's authorized book excerpt](https://assets.cambridge.org/97805218/67283/excerpt/9780521867283_excerpt.pdf), which develops fragmentation jump processes, and [a spatially dependent fragmentation process](https://pmc.ncbi.nlm.nih.gov/articles/PMC12122663/), which uses compound-Poisson comparison for another fragmentation model. These are adjacent precedents, not evidence that this theorem is new. Detailed comparison is delegated to the linked literature audit.
