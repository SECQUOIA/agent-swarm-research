# Optimizing disorder moments changes the kinetic-fold threshold

Research note, 2026-09-07. The parent proposed a new moment threshold for mobility design under uncertain defect locations. The argument below establishes the proposed powers and the critical logarithm up to positive multiplicative constants. The order bounds and the sharp leading constant below the threshold have passed [independent review](review-risk-sensitive-mobility.md). The critical coefficient has also passed a [separate independent review](review-critical-risk-mobility.md). The supercritical sharp constant remains open.

## Model and result

Use the periodic random-offset model from [robust-mobility-design.md](robust-mobility-design.md):

\[
 k_c(s)=(c+\cos s)^2,\qquad c\sim\operatorname{Uniform}[-2,2],
\]

\[
 J_c(D)=\sup_f\left\{2\int f-\int[D|f'|^2+k_cf^2]\right\},
 \qquad D\ge0,\quad\int_0^{2\pi}D=M.
\]

The same field is selected before the offset is observed. For every fixed `q>0`, define

\[
 \Phi_q(M)=\inf_{D:\,\int D=M}\mathbb E[J_c(D)^q].
\]

Then, as `M→0`,

\[
 \boxed{\Phi_q(M)\asymp
 \begin{cases}
 M^{-q/4},&0<q<8/5,\\
 M^{-2/5}[\log(1/M)]^{7/5},&q=8/5,\\
 M^{(2-3q)/7},&q>8/5.
 \end{cases}}
 \tag{1}
\]

Here `asymp` means upper and lower bounds with strictly positive constants independent of `M`; they may depend on the fixed moment order `q`. The bounds apply to unrestricted nonnegative integrable mobility fields, including fields with budget-dependent fine structure. The designs below achieve these orders while remaining positive everywhere and bounded for every fixed `M`.

For comparison, a uniform field with the same budget has the previously verified transition at `q=4/3`:

\[
 \mathbb E[J_c(M/(2\pi))^q]\asymp
 \begin{cases}
 M^{-q/4},&q<4/3,\\
 M^{-1/3}\log(1/M),&q=4/3,\\
 M^{1/3-q/2},&q>4/3.
 \end{cases}
\]

Spatial design therefore moves the threshold from `4/3` to `8/5`. Above the original threshold it improves the disorder-moment divergence rate. The objective is an unrooted moment; taking its `q`th root divides every power by `q`. Orders above one emphasize large responses, while orders below one should not be described as conventional risk aversion.

## Convexity and the formal shape calculation

For any nonzero smooth test field with nonzero integral,

\[
 J_c(D)=\sup_f\frac{(\int f)^2}{\int[D|f'|^2+k_cf^2]}.
\]

A positive denominator is understood, with the usual infinite-value extension. Consequently,

\[
 J_c(D)^q=\sup_f\frac{|\int f|^{2q}}
 {\bigl(\int[D|f'|^2+k_cf^2]\bigr)^q}
\]

is convex in `D` for every `q>0`: each denominator is affine and the negative power is convex. Thus averaging a design with its reflection cannot worsen this objective. Averaging also with the shift `s→s+π`, which maps `c→−c`, gives a reflection-symmetric, `π`-periodic design. This is a standard inverse-quadratic-form property, not a new convexity theorem.

For such a fixed symmetric positive shape `D=Md`, away from the folds the paired-root asymptotic formally gives

\[
 \mathbb E[J_c(Md)^q]\sim
 2^{q-3}C_0^q M^{-q/4}
 \int_0^{2\pi}|\sin s|^{1-3q/2}d(s)^{-q/4}ds,
\]

provided the relevant limit can be averaged. Minimizing this integral under `∫d=1` gives

\[
 d_q(s)\propto|\sin s|^{-\alpha_q},\qquad
 \alpha_q=\frac{6q-4}{q+4}.
 \tag{2}
\]

The shape is integrable exactly when `q<8/5`. At the threshold it behaves as `1/|s|`; above it the formal fixed-shape minimizer ceases to be integrable. The constructions below concentrate a substantial part of the budget near the known fold locations, but this does not prove that every order-optimal design must concentrate all its mass there. This formal calculation predicts the threshold but does not prove (1). The following lower and upper bounds do.

For `0<q<8/5`, the sharp coefficient, proved in the additional section below, is

\[
 2^{q-3}C_0^q
 \left[2B\left(\frac{1-\alpha_q}{2},\frac12\right)\right]^{1+q/4}.
 \tag{3}
\]

It reduces to the independently reviewed sharp coefficient when `q=1`. The additional proof below establishes `Φ_q(M)∼K_q M^(−q/4)` with `K_q` given by (3), using a sharp lower certificate and an integrable disorder envelope. The previously reviewed order bounds do not by themselves establish this coefficient.

At the threshold, the appended proof identifies the following coefficient multiplying `M^(−2/5)[log(1/M)]^(7/5)`, with its proof [independently verified](review-critical-risk-mobility.md):

\[
 K_{8/5}=\frac{(2C_0)^{8/5}}8
 \left(\frac47\right)^{7/5}.
\]

The coefficient reflects the truncated integral `∫|sin s|^(−1)ds∼4log(1/R)` and `log(1/R)∼log(1/M)/7`. The final section supplies the moving-arc lower bound and uniform upper matching needed to make this coefficient precise.

## A local budget lower bound for every positive moment

Consider one fold, centered at `s=0`, and root positions `u` in an interval `[r,3r/2]`, with `r` small. The corresponding offsets have probability density comparable to `r` with respect to `du`, hence total probability of order `r²`. On a fixed enlargement of this spatial interval, the local potential satisfies

\[
 k_c(s)=(\cos s-\cos u)^2\le C r^2(s-u)^2.
\]

Let `m` be the mobility mass in that enlarged interval, and assume `0<m≤c_1r^7`, with `c_1` fixed sufficiently small. Choose a fixed nonnegative compact smooth bump `ψ` with positive integral and let

\[
 \ell=\kappa(m/r^3)^{1/4},\qquad
 f_u(s)=\psi((s-u)/\ell),
\]

where the fixed `κ` is small enough that every support remains inside the enlarged interval. Write

\[
 B(u)=\ell^{-2}\int D(s)|\psi'((s-u)/\ell)|^2ds.
\]

The quotient form of the variational principle gives

\[
 J_c(D)^q\ge
 \frac{c_q\ell^{2q}}{[B(u)+Cr^2\ell^3]^q}.
\]

Averaging the moving bump over the root interval yields

\[
 \frac1r\int_r^{3r/2}B(u)du\le\frac{Cm}{r\ell}.
\]

Use Jensen's inequality on the convex function `x→(x+b)^(−q)`, valid for every `q>0`. The choice of width balances `m/(rℓ)` and `r²ℓ³`. After including the offset probability, this proves

\[
 \boxed{\mathbb E[J_c(D)^q;\ u\in[r,3r/2]]
 \ge c_q r^{2-5q/4}m^{-q/4}.}
 \tag{4}
\]

A zero local budget gives an infinite response for almost every offset with a zero in the interior of that interval, and is covered by a limit. Crucially, no smoothness or minimum feature size was assumed for `D`.

For `0<q<8/5`, choose one fixed regular root interval. Its mass is at most `M`, and the small-mass condition is automatic for sufficiently small `M`. Equation (4) immediately gives the lower bound `c_qM^(−q/4)`.

At `q=8/5`, use geometrically separated root intervals with radii `r_j=r_*4^(−j)`, each with a disjoint fixed spatial enlargement. Retain all radii above `C M^(1/7)`, so the small-mass condition follows from `m_j≤M`. There are `N` comparable to `log(1/M)` such intervals. Their parameter intervals are also disjoint. Since `2−5q/4=0`, summing (4) and using `Σm_j≤M` gives

\[
 \mathbb E[J_c(D)^{8/5}]
 \ge c\sum_{j=1}^Nm_j^{-2/5}
 \ge cN^{7/5}M^{-2/5}.
 \tag{5}
\]

This proves the critical logarithm uniformly over all designs.

## A fold lower bound for large moments

A simpler global-budget test gives the lower bound above the threshold. Let

\[
 R=M^{1/7}
\]

and use a fixed bump `f(s)=ψ(s/R)` centered on a fold. For offsets in a window `|t|≤cR²`, where `t=1−|c|`, the potential on the support is at most `CR⁴`. Therefore

\[
 \int D|f'|^2\le CM/R^2,\qquad
 \int k_cf^2\le CR^5,\qquad
 \int f\asymp R.
\]

Every admissible design consequently satisfies

\[
 J_c(D)\ge c\frac{R^2}{M/R^2+R^5}=cR^{-3}.
\]

The offset window has probability comparable to `R²`, hence

\[
 \mathbb E[J_c(D)^q]\ge c_qR^{2-3q}
 =c_qM^{(2-3q)/7}.
 \tag{6}
\]

For `q>8/5` this is the required lower bound. At the threshold it lacks the logarithm, which is supplied by the independent shell argument (5).

## Explicit graded designs attain all three orders

Let `r(s)` be the distance along the circle to the two fold sites `{0,π}`. For parameters `α,R`, define the normalized positive design

\[
 D_M(s)=A(r(s)+R)^{-\alpha},\qquad
 A=\frac{M}{\int_0^{2\pi}(r(s)+R)^{-\alpha}ds}.
 \tag{7}
\]

The corners can be smoothed without changing any of the following order bounds. This is one explicit admissible family, not a claim about the exact finite-budget optimizer.

Use `α=α_q` from (2), and choose

\[
 R=\begin{cases}
 M^{1/(6+\alpha)},&q<8/5,\\
 [M/\log(1/M)]^{1/7},&q=8/5,\\
 M^{1/7},&q>8/5.
 \end{cases}
 \tag{8}
\]

The normalization gives

\[
 A\asymp\begin{cases}
 M,&\alpha<1,\\
 M/\log(1/M),&\alpha=1,\\
 MR^{\alpha-1},&\alpha>1.
 \end{cases}
 \qquad A\asymp R^{\alpha+6}
 \tag{9}
\]

in each chosen regime. For `q>8/5`, any exponent `1<α<6−8/q` would suffice; the formal exponent lies strictly in this interval.

Here are uniform response bounds near either fold. Use `r=√|t|` as a parameter scale, with fixed factors absorbed into constants. On the side with two roots, for `r≥C R`,

\[
 J_c(D_M)\le C A^{-1/4}r^{-3/2+\alpha/4}.
 \tag{10}
\]

To obtain this, take neighborhoods of the two roots with radii proportional to `r`. On each, the mobility is comparable to `Ar^(−α)` and the potential is bounded below by a constant times `r²` times squared distance from the root. Neumann bracketing and the uniform interval oscillator bound give the displayed contribution. The remaining reciprocal-potential integral is `O(r^(−3))`, which is no greater than the displayed bound because `A` is comparable to `R^(α+6)` and `r≥CR`.

For the fold window `|t|≤CR²`,

\[
 J_c(D_M)\le CR^{-3}.
 \tag{11}
\]

Indeed, on an interval of radius a fixed multiple of `R`, the mobility is comparable to `AR^(−α)`, hence to `R⁶`. In the exact fold coordinate the potential is quartic with offset of order `R²`. Rescaling gives a uniformly coercive natural-endpoint problem of operator scale `R⁴` and integrated response scale `R^(−3)`. Choose the interval large enough that all roots in the retained parameter window lie strictly inside it. The reciprocal-potential integral outside is also `O(R^(−3))`.

On the side with no roots and `|t|≥CR²`, potential energy alone gives `J_c(D_M)≤C|t|^(−3/2)`. Away from the folds, the regular-root bound is `CA^(−1/4)`, and on fixed no-root parameter sets it is bounded.

Integrating (10) uses `dt` comparable to `r dr`. The potentially singular root contribution is

\[
 C A^{-q/4}\int_R^{r_*}
 r^{1-3q/2+\alpha q/4}dr.
 \tag{12}
\]

Put

\[
 e_q=2-3q/2+\alpha_q q/4
 =\frac{8-5q}{q+4}.
\]

For `q<8/5`, `e_q>0`, so (12) is `O(M^(−q/4))`. The fold and no-root contributions are smaller or bounded; equivalently, `R^(2−3q)/M^(−q/4)` is comparable to `R^(e_q)` when the fold term diverges.

At `q=8/5`, the integral in (12) is logarithmic. Equations (8)–(9) give

\[
 A^{-2/5}\log(1/R)
 \asymp M^{-2/5}[\log(1/M)]^{7/5}.
\]

The fold contribution is only `R^(−14/5)`, smaller by one logarithm.

For `q>8/5`, the integral is controlled by its lower endpoint. Using `A` comparable to `R^(α+6)` gives

\[
 A^{-q/4}R^{e_q}\asymp R^{2-3q}
 =M^{(2-3q)/7}.
\]

The fold and no-root contributions have at most the same order, and the regular-root contribution is smaller. These estimates prove all upper bounds in (1).

## What the result establishes and what remains open

The unrestricted optimum has the three orders in (1); the lower bounds explicitly prevent unaccounted improvements from microstructure. At the critical order, the logarithm arises because a growing number of spatial scales compete for the same mobility budget. A single fold patch misses that logarithmic cost. Above the threshold, a graded tail outside the fold patches regularizes the ordinary zeros without changing the leading order; a pure compact patch would leave a positive set of offsets with infinite response.

The exact leading constant is given by (3) below the threshold, with its proof independently reviewed. The appended section identifies the critical coefficient, with its proof independently reviewed. Above the threshold, identifying a canonical two-fold optimization problem would be needed to turn order bounds into a sharp equivalent. That supercritical sharp constant and a characterization of all limiting optimal profiles remain open. The order bounds do not force all mobility mass to concentrate: combining the graded trial for budget `M/2` with a uniform field of total mass `M/2` still attains the stated order by monotonicity. Claims about every near-minimizer would require a sharper result.

The scalar surface result has a finite-transverse-bulk extension at the level of moment orders: [the independent finite-bulk review](review-risk-sensitive-finite-bulk.md) supplies a logarithmic remainder bound for the graded trials and shows that it is smaller than every relevant moment scale. A fixed upper mobility cap, a minimum background, or an imposed fabrication scale can also change the admissible asymptotics.

Expected-moment or uncertainty-aware design, inverse-operator convexity, and fixed-budget reinforcement are established ideas. Relevant primary precedents include [Buttazzo, Oudet and Velichkov, *A free boundary problem arising in PDE optimization*](https://arxiv.org/abs/1506.00141) and [Jouve, Allaire and de Gournay, *Shape and topology optimization of the robust compliance via the level set method*](https://www.numdam.org/item/COCV_2008__14_1_43_0/). The candidate contribution is the design-induced `8/5` threshold and its critical logarithm for coalescing kinetic zeros. A [dedicated prior-art audit](risk-sensitive-prior-art.md) found no inspected source with this transition, while documenting broader precedents in risk measures, optimal conductivity, resource allocation, and rare bifurcations. That is a qualified novelty assessment, not proof that the result has never appeared.

## Sharp coefficient for every subcritical moment

This addition establishes the coefficient (3) for all `0<q<8/5`. It follows a suggestion from the parent to use a tangent of the inverse energy, which is convex for every positive `q`. The detailed calculation has passed [independent review](review-risk-sensitive-mobility.md).

Write

\[
 \beta=q/4,\qquad \alpha=\alpha_q,\qquad
 W_q(r)=|\sin r|^{1-3q/2}.
\]

Fix retained offsets in a compact symmetric subinterval of `(-1,1)`, with corresponding paired root arcs `E`. Define

\[
 Z_E=\int_E W_q^{1/(1+\beta)},\qquad
 d_E(r)=W_q(r)^{1/(1+\beta)}/Z_E,
\]

using the same smooth formula on slightly larger root neighborhoods. This is only a reference shape for the test functions; no restriction is placed on the actual design.

Choose a compact smooth real `ψ` with positive integral and set

\[
 I=\int\psi,\qquad T=\int|\psi'|^2,\qquad
 V_\psi=\int y^2\psi^2,\qquad Q=T+V_\psi,\qquad
 j_\psi=I^2/Q.
\]

For each retained offset, use the paired local fields from the first-moment proof, with

\[
 a(r)=\sin^2r,\qquad
 \ell_r=(Md_E(r)/a(r))^{1/4},\qquad
 h_r(s)=(Md_E(r)a(r))^{-1/2}\psi((s-r)/\ell_r).
\]

The two roots have the same `a,d_E`, so put

\[
 z_c=M^{-1/4}d_E(r)^{-1/4}a(r)^{-3/4}.
\]

Their combined source integral is exactly `2Iz_c`. Use the positive reference number `E_c^0=2Qz_c`; it is the quadratic local energy of the paired fields. It need not equal the energy of an actual global reference design. The true reaction contribution is `2V_ψz_c+o(z_c)`, uniformly over retained offsets.

For every positive `E`, convexity gives

\[
 E^{-q}\ge(E_c^0)^{-q}
 \left[1-q\frac{E-E_c^0}{E_c^0}\right].
\]

Apply this to the actual energy of the paired test field in the quotient lower bound for `J_c(D)^q`. The result is

\[
 J_c(D)^q\ge(2j_\psi)^qz_c^q
 \left[1+\frac{qT}{Q}
 -\frac{q}{2Qz_c}\int D|h_c'|^2+o(1)\right].
 \tag{13}
\]

The remainder comes only from the reaction Taylor expansion and is uniform on the retained arcs. It is independent of the actual mobility placement. A negative right-hand side causes no problem; this is a global supporting inequality.

Define

\[
 K_{\psi,E}=2^{q-3}j_\psi^qZ_E^{1+\beta}.
\]

The offset-to-root change of variables gives

\[
 \mathbb E[(2j_\psi)^qz_c^q;\ c\text{ retained}]
 =K_{\psi,E}M^{-\beta}.
\]

The factor of two from paired roots is essential: a function of either symmetric root averages as one half its marked integral over all root arcs. With root density `ρ(r)=|sin r|/4`, this identity is equivalent to

\[
 \frac{(2j_\psi)^q}{2}\int_E
 \rho(r)d_E(r)^{-\beta}a(r)^{-3q/4}dr
 =K_{\psi,E}.
\]

The weighted derivative density in (13) satisfies

\[
 \left\|\mathbb E\left[
 \frac{q(2j_\psi)^q}{2Q}z_c^{q-1}|h_c'|^2;
 c\text{ retained}\right]\right\|_\infty
 \le\left[\frac{qT}{Q}K_{\psi,E}+o(1)\right]M^{-1-\beta}.
 \tag{14}
\]

For completeness, the unweighted kernel has scale `M^(−5/4)ρd_E^(−5/4)a^(−3/4)`, as in the first-moment proof. Multiplying by `z_c^(q−1)` changes its scale to

\[
 M^{-1-\beta}\rho d_E^{-1-\beta}a^{-3q/4}.
\]

The root coefficients can be evaluated at the observation point with a uniform relative error of order `M^(1/4)`. The Jacobian in the moving-root kernel contributes the integral `T`. The spatial factor is constant because

\[
 \rho d_E^{-1-\beta}a^{-3q/4}
 =\tfrac14W_qd_E^{-1-\beta}
 =\tfrac14Z_E^{1+\beta}.
\]

Substituting the prefactor gives precisely (14). The root-arc edges truncate a nonnegative kernel and cannot increase its bound, so the estimate remains uniform in the observation point, even for a highly concentrated actual design.

Average (13), use `∫D=M`, and apply (14). The constant and derivative terms cancel their `qT/Q` factors exactly:

\[
 \liminf_{M\downarrow0}M^\beta\Phi_q(M)
 \ge K_{\psi,E}.
 \tag{15}
\]

This cancellation holds for every compact test function. No exact virial identity or equality of source and energy for an approximate oscillator field is needed. The oscillator quotient supremum is `sup_ψ j_ψ=C_0`. Taking that supremum, then expanding the retained offset interval to `(-1,1)`, proves the lower bound with coefficient (3), because `Z_E` converges to the finite integral of `|sin r|^(−α)` when `q<8/5`.

For a matching upper bound, use the normalized positive regularizations

\[
 d_M(s)=\frac{(|\sin s|+R)^{-\alpha}}
 {\int_0^{2\pi}(|\sin v|+R)^{-\alpha}dv},\qquad
 D_M=M d_M,\qquad R=M^{1/(6+\alpha)}.
 \tag{16}
\]

For every fixed offset with simple zeros, these shapes converge smoothly in root neighborhoods to the normalized shape in (2). Quadratic localization therefore gives the paired-root limit used in the formal calculation. For fixed offsets without zeros, `M^βJ_c(D_M)^q→0`.

The earlier graded estimates apply equally to `|sin s|+R`, which is comparable to `r(s)+R`. They give the uniform integrable envelope

\[
 M^\beta J_c(D_M)^q\le C|t|^{-\gamma_q},
 \qquad \gamma_q=\frac{3q}{4}-\frac{\alpha q}{8}
 =\frac{7q}{2(q+4)}<1,
 \tag{17}
\]

near each fold, on both sides, with an immaterial exclusion of the single point `t=0`.

On the root side with `|t|≥CR²`, (17) follows directly from (10). In the central fold window, (11) and `M` comparable to `R^(6+α)` bound the normalized response by `CR^(−2γ_q)`, which is no greater than a constant times `|t|^(−γ_q)`. On the no-root side outside that window, `J≤C|t|^(−3/2)` and `M≤C|t|^((6+α)/2)` give the same envelope. Away from the folds all normalized responses are uniformly bounded. Thus dominated convergence is justified, including when `q≥4/3` and the constant-mobility envelope would have failed.

The limiting integral is exactly (3). Combining it with (15) establishes

\[
 \boxed{\Phi_q(M)\sim
 2^{q-3}C_0^q
 \left[2B\left(\frac{1-\alpha_q}{2},\frac12\right)\right]^{1+q/4}
 M^{-q/4},\qquad0<q<8/5.}
 \tag{18}
\]

The normalized shapes (16) attain this sharp equivalent. The result does not assert convergence of every optimizing design to that profile or identify the exact finite-budget optimizer.

## Sharp critical coefficient

The moving-arc version of the same certificate also identifies the critical coefficient. The argument in this section has passed [independent review](review-critical-risk-mobility.md). Set

\[
 q_*=8/5,\qquad \beta_*=q_*/4=2/5,\qquad
 A_*=\frac{(2C_0)^{8/5}}8.
\]

Then

\[
 \boxed{\Phi_{8/5}(M)\sim
 A_*\left(\frac47\right)^{7/5}
 M^{-2/5}[\log(1/M)]^{7/5}.}
 \tag{19}
\]

The dimensionless leading coefficient is approximately `2.02233076396939`.

### Lower bound with root arcs approaching the folds

Fix `0<b<1/7` and put `r_min=M^b`. Retain the offsets `|c|≤cos(r_min)`, so their root arcs `E_M` exclude radius-`r_min` neighborhoods of both fold sites. At the critical order,

\[
 W_{q_*}^{1/(1+\beta_*)}=|\sin r|^{-1},\qquad
 Z_{E_M}=\int_{E_M}|\sin r|^{-1}dr
 =4b\log(1/M)+O(1).
\]

Use the compact-test construction of (13)–(15) with

\[
 d_{E_M}(r)=\frac1{Z_{E_M}|\sin r|},\qquad
 \ell_r=\left[\frac{M}{Z_{E_M}|\sin r|^3}\right]^{1/4}.
\]

The estimates previously obtained on fixed root arcs now remain uniform because

\[
 \varepsilon_M:=\sup_{r\in E_M}
 \frac{\ell_r}{\operatorname{dist}(r,\{0,\pi\})}
 \le C\left[\frac{M}{Z_{E_M}r_{\min}^7}\right]^{1/4}
 \longrightarrow0.
 \tag{20}
\]

Here distance is periodic. For every fixed compact test function, its support is contained in a root neighborhood of relative radius `O(ε_M)`. The two roots remain separated. On such a neighborhood the potential differs from `a(r)(s−r)²` by a relative `O(ε_M)` in the energy integral: near a fold, the cubic Taylor coefficient is of order `r`, while the quadratic coefficient is of order `r²`. Thus the ratio is controlled by `ℓ_r/r`.

All logarithmic derivatives of the kernel coefficients, including `ℓ_r`, are `O(1/r)` near a fold. Their variation over a test support and the relative error in the moving-root Jacobian are therefore also `O(ε_M)`. The same bound holds when the observation point is just beyond an arc edge, since its distance to that edge is only `O(ℓ_r)`. The truncated-kernel argument remains valid. Consequently, both sides of the cancellation in (15) have relative error tending to zero, even though `Z_{E_M}` now diverges logarithmically.

It follows for each fixed compact test that

\[
 \Phi_{q_*}(M)\ge
 [1+o(1)] 2^{q_*-3}j_\psi^{q_*}
 Z_{E_M}^{7/5}M^{-2/5}.
\]

Divide by `M^(−2/5)[log(1/M)]^(7/5)`, take `j_ψ→C_0`, and then let `b↑1/7`. This gives the lower coefficient in (19). The two limiting choices are made after the small-budget limit, so no uncontrolled simultaneous cutoff of the oscillator test is needed.

### Upper bound and uniform separated-root matching

Let

\[
 L=\log(1/M),\qquad R=(M/L)^{1/7},\qquad
 Z_R=\int_0^{2\pi}\frac{ds}{|\sin s|+R},\qquad
 D_M(s)=\frac{A}{|\sin s|+R},\qquad A=M/Z_R.
\]

Then

\[
 Z_R=4\log(1/R)+O(1)\sim\frac47L,
 \qquad A\sim\frac74R^7.
 \tag{21}
\]

The bounded term in `Z_R` follows by comparing `sin s` with `s` near each side of each fold. The factor `7/4` in `A/R^7` must not be set to one, but it does not change the leading logarithmic constant.

Retain offsets whose nearest root-to-fold distance is at least

\[
 r_0=RL.
\]

For all these offsets, including those approaching a fold, one has the uniform equivalent

\[
 J_c(D_M)=[1+o(1)] 2C_0A^{-1/4}
 (1-c^2)^{-5/8}.
 \tag{22}
\]

To justify uniformity, write `r=arccos|c|`, so `r≥r_0` and `|sin r|` is comparable to the distance to the nearest fold. Use root neighborhoods of radius `η sin r` with `η=L^(−1/2)`. On each neighborhood, the mobility differs from `A/sin r` by a relative `O(η+R/r)`, and the kinetic potential differs from its quadratic approximation by `O(η)`. Both errors tend to zero uniformly. The local oscillator width divided by root-to-fold distance is at most

\[
 C(A/r_0^7)^{1/4}=O(L^{-7/4}).
\]

The neighborhoods therefore have oscillator-scaled half-length at least of order `L^(5/4)`, tending uniformly to infinity. Dirichlet and Neumann oscillator integrals converge to `C_0` on these expanding intervals. The reciprocal-potential bound on the complement is at most `C/(η r³)`. Relative to the root contribution `A^(−1/4)r^(−5/4)`, this is at most

\[
 C\eta^{-1}(A/r_0^7)^{1/4}=O(L^{-5/4})\to0.
\]

These estimates prove (22), using the same bracketing argument on every retained offset.

At `q=q_*`, integration of (22) yields

\[
 \mathbb E[J_c(D_M)^{q_*};\ |c|\le\cos r_0]
 \sim A_*A^{-2/5}\int_{E(r_0)}\frac{ds}{|\sin s|}
 \sim4A_*A^{-2/5}\log(1/R).
 \tag{23}
\]

Here `log(1/r_0)=log(1/R)−log L∼log(1/R)`, and `E(r_0)` excludes the two fold neighborhoods.

The omitted root annuli `CR<r<r_0` satisfy the earlier uniform order bound. Their integrated contribution is `O(A^(−2/5)log L)`. The central fold windows have width `O(R²)` and response `O(R^(−3))`, giving `O(R^(−14/5))=O(A^(−2/5))`. On the side without roots, integrating the reciprocal-potential bound from offset distance `R²` outward gives the same order. The remaining no-root parameter sets contribute only a bounded amount. All of these terms are smaller than (23), since `log L=o(L)`.

Finally, combine `A=M/Z_R`, `Z_R∼4log(1/R)`, and `log(1/R)∼L/7` in (23). The resulting coefficient is exactly `A_*(4/7)^(7/5)`, which matches the lower bound and proves (19).

This coefficient concerns the optimum value. It does not characterize every optimizer, prove that all its mobility mass concentrates, or identify a unique critical profile at finite budget. The supercritical sharp constant remains a separate open problem.
