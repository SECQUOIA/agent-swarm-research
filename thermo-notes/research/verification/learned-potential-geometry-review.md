# Independent review: potential uncertainty near phase coexistence

Reviewed 2026-09-06. This review checks the proposed result supplied by the parent agent; it does not edit the scouting manuscript.

**Verdict:** the limiting phase weights, conditional Gaussian shift, full-state total-variation formula, and second-order compensation equation are correct under the assumptions stated precisely below. The scale distinction is useful but should be presented as a synthesis of exponential tilting, local asymptotic normality, and first-order finite-size scaling. The compensation equation is the second-order coexistence condition. This review does not establish a publishable novelty claim.

## 1. Sufficient assumptions and exact calculation

Let a fixed finite number of measurable phase sets partition each sample space. Write their labels as \(I_N\in\{1,\ldots,k\}\), with

\[
P_N(I_N=i)=w_{i,N}\longrightarrow w_i>0,
\qquad \sum_iw_i=1.
\]

The phase sets may depend on system size, but they must be defined under the reference measure and kept fixed during the comparison. Suppose an extensive descriptor vector satisfies

\[
X_{i,N}=\frac{S_N-Nm_i}{\sqrt N}
\ \Rightarrow\ Z_i\sim\mathcal N(0,\Sigma_i)
\quad\text{under }P_N(\cdot\mid I_N=i).
\]

The covariance matrices may be positive semidefinite. Fix \(h,g\in\mathbb R^p\), let

\[
\delta\theta_N=h/\sqrt N+g/N,
\qquad h\cdot m_i=a\quad\text{for every }i,
\]

and define the **exact linear** perturbation

\[
\frac{dQ_N}{dP_N}
=\frac{\exp(-\beta\delta\theta_N\cdot S_N)}
{E_{P_N}\exp(-\beta\delta\theta_N\cdot S_N)}.
\]

An adequate integrability assumption is uniform integrability, in every phase, of

\[
\exp[-\beta(h+g/\sqrt N)\cdot X_{i,N}].                 \tag{1}
\]

A convenient stronger sufficient condition is a uniform conditional exponential-moment bound \(\sup_NE[e^{b\|X_{i,N}\|}\mid I_N=i]<\infty\), for some \(b>\beta\|h\|\). More economical moment assumptions can bound moment-generating functions in a neighborhood of the required tilt and its slightly enlarged multiples. Merely having finite moments for each \(N\), or an unspecified neighborhood of zero that does not contain the required tilt, is insufficient.

The exponent decomposes exactly as

\[
-\beta\delta\theta_N\cdot S_N
=-\beta a\sqrt N-\beta g\cdot m_i
-\beta h\cdot X_{i,N}-\frac{\beta}{\sqrt N}g\cdot X_{i,N}.
\]

The first term cancels from the normalized likelihood. The remaining unnormalized likelihood converges in distribution to

\[
Y_i=\exp[-\beta g\cdot m_i-\beta h\cdot Z_i].
\]

Condition (1) supplies the convergence of expectations needed to conclude

\[
\mathcal Z_N\longrightarrow\mathcal Z
=\sum_iw_i\exp\left[-\beta g\cdot m_i
+\frac{\beta^2}{2}h^\top\Sigma_i h\right]>0.             \tag{2}
\]

Consequently,

\[
Q_N(I_N=i)\longrightarrow
\widetilde w_i=
\frac{w_i\exp[-\beta g\cdot m_i+\beta^2h^\top\Sigma_i h/2]}
{\mathcal Z}.                                             \tag{3}
\]

Completing the square in the Gaussian moment-generating function gives

\[
\mathcal L_{Q_N}(X_{i,N}\mid I_N=i)
\Rightarrow\mathcal N(-\beta\Sigma_i h,\Sigma_i).           \tag{4}
\]

Equation (4) is **weak convergence**. A conditional central limit theorem does not imply convergence of these descriptor laws in total variation to a Gaussian. For example, lattice descriptor laws remain singular relative to the Gaussian at every finite size. This does not invalidate the next result.

## 2. Full-state total variation requires no density local limit

Because the Radon–Nikodym derivative is known exactly,

\[
\|Q_N-P_N\|_{\rm TV}
=\frac12 E_{P_N}\left|\frac{Y_N}{\mathcal Z_N}-1\right|.
\]

Joint weak convergence of phase label and standardized descriptor, together with (1), yields

\[
\boxed{\displaystyle
\|Q_N-P_N\|_{\rm TV}\longrightarrow
\frac12\sum_iw_i E\left|
\frac{e^{-\beta g\cdot m_i-\beta h\cdot Z_i}}{\mathcal Z}-1
\right|.}                                                 \tag{5}
\]

