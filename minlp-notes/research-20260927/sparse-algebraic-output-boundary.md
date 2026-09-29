# Sparse minimal-polynomial output can also be large

Date: 2026-09-28. Status: elementary refinement of the reviewed
[short-input degree construction](short-input-qcqp-degree-lower-bound.md).
The translation and coordinate-change arguments below have a separate
[independent review](sparse-algebraic-output-review.md). They concern a
specified output representation, not the complexity of finding or
approximating an optimizer.

The existing construction forces a large algebraic degree for the optimal
value and the joint optimizer field. Two small changes strengthen its
output-size consequence. Adding a short integer to the objective makes
the minimal polynomial of its value have no zero coefficients. An integer
change of variables can also make one specified optimizer coordinate
generate the entire field; another short translation makes that
coordinate's minimal polynomial have no zero coefficients. Consequently,
allowing explicit sparse coefficient lists or separate coordinate minimal
polynomials does not give a fixed-parameter output bound for these
particular formats.

## 1. Output convention and statement

An **explicit sparse minimal polynomial** here is a list of all pairs
\((j,c_j)\) with \(c_j\ne0\) in the ordinary monomial expansion
\(\sum_j c_j X^j\) of the minimal polynomial over \(\mathbb Q\) of the
requested number. A monic rational normalization or a primitive integer
normalization makes no difference to the nonzero positions. The polynomial
is for the actual optimal value or actual input-coordinate value. A
polynomial for a different generator, accompanied by a map, is a different
output format.

**Theorem.** There are families of rational QCQPs with \(n\) variables,
exactly \(h\) quadratic constraints, positive definite objective and
constraint Hessians, a compact feasible set, and a strict feasible point,
with the following properties. For primes
\(p_1<\cdots<p_h\), each congruent to one modulo four, put

\[
 n=\sum_{i=1}^h(p_i-1),\qquad P=p_h,\qquad
 D=\prod_{i=1}^h2(p_i-1).
\]

The native constraint Hessian span has dimension exactly \(h\). There is
a unique optimizer \(y^*\), and both its first coordinate \(y_1^*\) and
the optimal value \(w\) have degree \(D\) over \(\mathbb Q\). Each of their
minimal polynomials has exactly \(D+1\) nonzero monomials. The total dense
rational input length can be bounded by

\[
 N=O\bigl((h+1)n^2[1+h^2\log(P+1)]\bigr).       \tag{1}
\]

The coefficient choices added here are existence statements with explicit
bit bounds. No polynomial-time method of finding these choices is
asserted.

Therefore no running-time bound \(f(h)N^C\), with an absolute constant
\(C\) and an arbitrary finite function \(f\), is possible for an algorithm
that must always return either the value in this format or an optimizer
as separate minimal polynomials over \(\mathbb Q\) for its input
coordinates. This is an unconditional output-length obstruction. It does
not establish computational hardness for a more succinct exact output.

## 2. A bounded translation removes every zero coefficient

Let

\[
 P_0(X)=\sum_{i=0}^D a_iX^i\in\mathbb Q[X],\qquad a_D\ne0.
\]

Write the translated polynomial as

\[
 P_0(X-t)=\sum_{j=0}^D b_j(t)X^j,\qquad
 b_j(t)=\sum_{i=j}^D a_i\binom ij(-t)^{i-j}.     \tag{2}
\]

For each \(j\), \(b_j\) has degree exactly \(D-j\), with leading
coefficient \(a_D\binom Dj(-1)^{D-j}\). In characteristic zero this
coefficient is nonzero. Thus the nonzero polynomial

\[
 \prod_{j=0}^{D-1}b_j(t)
\]

has degree

\[
 M=\sum_{j=0}^{D-1}(D-j)=\frac{D(D+1)}2.
\]

At most \(M\) integers make any coefficient vanish. Some

\[
 t\in\{0,1,\ldots,M\}                            \tag{3}
\]

therefore makes all \(D+1\) coefficients nonzero. This \(t\) needs only
\(O(\log(D+1))\) bits.

