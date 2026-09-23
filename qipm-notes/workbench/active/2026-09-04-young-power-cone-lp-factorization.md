# Young factorization of the \(\ell_p\)-ball by power cones

Status: Construction and regularity count proved and independently audited; barrier optimum left open  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let \(1<p<\infty\), let \(q=p/(p-1)\), and put

\[
 \alpha={1\over p},\qquad \beta={1\over q}=1-\alpha.
\]

Use the three-dimensional power cone and its dual in the conventions

\[
 \begin{aligned}
 P_\alpha&=\{(u,v,w):u,v\geq0,\ u^\alpha v^\beta\geq |w|\},\\
 P_\alpha^*&=\{(a,b,c):a,b\geq0,\
        (a/\alpha)^\alpha(b/\beta)^\beta\geq |c|\}.
 \end{aligned}                                                   \tag{1}
\]

For \(x\in S_p^{N-1}=\{x:\sum_i|x_i|^p=1\}\) and
\(y\in S_q^{N-1}\), define

\[
 A_i(x)=(|x_i|^p,1,x_i),\qquad
 B_i(y)=(\alpha,\beta|y_i|^q,-y_i).                             \tag{2}
\]

Then \(A_i(x)\in\partial P_\alpha\),
\(B_i(y)\in\partial P_\alpha^*\), and Young's identity gives

\[
 \begin{aligned}
 \langle A_i(x),B_i(y)\rangle
   &=\alpha|x_i|^p+\beta|y_i|^q-x_i y_i\geq0,\\
 \boxed{1-\langle x,y\rangle
   &=\sum_{i=1}^N\langle A_i(x),B_i(y)\rangle.}
                                                                    \tag{3}
 \end{aligned}
\]

Thus the standard coordinatewise power-cone model is also an exact,
globally labelled slack factorization.  It has a sharp global-regularity
count:

> **Theorem (sharp bi-contact-\(C^1\) count).** Let \(N\geq3\). Among
> exact factorizations of the \(B_p^N\) slack through products of arbitrary
> three-dimensional proper cones which admit globally labelled \(C^1\)
> primal selections on \(S_p^{N-1}\) and \(C^1\) dual selections on
> \(S_q^{N-1}\), the minimum number of factors is
> \[
>                              \boxed{k=N}.                       \tag{4}
> \]
> The same exact count consequently holds when all factors are required to
> be three-dimensional power cones.

The qualifier on global selections is essential.  Equation (4) is not an
unconditional power-cone extension-complexity lower bound.

## The affine lift and its dual certificate

Introduce \((r_i,v_i,w_i)\in P_\alpha\), impose

\[
                  v_i=1,\qquad \sum_i r_i=1,\qquad x_i=w_i.       \tag{5}
\]

The cone constraint is exactly \(r_i\geq|x_i|^p\).  Hence (5) projects
onto \(B_p^N\): necessity follows by summing, and sufficiency follows by
choosing \(r_i\geq|x_i|^p\) with sum one.  At \(x=0\), the choice
\(r_i=1/N\) is strictly feasible in every factor.  On the target boundary,
all inequalities saturate and the primal fiber is unique:

\[
                         r_i=|x_i|^p.                            \tag{6}
\]

For a support vector \(y\in S_q^{N-1}\), give the equality
\(\sum_i r_i=1\) multiplier \(\alpha\) and give \(v_i=1\) multiplier
\(\beta|y_i|^q\).  After subtracting the lifted objective
\(\sum_i y_iw_i\), the factorwise dual slacks are exactly \(B_i(y)\) in
(2).  The multiplier objective is

\[
              \alpha+\beta\sum_i|y_i|^q=\alpha+\beta=1,          \tag{7}
\]

so these are normalized dual certificates, not merely boundary vectors.

## Exact regularity ledger

For \(r>1\), the scalar function \(|t|^r\) is \(C^1\).  It is \(C^2\)
at zero exactly when \(r\geq2\), with the polynomial case \(r=2\)
included.  Therefore:

| exponent | primal sphere and \(A\) | dual sphere and \(B\) |
|---|---|---|
| \(1<p<2\) | globally \(C^1\), not \(C^2\) at coordinate zeros | \(q>2\): globally \(C^2\) |
| \(p=2\) | globally \(C^\infty\) | globally \(C^\infty\) |
| \(p>2\) | globally \(C^2\) | \(1<q<2\): globally \(C^1\), not \(C^2\) at coordinate zeros |

