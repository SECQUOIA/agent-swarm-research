# Independent review of capacity perturbation and nucleation bounds

Date: 2026-09-06. Reviewer: independent subagent, working from the mathematical definitions in `research/scouting-nucleation.md`. The scouting note was not edited.

**Verdict:** equations (1)–(4), their vector-field versions, the network sharpness claim, and the normalization cautions are correct under the stated hypotheses. These are verified mathematical results, not yet verified novel or publishable results. The central inequalities are immediate consequences of classical variational principles; prior-art risk is substantial. A small wording correction is needed: the interval width vanishes iff the score is constant only when the perturbation parameter is nonzero.

## 1. Independent finite-perturbation derivation

Write K=wD and let H be the admissible affine space of potentials taking values 0 and 1 on the fixed source and sink sets. Assume 0<C<∞ and that the associated Dirichlet and unit-current problems are well posed. For every admissible potential f and every divergence-free unit flow j, integration by parts gives

\[
\int j\cdot\nabla f=1.
\]

Weighted Cauchy–Schwarz therefore gives

\[
1\leq\left(\int\nabla f\cdot K\nabla f\right)
        \left(\int j\cdot K^{-1}j\right).
\]

For the old exact solution, q0 and j0=K0∇q0/C0 attain equality. For the new tensor K1=rK0, use q0 as a trial potential and use j0 in this Cauchy–Schwarz inequality with the *new* minimizing potential. The results are

\[
 C_1\leq C_0\mathbb E_{\nu_0}r,
 \qquad C_1\geq C_0/(\mathbb E_{\nu_0}r^{-1}).
\]

This reproduces equation (1) with r=exp(λQ) without having to assume a separate minimizer exists in the current formulation. The current is still admissible precisely because the domain and source/sink sets are fixed. The two moments must be finite for both bounds to be informative; C0 and C1 must also be positive and well defined. Vanishing capacities and disconnected boundary components require separate treatment and cannot be covered by the normalized dissipation measure.

The same calculation proves the matrix-valued trial-pair extension as written in the scout's note. Tensor changes do not in general reduce to one scalar exponential moment.

The logarithmic interval width is log M(λ)+log M(−λ), which is nonnegative by Cauchy–Schwarz. For λ≠0, equality holds precisely when exp(λQ/2) is proportional to exp(−λQ/2), meaning Q is constant ν0-almost everywhere. At λ=0 equality holds for every Q. With four sufficiently controlled moments, or more simply a moment-generating function in a neighborhood of zero, its expansion is λ²Var(Q)+O(λ⁴). Hoeffding's stated range corollary has the correct factor 1/8.

## 2. Curvature, its sign, and the vector bound

Use Eλ(u,v)=∫wλ∇u·D∇v, and let h=∂λqλ. The stationarity condition Eλ(qλ,v)=0 for all homogeneous-boundary v gives

\[
E_\lambda(h,v)=-\int w_\lambda Q\nabla q_\lambda\cdot D\nabla v.
\]

The envelope derivative and its derivative are

\[
C'=\int w_\lambda Q|\nabla q_\lambda|_D^2,
\]

\[
C''=\int w_\lambda Q^2|\nabla q_\lambda|_D^2
       +2\int w_\lambda Q\nabla q_\lambda\cdot D\nabla h
     =C\mathbb E_\nu Q^2-2E_\lambda(h,h).
\]

Consequently

\[
(\log C)''=\operatorname{Var}_\nu(Q)-2E_\lambda(h,h)/C.
\]

There is no missing factor of two or sign error. To bound the response, set m=EνQ. Orthogonality permits replacing Q by Q−m in the forcing. Testing with v=h and applying Cauchy–Schwarz gives

\[
E_\lambda(h,h)\leq
\sqrt{C\operatorname{Var}_\nu(Q)E_\lambda(h,h)},
\]

hence 0≤E(h,h)/C≤Varν(Q). Both susceptibility bounds follow.

