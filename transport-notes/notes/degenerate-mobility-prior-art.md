# Prior-art audit: coincident mobility and exchange zeros

Audit date: 2026-09-06. This note audits [degenerate-surface-mobility.md](degenerate-surface-mobility.md), with mathematical review recorded separately in [review-degenerate-mobility.md](review-degenerate-mobility.md).

The **quadratic-mobility floor crossover is an exact corollary of a published Brownian exponential-functional identity**. This is a stronger overlap than merely sharing Bessel-function techniques. Its use for a compact heterogeneous adsorbing wall may still be a useful transport result. The general two-exponent coefficient also follows from classical inverse-square spectral theory and Bessel Mellin transforms; I did not locate its exact expression as a pre-existing adsorption result.

## Candidate in context

For the natural reversible surface operator

\[
H=-\partial_s[D(s)\partial_s]+k(s),\qquad
D(s)\sim e|s|^n,\quad k(s)\sim a|s|^m,
\]

the candidate characterizes the extended energy inverse
\(J=\|H^{-1/2}1\|_2^2\), which determines the flow dispersion in the reduced constant-affinity adsorption model. The local finiteness criterion is

\[
J<\infty\quad\Longleftrightarrow\quad m<1\ \text{or}\ n<3,
\]

under the compact-wall assumptions and uniform source measure in the derivation. This is an elementary weighted-energy result, not a new Hardy-inequality framework. In particular, neither positive mobility almost everywhere nor an ordinary \(L^2\) Poisson inverse is the correct test for finite dispersion.

For \(m>1,0\le n<3\), set \(d=m+2-n\), \(r=(m-1)/d\). The zero-floor local coefficient under audit is

\[
C_{m,n}(0)=2\pi d^{-1-2r}\csc(\pi r)
\left[\frac{\Gamma(1/d)}{\Gamma(m/d)}\right]^2.
\]

The compact-wall asymptotic uses the scale
\(J\sim e^{-(m-1)/d}a^{-(3-n)/d}C_{m,n}(0)\).
Its proof and boundary conventions, rather than the special functions in isolation, carry the prospective transport contribution.

## Exact overlap: Yor's beta–gamma law

Let

\[
A_t^{(\mu)}=\int_0^t\exp[2(B_s+\mu s)]\,ds
\]

for standard Brownian motion \(B\). If \(T_q\) is an independent exponential time of rate \(q>0\), then

\[
A_{T_q}^{(\mu)}\overset{\rm law}=\frac{U}{2G},\quad
U\sim\operatorname{Beta}(1,\alpha),\quad
G\sim\operatorname{Gamma}(\beta,1),
\]

