# Independent review of the quadratic graph realization

Date: 2026-09-28. Status: the quantitative construction and its
strongly SOS-convex block consequence pass fresh independent review.
No mathematical correction was required. Publication priority was not
assessed.

This review concerns
[the quadratic graph realization](quadratic-graph-quartic-realization.md).
The reviewer read its earlier exploratory version without developing
the proof, then audited the complete frozen quantitative version.
The initial frozen source had SHA-256
`211ba52911032b695acab2845987dfa447a49b375a674c2ee6f806600bce7146`.
After the two clarifications recorded below, the final mathematical
source had SHA-256
`cd91a69214ccf5c0340cbe4d31bbe0558b090e6918bf5476ca906c2bb03bd41b`,
confirmed with
`sha256sum research-20260927/quadratic-graph-quartic-realization-candidate.md`.
A separate reviewer independently checked the approximation source,
precision order, rational recovery, and encoding bounds. The generic
singleton Hessian construction and the tower field obstruction remain
reviewed dependencies; their use here was checked.

The supplied full positive definite Hessian Gram implies
\(\nabla^2f\succeq\rho I\), with the stated determinant-over-trace
bound. In particular, the minimum is attained uniquely and strong
monotonicity gives \(\|p\|\le\|\nabla f(0)\|_1/\rho<P\),
including \(p=0\). The input promise supplies the exact value zero;
the construction never tests that promise.