This follows by uniform integrability of the absolute likelihood difference. No microscopic density convergence, coupling of the sample spaces across \(N\), or Gaussian approximation in total variation is needed. Since the likelihood depends only on \(S_N\), the full-state TV also equals the TV between the two exact finite-\(N\) descriptor laws.

The theorem assumes that all relevant mass is covered by the finite partition and its conditional limits. If one instead defines only selected metastable basins and leaves a rare complement, negligible reference probability of that complement alone does not control its reweighted probability. A separate integrability or tail estimate is then necessary.

For numerical evaluation, put

\[
\sigma_i^2=\beta^2h^\top\Sigma_i h,
\qquad \mu_i=-\beta g\cdot m_i-\log\mathcal Z,
\qquad M_i=e^{\mu_i+\sigma_i^2/2}.
\]

For \(\sigma_i>0\), the contribution to (5), after summing away the zero global mean likelihood difference, can be written

\[
w_i\left[
\Phi(-\mu_i/\sigma_i)
-M_i\Phi(-\mu_i/\sigma_i-\sigma_i)
\right].                                                  \tag{6}
\]

For \(\sigma_i=0\), its contribution is \(w_i(1-e^{\mu_i})_+\). These terms sum to (5).

## 3. Phase compensation and its limitation

All original phase weights are preserved if and only if the multiplicative factors in (3) are the same. Equivalently,

\[
g\cdot(m_i-m_1)
=\frac\beta2h^\top(\Sigma_i-\Sigma_1)h,
\qquad i=2,\ldots,k.                                     \tag{7}
\]

The sign and factor of \(1/2\) in the candidate equation are correct. For two distinct means there is always an unrestricted \(g\) solving this one linear equation. The solution is nonunique when \(p>1\). If the allowed correction parameters occupy a proper subspace, solvability must instead be checked on that subspace.

For multiple phases, (7) has a solution precisely when its right-hand side lies in the range of the matrix with rows \((m_i-m_1)^\top\). Equivalently, for every affine dependence

\[
\sum_i c_i=0,\qquad \sum_i c_i m_i=0,
\]

one must have

\[
\sum_i c_i h^\top\Sigma_i h=0.                            \tag{8}
\]

A simple obstruction has \(p=2\), means \((0,0),(1,0),(2,0)\), tangent \(h=(0,1)\), and covariance matrices \(\operatorname{diag}(1,1),\operatorname{diag}(1,1),\operatorname{diag}(1,2)\). Equation (7) would require both \(g_x=0\) and \(2g_x=\beta/2\). All covariances are positive definite. This is a valid Gaussian-mixture example; it is not by itself a microscopic thermodynamic realization.

Even when (7) is solved, the limiting full-state distortion usually remains positive. In that case \(M_i=1\), and (5) reduces to

\[
\boxed{\displaystyle
\lim_N\|Q_N-P_N\|_{\rm TV}
=\sum_iw_i\left[2\Phi\left(\frac{\beta\sqrt{h^\top\Sigma_i h}}2\right)-1\right].}
                                                               \tag{9}
\]

Thus correcting phase weights does not correct fluctuations within a phase. Under the theorem's fixed-\(h,g\) assumptions, the limiting TV is zero exactly when \(h^\top\Sigma_i h=0\) for every phase and \(g\cdot m_i\) is phase independent. If one phase has a positive-definite covariance, the first condition forces \(h=0\).

An independent numerical check also confirms the parent's labelled Gaussian example. For \(\beta=1\), equal weights, means \((-1,0),(1,0)\), covariances \(\operatorname{diag}(1,1),\operatorname{diag}(1,4)\), and \(h=(0,1)\), setting \(g=0\) gives second-phase probability \(0.8175744761936438\) and TV \(0.640770522662276\). Setting \(g=(3/4,0)\) preserves both weights at every finite \(N\). Its exact TV is

\[
\Phi\left(\tfrac12\sqrt{1+9/(16N)}\right)
+\Phi\left(\tfrac12\sqrt{4+9/(16N)}\right)-1,
\]

which is \(0.5354524311475877\), \(0.5334714473700264\), and \(0.5328138595188823\) at \(N=25,100,10000\), respectively, and tends to \(0.532807207342556\). These values were recomputed directly from the closed normal-CDF expression. This example illustrates the limits of first-order phase response; it does not disprove a linear-response theorem whose hypotheses are not satisfied on the mixed scaling path.

## 4. What the two parameter scales mean

Let \(D=\operatorname{span}\{m_i-m_1\}\). Components of parameter error in \(D\) change relative bulk phase energies by order \(N\|\delta\theta\|\). Components in \(D^\perp\) have no first-order bulk phase splitting but usually change fluctuating energies by order \(\sqrt N\|\delta\theta\|\). This explains the \(N^{-1}\) versus \(N^{-1/2}\) scales in the theorem.

