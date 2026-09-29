# Review: hard side, Section 5 and Section 1 lemmas of the sparse-regression phase-transition note

Reviewed file: [`../bb-complexity/sparse-regression/phase-transition.md`](../bb-complexity/sparse-regression/phase-transition.md)
(version of 2026-09-29 01:03). Scope: Section 4 (hard side), Section 5, the
Section 1 lemmas used there (Lemmas 1.3, 1.4, 1.5), the labels of Heuristic
3.8 and Conjecture 5.2, and the hard-side computations of Sections 6.4–6.5 as
evidence. Sections 2–3 are reviewed separately. Reviewer: independent research
agent (probability, random matrices, statistical physics of inference); I did
not write the note. Date: 2026-09-29. My scripts and logs are in
[`sparse-hard/`](sparse-hard/). I did not reuse the author's code, except to
read it and to replicate its instance generator for a direct comparison.

## Verdict

Theorems 4.3 and 4.4 are correct as asymptotic statements. I checked every
step and found no counterexample and no hidden gap. The points the brief asked
about (dependence between `OPT` and the chosen supports, randomness of `OPT`,
uniformity over supports, the use of `lam = o(n)`) are all handled correctly.
Lemmas 1.3, 1.4 (with the node form) and 1.5 are correct. The finite-`p`
vacuity claim holds in substance. Several side sentences are wrong or too
strong, and Conjecture 5.2 is under-specified. Its "what is missing" paragraph
also understates how far the conjecture is from the proved results. The proof
actually gives a stronger clique bound than stated (item S1).

| Claim | Verdict | Notes |
|---|---|---|
| Lemma 1.5 (midpoint formula), (a), (b), conflict inequality | **correct** | Checked by hand, by a second derivation (two-copy identity, Section 1.1 below), and numerically (399 random instances, max relative error `1.3e-13` using the `n`-side formula). |
| Lemma 1.4 (conflict bound) and its node form `omega/(2p+1)` | **correct** | The node form follows from the review's reduction argument. For binary fixings the factor `p+1` suffices, so `2p+1` is safe. The node form is informative only when `ck > log(2p+1)`. |
| Lemma 1.3 (removal half gives a `2k+1`-node certificate) | **correct** | Consistency check: in 50 exact instances where the removal half was certified, the exact clique number never exceeded `k+1`. |
| Lemma 4.1 (Beta Chernoff, first-moment bound on `OPT`) | **correct** | Chernoff algebra checked; the bound dominates the exact Beta tail on a wide grid (max log ratio `-0.69`). Part (b)'s decoupling (`v_T` independent of `X_T`) is right. |
| Lemma 4.2 | **correct** | Deterministic; the independence hypothesis is not needed for the inequality itself. Checked numerically. |
| Theorem 4.3 (pure noise, `x < x0`, `lam = o(n)`) | **correct (asymptotic)** | Every step checks. One wording error in Step 6. The proof gives more than `exp(ck)` (S1). |
| Theorem 4.4 (planted, total SNR below `e^{-x}(1+2x) - 1`) | **correct (asymptotic)** | The sentence about the "detection scale" is false for `gamma < 1/2` and large `alpha` (C1). The region lies strictly inside `n < n_IT`. |
| `x0 = 1.2564...`, `2/x0 = 1.5918`, max `0.2131` at `x = 1/2` | **correct** | `x0 = 1.2564312086`. |
| `k = p^gamma`, `n = alpha k log p` ⇒ `alpha > 1.59(1-gamma)` | **correct** | Also needs `lam = o(n)`. |
| Section 4.4: finite-`p` conditions vacuous; first nontrivial at `p = 10^12` | **correct on the stated grid; grid-specific** | I reproduce the grid result (my best `log|C'|` is 28 and 131 at `alpha = 8, 16`; the note has ≈30 and 88, and the difference comes from the optimization grid over `R`). On a wider grid the first certified conflict appears at `p ≈ 10^6` and a clique `>= e^10` at `p = 10^9`, but only with `n` in the millions (C4). The shortfall formula omits `log(4 pi)` (C3). |
| Section 5 regime list | **mostly correct; one overstatement** | The pure-noise bullet omits `x < x0` and `lam = o(n)`, and it sits under "Fix the SNR `b/sigma`", although Theorem 4.4 requires bounded *total* SNR (C2). |
| Section 5 heuristic, Question 5.1 | **labeled correctly** | The constant `0.6 sqrt n` and the idealized decision-tree model are not derived (C7). |
| Conjecture 5.2 | **labeled correctly, but under-specified and farther from reach than stated** | It does not specify `lam`, `eps` or a lower limit on `n`. At fixed SNR, `n <= n_IT` means `x >= log(1 + k b^2/sigma^2) -> inf`, and for `k = p^gamma`, `k/n_IT -> gamma/(2(1-gamma)) > 0`. This is outside both `q -> 0` and `x < x0`, where even pure noise is open (C5). |
| Heuristic 3.8 | **labeled correctly** | "(finite-size balance; not proved)"; consistent in Sections 6.7 and 8. |
| Section 6.5 as evidence for Conjecture 5.2 | **mislabeled regime** | 8 of the 12 rows are at or above the first-order `n_IT` (ratios 0.92–1.71). They lie below the *empirical* recovery threshold, not below `n_IT` (C6). |

