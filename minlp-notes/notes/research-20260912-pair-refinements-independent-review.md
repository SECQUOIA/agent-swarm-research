# Fresh mathematical review of the scalar residual-pair refinements

**Both proposed refinements are valid in their stated scopes.** The far-pair identity holds for the general scalar model, including signed, nonstationary transitions and zero process variances. The additional near-pair factor is valid under constant latent marginal variance and constant measurement variance. It cannot be obtained from the general model's upper latent-variance and lower measurement-variance bounds alone.

This review concerns the [proposed refinements](research-20260912-noisy-markov-far-pair-refinement.md), the [base theorem](research-20260912-noisy-markov-memory.md), and the previously reviewed [spacing bound](research-20260912-noisy-markov-spacing.md). It makes no publication-priority claim and changes no accepted bound helper, optimizer, or certificate. The [independent exact script](../code/research_20260912/review_noisy_markov_pair_refinements.py) and [saved results](../code/research_20260912/results/noisy-markov-pair-refinements-independent-review.json) retain the checks and source hashes.

## 1. General scalar far-pair identity

All variables below are centered errors. Let

\[
e_s=X_s-E[X_s\mid Y_{H_s}],\qquad
Z_s=e_s+v_s,\qquad p_s^-=\operatorname{Var}(e_s).
\]

The conditional predictor and its error are orthogonal, while \(v_s\) is independent of \(X_s\) and the earlier history. Therefore

\[
\operatorname{Cov}(X_s,Z_s)=p_s^-=d_s-r_s.
\]

Take selected \(s<t\) with **\(t-s>L\)**. Every observation in \(H_t\) occurs strictly after \(s\). Start the fresh local filter for \(H_t\) from the unconditional state distribution, and propagate the covariance of its state error with \(Z_s\). A transition multiplies this covariance by its scalar transition coefficient. An observation update has error

\[
e_j^+=(1-K_j^{(t)})e_j^- -K_j^{(t)}v_j.
\]

Here \(v_j\) and all subsequent process innovations are independent of \(Z_s\). Thus the update multiplies the covariance by \(1-K_j^{(t)}\). Multiplication of these scalar factors gives the exact identity

\[
\boxed{\operatorname{Cov}(Z_t,Z_s)
=\Phi(t,s)\,p_s^-\,\alpha_t},\qquad
\alpha_t=\prod_{j\in H_t}(1-K_j^{(t)}).
\]

Since \(0\le p_s^-\le\operatorname{Var}(X_s)\le\bar P\) and \(0\le\alpha_t\le1\),

\[
|\operatorname{Cov}(Z_t,Z_s)|\le\bar P\rho^{t-s}.
\]

This removes the earlier regression-history factor from the far majorant. The factors must come from the genuine fresh local filter. Neither a full-history filter with truncated coefficients nor the boundary case \(t-s=L\) is covered by this identity. At that boundary, \(s\in H_t\), and its observation noise is correlated with \(Z_s\), so the preceding propagation argument does not apply.

No stationarity, positive process-noise lower bound, or sign restriction on transitions was used. For \(L=0\), both histories are empty and the identity reduces to the ordinary latent cross-covariance.

## 2. Stationary near-pair refinement

The same argument, starting with an excluded old observation, gives

\[
\operatorname{Cov}(Z_t,Y_j)
=\Phi(t,j)\operatorname{Var}(X_j)\alpha_t,
\qquad j<t-L.
\]

Now assume constant latent marginal variance \(P\) and constant measurement variance \(r>0\). The first observation in any nonempty fresh history has prediction variance exactly \(P\). Its gain is

\[
\kappa=\frac{P}{P+r}.
\]

All subsequent factors \(1-K_j^{(t)}\) lie in \([0,1]\), so

\[
\alpha_t\le1-\kappa\qquad(H_t\ne\varnothing).
\]

For a near pair \(1\le h=t-s\le L\), selected \(s\) belongs to \(H_t\), ensuring the history is nonempty. Expand

\[
\operatorname{Cov}(Z_t,Z_s)
=\operatorname{Cov}(Z_t,Y_s)
-\sum_{j\in H_s}b_{sj}\operatorname{Cov}(Z_t,Y_j).
\]

Regression orthogonality removes the first term and every term with \(j\ge t-L\). Each surviving term has \(j<t-L\), so its old-observation covariance contains the common factor \(\alpha_t\le1-\kappa\). Applying the existing coefficient bound \(|b_{sj}|\le\kappa\rho^{s-j}\) therefore multiplies the entire previous near majorant by \(1-\kappa\). The coefficient bound's \(\kappa\) is retained.

For minimum gap \(g\), the reviewed pair majorant is consequently

\[
\phi_{\mathrm{new}}(h)=
\begin{cases}
P b^h,&h>L,\\[2mm]
P\kappa(1-\kappa)b^h
\displaystyle\sum_{d=\ell,\ell+g,\ldots\le L}b^{2d},
&g\le h\le L,
\end{cases}
\qquad \ell=\max(g,L+1-h),\quad b=|a|.
\]

