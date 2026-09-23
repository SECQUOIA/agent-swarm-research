# Rigorous diffusion bounds from cross-section transport

Date: 2026-09-06. Status: **the planar inequality is a rediscovery of the classical Ahlfors–Warschawski conformal-modulus bound**, identified during independent prior-art review. Its derivation and equivalence to a Zwanzig approximation are correct, but the geometric bound is not new. The elliptical-section extension has been independently checked; its twist cost is also related to established torsional rigidity. This note preserves a useful synthesis, not a publishable novelty claim.

## Main result

A common approximation for diffusion in a corrugated channel is also a rigorous lower bound under the assumptions below. This follows from a classical conformal-modulus inequality, as well as the direct current proof given here. The true long-time diffusion cannot be smaller than this prediction, even when it is an inaccurate approximation. The ordinary Fick–Jacobs expression supplies the upper bound. Neither inequality needs a small wall slope or a narrow channel.

Let a planar channel have smooth, positive, periodic width `W(x)` and periodic midline `m(x)`, period `ell`:

\[
\Omega=\{(x,y):m(x)-W(x)/2<y<m(x)+W(x)/2\}.
\]

A point tracer undergoes Brownian motion of constant isotropic diffusivity `D`, reflects at the walls, and experiences no force. Angular brackets mean a spatial average over one period, and `D_eff` means the long-time diffusion coefficient of the **axial Cartesian position**, not distance along the midline. Then

\[
\boxed{
\frac{D}{\langle W\rangle\left\langle
[1+m'^2+W'^2/12]/W\right\rangle}
\le D_{\rm eff}\le
\frac{D}{\langle W\rangle\langle1/W\rangle}.}
\tag{1}
\]

This is a corollary of the conditional transport argument in [the capacity note](capacity-certificates.md), but hard moving boundaries are best treated directly.

## Proof and normalization

Let `G` be the minimum of `D integral_cell |grad u|^2` over potentials satisfying the quasiperiodic condition `u(x+ell,y)=u(x,y)+1`. The cell problem for reflecting periodic Brownian diffusion gives

\[
D_{\rm eff}=\frac{\ell^2}{|\Omega_{\rm cell}|}G
=\frac{\ell}{\langle W\rangle}G.
\]

This is a periodic conductance problem; imposing separate constant-potential inlet and outlet faces would generally be a different problem.

Restricting `u` to a function of `x` gives `G <= D/integral_0^ell dx/W`, yielding the upper bound.

For the lower bound take a periodic unit current

\[
J_x=\frac1W,\qquad
J_y=\frac{m'+(W'/W)(y-m)}W.
\]

Direct differentiation gives `partial_x J_x + partial_y J_y=0`. At the two walls, `J_y/J_x=m'±W'/2`, exactly the wall slope, so the current has no normal component. Its section flux is one. The current resistance is

\[
R=\frac1D\int_0^\ell\frac{1+m'^2+W'^2/12}{W}\,dx,
\]

because a uniform section has `E(y-m)=0` and `E[(y-m)^2]=W^2/12`. For every unit-drop potential, `integral_cell J dot grad u=1`, and weighted Cauchy–Schwarz implies `G>=1/R`. Combining with the cell normalization proves (1).

The correction contains separate costs for translation and dilation of a section. A constant-width serpentine channel has no entropic free-energy barrier but can still have a transport penalty. This mechanism is established curved-channel physics; the potentially new statement is a finite-slope guaranteed inequality.

## Relation to Zwanzig's expression

For `m=0` and `W=2 epsilon zeta(x)` in the notation used by Mangeat, Guerin and Dean (2017), the lower side of (1) is

