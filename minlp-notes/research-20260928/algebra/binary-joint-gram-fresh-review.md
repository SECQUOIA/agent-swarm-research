# Fresh review of the full joint Hessian Gram refinement

Date: 2026-09-28. Reviewer: `/root/close_binary_gram_review`.

The full-Gram refinement in
[the binary extraction note](binary-extraction-known-value.md) passes
this fresh noncontributor review. I did not propose its polynomial,
Gram arrangement, or bounds. I independently reconstructed the proof
from the displayed polynomial, then compared it with the proposed
certificate and [the earlier review](binary-extraction-review.md).
No mathematical correction is needed.

The result is conditional on the supplied interface of the
[rational-optimizer coordinate theorem](../../research-20260927/rational-optimizer-posslp-coordinate-comparison.md).
I read that theorem and checked the original-coordinate Hessian basis
against its realization dependencies. This review does not claim a new
independent verification of the entire quaternion compiler or its
quartic realization.

## Certificate reconstruction

Let the original quartic have Hessian Gram \(Q\succ0\) on

\[
             w=(v,x\otimes v),\qquad d=N+N^2,
\]

and put \(\rho=\det(Q)/(\operatorname{tr}Q)^{d-1}\). The spectral
bound \(Q\succeq\rho I\) follows by writing the determinant as the
smallest eigenvalue times the product of the remaining eigenvalues;
each remaining eigenvalue is at most the trace. Here \(N\geq1\),
as required by the designated coordinate.

Choose the explicit rational number

\[
       \epsilon=\min\{\rho/4,1/(100N)\}>0
\]

and write \(t=z-1/2\). The added polynomial is

\[
 t^2+\epsilon(t^2-1/4)\|x\|^2
                      +\tfrac14(t^2-1/4)^2.
\]

Its second derivative in the direction \((v,s)\) is exactly

\[
 -\tfrac\epsilon2\|v\|^2+2\epsilon t^2\|v\|^2
 +2\epsilon\|x\|^2s^2+8\epsilon t(x^Tv)s
 +\tfrac74s^2+3t^2s^2.                                      \tag{1}
\]

In particular, the mixed term has coefficient \(8\epsilon\),
and the constant coefficient of \(s^2\) is \(7/4\).
These are the two places where a factor or translation error could
have invalidated the proposed certificate.

The ordered vector

\[
                    (w,s,tv,xs,ts)                         \tag{2}
\]

contains every direction coordinate and every coordinate-times-direction
monomial for the \(N+1\) joint variables, exactly once. Its length is

\[
           N+N^2+1+N+N+1=(N+1)(N+2).
\]

Thus this is a full Hessian basis, not a reduced list omitting mixed
monomials. Let \(E\) be the identity on the \(v\) part of \(w\),
and zero elsewhere. Let \(d_0\) be zero on \(v\) and the vectorized
identity on \(x\otimes v\), so \(d_0^Tw=x^Tv\) and
\(\|d_0\|^2=N\). The symmetric Gram is

\[
 G=\begin{pmatrix}
 Q-\epsilon E/2&0&0&0&4\epsilon d_0\\
 0&7/4&0&0&0\\
 0&0&2\epsilon I&0&0\\
 0&0&0&2\epsilon I&0\\
 4\epsilon d_0^T&0&0&0&3
 \end{pmatrix}.                                             \tag{3}
\]

Multiplication of (3) by (2) reproduces (1) plus the original Hessian
biform. No property of \(Q\) beyond its supplied Hessian identity and
positive definiteness is used.

For \(A=Q-\epsilon E/2\), the bound

\[
       A\succeq(\rho-\epsilon/2)I\succeq\rho I/2
\]

is valid. With \(b=4\epsilon d_0\),

\[
 b^TA^{-1}b\leq32\epsilon^2N/\rho
               \leq8\epsilon N\leq2/25<3.
\]

The Schur complement of \(A\) in the coupled first and last blocks is
strictly positive. The other blocks are positive definite because
\(\epsilon>0\). Hence \(G\succ0\).

Replacing \(tv\) by \(zv-v/2\) and \(ts\) by \(zs-s/2\) is an
invertible rational transformation of the full basis. The transformed
Gram is a rational congruence of \(G\), so it remains positive definite
on the original-coordinate full basis. This proves the claimed full
certificate, and therefore global strong SOS-convexity with some positive
rational modulus. The particular modulus \(3/2\) is not preserved by
this argument and is correctly absent from the refinement's promises.

## Exact encoding, positivity, and certificate size

