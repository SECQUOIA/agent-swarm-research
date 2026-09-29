# Exact strongly convex quartic optimization over rational polyhedra: an active-face oracle bound

Date: 2026-09-28. Status: proved and passed
[independent adversarial review](polyhedral-strong-quartic-posslp-upper-review.md).
The proof depends on the reviewed polynomial-observable
extension of the [unconstrained PosSLP upper bound](strong-convex-quartic-posslp-upper.md).
Publication priority is unestablished.

Exact threshold comparison for a globally strongly convex rational
quartic over an arbitrary rational polyhedron belongs to
\(\mathrm{NP}^{\mathrm{PosSLP}}\cap\mathrm{coNP}^{\mathrm{PosSLP}}\),
when a positive rational global curvature bound is supplied. The
certificate guesses at most \(n\) active, linearly independent
constraint normals. Its verification uses a polynomial number of
PosSLP queries about the minimizer on their affine intersection.

This is an elementary consequence of polyhedral optimality and the
unconstrained comparison theorem. It does not establish deterministic
\(\mathrm P^{\mathrm{PosSLP}}\), a single-query reduction, or a new
general algorithm for exact convex programming. Its useful point is
that arbitrary faces, redundant inequalities, and lower-dimensional
feasible sets need no strict-feasibility assumption.

## 1. Input, output, and the oracle dependency

Let \(f\in\mathbb Q[X_1,\ldots,X_n]\) have degree at most four,
and let the supplied rational \(\mu>0\) satisfy the promise
\[
                 \nabla^2 f(X)\succeq\mu I_n
                 \qquad(X\in\mathbb R^n).                 \tag{1}
\]
Let \(P=\{X:AX\le b\}\), with explicit rational \(A,b\), and
let \(r\in\mathbb Q\). For empty \(P\), set the optimal value
to \(+\infty\). Otherwise write \(p_P\) for the minimizer and
\(v_P=f(p_P)\).

**Theorem.** On the promised inputs, each exact comparison
\[
                         v_P\mathrel{\bowtie}r,
       \qquad \bowtie\in\{<,\le,=,\ne,\ge,>\},           \tag{2}
\]
has both an \(\mathrm{NP}^{\mathrm{PosSLP}}\) verifier and a
\(\mathrm{coNP}^{\mathrm{PosSLP}}\) verifier. The same holds for
the language asserting that \(P\ne\varnothing\) and a supplied
coordinate of \(p_P\) satisfies a chosen comparison with \(r\).

If a rational positive definite full Hessian Gram is supplied and
checked, as in the companion unconstrained theorem, (1) can be
certified in polynomial time and a suitable \(\mu\) computed.
Rejecting invalid Gram certificates gives the corresponding ordinary
languages. For a bare supplied \(\mu\), the theorem is a promise
statement; it does not include recognizing global strong convexity.

The only nonstandard algorithmic dependency is this companion lemma:

> Given an explicit rational strongly convex quartic \(g\), a supplied
> positive rational global curvature bound, and an explicit rational
> polynomial \(h\) of degree at most four, the sign of \(h(p_g)\)
> at the unique unconstrained minimizer can be compared exactly with
> zero using one PosSLP instance per comparison, in polynomial time.

The observable \(h\) need not be convex. The companion proof applies
its singleton real-projection separation bound to
\(\nabla g(Y)=0,\ z=h(Y)\), and evaluates \(h\) on its Newton
circuit with the corresponding derivative bound. The input length
includes \(h\). This argument does not assume a finite complex
critical locus. It also does not expand the high-precision Newton
iterate into a rational number with exponentially many bits.

All observables below are explicit polynomials of degree at most four
and polynomial coefficient bit length. No assertion about arbitrary
arithmetic-circuit observables is needed.

## 2. A small optimal active support exists without Slater's condition

Rational linear programming decides whether \(P\) is empty in
polynomial time. For nonempty \(P\), (1) implies coercivity of
\(f\), so the minimum on the closed set \(P\) is attained.
Strong convexity gives uniqueness.

Let \(\mathcal A=\{i:a_i^{\mathsf T}p_P=b_i\}\), where
\(a_i^{\mathsf T}\) is row \(i\) of \(A\). Then
\[
             -\nabla f(p_P)\in
                       \operatorname{cone}\{a_i:i\in\mathcal A\}.
                                                               \tag{3}
\]
Here is a direct argument that includes lower-dimensional polyhedra.
Every direction \(d\) satisfying \(a_i^{\mathsf T}d\le0\) for
all active rows gives a feasible segment \(p_P+td\), for sufficiently
small \(t\ge0\). The finitely many inactive inequalities have
positive slack. Therefore \(\nabla f(p_P)^{\mathsf T}d\ge0\).
The polar-cone form of Farkas' lemma gives (3).

