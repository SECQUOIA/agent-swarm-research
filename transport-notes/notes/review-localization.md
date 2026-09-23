# Independent review: quadratic localization of the integrated surface resolvent

Reviewed 2026-09-06 by `review_localization`.

The general-profile scalar crossover in [the surface-exchange result](result-surface-exchange.md) is correct under its stated fixed-profile assumptions. The proof below handles the constant source on the limiting real line, artificial Neumann boundaries, multiple minima, and uniformity for bounded minimum-rate crossover parameter. Together with the independently reviewed finite-bulk cell argument, it supports **verified within the stated model** for the static dispersion theorem. This mathematical conclusion does not establish literature novelty or experimental applicability.

An earlier localization paragraph asserted an unnecessary stronger interval-tail estimate. The main note now uses the proved uniform `O(L^-1/2)` integrated absolute-tail bound below, which suffices and avoids an unproved boundary comparison.

## Precise statement

Let Γ be a fixed finite union of smooth compact one-dimensional periodic components, with arclength coordinate s. Let `k0 >= 0` be fixed and C². Suppose its zero set consists of `m >= 1` isolated points, and

\[
k_0(s_j+x)=a_jx^2+o(x^2),\qquad a_j>0.
\]

Components with no zeros must have strictly positive k₀. Define

\[
H_{e,\delta}=-e\partial_s^2+k_0+\delta,
\qquad I(e,\delta)=\langle1,H_{e,\delta}^{-1}1\rangle_{L^2(\Gamma)},
\qquad e>0,\quad\delta\ge0.
\]

For every fixed finite `M`,

\[
\lim_{e\downarrow0}\sup_{0\le t\le M}
\left|e^{1/4}I(e,t\sqrt e)
-\sum_{j=1}^m a_j^{-3/4}\mathcal C(t/\sqrt{a_j})\right|=0,
\tag{1}
\]

where

\[
\mathcal C(z)=\frac\pi2
\frac{\Gamma((z+1)/4)}{\Gamma((z+3)/4)}.
\tag{2}
\]

The function in the sum is positive and continuous on `[0,M]`, with positive minimum. Thus (1) implies the claimed uniform relative asymptotic. If there are no zeros, the singular formula with an empty sum is not an asymptotic equivalent; instead the integral stays bounded and converges to `integral 1/k0` when δ tends to zero.

## 1. The constant source is a bounded energy functional

For `R >= 2` let

