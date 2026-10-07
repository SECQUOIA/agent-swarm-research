# Adaptive decomposition branch-and-bound without knowledge of `x*`, and Conjecture 3.7

Date: 2026-09-30. Extension of the decomposition note. Status: **reviewed
once** ([`../reviews/decomposition-adaptive-review.md`](../reviews/decomposition-adaptive-review.md),
verdict "fixes needed") **and revised after review**; then checked by a
confirmation review
([`../reviews/ext-decomposition-adaptive-confirm.md`](../reviews/ext-decomposition-adaptive-confirm.md),
verdict "fixes needed (minor)") **and revised again**; then checked by a
second confirmation review
([`../reviews/decomposition-adaptive-confirm-r1.md`](../reviews/decomposition-adaptive-confirm-r1.md),
verdict "fixes needed (minor)") **and revised a third time**; a third
confirmation review
([`../reviews/decomposition-adaptive-confirm-r2.md`](../reviews/decomposition-adaptive-confirm-r2.md),
verdict "verified") found the third revision correct, and its two optional
wording points were applied by the root (end of Section F). Section F lists
the changes of all three rounds and how each was checked. Proofs are complete where the status table
says "proved". Computations are floating-point illustrations, not certified
counts. Scripts and logs are in [`adaptive/`](adaptive/).

Cited notes:

- [D] [`decomposition-certificates.md`](decomposition-certificates.md)
  (Definition 1.2, Lemmas 1.3–1.5, 3.1, 3.2, Theorems 2.5, 3.4,
  Proposition 2.4, Section 3.4, Conjecture 3.7);
