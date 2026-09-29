# Three variables suffice for strict SOS-convexity without rational SOS

Date: 2026-09-28. Status: exact construction and certificate passed
independent review; the coefficient-field characterization received a
separate fresh review. Publication priority is not established.

There is an integer quartic in three variables with a positive definite
rational Hessian Gram matrix and minimum zero that has no rational SOS
decomposition. Its Hessian is everywhere at least the identity. The
polynomial has 31 monomials and integer coefficients of absolute value
at most 448.

The example is SOS over a real coefficient field exactly when that field
contains \(2^{1/5}\). The same characterization holds for positive
semidefinite polynomial Gram matrices. Thus \(\mathbb Q(2^{1/5})\)
is the smallest possible real coefficient field for either certificate;
coefficients from towers of quadratic extensions do not suffice. Three
is also the smallest number of affine variables for
failure of rational SOS under the positive definite Hessian Gram
assumption, by the two-variable consequence of Scheiderer's classification
described below.

## The integer polynomial

Define

\[
\begin{aligned}
 r_0&=2-2xy,& r_1&=2x^2-2yz,& r_2&=2y^2-4z,\\
 r_3&=2z^2-x,& r_4&=2xz-y,
\end{aligned}
\]

and put

\[
 A=4r_0+5r_1+3r_2+9r_3,
 \qquad
 \boxed{F=A^2+r_0^2+r_1^2+r_2^2+r_3^2-r_4^2.}       \tag{1}
\]

Let \(a=2^{1/5}\) be the positive fifth root, and set

\[
 p=(a^{-1},a,a^{-3})=(a^4/2,a,a^2/2).
                                                        \tag{2}
\]

Every \(r_i\) vanishes at \(p\). Consequently \(F(p)=0\) and
\(\nabla F(p)=0\). The certificate in the next section proves
\(\nabla^2F\succeq I\) globally, so

\[
                     F(X)\geq\tfrac12\|X-p\|^2.       \tag{3}
\]

In particular, \(p\) is the unique real zero and global minimizer.
The polynomial \(T^5-2\) is irreducible by Eisenstein's criterion,
so its coordinate field \(K=\mathbb Q(a)\) has degree five.

The point and first four quadratics come from the three-variable member
of the [cyclic quartic construction](cyclic-quartic-exponential-degree.md).
The additional quadratic \(r_4\) supplies the obstruction. No root
approximation enters the definition of (1).

## An exact rational Hessian certificate

Use the rational center

\[
 c=(3/4,1,1/2),\qquad u=X-c,
 \qquad Z=(v,u\otimes v),\quad v\in\mathbb R^3.
\]

For a rational quadratic \(q\), write
\(q(c+u)=d+b^{\mathsf T}u+u^{\mathsf T}Tu\), with \(T\)
symmetric. Define the rational \(12\times12\) matrix

\[
 \mathcal M(q)=
 \begin{pmatrix}C&D\\D^{\mathsf T}&Q\end{pmatrix},
\]

where tensor coordinates are ordered by \((k,j)\), and

\[
\begin{aligned}
 C&=2bb^{\mathsf T}+4dT,\\
 D_{i,(k,j)}&=2b_kT_{ij}+4b_iT_{kj},\\
 Q&=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
      +4T\otimes T.
\end{aligned}                                             \tag{4}
\]

Differentiating \(q^2\) proves that \(\mathcal M(q)\) is a
Hessian Gram matrix on \(Z\). The constant term \(4dT\) is
included because the rational center is not the zero.

Set

\[
 M=\mathcal M(A)+\sum_{i=0}^3\mathcal M(r_i)-\mathcal M(r_4).
                                                        \tag{5}
\]

The [exact checker](check_ternary_rational_sos_convex_counterexample.py)
verifies both identities

\[
 v^{\mathsf T}\nabla^2F(c+u)v=Z^{\mathsf T}MZ,
 \qquad M-I=LDL^{\mathsf T},\quad D_{ii}>0.              \tag{6}
\]

These are exact rational calculations. All numerators and denominators
of entries of \(M\) have at most twelve bits. A separate portable
positivity certificate is the sequence of leading principal minors of
the integer matrix \(2(M-I)\):

