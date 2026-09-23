# Independent review: uniform finite-bulk transfer for random offsets

Reviewed 2026-09-07 by `review_singular_exchange`.

The parent’s exchange-flux argument is correct. For the periodic family `k_c(s)=(c+cos s)^2`, it gives a uniform `L2` bound of order `D^(1/12)` on `k_c H_(D,c)^-1 1-1`. This closes the finite-bulk extension of the scalar disorder-moment theorem in [review-random-kinetic-barriers.md](review-random-kinetic-barriers.md). The regular bulk correction converges to a constant independent of the offset. Under the stated smooth-domain assumptions its error has the same uniform `O(D^(1/12))` bound.

This verification applies to the compact, fixed-amplitude offset family. It does not repair the distinct amplitude-collapse issue for general Gaussian disorder and does not establish literature novelty.

## Setting and uniform scalar estimates

Let

\[
H_{D,c}=-D\partial_s^2+k_c(s),\quad
k_c(s)=(c+\cos s)^2,\quad |c|\le2,
\]

on the circle of length `P=2pi`, with `D>0` tending to zero. Write

\[
h=H_{D,c}^{-1}1,\quad J=\int h,\quad w=k_ch,
\quad\lambda=\lambda_{\min}(H_{D,c}),\quad d=D^{1/3}.
\]

All constants below are independent of `c` and sufficiently small `D`. Put `t=1-|c|`. The needed bounds are

\[
\begin{array}{ll}
t\ge0:&
\lambda\ge C_1D^{1/2}(t+d)^{1/2},\quad
J\le C_2D^{-1/4}(t+d)^{-3/4},\\[3pt]
t<0:&
\lambda\ge C_1(|t|+d)^2,\quad
J\le C_2(|t|+d)^{-3/2}.
\end{array}
\tag{1}
\]

The integrated-resolvent bounds were independently proved in [the scalar disorder review](review-random-kinetic-barriers.md), including the required Neumann interval comparisons. I checked their rewriting into (1). I also checked the accompanying gap estimates, which require the additional argument below rather than following from a bound on the integrated resolvent alone.

## Uniform gap proof

Near `c=1`, center the wall at `s=pi` and use `z=2sin((s-pi)/2)`. Then

\[
c+\cos s=z^2/2-t
\]

exactly, and the coordinate metric and its inverse are bounded on a fixed small neighborhood. The local Rayleigh quotient is therefore comparable, with fixed factors, to the quotient of

\[
-D\partial_z^2+(z^2/2-t)^2.
\]

Set `z=(4D)^(1/6)y` and `mu=t/(D/2)^(1/3)`. The canonical energy scale is `(D/2)^(2/3)` and the potential becomes `(y^2-mu)^2`.

For bounded `mu`, this canonical operator has a uniform positive lower bound on expanding Neumann intervals. An anchored Poincare estimate controls mass in a fixed core by derivative energy and mass in an adjacent region with positive potential; quartic potential controls the exterior mass. The same argument holds uniformly for `mu` in a compact set. This supplies a lower bound proportional to `D^(2/3)` when `t=O(D^(1/3))`.

For large positive `mu`, split the interval at fixed-fraction neighborhoods of its roots `±sqrt(mu)`. On each root neighborhood,

\[
(y^2-\mu)^2\ge c\mu(y\mp\sqrt\mu)^2.
\]

Neumann bracketing and a further oscillator rescaling give a lower eigenvalue bound `c sqrt(mu)` there: the oscillator-scaled interval length is bounded below and tends to infinity with `mu`. The complementary intervals have potential at least `c mu^2`, which is larger than the required `sqrt(mu)` scale. Thus the canonical gap is bounded below by `c(1+mu)^(1/2)` for `mu>=0`, provided the roots remain inside the fixed-fraction interval used by the local construction. This yields the inside gap in (1). Away from the merging-root offsets, ordinary uniformly nondegenerate quadratic localization gives the same estimate with `t` bounded below.

