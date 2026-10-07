# Early sparse and feasible-domain review

Date: 2026-10-05 local / 2026-10-06 UTC. Reviewer: Sol.

This is an audit of the early manuscript, not approval of the paper or of
the source notes. I read the brief, independent-review brief, integration
contract and decisions, notation, the earlier sparse audit, and the actual
sections and Appendix C. I did not edit manuscript files, perform literature
research, rerun experiments, delegate, or run project-wide checks.

## Decision and snapshot

The sparse box argument and Appendix C are mathematically coherent, subject
to completion of the shared finite-tail and fallback dependencies. I found
no optimizer-loss error in their rounding, whitelist dynamic program,
pruning, deterministic-grid domination, or patch evaluation. Section 06 is
not ready for approval: Appendix D was absent throughout this audit, so its
theorems still have essential proof obligations. One actuator curvature
formula is false under its written assumptions and has a simple repair.

The author edited files during the first reads. The following hashes were
unchanged across the final two reads; all manuscript locators below refer to
this later snapshot, captured at 2026-10-06 02:52 UTC.

| File | Lines | SHA256 |
| --- | ---: | --- |
| `sections/05-sparse.tex` | 926 | `8294f707d601873a4ac3656246c69a370e085a5d1de6c465dabb444b7d707f24` |
| `sections/06-constraints.tex` | 739 | `cf4859647dbdcb4c0b120d606041ad687f940a26d5ef58d26a0ba31674e3b196` |
| `appendices/C-sparse.tex` | 272 | `28ca1ef81b4d15abfacd076ec1b604afea413f5e8e1d0e4eb54e324074a89d21` |
| `appendices/D-constraints.tex` | absent | no file to review |

The supporting model and counting section hashes were respectively
`30796e7df74e21c1ae7ca97527e3ae97c07b23c8f14691cd723dc0e278ee14d2`
and `eceb3aa3bd4b9d8e86b32c7f79901d51e2ba2d4ccc9ffdd30bc27f495ba42cbd`.
These supporting sections were read only for relevant contracts, not given a
full independent audit here.

## Findings requiring action

### 1. Blocking proof completion: Appendix D is missing

Locations: `06-constraints.tex:190`, `:273`, `:307`, `:325`, `:346`, `:458`,
`:549`, and `:653`; `C-sparse.tex:7`.

The section explicitly delegates the expanded decomposition, graph oracle,
approximate-cost pruning and closure, actuator theorem, simplex theorem,
and order theorem to Appendix D. The current outlines are useful, but do
not establish their finite-law margin constants, base-selected schedules,
closure depth, rare fallback probability, or feasible evaluation contracts.
This is missing proof, not evidence that the extensions are false. The
prewriting audit supports repairs and gives source locators, but cannot
replace proofs in the manuscript. The required checks for Appendix D are
listed below.

### 2. Medium: the actuator curvature choice can be negative

Location: `06-constraints.tex:428`–`:432`, used in the theorem at `:437` and
the work bracket at `:450`.

The premise only says that `L_q` is an upper bound on the pure second
derivatives of `q`. It permits a negative `L_q`, while the expression
`L=1+L_q+Lambda G_2` must be positive to apply the sparse theorem and to
make the claimed work bound meaningful.

For example, take one step, `a_0=0`, `g_0=0`, state and control intervals
`[0,1]`, and `q=-100(s_0^2+u_0^2)`, with unary bags and zero state costs.
The invariance condition holds. Every free pure second derivative is
`-200`, so the written assumptions allow `L_q=-200` and `G_2=0`. The
formula gives `L=-199`; with `sigma=1`, `n=2`, and `p=1`, the work bracket
is `4-199`, a negative upper bound on nonnegative work.

Repair: require `L_q>=0`, or use
`L=max{1,L_q+Lambda G_2}`. The source statement actually uses a nonnegative
bound on the absolute pure second derivatives:
`research-20261002/new-direction/smoothed-polynomial-actuator-dynamics.md:157`.
The adjoint reduction and the curvature estimate otherwise check out.

