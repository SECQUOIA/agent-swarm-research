# Exact moment relaxations and the arithmetic of Gram certificates

Date: 2026-09-28. Status: integrated proof checked in
[a separate review](strict-hessian-moment-arithmetic-review.md)
and [a fresh noncontributor review](strict-hessian-moment-arithmetic-fresh-review.md).
These are consequences
of strict Hessian certificates and standard semidefinite duality, not a
claim of a new general moment relaxation theorem.

A positive definite Hessian Gram certificate gives particularly strong
exactness of the first applicable moment relaxation: its optimal moment
matrix is unique and has rank one. Nevertheless, its exact Gram
certificates and facial reductions can require irrational coefficients.
The optimizer field is exactly the smallest field that can contain a
maximal-rank Gram certificate. Rational Gram certificates, when they
exist, must have smaller rank at an irrational minimizer.

## Assumptions and notation

Let \(F\in\mathbb Q[x_1,\ldots,x_n]\) be a quartic satisfying

\[
 v^{\mathsf T}\nabla^2F(x)v
   =(v,x\otimes v)^{\mathsf T}H(v,x\otimes v),
 \qquad H\in\mathbb S_{++}^{n+n^2}(\mathbb Q).
 \tag{1}
\]

This is stronger than global strong convexity or ordinary SOS-convexity.
It implies a uniform positive Hessian lower bound, so \(F\) has a unique
global minimizer \(a\). Put \(m=F(a)\) and \(K=\mathbb Q(a)\).
The point \(a\) is algebraic: it is the unique real solution of the
rational gradient equations, and real quantifier elimination over
\(\mathbb Q\) makes each singleton coordinate algebraic. Equivalently,
the nonsingular Hessian makes it an isolated nonsingular complex
solution of those equations.

Let \(b(x)\) list all monomials of degree at most two, starting with 1,
and put \(N=\binom{n+2}{2}\) and \(e=b(a)\). For a sequence
\(y=(y_\alpha)_{|\alpha|\le4}\), write

\[
 L_y(P)=\sum_\alpha P_\alpha y_\alpha,\qquad
 M_2(y)_{\alpha,\beta}=y_{\alpha+\beta}\quad
 (|\alpha|,|\beta|\le2).
\]

The real moment and SOS programs are

\[
 \begin{array}{ll}
 \text{minimize}&L_y(F)\\
 \text{subject to}&y_0=1,\quad M_2(y)\succeq0,
 \end{array}
 \qquad
 \begin{array}{ll}
 \text{maximize}&\gamma\\
 \text{subject to}&F-\gamma=b^{\mathsf T}Qb,\quad Q\succeq0.
 \end{array}
 \tag{2}
\]

All their input data are rational; the optimizer field need not be.

## A Gram matrix of the largest possible rank

Taylor integration at \(a\) yields a Gram matrix \(Q_*\) of \(F-m\)
with

\[
 Q_*\succeq0,\qquad \ker Q_*=\mathbb R e,\qquad
 \operatorname{rank}Q_*=N-1,\qquad Q_*\in\mathbb S^N(K).
 \tag{3}
\]

Here is why the rank and field assertions both hold. Put \(u=x-a\)
and translate (1), obtaining a positive definite Gram matrix on
\((v,u\otimes v)\) with entries in \(K\). Choose a real \(\mu>0\)
below its least eigenvalue. The identity

\[
 F(a+u)-m=\int_0^1(1-t)
              u^{\mathsf T}\nabla^2F(a+tu)u\,dt
 \tag{4}
\]

gives a real SOS Gram for

\[
 F(a+u)-m-\frac{\mu}{2}\|u\|^2-\frac{\mu}{12}\|u\|^4.
\]

The two subtracted terms have a diagonal positive definite Gram matrix
on every nonconstant monomial of degree at most two. Thus the directly
integrated Gram matrix is positive definite on that basis. Its entries
belong to \(K\), since the integrand has coefficients in \(K\) and
integration of powers of \(t\) multiplies by rational numbers. This
last assertion does not use \(\mu\) in the construction.

These centered nonconstant monomials form a basis of the hyperplane
of quadratics vanishing at \(a\). Translating them back gives (3).
Every positive semidefinite Gram matrix for \(F-m\) annihilates \(e\),
because its quadratic form evaluates to zero at \(a\). Hence rank
\(N-1\) is maximal.

