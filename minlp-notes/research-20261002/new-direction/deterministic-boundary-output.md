# Deterministic boundary output: effective enclosures and nearby local minima

Date: 2026-10-02. Status: independently reviewed; targeted exact checks
passed. This note separates an immediate approximation consequence
from a stronger obstruction to one proposed exact-output strategy. It does
not resolve finite exact certification under point growth alone.

The setting is an explicit fixed-degree rational polynomial on a bounded
mixed product box, with native integer coordinates, a supplied factor-tree
decomposition of maximum bag size `p`, and verified coordinate upper
curvature `L>0` on the full continuous hull. Assume an unknown unique
optimizer `a` and unknown point growth `g>0`, and write
`kappa=max(1,L/g)`. Input length includes the curvature certificate.
Round native-integer endpoints and remove fixed coordinates first. An
empty domain is reported immediately; a zero-dimensional domain returns
its single point. Thereafter `n>=1` is the number of remaining coordinates
and the maximum width `s` is positive.

## 1. Certified coordinate enclosures require no boundary Hessian premise

The [polynomial pruned-grid theorem](polynomial-pruned-grid-extension.md)
already preserves every original global optimizer in its retained product
hull. Add the individual integer-label filter from the
[convex-patch theorem](implicit-convex-patch-certificate.md): whenever an
integer grid lists all current labels, remove labels whose exact
min-marginal exceeds the feasible incumbent. That rule is sound without
growth and removes the unit-interval halo that ordinary interval filtering
can leave behind.

For every nonnegative integer `q`, these ingredients give a rational box
`C_q`, a feasible rational point `y_q`, and rational objective bounds
`b_q<=f*<=F(y_q)`, together with a finite pruning certificate, such that

\[
 \begin{gathered}
 \operatorname*{argmin}_X F\subseteq C_q\subseteq X,
 \qquad \operatorname{diam}_2 C_q\le2^{-q},\\
 y_q\in C_q,\qquad F(y_q)-b_q\le2^{-q},
 \end{gathered}                                                     \tag{1}
\]

and every integer coordinate of `C_q` is a singleton. Construction and
verification cost `f_d(p,kappa) poly(I+q)`. No lower Hessian bound or
active-gradient margin is needed. This is a corollary of the existing
search, not a new optimization mechanism.

Here is an explicit unknown-conditioning schedule. For `mu=2,3,...`, let
`K_mu=4^mu`, `theta=2^-mu`, restart from the original box, and impose the
usual coordinate-state cap before allocating DP tables. Set `h_j=s 2^-j`,
with `s` the original maximum width. Run through the first stage satisfying

\[
 h_j^2\le\min\left\{
 \frac{2^{-2q}}{100n^2K_\mu},\quad
 \frac{8\,2^{-q}}{7Ln}\right\}.                                  \tag{2}
\]

Stop only when the actual output hull has singleton integer coordinates,
the exact sum of squared widths is at most `2^-2q`, and the corrected-grid
point's certified objective gap is at most `2^-q`. The corrected-grid
point survives both filters. Do not substitute an early objective-gap
test for this enclosure stopping rule.

The first trial with `K_mu>=8kappa` has `K_mu<=32kappa` and respects the
state cap. The reviewed contraction estimate puts every continuous hull
coordinate within `5 sqrt(n*kappa) h_j` of the corrected-grid point;
its Euclidean diameter is therefore at most `10n sqrt(kappa) h_j`.
The first threshold in (2) proves the desired diameter and also implies
the unit-grid threshold `h_j<=1/(10 sqrt(n*kappa))`. The previous stage's
integer halo then has outward radius at most two. With `theta<=1/4`,
all integer grid steps are one, and the label-witness distance bound
`(22/15) kappa n h_j^2<1` fixes every integer. The second threshold
gives the objective-gap bound `7Ln h_j^2/8<=2^-q`.

The number of stages is `O(poly(I)+q+mu)`. The same caps, trial summation,
and polynomial evaluation denominator analysis as in the predecessor
give the stated bit bound. Verification checks only finite grid data,
the full pruning history, label removals, and the final rational widths
and gap. It does not trust `g` or the estimates used to prove termination.

