# Additional audit of rational SOS-convexity without rational SOS

Date: 2026-09-28. Status: the explicit example and the positive-constant
lemma pass this audit. No publication-priority conclusion is made.

This review checks the [integrated construction](rational-sos-convex-descent.md)
and its [exact checker](check_rational_sos_convex_descent.py).
The reviewer did not construct the concrete rational Hessian certificate.
During the investigation the reviewer independently suggested a reflected
version of the mixed cubic perturbation, so this is not a wholly
independent discovery of the perturbation mechanism. The separate
[adversarial review](rational-sos-convex-descent-review.md) provides an
additional proof check.

## Exact Hessian certificate and its consequence

For a quadratic written at a rational center as
\(q(c+u)=d+b^{\mathsf T}u+u^{\mathsf T}Tu\), direct differentiation gives

\[
 \nabla^2(q^2)=2\nabla q\nabla q^{\mathsf T}+4qT.
\]

Expanding this expression verifies the three Gram blocks in the main
note, including the necessary constant term \(4dT\). The tensor order
is \((k,j)\mapsto u_kv_j\). In that order the quadratic block
\(4T\otimes T\) represents
\(4(u^{\mathsf T}Tu)(v^{\mathsf T}Tv)\), while the rank-one term
represents \(8(u^{\mathsf T}Tv)^2\). The cross block contributes
\(4(b^{\mathsf T}u)(v^{\mathsf T}Tv)+8(b^{\mathsf T}v)(u^{\mathsf T}Tv)\).

The perturbation Gram construction distributes coefficients over ordered
matrix entries. This correctly includes both copies of off-diagonal
entries and gives a symmetric rational matrix. Every monomial of a
quartic Hessian biform occurs among these entries, so there is no missing
coefficient equation.

I read and reran the retained checker. It verifies an exact rational
\(20\times20\) factorization with strictly positive diagonal pivots,
and separately expands the differentiated biform identity. Thus it
establishes positive definiteness without floating-point tolerances.
If the Gram matrix is \(M\succ0\), its basis vector contains the
direction \(v\) itself, so

\[
 v^{\mathsf T}\nabla^2F(c+u)v
 \geq\lambda_{\min}(M)\bigl(\|v\|^2+\|u\otimes v\|^2\bigr)
 \geq\lambda_{\min}(M)\|v\|^2.
\]

This is a uniform global strong-convexity proof. A large positive LDL
pivot by itself would not give the same numerical eigenvalue bound;
the main note correctly avoids that inference.

All rational quadratic summands vanish exactly at
\(a=(\alpha,\alpha^2,\beta,\beta^2)\), where \(\alpha^3=2\) and
\(\beta^3=5\). The cubic multiplying \(y\) has value and both first
derivatives zero at \((\beta,\beta^2)\). Thus \(F(a)=0\) and
\(\nabla F(a)=0\). Strong convexity then proves that zero is the
global minimum and that \(a\) is the unique zero.

## The arithmetic obstruction

The field-degree argument is necessary in addition to the checker's
formal quotient arithmetic. I independently checked the simpler trace
argument in the integrated note. If \(\beta=b_0+b_1\alpha+b_2\alpha^2\)
belonged to \(\mathbb Q(\alpha)\), it would generate that cubic field.
Its zero trace and the zero trace of its square give \(b_0=0\) and
\(12b_1b_2=0\). The remaining equations require a rational cube root
of \(5/2\) or \(5/4\), contradicted by prime valuations. A reducible
cubic over a real field has a real root in that field, so \(T^3-5\)
is irreducible over \(\mathbb Q(\alpha)\). The joint degree is nine.

The nine field-basis elements are evaluations of
\(1,x,y,z,w,xz,xw,yz,yw\). Therefore the rational quadratic vanishing
space has dimension six. The six displayed quadrics are independent
because their degree-two monomials are distinct. They form its whole
basis, rather than merely a collection of vanishing relations.

Products of these basis elements either use only one block or have
degree at most two in each block. Their coefficient on \(yz^3\) is
therefore zero. The constructed polynomial has coefficient one there.
If a quartic is a rational SOS, every summand has degree at most two:
the highest homogeneous squares cannot cancel over the reals. At a
real zero every summand vanishes individually. These two facts put any
hypothetical rational SOS in the excluded product span and give the
contradiction.

This proof excludes positive rational weighted SOS as well. It does
not exclude real or algebraic polynomial squares, rational-function
SOS representations, or other certificate systems. In particular no
polynomial descent conclusion can be inferred merely from odd extension
degree.

## Positive constant perturbations

The lemma asserting rational SOS for every \(F+\eta\), rational
\(\eta>0\), is valid. Here is the rank issue that requires care.
Translate the full positive definite Hessian Gram matrix to the exact
minimizer \(a\); this is an invertible real congruence. After subtracting
\(\mu I\) for sufficiently small \(\mu>0\), the residual is positive
semidefinite. Taylor integration along \(a+tu\) gives a real SOS Gram
for the residual polynomial and contributes exactly

\[
 \frac{\mu}{2}\|u\|^2+\frac{\mu}{12}\|u\|^4.
\]

The first term covers all linear monomials. The identity
\(\|u\|^4=\sum_i u_i^4+2\sum_{i<j}(u_iu_j)^2\) covers every
quadratic monomial with a strictly positive diagonal coefficient.
Thus the Gram matrix is positive definite on the entire space of
nonconstant monomials of degree at most two, not only on a selected
subspace. Adding \(\eta\) fills the constant coordinate and makes the
full polynomial Gram matrix positive definite. Translating back is
again invertible.

The coefficient equations for this Gram matrix form a consistent
rational affine system. Gaussian elimination gives a rational point
and a rational basis for its nullspace, proving density of rational
points in the real solution space. Positive definiteness is open, so
a rational positive definite Gram matrix exists. Positive rational LDL
weights are sums of rational squares. This proves the lemma without
an unjustified rational rounding that could lose the coefficient
identities.

The argument is qualitative. It does not bound coefficient sizes as
\(\eta\) tends to zero. It proves nonattainment of the exact rational
SOS lower-bound supremum, while the real SOS problem does attain its
bound. It does not prove semidefinite-program nonattainment over the
reals.

## Verification record

Command independently run:

```text
python research-20260927/check_rational_sos_convex_descent.py
```

All assertions passed, including exact differentiation, positive rational
LDL factorization, zero and stationarity, evaluation rank, and the
forbidden coefficient. This is executable exact-arithmetic evidence;
it is not a formal verification of Python or SymPy. The field argument,
global implication of the Gram matrix, and density lemma were checked
mathematically above. No project-wide verification or CI checks were run.

The theorem is a useful arithmetic boundary for exact convex polynomial
optimization. This review does not establish novelty, minimal dimension,
or a complexity lower bound. Those claims would require separate work.
