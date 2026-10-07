# Residual regularization: an exact limit needs an effective evaluation rule

Date: 2026-10-02. Status: scoped exploration; independent review passed.
This investigates removing the uniform residual modulus from
[core-only strong recourse](core-only-noise-boundary-recourse.md).
It does not claim a general exact limit algorithm.

Vanishing quadratic regularization gives qualitative convergence to a
canonical residual point. It does not supply a polynomial-bit convergence
modulus. An explicit convex quartic example below defeats that modulus
even at constant requested coordinate accuracy, on every core-noise draw.
A separate finite-noise budget issue also prevents simply applying the
strong-recourse theorem at successively smaller regularizers.

## 1. Qualitative limits and the missing quantitative input

On a compact domain define

\[
 F_\varepsilon(v,z)=F(v,z)+\frac\varepsilon2\|z\|^2,
                 \qquad \varepsilon>0.                     \tag{1}
\]

Convex residual slices become strongly convex. Suppose the original
problem has a unique optimal core and a convex residual optimal fiber.
That fiber has a unique minimum-norm point. Comparison with this point
shows that every global minimizer of (1) has original objective gap
tending to zero and residual norm no greater than the selected norm.
Compactness then implies convergence to that selected original optimizer.

No fixed positive regularizer generally gives an original optimizer.
Moreover, writing the limit of regularized minimizers is not yet an
evaluable exact representation. A coordinate oracle needs a convergence
schedule whose precision has an appropriate bound in the input length
and the requested accuracy bits.

For a fixed convex residual problem `f`, let `S=argmin f` and suppose

\[
 \operatorname{dist}(z,S)\le C(f(z)-f^*)^\theta.               \tag{2}
\]

If the domain has norm bound `R`, a regularized minimizer satisfies
`f(z_epsilon)-f*<=epsilon R^2/2` and `||z_epsilon||<=||s_0||`, where
`s_0` is the minimum-norm point of `S`. Put `p=Proj_S z_epsilon` and
`a=||p-z_epsilon||`. Projection optimality of `s_0` gives

\[
 \|p-s_0\|^2\le\|p\|^2-\|s_0\|^2\le2Ra+a^2,
 \qquad
 \|z_\varepsilon-s_0\|\le a+\sqrt{2Ra+a^2},
 \quad a\le C(\varepsilon R^2/2)^\theta.                    \tag{3}
\]

Thus a usable error bound gives a schedule. This argument needs control
of both `1/theta` and `log C`. A degree-only exponent without a precision
bound on the constant is insufficient.

## 2. A fixed-degree convex obstruction to a polynomial-bit schedule

The independently developed
[point-precision obstruction](regularization-point-precision-obstruction.md)
uses `x in [0,1]^n`, `y in [0,1]`, and

\[
 G_n(x)=8\sum_{i=1}^n x_i^2-x_1/4
                   -\sum_{i=2}^n x_{i-1}^2x_i,\qquad
 f_n(x,y)=G_n(x)+x_n^2(y-1)^2.                              \tag{4}
\]

Its input has `O(n)` monomials, fixed degree four, and bounded rational
coefficients. The Hessian of `G_n` is at least `10I`. With `u=1-y`,
the full Hessian has the division-free identity

\[
 (p,q)^TH_{f_n}(p,q)
 =p^T(H_{G_n}-6u^2e_ne_n^T)p+2(x_nq-2up_n)^2\ge0.          \tag{5}
\]

Thus `f_n` is jointly convex on its box. Its unique optimizer is `(x*,1)`.
Writing the constant `x_0=1/2`, the stationary recurrence implies

\[
 0<x_n^*\le U_n:=14\,28^{-2^n}\le2^{-2^{n-1}}.             \tag{6}
\]

For the exact minimizer of `f_n+lambda(||x||^2+y^2)`, the regularized
stationarity recurrence gives the same upper bound `x_{n,lambda}<=U_n`
for every positive `lambda`. Conditional minimization in `y` gives

\[
 y_\lambda=\frac{x_{n,\lambda}^2}{x_{n,\lambda}^2+\lambda},
 \qquad
 y_\lambda\ge1/2\ \Longrightarrow\ \lambda\le U_n^2
                                    \le2^{-2^n}.           \tag{7}
\]

