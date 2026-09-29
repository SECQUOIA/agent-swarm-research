# Independent review of exact convex quadratic optimizer recovery

Date: 2026-09-27. Reviewer: `optimizer_over_algebraic_constant_review`.

## Scope and conclusion

This review checks the proposed extension from an exact optimal value to
an exact optimizer for a rational convex quadratic program whose native
constraint Hessians span a space of dimension `h`. The objective is an
arbitrary **rational convex quadratic**. The review assumes the separate
value theorem and algorithm: when the finite optimum is attained, its
value `theta` has degree and coefficient bit lengths `N^{O(h+1)}`, and its
minimal polynomial and a strict rational isolating interval can be
computed in polynomial time for fixed `h`.

No obstruction was found to the following extension. The unique
minimum-norm optimizer has coordinate degree and coefficient bit lengths
`N^{O((h+1)^2)}`. It can be approximated to any prescribed number of bits,
then recovered exactly with the algebraic-recognition algorithm used in
[the feasible-point construction](algebraic-witness-recovery.md).
The resulting running time is polynomial for fixed `h`; this review does
not assert a sharp exponent for the composed algorithm.

The useful simplification is that no general linear algebra over
`Q(theta)` is necessary. The only irrational input coefficient introduced
by the optimal-value constraint is its constant term.

## 1. The canonical point and the affine restriction

Let `F` be the original feasible set and set

\[
 F^*=F\cap\{x:q_0(x)-\theta\le0\}.
\]

The assumed attainment makes `F*` nonempty. It is closed and convex, so
it has a unique minimum-norm point `x*`. The augmented native Hessian span
has dimension at most `h+1`.

At `x*`, turn active affine inequalities into equations and delete the
inactive inequalities. Retain active quadratic inequalities. If a point
of this restricted system had smaller norm, a sufficiently short segment
from `x*` toward it would satisfy every deleted row and improve the
original problem. Thus the norm minimum is preserved. Strict convexity
of the norm squared also preserves uniqueness. Adding the affine
differences between active quadratics and combinations of a Hessian basis
retains `x*` and hence retains this minimum.

All Hessians, including that of `q0`, are rational. The Hessian-basis
coefficients are therefore rational with polynomial original-input bit
length. Write the objective-threshold row with a formal parameter `T`.
Every resulting affine equation has the form

\[
 A x=d+eT,
\]

where `A,d,e` are rational and have polynomial bit length in `N`.
Rational elimination gives

\[
 x=a+bT+Vu,
\]

with rational `a,b,V` of polynomial bit length, and `V` of full column
rank. A zero-dimensional chart is already an affine expression in
`theta`, so its degree and height bounds are immediate.

There is a small parameter caveat. A chart from independent rows may
leave scalar consistency equations `alpha+beta T=0` from dependent rows.
For example, `F={x>=1}` and `q0(x)=x` give active equations `x=1` and
`x=T`; the chart `x=T` solves both only at `T=1`. These scalar equations
may simply be retained. Alternatively, they are redundant after a
minimal polynomial and isolating interval fix `T=theta`, where all the
equations are known to be consistent. A parametric identity for arbitrary
`T` must not be asserted without this qualification.

A second reviewer, `active_norm_restriction_audit`, separately checked
the segment argument, uniqueness, rational elimination, zero-dimensional
case, and the consistency caveat, and found no further obstruction.

## 2. Compressed KKT and elimination

Fix `T=theta`. Relax the retained quadratic rows to right-hand side
`epsilon>0` and minimize `||a+b theta+Vu||^2`. The objective is coercive
with positive definite Hessian `2 V^T V`; the old optimizer is strictly
feasible. Thus a unique relaxed optimizer and nonnegative KKT multipliers
exist. Its norm is bounded by `||x*||`, so compactness and uniqueness give
convergence to `x*` as `epsilon` decreases to zero.

The existing conic support argument keeps at most `h+1` multipliers.
Choose one support `J` occurring along a sequence approaching zero. Then

\[
 M=2V^TV+\sum_{i\in J}\lambda_i V^TQ_iV\succ0,
 \qquad \Delta=\det M>0,
 \qquad u=p(T,\lambda)/\Delta.
\]

Here `M` and `Delta` are independent of `T`, and the adjugate numerator
`p` is affine in `T`. Restricted quadratic coefficients have `T`-degree
at most two. After multiplying primal inequalities by `Delta^2` and
including complementary slackness, all KKT polynomials have total degree
`O(N)` and rational coefficient bit lengths polynomial in `N`. Positive
fixed rational denominators can be cleared without changing any signs.
Every retained primal row must remain in the formula, including rows
outside `J`.

