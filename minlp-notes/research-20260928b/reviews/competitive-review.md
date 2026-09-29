# Adversarial review: competitive node-local branching

Date: 2026-09-29. Scope:
[`../bb-complexity/branching-competitiveness/competitive-branching.md`](../bb-complexity/branching-competitiveness/competitive-branching.md)
("the note"), with its scripts and logs. Context read: the program file, the
scout report (Theorem A and Section 3.4) and the earlier review of the scout
report. The reviewer did not write the note and did not edit it. Reviewer
scripts and logs are in [`competitive/`](competitive/). They do not import
the note's code, except for one cross-check of a single instance with the
note's simulator.

## Verdict

The main mathematics holds. Theorem 1, Lemma 2, Theorem 3, Proposition 4 (as a
statement about the family `R_{lambda,theta}`), Theorem 2, Proposition 0 and
Proposition 1 are correct. Exact searches over about 40,000 instances found no
counterexample to Theorem 1. The instance families were many local minima,
flat regions, minimizers at the box ends, exact ties with adversarial
tie-breaking, and non-convex relaxations.

The errors are in side claims, one proof, and the solver attributions:

1. **Corollary 1 (inexact minimizers): the proof is incomplete.** The second
   fact of Lemma 2 also gains a `delta`, so the `delta` terms do not cancel.
   A corrected statement with `N_opt(eps - 2 delta)` is proved below. The
   stated form was neither proved nor refuted.
2. **The "worst case found" for `R_min` is wrong.** An exact instance with
   convex `H` and unique minimizers at every node has `N_opt = 3` and `T = 11`,
   a ratio of `11/5 > 2`. The note's picture ("one wasted split per breakpoint,
   tends to 2") does not hold.
3. **New result: `R_min` uses at most 5 nodes whenever `N_opt = 2`.** So
   `R_min` is exactly `5/3`-competitive on such instances, which matches
   Theorem 3. Open question 1 ("force 7/3 with `N = 2`") has a negative
   answer.
4. **The SCIP default is misstated.** SCIP 10 does not use
   `(lambda, theta) = (1, 0.2)`. Its default moves the LP value 75% of the way
   to the midpoint, scales that pull by the local/global width ratio when the
   ratio is below 1/2, and then clamps at 0.2. This rule depends on depth and
   is not in the family of Proposition 4. Exact simulation shows the same
   `log(1/eps)` growth on the note's sharp instances, but Proposition 4's proof
   does not cover it. Couenne's default clamp is 0.05, not 0.2; this does not
   change `p̄`.
5. **Model scope of Theorem 3.** Model I1 lets the rule see `f` on a
   neighbourhood of the minimizer. For real-analytic `f`, including all
   polynomials, that determines `f`, so I1 equals I_inf and Proposition 0 gives
   ratio 1. Theorem 3 is therefore a lower bound for non-analytic classes
   (piecewise-linear or `C^inf`). This scope must be stated.
6. **Novelty is overstated relative to Hansen–Jaumard–Lu.** In 1D,
   Piyavskii's lower bound on a subinterval depends only on the two endpoint
   values. So Piyavskii is a node-local "split at the node bound's minimizer"
   rule, and `n_P <= 2 n_B + 1` is a constant-competitive result of the same
   kind as Theorem 1. The note's stated difference ("Piyavskii's lower envelope
   is global") is incorrect in 1D. Daskalakis–Diakonikolas–Yannakakis give a
   per-instance competitive analysis of the chord algorithm, including lower
   bounds for every algorithm in an oracle model. That is the closest precedent
   for Theorem 3's type of result, and the note does not cite it.

Smaller points are in the table and in Section 7.

