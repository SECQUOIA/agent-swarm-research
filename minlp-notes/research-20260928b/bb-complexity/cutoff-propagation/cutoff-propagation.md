# Objective-cutoff propagation and the node complexity of spatial branch-and-bound

Date: 2026-09-29. Workstream `cutoff-propagation/` of the
[program](../PROGRAM.md). Status: revised after an
[independent review](../../reviews/cutoff-review.md), which found no
counterexample to any numbered result, and a [recheck](../../reviews/cutoff-recheck.md) of that revision, which
found no numbered result false; Section 11 lists the changes. The changes of
Section 11.2 have not been re-reviewed. It answers the
scope question left open by the
[spatial review](../../reviews/spatial-bb-review.md) (Section 1.3, Fix 2) and by
Corollary 8.1(c) and Open problem 4 of the
[constrained note](../spatial-constrained/instance-dependent-node-complexity.md):
how far can interval propagation of the objective cutoff change the node counts
predicted by the relaxation-gap theory? Computations are floating-point
illustrations, not certified counts. Scripts and logs are in this directory.

## Summary

Solvers propagate the constraint `f(x) <= UBD - eps` through the expression
graph of `f` with interval arithmetic (feasibility-based bound tightening,
FBBT). The spatial review showed that on the scout's instance `t^2 - 2t^4` this empties
the root with no relaxation solved, so the `log(1/eps)` lower bound of the
relaxation-gap theory does not describe such solvers. This note gives a
quantitative theory of the combined scheme.

**Main message.** Cutoff propagation run to its fixed point is itself a node
bound, `pi_D(C)`, which depends on the chosen expression graph `D` and not only
on `f`. Whether it changes the `eps`-exponent is decided by the first-order
dependency loss of that representation at the optimal set.
- The loss is zero for "one-sided" representations. Then propagation certifies
  optimality with a number of nodes independent of `eps`: proved under the
  hypotheses of Theorem 3.8 and observed in every one-sided example.
- The loss is first order in the box width when the term gradients cancel
  without a dominant term. If no term dominates in any coordinate direction
  (CND), every lower bound of the relaxation-gap theory that uses (V) near the
  optimal set survives. If only the whole-cube condition holds (ND1), the
  `log(1/eps)` bound at isolated minima and the `eps^(-1/2)` bound on
  transversal optimal curves survive.

The same function with the same relaxation can fall on either side:
`h(x - y)` written through the node `s = x - y` needs one node for every
`eps`; the expanded polynomial needs `Omega(eps^(-1/2))` nodes with or without
propagation (and `Theta(eps^(-1/2))` observed). When propagation is exact, the
cost can move from nodes to propagation rounds. A heuristic fits every computed
example but is not proved (Section 3.3):
- the fixed point needs `Theta(eps^(-1/2))` rounds when some base node has at
  least two terms whose nonzero derivatives cancel at the minimizer;
- it needs few rounds when no base has such a cancellation, for example when
  all terms are stationary there, or when the minimizer is an end of a lifted
  range where `f` grows linearly.

Proved: at least `Omega(eps^(-1/2))` HC4 rounds for an expanded quadratic, and
`O(log log(1/eps))` rounds for the review's lifted form of `t^2 - 2t^4`.

Proved here (complete proofs; checked by an independent review, which found
no counterexample, and by a recheck of the first revision (Section 11.1);
the Section 11.2 changes are not re-reviewed):

1. **Model (Section 1).** Fixed-point cutoff FBBT on a factorable DAG is
   equivalent to a node bound `pi_D(C) = min{c : Z*(C,c) ≠ ∅}` plus a
   contraction. Here `Z*(C,c)` is the greatest hull-consistent lifted box, and
   `F_lo(C) <= pi_D(C) <= min_C f`, where `F_lo` is the natural interval
   extension. Any schedule, with any number of rounds, removes at most what the
   fixed point removes (Lemma 1.1 and Proposition 1.4; standard constraint
   propagation facts, restated with proofs).
2. **Hybrid certificates (Section 2).** Every run combining relaxations and
   cutoff propagation produces a family of boxes in which each point is
   certified either by the relaxation-gap condition (V) or by propagation.
   Unlike OBBT, consecutive propagation rounds can be merged into one frame
   (Lemma 2.1). No lower bound can hold for every representation of `f`
   (Proposition 2.3).
3. **Exact propagation (Section 3).**
   - For a flat sum of univariate terms, the fixed point is nonempty exactly
     when some sub-box `U'` has
     `Phi(U') = sum_j min_{U'} t_j + max_j [max(t_j at the two endpoints) - min_{U'} t_j] <= c`
     (Theorem 3.1). The random checks agree in 450 of 450 instances.
   - One-sided representations are exact (Corollary 3.3). For separable sums
     the loss is purely cross-coordinate (Corollary 3.5), and exactness holds
     when the sublevel set is box-like in the lifted coordinates that the DAG
     exposes (Proposition 3.6).
   - Local exactness gives node counts independent of `eps` for idealized
     propagation (Theorem 3.8; the "exact bound, no cluster" principle is
     known, and what is new is its application to `pi_D`).
   - The price can be rounds: at least `(pi/8 - o(1)) a eps^(-1/2)` HC4
     rounds for `s^2 - 2as + a^2`, whose two term derivatives cancel at the
     minimizer (Proposition 3.9; observed `pi a eps^(-1/2)`). It is only
     `O(log log(1/eps))` for the lifted form `u - 2u^2`, `u = t^2`, of
     `t^2 - 2t^4`, whose minimizer is the end `u = 0` of the lifted range
     (Proposition 3.10).
4. **Loss and lower bounds (Sections 4–5).**
   - A witness lemma bounds what any propagation schedule can remove (Lemma
     4.1). For flat sums, `pi_D(C) <= F_lo(C) + max_j width_C(t_j)`: the fixed
     point gains at most the width of one term over forward evaluation
     (Corollary 4.2).
   - Under a coordinatewise no-dominant-term condition (CND), points removed
     by propagation satisfy (V) with `alpha_F = D0/(2 n s0)`. Hence every lower
     bound of the relaxation-gap theory that uses (V) near the optimal set
     holds for hybrid runs with `alpha_eff = min(alpha, alpha_F)`, for example
     `|P| >= 2^(-n) N_inf(E(eta), 2 sqrt((eps+eta)/alpha_eff))`
     (Theorems 5.1–5.2). Here `|P|` counts leaves plus `2n` per propagation
     phase. Near stationary points, CND even confines every removal to boxes
     of width `O(m + eps)` (Proposition 5.1a).
   - Under the weaker cube condition, propagation can certify long thin boxes
     (observed), but the `log(1/eps)` bound at isolated nondegenerate minima
     survives (Theorem 5.4), and so does `eps^(-1/2)` on optimal curves
     transversal to all coordinate hyperplanes (Theorem 5.5).
5. **Computations (Section 7).** Interval HC4 with alphaBB bounds on 1-, 2-
   and 3-variable instances confirm each prediction. Propagation to the fixed
   point collapses the one-sided representations to 1 node (1D,
   `h(x-y)`, `h(x-y) + kappa (x+y-1)^2`, a 3D line) and to 17 nodes (2D
   `t^2 - 2t^4`). It leaves the expanded representations of the same functions
   at their relaxation-theory rates: `log(1/eps)` with prefactor `~ kappa^(-1/2)`,
   `eps^(-0.51)` in 2D and `eps^(-0.54)` in 3D. Where some base has cancelling
   term derivatives at the minimizer, bounded propagation (3 or 10 rounds per
   node) left the growth rate of the propagation-free runs unchanged in the 1D
   instances and on `linediag`; on the 3D line the tested range is too short
   to decide. For `t^2 - 2t^4`, where no base has cancellation, 10 rounds
   already reach the fixed point and its `O(1)` count.

Open (Section 9): bounded-round propagation in the exact case (Conjecture
3.11); whether face-type loss can beat `eps^(-p/2)` for optimal sets of
dimension `p >= 3`; constrained problems; general (non-flat) DAGs.

### Result status

| Item | Content | Status |
|---|---|---|
| Lemma 1.1, 1.2, Prop. 1.4 | greatest hull-consistent box, also for HC4's partial steps; monotonicity; `Z ⊆ Z0(Π_x Z)`; `pi_D` as a node bound | proved; known in constraint propagation (Section 8) |
| Lemma 2.1, Theorem 2.2 | hybrid leaf-and-piece family (proof corrected in revision); transfer principle | proved |
| Prop. 2.3 | no representation-free lower bound | proved |
| Theorem 3.1, Remark 3.2 | characterization of the fixed point for flat sums of univariate terms | proved; checked on 450 random instances |
| Cor. 3.3, 3.5, Prop. 3.6 | one-sided exactness; separable identity; lifted box-likeness | proved |
| Theorem 3.8 | `eps`-independent node count under local exactness (idealized propagation) | proved; the principle is known (Du–Kearfott, Wechsung et al.) |
| Prop. 3.9, 3.10 | round counts: `Omega(eps^(-1/2))` for HC4 on the expanded quadratic; `O(log log(1/eps))` for the lifted form of `t^2 - 2t^4` | proved |
| Heuristic 3.8a | `Theta(eps^(-1/2))` rounds iff some base has cancelling term derivatives at the minimizer | heuristic; fits all computed examples, not proved |
| Conjecture 3.11 | bounded rounds do not change the growth rate when some base has cancelling term derivatives at the optimal set | conjecture; numerics agree except one undecided case |
| Lemma 4.1, Remark 4.1a, Cor. 4.2, Example 4.3, Lemma 4.4 | witness lemma (also for any DAG below a flat root sum); one-term gain; `x^2 - 2xy + y^2`; first-order loss | proved |
| Theorems 5.1, 5.2, Prop. 5.1a | vertex localization under CND; the (V)-based relaxation lower bounds survive; two-sided localization | proved |
| Theorems 5.4, 5.5 | face-type loss: `log(1/eps)` at isolated minima; `eps^(-1/2)` on transversal curves | proved |
| Section 9, item 2 | face-type loss for `p >= 3` | open |

## 1. A model of cutoff propagation

### 1.1 Representation and propagation

**Representation.** A factorable representation `D` of `f` is a directed
acyclic graph whose nodes are the variables `x_1..x_n`, constants, and
operation nodes `w_k = op_k(w_a, w_b)` or `w_k = phi_k(w_a)`. The binary
operations are `+` (also n-ary sums with coefficients) and `*`; the unary
functions `phi_k` (powers, `exp`, `log`, `abs`, ...) are continuous on a closed
domain that contains the forward interval images below. The last node is the
root, whose value is `f(x)`. The **elementary constraints** are
`E_k = {w : w_k = op_k(w_children)}`, together with the cutoff constraint
`w_root <= c`.

**Boxes.** For a box `C ⊆ X0` of the variables, `Z0(C)` is the lifted box in
which each variable has its interval from `C` and each operation node has its
natural interval extension (forward evaluation). `F_lo(C)` is the lower end of
the root interval of `Z0(C)`. It is inclusion isotone: `C' ⊆ C` implies
`Z0(C') ⊆ Z0(C)`.

**Revise operators.** For a lifted box `Z` and an elementary constraint `E`,
the exact revise `rho_E(Z)` replaces the coordinates of the nodes of `E` by
the box hull of `E ∩ Z`, and returns the empty set if `E ∩ Z = ∅`. The cutoff
revise intersects the root interval with `(-inf, c]`. A **propagation run** is
any finite or infinite sequence `Z_{k+1} = rho(Z_k)` started at `Z0(C)` (or at
`Y ∩ Z0(C)` for a lifted box `Y` of inherited bounds), where
each step `rho` satisfies `rho_E(Z) ⊆ rho(Z) ⊆ Z` for some `E` (or is the
cutoff revise). This allows forward-only and backward-only steps, partial
updates, and any schedule. HC4, the FBBT of Couenne, BARON and SCIP, and the
code in [`fbbt.py`](fbbt.py) are of this form in exact arithmetic. A run is
**fair and exact** if every step is an exact revise and every revise is applied
infinitely often.

**Hull consistency.** A lifted box `Z` is hull-consistent (for cutoff `c`) if
`rho_E(Z) = Z` for every `E` and `Z_root ⊆ (-inf, c]`. For a closed `E ∩ Z`
this means that each endpoint of each interval of `E`'s nodes extends to a
point of `E ∩ Z`. It does **not** mean that every interior value extends
(Section 3.1 shows why this matters). The empty box is hull-consistent.

**Lemma 1.1 (greatest hull-consistent box).**

(a) Among the hull-consistent boxes contained in `Z0(C)` there is a greatest
one, `Z*(C, c)` (possibly empty).

(b) If a run with cutoff `c` starts from a lifted box that contains a
hull-consistent box `D`, then `D ⊆ Z_k` for all `k`. In particular every run
from `Z0(C)` keeps `Z*(C, c) ⊆ Z_k`.

(c) Every fair exact run converges to `Z*(C, c)`: `∩_k Z_k = Z*(C, c)`. If
`Z*(C,c) = ∅`, some `Z_k` is empty.

*Proof.* Each `rho_E` is monotone: `Z ⊆ Z'` implies `E ∩ Z ⊆ E ∩ Z'`, so the
hulls are nested and the other coordinates are unchanged.

(a) Let `Zh` be the box hull of the union of all hull-consistent boxes
`D ⊆ Z0(C)`. For each such `D`, `D = rho_E(D) ⊆ rho_E(Zh)`. So the box
`rho_E(Zh)` contains every `D`, hence contains `Zh`; since `rho_E(Zh) ⊆ Zh`,
equality holds. The root interval of `Zh` lies in `(-inf, c]` because each
`D_root` does. So `Zh` is hull-consistent and is the greatest such box.

(b) Induction: if `D ⊆ Z_k`, then `rho(Z_k) ⊇ rho_E(Z_k) ⊇ rho_E(D) = D`,
and the cutoff revise keeps `D` since `D_root ⊆ (-inf, c]`.

(c) The `Z_k` are decreasing compact boxes; let `Z_inf` be their intersection.
*Continuity:* for decreasing compact boxes `Y_k` with intersection `Y`,
`rho_E(Y) = ∩_k rho_E(Y_k)`. Indeed `E` is closed, so `E ∩ Y_k` are decreasing
compact sets with intersection `E ∩ Y`. If `E ∩ Y = ∅`, some `E ∩ Y_k` is
empty. Otherwise, for each node `v` of `E`, the maximum of `w_v` over
`E ∩ Y_k` decreases to its maximum over `E ∩ Y` (take maximizers and a
convergent subsequence), and likewise for minima. By fairness each `E` is
applied at infinitely many steps `k`, where `Z_{k+1} = rho_E(Z_k)`. Along those
steps, `Z_inf ⊆ ∩ rho_E(Z_k) = rho_E(Z_inf)`, so `rho_E(Z_inf) = Z_inf`. The
cutoff revise is applied infinitely often, so `Z_inf,root ⊆ (-inf, c]`. Thus
`Z_inf` is hull-consistent and `Z_inf ⊆ Z*`; with (b), `Z_inf = Z*`. If
`Z* = ∅`, the decreasing compact `Z_k` have empty intersection, so one of them
is empty. □

