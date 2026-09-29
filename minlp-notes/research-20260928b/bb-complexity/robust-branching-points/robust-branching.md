# Robust branching points: boundary immunity and kink competitiveness

Workstream `robust-branching-points/` of the
[bb-complexity program](../PROGRAM.md). Date: 2026-09-29, revised the same
day after the independent review
[`../../reviews/robust-branching-review.md`](../../reviews/robust-branching-review.md).
Status: reviewed, then closed by an audit
([`../../reviews/closing-audit-a.md`](../../reviews/closing-audit-a.md), item 3).
The review confirmed every numbered result apart from one parenthetical and
strengthened Proposition D. The audit restricted the scope of one bound in
Theorem A(ii). Section 11 lists all changes. The computations are commands
and logs, not certified counts.

Starting points:

- [competitive-branching.md](../branching-competitiveness/competitive-branching.md):
  in 1D, splitting at the relaxation minimizer (`R_min`) is 4-competitive
  (Theorem 1); every clamped rule `R_{lambda,theta} != R_min`, and SCIP's
  default, loses order `log(1/eps)` on explicit kinks (Propositions 4, 4').
- [face-exact-node-complexity.md](../spatial-face-exact/face-exact-node-complexity.md):
  on the McCormick kink family the unclamped relaxation point takes 3 nodes
  (Proposition 5.4(b)); a fixed clamp `beta` misses the optimal face on a
  Cantor set of kink positions, and at `a = 1/6`, `beta = 1/5` widest-side
  selection needs `Omega(eps^(-1/2))` nodes (Proposition 5.5).
- [branching-point-study.md](../minlplib-branching/branching-point-study.md):
  on 57 MINLPLib instances, removing SCIP's clamp multiplies nodes by 2.19,
  because LP values sit on variable bounds and unclamped splits create
  chains of nearly identical nodes. The clamp is protective.

Question: is there a branching-point rule that is both **(a) immune to
boundary relaxation points** (no child is a negligible fraction of its
parent, even when the relaxation point is adversarial and sits on a bound)
and **(b) competitive on kink instances**, where the unclamped relaxation
point is optimal?

## Summary

Short answer: no rule gets both (a) and a uniform form of (b). What is
achievable is a bound on the node count for each fixed kink, uniform in
`eps`. A deterministic rule, the **recentring clamp**, gets this on every
tested model. The randomized clamp gets it in 1D but not with widest-side
selection. On MINLPLib no safe rule tested differs from its reference, or
from SCIP's default, beyond seed noise.

Theory (Sections 1–5; `C_theta` is the clip at clamp `theta`, SCIP's clamp
with `branching/midpull = 0`):

- **Why SCIP's clamp fails (Theorem A).** When the relaxation point lies in
  a clamp zone, the clip splits at the zone's inner end. The child is then
  the whole zone, a rescaled copy of the parent in which the kink can sit
  anywhere, including the opposite zone.
  - This holds for every deterministic **clip schedule**: a clamp that may
    depend on depth, widths or history, with the fallback at the zone's
    inner end. Each such schedule misses an uncountable, Lebesgue-null set
    of kink positions.
  - At its alternating trap points it needs `Omega(log(1/eps))` nodes in 1D
    and with x-only selection, against `N_opt = 2`.
  - If in addition the clamp depends only on the `x`-interval history and
    `y`-splits are safe, it needs `Omega(eps^(-1/2))` nodes on the McCormick
    family with widest-side selection.
  - Ignoring the point's position inside the zone is not enough to trap: the
    midpoint fallback also ignores it and never traps for `theta <= 1/3`.
- **The claim "every deterministic fixed-clamp rule fails" is false.** The
  recentring clamp `RC_theta` puts the relaxation point at the centre of the
  child when the point is in a clamp zone but not too close to the bound. It
  is deterministic and keeps every child at least a `theta` fraction of its
  parent. It never traps (Proposition D):
  - 1D: exactly `J(theta) + 1` splits, which is Proposition C's lower bound
    for every `theta`-safe rule. So for `theta <= 1/3` it is split-optimal
    among all `theta`-safe rules, deterministic or randomized, with any
    information (strengthened after the review);
  - McCormick family with widest-side selection:
    `T <= 1 + 2/(theta^2 (1 - theta) d0)` for every `eps`, where `d0` is the
    kink's relative distance to the boundary.
- **The randomized clamp** (`theta ~ U[theta0, theta1]` independently at
  each node) is `theta0`-safe.
  - In 1D and with x-only selection it fixes the trap (Theorem B):
    `E[T]` is bounded uniformly in `eps` for every kink position, with an
    explicit bound, and `E[#splits] = log(1/d0)/E[log(1/theta)] + O(1)`.
    For `[0.1, 0.3]` at the trap point `a = 1/6` of `C_0.2`, the expected
    number of splits is 2.02.
  - Under widest-side selection it does not (Proposition E): `E[T]` grows at
    least like `log(1/eps)` (proved), numerically like `eps^(-gamma)` with
    fitted `gamma` 0.18–0.25 (one outlier, 0.31; Conjecture E'). For kinks
    near the boundary even the median grows.
  - Drawing the clamp once per (variable, interval) ("keyed") keeps the
    median bounded but gives exactly the same mean.
- **Price of safety (Proposition C).** Every `theta0`-safe rule, even a
  randomized rule with full knowledge of `f`, needs at least
  `J + 1 = ceil(log(theta0/a)/log(1/theta0)) + 1` splits on a kink at
  distance `a < theta0` from the boundary. Its worst-case ratio over the 1D
  kink family is therefore at least of order `log(1/eps)/log(1/theta0)`,
  while `R_min` uses 3 nodes. The obstruction is safety, not information.
  Recentring attains the bound exactly. On the other side, a `theta0`-safe
  rule halves boundary chains within about `ln 2/theta0` splits (Lemma 0).
- **Incumbent rule.** Splitting at the incumbent's coordinate (BARON's rule)
  creates at most one sub-`theta` child per distinct incumbent value and
  coordinate on any path (Proposition F). With an optimal incumbent it uses
  3 nodes in 1D, and on the McCormick family when `x` is split first; nodes
  that do not contain the incumbent fall back to the clip.

Experiments (SCIP 10.0.2, PySCIPOpt 6.2.1):

- **Two ways to change only the point.**
  - *Arm P* keeps SCIP's own variable selection and point formula, and
    redraws `branching/clamp` from `U[0.1, 0.3]` whenever a node is
    focused.
  - *Arm X* is a branching plugin. It re-implements cons_nonlinear's
    variable selection on the external candidates and splits at the rule's
    point (default, clip, randomized, recentring, incumbent, no clamp).
  - Default and LP-point runs reproduce the earlier study's node counts
    exactly (168/168 and 163/163 optimal runs).
- **Synthetic kinks in SCIP** (theory model: best-first, incumbent given, no
  propagation or cutoff reductions; 5 seeds, `eps = 1e-2 ... 1e-8`).
  - 1D, `a = 1/6`: `C_0.2` needs 3, 7, 9 and 13 nodes as `eps` shrinks; the
    randomized clamp needs a mean of 5 at `1e-8`; recentring needs 5 at
    every `eps`.
  - McCormick family, `a = 1/6`, `eps = 1e-8`. With SCIP's selection:
    `C_0.2` 7,190 nodes, randomized clamp 228 (range 3–1,091). With the
    plugin's selection: `C_0.2` 9,743, randomized clamp 86 (3–383),
    recentring 21.
  - McCormick, kinks near the boundary (`a = 0.0102`): `C_0.2` 26, the
    randomized clamp 766 (range 7–3,443). Randomization hurts there, as
    Proposition E predicts.
  - Recentring stays at 16–88 nodes on every tested kink.
  - SCIP's default point (midpull 0.75) grows on every kink, with or
    without the random clamp: 1,587–6,828 nodes at `1e-8`. The midpoint
    pull, not the clamp, dominates there.
- **MINLPLib** (57 instances, 3 seeds, 60 s, 2,052 runs). Node ratios
  against the matching fixed-clamp rule, with 95% CI:

  | Comparison | Node ratio (95% CI) |
  |---|---|
  | randomized clamp vs default, SCIP's selection | 0.96 (0.87–1.06), p = 0.58, no separated instance |
  | randomized clamp vs clamp 0.2, LP point | 1.00 (0.90–1.09) |
  | randomized clamp vs clamp 0.2, plugin | 1.00 (0.93–1.07) |
  | recentring vs clip, both in the plugin with midpull 0 | 0.94 (0.86–1.01), p = 0.29 |
  | recentring (plugin) vs SCIP's default | 0.92 (0.71–1.14), p = 0.52 |
  | incumbent rule vs clip | 1.05 (0.95–1.17) |
  | no clamp vs clip | 2.00 (1.43–2.96), p = 3e-5; 18 of 20 separated instances are losses |

  - The randomized clamp is **neutral beyond seed noise**, and so are
    recentring and the incumbent rule.
  - Under the LP-point plugin the clamp moves half of the continuous
    splits, and a third of all continuous splits have the LP value on a
    bound. Where such a split lands inside `[0.1, 0.3]` of the domain
    evidently matters little on these instances.
  - Removing the clamp is clearly harmful again, through boundary chains.

## 1. Model and rules

### 1.1 Instances

- **1D exact-gap kink** (Proposition 4 of the competitive note):
  `f_a(y) = 2 alpha |y - a|` on `[0,1]`, `a in (0,1)`, node relaxation
  `f_a - alpha (y - l)(u - y)`, optimum `f* = 0`, incumbent `f*`, tolerance
  `eps`.
  - A node `[l,u]` is open (not pruned) iff `a in (l,u)` and
    `alpha (a - l)(u - a) > eps`; its relaxation minimizer is `a`
    (steps 2–3 of the proof of Proposition 4 there).
  - `N_opt = 2` and `R_min` uses 3 nodes, for every `a` and every
    `eps < alpha a (1 - a)`.
- **McCormick kink family** (Section 5 of the face-exact note):
  `f_{a,b}(x,y) = L|x - a| + c (x - a)(y - b)` on `[0,1]^2`,
  `L > |c| max(b, 1 - b)`, termwise McCormick.
  - A box is open iff `l_x < a < u_x` and
    `|c| w_y (a - l_x)(u_x - a)/w_x > eps`
    (proof of Proposition 5.7 there).
  - At an open box the relaxation minimizer is `(a, l_y + rho w_y)` for
    `c < 0`, where `rho = (a - l_x)/w_x`.
  - `N_opt = 2`; the unclamped relaxation point takes 3 nodes.
  - Selections: **x-only** (split `x` at every open box; the counts are then
    those of the 1D chain) and **widest side** (ties to `x`).
- **Chain notation.** In both families the `x`-interval of an open box
  contains `a` at a relative position `rho in (0,1)`; write
  `d = min(rho, 1 - rho)` for its relative distance to the nearer end. `S`
  is the number of `x`-splits along the chain of `x`-intervals until one
  lands on `a`, computed with `eps = 0`; a positive `eps` can only stop the
  chain earlier. In 1D, and in the McCormick family with x-only selection,
  `T <= 2S + 1`.

### 1.2 Rules

For a node `[l,u]` of width `w`, relaxation point `p` and clamp
`theta in (0, 1/2)`:

| Rule | Split point |
|---|---|
| `R_min` | `p` |
| clip `C_theta` (SCIP's clamp; SCIP with `branching/midpull = 0`) | `clip(p, l + theta w, u - theta w)`: `p` if it lies in `[l + theta w, u - theta w]`, else the nearer clamp point |
| clip schedule `C_Theta` | as `C_theta` with `theta = theta_B`, any function of the sequence of boxes from the root to `B` (depth, widths, which side earlier splits fell on, ...), but not of the relaxation points; the fallback stays at the zone's inner end |
| randomized clamp `C_[theta0,theta1]` | as `C_theta` with `theta ~ U[theta0, theta1]` drawn independently at every node |
| keyed randomized clamp | as the randomized clamp, but one draw per distinct interval of the branching variable, shared by all nodes with that interval |
| recentring clamp `RC_theta` (`theta <= 1/3`) | `p` if it lies in `[l + theta w, u - theta w]`; if `p < l + theta w`, split at `l + max(theta w, 2(p - l))`, so that `p` becomes the centre of the child when that child is not too small; mirror image above. `theta <= 1/3` keeps the split inside `[l + theta w, u - theta w]` |
| incumbent rule `INC_theta` | the incumbent's coordinate if the incumbent lies in the node and the coordinate strictly inside `(l,u)` (BARON's rule, face-exact note §5.3); else `C_theta` |

### 1.3 Safety

A rule is **`theta0`-safe** if every split point lies in
`[l + theta0 w, u - theta0 w]`, so each child keeps at least a `theta0`
fraction of its parent's width, whatever the relaxation point.

Safety is measured against a **boundary adversary**, which chooses the
relaxation point of every node (any point of the node, including a bound)
and which nodes stay open. This models SCIP's LP values on variable bounds
(Section 3.4(a) of the MINLPLib study). In the kink families the adversary
has no power: open nodes have their relaxation point at the kink, strictly
inside.

- `C_theta`, `C_Theta` with `theta_B >= theta0`, `C_[theta0,theta1]` and
  `RC_theta` (with `theta0 = theta`) are safe. `R_min` is not.
- **Lemma 0 (boundary chains).**
  - (i) Under a `theta0`-safe rule every child is at most `(1 - theta0)`
    times as wide as its parent. So along any root-to-leaf path, whatever the
    relaxation points, the width halves within
    `ceil(ln 2 / -ln(1 - theta0))` splits (4 splits for `theta0 = 0.2`).
  - (ii) A rule that splits exactly at `p` whenever `p` lies at relative
    distance at least `delta` from both ends can be forced by the boundary
    adversary, with relaxation points at relative distance `delta`, to need
    at least
    `ln 2 / -ln(1 - delta) >= (1 - delta) ln 2 / delta` splits per halving
    along a path of nearly identical nodes. For `R_min`, `delta` is
    arbitrary.
  - *Proof.* (i) is immediate. (ii) Place `p` at relative distance `delta`
    from the lower end at every node and follow the upper child, of width
    `(1 - delta) w`. □

  Lemma 0(ii) is the mechanism the MINLPLib study observed: with
  `clamp = 0`, SCIP splits `1e-9` from the bound, and the trees have depths
  in the thousands.

## 2. Why the clip fails: clip schedules (Theorem A)

In the kink families the relaxation point is `a` at every open box. If
`d >= theta`, the clip splits at `a` and the chain ends. If `rho < theta`,
it splits at `l + theta w`, and the child that contains `a` is the whole
clamp zone `[l, l + theta w]`, in which `a` sits at relative position
`rho/theta`. This child is a rescaled copy of the parent, and the new
position can be anywhere in `(0,1)`, including the opposite clamp zone. The
mirror statement holds for `rho > 1 - theta`. This is the map `T` of the
face-exact note's Proposition 5.4(c); its orbits that stay in the clamp
zones form the trap set.

**Theorem A (clip schedules have trap sets).** Let `C_Theta` be a clip
schedule (Section 1.2: the fallback is the zone's inner end, and the clamp
is a deterministic function of the box path) with values
`theta_B in [theta0, theta1]`, `0 < theta0 <= theta1 < 1/2`.

- (i) The set `K_Theta` of kink positions `a in (0,1)` at which `C_Theta`
  never splits at `a` is uncountable and Lebesgue-null.
- (ii) At each of the two alternating trap points `a in K_Theta` (itinerary
  `L, R, L, R, ...` or `R, L, R, L, ...`), on the 1D kink `f_a`, for every
  `eps < alpha theta0/4`,
  `T >= 2K + 1` with `K = ceil( log(alpha theta0/(4 eps)) / (2 log(1/theta0)) )`,
  while `N_opt = 2` and `R_min` uses 3 nodes.
  - For the uncountably many points whose itinerary has runs of length at
    most 2, the same holds with `theta0/4` replaced by `theta0^2/4` in `K`.
  - On the McCormick family with x-only selection a box of full height has
    bound `|c| rho (1 - rho) w`, linear in its width. So for
    `eps < |c| theta0/4`:
    - at the two alternating points, `T >= 2K' + 1` with the larger
      `K' = ceil( log(|c| theta0/(4 eps)) / log(1/theta0) )`;
    - at the points whose runs have length at most 2, only
      `T >= 2K' - 1`.

    The second bound uses `theta0^2/4`, which replaces `K'` by `K' - 1`.
    `2K' + 1` can fail there: for the fixed clamp 1/5 at `a = 1/30`
    (itinerary `L, L, R, L, R, ...`), with `|c| = 1` and `eps = 1/25`,
    `T = 1 < 3`. *(Scope corrected after the closing audit.)*
  - *(Corrected after the review.* The first version claimed the stated `K`
    for uncountably many points. That is false: for the fixed clamp 1/5, a
    run of length 2 at step `k` gives `rho_k (1 - rho_k) < theta^2 = 0.04 <
    theta0/4`, so node `k` is already closed for some `eps` at which `K > k`;
    only 1/6 and 5/6 qualify.)
- (iii) If `theta_B` depends only on the sequence of `x`-intervals from the
  root (for example on depth in `x`, on the relative width as in SCIP, or on
  past clamp events of `x`), and `y`-splits keep each child at least a
  `theta0` fraction of its parent, then for the same `a` and widest-side
  selection on the McCormick family, `T >= theta0^2 |c|^(1/2) / (2 eps^(1/2))`
  for every `eps < theta0^2 |c|/4`.

*Proof.*

1. **Nested zones.** Build nested intervals from `I_0 = [0,1]` by choosing
   at step `k` one clamp zone of `I_k = [l_k, u_k]`, with
   `theta_k = theta_{I_k}` (the schedule is evaluated on the box path, which
   is determined by the choices so far): the left zone
   `(l_k, l_k + theta_k w_k)` or the right zone
   `(u_k - theta_k w_k, u_k)`. Set `I_{k+1}` to the closure of the chosen
   zone, of width `w_{k+1} = theta_k w_k`.
2. **The rule follows the itinerary.** If `a` lies in the chosen zone of
   `I_k`, then `C_Theta` splits `I_k` at the zone's inner end and the child
   containing `a` is `I_{k+1}`. So if `a` lies in every chosen zone, no split
   lands on `a`.
3. **Non-empty intersection.** The nested closed intervals `I_k` have a
   common point `a`. Suppose the itinerary uses both sides infinitely often.
   For each `k`, a later left choice moves the right end of the intervals
   strictly inside `I_{k+1}`, and a later right choice moves the left end,
   so `a` lies in the open zone chosen at step `k`. Distinct itineraries
   choose disjoint zones at their first difference (the two zones of a node
   are disjoint because `theta < 1/2`), hence give distinct points. There
   are uncountably many itineraries that use both sides infinitely often,
   which gives (i) apart from the measure. The `2^k` zones of depth `k` have
   total length at most `(2 theta1)^k -> 0`, so `K_Theta` is null.
4. **Alternating itinerary.** Take the itinerary `L, R, L, R, ...` and its
   point `a`. At an `L` step `a < l_k + theta_k w_k`, and at the following
   `R` step `a > u_{k+1} - theta_{k+1} w_{k+1}` with
   `u_{k+1} = l_k + theta_k w_k`. So the relative position satisfies
   `theta_k (1 - theta_{k+1}) < rho_k < theta_k`, and since
   `theta_{k+1} < 1/2`, `rho_k (1 - rho_k) >= theta0/4`. The mirror
   argument holds at `R` steps. More generally, if the run containing step
   `k` has `r` further steps on the same side (including `k`) before a
   switch, then `rho_k > theta_k ... theta_{k+r-1} (1 - theta_{k+r}) >=
   theta0^r/2`. So itineraries with runs of length at most `q` give
   `rho_k (1 - rho_k) >= theta0^q/4`. Itineraries with runs of length 1 or
   2 are uncountable.
5. **(ii).** The chain node `I_k` is open iff
   `alpha rho_k (1 - rho_k) w_k^2 > eps`. Since
   `w_k >= theta0^k` and `rho_k (1 - rho_k) >= theta0/4`, this holds for
   `k = 0, ..., K - 1`. Each open chain node is internal, so `T >= 2K + 1`.
   With runs of length at most 2, use `theta0^2/4` instead. With x-only
   selection the McCormick chain is the same, and a box of full height has
   bound `|c| w_y (a - l)(u - a)/w_x = |c| rho_k (1 - rho_k) w_k` (the first
   version wrote `w_k^2` here). At the alternating points this is at least
   `|c| (theta0/4) theta0^k`, which gives `K'`. At points with runs of
   length at most 2 it is at least `|c| (theta0^2/4) theta0^k`, which gives
   `ceil(log(|c| theta0^2/(4 eps))/log(1/theta0)) = K' - 1` (for `K' >= 1`)
   and hence `T >= 2K' - 1`.
6. **(iii), common columns.** At every open box the `x`-split point
   depends only on the `x`-interval, because the relaxation point is `a` and
   `theta_B` depends only on the `x`-interval path. So all open boxes with
   `x`-interval `I_k` ("level `k`") split `x` at the same point, as in step
   1 of Proposition 5.4(c) of the face-exact note.
7. **(iii), aspect ratio.** Every box has `w_y >= theta0 w_x`: the root has
   `w_x = w_y`; an `x`-split happens only when `w_x >= w_y` and shrinks
   `w_x`; a `y`-split happens only when `w_y > w_x` and each child keeps
   `w_y' >= theta0 w_y`.
8. **(iii), count.** A level-`k` box has bound magnitude
   `|c| w_y w_k rho_k (1 - rho_k) >= |c| theta0^2 w_k^2 / 4`. Let `K` be the
   largest `k` with `|c| theta0^2 w_k^2/4 > eps`. Then every box of level at
   most `K` is open, so the level-`K` boxes are refined in `y` until
   `w_y <= w_K` and then split in `x`; at that moment they partition `[0,1]`
   in `y`, so there are at least `1/w_K` of them. Finally
   `|c| theta0^2 (theta_K w_K)^2/4 <= eps` gives
   `w_K <= 2 eps^(1/2) / (theta0^2 |c|^(1/2))`. □

Remarks:

- **Checks.** `chain1d.py` part [A] builds the alternating trap point in
  200-digit arithmetic for four schedules (fixed `1/5`; depth-alternating
  `1/5, 1/4`; width-dependent `1/10 + w/5`; position-dependent `1/8 + l/4`)
  and replays the rule: no split lands on the point in 60 steps, and the
  1D counts respect (ii) at `eps = 1e-4 ... 1e-24` (for example 35, 37, 27
  and 29 nodes at `1e-24` against the bound 25 computed with
  `theta0 = 1/10`). Log: `chain1d.log`.
- **Checks added after the review** (`chain1d.py A2`, log `chain1d_A2.log`,
  300-digit arithmetic):
  - For the fixed clamp 1/5, itineraries with one run of length 2 at step
    0, 1, 3 or 5 violate the first version's `K` from
    `eps = 0.049, 0.002, 3.2e-6, 5.0e-9` on.
  - For 20 random itineraries with runs of length at most 2 and each of the
    four schedules, `T >= 2 K_2 + 1` holds at `eps = 1e-2 ... 1e-48`, where
    `K_2` uses `theta0^2/4`. It holds with equality for three schedules.
  - McCormick x-only chain at the alternating point of the fixed clamp 1/5:
    `T = 11, 23, 45, 69, 91, 137` at `eps = 1e-4, 1e-8, 1e-16, 1e-24, 1e-32,
    1e-48`, against `2K' + 1 = 9, 21, 45, 67, 89, 135`. The first version's
    `2K + 1` was 5, 11, 23, 35, 45, 69.
  - The review's own exact counts agree.
- **What causes the trap.** The proof uses one property of the clip: when
  the relaxation point is in a clamp zone, the split is at the zone's inner
  end, whose position does not depend on where the point sits inside the
  zone. The child is then the whole zone, and every position is possible
  again. Depth-, width- and history-dependent clamps keep this property.
- **The task's claim (1) is false as stated.** "Every deterministic rule
  with a fixed clamp fails on some kink" does not hold. The recentring clamp
  `RC_theta` is deterministic and `theta`-safe, and it never traps
  (Proposition D); it uses the point's position inside the zone.
  - The midpoint fallback (split at the midpoint when the point is in a
    clamp zone) ignores that position and also never traps when
    `theta <= 1/3`.
    - Measure the kink's position from the end it started near. While that
      position is below `theta`, the midpoint split doubles it.
    - When it first reaches `theta`, it lies in
      `[theta, 2 theta) ⊂ [theta, 1 - theta]`, so the next split is at the
      kink: `S = ceil(log2(theta/d0)) + 1`.
    - The review checked this exactly on 9,000 kinks, and the closing audit
      on about 20,000.
  - The bound `theta <= 1/3` is sharp (closing audit). For `theta > 1/3` the
    kink `a = 1/3` traps: the midpoint map is then the doubling map on both
    zones, with the orbit `1/3, 2/3, 1/3, ...`.
  - So what traps is the fallback at the zone's inner end, not the neglect
    of the position.
- **SCIP's default.** SCIP's point with midpull `0.75` (scaled by the
  relative width below `1/2`) is not a clip of `a`, so Theorem A does not
  cover it. Proposition 4' of the competitive note gives one kink with
  `log(1/eps)` loss. As the pull vanishes with depth, the zones' images
  approach the full interval, so a trap set is expected; this is not proved
  here.

## 3. The randomized clamp in 1D and with x-only selection (Theorem B)

**Theorem B.** Let `0 < theta0 < theta1 <= 1/2`, `D = theta1 - theta0`,
`mu = E[log(1/theta)]` for `theta ~ U[theta0, theta1]`, and

```
delta = log(1/theta1) - theta0/D  > 0.
```

For a kink at relative distance `d0` from the nearer end of the root, the
randomized clamp `C_[theta0,theta1]` satisfies

```
E[S] <= A + B log(1/d0),                                A = 1 + theta1/(D delta),  B = 1/delta,
E[S] <= (log(1/d0) - log 2)/mu + A + B log(2/theta0)     (d0 < theta0/2),
E[S] >= (log(1/d0) - log(2/theta0))/mu.
```

So `E[T] <= 2 E[S] + 1` is bounded uniformly in `eps`, for every `a`, in 1D
and on the McCormick family with x-only selection, and the growth in
`log(1/d0)` has the exact slope `1/mu`. Every child keeps at least a
`theta0` fraction of its parent.

For `[theta0, theta1] = [0.1, 0.3]`: `delta = 0.704`, `A = 3.13`,
`B = 1.42`, `1/mu = 0.604`.

*Proof.*

1. **The chain.** From distance `d`, a draw `theta <= d` splits at `a`. A
   draw `theta > d` clamps; the kink then sits at relative position
   `r = d/theta in (0,1)` of the child, so the new distance is
   `d' = min(r, 1 - r)`.
2. **Supersolution.** Let `g(d) = A + B log(1/d)`. It suffices to show
   `g(d) >= 1 + E[g(d'); theta > d]` for all `d in (0, 1/2]`: then
   `E[min(S, n)] <= g(d0)` by induction on `n`, and monotone convergence
   gives `E[S] <= g(d0)`.
3. **One-step estimate.** Write `log(1/d') = log(1/d) - log(1/theta) + log(r/(1-r))^+`.
   The last term is positive only for `theta < 2d`, and with
   `theta = d(1 + s)`,
   `integral_d^(2d) log(d/(theta - d)) dtheta = d integral_0^1 log(1/s) ds = d`.
   With `P_f = P(theta > d)`:
   `E[log(1/d'); theta > d] <= P_f log(1/d) - P_f log(1/theta1) + d/D`.
4. **Reduction.** The inequality of step 2 follows from
   `(1 - P_f)(A + B log(1/d)) + B P_f log(1/theta1) >= 1 + B d/D`.
5. **Cases.**
   - `d < theta0`: `P_f = 1`; need `B (log(1/theta1) - d/D) >= 1`, true since
     `d < theta0` and `B = 1/delta`.
   - `theta0 <= d < theta1`: put `s = (d - theta0)/D = 1 - P_f`. Using
     `log(1/d) >= 0`, it suffices that
     `s A + (1 - s) B log(1/theta1) >= 1 + B theta0/D + B s`. This is linear
     in `s`; at `s = 0` it is the previous case, and at `s = 1` it reads
     `A >= 1 + B theta1/D`, the definition of `A`.
   - `d >= theta1`: `P_f = 0` and `g >= 1`.
6. **Slope.** While `d < theta0/2`, every draw clamps and `d/theta < 1/2`,
   so `log(1/d)` decreases by exactly `log(1/theta_j)`, i.i.d. with mean
   `mu`. Let `N` be the first index with `d_N >= theta0/2`; `N` is bounded.
   Then `d_N < 1/2`, and Wald's identity gives
   `mu E[N] = log(1/d0) - E[log(1/d_N)]`, which lies between
   `log(1/d0) - log(2/theta0)` and `log(1/d0) - log 2`. After `N`, the
   first bound applies from `d_N >= theta0/2`, by the strong Markov
   property. □

Remarks:

- **Numbers** (`chain1d.py` [B], `10^6` chains per entry, standard errors
  0.001–0.002). For `[0.1, 0.3]`: `E[S] = 2.02` at `a = 1/6` (the trap
  point of `C_0.2`), `3.32` at `a = 3/238`, `1.93` at `a = 0.1999`, `6.31`
  at `a = 1e-4` and `11.88` at `a = 1e-8`. The first bound gives 5.68, 9.34
  and 5.42 for the first three. For `a = 1e-4` and `1e-8` the second bound
  is smaller: 12.5 and 18.1 (the first gives 16.2 and 29.3). For this
  window the 99.99% quantile of `S` is at most 20 in `10^6` chains (21 at
  `a = 1e-8` in the review's `10^7`).
- **Proof checks.** The supersolution inequality of step 2 holds with slack
  at least 0.54 on a grid of `d` for four windows (`chain1d.py S`). A value
  iteration of `E[S](d)` on a grid down to `d = 1e-14` agrees with the
  Monte Carlo values to `0.002` and has slope `0.6043` in `log(1/d)`,
  against `1/mu = 0.6044`.
- **Narrow windows.** Theorem B needs `delta > 0`. The windows
  `[0.15, 0.25]` and `[0.19, 0.21]` violate it, but `E[S]` stays small
  numerically: at `a = 1/6`, 2.54 and 3.73.
- **Node counts** (`sim_kink.py`, 20,000 runs per entry). On the 1D kink at
  `a = 1/6`, `C_[0.1,0.3]` needs a mean of 3.7, 4.7, 5.0, 5.1 and 5.0 nodes
  at `eps = 1e-2, 1e-4, 1e-8, 1e-16, 1e-32`; `C_0.2` needs 3, 7, 13, 23 and
  47.
- **Safety.** Worst-case safety is that of the lower end `theta0`; against
  an oblivious boundary adversary the expected chain behaves like a fixed
  clamp near the mean of `theta`.

## 4. The price of safety (Proposition C)

**Proposition C.** Let `R` be any `theta0`-safe rule, deterministic or
randomized, with any information about `f` (even model `I_inf` of the
competitive note). On the 1D kink `f_a` with `a < theta0` (by symmetry the
same holds for `1 - a < theta0`):

- if `alpha a^2 (1 - theta0)/theta0 > eps`, then
  `T >= 2J + 1` with `J = ceil( log(theta0/a) / log(1/theta0) )`, and a run
  that ends by splitting at `a` has `S >= J + 1`;
- consequently, for every `eps < alpha theta0 (1 - theta0)/2`, some kink
  position forces `T >= log(alpha theta0 (1 - theta0)/(2 eps)) / log(1/theta0) + 1`,
  while `N_opt = 2` and `R_min` uses 3 nodes. The competitive ratio of `R`
  over the 1D kink family is therefore at least
  `(1/3) log(alpha theta0 (1 - theta0)/(2 eps)) / log(1/theta0)`, unbounded
  as `eps -> 0`.

*Proof.* While the chain node `[l,u]` has `a - l < theta0 (u - l)`, every
allowed split point exceeds `a`, so the child containing `a` is `[l, s]`
and `l` stays `0`. Its width shrinks by a factor at least `theta0` per
split, so the first `J` chain nodes all have `a < theta0 u`. Each of them
is open, because `alpha a (u - a) > alpha a (a/theta0 - a) >= eps`. The
second statement takes `a = (2 theta0 eps/(alpha (1 - theta0)))^(1/2)`. □

Consequences:

- **(a) and uniform (b) are incompatible.** No safe rule, however much it
  knows, is competitive over all kink positions. The obstacle is not
  information but safety: a kink closer to the boundary than `theta0` is
  indistinguishable from a boundary relaxation point unless the rule is
  allowed to make a small child.
- **What is achievable is per-instance boundedness.** For each fixed `a`,
  bound `T` uniformly in `eps`. Theorem A shows that clip schedules fail
  this on a trap set; Theorem B and Proposition D show that the randomized
  and recentring clamps achieve it.
- **Recentring is exactly optimal; the randomized clamp is near
  optimal.** With `J(theta)` the bound of Proposition C, `RC_theta` uses
  exactly `J(theta) + 1` splits for `theta <= 1/3` (Proposition D), so the
  bound is tight. `C_[theta0,theta1]` uses `log(1/d0)/mu + O(1)` in
  expectation. `chain1d.py` [C] tabulates both: for `a = 1e-8`, the lower
  bound for `theta0 = 0.2` is 12 splits, and `RC_0.2` and `C_0.2` use
  exactly 12; `C_[0.1,0.3]` uses 11.9 in expectation, against 8 for
  `theta0 = 0.1`. The clip also meets the bound in these rows. On other
  kinks it exceeds it by up to 17 splits (`chain1d_D.log`), or traps
  (Theorem A).
- **Two-sided tradeoff.** Lemma 0 and Proposition C together: a
  `theta0`-safe rule halves boundary chains within about `ln 2/theta0`
  splits and pays about `log(1/d)/log(1/theta0)` splits for a kink at
  distance `d`. Making boundary chains short (large `theta0`) makes
  near-boundary kinks expensive, and conversely; the dependence on `theta0`
  is only logarithmic on the kink side.

## 5. Recentring, widest-side selection and the incumbent rule

**Proposition D (recentring clamp).** Let `0 < theta <= 1/3` and `d0 < 1/2`
the kink's relative distance from the nearer end of `[0,1]`. Write
`J = J(theta) = min{ j >= 0 : d0 >= theta^(j+1) }`, which equals
`ceil(log(theta/d0)/log(1/theta))` for `d0 < theta` (the `J` of
Proposition C) and 0 for `d0 >= theta`, and
`m = min{ j >= 0 : d0 >= theta^(j+1)/2 }`.

- (i) On the chain, `RC_theta` splits at `a` after exactly `S = J + 1`
  splits. By Proposition C no `theta`-safe rule, deterministic or
  randomized and with any information, needs fewer, so `RC_theta` is
  split-optimal among `theta`-safe rules in 1D and on the McCormick family
  with x-only selection. *(Strengthened after the review; the first version
  stated `S <= J + 2`.)*
- (ii) On the McCormick family with widest-side selection (ties to `x`),
  `T = 3` if `d0 >= theta`, and otherwise
  `T <= 1 + 4 theta^(-(m+2))/(1 - theta) <= 1 + 2/(theta^2 (1 - theta) d0)`,
  for every `eps`.

*Proof.*

1. **The orbit.** If `d < theta/2`, `RC_theta` clamps as `C_theta` does;
   the kink moves to `d/theta < 1/2`, on the same side. If
   `theta/2 <= d < theta`, the split is at `l + 2 rho w` (or its mirror),
   which lies in `[l + theta w, l + 2 theta w)` and hence, as
   `theta <= 1/3`, in `[l + theta w, u - theta w]`. The child has the kink
   at its centre, and the next split is at `a` because `1/2 >= theta`. If
   `d >= theta`, the split is at `a`. So after `m` clamps the distance is
   `d_m = d0 theta^(-m) in [theta/2, 1/2)`.
2. **Counting (the review's argument, rederived).** `m <= J`, because
   `theta^(j+1)/2 < theta^(j+1)`.
   - If `d_m >= theta`, then `d0 >= theta^(m+1)`, so `J <= m`, hence
     `J = m`, and `S = m + 1 = J + 1`.
   - If `theta/2 <= d_m < theta`, then `d0 < theta^(m+1)`, so `J >= m + 1`.
     Also `d0 >= theta^(m+1)/2 >= theta^(m+2)` because `theta <= 1/2`, so
     `J <= m + 1`. Hence `J = m + 1` and `S = m + 2 = J + 1`.
   - So `S = J + 1` directly; this direct argument is the closing audit's.
     Proposition C, which gives `S >= J + 1` for every `theta`-safe run
     ending at the kink, is needed only for the optimality claim.
3. **Widest side.** The `x`-orbit is deterministic and depends only on the
   `x`-interval, so, as in Proposition 5.4(c) of the face-exact note, all
   open boxes with the same `x`-level share their `x`-interval `I_k`, with
   `|I_k| >= theta^k`. Every box has `w_y >= theta w_x` (the aspect
   invariant of step 7 of Theorem A, valid for every `theta`-safe rule), so
   the level-`k` boxes that are split in `x` have
   `w_y in [theta |I_k|, |I_k|]`. They partition `[0,1]` in `y`, so there
   are at most `theta^(-(k+1))` of them, and at most `2 theta^(-(k+1))`
   internal nodes at level `k`, for `k <= k0 <= m + 1`. Summing gives the
   first bound, and `theta^(-m) <= 1/(2 d0)` gives the second. □

Checks:

- `chain1d.py D` (log `chain1d_D.log`, exact rationals) tests 3,090 kinks
  for each `theta in {1/10, 1/5, 1/4, 3/10, 1/3}`: 3,000 log-uniform
  distances down to `1e-12`, plus `theta^j` and `theta^j/2` perturbed by
  `0, ±1e-6, ±1e-2`.
  - `S_RC = J + 1` in every case.
  - The clip exceeds `J + 1` by up to 5, 8, 9, 15 and 17 splits.
  - The review ran the same test independently on 14,670 kinks.
- At `a = 1/6` and `theta = 0.2`, `RC_0.2` takes 5 nodes in 1D and at most 17
  on the McCormick family with widest-side selection. In exact arithmetic
  it is 17 for `eps <= 0.02` and fewer above: 9, 5, 3 and 1 node from
  `eps = 0.021, 0.042, 0.084, 0.139` on. The review quoted a threshold of
  0.0123; with this note's convention (`|c| = 1`) the change is at about
  0.021.
- `C_0.2` takes 19,537 nodes at `eps = 1e-8` there, in exact arithmetic
  (`exact2d.py`, log `exact2d.log`, which also gives 13, 39, 167, 547,
  1,513 and 4,917 at `eps = 1e-2 ... 1e-7`). Floating-point runs give
  19,541, because rounding breaks width ties `w_x = w_y` toward `y`, as
  documented in the face-exact note. The first version quoted 19,541.

**Proposition E (randomized clamps under widest-side selection).** On the
McCormick family with `c = -1`, `L = 2`, widest-side selection (ties to
`x`) and `C_[theta0,theta1]` for both coordinates, let
`a in (theta0, theta1)`, `a < 1/2`, and `g = min(theta0/2, 1 - a/theta1)`.
Then for `eps < g^2 theta0^3`,

```
E[T] >= (a theta0 / (2 theta1 D)) * log( g theta0^(3/2) / eps^(1/2) ),
```

which tends to infinity as `eps -> 0`.

*Proof.*

1. **A near-boundary flip.** At the root, `x` is split with clamp
   `theta_root`. If `theta_root in (a, a/(1 - g))`, the clamp binds, and
   the child `[0, theta_root] x [0,1]` has the kink at distance
   `d1 = 1 - a/theta_root in (0, g)` from its upper end. The density of
   `d1` on `(0, g)` is `a/(D (1 - d1)^2) >= a/D`.
2. **Aspect ratio.** As in step 7 of Theorem A, every box has
   `w_y >= theta0 w_x`.
3. **Climb along one column.** Fix `Y in [0,1]` and follow the boxes that
   contain the segment `{a} x {Y}`. While the kink's distance is below
   `theta0/2`, every `x`-split clamps and moves it to `d/theta < 1/2`. Let
   `v(Y)` be the first box on this path that is split in `x` with distance
   at least `theta0/2`. Its `x`-width is `theta_root d1/d(v)` with
   `d(v) < 1/2`.
4. **The path is open.** A box on it has bound magnitude at least
   `w_x (theta0 w_x) d/2 = (theta0/2) theta_root^2 d1^2/d >= theta0^3 d1^2`,
   so all these boxes are open when `d1 > (eps/theta0^3)^(1/2)`.
5. **Counting.** The boxes `v(Y)` form an antichain of processed boxes, so
   their number is `integral_0^1 dY / w_y(v(Y))`. Since `w_y <= w_x` at an
   `x`-split, this is at least `d(v)/(theta_root d1) >= theta0/(2 theta1 d1)`.
6. **Integrate** over `d1` from `(eps/theta0^3)^(1/2)` to `g`. □

Remarks on the proof:

- **Scope of the proof.** It uses only that the root draw has a density
  bounded below on `(a, a/(1 - g))`, so the same divergence holds for every
  clamp distribution with such a density.
- **Source of the divergence** (pointed out by the review). The divergence
  comes from `E[1/d1] = infinity`. The flip puts the kink at distance `d1`
  from a boundary with probability proportional to `d1`, and the climb that
  follows costs about `1/d1` columns. A deterministic rule has one fixed
  `d1` per kink, so it can fail only through a trap.

This bound only shows divergence. Simulations show faster growth. They
were rerun after the review with `sim2d.c` (`run_sim2d.py`, raw
`sim2d.jsonl`): `10^6` runs per entry for the randomized rules,
`eps = 1e-2 ... 1e-8`. The first version used 1,000 runs, and its `a = 1/6`
row was off by about 12% in the mean and 50% in the 99% quantile. "Keyed"
means one draw per (variable, interval).

| `a` | rule | mean `T` at `1e-4 / 1e-6 / 1e-8` (± s.e. at `1e-8`) | median at `1e-8` | 99% quantile at `1e-8` | `C_0.2` / `RC_0.2` at `1e-8` |
|---|---|---|---|---|---|
| 1/6 | `C_[0.1,0.3]` | 44.3 / 137.5 / 391.6 (± 1.0) | 21 | 3,721 | 19,537 / 17 |
| 1/6 | keyed `[0.1,0.3]` | 44.4 / 138.1 / 387.6 (± 2.0) | 21 | 12,473 | |
| 3/238 | `C_[0.1,0.3]` | 176.9 / 387.0 / 962.1 (± 0.6) | 855 | 2,747 | 183 / 183 |
| 3/238 | keyed `[0.1,0.3]` | 176.9 / 385.9 / 966.4 (± 2.9) | 213 | 17,269 | |
| 0.0102 | `C_[0.1,0.3]` | 177.8 / 455.5 / 1,212.3 (± 0.6) | 1,125 | 3,005 | 191 / 191 |
| 0.0102 | keyed `[0.1,0.3]` | 177.9 / 455.7 / 1,211.6 (± 3.3) | 251 | 18,295 | |
| 1/3 | `C_[0.05,0.35]` | 11.1 / 40.3 / 114.3 (± 0.7) | 3 | 2,679 | 3 / 3 |
| 0.25 | `C_[0.1,0.3]` | 32.9 / 104.0 / 292.1 (± 0.9) | 3 | 3,813 | 3 / 3 |

The deterministic counts are exact rationals for `C_0.2` at `a = 1/6`
(`exact2d.py`); the other deterministic entries are from `sim2d.c` in
floating point, and `RC_0.2` at 1/6 and 3/238 is confirmed exactly. The
review's independent C code gives the same numbers within the standard
errors, for example 389.8 ± 1.0 at `a = 1/6`.

**Conjecture E'.** Under widest-side selection, `E[T]` for the randomized
clamp grows like `eps^(-gamma)` with `0 < gamma < 1/2` for every kink with
`d0 < theta1`.

- Fitted slopes of `log10(mean T)` against `log10(1/eps)` between `1e-4`
  and `1e-8`, from `10^6` runs, are 0.18–0.25 (to two decimals) for 14 of
  the 15 pairs of `a` (8 values) and window (two) whose mean grows,
  independent or keyed. `a = 1/3` with `[0.1, 0.3]` never clamps.
- The exception is `a = 0.2986` with `[0.1, 0.3]`, where `d0` lies just
  below `theta1`. The mean rises from 3.2 to 55 and the slope is 0.31.
- The first version reported 0.18–0.29 from 1,000-run means.

What this means:

- **Mechanism.** Under widest-side selection a failing `x`-split is
  followed by about `1/theta` `y`-splits, each child of which retries the
  `x`-split with a fresh draw. Rare long runs of failures in one column
  then cost as much as a trap, and their probability does not fall fast
  enough to keep the mean bounded.
- **Median.** With independent draws per node, many columns retry
  independently, and the worst one dominates.
  - For kinks near the boundary the median itself grows: 5, 43, 177, 245,
    365, 555 and 855 nodes from `1e-2` to `1e-8` at `a = 3/238`, and 1,125
    at `1e-8` at `a = 0.0102`. `C_0.2` stays at 183 and 191.
  - Keyed draws make all columns with the same `x`-interval share one
    draw; the median then stays bounded (213 and 251), but the mean does
    not.
- **Keyed and independent draws have the same mean.** Along any
  root-to-leaf path every split changes the interval of the variable it
  splits. So the keys along a path are distinct, the draws along a path are
  independent under both schemes, every potential node has the same
  probability of being processed, and `E[T]` is identical. Only the
  dependence between columns changes.
  - In `sim2d.jsonl` the 102 keyed entries differ from the independent ones
    by between -2.6 and +2.7 standard errors.
- **Correction after the review.** The first version's `sim_kink.py`
  keyed on the interval `(l, u)` alone, so an `x`-split and a `y`-split on
  equal intervals shared a draw.
  - That scheme is not covered by the argument, and its mean differs:
    5.00 against 5.47 at `a = 3/238`, `eps = 1e-2` (`z = -589`), with the
    difference fading at small `eps` (`sim2d.c`, rule `kshared`).
  - `sim_kink.py` now keys on (variable, interval), and `sim_keyed.jsonl`
    was regenerated (5.45 at the same entry, 1,000 runs).
- **Deterministic recentring is bounded here** (Proposition D).

**Proposition F (incumbent rule: safety per incumbent).** Under
`INC_theta`, along every root-to-leaf path the number of splits whose
smaller child is below a `theta` fraction of its parent is at most
`sum_i N_i`, where `N_i` is the number of distinct values that coordinate
`i` of the incumbent takes during the run.

*Proof.* Only incumbent splits can be unsafe. After a split of coordinate
`i` at value `v`, `v` is an endpoint of coordinate `i` in both children and
therefore never strictly inside a later interval on the same path. □

With an optimal incumbent, `INC_theta` takes 3 nodes on both kink families
(with ties to `x` under widest-side selection; face-exact Proposition
5.4(d)). Its weakness is elsewhere: it needs a good incumbent, and it helps
only nodes that contain the incumbent.

## 6. Experiments

### 6.1 Exact-model simulations

- `chain1d.py` (logs `chain1d.log`, `chain1d_S.log`, `chain1d_A2.log`,
  `chain1d_D.log`):
  - trap points of clip schedules (Theorem A) and, after the
    review, the corrected bounds of Theorem A(ii);
  - Monte Carlo and value iteration for Theorem B, and the supersolution
    check;
  - the price-of-safety table (Proposition C);
  - the exact check `S_RC = J + 1` (Proposition D).
- `sim_kink.py` (raw `sim_kink.jsonl`) and `sim_keyed.py` (raw
  `sim_keyed.jsonl`, regenerated after the review) run exact
  branch-and-bound on both kink families. They use the closed-form node
  bounds of Section 1.1. Randomized rules get 20,000 runs per entry in 1D
  and 1,000 on the McCormick family with widest-side selection;
  deterministic rules one run.
- `sim2d.c` with `run_sim2d.py` (raw `sim2d.jsonl`, added after the review)
  runs the McCormick family with widest-side selection: `10^6` runs per
  entry for the randomized rules. It covers independent draws, draws keyed
  per (variable, interval), and the first version's shared keys.
- `exact2d.py` (log `exact2d.log`, added after the review) gives exact
  rational counts for `C_0.2` and `RC_0.2` with widest-side selection.
- `check_A2d.py` (log `check_A2d.log`) checks Theorem A(iii) with the
  width-dependent schedule `1/10 + w_x/5`.
  - At its alternating trap point, widest-side selection needs 15, 31, 135,
    267, 1,245, 2,589 and 12,003 nodes at `eps = 1e-2 ... 1e-8`, roughly
    `eps^(-1/2)`.
  - The proved bound is `0.005 eps^(-1/2)`.

The numbers are quoted in Sections 2–5.

### 6.2 SCIP setup

- **Software.** SCIP 10.0.2 (the bundled `libscip` of PySCIPOpt), SoPlex
  8.0.2, Ipopt 3.14.19, PySCIPOpt 6.2.1, Python 3.13.11. Linux 6.18 (WSL2)
  on an Intel Xeon w5-2565X with 36 logical CPUs, shared with other jobs.
  Details are in [`results/meta.json`](results/meta.json).
- **Run conditions.** Single-threaded runs, at most 6 in parallel,
  `timing/clocktype = 1` (CPU), `limits/memory = 4000` MB, and seeds as in
  the MINLPLib study. Seed 0 is SCIP's default. Seed `k` sets
  `randomization/permutationseed = k`, `permutevars = TRUE` and
  `randomseedshift = k`. The clamp draws use Python's `random.Random`,
  seeded from the run seed. Node counts are deterministic for a given seed.
- **Arm P** (`default`, `rclamp`, `c10`, `lp`, `lp_rclamp`). SCIP's own
  code throughout.
  - `rclamp` sets `branching/clamp` to a fresh `U[0.1, 0.3]` draw in a
    `NODEFOCUSED` event handler, through `SCIPsetRealParam`. Every
    `SCIPgetBranchingPoint` call at that node, both for pseudocost scoring
    and for the split, then uses the same clamp.
  - `c10` is the deterministic control with clamp 0.1, the safety level of
    the random clamp.
  - `lp` and `lp_rclamp` add `branching/midpull = 0`.
- **Arm X** (`x_*`). Sets `constraints/nonlinear/branching/external = TRUE`
  and adds a branching rule with priority `1e6` whose `branchexecext`
  handles all external candidates. Integer (LP) branching is left to SCIP.
  - PySCIPOpt 6.2.1 has no call for the external candidates, so the plugin
    calls `SCIPgetExternBranchCands`, `SCIPgetBranchingPoint` and
    `SCIPbranchVarVal` of the same `libscip` through `ctypes`.
  - Selection re-implements `scoreBranchingCandidates` and
    `selectBranchingCandidate` of `cons_nonlinear.c`, read in the 10.0.3
    source: weights violation 1, fractionality 1, pseudocost 1 and
    variable type 0.5; pseudocosts reliable after 2 observations and
    evaluated at the rule's point; a uniform random choice among candidates
    within 0.9 of the best score.
  - Differences from SCIP: the random choice uses Python's generator, and
    pseudo-solution nodes (no LP) go through this selection instead of the
    `pscost` rule.
  - Points: `x_default` and `x_rclamp` use SCIP's formula;
    `x_lp`/`x_lp_rclamp` use midpull 0; `x_recenter` uses `RC_0.2`;
    `x_inc` uses `INC_0.2`, with the incumbent inside the node box and its
    coordinate at relative distance above `1e-6` from both bounds;
    `x_noclamp` uses midpull 0 and clamp 0.
  - For `x_recenter` and `x_inc` the point is passed to
    `SCIPgetBranchingPoint` as a suggestion, so SCIP's handling of infinite
    bounds and tiny domains still applies.
- **Synthetic instances**, written as CIP.
  - `k1:a` is `min t s.t. 2|x - a| - (x - a)^2 <= t` on `x in [0,1]`. SCIP
    relaxes the concave square by its secant, so the gap is exactly
    `(x - l)(u - x)`.
    - The function differs from the model's `2|x - a|`, but the open nodes
      and relaxation minimizers are the same. On a node that straddles `a`,
      `f_B` has one-sided slopes `2 + 2a - (u + l) > 0` and
      `-2 + 2a - (u + l) < 0` at `a`, so its minimizer is `a`, with value
      `-(a - l)(u - a)`.
    - On a node with `l >= a`, `f_B` is increasing and `f_B(l) >= 0`;
      similarly on the other side. (Added after the review.)
  - `mc:a` is the McCormick kink family with `L = 2`, `c = -1` and
    `b = sqrt(2) - 1`.
  - The runs use the solver-validation note's `modelnoprop` setting:
    best-first, propagation off, heuristics off, the optimum given as the
    incumbent, `limits/absgap = eps`, `numerics/feastol = 1e-9` and
    `checkvarlocks = d`. They also set `misc/allowweakdualreds = FALSE`;
    without it, presolve's cutoff propagation solves `k1` at the root.
  - Grid: 8 kink positions, 4 tolerances, 12 settings and 5 seeds (3,840
    runs, 60 s limit).
- **MINLPLib.** The 57 instances of
  [`../minlplib-branching/selected.txt`](../minlplib-branching/selected.txt),
  12 settings, 3 seeds, 60 s (2,052 runs, 5.5 CPU hours of SCIP time).
- **Aggregation** as in the MINLPLib study (§2.4 there). Per instance, a
  shifted geometric mean over seeds (shift 10 nodes); then a shifted
  geometric mean over instances; a bootstrap 95% CI over instances; and a
  Wilcoxon signed-rank p on the per-instance log ratios.
  - A win or loss is a ratio beyond 10%. An instance is "separated" when
    all 3 seeds of one setting lie beyond all 3 of the other by more than
    10%.
  - Unsolved runs count at the limit.
  - Crashed runs have no node count. Their instance is left out of that
    pair's node comparison and counted at the time limit in the time
    comparison.

### 6.3 Synthetic kinks in SCIP

Mean nodes over 5 seeds (range when not constant). Full tables are in
[`results/summary.md`](results/summary.md), raw data in
[`results/synthetic.jsonl`](results/synthetic.jsonl). Every run ended with
gap at most `eps`. No primal or dual bound was worse than the optimum 0 by
more than `1e-9`, and the given optimum was accepted in all runs.

1D kink `k1`, `eps = 1e-8` (at `1e-4` in brackets for the first row):

| `a` | default | rclamp | lp (`C_0.2`) | lp_rclamp | x_recenter | x_inc | x_noclamp |
|---|---|---|---|---|---|---|---|
| 1/6 | 15 [9] | 16 [9] | 13 [7] | 5 (3–9) [5] | 5 [5] | 3 | 3 |
| 0.1999 | 13 | 16 | 13 | 7 (3–13) | 5 | 3 | 3 |
| 0.8252 | 13 | 16 | 7 | 5 (3–7) | 5 | 3 | 3 |
| 3/238 | 15 | 15 | 7 | 9 (7–11) | 7 | 3 | 3 |
| 0.0102 | 13 | 14 | 7 | 8 (7–11) | 7 | 3 | 3 |
| 0.25 | 15 | 16 | 3 | 4 (3–7) | 3 | 3 | 3 |
| 1/3 | 17 | 17 | 3 | 3 | 3 | 3 | 3 |

- `C_0.2` grows at its trap point 1/6: 3, 7, 9, 13 nodes. At 0.1999 it
  also grows over this range, but 0.1999 is only a near-trap point: five
  splits clamp and the sixth lands on the kink, so the 1D count saturates
  at 13, reached at `1e-8`. (The first version called 0.1999 a trap point.)
  The randomized clamp and recentring are bounded at both points.
- Near the boundary (3/238, 0.0102) the randomized clamp is slightly worse
  than `C_0.2` (8–9 against 7). The exact-model simulation of Section 3
  gives the same: a mean of 7.6 against 7.
- SCIP's default point grows for every `a`, including `a = 1/3` where no
  clamp binds (5, 9, 13, 17 nodes). The vanishing midpoint pull moves every
  split off the kink (competitive note, remark after Proposition 4'), and
  randomizing the clamp (`rclamp`) does not change this.

McCormick family `mc`, SCIP's selection (Arm P) or the plugin's (Arm X),
`eps = 1e-8`:

| `a` | default | rclamp | lp (`C_0.2`) | lp_rclamp | x_lp | x_lp_rclamp | x_recenter | x_inc | x_noclamp |
|---|---|---|---|---|---|---|---|---|---|
| 1/6 | 4,791 | 5,150 | 7,190 | 228 (3–1,091) | 9,743 | 86 (3–383) | 21 | 2,565 | 47 |
| 0.1999 | 1,587 | 6,828 | 1,197 | 231 (3–1,057) | 3,312 | 43 | 16 | 1,470 | 24 |
| 0.8252 | 5,048 | 5,141 | 60 | 68 | 56 | 51 | 17 | 34 | 99 |
| 3/238 | 6,091 | 4,847 | 26 | 128 (7–335) | 33 | 1,442 (21–5,911) | 33 | 22 | 17 |
| 0.0102 | 6,515 | 3,967 | 26 | 766 (7–3,443) | 33 | 1,164 (25–5,385) | 33 | 22 | 17 |
| 0.25 | 3,636 | 3,963 | 45 | 117 | 26 | 175 | 26 | 26 | 26 |
| 1/3 | 3,847 | 3,275 | 10 | 10 | 88 | 88 | 88 | 15 | 88 |

- **Trap point 1/6 and near-trap point 0.1999.** At 1/6, `C_0.2` grows
  roughly like `eps^(-1/2)` (61, 541 and 7,190 nodes at `1e-4, 1e-6, 1e-8`).
  At 0.1999 it has not yet saturated at `1e-8`. The randomized clamp cuts
  both by one to two orders of magnitude but still grows, with a wide spread
  across seeds. Recentring is flat: 21 nodes at 1/6 from `1e-4` to `1e-8`.
- **Near-boundary kinks** (3/238, 0.0102). The randomized clamp is much
  worse than `C_0.2`, by factors of 5 to 44 in the mean. This is the median
  growth predicted in Section 5. Recentring equals `C_0.2`.
- **Incumbent rule.** With SCIP's selection the root is often split in `y`
  first. Nodes that do not contain the incumbent then fall back to `C_0.2`
  and inherit its trap (2,565 nodes at `a = 1/6`); this is the tie-rule
  effect of the face-exact note's remark on Proposition 5.4(d). In 1D the
  rule takes 3 nodes.
- **No clamp** is harmless here (17–99 nodes). The theory's relaxation
  points are never on a bound, so the boundary adversary has no power, and
  the benefit of the clamp cannot show.
- **Default and `rclamp`** grow on every kink, again because of the pull:
  1,587–6,828 nodes at `1e-8`.

### 6.4 MINLPLib

Full tables, including per-instance node counts for every seed, are in
[`results/summary.md`](results/summary.md); raw data in
[`results/minlplib.jsonl`](results/minlplib.jsonl).

**Status.** Out of 171 runs per setting:

| Setting | default | rclamp | c10 | lp | lp_rclamp | x_default | x_rclamp | x_lp | x_lp_rclamp | x_recenter | x_inc | x_noclamp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| optimal | 168 | 170 | 166 | 163 | 165 | 168 | 163 | 164 | 163 | 162 | 162 | 129 |
| time limit | 3 | 0 | 4 | 8 | 5 | 3 | 8 | 7 | 8 | 8 | 9 | 41 |
| crash | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

- The five crashes are "error in LP solver" on wastewater05m1 and
  wastewater05m2, like the single crash of the earlier study.
- **Correctness.** No optimal run's primal value is worse than the MINLPLib
  best known by more than `4.5e-8` (relative). No dual bound exceeds it by
  more than `4.5e-8`.
- Values below the best known occur on 12 instances, in every setting:
  - within `1.4e-5` relative on 10 of them, and `5.3e-5` on hs62;
  - `4.3e-4` on hybriddynamic_varcc, the same deviation as in the earlier
    study.
- **Cross-check.** `default` and `lp` reproduce the earlier study's node
  counts exactly in every run that is optimal in both: 168 of 168 and 163
  of 163.

**Nodes** (ratio of shifted geometric means; "both solved" restricts to
instances where all six runs of the pair are optimal):

| Setting | Reference | What changes | Inst. | Ratio | 95% CI | Wilcoxon p | Wins / losses | Separated | Both solved (inst.) |
|---|---|---|---|---|---|---|---|---|---|
| rclamp | default | clamp 0.2 → `U[0.1,0.3]` (SCIP's selection and pull) | 56 | 0.963 | 0.87–1.06 | 0.58 | 11 / 10 | 0 / 0 | 1.009 (53) |
| c10 | default | clamp 0.2 → 0.1 (control) | 56 | 1.015 | 0.96–1.08 | 0.24 | 6 / 14 | 0 / 1 | 1.020 (53) |
| rclamp | c10 | clamp 0.1 → `U[0.1,0.3]` | 55 | 0.948 | 0.85–1.05 | 0.32 | 16 / 9 | 0 / 2 | 0.989 (52) |
| lp_rclamp | lp | LP point: clamp 0.2 → `U[0.1,0.3]` | 56 | 0.996 | 0.90–1.09 | 0.77 | 11 / 12 | 1 / 2 | 1.032 (50) |
| x_default | default | plugin selection vs SCIP's (reproduction check) | 57 | 1.005 | 0.84–1.13 | 0.016 | 6 / 19 | 1 / 0 | 0.994 (53) |
| x_rclamp | x_default | clamp 0.2 → `U[0.1,0.3]` | 57 | 0.996 | 0.88–1.12 | 0.91 | 12 / 10 | 0 / 0 | 0.942 (52) |
| x_lp_rclamp | x_lp | LP point: clamp 0.2 → `U[0.1,0.3]` | 57 | 1.001 | 0.93–1.07 | 0.59 | 11 / 13 | 0 / 1 | 0.989 (52) |
| x_recenter | x_lp | clip → recentring | 56 | 0.939 | 0.86–1.01 | 0.29 | 17 / 10 | 0 / 1 | 0.958 (50) |
| x_inc | x_lp | incumbent coordinate if inside | 57 | 1.047 | 0.95–1.17 | 0.74 | 8 / 9 | 0 / 1 | 1.027 (53) |
| x_noclamp | x_lp | clamp 0.2 → 0 | 56 | 1.999 | 1.43–2.96 | 3e-5 | 7 / 30 | 2 / 18 | 1.145 (40) |
| x_recenter | default | recentring (plugin) vs SCIP's default; added after the review | 56 | 0.923 | 0.71–1.14 | 0.52 | 14 / 18 | 3 / 5 | 0.855 (50) |
| x_recenter | x_default | recentring vs the plugin with SCIP's point; added after the review | 56 | 0.920 | 0.75–1.09 | 0.25 | 22 / 15 | 1 / 4 | 0.866 (49) |
| x_inc | default | incumbent rule (plugin) vs SCIP's default; added after the review | 57 | 1.032 | 0.81–1.27 | 0.14 | 14 / 21 | 4 / 4 | 0.936 (53) |

**Seed noise.** Default seed 1 against seed 0 gives 19 wins and 23 losses
beyond 10%, and seed 2 gives 19 and 20, with aggregate ratios 1.00 and
1.06. Comparisons of 3-seed means are less noisy than single seeds; the
Wilcoxon test and the bootstrap CI are the relevant yardsticks.

**Findings.**

- **Randomized clamp: neutral.**
  - All four randomized-clamp comparisons have ratios 0.96–1.00, CIs that
    contain 1, and p ≥ 0.57.
  - `rclamp` against default has no separated instance in either
    direction.
  - Against the control `c10`, which has the same worst-case safety, the
    ratio is 0.95 (0.85–1.05).
  - Times agree within 1–3%. The two LP-point pairs show time ratios 1.02
    and 1.03 with p ≈ 0.04, but their node ratios are 1.00. With 24 tests,
    this is within what chance produces.
  - Individual instances move both ways beyond seed noise under
    `lp_rclamp`:
    - prob09 gets worse: 4,335/3,030/8,348 against 1,730/1,736/1,701;
    - supplychainp1_030510 gets worse: 870/1,431/1,661 against
      425/614/757;
    - wastewater15m1 gets better: 6,729/8,843/4,233 against
      31,817/18,533/60,816.
- **Recentring: neutral, at best a small gain.**
  - Against the plugin's clip `x_lp` (same selection, midpull 0): 0.94
    (0.86–1.01), 17 wins against 10 losses. It changes the point on 9.8% of
    continuous branchings (88,273 of 901,422).
  - Against SCIP's default (different selection and midpull 0.75), added
    after the review: 0.92 (0.71–1.14), p = 0.52. The CI is twice as wide.
    - Time is 1.08 (0.96–1.22). The plugin's Python callbacks cost about
      the same (`x_default`/default time 1.075).
    - Against `x_default` (plugin with SCIP's point): 0.92 (0.75–1.09).
  - On the 12 instances where the LP value lies on a bound in at least 10%
    of `x_lp`'s continuous branchings, 0.77 (0.56–1.03, p = 0.21).
  - The randomized clamp shows a similar non-significant tendency on that
    subgroup: `rclamp`/default 0.81 (0.62–1.08).
- **Incumbent rule: neutral, and rarely active.**
  - Only 675 of about 1.03 million continuous branchings split at the
    incumbent, because the incumbent rarely lies in the node box.
  - It hurts prob09 (about 10,500 against 1,800 nodes, all seeds
    separated).
- **No clamp: harmful**, as in the earlier study. 2.00 (1.43–2.96) under the
  plugin selection, 18 of 20 separated instances are losses, and 41 runs
  hit the time limit.
  - 2.54 million of its 3.84 million continuous branchings create a child
    below 1% of its parent: Lemma 0(ii) in action.
  - The rules with a clamp never do, except for 43 incumbent splits.
- **How often the clamp matters.** Under `x_lp`, the clamp moves the split
  off the LP value in 50% of continuous branchings (488,850 of 968,098),
  and the LP value lies on a bound in 33%. These are the boundary
  relaxation points of the model. The point where such a split lands
  inside `[0.1, 0.3]` of the domain makes no aggregate difference.
- **Plugin reproduction.** `x_default` against default has aggregate ratio
  1.005 (0.84–1.13) but a systematic tilt (6 wins against 19 losses,
  p = 0.016), and time +7.5% from the Python callbacks. The plugin's
  selection is close to SCIP's but not identical. Arm X comparisons are
  therefore made within Arm X.

## 7. Interpretation

- **The question has a precise answer.**
  - (a) together with uniform competitiveness over kink positions is
    impossible for every rule, with any information (Proposition C).
  - (a) together with per-instance boundedness is possible
    deterministically, with the recentring clamp, on both kink families and
    under both selections studied.
  - It is also possible with the randomized clamp in 1D and with x-only
    selection, but not under widest-side selection (Proposition E).
- **Why SCIP's clamp traps, and what fixes it.** The trap comes from one
  design choice: the fallback split sits at the inner edge of the clamp
  zone, so the child is the whole zone. Three fixes work:
  - put the point at the child's centre when possible (recentring);
  - fall back to the midpoint (for `theta <= 1/3`), which is slower;
  - make the zone edge random.

  Recentring is the best fix in theory: it is deterministic, uses exactly
  the minimum number of splits of any safe rule in 1D, is bounded in 2D,
  and has no heavy tail.
- **Practical relevance is small on MINLPLib.**
  - None of the safe rules differs from its reference beyond seed noise.
    For the randomized clamp the 95% CIs exclude reductions above 13% and
    increases above 12%.
  - The references differ: the plugin rules (recentring, incumbent) were
    compared with the plugin's own clip. Against SCIP's default, recentring
    gives 0.92 (0.71–1.14), a CI twice as wide.
  - The theory's traps need exact kinks at special positions. MINLPLib
    instances rarely have exact kinks (the earlier study found `abs` in 2
    of 57).
  - Where the clamp binds on MINLPLib, it mostly does so because the LP
    value is on a bound (Section 6.4). There any point inside `[0.1, 0.3]`
    of the domain seems to do about as well.
- **SCIP's default point is dominated by the pull on kinks.** On the
  synthetic kinks, SCIP's default grows with `eps` at every kink position,
  including those where no clamp binds. Randomizing its clamp does not
  change this. A kink-robust SCIP rule would need midpull 0 (or a pull that
  vanishes fast) as well as a trap-free clamp. On MINLPLib, midpull 0 is
  neutral in aggregate (1.01, CI 0.81–1.21, as in the earlier study).
- **Recommendation**, conditional on the evidence here:
  - Keep a clamp. Removing it doubles node counts through boundary chains.
  - If robustness on sharp or face-aligned instances matters, replace the
    clip fallback by recentring: `split at l + max(theta w, 2(x - l))` when
    the LP value `x` is below `l + theta w`, and symmetrically above. On
    MINLPLib it is neutral in nodes both against the same-selection clip
    (0.94, CI 0.86–1.01) and against SCIP's default (0.92, CI 0.71–1.14).
    The second comparison also changes the selection and the midpoint pull.
    A native implementation inside SCIP's point formula would be the clean
    test.
  - Randomizing the clamp is harmless on MINLPLib, but it is not needed and
    has a heavy tail under widest-side-type selection.

## 8. Conjectures and open questions

- **Conjecture A'.** SCIP 10's default point (midpull 0.75 scaled by the
  relative width below 1/2, clamp 0.2) never splits at the kink for all but
  countably many positions `a`, so its count on the 1D kink is unbounded in
  `eps` for those `a`.
  - Proposition 4' of the competitive note proves unboundedness at one
    position.
  - For a fixed midpoint weight the countable-exception statement is
    Proposition 5.6(a) of the face-exact note, which leaves SCIP's
    width-dependent weight open.
  - The SCIP runs above grow at all 8 tested positions (Section 6.3).
  - **A reduction** (from the review, rederived here). At every node the
    pull `mu_B` (0.75, or `0.75 r_B` when the relative width `r_B < 1/2`) is
    positive, so the split lands on `a` iff `a` is the node's midpoint.
    - Unclamped, `mu mid + (1 - mu) a = a` iff `mid = a`.
    - Clamped at `l + 0.2 w`, equality with `a` would give `a < mid`, hence
      an unclamped point `mu mid + (1 - mu) a > a = l + 0.2 w`, so the lower
      clamp would not bind. The upper clamp is symmetric.
    - So the exceptional set is the set of kinks that are the midpoint of a
      node on their own chain.
    - Along each decision sequence the node's endpoints are explicit
      functions of `a`. The conjecture follows if `mid(a) = a` never holds
      identically along a sequence; this is not proved.
- **Conjecture E'** (Section 5): `E[T] = Theta(eps^(-gamma))` for the
  randomized clamp under widest-side selection, with `0 < gamma < 1/2`
  depending on the window and on `a`.
- **Open.**
  - Is the recentring clamp per-instance competitive on the whole 1D
    exact-gap class of Theorem 1, that is,
    `sup_eps T_RC(f, eps)/T_opt(f, eps) < infinity` for every continuous
    `f`? The kink families are the only instances analysed here.
  - The same question in `n >= 2` dimensions, where even `R_min` is not
    known to be competitive.
  - Is there a safe rule whose tree, with SCIP's lifted relaxations, stays
    close to `R_min` on instances where the LP point is informative? The
    MINLPLib data cannot separate the rules tested here.

## 9. Limitations

- **Theory.**
  - All positive results are for the two kink families: sharp minima with
    the relaxation minimizer exactly at the kink.
  - The boundary adversary is a worst-case model of SCIP's LP values on
    bounds, not a derivation from SCIP's relaxations.
  - Theorem B is for uniform draws.
  - The proofs are first-pass and unreviewed.
- **Numerics.** Floating point, apart from the 200-digit trap-point
  replay. Monte Carlo estimates of heavy-tailed means (Section 5) have
  large relative errors; the standard errors are in `sim_kink.jsonl`.
- **SCIP experiments.**
  - One solver version and one machine, shared with other jobs, so times
    are noisy; node counts are deterministic.
  - A 60 s limit, against 120 s in the earlier study.
  - The 57-instance set solves in 1–20 s under default (§2.3 of the study).
  - Arm X's selection is close to SCIP's but not identical (Section 6.4).
    Its times include Python callback overhead.
  - Only the window `[0.1, 0.3]` was tested in SCIP, with no tuning.
  - Twelve settings were compared without a multiple-comparison
    correction; the conclusions rest on CIs, not on single p-values.
  - The synthetic runs switch off propagation and cutoff reductions to
    match the model. With SCIP's defaults, cutoff propagation solves the 1D
    kink at the root.

## 10. Files and commands

All commands were run in `research-20260928b/bb-complexity/robust-branching-points/`:

```
python3 -u chain1d.py > chain1d.log            # Theorem A trap points, Theorem B, Proposition C
python3 chain1d.py S > chain1d_S.log           # supersolution check for Theorem B
python3 -u sim_kink.py sim_kink.jsonl > sim_kink.log     # exact-model B&B, both families
python3 -u sim_keyed.py sim_keyed.jsonl > sim_keyed.log  # keyed randomization
python3 check_A2d.py > check_A2d.log           # Theorem A(iii), width-dependent schedule
python3 runner.py minlplib_jobs.txt results/minlplib.jsonl --jobs 6
python3 runner.py synthetic_jobs.txt results/synthetic.jsonl --jobs 6
python3 summarize.py                           # results/summary.md
```

Revision after review (at most 4 processes at a time):

```
python3 chain1d.py A2 > chain1d_A2.log         # corrected Theorem A(ii); McCormick x-only bound
python3 chain1d.py D > chain1d_D.log           # Proposition D(i): S_RC = J + 1, exact
python3 exact2d.py > exact2d.log               # exact 2D counts: C_0.2 at 1/6 (19,537), RC_0.2
gcc -O2 -o sim2d sim2d.c -lm && python3 run_sim2d.py sim2d.jsonl > run_sim2d.log   # 10^6-run 2D table
python3 -u sim_keyed.py sim_keyed.jsonl > sim_keyed.log  # rerun with keys per (variable, interval)
python3 summarize.py                           # adds x_recenter and x_inc against default
python3 chain1d.py A3 > chain1d_A3.log         # closing audit: McCormick x-only bound at runs <= 2
```

- One SCIP run is `python3 scip_run.py INSTANCE SETTING SEED TIMELIMIT [--eps EPS]`.
- `chain1d.log` was produced before part [S] was added to `chain1d.py`; that
  part's output is `chain1d_S.log`.
- Before the batches, a few manual smoke runs checked the plugin. One found
  that `branchexeclp` must be implemented; after that fix, and after the
  selection was rewritten to follow cons_nonlinear, no plugin error
  occurred.
- `meta.json` was written by a one-off Python snippet.

| File | Content |
|---|---|
| [`scip_run.py`](scip_run.py) | one SCIP run: settings of both arms, the clamp-redraw event handler, the point-rule branching plugin (ctypes access to `libscip`), synthetic CIP instances |
| [`runner.py`](runner.py) | parallel runner (at most 6), resumable, appends JSONL |
| [`minlplib_jobs.txt`](minlplib_jobs.txt), [`synthetic_jobs.txt`](synthetic_jobs.txt) | job lists |
| [`results/minlplib.jsonl`](results/minlplib.jsonl) | 2,052 MINLPLib runs (raw) |
| [`results/synthetic.jsonl`](results/synthetic.jsonl) | 3,840 synthetic runs (raw) |
| [`results/summary.md`](results/summary.md) | all tables, including per-instance counts per seed |
| [`results/meta.json`](results/meta.json) | versions, default parameters, run conditions |
| [`summarize.py`](summarize.py) | aggregation, reusing the MINLPLib study's helpers |
| [`chain1d.py`](chain1d.py), [`chain1d.log`](chain1d.log), [`chain1d_S.log`](chain1d_S.log) | 1D chain checks |
| [`sim_kink.py`](sim_kink.py), [`sim_kink.jsonl`](sim_kink.jsonl), [`sim_keyed.py`](sim_keyed.py), [`sim_keyed.jsonl`](sim_keyed.jsonl) | exact-model simulations (raw) |
| [`check_A2d.py`](check_A2d.py), [`check_A2d.log`](check_A2d.log) | Theorem A(iii) check |
| [`chain1d_A2.log`](chain1d_A2.log), [`chain1d_A3.log`](chain1d_A3.log), [`chain1d_D.log`](chain1d_D.log) | revision checks of Theorem A(ii) and Proposition D |
| [`sim2d.c`](sim2d.c), [`run_sim2d.py`](run_sim2d.py), [`sim2d.jsonl`](sim2d.jsonl) | `10^6`-run McCormick simulations (raw; the `sim2d` binary is not kept) |
| [`exact2d.py`](exact2d.py), [`exact2d.log`](exact2d.log) | exact rational 2D counts for the deterministic rules |

**Checks run.** Only the targeted scripts above, plus smoke runs of the
plugin. No project-wide checks were run and no CI results are involved.
Nothing was committed.

## 11. Revision after review (2026-09-29)

The review
[`../../reviews/robust-branching-review.md`](../../reviews/robust-branching-review.md)
(scripts in [`../../reviews/robust-branching/`](../../reviews/robust-branching/))
confirmed every numbered result except one parenthetical. Each change below
was rederived here and, where computational, rechecked with this note's own
code (commands in Section 10).

1. **Theorem A(ii).** The parenthetical "(in fact uncountably many)" with the
   stated `K` was false.
   - For the fixed clamp 1/5, a run of length 2 gives
     `rho(1 - rho) < theta^2 < theta0/4`, and only `a = 1/6, 5/6` satisfy
     the bound.
   - The statement now names the two alternating points. It adds the
     uncountable family with runs of length at most 2 under the constant
     `theta0^2/4`, from the general bound `rho_k > theta0^r/2` in proof
     step 4.
   - `chain1d_A2.log` shows the violations of the old constant (from
     `eps = 0.049, 0.002, 3.2e-6, 5.0e-9`) and that the new bound holds.
2. **Theorem A, proof step 5.** The McCormick x-only bound is
   `|c| rho(1 - rho) w_k`, not `... w_k^2`. The statement stands. The
   sharper `K' = ceil(log(|c| theta0/(4 eps))/log(1/theta0))`, about twice
   `K`, is stated and checked (45 nodes against `2K' + 1 = 45` at `1e-16`).
   It holds at the two alternating points only; see item 10.
3. **Summary wording of Theorem A.** The class is clip schedules, whose
   fallback is the zone's inner end. It is not every rule that ignores the
   point's position inside the zone: the midpoint fallback ignores it and
   never traps for `theta <= 1/3` (short proof added in Section 2). The
   `eps^(-1/2)` claim now carries the hypotheses of (iii).
4. **Proposition D(i), strengthened.** `RC_theta` uses exactly `J + 1`
   splits, meeting Proposition C's bound, so it is split-optimal among
   `theta`-safe rules for `theta <= 1/3`. The first version had `J + 2`.
   - The proof is the review's three-case argument, rederived in
     Section 5.
   - It was checked exactly on 15,450 kinks (`chain1d_D.log`).
   - The Summary and Sections 4 and 7 were updated.
5. **Theorem B remarks.** The second bound (12.5 and 18.1 at `a = 1e-4`
   and `1e-8`) is now quoted where it is smaller than the first (16.2 and
   29.3).
6. **Numbers.**
   - `C_0.2` at `a = 1/6`, `eps = 1e-8`, widest side, is 19,537 in exact
     arithmetic; 19,541 was a floating-point tie artifact (`exact2d.log`).
   - The Section 5 table was recomputed with `10^6` runs per entry
     (`sim2d.jsonl`): at `a = 1/6` the mean is 391.6 ± 1.0 (was 435) and
     the 99% quantile 3,721 (was 5,663).
   - The Conjecture E' slopes are 0.18–0.25, with one stated exception
     (0.31 at `a = 0.2986`, where `d0` is just below `theta1`).
   - 0.1999 is a near-trap point, not a trap point.
   - SCIP's default at `1e-8` ranges over 1,587–6,828 nodes with `rclamp`
     included.
   - The smallest p among the randomized-clamp pairs is 0.576.
7. **Keyed randomization.** The first `sim_kink.py` keyed on `(l, u)`, so
   x- and y-splits on equal intervals shared a draw.
   - The equal-mean argument covers keys per (variable, interval). The code
     now uses that scheme.
   - `sim_keyed.jsonl` was regenerated, and `sim2d.jsonl` compares all
     three schemes: keyed and independent agree within ±2.7 standard errors
     on 102 entries, while the shared scheme differs (5.00 against 5.47 at
     `a = 3/238`, `eps = 1e-2`).
8. **Reference for recentring.** "0.94 (0.86–1.01)" is against the plugin's
   clip `x_lp` (midpull 0).
   - Against SCIP's default, recentring gives 0.92 (0.71–1.14), p = 0.52,
     and against `x_default` 0.92 (0.75–1.09).
   - The Summary, Section 6.4 and Section 7 now say so, and `summarize.py`
     reports these pairs.
9. **Smaller additions.**
   - The `k1` instance's function differs from the model's; a derivation
     shows it has the same open nodes and minimizers (Section 6.2).
   - The review's reduction of Conjecture A' (split at `a` iff `a` is the
     node midpoint) is rederived in Section 8.
   - A remark on the source of Proposition E's divergence was added.
   - "17 nodes for every `eps`" became "at most 17". Exact counts give 17
     for `eps <= 0.02` (the review quoted 0.0123 as the threshold; this
     note's recheck with `exact2d.py` puts the change at about 0.021).

Not changed: the SCIP runs (the review recomputed the MINLPLib ratios and
found agreement), Theorems A(i), A(iii) and B, Propositions C, E and F, and
Lemma 0.

### 11.1 Closing audit (2026-09-29)

The closing audit
[`../../reviews/closing-audit-a.md`](../../reviews/closing-audit-a.md)
(item 3; scripts in [`../../reviews/closing-audit-a/`](../../reviews/closing-audit-a/))
confirmed the 1D bounds of Theorem A(ii), the midpoint-fallback result and
`S = J + 1` in Proposition D(i). Changes:

10. **Scope of `K'` in Theorem A(ii)** (statement level). The McCormick
    x-only bound `T >= 2K' + 1` holds at the two alternating points only.
    - At points whose runs have length at most 2, the lower bound
      `rho(1 - rho) >= theta0^2/4` replaces `K'` by `K' - 1`. So the correct
      bound there is `T >= 2K' - 1`.
    - Counterexample to the wider reading: fixed clamp 1/5, `a = 1/30`,
      `|c| = 1`, `eps = 1/25`, where `T = 1 < 3 = 2K' + 1`.
    - The statement and proof step 5 now say this.
    - Recheck: `chain1d.py A3` (log `chain1d_A3.log`) reproduces the
      counterexample. On 20 random itineraries with runs of length at most
      2 per schedule, `T < 2K' + 1` occurs in 37 and 3 of 480 cases (fixed
      and position-dependent schedules) and `T < 2K' - 1` never.
11. **Midpoint fallback wording.** "Moves to `2d`, on the same side" was
    loose when `d > 1/4`. The remark now measures the position from the
    starting end. It adds the sharpness of `theta <= 1/3`: for
    `theta > 1/3`, `a = 1/3` traps.
12. **Proposition D(i) proof.** It now uses the audit's direct argument for
    `J <= m + 1` in the second case (`d0 >= theta^(m+1)/2 >= theta^(m+2)`).
    Proposition C is cited only for optimality.

The audit's other items concern other notes. This closes the note.
