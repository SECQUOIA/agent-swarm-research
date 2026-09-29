# Fresh review of the rational block-splitting obstruction

Date: 2026-09-28. Verdict: the new mathematical construction passes
independent adversarial review. The joint SOS lift, failure of rational
block splitting, inherited coefficient-field obstruction, and the
nonvacuous rational bit-cost lower bound are correct. The final
manuscript incorporates both requested clarifications: the precise
Schur complement and the constant-coordinate convention for separated
Grams. No unresolved mathematical finding remains.
Publication priority is not assessed by this review.

The initially reviewed frozen manuscript is
[rational-block-sos-splitting-obstruction.md](rational-block-sos-splitting-obstruction.md),
with SHA-256
`358a88833892612da6b6f3eafe0d5f6cb8ac74ae1c84e0366527e62ca4345bf6`.
I had no role in constructing the lift. A further fresh reader checked
the rational bit-cost argument and its encoding scope.

The hypotheses and applications agree with the imported reviewed
results. The tower quartic has the required rational positive definite
full Hessian Gram, unique zero, and field characterization. Its
\(k=1\) zero is \((a,a^2,a^3)\), not the differently parametrized
zero of the earlier small explicit quartic. The positive auxiliary
quartic supplies the stated tiny attained minimum and short rational
SOS. The rational-center Taylor lemma applies to any supplied positive
definite rational full Hessian Gram; it does not require an unchanged
unit lower bound. This review checks these applications rather than
re-proving the complete imported constructions or their literature
claims.

For the new lift, cubic gradient monomials are replaced exactly as
stated. If a monomial has sorted indices \(i,j,k\), replacing
\(y_iy_j\) by \(z_{ij}\) changes it by
\(y_k(y_iy_j-z_{ij})\). Summing the changes gives
\(e=E(y)r\), where \(E\) is homogeneous linear. Terms of degree
at most two stay unchanged. Thus \(a\) has degree at most two,
\(r\) has degree at most two, and \(e^{\mathsf T}d\) is a
bilinear expression in \(r\) and the \(y\otimes d\) entries of
\(w=(d,y\otimes d,d\otimes d)\). The matrix \(D\) in the
manuscript therefore exists over \(\mathbb Q\) with the stated
columns. No cubic polynomial factor is squared in the certificate.

The Taylor matrix is correct. Integrating the constant, linear, and
quadratic powers of the interpolation parameter gives respectively
\(1/2,1/6,1/12\), yielding the displayed matrix \(M\). The
inequality \(A\succeq\rho I\) transfers through the integral
to the stated lower bound for \(M\). Its scalar two-by-two moment
block has determinant \(1/72\). With \(\mu=\rho/2\), subtracting
\((\mu/2)\|d\|^2\) leaves a first-block margin \(\rho/4\)
and unchanged positive tensor blocks. Therefore \(N\succ0\)
as an ordinary rational matrix. The duplicated entries of
\(d\otimes d\) do not invalidate this matrix assertion.

The second determinant bound gives \(N\succeq\delta I\).
For the stated integer \(\lambda\), the relevant Schur complement
is explicitly
\[
 \lambda I_m-\tfrac14DN^{-1}D^{\mathsf T}
 \succeq
 \left(\lambda-\frac{\|D\|_F^2}{4\delta}\right)I_m
 \succeq I_m.
\]
Hence \(K\succ0\). This formula is the intended meaning of the
manuscript's phrase "Schur complement in the lower block"; spelling
it out would prevent confusion with the complement of \(\lambda I_m\).

All signs and scalar factors in the joint identity check. The first
Gram contributes
\[
 T_f-\frac\mu2\|d\|^2+e^{\mathsf T}d+\lambda\|r\|^2,
\]
and the completed square contributes
\(\mu\|d\|^2/2+a^{\mathsf T}d+\|a\|^2/(2\mu)\).
Using \(e+a=\nabla f(y)\) gives exactly \(f(x)+g(y,z)\).
Every factor has degree at most two. Rational LDL factorization gives
rational factors with positive rational weights. Binary expansion of
the integer product of a weight's numerator and denominator expresses
that weight as polynomially many rational squares, with polynomial
total coefficient length. This avoids relying on an efficient
four-square or integer-factorization algorithm.