**HC4 steps.** Part (c) was stated for exact revises, but HC4 (and
[`fbbt.py`](fbbt.py)) uses partial steps:
- the forward step of `E_k` replaces the parent interval `W_k` by
  `W_k ∩ op_k(Z_children)`, where `op_k(Z_children)` is the exact image, an
  interval;
- the backward step replaces each child interval by the hull of the projection
  of `E_k ∩ Z` onto that child.

Both are run steps in the sense above. The projection of `E_k ∩ Z` onto the
parent is exactly `W_k ∩ op_k(Z_children)`, and the unchanged coordinates
contain their projections. Both are also monotone and continuous from above,
by the argument of (c). A box fixed by the forward and the backward step of
`E_k` is fixed by `rho_{E_k}`: its projection onto the parent is
`W_k ∩ op_k(Z_children) = W_k`, and its projections onto the children are
fixed by the backward step. Hence the limit of a fair HC4 run (every forward,
backward and cutoff step applied infinitely often) is a common fixed point.
It is therefore hull-consistent, and equals `Z*` by (b). So Lemma 1.1(c) and
Proposition 1.4(b) hold for HC4, and the `fix` mode of `fbbt.py` computes
`pi_D` up to its stopping tolerance.

Belotti, Cafieri, Lee and Liberti describe the FBBT limit as the greatest fixed
point of a monotone deflationary operator (Section 8). Lemma 1.1 is that fact
for arbitrary schedules and weaker revise steps. Convergence need not be
finite (Belotti et al.; the repository's
[doubly exponential example](../../../results/fbbt-doubly-exponential-convergence.md)).

**Lemma 1.2 (monotonicity and closedness).**

(a) `C' ⊆ C` implies `Z*(C', c) ⊆ Z*(C, c)`.

(b) `c' <= c` implies `Z*(C, c') ⊆ Z*(C, c)`.

(c) For fixed `C`, the sets `{c : Z*(C,c) ≠ ∅}` and, for `y ∈ C`,
`{c : y ∈ Π_x Z*(C, c)}` are closed. `Π_x` denotes the projection onto the
variables.

(d) Every hull-consistent box `Z` whose constant nodes have their values
satisfies `Z ⊆ Z0(Π_x Z)`. This includes every hull-consistent box inside
some `Z0(C)`, where constants are points. Constants carry no elementary
constraint, so a box that widens them can be hull-consistent without the
inclusion.

*Proof.* (a) `Z*(C', c)` is hull-consistent and lies in `Z0(C') ⊆ Z0(C)`.
(b) A box hull-consistent for `c'` is hull-consistent for `c`. (c) Let `c_k`
decrease to `c̄` with `Z*(C, c_k)` nonempty (respectively containing `y` in its
projection). By (b) these are decreasing compact boxes; their intersection is
nonempty (respectively has `y` in its projection, since the projection of an
intersection of decreasing boxes is the intersection of the projections). The
continuity argument of Lemma 1.1(c) shows the intersection is hull-consistent
for `c̄`, so it lies in `Z*(C, c̄)`. (d) Go through the nodes in topological
order. Variables and constants have the same intervals on both sides. For an
operation node
`k`, the endpoints of its interval `W_k` are attained by points of
`E_k ∩ Z`, so `W_k ⊆ op_k(Z_children)`, the exact image. By induction the
children's intervals lie in those of `Z0(Π_x Z)`, and forward evaluation of
one operation is its exact image, so `W_k ⊆ Z0(Π_x Z)_k`. □

**Definition 1.3 (propagation bounds).** For a box `C` and `y ∈ C`,

```
pi_D(C)    = min { c : Z*(C, c) ≠ ∅ },
pi_D(C, y) = min { c : y ∈ Π_x Z*(C, c) }.
```

The minima exist by Lemma 1.2(c), because the sets are nonempty
(Proposition 1.4(a)) and bounded below by `F_lo(C)`.

**Proposition 1.4 (what cutoff propagation certifies).** For every box `C` and
`y ∈ C`:

(a) `F_lo(C) <= pi_D(C) <= pi_D(C, y) <= f(y)`. In particular
`pi_D(C) <= min_C f`.

(b) A propagation run with cutoff `c` can remove `y` from `C` (end with a box
whose projection excludes `y`) only if `c < pi_D(C, y)`, and can empty `C` only
if `c < pi_D(C)`. A fair run of exact revises, or a fair HC4 run, empties `C`
exactly when `c < pi_D(C)`, and its limit removes exactly the points with
`pi_D(C, y) > c`.

(c) `C' ⊆ C` implies `pi_D(C') >= pi_D(C)` and `pi_D(C', y) >= pi_D(C, y)`.

*Proof.* (a) The lifted point `w(y)` (all node values at `y`) satisfies every
elementary constraint, so the one-point box `{w(y)}` is hull-consistent for
every `c >= f(y)`. It lies in `Z0(C)`, because interval extensions contain
exact values. So `y ∈ Π_x Z*(C, f(y))`. If `c < F_lo(C)`, the root interval of
`Z0(C)` misses `(-inf, c]` and no nonempty box is hull-consistent. The middle
inequality holds because `y ∈ Π_x Z*` implies `Z* ≠ ∅`. (b) Lemma 1.1(b)–(c).
(c) Lemma 1.2(a). □

So, as far as pruning is concerned, fixed-point cutoff propagation **is** a
node bound: it prunes `C` when `pi_D(C) > UBD - eps`, and otherwise shrinks `C`
to `Π_x Z*(C, UBD - eps)`. The quantity that matters is the **propagation gap**
`min_C f - pi_D(C) >= 0`. Bounded-round propagation is weaker, so every upper
bound on the power of `pi_D` (Sections 4–5) also applies to it.