## 1. Section 1 lemmas

### 1.1 Lemma 1.5 (midpoint formula)

At `z = (1_S + 1_T)/2`, `z = 1` on `C = S ∩ T`, `z = 1/2` on `D = S Δ T`, and
0 elsewhere. By (F2) the penalty is `lam sum beta_i^2/z_i = lam ||beta_C||^2 + 2 lam ||beta_D||^2`.
This is the formula. Parts (a) and (b) follow as written. In (b), the
parallelogram step is
`||(r_S + r_T)/2||^2 = (||r_S||^2 + ||r_T||^2)/2 - ||r_S - r_T||^2/4` with
`r_S - r_T = X(beta^T - beta^S)`. The penalty bookkeeping on `C`, `S \ T` and
`T \ S` checks. Multiplying (b) by 4 gives the stated conflict inequality.

A second derivation, which I used for all computations:
`X diag(z) X' = (X_S X_S' + X_T X_T')/2 = Z Z'/2` with `Z = [X_S, X_T]`, so by
the push-through identity

```
g((1_S+1_T)/2) = y'(I + Z Z'/(2 lam))^{-1} y = min_{b1, b2} ||y - X_S b1 - X_T b2||^2 + 2 lam (||b1||^2 + ||b2||^2).
```

A shared feature appears twice with penalty `2 lam` each. Splitting a
coefficient optimally between the two copies gives effective penalty `lam`,
which recovers Lemma 1.5. This form could replace the proof in the note: it
is shorter and makes (a) evident.

Numerics (`check_midpoint.py`, 399 random instances, `n`-side formula, `lam`
from `1e-2` to `1e2`, planted and unplanted `y`, overlapping and disjoint
supports):

- formula: max relative error `1.3e-13`;
- (a) is never violated, and equality holds for disjoint supports (`4.7e-14`);
- (b) is never violated;
- the conflict-inequality equivalence has no mismatches;
- Lemma 4.2 is never violated.

### 1.2 Lemma 1.4 and the node form

The leaf form is correct. By induction every feasible 0/1 point lies in a
leaf. The midpoint of two points in one leaf lies in `Q_v ∩ K`, because both
sets are convex and `sum(mid) = (|S| + |T|)/2 <= k`. The node form needs each
reduction's removed part to contain its binary points inside a convex piece
with bound `>= OPT - eps`. For a fixing `z_i := 1`, the piece is
`Q_v ∩ {z_i = 0}`, not the removed interval `[0,1)`, whose fractional points
may have low `g`. With that reading, each node contributes at most `p` virtual
leaves (each binary variable is fixed at most once), so `p+1` suffices and
`2p+1` is safe. Two remarks for the text:

- The node bound `exp(ck)/(2p+1)` says something only when `ck > log(2p+1)`.
  This holds for `k = p^gamma`, but not for `k = O(log p)`.
- The bound also holds when node bounds are computed lower bounds (for
  example the dual bound of Lemma 1.1) rather than exact values, since weaker
  bounds only make pruning harder. It also holds for any relaxation that is
  pointwise below `g` on `K`. Adding big-M constraints `|beta_i| <= M z_i`
  changes the relaxation and is not covered.

### 1.3 Lemma 1.3

This is correct. The final node `z = 1_{S°}` has value `OPT`, and each
`z_i = 0` child has bound `>= r({i},∅)` by monotonicity. That gives
`1 + 2k` nodes and `k+1` leaves, so every clique has size at most `k+1`. My
exact computations are consistent with this (Section 5, E2): in all 50
instances with a certified removal half at the optimal support, the exact
clique number over all supports was `<= k+1`.

## 2. Lemmas 4.1 and 4.2

