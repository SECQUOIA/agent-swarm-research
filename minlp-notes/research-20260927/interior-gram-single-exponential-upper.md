# A singly exponential interior Gram bound with a supplied strict Hessian Gram

Date: 2026-09-28. Status: complete proof passed
[fresh source and construction review](interior-gram-single-exponential-upper-review.md)
without a mathematical correction. Publication priority is unestablished.

Strictly positive rational quartics with a supplied positive definite
full rational Hessian Gram admit positive definite rational polynomial
Grams with singly exponential encoding length in dimension.
Combined with the separately
[reviewed lower bound](interior-gram-bit-lower-bound.md), this
makes exponential dependence on dimension qualitatively necessary and
sufficient in this class. The constants in the exponents are not
matched, and the lower family still has short singular SOS certificates.

The proof combines an established rational sampling theorem for open
semialgebraic sets with the established SOS-convex Taylor identity.
It does not assert a new sampling method or a general bound of this
size for arbitrary interior SOS polynomials.

## Statement and input convention

Let \(n\ge1\), and let \(f\in\mathbb Q[X_1,\ldots,X_n]\) be a
strictly positive quartic. Suppose a rational matrix \(A\succ0\)
is supplied with
\[
 v^{\mathsf T}\nabla^2f(X)v
       =(v,X\otimes v)^{\mathsf T}A(v,X\otimes v).
 \tag{1}
\]
Let \(L\) be the total expanded binary encoding length of \(f\)
and \(A\), including dimension information. Use the full ordinary
quadratic monomial vector \(z(X)\), of length
\(D=\binom{n+2}{2}\).

**Theorem.** There exists a rational matrix \(Q\succ0\)
such that
\[
                         f=z^{\mathsf T}Qz
 \tag{2}
\]
whose total ordinary binary encoding length is at most
\[
                           \operatorname{poly}(L)\,2^{O(n)}.
 \tag{3}
\]
There is also an unweighted rational polynomial SOS of this total
encoding size. This is a size theorem under supplied-certificate
hypotheses. The proof identifies a construction after a rational
sample point is obtained; it does not claim a polynomial-time
algorithm in \(L\) alone.

## 1. One strict polynomial inequality selects a rational center

Put \(h=n+n^2\) and define
\[
                 \mu=\frac{\det A}{(\operatorname{tr}A)^{h-1}}>0.
 \tag{4}
\]
Then \(A\succeq\mu I\), and \(\mu\) has bit length polynomial
in \(L\). Equation (1) implies
\(\nabla^2f(X)\succeq\mu I_n\). Thus \(f\) is coercive and
has a unique minimizer \(p\), with
\(f(p)>0\) and \(\nabla f(p)=0\).

Consider the rational polynomial
\[
                   c(X)=f(X)-\frac{\|\nabla f(X)\|^2}{2\mu}.
 \tag{5}
\]
It has degree at most six, coefficient bit length polynomial in
\(L\), and \(c(p)>0\). Clearing denominators by a positive integer
gives an integer polynomial \(C\) of degree at most six, with
coefficient bit bound \(\tau=\operatorname{poly}(L)\), defining
the same nonempty basic open set
\[
                           \{X:C(X)>0\}.
 \tag{6}
\]

