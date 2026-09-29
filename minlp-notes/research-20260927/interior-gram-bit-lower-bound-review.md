# Fresh review of the interior Gram bit lower bound

Date: 2026-09-28. Status: the complete proof passed fresh adversarial
review. No mathematical correction was required in the frozen note.

I independently checked the construction, strict feasibility, cube
moment bound, determinant bounds, and encoding conclusion in
[the theorem note](interior-gram-bit-lower-bound.md). The result is a
lower bound for positive definite rational Grams in the specified full
monomial basis. The same polynomials have short singular rational PSD
Grams and short rational SOS certificates. This distinction is necessary
and is stated correctly throughout the note.

## The small-value construction

I read the imported
[root-chain construction](strict-convex-quartic-rational-witness-lower-bound.md)
and checked its use here. For \(t\ge0\),
\((1+t)^3\ge1+3t\) gives
\(0<\delta_i\le\delta_{i-1}^2\), so
\(\delta_k\le M^{-2^k}\). The constants and rational gate boxes
have polynomial bit length; the construction does not print a rational
approximation with \(2^k\) digits.

The signal is specifically \(u=X_{k,1}-\kappa\), the last
first-power coordinate. The literal last retained coordinate is the
second power and would not give this estimate. The frozen note uses the
correct coordinate. Since \(1<\kappa<2\),
\[
 0<f_k(p)=\kappa^2\delta_k^2<4M^{-2^{k+1}}.
\]
The strict inequality is sufficient for the strict denominator bound
in equation (1).

The supplied Hessian Gram \(M_0\) has polynomial size. Its
determinant-to-trace bound and the integer ceiling in (4) preserve
polynomial bit complexity. The resulting Hessian Gram is at least
\(3I\). Because \(F\) vanishes only at \(p\), and \(u(p)>0\),
\(f_k=\lambda F+u^2\) is positive everywhere. Strong convexity
ensures that its minimum is attained, so that minimum is positive.

The signed-root baseline has exactly \(n+1\) displayed rational
square factors. Adding \(u^2\) gives a rational Gram of rank at
most \(n+2\). For \(n=2k\ge2\), this is strictly less than
\(D=\binom{n+2}{2}\). Its entries have polynomial bit length.
Binary expansion of the positive integer \(\lambda\) converts the
weighted expression into polynomially many rational squares. Thus the
short singular certificate claim also holds in the unweighted SOS
convention.

## Positive definite rational Grams exist

Strict positivity by itself would not justify strict feasibility of
the SOS Gram system. The note supplies the additional argument needed
here, and I reconstructed it from the rational Taylor identity.

At the minimizer, \(f>0\) and \(\nabla f=0\). Continuity and
density of rational points give a rational \(q\) with
\(c=f(q)-\|\nabla f(q)\|^2/2>0\). No bit bound for this
choice is assumed. With \(d=X-q\), subtracting
\(\|d\|^2/2\) subtracts \(\operatorname{diag}(I,0)\) from
the full Hessian Gram. The remaining rational PSD Gram permits rational
Taylor SOS integration.

For the full-span conclusion, split that remaining Gram as the explicit
block \(\operatorname{diag}(0,I_{n^2})\) plus a rational PSD
remainder. Each explicit lower-block square has the form
\((q_i d_j+t d_i d_j)^2\) in the Taylor integral. The identity
\[
 \int_0^1(1-t)(U+tV)^2\,dt
 =\frac12(U+V/3)^2+(V/6)^2
\]
therefore includes every factor \(d_i d_j/6\). These span the
homogeneous quadratic terms in \(d\). The completed affine squares
and the positive constant span the degree-at-most-one terms. Their
rational coefficient vectors span the full quadratic polynomial space,
so their Gram is positive definite. Rational translation back to \(X\)
preserves this property.

This establishes nonvacuity without asserting a short positive
definite Gram. It is consistent with the lower bound.

## The moment bound controls every feasible Gram