Choose a representation in (3) with minimum support. Its used normals
are linearly independent. Indeed, any nonzero dependence can be signed
to have a positive coefficient. Subtracting the largest allowed
multiple from the positive representation preserves nonnegativity
and makes one coefficient zero, contradicting minimal support.
Consequently there is a set \(I\subseteq\mathcal A\), with
\(|I|\le n\), such that its rows are independent and
\[
       A_Ip_P=b_I,\qquad
       \nabla f(p_P)+A_I^{\mathsf T}\lambda=0,
       \qquad \lambda\ge0.                              \tag{4}
\]
If the gradient is zero, the empty support is allowed. The selected
set need not contain every active inequality or span the affine hull
of the minimal face containing \(p_P\). That distinction matters
when multipliers are zero.

## 3. Affine restriction preserves the supplied curvature bound

For any guessed set \(I\) with \(s=|I|\le n\), reject it if
the rows of \(A_I\) are dependent. Select an invertible
\(s\)-by-\(s\) column submatrix \(B\), and let \(N\) be the
remaining columns. In the corresponding coordinate order, parameterize
the affine space \(A_IX=b_I\) by
\[
       X_B=B^{-1}(b_I-NY),\qquad X_N=Y,
       \qquad X=\bar x+ZY.                              \tag{5}
\]
The case \(I=\varnothing\) means \(\bar x=0,Z=I_n\).
Rational elimination constructs (5) with polynomial bit length.
The free-coordinate block of \(Z\) is an identity, so
\[
                         Z^{\mathsf T}Z\succeq I_{n-s}.
\]
For \(s<n\), the restricted polynomial
\[
                         g_I(Y)=f(\bar x+ZY)
\]
therefore satisfies
\[
 \nabla^2g_I(Y)=Z^{\mathsf T}\nabla^2f(\bar x+ZY)Z
                       \succeq\mu I_{n-s}.                 \tag{6}
\]
No additional curvature loss or conditioning promise is required.
The coefficients of \(g_I\) have polynomial bit length and its
degree remains at most four. Fixed-degree expansion has polynomial
size in the input dimension.

Let \(y_I\) be its unique unconstrained minimizer and set
\(p_I=\bar x+Zy_I\). If \(s=n\), use instead the unique rational
point of the zero-dimensional affine space. That case requires no
unconstrained optimization or PosSLP query to evaluate a polynomial.

For the support in (4), the restriction has stationary point \(p_P\)
and hence \(p_I=p_P\). This remains true when the feasible polyhedron
has no ordinary interior.

## 4. Polynomial-oracle verification

For a guessed independent support \(I\), define the polynomial vector
\[
 \Lambda_I(Y)=-(A_IA_I^{\mathsf T})^{-1}A_I
                           \nabla f(\bar x+ZY).             \tag{7}
\]
It has degree at most three and polynomial rational coefficient length.
For the empty support it has no entries. Verify the following exact
conditions at \(Y=y_I\):

1. Every primal slack
   \(b_j-a_j^{\mathsf T}(\bar x+ZY)\) is nonnegative.
2. Every entry of \(\Lambda_I(Y)\) is nonnegative.
3. Every entry of
   \(\nabla f(\bar x+ZY)+A_I^{\mathsf T}\Lambda_I(Y)\)
   is zero.

The third condition also follows mathematically from restricted
stationarity, but keeping it explicit makes the certificate verification
transparent. All these tests use the companion polynomial-observable
lemma. There are polynomially many tests. Equality can be tested by
two strict-sign queries if necessary; the claimed complexity does not
require combining the tests into a single query.

If the tests pass, \(p_I\) is the global minimizer on \(P\).
Indeed, for every \(X\in P\), convexity and the tested conditions
give
\[
\begin{aligned}
 f(X)&\ge f(p_I)+\nabla f(p_I)^{\mathsf T}(X-p_I)\\
     &=f(p_I)-\Lambda_I(y_I)^{\mathsf T}A_I(X-p_I)
      \ge f(p_I),
\end{aligned}
\]
because \(A_Ip_I=b_I\). Thus no incorrectly guessed support can
pass and certify the wrong optimum.