For p fields, define hi=∂θi q and Gij=E(hi,hj)/C. The exact Hessian is Covν(Q)−2G. The argument above applied to every linear combination of the Qi proves 0≼G≼Covν(Q), not merely nonnegative diagonal entries. This validates the stated Loewner-order covariance sandwich. A Hessian component can have either sign; equilibrium convexity cannot be imported into a capacity without checking the committor response.

Regularity caveat: finite moments at a single parameter do not themselves justify twice differentiating the elliptic problem. A clean sufficient hypothesis is a fixed bounded Lipschitz domain with nontrivial Dirichlet pieces, uniformly elliptic bounded K0, and bounded Qi. More general unbounded domains and scores are possible but need explicit differentiability and coercivity hypotheses. The scout already assumes differentiation is justified, so this is a requirement for a theorem statement, not a discovered error.

## 3. Exact equality mechanisms and continuum sharpness

The parallel and series network examples are correct, including the use of normalized resistances in a chain. Both can realize the same prescribed finitely supported score law: for probabilities pi, use parallel conductances pi and series resistances pi. Both have C0=1 and ν0(i)=pi.

Sharpness also holds in a connected continuum geometry, without a thin-channel limit. Take Ω=(0,1)×(0,1), constant w0 and D=I, Dirichlet faces x=0 and x=1, and reflecting faces y=0 and y=1. Then q0=x and ν0 is uniform area measure.

- For Q(x,y)=F(x), direct integration gives Cλ/C0=[∫0¹exp(−λF(s))ds]⁻¹: the lower bound is exact.
- For Q(x,y)=F(y), qλ=x for every λ, and Cλ/C0=∫0¹exp(λF(s))ds: the upper bound is exact.

Thus the same reference score distribution realizes both extremes even within connected reversible diffusions. The rectangle is Lipschitz and piecewise smooth. A periodic transverse direction gives a smooth product manifold with only the two end boundaries. Do not call the Euclidean rectangle globally smooth.

There is a more general equality mechanism. The pushforward of ν0 under q0 is the uniform distribution on [0,1]. Indeed, for any smooth φ, choose Φ with Φ'=φ; integration by parts against the conserved reactive current gives

\[
\int\phi(q_0)\nabla q_0\cdot K_0\nabla q_0
 =C_0\int_0^1\phi(s)\,ds.
\]

Therefore, if Q(x)=F(q0(x)), set

\[
q_\lambda(x)=
\frac{\int_0^{q_0(x)}e^{-\lambda F(s)}ds}
     {\int_0^1e^{-\lambda F(s)}ds}.
\]

It has the prescribed boundary values, and Kλ∇qλ equals a spatially constant multiple of K0∇q0, so it solves the new equation and preserves the normalized current. This proves exact lower-bound attainment for arbitrary geometry with a perturbation depending only on the old committor. This is a useful characterization; no novelty claim is made for it.

Upper finite-bound equality holds precisely when q0 remains minimizing for the new Kλ. In a smooth setting and at λ≠0, a sufficient and necessary local PDE condition is

\[
\nabla Q\cdot K_0\nabla q_0=0
\]

along with the unchanged boundary conditions. This means the score is constant along reference current lines. At the curvature level, upper equality means h=0 in energy norm, while lower equality means the centered field (Q−m)∇q lies entirely in the subspace of homogeneous-boundary gradients. The explicit series/transverse constructions realize these alternatives.

## 4. Normalization and counterexample audit

Cλ depends on the arbitrary multiplicative normalization of wλ. A normalized equilibrium frequency is Cλ/Zλ; a capacity rate normalized by physical basin occupation is Cλ/ZA,λ. Dividing the established interval by the exactly reweighted basin moment yields equation (2), and subtracting the basin log partition Hessian yields the scout's rate Hessian bounds. Adding a constant to Q cancels in either physical normalization. This check passes.

The distinction from a rate normalized by last-visited-A occupation is material: that occupation includes the intervening domain and depends on the committor. Nor is C/ZA the inverse first-passage mean from an arbitrary ensemble. The scout preserves both distinctions correctly.