For independent coordinates uniform on \([-1,1]\), the centered
basis
\[
 1,\quad X_i,\quad X_i^2-1/3,\quad X_iX_j\ (i<j)
\]
is orthogonal. Its squared norms are respectively
\(1,1/3,4/45,1/9\). Thus equation (12) is exact.

Putting \(a'=a_0+\sum_i c_i/3\), Cauchy--Schwarz gives
\[
 a_0^2+\sum_i c_i^2
 \le2(a')^2+(1+2n/9)\sum_i c_i^2.
\]
Each coefficient on the right is bounded by \(15(n+1)\) times
the corresponding moment weight. The linear and mixed terms satisfy
the same comparison. Consequently
\(B\succeq I/[15(n+1)]\) for every relevant dimension.

For every real PSD Gram of \(f_k\),
\[
 \operatorname{tr}(QB)=\mathbb E[f_k(X)]\le\|f_k\|_1.
\]
The lower bound on \(B\) proves the trace and operator-norm bounds.
This argument applies to all feasible Grams and does not rely on their
rationality or on the displayed short Gram. The coefficient equations
and PSD constraint form a closed set, and the trace bound makes it
bounded. The Gram spectrahedron is therefore compact.

The algebraic evaluation point \(p\) need not lie in the cube. The
cube is used only to bound the coefficient matrix; the next Rayleigh
quotient estimate holds at any real point.

## Determinants and denominator length

The constant monomial gives \(\|z(p)\|^2\ge1\). Hence every
positive definite Gram satisfies
\(\lambda_{\min}(Q)\le f_k(p)\). All its other eigenvalues
are at most \(T_+\), proving
\[
 0<\det Q<4M^{-2^{k+1}}T_+^{D-1}.
\]

In a determinant permutation product, a diagonal entry appears at
most once, and an indexed off-diagonal entry can appear at most twice,
once in each orientation. Therefore
\(\prod_{i\le j}b_{ij}^2\) clears every term denominator.
It also clears their sum, regardless of common factors or
cancellation. For a positive definite rational matrix the resulting
integer is positive, so it is at least one. This proves equation (18).
Using squares for diagonal denominators is harmless overcounting.

Combining the strict upper bound with this lower bound gives exactly
\[
 \sum_{i\le j}\log_2 b_{ij}
 >2^k\log_2M-1-\frac{D-1}{2}\log_2T_+.
\]
There is no lost factor of two. Since \(\log_2M=(k+3)\log_2 1000\),
the positive term has order \(k2^k\). The subtracted term is
polynomial in \(k\): \(D=O(k^2)\), and the expanded coefficients
of \(f_k\) have polynomial count and bit length. The stated
asymptotic lower bound follows. The exact inequality remains valid
at small \(k\), where its right side can be weak.

Ordinary binary denominator lengths dominate the displayed logarithm
sum. This is an encoding bound in the fixed, unscaled monomial basis,
not a bound for compressed arithmetic circuits. A singular Gram has
zero determinant, so the positive-integer argument does not apply to
it. The short singular Gram is therefore fully compatible with the
theorem.

## Targeted verification and limits

I created and ran the small independent
[cube-moment checker](check_interior_gram_bit_lower_bound_review.py):

~~~text
python research-20260927/check_interior_gram_bit_lower_bound_review.py
~~~

For \(n=1,2,3,4\), it computes exact rational cube moments, checks
the centered diagonal weights, and verifies positive rational LDL
pivots for \(B-I/[15(n+1)]\). All four cases passed. These finite
examples check the constants and indexing; the coefficient comparison
above proves the general bound.

A targeted inline Python check passed for this review and its checker:
three local links resolved, and math delimiters, whitespace, control
characters, and final newlines were valid. The frozen main-note hash
was unchanged during this review.

The determinant, root-signal, strict-feasibility, and asymptotic
arguments were checked algebraically. No project-wide verification,
CI inspection, or Lean formalization was performed. This review does
not establish publication priority or a lower bound for arbitrary
PSD certificates, SOS certificates, approximate certificates, or
compressed descriptions.