**Lemma 4.1(a).** For fixed `T`, `||P_T yhat||^2 ~ Beta(k/2, (n-k)/2) = A/(A+C)`.
The exponential-moment bound
`(1 - 2theta(1-rho))^{-k/2}(1 + 2theta rho)^{-(n-k)/2}` at
`2theta(1-rho) = 1 - q/rho` gives `1 - 2theta(1-rho) = q/rho` and
`1 + 2theta rho = (1-q)/(1-rho)`. Hence the bound equals
`exp(-(n/2) d(q||rho))`, as claimed. This needs `rho > q`. The union bound over
`C(p,k)` supports and monotonicity of `f` in the support give the claim.
Numerically (`check_constants.py`), for `n` up to 3000 and `k` up to 100, with
`rho` both near `q` and near 1, the exact Beta tail never exceeds the bound
(max `log(exact) - log(bound) = -0.69`).

**Lemma 4.1(b).** `v_T = X_A beta*_A + sigma w` with `A = S* \ T` is
independent of `X_T`, and `y - v_T` lies in the span of `X_T`. The union bound
needs only the marginal law of each event, not independence across `T`. Then
`||v_T|| >= sigma ||P_{S*}^perp w||`. This is correct. It is the same device
as Gamarnik–Zadik's reduction of the planted problem to the pure-noise
problem by conditioning on the overlap with the support (arXiv 1701.04455,
Section 4), here for least-squares fits instead of binary coefficients.

**Lemma 4.2.** The inequality is deterministic. It uses
`y'X_U c_U = ||y|| s_U` and `||X_U c_U||^2 = s_U^2 + ||X_U^perp c_U||^2`, then
optimizes over `t`. The hypothesis "`y` independent of `X_N`" is needed only
later (Step 5), not for the lemma. This is cosmetic.

## 3. Theorems 4.3 and 4.4

### 3.1 Step-by-step check of Theorem 4.3

- **Step 1.** `d(q||rho) = -log(1-rho) + O(q log(1/q))` uniformly on compacts,
  and `(2/n) log k -> 0`. Hence `-log(1-rho*) -> x`, because `d(q||.)` is
  increasing on `(q,1)` and the limit is strictly increasing. This is correct.
  Convergence is very slow: at `x = 0.8`, `-log(1-rho*) = 1.07` at
  `p = 10^4`, 0.93 at `10^9`, 0.84 at `10^30` and 0.82 at `10^60`
  (`check_constants.log`).
- **Step 2.** At `mu = 1`, the condition `2x/(1+2x) > 1 - e^{-x}` is
  equivalent to `e^{-x}(1+2x) > 1`, which holds for `x < x0`. Continuity gives
  `mu < 1`. The requirement `R > 1/(1-mu)` gives `mu < (R-1)/R`. Correct.
- **Step 3.** The count of `|c_j| >= t_M` is `Bin(p, 2M/p)` with mean `2M`, and
  the multiplicative Chernoff bound gives `e^{-M/4}`. The bounds
  `log C(p,k) ∈ [k log(p/k), k log(ep/k)]` and `x > 0` fixed force
  `log(p/k) -> inf`, so `t_M^2 = 2 log(p/k)(1+o(1)) = (xn/k)(1+o(1))`. Correct.
  The `o(1)` is of order `log log(p/k)/log(p/k)`.
- **Step 4.** The GV count, the entropy bound, `phi_R' = log((1-nu)(R-1-nu)/nu^2)`
  (positive iff `nu < (R-1)/R`) and `phi_R((R-1)/R) = R H(1/R)` all check.
- **Step 5.** `c_j = x_j'yhat` and `(I - yhat yhat')x_j` are independent
  Gaussians. `W` and `C'` are measurable with respect to `(y, c)`, so
  conditionally on `(y, c)` each `||X_U^perp c_U||^2/s_U ~ chi^2_{n-1}`, and
  the union bound over the `|C'|^2` pairs is legitimate. `t = O(k) = o(n)`.
  Correct.
- **Step 6.** Correct, with one wording error: "the bound of Lemma 4.2
  increases in `s_U`" should read "decreases in `s_U`" (the fraction
  `s_U/(s_U + ...)` increases). The failure probability
  `2 delta + e^{-M/4} + o(1)` is right.

**The points the brief asked about.**

- *Dependence between `OPT` and the family.* There is none to worry about. The
  bound on `OPT` holds simultaneously for all `C(p,k)` supports, and the clique
  event is a separate high-probability event. The conflict graph is defined
  relative to the true, random `OPT`, and the proof only uses a uniform lower
  bound on it. The two events are intersected.
- *"Near-optimal" supports.* The proof never needs the clique members to be
  near-optimal. A top-`k` subset of `W` explains about `x/(1+x)` of
  `||y||^2`, which is less than `1 - e^{-x}`. Only the unions `U = S ∪ T`,
  weighted `1/2`, undercut `OPT`, through Lemma 1.5(a). This is the right
  mechanism for the perspective relaxation.