The bit-complexity assertion for the lift is justified under the
specified expanded input convention. Matrix dimensions are polynomial
in \(n\). Determinants, trace powers, rational inversion or LDL,
coefficient matching, and the final ceiling all have polynomial output
bit length and can be computed in polynomial time at those dimensions.
The lift does not calculate the minimizer or its algebraic field.

The minimum assertions are independent of rational specialization.
Since (15) is a real nonnegative identity, substituting the real point
\(x=p\) proves \(g\ge0\). At
\((y,z)=(p,(p_ip_j))\), the residuals vanish and
\(a=\nabla f(p)=0\), so \(g=0\). Rationality of \(p\) is
unnecessary for this nonnegativity argument. These facts establish the
zero minima needed for the separation obstruction.

If two sums of block-supported squares represent \(f+g\), their
differences from the corresponding blocks are opposite constants:
a polynomial depending only on \(x\) cannot equal one depending
only on \((y,z)\) unless both are constant. For rational factors,
this constant \(t\) is rational. The two attained zero minima force
\(t=0\), contradicting the imported non-rational-SOS theorem for
\(f\). The same reasoning applies to two rational local PSD Grams,
using the imported Gram obstruction. Over the reals, specialization
and the Taylor certificate give the two block SOS decompositions, as
claimed.

The field extension in Section 4 uses precisely the same zero-shift
argument over each real subfield \(E\). For necessity, the first
local Gram or SOS is a certificate of \(f_k\) over \(E\), so the
imported field characterization applies. This Gram argument does not
assume that every positive scalar of an arbitrary real subfield is a
sum of squares in that field. For sufficiency, \(a_k\in E\)
puts every coordinate of \(p_k\) in \(E\); specializing the
rational joint SOS at \(p_k\) then supplies the second block SOS
over \(E\). The individual-coefficient lemma applies to the finite
list of algebraic coefficients of a separated certificate.

Here the exact total variable count is
\[
 2(3k)+\frac{3k(3k+1)}2=\frac{9k^2+15k}{2}.
\]
Thus the bound \(5^k\) is \(5^{\Theta(\sqrt N)}\) when
expressed in this lifted total variable count \(N\). The manuscript
states that distinction correctly.

The strictly positive family is nonvacuous. Since \(g\) and
\(h_k\) use independent variables and attain their minima,
\(\min(g+h_k)=m_k>0\). Choose rational \(0<t<m_k\).
The shifted first block \(f+t\) is strictly positive and retains
its full positive definite rational Hessian Gram, so the imported
Taylor lemma applies. Continuity at the zero of \(f\) and density
of rational points give rational \(q\) with
\(s=f(q)<m_k-t\). Specializing the joint rational SOS at this
rational point gives \(g+s\) as a rational SOS. The polynomial
\(h_k-t-s\) is strictly positive with the same supplied Hessian
Gram as \(h_k\), and is therefore rational SOS as well. This proves
existence of a separated certificate. The proof makes no unsupported
inference from positivity alone to polynomial SOS and does not claim
short coefficients for these choices.

For every separated rational certificate, nonnegativity forces
\(0\le t\le m_k\), and \(t=0\) is excluded by the fixed
first block. If \(t=a/b\) is reduced and positive, then
\(1/b\le t<4M_k^{-2^{k+1}}\). This proves the strict bound
\(\log_2b>2^{k+1}\log_2M_k-2\).

Equations (24) and (25) are correct for the following explicit
encoding conventions. For two local ordinary-monomial Gram matrices,
each includes its own constant monomial, and the first has
\(Q_{00}=f(0)+t\). If \(\nu=\operatorname{den}(f(0))\),
then \(b\) divides \(\nu\operatorname{den}(Q_{00})\).
For an expanded unweighted separated SOS, writing
\(c_i=u_i(0)\) gives
\[
 t=\sum_i c_i^2-f(0),\qquad
 b\mid\nu\prod_i\operatorname{den}(c_i)^2.
\]
These are divisibility statements even when cancellation occurs.
Consequently the lower bound applies to coefficients actually present
in the certificate, whether or not the shift is separately printed.
It is exponential in the positive family's total variable count
\(2k+12\) and superpolynomial in its constructed input size. It is
not asserted to be exponential in total input bits or to apply to
compressed arithmetic-circuit coefficient descriptions.