**Solvers.** Couenne moves the objective into an auxiliary variable and uses
its upper bound in the downward pass of FBBT. SCIP also moves a nonlinear
objective into an auxiliary variable and uses the primal bound in bound
tightening; the papers read do not spell out the propagation path (Section 8).
SCIP applies a tightening only if its relative size exceeds a threshold, which
stops slowly converging propagation early. It also limits the propagation
rounds of its nonlinear constraint handler (parameter default 10, per the other
workstream's [probe](../solver-validation/results/maxproprounds_check.log)).
Floating point and such thresholds are outside the model.

**Scope.** The model covers every propagator built from revise steps of the
elementary constraints of the DAG: HC4, FBBT and their variants, with any
schedule. Stronger contractors that treat a whole constraint with repeated
variables at once are **outside** it. Examples are box consistency, shaving,
the monotonicity-based revise of Araya et al., and a specialized univariate
method in SCIP that "avoids the dependency problem" (Section 8).
The negative results of Sections 4–5 are about DAG-based propagation only.

## 2. Hybrid certificates

The node model is that of the constrained note (Section 1.2): boxes, a
relaxation bound, an incumbent `UBD >= f*` (possibly changing), pruning when
the bound is `>= UBD - eps`, and axis-parallel splits. Add **propagation
phases**. At any time, a node box `B_0` may be replaced by the projection
`B_f` of the final box of one or more propagation runs of the objective graph
with cutoffs `c = UBD - eps`. Each run starts from the forward box `Z0` of the
current x-box, intersected with any number of final lifted boxes of earlier
runs at this node or its ancestors (inherited bounds). A phase that empties the box prunes
the node. A maximal sequence of consecutive propagation runs at one node, with
no other reduction in between, counts as one phase. Relaxation-based
reductions (R-rel) and feasibility-based reductions (R-inf) of the constrained
note are also allowed, on x-boxes.

**Excluded.** Real solvers also tighten bounds of auxiliary (lifted) variables
by OBBT or reduced costs and then propagate from those bounds, and some branch
on auxiliary variables. Points removed that way are certified by neither (V)
nor (Π) below. Constraint propagation inside the same run as the cutoff is also
excluded; constraints may be propagated in separate (R-inf) rounds on x-boxes.
Inside one run, (Π) can fail at feasible points. The recheck's counterexample
is `f = -3x^2 + 2x^2 + 2x^2` on `[-1, 1]` with `F = {x >= 0.5}` and cutoff
`f* - 10^-3`: joint propagation empties the root, while
`pi_D([-1,1], y) = -1` for every `y`. (One could instead define `pi` on the
graph that includes the constraint nodes; Lemmas 1.1–1.2 hold unchanged, but
that bound is not the objective bound used in Sections 3–5.) "Every hybrid
run" in this note means every run of the model just described.

Write (V) for the relaxation-gap condition at a point,
`m(y) + eps >= alpha q_C(y)`, with `m = f - f*` and `q_C` as in the constrained
note, and (Π) for `pi_D(C, y) > f* - eps`.

**Lemma 2.1 (hybrid leaf-and-piece family).** Record as leaves the nodes pruned
by bound, by infeasibility, or by an emptying propagation phase. Decompose the
frame `B_0 \ int B_f` of each propagation phase, and the frame of each R-rel or
R-inf round, into at most `2n` boxes as in the constrained note (Section 2).
Let `P` be the family of leaves and pieces. Then:

(a) `P` consists of boxes with disjoint interiors covering `X0`.

(b) Under (G^pt_alpha), every `y ∈ F` lies in some `C ∈ P` for which (V) or
(Π) holds at `y`. Propagation leaves satisfy (Π) at all their points. A piece
`S` of a propagation phase from `B_0` to `B_f` satisfies (Π) at every
`y ∈ S \ B_f`.

(c) `|P| <= #leaves + 2n #(phases and reduction rounds)`. If every node has at
most one propagation phase and no other reduction, `|P| <= (2n+1) #nodes`.

*Proof.* (a) As in the constrained note, Lemma 2.1(a): splits partition boxes,
and each phase partitions `B_0` into `B_f` and frame pieces.

(b) *Propagation phases.* Define the **chain** of a phase recursively: its
own runs, and the chains of all phases one of whose runs has a final lifted
box that enters a start box of this phase. Let `c(Phi)` be the smallest cutoff
in the chain of phase `Phi`, and `B(Phi)` its start x-box. If a phase `Psi`
enters a start box of `Phi`, then the chain of `Psi` is part of that of `Phi`,
so `c(Phi) <= c(Psi)`. Also `B(Phi) ⊆ B(Psi)`, because `Psi` is at the same
node, earlier, or at an ancestor. We prove by induction over runs in time
order:

```
(*)  every run of a phase Phi keeps D(Phi) = Z*(B(Phi), c(Phi)).
```

Fix `Phi`, write `B_0 = B(Phi)`, `c = c(Phi)`, `D = D(Phi)`. `D` is
hull-consistent for every cutoff of `Phi`, since these are at least `c` (Lemma
1.2(b)). So by Lemma 1.1(b) it suffices that every start box of `Phi` contains
`D`. A start box is `Z0` of the current x-box intersected with final lifted
boxes of earlier runs.
- `Z0(B_0) ⊇ D` by definition. At a later run of `Phi`, the earlier runs kept
  `D` by (*), so `Π_x D ⊆ B_i`, and Lemma 1.2(d) with the monotonicity of
  `Z0` gives `D ⊆ Z0(Π_x D) ⊆ Z0(B_i)`.
- A final lifted box of an earlier run of `Phi` contains `D` by (*). A final
  lifted box of a run of an earlier phase `Psi` contains
  `D(Psi) = Z*(B(Psi), c(Psi)) ⊇ Z*(B_0, c) = D` by (*) for `Psi` and Lemma
  1.2(a)–(b).

This proves (*), and with it `Π_x D ⊆ B_f`. No assumption on how the
incumbent changes is needed. Every cutoff is at least `f* - eps`, and so is
`c`. (The first revision used only the phase's own cutoffs and assumed a
nonincreasing incumbent. With incumbents that move up and down,
[`check_revision.log`](logs/check_revision.log), part (E), finds 60 of 263
frame pieces uncertified by the phase-only minimum and none by the chain
minimum.)

(An earlier version said that consecutive runs "compose to one run". That is
false, because a restart from `Z0(B_i)` can enlarge the intervals of operation
nodes: [`logs/check_revision.log`](logs/check_revision.log), part (A).)

A piece `S ⊆ B_0` has `Z*(S, c) ⊆ D` by Lemma 1.2(a), so
`Π_x Z*(S, c) ⊆ B_f`. Hence a point `y ∈ S \ B_f` is not in `Π_x Z*(S, c)`,
that is `pi_D(S, y) > c >= f* - eps`. A phase that empties its box has
`D = ∅`, since a run that keeps `D` ends empty only if `D` is empty. So the
leaf satisfies (Π) at all its points.

Now follow a feasible point `y` through the run. At a split it goes to a child
that contains it. At a propagation phase, either `y ∈ B_f` and we continue, or
`y` lies in a piece `S` with `y ∉ B_f`, where (Π) holds. At an R-rel or R-inf
round, either `y` stays in the reduced box, or it lies in a piece where (V)
holds (constrained note, Lemma 2.1(b); R-inf pieces contain no feasible point).
At a leaf pruned by the relaxation bound, (V) holds (constrained note, Lemma
2.1(b)); at a leaf emptied by propagation, (Π) holds, as just shown. The
tree is finite, so this ends. Cutoffs `c = UBD - eps >= f* - eps` are covered
by Lemma 1.2(b).

(c) Each leaf is one member; each phase or round adds at most `2n` pieces. □

The merging of consecutive propagation rounds is legitimate because `Z*` is
monotone in the box and lies in the forward box of its own projection (Lemma
1.2(d)). This differs from OBBT, where the review found that merged
frames violate (V) (review, Section 1.3, Fix 1): an OBBT round uses the
relaxation of the current box, which changes from round to round.

**Theorem 2.2 (transfer principle).** Assume (G^pt_alpha). Let `N ⊆ X0`,
`beta > 0` and `theta > 0`, and suppose the representation satisfies:

```
(Π ⇒ V_beta)  for every box C and every y ∈ C ∩ N with m(y) + eps < theta,
              pi_D(C, y) > f* - eps  implies  m(y) + eps >= beta q_C(y).
```

Then the family `P` of every hybrid run satisfies (V) with
`alpha_eff = min(alpha, beta)` at every point of `N_theta = {y ∈ N ∩ F : m(y) + eps < theta}`.
Every lower bound of the constrained note whose proof uses (V) only at points
of `N_theta` holds for `|P|` with `alpha` replaced by `alpha_eff`. This includes
the covering bound (its Theorem 4.6) for `E(eta) ∩ N` with `eps + eta < theta`,
and the integral bound (its Theorem 3.1) over `N_theta`.

*Proof.* Lemma 2.1(b) and the hypothesis. The cited proofs sum, over the
members `C`, a bound on the part of the covered set certified by `C`, and use
(V) only at the certified points. The set certified by (Π) in `C`,
`{y ∈ C : pi_D(C, y) > c} = C \ Π_x Z*(C, c)`, is measurable, as the integral
bound needs. □

This is the precise form of the remark in the constrained note (Section 8.3)
that "the theory applies to a combined scheme exactly when that scheme still
satisfies a gap hypothesis". Sections 4–5 verify the hypothesis for classes of
representations.

**Proposition 2.3 (no lower bound holds for every representation).** For every
`f` that has a factorable representation `D` (with the operation `abs`
available), there is a representation `D'` of `f` with `pi_D'(X0) = f*`. With `UBD = f*`, cutoff propagation empties the root for
every `eps > 0`.

*Proof.* Take any representation of `f` with root `w` and add the nodes
`w1 = w - f*`, `w2 = abs(w1)`, `w3 = w2 + f*` (new root). The forward interval
of `w2` lies in `[0, inf)`, so `F_lo(X0) >= f*`, and Proposition 1.4(a) gives
`pi_D'(X0) = f*`. □

The new representation encodes the certificate `f >= f*`. So lower bounds must
be stated for a class of representations. Sections 4–5 use flat sums of
single-use terms, which include polynomials in monomial form, the form that
SCIP and BARON see after expanding products and powers. The same mechanism
explains the other workstream's observation that SCIP needs one node for the
ring `(x1^2 + x2^2 - 1)^2` when the square is not expanded
([summary](../solver-validation/results/summary.md), setting `noexpand`): the
forward interval of a square is nonnegative.

## 3. When propagation is exact

### 3.1 Flat sums of univariate terms

**Setting (FS).** The root is one sum node `f = b + sum_{j=1}^J a_j p_j`. Each
`p_j` is either a base node `z_{k(j)}` itself or a unary node
`p_j = phi_j(z_{k(j)})` used only by the root. The base nodes `z_1..z_K` are
variables or arbitrary subexpressions, and a base node may feed several terms
(this is the multiple occurrence). Write `t_j(z) = a_j phi_j(z)`, a continuous
function of one real variable, and `fh(z) = b + sum_j t_j(z_{k(j)})`, so that
`f(x) = fh(z(x))`. For base intervals `Z'_k = [sigma_k, tau_k]` define

```
m_j(Z') = min { t_j(z) : z ∈ Z'_{k(j)} },
h_j(Z') = max( t_j(sigma_{k(j)}), t_j(tau_{k(j)}) ),          (endpoint values only)
Phi(Z') = b + sum_j m_j(Z') + max_j ( h_j(Z') - m_j(Z') ).
```

For monotone terms, `h_j - m_j` is the width of the term's range. If the base
nodes are the variables (`K = n`, `z_k = x_k`), `D` is a **flat separable
sum**. Expanded univariate polynomials and separable polynomials in monomial
form are flat separable sums.

**Theorem 3.1 (fixed point of flat sums).**

(a) In setting (FS), if `Z*(C, c) ≠ ∅` and `Z'` are its base intervals, then
`Phi(Z') <= c`.

(b) For a flat separable sum, `Z*(C, c) ≠ ∅` if and only if `Phi(U') <= c` for
some nonempty box `U' ⊆ C`. Hence

```
pi_D(C) = min { Phi(U') : U' ⊆ C },     pi_D(C, y) = min { Phi(U') : y ∈ U' ⊆ C }.
```

*Proof.* (a) Let `P_j` be the interval of `p_j` in `Z*`, and
`T_j = a_j P_j`. Hull consistency of `p_j = phi_j(z_k)` means that the two
endpoints of `Z'_k` extend to points of the constraint, so `t_j(sigma_k)` and
`t_j(tau_k)` lie in `T_j`; and that the endpoints of `P_j` are attained, so
`T_j ⊆ t_j(Z'_k)`. Hence `min T_j >= m_j` and `max T_j >= h_j`. (If `p_j` is
the base node itself, `T_j = a_j Z'_k` and both facts are immediate.) Hull
consistency of the root constraint, whose interval lies in `(-inf, c]`, means
that the endpoint of `P_j` giving `max T_j` extends to a solution: there are
values in the other intervals with
`c >= b + max T_j + sum_{i≠j} t_i >= b + h_j + sum_{i≠j} m_i`. This holds for
every `j`, so `c >= Phi(Z')`.

(b) "Only if" is (a) with `Z' = Π_x Z*`. For "if", build a lifted box: the
variables get `U'`; each `p_j` gets the interval with `a_j P_j = [m_j, h_j]`
(for `p_j = x_k` this is `U'_k` itself); the root gets
`F = [b + sum_j m_j, min(c, b + sum_j h_j)]`. It is hull-consistent:
- for `p_j = phi_j(x_k)`: the endpoints of `U'_k` map into `[m_j, h_j]`; the
  value `m_j` is attained in `U'_k` and `h_j` at an endpoint;
- for the root: any value `v ∈ [m_j, h_j]` of term `j`, with all other terms at
  their minima, gives `b + v + sum_{i≠j} m_i <= Phi(U') <= c`, a point of `F`;
  the endpoints of `F` are attained because the sum of intervals is an
  interval.
The box lies in `Z0(C)`, since images over `U'` lie in images over `C`. So it
is contained in `Z*(C, c)`. The formula for `pi_D(C, y)` follows because the
witness has `x`-part `U'`, and because `Π_x Z*` is itself a sub-box satisfying
(a). The minimum exists because `Phi` is continuous in the endpoints. □

**Remark 3.2 (sums written as chains).** If the root sum is a chain or tree of
binary sums, (a) still holds. Within a box, each linear constraint has a convex
feasible set, so hull consistency makes every value of each of its intervals
extend within that constraint. Induction over the tree of sum constraints then
extends every value to all of them, which gives the same inequality. For (b),
give the partial sum `s_k = b + t_1 + ... + t_k` the interval
`[b + sum_{i<=k} m_i, min(b + sum_{i<=k} h_i, c - sum_{i>k} m_i)]`. Each binary
constraint `s_k = s_{k-1} + t_k` is then hull-consistent when `Phi(U') <= c`;
the critical case, extending the upper endpoint `h_k` of `t_k`, uses exactly
`b + h_k + sum_{i≠k} m_i <= c`.

The endpoint maximum `h_j` in `Phi` is essential. A first version of this
theorem used the full range `max t_j - m_j`. The check
[`check_formula.py`](check_formula.py) found HC4 fixed points below the grid
minimum of that expression, because hull consistency lets a non-monotone term
(for example `x^2` on an interval containing 0) drop its interior maximum.
With `h_j`, all 450 random instances agree: 300 univariate and 150 bivariate
separable sums of monomials `a x_i^k`, `k <= 4`, random boxes. A grid witness
gives a nonempty fixed point at `pi_grid + delta` in 450 of 450 cases. At
`pi_grid - delta`, HC4 empties the box in 440 cases. In the other 10 (all
bivariate, grid of 50 points per axis), the fixed box `U''` satisfies
`Phi(U'') = c` to machine precision: the grid was too coarse, as (a) predicts
([log](logs/check_formula.log)). The independent review repeated the test with
general non-monotone polynomial unary nodes (200 of 200 agree, also in chain
form). It noted that random tests rarely separate the two formulas: their
minima differ in only 4 of its 200 instances.

A targeted example (from the review; re-run in
[`check_revision.py`](check_revision.py), part (A)) separates them. Write `x^2`
as `-3x^2 + 2x^2 + 2x^2`, three separate power nodes, on `C = [-1, 1]`. The
endpoint formula gives `Phi([-a, a]) = -3a^2 + 2a^2 = -a^2`, so
`pi_D(C) = -1`, while the full-range formula has minimum 0 over sub-boxes.
Bisection with HC4 gives `pi_D([-1,1]) = -1`, `pi_D([-0.1,0.1]) = -0.01` and
`pi_D([-0.1,0.3]) = -0.03`, as the endpoint formula predicts. The single term
`x^2` has `pi_D = 0`. So the representation, not `f`, decides exactness.

**Corollary 3.3 (one-sided representations are exact).** In setting (FS) with
one base node (`K = 1`), say that a base interval `Z'` is **one-sided** if some
term `j0` and some endpoint `e` of `Z'` satisfy `t_{j0}(e) = h_{j0}(Z')` and
`t_i(e) = m_i(Z')` for all `i ≠ j0`. If every sub-interval of the base range
`Z0(C)_z` is one-sided, then

```
pi_D(C) >= min { fh(z) : z ∈ Z0(C)_z },
```

with equality `pi_D(C) = min_C f` when the base node is the variable itself.

*Proof.* By Theorem 3.1(a),
`c >= Phi(Z') >= b + h_{j0} + sum_{i≠j0} m_i = fh(e)` whenever `Z*(C,c) ≠ ∅`.
With `z = x`, combine with `pi_D(C) <= min_C f` (Proposition 1.4). □

A simple sufficient condition: on the base range all terms are monotone and at
most one of them is strictly increasing (take `e` = right endpoint), or at most
one is strictly decreasing (`e` = left endpoint). Examples:
- `s^2 - 2as + a^2` (terms `s^2` and `s`) on intervals inside `(0, inf)`;
- `h_c(s) = s^4 + (c-2)s^2 - 2cs + (1+c)` with `0 < c < 2` on intervals inside
  `(0, inf)` (only `s^4` increases) or inside `(-inf, 0)` (only `(c-2)s^2`
  increases; take `e` = right endpoint). For `h_{1/2}` on three intervals in
  `s < 0`, bisection gives `pi_D(C) = min_C h` to six digits
  ([`check_revision.log`](logs/check_revision.log), part (C));
- `t^2 - 2t^4` with terms `t^2` and `t^4` on **every** interval: take
  `j0 = t^2` and `e` the endpoint of larger `|t|`, where `-2t^4` is minimal.

**Remark 3.4 (the dichotomy at a stationary point).** Let `z0` be an interior
stationary point of `fh` (one base node), with every term `C^1` and
`t_j'(z0) ≠ 0`. Let `a` be the sum of the positive derivatives; it equals the
sum of the absolute values of the negative ones. If only one term has a
positive (or only one a negative) derivative, the terms are monotone near
`z0`, small intervals around `z0` are one-sided, and propagation is exact there.
Otherwise both sign classes have at least two terms, so
`max_j |t_j'(z0)| < a`, which is half the total derivative mass. Section 4
shows that this gives a first-order loss. These are the only two cases.

### 3.2 Separable sums and the lifted geometry

**Corollary 3.5 (separable identity).** For a flat separable sum and a box
`U'`, let `T_k` be the terms of variable `k`, `f_k = sum_{j ∈ T_k} t_j`,

```
e_k(U'_k) = min_{U'_k} f_k - sum_{j ∈ T_k} m_j >= 0          (forward excess of coordinate k),
G_k(U'_k) = max_{j ∈ T_k} (h_j - m_j) - e_k(U'_k).
```

Then

```
Phi(U') = min_{U'} f + max_k [ G_k(U'_k) - sum_{l ≠ k} e_l(U'_l) ],
```

and `G_k(U'_k) >= 0` whenever `U'_k` is one-sided for the terms of
coordinate `k`.

*Proof.* `b + sum_j m_j = min_{U'} f - sum_k e_k`, and
`max_j (h_j - m_j) = max_k (G_k + e_k)`. If `U'_k` is one-sided with `j0` and
`e`, then `h_{j0} - m_{j0} = f_k(e) - sum_{j∈T_k} m_j >= e_k`. □

So when every coordinate is one-sided, the only loss is **cross-coordinate**:
`Phi(U') >= min_{U'} f - min_k sum_{l≠k} e_l`. Propagation along coordinate `k`
is exact given the others' bounds, but it sees the other coordinates only
through their forward lower bounds `min f_l - e_l`. If all coordinates but one
have zero forward excess (for example a single term each), and that one is
one-sided, propagation is exact. The loss is real. For `h_{1/2}(x_1) + h_{0.7}(x_2)` in expanded form
(instance `iso2`), both coordinates are one-sided near `x* = (1,1)`, yet
`pi_D` of the cube of radius `r` around `x*` is `-7.99 r` at `r = 10^-3`
([`check_loss.log`](logs/check_loss.log)). The strip
`[1-h, 1+h] x [0.5, 1.5]` has `pi_D = -8.00 h` for `h = 10^-4`, whatever its
length ([`check_constants.log`](logs/check_constants.log)).

**Proposition 3.6 (box-likeness in lifted coordinates).** In setting (FS), let
`B(C) = Π_k Z0(C)_k` be the box of forward images of the base nodes over `C`.
Suppose that for every box `Z' ⊆ B(C)` of base intervals, each coordinate is
one-sided on `Z'_k`, and at most one coordinate has `e_k(Z'_k) > 0`. Then

```
pi_D(C) >= min { fh(z) : z ∈ B(C) }.
```

So cutoff propagation empties `C` whenever the lifted bounding box `B(C)`
misses the lifted sublevel set `{fh <= c}`.

*Proof.* If `Z*(C, c) ≠ ∅`, its base intervals `Z'` lie in `B(C)`, and
`Phi(Z') <= c` by Theorem 3.1(a). The identity of Corollary 3.5 is algebra in
the `t_j` and holds for `fh` on `Z'`. Choose `k` to be the coordinate with
positive excess (or any coordinate). Then `G_k >= 0` and `sum_{l≠k} e_l = 0`,
so `c >= Phi(Z') >= min_{Z'} fh`. □

The image `z(C)` lies in `B(C)`. When the base nodes depend on disjoint sets
of single-use variables, `z(C) = B(C)` and the bound is exact. When they are
overlapping linear forms (a rotation), `B(C)` is larger than `z(C)`. So the
geometry that decides exactness is the box-likeness of the sublevel set **in
the lifted coordinates the DAG exposes**, not in `x`. A rotated quadratic is
no obstacle if the rotation is in the DAG.

**Examples 3.7.** Relaxations are exact alphaBB with the stated `alpha`;
`h(s) = h_{1/2}(s) = (s-1)^2((s+1)^2 + 1/2) = s^4 - 1.5 s^2 - s + 1.5 >= 0`,
with its unique zero at `s = 1`. The instances are in
[`instances.py`](instances.py).

(a) *The review's instance* `t^2 - 2t^4` on `[-1/3, 2/3]`. In monomial form
(terms `t^2`, `t^4`), Corollary 3.3 gives `pi_D(C) = min_C f` for every
interval. In the review's form `u = t^2, v = u^2, f = u - 2v`, the base `u`
has range in `[0, inf)`, where `u` increases and `-2u^2` decreases, so
Proposition 3.6 gives `pi_D(C) >= min { u - 2u^2 : u ∈ t^2(C) } = min_C f`.
Either way, the root is emptied for every `eps > 0`. This explains the
review's observation.

(b) *The same function, shifted and expanded* (`nondeg1s`: `y = t + 1/3` in
`[0,1]`). The expanded form is
`-2y^4 + (8/3)y^3 - (1/3)y^2 - (10/27)y + 7/81`. On `[0, 1]` all four terms are
monotone and only `(8/3)y^3` increases, so every sub-interval is one-sided and
Corollary 3.3 gives `pi_D(C) = min_C f`. The root is emptied for every `eps`,
but after 43 to 27944 rounds (Section 3.3): all four terms are strictly
monotone at the minimizer `y = 1/3`.

(c) *`linediag`*: `f = h(x - y)` on `[-2, 2.2] x [-1.9, 2.1]`, `alpha = 3`,
optimal segment `x - y = 1`. With the base node `s = x - y` (representation
`s`, terms `s^4, s^2, s`), every `s`-interval inside `(0, inf)` or
`(-inf, 0)` is one-sided. So every box whose `s`-range excludes 0 has
`pi_D(C) >= 0 = f*` and is emptied at `c = -eps`.

(d) *`rot_kappa`*: `f = h(x - y) + kappa (x + y - 1)^2`, isolated minimizer
`(1, 0)`, Hessian eigenvalues `18` and `4 kappa`. With the bases
`s = x - y` and `t = x + y - 1`, the `t`-coordinate has one term (no excess),
and Proposition 3.6 applies: every box whose `s`-range excludes 0 is emptied,
for every `kappa`. The 3D instance `line3`
(`h(x_1 - x_2) + (x_2 + x_3 - 1)^2`, optimal line transversal to all axes)
behaves the same way.

(e) *`nd2`*: `sum_l (t_l^2 - k_l t_l^4)` with `k = (2, 1.5)` in monomial
form. Both coordinates have positive excess, so Proposition 3.6 does not apply.
Directly from Theorem 3.1(b): take in `Phi(U')` the term `t_i^2` at its larger
endpoint and all other terms at their minima. With `R_l = max_{U'} |t_l|`,
`K = max k_l` and `i` maximizing `R_l`,
`Phi(U') >= R_i^2 - sum_l k_l R_l^4 >= R_i^2 (1 - n K R_i^2) >= 0` if
`R_i^2 <= 1/(nK)`. So every box inside `{|t_l| <= (nK)^(-1/2)}` is emptied.

**Theorem 3.8 (node counts independent of eps).** Let `F = X0`, and let `f` be
`L`-Lipschitz in the sup-norm. Assume the relaxation satisfies (U_tau):
`LB(B) >= min_B f - tau w(B)^2`. Assume local exactness: there are a relatively
open set `R ⊇ M` and `w0 > 0` with `pi_D(C) >= f*` for every box `C ⊆ R` with
`w(C) <= w0`. Let `delta = min_{X0 \ R} m > 0` and
`w* = min(w0, delta/(2L), (delta/(2 tau))^(1/2))`. Consider the following
idealized branch-and-bound: `UBD = f*`; at every node, cutoff propagation
decides whether the fixed point `Z*` is empty (then the node is pruned) and
otherwise may contract the box to any box containing `Π_x Z*`; then the
relaxation bound; then widest-side bisection. For every `eps > 0` it processes
at most `2^(d+1) - 1` nodes, where `d = n ceil(log2(s0/w*))`.

The algorithm is idealized. A fair run empties a node with `Z* = ∅` after
finitely many rounds (Lemma 1.1(c)), but a node with `Z* ≠ ∅` may only
converge in the limit, and propagation cannot tell in advance which case it is
in. The node bound holds for any stopping rule that never stops propagation on
a node with `Z* = ∅` before the box is emptied. The number of rounds needed is
not bounded independently of `eps` (Section 3.3).

*Proof.* Let `D` be a node box with `w(D) <= w*`. If `D ⊆ R`, then
`pi_D(D) >= f* > f* - eps`, so `Z*(D, f* - eps) = ∅` and `D` is pruned. Otherwise `D`
contains a point `z ∉ R`, so `m(z) >= delta`, and `m >= delta - L w* >= delta/2`
on `D`. The contracted box `D' ⊆ D` then has
`LB(D') >= f* + delta/2 - tau w*^2 >= f*`, so it is pruned. Thus no box of
width at most `w*` is split. Let `Psi(B) = sum_i max(0, ceil(log2(w_i(B)/w*)))`.
It is at most `n ceil(log2(s0/w*))` at the root. Contraction does not increase
it. Bisecting a widest side longer than `w*` decreases it by at least 1. A
split node has `Psi >= 1`. So the tree has depth at most `d`. □

The relaxation is used only away from `M`; near `M`, propagation certifies
alone. The principle is known for exact bounds. Du and Kearfott: "In problems
in which the lower bound given by the interval extension F is exact, there will
be no cluster". Wechsung, Schaber and Barton: "When K is sufficiently small,
i.e., K <= λ1/8, the cluster problem is completely absent (N = 1)" (Section
8). What Theorem 3.8 adds is its application to the propagation bound `pi_D`,
with Corollary 3.3 and Proposition 3.6 as conditions under which `pi_D` is
exact. Theorem 3.8 applies to Examples 3.7:
- (a) with `R = X0`;
- (c) and (d), and `line3`, with `R = {x - y > 1/2}`, `w0 = inf` and
  `delta = h(1/2) = 0.6875`: `h` decreases on `(-inf, 1)`, because
  `h'(s) = (s - 1)(2s + 1)^2`;
