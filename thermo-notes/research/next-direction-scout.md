# Next direction: finite-reservoir limits on droplet coexistence

Date: 2026-09-06. Status: independently verified application of standard constrained-stability algebra; this research pass is closed. See the [proof and scope review](verification/droplet-reservoir-review.md). No novelty or publishability claim. The single-phase conclusion is classical Ostwald instability; the potentially useful extension is a quantitative susceptibility-metric separation criterion for distinct droplets in a finite multicomponent reservoir.

## Physical question and relevance

A small closed reservoir can stabilize a droplet that would be a critical nucleus in an open system. Can it stabilize an emulsion, or several different condensates at once? A count of conserved components alone is insufficient: compositionally similar droplets compete for almost the same reservoir response. The calculation below predicts a quantitative penalty as their depletion vectors become parallel.

This connects finite-system nucleation and constrained metastability to the thermodynamics of multicomponent condensates. It offers an observable stability criterion involving bulk susceptibilities, interfacial free energies, and compositions. Its physical scope is potentially broader than a bath-size threshold for convergence of complete energy distributions, but the underlying algebra is elementary and needs a convincing new application.

## Exact local decomposition, including nonlinear loads

Let x_i describe the internal state of droplet i, with local free energy f_i(x_i) and vector of r exchanged extensive quantities Q_i(x_i). All free energies must use a consistent potential and fixed external controls. Let the equilibrated background/reservoir have free energy B(Y), where

\[
 Y=Y_{\rm tot}-\sum_{i=1}^{m}Q_i(x_i),\qquad
 F(x_1,\ldots,x_m)=\sum_i f_i(x_i)+B(Y).
\]

Droplets are separated enough that direct interactions, overlap, and confinement forces can be neglected. At a stationary state let μ=∇B(Y), K=∇²B(Y), and

\[
 G_i=\nabla^2\bigl[f_i(x_i)-\mu\cdot Q_i(x_i)\bigr],
 \qquad J=(DQ_1,\ldots,DQ_m).
\]

Here μ is held fixed when taking each local Hessian. The exact full Hessian is

\[
 \boxed{H=\operatorname{diag}(G_1,\ldots,G_m)+J^TKJ.}\tag{1}
\]

For nonlinear Q_i, the −Σ_a μ_a∇²Q_{ia} terms are essential. They are already included in G_i. Omitting them and using raw ∇²f_i is generally incorrect. This identity holds without a Gaussian expansion of B; K is its exact local curvature.

If each isolated droplet has at least one negative grand-potential mode at the current reservoir conjugates, the block diagonal matrix has at least m negative modes. Since rank(JᵀKJ)≤r,

\[
 \boxed{n_-(H)\geq m-r.}\tag{2}
\]

**Proof:** the negative subspace of the block diagonal matrix intersects ker J in dimension at least m−r. On this intersection the reservoir correction vanishes and the quadratic form remains strictly negative. No sign assumption on K is needed for the lower bound. When K is positive semidefinite, the reservoir cannot add negative modes, and removes no more than r of them.

More precisely choose one negative direction u_i in each droplet, normalize its negative quadratic cost as u_iᵀG_i u_i=−d_i<0, and set b_i=DQ_i u_i. On their m-dimensional span,

\[
 H_{\rm rad}=-D+\mathcal B^TK\mathcal B,
 \quad D=\operatorname{diag}(d_i),\quad
 \mathcal B=(b_1,\ldots,b_m).
\]

For K positive semidefinite, a necessary condition for strict quadratic stability of the full state is

\[
 \boxed{\sigma_{\min}\left(K^{1/2}\mathcal B D^{-1/2}\right)>1,}\tag{3}
\]

with the convention that missing singular directions have zero singular value. This is necessary and sufficient on the chosen negative-mode subspace. It is **not** sufficient for full stability when extra internal, shape, or composition modes remain. For a model whose only coordinates are these amplitudes, it is sufficient.

Thus merely having m≤r is not enough. Reservoir-load vectors must be linearly independent *and* sufficiently separated in the susceptibility metric.

## Concrete two-droplet capillary model

At fixed temperature, let v_i>0 be the volume of a spherical droplet of phase i. Approximate the phase compositions and surface tensions as constant over the perturbations, and use

\[
 F(v_1,v_2)=\sum_i[a_i v_i^{2/3}-g_i v_i]
 +\frac{1}{2V_b}(y_0-\mathcal Bv)^T\chi^{-1}(y_0-\mathcal Bv),
 \qquad a_i=(36\pi)^{1/3}\gamma_i.
\]

Here b_i is the vector of bulk excess component density of phase i relative to the background, χ=∂ρ/∂μ is the positive definite background susceptibility on the independent composition space, and V_b is its reference volume. This quadratic reservoir model is a local approximation. Background-volume changes and composition relaxation must be added for a quantitatively complete incompressible solution model.