In particular, both selections in (2) are globally \(C^1\) for every
open-range exponent, but both are \(C^2\) only in the Euclidean case.

This statement concerns the two selections on their own contact spheres.
The contact correspondence is

\[
 y_i=\operatorname{sgn}(x_i)|x_i|^{p-1}.                         \tag{8}
\]

For \(p<2\), (8) is not \(C^1\) at a coordinate zero, whereas its inverse
is; for \(p>2\), (8) is \(C^1\), whereas its inverse is not.  Composing
both factor selections with one choice of contact coordinate would
therefore obscure the valid bi-\(C^1\) statement.  The sharp-count proof
uses the primal and dual maps independently and does not differentiate
(8).

## Proof of the sharp count

The universal curvature-capacity theorem gives \(k\geq N-1\), since a
three-dimensional proper cone has mixed-curvature capacity at most one.
Suppose equality holds.  At a contact pair \((x,y)\), the tangent spaces are

\[
 T_xS_p^{N-1}=y^\perp,\qquad T_yS_q^{N-1}=x^\perp.               \tag{9}
\]

The Euclidean pairing between these two \((N-1)\)-spaces is nondegenerate:
if \(u\in y^\perp\) is orthogonal to \(x^\perp\), then
\(u\in\operatorname{span}x\), while \(\langle x,y\rangle=1\)
forces \(u=0\).

Mixed differentiation of an arbitrary exact slack factorization therefore
writes this nondegenerate pairing as a sum of \(N-1\) maps

\[
                 M_i=-dA_i^*dB_i,\qquad \operatorname{rank}M_i\leq1. \tag{10}
\]

Every \(M_i\) must have rank one.  In particular, neither contact factor
can vanish: a two-sided differentiable map from a manifold into a pointed
cone has zero derivative wherever its value is the cone vertex.

Choose \(\ell_i\in\operatorname{int}K_i^*\) and normalize the primal
factor to the compact planar base,

\[
 p_i(x)={A_i(x)\over\ell_i(A_i(x))}
       \in\partial\{z\in K_i:\ell_i(z)=1\}.                      \tag{11}
\]

The base boundary is a Jordan circle.  As in the arbitrary-three-cone
phase lemma, \(dp_i\) cannot have rank zero, because then \(dA_i\) is
radial and differentiated complementarity makes \(M_i=0\).  It cannot
have rank two, because a local submersion into the base plane has open
image while (11) lies in its boundary.  Hence \(p_i\) has constant rank
one and is a \(C^1\) submersion onto the boundary circle.

For \(N\geq3\), \(S_p^{N-1}\) is simply connected.  The circle-valued map
\(p_i\) lifts to a real-valued \(C^1\) phase.  That phase attains a maximum
on the compact sphere, where its differential vanishes, contradicting
\(\operatorname{rank}dp_i=1\).  Thus \(k=N-1\) is impossible.  Construction
(2) uses \(N\) factors and proves (4).

For \(N=2\), the simple-connectivity step fails.  One arbitrary
three-dimensional cone is enough: the homogenization cone \(K_{p,3}\)
itself gives the slack factors \((1,x)\) and \((1,-y)\).  Within the power-
cone dictionary, one factor works at \(p=2\), because \(P_{1/2}\) is a
rotated Lorentz cone.  For \(p\ne2\), the displayed construction uses two
power cones.  A one-factor power-cone lift would, by minimum-space rigidity,
make \(K_{p,3}\) linearly isomorphic to a power cone.  The usual projective
boundary regularity test rules this out: a non-Lorentz power cone has one
distinguished non-\(C^2\) boundary ray, while \(K_{p,3}\) has four such
rays for \(p<2\) and none for \(p>2\).  This gives the low-dimensional
power-cone count \(2\), subject to that standard isomorphism lemma.

## Barrier accounting: an open interval, not an exact optimum

For any product of \(k\) three-dimensional proper cones, restriction to a
two-dimensional proper section of every factor gives a barrier with the same
logarithmic-homogeneity parameter on \(\mathbb R_+^{2k}\).  Hence every
possibly coupled ambient LHSC barrier has \(\nu\geq2k\).  Combining this
with (4), every bi-contact-\(C^1\) formulation in the arbitrary
three-dimensional dictionary has

