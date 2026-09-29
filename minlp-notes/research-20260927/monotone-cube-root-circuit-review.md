# Independent review of monotone cube-root circuit quartics

Date: 2026-09-28. Scope: the complete
[circuit realization manuscript](monotone-cube-root-circuit-quartic.md),
including its two imported quantitative constructions. This reviewer
did not develop the circuit proof. A fresh narrow reviewer independently
checked the exposing quadratic, Jacobian, and gate approximation; a
separate child checked the interval and bit-complexity argument.

**Finding.** The construction is correct for \(k\ge1\). It gives
a rational globally strongly convex SOS quartic, together with a
positive definite rational Hessian Gram certificate, in polynomial
time in the explicitly encoded circuit. It does not require an
expanded field polynomial. The literal missing assumption \(k\ge1\)
was reported and corrected. The author also accepted the precision-input
and explicit Gram-rounding clarifications below. Neither changes the
claimed complexity for the internally generated precision requests.

This review does not establish novelty or arithmetic-comparison hardness.
The imported strong-convexity and Gram formulas were read and
independently reconstructed, rather than inferred from earlier positive
reviews.

## 1. Circuit values, residuals, and the Jacobian

For \(k\ge1\), the stated
\[
 A=2+\sum_i(c_i+\sum_{j<i}a_{ij})
\]
is rational, has polynomial encoding length, and satisfies \(A\ge3\).
Induction gives \(\xi_i\ge1\). If its predecessors are at most \(A\),
the radicand is at most \(A(c_i+\sum_j a_{ij})\le A^2\).
Its cube root is at most \(A^{2/3}\le A\). Thus
\[
 1\le\xi_i\le A,\qquad \|p\|_2\le nA^2,\qquad n=2k.
\]
All bit bounds here concern the rational upper bound, not the height
or algebraic degree of the individual gate values.

The residual equations \(q_i=r_i=0\) imply
\(Y_i=X_i^2\) and the sequential equations
\(X_i^3=c_i+\sum_{j<i}a_{ij}X_j\). Each real cubic map is
strictly increasing, so induction gives exactly one real solution.
The \(s_i\) residuals also vanish there by multiplying the cubic
identity by \(\xi_i\).

The \(q_i,r_i\) Jacobian is block lower triangular. Its diagonal
block at gate \(i\) has determinant \(3\xi_i^2\), giving
\(\det J=\prod_i3\xi_i^2\ge1\). Every entry is bounded by
\(2A^2\), including the predecessor derivatives \(-a_{ij}\).
Hence \(\|J\|_2\le\|J\|_F\le2nA^2=V\).
The product of its singular values and their upper bounds yield
\[
 \sigma_{\min}(J)\ge|\det J|V^{-(n-1)}
                    \ge V^{-(n-1)}=\nu.
 \]
The residual quadratic blocks have norms at most one: they are the
single-coordinate square block for \(q_i\) and the symmetric product
block of norm \(1/2\) for \(r_i\). The potentially larger quadratic
coefficients in \(s_i\) are not part of this residual norm hypothesis.

At \(k=0\), several original constants are undefined and a degree-four
polynomial in zero variables is impossible. Explicitly assuming
\(k\ge1\) is therefore necessary, rather than a cosmetic convention.

## 2. Cancellation and the weighted acyclic coupling

Put \(b_i^*=c_i+\sum_{j<i}a_{ij}\xi_j=\xi_i^3\).
After translating \(X_i=\xi_i+u_i\),
\(Y_i=\xi_i^2+v_i\), the predecessor contribution is
\(\sum_{j<i}a_{ij}u_j\). Substituting in
\(\xi_i^2q_i+s_i-\xi_i r_i\) cancels the constant and every
linear term. The surviving expression is exactly
\[
 \xi_i^2u_i^2+v_i^2-\xi_i u_iv_i
                          -u_i\sum_{j<i}a_{ij}u_j.
 \]
In particular the derivatives with respect to predecessor coordinates
cancel. A calculation that froze \(b_i\) would miss this condition.

