# Closing audit A: final-round changes in three bb-complexity notes

Date: 2026-09-29. Auditor: fresh, independent; had not seen these notes before,
did not write them, and did not edit them. Scope: only the final-round changes
listed in the task:

1. [`cutoff-propagation.md`](../bb-complexity/cutoff-propagation/cutoff-propagation.md),
   Section 11.2;
2. [`separable-omega.md`](../bb-complexity/branching-competitiveness/separable-omega.md),
   Section 10 (Theorems C, C', Proposition 6.2 and the tie-free variant);
3. [`robust-branching.md`](../bb-complexity/robust-branching-points/robust-branching.md),
   Section 11 (Theorem A(ii), the midpoint fallback, Proposition D(i)).

Every proof step in scope was re-derived by hand. The claims were then tested
with new scripts in [`closing-audit-a/`](closing-audit-a/). The scripts import
no author or reviewer code. The authors' scripts were read only to learn the
conventions: instance boxes, the HC4 round order, and `|c| = 1`. All
computations use exact rationals (`fractions`).

## Verdict

| Item | Verdict | Main point |
|---|---|---|
| 1. Cutoff propagation, Section 11.2 | **correct** | The chain-minimum proof of Lemma 2.1(b) is complete. It assumes nothing about the incumbent and covers every start box. Lemma 1.2(d), Remark 4.1a (general DAGs), the heuristic label on 3.8a and the exclusion of joint constraint propagation are all correct. Only optional wording remains |
| 2. Separable omega, Section 10 | **correct with fixes** (minor, textual) | Theorem C holds for every `n >= 2` exactly on (6.1). `c = 1/(5n)` works. Theorem C' holds in the node-local I1 model. `G(2..5) = 3, 5, 9, 15` reproduced, and `G(6) = 25` is new. Proposition 6.2 and the tie-free variant hold. Fixes: a wrong cross-reference to `G(n)`, one imprecise counting sentence in step 5, and an explicit node-locality caveat |
| 3. Robust branching, Section 11 | **correct with fixes** (one statement-level) | The 1D bounds of Theorem A(ii) hold, both at the alternating points and on the runs-of-length-at-most-2 family. **The sharper McCormick bound `K'` holds only at the two alternating points.** At run-length-2 points it fails, for example `T = 1 < 3 = 2K' + 1`. There the correct bound is `T >= 2K' - 1`. The midpoint fallback (`S = ceil(log2(theta/d0)) + 1`, never traps for `theta <= 1/3`, sharp at 1/3) and Proposition D(i) (`S = J + 1` exactly) are correct |

No numbered result in scope is false. Item 3 needs one restriction of scope
in the statement of Theorem A(ii). Everything else is wording.

---

## 1. `cutoff-propagation.md`, Section 11.2

### 1.1 Lemma 2.1(b): the chain-minimum proof

I re-derived each step.

- **The chain is well founded.** A phase `Psi` "enters" `Phi` only through a
  final lifted box of one of its runs. Such a run ends before the run of
  `Phi` that uses it. `Psi` is therefore either an earlier phase at the same
  node or a phase at an ancestor, and the recursive definition terminates.
- **Monotonicity along the chain.** `c(Phi) <= c(Psi)` holds by definition.
  `B(Phi) ⊆ B(Psi)` holds because node boxes only shrink:
  - through phases, R-rel and R-inf rounds at a node;
  - through splits from a parent to a child.
- **The induction (\*).** `D = Z*(B0, c(Phi))` is hull-consistent for every
  cutoff `>= c(Phi)`, since only the root constraint depends on `c`. So by
  Lemma 1.1(b) it suffices that `D` lies in every start box. A start box is
  the intersection of `Z0(B_i)` with final boxes of earlier runs.
  - `D ⊆ Z0(B0)` by definition.
  - At a later run of `Phi`, the current x-box `B_i` is the projection of a
    final box that contains `D` (by (\*)). Hence `Π_x D ⊆ B_i`, and
    Lemma 1.2(d) gives `D ⊆ Z0(Π_x D) ⊆ Z0(B_i)`.
  - A final box of an earlier run of `Phi` contains `D` by (\*).
  - A final box of a run of an entering phase `Psi` contains
    `Z*(B(Psi), c(Psi))`, which contains `Z*(B(Phi), c(Psi))` by Lemma 1.2(a).
    That in turn contains `Z*(B(Phi), c(Phi))` by Lemma 1.2(b).
- **Consequences.**
  - A piece `S ⊆ B0` has `Z*(S, c) ⊆ D`, so `Π_x Z*(S, c) ⊆ B_f`.
  - `pi_D(S, y) > c` for `y ∈ S \ B_f`. Otherwise Lemma 1.2(b) would put `y`
    in `Π_x Z*(S, c)`.
  - `c >= f* - eps` because every incumbent is at least `f*`. No
    monotonicity of the incumbent is used.
  - An emptying phase has `D = ∅`.

The proof is complete, and it covers exactly the start boxes that the model
allows.

**Test** (`cutoff_audit.py E` and `E2`; logs `cutoff_audit_E.log` and
`cutoff_audit_E2.log`).
- **Setup.**
  - 400 random 2D DAGs per run. The node types are `lin`, `abs`, `sqr` and
    constants, with shared subexpressions.
  - Branch-and-bound trees reach depth 4. Each node has 1–2 phases, with
    random box shrinking between phases. Each phase has 1–3 runs.
  - Schedules are either full HC4 rounds or random sequences of single
    forward, backward and cutoff steps.
  - Cutoffs follow a random walk up and down.
  - Each start box is `Z0(x-box)` intersected with a random subset of the
    final lifted boxes of earlier runs at the node and its ancestors.
- **Exactness.** Every step rounds its new bounds outward to `2^-40` and
  then intersects. It is therefore a run step in the note's sense
  (`rho_E(Z) ⊆ rho(Z) ⊆ Z`), so every long-HC4 result is an outer
  approximation of `Z*`. A certificate from this test is therefore rigorous.
- **Two cutoff bands.** Run E uses cutoffs in `[fmin - 0.1 span,
  fmin + 0.4 span]` of the grid range of `f`. Run E2 uses
  `[fmin + 0.2 span, fmin + 0.7 span]`, so its cutoffs lie well above `f*`.

**Results.** "Violation" means the fixed-point box `Z*` was not inside `B_f`
(beyond a tolerance of `1e-6`) after HC4 had converged. "Inconclusive" means
HC4 had not converged.

| Test | E (chain min) | E (phase-only control) | E2 (chain min) | E2 (phase-only control) |
|---|---|---|---|---|
| Frame pieces and emptying phases: `Pi_x Z*(S, c) ⊆ B_f`, or `Z*(B0, c) = ∅` | 3,851 + 1,313: **0 violations** (5,153 empty `Z*`, 11 nonempty and inside) | 1,853 violations, 3 inconclusive | 5,855 + 956: **0 violations** (6,803 empty, 8 nonempty and inside) | 2,840 violations, 1 inconclusive |
| Direct test of the core claim: `Pi_x D ⊆ B_f`, `D = Z*(B0, c)`, over non-emptying phases | 5,646 phases, 5,199 nonempty `D`: **0 outside** | 1,532 outside | 13,887 phases, 13,658 nonempty `D`: **0 outside** | 2,604 outside |

The largest excess accepted within tolerance was `9e-13`, which is rounding
level. Most frame pieces have an empty `Z*`. That is expected: pieces are
regions that propagation removed. The direct test on `D` has 18,857
nonempty cases, so the chain-minimum claim is not verified only through
emptiness. The control fails often, which shows that the test can detect a
wrong cutoff. It also confirms the note's statement that the first
revision's phase-only minimum is not enough when incumbents move up and
down.

### 1.2 Lemma 1.2(d) with constant nodes

The proof is correct. With constants fixed at their values, the base of the
topological induction holds. For an operation node, hull consistency gives
`W_k ⊆ hull(image of E_k over Z_children) ⊆ op_k(Z_children)`. That set is
contained in the forward interval over `Z0(Π_x Z)`: it equals it for `+`,
unary functions and products of distinct children, and it is smaller for
`w*w` written as a product.

The constant-node caveat is also correct. For `w = x + k` with the constant
`k = 0` widened to `[0,1]` and `x = [0,0]`, the box with `w = [0,1]` is fixed
by both HC4 steps but is not in `Z0([0,0])` (checked in `cutoff_audit.py W`).

In the exact PL test below, 1,200 witness boxes and 909 exactly converged HC4
limits all satisfy `Z ⊆ Z0(Π_x Z)`.

### 1.3 Remark 4.1a (general form)

The proof is correct.
- Every non-root node gets the exact range of its expression over `U'`.
- For any elementary constraint below the root, a value of any of its
  intervals is attained at some `x ∈ U'`. The point `x` then gives a
  solution of the constraint inside the box.
- The root constraint involves only the root and the distinct coordinates
  `p_j`, so the argument of Theorem 3.1(b) applies unchanged.

"Distinct" is what makes the `p_j` independent coordinates of the root
constraint. The remark correctly states that single use is needed only for
`F_lo` in Corollary 4.2.

**Test** (`cutoff_audit.py W`). 300 random 1D piecewise-linear DAGs (`lin`,
`abs`, constants; 297 with a shared operation node) and 1,200 random boxes
`U' ⊆ C`. Exact ranges were computed from exact breakpoints.
- The witness box is fixed by every exact forward and backward step and by
  the cutoff: 1,200/1,200.
- It lies in `Z0(C)`: 1,200/1,200.
- HC4 from `Z0(C)` at `c = Phi_full(U')` keeps all of `U'`: 1,200/1,200.

### 1.4 Heuristic 3.8a

The heuristic is correctly labelled "not proved" everywhere it appears:
- the Summary;
- the status table ("heuristic; fits all computed examples, not proved");
- the Section 3.3 title;
- Conjecture 3.11 ("the slow case of Heuristic 3.8a");
- Section 7.2 (observed);
- Section 9, item 5 ("a proof or refutation").

No remaining text uses the retracted criterion ("every term strictly monotone
at the minimizer") as a result.

**Independent check** (`cutoff_audit.py R`, grid `2^-70`). HC4 root rounds on
`[1/5, 11/5]` for `s^2 - 2s + 1` are 30, 98, 313, 992 and 3140 for
`eps = 1e-2..1e-6`. For `x^2 - 2x + 1 + r^4`, `r = x - 1`, the counts are
identical. Both agree exactly with `logs/rounds.log`.

**Optional.** The parenthetical in 3.8a ("the box is not emptied at all once
it is wider than `O(eps)`") is a proved consequence of Lemma 4.4 and
Remark 4.1a. Citing them would separate it from the heuristic part.

### 1.5 Exclusion of joint constraint propagation

The exclusion and its counterexample are correct.

For `f = -3x^2 + 2x^2 + 2x^2` on `[-1, 1]` with `x >= 1/2` and
`c = 1/4 - 10^-3`:
- HC4 on the constrained box `[1/2, 1]` empties it (23 rounds).
  Theorem 3.1(b) predicts this: `Phi([s, t]) = s^2 >= 1/4` for
  `1/2 <= s <= t`.
- The box with `x = [-1, 1]`, `u1 = [1, 1]`, `u2 = u3 = [0, 1]` and root
  `[-3, -1]` is hull-consistent at `c = -1`. So `pi_D([-1,1], y) <= -1` for
  every `y`.
- HC4 at `c = -1.001` empties `[-1, 1]`. So `pi_D([-1,1], y) = -1`, and (Π)
  fails at every feasible point, as the note says.

Separate R-inf rounds followed by a phase on `[1/2, 1]` are certified by
Lemma 2.1, which is why the model allows them.

### 1.6 Corrections for item 1

None required. Optional:
- Lemma 2.1(b), first bullet: "the current x-box `B_i`, the projection of the
  previous run's final lifted box". The model says this, but repeating it
  makes the step `Π_x D ⊆ B_i` self-contained.
- Heuristic 3.8a: cite Lemma 4.4 and Remark 4.1a for the parenthetical.

---

## 2. `separable-omega.md`, Section 10

### 2.1 Theorem C for every `n >= 2`

I re-derived Lemma 6.1 (a)–(e) and steps 1–6 of Theorem C by hand.
- The left end of (6.1) is `nc > eps + eps/(2(n-1))`. This is exactly what
  steps 2 and 4 need, and it also gives the margin in (b) at 0 and 1.
- The right end of (6.1) is `nc < 1/4 + eps/2`. This keeps the floor lines
  below `1/2 - c` at `1/2`, as (a) needs.
- The existence condition `eps < (n-1)/(2n)` is correct.
- `c = 1/(5n)` with `eps = 1/100` satisfies (6.1) iff `190n > 195`, so for
  every `n >= 2`.
- The rigid function `R` is defined and convex without further conditions.

**Tests** (`sep_audit.py C`; log `sep_audit_C.log`). Node data are computed
exactly: `phi_J = H - (l+u)t + lu` is piecewise linear and convex.
- **`c = 1/(5n)`, `n = 2..40`.** Every item passes:
  - Lemma 6.1 (a)–(e);
  - root invalid;
  - both right-cut children have margin exactly `eps/2`;
  - every wrong cut at 101 points leaves both children invalid.
- **Agreement intervals.** The worst wrong-cut child value equals the
  analytic bound `-nc + eps + eps/(2(n-1))`, so the bound is attained. The
  agreement intervals match the note: `R = N` on
  `[0.3894.., 0.6105..]`, and `R - N` is constant on `[0, a_n]` with
  `a_2 = 3/398` and `a_40 = 3/15598`.
- **300 random admissible `(eps, c)`** with `n = 2..12`, including `c`
  within `1e-6` of either end of (6.1): all items pass.
- **(6.1) is sharp.**
  - At `c` equal to the left end, a wrong cut at `1/2` leaves valid children,
    so step 4 fails.
  - At `c` equal to the right end, `R = N` fails near `1/2`: the floor line
    touches, so (b) fails.

### 2.2 Theorem C' (iterated lower bound)

**The information model.** At a corner node `v` with `i` and `i'` both free,
the rule's data agree in `A_i` and `A_{i'}`.
- **Box, value and minimizer.** Every cut coordinate carries `N` on the
  same interval in both instances, and the selection is coordinate-wise.
  Every free coordinate is `[0,1]`, with unique minimizer `1/2` and value
  `-c`.
- **Incumbent.** It is fixed at `f*` (main note, Section 1.2).
- **`f` near `y_B` and near the corners.** `f_{A_i} - f_{A_{i'}}` involves
  only the two free coordinates, and those sit near `1/2` or near `{0, 1}`.
  There `R - N` is `0` or `phi + phi'`, respectively.
- **Ancestors.** Every ancestor of `v` is a corner node with `S` a subset of
  `S(v)`. So even data inherited along the path would agree.

**The proof.**
- Step 2's bound `-nc + eps(1 + |S|/(2(n-1))) <= -nc + 3eps/2` uses
  `|S| <= n - 1`. This holds because `i` is free.
- Steps 3–4 are correct. Every RT node with `i` free has all its ancestors
  with `i` free, and all of them are invalid in `A_i`. So they are reached
  by the common decisions and are internal. That gives `T(A_i) >= 2N_i + 1`.
- Step 6 is correct: `max >= average`, and Yao's principle with the uniform
  prior on `A_1..A_n`.
- Step 7's reduction to trees that cut only free coordinates is correct.
  Contracting re-cut chains gives a tree that is realizable by a rule and
  has pointwise smaller `N_i`. Different nodes with the same `S` have
  different boxes, so their choices are independent.
- The numbers are correct:
  - `sum_{d<n} 2^d (n-d) = 2^(n+1) - n - 2`;
  - deterministic ratios 7/3, 11/3, 19/3, 31/3;
  - randomized ratios 5/3, 25/9, 14/3, 119/15.

**Fixes (minor).**
1. **Cross-reference.** The statement says "`G(n)` ... the minimax problem
   in step 5". It is defined in step 7 ("`G(n)` is the minimum over trees
   `RT` of `max_i N_i`"). Change "step 5" to "step 7", or move the
   definition up.
2. **Step 5 wording.** "Each node of `RT` with `|S| = d < n` leads to a
   distinct node that cuts a free coordinate" is not injective. Two RT nodes
   on the same re-cut chain, for example `v` and its re-cut corner child,
   have the same `S` and lead to the same node. The conclusion is right if
   the count is over **branching nodes** (nodes that cut a free
   coordinate). Suggested text:
   > Let `b_d` be the number of RT nodes with `|S| = d` that cut a free
   > coordinate. Each has two children with `|S| = d + 1`. Their re-cut
   > chains lie in disjoint subtrees, so they end at distinct such nodes.
   > Hence `b_{d+1} >= 2 b_d`, `b_0 = 1`, and `RT` has at least `2^d` nodes
   > with `|S| = d`.
3. **Scope caveat (recommended).** Step 3 needs the rule to be node-local.
   The main note's I1 model includes this ("Nothing from other nodes is
   used"), but it deserves a sentence in Theorem C'.
   - A rule with memory across nodes breaks the bound. Such a rule can learn
     `i` the first time a cut produces valid children, then cut `i`
     everywhere else. That needs `O(n)` nodes on `A_i`.
   - Pseudocost-type rules are therefore not covered by the exponential
     lower bound.
   - Also add "incumbent `f* = 0`" to step 1 of Theorem C', as in Theorem C.

**Tests** (`sep_audit.py corner G` and an attainment run; logs
`sep_audit_omega.log`, `sep_audit_G.log` and `sep_audit_attain.log`).
- **Corner nodes.** 400 random corner nodes for each `n = 2..7`, with random
  rational cut intervals containing 0 or 1. Every free `A_i` gives identical
  value and minimizer, under both selections `knot` and `proj`, and every
  one is invalid.
- **Independent Pareto DP.** `G(2..5) = 3, 5, 9, 15`, with optimal vectors
  `(1,3)`, `(1,5,5)`, `(1,7,9,9)` and `(1,11,15,15,15)`. New: `G(6) = 25`,
  vector `(1,19,25,25,25,25)`, which gives a deterministic ratio of at least
  17. This value was computed with the pruning cap 26; it is exact because
  the optimum found is below the cap.
- **Attainment.** A rule that follows the DP's optimal tree, cutting at
  `1/2` and simulated exactly, gives `T(A_i) = [3, 7]`, `[3, 11, 11]`,
  `[3, 15, 19, 19]` and `[3, 23, 31, 31, 31]` for `n = 2..5`. The maximum is
  `2G + 1` in each case, so the exact-ratio claim extends to `n = 5`.
- **`G(7)`.** The DP for `n = 7` was stopped after about 40 minutes. No
  claim depends on it.

**Optional sharpening.** The coordinate cut at the root is free only at the
root, so `N_j = 1` for that coordinate. Hence
`max_i N_i >= (2^(n+1) - n - 3)/(n - 1)`. This gives 3, 5, 9, 14 and 24 for
`n = 2..6`, which is exact for `n <= 4`, against 2, 4, 7, 12 and 20 from the
plain average. The randomized bound is unchanged. The asymptotic
`2^(n+2)/(3n)` claim is about the lower bounds and is correct as stated.

### 2.3 Proposition 6.2 and the tie-free variant

The proof is correct.
- At a corner node every free coordinate has `w = 1/4`, and every cut `N`
  coordinate has `w < 1/4`. Before `i` is cut the node is invalid (step 2).
  After `i` is cut at `1/2`, the margin is `eps/2 + |S'| eps/(2(n-1)) >= 0`.
  This uses only `F_N(J) >= -phi'`, which holds because
  `H_N >= t/2 - phi'` and `H_N >= 3t/2 - 1/2 - phi'`.
- Counting `i` levels of a full binary tree gives `2^(i+1) - 1` nodes.

**Tie-free variant.** Also correct.
- The quadratic identities for `a_{[0,p]}` and `a_{[p,1]}` hold. The
  condition `nc < p(1-p) + eps/2` holds for `c = 1/(5n)`.
- The floor lines of `R'` are active near 0 and 1, with large margins.
- `w_{R'} = 156/625 < 1/4`, so `omega` cuts `R'` last on every labelling.

**Simplification (optional).** The knot-distance argument (`t_N`) is not
needed. A cut coordinate at a corner node has an interval of length
`ℓ < 1`, so `w <= ℓ^2/4 < 1/4`, for any selection rule.

**Tests** (`sep_audit.py omega`; log `sep_audit_omega.log`). Exact
simulation of `omega` and `deficit` on `A_1..A_n`, `n = 2..6`, under both
selections: `3, 7, ..., 2^(n+1) - 1` in every case. Tie-free variant for
`n = 2..6`, every labelling and both selections: `2^(n+1) - 1`, with root
`F_{R'} = -c`, unique minimizer `13/25`, and value `phi` on both halves.

---

## 3. `robust-branching.md`, Section 11

### 3.1 Theorem A(ii)

**Proof step 4 (general bound).** Correct. Suppose steps `k, ..., k+r-1` lie
on the same side (L) and step `k+r` switches.
- The switch gives
  `rho_k / (theta_k ... theta_{k+r-1}) > 1 - theta_{k+r} > 1/2`, so
  `rho_k > theta0^r/2`.
- Since `rho_k < theta_k < 1/2`, it follows that
  `rho_k (1 - rho_k) >= rho_k/2 > theta0^r/4`.
- Alternating itineraries give `theta0/4`. Itineraries with runs of length
  at most 2 give `theta0^2/4`.

**Step 5 (1D).** Correct. The chain node `I_k` is open iff
`alpha rho_k (1 - rho_k) w_k^2 > eps`, and `w_k >= theta0^k`, so nodes
`0..K-1` are open.

**Step 5 (McCormick x-only).** The bound `|c| rho_k (1 - rho_k) w_k` is
correct. It gives `K'` **only where `rho_k (1 - rho_k) >= theta0/4`**, that
is, at the two alternating points.

**Fix (statement-level).** In the statement, the McCormick sub-bullet ("the
same holds with `alpha` replaced by `|c|`, and in fact with the larger
`K'`") follows the runs-of-length-at-most-2 sub-bullet. A reader can
therefore take it to cover those points, where it is false.
- **Counterexample.** Fixed clamp `1/5`, itinerary `L, L, R, L, R, ...`, so
  `a = 1/30`. Take `|c| = 1` and `eps = 1/25 < theta0/4`. The root bound is
  `(1/30)(29/30) = 29/900 < 1/25`, so the root is closed and `T = 1`. But
  `K' = ceil(log(5/4)/log 5) = 1` gives `2K' + 1 = 3`.
- **Frequency.** Over 6 schedules and 72 random runs-≤2 itineraries,
  `T >= 2K' + 1` fails in 48 of 720 cases.
- **Correct bound.** Replacing `theta0/4` by `theta0^2/4` gives
  `K'_2 = ceil(log(|c| theta0^2/(4 eps))/log(1/theta0)) = K' - 1` for
  `K' >= 1`. So `T >= 2K' - 1` at those points, with 0 violations in the
  same 720 cases.
- **Suggested wording.** "On the McCormick family with x-only selection:
  at the two alternating points `T >= 2K' + 1`, with
  `K' = ceil(log(|c| theta0/(4 eps))/log(1/theta0))`. At points whose runs
  have length at most 2, `T >= 2K' - 1`. Both hold for
  `eps < |c| theta0/4`." The same qualifier belongs in proof step 5 ("This
  is at least `|c| (theta0/4) theta0^k` at the alternating points") and in
  Section 11, item 2.

**Tests** (`robust_audit.py`, part A; log `robust_audit.log`).
- **Schedules.** Six clip schedules: fixed 1/5, 2/5 and 1/10; depth
  alternating 1/5, 1/4; width `1/10 + w/5`; position `1/8 + l/4`. The last
  two are evaluated on the box rounded to `2^-30`, which is still a
  deterministic schedule.
- **Points.** Exact nested zones to depth 200.
- **Alternating points.** 1D, `T >= 2K + 1`: 0 violations in 120 cases.
  McCormick, `T >= 2K' + 1`: 0 violations in 120 cases.
- **Runs-≤2 points.** 1D, `T >= 2K_2 + 1`: 0 violations in 720 cases.
  McCormick with `K'`: 48 violations in 720 cases. McCormick with `K'_2`:
  0 violations in 720 cases.
- **Step-4 inequality.** Checked on 4,800 steps of itineraries with runs of
  length at most 3: 0 violations.
- **The note's numbers are reproduced.** At `a = 1/6` with fixed clamp 1/5,
  the McCormick x-only counts are `T = 11, 45, 137` at
  `eps = 1e-4, 1e-16, 1e-48`, against `2K' + 1 = 9, 45, 135`. The 1D count
  at `1e-16` is `T = 23 = 2K + 1`.

### 3.2 Midpoint fallback

The proof is correct. Measure the kink's position `rho` from the near end.
- While `rho < theta`, the midpoint split doubles it: `rho -> 2 rho`.
- At the first `k` with `2^k d0 >= theta`, the position satisfies
  `theta <= 2^k d0 < 2 theta <= 1 - theta`, so the next split is at the
  kink.
- Hence `S = ceil(log2(theta/d0)) + 1` for `d0 < theta`.

**Wording nit.** "Moves to `2d`, on the same side" is loose when
`d ∈ (1/4, theta)`: then `2d > 1/2`, and the kink's nearer end changes. The
conclusion is unaffected, because `2d ∈ [theta, 1 - theta]`.

**Sharpness (optional).** The bound `theta <= 1/3` is sharp. For
`theta > 1/3` the point `a = 1/3` traps: the midpoint map is the doubling
map, whose orbit `1/3, 2/3, 1/3, ...` stays in the clamp zones.

**Tests** (`robust_audit.py`, part B). About 4,000 exact kinks per `theta`
in `{1/10, 1/5, 1/4, 3/10, 1/3}`, on both sides: log-uniform distances down
to about `1e-12`, plus `theta^j`, `theta^j/2`, `2^-j` and `theta/2^j` with
perturbations `0`, `±1e-6` and `±1e-2`. Result: 0 mismatches. At
`theta = 2/5`, `a = 1/3` makes no landing in 2,000 splits.

### 3.3 Proposition D(i): `S = J + 1` exactly

The proof is correct. I checked `m <= J`, the two cases, the orbit
(`d < theta/2`: clip, same side; `theta/2 <= d < theta`: recentre, then hit),
and `d_m ∈ [theta/2, 1/2)`.

**Simplification (optional).** In the second case, `d_m >= theta/2` gives
`d0 >= theta^(m+1)/2 >= theta^(m+2)` because `theta <= 1/2`. So `J <= m + 1`
directly, and `S = m + 2 = J + 1` without citing Proposition C. Proposition C
is still needed for the optimality claim. Its proof (the first `J` chain
nodes all have `a < theta0 u`) is also correct.

**Tests** (`robust_audit.py`, part C). About 4,130 exact kinks per `theta`
(same five values, same point families): `S_RC = J + 1` in every case. The
clip exceeds `J + 1` by up to 5, 8, 12, 11 and 20 splits on this point set.
A grid brute force of the offline optimum over safe split points, at
`theta = 1/5`, gives `J + 1` for five kinks.

---

## 4. Commands run (targeted only)

All commands were run from `research-20260928b/reviews/closing-audit-a/`
with `OMP_NUM_THREADS=1`, using at most 3 concurrent processes. They are
pure Python with `fractions`; no BLAS is used.

| Command | Log | Result |
|---|---|---|
| `python3 sep_audit.py C` | `sep_audit_C.log` | Lemma 6.1 and Theorem C: `n = 2..40` and 300 random admissible `(eps, c)` pass; both ends of (6.1) are necessary |
| `python3 sep_audit.py corner omega` | `sep_audit_omega.log` | Corner nodes pass for `n = 2..7`. Proposition 6.2 and the tie-free variant pass for `n = 2..6`, both selections |
| `python3 sep_audit.py G` (stopped during `n = 7`) | `sep_audit_G.log` | `G(2..6) = 3, 5, 9, 15, 25` |
| `python3 -c "... sep_audit.plan_rule_counts(n, 1/100, 1/(5n)) for n = 2..5"` | `sep_audit_attain.log` | `T(A_i)` equals `2 N_i + 1`, and the maximum is `2G + 1` for `n = 2..5` |
| `python3 robust_audit.py` | `robust_audit.log` | Theorem A(ii) as in Section 3.1, with the `K'` scope failure; midpoint fallback and Proposition D(i) pass |
| `python3 cutoff_audit.py J W R` | `cutoff_audit_JWR.log` | Joint-propagation counterexample, Remark 4.1a, Lemma 1.2(d) and the round counts all agree with the note |
| `python3 cutoff_audit.py E`, `python3 cutoff_audit.py E2` | `cutoff_audit_E.log`, `cutoff_audit_E2.log` | Lemma 2.1(b): 0 violations for the chain minimum (11,975 piece and emptying-phase certificates; 18,857 nonempty `D`). The phase-only control fails 1,853 + 2,840 times on pieces and 1,532 + 2,604 times in the direct `D` test |

These are this audit's own targeted checks. No project-wide checks were run,
CI was not inspected, the notes were not edited, and nothing was committed.
