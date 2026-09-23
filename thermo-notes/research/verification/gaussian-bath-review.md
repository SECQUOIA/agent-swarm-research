# Independent review: Gaussian reservoirs at coexistence

Date: 2026-09-06. Reviewer: `check_bath_threshold`.

This note records an independent mathematical review of the exact model in [the ensemble scouting note](../scouting-ensembles.md). The threshold and crossover formulas below are correct under their stated assumptions. Literature novelty was **not checked by this reviewer**. These results alone do not establish publishability or validity for a molecular coexistence distribution.

## Model and exact transformation

Let

\[
p_N(E)=\tfrac12\phi_{s_N}(E-m_N)+\tfrac12\phi_{s_N}(E+m_N),
\qquad m_N/s_N\to\infty,
\]

and

\[
q_{N,t}(E)\propto p_N(E)\exp(tE-\kappa_NE^2/2),
\qquad \kappa_N\ge0.
\]

Here \(\phi_s\) is a centered normal density with variance \(s^2\), and total variation is one half of the L1 distance between densities. Write

\[
r=m/s,\qquad k=\kappa s^2,\qquad b=ts.
\]

Completion of squares shows that the law of \(E/s\) under \(q\) is exactly a two-normal mixture with common variance, component means, and upper weight

\[
v=\frac1{1+k},\qquad
\mu_\pm=\frac{\pm r+b}{1+k},\qquad
\pi_+=\frac1{1+\exp[-2rb/(1+k)]}.
\]

This verifies the formulas in the scouting note directly.

## Exact criterion for vanishing total variation

The necessary and sufficient condition is

\[
\exists\,t_N:\ d_{\rm TV}(p_N,q_{N,t_N})\to0
\quad\Longleftrightarrow\quad
\kappa_Nm_Ns_N\to0.
\]

For sufficiency, take \(t_N=0\). Since \(r_N\to\infty\), the condition \(k_Nr_N\to0\) implies \(k_N\to0\). The weights remain one half, variances converge to the target variance in standardized units, and the component mean displacements \(\mp k_Nr_N/(1+k_N)\) vanish. Each component converges in total variation, and so does its mixture.

For necessity, convergence in total variation requires the transformed law to retain the target probabilities near both modes. The target modes are separated by \(2r_N\to\infty\), whereas each transformed component has standard deviation at most one. Therefore one component cannot supply substantial probability to both target neighborhoods. Both components must have nonvanishing weights and lie within bounded standardized distance of their respective target modes. Their separation \(2r_N/(1+k_N)\) must consequently equal \(2r_N+O(1)\), forcing \(k_N\to0\) and bounded \(k_Nr_N\). The common translation \(b_N/(1+k_N)\) is bounded as well.

Pass to a subsequence along which the bounded component displacements and weights converge. In each translated phase neighborhood, the other component disappears. Equality with the limiting target measure then requires the local weight to be one half and its normal mean displacement to be zero. Thus both

\[
\frac{b_N-k_Nr_N}{1+k_N}\to0,
\qquad
\frac{b_N+k_Nr_N}{1+k_N}\to0.
\]

Subtracting proves \(k_Nr_N\to0\). The subsequence argument applies to every subsequence, giving the full necessary limit.

For \(m_N\asymp N\), \(s_N\asymp N^{1/2}\), and \(\kappa_N\asymp c_B^{-1}\) at fixed nonzero temperature, the condition becomes \(c_B\gg N^{3/2}\). Here \(c_B=C_B/k_B\) is dimensionless bath heat capacity. This inference assumes the Gaussian bath and subsystem model, or a separately justified extension.

## Finite crossover and optimized error

If \(k_Nr_N\to a\in[0,\infty)\), then \(k_N\to0\). At zero tilt the two standardized mean displacements approach \(\mp a\). Separation of the phase neighborhoods gives

\[
\lim_N d_{\rm TV}(p_N,q_{N,0})=2\Phi(a/2)-1.
\]

This is the phase-balanced error. It must not be described as the optimum over all tilts. The exact limiting optimum is

\[
\lim_N\inf_t d_{\rm TV}(p_N,q_{N,t})
=\min\{2\Phi(a/2)-1,\tfrac12\}.
\]

