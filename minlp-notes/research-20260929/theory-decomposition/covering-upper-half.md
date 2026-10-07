# The upper half of the covering characterization for one-dimensional separators: graded exact splits

Date: 2026-09-30. Extension of Part B of
[`extension-adaptive.md`](extension-adaptive.md) (Section B.5, Conjecture B.5).
Status: **revised after two review rounds**
([`../reviews/covering-upper-half-review.md`](../reviews/covering-upper-half-review.md)
and the confirmation review
[`../reviews/covering-upper-half-confirm-r1.md`](../reviews/covering-upper-half-confirm-r1.md));
the second revision was confirmed by
[`../reviews/covering-upper-half-confirm-r2.md`](../reviews/covering-upper-half-confirm-r2.md)
(verdict: verified; four trivial or optional items, applied by the root,
see "Root edits after the round-2 confirmation" at the end). The changes are listed in
"Revision after review" at the end. Proofs are complete where the status
table says "proved". Computations are floating-point illustrations on
grids, not certified values. Scripts and logs are in
[`covering/`](covering/).

Cited notes:

- [D] [`decomposition-certificates.md`](decomposition-certificates.md)
  (Definition 1.2, Lemmas 1.1, 1.3–1.5, Theorems 2.5, 3.4, Conjecture 3.7);
- [E] [`extension-adaptive.md`](extension-adaptive.md) (Theorems B.2, B.3,
  Propositions B.4, B.6, Section B.5, Conjecture B.5);
- [K] [`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
  (Theorem 2.1 band identity, Proposition 2.3, Theorem 3.1 tree sandwich,
  Proposition 3.3, Corollary 3.4, Lemmas 4.1, 4.2, Proposition 5.4);
- [C] [`../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`](../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md)
  (Section 1.1: `a_i >= d_i^2`; cited as [C] in [D]; added in revision
  round 2);
- the reviews [`../reviews/decomposition-adaptive-review.md`](../reviews/decomposition-adaptive-review.md)
  (Section B.5 item 3, `Phi_2`), [`../reviews/ext-decomposition-adaptive-confirm.md`](../reviews/ext-decomposition-adaptive-confirm.md),
  [`../reviews/consistency-review.md`](../reviews/consistency-review.md).

## Summary

**Question.** Section B.5 of [E] proves the upper half of the covering
characterization for *one* one-dimensional separator with exact bag minima
(Proposition B.4: cells `<= 1 + 3J sup_eta N_inf(pi_S E(eta), 2 sqrt((eps+eta)/M))`).
It could not extend this to paths. Per-edge band distances do not control
the gap in general ([K], Proposition 3.3). The tree sandwich of [K] (Theorem 3.1) measures
errors in sup norm over the whole separator and so does not localize to
the near-optimal set. Applying Proposition B.4 edge by edge would need
"band stability" of the reduced problems, which was neither proved nor
refuted. The task was to settle the upper half for paths with
one-dimensional separators (and trees if possible), or to show why it
fails.

**Answer in the exact-bag model (the model of Proposition B.4): settled
positively for trees with one-dimensional separators.** The number of
separator cells is at most `O(|T| log)` times the per-separator covering
numbers. The proof does not use band stability. It uses a new joint exact
split.

1. **Exact pointwise form (Lemma 0, proved; elementary).** For every split
   `phi` on a tree, `gap(phi) = sup_x [ sum_e delta_e(x_{S_e}) - m(x) ]`.
   Here `delta_e >= 0` is the one-sided error of `phi_e` below the
   *reduced* value function of edge `e`, which depends on the splits chosen
   further down. With relaxed bags the bag errors join the sum. So a split
   relaxation certifies `eps` exactly when all these errors together are
   *admissible*, in the sense of Theorem B.3 of [E] but imposed on all
   of `X`. The difficulty of B.5 is that
   `delta_e` is measured against reduced, not original, value functions.
2. **Graded exact splits and a margin-discounted sandwich (Theorem 1,
   proved; any tree, any separator dimension).** Put
   `theta_e = (2E_e + 1)/(2n)`, where `n` is the number of edges and `E_e`
   the number of edges below `e`. Then the split
   `psi_e = (1 - theta_e) U_e + theta_e L_e` is exact. For every
   perturbation `r`,
   `gap(psi + r) <= sum_e [ sup(r_e - w_e/(2n)) + sup(-r_e - w_e/(2n)) ]`.
   This is the tree sandwich of [K] with the sup-norm error replaced by an
   error discounted by `w_e/(2n)`, where `w_e` is the separator margin.
   Errors are free where the band is wide, as for one separator; the price
   is the factor `1/(2n)`. For `n = 1` it is the band identity. The ordering
   of `theta` matters: reversed grading is not exact in 155 of 161 random
   paths. The factor `1/(2n)` is optimal for bounds of this form: on the
   chain of copies, no split at all admits a discount `c w_e` with
   `c > 1/(2n)` (Proposition 1.3, proved after review).
   Theorem 1' adds bag relaxation errors, discounted by the bag-projection
   margin. Lemma 1' extends it to leafwise relaxations, as used for
   certificates.
3. **Kink concentration (Lemma 2, proved; one dimension).** Let `U` be
   `M`-semiconcave and `L` `M`-semiconvex with `L <= U`. Then the total
   slope drop of `U - M s^2/2`, plus the slope rise of `L + M s^2/2`, on
   `[c - h/2, c + h/2]` is at most `4 w(c)/h + 4 M h`. Neither constant 4
   can be lowered. So concave kinks of
   the value functions can occur only where the band is wide, in a
   quantified way. This is a quantitative one-dimensional form of the
   pinch-regularity Lemma 4.2 of [K]. *(Sharpened in revision round 2.
   Earlier versions proved `8 w(c)/h + 8 M h`. Section 4 still uses that
   weaker form, so rule R3 and its computations are unchanged. With the
   constants 4, Theorem 3's constants roughly halve; this is a sketch.)*
4. **Upper half, exact-bag model (Theorem 3, proved; trees with
   one-dimensional separators).** An explicit dyadic rule gives
   cellwise-affine splits with `gap <= eps` and
   `|P_e| <= 1 + (8n + 2) J_e sup_eta N_inf(pi_{S_e} E(eta), 2 sqrt((eps + eta)/M_e)) + 8n J'_e`
   cells on every separator. `J_e, J'_e` are logarithms (Section 4). The
   only hypotheses are semiconcavity of `U_e` and semiconvexity of `L_e`
   (automatic for `C^{1,1}` box data, [K] Lemma 4.1) and Lipschitz value
   functions. Kinks anywhere are allowed. No quadratic growth and no
   hypothesis on copy errors are needed. The power of `|T|` is 1 per
   separator, independent of anything else. The bound-driven rule `bd`
   (refine while the Theorem 1 cell bracket exceeds `eps/n`) refines a
   coarsening of R3's partition, so the same count bound applies to it
   (Corollary 3.2). Under the hypotheses of Theorem 2.5 of [D], with each
   separator among its child bag's gap coordinates, `sum_e N_e` is at most
   `2 ceil(sqrt(M/alpha)/2) N_dec(eps) <= (sqrt(M/alpha) + 2) N_dec(eps)`
   (Corollary 3.3; before revision round 2 the factor was
   `ceil(sqrt(M/alpha)) 2^{w+1}`).
5. **Cell placement by one-edge band brackets fails (Proposition 4,
   proved).** Take two edges with root `2 beta s1^2`, middle bag
   `kappa (s1 - s2)^2 - beta s2^2` and leaf `2 beta s2^2`
   (`kappa >= 2 beta`). Both bands contain the constant 0. Yet
   `gap(Aff) = beta`. So every rule that refines an edge only while its own
   *band bracket* exceeds a tolerance stops at one cell per edge and never
   certifies better than `beta`. On grid path instances with flat valleys
   and kinks (`n = 4, 6, 8`, `eps = 1e-3`, grid `m = 257`), the
   LP-optimal gap over *all* cellwise-affine splits on such cells is
   `2.5e-3`, `1.27e-2` and `2.29e-2`, and it barely changes when the
   per-edge tolerance is lowered from `eps/n` to `eps/n^2`. The failure lies
   in the placement *criterion*. It is not a failure of deciding placement
   edge by edge, and not a failure of the values: the LP already chooses
   the best joint values on these cells. Rule R3 decides the cells of edge
   `e` from `w_e`, `M_e`, `G_e`, `n` and `eps` alone and provably works
   (Theorem 3). So does `bd` (Theorem 1(c) and Corollary 3.2). Proposition
   B.4's rule `M r^2 - min w > eps/n`, applied edge by edge, reached the
   tolerance on every tested instance; whether it always does is open.
   *(Corrected after review: the first version called this "per-edge
   control of cell placement fails" and concluded that "a joint exact split
   is needed, not only a joint choice of values on per-edge cells". Both
   statements were wrong as worded; see Revision R2.)*
6. **Decomposition certificates (Definition 1.2 of [D]): partial.**
   Proposition 5 shows that a certificate whose leaves are aligned with the
   cells is exactly a split relaxation of the leafwise-relaxed bag
   functions, provided (LC) and (CM) are imposed only for pairs whose
   interiors meet (valid by the "touching pairs" remark in Section 1.4 of
   [D]). Lemma 1' (the leafwise form of Theorem 1') then gives a
   sufficient condition. In it the cell minorants use the slopes of the
   cell-bracket minimizers, and each
   bag's relaxation error is paid by a constant share of `eps` plus
   `W_t/(3n+1)`, where `W_t` is the bag-projection margin. A condition on
   the slopes is needed: with constant minorants the conclusion fails
   (revision round 2, Section 6). By a sketch,
   this gives leaf counts of the equal-share type (`|T|^{(w+1)/2}`,
   reading (R2)), plus a product term from the alignment. The upper half of Conjecture
   B.5 in reading (R1) for certificates remains **open**. Lemma 0
   identifies the missing step: realize a pointwise bag allocation (as the
   staircase certificate of Theorem B.2 does with exact fixing) while
   keeping the reduced separator errors admissible. Lemma 2 does not apply
   to the relaxed bag functions, because they jump at leaf boundaries.

**Numerical checks (Section 7).** They cover:

- Theorem 1 on 400 random finite trees and paths with 10,000
  perturbations: no violation. The bound is often nearly tight (median
  ratio gap/bound 0.89).
- Theorem 1' (600 checks) and Lemma 0 (200 instances, identity to
  `4e-15`).
- Proposition 1.3: on the chain of copies, an LP over all splits gives the
  largest `c` for which some split stays exact under both perturbation
  patterns `± c a` as exactly `1/(2n)`, for `n = 2, 3, 4, 6, 8`. With one
  pattern it gives `1/n`.
- Lemma 2 in its sharp form `4 w(c)/h + 4 M h`: explicit families come
  within a ratio of `0.999995`–`0.999998` of it for every tested `(w(c), M, h)`,
  including `w(c) = 0` and `M = 0`. An LP over all convex piecewise-linear
  functions on grids stays below it (ratio up to `0.9961`). Random
  semiconcave/semiconvex pairs (60,000 cases) reach only 0.55 of it.
  *(Corrected twice. The first version said that the constant 8 was "loose
  by about 4". Round 1 said "at most a factor 2 too large", on the basis of a
  two-kink family that approaches, but does not reach, half of
  `8 w(c)/h + 8 M h`. Round 2 proves the sharp constants 4 and 4.)*
- The rule of Theorem 3 on four grid path families (`n = 3, 6`,
  `m = 16385` grid points): `gap <= 1e-7` in every run. The cells number
  1.7–3.5 times `n J_e N_e`, well inside the proven `(8n + 2) J_e N_e`
  (plus boundary terms).
- The bound-driven rule `bd` uses 0.7–2.2 cells per unit of covering
  number, and its partition coarsens R3's on every run. The sup-norm
  sandwich needs 2.6–22 times more cells than `bd`.
- Proposition 5's slope condition (added in revision round 2): on the
  confirmation review's `n = 1` example, constant minorants on R3-adapted
  cells miss `eps` by factors 1.6–280. The prescribed slopes stay within
  `eps/2`.

**Significance and novelty.** The graded split (Theorem 1) is what B.5
lacked: an exact split around which the error on each edge is discounted
by that edge's own separator margin, at the price of a factor `1/(2n)`.
For bounds of this form the factor cannot be improved in general
(Proposition 1.3).
With the one-dimensional kink bound, it settles the separator (copy-error)
part of the covering characterization for one-dimensional separators on
trees. The certificate-model question in reading (R1) remains open. All
arguments are elementary. Mixing forward and backward dynamic-programming
messages is standard in graphical models (see, for example, Ruozzi and
Tatikonda on reparametrizations and splittings), and convex combinations of
exact splits are exact. I did not find the monotone grading, the discounted
sandwich or the kink-concentration bound in short searches (Section 8).
That does not establish novelty.

## Status

