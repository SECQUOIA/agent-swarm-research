# An exact-optimal hyperoctahedrally coupled box barrier retains the sharp tax

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the exact parameter and tax transfer; priority not claimed

## Result

Let \(r\geq2\), \(K=(-1,1)^r\), and set \(c=r+4\).  The barrier
\[
 F(x)=-\sum_{i=1}^r\log(1-x_i^2)
      -\log\!\left(c-\|x\|_2^2\right)                         \tag{1}
\]
is genuinely coupled and invariant under every signed coordinate
permutation.  Despite the extra ball term, its self-concordant barrier
parameter is exactly the cube optimum:
\[
                              \boxed{\nu(F)=r}.                 \tag{2}
\]
Moreover its positive-objective central paths satisfy
\[
 \boxed{\displaystyle
 \sup_{w_i>0,\ s_0<s_1}
 {L_F(x_w|_{[s_0,s_1]})\over d_F(x_w(s_0),x_w(s_1))}
 \ \geq\ \Gamma_r,}
 \qquad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
            ={1\over4}\log r+O(1).                            \tag{3}
\]

Thus all four properties coexist:

1. genuine dense Hessian coupling;
2. full hyperoctahedral symmetry, including independent sign changes;
3. the exact optimal parameter \(r\);
4. the full sharp \(\Theta(\sqrt{\log r})\) same-endpoint centrality tax.

This refutes any proposed escape based only on coupling, full cube
symmetry, or optimal barrier parameter.  It does not prove the tax for every
optimal barrier.

The [dyadic discrete
companion](2026-09-04-exact-optimal-hyperoctahedral-box-discrete-tax.md)
turns the same \(c=r+4\) example into an actual-accuracy
central-neighborhood round separation.

More generally, this is not an isolated example.  For every
\(\lambda\geq1\) and \(c-r\geq4\lambda\),
\[
 F_{\lambda,c}(x)
 =-\sum_i\log(1-x_i^2)-\lambda\log(c-\|x\|^2)                 \tag{3a}
\]
is standard self-concordant, fully hyperoctahedrally invariant, genuinely
coupled, has exact parameter \(r\), and satisfies the same lower bound (3).
Thus the generic sum-rule certificate \(r+\lambda\) can overcount the
actual parameter by an arbitrarily large additive amount.  Here \(c\) must
vary with \(\lambda\); for example, at fixed \(r\), the choice
\(c=r+4\lambda\) gives an additive overcount \(\lambda\).  For fixed \(r,c\),
the displayed sufficient condition instead restricts
\(\lambda\leq(c-r)/4\).

## 1. Standard self-concordance and genuine coupling

Write
\[
 U(x)=-\sum_i\log(1-x_i^2),\qquad
 G(x)=-\log(c-\|x\|^2),\qquad S=c-\|x\|^2.                    \tag{4}
\]
The function \(G\) is the standard one-parameter reduced barrier of the
ball of radius \(\sqrt c\).  Since \(c>r\), the closed cube lies strictly
inside this ball.  Restricting \(G\) to the cube preserves standard
self-concordance, and adding it to the standard barrier \(U\) preserves
standard self-concordance.  The term \(U\) supplies blow-up on every cube
boundary point.

Both summands depend only on the coordinate squares, so \(F\) has full
signed-permutation symmetry.  With
\[
                         a={2\over S},
\]
the radial term has
\[
 \nabla G(x)=ax,\qquad
 \nabla^2G(x)=aI+a^2xx^T.                                     \tag{5}
\]
The off-diagonal entries are nonzero whenever two coordinates of \(x\)
are nonzero, so the barrier is genuinely coupled.

## 2. Exact parameter \(r\)

Let
\[
 p=\nabla U(x),\qquad D=\nabla^2U(x),\qquad
 E=D+aI.
\]
Equation (5) gives
\[
 \nabla F=p+ax,\qquad \nabla^2F=E+a^2xx^T\succeq E.
\]
Inverse Loewner order therefore yields
\[
 \|\nabla F(x)\|_{F,x,*}^2
 \leq\sum_{i=1}^r{(p_i+ax_i)^2\over D_{ii}+a}.                 \tag{6}
\]
Put \(y=x_i^2\in[0,1)\).  Since
\[
 p_i={2x_i\over1-y},\qquad
 D_{ii}={2(1+y)\over(1-y)^2},
\]
the \(i\)-th summand in (6) is at most one precisely when
\[
\begin{aligned}
 &2(1+y)+a(1-y)^2-y[2+a(1-y)]^2\\
 &\hspace{25mm}
 =(1-y)\,[\,2+a(1-5y)-a^2y(1-y)\,]\geq0.                     \tag{7}
\end{aligned}
\]
For \(0<a\leq1/2\), the bracket in (7) decreases with \(y\), because
\[
 {d\over dy}[2+a(1-5y)-a^2y(1-y)]
   =a(2ay-a-5)<0,
\]
and its value at \(y=1\) is \(2-4a\geq0\).  In the open cube,
\[
 S=c-\|x\|^2>c-r=4,\qquad 0<a<1/2.                            \tag{8}
\]
Thus every summand in (6) is strictly below one and
\[
                         \|\nabla F(x)\|_{F,x,*}^2<r.         \tag{9}
\]
This proves the upper parameter \(r\).