- [K] [`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
  (Theorem 2.1, Proposition 2.3, Theorem 3.1, Proposition 3.3,
  Corollary 3.4, Lemma 4.1, Proposition 5.4);
- [C] the constrained note
  [`instance-dependent-node-complexity.md`](../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md)
  (Lemma 6.1, Theorem 6.3);
- the reviews [`../reviews/decomposition-review.md`](../reviews/decomposition-review.md),
  [`../reviews/decomposition-recheck.md`](../reviews/decomposition-recheck.md),
  [`../reviews/consistency-review.md`](../reviews/consistency-review.md).

Notation is that of [D]: bags `V_t`, separators `S_t`, `|T|` bags, width
`w`, `k = max_i |T_i|`, (QG) with `x*` and `c_g`, (L^{1,1}) with `M_a`,
(U^q) with `alpha'` and `A`, configurations and the Lagrangian unfolding of
Lemma 1.5, consistent points of Lemma 3.2, slopes `lambda_t(x)`.

## Summary

**Task 1 (adaptive algorithm).** Section 3.4 of [D] left open how to find a
small certificate without knowing `x*`. The difficulty named there was that
"taking part in a bad configuration" is a property of whole configurations,
not of single boxes.

- **Min-marginals remove that difficulty (Lemma A.1).** One extra top-down
  pass of the dynamic program gives, for every leaf and cell, the smallest
  Lagrangian value of a configuration that uses it. No extra convex programs
  are needed.
- **Algorithm LS (Section A.2).** Level-synchronous separator branching:
  dyadic leaves and cells; split every current-level box whose min-marginal
  is below `UBD - eps`; slopes are the gradients `lambda_t(x)` at the
  consistent point of the previous minimizing configuration; restart the
  partition whenever the slopes change. It uses no knowledge of `x*` and no
  local solver.
- **Theorem A.5 (proved).** Under the hypotheses of Theorem 3.4 of [D] plus
  monotone relaxations (M), LS stops with a certificate proving tolerance
  `eps` and an `eps`-optimal incumbent. The certificate has at most
  `2|T| (1 + i* (4 rho + 4)^{w+1})` leaves and cells, with
  `rho = 2(k-1) + sqrt(6 Psi_A |T|/c_g)`,
  `Psi_A = O(k^3 M_a^2 w/c_g + k^2 M_a w + alpha' A)` and
  `i* = ceil(log2(s0 sqrt(3 Psi_A |T|/eps)))`. So the size is
  `O(|T| (C sqrt(|T|))^{w+1} log(|T|/eps))`; the restarts cost one more
  factor `log(|T|/eps)` in the number of boxes created. No drift condition
  such as (T1)–(T2) is needed, and `Delta` does not enter.
- **Proposition A.6 (proved): the factor `|T|^{(w+1)/2}` is real for LS.**
  On the path family of Theorem 4.1 of [D], every run of LS (any slopes, any
  valid incumbent) ends with at least `c n^2 log(1/eps)` leaves for
  `n >= 63`, while certificates with `O(n log(n/eps))` leaves exist. In the
  computations with exact slopes (`c = 0`, `n <= 64`) the number of split
  leaves per bag per level is at most about `26 n` (the maximum over levels:
  `25.9 n` at `n = 16`, about `22 n` at `n = 32, 64`); on the plateau of the
  middle levels it is about `21 n` at `n = 16, 32` and `20 n` at `n = 64`.
  In LS (learned slopes and incumbent) it reaches `29 n` at `n = 16`. On the two random
  instances with `n = 16` it reaches `27–28 n` with exact slopes, and `29 n`
  and `45 n` in LS, which also learns its incumbent (Sections C.1, C.2).
- **What obstructs `|T| C^{w+1} log(1/eps)` for LS (Section A.5).** LS
  tests all bags at a common width `s`, so pruning by min-marginals compares
  the local cost of a far box, about `c_g dist^2`, with the relaxation
  deficit of *all* bags, about `|T| s^2`. Proposition A.6 covers this
  level-synchronous rule only; other refinement orders are open. The
  minimizing configuration locates `x*` only to Euclidean accuracy
  `sqrt(|T|) s`, which the computations confirm. In sup norm, in the
  exact-slope runs with `c = 0`, it locates `x*` to at most `6 s` from
  level 5 on for every tested `n` (`8 s` at level 4 for `n >= 16`), and in
  LS on random instances to `3–7 s` from level 6 on (up to `11 s` at
  levels 3–5), but I cannot prove this. Re-centering shells on the consistent
  point (algorithm RC) did not reach the tolerance in two of the three
  tested settings. At `n = 8` (`c = 0`) the lower bound did reach it and
  RC's incumbent rule failed; at `n = 16` (random linear terms) the lower
  bound did not converge. (The first version's RC runs dropped some touching
  leaf-cell pairs through rounding; they were redone, Section C.3.) With a
  local solver that returns `x*` to sup-norm accuracy `sqrt(eps/|T|)`,
  Theorem 3.4 applies directly, as [D] already notes.

**Task 2 (Conjecture 3.7).** The conjecture compares `N_dec(eps)` with
`Psi(eps)`, a sum of covering numbers of bag projections with the tolerance
split into constants `eps_t`, `sum_t eps_t = eps`.

- **Lower half with a `w`-dependent power of `|T|`: true (Proposition B.1).**
  `N_dec(eps) >= Psi(eps)/(2 ceil(2 sqrt|T|))^{w+1}`. This follows from
  Theorem 2.5 of [D] and scaling.
- **Lower half with a fixed-degree `poly(|T|)`: false (Theorem B.2).** On a
  path with one-dimensional (binary) separators and bags
  `{s_t, y_t, s_{t+1}}`, `y_t in [0,1]^d`, the near-optimal set is a union
  of pieces in which only one bag is "fat". A certificate of size
  `O(K ((alpha d/eps)^{d/2} + (C max(1, sqrt(alpha d)))^d log(K/eps)))`,
  with an absolute constant `C`, exists, while
  `Psi(eps) >= K (alpha K/eps)^{d/2}`. For fixed `eps` the ratio grows like
  `K^{d/2}/log K` (and tends to `(2K/d)^{d/2}` as `eps -> 0`), faster than
  `C^{w+1} p(K) log(1/eps)` for any fixed polynomial `p` of degree
  `< d/2 = (w-1)/2`. So the power of `|T|` must
  grow with `w`, and the exponent `(w+1)/2` of Proposition B.1 cannot be
  lowered below `(w-1)/2`. A continuous-variable version is sketched.
- **The right quantity allocates the tolerance pointwise (Theorem B.3,
  proved).** For every certificate and every `eta`, the per-bag tolerances
  `e_t(z) = alpha Q_t(z)` used by the leaves satisfy
  `sum_t e_t(x_{V_t}) <= eps + eta` on `E(eta)`, and each bag needs
  `2^{-|V_t|}` times a variable-radius covering number. With sup-norm balls
  this gives the lower bound `Phi`; with Euclidean balls, from the same
  proof, the larger lower bound `Phi_2 >= Phi`. Both contain Theorem 2.5 of
  [D] and recover Proposition 2.4 of [D] up to `C^d`.
- **Sup-norm coverings lose `w^{Theta(w)}` (Proposition B.6, added after
  review).** Already for one flat bag (`|T| = 1`), `N_dec/sup_eta Phi` is at
  least a quantity that tends to `4^d Gamma(d/2+1)/pi^{d/2}` as `eps -> 0`.
  For every `eps <= alpha`, `N_dec/Psi >= Gamma(d/2+1)/(4 pi)^{d/2}`. This
  bound is also of order `w^{Theta(w)}` (`8.8e3` at `d = 80`, `9.3e15` at
  `d = 120`), but it is below 1 for `d <= 62`; as `eps -> 0` the lower bound
  tends to `Gamma(d/2+1)/pi^{d/2}`. So a two-sided
  comparison of `N_dec` with `Psi` or `Phi` must allow factors of order
  `(c sqrt(w))^{w+1}`; `C^{w+1}` with `C` independent of `w` is not enough.
  The cause is that `Psi` and `Phi` measure the tolerance per coordinate,
  while the relaxation gap adds up over coordinates. With `Phi_2` this loss disappears
  on the flat bag and on the staircase family: there
  `N_dec <= C^{w+1} log(K/eps) sup_eta Phi_2` with an absolute constant `C`
  (for `alpha <= 1`, `eps <= 1/2`). The earlier claim that `Phi` is within
  `C^{w+1}` of the certificate on the staircase family, with `C` depending
  only on `alpha`, was wrong.
- **Upper half: partial.** For one one-dimensional separator with exact
  bags, the band identity of [K] gives a separator-cell count of the
  covering form (Proposition B.4). For paths the per-edge bound does not
  combine: [K]'s tree bounds either need a joint exact split measured in sup
  norm over the whole separator, or use the band widths of reduced problems,
  for which the available lower bound degrades by a factor 2 per edge
  (Section B.5). Revised form: Conjecture B.5, with `Phi_2` in place of
  `Psi`, the degree of the polynomial independent of `w`, and `C` allowed to
  depend on `w`.

**Task 3 (computations).** LS, oracle-slope and zero-slope runs on the path
family (`n = 4..64`) and on random linear terms; the staircase certificate
(`K` up to 1024, `d = 1, 2, 4`); the re-centering variants. Section C.
After review: a split of slope and incumbent effects (C.2), the RC reruns
with a corrected intersection test (C.3), a two-sided exactness check of
the staircase leaf minima (C.4), and an evaluation of the bounds of
Proposition B.6 (`d <= 64`).

## Status

| Item | Content | Status |
|---|---|---|
| Lemma A.1 | min-marginals by an inside–outside pass | proved |
| Lemma A.2 | within a pass, pruning is permanent | proved; 0 violations in all runs |
| Lemma A.3 | configurations of boxes of side `<= s`: value `>= F(x) - (c_g/2)|x-x*|^2 - Lambda |T| s^2 - 2 nu sqrt(w|T|) s` | proved |
| Theorem A.5 | LS: termination, size `O(|T|(C sqrt|T|)^{w+1} log(|T|/eps))` | proved |
| Proposition A.6 | LS needs `Omega(n^2 log(1/eps))` leaves on the path family | proved (`n >= 63`, weak constant; level-synchronous refinement only); computed on the family (`c = 0`, `n <= 64`) with exact slopes: at most about `26 n` split leaves per bag per level (`22 n` at `n = 32, 64`); at `n = 16`: `29 n` with learned slopes (`c = 0`); with random `c`, `27–28 n` with exact slopes and `29–45 n` in LS |
| Conjecture A.7 | sup-norm localization of the minimizing configuration, `O(s)` independent of `|T|` | conjecture (hypothesis clarified after the second confirmation); observed for LS (exact slopes, `c = 0`: at most `6 s` from level 5 on, `8 s` at level 4 for `n >= 16`; random instances: `3–7 s` from level 6 on, up to `11 s` at levels 3–5); RC does not test it (Section A.5) |
| Remark A.8 | two-stage algorithm with a local-solver oracle | sketch |
| Proposition B.1 | lower half of Conjecture 3.7 with `|T|^{(w+1)/2}` | proved |
| Theorem B.2 | lower half false for any fixed-degree `poly(|T|)` (paths, 1D binary separators) | proved (shell level count in (b) corrected after confirmation; its `O`-form in the Summary corrected after the second confirmation); continuous version sketched |
| Theorem B.3 | pointwise-shared covering lower bounds `Phi` (sup norm) and `Phi_2 >= Phi` (Euclidean) | proved (`Phi_2` added after review) |
| Proposition B.6 | `N_dec/sup Phi >= 2^d Gamma(d/2+1)/pi^{d/2}` for `eps <= alpha/4` (one flat bag; staircase), and `N_dec/Psi >= Gamma(d/2+1)/(4 pi)^{d/2}`, of order `w^{Theta(w)}` and above 1 from `d = 63`, for `eps <= alpha` (one flat bag); `N_dec <= C^{w+1} log(K/eps) sup Phi_2` on both, `C` absolute | proved (added after review; lower bound from the review, rechecked; `L` in (b) corrected after confirmation; the `Psi` bound for every `eps <= alpha` stated in (a) after the second confirmation) |
| Proposition B.4 | one 1D separator, exact bags: cells `<= 1 + 3 J sup_eta N_inf(pi_S E(eta), 2 sqrt((eps+eta)/M))` | proved (from [K]) |
| Conjecture B.5 | two-sided characterization by `Phi_2`; polynomial degree independent of `w`, `C` may depend on `w` | conjecture (revised after review) |

## 0. Setting and one extra hypothesis

Everything is as in [D]. For Part A, `X0` is a cube of side `s0` (for a box,
rescale the coordinates; this changes `M_a` and `c_g`). The level-`i`
**dyadic boxes** are the products of intervals of length `s_i = s0 2^{-i}`
of the dyadic grid; cells of `S_t` and leaves of `V_t` are dyadic boxes in
those coordinates.

**(M) Monotone relaxations.** If `B' ⊂ B` then `f_{c,B'} >= f_{c,B}` on
`B'`. alphaBB with a fixed `alpha` (or with `alpha` not increasing under
refinement) and McCormick envelopes satisfy (M). Any relaxation can be made
to satisfy it by taking the maximum with the parent's relaxation; this keeps
convexity, validity and (U^q).

Configurations are those of Lemma 1.5 of [D]. With one slope vector
`lambda = (lambda_t)` the value of a configuration is

```
val = sum_t tau_t(B_t, z^t),     tau_t(B, z) = sum_{c at t} f_{c,B}(z_c) - lambda_t^T z_{S_t} + sum_{u in ch(t)} lambda_u^T z_{S_u},
```

and the root bound of the certificate with maximal `beta` is the minimum of
`val` over configurations (Lemma 1.5 of [D]).

## A. An adaptive algorithm

### A.1 Min-marginals

Fix partitions and slopes. For a leaf `B in L_t` and a cell `D in P_t` with
`D ∩ B_{S_t} ≠ ∅` put `g_t(B, D) = min { tau_t(B, z) : z in B, z_{S_t} in D }`
(one convex program; at the root `g_r(B) = min_{z in B} tau_r(B, z)`). Put
`m_u(B) = min { beta_{u,D'} : D' in P_u, D' ∩ B_{S_u} ≠ ∅ }` for a child `u`
of `t`. The upward recursion of Lemma 1.5 of [D] is
`beta_{t,D} = min over B meeting D of [ g_t(B, D) + sum_{u in ch(t)} m_u(B) ]`.

**Lemma A.1 (min-marginals).** Define top-down: `o(B) = g_r(B)` for
`B in L_r`; for `t != r` and `D in P_t`,

```
out(D) = min { o(B') + sum_{u in ch(p(t)), u != t} m_u(B') : B' in L_{p(t)}, B'_{S_t} ∩ D ≠ ∅ },
o(B)   = min { out(D) + g_t(B, D) : D in P_t, D ∩ B_{S_t} ≠ ∅ }         for B in L_t.
```

Then `MM(B) := min {val : configurations with B_t = B} = o(B) + sum_{u in ch(t)} m_u(B)`
and `MM(D) := min {val : configurations with D_t = D} = out(D) + beta_{t,D}`.
For every bag `t`, `l_r = min_{B in L_t} MM(B)`.

*Proof.* Cut a configuration at the edge between `t` and `p(t)`. The two
parts interact only through the choice of `D_t` and the condition
`D_t ∩ (B_{p(t)})_{S_t} ≠ ∅`. Given `D_t = D`, the smallest value of the part
in `sub(t)` is `beta_{t,D}` (Lemma 1.5 of [D]). The rest consists of the
parent leaf `B'` (which must meet `D`), the part above `p(t)` and the other
children's subtrees; given `B'`, these are independent, with smallest values
`o(B')` (by induction from the root) and `m_u(B')`. This gives `MM(D)`. The
formula for `MM(B)` follows in the same way with the cut placed at `B`.
Every configuration uses one leaf of every bag, which gives the last
claim. □

The top-down pass reuses the numbers `g_t(B, D)` of the upward pass, so it
needs no new convex programs. This answers the difficulty stated in
Section 3.4 of [D]: whether a box "takes part" in a configuration of value
below `UBD - eps` is the test `MM < UBD - eps`, one number per box.

### A.2 Algorithm LS (level-synchronous separator branching)

Input: `F`, a rooted tree decomposition, per-factor relaxations with (M),
`eps > 0`, a starting point `x^(-1) in X0`. The incumbent starts at
`UBD = F(x^(-1))`.

For passes `p = 0, 1, 2, ...`:

1. *Slopes.* `lambda^(p) = lambda(x^(p-1))`, with
   `lambda_t(x) = ∇_{S_t} (sum_{s in sub(t)} a_s)(x)` as in Lemma 3.2 of [D].
2. *Restart.* `L_t = {X0_{V_t}}`, `P_t = {X0_{S_t}}` for all `t` (level 0).
3. For sublevels `i = 0, 1, ..., p`:
   1. Upward and top-down passes (Lemma A.1): `l_r`, all min-marginals, and
      a minimizing configuration with consistent point `x^cons`.
   2. `UBD := min(UBD, F(x^cons))`.
   3. If `l_r >= UBD - eps`, stop. Output the certificate (the current
      partitions, slopes `lambda^(p)`, maximal `beta`) and the incumbent.
   4. If `i < p`, split every leaf and every cell *of level `i`* whose
      min-marginal is `< UBD - eps` into its `2^{|V_t|}` (resp.
      `2^{|S_t|}`) dyadic children. All other boxes stay ("frozen").
4. `x^(p) := x^cons` of sublevel `p`.

LS uses the relaxations, the gradients of the factors at points it has
computed, and function values. It does not use `x*`, `c_g`, `M_a` or a
local solver. Pass `p` rebuilds the partition from scratch because the
slopes change between passes. Within a pass the slopes are fixed.

### A.3 Analysis

**Lemma A.2 (pruning is permanent within a pass).** In pass `p` at
sublevel `i`, every configuration with value `< UBD - eps` (current `UBD`)
consists of leaves and cells of level `i`. In particular every box with
min-marginal `< UBD - eps` has level `i`, and if the stop test fails, the
minimizing configuration consists of level-`i` boxes.

*Proof.* Partitions within a pass are nested, so every current box lies in
a unique box of the partition at any earlier sublevel `i'`. Map a current
configuration to one at sublevel `i'` by replacing each leaf and cell by the
box containing it and keeping the points `z^t`. The constraints survive
(larger boxes; intersections can only grow). By (M) and fixed slopes the
value does not increase. If the current configuration contains a box `B` of
level `< i`, let `i'` be the sublevel at which `B` was created and not split.
At that time `B` was a box of the partition, so the mapped configuration
contains `B`, and `MM_{i'}(B) >= UBD_{i'} - eps`. Hence the current value is
at least `UBD_{i'} - eps >= UBD - eps`, because the incumbent never
increases. □

**Lemma A.3 (configurations of small boxes).** Assume (QG), (L^{1,1}) and
(U^q). Let the slopes `lambdâ` have error
`nu = (sum_{t != r} |lambdâ_t - lambda_t(x*)|_2^2)^{1/2}`. Let a
configuration have all leaves and cells of side `<= s`, consistent point
`x` and `X = |x - x*|_2`. Then

```
val >= F(x) - (c_g/2) X^2 - Lambda |T| s^2 - 2 nu sqrt(w |T|) s  >=  f* + (c_g/2) X^2 - Lambda |T| s^2 - 2 nu sqrt(w |T|) s,
Lambda = 2 (k-1)^2 (k M_a^2 w/c_g + M_a w) + alpha' A/4.
```

*Proof.* This is steps 1–5 of the proof of Theorem 3.4 of [D] with uniform
widths in place of shells.

1. *Drift.* `z^t_{S_t} in D_t`, `z^{p(t)}_{S_t} in (B_{p(t)})_{S_t}`, and the
   two boxes intersect, so `d_t = |z^t_{S_t} - z^{p(t)}_{S_t}|_inf <= 2 s`.
   A variable of `V_t` is copied along at most `k - 1` edges to its top bag,
   so `Delta_t = |z^t - x_{V_t}|_inf <= 2 (k-1) s`. Only the `<= w`
   coordinates of `S_t` differ, so `|z^t - x_{V_t}|_2 <= sqrt(w) Delta_t`.
2. *Relaxation.* By (U^q), `val >= sum_t a_t(z^t) - |T| alpha' A s^2/4 + sum_{t != r} lambdâ_t^T (z^{p(t)}_{S_t} - z^t_{S_t})`.
3. *Telescoping.* By (3.1) of [D] (Lemma 3.2), with the exact slopes
   `lambda_t(x*)`, `sum_t a_t(z^t) + sum_{t != r} lambda_t(x*)^T (z^{p(t)}_{S_t} - z^t_{S_t})`
   equals `F(x) + sum_t [a_t(z^t) - a_t(x_{V_t}) - ∇a_t(x*_{V_t})^T (z^t - x_{V_t})]`.
   Each bracket is at least `-(M_a/2) w Delta_t^2 - M_a r_t sqrt(w) Delta_t`
   with `r_t = |x_{V_t} - x*_{V_t}|_2`. The slope error contributes at least
   `-sum_t |lambdâ_t - lambda_t(x*)|_2 sqrt(w) d_t >= -nu sqrt(w) 2 s sqrt(|T|)`.
4. *Absorbing.* Young's inequality gives
   `M_a sqrt(w) r_t Delta_t <= (c_g/(2k)) r_t^2 + (k M_a^2 w/(2 c_g)) Delta_t^2`,
   and `sum_t r_t^2 <= k X^2`. With `Delta_t^2 <= 4 (k-1)^2 s^2`, the sum of
   the brackets is at least `-(c_g/2) X^2 - 2 (k-1)^2 (k M_a^2 w/c_g + M_a w) |T| s^2`.
5. Collect, and use (QG) for the second inequality. □

**Lemma A.4 (slopes from a point).** For `x in X0`,
`nu(lambda(x)) <= k sqrt(k-1) M_a |x - x*|_2 <= k^{3/2} M_a |x - x*|_2`.

*Proof.* `lambda_{t,i}(x) - lambda_{t,i}(x*)` is a sum of at most `k`
differences `delta_{s,i} = ∂_i a_s(x) - ∂_i a_s(x*)`, so its square is at
most `k sum_{s in T_i} delta_{s,i}^2`. A pair `(s, i)` occurs for at most
`k - 1` separators. Summing, `nu^2 <= k (k-1) sum_s |∇a_s(x) - ∇a_s(x*)|^2 <= k (k-1) M_a^2 sum_s r_s^2 <= k^2 (k-1) M_a^2 |x - x*|_2^2`. □

This is the bound quoted in Remark 3.5 of [D].

**Theorem A.5 (LS under the hypotheses of Theorem 3.4).** Assume (QG),
(L^{1,1}), (U^q) and (M), and let `X0` be a cube of side `s0`. Put

```
gamma  = 8 k^{3/2} M_a sqrt(w)/c_g,        a* = (gamma + sqrt(gamma^2 + 8 Lambda/c_g))/2,
abar   = max(a*, sqrt(n/|T|)/2),            Psi_A = Lambda + 4 k^{3/2} M_a sqrt(w) abar,
rho    = 2 (k-1) + sqrt(6 Psi_A |T|/c_g),   i* = max(0, ceil(log2(s0 sqrt(3 Psi_A |T|/eps)))).
```

(a) *Slopes.* For every pass `p` that runs (`p = 0`, or pass `p - 1` did
not stop), the slopes of pass `p` have
`nu_p <= 2 k^{3/2} M_a abar sqrt(|T|) s_p`. If pass `p` does not stop, its
final consistent point has `|x^(p) - x*|_2 <= abar sqrt(|T|) s_p`.

(b) *Localization.* In pass `p`, at a sublevel `i <= p` whose stop test
fails, `UBD - f* <= 2 Psi_A |T| s_i^2`, and every leaf of bag `t` (cell of
`S_t`) with min-marginal `< UBD - eps` lies within sup-distance `rho s_i` of
`x*_{V_t}` (of `x*_{S_t}`).

(c) *Termination and output.* LS stops in some pass `p <= i*`, at a
sublevel `<= i*`. Then `f* - eps <= UBD - eps <= l_r <= f*`: the output is
a certificate proving tolerance `eps`, and `UBD <= f* + eps`.

(d) *Size.* The output certificate has at most
`sum_t [1 + i* (4 rho + 4)^{|V_t|}] + sum_{t != r} [1 + i* (4 rho + 4)^{|S_t|}] <= 2 |T| (1 + i* (4 rho + 4)^{w+1})`
leaves and cells. Over all passes at most
`2 |T| (i* + 1)(1 + i* (4 rho + 4)^{w+1})` boxes are created, and the dynamic
program runs `sum_{p <= i*} (p+1) <= (i* + 1)^2` times.

*Proof.* Write `X_p = |x^(p) - x*|_2`, `s_{-1} = 2 s0`, `a_p = X_p/(sqrt(|T|) s_p)`.

(a) By induction on `p >= -1`, `a_p <= abar` whenever `x^(p)` is defined
(`p = -1`, or pass `p` ran and did not stop). For `p = -1`,
`X_{-1} <= sqrt(n) s0`, so `a_{-1} <= sqrt(n/|T|)/2 <= abar`. Let pass `p`
run. Then `x^(p-1)` is defined, and by Lemma A.4 and the induction
hypothesis `nu_p <= k^{3/2} M_a X_{p-1} <= 2 k^{3/2} M_a abar sqrt(|T|) s_p`.
This is the slope bound; it holds whether or not pass `p` stops later. Now
let pass `p` not stop. At sublevel `p` the stop test fails, so by Lemma A.2 the minimizing
configuration has level-`p` boxes, and its value is `l_r <= f*`
(Lemma 1.3 of [D]). Lemma A.3 gives
`(c_g/2) X_p^2 <= Lambda |T| s_p^2 + 2 nu_p sqrt(w|T|) s_p`, that is,
`a_p^2 <= 2 Lambda/c_g + gamma a_{p-1} <= 2 Lambda/c_g + gamma abar <= abar^2`;
the last step holds because `abar >= a*`, the positive root of
`a^2 = gamma a + 2 Lambda/c_g`.

(b) Pass `p` runs, so the slope bound of (a) applies to it, also when pass
`p` stops at a later sublevel. For `i <= p`, `s_p <= s_i`, so (a) gives
`2 nu_p sqrt(w|T|) s_i <= 4 k^{3/2} M_a sqrt(w) abar |T| s_i^2`. With
Lemma A.3, every configuration of level-`i` boxes satisfies
`val >= f* + (c_g/2) X^2 - Psi_A |T| s_i^2`. The stop test fails, so the
minimizing configuration has level-`i` boxes (Lemma A.2) and value
`l_r <= f*`; hence `(c_g/2) X^2 <= Psi_A |T| s_i^2`, and the first form of
Lemma A.3 gives `F(x^cons) <= l_r + (c_g/2) X^2 + Psi_A |T| s_i^2 <= f* + 2 Psi_A |T| s_i^2`.
This bounds the updated `UBD`. Now let a box have min-marginal
`< UBD - eps`, and take a configuration attaining it. By Lemma A.2 all its
boxes have level `i`, so
`(c_g/2) X^2 < Psi_A |T| s_i^2 + (UBD - f*) - eps < 3 Psi_A |T| s_i^2`.
Its leaf of bag `t` contains `z^t`, and
`|z^t - x*_{V_t}|_inf <= Delta_t + X <= 2 (k-1) s_i + sqrt(6 Psi_A |T|/c_g) s_i = rho s_i`.
The same holds for its cell of `S_t`.

(c) If the stop test failed at a sublevel `i` with `3 Psi_A |T| s_i^2 <= eps`,
the inequality in (b) would give `(c_g/2) X^2 < 3 Psi_A |T| s_i^2 - eps <= 0`.
So every sublevel `i >= i*` passes the test. Pass `i*` reaches sublevel
`i*` unless it stops earlier. At the stop, `l_r >= UBD - eps`, `UBD >= f*`,
and `l_r <= f*` (Lemma 1.3 of [D]).

(d) At sublevel `i >= 1` of a pass, the level-`i` leaves of bag `t` are
the children of level-`(i-1)` leaves with min-marginal `< UBD - eps` at
sublevel `i - 1`, whose test failed. By (b) these lie within sup-distance
`rho s_{i-1}` of `x*_{V_t}`. At most `(2 rho + 2)^{|V_t|}` closed dyadic
boxes of side `s_{i-1}` meet a cube of half-side `rho s_{i-1}`, so at most
`(4 rho + 4)^{|V_t|}` level-`i` leaves are created. Cells are the same with
`|S_t|`. Sum over sublevels `1..i*` and add the root boxes; sum over passes
`p <= i*` for the second count. □

*Order of the constants.* `abar <= gamma + sqrt(2 Lambda/c_g) + sqrt(w+1)/2`
(because `n <= (w+1)|T|`), and by the AM–GM inequality
`Psi_A <= 2 Lambda + 40 k^3 M_a^2 w/c_g + 2 k^{3/2} M_a (w+1) = O(k^3 M_a^2 w/c_g + k^2 M_a w + alpha' A)`.
Hence

```
rho = O( k + sqrt(|T|) ( k^{3/2} M_a sqrt(w)/c_g + sqrt((k^2 M_a w + alpha' A)/c_g) ) ),
size = O( |T| (C rho)^{w+1} log(|T|/eps) ).
```

Theorem 3.4 of [D] has base `1/theta = O(k sqrt(K_1 (1+Delta) w) M_a/c_g + ...)`.
For bounded `k` and `Delta`, the base of LS is larger by the factor
`sqrt(|T|)`. On the other hand LS needs no condition like (T1)–(T2): all
live boxes have the same width, so drift is at most `2 s` per edge and never
amplifies along chains, and `Delta` and `D_k` do not enter.

*The constants are loose.* On the path family of Theorem 4.1 of [D]
(`k = 2`, `w = 1`, `M_a = 2.8`, `c_g = 0.1`, `alpha' = 0.4`, `A = 2`):
`Lambda = 319.4`. With the exact slopes (`nu = 0`, so `Psi_A` can be replaced
by `Lambda`) the proof gives `rho = 2 + 138 sqrt(|T|)`. With learned slopes
it gives `Psi_A = 2.07e4` and `rho = 2 + 1.1e3 sqrt(|T|)`. The computations
with exact slopes (Section C.1, `c = 0`, `n <= 64`) show at most about `26 n` split
leaves per bag per level (the maximum over levels: `25.9 n` at `n = 16`,
about `22 n` at `n = 32, 64`), that is, an effective `rho` (with
`(2 rho)^2` split leaves per bag per level) of at most about `2.5 sqrt(n)`
(`2.4 sqrt(n)` at `n = 32, 64`).
The review measured the largest sup-distance of a split leaf from `x*`
directly: `2.0–3.8 sqrt(n) s_i` for `n = 4..32`.

**Remark (other slope rules).** For differentiable relaxations such as
alphaBB, the gradients of the *relaxed* factors at the copies `z^s` of the
minimizing configuration can replace `∇a_s(x^cons)`. For alphaBB,
`|∇(alpha q_B)| <= alpha sqrt(|c|) w(B)` and `|z^s - x*_{V_s}| <= Delta_s + r_s`,
so the slope error gains a term `O((alpha' + k M_a) sqrt(w |T|) s_{p-1})`.
This is of the same order as the bound in (a), and the recursion closes with
larger constants. I have not written this variant out.

### A.4 The factor `|T|^{(w+1)/2}` is real for LS

**Proposition A.6.** Take the path family of Theorem 4.1 of [D]:
`F_n = sum_i (x_i^2 - 0.1 x_i^4) + 0.8 sum_i x_i x_{i+1}` on `[-1,1]^n`,
bags `{t, t+1}`, alphaBB with `alpha = 0.4` on the bilinear factors, unary
factors exact, `x* = 0`, `f* = 0`. Let
`r = r(n) = max { r in N : 2.8 r^2 + 0.8 r + 1.1 <= 0.075 n }` (so `r >= 1`
for `n >= 63`, and `r^2 ~ 0.0268 n`). In the pass in which LS stops (with
any slopes and any incumbent rule with `UBD >= f*`), for every level
`i >= 1` with `r s_i <= 1` and `0.075 n s_i^2 > eps`, every bag has all
`(2r)^2` level-`i` leaves inside `[-r s_i, r s_i]^2` and splits them. Hence
the output certificate has at least

```
(n - 1) (1 + 3 (2r)^2 ( (1/2) log2(2.8/eps) - 1 ))   leaves,   that is,   Omega(n^2 log(1/eps)).
```

By contrast, Theorem 4.1(b) of [D] gives certificates with `O(n log(n/eps))`
leaves, and Theorem A.5 gives `O(n^2 log(n/eps))` for LS. So LS is
`Theta(n^2 log(1/eps))` on this family, up to `log n`.

*Proof.* Write `s = s_i = 2^{1-i}`; for `i >= 1`, `0` is a node of the
level-`i` grid.

1. *Level 0.* The only leaf of each bag is the whole box, so its
   min-marginal is `l_r <= F(0) - 0.4 sum_t q_{[-1,1]^2}(0) = -0.8(n-1) < -eps <= UBD - eps`.
   It is split, and all level-1 leaves exist.
2. *An upper bound on a min-marginal.* Let `P` be a level-`i` leaf of bag
   `t` inside `[-r s, r s]^2`, and `p = (p_1, p_2) in P`. Let `x'` have
   `x'_t = p_1`, `x'_{t+1} = p_2`, and `x'_j = (-1)^j s/2` otherwise. Take
   the configuration with `z^j = x'_{V_j}` in every bag, the leaf containing
   it, and any cell containing `x'_j`. All copies agree, so the slope terms
   vanish whatever the slopes, and the value is
   `F(x') - 0.4 sum_j q_{B_j}(x'_{V_j})`.
   - For the `>= n - 4` bags `j` that do not contain `t` or `t+1`,
     `x'_{V_j}` is the centre of a level-`i` box with vertex `0`. Every
     dyadic box of level `<= i` containing it is an ancestor, of the form
     `[0, s'] × [-s', 0]` (up to signs) or `[-1,1]^2`, and has
     `q >= 2 (s/2)(s/2) = s^2/2`.
   - `F(x') <= sum x_j'^2 + 0.8 sum x'_j x'_{j+1} <= s^2 [ (n-2)/4 - 0.2 (n-4) + 2 r^2 + 0.8 (r^2 + r) ] = s^2 [0.05 n + 0.3 + 2.8 r^2 + 0.8 r]`,
     because the `n - 4` far pairs contribute `-0.2 s^2` each.
   - So `MM(P) <= s^2 [-0.15 n + 1.1 + 2.8 r^2 + 0.8 r] <= -0.075 n s^2`.
3. *Induction.* If `0.075 n s_i^2 > eps`, every such `P` has
   `MM(P) < -eps <= UBD - eps`, the stop test fails at sublevel `i`
   (`l_r <= MM(P)`), and `P` is split. A level-`(i+1)` leaf inside
   `[-r s_{i+1}, r s_{i+1}]^2` has its dyadic parent inside
   `[-(r+1) s_{i+1}, (r+1) s_{i+1}]^2 ⊂ [-r s_i, r s_i]^2` (as `r >= 1`), so
   it is created. Start the induction at `i = 1` (step 1).
4. *Count.* Where `r s_i <= 1`, the square `[-r s_i, r s_i]^2` is the union
   of `(2r)^2` level-`i` leaves. The admissible levels satisfy
   `1 + log2 r <= i < 1 + (1/2) log2(0.075 n/eps)`; with
   `r^2 <= 0.075 n/2.8` there are at least `(1/2) log2(2.8/eps) - 1` of them.
   Each split replaces one leaf by four. □

The constant is weak (the proof uses only consistent configurations and
box centres; the computed configurations also exploit drift). The
computations with exact slopes give `(2 rho_eff)^2` of at most about `26 n`
split leaves per bag per level for `n <= 64` (maximum over levels; about
`22 n` at `n = 32, 64`, and about `20–21 n` on the plateau for `n >= 16`,
Section C.1), against `(2r)^2 ≈ 0.107 n` in the proof. These runs are on
the family itself (`c = 0`). At `n = 16` the maximum is `29 n` in LS
(learned slopes and incumbent; `c = 0`, C.1). On the random instances of C.2 (`n = 16`) it is
`27–28 n` with exact slopes and `29–45 n` in LS, which learns both the
slopes and the incumbent.

The proof uses that LS tests all bags at a common width: at sublevel `i`
every bag other than `t` still has leaves of level `<= i` at the alternating
point, so each contributes a relaxation deficit of at least `0.2 s_i^2`.
Proposition A.6 therefore applies to level-synchronous refinement only (see
Section A.5, obstacle 1).

*Mechanism.* A box at sup-distance `rho` from `x*` in one bag costs its
configurations about `c_eff rho^2` locally, while every other bag
contributes its relaxation deficit, about `-gamma_i s_i^2` (`gamma_i ≈ 2.9`
at `n = 32`, measured from `l_r`). The box is kept while
`c_eff rho^2 < gamma |T| s_i^2`. Theorem 3.4 of [D] avoids this because its
certificate is built around `x*` and never compares a far box with the
global threshold.

### A.5 What blocks the count of Theorem 3.4

Theorem 3.4 of [D] reaches `O(|T| C^{w+1} log(|T|/eps))` because its boxes
at sup-distance `rho` from `x*` have width `theta rho`, with `theta`
independent of `|T|`. To reach this count, an adaptive algorithm would have
to stop refining a box once its width is a fixed fraction of its distance to
`x*`, without knowing `x*`. The following are the obstacles I found.

1. **Global thresholds at a common width.** LS stops refining a box only
   when all configurations through it are worth at least `UBD - eps`, and it
   tests all bags at the same width `s_i`. The test then compares the box's
   local cost with the relaxation deficit of all other bags, about
   `|T| s_i^2`. Proposition A.6 shows the resulting `|T|^{(w+1)/2}` on a
   concrete family. *Scope (corrected after review):* the proof of
   Proposition A.6 uses that at the test every other bag still has leaves of
   level `<= i`, so it covers level-synchronous refinement only. A rule that
   prunes by the same min-marginal test but refines in another order (for
   example, near the minimizing configuration first, which shrinks the other
   bags' deficits before far boxes are tested) is not covered. Whether such
   a rule avoids the factor `|T|^{(w+1)/2}` is open.
2. **Localization of `x*`.** What an algorithm can compute about `x*` is the
   consistent point of a minimizing configuration. Lemma A.3 bounds its
   Euclidean distance by `sqrt(2 Psi_A |T|/c_g) s`. A shell partition
   around such a point needs sup-norm accuracy `O(h)`, and with
   `h ~ sqrt(eps/|T|)` the Euclidean bound is too weak by `sqrt(|T|)`
   (Remark 3.5 of [D] makes the same point for local solves). The
   computations confirm both parts: for LS with exact slopes on the path
   family (`c = 0`), at every level from 5 on,
   `|x^cons - x*|_2/s_i = 5.3, 11.4, 21.5, 32.2, 46.7` for
   `n = 4, 8, 16, 32, 64` (divided by `sqrt(n)`: 2.6, 4.0, 5.4, 5.7, 5.8, so
   about `5.8 sqrt(n)` from `n = 32` on), while
   `|x^cons - x*|_inf/s_i = 4, 5, 6, 6, 6` (exactly, in a full-precision
   rerun; `logs/check_localization.log`). At level 4 the sup-norm ratio is
   6 at `n = 8`, and 8 for `n >= 16`, where the consistent point has a
   coordinate at `±1`. In the final pass of LS with learned slopes (`c = 0`,
   `n = 4..32`) the sup-norm ratio is the same as with exact slopes at
   levels 2–4 (8 at level 4 for `n = 16, 32`), below 1 at levels 0–1, and
   between 3 and 6 from level 5 on, except 12 at the
   stopping sublevel 11 of `n = 4`. At a stopping sublevel no box is live,
   Lemma A.2 does not apply, and here the minimizing configuration consists
   of frozen level-10 leaves; in units of their side `s_10` the ratio is 6.
   On the random
   instances of Section C.2 (`n = 8, 16`, not symmetric),
   `|x^cons - x*|_inf/s_i` in the final LS pass stays between 3.1 and 7.2
   from level 6 on (up to 11.0 at levels 3–5;
   `logs/random_n*_eps1e-4.log`).

**Conjecture A.7 (sup-norm localization).** Under (QG), (L^{1,1}) and
(U^q), possibly with an additional hypothesis, there is `C_loc` independent
of `|T|` such that, for every certificate in which some box is live
(min-marginal `< UBD - eps`) and all live boxes have side `<= s` (as in LS
at a sublevel whose stop test fails), the consistent point of a minimizing
configuration satisfies `|x^cons - x*|_inf <= C_loc s`.

*Clarified after the second confirmation review.* The earlier statement
did not require a live box. Without one the hypothesis holds for every
`s > 0`, and the statement would force `x^cons = x*`. If some box is live,
then `l_r < UBD - eps`, and every box of a minimizing configuration has
min-marginal `l_r`, so it is live and has side `<= s`.

Why a proof is not immediate: (QG) is a global statement,
`m(x) >= c_g |x - x*|_2^2`, and a minimizing configuration minimizes a sum
over all bags. A sup-norm bound needs a local exchange argument. One would
replace the configuration on a window of bags around the worst bag by one
near `x*`, and splice it at bags where the configuration is already close to
`x*`. That needs a *conditional* growth condition on windows with
perturbed boundary values, which (QG) does not give. On the path family the
Hessian `tridiag(0.8, 2, 0.8)` has entries of its inverse decaying by a
factor `0.5` per step, so such a condition plausibly holds there; I have not
proved it.

**A natural way to exploit Conjecture A.7 did not work in the tests.**
Algorithm RC (`adaptive/rc_lib.py`): in round `j` build shell partitions
`Pi(xhat_j; h_j, theta)` (Lemma 3.1 of [D]) around the current centre with
`h_j = 2^{1-j}` and `theta = 1/16`, use slopes `lambda(xhat_j)`, run the
dynamic program, update the incumbent with `F` at the consistent point, and
take the consistent point as the next centre. If the centre error stayed
`O(h_j)`, Theorem 3.4 of [D] with an inexact centre would give
`O(|T| (4/theta)^{w+1} log(1/h_j))` per round and
`O(|T| C^{w+1} log^2(|T|/eps))` in total. Note that RC does not test
Conjecture A.7 itself: its partitions do not have uniform live widths.

*Correction of the RC computations (after review).* The first version's RC
runs used a closed intersection test on rounded box edges. Around a
non-dyadic centre, a leaf and a cell that touch in exact arithmetic can miss
each other by one rounding unit; the test then drops the pair, and the
computed `l_r` is too high, so it is not a valid bound. The review found
that the `n = 16` trajectory changes under `1e-9` perturbations of the
centre and attributed this to shells around a centre on the box boundary.
My check (`adaptive/check_rc_sensitivity.py`) shows that the cause of the
jumps of `l_r` is the dropped pairs. With the closed test, `1e-9` moves of
the round-1 centre change `l_r` by up to 0.19, also for an interior
coordinate (`x_6 = -0.9915`, where moves of `1e-12` to `1e-3` flip `l_r`
between `-15.38` and `-15.57`). With the test widened by `1e-12`, which
keeps all touching pairs, every such move changes `l_r` by less than
`1e-9`, and the round-1 bound is `-15.725` instead of the `-15.384` of the
first version. The review's observation about the boundary is still right
for the partition itself: moving a centre coordinate at `±1` inward by
`1e-9` adds sliver boxes of width `1e-9` (for example, 11,333 leaves and 240
cells become 11,360 and 241), and with the widened test the round-1 pair
count changes from 25,612 to 25,673–25,718. So the shell partition is
discontinuous in a centre on the boundary, but this does not change `l_r`.
LS is not affected: its dyadic box edges are exact in binary floating point,
and the `n = 16` exact-slope run is identical with the widened test. All RC
runs were redone with the widened test (`logs/rc_*_tol.log`). The results
(Section C.3):

- `n = 4`, `c = 0`, `eps = 1e-6`: identical to the first version. Stable;
  the centre error settles at `3 h_j`, and RC stops at round 13 (the 14th
  round, counting round 0; 111,573 boxes).
- `n = 8`, `c = 0`, `eps = 1e-6`: identical to the first version through
  round 23. The centre error is at most `10 h_j` up to round 9 and
  `12–16 h_j` at rounds 10–15. From round 14 the incumbent stays at
  `1.013e-6`, and from round 15 the rounds form a period-2 cycle:
  `f* - l_r` alternates between `9.2e-7` and `1.54e-6` (round 14 has
  `1.59e-6`). At rounds 15, 17, ..., 23 the lower bound has reached the
  tolerance (`f* - l_r = 9.2e-7 < eps`). RC fails to stop only because its
  incumbent, `F` at consistent points, stalls `1.01e-6` above `f*`. So this
  run is evidence against RC's incumbent rule, not against the localization
  of the minimizing configuration. From round 15 the centre alternates
  between two nearly fixed points, at sup-distance `9.8e-4` and `1.22e-3` from `x*` (the
  centres of rounds `j` and `j - 2` differ by `5e-6` at round 17 and by
  `4e-7` at round 19; `adaptive/check_rc_cycle.py`). So the centre stops
  approaching `x*`, and its error in units of `h_j` grows (to `4096 h_j` at
  round 23).
- `n = 16`, random linear terms, `eps = 1e-4`, both seeds, 22 rounds: RC
  does not converge. For seed 0 the centre error grows geometrically from
  round 7 (`8.2 h_j`; `7e5 h_j` at round 21), and from round 16 the rounds
  form a period-2 cycle with `f* - l_r` alternating between 0.71 and 0.97
  and the incumbent stalled at `-0.1377` (`f* = -0.1491`). For seed 1 the
  centre error grows from round 4, the cycle starts at round 8 with
  `f* - l_r` alternating between 0.53 and 0.56, and the incumbent never
  improves on `F(0) = 0` (`f* = -0.1205`). Here the lower bound itself is
  far from the tolerance. The first version's seed-0 values (a gap cycling
  between `1.6e-2` and `2.9e-2`, `UBD = -0.1356`) came from the closed test
  and are withdrawn; the review's re-run with its own DP and the closed test
  diverged along yet another path.

So pure re-centering failed to reach the tolerance in two of the three
tested settings. At `n = 8` the failure is due to the incumbent rule; at
`n = 16` the lower bound does not converge either. A heuristic explanation
for the `n = 16` runs: when the centre is off, the region around `x*` is
covered by boxes of width about `theta` times the centre error. The
minimizing configuration sits there, and its consistent point is accurate
only to that width. So the conjecture, if true, has to be used with uniform
live widths near the optimum, as in LS; shells around an estimated centre do
not provide it. I do not know how to combine uniform live widths with a
count independent of `|T|`.

**Remark A.8 (two-stage algorithm with a local-solver oracle; sketch).**
Assume a local solver that, started within Euclidean distance `r_loc` of
`x*`, returns `xhat` with `|xhat - x*|_inf <= h` for any requested `h`
(Newton-type methods do this at a nondegenerate interior minimizer, for
some `r_loc`). Run LS until
`abar sqrt(|T|) s_p <= r_loc`; by Theorem A.5(a) this takes a number of
levels independent of `eps`, costing
`O(|T| (C sqrt(|T|))^{w+1} log(abar sqrt(|T|) s0/r_loc))`. Then build the
certificate of Theorem 3.4 of [D] around the local solution, with slopes
`lambda(xhat)`, whose size is `O(|T| C^{w+1} log(|T|/eps))`. The factor
`|T|^{(w+1)/2}` then multiplies only an `eps`-independent term. The
algorithm does not know `r_loc`, `theta` or `h_0`; interleaving the stages
with doubling guesses (and checking each candidate certificate by the
dynamic program) should cost at most logarithmic factors. I have not written
this bookkeeping out, so this remark is a sketch. On the tested instances
the local solve from the first consistent point already returns `x*`
(Section C.3), so these runs illustrate the second stage only.

## B. Conjecture 3.7

### B.1 The statement, and when it is trivial

Conjecture 3.7 of [D]: under (L^{1,1}), (U^q), (G_alpha) and a hypothesis
on the near-optimal sets "that makes copy errors second order along them",
`N_dec(eps)` lies within factors `C^{w+1} poly(|T|) log(1/eps)` of

```
Psi(eps) = min over eps_1 + ... + eps_|T| = eps of  sum_t sup_{eta >= 0} N_inf( pi_{V_t}(E(eta)), sqrt((eps_t + eta)/alpha) ),
```

where `N_inf(A, r)` is the least number of sup-norm cubes of side `r`
covering `A`. There are two readings of "`C^{w+1} poly(|T|)`": (R1) the
degree of the polynomial does not depend on `w`, and `C` may depend on `w`;
(R2) the degree may depend on `w`.

*Corrected after review.* The first version defined (R1) with `C` also
independent of `w`. In that form the upper half of the conjecture fails for
trivial reasons: already for one flat bag (`|T| = 1`), `N_dec(eps)/Psi(eps)`
is at least `Gamma(d/2+1)/(4 pi)^{d/2}` for every `eps <= alpha`, which is
of order `w^{Theta(w)}` (as `eps -> 0` the lower bound tends to
`Gamma(d/2+1)/pi^{d/2}`; Proposition B.6(a)), because `Psi` measures the tolerance
per coordinate in sup norm while the relaxation gap adds up over
coordinates. So `C` must be allowed to grow at least like `sqrt(w)`, and the
readings differ only in the power of `|T|`.

*Under (QG) the conjecture holds in both readings, with `C` of order
`sqrt(w)`.* `E(eta)` lies in the
Euclidean ball of radius `sqrt(eta/c_g)` around `x*`, so each term of `Psi`
is at most `ceil(2 sqrt(alpha/c_g))^{|V_t|}` for every `eps_t`, and
`|T| <= Psi(eps) <= |T| ceil(2 sqrt(alpha/c_g))^{w+1}`. On the other side
`|T| <= N_dec(eps)`, and Theorem 3.4 of [D] gives
`N_dec(eps) <= |T| C^{w+1} log(|T|/eps)` with `C = 4/theta`. Its `1/theta`
contains the factor `sqrt(w)` (and depends on `k`, `Delta`, `M_a/c_g` and
`alpha' A/c_g`), so the upper half is established with `C` of order
`sqrt(w)`; I do not know whether it holds under (QG) with `C` independent of
`w`. The conjecture therefore has content only for degenerate near-optimal
sets, and in its dependence on `|T|`.

### B.2 The lower half with a `w`-dependent power of `|T|`

**Proposition B.1.** Assume (G_alpha) with gap in all bag coordinates
(`K_t = V_t` in Theorem 2.5 of [D]). Then for every `eps > 0`

```
N_dec(eps) >= Psi(eps) / (2 ceil(2 sqrt(|T|)))^{w+1}.
```

*Proof.* Take the equal allocation `eps_t = eps/|T|` in `Psi`. Since
`eps/|T| + eta >= (eps + eta)/|T|` and `N_inf(A, r)` does not increase with
`r`, and a cube of side `2R` is the union of `ceil(2R/r)^d` cubes of side
`r`,

```
N_inf(A, sqrt((eps/|T| + eta)/alpha)) <= N_inf(A, sqrt((eps + eta)/(|T| alpha))) <= ceil(2 sqrt(|T|))^{|V_t|} N_inf(A, 2 sqrt((eps + eta)/alpha)).
```

The proof of Theorem 2.5 of [D] works bag by bag and for each `eta`:
`|L_t| >= 2^{-|V_t|} N_inf(pi_{V_t}(E(eta)), 2 sqrt((eps + eta)/alpha))`.
Take the supremum over `eta` in each bag and sum over `t`. □

So the lower half holds in reading (R2), with the exponent `(w+1)/2`.

### B.3 The lower half fails in reading (R1)

**The staircase family.** Fix `K >= 2`, `d >= 1`, `alpha in (0, 1]`,
`eps in (0, 1]` and `P >= alpha d/4 + 1`. Variables: `s_1, ..., s_{K+1}` in
`{0, 1}` and `y_1, ..., y_K` in `[0,1]^d`. Bags
`V_t = {s_t, y_t, s_{t+1}}`, `t = 1..K`, form a path with root `V_1`; the
separators are `S_t = {s_t}`, `t = 2..K`, one-dimensional. So `|T| = K`,
`w = d + 1`, `k = 2`. One factor per bag:

```
a_t(s_t, y_t, s_{t+1}) = (1 - s_{t+1} + s_t) |y_t|^2 + P (s_t - s_{t+1})_+^2.
```

It is `C^{1,1}` on `[0,1]^{d+2}`, and `a_t >= 0`, so `f* = 0`.
`a_t = 0` iff `s_{t+1} - s_t = 1`, or `s_t = s_{t+1}` and `y_t = 0`.
Hence `E(0)` is the set of nondecreasing binary sequences `s` with
`y_t = 0` in every bag, except that the (at most one) bag with
`(s_t, s_{t+1}) = (0, 1)` has `y_t` free. In particular
`E(0) ⊇ A_t = { s = (0^t, 1^{K+1-t}), y_t in [0,1]^d, y_j = 0 (j != t) }`:
only one bag is "fat" at a time.

*Relaxation.* On a box `B` (binary coordinates fixed or not), `f_{t,B}` is
the convex envelope, over the continuous hull of `B`, of the function equal
to `a_t - alpha q_{B_y}(y)` at points with binary `s`-coordinates (and
`+inf` elsewhere); `q_{B_y}` is the `q_B` of the `y`-coordinates. For fixed
binary `(s_t, s_{t+1})` this function is convex in `y`, and a binary point
is an extreme point of the `s`-square, so the envelope equals
`a_t - alpha q_{B_y}` at every feasible point of `B`. Hence (U^q) holds with
`alpha' = alpha`, and (G_alpha) holds with weight `alpha` on every
coordinate (the `s`-terms of `q_B` vanish at binary points). On boxes that
fix the binaries, `f_{t,B} = a_t - alpha q_{B_y}` (alphaBB with a fixed
`alpha`, the same modelling assumption as Proposition 2.4 of [D]).

**Theorem B.2.**

(a) `Psi(eps) >= K (alpha K/eps)^{d/2}`.

(b) There is a decomposition certificate proving tolerance `eps` with at
most

```
K [ ceil(sqrt(alpha d/(2 eps)))^d + 2 (J + 1)(4/theta)^d + 1 ] + 2 (K - 1)
```

leaves and cells, where `h_0 = sqrt(2 eps/(K d alpha^2))`,
`J = max(0, ceil(log2(1/h_0)))` (so `J + 1` is the number of shell levels of
Lemma 3.1 of [D] with `s0 = 1`), and `theta` is the largest power of `1/2`
with `theta <= min(1, 2/sqrt(alpha d))`. (*Corrected after confirmation:*
the earlier version had `log2(1/h_0) + 2` in place of `J + 1`. That is an
upper bound on `J + 1` only for `h_0 <= 2`; for `h_0 > 2`, allowed when
`alpha^2 K d < eps/2`, it is below 1 and can be negative.)

(c) For fixed `d`, `alpha`, `eps`, `Psi(eps)/N_dec(eps) >= c K^{d/2}/log K`
for `K >= 2`, with `c > 0` independent of `K`. Hence for every `C >= 1` and
every polynomial `p` of degree `< d/2 = (w-1)/2`, the inequality
`N_dec(eps) >= Psi(eps)/(C^{w+1} p(|T|) log(1/eps))` fails for all large
`K`. The lower half of Conjecture 3.7 is false in reading (R1), and in
reading (R2) the exponent of `|T|` must be at least `(w-1)/2`
(Proposition B.1 gives `(w+1)/2`). This holds also when `C` depends on `w`,
because `d` stays fixed while `K` grows.

*Proof.* (a) `pi_{V_t}(E(0))` contains the slice `{0} × [0,1]^d × {1}`. A
sup-norm cube of side `r` meets this slice in a set of `d`-volume at most
`r^d`, so `N_inf(pi_{V_t}(E(0)), r) >= r^{-d}`. Take `eta = 0` in the
supremum and `r = sqrt(eps_t/alpha)`. Then
`sum_t (alpha/eps_t)^{d/2} >= K (alpha K/eps)^{d/2}` for every allocation,
by convexity of `u -> u^{-d/2}`.

(b) *Cells:* `P_t = {{0}, {1}}` (exact fixing, Section 1.6 of [D]), zero
slopes, `beta` maximal. *Leaves of bag `t`*, for each binary pair
`(sigma, sigma')` of `(s_t, s_{t+1})`:

- `(0, 1)`: the uniform grid of `[0,1]^d` with side
  `h_1 = 1/ceil(sqrt(alpha d/(2 eps)))`. Here `a_t = 0`, and the relaxed
  minimum on a leaf is `-alpha d h_1^2/4 >= -eps/2`.
- `(0, 0)` and `(1, 1)`: the shell partition `Pi(0; h_0, theta)` of
  `[0,1]^d` (Lemma 3.1 of [D], centre at the corner `0`). Here
  `a_t = |y|^2`. On the central cube `[0, min(h_0, 1)]^d` the relaxed
  minimum is at least `-d alpha^2 h_0^2/(4 (1 + alpha)) >= -eps/(2K)`. Every other cube `B` has
  `w(B) <= theta dist_inf(B, 0)`, so its relaxed minimum is at least
  `dist_inf^2 (1 - alpha d theta^2/4) >= 0`.
- `(1, 0)`: one leaf `[0,1]^d`, relaxed minimum
  `>= P - alpha d/4 >= 1`.

Bags 1 and `K` split their private binary `s_1`, `s_{K+1}` the same way.
Cells fix the separator values exactly, and a parent leaf fixes them too,
so the intersection condition forces the copies to agree. Configurations
are therefore binary sequences `s` with one leaf per bag in the slice
`(s_t, s_{t+1})`, and by Lemma 1.5 of [D]
`l_r = min_s sum_t m_t(s_t, s_{t+1})`, where `m_t` is the smallest relaxed
minimum over the leaves of the slice. A sequence with `A` ascents and `D`
descents has `A <= D + 1`, so

```
sum_t m_t >= -A eps/2 - K eps/(2K) + D (P - alpha d/4) >= -eps/2 - eps/2 + D (P - alpha d/4 - eps/2) >= -eps.
```

The counts are those of the three slices, with Lemma 3.1 of [D] for the
shells (`s0 = 1`, at most `(J + 1)(4/theta)^d` boxes), plus two cells per
separator.

(c) For fixed `d`, `alpha`, `eps`, the bound in (b) is
`O(K) + O(K log K)`, while (a) gives `K^{1 + d/2} (alpha/eps)^{d/2}`. □

The mechanism: at every point of `E(0)` at most one bag has coordinates in
the interior of its leaves, and the other bags sit at box vertices, where
the relaxation gap vanishes. So each bag can use the whole tolerance on its
fat slice. `Psi` forces one constant allocation `eps_t` per bag, valid on all
of `E(eta)`, and so charges `K^{d/2}` too much. The computations
(Section C.4) reproduce the ratio: `Psi/size ≈ (2/d)^{d/2} K^{d/2}` for
`K = 4..1024`, `d = 1, 2, 4`, with `l_r >= -eps` in every case.

**Remark (continuous separators; sketch).** Let `s_t in [0,1]` and add to
bag `t` the concave penalty `P s_t (1 - s_t)` (and `P s_{K+1}(1 - s_{K+1})`
to bag `K`), relaxed by its secant, with alphaBB on the product term. Then
`E(0)` is the same set, so (a) holds verbatim. For (b) two new effects
appear. The `s`-coordinates now carry relaxation gaps; on cells of moderate
width the secant penalties grow linearly away from `{0, 1}` and should
dominate them. And configurations can move a separator copy across touching
cells, so a descent of `s` could be hidden in copy drift; cells of width
below `1/(2K)`, or suitable slopes, should block this at a cost polynomial
in `K` and independent of `eps`. I expect
`N_dec = O(K^{O(1)} (C/eps)^{d/2} log(K/eps))`, hence the conclusion of (c)
as `eps -> 0`. This is not proved.

### B.4 A lower bound that shares the tolerance pointwise

For a certificate and a bag `t` with gap weights as in Theorem 2.5 of [D]
(`alpha` on `K_t ⊂ V_t`), define on `X0_{V_t}`

```
Q_t(z) = min { sum_{i in K_t} a_i^B(z) : B in L_t, z in B },      e_t(z) = alpha Q_t(z).
```

For a function `e >= 0` on `X0_{V_t}` and `A ⊂ X0_{V_t}`, let `N_t(e; A)` be
the least number of points `v` in `R^{K_t}` such that every `z in A` has
`|z_{K_t} - v|_inf <= sqrt(e(z)/alpha)` for one of them (a covering with
variable radius). Let `N_t^{(2)}(e; A)` be defined in the same way with the
Euclidean norm `|z_{K_t} - v|_2` in place of the sup norm. A Euclidean ball
lies in the sup-norm ball of the same radius, so `N_t^{(2)} >= N_t`. Call a
family `(e_t)` **admissible for `E(eta)`** if
`sum_t e_t(x_{V_t}) <= eps + eta` for every `x in E(eta)`.

**Theorem B.3.** For every certificate proving tolerance `eps` and every
`eta >= 0`, the family `(alpha Q_t)` is admissible for `E(eta)`, and
`|L_t| >= 2^{-|K_t|} N_t^{(2)}(alpha Q_t; pi_{V_t}(E(eta))) >= 2^{-|K_t|} N_t(alpha Q_t; pi_{V_t}(E(eta)))`.
Hence

```
N_dec(eps) >= sup_{eta >= 0} Phi_2(eps, eta) >= sup_{eta >= 0} Phi(eps, eta),
Phi(eps, eta)   = inf over admissible (e_t) of  sum_t 2^{-|K_t|} N_t(e_t; pi_{V_t}(E(eta))),
Phi_2(eps, eta) = inf over admissible (e_t) of  sum_t 2^{-|K_t|} N_t^{(2)}(e_t; pi_{V_t}(E(eta))).
```

*Proof.* For `x in E(eta)`, Lemma 1.4 of [D] gives leaves `B_t ∋ x_{V_t}`
with `alpha sum_t sum_{i in K_t} a_i^{B_t}(x) <= m(x) + (f* - l_r) <= eta + eps`,
and `Q_t(x_{V_t})` is at most the inner sum. For `z in X0_{V_t}`, let `B`
attain `Q_t(z)`. Each `a_i^B(z) = (z_i - l_i)(u_i - z_i)` is at least the
square of the distance `d_i` from `z_i` to the nearer endpoint, so
`sum_{i in K_t} d_i^2 <= Q_t(z)`: `z_{K_t}` is within Euclidean (hence also
sup-norm) distance `sqrt(Q_t(z))` of a vertex of `B_{K_t}`. The
`2^{|K_t|} |L_t|` such vertices are an admissible set of points for
`N_t^{(2)}(alpha Q_t; ·)`. □

The first version stated Theorem B.3 with `Phi` only. The Euclidean form
`Phi_2` was pointed out in the review. The proof is the same; it only keeps
the fact that the squared distances `d_i^2` add up.

*Relation to the earlier bounds.*

- Every admissible family has `e_t <= eps + eta` on `pi_{V_t}(E(eta))`, and
  points with radius `R` correspond to cubes of side `2R`, so
  `Phi(eps, eta) >= sum_t 2^{-|K_t|} N_inf(pi_{K_t}(E(eta)), 2 sqrt((eps + eta)/alpha))`:
  Theorem B.3 contains Theorem 2.5 of [D].
- In the product setting of Proposition 2.4 of [D] (`K` blocks, `E(0)` contains
  a product of flat boxes of volume `v`), admissibility on the product forces
  `sum_k sup e_k <= eps`, and the same computation as in Theorem B.2(a)
  gives `N_dec >= K v (alpha K/(16 eps))^{d/2}`. This is Proposition 2.4 of
  [D] up to a factor at most `2^d`.
- On the staircase family every admissible family has `e_t <= eps` on the
  fat slice, so `Phi(eps, 0) >= K 2^{-(d+2)} (alpha/(4 eps))^{d/2}`.
  *Corrected after review:* the first version concluded from this and
  Theorem B.2(b) that `N_dec(eps) <= C^{w+1} log(K/eps) sup_eta Phi(eps, eta)`
  with `C` depending only on `alpha`. That is false. `C` must grow like
  `sqrt(w)` with `Phi`, while `Phi_2` needs no such growth
  (Proposition B.6(b)).

So `Phi` and `Phi_2` share the tolerance exactly where near-optimal points
force the bags to be simultaneously inaccurate, and nowhere else. Within a
bag, only `Phi_2` adds the tolerance up over coordinates the way the
relaxation gap does.

**Proposition B.6 (sup-norm coverings lose `w^{Theta(w)}`; added after
review).** Let `V_d = pi^{d/2}/Gamma(d/2+1)` be the volume of the unit ball
in `R^d`.

(a) *One flat bag.* Let `|T| = 1`, `X0 = [0,1]^d`, `F = 0`, and relax on
every box by `-alpha q_B` (so (U^q) and (G_alpha) hold with weight `alpha` on
every coordinate, and `w = d - 1`). For `eps <= alpha/4`,

```
N_dec(eps) >= (alpha/eps)^{d/2}/V_d,     sup_eta Phi(eps, eta) <= 2^{-d} ceil(sqrt(alpha/(4 eps)))^d <= 2^{-d} (alpha/eps)^{d/2}.
```

So `N_dec/sup_eta Phi >= 2^d/V_d`, and the ratio of the two bounds tends to
`4^d/V_d = 4^d Gamma(d/2+1)/pi^{d/2}` as `eps -> 0`. For `Psi`, which uses
cubes of side `sqrt(eps/alpha)`, `Psi(eps) = ceil(u)^d` with
`u = sqrt(alpha/eps)`, and the lower bound on `N_dec` holds for every
`eps > 0`, so `N_dec/Psi >= (u/ceil(u))^d/V_d`. For every `eps <= alpha`
this is at least `1/(2^d V_d) = Gamma(d/2+1)/(4 pi)^{d/2}`; it equals
`1/V_d = Gamma(d/2+1)/pi^{d/2}` when `u` is an integer and tends to `1/V_d`
as `eps -> 0`. All these grow like `w^{Theta(w)}`; for example
`1/(2^d V_d) >= (d/(8 pi e))^{d/2}`. The bound `1/(2^d V_d)` is below 1 for
`d <= 62` and above 1 from `d = 63` (`8.8e3` at `d = 80`). On the
other hand `N_dec(eps) <= ceil(sqrt(alpha d/(4 eps)))^d` and
`sup_eta Phi_2(eps, eta) >= 2^{-d} max(1, (alpha/eps)^{d/2}/V_d)`, so
`N_dec/sup_eta Phi_2 <= (8 pi e)^{d/2}` for `eps <= alpha d/4`.

(b) *Staircase family* (Section B.3) with `alpha <= 1` and `eps <= 1/2`.
Every certificate proving tolerance `eps` has at least
`K (alpha/eps)^{d/2}/V_d` leaves, while

```
sup_eta Phi(eps, eta) <= K 2^{-(d+2)} ( ceil(sqrt(alpha/(4 eps)))^d + 3 ).
```

So `N_dec/sup_eta Phi >= 2^d/V_d` for `eps <= alpha/4`, and the ratio of the
two bounds tends to `4 · 4^d/V_d` as `eps -> 0`. On the other hand, with
`L = J + 1`, the number of shell levels in Theorem B.2(b), which satisfies
`1 <= L <= (1/2) log2(K d/(2 eps)) + 2` (if `J >= 1`, then
`L < log2(1/h_0) + 2 = (1/2) log2(K d alpha^2/(2 eps)) + 2` and
`alpha <= 1`; if `J = 0`, then `L = 1` and `K d/(2 eps) >= 2`),

```
N_dec(eps) <= [ 4 (16 pi e)^{d/2} + 8 L (128 pi e)^{d/2} + 3 · 2^{d+2} ] sup_eta Phi_2(eps, eta),
```

which is `C^{w+1} log(K/eps) sup_eta Phi_2` with an absolute constant `C`.
With `Phi` in place of `Phi_2` the same computation gives
`N_dec <= (C sqrt(w))^{w+1} log(K/eps) sup_eta Phi`, and by the first part
the factor `sqrt(w)` cannot be removed.

*Proof.* *Lower bounds on `N_dec`.* In (b), fix a bag `t` and
`y in [0,1]^d`, and let `x in A_t` have `y_t = y`. Then `m(x) = 0`, and
Lemma 1.4 of [D] gives a leaf `B` of bag `t` containing `(0, y, 1)` with
`alpha q_{B_y}(y) <= eps` (the `s`-terms of `q_B` vanish at binary points).
As in the proof of Theorem B.3, `y` lies within Euclidean distance
`r = sqrt(eps/alpha)` of a vertex of `B_y`. Inside one leaf such points form
at most `2^d` pieces, each in one orthant of a ball of radius `r` around a
vertex, of total volume at most `V_d r^d`. The leaves must cover `[0,1]^d`
in this way, so `|L_t| >= 1/(V_d r^d)`. Sum over `t`. In (a) the same
argument applies to every `y in [0,1]^d = E(0)`. Neither argument uses a
bound on `eps`.

*Upper bounds on `Phi` and `Psi`.* In (a), `e = eps` is admissible for every `eta`
(`E(eta) = [0,1]^d`), and sup-norm cubes of side `2 sqrt(eps/alpha)` cover
`[0,1]^d` with `ceil(sqrt(alpha/(4 eps)))^d` centres; the last inequality
uses `ceil(u) <= 2u` for `u >= 1`. Likewise, with `|T| = 1` the only
allocation is `eps_1 = eps`, the supremum over `eta` is attained at
`eta = 0`, and `Psi(eps) = N_inf([0,1]^d, sqrt(eps/alpha)) = ceil(sqrt(alpha/eps))^d`,
which is at most `2^d (alpha/eps)^{d/2}` for `eps <= alpha`. Finally
`Gamma(d/2+1) >= (d/(2e))^{d/2}` gives `1/(2^d V_d) >= (d/(8 pi e))^{d/2}`.
In (b), take `e_t = a_t + eps` on the
slice `(s_t, s_{t+1}) = (0,1)`, `e_t = a_t` on `(0,0)` and `(1,1)`, and
`e_t = a_t - eps` on `(1,0)`. Here `e_t >= 0` because `a_t >= P >= 1` on
`(1,0)` and `eps <= 1/2`. A binary sequence with `A` ascents and `D`
descents has `A <= D + 1`, so `sum_t e_t = m(x) + eps (A - D) <= eta + eps`
on `E(eta)`, for every `eta`. On `(0,1)`, `e_t = eps` and
`ceil(sqrt(alpha/(4 eps)))^d` points suffice. On `(0,0)` and `(1,1)`,
`e_t = |y|^2` and the radius `|y|_2/sqrt(alpha) >= |y|_inf` (as `alpha <= 1`),
so the single point with `y = 0` suffices; on `(1,0)`,
`e_t >= 2 |y|^2` and again one point suffices. With `2^{-|K_t|} = 2^{-(d+2)}`
this gives the bound on `sup_eta Phi`. For fixed `eps <= alpha/4`,
`ceil(sqrt(alpha/(4 eps)))^d + 3 <= 4 (alpha/eps)^{d/2}`, which gives
`N_dec/sup_eta Phi >= 2^d/V_d`.

*Upper bounds on `N_dec` against `Phi_2`.* In (a), the uniform grid of side
`1/ceil(sqrt(alpha d/(4 eps)))` has relaxed minimum `>= -eps` on every leaf.
Every admissible family has `e <= eps` on `E(0) = [0,1]^d`, and a Euclidean
ball of radius `sqrt(eps/alpha)` has volume `V_d (eps/alpha)^{d/2}`, which
gives the lower bound on `Phi_2`. Then, for `eps <= alpha d/4`,
`N_dec/sup Phi_2 <= (alpha d/eps)^{d/2} 2^d V_d (eps/alpha)^{d/2} = (4 pi d)^{d/2}/Gamma(d/2+1) <= (8 pi e)^{d/2}`,
using `Gamma(d/2+1) >= (d/(2e))^{d/2}`. In (b), the same volume argument on
the fat slice gives `sup_eta Phi_2 >= K 2^{-(d+2)} M` with
`M = max(1, (alpha/eps)^{d/2}/V_d)`. Compare the three parts of the size
bound of Theorem B.2(b) with `K 2^{-(d+2)} M`:
- the fat grid: `ceil(sqrt(alpha d/(2 eps)))^d` is `1` or at most
  `(2 alpha d/eps)^{d/2}`; the ratio is at most `2^{d+2}` or
  `4 (8 pi d)^{d/2}/Gamma(d/2+1) <= 4 (16 pi e)^{d/2}`;
- the shells: `2 L (4/theta)^d` with `4/theta < max(8, 4 sqrt(alpha d))`;
  the ratio is at most `8 L 16^d` (if `alpha d <= 4`) or
  `8 L (64 pi d eps)^{d/2}/Gamma(d/2+1) <= 8 L (128 pi e)^{d/2}`;
- the remaining `K` leaves and `2 (K-1)` cells: ratio at most `3 · 2^{d+2}`.
With `Phi` and `sup Phi >= K 2^{-(d+2)} max(1, (alpha/(4 eps))^{d/2})` the
same three comparisons give `4 (32 d)^{d/2}`, `8 L max(16, 16 sqrt(d))^d`
and `3 · 2^{d+2}`, that is, `(C sqrt(w))^{w+1} log(K/eps)`. □

The computation `adaptive/check_phi_loss.py` evaluates these bounds for
`d` up to 64 (`logs/check_phi_loss.log`). With `alpha = 1`, `K = 1024`,
`eps = 1e-6`, the lower bound on `N_dec/sup Phi` on the staircase family,
taken to the power `1/(d+2)`, is `2.43, 4.01, 5.52, 7.74` at
`d = 4, 16, 32, 64` (about `0.97–1.2 sqrt(d)`). The upper bound on
`N_dec/sup Phi_2` to the same power is `3.29, 4.65, 5.13, 5.44`; it stays
below 5.5 for `d <= 64`, and the proof bounds it by an absolute constant
(times the logarithmic factor). For one flat bag
at `eps = 1e-6` the corresponding numbers are `2.68, 4.38, 5.89, 8.07`
(power `1/d`) and `2.98, 3.65, 3.85, 3.97`. The script also scans 2,880
cases (`alpha` from 1 to `1e-4`, `eps` from `1/2` to `1e-6`, `K` from 2 to
1024, `d` from 1 to 64). With `L = J + 1` the upper bound on
`N_dec/sup Phi_2` stays below the displayed constant in every case (at most
0.31 times it), and `L <= (1/2) log2(K d/(2 eps)) + 2` holds. With the
earlier `L = log2(1/h_0) + 2` it exceeded the displayed constant in 89
cases, all with `h_0 > 4`, by up to a factor 1.36.

### B.5 The upper half

**One separator.** Take two super-bags sharing a one-dimensional separator
`s in X_S` (an interval of length `s0`), exact bag minima (the split
relaxation of [K]) and the cellwise affine class `PA` on cells `P`. Assume
box data that are `C^{1,1}`, so that by Lemma 4.1 of [K] the child value
function `U` is `M_U`-semiconcave and `L = f* - V` is `M_L`-semiconvex. Put
`M = (M_L + M_U)/2` and `w(s) = U(s) - L(s) = min { m(x) : x_S = s }`, so
that `{w <= eta} = pi_S(E(eta))`.

**Proposition B.4.** Refine dyadically, splitting a cell `D` while
`M r_D^2 - min_D w > eps` (`r_D` = half the length of `D`). The result has
`gap(PA) <= eps` and at most

```
1 + 3 J sup_{eta >= 0} N_inf( pi_S(E(eta)), 2 sqrt((eps + eta)/M) )   cells,     J = max(0, ceil(log2(s0 sqrt(M/eps)/2))).
```

*Proof.* By Proposition 2.3 of [K], `gap(PA) = max_D g_D`, and by
Proposition 5.4(a) of [K], `g_D <= M r_D^2 - min_D w`, which is `<= eps` for
the final cells. A dyadic interval of level `j` (half-length `r_j`) is split
only if `M r_j^2 > eps` (at most `J` levels) and it meets
`{w < eta_j} ⊂ pi_S(E(eta_j))` with `eta_j = M r_j^2 - eps`. A closed
interval of length `2 r_j = 2 sqrt((eps + eta_j)/M)` meets at most 3 closed
dyadic intervals of that length, so at most
`3 N_inf(pi_S(E(eta_j)), 2 sqrt((eps + eta_j)/M))` intervals are split at
level `j`. Each split adds one cell. □

So for one one-dimensional separator the copy error has exactly the
covering form of `Psi`, with `M` in place of `alpha`, and kinks of the value
functions anywhere cost nothing extra. In this sense the "hypothesis that
makes copy errors second order" holds automatically for one-dimensional
separators of box problems with `C^{1,1}` data (on original bands).

**Why this does not extend to paths.** Three facts from [K] block the
obvious routes.

1. *Per-edge control is false* (Proposition 3.3 of [K]). Any proof must be
   joint over the edges.
2. *The joint upper bound of Theorem 3.1 of [K]* is
   `2 inf_{psi exact} sum_e dist(psi_e, Phi_e)` with the sup norm over the
   whole separator. It does not discount the parts of the separator where the
   band is wide. With `psi` the DP split, concave kinks of `U_e` away from the
   pinch set then cost first order, so cells are needed there even though
   Proposition B.4 says they are not needed for one edge.
3. *The sequential bound (Corollary 3.4 of [K])* uses the band widths `w'_e`
   of the reduced problems. After a split `phi_e` is absorbed, the reduced
   margin satisfies only `m' >= m̃ - (U_e - phi_e)(x_{S_e})`, with
   `m̃ = min_{x_u} m`. A split in the middle of the band gives only the
   bound `m' >= m̃/2`, and repeating this along a path degrades this lower
   bound by a factor `2` per edge. This is a loss in the available bound; I
   have not shown that the reduced bands themselves thin out. A split near
   the top of the band avoids the loss but cannot be affine near concave
   kinks of `U_e`.

If the reduced bands were stable (`w'_e >= c w_e - eps/|T|` for a constant
`c`), Proposition B.4 applied edge by edge with tolerance `eps/|T|` would
give the upper half for paths with one-dimensional separators in the
exact-bag model; splitting the tolerance costs at most a factor
`ceil(sqrt(|T|))` per one-dimensional separator. I could neither
prove nor refute band stability. The certificate model adds the bag
relaxation error, which Theorem 3.4 of [D] handles under (QG) and which
would need the pointwise allocation of Theorem B.3 in general.

### B.6 Revised conjecture

**Conjecture B.5 (revised after review).** Replace `Psi` by `Phi_2` (with
`alpha` on the lower side and `alpha'` on the upper side). Under (L^{1,1}),
(U^q) and (G_alpha), and a hypothesis on copy errors (for paths with
one-dimensional separators and `C^{1,1}` box data perhaps none, by
Proposition B.4), `N_dec(eps)` lies within factors
`C^{w+1} poly(|T|) log(1/eps)` of `sup_eta Phi_2(eps, eta)`, where the degree
of the polynomial does not depend on `w` and `C` may depend on `w` (reading
(R1) of Section B.1).

The first version used `Phi` and did not say whether `C` may depend on `w`.
Since `Phi_2 >= Phi`, the lower half becomes stronger and the upper half
weaker; the lower half is Theorem B.3. The conjecture is consistent with
every case worked out so far: (QG) (Theorem 3.4 of [D] and Section B.1, with
`C` of order `sqrt(w)`, using `Phi_2 >= |T| 2^{-(w+1)}`), products
(Proposition 2.4 of [D]), the staircase family (Theorem B.2 and
Proposition B.6(b)) and one flat bag (Proposition B.6(a)); in the last two
`C` is absolute. With `Phi` or `Psi` in place of `Phi_2`, `C` must grow at
least like `sqrt(w)` (Proposition B.6). Whether `C` can be taken independent
of `w` with `Phi_2` is open: under (QG) the upper bound of Theorem 3.4 of [D]
has `sqrt(w)` in its base, and I have no matching lower bound. It is a
conjecture: the upper half is open even for one-dimensional separators
(Section B.5).

*Follow-up (root, 2026-09-30):*
[`covering-upper-half.md`](covering-upper-half.md) proves the upper half in
the exact-bag model of Proposition B.4 for trees with one-dimensional
separators, without band stability or copy-error hypotheses (Theorem 3
there; an upper bound only), and for decomposition certificates only in
part. The conjecture in reading (R1) for certificates remains open.

## C. Numerical checks

All values are floating point (nested bisection with 60 steps for the
convex subproblems, as in `../dp_certificate.py`). They illustrate the
statements; they are not certified counts. Family of Theorem 4.1 of [D]:
`b = 0.8`, `kappa = 0.1`, alphaBB `alpha = 0.4` on the bilinear factors,
unary factors exact, `X0 = [-1,1]^n`, bags `{t, t+1}`. "Split per bag per
level" is the largest, over levels, of the mean number of level-`i` leaves
per bag with min-marginal `< UBD - eps`. "Processed" counts the partition
size summed over all dynamic-program sweeps (all passes and sublevels).

### C.1 LS on the path family (`c = 0`, `x* = 0`)

Exact slopes (`lambda = 0`), one pass, `eps = 1e-6` (`logs/oracle_eps1e-6.log`).
These runs start at `x^(-1) = 0 = x*`, so the incumbent equals `f*` from the
first sweep (not stated in the first version). The last column is the shell
certificate of [D] at `theta = 1/16` (Section 5.4 of [D]).

| n | final level | size | split per bag per level | per `n` | processed | shells [D] |
|---|---|---|---|---|---|---|
| 4 | 12 | 2,914 | 35.3 | 8.8 | 16,047 | 92,816 |
| 8 | 13 | 29,228 | 152.9 | 19.1 | 159,953 | 238,696 |
| 16 | 14 | 153,584 | 413.7 | 25.9 | 887,743 | 511,896 |
| 32 | 15 | 632,586 | 725.1 | 22.7 | 3,928,245 | 1,154,488 |
| 64 | 15 | 2,397,460 | 1,428.3 | 22.3 | 13,759,255 | 2,346,616 |

- The split count per bag per level grows linearly in `n`, as Theorem A.5
  and Proposition A.6 predict for `w = 1`. The table gives its maximum over
  levels: `25.9 n` at `n = 16` (level 5) and about `22 n` at `n = 32` and
  `64` (level 6). It is roughly constant over the middle levels, about
  `21 n` at `n = 16` and `32` (levels 7–11) and `20 n` at `n = 64` (about
  1,290 at levels 8–12), and drops in the last levels, where the gap
  reaches `eps`.
- LS certificates are smaller than the shell certificates of [D] up to
  `n = 32` and about equal at `n = 64`. Beyond that the `n^2` growth of LS
  must lose.
- The root gap falls by a factor 4 per level (for example
  `2.15e-5 -> 5.37e-6 -> 1.34e-6` at `n = 32`, levels 12–14), and the
  measured deficit is about `2.9 s_i^2` per bag.
- Localization of the consistent point (every level from 5 on, the same up
  to the rounding of the log because on this symmetric instance the
  consistent point scales with `s_i` from level to level): `|x^cons - x*|_2/s_i = 5.3, 11.4, 21.5, 32.2, 46.7`
  and `|x^cons - x*|_inf/s_i = 4, 5, 6, 6, 6` for `n = 4..64`. The log
  prints three digits (for example 5.98–6.02 for `n >= 16`); a full-precision rerun
  (`check_localization.py`, `logs/check_localization.log`) gives exactly
  4, 5 and 6. Earlier levels differ: at level 4 the sup-norm ratio is
  4, 6, 8, 8, 8 (the consistent point has a coordinate at `±1` for
  `n >= 16`), and at levels 1–3 it is at most 4. (This bullet previously
  said levels 8–12.)

LS with restarts and learned slopes, `x^(-1) = 0.5 (1, ..., 1)`,
`eps = 1e-4` (`logs/scaling_eps1e-4.log`):

| n | stopping pass / level | size | processed | split per bag per level | shells [D] at `1e-4` |
|---|---|---|---|---|---|
| 4 | 11 / 11 | 2,841 | 61,701 | 41.3 | 64,976 |
| 8 | 12 / 11 | 21,473 | 505,380 | 152.9 | 173,608 |
| 16 | 12 / 12 | 136,187 | 2,299,137 | 468.9 | 372,312 |
| 32 | 13 / 12 | 459,928 | 10,190,068 | 726.3 | 865,912 |

The split count per bag per level of this table is the maximum over the
levels of the final pass: `10.3, 19.1, 29.3, 22.7 n` for `n = 4, ..., 32`.
At `n = 16` it rises in the last split level (level 11) above the
exact-slope maximum of `25.9 n`; at levels 4–10 it is `14–26 n`.

The processed count of LS with restarts is 17–24 times the final size in
this table and 15.5–22.8 times in the LS runs of C.2, so about 15–24 times
over all LS runs. For a single pass (the exact-slope table above, and the
oracle runs of C.2) this ratio is 4.0–6.2. At the same `eps`, LS processes
5.0–6.5 times as many boxes as the oracle pass of C.2. That pass has the
exact slopes and also the exact incumbent from the first sweep, so this
factor combines the cost of the restarts with the effect of the learned
slopes and incumbent (C.2). (The first version said "by about 20"; that is
the ratio to the final size.)
Lemma A.2 was checked in every sublevel of every run: no frozen box ever had
min-marginal below `UBD - eps` (`viol = 0`).

### C.2 Nonzero multipliers (`c ~ U(-0.2, 0.2)^n`, seeds 0 and 1, `eps = 1e-4`)

`logs/random_n8_eps1e-4.log`, `logs/random_n16_eps1e-4.log`. Oracle = one
pass with the exact slopes `lambda(x*)`, started at `x^(-1) = x*`, so it
also has the exact incumbent `f*` from the first sweep. Zero slopes also
start at `x*` and were capped at 10 levels. LS starts at `x^(-1) = 0`.

| n | seed | `lambda*` range | LS size (processed) | oracle size (processed) | zero slopes |
|---|---|---|---|---|---|
| 8 | 0 | [-0.10, 0.07] | 22,559 (514,961) | 19,590 (79,034) | not done; at level 10 gap `1.27e-3`, 1,422 split per bag |
| 8 | 1 | [-0.22, 0.21] | 25,225 (562,420) | 22,075 (87,403) | not done; 3,953 split per bag |
| 16 | 0 | [-0.27, 0.27] | 147,538 (2,473,132) | 114,215 (491,624) | not done; 6,858 split per bag |
| 16 | 1 | [-0.22, 0.21] | 165,598 (2,568,857) | 111,980 (481,905) | not done; 7,735 split per bag |

- LS certificates are 14–48% larger than the oracle's, and LS also pays for
  the restarts. *Corrected after review:* the first version attributed this
  excess to the learned slopes alone. It compares learned slopes *and* a
  learned incumbent with exact ones. Rerunning the final LS pass with one
  ingredient swapped (`adaptive/check_slope_incumbent.py`; sizes relative to
  the oracle):

  | n | seed | LS slopes, exact incumbent | exact slopes, LS incumbent | both (= final LS pass) | exact slopes, `x^(-1) = 0` |
  |---|---|---|---|---|---|
  | 8 | 0 | 1.074 | 1.022 | 1.152 | 2.322 |
  | 8 | 1 | 1.078 | 1.020 | 1.143 | 2.424 |
  | 16 | 0 | 1.103 | 1.060 | 1.292 | 2.517 |
  | 16 | 1 | 1.253 | 1.161 | 1.479 | 2.495 |

  So the slopes alone cost 7–25%, the incumbent alone 2–16%, and the two
  effects compound. The LS incumbent at the start of the final pass was
  `0.27–0.76 eps` above `f*`. The slope error in the final pass is about
  `1e-2` (`n = 8`, seed 0: `nu = 1.16e-2`).
- The incumbent also explains part of the value of the restarts: one pass
  with the exact slopes but `x^(-1) = 0` gives 45,491 and 53,506 at `n = 8`
  (about twice LS with restarts) and 287,423 and 279,384 at `n = 16`
  (about 1.9 and 1.7 times LS).
- With zero slopes the gap only halves per level and the split count
  doubles per level, as Proposition 2.6 of [D] predicts (first-order copy
  error); with LS the gap falls by 4 per level and the split count per bag
  stays roughly constant across levels (about 150 at `n = 8`), except that
  at `n = 16` it rises in the last split levels, to `29 n` (seed 0) and
  `45 n` (seed 1) at level 11 of the final pass.

### C.3 Re-centering (Section A.5)

`theta = 1/16`. Current logs, made with the leaf-cell intersection test
widened by `1e-12` (Section A.5): `logs/rc_zero_eps1e-6_tol.log`,
`logs/rc_random_n16_eps1e-4_tol.log`, `logs/rc_randomlocal_n16_eps1e-4_tol.log`.
The first-version logs without `_tol` used the closed test and are kept for
the record; for `c = 0` they are identical to the new ones, for random `c`
without a local solve they are superseded.

- Pure re-centering: stable at `n = 4` (`c = 0`, stops at round 13, size
  111,573, processed 717,302); period-2 cycle at `n = 8` (`c = 0`, capped at
  23 rounds), with the lower bound within the tolerance at every other round
  and the incumbent stalled; no convergence at `n = 16` (random `c`, seeds 0
  and 1, capped at 22 rounds). Details in Section A.5.
- With a local solve (L-BFGS-B) from each consistent point: the first local
  solve returns `x*` (to `1e-8` in the slopes) for both seeds at `n = 16`,
  and the shell certificates around it stop at round 9 with 368,172 and
  367,750 boxes (processed 1,645,240 and 1,642,045), the same as with the
  closed test. This is Theorem 3.4 of [D] with an almost exact centre. At
  `n = 16` it is larger than LS (147,538 and 165,598), as in C.1.

### C.4 The staircase family (`logs/check_staircase.log`)

`alpha = 1`, `P = alpha d/4 + 1`. The root bound of the certificate of
Theorem B.2(b) is computed exactly (closed-form bag minima, then a two-state
dynamic program over binary sequences). `Psi_lb = K (alpha K/eps)^{d/2}`.
The prediction for the last column is `(2/d)^{d/2}` as `eps -> 0`
(1.41, 1, 0.25).

| d | eps | K | `l_r/eps` | size | `Psi_lb` | `Psi_lb/size` | `/K^{d/2}` |
|---|---|---|---|---|---|---|---|
| 1 | 1e-6 | 4 | -0.69 | 2.94e3 | 8.00e3 | 2.72 | 1.36 |
| 1 | 1e-6 | 1024 | -0.75 | 7.61e5 | 3.28e7 | 43.1 | 1.35 |
| 2 | 1e-3 | 4 | -0.68 | 4.26e3 | 1.60e4 | 3.76 | 0.94 |
| 2 | 1e-3 | 1024 | -0.74 | 1.12e6 | 1.05e9 | 940 | 0.92 |
| 2 | 1e-6 | 1024 | -0.75 | 1.02e9 | 1.05e12 | 1024 | 1.00 |
| 4 | 1e-3 | 1024 | -0.74 | 4.20e9 | 1.07e15 | 2.56e5 | 0.244 |
| 4 | 1e-6 | 1024 | -0.75 | 4.11e15 | 1.07e21 | 2.62e5 | 0.249 |

In all 30 rows `l_r >= -eps` (between `-0.66 eps` and `-0.75 eps`).

*Exactness of the closed-form leaf minima (check corrected after review).*
The first version supported the closed forms only by a brute-force grid
check (`K = 4`, `eps = 1e-3`, `d = 1, 2`: no leaf where the closed form
exceeds the grid minimum). That check is one-sided: closed form `<=` grid
minimum does not imply closed form `<=` true minimum, which is what the
validity of `l_r` needs. `check_staircase.py` now checks every row
two-sidedly. The relaxed function on a leaf is a separable, strictly convex
quadratic, so its minimizer is the clipped stationary point; the script
verifies the KKT conditions at that point (so it is the true minimizer) and
that the relaxed function evaluated directly there equals the closed form.
In all 30 rows the largest KKT violation is 0 and the largest value
difference is `2.2e-16`, for all shell leaves, the `(1,0)` leaf and a fat
grid leaf. All other numbers of the table are unchanged. (The review also
found agreement with L-BFGS-B to `2.2e-16`.)

## D. Limitations and open problems

- *Constants.* The proof constants of Theorem A.5 are loose (Section A.3):
  `rho = 2 + 138 sqrt(|T|)` with exact slopes against at most about
  `2.5 sqrt(n)` observed (`c = 0`, `n <= 64`). Proposition A.6's constant is weak (it uses only
  consistent configurations), and it covers level-synchronous refinement
  only.