| Item | Content | Status |
|---|---|---|
| Lemma 0 | `gap(phi) = sup_x [sum_e delta_e - m]` (reduced one-sided errors); relaxed bags add `sum_t err_t` | proved; checked numerically (200 trees, error `4e-15`) |
| Theorem 1 | graded split `theta_e = (2E_e+1)/(2n)` is exact; `gap(psi + r) <= sum_e [sup(r_e - w_e/2n) + sup(-r_e - w_e/2n)]`; cellwise form | proved (trees, any separator dimension); no violation in 10,000 random checks |
| Theorem 1' | with bag errors: discount `1/(3n+1)` on separators and on the bag-projection margin `W_t` | proved; no violation in 600 checks |
| Lemma 1' | Theorem 1' for leafwise relaxations (leaf-dependent errors, cell pieces used on closed cells) | proved (added after review) |
| Remark 1.2 | reversed grading not exact; discount `c > 1/(2n)` fails for the graded split | computed |
| Proposition 1.3 | a bound of the form (b) with discount `c w_e` around any split forces `2c sum_e w_e(x_{S_e}) <= m(x)`; on the chain of copies `c <= 1/(2n)` for every split | proved (added after review; replaces a sketch that gave only `c <= 1/n`); LP gives exactly `1/(2n)` for `n = 2, 3, 4, 6, 8` |
| Lemma 2 | `Delta_U + Delta_L <= 4 w(c)/h + 4 M h` on `[c-h/2, c+h/2]` (one dimension); neither constant 4 can be lowered | proved (sharp form added in revision round 2; earlier versions had `8 w(c)/h + 8 M h`, which Section 4 still uses); explicit families reach ratio `0.999995`–`0.999998`, an LP over grid-convex functions stays below the bound |
| Theorem 3 | exact-bag model, trees with 1D separators: `|P_e| <= 1 + (8n+2) J_e N_e + 8n J'_e`, `gap <= eps` | proved; the rule gives `gap <= 1e-7` and 1.7–3.5 times `n J_e N_e` cells in all runs |
| Corollary 3.2 | `bd`'s partition coarsens R3's, so Theorem 3's count applies to `bd` | proved (added after review); coarsening and `g <= B` hold on all 47,782 tested cells |
| Corollary 3.3 | `sum_e N_e <= 2 ceil(sqrt(M/alpha)/2) N_dec(eps)` if `S_t ⊂ K_t` for every non-root bag | proved (added after review, from the review's sketch; factor `2^{w+1}` removed in revision round 2) |
| Proposition 4 | both bands contain 0 but `gap(Aff) = beta`; rules driven by one-edge band brackets never refine | proved; LP plateaus `1.1e-2`–`1.3e-2` (`n = 6`) and `2.3e-2`–`2.5e-2` (`n = 8`) at both tolerances |
| Proposition 5 | aligned certificates (checks only for pairs whose interiors meet) = split relaxation of the leafwise-relaxed bags; sufficient condition via Lemma 1', with the cell slopes of the bracket minimizers | proved (validity and equality; slope clause added in revision round 2, without it the condition fails); size estimate is a sketch |
| Upper half of Conjecture B.5, certificates, reading (R1) | | open |

## 0. Setting

Notation of [K], Section 0, and [D], Section 1.

- `X` is a box, `(T, {V_t})` a rooted tree decomposition with root `r`,
  bag functions `F_t` bounded (continuous where stated), `F = sum_t F_t`,
  `f* = inf F`, `m = F - f*`, `E(eta) = {m <= eta}`.
- Every non-root bag `t` has the separator `S_t = V_t ∩ V_{p(t)}` of its
  edge `e(t)` to the parent. Edges and non-root bags are identified. `n` is
  the number of edges (`|T| = n + 1`), and `E_t` is the number of edges
  inside `sub(t)` (so `E_t = 0` for a leaf).
- Value functions of edge `t`: `U_t(s) = inf {sum_{u in sub(t)} F_u : x_{S_t} = s}`
  (child side), `V_t(s)` the same over the other bags, `L_t = f* - V_t`,
  `w_t = U_t - L_t`. Then `w_t(s) = inf {m(x) : x_{S_t} = s} >= 0` and
  `{w_t <= eta} = pi_{S_t}(E(eta))` when infima are attained.
- The **bag-projection margin** is `W_t(z) = inf {m(x) : x_{V_t} = z}` for
  `z in X_{V_t}`.
- The **DP margin** (Lemma 1.1 of [D]):
  `g_t(z) = F_t(z) + sum_{u in ch(t)} U_u(z_{S_u}) - U_t(z_{S_t}) >= 0` for
  `t != r`, and `g_r(z) = F_r(z) + sum_{u in ch(r)} U_u(z_{S_u}) - f*`.
- **Splits.** `phi = (phi_t)_{t != r}` gives
  `F_t^phi = F_t + sum_{u in ch(t)} phi_u(x_{S_u}) - phi_t(x_{S_t})`,
  `rho(phi) = sum_t inf F_t^phi <= f*`, and `gap(phi) = f* - rho(phi)`. For
  a class `Phi = prod_t Phi_t`, `gap(Phi) = inf_{phi in Phi} gap(phi)`.
- **Cellwise-affine class `PA(P)`.** For a one-dimensional separator with
  range `I_t` and a partition `P_t` of `I_t` into intervals, `PA(P_t)` is the
  set of functions that are affine on each cell. It is the class of
  Proposition B.4 of [E] and of Section 5.3 of [K].
- "**Exact-bag model**" means `rho` with exact bag infima, as in [K] and
  Proposition B.4 of [E]. It counts separator cells only. Decomposition
  certificates, which also relax bags, are treated in Section 6.
- *Notation (revision round 2).* `L_t` always denotes the lower value
  function. The leaf family of bag `t` in a certificate is `Leaves_t`
  (written `L_t` in [D]). The discounts are `tau = 1/(2n)` (Theorem 1) and
  `tau' = 1/(3n+1)` (Theorem 1'). In formulas, `D` denotes a cell only.

Two facts used below.

- (F1) `W_t(z) = w_t(z_{S_t}) + g_t(z)` for `t != r`, and
  `W_r(z) = g_r(z)`. *Proof.* With `x_{V_t} = z` fixed, running
  intersection splits the problem into bag `t`, the subtrees of the children
  (which see only `z_{S_u}`) and the bags outside `sub(t)` (which see only
  `z_{S_t}`). So
  `W_t(z) = V_t(z_{S_t}) + F_t(z) + sum_{u in ch(t)} U_u(z_{S_u}) - f*`,
  which is `(U_t + V_t - f*)(z_{S_t}) + g_t(z)`. □
- (F2) `W_t(z) >= w_u(z_{S_u})` for every child `u`, and
  `W_t(z) >= w_t(z_{S_t})`, because `{x_{V_t} = z}` lies in both
  `{x_{S_u} = z_{S_u}}` and `{x_{S_t} = z_{S_t}}`.

## 1. The exact pointwise form of the split gap

**Lemma 0.** Let `phi` be any split with bounded components. Define bottom
up, for `t != r`, the **reduced value function**

```
U_t^phi(s) = inf { F_t(z) + sum_{u in ch(t)} phi_u(z_{S_u}) : z in X_{V_t}, z_{S_t} = s },
c_t = inf_s (U_t^phi - phi_t)(s),      delta_t = U_t^phi - phi_t - c_t >= 0.
```

Then `rho(phi) = inf_x [ F(x) - sum_{t != r} delta_t(x_{S_t}) ]`, so

```
gap(phi) = sup_x [ sum_{t != r} delta_t(x_{S_t}) - m(x) ].
```

If each `F_t` is replaced by a relaxed bag function `F~_t = F_t - err_t`
(`err_t >= 0`), and `delta~` is defined with `F~`, then
`f* - rho~(phi) = sup_x [ sum_t err_t(x_{V_t}) + sum_{t != r} delta~_t(x_{S_t}) - m(x) ]`.

*Proof.* The infimum of bag `t != r` is
`inf_z [F_t + sum_{u in ch(t)} phi_u - phi_t] = inf_s (U_t^phi - phi_t) = c_t`.
Let `Ubar_t(s)` be the infimum over `sub(t)` with `x_{S_t} = s` of
`sum_{u in sub(t)} F_u - sum_{u in sub(t), u != t} delta_u(x_{S_u})`.
Induction from the leaves gives `U_t^phi = Ubar_t - sum_{u in sub(t), u != t} c_u`:
substitute `phi_u = U_u^phi - delta_u - c_u` for the children. The root
infimum is then
`inf_x [F(x) - sum_{t != r} delta_t(x_{S_t})] - sum_{t != r} c_t`. Adding
the `c_t` of the other bags gives the formula for `rho`. The relaxed case
is the same computation with `F~`, and `F~ = F - sum_t err_t`. □

*Remarks.*

- For one edge, `U^phi = U` and `sup_s [delta(s) - w(s)] = sup(phi - U) + sup(L - phi)`:
  Lemma 0 is the band identity (Theorem 2.1 of [K]).
- Lemma 0 is the sufficiency counterpart of Theorem B.3 of [E]. There the
  leaf errors of any certificate were shown to be admissible,
  `sum_t e_t <= eps + eta` on `E(eta)`, by the chain inequality (Lemma 1.4
  of [D]). Here, for split relaxations, admissibility of the bag errors
  together with the separator errors `delta~` is also sufficient.
- The obstacle of Section B.5 of [E] is visible in the formula. `delta_t`
  is the error of `phi_t` against the *reduced* function `U_t^phi`, which
  depends on the choices below `t`. A choice inside the original band of
  one edge can make `U_t^phi` of the next edge lose all affine band
  elements (Proposition 4).
- Lemma 0 is elementary and close to the reparametrization view of
  min-sum problems on trees. It is stated here because the rest of the note
  uses it as the exact target.

## 2. Graded exact splits and the margin-discounted sandwich

**Theorem 1.** Let the `F_t` be bounded. For `t != r` put

```
theta_t = (2 E_t + 1)/(2n),     psi_t = (1 - theta_t) U_t + theta_t L_t = U_t - theta_t w_t.
```

(a) `psi` is an exact split: `rho(psi) = f*`.

(b) For all bounded `r = (r_t)`,

```
gap(psi + r) <= sum_{t != r} [ sup (r_t - w_t/(2n)) + sup (-r_t - w_t/(2n)) ].
```

(c) Let `Phi_t` be linear spaces containing the constants, and let
`Sliver_t = {sigma : |sigma - psi_t| <= w_t/(2n)}`, which lies in `Band_t`.
Then `gap(Phi) <= 2 sum_t dist_inf(Phi_t, Sliver_t)`. For cellwise classes
`Phi_t = {sum_D 1_D phi_D : phi_D in Phi_{t,D}}` on partitions `P_t`,

```
gap(Phi) <= sum_{t != r} max_{D in P_t} g_{t,D},
g_{t,D} = inf_{phi_D in Phi_{t,D}} [ sup_D (phi_D - psi_t - w_t/(2n)) + sup_D (psi_t - w_t/(2n) - phi_D) ].
```

*Proof.* Write `phi_t = U_t - eps_t` for an arbitrary split.

*Step 1 (exact per-bag decomposition).* For `t != r`,
`F_t^phi = g_t - sum_{u in ch(t)} eps_u + eps_t` and
`F_r^phi = f* + g_r - sum_{u in ch(r)} eps_u`. Hence
`gap(phi) = sum_t Def_t` with

```
Def_t = sup_z [ sum_{u in ch(t)} eps_u(z_{S_u}) - eps_t(z_{S_t}) - g_t(z) ]      (no eps_t term at the root).
```

*Step 2.* Let `eps_t = theta_t w_t - r_t` and `tau = 1/(2n)`. By (F1),
`-g_t = w_t - W_t` for `t != r` (and `-g_r = -W_r`). So for `t != r`

```
Def_t = sup_z [ sum_{u in ch(t)} (-r_u - tau w_u) + (r_t - tau w_t)
               + sum_{u in ch(t)} (theta_u + tau) w_u + (1 - theta_t + tau) w_t - W_t ].
```

The coefficients in the second line are nonnegative, and each `w` there is
at most `W_t` by (F2). So the second line is at most
`[sum_{u in ch(t)} (theta_u + tau) + tau - theta_t] W_t`. This is zero, because
`E_t = sum_{u in ch(t)} (E_u + 1)` gives
`theta_t = sum_{u in ch(t)} (theta_u + tau) + tau`. At the root the second line is
`sum_{u in ch(r)} (theta_u + tau) w_u - W_r`, and
`sum_{u in ch(r)} (theta_u + tau) = tau sum_{u in ch(r)} (2E_u + 2) = 2n tau = 1`.
So

```
Def_t <= sum_{u in ch(t)} sup (-r_u - tau w_u) + sup (r_t - tau w_t)       (no last term at the root).
```

Summing over `t`, every edge `u` appears once as a child and once as the
parent separator of `u`. This gives (b).

*(a)* Take `r = 0`: the bound is `sum_t 2 sup(-tau w_t) <= 0`, and
`gap >= 0` always.

*(c)* For `sigma in Sliver_t` and `phi_t in Phi_t`, the bracket of edge `t`
in (b) with `r_t = phi_t - psi_t` is at most `osc(phi_t - sigma)`. Shifting
`phi_t` by a constant gives `2 dist(sigma, Phi_t)`. For cellwise classes,
choose on each cell a near-optimal `phi_D` and shift it by a constant so
that both suprema on `D` equal `g_{t,D}/2`. Then the bracket of edge `t` is
at most `max_D g_{t,D}`, as in Proposition 2.3 of [K]. Also
`psi_t ± w_t/(2n)` lies in `[L_t, U_t]` because `tau <= theta_t <= 1 - tau`. □

*Remarks 1.1.*

- **Relation to the tree sandwich of [K].** Theorem 3.1 of [K] gives
  `2 max_e dist(Phi_e, Band_e) <= gap <= 2 inf_{psi exact} sum_e dist(psi_e, Phi_e)`.
  Theorem 1 replaces the upper end, for the graded split, by the distance
  to the sliver of half-width `w_e/(2n)`. Errors are therefore discounted
  where the band is wide, which the sup-norm distance to one exact split
  cannot do. This is the localization Section B.5 of [E] was missing (its
  item 2).
- **n = 1.** `theta = 1/2`, the sliver is the band, and (b) is the band
  identity.
- **Why grading.** The set of exact splits is convex, because `rho` is
  concave. On a path, `L` is the DP split for the reversed root, so every
  convex combination of `U` and `L` with a *common* weight is exact. On a
  tree with branching, `L` itself need not be exact (a bag with several
  children can have `sum_u w_u > W_t`); it was not exact in any of 238
  random branching trees (check (i), Section 7.1). Theorem 1(a) is what
  guarantees exactness of the graded split. The grading makes the weight
  decrease from the root to the leaves: from edge `t` to a child edge `u`
  it drops by `(E_t - E_u)/n >= 1/n`, with equality on paths. That keeps
  `1/(2n)` of every edge's band free on each side.

**Theorem 1' (bag relaxation errors).** Let `F~_t = F_t - err_t` with
`err_t >= 0`, and write `rho~` for the split relaxation of the `F~_t`. Put
`tau' = 1/(3n + 1)`, `theta'_t = (3E_t + 2) tau'` and
`psi'_t = U_t - theta'_t w_t`, where `U`, `w` are those of the original `F`.
Then for all `r`

```
f* - rho~(psi' + r) <= sum_{t != r} [ sup (r_t - tau' w_t) + sup (-r_t - tau' w_t) ] + sum_t sup_z [ err_t(z) - tau' W_t(z) ].
```

*Proof.* In Step 1 the bag term gains `+ err_t(z)`. In Step 2, add and
subtract `tau' W_t`. The coefficient of `W_t` becomes
`sum_{u in ch(t)} (theta'_u + tau') + tau' + tau' - theta'_t = 0` for
`t != r`, and `sum_{u in ch(r)} (theta'_u + tau') + tau' - 1 = 3n tau' + tau' - 1 = 0`
at the root. At a leaf, `theta'_t = 2 tau'` covers `tau' w_t` and `tau' W_t`. □

**Lemma 1' (leafwise form of Theorem 1'; added after review).** For each
bag `t` let `Leaves_t` be a finite family of boxes (leaves) covering `X_{V_t}`,
and for each leaf `B` let `err_{t,B} >= 0` be a bounded function on `B`.
For each edge `e` let `P_e` be a partition of `I_e` into intervals, and for
each cell `D in P_e` let `phi_{e,D}` be a bounded function on the closed
cell `cl D`. Assume alignment: for every leaf `B` of bag `t` and every
separator `S_u` of `t` (its own, `u = t`, and its children's), `B_{S_u}`
lies in `cl D_u(B)` for a chosen cell `D_u(B) in P_u`. Define the leafwise
relaxation

```
rho~(phi) = sum_t inf_{B in Leaves_t} inf_{z in B} [ F_t(z) - err_{t,B}(z) + sum_{u in ch(t)} phi_{u,D_u(B)}(z_{S_u}) - phi_{t,D_t(B)}(z_{S_t}) ]
```

(no last term at the root). With `tau'` and `psi'` as in Theorem 1', put
`r_{e,D} = phi_{e,D} - psi'_e` on `cl D`. Then

```
f* - rho~(phi) <= sum_{e} [ max_{D in P_e} sup_{cl D} (r_{e,D} - tau' w_e) + max_{D in P_e} sup_{cl D} (-r_{e,D} - tau' w_e) ]
                + sum_t max_{B in Leaves_t} sup_{z in B} [ err_{t,B}(z) - tau' W_t(z) ].
```

*Proof.* Fix `t`, a leaf `B` and `z in B`. The bracket above is the bag-`t`
expression of Theorem 1' at `z` for the single-valued data
`phi_u := phi_{u,D_u(B)}` (children), `phi_t := phi_{t,D_t(B)}` and
`err_t := err_{t,B}`. Steps 1 and 2 of the proofs of Theorems 1 and 1' are
identities and inequalities at the single point `z`. They use only (F1),
(F2), the values of these functions at `z_{S_u}` and `z_{S_t}`, and the
coefficient identities for `theta'`. So, for `t != r`, minus the bracket is at
most

```
[err_{t,B}(z) - tau' W_t(z)] + sum_{u in ch(t)} [-r_{u,D_u(B)}(z_{S_u}) - tau' w_u(z_{S_u})] + [r_{t,D_t(B)}(z_{S_t}) - tau' w_t(z_{S_t})],
```

and at the root `f*` minus the bracket is at most the same expression
without the last term. Because `z_{S_u} in cl D_u(B)`, each separator term
is at most `max_D sup_{cl D}` of the corresponding function of edge `u`.
The resulting bound does not depend on `(B, z)`. Now
`f* - rho~(phi) = [f* - inf_{B,z} (root bracket)] + sum_{t != r} sup_{B,z} (- bracket of t)`,
and each term is at most the bound of its bag. Sum over `t`. As in
Theorem 1, every edge appears once as a child and once as its own
separator. □

For cellwise pieces, choose `phi_{e,D}` on each closed cell as the
balanced minimizer of the closed-cell bracket of Theorem 1(c) with
half-width `tau' w_e`:

```
g'_{e,D} = inf_{l affine} [ sup_{cl D} (l - psi'_e - tau' w_e) + sup_{cl D} (psi'_e - tau' w_e - l) ],
```

with the intercept shifted so that both suprema equal `g'_{e,D}/2`. The
separator term of edge `e` is then at most `max_D g'_{e,D}`. The same holds
for any slope on `D` if `g'_{e,D}` is replaced by the bracket minimized
over the intercept only, for that slope.

*Remarks 1.2 (the grading).*

- *Order matters.* With `theta` increasing from the root to the leaves,
  the split is not exact in 155 of 161 random paths (check (e), Section 7).
- *The graded split fails with a larger discount.* On the chain of copies
  below, the graded split with the perturbation `r_e = -c w_e` has gap
  `c - 1/(2n)` for `c > 1/(2n)`, while the bracket with discount `c w_e`
  is 0 (check (f): for example gap `0.1875` at `n = 8`, `c = 1/4`).
  Proposition 1.3 shows that no other split does better.

**Proposition 1.3 (a necessary condition on the discount; added after
review).** Assume `f*` is attained at `x*`. Let `psi` be a split and
`c > 0` such that

```
gap(psi + r) <= sum_e [ sup (r_e - c w_e) + sup (-r_e - c w_e) ]   for all bounded r.      (b_c)
```

Then

```
2c sum_e w_e(x_{S_e}) <= m(x)   for every x.                                               (1.1)
```

In particular, on the chain of copies defined below, `c <= 1/(2n)`. So the
discount `1/(2n)` of Theorem 1 is optimal, over all splits, for bounds of
the form (b).

*Proof.*

1. If `|r_e| <= c w_e` for every `e`, the right side of (b_c) is `<= 0`, so
   `psi + r` is exact.
2. A split `phi` is exact if and only if every `F_t^phi` attains its
   infimum at `x*_{V_t}`. Indeed
   `rho(phi) = sum_t inf F_t^phi <= sum_t F_t^phi(x*_{V_t}) = F(x*) = f*`,
   with equality only if every term is equal.
3. Let `d(t)` be the depth of bag `t` (`d(r) = 0`) and
   `a_t = (-1)^{d(t)} w_t`. Apply step 1 to `r = c a` and `r = -c a`. Both
   vanish at `x*`, since `w_t(x*_{S_t}) = 0`. In bag `t` the split terms of
   `r = ± c a` are
   `sum_{u in ch(t)} r_u - r_t = ± c (-1)^{d(t)+1} [ sum_{u in ch(t)} w_u + w_t ]`
   (no `w_t` at the root). By step 2, applied to both signs,
   `Delta_t(z) := F_t^psi(z) - F_t^psi(x*_{V_t}) >= c [ sum_{u in ch(t)} w_u(z_{S_u}) + w_t(z_{S_t}) ]`.
4. For every `x`, `sum_t Delta_t(x_{V_t}) = F(x) - F(x*) = m(x)`, because
   the split terms cancel. Each edge appears in two bags, which gives
   (1.1). □

*The chain of copies.* Take a finite grid `S ⊂ [-1, 1]` that contains 0
and has smallest spacing `h`. Use the path with root `s_1^2`, middle bags
`P (s_t - s_{t+1})^2` with `P h^2 >= 1`, and leaf 0. A non-constant chain
costs at least `P h^2 >= 1 >= s^2`. Hence `U_e = 0`, `V_e(s) = s^2`,
`f* = 0` and `w_e(s) = s^2`. At `x = (s, ..., s)`, `m(x) = s^2` and
`sum_e w_e = n s^2`, so (1.1) gives `c <= 1/(2n)`. (In the continuum with
finite `P`, `w_e(s) = P s^2/(P + e - 1)` and (1.1) gives
`c <= 1/(2 sum_e P/(P + e - 1))`, which tends to `1/(2n)` as `P -> inf`.)
The instance of check (f), with `m = 41` and `P = 10^3`, is of this kind.

*Remarks on Proposition 1.3.*

- One perturbation pattern alone, `psi` and `psi + c a` exact, allows
  `c = 1/n` on the chain. That was the value of the sketch in the first
  version. The second pattern halves it.
- On a tree, (1.1) is also sufficient for the two-pattern condition. The
  largest `c` for which some split makes both `psi + c a` and `psi - c a`
  exact equals `inf_{m(x) > 0} m(x)/(2 sum_e w_e(x_{S_e}))`. To see this,
  put `b_t = sum_{u in ch(t)} w_u + w_t`. By steps 2 and 3, both patterns
  keep `psi` exact if and only if every `F_t^psi - c b_t` attains its
  minimum at `x*_{V_t}`. These are the bag functions of the split `psi`
  for the objective `F - 2c sum_e w_e`. Such a `psi` exists if and only if
  `x*` minimizes `F - 2c sum_e w_e`, because the DP split of a tree is
  exact (and then step 2 applies to it). So (1.1) is the most that these
  two patterns can show.
- Checks (`check_chain_discount.py`). An LP over all splits on the chain
  (`m = 21` and `41`, `P = 10^3`) gives the largest `c` as exactly `1/(2n)`
  with both patterns and `1/n` with one, for `n = 2, 3, 4, 6, 8`. On 60
  random small trees (paths and branching trees), the two-pattern LP value
  equals the infimum in the previous item to `1.5e-15`. It lies between
  `1/(2n)` and `2.83/(2n)`. So on random instances a somewhat larger
  discount is not excluded by this argument.
- Whether cell *counts* need the full factor `1/(2n)` is a different
  question (Section 9).

## 3. Kink concentration in one dimension

For an interval `J = [alpha, beta]` and an `M`-semiconcave `U`, let
`Delta_U(J) = U'(alpha+) - U'(beta-) + M (beta - alpha)`. This is the slope
drop of the concave function `U - M s^2/2` over `J`, and does not depend on
where the quadratic is centred. For an `M`-semiconvex `L`, let
`Delta_L(J) = L'(beta-) - L'(alpha+) + M (beta - alpha)`. Both are
nonnegative and increase with `J`.

**Lemma 2.** Let `U` be `M`-semiconcave and `L` `M`-semiconvex on an
interval `I`, with `L <= U`, and `w = U - L`. If `[c - h, c + h] ⊂ I`, then

```
Delta_U([c - h/2, c + h/2]) + Delta_L([c - h/2, c + h/2]) <= 4 w(c)/h + 4 M h.
```

The constants are sharp: for all `w(c) >= 0`, `M >= 0` and `h > 0`, the
supremum of the left side over admissible pairs `(U, L)` equals the right
side. So no bound `a w(c)/h + b M h` holds with `a < 4` or with `b < 4`.
In particular the lemma holds with `8 w(c)/h + 8 M h`, the form of the
first version, which Section 4 uses.

Moreover, for an interval `D` of radius `r` and `theta in [0, 1]`, the
function `psi = (1 - theta) U + theta L` has an affine `l` with
`osc_D(psi - l) <= (r/2)(Delta_U(D) + Delta_L(D)) + (M/2) r^2`.

*Proof (revised in round 2).* Let `U_c = U - (M/2)(s - c)^2`, which is
concave, `L_v = L + (M/2)(s - c)^2`, which is convex, and
`phi = L_v - U_c`, which is convex. Then `w = U - L = M (s - c)^2 - phi`.
So `L <= U` means `phi(s) <= M (s - c)^2` on `[c - h, c + h]`, and
`w(c) = -phi(c)`. Since `U_c'(s±) = U'(s±) - M (s - c)`, `Delta_U(J)` is the
slope drop of `U_c` over `J`. Likewise `Delta_L(J)` is the slope rise of
`L_v`. With `alpha = c - h/2` and `beta = c + h/2`,

```
Delta_U + Delta_L = phi'(beta-) - phi'(alpha+).
```

By convexity, `phi'(beta-) <= (phi(c+h) - phi(beta))/(h/2)` and
`phi'(alpha+) >= (phi(alpha) - phi(c-h))/(h/2)`. Also
`phi(alpha) + phi(beta) >= 2 phi(c)`, because `c` is the midpoint. Hence

```
Delta_U + Delta_L <= (2/h) [phi(c+h) + phi(c-h) - 2 phi(c)] <= (2/h) [2 M h^2 + 2 w(c)] = 4 w(c)/h + 4 M h.
```

*Sharpness.* Conversely, every convex `phi` with `phi <= M (s - c)^2` on
`[c - h, c + h]` comes from the admissible pair `U = (M/2)(s - c)^2`,
`L = phi - (M/2)(s - c)^2`. Given `W >= 0` and a small `delta > 0`, put
`a = h/2 - delta`. Let `phi = -W` on `[c - a, c + a]`, rising linearly
with slope `k` on both sides, where:

- `k = (M h^2 + W)/(h/2 + delta)` if this is at least `2 M h`. This line
  meets `M v^2` (`v = |s - c|`) at `v = h`. Its slope there is at least
  that of the parabola, so the line stays below the parabola for `v <= h`.
- Otherwise `k = 2 M a + 2 sqrt(M^2 a^2 + M W)`, the slope of the tangent
  from `(a, -W)` to `M v^2`. This line lies below the parabola everywhere.

In both cases `phi` is convex and `phi <= M (s - c)^2`, and `w(c) = W`. The
two kinks lie inside `[alpha, beta]`, so `Delta_U + Delta_L = 2k`. As
`delta -> 0`, `2k -> 4 W/h + 4 M h`. For `W > 0` the first case applies
once `2 M h delta <= W`. For `W = 0` the tangent slope is `4 M a -> 2 M h`.

For the second claim, centre the quadratics at the centre `c` of `D` and
write `psi = (1-theta) U_c + theta L_v + (1-2theta)(M/2)(s-c)^2`. Take for
`l` the same combination of the chords of `U_c` and `L_v` on `D` and the
constant `(1-2theta)(M/2) r^2`. A concave function lies above its chord by
at most `|D| Delta/4 = r Delta/2`, and a convex one below its chord by the
same amount. The quadratic term varies by at most `(M/2) r^2`. □

*Remarks.*

- With `w(c) = 0` and `h -> 0` the lemma gives `Delta_U = Delta_L = 0` at
  interior pinch points, which is Lemma 4.2 of [K] in dimension one.
  Choosing `h = sqrt(w(c)/M)`, when admissible, gives a slope drop of at
  most `8 sqrt(M w(c))`. So if `U` has a concave kink of size `J` at `c`
  and `[c - h, c + h] ⊂ I` for `h = sqrt(w(c)/M)`, then
  `w(c) >= J^2/(64 M)`. (The first version, with the constants 8, had
  `16 sqrt(M w(c))` and `J^2/(256 M)`.)
- *History of the constants.* The first version proved `(8, 8)` by bounding
  `Delta_U` and `Delta_L` separately, each by `4 w(c)/h + 4 M h`, through
  the second differences of `U_c` and `L_v`. It called the constant "loose
  by about 4", on the basis of the largest ratio 0.274 in 60,000 random
  cases and the family `U = -J|s|`, `L = -J^2/(2M) - M s^2/2` (ratio 0.25).
  Those numbers describe those families only. After review round 1 the
  note used the two-kink family `U = -J (s - 1/2 + delta)_+`,
  `L = J (-1/2 + delta - s)_+ - J (1/2 + delta)` on `[-1, 1]`, `c = 0`,
  `h = 1`. For `M = 0` it has the same `phi` as the family above with
  `W = J (1/2 + delta)`, split differently between `U` and `L`. It showed
  `a >= 4`. The example `U = L = -M s^2/2`, with
  `Delta_U + Delta_L = 2 M h`, gave only `b >= 2`. That version called the
  constant 8 "at most a factor 2 too large". That holds for the
  coefficient of `w(c)/h`, or for one common constant, but not for the
  coefficient of `M h` alone. Bounding `Delta_U + Delta_L` jointly through
  `phi` settles both coefficients at 4 (`check_kink_concentration.py`,
  `check_kink_sharp_lp.py`, Section 7.2).
- The lemma is special to one dimension, like Proposition 5.4(a) of [K].
  In two dimensions, convex and concave kinks can block affine functions at
  first order even at pinch points ([K], example after Proposition 5.4).

## 4. The upper half for one-dimensional separators (exact-bag model)

**Hypotheses (H3).** A tree decomposition with `n` edges. Every separator
`S_e` is one variable with range `I_e` of length `l_e`. The `F_t` are
bounded and continuous. `U_e` is `M_e`-semiconcave and `L_e` is
`M_e`-semiconvex on `I_e`, and both are `G_e`-Lipschitz. On box domains
with bag functions that are `C^{1,1}` (or semiconcave in the separator
variables uniformly in the others), the first condition is Lemma 4.1 of
[K]. Lipschitz data give the second.

**Rule R3.** Refine `I_e` dyadically. For a cell `D` with half-length `r`
and `w_min(D) = min_D w_e`, call `D` interior if
`dist(D, ∂I_e) >= 8 n r`, and put

```
B(D) = (32 n + 1/2) M_e r^2 - w_min(D)/(2n)      (interior),
B(D) = 2 G_e r + (5/2) M_e r^2 - w_min(D)/n     (otherwise).
```

Split `D` while `B(D) > eps/n`. On the final cells use the minimizers of
the cell brackets of Theorem 1(c).

**Theorem 3.** Under (H3), rule R3 terminates and gives `gap(PA(P)) <= eps`
with

```
|P_e| <= 1 + (8n + 2) J_e N_e + 8 n J'_e,
N_e  = sup_{eta >= 0} N_inf( pi_{S_e}(E(eta)), 2 sqrt((eps + eta)/M_e) ),
J_e  = max(0, ceil(log2( l_e sqrt((64 n^2 + n) M_e/(8 eps)) ))),
J'_e = max(0, ceil(log2( l_e/(2 rho_e) ))),   rho_e = min( eps/(4 n G_e), sqrt(eps/(5 n M_e)) ).
```

So `sum_e |P_e| = O(|T| log(|T| (G + M s0) s0/eps)) sum_e N_e`, using
`N_e >= 1`. `N_inf(A, l)` is the least number of intervals of length `l`
covering `A`, as in [D].

*Proof.* *Validity.* Let `D` be interior, `c_m in D` a minimizer of `w_e`
on `D`, and `h = 8nr`. Then `[c_m - h, c_m + h] ⊂ I_e` and
`D ⊂ [c_m - h/2, c_m + h/2]`. By Lemma 2 (in the weaker form with the
constants 8) and monotonicity,
`Delta_U(D) + Delta_L(D) <= 8 w_min(D)/h + 8 M_e h`. So
`osc_D(psi_e - l) <= w_min/(2n) + (32n + 1/2) M_e r^2` for some affine
`l`. Hence `g_{e,D} <= osc_D(psi_e - l) - w_min/n <= B(D)`: the bracket of
Theorem 1(c) with half-width `w/(2n)` subtracts `w_min/(2n)` twice. For a
cell near the boundary, the Lipschitz bound gives
`Delta_U(D) + Delta_L(D) <= 4 G_e + 4 M_e r`, hence
`osc <= 2 G_e r + (5/2) M_e r^2` and again `g_{e,D} <= B(D)`. As `r -> 0`
both forms of `B` tend to at most 0, so the rule stops. The final cells
have `g <= eps/n`, and Theorem 1(c) gives `gap <= n (eps/n)`.

*Count.* Each split adds one cell. An interior cell of level `j`
(half-length `r_j = l_e 2^{-j-1}`) is split only if
`w_min(D) < eta_j := (64n^2 + n) M_e r_j^2 - 2 eps`. So it meets
`pi_{S_e}(E(eta_j))`, and `eta_j > 0` holds for at most `J_e` levels. Cover
`pi_{S_e}(E(eta_j))` by `N_e` intervals of length
`l_c = 2 sqrt((eps + eta_j)/M_e)`. Since
`r_j^2 >= (eps + eta_j)/((64n^2 + n) M_e)`, we have
`l_c/(2 r_j) <= sqrt(64n^2 + n) <= 8n + 1/16`. So each interval meets at
most `8n + 2` closed dyadic cells of level `j`. Near-boundary cells of level
`j` number at most `4n` at each end. They are split only if
`2 G_e r_j + (5/2) M_e r_j^2 > eps/n`, which forces `r_j > rho_e`. That
happens for at most `J'_e` levels. □

*Remark (sharper constants; sketch, revision round 2).* R3 was designed
with the constants 8 of the first version of Lemma 2. It is kept as stated,
because all computations of Section 7 use it. With the sharp constants 4
the same proof works with `h = 4nr`:

- `D` is interior if `dist(D, ∂I_e) >= 4nr`;
- `B(D) = (8n + 1/2) M_e r^2 - w_min(D)/(2n)` for interior cells;
- a cell of level `j` is split only if `w_min < (16n^2 + n) M_e r_j^2 - 2 eps`;
- `l_c/(2 r_j) <= sqrt(16n^2 + n) <= 4n + 1/8`;
- there are `2n` near-boundary cells at each end.

This gives `|P_e| <= 1 + (4n + 2) J~_e N_e + 4n J'_e`, where `J~_e` is
`J_e` with `16n^2 + n` in place of `64n^2 + n`. Corollary 3.2 then applies
to this rule in the same way. I checked these steps by hand. I have not
run this rule.

**Corollary 3.2 (the bound-driven rule; added after review).** Let rule
`bd` split a dyadic cell `D` of `I_e` while `g_{e,D} > eps/n` (the cell
bracket of Theorem 1(c)), and use the cell-bracket minimizers on the final
cells. Under (H3), `bd` terminates, gives `gap(PA(P)) <= eps`, and its
partition is a coarsening of the partition of R3. In particular
`|P_e^bd| <= |P_e^R3|`, and the bound of Theorem 3 applies to `bd`.

*Proof.* The validity part of the proof of Theorem 3 shows
`g_{e,D} <= B(D)` for every dyadic cell `D`, interior or not. Both rules
start from `I_e` and halve cells. By induction on the level, every cell
that `bd` splits is also split by R3. So every R3 cell lies in one `bd`
cell. The final `bd` cells have `g_{e,D} <= eps/n`, and Theorem 1(c) gives
`gap <= eps`. □

On D1–D4 (Section 7.3, `m = 16385`), `g_{e,D} - B(D) <= -7.0e-5` on all
47,782 dyadic cells that R3 tests (logged maximum `-7.08e-5`, D2 at
`eps = 1e-3`), and every R3 cell lies in one `bd` cell
(`check_bd_coarsening.py`).

**Corollary 3.3 (comparison with certificate size; added after review,
from the review's sketch).** Consider the certificate model of [D] with
the hypotheses of Theorem 2.5 of [D] (gap coordinates `K_t` with weight
`alpha`). Assume that every non-root bag `t` has its separator among its
gap coordinates, `S_t ⊂ K_t`. Let `M = max_e M_e`, and let `N_dec(eps)` be
the least size of a certificate proving `eps`. Then

```
sum_e N_e <= 2 ceil(sqrt(M/alpha)/2) N_dec(eps) <= (sqrt(M/alpha) + 2) N_dec(eps),
sum_e |P_e| <= n + (8n + 2) (max_e J_e) 2 ceil(sqrt(M/alpha)/2) N_dec(eps) + 8n sum_e J'_e,
```

where the second line is for the cells of Theorem 3.

*Proof (revised in round 2).* Fix `eta` and a non-root bag `t` with edge
`e`. The proof of Theorem 2.5 of [D] works bag by bag (as used in
Proposition B.1 of [E]). It shows, via Lemma 1.4 of [D], that every
`x in E(eta)` has a leaf `B in Leaves_t` with `x_{V_t} in B` and
`alpha a_i^B(x) <= eps + eta` for every `i in K_t`. Take `i = S_e`. Since
`a_i^B >= d_i^2`, where `d_i` is the distance from `x_i` to the nearer
endpoint of `B_i` ([C], Section 1.1, as used in the proof of
Proposition 2.4 of [D]), `x_i` lies in `B_i` within
`l_a = sqrt((eps + eta)/alpha)` of one of its two endpoints. So the `2 |Leaves_t|` intervals `[lo, lo + l_a]` and
`[hi - l_a, hi]`, one pair for each leaf with `B_i = [lo, hi]`, cover
`pi_{S_e}(E(eta))`. Each of them is covered by
`ceil(l_a/l_c) = ceil(sqrt(M_e/alpha)/2)` intervals of length
`l_c = 2 sqrt((eps + eta)/M_e)`. Take the supremum over `eta`, use
`M_e <= M`, and sum over the non-root bags, which correspond one to one to
the edges. Apply this to a smallest certificate, for which
`sum_t |Leaves_t| <= N_dec(eps)`. Finally `2 ceil(x/2) <= x + 2`. The
second line follows from Theorem 3. □

*(Revised in round 2. The first form projected the `2^{|K_t|} |Leaves_t|`
cubes of the proof of Theorem 2.5 and had the factor
`ceil(sqrt(M/alpha)) 2^{w+1}`, with `w + 1` the largest bag size. As the
confirmation review noted, one coordinate needs only the two endpoints of
each leaf. Using intervals inside the leaf also halves their length. The
first form was correct but looser.)*

*What this settles.*

- In the exact-bag model the copy-error part of the covering
  characterization holds for one-dimensional separators on trees. Separator
  cells are bounded by `O(|T| log)` times the per-separator covering
  numbers with the *whole* tolerance, at radius `sqrt((eps + eta)/M_e)`.
  The polynomial has degree 1 in `|T|` per separator. The quantity has the
  form of the separator part of the quantity of Theorem 2.5 of [D], with
  `alpha` replaced by `M_e`. Corollary 3.3 makes this precise: when the
  separators are gap coordinates, the exact-bag separator cells number at
  most `O(|T| log) (sqrt(M/alpha) + 2)` times the size of a smallest
  certificate. There is no factor exponential in the width. This is an
  upper bound only. The lower bounds of [D] and [E] come
  from relaxation gaps (G_alpha) in the bags and do not apply to the
  exact-bag model, so Theorem 3 is not a two-sided result in either
  model.
- The hypothesis "that makes copy errors second order" in Conjecture 3.7
  of [D] and Conjecture B.5 of [E] is not needed here. Semiconcavity and
  semiconvexity (automatic for `C^{1,1}` box data) and Lipschitz value
  functions suffice. Kinks anywhere are allowed, and near-optimal sets may
  be degenerate.
- Compared with Proposition B.4 (one separator: `1 + 3J N`), the factor
  `(8n+2)/3` comes from the discount `1/(2n)`. Splitting the tolerance
  alone would cost `ceil(sqrt n)`. The rest comes from making the
  approximation robust to kinks (Lemma 2 with `h = 8nr`). With the sharp
  constants of Lemma 2 the factor would be about `(4n+2)/3` (sketch in the
  remark after Theorem 3).
- The same construction does not need band stability ([E], B.5 item 3). It
  never uses reduced value functions; the graded split is built from the
  original `U_e`, `L_e`.
- Rule R3 decides the cells of each edge from that edge's data (`w_e`,
  `M_e`, `G_e`) and the global `n` and `eps`. So cell placement can be
  decided edge by edge. Section 5 shows that the *criterion* matters.

## 5. Cell placement by one-edge band brackets fails

*(Heading corrected after review. The first version read "Per-edge control
of cell placement fails", which Theorem 3 contradicts; see Revision R2.)*

**Proposition 4.** Let `beta > 0`, `kappa >= 2 beta`, and consider the path
with two edges on `[-1, 1]^2`:

```
root:   2 beta s1^2,     middle:   kappa (s1 - s2)^2 - beta s2^2,     leaf:   2 beta s2^2.
```

Then `f* = 0`, both bands contain the constant 0, and
`gap(Aff) = gap(R) = beta`. Consequently a rule that refines an edge only
while the one-edge bracket `inf_l [sup_D (l - U_e) + sup_D (L_e - l)]` of
its *original* band exceeds a tolerance stops at one cell per edge, for
every tolerance, and its gap is `beta`.

*Proof.* `F = 2beta s1^2 + kappa (s1 - s2)^2 + beta s2^2 >= 0`, with
equality at 0.

- Edge 1: `U_1(s1) = min_{s2} [kappa (s1 - s2)^2 + beta s2^2] = (kappa beta/(kappa + beta)) s1^2 >= 0`
  (the minimizer is interior) and `L_1 = -2 beta s1^2 <= 0`.
- Edge 2: `U_2 = 2 beta s2^2`, and
  `V_2(s2) = min_{s1}[2 beta s1^2 + kappa (s1 - s2)^2] - beta s2^2 = (2 beta kappa/(2 beta + kappa) - beta) s2^2 >= 0`
  for `kappa >= 2 beta`, so `L_2 = -V_2 <= 0`.

So 0 lies in both bands, and every one-edge bracket with one cell is
`<= 0`. For affine splits `phi_e = lambda_e s_e + const`, the middle bag
evaluated at `s1 = s2 = ±1` gives `-beta ± (lambda_2 - lambda_1)`. So its
minimum is at most `-beta - |lambda_2 - lambda_1|`. The root and leaf
minima are at most 0 (value at 0). So `rho(Aff) <= -beta`. The split
`phi = 0` attains `-beta`, since the middle bag is `>= -beta s2^2 >= -beta`. □

*What it shows.* Proposition 3.3 of [K] showed that per-edge band
distances do not control the gap of a *fixed* class (constants). The new
point is about *cell placement*. Here each edge's band contains an affine
function (even a constant), yet no affine split is jointly good. The
one-edge band bracket is `<= 0` on every cell where the original band
contains an affine function. So a refinement rule driven by it can stop
far too early.

This does not mean that placement must be decided jointly. Rule R3
(Theorem 3), the sliver rule `bd` (Corollary 3.2) and Proposition B.4's
rule `M r^2 - min w > eps/n` each decide the cells of edge `e` from edge
`e`'s own data and the global `n` and `eps`. R3 and `bd` provably reach
the tolerance, and B.4's rule did so on every tested instance. Unlike the
band bracket, R3 and B.4's rule refine wherever the margin `w_e` is small
compared with the curvature times the squared cell size, that is, near
pinch points, even where the band contains an affine function. `bd` uses a
different test. It refines where the sliver of edge `e` (half-width
`w_e/(2n)` around the graded split `psi_e`) admits no affine function
within `eps/n`. Near a pinch point where `psi_e` is locally affine, it does
not refine. In Proposition 4, `psi_1` and `psi_2` are nonzero multiples of
`s1^2` and `s2^2`; more precisely, both sliver bounds `psi_e ± w_e/4` are
strictly concave for edge 1 (coefficients in
`[-2 beta, kappa beta/(2(kappa+beta)) - beta]` times `s1^2`) and strictly
convex for edge 2 (`[3 beta/2 - beta kappa/(2 beta+kappa), 2 beta]` times
`s2^2`), so no affine function fits in the sliver near 0 and `bd` refines
there, for all `kappa >= 2 beta` (reason sharpened by the root after the
round-2 confirmation). The choice of values is not
the issue either: on the cells of the band-bracket rule, the LP-optimal
joint values still fail (below). *(Corrected in revision round 2: the
margin-and-curvature sentence used to speak of all three rules.)*

For `kappa > 2 beta` the failure is not a thinning of the band *width*.
The reduced band keeps width of order `s1^2` near 0, but it has the wrong
shape. (For `kappa = 2 beta` the width does drop to zero near 0.) After the
choice `phi_2 = 0`, the reduced function
`U'_1(s1) = min_{s2}[kappa (s1 - s2)^2 - beta s2^2]` equals
`-kappa beta/(kappa - beta) s1^2` for `|s1| <= 1 - beta/kappa`. There it is
concave. Beyond, the box constraint is active and
`U'_1 = kappa (|s1| - 1)^2 - beta` is convex. It touches
`L_1 = -2 beta s1^2` at 0. Near 0 the reduced band has width
`beta (kappa - 2 beta)/(kappa - beta) s1^2`. That is of order `s1^2` for
`kappa > 2 beta`, and zero on `|s1| <= 1/2` for `kappa = 2 beta`. In every
case the reduced band contains no affine function. An affine `l` in it
would have `l(0) = 0` and would lie below `-k s1^2`, with
`k = kappa beta/(kappa - beta) > 0`, on both sides of 0, which is
impossible. Its one-cell affine bracket equals `beta` (`check_prop4.py`).
*(Corrected after review: the first version called `U'_1` concave without
restriction and said the reduced band has width of order `s1^2`, which
fails for `kappa = 2 beta`. Corrected again in revision round 2: the lead
sentence of this paragraph said, without restriction, that the failure is
not a thinning of the width.)*

The rule of Theorem 1 refines near the pinch point and reaches the
tolerance (Section 7.4). So does Proposition B.4's rule, which refines
near pinch points because of its `M r^2` term.

*Numerical plateau.* On the path families of Section 7.3 with `n = 4, 6, 8`,
cells refined edge by edge until the one-edge band bracket is `<= eps/n`,
or even `<= eps/n^2`, leave an LP-optimal gap over *all* cellwise-affine
splits on those cells of `2.5e-3`, `1.27e-2` and `2.29e-2` for
`eps = 1e-3` (`m = 257`). These values barely change when the tolerance is
lowered: the `n = 4` value moves from `2.52e-3` to `2.50e-3`, and the others
agree to three digits. On the same instances the rule of Theorem 1 gives LP
gaps below `1e-15` (`check_naive_failure.py`). The plateau is not a
coarse-grid artifact up to `m = 2049`. The review's independent
cutting-plane LP found `1.22e-2`–`1.27e-2` (`n = 6`) and
`2.33e-2`–`2.36e-2` (`n = 8`) at `m = 513, 1025, 2049`. I reran the
review's script for this revision; its output was identical apart from
timings (`logs/rerun_review_indep_naive_fine.log`). These are still grid
values, not continuum values.

## 6. Decomposition certificates and Conjecture B.5

**Proposition 5 (aligned certificates).** Consider a decomposition
certificate (Definition 1.2 of [D]) on a tree with one-dimensional
separators, with (LC) and (CM) imposed only for pairs whose interiors meet
in the separator coordinates. The "touching pairs" remark in Section 1.4 of
[D] shows that such certificates are valid (Lemma 1.3 holds); their size is
counted as in Definition 1.2. Call the certificate *aligned* if, for every
bag `t`, every leaf `B in Leaves_t` and every separator `S` of `t` (its own and
its children's), `B_S` lies in one cell of `P_S`. Take child bounds
`psi_{u,B} = l_{u,D_u(B)}`, where `D_u(B)` is the unique cell of `P_u` whose
interior meets `B_{S_u}`, and
maximal `beta` (Lemma 1.5 of [D]). Then, for fixed cell slopes, `l_r`
equals the best value over intercepts of the split relaxation in which bag
`t` is evaluated leaf by leaf,
`inf_{B in Leaves_t} inf_{z in B} [ sum_{c at t} f_{c,B}(z_c) + sum_{u in ch(t)} l_{u,D_u(B)}(z_{S_u}) - l_{t,D_t(B)}(z_{S_t}) ]`.
Consequently Lemma 1'
applies, with `err_{t,B} = F_t - sum_{c at t} f_{c,B}` on `B`, which is at
most `alpha' A_t w(B)^2/4` under (U^q), and with each cell's affine piece
used on the closed cell. A certificate proves tolerance `eps` if, for
example:

- its cells satisfy rule R3 adapted to the discount `tau' = 1/(3n+1)`
  (the proof of Theorem 3 with `h = 4r/tau'`) and tolerance `eps/(2n)`,
  and its cell minorants have suitable slopes. On each cell `D` of `P_e`,
  `l_{e,D}` has the slope of the balanced minimizer of the closed-cell
  bracket `g'_{e,D}` (half-width `tau' w_e`; the paragraph after
  Lemma 1'). More generally, it may have any slope for which this bracket,
  minimized over the intercept alone, is at most `eps/(2n)`. The intercepts
  are the maximal ones, as above; and
- every leaf `B` of bag `t` has
  `alpha' A_t w(B)^2/4 <= min_B W_t/(3n+1) + eps/(2(n+1))`.

*Proof.* With aligned leaves, the only pairs whose interiors meet are a
leaf and the cell containing its projection. So (CM) holds with equality
for `psi_{u,B} = l_{u,D_u(B)}`, and (LC) involves one cell per leaf. The
relaxation is evaluated leaf by leaf. A point on a cell boundary belongs to
leaves on both sides, so each cell's affine piece is used on the closed
cell, and the cell brackets of Theorem 1(c), computed on closed cells,
bound the deficits. This is the setting of Lemma 1'. The maximal
`beta_{t,D}` is the infimum of the relaxed bag-`t` function over the cell,
minus the cell minorant. This is the "touching" normalization of Lemma 0;
raising an intercept until the bag minimum on its cell is 0 never lowers
`rho~`. So `l_r = sup_beta rho~`, the supremum over intercepts for the
given slopes. The rest is Lemma 1'. With the slopes of the first
condition, each cell bracket, minimized over the intercept, is at most
`eps/(2n)`: by the proof of Theorem 3 with discount `tau'`, or by
assumption for other slopes. So at the balanced intercepts the separator
terms of Lemma 1' contribute at most `n · eps/(2n) = eps/2` (paragraph
after Lemma 1'), and `l_r` is at least the value of `rho~` there. By the
second condition,
`err_{t,B} - tau' W_t <= eps/(2(n+1))` on every leaf, so the bag terms
contribute at most `(n + 1) · eps/(2(n+1)) = eps/2`. □
*(Revised after review: the first version applied Theorem 1' directly,
although the split here is two-valued at cell boundaries and the bag errors
depend on the leaf. Lemma 1' states the extension.)*

*A condition on the slopes is needed (added in revision round 2; the
example shows that the cell condition alone is not sufficient, not that
this particular slope condition is necessary).* The first
condition used to speak of the cells only. The proof needs the slopes.
With other slopes the conclusion can fail. This example is from the
confirmation review.

- *Instance.* `n = 1` on `[-1, 1]`, root `-lambda s + M s^2/2`, leaf
  `lambda s + M s^2/2`. Then `f* = 0`, `w = M s^2`, and `psi' = lambda s`.
- *Certificate.* Exact leaves aligned with the cells, so the second
  condition holds, and constant minorants.
- *Why it fails.* A cell `[0, ell]` with `ell <= lambda/M` then forces
  `f* - l_r >= lambda ell - M ell^2/2`. The R3-adapted cells near 0 have
  length of order `sqrt(eps/M)/n`. So the certificate fails once `eps` is
  small against `lambda^2/(n^2 M)`. This is the effect of Proposition 2.6
  of [D].

`check_prop5_slopes.py` (`lambda = M = 1`, R3-adapted cells, 58–146 cells)
confirms this:

- *Constant minorants:* gaps of 1.6, 5.2, 34 and 280 times `eps` for
  `eps = 1e-2, 1e-3, 1e-4, 1e-5`.
- *Balanced-minimizer slope `lambda`:* gap 0.
- *Slopes `lambda + nu_D`, with `nu_D` as large as the bracket bound
  `eps/(2n)` allows:* gaps of at most `0.498 eps`, within the proven
  `eps/2`.

*Definition 1.2 as written* also imposes (LC) and (CM) on pairs that only
touch. Then a configuration may place the parent copy in one cell and the
child copy in the touching neighbour (Lemma 1.5 of [D]). This drift across
touching cells is not covered by Lemma 1'. I have not bounded its effect;
one route is to control the jumps of the cellwise-affine function at cell
boundaries.

*Size (sketch, not proved).* The cells cost as in Theorem 3, with `n`
replaced by about `3n/2`. The leaves cost (i) the alignment, at least
`prod_S |P_S|` boxes per bag, and (ii) the refinement for the bag error,
of the equal-share type: coverings of `pi_{V_t}(E(eta))` at radius of
order `sqrt((eps/|T| + eta/|T|)/(alpha' A))`. That is
`|T|^{(w+1)/2}` times the quantity of Theorem 2.5 of [D]. So the route
gives at best reading (R2) of Section B.1 of [E]. Term (i) can be
quadratic in the separator covering numbers, which a two-sided
characterization would not allow.

**Where the certificate case stands.**

- *Separator part.* Settled for one-dimensional separators in the
  exact-bag model (Theorem 3). No hypothesis on copy errors is needed.
- *Bag part with a constant share of the tolerance per bag.* This is what
  Theorem 1' and its leafwise form, Lemma 1', give. Theorem B.2 of [E] shows that such constant shares can
  lose `|T|^{d/2}` against the true certificate size (staircase family). So
  this route cannot give reading (R1).
- *The exact criterion.* By Lemma 0 (relaxed form), an aligned certificate
  proves `eps` exactly when the bag errors together with the reduced
  separator errors are admissible *uniformly*:
  `sum_t err_t + sum_e delta~_e <= m + eps` everywhere. For finite-valued
  separators with exact fixing, the cellwise class is the full class, so
  one can take `phi_e` equal to the reduced value function and
  `delta~ = 0`. The criterion is then admissibility of the bag errors
  alone. That is how the staircase certificate of Theorem B.2(b) works.
- *Per-level versus uniform admissibility.* `Phi_2` uses families
  admissible on one `E(eta)` at a time. Per-level families
  (`eta_j = 2^j eps`, set to `+inf` outside `pi_{V_t}(E(eta_j))`) can be
  combined by the pointwise minimum. The result satisfies
  `sum_t e_t <= 2(eps + m)` everywhere, and its centres are the union of
  the per-level centres. *Sketch:* at `x` with
  `m(x) in (eta_{j-1}, eta_j]` (or `m(x) <= eta_0` for `j = 0`), the
  pointwise minimum is at most the level-`j` family, which gives
  `sum_t e_t <= eps + eta_j`. Here `eta_j <= max(2 m(x), eps)`: for
  `j >= 1`, `eta_j = 2 eta_{j-1} < 2 m(x)`, and `eta_0 = eps`. Hence
  `sum_t e_t <= eps + max(2 m(x), eps) <= 2(eps + m(x))`.
  *(Corrected after review: the first version used the intermediate bound
  `eps + 2 max(m(x), eps)`, which exceeds `2(eps + m(x))` when
  `m(x) < eps/2`; at `m = 0` it reads `3 eps <= 2 eps`. The conclusion is
  unchanged.)* Halving `e` to make
  it admissible shrinks the radii by `sqrt 2`. For irregular allocations
  the effect of that on the count is part of open step (1) below.
- *Two steps remain open for reading (R1).* (1) Realize an irregular
  variable-radius allocation by leaves. The upper-bound side needs the
  error roughly constant over a leaf, while the lower bound of
  Theorem B.3 exploits `q_B` vanishing at vertices. (2) Control the reduced
  separator errors of the *relaxed* problem. Its value functions jump at
  leaf boundaries in the separator coordinates, so Lemma 2 does not apply
  across cells. The upper half of Conjecture B.5 for certificates in
  reading (R1) therefore remains a conjecture.

## 7. Numerical checks

All in [`covering/`](covering/). Environment: Python 3.13, NumPy 2.5.1,
SciPy 1.18.0 (HiGHS). `OMP_NUM_THREADS=1`. Exact minima over finite grids;
floating point.

### 7.1 Theorem 1, Theorem 1', Lemma 0 (`check_graded_split.py`, `logs/check_graded_split.log`)

Random finite trees: 2–6 bags, half paths and half trees with up to two
children, 1D separators with 3–11 values, uniform or smooth random bag
tables.

- (a) The exact per-bag decomposition matches the gap to `1.4e-14`.
- (b) The graded split is exact (`|gap| <= 9e-16`).
- (c) 10,000 perturbations `r` (Gaussian at five scales, proportional to
  `w`, cellwise constant): no violation of the bound. The ratio gap/bound
  has median 0.885 and maximum 1.000.
- (d) For `n = 1` the bound is an equality (error `4e-15`).
- (e) Reversed grading is non-exact in 155 of 161 paths.
- (f) Chain of copies (`m = 41`, `P = 10^3`, so `w_e = s^2` on the grid;
  Section 2), graded split, discount `c w_e`: holds for `c = 1/(2n)`;
  fails for `c = 1/4, 1/2` when `n >= 4` (and `c = 1/2`, `n = 2`). For
  example `n = 8`, `c = 1/4`: gap 0.1875, bracket 0. (The row `c = 0.25`
  appears twice for `n = 2`, where `1/(2n) = 1/4`.)
- (g) Theorem 1' with random bag errors in `[0, 0.5]` and bag-projection
  margins by enumeration: 0 violations in 600 checks.
- (h) Lemma 0, all separator assignments enumerated: error `3.6e-15` over
  200 instances.
- (i) The split `phi_t = L_t` on trees with branching is not exact in any
  of 238 random trees (largest gap 1.67).
- (j) *Added after review* (`check_chain_discount.py`,
  `logs/check_chain_discount.log`). On the chain of copies (`m = 21, 41`,
  `P = 10^3`; `w_e = s^2` exactly on the grid), an LP over all splits gives
  the largest `c` for which some `psi` makes `psi + c a` and `psi - c a`
  exact: `1/(2n)` to six digits for `n = 2, 3, 4, 6, 8`. With the single
  pattern `psi + c a` it gives `1/n`. On 60 random small trees (`m = 4`,
  paths and branching trees), the two-pattern LP value agrees with
  `min_{m(x) > 0} m(x)/(2 sum_e w_e(x_{S_e}))` to `1.5e-15` and lies in
  `[1/(2n), 2.83/(2n)]` (Proposition 1.3 and the remarks after it).

### 7.2 Lemma 2 (`check_kink_concentration.py`, `logs/check_kink_concentration.log`)

`U` is a minimum of 1–5 random quadratics with curvature `<= M` (half of
them strongly concave, down to `-60`). `L` is a maximum of quadratics with
curvature `>= -M`, shifted below `U`. `M in {0.1, 1, 5}`. One-sided
derivatives are exact. Over 60,000 `(c, h)` pairs the largest value of
`(Delta_U + Delta_L)/(8 w(c)/h + 8 M h)` is 0.274. The family
`U = -J|s|`, `L = -J^2/(2M) - M s^2/2` gives 0.25 at `x = M h/J = 1`.

*Added after review.* The two-kink family of Section 3 (with `J = 1`)
gives the ratios 0.4856, 0.4990, 0.4999 and 0.5000 (rounded; the ratio
is below 1/2 for every `delta > 0`) for
`(M, delta) = (1e-2, 1e-2), (1e-4, 1e-3), (1e-6, 1e-4), (0, 1e-6)`, with
`(Delta_U + Delta_L)/(w(c)/h)` up to 4.0000. `U - L >= 0` holds on a
200,001-point grid. The example `U = L = -M s^2/2` gives
`Delta_U + Delta_L = 2 M h`. So the random family's 0.274 says nothing
about the sharpness of the constant. The review's differential-evolution
search over two-piece families reached 0.4971.

*Added in revision round 2 (sharp form).* The extended
`check_kink_concentration.py` reuses the same random numbers, so its first
15 output lines are unchanged. It adds:

- The random pairs compared with `4 w(c)/h + 4 M h`: largest ratio 0.5475,
  no violation.
- The family of the sharpness proof (Section 3) for
  `(W, M, h) = (1, 0, 1), (0, 1, 1), (1, 1, 1), (0.05, 2, 0.4), (2, 0.1, 0.8)`
  and `delta = 1e-2, 1e-4, 1e-6`. `U - L >= -6.6e-16` on a 200,001-point
  grid. The ratio to `4 w(c)/h + 4 M h` is `0.95`–`0.98` at `delta = 1e-2`
  and `0.999995`–`0.999998` at `delta = 1e-6`, including `W = 0`, where it
  gives `Delta_U + Delta_L -> 4 M h`.

A first draft of this family used the slope `(M h^2 + W)/(h/2 + delta)`
also for `W = 0`. The grid check caught `U - L = -3.8e-4` there, and the
tangent case of Section 3 fixes it.

The new script `check_kink_sharp_lp.py` maximizes `Delta_U + Delta_L` by
an LP over all convex piecewise-linear `phi` with breakpoints on a uniform
grid of `[-h, h]` (`2m + 1` points). It uses the reduction of the proof and
requires `phi <= M s^2 - M ds^2/4` at the grid points, so the interpolant
stays below `M s^2` except near `s = 0`, where the script fixes
`phi(0) = -W` in place of that bound (in 4 of the 18 runs the LP optimum
exceeds `M s^2` between grid points, by at most `5.1e-3`; noted by the
round-2 confirmation). No conclusion changes: the upper-bound check holds on
this larger class, and the explicit family proves sharpness. For six `(W, M, h)` the optimum stays below
`4 W/h + 4 M h` and approaches it: ratio 0.74–0.80 at `m = 8`, 0.969–0.970
at `m = 64`, and 0.9961 at `m = 512`. This checks the upper bound against
every function of this class, not only random ones.

### 7.3 Theorem 3 on path families (`run_paths.py`, `logs/run_paths.log`)

**Instances D1–D4.** Path with `n` edges, `s_e in [-1, 1]`, coupling
`kappa = 10`:

- root: `u(s1) + 0.3 sin(3 s1)`;
- middle bag `t`: `10 (s_t - s_{t+1})^2 + u(s_{t+1})`;
- leaf: `u(s_n) - 0.3 sin(3 s_n)`.

Here `u` is a flat valley `(|s| - v)_+^2`, plus concave kinks
`min(0, 0.5 sigma (p - s))` at `p in {0.6, 0.65, -0.7, 0.75, -0.8}` in some
bags. D1: `n = 3`, `v = 0.3`. D2: `n = 6`. D3: two valleys at `±0.4` with
`v = 0.15`. D4: `v = 0` (quadratic growth). `M = 2 kappa + 2 + 0.3·9 = 24.7`,
checked against grid second differences (`<= 22`). `G` is a grid estimate.
Fine grid `m = 16385`, coarse grid `m = 257` for LPs.

Rules compared (tolerance `eps/n` per edge):

- `thm`: rule R3;
- `bd`: refine while the Theorem 1 cell bracket exceeds `eps/n`;
- `naive`: the one-edge band bracket;
- `sup`: twice the sup-norm affine error of `U_e` (the sup-norm sandwich
  with the DP split).

`N_e` is computed by greedy covering of `{w_e <= eta}` on the grid over 81
values of `eta`.

| inst., eps | `N_e` | thm cells (total) | thm/(n J sum N) | bd cells | bd/N per edge | sup cells | naive: LP gap(PA), m = 257 |
|---|---|---|---|---|---|---|---|
| D1, 1e-2 | 9, 8, 8 | 1464 | 1.95 | 26 | 1.0–1.1 | 74 | 4.4e-3 |
| D1, 1e-3 | 10, 10, 10 | 2515 | 2.33 | 31 | 1.0–1.1 | 266 | 4.8e-5 |
| D2, 1e-2 | 6 (all) | 4891 | 2.06 | 53 | 1.3–1.5 | 277 | **1.30e-2** |
| D2, 1e-3 | 7, 7, 7, 7, 6, 6 | 7864 | 2.52 | 68 | 1.3–2.2 | 659 | **1.27e-2** |
| D3, 1e-2 | 15, 14, 15 | 2193 | 1.66 | 35 | 0.7–0.9 | 92 | **1.33e-2** |
| D3, 1e-3 | 17, 16, 17 | 3060 | 1.70 | 43 | 0.8–0.9 | 300 | **2.35e-3** |
| D4, 1e-2 | 3, 3, 3 | 788 | 2.92 | 10 | 0.7–1.3 | 84 | 0 |
| D4, 1e-3 | 3, 3, 3 | 1131 | 3.49 | 14 | 1.0–2.0 | 312 | 0 |

Bold: above `eps`.

- **Rule R3.** In every run the explicit split has gap `<= 1e-7` and all
  cell brackets are `<= eps/n`. The rule was never grid-limited at
  `m = 16385`. Its counts are 1.7–3.5 times `n J_e N_e`, inside the proven
  `(8n+2) J_e N_e + 8n J'_e`. For D1 at `eps = 1e-2` the proven bound on
  edge 1 is 2653 cells (`J = 10`, `J' = 13`, `N = 9`) against 497 used.
- **Bound-driven rule.** The practical version certified by Theorem 1 uses
  0.7–2.2 cells per unit of covering number. Its explicit split has gap
  `<= 4.5e-3` (`eps = 1e-2`) and `<= 4.4e-4` (`eps = 1e-3`). Its LP optimum
  on the coarse grid is `<= 8.2e-4`. In every run its partition coarsens
  R3's, and `g_{e,D} <= B(D)` on every dyadic cell R3 tests (Corollary 3.2;
  `check_bd_coarsening.py`, `logs/check_bd_coarsening.log`, added after
  review).
- **Sup-norm sandwich.** It needs 2.6–22 times more cells than `bd`. It
  must approximate `U_e` everywhere, including concave kinks where the band
  is wide.
- **Naive rule.** Its explicit per-edge choices give gaps of 0.098–0.87
  on D1–D3 in the fine runs (0 on D4). Good per-edge values do not combine
  (Proposition 3.3 of [K]). But the values are not the whole problem: the
  LP-optimal joint values on its cells also miss the tolerance on D2 and
  D3. The cells are in the wrong places, as in Proposition 4.

### 7.4 Band-bracket placement and Proposition 4 (`check_naive_failure.py`, `check_prop4.py`)

`check_naive_failure.py` uses instances of type D with `n = 2, 3, 4, 6, 8`,
`eps = 1e-2, 1e-3` and `m = 129, 257`. It reports the LP gap over all
cellwise-affine splits on the cells of four rules: naive (`eps/n`), naive
with `eps/n^2`, Proposition B.4 edge by edge (`M r^2 - min w > eps/n`),
and `bd`.

- Each naive rule misses the tolerance in the same 10 of the 20 settings
  (all settings with `n = 6, 8`, and `n = 4` at `eps = 1e-3`). In these
  settings its LP gap is `2.0e-3`–`2.5e-3` (`n = 4`), `1.1e-2`–`1.3e-2`
  (`n = 6`) and `2.3e-2`–`2.5e-2` (`n = 8`). There, lowering the per-edge
  tolerance from `eps/n` to `eps/n^2` decreases it by at most 4.4% in the
  logged three-digit values (largest: `1.14e-2` to `1.09e-2`, `n = 6`,
  `eps = 1e-2`, `m = 129`).
- In settings that reach the tolerance, the lower tolerance can lower the
  gap. In two settings it drops by more than a factor 10: `n = 2`,
  `eps = 1e-2`, at both grids (`6.07e-3` to `3.59e-4` at `m = 129`,
  `6.64e-3` to `4.15e-4` at `m = 257`). At `eps = 1e-2`, `m = 257` it also
  moves from `4.37e-3` to
  `3.87e-3` (`n = 3`) and from `3.43e-3` to `2.52e-3` (`n = 4`).
  *(Corrected in revision round 2: this said "in one case by an order of
  magnitude".)* *(Corrected after review: the first
  version said that the gap does not decrease, without restricting to the
  failing settings.)*
- The Proposition B.4 rule and `bd` reach the tolerance in all 20
  settings. B.4 uses 80–309 cells; `bd` uses 17–102.

`check_prop4.py` covers `(beta, kappa) = (1, 10), (1, 2), (0.1, 10)`:

- 0 is in both bands, and `gap(Aff) = beta` to 6 digits.
- The band-bracket rule keeps one cell per edge, with gap `beta`, at
  tolerances `1e-2, 1e-4, 1e-6`.
- `bd` reaches `eps` with 2–14 cells per edge for `eps` down to `1e-4`.
  The count grows logarithmically, as expected under quadratic growth.
- The Proposition B.4 rule also reaches `eps`, with 8–54 cells per edge.
- *Added after review.* The reduced function `U'_1` (after `phi_2 = 0`,
  2001-point grid) matches its closed form to `2.4e-6`. It is concave on
  `[-0.899, 0.899]`, `[-0.500, 0.500]` and `[-0.989, 0.989]`
  (`1 - beta/kappa = 0.9, 0.5, 0.99`). The largest width of the reduced
  band on `|s| <= 0.2` is `3.56e-2`, `1.4e-17` (that is, zero for
  `kappa = 2 beta`) and `3.96e-3`, as the closed form predicts. The one-cell
  affine bracket of the reduced band equals `beta` in all three cases.

## 8. Literature and novelty

Examined for this note:

- the notes [D], [E], [K] and their reviews;
- two short web searches:
  - "reparametrization tree min-sum forward backward messages convex
    combination": found the tree-reweighted message passing literature
    (Wainwright–Jaakkola–Willsky; Kolmogorov, "Generalized sequential
    tree-reweighted message passing", arXiv:1205.6352) and lecture notes
    on reparametrizations;
  - "semiconcave above semiconvex quantitative bound": found standard
    semiconcavity definitions and the fact that functions both semiconvex
    and semiconcave are `C^{1,1}`, but no quantitative kink bound of the
    form of Lemma 2.
- added after review, on the review's pointer: N. Ruozzi and
  S. Tatikonda, "Message-passing algorithms: reparameterizations and
  splittings", arXiv:1002.3239 (v1 February 2010, v3 December 2012). I
  checked the arXiv abstract page only (rechecked in revision round 2).
  The abstract describes a systematic study of convergent max-product-type
  message-passing algorithms for MAP estimation. It gives new sufficient
  conditions for convergence to local or global optima and "a
  combinatorial characterization of these optima based on graph covers". It
  also describes a new convergent and correct algorithm. Finally, it says
  that the conditions needed to guarantee convergence to a global optimum
  "can be too restrictive in both theory and practice", and that this
  limitation "is characterized by graph covers". The paper is background
  for Lemma 0 and for the split viewpoint of this note. From the abstract
  I cannot tell whether it contains anything like the monotone grading;
  the review, which also searched for it, found nothing of the kind.

Assessment:

- **Lemma 0.** Reparametrization on trees in substance: a split relaxation
  is exact for the modified objective `F - sum delta`. Known in substance
  for discrete min-sum problems; stated here for general bag functions with
  relaxation errors.
- **Theorem 1 and Proposition 1.3.** The ingredients are standard: DP
  messages give exact reparametrizations (see also Ruozzi–Tatikonda for
  splittings), and the exact set is convex. I did not find the monotone
  grading, the resulting margin-discounted sandwich, the optimality of its
  discount (Proposition 1.3), or its use for cell counts. The upper end of
  the tree sandwich of [K] and the approximate-LP bound of de Farias–Van
  Roy (cited in [K]) are sup-norm forms without the discount.
- **Lemma 2.** A quantitative, one-dimensional form of the pinch regularity
  of semiconcave pairs (Cannarsa–Sinestrari 2004; Ilmanen's lemma; Lemma
  4.2 of [K]). The first version's proof used the second-difference
  estimate that appears in standard proofs of Ilmanen's lemma. The sharp
  form (revision round 2) reduces to chord-slope bounds for one convex
  function below a parabola. Both proofs are elementary. So the lemma is
  best described as an aggregated one-dimensional form of a standard
  estimate. I did not find this statement or its sharp constants. No new
  search was run in revision round 2.
- **Theorem 3, Corollaries 3.2 and 3.3, Lemma 1', Propositions 4 and 5.**
  Consequences within this program's models. Proposition 4 extends
  Proposition 3.3 of [K] from constants to affine classes and to cell
  placement by one-edge band brackets.

Short, unsuccessful searches do not establish novelty.

## 9. Limitations and open questions

- **Certificates, reading (R1).** Open (Section 6). The two missing steps
  are the realization of irregular pointwise allocations by leaves, and the
  control of reduced separator errors for relaxed bag functions.
- **The factor `|T|` per separator.** Theorem 3 pays `8n + 2` (about
  `4n + 2` with the sharp Lemma 2; sketch after Theorem 3). Tolerance
  splitting alone would cost `sqrt(n)`. For bounds of the form of
  Theorem 1(b), the discount `1/(2n)` is optimal over all splits on the
  chain of copies (Proposition 1.3, proved after review; the first version
  had only a sketch giving `1/n`). Cell counts may not need the full
  factor, though. Proposition B.4's rule, with `M r^2` in place of about
  `64 n^2 M r^2`, reached the tolerance in all tested cases. Whether B.4
  edge by edge with `eps/|T|` always suffices is open.
- **Cell placement.** Placement decided edge by edge works with the right
  criterion (R3, `bd`). Placement by one-edge band brackets does not
  (Proposition 4). Which per-edge criteria suffice in general, beyond
  those certified through Theorem 1, is open.
- **Higher-dimensional separators.** Theorem 1 holds in any dimension.
  Lemma 2 does not (Section 3). In dimension `k >= 2`, affine cell
  approximations can fail at first order at boundary pinch sets ([K],
  after Proposition 5.4). An upper half there needs either smooth value
  functions near pinch sets or richer cell classes.
- **Constants.** Rule R3 uses 56–116 times more cells than the
  bound-driven rule `bd` on the tested instances. `bd` is certified by
  Theorem 1 and, since its partition coarsens R3's, inherits Theorem 3's
  count (Corollary 3.2). A sharper a-priori count for `bd` is open.
  Lemma 2 now has the sharp constants `(4, 4)` (Section 3; the earlier
  statement "at most a factor 2 too large" held only for the coefficient of
  `w(c)/h`). R3 still uses the first version's `(8, 8)`. The rule with
  `(4, 4)` is sketched after Theorem 3 and roughly halves the proven count.
  It was not run.
- **Scope of the computations.** Grid problems (exact on the grid, not
  the continuum), four instance families, `n <= 8`. My LP optimum over the
  class was computed only on grids with `m <= 257`. The review's
  cutting-plane LP, which I reran, extends the plateau to `m = 2049`.

## 10. Commands run

All from `theory-decomposition/covering/`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. These are
targeted checks only. No project-wide verification was run, and CI was not
consulted.

| Command | Log | Result |
|---|---|---|
| `python3 check_graded_split.py` | `logs/check_graded_split.log` | Theorem 1: 0 violations in 10,000; exactness; (e)–(i) as in 7.1 |
| `python3 check_kink_concentration.py` | `logs/check_kink_concentration.log` | Lemma 2: max ratio 0.274 |
| `python3 run_paths.py 16385 257` | `logs/run_paths.log` | table of 7.3 |
| `python3 check_naive_failure.py 129 257` | `logs/check_naive_failure.log` | naive plateaus; B.4 and `bd` pass (6 minutes) |
| `python3 check_prop4.py` | `logs/check_prop4.log` | Proposition 4 confirmed on the grid; reduced-band section added and rerun after review (earlier lines unchanged) |

Earlier smoke runs (`run_paths.py 257 65`, `run_paths.py 2049 129`) were
used only to debug; their output was not kept.

Commands run for the revision after review (same directory and thread
settings; targeted checks only, no project-wide verification, CI not
consulted):

| Command | Log | Result |
|---|---|---|
| `python3 check_kink_concentration.py` (extended) | `logs/check_kink_concentration.log` | earlier lines unchanged; two-kink family ratio 0.4856 to 0.5000; `w = 0` example `2 M h` |
| `python3 check_chain_discount.py` (new) | `logs/check_chain_discount.log` | chain LP: `1/(2n)` (two patterns), `1/n` (one pattern), `n = 2, 3, 4, 6, 8`, `m = 21, 41`; 60 random trees: LP value = `min m/(2 sum w)` to `1.5e-15`; exit 0 |
| `python3 check_prop4.py` (extended) | `logs/check_prop4.log` | reduced band: concavity intervals, widths and bracket `beta` as in 7.4; exit 0 |
| `python3 check_bd_coarsening.py 16385` (new, 72 s) | `logs/check_bd_coarsening.log` | `g - B <= -7.0e-5` (logged maximum `-7.08e-5`) on 47,782 cells; `bd` coarsens R3 in all 8 runs; exit 0 |
| `python3 indep_naive.py 513 1025 2049`, run from `../../reviews/covering-upper-half-review-checks/` (the review's script, 2 min) | `logs/rerun_review_indep_naive_fine.log` (in `covering/`) | identical to the review's log apart from timings |

`check_graded_split.py`, `run_paths.py` and `check_naive_failure.py` were
not changed and not rerun. The figures quoted from their logs in R2 and R6
were reread from the existing logs.

Commands run for revision round 2 (same directory and thread settings;
targeted checks only, no project-wide verification, CI not consulted):

| Command | Log | Result |
|---|---|---|
| `python3 check_kink_concentration.py` (extended again, 4 s) | `logs/check_kink_concentration.log` | first 15 lines identical to the round-1 log; random pairs at most 0.5475 of `4 w/h + 4 M h`; sharpness family ratio `0.999995`–`0.999998` at `delta = 1e-6` for all five `(W, M, h)`, `U - L >= -6.6e-16`; exit 0 |
| `python3 check_kink_sharp_lp.py` (new, 0.5 s) | `logs/check_kink_sharp_lp.log` | LP over grid-convex `phi`: optimum below `4 W/h + 4 M h` in all 18 runs, ratio 0.9961 at `m = 512`; exit 0 |
| `python3 check_prop5_slopes.py` (new, 0.2 s) | `logs/check_prop5_slopes.log` | constant minorants: gap 1.6–280 `eps`; balanced-minimizer slopes: gap 0; perturbed slopes: gap at most `0.498 eps`; exit 0 |

The final version of each script was run twice, and the second run
reproduced the log exactly. An earlier run of the extended
`check_kink_concentration.py` used the flawed first draft of the sharpness
family and exited with status 1 (Section 7.2).
`check_bd_coarsening.log`, `check_naive_failure.log` and `check_prop4.log` were only reread
(items T3, T4 and M2). No other script was changed or rerun.

## Revision after review

Review: [`../reviews/covering-upper-half-review.md`](../reviews/covering-upper-half-review.md)
(round 1). The review found no gap in the proofs. It found wrong or
imprecise side claims. I checked each item myself before changing the note.
No theorem changed. One sketch was replaced by a proof (R3), and one
extension was written out as a lemma (R7).

- **R1 (Lemma 2 sharpness; Summary, Status, Section 3, Section 7.2).**
  *Claim withdrawn:* "the constant 8 is loose by about 4". *Check:* I
  verified the review's family by hand. `U = -J(s - 1/2 + delta)_+` is
  concave and `L = J(-1/2 + delta - s)_+ - J(1/2 + delta)` is convex. `L <= U`
  holds on `[-1, 1]`, `w(0) = J(1/2 + delta)`, and both kinks lie inside
  `[-1/2, 1/2]`, so `Delta_U = Delta_L = J + M`. I added the family to
  `check_kink_concentration.py` (exact one-sided derivatives; `U >= L` on a
  200,001-point grid). The ratios are 0.4856 to 0.5000. So the coefficient
  of `w(c)/h` cannot go below 4, and the constant is at most a factor 2 too
  large. I also added the example `U = L = -M s^2/2` (coefficient of `M h`
  at least 2). The 0.274 and 0.25 figures remain, labelled as properties of
  those families only.
- **R2 (framing of Proposition 4; Summary item 5, Status, Sections 4, 5,
  7.3, 7.4, 8, 9).** *Claims withdrawn:* "per-edge control of cell
  placement fails" and "a joint exact split is needed, not only a joint
  choice of values on per-edge cells". *Check:* rule R3 (Section 4)
  computes `B(D)` from `w_e`, `M_e`, `G_e`, `n` and `eps` only, and `bd`
  uses the sliver of edge `e` only. The logs of `run_paths.py` and
  `check_naive_failure.py` show the LP-optimal joint values failing on the
  naive cells (for example `1.27e-2` at `n = 6`, `eps = 1e-3`) and passing
  on `bd`'s cells. The corrected statement is that cell placement by
  one-edge *band brackets* fails, while placement by margin and curvature
  (R3, B.4) or by the sliver bracket (`bd`) works and is still decided edge
  by edge. The negative result (Proposition 4 and the LP plateau) is kept.
- **R3 (optimality of the discount; Summary item 2, Status, Remark 1.2,
  new Proposition 1.3, Sections 8, 9).** *Sketch replaced by a proof.* I
  checked the review's argument and wrote it for trees, with alternating
  signs by depth: any bound of the form (b) with discount `c w_e` forces
  `2c sum_e w_e(x_{S_e}) <= m(x)`. On the chain of copies, where
  `w_e = s^2 = m(s, ..., s)`, this gives `c <= 1/(2n)` for every split. I
  also noted that the two-pattern condition is exactly this inequality on
  trees, because the DP split of `F - 2c sum_e w_e` is exact. *Check:* a new
  LP (`check_chain_discount.py`, my own code) gives `1/(2n)` with both
  patterns and `1/n` with one, for `n = 2, 3, 4, 6, 8` and `m = 21, 41`. On
  60 random small trees, the LP value equals `min m/(2 sum w)` to
  `1.5e-15`.
- **R4 (per-level admissibility sketch, Section 6).** *Intermediate step
  corrected.* `eps + 2 max(m, eps) <= 2(eps + m)` is false for `m < eps/2`.
  I checked the case analysis: `eta_0 = eps`, and
  `eta_j = 2 eta_{j-1} < 2 m(x)` for `j >= 1`. So `eta_j <= max(2m, eps)`,
  and `eps + max(2m, eps) <= 2(eps + m)`. The conclusion is unchanged.
- **R5 (Proposition 4, "What it shows").** *Two statements restricted.*
  `U'_1` is concave only on `|s1| <= 1 - beta/kappa` and convex beyond.
  The width `beta(kappa - 2 beta)/(kappa - beta) s1^2` near 0 is of order
  `s1^2` only for `kappa > 2 beta`, and zero for `kappa = 2 beta`. The
  statement that the reduced band contains no affine function is kept, with
  a one-line proof that covers `kappa = 2 beta`. *Check:* closed forms
  derived by hand. The new section of `check_prop4.py` confirms them on a
  2001-point grid, including zero width (`1.4e-17`) for `kappa = 2 beta` and
  a one-cell bracket equal to `beta`.
- **R6 (Section 7.4, Summary, Section 5).** *Sentence restricted.* I reread
  `logs/check_naive_failure.log`. At `eps = 1e-2` the naive LP gap does
  decrease with the lower tolerance for `n = 2` (`6.64e-3` to `4.15e-4`),
  `n = 3` and `n = 4` (and likewise at `m = 129`). In the ten settings that
  miss the tolerance, the decrease is at most 4.4% in the logged values.
  The sentence now covers only those settings. The Summary's plateau
  figures (`eps = 1e-3`, `m = 257`) were already correct; "stays at" became
  "barely changes". I also reran the review's fine-grid script. Its output
  matches the review's log, so the plateau persists up to `m = 2049`.
- **R7 (Proposition 5).** *Lemma added.* Lemma 1' states Theorem 1' for
  leafwise relaxations, with leaf-dependent errors `err_{t,B}` and cell
  pieces used on closed cells, and gives the explicit bound. The proof
  notes that Steps 1–2 are pointwise in `(B, z)`. Proposition 5 now cites
  Lemma 1', and its proof spells out the `eps/2 + eps/2` accounting.
  *Check:* by hand against the proofs of Theorems 1 and 1'. No new
  computation; the existing Theorem 1' checks cover the pointwise
  inequality.
- **Trivial (Remark 1.1).** "Decreases by `1/n` per edge" now reads "drops by
  `(E_t - E_u)/n >= 1/n`, with equality on paths". Checked from
  `theta_t = (2E_t + 1)/(2n)` and `E_t >= E_u + 1`.
- **Optional, adopted: `bd` inherits Theorem 3 (new Corollary 3.2).** The
  validity proof of Theorem 3 gives `g_{e,D} <= B(D)` on every dyadic cell,
  so `bd` splits only cells that R3 splits. *Check:* new script
  `check_bd_coarsening.py` on D1–D4 (`m = 16385`, both tolerances):
  `g - B <= -7.0e-5` on all 47,782 dyadic cells that R3 tests, and every R3
  cell lies in one `bd` cell. Section 9 no longer says that `bd` has no
  a-priori count.
- **Optional, adopted: link to certificate size (new Corollary 3.3).** I
  checked the review's sketch and wrote it as a corollary. If `S_t ⊂ K_t`
  for every non-root bag, then
  `sum_e N_e <= ceil(sqrt(M/alpha)) 2^{w+1} N_dec(eps)`. It uses the
  bag-by-bag form of Theorem 2.5 of [D], as stated in the proof of
  Proposition B.1 of [E], a coordinate projection, and a subdivision of
  intervals. It replaces the loose parenthetical in "What this settles".
  No computation.
- **Optional, adopted: Ruozzi–Tatikonda (Section 8).** Added
  arXiv:1002.3239 after checking the arXiv abstract page (title, authors,
  dates, scope). I did not read the full paper.

### Revision after the confirmation review (round 2)

Review: [`../reviews/covering-upper-half-confirm-r1.md`](../reviews/covering-upper-half-confirm-r1.md).
It found two minor problems (M1, M2), six trivial points (T1–T6) and one
optional improvement (O1). I checked each item myself before changing the
note. All were adopted. T6 was adopted in a different form from the one
suggested, and T1 led to a stronger Lemma 2. Proposition 5's sufficient
condition was false as worded and is corrected (M1). No other statement
was weakened. Lemma 2 and Corollary 3.3 were strengthened.

- **M1 (Proposition 5, sufficient condition).** *Condition corrected.* The
  first bullet named the cells but not the slopes. The proof bounds the
  separator terms through the brackets at the balanced minimizers
  (paragraph after Lemma 1'), so it needs those slopes. *Check:* by hand,
  the review's example (`n = 1`, root `-lambda s + M s^2/2`, leaf
  `lambda s + M s^2/2`) has `psi' = lambda s`. A constant minorant on
  `[0, ell]` forces `f* - l_r >= lambda ell - M ell^2/2`. The new script
  `check_prop5_slopes.py` computes the R3-adapted cells and the exact
  certificate value. Constant minorants give gaps of 1.6 to 280 times
  `eps`, the balanced slope gives 0, and slopes perturbed up to the bracket
  bound give at most `0.498 eps`. The first bullet now requires the
  balanced-minimizer slopes, or any slopes whose intercept-minimized
  bracket is at most `eps/(2n)`. The proof says where they enter, and a
  paragraph records the counterexample.
- **M2 (Section 5, "not a thinning of the band width").** *Sentence
  restricted.* For `kappa = 2 beta` the reduced band has zero width on
  `|s1| <= 1/2` (closed form of R5, rechecked by hand; `check_prop4.log`
  shows the largest width `1.4e-17` on `|s| <= 0.2`). So the unrestricted sentence was wrong. It now
  reads "for `kappa > 2 beta`". The `kappa = 2 beta` case is named, and the
  common point (no affine function in the reduced band) is stated for both
  cases.
- **T1 (Lemma 2 sharpness; Summary, Status, Sections 3, 7.2, 8, 9).**
  *Claim corrected and strengthened.*
  - I confirmed the review's point: the two-kink family's ratio
    `(2J + 2M)/(8J(1/2 + delta) + 8M)` is below 1/2 for every `delta > 0`.
    "Reaches" should have been "approaches", and "at most a factor 2 too
    large" held only for the coefficient of `w(c)/h`.
  - While checking the coefficient of `M h`, I found that both constants
    can be halved. `phi = L_v - U_c` is convex, `w = M (s - c)^2 - phi`, and
    `Delta_U + Delta_L` is the slope rise of `phi`. Chord-slope bounds give
    `4 w(c)/h + 4 M h`. An explicit family, where `phi` is flat and then
    linear, approaches this bound for every `(w(c), M, h)`. So `(4, 4)` is
    optimal in each coefficient. The round-1 lower limit `b >= 2` was not
    tight.
  - *Check:* proof by hand. The extended `check_kink_concentration.py` has
    no violation in the random cases (at most 0.5475) and reaches ratio
    `0.999998` on the family. The new `check_kink_sharp_lp.py` is an LP
    over all grid-convex `phi`: its optimum stays below the bound and
    reaches 0.9961 of it at `m = 512`.
  - A first draft of the family used the wrong slope for `W = 0`, and the
    grid check caught it (Section 7.2).
  - Lemma 2 now states `(4, 4)` and their optimality. Section 4 keeps the
    weaker `(8, 8)`, so R3, Theorem 3 and all computations are unchanged.
    A remark after Theorem 3 sketches the rule with `(4, 4)`, which gives
    `(4n + 2) J~_e N_e + 4n J'_e`. I checked its steps by hand and did not
    run it.
  - The kink remark now reads `8 sqrt(M w(c))` and `w(c) >= J^2/(64 M)`.
    The round-1 entry R1 above is kept as a record; its phrase "at most a
    factor 2 too large" is superseded.
- **T2 (Section 5, "What it shows").** *Sentence corrected.* The
  margin-and-curvature description fits R3 and B.4's rule, not `bd`. *Check:*
  with `w_e = 0` at a pinch point and `psi_e` affine near it, the sliver
  bracket is `<= 0`, so `bd` does not refine. The M1 example
  (`psi' = lambda s`) is such a case. The sentence now names R3 and B.4
  and describes `bd`'s test separately. It also notes that in
  Proposition 4, `psi_1 = (kappa beta/(4(kappa + beta)) - 3 beta/2) s1^2`
  and `psi_2` are nonzero multiples of `s_e^2`, so `bd` refines there
  (computed by hand from the closed forms).
- **T3 (rounding; Section 4, Section 10 table, round-1 entry).**
  *Corrected.* `check_bd_coarsening.log` gives the maximum `-7.08e-05` (D2,
  `eps = 1e-3`), which is above `-7.1e-5`. All three places now say
  `<= -7.0e-5`.
- **T4 (Section 7.4).** *Corrected.* `check_naive_failure.log` shows a drop
  of more than a factor 10 in two settings: `n = 2`, `eps = 1e-2`, at
  `m = 129` (`6.07e-3` to `3.59e-4`) and at `m = 257` (`6.64e-3` to
  `4.15e-4`). No other setting drops by a factor 10. The text now says
  "two settings" and gives both.
- **T5 (notation).** *Renamed.* I confirmed the clashes by searching the
  text. `D` was the discount `1/(2n)` in the proof of Theorem 1 and also a
  cell. `D'` was the discount `1/(3n+1)` and also a cell in Proposition 5.
  `L_t` was the lower value function and also the leaf family. The
  discounts are now `tau` and `tau'`, and the leaf family is `Leaves_t`.
  Proposition 5's `l_{u,D'}` is `l_{u,D_u(B)}`. A notation item in
  Section 0 records this. I also renamed `l_e` in the proof of
  Corollary 3.3 to `l_c`, because (H3) uses `l_e` for the length of `I_e`.
- **T6 (Section 8, Ruozzi–Tatikonda).** *Paraphrase replaced.* I fetched
  the arXiv abstract again (arXiv:1002.3239). It uses graph covers twice:
  "a combinatorial characterization of these optima based on graph
  covers", and, for the conditions needed for convergence to a global
  optimum, which "can be too restrictive", "This limitation ... is
  characterized by graph covers". So the old
  paraphrase matched the first use but was loose ("the optima", no mention
  of the second use). The review's suggested wording covers only the
  second use. Section 8 now summarizes the abstract's four points and
  quotes both phrases. I still have not read the full paper.
- **O1 (Corollary 3.3).** *Adopted, slightly sharpened.* I checked the
  review's argument against [D] (proof of Theorem 2.5, Lemma 1.4) and
  [C], Section 1.1 (`d_i(y) = min(y_i - l_i, u_i - y_i)`, `a_i >= d_i^2`).
  For a single coordinate `S_e ⊂ K_t`, `x_i` lies within
  `sqrt((eps + eta)/alpha)` of one of the two endpoints of the leaf's
  projection, and inside the leaf. So `2 |Leaves_t|` intervals of length
  `sqrt((eps + eta)/alpha)` suffice. That is half the length the review
  used, because the intervals may stay inside the leaf. The factor becomes
  `2 ceil(sqrt(M/alpha)/2) <= sqrt(M/alpha) + 2` in place of
  `ceil(sqrt(M/alpha)) 2^{w+1}`. The Summary, the Status row and "What this
  settles" were updated. No computation.

### Root edits after the round-2 confirmation

The round-2 confirmation
([`../reviews/covering-upper-half-confirm-r2.md`](../reviews/covering-upper-half-confirm-r2.md))
returned "verified" with three trivial items and one optional wording item.
The root applied all four: the Lemma 2 sharpness ratio is given as
`0.999995`–`0.999998` in the Summary, the Status table and the Section 10
commands table; Section 7.2 notes that
the LP of `check_kink_sharp_lp.py` fixes `phi(0) = -W` and can exceed
`M s^2` between grid points (the script's docstring has the same
simplification; not edited); Section 5 gives the actual reason `bd` refines
near 0 in Proposition 4 (the round-2 revision entry T2 above keeps the
earlier, incomplete reason); and "the slope condition is needed" now reads
"a condition on the slopes is needed". No result changes.