To check the lower bound, take any sequence of tilts and a subsequence along which the upper component weight converges. If both weights have positive limits, the logistic formula forces \(b_N=O(1/r_N)\). The local component displacements are then fixed at \(\mp a\). The limiting L1 error is convex in the remaining choice of upper weight, and reflection makes it symmetric around one half. It is therefore minimized at equal weights, giving the balanced expression. If either weight tends to zero, the surviving component, whose variance tends to one, cannot cover both increasingly separated target neighborhoods. The missing target neighborhood gives a TV lower bound of one half. If the surviving mean escapes both target neighborhoods, the error is larger.

Zero tilt attains the balanced bound. For \(a>0\), choosing \(t_N=\kappa_Nm_N\), or \(b_N=k_Nr_N\), leaves the upper component mean exactly at \(r_N\). Its variance tends to one, and its weight tends to one because

\[
\frac{2r_Nb_N}{1+k_N}
=\frac{2k_Nr_N^2}{1+k_N}\to\infty.
\]

The corresponding TV limit is one half. When \(a=0\), the balanced construction already attains zero.

The change in the preferred limiting approximation occurs at

\[
a_*=2\Phi^{-1}(3/4)\approx1.34898.
\]

Above this value the scalar TV objective favors reproducing one phase and abandoning the other. That is a limitation of this fitting objective, not recovery of coexistence. Phase weights should accompany any optimized-error report.

## Unequal weights and the bath reference energy

Let the upper target phase have fixed weight \(w\in(0,1)\), with \(w\ne1/2\). Its mean is \(\bar E=(2w-1)m\). A quadratic bath centered at that mean has residual weight

\[
\exp[-\kappa(E-\bar E)^2/2],
\]

equivalent to \(t=\kappa\bar E\). Its exact phase log odds are

\[
\log\frac{\pi_+}{1-\pi_+}
=\log\frac{w}{1-w}
+\frac{2(2w-1)\kappa m^2}{1+\kappa s^2}.
\]

For this specified centering, convergence in TV occurs if and only if \(\kappa m^2\to0\). Necessity follows from component matching and preservation of the nonzero target phase weights; sufficiency follows directly from the exact weights, means, and variances. With the usual coexistence scaling, this gives \(c_B\gg N^2\).

This stronger condition is not a generic consequence of unequal weights. A bath centered at the midpoint \(E=0\) preserves the original weights exactly for every \(\kappa\), including unequal weights, and only requires \(\kappa ms\to0\). A freely chosen linear tilt can also cancel the mean-centering bias. The reference energy or temperature prescription must therefore be stated explicitly.

## Scope of the smooth-bath extension

For an exactly Gaussian-mixture reference, a globally concave residual bath log-weight \(g_N\) admits a useful sufficiency argument. Choose the secant tilt

\[
t_N=-\frac{g_N(m_N)-g_N(-m_N)}{2m_N},
\qquad h_N(E)=g_N(E)+t_NE.
\]

The endpoint values agree. Uniformly small curvature on the gap and fixed standardized phase neighborhoods, in the form

\[
m_Ns_N\sup_{|E|\le m_N+Rs_N}|g_N''(E)|\to0
\quad\text{for each fixed }R,
\]

makes the log-weight variation vanish locally in each phase and gives \(s_Nh_N'(\pm m_N)\to0\). The concave tangent bound

\[
h_N(\pm m_N+s_Nz)-h_N(\pm m_N)
\le s_Nh_N'(\pm m_N)z
\]

controls normalization under each standard normal component. Local convergence and the Gaussian exponential moment then give L1 convergence after normalization. If the bath has a restricted domain, the phase neighborhoods must lie inside it eventually and the weight must be zero outside; the same upper bound applies there.

This supports a smooth-bath sufficiency extension for an exact Gaussian reference. A generalized necessity statement under a positive lower curvature bound still needs a complete formulation and proof for the chosen domains. A real coexistence distribution also needs independent control of valley states and tails: a local Gaussian approximation alone does not justify transferring the result.

## Review conclusion

The exact Gaussian-model iff threshold, balanced crossover, optimized crossover, and mean-centered unequal-weight criterion pass this independent review. Their assumptions and distinctions must remain explicit. This reviewer did not search prior literature, and makes no novelty or publishability claim.
