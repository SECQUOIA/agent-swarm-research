# Independent review of asymptotic Fourier identification

Date: 2026-09-07. Reviewer: /root/closure_direction/review_rigidity. Scope: the derivation supplied by the root agent and the full written [Fourier-identification result](../results/fourier-identification.md), read on this date. The review starts from the established log-characteristic Duhamel equation and its exponentially decaying source bound; it does not independently reprove that preceding log-size estimate.

## Verdict

The amplitude limit, asymptotic characteristic-function ratio, local recovery of the fragmentation exponent, and uniqueness of the daughter measure from that local exponent are correct. The proof requires neither an initial logarithmic moment nor a daughter logarithmic moment. The lower-half-plane argument has the correct sign.

The identification conclusion is an exact-data uniqueness result. It does not establish stable numerical recovery, a finite-time parameter estimator, or uniqueness of the underlying nonlinear population equation. Recovery of the coagulation coefficient additionally requires the conserved mass and the unnormalized particle-count growth rate.

The completed manuscript implements the continuity, phase, data-scope, and stability qualifications checked below. No mathematical correction was needed after the full-draft audit.

## Assumptions checked

Let \(b=\lambda m>0\), \(\sigma\ge0\), and let the parent-independent daughter measure \(B\) be a nonnegative finite measure on \((0,1)\) satisfying
\[
B((0,1))=2,\qquad \int\theta\,B(d\theta)=1.
\]

The coefficients and daughter measure are constant in time. A global mass-conserving weak solution supplies normalized characteristic functions
\[
\phi_t(k)=\mathbb E e^{ik\log X_t},\qquad k\in\mathbb R.
\]

Assume the established scalar integral equation
\[
\phi_t(k)=e^{\psi(k)t}\phi_0(k)
+\int_0^t e^{\psi(k)(t-s)}r_s(k)\,ds,
\tag{1}
\]
\[
\psi(k)=\sigma\int(\theta^{ik}-1)\,B(d\theta),\qquad
|r_s(k)|\le |k|a_0e^{-\omega s},
\tag{2}
\]

where \(a_0<\infty\) and \(\omega>0\). The proposed values \(a_0=\lambda H_0^2/N_0\) and \(\omega=\kappa(b+\sigma)\) may be substituted when their earlier hypotheses hold. Positivity of \(\omega\) is essential to this argument. No derivative of \(\phi_t\) in \(k\) is assumed.

Since \(B\) is finite, \(\psi\) is continuous, \(\psi(0)=0\), and \(\operatorname{Re}\psi(k)\le0\).

## Amplitude and remainder

Set \(\delta(k)=\omega+\operatorname{Re}\psi(k)\). Continuity supplies an interval around zero on which \(\delta(k)>0\). For such \(k\), the integral
\[
C(k)=\phi_0(k)+\int_0^\infty e^{-\psi(k)s}r_s(k)\,ds
\tag{3}
\]

is absolutely convergent, since its integrand has modulus at most \(|k|a_0e^{-\delta(k)s}\). Subtracting the tail from (1) gives
\[
\left|\phi_t(k)-e^{\psi(k)t}C(k)\right|
\le \frac{|k|a_0}{\delta(k)}e^{-\omega t},
\tag{4}
\]

and equivalently
\[
\left|e^{-\psi(k)t}\phi_t(k)-C(k)\right|
\le A(k)e^{-\delta(k)t},\qquad
A(k)=\frac{|k|a_0}{\delta(k)}.
\tag{5}
\]

The exponent in (4) is indeed \(\omega\), rather than \(\delta(k)\): multiplication by \(e^{\operatorname{Re}\psi(k)t}\) cancels the additional real part in (5).

There is a particularly clean continuity proof. Restrict to a compact interval \(I\) around zero on which \(\delta\ge\delta_*>0\). The finite-time functions \(e^{-\psi(k)t}\phi_t(k)\) are continuous in \(k\), and (5) gives uniform convergence on \(I\). Their limit \(C\) is therefore continuous. This proof does not need an additional pointwise-in-\(k\) regularity assumption on the chosen source representative \(r_s(k)\). Also, \(\phi_t(0)=1\), so \(C(0)=1\). After shrinking \(I\), there is \(c>0\) with \(|C(k)|\ge c\) throughout it.

