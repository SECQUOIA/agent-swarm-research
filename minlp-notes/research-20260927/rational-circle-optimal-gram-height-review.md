# Independent review of rational Gram and exposing-matrix height bounds

Date: 2026-09-28. Verdict: the stated consequences pass this review.
A classical SDP construction already implies the general phenomenon
described below; publication priority for the restricted quartic
realization remains unestablished.

This review covers the frozen
[height note](rational-circle-optimal-gram-height.md) with SHA-256
`a51334082cb33b854b7d29410bf6458749ce28510102edf0a899bca5229e371a`.
I did not derive the proposed consequence before receiving it for
review. I read the complete
[strict-Hessian moment argument](strict-hessian-moment-arithmetic.md),
reconstructed its rank and duality steps, and independently reviewed
the [rational optimizer construction](rational-convex-quartic-minimizer-height-review.md).

## The rank, moment, and face statements apply

Let \(p\) be the rational zero and let \(S\) be the number of
monomials of degree at most two. Translating the strictly positive
definite rational Hessian Gram to \(p\) preserves rationality.
Taylor integration produces a positive definite Gram on the centered
nonconstant monomials. To see strict positivity directly, integrate
the positive quadratic form on \((u,t\,u\otimes u)\) against
\(1-t\). On the corresponding formal coefficient vectors this is
positive for every nonzero vector; compressing the repeated quadratic
monomials preserves positive definiteness.

Translation back therefore produces a rational polynomial Gram of
rank \(S-1\), with kernel spanned by \(e=b(p)\). Every feasible
PSD Gram annihilates \(e\), since its polynomial evaluates to zero
at \(p\). These observations justify both maximality and the precise
kernel, rather than merely a lower bound on possible ranks.

For an optimal moment matrix, the trace pairing with this maximal-rank
Gram is zero. Positivity forces the moment matrix's range into
\(\mathbb R e\). Its normalized constant moment then forces it to
be \(ee^{\mathsf T}\). All degree-four moment coordinates occur
in that matrix, so the complete moment sequence is unique as well.

Likewise, a PSD exposing matrix orthogonal to every feasible Gram is
orthogonal to the maximal-rank Gram. Its range is contained in
\(\mathbb R e\), and a nonzero such matrix is exactly
\(c\,ee^{\mathsf T}\), \(c>0\). Evaluation at \(p\) belongs
to the span of the Gram coefficient equations, so this matrix supplies
an actual one-step facial reduction of the optimal-level feasibility
problem. The existence of a relative-interior Gram in the resulting
face gives singularity degree one.

There is no conflict with strict feasibility of the optimization
programs. Gaussian moments give a strictly positive moment matrix.
Adding a positive constant to the objective's minimum-level SOS
polynomial supplies a positive full polynomial Gram. The exhibited
optimal moment and maximal-rank Gram have complementary ranks.

## Recovering the optimizer bounds Gram entry heights

Partition the Gram as in the main note, with constant coordinate first:
\(Q=\bigl(\begin{smallmatrix}q_{00}&c^{\mathsf T}\\c&A\end{smallmatrix}\bigr)\).
The principal matrix \(A\) is positive definite. Indeed,
\(u^{\mathsf T}Au=0\) would imply that \((0,u)\) belongs to
the kernel of the PSD matrix \(Q\); that kernel is spanned by a
vector whose first coordinate is one. Thus \(u=0\).

Consequently the normalization of the kernel is recovered uniquely by
\(Aw=-c\). If every numerator and denominator is bounded by
\(2^B\), clearing each row's \(S\) denominators gives integer
entries bounded by \(2^{(S+1)B}\). This estimate is conservative
but valid. The integer determinant is nonzero and at most

\[
 (S-1)!\,2^{(S-1)(S+1)B}
\]

in absolute value. Each reduced coordinate denominator divides this
determinant by Cramer's rule. In particular,

\[
 2^k\log_2 5\leq\log_2((S-1)!)+(S^2-1)B.
\]

This verifies the stated bound and its
\(\Omega(2^k/N^4)\) per-entry consequence. The factorial term is
\(O(N^2\log N)\), negligible compared with \(2^k\).
Separate row scaling need not preserve symmetry or positivity; only
nonsingularity is used after that operation, so this presents no gap.

