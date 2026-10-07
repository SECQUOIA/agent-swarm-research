# Small residual multipliers on a stable branch preserve positive curvature

Date: 2026-10-02. Scope: a local calculus lemma, not a branch-discovery,
global-certificate, or running-time theorem. The radius of the stable
branch remains an assumption. No external search was used.

## 1. Precise branch and elimination assumptions

Let `v` denote core coordinates and partition residual coordinates into
interior free coordinates `f` and original-bound coordinates `a`.
Suppose the smooth objective satisfies `H_RR >= mu I`, with `mu>0`,
on the relevant neighborhood. Assume a smooth stationary branch

\[
 F_f(v,\phi(v,a),a)=0,\qquad
 P(v,a)=F(v,\phi(v,a),a)
 \tag{1}
\]

exists near `(v_*,abar)`, with `phi` interior to the original free
residual bounds. On the full Euclidean core ball `B(v_*,rho)`, `rho>0`, assume
that fixing `a=abar` gives the conditional optimizer, so that

\[
 V(v)=P(v,\bar a),\qquad
 A=P_{vv}(v_*,\bar a)=V''(v_*)\succeq2gI,
 \qquad g>0.
 \tag{2}
\]

Equivalently, under residual convexity, interior stationarity and valid
original-bound multiplier signs certify this branch identity. The
implicit function theorem supplies a local smooth extension in `a`
because `H_ff` is positive definite, including when `abar` is on the
original residual boundary. The assumed ball and its derivative bounds
are additional data, not consequences of that local theorem.

For an active residual coordinate let `s_i=1` at a lower bound and
`s_i=-1` at an upper bound, and define its inward multiplier

\[
 \lambda_i(v)=s_iP_{a_i}(v,\bar a).
 \tag{3}
\]

Assume `lambda_i>=0` throughout the ball and
`||Hess lambda_i||_2<=R` there. Use inward displacement coordinates
`y_i=s_i(a_i-abar_i)` when releasing a bound. This diagonal sign
change preserves all eigenvalue and norm bounds.

Elimination preserves the lower residual curvature:

\[
 C=P_{aa}=H_{aa}-H_{af}H_{ff}^{-1}H_{fa}\succeq\mu I.
 \tag{4}
\]

Indeed `u^TCu` is the minimum over `w` of the residual quadratic form
on `(w,u)`, which is at least `mu(||w||^2+||u||^2)`.

## 2. Multiplier gradient and simultaneous release

**Scalar estimate.** A nonnegative `C^2` function `lambda` on a
two-sided Euclidean ball of radius `rho`, with Hessian norm at most
`R`, satisfies at its center

\[
 \|\nabla\lambda\|^2
 \le\max\{2R\lambda,4\lambda^2/\rho^2\}
 \le2R\lambda+4\lambda^2/\rho^2.
 \tag{5}
\]

To prove it, write `b=||grad lambda||` and move a distance `t` in the
negative-gradient direction. Nonnegativity and Taylor's upper bound give
`0<=lambda-bt+Rt^2/2`. If `R>0` and `b/R<=rho`, use `t=b/R` to get
`b^2<=2R lambda`. Otherwise use `t=rho`: when `b>Rrho`, this gives
`lambda>=b rho/2`, proving the second case. Open-ball assumptions give
the same result by taking a limit to its boundary. If `R=0`, directly
`b<=lambda/rho`; the zero-gradient case is immediate.

Release any subset `J` of `m>=1` active residual coordinates, retaining
all others at their original bounds. Suppose
`0<=lambda_i(v_*)<=tau` for `i in J`. The Hessian of the reduced
objective on `(v,y_J)` has block form

\[
 M_J=\begin{pmatrix}A&B_J\\B_J^T&C_J\end{pmatrix},
 \quad (B_J)_i=\nabla\lambda_i(v_*),\quad C_J\succeq\mu I.
 \tag{6}
\]

Here `C_J` is the sign-conjugated principal submatrix of (4). Hence