```text
98
8714
1060526
1508095300
505804465336
388208815855184
132268108059697184
26367351626513255040
8176807399117693383936
4716316942464353421986304
2238789673795455159378824192
1231832682931718409670151748608
```

Their positivity gives \(M-I\succ0\) by Sylvester's criterion.
Since \(\|Z\|^2\geq\|v\|^2\), (6) proves (3) and the
global Hessian bound. Changing from \((v,u\otimes v)\) to
\((v,X\otimes v)\) is an invertible rational linear change, so
congruence also gives a positive definite rational Hessian Gram matrix
on the original full monomial vector. Rational LDL factorization and
the four-square theorem express each positive rational weight as
rational squares; hence this is rational SOS-convexity.

## Two coefficients exclude rational SOS

Let \(I_2\) be the rational vector space of polynomials of degree
at most two vanishing at \(p\). Its evaluation map has rank five:
the quadratic monomials \(1,y,z,yz,x\) evaluate to nonzero rational
multiples of \(1,a,a^2,a^3,a^4\). Since there are ten quadratic
monomials, \(\dim I_2=5\). The five independent polynomials
\(r_0,\ldots,r_4\) therefore form a basis.

For a polynomial \(P\), write \([m]P\) for the coefficient of
the indicated monomial and define

\[
                    \Lambda(P)=2[z]P+4[y^2]P.
\]

Direct multiplication gives

\[
 \Lambda(r_i r_j)=
 \begin{cases}4,&i=j=4,\\0,&\text{otherwise}.
 \end{cases}                                             \tag{7}
\]

Thus \(\Lambda(q^2)=4c_4^2\geq0\) whenever
\(q=\sum_{i=0}^4c_i r_i\) with real coefficients. In contrast,
\(\Lambda(F)=-4\). The latter equality can also be read from
the two expanded coefficients \([z]F=-192\) and
\([y^2]F=95\).

Suppose \(F=\sum_j q_j^2\) with rational polynomials \(q_j\).
Highest-degree real squares cannot cancel, so every \(q_j\) has
degree at most two. Evaluating at \(p\) forces each \(q_j(p)=0\).
Consequently each \(q_j\in I_2\), and (7) would imply
\(\Lambda(F)=\sum_j\Lambda(q_j^2)\geq0\), a contradiction.
This also excludes positive rational weighted SOS and rational positive
semidefinite polynomial Gram matrices.

The functional \(\Lambda\) is nonnegative only on squares from
this particular vanishing space. It is not nonnegative on arbitrary
squares; for example, \(\Lambda((1-z)^2)=-4\). The use of the
zero and the coefficient field is essential.

## The exact coefficient field for SOS and Gram certificates

**Proposition.** For every subfield \(E\subseteq\mathbb R\), the
following statements are equivalent:

1. \(a=2^{1/5}\) belongs to \(E\).
2. \(F\) is a sum of polynomial squares over \(E\).
3. \(F\) has a positive semidefinite polynomial Gram matrix with
   entries in \(E\), on the full monomial basis of degree at most two.

The field need not be a number field or an algebraic extension.

**The irreducibility step.** If \(a\notin E\), then \(T^5-2\)
is irreducible over \(E\). Otherwise a proper monic factor of degree
\(r\in\{1,2,3,4\}\) would have constant term
\((-1)^r a^r\zeta_5^k\), where \(\zeta_5\) is a primitive
fifth root of unity. The constant is real, so \(\zeta_5^k=1\).
It follows that \(a^r\in E\). Since \(\gcd(r,5)=1\) and
\(a^5=2\), an integer Bézout identity then gives \(a\in E\),
a contradiction. Consequently \(1,a,a^2,a^3,a^4\) are linearly
independent over \(E\), and the same evaluation argument proves
that \(r_0,\ldots,r_4\) form a basis of the \(E\)-space of
quadratics vanishing at \(p\).

**SOS necessity.** An SOS over \(E\) again consists of quadratic
summands vanishing at \(p\). If \(a\notin E\), (7) contradicts
their sum having \(\Lambda(F)=-4\). This proves 2 implies 1.

**SOS sufficiency.** The rational positive definite Hessian
Gram certificate gives rational polynomials \(B_j(X,v)\), linear
in \(v\) and affine in \(X\), such that

\[
 v^{\mathsf T}\nabla^2F(X)v=\sum_j B_j(X,v)^2.
\]

