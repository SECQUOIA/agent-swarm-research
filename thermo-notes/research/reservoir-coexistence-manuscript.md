# Thermal reservoir size and phase correlations at coexistence

Superseded internal draft. Use [the complete LaTeX manuscript and reproduction bundle](../paper-finite-reservoirs/README.md). Manuscript development resolved isolated short-range sufficiency, removed the unnecessary kinetic-sector requirement for the mean-field exponent, and completed physical and multivariate optimization results. Historical priority remains a separate bounded literature assessment; earlier unresolved-status wording below records the previous draft.

*Internal manuscript candidate, 6 September 2026; extended 7 September 2026. The results below have independent mathematical and numerical reviews. Priority remains provisional: the cited literature search did not locate these sharp coexistence thresholds, but it does not establish that they are previously unknown.*

## Abstract

A finite thermal reservoir can reproduce each subsystem's canonical distribution while imposing strong correlations between their phases. We study complete probability laws for a physical constant-heat-capacity bath, allowing its total energy to be calibrated optimally. If energy rescaled by \(b_N\) has a weak limit with at least three support points, canonical convergence in total variation holds if and only if the bath exponent satisfies \(c_N\gg b_N^2\); no density or moment assumptions are needed. Two macroscopic energy phases are exceptional: a separation of order \(N\) and fluctuations of order \(\sqrt N\) give the smaller \(N^{3/2}\) threshold under explicit tail control. A mean-field Potts model realizes this iff statement. For two independent short-range Potts systems, joint canonical accuracy requires \(c_N\gg N^2\). Yet in \(N\ll c_N\ll N^2\), a centered shared bath selects opposite phases. With balanced target phase weights, both complete marginals become canonical while joint total-variation error tends to \(1/2\) and microscopic mutual information to \(\log2\). These results refine established finite-bath and phase-correlation theory; isolated short-range sufficiency and priority remain unresolved.

## 1. Scientific question and exact reservoir model

An ideal thermal reservoir imposes a temperature without changing it when a subsystem exchanges energy. A finite reservoir cannot do this exactly. Near coexistence, the distinction matters on two separate scales: the energy difference between phases is extensive, while fluctuations within each phase typically have width proportional to \(\sqrt N\). How large must a physical reservoir be to preserve both the probabilities of the phases and their fluctuation laws?

We formulate preservation in total variation,

\[
\|P-Q\|_{\mathrm{TV}}=\sup_A|P(A)-Q(A)|
=\frac12\int\left|\frac{dP}{d\mu}-\frac{dQ}{d\mu}\right|\,d\mu,
\tag{1}
\]

where \(\mu\) is any common dominating measure, for example \(P+Q\). This criterion applies equally to discrete and continuous energies and bounds the discrepancy in the probability of every measurable event. It is stronger than agreement of a free energy per particle, an equilibrium macrostate set, or selected local observables. The target inverse temperature \(\beta=1/(k_BT)>0\), subsystem Hamiltonian, and all other fields are fixed. The adjustable quantity is the total energy of the isolated subsystem–reservoir composite. We neglect interaction energy in the equilibrium measure and make no dynamical assertion.

Let the bath have surface density of states

\[
\omega_{B,N}(U)=D_N U^{c_N}\mathbf1_{U>0},\qquad c_N>0.
\tag{2}
\]

Its surface entropy is \(S_{B,\omega}=k_B\log\omega_B\), its inverse temperature is \(c_N/U\), and its associated heat capacity is

\[
C_{B,\omega}=k_Bc_N.
\tag{3}
\]

These conventions matter for a finite bath. For \(f_N\) independent classical quadratic bath degrees of freedom, \(c_N=f_N/2-1\). The canonical heat capacity of that same quadratic Hamiltonian is \(k_Bf_N/2=k_B(c_N+1)\). The finite offset does not change the asymptotic exponents below, but the two capacities should not be identified exactly.

If \(P_N\) is the canonical subsystem law, the exact marginal of an energy-conserving composite at total energy \(\mathcal E_N\) has likelihood ratio

