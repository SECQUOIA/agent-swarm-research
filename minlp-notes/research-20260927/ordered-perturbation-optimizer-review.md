# Independent audit of the ordered-perturbation optimizer bound

Date: 2026-09-27. Status: the proposed argument and the complete
[written proof](ordered-perturbation-optimizer.md) passed this review. This reviewer
was assigned after the root agent had proposed the argument, and did not
derive the original result. The review used the existing
[explicit elimination proof](explicit-span-separation.md) and
[optimizer recovery proof](exact-convex-optimizer-recovery.md).

The proposed conclusion is that the minimum-norm optimizer of an attained
rational convex QCQP belongs to a number field of degree at most
\((2n+1)^{\min(h,n)}\), and each coordinate has an integer annihilator
with coefficient bit length \(N^{O(h+1)}\). Here `h` is the span dimension
of the native constraint Hessians, excluding the objective Hessian. Neither
Slater's condition nor a zero-dimensional full complex KKT variety is
assumed. The argument reviewed below supports this conclusion. It does not
establish publication priority or a practical algorithmic speedup.

## Active restriction and the selected point

Let \(x^*\) be the minimum-norm optimizer, with value \(\theta\).
Deleting inactive inequalities and replacing active affine inequalities by
equalities preserves the lexicographic minimum of
\((q_0(x),\|x\|^2)\). Indeed, a retained-feasible point with objective
below \(\theta\) would, on a sufficiently short segment from \(x^*\),
give an original feasible point with smaller objective. If its objective
equals \(\theta\) and its norm is smaller, the same segment is originally
feasible and optimal: convexity gives objective at most \(\theta\),
and global optimality gives the opposite inequality. Its squared norm is
smaller by convexity. Strict convexity also excludes a second distinct
point of equal minimum norm.

The added Hessian-basis difference equations are rational affine equations
vanishing at \(x^*\). Restricting to them retains that same lexicographic
minimum. Rational row elimination gives \(x=x_0+Vu\), with full-column-rank
`V` and polynomial coefficient bit lengths. On this affine space, all
retained native quadratic polynomials span a space of dimension at most
`h`. This statement concerns complete restricted polynomials, so their
gradients at any one point also span at most `h` dimensions.

The regularizer must be the original squared norm
\(\|x_0+Vu\|^2\). Using \(\|u\|^2\) instead can select a different
optimizer. The proposed proof uses the correct norm.

## Both limits are justified separately

On the retained feasible set, minimize
\(q_0(x)+\varepsilon\|x\|^2\) for \(\varepsilon>0\).
In free coordinates its Hessian is positive definite. Its unique optimizer
\(x_\varepsilon\) satisfies

\[
 q_0(x_\varepsilon)+\varepsilon\|x_\varepsilon\|^2
 \le \theta+\varepsilon\|x^*\|^2,
 \qquad q_0(x_\varepsilon)\ge\theta.
\]

Thus \(\|x_\varepsilon\|\le\|x^*\|\), and every cluster point as
\(\varepsilon\downarrow0\) is optimal with norm at most
\(\|x^*\|\). Uniqueness of the minimum-norm optimizer proves convergence
to \(x^*\).

For each fixed positive \(\varepsilon\), relaxing retained rows to
\(q_i\le\delta\) gives strict feasibility for every \(\delta>0\).
The objective is coercive, and comparison with \(x^*\) places all these
minimizers in one compact sublevel set for that fixed \(\varepsilon\).
Any limit as \(\delta\downarrow0\) is retained-feasible and minimizes
the strongly convex regularized objective. It is therefore
\(x_\varepsilon\). No compact bound uniform in \(\varepsilon\),
and no rate relating \(\delta\) to \(\varepsilon\), is required.

## Support selection and local nonsingularity

At each doubly perturbed optimizer, take a representation of the negative
objective gradient by active constraint gradients with minimum support.
Its positive-weight gradients are linearly independent: a nonzero linear
dependence permits varying the weights until one positive weight becomes
zero, while preserving nonnegativity and the represented vector. Hence the
support size is at most \(\min(h,d)\).

For each member of a sequence \(\varepsilon_\ell\downarrow0\), one
support occurs along an inner sequence \(\delta\downarrow0\). Among
the finitely many resulting supports, one occurs for an outer subsequence.
This fixes one support before choosing any coordinate or linear
combination. It provides all the nested limits used in the joint-field
argument.

For that support the positive definite Lagrangian matrix `M` gives the
stationary point by \(u=p/\Delta\), where \(\Delta=\det M\).
For \(G_i=\Delta^2(q_i(p/\Delta)-\delta)\), the multiplier Jacobian
at the selected root is

\[
 -\Delta^2
 \left[\nabla q_i(u)^T M^{-1}\nabla q_j(u)\right]_{i,j}.
\]

It is negative definite. Rational denominator clearing only multiplies
rows by nonzero constants, so it preserves nonsingularity. The selected
roots need not be nonsingular points of unrelated KKT components.

## Ordered elimination and exceptional parameter values

The finite-quotient construction in the linked elimination proof treats
\(\varepsilon,\delta\) as coefficient indeterminates and introduces a
third parameter \(\beta\) in
\(G_i+\beta\lambda_i^{a+1}\). The same staircase quotient and
determinant bound apply. First extract the lowest nonzero coefficient of
the auxiliary undefined-value parameter, then the lowest nonzero
\(\beta\)-coefficient. This gives a nonzero
\(R(\varepsilon,\delta,w)\) vanishing at every selected nonsingular
root's ratio.