### 3. Major shared-interface dependency: current fallback statement does not provide the advertised algebraic format

Locations: `05-sparse.tex:109`, `:139`, `:787`; `06-constraints.tex:204`,
`:445`, `:540`, `:635`; compare `02-model.tex:260`–`:264` with
`03-counting.tex:518`–`:524` and `:541`–`:544`.

The model requires coordinates and value to be rational polynomial maps
of one isolated algebraic root. The current fallback theorem returns
separate coordinate root representations of one canonical optimizer, and
the explanatory paragraph explicitly says that no common primitive
element is required. Canonical selection prevents mixing optimizers, but
does not by itself supply the common-root format promised by the callers.

The integration contract already records a completed shared-root
supplement. Incorporate it into the shared theorem and its proof, with a
base-only multiplier `B` paying for construction and refinement. This is a
dependency owned by the shared-tools author, not a request to redesign the
sparse algorithm. A second related current statement, `03-counting.tex:534`,
says that the whole output length is at most `B`; for arbitrary added
coefficient precision the correct budget is `B poly_d(I+b)`, as the
integration contract also records.

### 4. Medium interface gap: the uniform-family lemma uses an unnecessarily restrictive coefficient-length premise

Locations: `06-constraints.tex:71`–`:73`, with applications at `:260`–`:273`
and `:410`–`:439`.

Substitution and the adjoint recurrence produce coefficients of length
`poly(I+b)`. They need not satisfy the literal bound `I+b`. Repeated powers
of a supplied rational coefficient in a fixed-depth composition already
increase its bit length by a constant greater than one. The family lemma
is therefore not directly applicable under the assumptions actually proved
in these reductions.

Repair: replace the premise by a stated polynomial bound on coefficient
length and production cost, whose exponent depends on the fixed degrees
and depth only. The conclusions remain unchanged after absorbing that
polynomial into the polynomial work factor. The tail constants are
independent of coefficient heights, so this repair does not affect the
pre-draw choice of `M` or introduce a circular precision schedule.

### 5. Minor contract corrections

- `05-sparse.tex:35`–`:41` does not explicitly require `n>=1`, although its
  maxima and its schedule divide by `W`. The prose at `:64`–`:65` recognizes
  the all-fixed case, but the algorithm at `:773` has no direct branch for
  it. State that the defined sparse instance has `n>=1`, and return the
  substituted rational point/value before constructing the schedule if no
  coordinate remains. The actuator theorem also needs this direct branch
  when every free coordinate is fixed.
- `05-sparse.tex:110`–`:114` and `:584`–`:585` allow a continuous value forced
  by a singleton hull, whereas `02-model.tex:243`–`:244` lists only original
  continuous bounds. Align the common output definition with the local
  descriptor. At `05-sparse.tex:641`–`:643`, qualify the claim about never
  fixing an artificial endpoint as a claim about the gradient rule; the
  singleton rule is separately justified by optimizer containment.
- `06-constraints.tex:24`–`:25` says that every class supplies (P1)–(P4), but
  `:597`–`:599` correctly says that (P1) fails for orders. Say that the
  classes supply or replace the four proof steps. Transport is a valid
  replacement for fixed outside feasibility; it does not make the outside
  domain independent of the bag values.
- `05-sparse.tex:902`–`:903` says that decision thresholds of the cited
  hardness reductions are not preserved at the stated noise scale.
  `09-boundaries.tex:491` proves a threshold-crossing bound under specific
  small-gap and witness assumptions, not that assertion about every cited
  hardness reduction. Keep the conclusion that a theorem for sampled
  instances does not contradict worst-case hardness of the original
  threshold problem; describe the proposition as an illustration unless
  the cited reduction's gap assumptions are explicitly checked.

## What the existing sparse proof establishes

The following conclusions are about the actual current text, conditional
on its stated valid curvature premise and shared theorems.