These are scales for **nontrivial finite distortion**, not sufficient bounds for TV convergence to zero. A generic nonzero \(g/N\) gives a nonzero phase-weight shift, and a generic tangent \(h/\sqrt N\) gives a nonzero Gaussian shift. Directions annihilated by all conditional covariance matrices can have different scales. The theorem also does not establish necessity for every possible sequence of larger perturbations: such a claim needs additional large-deviation or moderate-deviation control.

The result is pointwise in fixed \(h,g\). Uniform statements over an uncertainty set need appropriately uniform moment control. A distribution over uncertain potential parameters is an additional probabilistic layer; averaging separately normalized Gibbs laws is not the same as substituting an averaged parameter into (2)–(5).

Finally, the linear potential assumption matters. For a nonlinear parameterization,

\[
U_{\theta+\delta\theta}-U_\theta
=\delta\theta\cdot S_N
+\tfrac12\delta\theta^\top H_N\delta\theta+\cdots,
\]

an extensive Hessian \(H_N\) contributes an order-one phase-dependent term for \(\delta\theta=h/\sqrt N\). That term changes (3) and (7). A merely pointwise first-order linearization of a neural potential therefore does not justify the stated theorem.

## 5. Relation to coexistence curvature and prior work

For a linear potential, a smooth restricted phase free-energy density \(f_i(\theta)\) has

\[
\nabla f_i=m_i,\qquad \nabla^2 f_i=-\beta\Sigma_i.
\]

Along a path \(\theta(t)=\theta_0+t h+t^2g\), the coefficient of \(t\) in \(f_i-f_1\) is \(h\cdot(m_i-m_1)\), and the coefficient of \(t^2\) is

\[
g\cdot(m_i-m_1)-\frac\beta2h^\top(\Sigma_i-\Sigma_1)h.
\]

Therefore (7) is exactly the condition that the path preserve coexistence through second order. Calling it a new thermodynamic curvature law would be unjustified without a much stronger literature case. This interpretation assumes differentiable restricted phase free energies; it is explanatory and is not needed for the direct likelihood proof above.

The following openly accessible primary work bounds the novelty claim:

- Borgs and Kotecký, *A rigorous theory of finite-size scaling at first-order phase transitions* (1990), gives an explicit field crossover on the inverse-volume scale. The normal \(N^{-1}\) scale is established first-order finite-size physics. [Original article and abstract](https://doi.org/10.1007/BF01013955).
- Borgs and Janke, *New method to determine first-order transition points from finite-size data* (1992), analyzes the finite-volume partition function as a sum of exponential phase-free-energy contributions. The phase-weight softmax structure is established. [Original article and abstract](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.68.1738).
- Sturgeon and Laird, *Adjusting the melting point of a model system via Gibbs-Duhem integration: application to a model of Aluminum* (2000), already adjusts potential parameters to change the melting point while largely preserving fitted mechanical properties. This is older direct prior art for potential calibration through coexistence conditions. [Open primary preprint](https://arxiv.org/abs/cond-mat/0006390).
- Swinburne, Lapointe, and Marinica, *Score matching the descriptor density of states for model-agnostic free energy estimation*, published online December 2025, Nature Communications **17**, 248 (2026), develops differentiable phase free energies for linear descriptor potentials, including uncertainty propagation and adjustment of phase boundaries. Descriptor-based thermodynamic calibration itself is therefore occupied. [Open primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12783767/).
- Fuchs and Zavadlav, *Refining machine learning potentials through thermodynamic theory of phase transitions*, npj Computational Materials **12**, 216 (2026), refines potentials using differences between phase free energies at target coexistence conditions. [Published primary article](https://doi.org/10.1038/s41524-026-02195-7), [open author preprint](https://arxiv.org/abs/2512.03974).

The Gaussian shift and likelihood expectation argument are direct consequences of exponential tilting, closely related to Le Cam's third lemma and local asymptotic normality. Because several distinct phases retain positive mass, the aggregate limit generally is a phase-labelled mixture of Gaussian shift experiments, rather than one ordinary Gaussian shift experiment. That distinction may support a useful formulation, but not a claim that Gaussian tilting is new.

No exact match to the combined finite-phase, mixed-scale, full-state-TV statement was located in this bounded review. The clearest potentially useful contribution is an explicit error criterion separating phase probability errors from conditional fluctuation errors, with the affine compatibility condition made visible. Further novelty assessment should compare the full theorem against statistical limit-experiment theory and the recent descriptor-potential literature before developing a publication claim.