- *Cost measure.* Theorem A.5 counts boxes and dynamic-program sweeps. The
  convex programs are one per (leaf, cell) pair; in LS a frozen coarse leaf
  can meet many fine cells, and I have not bounded the pairs per leaf beyond
  the trivial `|P_t|`.
- *Assumptions.* (M) is needed for Lemma A.2; LS is stated for a cube.
  The slope rule uses exact gradients of the factors; relaxed gradients are
  only remarked on.
- *The main open problem of Part A.* Is there an algorithm that knows
  neither `x*` nor the constants, uses no local solver, and needs
  `|T| C^{w+1} polylog(|T|/eps)` boxes under the hypotheses of Theorem 3.4?
  (*Root, 2026-10-01:* answered yes for path decompositions with
  `∇F(x*) = 0` in [`adaptive-matching.md`](adaptive-matching.md), whose
  Corollary 4 also proves Conjecture A.7 for path decompositions under
  `∇F(x*) = 0`; trees remain open. The next sentence predates this and
  holds beyond that case.)
  Proposition A.6 rules out LS. Conjecture A.7 (sup-norm localization) is
  supported by the LS data but unproved, and the re-centering heuristic RC
  did not reach the tolerance in two of three tested settings (at `n = 8`
  because of its incumbent rule; Section A.5). Remark A.8 is a sketch.