Nothing in this argument says that \(C\) itself is a characteristic function or the transform of a probability distribution. It is a continuous asymptotic amplitude; no stronger interpretation is needed.

## Ratio convergence and phase

Write \(e^{-\psi(k)t}\phi_t(k)=C(k)+\varepsilon_t(k)\), with the bound in (5). For fixed \(h>0\), sufficiently large \(t\) makes \(\phi_t(k)\ne0\), and
\[
\frac{\phi_{t+h}(k)}{\phi_t(k)}-e^{h\psi(k)}
=e^{h\psi(k)}
\frac{\varepsilon_{t+h}(k)-\varepsilon_t(k)}
{C(k)+\varepsilon_t(k)}.
\]

In particular, whenever \(A(k)e^{-\delta(k)t}<|C(k)|\),
\[
\left|\frac{\phi_{t+h}(k)}{\phi_t(k)}-e^{h\psi(k)}\right|
\le
\frac{e^{h\operatorname{Re}\psi(k)}A(k)
(1+e^{-h\delta(k)})}
{|C(k)|-A(k)e^{-\delta(k)t}}\,
e^{-\delta(k)t}.
\tag{6}
\]

This establishes the stated rate. A smaller fixed interval with \(|C|\ge c\) and \(\delta\ge\delta_*\) also gives uniform ratio convergence and a common eventual time after which the denominators do not vanish.

The fixed-lag ratio by itself records an exponential, so its logarithm has a branch ambiguity unless the normalization at zero is used. Here \(\psi(0)=0\) and \(\psi\) is continuous. Shrink the interval until \(|h\operatorname{Im}\psi(k)|<\pi\). On it,
\[
\psi(k)=h^{-1}\operatorname{Log}
\left(\lim_{t\to\infty}\frac{\phi_{t+h}(k)}{\phi_t(k)}\right)
\tag{7}
\]

with the principal logarithm. Thus there is no local phase alias. Equivalently, use the unique continuous logarithm normalized to zero at \(k=0\). Claiming a principal-log formula at arbitrary frequencies without this qualification would be incorrect.

For finite-time numerical work, the denominator \(\phi_t(k)\) may be exponentially small even though it is eventually nonzero. Equation (6) is an exact mathematical error estimate, not protection against measurement or roundoff error in that ratio.

## Uniqueness of a one-sided jump measure from local data

Define the finite nonnegative measure
\[
\nu=\sigma(\log)_\#B
\quad\text{on }(-\infty,0).
\]

Suppose two such measures give the same exponent on a nonempty open real interval. Their finite signed difference \(\Delta\nu\) satisfies
\[
\int(e^{iky}-1)\,\Delta\nu(dy)=0
\]

there. Set
\[
\mu=\Delta\nu-\Delta\nu(\mathbb R)\delta_0.
\]

This is a finite signed measure supported on \((-\infty,0]\), and its Fourier transform vanishes on the interval. Its complex transform
\[
F(z)=\int e^{izy}\,\mu(dy)
\]

is holomorphic for \(\operatorname{Im}z<0\), bounded there by \(\|\mu\|_{\rm TV}\), and continuous up to the real axis. Indeed, for \(y\le0\) and \(\operatorname{Im}z<0\), \(|e^{izy}|\le1\). On compact subsets of the lower half-plane, all factors \(|y|^j|e^{izy}|\) are bounded, justifying complex derivatives without moments of \(|y|\). Boundary continuity follows by dominated convergence.

On the interval in question, the continuous boundary value is zero and hence real. The Schwarz reflection principle extends \(F\) analytically across every smaller interval. The extension has a real interval of zeros in its interior, so the identity theorem makes it zero. Consequently \(F\) vanishes throughout the lower half-plane and, by boundary continuity, on the whole real axis. Fourier uniqueness for finite signed measures gives \(\mu=0\).

Thus \(\Delta\nu=\Delta\nu(\mathbb R)\delta_0\). Both original measures are supported strictly below zero, so \(\Delta\nu\) has no atom at zero, forcing \(\Delta\nu=0\). This completes the uniqueness argument.