independently, with
\(v=\sqrt{\mu^2+2q}\), \(\alpha=(v+\mu)/2\),
\(\beta=(v-\mu)/2\).
This is explicitly Theorem 4.12, equation (4.18), of **Matsumoto and Yor (2005), “Exponential functionals of Brownian motion, I: Probability laws at fixed time,” Probability Surveys 2, 312–347**. [Open primary-author account](https://arxiv.org/pdf/math/0511517).

The identity predates that account. **Dufresne, “Bessel processes and Asian options,” Section 4**, attributes it to **Yor (1992), “On some exponential functionals of Brownian motion,” Advances in Applied Probability 24, 509–531**, and also cites Yor's 1992 C. R. Acad. Sci. note on random times. The original paper's 1991 technical-report version is openly accessible. [Dufresne's author manuscript](https://ozdaniel.com/A/DufresneBessel2005.pdf), [Yor's original technical report](https://digicoll.lib.berkeley.edu/record/86110/files/310.pdf), [journal DOI](https://doi.org/10.1017/S0001867800024381).

### Direct reduction of the candidate to the known law

The following change of variables is the audit's explicit overlap calculation. It gives a probabilistic derivation independent of the repository's Hankel-transform calculation.

For \(m=n=2\), nondimensionalize to

\[
H_\zeta=-\partial_x(x^2\partial_x)+x^2+\zeta.
\]

On the positive half-line, the underlying diffusion generator is
\(Lf=x^2f''+2xf'\). Hence
\(X_t=x\exp(t+\sqrt2W_t)\). Its accumulated quadratic killing obeys

\[
\int_0^tX_s^2\,ds\overset{\rm law}=
\frac{x^2}{2}A_{2t}^{(1/2)}.
\]

Use Feynman–Kac, integrate over the two symmetric half-lines, and then set \(u=2t\). Positivity justifies Tonelli:

\[
\begin{aligned}
C_{2,2}(\zeta)
&=2\int_0^\infty\!dx\int_0^\infty\!dt\,
e^{-\zeta t}\mathbb E\exp[-x^2A_{2t}^{(1/2)}/2]\\
&=\sqrt{\pi/2}\int_0^\infty e^{-\zeta u/2}
\mathbb E[(A_u^{(1/2)})^{-1/2}]\,du.
\end{aligned}
\]

For \(\zeta>0\), write this as

\[
C_{2,2}(\zeta)=\frac{\sqrt{2\pi}}\zeta
\mathbb E[(A_{T_{\zeta/2}}^{(1/2)})^{-1/2}].
\]

Now set \(\nu=\sqrt{1/4+\zeta}\),
\(\alpha=\nu/2+1/4\), \(\beta=\nu/2-1/4\). Elementary beta and gamma moments give

\[
\begin{aligned}
\mathbb E[(U/(2G))^{-1/2}]
&=\sqrt2\frac{\Gamma(\beta+1/2)}{\Gamma(\beta)}
\frac{\Gamma(1/2)\Gamma(\alpha+1)}{\Gamma(\alpha+1/2)}\\
&=\frac{\sqrt{2\pi}\,\zeta}{4}
\left[\frac{\Gamma(\alpha)}{\Gamma(\alpha+1/2)}\right]^2,
\end{aligned}
\]

where \(\beta+1/2=\alpha\) and \(\alpha\beta=\zeta/4\). Substitution yields exactly

\[
\boxed{C_{2,2}(\zeta)=\frac\pi2
\left[\frac{\Gamma(\nu/2+1/4)}{\Gamma(\nu/2+3/4)}\right]^2.}
\]

At \(\zeta=0\), use monotone convergence from positive floors; the expression tends to \(\pi^2/2\). The beta–gamma identity itself is used only at a strictly positive exponential rate. No appeal to a nonexistent rate-zero exponential random variable is needed.

Thus the local crossover is a direct negative-half-moment specialization of an established distributional formula. It should not be presented as a new identity about geometric Brownian motion or special functions.

## General exponents: known inverse-square and Mellin machinery

**Dereziński and Richard (2016), “On Schrödinger operators with inverse square potentials on the half-line.”** Sections 4.1–4.3 provide explicit resolvents, spectral densities, and Hankel diagonalization for homogeneous inverse-square operators. These include the distinct scale-invariant boundary branches. That literature is directly relevant to the signed order \(\nu=(n-1)/(m+2-n)\) in the repository derivation. For \(n<1\), replacing the natural signed-order branch by the positive-order Friedrichs branch would change the problem. This domain issue is established operator theory, but correctly carrying it through the transport reduction matters. [Open primary manuscript](https://arxiv.org/pdf/1604.03340), [journal article](https://doi.org/10.1007/s00023-016-0520-7).

The source transformation in the general-coefficient derivation is precisely the classical Mellin integral

\[
\int_0^\infty t^\mu J_\nu(t)\,dt
=2^\mu\frac{\Gamma((\nu+\mu+1)/2)}{\Gamma((\nu-\mu+1)/2)},
\]

with its convergence conditions. [NIST DLMF 10.22.43](https://dlmf.nist.gov/10.22.E43). Combining this with the inverse-square resolvent and an elementary beta integral produces the coefficient above. I did not find its exact two-exponent expression in the inspected sources, but it is a direct computable consequence of their machinery. The literature audit therefore supports “explicit coefficient for this transport model,” not “new Bessel integral” or “new spectral transform.”

Classical exponential-functionals literature extends much further than the simple beta–gamma identity, including Bessel time changes and Mellin transforms for Lévy exponential functionals. No such generalization is required to establish the exact quadratic-mobility overlap, so citing a large collection of adjacent probability papers would obscure the closest precedent.

## Coupled adsorption application and search limits

General adsorption/desorption Taylor dispersion, lateral surface transport, and distributed trapping rates are established; the earlier audit in [singular-exchange-prior-art.md](singular-exchange-prior-art.md) records the relevant sources and historical access gaps. Searches adding coincident mobility zeros, degenerate diffusion, power-law killing, mean lifetime, and adsorption dispersion did not locate the present compact-wall theorem with both exponents and the stated natural domain.

| Result or claim | Audit assessment |
|---|---|
| Gamma floor crossover for the local \(m=n=2\) model | Exact corollary of Yor's known beta–gamma identity. |
| General zero-floor gamma coefficient | No verbatim match found; classical inverse-square spectral theory plus a standard Mellin integral gives it directly. |
| Threshold \(m<1\) or \(n<3\) | Elementary weighted-energy application; useful physical criterion, weak novelty as pure analysis. |
| Same finite coefficient despite failure of an \(L^2\) corrector | Standard extended-energy distinction applied to the model; retain it for correctness and interpretation. |
| Compact-wall localization and adsorption-dispersion consequences | No exact collision located; plausible applied-theory contribution under the stated assumptions. |

A defensible presentation would derive the transport classification, explicitly credit the known local kernels and probability identity, and prove the compact-wall asymptotic. It should distinguish the well-mixed bulk reduction from any additional theorem about a finite-diffusivity bulk. The mathematical review, not this search, determines which coupled-model extensions are established.