- *Floating point.* Box edges around non-dyadic centres are rounded. The
  RC code now widens the leaf-cell intersection test by `1e-12` so that
  touching boxes are paired (Section A.5). LS uses dyadic boxes, whose edges
  are exact. `../dp_certificate.py` of [D] uses the same closed test; the
  shell certificates of [D] quoted in C.1 are centred at `x* = 0`, and I
  have not checked whether its computations with non-dyadic centres are
  affected.
- *Theorem B.2* is rigorous for binary separator variables, allowed by
  Section 1.6 of [D]; the continuous version is a sketch.
- *Upper half of Conjecture 3.7.* Open, even for paths with one-dimensional
  separators in the exact-bag model. With `Psi` (or `Phi`) it can hold only
  if `C` may grow like `sqrt(w)` (Proposition B.6). The missing piece is a joint
  (not edge-by-edge) control of copy errors, for example band stability of
  reduced problems (Section B.5).
- *Computations* are on the path family only (`w = 1`, two-variable bags),
  up to `n = 64`, and on the staircase family by exact formulas.
- *Literature.* No new search was made. Lemma A.1 is the standard two-pass
  min-marginal (max-marginal) computation on junction trees, known in
  substance from graphical models; its use as a pruning test for
  decomposition certificates is the point here. LS is the decomposition
  analogue of uniform bisection in [C, Lemma 6.1]. Novelty of the other
  results is not established.