\[
 \begin{aligned}
 \|B_JC_J^{-1}B_J^T\|_2
 &\le\mu^{-1}\|B_J\|_F^2\\
 &\le\frac m\mu\left(2R\tau+\frac{4\tau^2}{\rho^2}\right).
 \end{aligned}
 \tag{7}
\]

In particular, if

\[
 \tau\le\min\left\{
 \frac{g\mu}{4mR},\quad
 \rho\sqrt{\frac{g\mu}{8m}}
 \right\},
 \tag{8}
\]

the two terms in (7) are at most `g/2` each. Interpret the first
threshold as infinity when `R=0`. Thus
`A-B_JC_J^{-1}B_J^T >= gI`, and `M_J` is positive definite.
This is a simultaneous release statement; it does not add losses
calculated after different sequential eliminations.

Restoring the original free residual coordinates `f` preserves positive
definiteness: their Hessian block is positive definite and its Schur
complement is exactly `M_J`. Consequently the original Hessian restricted
to `(v,f,a_J)`, with other active coordinates fixed, is positive definite
at the candidate. By continuity it remains so on some neighborhood.
No quantitative neighborhood radius is asserted here. When `m=0` there
is no release loss; when the free core dimension is zero the cross block
is empty and residual strong convexity already suffices.

## 3. Uniform derivative bounds and a restored Hessian modulus

Suppose verified bounds on the relevant ambient domain give

\[
 \|\nabla^2F\|_2\le M,\qquad
 \|D^3F\|_{\mathrm{op}}\le B_3,
 \qquad H=M/\mu.
 \tag{9}
\]

The third-derivative norm is the Euclidean trilinear operator norm.
These bounds are uniform over the fixed active patterns considered here.
They do not assert that the same pattern is stable at all core points.

On one stable branch put `s_f(v)=phi(v,abar)` and
`W u=(u,Ds_f u,0)`. Differentiating free stationarity once and twice
gives

\[
 \begin{aligned}
 \|Ds_f\|_2&\le H,\\
 D^2s_f[u,w]&=-H_{ff}^{-1}D^3F[\,\cdot_f,Wu,Ww],\\
 \|D^2s_f\|_{\mathrm{op}}
     &\le B_3(1+H)^2/\mu.
 \end{aligned}
 \tag{10}
\]

Here `||W||_2<=sqrt(1+H^2)<=1+H`. The envelope identity
`P_ai=F_ai` on the branch gives, up to the fixed inward sign,

\[
 D^2\lambda_i[u,w]
   =D^3F[e_{a_i},Wu,Ww]+H_{a_if}D^2s_f[u,w].
\]

Consequently
`||Hess lambda_i||_2<=B_3(1+H)^3`. Thus
`K=max{1,B_3(1+H)^3}` is a uniform multiplier Hessian bound over every
fixed pattern for which the assumed branch exists. Empty free-coordinate
blocks obey the same upper bounds without an implicit solve.

Let `r>=1` be the total residual coordinate count, and assume the branch
and nonnegative multipliers persist on a two-sided core ball of radius
`eta>0`. Choose

\[
 0<\theta\le\min\left\{
       K\eta^2/2,\quad \frac{\mu g}{4rK}\right\}.
 \tag{11}
\]

For a multiplier with `0<lambda_i(v_*)<=theta`, Taylor's inequality in
the negative-gradient direction with
`t=sqrt(2lambda_i(v_*)/K)<=eta` gives
`||grad lambda_i(v_*)||^2<=2Klambda_i(v_*)`. If its value is zero,
nonnegativity on the two-sided ball gives zero gradient directly.
Therefore the set `J` of any released active coordinates with
`lambda_i(v_*)<=theta` satisfies

\[
 \|B_J\|_2^2\le\|B_J\|_F^2
        \le2rK\theta\le\mu g/2,
 \qquad
 M_J\succeq
       \operatorname{diag}(gI,\tfrac\mu2 I).
 \tag{12}
\]