- **Clipped cells and whitelists.** `05-sparse.tex:179`–`:245` handles the
  clipped last interval, integer intervals down to spacing one, and then
  integer singletons. Every parent has at most two coordinate children,
  and a grid node lying in a cell is a corner. This proves
  `A_j=G_j intersect Omega_j`; it is not an assumed correspondence between
  row lists and the physical domain.
- **Consistent dynamic programming.** `:247`–`:305` assigns each factor and
  noise term once, conditions messages on separators, and uses running
  intersection to glue full assignments. Bounded tree degree makes the
  number of row operations linear in stored rows. Recomputing sums avoids
  subtracting infinities. The work argument at `:798`–`:824` does not
  multiply random adjacent table sizes.
- **Optimizer-preserving pruning.** `:319`–`:414` rounds every coordinate
  with its mean preserved, fixes grid nodes, and stays in all candidate
  cells simultaneously. Sequential Taylor expansion gives the global
  allowance `E_j=nLh_j^2/8` at higher degree. The cell lower bound holds
  on the current physical domain; all optimizers survive; deleted points
  have value above a feasible incumbent; each retained cell has one
  globally consistent feasible witness with gap at most `2E_j`. Earlier
  incumbents may leave the whitelist without becoming invalid.
- **Expected counts and atomic correction.** `:426`–`:529` conditions on
  original outside noise, uses attaining witnesses for coordinate upper
  curvature, and obtains intervals independent of all bag coefficients.
  At most three coordinate nodes are exceptional. The product count is
  `[4+(1+n/2)Lw_i/(2 sigma)]`, and `M>=2^J` pays for the finite-law atomic
  term. Retained adaptive cells are dominated by a deterministic complete
  grid; no independence of survival is used.
- **Closure and ties.** `:570`–`:693` forces original continuous bounds by
  sound derivative tests, records integer singletons, and tests the
  remaining Hessian on the full patch. Strict growth and active margins
  are used to prove stopping, not assumed for correctness. `:736`–`:821`
  fixes `B`, thresholds, cap, and then `M` before drawing once. Tied,
  singular, and positive-dimensional optima remain eligible for same-draw
  fallback.
- **Evaluation.** `C-sparse.tex:61`–`:172` supplies a capped-epigraph weak
  separation oracle with certified value/gradient errors, explicitly
  repairs the weakly feasible point, and compares against an eroded body
  by moving an optimizer toward a known interior ball. It therefore
  proves value accuracy even at a boundary optimizer. The modulus gives
  Euclidean distance. `:180`–`:215` uses sufficient extra coordinate
  precision for fallback distance, fixes the same integer labels, and
  gives a feasible rational point with a certified objective gap.
- **Quadratic specialization.** `C-sparse.tex:220`–`:272` correctly obtains
  a rational minimizer on every draw: a global minimizer with the fewest
  interior coordinates has a positive definite free principal block,
  since a null direction would reach a bound at unchanged value. Face
  enumeration costs `3^{n_c} N_Z poly(I+b)`; usual patches use exact convex
  quadratic programming. This proof permits ties and does not assume
  that all stationary points are isolated.

## Required Appendix D proof checks

### Graphs and actuators

The expanded bag statement `06-constraints.tex:179` must prove running
intersection using the constraint scopes, including dependent chains and
empty ancestor sets. It is not enough to count ancestor cardinalities.
With fixed degree and depth, explicit substitution has polynomial output
size and polynomial coefficient height; the ambient retained coefficients
remain independent after conditioning on dependent-coordinate noise.

For implicit charts, `:137` requires global brackets and a derivative
floor on the full real hull, including between integer labels. These
premises imply one smooth root and the displayed first-through-third
derivative bounds. The oracle at `:294` must turn root precision into
certified value, gradient, and Hessian precision, accounting for division
by the derivative floor. To obtain an operator-norm Hessian error
`epsilon_H`, evaluate entries to at most `epsilon_H/n` and symmetrize.
Checking positivity of an arbitrary input polynomial is not hidden inside
this oracle: the global chart and curvature premises remain promised or
explicitly certified, as stated at `:169`–`:174`.

