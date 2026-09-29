# Do stronger convexifications move the sparse-regression thresholds?

Workstream `sparse-regression/stronger-relaxations/`. Date: 2026-09-29.
Status: proofs and computations by the workstream owner. Independently
reviewed in
[`stronger-relaxations-review.md`](../../../reviews/stronger-relaxations-review.md),
which found Theorem 4.4 and its proof correct and the computations
reproducible. Revised in response (see "Revision after review"). Code is in [`code/`](code/), result files in
[`data/`](data/). The parent note is
[`../phase-transition.md`](../phase-transition.md), cited as [PT]; "PT 3.1"
means Theorem 3.1 there. Its reviews
([`sparse-easy-review.md`](../../../reviews/sparse-easy-review.md),
[`sparse-hard-review.md`](../../../reviews/sparse-hard-review.md),
[`sparse-recheck.md`](../../../reviews/sparse-recheck.md)) do not change the
results used here. The recheck's correction of the seed-1007 explanation
(many violators, not one) is consistent with Section 2 below.

## Summary

**Question.** In the random-design model of [PT] (Gaussian `X`, `k`-sparse
`beta*` with entries `±b`, noise `sigma`, ridge `lam`), the perspective
relaxation is root-exact iff `tau_lam^2 >= (2+o(1)) log p` and satisfies C1
(every single wrong fixing prunable, hence linear variable-branching trees)
iff `tau_lam^2 >= (2+o(1)) log(p lam/n)` (PT 3.1, 3.2). In samples:
`n ≈ 2k log p` and `n ≈ 2k log(p/sqrt n)`; for `k = p^gamma`,
`n = alpha k log p`: `alpha = 2` and `alpha = 2 - gamma`. Do the stronger
convexifications used in practice lower these constants?

**Answer for convexifications in the `(z, beta, beta beta')` lift: no
(Theorem 4.4, proved).** Let `L_r` be the relaxation in the variables
`(z, beta, B)` (with `B` a proxy for `beta beta'`) that imposes
`[[1, beta'], [beta, B]] ⪰ 0` and, on every set `T` of at most `r`
coordinates, the exact closed convex hull of the lifted mixed-integer set
`{(zeta, b, b b')}` without the cardinality constraint (equivalently, with it
when `r <= k`; Definition 1.1). `L_r` dominates

