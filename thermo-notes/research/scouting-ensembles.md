# Finite reservoirs at coexistence: a sharp distribution-level obstruction

Superseded by [the complete LaTeX paper](../paper-finite-reservoirs/README.md), which retains these exact Gaussian results and adds physical microscopic iff theorems, boundary optimization, and rigorous tail qualifications. Earlier next-step and missing-short-range statements below are development history.

Date: 2026-09-06. Status: a verified result for an exact Gaussian-mixture model, with a conditional physical extension and unresolved prior-art risk. This is **not yet a publishability claim**.

## Main finding

For a two-phase canonical energy distribution with latent-energy separation proportional to system size and ordinary within-phase fluctuations proportional to its square root, a finite Gaussian reservoir can reproduce the complete canonical energy distribution in total variation only when its heat capacity grows faster than the system size to the power 3/2. This remains necessary even if the reservoir's temperature is freely retuned. Keeping the bath temperature fixed at a generic reference instead can require growth faster than size squared.

The elementary finite-bath mechanism and the Gaussian coexistence approximation are established ideas. The candidate contribution is the **sharp distinction between phase-weight matching, within-phase distribution matching, and barrier matching**, expressed in a probability metric that controls event probabilities. The derivation also exposes why an unscaled Euclidean distance between spreading energy histograms can tend to zero while physically measurable probability differences remain finite.

This direction fits Corti's work on operational finite-system ensemble consistency. It could become a focused theoretical paper with a rigorous extension to smooth physical baths, a molecular or Potts-model example, and a complete comparison with the early Gaussian-ensemble literature. Its potential impact is moderate; the current exact-model theorem alone is probably insufficient for a strong paper.

## Established starting point and prior-art boundaries

For weak energy coupling and an isolated composite, the subsystem energy density is

\[
 q(E)\propto\omega_S(E)\omega_B(E_{\rm tot}-E).
\]

Writing the dimensionless bath entropy as \(s_B=\log\omega_B\), its expansion gives a canonical factor and a negative quadratic correction when the bath has positive heat capacity. With \(\beta=1/(k_BT)\) and dimensionless heat capacity \(c_B=C_B/k_B\),

\[
 -s_B''=\frac{\beta^2}{c_B}\equiv\kappa.
\]