- *Uniformity.* The lower bound on `s_U` is deterministic on the Step 3
  event, and the chi-square bound is uniform over pairs by the union bound.
- *`lam = o(n)`.* This is used only in Step 6, next to `n` in the denominator.
  Two remarks. (i) The theorem says `lam >= 0`, but Section 1.1 needs
  `lam > 0` (`M_z` is undefined at `lam = 0`), so write `lam > 0`. (ii) For
  `lam = c n` the same proof gives the condition
  `(1+mu)x/((1+mu)x + 1 + 2c) > 1 - e^{-x}`. This is a free generalization,
  although the ridge penalty then also raises `OPT`.

### 3.2 Theorem 4.4

Conditioning on `(X_{S*}, w)` makes `y` fixed and `X_N` independent of it. The
bound on `OPT` comes from Lemma 4.1(b) together with
`||P^perp_{S*} w||^2 = n(1+o(1))`, and `||y||^2 = n(sigma^2 + ||beta*||^2)(1+o(1))`.
The resulting condition `1 + kappa_s < e^{-x}(1 + (1+mu)x)` is correct, and
some `mu < 1` works by strict inequality. The derived constants check:
`K(x) := e^{-x}(1+2x) - 1` is positive exactly on `(0, x0)`, with maximum
`2e^{-1/2} - 1 = 0.2131` at `x = 1/2`.

**C1 (false sentence).** "The per-coefficient signal is below the detection
scale `sigma sqrt(log p/n)` by a constant factor." The theorem gives
`b / (sigma sqrt(log p/n)) < sqrt(alpha K(x))` with `x = 2(1-gamma)/alpha`.
This factor tends to `sqrt(2(1-gamma))` as `alpha -> inf`, so it exceeds 1
whenever `gamma < 1/2`. For example, with `gamma = 0` and `alpha = 100` it is
1.39 (`check_constants.log`). A correct statement:
`b < sigma sqrt(2 log(p/k)/n) · sqrt(K(x)/x)`, and `K(x)/x < 1`. Equivalently,
`log(1 + kappa_s) < log(1+2x) - x < x`, so the Theorem 4.4 region lies
strictly inside the sub-information-theoretic region `n < n_IT`
(`x > log(1 + kappa_s)`). The ratio `K(x)/(e^x - 1)` is 0.82, 0.33, 0.06 and
0.01 at `x = 0.1, 0.5, 1.0, 1.2`, so the theorem covers only part of that
region. It is worth saying this explicitly: the theorem is a statement about
a regime where recovery is impossible.

### 3.3 S1: the proof gives cliques of size `C(p,k)^{c'}` (strengthening; my sketch, not reviewed)

The GV exponent `e(mu, R) = R H(1/R) - phi_R(mu)` grows like
`(1-mu) log R + O(1)` as `R -> inf`. For example, at `mu = 0.5` it is 0.09,
0.63, 1.76 and 2.91 at `R = 3, 10, 100, 1000` (`check_constants.log`). For
fixed `R`, Step 3 is unaffected asymptotically, so `c(x)` in Theorem 4.3 can
be taken arbitrarily large.

Going further, take `R = (p/k)^theta`. Then:

- `t_M^2 = 2(1-theta) log(p/k)(1+o(1))`;
- `log|C| >= (1-mu) theta k log(p/k)(1-o(1))`;
- Step 5 with `log|C'| = c' k log(p/k)` gives
  `nu^2 <= n(1 + 2 sqrt(c'x) + 2c'x)(1+o(1))`;
- Step 6 needs `(1+mu)(1-theta)x / (1 + 2 sqrt(c'x) + 2c'x) > e^x - 1`.

Because `2x > e^x - 1` on `(0, x0)`, the last condition holds for `mu` near 1
and small `theta` and `c'`. So w.h.p. the clique number is at least
`exp(c' k log(p/k)) = C(p,k)^{c'(1+o(1))}` for some `c' = c'(x) > 0`. In
words, perspective B&B in this regime is no better than brute-force
enumeration raised to a constant power. The note may want this form, after
checking it.

## 4. Section 4.4: finite-`p` vacuity

I re-implemented the finite-`p` condition independently (`finite_p.py`). The
condition is
`(k+m) t_M^2/((k+m) t_M^2 + nu^2 + 2 lam) > rho*`, with the note's `nu^2` and
`t`, and `log|C'|` at most the GV bound. For each configuration I report the
largest admissible `L = log|C'|`.

- **The note's grid** (`lam = sqrt(n log p)`, `delta = 0.05`): the condition
  fails at every point with `p <= 10^8`. At `p = 10^12` it holds for
  `alpha = 8` (`L = 28.0`) and `alpha = 16` (`L = 131`). The note reports ≈30
  and 88; my `R` grid (up to 64, best `R = 16`) explains the difference. The
  claim is confirmed.