The approximation step is justified by
[Slot, Steurer, and Wiedmer, Corollary 1.2](https://arxiv.org/html/2511.03440v1#S1).
It gives additive-error convex polynomial minimization over a rational
polyhedron in polynomial bit time. Proposition 3.2 and Appendix D
explain its rational implementation. The displayed box contains
\(p\), and objective error \(\rho\eta^2/2\) implies distance
at most \(\eta\). The final source caps that tolerance at one;
the smaller tolerance preserves the distance bound and makes the
runtime logarithm nonnegative. This clarification was checked.
The source's Proposition 3.2 omits the word
“convex” in its statement; the proof uses convexity, which is satisfied
here. No extension of that statement to nonconvex polynomials is used.

The lifted quadratic has the exact graph restriction claimed in
equation (6). On the graph, \(Cs=d\otimes d\), so the vector in
its integral is exactly the full Hessian vector along the Taylor
segment from \(q\) to \(y\). The integrated coefficients are
\(1/2,1/6,1/12\). This proves \(G_q(w_*)=0\) even though
\(q\) is only approximate. At \(q=p\), both the constant and
linear Taylor terms vanish, so the exposing gradient is zero.

The uniform quadratic-part bounds are valid. The duplication map has
\(C^{\mathsf T}C\) diagonal, with entries one for diagonal
coordinates and two for off-diagonal coordinates. The scalar moment
matrix has determinant \(1/72\) and trace \(7/12\), giving
minimum eigenvalue at least \(1/42\). Keeping the weaker \(1/48\)
therefore proves the claimed lower bound in \((d,s)\).

For clarity, the off-diagonal block of the affine-coordinate shear is
\[
 L_qd=(q_i d_j+q_j d_i)_{i\le j}.
\]
Its norm is at most the Frobenius norm of
\(qd^{\mathsf T}+dq^{\mathsf T}\), hence
\(\|L_q\|\le2\|q\|\). The shear and its inverse have norm
at most \(1+2\|q\|\), which is below the stated
\(2+2\|q\|\le J\). This verifies the congruence loss in
\(m_0\).

For the upper bound, before that shear the integral is at most
\[
 U\left[(\tfrac12+\|q\|^2)\|d\|^2
                          +\tfrac13\|s\|^2\right].
\]
This follows from the inequality used in the note and
\(\|C\|^2\le2\). Since \(\|q\|\le P+1\), the expression
is at most \(U(P+2)^2(\|d\|^2+\|s\|^2)\). The stated
\(L_0=10U(P+2)^2J^2\) is consequently conservative. Also
\(\|w_*\|\le\|p\|+\|p\|^2\le2P^2=K\), because
\(P\ge1\).

The coefficient majorant for \(\Phi\) introduces no hidden
dimension factor. The sum of the absolute values of all its
\(q\)-derivative entries is bounded by
\(d_\Phi S_\Phi(P+1)^{d_\Phi-1}\), and bounds the operator
norm. It is below \(D_\Phi\). Applying this bound along the
segment from \(p\) to \(q\), with the graph evaluation point
fixed at \(p\), proves equation (11). The degree is fixed and the
coefficient list is polynomial in size, so this bound is available
before \(q\) is computed.

The residual equations have the asserted unique real zero. The
quadratic graph equations enforce \(z_{ij}=y_i y_j\); the remaining
equations then enforce \(\nabla f(y)=0\). Strong convexity makes
that stationary point unique. In coordinates \((y,r)\), the
Jacobian is block triangular with blocks \(\nabla^2f(p)\) and
identity. The preceding coordinate change has determinant of absolute
value one, so equation (12) is correct, including its determinant
normalization.

The coefficient bounds in (13) suffice for every normalized residual.
For a quadratic of coefficient one-norm \(S\), its quadratic-part
matrix has operator norm at most \(S\), and its gradient on the
radius-\(K\) ball has norm at most \(2S(1+K)\). Thus the stated
\(W\) safely bounds the full Jacobian norm. Scaling by \(C_0\)
scales every singular value by that number. The determinant estimate
therefore gives
\[
 \sigma_{\min}(J_R/C_0)
 \ge \frac{\rho^n/C_0^N}{(W/C_0)^{N-1}}
 =\frac{\rho^n}{C_0W^{N-1}}\ge\nu.
\]
This establishes the lower bound on
\(\sum_jb_jb_j^{\mathsf T}\) with exactly the stated power of
\(C_0\). The quadratic normalization and gradient upper bounds
also follow. The exponents \(n\) and \(N-1\) are polynomially
bounded, so these rational constants have polynomial encoding length.

The full Hessian Gram calculation retains the potentially negative
\(T_j\otimes T_j\) terms. Its upper-left block is at least
\(2\epsilon\nu^2I\), and the lower-right block is at least
\((4m_0^2-4\epsilon N)I\succeq2m_0^2I\). The cross-block
bound is \(6\sqrt N\epsilon(L_0+NV)\). Consequently the Schur
subtraction is at most
\[
 \frac{18N\epsilon^2(L_0+NV)^2}{m_0^2}I
 \preceq\frac{\epsilon\nu^2}{2}I,
\]
using the final bound in (15). This gives the displayed
\(3\epsilon\nu^2/2\) margin. Equality in any permitted
upper bound on \(\epsilon\) causes no problem.

Completing the block square and translating the Hessian basis gives
the stated lower margin \(\gamma\). The shear inverse has norm
at most \(2+K\), and the bound \(B_D\) uses
\(\sqrt N\le N\). These are ordinary matrix estimates; the
argument does not infer Gram positive definiteness merely from
pointwise Hessian positivity. The explicit SOS has the unique zero
\(w_*\), and its degree is exactly four because the positive
definite quadratic part of \(G_q\) has a nonzero square as its
leading quartic term.

The rational recovery step is also valid. With \(q\) fixed, the
formal-center gradients are affine polynomials. The blocks \(C,D,Q\)
in (18) have degrees at most two, one, and zero, respectively.
Translation then yields a rational polynomial matrix of degree at
most four; that bound is sufficient. The formula is required to be
the correct Gram only at the true center. Omitting the nonzero
constant terms that arise at other formal centers therefore causes
no error in the argument.

After vectorizing the formal matrix, the sum of absolute derivative
entries is at most \(d_MS_M(K+1)^{d_M-1}\le L_M\). This bounds
the Euclidean-to-Frobenius operator norm without an additional
dimension factor. For the second approximation \(\widehat p\),
the graph error satisfies
\[
 \|v-w_*\|
 \le\delta+(\|p\|+\|\widehat p\|)\delta
 \le(2P+2)\delta.
\]
Thus (23) keeps the segment inside the radius-\(K+1\) ball and
makes the matrix error at most \(\gamma/8\). The final source
uses \(\widehat p\) in the general graph inequality immediately
after (23), replacing the initial dummy \(q\). This notation
clarification was checked; it does not change the estimate.

The coefficient selectors partition all ordered matrix entries.
Their disjoint supports make them Frobenius orthogonal; off-diagonal
pairs are counted twice, as required by a symmetric Gram. Equation
(24) is consequently the exact orthogonal projection onto every
Hessian coefficient equation. It fixes the true Gram, so the error
cannot increase, and
\(\widehat M\succeq7\gamma I/8\). Its support cardinalities
are nonzero integers at most \((N+N^2)^2\). They cause no
conditioning or encoding gap. Scaling by \(2/\gamma\) makes
the returned full Gram at least \(7I/4\), which implies the
claimed global Hessian lower bound.

The precision choices are acyclic:
\[
 (f,A)\longrightarrow\epsilon,D_\Phi
 \longrightarrow q,G_q,B_*
 \longrightarrow\mathcal M,L_M,\delta
 \longrightarrow\widehat p,T,\widehat M.
\]
There is no use of a tolerance that depends on its own approximation
output. Every polynomial degree is bounded by a constant; every
matrix dimension, coefficient list, rational exponent, and requested
precision is polynomial in the expanded input. Determinants,
fixed-degree expansion, evaluation, and projection therefore retain
polynomial bit time and size. The explicit squared factors for
\(B_*\) are supplied by construction. Rational scaling weights
can be expanded into polynomially many rational squares by the
binary numerator-times-denominator argument. No unspecified baseline
SOS, integer factorization, or algebraic minimal polynomial is needed.

The final field consequence uses only these established outputs and
the previously reviewed block lift. Adding a sufficiently large
polynomial-bit integer multiple of \(B_k\) makes the lifted second
block strongly SOS-convex while preserving its unique zero and the
joint rational SOS. The common zero minima force every separated
constant shift to vanish. Necessity of the tower field follows from
the first block; sufficiency follows by specialization at its tower
point. The imported individual-coefficient lemma then applies to
finite algebraic coefficient lists. The total variable count is
\(\Theta(k^2)\), so the degree lower bound is exponential in
\(\sqrt N\), as stated, rather than in \(N\). The joint
Hessian has a uniform positive bound and a short rational SOS
certificate, but every PSD Gram on its full joint Hessian basis is
singular because of additive block separation. No full joint
positive definite Gram is inferred.

The distinct exact check retained for this review is
[check_quadratic_graph_quartic_realization_review.py](check_quadratic_graph_quartic_realization_review.py).
For rational quartics with nonzero translated centers in one and two
variables, it independently forms the Taylor lift and verifies its
graph restriction, zero exposing gradient at the true center, and
the residual Jacobian determinant identity. A one-variable example
also checks the formal-center polynomial degree, the true-center
Hessian identity, exact coefficient projection, and Frobenius error
contraction. The command actually run was

```text
python research-20260927/check_quadratic_graph_quartic_realization_review.py
```

All checks passed. A final inline `python - <<'PY'` document check
passed local links, trailing whitespace, the final newline, and
balanced math delimiters. These finite checks support the new identities;
the uniform inequalities and polynomial-time claims are established
by the review above and the cited approximation theorem. No
project-wide verification, CI inspection, or Lean check was run.
