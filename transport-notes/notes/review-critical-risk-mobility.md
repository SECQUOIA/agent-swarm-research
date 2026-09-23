# Independent review of the sharp critical disorder moment

Reviewed 2026-09-07 by `review_traveling_channel`, at the request of `review_optimal_placement`.

The critical coefficient in equations (19)–(23) of [risk-sensitive-mobility.md](risk-sensitive-mobility.md) is correct for the stated scalar variational problem. Independent examination confirms the moving-root lower certificate, the uniform separated-root upper asymptotic, the probability factors, and the negligible omitted regions. No mathematical correction to the coefficient is needed.

With the same mobility field chosen before observing `c`, the result is

\[
\inf_{D\ge0,\,\int_0^{2\pi}D=M}
\mathbb E[J_c(D)^{8/5}]
\sim
\frac{(2C_0)^{8/5}}8
\left(\frac47\right)^{7/5}
M^{-2/5}[\log(1/M)]^{7/5},
\]

where `c` is uniform on `[-2,2]`, `k_c(s)=(c+cos s)²`, and `C₀` is the integrated unit-oscillator response used in the source note. This review does not establish literature novelty, a finite-bulk extension, or a characterization of all optimizing designs.

## Lower certificate on moving root arcs

At `q=8/5`, write `β=2/5`. The formal local weight is

\[
W(r)=|\sin r|^{-7/5},\qquad
W(r)^{1/(1+\beta)}=|\sin r|^{-1}.
\]

Retain all roots at periodic distance at least `r_min=Mᵇ` from `{0,π}`, with fixed `0<b<1/7`. The retained integral and reference shape are

\[
Z_E=4b\log(1/M)+O(1),\qquad
d_E(r)=\frac1{Z_E|\sin r|}.
\]

There are four one-sided approaches to fold points on the circle; each contributes one logarithm. This confirms the factor four.

For each fixed compact smooth oscillator test, the test width is

\[
\ell_r=\left(\frac{M}{Z_E|\sin r|^3}\right)^{1/4}.
\]

Consequently

\[
\sup_{r\in E}\frac{\ell_r}{\operatorname{dist}(r,\{0,\pi\})}
\le C\left(\frac{M}{Z_Er_{\min}^7}\right)^{1/4}
=O\left(M^{(1-7b)/4}[\log(1/M)]^{-1/4}\right)\to0.
\tag{1}
\]

This single small parameter controls both errors needed for the lower certificate:

- Taylor expansion gives `(cos s−cos r)²=sin²r(s−r)²[1+O(ℓ_r/r)]` on the test support near a fold. In particular, the reaction-energy error is relative and uniform over the retained offsets.
- The logarithmic derivatives of the reference amplitude, test width, root density, and powers of the local response are `O(1/r)`. In the moving-root integration, putting `y=(s−r)/ℓ_r` gives Jacobian denominator `1+yℓ'_r=1+O(ℓ_r/r)`. Thus the weighted derivative kernel is its frozen-coefficient value times `1+o(1)`, uniformly in the observation point.

For a point just outside a retained arc, a nonzero kernel requires distance `O(ℓ_r)` from an arc endpoint. It is therefore still separated from the fold by a quantity comparable to `r_min`. Extending the reference formula there is legitimate. Restricting the root integral only removes part of a nonnegative kernel, so an arc edge cannot increase its upper bound. This checks the boundary issue that could otherwise invalidate the argument for highly concentrated competitors.

Let `j_ψ` be the oscillator quotient of the fixed compact test and let `K_(ψ,E)=2^(q−3)j_ψ^q Z_E^(7/5)`. The supporting-line calculation then yields

\[
\mathbb E[J_c(D)^q]\ge
K_{\psi,E}M^{-2/5}
\left[1+\frac{qT}{Q}-\frac{qT}{Q}+o(1)\right].
\]

The two canceled terms have errors relative to `K_(ψ,E)M^(−2/5)`. The logarithmic growth of `Z_E` therefore does not leave an uncontrolled absolute error. The derivative term uses only `∫D=M`, so the estimate is uniform over all nonnegative integrable competing fields, including budget-dependent concentration and oscillation.

Take the small-budget limit first, then the compact-test quotient supremum `j_ψ→C₀`, and finally `b↑1/7`. The resulting lower coefficient is

\[
2^{8/5-3}C_0^{8/5}(4/7)^{7/5}
=\frac{(2C_0)^{8/5}}8(4/7)^{7/5}.
\]

The order of limits in the source note is sufficient. There is no need to choose a budget-dependent oscillator cutoff.