\[
E_{R,z}(v)=\int_{-R}^R\bigl(|v'|^2+(y^2+z)|v|^2\bigr)\,dy,
\qquad z\ge0.
\]

There is an absolute constant `c > 0`, independent of `R >= 2`, such that

\[
E_{R,0}(v)\ge c\int_{-R}^R(1+y^2)|v|^2\,dy,
\qquad v\in H^1(-R,R).
\tag{3}
\]

Here is a direct reason why free endpoints cause no difficulty. On `[-2,2]`, the elementary anchored Poincaré estimate

\[
\int_{-1}^1|v|^2
\le C\left(\int_{-2}^2|v'|^2+\int_1^2|v|^2\right)
\]

follows by writing `v(x)=v(y)+integral_y^x v'` and averaging over `y in [1,2]`. The last integral is bounded by `integral y²|v|²`. On the rest of the interval, `y² >= 1` controls the unweighted mass. This proves (3), without a boundary condition.

Weighted Cauchy–Schwarz consequently gives

\[
\left|\int_{-R}^R v\right|
\le \int_{-R}^R|v|
\le A E_{R,z}(v)^{1/2},
\tag{4}
\]

with a universal `A`. Moreover, for `L >= 1`,

\[
\int_{L<|y|<R}|v|\,dy
\le \left(\int_{L<|y|<R}y^{-2}\,dy\right)^{1/2}
     \left(\int_{-R}^R y^2|v|^2\,dy\right)^{1/2}
\le (2/L)^{1/2}E_{R,z}(v)^{1/2}.
\tag{5}
\]

The same estimates hold on the real line. In particular, on the Hilbert energy space

\[
\mathcal E=\{v\in H^1(\mathbb R):yv\in L^2(\mathbb R)\},
\]

with squared norm `E_(infinity,0)`, the map `v -> integral v` is bounded. Although `1` is not an L² source on the real line, its inverse under the harmonic oscillator is therefore well defined as the unique energy solution. The quadratic variational quantity

\[
C_\infty(z)=\sup_{v\in\mathcal E}
\left\{2\int_{\mathbb R}v-E_{\infty,z}(v)\right\}
\tag{6}
\]

is finite. Its maximizer q satisfies `E(q)=integral q=C_infinity(z)`.

## 2. Expanding Dirichlet and Neumann intervals have the same limit

Define

\[
C_R^B(z)=\sup_{v\in\mathcal V_R^B}
\left\{2\int_{-R}^R v-E_{R,z}(v)\right\},
\]

where `V_R^D=H0¹(-R,R)` and `V_R^N=H¹(-R,R)`. These equal the integrals of the Dirichlet and Neumann resolvent solutions, respectively. The weak problem, not a pointwise assumption about endpoint behavior, supplies the Neumann condition.

For either boundary condition, the maximizing solution `q_R` obeys

\[
E_{R,z}(q_R)=\int_{-R}^R q_R=C_R^B(z)\le A^2.
\tag{7}
\]

Indeed, insert `q_R` in its own weak equation and use (4). The energy bound also bounds its L² norm uniformly by (3), and its source tails uniformly by (5).

For Dirichlet conditions, extension by zero embeds the variational space in `E`, so `C_R^D(z) <= C_infinity(z)`. Conversely every compactly supported smooth test function is admissible for all large R. Such functions are dense in `E`: cutoff first, using `v', yv, v in L²`, and then mollify on the compact support. Hence

\[
C_R^D(z)\longrightarrow C_\infty(z).
\tag{8}
\]

For Neumann conditions, the Dirichlet inclusion already gives the lower limit. To check the upper limit, take any sequence `R_n -> infinity` and its Neumann maximizers. By (3) and (7), a subsequence converges weakly in H¹ on every fixed compact interval and strongly in L² there to a function q. Lower semicontinuity followed by expansion of the compact interval gives

\[
q\in\mathcal E,\qquad
E_{\infty,z}(q)\le\liminf_n E_{R_n,z}(q_{R_n}).
\]

Local strong convergence and the uniform tails (5) give

\[
\int_{-R_n}^{R_n}q_{R_n}\,dy\longrightarrow\int_{\mathbb R}q\,dy.
\]

Using the variational objective itself now yields

\[
\limsup_n C_{R_n}^N(z)
\le 2\int q-E_{\infty,z}(q)
\le C_\infty(z).
\tag{9}
\]

The subsequence may be chosen to attain the upper limit, so (9) proves convergence along every sequence. This explicitly rules out a surviving contribution from the artificial Neumann endpoints.

The convergence is uniform for `z` in any fixed compact subset of `[0,infinity)`. Indeed, if `z2 >= z1`, evaluation at the maximizer for z₁ and monotonicity give

\[
0\le C_R^B(z_1)-C_R^B(z_2)
\le(z_2-z_1)\|q_{R,z_1}\|_2^2
\le C(z_2-z_1).
\tag{10}
\]

The real-line quantity has the same Lipschitz bound. Pointwise convergence plus this common Lipschitz bound gives uniform convergence on compact intervals by a finite-grid argument. All these statements include z=0.

## 3. Evaluation of the real-line quantity

Let `H0=-partial_y²+y²`. Its Mehler kernel is

\[
K_t(y,w)=\frac1{\sqrt{2\pi\sinh(2t)}}
\exp\left[-\frac{(y^2+w^2)\cosh(2t)-2yw}{2\sinh(2t)}\right].
\]

The exponent matrix has determinant one, so direct Gaussian integration gives

\[
\int_{\mathbb R^2}K_t(y,w)\,dy\,dw
=\sqrt{\frac{2\pi}{\sinh(2t)}}.
\]

To justify applying the semigroup resolvent to a constant source, first use the L² source `1_[-L,L]`. These sources converge to the constant functional in the dual energy norm, by the real-line version of (5). Their quadratic resolvent forms therefore converge to (6). Kernel positivity and monotone convergence identify this limit as

\[
C_\infty(z)=\int_0^\infty e^{-zt}
\sqrt{\frac{2\pi}{\sinh(2t)}}\,dt.
\tag{11}
\]

The integral is finite even at z=0: its integrand is `O(t^-1/2)` near zero and `O(exp(-t))` at infinity. Setting `r=exp(-4t)` gives

\[
C_\infty(z)=\frac{\sqrt\pi}{2}
B\left(\frac{z+1}{4},\frac12\right)=\mathcal C(z),
\]

which proves (2) without treating the constant as an L² vector.

## 4. Bracketing the physical wall

Fix `eta > 0` smaller than every aⱼ. Choose disjoint fixed coordinate intervals `U_j=(-r_j,r_j)` around the zeros, small enough that

\[
(a_j-\eta)x^2\le k_0(s_j+x)\le(a_j+\eta)x^2
\qquad (|x|\le r_j).
\tag{12}
\]

Their complement is a finite union of intervals or periodic components on which `k0 >= kappa_eta > 0`. Introduce the scalar variational form

\[
I(e,\delta)=\sup_{v\in H^1(\Gamma)}
\left\{2\int_\Gamma v-
\int_\Gamma[e|v'|^2+(k_0+\delta)|v|^2]\right\}.
\tag{13}
\]

For a lower bound, restrict to functions supported on the Uⱼ with zero endpoint traces. For an upper bound, allow independent H¹ functions on every cut piece. Restriction reduces the supremum, while independent endpoint traces enlarge it. Ordering the potential in (12) therefore gives

\[
\sum_j J^D(e,\delta,a_j+\eta,r_j)
\le I(e,\delta)
\le \sum_j J^N(e,\delta,a_j-\eta,r_j)+O_\eta(1),
\tag{14}
\]

where J denotes the integrated resolvent on `(-r,r)` with quadratic potential `b x²+delta`. The complementary term is bounded uniformly in e and δ by its length divided by κη: discard its derivative energy and maximize the remaining pointwise quadratic objective. There are no interface cross terms in (13).

The exact change of variables `x=(e/b)^(1/4)y` gives

\[
J^B(e,\delta,b,r)
=e^{-1/4}b^{-3/4}
C_{r(b/e)^{1/4}}^B\left(\frac{\delta}{\sqrt{be}}\right).
\tag{15}
\]

Set `delta=t sqrt(e)`, with `0 <= t <= M`, multiply (14) by `e^(1/4)`, and use the uniform interval convergence. Its lower and upper sums converge uniformly to

\[
F_\eta^+(t)=\sum_j(a_j+\eta)^{-3/4}
\mathcal C\left(\frac{t}{\sqrt{a_j+\eta}}\right),
\qquad
F_\eta^-(t)=\sum_j(a_j-\eta)^{-3/4}
\mathcal C\left(\frac{t}{\sqrt{a_j-\eta}}\right),
\]

respectively. Continuity on a compact set of positive b and bounded t makes both sums converge uniformly to the target sum in (1) as η tends to zero. First take e to zero at fixed η, and then η to zero. This proves (1).

## Consequences and limits of this review

The result is a uniform leading asymptotic, with an `o(e^-1/4)` absolute error for bounded `delta/sqrt(e)`. C² regularity alone does not supply a useful algebraic error rate, and this proof does not claim an O(1) scalar remainder after subtracting the harmonic approximation. The separately proved convergence of the bulk correction concerns subtraction of the exact scalar integral I, which is a distinct statement.

The theorem transfers to the static finite-bulk dispersion through the reviewed relation `D_flow=(KV²/Z)I+O(1)`, and through its stronger version with a convergent bulk correction. It does not transfer transient formulas, establish an interchange of long-time and weak-diffusion limits, or settle the novelty of the resulting transport application.

No numerical test is needed to complete this localization step: the bracketing proof controls arbitrary fixed C² profiles satisfying the hypotheses, including multiple unequal minima. Existing oscillator and periodic-profile numerical checks remain useful checks of the coefficients and implementation.
