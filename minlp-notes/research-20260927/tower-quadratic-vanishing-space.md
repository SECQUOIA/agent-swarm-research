# The quintic tower has a small quadratic vanishing space and unique rational SOS Grams

Date: 2026-09-28. Status: complete uniform proofs and exact finite checks;
[fresh adversarial review](tower-quadratic-vanishing-space-review.md) passed
without a substantive correction. No publication-priority claim is made.

For the supplied quintic tower point in the
[exponential SOS-field construction](exponential-least-sos-field.md),
the entire rational quadratic vanishing space has a basis of only five
relations per gate. Pairwise products of these basis relations are also
linearly independent. Consequently, rational SOS recognition for rational
quartics with this particular supplied zero reduces to rational linear
algebra and one positive-semidefiniteness test of order \(5k\).

The result concerns rational polynomial SOS certificates. It does not
decide real SOS, find an unknown zero, or cover arbitrary root circuits.
Its immediate use is to describe the full rational certificate space of
the tower, including all quadratic directions eligible for the companion
[multiplier construction](rational-tower-quadratic-denominator.md).
The reviewed [stationary-space continuation](tower-quartic-stationary-space.md)
proves that the pair-product span is exactly the rational quartics with
zero value and zero ambient gradient at the tower point.

## 1. The complete rational quadratic space

Fix \(k\geq1\), set \(D=5^k\), and define
\[
 a_i=2^{1/5^i},\qquad
 p=(a_i,a_i^2,a_i^3)_{i=1}^k\in\mathbb R^{3k}.
\]
Use variables \((x_i,y_i,z_i)\) for gate \(i\), and set
\(b_1=2\), \(b_i=x_{i-1}\) for \(i>1\). Write
\[
\begin{aligned}
 q_{i,1}&=x_i^2-y_i,&
 q_{i,2}&=x_i y_i-z_i,&
 q_{i,3}&=y_i^2-x_i z_i,\\
 q_{i,4}&=y_i z_i-b_i,&
 q_{i,5}&=z_i^2-b_i x_i.
\end{aligned}                                                   \tag{1}
\]
Let
\[
 I_2=\{q\in\mathbb Q[X]_{\leq2}:q(p)=0\}.
\]

**Theorem 1.** The \(5k\) polynomials in (1) form a basis of
\(I_2\). In particular,
\[
 \dim_{\mathbb Q}I_2=5k,\qquad
 \dim_{\mathbb Q}\operatorname{ev}_p(\mathbb Q[X]_{\leq2})
   =\binom{3k+2}{2}-5k=1+4k+9\binom{k}{2}.                    \tag{2}
\]

**Proof.** Every relation in (1) vanishes at \(p\), including
\(a_i^6=b_i(p)a_i\). Use each relation to eliminate its respective
pivot monomial
\[
 x_i^2,\quad x_i y_i,\quad y_i^2,\quad y_i z_i,\quad z_i^2.
                                                                    \tag{3}
\]
Each right-hand side is a linear combination of monomials outside this
pivot list. The retained monomials are exactly:

1. the constant \(1\);
2. \(x_i,y_i,z_i,x_i z_i\) for every gate;
3. all nine products of one variable from gate \(i\) and one from
   gate \(j\), for \(i<j\).

Let \(a=a_k\). Since \(a_i=a^{5^{k-i}}\), the retained monomials
evaluate to powers \(a^e\) whose exponents have the following base-five
forms: all digits zero; a single nonzero digit in \(\{1,2,3,4\}\);
or exactly two nonzero digits, each in \(\{1,2,3\}\). These
patterns are distinct, and every exponent is less than \(5^k\).

The polynomial \(T^{5^k}-2\) is irreducible over \(\mathbb Q\) by
Eisenstein's criterion at two. Therefore these retained evaluations are
linearly independent over \(\mathbb Q\). Reducing any element of
\(I_2\) using (1) leaves a linear combination of retained monomials
that evaluates to zero, so the remainder is zero. Finally, the distinct
pivots (3), which never occur on the right-hand sides, prove independence
of the \(5k\) relations. This proves both claims. \(\square\)

This argument handles the wrap at \(D\) without treating all collision
classes as pairs. At the first gate,
\(y_1z_1=2\) and \(z_1^2=2x_1\) under evaluation. For \(k\geq2\),
the three monomials \(x_1,y_2z_2,z_1^2\) evaluate to rational multiples
of the same power of \(a\); the two corresponding relations in (1)
already span that collision class. The case \(k=1\) leaves precisely
\(1,x_1,y_1,z_1,x_1z_1\), with evaluations \(1,a,a^2,a^3,a^4\).

