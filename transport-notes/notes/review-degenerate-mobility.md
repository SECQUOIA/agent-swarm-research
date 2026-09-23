# Independent review: coincident mobility and desorption zeros

Reviewed 2026-09-06 by an agent independent of the derivation. The threshold and the quadratic-mobility crossover coefficient pass analytical review. An independent boundary-value calculation also confirms the coefficient. This review establishes correctness under the assumptions below; it does not establish novelty.

## Precise interpretation and assumptions

Take a finite one-dimensional wall, with reflecting endpoints or periodic geometry, and the closed reversible form

\[
\mathcal E[u]=\int \{D(s)|u'(s)|^2+k(s)|u(s)|^2\}\,ds.
\]

Use the closure of the smooth functions appropriate to that geometry, including constants; do not silently impose absorption at a mobility zero. Suppose there are finitely many isolated common zeros, all positive-mobility regions have nonzero killing somewhere, and near each common zero

\[
D(s)\asymp d|s|^n,\qquad k(s)\asymp a|s|^2,
\qquad a,d>0,\ n\geq0.
\]

Here `d=εb`. Coefficients should be regular and strictly positive away from their stated zeros. The finiteness criterion needs only two-sided comparability; the exact coefficient below needs asymptotic equality.

Define the integrated lifetime by the extended quadratic form

\[
J=\int_0^\infty\langle1,e^{-tH}1\rangle\,dt
=\|H^{-1/2}1\|_2^2
=\sup_u\{2\!\int u\,ds-\mathcal E[u]\}.
\tag{1}
\]

It is allowed to be infinite. For normalized uniform initial data the mean lifetime is `J/L`, where `L` is wall length. Formula (1), rather than an ordinary operator inverse, is essential: for `5/2≤n<3`, `J` is finite although the formal function `H^{-1}1` is not in `L²`. The notation `〈1,H^{-1}1〉` can be retained only if this extended meaning is stated.

## Threshold proof

On a one-sided neighborhood `(0,r)`, integrate a smooth test function by parts:

\[
\int_0^r u(x)\,dx=r u(r)-\int_0^r x u'(x)\,dx.
\]

The derivative term obeys

\[
\left|\int_0^r x u'\,dx\right|^2
\leq \left(\int_0^r D|u'|^2dx\right)
\left(\int_0^r \frac{x^2}{D(x)}dx\right).
\]

The second factor is finite exactly when `n<3`. A trace estimate on a fixed annulus away from zero, where `D` and `k` are positive, controls `u(r)` by the total form energy. Applying this on each side and controlling the remainder directly with killing proves `|∫u|²≤C E[u]`. Extend from the smooth form core by continuity. The variational formula then gives `J<∞`.

For the converse, choose a nonnegative smooth bump `φ` supported in `(1,2)` and set `φ_r(x)=φ(x/r)`. Then

\[
\int\phi_r\asymp r,\qquad
\mathcal E[\phi_r]\asymp d r^{n-1}+a r^3.
\]

If `n>3`, the ratio `(∫φ_r)²/E[φ_r]` tends to infinity as `r→0`, proving `J=∞`. At `n=3` the ratio remains bounded below by a positive constant. Choose disjoint dyadic annuli and optimize the amplitude of the bump in each annulus. Energies add without cross terms, and each annulus supplies a fixed positive amount to the variational supremum. Summing arbitrarily many annuli proves divergence, logarithmic in the spatial cutoff.

Thus, for a quadratic reaction zero and fixed positive `d`,

\[
\boxed{J<\infty\quad\Longleftrightarrow\quad n<3.}
\tag{2}
\]

A positive mobility amplitude does not guarantee finite mean lifetime if the mobility itself has a sufficiently strong zero.

For exact powers and `2<n<4`, the local mean-lifetime solution has leading behavior

\[
u(x)\sim\frac{x^{2-n}}{d(n-2)}.
\tag{3}
\]

Indeed, `−(d x^n u')'=1` to leading order, while `a x²u→0`. In particular `n=3` gives `u∼1/(d x)` and a logarithmic integral. Formula (3) also gives the `L²` threshold `n<5/2`. At `n=2`, `u∼d^{-1}\log(1/x)`; at `n=4`, `u∼[(a+2d)x²]^{-1}`; for `n>4`, reaction dominates and `u∼1/(a x²)`. These local formulas require enough coefficient regularity to justify asymptotic differentiation and are unnecessary for the comparability proof of (2).

## Exact quadratic-mobility crossover

Consider the local whole-line model

\[
H=-d\partial_x(x^2\partial_x)+a x^2+\delta,
\qquad d,a>0,\quad\delta\geq0.
\]

Set `y=x√(a/d)`, `ζ=δ/d`. Then

\[
J=(ad)^{-1/2}C_2(\zeta),\qquad
C_2(\zeta)=\int_{\mathbb R}v(y)\,dy,
\]

where

\[
-(y^2v')'+(y^2+\zeta)v=1.
\]

The natural realization splits the whole line into its two half-lines, and the forcing is symmetric. On `y>0`, substitute `w=yv`. The equation becomes

\[
-w''+\left(1+\frac\zeta{y^2}\right)w=\frac1y.
\tag{4}
\]

The natural solution corresponds to the Friedrichs realization of the inverse-square Schrödinger operator in (4). Let `ν=√(1/4+ζ)`. The generalized eigenfunctions of `−∂²_y+ζ/y²` are `√(py)J_ν(py)`, with eigenvalue `p²` and delta-function normalization in `p`. The transform of the source is independent of `p`:

\[
A_\nu=\int_0^\infty\frac{\sqrt{py}J_\nu(py)}y\,dy
=\int_0^\infty t^{-1/2}J_\nu(t)\,dt
=\frac1{\sqrt2}
\frac{\Gamma(\nu/2+1/4)}{\Gamma(\nu/2+3/4)}.
\]

The last equality is the classical Bessel Mellin integral, [DLMF 10.22.43](https://dlmf.nist.gov/10.22.E43). Regularizing the source at zero and infinity justifies spectral manipulations with this non-`L²` source. The resulting finite energy pairing is

\[
\int_0^\infty\frac{w(y)}y\,dy
=A_\nu^2\int_0^\infty\frac{dp}{1+p^2}
=\frac\pi2 A_\nu^2.
\]

Doubling for the two half-lines yields

\[
\boxed{C_2(\zeta)=\frac\pi2
\left[\frac{\Gamma(\nu/2+1/4)}{\Gamma(\nu/2+3/4)}\right]^2,
\qquad\nu=\sqrt{\tfrac14+\zeta}.}
\tag{5}
\]

At `ζ=0`, `ν=1/2`, so `C₂(0)=π²/2`. This can also be checked without general Bessel functions: (4) reduces to `−w''+w=1/y` with the Dirichlet realization at zero. The sine transform of `1/y` equals `π/2`, giving the one-sided energy `π²/4`.

At large `ζ`, the gamma ratio gives `C₂(ζ)∼π/√ζ`; thus `J∼π/√(aδ)`, precisely the integral of the local no-diffusion lifetime `1/(a x²+δ)`.

For a compact wall, (5) is a leading local asymptotic, not a globally exact formula. For one symmetric quadratic zero take `d→0`, `δ=dζ`, fixed `ζ≥0`, and uniform local coefficient comparisons as specified in the localization argument below. A one-sided endpoint contributes half of (5). Multiple isolated zeros contribute their respective one-sided terms; unequal coefficients on opposite sides require the appropriate separate prefactors and scaled floors. Claims uniform over unbounded `ζ` need additional control of the scale `√(δ/a)` and cannot follow from the fixed-`ζ` inner limit alone.

### Compact-wall localization proof for a fixed scaled floor

Here are sufficient precise assumptions for the preceding asymptotic. Near the sole zero let `D_d(s)=d s²[1+o(1)]` and `k_d(s)=dζ+a s²[1+o(1)]`, with the relative remainders uniform for small `d`; outside each fixed neighborhood of zero assume a positive lower bound on `k_d` independent of small `d`. Choose a fixed small radius `r` such that the local relative errors are below `η`, and smooth cutoffs `χ²+ξ²=1`, with `χ=1` near zero and supported inside `|s|<r`. The form localization identity is

\[
Q_d[u]=Q_d[\chi u]+Q_d[\xi u]
-\int D_d(\chi^{\prime2}+\xi^{\prime2})u^2ds.
\]

At fixed `r`, the last integrand is supported on a nondegenerate annulus and is bounded by `O_r(d) k_d u²`. Therefore

\[
Q_d[u]\geq[1-O_r(d)]\{Q_d[\chi u]+Q_d[\xi u]\}.
\]

Split the linear functional exactly as `∫u=∫χ(χu)+∫ξ(ξu)`, and enlarge the variational supremum by allowing its two localized arguments to vary independently. The outer supremum is `O_r(1)`, because killing there is bounded below. Extend the inner argument by zero to the whole line. Its energy is at least `(1−η)` times the exact quadratic local-model energy. Since `0≤χ≤1`, replacing an arbitrary test function by its absolute value bounds its source pairing by the full constant-source pairing. Thus

\[
\limsup_{d\downarrow0}\sqrt{ad}\,J_d
\leq\frac{C_2(\zeta)}{1-\eta}.
\]

For the lower bound, insert any smooth compactly supported test function of the scaled coordinate `y=s√(a/d)` into the global variational formula, with amplitude `d^{-1}`. Uniform coefficient convergence gives the exact local energy functional after multiplying by `√(ad)`. Taking the supremum over local test functions gives `liminf √(ad)J_d≥C₂(ζ)`. Finally let `η→0`. This proves `√(ad)J_d→C₂(ζ)` under these assumptions. For multiple zeros, use disjoint inner cutoffs and the same argument. The proof does not claim an error rate or uniformity for `ζ→∞`.

## Independent numerical check

A boundary-value solver was applied to a different representation from the Hankel derivation. Set `y=eᵗ`, `v=e^{-t/2}ψ(t)`. Then

\[
-\psi''+(\tfrac14+\zeta+e^{2t})\psi=e^{t/2},
\qquad C_2=2\int_{-\infty}^{\infty}e^{t/2}\psi(t)\,dt.
\]

The computation used SciPy `solve_bvp` on `[-32,14]`, left Dirichlet value zero, right value `e^{-21}`, solver tolerance `10^{-9}`, and Simpson quadrature on 30,000 points. The omitted right tail was included as its leading value `2e^{-14}`. This endpoint approximation is adequate at the displayed precision; it is not asserted to be an exact boundary condition.

| `ζ` | Boundary-value integral | Formula (5) | Relative difference |
| ---: | ---: | ---: | ---: |
| 0 | 4.934802200519241 | 4.934802200544678 | 5.2×10⁻¹² |
| 0.01 | 4.867914613323569 | 4.867914613341871 | 3.8×10⁻¹² |
| 0.1 | 4.374481906235506 | 4.374481906237051 | 3.5×10⁻¹³ |
| 1 | 2.605941085094926 | 2.605941085092840 | 8.0×10⁻¹³ |
| 10 | 0.9699899167692415 | 0.9699899167685436 | 7.2×10⁻¹³ |
| 100 | 0.3133787024326066 | 0.3133787024336896 | 3.5×10⁻¹² |

All six solves converged, using 7,226–7,647 adaptive nodes. This is a consistency check; the analytical derivation supplies the correctness argument.

## Boundary classification and initial laws

For `L f=(D f')'`, scale density is `1/D` and speed density is constant. A one-sided zero has finite resistance `∫₀ dx/D` exactly when `n<1`. With the stated closure of globally smooth functions, this gives a transmitting interface. For `n≥1`, the resistance is infinite, the point has zero capacity, and the canonical form imposes no matching of traces through it. The one-sided scale boundary is inaccessible from the interior; it is entrance type for `1≤n<2` and natural type for `n≥2`, since the remaining classification integral scales as `∫₀x^{1-n}dx`.

Geometry matters. An interior zero on an interval separates two invariant components. One zero on a circle does **not** separate the remaining state space: the circle with that point removed is a connected interval, whose two endpoints are inaccessible. At least two barrier zeros are needed to split the positive-mobility region of a circle into multiple components.

Uniform Lebesgue measure is invariant for the *unkilled* reversible motion. On each invariant component, normalized Lebesgue measure is stationary, and arbitrary mixtures of those component laws are stationary. A killed motion has no nontrivial stationary probability law of this kind. Any use of a stationary wall law in a bulk/surface model must be checked against the full coupled dynamics.

The `L²(ds)` Dirichlet form does not specify the law of a particle initialized at an isolated zero-capacity point. An absorbing extension there would give an infinite lifetime when `δ=0`, and lifetime `1/δ` when `δ>0`. Such atomic initial data are distinct from uniform initial data and require an explicit state-space/Markov-extension convention. In particular, neither (2) nor (5) is a statement about an atom initially placed exactly at the common zero.

## Scope beyond the quadratic zero

The same variational proof establishes a useful broader **finiteness criterion**, without needing a new special-function calculation. In one dimension, with `k∼a|x|^m`, `D∼d|x|^n`, `m,n≥0`, isolated zeros, and uniform source and initial measure,

\[
J<\infty\quad\Longleftrightarrow\quad m<1\ \hbox{or}\ n<3.
\]

If `m<1`, apply Cauchy–Schwarz directly with `∫1/k<∞`. If `n<3`, use the derivative argument above. If both inequalities fail, disjoint annular bumps give divergence, including the equality cases. This claim concerns finiteness only: small-`d` exponents, constants, and floor crossovers still depend on `m` and `n`.

Different source or initial densities change the criterion. For example, when `2<n<4` and an initial density behaves like `|x|^p`, equation (3) shows that its mean lifetime is finite near zero exactly when `p>n-3`, subject to an integrable initial density (`p>−1`). One should therefore state the initial measure whenever calling `n=3` a universal threshold.

## Review disposition

The proposed `n=3` mean-lifetime threshold and formula (5) are correct in the stated natural realization. Required qualifications are the extended-inverse interpretation, explicit initial measure, compact-wall asymptotic versus whole-line exactness, and geometry-dependent component structure. Classical inverse-square spectral theory and weighted Hardy-type estimates underlie the calculations; publication claims require a separate literature audit of the transport consequence.

## Follow-up review: general zero-floor coefficient

A second independent audit, requested after the initial review, checked the general coefficient in Eq. (15) of [the derivation note](degenerate-surface-mobility.md). It passes, including `0≤n<1` with the explicitly stated non-Friedrichs transformed boundary condition.

Write `d=m+2−n`, `r=(m−1)/d`, `q=d/2`, `ν=(n−1)/d`, and `β=−1/2−r`. For `m>1`, `0≤n<3`, we have `0<r<1` and `ν>−1/2`. The original-variable fundamental solution

\[
x^{(1-n)/2}I_\nu(x^q/q)
\]

approaches a constant with zero weighted flux at zero for either sign of `ν`: the power from `I_ν` exactly cancels the prefactor. Its first correction has exponent `d`, whose weighted derivative vanishes as `x^{m+1}`. The weighted Wronskian with the `K_ν` solution is `−q`, confirming the Green-function normalization.

For `n<1`, the full-line forcing is even and the symmetric solution is the half-line zero-flux solution. The signed-order mode has transformed exponent `1/2+ν<1/2`. Replacing `ν` by `|ν|` would instead impose the wrong original-variable boundary condition. The derivation correctly preserves the signed order and warns against dropping the transformed boundary term.

The transform is the classical Hankel transform with kernel `√(κt)J_ν(κt)`; see [DLMF §10.22(v)](https://dlmf.nist.gov/10.22#v). The present order range is within its usual inversion regime. The source Mellin integral has exponent `ν+β+1/2=(n−m)/d>−1` at zero, and has a convergent oscillatory tail at infinity. Its gamma arguments reduce exactly to `1/d` and `m/d`. The remaining spectral integral is

\[
\int_0^\infty\frac{\kappa^{2r-1}}{1+\kappa^2}d\kappa
=\frac\pi{2\sin\pi r}.
\]

The factors from coordinate scaling, the squared Mellin coefficient, and the two half-lines therefore give

\[
\boxed{C_{m,n}(0)=2\pi d^{-1-2r}\csc(\pi r)
\left[\frac{\Gamma(1/d)}{\Gamma(m/d)}\right]^2.}
\]

No extra discrete mode is required for this scale-invariant nonnegative Bessel realization. The original positive `I_νK_ν` Green function also identifies the chosen resolvent directly, avoiding an ambiguous formal energy transformation.

### Independent original-coordinate checks for the negative-order cases

I solved `h″=x^{m−n}h−x^{-n}−nh′/x` using SciPy `solve_bvp` on `10⁻⁴≤x≤10`. The left condition was the natural local expansion `h′(ε)=−ε^{1−n}`. The right condition used

\[
h(R)=R^{-m}+m(m+1-n)R^{n-2m-2}.
\]

The integral includes the corresponding two-term outer tail and the leading omitted left interval `εh(ε)`. Solver tolerance was `10⁻⁶`; every displayed solve converged, with 500–551 nodes. Simpson quadrature used 20,000 logarithmically spaced points.

| m | n | Numerical full-line integral | Gamma formula | Relative difference |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 0 | 4.6474759617 | 4.6474760094 | 1.0×10⁻⁸ |
| 2 | 0.5 | 4.5816393487 | 4.5816398156 | 1.0×10⁻⁷ |
| 3 | 0 | 3.4650620497 | 3.4650620588 | 2.6×10⁻⁹ |
| 3 | 0.5 | 3.4247592808 | 3.4247592744 | 1.9×10⁻⁹ |
| 4 | 0 | 2.9491719866 | 2.9491719847 | 6.2×10⁻¹⁰ |
| 4 | 0.5 | 2.9331051175 | 2.9331051257 | 2.8×10⁻⁹ |

These are independent consistency checks of the delicate negative-order branch, not error-certified evaluations. Earlier attempts at tighter solver tolerance and a larger interval produced close values but did not converge within the adaptive-node budget; they are not counted as verified numerical evidence.

## Follow-up review: quadratic-mobility finite-bulk remainder

The logarithmic supersolution and the resulting bounded finite-bulk correction in the final subsection of the derivation note pass independent review under the stated fixed `C²` profile assumptions, quadratic coincident zeros, and fixed positive bulk diffusivity.

For `c=eb`, let `Q=(2c)^{-1}log(1+c/(as²))` and `z=as²/c`. Direct differentiation gives

\[
c sQ'=-\frac1{1+z},\qquad
c s^2Q''=\frac{1+3z}{(1+z)^2}\le\frac98.
\]

The proposed expression for `H_0Q` is correct. Its rational lower bound is at least `1/5`: after multiplication by its positive denominator, the required polynomial is `3z³−5z²+6z+4`, positive for `z≥0` because its derivative `9z²−10z+6` is strictly positive. Also `as²Q≤1/2`.

The coefficient-error argument is uniform in small `e`. In particular, `d_0−bs²=o(s²)` multiplies `eQ″`, `d_0′−2bs=o(s)` multiplies `eQ′`, and `k_0−as²=o(s²)` multiplies `Q`. The three displayed bounds control these products uniformly. A fixed sufficiently small neighborhood therefore preserves a positive supersolution margin.

A fixed cutoff has transition region separated from zero; there `Q,Q′,Q″` remain bounded as `e→0`, and killing is bounded below. Adding a sufficiently large constant handles the transition error and the rest of the wall. At the zero, `D_eQ′=O(s)` tends to zero, so the weak divergence has no delta source. The logarithm belongs to `L²` and to the natural energy domain for every fixed `e>0`. The comparison argument is legitimate.

Consequently `||k_0h_0||∞≤C`. Positivity and the constant supersolution for a positive floor give `h_δ≤h_0` and `δh_δ≤1`, hence

\[
\|k_\delta h_\delta\|_\infty\le C+1
\]

uniformly for small `e` and every `δ≥0`. Testing the Poisson equation against 1 gives `∫k_δh_δ=P`, so the residual bulk source annihilates constants exactly.

I also checked the connection to the existing finite-bulk Schur identity. The surface boundary form is nonnegative because it is the minimum of `∫D_e|w′|²+∫k_δ(w-f_Γ)²`. Its removal can only increase the variational remainder. On mean-zero bulk functions, fixed-domain Poincaré and trace bounds give `|L(f)|≤C||∇f||₂`, with `C` uniform by the preceding bound on `k_δh_δ`. Thus

\[
0\le D_{\rm flow}-\frac{KV^2}{Z}J
\le\frac{C^2}{ZD_b}=O(1).
\]

This confirms preservation of the leading compact-wall quadratic-mobility crossover at finite transverse bulk diffusivity. It does not supply a uniform limit when `D_b→0`, or extend the bounded remainder to arbitrary `n<3`.

The compact-floor uniformity added to the localization proof also passes: continuity of the finite local resolvent functional, together with the same upper/lower bounds along convergent sequences of scaled floors, suffices for uniformity on compact subsets of `[0,∞)`.
