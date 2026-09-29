# Fresh review of rational quadratic perturbation multipliers

Date: 2026-09-28. Status: the complete proof passed fresh adversarial
review after one clarification of the optional convexity input.

I independently reconstructed the
[multiplier theorem](rational-quadratic-perturbation-multipliers.md),
including its inhomogeneous terms, simultaneous targets, arbitrary
symmetric perturbations, bit bounds, rational-square conversion, and
optional convexity conclusion. No mathematical gap was found.

The original supplied data required a rational coercive quadratic
\(G\). I requested the same explicit input convention for the optional
positive definite Hessian Gram \(M\). The author incorporated that
clarification and I checked the revised paragraph. The construction
does not claim to discover either certificate from its mere existence.

## The zero identity

For one target, put \(b=XR\). The first three terms satisfy
\[
 b^{\mathsf T}Hb+R\ell^{\mathsf T}b+cR^2=GR^2.
\]
Writing \(R=X^{\mathsf T}TX+r^{\mathsf T}X+s\), the other
three terms satisfy
\[
 (XG)^{\mathsf T}Tb+Gr^{\mathsf T}b+sGR
 =GR(X^{\mathsf T}TX+r^{\mathsf T}X+s)=GR^2.
\]
Their difference is zero. The symmetric old block contributes
\(cR^2-sGR\), and twice the cross block contributes
\(R\ell^{\mathsf T}b-(XG)^{\mathsf T}Tb-Gr^{\mathsf T}b\).
Thus both factors of one half and all signs in equation (7) are
correct. Summing introduces no cross terms between different lower
blocks, giving \(I_s\otimes H\).

The columns representing \(X_jG\) exist because the hypothesis places
\(G\) in the constant rational span of the baseline factors. Membership
of \(G\) only in \(W\) would not by itself justify that step.

## Positivity and arbitrary perturbations

The entrywise absolute sum bounds \(\|A\|_{\rm op}\), so the
chosen \(\varepsilon\) gives \(I+\varepsilon A\succeq I/2\).
The determinant-to-trace bound gives \(H\succeq\eta I\),
including when \(n=1\). Consequently the Schur complement is at least
\[
 (\varepsilon\eta-2\varepsilon^2\|C\|_F^2)I
 \succeq\varepsilon\eta I/2\succ0.
\]
This proves positivity of the full ordinary coefficient matrix.
Dependence or zero entries in the polynomial vector do not contradict
that matrix statement. Constant, linear, repeated, and zero targets
are allowed when they satisfy the stated membership condition.

For arbitrary symmetric \(J\), the upper block of \(D_J\)
evaluates to \(R^{\mathsf T}JR\). Its lower block evaluates to
\(\|X\|^2R^{\mathsf T}JR\), since the target-major ordering
requires \(J\otimes I_n\). Equation (13) is therefore correct.
The maximum absolute row sum bounds the operator norm of a symmetric
matrix, even if \(J\) is indefinite. The separate determinant bound
on \(Q_\varepsilon\) then proves
\(\lambda Q_\varepsilon-D_J\succeq I\) with exactly the threshold
in (15). The proof does not incorrectly infer a full-matrix eigenvalue
bound from the Schur complement alone.

Neither convexity, nonnegativity of \(G\), nor a common zero is
used in this argument. Only its leading matrix must be positive
definite. The theorem assumes \(n,m,s\ge1\); an empty target list
would be a separate trivial case.

## Exact construction and scope

Degree-three coefficient matching has at most \(\binom{n+3}{3}\)
rows and \(m(n+1)\) columns. Exact rational elimination finds the
required coordinates with polynomial bit length. The final Gram
dimension is \(m(n+1)+sn\). Determinants of matrices of this size,
the stated trace powers, rational comparisons, and the integer ceiling
all have polynomial bit complexity in the explicit rational input.
The supplied \(G\), \(J\), and optional \(M\) are part of that
input. This is not a claim about a compressed arithmetic-circuit
encoding of the data.

Positive definite rational LDL factorization has rational positive
pivots with polynomial bit length. For a pivot \(u/v>0\), the binary
expansion of \(uv\), divided by \(v^2\), uses polynomially many
rational squares. The resulting polynomial factors have degree at most
three and polynomial total encoding length. No integer factorization
or efficient four-square algorithm is assumed. The construction gives
an upper bound on square count, not a minimum.

Multiplying the SOS identity by \(h\) verifies the rational-function
formula (17). Its numerator degrees are at most four and its common
denominator is everywhere positive. The note correctly makes no
general claim that a quadratic denominator is necessary.

## Optional convexity conclusion

Every monomial of the Hessian biform of a rational quartic is a product
of two entries of \((u,X\otimes u)\): its degree in \(X\) is at
most two and its degree in \(u\) is two. A rational symmetric Hessian
Gram therefore exists and can be found by coefficient matching.
It need not be positive semidefinite.

Given the supplied positive definite baseline Gram \(M\), threshold
(18) gives \(\lambda M-B\succeq I\). In particular,
\[
 \nabla^2P(X)\succeq(1+\|X\|^2)I.
\]
At a common baseline zero all targets vanish by their affine
membership identities, and both \(P\) and its gradient vanish.
Strong convexity then makes that point the unique global minimizer
with value zero. The common-zero hypothesis is needed for this last
conclusion, not for the multiplier theorem.

## Targeted exact checks

The independent
[checker](check_quadratic_perturbation_multiplier_review.py) uses
\[
\begin{aligned}
 G&=2x^2+2xy+3y^2+5x-7y-11,\\
 q_2&=x^2-y-1,\qquad q_3=xy-x+2,\\
 R_1&=y^2+2x-1,\\
 R_2&=-4x^2+2xy+y^2+4y+7.
\end{aligned}
\]
Here \(q_1=G\), \(R_1=xq_3-yq_2+q_2\), and
\(R_2=xq_3-yq_2+2q_3-3q_2\). Thus the test exercises negative
\(c\), nonzero linear terms, constants of both signs, a mixed
quadratic term, and two simultaneous targets.

The checker tests both \(J=I_2\) and
\(J=\left(\begin{smallmatrix}2&3\\3&-5\end{smallmatrix}\right)\),
whose determinant is \(-19\). A separate one-variable case uses zero,
constant, and linear targets. It verifies the polynomial span identities,
zero Gram identity, exact LDL positivity, target-major Kronecker order,
scaling margin, multiplier identity, and binary rational-square
conversion.

The retained targeted command was:

~~~text
python research-20260927/check_quadratic_perturbation_multiplier_review.py
~~~

All three cases passed. Their Gram dimensions were 13, 13, and 7;
their scaling bit lengths were 80, 83, and 28. Two earlier inline
exact calculations also checked the two-target construction and its
indefinite perturbation before the note was frozen. These finite
calculations stress the formulas; the preceding proof review supports
the universal statement.

No project-wide verification, CI inspection, or Lean formalization was
performed. The optional convexity conclusion was checked algebraically.
A targeted inline Python document check also passed for this review
and its checker: two local links resolved, and math delimiters,
whitespace, control characters, and final newlines were valid.

## Prior-work limits

A limited literature check located neighboring work on
[facial reduction for exact SOS decompositions](https://arxiv.org/abs/1810.04215)
and on
[rational SOS representations and denominator degrees](https://ems.press/journals/jems/articles/13893).
Those sources concern established surrounding methods and questions.
This review does not establish publication priority or identify an
exact prior theorem with the present hypotheses and certificate bounds.
The note correctly leaves that assessment open.