Under the promise, (1) is a certified Cauchy-name algorithm for `a`.
Separate requested enclosures need not be nested; intersecting them keeps
all optimizers and makes them nested if desired. Each finite output is
valid without the promise, but a single such output does not prove that
only one optimizer lies inside it. The theorem supplies termination and
the complexity bound under point growth, not a finite certificate of that
promise or of termination at every future precision.

In particular, packaging the original quantified global-minimizer formula
with this evaluation program is a useful effective representation under a
promise. It does not by itself solve the stronger problem of discovering
a finite, independently verified uniqueness/optimality descriptor with
the same parameterized construction bound.

## 2. A constant-condition benchmark has another strict local minimum

Use the residual chain from the
[precision obstruction](implicit-optimum-precision-obstruction.md). For
`n>=1`, on `[0,1/2]^(n+1)`, define

\[
 r_0=x_0-\tfrac14,\qquad
 r_i=x_i-\tfrac14x_{i-1}^2,\qquad
 F_n(x)=\sum_{i=0}^n r_i^2.
\]

Its unique zero is

\[
 a_0=\tfrac14,\qquad a_i=\tfrac14a_{i-1}^2
       =2^{-(4\,2^i-2)}.
\]

Add `y in [0,1/2]` and set

\[
 h=x_n-\tfrac18x_{n-1}^2=\tfrac12(x_n+r_n),\qquad
 G_n(x,y)=F_n(x)+y^2+3yh.                                       \tag{3}
\]

The [frontier benchmark](nonlinear-frontier-significance.md) records
the identity

\[
 G_n=\tfrac14(F_n+y^2)+\tfrac34(F_n-r_n^2)
             +\tfrac34(r_n+y)^2+\tfrac32yx_n.                   \tag{4}
\]

Every term is nonnegative on the box. The residual contraction bound
`F_n(x)>=(9/16)||x-a||^2` therefore gives

\[
 G_n(x,y)\ge\tfrac9{64}(\|x-a\|^2+y^2).                       \tag{5}
\]

Its unique global optimizer is `(a,0)`, and `L=35/16` is a valid coordinate
upper-curvature bound. The extra diagonal term from `3yh` is nonpositive;
the `y` diagonal is two. Degree is four, maximum bag size is three, and
`L/g=140/9` using (5), uniformly in `n`.

Nevertheless, `G_n` has a second **strict nonglobal local minimum** at
distance less than `sqrt(3)*a_n` from `(a,0)`. It satisfies the original
box KKT conditions, strict complementarity, and a positive definite free
Hessian. Thus merely adding second-order tests to local KKT isolation
does not remove the issue.

## 3. Exact construction of the nearby local minimum

Restrict to the face `x_n=0`, and put `u=(x_0,...,x_{n-1})`. Its objective is

\[
 F_{n-1}(u)+\tfrac1{16}u_{n-1}^4
                 +y^2-\tfrac38yu_{n-1}^2.
\]

For every feasible `u`, the unique minimizing `y` is

\[
 y(u)=\tfrac3{16}u_{n-1}^2\in[0,3/64].
\]

The reduced objective is consequently

\[
 H(u)=F_{n-1}(u)+\tfrac7{256}u_{n-1}^4.                       \tag{6}
\]

The residual-chain Hessian is at least `5I/8`; the added quartic is convex.
Hence (6) has a unique minimizer `u` on its box. Comparing its value with
the prefix of `a` and using the residual growth bound gives

\[
 \tfrac9{16}\|u-a_{0:n-1}\|^2
 \le H(u)\le H(a_{0:n-1})=\tfrac7{16}a_n^2,
 \qquad
 \|u-a_{0:n-1}\|\le\tfrac{\sqrt7}{3}a_n<a_n.                 \tag{7}
\]

Every prefix coordinate lies between `a_{n-1}` and `1/4`, and
`a_n<=a_{n-1}/16`. Bound (7) therefore puts every coordinate of `u`
strictly between zero and `1/2`. In particular, its unconstrained
stationarity equations hold. Set

\[
 b=(u,0,y(u)).                                                \tag{8}
\]