At a stationary pair with v_1=v_2=v and a_1=a_2=a,

\[
 d=\frac{2a}{9}v^{-4/3},\qquad
 H=-dI+\frac1{V_b}\mathcal B^T\chi^{-1}\mathcal B.
\]

Assume equal susceptibility-metric load norms,

\[
 b_1^T\chi^{-1}b_1=b_2^T\chi^{-1}b_2=s^2,
 \qquad
 c=\frac{b_1^T\chi^{-1}b_2}{s^2}\in[-1,1].
\]

The Hessian eigenvalues are exactly

\[
 h_\pm=-d+\frac{s^2}{V_b}(1\pm c).
\]

Both size modes are strictly quadratically stable precisely when

\[
 \boxed{V_b<\frac{s^2}{d}(1-|c|)
 =\frac{9s^2}{2a}v^{4/3}(1-|c|).}\tag{4}
\]

Writing c=cosθ for the angle between the two loads in the χ⁻¹ metric, nearly parallel or antiparallel loads require

\[
 V_b<\frac{9s^2}{4a}v^{4/3}\theta^2+O(\theta^4)
\]

near θ=0 (use π−θ near antiparallel loads). Equivalently, for fixed V_b the minimum droplet volume scales as θ^(−3/2), and its radius scales as θ^(−1/2), at fixed a and s. The scaling is not universal near a bulk critical point because a, s, and χ then also vary.

The mechanism is explicit: the weak mode exchanges volume between droplets while almost cancelling total depletion. A reservoir barely senses that perturbation, so it cannot overcome surface-energy concavity. This is an angle-dependent strengthening of the simple conserved-quantity count. It can be tested by computing the spectrum of size fluctuations as reservoir volume or mixture composition varies.

The stationary state itself must exist and the local expansion must be self-consistent. For full-rank two-phase loads, one can choose two independent background conjugates to satisfy the two stationarity equations; this is a local construction, not a guarantee for an arbitrary phase diagram. One must also check the reservoir remains thermodynamically stable and no other phase or morphology wins globally.

## Same-phase and kinetic consequences: retained as known limits

For identical droplets at identical states, all b_i are equal. The reservoir correction on their radial modes has rank one regardless of how many thermodynamic quantities the reservoir exchanges. If their individual radial curvature is −d, the restricted radial quadratic form has m−1 exchange eigenvalues equal to −d. These are eigenvalues of the full Hessian only when the radial directions form an invariant subspace; in either case they are negative quadratic directions of the full state. Arbitrarily stiff global constraints therefore cannot stabilize multiple identical critical droplets. This is the standard Ostwald-ripening mechanism in Hessian language; it is not claimed new.

For gradient dynamics \dot x=−M(x)∇F with a positive definite mobility M, the stationary linearization is −MH. It is similar to −M^(1/2)HM^(1/2), so the number of growing modes equals n_−(H). The rank obstruction therefore survives arbitrary positive dissipative kinetic couplings. A mobility with null directions can kinetically freeze an unstable mode; this is not thermodynamic stabilization.

Individually trapped insoluble material, anchored polymers, local elastic confinement, charged interfaces, nonlocal interactions, and sustained chemical reactions lie outside the simple common-reservoir model. Trapped material contributes separate per-droplet constraints, so the effective number of stabilizing quantities can scale with droplet number. These established mechanisms are not counterexamples to (2).

## Relation to the Gibbs phase rule and novelty risk

The Gibbs phase rule counts independently coexisting bulk phases and their intensive degrees of freedom. Equation (2) instead counts local negative modes of finite nuclei under a specified reservoir coupling. Multiple copies of one phase count separately here, even though they are one Gibbs phase. Equation (3) supplies a quantitative conditioning requirement absent from a bare phase count. Nevertheless, this distinction does not establish novelty: constrained Morse-index arguments and multicomponent stability calculations are long-established, and the result might already exist in interfacial thermodynamics or coarsening literature.

The most defensible candidate contribution is a physical study showing that susceptibility-metric near-collinearity destabilizes distinct finite droplets despite an adequate number of conserved components, with equation (4) as a prediction. The general rank bound alone is unlikely to support a strong paper.

## Closest open primary work inspected