This argument is the strict version of the Taylor SOS argument already
recorded in [the descent audit](rational-sos-convex-descent-prior.md).
It does not assert that all positive semidefinite matrices over a real
number field have square factors over that field.

## The moment optimum is unique

Both programs in (2) attain value \(m\). The point sequence
\(y^a_\alpha=a^\alpha\) is feasible with value \(m\), and (3) is a
dual feasible certificate of the same value.

If \(y\) is any optimal moment sequence, then

\[
 0=L_y(F-m)=\operatorname{tr}(Q_*M_2(y)).
\]

For two positive semidefinite matrices, a zero trace product implies
that the range of either lies in the kernel of the other. Applying
this to (3) gives

\[
 \operatorname{range}M_2(y)\subseteq\mathbb R e.
\]

As \(y_0=1\) and the first coordinate of \(e\) is 1, this forces
\(M_2(y)=ee^{\mathsf T}\). Every monomial of degree at most four
is a product of two monomials of degree at most two. Consequently
\(y_\alpha=a^\alpha\) for every index, and the optimum is unique.

The pair \((M_2(y^a),Q_*)\) is strictly complementary: its ranks
sum to \(N\). Both programs also have strictly feasible points.
For the moment program, use the moments of a Gaussian measure with
positive density everywhere. A nonzero quadratic has positive square
integral, so its moment matrix is positive definite. For the dual,
adding any positive constant to \(F-m\) fills the constant coordinate
in the centered Gram and gives a positive definite full Gram.

Thus an arithmetic obstruction to rational optimal certificates need
not come from a gap in relaxation value, lack of real attainment,
absence of real strict complementarity, or lack of Slater points.
Strict feasibility here concerns the optimization programs; the
optimal-level Gram feasibility problem is necessarily singular.

## The least field for maximal-rank Gram certificates

Suppose a field \(L\subseteq\mathbb R\) contains the entries of a
positive semidefinite Gram matrix \(Q\) for \(F-m\), and
\(\operatorname{rank}Q=N-1\). Its kernel is \(\mathbb R e\).
Gaussian elimination over \(L\), followed by normalization of the
constant coordinate to 1, recovers \(e\) over \(L\). In particular
\(a_i\in L\) for every \(i\), so \(K\subseteq L\).
Conversely (3) gives such a matrix over \(K\).

Therefore \(K\) is exactly the least coefficient field for a
maximal-rank Gram certificate, under inclusion. This conclusion refers
to Gram matrix entries, not automatically to coefficients of an
unweighted square factorization.

For rational matrices there is a more detailed rank bound. Define

\[
 r=\dim_{\mathbb Q}\operatorname{span}_{\mathbb Q}
                   \{a^\alpha:|\alpha|\le2\}.
\]

Choose a basis \(\theta_1,\ldots,\theta_r\) over \(\mathbb Q\) of this span and
write \(e=\sum_{j=1}^r\theta_j c_j\), with \(c_j\in\mathbb Q^N\).
The vectors \(c_j\) are independent: the coordinate values of \(e\)
span the entire space for which the \(\theta_j\) form a basis.
If \(Q\) is rational and \(Qe=0\), independence of the \(\theta_j\)
implies \(Qc_j=0\) for every \(j\). Hence

\[
 \operatorname{rank}Q\le N-r. \tag{5}
\]

At an irrational \(a\), \(r\ge2\), so every rational optimal Gram,
if one exists, fails strict complementarity with the unique optimal
moment matrix. Rational optimal Grams need not exist at all, as the
[explicit counterexample](rational-sos-convex-descent.md) shows.
Existence of smaller-rank rational Grams and existence of a real
maximal-rank Gram are compatible.

## Why a rational facial-reduction step can be impossible

For the interpretation as a rational optimal-level feasibility problem,
assume here that \(m\in\mathbb Q\). The real face and field conclusions
below also hold without that assumption, but then its constant data
already involve the irrational number \(m\).

For clarity, a facial-reduction step here means a nonzero positive
semidefinite matrix \(Z\) such that
\(\operatorname{tr}(ZQ)=0\) for every real feasible Gram matrix at
the optimal level. The smallest face of the positive semidefinite
cone containing those Grams is

