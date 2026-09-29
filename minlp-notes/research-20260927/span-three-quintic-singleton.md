# Three rational ellipsoids with a quintic singleton intersection

Date: 2026-09-28. Status: exact construction verified by rational matrix
arithmetic and polynomial identities. This supplies a concrete degree-five
feasible singleton at Hessian span three. It does not establish unbounded
degree at fixed span, an FPT decision lower bound, or a lower bound for
approximate-feasibility precision.

Let `alpha` be the positive real root of `t^5 - 2`, and put

\[
p=(\alpha,\alpha^2,\alpha^3,\alpha^4).
\]

Define `q_i(x)=x^T A_i x+b_i^T x+c_i`, with the following integer data:

\[
A_1=\begin{pmatrix}
2614623632&-522768322&104803068&-1017153954\\
-522768322&3799174020&-1671829550&-126985510\\
104803068&-1671829550&2862304974&-382898195\\
-1017153954&-126985510&-382898195&1869362838
\end{pmatrix},
\]

\[
A_2=\begin{pmatrix}
2265538524&-718575346&573734926&-809282652\\
-718575346&4076479140&-2230110528&-87667068\\
573734926&-2230110528&3054800858&-348343533\\
-809282652&-87667068&-348343533&2198392654
\end{pmatrix},\qquad
A_3=\begin{pmatrix}
2&1&0&-1\\
1&4&-1&-2\\
0&-1&2&1\\
-1&-2&1&3
\end{pmatrix}.
\]

The remaining coefficients are

| Row | `b_i^T` | `c_i` |
| --- | --- | --- |
| 1 | `(-5216667908,-1083030852,-2693189032,-4008780156)` | `10755934016` |
| 2 | `(-5758933444,-872164392,-2959634616,-5223948992)` | `12157572720` |
| 3 | `(4,-6,-8,-4)` | `8` |

All three matrices are positive definite, and they are linearly
independent. Define

\[
\begin{aligned}
\lambda_1&=3-\alpha+2\alpha^2+\alpha^3-3\alpha^4,\\
\lambda_2&=-3+\alpha-\alpha^2+3\alpha^4,\\
\lambda_3&=1319581982.
\end{aligned}
\]

Exact reduction modulo `alpha^5 - 2` gives

\[
q_i(p)=0\quad(i=1,2,3),\qquad
\sum_{i=1}^3\lambda_i(2A_i p+b_i)=0.
\]

All multipliers are strictly positive. Indeed,
`1148/1000 < alpha < 1149/1000`, as verified by fifth powers, and
termwise interval bounds give

\[
\lambda_1\ge
\frac{770969750797}{10^{12}}>0,\qquad
\lambda_2\ge
\frac{31850185307}{15625000000}>0.
\]

Consequently `H=sum_i lambda_i A_i` is positive definite. The vanishing
values and gradient give the exact identity

\[
\sum_i\lambda_iq_i(x)=(x-p)^TH(x-p).
\]

A point satisfying all three inequalities `q_i(x)<=0` must make the left
side nonpositive. The right side vanishes only at `p`. Conversely, `p`
satisfies all three rows with equality. Hence their feasible set is
exactly `{p}`, and its Hessian span is three.

Each individual sublevel set is a proper ellipsoid. Its positive-definite
quadratic has a rational center. That center differs from the irrational
point `p` on its zero level, so its minimum is strictly negative. Finally,
`t^5-2` is Eisenstein at two, and all coordinates belong to `Q(alpha)`,
so the unique feasible point has coordinate field of degree exactly five.

The construction was discovered by solving rational linear conditions on
quadratic coefficients for a prescribed algebraic point and multiplier
triple, with numerical positive-definiteness constraints. The final data
were reconstructed in the exact rational nullspace. Numerical solver
output is not used in the proof or final verification.

The targeted command

```text
python3 research-20260927/check_span_three_quintic_singleton.py
```

passed. The [checker](check_span_three_quintic_singleton.py) verifies
positive leading principal minors, Hessian-span rank, the three vanishing
values, the weighted gradient identity, positive interval bounds, and
irreducibility. No project-wide verification or CI inspection was run.

Two structural observations explain what remains to be investigated.

First, a rational convex basic system with singleton feasible set `{p}`
has a coordinate field with exactly one real embedding. Remove the rows
strict at `p`. If the remaining active convex sublevel sets had a second
common point, a sufficiently short segment from `p` toward it would also
satisfy every removed strict row, contradicting the singleton property.
Every real conjugate of `p` is a common zero of the active rational rows,
so it must equal `p`. Thus the coordinate-field degree is odd. This gives
no uniform upper bound for the degree.

Second, arbitrary-degree examples with three ellipsoids can be sought
through rational affine pencils in two parameters whose PSD feasible set
is a singleton of corank one. At such a point, choose a rational
congruence and a principal block that is positive definite; this block
stays positive definite nearby. The kernel vector can be normalized as
`(p,1)`. Its quadratic evaluation on both parameter-direction matrices
must vanish: otherwise one direction gives a positive first-order Schur
complement and a nearby positive-definite feasible matrix. Take a small
rational triangle around the parameter point within the neighborhood of
positive-definite principal blocks. The matrices at its vertices define
three rational quadratics with positive-definite Hessians and common
zero `p`. Positive barycentric coordinates give a positive-definite
aggregate, hence a singleton. This reduction is qualitative; a family
with controlled rational coefficient lengths is still needed for a
complexity lower bound.