A one-sentence definition of the two-local-Gram convention is
recommended. A single sparse PSD matrix with one shared constant
coordinate is a different encoding: its global constant entry is
\(P_k(0)\), so equation (24) is not the proof for that matrix.
The same asymptotic bound nevertheless extends to that encoding, as
the fresh bit-cost reader established and I checked below.

Suppose mixed-monomial rows are zero and the two sets of nonconstant
block monomials have zero cross entries, giving the arrowhead form
\[
 Q=\begin{pmatrix}
 a&u^{\mathsf T}&v^{\mathsf T}\\
 u&B&0\\v&0&C
 \end{pmatrix}\succeq0.
\]
The first nonconstant block has at most nine ordinary quadratic
monomials. Let \(r=\operatorname{rank}B\le9\), select an
invertible principal submatrix \(B_{II}\), and put
\(\alpha=u_I^{\mathsf T}B_{II}^{-1}u_I\).
Positive semidefiniteness implies \(u\in\operatorname{range}B\).
Schur complementation splits \(Q\) into rational local PSD Grams
with constants \(\alpha\) and \(a-\alpha\). Thus
\(t=\alpha-f(0)\) again lies in \((0,m_k]\). The case \(r=0\)
cannot represent the nonconstant quartic first block.

Because \(t<1\), the reviewed cube-moment norm bound puts every
entry of the first local Gram below the fixed bound
\(T=60(\|f\|_1+1)\) in absolute value. Let \(D_0\) be the
product of the reduced denominators of \(B_{II}\)'s upper triangle
and \(u_I\). These are at most 54 entries of the original sparse
Gram. Clearing their denominators shows that the denominator of
\(\alpha\) divides
\(D_0\det(D_0B_{II})\), a positive integer at most
\(D_0^{r+1}T^r\). Consequently, if \(S\) is their total
denominator length,
\[
 S>\frac{2^{k+1}\log_2M_k-2-\log_2\nu-9\log_2T}{10}
   =\Omega(k2^k).
\]
This optional extension needs the stated sparse-matrix structure;
arbitrary joint Grams remain short. Arbitrary polynomial basis changes
must have their own coefficients counted if this encoding question is
reformulated.

Finally, the absence of a full positive definite joint Hessian Gram
for a nontrivial block-separable polynomial is correctly explained.
Fix a nonzero direction supported in one block and fix that block's
variables. Its Hessian value is independent of the other block. A
positive definite full joint Hessian Gram would lower-bound it by a
positive multiple of the squared full Hessian-basis norm, which grows
without bound as the other block tends to infinity. The stated scope
therefore avoids extending the construction into an incompatible full
Hessian certificate class.

The targeted command actually run was
`python3 /tmp/check_rational_block_lift_review.py`.
It independently used \(f(X)=\|X\|^2+\|X\|^4\) in dimensions
one and two, with explicit rational full Hessian Grams. Both cases
passed the Hessian identity, the monomial lifting and error identities,
the Taylor and completed-square identities, quartic degree, and the
zero specialization. All four and thirteen leading principal minors
of the respective joint matrices \(K\) were positive. These checks
test constants and tensor indexing; the proof above checks the
all-dimension argument and the separate imported obstruction. The
frozen manuscript hash was also checked with `sha256sum`. No
project-wide verification, CI inspection, or new literature-priority
claim was made.

The final reconciled manuscript has SHA-256
`c2bd18543ec2aba8bf84e65a0c42a5d7c59b17f5870bc0a140c5fa3380d909c2`.
I verified that hash with `sha256sum` and reread the full revised
manuscript. It now displays the Schur complement after eliminating
\(N\) and explicitly defines separated Grams as two local matrices,
each with its own constant entry. Both clarifications are correct and
resolve the review comments. The optional shared-constant arrowhead
extension remains in this review; it is not needed for the final
manuscript's stated convention. The existing dimension-one and
dimension-two exact checks were not repeated because no tested
identity or construction changed.