For the second inequality, bound the cross term by
`2|u^TB_Jw|<=g||u||^2+||B_Jw||^2/g`, and use the initial bounds
`A>=2gI` and `C_J>=mu I`. This supplies a modulus, beyond the positive
definiteness established in Section 2.

To restore the eliminated coordinates, write the original Hessian in
the order `(f,q)`, where `q=(v,a_J)`, as `[[D,E],[E^T,G]]`.
Then `D>=mu I`, `||D^{-1}E||_2<=H`, and its Schur complement is
`M_J>=delta I`, where `delta=min{g,mu/2}`. Completing the square gives
the energy bound
`mu||u+D^{-1}Eq||^2+delta||q||^2`. Since

\[
 \|u\|^2+\|q\|^2
 \le2\|u+D^{-1}Eq\|^2+(1+2H^2)\|q\|^2,
 \tag{13}
\]

the restored Hessian is at least `nu I`, with the explicit choice

\[
 \nu=\min\left\{\frac\mu2,
       \frac{\min\{g,\mu/2\}}{1+2(M/\mu)^2}\right\}>0.
 \tag{14}
\]

The first term in this minimum is redundant but records the two separate
energy bounds. If no free residual coordinate was eliminated, (12)
already gives the stronger modulus `delta`. Additional coordinates
fixed by sound exact gradient tests, including some tiny-multiplier
coordinates, leave a principal restriction of the restored Hessian and
therefore preserve the modulus `nu`.

The existing bound
`T>=max_i sum_{j,l} sup |partial_ijl F|` permits the conservative choice
`B_3=nT`, where `n` is total scalar dimension. In fact `B_3=T` suffices
with this definition: for a unit vector `w`, the symmetric matrix
`D(H_F)[w]` has absolute row sums at most `T||w||_infinity<=T`, so its
operator norm is at most `T`. Either choice has the required encoding
size. A quantitative neighborhood on which the restored Hessian stays
positive then follows from a supplied Hessian-variation bound; locating
and certifying the stable branch remains a separate task.

## 4. Boundary and scope limits

The two-sided ball is essential. On a feasible half-interval,
`lambda(v)=v` is nonnegative at `v>=0`, but has value zero and derivative
one at the endpoint. A complete optimization example is

\[
 F(v,a)=\tfrac14v^2+va+\tfrac12a^2,
 \qquad (v,a)\in[0,1]^2.
 \tag{15}
\]

Its conditional minimizer is `a=0`, its projected value is `v^2/4`,
and `H_aa=1`, yet the full Hessian
`[[1/2,1],[1,1]]` is indefinite. The active residual multiplier is
`lambda(v)=v`. Thus projected growth and nonnegativity only on the
feasible core domain do not imply (5).

For a core-boundary optimum, the lemma may instead be applied in the
two-sided tangent coordinates of an original core face after its other
coordinates have been soundly fixed. It does not justify discarding
those core coordinates or control cross-curvature in their directions.

A stable active set, a usable positive radius `rho`, and a verified
multiplier Hessian bound remain substantive requirements. Branch changes
can invalidate the smooth value representation, and a small unknown
radius can make (8) unusable. The lemma supplies local positive curvature
without requiring every residual active multiplier to exceed a fixed
threshold. It does not itself locate the branch, certify global
containment, or bound the work needed to find and verify the patch.

## Verification

The one-dimensional estimate, elimination formula, simultaneous-release
bound, and boundary counterexample were checked algebraically. A scoped
`git diff --check` passed. An inline `python3 - <<'PY'` command checked
whitespace and paired math delimiters, then used exact SymPy calculations
to verify the boundary Hessian and multiplier, and both `g/2` budgets in
(8). A second scoped command checked equation numbering and symbolically
verified the implicit second derivative and multiplier chain rule on a
nonlinear interior-response example, the threshold budget in (12), the
sharp scalar case of its Young bound, and the restoring norm identity.
All checks passed. No external search, project-wide checks, or CI
inspection was used.
