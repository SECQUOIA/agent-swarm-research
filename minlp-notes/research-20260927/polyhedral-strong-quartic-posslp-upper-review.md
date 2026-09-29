# Independent review of the polyhedral strongly convex quartic oracle bound

Date: 2026-09-28. Status: the frozen proof passes independent adversarial
review. No substantive defect was found. The result is an elementary
oracle extension of the unconstrained observable theorem; publication
priority is not established by this review.

The reviewed [main note](polyhedral-strong-quartic-posslp-upper.md)
has SHA256
8225490a64a323f9cb10578657ac93237aff2c70eea1636189837a93267195ba.
This reviewer did not contribute to the constrained construction.
The reviewer separately completed the
[fresh audit of its unconstrained observable dependency](strong-convex-quartic-posslp-upper-independent-review.md),
including the arbitrary nonconvex quartic observable extension.

## Optimality and a small independent support

Rational LP feasibility handles empty polyhedra. If \(P\) is
nonempty, global strong convexity makes the objective coercive, and
continuity on the closed set \(P\) gives an attained minimum.
Strict convexity gives uniqueness even when \(P\) is unbounded or
lies in a proper affine subspace.

At the minimizer \(p\), let \(\mathcal A\) be all active rows.
Every \(d\) with \(a_i^{\mathsf T}d\le0\) for \(i\in\mathcal A\)
gives a feasible segment \(p+td\) for sufficiently small \(t\ge0\).
For an inactive inequality with \(a_i^{\mathsf T}d>0\), take
\(t\) below its positive slack divided by \(a_i^{\mathsf T}d\).
There are only finitely many such requirements. Thus no constraint
qualification or ordinary interior is needed to obtain
\(\nabla f(p)^{\mathsf T}d\ge0\).

The polar of \(\{d:A_{\mathcal A}d\le0\}\) is the finitely generated
cone of the active normals. The signs therefore give
\(-\nabla f(p)=\sum_{i\in\mathcal A}\lambda_i a_i\) with
\(\lambda_i\ge0\).

Choose a representation with minimum support, and omit its zero
coefficients. If its normals were dependent, choose a dependence
\(\sum_i t_i a_i=0\) with some \(t_i>0\). Setting

\[
 \theta=\min_{t_i>0}\frac{\lambda_i}{t_i}
\]

and replacing \(\lambda_i\) by \(\lambda_i-\theta t_i\)
preserves the represented vector and nonnegativity while removing a
support index. This proves linear independence, including cones with
lineality. Hence at most \(n\) normals suffice.
When the gradient vanishes, the empty support suffices.

This support need not contain every active row, or span the affine
hull of the minimal face. Zero multipliers are not a defect in that
argument. The manuscript preserves this distinction correctly.

## Affine restriction and bit bounds

An independent selected row matrix \(A_I\) has full row rank, so
its affine equations are consistent for every right-hand side.
Selecting an invertible column submatrix \(B\) gives

\[
 X_B=B^{-1}b_I-B^{-1}NY,\qquad X_N=Y.
\]

The resulting \(Z\) spans the nullspace of \(A_I\), and its free
coordinate block is an identity. In particular,

\[
 Z^{\mathsf T}Z=I+(B^{-1}N)^{\mathsf T}(B^{-1}N)\succeq I.
\]

Thus the restricted polynomial has Hessian at least \(\mu I\)
everywhere. A general nullspace basis would require controlling its
least singular value; the chosen coordinates avoid that omission.
The rational elimination has polynomial bit complexity. Substituting
an affine map into a degree-four polynomial creates polynomially many
monomials and coefficient bits.

If \(|I|=n\), the restriction is a single rational point and is
evaluated directly. If \(I\) is empty, the restriction is the
original unconstrained problem. Both edge cases are handled correctly.

For a support coming from the optimum, the KKT relation implies
\(Z^{\mathsf T}\nabla f(p)=0\). The affine restriction is globally
strongly convex, so its unique unconstrained minimizer is the original
constrained optimum. No strict complementarity is used.

## Observable verification and soundness

For an independent support, \(A_IA_I^{\mathsf T}\) is a rational
positive definite matrix. The multiplier expression

\[
 \Lambda(Y)=-(A_IA_I^{\mathsf T})^{-1}A_I
                   \nabla f(\bar x+ZY)
\]

is an explicit rational polynomial vector of degree at most three.
Its matrix coefficients have polynomial bit length. Every primal
slack has degree at most one, every multiplier and stationarity
residual has degree at most three, and the value test has degree at
most four. Coordinate tests are affine.

