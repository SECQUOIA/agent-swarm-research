# Polynomial-size rational-circuit interior Grams

Date: 2026-10-03. This is a representation consequence of the
[variable-degree upper reduction](strong-convex-polynomial-posslp-upper.md)
and the [explicit Taylor Gram formula](../../../../research-20260927/interior-gram-single-exponential-upper.md).
It does not improve the expanded rational output bound or establish a new
general SOS algorithm.

## Statement

Let \(f\in\mathbb Q[X_1,\ldots,X_n]\), \(n\ge1\), have degree at most
four, and suppose the input supplies a rational positive definite matrix
\(A\) with
\[
 v^{\mathsf T}\nabla^2f(X)v
       =(v,X\otimes v)^{\mathsf T}A(v,X\otimes v).
\]
Count the expanded coefficients and the full matrix in the input length.
Let \(z(X)\) be the ordinary vector of all monomials of degree at most two.

**Corollary.** A deterministic polynomial-time algorithm constructs a
symmetric matrix \(Q\) of rational arithmetic circuits satisfying
\(f=z^{\mathsf T}Qz\). If \(\min f>0\), this matrix is positive definite.
Thus every strictly positive input in this class has a positive definite
ordinary polynomial Gram whose entries admit a polynomial-size shared
rational-circuit representation. The construction uses no sign oracle and
does not need a supplied lower bound on the positive minimum.

The identity holds on every valid input. When \(\min f\le0\), the
constructed Gram is not positive definite, since no positive definite Gram
on this full monomial basis could represent \(f\).

## Construction and proof

Put \(m=n+n^2\), and compute
\[
                   \mu=\det(A)/(\operatorname{tr}A)^{m-1}.
\]
This has polynomial bit length and satisfies \(A\succeq\mu I\).
Define the explicitly expanded rational observable
\[
             h(X)=f(X)-\frac{\|\nabla f(X)\|^2}{2\mu}.
\]
It has degree at most six and polynomial encoding length. At the unique
minimizer \(p\), \(h(p)=f(p)\).

Run the Newton-circuit construction of the upper theorem with objective
\(f\) and observable \(h\), stopping before its final PosSLP query. It
produces a rational vector \(q\), as a polynomial-size shared circuit,
such that \(|h(q)-h(p)|\le g/8\), where every nonzero \(h(p)\) has
absolute value at least \(g\). Hence \(\min f>0\) implies
\(c:=h(q)>0\). Every division in the construction is well-defined on all
valid inputs, independently of the minimum's sign.

Let \(d=X-q\), \(b=\nabla f(q)\), and
\(\bar A=A-\mu\operatorname{diag}(I_n,0)\). Write
\[
 U=(d,q\otimes d)=C_Uz,\qquad
 V=(0,d\otimes d)=C_Vz,\qquad
 d+b/\mu=C_{\rm aff}z.
\]
These coefficient matrices have polynomial dimensions and rational-circuit
entries of polynomial total size. If \(e_0\) selects the constant
monomial, set
\[
\begin{aligned}
 Q={}&\tfrac12(C_U+C_V/3)^{\mathsf T}\bar A(C_U+C_V/3)
       +\tfrac1{36}C_V^{\mathsf T}\bar A C_V\\
    &+\tfrac\mu2 C_{\rm aff}^{\mathsf T}C_{\rm aff}
       +c\,e_0e_0^{\mathsf T}.
\end{aligned}
\]
Taylor integration and completion of the gradient term give the exact
identity \(f=z^{\mathsf T}Qz\). No approximation enters this identity:
the circuit \(q\) represents an exact rational vector.

Since \(\bar A\succeq\mu\operatorname{diag}(0,I_{n^2})\), the first
three summands are PSD. If \(c>0\), the second summand supplies all
translated homogeneous quadratics \(d_id_j\), the third supplies the
affine factors \(d_i+b_i/\mu\), and the last supplies the constant.
Together they span the full quadratic polynomial space. Therefore
\(Q\succ0\).

Every subsequent operation has polynomial matrix dimension and adds only
polynomially many gates while retaining the shared circuit for \(q\).
This proves the output-size and construction-time statements.

## Limits and relation to expanded output

The [interior-Gram lower family](../../../../research-20260927/interior-gram-bit-lower-bound.md)
requires \(\Omega(n2^{n/2})\) denominator bits in every expanded positive
definite ordinary Gram. The corollary gives short shared rational circuits
even for that family. It does not contradict the lower bound: expanding a
small circuit can require exponentially many bits.

Constructing this representation does not assert polynomial-time exact
validation of circuit identities, positive definiteness, or the premise
\(\min f>0\). Those are different computational tasks. No polynomial-size
unweighted rational SOS decomposition is asserted by this argument; splitting
circuit-encoded positive rational weights into rational squares needs a
separate analysis. The theorem concerns a circuit representation of a Gram,
with the original full strict Hessian certificate still required.