With \(\rho=(8kA)^{-2}\) and \(\omega_i=\rho^{i-1}\),
scale the displacement pair of gate \(i\) by
\(\sqrt{\omega_i}\). These square roots are used only in the
proof, not in the rational output. The resulting local block has
determinant \(3\xi_i^2/4\) and trace \(\xi_i^2+1\), so its
smallest eigenvalue is at least \(3/8\).

For an edge \(j<i\), the scaled symmetric off-diagonal entry is
\(-a_{ij}\rho^{(i-j)/2}/2\). Each row has at most \(k-1\)
such entries, each of magnitude at most \(A\sqrt{\rho}/2\).
Its absolute row sum is therefore at most \(1/16\).
The symmetric coupling has operator norm at most this row bound.
The full scaled matrix is at least \(5I/16\), and the stated weaker
\(I/4\) bound follows. Scaling back gives
\[
 H_*\succeq(\omega_k/4)I.
 \]
The unscaled local norm bound \(2A^2\) and coupling row bound
\(kA/2\) also imply the stated \(W=3kA^2\).
The weights can be extremely small, but their reciprocal magnitude
logarithms are \(O(k\log(kA))\). Their exact rational encodings
have length polynomial in \(k\) and the encoding length of \(A\),
including its denominator.

## 3. Rational perturbation retains the exact zero

Replacing \(\xi_i,\xi_i^2\) by rational coefficients in the
linear combination of \(q_i,r_i,s_i\) does not approximate its
value at \(p\): every residual is exactly zero there. Thus
\(G(p)=0\) remains exact.

With coefficient errors at most \(\delta\), summing the \(2k\)
affected quadratic blocks gives
\(\|H-H_*\|\le2k\delta\). Summing the corresponding residual
gradients gives \(\|\ell\|\le2kV\delta\). The manuscript's
choice of \(\delta\) therefore implies
\[
 H\succeq\gamma I/2=mI,\qquad
 \|H\|\le W+\gamma/2\le W+1=L,\qquad
 \|\ell\|\le\varepsilon.
 \]
The squared gate approximation has the required accuracy because
\[
 |\widehat\xi_i^2-\xi_i^2|
 \le(2A+1)|\widehat\xi_i-\xi_i|
 \le3A\theta\le\delta
 \]
when \(\theta=\delta/(4A)\) and \(\delta\le1\).
No rationalization inside the generated number field is used.

## 4. Certified forward approximation

Clipping predecessor enclosures to \([1,A]\) preserves the true
gate values. Nonnegative coefficients make affine endpoint evaluation
an exact radicand enclosure, whose lower endpoint is at least one.
On this range, the real cube-root derivative is at most \(1/3\).
If \(D_{i-1}\) bounds all previous widths, the new width is at most
\[
 (A/3)D_{i-1}+2\eta.
 \]
Taking the maximum with the previous widths preserves the manuscript's
coarser recurrence \(D_i\le AD_{i-1}+2\eta\), since \(A\ge3\).
Thus
\[
 D_k\le2\eta\sum_{j=0}^{k-1}A^j
 \le2k\eta(A+1)^k\le\theta/2
 \]
for the stated choice of \(\eta\). This supplies rational
midpoint approximations of the requested accuracy.

A fixed dyadic mesh can be used at every gate. Each exact radicand
endpoint is then a sum of input rationals times dyadics, rather than
an expression inheriting the denominator of every previous bisection.
Its bit length is bounded by the total input coefficient length plus
the fixed mesh precision and a polynomial summation overhead. Rational
cubing and comparisons, and the polynomially many gate bisections,
therefore have polynomial bit complexity. There is no concealed
\(3^k\) representation cost.

For a general rational requested tolerance, its encoding length must
also be counted: an unnecessarily long fraction cannot be read in time
depending only on \(\log(1/\theta)\). Equivalently request a dyadic
precision \(2^{-P}\) with integer \(P\ge0\). The main construction
already generates polynomial-size rational tolerances, so this wording
qualification does not affect its theorem.

