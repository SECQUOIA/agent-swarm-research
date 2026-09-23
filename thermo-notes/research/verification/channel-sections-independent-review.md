# Independent review: general and elliptical section transport

Reviewer: `capacity_review`. Date: 2026-09-06. Scope: Equations (3)–(6) in `research/channel-diffusion-bounds.md`.

**Verdict:** all four equations are correct under smooth periodic geometry, positive section volume, and finite-energy transport solvability. The ellipse coefficient and its circular limit check exactly. The pure-twist coefficient is a classical Saint-Venant warping-energy quantity, so it should not be described as a new shape metric. The parent reports that the planar inequality is already an Ahlfors–Warschawski conformal-modulus bound; its novelty status must be revised accordingly.

## 1. Arbitrary cross sections

Write the normalized section density as the distribution

\[
\nu_x(y)=\frac{\mathbf1_{S_x}(y)}{A(x)}.
\]

Let `V_n` be the outward normal velocity of the section boundary as `x` increases. The distributional continuity equation in (3) is equivalent to

\[
\operatorname{div}_y v=A'/A\quad\hbox{inside }S_x,
\qquad v\cdot n=V_n\quad\hbox{on }\partial S_x.
\]

The divergence theorem compatibility condition is exactly the volume derivative identity `integral_boundary V_n=A'`. Among such velocities the minimizer is `v=grad psi`, with

\[
\Delta_y\psi=A'/A,\qquad\partial_n\psi=V_n.
\]

For any other feasible velocity `v+z`, one has `div z=0`, `z dot n=0`, and `integral grad psi dot z=0`. Its kinetic cost is therefore the minimizing cost plus `integral|z|^2/A`. This proves the potential-flow interpretation, including the boundary term omitted by an ordinary interior score formula.

The current `J_x=1/A`, `J_y=v/A` is divergence-free and tangent to the full sloping wall. Its section flux is one. Its resistance per cell is

\[
R=\frac1D\int_0^\ell\frac{1+\mathfrak g(x)}{A(x)}\,dx.
\]

The cell volume is `ell<A>`, and its quasiperiodic unit-drop conductance `G` satisfies `D_eff=ell G/<A>`. Thus Equation (4) follows exactly from the current resistance bound and the projected potential upper bound. All powers of section area and period are correct.

Disconnected sections require componentwise transport compatibility. Total volume compatibility alone does not permit transfer between disconnected components. The finite-energy-solvability qualification in the note is necessary, and a connected smooth section is a convenient sufficient setting. Smooth topology changes should not be assumed to satisfy these conditions automatically.

For a translating two-dimensional disk, `E|y-m|^2=R^2/2`, so `g=|m'|^2+R'^2/2` is correct. More generally, a transverse `p`-ball gives dilation cost `p R'^2/(p+2)`.

## 2. Ellipse transport by a symmetric affine field

Let `H=4 Sigma` be the defining shape matrix, so the ellipse is

\[
(y-m)^TH^{-1}(y-m)<1.
\]

For the affine velocity `v=m'+B(y-m)`, the shape evolves correctly precisely when

\[
H'=BH+HB^T.
\]

For symmetric `B`, this is the proposed Sylvester equation. Since `Sigma` is positive definite, the symmetric solution is unique. Differentiating the determinant gives