| Claim | Verdict | Main point |
|---|---|---|
| Information models I0, I1, I_inf | correct, with a scope gap | I1 is degenerate for analytic `f` (Section 1) |
| Theorem 1 (`T <= 8 N_opt - 9`) | correct | proof checked line by line; exact searches confirm it |
| Lemma 2 | correct | the identity and the chain of three facts check out |
| Per-interval counts (3 inside, 1 in end intervals) | correct, attained | `[1, 3, 1]` on the `11/5` instance |
| "any choice of minimizer" | correct | worst case over all tie-breaks computed exactly |
| "only continuity of `f` is needed" | correct | lower semicontinuity suffices; without convexity the "relaxation" is not tractable |
| Incumbent robustness (Section 4.1) | correct | direct proof, simpler than via Corollary 1 |
| Corollary 1 (inexact minimizers) | proof incomplete | proved with `eps - 2 delta`; stated form open |
| Section 4.2 "worst case found tends to 2" | wrong | `T = 11`, `N_opt = 3` (ratio `11/5`) |
| Section 4.2 "worst ratio of `R_min` in `[5/3, 4)`" | correct, refined | now `[11/5, 4)`; exactly `5/3` when `N_opt = 2` |
| Theorem 3 (`5/3` deterministic, `4/3` randomized) | correct in its model | verified in exact arithmetic; scope caveat for analytic `f` |
| Theorem 3 smoothing remark | plausible, argued only | not computed (by the note or by the reviewer) |
| Proposition 4 (family `R_{lambda,theta}`) | correct | all table values reproduced, including irrational ones |
| Proposition 4 "contains the SCIP and Couenne defaults" | partly wrong | SCIP 10's default depends on depth; Couenne's clamp is 0.05 |
| Theorem 2 | correct | the note's check script undercounts `T` for `n >= 2` (assertions still valid) |
| Proposition 0 | correct | the standard greedy exchange argument |
| Proposition 1 | correct | |
| Section 6.3 / table row I_inf, `n` dimensions | inconsistent | by the note's own benchmark `2 N_guill - 1`, the ratio is 1 |
| Section 7.1 "without loss of generality" argument | correct only for convex `H` | the interpolant raises `H` only if `H` is convex |
| Section 8.2 "chord rule" identification | imprecise | the tangent is parallel to the chord of `alpha y^2`, not of `H` |
| Novelty claims (Section 8.3) | overstated | see Section 8 |

## 1. Information models

The note defines I0 (box and depth), I1 (box, `alpha`, `eps`, incumbent,
`LB(B)`, a solver-chosen relaxation minimizer, and `f` on a neighbourhood of
it) and I_inf (`f` on the whole node).

Whether each result respects its model:

- Theorem 1 and Corollary 1 use only the minimizer, so they are I1 rules.
  Theorem 1 holds for any choice among tied minimizers.
- Theorem 3 compares two instances whose I1 data at the root coincide. This
  was checked exactly (Section 3): the same unique minimizer `3/5`, the same
  `LB`, the same `f* = 0`, and `f` equal on `[1/60, 27/40]`, which contains
  `3/5` in its interior. The rule may also see `f` near both ends; `f` agrees
  on `[0, 30 eps/13]` and `[1 - 3 eps, 1]`.
- Proposition 4's rules use the box and the minimizer only.
- Theorem 2's adversary uses only the rule's box-and-depth decisions, so it
  handles depth-dependent rules as well.
- Proposition 0 uses I_inf.

Scope gap in I1. "`f` (hence all its derivatives) on a neighbourhood of
`y_B`" determines a real-analytic `f` everywhere. For polynomial objectives,
the usual MINLP case, a rule in I1 can therefore run Proposition 0's greedy
rule. The information-theoretic ratio is then 1, although computing it is a
global optimization problem. Restricting I1 to a finite jet at `y_B` does not
remove the problem for polynomials: a jet of order at least the degree also
determines `f`. So:

