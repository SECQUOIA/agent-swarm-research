# Inferring interfacial cost from bulk response with finite-range kernels

Date: 2026-09-07. Status: a conditional result for an explicit variational free-energy model; [independently reviewed mathematical ingredients](verification/interfacial-inference-review.md). No exact microscopic structure-factor or molecular nucleation theorem is claimed. Novelty remains provisional; see the [independent prior-art audit](verification/interfacial-inference-prior-art.md).

## What this scout establishes

There is a useful distinction between incomplete structural information and all-wavevector information. For the model below, identical homogeneous free energy and identical bulk response through fourth order in wavevector do **not** determine planar interfacial tension, even with smooth, nonnegative, isotropic interactions of a common finite range. An explicit construction and a strict finite-parameter separation prove this statement. It avoids changing the square-gradient coefficient or introducing a phase-dependent nonlocal offset.

Conversely, the same model gives an exact relation between interfacial tension and bulk linear response. A measured wavevector band gives an interval bound. A bulk slab susceptibility gives a particularly simple finite-range certificate with an exponentially decreasing remainder. These positive inference results are at least as useful as the counterexample.

The model is a nonlocal double-parabola **variational free energy**. Its homogeneous response is its inverse Hessian. If one instead treats this functional as a fluctuating microscopic Hamiltonian, the full finite-temperature structure factor need not equal that inverse Hessian: crossings between wells introduce non-Gaussian fluctuations. Keep that distinction in every subsequent use of these results.

## 1. Primary literature and boundaries of the proposed contribution

Henderson's pair-potential uniqueness principle already rules out unrestricted claims that complete pair structure cannot identify pair interactions. A rigorous modern treatment is Frommer, Hanke and Jansen, *A note on the uniqueness result for the inverse Henderson problem* (2019), [primary paper](https://doi.org/10.1063/1.5112137). Wang, Stillinger and Torquato, *Sensitivity of pair statistics on pair potentials in many-body systems* (2020), explicitly investigate practical ambiguity from limited precision and range of structural information. Their result already establishes that almost indistinguishable pair statistics can correspond to substantially different pair potentials. [Open author-hosted paper](https://fhstillinger.github.io/FrankStillingerWebsite/fhspapers/fhspaper410.pdf).