\[
\operatorname{tr}B=\tfrac12\operatorname{tr}(\Sigma^{-1}\Sigma')
=A'/A.
\]

The shape derivative gives the required boundary normal speed. Thus the same affine field also transports the uniform density, not merely its covariance. The fact that it is a gradient then proves global minimality among all admissible velocities, including non-affine ones.

At a fixed `x`, rotate into the instantaneous principal-axis frame. Put `lambda_1=a^2/4`, `lambda_2=b^2/4`. In that frame,

\[
\widetilde\Sigma'=
\begin{pmatrix}
a a'/2&\theta'(a^2-b^2)/4\\
\theta'(a^2-b^2)/4&b b'/2
\end{pmatrix},
\quad
\widetilde B=
\begin{pmatrix}
a'/a&\theta'(a^2-b^2)/(a^2+b^2)\\
\theta'(a^2-b^2)/(a^2+b^2)&b'/b
\end{pmatrix}.
\]

The translation–shape cross term is zero because the centered section has mean zero. Therefore

\[
\begin{aligned}
\mathfrak g
&=|m'|^2+\operatorname{tr}(B\Sigma B)\\
&=|m'|^2+\frac{a'^2+b'^2}{4}
+\frac{(a^2-b^2)^2}{4(a^2+b^2)}\theta'^2.
\end{aligned}
\]

This verifies Equation (5). A symbolic SymPy check independently confirmed the Sylvester identity, the trace expression, and the torsion identity below. The result remains finite at `a=b`; orientation itself becomes unidentifiable there, but the matrix formulation remains the reliable representation if axes exchange or orientation coordinates become singular.

Rigid rotational transport uses the antisymmetric field `theta' J(y-m)` and incurs cost `theta'^2(a^2+b^2)/4`. Its excess over the minimizing twist cost is `theta'^2 a^2 b^2/(a^2+b^2)`, which is positive. It carries particles tangentially as well as moving the boundary; section-distribution transport does not require that additional motion.

For constant semiaxes, fixed center, and `theta(x)=omega x+theta_0`, the family is periodic whenever `omega ell` is an integer multiple of `pi` for a noncircular ellipse. Substituting the constant area and cost gives Equation (6). This is a bound on Cartesian axial diffusion, with no small-twist approximation.

## 3. Classical torsion and internal potential flow

For a fixed planar section `S` centered at the rotation axis, let `J(y_1,y_2)=(-y_2,y_1)` and let `psi` solve

\[
\Delta\psi=0\text{ in }S,\qquad
\partial_n\psi=Jy\cdot n\text{ on }\partial S.
\]

The pure-rotation transport field for unit angular speed is `grad psi`. Let

\[
I_p=\int_S|y|^2\,dy,
\qquad
J_{\rm SV}=\min_\varphi\int_S|Jy+\nabla\varphi|^2\,dy.
\]

Here `J_SV` is the Saint-Venant **torsion constant**; the mechanical torsional rigidity includes an additional shear modulus. The minimizer is `varphi=-psi` up to an additive constant. Orthogonality gives

\[
J_{\rm SV}=I_p-\int_S|\nabla\psi|^2\,dy,
\qquad
\boxed{\mathfrak g_{\rm twist}
=\theta'^2\frac{I_p-J_{\rm SV}}{|S|}.}
\]

For the ellipse,

\[
I_p=\frac{\pi ab(a^2+b^2)}4,
\quad J_{\rm SV}=\frac{\pi a^3b^3}{a^2+b^2},
\]

and their difference divided by `pi ab` reproduces (5).

This is the kinetic energy of an **internal irrotational fluid** whose normal velocity follows the rotating section boundary. It should not be conflated with the exterior added moment of inertia of a rotating solid ellipse in an infinite fluid, which has a different coefficient. An [open archived elasticity text, Equation (6.73), printed page 163](https://orbi.uliege.be/bitstream/2268/205837/1/ST_Veubeke_102.pdf) explicitly records the classical identity between the torsion constant, polar moment, and warping-gradient energy. The downloaded file is a scanned 339-page text; the source's indexed excerpt supplied the equation. Full bibliographic identification and a diffusion-specific prior-art comparison remain pending.

## 4. Strict slowdown under nontrivial constant twist

Equation (6) alone does not prove strict slowdown, but the exact cell variational principle does. The constant corrector `chi=0` has energy `D`; it minimizes only if its natural reflecting boundary condition `e_x dot n_wall=0` holds. For a noncircular ellipse with nonzero twist, the wall's axial normal component is nonzero on a set of positive surface measure. Thus `chi=0` fails the first-order optimality condition and cannot minimize. Consequently `D_eff<D` for that geometry. This argument does not give a quantitative minimum slowdown and has no independent novelty claim.
