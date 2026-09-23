# Independent review of droplet stabilization by a common reservoir

Date: 2026-09-06. Reviewed `research/next-direction-scout.md`, including equations (1)–(4) and its subsequently added composition-screening equations (5)–(7). The scouting author retained ownership of that file; this review did not edit it.

**Verdict:** the Hessian identity, negative-mode rank obstruction, singular-value test, two-droplet angular condition, and composition-screening formulas are correct for the stated finite-dimensional model. The radial test alone cannot certify full stability. A precise general replacement is: an arbitrarily stiff positive reservoir eventually stabilizes the full Hessian if and only if the open-system Hessian is positive definite on perturbations that conserve its total load. Proofs and a counterexample are given below.

All strict inequalities in this review concern **strict quadratic stability**, meaning positive definiteness of the relevant Hessian. A degenerate local minimum can have zero Hessian modes stabilized by higher-order terms; such a minimum is not excluded by a failure of a strict Hessian test at equality.

## 1. Equations (1)–(4)

Let `Y=Ytot−ΣQ_i(x_i)` and `F=Σf_i(x_i)+B(Y)`. At the stationary point write `μ=∇B(Y)` and `K=∇²B(Y)`. Differentiation gives

\[
D^2F[\delta x,\delta x]
=\sum_i\left\{D^2f_i[\delta x_i,\delta x_i]
-\mu\cdot D^2Q_i[\delta x_i,\delta x_i]\right\}
+\left(\sum_i DQ_i\delta x_i\right)^TK
\left(\sum_i DQ_i\delta x_i\right).
\]

This proves (1), including the sign of the nonlinear-load correction. The local block is the Hessian of the grand potential with the reservoir conjugates held fixed. Replacing it with the raw local free-energy Hessian is generally wrong when the load map is nonlinear.

Let `G=diag(G_i)`, and suppose it has a negative subspace of dimension `n_-(G)`. Its intersection with `ker J` has dimension at least `n_-(G)−rank J`. The reservoir quadratic form vanishes there, proving the stronger statement

\[
n_-(H)\ge n_-(G)-\operatorname{rank}J\ge m-r.
\]

No sign condition on `K` is required for this lower bound. If `K` is positive semidefinite, the added quadratic form cannot increase the number of negative modes.

For the chosen one-negative-direction-per-droplet subspace, congruence by `D^(−1/2)` gives

\[
D^{-1/2}H_{\rm rad}D^{-1/2}
=-I+T^TT,\qquad T=K^{1/2}\mathcal B D^{-1/2}.
\]

Thus `Hrad≻0` iff every singular direction has singular value greater than one. Equation (3) requires `K⪰0`; equation (2), by contrast, does not. A rectangular matrix with fewer independent load directions than radial directions necessarily fails this condition.

For `f_i(v)=a_i v^(2/3)−g_i v`, its second derivative is `−2a_i v^(−4/3)/9`. The symmetric two-droplet Gram matrix has diagonal entries `s²` and off-diagonal entries `s²c`, so the smaller full radial eigenvalue is

\[
-d+\frac{s^2}{V_b}(1-|c|).
\]

This proves (4). Near parallel loads, `1−|cos θ|=θ²/2+O(θ⁴)`, yielding the stated volume threshold `vmin∝θ^(−3/2)` and radius threshold `Rmin∝θ^(−1/2)` when all other coefficients are held fixed. These are model scalings, not universal critical exponents.

## 2. Independent derivation of the full composition Schur complement

Use the author's screening notation. The open-system quadratic form is

\[
\frac12x^TGx+x^TPy+\frac12y^TCy,\qquad C\succ0,
\]

and the linearized exchanged load is `Bx+Ay`. The exact combined Hessian is

\[
H=\begin{pmatrix}
G+B^TKB&P+B^TKA\\
P^T+A^TKB&C+A^TKA
\end{pmatrix}.
\tag{R1}
\]

For `K⪰0`, the lower-right block is positive definite. Therefore full strict quadratic stability is equivalent to positivity of its Schur complement:

\[
G+B^TKB-(P+B^TKA)(C+A^TKA)^{-1}(P^T+A^TKB)\succ0.
\tag{R2}
\]

To expose the physical content, change internal variables to `y′=y+C^(−1)Pᵀx`. Then

