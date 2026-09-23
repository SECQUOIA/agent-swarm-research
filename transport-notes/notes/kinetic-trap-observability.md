# Which velocity observables detect slow kinetic traps?

Status: independently derived and checked mathematical corollary, 2026-09-06. This generalizes the model in [the singular-exchange review](review-singular-exchange.md). The projection principle behind the result is standard spectral reasoning; novelty of this application has not been established.

A quadratic zero of the exchange rate produces divergent axial dispersion only when the local wall velocity differs from the overall mean velocity. Matching these velocities removes the divergence, even though transverse equilibration remains slow. For an immobile wall and vector transport, the divergent part of the dispersion tensor has rank at most one and points along the mean displacement velocity.

## Assumptions and exact formula

Let a fixed bounded connected smooth cross-section `Omega` have area `A` and wall length `P`. Bulk transverse diffusivity is `Db>0`; wall transverse diffusivity is `Ds>0`. Exchange rates are `k_delta(s)=delta+k0(s)` from wall to bulk and `K k_delta(s)` in the reverse direction, with constant `K>0`. The function `k0` is nonnegative and `C2`, with finitely many nondegenerate quadratic zeros `s_j`:

\[
k_0(s)=a_j(s-s_j)^2+o((s-s_j)^2),\qquad a_j>0.
\]

Write `Z=A+KP`. Let `u(y)` be a prescribed longitudinal bulk drift and `w(s)` a prescribed longitudinal wall drift. The latter is a velocity in the transported coordinate, not advection around the wall coordinate `s`. All coefficients are independent of the transported coordinate, so these velocities leave the transverse invariant measure unchanged. Assume `u` belongs to `L2(Omega)` and `w` is `C1` on the wall.

Define

\[
V={\int_\Omega u+K\int_{\partial\Omega}w\over Z},
\quad g_b=u-V,\quad g_s=w-V,
\quad H=-D_s\partial_s^2+k_\delta.
\]

Then `int g_b+K int g_s=0`. Eliminating the surface cell field from the reversible variational principle gives the exact decomposition

\[
D_{\rm flow}={K\over Z}\langle g_s,H^{-1}g_s\rangle+R_D,
\tag{1}
\]

where

\[
\begin{aligned}
ZR_D=\sup_b\{&2\int_\Omega g_b b
+2K\int_{\partial\Omega}k_\delta(H^{-1}g_s)b
-D_b\int_\Omega|\nabla b|^2\\
&-K\langle b,(k_\delta-k_\delta H^{-1}k_\delta)b\rangle\}.
\end{aligned}
\tag{2}
\]

The surface cell field at the maximizing bulk field is `H^-1(k_delta b+g_s)`. Thus the sign of the wall contribution to the bulk load is positive in (2). The immobile case `g_s=-V` recovers the negative sign in the earlier review.

The last quadratic form in (2) is nonnegative. Also

\[
\int k_\delta H^{-1}g_s=\int g_s,
\]

so the bulk linear functional annihilates constants. The same trace and Poincare argument as in the earlier review therefore applies once its wall load is bounded in `L2`.

## Bounded and convergent bulk correction

Set `q=H^-1 g_s`. Multiplying `Hq=g_s` by `k_delta q` gives

\[
\|k_\delta q\|_2^2+D_s\int k_\delta|q'|^2
=\int g_s k_\delta q+{D_s\over2}\int k_0''q^2.
\tag{3}
\]

The spectral estimate `lambda_min(H)>=delta+c sqrt(Ds)` gives `Ds||q||_2^2<=C||g_s||_2^2`. Cauchy–Schwarz in (3) therefore bounds `||k_delta q||_2` uniformly. Consequently

\[
0\le R_D\le C.
\tag{4}
\]

One can also identify its limit. Let `h=H^-1 1` and `J=int h`. Positivity of the inverse gives `|q|<=||g_s||_infinity h`, and the bounds in the earlier review imply

\[
\langle g_s,H^{-1}g_s\rangle\le\|g_s\|_\infty^2J=O(D_s^{-1/4}),
\quad D_s\|q\|_2^2=O(D_s^{1/4}),
\quad D_s\|q'\|_2^2=O(D_s^{-1/4}).
\]

Using (3) and `k_delta q=g_s+Ds q''`, integration by parts gives

\[
\begin{aligned}
\|k_\delta q-g_s\|_2^2
&\le D_s\int g_s' q'
+{D_s\over2}\|k_0''\|_\infty\|q\|_2^2\\
&=O(D_s^{1/4})\longrightarrow0.
\end{aligned}
\tag{5}
\]

The first term is bounded in magnitude by `O(Ds^3/8)`; the last bound records the larger of the two estimates. Thus the linear load in (2) converges in the energy dual norm. The Schur penalty is nonnegative and tends to zero on every fixed smooth bulk test field because it is at most `Ds` times the squared wall derivative of that trace. The upper-bound and dense-test-field argument from the earlier review proves

