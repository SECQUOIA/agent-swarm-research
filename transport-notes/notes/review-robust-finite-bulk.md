# Independent review: finite-bulk robust and adaptive mobility design

Reviewed 2026-09-07 by `review_singular_exchange`.

The parent’s proposed transfer to finite transverse bulk diffusion is sound. Smooth positive approximations suffice for the design chosen before observing the random offset, so no uniform bulk estimate for its singular limiting shape is needed. The localized designs used after observing the offset have uniformly bounded exchange flux, including when two roots merge. Their zero-mobility exterior gives natural Neumann patch endpoints in the variational model.

Together with [the independently reviewed scalar theorem](review-robust-mobility-design.md), this proves the same two leading constants and budget exponents for the full bulk–surface flow dispersion. The proof uses fixed positive bulk diffusivity, constant affinity, a fixed smooth cross-section, and a fixed nonzero mean velocity. It does not establish literature novelty.

## Full-bulk quantities and target statements

Use the periodic family

\[
k_c(s)=(c+\cos s)^2,\qquad c\sim\operatorname{Uniform}[-2,2],
\quad D(s)\ge0,\quad\int_\Gamma D=M.
\]

The wall has length `2pi`, and the transverse surface operator is in divergence form:

\[
H_{D,c}=-\partial_s(D\partial_s)+k_c.
\]

With the notation of [the random finite-bulk review](review-random-finite-bulk.md),

\[
D_{\rm flow}(D,c)=B J_c(D)+R(D,c),\qquad
B={KV^2\over Z}>0,\quad R\ge0.
\tag{1}
\]

Let `C_blind=18.3860636501...` and `C_adapt=22.4046282307...` denote the exact beta–gamma expressions in [robust-mobility-design.md](robust-mobility-design.md). Then

\[
\boxed{\inf_{D:\int D=M}\mathbb E_cD_{\rm flow}(D,c)
\sim B C_{\rm blind}M^{-1/4},}
\tag{2}
\]

\[
\boxed{\mathbb E_c\left[\inf_{D:\int D=M}D_{\rm flow}(D,c)\right]
\sim B C_{\rm adapt}M^{-1/5}.}
\tag{3}
\]

The full-bulk designs attaining the infimum at a finite budget need not coincide with the scalar optimizers. Equations (2)–(3) identify the leading optimum values.

## Designs chosen before observing the offset

Choose any fixed periodic `C1` shape `d` with `0<b<=d<=b1`, `int d=1`, and put `D=Md`. Let `h=H_(Md,c)^-1 1`, `J=int h`, and `w=k_c h`. Multiplication of the differential equation by `k_c h` gives the exact variable-coefficient identity