\[
\frac{D_{\rm lower}}D=
\frac1{\langle\zeta\rangle\langle\zeta^{-1}\rangle}
\left[1+\frac{\epsilon^2\langle\zeta'^2/\zeta\rangle}
{3\langle\zeta^{-1}\rangle}\right]^{-1}.
\tag{2}
\]

This is exactly their Eq. (120), attributed to Zwanzig's resummation. Their discussion treats it as an approximation, which can become inaccurate for wide channels. The present lower-bound interpretation is fully compatible with that failure: it may become small while the true diffusion stays bounded away from zero.

The formula itself and its underlying universal geometric inequality are **not new**. The independent reviewer found the exact width/midline expression in the Ahlfors–Warschawski modulus bound, stated as Theorem 8.1 in a [primary mathematical survey](https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&option_lang=eng&paperid=10076&what=fullteng). A diffusion-focused explanation of this connection may be useful, but it does not establish a new theoretical bound. Kalinay and Percus's 2005 variational work is additional relevant context.

## General cross sections

Let `S_x` be a smooth periodic family of bounded transverse cross sections in `R^p`, with volume `A(x)`. Let `nu_x` be the uniform probability measure on `S_x`. Among velocities transporting this family, define

\[
\mathfrak g(x)=\min_v\int_{S_x}|v(y)|^2\nu_x(dy),
\quad \partial_x\nu_x+\nabla_y\cdot(\nu_xv)=0
\tag{3}
\]

where the continuity equation is distributional and includes motion of the section boundary. The gradient solution minimizes this kinetic cost. If a finite-energy solution exists, the same unit current `J=(nu_x,nu_x v)` gives

\[
\frac{D}{\langle A\rangle\langle(1+\mathfrak g)/A\rangle}
\le D_{\rm eff}\le
\frac{D}{\langle A\rangle\langle1/A\rangle}.
\tag{4}
\]

This is a shape-transport formulation of the bound. It is a direct application of established optimal transport and conductivity principles; no new metric is being proposed.

For a translating circular section of radius `R(x)`, the velocity `v=m'+(R'/R)(y-m)` is a gradient and
`mathfrak g=|m'|^2+R'^2/2`. Thus the three-dimensional circular-tube counterpart is explicit. A circular section that merely rotates about its center does not change shape and incurs zero cost.

## Elliptical sections: dilation and twist

For a transverse ellipse with center `m(x)`, semiaxes `a(x),b(x)>0`, and orientation `theta(x)`, the covariance of its uniform measure is

\[
\Sigma=\tfrac14 R_\theta\operatorname{diag}(a^2,b^2)R_\theta^T.
\]

Let the symmetric matrix `B` solve the Sylvester equation

\[
B\Sigma+\Sigma B=\Sigma'.
\]

The affine gradient velocity `v=m'+B(y-m)` transports the uniform ellipse: the covariance evolution transports its defining quadratic form and the trace of `B` accounts for the density normalization. It minimizes (3), since any other admissible current differs by a measure-divergence-free current orthogonal to gradients. Consequently

\[
\mathfrak g=|m'|^2+\operatorname{tr}(B\Sigma B)
=|m'|^2+\frac14\left[a'^2+b'^2+
\frac{(a^2-b^2)^2}{a^2+b^2}\theta'^2\right].
\tag{5}
\]

The circular limit makes the twist term vanish. A rigid rotational velocity would cost `(a^2+b^2)theta'^2/4`; it is not the minimum-cost transport of the **unlabelled section distribution** and gives a weaker bound. The difference matters especially near a circular section.

Substitute `A=pi a b` and (5) into (4) to obtain an explicit all-slope, all-twist bound. For fixed semiaxes and constant twist rate compatible with periodicity, it reads

\[
\frac{D}{1+\frac{(a^2-b^2)^2}{4(a^2+b^2)}\theta'^2}
\le D_{\rm eff}\le D.
\tag{6}
\]

Equation (6) has been independently checked as a corollary, but does not assert that twist changes diffusion by exactly that amount. A constant upper bound does not identify a nonzero slowdown. The shape coefficient is the polar area moment minus Saint-Venant torsional rigidity, divided by section area, which is established geometry. No novelty claim is made for that coefficient.

## Evidence and remaining work

- Independent derivation of (1), including periodic normalization: [review](verification/capacity-independent-review.md).
- Mangeat, Guerin and Dean, *Dispersion in two-dimensional channels—the Fick–Jacobs approximation revisited* (2017), [open author PDF](https://www.mangeatm.fr/papers/mangeat_guerin_2017_dispersion.pdf), Eq. (120) and nearby discussion. This establishes the formula's prior existence.
- Kalinay and Percus, *Extended Fick–Jacobs equation: Variational approach* (2005), [DOI](https://doi.org/10.1103/PhysRevE.72.061203). Open full text retrieved by the prior-art reviewer.
- Legoll and Lelievre, [arXiv:0906.4865](https://arxiv.org/abs/0906.4865), for known limitations of projected stiff dynamics.

The prior-art search further found general weighted modulus theory for tubes of solenoidal trajectories (Ohtsuka, cited by Brakalova, Markina and Vasil'ev, [arXiv:1409.1626](https://arxiv.org/abs/1409.1626)). Such results may subsume higher-dimensional flow constructions. Further numerical checks may illustrate the formulas, but cannot restore novelty. See the [independent prior-art report](verification/capacity-prior-art.md) for details as the audit is completed.