If \(P_0\) is the minimal polynomial of an algebraic number \(a\), then
\(P_0(X-t)\) is irreducible over \(\mathbb Q\) and annihilates \(a+t\).
It is consequently a scalar multiple of that number's minimal polynomial.
For an integer primitive \(P_0\), integer translation also preserves
content: the substitutions \(X\mapsto X-t\) and \(X\mapsto X+t\) are
inverse automorphisms of \(\mathbb Z[X]\). Hence normalization cannot
remove any of these nonzero terms.

Apply this lemma to the degree-\(D\) optimal value \(v\) in the source
construction. Replacing its objective \(f\) by \(f+s\), with an integer
\(s\) as in (3), gives a value \(w=v+s\) whose minimal polynomial has
\(D+1\) nonzero terms. The feasible set, optimizer, and all Hessians are
unchanged. Since \(\log D=O(h\log(P+1))\), this objective constant has
short binary length.

## 3. One coordinate can generate the whole field

In the source construction, let \(a_i=x_{i1}^*\) be the first optimizer
coordinate of block \(i\). Its block multiplier is recovered from

\[
 \lambda_i=K_i/a_i-1.
\]

Thus the \(a_i\)'s generate the optimizer field
\(E=E_1\cdots E_h\), which has degree \(D\). This remains true after the
positive definite constraint modification in Section 6 of the source
note: that modification preserves the same optimizer.

For two distinct embeddings \(\sigma,\tau:E\to\mathbb C\), the polynomial

\[
 \sum_{i=1}^h T^{i-1}\bigl(\sigma(a_i)-\tau(a_i)\bigr)       \tag{4}
\]

is nonzero, since the embeddings differ on some generator. Its degree is
at most \(h-1\). There are \(D(D-1)/2\) unordered pairs of embeddings, so
some integer

\[
 1\le k\le1+\frac{(h-1)D(D-1)}2                    \tag{5}
\]

causes no collision. For this \(k\),

\[
 \alpha=\sum_{i=1}^h k^{i-1}a_i                    \tag{6}
\]

has \(D\) distinct conjugates and generates \(E\). When \(h=1\), simply
take \(k=1\). The largest weight in (6) has
\(O(h\log(h+1)+h\log(D+1))=O(h^2\log(P+1))\) bits.

Order the original coordinates so that \(x_{11}\) is coordinate one. Make
the integer change of variables

\[
 y_1=x_{11}+\sum_{i=2}^h k^{i-1}x_{i1}+t,
 \qquad y_j=x_j\quad(j\ne1),                      \tag{7}
\]

where the integer \(t\) is selected by (3) for the minimal polynomial of
\(\alpha\). The linear part \(U\) of (7) is a row shear with determinant
one. Its inverse is explicit:

\[
 x_{11}=y_1-t-\sum_{i=2}^h k^{i-1}y_{i1},
 \qquad x_j=y_j\quad(j\ne1).                      \tag{8}
\]

The transformed optimizer has \(y_1^*=\alpha+t\). This coordinate has
degree \(D\), and its minimal polynomial has every coefficient nonzero.
The separate objective shift \(s\) from Section 2 makes the value dense as
well. The two shifts are chosen independently; each has the bound (3).

Under (8), a Hessian \(Q\) becomes \(U^{-T}QU^{-1}\). This invertible
linear congruence preserves positive definiteness and preserves the
dimension of the span of the constraint Hessians. The affine bijection
also preserves compactness, strict feasibility, and uniqueness of the
optimizer. The objective value before its constant shift is unchanged.
Thus all the optimization properties in the theorem hold.

## 4. Input length and the parameter lower bound

Use the short existential objective weights in Section 4 of the source
note, followed by its positive definite constraint modification. All
original objective and constraint Hessians are diagonal, and every
coefficient has \(O(h^2\log(P+1))\) bits. The additional integers in
(3) and (5), and the weights in (7), satisfy the same bound.

Only the original variable \(x_{11}\) is replaced by a nontrivial affine
expression in (8). In each quadratic polynomial, expanding its diagonal
\(x_{11}^2\) term produces one square of that expression. Each resulting
coefficient is a sum of a bounded number of products of original
coefficients, shear weights, and \(t\); the untouched diagonal and linear
terms add at most one further coefficient. Their bit lengths therefore
remain \(O(h^2\log(P+1))\). Adding \(s\) affects only the objective
constant. There are \(O((h+1)n^2)\) coefficient positions in a dense
encoding, proving (1). No coefficient expansion of a degree-\(D\)
minimal polynomial is part of the input.