- (e) with `R = {|t_l| < 1/2}`.

### 3.3 Where the cost goes: propagation rounds

Exactness is a property of the fixed point. Reaching it can be slow.

**Heuristic 3.8a (round counts; not proved).** Consider setting (FS) with a
representation that is one-sided near a nondegenerate minimizer, so that the
fixed point of a small box around it is empty (Corollary 3.3, Proposition 3.6).
Emptying the box takes `Theta(eps^(-1/2))` rounds when some base node has at
least two terms whose nonzero derivatives cancel at the minimizer. It takes few
rounds when no base has such a cancellation: all terms are stationary there, or
the minimizer is an end of a lifted range where `f` grows linearly in the base.
(Without one-sidedness, the balanced case of Remark 3.4, the box is not emptied
at all once it is wider than `O(eps)`.)

Evidence ([`logs/rounds.log`](logs/rounds.log), Table 7.1). Rounds times
`sqrt(eps)` tend to a constant in the cancelling cases:
- `(s-1)^2`: 3.14;
- `h_{1/2}`: 5.92;
- `nondeg1s`: 2.79;
- `linediag`/`s`, `rot_kappa`/`st` and `line3`/`st`: 5.92.

In the last two, the base `t` carries a single term `t^2` that is stationary
at the minimizer, and it changes nothing. Likewise `x^2 - 2x + 1 + (x-1)^4`,
with the quartic written through the base `r = x - 1`, needs exactly the rounds
of the plain quadratic (30 to 31414). The non-cancelling cases need 3–7
rounds: `t^2 - 2t^4` in monomial form (both terms stationary at `t = 0`), the
forms `u` and `centered` (one nonzero derivative, minimizer at `u = 0`), and
`nd2`. An interior minimizer of `f` alone does not decide the count. A first
revision of this note stated a criterion "every term strictly monotone at the
minimizer"; the recheck showed it is contradicted by `rot_kappa`/`st` and
`line3`/`st`.

**Proposition 3.9 (slow fixed point when term derivatives cancel).** Let `a > 0`,
`0 < eps <= a^2/16`, and `f = (s - a)^2` in the representation
`s^2 - 2as + a^2` (terms `s^2` and `s`). Run HC4 rounds as in
[`fbbt.py`](fbbt.py) (forward pass, cutoff `c = -eps`, backward pass) from
`[a - y0, a + x0]` with `0 < x0, y0 <= a/4`, and let
`z0 = min(x0, y0)`. The box remains nonempty for at least

```
(a / (4 sqrt(eps))) (arctan(z0/sqrt(eps)) - arctan(4 sqrt(eps)/a)) - 1  =  (pi/8 - o(1)) a eps^(-1/2)
```

HC4 rounds. The fixed point is empty (Corollary 3.3), so the root is
eventually pruned. The bound is for this schedule. The review observed about
`4.2/sqrt(eps)` rounds for `(s-1)^2` under a random chaotic schedule of exact
revises; a schedule-free bound counting revise steps was not worked out.

*Proof.* Write `x = tau - a` and `y = a - sigma`. In one round the backward
step of the sum node gives `s^2 <= c - a^2 + 2a tau` and
`-2as <= c - a^2 - sigma^2`, using the forward images `[sigma^2, tau^2]` and
`[-2a tau, -2a sigma]`. The power node then gives the new upper bound. So

```
y' = y - (y^2 + eps)/(2a),        x' = sqrt(a^2 + 2ax - eps) - a >= x - (x^2 + eps)/a,
```

where the inequality is equivalent, after squaring, to
`(x^2 + eps)(1 + 2x/a - (x^2 + eps)/a^2) >= 0` and holds for `0 <= x <= a`,
`eps <= a^2`. Both sequences satisfy `z' >= z - (z^2 + eps)/a` and are
nonincreasing. While `x, y >= 4eps/a` the box is nonempty: the new lower bound
is at most `a + eps/(2a) <= tau'`, and the power-node update needs
`sigma^2 <= 2a tau - a^2 - eps`, which holds since `sigma <= a - eps/a`.
Let `theta(z) = arctan(z/sqrt(eps))`. If `4eps/a <= z <= a/4`, then
`Delta = (z^2 + eps)/a <= z/2`, so `z' >= z/2`, and

```
theta(z) - theta(z') <= Delta sqrt(eps)/(eps + z'^2) <= ((z^2 + eps)/a) sqrt(eps)/(eps + z^2/4) <= 4 sqrt(eps)/a.
```

So `theta(z_k)` falls by at most `4 sqrt(eps)/a` per round until `z_k < 4eps/a`,
and at least `(theta(z0) - theta(4eps/a)) a/(4 sqrt(eps))` rounds pass first.
□

The bound is not sharp. The observed count is `pi a/sqrt(eps)` (round count
times `sqrt(eps)` = 3.000, 3.099, 3.130, 3.137, 3.140, 3.141, 3.141 for
`eps = 10^-2..10^-8`, `a = 1`, box `[0.2, 2.2]`). This is the ODE
`dz/dk = -(z^2 + eps)/(2a)`, which takes `pi a/sqrt(eps)` to cross 0. For the
double well `h` (expanded, box `[0.2, 2.2]` or the root `[-2, 2.2]`), the
count is `5.92/sqrt(eps)`; for `nondeg1s`, `2.79/sqrt(eps)`. In both, the
terms of the single base have cancelling nonzero derivatives at the minimizer.
With fixed-point propagation these instances have one node but
`Theta(eps^(-1/2))` propagation rounds (observed). Relaxation-only
branch-and-bound on the same 1D instances needs `Theta(log(1/eps))` nodes
(Table 7.1). So where a base has cancelling term derivatives, exact
propagation does not remove the cost; it moves it into rounds.

**Proposition 3.10 (fast fixed point at a lifted endpoint).** In the review's
form `u = t^2, v = u^2, f = u - 2v` with cutoff `-eps`, let `U_k` be the upper
bound of `u` after round `k`. If `2 U_0 < 1`, then `2U_{k+1} <= (2U_k)^2`, and
the box is empty after at most `2 + log2( ln(1/(2eps)) / ln(1/(2U_0)) )`
rounds.

*Proof.* The backward step of the sum gives `u <= c + 2 max v = 2U_k^2 - eps`.
So `2U_{k+1} <= (2U_k)^2` and `2U_k <= (2U_0)^(2^k)`. The box is empty once
`2U_k^2 - eps < 0`, which holds when `(2U_0)^(2^(k+1)) < 2 eps`. □

For the review's box `U_0 = 4/9`. The observed counts are 3–4 rounds (form
`u`) and 4–7 rounds (monomial form) for `eps = 10^-2..10^-8`. The
difference from Proposition 3.9 is that the minimizer sits at the end `u = 0`
of the lifted range, where `f` grows linearly in `u` and the interval loss is
quadratic in the `u`-width. In the monomial form both terms are stationary
at `t = 0`, so no base has cancelling derivatives. A proof of the
`O(log log(1/eps))` rate for the monomial form was not written out. This mirrors sharp versus quadratic growth for
iterated OBBT (repository note
[`iterated-obbt/theory.md`](../../../research-20260922/iterated-obbt/theory.md),
Propositions 2–3).

**Conjecture 3.11 (bounded rounds).** Suppose the representation is one-sided
near a nondegenerate optimal set, and some base has at least two terms whose
nonzero derivatives cancel there (the slow case of Heuristic 3.8a), as in
Examples 3.7(b)–(d) and `line3`.
Then branch-and-bound with a (G_alpha) relaxation and at most `R` propagation
rounds per node has the same `eps`-exponent as without propagation, for fixed
`R`.

*Evidence.* Heuristically, `R` rounds shrink a box around the optimum by only
`O(R (w^2 + eps)/a)` per side (proof of Proposition 3.9). Numerically (Table
7.1):
- `linediag` in representation `s` with `R = 3` or `10`: `eps^(-0.50)`, the
  same as without propagation (13451 and 13911 against 14559 nodes at
  `10^-5`);
- `line3` with `R = 10`: undecided. The fitted exponent over `10^-1..10^-4`
  is 0.72, against 0.54 without propagation. The counts are smaller at every
  `eps` and approach the propagation-free counts (23387 against 25475 at
  `10^-4`), so the exponents may agree asymptotically, but over the tested
  range they do not;
- `h` and `nondeg1s` with `R = 3` or `10`: `log(1/eps)`.

SCIP's relative threshold on tightenings has the same effect as bounded rounds
in these slowly converging cases. It is consistent with the other workstream's
finding that SCIP's node counts on `linediag2` barely depend on cutoff
propagation (Section 8).

## 4. The witness lemma and first-order dependency loss

**Setting (FS1).** `f = b + sum_j t_j`, one root sum, where each term
`t_j = a_j g_j` and `g_j` is a single-use expression: a tree in which each
variable occurs at most once and whose nodes are used only inside the term.
Different terms may share variables. Polynomials in monomial form
(`c x_1^3 x_2`, ...) are of this form. The shared-base representations `s`,
`st`, `u` and `centered` of Section 3 are not, because one base node feeds
several terms; Remark 4.1a covers them.

**Lemma 4.1 (witness lemma).** In setting (FS1), for every box `U' ⊆ C` and
every `y ∈ U'`,

```
pi_D(C, y) <= Phi_full(U') = b + sum_j min_{U'} t_j + max_j ( max_{U'} t_j - min_{U'} t_j ).
```

Hence no propagation run with a cutoff `c >= Phi_full(U')` removes any point of
`U'` from `C`.

*Proof.* Build a lifted box: variables get `U'`; each node inside a term gets
the exact image of its subtree over `U'`; the root gets
`[b + sum_j min t_j, min(c, b + sum_j max t_j)]` with `c = Phi_full(U')`.
Inside a term, the two arguments of a binary node depend on disjoint sets of
variables, so the set of their joint values is the product of their images and
the node's image is exact. Every value of every interval therefore extends, so
these constraints are hull-consistent. The root is handled as in Theorem
3.1(b), with `h_j = max_{U'} t_j`. The box lies in `Z0(C)`. □

**Remark 4.1a (general form).** Single use is not needed for the witness.
Let the root be a sum `b + sum_j a_j p_j` of distinct nodes `p_j`, over any
DAG below them. Define `Phi_full(U')` from the exact ranges of the `p_j` over
`U'`. Then `pi_D(C, y) <= Phi_full(U')` for all `y ∈ U' ⊆ C`.

*Proof.* Give every non-root node the exact range of its expression over `U'`
(an interval, by continuity), and give the root the interval of Lemma 4.1. Take
an elementary constraint `w = op(u, v)` below the root and any value of one of
its three intervals. That value is attained at some point `x ∈ U'`, and then
`u(x)`, `v(x)` and `w(x)` lie in their intervals and satisfy the constraint.
So every value of every interval extends, and these constraints are
hull-consistent. The root constraint treats the `p_j` coordinates
independently and is handled as in Theorem 3.1(b). The box lies in `Z0(C)` by
the inclusion property of interval extensions. □