- the perspective relaxation;
- the optimal perspective relaxation of Dong–Chen–Linderoth (`= L_1`; Han–Gómez–Atamtürk show that it equals Shor's SDP in their nonnegative setting);
- the rank-one relaxations `sdp_r` of Atamtürk–Gómez;
- for `r >= 2`, every relaxation built from 2×2 decompositions with the free-sign 2×2 hull of Wei–Atamtürk–Gómez–Küçükyavuz (Proposition 2 of arXiv 2201.00387). This is the free-sign analogue of Han–Gómez–Atamtürk's `OptPairs`; `OptPairs` itself is for nonnegative continuous variables, is not valid for this model, and is not covered.

Our construction also satisfies the Shor lift in `(zeta, beta)` with
McCormick inequalities and the lifted cardinality constraint (Remark 4.5).
Under the assumptions (A) of [PT] and `r n log p = o(p)` (true for
`k = p^gamma`, `gamma < 1`), every relaxation `R` that is at least the
perspective relaxation at every node and at most `L_r` at the root and at the
forced-in nodes has exactly the same sharp thresholds. This includes solvers
that delete fixed-to-zero columns. The thresholds are:

- root exactness iff `tau_lam^2 >= (2 ± eps) log p`;
- C1 iff `tau_lam^2 >= (2 ± eps) log(p lam/n)` (the converse needs `k >= 20000/eps^2`);
- in samples, `n ≈ 2k log p` and `n ≈ 2k log(p/sqrt n)`; for `k = p^gamma`, `alpha = 2` and `2 - gamma`.

The exponential conflict-clique lower bounds of PT 4.3–4.4 (pure noise, low
total SNR) also hold for `L_2` (Corollary 4.6, proof sketch), with node bounds
taken from the root-lifted `L_2` (fixings only on `z`). Implementations that
delete fixed-to-zero columns are not covered.

**Mechanism.** The constant would change only if `R` priced the fractional
excess `pi(z, beta) = sum_j beta_j^2 (1/z_j - 1)` of the violating null
features at `lam (1 + c)` with `c` bounded away from 0 (Section 2). Local
lifts cannot do this when `p ≫ n`.

- A perspective point is the mean of a random support (Lemma 1.4). The lift `B` can hide that mixture's `X`-variance in the null space of `X`, using the null features with `z = 0` as helpers at ridge price.
- Local hull constraints are then satisfied by adding a small incoherent null-space component (Lemma 4.1).
- Quantitatively, for the root-lifted `L_r` (node convention after Definition 1.1), at every node containing `z`, `L_r <= ||y - X beta||^2 + lam ||beta||^2 + lam (1 + eps_p) pi(z, beta)`, with:
  - `eps_p = O(sqrt(r n log p/p))` for `L_r`;
  - `eps_p = O(sqrt(n/p))` for `L_2`, deterministically in terms of two design quantities (Lemma 4.1(ii));
  - `eps_p = O(n/p)` for the optimal perspective relaxation (Proposition 3.1, whose certificate part is Dong's).

**Finite sizes behave differently, and the computations show both
effects** (Section 7, `k = 3`, exact `OPT` by enumeration or by C1).

- *Gains at moderate `p/n`.* When `n/p` is not small, the SDPs are much stronger, as Dong observed for the optimal perspective relaxation.
  - At `n = 20`, `p = 40, 80`, `sdp_2` is root-exact in 5 of 8 runs, against 1 and 0 for the perspective relaxation.
  - At `n = 40`, `p = 100`, `SDP1` and `sdp_2` are root-exact in 8 of 8 runs, against 2.
- *Loss as `p/n` grows.* At fixed `n = 20`, `SDP1` closes 51%, 25%, 12% and 3% of the perspective root gap at `p = 40`, 80, 160 and 320, tracking `delta` (1.1, 0.53, 0.29, 0.14).
- *Inside the C1 window.* At `n = 40`, `p = 3200`, the perspective relaxation certifies `S*` by C1 but its root is inexact. There, explicit feasible points certify that the `L_2` root, and with it `sdp_2`, is inexact in 4 of 6 runs.
- *Where the helpers come from.* On the same instances restricted to the 60 strongest null features, `sdp_2` is exact. So the failure uses the thousands of `z = 0` helpers, exactly as in the proof.

**Beyond the `(z, beta, beta beta')` lift (Section 5).** The obstruction is
escaped by lifting the products `zeta_j beta_m` *into the PSD moment matrix
of `(1, zeta, beta)`*, not by non-locality alone.

- The pairwise second-order cones `U_jm^2 <= Z_jm B_mm` link the lifted moments `E[zeta_j beta_m]`, `E[zeta_j zeta_m]` and `E[beta_m^2]`. They are implied by the exact 2×2 hull of the richer lift `(zeta, beta, zeta zeta', zeta beta', beta beta')`, and they are 2×2 principal minors of the level-2 moment matrix.
- Together with Shor's lift of `(zeta, beta)` (the full moment matrix `Y ⪰ 0`) and McCormick inequalities they give an SDP, `zb`. We have not seen it analyzed in the sparse-regression literature.
- Pairwise, or `r`-wise, hulls of the full lift with PSD imposed only on `(1, beta, B)` are still defeated by the Section 4 construction: complete it with zero cross moments on the helpers (Remark 4.5).
- `r`-wise hulls of the full lift *together with* `Y ⪰ 0` are not covered by Theorem 4.4. Proposition 5.1 shows that already `r = 2`, with `Y ⪰ 0`, escapes its obstruction.
- Proposition 5.1 (proved): `zb` prices the fractional excess on a support `A` at `lam + lambda_min(X_A'X_A)`, about `lam + n` when `|A| ≪ n`.
- Proposition 5.3 (proved): on a support `A`, `zb` loses at most the fraction `(Lambda_max - Lambda_min)/(lam + Lambda_max)` of the overfit gain `OPT - f(A)`. The perspective relaxation's factor is `Lambda_max/(lam + Lambda_max) ≈ 1`. For a fixed `A` of size `s` independent of `X`, the fraction is about `4 sqrt(s/n)`. Uniformly over all supports of size `s` it is of order `sqrt(s log(p/s)/n)`, by a union-bound upper bound and a matching lower bound from a data-dependent support. So it is small only when `s log(ep/s) = o(n)`, and at `s ≈ k`, `n ≈ 2k log p` it is `Theta(1)`.
- Computations:
  - in the planted runs `zb` is exact in 39 of 40 nested runs (`p <= 200`) and in 19 of 20 runs of the parent note's family at `p = 100`, including runs where the perspective relaxation and `SDP1` close little of their gap;
  - in pure noise it is exact for small `k`, but inexact in every run with `k = 8`, `alpha <= 2`, with gaps about 14 times smaller (median) than the perspective relaxation's.
- Whether its threshold constant is below 2 is open (Question 5.4). A heuristic points to between `alpha = 2(1 - gamma)` and `2 - gamma`.

**Computational barriers (Section 6).** The literature summarized by
Bandeira, El Alaoui, Hopkins, Schramm, Wein and Zadik (BAHSWZ, arXiv
2205.09727) suggests that approximate recovery is computationally hard below
`n ≈ 2k log(p/k)`, that is `alpha = 2(1 - gamma)`. BAHSWZ themselves prove
that a simple thresholding algorithm achieves approximate recovery above it.

- BAHSWZ's own low-degree analysis proves hardness of *detection* below `alpha = 2(1 - sqrt gamma)^2` for `gamma < 1/4`. This tends to 2 as `gamma -> 0`.
- The authors add that for larger `gamma` their bound does not suggest a sharp recovery threshold.
- A polynomial-size relaxation that is root-exact, with a unique optimum, is a polynomial-time exact-recovery algorithm. Exact recovery is harder than approximate recovery, so the inference goes in the right direction. The barriers therefore forbid root exactness only below about `alpha = 2(1 - gamma)` (conjecturally), not below 2.

- For `gamma > 0` the known barriers leave the windows `2(1 - gamma) < alpha < 2` (root) and `2(1 - gamma) < alpha < 2 - gamma` (C1) open.
- Theorem 4.4 closes them only for relaxations in the `(z, beta, beta beta')` lift. Any relaxation that enters them must lift the products `zeta_j beta_m` (or use other extended variables) or use global constraints.
- As `gamma -> 0` all thresholds merge at 2. In that limit the constant 2 is optimal for polynomial relaxations, conditionally on the low-degree conjecture. For every `delta > 0` there is `gamma_0 > 0` such that, for each fixed `gamma in (0, gamma_0)`, low-degree detection fails below `alpha = 2 - delta` (BAHSWZ). Arpino's reduction then rules out polynomial-time approximate recovery there, and hence root exactness. This also rests on the heuristic model transfer of Section 6.1 (binary signals, BAHSWZ's normalization with `sigma^2 = o(k)`). BAHSWZ's theorem is stated for fixed `gamma > 0`. The case `log k = o(log p)` itself (`gamma = 0`) lies outside it and is not claimed.
- We found no sum-of-squares lower bounds for this problem.

## 1. Setting and relaxations

### 1.1 Notation

As in [PT, Sections 1.1–1.2, 3.1]:

- `X in R^{n x p}` has iid `N(0,1)` entries; `y = X beta* + sigma w`; `|S*| = k`.
- `f(S) = min_b ||y - X_S b||^2 + lam ||b||^2`, with minimizer `beta^S`.
- `r = r_{S*}` is the ridge residual, `a = X'r`, `m0 = lam min_{i in S*} |beta^{S*}_i|`, and `tau_lam`, `L_lam = log(p lam/n)` and (A) are as in PT 3.1.
- `K = {z in [0,1]^p : sum z <= k}`, and `K(S0,S1)` is the face of `K` with `z_{S0} = 0` and `z_{S1} = 1`.

New notation:

- `Q = X'X + lam I` and `c = X'y`.
- The lifted objective is `Phi(beta, B) = y'y - 2c'beta + <Q, B>`, so `Phi(beta, beta beta') = ||y - X beta||^2 + lam ||beta||^2`.
- For `z in K` and `beta` with `beta_j = 0` whenever `z_j = 0`:
  - the perspective objective `P(z, beta) = ||y - X beta||^2 + lam sum_{z_j > 0} beta_j^2/z_j`, whose minimum over `beta` is `g(z)` (PT (F2));
  - the fractional excess `pi(z, beta) = sum_{z_j > 0} beta_j^2 (1/z_j - 1)`, so that `P = ||y - X beta||^2 + lam ||beta||^2 + lam pi`;
  - for `eps >= 0`, the inflated perspective objective `P_eps(z, beta) = ||y - X beta||^2 + lam ||beta||^2 + lam (1 + eps) pi(z, beta)` and `g_eps(z) = min_beta P_eps(z, beta)`, so `g_0 = g`.

### 1.2 The relaxations

For `T ⊆ [p]` let

```
H_T = cl conv{ (zeta, b, b b') : zeta in {0,1}^T, b in R^T, b_j = 0 whenever zeta_j = 0 }  ⊂ R^T x R^T x S^T.
```

**Definition 1.1.** For an integer `r >= 1` and a node `(S0, S1)`,

```
L_r(S0,S1) = inf { Phi(beta, B) :  z in K(S0,S1),  [[1, beta'], [beta, B]] ⪰ 0,
                                   (z_T, beta_T, B_T) in H_T  for all T with |T| <= r }.
```

Two conventions matter.

- *Cardinality.* `H_T` has no cardinality restriction. For `r <= k`, adding `|zeta| <= k` inside `H_T` changes nothing. For `r > k` (allowed in Theorem 4.4 when `k` is small), `L_r` is weaker than the exact hull of the cardinality-constrained set on `r`-sets. Lemma 1.2(b) fails for that hull: with `k = 1` it forces `B_jm = 0` on pairs.
- *Nodes.* `L_r(S0, S1)` imposes the root hulls `H_T` and fixes only `z`. A feature `m in S0` keeps a free `B_mm >= 0`, since `H_{{m}} ∩ {z_m = 0} = {(0, 0, B) : B >= 0}`, and it can serve as a helper in Section 4. The node bound of a convex-piece node `Q_v` is `inf_{z in K ∩ Q_v} R(z)`, where `R` is the projected root-lifted function. Solvers that delete fixed-to-zero columns, or the exact hull of the node's own feasible set, have `B_{m·} = 0` and can give larger node bounds. Theorem 4.4 does not depend on this convention (see its statement). At a forced-in node `(∅, {j})` the exact hull of the node's own feasible set coincides with `L_r(∅, {j})`, provided the cardinality constraint is dropped inside `H_T` or `r <= k`. Points with `zeta_j = 0` of vanishing weight contribute only a PSD recession term with zero row `j`, which points with `zeta_j = 1` also generate (Lemma 1.2(b)). For `r > k` the node's own cardinality-constrained hull is stronger, as in the cardinality convention above. Corollary 4.6 does depend on the node convention.

The relaxations from the literature, in this notation (all node versions add
`z in K(S0,S1)`):

- **Perspective** (PWE's Boolean relaxation; Xie–Deng): `g(z)`, minimized over `z`.
- **Optimal perspective** `SDP1` (Dong–Chen–Linderoth, arXiv 1510.06083; `sdp_1` of Atamtürk–Gómez): `[[1, beta'], [beta, B]] ⪰ 0` and `beta_i^2 <= z_i B_ii`. By duality it equals the best relaxation obtained by splitting `Q = R + diag(mu)`, `R ⪰ 0`, `mu >= 0`, and applying the perspective to `mu_i beta_i^2`. Han–Gómez–Atamtürk (arXiv 2004.07448, Theorem 1) prove it equal to Shor's SDP in `(z, beta)`, for nonnegative continuous variables.
- **Rank-one `sdp_r`** (Atamtürk–Gómez, arXiv 1901.10334, formulation (20), read): `SDP1` plus, for every `|T| <= r`, some `w_T` with `0 <= w_T <= min(1, sum_{j in T} z_j)` and `[[w_T, beta_T'], [beta_T, B_T]] ⪰ 0`. It is the optimal decomposition of `Q` into PSD pieces supported on sets of size at most `r`, each strengthened by their rank-one hull `(a'beta)^2 <= t min(1, z(T))` (their Theorem 1).
- **2×2 hulls, free signs** (Wei–Atamtürk–Gómez–Küçükyavuz, arXiv 2201.00387, Proposition 2): the exact convex hull of the epigraph of a bivariate convex quadratic with indicators and free continuous variables, applied to the 2×2 pieces of a decomposition of `Q`. This is the free-sign analogue of `OptPairs` of Han–Gómez–Atamtürk (arXiv 2004.07448). `OptPairs` itself is built for nonnegative continuous variables. Its hull is smaller: with `b >= 0` every lifted point has an entrywise nonnegative `B`. It is not valid for the free-sign model with `beta*_i = ±b`, and it is not dominated by `L_2`. The disjunctive 2×2 decompositions of Frangioni–Gentile–Hungerford (not read; per Wei et al. and the review), adapted to unbounded variables, are covered as well. With explicit bounds `l <= beta <= u` they use information this model does not have.
- **Beyond the `(z, beta, beta beta')` lift**: the moment relaxation `zb` of Section 5.

**Lemma 1.2 (hull calculus).** Let `T' ⊆ T ⊆ [p]`.

- (a) If `(z', b', B') in H_{T'}`, its extension by zeros lies in `H_T`.
- (b) If `(z, b, B) in H_T` and `N in S^T_+`, then `(z, b, B + N) in H_T`.
- (c) `H_{{i}} = {(z, b, B) : 0 <= z <= 1, B >= 0, b^2 <= z B}`. Hence `L_1 = SDP1`.
- (d) If `A ⊆ R^T x R^T x S^T` is closed and convex and contains every `(zeta, b, b b')` with `supp b ⊆ supp zeta`, then `H_T ⊆ A`.
  Consequently `L_r >= sdp_r` at every node, and `L_2` is at least any relaxation obtained from a decomposition `Q = R + sum_{|T| = 2} Q_T` (`R ⪰ 0`, `Q_T ⪰ 0`) by replacing each `beta_T' Q_T beta_T` with the closed convex envelope of `(zeta, b) -> b'Q_T b` on the mixed-integer set.

*Proof.*

- (a) Zero extension maps generating points to generating points and commutes with convex combinations and limits.
- (b) It suffices to take `N = v v'`. For `eps in (0,1)`, the point `(1 - eps)(z, b, B) + eps (1_T, v/sqrt(eps), v v'/eps)` lies in `H_T`, since `(1_T, w, w w')` with `w = v/sqrt(eps)` is a generating point. It equals `((1-eps) z + eps 1_T, (1-eps) b + sqrt(eps) v, (1-eps) B + v v')`, which tends to `(z, b, B + v v')`. `H_T` is closed.
- (c) The generating points are `(0, 0, 0)` and `(1, b, b^2)`, and the closed perspective cone of `b^2` is the stated set.
- (d) `A` contains the convex hull of the generating points and is closed.
  - *`sdp_r`.* The set `{(z, b, B) : 0 <= z <= 1, ∃ w in [0, min(1, 1'z)], [[w, b'], [b, B]] ⪰ 0}` is convex and closed, since it is the projection of a closed convex set along the compact coordinate `w`. It contains every generating point: take `w = 1` if `zeta ≠ 0`, and `w = 0`, `b = 0` if `zeta = 0`.
  - *Decompositions.* The closed convex envelope `f_{Q_T}` satisfies `f_{Q_T}(z, b) <= <Q_T, B>` on `H_T`. The reason is that `(z, b, <Q_T, B>)` is a limit of convex combinations of the epigraph points `(zeta, b, b'Q_T b)`. With `B ⪰ beta beta'` (so `<R, B> >= beta'R beta`), the value of `L_2` is at least that of the decomposition relaxation. ∎

**Lemma 1.3 (order and validity).** At every node,
`min_z g <= SDP1 = L_1 <= L_2 <= ... <= min{ f(T) : |T| <= k, S1 ⊆ T, T ∩ S0 = ∅ }`.
The projected function `R(z) = inf{Phi : (z, beta, B) feasible}` of each of
these relaxations is convex. So PT Lemmas 1.2–1.4 (path lemma, conflict
bound) hold with `R` in place of `g`, for branching on `z` (variable, split,
SOS or general convex pieces in `z`-space), with node bounds
`inf_{z in K ∩ Q_v} R(z)` as in the node convention after Definition 1.1.

*Proof.* For validity, `(1_T, beta^T, beta^T beta^T')` is feasible with
`Phi = f(T)`. For the first inequality, the constraints give
`B - beta beta' ⪰ 0` and `B_ii >= beta_i^2/z_i`. So
`Phi = ||y - X beta||^2 + lam ||beta||^2 + <X'X, B - beta beta'> + lam tr(B - beta beta') >= P(z, beta) >= g(z)`.
Convexity holds because the projection of a convex program's value onto some
of its variables is convex. ∎

**Lemma 1.4 (perspective points are means of random supports).** Let
`z in K(S0,S1)` and let `beta` vanish where `z` does. There is a random set
`T` with, almost surely, `|T| <= k`, `S1 ⊆ T` and `T ∩ S0 = ∅`, and with
`P(j in T) = z_j`. Put `b_j = beta_j/z_j` (0 if `z_j = 0`) and
`xi = b ⊙ 1_T`. Then:

- `E xi = beta`;
- `D := Cov(xi) = diag(b)(E[1_T 1_T'] - z z')diag(b)` has `tr D = pi(z, beta)`;
- for every `T' ⊆ [p]`, `(z_{T'}, beta_{T'}, (beta beta' + D)_{T'}) in H_{T'}`;
- `Phi(beta, beta beta' + D) = P(z, beta) + <X'X, D>`.

*Proof.* The constraint matrix of `K` (identity rows and one all-ones row) is
totally unimodular. So `K` and its face `K(S0,S1)` are integral polytopes,
and `z` is a convex combination of 0/1 points of the face. Then
`E xi_j = b_j z_j = beta_j` and `Var xi_j = b_j^2 z_j (1 - z_j) = beta_j^2 (1/z_j - 1)`.
The third item holds because the moment point is a convex combination of
generating points. For the last item,
`Phi = ||y - X beta||^2 + lam ||beta||^2 + <Q, D>` and `lam tr D = lam pi`. ∎

So the perspective relaxation is the random-support average with the
`X`-variance `<X'X, D>` of the fit dropped. Every exact convexification must
pay it; the question is how much of it a relaxation pays.

## 2. What would have to change

By PT Corollary 2.4, the perspective root is exact at `S = S*` iff
`max_{l ∉ S} |a_l| <= m0`. Its failure direction moves mass `t` from the
weakest true feature `i` to a violator `l`:
`g(1_S - t e_i + t e_l) = f(S) - (t/lam)(a_l^2 - m0^2) + O(t^2)`. The null
correlations are iid `N(0, ||r||^2)` given `(X_S, w)`, with maximum
`||r|| sqrt(2 log p)`, and `m0 ≈ tau_lam ||r||`. This gives `2 log p`.

Suppose a relaxation priced the fractional excess of a coordinate at
`lam (1 + c)` instead of `lam`. The same computation (Section 4.3) gives
descent if `|a_l| > (1 + c) m0` (proved there for an upper bound). The
converse, no descent when `|a_l| < (1 + c) m0`, holds to first order for a
uniformly inflated relaxation by the dual computation of Corollary 5.2. It is
heuristic for the full relaxation. So the root threshold becomes
`(1 + c)^2 tau_lam^2 = 2 log p`. **A constant `c > 0` changes the constant 2
to `2/(1+c)^2`, and `c -> 0` leaves it unchanged.** The C1 balance of
PT Heuristic 3.8 changes the same way: violators are capped at `(1 + c) m0`
instead of `m0`. The question is therefore whether stronger convexifications
inflate the price of fractional null features by a constant factor.

Pairwise hulls look as if they should. For a pair `{m, j}` with `z_m = 0` and
`j` fractional, `H_{{m,j}}` requires
`[[B_mm, B_mj], [B_mj, B_jj - beta_j^2/z_j]] ⪰ 0`. A null feature at `z = 0`
may carry pseudo-second-moment `B_mm > 0`, but it may correlate with `j` only
through `j`'s slack above the perspective value. Section 4 shows that this
slack can be made tiny at negligible cost when `p ≫ n`. Section 5 shows that
a constraint on `E[zeta_j beta_m]` cannot be evaded this way.

## 3. The optimal perspective relaxation (`L_1`)

**Proposition 3.1.**

- (a) *(Certificate.)* Let `S` have `|S| = k`, and let `mu in R^p_+` satisfy:
  - `Q ⪰ diag(mu)`;
  - `mu_l > 0` whenever `l ∉ S` and `a_l ≠ 0` (here `a = X' r_S`);
  - `min_{i in S} mu_i (beta^S_i)^2 >= max_{l ∉ S} a_l^2/mu_l`.

  Then `SDP1(∅,∅) = f(S)`, and `S` is optimal. With `mu = lam 1` this is PWE's certificate (PT Corollary 2.4).
  This is the sufficiency half of Dong's Theorem 2 (arXiv 1603.04572, read). Dong proves the converse
  too, with `mu = lam d~` and `min_S mu_i (beta^S_i)^2` attained on all of `S`. We include the short
  weak-duality proof for completeness.
- (b) *(Pointwise bound.)* Let
  `delta := max_i x_i'(I + X_{-i}X_{-i}'/lam)^{-1} x_i / lam <= max_i ||x_i||^2/(lam + lambda_min(X_{-i} X_{-i}'))`.
  At every node and for every `z` in the node, `SDP1(z) <= g_delta(z)`. That is, the optimal perspective relaxation prices the fractional excess at most at `lam (1 + delta)`.
- (c) *(Size of `delta`.)* With probability at least `1 - 2/p`,
  `delta <= nu/((sqrt p - sqrt n - 2 sqrt(log p))^2 - nu)` with
  `nu = n + 2 sqrt(3 n log p) + 6 log p`. So `delta = O(n/p)` when `n = o(p)`.

*Proof.*

- (a) Fix a feasible `(z, beta, B)` and put `D_mu = diag(mu)`. Since `Q - D_mu ⪰ 0` and `B ⪰ beta beta'`, and `B_ii >= beta_i^2/z_i`,
  `Phi >= y'y - 2c'beta + beta'(Q - D_mu) beta + sum_i mu_i beta_i^2/z_i =: Psi(z, beta)`.
  For any `v in R^p`, `mu_i beta_i^2/z_i >= 2 v_i beta_i - z_i v_i^2/mu_i` (convention `0` when `mu_i = 0 = v_i`). Take `v = c - (Q - D_mu) beta^S`, with `beta^S` padded by zeros. Then `v_i = mu_i beta^S_i` for `i in S` (because `x_i' r_S = lam beta^S_i`) and `v_l = a_l` for `l ∉ S`. Hence
  `Psi >= y'y - 2(c - v)'beta + beta'(Q - D_mu) beta - sum_i z_i v_i^2/mu_i`.
  The quadratic in `beta` is minimized at `beta = beta^S`, because `c - v = (Q - D_mu) beta^S`, with value `y'y - beta^S'(Q - D_mu) beta^S`. By the hypothesis, the `k` largest values of `v_i^2/mu_i` are those on `S`, which equal `mu_i (beta^S_i)^2`. So
  `Psi >= y'y - beta^S' (Q - D_mu) beta^S - sum_{i in S} mu_i (beta^S_i)^2 = y'y - beta^S' Q beta^S = f(S)`,
  using `(Q beta^S)_S = c_S`. Hence `SDP1 >= f(S)`, and `SDP1 <= f(S)` by validity.
- (b) For fixed `(z, beta)`, the minimization over `B` is
  `min { <Q, E> : E ⪰ 0, E_ii >= d_i }`, with `E = B - beta beta'` and `d_i = beta_i^2 (1/z_i - 1)`. Both it and its dual `max { sum_i mu_i d_i : Q ⪰ diag(mu), mu >= 0 }` are strictly feasible, since `Q ≻ 0`. So they are equal.
  Every feasible `mu` has `mu_i <= 1/(Q^{-1})_ii`: take the vector `u` with `u_i = 1` minimizing `u'Qu`. By the Schur complement and Woodbury's identity, `1/(Q^{-1})_ii = lam + x_i'(I + X_{-i}X_{-i}'/lam)^{-1} x_i = lam(1 + delta_i)`. Hence `SDP1(z) <= min_beta [ ||y - X beta||^2 + lam ||beta||^2 + lam (1 + delta) sum_i d_i ] = g_delta(z)`. The second bound on `delta` uses `(I + A/lam)^{-1} ⪯ lam/(lam + lambda_min(A)) I`.
- (c) By (G3) of [PT], `s_min(X') >= sqrt p - sqrt n - 2 sqrt(log p)` with probability `>= 1 - p^{-2}`. By (G2) of [PT] and a union bound, `max_i ||x_i||^2 <= nu` with probability `>= 1 - p^{-2}`. Also `lambda_min(X_{-i}X_{-i}') >= lambda_min(XX') - ||x_i||^2`. ∎

By (b) and (c), the converses PT 3.1(b) and 3.2(b) hold for `SDP1` under
(A) and `n = o(p)`, with no helper split. The proofs are those of
Theorem 4.4(b) and (d) below with `eps_p` replaced by `delta`.

Dong's experiments (Gaussian ensemble, `p = 64`–`512`) found that the
optimal perspective relaxation needs "much fewer observations" than the
perspective relaxation. Parts (a)–(c) explain both findings. In the
certificate, the multipliers on the violating nulls may exceed `lam` by a
factor up to `1 + delta`. That factor is large when `n/p` is not small, for
example `delta ≈ 0.30` at `n = 20`, `p = 160` (median over our runs; `n/(sqrt p - sqrt n)^2 = 0.30`), and it
tends to 0 as `n/p -> 0`. So the asymptotic constant is unchanged, while
finite sizes show a real gain (Section 7).

## 4. Local hulls in the `(z, beta, beta beta')` lift: the thresholds are unchanged

### 4.1 Null-space completion

Let `(z, beta)` and `D` be as in Lemma 1.4. Let `F ⊇ supp z` and let
`Z1 ⊆ [p] \ F` satisfy `W := X_{Z1} X_{Z1}' ≻ 0` (so `|Z1| >= n`). Put:

- `P_N = I - X_{Z1}' W^{-1} X_{Z1}`, the projector onto the null space of `X_{Z1}` in `R^{Z1}`;
- `q_m = x_m' W^{-1} x_m = 1 - (P_N)_mm` for `m in Z1`;
- `theta_F = ||X_F' W^{-1} X_F||`;
- `Y = X_F D^{1/2}`.

**Lemma 4.1 (null-space completion; deterministic).** Fix `sigma > 0` and set
`G_F = sqrt(1+sigma) D^{1/2}` and `C = -X_{Z1}' W^{-1} X_F G_F` (rows `C_m`).
Let `G in R^{p x |F|}` have rows `G_F` on `F`, `C` on `Z1` and 0 elsewhere.
For a PSD matrix `K` on `Z1` with range in the null space of `X_{Z1}`, put
`B = beta beta' + G G' + K` (with `K` embedded in the `Z1` block). Then:

- (o) `Phi(beta, B) = P(z, beta) + lam [sigma pi + ||C||_F^2 + tr K]`, and `||C||_F^2 = (1+sigma) tr(Y' W^{-1} Y) <= (1+sigma) theta_F pi`.
- (i) *(General `r`.)* Let `eta = max_{M ⊆ Z1, |M| <= r-1} ||X_M' W^{-1} X_M|| < 1`, and let `K = kappa P_N` with `kappa = ((1+sigma)/sigma) max_{|M| <= r-1} ||C_M||^2/(1 - eta)`. Then `(z, beta, B)` is feasible for `L_r` at every node containing `z`, and `tr K = kappa (|Z1| - n)`.
- (ii) *(Pairs, weighted.)* Let `K = P_N Lambda P_N` with `Lambda = diag(||C_m||^2/(sigma (1 - q_m)^2))`. Then `(z, beta, B)` is feasible for `L_2`, and `tr K <= ||C||_F^2/(sigma (1 - max_m q_m))`. Consequently
  ```
  L_2(node) <= P(z, beta) + lam pi [ sigma + (1+sigma) theta_F (1 + 1/(sigma (1 - q_max))) ],
  ```
  and with `sigma` of order `sqrt(theta_F)` the bracket is `2 sqrt(theta_F) + O(theta_F)` when `q_max` is small.
- (iii) *(`r = 1`.)* With `K = 0` and `sigma -> 0`: `SDP1(node) <= P(z, beta) + lam theta_F pi`.

*Proof.*

- *PSD and objective.* Put `E = G G' + K ⪰ 0`. Then `[[1, beta'], [beta, B]] ⪰ 0`. `X G = X_F G_F + X_{Z1} C = 0` and `X_{Z1} K = 0`, so `<X'X, E> = 0` and
  `Phi = ||y - X beta||^2 + lam ||beta||^2 + lam tr E`.
  Also `tr E = (1+sigma) tr D + ||C||_F^2 + tr K`, `tr D = pi`, and `P = ||y - X beta||^2 + lam ||beta||^2 + lam pi`. Since `X_{Z1} X_{Z1}' = W`, `||C||_F^2 = tr(G_F' X_F' W^{-1} X_F G_F) = (1+sigma) tr(Y'W^{-1}Y) <= (1+sigma) theta_F tr D`. This proves (o).
- *Hull constraints.* Let `|T| <= r`, `T' = T ∩ F`, `M = T ∩ Z1`. On `T \ (F ∪ Z1)`, `z`, `beta` and `B` vanish. By Lemma 1.4, `(z_{T'}, beta_{T'}, (beta beta' + D)_{T'}) in H_{T'}`. By Lemma 1.2(a, b), it suffices that `B_T - embed((beta beta' + D)_{T'}) = E_T - embed(D_{T'}) ⪰ 0`. This is a principal submatrix of
  `Xi_M = [[E_MM, E_MF], [E_FM, E_FF - D]]`, and `E_FF - D = sigma D`, `E_MF = C_M G_F'`, `E_MM = C_M C_M' + K_MM`.
  If `M = ∅` or `T' = ∅`, the matrix is `sigma D_{T'}` or `E_MM`, both PSD. Otherwise `1 <= |M| <= r - 1`, and by the Schur complement it suffices that `K_MM ≻ 0` and
  `sigma D ⪰ G_F C_M' (C_M C_M' + K_MM)^{-1} C_M G_F'`.
  - (i) `K_MM = kappa (I - X_M' W^{-1} X_M) ⪰ kappa (1 - eta) I`. So the right side is `⪯ ||C_M||^2 G_F G_F'/(kappa (1-eta)) = ||C_M||^2 (1+sigma) D/(kappa (1 - eta)) ⪯ sigma D`.
  - (ii) Here `M = {m}`. `K_mm = sum_q (P_N)_{mq}^2 Lambda_q >= (1 - q_m)^2 Lambda_m = ||C_m||^2/sigma`. The right side is `⪯ ||C_m||^2 (1+sigma) D/(||C_m||^2 + K_mm) ⪯ sigma D`. If `C_m = 0`, then `E_mF = 0` and the condition is trivial.

  In (ii), `tr K = sum_m (1 - q_m) Lambda_m = sum_m ||C_m||^2/(sigma (1 - q_m))`.
- *(iii)* This is (o) with `sigma -> 0` and `K = 0`. `L_1` has no conditions with `M ≠ ∅`, and `E_FF = D` is the mixture's own covariance.

The node constraints hold because `z in K(S0,S1)`. ∎

In words: the lifted relaxation may pretend that the null features in `Z1`,
which have `z = 0` and `beta = 0`, carry a random coefficient vector. That
vector cancels the fluctuation `X_F (xi - beta)` of the random support fit
exactly, at ridge price `lam ||C||_F^2 ≈ lam (n/p) pi`. The extra independent
null-space component `K` keeps each helper's correlation with the fractional
coordinates below their slack `sigma D`. Local hull constraints see no
contradiction.

### 4.2 Random design bounds

Given `S*`, split the nulls `[p] \ S*` in increasing order into two halves
`H1`, `H2` of sizes `floor((p-k)/2)` and `ceil((p-k)/2)`. For a half `H`, let
`G_H = sigma(X_{[p] \ H}, w)`. Given `G_H`, the entries of `X_H` are iid
`N(0,1)`.

**Lemma 4.2.** Let `H` be a half, `m1 = |H|`, `W = X_H X_H'`, and let
`Y^{(1)}, Y^{(2)}` be `G_H`-measurable `n x s` matrices. With probability at
least `1 - 4/p`:

- (E1) `lambda_min(W) >= w_- := (sqrt(m1) - sqrt n - 2 sqrt(log p))^2`;
- (E2) `max_{m in H} ||x_m||^2 <= nu := n + 2 sqrt(3 n log p) + 6 log p`;
- (E3) for `u = 1, 2` and all `m in H`, `||x_m' W_{-m}^{-1} Y^{(u)}||^2 <= (1 + 2 sqrt(3 log p) + 6 log p) ||W_{-m}^{-1} Y^{(u)}||_F^2`, where `W_{-m} = W - x_m x_m'`.

On these events, if `w_- > r nu`, the quantities of Lemma 4.1(i) with
`Z1 = H` and `Y = Y^{(u)}` satisfy:

- `max_{|M| <= r-1} ||C_M||^2 <= (1+sigma)(r-1) ell_p ||Y||_F^2/(w_- - nu)^2`, where `ell_p = 1 + 2 sqrt(3 log p) + 6 log p`;
- `eta <= (r-1) nu/w_-`;
- `tr(Y'W^{-1}Y) <= ||Y||_F^2/w_-`.

*Proof.*

- (E1) is (G3) with `t = 2 sqrt(log p)`. (E2) is (G2) with `t = 3 log p` and a union bound.
- (E3): given `(X_{H \ {m}}, G_H)`, `x_m ~ N(0, I_n)` is independent of `A = W_{-m}^{-1} Y Y' W_{-m}^{-1}`. The Laurent–Massart bound for `x'Ax = sum_i lambda_i g_i^2` gives `x'Ax <= tr A + 2 sqrt(t) ||A||_F + 2t ||A|| <= (1 + 2 sqrt t + 2t) tr A` with probability `>= 1 - e^{-t}`. Take `t = 3 log p` and a union bound over `m` and `u`.
- For the consequences:
  - by Sherman–Morrison, `W^{-1} x_m = W_{-m}^{-1} x_m/(1 + x_m' W_{-m}^{-1} x_m)`, so `||C_m|| <= sqrt(1+sigma) ||x_m' W_{-m}^{-1} Y||`;
  - `||C_M||^2 <= ||C_M||_F^2 <= (r-1) max_m ||C_m||^2`;
  - `||W_{-m}^{-1} Y||_F <= ||Y||_F/lambda_min(W_{-m})`, and `lambda_min(W_{-m}) >= w_- - nu` (Weyl);
  - `||X_M' W^{-1} X_M|| <= ||X_M||_F^2/lambda_min(W)`;
  - `tr(Y'W^{-1}Y) <= ||Y||_F^2/lambda_min(W)`. ∎

**Corollary 4.3 (inflated-perspective comparison).** Assume (A) and
`r n log p = o(p)`. For `(z, beta)` and `D` as in Lemma 1.4, with
`F ⊇ supp z`, `F ∩ H = ∅`, `G_H`-measurable `(z, beta, D)` and
`||X_F||^2 <= 16 n`: on the events of Lemma 4.2 (with `Y = X_F D^{1/2}`), for
every node containing `z`,

```
L_r(node) <= P_{eps_p}(z, beta),   eps_p = sigma_p + C_1 n/p + C_2 (r-1) n log p/(sigma_p p) -> 0,
```

with `sigma_p = sqrt(r n log p/p)` and absolute constants `C_1`, `C_2`
(for large `p`). *Proof.* Combine Lemma 4.1(i) and Lemma 4.2, with
`||Y||_F^2 <= ||X_F||^2 pi`, `m1 >= (p - k)/2 - 1`, `w_- = m1(1 - o(1))` and
`nu = n(1 + o(1))`; `log p = o(n)` under (A). ∎

### 4.3 The thresholds

**Theorem 4.4.** Assume (A) of [PT], fix `eps in (0,1)`, and let
`r = r_p >= 1` satisfy `r n log p/p -> 0`. Let `R` be any node relaxation
with `R >= min_z g` at every node and `R <= L_r` at the root and at the
forced-in nodes `(∅, {j})`. (No column is fixed to zero at these nodes, so
solvers that delete fixed-to-zero columns are covered.) Then w.h.p.:

- (a) If `tau_lam^2 >= (2+eps) log p`, the `R` root equals `f(S*) = OPT`, `S*` is the unique optimum, and strict C1 holds for `R`.
- (b) If `tau_lam^2 <= (2-eps) log p`, the `R` root value is `< f(S*)`.
- (c) If `tau_lam^2 >= (2+eps) L_lam`, every single wrong fixing has `R`-bound `>= OPT + lam b^2/log p`. Every variable-branching tree with `R` bounds then has at most `2p+1` nodes, if the incumbent `OPT` is available when off-path nodes are examined or best-bound selection is used. This follows as in PT Lemma 1.2. PT's proof uses node bounds that increase with fixings, which a general `R` need not have. Here it suffices that `R >= g` at every node and that `g`'s node bounds increase with fixings: an off-path node `v` has `R(v) >= g(v) >=` the perspective bound of its single wrong fixing `> OPT`. The best-bound variant also uses validity of `R` (path nodes have bound `<= OPT`).
- (d) If `tau_lam^2 <= (2-eps) L_lam` and `k >= 20000/eps^2`, all but at most `2n/log^2 p` null features `j` satisfy `R(∅,{j}) < f(S*) - lam b^2/2`. So C1 fails for `R` whenever `S*` is optimal.
- (e) The sample-size forms of PT 3.1(c), 3.2(c) and PT Corollary 3.3 hold verbatim for `R`: root exactness is achievable iff `n >= (2+o(1)) k log p`, and C1 iff `n >= (2+o(1)) k log(p/sqrt n)`. For `k = p^gamma`, the thresholds are `alpha = 2` and `alpha = 2 - gamma`.

The same conclusions hold for `SDP1` under (A) and `n = o(p)`, by
Proposition 3.1.

*Proof.*

*(a), (c).* The `R` bounds are at least the perspective bounds at every node
(Lemma 1.3), and the conclusions are those of PT 3.1(a) and 3.2(a). The root
value is at most `f(S*)` by validity.

*(b).* Take the helper half `H = H1` and candidates in `H2`.

- As in the proof of PT 3.1(b), `m0 <= (1 + o(1)) sqrt((2 - eps) log p) ||r||` w.h.p. Given `(X_{S*}, w)`, the `a_l/||r||`, `l in H2`, are iid `N(0,1)`, and `P(max_{l in H2} |a_l| <= sqrt((2 - eps/2) log p) ||r||) <= exp(-2|H2| Phibar(sqrt((2 - eps/2) log p))) -> 0`.
- So w.h.p. some `l in H2` has `|a_l| >= (1 + c) m0` with `c := eps/12 <= 1`, because `sqrt((2 - eps/2)/(2 - eps)) >= 1 + 3 eps/32`. Fix such `l` (the maximizer) and `i in S*` with `lam |beta^{S*}_i| = m0`.
- Put `ebar = c/4`, `t0 = min(c/8, c lam/(8 nu))`, `s = t0 a_l/(lam (1 + ebar))`, `z = 1_{S*} - t0 e_i + t0 e_l` and `beta = beta^{S*} + s e_l`. Take the two-point mixture (support `S*` with probability `1 - t0`, support `S* - i + l` with probability `t0`), and `F = S* ∪ {l}`.
- All of these are `G_{H1}`-measurable. With probability `>= 1 - 1/p`, (G2) with a union bound over all `p` features gives `max_j ||x_j||^2 <= nu`, in particular for the violator `l in H2` (Lemma 4.2's (E2) covers only the helper half). With (G3) for `X_{S*}`, this gives `||X_F||^2 <= (||X_{S*}|| + ||x_l||)^2 <= 16 n`. For large `p`, `eps_p <= ebar`.
- By Corollary 4.3, `R(∅,∅) <= P_ebar(z, beta)`. The same algebra as in Section 2 gives
  ```
  P_ebar(z, beta) = f(S*) - 2 s a_l + s^2 (||x_l||^2 + lam) + lam (1 + ebar)[ beta_i^2 t0/(1 - t0) + s^2 (1 - t0)/t0 ]
                  <= f(S*) - (t0/lam)[ a_l^2/(1 + ebar) - (1 + ebar) m0^2/(1 - t0) - t0 a_l^2 ||x_l||^2/lam ].
  ```
- Divide the bracket by `a_l^2`. It is at least `(1 - c/4) - (1 + c/4)/((1 + c)^2 (1 - c/8)) - c/8`. Using `(1 + c/4)/(1 - c/8) <= 1 + c/2` and `(1 + c/2)/(1 + c)^2 <= 1/(1 + c) <= 1 - c/2` for `c in (0, 1]`, it is at least `c/8 > 0`. So `R(∅,∅) < f(S*)`.

*(d).* For `j in H2` take helper `H1`, and let `V' ⊆ H2 \ {j}` be the `N'`
elements of `H2` with the largest `|a_l|`. Symmetrically, for `j in H1` take
helper `H2` and `V' ⊆ H1`. Fix a half, and repeat the proof of PT 3.2(b)
inside it, with `kappa = lam b_+(1 + zeta)`, `delta0 = eps/16`, `t0` and
`N'` as there. The counts in a half are binomial with half the mean, which
changes no limit. The only change is the primal point bound, PT Lemma 2.5,
which becomes:

> **Lemma 2.5′.** Under the hypotheses of PT Lemma 2.5, and if
> `L_r(∅,{j}) <= P_ebar(z, beta)` for the point `(z, beta)` built there,
> then, with `e'_l = (|a_l| - (1 + ebar) kappa)_+`, `Q' = sum_{V'} e'^2_l`
> and `w_l = s sign(a_l) e'_l/L`,
> `L_r(∅,{j}) <= f(S) + (1 + ebar) lam b_+^2 [1 + (1+T)^2/(k-1-T)] - (2s - s^2) Q'/L`.

*Proof of Lemma 2.5′.* The point is `z_i = 1 - tau` on `S` with
`tau = (1+T)/k`, `z_j = 1`, `z_l = t_l = lam |w_l|/kappa` on `V'`, and
`beta = beta^S` on `S`, `w` on `V'`, 0 at `j`. Then:

- `lam ||beta||^2 + lam (1+ebar) pi <= lam ||beta^S||^2 (1 + (1+ebar) tau/(1-tau)) + (1+ebar) lam sum_l w_l^2/t_l`;
- `lam w_l^2/t_l = kappa |w_l|` and `tau/(1-tau) = (1+T)/(k-1-T)`;
- as in PT Lemma 2.5, `lam ||beta^S||^2 (1+T)/(k-1-T) <= lam b_+^2 [1 + (1+T)^2/(k-1-T)] + lam b_+^2 T` and `lam b_+^2 T <= kappa sum |w_l|`.

Collecting terms,
`P_ebar <= f(S) + (1+ebar) lam b_+^2 [...] - 2 sum_l |w_l| (|a_l| - (1+ebar) kappa) + ||X_{V'} w||^2`,
and the last two terms are at most `-(2s - s^2) Q'/L` as in PT. ∎

*Finishing (d).*

- Take `ebar = delta0/2`, a constant; `eps_p <= ebar` for large `p`. The mixture of Lemma 1.4 for this `z` is chosen on `S ∪ V'` (supports of size `<= k - 1`) together with `j`. Then `D` vanishes on the row and column of `j`, and `Y = X_{S ∪ V'} D^{1/2}` is one `G_H`-measurable matrix for all `j` in the half.
- `||X_{S ∪ V'}||^2 <= 16 n` by the bounds `||X_S|| <= 1.1 sqrt n` and `||X_{V'}|| <= sqrt(n)(1 + o(1))` from the proof of PT 3.2(b). So Corollary 4.3 applies.
- On `V'`, `|a_l| >= (1 + delta0) kappa`, so `e'_l >= (delta0/2) kappa` and `Q' >= N' (delta0/2)^2 kappa^2`. The rest of PT's proof goes through with `delta0/2` in place of `delta0`:
  - `N' >= 12 (1 + o(1)) n/(delta0^2 lam)` holds because `mu/(n/lam) -> inf` and `n/log^2 p ≫ n/lam`;
  - `T <= 6/delta0 = 96/eps`;
  - `(1+T)^2/(k-1-T) <= 1/2` once `k >= 2(1 + 96/eps)^2 + 1 + 96/eps`, which holds for `k >= 20000/eps^2`.
- With `s = 3 lam b_+^2 L/Q'`, the bound becomes `f(S) + (1 + ebar)(3/2) lam b_+^2 - 3 lam b_+^2 < f(S) - lam b_+^2`, and `b_+ >= b(1 - o(1))`.
- The exceptions are the at most `2N' <= 2n/log^2 p` elements of the two sets `V'`.

*(e).* The converse parts of PT 3.1(c) and 3.2(c) state that for
`n <= (2-eps) k log p` (respectively `(2-eps) k log(p/sqrt n)`), every `lam`
in (A) has `tau_lam^2 <= (2 - eps/2) log p` (respectively `L_lam`). Then (b)
and (d) apply. Achievability follows from (a) and (c). ∎

**Remark 4.5 (what is and is not covered).**

- *Shor lift in `(zeta, beta)`.* The point of Lemma 4.1 is realized by genuine random variables:
  - the random support `T` of Lemma 1.4;
  - `beta_F + (xi - beta) + sqrt(sigma) chi` on `F`, with `chi ~ N(0, D)` independent;
  - `C e + h` on `Z1`, where `e` is the standardized fluctuation `(1+sigma)^{-1/2} D^{+1/2}[(xi - beta) + sqrt(sigma) chi]` and `h ~ N(0, K)` is independent.

  So its moment matrix in `(1, zeta, beta)` is PSD. Its entries satisfy `Z_jj = z_j`, `U_jj = E[zeta_j beta_j] = beta_j` (lifted complementarity), all McCormick inequalities on `Z`, and `sum_m Z_jm <= k z_j`. Theorem 4.4 therefore also covers `L_r` intersected with this "Boolean + Shor" lift. What the construction violates is `E[zeta_j beta_m] = 0` for `z_m = 0`, `j ≠ m`, the consequence of `beta_m (1 - zeta_m) = 0` multiplied by `zeta_j`. That condition is pairwise. It follows from the product cone `U_jm^2 <= Z_jm B_mm` together with `Z_jm <= z_m`, both implied by the exact 2×2 hull of the full lift `(zeta, beta, zeta zeta', zeta beta', beta beta')` (Section 5). Pairwise hulls alone do not defeat the construction, though. Complete the point of Lemma 4.1 in the full lift with `Z`, `U` taken from the random-support mixture on `F`, and `Z_jm = U_jm = U_mj = 0` for helpers `m`.
  - On every `r`-set `T` the mixture restricted to `T` is a genuine distribution. The remainder `B_T - E[xi xi']_T` is the PSD matrix `Xi_M` of Lemma 4.1(i), or its pair version (ii), and it is a recession term. So the completion lies in the exact `r`-wise hull of the full lift for every `T`, and it satisfies all product cones and McCormick inequalities.
  - It keeps `[[1, beta'], [beta, B]] ⪰ 0` and `Phi`.
  - It violates only PSD of the full moment matrix `Y` of `(1, zeta, beta)`. The first completion above satisfies that PSD constraint but violates the product cones. The recheck confirms both numerically.

  So Theorem 4.4's proof also covers `r`-wise hulls of the full lift combined with PSD only on `(1, beta, B)`. What escapes is lifting the products `zeta_j beta_m` into the PSD moment matrix `Y`: `r`-wise hulls of the full lift together with `Y ⪰ 0` are not covered, and Proposition 5.1 shows that already `r = 2`, with `Y ⪰ 0`, escapes the obstruction.
- *Regime.* The proof needs `r n log p = o(p)`. When `n ≍ p`, `delta` and `eps_p` are constants, and the thresholds can move (Section 2). This is the regime of most small computations (Section 7).
- *Constants.* Theorem 4.4 is first-order, like PT 3.1–3.2. To first order (Section 2), pricing the fractional excess at `lam (1 + eps_p)` turns the root threshold `tau^2 = 2 log p` into `2 log p/(1 + eps_p)^2`. That is a factor, equivalently a downward shift of about `4 eps_p log p` in `tau^2`. The constant is unchanged because `eps_p -> 0`. The shift itself vanishes only if `eps_p log p -> 0`, for example when `r n log^3 p = o(p)`. Lemma 4.1(ii) makes `eps_p` computable (Section 7).
- *Spartrahedron.* The spartrahedral constraint `k Diag(B) ⪰ B` of Cifuentes–Li (arXiv 2603.18215) is global and is not covered. Our point violates it slightly at `p = 1000` (smallest eigenvalue `-0.015`; `verify_construction.py`). Whether it moves the thresholds is open.

**Corollary 4.6 (the hard side survives pairwise hulls).** Assume the
hypotheses of PT Theorem 4.3 (pure noise) or 4.4 (planted, low total SNR).
Then the conclusions hold with `L_2` (hence `sdp_2`, the free-sign 2×2
decomposition relaxations, and `SDP1`) in place of the perspective
relaxation, for convex-piece trees branching in `z` with node bounds
`inf_{z in K ∩ Q_v} R(z)`, where `R` is the projected root-lifted `L_2`
function (node convention after Definition 1.1): w.h.p. the `L_2` conflict
graph has a clique of size `C(p,k)^{c'}`. Implementations that delete
fixed-to-zero columns at nodes compute larger leaf bounds and are not
covered. A variable-branching leaf containing two clique members may have
fixed every helper to 0, and then the proof gives nothing.

*Proof sketch.* PT's clique consists of `k`-subsets `S, T` of the
top-correlated set with `|S \ T| >= m` pairwise, so each union `U = S ∪ T`
has `|U| <= 2k`. PT Lemma 4.2 bounds `g(mid)` by the value
`||y - t X_U c_U||^2 + 2 lam t^2 s_U` of `beta = t c_U` (supported on `U`).
The midpoint `z` (1 on `S ∩ T`, `1/2` on `S Δ T`) is the two-point mixture of
`S` and `T`. Lemma 4.1(ii) with `F = U` and `Z1 = [p] \ U` gives
`L_2(mid) <= P_{e2}(z, beta) <= ||y - X beta||^2 + (2 + e2) lam ||beta||^2`.
This is PT's bound with `2 lam` replaced by `(2 + e2) lam`. Here
`e2 = O(sqrt(theta_U))` with `theta_U <= ||X_U||^2/(lambda_min(XX') - ||X_U||^2)`.
Uniformly over all `|U| <= 2k`, `||X_U||^2 <= (sqrt n + sqrt(2k) + sqrt(4k log(ep/2k)))^2 = O(n)`
(since `k log(p/k) = O(n)` there). Also `lambda_min(XX') = p(1 - o(1))` and
`p/n -> inf` (`log(p/k) ≍ n/k -> inf` and `k = o(n)`). So `e2 -> 0`
uniformly, and PT's proof uses the penalty only through `lam = o(n)`. `OPT`
is unchanged. ∎ (We have checked the steps but not written out every error
term; label: corollary with proof sketch.)

## 5. Beyond the `(z, beta, beta beta')` lift: products of indicators and coefficients

**Definition 5.0 (`zb`).** The moment matrix
`Y = [[1, z', beta'], [z, Z, U], [beta, U', B]]` is PSD, with:

- `diag Z = z` and `diag U = beta` (lifted complementarity);
- McCormick: `0 <= Z_jm <= min(z_j, z_m)` and `Z_jm >= z_j + z_m - 1`;
- `sum z <= k` and `Z 1 <= k z`;
- the **product cones** `U_jm^2 <= Z_jm B_mm` for `j ≠ m`;
- node fixings on `z`.

The objective is `Phi(beta, B)`. *Validity:* for a random support `T` and
coefficients `xi` vanishing off `T`,
`E[zeta_j xi_m]^2 = E[zeta_j zeta_m xi_m]^2 <= E[zeta_j zeta_m] E[xi_m^2]`.
Each cone is a 3-dimensional rotated cone, so `zb` has one PSD block of size
`2p+1`, `p(p-1)` small cones and `O(p^2)` linear constraints.

*Where `zb` sits.* Apart from the global PSD constraint on `Y` and
`Z 1 <= k z`, every constraint of `zb` involves at most two coordinates.
Proposition 5.1 below uses the global PSD constraint and pairwise constraints
only, not `Z 1 <= k z`.

- *Implied by 2×2 hulls of the full lift.* At every generating point `(zeta, b)` with `b_m = 0` whenever `zeta_m = 0`, `(zeta_j b_m)^2 = zeta_j zeta_m b_m^2`: both sides vanish if `zeta_m = 0`, and `zeta_j^2 = zeta_j` otherwise. So the product cone holds with equality there. The cone `{U^2 <= Z B, Z, B >= 0}` is closed and convex, and adding a PSD recession term to `B` keeps it. Hence the exact 2×2 hull of `{(zeta, b, zeta zeta', zeta b', b b')}` implies the product cones and McCormick. The obstruction of Section 4 is escaped by lifting the cross products `zeta_j beta_m` into the PSD moment matrix `Y`. Without `Y ⪰ 0`, pairwise full-lift hulls are still defeated by the construction (Remark 4.5).
- *A sparse, partial level-2 moment relaxation.* Take the degree-4 (level-2 Lasserre) moment matrix in `(zeta, beta)` and reduce it by the ideal `zeta^2 = zeta`, `beta_m (1 - zeta_m) = 0`. Its 2×2 principal minor on the monomials `{zeta_j zeta_m, beta_m}` has entries `E[zeta_j zeta_m] = Z_jm`, `E[beta_m^2] = B_mm` and `E[zeta_j zeta_m beta_m] = E[zeta_j beta_m] = U_jm`. Its PSD-ness is exactly the product cone.
- *Exact hulls with switching variables.* Hulls of this kind for `n = 2`, such as Anstreicher–Burer, "Quadratic optimization with switching variables: the convex hull for n = 2" (Math. Program. 2021; from memory, not re-read; they treat bounded variables), imply the product cones as well.

**Proposition 5.1 (local pricing in `zb`).** For any feasible point of `zb`
with first moments `(z, beta)`, let `A = supp z` and
`Lambda_A = lambda_min(X_A' X_A)` (0 if `|A| > n`). Then

```
Phi(beta, B) >= ||y - X beta||^2 + lam ||beta||^2 + (lam + Lambda_A) pi(z, beta).
```

*Proof.* Write `Y` as a Gram matrix of vectors `v_0, v_{zeta_j}, v_{beta_j}`.
Put `w_j = v_{zeta_j} - z_j v_0`, `u_j = v_{beta_j} - beta_j v_0` (so
`B - beta beta' = Gram(u)`), let `F = {j : 0 < z_j < 1}` and
`Wsp = span{w_j : j in F}`.

- For `m ∉ A`: `beta_m^2 = U_mm^2 <= z_m B_mm = 0` (a 2×2 minor of `Y`), so `beta_m = 0`. The product cone and `Z_jm <= z_m = 0` give `U_jm = 0`. Hence `<u_m, w_j> = U_jm - z_j beta_m = 0` and `u_m ⊥ Wsp`.
- For `j in F`: `<u_j, w_j> = U_jj - z_j beta_j = beta_j (1 - z_j)` and `||w_j||^2 = z_j (1 - z_j)`.
- Let `g_q = P_Wsp u_q`. Then `Gram(u) ⪰ Gram(g)`, and `g_q = 0` for `q ∉ A`. So
  `<Q, B - beta beta'> >= <X_A' X_A + lam I, Gram_A(g)> >= (Lambda_A + lam) sum_{j in F} ||g_j||^2`,
  and `||g_j||^2 >= <u_j, w_j>^2/||w_j||^2 = beta_j^2 (1/z_j - 1)`. ∎

**Corollary 5.2.** Let `S = S*`, `i in S` with `lam |beta^S_i| = m0`, `l ∉ S`,
`A = S ∪ {l}`, `Lambda = lambda_min(X_A'X_A)` and `lam' = lam + Lambda`.
Along the perspective's failure direction `z_t = 1_S - t e_i + t e_l`,
`t in (0,1)`,

```
zb(z_t) >= f(S) + m0^2 [1/lam - 1/(lam + lam' t/(1-t))] - a_l^2 t/(lam t + lam' (1-t)).
```

To first order this is `f(S) + t [m0^2 lam'/lam^2 - a_l^2/lam']`. So `zb`
does not descend along this direction unless `|a_l| > (1 + Lambda/lam) m0`.
For `|A| ≪ n`, `Lambda ≈ n`, and in (A) `Lambda/lam >= (1 - o(1)) log^2 p`.
The perspective relaxation descends as soon as `|a_l| > m0`.

*Heuristic reading (not proved).* Corollary 5.2 and Proposition 5.3 suggest
that `zb` can be inexact only through points whose support is large enough
that `Lambda_A` is small, that is, comparable to `n`. There the fractional
features' own `X`-fluctuations can cancel each other. Proposition 5.3 does
not exclude a gap at a small support: it allows one whenever the fraction in
its bound times `OPT - f(A)` is positive.

*Proof.* By Proposition 5.1, `zb(z_t) >= min_beta [ ||y - X beta||^2 + sum_j c_j beta_j^2 ]`
with `c_j = lam + lam' (1/z_j - 1)` on `A` (`c_j = lam` where `z_j = 1`).
By weak duality this is `>= 2 a'y - ||a||^2 - sum_{j in A} (x_j'a)^2/c_j`
for every `a`. Take `a = r_S` and use PT Lemma 2.1 (`h(r_S, 1_S) = f(S)`,
`x_j' r_S = lam beta^S_j` on `S`) with `c_i = lam + lam' t/(1-t)` and
`c_l = lam + lam'(1-t)/t`. ∎

**Proposition 5.3 (how much of the gap `zb` can lose on a support).** Fix
a node, and let `OPT_v` be its integer optimum. Let `z` be in the node with
support `A`, and put `Lambda_± = lambda_max/min(X_A'X_A)` (`Lambda_- = 0` if
`|A| > n`) and `f(A) = min_{supp beta ⊆ A} ||y - X beta||^2 + lam ||beta||^2`
(ridge on all of `A`, which may have more than `k` elements). Then

```
zb(z) >= OPT_v - [(Lambda_+ - Lambda_-)/(lam + Lambda_+)] (OPT_v - f(A)),
g(z)  >= OPT_v - [Lambda_+/(lam + Lambda_+)] (OPT_v - f(A)).
```

The bound is deterministic. Its size depends on how `A` is chosen:

- For Gaussian `X` and a fixed `A` of size `s ≪ n` independent of `X`, `(Lambda_+ - Lambda_-)/Lambda_+ ≈ 4 sqrt(s/n)`, while `Lambda_+/(lam + Lambda_+) ≈ 1` in (A).
- For a data-dependent `A`, such as the support of a minimizing `z`, the relevant quantity is the worst case over `|A| = s`, which is of order `sqrt(s log(p/s)/n)`:
  - *Upper bound.* By (G3) with a union bound over the `C(p, s)` supports it is at most about `4 (sqrt s + sqrt(2 s log(ep/s)))/sqrt n`.
  - *Matching lower bound.* Take a column `j0` and the `s - 1` columns most correlated with it. Then `X_A'X_A ≈ n I` plus an arrow with entries `x_{j0}'x_l` of size about `sqrt(2 n log(p/s))`, so `Lambda_± ≈ n ± ||c||` with `||c||^2 ≈ 2 (s-1) n log(p/s)`. The fraction is about `2||c||/(n + ||c||)`.
  - *Numbers* (one Gaussian draw, `n = 2000`, `p = 10^4`, `s = 2, 5, 10, 20`). The data-dependent fraction is 0.15, 0.27, 0.38, 0.48, and the arrow formula gives 0.15, 0.27, 0.37, 0.48. For the fixed support `{1..s}` it is 0.02, 0.11, 0.22, 0.32.
  - So the fraction is small only when `s log(ep/s) = o(n)`, and it is `Theta(1)` at `s ≈ k`, `n ≈ 2k log p`, where `||c|| ≍ n`. The recheck reports about 0.80 at `s = k`, `n = round(2k log p)`.

So `zb` loses only a vanishing fraction of the overfit gain `OPT_v - f(A)` on supports with `s log(ep/s) = o(n)`, while the perspective relaxation, and by Section 4 every local hull in the `(z, beta, beta beta')` lift, can lose almost all of it. At the scale `s ≈ k` of the thresholds the bound alone does not decide exactness.

*Proof.* For `c >= 0` and `beta` supported on `A`, put
`G(beta) = ||y - X beta||^2 + lam ||beta||^2` and
`F_c(beta) = G(beta) + (lam + c) pi(z, beta)`.

- *`F_{Lambda_+} >= OPT_v`.* Take the random-support mixture of Lemma 1.4 for `(z, beta)`, with node-feasible supports. Its expected objective is `G(beta) + <X'X + lam I, D> <= G(beta) + (Lambda_+ + lam) tr D = F_{Lambda_+}(beta)`, because `D` is supported on `A`. Every realization costs at least `f(T) >= OPT_v`.
- *Interpolation.* With `s = (lam + Lambda_-)/(lam + Lambda_+)`, `F_{Lambda_-} = s F_{Lambda_+} + (1 - s) G >= s OPT_v + (1 - s) f(A)`, and `1 - s = (Lambda_+ - Lambda_-)/(lam + Lambda_+)`.
- By Proposition 5.1, `zb(z) >= min_beta F_{Lambda_-}(beta)`, which gives the first inequality. The second is the same argument with `c = 0`, since `g(z) = min_beta F_0`. ∎

Consequences.

- The depth of midpoint conflicts (PT Lemma 1.4) shrinks. For `z = (1_S + 1_T)/2`, the conflict depth `OPT - zb(mid)` is at most `(Lambda_+ - Lambda_-)/(lam + Lambda_+)` times `OPT - f(S ∪ T)`, where `|S ∪ T| <= 2k`. For the perspective relaxation the factor is about 1.
- In PT's pure-noise regime `k/n -> 0`, but `k log(p/k) ≍ n`, so `Lambda_+/Lambda_-` is not uniformly close to 1 over all `2k`-subsets. We therefore do not claim that PT 4.3 fails for `zb`; we only claim that its mechanism is much weaker. Section 7.4 shows `zb` exact on most of PT's pure-noise instances with small `k`, but not at `k = 8`.

**Question 5.4 (open).** What are the root-exactness and C1 thresholds of
`zb` in the model of [PT]? In particular, is its root threshold in `tau_lam^2`
still `2 log p`, or smaller by a constant factor?

What is proved:

- `zb` blocks the perspective relaxation's failure direction unless `|a_l| > (1 + Lambda/lam) m0` (Corollary 5.2). On supports with `s log(ep/s) = o(n)` it loses at most a vanishing fraction of the overfit gain (Proposition 5.3).
- The obstruction behind Theorem 4.4 does not apply to it (Remark 4.5).

What is not proved: that `zb` is exact anywhere below the perspective
thresholds. That needs a dual certificate against spread-out configurations
with `|supp z| ≳ n`, where `Lambda_A` is small.

*Heuristic (not proved).* A spread configuration can cancel its
indicator-driven `X`-variance in two ways:

- with fractional features whose columns span `R^n`, which needs at least `n` of them;
- with many helpers of small mass, whose correlations the product cones limit to `sqrt(z_m B_mm/z_j)`.

Balancing the helpers' ridge price and their share of the budget against the
violators' first-order gain suggests that `zb` becomes inexact once the
number of violators is between about `sqrt n` and `n`. That corresponds to
`tau_lam^2 ≈ 2 log(p/sqrt n)` to `2 log(p/n)`. For `k = p^gamma` this is
`alpha ≈ 2 - gamma` to `alpha ≈ 2(1 - gamma)`, and the latter is the
conjectured computational recovery threshold of Section 6. We have not
checked that such configurations are globally consistent (PSD). The count
only indicates that nothing obvious pins `zb` to the constant 2.

*Evidence (Section 7).* At `k = 3` and `n = 20, 40` (Sections 7.2–7.3, 7.5), `zb` is exact in 39 of
the 40 nested runs where it was solved in full (`p <= 200`) and in 19 of 20
runs of the parent note's family at `p = 100`. That includes 9 of the 10
runs where `S*` is not optimal; there `zb` returns the true optimum of
another support. It is inexact in the `n = 20`, `p = 160` run with 30 violators, and in
the parent-family run at `alpha = 1.5`, seed 1003 (gap `4.8e-4`, `S*`
optimal, 27 failing perspective nodes). It is certified inexact
(restricted) in 2 of 8 runs at `p = 320`, both with more than `n`
violators. In pure noise (Section 7.4) it is exact for small `k` and inexact
for `k = 8`, `alpha <= 2`, with gaps 3–400 times smaller than the
perspective relaxation's. This is consistent with the heuristic that `zb`
fails only through configurations that spread over about `n` coordinates or
more. With `k <= 8` and `n <= 140` it cannot determine asymptotic
constants.

## 6. Computational barriers

Model correspondence. Bandeira, El Alaoui, Hopkins, Schramm, Wein and Zadik
(arXiv 2205.09727, Section 3.2, read) treat sparse regression with Gaussian
design, binary `k`-sparse signal, `k = p^theta`, per-sample SNR growing
(`sigma^2 = o(k)`), and `n = R k log(p/k)`. In our parametrization
`alpha = R(1 - gamma)` with `gamma = theta`. They state:

- LASSO recovers exactly for `n > 2k log p`, that is `alpha > 2` (Wainwright);
- simple thresholding achieves approximate recovery for `R > 2`, that is `alpha > 2(1 - gamma)`;
- the information-theoretic threshold is `o(k log(p/k))`;
- degree-`o(k)` polynomials fail to detect for `R < R_LD(theta)`, that is `alpha < 2(1 - sqrt gamma)^2` for `gamma < 1/4` and `alpha < 1 - 2 gamma` for `1/4 <= gamma < 1/2`. Detection is easy above;
- a low-degree lower bound for recovery for all `R < 2` is posed as open. They say `R = 2` matches known algorithms as `theta -> 0`.

Gamarnik–Zadik (arXiv 1711.04952, abstract; COLT 2017 companion from memory)
prove the overlap gap property for `n <= c n_alg` with a small constant `c`.

Consequences for relaxations:

1. **Root exactness is recovery.** Suppose a relaxation computable in polynomial time is root-exact at `S*` w.h.p., with `1_{S*}` its unique optimal `z`, as happens with a strict dual certificate. Then solving it recovers `S*`. BAHSWZ's model differs slightly (binary signal, `sigma^2 = o(k)`), so the transfer is heuristic. With that caveat, the conjectured barrier for approximate recovery forbids root exactness below `alpha ≈ 2(1 - gamma)`. Root exactness gives exact recovery, which is harder than approximate recovery, so the inference goes in the right direction. The proven low-degree detection bound only reaches `2(1 - sqrt gamma)^2`, and it is evidence rather than a proof for SDPs. Nothing in this literature forbids a polynomial-size relaxation that is root-exact at `2(1 - gamma) < alpha < 2`.
2. **C1 already beats `alpha = 2`.** By PT 3.2 and Lemma 1.2(b) of [PT], perspective B&B with best-bound search recovers `S*` in at most `2p+1` convex solves at `alpha > 2 - gamma`. That is a polynomial-time exact recovery below LASSO's `alpha = 2`, consistent with the barrier `2(1 - gamma)` (since `2 - gamma > 2 - 2 gamma`).
3. **What Theorem 4.4 adds.** For `gamma > 0` the known barriers leave the windows `(2(1 - gamma), 2)` (root) and `(2(1 - gamma), 2 - gamma)` (C1) open. Theorem 4.4 shows that no local convexification in the `(z, beta, beta beta')` lift enters them. Any relaxation that does must lift the products `zeta_j beta_m` (as `zb` does, pairwise), use other extended variables, or use global constraints. As `gamma -> 0` all these values tend to 2, and the constant 2 is optimal in the following limit sense, conditionally on the low-degree conjecture:

   - Fix `delta > 0`. There is `gamma_0 > 0` such that, for each fixed `gamma in (0, gamma_0)`, BAHSWZ's detection bound `2(1 - sqrt gamma)^2` exceeds `2 - delta`. So degree-`o(k)` polynomials fail to detect below `alpha = 2 - delta`.
   - By Arpino's reduction from detection to approximate recovery (as cited by BAHSWZ), and conditionally on the low-degree conjecture, no polynomial-time algorithm achieves approximate recovery there.
   - A root-exact relaxation with a unique optimum would be such an algorithm.

   This uses the proven detection bound rather than the approximate-recovery conjecture. The conclusion also rests on the heuristic model transfer of item 1 (binary signals, `sigma^2 = o(k)`). BAHSWZ's theorem is for fixed `theta = gamma in (0, 1)`, so the case `log k = o(log p)` (`gamma = 0`) lies outside it and is claimed only as this limit.
4. **No SoS lower bounds.** We did not find sum-of-squares lower bounds for certifying optimality in sparse regression. The arXiv API queries of Section 8 returned none; an unsuccessful search does not establish absence. `zb` is a sparse, partial level-2 moment relaxation in `(zeta, beta)`: Shor's degree-2 moments plus the product cones, which are 2×2 principal minors of the level-2 moment matrix (Section 5). Its thresholds are Question 5.4. By Proposition 5.1, moment-based lower bounds against `zb`, if they exist here, cannot use the few-violator pseudo-moments that defeat the `(z, beta, beta beta')` lift.

## 7. Computations

All values are floating point. Perspective bounds are certified dual bounds
(Clarabel). `SDP1`, `sdp_2` and `L_2` values come from Clarabel (tolerance
`1e-9`) for `p <= 100`, and `SDP1` from SCS (`eps = 1e-7`) for
`100 < p <= 400`. `zb` values come from SCS (`eps = 1e-7`, or `1e-6` where
marked), or Clarabel. The "certified" upper bounds on `L_1`/`L_2` values are
objective values of explicit feasible points (Lemma 4.1(ii)/(iii),
Proposition 3.1(b); `cbound.py`), evaluated in floating point. `OPT` is exact
for `k = 3` (enumeration of all triples, `opt_check.py`) wherever stated.

Exactness is decided as follows.

- *Perspective root, `S*` optimal:* the exact PWE criterion `max_{l ∉ S*} |a_l| <= m0` (PT Corollary 2.4).
- *`SDP1` root:* Dong's exact certificate (Theorem 2 of arXiv 1603.04572; `dong_check.py`) at the `OPT` support. It minimizes the convex function `lambda_max(D(t) - X'X/lam - I)` over `t > 0`. It agrees with the solver rule below on all 73 rows of Tables 7.1, 7.2 and 7.4. `SDP1` was also solved on the 71 rows of Table 7.3, where the certificate was not run. The smallest `SDP1` gap there is `1.6e-2`, so the solver rule is safe.
- *Otherwise:* a value `v` is *exact* if `-1e-5 OPT <= OPT - v <= 1e-6 OPT`, that is, within solver accuracy. For `zb` in Table 7.3, values more than `1e-5` above `OPT` count as unclear. Six stored values exceed `OPT` by more than `1e-6` relative, so solver accuracy is about `1e-5` relative:
  - `zb`: `3.3e-5` and `3.0e-6` in Table 7.3 (SCS `1e-6` and `1e-7`), and `1.9e-6` in Table 7.4 (`alpha = 2`, seed 1000);
  - `sdp_2`: `2.0e-6` and `1.3e-6` in Table 7.4 (`alpha = 1.5`, seeds 1006, 1004), and `1.5e-6` in Table 7.2 (`p = 100`, seed 2005).
- A relaxation is *certified inexact* if an upper bound is below `OPT (1 - 1e-7)`.

### 7.1 Model checks

- `test_relax.py` (6 instances, `n = 6`, `p = 8`, `k = 2`, `OPT` by enumeration):
  - every relaxation is `<= OPT`;
  - the order perspective `<= SDP1 <= sdp_2 <= L_2` holds, as does `SDP1 <= ` spartrahedron and `SDP1 <= zb`;
  - with `S1 = S*` every relaxation equals `f(S*)` (relative error `<= 3e-8`).
- `test_zb_valid.py` (40 random instances, `n = 5..12`, `p = 12..21`, `k = 2, 3`; a third pure noise, a third weak signal):
  - no relaxation value exceeds `OPT` (0 violations);
  - exact runs: perspective 0/40, `SDP1` 3/40, `sdp_2` 19/40, `zb` 40/40.
- `verify_construction.py` (`n = 30`, `p = 1000`, `k = 3`, seed 1; `data/verify_construction_p1000.log`) builds the point of Lemma 4.1(ii) along the failure direction of Section 2 and checks:
  - `<X'X, B - beta beta'> = 5e-16`;
  - `[[1, beta'], [beta, B]] ⪰ 0` (smallest eigenvalue `-2e-16`);
  - all 125,751 `sdp_2` pair constraints on `F ∪ Z1` (smallest scaled eigenvalue `-2e-16`; pairs outside are trivially feasible);
  - `L_2` membership for 40 sampled pairs, including all pairs inside `F`, each by an independent small SDP (worst margin `-6e-10`);
  - objective `f(S*) - 0.123`, with inflation `eps_eff = 0.64` at this size. The independent review's own construction, on a finer grid, gives `f(S*) - 0.454`.

  `S*` is the optimum here (enumeration of all 166 million triples, `data/verify_construction_opt.log`). So `sdp_2` and `L_2` are root-inexact on this instance, which is beyond the reach of the SDP solvers. The spartrahedron constraint is violated (smallest eigenvalue `-0.015`).
- `test_cbound.py` (12 instances, `n = 8`, `p = 40`, `k = 2`; root, a forced-in node and a removal node each; `data/test_cbound.log`): on all 36 nodes, the exact `SDP1` and `L_2` values (Clarabel) are below the certified bounds of `cbound.py`, up to the solver accuracy `1e-6`. In the one case that needed this tolerance, the Clarabel `L_2` value exceeds the node's integer optimum itself by `3e-7` relative, and the bound equals that optimum.
- On all 77 stored rows where both exist, `SDP1 <=` its certified bound and `sdp_2 <=` the `L_2` bound (tolerance `1e-6`): no inconsistency. An earlier version of `cbound.py` returned invalid bounds when the helper set had at most `n` columns (`p = 40`). Found by this check, it was fixed by the guard `|Z1| > n`, `q_max < 1`, and those rows were recomputed.

### 7.2 Nested designs: the finite-size advantage and its disappearance

For each seed, one Gaussian `n x 2560` design, one response
(`k = 3`, `S* = {0,1,2}`, `b = 1`, `sigma = 0.5`,
`lam = 1.5 sigma sqrt(2 n log 200)/b` fixed), and the instance with `p`
features uses the first `p` columns (`exp_mech.py`). As `p` grows, `n/p`
shrinks and more null features compete.

Table 7.1 (`n = 20`; 8 seeds; `OPT` by enumeration; at `p = 2560` only the 4
seeds with `OPT` enumerated). "`SDP1` gap closed" is the median of
`(SDP1 - P)/(OPT - P)` over runs with a perspective gap. "`L_2` gap kept" is
the median lower bound `(OPT - L_2 bound)/(OPT - P)` on the fraction of the
perspective root gap that `L_2` does not close.

| `p` | runs | `S*` optimal | median `delta` | median #viol. | persp. exact | median rel. root gap | `SDP1` exact | `SDP1` gap closed | `sdp_2` exact | `zb` exact | `L_1` cert. inexact | `L_2` cert. inexact | median `L_2` gap kept (lower bd.) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 40 | 8 | 6/8 | 1.118 | 5.5 | 1/8 | 2.0e-02 | 3/8 | 0.51 | 5/8 | 8/8 | 2/8 | 0/8 | 0.00 |
| 80 | 8 | 6/8 | 0.531 | 9.5 | 0/8 | 2.6e-02 | 0/8 | 0.25 | 5/8 | 8/8 | 5/8 | 0/8 | 0.00 |
| 160 | 8 | 6/8 | 0.289 | 16 | 0/8 | 5.5e-02 | 0/8 | 0.12 | — | 7/8 | 8/8 | 0/8 | 0.00 |
| 320 | 8 | 4/8 | 0.142 | 33.5 | 0/8 | 1.1e-01 | 0/8 | 0.03 | — | — | 8/8 | 1/8 | 0.00 |
| 640 | 8 | 1/8 | 0.073 | 62.5 | 0/8 | 1.4e-01 | — | — | — | — | 8/8 | 1/8 | 0.00 |
| 1280 | 8 | 0/8 | 0.036 | 120.5 | 0/8 | 1.2e-01 | — | — | — | — | 8/8 | 4/8 | 0.03 |
| 2560 | 4 | 0/4 | 0.019 | 314 | 0/4 | 1.7e-01 | — | — | — | — | 4/4 | 3/4 | 0.13 |

- At `p = 40, 80` (`n/p = 1/2, 1/4`) the pairwise SDP `sdp_2` is root-exact in 5 of 8 runs and `zb` in 8 of 8, against 1 and 0 for the perspective relaxation. `SDP1` closes about half, then a quarter, of the perspective root gap.
- As `p` grows at fixed `n`, `SDP1` closes a shrinking fraction of the gap (0.51, 0.25, 0.12, 0.03). This matches `delta` (1.1, 0.53, 0.29, 0.14; Proposition 3.1).
- From `p = 1280` on, explicit points certify that the `L_2` root (hence `sdp_2`) is below `OPT` in about half or more of the runs: 4 of 8 at `p = 1280`, 3 of 4 at `p = 2560`. At `p = 2560`, `L_2` keeps at least 13% of the perspective gap in the median.
- *Caveat:* with `n = 20`, `S*` stops being optimal as `p` grows (6/8 at `p <= 160`, 0/8 from `p = 1280`). The large-`p` rows lie below the recovery threshold. Table 7.2 repeats the experiment at `n = 40`, where `S*` stays optimal.

### 7.3 `n = 40`: inside the C1 window

Same construction with `n = 40`, `pmax = 3200` (8 seeds). `S*` is optimal
by enumeration for `p <= 1600`. At `p = 3200` the perspective relaxation
satisfies C1 at `S*` in 6 of 8 runs, which certifies `S*` as the unique
optimum; only those 6 runs are kept. This is the C1 window of [PT]:
perspective B&B trees are linear, but the perspective root is not exact.

Table 7.2 (`n = 40`; columns as in Table 7.1).

| `p` | runs | `S*` optimal | median `delta` | median #viol. | persp. exact | median rel. root gap | `SDP1` exact | `SDP1` gap closed | `sdp_2` exact | `zb` exact | `L_1` cert. inexact | `L_2` cert. inexact | median `L_2` gap kept (lower bd.) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 8 | 8/8 | 0.896 | 1 | 2/8 | 2.4e-04 | 8/8 | 1.00 | 8/8 | 8/8 | 0/8 | 0/8 | 0.00 |
| 200 | 8 | 8/8 | 0.441 | 1 | 1/8 | 5.3e-04 | 6/8 | 1.00 | — | 8/8 | 0/8 | 0/8 | 0.00 |
| 400 | 5 | 5/5 | 0.196 | 6 | 0/5 | 1.6e-02 | 0/5 | 0.29 | — | — | 4/5 | 0/5 | 0.00 |
| 800 | 8 | 8/8 | 0.098 | 8 | 0/8 | 6.8e-03 | — | — | — | — | 8/8 | 0/8 | 0.00 |
| 1600 | 8 | 8/8 | 0.049 | 15.5 | 0/8 | 1.2e-02 | — | — | — | — | 8/8 | 2/8 | 0.00 |
| 3200 | 6 | 6/6 | 0.026 | 25.5 | 0/6 | 2.3e-02 | — | — | — | — | 6/6 | 4/6 | 0.01 |

- At `p = 100` (`n/p = 0.4`, `delta ≈ 0.9`), `SDP1`, `sdp_2` and `zb` are root-exact in 8 of 8 runs, against 2 of 8 for the perspective relaxation. (Seed 2006 has perspective gap `1.9e-7` relative but PWE ratio 1.0018, so it is inexact.) At `p = 400` (5 of the 8 seeds; the run was stopped for time), `SDP1` closes a median 29% of the gap.
- At `p = 3200` (`n/p = 0.0125`), in the C1 window, the `L_2` root is certified inexact in 4 of the 6 runs. So at an accessible size, pairwise hulls in the `(z, beta, beta beta')` lift, and with them `sdp_2`, the free-sign 2×2 decompositions and the optimal perspective, do not make the root exact where [PT]'s linear-tree regime holds. This is Theorem 4.4 in action.
- *Where the helpers come from* (`exp_restr_cmp.py`, seeds 2000, 2001, 2003, 2004 at `p = 3200`). Restrict the instance to `S*` and the 60 nulls with the largest `|a_l|`, 63 columns, which contain the perspective's violators.
  - The perspective root gap on the restricted instance is the full gap (1.007, 3.864, 1.479, 0.918).
  - `SDP1` closes 40–72% of it.
  - `sdp_2` and `zb` are exact (`|value - f(S*)| <= 4e-5`).

  On the full instance the `L_2` root is certified below `f(S*)` for all four seeds, and `S*` is certified optimal for 2000, 2003 and 2004. The local hulls in the `(z, beta, beta beta')` lift therefore fail at `p = 3200` only through the thousands of other null features, used as `z = 0` helpers. That is exactly the mechanism of Lemma 4.1.
- The restricted `zb` stays exact with 150 nulls as well (seeds 2000, 2001, 2002, 2005: `|zb_restr - f(S*)| <= 3e-6`). Full `zb` at `p = 3200` (a PSD block of size 6401) was beyond our budget. So whether `zb` is exact on these instances is not known; the restricted values are only consistent with it.

### 7.4 `zb` at larger `p` and in pure noise

*Restricted `zb` at `p = 320`, `n = 20`* (`exp_zbr.py`). Setting all
rows and columns outside `C = S* ∪ (top-N nulls)` to zero is feasible for
`zb`. So `zb` of the restricted instance is an upper bound on the full `zb`
root, and a value below `OPT` certifies (up to solver accuracy) that the full
`zb` root is inexact.

| seed | `S*` optimal | #violators | `OPT - zb_restr`, `N = 40` | `N = 100` |
|---:|---:|---:|---:|---:|
| 2000 | yes | 17 | 0 | 0 |
| 2003 | yes | 19 | 0 | 0 |
| 2005 | yes | 23 | 0 | 0 |
| 2007 | yes | 30 | 0 | 0 |
| 2004 | no | 43 | 0 | 0 |
| 2006 | no | 43 | 0 | 0 |
| 2001 | no | 37 | 0.829 | 1.332 |
| 2002 | no | 63 | 0.567 | 0.743 |

("0" means `|OPT - zb_restr| <= 5e-6`.) `zb` is certified inexact at the
root in 2 of 8 runs, both below the recovery threshold (`S*` not optimal) and
with more violators than `n`. In the other 6 the restricted value equals
`OPT`, which is consistent with, but does not prove, exactness of the full
`zb`. On these instances the perspective root gap has median 11% of `OPT`,
and `SDP1` closes about 3% of it (Table 7.1).

*`zb` in pure noise* (`exp_hardzb.py`). These are the pure-noise
instances of PT Table 6.4: `p = 10k`, `n = round(alpha k log p)`,
`lam = 0.75 sqrt(2 n log p)`, `y` independent of `X`, 4 seeds each, with
`OPT`, the perspective root and the certified perspective conflict clique
taken from PT's stored runs. `zb` was solved by Clarabel for `p <= 50` and
by SCS otherwise (`eps = 1e-7` for the first 16 runs, `1e-6` after). Relative
gaps are `(OPT - value)/OPT`.

Table 7.3.

| `k` | `p` | `alpha` | `n` | runs | median persp. clique | median B&B nodes | persp. median rel. gap | `SDP1` exact | `SDP1` median rel. gap | `zb` exact | `zb` inexact (gap > 1e-4) | `zb` unclear | max `zb` rel. gap |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 30 | 1 | 10 | 4 | 3.5 | 14 | 6.8e-02 | 0 | 4.2e-02 | 4 | 0 | 0 | -9.4e-09 |
| 3 | 30 | 2 | 20 | 4 | 6.0 | 21 | 9.8e-02 | 0 | 6.0e-02 | 4 | 0 | 0 | 7.2e-08 |
| 3 | 30 | 4 | 41 | 4 | 6.0 | 28 | 5.8e-02 | 0 | 2.1e-02 | 4 | 0 | 0 | 7.7e-08 |
| 4 | 40 | 1 | 15 | 4 | 5.0 | 29 | 5.5e-02 | 0 | 4.7e-02 | 3 | 1 | 0 | 8.1e-03 |
| 4 | 40 | 2 | 30 | 4 | 9.0 | 52 | 9.0e-02 | 0 | 6.0e-02 | 3 | 0 | 1 | 6.5e-06 |
| 4 | 40 | 4 | 59 | 4 | 10.0 | 56 | 6.5e-02 | 0 | 2.4e-02 | 4 | 0 | 0 | -8.9e-09 |
| 5 | 50 | 1 | 20 | 4 | 6.0 | 33 | 5.0e-02 | 0 | 4.1e-02 | 3 | 1 | 0 | 5.2e-03 |
| 5 | 50 | 2 | 39 | 4 | 21.0 | 209 | 8.6e-02 | 0 | 6.0e-02 | 2 | 2 | 0 | 1.0e-02 |
| 5 | 50 | 4 | 78 | 4 | 29.0 | 374 | 7.0e-02 | 0 | 2.5e-02 | 4 | 0 | 0 | -3.8e-08 |
| 6 | 60 | 1 | 25 | 4 | 14.0 | 119 | 8.0e-02 | 0 | 6.7e-02 | 0 | 4 | 0 | 9.9e-03 |
| 6 | 60 | 2 | 49 | 4 | 21.0 | 236 | 7.2e-02 | 0 | 5.0e-02 | 1 | 2 | 1 | 6.8e-03 |
| 6 | 60 | 4 | 98 | 4 | 35.5 | 1327 | 1.0e-01 | 0 | 3.1e-02 | 3 | 1 | 0 | 2.7e-04 |
| 7 | 70 | 1 | 30 | 4 | 12.5 | 195 | 7.9e-02 | 0 | 6.8e-02 | 0 | 4 | 0 | 1.1e-02 |
| 7 | 70 | 2 | 59 | 4 | 26.5 | 540 | 8.7e-02 | 0 | 5.7e-02 | 0 | 4 | 0 | 2.5e-03 |
| 7 | 70 | 4 | 119 | 4 | 25.5 | 769 | 7.1e-02 | 0 | 2.0e-02 | 4 | 0 | 0 | 3.2e-08 |
| 8 | 80 | 1 | 35 | 4 | 44.0 | 1200 | 9.8e-02 | 0 | 8.6e-02 | 0 | 4 | 0 | 3.4e-02 |
| 8 | 80 | 2 | 70 | 4 | 74.0 | 5437 | 1.1e-01 | 0 | 7.6e-02 | 0 | 4 | 0 | 1.7e-02 |
| 8 | 80 | 4 | 140 | 3 | 112.0 | 12171 | 9.0e-02 | 0 | 2.8e-02 | 1 | 1 | 1 | 2.1e-03 |

- The perspective relaxation has relative root gaps of 2–14% (medians 5–11% per cell). `SDP1` closes 9–76% of them (median 33%) and is never exact.
- `zb` is exact in 40 of 71 runs, inexact (gap `> 1e-4`) in 28, and unclear in 3. A value more than `1e-5` above `OPT` counts as unclear. In one such run (`k = 6`, `alpha = 2`, seed 3002) SCS puts `zb` `3.3e-5` above `OPT`, while Clarabel (`optimal_inaccurate`) puts it `3.8e-5` below (`zb_recheck.py`; the reviewer found the same). It is exact on every instance with `k = 3` and on most with `k <= 5`. It becomes inexact as `k` grows: at `k = 8` and `alpha <= 2` in all runs, with largest gaps of 3.4% and 1.7%. Where it is inexact, its gap is 2.9–403 times smaller than the perspective relaxation's (median 14).
- It is exact more often at larger `alpha` (larger `n`), as Proposition 5.3 suggests.
- Where `zb` is exact, the root proves optimality with no branching. That includes instances where every convex-piece certificate for the perspective relaxation needs at least 67 leaves (the largest certified clique among those runs), and where perspective B&B used up to 5537 nodes.
- So at these sizes `zb` greatly weakens the pure-noise obstruction of PT 4.3 but does not remove it. Whether its gaps vanish or persist asymptotically is part of Question 5.4.

### 7.5 The parent note's instance family: root and C1 (`p = 100`)

The generator is `core.instance` of [PT] with `k = 3`, `p = 100`, `tau0 = 1.5`
(`lam = 0.75 sqrt(2 n log p)`), `n = round(alpha k log p)`, seeds 1000–1007
(4 seeds at `alpha = 1`), and `OPT` by enumeration (`exp_cmp.py`,
`opt_check.py`). For C1 the perspective relaxation's failing single-fixing
nodes were found exactly (dual pool plus column generation), and `SDP1` and
`sdp_2` were solved at the weakest failing node of each run. A relaxation
fails C1 if that node's value is below `OPT`. It is "undecided" if that node
passes but other failing nodes were not solved.

Table 7.4.

| `p` | `alpha` | `n` | runs | `S*` optimal | median #viol. | persp. root exact | `SDP1` exact | `sdp_2` exact | `zb` exact | `L_2` root cert. inexact | persp. C1 | `SDP1` C1 (solved) | `sdp_2` C1 (solved) | C1 fails for `L_2` (cert.) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 1.00 | 14 | 4 | 2/4 | 29.5 | 0/4 | 0/4 | 0/4 | 4/4 | 0/4 | 1/4 | 1/4 (0 undecided) | 1/4 (1 undecided) | 0/3 |
| 100 | 1.50 | 21 | 8 | 6/8 | 10 | 0/8 | 1/8 | 3/8 | 7/8 | 0/8 | 5/8 | 5/8 (0 undecided) | 5/8 (0 undecided) | 0/3 |
| 100 | 2.00 | 28 | 8 | 8/8 | 2.5 | 0/8 | 3/8 | 8/8 | 8/8 | 0/8 | 8/8 | 8/8 (0 undecided) | 8/8 (0 undecided) | 0/0 |

- *Root.* At `p = 100` (`n/p = 0.14`–`0.28`), the root-exactness counts rise with the relaxation: perspective 0 of 20, `SDP1` 4, `sdp_2` 11, `zb` 19. This is the finite-size regime of Section 7.2.
- *C1.*
  - Among the `S*`-optimal runs, the perspective relaxation fails C1 in two: `alpha = 1.5`, seed 1003, with 27 failing nodes; and `alpha = 1`, seed 1001, with 5.
  - At seed 1003, `SDP1` and `sdp_2` also fail C1: their weakest-node values are 11.5% and 6.3% below `OPT`, and `zb`'s root is `4.8e-4` below `OPT`.
  - At seed 1001, `sdp_2` passes the weakest failing node (0.35% above `OPT`), but the other four nodes were not solved.
  - We saw no case where a stronger relaxation provably restores C1 when the perspective relaxation lacks it.
  - Our upper bounds for `L_2` certify no C1 failure at this `p`, because `theta_F` is too large at `n/p ≈ 0.2`.

## 8. Literature comparison

How sources were checked: full text of the relevant sections where marked
"read"; otherwise abstract only or from memory, as marked. The web-search
tool's budget was exhausted in this session, so searches used the arXiv API
directly (queries listed in the appendix). An unsuccessful search does not
establish novelty.

- **Atamtürk–Gómez, rank-one convexification** (arXiv 1901.10334v2; Sections 1–2 read).
  - Theorem 1: `conv{(z, beta, t) : t >= (a'beta)^2, beta_i (1 - z_i) = 0} = {(a'beta)^2 <= t min(1, z(T))}`.
  - Formulation (15): the optimal decomposition into rank-one pieces.
  - Theorem 3 and formulations (19)–(21): `sdp_r`, `sdp_2`.
  - Their experiments (UCI data, `p <= 100`, low diagonal dominance) show `sdp_2` far stronger than `sdp_1`.

  Relation: Lemma 1.2(d) puts `sdp_r` below `L_r`, so Theorem 4.4 applies. Their gains are real at their sizes; Theorem 4.4 says they vanish in random designs when `n = o(p/(r log p))`.
- **Han–Gómez–Atamtürk, 2×2 convexifications** (arXiv 2004.07448; Section 2 and Section 4's `OptPairs` read).
  - Theorem 1: Shor's SDP equals the optimal perspective relaxation, for nonnegative continuous variables.
  - `OptPairs` dominates Shor, the optimal perspective and the optimal rank-one relaxations.

  Relation: their problem has nonnegative continuous variables. `OptPairs` is not valid for our free-sign model and is not dominated by `L_2`. Its free-sign analogue, 2×2 decompositions with the free-sign hull of Wei et al., is below `L_2` (Lemma 1.2(d)). Remark 4.5 shows that the Shor lift in `(zeta, beta)` with McCormick inequalities does not help either.
- **Wei–Atamtürk–Gómez–Küçükyavuz, convex hull with indicators** (arXiv 2201.00387; Theorem 1 and Proposition 2 read). The exact hull for general `Q ≻ 0` is one PSD constraint plus a polytope `P = conv{(e_S, Q_S^{-1})}` in extended variables. Relaxations of `P` are not local in our sense, and Theorem 4.4 does not cover them. The 2×2 hull (Proposition 2, free signs) is covered. The earlier Wei–Gómez–Küçükyavuz 2×2 papers (IPCO 2020 and Math. Program.) were not read.
- **Dong–Chen–Linderoth** (arXiv 1510.06083; abstract read), the optimal perspective relaxation and its equivalence with MC+ regularization. **Zheng, Sun and Li**, "Improving the performance of MIQP solvers for quadratic programs with cardinality and minimum threshold constraints: a semidefinite program approach" (INFORMS J. Comput. 26, 2014; identified by the review, not read), computes the best diagonal perturbation by SDP; the earlier source for SDP-computed diagonal perturbations is Frangioni–Gentile (2007; not read). The brief's "Zheng–Fan–Sun" refers to this line of work.
- **Dong, exact recovery via conic relaxations** (arXiv 1603.04572; read).
  - Proposition 1: `SDP1 >= ` perspective.
  - Theorem 2: exactness certificate of `SDP1`; our Proposition 3.1(a) is its sufficiency half.
  - Section 3: in Gaussian experiments `SDP1` needs "much fewer observations".
  - His Theorem 3 is PWE's Gaussian theorem, which is false as stated (PT Remark 3.5).

  Relation: Proposition 3.1(b, c) and Theorem 4.4 show that the gain is a finite-size effect governed by `delta ≈ n/p`, and that the asymptotic constant is unchanged. We know of no prior random-design threshold for `SDP1`, `sdp_r` or 2×2 hulls.
- **Cifuentes–Li, spartrahedron** (arXiv 2603.18215; definitions and Section 5 read).
  - The SDP adds `k Diag(B) ⪰ B`.
  - Exactness regions for sparse ridge regression need `sigma_min(A) > 0`, that is, the overdetermined case `n >= p`.
  - The approximation bound is `O(k)`.

  Relation: not covered by Theorem 4.4 (Remark 4.5), and outside our regime `n < p`.
- **Bandeira–El Alaoui–Hopkins–Schramm–Wein–Zadik** (arXiv 2205.09727; Section 3.2 read) and **Gamarnik–Zadik** (arXiv 1711.04952; abstract): see Section 6. **Reeves–Xu–Zadik** (all-or-nothing) is cited through BAHSWZ.
- **Pilanci–Wainwright–El Ghaoui, Xie–Deng**: through [PT].

Novelty assessment (cautious). The deterministic completion Lemma 4.1 and
Theorem 4.4 appear new. They are the first random-design statements for these
relaxations that we know of, and they are negative: the thresholds do not
move. The mechanism (null-space pseudo-moments defeat local hulls when
`p ≫ n`) is elementary once stated; we have not seen it stated.
Proposition 3.1(a) is Dong's. The product cones themselves are not new in
kind: they are 2×2 principal minors of the level-2 moment matrix, and exact
2×2 hulls of the full switching-variable lift (for example Anstreicher–Burer
2021, from memory) imply them. What we have not seen is their use for sparse
regression and the analysis of Propositions 5.1 and 5.3 (direct
computations); this search was limited.

## 9. Open problems

1. **Question 5.4.** The thresholds of `zb` (Shor in `(zeta, beta)` with McCormick and product cones), and more generally of `r`-wise hulls in the full lift `(zeta, beta, zeta zeta', zeta beta', beta beta')` together with the PSD moment matrix `Y ⪰ 0` of `(1, zeta, beta)`, and of level-2 moment relaxations. Theorem 4.4 does not cover them. (With PSD only on `(1, beta, B)`, full-lift hulls are covered; see Remark 4.5.) A proof either way would settle whether such SDPs can enter the window `(2(1 - gamma), 2)`.
2. **Relaxations of the Wei–Atamtürk–Gómez–Küçükyavuz polytope** `conv{(e_S, Q_S^{-1})}`. They use extended variables outside the `(z, beta, beta beta')` lift, so Theorem 4.4 says nothing about them.
3. **The spartrahedron** `k Diag(B) ⪰ B` together with `L_r` (Remark 4.5).
4. **The regime `n ≍ p`.** There `delta` and `eps_p` are constants, and `SDP1` and `sdp_2` do move the thresholds. A sharp formula, for example the root threshold of `SDP1` as a function of `n/p` via the certificate of Proposition 3.1(a), is open. This is the regime of most benchmark data.
5. **Finite-size corrections.** A computable prediction of the `L_2` root gap from Lemma 4.1(ii) along the lines of PT Heuristic 3.8.
6. **General `r` without `log p`.** Lemma 4.1(ii) removes the `log p` for pairs. We do not know whether `eps_p = O(sqrt(r n/p))` holds for `r >= 3`.

## Revision after review (2026-09-29)

The review found Theorem 4.4, Lemmas 4.1–4.2, Corollary 4.3,
Proposition 3.1, Propositions 5.1 and 5.3 and Corollary 5.2 correct, and the
computations reproducible. It found errors of scope, framing and attribution.
Each change below was re-derived here before it was made.

1. **`OptPairs` (F1).** Han–Gómez–Atamtürk's `OptPairs` is for nonnegative continuous variables. With `b >= 0` the lifted hull forces `B >= 0` entrywise, so it is smaller than the free-sign `H_T`. It is not valid for the model and not dominated by `L_2`. It is replaced everywhere (Summary, Section 1.2, Corollary 4.6, Sections 7.3, 8) by its free-sign analogue: 2×2 decompositions with the free-sign hull of Wei–Atamtürk–Gómez–Küçükyavuz (Proposition 2). That analogue is below `L_2` by Lemma 1.2(d), where `Q_T ⪰ 0` is now stated. The statement that Han–Gómez–Atamtürk prove Shor = OptPersp in the nonnegative setting is kept.
2. **Framing (F2, F7).**
   - Re-derived: at every generating point `(zeta_j b_m)^2 = zeta_j zeta_m b_m^2`, so the product cone is implied by the exact 2×2 hull of `(zeta, beta, zeta zeta', zeta beta', beta beta')`. After reduction by `zeta^2 = zeta`, `beta_m (1 - zeta_m) = 0`, it is the 2×2 principal minor on `{zeta_j zeta_m, beta_m}` of the level-2 moment matrix.
   - So the obstruction is escaped by lifting the products `zeta_j beta_m`, not by non-locality (qualified in item 11: the products must sit in the PSD moment matrix of `(1, zeta, beta)`). "Beyond local lifts" became "beyond the `(z, beta, beta beta')` lift" (Summary, Sections 1.2, 5); Section 4's title now says "local hulls in the `(z, beta, beta beta')` lift"; Section 6.3 now says such relaxations "must lift the products `zeta_j beta_m` (or use other extended variables) or use global constraints".
   - Remark 4.5 and Section 9.1 now state that `r`-wise hulls in the full `(zeta, beta)` lift are not covered by Theorem 4.4, and that Proposition 5.1 shows that already `r = 2` escapes (qualified in item 11: with `Y ⪰ 0`).
   - Section 5 ("Where `zb` sits"), Section 6.4 ("sparse, partial level-2 moment relaxation") and the novelty assessment were updated accordingly. Anstreicher–Burer (2021) is cited from memory.
3. **Conventions (F3).**
   - After Definition 1.1: `L_r(S0, S1)` imposes root hulls and fixes only `z`, so fixed-to-zero features keep a free `B_mm` and can be helpers. Also, `H_T` has no cardinality restriction; for `r > k`, the cardinality-constrained hull is stronger and Lemma 1.2(b) fails for it (re-derived: with `k = 1` it forces `B_jm = 0` on pairs).
   - Theorem 4.4 now requires `R <= L_r` only at the root and the forced-in nodes `(∅, {j})`. Its proof uses only these, and no column is fixed to zero there, so solvers that delete fixed-to-zero columns are covered.
   - Corollary 4.6 states the node convention and says that column-deleting implementations are not covered.
4. **Proposition 5.3 and the reading of Corollary 5.2 (F4).** `≈ 4 sqrt(s/n)` holds for a fixed support independent of `X`. Uniformly over size-`s` supports, the fraction is about `4 (sqrt s + sqrt(2 s log(ep/s)))/sqrt n` (re-derived from (G3) with a union bound). That is small only if `s log(ep/s) = o(n)`, and it is `Theta(1)` at `s ≈ k`, `n ≈ 2k log p`. The Summary, the text after Proposition 5.3 and Question 5.4 now say so. "`zb` can be inexact only through points whose support is large" is relabeled as a heuristic reading.
5. **Minor slips (F5).**
   - Theorem 4.4(b): the bound `||x_l||^2 <= nu` for the violator now uses (G2) with a union bound over all `p` features, since Lemma 4.2's (E2) covers only the helper half.
   - `c := eps/12` (the `min` was redundant).
   - Remark 4.5, *Constants*: re-derived. Pricing at `lam (1 + eps)` gives the root threshold `2 log p/(1 + eps)^2`, a factor, equivalently a shift of about `4 eps log p`. The wrong "additive `2 log(1 + eps_p)`" is removed.
   - Section 2: "descent iff" became "descent if", with the converse labeled first-order and heuristic.
   - Median violator counts are now exact (5.5, 9.5, ...).
   - Remark 4.5's regime statement now reads `r n log p = o(p)`.
6. **Barrier attribution (F6).** The Summary no longer says that BAHSWZ place the recovery threshold. It now says that the literature they summarize suggests hardness of approximate recovery below `R = 2`, and that their low-degree bound proves detection hardness below `alpha = 2(1 - sqrt gamma)^2`, with no sharp recovery bound suggested for larger `gamma`. Section 6.1 notes that root exactness is exact recovery. Section 6.3 bases the `gamma -> 0` statement on the proven detection bound, the low-degree conjecture and Arpino's reduction.
7. **Reference (F8).** "Zheng–Fan–Sun" is replaced by Zheng, Sun and Li (INFORMS J. Comput. 2014), with Frangioni–Gentile (2007) as the earlier source. Neither was read.
8. **Tolerances (F9).**
   - Perspective root exactness is now decided by the exact PWE criterion when `S*` is optimal. At `n = 40`, `p = 100` the count is 2 of 8, not 3: seed 2006 has gap `1.9e-7` relative but ratio 1.0018. Table 7.2, Section 7.3 and the Summary were corrected.
   - `SDP1` exactness is now checked by Dong's exact certificate (`dong_check.py`). It agrees with the solver rule on all 73 rows, so no `SDP1` count changes.
   - Section 7 states that `zb` and `sdp_2` "exact" means within solver accuracy (about `1e-5`), since two stored `zb` values and one `sdp_2` value exceed `OPT` by `3e-6`–`3.3e-5` relative.
   - The review's finer-grid `p = 1000` value (`f(S*) - 0.454`) is recorded next to ours (`- 0.123`).

Second round (the reviewer's check of this revision found F1–F8 addressed
and the weakened hypothesis of Theorem 4.4 sufficient):

9. **Table 7.3, one `zb` run (F9 remainder).** `k = 6`, `alpha = 2`, seed 3002 had been counted as `zb`-exact. Re-solving with Clarabel (`zb_recheck.py`, `data/zb_recheck.log`) gives `optimal_inaccurate`, `3.8e-5` below `OPT`, while the stored SCS value is `3.3e-5` above. The two solvers disagree in sign, so the run is now unclear. The `zb` rule for Table 7.3 is now: exact if `-1e-5 <= (OPT - v)/OPT <= 1e-6`, inexact if `> 1e-4`, unclear otherwise; the table has an explicit "unclear" column. The row reads 1 exact, 2 inexact, 1 unclear, and the totals are 40 exact, 28 inexact, 3 unclear. The other quoted statistics (the 67-leaf clique, 5537 nodes, gap ratio 2.9–403, median 14) are unchanged.
10. **Section 6.3 and the Summary (R1).** BAHSWZ's theorem holds for fixed `theta in (0, 1)`, so "when `log k = o(log p)`" was outside it. The optimality of the constant 2 is now stated as the `gamma -> 0` limit: for every `delta > 0` some `gamma_0 > 0` makes low-degree detection fail below `2 - delta` for each fixed `gamma < gamma_0`. With Arpino's reduction and the low-degree conjecture, this rules out polynomial-time approximate recovery, hence root exactness. The model caveats are kept.

Third round (fresh recheck, `../../../reviews/stronger-relaxations-recheck.md`, which
found the six revised items correct):

11. **Full-lift pairwise hulls (R1).** Re-derived: completing the Lemma 4.1 point with the mixture's `Z`, `U` on `F` and zero cross moments on the helpers puts it in every exact `r`-wise hull of the full lift. It satisfies the product cones and McCormick, and it violates only `Y ⪰ 0`. The Summary, Remark 4.5 and Section 5 now say that the obstruction is escaped by lifting the products `zeta_j beta_m` *into the PSD moment matrix of `(1, zeta, beta)`*. Full-lift hulls with PSD only on `(1, beta, B)` are still covered by the construction. "Already `r = 2` escapes" now reads "`r = 2` with `Y ⪰ 0`". Section 6.3's necessary condition is unchanged.
12. **Summary wording (R2, R3).**
    - The "Mechanism" bound is now stated for the root-lifted `L_r` at nodes containing `z`, not for a general `R`.
    - The node-convention paragraph now notes that at forced-in nodes the node's own hull equals `L_r(∅, {j})` when the cardinality constraint is dropped or `r <= k` (re-derived via Lemma 1.2(b)).
    - The Summary's sentence on Corollary 4.6 carries the node caveat.
13. **BAHSWZ (R4).** "Thresholding works there" is attributed to BAHSWZ's own theorem. The `gamma -> 0` statements (Summary, Section 6.3) now also cite the heuristic model transfer of Section 6.1. The limit framing is kept.
14. **Tolerances (R5).** All six stored values more than `1e-6` above `OPT` are listed, re-counted from the data files. Dong's certificate is stated to cover the 73 rows of Tables 7.1, 7.2 and 7.4, and the smallest `SDP1` gap among Table 7.3's 71 rows is `1.6e-2`.
15. **Proposition 5.3 fraction (R6).** A matching lower bound is added from a data-dependent support: a column and its `s - 1` most correlated columns give an arrow matrix with `Lambda_± ≈ n ± ||c||`. It was checked numerically at `n = 2000`, `p = 10^4`, where the arrow formula matches the observed fraction to `0.01`.
16. **Theorem 4.4(c) (N1).** Added the clause that `R >= g` at every node and `g`'s bounds increase with fixings, so off-path nodes are pruned; the best-bound variant uses validity of `R`.

Checks rerun for this revision (threads pinned to 1; at most 3 processes):
`dong_check.py` on all solved rows (commands in the appendix),
`zb_recheck.py` (one Clarabel solve), `summ.py` for all four tables, and,
in the third round, a recount of the stored values above `OPT` and a
one-draw check of the Proposition 5.3 fraction (inline NumPy; `n = 2000`,
`p = 10^4`). No theorem statement changed except the
weaker hypothesis of Theorem 4.4.

## Appendix: code, commands, and what each check establishes

All commands ran from `stronger-relaxations/code/` with Python 3.13,
NumPy 2.5, SciPy 1.18, cvxpy 1.9.3, Clarabel 0.11 and SCS. Every script
pins BLAS/OpenMP threads to 1 before importing NumPy, and at most six worker
processes ran at once. These are targeted local checks; no project-wide checks
were run and CI was not inspected. *CPU note:* before the thread pinning was
added to all helper scripts, three short auxiliary runs used multithreaded
BLAS and exceeded the 6-core budget: a solver-profiling script (about 6 min),
a 10-minute exploratory probe (killed when noticed; up to about 20 cores), and
the first few runs of `test_relax.py` and `verify_construction.py` (under a
minute each). The logs in `data/` were regenerated single-threaded.

Code:

- `relax.py`: cvxpy models of the perspective relaxation (via `../../code/core.py`), `SDP1` (optimal perspective; `spart=True` adds `k Diag(B) ⪰ B`), `sdp2` (Atamtürk–Gómez `sdp_2`), `L2` (exact lifted pairwise hull, disjunctive form), and `zb` (Section 5).
- `cbound.py`: the certified upper bounds of Lemma 4.1(ii)/(iii) and Proposition 3.1(b) on `L_2` and `SDP1` node values. It minimizes the inflated perspective over supports `S ∪ S1 ∪ (top-h violators)`. The helper set is `[p] \ F`, with a guard requiring `|Z1| > n` and `q_max < 1`. Any `z` gives a valid bound; local search (SLSQP) picks a good one.
- `verify_construction.py`: builds the explicit point of Lemma 4.1(ii) at the root and checks every constraint numerically.
- `exp_mech.py`, `exp_zbr.py`, `exp_restr_cmp.py`, `exp_cmp.py`, `exp_hardzb.py`: the experiments of Section 7.
- `opt_check.py`: exact `OPT` for `k = 3` by vectorized enumeration of all triples (3×3 adjugate formula), and the perspective C1 decider otherwise.
- `rebound.py`: recomputes the stored bounds with the current `cbound.py` and checks `SDP1 <= L1 bound` and `sdp2 <= L2 bound` wherever both exist.
- `summ.py`: tables. Perspective exactness uses the PWE ratio when `S*` is optimal.
- `dong_check.py`: exact `SDP1` root-exactness decision by Dong's Theorem 2 at the `OPT` support.
- `zb_recheck.py`: re-solves `zb` with Clarabel on the disputed pure-noise run of Table 7.3.
- `test_relax.py`, `test_cbound.py`, `test_zb_valid.py`: validity checks.

Commands behind each result (from `code/`; outputs in `data/`):

- Section 7.1:
  - `python3 test_relax.py > ../data/test_relax.log`
  - `python3 test_zb_valid.py > ../data/test_zb_valid.log`
  - `python3 test_cbound.py > ../data/test_cbound.log`
  - `python3 verify_construction.py 30 1000 3 1 > ../data/verify_construction_p1000.log`; the instance's `OPT` came from `opt_check.opt3` (inline; `../data/verify_construction_opt.log`).
- Table 7.1 (`n = 20`):
  - `python3 exp_mech.py ../data/mech_n20_k3.jsonl 20 3 2560 40,80,160,320,640,1280,2560 8 5 80 320 80 160`
  - then `python3 rebound.py ../data/mech_n20_k3.jsonl 80` (recomputes the `p <= 80` bounds after the `cbound.py` guard fix)
  - `OPT`: `PMAX=1280 APPEND=1 python3 opt_check.py mech ../data/mech_n20_k3.jsonl ../data/opt_mech_n20_k3.jsonl 1`. The 4 enumerated `p = 2560` rows come from an earlier run of the same command without `PMAX`, stopped for time.
- Table 7.2 (`n = 40`):
  - `python3 exp_mech.py ../data/mech_n40_k3.jsonl 40 3 3200 100 8 1 100 400 100 200`
  - `python3 exp_mech.py ../data/mech_n40_k3.jsonl 40 3 3200 200,400,800,1600,3200 8 1 100 400 100 200`, stopped after 5 of 8 rows at `p = 400`. The `p = 200` rows came from the same command with the list `200`, written to a separate file and appended.
  - `PMAX=3200 APPEND=1 python3 opt_check.py mech ../data/mech_n40_k3.jsonl ../data/opt_mech_n40_k3.jsonl 2`, which runs the C1 decider at `p = 3200`. A first run regenerated the instances with the wrong design size (`pmax = 2560`); it was discarded and the file recomputed.
- Section 7.3, restricted comparisons:
  - `python3 exp_restr_cmp.py ../data/restr_cmp_n40.jsonl 60 2000,2001,2003,2004`
  - `python3 exp_zbr.py ../data/zbr_n40_k3.jsonl 40 3 3200 3200 60 2000,2001,2002,2003,2004,2005,2006,2007 1`, and the same with `150 2000,2001,2002,2005`
- Section 7.4:
  - `python3 exp_zbr.py ../data/zbr_n20_k3.jsonl 20 3 2560 320 40,100 2000,2001,2002,2003,2004,2005,2006,2007 1`, with `OPT` from `opt_mech_n20_k3.jsonl`
  - Table 7.3: `python3 exp_hardzb.py ../data/hardzb.jsonl 1`. The first 16 rows used SCS `eps = 1e-7` for `zb`. The run was restarted (skipping finished rows) with Clarabel for `p <= 50` and SCS `eps = 1e-6` otherwise, because one SCS solve hit its 200,000-iteration cap.
- Table 7.4:
  - `python3 exp_cmp.py ../data/cmp_p100_k3.jsonl 100 3 1.0,1.5,2.0,3.0 8 3 100 400 100 100 30 1`, stopped after the 4 rows at `alpha = 1` for time;
  - then `python3 exp_cmp.py ../data/cmp_p100_k3.jsonl 100 3 1.5,2.0 8 2 100 400 100 100 30 1`;
  - `APPEND=1 python3 opt_check.py cmp ../data/cmp_p100_k3.jsonl ../data/opt_cmp_p100_k3.jsonl 1`.
- Revision checks: `python3 dong_check.py ../data/dong_n20.jsonl mech ../data/mech_n20_k3.jsonl ../data/opt_mech_n20_k3.jsonl`; the same for `n40` (`dong_n40.jsonl`); `python3 dong_check.py ../data/dong_cmp.jsonl cmp ../data/cmp_p100_k3.jsonl ../data/opt_cmp_p100_k3.jsonl` (3 processes). Agreement with the solver rule is 32/32, 21/21 and 20/20. Second round: `python3 zb_recheck.py > ../data/zb_recheck.log`, then `python3 summ.py hardzb ../data/hardzb.jsonl > ../data/table_hardzb.md` (the table plus a totals line).
- Tables: `python3 summ.py mech ../data/mech_n20_k3.jsonl ../data/opt_mech_n20_k3.jsonl` (likewise `n40`), `python3 summ.py hardzb ../data/hardzb.jsonl`, and `python3 summ.py cmp ../data/opt_cmp_p100_k3.jsonl ../data/cmp_p100_k3.jsonl`; outputs in `data/table_*.md`.

Literature access: arXiv full texts of 1901.10334, 2004.07448, 2201.00387,
1603.04572, 2603.18215 and 2205.09727 (relevant sections as marked in
Section 8); arXiv API abstract queries (2026-09-29):

- `ti:"2x2" AND abs:indicator`
- `au:Kucukyavuz AND abs:indicator AND abs:quadratic`
- `ti:"regularization vs. relaxation"`
- `ti:"Franz-Parisi"`
- `abs:"sparse linear regression" AND abs:"low-degree"`
- `ti:"sparse regression" AND abs:"sum-of-squares"`
- `abs:"perspective relaxation" AND abs:recovery`
- `abs:"rank-one" AND abs:convexification AND abs:"sparse regression"`
- `abs:semidefinite AND abs:"best subset" AND abs:exact`
- `abs:"sparse ridge regression" AND abs:semidefinite`
- `abs:"rank-one convexification"`
- `abs:"perspective" AND abs:"sparse regression" AND abs:"random"`
- `abs:"Boolean relaxation" AND abs:"semidefinite" AND abs:sparse`

None of them returned a random-design threshold for these relaxations or a
sum-of-squares lower bound for sparse regression.
