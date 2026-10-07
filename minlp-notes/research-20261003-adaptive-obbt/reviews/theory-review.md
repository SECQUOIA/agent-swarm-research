# Independent review of adaptive OBBT theory

Review date: 2026-10-03. Status: **PASS for the stated mathematical results
and reference certificate workflow, after the corrections below.** This is
not an endorsement of universal topic completion, publication novelty,
benchmark performance, or certification of an external solver.

## Scope and method

I independently read the three theory manuscripts, `theory/certificates.py`,
`theory/certified_driver.py`, and their targeted check scripts, together with
the relevant operator assumptions in the earlier iterated-OBBT study. I
derived small counterexamples to plausible stronger claims and wrote a separate
[exact review diagnostic](check_theory_review.py). The mathematical checks
use rational arithmetic; they are not empirical runtime evidence.

## Findings requiring correction

1. **An exact basis verifier initially accepted floating residual arithmetic.**
   The proposed point `(1,1)` was accepted for the three inequalities
   `x<=1`, `y<=1`, and `10^16 x+y<=10^16` when the last coefficient was passed
   as `1e16`. The exact last residual is `1`, but the floating sum discarded
   it. Rationalizing only the proposed basis did not protect the nonbasis
   residual checks. The author was asked to reject floating inputs at the
   public verifier boundary or convert every input before arithmetic. The
   separate diagnostic retains this reproducer and its exact-integer variant.
   **Resolved:** all verifier inputs now pass through a strict integer or
   `Fraction` reader. Both versions of the infeasible proposal are rejected.

2. **Rejected callback entries need a place in the effort bound.** The proof
   of the ledger inequality assumes every increment of enhancement work
   belongs to an admitted or reserved operation. Repeated admission checks
   after exhaustion can otherwise exceed the bound even when no enhancement
   is admitted. The corrected note states this condition and adds a separate
   measured term `J` when this overhead cannot be reserved. That correction
   is sufficient; an unbounded `J` precludes a total-overhead guarantee.

3. **A directly constructed protected-box object needed verification.** The
   first version checked witnesses only through the factory. The revised
   `ProtectedBox.__post_init__` checks exact feasibility on its own box and
   support of every face. Direct construction now has the same invariant.
   The factory separately checks the outer domain and requested cutoff.
   **Resolved:** the independent counterexample is rejected by both entry paths.

4. **Numerical model identity is not node-local row provenance.** The
   implementation compares rational row and objective data. It cannot infer
   whether those rows are valid for a particular original model or node.
   **Resolved:** the manuscript and `Model` contract now state that this
   separate validity and locality obligation belongs to the caller. The
   native solver does not use these protected boxes as a permanent stop rule.

## Mathematical assessment

The ledger inequality is valid on the enhanced trajectory under its stated
cost assumptions. The independent-baseline scheduling and serial-rescue
bounds are valid in their explicit preemptible work model. None compares
the native work on a modified search trajectory with the independent
baseline trajectory. The abstract branching-order counterexample correctly
shows why that extra comparison cannot follow from a ledger alone.

R2's one-round witness bounds and R3's protected-box induction are sound.
The crucial check is feasibility in the relaxation rebuilt on the protected
box, not just on the original outer box. Lifted isotonicity then preserves
all face witnesses through every permitted coordinate update. The objective
ceiling follows from retaining one objective witness, with no assertion of
its nonlinear feasibility. R4's cutoff threshold, same-domain mixing, and
pairwise convex-pool construction have the stated scope. The pairwise
construction follows from the two affine constraints on its coefficient LP.

For R5, uniform sensitivity gives `d_(k+1)<=M d_k`. The majorant inequality
`d+Me<=e` bounds every finite partial sum and hence total future movement.
Subtracting the exact completed first displacement gives `e-d`. Replacing
the residual by an upper bound does not authorize subtracting that upper
bound. The text correctly distinguishes a verified residual from displacement
observed during selective or interrupted OBBT. The fixed-point cutoff
perturbation bound also follows under its stronger uniform estimate.

