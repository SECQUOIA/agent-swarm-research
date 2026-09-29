# Independent review of explicit elimination for the Hessian-span bound

Date: 2026-09-27. Scope: the elimination step proposed in
[explicit-span-separation.md](explicit-span-separation.md). This review develops
a sufficient algebraic lemma, checks the KKT nonsingularity argument, and
identifies why a direct determinant without an auxiliary variable can fail.
The construction below is classical finite-algebra elimination machinery; no
novelty claim is made for that machinery.

## A sufficient elimination lemma

Let

\[
 G_1(e,\lambda),\ldots,G_s(e,\lambda),\quad
 A(e,\lambda),B(e,\lambda)\in\mathbb Z[e,\lambda_1,\ldots,\lambda_s]
\]

have total degree at most \(d\geq1\), and integer coefficients of absolute
value at most \(2^\tau\). Assume \(s\geq1\). There is a nonzero polynomial
\(R(e,w)\in\mathbb Z[e,w]\) such that

\[
 G(e_0,\lambda_0)=0,\quad
 \det D_\lambda G(e_0,\lambda_0)\ne0,\quad
 A(e_0,\lambda_0)\ne0
 \quad\Longrightarrow\quad
 R\!\left(e_0,\frac{B(e_0,\lambda_0)}{A(e_0,\lambda_0)}\right)=0
 \tag{1}
\]

for every real \(e_0,\lambda_0\). It is allowed that
\(R(e_0,w)\) is identically zero for some parameter values.
The construction gives

\[
 \deg_w R\leq(d+1)^s,
 \qquad \deg_e R\leq(d+1)^s d(T+1),
 \qquad T=s d+d,
 \tag{2}
\]

and coefficient bit length at most

\[
 1+(d+1)^s\left[(T+1)\log_2(1+C)+2+
                              \log_2((d+1)^s)\right],
 \qquad C=2^\tau {s+1+d\choose d}.
 \tag{3}
\]

Rounding the displayed bit bound upward is understood. Enlarging the harmless
constant in (3) also accommodates signs and the convention for zero bits.
The useful conclusion is a bound singly exponential in the number \(s\) of
eliminated variables and polynomial in the input coefficient bit length.

**Proof.** Set \(D=d+1\) and introduce a deformation parameter \(\delta\).
Use the equations

\[
 F_i=\delta\lambda_i^D+G_i(e,\lambda)=0.
 \tag{4}
\]

Over \(\mathbb Q(e,\delta)\), their leading monomials for a graded monomial
order are the relatively prime monomials \(\lambda_i^D\). They form a
Gröbner basis. For example, the usual coprime-leading-term criterion follows
here directly by reducing the two terms of each S-polynomial: the two
remaining products of lower-degree parts cancel. The quotient algebra has
the basis

\[
 \mathcal B=\{\lambda^\alpha:0\leq\alpha_i<D\},
 \qquad Q=|\mathcal B|=D^s.
 \tag{5}
\]

Let \(M_A,M_B\) denote multiplication by \(A,B\) in this basis. Reduction
uses only

\[
 \lambda_i^D=-\delta^{-1}G_i(e,\lambda).
 \tag{6}
\]

Every substitution strictly reduces total degree in \(\lambda\). Each
initial product of a basis monomial with \(A\) or \(B\) has degree in
\(\lambda\) at most \(T=s(D-1)+d\), so every reduction branch has length
at most \(T\). Thus \(\delta^T M_A\) and \(\delta^T M_B\) have integer
polynomial entries. Define

\[
 H(e,\delta,w,\zeta)=
 \det\!\left(\delta^T(wM_A-M_B-\zeta I_Q)\right).
 \tag{7}
\]

This polynomial is nonzero: its coefficient of \(\zeta^Q\) is
\((-1)^Q\delta^{TQ}\).

Let \(k\) be its smallest occurring exponent of \(\zeta\), and put

\[
 K(e,\delta,w)=[\zeta^k]H.
 \tag{8}
\]

Let \(j\) be the smallest occurring exponent of \(\delta\) in \(K\),
and define the nonzero polynomial

\[
 R(e,w)=[\delta^j]K.
 \tag{9}
\]