For fixed \(h\), take the primes in \([R,2R]\), as in the source
construction. Arbitrarily large such intervals contain \(h\) primes in
the required residue class. Then

\[
 N=O_h(R^2\log R),\qquad D\ge[2(R-1)]^h.         \tag{9}
\]

Each of the two requested minimal polynomials has \(D+1\) nonzero
terms. Even a sparse term list needs at least \(D+1\) records, irrespective
of the coefficient magnitudes. If the claimed running time were
\(f(h)N^C\), choose a fixed integer \(h>2C\) and let \(R\) grow. Equation
(9) makes this claimed bound smaller than the required output length.
The unknown search cost for \(s,t,k\) has no bearing on this contradiction:
the existence of valid inputs of the stated length is sufficient.

## 5. What this refinement does and does not establish

The new point is specific. The original block construction allowed all
separate optimizer coordinates to have small absolute degrees, even when
their joint field was large. The shear in (7) removes that possibility
for one required input coordinate. The translations remove zero
coefficients as a possible saving in its explicit minimal polynomial and
the value's explicit minimal polynomial.

The conclusion still does not cover a polynomial written in a shifted
power basis, an arithmetic circuit for a polynomial, a nonminimal
annihilating polynomial, a compact tower of number fields, an implicit
system of polynomial equations, or another primitive generator with a
rational expression for the requested answer. Such representations are
not lists of the ordinary-monomial coefficients required here. No lower
bound for feasibility, exact comparison, numerical approximation, or all
exact output formats follows. In particular, (7) can be undone with a
short circuit, so the construction has not made the underlying problem
harder to represent implicitly.

For a small illustration of the distinction, \(\sqrt2+\sqrt3+1\) has
minimal polynomial

\[
 X^4-4X^3-4X^2+16X-8,
\]

which has every coefficient nonzero. Its displayed nested expression is
still short. Density of a minimal polynomial is a property of the output
basis and requested scalar, not an intrinsic lower bound on every exact
description.

## 6. Literature comparison and verification

The field construction and its comparisons with generic QCQP degree,
trust-region secular equations, and effective Hilbert irreducibility are
documented in the source note and its
[arithmetic review](short-input-degree-adversarial-review.md). The present
note uses that result as an input; it does not repeat its irreducibility
or local-field proof. The bounded primitive-element argument in Section 3
is the same classical embedding-collision argument already used for the
source note's objective weights.

The dependence of polynomial sparsity on a shift is established subject
matter. Giesbrecht and Roche explicitly distinguish dense, sparse, and
shifted-lacunary representations and exhibit large differences between
their sizes. Their interpolation problem and algorithms concern the
smallest shifted representation. Here the elementary root-count argument
is used only to choose a short shift whose ordinary representation is
dense. No novelty is claimed for either this algebraic observation or the
general representation distinction. [Giesbrecht–Roche, author-hosted
extended abstract, Section 1](https://cs.uwaterloo.ca/~mwg/files/lacunaryShift.pdf).

Minimal polynomials and arbitrary annihilating multiples are also
different representation questions. Giesbrecht, Roche, and Tilak study
whether a given polynomial has a multiple with a prescribed number of
nonzero terms. The present argument supplies no lower bound for that
problem. [Giesbrecht–Roche–Tilak, primary abstract](https://arxiv.org/abs/1009.3214).

Sources examined for this refinement were the two local construction
notes and their reviews, the introduction of the Giesbrecht–Roche
extended abstract, and the primary abstracts of its full version and of
the sparse-multiples paper. Searches included polynomial translation,
sparsest shifts, shifted-lacunary interpolation, and sparse multiples.
No separate priority claim is made for the QCQP output-format corollary;
this is a modest clarification of the short-input degree lower bound.

The general translation, primitive-element, congruence, and bit-length
arguments are proved above and independently audited in the companion
review. That reviewer ran targeted exact symbolic checks of the
translation and affine-substitution formulas and records their limits.
No computational test or formal proof is claimed to establish the general
statements. A targeted inline Python document check passed for this file:
its three local links resolve, its mathematical delimiters are balanced
without nesting, and its newline, whitespace, and control-character
checks pass. No project-wide check or CI inspection was performed.