[Basu, Pollack, and Roy, *On the Combinatorial and Algebraic
Complexity of Quantifier Elimination*](https://www.math.purdue.edu/~sbasu/jacm95.ps),
Theorem 4.1.2, printed pages 1031--1032, gives a rational point in
each connected component of a nonempty set defined by strict integer
polynomial inequalities, with coordinate numerator and denominator
bits \(\tau d^{O(n)}\). Applied to the single inequality (6),
it supplies \(q\in\mathbb Q^n\) with
\[
 c(q)>0,\qquad
          \operatorname{bits}(q_i)\le\operatorname{poly}(L)\,6^{O(n)}.
 \tag{7}
\]
The strict-open hypothesis is exactly satisfied here. No convexity
of the set (6) is needed.

The primary theorem and proof were read directly in the repository's
PDF using:

~~~text
pdftotext -f 30 -l 31 -layout literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf -
~~~

Its use in the rational-witness comparison also has a
[separate primary-source audit](strict-convex-quartic-witness-prior.md).

## 2. An explicit rational polynomial Gram

Put \(d=X-q\), \(g=\nabla f(q)\), \(c=c(q)>0\), and
\[
                 \bar A=A-\mu\operatorname{diag}(I_n,0).
 \tag{8}
\]
Then
\[
                     \bar A\succeq\mu\operatorname{diag}(0,I_{n^2}).
 \tag{9}
\]
The Taylor Hessian vector at \(q+td\) is
\[
 (d,(q+td)\otimes d)=U(X)+tV(X),\quad
 U=(d,q\otimes d),\quad V=(0,d\otimes d).
 \tag{10}
\]
Let \(C_U,C_V\) be their rational coefficient matrices in \(z\),
so \(U=C_Uz\) and \(V=C_Vz\). Taylor's formula and
completion of the square give
\[
 f=S_q+\frac{\mu}{2}\|d+g/\mu\|^2+c,
 \tag{11}
\]
where
\[
\begin{aligned}
 S_q
 &=\int_0^1(1-t)(U+tV)^{\mathsf T}\bar A(U+tV)\,dt\\
 &=\frac12(U+V/3)^{\mathsf T}\bar A(U+V/3)
                       +\frac1{36}V^{\mathsf T}\bar A V.
\end{aligned}
 \tag{12}
\]
In particular, let \(C_{\rm aff}\) express the affine vector
\(d+g/\mu\) in \(z\), and let \(e_0\) select its constant
monomial. The following matrix is rational and represents \(f\):
\[
\begin{aligned}
 Q={}&\frac12(C_U+C_V/3)^{\mathsf T}\bar A(C_U+C_V/3)\\
    &+\frac1{36}C_V^{\mathsf T}\bar A C_V
      +\frac{\mu}{2}C_{\rm aff}^{\mathsf T}C_{\rm aff}
      +c\,e_0e_0^{\mathsf T}.
\end{aligned}
 \tag{13}
\]

Every summand is PSD. Moreover, (9) shows that the second summand
dominates the Gram of
\(\frac{\mu}{36}\sum_{i,j}(d_id_j)^2\).
Those factors, together with the affine factors in (11) and the
positive constant, span every polynomial of degree at most two.
Consequently \(Q\succ0\), rather than merely \(Q\succeq0\).
This is the same full-span step as in the reviewed Taylor existence
lemma, now with an explicit rational center-height bound.

## 3. Bit size and unweighted squares

Write \(B=\max_i\operatorname{bits}(q_i)\). Evaluation of a
degree-four rational polynomial and its gradient at \(q\) uses
polynomially many rational operations at this fixed degree.
The bit lengths of \(f(q)\), \(g\), and \(c\) are
\(\operatorname{poly}(L,n,B)\). The matrices in (10)--(13) have
polynomial dimensions, and their entries satisfy the same bound.
All products, sums, and divisions displayed there therefore give a
total Gram encoding length \(\operatorname{poly}(L,n,B)\).

Substituting (7) yields (3): a fixed polynomial in
\(\operatorname{poly}(L)6^{O(n)}\) is again
\(\operatorname{poly}(L)2^{O(n)}\).
No exponentially repeated matrix construction is hidden in (13).

Rational LDL factorization of \(Q\) has polynomial complexity and
coefficient growth in its dimension and entry bit length. It gives
rational linear forms with positive rational weights. For a weight
\(a/b>0\), expand the integer \(ab\) in binary and divide by
\(b^2\): an even power of two is one rational square, and an odd
power is two equal rational squares. The number and total length of
the resulting unweighted square factors are polynomial in the
weighted Gram encoding length. Thus they retain the bound (3).

This conversion is elementary and does not assume a polynomial-time
integer factorization or four-square algorithm.

## Consequences and limits

The combination with the lower family shows:

* An upper bound \(\operatorname{poly}(L)2^{O(n)}\) always
  suffices for an interior rational Gram under the supplied full
  positive definite Hessian hypothesis.
* Some polynomial-size inputs need
  \(\Omega(n2^{n/2})\) denominator bits in every interior Gram.
* Those lower-bound instances still have short singular rational
  Grams and short unweighted SOS certificates. The lower bound
  therefore applies to insisting on an interior certificate.

The fixed constants in the exponent, polynomial factors, and input
normalizations are not matched. The argument makes no singly
exponential claim for arbitrary SOS-interior polynomials without
the supplied Hessian structure. General rational SOS bounds require
the version care recorded in the
[literature comparison](gram-bit-size-prior.md).

The method is a consequence of established rational sampling and
Taylor SOS tools.
[Helton and Nie, *Semidefinite Representation of Convex Sets*,
Lemmas 7--8](https://arxiv.org/pdf/0705.4068v5), prove the integrated
SOS-Hessian and Taylor-remainder principles over the reals. The
author read those primary lemma proofs; their statements do not give
the rational encoding bound here. The addition is the rational-center
size reduction and explicit full positive definite Gram bound under
the supplied Hessian hypothesis, combined with the lower family.
Publication priority for this combined statement remains unestablished.

Fresh independent review checked the exact BPR theorem in both
extracted text and rendered primary pages, the center condition,
the explicit Gram and full-span proof, and total bit growth through
unweighted SOS conversion. The author independently reread the
complete review. No correction or new numerical experiment was
needed. The later Helton--Nie attribution paragraph was checked by
the author and is not part of that fresh source review.
No project-wide verification, CI inspection, or Lean formalization
was performed.
A final targeted inline Python document check passed for the lower
and upper notes, both proof reviews, the all-PSD frontier, and the
two prior-work notes: seven Markdown files and nineteen local links,
with valid math delimiters, whitespace, control characters, and
final newlines.