- **C4 (wider grid, grid-specific wording).** Allowing any `k` and `alpha` up
  to 4096 (`finite_p_wide.log`, `finite_p_wide2.log`):

  | Threshold | `lam = 0` | `lam = sqrt(n log p)` |
  |---|---|---|
  | first certified conflicting pair | `p = 10^6` (`k = 3`, `alpha = 512`, `n ≈ 2·10^4`) | `p ≈ 3·10^7` (`k = 9`, `alpha = 128`, `n ≈ 2·10^4`)* |
  | clique `> k+1` | `p = 10^7` (`k = 3`, `alpha = 512`) | not searched |
  | clique `>= e^10` | in `(10^8.5, 10^9]`; at `10^9`: `k = 133`, `n ≈ 1.1·10^7` | `<= 10^9`; at `10^9`: `k = 47`, `n ≈ 4·10^6`** |

  The `p` grid has half-decade steps.
  (*) From `finite_p.log`, whose grid has `alpha <= 128`; the wider-`alpha`
  search was run only for `lam = 0`.
  (**) Only `p ∈ {10^9, 10^10, 10^12}` were evaluated for this entry.

  So the proof is vacuous at practical sizes, as the note says. But "first
  gives a nontrivial clique at `p = 10^12`" is true only for `alpha <= 16`.
  Suggested wording: "on this grid ...; allowing `alpha` up to 4096, the
  condition first certifies a clique `>= e^10` at `p = 10^9`, with `n` in the
  millions".
- **Where the loss is.** At small sizes the true `OPT` is far above the
  union-bound value (`construction_small.log`, exact `OPT` by enumeration). For
  `p = 200`, `k = 3`, `alpha = 4`: `OPT/||y||^2 = 0.695`, `e^{-x} = 0.644`,
  and the rigorous `1 - rho*` is only 0.484.
- **C3.** "`t_M^2` falls short of `2 log(ep/k)` by about
  `log log(p/M) + 2 + 2 log R`" omits `log(4 pi) ≈ 2.53`. At
  `(p, k, R) = (10^12, 1000, 16)` the actual shortfall is 12.86; the note's
  formula gives 10.43, and adding `log(4 pi)` gives 12.96.
- The sentence "In pure noise ... every support explains about `x ||y||^2`"
  should read "the best supports explain about `(1 - e^{-x}) ||y||^2`, which is
  about `x ||y||^2` for small `x`".

## 5. Own simulations (exact cliques over all supports)

All cliques below are exact maximum cliques of the conflict graph
`g(mid) < OPT(1 - 1e-10)`. `OPT` comes from full enumeration and midpoints
from the two-copy identity (`cliquelib.py`, `exact_clique.py`). The
maximum-clique solver is a bitset branch and bound checked against brute
force on 200 random graphs.

**E1: the note's Table 6.4 instances** (`p = 30`, `k = 3`, seeds 3000–3003,
the same generator and ridge rule, `alpha ∈ {1, 2, 4}`, `b ∈ {0, 1}`; 24
instances). My `OPT` agrees with the author's B&B `OPT` in 24/24. The exact
clique number over all 4060 supports equals the author's greedy
pool-of-300 clique in 24/24, and it never exceeds the author's node count.
The Table 6.4 entries for `k = 3` are therefore exact maxima.

**E2: own seeds** (10 per cell; `lam = 0.75 sqrt(2 n log p)`; `b = 0` is pure
noise, `b = 1` is planted with `sigma = 0.5`):

| `(p, k)` | `alpha` | pure noise: `omega` median [range] | planted: `omega` median [range] | planted: C1 at `S°` |
|---|---:|---|---|---:|
| (30, 3) | 1 | 3 [2, 10] | 3 [2, 5] | 3/10 |
| (30, 3) | 2 | 6 [2, 10] | 1.5 [1, 4] | 6/10 |
| (30, 3) | 4 | 6.5 [4, 19] | 1 [1, 1] | 10/10 |
| (20, 4) | 1 | 4 [1, 11] | 3 [1, 7] | 2/10 |
| (20, 4) | 2 | 5.5 [3, 8] | 1.5 [1, 2] | 8/10 |
| (20, 4) | 4 | 8 [4, 20] | 1 [1, 1] | 10/10 |

