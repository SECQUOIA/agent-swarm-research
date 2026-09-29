# Scope review of the Hessian-span synthesis

Date: 2026-09-27. This is an independent review of
[the main-results synthesis](hessian-span-main-results.md), focused on its
scope, outputs, contribution claims and agreement with linked manuscripts.
It does not repeat the universal proof reviews or establish publication
priority.

**Finding.** No substantive overclaim or inconsistency was found in the
reviewed synthesis. Its principal table agrees with the statements in the
unbounded-value, continuous-optimizer, algebraic-witness and unbounded-integer
notes. A follow-up also checked the full unbounded mixed-integer optimization
result, which subsumes the earlier integer-only objective statement.
Three small clarifications were suggested; the author has applied all
three, and this reviewer checked their saved wording.

## Scope checks

- The continuous parameter counts the span of constraint Hessian matrices;
  the mixed-integer parameter counts their continuous blocks. Neither
  constraint count nor aggregate rank is silently substituted for this
  parameter. The continuous objective Hessian is excluded from the original
  parameter, and the larger bound for optimizer coordinates is retained.
- The running-time statements allow exponents depending on the parameters.
  They do not claim an FPT bound. The fully unbounded integer-witness bit
  bound matches [the integer extension](unbounded-integer-frontier.md) and
  [its independent review](unbounded-integer-review.md).
- The mixed-integer formulation and unbounded-integer results require joint
  convexity. The weaker bounded-integer NP consequence is correctly stated
  for convex continuous slices alone. The supplied slice-convex
  counterexample explains why these hypotheses cannot simply be merged.
- Exact integer preservation is restricted to bounded integer domains.
  Removing input bounds for decision is distinguished from preserving every
  feasible assignment by one finite MILP. The integer-parabola obstruction
  in [the applications note](hessian-span-applications-and-limits.md) matches
  this distinction.
- Coordinatewise algebraic recovery is distinguished from rational output,
  an exact original continuous vector displayed by the lifted MILP, and an
  efficient general multivariate sign certificate. The minimum-norm
  optimizer statement agrees with
  [the optimizer theorem](exact-convex-optimizer-recovery.md). The finite
  integer-only optimum and rational value statement agrees with
  [its objective review](integer-objective-review.md).
- The binary-circuit comparison preserves accepted binary assignments with
  continuous gate variables. It does not claim an ideal convex-hull
  formulation, or extend digit extraction to arbitrary bounded integers
  without new integer variables. The synthesis preserves both qualifications.
- The fitting model keeps sample parameters fixed and uses vector Euclidean
  residuals. Its Hessian-span bound and uniform-radius big-M construction
  match the applications note. No solver-performance or polynomial-time
  maximum-consensus claim is made.
- The prior-result table agrees with the recorded prior audits. It credits
  algebraic elimination, recognition, finite attainment and polyhedral
  approximation as established machinery. The stronger FPT guarantee in
  Del Pia's special case is acknowledged. The synthesis explicitly treats
  an unsuccessful equivalence search as insufficient to establish novelty.
  This review checked those comparisons against the linked audit records;
  it did not independently reinspect every external primary paper.

## Clarifications raised during review

1. **Resolved.** Replace the two uses of “fixed-parameter polynomial-time” by “polynomial
   time for each fixed parameter pair.” Although the surrounding text
   excludes an FPT claim, the former phrase is easily misread as one.
2. **Resolved, then superseded by the extension below.** Before listing
   continuous-dependent mixed-integer objectives as a next question, record
   the already established exact decision result for a
   supplied rational objective threshold. Appending that jointly convex
   quadratic row increases continuous Hessian span by at most one. Exact
   recovery, attainment and unboundedness classification were separate
   questions at that stage; threshold feasibility itself was already covered.
3. **Resolved.** The contribution comparison would benefit from explicitly naming the
   existing local fixed-count value-height proof. As recorded in
   [the package assessment](hessian-package-assessment.md), it already
   supplies the active affine-face reduction, regularized KKT elimination
   and limit formula. The present structural additions are the affine
   equations induced by active Hessian dependencies and the compressed
   multiplier representation. This sharpens the contribution without
   diminishing the extension to arbitrarily many native quadratic rows.

## Follow-up: full unbounded mixed-integer optimization

The follow-up review read
[the unbounded optimization manuscript](mixed-integer-attainment-frontier.md),
[its complexity review](mixed-integer-attainment-complexity-review.md), and
[its prior audit](mixed-integer-attainment-prior.md). This extends the scope
comparison beyond the initial integer-only objective statement.

The reviewed theorem permits a rational jointly convex quadratic objective
depending on both integer and continuous coordinates. Every native full
Hessian, including the objective Hessian, must be PSD. The objective
Hessian is excluded from the parameter that counts the span of continuous
constraint Hessians. For each fixed integer dimension and that span,
the stated output is exact infeasible, unbounded or finite status; in the
finite case it includes an optimal integer assignment, an algebraic optimal
value and algebraic continuous optimizer. No variable bounds or strict
feasibility assumption is imposed. No FPT bound or practical exponent is
claimed.

The updated saved synthesis retains all the following distinctions. No
scope error was identified in its new theorem row, proof outline, prior
comparison, limitation paragraph or revised research questions.

- Finite attainment itself is old: the prior audit identifies the directly
  inspected Bank–Mandel 1987 theorem for a broader rational quasiconvex
  polynomial class. The candidate advance is the effective exact algorithm
  and its uniform algebraic and witness bounds at fixed parameters.
- Recession elimination preserves attainable objective values. At most
  the original number of integer coordinates require coefficient-changing
  unimodular substitutions; intervening continuous eliminations only remove
  coefficients. This supplies the bit-control argument, rather than a
  claim that every original unbounded problem has a decreasing straight ray.
- Compact terminal projections give endpoint and value bounds. A separate
  isolated-optimal-value projection argument bounds an optimal integer
  assignment in the original coordinates. Simply lifting a small terminal
  assignment through all eliminations is not the size argument.
- The optimization step must preserve objective thresholds or actual
  optimizers. The amended manuscript supplies both a threshold-specific
  continuous radius and an alternative common radius for canonical fiber
  optimizers. A box retaining only an arbitrary feasible point on each
  integer slice does not justify the optimization conclusion.
- Continuous recovery applies the separately reviewed continuous optimizer
  theorem on a returned optimal integer slice. It supplies an exact
  optimizer; it does not assert that the complete mixed-integer vector has
  minimum norm among all mixed-integer optimizers.
- No sharp combined exponent for the full algorithm is given. This result
  does not extend the finite MILP formulation to preserving every
  unbounded integer assignment, or extend the PSD quadratic assumptions to
  arbitrary second-order-cone presentations.

These checks concern agreement with the linked statements and their
independent reviews. This scope audit does not independently reprove the
recession argument, the endpoint bounds or the imported Bank–Mandel
theorem.

## Verification record

The initial suggestions were clarity and attribution improvements, not
counterexamples to a stated theorem. No numerical or Lean verification is
claimed. The review
used targeted reads of the synthesis and its linked result, application,
prior-audit and review files; it did not run project-wide checks or inspect
CI. An inline `python -` check of this review file passed its ten local
links, final newline, control characters and trailing whitespace. That
document check does not verify any mathematical theorem.