\[
G_{\rm rel}=G-PC^{-1}P^T,\quad
\widetilde B=B-AC^{-1}P^T,\quad S=AC^{-1}A^T,
\]

and the energy becomes

\[
\frac12x^TG_{\rm rel}x+\frac12y'^TCy'
+\frac12(\widetilde Bx+Ay')^TK(\widetilde Bx+Ay').
\]

Minimizing over `y′` gives

\[
H_{\rm size}=G_{\rm rel}+\widetilde B^TK_{\rm eff}\widetilde B,
\]

\[
K_{\rm eff}=K-KA(C+A^TKA)^{-1}A^TK.
\tag{R3}
\]

For `K≻0`, the matrix inversion identity gives

\[
K_{\rm eff}=(K^{-1}+S)^{-1},
\]

which is exactly equation (5). Formula (R3) remains valid for a singular positive-semidefinite `K` and avoids inventing inverses on inaccessible reservoir directions. An alternative is

\[
K_{\rm eff}=K^{1/2}
[I+K^{1/2}SK^{1/2}]^{-1}K^{1/2}.
\]

Because the eliminated internal block is positive, `n_-(H)=n_-(Hsize)` and the numbers of zero modes also agree. Thus the full stability criterion after internal relaxation is exact, not merely necessary on a chosen radial subspace.

The inequality `Keff⪯K` describes screening after the local size–composition coupling has been absorbed into `Grel` and `Btilde`. For a direct comparison with physically frozen coordinates, (R2) also gives the simpler exact inequality

\[
H_{\rm size}\preceq G+B^TKB.
\]

Thus allowing internal relaxation never raises the effective curvature at fixed original size amplitudes.

## 3. Counterexample to radial sufficiency

Consider one radial mode `x`, one stable internal mode `y`, open Hessian

\[
G_0=\begin{pmatrix}-1&0\\0&1\end{pmatrix},
\]

and conserved load `x+2y`. Let the reservoir stiffness be `k>0`. The full Hessian is

\[
H_k=\begin{pmatrix}k-1&2k\\2k&1+4k\end{pmatrix}.
\]

The radial curvature with composition frozen is `k−1`, positive for `k>1`. The internal diagonal block is also positive. Nevertheless,

\[
\det H_k=-1-3k<0
\]

for every positive stiffness: the full state always has one negative mode. Its relaxed radial curvature is

\[
-1+\frac{k}{1+4k}< -\frac34.
\]

A load-preserving perturbation `y=−x/2` has negative open curvature `−3x²/4`. The reservoir cannot detect or penalize it. This is a direct counterexample to treating the radial singular-value criterion as sufficient after internal composition is admitted.

For comparison, replacing the load by `x+y/2` makes the constrained perturbation `y=−2x` have positive open curvature `3x²`. The relaxed Hessian is now

\[
-1+\frac{k}{1+k/4},
\]

and the full state is stable exactly when `k>4/3`. The internal response raises the threshold but no longer blocks eventual stabilization.

## 4. Exact strong-reservoir criterion

Let `G0` be any real symmetric finite-dimensional open Hessian, `J` any linearized load map, and `K0≻0`. Fix the stationary point and local matrices, and consider

\[
H_\tau=G_0+\tau J^TK_0J,\qquad\tau>0.
\]

Then

\[
\boxed{\exists\tau_0<\infty:\ H_\tau\succ0\text{ for all }\tau>\tau_0
\iff G_0|_{\ker J}\succ0.}
\tag{R4}
\]

If `ker J` is trivial, positivity on it is interpreted vacuously. If `J=0`, the statement reduces to positivity of `G0` itself.

Necessity is immediate: the reservoir quadratic form vanishes on `ker J` for every finite stiffness.

For sufficiency, choose orthonormal coordinates splitting the space into `ker J` and its orthogonal complement. Then

\[
G_0=\begin{pmatrix}G_{00}&G_{01}\\G_{10}&G_{11}\end{pmatrix},
\qquad
J^TK_0J=\begin{pmatrix}0&0\\0&W\end{pmatrix},\quad W\succ0.
\]

By hypothesis `G00≻0`. A Schur complement gives

\[
H_\tau\succ0
\iff G_{11}-G_{10}G_{00}^{-1}G_{01}+\tau W\succ0.
\]