- Theorem 1 is unaffected, because `R_min` uses no extra information.
- Theorem 3 is a lower bound over non-analytic classes (piecewise linear, or
  `C^inf` after the note's mollification). The note should state the function
  class explicitly. If it wants a statement for polynomial `f`, it should
  restrict I1 to a jet of order below the degree. Theorem 3's instances do not
  cover that case, because they are not polynomials.
- A computational version of the lower bound for polynomial `f` (rules with
  bounded work per node) is a different question, and is open.

## 2. Theorem 1 and its robustness claims

### 2.1 Proof check

All steps were checked by hand:

- Lemma 1 (i)–(iv). Endpoint values of `phi_B` are `m >= eps > 0`, so every
  minimizer of an invalid node is interior. Split points are distinct.
  Hereditary validity gives (iii).
- Lemma 2. The identity
  `(t1+d)(e-t1) - (t2+d)(e-t2) = (t1-t2)(e-t1-t2-d)` is correct. Adding
  `(t2+d)(t1-t2)` gives `(t1-t2)(e-t1)`, and `0 < t1 - t2 < t1` gives
  `lambda < e`.
- The class count (`Y^L`, `Y^R`, `Y^LR`, each at most 1; end intervals at most
  1) and the total `(N-1) + 2 + 3(N-2) = 4N - 5` internal nodes are correct.

Hypotheses actually used:

- the bilinear form of the gap;
- exact minimizers;
- `m >= eps > 0`;
- existence of minimizers.

Lower semicontinuity of `f` suffices. The claim "neither convexity nor
smoothness" is true. Without convexity, however, the "relaxation" `f - alpha
q_B` is a nonconvex problem as hard as the original. That generality has no
algorithmic content, and the note could say so.

### 2.2 Exact search for counterexamples

The simulator ([`competitive/exact1d.py`](competitive/exact1d.py)) is exact.
For piecewise-linear `H = m + y^2`, every `phi_B` is linear between knots,
whether or not `H` is convex. So node values, minimizers and greedy
certificates are exact rationals. The check
([`competitive/thm1_check.py`](competitive/thm1_check.py)) does the
following:

- It computes the worst tree over all tie-breaking choices by memoized
  recursion over nodes.
- It asserts the per-interval class counts against the left-greedy and the
  right-greedy optimal certificates.
- It asserts `T <= 8N - 9` and, when `N = 2`, `T <= 5` (Section 2.3).
- It checks the incumbent remark with gaps `g = eps/3` and `9 eps/10`.

Families: random convex, random non-convex `H`, flat regions (`m = eps` on an
interval), minimizers at an endpoint, many local minima, symmetric dyadic grids
with exact ties, and rigid chord breakpoints.

Result (`thm1_check_s11.log`, `thm1_check_s12.log`): 39,831 instances with
`N >= 2`.

- All assertions passed.
- Up to 3 splits inside an interior interval and 1 inside an end interval
  were observed. Both bounds are attained.
- In 276 instances an adversarial tie-break gave a larger tree than leftmost or
  rightmost tie-breaking. All of them stayed within the bound.

### 2.3 New: `T <= 5` whenever `N_opt = 2`

**Claim.** If `N_opt = 2`, then `R_min`, with any choice of minimizers, uses
at most 5 nodes.

*Proof.* Let the certificate be `J_1 = [L, s]`, `J_2 = [s, U]`.

1. If the root splits at `s`, then `T = 3`. By symmetry, let the root split
   at `y1` in `int J_2`. Then `[y1, U]` lies in `J_2` and is valid.
2. If `B2 = [L, y1]` is valid, then `T = 3`. Otherwise `B2` splits at `y2`.
   - `y2 = s`: both children are valid and `T = 5`.
   - `y2` in `int J_2`: Lemma 2, applied to the root and `B2`, would give
     `U > U`. This case is impossible.
   - `y2` in `int J_1`: then `[L, y2]` is valid.
3. It remains to show that `B3 = [y2, y1]` is valid. Suppose not, and take `w`
   in `B3` with `m(w) < (w - y2)(y1 - w)` (units `alpha = 1`).
4. `y2` minimizes `phi_{B2}`, and `w` lies in `B2`. So
   `m(y2) <= m(w) + (y2-L)(y1-y2) - (w-L)(y1-w) < (y2-L)(w-y2)`. Validity of
   `J_1` at `y2` gives `m(y2) >= (y2-L)(s-y2)`. Hence `w > s`.
5. `y1` minimizes `phi_root`. So
   `m(y1) <= m(w) + (y1-L)(U-y1) - (w-L)(U-w) < (y1-w)((U-y1) - (y2-L))`.
   Validity of `J_2` at `y1` gives `m(y1) >= (y1-s)(U-y1) > 0`. If
   `(U-y1) - (y2-L) <= 0`, this is already a contradiction. Otherwise
   `(y1-s)(U-y1) < (y1-w)(U-y1)`, so `w < s`.
6. Steps 4 and 5 contradict each other. □

The exact searches assert this bound on every `N = 2` instance, with the
worst tie-breaking. Consequences:

- Theorem 3 shows that no I1 rule does better than `5/3` on `N_opt = 2`
  instances. So `R_min` is optimal in model I1 on these instances.
- Open question 1 asks whether an adversary can force `7/3` "with two wasted
  splits for `N = 2`". It cannot, for any rule, because `R_min` never exceeds 5
  nodes when `N_opt = 2`.
- The LP example of Section 4.2 ("a right split, then a left split") is
  consistent with this bound only because the third node `[y2, y1]` is then
  valid. So "two wasted splits" there means `T = 5`, not 7.

### 2.4 Correction: the worst ratio of `R_min` exceeds 2

Instance ([`competitive/rmin_11_5.py`](competitive/rmin_11_5.py), exact):
`alpha = 1`, `eps = 1/100`, knots
`0, 1/16, 3/16, 7/16, 1/2, 9/16, 13/16, 15/16, 1`, and
`m = 41/1600, 41/1600, 823/20000, 1/100, 1/100, 1/100, 823/20000, 41/1600, 41/1600`.

- `H` is convex.
- `N_opt = 3`, from the left and the right greedy certificates.
- Every processed node has a unique relaxation minimizer.
- `R_min` splits at `1/2`, `3/16`, `7/16`, `13/16` and `9/16`, so `T = 11`.
  The per-interval counts are `[1, 3, 1]`, with no split at a breakpoint.
- The note's own float simulator (`poly1d.py`) also gives `N_opt = 3`,
  `T = 11`.

So the worst ratio of `R_min` lies in `[11/5, 4)`, not "around 2". The
remark "one wasted split per breakpoint" is not the worst case. Hill-climbing
searches ([`competitive/search_grid.py`](competitive/search_grid.py),
[`competitive/search_seeded.py`](competitive/search_seeded.py),
[`competitive/worst_rmin.py`](competitive/worst_rmin.py)) found nothing above
`11/5`. These searches are weak evidence; the true worst ratio is open.

### 2.5 Incumbent robustness (Section 4.1): correct

Suppose all incumbents satisfy `U_t <= f* + g` with `g < eps`. Every node
that is not pruned then has `LB < f* - (eps - g)`, so it is invalid at
tolerance `eps - g`. The split points (exact minimizers) do not depend on
`eps`. So the proof of Theorem 1 applies verbatim at tolerance `eps - g`, and
`delta` bookkeeping is not needed. The exact check (worst case over ties,
`g = eps/3` and `9 eps/10`) passed on all instances. The containment claim
("the tree contains the fixed-`f*` tree") needs the same tie-breaking in both
runs.

### 2.6 Corollary 1 (inexact minimizers): proof incomplete

The note says that only the first and third facts of Lemma 2 change. But the
second fact uses that `B2` is invalid **at its split point**. With a
`delta`-minimizer this weakens to `phi_{B2}(y2) < delta`, so
`m(y2) < alpha (t2+d)(t1-t2) + delta`. The combination then gives

```
alpha t1 (lambda - t1) < alpha (t1 - t2)(e - t1) + delta,
```

which does not force `lambda < e`. Two correct versions:

- **(a)** For `0 <= delta < eps/2`:
  `T_eps <= 8 N_opt(eps - 2 delta) - 9`. Take the certificate at
  `eps - 2 delta`. Then the third fact reads
  `m(y1) - 2 delta >= alpha t1 (lambda - t1)`, and the two `delta`s from facts
  1 and 2 cancel against it. Lemma 1(iii) still holds.
- **(b)** The stated `N_opt(eps - delta)`, if every split point also
  satisfies `phi_B(y) < 0`. Fact 2 then has no `delta`. Such a point exists at
  every invalid node, for example the exact minimizer. So this is a
  restriction on which `delta`-minimizer the solver returns.

Whether the stated form holds for all `delta`-minimizers is open. The
reviewer's searches found no violation:

- 119,493 exact worst-case runs over all `delta`-minimizer choices, with
  `delta/eps` equal to `1/4`, `1/2` and `9/10`, on the families above
  (`thm1_check_*.log`);
- rigid instances that are tight at `eps - delta`, with `delta/eps` up to
  `0.999` ([`competitive/cor1_rigid.py`](competitive/cor1_rigid.py));
- MILP searches for chains `RRR`, `RRL`, `RLR`, `RLL` with `N_opt(eps-delta) = 2`
  and `T >= 9`, with convex or non-convex `H`
  ([`competitive/cor1_milp.py`](competitive/cor1_milp.py)). All best margins
  were negative.

The candidate set is restricted to knots, and the MILP uses random chain
geometry. So this is weak evidence.

### 2.7 Two-sided gaps (`kappa > 1`)

The note correctly states that Theorem 1 needs the exact gap and that the
two-sided case is open. The reviewer checked only one case: an exact-gap
relaxation with the larger constant `alpha'`, used against an
`alpha`-certificate, on the sharp instance. There `R_min` is still bounded,
because `N_opt(alpha')` does not grow with `1/eps`. No adversarial non-uniform
gap was tried.

## 3. Theorem 3: verified

[`competitive/thm3_check.py`](competitive/thm3_check.py) rebuilds `H_A` and
`H_B` from the lines as written in the note, in exact rationals.

- `min m = eps`, attained only at `0` and `1`, so `f* = 0` in both instances.
- The root relaxation has value `-37/300` and the unique minimizer `3/5` in
  both instances.
- The maximal intervals of agreement are exactly `[0, 3/13000]`,
  `[1/60, 27/40]` and `[9997/10000, 1]`. These are the stated sets, since
  `30 eps/13 = 3/13000`.
- `[0,b]` is valid iff `b <= s*`, and `[c,1]` is valid iff `c >= s*`, with
  `s* = 1/3` (A) and `3/5` (B). So `N_opt = 2` with a unique certificate.
- The four tight-chord segments of step 4 are confirmed.

The deterministic bound `5/3` and the randomized bound `4/3` follow as stated.
The `C^inf` smoothing remark is plausible: a convex mollification of `H` lies
above `H` and keeps the tight chord segments away from the kinks. It was not
computed. The scope caveat of Section 1 applies.

## 4. Proposition 4 and solver defaults

### 4.1 The family `R_{lambda,theta}`: correct

Steps 1–6 were checked:

- Existence of `p̄` by the intermediate value theorem.
- The minimizer is the kink when width `<= 1`.
- Nodes without `p̄` in their interior are pruned.
- The chain alternates between relative positions `p̄` and `1 - p̄`, and the
  width shrinks by `kappa` per level.

[`competitive/prop4_check.py`](competitive/prop4_check.py) reproduces every
table value. The irrational `p̄` are computed to 60 digits and the rational
ones exactly. It also confirms `T >= 2K + 1` down to `eps = 1e-32`. Two more
rows, from the same Speakman–Lee table:

| Rule | `(lambda, theta)` | `p̄` | `kappa` |
|---|---|---|---|
| ANTIGONE (per Speakman–Lee) | `(0.75, 0.10)` | `0.2287` | `0.2965` |
| BARON (per Speakman–Lee) | `(0.70, 0.01)` | `0.2421` | `0.3195` |

### 4.2 What SCIP and Couenne actually do

SCIP 10.0 (pyscipopt 6.2.1) has the defaults `branching/clamp = 0.2`,
`branching/midpull = 0.75` and `branching/midpullreldomtrig = 0.5`. The
parameter descriptions were dumped with `writeParams`.

The logic is in `SCIPbranchGetBranchingPoint`, in `src/scip/branch.c` on
master, fetched 2026-09-28. The nonlinear constraint handler calls it with no
suggestion (`cons_nonlinear.c`, the two `SCIPgetBranchingPoint(scip, var,
SCIP_INVALID)` calls). It then:

1. takes the LP value `x`;
2. forms `b = midpull (l+u)/2 + (1 - midpull) x`, where `midpull = 0.75` is
   multiplied by `r = (u - l)/(global width)` when `r < 1/2`;
3. clamps `b` to `[l + 0.2 w, u - 0.2 w]`.

So the effective rule is `(lambda, theta) = (0.25, 0.2)` on nodes of at least
half the global width, and `(1 - 0.75 r, 0.2)` below that. Speakman–Lee
describe SCIP's rule as "(mostly)" `alpha = 1`, `beta = 0.2`; that matches
only the deep-node limit. The repository's own probe B varied exactly this
parameter (`midpull = 0` for the LP value, `midpull = 1` for the midpoint)
against the default. That already shows the default is neither.

Couenne's default `branch_pt_select` is `mid-point` with
`branch_midpoint_alpha = 0.25` (`CouenneChooseVariable.cpp`). In that mode the
clamp is `closeToBounds = 0.05` (`CouenneObject.hpp`); `branch_lp_clamp = 0.2`
applies only to the `lp-clamped` and `lp-central` modes. Couenne also raises
`alpha` towards 1 when the relative gap is below `1e-3`. Per-operator
overrides (`branch_pt_select_<op>`) were not checked. With `lambda = 0.25` the
clamp is inactive, so `p̄ = 0.3117` stands.

Exact simulation of both actual rules on `f = 2|y - a|` (`prop4_check.log`,
part 2) gives the following:

- SCIP: `T` grows like `log(1/eps)` for every tested kink except `a = 1/2`.
  For example, at `a = 1/6`, `T = 9, 15, 25, 45, 89` at
  `eps = 1e-4, 1e-8, 1e-16, 1e-32, 1e-64`.
- Couenne: the same, with `T = 11, 21, 45, 89, 175` at `a = 1/6`.
- `R_min`: `T = 3` throughout.

So the practical conclusion stands, but the SCIP row of the table and the
claim that the family "contains the SCIP default" must be corrected. A proof
for SCIP's depth-dependent rule needs a fixed-point choice of the kink. One
route is to note that once `r <= 2/15`, `lambda >= 0.9` and the clamp binds at
relative position `1/6`, so the `(1, 0.2)` chain applies. Getting the kink to
that position is not proved.

### 4.3 What this means for the note's solver statements

Deep in the tree, SCIP's mixing weight `0.75 r` goes to 0 as boxes shrink.
The safeguard that persists is the clamp at 0.2. So for SCIP the mechanism of
Proposition 4 is the clamp, that is, the `(1, 0.2)` chain with `p̄ = 1/6` and
`kappa = 1/5`, and not the midpoint mixing. The root coordinator's
independent check with SCIP 10.0.2 reports the same three parameter values.

The following statements in the note need correction:

1. **Section 1.5.** "SCIP uses `(lambda, theta) = (1, 0.2)` and Couenne uses
   `(0.25, 0.2)`." Replace with:
   - SCIP 10: `lambda = 0.25` when `r >= 1/2` and `lambda = 1 - 0.75 r` below
     that, with `theta = 0.2`. So SCIP starts like `(0.25, 0.2)` and approaches
     `(1, 0.2)` as `r` goes to 0.
   - Couenne: `(0.25, 0.05)`, with gap-adaptive `alpha`.
   - The Speakman–Lee `(1, 0.2)` describes SCIP only in the deep-node limit.
2. **Summary and Section 5.2** ("the family ... contains the SCIP and Couenne
   defaults"; "which covers the practical choices"). This holds for Couenne,
   for ANTIGONE and BARON as tabulated by Speakman–Lee, and for SCIP with
   `midpull = 0`. It does not hold for SCIP's default, whose `lambda` depends
   on the node width.
3. **The Proposition 4 table row "SCIP, per Speakman–Lee".** Keep the row as
   the `(1, 0.2)` member of the family. Label it as SCIP's asymptotic (deep
   node) behaviour, or as SCIP with `midpull = 0`. Add SCIP's shallow-node rule
   `(0.25, 0.2)`, which has the same `p̄` as Couenne.
4. **Section 8.2, "Solver practice".** "Proposition 4 shows every such choice
   ... has unbounded ratio on a fixed sharp 1D instance" is proved for fixed
   `(lambda, theta)` only. For SCIP it is supported by exact simulation
   (Section 4.2) but not proved. The persistent clamp is the likely
   mechanism.
5. **Section 8.2, SCIP probe B.** The probe's "LP point" and "midpoint"
   settings are `midpull = 0` and `midpull = 1`, compared against the default
   `midpull = 0.75`. The note should say so. The probe then compares the
   `(1, 0.2)` member, pure bisection and SCIP's depth-dependent default.

## 5. Theorem 2: correct

The invariants (P1)–(P3), the choice of `a`, the per-coordinate bound
`q >= 36^(-k/n)/9` and the count were all checked.
[`competitive/thm2_check.py`](competitive/thm2_check.py) reimplements the
adversary against rules that see the box and depth. The rules are widest
bisection, coordinate cycling with depth-dependent positions, a hash-based
rule (deterministic but irregular) and a 2%-edge rule, for `n = 1, 2, 3`.
Every completed run met the bound (`thm2_check.log`). For `n = 3` only
`eps = 1e-4, 1e-8` were attempted, and only bisection and coordinate cycling
completed: the reviewer stopped the hash-based run because exact arithmetic
was too slow.

A defect in the note's `thm2_check.py`: it prunes every node that does not
contain `a` in its interior. That is wrong for `n >= 2`. Such a node can be
invalid, because the other coordinates contribute
`-alpha (a_i - l_i)(u_i - a_i)`. The script therefore undercounts `T`: for
`n = 2` bisection it reports 27, 53, 81 where the exact counts are 29, 55, 83.
Its assertions are lower bounds, so they remain valid, but the logged numbers
are not the true tree sizes. The same caveat applies to any claim that such
nodes are pruned in `n` dimensions. Section 6.1 of the note does not make that
claim.

## 6. Proposition 0: correct

The maximal valid `b(l)` exists because validity of `[l, b]` is closed in `b`.
The greedy is optimal by the exchange argument. Exact check
([`competitive/prop0_check.py`](competitive/prop0_check.py)): `T = 2 N_opt - 1`
on 3,000 instances, and the left and right greedy sizes agree.

## 7. Other points

- **Proposition 1** (the Moreau-envelope characterization of 1D validity) is
  correct as stated. Convexity of `f + alpha y^2` is needed in step 3.
- **Benchmark inconsistency in `n` dimensions.** Section 1.3 defines
  `T_opt = 2 N_guill - 1`. By that definition the Bellman rule of Section 6.3
  has ratio exactly 1 in model I_inf. The results table instead reports the
  guillotine overhead `sup N_guill/N_opt`. Choose one benchmark and use it
  throughout.
- **Section 7.1** ("without loss of generality" for rules that see only the
  box, the value and the minimizer). The piecewise-linear interpolant lies
  above `H` only when `H` is convex. The argument is fine within the convex
  class, which is the class the note uses.
- **Section 8.2, chord rule.** The relaxation minimizer is where a tangent of
  `H` is parallel to the chord of `alpha y^2` over the node. The sandwich chord
  rule uses the chord of `H` itself. The two coincide only when
  `m(l) = m(u)`. The identification should be weakened to an analogy.
- **Section 4.2, "two wasted splits".** See Section 2.3: with `N_opt = 2` the
  third node is always valid.
- **`poly1d.py` docstring** cites "Lemma 3" of the note, which does not exist.
- **Section 6.2** (the `n`-dimensional obstruction inequality) was checked
  algebraically and is correct. Conjecture 1 and the 2D separable experiments
  were not reviewed.

## 8. Novelty assessment

Sources examined by the reviewer:

- **Hansen–Jaumard–Lu (1991).** OpenAlex abstract: "nP ≤ 2nB + 1 and this
  bound is sharp", and `nPY <= 4 nB + 1` for an `eps`-optimal value together
  with a point.
- **Bachoc–Cesari–Gerchinovitz (2021).** Local full text. They call a
  multivariate question left open by Hansen–Jaumard–Lu "long-standing".
  Their Proposition 3 is a two-query certificate for `L‖x‖`.
- **Daskalakis–Diakonikolas–Yannakakis**, "How good is the Chord algorithm?"
  (SODA 2010; SIAM J. Comput. 2016; arXiv:1309.7084). Full text downloaded.
- **Baran–Demaine–Katz (2008).** Abstract via Demaine's page.
- **Speakman–Lee (2018).** Full text, arXiv:1706.08438.
- **Cheng–Basu, arXiv:2601.23249.** Abstract page.
- **SCIP and Couenne source code**, as cited in Section 4.2.

Rote (1992) and Guérin–Marcotte–Savard (2006) could not be accessed:
publisher redirects blocked them, and general web search was exhausted. DDY's
related-work section states that the analyses of Rote and of Yang–Goh
"compute only the worst-case cost … in terms of ε", with no per-instance
ratio.

Assessment by claim:

- **Theorem 1.** In 1D the Piyavskii–Shubert bound on a subinterval between
  consecutive evaluation points is determined by the two endpoint values.
  Cones from farther points are dominated, because `f` is `L0`-Lipschitz and
  the method uses `L1 >= L0`. So Piyavskii is exactly a node-local
  branch-and-bound that splits at the minimizer of the node bound. HJL's
  `n_P <= 2 n_B + 1` is then a constant competitive ratio for that rule against
  the optimal certificate: the same phenomenon, 35 years earlier.
  - What is new in Theorem 1 is the relaxation model. The gap is quadratic,
    and validity depends on `f` over the whole node rather than on two
    endpoint values.
  - The certificate-interval charging proof (Lemma 2) was not found elsewhere.
  - The note's stated difference ("Piyavskii's lower envelope is global,
    built from all evaluations") is incorrect in 1D and should be removed.
  - Originality: modest. It transfers a known phenomenon to a new relaxation
    with a new proof.
- **Theorem 3.** A per-instance lower bound for every rule in a
  restricted-information model is the framework of DDY.
  - For the ratio distance, the chord algorithm has worst-case performance
    ratio `Theta((m + log(1/eps))/(log m + log log(1/eps)))`, and every
    algorithm with Comb-oracle access has ratio at least
    `Omega(log m + log log(1/eps))`.
  - For the Hausdorff distance the bounds are
    `Theta(log(L/eps)/log log(L/eps))` and `Omega(log log(L/eps))`.
  - For the vertical distance every algorithm has unbounded ratio.

  Baran–Demaine–Katz prove a log-factor competitive ratio with a matching
  lower bound for adaptive integration. Theorem 3's two-instance construction
  is standard adversary technique; its constant `5/3` and the instances are
  new as far as checked.
  - Theorem 1 and Theorem 3 together (constant ratio, with the best constant
    in `[5/3, 4)`) contrast with DDY's non-constant ratio for the chord
    algorithm.
  - DDY should be cited as the closest competitive-analysis precedent.
  - Originality: modest.
- **Proposition 4.** No precedent was found for the statement that clamped or
  mixed branching points lose `log(1/eps)` on a fixed sharp 1D instance, while
  the pure minimizer does not. The proof is short. Its practical reading
  depends on the solver-default corrections in Section 4.
  - Originality: modest.
- **Theorem 2.** A routine adversary, as the note says.
- **Proposition 0.** The greedy exchange argument for interval covers is
  folklore.
- **Proposition 1.** The Moreau envelope is standard. Its use to characterize
  1D validity as a variable-radius `rho`-net was not found elsewhere.
  - Originality: modest.
- **Cheng–Basu.** The abstract confirms that the paper covers MILP variable
  and cut selection only, with no information model and no continuous
  branching points. The note's contrast with it is fair.

The note's novelty section should:

- cite HJL as a direct precedent for a node-local, constant-competitive rule
  in 1D;
- cite DDY for the competitive-analysis framework and the information-model
  lower bounds;
- drop the "global envelope" distinction.

An unsuccessful search does not establish novelty. The interval-analysis and
"sequentially optimal search" literature (Sukharev, Danilin) and online
geometric probing (shape probing, DDY's reference [CY]) were not searched.

## 9. Commands run

Targeted checks only. All were run from `research-20260928b/reviews/competitive/`
with single-threaded Python and exact `fractions` unless noted. No
project-wide checks were run and CI was not inspected.

| Command | Result |
|---|---|
| `python3 thm1_check.py 20000 11` and `... 20000 12` | 39,831 instances with `N >= 2`; all Theorem 1, `N = 2` and incumbent assertions pass; Corollary 1 (stated form and corrected form): 0 violations in 119,493 `delta` runs (`thm1_check_s11.log`, `thm1_check_s12.log`) |
| `python3 rmin_11_5.py` | `T = 11`, `N_opt = 3`, unique minimizers, convex `H` (`rmin_11_5.log`); cross-checked with the note's `poly1d.py` |
| `python3 worst_rmin.py 12 3000 40`; `search_grid.py {1,2} 1500 60 {0,1}`; `search_seeded.py {1,2} 6000 {1,0}` | best ratio `11/5`; nothing higher (`worst_rmin.log`, `search_grid_*.log`, `search_seeded_*.log`) |
| `python3 cor1_rigid.py`; `python3 cor1_milp.py 1 200 0`, `... 2 200 1` (HiGHS MILP, floats) | no Corollary 1 violation; all MILP margins negative (`cor1_rigid.log`, `cor1_milp_c*.log`) |
| `python3 thm3_check.py` | all Theorem 3 facts confirmed (`thm3_check.log`) |
| `python3 prop4_check.py` (mpmath 60 digits for irrational `p̄`) | table reproduced; SCIP and Couenne actual rules grow like `log(1/eps)` (`prop4_check.log`) |
| `python3 thm2_check.py` | all completed runs meet the bound; `n = 3` hash-based and 2%-edge runs stopped (`thm2_check.log`) |
| `python3 prop0_check.py 3000 5` | `T = 2 N_opt - 1` on all 3,000 instances (`prop0_check.log`) |
| pyscipopt `writeParams`; `curl` of SCIP `branch.c`, `cons_nonlinear.c`, `scip_branch.c` and Couenne `CouenneObject.{cpp,hpp}`, `CouenneChooseVariable.cpp` | the solver defaults of Section 4.2 |

## 10. What remains unchecked

- Whether Corollary 1 holds in its stated form (`eps - delta`), as opposed to
  the corrected `eps - 2 delta`.
- The exact worst ratio of `R_min` (now known to lie in `[11/5, 4)`) and of
  the best I1 rule (in `[5/3, 4)`). Lower-bound constructions beyond `5/3`
  need `N_opt >= 3`.
- The `C^inf` smoothing of Theorem 3's instances; the reviewer only argued it.
- A proof of `Omega(log(1/eps))` for SCIP's depth-dependent default. Only the
  simulation was done.
- Couenne's per-operator branching-point overrides and the gap-adaptive
  `alpha` in a real run.
- Two-sided gaps, Conjecture 1, the 2D separable experiments (`sep2d.py`),
  Section 6.1's `n`-dimensional transfer of Proposition 4 beyond the algebra,
  and the guillotine-overhead question.
- `thm2_check.py` for `n = 3` with the hash-based and 2%-edge rules. The
  reviewer stopped the run because exact arithmetic was too slow; the log
  records what finished.
- Full texts of Hansen–Jaumard–Lu, Rote (1992), Burkard–Hamacher–Rote (1991),
  Guérin–Marcotte–Savard (2006) and Baran–Demaine–Katz; the Sukharev and
  Danilin line; and online-search competitive analysis beyond DDY.
