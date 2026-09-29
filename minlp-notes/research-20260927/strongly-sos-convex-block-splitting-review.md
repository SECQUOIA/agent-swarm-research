# Independent review of the strongly SOS-convex block obstruction

Date: 2026-09-28. Status: the fixed counterexample and the strictly
positive sparse-certificate lower bound pass independent review after
one input-scope correction to the extension lemma. Publication priority
was not assessed.

This review concerns
[the frozen strong-convexity supplement](strongly-sos-convex-block-splitting-obstruction.md).
The reviewer did not contribute to that construction. The underlying
[quartic lifting theorem](rational-block-sos-splitting-obstruction.md)
has a separate fresh review; here its certificate, zero, and size
properties are treated as imported hypotheses, and their use in the
supplement is checked. The reviewed singleton realization, quintic
field obstruction, tiny-minimum family, and rational-center Taylor
lemma are also dependencies, rather than new results proved by this
review.

The final reviewed source, including the explicit \(r\ge1\) assumption
and the local-Gram convention, had SHA-256
`41f7981ce69df273ea872c4ebdf6977d5c1bb1558e5a6797671cec48353805a1`,
obtained with
`sha256sum research-20260927/strongly-sos-convex-block-splitting-obstruction.md`.

The original extension lemma assumed only that its baseline polynomial
was rational SOS, while claiming polynomial-size SOS output from the
expanded polynomial and Hessian Gram. Appending squares bounds the
output only when a baseline SOS certificate is supplied and counted.
The author amended the lemma to include that certificate in the input.
This amendment was checked. The fixed degree-five application already
supplies a short rational SOS, so the correction does not change either
counterexample or the quantitative separation.

The final lemma explicitly assumes \(r\ge1\) and \(s\ge1\).
This matters because the chosen bound divides by \(rs\). A quartic in
no point variables is not a case used by the construction.

The new Hessian calculation is correct. Differentiating
\(\epsilon\|v\|^2(1+\|u\|^2+\|v\|^2)\) gives the six terms
in equation (3), including the mixed term
\(8\epsilon(u^{\mathsf T}a)(v^{\mathsf T}b)\). In the stated
ordering, that term is represented by the old-new block
\(4\epsilon e_re_s^{\mathsf T}\), because a symmetric Gram counts
the cross block twice. The four new diagonal blocks have minimum
eigenvalue at least \(2\epsilon\); the squared operator norm of
the cross block is exactly \(16\epsilon^2rs\). No other mixed
block is needed.

For an \(h\)-by-\(h\) positive definite matrix \(A_0\), each
eigenvalue is at most \(\operatorname{tr}A_0\). Factoring the
smallest eigenvalue out of the determinant therefore proves
\[
 \lambda_{\min}(A_0)\ge
 \frac{\det A_0}{(\operatorname{tr}A_0)^{h-1}}=\rho.
\]
Thus the Schur complement is bounded below by
\[
 \left(2\epsilon-16\epsilon^2rs/\rho\right)I
 \succeq\epsilon I
\]
for the stated choice, including equality in the allowed upper bound
on \(\epsilon\). The full matrix is positive definite. Its
constant direction coordinates give a positive global Hessian lower
bound. This verifies positivity of the ordinary Gram matrix, not only
positivity on the restricted monomial vectors.

The added polynomial is an SOS of the displayed linear and quadratic
monomials with positive rational weights. Since
\(1+\|u\|^2+\|v\|^2>0\), it vanishes exactly when \(v=0\).
Combining this with the baseline zero proves the asserted singleton
zero set. The quartic degree is preserved.

All encoding claims for this amended lemma are justified. Rational
determinants and trace powers have bit length polynomial in matrix
dimension and entry length; the same holds for \(\rho\), a chosen
\(\epsilon\), and the assembled Gram. The number of added monomial
squares is polynomial in \(r+s\). For a positive rational weight
\(a/b\), write the integer \(ab\) in binary. An even-position
binary power is one integer square, and an odd-position power is two
equal integer squares. Dividing these integers by \(b\) represents
\(a/b\) with at most twice the bit length of \(ab\) rational
squares and polynomial total length. Rational LDL factorization gives
the same bound for the Hessian certificate. These arguments neither
factor integers nor recover an unspecified SOS of the baseline.

An invertible rational affine substitution preserves positive
definiteness by an invertible rational congruence on the full Hessian
basis. For \(z=Lw+c\), the direction vector becomes \(L\eta\),
and \(z\otimes L\eta\) is a linear combination of
\((\eta,w\otimes\eta)\). Both the direction and tensor diagonal
blocks of this basis map are invertible. With the affine map included
in the input, fixed-degree substitution and this congruence have
polynomial bit length.

For the particular nine-variable map, the inverse is explicit:
\[
 \begin{aligned}
 y_1&=u_1,&y_2&=u_2,&y_3&=u_3,&z_{13}&=u_4,\\
 z_{11}&=v_1+u_2,&z_{12}&=v_2+u_3,&z_{22}&=v_3+u_4,\\
 z_{23}&=v_4+2,&z_{33}&=v_5+2u_1.
 \end{aligned}
\]
The point in equation (8) has exactly the six products of
\((a,a^2,a^3)\), using \(a^5=2\), and maps to the four-coordinate
power-basis point with all five new coordinates zero. The degree-five
power-basis realization applies because \(T^5-2\) is irreducible
and has exactly one real root. It supplies the baseline SOS as well
as the full positive definite rational Hessian Gram.