- In pure noise at `alpha = 2, 4` the removal half failed in 37 of 40 runs.
- Restricting the clique search to the 300 best supports lost nothing in all
  60 pure-noise runs (`pool300.log`). The largest cliques often use features
  ranked beyond the top `3k` by `|x_j'y|`: per cell, the median of the worst
  rank used is 10.5–12, and the maximum is 18–23 (out of `p = 20` or 30). The
  top-correlation restriction is a proof device, not where the largest
  cliques sit at these sizes.
- At `alpha = 1`, `lam/n ≈ 0.6`, far from `lam = o(n)`. This matches the weak
  cliques there, and it is a reason not to read `alpha = 1` data as evidence
  about `x > x0`.

**E3: total-SNR scan for Theorem 4.4** (`p = 30`, `k = 3`, `n = 41`,
`x = 0.405`, `lam = sqrt n`; the same `X` and `w` for every `kappa_s`; 10
seeds). The theorem's sufficient threshold is `K(x) = 0.207`, and the
first-order IT threshold is `e^x - 1 = 0.50`.

| `kappa_s` | 0 | 0.05 | 0.1 | 0.2 | 0.4 | 0.8 | 1.6 | 3.2 | 6.4 |
|---|---|---|---|---|---|---|---|---|---|
| median `omega` | 9 | 9 | 10.5 | 9.5 | 8 | 5 | 4 | 2 | 1 |
| `S*` optimal | 0/10 | 0 | 0 | 0 | 0 | 4 | 7 | 10 | 10 |

Cliques stay at the pure-noise level up to `kappa_s ≈ 0.4` and decay once
`S*` becomes optimal. This is consistent with the theorem being a
conservative sufficient condition.

**Theorem 4.3 construction at small sizes** (`construction_small.log`; pure
noise, `lam = sqrt n`, `W` = the top `3k` features, exact `OPT`). The
fraction of disjoint code pairs that conflict rises with `alpha` (smaller
`x`), as the proof suggests:

- `p = 200`, `k = 3`: 0.49, 0.83 and 1.00 at `alpha = 2, 4, 8`.
- `p = 60`, `k = 3`: 0.31, 0.68 and 0.86.
- The exact clique inside `W` has median 19 (max 55) at `p = 200`, `k = 3`,
  `alpha = 8`.

## 6. Section 5 and Conjecture 5.2