\[
\|w-1\|_2^2+M\int d k_c|h'|^2
={M\over2}\int(d k_c')'h^2.
\tag{4}
\]

Integration of the original equation still gives `int w=P`. The derivative of `d` must be retained in (4).

For `g=c+cos s`,

\[
k_c''=2(1-c^2)+6cg-4g^2,
\qquad |k_c'|\le2\sqrt{k_c}.
\]

Consequently, with constants allowed to depend on this fixed shape,

\[
(d k_c')'\le C_d[(1-c^2)_++\sqrt{k_c}].
\]

The energy and spectral inequalities imply

\[
\|h\|_2^2\le J/\lambda,\qquad
\int\sqrt{k_c}h^2\le J/\sqrt\lambda.
\]

Form ordering against the constant coefficient `Mb` supplies the same piecewise gap and integrated-resolvent scales as in the random finite-bulk review, with `M` replacing its constant diffusivity. Substitution into (4) therefore gives

\[
\sup_{|c|\le2}\|k_cH_{Md,c}^{-1}1-1\|_2
\le C_dM^{1/12}.
\tag{5}
\]

The Schur argument then proves `R(Md,c)->R0` uniformly in `c`, where `R0` is the rate-independent bulk Neumann energy. In particular, its ensemble mean is bounded for each fixed `d`.

Now approximate the scalar optimal shape proportional to `|sin s|^(-2/5)` by normalized smooth positive truncations `d_C`. They can be chosen so that

\[
C_0\int_\Gamma w_0(s)d_C(s)^{-1/4}ds
\longrightarrow C_{\rm blind},
\qquad w_0(s)=\tfrac14|\sin s|^{-1/2}.
\]

For each fixed truncation level, the scalar theorem and (5) give the full-bulk upper coefficient associated with `d_C`. First send `M` to zero, and then send the truncation level to infinity. This proves the upper bound in (2). The lower bound follows immediately from (1) and the unrestricted scalar lower bound.

The constants in (5) may grow with the truncation level. The ordered limit is essential to this proof: it does not certify the bulk remainder for the unbounded limiting shape itself, nor does it assume a uniform estimate over all smooth approximations.

## Natural endpoints for a mobility patch

The adaptive upper bound uses positive mobility on a finite interval and zero mobility outside. Its variational definition is the closure of smooth periodic tests under the mobility energy plus the potential-weighted norm.

For a step from a positive constant inside the patch to zero outside, that completion permits an independent `H1` field on the patch and a potential-weighted `L2` field outside. A jump between their limiting boundary values can be approximated through arbitrarily thin transition layers on the zero-mobility side. Their gradient has zero mobility cost, and their potential cost tends to zero. Thus the inside operator has natural zero-flux, or Neumann, endpoints; continuity with the exterior field is not imposed by this energy completion.

For the polynomial patches whose coefficient vanishes quadratically at their outer endpoints, the same conclusion holds. The weighted derivative cost of smoothing a fixed jump across a layer of width `epsilon` is `O(epsilon)` because the coefficient is `O(distance^2)` there. In every case the exterior solution is `h=1/k_c`, since the chosen supports contain all kinetic zeros.

This endpoint convention agrees with the scalar functional being optimized. Requiring a uniformly positive mobility background or imposing an additional trace-continuity condition would define a different design problem.

## Adaptive trial family: separated roots

Put `t=1-|c|`. In the inside regime `t>=L M^(2/7)`, each root has curvature `a=1-c^2` comparable to `t`. The roots are separated by a distance comparable to `sqrt(t)` near a fold. Place half the budget in each quadratic optimal patch, using a lower comparison curvature `a_-` comparable to `t`. Each patch radius satisfies

\[
R\asymp(M/t)^{1/5}\le C M^{1/7}.
\]

Choosing `L` sufficiently large ensures both patches fit in neighborhoods where

\[
a_-x^2\le k_c\le a_+x^2,
\qquad a_+/a_-\le C.
\]

For the same mobility coefficient, the quadratic-model field is a positive supersolution for the actual potential. The weak comparison principle for the common diffusion form therefore gives

\[
0\le h\le h_{*,a_-},\qquad
k_ch\le{a_+\over a_-}\max_{0\le y\le1}y^2(9-8y)
={27a_+\over16a_-}.
\tag{6}
\]

The number `27/16` alone applies to the exact quadratic model; the curvature ratio is required for the cosine profile. It is uniformly bounded in this trial construction. Outside the patches, `k_ch=1`. The exact polynomial model and its zero-flux endpoints justify comparison even though its mobility degenerates at the center and the outer endpoints.

## Adaptive trial family: merging roots

For `|t|<=L M^(2/7)`, choose a patch of radius

\[
R=K_1M^{1/7}
\]

around the fold center and set its constant mobility to

\[
D_{\rm patch}=M/(2R)=(2K_1)^{-1}M^{6/7}.
\]

Take `K1` fixed and large enough that every root in this regime lies strictly inside the patch with a fixed scaled margin. In the physical coordinate centered at the fold, write `x=M^(1/7)y` and `tau=t/M^(2/7)`. The interval is exactly `[-K1,K1]`, and

\[
H=M^{4/7}\left[-{1\over2K_1}\partial_y^2+v_{M,\tau}(y)\right],
\]

\[
v_{M,\tau}(y)=
\left[-\tau+{1-\cos(M^{1/7}y)\over M^{2/7}}\right]^2
\longrightarrow(y^2/2-\tau)^2.
\tag{7}
\]

The convergence is uniform with the required derivatives on this fixed interval and for `|tau|<=L`. This physical-coordinate rescaling avoids needing an additional endpoint metric argument.

With Neumann endpoints, the limit operators have a uniformly positive gap: their derivative coefficient is fixed and positive, the parameter range is compact, and none of their nonnegative potentials is identically zero. Positivity of each gap follows because zero energy would require a constant function annihilated by the potential. Compactness supplies a common bound, which persists for small `M`.

Let `q` solve the bracketed operator with source one. The gap bounds its `L2` norm; uniform one-dimensional elliptic estimates then bound its `H2` norm and hence its supremum. Both `q` and `v_(M,tau)` are uniformly bounded. Since `h=M^(-4/7)q` inside the physical patch,

\[
0\le k_ch=v_{M,\tau}q\le C.
\tag{8}
\]

The exterior again has `k_ch=1`. This proves the pointwise estimate needed by the bulk Schur bound; a bound on the integrated inverse alone would not have supplied it.

## Adaptive trial family: no roots

For the remaining no-root offsets, choose the uniform coefficient `D=M/P`, which uses the required budget. The uniform-offset flux bound in [review-random-finite-bulk.md](review-random-finite-bulk.md) gives a uniform `L2` bound on `k_ch`, as well as convergence to one. Scalar potential ordering also gives `J_c(D)<=int 1/k_c`, as required by the adaptive scalar envelope.

Equations (6)–(8) and this uniform choice prove that every member of the piecewise trial family has `R(D,c)<=C`, uniformly in the offset and budget.

There is a stronger optional estimate. The localized trial supports have total length `O(M^(1/7))`, and their exchange product is uniformly bounded and equals one outside. Thus their flux difference has `L2` norm `O(M^(1/14))`. The no-root uniform designs have the faster bound `O(M^(1/12))`. The selected coefficients also satisfy `||D||_infinity<=C M^(4/5)`. Testing the Schur form with the smooth-domain bulk Neumann solution therefore gives

\[
R(D_{\rm trial}(c),c)=R_0+O(M^{1/14})
\tag{9}
\]

uniformly for this selected family, under the trace regularity used in the random finite-bulk review. Only the boundedness, not (9), is needed for the leading optimum.

## Recovering the sharp adaptive constant

The coarse comparison choice `a_-=c_1t` establishes the envelope and bulk bound, but on its own need not attain the sharp fixed-offset scalar coefficient. This distinction must be retained when proving the upper bound in (3).

One clean construction fixes a small offset cutoff around the folds and a small curvature error `epsilon>0`. On the retained compact inside-offset region, use local quadratic patches with lower curvature `(1-epsilon)(1-c^2)`. For all sufficiently small budgets their actual potentials are bounded between the corresponding `1±epsilon` quadratics uniformly on that region. Their coefficient approaches the sharp fixed-offset value as `epsilon` tends to zero, and (6) bounds their bulk remainder uniformly.

In the removed fold neighborhoods, use the coarse trials above. Their normalized scalar costs obey the integrable bound `C|t|^(-4/5)` proved in the scalar review; the normalized bounded bulk remainder vanishes. Their contribution to the normalized mean is therefore at most a constant times the one-fifth power of the offset cutoff. Outside the folds and the root-containing region, the no-root trial contributes no leading term.

Send `M` to zero first, then shrink the excluded offset neighborhoods and send `epsilon` to zero. This yields the upper constant `B C_adapt`. The pointwise nonnegative remainder in (1) and the independently reviewed scalar adaptive equivalent give the matching lower bound. The explicit piecewise trial policies can be chosen measurably in `c` through their root positions and regime thresholds.

This proves (3) without assuming that an arbitrary scalar optimizer has a controlled bulk remainder.

## Independent merging-patch computation

I discretized the rescaled Neumann problem (7) on 1,200 cell centers with `K1=3` and `tau=-1,0,1`. The table reports the largest value of the scaled inverse field `q` and of the exchange product `v q` over those three parameters.

| M | maximum scaled field | maximum exchange product |
|---:|---:|---:|
| 1e-7 | 6.35588247 | 1.86709677 |
| 1e-10 | 6.35162223 | 1.86801033 |
| 1e-13 | 6.35103105 | 1.86813724 |

These fresh computations support the uniform bound used above. The analytic finite-interval coercivity and elliptic estimates establish uniformity over the whole parameter range; the table is only a separate consistency check.

Additional fixed bulk axial molecular diffusion and the isotropic surface term `(K/Z)M` are lower order than the divergent leading terms in (2)–(3). If `V=0`, those singular flow terms disappear, so neither displayed equivalent applies. Fixed mobility caps, fabrication scales, uncertain affinity, or bulk diffusivity vanishing with the budget remain separate models.
