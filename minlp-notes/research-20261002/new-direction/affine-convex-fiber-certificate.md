# Affine optimal fibers and a polynomial-selector certificate

Date: 2026-10-02. Status: a structural lemma and a sufficient certificate
interface. Neither supplies a general exact closure theorem for core-only
noise. No external search or priority claim is made.

Let the core variable be \(v\in B\subseteq\mathbb R^k\), and the residual
variable be \(y\in Y=\prod_{i=1}^r[\ell_i,u_i]\). The boxes are nonempty,
compact, and rational. Substitute fixed coordinates. Let \(F(v,y)\) be a
rational polynomial and assume that \(F(v,\cdot)\) is convex on \(Y\)
for every \(v\in B\). A global certificate must include a verified proof
of this residual convexity. Define

\[
 V(v)=\min_{y\in Y}F(v,y),\qquad
 S(v)=\operatorname*{argmin}_{y\in Y}F(v,y).
\]

## 1. Every optimal fiber is an affine section of its box

**Lemma.** For every fixed real core point \(v\), including an algebraic
point not yet known explicitly,

\[
 S(v)=Y\cap\operatorname{aff} S(v).
 \tag{1}
\]

*Proof.* Compactness makes \(S(v)\) nonempty. Convexity of the residual
objective makes \(S(v)\) convex. A nonempty finite-dimensional convex set
has nonempty relative interior in its affine hull \(A\). The polynomial
\(F(v,\cdot)-V(v)\), restricted to \(A\), therefore vanishes on a
nonempty relatively open set. The polynomial identity principle makes it
zero everywhere on \(A\). Every point of \(A\cap Y\) is consequently
optimal, and the reverse inclusion is immediate. The argument also covers
a singleton affine hull. \(\square\)

Thus an optimal fiber is a polytope, although its affine equations can
have irrational coefficients. The lemma identifies its geometry; it does
not compute those equations, prove that they remain fixed as \(v\)
changes, or make the full Hessian positive semidefinite.

## 2. A checkable polynomial selector identifies the value function

The following sufficient interface avoids the full Hessian. Supply a
rational polynomial map \(s:B\to\mathbb R^r\), and partition the residual
coordinates into \(J_\ell,J_u,J_0\). Supply proofs of these statements
throughout \(B\):

\[
\begin{array}{ll}
 \ell_i\le s_i(v)\le u_i &\text{for every }i,\\
 s_i(v)=\ell_i,\quad \partial_{y_i}F(v,s(v))\ge0
      & i\in J_\ell,\\
 s_i(v)=u_i,\quad \partial_{y_i}F(v,s(v))\le0
      & i\in J_u,\\
 \partial_{y_i}F(v,s(v))=0 & i\in J_0.
\end{array}
\tag{2}
\]

The equalities are polynomial identities and can be checked by exact
coefficient comparison. The inequalities need explicit, verifiable
proofs. For example, after scaling the core box to \([0,1]^k\), an
explicit Bernstein expansion with nonnegative rational coefficients
certifies nonnegativity. This is a sufficient proof format, not a claim
that every nonnegative polynomial admits such a finite certificate.
Charge every expansion, degree, coefficient length, and verification cost
to the supplied certificate. Other already established proof formats may
be used with their own explicit costs.

**Selector certificate.** Under residual convexity and (2),

\[
 F(v,y)\ge P(v):=F(v,s(v))\quad(v\in B,\ y\in Y),
 \qquad V(v)=P(v).
 \tag{3}
\]

*Proof.* The convex tangent inequality gives

\[
 F(v,y)\ge F(v,s(v))+
       \sum_i\partial_{y_i}F(v,s(v))(y_i-s_i(v)).
\]

Each summand is nonnegative by its corresponding condition in (2).
Equality of the minimum with \(P(v)\) follows because \(s(v)\) is
feasible. \(\square\)

These are the box KKT conditions, certified simultaneously for every
core point. Neither \(v^*\), \(V(v^*)\), nor the affine hull of its
optimal fiber is needed to verify (3). A coordinate in \(J_0\) may touch
a box bound; its zero derivative remains sufficient. Polynomial
multipliers with complementarity give the same interface, but add no
generality here: a polynomial identity
\(\lambda_i(v)(s_i(v)-\ell_i)=0\) on a full-dimensional core box implies
that one factor is the zero polynomial.

Given an independently certified global minimizer \(v^*\) of \(P\)
on \(B\), equation (3) certifies \((v^*,s(v^*))\) as a global minimizer
on \(B\times Y\). If \(B\) is only a retained part of the original
core domain, the output must also include an independently verified
containment or excluded-region proof. A local selector does not certify
the discarded core region.

If \(F\) has total degree \(d\) and \(s\) has degree at most
\(\delta\), then \(P\) has degree at most
\(D=d\max(1,\delta)\). Its expanded representation has at most
\(\binom{k+D}{D}\) monomials. Consequently the remaining exact problem
has only \(k\) variables and degree \(D\). The reduction itself requires
no smoothing or growth assumption. Any complexity claim for its exact
solution must charge the chosen core algebraic solver, the selector,
and all sign certificates. In particular, an unrestricted selector degree
cannot silently disappear from the parameter list.

## 3. The structural lemma does not supply this certificate

Consider

\[
 F(v,y,z)=v^2+(y^2-2-v)^2,
 \quad v\in[0,1],\ y\in[1,2],\ z\in[0,1].
 \tag{4}
\]

The residual Hessian is diagonal, with entries

\[
 12y^2-8-4v=12(y^2-1)+4(1-v)\ge0,
 \qquad 0.
\]

Thus residual convexity has a direct certificate. Yet

\[
 V(v)=v^2,\qquad
 S(v)=\{\sqrt{2+v}\}\times[0,1].
 \tag{5}
\]

The core value has quadratic growth with constant one at its unique
minimizer \(v^*=0\). Every optimal fiber is the affine section predicted
by (1), but its affine hull moves nonpolynomially. There is no polynomial
selector, even with arbitrary real coefficients: its first residual
coordinate would satisfy the polynomial identity
\(s_y(v)^2=2+v\), which is impossible by degree. At the rational core
point zero, the affine hull already has no rational point.

This example itself has a short exact certificate: the square in (4)
proves the lower bound, and the unique root of
\(y^2=2+v\) in \([1,2]\), with \(z=0\), proves attainment. It shows
that rational polynomial selectors are sufficient but not necessary.
It does not establish that such an algebraic selector and value identity
can always be found or verified at the desired cost.

Even a supplied fixed rational affine section is only geometric data.
Constancy of the polynomial on that section can be checked by
parameterization and coefficient comparison, but optimality still needs
a lower-bound certificate, such as the convex KKT conditions at one
feasible point. Conversely, once a feasible point is certified optimal,
an exact description of every minimizer is unnecessary for outputting one
optimizer.

For a single fixed core, the polynomial box KKT system describes all
fiber minimizers exactly under convexity. It is a compact implicit
description. It does not, by itself, select one minimizer, give a
polynomial-time point-evaluation guarantee under degeneracy, or certify
which unknown core minimizes \(V\). Those are separate obligations in a
general core-only-noise closure theorem.

## Verification record

An inline exact symbolic check verified the residual-curvature identity,
the tangent/KKT sign convention, the value identity in (4), and a simple
polynomial-selector example. Scoped whitespace and Markdown math-delimiter
checks passed. No external search, knowledge-base access, project-wide
verification, or CI inspection was performed.