The approximate pruning claim `:309`–`:332` has the right error accounting:
the sum of lower-cost errors is at most `E_j`; the feasible upper value is
`m_j^-+E_j`; witnesses have true gap at most `4E_j`; hence the comparison
factor becomes `1+n`. Give the induction and the original-domain
deterministic dominating count. Different root brackets per bag are safe
because the lower rational row costs approximate a unique chart at the
same rational coordinate tuple, not independently chosen algebraic roots.

For `:334`–`:346`, charge the enlarged witness radius as well as oracle
errors. A `4E_j` witness has distance at most
`h_j sqrt(nL/(2g_0))`; nevertheless `A=2+nL/g_0` still bounds its cell
distance by `A h_j`. The old cap then leaves gradient margin at least
`tau/4` and matrix margin at least `g_0/4` after charging two oracle errors
of sizes `tau/8` and `g_0/8`. Thus the asserted constants can be proved;
they should not be justified by citing the exact-cost proof unchanged.

The implicit active-margin tail must use the original polynomial graph
KKT equations. Positive reduced growth and nonzero chart derivative make
the bordered stationary Jacobian nonsingular; then a fixed-degree root
count is uniform in coefficient heights. A polynomial reduced objective
must not be assumed in this case. Growth transfer uses retained-coordinate
noise conditionally on dependent noise. Its degree/format bound and its
fallback factor must be selected before either part is sampled.

For `:215`–`:224`, prove ambient distance by tightening retained precision
with the encoded chart Lipschitz bound, and prove the model's feasible
objective-gap contract. An implicit graph may have no rational ambient
feasible point. Its exact feasible evaluation is rational retained
coordinates plus the unique algebraic dependent roots; a separate rational
ambient approximation is allowed to be infeasible. Fallback coordinate
enclosures must be lifted or repaired consistently.

The actuator adjoint identity `:410`–`:427` is valid for signed `a_k`, all
horizons, and ambient state noise. Its added terms are unary and preserve
the free-variable decomposition. After fixing Finding 2, prove coefficient
bit length by additive denominator lengths in the affine recurrence, and
use a uniform trajectory Lipschitz bound to meet the ambient Euclidean
evaluation promise at `:451`–`:454`. Invariance makes state bounds
redundant; additional path constraints and nonlinear state costs are
correctly excluded.

### Simplices

`06-constraints.tex:497`–`:527` has the right scope: disjoint unit
inequality/equality simplices, whole-block bags, native integers, block
Hessian upper bounds for correlated rounding, and derivative bounds on the
enclosing coordinate box for midpoint tests. Diagonal curvature alone
would not justify the rounding allowance.

Prove that each aligned cell is a cube cut by an integral budget and has
only cube-corner vertices. A mean-preserving distribution on these
vertices fixes grid coordinates and therefore preserves all whitelists.
Round blocks independently; the block Hessian bound gives the global
`nLh_j^2/8` allowance. Include the coarse levels whose block cell is the
whole simplex, and bounded child and corner incidence counts.

For the face count at `:563`–`:573`, conditional anchor noise leaves
independent remaining coefficients. Tight-face directions have squared
norm two; slack-face directions have squared norm one. Relative-interior
grid counts are bounded by `h^{-r}`, and the finite atomic correction must
be controlled by the same pre-draw level cap. Include zero-dimensional
faces and the native integer coordinates.

For closure at `:575`–`:587`, equality-simplex blocks use derivative
differences only. Their common equality multiplier has no sign condition.
Inequality blocks additionally use the one-coordinate tests to detect zero
coordinates and tight budgets. The positive anchor's derivative equals
the negative budget multiplier only in the inequality-block calculation;
make this distinction explicit in the proof. The metric factor
`Z^T Z` in the displayed Hessian test is necessary after anchor elimination.