This is established Gaussian-ensemble theory, not a new derivation. Johal, Planes and Vives explicitly derive a quadratic bath correction in their section II and distinguish an exactly quadratic bath entropy from a constant-heat-capacity bath in section VII. [Open primary full text](https://arxiv.org/html/cond-mat/0307646v1).

The most important prior-art gap is Challa, Landau and Binder, *Monte Carlo studies of finite-size effects at first-order transitions*, **Phase Transitions** 24–26, 343–369 (1990), [DOI](https://doi.org/10.1080/01411599008210236). Its accessible abstract explicitly discusses both a Gaussian mixture description of first-order distributions and a finite reservoir. Full text has not yet been obtained or checked. Challa and Hetherington's 1988 papers, [PRL 60, 77](https://doi.org/10.1103/PhysRevLett.60.77) and [PRA 38, 6324](https://doi.org/10.1103/PhysRevA.38.6324), are also essential unresolved full-text checks. These could already contain the required finite-size scales, even if not stated in total variation.

Costeniuc, Ellis, Touchette and Turkington's [generalized-ensemble work](https://arxiv.org/html/cond-mat/0505218v2) establishes thermodynamic and equilibrium-macrostate equivalence with generalized canonical ensembles; it is necessary background, but those equivalence notions must not be silently identified with total variation convergence of the full finite-system law.

The local Griffin–Matty–Swendsen paper compares finite-bath and canonical energy distributions with an unscaled Euclidean metric; the oscillator scaling and first-order Potts observations are in [[griffin2017-finite-thermal-reservoirs-and-the]] p.3-7. It motivates the probability-metric issue developed below. [Open preprint](https://arxiv.org/abs/1608.05455).

## Exact model and theorem

Let \(\phi_s(E-a)\) denote the normal density with mean \(a\) and variance \(s^2\). Consider

\[
 p_N(E)=\tfrac12\phi_{s_N}(E-m_N)+\tfrac12\phi_{s_N}(E+m_N),
 \qquad m_N/s_N\longrightarrow\infty.
\]

The energy origin lies halfway between phases. This is an exact probability model, not an assertion that a short-range fluid has Gaussian tails throughout its coexistence interval. Define the Gaussian-bath family

\[
 q_{N,t}(E)=Z_{N,t}^{-1}p_N(E)
 \exp\{tE-\kappa_NE^2/2\},\qquad \kappa_N\ge0.
\]

The parameter \(t\) permits arbitrary adjustment of the linear reservoir bias relative to the reference canonical law. The metric is

\[
 d_{\rm TV}(p,q)=\tfrac12\int|p-q|\,dE
 =\sup_A|P(A)-Q(A)|.
\]

**Theorem.** There exists a sequence \(t_N\) for which
\(d_{\rm TV}(p_N,q_{N,t_N})\to0\) if and only if

\[
 \boxed{\kappa_Nm_Ns_N\longrightarrow0.}
\]

Thus, for \(m_N=\Theta(N)\), \(s_N=\Theta(N^{1/2})\), and fixed nonzero temperature, the condition is

\[
 \boxed{c_B\gg N^{3/2}.}
\]

The heat capacity here is that of the reservoir, not the canonical heat capacity of the two-phase system, which includes the latent-heat contribution.

### Completion of squares

Suppress subscripts. Each transformed Gaussian has variance and mean

\[
 v=\frac{s^2}{1+\kappa s^2},\qquad
 \mu_\pm=\frac{\pm m+ts^2}{1+\kappa s^2}.
\]

The transformed upper-phase weight is exactly

\[
 w_+=\frac{1}{1+\exp[-2tm/(1+\kappa s^2)]}.
\]

Introduce \(r=m/s\), \(k=\kappa s^2\), \(b=ts\). In units of the canonical within-phase standard deviation, the two means are \((\pm r+b)/(1+k)\), the variance is \((1+k)^{-1}\), and the target means are \(\pm r\).

### Sufficiency

Take \(t=0\). The weights remain exactly one half. The standardized component mean displacements have magnitude

\[
 a_N=\frac{\kappa_Nm_Ns_N}{1+\kappa_Ns_N^2}.
\]

The theorem's condition implies \(\kappa_Ns_N^2\to0\), because \(s_N/m_N\to0\). Each corresponding pair of normal laws therefore converges in total variation. Convexity of total variation for mixtures gives convergence of the complete distributions.

### Necessity

If total variation tends to zero, the two canonical windows at \(\pm m_N\), whose width is a fixed multiple of \(s_N\), must each retain their canonical probability. The transformed Gaussian components have standard deviation no larger than \(s_N\). A single such component cannot supply substantial mass to both windows separated by \(2m_N/s_N\to\infty\). Consequently both components must retain nonvanishing weights and match the respective target windows. Taking increasing fixed window widths and then using the conditional normal laws forces their standardized variances to tend to one and their standardized mean displacements to tend to zero. Thus

\[
 k_N\to0,\qquad
 \frac{b_N-k_Nr_N}{1+k_N}\to0,\qquad
 \frac{b_N+k_Nr_N}{1+k_N}\to0.
\]

Subtracting the last two limits gives \(k_Nr_N=\kappa_Nm_Ns_N\to0\). This argument can be formalized as asymptotic identifiability of two separated normal components. It does not assume that the temperature adjustment preserves phase weights in advance.

### Nonzero limiting error

For the phase-balanced choice \(t_N=0\), if
\(\kappa_Nm_Ns_N\to a\in[0,\infty)\), separation of the two phases and the normal translation formula give

\[
 \lim_{N\to\infty}d_{\rm TV}(p_N,q_{N,0})
 =2\Phi(a/2)-1.
\]

Here \(\Phi\) is the standard-normal CDF. This is the error for the phase-balanced bath, **not** the minimum over all temperature adjustments. At sufficiently large \(a\), one can make the bath concentrate on and approximately align one phase, giving an error approaching one half and improving on the symmetric choice. It still fails to converge to the desired two-phase law.

## Why a fixed temperature can need a still larger bath

Replace the equal weights by fixed \(w\) and \(1-w\), with \(w\in(0,1)\) and \(w\ne1/2\). The reference canonical mean is \(\bar E=(2w-1)m\). Suppose the bath's tangent inverse temperature is fixed at this mean, so the residual factor is

\[
 \exp[-\kappa(E-\bar E)^2/2].
\]

This corresponds to \(t=\kappa\bar E\). The transformed phase log odds are exactly

\[
 \log\frac{w_+^B}{1-w_+^B}
 =\log\frac{w}{1-w}
 +\frac{2\kappa(2w-1)m^2}{1+\kappa s^2}.
\]

Full-distribution convergence first requires the within-phase width ratio to tend to one. Under that necessary condition, phase-weight convergence therefore requires \(\kappa m^2\to0\), or \(c_B\gg N^2\). This condition is also sufficient in the exact model. For a bath centered at the midpoint, or for a deliberately adjusted linear bias, the leading phase-weight error cancels and the weaker \(N^{3/2}\) scale remains.

This fixed-temperature statement concerns a **specified reference energy**. It must not be confused with self-consistent finite-bath constructions in which the expansion point is the already modified mean energy.

## A related diagnostic: Euclidean histogram convergence can be misleading

Consider even a single Gaussian canonical peak
\(p=\mathcal N(0,\sigma^2)\). Multiplication by a quadratic bath factor gives
\(q=\mathcal N(0,r\sigma^2)\), where

\[
 r=\frac{c_B}{c_S+c_B}\in(0,1)
\]

if \(\sigma^2=c_S/\beta^2\). For any fixed \(r\),

\[
 \|p-q\|_2^2
 =\frac{1}{2\sqrt\pi\,\sigma}
 \left[1+r^{-1/2}-2\sqrt{\frac{2}{1+r}}\right]
 \longrightarrow0
\]

as \(\sigma\to\infty\). In contrast, total variation is independent of \(\sigma\):

\[
 d_{\rm TV}(p,q)=2\left[
 \Phi\!\left(\sqrt{\frac{\log r}{r-1}}\right)
 -\Phi\!\left(\sqrt{\frac{r\log r}{r-1}}\right)
 \right]>0.
\]

For equal system and reservoir heat capacities, the variance ratio is one half and the limiting TV error is approximately 0.1661. A reservoir heat capacity 1000 times smaller gives an error approximately 0.9252. The event distinguishing the distributions is the central fluctuation interval bounded by the two density crossings.

The same dilution occurs for discrete Gaussian histograms with a fixed microscopic energy bin: the L2 norm falls like \(N^{-1/4}\) when the physical width grows like \(\sqrt N\), even at a fixed nonzero TV discrepancy. This is an elementary probability fact, not claimed as a new theorem. Its application prevents an incorrect interpretation of a small spreading-histogram metric as uniform agreement of physical event probabilities. Local thermodynamic observables can still agree, and this calculation does not deny those weaker forms of ensemble equivalence.

## Barrier accuracy is a separate requirement

For an arbitrary reference energy density with phase energies at \(\pm m\), a phase-balanced quadratic bath changes the log-density ratio between an endpoint and an intermediate energy \(E^\ddagger\) by exactly

\[
 B_B(E^\ddagger;m)-B_{\rm can}(E^\ddagger;m)
 =-\frac{\kappa}{2}\left[m^2-(E^\ddagger)^2\right].
\]

Here the barrier means the log-density ratio evaluated at these **specified energies**. The identity alone does not locate the actual displaced peaks or saddle. For \(E^\ddagger=0\), it lowers this barrier by \(\kappa m^2/2\).

If a short-range model has a canonical interfacial barrier \(B_N\asymp N^{(d-1)/d}\), and separate control shows that shifts of the relevant stationary points are subleading, relative barrier accuracy requires

\[
 c_B\gg N^2/B_N\asymp N^{1+1/d}.
\]

This is a **conditional scaling inference**, not an additional theorem for the double Gaussian model: the exact two-Gaussian model has an extensive artificial valley barrier and cannot itself validate interfacial scaling. In three dimensions the inferred barrier scale \(N^{4/3}\) is smaller than the distribution-matching scale \(N^{3/2}\), leaving a possible regime in which the leading interfacial barrier is accurate but the full histogram remains strongly distinguishable. In two dimensions the two powers coincide.

An absolute barrier error tending to zero is stronger than relative accuracy and instead needs \(c_B\gg N^2\) in this quadratic model. For rates, a subleading but diverging barrier error can still imply an exponentially large multiplicative error. This distinction is important for nucleation applications.

## Extension to physical baths: what is proved and what remains

A quadratic bath entropy is a legitimate idealized reservoir model locally, but is not globally a constant-positive-heat-capacity reservoir. For a physical bath with smooth extensive entropy, the quadratic approximation must be controlled over both phase windows. At the threshold \(c_B\asymp N^{3/2}\), the cubic term at the phase centers can be order one because its nominal size is \(N^3/c_B^2\). It cannot simply be dropped when claiming the crossover formula.

A promising route is to choose the reservoir energy so that the *secant* entropy slope between the two phase centers matches the canonical inverse temperature. This removes the endpoint phase bias exactly. If \(-s_B''\sim\beta^2/c_B\) uniformly over the latent-energy interval, the residual slopes at the endpoints remain of order \(N/c_B\). Their variation across a phase width is order \(N^{3/2}/c_B\), giving the same obstruction. A proof still needs tail control and a demonstration that intermediate states cannot gain appreciable mass under reweighting. Gaussian approximations valid only in the original peak neighborhoods are not sufficient: an exponentially rare canonical valley may be amplified by the bath.

For the sufficiency side of a general physical theorem, use an explicit lower bound on the canonical valley cost relative to \(N^2/c_B\), plus uniform local limit and bath-curvature assumptions. For necessity, local peak matching under a bath with one sign of curvature may already suffice. A real short-range system in three dimensions with \(c_B\gg N^{3/2}\) should also pass the interfacial-barrier condition; this expectation still requires a proof, rather than replacing the missing tail estimate.

## Independent verification and next decisions

The independent subagent `check_bath_threshold` completed the Gaussian square completion and checked the iff threshold and the finite-error crossover. It also independently identified the caveat that phase-balanced temperature need not minimize total variation when the error is large. The derivations above incorporate that caveat. Numerical values for the single-phase TV example were checked with SciPy's normal CDF.

Before advancing this as a new research result:

1. Obtain and inspect the 1988 and 1990 Gaussian-ensemble papers, especially their scaling equations and histogram comparisons. The nearest prior art is not a peripheral citation.
2. Prove a smooth-bath extension with explicit phase-window and valley assumptions. An exact constant-heat-capacity bath is a useful first benchmark.
3. Validate the three distinct accuracy targets on a first-order short-range model, preferably using a published density of states or a reproducible exact/controlled calculation.
4. Compare against KL divergence, relative entropy per particle, and experimentally meaningful fluctuation events. Avoid implying that a failure in total variation refutes equivalence for local observables.

Useful negative finding: a claim that *finite baths generate quadratic corrections* or that *finite baths alter first-order transition histograms* would duplicate established work. The sharp information-level resource requirement is the only plausible novelty identified here, and its prior-art status remains unresolved.

## Independently suggested refinement: an exact optimized-error crossover

The independent reviewer derived a further result, which the scouting agent then checked by separating the two phase neighborhoods. For \(\kappa_Nm_Ns_N\to a<\infty\),

\[
 \boxed{\lim_{N\to\infty}\inf_t d_{\rm TV}(p_N,q_{N,t})
 =\min\{2\Phi(a/2)-1,\tfrac12\}.}
\]

To justify the lower bound, take any subsequence of candidate tilts. If both transformed phase weights have nonzero limiting mass, their exact logistic formula implies \(b_N=O(1/r_N)\). The limiting component shifts are then \(\mp a\). At fixed shifted component shapes, the total variation is a convex function of the limiting upper-phase weight, and reflection makes that function symmetric about one half. Its minimum is therefore the phase-balanced error \(2\Phi(a/2)-1\). If a transformed phase weight vanishes, the surviving component has unit limiting variance and cannot cover both target phase neighborhoods, so the limiting error is at least one half. Subsequences with component means escaping both neighborhoods have larger errors.

The balanced bound is attained by \(t=0\). For \(a>0\), the other bound is attained by \(t_N=\kappa_Nm_N\): the transformed upper component remains exactly centered at \(m_N\), its variance ratio tends to one, and its weight tends to one. For \(a=0\), the balanced bound already gives zero. This proves the displayed formula.

The preferred TV approximation changes at

\[
 a_*=2\Phi^{-1}(3/4)\simeq1.34898.
\]

Beyond this value, fitting in total variation can favor reproducing one phase accurately and discarding the other. The scalar best-fit error should therefore be reported together with the individual phase weights. This is a property of the chosen approximation objective, not successful recovery of coexistence.

## A smooth-bath sufficiency lemma for the exact Gaussian reference

The tail problem is simpler when the canonical reference is *exactly* the Gaussian mixture. Let the residual bath log-weight be \(g_N(E)\), globally concave on its energy domain, and set

\[
 t_N=-\frac{g_N(m_N)-g_N(-m_N)}{2m_N},\qquad
 h_N(E)=g_N(E)+t_NE.
\]

Then \(h_N(m_N)=h_N(-m_N)\). Suppose that for every fixed \(R\), the phase neighborhoods lie in the domain eventually, and

\[
 s_Nm_N\sup_{|E|\le m_N+Rs_N}|g_N''(E)|\longrightarrow0.
\]

The secant construction and the curvature bound imply
\(s_Nh_N'(\pm m_N)\to0\), and the log-weight varies by \(o(1)\) throughout either fixed standardized phase window. Global concavity supplies the tangent bound

\[
 h_N(\pm m_N+s_Nz)-h_N(\pm m_N)
 \le s_Nh_N'(\pm m_N)z.
\]

Under a standard normal \(Z\), the expectation of the right-hand exponential tends to one. Together with local convergence and nonnegativity, this proves convergence of each reweighted component's normalization to the same endpoint factor, and its normalized density to the original component in L1. Hence total variation of the full mixture tends to zero.

For a regular bath with uniformly bounded curvature proportional to \(1/c_B\), this proves sufficiency of \(c_B\gg N^{3/2}\) beyond an exactly quadratic reservoir, while retaining the exact Gaussian subsystem model. It does **not** remove the need for a separate valley argument for real short-range coexistence distributions. The reviewer also proposed necessity under a matching positive lower curvature bound; the local slope argument is persuasive, but a formal statement for arbitrary concave domains remains to be written before treating that generalized iff theorem as established.

Reproducible numerical check: run `python research/verify-ensemble-scaling.py`. It integrates the exact mixture densities at increasing phase separation, verifies the balanced crossover, and checks the one-phase limiting approximation. At \(a=1\), the balanced error at \(m/s=1000\) is 0.382661, approaching 0.382925. At \(a=1.5\), it is 0.546238, while the phase-abandoning error is 0.5. These are deterministic checks of the analytic model, not evidence for any particular molecular fluid.