## 5. Strong convexity and the full Hessian Gram

There are \(n=2k\) residuals, exactly the count used by the imported
small-square estimate. They satisfy all its quantitative hypotheses:
quadratic blocks bounded by one, gradient bound \(V\), Jacobian
gap \(\nu\), positive quadratic part \(H\succeq mI\), and
gradient error at most \(\varepsilon\). The manuscript's last
epsilon denominator has the additional factor \(n\) needed for
the full Gram certificate. It is therefore also sufficient for the
ordinary global Hessian estimate.

For \(F_0=G^2+\varepsilon\sum r_j^2\), the homogeneous Hessian
bounds give
\[
 \nabla^2F_0(p+z)
 \succeq
 \bigl(2\varepsilon\nu^2-12\varepsilon(L+nV)\|z\|
                         +2m^2\|z\|^2\bigr)I
 \succeq\tfrac32\varepsilon\nu^2I.
 \]
Scaling by \(1/(\varepsilon\nu^2)\) proves the claimed stronger
\(3I/2\) bound. All factors in the displayed SOS are rational
because \(\varepsilon=t^2\) is chosen as a dyadic square.
There are exactly \(n+1=2k+1\) factors.

The imported block Gram has
\[
 C\succeq2\varepsilon\nu^2I,\qquad
 Q_{\rm G}\succeq2m^2I,\qquad
 \|D\|\le6\sqrt n\,\varepsilon(L+nV).
 \]
Its Schur complement is at least
\(3\varepsilon\nu^2I/2\). This is positive definiteness on the
full \(n+n^2\)-dimensional Gram space, not merely positivity on
vectors of tensor form. The term \(T_j\otimes T_j\) is allowed
to be indefinite and its negative norm contribution is retained.

The coordinate shift and the explicit spectral-gap formula in
[the Gram note, equation (14)](sos-convex-quartic-realization.md)
apply with \(K=nA^2\). Every bound entering that positive rational
gap \(\mu\), including its reciprocal, has polynomial bit length.
The applicability of this calculation depends on the translated
quadratic identities, not on how the algebraic point was encoded.

## 6. Explicit multivariate Gram precision

The following gives a direct implementation of the manuscript's
rounding paragraph. Freeze the rational polynomials \(G,r_j\)
already constructed, and let \(p\) now denote a formal center.
Their quadratic blocks \(H,T_j\) are constant rational matrices;
their translated gradients are affine in \(p\).

In the block Gram formula, the constant block is degree at most two
in \(p\), the cross block has degree at most one, and the quadratic
block is constant. The triangular shift
\[
 S_p=\begin{pmatrix}I&0\\-p\otimes I&I\end{pmatrix}
 \]
therefore leaves every entry of
\(M_x(p)=S_p^TM(p)S_p\) of degree at most two in \(p\).
It does not create degree four: the two shift factors multiply only
the constant lower-right block when both contribute a factor of \(p\).

Let \(N_{\rm G}=n+n^2\), let \(R=nA^2+1\), and compute a
rational \(C_1\ge1\) bounding the coefficient absolute sum of
each entry polynomial of \(M_x\). These degree-two polynomials
can be formed explicitly; their number of monomials and coefficient
bit lengths are polynomial. Hence \(C_1\) has polynomial bit length.
On the center box of radius \(R\), each coordinate derivative is
bounded in absolute value by \(2C_1R\).

If \(\|\widehat p-p\|_\infty\le\zeta\le1\), the segment between
the points lies in this box and
\[
 \|M_x(\widehat p)-M_x(p)\|_F
                      \le2N_{\rm G}n C_1R\,\zeta.
 \]
Choose, for example,
\[
 \zeta\le\min\{1,\mu/(16N_{\rm G}nC_1R)\},
 \qquad
 |\widehat\xi_i-\xi_i|\le\zeta/(2A+1).
 \]