Nonlocal free energies and their interfacial minimizers are established. Alberti, Bellettini, Cassandro and Presutti, *Surface tension in Ising systems with Kac potentials* (1996), justify an interfacial variational description for a microscopic Kac model. This does not automatically justify the double-parabola local term used here. [Open primary author manuscript](https://pagine.dm.unipi.it/alberti/ricerca/1992-96/abcp-rdc.pdf).

Double-parabola interface models also have substantial prior literature. Parry and colleagues derive nonlocal **interfacial** Hamiltonians from a square-gradient bulk model in [their 2006 paper](https://doi.org/10.1088/0953-8984/18/28/001). Their [2014 correlation analysis](https://arxiv.org/abs/1404.3100) distinguishes bulk and excess response and carefully discusses observable-dependent definitions of wavevector-dependent tension. Our bulk model retains a finite-range convolution instead of first truncating its symbol at order \(k^2\).

An independent audit identified a closer algebraic predecessor: Koslowski, Cuitiño and Ortiz, *A phase-field theory of dislocation dynamics, strain hardening and hysteresis in ductile single crystals* (2002), eliminate a continuous field from a piecewise-quadratic nonlocal model, obtaining an effective kernel of the same resolvent form. [Open primary manuscript](https://arxiv.org/abs/cond-mat/0109447). Thus the elimination technique is established. Höfling and Dietrich's [2020 slab-structure paper](https://arxiv.org/abs/2006.06083) and [2024 interface analysis](https://doi.org/10.1063/5.0186955) contain the bulk-slab response correction and a spectral excess functional closely related to the one below. The independent audit did not locate the complete inference theorem in these sources. Older simplified Sullivan models remain an unresolved special-case check; the exact resolvent formula should not be promoted as a new general principle.

The narrower candidate is the combination of a positive finite-range response certificate and explicit smooth moment-matched interactions with distinct tensions. The sharp moment inequalities themselves belong to the classical moment problem.

## 2. Model and homogeneous response

In three dimensions let \(J(x)\ge0\) be radial, integrable, and supported in \(|x|\le R\), with fixed mass

\[
M=\int_{\mathbb R^3}J(x)\,dx>0.
\]

Consider the variational free energy

\[
\mathcal F_J[m]=\frac a2\int (|m(x)|-1)^2\,dx
+\frac14\iint J(x-y)[m(x)-m(y)]^2\,dx\,dy,
\qquad a>0.
\tag{1}
\]

Both terms are nonnegative, so no unstable negative-gradient symbol is being used. All kernels have the same homogeneous free-energy density \(W(m)=a(|m|-1)^2/2\), minima \(\pm1\), and homogeneous well curvature \(a\).

For a planar profile, project the kernel along a normal:

\[
j(z)=\int_{\mathbb R^2}J(z,y)\,dy,
\qquad
D(k)=M-\widehat j(k)=M-\widehat J(k\mathbf n).
\tag{2}
\]

Here \(0\le D(k)\le2M\). The homogeneous Hessian is \(H=a+L\), where \(L=M-j*\), and its susceptibility is

\[
\chi(k)=\frac1{a+D(k)}.
\tag{3}
\]

The associated Gaussian fluctuation expression is \(S_G(k)=\chi(k)/\beta\), for the field normalization in (1). Equations (3) and the proofs below are exact statements about variational linear response. Calling \(S_G\) an exact microscopic structure factor would require an additional model justification not provided here.

Let the normalized radial probability measure of \(J\) have moments

\[
\mu=\mathbb E r^2,\qquad \nu=\mathbb E r^4.
\]

Radial symmetry in three dimensions gives

\[
\widehat J(k)=M\mathbb E\operatorname{sinc}(kr),
\qquad
D(k)=M\left(\frac{\mu k^2}{6}-\frac{\nu k^4}{120}+O(k^6)\right).
\tag{4}
\]

Thus matching \(M,\mu,\nu\) matches the Hessian response and its Gaussian structure expression through \(k^4\), including the square-gradient coefficient.

## 3. Exact global planar minimization

Define \(\sigma_J(a)\) as the infimum of (1) per unit area among planar finite-energy profiles with limits \(-1\) and \(+1\). Measurable profiles are admissible. The minimizer generally has a jump; this is an integrable-kernel model without a local gradient term, not a continuous diffuse-interface model.

Use the pointwise identity

\[
\frac a2(|m|-1)^2=\min_{s\in\{-1,1\}}\frac a2(m-s)^2.
\]

For any fixed binary front \(s\), quadratic minimization over \(m\) gives

\[
m=G*s,\qquad
G=a(a+L)^{-1}
=\frac a{a+M}\sum_{n=0}^{\infty}\frac{j^{*n}}{(a+M)^n}.
\tag{5}
\]

The measure \(G\) is symmetric and nonnegative with mass one; \(j^{*0}=\delta_0\). The minimized energy is a binary nonlocal perimeter,

\[
\inf_m\mathcal F_J[m,s]
=\frac14\iint K(z-z')[s(z)-s(z')]^2\,dz\,dz',
\tag{6}
\]

where

\[
K=\frac{a^2}{a+M}\sum_{n=1}^{\infty}\frac{j^{*n}}{(a+M)^n},
\qquad
\widehat K(0)-\widehat K(k)=\frac{aD(k)}{a+D(k)}.
\tag{7}
\]

The kernel \(K\) is positive and has a finite first moment, although it no longer has compact support.

Global minimality does not require a rearrangement assumption about shell kernels. For every binary front with the stated limits and every shift \(t\), the signed integral of \(s(z+t)-s(z)\) is \(2t\). Hence its mismatch set has measure at least \(|t|\), and

\[
\int[s(z+t)-s(z)]^2\,dz\ge4|t|.
\]

The step \(s(z)=\operatorname{sgn}z\) attains equality at every shift. Integrating against the positive kernel in (6) proves that it is a global minimizer of the binary problem. The convolution \(m=G*\operatorname{sgn}\) is nondecreasing, odd, and sign-compatible, so it also attains the minimum in the original local-well representation.

Consequently

\[
\boxed{
\sigma_J(a)=\int|z|K(z)\,dz
=\frac{2a}{\pi}\int_0^\infty
\frac{D(k)}{a+D(k)}\,\frac{dk}{k^2}.}
\tag{8}
\]

The Fourier identity follows from \(\int_0^\infty(1-\cos kz)k^{-2}dk=\pi|z|/2\). The formula is finite because \(D(k)=O(k^2)\) at zero and is bounded at infinity.

For smooth \(j\), (5) includes an atom \(a/(a+M)\) at zero, and the minimizer has jump

\[
m(0+)-m(0-)=\frac{2a}{a+M}.
\]

If continuous profiles are required, smoothing this jump gives the same infimum, but generally not an attained minimum. This limitation should remain visible when interpreting the model.

## 4. Sharp moment information in the strong-well limit

From (8),

\[
\frac{a}{a+2M}\sigma_J(\infty)
\le\sigma_J(a)\le\sigma_J(\infty),
\qquad
\sigma_J(\infty)=\int|z|j(z)\,dz
=\frac M2\mathbb E r.
\tag{9}
\]

The last equality uses \(\mathbb E|\cos\theta|=1/2\) in three dimensions. The bounds follow pointwise from \(0\le D\le2M\), and monotone convergence gives the limit as \(a\to\infty\).

Suppose

\[
0<\mu<R^2,\qquad \mu^2<\nu<R^2\mu.
\]

Among radial probability measures supported in \([0,R]\) with the prescribed second and fourth moments, the sharp first-moment bounds are

\[
\boxed{\frac{\mu^{3/2}}{\sqrt\nu}\le\mathbb E r\le
p\sqrt{x}+(1-p)R,}
\tag{10}
\]

where

\[
x=\frac{R^2\mu-\nu}{R^2-\mu},\qquad
p=\frac{R^2-\mu}{R^2-x}.
\]

For the lower bound, Hölder gives \(\mu\le(\mathbb E r)^{2/3}\nu^{1/3}\). Equality is attained by radial mass \(\mu^2/\nu\) at \(\sqrt{\nu/\mu}\), with the remaining mass at zero.

For the upper bound, let \(Y=r^2\), and interpolate \(\sqrt Y\) by a quadratic with matching value and derivative at \(x\), and matching value at \(R^2\). Because the third derivative of \(\sqrt Y\) is positive on \(Y>0\), its interpolation remainder has sign \((Y-x)^2(Y-R^2)\le0\). The quadratic majorizes \(\sqrt Y\) on the interval, including zero by continuity. Its expectation is fixed by \(1,\mu,\nu\), and the measure supported on \(Y=x,R^2\) attains equality.

These are sharp bounds on the strong-well tension coefficient. Together with (9), they give certified finite-\(a\) bounds, but they do not identify the exact finite-\(a\) extremizers.

## 5. An explicit smooth finite-range nonidentifiability theorem

Set \(M=R=1\), \(\mu=1/2\), and \(\nu=3/8\). The two extremal radius measures are

\[
\rho_- =\tfrac13\delta_0+\tfrac23\delta_{\sqrt3/2},
\qquad
\rho_+ =\tfrac23\delta_{1/2}+\tfrac13\delta_1.
\tag{11}
\]

Their strong-well tensions are \(1/(2\sqrt3)\) and \(1/3\), respectively. In particular, (9) proves strict separation at any

\[
a>\frac{2}{2/\sqrt3-1}=12.9282\ldots.
\tag{12}
\]

For example, at \(a=20\), the lower-moment model has tension at most \(0.288676\), while the higher-moment model has tension at least \(0.303030\). These are analytic bounds, not numerical evidence alone.

The shell measures in (11) are a convenient construction device. They can be replaced by **smooth radial nonnegative kernels obeying the same range bound and exactly the same target moments**. The common range condition means support within the same radius \(R\); the minimal support radii need not coincide. Let \(Z_\varepsilon\) have a smooth isotropic probability density supported in the ball of radius \(\varepsilon\), with \(z_2=\mathbb E|Z_\varepsilon|^2\) and \(z_4=\mathbb E|Z_\varepsilon|^4\). For independent isotropic \(X\),

\[
\mathbb E|X+Z_\varepsilon|^2=\mu_0+z_2,
\qquad
\mathbb E|X+Z_\varepsilon|^4
=\nu_0+\frac{10}{3}\mu_0z_2+z_4.
\]

Choose

\[
\mu_0=\mu-z_2,\qquad
\nu_0=\nu-\frac{10}{3}\mu_0z_2-z_4.
\]

For sufficiently small \(\varepsilon\), these are interior feasible moments on radius \(R-\varepsilon\). Construct both extremal radial measures for those moments, then convolve each corresponding three-dimensional isotropic measure with the same smooth bump. The resulting kernels are smooth, radial, nonnegative, supported in radius \(R\), and have exactly mass one, second moment \(\mu\), and fourth moment \(\nu\).

As \(\varepsilon\to0\), their Fourier symbols converge pointwise to those of (11). The uniform bounds \(D(k)\le\mu k^2/6\) and \(D(k)\le2\) permit dominated convergence in (8). Thus the strict finite-\(a\) tension gap persists for all sufficiently small smoothing widths.

This proves, within (1), that smooth stable finite-range kernels with identical homogeneous free energy and identical Hessian response through \(k^4\) can have different exact planar tensions. It is more specific than changing an unspecified higher-gradient coefficient, but does not establish the same assertion for the exact equilibrium structure of a microscopic fluid.

Deterministic quadrature of the limiting shell models gives:

| \(a\) | \(\sigma_-\) | \(\sigma_+\) | ratio \(\sigma_+/\sigma_-\) |
|---:|---:|---:|---:|
| 1 | 0.208562 | 0.221874 | 1.063825 |
| 5 | 0.265842 | 0.298573 | 1.123121 |
| 20 | 0.282454 | 0.323572 | 1.145575 |
| 100 | 0.287400 | 0.331314 | 1.152797 |

The [check script](verification/interfacial_inference_check.py) and [results](verification/interfacial-inference-check.json) preserve moment checks, quadrature error estimates, and an analytic spectral-tail bound. They are not interval-arithmetic enclosures. The existence theorem relies on the analytic separation, not the numerical values.

## 6. Positive inference from a measured wavevector band

Within this model, all-wavevector response determines \(D\), hence \(\sigma\) by (8). For a compactly supported \(J\), \(\widehat J\) is analytic. Exact response on an open continuum interval therefore determines the kernel by analytic continuation. An exact counterexample with equal response at every wavevector of such an interval is impossible here. A finite set, low-order moments, or finite-precision data is a different information set.

The known local potential is also essential. Outside this model class, adding a local term \(\epsilon(m^2-1)^4\) preserves the values, first derivatives, and second derivatives at both homogeneous minima, hence their entire homogeneous Hessian response, while changing off-phase free energy and potentially interfacial costs. Knowledge of that off-phase homogeneous free-energy function would exclude this particular ambiguity.

Analytic continuation is unnecessary for a robust interval certificate. Suppose \(D\) is known on \([k_0,K]\), with \(0<k_0<K\), and define the measured contribution

\[
\sigma_{[k_0,K]}=\frac{2a}{\pi}\int_{k_0}^K
\frac{D(k)}{a+D(k)}\,\frac{dk}{k^2}.
\]

With \(C=M\mu/6\), the missing bands satisfy

\[
0\le\sigma-\sigma_{[k_0,K]}\le
\frac{2\sqrt{aC}}\pi\arctan\!\left(k_0\sqrt{C/a}\right)
+\frac{4aM}{\pi(a+2M)K}.
\tag{13}
\]

For the low band use \(D(k)\le Ck^2\); its term is at most \(M\mu k_0/(3\pi)\). The high-band bound uses \(D\le2M\). Positivity is essential: it controls both missing contributions without cancellation.

If measured values give pointwise bounds \(D_-\le D\le D_+\), replace the measured integral by the corresponding lower and upper integrals, clipping to the known admissible bounds if needed. The integrand is monotone, with derivative

\[
\frac{2a^2}{\pi k^2(a+D)^2}.
\]

This is a model-level data certificate, not a claim that finite-band inversion of arbitrary pair potentials is well-conditioned.

## 7. A finite slab-response certificate with exponential remainder

An additional identity derived by the parent investigation gives a direct alternative to a wavevector integral. Let \(b_L=\mathbf1_{[0,L]}\), and measure the homogeneous planar slab susceptibility

\[
\chi_L=\frac1L\langle b_L,H^{-1}b_L\rangle,
\qquad H=a+L_{\rm op},\quad L_{\rm op}=M-j*.
\]

The use of \(L_{\rm op}\) distinguishes the operator from slab width \(L\). Since \(H^{-1}=G/a\),

\[
\sigma_L:=a^2L(1/a-\chi_L)
=a\int\min(|z|,L)\,G(dz)\uparrow\sigma.
\tag{14}
\]

The positive measure (5) has a compound-geometric representation. Write

\[
p=\frac M{a+M},\qquad
\Pr(N=n)=(1-p)p^n,\qquad
Z=X_1+\cdots+X_N,
\]

where each step has law \(j/M\) and therefore \(|X_i|\le R\). For slab width \(L=mR\), with integer \(m\ge1\),

\[
\begin{split}
0\le\sigma-\sigma_{mR}
&=a\mathbb E(|Z|-mR)_+\\
&\le aR\mathbb E(N-m)_+
=MR\left(\frac M{a+M}\right)^m.
\end{split}
\tag{15}
\]

Thus one finite slab response gives an explicit interval for tension, and increasing the slab by one interaction range shrinks its worst-case remainder by \(M/(a+M)\). A susceptibility measurement error \(|\delta\chi_L|\le\varepsilon_L\) adds \(a^2L\varepsilon_L\) to the uncertainty in \(\sigma_L\). Larger slabs reduce truncation error but require more precise response differences. That tradeoff should be retained in any proposed inference method.

The exact slab-response/spectral-excess connection has close prior art. The finite-range compound-geometric remainder is the narrower item needing a targeted novelty check.

### Fixed finite inclusions

The same elimination also gives a finite-region statement, without a planar or large-radius approximation. In three dimensions, let \(\Omega\) be a finite-volume inclusion and fix its binary phase label \(s=2\mathbf1_\Omega-1\). Define the homogeneous response

\[
\chi_\Omega=\frac1{|\Omega|}
\langle\mathbf1_\Omega,H^{-1}\mathbf1_\Omega\rangle,
\]

now using the full three-dimensional operator. The relaxed fixed-label energy is exactly

\[
E_{\rm rel}(\Omega)
=2a^2|\Omega|\,[1/a-\chi_\Omega].
\tag{16}
\]

Indeed, the effective binary energy is twice the interaction between \(\Omega\) and its complement; inserting \(K=aG\) away from its atom gives (16). When \(a>M\), the atom of \(G\) has mass greater than one half. Therefore \(G*s\) has the prescribed sign everywhere away from irrelevant boundary conventions, so the fixed-label quadratic minimizer is also a minimizer of (1) within that sign sector. This is an exact restricted inclusion formation energy from bulk response. It is not a proof that the chosen inclusion shape is stationary or that its energy is a critical nucleation barrier.

## 8. Nucleation interpretation and research decision

If an isotropic capillarity approximation is valid with a common bulk driving free-energy density \(\Delta f\), then \(R_*=2\sigma/\Delta f\) and \(\Delta F_*=16\pi\sigma^3/(3\Delta f^2)\). Different tensions consequently imply different capillary predictions even when the low-wavevector bulk response agrees through \(k^4\). The numerical ratio 1.1456 at \(a=20\) would correspond to a barrier ratio of approximately 1.50 in that approximation. No actual critical-nucleus or mountain-pass calculation is supplied here; this conversion is an illustration, not a proved nucleation theorem.

Retain the positive-kernel construction, the exact global planar proof, and the slab certificate. They give a coherent, locality-aware answer at a specified model level. Avoid claiming that the double-parabola functional is itself new, that its profile is continuous, that its inverse Hessian is an exact microscopic structure factor, or that the classical moment inequalities were discovered here.

The main unresolved step toward a stronger physical result is either a microscopic model realizing the same inference problem with controlled response errors, or an extension of the positive response certificate to smoother local free energies without an exactly quadratic elimination. The latter will require more than formally substituting a local curvature into (8).