The support condition is important. A jump measure atom at zero contributes nothing to \(\int(e^{iky}-1)\nu(dy)\); without excluding it, its mass cannot be identified from this exponent. The present assumption \(B((0,1))=2\), with support in the open interval, excludes such null jumps. An atom at daughter fraction zero is also outside the model.

This analytic uniqueness statement is standard one-sided-transform reasoning; this review does not claim it as a new complex-analysis theorem.

## Parameter recovery and observed information

Once \(\nu\) is identified,
\[
\sigma=\frac{\nu(\mathbb R)}2.
\]

If \(\sigma>0\), the daughter measure is uniquely recovered by
\[
B=\sigma^{-1}(\exp)_\#\nu.
\]

When \(\sigma=0\), the exponent identifies the zero rate, but \(B\) is unidentifiable and has no effect on the dynamics. The conservation constraint provides the consistency check \(\int e^y\nu(dy)=\sigma\).

The manuscript's additional identity \(\psi(-i)=-\sigma\) is also correct: \(-i\) lies in the lower half-plane, \(e^{i(-i)y}=e^y\), and therefore \(\psi(-i)=\int(e^y-1)\nu(dy)=\sigma-2\sigma\). Its stated interpretation as an analytic identity, rather than a stable prescription for noisy continuation, is necessary and sufficient.

For the additive model, observed particle number has exponential rate \(r_{\rm count}=\sigma-\lambda m\). If the conserved mass \(m>0\) is known and this unnormalized count rate is observed, then
\[
\lambda=\frac{\sigma-r_{\rm count}}m.
\]

Normalized characteristic functions alone do not provide the unnormalized count rate or the physical mass scale. Accordingly, the final statement should specify marginal traces that include particle count and known or observed conserved mass, in addition to the normalized log-characteristic functions. The proof uses an open continuum of nearby frequencies; finitely many Fourier samples do not supply the analytic uniqueness conclusion.

## Stability limitation

Local exact determination by analytic continuation is not a quantitative stable inversion theorem. A simple illustration already respects both daughter constraints: for \(p,q\in(0,1)\), let \(B_p=\delta_p+\delta_{1-p}\) and \(B_q=\delta_q+\delta_{1-q}\). As \(q\to p\), their exponents converge uniformly on every bounded frequency interval, while their daughter measures have TV distance four whenever all four atoms are distinct. Thus the inverse cannot be continuous in daughter-measure total variation under that data norm.

This example does not rule out weaker stability under additional assumptions or in weaker metrics. None has been established here. The exact identifiability conclusion should remain separate from practical estimation, regularization, and noisy analytic continuation.

## Addendum: pointwise empirical ratios under independent sampling

Date: 2026-09-07. The root agent proposed the following supporting sampling application after the full-draft review. I subsequently read the complete [sampling tradeoff manuscript](../results/fourier-sampling-tradeoff.md). Its equations (1)–(6), observation model, and final scope qualifications agree with the independently checked argument below; no correction was needed. The manuscript calls the denominator \(A\) and numerator \(B\), reversing the temporary labels used in this addendum without changing the algebra. This is a pointwise ratio bound, not a stable inversion result for the daughter measure.

Fix one real frequency \(k\) in the established interval. Write \(r=-\operatorname{Re}\psi(k)\ge0\) and \(\delta=\omega-r>0\). Suppose that, for \(t\ge t_0\),
\[
\left|\frac{\phi_{t+h}(k)}{\phi_t(k)}-e^{h\psi(k)}\right|
\le K e^{-\delta t},
\qquad
|\phi_t(k)|\ge\frac c2 e^{-rt},
\tag{8}
\]

where \(c>0\). Take \(n\) independent identically distributed observations from each of \(\eta_t\) and \(\eta_{t+h}\), and form their empirical characteristic functions \(\widehat A\) and \(\widehat B\), respectively with the numerator and denominator ordering \(\widehat A=\widehat\phi_{t+h}(k)\), \(\widehat B=\widehat\phi_t(k)\). Samples independent across the two times are sufficient; the union bound below actually does not need cross-time independence.