One may combine the fixed physical neighborhoods with either Neumann bracketing or a smooth partition. A smooth partition introduces only an `O(D)` localization error, smaller than the minimum `D^(2/3)` gap scale.

On the outside, write `|c|=1+nu`, `nu>=0`. After translating the circle if necessary,

\[
k_c=(\nu+1-\cos s)^2\ge\nu^2+(1-\cos s)^2.
\]

The quartic gap at `|c|=1` therefore gives

\[
\lambda\ge\nu^2+cD^{2/3}\ge c'(\nu+D^{1/3})^2.
\]

This establishes the outside bound throughout the compact parameter range. The fold at `c=-1` follows by a translation and sign change. All comparison constants can consequently be chosen uniformly for `|c|<=2`.

## Exact exchange-flux identity

Integration of `Hh=1` gives `int w=P`, and the energy identity gives

\[
D\int|h'|^2+\int k_ch^2=J,
\qquad
\|h\|_2^2\le J/\lambda.
\tag{2}
\]

Multiplying the differential equation by `k_ch` and integrating by parts gives

\[
\|w-1\|_2^2+D\int k_c|h'|^2
={D\over2}\int k_c''h^2.
\tag{3}
\]

The subtraction of `P` on the left uses `int w=P` exactly. The sign of the second-derivative term on the right is positive as displayed.

Put `g=c+cos s`, so `k_c=g^2`. Direct differentiation gives the useful exact identity

\[
k_c''=2(1-c^2)+6cg-4g^2.
\tag{4}
\]

For `|c|<=2`, discard the negative quadratic term and bound the mixed term by a constant times `sqrt(k_c)`. Also,

\[
\int\sqrt{k_c}\,h^2
\le\left(\int k_ch^2\int h^2\right)^{1/2}
\le J/\sqrt\lambda.
\]

Consequently,

\[
\|w-1\|_2^2
\le CDJ\left[\frac{(1-c^2)_+}{\lambda}
+\frac1{\sqrt\lambda}\right].
\tag{5}
\]

On the inside, `(1-c^2)_+=t(2-t)<=2t`. Substitution of (1) gives

\[
\|w-1\|_2^2
\le C\left[
\frac{D^{1/4}t}{(t+d)^{5/4}}
+\frac{D^{1/2}}{t+d}\right]
\le CD^{1/6}.
\]

The last step uses `t/(t+d)^(5/4)<=(t+d)^(-1/4)<=d^(-1/4)` and `t+d>=d`. On the outside the first term in (5) vanishes, leaving

\[
\|w-1\|_2^2\le\frac{CD}{(|t|+d)^{5/2}}
\le CD^{1/6}.
\]

Thus

\[
\boxed{\sup_{|c|\le2}\|k_cH_{D,c}^{-1}1-1\|_{L^2(\Gamma)}
\le CD^{1/12}.}
\tag{6}
\]

The special identity (4) matters: using only a fixed bound on `||k_c''||_infinity` would lose the needed smallness near the quartic offsets.

## Uniform finite-bulk correction

Take a fixed bounded connected smooth cross-section with wall coordinate as above, fixed positive transverse bulk diffusivity `Db`, fixed square-integrable axial velocity `u`, and constant affinity `K>0`. Let `Z=A+KP`, `V=int_Omega u/Z`, and `B=KV^2/Z`. The invariant bulk and surface weights are independent of `c` because adsorption and desorption share the same rate factor.

The exact Schur decomposition is

\[
D_{\rm flow}(D,c)=BJ_D(c)+R_D(c),
\]

\[
ZR_D(c)=\sup_b\left[
2L_{D,c}(b)-D_b\int_\Omega|\nabla b|^2-KS_{D,c}(b)\right],
\]

\[
L_{D,c}(b)=\int_\Omega(u-V)b-KV\int_\Gamma wb,
\quad
S_{D,c}(b)=\langle b,(k_c-k_cH_{D,c}^{-1}k_c)b\rangle\ge0.
\tag{7}
\]

All boundary occurrences of `b` denote its trace. The forms annihilate constants in the required way, since `int w=P`. On the mean-zero bulk space, trace and Poincare inequalities together with (6) give