Let `P(T)=0`, together with `l<T<r`, isolate `theta`. For coordinate `j`,
write the numerator of `x_j` as

\[
 A_j(T,\lambda)=(a_j+b_jT)\Delta+(Vp)_j.
\]

The formula

\[
 \forall\gamma\;[\gamma\le0\ \lor\
 \exists T,\epsilon,\lambda:\quad
 P(T)=0,\ l<T<r,\quad
 0<\epsilon<\min(1,\gamma),\quad
 -\gamma\Delta<A_j-z\Delta<\gamma\Delta,\quad
 \mathcal K_J(T,\epsilon,\lambda)]
\]

defines precisely the singleton `{x_j*}`. The root isolator fixes the
same `T=theta` for every positive `gamma`; placing `T` in the innermost
existential block is therefore valid. Only two quantifier blocks are
needed, of sizes `1` and at most `h+3`.

The reviewer inspected
[Basu's survey, Theorem 2.27, printed page 16](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
Its degree and integer coefficient-size estimates apply to this block
structure. The isolating polynomial contributes degree and coefficient
bits `N^{O(h+1)}`; the other polynomials have the bounds just given.
Thus output degree and coefficient bits are
`N^{O((h+1)^2)}`. Some nonzero output polynomial must vanish at the
singleton, and the elementary factor bound in the feasible-point note
transfers the estimate to its primitive minimal polynomial.

The same proof works for every rational linear form in the coordinates.
Its degree bound does not depend on the linear form's coefficient
magnitudes. The primitive-element argument already given in the
feasible-point note therefore also bounds the degree of the whole
optimizer field. Coordinate degrees alone would not justify that claim.

## 3. Recovery with rational-input queries

There is no need to pass the algebraic threshold `theta` to the
rational-input feasibility algorithm. The coordinate height bound gives
a computable rational box containing `x*`. For any additional rational
affine cuts and a rational norm threshold, intersect those cuts with the
box and `F`. Decide emptiness using the rational feasibility algorithm.
If the intersection is nonempty, compute the exact minimum of `q0` there
and compare its real algebraic value with `theta`. Compactness supplies
attainment. Equality holds precisely when these cuts meet `F*`.

This gives an exact decision oracle for the optimal set using only
rational-input optimization calls. The norm row increases the constraint
Hessian-span dimension by at most one; affine cuts do not increase it.
Apply the norm-value and coordinate bisections from the feasible-point
note with this oracle. The minimum-norm projection inequality supplies
the same quantitative coordinate approximation guarantee. Standard exact
univariate algebraic comparison handles the value equality test in time
polynomial in the polynomial degrees and coefficient bit lengths.

Finally, apply the already cited algebraic-recognition procedure at the
precision prescribed by the new degree and height bounds. This returns
the selected roots describing one common exact optimizer. The reasoning
depends on the separate exact-value algorithm; an approximate value
oracle alone would not justify equality tests against `theta`.

## 4. Limits of this review

This is a symbolic proof review, not a novelty determination or a
formalization. It does not re-prove the separate unbounded-domain
attainment and optimal-value theorem. It gives no universal rational
optimizer claim, no practical numerical conditioning estimate, and no
extension to nonquadratic objectives. The active set and sparse support
are existential devices for size bounds; the recovery procedure must not
enumerate all of them.

No mathematical experiment or project-wide verification was run. A
targeted document check verified this note's local Markdown links, final
newline, control characters, and trailing whitespace.

## 5. Check of the completed author text

The reviewer subsequently read the complete saved
[optimizer-recovery note](exact-convex-optimizer-recovery.md), rather than
only the proposed argument. Its equations (3)--(6) match the audited
route: rational pivot equations give the affine chart; dependent-row
consistency equations remain in the KKT formula; the determinant is
independent of the algebraic parameter; every retained primal row is
present; and the strict root isolator fixes that parameter in the two-block
limit formula. No substantive correction was needed.

The exact-value comparison paragraph is valid. Distinct normalized
irreducible integer polynomials are coprime and squarefree, so their
product has nonzero discriminant. An approximation error smaller than one
eighth of a valid distinct-root separation makes its stated half-separation
equality test exact. The minimum-norm bisection and Kannan--Lenstra--Lovasz
recovery refer to one common optimizer, and the conservative running-time
claim `N^{poly(h+1)}` allows the successive polynomial increases in input
length and oracle costs. The stated coordinatewise output does not claim
an independent common-field certificate. The review suggested only two
clarifications: explicitly retain original affine equalities, and specify
the one-eighth separation precision in the comparison paragraph.