**Affine membership consequence.** Define the three chain residuals
\(r_{i,1}=q_{i,1}\), \(r_{i,2}=q_{i,2}\), and
\(r_{i,3}=q_{i,4}\). The exact identities
\[
 q_{i,3}=-y_i r_{i,1}+x_i r_{i,2},\qquad
 q_{i,5}=-z_i r_{i,2}+x_i r_{i,3}                         \tag{4}
\]
show that every member of \(I_2\) is a sum of the \(3k\) chain
residuals with rational affine multipliers. The resulting individual
products may have degree three; their degree-three terms cancel.
This is a uniform degree bound for membership of the quadratic piece,
not an assertion of such a bound for all elements of the full ideal.

## 2. Pairwise products are independent

Order the relations in (1) gate by gate, and let \(q\) be their column
vector of length \(5k\).

**Theorem 2.** The multiplication map
\[
 \Psi:\operatorname{Sym}_{5k}(\mathbb Q)\longrightarrow
        \mathbb Q[X]_{\leq4},\qquad A\longmapsto q^{\mathsf T}Aq
                                                                    \tag{5}
\]
is injective. Equivalently, all \(\binom{5k+1}{2}\) unordered pairwise
products of the relations are linearly independent. The same
injectivity holds after extending scalars to \(\mathbb R\).

**Proof.** For a single gate, the parts of degree two in its own three
variables are
\[
 L=(x^2,xy,y^2-xz,yz,z^2).                                  \tag{6}
\]
Their fifteen unordered products span all ternary homogeneous quartics.
Ten quartic monomials are directly products of entries of \(L\):
\[
 x^4,x^3y,x^2y^2,x^2yz,x^2z^2,xy^2z,xyz^2,y^2z^2,yz^3,z^4.
\]
The remaining five follow from
\[
\begin{aligned}
 x^3z&=L_2^2-L_1L_3,&
 xy^3&=L_2L_3+L_1L_4,\\
 y^3z&=L_3L_4+L_2L_5,&
 xz^3&=L_4^2-L_3L_5,\\
 y^4&=L_3^2+2L_2L_4-L_1L_5.
\end{aligned}                                                    \tag{7}
\]
There are fifteen quartic monomials and fifteen products, so the latter
are independent. The five quadratics in (6) are also independent.

Now induct on the number of gates in a relation among the products in
(5). Consider polynomial degree only in the last gate's variables
\((x_k,y_k,z_k)\), allowing coefficients in the earlier variables.
All earlier-gate relations have degree zero in this triple. Each
last-gate relation has degree-two part equal to the corresponding
entry of (6): the term \(-b_kx_k\) has last-gate degree one, and
\(-b_k\) has last-gate degree zero.

Consequently, the last-gate degree-four part of a product dependence
contains only products of two last-gate relations. Independence of
the fifteen products in (6) forces their scalar coefficients to zero.
The last-gate degree-two part of what remains is
\[
                      \sum_{j=1}^5 L_j P_j=0,                \tag{8}
\]
where each \(P_j\) is a rational linear combination of earlier-gate
relations. Independence of the \(L_j\) remains valid over the
polynomial ring in earlier variables, so every \(P_j\) is zero.
Theorem 1 applied to the earlier gates forces all cross coefficients
to zero. The remaining dependence concerns earlier gates only and
vanishes by induction. The argument also works over \(\mathbb R\),
since the rationally independent coefficient columns retain their rank
over a field extension. \(\square\)

## 3. Exact rational SOS recognition for this supplied zero

**Corollary 3.** Given \(k\) and a rational polynomial \(F\) of degree
at most four satisfying \(F(p)=0\), the following are equivalent:

1. \(F\) is a sum of squares of rational polynomials.
2. \(F\) has a rational positive semidefinite Gram matrix on all
   monomials of degree at most two.
3. \(F\) belongs to the image of (5), and its unique symmetric matrix
   \(A\) in (5) is positive semidefinite.

These conditions can be decided in deterministic time polynomial in
\(k\) and the explicit rational input length. In the affirmative case,
one can construct a rational SOS in polynomial time and output length.
There is exactly one rational positive semidefinite Gram matrix on the
full monomial basis. This does not assert uniqueness of real Gram matrices.

**Proof.** In an SOS for a polynomial of degree at most four, every
square factor has degree at most two: highest-degree homogeneous squares
cannot cancel over \(\mathbb R\). If the factors are rational and
\(F(p)=0\), each factor vanishes at \(p\), so Theorem 1 puts it in
the span of \(q\). This yields a rational positive semidefinite
matrix \(A\). Theorem 2 makes it unique.

Conversely, a rational positive semidefinite matrix admits a rational
congruence decomposition into nonnegative rational scalar weights and
rational linear forms. A positive rational weight \(u/v\), with
positive integers \(u,v\), is a sum of polynomially many rational
squares: expand \(uv\) in binary and divide by \(v^2\); an even
power of two is one square, and an odd power is two equal squares.
Thus no extension of the coefficient field is needed.