These are the exact observables admitted by the already reviewed
unconstrained theorem. The verifier does not rely on a broader theorem
for arbitrary arithmetic-circuit observables, or on expansion of
the high-precision minimizer.

The full stationarity check is mathematically redundant because the
restricted gradient vanishes and \(Z\) spans the kernel of \(A_I\).
Keeping it as an additional polynomial collection of oracle tests is
sound and does not change the complexity classification.

For every support that passes all tests, its affine minimizer \(p_I\)
is feasible, \(\Lambda\ge0\), and
\(\nabla f(p_I)=-A_I^{\mathsf T}\Lambda\). For \(X\in P\),

\[
 f(X)\ge f(p_I)-\Lambda^{\mathsf T}A_I(X-p_I)\ge f(p_I),
\]

since \(A_Ip_I=b_I\) and \(A_IX\le b_I\).
Thus no accepted incorrect support can certify a different value.
Strong convexity also identifies the point uniquely, which is needed
for coordinate predicates.

## Both oracle inclusions

The witness consists only of at most \(n\) row indices, taking
\(O(n\log(m+1))\) bits for \(m\) inequalities.
All chart construction, polynomial expansion, and rational linear
algebra are polynomial time. There are polynomially many oracle tests,
each a valid PosSLP instance produced by the observable reduction.
The oracle machine may use positive and negative answers normally.

For every nonempty feasible polyhedron, an optimal support exists.
Every support passing the optimality checks yields the same optimum.
Testing the requested relation after those checks therefore gives
an \(\mathrm{NP}^{\mathrm{PosSLP}}\) verifier.
Replacing only the last predicate by its complement gives such a
verifier for the complement language. Hence the decision problem lies
in

\[
 \mathrm{NP}^{\mathrm{PosSLP}}
 \cap \mathrm{coNP}^{\mathrm{PosSLP}}.
\]

Empty polyhedra are decided first in deterministic polynomial time.
For rational \(r\), the \(+\infty\) convention makes \(<,\le,=\)
false and \(\ne,\ge,>\) true. The coordinate language explicitly
requires nonemptiness, so it is false on an empty polyhedron and its
complement is true there. This completes both verifier branches.

For a bare curvature promise, this is a statement on promised inputs.
For the full Hessian-Gram format, certificate validity is checked
first; invalid inputs are rejected, and their membership in the
complement is consequently decidable in polynomial time.
The note correctly distinguishes these two models.

## Sources and limitations

The inspected
[Slot–Steurer–Wiedmer Section 1.3 and Table 1](https://arxiv.org/html/2511.03440v1#S1.SS3)
do distinguish exact polynomial feasibility from additive
approximation and list the exact convex-quartic case as unresolved in
that version. Their Corollary 1.2 is an approximation result. This
confirms the scope of the source comparison, without proving that
the present restricted oracle classification is new.

The active-cone argument and support reduction are classical; their
short proofs above suffice for the result. The Tardos and
Dadush–Natura–Vegh references discussed as possible routes to stronger
results are not used in this theorem. This review does not validate a
real-arithmetic LP simulation or infer such a simulation from their
theorem statements.

The proof does not produce a deterministic
\(\mathrm P^{\mathrm{PosSLP}}\) algorithm, a many-one reduction,
or an unambiguous verifier. Enumerating supports is generally
exponential in dimension, and uniqueness of the optimum does not imply
uniqueness of a support certificate. The author's modest assessment
as a useful scope extension is appropriate.

## Targeted verification

The author checker was read in full, then independently rerun with

~~~text
python research-20260927/check_polyhedral_strong_quartic_upper.py
~~~

It passed. Its exact examples test lower-dimensional and redundant
constraints, supports smaller than the full active face, empty and
zero-dimensional restrictions, primal infeasibility, negative
multipliers, and the identity-block curvature bound for a skew chart.
The radial example correctly illustrates the possibility of complex
critical components in the companion theorem.

These tests supply boundary-case checks, not a proof of the complexity
classification or an implementation of a PosSLP oracle. The
all-dimensional support, soundness, and size arguments were checked
separately above. No Lean proof, project-wide verification, or CI
inspection was performed.

## Final status reconciliation

The final status-and-verification version has SHA256
ea390e27f2790212e8b5bc988cb34ed1c3621fddab703d47d50c14d85ce05450.
Its review link and verification account match this completed audit,
including the independent rerun of the author checker. These updates
pass scoped reconciliation. The mathematical proof is unchanged.