Write the lowest nonzero \(\delta\)-coefficient as
\(S(\varepsilon,w)\). For each fixed selected
\(\varepsilon_\ell\), divide the identity by the global lowest power
of \(\delta\), then take the inner limit. This proves
\(S(\varepsilon_\ell,w_\ell)=0\). A specialization may make
\(S(\varepsilon_\ell,w)\) identically zero; that does not invalidate
the equality. Finally extract its globally lowest nonzero
\(\varepsilon\)-coefficient and pass to the outer limit. The resulting
univariate polynomial is nonzero by construction and vanishes at the
limiting ratio.

This order is essential to the proof as written. Simply substituting zero
for both perturbations in the determinant could produce the zero
polynomial. The proof does not make that substitution, and it does not
assume a generic outer parameter or bounded multipliers.

## Degree, height, and the common field

With `s` selected multipliers and `d` free primal coordinates,
\(\Delta\) and `p` have multiplier degree at most `d`. Use common
denominator \(A=\Delta^2\) and coordinate numerators
\((x_{0j}\Delta+(Vp)_j)\Delta\). These numerators and the active
equations have multiplier degree at most \(a=2d\). The quotient dimension
is \((a+1)^s\), yielding the asserted degree bound.

The coefficient \(\ell_1\)-norm estimate is unchanged by having two
coefficient parameters. Reduction multiplies by the full polynomials
`G_i`, so its norm already includes all their parameter monomials.
Rational affine elimination, determinant expansion, and common denominator
clearing give initial log norm \(N^{O(1)}\). Multiplication determinants
then give log norm \(N^{O(h+1)}\); successive coefficient extractions
cannot enlarge it. An integer factor bound is still needed to transfer the
annihilator bound to a primitive minimal polynomial, with the same
asymptotic exponent.

For every rational linear combination of coordinates, the same selected
support and nested sequences apply. Its numerator still has multiplier
degree at most `a`, irrespective of the rational coefficients' heights.
Each coordinate is algebraic, and the primitive element theorem provides a
rational linear combination generating their field. Its degree bound is
the same quotient dimension. Thus one must not multiply separate
coordinate degrees to estimate the joint field. The optimal value belongs
to this field because the objective has rational coefficients.

The cases `d=0` and `s=0` are harmless. A zero-dimensional rational affine
space gives a rational point directly; an empty multiplier support gives a
one-dimensional quotient and a degree-one bound. Empty native constraint
lists, zero objective, inactive constraints, and singular original KKT
systems cause no additional exception. Finite attainment remains a stated
dependency when it is not taken as a hypothesis.

## Prior comparison and remaining limits

[Grigoriev and Pasechnik, Theorem 1.10 and Section 2](https://arxiv.org/pdf/cs/0403008v3)
already study iterated limits of rational maps over ordered infinitesimals,
with algebraic degree and integer coefficient-size bounds. Section 2 uses
special Gröbner bases with pure-power leading monomials, finite staircase
quotients, and multiplication matrices. The theorem and the beginning of
its proof were inspected directly in the primary PDF. Accordingly, ordered
perturbations and finite-quotient limit algebra are established machinery.
The contribution under review is their use after the native-Hessian-span
restriction, including the original-coordinate canonical optimizer and the
explicit degree formula.

[Nie and Ranestad, Theorem 2.2 and Corollary 2.5](https://arxiv.org/pdf/0802.1233)
give a sharper generic QCQP degree and a nongeneric upper bound when the
entire critical system is zero-dimensional. The primary text was inspected.
The present proof requires nonsingularity only at selected perturbed
multiplier roots and permits other positive-dimensional components. This
distinction supports the stated scope; it does not prove that standard
intersection theory cannot yield the same or a sharper bound.

Minimum-norm selection by vanishing Tikhonov regularization is also
classical. For example, the primary
[Attouch--Laszlo abstract](https://arxiv.org/abs/2104.11987)
describes minimum-norm convergence for much broader convex problems. That
abstract was inspected only to check the attribution, not as a dependency
for the elementary compactness proof above.

No substantive correction to the root's proposed proof was needed in this
review. The requests for explicit wording were: keep the original norm,
fix the nested support independently of the output coordinate, retain the
factor-height step, and cite the established ordered-infinitesimal
machinery. Reading the complete draft also prompted correction of a missing
display delimiter, clarification that only the retained constraint
polynomials have span at most `h`, and consistent use of original and
free-coordinate feasible sets. The bound does not by itself construct the unknown active
restriction or a common-field representation, improve the full algorithm's
stated running-time exponent, or establish novelty. Those remain separate
claims requiring their own proofs.

Verification consists of independent proof reconstruction, a complete read
of the author's written proof, and the specified primary-source checks.
The targeted command

```text
python research-20260927/check_ordered_optimizer_review.py
```

passed four exact symbolic stress cases: ordered limits differing from a
diagonal limit, an identically vanishing specialized lowest coefficient,
a permanent undefined-value factor requiring the auxiliary extraction, and
minimum-norm selection after a rational affine change of coordinates. These
cases exercise specific delicate steps; they do not establish the general
theorem. A targeted inline Python check of this review and its symbolic
script passed for three local links, trailing whitespace, control
characters, and final newlines. The author's three wording and display
corrections listed above were reread after application. No numerical
computation or Lean proof is claimed to establish the general theorem. No
project-wide checks or CI inspection were performed.