Consequently even constant point accuracy along the exact regularized
path requires exponentially many binary parameter bits. More accurate
optimization of the regularized problem cannot repair this schedule.
A compressed expression for such a parameter would require a different
arithmetic/oracle interface; it is not the explicit rational bit model
used by the completed recourse theorem.

This also rules out a uniformly polynomial-effective pair of constants
in (2). At `(x*,0)`, distance to the optimizer is one and the original
objective gap is `(x_n*)^2<=U_n^2`. Therefore any global error bound (2)
for this family must satisfy

\[
                    \frac{\log_2 C}{\theta}
                       \ge2\log_2(1/U_n)\ge2^n.             \tag{8}
\]

Both `1/theta` and `max(1,log C)` cannot be polynomially bounded in its
input length. This does not contradict qualitative error bounds or a
degree-only exponent with a very large constant. The example isolates
the precision cost rather than assuming an unfavorable exponent.

Adjoining the independent core term `(v-1/2)^2+gamma v`, with
`|gamma|<=1/2`, gives core curvature two and projected growth one on
every draw. The residual subproblem is unchanged. Thus core smoothing
does not remove this obstruction, even probabilistically.

The original optimization problem remains easy: choosing `y=1` never
increases the objective, after which only the uniformly strongly convex
problem `G_n` remains. This is a lower bound for the specified isotropic
regularization path, not for exact convex optimization, other selectors,
structural extraction, or compact implicit output.

## 3. Approximate core points and a fixed sampling law are separate issues

Minimum-norm fiber selection need not be continuous in the core. For
`v in [-1,1]` and `y in [0,1]`, take `F(v,y)=v^2(2-y)`. Its value is
`V(v)=v^2`. At the optimal core zero, the minimum-norm fiber point is
zero, but at every nonzero core it is one. Residual regularization
`lambda y^2` gives

\[
                      s_\lambda(v)=\min\{1,v^2/(2\lambda)\}.
\]

For `v` tending to zero, the choices `lambda=v^4`, `lambda=v^2`, and
`lambda=|v|` converge respectively to one, one-half, and zero. Approximating
the core and decreasing the regularizer independently is therefore
unsound for canonical point output. This is an evaluation-interface
counterexample, not a positive-probability smoothed lower bound.

There is also a distinct sampling-budget issue. Applying the completed
strong-recourse theorem at each regularizer makes its uniform residual
modulus of order `lambda`. Its localization cutoff `J(lambda)` then
depends on `log(1/lambda)`, while the finite-grid cell estimate requires
`M>=2^J`. One fixed finite `M` cannot satisfy that proof for arbitrarily
small regularizers. A new law for each requested accuracy gives different
sampled instances, not a Cauchy oracle for one draw. This is a limitation
of the composition, not a proof that every fixed-law fine-stage estimate
must fail.

## 4. What remains valid and what a stronger result must supply

Value convergence is straightforward. For residual norm bound `R`,
optimality of (1) gives `F(z_epsilon)-F*<=epsilon R^2/2`. A point can
therefore have an excellent original objective value while remaining
far from the selected optimizer. Certified convex residual value
evaluation was already available without regularization; it must not
be advertised as a new coordinate oracle.

An exact limit representation with polynomial-precision evaluation needs
a different mechanism, such as a uniformly valid structural selector or
limit certificate, rather than the unmodified isotropic path. It also
needs a sampling and exceptional-event budget fixed for the original
draw. Neither qualitative convergence nor an unquantified polynomial
error bound provides these two ingredients.

The counterexample does not settle whether arbitrary convex residual
fibers admit another useful core-only-noise exact representation. That
question remains open in this investigation. The completed strong-
residual theorem and its output guarantees are unchanged.

## Verification status

The [independent actual-file review](regularization-limit-independent-review.md)
passed both this exploration and the linked obstruction. It checked the
Hessian and stationarity proofs, error-bound implication (8), projection
estimate (3), moving-core example, and the fixed-law distinction.

An inline `python` script using `fractions.Fraction` passed 72 exact
precision-threshold cases and 13 moving-core schedule cases. It also
checked this note's local links, math delimiters, and whitespace. These
checks are separate from the obstruction author's symbolic diagnostics
and the reviewer's proof audit. No project-wide checks, CI inspection,
or index edits were made.
