# Recovering exact algebraic coordinates from certified approximations

Status: primary-source audit and elementary supporting derivations, 2026-09-27.
These are established tools for the witness-recovery project, not new research
claims. The input must include proved degree and coefficient bounds and a
certified approximation procedure. An arbitrary floating-point approximation is
insufficient.

## 1. The source theorem

R. Kannan, A. K. Lenstra, and L. Lovász, *Polynomial Factorization and
Nonrandomness of Bits of Algebraic and Some Transcendental Numbers*, Mathematics
of Computation 50 (1988), 235–250,
[Theorem (1.19), p. 241](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf),
[bibliographic record](https://doi.org/10.2307/2007927).
The linked PDF is a collection; the article occupies PDF pages 7–22 and the
theorem is on PDF page 13, counting the first PDF page as 1.

Write \(A\geq1\) for a bound on the absolute coefficients of the primitive
minimal polynomial of an algebraic number \(\alpha\), and \(D\geq1\) for a degree
bound. Let \(s\) be the least positive integer satisfying

\[
2^s>2^{D^2/2}(D+1)^{(3D+4)/2}A^{2D}.
\]

A rational approximation with error less than \(2^{-s}/(12D)\) determines the
minimal polynomial algorithmically. The theorem gives

\[
O\bigl(n_0D^4(D+\log A)\bigr)
\]

arithmetic operations on integers with \(O(D^2(D+\log A))\) bits, where
\(n_0\leq D\) is the actual degree. Thus its bit complexity is polynomial in
\(D\) and \(\log A\). The theorem applies without an assumption
\(|\alpha|\leq1\); Explanation (1.18) handles the larger-modulus case using a
reciprocal. Algorithm (1.16) tries degrees in increasing order, so the actual
degree need not be supplied.

The approximation precision is

\[
s+O(\log D)=O(D^2+D\log A).
\]

Consequently, polynomial-time approximation to arbitrary requested absolute
precision, together with polynomial degree and coefficient-bit bounds, gives
deterministic polynomial-time minimal-polynomial recovery. This implication
requires the approximation procedure's running time to be polynomial in the
requested number of bits, not in the reciprocal error.

## 2. A bound for an arbitrary annihilating polynomial suffices

Suppose a nonzero \(P\in\mathbb Z[X]\) satisfies \(P(\alpha)=0\),
\(\deg P\leq D\), and \(\|P\|_\infty\leq2^H\). The polynomial \(P\) need not be
known to the recovery algorithm: its existence and the explicit bounds are
enough.

Let \(m_\alpha\) denote the primitive minimal polynomial with positive leading
coefficient. Gauss's lemma gives \(m_\alpha\mid P\) in \(\mathbb Z[X]\). Mignotte's
factor bound yields

\[
\|m_\alpha\|_\infty
\leq2^D\|P\|_2
\leq2^{H+D}\sqrt{D+1}.
\tag{2.1}
\]

An accessible author-written statement is M. Mignotte, *Some Useful Bounds*,
Computing Supplementum 4 (1982), 259–263,
[Theorem 4, p. 261](https://web.dm.unipi.it/gianni/TC%26C/Mignotte.pdf).
It bounds the coefficient 1-norm of a degree-\(q\) divisor by
\(2^q\|P\|_2\) times the ratio of the absolute leading coefficients. That ratio
is at most 1 for an integer divisor. Thus one may pass

\[
H_{\min}=H+D+\left\lceil\tfrac12\log_2(D+1)\right\rceil
\]

as a coefficient-bit bound to the recognition theorem. The original related
source is Mignotte, *An Inequality About Factors of Polynomials*, Mathematics of
Computation 28 (1974), 1153–1157,
[publication record](https://doi.org/10.2307/2005373); the 1982 statement was the
one checked directly here.

There is also a sufficient elementary bound that avoids using (2.1). Cauchy's
root bound puts every root of \(P\) in \(|z|\leq1+2^H\leq2^{H+1}\).
The leading coefficient of \(m_\alpha\) has magnitude at most \(2^H\). Expanding
the product over its at most \(D\) roots gives

\[
\|m_\alpha\|_\infty
\leq2^H2^D(2^{H+1})^D
=2^{(D+1)H+2D}.
\]

This weaker bound still makes recovery polynomial in \(D,H\).

## 3. Selecting the correct real conjugate

A minimal polynomial alone does not specify a real algebraic number. A further
certified approximation gives an isolating interval using the following direct
argument; a general real-root isolation algorithm is unnecessary for this step.

Let \(p\in\mathbb Z[X]\) be the recovered irreducible polynomial of degree
\(d\leq D\) and coefficient magnitude at most \(2^K\), with \(K\geq0\).
Its roots are distinct in characteristic zero. If \(d\geq2\), write its roots as
\(r_1,\ldots,r_d\), leading coefficient as \(a_d\), and
\(R=1+2^K\). Its nonzero integer discriminant satisfies

\[
1\leq |\operatorname{disc}(p)|
=|a_d|^{2d-2}\prod_{i<j}|r_i-r_j|^2.
\]

Every root has magnitude at most \(R\). Isolating one pair in this product gives

\[
|r_i-r_j|^2
\geq
\bigl(2^{K(2d-2)}(2R)^{d(d-1)-2}\bigr)^{-1}.
\tag{3.1}
\]

In particular the deliberately conservative dyadic number

\[
\delta=2^{-4D^2(K+2)}
\]

is smaller than the distance between distinct roots. Obtain a rational \(a\)
with \(|a-\alpha|<\delta/8\), and output

\[
\left(p,\;[a-\delta/4,\ a+\delta/4]\right).
\]

The interval contains \(\alpha\) strictly and has length \(\delta/2\), so it
contains no other root. Neither endpoint is a root. For \(d=1\) the same
construction is valid without needing a separation argument. The requested
precision and interval encoding size are polynomial in \(D,K\). This proves
correct conjugate selection even if a separate root-isolation implementation
is not called.

## 4. What coordinatewise recovery does and does not establish

For a vector \(x^*\in\mathbb R^n\), suppose every coordinate has the above
bounds and a certified procedure approximates that same vector to arbitrary
precision in polynomial time. Applying recognition separately to the
coordinates constructs an exact representation by minimal polynomials and
isolating intervals in time polynomial in \(n,D,H\) and the approximation
procedure's input size. Consistency comes from the approximation procedure and
its mathematical proof.

This statement does **not** supply a polynomial bound on the degree of the
joint field, a polynomial-size primitive-element representation, or a
polynomial-time algorithm for arbitrary exact arithmetic on the output vector.
For example, the vector of square roots of \(n\) distinct primes has individual
degrees 2 but generates a multiquadratic field of degree \(2^n\). Consequently,
coordinatewise representation alone does not prove polynomial-time independent
verification of all multivariate equations and inequalities. Any stronger
certificate claim needs an additional common-field or structural argument.

The theorem also does not rescue an approximation procedure that may switch
between unrelated feasible points as precision increases. A canonical point,
or another proof that all approximations refer to one fixed point, is needed.

## 5. Verification record

- Read Kannan–Lenstra–Lovász's source statement, Algorithm (1.16), Explanation
  (1.18), and Theorem (1.19); checked the distinction between arithmetic
  operations and bit complexity.
- A separate source scout checked Mignotte's 1982 Theorem 4, and this reviewer
  independently downloaded and read the same theorem and its proof. The weaker
  elementary factor bound above also suffices for the stated use.
- Derived (3.1) directly from the discriminant identity and Cauchy's root
  bound. No numerical experiment or Lean proof was used for these arguments.
- Local source inspection used `curl`, `pdftotext`, and targeted text reads.
  A targeted Python check of this file passed for trailing whitespace, control
  characters, final newline, and paired math delimiters. No project-wide
  verification or CI inspection was run.