For completeness, let \(m\) be the full monomial vector and write
\(q=B^{\mathsf T}m\), where \(B\) is rational and has full column
rank. If a rational matrix \(Q\succeq0\) satisfies
\(F=m^{\mathsf T}Qm\), then \(m(p)^{\mathsf T}Qm(p)=0\) implies
\(Qm(p)=0\). Every row of \(Q\) therefore represents a member of
\(I_2\). Symmetry implies
\(\operatorname{range}Q\subseteq\operatorname{range}B\). Choose
a rational left inverse \(C\) of \(B\). Then
\[
              Q=B A B^{\mathsf T},\qquad A=CQC^{\mathsf T}\succeq0.
                                                                    \tag{9}
\]
Theorem 2 uniquely determines \(A\), hence \(Q\).

Computationally, the columns of (5) have bounded integer entries and
polynomial dimensions. Rational linear algebra determines membership
in their span and recovers \(A\), whose bit length is polynomial in
the input length. Exact rational symmetric elimination tests
positive semidefiniteness and supplies the congruence decomposition.
The binary-weight conversion above keeps the certificate polynomial
in length. If validation of \(F(p)=0\) is desired, evaluate each
monomial as \(2^t a^e\), reducing its exponent modulo \(5^k\), and
collect coefficients with equal residues. All exponent integers have
\(O(k)\) bits; no dense degree-\(5^k\) field representation is required.
\(\square\)

This gives a full description of the rational certificate cone in
this special class: it is the rational positive semidefinite cone of
order \(5k\), carried into quartic coefficient space by an injective
linear map. Its closure over real coefficients is the image of the
real positive semidefinite cone under the same map. The latter is the
cone of squares drawn from \(I_2\otimes_{\mathbb Q}\mathbb R\),
which is much smaller than the space of all real quadratics vanishing
at \(p\). Confusing those two vanishing spaces would incorrectly turn
the rational recognition theorem into a real SOS recognition theorem.

## 4. Consequences, prior work, and limits

The complete basis upgrades statements about one selected missing
relation to statements about all rational quadratic relations at the
tower zero. Equation (4) provides the required affine ideal membership
for any such relation. A simultaneous multiplier theorem can use this
fact, but that theorem needs its own positivity proof, especially for
nonhomogeneous relations and cross terms. It is not inferred here from
membership alone.

The recognition result can detect whether a proposed rational quartic
in this supplied-zero class has any rational SOS certificate, without
searching over algebraic coefficient fields or solving an SDP feasibility
problem with a free matrix. Its potential solver value is structural:
an exact certificate routine for detected tower subproblems could use
this recognition step. Detection of such subproblems and evidence that
they arise usefully in MINLP models remain necessary for practical value.
The result does not provide a general MINLP complexity improvement.

The algebraic tools are classical. Eisenbud and Sturmfels,
[Binomial Ideals](https://arxiv.org/abs/alg-geom/9401001), study ideals
generated by binomials and their structural and computational properties;
their abstract was examined as background. No new general result about
binomial ideals is claimed here. The explicit degree-two normal form and
uniform product-independence calculation are for this particular tower.

Laplagne,
[Sum of squares decomposition of positive polynomials with rational coefficients](https://arxiv.org/pdf/2312.16801),
Section 2 and Proposition 3.1, uses the standard restriction of SOS factors
to kernels of positive semidefinite functionals and studies rational
vectors inside those kernels. Section 3.2 also recalls an example with
unique SOS decompositions up to orthogonal transformations. These passages
were read directly. Thus neither the kernel restriction nor uniqueness
as an SOS mechanism is new. What is supplied here is an explicit uniform
description for the quintic tower and its elementary exact recognition
consequence. These two sources do not establish publication priority;
no claim is made that an equivalent tower calculation is absent elsewhere.

The local fifteen-product calculation also appears in the repository's
[least-field proof](exponential-least-sos-field.md). The new step here is
the induction that couples all gates and characterizes the full rational
quadratic space, rather than only the final-gate specialization.

## 5. Targeted verification

The author ran:

```text
python3 research-20260927/check_tower_quadratic_vanishing_space.py
```

The command passed. Using exact integer and rational arithmetic, it checks:

- the rank of the complete evaluation map on all degree-at-most-two
  monomials, the rank of the proposed basis, and identities (4), for
  \(k=1,\ldots,32,64,100\);
- the first-gate wrap factors and the three-monomial collision above;
- the determinant of the local fifteen-product matrix, equal to \(1\)
  in the script's ordering;
- the rank of the full pair-product list for \(k=1,\ldots,12\).

The script does not use numerical root approximations. Its finite cases
do not prove the uniform results or the complexity claim; those rely on
the arguments above. No Lean verification, project-wide checks, or CI
inspection was performed for this note.