Put \(u=X-p\). Taylor's formula at the stationary zero gives

\[
 F(p+u)=\sum_j\int_0^1(1-t)B_j(p+tu,u)^2\,dt.
\]

Write \(B_j(p+tu,u)=U_j(u)+tV_j(u)\), with coefficients in
\(K\). The identity

\[
 \int_0^1(1-t)(U+tV)^2\,dt
 =\frac12(U+V/3)^2+(V/6)^2
 =2\bigl((U+V/3)/2\bigr)^2+(V/6)^2
\]

expresses each integral as three squares over \(K\). Translating
back uses coefficients in the same field. Hence 1 implies 2, and 2
implies 3 by forming the polynomial Gram matrix of the square factors.

**Gram necessity.** A positive semidefinite Gram matrix over a general
real field need not factor into squares over that field, so this
direction needs a separate argument. Suppose \(a\notin E\), and
let \(m(X)\) be the ten-entry monomial vector. If
\(F=m^{\mathsf T}Qm\), with \(Q\succeq0\) and entries in
\(E\), then

\[
 m(p)^{\mathsf T}Qm(p)=0\quad\Longrightarrow\quad Qm(p)=0.
\]

Thus every row of \(Q\) is the coefficient vector of a quadratic
in the \(E\)-span of \(r_0,\ldots,r_4\). Let \(B\) be
the rational \(10\times5\) matrix of their coefficient columns,
so \(r=B^{\mathsf T}m\). Choose a rational left inverse \(C\)
of \(B\). Symmetry and the row-space statement give

\[
 Q=BSB^{\mathsf T},\qquad S=CQC^{\mathsf T}\succeq0.
\]

Now (7) implies \(\Lambda(F)=4S_{44}\geq0\), contradicting
\(-4\). This proves 3 implies 1. \(\square\)

Every real number field admitting either certificate therefore has degree
divisible by five. The smallest possible degree is exactly five, attained
by \(K\). The characterization says more than this degree condition:
the field must contain this particular real quintic field.

Any finite collection of real constructible algebraic numbers lies in
a finite tower of quadratic extensions. Its joint field degree is a
power of two, so it cannot contain coefficients of an SOS decomposition
of \(F\). This is a restriction on algebraic SOS coefficient fields,
not on all possible exact certificate formats.

## Why the perturbation works

The rational SOS baseline
\(G=A^2+\sum_{i=0}^3r_i^2\) uses a four-dimensional subspace of
\(I_2\), although its Hessian Gram is strictly positive definite.
The checker verifies this additional claim for the explicit matrix
\(M+\mathcal M(r_4)\); it is not inferred from adding an arbitrary
quadratic square to a convex polynomial.
Subtracting the missing square \(r_4^2\) retains that strict Hessian
certificate for the explicit coefficients in (1), but prevents a
positive semidefinite Gram matrix on \(I_2\).

More precisely, the fifteen products \(r_i r_j\), \(i\leq j\),
are linearly independent. Restrict to \(x=0\); their coefficient
matrix on the fifteen monomials \(y^jz^k\), \(j+k\leq4\),
has determinant \(-2^{26}\) when pairs are ordered lexicographically
and monomials by increasing \(j\), then increasing \(k\).
The checker verifies this determinant. Thus the Gram matrix on this
basis is unique and equals

\[
 \begin{pmatrix}I_4+gg^{\mathsf T}&0\\0&-1\end{pmatrix},
 \qquad g=(4,5,3,9)^{\mathsf T}.
\]

Unlike the [four-variable example](rational-sos-convex-descent.md),
this polynomial belongs to the span of products of rational vanishing
quadratics. Membership in that span is insufficient for rational SOS,
even under the strict Hessian assumption. The obstruction here is
positivity, not membership. The coefficient argument (7) already
proves the needed impossibility without relying on the determinant.

## Dimension, prior work, and relevance to exact optimization

