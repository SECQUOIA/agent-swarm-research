# Scope review of the algebraic bounds and Hölder consequences

Date: 2026-09-27. This is a fresh review of the additions to
[the main-results synthesis](hessian-span-main-results.md). It compares the
synthesis with the statements, limitations, and completed reviews of its
dependencies. It is not another proof audit of the general theorems and
does not establish publication priority.

The review covers the explicit algebraic degree and coefficient bounds,
the common field of a canonical optimizer, the Hölder exponent and
constant, and the mixed-integer penalty and outer-model consequences.
The final saved revision also includes the sharper multihomogeneous degree
bound and its separate sharpness theorem. No unresolved scope error was
found after the clarifications recorded below.

## Algebraic outputs and complexity

The explicit value result and
[ordered optimizer theorem](ordered-perturbation-optimizer.md) count the
span of the native constraint Hessians. The objective Hessian is excluded.
The synthesis preserves this convention and requires a convex objective
when invoking the optimizer theorem. Its canonical point is the unique
minimum Euclidean norm optimizer in the original coordinates.

The coordinate coefficient-bit bound is \(N^{O(h+1)}\). A bound on the
joint field is stronger than a collection of separate coordinate-degree
bounds; the synthesis correctly attributes it to one common ordered
limit and the primitive element argument. The objective value belongs to
the same field because it is a rational polynomial in the optimizer
coordinates. The table does not infer a product of coordinate degrees.

The final degree formula is