Both correction terms vanish identically at \(z=0\) and \(z=1\), for
every \(x\). Consequently all feasible mixed-integer objective values
are unchanged. Equality with \(1/4\) still forces \(x=p\); the nonzero
coordinate \(p_j\in[-1,1]\) belongs to exactly one of the intervals
\([-1,0]\) and \([0,1]\). The optimizer is therefore uniquely
\((p,\mathbf1[p_j>0])\). The constraint matrix is unchanged and its
continuous part has rank exactly one. The feasible region is not
asserted bounded.

The global positivity claim is also correct. Strong convexity of the
original \(F\), its zero at \(p\), and \(\|p\|^2\leq N\) give

\[
 \begin{aligned}
 F(x)-\tfrac\epsilon4\|x\|^2
 &\geq(\tfrac34-\tfrac\epsilon2)\|x-p\|^2
                              -\tfrac\epsilon2\|p\|^2\\
 &\geq-\epsilon N/2.
 \end{aligned}
\]

The discarded quadratic coefficient is positive since
\(\epsilon\leq1/(100N)\leq1/100\). For \(u=t^2\geq0\),

\[
        u+\tfrac14(u-1/4)^2
          =\tfrac14u^2+\tfrac78u+\tfrac1{64}
          \geq\tfrac1{64}.
\]

Discarding the additional nonnegative term
\(\epsilon t^2\|x\|^2\) proves the stated uniform bound

\[
            \widehat H\geq1/64-\epsilon N/2
                          \geq17/1600>0.
\]

The polynomial has degree exactly four: its \(z^4\) coefficient is
\(1/4\), independently of the original quartic. The determinants,
traces, rational power with exponent \(d-1\), and the minimum defining
\(\epsilon\) all have polynomial bit length and are computable by
exact rational arithmetic in polynomial time in the explicit input
matrix. The Gram has \((N+1)(N+2)\) rows; its construction and rational
congruence therefore also have polynomial size and time bounds.
No coordinate of \(p\) is needed to construct it.

An exact rational \(LDL^T\) decomposition verifies the certificate and
gives positive rational weights multiplying squares of rational
polynomials. A rational Gram certificate does not require square roots
of those weights to be rational. If unweighted rational squares are
the required Hessian-certificate format, a positive rational weight
\(a/b=ab/b^2\) can be expanded using the binary digits of the positive
integer \(ab\): an even power of two is one integer square, and an odd
power is two equal integer squares. This uses polynomially many
rational squares. This observation concerns the Hessian certificate;
it does not supply an objective SOS decomposition.

## Exact checks and scope

I ran a targeted inline command, `python3 -B - <<'PY' ... PY`, with
SymPy exact arithmetic. It completed successfully and reported:

```text
PASS: 4 symbolic Hessian identities and full-basis counts; 3 exact rational Schur, centered/original Gram LDL, and positivity checks.
```

The symbolic checks differentiated the correction polynomial directly
in dimensions \(N=1,2,3,5\) and compared every coefficient with (1).
The rational matrix checks used \(N=1,2,3\),
\(p_i=(-1)^i/3\), and \(F(x)=\|x-p\|^2+\|x-p\|^4\).
For this test family the centered source Gram is
\(\operatorname{diag}(2I,4I+8\operatorname{vec}(I)
\operatorname{vec}(I)^T)\), translated exactly to the original
coordinates. Each check constructed (3) with the stated rational
\(\epsilon\), checked the Schur inequalities, and verified strictly
positive exact \(LDL^T\) pivots before and after the joint translation.
It also checked the \(17/1600\) positivity bound. These finite checks
guard against algebraic and indexing errors; the preceding symbolic
argument establishes the arbitrary-dimensional claim.

The established conclusion is a polynomial-time reduction proving
PosSLP-hardness of the optimal binary decision with one binary variable,
continuous constraint rank one, known optimum \(1/4\), a rational bounded
optimizer, and an explicitly supplied rational positive definite full
Hessian Gram. It is not an unconditional lower bound against polynomial
time, an NP-hardness result, or a guarantee about approximate decisions
without a branch-gap promise. A short objective SOS certificate and
the original \(3/2\) modulus are not part of this refinement.

The original note already treats this as an elementary consequence of
the coordinate theorem and makes no independent priority claim. This
review does not enlarge that assessment or establish novelty. The
Hessian-certificate refinement has no unresolved proof obligation
within its stated scope.

A separate targeted `python3 -B` inline documentation check passed this
file's three local links, final newline, trailing whitespace, control
characters, and balanced inline/display math delimiters. The command
`git diff --check -- research-20260928/algebra/binary-joint-gram-fresh-review.md`
also returned successfully; because the review was new and untracked,
the explicit file-content check supplies the whitespace validation.
I did not run project-wide verification, inspect CI, or formalize this
proof in Lean.