At `b`, all free derivatives of `G_n` vanish, while its one active
derivative is

\[
 \partial_{x_n}G_n(b)
       =-\tfrac12u_{n-1}^2+3y(u)
       =\tfrac1{16}u_{n-1}^2>0.                              \tag{9}
\]

The free Hessian in `(u,y)` is positive definite. Its `y,y` entry is two,
and the Schur complement after eliminating `y` is exactly

\[
 \nabla^2F_{n-1}(u)+\tfrac{21}{64}u_{n-1}^2 ee^T
      =\nabla^2 H(u)\succeq\tfrac58 I.                       \tag{10}
\]

Here `e` is the last prefix coordinate vector. Equations (9)--(10)
give a strict constrained local minimum: the positive first derivative
dominates sufficiently small inward changes of `x_n`, and the positive
free quadratic term handles tangent changes. Equivalently, complete
the square in mixed Taylor terms; their adverse contribution is only
quadratic in the inward displacement, while (9) contributes linearly.
The point is nonglobal because (6) is strictly positive at its minimum:
zero would require both `u=a_prefix` and `u_last=0`, which is impossible.

Finally, from (7), `a_n/a_{n-1}<=1/16`, and (8),

\[
 y(u)\le\tfrac{867}{1024}a_n<a_n,\qquad
 \|b-(a,0)\|^2
 \le\left(\tfrac79+1+(\tfrac{867}{1024})^2\right)a_n^2
 <3a_n^2.                                                     \tag{11}
\]

The input uses only fixed rational coefficients and `O(n)` local factors;
its ordinary indexed encoding is `O(n log(n+1))`. The distance in (11)
is doubly exponentially small in the chain length while degree, bag size,
and the growth/upper-curvature ratio stay fixed.

## 4. What this rules out, and what it does not

There is no universal `2^-poly(I)` neighborhood radius, even at these
fixed parameters, that isolates the global optimizer from other box KKT
points satisfying strict complementarity and second-order sufficiency.
Every relative Euclidean ball around `(a,0)` of radius greater than
`sqrt(3)*a_n` contains the second local minimum. A closure rule requiring
that this entire neighborhood have a unique such stationary point can
therefore need exponentially many accuracy bits on this family.

This is a limitation of quantitative stationarity isolation, not a lower
bound for arbitrary exact descriptors or all rational rectangles. A
directional cut or an exact correlated relation could distinguish the
points without producing a symmetric neighborhood at that scale. The
construction does not show that every global pruning algorithm must
retain `b` for exponentially many stages.

Indeed, this particular family has a short successful correlated
certificate already: (4) proves nonnegativity, and its zero conditions
give `y=0` and the unique recurrence `r_i=0`. The recurrence can be
evaluated with controlled dyadic rounding in polynomial time in `n+q`,
without expanding the tiny exact rational coordinates. Thus the example
identifies a failure of generic local KKT/SOSC closure while remaining
easy for a certificate that uses its algebraic correlations.

No general method has been established here for finding analogous
correlated certificates from an arbitrary sparse polynomial and point
growth alone. The effective enclosures in Section 1 remain the general
positive statement. Turning them into a finite independently verified
exact descriptor without a Hessian, active-gradient, or slack parameter
is still an additional problem.

## 5. Review and checks

The [completed-text independent review](../reviews/deterministic-boundary-output-review.md)
approved the proof and scope. The nearby-minimum calculation was also
independently checked before drafting,
including the Schur coefficient, interiority, distance bound, and uniform
growth constants. A fresh completed-text review also checked the enclosure
schedule against both predecessor proofs; its only requested clarification
was explicit removal of fixed coordinates before formulas dividing by `n`.

The targeted command
`python research-20261002/reviews/check_deterministic_boundary_output.py`
passed four exact symbolic identities, isolated the one-link example's
secondary-minimum cubic through 100 rational bisections, and checked 243
independent enclosure-budget fixtures. The
[checker](../reviews/check_deterministic_boundary_output.py) tests the new
algebra and stopping thresholds; it does not rerun the existing sparse DP.
No project-wide verification, CI inspection, or index edit was performed.
