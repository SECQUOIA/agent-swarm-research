# Second independent review: localization of optimal surface mobility

Reviewed 2026-09-06 by `review_localization`.

The compact-wall optimum, allocation among separated equal-order zeros, and leading optimum for the full finite-bulk dispersion in [the optimal-placement note](optimal-mobility-placement.md) are correct for the stated unrestricted integral budget. This review supplies the details needed for arbitrary concentrated placements and for the degenerate trial profiles. It also checks the extension from quadratic zeros to any common power `m>1`.

The conclusion is mathematical verification within the model, not a novelty finding. The leading asymptotics below do not imply an additive bounded error after subtracting their leading term.

## Assumptions and result

Let Γ be a fixed compact periodic one-dimensional wall, or a finite union of such components. Assume k is fixed, continuous, nonnegative, bounded away from zero outside neighborhoods of finitely many separated zeros, and

\[
k(s_j+x)=a_j|x|^m[1+o(1)],\qquad a_j>0,\quad m>1.
\]

There is at least one zero. No component has identically zero k. For `D>=0` in `L¹(Γ)` with `integral D=M`, define

\[
J_\Gamma(D)=\sup_{f\in C^\infty(\Gamma)}
\left\{2\int_\Gamma f-\int_\Gamma kf^2-\int_\Gamma D|f'|^2\right\},
\tag{1}
\]

allowing an infinite value. This definition gives an unambiguous scalar design problem even for an irregular D for which no diffusion realization has been specified.

Write

\[
\alpha=\frac{m-1}{m+3},\qquad
C_m=\frac{m^2(m+1)}{m-1}
\left[\frac{m+1}{(m+2)^2(m+3)}\right]^\alpha,
\qquad S=\sum_j a_j^{-2/(m+1)}.
\]

Then

\[
\inf_{D\ge0,\,\int D=M}J_\Gamma(D)
\sim C_m S^{\alpha+1}M^{-\alpha}.
\tag{2}
\]

An asymptotically optimal allocation is

\[
M_j=M a_j^{-2/(m+1)}/S.
\tag{3}
\]

For a quadratic zero, `m=2`, this is precisely `C_2=12(3/80)^(1/5)`, exponent `−1/5`, and weights proportional to `a_j^(−2/3)`.

## A lower bound uniform over all placements

Fix `eta in (0,1)` and disjoint fixed coordinate neighborhoods `U_j=(-r_j,r_j)` so that

\[
a_{j,-}|x|^m\le k(s_j+x)\le a_{j,+}|x|^m,
\qquad a_{j,\pm}=(1\pm\eta)a_j.
\tag{4}
\]

For any admissible D set `b_j=integral_(U_j) D`. The argument must use these actual local masses, rather than assume that a minimizing sequence has already localized. Their sum is at most M.

For `b_j>0`, take the exact whole-line optimal inverse field h for curvature `a_(j,+)` and budget bⱼ. Its support radius in the associated optimal coefficient is

\[
R_j=\left[\frac{b_j(m+2)^2(m+3)}{a_{j,+}(m+1)}\right]^{1/(m+3)},
\]

and its central absolute slope is

\[
c_j=\frac{m(m+2)}{a_{j,+}R_j^{m+1}}.
\]

Multiply h by a fixed smooth cutoff equal to one on `|x|<r_j/2` and supported strictly inside Uⱼ. For all sufficiently small M, uniformly over `0<b_j<=M`, the cutoff acts only on the exact tail `h=1/(a_(j,+)|x|^m)`. Consequently:

- The change in the load-minus-potential expression `2 integral h − integral a_(j,+)|x|^m h²`, relative to the whole line, is bounded by a constant independent of bⱼ.
- Every slope introduced in the cutoff region is bounded independently of bⱼ. The diverging central slope cⱼ therefore remains the global Lipschitz bound for all sufficiently small M.
- Smooth approximations supported inside Uⱼ can retain this slope bound. Ordinary convolution of the cutoff Lipschitz field suffices, with a sufficiently small convolution radius.

The potential ordering in (4) and `integral_(U_j) D|f'|² <= b_j c_j²` now give

\[
J_\Gamma(D)\ge
\sum_j C_m a_{j,+}^{-4/(m+3)}b_j^{-\alpha}-C_\eta.
\tag{5}
\]

To justify adding the tests, choose their supports disjoint; both the quadratic energy and the linear load then add exactly. The smoothing limit concerns only the ordinary load and potential integrals. The mobility term is bounded directly by the Lipschitz constant, so the proof does not need a uniform bound, positive lower bound, or regularity bound on D.

If `b_j=0`, use the same local test with an arbitrary auxiliary positive budget tending to zero. Its source-minus-potential value diverges, while its mobility cost is zero. Thus `J_Γ(D)=infinity`, consistent with (5).

Set `w_j=C_m a_(j,+)^(−4/(m+3))`. Elementary constrained minimization gives

\[
\inf_{b_j>0,\,\sum b_j\le M}\sum_j w_jb_j^{-\alpha}
=M^{-\alpha}\left(\sum_j w_j^{1/(\alpha+1)}\right)^{\alpha+1}.
\tag{6}
\]

Indeed the objective decreases in every bⱼ, so all available budget is used; its derivative condition gives `b_j proportional to w_j^(1/(alpha+1))`. Since this power is proportional to `a_(j,+)^(−2/(m+1))`, (5) proves the required uniform lower bound before η tends to zero.

This excludes improvements from arbitrary sequences of increasingly concentrated L¹ designs, or from placing part of the budget away from the kinetic zeros. No compactness assumption on candidate designs enters the proof.

## A matching trial construction and its endpoints

Allocate the budget according to the curvatures `a_(j,−)` and place the exact whole-line optimal coefficient inside each sufficiently small radius Rⱼ. Set D to zero elsewhere. The supports are disjoint for small M, and their masses sum exactly to M.

For one such interval, with curvature b, the inverse comparison field is

\[
h_b(x)=\frac{(m+1)^2-m(m+2)|x|/R}{bR^m},
\qquad |x|<R.
\]

Its coefficient satisfies

\[
-(D_*h_b')'+b|x|^m h_b=1,
\qquad D_*h_b'=0\quad\text{at }-R,0,R.
\tag{7}
\]

For every smooth field f restricted to this interval, integration by parts and completion of the square yield

\[
2\int_{-R}^R f-\int_{-R}^R[D_*|f'|^2+kf^2]
\le \int_{-R}^R h_b
=\frac{m^2+2m+2}{bR^{m-1}}.
\tag{8}
\]

The potential inequality `k>=b|x|^m` was used here. Because the flux in (7) vanishes, no imposed trace of f or artificial boundary term is needed. This is a direct upper bound for the original smooth-test problem and does not assume domain splitting.

On the rest of the wall, D=0 and the pointwise inequality `2f−kf²<=1/k` applies. The nearby exterior tail satisfies

\[
\int_{R<|x|<r_j}\frac{dx}{k(s_j+x)}
\le\frac{2}{(m-1)bR^{m-1}}+O_{r_j,\eta}(1).
\]

The remaining fixed exterior region contributes a bounded amount. Adding (8) and this tail gives the exact whole-line constant as an upper bound plus a fixed bounded error. Combining with (5), dividing by `M^(−alpha)`, taking M to zero at fixed η, and finally taking η to zero proves (2).

These fixed-η bounded errors are sufficient for a relative asymptotic. Their existence does not imply a bounded error relative to the final expression with the exact curvatures aⱼ.

## Natural form and the cusp

For each trial coefficient, D is continuous, is positive on the two open half-supports, behaves as a positive constant times `|x|` near the center, and vanishes quadratically at each outer endpoint. Its weighted derivative form, initially on smooth periodic functions, has a natural closed realization. One may check closability directly by working on compact subintervals where D is positive; outside the support the derivative energy is zero. The bounded continuous nonnegative potential can then be added to this form.

The endpoint zeros have zero capacity for this derivative energy. For example, a transition of fixed height over width ε at an outer endpoint costs `O(ε)` because `D=O(distance²)`; its L² and potential costs also tend to zero. Thus the closed domain permits independent interior and exterior traces. At the central linear zero, logarithmic transition profiles have derivative cost tending to zero, since `integral dx/D` diverges logarithmically. This also permits separation of the two halves if one needs that domain description.

The inverse comparison field itself is continuous and Lipschitz through the center; its derivative cusp produces no delta source because the flux vanishes there. Its exterior joining value may differ from `1/k` for the actual profile. This jump is allowed at the outer zero-capacity endpoints. No physical claim about transmission of individual paths through the exact center is needed for stationary absolutely continuous quantities.

For every fixed positive M, the trial problem has a finite scalar inverse field q. This can also be seen from coercivity: near a center, an anchored weighted Cauchy–Schwarz estimate bounds a field by its derivative energy times `1+|log |x||`, which is integrable in x; away from the centers, k is bounded below. No coercivity constant uniform in M is asserted or needed.

## Finite-bulk optimization

Use the constant-affinity reversible bulk–surface model, with fixed smooth bounded connected cross-section, fixed positive bulk diffusivity, and bulk velocity in L². Set `B=KV²/Z`. For any admissible design with a specified reversible variational realization, choosing the bulk cell test field to be zero gives

\[
D_{\rm flow}(D)\ge B J_\Gamma(D).
\tag{9}
\]

The same inequality holds directly if both quantities are defined through their smooth-test variational suprema. Thus the uniform scalar lower bound already bounds the infimum of the full dispersion; no bound on the bulk remainder for arbitrary designs is required.

For the localized trial designs, positivity comparison with h_b on each support gives `0<=q<=h_b`. The comparison is valid in the closed form: test the difference equation with its positive part, use `k>=b|x|^m`, and use the natural zero flux at the endpoints. Consequently

\[
0\le kq\le\frac{a_{j,+}}{a_{j,-}}
(m+1)\left(\frac{m+1}{m+2}\right)^m
\quad\text{on support }j,
\tag{10}
\]

where the maximum follows by differentiating `y^m[(m+1)²−m(m+2)y]`. Outside the supports, q=1/k almost everywhere. Hence kq is uniformly bounded on the entire wall, independently of M.

The exact Schur-complement cell formula, with this weighted surface form, gives

\[
D_{\rm flow}(D)=BJ_\Gamma(D)+\mathcal R(D),\qquad
0\le\mathcal R(D)\le C_{\rm bulk}
\tag{11}
\]

along the trial designs. The bound follows from (10), the bulk trace and Poincaré inequalities, and dropping the nonnegative Schur penalty. Constant wall tests are allowed and give `integral kq=P`, which preserves the bulk gauge compatibility.

Combining the full-model lower bound (9) with the trial upper bound (11), for `V!=0`, proves

\[
\inf_{\int D=M}D_{\rm flow}(D)
\sim BC_m S^{\alpha+1}M^{-\alpha}.
\tag{12}
\]

The finite-budget full-model optimizer need not equal the scalar optimizer. If V=0, (12) is not an asymptotic equivalence.

The stronger convergence claim for the regular bulk correction along these trials is also sound. The bounded field `kq−1` is supported on intervals of total length `O(M^(1/(m+3)))`, so its L² norm tends to zero. The bulk load therefore converges in the bulk energy dual norm. For every fixed smooth bulk test field f, its Schur penalty is at most `M ||partial_s f_Γ||_infinity²`, and tends to zero. Dropping this nonnegative penalty gives the upper limit of the bulk supremum; fixed smooth tests and density give the lower limit. The limit is the rate-independent zero-mobility bulk correction derived in the earlier surface-exchange review.

## Concentration and measure-valued relaxations

The theorem as written optimizes over L¹ coefficients. It already includes arbitrarily narrow, high-amplitude concentration sequences, without an amplitude constraint.

If a broader scalar variational relaxation is desired, replace `D ds` in (1) by any finite nonnegative measure μ of mass M and keep smooth tests. The same universal lower bound holds: the smoothed local certificates have uniformly bounded derivatives, so `integral |f'|² dμ <= c_j² μ(U_j)`, including atoms. The absolutely continuous trial coefficients remain admissible and attain the matching upper asymptotic. Thus allowing singular measures in this precise scalar relaxation does not improve the leading constant or exponent. This does not assign a physical diffusion generator to an atomic mobility measure, or prove uniqueness in that enlarged class.

No conclusion here requires undocumented uniform additive errors, regularity of arbitrary competing mobility designs, or an interchange between weak-budget and long-time limits. The only domain claims concern the explicit trial designs, where the degeneracies and fluxes can be checked directly.