The margin proof at `:589`–`:593` must count transformed finite tuples;
differences of independent grid coefficients are not independent grid
coefficients. Finish the relative-polytope evaluator with a rational
relative interior point, inner-radius bounds, exact feasible repair for
box-plus-sum slabs, and fallback precision adequate for physical distance
and a certified objective gap.

### Continuous and binary orders

The theorem at `06-constraints.tex:623` uses the selected stronger count
`C_0^p p_c! (p_c+1)[2+3 n_c Lbar/(4 sigma)]^{p_c} poly_d(I)`. Its purely
continuous specialization at `:647` is valid. Binary coordinates contribute
only the constant-base factor outside the bracket; arbitrary integer
levels are correctly excluded.

At `:655`–`:665`, the common threshold preserves every order relation,
every binary label, and every candidate cell. The full Hessian bound gives
`E_j=n_c Lbar h_j^2/8`. At `:667`–`:682`, prove the conditional transport
upper support, rather than asserting that transported fibers exhaust true
fibers. Along a free-knot direction all moving continuous coordinates have
rates in `[0,1]`, so squared speed is at most `n_c` independently of bag
size. The resulting interval width is at most `3 n_c Lbar h_j/2`.
Condition on all but one coefficient in each tested tie block. The remaining
block sums are independent, and their finite interval probabilities are
bounded by those of one noise marginal each.
Counting `r` distinct interior grid levels and ordered partitions gives
the factorial and `(p_c+1)` factors. This proof must include ties, endpoints,
cycles, and binary feasibility filtering.

The exposure order at `:684`–`:706` is correct and essential: fix all binary
hulls first, and then use the continuous slice LP. The supplied example
correctly refutes exposure in the unfixed mixed relaxation. For the LP
gap, the slice has zero-one vertices, and a failing active equality has
an opposite-face vertex in the face exposed by the true optimizer
gradient. The gap is `n_c`-Lipschitz in the gradient's infinity norm; the
threshold is therefore `n_c delta`.

The finite-law exposure-margin proof is still missing. It must count
nonsingular stationary roots on minimal order faces and, for an active
edge, vary its two noise coefficients at fixed sum. Count entire finite
sum fibers directly; do not assume a uniform conditional density. Include
the atomic `2/M` correction, infinite gaps for empty opposite faces, and
bound gaps. Closure must use the weighted metric `D^T D` or explicitly
charge the copy-basis norm in an unweighted test, retain inactive order
inequalities, and handle forced singletons and cycles. Evaluation needs a
rational relative interior point, explicit interval/order repair, and
physical Euclidean precision, including on fallback draws.

### TU scope

`06-constraints.tex:711`–`:727` correctly limits the claim to aligned
rounding for a continuous box cut by integral totally unimodular `A` and
integral `b`. After scaling an aligned dyadic cell, the right-hand side
remains integral, and appending coordinate bounds preserves total
unimodularity. With a full Hessian upper bound, a feasible mean of corners
gives `n Lbar h^2/8`; with bag-contained constraints this proves pruning.
It supplies no input-controlled expected retained count or complete TU
closure/tail theorem. The text correctly refrains from claiming one.
Rational right-hand sides require a compatible initial grid, and arbitrary
unfixed mixed integer ranges are outside this preliminary lemma.

## Checks actually performed

I read the current files with numbered lines, compared their interfaces
against the integration contract and prewriting audit, reconstructed the
rounding/pruning/count and convex-evaluation inequalities, and derived the
actuator counterexample exactly. I checked file presence, line counts, and
SHA256 hashes with `ls`, `wc -l`, and `sha256sum`. A targeted Python check
of this report's final newline, trailing whitespace, and code-fence parity
passed. The final manuscript hashes still matched the table, and Appendix D
was still absent. I did not compile the manuscript, run saved diagnostics,
rerun optimization experiments, inspect CI, or verify literature identities.
External citation identity and exact classical theorem scope remain with
the literature owner. Appendix D and the integrated shared-root fallback
need a fresh review once written; this report does not approve unseen
proofs.