\[
\frac{dQ_N}{dP_N}=\frac{e^{h_N(E)}}{Z_N},\qquad
h_N(E)=\beta E+c_N\log(\mathcal E_N-E),
\tag{4}
\]

with \(h_N=-\infty\) for \(E\ge\mathcal E_N\). Here \(Z_N=\mathbb E_{P_N}e^{h_N(E)}\). The factor \(e^{\beta E}\) removes the canonical Boltzmann weight before the bath density is inserted. The residual log-weight is strictly concave:

\[
h_N'(E)=\beta-\frac{c_N}{\mathcal E_N-E},\qquad
-h_N''(E)=\frac{c_N}{(\mathcal E_N-E)^2}.
\tag{5}
\]

The likelihood ratio of the complete subsystem state laws depends on energy alone. Integrating its absolute difference from one over the canonical state law proves that full-state TV equals energy-law TV exactly. Thus controlling (1) does not discard configuration or momentum events in this model.

Power-law finite-bath marginals are established statistical mechanics; see [Campisi's constant-capacity discussion](https://arxiv.org/abs/cond-mat/0611068). Our question concerns their size-dependent accuracy at coexistence.

## 2. Phase assumptions and a local necessity lemma

For the local lemma and Theorem 1, suppose the canonical energy density \(p_N\) has finitely many phase centers \(E_{i,N}\), separated by order \(N\). At every fixed bounded interval of standardized energy \(z\), assume

\[
\sqrt N\,p_N(E_{i,N}+\sqrt N z)
\longrightarrow w_i\phi_{v_i}(z)
\quad\text{in }L^1,
\tag{6}
\]

where \(\phi_v\) is the centered normal density of variance \(v\), all \(w_i,v_i>0\), and \(\sum_iw_i=1\). The variances may differ. These local limits imply concentration in the union of phase windows when their standardized width tends to infinity after \(N\). They do not impose a Gaussian shape on the intervening valley.

A useful consequence of full-law preservation is

\[
h_N(E_{i,N})-\log Z_N\longrightarrow0,
\qquad
\sqrt N\,h_N'(E_{i,N})\longrightarrow0.
\tag{7}
\]

To justify this without assuming pointwise likelihood convergence, TV convergence first implies \(e^{h_N}/Z_N\to1\) in canonical probability. Equation (6), whose limiting density is positive on bounded intervals, transfers this to convergence in Lebesgue measure of
\(f_{i,N}(z)=h_N(E_{i,N}+\sqrt N z)-\log Z_N\) toward zero. Any bath cutoff within a fixed phase window would remove a positive limiting canonical mass, so these functions eventually have the required interior domain.

Concavity upgrades convergence in measure to the center and derivative statements. Choose two points to the left of zero and two to the right, in four disjoint fixed intervals, where \(f_{i,N}\to0\). Secant slopes on the left and right bound \(f'_{i,N}(0)\) from above and below, respectively. Both slopes tend to zero. A chord through one point on each side bounds \(f_{i,N}(0)\) below, while a tangent and a left secant bound it above. This proves (7). The argument is useful because it covers arbitrary total-energy tuning, including attempts to move the bath cutoff or favor one phase.

For two centers with \(\Delta_N=E_{+,N}-E_{-,N}\sim\ell N\), (7) implies

\[
\beta_{B,\pm}:=\frac{c_N}{\mathcal E_N-E_{\pm,N}}
=\beta+o(N^{-1/2}).
\]

Taking reciprocal differences gives

\[
\frac{\Delta_N}{c_N}
=\frac1{\beta_{B,-}}-\frac1{\beta_{B,+}}
=o(N^{-1/2}),
\tag{8}
\]

and hence \(c_N/N^{3/2}\to\infty\). No interphase probability bound is needed for this necessary condition.

## 3. Two energy phases: the sharp \(N^{3/2}\) scale

Local phase limits alone cannot establish sufficiency: a finite bath may amplify a small canonical valley probability. We therefore state the missing control explicitly. For \(E\) between the two centers let

\[
x_N(E)=\min\{E-E_{-,N},E_{+,N}-E\}.
\]

In fixed energy units, assume constants \(A,c_0>0\) and \(1/2\le\alpha\le1\), independent of \(N\), such that

\[
p_N(E)\le\frac A{\sqrt N}
\exp\!\left[-c_0\min\left\{\frac{x_N(E)^2}{N},x_N(E)^\alpha\right\}\right].
\tag{9}
\]

A droplet-motivated exponent in dimension \(d\ge2\) is \(\alpha=(d-1)/d\). Equation (9) permits Gaussian fluctuation costs near a phase and a weaker surface-order cost deeper in the valley. It is a hypothesis requiring verification for a proposed short-range fluid or lattice model, not a universal interface theorem.

**Theorem 1.** With exactly two energy phases in (6), under (9) and \(\Delta_N/N\to\ell>0\), there exists a sequence \(\mathcal E_N\) for which \(\|P_N-Q_N\|_{\rm TV}\to0\) if and only if

\[
\boxed{c_N/N^{3/2}\longrightarrow\infty.}
\tag{10}
\]

Necessity follows from (8). For sufficiency, balance the residual weight at the two phase centers exactly:

\[
\mathcal E_N=E_{-,N}
+\frac{\Delta_N}{1-\exp[-\beta\Delta_N/c_N]}.
\tag{11}
\]

Subtract the common endpoint value from \(h_N\), which leaves (4) unchanged. Its curvature on the coexistence interval and every fixed phase window is then \(\beta^2c_N^{-1}[1+o(1)]\). Twice integrating the curvature bound gives, inside the interval,

\[
0\le h_N(E)\le
\frac C{c_N}(E-E_{-,N})(E_{+,N}-E)
\le\frac{CNx_N(E)}{c_N}.
\tag{12}
\]

It also gives \(h_N\to0\) uniformly on each fixed standardized phase window. Outside the endpoint interval, concavity gives \(h_N\le0\), so exterior canonical tails cannot be amplified.

For the interior tail \(x\ge R\sqrt N\), compare the gain in (12) separately with the two costs in (9):

\[
\frac{CNx/c_N}{x^2/N}\le\frac{CN^{3/2}}{Rc_N},
\qquad
\frac{CNx/c_N}{x^\alpha}
\le\frac{CN^{2-\alpha}}{c_N}.
\tag{13}
\]

Both vanish under (10), since \(\alpha\ge1/2\). The reweighted tail is consequently bounded by (9) with a smaller positive exponent. Its Gaussian part becomes small as \(R\to\infty\); its stretched-exponential part tends to zero as \(N\to\infty\). One may separate these terms using \(e^{-\min(a,b)}\le e^{-a}+e^{-b}\). Combining the local windows, interior valley, and exterior tails yields
\(\int p_N|e^{h_N}-1|\to0\). Normalization proves the theorem.

The exponent comes from the residual bath slope across a phase window: it has size \(N/c_N\), and acts over a width \(\sqrt N\). Balancing the endpoint weights removes their extensive relative offset, but cannot remove both local slopes. This explains why simply using the full coexistence energy range in a uniform quadratic remainder bound is conservative for two phases.

There is also a quantitative boundary limit. If \(c_N/N^{3/2}\to\gamma\in(0,\infty)\), with the calibration (11), write

\[
b=\frac{\beta^2\ell}{2\gamma},\quad b_-=b,\quad b_+=-b.
\]

For \(\alpha>1/2\), or for the stronger Gaussian valley bound proved below, the limiting weighted phase densities are

\[
q_i^{(\gamma)}(z)=
\frac{w_i\phi_{v_i}(z)e^{b_i z}}{Z_\gamma},\qquad
Z_\gamma=\sum_{i\in\{-,+\}}w_i e^{b^2v_i/2}.
\tag{14}
\]

The TV limit is \(\tfrac12\sum_i\int|w_i\phi_{v_i}-q_i^{(\gamma)}|\). Each conditional mean shifts by \(b_iv_i\), and its phase weight is multiplied by \(e^{b^2v_i/2}/Z_\gamma\). Equal endpoint likelihoods therefore need not preserve integrated phase weights when variances differ. Equation (14) describes this calibration, not an optimization of finite nonzero error over all total energies. For \(d=2\), the boundary-scale reservoir gain can compete with a surface-order valley cost, so (14) does not follow from (9) alone at \(\alpha=1/2\).

## 4. Three macroscopic support points: the sharp \(N^2\) scale

The three-phase obstruction needs much less than a local Gaussian limit. Suppose that for some centers \(a_N\), the scaled energy \((E_N-a_N)/N\) converges weakly to a probability law whose support contains at least three distinct points. No density, moment, or interphase-tail assumption is needed.

**Theorem 2.** There exists a total-energy sequence preserving the canonical state law in TV if and only if

\[
\boxed{c_N/N^2\longrightarrow\infty.}
\tag{15}
\]

For necessity, choose three separated bounded intervals with positive limiting probability. TV convergence supplies an energy \(e_{i,N}\) in each interval at which the normalized log likelihood tends to zero. These energies lie below the bath cutoff. Set \(\Delta_N=e_{3,N}-e_{1,N}=\Theta(N)\), \(\theta_N=(e_{2,N}-e_{1,N})/\Delta_N\), and \(q_N=\log[(\mathcal E_N-e_{1,N})/(\mathcal E_N-e_{3,N})]>0\). The interval choices keep \(\theta_N\) bounded away from zero and one.

Equality of endpoint log likelihoods gives \(c_Nq_N=\beta\Delta_N+o(1)\). The exact middle-point chord gap is

\[
c_N\left\{\log[(1-\theta_N)e^{q_N}+\theta_N]
-(1-\theta_N)q_N\right\}\longrightarrow0.
\tag{16}
\]

Uniformly for these \(\theta_N\), the bracket is at least \(C\min(q_N^2,q_N)\). Its second derivative has a positive lower bound on \(0\le q\le1\); convexity extends the bound linearly for \(q\ge1\). Since \(c_Nq_N=\Theta(N)\to\infty\), the vanishing gap first forces \(q_N\to0\), then \(c_Nq_N^2\to0\). The endpoint identity therefore gives \(N^2/c_N\to0\).

For sufficiency choose \(\mathcal E_N=a_N+c_N/\beta\) and subtract the residual log-weight at \(a_N\). The relative weight is globally between zero and one, since \(\log(1-y)\le-y\). Tightness of \((E_N-a_N)/N\) and \(c_N\gg N^2\) make its log-weight tend to zero in probability. Bounded convergence and normalization prove full-state TV convergence. The [general proof and independent reviews](reservoir-support-classification.md) apply equally to any diverging energy scale \(b_N\), with threshold \(c_N\gg b_N^2\).

Three distinct macroscopic energy phases with positive weights are a special case. Their within-phase widths need not be Gaussian or even known. Conversely, an exactly two-atom energy law can be matched for every \(c_N>0\) by balancing the two atom weights, so the support assumption is essential. The intermediate two-phase threshold arises only when within-phase fluctuations must also be preserved.

Distinct energies remain essential: several order-parameter phases at one energy count as one thermal support point. Additional adjustable chemical fields or interaction parameters define a different control problem. These statements describe probabilities of finite-system phase states, not simultaneous spatial phase fractions or the number of phases allowed by the Gibbs phase rule.

## 5. A microscopic realization and direct probability calculation

Consider \(N\) three-state mean-field Potts spins, with occupation numbers \(n_1+n_2+n_3=N\), multiplicity \(M(n)=N!/\prod_jn_j!\), and potential energy

\[
U_N(n)=-\frac J{2N}\sum_{j=1}^3n_j^2,\qquad J>0.
\tag{17}
\]

Add \(2aN\) independent quadratic subsystem kinetic degrees of freedom, where \(a>0\) is fixed and \(2aN\) is integral along the size sequence. Canonically, \(K\sim\operatorname{Gamma}(A,\mathrm{rate}\ \beta)\), with \(A=aN\), independently of the spins. This kinetic shape is a subsystem parameter and is distinct from the bath exponent \(c_N\).

At \(\beta J=b_0=4\log2\), the established coexistence states have spin-density vectors \((1/3,1/3,1/3)\) and the three permutations of \((2/3,1/6,1/6)\). The ordered colors share an energy, so the total energy \(E=U_N+K\) has two phase centers. The phase classification and conditional occupation fluctuations are established in [Costeniuc, Ellis and Touchette](https://arxiv.org/abs/cond-mat/0410744) and [Gandolfo, Ruiz and Wouts](https://arxiv.org/abs/0811.2735).

Their Laplace weights and energy fluctuations give

\[
\begin{gathered}
e_-=-J/4+a/\beta,\qquad e_+=-J/6+a/\beta,\qquad\ell=J/12,\\
r=\sqrt{\frac{2(3-b_0)}{6-b_0}},\qquad
w_-=\frac{3r}{1+3r},\qquad w_+=\frac1{1+3r},\\
v_-=\frac a{\beta^2}+\frac{J^2}{6(3-b_0)},\qquad
v_+=\frac a{\beta^2}.
\end{gathered}
\tag{18}
\]

At the disordered minimum, the tangent derivative of the potential energy density vanishes; its potential energy fluctuations alone are only \(O(1)\). The kinetic sector supplies a positive extensive variance in both phases and a continuous density. These phase ingredients are established fluctuation theory rather than proposed new results.

The hypotheses of Theorem 1 can be proved for this microscopic measure. Its spin rate potential on the compact simplex is

\[
I(p)=\sum_jp_j\log p_j-\frac{\beta J}{2}\sum_jp_j^2.
\]

The four global minima \(\mathcal M\) are interior and nondegenerate. Compactness and positive local Hessians imply \(I-I_{\min}\ge c\,\mathrm{dist}(p,\mathcal M)^2\). Stirling bounds give the global occupation estimate

\[
P_N(n)\le\frac C N
 e^{-cN\mathrm{dist}(n/N,\mathcal M)^2}.
\tag{19}
\]

Near the simplex boundary a fixed positive rate gap absorbs the missing Stirling prefactor, so (19) remains uniform there. On any fixed compact total-energy-density interval, the Gamma density satisfies

\[
f_K(K)\le\frac C{\sqrt N}
 e^{-c(K-aN/\beta)^2/N}.
\tag{20}
\]

One obtains this from its \(O(N^{-1/2})\) maximum and log curvature \(-(aN-1)/K^2\le-c/N\) over the available kinetic-energy interval; the mode differs from the mean by only \(1/\beta\). This also handles arbitrarily small positive kinetic energies.

The potential energy density is Lipschitz on the simplex. Multiplying (19) and (20) and summing the two-dimensional occupation lattice therefore gives, on the coexistence interval,

\[
p_N(E)\le\frac C{\sqrt N}
\sum_{i\in\{-,+\}}
 e^{-c(E-Ne_i)^2/N}.
\tag{21}
\]

The lattice Gaussian sum is \(O(N)\), canceling the occupation prefactor. Conditional occupation CLTs convolved with the uniform Gamma density local limit give (6), with (18). Thus (21) verifies a stronger tail bound than (9), and Theorem 1 proves the microscopic iff condition (10). This is a mean-field realization with an extensive valley cost; it does not establish a short-range droplet bound.

Finite-size probabilities can also be evaluated without sampling or energy binning. Canonical occupations have weights \(M(n)e^{-\beta U_N(n)}\). Integrating kinetic energy against the bath gives

\[
Q_N(n)\propto M(n)[\mathcal E_N-U_N(n)]_+^{A+c_N},
\qquad
\frac K{\mathcal E_N-U_N(n)}\mid n
\sim\operatorname{Beta}(A,c_N+1).
\tag{22}
\]

The power is \(A+c_N\), as follows directly from integrating \(K^{A-1}(\mathcal E_N-U_N-K)^{c_N}\). The canonical conditional kinetic law is Gamma. Since the log likelihood (4) is strictly concave, the event where \(q_N>p_N\) is an interval \((E_L,E_R)\), intersected with support. Hence

\[
\|P_N-Q_N\|_{\rm TV}
=Q_N(E_L<E<E_R)-P_N(E_L<E<E_R),
\tag{23}
\]

computed from finite sums of Beta and Gamma CDF differences and two scalar likelihood crossings.

For \(J=1,a=1/2\), using (11) at \(Ne_-\) and \(Ne_+\), representative calculations are:

| \(N\) | \(c_N=0.5N^{3/2}\) | \(c_N=2N^{3/2}\) | \(c_N=N^{7/4}\) | \(c_N=N^{5/4}\) |
|---:|---:|---:|---:|---:|
| 300 | 0.09790 | 0.02945 | 0.01472 | 0.16856 |
| 3000 | 0.13684 | 0.03605 | 0.00991 | 0.44885 |
| 6000 | 0.14454 | 0.03698 | 0.00850 | 0.60743 |
| 12000 | 0.14834 | 0.03730 | — | — |

Equation (14) predicts limiting errors of 0.15739 and 0.037986 for the first two columns. These finite-size data use a specified calibration; they do not numerically optimize over total energy. Enumeration of all \(3^N\) spin states for \(N=1,\ldots,8\) verifies the occupation reduction, and independent density quadrature at \(N=12\) agrees with (23) to about \(10^{-11}\). Large-size calculations use floating-point special functions, with a bound on possible reweighted mass from underflowed classes; they are not interval-arithmetic certificates. The [implementation](verification/potts_finite_bath.py), [independent checker](verification/check_potts_finite_bath.py), and [standalone figure](verification/potts-bath-scaling.pdf) preserve the computational record.

### A short-range necessity corollary

The necessary two-phase scale also applies to plain short-range spins. Consider the nearest-neighbor Potts Hamiltonian \(U=-\sum_{\langle x,y\rangle}\mathbf1_{\sigma_x=\sigma_y}\) on a periodic two-dimensional square, \(N=L^2\), at coexistence, with a fixed sufficiently large number \(q\) of colors. Then, for any sequence of composite total energies,

\[
\|P_N-Q_N\|_{\rm TV}\to0
\quad\Longrightarrow\quad c_N/N^{3/2}\to\infty.
\tag{24}
\]

This follows from the real-temperature partition expansion proved by [Borgs, Kotecký and Miracle-Solé](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Finite-Size-Scaling-for-Potts-Models.pdf), Theorem 1. Tilts of order \(1/N\) identify the two macroscopic energy weights; tilts of order \(1/\sqrt N\) identify one-sided Laplace transforms of energy-midpoint-conditioned spin fluctuations. Exponential tilting gives conditional weak Gaussian limits. Their variances are positive: conditioning on spins outside an independent set of at least \(N/5\) sites gives a uniform extensive energy-variance lower bound for \(q>4\). Strong convexity passes to the thermodynamic pressure and both stable phase branches. The uniform chord argument underlying (16), retaining unequal spacings, then gives the necessary product of phase gap and fluctuation width, \(N\sqrt N\). No kinetic sector or spin local limit theorem is needed.

The [source audit and derivation](short-range-potts-route.md) check the Hamiltonian, periodic geometry, uniform real-temperature interval, variance bound, and one-sided-transform argument; the latter also has [independent mathematical review](verification/phase-decomposition-review.md). A positive phase-decomposition lemma gives a route to sufficiency, but the required inward spin-energy exponential-moment bound has not been established here. Thus (24) is a necessity corollary, **not an isolated short-range iff theorem**.

### A shared bath can preserve both marginals while correlating the phases

Take two independent identical copies of a two-phase system, each of size \(N\), with phase centers \(E_{-,N},E_{+,N}\), positive weights \(w_-,w_+\), and tight conditional fluctuations of order \(\sqrt N\). Their canonical joint law is \(P_N\otimes P_N\). Center the physical bath at the mixed-phase total energy \(E_{m,N}=E_{-,N}+E_{+,N}\), choosing \(\mathcal E_N=E_{m,N}+c_N/\beta\). Its relative weight is

\[
W_N(E)=e^{\beta(E-E_{m,N})}
\left(1-\frac{\beta(E-E_{m,N})}{c_N}\right)^{c_N}_+\le1.
\]

If \(N\ll c_N\ll N^2\), this weight tends to one on opposite-phase pairs and to zero on same-phase pairs. The first assertion uses total fluctuations of order \(\sqrt N\), the second an energy offset of order \(N\). Bounded convergence therefore gives full-state TV convergence of the bath-coupled law to the canonical product conditioned on opposite phases. No valley-envelope estimate is needed. Consequently

\[
\begin{aligned}
\|Q_N-P_N\otimes P_N\|_{\rm TV}&\to w_-^2+w_+^2,\\
\|Q_N^{(i)}-P_N\|_{\rm TV}&\to |w_--1/2|,\\
I_{Q_N}(X_1;X_2)&\to\log2.
\end{aligned}
\]

The entropy conclusion requires its own proof. With \(h=\log W\le0\), the bounded quantity \(W|\log W|\) tends to zero on every phase pair. Thus joint relative entropy against the canonical product tends to \(-\log(2w_-w_+)\). Marginal likelihood ratios are uniformly bounded; their TV limits therefore also give their relative-entropy limits. The chain rule yields the displayed full microscopic mutual information, not just phase-label information.

At balanced phase weights, each complete subsystem marginal becomes canonical while the joint error remains \(1/2\). The limiting phase table is

| Phase pair | Canonical product | Shared-bath limit |
|---|---:|---:|
| \((-,-)\) | 1/4 | 0 |
| \((-,+)\) | 1/4 | 1/2 |
| \((+,-)\) | 1/4 | 1/2 |
| \((+,+)\) | 1/4 | 0 |

The companion system supplies a latent-energy buffer; it is not another constant-capacity bath. This does not contradict the isolated-system threshold. In a sufficiently-large-q short-range Potts model, balanced weights follow from a specified finite-size target temperature \(\beta_N=\beta_c-\log q/(N\ell)+o(N^{-1})\), with \(\ell\) the latent energy per spin. Bounded spin energies and the partition expansion justify the tuning and preserve the conditional fluctuation limits.

The two-copy canonical total-energy law has three distinct macroscopic support points, with weights \(w_-^2,2w_-w_+,w_+^2\). Theorem 2 therefore gives a full microscopic **joint-law iff threshold** \(c_N\gg N^2\) for the pair of plain short-range Potts systems, without solving the isolated-copy sufficiency problem. The [shared-bath note](shared-bath-phase-correlations.md) and [independent review](verification/shared-bath-review.md) give the proofs, fixed-copy-number extension, and exact-power-law numerical benchmark.

At the lower boundary \(c_N/N\to\gamma>0\), the same centered calibration still selects opposite phases but also correlates their energy fluctuations. Under positive conditional weak Gaussian limits with variances \(v_-,v_+\), set \(a=\beta^2/\gamma\). The limiting full microscopic mutual information is

\[
\log2+\frac12\log\frac{(1+av_-)(1+av_+)}{1+a(v_-+v_+)}.
\]

Each phase-conditional marginal variance becomes \(v_i(1+av_j)/(1+a(v_-+v_+))\), leaving strictly positive full-marginal TV error at balanced phase weights. Section 11 of the shared-bath note gives the exact error, cutoff treatment, and separate relative-entropy proof. These independently reviewed statements concern the specified centered calibration and do not assert an arbitrary-calibration necessity theorem at the linear scale.

## 6. Relation to established results and remaining scope

Quadratic finite-reservoir weights, altered coexistence histograms, and Gaussian approximations to phase peaks are old. [Challa and Hetherington's 1988 Gaussian-ensemble paper](https://doi.org/10.1103/PhysRevA.38.6324) constructs a reservoir entropy quadratic in energy and studies finite-bath effects at transitions. [Challa, Landau and Binder's 1986 analysis](https://doi.org/10.1103/PhysRevB.34.1841) explicitly distinguishes Gaussian valley suppression from interfacial suppression. These precedents motivate both the local scales and the separate tail hypothesis here. Generalized-ensemble supporting-parabola theory also treats equilibrium equivalence, including the mean-field Potts model; see [Costeniuc and colleagues](https://arxiv.org/abs/cond-mat/0408681) and [the Potts application](https://arxiv.org/abs/cond-mat/0605213).

A square-energy-range sufficient bound already exists in a strong metric. [Riera, Gogolin and Eisert](https://arxiv.org/abs/1102.2389), Appendix B, bound a reduced microcanonical/Gibbs trace distance by a term of the form

\[
\frac12\left\{\exp\!\left[\frac{2\|H_S\|_\infty^2}{\eta^2m}\right]-1\right\}+C,
\tag{25}
\]

for their finite-dimensional subsystem and smoothed spin bath. Here \(m\) is bath size, \(\eta\) a bath energy scale, and \(C\) their density-of-states approximation error. Trace distance reduces to TV in the commuting case. For extensive subsystem energy range, the sufficient scale is \(m\gg N^2\). Theorem 2 does not introduce that sufficient scale; it makes the scale necessary for three thermal peaks despite arbitrary total-energy calibration. Theorem 1 identifies a two-phase setting where calibration and tail control reduce the requirement. Equation (25) does not directly cover the unbounded kinetic sector in our benchmark.

Sharp growing-block TV conditioning results also precede this work, including [Diaconis and Freedman](https://digicoll.lib.berkeley.edu/record/86140/files/91.pdf) and [Dembo and Zeitouni](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/sanovreffull.pdf). The present target is an interacting subsystem retaining a positive mixture of phase laws, rather than a homogeneous block approaching a single product tilt. First-order finite-reservoir Potts comparisons are likewise established in [Griffin, Matty and Swendsen](https://arxiv.org/abs/1608.05455). Their unweighted energy-level Euclidean distance can tend to zero on growing supports while TV remains positive, so their numerical criterion does not answer the present full-law question.

Opposite-phase locking of identical thermally coupled systems is itself established; [Ramírez-Hernández, Larralde and Leyvraz](https://arxiv.org/abs/0802.1748) explicitly exhibit it. Locally thermal states with global correlations and ensemble-dependent mutual information are also known. The [shared-bath audit](verification/shared-bath-prior-art.md) did not locate the more specific full-marginal TV result in the window \(N\ll c_N\ll N^2\), or the distinction among isolated and joint optimized bath scales. Those are the candidate refinements, rather than the existence of anticorrelation or thermal marginals in general.

The candidate contribution is therefore narrow: sharp, calibration-optimized physical-bath thresholds based on energy support and within-phase fluctuations, microscopic realizations, and a shared-bath regime with full marginal accuracy but persistent joint error. The literature examined did not supply those statements. Priority nevertheless remains uncertain, particularly in older finite-bath Potts studies, nonconvex conditioning work, and papers using different language for energy calibration. A closely related 1990 Challa–Landau–Binder review was not obtained in open full text. No claim of established novelty follows from this bounded search.

For molecular thermodynamics, the next substantive question is whether (9) can be established or tested with reliable finite-size control in a short-range coexistence model. The present results already separate complete canonical sampling from agreement of simpler observables. They do not provide molecular interfacial barriers, nucleation rates, or convergence times, and the mean-field benchmark should not be used to infer those quantities.

## Internal verification record

The underlying statements and proofs are retained in [the physical two-phase note](finite-bath-physical-extension.md), [the physical three-phase note](three-phase-physical-bath.md), and [the microscopic benchmark](potts-physical-bath.md). Independent reports cover [two-phase tail and concavity arguments](verification/physical-bath-review.md), [three-phase necessity and sufficiency](verification/three-phase-physical-review.md), [the microscopic hypotheses](verification/potts-microscopic-theorem-review.md), and [finite-bath formulas and numerical checks](verification/potts-bath-formula-review.md). The [expanded novelty audit](verification/physical-reservoir-novelty-audit.md) records the source comparisons and remaining gaps. This manuscript consolidates those reviewed results; it adds no independently asserted physical model assumptions beyond those stated above.

The final expanded manuscript also passed [a fresh-reader audit](verification/reservoir-manuscript-review.md). Independent reports verify [the weak-support theorem](verification/three-support-bath-review.md), [the short-range weak limits and positive phase variances](verification/phase-decomposition-review.md), and [the shared-bath limits including linear capacity](verification/shared-bath-review.md). The research pass closed on 2026-09-07 at the user’s request; unresolved extensions are limitations, not asserted results.