- Ø. Wilhelmsen, D. Bedeaux, S. Kjelstrup, and D. Reguera, *Thermodynamic stability of nanosized multicomponent bubbles/droplets: The square gradient theory and the capillary approach*, J. Chem. Phys. 140, 024704 (2014), DOI <https://doi.org/10.1063/1.4860495>. Open institutional article: <https://diposit.ub.edu/server/api/core/bitstreams/bd04fd66-275a-49ef-87ba-275d0a34f727/content>. It compares second variations and capillary Hessians for single- and two-component canonical droplets and shows finite minimum sizes. This already establishes the reservoir-stabilization and Hessian framework; a multi-droplet angle criterion must add something beyond it. The full capillary Hessian was subsequently inspected; see the follow-up audit below.
- D. Zwicker, A. A. Hyman, and F. Jülicher, *Suppression of Ostwald ripening in active emulsions*, Phys. Rev. E 92, 012317 (2015), DOI <https://doi.org/10.1103/PhysRevE.92.012317>. Open author PDF: <https://www.pks.mpg.de/fileadmin/user_upload/MPIPKS/group_pages/BiologicalPhysics/juelicher/publications/2015/SpORiAE2015.pdf>. Appendix D explicitly derives an (N−1)-fold droplet-exchange eigenvalue and says its eigenspace preserves background composition and total droplet volume. The identical-droplet/global-feedback no-go is consequently a **negative novelty finding**, not a new mechanism.
- Y. Qiang, C. Luo, and D. Zwicker, *Scaling laws for phase coexistence in multicomponent mixtures*, Phys. Rev. Research 7, 043008 (2025), DOI <https://doi.org/10.1103/zcvb-9t4b>. Open institutional PDF: <https://pure.mpg.de/pubman/item/item_3678017_2/component/file_3678153/Publisher%2BVersion.pdf>. It studies the number of equilibrium phases and metastable multi-droplet configurations in finite mixtures. Its emphasis is generic interaction/composition scaling, not a local reservoir-angle bound. Sections II, IV, VIII, IX were inspected through available full text; a detailed supplement search remains.
- The recently surfaced JACS paper *Computing Nucleation Rates from Confined Equilibria: The Critical Cluster Equivalence Principle*, DOI <https://doi.org/10.1021/jacs.6c09002>, directly treats the open/closed stability reversal for single clusters. Single-cluster stability reversal is established and cannot be presented as this work's novelty.

Searches included “finite reservoir Ostwald stability droplets,” “droplets rank stability reservoir,” “multiple droplets canonical unstable,” “droplet stability rank-one,” “Ostwald ripening global feedback,” “droplets Gibbs phase rule stability,” and multicomponent/Hessian/finite-reservoir combinations. No exact match to equation (4) was found in this limited search. This does not establish novelty.

## Other directions rejected or deferred in this scout

1. A global feedback control cannot arrest identical-droplet coarsening: physically useful but directly overlaps the droplet-exchange modes in Zwicker et al. (2015).
2. Finite-bath correction involving surface adsorption, ΔF_b≈(ΔρV+ΓA)ᵀχ⁻¹(ΔρV+ΓA)/(2V_b), would generate R⁶/V_b, R⁵/V_b, and R⁴/V_b terms. This could contaminate curvature fits, but it is a direct depletion expansion and prior work already treats adsorption in multicomponent finite-drop nucleation. Source surfaced: Djikaev, Tabazadeh, Reiss, *Thermodynamics of crystal nucleation in multicomponent drops: The effects of surface adsorption and dissociation*, JCP 118, 6572 (2003), listed by NASA at <https://airbornescience.nasa.gov/content/Thermodynamics_of_crystal_nucleation_in_multicomponent_drops_The_effects_of_surface>. Deferred pending primary full-text inspection; no novelty claim.
3. Finite-reservoir shape stabilization by global volume control only changes a monopole mode and leaves volume-preserving capillary modes untouched at quadratic order. This is another familiar constrained-stability consequence rather than a strong new research direction by itself.

## Final disposition

Independent review verified (1)–(7), including thermodynamic-potential conventions, composition relaxation, and the limits of radial tests. Strict inequalities refer to positive Hessians; a zero mode can be stabilized by higher-order terms and is not excluded as a degenerate local minimum. The general strong-reservoir criterion and a counterexample to radial sufficiency are recorded in the review. A concrete mixture realization was not developed. Given the substantial prior art, this note is retained as a mathematical synthesis and possible application, without a claim of new physical behavior.

## Extension: internal composition relaxation screens reservoir stabilization

A reservoir-only Hessian can overestimate stability because droplets can also change their compositions or densities. This correction can be derived exactly at quadratic order. It is another standard Schur-complement identity; the candidate physical contribution is its use in a droplet-distinguishability criterion.

Let x collect size amplitudes and y stable internal droplet modes. Write the *open-reservoir* quadratic form as

\[
 \frac12x^TGx+x^TPy+\frac12y^TCy,\qquad C\succ0,
\]

and linearized total load as Bx+Ay. Adding the reservoir gives (Bx+Ay)ᵀK(Bx+Ay)/2, with K≻0. Complete the open-reservoir square by y′=y+C⁻¹Pᵀx. Define