Fix a point satisfying the antecedent of (1). The implicit function theorem
gives a real analytic solution \(\lambda(\delta)\) of (4), defined near
zero, with \(\lambda(0)=\lambda_0\). Also
\(A(e_0,\lambda(\delta))\ne0\) after shrinking the neighborhood. Write

\[
 a(\delta)=A(e_0,\lambda(\delta)),\quad
 b(\delta)=B(e_0,\lambda(\delta)),\quad
 w(\delta)=b(\delta)/a(\delta).
\]

For each fixed sufficiently small \(\delta\ne0\), evaluation at this
solution is a common left eigenvector of \(M_A,M_B\). It is nonzero because
the basis includes the constant monomial. Consequently the polynomial
\(H(e_0,\delta,w,\zeta)\) is divisible by

\[
 a(\delta)w-b(\delta)-\zeta.
\]

That factor is coprime to \(\zeta\), since \(a(\delta)\ne0\). Because
the same specialized \(H\) is divisible by \(\zeta^k\), extracting its
coefficient of \(\zeta^k\) gives

\[
 K(e_0,\delta,w(\delta))=0.
 \tag{10}
\]

This implication remains true when specialization increases the order of
vanishing in \(\zeta\); then the extracted coefficient is zero outright.
Divide (10) by \(\delta^j\) and let \(\delta\to0\). This proves (1).
There is no need to exclude exceptional values of \(e_0\).

For the bounds, the coefficient 1-norm of every input polynomial is at most
\(C\). Each normal-form entry, after multiplication by \(\delta^T\),
has coefficient 1-norm at most \(C(1+C)^T\), degree in \(e\) at most
\(d(T+1)\), and degree in \(\delta\) at most \(T\). The coefficient
1-norm of (7) is therefore at most

\[
 Q!\left(2C(1+C)^T+1\right)^Q.
\]

Equations (2) and (3) follow by the determinant expansion; extracting
coefficients cannot increase these bounds. This proves the lemma.

If \(s=0\), no quotient algebra or deformation is needed: use
\(R(e,w)=A(e)w-B(e)\), which is nonzero whenever an applicable point exists.

## Application to the KKT equations

In the regularized convex quadratic problem, choose a positive multiplier
representation of the stationarity vector with minimum support among active
constraint gradients. The supported gradients are linearly independent:
otherwise a linear dependence lets one subtract a multiple that preserves
nonnegativity and eliminates a positive coefficient. After the affine
restriction in the Hessian-span proof, the native gradients span at most
\(h\) dimensions; a ball constraint adds at most one. Thus the number of
supported gradients is at most \(h+1\). The relevant count is the number of
all supported gradients, including the ball if its multiplier is positive.

For a fixed support, stationarity gives \(u=p/\Delta\), where
\(\Delta=\det M\) and \(M\succ0\) at the chosen KKT point. The selected
active equations are

\[
 G_i=\Delta^2(q_i(u)-e)=0.
\]

At their root, differentiating stationarity gives

\[
 \frac{\partial u}{\partial\lambda_j}=-M^{-1}\nabla q_j(u),
 \qquad
 \frac{\partial G_i}{\partial\lambda_j}
 =-\Delta^2\nabla q_i(u)^TM^{-1}\nabla q_j(u).
 \tag{11}
\]

The last matrix is negative definite because the supported gradients are
independent. This verifies the nonsingularity required by the lemma. Set
\(A=\Delta^2\) and let \(B\) be the numerator of the regularized objective
value. Taking \(d\) to bound the total degrees of \(G_i,A,B\), which are
all \(O(n+1)\), gives the required value relation with degree and height
\(L^{O(h+1)}\).

There are finitely many supports. Along a sequence \(e_\nu\downarrow0\),
retain one support occurring infinitely often. No uniform lower bound on
the determinant in (11) is needed, and its multipliers may be unbounded.
The deformation limit is taken separately at each positive \(e_\nu\).
If the resulting nonzero polynomial is

\[
 R(e,w)=e^rP(w)+e^{r+1}P_1(w)+\cdots,
 \qquad P\ne0,
\]