The fixed-matrix dual envelope, basis-cell certificate, retained-witness
bound, and finite-cell derivative bound in the constrained note are sound.
The sign distinction matters: a cutoff-row dual multiplier yields a lower
bound on the support reduction available after an incumbent improvement;
a retained primal witness yields an upper bound on the possible reduction.
A zero old multiplier is not proof that later tightening will be useless.

The fixed-matrix qualification is essential. Rebuilding McCormick rows
changes their coefficients, so an affine-right-hand-side basis formula
cannot simply be reused for varying boxes. The note states this limitation.
For a finite certified cell cover of a convex region, agreement of exact
support values at boundaries and integration along a segment establish the
uniform comparison matrix. A single observed active cell does not.

I checked the equality example algebra independently. On `y=-x`, the
expanded-square McCormick objective becomes `2t^2+4r|t|-2r^2`, giving
`min(r,sqrt(2r^2+U/2)-r)`. The zero-cutoff factor is `sqrt(2)-1`, and the
positive-cutoff radius limit is `sqrt(U)/2` when the starting radius is at
least that value. Eliminating the equality gives `4x^2`, whose exact convex
relaxation reaches that radius immediately. The example correctly attributes
the rate to the formulation and relaxation, not the original problem alone.

C5's nonlinear feasible-repair extension is also sound. The objective error
and cutoff bound `f(x)`; a uniform one-sided change bound then bounds the
repaired objective. Feasible quadratic growth bounds the distance of the
repair from the optimizer, and the triangle inequality supplies the stated
width bound. Nesting and the scalar recurrence justify the positive-slack
upper floor. The proof requires all four uniform assumptions, including that
the repair stays in the growth neighborhood.

For the explicit graph `y=x^2`, I checked the repair and constants over the
whole stated box: the graph secant gap is at most `w^2/4`, the bilinear gap
at most `w_x*w_y/4`, the objective Lipschitz constant is `165/256`, and the
feasible growth constant `63/64` is valid. Thus `q^2=181/252` and the rational
rate bound `15/16` at width at most `1/8` follow. The 141 finite checks
supplement these inequalities; sampling alone would not certify them.

The standalone driver verifies every primal row, nonpositive minimization
dual multiplier, exact dual stationarity, and equality of primal and dual
objectives before applying a complete Jacobi round. This proves its endpoint
updates for the stated rational relaxation. A rebuilt face-witness check
then proves a fixed box. Failure discards the incomplete round while retaining
previous completed rounds. The optional objective proposal needs only primal
feasibility because it supplies an upper ceiling, not a lower-bound proof.
No finite termination or wall-clock budget is proved. A solver's inability
to propose an optimum remains inconclusive, including when its numerical
status reports infeasibility.

## Certificate boundaries tested independently

- **One frozen round versus rebuilt rounds.** For the finite LP relaxation
  of `w=x^2` on `[-1,1]` with cutoff `w<=0`, the points `(-1/2,0)` and
  `(1/2,0)` certify the first round's endpoints. They fail the relaxation
  rebuilt on `[-1/2,1/2]`. Repeated rebuilds halve the interval. Treating
  these original witnesses as a permanent protected interval would be false.
- **Cutoff reuse.** Endpoints `(+/-1/2,1/4)` protect `[-1/2,1/2]` only while
  the cutoff remains at least `1/4`. Tightening it to zero invalidates their
  support. Convexly mixing witnesses with a lower-objective anchor retains
  feasibility on the frozen box; the resulting hull must still be rechecked
  before it is treated as protected.
- **Relaxation versus original feasibility.** The extra point `(0,-1/4)`
  is feasible on that protected finite square LP. Its objective gives a
  relaxation-value ceiling of `-1/4`, although every true square value is
  nonnegative. It is not an incumbent or a proof of original feasibility.
