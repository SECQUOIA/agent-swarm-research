# Independent review: shared-bath phase correlations

Reviewer: `capacity_review`. Date: 2026-09-07. Reviewed `research/shared-bath-phase-correlations.md`, including the root's proposed stronger three-point support theorem. This report independently re-derives the mathematical claims; it does not clear literature priority.

**Verdict:** the opposite-phase selection, full joint and marginal total-variation limits, and full-state mutual-information limit are correct. The entropy proof uses the necessary likelihood bounds rather than relying on total variation alone. The bath-temperature tuning has the stated sign, subject to the explicitly required phase partition asymptotics. The composite `N^2` iff theorem admits a substantial assumption reduction: three distinct points in the limiting scaled-energy support suffice. Gaussian phases, densities, and interphase-tail bounds are unnecessary for that theorem.

## 1. Opposite-phase selection

Let `P_N` have the actual disjoint phase events and conditional `sqrt N` tightness stated in the note. For the product law, set `M_N=E_-,N+E_+,N` and center the bath residual weight at this mixed-phase total energy. On its feasible domain,

\[
W_N=\exp\{c_N[x+\log(1-x)]\},
\qquad x=\beta(T-M_N)/c_N.
\]

The elementary inequality `log(1-x)<=-x` gives `0<=W_N<=1` globally after setting the weight to zero beyond the cutoff. This upper bound covers rare tails of arbitrary shape.

On mixed assignments, `T-M_N=O_P(sqrt N)`. If `N/c_N->0`, then `x->0` and `c_N x^2=O_P(N/c_N)->0`, so `W_N->1` in conditional probability. On equal-phase assignments, `T-M_N=±Delta_N+O_P(sqrt N)`, with `Delta_N~ell N`. In the range `N<<c_N<<N^2`, `x->0` but `c_N x^2~beta^2 ell^2 N^2/c_N->infinity`. Thus their weights tend to zero. The Taylor remainder relative to the quadratic term is `O_P(N/c_N)->0`, so it does not change this conclusion.

Therefore `W_N-1_{O_N}->0` in product-law probability and in L1 by boundedness. Its normalizer tends to `p_O=2w_-w_+>0`. Normalization gives the claimed TV convergence to the product law conditioned on opposite phases.

No local Gaussian limit, microscopic interface estimate, or exponential phase moment is required. A negligible additional phase-classification remainder would also be harmless because `W_N<=1`.

## 2. Full joint and marginal errors

The TV distance between a law and its conditioning on an event of probability `p` is exactly `1-p`. The joint error consequently tends to `w_-^2+w_+^2`.

Independence and identical phase weights give an exact marginal of the conditioned law equal to the half-and-half mixture of the two original conditional phase laws. Their supports are disjoint. Its TV distance from the canonical one-copy law is exactly `|w_-,N-1/2|`. Contraction under marginalization transfers that conclusion to the physical shared-bath law.

Thus balanced phase weights give correct complete one-copy marginals while the joint TV error tends to `1/2`. The comparison with an isolated subsystem's necessary `N^(3/2)` scale needs the positive nondegenerate `sqrt N` fluctuation assumptions of that earlier theorem. Tightness alone is insufficient for that comparison: two exactly atomic energy phases are tight and can be endpoint-balanced exactly without that capacity scale. The Potts-plus-kinetic examples have the required positive variance.

## 3. Mutual information: the additional control is valid

Writing `h_N=log W_N`, with `0 log0=0`, gives

\[
D(Q_N\|P_N^{\otimes2})
=Z_N^{-1}\mathbb E_{P_N^{\otimes2}}[W_N\log W_N]-\log Z_N.
\]

On every phase assignment, `W_N log W_N` tends to zero. Its absolute value is bounded by `1/e`, so its expectation tends to zero despite the changing underlying probability laws. Consequently

\[
D(Q_N\|P_N^{\otimes2})\to-\log(2w_-w_+).
\]

Marginal likelihood ratios are bounded by `1/Z_N`; the opposite-phase-conditioned target ratios are eventually bounded as well because both limiting phase weights are positive. L1 convergence of these ratios, plus uniform continuity of `r log r` on their common compact range, gives

\[
D(Q_N^{(i)}\|P_N)\to-\log2-\tfrac12\log(w_-w_+).
\]