\[
R_D\longrightarrow R_0={D_b\over Z}\int_\Omega|\nabla b_0|^2,
\tag{6}
\]

where the mean-zero Neumann solution satisfies

\[
-D_b\Delta b_0=g_b,
\qquad D_b\partial_n b_0=K g_s.
\tag{7}
\]

The compatibility condition is exactly the centering identity. These conclusions are uniform for additive floors `delta>=0`, with fixed `g_b,g_s`. As before, `Db` must stay strictly positive.

## Leading singular term and cancellation

Dirichlet–Neumann bracketing and the harmonic-oscillator comparison in the earlier review give, uniformly for bounded `delta/sqrt(Ds)`,

\[
\langle g_s,H^{-1}g_s\rangle
=D_s^{-1/4}\sum_j g_s(s_j)^2a_j^{-3/4}
\mathcal C\!\left({\delta\over\sqrt{a_jD_s}}\right)
+o(D_s^{-1/4}),
\tag{8}
\]

with

\[
\mathcal C(z)={\pi\over2}
{\Gamma((z+1)/4)\over\Gamma((z+3)/4)}.
\]

To check the source dependence, on a fixed neighborhood of `s_j` write `g_s=g_s(s_j)+r_j`. Since `r_j=O(s-s_j)`, the quadratic form of its remainder is bounded by `int r_j^2/k_delta=O(1)`. The inverse-operator Cauchy–Schwarz inequality then bounds its cross term with the constant source by `O(Ds^-1/8)`. This is smaller than the `Ds^-1/4` leading term. The source contribution away from the wells is bounded. These observations justify replacing the source by its value at each minimum in the leading local term.

In particular, if

\[
w(s_j)=V\quad\text{at every zero of }k_0,
\tag{9}
\]

then smoothness gives `int g_s^2/k0<infinity`. The variational inequality `H>=k_delta>=k0` implies

\[
0\le\langle g_s,H^{-1}g_s\rangle
\le\int{g_s^2\over k_0}<\infty.
\tag{10}
\]

Together with (4), this proves bounded axial dispersion despite arbitrarily slow local exchange. This stronger boundedness conclusion does not follow merely by setting the coefficient in (8) to zero; it needs (10).

If `Ds` and `delta` both approach zero, fixed smooth trial functions supported away from the zeros give the matching lower bound in the variational formula. Hence, under (9),

\[
D_{\rm flow}\longrightarrow
{K\over Z}\int{[w(s)-V]^2\over k_0(s)}\,ds
+{D_b\over Z}\int_\Omega|\nabla b_0|^2.
\tag{11}
\]

For zero surface diffusion and a positive floor, (11) with `k0` replaced by `k_delta` is an exact identity. The finite limit at zero floor concerns the diffusivity quadratic form; it does not require the limiting cell field itself to belong to unweighted `L2`, which can fail because `g_s/k0` may behave as `1/(s-s_j)`.

The cancellation condition is specific to this velocity observable. It removes its singular dispersion contribution; it does not remove slow state relaxation or imply that other observables are insensitive to the wells.

## Vector transport and rank of the singular tensor

For an additive vector displacement, replace `u,w,V` by vectors. Apply the scalar result to every directional observable `e dot u, e dot w`. Polarization gives the leading flow-dispersion tensor

\[
\mathbf D_{\rm sing}
={K\over Z}D_s^{-1/4}\sum_j a_j^{-3/4}
\mathcal C\!\left({\delta\over\sqrt{a_jD_s}}\right)
[\mathbf w(s_j)-\mathbf V][\mathbf w(s_j)-\mathbf V]^T.
\tag{12}
\]

The remainder after subtracting the exact surface resolvent tensor is positive semidefinite and bounded, with a finite limit described by the bulk Neumann fields. The singular tensor has rank equal to the dimension of the span of the nonzero vectors `w(s_j)-V` when their scaled weights remain positive and comparable.

For an immobile wall, every vector in (12) equals `-V`, so

\[
\mathbf D_{\rm sing}
={K\over Z}D_s^{-1/4}
\left[\sum_j a_j^{-3/4}\mathcal C\!\left({\delta\over\sqrt{a_jD_s}}\right)\right]
\mathbf V\mathbf V^T.
\tag{13}
\]

Thus the divergent part has rank at most one. Any direction perpendicular to the mean velocity has bounded dispersion. If the mean velocity vanishes, the entire flow-induced dispersion remains bounded, even with a nonuniform bulk velocity field. These statements concern the model's additive transport observables and exclude independently imposed divergent molecular diffusivities.

## Interpretation and novelty status

The new quantitative content relative to the base calculation is the explicit coefficient `g_s(s_j)^2` and its tensor form. The general principle that a slow mode contributes to dispersion according to its overlap with a centered velocity is inherent in Green–Kubo and cell-problem theory. It would be misleading to present that principle as a new discovery. This note records a useful, mathematically verified corollary of the surface-exchange asymptotics; an independent literature comparison is needed before making a publication claim.