Negative correlation does not affect these absolute bounds. The first-gain argument only needs constant marginal \(P\) and constant \(r\); stationary AR(1) is a sufficient setting. This observation does not by itself extend every other stationary formula to arbitrary dynamics.

The far majorant cannot receive \(1-\kappa\) uniformly: its fresh history may be empty. For example, with \(L=0\), \(P=r=1\), and \(a=1/2\), the two-observation covariance is \(1/2\), exceeding the incorrectly modified far bound \(1/4\).

## 3. A counterexample to the prohibited generalization

Use three selected times \(0,1,2\), \(L=1\), initial latent variance one, both transitions \(1/2\), zero process noise, and measurement variances all one. The latent variances are

\[
(P_0,P_1,P_2)=(1,1/4,1/16).
\]

The general assumptions hold with \(\bar P=1\), \(r_{\min}=1\), and \(\rho=1/2\). But the fresh history at time two starts from prediction variance \(1/4\), so its gain is \(1/5\) and its update factor is \(4/5\). The exact residual covariance is

\[
\operatorname{Cov}(Z_2,Z_1)=-1/20.
\]

Substituting \(\kappa=\bar P/(\bar P+r_{\min})=1/2\) into the stationary improved near bound would give \(1/32<1/20\), which is false. An upper bound on a gain cannot provide the lower bound on its first value that this improvement requires. Constant measurement variance alone is insufficient.

## 4. Transfer to row and spectral bounds

The new far majorant is no larger than the original far majorant. The new stationary near majorant multiplies its predecessor by a number in \([0,1]\). Both changes therefore reduce every pair weight. The existing exact interval-scheduling recurrence for a row is monotone in these weights, so it remains valid and cannot increase its row bound.

The existing spacing innovation floor

\[
d_* = r+T_g^{\lfloor L/g\rfloor}(P)
\]

is unchanged. Dividing the maximum priced absolute row majorant by this floor gives the same normalized covariance spectral bound and subsequent precision sandwich. Full history, independent observations, and families permitting at most one selected observation retain their exact zero-bound cases. The spacing constraint must still be enforced by the optimization and certificate domain.

For unrestricted distances, the near geometric sum in the proposal is also correct:

\[
\sum_{h=1}^L\sum_{d=L+1-h}^L b^{h+2d}
=\frac{b^{L+2}(1-b^L)(1-b^{L+1})}{(1-b)(1-b^2)}.
\]

Thus the general scalar far-only row bound is twice \(\bar P/d_*\) times the geometric far tail \(b^{L+1}/(1-b)\), plus \(\kappa\) times this near sum. In the constant-\(P,r\) case, the near multiplier becomes \(\kappa(1-\kappa)\). The \(b=0\) case is exact independence.

## 5. Independent exact checks

The reference covariance was formed directly from independent-innovation loading matrices. Local conditionals used exact rational dense LDL solves, with orthogonality checked. Update products used \(1-K_j=r_j/d_j\), where each prefix innovation variance \(d_j\) came from another dense conditional, rather than the author's Kalman recursion. No author verification function was reused.

The suite passed:

| Check | Count |
|---|---:|
| General nonstationary subset/window cases | 3,072 |
| Latent/residual covariance identities | 8,184 |
| Excluded-observation covariance identities | 6,152 |
| General far-pair identities | 3,076 |
| General near-pair bounds | 6,152 |
| Stationary subset/window/gap cases | 11,394 |
| Stationary pair inequalities | 23,391 |
| Stationary gain-product inequalities | 10,332 |
| Innovation-floor inequalities | 24,750 |
| Exact spectral sandwich matrices | 22,788 |
| Exhaustively enumerated row-majorant comparisons | 711 |
| Geometric-sum identities | 84 |

The nonstationary suite contains 24 covariance models with up to six times, signed and zero transitions, unequal measurement variances, zero process variances, and a zero-latent case. The stationary suite includes correlations \(-3/4,0,2/3\), zero and positive latent variances, unequal latent/nugget magnitudes, all subsets respecting each tested gap, \(L=0\), and complete-history windows. Spectral sandwiches were checked with exact PSD tests on the congruent matrices \(\delta D\pm(\operatorname{Cov}(Z)-D)\), avoiding numerical square roots or eigenvalues.

For the current 96-candidate probe, with \(g=2\), \(L=13\), \(b=0.6324555320336759\) interpreted as an exact decimal, and \(P=r=0.00125\):

| Majorant | Delta |
|---|---:|
| Previously accepted pair bound | 0.003795597732542757 |
| Far identity only | 0.0035242102623550668 |
| Far identity and stationary near factor | 0.003186913253976541 |

The combined refinement reduces delta by about 16.04%. This is a rigorously checked improvement in the approximation constant, not a newly regenerated optimization certificate or a measured solver improvement.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
  code/research_20260912/review_noisy_markov_pair_refinements.py
```