- **Domain, row, and integer scope.** A descendant box excluding a protected
  face cannot reuse the certificate. Adding the valid square row `w>=0`
  excludes the negative lifted witness. Integer rounding turns the protected
  half interval into `{0}` and does not preserve its fractional faces. A
  continuous-LP certificate therefore does not cover arbitrary native
  propagation, stronger cuts, or integer rounding without an additional
  preservation argument.
- **Observed versus uniform contraction.** Two continuous monotone maps
  satisfying `0<=F(s)<=s` share the width history `1,9/10,899/1000` but then
  either stall or shrink to zero. Extrapolating the observed decrement ratio
  `1/100` predicts at most `1/990` further movement after the first step;
  the shrinking map moves `9/10`. Both can define valid nested interval
  relaxations of the singleton feasible set `{0}`. This refutes the inference
  from history alone, not every structure-specific screening method.
- **Tail-majorant arithmetic.** The inequality `d+Me<=e` can hold with
  `rho(M)=1`: take `M=diag(1,1/2)`, `d=(0,1)`, and `e=(5,2)`. Its finite
  partial sums stay below `e`. A checker for this inequality does not
  establish that `M` uniformly bounds the actual operator or that an observed
  displacement bounds its exact residual.
- **Atomic driver and signed directions.** An independent exact proposal
  oracle proves a fixed interval with a negative lower endpoint and nonzero
  objective constant. Reusing the lower-direction proof for the upper
  direction rejects the incomplete round. A missing proposal on an
  infeasible relaxation returns `inconclusive`, not certified infeasibility.

## Attribution and unresolved scope

I independently read the relevant primary sources. Feasible-point filtering,
near-bound filtering, Lagrangian variable bounds, and incumbent-triggered
reuse are established ingredients in Gleixner et al., Sections 2.2 and 3.2.
[Primary report](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf).
Affine optimizers, affine values, and critical regions for fixed-matrix
parametric LPs are established in Borrelli, Bemporad, and Morari, Section 3.2,
equations (8)–(11).
[Author-hosted paper](https://cse.lab.imtlucca.it/~bemporad/publications/papers/jota-mplp.pdf).

These facts support the manuscript's classical-attribution boundaries.
They do not establish publication priority for the protected-box packaging,
the exact certificate implementation, or any related result. The conditional
nonlinear repair theorem is a developed extension; it does not supply an
automatic method for finding its repair and growth constants for arbitrary
models. An inexpensive general uniform comparison-matrix constructor is also
absent. No theorem here proves a positive net runtime benefit or a universally
best choice between tightening, cuts, and branching. Those limits must remain
visible in any completion claim.

## Targeted commands

The following commands were actually run from the repository root:

```text
python3 research-20261003-adaptive-obbt/reviews/check_theory_review.py
python3 research-20261003-adaptive-obbt/theory/check_effort_allocation.py
python3 research-20261003-adaptive-obbt/theory/check_constrained_obbt.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python research-20261003-adaptive-obbt/theory/check_remaining_benefit.py --with-lp-proposals
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python research-20261003-adaptive-obbt/theory/check_certified_driver.py
```

All passed after correction. The independent diagnostic checks 3,360 exact
nested McCormick points, 65 separately enumerated cutoff LPs, 1,089 pairs
across the changing basis cells, 50 matrix partial sums, seven scope cases,
two arithmetic rejections, three independent driver cases, and the explicit
observed-ratio and bookkeeping counterexamples. The author's checks cover
19,683 ledger traces, 8,000 scheduling traces, the constrained propositions
including 141 graph-repair cases, 12 remaining-benefit check groups, eight
discovery fixtures, ten driver fixtures, and five rejected LP proofs.

Six discovery fixtures yielded certificates and two contracting fixtures
returned inconclusive. The driver preserved positive residuals on its
contracting examples; it did not claim exact closure from a small numerical
change. These are targeted correctness results. No project-wide verification
or CI inspection was run.
