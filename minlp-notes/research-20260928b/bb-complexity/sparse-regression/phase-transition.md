# Phase transitions of perspective branch-and-bound in random sparse regression

Workstream `sparse-regression/` of [`../PROGRAM.md`](../PROGRAM.md). Date:
2026-09-28, revised 2026-09-29. Status: proofs and computations by the
workstream owner, independently reviewed in
[`../../reviews/sparse-easy-review.md`](../../reviews/sparse-easy-review.md)
(Sections 1–3, 6) and
[`../../reviews/sparse-hard-review.md`](../../reviews/sparse-hard-review.md)
(Sections 1, 4, 5), and revised in response (see "Revision after review"). Code is in [`code/`](code/), result files
are in [`data/`](data/). All computations use floating point; node bounds are
certified dual bounds, not exact arithmetic.

## Summary

We study branch-and-bound (B&B) with the perspective (Boolean) relaxation for
L0-constrained ridge regression with a Gaussian design. The ridge parameter
`lam` matters: the natural threshold quantity is

```
tau_lam = lam * b_lam / omega_lam,     b_lam = b n/(n+lam),
omega_lam^2 = n sigma^2 + k b^2 lam^2 n/(n+lam)^2,
```

the smallest correlation of a true feature with the ridge residual on the true
support `S*`, in units of the typical correlation of a null feature
(Section 3). Throughout, "w.h.p." means with probability tending to 1.

**Proved (easy side, Section 3).** Assume `log^6 p <= n <= p`,
`k <= C0 n/log p`, `sqrt(n) <= lam <= n/log^2 p`, and fixed
`b, sigma, C0, eps > 0`. (These require `p >= e^17 ≈ 2.4 × 10^7`; every
computation in Section 6 lies outside them.)

- *Root exactness (Theorem 3.1).* If `tau_lam^2 >= (2+eps) log p`, the root
  relaxation is exact w.h.p. and B&B needs one node. If
  `tau_lam^2 <= (2-eps) log p`, the root relaxation value is w.h.p. strictly
  below `f(S*)`. Because `tau_lam^2 < (1+o(1)) n/k` for every `lam`,
  root exactness is possible iff `n >= (2+o(1)) k log p`. This gives the
  sharp constant 2 in the sample-size scaling `n ≍ k log p` at which the
  Gaussian theorem of Pilanci–Wainwright–El Ghaoui (PWE) aims. PWE's theorem
  itself, with `rho = sqrt n` and per-entry noise, is false as stated
  (Remark 3.5; confirmed by an independent verification report).
- *Single-fixing probing, C1 (Theorem 3.2).* If
  `tau_lam^2 >= (2+eps) log(p lam/n)`, then w.h.p. `S*` is the unique optimal
  support and every single wrong fixing is prunable with a margin (strict C1).
  Hence every variable-branching B&B tree, for any branching rule, has at most
  `2p+1` nodes (if the incumbent `OPT` is available when off-path nodes are
  examined, or with best-bound search). Conversely, if
  `tau_lam^2 <= (2-eps) log(p lam/n)` and `k >= 5000/eps^2`, then w.h.p. all
  but at most `n/log^2 p` forced-in nodes at `S*` have bound below `f(S*)`, so
  C1 fails whenever `S*` is optimal.
- *Thresholds in `n` (Corollaries 3.3, 3.4).* Optimizing over `lam`: C1 is
  achievable iff `n >= (2+o(1)) k log(p/sqrt n)`, and root exactness iff
  `n >= (2+o(1)) k log p`. For `k = p^gamma` and `n = alpha k log p`, the
  thresholds are `alpha = 2 - gamma` (C1) and `alpha = 2` (root). In the
  window `2 - gamma < alpha < 2`, every variable-branching tree has linear
  size (with the incumbent `OPT` available when off-path nodes are examined,
  or with best-bound search) although the root relaxation is not exact.
- *Fixed ridge `lam = sqrt n` with fixed per-entry SNR (the scout's model).*
  Then `tau_lam <= b/sigma` stays bounded, so in the asymptotic regime of
  the theorems C1 fails at `S*` once `p/sqrt(n) >= exp(b^2/((2-eps) sigma^2))`,
  for every `n`: there is no `k log p` threshold for C1 in that limit. This
  is invisible at practical sizes. The proofs need `n >= log^6 p`, and the
  failure mechanism needs about `sqrt(n)` polylog nearly orthogonal
  violators. In runs with `k = 5`, `alpha = 3` (`n ≈ 15 log p`), C1 held in
  every run up to `p = 800` and in 7 of 8 at `p = 3200`. In the failing run
  the many violators already recover about 60% of the budget price for
  every forced-in feature, and four nulls then fail: the finite-size form of
  the many-violator balance (Section 6.3).

**Proved (hard side, Section 4), asymptotic only.** In the pure-noise model
(`beta* = 0`), and in the planted model with bounded total SNR
`||beta*||^2/sigma^2 < e^{-x}(1+2x) - 1`, where `x = lim 2 log C(p,k)/n`,
w.h.p. the midpoint-conflict graph of the perspective relaxation has a clique
of size `C(p,k)^{c'}` for some `c' > 0` (so larger than `exp(ck)` for every
`c`), provided `x < x0 = 1.2564...`, `k -> inf`, `k/n -> 0` and
`lam = o(n)`. The `c'` the proof delivers is small: at most
`3 - 2 sqrt 2 ≈ 0.17`, approached only as `x -> 0` (0.16 at `x = 10^-3`,
0.106 at `x = 0.05`), about 0.02 at `x = 1/2`, and tending to 0 as
`x -> x0`. For
`k = p^gamma`, `n = alpha k log p`, the condition is `alpha > 1.59 (1-gamma)`.
Every convex-piece `eps`-certificate (variable, split or SOS branching, any
rule) then has at least `C(p,k)^{c'}` leaves; with incumbent-based bound
tightening, at least `C(p,k)^{c'}/(2p+1)` nodes. The planted region lies
strictly below the information-theoretic recovery threshold. The explicit finite-`p` conditions in the proof
are vacuous at every practical size (Section 4.4); the computations in
Section 6 show large certified cliques and fast-growing trees in pure noise at
small sizes, but not through this proof.

**Structural facts (Section 1).** Exact midpoint formula: for supports `S, T`,
`g((1_S+1_T)/2)` is a ridge fit on `S ∪ T` with penalty `lam` on `S ∩ T` and
`2 lam` on `S Δ T` (Lemma 1.5). If only the *removal half* of C1 holds, a
variable-branching certificate with `2k+1` nodes exists (Lemma 1.3), so no
conflict-type lower bound can exceed `k+1` leaves there.

**Conjectured and open (Section 5).** Below the information-theoretic
threshold at fixed SNR, conflict cliques should be `exp(Omega(k))`
(Conjecture 5.2); a proof needs a second-moment count of pairwise-far
near-optimal supports, which we do not have. Whether a rule-dependent regime
exists between that threshold and `2k log(p/sqrt n)` is open (Question 5.1);
the computations at `p <= 200` do not show one.

**Computations (Section 6).**

- With the scaled ridge (`k = 8`, `p = 100–1600`, SNR 2), C1 held in every
  run from `alpha ≈ 1.5` (`p = 100, 200`) and 1.75 (`p = 400`, `1600`) on,
  while the root relaxation was certified
  exact in at most 4 of 8 runs even at `alpha = 4`: linear trees below root
  exactness, as predicted. The same holds in the scout's data (124 of 124
  C1 runs had an inexact root). The empirical C1 threshold rises with `p`;
  its constant is not yet the asymptotic one.
- With `lam = sqrt n`, `k = 5`, `alpha = 3`, C1 held in all runs up to
  `p = 800` and in 7 of 8 at `p = 3200` (exact decisions). The one failure
  is the finite-size form of the many-violator balance behind
  Corollary 3.4, not yet its asymptotic regime.
- In pure noise, B&B trees and exactly certified conflict cliques grow
  quickly with `k` (`k <= 8`) at every `alpha`, fastest at `alpha = 4`
  (median clique 112 at `k = 8`), where the planted problem on the same
  designs is solved in at most 17 nodes with clique 1. Below the recovery
  threshold in the planted model, cliques grow slowly.
- Most-fractional and largest-`z` branching behave alike at `p <= 200`.

## 1. Setting, relaxation and B&B conventions

### 1.1 Model

- `X in R^{n x p}` has iid `N(0,1)` entries and columns `x_1, ..., x_p`.
- `S* ⊂ [p]`, `|S*| = k`. In Section 3, `beta*_i = ±b` on `S*` (signs
  arbitrary) and 0 elsewhere. Section 4 also treats `beta* = 0` and general
  `beta*` with `||beta*||^2 = B^2`.
- `w ~ N(0, I_n)` is independent of `X`, and `y = X beta* + sigma w`.
- `lam > 0` is deterministic (it may depend on `n, p, k, b, sigma`).

### 1.2 Problem and perspective relaxation

For `S ⊆ [p]` let `M_S = I_n + X_S X_S'/lam` and

```
f(S)   = min_beta ||y - X_S beta||^2 + lam ||beta||^2 = y' M_S^{-1} y,
beta^S = (X_S'X_S + lam I)^{-1} X_S' y,     r_S = y - X_S beta^S = M_S^{-1} y.
```

Then `f(S) = y' r_S = ||r_S||^2 + lam ||beta^S||^2` and
`X_S' r_S = lam beta^S`. The problem is `OPT = min{ f(S) : |S| <= k }`. Since
`f` does not increase when features are added, some optimal support has
exactly `k` elements.

For `z in [0,1]^p` let `M_z = I_n + X diag(z) X'/lam` and
`g(z) = y' M_z^{-1} y`.

- (F1) `g(1_S) = f(S)`.
- (F2) `g(z) = min{ ||y - X beta||^2 + lam sum_{i: z_i>0} beta_i^2/z_i :
  beta_i = 0 if z_i = 0 }`, the perspective relaxation.
- (F3) `g(z) = max_a h(a,z)` with
  `h(a,z) = 2a'y - ||a||^2 - (1/lam) sum_i z_i (x_i'a)^2`, maximized at
  `a(z) = M_z^{-1} y`.
- (F4) `g` is convex and continuous on `[0,1]^p`.

*Proof.* `h(., z) = 2a'y - a'M_z a` is strictly concave with maximizer
`M_z^{-1}y` and maximum `y'M_z^{-1}y`, which is (F3). For (F2), fix `z` with
support `P`; the minimization is a generalized ridge problem, and the identity
`min_beta ||y - A beta||^2 + beta'Q beta = y'(I + A Q^{-1} A')^{-1} y`
for `Q ≻ 0`, with `A = X_P` and `Q = lam diag(z_P)^{-1}`, gives `g(z)`. (F4): `g` is
a pointwise maximum of functions affine in `z`, and the formula is continuous.
(F1) is (F2) at `z = 1_S`. ∎

Let `K = {z in [0,1]^p : sum z <= k}`. For disjoint `S0, S1 ⊆ [p]` with
`|S1| <= k`, the node relaxation is

```
r(S0,S1) = min{ g(z) : z in K, z_{S0} = 0, z_{S1} = 1 },    R = r(∅,∅).
```

Write `top_m(A)` for the sum of the `m` largest elements of a multiset `A`
(all of them if `|A| <= m`).

**Lemma 1.1 (dual bounds).** For every `a in R^n`, with `c = X'a` and
`F = [p] \ (S0 ∪ S1)`,

```
r(S0,S1) >= L_{S0,S1}(a) := 2a'y - ||a||^2
            - (1/lam) [ sum_{i in S1} c_i^2 + top_{k-|S1|}{ c_i^2 : i in F } ].
```

Equality holds for a maximizing `a`.

*Proof.* For feasible `z`, `g(z) >= h(a,z)` by (F3), and
`sum_i z_i c_i^2 <= sum_{S1} c_i^2 + top_{k-|S1|}(c_F^2)` because
`z_F in [0,1]^F` and `sum z_F <= k - |S1|`. Equality follows from Sion's
minimax theorem: `h` is concave in `a`, affine in `z`, and the feasible
`z`-set is compact and convex. ∎

This is the dual of PWE after minimizing out `beta`. The equality of the
perspective form (F2) and PWE's Boolean relaxation is due to Xie and Deng
(arXiv 1806.03756); (F3) and Lemma 1.1 are PWE's duality. Bounds of this
type at fixed nodes underlie the safe screening rules of Atamtürk and Gómez
(arXiv 2004.08773): Lemma 2.2 below, evaluated at the root-optimal residual,
is their Proposition 2 for the cardinality-constrained problem (read in
their paper: fix `z_i = 0` if `zeta_CC - gamma(delta_i - delta_[k]) > zeta_bar`,
fix `z_i = 1` if `zeta_CC + gamma(delta_i - delta_[k+1]) > zeta_bar`, with
`delta_i` the squared correlations of the root residual). C1 is the same
test with each single-fixing node relaxation solved exactly instead of
bounded at the root dual.

### 1.3 Branch-and-bound conventions

- *Variable branching.* A node carries fixings `(S0, S1)`. Branching on a free
  `i` creates `(S0+i, S1)` and `(S0, S1+i)`. The node bound is `r(S0,S1)` or a
  computed lower bound on it. Nodes are pruned by bound (bound
  `>= UB - eps`, where `UB` is the incumbent value), by integrality (a
  relaxation minimizer is integral; its value is then `>= OPT`), or by
  infeasibility (`|S1| > k`).
- *Convex-piece trees and certificates* (scout report, Section 3.1, with the
  corrections of [the review](../../reviews/bb-conflict-review.md)). A finite
  rooted tree whose nodes carry convex sets `Q_v`; the children of `v` cover
  the feasible 0/1 points of `Q_v`; the node bound is
  `r(v) = inf{ g(z) : z in K ∩ Q_v }`. An `eps`-certificate is such a tree
  whose leaves all satisfy `r(v) >= OPT - eps`. Variable, general split,
  multiway and SOS branching are included. Incumbent-based domain reductions
  are *not* included unless stated.
- *Condition C1 at an optimal support `S°`*: `r({i},∅) >= OPT - eps` for all
  `i in S°` (removal half) and `r(∅,{j}) >= OPT - eps` for all `j ∉ S°`
  (forced-in half). *Strict C1*: all these bounds are `> OPT`.

