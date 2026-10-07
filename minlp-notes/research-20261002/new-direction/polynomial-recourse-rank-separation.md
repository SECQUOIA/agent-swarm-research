# A nonlinear convex-recourse family requiring full-rank quadratic correction

Date: 2026-10-02. Scope: mathematical significance of the
[polynomial recourse theorem](smoothed-polynomial-box-recourse.md), not
a review of its proof or a hardness claim. No external search was used.

## 1. One core coordinate and dense quartic recourse

For `t in [0,1]`, `z in [0,1]^m`, and rational `lambda,T>0`, let

\[
 P(z)=\sum_{i=1}^m z_i^4+\left(\sum_{i=1}^m z_i\right)^4,
 \qquad
 F(t,z)=\frac\lambda2(t-t_0)^2+TtP(z)-b^Tz.
 \tag{1}
\]

This has degree five and an explicit expansion with `O(m^4)` monomials.
Its relevant Hessian blocks are

\[
 \begin{aligned}
 H_{tt}&=\lambda, & H_{zt}&=T\nabla P(z),\\
 H_{zz}&=Tt\nabla^2P(z), &
 \nabla^2P(z)&=12\operatorname{diag}(z_i^2)
       +12\left(\sum_i z_i\right)^2\mathbf1\mathbf1^T\succeq0.
 \end{aligned}
 \tag{2}
\]

Thus fixing the single core coordinate always leaves a convex polynomial,
including after arbitrary linear perturbations and residual subbox
restrictions. The residual Hessian is dense at positive points. The
core upper curvature is exactly `L=lambda`, while mixed derivatives
grow linearly with the arbitrary scale `T`. The theorem's expected state
factor is independent of `T`; its polynomial input factor still accounts
for the binary encoding of `T` and derivative bounds. This is a numerical
separation, not a claim of running time independent of input length.

The quartic choice also gives recourse values outside the rational-QP
case: for `m=1`, an interior residual minimizer satisfies
`8Tt z^3=b`, so rational conditional data need not have a rational
optimizer or optimum value. More general dense quartics
`sum_l (a_l^T z)^4` with rational vectors spanning the residual space
have the same convexity and rank argument. The particular symmetric
choice in (1) is for a transparent proof, not a residual hardness example.

## 2. Fixed quadratic corrections require residual rank

**Lemma.** If a fixed symmetric positive semidefinite matrix `K` makes

\[
 (t,z)\longmapsto F(t,z)+\tfrac12(t,z)^TK(t,z)
 \tag{3}
\]

convex on the full box, then `K_zz` is positive definite. In particular,
`rank K >= m`.

**Proof.** Convexity implies `H_F+K` is positive semidefinite at every
interior point. Polynomial Hessian continuity and closedness of the
positive semidefinite cone extend this conclusion to `t=0` and all
`z in [0,1]^m`. At that boundary,

\[
 H_F(0,z)=
 \begin{pmatrix}
  \lambda&T\nabla P(z)^T\\
  T\nabla P(z)&0
 \end{pmatrix}.
 \tag{4}
\]

Suppose `u in ker K_zz`, and set `w=(0,u)`. Since `K` is positive
semidefinite, `w^TKw=0` implies `Kw=0`, including `K_tz u=0`.
The positive semidefinite matrix `H_F(0,z)+K` also has zero quadratic
form on `w`, so it annihilates `w`. Its core component gives

\[
                    \nabla P(z)^Tu=0
                         \quad\hbox{for every }z\in[0,1]^m.
 \tag{5}
\]

But \(\nabla P(e_i)=4(e_i+\mathbf1)\) for every residual coordinate
`i`, and these vectors span `R^m`: their column matrix is `4(I+11^T)`, which is
invertible. Hence `u=0`. The positive semidefinite principal block
`K_zz` has trivial kernel, proving the claim. Linear terms and added
linear noise do not affect any step. QED.

Consequently, although the core has dimension one, there is no
representation `F=G-1/2 x^TKx` with `G` convex and fixed `K>=0` of rank
bounded independently of the residual dimension. Pointwise negative
inertia does not give such a fixed subspace: the residual block is
positive semidefinite, so there is at most one negative eigenvalue at
each point, while the direction requiring correction varies with `z`.

## 3. What the example does and does not establish

The positive core quadratic matters. With `lambda=0`, the objective is
affine in `t` for every fixed `z`, so two endpoint recourse solves find
a global optimum. With `lambda>0`, that reduction fails even for this
family. Choose `t_0=1/2`, `b>=0`, and
`0<sum_i b_i<lambda/8`. Both core endpoints have objective bounded
below by `lambda/8-sum_i b_i>0`. For an index with `b_i>0`, the point
`t=1/2, z=epsilon e_i` has objective `T epsilon^4-b_i epsilon<0`
for sufficiently small positive `epsilon`. Every global optimizer
therefore has an interior core coordinate. Strict value separation
persists under sufficiently small linear perturbations.

The whole objective is not jointly convex: at `t=0` and any point with
nonzero `grad P`, the matrix (4) is indefinite. Thus the ordinary
jointly convex, empty-core baseline does not already cover this family.
Convex optimization still supplies each conditional solve; the additional
capability is global optimization over the nonconvex core, with a
smoothed bound controlled by its upper curvature and noise scale.

The rank lemma excludes fixed quadratic corrections only. It does not
exclude every correction depending on a small number of coordinates.
For example, extend `t log t` continuously by zero at `t=0`. The quartic
homogeneity identity gives, at positive residual points,

\[
 \nabla P^T(\nabla^2P)^{-1}\nabla P=\tfrac43P.
\]

Adding `C t log t` with `C >= (4T/3) max_box P` makes the Hessian
positive semidefinite in the interior by the Schur complement, and
continuity extends convexity to the closed box. This is a one-coordinate
convex correction with a singular boundary derivative and a scale
growing with `T`. Therefore the example does not separate the theorem
from all classical difference-of-convex representations or establish
hardness. It does separate its stated numerical bound from a supplied
small-rank fixed quadratic convexification.

The strongest next capability would preserve an exactly handled convex
core component or permit affine core-dependent recourse constraints,
without charging their positive curvature to the grid count. Such value
functions can be nonsmooth even with linear recourse, so the present
upper-semiconcavity counting argument does not supply that extension.
Establishing a replacement for that argument would be a substantive
step beyond enlarging the catalogue of box-stable convex polynomials.

## Verification

The residual convexity, boundary kernel argument, endpoint separation,
and entropy-correction caveat were checked algebraically. A scoped
`git diff --check` passed. An inline `python3 - <<'PY'` command checked
whitespace and paired math delimiters, and verified 15 exact rational
endpoint/interior witness inequalities for dimensions one through five
and scales `T=1,100,10^6`. No external search, project-wide checks, or
CI inspection was used.