## E. Commands run

All commands were run from `research-20260929/theory-decomposition/adaptive/`
with `OMP_NUM_THREADS=1`, Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0. These
are targeted checks of this note only; no project-wide verification was
run and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 run_ls.py oracle 64 1e-6` | `logs/oracle_eps1e-6.log` | table C.1 (exact slopes); split per bag per level at most about `26 n` (`25.9 n` at `n = 16`, `22 n` at `n = 32, 64`); localization ratios; `viol = 0` |
| `python3 run_ls.py scaling 32 1e-4` | `logs/scaling_eps1e-4.log` | table C.1 (LS with restarts); `viol = 0` |
| `python3 run_ls.py random 8 1e-4`, `python3 run_ls.py random 16 1e-4` | `logs/random_n8_eps1e-4.log`, `logs/random_n16_eps1e-4.log` | table C.2 |
| first version: `python3 run_rc.py zero 64 1e-6` (stopped by hand during `n = 8`, after round 23) | `logs/rc_zero_eps1e-6.log` | closed intersection test; identical to the rerun below |
| first version: `python3 run_rc.py random 16 1e-4` (stopped by hand during seed 0, after round 21; the log's closing comment says 20, corrected by an appended line) | `logs/rc_random_n16_eps1e-4.log` | closed intersection test; superseded |
| first version: `python3 run_rc.py randomlocal 16 1e-4` | `logs/rc_randomlocal_n16_eps1e-4.log` | closed intersection test; same stops as the rerun |
| `python3 check_staircase.py` (rerun after review) | `logs/check_staircase.log` | table C.4; `l_r >= -eps` in all rows; ratio `~ (2/d)^{d/2} K^{d/2}`; two-sided exactness check: KKT violation 0, value error `<= 2.2e-16` |
| after review: `python3 check_slope_incumbent.py 8 1e-4`, `python3 check_slope_incumbent.py 16 1e-4` | `logs/check_slope_incumbent_n8.log`, `logs/check_slope_incumbent_n16.log` | C.2 split of slope and incumbent effects; LS, oracle and final-pass sizes reproduced |
| after review: `python3 check_rc_sensitivity.py 16 0` | `logs/check_rc_sensitivity.log` | round-1 RC bound: jumps up to 0.19 under `1e-9` centre moves with the closed test, `< 1e-9` with the widened test |
| after review: `python3 run_rc.py zero 8 1e-6 23` | `logs/rc_zero_eps1e-6_tol.log` | widened test; `n = 4` stops at round 13; `n = 8` cycle, identical to the first version |
| after review: `python3 run_rc.py random 16 1e-4 21` | `logs/rc_random_n16_eps1e-4_tol.log` | widened test; no convergence for seeds 0 and 1 (Section A.5) |
| after review: `python3 run_rc.py randomlocal 16 1e-4 21` | `logs/rc_randomlocal_n16_eps1e-4_tol.log` | widened test; stops at round 9 with 368,172 and 367,750 boxes |
| after review, rerun after confirmation: `python3 check_phi_loss.py` | `logs/check_phi_loss.log` | bounds of Proposition B.6 for `d <= 64`; after confirmation with the level count `L = J + 1` (quoted `eps = 1e-6` values unchanged) and a scan of 2,880 cases: displayed constant holds in all (Section B.4) |
| after review: inline regression, `run_ls` (exact slopes, `n = 16`, `eps = 1e-6`) with the intersection test widened by `1e-12` | none (quoted in Section F) | identical to the closed test: size 153,584, `l_r = -5.7944e-7`, split per bag 413.7 |
| after confirmation: `python3 check_rc_cycle.py 19` | `logs/check_rc_cycle.log` | RC `n = 8`, `c = 0`: rounds 0–19 reproduce `logs/rc_zero_eps1e-6_tol.log`; centre alternates between two nearly fixed points from round 15 (Section A.5) |
| after confirmation: inline, round-1 RC shell partitions of `check_rc_sensitivity.py` (`n = 16`, seed 0) with one centre coordinate moved by `1e-9` | none (quoted in Section F) | moves of the `±1` coordinates 1, 2, 7, 14 add sliver boxes of width `1e-9` (11,333 leaves and 240 cells become 11,357–11,369 and 241); a move of the interior coordinate 6 changes nothing |
| after confirmation: inline recomputation from `logs/oracle_eps1e-6.log`, `logs/scaling_eps1e-4.log`, `logs/random_n*_eps1e-4.log` | none (quoted in Section F) | split per bag per level by level; processed/size ratios; random-`c` localization by level |
| after the second confirmation: `python3 check_localization.py 64 32` | `logs/check_localization.log` | reruns the C.1 exact-slope runs (`n = 4..64`) and LS runs (`n = 4..32`); sizes equal the logs; `|x^cons - x*|_inf/s_i` exactly 4, 5, 6, 6, 6 from level 5 on with exact slopes, 8 at level 4 for `n >= 16`; leaves of the minimizing configuration at the current level except at the stopping sublevel of LS at `n = 4` (level 10; ratio `12 s_11 = 6 s_10`) |
| after the second confirmation: inline recomputation from `logs/oracle_eps1e-6.log`, `logs/scaling_eps1e-4.log`, `logs/random_n*_eps1e-4.log` | none (quoted in Section F) | localization ratios by level (including levels 1–4 and the stopping sublevels); split per bag per level of the random-`c` oracle runs (`27.86 n`, `27.16 n` at `n = 16`) |
| after the second confirmation: inline evaluation of `Gamma(d/2+1)/(4 pi)^{d/2}` (`d = 1..199`) and of the size bound of Theorem B.2(b) against the old and corrected Summary forms (720 cases, `d <= 4096`) | none (quoted in Section F) | below 1 exactly for `d <= 62`; `8.8e3` at `d = 80`, `9.3e15` at `d = 120`. Old form with `C = 16` below the bound in 103 cases; corrected form above it in all cases |

The runs in `logs/random_n*.log`, `logs/scaling_eps1e-4.log` and
`logs/oracle_eps1e-6.log` used a first version of `ls_lib.dp` with dense
leaf-by-cell matrices; the current version uses sparse interval pairs. The
two versions agree on the `n = 16` oracle run (size 153,584,
`l_r = -5.7944e-7`, split per bag 413.7), which was rerun with the current
version as a check. Scripts: `ls_lib.py` (algorithm LS, min-marginals),
`run_ls.py`, `rc_lib.py` and `run_rc.py` (re-centering), `check_staircase.py`
(Theorem B.2); added after review: `check_slope_incumbent.py`,
`check_rc_sensitivity.py`, `check_phi_loss.py`; added after confirmation:
`check_rc_cycle.py`; added after the second confirmation:
`check_localization.py`. Code changes after review:
`ls_lib.run_ls` also records the slopes and incumbent point at the start of
each pass (no change in any computed number); `ls_lib.dp` and
`interval_pairs` take an optional widening `tol` (default 0, so LS is
unchanged); `rc_lib.run_rc` uses `tol = 1e-12`; `run_rc.py` takes an
optional round cap. Code change after confirmation: `check_phi_loss.py` uses
the level count `J + 1` of Lemma 3.1 of [D] in the staircase size bound
(it had `log2(1/h_0) + 2`) and prints the scan of Proposition B.6(b).
Code change after the second confirmation: `ls_lib.dp` also returns the
leaf of the minimizing configuration in each bag, and `ls_lib.run_ls`
records their levels (`conf_lev`); no computed number changes (the rerun
sizes and ratios equal the logs).

## F. Revision after review

The review ([`../reviews/decomposition-adaptive-review.md`](../reviews/decomposition-adaptive-review.md))
found the proofs of Part A and of Proposition B.1, Theorem B.2, Theorem B.3
and Proposition B.4 correct, reproduced every LS number with independent
code, and listed nine issues (verdict "fixes needed"). I checked each issue
before changing the note. All checks are targeted checks of this note; no
project-wide verification was run and no CI results were consulted.

1. **Staircase: "`C` depending only on `alpha`" (moderate). Confirmed; the
   claim was false.** I re-derived the review's volume bound (Lemma 1.4 of
   [D] at the points of `A_t`, and at most one orthant of a ball of radius
   `sqrt(eps/alpha)` per vertex of a leaf) and its admissible family
   (`sum_t e_t = m(x) + eps (A - D) <= eta + eps`, `e_t >= 0`, the four
   covering counts). *Changes:* the third bullet after Theorem B.3 and the
   Summary are corrected; Theorem B.3 now also gives the Euclidean bound
   `Phi_2 >= Phi`; new Proposition B.6 proves that `Phi` loses a factor
   `w^{Theta(w)}` on the staircase family and that `Phi_2` is within
   `C^{w+1} log(K/eps)` of `N_dec` there, with an absolute `C`. *Check:*
   `check_phi_loss.py` evaluates all bounds of Proposition B.6 for
   `d <= 64`. It reproduces the review's values of the loss divided by
   `4^{d+2}` (`0.05, 0.19, 1.06, 130, 5.8e4` at `d = 4, 12, 16, 24, 32`,
   `alpha = 1`, `eps = 1e-2`).
2. **Flat bag, reading (R1), and the (QG) remark (moderate). Confirmed.**
   For `|T| = 1` and `F = 0` the same computation gives
   `N_dec/sup Phi >= 2^d Gamma(d/2+1)/pi^{d/2}` for `eps <= alpha/4`, with
   the ratio of the bounds tending to `4^d Gamma(d/2+1)/pi^{d/2}`
   (Proposition B.6(a)), and `1/theta` in Theorem 3.4 of [D] contains
   `sqrt(w)`. *Changes:* (R1) is
   redefined as "degree independent of `w`; `C` may depend on `w`"
   (Section B.1); the (QG) remark now says that it is established with `C` of order
   `sqrt(w)`; Conjecture B.5 is restated with `Phi_2` and with `C` allowed
   to depend on `w`; Theorem B.2(c) notes that the refutation of the lower
   half is unaffected. I used both fixes the review offered: the
   redefinition is needed anyway for the (QG) case, and `Phi_2` removes the
   loss on the two worked examples. Whether `C` can be independent of `w`
   with `Phi_2` is stated as open.
3. **Scope of Section A.5, obstacle 1 (moderate). Confirmed.** Step 2 of the
   proof of Proposition A.6 uses that every bag other than `t` has leaves of
   level `<= i` at the alternating point. *Changes:* obstacle 1, a new
   paragraph after Proposition A.6, the Summary, the status table and
   Section D now restrict the statement to level-synchronous refinement.
4. **Slopes versus incumbent in Section C.2 (moderate). Confirmed.** In
   `run_ls.py` the oracle and zero-slope runs start at `x*`, and the `c = 0`
   exact-slope runs at `0 = x*`. *Check:* the new `check_slope_incumbent.py`
   (the note's own `ls_lib`, which now records the incumbent point at the
   start of each pass) reproduces the review's split exactly: slopes alone
   `+7.4, 7.8, 10.3, 25.3%`, incumbent alone `+2.2, 2.0, 6.0, 16.1%`, both
   `+15.2, 14.3, 29.2, 47.9%` (the last equal to the final LS pass, and
   giving the LS sizes 22,559, 25,225, 147,538, 165,598). One pass with
   exact slopes from `x^(-1) = 0` gives 45,491 and 53,506 at `n = 8`, as in
   the review, and 287,423 and 279,384 at `n = 16`. *Changes:* C.1 and C.2
   state the starting points; C.2 has the split table.
5. **RC at `n = 8` (minor to moderate). Confirmed.** In
   `logs/rc_zero_eps1e-6.log`, `l_r = -9.206e-7 >= f* - eps` at rounds 15,
   17, ..., 23, while the incumbent is `1.013e-6`. The rerun with the
   widened intersection test (item 6) is identical. *Changes:* Section A.5,
   C.3, the Summary and Section D say that this failure is due to RC's
   incumbent rule, not to localization.
6. **RC at `n = 16` (minor to moderate). Confirmed that the trajectory is
   not reproducible and the cycle values must not be quoted; the cause is
   different from the one the review gives.** `check_rc_sensitivity.py`
   repeats the review's experiment with the note's code. With the closed
   intersection test, `1e-9` moves of the round-1 centre change `l_r` by up
   to 0.19, but this happens also for the interior coordinate
   `x_6 = -0.9915`, and the pair count changes with the size of the move.
   The cause is rounding: leaf and cell edges that coincide in exact
   arithmetic can differ by one unit, and the closed test then drops the
   pair, which makes `l_r` too high. With the test widened by `1e-12`,
   every move changes `l_r` by less than `1e-9`, and the round-1 bound is
   `-15.725` (first version: `-15.384`). *Changes:* `ls_lib.dp` takes an
   optional `tol` (default 0), and `rc_lib` uses `tol = 1e-12`. LS is not
   affected: the `n = 16` exact-slope run is identical with `tol = 1e-12`
   (size 153,584, `l_r = -5.7944e-7`, split per bag 413.7). All RC runs
   were redone: `c = 0` (`n = 4, 8`) and the local-solve runs give the same
   results as before; the random-`c` runs without a local solve still do not
   converge, now for both seeds and with different numbers. The first
   version's `n = 16` cycle values are withdrawn. Section A.5 and C.3 are
   rewritten.
7. **Theorem A.5(a) (minor). Confirmed.** Part (a) now states the slope
   bound for every pass that runs, and the proofs of (a) and (b) say so. No
   constant changes.
8. **Wording and numbers (minor). Confirmed.**
   - "About `5.8 sqrt(n)`" holds from `n = 32` on (ratios 2.6, 4.0, 5.4, 5.7,
     5.8, recomputed from the note's own numbers); Section A.5 now says so.
   - "About `22 n`" is the maximum over levels. `logs/oracle_eps1e-6.log`
     gives 1,428.3 at level 6 and 1,264.8–1,297.2 at levels 8–12 for
     `n = 64`, and 725.1 at level 6 and 675.9–702.9 at levels 7–11 for
     `n = 32`. The Summary, Sections A.3, A.4, C.1 and the status table now
     say "at most about `22 n`" and give the plateau; the effective `rho` is
     restated as about `2.3 sqrt(n)` (it was rounded up to 2.4). This
     wording missed `25.9 n` at `n = 16`; it was corrected again after the
     confirmation review (item 2 of the next subsection).
   - The processed-count factor "about 20" is restated: 17–24 times the
     final size, and 5.0–6.5 times a single exact-slope pass (C.2:
     6.5, 6.4, 5.0, 5.3). Refined after the confirmation review (item 3 of
     the next subsection).
   - Section B.5, item 3, and the Summary now call the factor 2 per edge a
     loss in the available bound, not a shown thinning of the bands.
   - The first-version RC random log ends after round 21. A correction line
     was appended to that log, and the command table is corrected.
   - Added (from the review, checked in the logs): on the random-`c` runs
     `|x^cons - x*|_inf/s_i` is 3.1–7.2 from level 6 on (Section A.5).
9. **One-sided grid check (minor). Confirmed.** `check_staircase.py` now
   checks every row two-sidedly: the closed-form minimizer satisfies the
   KKT conditions of the strictly convex leaf problem, and the directly
   evaluated relaxed function equals the closed form. Rerun: KKT violation
   0 and value difference at most `2.2e-16` in all 30 rows; all other
   printed numbers are identical to the previous log.

Not changed: the status of every proof marked "proved" in the first
version; Conjecture A.7 and Remark A.8 remain a conjecture and a sketch.

Targeted commands run for this revision (from `adaptive/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`):
`python3 check_slope_incumbent.py 8 1e-4`;
`python3 check_slope_incumbent.py 16 1e-4`;
`python3 check_rc_sensitivity.py 16 0`;
`python3 run_rc.py zero 8 1e-6 23`;
`python3 run_rc.py random 16 1e-4 21`;
`python3 run_rc.py randomlocal 16 1e-4 21`;
`python3 check_staircase.py`;
`python3 check_phi_loss.py`;
and an inline `run_ls` regression with the widened test (item 6). Their
logs are listed in Section E.

### After the confirmation review (round 1)

The confirmation review
([`../reviews/ext-decomposition-adaptive-confirm.md`](../reviews/ext-decomposition-adaptive-confirm.md))
found all nine fixes above correct and listed two minor errors and four
optional wording points (verdict "fixes needed (minor)"). I checked each one
before changing the note. All checks are targeted checks of this note; no
project-wide verification was run and no CI results were consulted.

1. **Level count in Theorem B.2(b) and Proposition B.6(b) (minor).
   Confirmed.** Lemma 3.1 of [D] has `J + 1` levels with
   `J = max(0, ceil(log2(s0/h)))`. The bound `J + 1 <= log2(1/h_0) + 2` used
   in Theorem B.2(b) holds only for `h_0 <= 2`. For `h_0 > 2`, that is
   `alpha^2 K d < eps/2` (allowed when `alpha < 1/(2 sqrt(K d))`),
   `log2(1/h_0) + 2 < 1`. Example: `alpha = 0.1`, `eps = 1/2`, `K = 2`,
   `d = 1` gives `h_0 = 7.07` and `log2(1/h_0) + 2 = -0.82`, so the old size
   bound of Theorem B.2(b) is negative. *Changes:* Theorem B.2(b) and its
   proof use `J + 1`; Proposition B.6(b) uses `L = J + 1` and now proves
   `1 <= L <= (1/2) log2(K d/(2 eps)) + 2`; the status table marks both.
   The proof of Theorem B.2(b) now also says that the central shell cube is
   `[0, min(h_0, 1)]^d`, since for `h_0 > 1` it is clipped to `[0,1]^d`
   (the bound on its relaxed minimum is unchanged).
   *Check:* `check_phi_loss.py` now uses `J + 1` and scans 2,880 cases
   (`alpha` down to `1e-4`, `eps <= 1/2`, `K <= 1024`, `d <= 64`). With
   `L = J + 1` the displayed constant holds in every case (the bound is at
   most 0.31 times it) and the upper bound on `L` holds. With the old `L` it
   fails in 89 cases, all with `h_0 > 4`, by up to a factor 1.36 (the review
   found 27 of 1,120 cases, up to 1.36). The quoted values at `eps = 1e-6`
   are unchanged; at `eps = 1e-2` only the upper bases for `d = 1, 2, 4`
   change in the second or third digit (for example 5.233 to 5.102 at
   `d = 1`), and none of these is quoted. The conclusions (absolute `C`, the
   factor `log(K/eps)`, Theorem B.2(c)) are unaffected. Table C.4 is
   unaffected: `check_staircase.py` builds and counts the shell partitions
   directly.
2. **"At most about `22 n`" (minor). Confirmed.** Recomputed from
   `logs/oracle_eps1e-6.log`: the maxima over levels are `8.8, 19.1, 25.9,
   22.7, 22.3 n` for `n = 4, ..., 64` (`n = 16`: 413.7 at level 5); the
   plateau is `21.0–21.5 n` at `n = 16` and `21.1–22.0 n` at `n = 32`
   (levels 7–11), and `19.8–20.3 n` at `n = 64` (levels 8–12). The
   effective `rho = sqrt(max)/2` is `1.5, 2.2, 2.5, 2.4, 2.4` times
   `sqrt(n)`. *Changes:* the Summary, the status table, Sections A.3, A.4,
   C.1 and D and the command table now say "at most about `26 n` for
   `n <= 64` (`22 n` at `n = 32, 64`)", with the plateau `20–21 n` for
   `n >= 16` and an effective `rho` of at most about `2.5 sqrt(n)`. While
   checking this I found that the bound holds only for the exact-slope runs:
   in the final pass of LS with learned slopes the maximum is
   `10.3, 19.1, 29.3, 22.7 n` for `n = 4, ..., 32` (`logs/scaling_eps1e-4.log`)
   and `19.8, 24.2, 29.2, 45.0 n` in the C.2 runs, reached at level 11 for
   `n = 16`. So the Summary, the status table and Sections A.3 and A.4 now
   say "with exact slopes" and give the learned-slope maxima, and C.1 and
   C.2 describe the rise at the last split levels for `n = 16`. (This
   contrast mixed `c = 0` with random `c`; it was scoped after the second
   confirmation review, item 2 of the next subsection.)
3. **Processed-count ratios (optional). Confirmed.** Recomputed from the
   logs: processed/size is 16.9–23.5 in the C.1 restart table and 15.5–22.8
   in the C.2 LS runs; 3.96–6.21 for single passes; LS over the oracle
   pass 6.52, 6.43, 5.03, 5.33. The oracle pass starts at `x*`, so it also
   has the exact incumbent. *Change:* the paragraph after the second C.1
   table gives both ranges and says that the factor 5.0–6.5 compares with a
   pass that has exact slopes and the exact incumbent, so it is not the cost
   of the restarts alone.
4. **RC wording in Section A.5 (optional). Confirmed.** In
   `logs/rc_zero_eps1e-6_tol.log` (`n = 8`) the centre error is at most
   `10 h_j` up to round 9 and `12–16 h_j` at rounds 10–15; round 14 has
   `f* - l_r = 1.586e-6`, and the cycle `9.206e-7`/`1.544e-6` starts at
   round 15. The new `check_rc_cycle.py` reruns rounds 0–19 (identical
   numbers) and prints the centres: their errors alternate between
   `9.7656e-4` and `1.2207e-3`, and the centres of rounds `j` and `j - 2`
   differ by `3.7e-4, 5.1e-6, 1.5e-6, 4.2e-7` at `j = 16, ..., 19`. So the
   centre does not stop moving; it alternates between two nearly fixed
   points. At `n = 4` RC stops at round 13. *Changes:* the `n = 4` and
   `n = 8` bullets of Section A.5.
5. **Localization range and `N_dec/Psi` (optional). Confirmed.** In the
   final LS pass of `logs/random_n*_eps1e-4.log`, `|x^cons - x*|_inf/s_i` is
   3.11–7.23 from level 6 on and up to 11.01 at levels 3–5. For `c = 0` it
   is 4.0 and 5.0 at `n = 4, 8`, so "about `6 s` for every tested `n`" is
   now "at most `6 s`". (This used the values of levels 8–12 only and was
   wrong at level 4; corrected after the second confirmation review, item 1
   of the next subsection.) For one flat bag and fixed `eps`, the proven lower
   bound on `N_dec/Psi` is `1/(2^d V_d) = Gamma(d/2+1)/(4 pi)^{d/2}`; with
   `lgamma` it is below 1 for `d <= 62` and above 1 from `d = 63`.
   *Changes:* the Summary and the status table add "from level 6 on (up to
   `11 s` at levels 3–5)"; the Summary, Section B.1 and the status table
   state the `w^{Theta(w)}` loss of `Psi` as `eps -> 0`, and the Summary
   gives the fixed-`eps` caveat.
6. **Boundary centres in RC (optional nuance). Confirmed.** In
   `logs/check_rc_sensitivity.log` (widened test), `1e-9` moves of the
   `±1` coordinates change the round-1 pair count from 25,612 to
   25,673–25,718, while interior moves leave it at 25,612, and `l_r` changes
   by less than `1e-9` in all cases. An inline check of the partitions shows
   why: a move of a `±1` coordinate adds sliver boxes of width `1e-9` (for
   coordinates 1, 2, 7, 14: 11,357–11,369 leaves instead of 11,333, and 241
   cells instead of 240). *Change:* the correction paragraph of Section A.5
   now says that the shell partition is discontinuous in a boundary centre,
   as the first review said, and that the jumps of `l_r` come from the
   dropped pairs.

Not changed: the status of every proof; Conjecture A.7 and Remark A.8
remain a conjecture and a sketch. The review's pointer about the closed
intersection test in `../dp_certificate.py` of [D] concerns [D], not this
note; Section D already records it as unchecked, and I did not investigate
it here.

Targeted commands run for this revision (from `adaptive/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`):
`python3 check_phi_loss.py` (modified, rerun; under 1 s);
`python3 check_rc_cycle.py 19` (new; 2 min 11 s);
an inline check of the round-1 RC partition sizes under `1e-9` centre moves
(item 6); inline recomputations from the existing logs (items 2, 3, 5); and
an inline evaluation of `Gamma(d/2+1)/(4 pi)^{d/2}` for `d = 1..79`
(item 5). Their logs, where written, are listed in Section E.

### After the second confirmation review (round 2)

The second confirmation review
([`../reviews/decomposition-adaptive-confirm-r1.md`](../reviews/decomposition-adaptive-confirm-r1.md))
found all six fixes of round 1 correct and listed one minor error (N1), two
optional points and one pre-existing imprecision in the Summary (verdict
"fixes needed (minor)"). I checked each one before changing the note. All
checks are targeted checks of this note; no project-wide verification was
run and no CI results were consulted.

1. **"At most `6 s`" at `c = 0` (N1, minor). Confirmed.** Recomputed from
   `logs/oracle_eps1e-6.log` (exact slopes) with `s_i = 2^{1-i}`:
   `|x^cons - x*|_inf/s_i` is 8.00 at level 4 for `n = 16, 32, 64` (the
   consistent point has a coordinate at `±1`), 3.99–6.02 from level 5 on,
   and at most 4 at levels 1–3. In `logs/scaling_eps1e-4.log` (learned
   slopes, `c = 0`) it is also 8.00 at level 4 for `n = 16, 32`, and 11.98 at
   the stopping sublevel 11 of `n = 4`. The new `check_localization.py`
   reruns these runs with the note's code (all sizes equal the logs) and
   prints the ratio at full precision: from level 5 on it is exactly 4, 5,
   6, 6, 6 with exact slopes (5.98–6.02 is rounding in the log), and 8 at
   level 4 for `n >= 16`. It also prints the leaf levels of the minimizing
   configuration. They equal the sublevel everywhere except at the stopping
   sublevel 11 of the learned-slope run at `n = 4`: there all its leaves
   have level 10, so the ratio `12 s_11` is `6 s_10`. *Changes:* the Summary
   and the status table now say "in the exact-slope runs with `c = 0`, at
   most `6 s` from level 5 on (`8 s` at level 4 for `n >= 16`)", as the
   review suggested. Section A.5 (obstacle 2) gives the level range, the
   level-4 values, the learned-slope values and the stopping case; the C.1
   localization bullet gives the level range, the full-precision values and
   the values at levels 1–4. Item 5 of the previous subsection has a
   pointer. *Related change.* The stopping case showed a defect in the
   statement of Conjecture A.7: at a sublevel with no live box, "all live
   boxes have side `<= s`" holds for every `s`, so the statement forced
   `x^cons = x*` there, which fails at every stopping sublevel of the runs. The conjecture now requires
   a live box. Then every box of a minimizing configuration has
   min-marginal `l_r < UBD - eps`, so it is live and has side `<= s`. The
   status table marks this. No conclusion changes.
2. **Exact against learned slopes (optional). Confirmed.** In
   `logs/random_n16_eps1e-4.log` the oracle runs (random `c`, exact slopes
   and exact incumbent) split 445.8 and 434.5 leaves per bag at level 5,
   that is `27.86 n` and `27.16 n`, above the `c = 0` maximum of `25.9 n`.
   The `45 n` comes from LS, which learns the slopes and the incumbent.
   *Changes:* the status table (Proposition A.6 row) and the paragraph after
   the proof of Proposition A.6 now say that `26 n` is for the family itself
   (`c = 0`) and give, at `n = 16`, `29 n` with learned slopes at `c = 0`,
   and `27–28 n` (exact slopes) against `29–45 n` (LS) with random `c`. The
   Summary was already scoped to `c = 0`; it now also gives the random-`c`
   exact-slope value. Sections A.3 and D now say `c = 0` where they quote
   the exact-slope maximum. Item 2 of the previous subsection has a pointer.
3. **`N_dec/Psi` for fixed `eps` (optional). Confirmed.** For one flat bag,
   `Psi(eps) = ceil(u)^d` with `u = sqrt(alpha/eps)` (only one allocation;
   the supremum over `eta` is at `eta = 0`), and the lower bound
   `N_dec >= (alpha/eps)^{d/2}/V_d` uses no bound on `eps`. So
   `N_dec/Psi >= (u/ceil(u))^d/V_d >= 1/(2^d V_d) = Gamma(d/2+1)/(4 pi)^{d/2}`
   for every `eps <= alpha`. With `Gamma(d/2+1) >= (d/(2e))^{d/2}` this is at
   least `(d/(8 pi e))^{d/2}`, so it is of order `w^{Theta(w)}`. Evaluated
   with `lgamma`: below 1 for `d <= 62`, 1.10 at `d = 63`, `8.8e3` at
   `d = 80`, `9.3e15` at `d = 120`. *Changes:* Proposition B.6(a) states this
   bound, and its proof gives the value of `Psi`; the Summary, Section B.1
   and the status table state the order for every `eps <= alpha`, with the
   threshold `d >= 63` as the only caveat.
4. **Summary form of Theorem B.2(b) (pre-existing). Confirmed.** The shell
   term of Theorem B.2(b) is `2 (J + 1)(4/theta)^d` with
   `4/theta < max(8, 4 sqrt(alpha d))`, so its base grows like
   `sqrt(alpha d)`. An inline evaluation of the bound of Theorem B.2(b)
   reproduces the review's example: `alpha = 1`, `eps = 1/2`, `d = 1024`
   gives `4/theta = 64`, a fat-slice base of 32 and
   `(alpha d/eps)^{1/2} = 45.25`; at `d = 4096` the numbers are 128, 64 and
   90.51. Over 720 cases (`alpha` from 1 to `1e-4`, `eps` from 1 to `1e-6`,
   `K` from 2 to 1024, `d` from 1 to 4096), the old form
   `K ((alpha d/eps)^{d/2} + C^d log2(K/eps))` with `C = 16` is below the
   bound in 103 cases, by factors up to `2^6807`. The corrected form
   `K ((alpha d/eps)^{d/2} + (16 max(1, sqrt(alpha d)))^d log2(K/eps))` is
   above it in every case (the bound is at most 0.69 times it). Why the
   corrected form holds:
   `ceil(v) <= sqrt(2) v` for `v >= 2.42` and `ceil(v) <= 3` otherwise
   (`v = sqrt(alpha d/(2 eps))`); `4/theta <= 8 max(1, sqrt(alpha d))`; and
   `J + 1 <= (1/2) log2(K d/(2 eps)) + 2` (Proposition B.6(b)), where the
   factor from `log d` is absorbed into `C^d`. *Change:* the Summary bullet
   now reads `O(K ((alpha d/eps)^{d/2} + (C max(1, sqrt(alpha d)))^d log(K/eps)))`
   with an absolute constant `C`, and the status table notes the
   correction. Theorem B.2 itself, Theorem B.2(c) (fixed
   `d`) and Proposition B.6(b) (which uses `max(8, 4 sqrt(alpha d))`
   explicitly) are unaffected.

Not changed: the status of every proof; Remark A.8 remains a sketch, and
Conjecture A.7 remains a conjecture (its hypothesis is clarified, item 1).

Targeted commands run for this revision (from `adaptive/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`):
`python3 check_localization.py 64 32` (new; 3 min 54 s), preceded by the
same computation run once inline with a patched copy of `ls_lib.dp` (same
numbers); inline recomputations from `logs/oracle_eps1e-6.log`,
`logs/scaling_eps1e-4.log` and `logs/random_n*_eps1e-4.log` (items 1, 2);
an inline evaluation of `Gamma(d/2+1)/(4 pi)^{d/2}` for `d = 1..199`
(item 3); and an inline evaluation of the size bound of Theorem B.2(b)
against the old and corrected Summary forms (item 4). Their logs, where
written, are listed in Section E.

*Root edit (2026-09-30), from `reviews/decomposition-adaptive-confirm-r2.md`:*
the `29 n` value at `n = 16` (`c = 0`) comes from LS, which learns both
slopes and incumbent (and uses `eps = 1e-4`), so it is not attributed to the
slopes alone; wording changed in the Summary and after Proposition A.6. The
random-`c` exact-slope value 27–28 n appears in A.4, the status table and
Sections E–F (C.2 gives only the oracle sizes). No number changed.

*Root edit (2026-09-30, closing revision):* the header now cites the third
confirmation review (`reviews/decomposition-adaptive-confirm-r2.md`,
verdict "verified"). No text of the results changed.