For the lifted polynomial \(g_0\), the existence of a rational
symmetric Hessian Gram does not assert its positivity. Such a Gram
exists because every direction-quadratic, point-degree-at-most-two
monomial is a product of two entries of the full basis. The norm bound
\(\|C\|_2\le\sum_{ij}|C_{ij}|=U\) and
\(A_B\succeq\beta I\) give
\[
 C+T A_B\succeq(-U+T\beta)I\succeq I.
\]
The ceiling and the extra one in equation (10) have the correct
direction. Adding \(TB\) preserves the joint rational SOS and the
common zero; it makes \(g\) strongly SOS-convex and leaves its unique
zero at \(w_0\). All data here are fixed, independent of \(k\).

The block-existence obstruction is valid. Independence of the two
variable groups forces any block certificate to differ from
\((f,g)\) by one rational constant. Evaluation at their zero minima
forces that constant to vanish, contradicting the imported rational
SOS obstruction for \(f\). Restriction of the joint certificate at
the algebraic zero of \(f\) gives a real SOS for \(g\), so there
is no claimed failure over the reals.

For the strictly positive family, \(f\), \(g\), and \(h_k\)
have global Hessian lower bounds at least the identity, with rational
SOS Hessian certificates. Their sum has the same lower bound and a
polynomial-size certificate, obtained by embedding and adding the
three certificates. Its variable count is \(12+2k\), and its
minimum is exactly \(m_k\), attained independently in the three
blocks. Fixed data for \(f+g\) and polynomial-size data for \(h_k\)
give the claimed polynomial input and unrestricted SOS size.

The sparse lower bound is nonvacuous. Choose rational
\(0<c<m_k\) and rational \(s>0\) with \(c+s<m_k\). The
rational-center Taylor lemma applies to \(f+c\) and
\(h_k-c-s\): they remain strictly positive and retain their full
positive definite rational Hessian Grams. Rational points are dense,
so continuity at \(p\) supplies a rational point \(q\) with
\(f(q)<s\). The joint rational certificate specialized at \(q\)
gives \(g+f(q)\) as a rational SOS; adding the positive rational
constant \(s-f(q)\) gives one for \(g+s\). This constructs both
prescribed blocks. It does not claim these choices have short
encodings and does not apply the full-Hessian Taylor lemma to the
separable polynomial \(g+h_k\).

The Gram convention for the individual-entry bound is a pair of local
PSD polynomial Grams, one for each prescribed block, each with its own
constant monomial. On this convention the first local Gram satisfies
\(Q_{00}=f(0)+c\). If \(d\) is the reduced denominator of this
entry and \(b_0\) that of \(f(0)\), the reduced denominator of
\(c\) divides \(b_0d\). A positive rational with denominator
\(b\) is at least \(1/b\). Combining these facts with equation
(16) gives exactly
\[
 \log_2d>2^{k+1}\log_2 M_k-2-\log_2b_0.
\]
No positive definiteness of the local polynomial Grams is needed.
This review does not extend that individual-entry assertion to a
single sparse matrix with only one shared constant coordinate.

For explicit unweighted block squares, the first local constant entry
is the sum of their squared constant coefficients. Its denominator
divides the product of their squared denominators. Consequently the
total coefficient length is \(\Omega(k2^k)\); an individual square
factor need not itself have that many bits. These bounds concern
ordinary explicit rational encodings and the stated block restriction.
They do not bound unrestricted certificates, arithmetic circuits, or
optimization time.

The distinction about joint Hessian Grams is also necessary and
correct for PSD Grams. A positive definite matrix on the full joint
basis would bound the Hessian biform below by a positive multiple of
\((1+\|X\|^2)\|\eta\|^2\). Fixing a direction in one block
and sending a different point block to infinity contradicts additive
separability. Thus every PSD Hessian Gram on that full joint basis is
singular, despite the uniform positive Hessian lower bound. The note
does not claim otherwise or claim a polynomial-size strong-convexity
upgrade for the exponential-degree power-basis realization.

The targeted check retained for this review is
[check_strongly_sos_convex_block_splitting_review.py](check_strongly_sos_convex_block_splitting_review.py).
It independently differentiates the extension polynomial and compares
the result with the displayed Gram in dimensions two, five, and nine.
It checks exact positive LDL pivots for one rational example using the
prescribed choice of \(\epsilon\), and checks the actual affine
inverse, the quintic lifted point, and the Hessian chain rule through
the nonzero translation. The command actually run was

```text
python research-20260927/check_strongly_sos_convex_block_splitting_review.py
```

All checks passed. A final inline `python - <<'PY'` document check also
passed the typo correction, trailing whitespace, final newline, and
balanced math delimiters. The finite checks support the identities; the
general Schur bounds, certificate existence, and denominator lower
bound are justified by the arguments above. No project-wide tests,
CI inspection, or Lean verification were performed.
