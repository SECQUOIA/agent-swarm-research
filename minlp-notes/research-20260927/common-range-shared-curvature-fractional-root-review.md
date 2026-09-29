# Independent review of the shared-curvature fractional theorem

Date: 2026-09-28. Reviewer: the root investigator, who did not develop
this extension. Scope: the complete
[shared-curvature manuscript](common-range-shared-curvature-fractional.md),
with particular attention to its value, attainment, and algorithmic
composition. The separate field review was also read. The previously
reviewed one-PSD-cut oracle, constant-matrix QP charts, quasiconvex
mixed-value bounds, and algebraic recovery machinery are dependencies.

**Finding.** No substantive gap was found under the stated assumption
that every numerator has a strictly positive multiple of the same
full PSD Hessian. The proof yields the claimed
\(f(k,\rho,\ell)N^C\) bound conditional on its imported quantitative
theorems, with an absolute input exponent. This review is not a
formal verification or a publication-priority assessment.

## Thresholds and the value bound

Dividing both numerator and denominator by the positive rational
curvature multiplier preserves the ratio, denominator positivity,
and the restricted denominator-gradient rank. It costs polynomial
encoding length even if the multiplier is very small.

At a rational threshold, introducing \(\eta\ge B(w)\) adds precisely
one unrestricted PSD row. All scenario thresholds are affine, and
the auxiliary coordinate has a zero native Hessian column. The
distinguished quadratic-row oracle therefore retains the original
native parameter \(\rho\).

After retaining all denominator directions, the coefficients on
\((v,\eta)\) are constant rational numbers. Their right-hand sides
are quadratic in the retained parameters and threshold. The fiber
objective \(B-\eta\) has a constant PSD Hessian. Its negative recession
directions are exactly those in equation (7), after a positive
homogeneous scaling: the scalar component must be positive, and
full PSD kills all cross terms involving a null direction of the
eliminated Hessian block. Such a direction decreases every normalized
numerator while fixing every denominator. A finite maximum then
tends to minus infinity. Checking original mixed-integer feasibility
before using this alternative is necessary and is explicitly done.

If no negative direction exists, the real-right-hand-side QP lemma
gives a finite attained fiber minimum. Its least-norm minimizer is
covered by a rational degree-two chart. Every accepted chart is
tested for actual feasibility and actual objective value, so
inconsistent stationarity equations or missing multiplier guards
cannot introduce a false epigraph point. Conversely the true fiber
minimum supplies a chart whenever the threshold is feasible.

The quartic chart formula quantifies only over the retained coordinates.
The exponentially many charts are used solely for bounds. Individual
coefficient sizes and logarithmic chart count have absolute polynomial
input bounds. Weak epigraph slices are convex because each threshold
residual has the same PSD Hessian; strict slices are nested unions.
Thus the separate quasiconvex value theorem and its weak-slice integer
witness conclusion have their required hypotheses. The original
unbounded threshold oracle, followed by recognition, classifies finite
values and unboundedness. A weak threshold can fail exactly at an
unattained infimum without spoiling this bisection.

## The canonical point really belongs to a QP chart

At a finite attained optimum, every feasible lifted optimal point
must have \(\eta=B(w)\). Otherwise all the finitely many ratios
would be strictly smaller than the optimum. This uses strict positivity
of every curvature multiplier and every denominator.

For two optimal points with the same integer assignment, the
midpoint identity gives the same nonpositive quadratic gap in every
normalized threshold residual. If that gap were negative, all ratios
at the midpoint would be strictly better. Hence their difference is
in \(\ker Q\). Both the full vector \(Qw\) and the value
\(B(w)\) are constant on that optimal set. The full PSD assumption
also handles the integer-continuous cross blocks.

The projected optimal set is a finite union of closed quartic chart
sets, and is convex by projection. The proof does not infer closedness
from convexity. Its unique minimum-norm retained point lies in one
chart, and it is the unique norm minimizer on that chart's subset.
The low-dimensional singleton formula supplies the required field and
height bounds.

Within that retained fiber, the lifted QP optimum is zero. Its
minimizers are exactly the actual optimal lifts. Since their \(\eta\)
coordinate is constant, the least-norm lifted selector also selects
the least-norm \(v\). This is the point represented by the QP chart;
there is no mismatch between the two canonical choices. Rational
chart evaluation introduces no new field extension, including for
the full common gradient.

## Attainment and recovery

Every integer assignment in the conditional integer box that has a
point at the global value has that value as its actual continuous
minimum. Therefore the canonical encoding bound applies to all and
only the fibers needed for the uniform box. It is not used for an
arbitrary nonoptimal quadratic sublevel.

Intersecting both boxes gives a compact mixed-integer domain.
Continuity of the finite maximum of positive-denominator ratios
makes its infimum attained. Equality of its value with the original
value therefore decides attainment, and successive integer bisections
preserve a genuine optimizer.

In a fixed optimal integer fiber, the same compact comparison tests
membership in the optimal set. Norm cuts involve only retained
coordinates, so the native range remains at most \(\rho+\ell\).
Affine cuts do not affect curvature. Since the retained kernel
already annihilates every denominator gradient, later calls do not
repeatedly enlarge the parameter.

The common full gradient can be approximated by rational affine
cuts. A rational right inverse of \(Q\) produces a vector with
the same gradient and hence the same quadratic value. It need not
have the fixed integer coordinates: equality of the quadratic value
depends only on equality under \(Q\). The equations and inequalities
in (11) consequently characterize the exact optimal fiber. Their
matrices on the remaining variables are rational; the algebraic
data appear only on the right-hand sides. The existing outward
rounding and Hoffman estimate therefore recover the specified
least-norm point.

All precision requests restart from the original containing box.
Queried algebraic values are compared and discarded, avoiding a
growing compositum. The subroutine nesting depth is fixed, and each
input length and precision bound has an absolute input exponent.
These facts preserve the claimed FPT time through the composition.

The shared reciprocal lift correctly handles an explicitly positive
denominator domain. Compact queries include its auxiliary coordinate;
boxing only the original open domain would not suffice.

## Boundaries and evidence

The zero-curvature counterexamples correctly delimit this proof.
For \(\max\{x^2,1\}\), the shared gradient varies on the optimal
interval. For \(\max\{(v-2)^2,2\}\), the canonical minimum-norm
optimizer is irrational at a rational optimum with no retained
native direction. Neither example disproves some other FPT algorithm;
both refute the field or gradient argument being used here.

The many-scenario example in the manuscript also checks directly:
the numerator is \(\sum_i v_i^2+u+|s|\), its smallest value at
\(u\ge\sqrt2\), \(v_i\ge u\), is \(2M+\sqrt2\), and the
positive denominator is maximized at two. The claimed value is
therefore \(M+\sqrt2/2\), while the unused constrained coordinate
gives an unbounded optimal set. This is a hand calculation, not a
new computational run.

The root read all seven sections, the separate field review, and
the complete single-numerator value and optimizer proofs. No
additional symbolic test duplicated the author's already completed
checks. The generalized fractional programming comparisons remain
limited as the manuscript states; no matching theorem being found
does not establish novelty. This review claims no new convexity,
fractional reformulation, or algebraic recognition principle.