## Upper normalization and the local response

Write `H=log(1/M)` to distinguish this logarithm from a spatial period, and choose

\[
R=(M/H)^{1/7},\quad
Z_R=\int_0^{2\pi}\frac{ds}{|\sin s|+R},\quad
A=M/Z_R,\quad D_M(s)=\frac A{|\sin s|+R}.
\]

Direct integration near the four one-sided fold neighborhoods gives

\[
Z_R=4\log(1/R)+O(1)\sim\frac47H,
\qquad \frac A{R^7}=\frac H{Z_R}\to\frac74.
\tag{2}
\]

Thus the source note correctly retains the nonunit factor in `A/R⁷`.

Retain root distances `r≥r₀=RH`, and let `η=H^(−1/2)`. Around each root use an interval of half-length `η sin r`. The mobility is `A/sin r` times `1+O(η+R/r)`, and the potential is its local quadratic form times `1+O(η)`. These errors tend uniformly to zero, including the smallest retained roots.

The local oscillator width obeys

\[
\frac{\ell_r}{r}\le C(A/r_0^7)^{1/4}=O(H^{-7/4}).
\]

The retained neighborhoods thus have oscillator-scaled half-length at least a constant times `H^(5/4)`, tending uniformly to infinity. The Dirichlet and Neumann oscillator responses both approach `C₀`. Bracketing yields the paired-root equivalent

\[
J_c(D_M)=[1+o(1)]\,2C_0A^{-1/4}|\sin r|^{-5/4}
=[1+o(1)]\,2C_0A^{-1/4}(1-c^2)^{-5/8}.
\tag{3}
\]

The complementary reciprocal-potential integral is at most `C/(ηr³)`. Its ratio to the displayed root contribution is bounded by

\[
C\eta^{-1}(A/r_0^7)^{1/4}=O(H^{-5/4})\to0.
\]

Hence the complement does not alter the leading coefficient. This also verifies that a pointwise simple-root asymptotic is not being used without the required uniformity.

## Probability factors and omitted regions

Raising (3) to the critical power changes its offset factor to `(1−c²)^(−1)`. The uniform disorder density is `1/4`, so directly in the offset variable the retained integral is

\[
\frac{(2C_0)^{8/5}}4 A^{-2/5}
\int_{-\cos r_0}^{\cos r_0}\frac{dc}{1-c^2}
\sim \frac{(2C_0)^{8/5}}2A^{-2/5}\log(1/r_0).
\tag{4}
\]

The exact integral is `2log cot(r₀/2)`. Equation (4) agrees with the source note's `4A_*A^(−2/5)log(1/R)`, because `A_*=(2C₀)^(8/5)/8` and `log(1/r₀)=log(1/R)−log H∼log(1/R)`. This independently checks the potentially delicate factor from two roots and two folds.

The omitted contributions satisfy the stated smaller bounds:

| Region | Integrated critical moment bound | Reason |
|---|---:|---|
| Root annuli `CR<r<RH` | `O(A^(−2/5)log H)` | The order response has power `r^(−5/4)`; after raising to `8/5` and multiplying by root density proportional to `r`, its integral is logarithmic. |
| Fold windows of offset width `O(R²)` | `O(R^(−14/5))=O(A^(−2/5))` | Response is `O(R^(−3))`. |
| Adjacent no-root offsets, distance at least `CR²` | `O(R^(−14/5))` | Integrate the potential-only bound `J^q≤C|t|^(−12/5)`. |
| Fixed no-root offset regions | `O(1)` | Potential is bounded away from zero. |

All are negligible compared with `A^(−2/5)H`. No unestimated region remains between the inner fold window and the retained separated roots.

Combining (2) and (4) gives

\[
4A_*M^{-2/5}Z_R^{2/5}\log(1/R)
\sim A_*M^{-2/5}[4\log(1/R)]^{7/5}
\sim A_*(4/7)^{7/5}M^{-2/5}H^{7/5},
\]

matching the lower coefficient.

## Documentation corrections

The source note's earlier status statements initially called the critical coefficient open or conjectural. The author reports that these were reconciled during this review; they can now record the independent verification given here. The older review of the order and subcritical results may also need its historical critical-status statements updated. Two displayed formulas in the new section contain a stray comma after `[1+o(1)]`; that is typographical only.

The substantive remaining limitations are unchanged: the theorem concerns the optimum value in the unrestricted scalar problem, not every near-minimizer or a unique finite-budget optimal shape. The supercritical sharp coefficient is not settled by this argument.