If Dλ=e^{aλ}D0, the generator and capacities acquire the same rate multiplier while the invariant probability measure stays fixed. If Dλ=e^{bλ²/2}D0, the capacity curvature gains b. This is an explicit counterexample to any universal susceptibility bound expressed only through the equilibrium potential score with unrestricted mobility changes. The scout's exclusion is necessary. Temperature perturbations often change both β and mobility, and cannot automatically be treated as the specified potential-only field.

An approximate committor generally produces a vector K0∇qapprox with nonzero divergence. Its use as a supposed trial current invalidates the lower guarantee. A valid approximate implementation needs an independently admissible flow or a certified correction. This warning is mathematically necessary, not merely a numerical nicety.

## 5. Independent numerical check

The standalone script `check_nucleation_bounds.py` uses weighted graph Laplacians, solves the Dirichlet problem directly, differentiates the linear equations, and compares directional second derivatives with centered finite differences. It uses a fixed seed and no source code from the scout. It also constructs paired exact series/parallel examples with the same score law.

Command:

```bash
python research/verification/check_nucleation_bounds.py
```

Observed results on 2026-09-06:

| Check | Result |
| --- | --- |
| Random connected networks | 200 |
| Finite perturbations | 800 |
| Maximum finite-bound violation | 1.11×10⁻¹⁵ |
| Maximum covariance-order violation | 3.57×10⁻¹⁵ |
| Maximum second finite-difference discrepancy | 1.06×10⁻⁷ |
| Maximum first finite-difference discrepancy | 2.83×10⁻⁸ |
| Maximum series/parallel equality discrepancy | 2.22×10⁻¹⁶ |

Numerics are consistent with floating-point error and finite-difference truncation. The analytical proof supplies the general guarantee.

## 6. Prior art and publication assessment

The following openly available primary sources were independently checked on 2026-09-06:

1. Gu, Lin, and Zhou, *Sensitivity Analysis and Optimization of Reaction Rate* (2017), [author PDF](https://personal.cityu.edu.hk/xizhou/cmsv-207-xiangzhou.pdf). This is direct prior art for potential sensitivity of reaction rates. The first-order formula should remain explicitly attributed, as in the scout.
2. Ghosh, Boyd, and Saberi, *Minimizing Effective Resistance of a Graph* (2006), [author PDF](https://web.stanford.edu/~boyd/papers/pdf/eff_res_mtns06.pdf). The paper derives conductance derivatives and Hessians for total effective resistance and observes that analogous derivations apply to pair resistance. It does not establish the precise log-capacity covariance sandwich in the passages checked, but confirms that network Hessian machinery is established.
3. Harrach and Ullrich, *Monotonicity-Based Shape Reconstruction in Electrical Impedance Tomography*, SIAM J. Math. Anal. 45 (2013), 3382–3403, [open preprint](https://arxiv.org/html/1812.05300), [publisher record](https://epubs.siam.org/doi/10.1137/120886984). Lemma 6 bounds a finite current-voltage change above and below by integrals using the reference potential and conductivity ratios. The paper explicitly traces that estimate to earlier work by Ikehata, Kang, Seo, and Sheen. This is close structural prior art for comparison bounds based on one known field, though its fixed boundary-current operator is not identical to the capacity experiment.

Additional searches used “effective resistance Hessian conductance sensitivity,” “conductivity sensitivity second derivative variational,” “capacity perturbation Thomson inequality,” and “conductivity monotonicity inequality.” No exact preexisting statement of the dissipation-covariance sandwich was located in this limited independent search. That does not establish novelty.

My assessment is that the proof is sound but too immediate from established Dirichlet/Thomson duality to support a strong novelty claim alone. A useful contribution would need a distinctive thermodynamic application or a certified computational method that answers a practical rate-extrapolation question better than current techniques. The equality mechanisms and failure of a positive-variance interpretation are worth retaining as precise explanatory results regardless of publication outcome.
