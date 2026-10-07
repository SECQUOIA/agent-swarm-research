# Core-only noise does not give a jointly convex full-coordinate patch

Date: 2026-10-02. Scope: an obstruction to extending the full-Hessian
closure in [polynomial recourse](smoothed-polynomial-box-recourse.md)
to core-only noise. This is not a hardness claim or an obstruction to
other compact exact certificates. No external search was used.

## 1. A degree-four family with robust projected growth

On `[0,1]^3`, take the single core coordinate `v`, residual coordinates
`z=(z_1,z_2)`, and objective

\[
 F_\gamma(v,z)=\left(v-\tfrac12\right)^2
                    +(z_1-vz_2)^2+\gamma v.
 \tag{1}
\]

Only the core is perturbed. For every core point, `(z_1,z_2)=(0,0)`
is feasible and makes the residual square vanish. Therefore

\[
 \begin{aligned}
 V_\gamma(v)&=\min_z F_\gamma(v,z)
                   =\left(v-\tfrac12\right)^2+\gamma v,\\
 a_\gamma&=\tfrac12-\tfrac\gamma2,\qquad
 f_\gamma^*=\tfrac\gamma2-\tfrac{\gamma^2}4,\\
 V_\gamma(v)-f_\gamma^*&=(v-a_\gamma)^2.
 \end{aligned}
 \tag{2}
\]

For every `gamma in (-1,1)`, the unique core optimum is interior and
the projected quadratic-growth constant is exactly one. In particular,
any continuous or finite noise law supported on `[-1/2,1/2]` has this
property on every draw, with `a_gamma in [1/4,3/4]`.

The complete optimal set is the nontrivial residual segment

\[
 S_\gamma=\{(a_\gamma,a_\gamma s,s):0\le s\le1\}.
 \tag{3}
\]

The base polynomial has a fixed core curvature bound:
`partial_vv F_0=2+2z_2^2<=4`. Its residual Hessian is

\[
 H_{zz}=2
 \begin{pmatrix}1&-v\\-v&v^2\end{pmatrix}
       =2(1,-v)^T(1,-v)\succeq0
 \tag{4}
\]

throughout the box. Thus the example satisfies the conditional convexity
and bounded core upper-curvature assumptions with fixed constants.

## 2. The full Hessian is indefinite off the residual zero set

Write `r=z_1-vz_2`, let `H` be the full Hessian, and set
`w=(0,v,1)`. Direct differentiation gives

\[
 w^THw=0,\qquad Hw=(-2r,0,0)^T,
 \qquad H_{vv}=2+2z_2^2.
 \tag{5}
\]

For `r!=0`, a positive semidefinite matrix cannot satisfy (5), because
zero quadratic form would force `Hw=0`. An explicit negative direction
is `d=w+t e_v`, with `t=r/(1+z_2^2)`:

\[
 d^THd=(2+2z_2^2)t^2-4rt
       =-\frac{2r^2}{1+z_2^2}<0.
 \tag{6}
\]

Since `H_{z_1z_1}=2>0`, the Hessian is indefinite at every `r!=0`.
At `r=0` it is positive semidefinite but singular, with the residual
fiber direction in its kernel. Core linear noise changes neither fact.

Every neighborhood of any point of `S_gamma` contains interior box
points with `r!=0`. Hence there is no full-dimensional jointly convex
neighborhood of any optimal point. In fact, no full-dimensional convex
patch anywhere in the box can make the restricted objective convex:
such a patch has an interior point off `r=0`, where (6) contradicts
the necessary Hessian condition for convexity. Restricting to a lower-
dimensional face or to a graph is a different certificate mechanism.

The obstruction does not come solely from using projected growth.
For any feasible point, the point `(a_gamma,a_gamma z_2,z_2)` belongs
to `S_gamma`. If `delta=v-a_gamma`, then

\[
 \begin{aligned}
 \operatorname{dist}((v,z),S_\gamma)^2
 &\le\delta^2+(r+\delta z_2)^2\\
 &\le3\delta^2+2r^2
 \le3\bigl(F_\gamma(v,z)-f_\gamma^*\bigr).
 \end{aligned}
 \tag{7}
\]