The right side holds at all sufficiently large `τ`. More precisely the threshold is the strict generalized-eigenvalue condition

\[
\tau>
\lambda_{\max}\left[
W^{-1/2}(G_{10}G_{00}^{-1}G_{01}-G_{11})W^{-1/2}
\right],
\]

together with `τ>0`. When the kernel is trivial, omit the empty `G00` block and its correction. If `K0` is merely positive semidefinite, replace `ker J` by `ker(K0^(1/2)J)` throughout.

This criterion concerns varying stiffness at a fixed stationary state and fixed local constitutive matrices. A physical experiment changing bath size may move the stationary state, alter `G0,J,K0`, or destroy that state; the theorem does not bypass those existence checks.

### Relation to composition-screening saturation

If `S=AC^(−1)Aᵀ≻0`, all load directions can be compensated through stable internal modes. In the infinite-stiffness limit, minimizing over those modes under the exact constraint `Btilde x+Ay′=0` gives

\[
H_\infty=G_{\rm rel}+\widetilde B^TS^{-1}\widetilde B.
\]

The remaining internal directions in `ker A` have positive quadratic form `C`. Thus `H∞≻0` is equivalent to positivity of the **full** open Hessian on `ker J`. It is also equivalent to the existence of a sufficiently stiff finite reservoir that stabilizes the state.

If `H∞` has a negative or zero eigenvalue, no finite positive-definite external stiffness yields strict full stability: `Keff≺S^(−1)` and hence `Hsize⪯H∞`. A negative eigenvalue supplies a robust instability; a zero eigenvalue excludes strict positivity but may require higher-order terms to classify the stationary point.

When `S` is singular, full saturation need not occur. Some load directions remain unscreened and their stiffness can diverge. Equation (R4), rather than an inverse of singular `S`, gives the correct general answer.

## 5. Screening example and angular scale

For `Grel=−dI`, `K^(−1)=Vb χb I`, `S=s_d I`, and the two equal-norm load vectors, the minimum eigenvalue is

\[
-d+\frac{b^2(1-|c|)}{V_b\chi_b+s_d}.
\]

Equation (6) follows exactly. Substitution of `s_d=2vχd` and `d=2av^(−4/3)/9` yields the necessary condition for stabilization by some arbitrarily stiff bath,

\[
v^{1/3}>\frac{4a\chi_d}{9b^2(1-|c|)},
\]

confirming (7), including its factor of four and its angle-to-the-power-minus-two linear-size scaling. This is a mathematically consistent isotropic compliance model. It is not yet evidence that a particular multicomponent fluid realizes constant `b,a,χd` while the angle is independently tuned.

## 6. Physical scope and numerical verification

The free energy must use one consistent thermodynamic potential. Conserved-composition redundancies, fixed-volume constraints, and any allowed exchange directions should be eliminated before identifying `r`, `K`, or a positive susceptibility metric. The stated capillary model explicitly freezes background volume and phase compositions before the extension; its coefficients cannot be interpreted as a complete incompressible-mixture calculation without the omitted terms.

The negative-mode count concerns finite droplets, not the Gibbs count of distinct bulk phases. Identical copies contribute separate local negative modes. The claim of exactly `m−1` eigenvalues `−d` for identical droplets is exact on the stated radial subspace; for the full Hessian it additionally requires the chosen radial direction to be an eigenmode, or else should be expressed as an instability/index statement after coupled modes are included.

For positive-definite gradient-dynamics mobility, the stated similarity argument correctly identifies the number of growing modes with `n_-(H)`. Null mobility directions can freeze perturbations without changing thermodynamic curvature.

The independent script `check_droplet_schur.py` compares direct block elimination of (R1) with the screened formula on 200 random matrices. Its maximum operator-norm discrepancy was `1.84×10⁻¹⁴`. It also checks both explicit two-variable examples over five stiffness values. Run:

```bash
python research/verification/check_droplet_schur.py
```

The main correctness result is analytical. The numerical checks catch algebra and implementation mistakes; they do not validate a microscopic mixture or establish novelty. Constrained Hessians, Schur complements, and quadratic-penalty limits are standard mathematical tools, so any publication claim needs a physical result beyond these identities.