This covers the shared-base representations `s`, `st`, `u` and `centered`.
Single use matters only in Corollary 4.2, where Moore's theorem gives
`F_lo(C) = b + sum_j min_C t_j`. The recheck confirmed the witness on 300
random DAGs with non-single-use bases and on 750 boxes of the named
representations. Sections 4–5 apply the witness only to expanded forms, so
nothing below depends on this remark. (The first revision stated it only for
single-use bases.)

**Corollary 4.2 (propagation gains at most one term).** In setting (FS1),

```
F_lo(C) <= pi_D(C) <= F_lo(C) + max_j width_C(t_j).
```

*Proof.* Forward evaluation of a single-use term gives its exact range (Moore's
theorem), so `F_lo(C) = b + sum_j min_C t_j`. Apply Lemma 4.1 with `U' = C`. □

So the fixed point can improve on forward interval evaluation by at most the
width of the widest term. Exactness therefore requires the forward excess
`min_C f - F_lo(C)` to be concentrated in one term, which is what one-sidedness
provides.

**Example 4.3 (a rotated quadratic).** Take `f = x^2 - 2xy + y^2` with terms
`x^2`, `-2(x*y)`, `y^2`, and a box `C` whose diagonal chord is
`[a, b] = [x_l, x_u] ∩ [y_l, y_u]`, with `0 < a < b`. Then every diagonal point
`(t, t) ∈ C` satisfies

```
pi_D(C, (t,t)) <= -2a(b - a).
```

So at cutoff `-eps` (here `f* = 0`), no propagation run removes a diagonal
point from `C` unless `2a(b - a) < eps`: the chord has length `O(eps/a)`.

*Proof.* A witness with a reduced product range: `x, y ∈ [a, b]`, the squares
`[a^2, b^2]`, the product `w = xy` in `W = [ab, b^2]`, and the root in
`[2a^2 - 2b^2, -2a(b-a)]`. For `w = xy`: `x = a` extends with `y = b`, `x = b`
with `y = b`, and symmetrically; `ab` and `b^2` are attained. The terms have
ranges `[a^2, b^2]`, `[-2b^2, -2ab]` and `[a^2, b^2]`. Their minima sum to
`2a^2 - 2b^2`. Raising the middle term to its maximum gives `-2a(b-a)`;
raising a square gives `a^2 - b^2 <= -2a(b-a)`. So the root constraint is
hull-consistent at `c = -2a(b-a)`. `W` lies in the forward image of `xy` over
`C ⊇ [a,b]^2`, and the diagonal points of `C` lie in `[a,b]^2`. □

The full-range witness gives nothing here: `Phi_full([a,b]^2) = 0`. Hull
consistency supports only interval endpoints, so a witness may drop part of a
multivariate term's range. The forward bound on `[a, b]^2` is `-2(b-a)(b+a)`,
and propagation recovers at most part of it.

**Lemma 4.4 (first-order loss).** In setting (FS1), let
`U' = y + Π_i [-delta_i, delta_i] ⊆ C`, with the terms `C^2` on `U'`. Let `H_j`
bound all second partial derivatives of `t_j` on `U'`, and
`K = sum_j H_j/2 + max_j H_j`. Then

```
pi_D(C, y) <= f(y) - Lambda_y(delta) + K |delta|_1^2,
Lambda_y(delta) = sum_j sum_i |d_i t_j(y)| delta_i  -  2 max_j sum_i |d_i t_j(y)| delta_i.
```

*Proof.* For `h ∈ Π [-delta_i, delta_i]`, Taylor's theorem gives
`|t_j(y+h) - t_j(y) - grad t_j(y)·h| <= (H_j/2) |h|_1^2`. With
`h_i = -delta_i sign(d_i t_j(y))`,
`min_{U'} t_j <= t_j(y) - sum_i |d_i t_j(y)| delta_i + H_j |delta|_1^2/2`, and
`max_{U'} t_j - min_{U'} t_j <= 2 sum_i |d_i t_j(y)| delta_i + H_j |delta|_1^2`.
Insert these into `Phi_full(U')` and apply Lemma 4.1. □

Two special cases are used below.

- *Segments* `delta = delta e_i`: `Lambda = D_i(y) delta` with
  `D_i(y) = sum_j |d_i t_j(y)| - 2 max_j |d_i t_j(y)|`. Only `d_ii t_j` enters
  the remainder.
- *Cubes* `delta = delta (1,...,1)`: `Lambda = L(y) delta` with
  `L(y) = sum_j |grad t_j(y)|_1 - 2 max_j |grad t_j(y)|_1`, and remainder
  `K n^2 delta^2`.

We say the representation has **no dominant term coordinatewise (CND)** at `y`
if `D_i(y) > 0` for every `i`, and **no dominant term (ND1)** if `L(y) > 0`.
CND says that in each coordinate direction no single term carries half of the
total absolute partial derivative. At a stationary point the partials sum to
zero, so CND requires, in each coordinate, at least two terms of each sign and
no term carrying its whole sign class (Remark 3.4). In two variables, a
quadratic in monomial form never satisfies CND at a stationary point with
nonzero coordinates. Each coordinate has at most three nonzero monomial
partials (`x_i^2`, `x_1 x_2`, `x_i`), and three numbers summing to zero have a
sign class with one element. ND1 can still hold.

Measured values ([`check_loss.log`](logs/check_loss.log),
[`check_constants.log`](logs/check_constants.log)):
- On the optimal line `(t+1, t)` of `linediag` (expanded form), `D_1 = D_2`
  equals 0 at `t = 0` and `0.864, 2.35, 7.78, 22.0` at `t = 0.1, 0.2, 0.4, 1.0`,
  and `3.2–5.0` for `t ∈ [-0.8, -0.2]`. At `t = 0`, the point `(1, 0)`, the
  coordinate-segment loss vanishes (`D_i = 0`), but `L = 8` and the measured
  cube loss is `8.01 r`. So the representation has face-type loss there, not
  exactness. (The first version wrongly called it locally one-sided; the
  point was added to `check_loss.py` in the revision.)
- The observed loss `(f(y) - pi_D(C))/r` on cubes of radius `r = 10^-3` is 51,
  18.5 and 140 at `t = 0.5, 0.2, 1.0`. Lemma 4.4 predicts at least
  `L = 24, 11.6, 76`. The difference comes from witnesses that drop parts of
  term ranges, as in Example 4.3.
- For `iso2` at `(1,1)` and `rot_kappa` at `(1,0)` (expanded): `D_i = 0` and
  `L = 8`. The observed cube loss is `7.99 r` and `8.01 r`.
- The representations `s` and `st` give `pi_D = f*` up to the bisection
  resolution (`-9e-8`).

## 5. Lower bounds that survive cutoff propagation

In this section `F = X0` and the relaxation satisfies (G^pt_alpha). The
representation is in setting (FS1). `s0` is the largest side of `X0`, and
`d_i^C(y) = min(y_i - l_i, u_i - y_i)` is the distance from `y` to the nearer
face of `C` in coordinate `i`.

**Theorem 5.1 (CND localizes propagation at vertices).** Let `N ⊆ X0`,
`D0 > 0`, `rho > 0` and `K0 >= 0` be such that for every `y ∈ N` and every
`i`:
- `D_i(y) >= D0`;
- for `|s| <= rho` with `y + s e_i ∈ X0`, every `t_j` has
  `|d_ii t_j(y + s e_i)| <= H_j`, where `sum_j H_j/2 + max_j H_j <= K0`.

Let `rho* = min(rho, D0/(2K0))` and `theta = D0 rho*/2`. If `y ∈ N ∩ C`,
`pi_D(C, y) > f* - eps` and `m(y) + eps < theta`, then

```
d_i^C(y) < 2 (m(y) + eps)/D0  for every i,   and   m(y) + eps >= (D0/(2 n w(C))) q_C(y) >= alpha_F q_C(y),
```

with `alpha_F = D0/(2 n s0)`.

*Proof.* Fix `i` and let `delta = min(d_i^C(y), rho*)`. The segment
`y + [-delta, delta] e_i` lies in `C`. By Lemma 4.4 (segment case),
`f* - eps < pi_D(C, y) <= f(y) - D0 delta + K0 delta^2 <= f(y) - D0 delta/2`,
since `delta <= D0/(2K0)`. So `delta < 2(m(y) + eps)/D0 < 2 theta/D0 = rho*`.
Hence `delta = d_i^C(y)`, which proves the first claim. Then
`a_i(y) = (y_i - l_i)(u_i - y_i) <= d_i^C(y) w(C)`, so
`q_C(y) <= n w(C) max_i d_i^C(y) < 2 n w(C)(m(y) + eps)/D0`. □

The same proof with Lemma 4.4 for boxes gives the conclusion whenever
`Lambda_y(delta) >= Lambda0 max_i delta_i` for all `delta >= 0`, with `D0`
replaced by `Lambda0` and `K0` by `n^2 K`. CND implies this with
`Lambda0 = min_i D_i(y)`, because `max_j sum_i <= sum_i max_j`.

**Proposition 5.1a (two-sided localization).** This is the review's
observation, proved here. In the setting of Theorem 5.1, replace
`D_i(y) >= D0` by `D_i(y) - |d_i f(y)| >= D0' > 0` for all `y ∈ N` and all
`i`. Let `rho' = min(rho, D0'/(4K0))` and `theta' = D0' rho'/4`. If `y ∈ N ∩ C`,
`pi_D(C, y) > f* - eps` and `m(y) + eps < theta'`, then for every `i`

```
y_i - l_i < 4(m(y) + eps)/D0'   and   u_i - y_i < 4(m(y) + eps)/D0',
```

so `C` has width below `8(m(y) + eps)/D0'` in every coordinate.

*Proof.* Take the one-sided segment `U' = y + [0, delta] e_i` with
`delta = min(u_i - y_i, rho')`, and write `phi_j(s) = t_j(y + s e_i)` and
`x^- = max(-x, 0)`. By Taylor's theorem,
`min_{[0,delta]} phi_j <= phi_j(0) - delta phi_j'(0)^- + H_j delta^2/2` and
`max - min <= delta |phi_j'(0)| + H_j delta^2`. Since
`sum_j phi_j'(0)^- = (sum_j |phi_j'(0)| - d_i f(y))/2`, Lemma 4.1 gives

```
pi_D(C, y) <= f(y) - (delta/2)(D_i(y) - d_i f(y)) + K0 delta^2 <= f(y) - delta D0'/2 + K0 delta^2 <= f(y) - delta D0'/4.
```

As in Theorem 5.1, this forces `delta < 4(m(y) + eps)/D0' < rho'`, so
`delta = u_i - y_i`. The segment `y + [-delta, 0] e_i` gives the same with
`D_i(y) + d_i f(y)`, which bounds `y_i - l_i`. □

Near a stationary point `d_i f(y) ≈ 0`, so CND alone gives it. The check
([`check_revision.log`](logs/check_revision.log), part (D)) samples 600 boxes
around points near the `linediag` optimal line (expanded form). In the 125
cases where `y` was removed, the farthest face was at most 0.37 times the
bound. That check did not verify `m + eps < theta'`. The recheck verified the
hypotheses point by point and found 0 violations in 909 removals. Its
adversarial search reached 0.50 of the bound. The first-order witness predicts
`2(m + eps)/(D_i ∓ d_i f)`, so the constant 4 is within a factor 2 of sharp.

**Theorem 5.2 (relaxation lower bounds survive).** In the setting of Theorem
5.1, let `alpha_eff = min(alpha, alpha_F)` and
`N_theta = {y ∈ N : m(y) + eps < theta}`. For every hybrid run of Section 2
(any branching, node order, incumbents, propagation schedule and number of
rounds), the family `P` of Lemma 2.1 satisfies (V) with `alpha_eff` at every
point of `N_theta`. Consequently:

(a) for every `eta >= 0` with `eps + eta < theta`,
`|P| >= 2^(-n) N_inf(E(eta) ∩ N, 2 sqrt((eps + eta)/alpha_eff))`;

(b) `|P| >= (alpha_eff n/pi^2)^(n/2) integral_{N_theta} (m + eps)^(-n/2) dy`;

(c) if every node has at most one propagation phase and no other reduction,
the number of processed nodes is at least `|P|/(2n+1)`.

In particular:
- if `M ∩ N` contains a relatively open piece of a `p`-dimensional `C^1`
  submanifold, then `|P| = Omega(eps^(-p/2))` for every hybrid run;
- if `N` is a neighbourhood of an isolated minimizer `x*` with
  `m(y) <= Gamma |y - x*|^2` near `x*`, then `|P| = Omega(log(1/eps))`.

The same rates hold for the number of processed nodes whenever the number of
propagation phases and reduction rounds per node is bounded (Lemma 2.1(c)).

*Proof.* Lemma 2.1(b) certifies each point by (V) with `alpha`, or by (Π),
and Theorem 5.1 turns (Π) into (V) with `alpha_F`. Then apply Theorem 2.2 with
the covering bound (constrained note, Theorem 4.6) and the integral bound
(constrained note, Theorem 3.1). Both proofs use (V) only at the points they
count. The two consequences are the covering number of a `p`-dimensional piece
at scale `sqrt(eps)`, and the integral
`integral (Gamma |y - x*|^2 + eps)^(-n/2) dy >= c_n Gamma^(-n/2) log(1/eps) - O(1)`. □

This is the requested statement: with interval cutoff propagation to the
fixed point, on any CND representation, the number of leaves is at least a
covering number of the near-optimal set by cubes of side
`2 sqrt((eps+eta)/alpha_eff)`. Since `alpha_F` does not depend on `eps`, the
`eps`-exponents of the relaxation-gap theory (half the box-counting dimension
of `M`; `log(1/eps)` at nondegenerate points) survive.

**Example 5.3 (`linediag`, expanded form).** On the part `t ∈ [0.2, 1.1]` of
the optimal line:
- `D0 = 2.352`, and `K0 = 322.7` over segments `|s| <= 1`, so
  `rho* = 0.0036`;
- `alpha_F = D0/(2 n s0) = 0.140` (`n = 2`, `s0 = 4.2`), so `alpha_eff = 0.140`;
- the theorem applies for `eps + eta < theta = 4.3e-3`.

With `eta = 0`, Theorem 5.2(a) gives `|P| >= 1.5, 4.25, 13.5, 42.3` at
`eps = 10^-3..10^-6`. Every hybrid run therefore has `Omega(eps^(-1/2))` nodes.
The observed counts (1325, 4035, 14557, 42345 with fixed-point propagation) are
about 1000 times larger and grow at the same rate. The constant is poor: `D0`
is taken at the worst point, and the covering bound loses `2^n`.

**Theorem 5.4 (face-type loss: `log(1/eps)` survives at isolated minima).** Let
`n >= 2` and let `x*` be an isolated minimizer with `Q(x*, 2 rho0) ⊆ X0`.
Assume:
- (QG) `m(y) >= gamma |y - x*|_inf^2` on `Q(x*, 2 rho0)`;
- `|d_i m| <= L0/8` on `Q(x*, 2 rho0)` for every `i`;
- (ND1) `L(y) >= L0 > 0` for `y ∈ N = Q(x*, rho0)`, with the terms `C^2` on
  the cubes `y + [-rho1, rho1]^n` and cube remainder constant
  `K0 >= n^2 (sum_j H_j/2 + max_j H_j)` there.