Subtracting the two marginal divergences from the joint divergence yields `I_Q(X_1;X_2)->log2`. Every divergence is finite, so the chain rule applies directly. This is a valid full-state information result, not just a binary-label calculation or an unsupported consequence of TV convergence.

Because the binary-label mutual information also tends to `log2`, the chain rule and nonnegativity show that the additional dependence beyond the phase labels vanishes in mutual information. This supports the note's last sentence interpreting Equation (11).

## 4. Stronger theorem: three points of scaled-energy support

Here is a rigorous version of the root's generalization.

**Theorem.** Fix `beta>0`. Let `P_N` be canonical energy laws and let `b_N` be any deterministic centering sequence such that

\[
X_N=(E-b_N)/N\Rightarrow X,
\]

where `X` is a real probability law whose support contains at least three distinct points. Let the physical bath have density proportional to `U^{c_N}1_{U>0}`, with arbitrary `c_N>0`. Then

\[
\boxed{\exists\mathcal E_N:\operatorname{TV}(Q_{N,\mathcal E_N},P_N)\to0
\quad\Longleftrightarrow\quad c_N/N^2\to\infty.}
\]

The conclusion remains valid for `beta_N->beta>0`. No density, conditional CLT, or quantitative tail estimate is required.

### Sufficiency

Choose `mathcal E_N=b_N+c_N/beta`, and normalize the residual likelihood to one at `E=b_N`. It is again

\[
W_N(E)=\exp\{c_N[x+\log(1-x)]\}\le1,
\qquad x=\beta(E-b_N)/c_N.
\]

Weak convergence implies tightness of `X_N`. If `c_N>>N^2`, then `x->0` in probability and

\[
c_Nx^2=\beta^2(N^2/c_N)X_N^2\to0
\]

in probability. Thus `W_N->1` in probability. Its global bound upgrades this to L1 convergence; its normalizer tends to one, and TV convergence follows. In particular, rare unbounded-energy tails cannot be amplified.

### Necessity: selecting three good energies

Suppose arbitrary total energies give TV convergence. Let

\[
f_N(E)=\beta E+c_N\log(\mathcal E_N-E)-\log Z_N
\]

on the feasible domain. TV implies `exp(f_N)->1`, and hence `f_N->0`, in canonical probability.

Choose three bounded disjoint standardized-energy intervals around distinct support points of `X`, with gaps between intervals bounded below by positive constants. Choose their endpoints as continuity points; each interval has positive limiting probability. There are therefore energies `e_1,N<e_2,N<e_3,N` within their corresponding intervals such that `f_N(e_i,N)->0`. The selected points are feasible, because a zero likelihood cannot approximate one. Set

\[
d_N=e_{3,N}-e_{1,N}=\Theta(N),\qquad
\theta_N=(e_{2,N}-e_{1,N})/d_N.
\]

The fixed interval geometry gives `theta_N in [epsilon,1-epsilon]` for some positive epsilon.

Let

\[
q_N=\log\frac{\mathcal E_N-e_{1,N}}{\mathcal E_N-e_{3,N}}>0.
\]

Equality of the endpoint log likelihoods up to a vanishing error gives

\[
c_Nq_N=\beta d_N+o(1)=\Theta(N).
\]

Their middle concavity gap is exactly

\[
\begin{aligned}
g_N&=f_N(e_{2,N})-(1-\theta_N)f_N(e_{1,N})-\theta_Nf_N(e_{3,N})\\
&=c_N F_{\theta_N}(q_N),\\
F_\theta(q)&=\log[(1-\theta)e^q+\theta]-(1-\theta)q.
\end{aligned}
\]

The left side tends to zero. The common normalization and the linear term in energy cancel exactly.

### A uniform elementary lower bound

For `theta in [epsilon,1-epsilon]`, `F_theta(0)=F_theta'(0)=0`, and

\[
F_\theta''(q)=\frac{\theta(1-\theta)e^q}
{[(1-\theta)e^q+\theta]^2}.
\]

This has a uniform positive lower bound for `0<=q<=1`, giving `F_theta(q)>=Cq^2` on that interval. Convexity and `F_theta(0)=0` imply that `F_theta(q)/q` is nondecreasing for positive q. Thus `F_theta(q)>=F_theta(1)q>=Cq` for `q>=1`, with a common positive C. In total,