\[
 D(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns.
\]

It agrees with the [reviewed sharper-degree theorem](multihomogeneous-span-degree.md).
The maximum over supported active gradients is essential: the expression
need not increase with \(s\). The synthesis's example
\(D(3,3)=12\), with the support-three expression equal to eight, is
correct. Its \(D(n,h)\le3^n\) and fixed-\(h\) \(O(n^h)\)
statements are consistent with the formula. The \(n=0\) and \(h=0\)
conventions give degree one.

The sharper root count and the coefficient-height estimate come from
different arguments. A primitive minimal polynomial divides the earlier
height-controlled annihilator, so an integer factor-height bound preserves
\(N^{O(h+1)}\) coefficient bits while the degree argument improves its
degree. The synthesis attributes these two ingredients separately; it does
not suggest that an unquantified generic degree calculation alone controls
arithmetic precision.

The [sharpness note](multihomogeneous-degree-sharpness.md) establishes
existence of rational examples attaining this degree both for the value
and for the joint optimizer field. The synthesis keeps its exact parameter
range \(n\ge1\), \(0\le h\le n(n+1)/2\), and its favorable
conditions: positive definite objective, strict feasibility, compact feasible
set, and unique optimizer. Positive definite native constraint Hessians are
available when \(h>0\). It does not assert that every individual
coordinate has full degree. Its explicit exclusions of efficient extremal
coefficient construction and a matching height lower bound are appropriate.
No running-time lower bound follows from this sharpness result.

The synthesis retains the established
\(N^{\operatorname{poly}(h+1)}\) recovery running time. Improved output
bounds do not by themselves justify an equally improved exponent for the
composed recovery algorithm. Coordinatewise minimal polynomials and
isolating intervals are the established output. The synthesis explicitly
does not claim that this constructs a primitive generator, every coordinate
expression in that generator, or an efficient certificate for arbitrary
multivariate sign queries.

For an attained mixed-integer optimum, fixing an optimal assignment gives
a rational continuous fiber. Its value and canonical continuous optimizer
obey the continuous field-degree bound independently of the integer
dimension. This inference requires neither a small assignment nor joint
convexity, provided the continuous constraints and objective are convex
on each slice and attainment is assumed. In contrast, the height bound
uses the substituted fiber's input length. The synthesis correctly warns
that this length includes the assignment's bits and need not be polynomial
in the original input when the integer dimension grows. Its repeated-
squaring obstruction makes this distinction concrete.

The stronger unbounded mixed-integer algorithm continues to require joint
PSD Hessians and fixed integer dimension and Hessian span. No degree-only
statement is used to remove those hypotheses.

## Real data, bounded regions, and arithmetic bounds

The [qualitative geometry theorem](hessian-span-holder-geometry.md)
allows real data and any bounded trial region. Its constant can depend on
that region and on the data. It does not assert a global pure-power bound
on an unbounded region. The synthesis states this limitation explicitly.

The [constant-height theorem](hessian-span-holder-height-review.md)
requires rational data and an input box in the exact affine system. It
gives \(\log_2\max(1,C)\le N^{O((h+1)^2)}\). The synthesis
separates this arithmetic assertion from the real-data exponent statement.
For the boxed statement, including affine violations in the residual is
supported by the dependency's preliminary Hoffman projection. This does
not silently assume that a trial point already satisfies every affine row.

The exponent \(2^{-h}\) is uniformly sharp, as established by the
classical power-chain example. That sharpness does not concern the
coefficient-size bound or the practical size of a sufficient constant.
The synthesis does not claim either of those stronger forms of sharpness.

## Mixed-integer penalties and every-fiber outer models

The [consequence note](hessian-span-holder-consequences.md) assumes a
nonempty feasible set and a box on all original variables. The synthesis
keeps that fully boxed scope. Convex continuous slices suffice for its
uniform error bound and exact penalty. An infeasible slice may be repaired
in another integer slice using the positive residual gap and full-box
diameter; a feasible slice has a repair in the same slice. These two
arguments are not interchangeable, and the synthesis distinguishes them.

The penalty statement concerns the full minimizer set and requires an
objective Lipschitz on the whole boxed mixed-integer domain. A rational
quadratic objective can be indefinite here. A sufficient integer penalty
has \(N^{O((h+1)^2)}\) bits; the short lift uses exactly \(h\)
squaring equations, including the empty chain when \(h=0\). The
synthesis expressly states that this lift is nonconvex and gives no
solver-speed guarantee.

For the outer MILP, the stronger assumption is joint PSD of the full
quadratic Hessians. Its precision both excludes every infeasible integer
fiber and gives a same-slice repair within \(\tau\) for every projected
outer point. The model preserves feasible integer assignments and adds no
integer variables; its continuous output need not be exactly feasible.
The affine-objective loss depends only on the continuous coefficient
vector because the repair preserves the integer assignment.

The formulation-size statement is polynomial in \(N+p\), for fixed
\(h\), when \(\tau=2^{-p}\). It is not polynomial in the binary
encoding length of \(p\). The synthesis uses the correct formulation.
The existence and arithmetic control of repairs are distinguished from a
constructed facial-repair procedure or practical numerical calibration.
The synthesis also records a separate exact algebraic construction of a
nearest repair: translate a rational outer point to the origin and recover
the minimum-norm feasible point. This is supported by the consequence
review, and its complexity includes the outer point's encoding length.
It does not assert a numerically efficient implementation.

## Prior-art qualification strengthened during this review

The newer [original-source follow-up](hessian-span-holder-original-source-audit.md)
and [full Shor/conic comparison](hessian-span-holder-hu-li-comparison.md)
give a stronger assessment than a resemblance between proof techniques:
the qualitative exponent follows from a short span-decrease argument in
the full Shor lift combined with established partial-polyhedral facial
reduction and conic error bounds. The synthesis initially cited the first
prior audit without this explicit derivability comparison.

I requested that the synthesis record the stronger comparison. The author
added it to the geometry discussion and prior-results table and linked the
new source audits. The qualitative theorem is now described as a modest
structural refinement or corollary. The coefficient-encoding argument is
identified separately. This is an appropriate qualification; the absent
original Wang–Pang full-text comparison remains an unresolved literature
limit, not evidence of novelty.

Likewise, elimination, ordered perturbations, primitive elements, and the
classical quadratic KKT degree counts must remain attributed to existing
theory. The proposed addition concerns Hessian-span compression and its
nongeneric convex consequences. No new general elimination or root-counting
principle is supported by these notes.

## Verification record

This review read the synthesis, explicit value note, ordered optimizer
note and two proof reviews, qualitative geometry note, constant-height
argument and adversarial review, consequence note and review, and the
newer original-source and conic comparisons. For the final degree update,
it read the upper-bound note, degree prior audit, sharpness statement and
limitations, and the upper-bound and primitive-value review conclusions.
The general mathematical
proofs and source inspections remain dependencies; I did not claim to
repeat them. A separately delegated narrow review of the geometry and
consequence scope found no substantive overclaim. Its suggested clarifications
of nonemptiness, the whole-domain Lipschitz assumption, and precision bits
were incorporated and reread. No numerical test, Lean formalization,
project-wide check, or CI inspection was run for this scope review.

The final saved synthesis was reread after the author confirmed its
sharper-degree revision. An inline Python command checked only this review
for local-link existence, paired math delimiters, control characters,
trailing whitespace, and final newline. These document checks validate
formatting and references, not the mathematical theorems.