The total-length refinement is valid under ordinary full-entry
encoding. For one row, an integer-entry logarithmic bound is the sum
of the denominator bit lengths in that row plus its largest numerator
bit length. Summing over rows is bounded by the sum of all numerator
and denominator bit lengths used in the linear system. The determinant
expansion adds only \(\log_2((S-1)!)\). Encoding symmetric matrices
by only their upper triangle changes this conclusion by at most a
constant factor. Thus the polynomial divisor is needed for the
per-entry bound, but not for a total expanded matrix-length bound.

## Scaling cannot make the exposing matrix short

For any nonzero rational exposing matrix,
\(p_i=Z_{0i}/Z_{00}\), and \(Z_{00}>0\). If both entries have
numerators and denominators bounded by \(2^B\), the quotient has
a reduced denominator at most \(2^{2B}\). Comparing with the
terminal coordinate denominator \(5^{2^k}\) gives
\(B\geq2^{k-1}\log_2 5\). This argument includes arbitrary
positive rational rescaling; fixing a particular normalization of
the exposer is unnecessary.

The normalized optimal moment matrix directly contains the terminal
coordinate in a constant-versus-linear entry. Its denominator bound
therefore follows without any determinant or scaling argument.

## Scope and verification

The claim concerns every maximal-rank optimal Gram, every optimal
moment matrix, and every nonzero PSD matrix exposing all real feasible
Grams at the optimal level. It does not concern every feasible Gram.
The original construction supplies a polynomial-size rational SOS
Gram of rank at most \(N+1<S-1\), so a statement that all SOS
certificates must be long would be false here. The lower bound is
exponential in dimension and superpolynomial in the family's total
input size; it is not asserted to be exponential in that total size.
Arithmetic circuits can still describe these matrices compactly.

The Cramer and ratio arguments are elementary consequences of the
optimizer height. The significant feature of this example is their
coexistence with fixed quartic degree, bounded rational optimizer,
strict convexity certificates, and short lower-rank SOS certificates.
No claim that large exact SDP solutions or difficult facial reduction
are new phenomena is justified by these arguments.

After the initial audit, the author proposed a useful prior comparison,
which I independently checked. Homogenize the Khachiyan blocks in
[Zhang's Example 2.5.3](https://optimization-online.org/wp-content/uploads/2020/08/7992.pdf)
to obtain

\[
 \begin{pmatrix}x_1&2t\\2t&t\end{pmatrix}\succeq0,
 \qquad
 \begin{pmatrix}x_j&x_{j-1}\\x_{j-1}&t\end{pmatrix}\succeq0
 \quad(2\leq j\leq k).
\]

At \(t=0\), \(x_1=\cdots=x_{k-1}=0\), \(x_k=1\)
gives a short rank-one feasible block matrix. A full-rank feasible
matrix has \(t>0\), \(x_1/t>4\), and
\(x_j/t>(x_{j-1}/t)^2\), hence
\(x_k/t>2^{2^k}\). The same two-entry ratio argument forces
an exponentially long rational entry. This is an elementary inference
from the classical example, not a new prior theorem attributed to
Zhang. It rules out novelty for the unrestricted distinction between
short feasible certificates and long maximal-rank certificates.
The remaining potential contribution is the stated quartic realization
and its rational optimizer and moment geometry.

The independent
[exact checker](check_rational_circle_minimizer_review.py) additionally
constructs the Taylor polynomial Gram at \(k=1\), verifies its
polynomial identity, rank \(S-1\), and evaluation-vector kernel,
recovers the evaluation vector from its nonsingular principal system,
and checks the exposing-matrix ratio after a nontrivial rational
rescaling. These finite checks supplement the general proof and do
not establish the asymptotic bounds by themselves. No Lean,
project-wide, or CI verification is claimed.

The targeted command was
`python research-20260927/check_rational_circle_minimizer_review.py`.
An inline `python - <<'PY'` check passed local-link, math-delimiter,
whitespace, control-character, and final-newline checks on the two
review notes and their checker: three files and eight local links.
`git diff --check --` restricted to those same three paths also passed.