\[
F_\theta(q)\ge C\min(q^2,q).
\]

Consequently,

\[
g_N\ge Cc_N\min(q_N^2,q_N)
=C\min\{(c_Nq_N)^2/c_N,c_Nq_N\}
\ge C'\min\{N^2/c_N,N\}.
\]

Since `g_N->0` and `N->infinity`, necessarily `N^2/c_N->0`. This proves necessity for arbitrary positive bath exponents and arbitrary tuning, without presupposing that the bath is large or near the target temperature.

The proof also shows why three positive limiting energy regions matter. A third region whose probability vanishes does not supply a third good point in this argument. A two-point limiting support requires information on a finer fluctuation scale to infer the earlier `N^(3/2)` obstruction.

## 5. Consequence for the two-copy model

The two-copy canonical total energy, centered at `2E_-,N` and divided by N, converges to three atoms at `0,ell,2ell`, with positive weights `w_-^2,2w_-w_+,w_+^2`. Conditional `sqrt N` tightness already implies this convergence; even conditional concentration on an `o(N)` scale would suffice.

The generalized theorem therefore establishes the composite iff condition `c_N>>N^2` without the conditional Gaussian assumptions currently used in Section 6. The actual short-range composite obstruction needs only the source theorem's canonical macroscopic two-phase energy concentration for each copy. It does not require an inward phase-energy exponential moment or a spin energy CLT. This is a safe route around the isolated-copy sufficiency gap.

A claim about a particular microscopic Potts law must still use the correctly normalized, uniformly valid source partition theorem to establish that macroscopic concentration. This review verifies the deduction from that input rather than re-auditing its literature source. The full one-bit selection theorem additionally needs the stated internal fluctuation tightness in the chosen capacity range.

## 6. Balancing the reference weights

Under valid real-temperature phase partition asymptotics, shifting inverse temperature by `delta/N` multiplies the low/high phase ratio by `exp(delta ell)`. Thus the stated sign and coefficient

\[
\beta_N=\beta_c-\frac{\log(w_-/w_+)}{N\ell}+o(N^{-1})
\]

are correct. For ordered multiplicity q, the shift is `-log q/(N ell)`. The kinetic contribution multiplies both spin phase partition functions by the same factor, so it does not alter that ratio.

The change-of-temperature statement is not a consequence of mere conditional tightness for arbitrary unbounded-energy laws. It needs the phase partition asymptotics or suitable uniform exponential control. The note states that premise. The reference law, kinetic temperature, and physical bath must all use the adjusted `beta_N`; comparison to the original unbalanced `beta_c` law would give a different marginal error.

## 7. Fixed number of copies: requested extension

For a fixed integer m, center the bath at the total energy of exactly k high-energy copies, with `0<=k<=m`. The same proof selects the event that the high-phase count is k. Under identical canonical copies its probability tends to

\[
p_k=\binom mk w_+^k w_-^{m-k}.
\]

The selected phase assignments are uniform across the binomial number of possibilities. Each marginal has high-phase probability `r=k/m`. Bounded-likelihood entropy arguments give total correlation

\[
\boxed{D\left(Q_N\middle\|\bigotimes_{j=1}^m Q_N^{(j)}\right)
\to mH(r)-\log\binom mk,}
\]

where `H(r)=-r log r-(1-r)log(1-r)`, with the usual endpoint convention. Dependence on the original positive weights cancels. If `w_+=r` and `0<k<m`, all marginals approach their canonical laws and this limit equals `-log p_k`.

This checks the proposed fixed-m formula. A growing number of copies would change fluctuation, probability, and entropy estimates and is not covered by this proof.

## 8. Uniform chord bound and the two-scale obstruction

The root's further refinement also checks. The elementary bound can retain its full dependence on the middle-point fraction:

\[
F_\theta''(q)\ge e^{-1}\theta(1-\theta),\qquad 0\le q\le1.
\]

Integrating twice and using convexity beyond one yields, for every `0<theta<1` and `q>0`,

\[
\boxed{F_\theta(q)\ge\frac{\theta(1-\theta)}{2e}\min(q^2,q).}
\]