Finally test the chosen relation for \(g_I(y_I)-r\), an observable
of degree at most four. This gives an NP oracle verifier for (2).
For its complement, guess a support, run exactly the same optimality
checks, and test the complementary relation. For every nonempty
polyhedron an optimal support exists by Section 2, regardless of
which comparison is true. Empty polyhedra are handled deterministically
according to the stated \(+\infty\) convention. Coordinate comparison
uses the affine observable \((\bar x+ZY)_j-r\) instead.

This proves both oracle inclusions. It uses polynomially many
PosSLP calls after a polynomial-length discrete guess, not one
PosSLP instance for the entire constrained decision problem.

## 5. Stronger bounds not established here

Enumerating all independent supports gives an exact deterministic
algorithm with up to \(\sum_{s=0}^n\binom ms\) candidate supports,
each handled in polynomial time with a PosSLP oracle. This count is
not polynomial when dimension varies.

An ordinary polynomial-bit approximate minimizer does not automatically
identify the correct support. A nonzero slack or multiplier can be much
smaller than inverse exponential in the printed input length, and the
algebraic bounds used in the companion theorem permit doubly
exponentially small gaps. Asking a weak-optimization routine for that
many expanded accuracy bits does not give a polynomial-time reduction.
This observation blocks that particular argument; it is not a lower
bound excluding some different deterministic oracle algorithm.

Guessing the entire active set would make that set unique, but verifying
optimality then requires checking membership of the gradient in the
cone of all active normals. An appeal to a real-arithmetic LP algorithm
is insufficient without verifying its operation model, rounding steps,
and how every algebraic comparison reduces to the available observable
oracle. No unambiguous complexity bound is asserted here.

## 6. Sources examined and contribution assessment

Slot, Steurer, and Wiedmer,
[Hesse's Redemption: Efficient Convex Polynomial Programming](https://arxiv.org/html/2511.03440v1),
Corollary 1.2, gives polynomial-time additive approximation over rational
polyhedra, including variable dimension. Section 1.3 and Table 1
distinguish exact comparison from approximation and leave exact convex
quartic complexity unresolved in their discussion. Section 1.4 also
explains why an SOS-based SDP formulation alone does not settle exact
bit complexity. Those passages were read directly. Their polynomial-time
approximation theorem is a dependency of the companion unconstrained
upper, not an exact-comparison theorem for the present problem.

The active-support argument uses classical polyhedral normal cones,
Farkas' lemma, and conic support reduction. Their elementary proofs are
included above, so no additional nonlinear constraint qualification is
imported. The result adds an oracle classification by combining those
facts with the separately proved unconstrained observable lemma.
It should be treated as a useful scope extension of that lemma, not
as a standalone major advance in convex optimization.

I also inspected the primary abstract of Tardos,
[A Strongly Polynomial Algorithm to Solve Combinatorial Linear Programs](https://pubsonline.informs.org/doi/10.1287/opre.34.2.250),
which bounds arithmetic steps independently of objective and right-hand
side sizes, and the statements of Theorems 1.1--1.2 in Dadush, Natura,
and Vegh,
[Revisiting Tardos's Framework for Linear Programming](https://arxiv.org/pdf/2009.04942),
which treat real LP data. These are possible ingredients for a stronger
canonical-support verifier. Their statements alone do not establish the
needed PosSLP simulation, and they are not used in the theorem above.

The source audit did not locate an equivalent constrained oracle theorem.
It was a narrow search and does not establish novelty. Further comparison
would be required before any publication-priority claim.

## 7. Verification record

The proof explicitly separates affine restriction, primal feasibility,
dual sign, stationarity, and comparison. No computation is used as a
substitute for the oracle complexity argument. The author ran:

```text
python3 research-20260927/check_polyhedral_strong_quartic_upper.py
```

It passed exact checks for lower-dimensional polyhedra, redundant active
rows, a support smaller than the full active face, empty supports,
zero-dimensional restrictions, rejection by primal infeasibility,
rejection by a negative multiplier, and preservation of the curvature
bound in a skew free-coordinate basis. It also checks a strongly convex
radial quartic with a positive-dimensional complex critical component,
illustrating why such components cannot be excluded in the oracle
dependency. These examples do not prove the complexity classification.

The independent reviewer reconstructed the complete proof and reran
the targeted checker successfully. The review covers lower-dimensional
normal cones, minimal conic supports, affine curvature, all observable
degree and bit bounds, both oracle inclusions, and the empty-input and
invalid-certificate branches. No substantive correction was needed.
No project-wide verification or CI inspection was performed.