Thus full quadratic growth to the optimal set also holds, uniformly
over this interval of core noise.

## 3. A compact exact certificate still exists

Completion of the core square gives the global identity

\[
 F_\gamma(v,z)-f_\gamma^*
       =(v-a_\gamma)^2+(z_1-vz_2)^2\ge0.
 \tag{8}
\]

Together with feasibility of `(a_gamma,0,0)`, this is an explicit compact
exact global certificate and selector. It certifies the whole optimal
fiber by (3) as well. For rational noise all displayed coefficients,
the value, and this selected optimizer are rational.

At every optimum both residual partial derivatives vanish, including
at the endpoint `(a_gamma,0,0)`. Strict-sign tests therefore do not
justify fixing the residual bounds there. One can nevertheless choose
that endpoint by the explicit global certificate. On the face `z_2=0`,
the remaining objective is strongly convex in `(v,z_1)`. This distinction
is why the example refutes full-Hessian closure from the projected-growth
promise, without refuting all possible face-selection strategies.

Core-only perturbations can therefore leave a positive-dimensional
optimal fiber on every draw, even when the unique core optimum has a
fixed quadratic-growth constant. A replacement closure must certify
the value or select an optimal residual face or section without relying
on ambient strict complementarity and a full-coordinate convex patch.
The explicit identity here shows one way that can succeed; it does not
establish a general certificate theorem.

## 4. A strictly convex residual variant with an interior unique optimizer

Set `a=z_1-1/2`, `b=z_2-1/2`, and instead take

\[
 \widetilde F_\gamma(v,z)
   =\left(v-\tfrac12\right)^2+(a-vb)^2+b^4+\gamma v.
 \tag{9}
\]

For fixed `v`, the residual objective is strictly convex: if two points
have different `b` coordinates, strict convexity of `b^4` gives strict
convexity on their segment; if their `b` coordinates agree, the square
is strictly convex in `a`. Its unique minimizer is `a=b=0`. The residual
Hessian is

\[
 2(1,-v)^T(1,-v)+\operatorname{diag}(0,12b^2)\succeq0.
 \tag{10}
\]

The projected value, core optimum, value, and exact projected growth in
(2) are unchanged. For every `|gamma|<1`, the whole problem has the
unique interior optimizer `(a_gamma,1/2,1/2)`.

At any point with `b=0` and `a!=0`, the quartic term has zero Hessian.
For `w=(0,v,1)` the full Hessian still satisfies
`w^THw=0` and `Hw=(-2a,0,0)`. More explicitly, the direction
`w+a e_v` has quadratic form `-2a^2<0`. Such points occur arbitrarily
close to the unique interior optimizer. Therefore even qualitative
strict residual convexity and interior uniqueness do not produce a
jointly convex full-coordinate neighborhood. No proper original-bound face
contains this optimizer, so the earlier endpoint face-selection escape
is absent.

The residual Hessian is singular at its optimizer, so this example does
not satisfy uniform strong residual convexity. Full point quadratic
growth also fails: at `v=a_gamma` and `a=a_gamma b`, the objective gap
is `b^4` while the squared distance to the optimizer is
`(1+a_gamma^2)b^2`. The projected growth remains exactly one. This is
the distinction relevant to the
[small-multiplier curvature lemma](small-residual-multiplier-curvature.md).

The exact global certificate remains explicit:

\[
 \widetilde F_\gamma-f_\gamma^*
       =(v-a_\gamma)^2+(a-vb)^2+b^4\ge0.
 \tag{11}
\]

Thus this variant strengthens the closure obstruction without making a
hardness claim or excluding other compact exact certificates.

## Verification

The residual Hessian, negative-direction formula, projected value, and
sum-of-squares identity were derived directly. A scoped `git diff --check`
passed. An inline `python3 - <<'PY'` command checked whitespace and
paired math delimiters, then used exact SymPy differentiation to verify
the residual Hessian factorization, (5), (6), (8), and the selector value.
A second scoped check verified the strictly convex variant's residual
Hessian, negative direction at `b=0`, and identity (11). All checks
passed. No external search, project-wide checks, or CI inspection was used.