\[
\|L_{D,c}-L_0\|_{(H^1/\mathbb R)^*}\le CD^{1/12},
\quad
L_0(b)=\int_\Omega(u-V)b-KV\int_\Gamma b,
\tag{8}
\]

uniformly in the offset.

Let `b0` be the mean-zero weak solution

\[
-D_b\Delta b_0=u-V,\qquad D_b\partial_n b_0=-KV,
\]

and put

\[
R_0={D_b\over Z}\int_\Omega|\nabla b_0|^2.
\]

Dropping the nonnegative Schur penalty proves the uniform upper limit `R_D<=R0+o(1)`. For every fixed smooth trial field,

\[
S_{D,c}(b)\le D\int_\Gamma|b_\Gamma'|^2,
\]

independently of `c`. Inserting such fields and using density proves the matching uniform lower limit. Hence

\[
\boxed{D_{\rm flow}(D,c)=BJ_D(c)+R_0+o(1)
\quad\text{uniformly for }|c|\le2.}
\tag{9}
\]

There is also a rate under the stated smooth-domain regularity. The Neumann solution for `u` in `L2` belongs to `H2`, so its boundary trace has a square-integrable derivative. Insert `b0` directly in the lower bound, use (8), and bound its Schur penalty by `D int|b0_Gamma'|^2`. The upper bound is controlled by the squared energy-dual norm in (8). This gives

\[
\sup_{|c|\le2}|R_D(c)-R_0|\le CD^{1/12}.
\tag{10}
\]

If only weaker domain regularity is assumed, retain the density proof and the uniform `o(1)` statement unless the trace regularity needed for (10) is separately established. No estimate is uniform as bulk diffusivity tends to zero.

## Transfer of disorder moments

Let `c` be uniform on `[-2,2]` as in the scalar theorem, and assume `V!=0`, so `B>0`. The scalar review proves divergence of `E J_D^q` for every fixed `q>0`, with the threshold at `q=4/3` and the explicit constants recorded there. The uniformly bounded correction in (9) implies

\[
\mathbb E[D_{\rm flow}(D,c)^q]
\sim B^q\mathbb E[J_D(c)^q]
\quad(q>0).
\tag{11}
\]

For `0<q<=1`, the bounded additive correction changes the moment by a bounded amount using the Hölder continuity of the power function. For `q>1`, the moment change is at most a constant times `E J_D^(q-1)+1`; Hölder's inequality makes this lower order than `E J_D^q`. These arguments do not assume that `J_D` diverges uniformly in the offset, which would be false on the outside region.

The same reasoning gives the leading mean and variance and preserves the divergent squared coefficient of variation. Additional bounded molecular-diffusion contributions do not change these leading disorder moments. If `V=0`, the singular term is absent and (11) is not the applicable asymptotic; the bulk remainder remains bounded instead.

## Independent numerical checks

I solved the periodic finite-difference resolvent on 8,192 points and used a shift-invert eigenvalue solve for its smallest eigenvalue. For each `D`, offsets included `0,0.5,1.5,2` and `1+D^(1/3) z` for `z=-10,-3,-1,0,1,3,10`, clipped to `[0,2]`; the negative-offset side is identical by symmetry.

| D | sampled maximum of `||kh-1||²/D^(1/6)` | minimum scaled gap | maximum scaled J |
|---:|---:|---:|---:|
| 1e-3 | 3.11999076 | 0.53364545 | 10.31003590 |
| 1e-4 | 3.13791338 | 0.53462823 | 10.03102047 |
| 1e-5 | 3.14621017 | 0.53508222 | 9.90653128 |
| 1e-6 | 3.15004870 | 0.53529196 | 9.84978146 |

The gap and `J` were divided by their corresponding piecewise scales in (1). The sampled maximum of the flux quantity occurred at `c=1` in every run. These calculations support the uniform exponents but do not prove a supremum over the continuum of offsets or establish mesh convergence; those claims rest on the analytic estimates above.
