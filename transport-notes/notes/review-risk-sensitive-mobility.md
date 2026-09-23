# Independent review: the optimized disorder-moment threshold

Reviewed 2026-09-07 by `review_localization`.

The matching-order theorem in [risk-sensitive-mobility.md](risk-sensitive-mobility.md) is correct for every fixed `q>0`. Independent derivation confirms the threshold `q=8/5`, the critical logarithm with exponent `7/5`, the lower bounds for arbitrary integrable mobility placements, and the graded upper constructions. The result is a pair of bounds up to constants, not an asymptotic equivalent with a known coefficient.

No error requiring a change to the theorem was found. A subsequently added tangent-of-energy argument also verifies the sharp coefficient for every subcritical order `0<q<8/5`; its independent review appears below. A separate moving-arc derivation of the critical constant is under independent review; this report does not verify that addition. The supercritical sharp constant remains undetermined. The finite-bulk optimized-moment transfer is proved separately in [review-risk-sensitive-finite-bulk.md](review-risk-sensitive-finite-bulk.md). Mathematical verification does not establish novelty.

## Statement and admissible class

For the periodic wall, `c` uniform on `[-2,2]`, and `k_c(s)=(c+cos s)²`, let

\[
J_c(D)=\sup_{f\in C^\infty_{\rm per}}
\left\{2\int f-\int[D|f'|^2+k_cf^2]\right\},
\qquad D\in L^1,\quad D\ge0,\quad\int D=M.
\]

Infinite values are permitted. The same D must be used for every c. Define

\[
\Phi_q(M)=\inf_D\mathbb E[J_c(D)^q].
\]

There are positive constants depending on q, but independent of sufficiently small M, that bound this quantity above and below by the corresponding expression

\[
\Phi_q(M)\asymp
\begin{cases}
M^{-q/4},&0<q<8/5,\\
M^{-2/5}[\log(1/M)]^{7/5},&q=8/5,\\
M^{(2-3q)/7},&q>8/5.
\end{cases}
\tag{1}
\]

All lower-bound tests are smooth. They therefore apply to the stated variational definition for every L¹ competitor, without assuming that a classical diffusion generator has already been assigned to an irregular coefficient.

## 1. The quotient representation handles all positive q

Optimizing the amplitude of any fixed test shape gives

\[
J_c(D)=\sup_{f\ne0}\frac{(\int f)^2}{\int[D|f'|^2+k_cf^2]}.
\tag{2}
\]

Terms with zero numerator are irrelevant. The denominator is positive for nonzero smooth f, since k_c is positive except at finitely many points. Raising the supremum to a positive power gives the corresponding quotient representation of `J_c(D)^q`.

For fixed f, the negative qth power of the affine denominator is convex for every `q>0`. Thus `J_c(D)^q` is convex in D even when `q<1`. The convexity claim in the source note is correct; it does not follow merely by composing a convex J with a concave power. The quotient representation is essential.

The reflection and half-period symmetrizations also check: reflection preserves k_c, and shifting s by π maps k_c to k_(−c). Averaging over the symmetric disorder law therefore permits those design symmetries without increasing the objective. These symmetries are not needed for the lower bounds below.

## 2. Independent derivation of the local mass bound

Near one fold, use the root position u as the parameter. On `u in [r,3r/2]`, with r small and fixed relative geometric constants, the parameter density is comparable to r because `|dc/du|=|sin u|`. The interval thus has probability comparable to r².

Choose a fixed spatial enlargement of this root interval. Inside it,

\[
k_c(s)=(\cos s-\cos u)^2\le Cr^2(s-u)^2.
\]

Let m be the actual mass of the competing mobility in that enlargement. Assume `0<m<=c_1r^7`; there is no assumption on its distribution within the enlargement. Choose a fixed nonnegative compact smooth bump psi and

\[
\ell=\kappa(m/r^3)^{1/4},\qquad f_u(s)=\psi((s-u)/\ell).
\]

With fixed sufficiently small constants, every support lies in the enlargement. The load has magnitude proportional to ell, and the potential energy is at most `Cr²ell³`. Define the actual derivative energy

\[
B(u)=\ell^{-2}\int D(s)|\psi'((s-u)/\ell)|^2ds.
\]

Fubini gives

\[
\frac1r\int_r^{3r/2}B(u)du\le\frac{Cm}{r\ell}.
\tag{3}
\]

The integral in u has length comparable to r; normalization factors of two only change constants. The quotient formula and Jensen's inequality for the convex decreasing function `x -> (x+Cr²ell³)^(−q)` imply

\[
\mathbb E[J_c(D)^q;\,u\in[r,3r/2]]
\ge c_q r^2\frac{\ell^{2q}}
{[m/(r\ell)+r^2\ell^3]^q}.
\]

The chosen width makes both denominator terms comparable. Since `ell^4` is proportional to `m/r³`, the result is

\[
\mathbb E[J_c(D)^q;\,u\in[r,3r/2]]
\ge c_q r^{2-5q/4}m^{-q/4}.
\tag{4}
\]

The exponents check directly: after balancing, the quotient is `r^(−2q)ell^(−q)`, and multiplication by the probability r² gives (4). Jensen is applied to the inverse denominator, so the argument is valid for all positive q, including q<1.

If m=0, the coefficient vanishes almost everywhere throughout the chosen open interval. Every retained interior root then has zero mobility in a neighborhood and a quadratic potential zero. Bumps of width tending to zero make the quotient diverge. The infinite-value interpretation in (4) is therefore correct.

## 3. The three lower bounds

For q<8/5, take one fixed regular root interval. Its local mass satisfies `m<=M`, so the condition `m<=c_1r^7` holds for sufficiently small M. Equation (4) immediately gives `Phi_q(M)>=c_qM^(−q/4)`.

For q=8/5, use root intervals at radii `r_j=r_*4^(−j)` and disjoint fixed spatial enlargements. Retain radii at least `C M^(1/7)`, so every actual local mass `m_j<=M` satisfies the small-mass condition. There are `N` proportional to `log(1/M)` intervals. Their disorder parameter intervals are also disjoint. Since the radius power in (4) vanishes at q=8/5,

\[
\mathbb E J_c(D)^{8/5}\ge c\sum_{j=1}^N m_j^{-2/5}
\ge cN^{7/5}M^{-2/5},
\tag{5}
\]

using `sum m_j<=M` and convexity of the inverse power. A zero mⱼ already makes the expectation infinite. This proves the critical logarithm without assuming the design has a particular shape or a smallest spatial scale.

For q>8/5, take a single bump `f(s)=psi(s/R)` at a fold, with `R=M^(1/7)`. For offsets in a window of width proportional to R² around that fold, k_c is at most `CR⁴` on the support. For every design,

\[
\int D|f'|^2\le CM/R^2,\qquad
\int k_cf^2\le CR^5,\qquad |\int f|\ge cR.
\]

Since `M=R^7`, (2) gives `J_c(D)>=cR^(−3)` throughout this parameter window. Hence

\[
\mathbb E J_c(D)^q\ge c_qR^{2-3q}
=c_qM^{(2-3q)/7}.
\tag{6}
\]

At the critical q this single test misses a logarithm; the disjoint-scale argument (5) supplies it. These lower bounds are independent and cover all the regimes of (1).

## 4. Graded upper designs and their domains

Let r(s) denote distance to `{0,pi}`. Set

\[
\alpha=\frac{6q-4}{q+4},\qquad
D_M(s)=A(r(s)+R)^{-\alpha},
\qquad A=M\left[\int(r+R)^{-\alpha}\right]^{-1}.
\]

For every q>0, `−1<alpha<6`. Choose

\[
R=\begin{cases}
M^{1/(6+\alpha)},&q<8/5,\\
[M/\log(1/M)]^{1/7},&q=8/5,\\
M^{1/7},&q>8/5.
\end{cases}
\]

Direct integration near the two distance zeros gives `A` comparable to M for alpha<1, to `M/log(1/R)` for alpha=1, and to `MR^(alpha−1)` for alpha>1. In all three choices,

\[
A\asymp R^{\alpha+6}.
\tag{7}
\]

For each fixed M>0, this coefficient is continuous, bounded above, and bounded below by a positive number. Its natural form domain is ordinary periodic H¹. The corners of the distance function introduce no domain ambiguity; no derivative of D is required in the variational proof. Smooth approximations preserving comparability give the same order bounds.

For q<2/3, alpha is negative. This is allowed: the design then decreases toward the fold sites, while remaining positive for every fixed M. All comparability and coercivity arguments below remain valid for negative alpha because alpha is fixed and greater than −1.

## 5. Uniform upper response estimates

Near either fold let `t=1−|c|`; on the side with roots put `r=sqrt(t)`, up to fixed geometric constants. For `r>=C R`, choose neighborhoods of each root of radius proportional to r. On each neighborhood the mobility is comparable to `Ar^(−alpha)` and the potential is bounded below by a constant times `r²` times squared distance from that root.

Neumann bracketing, coefficient comparison, and the expanding-interval harmonic estimate give

\[
J_c(D_M)\le CA^{-1/4}r^{-3/2+\alpha/4}.
\tag{8}
\]

To check that the oscillator interval is sufficiently large, its scaled half-length is comparable to `(r/R)^((alpha+6)/4)`, by (7). This is uniformly bounded below when the fixed C is large enough. The complement contributes at most `Cr^(−3)` by its reciprocal potential, and this is no greater than the right side of (8), since

\[
\frac{r^{-3}}{A^{-1/4}r^{-3/2+\alpha/4}}
\asymp(R/r)^{(\alpha+6)/4}\le C.
\]

In the central parameter window `|t|<=C R²`, choose an interval of radius `K R` containing both possible roots with a fixed scaled margin. There `D_M` is comparable to R⁶. The exact local sine coordinate converts the potential to a quartic fold. Rescaling distance by R gives a uniformly coercive Neumann problem on a fixed interval, with operator scale R⁴ and integrated inverse scale R^(−3). The derivative coefficient is uniformly positive and bounded, and the compact family of nonnegative potentials contains no identically zero member. The complementary reciprocal-potential integral is also `O(R^(−3))`. Thus

\[
J_c(D_M)\le CR^{-3}\qquad(|t|\le CR^2).
\tag{9}
\]

On the side without roots, for `|t|>=C R²`, discard derivative energy to obtain `J_c(D_M)<=C|t|^(−3/2)`. Away from folds, the inside bound is `CA^(−1/4)` and the outside bound is constant.

## 6. Integrating the bounds

Since the offset measure on the inside is comparable to `r dr`, (8) gives the integral

\[
CA^{-q/4}\int_R^{r_*}r^{1-3q/2+\alpha q/4}dr.
\tag{10}
\]

Its decisive exponent is

\[
e_q=2-3q/2+\alpha q/4=\frac{8-5q}{q+4}.
\]

Below q=8/5, this is positive, so (10) is `O(M^(−q/4))`. The fold contribution is `O(R^(2−3q))`. If q>2/3 it may diverge, but its ratio to `M^(−q/4)` is comparable to `R^(e_q)` and tends to zero. For q<2/3, the no-root integral is bounded; at q=2/3 it grows logarithmically. These contributions are still smaller than `M^(−q/4)`. Thus no additional threshold occurs at q=2/3 in the optimum.

At q=8/5, alpha=1 and (10) is

\[
CA^{-2/5}\log(1/R)
\asymp M^{-2/5}[\log(1/M)]^{7/5}.
\]

The fold and adjacent no-root contributions are at most `CR^(−14/5)`, or `CM^(−2/5)[log(1/M)]^(2/5)`, one logarithm smaller. The regular-root contribution is also smaller.

Above q=8/5, e_q is negative and (10) is controlled by its lower limit. Using (7),

\[
A^{-q/4}R^{e_q}\asymp R^{2-3q}
=M^{(2-3q)/7}.
\]

The fold and no-root pieces have at most this order, and the regular-root piece is smaller because e_q<0. These computations complete the upper bounds matching (4)–(6).

## Verification boundary

The transition at 8/5 and the critical logarithm are established up to fixed multiplicative constants. The logarithm is a cost of allocating one finite budget among a growing number of disjoint spatial scales; a single fold test cannot establish it.

The formal fixed-shape expression and the beta-function coefficient in the source note are algebraically consistent, including their reduction at q=1. The order argument above does not establish their sharpness; the additional independent review below now does so for every subcritical q. The graded families need not be exact finite-budget optimizers, and no uniqueness claim follows.

The same lower tests also exclude an improvement from finite-measure concentration in the corresponding smooth-test scalar relaxation: the moving-bump average estimate uses only nonnegative integration and total local mass. This statement does not define a physical diffusion process for atomic mobility.

All claims here concern a field selected before observing c. Allowing an offset-dependent design changes the problem. The optimized-moment transfer to finite transverse bulk mixing is now established in [review-risk-sensitive-finite-bulk.md](review-risk-sensitive-finite-bulk.md), with its stated assumptions and uniform correction bound.

## Additional review: the sharp subcritical coefficient

The new tangent-of-energy proof appended to the source note is correct and improves the subcritical order result to the equivalent

\[
\Phi_q(M)\sim K_qM^{-q/4},\qquad
K_q=2^{q-3}C_0^q
\left[2B\left(\frac{1-\alpha_q}{2},\frac12\right)\right]^{1+q/4},
\quad0<q<8/5.
\tag{11}
\]

I checked this independently without assuming an oscillator virial identity or an exact maximizing test function.

Retain a compact symmetric set of offsets inside `(-1,1)`, and let E be its two root arcs. Put `beta=q/4`, `W_q=|sin r|^(1−3q/2)`, `Z_E=integral_E W_q^(1/(1+beta))`, and `d_E=W_q^(1/(1+beta))/Z_E`. Choose a fixed compact smooth test psi of positive integral I. Write `T=integral |psi'|²`, `V=integral y²psi²`, `Q=T+V`, and `j=I²/Q`.

Use the two local test fields with widths `(Md_E/a)^(1/4)` and amplitudes `(Md_Ea)^(−1/2)`. Their common scaling factor is `z=M^(−1/4)d_E^(−1/4)a^(−3/4)`. The paired source is exactly `2Iz`; their true reaction energy is `2Vz+o(z)`, uniformly over the retained offsets. Their actual derivative energy B is unrestricted and depends on the competing design.

The reference number `E0=2Qz` is positive. The supporting-line inequality for `E^(−q)` and the quotient formula give

\[
J_c(D)^q\ge(2j)^qz^q
\left[1+\frac{qT}{Q}-\frac{qB}{2Qz}+o(1)\right].
\tag{12}
\]

The remainder is independent of D. The inequality is valid for every positive q and every actual energy, including where its right side is negative.

The average of the factor `(2j)^qz^q` is

\[
K_{\psi,E}M^{-\beta},\qquad
K_{\psi,E}=2^{q-3}j^qZ_E^{1+\beta}.
\]

The paired-root factor is important: a function with the same value at both roots has offset average equal to one half its root-density integral over E. With `rho=|sin r|/4`, this gives the factor `2^(q−3)` displayed above.

For the weighted derivative term in (12), the uniform moving-root calculation gives

\[
\left\|\mathbb E\left[\frac{q(2j)^q}{2Q}z^{q-1}|h_c'|^2\right]\right\|_\infty
\le M^{-1-\beta}\left[\frac{qT}{Q}K_{\psi,E}+o(1)\right].
\tag{13}
\]

In particular, multiplying the earlier derivative density by `z^(q−1)` changes its coefficient to `M^(−1−beta) rho d_E^(−1−beta)a^(−3q/4)`. Its spatial factor is exactly `Z_E^(1+beta)/4`. The kernel Jacobian contributes T, and the remaining prefactor is `q(2j)^q/(2Q)`. These factors produce exactly the coefficient in (13), with no missing factor from the paired roots. The extended-arc and truncated-kernel argument still makes the estimate uniform at all spatial points, including the arc edges.

Using the actual budget in (13) cancels precisely the `qT/Q` part of the constant term in (12). Therefore every design satisfies the lower asymptotic coefficient `K_(psi,E)`. Taking the oscillator quotient supremum `sup j=C0` and then expanding E proves the lower bound in (11). This confirms sharpness against arbitrary M-dependent concentration and oscillation, rather than only fixed-shape competitors.

For the matching upper bound, the positive regularized shape

\[
d_M(s)=\frac{(|\sin s|+R)^{-\alpha_q}}
{\int(|\sin v|+R)^{-\alpha_q}dv},\qquad
R=M^{1/(6+\alpha_q)},\qquad D_M=Md_M
\]

converges smoothly near every fixed simple root to the formal normalized optimizer. Its pointwise scalar asymptotic follows from variable-coefficient quadratic bracketing. The graded estimates already verified above imply the common envelope

\[
M^{q/4}J_c(D_M)^q\le C|1-|c||^{-\gamma_q},\qquad
\gamma_q=\frac{3q}{4}-\frac{\alpha_qq}{8}
=\frac{7q}{2(q+4)}<1.
\]

This includes both sides of each fold. In the central window the normalized bound is `CR^(−2gamma_q)`, dominated by `C|t|^(−gamma_q)` for `|t|<=CR²`. Outside on the no-root side, use `M<=C|t|^((6+alpha_q)/2)` and the reciprocal-potential bound. Thus dominated convergence applies even for `4/3<=q<8/5`, where constant-mobility moment domination would fail. Its limiting integral is exactly K_q, proving the upper bound.

The sharp extension is consequently verified. It establishes one asymptotically optimal regularized family; it does not prove convergence of all optimizing families, uniqueness, or an exact optimizer at finite budget.
