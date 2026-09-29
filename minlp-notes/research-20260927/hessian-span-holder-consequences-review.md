# Independent review of the Hölder consequences

Date: 2026-09-27. This review concerns
[the integer-slice, exact-penalty, and polyhedral-model note](hessian-span-holder-consequences.md).
It found no substantive gap in its deductions, conditional on the quantitative
Hölder constant, value-separation, polyhedral square-lift, and algebraic-witness
theorems cited there. A second, fresh reviewer independently checked the
outer-model and nearest-point deductions and reached the same conclusion.
Neither review establishes the dependencies themselves or novelty.

## Uniformity over integer assignments

An explicit rational box bounds the bit length of every allowed integer
coordinate by a polynomial in the original input length. Substituting an
integer assignment into total-degree-two rational rows therefore increases
their total encoding length by at most a polynomial, uniformly over all
assignments. The continuous Hessians do not change under substitution.
Consequently, the quantitative continuous estimate supplies one uniform
upper bound on all feasible-slice constants without enumerating slices.

The quantitative dependency explicitly covers trial points violating affine
rows: it first projects onto the polyhedron containing those rows and the
input box. Thus using the maximum of affine and quadratic violations in the
consequences note is justified. A feasible-slice repair remains inside that
slice's original box and affine system.

For an infeasible slice, the epigraph formulation of its minimum maximum
violation is compact after adding a direct rational upper bound on the
epigraph variable. Appending this variable adds zero Hessian rows and
columns, so its Hessian-span dimension is still at most the original \(h\).
The positive value gap applies uniformly after substitution. If its residual
is at least \(\Delta\), distance to any global feasible point is at most
the full box diameter. The constant
\(D_B\max\{1,\Delta^{-2^{-h}}\}\) therefore handles every infeasible
slice. Its logarithm fits the asserted bound. This use of a global repair is
appropriate only in this first mixed-integer estimate; the later Hausdorff
argument correctly uses feasible-slice repairs.

## Exact penalty and its quadratic lift

The bounded mixed-integer domain is a finite union of compact boxes, and the
feasible set is nonempty and closed. A closest feasible point exists.
Lipschitz continuity and the error bound give, at every infeasible point,

\[
 f(w)+\rho V(w)^{2^{-h}}
 \ge f(w_F)+(\rho-L_f C)V(w)^{2^{-h}}>f(w_F).
\]

This excludes every infeasible point from the full minimizer set, not merely
from one selected optimum. On feasible points the objective is unchanged.
The Lipschitz assumption is on the whole bounded mixed-integer domain, so it
also applies when an infeasible slice must be repaired in a different slice.
A rational quadratic objective has such a bound from its gradient on the
whole ambient box, regardless of its Hessian's sign.

For nonnegative lifted variables, the equations imply
\(t_h=t_0^{2^h}\). The residual inequalities are therefore equivalent
to \(t_0\ge V(w)^{2^{-h}}\). Conversely, the claimed values
\(t_j=V(w)^{2^{j-h}}\) satisfy every equation. They all lie in
\([0,U]\): if \(V\le1\), they are at most one; if \(V\ge1\),
they are at most \(V\le U\). The positive coefficient of \(t_0\)
selects equality. This verifies both the count of exactly \(h\) squaring
equations and the \(h=0\) case. The lift is nonconvex, as the note states.

## Every-fiber outer approximation

Joint positive semidefiniteness is explicitly imposed before invoking the
square-lift construction. Convexity only after fixing the integer variables
is sufficient for the error bound but is not silently substituted for this
stronger assumption.

For every projected lifted point, exact affine rows and the lower quadratic
approximations give \(V(z,x)\le\varepsilon\). Choosing
\(\varepsilon<\Delta\) excludes all infeasible integer slices. In a
feasible slice, the uniform Hölder estimate gives a point of the same
original fiber at distance at most
\(\overline C\varepsilon^{2^{-h}}\le\tau\). Original feasible points
all lift. These are precisely the two inclusions required for the claimed
Hausdorff bound.

The outer fiber is a projection of a polyhedron and is consequently a
polyhedron. The original box bounds it, so a nonempty outer fiber is compact.
The original feasible fiber is compact as well. This justifies both the
Hausdorff statement and attainment for the affine objective. Auxiliary
variable boundedness is not needed for this argument.

To make the precision calculation explicit, take
\(\tau=2^{-p}\), with integer \(p\ge0\), and
\(\varepsilon=2^{-L}\), where

\[
 L\ge\max\left\{\left\lceil\log_2(2/\Delta)\right\rceil,
       \left\lceil2^h(p+\log_2\overline C)\right\rceil\right\}.
\]

Because \(N\ge2\), the factor \(2^h\) multiplying
\(N^{O((h+1)^2)}\) is absorbed into the same asymptotic form. Thus
\(L\le N^{O((h+1)^2)}+O(2^h p)\) is sufficient. The formulation is
polynomial in \(N+p\) for fixed \(h\); this is a precision-bit
claim, not a polynomial bound in the bit length of a binary-encoded \(p\).

## Objective transfer and algebraic repair

The repair preserves \(z\), so only the continuous coefficient vector
enters the objective error:

\[
 c_z^Tz+c_x^Tx_F
 \le c_z^Tz+c_x^Tx+\|c_x\|_2\tau.
\]

Applying this to an outer optimizer and using inclusion of the original
feasible set proves the two-sided bound on optimal values. It does not imply
that the outer optimizer's integer assignment is optimal for the original
problem; it supplies the stated additive objective guarantee after repair.

For an exact rational outer output \(\bar x\) at integer assignment
\(z\), define

\[
 G=\{u:\bar x+u\in F_z\}.
\]

This is a nonempty rational convex quadratic system. Translation preserves
every continuous Hessian and hence their span. Its unique minimum-norm point
is \(x_F-\bar x\), where \(x_F\) is the unique Euclidean projection
of \(\bar x\) onto the closed convex fiber. The canonical algebraic-point
theorem therefore gives exactly the nearest repair claimed in the note.
The recovery algorithm's input length includes the rational output's bit
length. A polynomial-bit rational optimal continuous point can be selected
in the rational polyhedral fiber at the chosen integer assignment; the
integer box already bounds the assignment's bit length. This observation
supports fixed-parameter encoding claims, but does not supply a practical
algebraic repair implementation or certify a floating-point solver output.

## Verification limits

The review read the consequences note and the relevant sections of
[the qualitative estimate](hessian-span-holder-geometry.md),
[the constant-height argument](hessian-span-holder-height-review.md),
[the MILP projection construction](mixed-integer-span-frontier.md), and
[the algebraic recovery theorem](algebraic-witness-recovery.md).
The core quantitative and recovery theorems were treated as dependencies.
The second reviewer independently checked the every-fiber argument,
precision calculation, attainment, and translation.

No numerical experiment is needed to verify these deductions, and none is
claimed. No Lean verification, project-wide check, or CI inspection was
performed. Targeted verification run: an inline `python` command read only
this review, checked its five relative links, paired inline/display math
delimiters, trailing whitespace, control characters, and final newline.
All checks passed. These checks validate document integrity only.
