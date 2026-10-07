# Isotropic Tikhonov regularization can need exponentially many coefficient bits

Date: 2026-10-02. Scope: a fixed-degree convex polynomial example for
point extraction by the exact path minimizing `F+lambda||z||^2`.
This is not a lower bound for solving the original convex problem or
for all ways of selecting an exact optimizer. No external search was used.

## 1. A strongly convex chain with a tiny last coordinate

For `n>=1`, let `x in [0,1]^n`, set the constant `x_0=1/2`, and define

\[
 G_n(x)=8\sum_{i=1}^n x_i^2-\frac{x_1}{4}
                 -\sum_{i=2}^n x_{i-1}^2x_i.
 \tag{1}
\]

The Hessian is tridiagonal. Its diagonal entries are
`16-2x_{i+1}` for `i<n` and `16` for `i=n`; its off-diagonal entries
are `-2x_i`. Each diagonal is at least 14 and the off-diagonal absolute
row sum is at most 4. Therefore `H_G>=10I` on the whole box.

The unique minimizer `x*` is interior. At a lower bound, the first
coordinate derivative is `-1/4`, and each subsequent derivative is
`-(x_{i-1})^2`; induction excludes all lower bounds. At an upper bound
each derivative is positive, since it is at least `16-1-2=13`.
Stationarity thus gives

\[
 x_i^*=\frac{(x_{i-1}^*)^2}{16-2x_{i+1}^*}\quad(i<n),
 \qquad x_n^*=\frac{(x_{n-1}^*)^2}{16}.
 \tag{2}
\]

In particular, all coordinates are positive and

\[
 x_i^*\le (x_{i-1}^*)^2/14,
 \qquad
 x_n^*\le U_n:=14\,28^{-2^n}
                \le2^{-2^{n-1}}.
 \tag{3}
\]

The tiny coordinate alone does not obstruct approximate point output:
rounding it to zero can be harmless. The next coordinate makes this
precision issue affect an order-one output instead.

## 2. Transfer the tiny scale to an order-one optimal coordinate

Add `y in [0,1]` and set

\[
 F_n(x,y)=G_n(x)+x_n^2(y-1)^2.
 \tag{4}
\]

This has degree four, constant-size rational coefficients, and `O(n)`
monomials. Standard binary indexing gives input length `O(n log n)`.
It is jointly convex on the box. To verify this explicitly, put
`u=1-y`. For a Hessian direction `(p,q)`, its quadratic form is

\[
 \begin{aligned}
 (p,q)^TH_F(p,q)
 &=p^T(H_G-6u^2e_ne_n^T)p
                  +2(x_nq-2up_n)^2\\
 &\ge4\|p\|^2\ge0.
 \end{aligned}
 \tag{5}
\]

The identity also covers `x_n=0`; no division by this tiny coordinate
is needed for the convexity certificate.

Since `F_n>=G_n>=G_n(x*)` and `x_n*>0`, the unique original minimizer
is `(x*,1)`. In particular it is also the minimum-norm optimizer. The
point `(x*,0)` is at distance one from it, while its objective gap is
only `(x_n*)^2<=U_n^2`.

Consequently, for any fixed positive exponent `d`, a global error bound
`dist((x,y),argmin F_n)^d<=C(F_n(x,y)-min F_n)` requires
`C>=1/(x_n*)^2>=U_n^(-2)`: evaluate it at `(x*,0)`, where the left
side is exactly one. Thus `log C=Omega(2^n)` even though the polynomial
degree is fixed. Changing this distance exponent does not remove the
large constant exposed by that point.

## 3. The exact Tikhonov path requires exponential bit precision

For `lambda>0`, let `(x_lambda,y_lambda)` be the unique minimizer of

\[
 F_n(x,y)+\lambda(\|x\|^2+y^2)
 \quad\hbox{on }[0,1]^{n+1}.
 \tag{6}
\]

The same boundary derivative tests make every `x_lambda,i` interior.
For fixed `x_lambda`, minimizing over `y` gives exactly

\[
 y_\lambda=\frac{x_{n,\lambda}^2}
                        {x_{n,\lambda}^2+\lambda}.
 \tag{7}
\]

The regularized stationarity equations are

