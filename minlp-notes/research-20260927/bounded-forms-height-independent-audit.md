# Independent audit of the general bounded-form value bound

Date: 2026-09-28. Scope: Sections 2.1–2.2 and the coefficient accounting
in Sections 4.1–4.3 of
[the multiple-integer manuscript](unbounded-misocp-multiple-integer-frontier.md).
This reviewer did not develop that manuscript's argument. The audit finds
no mathematical gap in the degree and height accounting, conditional on
the geometric descent. The parent reviewer is separately auditing that
descent. This note does not establish novelty or audit the compressed
SOCP projection theorem.

## Primary statements checked

The full primary paper by Khachiyan and Porkolab,
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
was inspected directly, including the formulas missing from some local
text extraction:

- Theorem 1.1, printed page 208, bounds an optimal integer point. A
  constant objective gives the integer-feasibility witness version.
- Proposition 2.1, printed page 211, bounds each eliminated polynomial's
  degree and coefficient bit length independently of the number of input
  predicates. Output count and computation time do depend on that number.
- Proposition 2.2 and Corollary 2.3, printed pages 211–212, give a sample
  represented in one number field, with degree bounded in terms of degree
  and variable counts, and representation bit lengths linear in the
  input coefficient bit bound. Their representation uses an irreducible
  polynomial and a common rational denominator.

Strict inequalities and arbitrary Boolean formulas are allowed by these
statements. They impose convexity for the integer witness theorem, but
not for elimination and sampling. No closedness assumption is needed.

## Rational part: an explicit bound without repeated inversions

Here is a direct derivation of the manuscript's field-linear-algebra step.
It makes the polynomial dependence on field degree explicit; merely
saying that the factor depends on field degree would not suffice.

Suppose a real basis of an \(r\)-dimensional space \(V\subseteq\mathbb R^k\)
is sampled jointly. Write its column matrix as

\[
 W_{ij}=P_{ij}(\alpha)/q,\qquad
 g(\alpha)=0,\quad \deg g=D,\quad \deg P_{ij}<D,
\]

where \(g\in\mathbb Z[T]\) is irreducible and all integer coefficients
and \(q\ne0\) have at most \(B\) bits. The cases \(r=0\) and \(r=k\)
are immediate. Otherwise select \(r\) rows \(I\) for which \(W_I\)
is invertible. For each \(j\notin I\), the equation

\[
 \det(W_I)v_j-W_j\operatorname{adj}(W_I)v_I=0
\]

defines an annihilating row. These \(k-r\) equations have real kernel
exactly \(V\). Each coefficient is a determinant involving \(r\)
sample entries. After multiplying by \(q^r\), it is an integer
polynomial in \(\alpha\) of degree at most \(r(D-1)\), with coefficient
bits at most

\[
 rB+O(r\log(D+1)+r\log(r+1)).
\]

Reduce these polynomials modulo \(g\), allowing \(g\) to be nonmonic.
Clearing a common power of its leading coefficient, with exponent at
most \(rD\), gives degree-less-than-\(D\) representatives whose
coefficient bits are

\[
 C=O\bigl(rD(B+\log(D+1))+r\log(r+1)\bigr).
\]

One can obtain this bound directly from polynomial pseudo-division:
there are at most \(rD\) reductions, and each adds at most
\(O(B+\log(D+1))\) bits to the coefficient norm. No new field or
primitive-element construction occurs.

For rational \(v\), each field-valued equation is equivalent to its
\(D\) rational coefficient equations because
\(1,\alpha,\ldots,\alpha^{D-1}\) are rationally independent. Stack
the resulting at most \(kD\) integer rows. Its rational kernel is
exactly \(V\cap\mathbb Q^k\). Choose at most \(k\) independent rows
and construct a kernel basis by Cramer minors. The basis coefficient
bits are \(O(kC+k\log(k+1))\). Its real span is precisely the
rational part claimed in Section 2.1.

Thus if \(D\le d^{A(k)}\) and
\(B\le(H+1)d^{A(k)}\), the rational-part basis still has coefficient
bits \((H+1)d^{A'(k)}\). This is linear in \(H+1\) and has only a
power-of-\(d\) loss with exponent depending on \(k\).

## Affine equations and integer lattice changes

For a jointly sampled algebraic affine equation \(a^Tz=b\), the
common-field expansion gives rational affine equations on rational
\(z\). At least one has a nonzero normal whenever \(a\ne0\).
Clearing the common denominator gives an integer equation
\(p^Tz=c\) with the same type of bit bound. An integer point in the
cap ensures consistency, so \(\gcd(p_1,\ldots,p_k)\mid c\).

The needed lattice bound can be proved directly. Repeated two-coordinate
extended-gcd operations give a unimodular integer matrix \(U\) satisfying

\[
 p^TU=(g,0,\ldots,0),\qquad g=\gcd(p_1,\ldots,p_k)>0.
\]

If \(p,c\) have \(L\ge1\) bits, each elementary matrix has
\(O(L)\)-bit entries and there are at most \(k-1\) such matrices.
The resulting entries have \(O(k(L+\log(k+1)))\) bits. Therefore

\[
 z=U(c/g,y_1,\ldots,y_{k-1})^T,
 \qquad y\in\mathbb Z^{k-1},
\]

parametrizes every integer solution, with a bit bound linear in \(L\).
This argument also covers nonprimitive normals; requiring \(g=1\)
would have been an unnecessary restriction.

Under such a substitution, each original polynomial keeps its degree
at most \(d\). A direct coefficient-norm bound gives the new coefficient
bits at most

\[
 H+dL+d\log(k+1)+(k+1)\log(d+1)+O(1).
\]

Consequently, carrying the transformed original atoms through at most
\(k\) restrictions preserves \((H+1)d^{O_k(1)}\). Reusing arbitrary
elimination output as the next carried description is unnecessary.
Neither a number of field operations depending on \(H\) nor an
uncontrolled product of denominator lengths is hidden here.

## Cap, endpoints, and attainment

Upward closure turns any feasible integer \(z\) into a fully integer
pair \((z,t)\) by rounding a feasible \(t\) upward. The integer witness
theorem therefore supplies a cap \(U=t+1\) of the stated bit length.
For a witness-only use of Theorem 1.1, one can append a zero objective
coordinate; replacing \(k+1\) by \(k+2\) does not change the displayed
\(O((k+1)^4)\) exponent class. This step does not assume an optimal
mixed-integer point exists.

A finite endpoint of a one-dimensional semialgebraic set must be a zero
of at least one nonzero defining polynomial after elimination. Otherwise
all nonconstant polynomial signs, and hence the formula's truth value,
would be locally constant there. This remains true for open endpoints
and singleton sets. Identically zero atoms can be discarded first.

After the finite value is bounded, its primitive minimal polynomial and
a rational isolating interval have the same coefficient-sensitive bound,
after changing the dimension-dependent exponent. Introducing a real
variable selected by that polynomial and interval describes exactly the
optimal projection. That projection is convex; if it contains an integer
point, the quantified integer witness theorem yields the claimed optimal
integer-vector bound. The argument does not confuse a limit value with
membership at that value.

No targeted numerical experiment was needed for these symbolic bounds.
The checks here concern proof dependencies and coefficient arithmetic;
they do not test an implementation or establish practical efficiency.