Three is the minimal affine dimension under the stated strict Hessian
Gram assumption. In two variables, that assumption makes the leading
quartic form positive away from the origin, by Euler's identity.
Homogenization therefore has exactly one real projective zero.
[Scheiderer's published Theorem 4.1](https://ems.press/content/serial-article-files/32129)
classifies rational nonnegative ternary quartics that are not rational
SOS: they factor into four distinct complex lines in general position.
Nonnegativity excludes a real line, so there are two conjugate pairs.
Their distinct real intersection points give at least two projective
zeros, a contradiction. The [reviewed prior audit](rational-sos-convex-descent-prior.md)
gives the full argument. In one variable, the minimal polynomial of
the zero has its square dividing the quartic, so it has degree at most
two. An irrational real quadratic zero would have a second real
conjugate zero. Thus the unique zero is rational, and the rational
Taylor integration argument gives rational SOS. No dimension claim is
made after weakening the strict Hessian Gram assumption.

General failures of rational SOS descent and odd-degree descent are
established prior results. The [general audit](rational-sos-convex-descent-prior.md)
compares Scheiderer, Hillar, and Laplagne, including a known quartic
over a cubic field. The [three-variable literature comparison](three-variable-rational-sos-descent-prior.md)
examines that quaternary quartic's projective zeros, the obstruction to
turning it into the present convex example by a change of chart, and
the prior point-ideal perturbation results of Blekherman, Iliman, and
Kubitzke. The present result combines strict global SOS-convexity, a
minimum rational value, dimension three, and a complete description of
the real fields supporting SOS or PSD Gram certificates. Neither an
unsuccessful search nor the improvement over the local four-variable
construction establishes publication priority.

The [positive-constant lemma](rational-sos-convex-descent.md)
applies: \(F+\eta\) has a rational positive definite polynomial
Gram matrix for every positive rational \(\eta\). Hence

\[
 \sup\{\gamma\in\mathbb Q:F-\gamma\text{ is rational SOS}\}=0
\]

is not attained. Exact rational convexity certificates therefore do not
guarantee rational SOS certificates for the attained optimum, even in
three variables with small integer coefficients. Algebraic certificates
remain available, and this example identifies their necessary field
degree. This could guide exact certificate formats and rational
reconstruction procedures. It proves no complexity lower bound or
computational speedup, and does not exclude rational certificates using
denominators, multipliers, or other proof systems.

## Verification record

The targeted command actually run was

```text
python research-20260927/check_ternary_rational_sos_convex_counterexample.py
```

It passed exact differentiation, rational Hessian Gram construction,
positive-pivot LDL factorizations of \(M-I\) and the baseline Gram,
polynomial identity,
algebraic zero and stationarity, evaluation rank, vanishing-space basis,
all 25 functional identities, and the optional product determinant.
It also counted the monomials and bounded the expanded coefficients.
A separate exact calculation produced the listed principal minors.
These finite checks establish the explicit identities and signs; the
field arguments and minimal-dimension consequence use the proofs above.
The exploratory numerical eigenvalues were used only to choose simple
constants and play no role in verification. No project-wide checks or CI
inspection was used.

A later [targeted Lean proof](../formal/TernarySOSDescent.lean), with a
[verification record](ternary-sos-descent-lean-verification.md) and
[independent correspondence review](ternary-rational-sos-convex-lean-review.md),
also verifies the conditional zero, directional stationarity, and the
actual second affine-line derivative bound by the squared direction norm.
The exact square identity is checked inside Lean; Python is not a proof
premise. Both targeted compilations passed without warnings, and all six
axiom reports contain only the permitted foundations. The field
classification, exclusion of rational SOS, dimension minimality, and
global convexity/minimum predicates are not formalized there; their
separate mathematical proofs and reviews remain necessary.

The [independent construction review](ternary-rational-sos-convex-counterexample-review.md)
reconstructed the explicit Gram without importing the checker and used
Sylvester's criterion to verify positivity. It also checked the
vanishing-space and functional arguments. A [separate fresh review](ternary-rational-sos-convex-counterexample-independent-review.md)
checked the explicit certificate, exact SOS and PSD Gram coefficient-field
characterization, and dimension conclusion, then rechecked the final
strengthened subsection. A positive review is evidence of correctness,
not a formal verification of the mathematics or the symbolic algebra
implementation.

An inline `python -` check passed the relative links, mathematical
delimiters, final newlines, trailing whitespace, and control characters
of this note and the [search record](three-variable-rational-sos-descent-search.md),
with the applicable text checks also applied to the retained checker.
The targeted `git diff --check --` command for those three files returned
no diagnostics.