- **C2.** The fourth bullet ("Pure noise, or total SNR below ...: every
  convex-piece tree needs `exp(Omega(k))` leaves") omits the hypotheses
  `x < x0` (that is, `alpha > 1.59(1-gamma)`), `lam = o(n)` and
  `k/n -> 0`. It also sits under "Fix the SNR `b/sigma`". At fixed `b/sigma`,
  the total SNR `k b^2/sigma^2 -> inf`, so Theorem 4.4 never applies. The
  bullet should say that it concerns a different scaling (bounded total SNR,
  per-coefficient SNR `-> 0`).
- **Scale of the windows.** At fixed `b/sigma` and `k = p^gamma`,
  `n_IT/(k log p) ≈ 2(1-gamma)/(gamma log p) -> 0`. In the `alpha`
  parametrization the conjectured hard regime therefore shrinks to `alpha -> 0`,
  and almost all of `(0, 2 - gamma)` falls under Question 5.1. The note should
  say so, because "between the thresholds" reads like a bounded window.
- **"Where the empirical transition sits."** This paragraph reads the scout's
  `lam = sqrt n` runs through "a rule-independent [transition] at the C1
  threshold `2k log(p/sqrt n)`". By Corollary 3.4, with `lam = sqrt n` there
  is no such threshold asymptotically; it exists only for a tuned ridge.
  Qualify accordingly.
- **Lemma 1.3 as the explanation** for the absence of lower bounds below
  `2 - gamma`: correct as a conditional statement.
- **C7.** The heuristic paragraph is labeled "not proved", which is
  appropriate. The constant "`lam` well above `0.6 sqrt n`" has no derivation
  anywhere, and the "idealized model" behind "at least `2^{K/2}` leaves" is not
  specified (it does not say when a node with many zero-fixings becomes
  prunable). Either give the model and its derivation, or drop the numbers.
- **C5 (Conjecture 5.2).** The label is right, but the statement and the
  "what is missing" paragraph need work:
  1. *Under-specified.* The statement names no `lam` range (the proved results
     need `lam = o(n)`), no `eps` (the result depends on it; the theorems use
     `eps <= eta · (scale)`), and no lower limit on `n`. For `gamma > 2/3`,
     `n_IT ≈ 2(1-gamma)k/gamma < k`, so the conjecture includes `n < k`,
     where every `k`-support nearly interpolates `y` and the behavior of
     midpoints is unclear.
  2. *Regime.* At fixed SNR, `n <= n_IT` means
     `x = 2 log C(p,k)/n >= log(1 + k b^2/sigma^2) -> inf`. For `k = p^gamma`
     we also have `k/n_IT -> gamma/(2(1-gamma)) > 0`. Both `q = k/n -> 0` and
     `x < x0` are used essentially in Section 4, and even the pure-noise case
     with `x >= x0` is open (Section 8, item 6). So a second-moment count is
     not the only missing piece.
  3. *Criterion.* For near-optimal supports with large overlap, which is what
     one expects near `S*`, Lemma 1.5(b) is the natural criterion, not (a):
     (a) charges `2 lam` on the overlap. Using (b) needs a lower bound on
     `||X(beta^S - beta^T)||^2` that holds uniformly over the packing, and
     uniform restricted-eigenvalue bounds for `2k`-sparse vectors are not
     available at `n < 2k log(p/k)`. "With such a count, the greedy packing
     ... and the criterion of Lemma 1.5(a) would give the clique" is
     therefore an unproved claim; it should be softened.
- **C6 (Section 6.5 evidence).** For `b/sigma = 2`, `p = 10k`, the ratio
  `n/n_IT` (first order) is 0.93, 0.92, 0.93, 1.05, 1.04, 1.14 at
  `alpha = 0.35` and 0.93, 1.08, 1.32, 1.40, 1.57, 1.71 at `alpha = 0.5`
  (`k = 3..8`; `misc_checks.log`). Most rows are therefore above the
  threshold named in the section title and in Conjecture 5.2. They are below
  the *empirical* recovery threshold (`S*` never optimal), and `k/n` is
  0.4–0.8, not small. Retitle the section ("below the empirical recovery
  threshold") and weaken "weak evidence for Conjecture 5.2" accordingly.
- **Minor (Section 6.4).** "The planted model with the same `X` and `w`": the
  generator draws the signs only when `b > 0`, so `w` differs between the
  `b = 0` and `b = 1` runs (`X` and `S*` agree; checked for seeds
  3000–3003). Say "same `X`".

## 7. Novelty and literature

Web search was exhausted (the session limit was reached). I used arXiv pages,
the arXiv API and local copies. Checked:

- **Dey–Dubey–Molinaro, "Lower bounds on the size of general branch-and-bound
  trees"** (Math. Program. 2023, arXiv 2103.09807; local full text, Sections 5
  and 6). Proposition 3 is the midpoint argument for the cross-polytope.
  Section 6 gives exponential lower bounds with high probability for a
  Gaussian-perturbed cross-polytope: a random-instance, LP-based general-B&B
  lower bound, which is the closest prior "random instance" result.
- **Dey–Shah, lot-sizing** (ORL 2022, arXiv 2112.03965; local summary). They
  use midpoints of 0/1 points whose *objective value* lies below the integer
  optimum, the linear-objective version of Lemma 1.4. The note should cite
  it next to Dey–Dubey–Molinaro.
- **Lemma 1.4 with a convex objective** is a direct transfer of these
  arguments, as the note says. The note's contribution is Lemma 1.5 and its
  use.
- **Gamarnik–Zadik** (arXiv 1701.04455, PDF read for Sections 1.2 and 3;
  arXiv 1711.04952, abstract). Their pure-noise analysis is for *binary*
  `k`-sparse `beta`. It gives a first-moment lower bound (Theorem 3.1) and a
  conditional second-moment upper bound, showing that exponentially many
  near-optimal binary vectors exist. Their Section 4 reduces the planted
  model to pure noise by conditioning on the overlap, which is the same idea
  as Lemma 4.1(b). The OGP result (1711.04952) concerns the overlap structure
  of near-optimal solutions for `n` in `[n*, c n_alg]`. The clique here is a
  different object: pairwise-far supports whose relaxed midpoints undercut
  `OPT`. Its proof uses only a first-moment bound and a marginal construction,
  with no OGP and no second moment. Section 7's description is fair.
- **Gamarnik's OGP survey** (arXiv 2109.14409, abstract) does not discuss
  relaxations or branch-and-bound.
- **arXiv API searches (2026-09-29).** No hits relevant to a
  branch-and-bound lower bound for random sparse regression with
  perspective or convex relaxations:
  - `abs:"branch-and-bound" AND abs:"overlap gap"`: 0 hits;
  - `abs:"perspective relaxation" AND abs:"regression"`: 0 hits;
  - `abs:"mixed-integer" AND "sparse" AND "exponential" AND "branch" AND "random"`: 0 hits;
  - `abs:"subset selection" AND "branch-and-bound" AND "random"`: 2 irrelevant hits;
  - `abs:"branch-and-bound" AND "sparse" AND "lower bound" AND "tree"`: 2 irrelevant hits.
- **Not checked** (from memory, worth citing as context): certification
  hardness for random optimization (e.g. Bandeira–Kunisky–Wein, low-degree
  certification), and the proof-complexity lower bounds of Dadush–Tiwari and
  Fleming et al.

**Assessment.** As far as this bounded search goes, an exponential lower bound
on *every* convex-piece certificate for the perspective relaxation of random
sparse regression appears new. The ingredients (a first-moment union bound, a
marginal top-correlation construction, a GV packing, the midpoint argument)
are standard. The significance is limited by two facts: the result is
asymptotic only, and it holds only in pure noise or at bounded total SNR,
where recovery is impossible anyway (Section 3.2). The practically relevant
fixed-SNR regime is Conjecture 5.2. An unsuccessful search does not establish
novelty.

## 8. Corrections requested

1. Section 4.2, after Theorem 4.4: replace the detection-scale sentence (C1)
   with the `sigma sqrt(2 log(p/k)/n) · sqrt(K(x)/x)` form, and state that the
   region is strictly inside `n < n_IT`.
2. Section 5, fourth bullet: add `x < x0` (`alpha > 1.59(1-gamma)`),
   `lam = o(n)` and `k/n -> 0`, and say that it concerns bounded total SNR,
   not fixed `b/sigma` (C2).
3. Proof of Theorem 4.3, Step 6: change "increases in `s_U`" to "decreases".
4. Theorem 4.3: change `lam >= 0` to `lam > 0`.
5. Section 4.4: add `log(4 pi)` to the shortfall (C3). Qualify "first gives a
   nontrivial clique at `p = 10^12`" by the grid (C4). Fix "every support
   explains about `x ||y||^2`".
6. Conjecture 5.2: specify `lam`, `eps` and a lower limit on `n`. In "what is
   missing", say that the fixed-SNR regime has `x -> inf` (and `k/n` bounded
   away from 0 for polynomial `k`), outside the Section 4 method even in pure
   noise. Replace "criterion of Lemma 1.5(a) would give the clique" with a
   hedged statement based on (b) (C5).