\[
 G_{\rm rel}=G-PC^{-1}P^T,\qquad
 \widetilde B=B-AC^{-1}P^T,\qquad
 S=AC^{-1}A^T.
\]

After minimizing over y′, the exact size Hessian is

\[
 \boxed{H_{\rm size}=G_{\rm rel}
 +\widetilde B^T(K^{-1}+S)^{-1}\widetilde B.}\tag{5}
\]

The matrix S is the susceptibility contributed by the stable internal modes of the droplets at fixed size. Since (K⁻¹+S)⁻¹⪯K, internal relaxation weakens reservoir stabilization relative to freezing these modes. The comparison must use the relaxed load \widetilde B and open curvature Grel; comparing with a different unrelaxed size coordinate would mix effects.

If S≻0, increasing external reservoir stiffness without bound only produces the finite limit

\[
 H_{\rm size}\longrightarrow G_{\rm rel}+\widetilde B^TS^{-1}\widetilde B.
\]

If this limiting matrix has a strictly negative eigenvalue, **no positive external reservoir stiffness can stabilize the specified stationary state against size perturbations**, even if the number of conserved components is adequate and the load vectors have full rank. This is an internal-compliance obstruction. A zero limiting eigenvalue precludes strict positive definiteness in that direction at finite positive K⁻¹, but the clean robust statement above uses a strict negative eigenvalue.

For an explicit symmetric model, take Grel=−dI, K⁻¹=Vb χb I, S=s_d I, and equal Euclidean load norms |b_i|=b with correlation c. The criterion becomes

\[
 \boxed{V_b\chi_b+s_d<\frac{b^2}{d}(1-|c|).}\tag{6}
\]

The finite reservoir is not the only compliance: composition fluctuations inside the droplets consume the stabilization available from conservation. If s_d=2vχd and d=2av^(−4/3)/9 in the symmetric capillary example, stability requires

\[
 V_b\chi_b+2v\chi_d<\frac{9b^2}{2a}v^{4/3}(1-|c|).
\]

Even allowing arbitrary external stiffness, a necessary condition is therefore

\[
 \boxed{v^{1/3}>\frac{4a\chi_d}{9b^2(1-|c|)}.}\tag{7}
\]

At fixed constitutive coefficients and nearly parallel loads this lower bound on a linear droplet size grows as angle⁻². This stronger dependence differs from the angle⁻¹/² threshold of the frozen-composition, finite-external-bath example. Neither exponent is claimed universal as phases approach a critical point, where the constitutive coefficients also vary.

Equation (7) could be a useful prospective prediction: two weakly distinguishable condensates might fail to coexist stably even in an arbitrarily small reservoir, because internal composition response defeats the global constraint. But Wilhelmsen et al. (2014) already established minimum stable radii for individual compressible/multicomponent droplets, so this is potentially a multibody angular refinement of a known mechanism, not a discovery of a minimum-size mechanism itself. The explicit isotropic S=2vχd model is illustrative and requires an actual mixture model before any physical novelty claim.

### Follow-up primary-source audit

The open Wilhelmsen et al. (2014) PDF was downloaded and its capillary derivation and conclusions inspected in detail. Printed p.024704-5, equations (29)–(35), explicitly includes radius/volume and all component particle numbers in a joint Hessian. Its particle-number block contains the sum of internal and external chemical-potential derivatives; its mixed block contains both phases' pressure/composition derivatives. Therefore composition relaxation and reservoir susceptibility are already structurally present in that paper, even though the matrix screening form (5) is not written there. Printed pp.024704-8–9 compare local and global stability and discuss minimum stable radii. The appropriate novelty target is consequently a *multiple-distinct-droplet conditioning criterion*, not internal compressibility or finite-radius stabilization.

Further close predecessors identified from its bibliography are Yang, *The thermodynamical stability of the heterogeneous system with a spherical interface*, JCP 82, 2082 (1985), DOI <https://doi.org/10.1063/1.448344>; Reguera and Reiss, *Nucleation in confined ideal binary mixtures: The Renninger–Wilemski problem revisited*, JCP 119, 1533–1546 (2003), DOI <https://doi.org/10.1063/1.1579685>; and Glavatskiy, Reguera, Bedeaux, *Effect of compressibility in bubble formation in closed systems*, JCP 138, 204708 (2013), DOI <https://doi.org/10.1063/1.4807323>. Their full texts were not obtained in this bounded scout. They are specific outstanding prior-art checks, not sources for an assertion that the present formula is absent from prior work.

Targeted searches for droplets/composition/Schur-complement and droplets/susceptibility/angle did not return a direct primary-source match to equations (4), (6), or (7). Given the elementary matrix derivation and extensive older stability literature, this negative search result provides only weak novelty evidence.