For the reverse inequality, let \(x=(1-\tau){\bf1}\) and send
\(\tau\downarrow0\).  The radial term and all its derivatives stay bounded
because \(S\to4\), whereas the \(r\) interval channels have squared local
gradient norm tending to one each.  Equivalently, the directional ratio
along this ray tends to \(r\).  Hence the supremum in (9) is \(r\), proving
(2).

For (3a), replace \(a\) by \(2\lambda/S\).  Its radial Hessian is
\[
             \nabla^2[-\lambda\log S]
             =aI+{a^2\over\lambda}xx^T\succeq aI.             \tag{9a}
\]
Its gradient is still \(ax\), and its generic off-diagonal Hessian entries
\((a^2/\lambda)x_ix_j\) are nonzero.  Thus scaling does not destroy dense
coupling, while dependence only on \(\|x\|^2\) preserves every signed
permutation symmetry.  Scaling a standard self-concordant function
by \(\lambda\geq1\) preserves standard self-concordance because
\[
 |D^3(\lambda G)[h,h,h]|
 \leq {2\over\sqrt\lambda}
       \bigl(D^2(\lambda G)[h,h]\bigr)^{3/2}
 \leq2\bigl(D^2(\lambda G)[h,h]\bigr)^{3/2}.
\]
The condition \(c-r\geq4\lambda\) again gives \(a<1/2\) in the open cube,
so dropping the positive rank-one term in (9a) and repeating the identical
scalar calculation (6)--(9) proves
\(\nu(F_{\lambda,c})\leq r\).  Along \(x=t{\bf1}\), the exact directional
ratio is
\[
 {r(p_0+at)^2\over
   D_0+a+(a^2/\lambda)rt^2}\longrightarrow r,               \tag{9b}
\]
where \(p_0=2t/(1-t^2)\) and
\(D_0=2(1+t^2)/(1-t^2)^2\).  Thus the bounded radial terms cannot lower the
vertex limit, and equality follows.  The uniform derivative bounds below
also show directly that the tax transfer applies to the full family.

## 3. Transfer of the full tax

Every radial coupling in (3a) is globally second-order bounded on the cube,
uniformly over the allowed \(\lambda,c\).  Indeed, with
\(G_{\lambda,c}=-\lambda\log S\), (9a) and
\(a=2\lambda/S<1/2\) give
\[
 \|\nabla G_{\lambda,c}(x)\|_\infty< {1\over2},\qquad
 0\preceq\nabla^2G_{\lambda,c}(x)
 \preceq\left({1\over2}+{r\over4\lambda}\right)I
 \preceq\left({1\over2}+{r\over4}\right)I.                    \tag{10}
\]
Therefore every \(F_{\lambda,c}=U+G_{\lambda,c}\) satisfies the hypotheses of
[Facet-regular convex coupling cannot remove the box centrality
tax](2026-09-04-facet-regular-coupling-box-centrality-tax.md), in fact on
the whole cube rather than only one facet collar.  Applying that theorem
with
\[
 \alpha_i=\sqrt i-\sqrt{i-1},\qquad
 w_i(T)=e^{T\alpha_i}
\]
gives
\[
\begin{aligned}
 L_F(x_T|_{(-\infty,0]})
   &\geq T\Gamma_r^2-o_r(T),\\
 d_F(x_T(-\infty),x_T(0))
   &\leq T\Gamma_r+O_r(1).
                                                                  \tag{11}
\end{aligned}
\]
Here \(F=F_{\lambda,c}\); the derivative bounds in (10) are uniform over the
allowed family.
All weights are strictly positive, so the exposed optimizer is the unique
cube vertex \({\bf1}\).  Dividing (11) and taking \(T\to\infty\) proves
(3).  Importantly, the denominator is distance in the actual coupled
Hessian metric, not in the product metric.

## Scope and novelty boundary

The result concerns exact central paths and primal Hessian distance to the
same central endpoint.  It is not a distance-to-objective-sublevel,
central-neighborhood round, finite-bit, or quantum-query lower bound.

The interval and larger-ball barriers, restriction and summation rules, and
inverse Loewner order are standard.  The candidate contribution is the
exact-\(r\), fully hyperoctahedral, genuinely coupled construction together
with the surviving sharp tax.  A targeted search found no matching
statement, but priority requires specialist review.

The offset condition \(c-r\geq4\lambda\) is only a clean sufficient
threshold.  No claim of its optimality is made.

## Audit targets

1. Verify that the larger-ball term is standard self-concordant after
   restriction and that barrier summation is valid.