For confidence parameter \(0<\beta<1\), set
\[
\varepsilon_n=2\sqrt{\frac{\log(8/\beta)}n}.
\]

Hoeffding for the real and imaginary parts, each bounded in \([-1,1]\), gives
\[
\mathbb P\!\left(
\max\{|\widehat A-\phi_{t+h}(k)|,\,
|\widehat B-\phi_t(k)|\}>\varepsilon_n
\right)
\le8e^{-n\varepsilon_n^2/4}=\beta.
\tag{9}
\]

The constant follows by testing each component at threshold \(\varepsilon_n/\sqrt2\), taking a union over real and imaginary parts, and then over the two times.

On the complementary event, assume also
\[
\varepsilon_n\le \frac c4e^{-rt}.
\tag{10}
\]

Then \(|\widehat B|\ge(c/4)e^{-rt}>0\). Let \(R_t=\phi_{t+h}/\phi_t\) and \(\widehat R_t=\widehat A/\widehat B\). Exact division gives
\[
|\widehat R_t-R_t|
\le\frac{\varepsilon_n(1+|R_t|)}{|\widehat B|}.
\]

Importantly, use the existing ratio estimate to bound \(|R_t|\le1+K e^{-\delta t}\le1+K\). Bounding only the numerator characteristic function by one would give an unnecessarily worse exponential denominator factor. The correct resulting estimate is
\[
|\widehat R_t-R_t|
\le K'\varepsilon_n e^{rt},\qquad
K'=\frac{4(2+K)}c.
\]

Together with (8),
\[
|\widehat R_t-e^{h\psi(k)}|
\le K e^{-\delta t}+K'\varepsilon_n e^{rt}
\quad\text{with probability at least }1-\beta.
\tag{11}
\]

There is also a valid observable error certificate on the event in (9):
\[
|\widehat R_t-R_t|
\le
\frac{\varepsilon_n(1+|\widehat R_t|)}
{|\widehat B|-\varepsilon_n},
\qquad |\widehat B|>\varepsilon_n.
\tag{12}
\]

To obtain it, expand \(A-\widehat R_t B\) around the empirical numerator and denominator, then use \(|B|\ge|\widehat B|-\varepsilon_n\). Its denominator condition is strict. At equality in (10), that strict observed condition is not automatic, although the nonzero-denominator estimate (11) still holds. Formula (12) controls sampling error to the exact finite-time ratio; the model bias in (8) must be added when the target is \(e^{h\psi(k)}\).

For sufficiently large \(n\), choose the deterministic observation time
\[
t_n=\frac{\log(1/\varepsilon_n)}{\omega}.
\]

Then \(t_n\ge t_0\), and (10) eventually holds because
\[
\varepsilon_n e^{rt_n}
=\varepsilon_n^{\delta/\omega}\longrightarrow0.
\]

Both terms in (11) have the same exponent:
\[
|\widehat R_{t_n}-e^{h\psi(k)}|
\le(K+K')\varepsilon_n^{\delta/\omega}
\quad\text{with probability at least }1-\beta
\]

for all sufficiently large \(n\). At fixed confidence this is order \(n^{-\delta/(2\omega)}\). The case \(r=0\) is included. If confidence changes with \(n\), retain the explicit \(\varepsilon_n\) rather than omitting its logarithmic factor.

This schedule is a sufficient bias-noise balance and is not claimed minimax optimal. It assumes the decay scale needed to choose the observation time is known or otherwise supplied by a specified parameter class. It does not supply an adaptive schedule for unknown kinetic parameters. The probability statement is for a fixed frequency and predetermined observation time; data-dependent frequency or time selection needs additional analysis. The samples represent iid draws from deterministic continuum marginal laws, not an unverified independence approximation for interacting particles in one finite reactor.

With a fixed local logarithm branch separated from its cut, the same pointwise convergence transfers to the exponent by local Lipschitz continuity of the logarithm. It still does not justify noisy analytic continuation, recovery of \(\sigma\) through a complex argument, or stable reconstruction of all of \(B\).