**Lemma 1.2 (path lemma; scout Lemma 4 with the review's correction).**
Assume C1 at `S°`, and node bounds computed exactly or with an error that
keeps the single-wrong-fixing bounds `>= OPT - eps`.

- (a) If the incumbent value `OPT` is available whenever a node not
  containing `1_{S°}` is examined (for example, it is given at the start),
  then for any branching rule and any node order the tree has at most
  `2d + 1 <= 2p + 1` nodes, where `d` is the number of branchings at nodes
  containing `1_{S°}`.
- (b) If strict C1 holds (and computed bounds at single-wrong-fixing
  descendants stay `> OPT`), the same bound holds for best-bound node
  selection without an initial incumbent.

*Proof.* Adding fixings shrinks the feasible set, so bounds are monotone.
The nodes containing `1_{S°}` form a path from the root. A node off this
path has a wrong fixing, so its bound is at least the corresponding
single-fixing bound. (a) Each off-path node is a child of a path node and is
pruned when examined, so the tree has at most `d+1` path nodes and `d`
off-path nodes. (b) Path nodes have bound `<= OPT` (they contain a point of
value `OPT`), off-path nodes have bound `> OPT`, so best-bound search examines
path nodes while one is open. The last path node is pruned by integrality
(then `UB = OPT`, because an integral relaxation minimizer of value `<= OPT`
is optimal) or by bound (then `UB <= OPT + eps`). The path cannot continue
past depth `p`. Afterwards every open node is off-path, with bound
`> OPT >= UB - eps`, and is pruned when examined. ∎

**Lemma 1.3 (the removal half suffices for a small certificate).** Let `S°`
be optimal with `|S°| = k` and suppose `r({i},∅) >= OPT - eps` for every
`i in S°`. Branching on the elements of `S°` in any order, always continuing
in the child `z_i = 1`, gives a variable-branching `eps`-certificate with
`2k + 1` nodes.

*Proof.* After all of `S°` is fixed to 1, the budget `sum z <= k` forces
`z = 1_{S°}`, so the node value is `f(S°) = OPT`. Each child `z_i = 0` has
bound `>= r({i},∅) >= OPT - eps` by monotonicity. ∎

So wherever the removal half holds, the minimum variable-branching tree has at
most `k+1` leaves, and every lower bound valid for all variable-branching
trees (conflict cliques included) is at most `k+1`. Large trees in that
regime come from the branching rule, not from the relaxation.

**Lemma 1.4 (conflict bound; scout Theorem 1 in the review's form).** If
`|S|, |T| <= k`, `S != T`, and `g((1_S+1_T)/2) < OPT - eps`, then no leaf of
an `eps`-certificate contains both `1_S` and `1_T`. Hence the number of leaves
is at least the clique number `omega(G_eps)` of the graph with these edges.
With incumbent-based variable-bound reductions whose removed parts all have
bound `>= OPT - eps` (OBBT on `{g <= UB}`, reduced-cost fixing, probing), the
number of *nodes* is at least `omega(G_eps)/(2p+1)` (review, Section 2.3).
The midpoint may be replaced by any point of the segment `[1_S, 1_T]`. The
bounds remain valid when node bounds are computed lower bounds (such as
Lemma 1.1) and for every relaxation pointwise below `g` on `K`; adding
big-M constraints `|beta_i| <= M z_i` changes the relaxation and is not
covered. For binary variables the node form holds even with `p+1` in place
of `2p+1` (the reductions at one node fix each variable at most once, so they
add at most `p` pruned pieces per node), and it says something only when the
clique exceeds `2p+1`.

*Proof.* Every 0/1 point lies in some leaf. If a leaf `v` contained both
points, then the midpoint would lie in `Q_v ∩ K` by convexity, and
`r(v) <= g(midpoint) < OPT - eps`. The node form is the review's reduction
argument. ∎

**Lemma 1.5 (midpoint formula).** For supports `S, T` let `U = S ∪ T`,
`C = S ∩ T`, `D = S Δ T`. Then

```
g((1_S+1_T)/2) = min_{beta: supp beta ⊆ U} ||y - X beta||^2 + lam ||beta_C||^2 + 2 lam ||beta_D||^2.
```

Consequently, extending `beta^S, beta^T` by zeros:

- (a) `g((1_S+1_T)/2) <= f_{2lam}(U) := min_{supp beta ⊆ U} ||y - X beta||^2 + 2 lam ||beta||^2`,
  with equality if `C = ∅`;
- (b) `g((1_S+1_T)/2) <= (f(S)+f(T))/2 - ||X(beta^S - beta^T)||^2/4 - lam ||beta^S_C - beta^T_C||^2/4`.

*Proof.* The formula is (F2) with `z = 1` on `C` and `z = 1/2` on `D`.
(Equivalently, `X diag(z) X' = (X_S X_S' + X_T X_T')/2`, so
`g((1_S+1_T)/2) = min_{b1, b2} ||y - X_S b1 - X_T b2||^2 + 2 lam(||b1||^2 + ||b2||^2)`;
splitting a shared coefficient optimally between its two copies gives the
penalty `lam` on `C`.) (a) replaces `lam` by `2 lam` on `C`. For (b) take `beta = (beta^S+beta^T)/2`. By
the parallelogram identity,
`||y - X beta||^2 = (||r_S||^2 + ||r_T||^2)/2 - ||X(beta^S-beta^T)||^2/4`.
For `i in C`, `lam beta_i^2 = lam((beta^S_i)^2 + (beta^T_i)^2)/2 - lam(beta^S_i - beta^T_i)^2/4`;
for `i in S \ T`, `2 lam (beta^S_i/2)^2 = lam (beta^S_i)^2/2`, and similarly
on `T \ S`. Summing and using `f(S) = ||r_S||^2 + lam ||beta^S||^2` gives (b). ∎

So `S` and `T` conflict whenever `f_{2lam}(S ∪ T) < OPT - eps`, or whenever

```
||X(beta^S - beta^T)||^2 + lam ||beta^S_C - beta^T_C||^2 > 2(f(S) - OPT) + 2(f(T) - OPT) + 4 eps.
```

The second form is the inequality proposed in the program (with the extra
`lam ||beta^S_C - beta^T_C||^2` term). Form (a) is exact for disjoint
supports and is the one used in Section 4. The formula, (a) and (b) were
checked numerically on 30 random instances (`code/check_lemmas.py`: relative
error `<= 2e-15` for the formula; no violation of (a) or (b)).

## 2. Deterministic certificates for single fixings

Fix `S` with `|S| = k` and write `r = r_S`, `a = X'r` (so `a_S = lam beta^S`),
`m0 = min_{i in S} |a_i| = lam min_i |beta^S_i|`. For `V ⊆ [p] \ S` and
`u in R^V` put

```
H_V = X_V' M_S^{-1} X_V,     Delta = M_S^{-1} X_V u,     alpha = r - Delta,     c = X'alpha.
```

**Lemma 2.1 (witness identity).** `h(alpha, 1_S) = f(S) - u'H_V u`,
`c_V = a_V - H_V u`, and `||Delta||^2 <= u'H_V u`.

*Proof.* `h(alpha, 1_S) = 2 alpha'y - alpha'M_S alpha`. With `r = M_S^{-1}y`,
`alpha'M_S alpha = y'M_S^{-1}y - 2u'X_V'M_S^{-1}y + u'H_V u = f(S) - 2u'a_V + u'H_V u`
and `2 alpha'y = 2f(S) - 2u'a_V`. Subtracting gives the first identity.
`X_V'alpha = X_V'r - H_V u`. Finally `M_S ⪰ I` implies
`M_S^{-2} ⪯ M_S^{-1}`, so `||Delta||^2 = u'X_V'M_S^{-2}X_V u <= u'H_V u`. ∎

**Lemma 2.2 (single-fixing bounds).** Let `alpha in R^n`, `c = X'alpha`,
`m = min_{i in S}|c_i|`, `M = max_{l ∉ S}|c_l|`, and suppose `M <= m`. Then

```
r({i},∅) >= h(alpha,1_S) + (c_i^2 - M^2)/lam      (i in S),
r(∅,{j}) >= h(alpha,1_S) + (m^2 - c_j^2)/lam      (j ∉ S),
R        >= h(alpha,1_S).
```

*Proof.* Use Lemma 1.1 and `2 alpha'y - ||alpha||^2 = h(alpha,1_S) + lam^{-1} sum_S c_i^2`.
Since `M <= m`: the `k` largest of `{c_l^2 : l != i}` are `c^2_{S \ i}` and
`M^2`; the `k-1` largest of `{c_l^2 : l != j}` sum to `sum_S c_i^2 - m^2`; the
`k` largest of all are `c_S^2`. ∎

**Proposition 2.3 (saturated witness).** Let `kappa > 0`,
`V = {l ∉ S : |a_l| > kappa}`, `s = sign(a_V)`, assume `H_V` is invertible
(`V = ∅` is allowed), and set

```
u = H_V^{-1}(a_V - kappa s),     Gamma = u'H_V u = (a_V - kappa s)' H_V^{-1} (a_V - kappa s).
```

Define `alpha, c, m, M` as above. If `M <= m` and `Gamma < (m^2 - M^2)/lam`,
then every node with a single wrong fixing relative to `S` has bound at least
`f(S) + (m^2 - M^2)/lam - Gamma > f(S)`. In particular `S` is the unique
optimal support, strict C1 holds at `S`, and Lemma 1.2 applies. Moreover
`f(S) - R <= Gamma`.

*Proof.* Lemma 2.1 gives `h(alpha,1_S) = f(S) - Gamma`; apply Lemma 2.2. Any
support `T != S` with `|T| <= k` contains some `j ∉ S` or misses some
`i in S`, so `1_T` lies in a single-wrong-fixing node and
`f(T) = g(1_T) > f(S)`. ∎

The witness "caps" every violator at exactly `kappa` (`c_V = kappa s`) at the
price `Gamma`, which is of order `sum_l (|a_l| - kappa)_+^2 / n`. With
`V = ∅` (that is, `kappa >= max_{l ∉ S}|a_l|`) it reduces to `alpha = r`, the
PWE certificate:

**Corollary 2.4 (root exactness at `S`; PWE Corollary 2).**
`R = f(S)` if and only if `max_{l ∉ S}|a_l| <= m0`.

*Proof.* "If": Lemma 2.2 with `alpha = r`. "Only if": suppose `R = f(S)`, so
`1_S` minimizes `g` over `K`. Let `alpha*` maximize the concave dual function
of Lemma 1.1 (it exists because of the `-||a||^2` term). By Sion's theorem,
`(alpha*, 1_S)` is a saddle point of `h` on `R^n x K`. Hence `alpha*`
maximizes `h(., 1_S)`, so `alpha* = M_S^{-1}y = r`, and `1_S` maximizes
`sum_i z_i a_i^2` over `K`, which forces `min_S a_i^2 >= max_{l ∉ S} a_l^2`. ∎

**Lemma 2.5 (explicit upper bound for forced-in nodes).** Let `j ∉ S`,
`V' ⊆ [p] \ (S ∪ {j})`, `b_+ = max_{i in S}|beta^S_i|`, `kappa >= lam b_+`,
`e_l = (|a_l| - kappa)_+`, `Q = sum_{V'} e_l^2`, `L = ||X_{V'}||_op^2`,
`s in (0,1]`, `w_l = s sign(a_l) e_l / L`, `t_l = lam |w_l|/kappa`, and
`T = sum_{V'} t_l`. If `max_l t_l <= 1` and `T < k - 1`, then

```
r(∅,{j}) <= f(S) + lam b_+^2 [ 1 + (1+T)^2/(k-1-T) ] - (2s - s^2) Q/L.
```

*Proof.* Take `z_i = 1 - (1+T)/k` on `S`, `z_j = 1`, `z_l = t_l` on `V'`, and
0 elsewhere; then `z in K` and `z_j = 1`. Take `beta = beta^S` on `S`,
`beta = w` on `V'`, 0 elsewhere. By (F2), `g(z)` is at most

```
||r - X_{V'}w||^2 + lam ||beta^S||^2 k/(k-1-T) + kappa sum|w_l|
 = f(S) + lam ||beta^S||^2 (1+T)/(k-1-T) - 2 sum|w_l||a_l| + ||X_{V'}w||^2 + kappa sum|w_l|,
```

using `lam w_l^2/t_l = kappa |w_l|`. Now `lam ||beta^S||^2 <= k lam b_+^2`,
`k(1+T)/(k-1-T) = (1+T)(1 + (1+T)/(k-1-T))`, and
`lam b_+^2 T = (lam^2 b_+^2/kappa) sum|w_l| <= kappa sum|w_l|`. Hence
`g(z) <= f(S) + lam b_+^2 [1 + (1+T)^2/(k-1-T)] - 2 sum|w_l| e_l + ||X_{V'}w||^2`
(terms with `e_l = 0` vanish). Finally `2 sum |w_l| e_l = 2sQ/L` and
`||X_{V'}w||^2 <= L ||w||^2 = s^2 Q/L`. ∎

## 3. Easy side: sharp thresholds for root exactness and for C1

### 3.1 Statements

Notation, with `S = S*`:

```
b_lam = b n/(n+lam),   omega_lam^2 = n sigma^2 + k b^2 lam^2 n/(n+lam)^2,
tau_lam = lam b_lam / omega_lam,   L_lam = log(p lam / n).
```

Heuristically, `m0 ≈ lam b_lam` and `||r_{S*}|| ≈ omega_lam`, and each null
correlation `a_l = x_l' r_{S*}` is exactly `N(0, ||r_{S*}||^2)` given
`(X_{S*}, w)`. So `tau_lam` is the true-feature signal measured in units of
the null-correlation noise.

**Assumption (A).** `b, sigma > 0`, `C0 > 0` and `eps in (0,1)` are fixed;
`p -> inf`; `log^6 p <= n <= p`; `1 <= k <= C0 n/log p`;
`sqrt(n) <= lam <= n/log^2 p`.

The condition `log^6 p <= n <= p` can hold only if `log^6 p <= p`, that is,
`p >= e^17 ≈ 2.4 × 10^7`. All computations in Section 6 lie outside (A); they
illustrate trends and finite-size behavior, and do not test the theorems'
constants.

**Theorem 3.1 (root exactness).** Assume (A).

- (a) If `tau_lam^2 >= (2+eps) log p` for all large `p`, then w.h.p.
  `R = OPT = f(S*)`, `S*` is the unique optimal support, and strict C1 holds.
  B&B with incumbent value `OPT` prunes the root.
- (b) If `tau_lam^2 <= (2-eps) log p` for all large `p`, then w.h.p.
  `R < f(S*)`. So the root relaxation is not exact whenever `S*` is optimal.
- (c) If `n >= (2+eps) k log p`, some `lam` satisfying (A) meets (a). If
  `n <= (2-eps) k log p`, every `lam` satisfying (A) meets (b).

**Theorem 3.2 (single-fixing probing, C1).** Assume (A).

- (a) If `tau_lam^2 >= (2+eps) L_lam` for all large `p`, then w.h.p. `S*` is
  the unique optimal support and every single wrong fixing at `S*` has
  relaxation bound at least `OPT + lam b^2/log p`. Consequently, by
  Lemma 1.2, every variable-branching B&B tree (any rule; incumbent `OPT`
  available, or best-bound search) has at most `2d+1 <= 2p+1` nodes.
- (b) If `tau_lam^2 <= (2-eps) L_lam` for all large `p` and
  `k >= 5000/eps^2`, then w.h.p. all but at most `n/log^2 p` null features
  `j` satisfy `r(∅,{j}) < f(S*) - lam b^2/2`. So C1 fails whenever `S*` is
  optimal.
- (c) If `n >= (2+eps) k log(p/sqrt n)`, some `lam` satisfying (A) meets (a);
  one can take `lam = (sigma/b) sqrt(T n)` with
  `T = A/(1 - A k/n)`, `A = (2 + eps/2)(1 + eps/8) log(p/sqrt n)`; thus
  `T = Theta_eps(log p)`, and `T` depends also on `n/(k log(p/sqrt n))`
  through the denominator. If `n <= (2-eps) k log(p/sqrt n)` and `k >= 5000/eps^2`,
  every `lam` satisfying (A) meets (b).

*Explicit form for a given ridge.* Write `lam = ell (sigma/b) sqrt n`. For
`lam <= n/log^2 p`, `tau_lam^2 = (1 + O(log^{-2} p)) ell^2 n/(n + k ell^2)`.
So, up to the `(1 + o(1))` factors, the hypothesis of Theorem 3.2(a) reads

```
ell^2 > (2+eps) L_lam     and     n >= (2+eps) k L_lam / (1 - (2+eps) L_lam/ell^2),     L_lam = log(p ell sigma/(b sqrt n)),
```

and that of Theorem 3.1(a) is the same with `L_lam` replaced by `log p`. The
constant in `n >= C k log p` is therefore
`C = (2+eps)(L_lam/log p)/(1 - (2+eps) L_lam/ell^2)`; it tends to
`2 L_lam/log p` as `ell` grows (while `lam <= n/log^2 p`) and depends on
`b/sigma` only through `L_lam` and the requirement `ell^2 > 2 L_lam`.

**Corollary 3.3 (linear trees strictly below root exactness).** Let
`k = p^{gamma+o(1)}` with `gamma in (0,1)` and `n = alpha k log p`, so that
`log(p/sqrt n) = (1 - gamma/2 + o(1)) log p`.

- For `alpha in (2 - gamma, 2)`, with `lam` as in Theorem 3.2(c): w.h.p. the
  root relaxation is not exact, yet every variable-branching tree has at most
  `2p+1` nodes, provided the incumbent `OPT` is available when off-path
  nodes are examined or best-bound node selection is used (Lemma 1.2).
- For `alpha < 2 - gamma` and `k >= 5000/eps^2`: w.h.p. C1 fails at `S*` for
  every `lam` satisfying (A).
- For `alpha > 2`: some `lam` makes the root exact.

*Proof.* Combine Theorems 3.1 and 3.2. For the first item, Theorem 3.2(a)
gives C1 and that `S*` is optimal, and Theorem 3.1(c) gives `R < f(S*) = OPT`
because `n <= (2 - eps') k log p` for some `eps' > 0`. ∎

**Corollary 3.4 (the fixed ridge `lam = sqrt n`).** Assume (A) with
`lam = sqrt n`. Then `tau_lam <= b/sigma` and `L_lam = log(p/sqrt n)`. If
`p/sqrt(n) >= exp(b^2/((2-eps) sigma^2))` and `k >= 5000/eps^2`, then w.h.p.
C1 fails at `S*` (Theorem 3.2(b)), for every `n` in (A); the root is exact
only if `b^2/sigma^2 > (2-eps) log p` (Theorem 3.1(b)).

*Proof.* `b_lam <= b` and `omega_lam >= sigma sqrt n` give
`tau_lam^2 <= lam^2 b^2/(n sigma^2) = b^2/sigma^2`. ∎

Corollary 3.4 is a statement about the limit only. The proof of
Theorem 3.2(b) uses `N' >= 3 n/(delta0^2 lam)` nearly orthogonal violators
with `N' <= n/log^2 p`; for `lam = sqrt n` this needs
`sqrt(n) >= 3 log^2 p/delta0^2`, that is, astronomically large `n`. The same
remark applies to Theorem 3.2(b) and the second item of Corollary 3.3 for
every `lam`: at `tau_lam^2 = (2 - eps) L_lam`, a mean-field estimate of the
violators' gain relative to the budget price is about
`1.6 (p lam/n)^{eps/2}/tau^5` (independent review), which exceeds 1 only for
`p lam/n` of order `10^17` when `eps = 1/2`. At the sizes we can solve, the
root gap stays moderate because the many violators overlap in `R^n`, and C1
holds in 15 of 16 runs at `p = 800, 3200`. In the one failure (Section 6.3)
the violators recover about 60% of the budget price for every forced-in
null, and four nulls fail: the many-violator mechanism is already visible
at finite size there, though not yet in its asymptotic form, where the
violators alone outweigh the price for almost every null. The scout's
observation of C1 for `alpha >= 1.4` at `p = 6k <= 120` is consistent with
this.

**Remark 3.5 (PWE's Gaussian theorem is false as stated).** Page numbers
refer to Pilanci, Wainwright and El Ghaoui, Math. Program. Ser. B 151 (2015)
63–87 (author-hosted PDF), as checked in the independent verification report
[`../../reviews/pwe-verification.md`](../../reviews/pwe-verification.md).
Their Section 3.1 (p. 72) takes `X` with iid `N(0,1)` entries and noise
`epsilon` with iid `N(0, gamma^2)` entries, and their Theorem 2 (p. 72)
states: if `n > c0 (gamma^2 + ||w*_S||^2)/w_min^2 log d` and `rho = sqrt n`,
then with probability at least `1 - 2e^{-c1 n}` the relaxation is integral.

*Why the statement is false.* Fix `d > k`, `w*` with support `S`, and
`gamma > 0`, and let `n -> inf` with `rho = sqrt n`.

1. The optimal support is `S` with probability tending to 1: a support
   `T != S` with `|T| = k` misses some `j in S`, and
   `f(T) - f(S) = n ||w*_{S \ T}||^2 (1 + o_P(1)) -> inf`.
2. `X_S'M_S^{-1} y = rho beta^S` with `beta^S -> w*`, so
   `m0/sqrt n = min_{j in S}|a_j|/sqrt n -> w_min`.
3. For `l ∉ S`, `x_l` is independent of `(X_S, epsilon)`, so given these the
   `a_l = x_l'M_S^{-1} y` are iid `N(0, ||r||^2)`, and `||r||^2/n -> gamma^2`.
4. By their Corollary 2 (p. 71; our Corollary 2.4), applied at the optimal
   support, the probability that the relaxation is exact tends to
   `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`.

The hypothesis of Theorem 2 holds for all large `n` and `1 - 2e^{-c1 n} -> 1`,
so the theorem fails for every choice of `c0` and `c1`. For `d = 50`, `k = 5`,
`w_min = 1`, `gamma = 0.5` the limit is 0.123. (Within this note, Theorem 3.1(b)
and Corollary 3.4 give the same conclusion in regime (A), but the argument
above is self-contained and covers PWE's fixed-`d` setting.)

*Where the proof goes wrong* (Appendix 7.1, pp. 81–85). Here
`M = (I + rho^{-1} X_S X_S')^{-1}` is PWE's matrix, our `M_S^{-1}`. The two
lemmas are proved for different normalizations of `U_j`. PWE define
`U_j = X_j'M y/(rho n)` (p. 81), split into `A_j + B_j`. Under that
normalization Lemma 1 (bound on `max_j |B_j|`) is true, but Lemma 2 (34a),
`min_{j in S}|A_j| >= w_min/4`, is false, because `A_j ≈ w*_j/n`. The proof of
Lemma 2 (pp. 83–85) in fact works with `U_j = X_j'M y/rho`; under that
normalization Lemma 2 holds, but Lemma 1 is false, because
`B_j = X_j'M epsilon/rho` has standard deviation about `gamma` and
`max_j |B_j| ≈ gamma sqrt(2 log d)` does not shrink with `n`. The mismatch is
hidden by two incorrect steps in the proof of Lemma 1 (p. 82): the claim
`sigma_max(M) <= rho^{-1}` (in fact `M` has eigenvalue 1 on the orthogonal
complement of the columns of `X_S`), and the variance bound `4 gamma^2/rho^2`
for `X_j'M epsilon/rho` (from `||M X_j|| <= 2 sqrt n` the bound is
`4 n gamma^2/rho^2 = 4 gamma^2`). No normalization can rescue the argument:
the comparison of `min_S |a_j| ≈ sqrt(n) w_min` with
`max_{S^c}|a_l| ≈ sqrt(n) gamma sqrt(2 log d)` is scale-invariant.

*Numerical evidence.*

- `code/check_pwe.py` (this note): `d = p = 50`, `k = 5`, `w_min = b = 1`,
  `gamma = 0.5`, `rho = sqrt n`, 10 instances each at `n = 500` (`c0 ≈ 24`)
  and `n = 5000` (`c0 ≈ 243`). In 19 of 20 instances an exact C1 decision
  certifies that `S*` is the unique optimal support, while the root
  relaxation value is strictly below `f(S*) = OPT` (relative gap `4e-6` to
  `1.4e-3`) and the exactness certificate of Corollary 2.4 fails.
- The verification report confirms `S*` as the unique optimum by full
  enumeration and finds the relaxation strictly inexact in 13 of 16 instances
  (8 of the 16 regenerate the easy-side review's instances). Its Monte Carlo
  exactness frequencies are 0.080, 0.093, 0.113 and 0.153 at `n = 500` to
  `50000` (`c0` from 24 to 2434), consistent with the limit 0.123 (the last
  95% interval, [0.096, 0.211], contains it); its lower-variance conditional
  estimates 0.052, 0.081, 0.104 and 0.114 approach 0.123 from below.

*Literature status* (from the verification report). Crossref lists no
erratum. Pilanci's 2016 PhD thesis (UCB/EECS-2016-147, Theorem 12, p. 180,
proof pp. 199–200) repeats the theorem and proof unchanged. Dong
(arXiv 1603.04572, Theorem 3) and Bertsimas–Pauphilet–Van Parys
(arXiv 1902.06547) cite the theorem as valid. The search was limited, so an
informal correction cannot be excluded.

*What survives.* PWE's exactness characterization (their Corollary 2, our
Corollary 2.4) and their algorithms are unaffected.

- *Total-energy noise.* If `epsilon` has iid `N(0, gamma^2/n)` entries, PWE's
  argument goes through once `U_j` is normalized by `rho` and
  `sigma_max(M) <= 1` is used; the printed bound `4 gamma^2/rho^2` is then
  valid. The verification report checked this repair at the level of the
  displayed steps of Appendix 7.1, not every constant. According to it, this
  gives their sample-size condition with an unspecified `c0` and failure
  probability `c exp(-c' n w_min^2/(gamma^2 + ||w*||^2))`, which is of the form
  `e^{-c1 n}` only when `k` and `gamma/w_min` stay bounded. Its Monte Carlo
  exactness probability (for `d = 50`, `k = 5`) is 0.99 or more from
  `n ≈ 5 (gamma^2 + ||w*||^2)/w_min^2 log d`.
- *Our extension.* Theorem 3.1 assumes fixed `sigma`. Its proof (Step 1 of
  Section 3.3 and Section 3.4) uses `sigma` only through `omega_lam`, through
  the scale-free bound
  `2 sigma ||v|| sqrt(2 log p) <= sqrt(2 log p/n)(n sigma^2 + ||v||^2)` on the
  cross term, and through the leave-one-out term `(sigma/b) sqrt(log p/n)`,
  which only shrinks as `sigma` decreases. So Theorem 3.1 remains valid for
  `sigma = gamma/sqrt n` (inside (A) otherwise); this extension was
  confirmed by the recheck [`../../reviews/sparse-recheck.md`](../../reviews/sparse-recheck.md).
  With `lam = sqrt n` it gives `tau_lam^2 = (1+o(1)) n b^2/(gamma^2 + k b^2)`,
  hence, for equal magnitudes `b`, `p -> inf` and the other conditions of
  (A), exactness at `S*` w.h.p. iff `n >= (2+o(1))(k + gamma^2/b^2) log p`.
  For fixed `gamma`, the condition `log^6 p <= n` of (A) forces `k -> inf`,
  so the `gamma^2/b^2` term lies inside the `o(1)` and the sharp constant
  concerns the `k` term. The proof also allows `gamma = gamma_n` with
  `gamma^2 = O(k b^2)` (then `sigma = O(b sqrt(k/n)) -> 0` and every error
  term still vanishes); in that case the coefficient 2 applies to both terms
  (the recheck's simulation at `gamma^2/b^2 = k` agrees). This identifies the
  sharp constant `c0 = 2` in that asymptotic regime; it does not prove PWE's
  non-asymptotic statement with probability `1 - 2e^{-c1 n}`, and it says
  nothing about PWE's fixed-`d`, `n -> inf` setting.
- *Per-entry noise.* Some assumption of the form `w_min^2/gamma^2 >= C log d`
  is necessary, since otherwise the exactness probability has the limit above,
  below 1. According to the verification report, such an assumption repairs
  the argument, but only with probability at least
  `1 - c d^{-c'} - c exp(-c'' n w_min^2/||w*||^2)`, not `1 - 2e^{-c1 n}`: for
  fixed `d`, `w*`, `gamma` the exactness probability still tends to
  `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`.

### 3.2 Probabilistic tools

We use the following standard facts.

- (G1) For `Z ~ N(0,1)` and `t >= 0`, `P(|Z| > t) <= e^{-t^2/2}`, and
  `phi(t) t/(1+t^2) <= Phibar(t) <= phi(t)/t` (`t > 0`), where `phi` and
  `Phibar` are the standard normal density and upper tail.
- (G2) (Laurent–Massart) For `chi^2_d` and `t > 0`:
  `P(chi^2_d >= d + 2 sqrt(dt) + 2t) <= e^{-t}` and
  `P(chi^2_d <= d - 2 sqrt(dt)) <= e^{-t}`.
- (G3) (Davidson–Szarek, Gordon) For `A in R^{d x m}` with iid `N(0,1)`
  entries, `d >= m`, and `t > 0`: `s_max(A) <= sqrt d + sqrt m + t` and
  `s_min(A) >= sqrt d - sqrt m - t`, each with probability `>= 1 - e^{-t^2/2}`.
- (G4) (Chernoff) For `N ~ Bin(N0, q)` with mean `mu`:
  `P(N >= 2mu + 3t) <= e^{-t}` and `P(N <= mu/2) <= e^{-mu/8}`.
  (From `P(N >= mu + x) <= exp(-x^2/(2(mu + x/3)))` with `x = mu + 3t`, and
  the multiplicative lower tail.)
- (G5) (truncated squares) Let `Z_1, ..., Z_N` be iid `N(0,1)`, `tau > 0`,
  and `Y_l = (|Z_l| - tau)_+^2`. Then
  `m(tau) := E e^{Y/4} - 1 = 2 sqrt2 e^{tau^2/2} Phibar(sqrt2 tau) - 2 Phibar(tau) <= 2 phi(tau)/tau`,
  and `P(sum_l Y_l >= 4(N m(tau) + t)) <= e^{-t}`.

*Proof of (G5).* For `z > tau`, `-z^2/2 + (z-tau)^2/4 = -(z+tau)^2/4 + tau^2/2`,
so `int_tau^inf e^{(z-tau)^2/4} phi(z) dz = sqrt2 e^{tau^2/2} Phibar(sqrt2 tau)`,
which gives the formula. By (G1),
`m(tau) <= 2 sqrt2 e^{tau^2/2} phi(sqrt2 tau)/(sqrt2 tau) = 2 phi(tau)/tau`.
Chernoff: `P(sum Y >= s) <= e^{-s/4} (1+m)^N <= exp(N m - s/4)`. ∎

**Lemma 3.6 (leave-one-out coefficients).** For `i in S`, let
`A_i = M_{S \ i}^{-1}` and `y_(i) = y - beta*_i x_i`. Then

```
beta^S_i = (beta*_i q_i + xi_i)/(lam + q_i),    q_i = x_i'A_i x_i,    xi_i = x_i'A_i y_(i).
```

Conditionally on `(X_{S \ i}, w)`, `xi_i ~ N(0, ||A_i y_(i)||^2)`, and
`||P^perp_{S \ i} x_i||^2 <= q_i <= ||x_i||^2`, where `P^perp_{S \ i}`
projects onto the orthogonal complement of the columns of `X_{S \ i}`.

*Proof.* Minimizing over `beta_{S \ i}` first,
`f(S) = min_{beta_i} (y - x_i beta_i)'A_i(y - x_i beta_i) + lam beta_i^2`,
because `min_beta ||v - X_{S\i} beta||^2 + lam ||beta||^2 = v'A_i v`. Hence
`beta^S_i = x_i'A_i y/(x_i'A_i x_i + lam)`; substitute
`y = beta*_i x_i + y_(i)`. Here `x_i` is independent of `(A_i, y_(i))`, and
`P^perp_{S \ i} ⪯ A_i ⪯ I`. ∎

**Lemma 3.7 (residual).** Let `G = X_S'X_S` with extreme eigenvalues
`s_-, s_+`, and `v = M_S^{-1} X_S beta* = lam X_S (lam + G)^{-1} beta*`. Then
`r = v + sigma M_S^{-1} w`,

```
||beta*||^2 min_{s in [s_-,s_+]} lam^2 s/(lam+s)^2 <= ||v||^2 <= ||beta*||^2 max_{s in [s_-,s_+]} lam^2 s/(lam+s)^2,
||P^perp_S w||^2 <= ||M_S^{-1} w||^2 <= ||w||^2,
```

and, given `X_S`, `v'M_S^{-1}w ~ N(0, ||M_S^{-1}v||^2)` with
`||M_S^{-1}v|| <= ||v||`.

*Proof.* `M_S^{-1} X_S = lam X_S (lam+G)^{-1}` (push-through identity), so
`||v||^2 = lam^2 beta*'(lam+G)^{-1} G (lam+G)^{-1} beta*`. `M_S^{-1}` has
eigenvalue 1 on the orthogonal complement of the columns of `X_S` and
eigenvalues in `(0,1)` on their span, so `P^perp_S ⪯ M_S^{-2} ⪯ I`. The last
claim uses the independence of `w` and `X_S`. ∎

### 3.3 Proof of Theorem 3.2(a)

Write `S = S*`, `theta_n = sqrt(k/n) + 2 sqrt(log p / n)`. Under (A),
`theta_n <= (sqrt(C0) + 1)/sqrt(log p)`, `lam/n <= 1/log^2 p`, and
`p lam/n >= p/sqrt n >= sqrt p`, so `L_lam >= (1/2) log p`. All `o(1)` terms
below are bounded by explicit functions of `p` that tend to 0 under (A); we
indicate the rates.

*Step 0 (events).* Consider the events:

- E1: `(sqrt n - sqrt k - sqrt(2 log p))^2 <= s_- <= s_+ <= (sqrt n + sqrt k + sqrt(2 log p))^2` (G3);
- E2: `||w||^2 <= n + 2 sqrt(n log p) + 2 log p` and `||P^perp_S w||^2 >= n - k - 2 sqrt(n log p)` (G2);
- E3: `|v'M_S^{-1}w| <= ||v|| sqrt(2 log p)` (G1);
- E4: for all `i in S`: `q_i >= n - k - 2 sqrt(n log p)`,
  `q_i <= n + 2 sqrt(n log p) + 2 log p`, `|xi_i| <= 2 ||A_i y_(i)|| sqrt(log p)`
  (Lemma 3.6, G1, G2).

Given `(X_S, w)`, the null correlations `Z_l = a_l/||r||`, `l ∉ S`, are iid
`N(0,1)`, and `x_l = (a_l/||r||^2) r + x_l^perp` with `x_l^perp ~ N(0, P_{r⊥})`
independent of `a_l`. Let `tau` be the `(X_S, w)`-measurable threshold of Step
2, `V = {l ∉ S : |Z_l| > tau}`, `N_V = |V|`, `P` the orthogonal projection
onto `(col X_S + span r)^perp` (rank `n - k - 1` a.s.), and
`W = P X_V^perp`. Conditionally on `(X_S, w, (a_l)_l)`, the columns of
`X_V^perp` are iid `N(0, P_{r⊥})` and those of `W` are iid `N(0, P)`.

- E5: `sum_{l ∉ S}(|Z_l| - tau)_+^2 <= 4(p m(tau) + log p)` (G5);
- E6: `N_V <= 4 p Phibar(tau) + 3 log p` (G4);
- E7: `max_{l ∉ S}|Z_l| <= 2 sqrt(log p)` (G1);
- E8: `s_min(W) >= sqrt(n-k-1) - sqrt(N_V) - sqrt(2 log p)` and
  `||X_V^perp||_op <= sqrt n + sqrt(N_V) + sqrt(2 log p)` (G3);
- E9: `max_{l ∉ S ∪ V} |x_l^perp' Delta| <= 2 ||Delta|| sqrt(log p)`, where
  `Delta` is the witness perturbation of Step 4. Given
  `(X_S, w, (a_l), X_V)`, `Delta` is fixed and, for `l ∉ S ∪ V`,
  `x_l^perp' Delta ~ N(0, ||P_{r⊥}Delta||^2)`, so (G1) and a union bound over
  at most `p` indices apply.

The failure probability of E1–E9 is at most `(12 + 3k)/p -> 0`.

*Step 1 (residual and coefficients).* On E1–E4:

- By Lemma 3.7 and E1, `||v||^2 = (1 + O(theta_n)) k b^2 lam^2 n/(lam+n)^2`,
  because for `s in [n(1-theta)^2, n(1+theta)^2]` the ratio
  `(lam^2 s/(lam+s)^2)/(lam^2 n/(lam+n)^2)` lies in
  `[(1-theta)^2(1+theta)^{-4}, (1+theta)^2(1-theta)^{-4}]`. With E2, E3 and
  `2 sigma ||v|| sqrt(2 log p) <= sqrt(2 log p/n) (n sigma^2 + ||v||^2)`:
  `||r||^2 = (1 + O(theta_n)) omega_lam^2`.
- By Lemma 3.6 and E4, `q_i = n(1 + O(theta_n))`, so
  `b q_i/(lam+q_i) = b_lam (1 + O(theta_n lam/n)) = b_lam (1 + O(theta_n log^{-2} p))`, and,
  using `||A_i y_(i)|| <= ||v_i|| + sigma ||w||` with `||v_i||` bounded as in
  Lemma 3.7 (eigenvalue interlacing),
  `|xi_i|/(lam + q_i) <= b_lam * O( (sigma/b) sqrt(log p/n) + sqrt(k log p/n) lam/n )`.
  The last term is `O(log^{-2} p)` since `k log p <= C0 n`.

Hence `m0 >= lam b_lam (1 - eta_1)`, `lam max_i |beta^S_i| <= lam b_lam (1 + eta_1)`,
and `m0/||r|| >= tau_lam (1 - eta_2)`, where
`eta_1, eta_2 = O(theta_n + log^{-2} p) -> 0`.

*Step 2 (threshold).* Put `zeta = 1/log p`, `kappa = (1 - zeta) m0`, and
`tau = kappa/||r||`. Then `tau^2 >= (1-zeta)^2 (1-eta_2)^2 (2+eps) L_lam >= (2 + eps/2) L_lam`
for large `p`. By (G1), `phi(tau) <= e^{-(1+eps/4) L_lam}/sqrt(2 pi)`, so

```
Pi := 2 p phi(tau)/tau <= (2/(sqrt(2 pi) tau)) (n/lam) (n/(p lam))^{eps/4}
    <= sqrt(n) p^{-eps/8}.
```

*Step 3 (violators and `H_V`).* On E5–E8: `sum_l (|Z_l|-tau)_+^2 <= 4(Pi + log p)`,
`N_V <= 2 Pi + 3 log p = o(sqrt n)`, and
`s_min(H_V) >= s_min(W)^2 >= n(1 - o(1))`, because `M_S^{-1} ⪰ P` gives
`H_V ⪰ X_V'P X_V = W'W` (note `P X_V = P X_V^perp` since `P r = 0`).
Therefore the witness of Proposition 2.3 is defined and

```
Gamma <= ||a_V - kappa s||^2 / s_min(H_V) <= 4 ||r||^2 (Pi + log p) / (n (1 - o(1))).
```

*Step 4 (perturbation of correlations).* Let `Delta`, `alpha`, `c` be as in
Proposition 2.3 and `gamma_1 = sqrt(Gamma)/||r||`. Then
`gamma_1^2 = O((Pi + log p)/n) = O(n^{-1/2} + log^{-5} p)`, so
`gamma_1 = o(zeta)`.

- *Nulls.* For `l in V`, `|c_l| = kappa`. For `l ∉ S ∪ V`,
  `c_l = a_l (1 - r'Delta/||r||^2) - x_l^perp' Delta`, so by Lemma 2.1 and E9,
  `|c_l| <= kappa (1 + gamma_1) + 2 sqrt(Gamma log p)`. Since
  `m0 >= tau ||r||` and `tau^2 >= log p`,
  `2 sqrt(Gamma log p)/m0 <= 2 gamma_1`. Hence `M <= m0 (1 - zeta + 3 gamma_1)`.
- *True features.* For `i in S`, `c_i = lam beta^S_i - x_i'Delta` and
  `x_i'Delta = lam e_i'(lam + G)^{-1} X_S' X_V u`, so
  `max_i |x_i'Delta| <= lam (sqrt(s_+)/(lam + s_-)) ||X_V||_op ||u||`. Here
  `||u|| <= ||r|| sqrt(sum_l (|Z_l|-tau)_+^2) / s_min(H_V)` and
  `||X_V||_op <= ||a_V||/||r|| + ||X_V^perp||_op <= sqrt n (1 + o(1))` (by E7,
  `||a_V||^2 <= 4 N_V ||r||^2 log p = o(n ||r||^2)`). So
  `max_i |x_i'Delta| <= (1 + o(1)) 2 lam ||r|| sqrt(Pi + log p)/n`. Dividing
  by `m0 >= lam b_lam (1 - eta_1)` and using
  `||r|| <= (1+o(1)) omega_lam <= (1+o(1)) (sigma sqrt n + b sqrt k lam/sqrt n)`:

  ```
  eta_S := max_i |x_i'Delta| / m0
        = O( (sigma/b)(sqrt(log p/n) + sqrt(Pi/n)) + sqrt(k/n)(lam/n)(sqrt(log p) + sqrt Pi) ).
  ```

  Each term is `o(zeta)`: `sqrt(Pi/n) <= n^{-1/4} p^{-eps/16}`;
  `sqrt(k/n) sqrt(log p) lam/n <= sqrt(C0) log^{-2} p`; and, since
  `Pi <= (n/lam) p^{-eps/8}`,
  `sqrt(k/n)(lam/n) sqrt(Pi) <= sqrt(lam/n) p^{-eps/16} <= p^{-eps/16}`.
  So `m >= m0 (1 - eta_S)`.

*Step 5 (margin).* By Step 4, `M <= m` and
`m^2 - M^2 >= m0^2 [(1-eta_S)^2 - (1-zeta+3gamma_1)^2] >= zeta m0^2 (1 - o(1))`.
With `m0^2 >= tau^2 ||r||^2` and Step 3,

```
Gamma / ((m^2 - M^2)/lam) <= (1 + o(1)) 4 lam (Pi + log p) / (n zeta tau^2).
```

Here `zeta tau^2 >= (2 + eps/2) L_lam/log p >= 1`,
`lam Pi/n <= (2/(sqrt(2 pi) tau)) p^{-eps/8}`, and `lam log p/n <= 1/log p`.
So the ratio tends to 0, that is, `Gamma = o((m^2 - M^2)/lam)`. In Step 5 the
bracket is in fact `2 zeta - 2 eta_S - 6 gamma_1 - O(zeta^2) = (2 - o(1)) zeta`,
so `m^2 - M^2 >= (2 - o(1)) zeta m0^2`. By Proposition 2.3, every single wrong
fixing has bound at least
`f(S) + (1 - o(1))(m^2 - M^2)/lam >= f(S) + (2 - o(1)) zeta m0^2/lam`, and with
`m0 >= lam b_lam (1 - eta_1)` and `b_lam = b(1 - O(log^{-2} p))` this is at
least `f(S) + (2 - o(1)) lam b^2/log p >= f(S) + lam b^2/log p` for large
`p`. ∎

### 3.4 Proofs of Theorem 3.1, Theorem 3.2(b), and the sample-size forms

*Theorem 3.1(a).* On E1–E4, Step 1 gives `m0/||r|| >= tau_lam (1 - eta_2)`.
By (G1) and a union bound,
`P(max_{l ∉ S}|Z_l| > sqrt(2 log p + 2 log log p)) <= 1/log p`. Since
`tau_lam^2 (1-eta_2)^2 >= (2 + eps/2) log p > 2 log p + 2 log log p` for large
`p`, w.h.p. `M = max_{l ∉ S}|a_l| < m0`. Apply Lemma 2.2 with `alpha = r`:
`h(r,1_S) = f(S)`, so `R >= f(S)` and every single wrong fixing has bound
`>= f(S) + (m0^2 - M^2)/lam > f(S)`. Hence `R = OPT = f(S*)` and `S*` is the
unique optimum. ∎

*Theorem 3.1(b).* Lemma 3.6 and E4 give
`m0 <= lam |beta^S_{i0}| <= lam b_lam (1 + eta_1)` for any fixed `i0 in S`, and
Step 1 gives `||r|| >= omega_lam (1 - O(theta_n))`, so
`m0/||r|| <= tau_lam (1 + o(1)) <= sqrt((2 - eps) log p) (1 + o(1))`. Let
`t = sqrt((2 - eps/2) log p)`. Given `(X_S, w)`,
`P(max_{l ∉ S}|Z_l| <= t) = (1 - 2 Phibar(t))^{p-k} <= exp(-2(p-k) Phibar(t))`,
and by (G1) `2(p-k) Phibar(t) >= c p^{eps/4}/sqrt(log p) -> inf`. So w.h.p.
`max_{l ∉ S}|a_l| > t ||r|| > m0`, and Corollary 2.4 gives `R < f(S*)`. ∎

*Theorem 3.2(b).* Let `delta0 = eps/16`, `kappa = lam b_+ (1 + zeta)` with
`b_+ = max_{i in S}|beta^S_i|`, `tau' = kappa/||r||`, and
`t0 = (1 + delta0) tau'`. By Step 1 (upper bounds),
`tau' <= tau_lam (1 + o(1))`, so `t0^2 <= (2 - eps/2) L_lam` for large `p`.
Given `(X_S, w)`, the count `N_t0 = #{l ∉ S : |Z_l| >= t0}` is binomial with
mean `mu >= 2(p-k) phi(t0) t0/(1+t0^2) >= c (n/lam) (p lam/n)^{eps/4}/sqrt(log p)`.
Since `p lam/n >= sqrt p`, `mu/(n/lam) -> inf`. By (G4), w.h.p.
`N_t0 >= mu/2`. Let `N' = min(floor(mu/2), floor(n/log^2 p))`, let `V'` be
the `N'` null indices with the largest `|a_l|`, and fix any null `j ∉ V'`
(all nulls except at most `N' <= n/log^2 p`). Every `l in V'` has
`|Z_l| >= t0`, that is, `|a_l| - kappa >= delta0 kappa`, so
`Q >= N' delta0^2 kappa^2`.

Next, `L = ||X_{V'}||_op^2 <= (||a_{V'}||/||r|| + ||X_{V'}^perp||_op)^2 <= n(1 + o(1))`,
because `N' <= n/log^2 p` and `max_l |Z_l| <= 2 sqrt(log p)` w.h.p. So
`Q/L >= (1 - o(1)) N' delta0^2 lam^2 b_+^2 / n >= 3 lam b_+^2`, since
`N' >= 3(1 + o(1)) n/(delta0^2 lam)` (both for `N' = mu/2` and for
`N' = n/log^2 p`, the latter because `lam >= sqrt n >> log^2 p`).

Apply Lemma 2.5 with `s = 3 lam b_+^2 L/Q <= 1`. Then
`(2s - s^2)Q/L >= sQ/L = 3 lam b_+^2`. Also
`T = (lam/kappa)(s/L) sum_l e_l <= 3 lam^2 b_+^2 sum_l e_l/(kappa Q) <= 3/delta0`,
because `Q >= delta0 kappa sum_l e_l`. Each
`t_l <= 3 lam^2 b_+^2 e_l/(kappa Q) <= 3 lam^2 b_+^2 max_l e_l/(kappa N' delta0^2 kappa^2) -> 0`,
since `max_l e_l <= 2 ||r|| sqrt(log p)`,
`N' >= min(mu/2, n/log^2 p) - 1 >= min(mu/2, log^4 p) - 1 -> inf` (because
`n >= log^6 p`, and `mu/2 >= c (n/lam) p^{eps/8}/sqrt(log p) -> inf`),
and `tau'` is bounded below (`tau' >= (1 - o(1)) tau_lam` and
`tau_lam^2 >= (1 - o(1)) min(b^2/(2 sigma^2), log p/(2 C0))`, because
`lam >= sqrt n` and `k log p <= C0 n`).
Finally `(1+T)^2/(k-1-T) <= 1/2` when `k >= 5000/eps^2`, because
`T <= 3/delta0 = 48/eps` and `2(1 + 48/eps)^2 + 1 + 48/eps <= 4851/eps^2`. Lemma 2.5 gives
`r(∅,{j}) <= f(S) + (3/2) lam b_+^2 - 3 lam b_+^2 < f(S) - lam b_+^2`, and
`b_+ >= b_lam(1 - o(1))` gives the stated form. ∎

*Sample-size forms, Theorems 3.1(c) and 3.2(c).* For `lam <= n/log^2 p`,
`b_lam = b(1 - O(log^{-2} p))` and
`omega_lam^2 = (n sigma^2 + k b^2 lam^2/n)(1 + O(log^{-2} p))`. Writing
`lam^2 b^2 = T n sigma^2` gives

```
tau_lam^2 = (1 + O(log^{-2} p)) T n/(n + k T) < (1 + O(log^{-2} p)) n/k   for every lam.
```

Converses: if `n <= (2-eps) k log p` then
`tau_lam^2 <= (2 - eps/2) log p` for every `lam` in (A); if
`n <= (2-eps) k log(p/sqrt n)` then, since `L_lam >= log(p/sqrt n)` for
`lam >= sqrt n`, `tau_lam^2 <= (2 - eps/2) L_lam`. Achievability: let
`Lambda` be `log p` (root) or `log(p/sqrt n)` (C1), assume
`n >= (2+eps) k Lambda`, and put `T = (2 + eps/2)(1 + eps/8) Lambda/(1 - (2+eps/2)(1+eps/8) k Lambda/n)`.
The denominator is at least `c_eps > 0`, so `T = Theta_eps(log p)`,
`lam = (sigma/b) sqrt(T n)` lies in `[sqrt n, n/log^2 p]` for large `p` by
`n >= log^6 p`, `L_lam = log(p/sqrt n) + (1/2) log(T sigma^2/b^2) = (1 + o(1)) log(p/sqrt n)`,
and `tau_lam^2 >= (2 + eps/2) Lambda (1 + o(1))`. Replacing `eps` by a
smaller constant in the theorems gives the claims. ∎

### 3.5 What the easy side says

- C1 is exactly "root probing fixes every variable" (Atamtürk–Gómez safe
  screening in its strongest single-variable form). Theorem 3.2 says that the
  perspective relaxation certifies optimality through probing down to
  `n ≈ 2k log(p/sqrt n)`, which is below the root-exactness threshold
  `2k log p` by `k log n`. The root-exactness constant 2 coincides with
  Wainwright's sharp constant for Lasso sign recovery with standard Gaussian
  designs (`n > 2k log(p-k)`; recalled from memory, not re-read).
- The gain of C1 over root exactness comes from saturation: a null feature
  whose correlation exceeds the cap `kappa` costs the relaxation only
  about `(|a_l| - kappa)^2/n`, not `(a_l^2 - kappa^2)/lam`, and there are about
  `p exp(-tau^2/2)` such features, while forcing one feature in costs about
  `lam b^2 ≈ tau omega b`. Balancing gives `tau^2 ≈ 2 log(p lam/n)`.
- The theorems are first-order asymptotics with logarithmic error terms.
  Section 6 shows that at `p <= 1600` C1 holds at noticeably smaller `tau`
  than `2 log(p lam/n)`.

**Heuristic 3.8 (finite-size balance; not proved).** The primal side of the
argument suggests the prediction

```
C1 at S*   iff   m0^2/lam  >  sum_{l ∉ S*} (|a_l| - m0)_+^2 / n  +  max_{l ∉ S*} a_l^2/(n + lam).
```

The left side is the price of the budget unit that a forced-in feature takes
from `S*` (the true features' marginal value `lam beta_i^2`); the first term
on the right is the saturated gain that the relaxation already collects from
violators at the cap `m0` (this is the root gap to first order); the last
term is the gain of the forced feature itself. Replacing the sum by its mean
`(p-k) ||r||^2 Psi(m0/||r||)/n`, with `Psi(t) = E(|Z| - t)_+^2 ≈ 4 phi(t)/t^3`,
and `m0 = tau ||r||`, the balance becomes `p Psi(tau) ≈ tau^2 n/lam`, whose
solution is `tau^2 = 2 log(p lam/n) (1 + o(1))`, the threshold of
Theorem 3.2.

*Second order (heuristic).* Keeping the next terms,
`p · 4 phi(tau)/tau^3 = tau^2 n/lam` gives

```
tau^2 ≈ 2 log(p lam/n) + 2 log(4/sqrt(2 pi)) - 5 log tau^2 = 2 log(p lam/n) + 0.93 - 5 log tau^2     (C1).
```

For the saturated witness the cap is `kappa = (1 - zeta) m0`, the gap is
multiplied by about `e^{zeta tau^2}`, and the margin is `2 zeta m0^2/lam`;
optimizing gives `zeta tau^2 = 1` and

```
tau^2 ≈ 2 log(p lam/n) + 2 log(2e/sqrt(2 pi)) - 3 log tau^2 = 2 log(p lam/n) + 1.55 - 3 log tau^2     (witness).
```

(The same formulas are derived in the independent review.) With the `n` and
`lam` of Table 6.1 near the transitions they give about 3.3 (C1) and 5.0
(witness) at `p = 200`, and 5.0 and 7.7 at `p = 1600`. The observed 50%
points, read off Table 6.1's mean `tau^2`, are about 3.3 and 4.7 at
`p = 200` and 4.8 and 7.4 at `p = 1600`, whereas `2 log(p lam/n)` is 8.2 and
12.2. The `-5 log tau^2` term is why C1 appears at about half of the
first-order value at these sizes. The additive sum is meaningful only when the violators are few compared
with `n` (then their fits are nearly orthogonal); with hundreds of violators
in `R^n` it grossly overestimates the gap (at `lam = sqrt n`, `p = 3200`,
`n = 121` it gives 13.8–30.9 for seven seeds and 70.3 at seed 1007, while the
root gap is 2.9–5.7 and 9.9, respectively). Evaluated on the
realized `a_l` of each instance of Table 6.1, the prediction
agrees with the exact C1 outcome in 207 of 232 instances of Table 6.1
(with the exact decisions) and errs only on the conservative side near the
threshold
(`code/predict_c1.py`). The rigorous witness of Proposition 2.3 is weaker at
these sizes: it caps violators strictly below `m0`, and at `n <= 100` the
perturbation of the other correlations is not small (the asymptotic proof
controls it only as `p -> inf`).

## 4. Hard side: exponential conflict cliques in pure noise and at low SNR

### 4.1 Two lemmas

Let `q = k/n`, `d(q||rho) = q log(q/rho) + (1-q) log((1-q)/(1-rho))`, and for
`delta in (0,1)` let `rho*` be the root in `(q, 1)` of

```
(n/2) d(q || rho*) = log C(p,k) + log(1/delta).
```

(`d(q||.)` increases from 0 to `inf` on `(q,1)`, so the root exists.)

**Lemma 4.1 (first-moment lower bound on OPT).**

- (a) If `y` is independent of `X`, then with probability at least `1-delta`,
  every `T` with `|T| = k` has `||P_T^perp y||^2 >= (1-rho*) ||y||^2`, and
  hence `OPT >= (1-rho*) ||y||^2`.
- (b) If `y = X_{S*} beta*_{S*} + sigma w`, then with probability at least
  `1-delta`, `OPT >= (1-rho*) sigma^2 ||P^perp_{S*} w||^2`.

*Proof.* (a) Fix `T` and condition on `y`. The column span of `X_T` is a
uniformly random `k`-dimensional subspace, so `||P_T yhat||^2`
(`yhat = y/||y||`) has the law of `A/(A+C)` with independent
`A ~ chi^2_k`, `C ~ chi^2_{n-k}`. For `rho > q` and `theta > 0`,
`P(A/(A+C) >= rho) <= E exp(theta((1-rho)A - rho C))
= (1 - 2theta(1-rho))^{-k/2} (1 + 2theta rho)^{-(n-k)/2}`;
at `2theta(1-rho) = 1 - q/rho` this equals `exp(-(n/2) d(q||rho))`. A union
bound over the `C(p,k)` supports gives the first claim. Since the ridge
penalty is nonnegative and `f` does not increase when features are added,
`OPT >= min_{|T|=k} ||P_T^perp y||^2`.
(b) For `|T| = k`, let `A = S* \ T` and `v_T = X_A beta*_A + sigma w`. Then
`y - v_T` lies in the span of `X_T`, so `||P_T^perp y|| = ||P_T^perp v_T||`,
and `v_T` is independent of `X_T` because `T ∩ A = ∅`. The argument of (a)
gives `||P_T^perp v_T||^2 >= (1-rho*) ||v_T||^2` for all `T` simultaneously,
and `||v_T|| >= ||P^perp_{S*} v_T|| = sigma ||P^perp_{S*} w||`. ∎

**Lemma 4.2 (midpoints of top-correlated supports).** Let `N ⊆ [p]` be a set
of features such that `y` is independent of `X_N`, let
`c_j = x_j' yhat` (`j in N`), and let `X^perp = (I - yhat yhat') X`. For
supports `S, T ⊆ N` with union `U` and `s_U = ||c_U||^2 > 0`,

```
g((1_S+1_T)/2) <= ||y||^2 [ 1 - s_U/(s_U + ||X^perp_U c_U||^2/s_U + 2 lam) ].
```

*Proof.* By Lemma 1.5(a), `g((1_S+1_T)/2) <= ||y - t X_U c_U||^2 + 2 lam t^2 s_U`
for every `t`. Since `X_U = yhat c_U' + X_U^perp`,
`||y - t X_U c_U||^2 = ||y||^2 - 2t ||y|| s_U + t^2 (s_U^2 + ||X_U^perp c_U||^2)`.
Minimizing over `t` gives the bound. ∎

### 4.2 Statements

Let `x0 = 1.2564...` be the positive root of `e^{-x}(1+2x) = 1`.

**Theorem 4.3 (pure noise).** Let `y` be independent of `X` with `y != 0`
almost surely. Let `p -> inf` with `k -> inf`, `k/n -> 0`, `lam/n -> 0`
(`lam > 0`), and `x_p := (2/n) log C(p,k) -> x in (0, x0)`. Then there are
`c' = c'(x) > 0` and `eta = eta(x) > 0` such that, for every
`eps <= eta ||y||^2`, w.h.p. the conflict graph `G_eps` has a clique of size
at least `exp(c' k log(p/k)) = C(p,k)^{c'(1+o(1))}`, in particular of size
at least `exp(c k)` for every fixed `c`.
Consequently every convex-piece `eps`-certificate for the perspective
relaxation has at least `C(p,k)^{c'(1+o(1))}` leaves, and every such tree
with incumbent-based variable-bound reductions has at least
`C(p,k)^{c'(1+o(1))}/(2p+1)` nodes (Lemma 1.4).

*Size of `c'`.* The proof gives only a small constant. Maximizing `c'`
over the proof's parameters (`c' < (1-mu) theta` and condition (*) of
Step 2; `code/check_cprime.py`) gives 0.171, 0.161, 0.140, 0.106, 0.059,
0.022, 0.0068, 0.0020 and 0.0001 at `x = 10^-6, 10^-3, 0.01, 0.05, 0.2, 0.5,
0.8, 1.0, 1.2`. As `x -> 0`, (*) becomes `(1+mu)(1-theta) > 1`, and the
supremum of `(1-mu) theta` under it is `3 - 2 sqrt 2 ≈ 0.1716`, attained at
`mu = sqrt 2 - 1`, `theta = mu/(1+mu)`; the approach is slow because of the
`sqrt(c'x)` term in `B`. In the planted case of Theorem 4.4 at
`kappa_s = K(x)/2` the constant is 4.1–5.1 times smaller.

For `k = p^{gamma + o(1)}`, `gamma in (0,1)`, and `n = alpha k log p`, one has
`x = 2(1-gamma)/alpha`, so the hypothesis is `alpha > 2(1-gamma)/x0 ≈ 1.592 (1-gamma)`.

**Theorem 4.4 (planted model, low total SNR).** Let
`y = X_{S*} beta*_{S*} + sigma w` with `|S*| = k` and
`||beta*||^2/sigma^2 -> kappa_s`. Under the assumptions of Theorem 4.3 on
`(p, k, n, lam, x)`, if

```
kappa_s < e^{-x}(1 + 2x) - 1,
```

then the conclusion of Theorem 4.3 holds (with `eta ||y||^2` replaced by
`eta n sigma^2`), with a clique of supports disjoint from `S*`. The right
side is positive iff `x < x0`, with maximum `2e^{-1/2} - 1 ≈ 0.213` at
`x = 1/2`.

For `beta*_i = ±b` this is `k b^2/sigma^2 < K(x) := e^{-x}(1+2x) - 1`,
equivalently `b < sigma sqrt(2 log(p/k)/n) · sqrt(K(x)/x) (1 + o(1))`, with
`K(x)/x < 1`. (This factor is not always below the detection scale
`sigma sqrt(log p/n)`: for `k = p^gamma` and large `alpha` it tends to
`sqrt(2(1-gamma)) > 1` when `gamma < 1/2`.) The right characterization is
relative to the information-theoretic threshold: `kappa_s < K(x)` means
`log(1 + kappa_s) < log(1 + 2x) - x < x`, while `n < n_IT` (to first order)
means `log(1 + kappa_s) < x`. So the region of Theorem 4.4 lies strictly
inside the regime where exact recovery is information-theoretically
impossible; it covers the fraction `K(x)/(e^x - 1)` of that regime's range of
`kappa_s` at given `x` (0.82, 0.33, 0.06 at `x = 0.1, 0.5, 1`).

### 4.3 Proofs

*Proof of Theorem 4.3.* Let `delta = 1/k`.

*Step 1 (`OPT`).* As `q -> 0`, `d(q||rho) = -log(1-rho) + O(q log(1/q))`
uniformly for `rho` in compact subsets of `(0,1)`, and
`(2/n) log(1/delta) -> 0`. Hence `-log(1-rho*) -> x`, and by Lemma 4.1(a),
w.h.p. `OPT >= (e^{-x} - o(1)) ||y||^2`.

*Step 2 (parameters).* Since `e^{-x}(1+2x) > 1`, that is `2x > e^x - 1`,
continuity gives `mu in (0,1)`, `theta in (0,1)` and `c' in (0, (1-mu) theta)`
with

```
(*)   (1+mu)(1-theta) x / B  >  e^x - 1,        B := 1 + 2 sqrt(c'x) + 2 c'x.
```

Fix them, and put `M = ceil(k (p/k)^theta)`, `m = ceil(mu k)`, and
`eta_0 := e^{-x} - B/(B + (1+mu)(1-theta)x) > 0` (positive by (*)).

*Step 3 (top correlations).* Given `y`, the `c_j = x_j'yhat` are iid
`N(0,1)`. Let `t_M = Phibar^{-1}(M/p)`. The number of `j` with
`|c_j| >= t_M` is `Bin(p, 2M/p)`, so by (G4) it is at least `M` with
probability `>= 1 - e^{-M/4}`. Let `W` be the `M` indices with the largest
`|c_j|`; then `c_j^2 >= t_M^2` on `W`. Because `k/n -> 0` and `x_p -> x`,
`log(p/k) = x n/(2k) (1+o(1)) -> inf` and
`log C(p,k) = k log(p/k)(1 + O(1/log(p/k)))`. Since `p/M = (p/k)^{1-theta} -> inf`,
`t_M^2 = 2 log(p/M)(1+o(1)) = 2(1-theta) log(p/k)(1+o(1))`. Therefore every
`U ⊆ W` with `|U| >= k+m` has
`s_U >= (k+m) t_M^2 = (1+mu)(1-theta) x n (1+o(1))`.

*Step 4 (code).* Let `C` be the greedy (lexicographic) family of `k`-subsets
of `W` with pairwise `|S \ T| >= m`; it depends on the data only through `W`.
By the Gilbert–Varshamov argument,
`|C| >= C(M,k)/sum_{d<m} C(k,d) C(M-k,d)`. Here `C(M,k) >= (M/k)^k >= (p/k)^{theta k}`
and, since `C(k,d) <= 2^k` and `C(M-k,d) <= (eM/d)^d` increases in `d < m`,
`sum_{d<m} C(k,d) C(M-k,d) <= m 2^k (eM/m)^m`. With
`log(eM/m) <= theta log(p/k) + 1 + log(1/mu) + o(1)`,

```
log |C| >= (1 - mu) theta k log(p/k) - O(k) - O(log(p/k)) = (1-mu) theta k log(p/k) (1 - o(1)).
```

Let `C'` consist of the first `ceil(exp(c' k log(p/k)))` members of `C`; this
is possible for large `p` because `c' < (1-mu) theta`.

*Step 5 (cross terms).* Given `y` and `(c_j)`, the columns of `X^perp` are iid
`N(0, I - yhat yhat')` and independent of `(c_j)`, hence of `W` and `C'`. For
a fixed `U`, `X^perp_U c_U ~ N(0, s_U (I - yhat yhat'))`, so
`||X_U^perp c_U||^2/s_U ~ chi^2_{n-1}`. By (G2) and a union bound over the at
most `|C'|^2` pairs, with `t = log(|C'|^2/delta) = 2c'k log(p/k)(1+o(1)) + log k = c'x n (1+o(1))`,
all pairs satisfy

```
||X_U^perp c_U||^2/s_U <= n + 2 sqrt(nt) + 2t = n B (1 + o(1)).
```

*Step 6 (conflicts).* For distinct `S, T in C'`, `|S ∪ T| >= k+m`, and the
bound of Lemma 4.2 decreases as `s_U` grows, so, using `lam = o(n)`,

```
g((1_S+1_T)/2) <= ||y||^2 [ B/(B + (1+mu)(1-theta)x) + o(1) ]
              = ||y||^2 [ e^{-x} - eta_0 + o(1) ] <= OPT - (eta_0 - o(1)) ||y||^2.
```

With `eta = eta_0/2`, every pair in `C'` is an edge of `G_eps` w.h.p., and
`|C'| >= exp(c' k log(p/k)) = C(p,k)^{c'(1+o(1))}`. The failure probability is
at most `2 delta + e^{-M/4} + o(1)`. ∎

(For fixed `R = M/k` instead of `R = (p/k)^theta`, the same steps give a
clique of size `exp(k e(mu,R)(1 - o(1)))` (with fixed `R`, `t = O(k) = o(n)`,
so `B -> 1` and the whole code can be used) with
`e(mu,R) = R H(1/R) - H(mu) - (R-1) H(mu/(R-1)) > 0` for `mu < (R-1)/R`,
`H` the binary entropy in nats; this was the form in the first version of
this note. The strengthening to `C(p,k)^{c'}` was suggested by the
independent review and is proved above.)

*Proof of Theorem 4.4.* Apply Steps 2–6 to `N = [p] \ S*`: conditionally on
`(X_{S*}, w)`, `y` is fixed and `X_N` is independent of it. The number of
candidates is `p - k = p(1-o(1))`. By Lemma 4.1(b) and (G2), w.h.p.
`OPT >= (e^{-x} - o(1)) n sigma^2`. Also
`||y||^2 = ||X_{S*}beta*||^2 + 2 sigma w'X_{S*}beta* + sigma^2 ||w||^2 = n(sigma^2 + ||beta*||^2)(1+o(1))`,
because `X_{S*}beta* ~ N(0, ||beta*||^2 I_n)`. Step 6 now gives
`g(midpoint) <= n sigma^2 (1 + kappa_s) B/(B + (1+mu)(1-theta)x) (1+o(1))`, which
is below `OPT - eta n sigma^2` once
`(1+kappa_s) < e^{-x}(1 + (1+mu)(1-theta)x/B)`; since
`kappa_s < e^{-x}(1+2x) - 1`, this holds for `mu` close to 1 and `theta`, `c'`
small. ∎

### 4.4 The proof is asymptotic only

The finite-`p` version of the argument (in its fixed-`R` variant, see the
remark after the proof of Theorem 4.3) certifies a clique when

```
(k+m) t_M^2 / ((k+m) t_M^2 + nu^2 + 2 lam) > rho*,      nu^2 = (n-1) + 2 sqrt((n-1) t) + 2 t,
```

with `t = 2 log|C'| + log(1/delta)`. We evaluated this condition, optimizing
over `R`, `mu`, and `|C'|` (`code/hard.py`, `theorem_condition2`), for
`(p,k) = (2000,20), (10^4,30), (10^5,50), (10^6,100), (10^8,300),
(10^12,1000)`, `alpha in {2,4,8,16}`, `lam = sqrt(n log p)`,
`delta = 0.05`. On this grid it fails at every point with `p <= 10^8`, and
first gives a nontrivial clique (`log |C'| ≈ 30` and `88`) at `p = 10^12`,
`alpha in {8, 16}`. The grid matters: allowing `alpha` up to 4096, a single
conflicting pair is certified already at `p = 10^{5.5}` (`lam = 0`) or
`p = 10^6` (`lam = sqrt(n log p)`), with `k = 2`, `alpha = 2048` and
`n ≈ 5 × 10^4` (`code/check_hard_revision.py`; a single pair needs no
Gilbert–Varshamov bound, and with `M = 2k` the recheck certifies a pair
already at `p = 10^5`, `lam = 0`; at such small `M` the failure probability
`e^{-M/4}` of Step 3 is not small and is not included in "certified"); the
independent review reports a certified clique `>= e^10` at `p = 10^9`, with
`n` in the millions.
Either way the proof is vacuous at practical sizes. The losses are second
order: `t_M^2` falls short of `2 log(ep/k)` by about
`log log(p/M) + log(4 pi) + 2 + 2 log R` (with `log(4 pi) ≈ 2.53`), and the
union bound over all `C(p,k)` supports charges `log(ep/k)` per feature. So Theorems 4.3 and
4.4 establish the existence of the hard regime, not its location at practical
sizes. Section 6 gives direct evidence at small sizes.

The mechanism is the one in Theorem 3 of the scout report (correlated pairs),
now produced by randomness: the perspective relaxation prices `k` features at
weight 1 and `k+m` features at weight about 1/2 the same, so whenever no
support explains much more than a random one, midpoints of far-apart good
supports undercut `OPT`. In pure noise the proof works best for large `alpha`
(`x -> 0`), where the best supports explain about
`(1 - e^{-x}) ||y||^2 ≈ x ||y||^2` and a union of `k+m` top features explains
about `(1+mu) x ||y||^2`. The clique members themselves need not be
near-optimal: only their unions, at weight 1/2, undercut `OPT`.

## 5. Between the thresholds: what is and is not explained

Fix the SNR `b/sigma`, let `k = p^{gamma+o(1)}` and `n = alpha k log p`. The
regimes are:

- `alpha > 2`: the root is exact for a suitable `lam` (Theorem 3.1).
- `2 - gamma < alpha < 2`: for every `lam` in (A) the root is not exact;
  for a suitable `lam` every variable-branching tree has at most `2p+1`
  nodes, with the incumbent `OPT` available or best-bound search
  (Theorem 3.2, Corollary 3.3).
- `alpha < 2 - gamma`: for every `lam` in (A), C1 fails at `S*`
  (Theorem 3.2(b), for `k >= 5000/eps^2`).

The hard side concerns a different scaling, with bounded total SNR (so the
per-coefficient SNR `b/sigma -> 0`): in pure noise, or with
`||beta*||^2/sigma^2 < e^{-x}(1+2x) - 1`, where
`x = lim 2 log C(p,k)/n < x0` (for `k = p^gamma`: `alpha > 1.59(1-gamma)`),
`lam = o(n)`, `k -> inf` and `k/n -> 0`, every convex-piece certificate
needs `C(p,k)^{c'}` leaves (Theorems 4.3–4.4), asymptotically, with a small
`c'` (Section 4.2). At fixed
`b/sigma` the total SNR `k b^2/sigma^2 -> inf`, so these theorems never apply
there.

At fixed `b/sigma`, the information-theoretic threshold
`n_IT = 2k log(p/k)/log(1 + k b^2/sigma^2)` satisfies
`n_IT/(k log p) ≈ 2(1-gamma)/(gamma log p) -> 0`. In the `alpha`
parametrization the conjectured intrinsically hard region (Conjecture 5.2)
therefore shrinks to `alpha -> 0`, and almost all of `(0, 2 - gamma)` falls
under Question 5.1 below.

Below `2 - gamma` the theorems do not give a lower bound on tree size, and
Lemma 1.3 explains why no relaxation-intrinsic lower bound can: if the removal
half of C1 holds at an optimal `S*`, a `(2k+1)`-node certificate exists.

*Heuristic (not proved).* Removing a true feature costs the relaxation about
`n b^2`. If the ridge is large compared with `sqrt n`, replacing `x_i` by many
fractional null features costs more than it gains, and the removal half should
survive below the C1 threshold. If this held asymptotically, there would be a
window between the information-theoretic threshold and `2k log(p/sqrt n)`
where a `(2k+1)`-node certificate exists but most-fractional branching might
still build large trees, because a node that forces violators in becomes
prunable only after about `K = G/(lam b^2)` of them are forced in (`G` the
root gap). We have not derived a quantitative version of either statement.

**Question 5.1.** Is there such a rule-dependent window? The computations do
not support it at the sizes we can solve: at `p <= 200`, `k <= 8`, the
removal half fails whenever C1 fails, and most-fractional and largest-`z`
branching give trees of similar size (Table 6.6). At `n = 42`, `p = 200`,
`k = 8` the removal-node relaxation moves 2–3.5 units of budget from the
other true features onto 12–16 null features, so the large-ridge regime of
the heuristic is not reached.

**Conjecture 5.2 (hard regime at fixed SNR).** Fix `b/sigma > 0`,
`gamma in (0, 2/3)` and `delta > 0`. Let `k = p^{gamma+o(1)}`, let `n` satisfy
`(1+delta) k <= n <= (1-delta) n_IT`, with
`delta < (2 - 3 gamma)/(2 - gamma)` so that this range is nonempty for large
`p` (since `n_IT/k -> 2(1-gamma)/gamma`, slowly: 1.54, 1.74, 1.86 at
`p = 10^4, 10^8, 10^16` for `gamma = 1/2`, `b/sigma = 2`, per the recheck),
let `1 <= lam <= n^{1-delta}`, and let
`eps = 0`. Then w.h.p. the conflict graph `G_0` has a clique of size
`exp(c k)` for some `c = c(b/sigma, gamma, delta) > 0`, so every exact
convex-piece certificate has at least that many leaves.

*What is missing.* The Section 4 method does not reach this regime, for
three reasons.

- At fixed SNR, `n <= n_IT` means `x = 2 log C(p,k)/n >= (1 - o(1)) log(1 + k b^2/sigma^2) -> inf`,
  and `k/n >= k/n_IT -> gamma/(2(1-gamma)) > 0`. Section 4 uses both
  `q = k/n -> 0` and `x < x0` essentially, and even the pure-noise case with
  `x >= x0` is open (Section 8).
- Lemma 4.1 still bounds `OPT` from below (it holds for every `beta*`), but
  at fixed SNR the relevant supports must nearly match `f(S*)`, explaining a
  fraction `1 - O(1/(k b^2/sigma^2))` of `||y||^2`. The marginal
  construction of Section 4 explains only about
  `(1+mu)x/(1+(1+mu)x)` for unions. One would need a second-moment count of
  supports `T` with `f(T) <= f(S*) + Delta` and of pairs with small overlap,
  in the style of the Gamarnik–Zadik landscape analysis (which counts
  binary-coefficient vectors, not least-squares fits).
- For near-optimal supports with large overlap, the natural conflict
  criterion is Lemma 1.5(b), not (a), which charges `2 lam` on the overlap.
  Using (b) needs a lower bound on `||X(beta^S - beta^T)||^2` uniform over
  the packing, and uniform restricted-eigenvalue bounds for `2k`-sparse
  vectors are not available when `n < 2k log(p/k)`.

**Where the empirical transition sits.** In the scout's runs
(`lam = sqrt n`, `b/sigma = 2`, `p = 6k`, `k <= 20`) the large trees appear
near `alpha ≈ 0.5`, where the L0 optimum is not `S*` (recovery in 0 of 8
runs at `alpha = 0.5` for every tested `k`, and in most runs from
`alpha = 0.7–0.9`), and C1 appears near `alpha ≈ 1.1–1.4`. (The first-order
formula for `n_IT` gives `alpha_IT ≈ 0.2` at these sizes, so lower-order
terms matter here too.) For a tuned ridge, the theory above suggests reading
the empirical transition as two transitions: a rule-independent one at the
C1 threshold `2k log(p/sqrt n)`, above which every variable-branching tree is
linear (with the incumbent qualifier of Lemma 1.2), and a relaxation-intrinsic
one near the information-theoretic threshold, below which (conjecturally)
every convex-piece tree is exponential. With `lam = sqrt n` itself there is
no C1 threshold in the limit (Corollary 3.4), although at the scout's sizes
C1 still appears (Section 6.3). What happens between the two transitions is
Question 5.1.

## 6. Computations

*Setup.* Unless stated otherwise, `b = 1`, `sigma = 0.5` (per-entry SNR 2),
`n = round(alpha k log p)`, and the scaled ridge is
`lam = 1.5 sigma sqrt(2 n log p)/b` ("`tau0 = 1.5`"). Node relaxations are
solved by Clarabel; every pruning decision uses the certified dual bound of
Lemma 1.1. C1 is decided exactly at `S*`: a node passes if some dual vector
certifies a bound `>= f(S*)(1 + 1e-9)`, and C1 fails if some node's primal
(restricted) value is below `f(S*)(1 - 1e-7)`; if all `p` single fixings
pass, C1 holds and `S*` is the unique optimum. In the first runs, nodes the
saturated witness of Proposition 2.3 could not certify were solved in order
of the witness bound, and at `p >= 800` (and in one sweep at `p = 400`) at
most 40 were solved; 31 runs whose 40 solved nodes all passed were recorded
as "capped". That ordering is ineffective: the witness gives every violator
the same correlation `kappa`, hence the same bound (521 tied nodes in one run
at `p = 3200`), so the 40 nodes were effectively chosen by index. After the
independent review found this, all 31 capped runs were re-decided exactly
(`code/redecide_c1.py`, function `decide_c1_exact`): lower bounds come from a
pool of dual vectors (the residual `r_{S*}`, saturated witnesses, the root
residual, and the residual of every node solved so far), evaluated on all
`p` single fixings at once; the weakest undecided node is solved by column
generation and its residual joins the pool. At most 109 node solves and
180 s per run were needed. 30 of the 31 runs satisfy C1 and one fails
(`p = 3200`, Section 6.3); the tables report these exact decisions, in
agreement with the review's independent re-decision. "PWE root cert." counts runs with
`max_{l ∉ S*}|a_l| <= m0`, which certifies root exactness. B&B is best-first
with certified pruning. Cliques are greedy cliques in a pool of near-optimal
supports (B&B candidates and one-swap neighbours of the 20 best; the 300 best
are used), with every edge checked by the exact midpoint formula against the
exact `OPT` of the completed B&B. So each reported clique is a valid lower
bound on the number of leaves of every convex-piece certificate for that
instance (Lemma 1.4). Commands are in the appendix.

### 6.1 C1 versus root exactness with a scaled ridge

Table 6.1 (`k = 8`, `tau0 = 1.5`, 8 seeds).

| `p` | `k` | `lam` rule | `n` | `alpha` | runs | PWE root cert. | witness | C1 (exact) | mean `tau^2` | `2 log(p lam/n)` | `2 log p` | mean root gap |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 8 | tau0=1.5 | 37 | 1.00 | 8 | 0 | 0 | 4 | 2.26 | 7.24 | 9.21 | 2.833 |
| 100 | 8 | tau0=1.5 | 46 | 1.25 | 8 | 0 | 0 | 5 | 2.22 | 7.03 | 9.21 | 1.922 |
| 100 | 8 | tau0=1.5 | 55 | 1.49 | 8 | 0 | 1 | 8 | 3.52 | 6.85 | 9.21 | 0.706 |
| 100 | 8 | tau0=1.5 | 64 | 1.74 | 8 | 0 | 4 | 8 | 3.49 | 6.70 | 9.21 | 0.530 |
| 100 | 8 | tau0=1.5 | 74 | 2.01 | 8 | 0 | 3 | 8 | 3.51 | 6.55 | 9.21 | 0.746 |
| 100 | 8 | tau0=1.5 | 92 | 2.50 | 8 | 2 | 8 | 8 | 5.21 | 6.33 | 9.21 | 0.164 |
| 100 | 8 | tau0=1.5 | 111 | 3.01 | 8 | 1 | 8 | 8 | 5.67 | 6.15 | 9.21 | 0.135 |
| 200 | 8 | tau0=1.5 | 53 | 1.25 | 8 | 0 | 0 | 6 | 3.32 | 8.41 | 10.60 | 1.891 |
| 200 | 8 | tau0=1.5 | 64 | 1.51 | 8 | 0 | 1 | 8 | 3.50 | 8.22 | 10.60 | 1.465 |
| 200 | 8 | tau0=1.5 | 74 | 1.75 | 8 | 0 | 2 | 8 | 3.93 | 8.08 | 10.60 | 1.148 |
| 200 | 8 | tau0=1.5 | 85 | 2.01 | 8 | 0 | 4 | 8 | 4.64 | 7.94 | 10.60 | 0.421 |
| 200 | 8 | tau0=1.5 | 106 | 2.50 | 8 | 1 | 8 | 8 | 6.11 | 7.72 | 10.60 | 0.244 |
| 200 | 8 | tau0=1.5 | 127 | 3.00 | 8 | 2 | 8 | 8 | 6.27 | 7.54 | 10.60 | 0.101 |
| 200 | 8 | tau0=1.5 | 148 | 3.49 | 8 | 4 | 8 | 8 | 7.49 | 7.38 | 10.60 | 0.036 |
| 200 | 8 | tau0=1.5 | 170 | 4.01 | 8 | 2 | 8 | 8 | 8.46 | 7.25 | 10.60 | 0.016 |
| 400 | 8 | tau0=1.5 | 48 | 1.00 | 8 | 0 | 0 | 2 | 3.14 | 10.02 | 11.98 | 6.576 |
| 400 | 8 | tau0=1.5 | 60 | 1.25 | 8 | 0 | 1 | 6 | 3.62 | 9.80 | 11.98 | 2.762 |
| 400 | 8 | tau0=1.5 | 72 | 1.50 | 8 | 0 | 0 | 6 | 3.78 | 9.61 | 11.98 | 2.808 |
| 400 | 8 | tau0=1.5 | 84 | 1.75 | 8 | 0 | 1 | 8 | 4.87 | 9.46 | 11.98 | 1.098 |
| 400 | 8 | tau0=1.5 | 96 | 2.00 | 8 | 1 | 3 | 8 | 5.54 | 9.33 | 11.98 | 0.735 |
| 400 | 8 | tau0=1.5 | 120 | 2.50 | 8 | 0 | 8 | 8 | 6.40 | 9.10 | 11.98 | 0.174 |
| 400 | 8 | tau0=1.5 | 144 | 3.00 | 8 | 2 | 8 | 8 | 7.46 | 8.92 | 11.98 | 0.112 |
| 1600 | 8 | tau0=1.5 | 59 | 1.00 | 8 | 0 | 0 | 0 | 2.84 | 12.79 | 14.76 | 16.235 |
| 1600 | 8 | tau0=1.5 | 74 | 1.25 | 8 | 0 | 0 | 2 | 4.29 | 12.57 | 14.76 | 6.575 |
| 1600 | 8 | tau0=1.5 | 89 | 1.51 | 8 | 0 | 0 | 7 | 5.39 | 12.38 | 14.76 | 3.276 |
| 1600 | 8 | tau0=1.5 | 103 | 1.75 | 8 | 0 | 0 | 8 | 6.05 | 12.24 | 14.76 | 1.512 |
| 1600 | 8 | tau0=1.5 | 118 | 2.00 | 8 | 0 | 2 | 8 | 6.79 | 12.10 | 14.76 | 0.638 |
| 1600 | 8 | tau0=1.5 | 148 | 2.51 | 8 | 0 | 6 | 8 | 8.13 | 11.87 | 14.76 | 0.531 |
| 1600 | 8 | tau0=1.5 | 177 | 3.00 | 8 | 0 | 8 | 8 | 9.80 | 11.70 | 14.76 | 0.209 |

- The PWE certificate, hence root exactness, holds in at most 4 of 8 runs
  in any cell, and in at most 1 of 8 for `alpha <= 2`. The root gap is
  positive in every run without the certificate.
- C1 holds in every run from `alpha ≈ 1.5` at `p = 100, 200`, from
  `alpha ≈ 1.75` at `p = 400`, and from `alpha = 1.75` at `p = 1600` (7 of 8
  at `alpha = 1.5`).
  Linear trees for every variable-branching rule (with the incumbent `OPT`
  available or best-bound search, Lemma 1.2) are therefore certified in a
  range where the root relaxation is not exact, the phenomenon of
  Theorem 3.2 and Corollary 3.3.
- At fixed `k = 8`, the empirical C1 threshold moves up with `p`. This is
  consistent with the heuristic direction (for fixed `k`,
  `gamma = log k/log p -> 0` and the threshold moves toward `alpha = 2`), but
  it is not a prediction of the theorems: fixed `k` gives `n = O(log p)`,
  outside (A).
  At these sizes C1 appears at `tau^2 ≈ 3.5–5`, about half of
  `2 log(p lam/n)`, so the first-order constant is not yet visible.
  Solving `tau_lam^2 = 2 log(p lam/n)` and `tau_lam^2 = 2 log p` with the
  exact `b_lam, omega_lam` for this ridge rule gives first-order thresholds
  `alpha ≈ 2.6, 2.8, 2.9, 3.2` (C1) and `alpha ≈ 5.1` (root) for
  `p = 100, 200, 400, 1600`. The observed C1 thresholds are well below the
  first-order ones, and root certificates appear earlier than `alpha = 5.1`
  (at most 4 of 8 runs).
- The saturated witness certifies C1 by itself in every run with
  `alpha >= 2.5` at `p <= 400`, in 14 of 16 such runs at `p = 1600`, and
  rarely below `alpha = 2`.
- The scout's data (`lam = sqrt n`, `p = 6k`, `k <= 20`,
  `../../scouting/bb-tree-size-convex/sparse_single.jsonl`) show the same
  phenomenon: in all 124 runs where C1 held, B&B started with the incumbent
  `S*` still used 5 to 55 nodes, so the root relaxation was never exact
  there.

### 6.2 Sparsity `k ≈ sqrt p`

Table 6.2 (`p = 400`, `k = 20`, `tau0 = 1.5`, 6 seeds).

| `p` | `k` | `lam` rule | `n` | `alpha` | runs | PWE root cert. | witness | C1 (exact) | mean `tau^2` | `2 log(p lam/n)` | `2 log p` | mean root gap |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | 20 | tau0=1.5 | 120 | 1.00 | 6 | 0 | 0 | 2 | 2.24 | 9.10 | 11.98 | 12.798 |
| 400 | 20 | tau0=1.5 | 150 | 1.25 | 6 | 0 | 0 | 5 | 3.31 | 8.88 | 11.98 | 5.408 |
| 400 | 20 | tau0=1.5 | 180 | 1.50 | 6 | 0 | 0 | 6 | 3.91 | 8.70 | 11.98 | 2.318 |
| 400 | 20 | tau0=1.5 | 210 | 1.75 | 6 | 0 | 3 | 6 | 5.06 | 8.54 | 11.98 | 1.082 |
| 400 | 20 | tau0=1.5 | 240 | 2.00 | 6 | 0 | 6 | 6 | 6.00 | 8.41 | 11.98 | 0.294 |
| 400 | 20 | tau0=1.5 | 300 | 2.50 | 6 | 1 | 6 | 6 | 7.04 | 8.19 | 11.98 | 0.091 |

Here `gamma = log 20/log 400 = 0.5`, and the rows `alpha <= 1.5` were
rerun with exact checks of all single fixings (no cap). C1 holds in every run
from `alpha = 1.5`, in 5 of 6 at `alpha = 1.25` and in 2 of 6 at
`alpha = 1`, while the root certificate appears once (at `alpha = 2.5`). The first-order predictions
for this ridge rule are `alpha ≈ 2.3` (C1) and 4.4 (root); the optimal-ridge
C1 threshold of Corollary 3.3 is `2 - gamma = 1.5`.

### 6.3 The fixed ridge `lam = sqrt n` as `p` grows

Table 6.3 (`lam = sqrt n`, `k = 5`, `alpha = 3`, 8 seeds).

| `p` | `k` | `lam` rule | `n` | `alpha` | runs | PWE root cert. | witness | C1 (exact) | mean `tau^2` | `2 log(p lam/n)` | `2 log p` | mean root gap |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 5 | sqrt n | 59 | 3.02 | 8 | 0 | 3 | 8 | 2.01 | 3.75 | 7.82 | 0.689 |
| 200 | 5 | sqrt n | 79 | 2.98 | 8 | 0 | 0 | 8 | 2.37 | 6.23 | 10.60 | 1.315 |
| 800 | 5 | sqrt n | 100 | 2.99 | 8 | 0 | 0 | 8 | 2.60 | 8.76 | 13.37 | 2.903 |
| 3200 | 5 | sqrt n | 121 | 3.00 | 8 | 0 | 0 | 7 | 2.78 | 11.35 | 16.14 | 5.381 |

The first version of this note reported all eight `p = 3200` runs as
"capped" and read them as C1. The exact re-decision shows that C1 fails in
one run (seed 1007), and a first explanation given in the revision ("a
single unusually strong null feature") was also wrong, as the recheck
[`../../reviews/sparse-recheck.md`](../../reviews/sparse-recheck.md) found.
The facts, re-checked here (`code/check_s1007.py`, column generation to
convergence, primal and dual values agreeing to about `1e-6`):

- Seed 1007 has the lowest realized `tau^2` (1.96), the most violators (521,
  against 203–326 in the other seven runs) and the largest root gap (9.9,
  against 2.9–5.7).
- Every forced-in node we solved (nulls of ranks 1–60, 100, 500, the median
  and the weakest by `|a_j|`) is within 2.75 of `f(S*) = 82.700`; at seed
  1000 the same ranks give margins 5.87–8.70. Over all 3195 forced-in nodes,
  solved in the closing audit
  ([`../../reviews/closing-audit-b.md`](../../reviews/closing-audit-b.md)),
  the largest margin is 2.79 (rank 2816), and the relaxation recovers at
  least 61.0% of the budget price for every forced-in null. The budget price is
  `m0^2/lam = 7.16` at seed 1007 (8.94 at seed 1000). Even forcing in the
  weakest null, whose own fit is 0, costs only 2.75, so the relaxation
  recovers about 4.4 (about 60%) of the price by spreading the freed budget
  over the violators; at seed 1000 it recovers 0.24.
- Four of the solved forced-in nodes fail: nulls of ranks 1, 5, 6 and 50 by
  `|a_j|` (`j = 991, 1453, 2714, 2119`; node values below `f(S*)` by 2.414,
  0.454, 0.124 and 0.023). The rank-2 null passes by only 0.024. The
  recheck, which solved all 504 nodes its dual pool could not certify, found
  exactly these four failures. Ranks 5, 6 and 50 are ordinary nulls
  (`|a_j|/||r|| = 3.21, 3.20, 2.49`); the strongest (`|a_j| = 4.76 ||r||`,
  own fit `a_j^2/(n+lam) = 6.89`) fails by the most.

So the failure is the finite-size form of the many-violator balance of
Heuristic 3.8, including its own-fit term. It is not yet the asymptotic
regime of Corollary 3.4, where the violators alone outweigh the price for
almost every null. The other seven runs satisfy C1; direct solves at seeds
1000 and 1003 (root gaps 5.68 and 2.92; forced-in nodes of the strongest, a
median and the weakest null exceed `f(S*)` by 5.99, 8.47, 8.70 and 6.84,
9.22, 9.26) show the typical margins. The mean root gap grows with `p`
(0.7, 1.3, 2.9, 5.4 for `p = 50, 200, 800, 3200`), while the realized budget
price `m0^2/lam` at `p = 3200` is 7.2–8.9 (nominal `lam b^2 = sqrt n ≈ 11`),
so failures in more runs at larger `p` are plausible.

### 6.4 Pure noise versus planted signal on the same designs

Here `p = 10k`, `lam = 0.75 sqrt(2 n log p)`, 4 seeds; `b = 0` is pure noise
and `b = 1` is the planted model with the same `X` and `S*` (the noise `w`
differs, because the generator draws the signs of `beta*` only when `b > 0`).
Node cap 30000 (40000 for `k >= 9`).

Table 6.4.

| signal `b` | `alpha` | `k` | `p` | `n` | runs (done) | nodes, geo. mean [min, max] | certified clique, median [min, max] |
|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 1 | 3 | 30 | 10 | 4 (4) | 14 [11, 19] | 3.5 [3, 4] |
| 0 | 1 | 4 | 40 | 15 | 4 (4) | 26 [15, 39] | 5.0 [3, 8] |
| 0 | 1 | 5 | 50 | 20 | 4 (4) | 34 [17, 79] | 6.0 [4, 10] |
| 0 | 1 | 6 | 60 | 25 | 4 (4) | 126 [67, 269] | 14.0 [10, 24] |
| 0 | 1 | 7 | 70 | 30 | 4 (4) | 161 [73, 291] | 12.5 [9, 24] |
| 0 | 1 | 8 | 80 | 35 | 4 (4) | 869 [213, 2389] | 44.0 [19, 59] |
| 0 | 1 | 9 | 90 | 40 | 4 (4) | 1320 [303, 3377] | 37.5 [24, 79] |
| 0 | 1 | 10 | 100 | 46 | 4 (4) | 804 [227, 1563] | 33.0 [9, 34] |
| 0 | 2 | 3 | 30 | 20 | 4 (4) | 22 [17, 29] | 6.0 [5, 8] |
| 0 | 2 | 4 | 40 | 30 | 4 (4) | 44 [19, 73] | 9.0 [5, 12] |
| 0 | 2 | 5 | 50 | 39 | 4 (4) | 177 [89, 355] | 21.0 [10, 33] |
| 0 | 2 | 6 | 60 | 49 | 4 (4) | 198 [75, 473] | 21.0 [10, 34] |
| 0 | 2 | 7 | 70 | 59 | 4 (4) | 558 [419, 801] | 26.5 [23, 46] |
| 0 | 2 | 8 | 80 | 70 | 4 (4) | 4358 [1325, 9335] | 74.0 [31, 90] |
| 0 | 4 | 3 | 30 | 41 | 4 (4) | 26 [21, 29] | 6.0 [5, 9] |
| 0 | 4 | 4 | 40 | 59 | 4 (4) | 56 [49, 65] | 10.0 [7, 11] |
| 0 | 4 | 5 | 50 | 78 | 4 (4) | 325 [111, 803] | 29.0 [9, 45] |
| 0 | 4 | 6 | 60 | 98 | 4 (4) | 1202 [703, 1707] | 35.5 [31, 78] |
| 0 | 4 | 7 | 70 | 119 | 4 (4) | 1212 [661, 5537] | 25.5 [19, 67] |
| 0 | 4 | 8 | 80 | 140 | 4 (3) | 13102 [3517, 30001] | 112.0 [29, 195] |
| 1 | 1 | 3 | 30 | 10 | 4 (4) | 9 [3, 13] | 1.5 [1, 4] |
| 1 | 1 | 4 | 40 | 15 | 4 (4) | 20 [9, 51] | 4.5 [2, 8] |
| 1 | 1 | 5 | 50 | 20 | 4 (4) | 31 [17, 69] | 5.5 [4, 10] |
| 1 | 1 | 6 | 60 | 25 | 4 (4) | 15 [3, 31] | 4.0 [1, 5] |
| 1 | 1 | 7 | 70 | 30 | 4 (4) | 27 [13, 57] | 4.0 [1, 6] |
| 1 | 1 | 8 | 80 | 35 | 4 (4) | 28 [19, 63] | 2.0 [2, 7] |
| 1 | 2 | 3 | 30 | 20 | 4 (4) | 3 [1, 7] | 1.5 [1, 2] |
| 1 | 2 | 4 | 40 | 30 | 4 (4) | 5 [1, 11] | 1.0 [1, 2] |
| 1 | 2 | 5 | 50 | 39 | 4 (4) | 10 [7, 13] | 1.0 [1, 2] |
| 1 | 2 | 6 | 60 | 49 | 4 (4) | 6 [1, 13] | 1.0 [1, 2] |
| 1 | 2 | 7 | 70 | 59 | 4 (4) | 7 [5, 11] | 1.0 [1, 1] |
| 1 | 2 | 8 | 80 | 70 | 4 (4) | 11 [9, 15] | 1.0 [1, 1] |
| 1 | 4 | 3 | 30 | 41 | 4 (4) | 3 [1, 5] | 1.0 [1, 1] |
| 1 | 4 | 4 | 40 | 59 | 4 (4) | 3 [1, 5] | 1.0 [1, 1] |
| 1 | 4 | 5 | 50 | 78 | 4 (4) | 3 [1, 7] | 1.0 [1, 1] |
| 1 | 4 | 6 | 60 | 98 | 4 (4) | 2 [1, 13] | 1.0 [1, 1] |
| 1 | 4 | 7 | 70 | 119 | 4 (4) | 3 [1, 5] | 1.0 [1, 1] |
| 1 | 4 | 8 | 80 | 140 | 4 (4) | 3 [1, 17] | 1.0 [1, 1] |

Clique <= leaves in every completed run: True.

- In pure noise, trees and certified cliques grow quickly with `k` at every
  `alpha`, including `alpha = 4`, where the planted problem on the same
  designs is solved in at most 17 nodes. At `k = 8` the median certified
  clique is 44, 74 and 112 for `alpha = 1, 2, 4` (maximum 195), and one
  `alpha = 4` run hit the 30000-node cap. Growth is fastest at large
  `alpha`, as the proof of Theorem 4.3 suggests. At `alpha = 1`, `k = 9, 10`
  (4 seeds) show no further growth over `k = 8`; with 4 seeds and a pool of
  300 supports the clique is a weak lower bound there. Each clique is a lower
  bound for every convex-piece certificate, not only for the B&B we ran.
- With signal (SNR 2), the certified clique is 1 for `alpha >= 2`: the
  conflict graph gives no obstruction, consistent with Theorem 3.2.
- In every completed run the certified clique is at most the number of
  leaves of our B&B tree, as Lemma 1.4 requires.

### 6.5 Planted signal below the empirical recovery threshold

Table 6.5 (planted, `b = 1`, `p = 10k`, 4 seeds).

| signal `b` | `alpha` | `k` | `p` | `n` | runs (done) | nodes, geo. mean [min, max] | certified clique, median [min, max] |
|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 0.35 | 3 | 30 | 5 | 4 (4) | 8 [3, 19] | 2.5 [2, 4] |
| 1 | 0.35 | 4 | 40 | 6 | 4 (4) | 4 [1, 11] | 1.5 [1, 2] |
| 1 | 0.35 | 5 | 50 | 7 | 4 (4) | 14 [9, 31] | 2.5 [1, 5] |
| 1 | 0.35 | 6 | 60 | 9 | 4 (4) | 20 [11, 53] | 3.5 [2, 8] |
| 1 | 0.35 | 7 | 70 | 10 | 4 (4) | 30 [15, 43] | 5.0 [3, 5] |
| 1 | 0.35 | 8 | 80 | 12 | 4 (4) | 48 [21, 137] | 6.0 [3, 11] |
| 1 | 0.5 | 3 | 30 | 5 | 4 (4) | 8 [3, 19] | 2.5 [2, 4] |
| 1 | 0.5 | 4 | 40 | 7 | 4 (4) | 8 [3, 11] | 1.5 [1, 3] |
| 1 | 0.5 | 5 | 50 | 10 | 4 (4) | 19 [11, 49] | 3.5 [2, 7] |
| 1 | 0.5 | 6 | 60 | 12 | 4 (4) | 36 [17, 79] | 5.5 [3, 9] |
| 1 | 0.5 | 7 | 70 | 15 | 4 (4) | 73 [37, 211] | 8.0 [4, 24] |
| 1 | 0.5 | 8 | 80 | 18 | 4 (4) | 100 [59, 167] | 11.5 [7, 18] |

Clique <= leaves in every completed run: True.

In these runs `S*` is never the optimum, so they lie below the empirical
recovery threshold. They are not all below the first-order `n_IT`: the ratio
`n/n_IT` is 0.93, 0.92, 0.93, 1.05, 1.04, 1.14 at `alpha = 0.35` and 0.93,
1.08, 1.32, 1.40, 1.57, 1.71 at `alpha = 0.5` (`k = 3..8`;
`code/check_hard_revision.py`), and `k/n` is 0.4–0.8, far from the regime
`k/n -> 0` of Section 4. At `alpha = 0.5` the certified clique grows from 2.5
to 11.5 as `k` goes from 3 to 8, and the tree from 8 to 100 nodes: growth, but
much slower than in pure noise. At these sizes this says little about
Conjecture 5.2.

### 6.6 Branching rules below the C1 threshold

`p = 100, 200`, 6 seeds, scaled ridge. Failing single fixings are counted at
the B&B optimum `S°` by exact node solves.

Table 6.6.

| `p` | `k` | `alpha` | `n` | runs | `S*` optimal | removal half holds | C1 holds | median #failing forced-in nodes | `maxz` nodes, geo. mean [max] | `maxfrac` nodes, geo. mean [max] |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 100 | 6 | 0.50 | 14 | 6 | 0 | 0 | 0 | 14 | 66 [273] | 77 [271] |
| 100 | 6 | 0.75 | 21 | 6 | 2 | 3 | 3 | 14 | 29 [155] | 31 [159] |
| 100 | 6 | 1.00 | 28 | 6 | 3 | 2 | 1 | 28 | 39 [141] | 47 [153] |
| 100 | 6 | 1.25 | 35 | 6 | 5 | 5 | 4 | 0 | 17 [79] | 18 [91] |
| 100 | 6 | 1.50 | 41 | 6 | 6 | 4 | 4 | 0 | 14 [73] | 15 [95] |
| 100 | 6 | 2.00 | 55 | 6 | 6 | 5 | 5 | 0 | 10 [13] | 9 [17] |
| 200 | 8 | 0.50 | 21 | 6 | 0 | 0 | 0 | 70 | 311 [643] | 312 [619] |
| 200 | 8 | 0.75 | 32 | 6 | 3 | 0 | 0 | 126 | 156 [555] | 163 [601] |
| 200 | 8 | 1.00 | 42 | 6 | 5 | 0 | 0 | 14 | 51 [581] | 62 [667] |
| 200 | 8 | 1.25 | 53 | 6 | 5 | 4 | 3 | 0 | 24 [187] | 28 [213] |
| 200 | 8 | 1.50 | 64 | 6 | 6 | 6 | 6 | 0 | 14 [17] | 11 [15] |
| 200 | 8 | 2.00 | 85 | 6 | 6 | 6 | 6 | 0 | 10 [17] | 7 [17] |

The removal half fails whenever C1 fails, and the two rules give trees of
similar size. There is no sign of the rule-dependent window of Question 5.1
at these sizes. Trees are largest below the recovery threshold (`alpha = 0.5`,
where `S*` is never optimal).

### 6.7 The finite-size heuristic

Heuristic 3.8, evaluated on the realized null correlations, agrees with the
exact C1 outcome in 207 of 232 runs of Table 6.1 (`code/predict_c1.py`).

## 7. Literature comparison

Sources were checked as stated. The web-search budget of this session was
exhausted, so the search here was limited to direct arXiv fetches of the
abstracts named below and five arXiv API abstract queries (2026-09-28):
"perspective relaxation" AND "sparse regression" (0 hits); "safe screening"
AND "L0" (1 hit: Guyard–Herzet–Elvira, arXiv 2110.07308, node-screening
tests for L0-penalized least squares, with no random-design guarantee in the
abstract); "branch-and-bound" AND "sparse regression" AND "phase transition"
(0 hits); "Boolean relaxation" AND "sparse" (4 hits: Dong 1603.04572;
Bertsimas–Cory-Wright 1811.00138, a tightness condition for sparse
portfolios without sample-size thresholds; two applied papers);
"perspective" AND "cardinality" AND "ridge" (0 hits). None states a
node-count bound or a sharp exactness constant for random designs. An
unsuccessful search does not establish novelty.

- **Pilanci–Wainwright–El Ghaoui (Math. Program. 151, 2015; Section 3.1,
  Theorem 2 and Appendix 7.1 read in the author-hosted PDF; Dong,
  arXiv 1603.04572, read; page references and the literature status as in
  [`../../reviews/pwe-verification.md`](../../reviews/pwe-verification.md)).**
  The Boolean relaxation is `min_z y'(I + X D(z) X'/rho)^{-1} y` (our `g`
  with `lam = rho`); their Corollary 2 characterizes exactness by the
  certificate of our Corollary 2.4. Their Gaussian Theorem 2 (p. 72;
  per-entry noise `N(0, gamma^2)`, `rho = sqrt n`,
  `n > c0 (gamma^2 + ||w*||^2)/w_min^2 log d`, probability
  `1 - 2e^{-c1 n}`) is false as stated: for fixed `d, k, w*, gamma` the
  exactness probability tends to `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`
  (Remark 3.5). In their Appendix 7.1 the two lemmas are proved for different
  normalizations of `U_j` (Lemma 1 is true for `X_j'My/(rho n)`, Lemma 2 for
  `X_j'My/rho`); the mismatch is hidden by two incorrect steps in the proof of
  Lemma 1 (`sigma_max(M) <= 1/rho`, and variance `4 gamma^2/rho^2` instead of
  `4 n gamma^2/rho^2`). The theorem is repeated in Pilanci's 2016 thesis and
  cited as valid by Dong and by Bertsimas–Pauphilet–Van Parys; no erratum was
  found. With total noise energy `gamma^2`, PWE's argument goes through with
  an unspecified `c0` and failure probability
  `c exp(-c' n w_min^2/(gamma^2 + ||w*||^2))` (verification report); our
  Theorem 3.1, extended to `sigma = gamma/sqrt n` (that is, regime (A) with
  `sigma` replaced by `gamma/sqrt n`), identifies the sharp constant
  `c0 = 2` asymptotically, with equal magnitudes, which is not PWE's
  non-asymptotic statement. (PWE's `M` is our `M_S^{-1}`.) PWE's certificate is the `V = ∅`
  case of our saturated witness; C1 needs the saturated version.
- **Bertsimas–Van Parys (Ann. Statist. 2020, arXiv 1709.10029; abstract
  read).** Cutting-plane/outer-approximation algorithm on the same convex
  integer function (`g` restricted to binaries), with an empirical phase
  transition: above a sample size the method recovers the support and is
  faster than Lasso; below it, it is slow. Relation: the hard-side bounds
  (Lemma 1.4, Theorems 4.3–4.4) apply to any relaxation that is pointwise
  weaker than `g`, hence to outer-approximation master problems as well
  (review, Section 1). The easy-side theorems are for the perspective
  relaxation itself and do not transfer to weaker OA relaxations. Our reading
  of their transition is Section 5: a rule-independent easy regime above
  `2k log(p/sqrt n)` and, conjecturally, an intrinsically hard regime near the
  information-theoretic threshold.
- **Hazimeh–Mazumder–Saab (Math. Program. 2022, arXiv 2004.06152; abstract
  read).** Nonlinear B&B for `L0L2`-penalized least squares with
  perspective-type node relaxations solved by first-order methods, scaling to
  `p ≈ 10^7`. They report harder instances at small `n`/low signal. Their
  model penalizes `||beta||_0` instead of constraining it; our results are for
  the cardinality constraint, and the penalized analogue is open (Section 8).
- **Atamtürk–Gómez (safe screening from perspective relaxations, ICML 2020;
  rank-one convexification, arXiv 1901.10334; from memory, not re-read).**
  Screening fixes variables whose single fixing is prunable against the
  incumbent. C1 is the statement "screening by single-variable probing fixes
  every variable", so Theorem 3.2 is a random-design guarantee for complete
  screening, with the sharp threshold `2k log(p/sqrt n)`. Their stronger
  (rank-one, 2x2) relaxations change `g` and hence the conflict graph; the
  hard side says that in the pure-noise and low-SNR regimes, branching cannot
  replace such strengthening.
- **Gamarnik–Zadik (arXiv 1711.04952; abstract read; COLT 2017 companion
  from memory).** For `y = X beta* + W` with binary `beta*`, there is a gap
  between the information-theoretic `n*` and `n_alg ≈ (2k + sigma^2) log p`;
  the overlap gap property holds on `[n*, c n_alg]`; Lasso fails there; local
  search succeeds above `C n_alg`. Relation: our C1 threshold
  `2k log(p/sqrt n)` is below `2k log p` by `k log n`. For `k = p^gamma` it is
  `(2-gamma) k log p`, strictly inside the region where (by Wainwright's sharp
  threshold, recalled from memory) Lasso sign recovery fails. So on
  `(2-gamma, 2)` the L0-ridge estimator recovers `S*` exactly and
  perspective B&B certifies it with at most `2p+1` nodes for every
  variable-branching rule (with the incumbent available or best-bound
  search), while the Lasso fails. Their first-moment landscape computation is
  the model for our Lemma 4.1, and Lemma 4.1(b)'s reduction of the planted
  problem to a noise problem (the part of `y` outside `X_T` is independent of
  `X_T`) mirrors their reduction by conditioning on the overlap with the
  support (arXiv 1701.04455, Section 4, per the independent review); here it
  is applied to least-squares fits instead of binary coefficients. The
  second-moment part (Conjecture 5.2) is what we lack. OGP concerns local algorithms; our lower
  bounds concern certificates, and the two need not coincide (Li–Schramm,
  arXiv 2411.01836, per the scout report).
- **Dey–Dubey–Molinaro (midpoint argument) and Dey–Shah (lot-sizing).**
  Lemma 1.4 is the cross-polytope argument of Dey–Dubey–Molinaro
  (Proposition 3; their Section 6 also gives high-probability exponential
  lower bounds for a Gaussian-perturbed cross-polytope, the closest earlier
  random-instance result) with a convex objective, in the corrected form of
  the review. Dey–Shah (lot-sizing, ORL 2022, arXiv 2112.03965) use midpoints
  of 0/1 points whose objective value lies below the integer optimum, which
  is the linear-objective version of Lemma 1.4 and the closest precedent
  (both credited per the reviews' reading; we did not re-read them). The
  curvature enters through Lemma 1.5. The other mechanism
  named in the program, the certificate integral of
  Bachoc–Cesari–Gerchinovitz for Lipschitz optimization, concerns spatial
  branching and is not used here.
- **Other connections (from memory).** The perspective relaxation of `L0L2`
  equals least squares regularized by the squared `k`-support norm
  (Argyriou–Foygel–Srebro), and Dong–Chen–Linderoth relate relaxation and
  regularization. As `lam -> inf` the relaxation becomes linear in `z` and
  exact, and the estimator becomes marginal screening, whose recovery
  threshold `n > 2(k + sigma^2/b^2) log p` matches Theorem 3.1 in that limit
  when `log k = o(log p)`. For `k = p^gamma`, interference among the true
  features changes the constant (heuristically to
  `2(1 + sqrt gamma)^2 (k + sigma^2/b^2) log p`, per the independent review;
  not checked here). Inside (A), `lam <= n/log^2 p` suppresses this
  interference, which is why Theorem 3.1 has no such factor.

## 8. What remains open

1. Question 5.1 (a rule-dependent regime below the C1 threshold), in
   particular whether the removal half of C1 survives below
   `2k log(p/sqrt n)` for large `p`.
2. Conjecture 5.2 (exponential cliques below the information-theoretic
   threshold at fixed SNR): a second-moment count of near-optimal,
   pairwise-far supports.
3. Non-asymptotic versions: Theorems 3.1–3.2 hold with explicit error terms
   (the proofs give them), but at `p <= 1600` the observed C1 threshold is at
   a markedly smaller `tau` than `2 log(p lam/n)` (Section 6). A
   finite-`p` predictor with the right constants (for example, the
   Gaussian-tail heuristic `sum_l (|a_l| - kappa)_+^2/n` versus
   `(m0^2 - kappa^2)/lam`) is not proved.
4. General split and SOS trees in the window below C1: Lemma 1.2 is specific
   to variable branching.
5. The `L0L2`-penalized problem of Hazimeh–Mazumder–Saab, and
   outer-approximation relaxations (Bertsimas–Van Parys) on the easy side.
6. The pure-noise hard side at small `alpha` (`x >= x0`), where our
   construction fails but the computations still show fast-growing trees
   (for `alpha = 1` the runs have `lam/n ≈ 0.6`, far from `lam = o(n)`, so
   they do not bear on this).
7. The second-order formulas of Heuristic 3.8 (Section 3.5), which match the
   observed finite-size thresholds, are not proved.

## Revision after review (2026-09-29)

Both reviews found Theorems 3.1, 3.2, 4.3 and 4.4 correct. Each change below
was re-derived or re-checked here before it was made.

Easy side (Sections 1–3, 6):

1. The qualifier "with the incumbent `OPT` available when off-path nodes are
   examined, or with best-bound search" now accompanies every statement that
   all variable-branching trees are linear (Summary, Corollary 3.3,
   Section 5, Section 6.1, Section 7).
2. Attributions: (F2) = PWE's Boolean relaxation is due to Xie–Deng
   (abstract checked); Lemma 2.2 at the root-optimal residual is
   Atamtürk–Gómez's Proposition 2 (read in their paper and quoted after
   Lemma 1.1).
3. Proof of Theorem 3.2(b): the false phrase "`N'` grows polynomially" is
   replaced by `N' >= min(mu/2, log^4 p) - 1 -> inf`. Theorem 3.2(c) now
   gives `T` explicitly (it depends on `n/(k log(p/sqrt n))` as well as on
   `eps`). Assumption (A) is noted to require `p >= e^17 ≈ 2.4 × 10^7`, so
   all computations lie outside it, and Section 6.1 no longer calls the
   fixed-`k` trend a prediction of the theorems. Theorem 3.2(a)'s margin is
   improved to `lam b^2/log p` (Step 5 already gave `(2 - o(1)) lam b^2/log p`).
   The converse's remoteness from computable sizes is now stated for all
   `lam`, not only `lam = sqrt n`.
4. PWE: Remark 3.5 and Section 7 now state that PWE's Theorem 2 is false as
   stated for per-entry noise. We read their Appendix 7.1 and confirmed the
   error the review located: the proof of Lemma 1 uses
   `sigma_max(M) <= 1/rho` (in fact 1) and a variance bound `4 gamma^2/rho^2`
   (in fact `4 n gamma^2/rho^2`), with inconsistent normalizations between
   Lemmas 1 and 2. Our own counterexample script (`check_pwe.py`, 19 of 20
   instances with `S*` certified unique optimum and an inexact root) confirms
   the review's `pwe_counterexample.py`. After an independent verification
   report (`../../reviews/pwe-verification.md`), Remark 3.5 was rewritten a
   second time: it now leads with the elementary `n -> inf` argument (optimal
   support equal to `S*` w.h.p., exactness probability tending to
   `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`), describes the proof error as a
   normalization mismatch between PWE's Lemmas 1 and 2 hidden by two
   incorrect steps, cites page numbers and the literature status (no erratum;
   repeated in Pilanci's thesis; cited as valid by Dong and by
   Bertsimas–Pauphilet–Van Parys), drops the claim that an extra SNR
   assumption restores the theorem as stated, and states that the
   total-energy version with `c0 = 2` is our asymptotic extension of
   Theorem 3.1 (checked step by step for `sigma = gamma/sqrt n`), not a proof
   of PWE's non-asymptotic statement.
5. Section 6: the "capped" procedure could not find failures, because the
   saturated witness ties all violators. All 31 capped runs were re-decided
   exactly with a new decider (dual-vector pool plus column generation):
   30 satisfy C1 and one fails (`p = 3200`, seed 1007; forcing in `j = 991`
   gives 80.286 and `j = 2714` gives 82.576, below `f(S*) = 82.700`). Tables
   6.1–6.3, Section 6.3 and the Summary were corrected. The results agree
   with the review's independent re-decision.
6. Heuristic 3.8 now includes the second-order formulas
   `tau^2 ≈ 2 log(p lam/n) + 0.93 - 5 log tau^2` (C1) and
   `+ 1.55 - 3 log tau^2` (witness), re-derived here, which explain why the
   observed thresholds sit at about half of `2 log(p lam/n)`. The marginal
   screening remark of Section 7 is restricted to `log k = o(log p)`.

Hard side (Sections 1, 4, 5, 6):

7. The sentence after Theorem 4.4 about the "detection scale" was false for
   `gamma < 1/2`; it is replaced by the correct form
   `b < sigma sqrt(2 log(p/k)/n) sqrt(K(x)/x)` and the statement that the
   region lies strictly below the information-theoretic threshold
   (factor values re-computed in `check_hard_revision.py`).
8. Section 5 now lists the hard side under its own scaling (bounded total
   SNR), with the hypotheses `x < x0`, `lam = o(n)`, `k/n -> 0`, and notes
   that at fixed SNR the conjectured hard region shrinks to `alpha -> 0` in
   the `alpha` parametrization.
9. Smaller fixes: Step 6 "increases in `s_U`" is now "decreases"; the
   Section 4.4 shortfall includes `log(4 pi)`; "every support explains about
   `x ||y||^2`" is corrected; Section 6.4 says "same `X`" (the noise differs
   between `b = 0` and `b = 1`); Theorem 4.3 requires `lam > 0`.
10. Conjecture 5.2 is restated with a range for `lam`, `eps = 0`, and a lower
    limit `n >= (1+delta)k` (requiring `gamma < 2/3`), and its
    "what is missing" paragraph now says that the regime has `x -> inf` and
    `k/n` bounded away from 0 (outside the Section 4 method even in pure
    noise) and that Lemma 1.5(b), not (a), is the natural criterion there.
11. Section 6.5 is retitled "below the empirical recovery threshold":
    8 of its 12 rows have `n/n_IT` between 0.92 and 1.71 (re-computed), and
    the claimed evidence for Conjecture 5.2 is weakened.
12. Theorem 4.3 (and 4.4) now give cliques of size `C(p,k)^{c'}`, via
    `M = k(p/k)^theta` in the construction. This was the review's sketch; the
    error terms were checked and the full proof is in Section 4.3 (Steps
    2–6). The previous fixed-`R` form, `exp(c k)`, is kept as a remark.
13. Novelty and precedents: Dey–Shah (lot-sizing) and Dey–Dubey–Molinaro's
    Gaussian-perturbed cross-polytope are credited next to Lemma 1.4;
    Lemma 4.1(b)'s reduction is credited to the Gamarnik–Zadik device. The
    finite-`p` statement of Section 4.4 is now grid-specific: on a wider grid
    (`alpha` up to 4096) a conflicting pair is certified at
    `p = 10^{5.5}`–`10^6` (re-computed), and the review reports a clique
    `>= e^10` at `p = 10^9`, in each case with `n` of order `10^4` to
    `10^7`.

Also added, following suggestions in the reviews: the two-copy form of
Lemma 1.5's proof, and a remark on when the node form of Lemma 1.4 is
informative (factor `p+1` suffices for binary variables).

### Second round: recheck of the revision

A fresh recheck ([`../../reviews/sparse-recheck.md`](../../reviews/sparse-recheck.md))
found the proofs and all Section 6 table numbers correct and asked for the
following; each was verified here before the change.

1. **Seed-1007 explanation.** The revision had attributed the `p = 3200`
   failure to "a single unusually strong null feature". Re-checked with
   `check_s1007.py`: four forced-in nodes fail (null ranks 1, 5, 6, 50), and
   every forced-in bound we solved is within 2.75 of `f(S*)` (5.87–8.70 at
   seed 1000; over all 3195 nodes, per the closing audit, within 2.79). The violators recover about 60% of the budget price. Section 6.3,
   the remark after Corollary 3.4 and the Summary now describe it as the
   finite-size many-violator balance.
2. **Stale numbers.** The Summary's C1 onset at `p = 1600` is 1.75, not 2.0.
   Heuristic 3.8's ranges now include seed 1007 (sat-gain 70.3, root gap
   9.9, re-computed). The price `sqrt n ≈ 11` is labeled nominal (realized
   7.2–8.9).
3. **`decide_c1_exact`.** It now returns `'undecided'` if `max_solves` is
   exhausted and `'C1-nonstrict'` if some node equals `f(S*)` only within
   tolerance. Neither case occurred in the stored runs (at most 109 solves,
   no tolerance passes), so all reported decisions stand. A regression test
   on three `p = 200` instances reproduced the stored decisions.
4. **Hard-side hypotheses.** `k -> inf` is added to the Summary and
   Section 5. The delivered `c'` is reported as small (values corrected in
   the third round below). The fixed-`R`
   remark now gives `exp(k e(mu,R)(1 - o(1)))`, and Section 4.4 notes the
   Gilbert–Varshamov-free pair and the `e^{-M/4}` term.
5. **Total-energy extension.** The sentence no longer cites Theorem 3.2(b)
   as part of Theorem 3.1's proof. It now says that for fixed `gamma`, (A)
   forces `k -> inf`, so the `gamma^2/b^2` term lies inside the `o(1)`, and
   that the proof also allows `gamma^2 = O(k b^2)`, where the coefficient 2
   applies to both terms.
6. **PWE remark.** `M_S` is corrected to `M_S^{-1}` in items 2–3, PWE's `M`
   is identified with our `M_S^{-1}`, the Monte Carlo frequencies and the
   conditional estimates are distinguished, the report's caveat on the
   total-energy repair is restored, the 0.99 figure is tied to `d = 50`,
   `k = 5`, and "8 of which" is disambiguated. Section 7 says "(A) with
   `sigma` replaced by `gamma/sqrt n`".
7. **Conjecture 5.2.** It now requires `delta < (2 - 3 gamma)/(2 - gamma)`,
   the condition for its range of `n` to be nonempty.

### Third round: closing audit

The closing audit ([`../../reviews/closing-audit-b.md`](../../reviews/closing-audit-b.md))
confirmed the second-round substance (all 3195 forced-in nodes at seed 1007
solved; exactly the four stated nulls fail) and asked for four corrections,
each re-derived here:

1. The Summary's "`c'` at most about 0.11 (as `x -> 0`)" was false. As
   `x -> 0` the proof's constraints allow up to `3 - 2 sqrt 2 ≈ 0.17`
   (derived by hand: maximize `(1-mu) theta` subject to
   `(1+mu)(1-theta) > 1`); the approach is slow (0.161 at `x = 10^-3`).
2. The values from a coarse grid were slightly low. Re-computed with a fine
   grid and Nelder–Mead polish (`check_cprime.py`): 0.106, 0.059, 0.022,
   0.0068, 0.0020, 0.0001 at `x = 0.05, 0.2, 0.5, 0.8, 1.0, 1.2`; the planted
   case is 4.1–5.1 times smaller.
3. Section 5 cited Section 4.2 for the small `c'`; Section 4.2 now states the
   values (paragraph "Size of `c'`").
4. "Within 2.75 of `f(S*)`" holds for the nodes we solved; over all 3195
   forced-in nodes the maximum is 2.79, and the relaxation recovers at least
   61.0% of the price for every one (audit's computation). Section 6.3 and
   the second-round item 1 now say so.

## Appendix: code, commands, and what each check establishes

All commands ran from `research-20260928b/bb-complexity/sparse-regression/data/`
(or `code/` where noted) with Python 3.13, NumPy 2.5, SciPy 1.18,
Clarabel 0.11, single-threaded (`OMP/OPENBLAS/MKL/RAYON_NUM_THREADS=1`).
These are targeted local checks; no project-wide checks were run and CI was
not inspected.

Code (`code/`):

- `core.py`: instances; ridge values; node relaxation by Clarabel in residual
  form (`solve_node`), returning the certified dual bound `L(a)` of
  Lemma 1.1 at the recovered residual; column generation for large `p`
  (`solve_node_cg`; the dual bound is always evaluated on the full node);
  the saturated witness of Proposition 2.3 (`saturated_witness`,
  `best_saturated`, grid over `kappa/m0 in [0.5, 1]`); exact single-fixing
  dual bounds at a given `alpha` (`single_fixing_bounds`).
- `bnb.py`: best-first B&B, branching rules `maxfrac` and `maxz`, pruning
  on certified bounds (relative tolerance `1e-7`).
- `hard.py`: exact midpoint values (Lemma 1.5), Gilbert–Varshamov codes, the
  union-bound level `rho*`, and the finite-`p` condition of Section 4.4.
- `exp_c1.py`, `exp_hard.py`, `exp_rule.py`: the experiments of Section 6;
  `summ_c1.py`, `summ_hard.py`, `summ_rule.py`: the summaries.
- `check_lemmas.py`, `check_converse.py`: numerical checks of the
  deterministic lemmas.

Commands and results:

- `python3 ../code/check_lemmas.py` (from `code/`): on 30 random instances,
  the witness identity of Lemma 2.1 holds to relative error `5e-15`,
  `c_V = a_V - H u` to `3e-14`, `beta^S = X_S'r_S/lam` to `4e-15`, the
  midpoint formula of Lemma 1.5 to `1.2e-15`; Lemma 1.5(a) and (b) are never
  violated; the dual bound of Lemma 1.1 at a random `alpha` is below the
  node value.
- `python3 test_core.py` (from `code/`): the Clarabel residual-form node
  solver agrees with the scout's solver (`sparse_bb.py`) on 6 random nodes
  and gives equal or tighter certified bounds.
- `python3 check_converse.py` (from `code/`): evaluates the explicit primal
  point of Lemma 2.5; its value never exceeds the analytic bound. At
  `p <= 1000` it does not yet certify failure of C1 (the exact node values
  do), consistent with Theorem 3.2(b) being asymptotic.
- `python3 check_pwe.py` (from `code/`): the PWE counterexample of
  Remark 3.5 (20 instances; 19 with `S*` certified unique optimum and root
  value strictly below `f(S*)`).
- `python3 check_prob.py` (from `code/`): the closed form of `m(tau)` in
  (G5) matches numerical quadrature for `tau in {0.5,1,2,3,4}` (to 7
  digits) and is below `2 phi(tau)/tau`; the Beta Chernoff bound of
  Lemma 4.1 dominates the exact Beta tail on a grid of `(n, k, rho)`
  (maximum ratio 0.48).
- The PWE-certificate check of Remark 3.5 (inline Python in `code/`):
  `lam = sqrt n`, `b = 1`, `sigma = 0.5`, `k = 5`, 20 seeds for each
  `p in {100, 1000, 10^4}` and `alpha in {5, 20}`: certificate holds in 0 of
  120 instances; median `max|a_l|/m0` = 1.61, 1.39, 2.02, 1.83, 2.27, 2.13.
- Hard-side finite-`p` condition (Section 4.4): inline evaluation of
  `hard.theorem_condition2` over the grid stated there.

Experiments of Section 6 (from `data/`; `MAXEX` caps exact node solves):

- Table 6.1:
  `python3 ../code/exp_c1.py c1_p200_k8_t1.5.jsonl 200 8 1.5 1.25,1.5,1.75,2.0,2.5,3.0,3.5,4.0 8 4`;
  `python3 ../code/exp_c1.py c1_scaleP_k8_t1.5.jsonl P 8 1.5 1.0,1.25,1.5,1.75,2.0,2.5,3.0 8 2`
  for `P = 100, 400` and, with `MAXEX=40`, `P = 1600`; plus
  `MAXEX=40 python3 ../code/exp_c1.py c1_scaleP_1600_hi.jsonl 1600 8 1.5 3.0,2.5,2.0 8 1` and
  `MAXEX=40 python3 ../code/exp_c1.py c1_scaleP_1600_a2.jsonl 1600 8 1.5 2.0 8 2`
  (same seeds, run in parallel to save time; duplicates removed when
  tabulating; runs still unfinished when this note was written are
  omitted).
- Table 6.2: `MAXEX=40 python3 ../code/exp_c1.py c1_gamma_half.jsonl 400 20 1.5 1.0,1.25,1.5,1.75,2.0,2.5 6 2`,
  and the rows `alpha <= 1.5` rerun without a cap:
  `MAXEX=100000 python3 ../code/exp_c1.py c1_gamma_half_full.jsonl 400 20 1.5 1.0,1.25,1.5 6 2`.
- Table 6.3: `python3 ../code/exp_c1.py c1_sqrtn_k5.jsonl P 5 sqrtn 3.0 8 2` for
  `P = 50, 200`, and with `MAXEX=40` for `P = 800, 3200`; the direct node
  solves at `p = 3200` are an inline script using `solve_node_cg`.
- Table 6.4: `python3 ../code/exp_hard.py hard_k3-8.jsonl 3,4,5,6,7,8 1,2,4 0,1 4 3 30000 10`
  and `python3 ../code/exp_hard.py hard_noise_k9-10.jsonl 9,10 1 0 4 1 40000 10`.
- Table 6.5: `python3 ../code/exp_hard.py hard_planted_lowalpha.jsonl 3,4,5,6,7,8 0.35,0.5 1 4 1 30000 10`.
- Table 6.6: `python3 ../code/exp_rule.py rule_p100_k6.jsonl 100 6 0.5,0.75,1.0,1.25,1.5,2.0 6 1 20000`
  and the same with `rule_p200_k8.jsonl 200 8`.
- Section 6.7: `python3 ../code/predict_c1.py c1_p200_k8_t1.5.jsonl c1_scaleP_*.jsonl`.
- Tables: `python3 ../code/make_tables.py`; `python3 ../code/fill_note.py`
  inserted them into this note; after the review,
  `python3 ../code/regen_tables.py` regenerated Tables 6.1–6.3 with the exact
  decisions.
- Exact re-decision of the 31 capped runs (after review):
  `python3 ../code/redecide_c1.py c1_redecided.jsonl 5 c1_p200_k8_t1.5.jsonl c1_scaleP_k8_t1.5.jsonl c1_scaleP_1600_hi.jsonl c1_scaleP_1600_a2.jsonl c1_sqrtn_k5.jsonl c1_gamma_half_full.jsonl`
  (30 satisfy C1, 1 fails; at most 109 node solves and 179 s per run), and
  the direct solves of the failing nodes `j = 991, 2714` at `p = 3200`,
  seed 1007 (inline script with `solve_node_cg`, 300 rounds).
- Second recheck round: `python3 ../code/check_s1007.py` (forced-in node
  values at `p = 3200`, seeds 1007 and 1000, nulls of ranks 1–60, 100, 500,
  median and weakest; log `data/check_s1007.log`) and
  `python3 ../code/check_cprime.py` (the largest `c'` the proof of
  Theorem 4.3 admits, pure noise and planted).
- Hard-side revision checks: `python3 ../code/check_hard_revision.py`
  (the `n/n_IT` ratios of Table 6.5, the detection-scale factor, and the
  wider finite-`p` grid of Section 4.4).
- The scout's C1 data check of Section 6.1: inline Python over
  `../../scouting/bb-tree-size-convex/sparse_single.jsonl`.

Each run of the C1 experiment decides, for its instance, whether C1 holds
at `S*` (and hence whether every variable-branching tree is linear); each
hard-side run gives a certified lower bound (the clique) on the leaves of
every convex-piece certificate for its instance. None of these runs is
evidence for the asymptotic constants of Theorems 3.1–3.2 and 4.3–4.4 beyond
the trends described in Section 6.