\[
 \begin{aligned}
 x_{i,\lambda}
    &=\frac{x_{i-1,\lambda}^2}
               {16+2\lambda-2x_{i+1,\lambda}} &&(i<n),\\
 x_{n,\lambda}
    &=\frac{x_{n-1,\lambda}^2}
               {16+2\lambda+2(1-y_\lambda)^2}.
 \end{aligned}
 \tag{8}
\]

Thus the bound `x_n,lambda<=U_n` in (3) holds uniformly for every
positive `lambda`, not just at the original optimum. Equation (7) implies

\[
 y_\lambda\ge\tfrac12
 \quad\Longrightarrow\quad
 \lambda\le x_{n,\lambda}^2
       \le U_n^2\le2^{-2^n}.
 \tag{9}
\]

Therefore reaching even constant point accuracy along this exact path
requires `log_2(1/lambda)>=2^n`. A positive rational satisfying this
bound needs exponentially many bits in its ordinary numerator/denominator
encoding. A polynomial-bit choice of `lambda` cannot give a uniform
constant-accuracy point guarantee for this family.

The same conclusion applies to a computed point within `1/8` in maximum
norm of the regularized minimizer, if it must approximate the original
minimizer within `1/4`: these requirements force `y_lambda>=5/8`.
An objective-only approximate solve need not track the regularized
minimizer this closely; no lower bound is claimed for every point such
an oracle might happen to return.

For each fixed `n`, the usual Tikhonov convergence still holds as
`lambda` tends to zero. This example rules out a uniform polynomial-bit
modulus for this schedule. More precisely, uniqueness and compactness
give `x_lambda -> x*`, so (7) implies

\[
 \lim_{\lambda\downarrow0}\frac{1-y_\lambda}{\lambda}
                     =\frac1{(x_n^*)^2}\ge U_n^{-2}.
\]

The `y`-coordinate has a linear asymptotic rate, with a constant requiring
exponentially many bits. This does not require a dimension-dependent
asymptotic Hölder exponent. For a uniform estimate
`1-y_lambda<=C lambda^alpha` on `0<lambda<=1`, setting `lambda=U_n^2`
gives `C>=U_n^(-2alpha)/2`. Every fixed positive exponent therefore
requires `log C=Omega(2^n)`. An exponentially small onset threshold is
another way such an estimate could conceal the same precision cost.

## 4. Value approximation and the original point problem remain easy

Optimality of (6) gives the usual value bound

\[
 0\le F_n(x_\lambda,y_\lambda)-F_n(x^*,1)
                   \le(n+1)\lambda.
 \tag{10}
\]

Thus polynomial-bit regularization suffices for a requested objective
error, while the returned point can remain order-one wrong. The problem
also shows why a useful point-convergence estimate cannot simply be
inferred from objective convergence or qualitative uniqueness.

The original point problem has a direct polynomial-time route: choosing
`y=1` never increases `F_n`, and then only the uniformly strongly convex
problem `G_n` remains. Its curvature converts value accuracy to point
accuracy without resolving the tiny coordinate exactly. This is a
counterexample to a vanilla isotropic Tikhonov schedule, not to convex
optimization, alternative regularization, structural extraction, or
compact exact descriptors.

If a core is desired, add an independent term `(v-1/2)^2+gamma v`.
For `|gamma|<1`, its exact core optimum and projected quadratic growth
are elementary and unaffected by the residual construction. Core-only
noise therefore does not remove this residual precision obstruction.

## Verification

The convexity identity, interior stationarity, uniform regularized chain
bound, and precision implication were derived algebraically. A scoped
`git diff --check` passed. An inline `python3 - <<'PY'` command checked
whitespace, paired math delimiters, and equation numbering. Exact SymPy
calculations verified the Hessian convexity identity and all regularized
stationarity formulas for `n=1,...,5`; exact fractions verified (3) and
its squared bound for `n=1,...,8`. All checks passed. No external search,
project-wide checks, or CI inspection was used.

A later scoped control-character scan found and removed one form-feed
in the fraction command in (7). The follow-up scan found no C0 or C1
control characters other than line feeds, and `git diff --check` passed.
No mathematical checks were rerun for that formatting correction.