Let `rho* = min(rho0, rho1, L0/(2K0))`, `theta = L0 rho*/2` and
`N_theta = {y ∈ N : m(y) + eps < theta}`. Then every hybrid family satisfies

```
|P| >= integral_{N_theta} (m + eps)^(-n/2) dy  /  (K_R + K_F),
K_R = (pi^2/(alpha n))^(n/2),     K_F = (16 n (n-1) 2^n rho0 / (3 L0)) (5/4)^(n/2) gamma^(1 - n/2).
```

If also `m(y) <= Gamma |y - x*|_inf^2` near `x*`, the right-hand side is
`Omega(log(1/eps))`.

*Proof.* *Face localization.* Let `y ∈ N_theta` be certified by (Π) in `C`, and
let `delta = min(min_i d_i^C(y), rho*)`. The cube `y + [-delta, delta]^n` lies
in `C`, and Lemma 4.4 gives
`f* - eps < f(y) - L0 delta + K0 delta^2 <= f(y) - L0 delta/2`. As in Theorem
5.1, `min_i d_i^C(y) < r(y) := 2(m(y) + eps)/L0 < rho*`.

*Per-member integral of the (Π)-points.* They lie in the `2n` layers
`{y ∈ C ∩ N_theta : y_i - l_i < r(y)}` and `{u_i - y_i < r(y)}`. Take the layer
at `y_1 = l_1`, write `y = (l_1 + s, z)`, and let `y' = (l_1, z)`. Since
`s < r(y) < rho0` and `y ∈ Q(x*, rho0)`, the segment `[y', y]` lies in
`Q(x*, 2 rho0)`. So `|m(y) - m(y')| <= (L0/8) s < (m(y) + eps)/4`. With
`M(z) = m(y') + eps`, this gives `(3/4)(m(y)+eps) < M(z) < (5/4)(m(y)+eps)`.
Hence `s < (8/3) M(z)/L0` and `(m(y)+eps)^(-n/2) < (5/4)^(n/2) M(z)^(-n/2)`.
Integrating over `s` first,

```
integral_layer (m + eps)^(-n/2) <= (8/(3 L0)) (5/4)^(n/2) integral_{|z - z*|_inf <= 2 rho0} M(z)^(1 - n/2) dz,
```

where `z*` is `x*` without its first coordinate. By (QG),
`M(z) >= gamma |y' - x*|_inf^2 >= gamma |z - z*|_inf^2`. For `n = 2` the
integrand is 1 and the integral is at most `4 rho0`. For `n >= 3`, with the
layer-cake formula,
`integral |z - z*|_inf^(2-n) dz = integral_0^(2 rho0) t^(2-n) (n-1) 2^(n-1) t^(n-2) dt = (n-1) 2^n rho0`.
In both cases the layer contributes at most
`(8/(3L0))(5/4)^(n/2) (n-1) 2^n rho0 gamma^(1-n/2)`, and the `2n` layers give
`K_F`.

*(V)-points* contribute at most `K_R` per member (constrained note, proof of
Theorem 3.1).

*Covering.* Every point of `N_theta` is certified by some member, so
`integral_{N_theta} (m+eps)^(-n/2) <= |P| (K_R + K_F)`. The last claim follows
because `N_theta` contains a fixed cube around `x*` once `eps < theta/2`, and
`integral_{Q(x*, r1)} (Gamma |y-x*|_inf^2 + eps)^(-n/2) dy >= n 2^(n-1) (2 Gamma)^(-n/2) log(Gamma r1^2/eps)`. □

For `n = 2`, `K_F` does not involve `gamma`. For the rotated instances
`rot_kappa` (expanded form; `L = 8` at the minimizer independently of
`kappa`), the integral is about `2 pi (det H)^(-1/2) log(1/eps)` once
`eps << kappa rho0^2`, where `H` is the Hessian at the minimizer and
`det H = 72 kappa`. (The hypothesis `|d_i m| <= L0/8` on `Q(x*, 2 rho0)` forces
`rho0 <~ 1/36` here, since the Hessian rows have absolute sum 18; the cube
`N_theta` cuts off the soft direction at `rho0`, so the condition is about
`eps << 8e-4 kappa`.) The other constants do not depend on `kappa`, because the
largest eigenvalue (18) controls `rho0` and `n = 2` removes `gamma`. So the
lower bound grows like `kappa^(-1/2) log(1/eps)`: the square root of the
condition number times `log(1/eps)`.
The observed node counts per decade are 20, 55 and 168 for
`kappa = 1, 0.1, 0.01`, with or without propagation (ratios 2.75 and 3.05
against `sqrt(10) = 3.16`).

**Face localization is sharp.** Theorem 5.4 cannot be strengthened to vertex
localization. For `iso2` in expanded form, propagation empties the strip
`[1 - h, 1 + h] x [0.5, 1.5]` through the minimizer as soon as `8h < eps`,
whatever its length (Corollary 3.5 and
[`check_constants.log`](logs/check_constants.log)). At the minimizer `(1,1)`
such a strip has `q_C >= 1/4`, so it violates (V) whenever `alpha > 4 eps`.
Hypothesis (Π ⇒ V_beta) of Theorem 2.2 therefore fails for this
representation; the integral argument above is what rescues the bound. The rotated instance behaves
differently: the strip `[1 ± h] x [-0.5, 0.5]` keeps `pi_D ≈ -0.85` as
`h -> 0`. Its bilinear terms couple the long side into the loss.

**Theorem 5.5 (transversal optimal curves).** Assume (ND1) with the constants
of Theorem 5.4 on a set `N`, and let `S ⊆ E(eta) ∩ N` be a compact connected
`C^1` curve whose unit tangent satisfies `|tau_i| >= tau0 > 0` for every `i`.
Let `eps + eta < theta`. Then every hybrid family satisfies

```
|P| >= tau0 H^1(S) / (2^(n+1) r_R + 4 n r_F),     r_R = sqrt((eps + eta)/alpha),   r_F = 2(eps + eta)/L0.
```

So a transversal optimal curve still forces `Omega(eps^(-1/2))` nodes.

*Proof.* Each coordinate is strictly monotone along `S`, so the part of `S` in
a slab `{|y_i - v| <= r}` is one arc of length at most `2r/tau0`. A point of
`S` certified by (V) in `C` lies in `Q(v, r_R)` for a vertex `v` of `C`
(constrained note, proof of Theorem 4.6). The `2^n` vertices account for arc
length at most `2^(n+1) r_R/tau0`. A point certified by (Π) lies within `r_F`
of one of the `2n` face hyperplanes of `C` (proof of Theorem 5.4), which
accounts for at most `4n r_F/tau0`. Summing over the cover gives the claim. □

**Remark 5.6 (higher-dimensional optimal sets).** The argument of Theorem 5.5
extends to `p`-dimensional transversal pieces, with face layers contributing
`O(r_F diam^(p-1)) = O(eps)` of `p`-dimensional measure per member and vertex
cubes `O(eps^(p/2))`. For `p <= 2` this preserves the exponent `p/2`. For
`p >= 3` it gives only `Omega(eps^(-1))`. Whether propagation with only
face-type loss can beat `eps^(-p/2)` for `p >= 3` is open (Section 9). Under
CND, Theorem 5.2 settles every `p`.

## 6. What decides the outcome: representation, dependency, and level sets

**When propagation alone proves `eps`-optimality.** With `UBD = f*`, the
propagation fixed point at the root proves `eps`-optimality exactly when
`pi_D(X0) > f* - eps` (Proposition 1.4). It does so for every `eps > 0` exactly
when `pi_D(X0) = f*`, that is, when the representation's hull consistency
certifies the global lower bound. With branching, it does so with a number of
boxes independent of `eps` when it certifies `f >= f*` on all small boxes near
`M` (Theorem 3.8). Sections 3–4 translate this into conditions on the
representation:
- *Dependency.* The fixed point gains at most one term's width over forward
  evaluation (Corollary 4.2). So exactness needs the forward excess to sit in
  one term. For flat separable sums, Theorem 3.1 gives the exact bound.
- *One-sidedness.* At a stationary point of a univariate flat sum, either one
  term carries its whole sign class of derivatives, and propagation is exact
  nearby, or no term dominates, and the loss is first order (Remark 3.4,
  Lemma 4.4).
- *Separable sums.* Propagation is exact along each coordinate given the
  others' bounds, but it sees the other coordinates only through their forward
  bounds. With two or more coordinates having forward excess, the loss is
  cross-coordinate and still first order (Corollary 3.5).
- *Lifted geometry.* The sublevel set must be box-like in the lifted
  coordinates exposed by the DAG (Proposition 3.6). Rotation in `x` is no
  obstacle if the rotated coordinates are nodes of the DAG.

**Box-likeness in `x` matters for contraction, not for pruning.** With
`UBD = f*` the cutoff `f* - eps` has an empty sublevel set, so only `pi_D`
matters. With a poor incumbent, `UBD - eps > f*`, the best any propagation can
do is shrink `C` to the bounding box of `{x ∈ C : f(x) <= UBD - eps}`. For a
quadratic sublevel set `{x : x^T A x <= r}` this box has half-widths
`sqrt(r (A^-1)_ii)`. Its volume divided by that of the ellipsoid is
`(2^n/omega_n) (prod_i (A^-1)_ii / det A^-1)^(1/2) >= 2^n/omega_n` (Hadamard),
where `omega_n` is the volume of the unit ball. For a 45-degree rotation in 2D
with eigenvalues `lambda_1, lambda_2`, the ratio is
`(2/pi)(sqrt(lambda_1/lambda_2) + sqrt(lambda_2/lambda_1))`, which grows like
the square root of the condition number. So box-likeness of level sets
controls how much contraction can achieve before the incumbent is optimal;
the node model of the program (`UBD = f*`) does not see it.

**Same function, same relaxation, different representation.** Every pair
below has identical `f` and identical alphaBB bounds; only the DAG differs
(Table 7.1).

| instance | exact representation (fixed point) | expanded monomials (fixed point) | no propagation |
|---|---|---|---|
| `linediag`, optimal segment | 1 node | `Omega(eps^(-1/2))` proved (Theorem 5.2); 42345 at `10^-6` | 42349 at `10^-6` |
| `line3`, optimal line in 3D | 1 node | same as without (25475 at `10^-4`) | 25475 at `10^-4` |
| `rot_kappa`, isolated minimizer | 1 node | `Omega(log(1/eps))` proved (Theorem 5.4); `~ kappa^(-1/2) log(1/eps)` observed | same, 2 more nodes |
| `nondeg1s` (1D) | 1 node, 4 rounds (centered) | 1 node, `2.79/sqrt(eps)` rounds | `Theta(log(1/eps))` |

Upper rates for runs with propagation are observed, not proved. The
constrained note's bisection upper bounds are for trees without contraction,
and "propagation can only help" is not a theorem about tree size, because
contraction changes the split points.

