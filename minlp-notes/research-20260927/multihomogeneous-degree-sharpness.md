# Sharp degree bounds within strictly convex rational QCQP

Date: 2026-09-27. Status: proof developed and independently checked in two
stages. The incidence reviewer supplied the critical-value argument below;
a fresh reviewer then checked that argument and the specialization step.
The latter audit is recorded in
[the primitive-value review](generic-degree-primitive-value-review.md).
This note records a sharpness consequence of classical generic degree and
Hilbert irreducibility results. It does not claim a new generic degree formula.

For integers \(n\ge1\) and \(0\le h\le n(n+1)/2\), put

\[
 B(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns.
\]

**Sharpness theorem.** There is a rational convex QCQP in \(n\) variables
whose constraint Hessians span a space of dimension exactly \(h\), with a
positive definite objective Hessian, strict feasibility, and a unique
optimizer \(x^*\), such that

\[
 [\mathbb Q(x^*):\mathbb Q]
 = [\mathbb Q(q_0(x^*)):\mathbb Q]
 = B(n,h).
\]

For \(h>0\), every constraint Hessian may also be chosen positive definite.
The feasible set may be compact. Thus, if the proposed universal upper bound
\(B(n,h)\) is established, its dependence on both parameters is exact even
under these favorable convexity and regularity assumptions. The lower-bound
proof here does not depend on that proposed upper bound.

The field \(\mathbb Q(x^*)\) means the field generated jointly by all
optimizer coordinates. No assertion is needed that each individual coordinate
has this degree. The construction is an existence argument and gives no useful
bound on the coefficient sizes of an extremal example.

## 1. The universal KKT incidence is integral

Fix \(1\le s\le n\). Let every coefficient of

\[
 q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
 \qquad i=0,\ldots,s,
\]

be an independent parameter, with \(Q_i\) symmetric. Write \(t\) for the
full coefficient tuple and \(K=\mathbb Q(t)\). Consider the affine incidence
defined by the equality-constrained KKT equations

\[
 q_i(x)=0\quad (1\le i\le s),\qquad
 Q_0x+a_0+\sum_{i=1}^s\lambda_i(Q_ix+a_i)=0.                 \tag{1}
\]

This incidence is an affine space over \(\mathbb Q\). Indeed, freely choose
\(x,\lambda\), every Hessian entry, \(a_1,\ldots,a_s\), and \(c_0\).
The remaining coefficients are uniquely determined by

\[
 c_i=-\tfrac12x^TQ_ix-a_i^Tx,
 \qquad
 a_0=-Q_0x-\sum_i\lambda_i(Q_ix+a_i).                       \tag{2}
\]

In particular its coordinate ring is an integral domain. This point matters:
counting generic critical points alone would not show that they belong to one
irreducible arithmetic family.

Nie and Ranestad's generic degree theorem gives exactly

\[
 D=2^s\binom ns                                             \tag{3}
\]

distinct complex solutions of (1) over a nonempty Zariski open set of
coefficients. The active constraint gradients are independent there. Thus the
function field \(L\) of the incidence is a finite separable extension of
\(K\), of degree \(D\). Cramer's rule on a nonzero gradient minor gives

\[
 \lambda\in K(x),\qquad L=K(x).
\]

The generic count and smoothness used here are classical: see Theorem 2.2,
Corollary 2.5, and Section 3.2 of
[Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*](https://arxiv.org/abs/0802.1233).
Their local PDF and text copy were inspected for these statements.

## 2. The critical value generates the whole field

Let \(\beta=q_0(x)\in L\). Because all objective linear coefficients are
independent parameters, the derivation
\(D_j=\partial/\partial a_{0,j}\) is defined on \(K\). It extends uniquely
to the finite algebraic extension \(L\), since the characteristic is zero.

Differentiating the constraint equations gives

\[
 \nabla q_i(x)^T D_jx=0.
\]

Differentiating the objective and using stationarity in (1) therefore gives

\[
 D_j\beta
 =x_j+\nabla q_0(x)^TD_jx
 =x_j-\sum_i\lambda_i\nabla q_i(x)^TD_jx
 =x_j.                                                     \tag{4}
\]

Every derivation of \(K\) preserves an algebraic intermediate field
\(K(\beta)\). To see this directly, let \(P(Y)\in K[Y]\) be the monic
minimal polynomial of \(\beta\). Separability gives \(P'(\beta)\ne0\), and

\[
 D_j\beta=-\frac{(D_jP)(\beta)}{P'(\beta)}\in K(\beta).
\]

Equation (4) now gives every \(x_j\in K(\beta)\). Conversely
\(\beta\in K(x)\), and hence

\[
 K(\beta)=K(x)=L,\qquad [K(\beta):K]=D.                    \tag{5}
\]

This proves that the generic critical value is primitive for the KKT field.
No separate claim about generic distinct critical values is required.

For specialization, express each \(x_j\) and \(\lambda_i\) as a polynomial
of degree less than \(D\) in \(\beta\), with coefficients in \(K\). Clear
the finitely many parameter denominators in these expressions and in
\(P\). The resulting identities hold on the entire integral incidence:
they hold in its function field and are polynomial identities after
denominator clearing. Consequently, at any coefficient specialization that
avoids those denominators, every KKT point satisfies the specialized
polynomial relation and the same coordinate recovery identities.

## 3. A real open set of strictly convex instances

The arithmetic specialization must retain convexity. The following seed
shows that the desired convex instances occupy a nonempty Euclidean open
subset of the full coefficient space:

\[
 \begin{aligned}
 Q_i&=I+e_ie_i^T,& a_i&=e_i,& c_i&=0 &&(1\le i\le s),\\
 Q_0&=I,& a_0&=-\sum_{i=1}^s e_i,& c_0&=0.
 \end{aligned}                                             \tag{6}
\]

At \(x=0\), the multipliers \(\lambda_i=1\) satisfy (1). All Hessians are
positive definite, and \(Q_1,\ldots,Q_s\) are linearly independent. The
active gradients are \(e_1,\ldots,e_s\). The bordered KKT Jacobian is

\[
 \begin{pmatrix}
  I+\sum_iQ_i & J\\
  J^T & 0
 \end{pmatrix},\qquad J=(e_1\ \cdots\ e_s),
\]

and is nonsingular: if \(Mv+Jw=0\) and \(J^Tv=0\), then
\(v^TMv=0\), so \(v=0\), and then \(w=0\).

The implicit-function theorem supplies a real KKT branch for all coefficients
in a sufficiently small neighborhood of (6). Shrinking this neighborhood
preserves positive definite Hessians, Hessian independence, independent active
gradients, and positive multipliers. The KKT point is therefore the unique
global optimizer of the inequality problem \(q_i\le0\): the objective is
strictly convex and the convex KKT conditions are sufficient.

Strict feasibility holds at the seed by taking
\(x=-u\sum_{i=1}^s e_i\), for small \(u>0\), and persists at that fixed
point after a further shrink. Because a positive definite quadratic sublevel
is bounded, the feasible set is compact. Thus these properties hold throughout
a nonempty real open set \(\mathcal O\).

## 4. Rational specialization inside the convex open set

We need a rational \(t\in\mathcal O\) such that the specialized polynomial
\(P_t(Y)\) stays irreducible of degree \(D\) and the finitely many
denominators from Section 2 stay nonzero. Zariski density alone would not
justify meeting an arbitrary real open set.

Here is a direct reduction to integral multivariable Hilbert irreducibility.
Choose a rational point \(a\in\mathcal O\) and an integer \(M\) large enough
that

\[
 t_j=a_j+1/u_j\quad\text{for all }j,\qquad |u_j|>M,
\]

implies \(t\in\mathcal O\). This substitution is birational, so the
substituted minimal polynomial remains irreducible over
\(\mathbb Q(u_1,\ldots,u_r)\). Clear denominators, remove content in
\(\mathbb Q[u_1,\ldots,u_r]\), and scale to primitive integer coefficients.
Gauss's lemma gives an irreducible polynomial representative.
Hilbert irreducibility gives integral tuples \(u\) that
preserve irreducibility and degree while avoiding any prescribed nonzero
polynomial in \(u\). Include its leading coefficient, the transformed
parameter denominators, and the factors \(u_j-k\), for all integers
\(-M\le k\le M\), among the exclusions.
The resulting rational tuple \(t\) has all required properties.

One primary source giving more than the integral specialization statement
needed here is Corollary 2 of
[Castillo and Dietmann, *On Hilbert's Irreducibility Theorem*](https://arxiv.org/pdf/1602.00314).
Its sublinear-density estimate for reducible specializations, together with
the elementary \(O(H^{r-1})\) count for zeros of a fixed nonzero polynomial
on an integer box, permits all the finite exclusions above. The statement on
pages 1–2 was inspected, and a fresh reviewer also checked the degree-drop
exclusions in its proof on pages 10–11. This use of Hilbert irreducibility
is classical.

Let \(x^*\) be the unique optimizer of this rational instance and let
\(\beta^*=q_0(x^*)\). It is a KKT point on the real branch. Therefore
\(P_t(\beta^*)=0\), and irreducibility gives
\([\mathbb Q(\beta^*):\mathbb Q]=D\). The specialized coordinate recovery
identities give \(x^*\in\mathbb Q(\beta^*)^n\), while rationality of the
objective gives \(\beta^*\in\mathbb Q(x^*)\). Hence

\[
 \mathbb Q(x^*)=\mathbb Q(\beta^*),\qquad
 [\mathbb Q(x^*):\mathbb Q]=D.                              \tag{7}
\]

This completes the construction with Hessian span exactly \(s\).

## 5. Prescribe the full Hessian span

Choose an index \(s\le\min(h,n)\) attaining \(B(n,h)\). If \(h>0\),
one may choose \(s\ge1\). Apply the construction above.

If \(s<h\), extend the rational positive definite matrices
\(Q_1,\ldots,Q_s\) to \(h\) linearly independent rational positive definite
matrices. This is always possible: the positive definite cone is open in the
space of symmetric matrices and is not contained in any proper linear
subspace; its rational points are dense. For each added matrix \(R\), add

\[
 \tfrac12x^TRx-C\le0
\]

with a rational \(C\) large enough that the inequality is strictly slack at
\(x^*\). The optimizer and its value are unchanged. Strict feasibility of the
augmented system follows by taking a point sufficiently close to \(x^*\) on
a segment toward an original strictly feasible point. The constraint Hessian
span is now exactly \(h\).

For \(h=0\), unconstrained minimization of \(\|x\|^2\) has degree one,
which equals \(B(n,0)\). If a compact feasible set is desired in this case,
add a rational box; its affine constraint Hessians are zero.

## 6. A small exact example

For \(n=2,h=1\), consider

\[
 \min_{x,y}\ \tfrac12(x^2+y^2)-2x-2y
 \quad\text{subject to}\quad x^2+2y^2\le1.
\]

At the optimum there is a unique positive multiplier \(\lambda\) with

\[
 x=\frac2{1+2\lambda},\qquad
 y=\frac2{1+4\lambda},\qquad
 \frac4{(1+2\lambda)^2}+\frac8{(1+4\lambda)^2}=1.
\]

The last left-hand side decreases strictly from 12 to 0 on
\([0,\infty)\). Clearing denominators gives

\[
 64\lambda^4+96\lambda^3-44\lambda^2-52\lambda-11=0.
\]

Exact elimination gives the following annihilator of the optimal value \(v\):

\[
 64v^4+160v^3+1588v^2-3036v-12599=0.                        \tag{8}
\]

Modulo 3, this is \(p(v)=v^4+v^3+v^2+1\). The exact identities
\(v^{81}-v\equiv0\pmod p\) and
\(\gcd(p,v^9-v)=1\) prove that \(p\) is irreducible over \(\mathbb F_3\).
Thus (8) is irreducible over \(\mathbb Q\), and the value has degree
four, equal to \(B(2,1)\). Rational expressions in \(\lambda\) show the
joint optimizer field has degree at most four; since it contains the value,
its degree is exactly four.

The targeted exact script is
[check_multihomogeneous_degree_sharpness.py](check_multihomogeneous_degree_sharpness.py).
It verifies the elimination and modular irreducibility certificates for this
example. It does not verify the generic incidence or Hilbert specialization
arguments, which were checked mathematically.

## 7. What this establishes and what it does not

The full generic degree can occur with rational data inside a robust region
of strictly convex, strictly feasible instances. In particular, degeneracy,
lack of strict feasibility, and nonconvexity are not needed to attain the
worst algebraic degree. Additional slack constraints can raise the Hessian
span without lowering that degree.

The generic number \(2^s\binom ns\) and the specialization mechanism are
established theory. The role of this note is to supply the precise rational
convex sharpness statement needed to assess the proposed Hessian-span upper
bound. No novelty claim is made for the ingredients, and a broader search for
an identical sharpness statement remains appropriate. This result gives no
running-time lower bound, no useful coefficient-height bound for the existence
construction, and no claim that an exact solver must enumerate all complex
critical points.