\[
                              \nu\geq2N.                        \tag{11a}
\]

This lower bound is attained by the Euclidean construction at \(p=2\).  No
matching arbitrary-three-cone formulation is asserted for \(p\ne2\).

Let \(c=\min\{\alpha,\beta\}\).  For \(p\ne2\), let
\(\gamma\in(0,1)\) be the unique solution of

\[
 (1-2c)\gamma^{1-c}+(1-c)\gamma^{1-2c}-c=0,
\]

and put

\[
 h(p)=1+{1+\gamma^c\over1+\gamma^{1-c}},\qquad h(2)=2.           \tag{12}
\]

This is Hildebrand's explicit cross-ratio lower bound and lies in \((2,3)\)
away from \(p=2\).  His Corollaries 7.1 and
7.2 give the same scalar function for the power cone and the
three-dimensional \(p\)-order cone.

Here \(\nu_{\rm opt}\) always denotes the infimum over logarithmically
homogeneous self-concordant barriers, the class covered by Hildebrand's
theorem.

The positive-branch product certificate applies to arbitrary coupled
barriers on \(P_\alpha^N\), so

\[
       \boxed{\nu_{\rm opt}(P_\alpha^N)\geq Nh(p).}              \tag{13}
\]

Chares proved a parameter-three barrier for each three-dimensional power
cone.  Equivalently, the canonical-barrier theorem supplies parameter three.
Summing factor barriers gives the computable upper bound

\[
       \boxed{Nh(p)\leq\nu_{\rm opt}(P_\alpha^N)
                       \leq 3N.}                                \tag{14}
\]

At \(p=2\), both endpoints equal \(2N\), so the ambient optimum is exactly
\(2N\).  For \(p\ne2\), neither the one-factor optimum nor the coupled
product optimum is known.  In particular, \(Nh(p)\) must not be described
as the exact ambient parameter.

These are ambient-product parameters.  They are not lower bounds for a
barrier obtained after eliminating or partially minimizing over the affine
lift fibers.

## Literature boundary

The lift (5) is standard.  The
[MOSEK Modeling Cookbook, Section 4.2.2](https://docs.mosek.com/modeling-cookbook/powo.html)
gives exactly
\((r_i,t,x_i)\in P_{1/p}\), \(\sum_i r_i=t\), for the \(p\)-norm cone.
JuMP's conic modeling guide points to the same formulation.  Accordingly,
neither the lift nor its Young-inequality identity is claimed as new.

Robert Chares,
*Cones and Interior-Point Algorithms for Structured Convex Optimization
Involving Powers and Exponentials* (2008), Theorem 3.1.1, proves a
parameter-three barrier.  The smaller formula \(3-2c\), displayed later in
that section, is explicitly based on numerical tests and is a conjecture;
it is not used in (14).  Hildebrand,
[*A Lower Bound on the Barrier Parameter of Barriers for Convex
Cones*](https://doi.org/10.1007/s10107-012-0576-1), gives \(h(p)\) only as
a lower bound and explicitly does not solve the optimal-barrier problem.
Recent work on convex relaxations of the barrier-design problem likewise
states that the exact optimum for three-dimensional power cones remains
unknown.

The potentially new part is the combination of the standard Young lift
with the arbitrary-three-cone phase obstruction to obtain the exact
bi-contact-\(C^1\) count (4), together with the primal/dual regularity
ledger.  It remains a regular-selection theorem, not an unconditional
extension-complexity theorem.

## Audit record

An independent hostile audit checked the dual-cone scaling, nonzero
boundary membership at zero coordinates, Young identity, exact \(C^1/C^2\)
ledger, tangent-space formulas, nondegeneracy of the rectangular mixed
pairing, and the arbitrary-three-cone phase contradiction.  It found the
construction and sharp bi-contact-\(C^1\) count correct.  In particular,
only mixed first derivatives are used, so the axial failure of \(C^2\)
does not affect the theorem.  The audit also caught and removed an earlier
incorrect use of Chares's conjectural parameter \(3-2c\); the rigorous
upper endpoint in (14) is \(3N\).