A solver sees whichever DAG its presolve produces. SCIP, for example, expands
squares of sums by default (the other workstream's
[instances](../solver-validation/instances.py) note "SCIP expands the
square"). The theory predicts that such expansions switch instances from the
exact column to the expanded column. That is consistent with the other
workstream's SCIP counts (Section 7.4).

## 7. Computations

### 7.1 Setup

- [`fbbt.py`](fbbt.py): interval HC4 on a DAG with `lin` (n-ary sum), `mul`
  and integer `pow` nodes. Each revise is the hull of the exact projection of
  one elementary constraint (extended division for products whose factor
  interval contains 0). A round is a forward pass, the cutoff, and a backward
  pass. Mode `fix` iterates until no bound changes by more than `10^-15`
  relatively (at most `2*10^5` rounds per node; the limit was never hit). Mode
  `R` runs at most `R` rounds. Floating point, no outward rounding.
- [`bb.py`](bb.py): the program's node model. `UBD = f*` from the start; prune
  when the bound is `>= f* - eps`; per node, one propagation phase (if
  enabled), then the uniform alphaBB bound on the contracted box, then
  widest-side bisection at the midpoint. The alphaBB minimum is computed by
  L-BFGS-B. The reported bound is the linearization bound at the returned
  point, which is valid for a convex objective. `alpha` is at least half the
  most negative Hessian eigenvalue on the root box (checked on a grid by
  `instances.min_hessian_eig`).
- [`instances.py`](instances.py): instances and representations. Every
  representation matches `f` to `6e-14` on 200 random points.
- [`sweep.py`](sweep.py), [`sweep3.py`](sweep3.py),
  [`sweep_nd2.py`](sweep_nd2.py): runs; [`tables.py`](tables.py): tables. The
  full tables, with every `eps`, are in [`logs/tables.md`](logs/tables.md).

### 7.2 Node counts

**Table 7.1.** Processed nodes; for propagation runs, the total number of HC4
rounds in brackets. `fix` = fixed point, `R` = rounds per node. `—` = not run;
`*` = stopped at `4*10^5` nodes. "Growth" is the least-squares slope of
`log nodes` against `log(1/eps)` over the last four values, or nodes per
decade for logarithmic cases.

| instance (`alpha`) | representation | FBBT | `10^-2` | `10^-4` | `10^-6` | `10^-8` | growth |
|---|---|---|---|---|---|---|---|
| `nondeg1` (13/3) | — | off | 13 | 29 | 45 | 57 | 7/decade |
| | `mono` | fix | 1 [4] | 1 [6] | 1 [6] | 1 [7] | 0 |
| | `u` | fix | 1 [3] | 1 [4] | 1 [4] | 1 [4] | 0 |
| `nondeg1s` (13/3) | — | off | 13 | 29 | 45 | 57 | 7/decade |
| | `centered` | fix | 1 [3] | 1 [4] | 1 [4] | 1 [4] | 0 |
| | `exp` | fix | 1 [43] | 1 [298] | 1 [2812] | 1 [27944] | rounds `2.79/sqrt(eps)` |
| | `exp` | 10 | 5 | 17 | 31 | 47 | 7/decade |
| `h1` (1.5) | — | off | 11 | 17 | 23 | 31 | 3/decade |
| | `exp` | fix | 1 [54] | 1 [587] | 1 [5919] | 1 [59233] | rounds `5.92/sqrt(eps)` |
| | `exp` | 10 | 5 | 9 | 17 | 23 | 3/decade |
| | `exp` | 3 | 7 | 13 | 19 | 27 | 3/decade |
| `nd2` (4.5) | — | off | 107 | 241 | 369 | 493 | 64/decade |
| | `mono` | fix | 17 [47] | 17 [68] | 17 [70] | 17 [70] | 0 |
| | `mono` | 10 | 17 | 17 | 17 | 17 | 0 |
| `iso2` (1.5) | — | off | 41 | 73 | 97 | 133 | 17/decade |
| | `exp` | fix | 29 | 55 | 93 | 115 | 15/decade |
| | `exp` | 10 | 29 | 55 | 93 | 115 | 17/decade |
| `rot1` (3) | — | off | 73 | 111 | 157 | 195 | 20/decade |
| | `exp` | fix | 71 | 109 | 155 | 193 | 20/decade |
| | `st` | fix | 1 [55] | 1 [588] | 1 [5920] | 1 [59234] | 0 |
| `rot0.1` (3) | — | off | 135 | 235 | 343 | 447 | 55/decade |
| | `exp` | fix | 133 | 233 | 341 | 445 | 55/decade |
| | `st` | fix | 1 | 1 | 1 | 1 | 0 |
| `rot0.01` (3) | — | off | 273 | 575 | 899 | 1235 | 168/decade |
| | `exp` | fix | 271 | 573 | 897 | 1233 | 168/decade |
| | `st` | fix | 1 | 1 | 1 | 1 | 0 |
| `linediag` (3) | — | off | 471 | 4037 | 42349 | — | `eps^(-0.51)` |
| | `exp` | fix | 469 | 4035 | 42345 | — | `eps^(-0.51)` |
| | `exp` | 10 | 469 | 4035 | 42345 | — | `eps^(-0.51)` |
| | `s` | fix | 1 [55] | 1 [588] | 1 [5920] | 1 [59234] | 0 |
| | `s` | 10 | 313 | 4137 | 43555 | 400001* | `eps^(-0.50)` |
| | `s` | 3 | 371 | 4273 | 42649 | 400001* | `eps^(-0.50)` |

Three-variable instances (Table 7.1, continued):

| instance (`alpha`) | representation | FBBT | `10^-1` | `10^-2` | `10^-3` | `10^-4` | `10^-6` | growth |
|---|---|---|---|---|---|---|---|---|
| `iso3` (1.5) | — | off | 89 | 143 | 199 | 241 | 333 | 45/decade |
| | `exp` | fix | 75 | 133 | 185 | 217 | 291 | 35/decade |
| `line3` (3) | — | off | 603 | 2235 | 7559 | 25475 | — | `eps^(-0.54)` |
| | `exp` | fix | 603 | 2235 | 7559 | 25475 | — | `eps^(-0.54)` |
| | `st` | fix | 1 | 1 | 1 | 1 | — | 0 |
| | `st` | 10 | 147 | 1549 | 6577 | 23387 | — | `eps^(-0.72)` |

Instances: `nondeg1` is `t^2 - 2t^4` on `[-1/3, 2/3]` (the review's);
`nondeg1s` is the same function of `y = t + 1/3` on `[0,1]`; `h1` is
`h_{1/2}(s)` on `[-2, 2.2]`; `nd2` is `x^2 - 2x^4 + y^2 - 1.5 y^4` on
`[-0.6, 0.55] x [-0.55, 0.62]` (the other workstream's `isofbbt2`); `iso2` and
`iso3` are `sum h_{c_i}(x_i)` with `c = (0.5, 0.7, 0.6)`; `rot_kappa`,
`linediag` and `line3` are as in Examples 3.7. Boxes are in
[`instances.py`](instances.py).

**Agreement with the theory.**
- *Exact representations* (`mono`, `u`, `centered`, `s`, `st`, `nd2`): `O(1)`
  nodes, as Theorem 3.8 and Examples 3.7 predict. Fixed-point rounds grow like
  `eps^(-1/2)` where some base has cancelling term derivatives at the
  minimizer, including `rot_kappa`/`st` and `line3`/`st`, whose stationary
  `t^2` term does not matter (Proposition 3.9, Heuristic 3.8a). They stay at
  3–7 for `nondeg1`, where no base has cancellation (Proposition 3.10).
- *Expanded representations with loss* (`linediag`, `line3`, `rot`, `iso2`,
  `iso3` in `exp`): the same exponent as without propagation. The
  `eps^(-1/2)` rate on `linediag` is Theorem 5.2 (CND on part of the line,
  Example 5.3). The `log(1/eps)` rates on `rot`, `iso2` and `iso3` are Theorem
  5.4. Propagation removes 2–4 nodes on `linediag` and `rot`, and 4–39 % of
  the nodes on `iso2` and `iso3`, where it empties thin boxes
  (face-type loss).
- *Bounded rounds* (`R = 3, 10`): where some base has cancelling term
  derivatives at the minimizer (`linediag`/`s`, `h1`, `nondeg1s`), the growth rate of the
  propagation-free runs is unchanged (Conjecture 3.11). `line3`/`st` is
  undecided over the tested range (exponent 0.72 against 0.54). Where no base
  has cancellation (`nondeg1`, `nd2`), 10 rounds reach the fixed point and
  give `O(1)` nodes, as the quadratic convergence of Proposition 3.10
  suggests.
- *Prefactor:* nodes per decade on `rot_kappa` scale like `kappa^(-1/2)`,
  as in the remark after Theorem 5.4.

### 7.3 Checks of individual statements

- [`check_formula.py`](check_formula.py) → [`logs/check_formula.log`](logs/check_formula.log):
  Theorem 3.1 on 450 random flat separable sums (Remark 3.2); also documents
  the rejected full-range version.
- [`check_loss.py`](check_loss.py) → [`logs/check_loss.log`](logs/check_loss.log):
  `pi_D` of cubes of radius `r = 0.1..0.001` around optimal points, by
  bisection on `c` with HC4 (a round limit counts as "not empty", so the
  estimate can only be low). Exact representations give `pi_D = f*`
  (`-9e-8`, the bisection resolution). Expanded ones give first-order losses of
  at least the predicted `L r` (Section 4).
- [`check_constants.py`](check_constants.py) → [`logs/check_constants.log`](logs/check_constants.log):
  the CND constants and lower bounds of Example 5.3, and the thin-strip test
  after Theorem 5.4.
- [`rounds.py`](rounds.py) → [`logs/rounds.log`](logs/rounds.log): root
  round counts for Propositions 3.9 and 3.10.
- [`check_revision.py`](check_revision.py) → [`logs/check_revision.log`](logs/check_revision.log)
  (added in the revision): the endpoint example after Remark 3.2; merged
  phases with restarts and inherited bounds (Lemma 2.1(b)); `h_{1/2}` on
  `s < 0`; two-sided localization (Proposition 5.1a).

### 7.4 Comparison with the SCIP runs of the other workstream

The workstream `solver-validation/` (not part of this note, not re-run here)
ran SCIP 10.0.2 on related instances
([summary](../solver-validation/results/summary.md)). Its setting `noweakdual`
forbids every reduction that uses the cutoff; `nocutoffprop` switches off only
some propagators (pseudo-objective and reduced-cost), and on `isofbbt2` only
`noweakdual` changes the count. The comparison is only qualitative: SCIP's
representation, bounding and branching differ from the toy model, and SCIP
also tightens auxiliary-variable bounds by OBBT, which is outside the model
of Section 2.
- `linediag2` (`h(x1 - x2)` with SCIP expanding the square): 65701 nodes at
  `10^-6` by default, 66661 with `noweakdual`. This matches the loss column.
- `ring2` (`(x1^2 + x2^2 - 1)^2`): with the square expanded (SCIP's
  default), 56151 nodes at `10^-6` and 66991 with `nocutoffprop`. With the
  square not expanded (`noexpand`), 1 node for every `eps`: the unexpanded
  square has a nonnegative forward interval (Section 2).
- `isofbbt2` (= `nd2`): 15 nodes for every `eps` by default, and 37 with
  `noweakdual`. This matches the 17 nodes of Table 7.1 and Example 3.7(e).

SCIP also applies only relative tightenings above a threshold (Section 8). So
it cannot reach the slow fixed points of Proposition 3.9 and behaves like the
bounded-round rows.

## 8. Literature comparison and novelty

Sources: the local full texts in
[`literature/papers/`](../../../literature/papers/), with page numbers from
their page markers. A delegated reader extracted most quotations. Those from
Wechsung et al. (p.8), Araya et al. (p.3) and Neumaier (p.29) were checked
against the local texts for this revision. Sources marked "(via the review)"
were read by the independent review's delegated reader, partly from the web;
they were not checked here. General web search was unavailable (session quota
exhausted).

| Source | What it gives | Relation to this note |
|---|---|---|
| Benhamou, Goualard, Granvilliers, Puget (1999), *Revising hull and box consistency* (via the review); Bordeaux, Hamadi, Vardi (2007); Dlask, Werner (2024) | HC4; confluence: "the output is independent of the reinvocation order of constraints"; greatest fixed points. Benhamou et al. (§4.1): "the exact characterization of the result provided by the execution of HC4revise is still an open problem" | Section 1 is known. Theorem 3.1 characterizes the HC4 **fixed point** (not one revise) for flat sums of univariate terms |
| Belotti, Cafieri, Lee, Liberti (2012 preprint), *On feasibility based bounds tightening* | FBBT as "a monotone deflationary operator … its limit point as its greatest fixed point" (p.10); non-finite convergence (pp.8, 12) | Lemma 1.1 is this fact for arbitrary schedules; not claimed as new. The objective enters only as an epigraph constraint (p.3) |
| Schichl, Neumaier, JOGO 33 (2005), *Interval analysis on directed acyclic graphs* | Forward and backward propagation on DAGs; with a feasible point, "we can introduce the new constraint f(x) ≤ fbest" (p.11), with a worked example (pp.12–13) | The mechanism modelled here. No exactness statement or node-count analysis was found |
| Schichl, Markót, Neumaier (2014 preprint, §2) and Schichl, Neumaier (2004, §3) (via the review) | "constraint propagation techniques lead to overestimation of order k = 1, hence they suffer from the cluster effect", stated without proof | The note refines this. For flat sums with first-order loss it is proved in a node-count form (Lemma 4.4, Theorems 5.2–5.5). For one-sided representations it is false: the loss is zero and there is no cluster (Corollary 3.3, Theorem 3.8), although the cost can move into rounds (Proposition 3.9) |
| Araya, Trombettoni, Neveu (2010), *Exploiting monotonicity in interval constraint propagation* | "HC4-Revise is known to achieve the hull-consistency of constraints having no variable with multiple occurrences" (p.2); with multiple occurrences it is "generally not optimal" (p.1); a monotonicity-based revise is optimal when `f` is monotone in the multiply occurring variables (Props. 1, 4). Example: for `x^2 - 3x + y = 0` on `[4,10] x [-80,14]`, "a standard HC4-Revise … would have brought no contraction" (p.3) | Single-use exactness (Lemma 4.1, Corollary 4.2) is known. The example is prior evidence of fixed-point dependency loss: the review checked that the fixed point for the equation keeps `y ∈ [-80, 14]`, although the hull is `[-70, -4]`. Theorem 3.1 explains the inequality half `f <= 0`: the whole box is a witness, `Phi(C) = 16 - 30 - 80 + max(84, 18, 94) = 0`, although the hull of `{f <= 0}` has `y <= -4`. It also shows that exactness of the bound `pi_D` (here one-sided in `x`) does not imply exact contraction. Monotonicity-based exactness differs from Corollary 3.3, which allows non-monotone `f` and gets exactness only at the fixed point of plain HC4 |
| Du, Kearfott, JOGO 5 (1994); Wechsung, Schaber, Barton, JOGO 58 (2014); Kannan, Barton (2017) | "In problems in which the lower bound given by the interval extension F is exact, there will be no cluster even though F is not of high order" (Du–Kearfott, p.9); "When K is sufficiently small, i.e., K ≤ λ1/8, the cluster problem is completely absent (N = 1)" (Wechsung et al., p.8) | Theorem 3.8 is this known principle applied to the propagation bound `pi_D`. New are the conditions under which `pi_D` is exact (Corollary 3.3, Proposition 3.6) |
| Neumaier, Acta Numerica (2004) | Pruning "is equivalent to adding the constraint f(x) ≤ fbest" (p.35); separable constraints give "an optimally reduced box" (p.40), block-separable ones need "suboptimal interval techniques" (p.43); fixed-point convergence "may be arbitrarily slow" (p.42); the cluster effect disappears with overestimation `o(eps^2)` (p.44); "pathological exceptions include min x − x s.t. x ∈ [0, 1]" (p.29) | Corollary 3.5 refines the separable statement: with each coordinate's range computed exactly (`e_k = 0`) propagation is exact; with term-wise ranges the loss is cross-coordinate and first order. The `x - x` example is the folklore behind Proposition 2.3. Section 3.3 quantifies "arbitrarily slow" in the exact case |
| Vu, Schichl, Sam-Haroud (2009); Faltings (1994) (via the review) | DAG against tree representations; non-termination of continuous propagation | Representation dependence and slow convergence are known in general. The rates `Theta(eps^(-1/2))` (Proposition 3.9) and `O(log log(1/eps))` (Proposition 3.10) were not found |
| Belotti, Lee, Liberti, Margot, Wächter, OMS (2009), Couenne | The downward pass uses "an upper bound x̂_{n+q}" on the objective auxiliary (p.11); "the upper bound helps eliminate part of the solution set" (p.23); node counts empirical | The cutoff propagation modelled here, in a solver; no theory |
| Vigerske, Gleixner (2017), SCIP; Bestuzheva et al. (2025), SCIP | Nonlinear objective moved to an auxiliary variable (2017, p.34; 2025, p.2); primal bound used in bound tightening (2017, p.17); tightenings propagated only above a relative threshold (2017, p.7); term-wise propagation "suffering from the so-called dependency problem" (2025, p.10) | The threshold is why SCIP behaves like bounded rounds on slowly converging instances (Section 7.4) |
| Domes, Neumaier, Constraints (2010) | Univariate quadratic terms get "the best interval" (p.4); bilinear terms are eliminated, and "approximating the bilinear entries in different ways can lead to different results" (pp.11–12) | Exact per univariate term, which is `e_k = 0` in Corollary 3.5. Example 4.3 shows the bilinear loss that such eliminations face |
| Puranik, Sahinidis, Constraints (2017), survey | The fixed point "is independent of the order" but may not be reached finitely (p.9); domain reduction "not even necessary to prove convergence" (p.9); node reductions empirical (pp.15–16); "at least second-order convergence is required to overcome the cluster effect" (p.15) | No theorem relating cutoff propagation to node counts was found |
| Tawarmalani, Sahinidis, MP (2004) | Feasibility-based reduction with "the objective function cut" is a special case of duality-based tightening (p.21) | Same mechanism; no node-count theory |
| Constrained note and its reviews; Bachoc–Cesari–Gerchinovitz (2021); Hansen–Jaumard–Lu (1991); Neumaier (2004, §15) | Relaxation-gap and Lipschitz lower bounds | Section 5 transfers those bounds to hybrid runs |

**Known.**
- The facts of Section 1: greatest fixed point, confluence, schedule
  independence.
- The principle behind Theorem 3.8, that an exact bound gives no cluster
  (Du–Kearfott; Wechsung et al.; Kannan–Barton).
- Representation dependence in general, and Proposition 2.3, which is
  folklore.
- Slow and non-finite convergence of propagation in general.

**Not examined:**
- Hansen and Walster, *Global Optimization Using Interval Analysis* (2004),
  which uses hull and box consistency on `f(x) <= f̄` and is the most likely
  place for close prior statements;
- Collavizza, Delobel and Rueher (1999), *Comparing partial consistencies*;
- Kearfott (1996); Ratschek and Rokne (1988); Messine (2004); Apt (1999);
  Moore (1966);
- the journal version of Schichl, Markót and Neumaier (2014).

**What is claimed as new, as far as the sources checked go.**
- The node-bound view of fixed-point cutoff propagation, combined with a
  hybrid certificate family whose propagation frames may be merged (Lemma 2.1)
  and the transfer principle (Theorem 2.2).
- The characterization of the HC4 fixed point for flat sums of univariate terms
  with multiple occurrences (Theorem 3.1). This includes the role of endpoint
  support, the one-sided exactness criterion, the separable identity, and
  lifted box-likeness (Corollaries 3.3, 3.5, Proposition 3.6).
- The bound "fixed point gains at most one term's width" (Corollary 4.2), the
  first-order loss constants (Lemma 4.4), and the localization results
  (Theorem 5.1, Proposition 5.1a).
- Lower bounds for spatial branch-and-bound with cutoff propagation included
  (Theorems 5.2, 5.4, 5.5). No lower bound on node counts that survives
  propagation was found in the cluster literature, whose analyses are upper
  bounds or worst-case counts and do not model domain reduction.
- The round-count results (Propositions 3.9–3.10).

The individual tools (hull consistency, Moore's single-use theorem, the
covering and integral arguments) are standard, and the mathematical steps are
short once the witness lemma is available. Constraint-programming work on the
optimality of HC4 for sums may contain Theorem 3.1 or special cases. That
literature was searched only through the sources above. An unsuccessful search
does not establish novelty.

## 9. Open problems and conjectures

1. **Bounded rounds in exact representations** (Conjecture 3.11). Prove that
   `R` rounds per node do not change the growth rate at optimal sets where
   the representation is one-sided and some base has cancelling term
   derivatives.
   Settle `line3`, which is undecided over the tested range. This is the regime of real solvers,
   because of round limits and relative tightening thresholds. A proof would
   need a witness family for the iterates rather than for the fixed point.
2. **Face-type loss for `p >= 3`** (Remark 5.6). Can propagation with only a
   cube loss (ND1, not CND) beat `eps^(-p/2)` on optimal sets of dimension
   `p >= 3`? An instance or a sharper covering argument would settle it.
3. **Constrained problems.** The witness lemma must then produce boxes that
   are also hull-consistent for the constraint propagators. Open, including
   whether constraint propagation can remove the constraint-gap lower bounds on
   curved strata (constrained note, Open problem 3).
4. **General DAGs.** Characterize `pi_D` beyond flat sums (nested sums,
   products of sums, shared subexpressions). Approximating FBBT limits of
   bilinear equality systems is PosSLP-hard (repository result
   [`fbbt-monotone-system-hardness.md`](../../../results/fbbt-monotone-system-hardness.md)).
   That is a related but different question from computing `pi_D`. It
   suggests that no efficiently computable characterization covers all DAGs
   unless PosSLP is in P.
5. **Round counts.** A matching upper bound `O(a/sqrt(eps))` in Proposition
   3.9; a schedule-free version counting revise steps; a proof or refutation
   of Heuristic 3.8a; and the
   `O(log log(1/eps))` rate for the monomial form of `t^2 - 2t^4`. The observed
   constants are `pi a` for the quadratic, `5.92` for `h_{1/2}` and `2.79` for
   `nondeg1s`.
6. **Choosing the representation.** Theorem 3.8 and Proposition 3.6 reward
   DAGs that expose the coordinates in which the sublevel set is box-like
   (common linear forms, sums of squares). Detecting such rewritings, and
   their cost in propagation rounds, is a representation-design question that
   the relaxation-gap theory does not see.
7. **Relative tolerances and thresholds.** Model SCIP's relative tightening
   threshold explicitly and show that it yields the bounded-round behaviour.
8. **Lifted-space reductions.** Extend Lemma 2.1 to OBBT or reduced-cost
   tightening of auxiliary variables interleaved with propagation, and to
   branching on auxiliary variables. Both are excluded from the model.

## 10. Checks run

All from `research-20260928b/bb-complexity/cutoff-propagation/` with
`OMP_NUM_THREADS=1`. Outputs are in `logs/`.

- `python3 bb.py nondeg1 u fix 1e-2,1e-5,1e-8` (and `mono`, and `- off`): the
  review's instance; 1 node, 0 relaxations, 3–7 rounds with propagation; 13–57
  nodes without.
- `python3 sweep.py 8 > logs/sweep.jsonl`: 246 runs (1D and 2D instances,
  modes `off`, `fix`, `3`, `10`).
- `python3 sweep3.py 6 > logs/sweep3.jsonl`: 28 runs (`iso3`, `line3`).
- `python3 sweep_nd2.py > logs/sweep_nd2.jsonl`: 12 runs (`nd2`).
- `python3 tables.py > logs/tables.md`: Table 7.1.
- `python3 check_formula.py > logs/check_formula.log`: Theorem 3.1 (450
  instances). It was run twice: first with the rejected full-range formula,
  which failed on 9 of 18 nonempty fixed points (output overwritten), then
  with the endpoint formula, which the log records.
- `python3 check_loss.py > logs/check_loss.log`: propagation bounds on cubes
  (Section 4).
- `python3 check_constants.py > logs/check_constants.log`: Example 5.3 and the
  thin-strip test.
- `python3 rounds.py > logs/rounds.log`: root round counts for
  `eps = 10^-2..10^-8` (Propositions 3.9 and 3.10, Heuristic 3.8a). Extended
  in the recheck revision with `x^2 - 2x + 1 + (x-1)^4`, `rot1`/`st` and
  `line3`/`st`. The first counts were computed with an inline command.
- Revision (Section 11): `python3 check_revision.py > logs/check_revision.log`
  (the endpoint example and restart; 98 merged-phase frame pieces and 360
  children with inherited bounds, 0 violations; `h_{1/2}` on `s < 0`;
  two-sided localization, 125 removals, worst ratio 0.37; part (E), added for
  the recheck: cutoffs moving up and down, 263 frame pieces, 0 uncertified
  with the chain-minimum cutoff and 60 with the phase-only minimum). Also
  `python3 check_loss.py > logs/check_loss.log` re-run with the added point
  `(1, 0)` of `linediag` (cube loss `8.01 r`). Regression after extending
  `fbbt.hc4`: `bb.py nondeg1 mono fix 1e-5` (1 node, 6 rounds) and
  `bb.py linediag exp fix 1e-3` (1325 nodes, 3185 rounds), both unchanged.
- `instances.check_reps` and `instances.min_hessian_eig` for every instance:
  representations agree with `f` to `6e-14`; each `alpha` is at least half
  the most negative Hessian eigenvalue found on a grid.

These checks test the statements they cite. They are floating-point
illustrations and certify nothing; each theorem rests on its written proof. No
project-wide checks were run, CI was not inspected, and nothing was committed.

## 11. Revision after review

### 11.1 First review

The [independent review](../../reviews/cutoff-review.md) (code and logs in
[`reviews/cutoff/`](../../reviews/cutoff/)) found no counterexample to any
numbered result. It reproduced 55 cells of Table 7.1 with independent code and
confirmed Theorem 3.1 on 200 instances with non-monotone unary nodes. Each
correction below was re-derived before it was made.

1. **Round-count criterion (Summary, Section 3.3, Conjecture 3.11, Section
   7.2).** The summary said that an interior nondegenerate minimizer needs
   `Theta(eps^(-1/2))` rounds in the computed examples. That is false:
   `t^2 - 2t^4` in monomial form has an interior minimizer and needs 4–7
   rounds. Proposition 3.9 is now stated for HC4. The replacement criterion
   of this revision ("every term strictly monotone at the minimizer") was
   itself contradicted by the recheck. It was replaced by Heuristic 3.8a;
   see Section 11.2, item 1.
2. **Lemma 2.1(b), proof.** "Consecutive runs compose to one run" is false,
   because a restart from `Z0(B_i)` can enlarge lifted intervals
   ([`check_revision.log`](logs/check_revision.log), part (A): a square node
   in `[0.0033, 1]` at the end of a run, `[0, 1]` after the restart). New
   Lemma 1.2(d), `Z ⊆ Z0(Π_x Z)` for hull-consistent `Z`, proved by induction
   in topological order. Lemma 1.1(b) now keeps any hull-consistent box
   contained in the start box. `D` survives every restart and every start
   from inherited parent bounds. (This revision used the smallest cutoff of
   the phase and a nonincreasing incumbent; Section 11.2, item 3, removes the
   assumption.) Check:
   98 frame pieces of phases with restarts and 360 children started from
   inherited bounds, 0 violations (part (B)). The review's own test found 0
   violations in 57 pieces.
3. **HC4 partial steps (after Lemma 1.1).** Lemma 1.1(c) and Proposition
   1.4(b) were proved for exact revises only. Added: forward and backward
   steps are run steps; they are monotone and continuous from above; a box
   fixed by both steps of `E_k` is fixed by `rho_{E_k}`. So fair HC4 converges
   to `Z*`.
4. **`linediag` at `(1, 0)` (Section 4).** It is not locally one-sided:
   `D_i = 0` but `L = 8`, and the cube loss is `8.01 r` (`check_loss.log`,
   point added).
5. **Scope of (FS1) (Section 4).** The shared-base representations `s`,
   `st`, `u` and `centered` are not in (FS1). New Remark 4.1a extends Lemma
   4.1 to bases that are single-use expressions, with proof. Nothing
   downstream depended on the old sentence.
6. **Smaller corrections.**
   - `h_c` on `(-inf, 0)`: the only increasing term is `(c-2)s^2`, with
     `e` = right endpoint. Checked: `pi_D = min h` on three intervals (part
     (C)).
   - Theorem 3.8 is stated for idealized propagation, with the stopping-rule
     condition, and the prior "exact bound, no cluster" principle is credited.
   - Theorem 5.2 bounds `|P|`, and bounds nodes only when phases and
     reduction rounds per node are bounded.
   - The `kappa^(-1/2)` remark needs `eps << kappa rho0^2` (about
     `8e-4 kappa`), since `rho0 <~ 1/36`.
   - Section 6 table: "2 fewer" is now "2 more", and upper rates for
     propagation runs are marked as observed.
   - Section 7.2: "4–30 %" is now "4–39 %" (`iso2` at `10^-1`: 31 to 19).
     `line3` with `R = 10` is called undecided.
   - Also: `nondeg1s` one-sidedness is now justified (Example 3.7(b)).
     Corollary 3.5 needs the remaining coordinate to be one-sided. The
     exclusion of lifted-space OBBT and branching on auxiliaries is stated
     (Section 2, Section 7.4, open problem 8). Proposition 2.3 is stated for
     factorable `f`. Measurability is noted in Theorem 2.2. The SCIP settings
     `nocutoffprop` and `noweakdual` are distinguished.
   - The review's endpoint example `-3x^2 + 2x^2 + 2x^2` was added after
     Remark 3.2 and re-run (part (A): `pi_D = -1, -0.01, -0.03`).
7. **Novelty (Section 8).** Added:
   - Benhamou et al. (1999), who call the characterization of HC4revise's
     output open;
   - Araya et al.'s `x^2 - 3x + y` example (checked locally, p.3), with its
     explanation by Theorem 3.1;
   - Schichl–Markót–Neumaier's unproved order-1 claim, which the note refines
     and, for one-sided representations, contradicts;
   - Wechsung et al. (2014, p.8, checked locally) and Kannan–Barton for the
     principle behind Theorem 3.8;
   - Neumaier's `min x − x` example (p.29, checked locally).

   Section 8 now separates what is known from what is claimed as new.
8. **Review observation, now proved.** Proposition 5.1a: if
   `D_i - |d_i f| >= D0'`, every removal confines the whole box to width
   below `8(m+eps)/D0'` in every coordinate. The proof uses one-sided
   segment witnesses. Check: 125 removals, worst ratio 0.37 (part (D)).

Checks re-run for this revision: `check_revision.py` (new) and
`check_loss.py`, plus the two `bb.py` regressions listed in Section 10. The
sweeps were not re-run: no statement they test changed, and `fbbt.hc4` gives
identical results after the extension (regression above). No project-wide
checks were run, CI was not inspected, and nothing was committed.

### 11.2 Recheck

A [fresh recheck](../../reviews/cutoff-recheck.md) of the Section 11.1
revisions (code in [`reviews/cutoff-recheck/`](../../reviews/cutoff-recheck/),
written from scratch) found no numbered result false. It confirmed:
- Lemma 1.2(d) and the new proof of Lemma 2.1(b), under the two assumptions
  below;
- the HC4 paragraph;
- Remark 4.1a and Proposition 5.1a;
- Proposition 3.9.

Changes, each re-derived:

1. **Round-count criterion.** The restated criterion ("every term strictly
   monotone at the minimizer") is false. `rot_kappa`/`st` and `line3`/`st`
   have a term `t^2` that is stationary at the minimizer, yet need 55, 588,
   5920 and 59234 rounds (Table 7.1). `x^2 - 2x + 1 + (x-1)^4` needs exactly
   the rounds of the plain quadratic. Both are re-run in
   [`rounds.py`](rounds.py). The statement is now Heuristic 3.8a, a per-base
   heuristic that fits all examples: slow when some base has cancelling
   nonzero term derivatives at the minimizer. It is labelled as not proved.
   Updated: the Summary, Section 3.3 (with the evidence), Proposition 3.9's
   title, the remark after Proposition 3.10, Sections 7.2 and 9, and the
   status table. Conjecture 3.11's hypothesis is now per base, so that it
   covers its cited examples, Example 3.7(d) and `line3`.
2. **Gap A: constraint propagation inside runs.** The model's "(and possibly
   propagation of the constraints)" was not covered by the proof. The recheck
   gave a counterexample (`-3x^2 + 2x^2 + 2x^2` on `[-1, 1]` with
   `x >= 0.5`). The parenthetical is removed. Constraint propagation is
   allowed as separate (R-inf) rounds on x-boxes, and joint propagation is
   listed as excluded, with the counterexample (Section 2). Section 5 has
   `F = X0`, so nothing downstream changes.
3. **Gap B: incumbents.** The proof of Lemma 2.1(b) assumed a nonincreasing
   incumbent, while Theorem 5.2 allows any incumbents. The proof now uses the
   smallest cutoff along the chain of inherited lifted boxes, with an explicit
   induction (*) over runs, and needs no assumption. It covers every start
   box: `Z0` of the current x-box intersected with any final lifted boxes of
   earlier runs at the node or its ancestors. Check
   ([`check_revision.log`](logs/check_revision.log), part (E)): with cutoffs
   moving up and down and inherited starts, 263 frame pieces, 0 uncertified
   with the chain minimum, 60 uncertified with the phase-only minimum
   (control). The recheck found 0 failures with the chain minimum as well.
4. **Lemma 1.2(d):** now requires constant nodes to have their values, which
   holds for every hull-consistent box inside some `Z0(C)`.
5. **Remark 4.1a:** replaced by its general form, with proof. Any DAG below a
   flat root sum works, with `Phi_full` from exact term ranges; single use
   matters only in Corollary 4.2.
6. **Proposition 5.1a:** the note now says that its own check did not verify
   `m + eps < theta'`. It cites the recheck's verified test and the recheck's
   observation that the constant is within a factor 2 of sharp.

Checks re-run for the recheck: `python3 rounds.py > logs/rounds.log`
(extended) and `python3 check_revision.py > logs/check_revision.log` (part
(E) added; parts (A)–(D) unchanged). No project-wide checks were run, CI was
not inspected, and nothing was committed.