then \(R(e_\nu,w_\nu)=0\), \(w_\nu\to\theta\), and division by
\(e_\nu^r\) imply \(P(\theta)=0\). Coefficient extraction again preserves
the degree and height bounds.

The completed main note uses the subsequent unbounded-domain theorem, so
its regularization needs no ball constraint. There the sharper support
bound is \(s\le\min(h,n)\). Separating degree in the parameter from degree
in the multipliers gives multiplier degree at most \(2d\), hence its
displayed value-degree bound \((2n+1)^{\min(h,n)}\). I read the completed
main statement, its coefficient 1-norm estimate, and its separate cases
\(s=0\) and \(d=0\); they are consistent with the elimination proof.

## A joint field-degree consequence

Suppose the same sequence of nonsingular roots has finite limits

\[
 \frac{B_j(e_\nu,\lambda_\nu)}{A(e_\nu,\lambda_\nu)}
       \longrightarrow\theta_j,\qquad j=1,\ldots,r.
\]

Assume all \(B_j\) satisfy the same multiplier-degree bound used to form
\(Q=(d+1)^s\), or use the main note's \(Q=(a+1)^s\) when parameter
degree is counted separately. Then

\[
 [\mathbb Q(\theta_1,\ldots,\theta_r):\mathbb Q]\le Q.
 \tag{12}
\]

Indeed, the lemma first makes each \(\theta_j\) algebraic. Every rational
linear combination of the \(B_j\) has the same degree bound, so the limit
of the corresponding ratio has algebraic degree at most \(Q\). The
primitive element theorem in characteristic zero gives a rational linear
combination of \(\theta_1,\ldots,\theta_r\) that generates their joint
number field. Applying the preceding bound to that combination proves
(12). Large coefficients in that combination could worsen height bounds,
but do not affect this degree argument.

The common sequence and finite coordinate limits are essential hypotheses
of this consequence. Separate bounds on coordinates obtained from unrelated
sequences would only bound the joint degree by the product of their degrees.
Nor does the argument establish convergence or boundedness of the primal
minimizers in an unbounded problem; those require an independent argument.

## Failure modes that the construction addresses

- Directly setting \(\zeta=0\) in (7) can produce the zero polynomial if
  any deformed solution has \(A=B=0\). The lowest nonzero coefficient of
  \(\zeta\) removes this obstruction while retaining every branch with
  \(A\ne0\).
- The original equations can have positive-dimensional complex components.
  The deformation has a fixed finite quotient basis for every
  \(\delta\ne0\); only local nonsingularity at the selected original root
  is used to carry that root through the deformation.
- Using minimal support only among the Hessian coefficient vectors does not
  guarantee independence of the actual active gradients. The new step must
  choose minimal support among the gradients themselves. Their dimension
  bound still follows from the preceding affine restriction.
- The proof is an annihilator bound. It does not identify the correct root
  from that polynomial or by itself provide a point recovery algorithm.

## Sources and verification scope

The finite-algebra ingredients are standard. David Cox's author-written
[Solving Equations via Algebras](https://sites.math.rutgers.edu/~zeilberg/akherim/coxFinite.pdf),
Section 1.2.1, explains the standard monomial basis; Theorem 1.2.4 and its
proof give the multiplication-matrix evaluation eigenvector used here.
The proof above includes the required specialization and coefficient bounds
instead of relying on a generic zero-dimensionality assertion.

This review checks the elimination argument and the differential identity
(11). It does not replace independent review of the original active-face
restriction, convergence of the regularized optimum, or the broader
complexity and novelty claims.

A separately delegated exact-algebra check ran
`python research-20260927/check_explicit_span_resultant.py`; all assertions
passed. The [worked examples](explicit-elimination-adversary.md) cover a
permanent base point, a positive-dimensional component together with an
isolated regular root, and a parameter specialization that increases base
multiplicity. The two-variable multiplication determinant also agrees with
an independently computed iterated resultant. A singular-root example shows
that the lemma cannot simply be extended to arbitrary points of the original
variety. These computations challenge specific failure modes; they do not
prove the general lemma or its complexity bounds. No project-wide checks or
CI inspection were performed.
