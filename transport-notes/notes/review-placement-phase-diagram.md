# Independent review: three phases of finite-floor mobility placement

Review date: 2026-09-06. Reviewer: `review_singular_exchange`.

The three branches in [placement-phase-diagram.md](placement-phase-diagram.md) are correct for the stated whole-line quadratic design problem. I independently checked the differential equations, global slope constraints, completeness, uniqueness, exact masses and objective values, and both onset coefficients. The compact-wall leading optimum and the exact full-bulk no-placement criterion also follow under the qualifications below. A fresh numerical optimization starting from zero mobility recovered the predicted profiles.

This is mathematical verification, not a novelty determination. The underlying weighted Lipschitz projection and complementary-slackness certificate belong to established convex-design reasoning.

## Global certificate and sufficiency

Put `v(x)=1+x^2`, `f=1/v`, and

\[
F_\eta(d)=\int d+\eta^2J(d),\qquad
J(d)=\sup_{\phi\in C_c^\infty}\left[2\int\phi-\int(d|\phi'|^2+v\phi^2)\right].
\]

For any integrable finite-energy Lipschitz `h` with `|h'|<=1/eta`,

\[
F_\eta(d)\ge\eta^2\int(2h-vh^2)
+\int d(1-\eta^2|h'|^2).
\tag{1}
\]

The candidate fields have integrable `1/x^2` tails and bounded derivatives. Truncation followed by mollification justifies using them in this inequality for every nonnegative integrable coefficient, even though the definition initially uses compact smooth tests.

If a candidate pair satisfies

\[
-(dh')'+vh=1,\quad d\ge0,\quad
|h'|\le1/\eta,\quad d(1-\eta^2|h'|^2)=0,
\tag{2}
\]

then its weak equation yields `J(d)=int h`, and every inequality in (1) is saturated. This proves global optimality over all admissible placements. No assumption about the number of active intervals and no minimax interchange is needed.

The dual objective can be written

\[
\eta^2\int(2h-vh^2)=\pi\eta^2-\eta^2\int v(h-f)^2.
\]

Thus the explicit `h` is also the unique weighted least-squares projection of `f` onto the derivative constraint, up to the natural almost-everywhere convention.

## Checking the three branches

For zero mobility, `h=f`. Its derivative magnitude has maximum `3 sqrt(3)/8` at `|x|=1/sqrt(3)`, giving the first threshold `eta_1=8/(3 sqrt(3))`.

For the two-flank branch, write `q=r-l`, `S=r+l`. The proposed relations imply

\[
q^2=3S^2-4,\qquad lr=1-S^2/2,\qquad
\eta=S+S^3/4.
\]

The last expression increases strictly with `S`. The endpoints run from `l=r=1/sqrt(3)` to `l=0,r=sqrt(2)` as `S` increases from `2/sqrt(3)` to `sqrt(2)`, giving `eta_2=3/sqrt(2)`.

On the positive flank, put

\[
h=(3S/2-x)/\eta,\qquad
 d=(x-l)^2(x-r)^2/4.
\]

Direct expansion gives

\[
d'=\eta(1-vh),\qquad d(l)=d(r)=d'(l)=d'(r)=0.
\]

Consequently (2) holds on the interval and its flux matches the zero exterior flux. The endpoint values of `h` equal `f`. To verify the global slope bound without relying on a picture, differentiate the flux equation at either endpoint:

\[
d''=v[1-\eta|f'|],\qquad d''(l)=d''(r)=q^2/2>0.
\]

Thus `|f'|<1/eta` at both endpoints. The endpoints straddle the unique positive maximum of `|f'|`; its monotonicity on either side of that maximum proves the same strict bound throughout the inactive region.

On the central branch,

\[
\eta(R)=(R^3+7R+6/R)/8,
\quad R\ge\sqrt2.
\]

Its derivative `(3R^2+7-6/R^2)/8` is positive there. With `C=R/eta+1/(1+R^2)`, the proposed polynomial and field satisfy

\[
d'=\eta[1-v(C-x/\eta)],\qquad d(0)=d(R)=0.
\]

Nonnegativity follows from its factored form because `R^2>=2`. Outside the support,

\[
\eta|f'(R)|={6+R^2\over4(1+R^2)}<1,
\]

and the reciprocal-rate derivative decreases for `x>=R`. Even reflection gives zero matching flux at the center despite the cusp of `h`. At `R=sqrt(2)`, this coefficient is exactly `x^2(R-x)^2/4` on the positive half, agreeing with the limiting flank branch.

The third phase retains zero pointwise mobility at the center. Its two positive open intervals have touching closures; it is not a phase with strictly positive mobility across the center.

These explicit certified branches cover every nonnegative `eta`. Therefore no unexamined asymmetric arrangement or additional patches can improve their values.

## Uniqueness

For a competing coefficient to attain the certificate value, (1) forces it to vanish almost everywhere where the derivative constraint is strict. In the first phase this leaves only isolated points, so the unique integrable coefficient is zero, including at the threshold.

On every active open interval of the other phases, the candidate `h'` is a nonzero constant. Equality in the variational definition forces the weak equation in (2), which determines `d'` there. The zero exterior flux fixes its integration constant. At the center of the third phase, opposite signs of `h'` and nonnegativity of `d` exclude a nonzero common flux. These conditions uniquely recover the displayed polynomial coefficients almost everywhere.

The admissible class here consists of integrable functions. Extending it to measure-valued mobility would require an additional definition and a separate uniqueness argument; that extension is not needed for the theorem.

## Mass, cost, and critical coefficients

Independent symbolic calculations gave

\[
M_{\rm flank}=q^5/60,
\qquad
M_{\rm central}=R^3(9R^2-10)/240,
\]

and zero residual in both proposed differential equations. Integrating the piecewise linear and reciprocal fields directly gives exactly the two expressions for `J` in the development note, so `F=M+eta^2J` is verified.

A useful exact identity checks the delicate onset subtraction:

\[
\pi\eta^2-F_*=
\eta^2\int v(h-f)^2
=\int{(d')^2\over v}.
\tag{3}
\]

The last equality follows from `vh-1=-d'/eta`. In the flank branch, set `x=S/2+qy/2`, `-1<y<1`. Then

\[
d=q^4(1-y^2)^2/64,\qquad
 d'=-q^3y(1-y^2)/8.
\]

Since `v` tends to `4/3`, accounting for both flanks gives

\[
\pi\eta^2-F_*\sim {3q^7\over256}
\int_{-1}^1y^2(1-y^2)^2dy={q^7\over560}.
\tag{4}
\]

Also `eta-eta_1~q^2/(2 sqrt(3))`. The claimed mass exponent `5/2`, benefit exponent `7/2`, and their constants are therefore correct. The large-`eta` relations `R~2eta^(1/3)`, `M~(6/5)eta^(5/3)`, and `F~(36/5)eta^(5/3)` follow directly from the central formulas and agree with the zero-floor design.

## Exact finite-bulk no-placement criterion

At a fixed positive rate floor, let `h0` be the actual zero-surface-mobility wall corrector, including its bulk trace, and assume `h0'` is essentially bounded. The exact criterion in the development note is sound:

\[
D=0\text{ is a global optimum}\quad\Longleftrightarrow\quad
\|h_0'\|_\infty\le1.
\tag{5}
\]

For sufficiency, insert the zero-mobility full corrector into the full variational formula at arbitrary `D`. Its objective difference is bounded below by `(K/Z)int D(1-|h0'|^2)`, which is nonnegative. For necessity, if the essential supremum exceeds one, choose a bounded nonnegative perturbation supported on a positive-measure subset where `|h0'|>1`; the directional derivative is negative. The derivative is finite for that perturbation under the stated regularity.

The surface gradient includes the bulk trace. Replacing it with a reciprocal-rate gradient alone requires the well-mixed reduction. The same criterion also shows why unrestricted placement depends on an essential maximum, whereas varying a spatially uniform coefficient depends on an integrated squared gradient.

## Controlled compact-wall and full-bulk limit

Let `k_delta=delta+k0`, with one isolated quadratic zero `k0(s)=a s^2[1+o(1)]`, and positive lower bounds away from its neighborhoods. Scale the entire flow amplitude to zero with `V=eta delta^(3/2)/sqrt(a)`, for fixed `eta>0`. The leading scalar optimum is

\[
\inf_D\left[\int_\Gamma D+V^2J_\Gamma(D)\right]
\sim {\delta^{5/2}\over a^{3/2}}\mathcal F(\eta).
\tag{6}
\]

For a precise lower-bound argument, choose fixed nearby curvatures `a_+>a>a_->0` that bound `k0` in a fixed neighborhood. The whole-line certificate for `a_+` and the same physical `V,delta` has the correct physical slope bound `1/|V|`. Cut it off in the far part of that fixed neighborhood. Its tail and cutoff slopes stay bounded there, while the permitted central slope diverges, so the cutoff remains feasible for small `delta`. Potential ordering and the removed tails change the dual bound by only `O(V^2)`. This yields the whole-line optimal value for `a_+`, less `O(V^2)`, for every admissible compact-wall design.

For the upper bound, use the exact design for `a_-` on its shrinking support and zero mobility elsewhere. The natural zero-flux endpoints separate its active and inactive pieces. Potential ordering bounds its inverse functional by the model value plus `O(1)` from the remote reciprocal-rate tail. Thus the objective is bounded above by the whole-line value for `a_-`, plus `O(V^2)`. First send `delta` to zero, then send `a_+,a_-` to `a`. Continuity of the explicit value function in its scaled parameters proves (6).

The same comparison handles the zero-design first phase. The physical prefactor is `delta^(5/2)a^(-3/2)`, whereas the tail error is `O(V^2)=O(delta^3)` and is lower order.

For fixed positive bulk diffusivity, the Schur remainder is nonnegative for every placement. The localized trial designs have uniformly bounded `k_delta H_D^-1 1`: this follows from their bounded local model field and potential comparison, with the product equal to one on inactive regions. Their bulk remainder is therefore `O(V^2)` when the entire bulk flow is scaled as stated. Multiplication by `K/Z` gives the claimed leading full-channel optimum.

This proves the optimum-value limit. Convergence of a complete optimizing coefficient, exact support topology for a nonsymmetric finite profile, and transition laws in a shrinking physical window require additional stability estimates and are not implied by (6). The explicit phase boundaries and critical powers are exact properties of the quadratic local problem.

## Independent numerical optimization

The reproducible script [check-placement-phase-review.py](../scripts/check-placement-phase-review.py) discretizes the inverse problem on `[-6,6]` with 1,200 cell centers and nonnegative mobility on the faces. It minimizes the convex discrete objective from the zero coefficient using its exact gradient `dx[1-eta^2(h_x)^2]`. The analytic profiles are used only after optimization for comparison. The reciprocal-rate tail outside the finite interval is added analytically.

| eta | optimizer iterations | relative cost error | numerical mass | exact mass | maximum profile error |
|---:|---:|---:|---:|---:|---:|
| 1.4 | 0 | 2.33e-8 | 0 | 0 | 0 |
| 1.8 | 120 | 2.32e-8 | 0.01281854558 | 0.01282228800 | 4.64e-6 |
| 3.0 | 232 | -2.34e-7 | 0.7296599163 | 0.7296416253 | 1.11e-5 |

All three runs reported successful optimization. This independent discretization supports the three regimes and the explicit profiles. The mathematical certificate establishes the continuum optimum; the numerical table is a separate consistency check, not a mesh-convergence proof.

For the periodic benchmark `k_delta=delta+2(1-cos s)`, the developing agent supplied an additional exact reduced-model onset formula. I checked its maximizing condition and expansion independently. With `c=cos(s_*)`, stationarity of the positive reciprocal-rate gradient gives

\[
2c^2+(\delta+2)c-4=0,\qquad
c={-(\delta+2)+\sqrt{(\delta+2)^2+32}\over4}.
\]

The scaled onset is therefore

\[
\eta_{1,\delta}=
{(\delta+2-2c)^2\over2\delta^{3/2}\sqrt{1-c^2}}
={8\over3\sqrt3}\left[1+{\delta\over24}+{\delta^2\over3456}+O(\delta^3)\right].
\]

An independent symbolic expansion reproduced both correction coefficients. This provides a concrete finite-profile shift of the first threshold and supports the caution about using the local critical law inside an arbitrarily shrinking physical onset window.