\[
 \mathcal F_a=\{Q\succeq0:Qe=0\}. \tag{6}
\]

Indeed, all feasible Grams lie in this face, and (3) is in its relative
interior. Every nonzero positive semidefinite exposing matrix for the
feasible set must therefore have the form
\(Z=c\,ee^{\mathsf T}\), with \(c>0\).

The ratios \(Z_{0i}/Z_{00}\), for the linear-monomial indices \(i\),
recover \(a_i\). Every such exposing matrix thus has coefficient
field containing \(K\); \(ee^{\mathsf T}\) itself has entries in \(K\).
If \(a\) is irrational, no nonzero rational exposing matrix exists.

One real step does suffice: evaluation at \(a\) is a linear
combination of the polynomial coefficient equations and exposes (6).
After this reduction, (3) is strictly feasible in that face. Thus the
usual real singularity degree of this optimal-level feasibility
problem is one, whereas no first rational exposing step can preserve
all of its real feasible points.

This does not prohibit an arithmetic procedure that deliberately
restricts to rational Gram candidates and uses their conjugate
vanishing relations. Such a procedure can remove real feasible
matrices and addresses a different feasibility question.

## Examples, prior results, and practical limits

The [cyclic quartics](cyclic-quartic-exponential-degree.md) have short
rational SOS certificates and satisfy (1), while
\([K:\mathbb Q]=(2^{n+1}-(-1)^{n+1})/3\).
Every maximal-rank Gram certificate and every exposing matrix above
must therefore use a coefficient field of at least that degree.
This does not force a large arithmetic circuit representation, and
does not imply hardness of approximate or exact decision.

The full positive definite Hessian Gram condition is material.
The polynomial \(x^2+y^2+y^4\) is strongly convex and SOS-convex,
with unique minimum zero at the origin. Its order-two moment
relaxation permits all moments to vanish except \(y_{00}=1\) and
an arbitrary \(y_{40}\ge0\). These are feasible optimal moment
sequences, so uniqueness fails. Its missing leading \(x^4\) term
precludes (1).

Exact low-order moment relaxations for SOS-convex optimization are
established results. Lasserre's Theorem 2.6 proves the functional
Jensen inequality, and Theorem 3.3 proves exactness and extraction of
an optimizer from the first moments under its stated assumptions.
The proof above uses a stronger full Gram hypothesis to determine
every moment and identify the coefficient field of the maximal-rank
dual certificate. No novelty claim is made for the complementarity
argument. [Primary text, arXiv:0806.3784v3, Sections 2.3 and 3.2](https://arxiv.org/pdf/0806.3784).

The equivalence between rational SOS and a rational positive
semidefinite Gram is also standard. Chua--Plaumann--Sinn--Vinzant's
Lemma 1.6 gives the equivalence, and Remark 1.7 explains the
additional ordering issue over other number fields. This is why the
field statement above is explicitly about Gram entries.
[Primary text, Section 1](https://arxiv.org/pdf/1608.00234).

Laplagne's Proposition 3.2 uses real zeros as Gram kernel vectors.
Section 3.2 imposes their conjugate relations when seeking rational
Grams, and Proposition 3.4 extracts rational relations by traces.
Thus (5) is a dimension count for an established mechanism.
The exact field statements above additionally use the maximal rank
in (3). [Primary text, Sections 3.1--3.2](https://arxiv.org/pdf/1810.04215).

Kolmogorov--Naldi--Zapata explicitly address certification of algebraic
feasible points near a maximal-rank solution of a degenerate SDP.
Irrational exact SDP solutions and methods for certifying them are
therefore established prior. The present examples specify which field
is forced for the stated certificates; they do not discover the
general need for algebraic SDP certificates.
[Primary paper](https://arxiv.org/pdf/2405.13625).

The solver implication is limited but precise: a method that seeks
maximal-rank exact Grams, or preserves all real feasible Grams through
facial reduction, must accommodate the optimizer field in these
examples. A method seeking any rational certificate has a different
rank target, and in the descent counterexample no rational target
exists. Turning these distinctions into better exact algorithms
requires representation choices, arithmetic reconstruction procedures,
and complexity bounds beyond the statements proved here.

The mathematical proofs use exact finite-dimensional linear algebra
and Taylor's identity. No numerical experiment or Lean verification
is asserted for this note.