Suppose TV preservation supplies three good likelihood energies, of which two lie in one phase and have separation `Theta(b_N)`, while the third lies a distance `Theta(Delta_N)` away. Assume `b_N->infinity`, `b_N=o(Delta_N)`, and `Delta_N->infinity`. Then `theta_N(1-theta_N)=Theta(b_N/Delta_N)` and endpoint matching gives `c_Nq_N=Theta(Delta_N)`. The same exact chord gap therefore obeys

\[
0\leftarrow g_N\ge C\min\{\Delta_N b_N/c_N,b_N\},
\]

forcing

\[
\boxed{c_N\gg\Delta_N b_N.}
\]

Two separated positive-probability neighborhoods in a nondegenerate weak within-phase fluctuation limit at scale `b_N` provide the first two good points. A second positive-weight phase concentrated an extensive distance away provides the third. Thus Gaussian fluctuation laws and local densities are unnecessary even for this two-scale necessary condition. The original `N^(3/2)` obstruction is recovered from `Delta_N~ell N`, `b_N=sqrt N`.

The positive phase-decomposition sufficiency proof likewise adapts when its exponential-moment scale is `b_N` and phase separation is `Delta_N`, with `b_N=o(Delta_N)`. The endpoint tangent coefficient is `O(Delta_N b_N/c_N)`, the local quadratic correction is `O(b_N^2/c_N)`, and the global amplification is `O(Delta_N^2/c_N)`. Therefore a sufficient condition is

\[
c_N\gg\Delta_N b_N,
\qquad\delta_N\exp(C\Delta_N^2/c_N)\to0,
\]

or, if `delta_N<=exp(-s_N)` with `s_N->infinity`,

\[
c_N\gg\max\{\Delta_N b_N,\Delta_N^2/s_N\}.
\]

This is an assumption simplification and a change-of-scale statement, not an automatic theorem for phases with unverified fluctuation or exponential-moment properties.

## Final linear-capacity appendix review, 2026-09-07

Read and independently checked Section 11, Equations (18)–(28), of `shared-bath-phase-correlations.md`. All formulas and limiting arguments pass review.

For `c_N/N->gamma>0`, put `a=beta^2/gamma`, `V=v_-+v_+`. On mixed assignments the exact weight converges uniformly on bounded standardized windows to `exp[-a(z_-+z_+)^2/2]`. On aligned assignments its argument tends to the nonzero constants `±beta ell/gamma`; the exact logarithmic inequality or the cutoff gives suppression. The appendix correctly avoids applying a small-argument expansion to those aligned states.

The normalizer tends to `2w_-w_+(1+aV)^(-1/2)`. Adding `a11^T` to the Gaussian precision gives

\[
\Sigma=\operatorname{diag}(v_-,v_+)
-\frac{a}{1+aV}(v_-,v_+)^T(v_-,v_+),
\qquad
u_i=\frac{v_i(1+av_j)}{1+aV}.
\]

The exact marginal likelihoods converge uniformly on compact phase windows and are globally uniformly bounded. Conditional tightness therefore yields the stated full-state marginal TV limit

\[
\frac12\sum_i\int\left|\frac12\phi_{u_i}-w_i\phi_{v_i}\right|.
\]

At balanced weights this is one half the sum of the two normal-law TV distances. The stated crossing point `x_i^2=u_i v_i log(v_i/u_i)/(v_i-u_i)` and the resulting normal-CDF expression are correct.

The appendix separately controls entropy through the bounded function `W log W` and bounded marginal likelihoods. The joint divergence has the additional Gaussian term

\[
\frac12\log(1+aV)-\frac{aV}{2(1+aV)},
\]

while each marginal divergence has one half the sum of its phasewise Gaussian divergences. Subtraction gives exactly

\[
I_Q\longrightarrow\log2+
\frac12\log\frac{(1+av_-)(1+av_+)}{1+aV}.
\]

This proof uses conditional weak Gaussian limits to evaluate bounded likelihood integrals. It does not assert full-state Gaussian TV convergence or invoke convergence of differential entropies. The finite-N reference-dependent approximation in Section 11.1 makes that distinction explicit. The statement is restricted to the centered calibration and does not claim an arbitrary-tuning impossibility result at linear capacity. No corrections to the appendix were required.