7. Section 6.5: retitle ("below the empirical recovery threshold"), and
   weaken the claim of evidence for Conjecture 5.2 (C6).
8. Section 6.4: "same `X` and `w`" becomes "same `X`".
9. Section 5 heuristic: derive or drop `0.6 sqrt n` and the `2^{K/2}` model
   (C7).
10. Optional: state the clique bound in the stronger form `C(p,k)^{c'}`
    (S1), after checking the sketch. Optionally use the two-copy identity as
    the proof of Lemma 1.5. Cite Dey–Shah.

## 9. Not checked

- Sections 2–3, Lemma 1.2, Corollaries 3.3–3.4, and the Section 6.1–6.3 and
  6.6–6.7 computations (other reviewer). The Section 5 text that depends on
  them was checked only for consistency.
- Rows of Tables 6.4–6.5 with `k >= 4`. I recomputed only the 24 instances
  with `k = 3` of the note's Table 6.4 exactly. My own `k = 4` runs use other
  seeds.
- The S1 strengthening is a sketch; I did not write out the error terms.
- Whether pure noise with `x >= x0` (and `lam = o(n)`) gives exponential
  cliques. My `alpha = 1` data have `lam/n ≈ 0.6` and do not bear on it.
- Literature beyond the sources listed in Section 7.

## Commands run (targeted local checks only; no project-wide checks; CI not inspected)

From `research-20260928b/reviews/sparse-hard/`, single-threaded BLAS, at most
5 worker processes:

- `python3 check_midpoint.py` → `check_midpoint.log` (Lemma 1.5 (a)/(b), conflict inequality, segment, Lemma 4.2).
- `python3 check_constants.py` → `check_constants.log` (`x0`, Beta Chernoff grid, `rho*` convergence, IT comparison, detection-scale factor, GV exponent).
- `python3 finite_p.py` → `finite_p.log`; `python3 finite_p_wide.py` (stopped at `p = 10^8.5` for time) → `finite_p_wide.log`; `python3 finite_p_wide2.py` → `finite_p_wide2.log`.
- `python3 exact_clique.py E1 e1.jsonl 4`, `... E2 e2.jsonl 4`, `... E3 e3.jsonl 5`; summaries `e1_summary.log`, `summarize.log` (`python3 summarize.py`).
- `python3 pool300.py` → `pool300.log`.
- `python3 construction_small.py construction_small.jsonl 1` → `construction_small.log`.
- `python3 misc_checks.py` → `misc_checks.log` (Table 6.5 `n/n_IT`, the shared-`w` check, `Psi(t)` asymptotics).