2. Recompute the factorization and monotonicity in (7).
3. Check that dropping the positive rank-one Hessian term gives the correct
   direction in (6).
4. Verify exactness of the parameter at a vertex.
5. Check the hypotheses and scope of the facet-regular tax transfer.

## Independent hostile audit record

**PASS.**  The radial term is the standard reduced ball barrier on the
radius-\(\sqrt c\) ball; restriction and barrier addition preserve standard
self-concordance.  Its Hessian is \(aI+a^2xx^T\), so replacing the full
Hessian by \(D+aI\) increases the inverse quadratic form, exactly as used
in (6).

After clearing the positive denominator \((1-y)^2\), the difference
between the denominator and numerator of each scalar quotient is exactly
the expression in (7).  For \(a\leq1/2\), its bracket is decreasing on
\([0,1]\) and has endpoint value \(2-4a\geq0\).  Since \(c=r+4\) gives
strict \(a<1/2\) in the open cube, every quotient is strictly below one.
This proves the global upper gradient parameter \(r\).  Along the positive
vertex ray, the radial gradient and Hessian remain bounded while the
diagonal interval Hessian diverges coordinatewise; the full squared dual
gradient norm therefore tends to \(r\).  Hence the parameter is exactly
\(r\), not merely bounded above by it.

The scaled family (3a) passes the same check: its radial Hessian is
\(aI+(a^2/\lambda)xx^T\), scaling by \(\lambda\geq1\) preserves
standard self-concordance, and \(c-r\geq4\lambda\) gives \(a<1/2\).
The same scalar quotient therefore remains below one, while the smooth
vertex limit still gives parameter \(r\).

Finally, (10) supplies global gradient and Hessian bounds for the convex
coupling, so the independently audited facet-regular theorem applies
without a localization caveat.  Its comparison curve measures the actual
 \(F\)-metric, all objective weights are positive, and division of (11)
gives the full \(\Gamma_r\) lower bound.  The result is correctly scoped
as a continuous same-endpoint theorem for this explicit barrier, not an
all-barrier, accuracy-set, discrete-round, or query lower bound.

### Full-family hostile audit (2026-09-04)

**PASS with the \(c\)-versus-\(\lambda\) dependence made explicit.**  The
unit-ball function \(-\log(1-\|z\|^2)\) is standard self-concordant with
parameter one, and \(z=x/\sqrt c\) changes it to
\(-\log(c-\|x\|^2)\) only by affine pullback and an additive constant.
Multiplication by \(\lambda\geq1\) preserves the standard third-derivative
inequality with the factor \(1/\sqrt\lambda\) displayed above.  Summing with
\(U\) is therefore legitimate, and \(U\) supplies the cube-boundary blow-up.
The generic sum rule records the valid but nonsharp certificate
\(r+\lambda\).

For \(a=2\lambda/S\), direct differentiation gives
\(\nabla G_{\lambda,c}=ax\) and
\(\nabla^2G_{\lambda,c}=aI+(a^2/\lambda)xx^T\).  Dropping the positive
rank-one term enlarges the inverse quadratic form.  Clearing
\((1-y)^2>0\) from the resulting scalar quotient gives exactly
\[
 (1-y)\,[2+a(1-5y)-a^2y(1-y)].
\]
Its bracket is strictly decreasing on \(0\leq y\leq1\) for
\(0<a\leq1/2\), with endpoint \(2-4a\).  Since the open cube and
\(c-r\geq4\lambda\) give the strict inequality \(a<1/2\), every coordinate
quotient is strictly below one and the squared local gradient norm is below
\(r\).  Formula (9b) independently lower-bounds the full local norm by a
directional quotient tending to \(r\) at a vertex; the radial terms remain
bounded there.  Hence the exact parameter is \(r\), not just at most \(r\).

The family retains full hyperoctahedral symmetry, and
\((a^2/\lambda)x_ix_j\neq0\) for every generic pair of nonzero coordinates,
so the Hessian coupling is genuinely dense.  There is no claim of a
uniform positive lower bound on the coupling strength when \(c\) is allowed
to grow.  Conversely, (10) gives uniform upper bounds
\(M=1/2\) and \(C=1/2+r/4\) on the whole cube for all allowed
\(\lambda,c\).  These are stronger than the bounded-full-collar hypotheses,
so the independently audited transfer theorem yields the same exact
\(\Gamma_r\) lower bound in the actual \(F_{\lambda,c}\)-metric.

The arbitrary additive overcount varies the family: at fixed \(r\), taking
\(c=r+4\lambda\) permits \(\lambda\to\infty\), and the certificate
\(r+\lambda\) exceeds the exact parameter \(r\) by \(\lambda\).  At fixed
\(r,c\), the sufficient condition bounds \(\lambda\), so it would not support
that asymptotic claim.  This example remains inside the special class
\(U+\) a globally derivative-regular convex coupling.  It neither proves nor
suggests that every optimal, coupled, or symmetric cube barrier has the
centrality tax.