Then both coordinates \(\xi_i,\xi_i^2\) have error at most
\(\zeta\), and the Frobenius error is at most \(\mu/8<\mu/4\).
Section 4 obtains this accuracy with polynomially many bits.
Exact evaluation at \(\widehat p\) gives a rational symmetric
matrix. The approximating point need not satisfy the circuit equations.
Only the true point must satisfy them for \(M_x(p)\) to represent
the exact Hessian.

Apply the rational orthogonal projection onto every coefficient equation
of the Hessian biform, including its zero coefficients. The disjoint
supports of the monomial coefficient matrices make this projection
nonexpansive in Frobenius norm, and it fixes \(M_x(p)\). The
result is therefore an exact rational Hessian Gram with eigenvalue
at least \(3\mu/4\). Positive scaling gives the certificate for
the normalized \(F\).

There are \(O(n^4)\) matrix entries, and all coefficient equations
and rational arithmetic have polynomial size. A rational
\(LDL^T\) decomposition verifies the certificate without an
algebraic field, an SDP oracle, integer factorization, or a rational
Cholesky square root.

## 7. Encoding, arithmetic consequences, and limits

The input counts the explicitly listed rational circuit coefficients
and gates. Powers such as \(\rho^{k-1}\), \(V^{-(n-1)}\), and
the epsilon bound have polynomial exact rational encodings. Their
reciprocal magnitude logarithms are \(O(k\log(kA))\), up to
polynomial factors. These are different assertions: a rational \(A\)
of small magnitude can still have a large denominator. Such
denominator lengths already contribute to the circuit input.
The quartic has at most \(O(k^4)\) monomials, and the Gram has
polynomial dimension, so the actual outputs can be printed within
the claimed bound.

The field degree upper bound \(3^k\) follows from the tower of
cubic extensions. It can be attained with independent gates
\(\xi_i^3=p_i\) for distinct rational primes: the elementary
field argument in
[the earlier cube-root review, Section 2](quartic-span-boundary-review.md#2-exact-algebraic-degree)
proves degree \(3^k\). Thus dense-field expansion can indeed be
exponential in this input. The present algorithm avoids it.

Every real embedding of the generated field preserves the rational
gate equations and hence fixes the unique real solution. The circuit
class consequently satisfies the relevant one-real-embedding condition.
This observation does not expand the allowed circuit syntax.

The exact comparison reduction is valid for a weak comparison:
intersect \(F\le0\) with the requested rational affine inequality.
Its only possible feasible point is the circuit point. A rational
containing box has polynomial bit length. A strict comparison requires
a strict row or the appropriate complementary decision; these logical
conventions should be stated when a benchmark problem is specified.
No separation bound for the sign of a general small circuit linear
form, NP-hardness result, or lower bound on exact decision follows
from the construction.

The present review checks the claimed construction and the scope of
these consequences. It does not conduct a new publication-priority
search. The manuscript correctly leaves that question to a separate
comparison with existing arithmetic-circuit and convex-polynomial work.

## 8. Targeted verification

An inline Python command using exact SymPy arithmetic constructed the
coupled two-gate circuit
\[
 \xi_1^3=1,\qquad \xi_2^3=7+\xi_1,\qquad
                     p=(1,1,2,4).
 \]
With the manuscript's bounds it selected
\(\varepsilon=2^{-128}\). The check verified:

- the complete \(20\times20\) shifted Hessian Gram identity;
- exact rational \(LDL^T\) positive definiteness on its full space;
- degree at most two in every formal center entry polynomial;
- exact correction of all monomial coefficients by the stated projection.

All assertions passed. This rational example challenges the coupled
Gram algebra and rounding interface; it does not establish the general
irrational arithmetic theorem. The universal inequalities and bit
bounds are supplied by the proof above. A final targeted document check
passed for this review's three local links, paired math delimiters,
whitespace, control characters, and final newline. The author then
incorporated the tolerance and explicit multivariate precision text;
this reviewer read those final changes and confirmed their bounds.
No unchanged project-wide tests, CI inspection, or Lean verification
were performed.
