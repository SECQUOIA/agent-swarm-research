# Certification thresholds for box-relaxation branch-and-bound in random binary least squares

Workstream `binary-least-squares/` of [`../PROGRAM.md`](../PROGRAM.md) (the
scout's question Q2 in
[`../../scouting/bb-tree-size-convex.md`](../../scouting/bb-tree-size-convex.md)).
Date: 2026-09-29. Status: proofs and computations by the workstream owner,
revised after two independent reviews and a recheck of the revisions
(Section 10); the reviews found no counterexample to a theorem. Code is in [`code/`](code/),
result files in [`data/`](data/). All computations use floating point; node
bounds are certified dual bounds, not exact arithmetic.

## Summary

Model: `y = A x* + w`, `A = sqrt(rho/N) H`, `H` an `M x N` Gaussian matrix
with `M = beta N`, `beta >= 1`, `x* in {-1,1}^N`, `w ~ N(0, I)`; branch and
bound (B&B) for `min ||y - Ax||^2` over `{-1,1}^N` with the box relaxation
`[-1,1]^N` at the nodes. Main findings (w.h.p. means with probability
`1 - o(1)` as `N -> inf`, `beta` fixed). Section 10 lists the changes made
after the two independent reviews.

| quantity (`beta = 1` unless stated) | threshold | status |
|---|---|---|
| `x*` is the ML point | `rho = 2 log N` | known for `beta = 1` (Hansen et al. 2009; Hassibi et al. 2014); Theorem 2.2 for all `beta` |
| box decoder `sign(xhat) = x*` | `rho = 4 log N` | Hu–Lu 2020 (used as an input only) |
| midpoint conflicts exist | `rho < 8 log N` | Theorems 2.3 and 5.1 |
| root relaxation exact | never: probability `<= ((1 + 2(1+4rho)^{-1/2})/2)^N` | Theorem 1.2 |
| C1, hence `<= 2N+1` nodes for every variable-branching rule (incumbent `OPT` given, or best-bound search) | `rho = (1 + o(1)) N/4` | `>= (1+eps) N/4` suffices; below `(1-eps) N/4` C1 fails (given Hu–Lu); every single fixing fails below `(1-eps) N/8` (Theorem 3.1) |
| size of every certificate for the box relaxation of `f` | `exp(Theta((N/rho) log rho))` for `rho -> inf`, `rho <= c' N`; `exp(Theta(N))` at fixed `rho >= 71` | Theorems 4.1 and 4.3; the constants differ by a factor `~10^4 - 10^5`, and the lower bound is vacuous below `N ~ 1.7 10^7` |
| Shor SDP, and the eigenvalue-shift convex relaxation, exact at `x*` (`beta > 1`) | `rho = Theta(log N)` | Theorem 6.2, Proposition 6.3; the SDP is not exact for `beta = 1` below `rho ~ N^3` (numerics) |

**(1) Root exactness has no SNR threshold (Section 1).** `x*` is a box
minimizer iff every `zeta_i = x*_i a_i'w >= 0` (the KKT signs). These are
fair coins at every SNR, so the probability is exactly `2^{-N}`
(Proposition 1.1). The root is exact iff the box minimizer is a vertex, which
has probability at most `((1 + 2(1+4rho)^{-beta/2})/2)^N` (Theorem 1.2). No
margin is gained from the SNR: the sign of each gradient coordinate does not
depend on `rho`. The root gap is linear in `N`. We use the known law of the
projection onto a cone spanned by Gaussian vectors (the NNLS face is uniform
over all `2^n` faces and the projected fraction is a Beta mixture;
Hug–Schneider, Godland–Kabluchko–Thäle, McCoy–Tropp), with a self-contained
proof that extends the face law to sign-symmetric column laws (Theorem 1.3).
It gives `W - R <= chi^2` with `Bin(N, 1/2)` degrees of freedom, with
equality once the box's upper bounds are inactive (for `beta > 1` at
`rho >= C_beta log N`, proved; for `beta = 1` from `rho ~ log N`, using
Hu–Lu). An explicit witness gives `W - R >= (beta/(1 + 2beta) - o(1)) N`
(Theorem 1.7). The `4 log N` threshold in the literature concerns rounding,
not exactness.

**(2) C1 needs linear SNR (Section 3).** Forcing one wrong value costs about
`(W + 4 rho beta)(1 - 1/(2beta)) - W`, because the remaining coordinates
absorb the fraction `1/(2beta)` of the new residual (Theorem 1.3 again). C1
holds w.h.p. iff `rho > (1 + o(1)) N/(4(2beta - 1))`: for `beta > 1`
unconditionally, for `beta = 1` given the Hu–Lu input (Theorem 3.1). Above
the threshold every variable-branching tree has at most `2N+1` nodes, for any
rule, provided the incumbent value `OPT` is available when off-path nodes are
examined (or with best-bound search). C1 lies strictly below root exactness
(which never holds), but it is not a `c log N` threshold.

**(3) ML (Section 2).** `x*` is the unique ML point w.h.p. when
`rho beta >= (2+eps) log N`, and not when `rho beta <= (2-eps) log N`. For
`beta = 1` the achievability half is due to Hansen et al. and Hassibi et al.
Below the threshold, `W - OPT` is at most `N^{1 - c/2 + o(1)}` at
`rho beta = c log N` and at most `4N e^{-0.148 beta rho} + O(log N)` at
fixed `rho`.

**(4) Hard side: superpolynomial for every `rho = o(N)` (Sections 4, 5).**
All statements concern the box relaxation of `f` itself (Section 4.3 lists
what is not covered).

- *Class number (Theorem 4.3).* For `71 <= rho <= c'_1 N` (`beta = 1`,
  `c'_1 ~ 1.4e-4`), `log kappa >= c_1 (N/rho) log rho - log(8N)` with
  `c_1 = 1.8e-5`. So every convex-piece certificate for the box relaxation —
  variable, general split, multiway or semantic branching, any rule, with cuts
  in `x` valid at the nodes — has at least `kappa` leaves, and at least
  `kappa/(N+1)` nodes with incumbent-based bound tightening, for tolerances
  `eps' <= rho`. The proof is non-pairwise: a class containing many vertices
  that differ from `x*` on descent coordinates contains their barycenter,
  whose value undercuts `OPT` unless the class's supports overlap heavily; an
  entropy lemma (Lemma 4.2) shows that heavily overlapping families are
  exponentially small. The bound is asymptotic: it is positive only for
  `N >~ 1.7 10^7`.
- *Upper bound (Theorem 4.1, sharpened after review).* Static-order variable
  branching with the incumbent needs at most
  `(N+1) exp((1 + o(1)) (N/(4(2beta - 1) rho)) log rho)` nodes for every
  `rho -> inf`, `rho beta <= N`, including below the ML threshold (the factor
  `N+1` matters when `rho = Theta(N)`; at practical sizes the proved exponent
  is 2–8.5 times the asymptotic one, of which the prefactor `1/kappa_rho`
  accounts for 1.5–5). Hence
  `log(min certificate) = Theta((N/rho) log rho)`: `exp(Theta(N log log
  N/log N))` at `rho = c log N`, and `exp(Theta(N))` at fixed `rho >= 71`. The
  two constants differ by a factor of about `10^4 - 10^5`. For `beta = 1` and
  `c >= 2`, Papailiopoulos' algorithm finds `x*` in polynomial time at
  `rho = c log N`, so box-relaxation certificates are superpolynomially
  harder than search there; for `beta > 1` the known polynomial search covers
  only `rho > 4 log N/(2beta - 1)` (Hu–Lu). Conjecture 4.5 gives the sharp
  constant `1/(4(2beta - 1))` for every variable-branching rule.
- *Midpoint cliques (Theorems 2.3, 5.1).* The midpoint clique number is
  `exp(N^{1 - c/8 + o(1)})` at `rho beta = c log N`, `c < 8` (both bounds
  proved; the upper bound follows the hard review), `exp(Omega(N))` at fixed
  `rho >= rho_1` (`~ 600` for `beta = 1`), and 1 above `8 log N`: midpoint
  conflicts are blind on `8 log N < rho = o(N)`, where the class number is
  superpolynomial. The segment graph is not analysed. The binary problem
  sidesteps the Gaussian-basis obstacle of the integer-core note (its
  Conjecture 3.8 remains open): the box creates the conflicts.

**(5) SDP (Section 6).** The Shor SDP is exact at `x*` iff
`A'A + diag(zeta) ⪰ 0` (Jaldén–Martin–Ottersten 2003). For `beta > 1` this
holds w.h.p. once `rho >= (1+eps) 2beta log N/(sqrt(beta)-1)^4`
(Theorem 6.2), and from that SNR on even the convex eigenvalue-shift
relaxation `f + lambda_min(A'A) sum(1 - x_i^2)` is exact (Proposition 6.3).
For the shift this threshold is sharp; the SDP becomes exact much earlier
(at `beta = 2` the per-instance thresholds are about `73–110 log N` for the
shift against `4.4 log N` for the SDP).
Numerically the SDP threshold is near `2 beta log N/(beta - 1)^2` for
`beta >= 2`. At those SNRs one node certifies `x*` while every box-relaxation
certificate has `exp(Omega(N log log N/log N))` leaves: a superpolynomial
separation between relaxations, as the program's thesis predicts. For
`beta = 1` the SDP becomes exact only for `rho` of order `N^3`, and at
`N <= 40` its root gap is about one half to two thirds of the box gap;
whether SDP-based B&B is polynomial for square systems is open.

**(6) Computations (Section 7).** Root law, C1 transitions (`N <= 800`), B&B
trees (`N <= 256`), the thresholds 2 and 8 (single-coordinate law up to
`N = 10^5`), and SDP thresholds (`N <= 1600`) agree with the theory at first
order. The asymptotic statements are pre-asymptotic at practical sizes: C1
needs `rho ~ 0.4 N` at `N = 800`, and most-fractional B&B trees at
`rho = 4 log N` have 44, 97, 509 and about `1.6 10^4` nodes for
`N = 32, 64, 128, 256` (static order: more than `10^5` at `N = 256`). In node
count the box relaxation still beats natural-order sphere decoding by a wide
margin on the same square instances (at `N = 64`: 246 against `6 10^4`
nodes); a sphere-decoder node is much cheaper, and in single-thread Python the
sphere decoder was faster in wall-clock time at `N = 64` (recheck: 0.8 s
against 3.4 s for six instances). An exact-law
predictor of tree size (node bound `~ f(x^Wr)(1 - (N-d)/(2M))`) matches real
static-order trees within a factor of about 2 where both are available. As a
heuristic model, not a bound, it extrapolates to `e^{~80}` nodes at
`N = 3000` and `e^{~1900}` at `N = 10^5` for `rho = 4 log N`.

What is open: the sharp constants (Conjectures 3.3 and 4.5), small fixed
`rho < 71`, adaptive-rule upper bounds, the segment-graph chromatic number,
and SDP-based B&B for square systems (Section 9).

Targeted local checks only (commands in the appendix). No project-wide
checks were run and CI was not inspected.

## 0. Model, notation, and conventions

### 0.1 Model

- `N` unknowns, `M = beta N` observations with `beta >= 1` fixed (the
  square case is `beta = 1`). `H in R^{M x N}` has iid `N(0,1)` entries,
  `A = sqrt(rho/N) H`, `w ~ N(0, I_M)` is independent of `H`, and
  `y = A x* + w` for a deterministic `x* in {-1,+1}^N`. So `rho` is the SNR
  per observation and `||a_i||^2 ~ rho beta`.
- Problem: `OPT = min{ f(x) : x in {-1,1}^N }`, `f(x) = ||y - A x||^2`.
  Write `W = ||w||^2 = f(x*)`.
- Node relaxation: `min{ f(x) : x in [-1,1]^N, x_i fixed on the node's
  fixed set }` (the box relaxation). `R` is the root value.
- "W.h.p." means with probability `1 - o(1)` as `N -> inf`; all statements
  hold uniformly in `x*`.

### 0.2 Error coordinates

Put `b_i = x*_i a_i` (so `B = A diag(x*)`), `u_i = 1 - x*_i x_i in [0,2]`, and

```
y - A x = w + B u,      F(u) := ||w + B u||^2 = f(x),      zeta_i := b_i' w .
```

`u_i = 0` is the correct value of coordinate `i`, `u_i = 2` the wrong one.
The vertex that differs from `x*` on `S` is `x^S`, with `u = 2 1_S`, and

```
f(x^S) - W = 4 sum_{i in S} zeta_i + 4 ||B_S 1||^2,      f(x^{i}) - W = 4 (zeta_i + ||b_i||^2).
```

The gradient of `f` at `x*` is `-2 A'w`, and `x*_i d_i f(x*) = -2 zeta_i`: a
positive `zeta_i` means that moving coordinate `i` into the box increases `f`
to first order.

A node fixes some `u_i` to `0` (correct fixing) or `2` (wrong fixing). If
`Fx` is the fixed set, `Wr ⊆ Fx` the wrong fixings and `Phi = [N] \ Fx` the
free set, the node value is

```
r(Fx, Wr) = min{ ||v + B_Phi u||^2 : u in [0,2]^Phi },     v = w + 2 B_Wr 1 .      (0.1)
```

The vector `v` depends only on `w` and the columns in `Wr`, so it is
independent of `B_Phi`. This independence is used throughout.

**Lemma 0.1 (conditional structure).** The signed columns
`h~_i = x*_i h_i` are iid `N(0, I_M)` and independent of `w`. Given `w != 0`,
put `what = w/||w||`, `g_i = h~_i' what` and `h_i^perp = h~_i - g_i what`.
Then `g_1, ..., g_N` are iid `N(0,1)`, the `h_i^perp` are iid
`N(0, I - what what')`, and all of these are independent of each other and of
`w`. Moreover `zeta_i = sqrt(rho/N) ||w|| g_i` and
`||b_i||^2 = (rho/N)(g_i^2 + ||h_i^perp||^2)`.

*Proof.* Sign changes of columns preserve the law of `H`, and `x*` is
deterministic. Given `w`, rotate so that `what = e_1`; the rotated columns are
iid `N(0, I)` and their first coordinates are the `g_i`. ∎

The same statement holds with `w` replaced by any vector `v` independent of
the columns considered (for example `v` of (0.1) and the free columns).

### 0.3 Branch-and-bound conventions

We use the framework of the integer-core note
[`../integer-core/relaxation-intrinsic-bounds.md`](../integer-core/relaxation-intrinsic-bounds.md)
(Sections 1 and 5), with `P = {-1,1}^N` (all vertices are feasible):

- *Convex-piece trees and certificates* (its Definitions 1.1, 1.2): nodes
  carry convex sets whose children cover the parent's vertices; the node
  bound is the box relaxation over the node's effective set; a
  `tau`-certificate has all leaf bounds `>= tau`, with `tau = OPT - eps`.
  Every completed B&B run that prunes by bound, integrality or infeasibility
  is such a certificate (its Lemma 1.3). Variable, general split, multiway and
  "semantic" branching are included.
- *Class number* `kappa_tau` (its Definition 1.4): the least number of
  classes, covering `P`, whose convex hulls have relaxation value `>= tau`.
  Every certificate has at least `kappa_tau` leaves (its Theorem 1.6), and
  `kappa_tau` is exactly the minimum number of leaves over arbitrary convex
  pieces (its Theorem 1.7). The bound survives cuts in `x` that are valid for
  the node's vertices (its Theorem 1.8(a)); with incumbent-based bound
  tightening on binaries (OBBT, probing, reduced-cost fixing) the node count is
  at least `kappa_tau/(N+1)` (its Theorem 1.8(c)).
- *Midpoint graph* `G^mid_tau`: vertices `a ~ b` iff `f((a+b)/2) < tau`;
  `omega(G^mid) <= kappa_tau` (its Lemma 1.5).
- *Condition C1 at `x°`*: every node with a single wrong fixing relative to
  `x°` has bound `>= OPT - eps` (strict C1: `> OPT`). If C1 holds and the
  incumbent value `OPT` is available when off-path nodes are examined (or
  strict C1 with best-bound search), every variable-branching tree has at
  most `2N+1` nodes, for any branching rule (its Lemma 5.1; the
  sparse-regression note's Lemma 1.2(b)). Under C1, `kappa_tau <= 2N+1` (its
  Proposition 5.2(b)).
- *Root exactness*: `R = OPT`.

### 0.4 Probabilistic tools

- (T1) `P(|Z| > t) <= e^{-t^2/2}` for `Z ~ N(0,1)`; hence
  `max_{i <= n} |Z_i| <= sqrt(2 log n + 2s)` with probability `>= 1 - e^{-s}`.
- (T2) (Laurent–Massart) `P(chi^2_d >= d + 2 sqrt(dx) + 2x) <= e^{-x}` and
  `P(chi^2_d <= d - 2 sqrt(dx)) <= e^{-x}`.
- (T3) (Davidson–Szarek) For a `d x m` matrix with iid `N(0,1)` entries,
  `d >= m`: `s_max <= sqrt d + sqrt m + t` and `s_min >= sqrt d - sqrt m - t`,
  each with probability `>= 1 - e^{-t^2/2}`.
- (T4) (Hoeffding) `P(|Bin(n,1/2) - n/2| >= s) <= 2 e^{-2 s^2/n}`.
- (T5) For `n >= k >= 1`: `k log(n/k) <= log C(n,k) <= k log(en/k)` and
  `log C(n,k) >= n h(k/n) - (1/2) log(8k)`, where
  `h(q) = -q log q - (1-q) log(1-q)`.

**Lemma 0.2 (Beta concentration).** Let `X ~ chi^2_s` and `Z ~ chi^2_{M-s}`
be independent, `0 <= s <= M`, and `Y = X/(X+Z)`. For `t in [0,1]`,
`P(|Y - s/M| >= t) <= 4 exp(-M t^2/64)`. If instead `s ~ Bin(n, 1/2)` with
`n <= M` (and `X, Z` conditionally as above), then
`P(|Y - n/(2M)| >= 2t) <= 6 exp(-M t^2/64)`.

*Proof.* Put `x = M t^2/64`. By (T2), with probability `>= 1 - 2e^{-x}`,
`X <= s + delta_1` and `Z >= M - s - delta_2`, where
`delta_1 = 2 sqrt(sx) + 2x <= M(t/4 + t^2/32)` and
`delta_2 = 2 sqrt((M-s)x) <= M t/4`. On this event

```
Y - s/M <= ((M-s) delta_1 + s delta_2) / (M (M + delta_1 - delta_2))
        <= (t/4 + t^2/32)/(1 - t/4) <= 3t/8 < t .
```

The lower tail is symmetric (`X >= s - 2 sqrt(sx)`,
`Z <= M - s + 2 sqrt((M-s)x) + 2x`). For the mixture, (T4) gives
`|s - n/2| <= tM` except with probability `2 e^{-2 t^2 M^2/n} <= 2e^{-2t^2 M}`. ∎

## 1. The root relaxation: never exact, gap about `N/2`

### 1.1 The sign condition at `x*` has no SNR threshold

**Proposition 1.1 (KKT at `x*`).** For every `M >= 1` and `rho > 0`, `x*`
minimizes `f` over the box iff `zeta_i >= 0` for all `i`, and

```
P(x* is a box minimizer) = 2^{-N}   exactly.
```

For `M >= N` the box minimizer is unique almost surely.

*Proof.* `f` is convex, so `x*` is a box minimizer iff
`d_i f(x*) (x_i - x*_i) >= 0` for all `x_i in [-1,1]` and all `i`, that is,
iff `x*_i d_i f(x*) <= 0`, that is, iff `zeta_i >= 0`. By Lemma 0.1,
given `w != 0` the `zeta_i = sqrt(rho/N) ||w|| g_i` are independent,
symmetric and continuous. For `M >= N`, `A` has full column rank almost
surely, so `f` is strictly convex. ∎

So the program's guess ("exactness iff every coordinate of the gradient at
`x*` has the right sign with margin", suggesting a threshold `rho ~ c log N`)
fails for the box relaxation: the gradient is `-2A'w`, its signs are fair
coins at every SNR, and scaling `rho` scales all its coordinates together.
There is no margin to gain. The `4 log N` threshold of the box relaxation in
the literature (Section 8) concerns the *box decoder* `sign(xhat)`, not
exactness of the relaxation.

**Theorem 1.2 (root exactness is exponentially rare).** Let `M >= N`,
`beta = M/N`. Then `R = OPT` iff the box minimizer is a vertex, and

```
P(R = OPT) <= sum_{k=0}^N C(N,k) 2^{k-N} (1 + 4 rho k/N)^{-M/2}
           <= ( (1 + 2 (1 + 4 rho)^{-beta/2}) / 2 )^N .
```

The right side tends to 0 exponentially whenever `(1+4rho)^{beta/2} > 2`
(for `beta = 1`: `rho > 3/4`), and it is `2^{-N} e^{O(N rho^{-beta/2})}`
for large `rho`.

*Proof.* If the unique box minimizer is a vertex, then `R = f(vertex) >= OPT
>= R`. Conversely, if `R = OPT = f(x_ML)`, then `x_ML` is a box minimizer,
hence the unique one. Fix a vertex `v = x^S`, `|S| = k`. By the argument of
Proposition 1.1, `v` is a box minimizer iff `v_i a_i'(y - Av) >= 0` for all
`i`, where `y - Av = w + 2 B_S 1 =: q`. For `i notin S` the condition reads
`b_i' q >= 0`; given `(w, B_S)`, the `b_i`, `i notin S`, are iid centred
Gaussian vectors, so these `N - k` conditions hold with conditional
probability exactly `2^{-(N-k)}`. For `i in S` the condition reads
`-b_i' q >= 0`; summing over `S` gives the necessary condition
`-<z, w> - 2||z||^2 >= 0` with `z = B_S 1 ~ N(0, (rho k/N) I_M)` independent
of `w`. For `lambda > 0`, taking expectations over `w` and then `z`
coordinatewise,

```
E exp(lambda(-<z,w> - 2||z||^2)) = (1 + 4 lambda a^2 - lambda^2 a^2)^{-M/2},   a^2 = rho k/N,
```

and `lambda = 2` gives `(1 + 4 rho k/N)^{-M/2}`. The `(w, B_S)`-measurable
condition and the conditionally independent ones multiply, and a union bound
over `v` gives the first inequality. For the second, concavity of `log`
gives `log(1 + 4 rho k/N) >= (k/N) log(1 + 4 rho)`, so each term is at most
`C(N,k) 2^{k-N} (1+4rho)^{-beta k/2}`, and the binomial theorem finishes. ∎

Check (`code/exp_root.py`, part b; 20000 trials per cell, `N = 2..8`,
`beta = 1, 2`, `rho = 1..64`): the frequency of `x*` being the box minimizer
matches `2^{-N}` within sampling error in every cell, and the frequency of a
vertex minimizer never exceeds the bound (Section 7.1).

### 1.2 The law of the projection onto a Gaussian cone

The law below is known in substance. The expected conic intrinsic volumes of
the cone spanned by `n <= d` iid Gaussian vectors in `R^d` are
`E v_k = C(n,k) 2^{-n}` (Hug–Schneider, DCG 2016, via the Cover–Efron cone;
stated as Lemma 5.1 and formula (3.5) of Godland–Kabluchko–Thäle, Discrete
Analysis 2022). Given the face dimension, the squared lengths of the
projections onto the cone and its polar are independent `chi^2_k` and
`chi^2_{d-k}` (the master Steiner formula of McCoy–Tropp, DCG 2014; the
chi-bar-squared law of order-restricted inference, Kudô 1963, Shapiro 1985).
We give a self-contained derivation because we need the per-face form for a
fixed vector, and because it shows that part (a) needs only sign symmetry
(this extension was pointed out in the easy review).

**Theorem 1.3 (projection onto a random cone).** Let `g_1, ..., g_n` be random
vectors in `R^M`, `n <= M`, `K = cone{g_1, ..., g_n}`, and let `v != 0` be
fixed (or random and independent of the `g_j`). Almost surely `Pi_K(v)` lies
in the relative interior of a unique face `F_S = cone{g_j : j in S}`.

- (a) Suppose the `g_j` are almost surely linearly independent and in general
  position with respect to `v`, and their joint law is invariant under
  changing the sign of any single `g_j`. Then the face index `S` is uniform
  over all `2^n` subsets of `[n]`; in particular `|S| ~ Bin(n, 1/2)`.
- (b) If the `g_j` are iid `N(0, I_M)`, then in addition, given `|S| = s`,
  `||Pi_K v||^2/||v||^2 ~ Beta(s/2, (M-s)/2)`.
- (c) If moreover `v ~ N(0, I_M)`, then `||Pi_K v||^2 ~ chi^2_{|S|}`, a
  chi-square with `Bin(n, 1/2)` degrees of freedom; its mean is `n/2` and its
  variance `5n/4`.

Part (b) needs rotation invariance: the easy review found the Beta law
rejected for iid Laplace and for correlated Gaussian columns, while the face
law (a) holds for both (also `code/check_revision.py`, part A).

*Proof.* Let `L_S = span{g_j : j in S}`. The point `p = Pi_K(v)` is
characterized by `p in K`, `v - p ⊥ p` and `<v - p, g_j> <= 0` for all `j`. If
`p = sum_{j in S} alpha_j g_j` with all `alpha_j > 0`, then
`0 = <v-p, p> = sum_S alpha_j <v-p, g_j>` forces `<v - p, g_j> = 0` on `S`,
so `p = P_{L_S} v`. Hence `p in relint F_S` iff

- (i) `P_{L_S} v` has positive coordinates in the basis `(g_j)_{j in S}`, and
- (ii) `<g_j, P_{L_S}^perp v> < 0` for all `j notin S`

(ties have probability 0 under general position).

(a) Fix the vectors and a subset `S`, and consider the `2^n` cones
`K_eps = cone{eps_j g_j}`, `eps in {-1,1}^n`. Changing signs does not change
`L_S`. Condition (i) for `K_eps` holds for exactly one choice of `eps` on `S`
(the signs of the coordinates of `P_{L_S} v`, all nonzero by general
position), and condition (ii) holds for exactly one choice of `eps` off `S`
(`eps_j = -sign <g_j, P_{L_S}^perp v>`). So, deterministically, exactly one
of the `2^n` cones `K_eps` has projection face `S`:
`sum_eps 1{face(K_eps) = S} = 1`. By sign invariance all `2^n` terms have the
same probability, so `P(face = S) = 2^{-n}`.

(b), (c) For Gaussian vectors the law of `(g_j)` is invariant under
rotations, so `||Pi_K v||/||v||` has the same law as `||Pi_K xi||/||xi||`
with `xi ~ N(0, I_M)` independent of the `g_j`. Given the `g_j`, the
components `P_{L_S} xi` and `P_{L_S}^perp xi` are independent Gaussian
vectors in their subspaces, and the event `face = S` depends only on their
directions ((i) and (ii) are invariant under positive scaling of each
component). A Gaussian vector's norm is independent of its direction, so given
`face = S`, `(||P_{L_S} xi||^2, ||P_{L_S}^perp xi||^2)` are independent
`chi^2_{|S|}` and `chi^2_{M-|S|}`. This gives (b) and (c); the moments follow
from `E chi^2_s = s`, `Var chi^2_s = 2s` and `Var |S| = n/4`. ∎

In particular, the number of active coordinates of a nonnegative
least-squares fit of pure noise on `n <= M` Gaussian columns is `Bin(n, 1/2)`,
a corollary of the known intrinsic volumes. What is used below is the
per-node form: at every B&B node the residual `v` of (0.1) is independent of
the free columns, so (a)–(b) apply node by node.

### 1.3 The root gain

Let `G = W - R` (the *root gain*) and let `u°(rho)` be the nonnegative
least-squares (NNLS) solution `argmin_{u >= 0} ||w + B u||^2` (upper bounds
dropped). Put `G_inf = W - ||w + B u°||^2 = ||Pi_{-cone(B)} w||^2`.

**Corollary 1.4.** Let `M >= N`.

- (a) `G <= G_inf`, and `G_inf ~ chi^2` with `Bin(N, 1/2)` degrees of
  freedom, for every `rho`. W.h.p. `G_inf = N/2 + O(sqrt(N log N))`, and
  `(G_inf - N/2)/sqrt(5N/4)` is asymptotically standard normal.
- (b) `G = G_inf` iff `max_j u°_j(rho) <= 2`.
- (c) `u°(rho) = u°(1)/sqrt(rho)`. Hence `G = G_inf` exactly for
  `rho >= rho_box := (max_j u°_j(1))^2/4`, and `G` is nondecreasing in `rho`.
- (d) If the box decoder succeeds at `rho_0` (that is,
  `sign(xhat) = x*` for the box minimizer `xhat`), then `rho_box < rho_0/4`.

*Proof.* (a) The box `[0,2]^N` lies in the orthant, so the box minimum is at
least the NNLS minimum. `cone(B) = cone(h~_1, ..., h~_N)` is a Gaussian cone
and `-w` is an independent standard Gaussian, so Theorem 1.3(c) applies. The
concentration follows from (T2) and (T4), and the CLT from the mixture
representation. (b) If `u° <= 2`, it is feasible for the box problem and
attains the lower bound. Conversely, if `G = G_inf`, the box minimizer
attains the NNLS minimum and, by strict convexity, equals `u°`. (c) `B` scales
as `sqrt(rho)`; substitute `u' = sqrt(rho) u`. The box value is the minimum
over `[0,2]^N`, and scaling up `B` enlarges the set `{B u}`, which contains
`0`. (d) If `sign(xhat) = x*` then the box minimizer has all `u_j < 1 < 2`,
so it is also the NNLS minimizer (its KKT conditions for the box are those
of NNLS). So `max u°(rho_0) < 1`, and (c) gives
`max u°(1) < sqrt(rho_0)`. ∎

**Lemma 1.5 (leave-one-out bound for NNLS).** Let `C in R^{M x n}` have
smallest singular value `sigma > 0`, `v in R^M`, `u° = argmin_{u>=0}
||v + C u||^2`, and for each `j` let `u~` minimize over `{u >= 0, u_j = 0}`
with residual `r~_j = v + C u~`. Then

```
u°_j <= 2 (-c_j' r~_j)_+ / sigma^2 .
```

*Proof.* Let `Q(u) = ||v + Cu||^2`. Since `Q` is quadratic,
`Q(u°) = Q(u~) + grad Q(u~)'(u° - u~) + ||C(u° - u~)||^2`. The KKT
conditions of the restricted problem give, for `k != j`, `c_k' r~_j >= 0`
with equality when `u~_k > 0`; with `u°_k >= 0` this makes each term
`2 c_k' r~_j (u°_k - u~_k)` nonnegative. So
`0 >= Q(u°) - Q(u~) >= 2 c_j' r~_j u°_j + sigma^2 (u°_j)^2`, because `u~` is
feasible for the full problem and `||C(u° - u~)||^2 >= sigma^2 (u°_j)^2`. ∎

**Corollary 1.6 (box inactivity at the root).** Let `beta > 1` be fixed and
`rho >= (1+eps) 6 beta log N/(sqrt(beta) - 1)^4`. Then w.h.p.
`max_j u°_j(rho) <= 2`, so `G = G_inf`. For `beta >= 1`, the same conclusion
holds for `rho >= (1+eps) log N/(2 beta - 1)` if one takes as input the
box-decoder theorem of Hu–Lu (Section 8): it gives success at
`rho_0 = (1+eps) 4 log N/(2beta - 1)`, and Corollary 1.4(d) applies.

*Proof.* Apply Lemma 1.5 with `C = B`, `v = w`. The residual `r~_j` depends
on `w` and the columns other than `b_j`, so given it,
`b_j' r~_j ~ N(0, (rho/N)||r~_j||^2)`, and `||r~_j|| <= ||w||` (take
`u = 0`). By (T1) and a union bound, `|b_j' r~_j| <= sqrt(rho/N) ||w||
sqrt(6 log N)` for all `j` with probability `>= 1 - 1/N^2`. By (T3),
`sigma_min(B) >= sqrt(rho/N)(sqrt M - sqrt N - sqrt(2 log N))`, and
`||w|| <= sqrt(M)(1 + o(1))`. So
`u°_j <= 2 sqrt(6 beta log N/rho)(1 + o(1))/(sqrt(beta) - 1)^2 <= 2`. In
Hu–Lu's normalization (`A_ij ~ N(0, 1/N)`, noise variance `1/rho`,
`delta = beta`) the box decoder succeeds w.h.p. when
`rho (beta - 1/2)/(2 log N) -> alpha* > 1`, inside their range
`rho = O(log^2 N)`. ∎

**Theorem 1.7 (the root gap is linear in `N`).** Let `beta >= 1` be fixed.

- (a) For `rho >= (1 + eps) 2 beta log N/(1 + 2beta)^2`, w.h.p.
  `G >= (beta/(1 + 2beta) - o(1)) N` (for `beta = 1`: `N/3`). The condition
  holds when `rho >= (log N)/4` and when `rho beta >= (2+eps) log N`.
- (b) Under the conditions of Corollary 1.6, w.h.p. `G = G_inf = N/2 +
  O(sqrt(N log N))`.
- (c) If `rho beta >= (2+eps) log N`, then w.h.p. `OPT = W` (Theorem 2.2), so
  the root gap `OPT - R = G` lies in `[(beta/(1+2beta) - o(1)) N, (1/2 +
  o(1)) N]`, and equals `(1/2 + o(1)) N` under (b). The relative gap
  `(OPT - R)/OPT` tends to `1/(2 beta)` in case (b).

*Proof of (a).* Use the explicit point `u = tau s` with
`s_j = (-g_j)_+` (Lemma 0.1). Then `<w, B u> = -tau sqrt(rho/N) ||w|| Q`
with `Q = ||s||^2`, and
`||B u||^2 = tau^2 (rho/N)(Q^2 + X)`, where `X = ||H^perp s||^2` and
`H^perp = (h_j^perp)`. Minimizing `F(tau s)` over `tau` gives
`tau* = sqrt(N/rho) ||w|| Q/(Q^2 + X)` and

```
F(tau* s) = W X/(Q^2 + X),       G >= W Q^2/(Q^2 + X),                    (1.1)
```

provided `tau* max_j s_j <= 2`. Given `s`, `X ~ Q chi^2_{M-1}` (Lemma 0.1),
and `Q` is a sum of `N` iid variables with mean `1/2`, so w.h.p.
`Q = N/2 + O(sqrt(N log N))` and `X = Q (M-1)(1 + O(sqrt(log N/N)))`. Then
`G >= W Q/(Q + (M-1)(1+o(1))) = (W/(1 + 2beta))(1 - o(1))` and
`W = M(1 + o(1))`. Feasibility: `tau* = (2 sqrt(beta)/((1 + 2beta)
sqrt(rho)))(1 + o(1))` and `max_j s_j <= sqrt(2 log N)(1 + o(1))`, so
`tau* max s_j <= 2` when `rho >= 2 beta log N (1+o(1))/(1+2beta)^2`. This
holds for `rho >= (log N)/4` because `2beta/(1+2beta)^2 <= 2/9`, and for
`rho beta >= (2+eps) log N` because `2/beta >= 2beta/(1+2beta)^2`. (b) is
Corollaries 1.4 and 1.6. (c) combines (a), (b) and Theorem 2.2(a); the
hypothesis of (c) implies that of (a). ∎

The explicit point (1.1) is the "correlation witness": each coordinate moves
into the box in proportion to how strongly the objective decreases along it.
It recovers the fraction `1/(1+2beta)` of `W`; the optimal NNLS fit recovers
`1/(2 beta)`. For the box relaxation the root gap is a constant fraction of
`OPT` at *every* SNR `rho >= (log N)/4`. It is not a small-gap relaxation in
the sense needed by gap-to-tree-size arguments (Dey–Dubey–Molinaro), and
Sections 3–5 show that it is not rescued by branching either, except when
`rho` is linear in `N`.

Numerically (Section 7.1, 200 instances per cell for `N = 50, 200` and 40
for `N = 800`, `beta = 1, 2`, `rho` from `2 log N` to `N/4`), the mean of
`G/N` is 0.497–0.509 and its variance divided by `N` is 1.17–1.30 (law:
0.5 and 1.25; one cell with 40 samples gave 1.81); the number of active NNLS
coordinates has mean `N/2` and variance close to `N/4`; and `G = G_inf` in
3519 of the 3520 instances, including all but one at `rho = 2 log N` (the
exception has `N = 50`, `beta = 1`).

## 2. Maximum likelihood, and midpoints above `8 log N`

### 2.1 A Chernoff bound for a fixed direction

**Lemma 2.1.** For every fixed `c in R^N \ {0}` and `s >= 0`,

```
P( F(c) <= W - s ) <= e^{-s/4} (1 + rho ||c||^2/(4N))^{-M/2} .
```

*Proof.* `B c = sqrt(rho/N) H~ c = a z` with `a^2 = rho ||c||^2/N` and
`z ~ N(0, I_M)` independent of `w`, and `F(c) - W = 2a<z,w> + a^2||z||^2`.
For `lambda > 0`, coordinatewise,
`E exp(-lambda(2a z w + a^2 z^2)) = E_z exp((2 lambda^2 - lambda) a^2 z^2)
= (1 - 2(2lambda^2 - lambda) a^2)^{-1/2}`. At `lambda = 1/4` this is
`(1 + a^2/4)^{-1/2}`; Markov's inequality gives the claim. ∎

For vertices, `c = 2 1_S` and the factor is `(1 + rho |S|/N)^{-M/2}`. For
midpoints of two vertices, `c in {0,1,2}^N` and `||c||^2 = n_1 + 4 n_2`,
where `n_1` and `n_2` count the entries equal to 1 and 2.

### 2.2 When is `x*` the ML point?

**Theorem 2.2 (ML).** Let `beta >= 1` be fixed.

- (a) If `rho beta >= (2+eps) log N`, then w.h.p. `x*` is the unique ML point,
  so `OPT = W`. For `beta = 1` this first-order achievability is due to
  Hansen–Hassibi–Dimakis–Xu (2009) and Hassibi et al. (2014, Lemma IV.2:
  `rho > 2 log N + f(N)`, `f -> inf`), as Papailiopoulos (Appendix A) states;
  we include the short first-moment proof for general `beta`.
- (b) If `rho beta = c log N` with `c > 0` fixed, then for every `delta > 0`,
  w.h.p. `W - OPT <= N^{1 - c/2 + delta}`.
- (c) For every `rho > 0`, w.h.p. `W - OPT <= 4 N log(1 + e^{-0.148 beta rho})
  + 4 log N`.
- (d) (Converse.) If `c0 <= rho beta <= (2 - eps) log N` for a constant
  `c0 > 0`, then w.h.p. some one-bit neighbour `x^{i}` has `f(x^{i}) < W`, so
  `x*` is not ML. For `beta = 1` this is Papailiopoulos' Theorem 2.1(b), which
  gives the sharper range `rho <= 2 log N - log log N - s_N`. Unlike (a), this
  direction is not a first-moment bound: it uses the conditional independence
  of the `N` one-bit events given `w`.

*Proof.* By Lemma 2.1 and a union bound,

```
P(W - OPT >= s) <= e^{-s/4} Sigma,     Sigma = sum_{k=1}^N C(N,k) (1 + x_k)^{-M/2},   x_k = rho k/N.   (2.1)
```

Split the sum at `x_k = x0`.

*Small `x_k <= x0`.* Then `log(1 + x) >= x(1 - x0/2)`, so the term is at most
`(N e^{-(beta rho/2)(1 - x0/2)})^k / k!`, and the partial sum is at most
`exp(N e^{-(beta rho/2)(1 - x0/2)}) - 1`.

*Large `x_k > x0`.* Write `t = k/N = x_k/rho in (x0/rho, 1]`. By (T5) the
logarithm of the term is at most `N[t log(e/t) - (beta/2) log(1 + rho t)]`.
If `rho -> inf`, this is at most `-c N` uniformly in `t`: for `t <= t1`
(with `t1 log(e/t1) <= (1/4) log(1+x0)`) the bracket is at most
`-(1/4) log(1 + x0)`, and for `t in [t1, 1]` it is at most
`1 - (1/2) log(1 + rho t1) -> -inf`. So the large part is at most `N e^{-cN}`.

(a) Take `s = 0` and `x0 = eps/4`, `eps <= 1`. Since
`(1 + eps/2)(1 - eps/8) >= 1 + eps/4`, the small part is at most
`sum_k N^{-eps k/4} -> 0`. (b) Take `x0` small, so the small part is at most
`exp(N^{1 - (c/2)(1 - x0/2)})`, and `s = 4 N^{1 - (c/2)(1 - x0/2)} + 4 log N`;
then the bound (2.1) is `O(1/N)`. (c) Use instead, for `x <= 7`,
`log(1+x) >= x log(8)/7 >= 0.297 x`, which bounds the small part (now
`x_k <= 7`) by `exp(N e^{-0.148 beta rho})`; for `x_k > 7`,
`t log(e/t) - (beta/2) log(1 + rho t) <= 1 - (1/2) log 8 < -0.039`. Take
`s = 4 N log(1 + e^{-0.148 beta rho}) + 4 log N`.
(d) Given `w` with `W = M(1 + o(1))`, the events
`E_i = {zeta_i + ||b_i||^2 < 0}` are conditionally independent (Lemma 0.1:
each depends only on `(g_i, h_i^perp)`), and
`E_i` contains `{g_i in [-2 sqrt(rho beta), -(1+2eta) sqrt(rho beta)],
||h_i^perp||^2 <= M(1+eta)}` for large `N`: on this set
`zeta_i + ||b_i||^2 <= rho beta(-(1+2eta)(1 - o(1)) + (1+eta) + o(1)) < 0`
(the `g_i^2` term is `O(rho^2/N) = o(rho)`). Its probability is at least
`N^{-(1 - eps/2)(1+2eta)^2 + o(1)}` if `rho beta -> inf`, and a positive
constant if `rho beta` stays bounded; either way it is `>> 1/N` for small
`eta`, so `P(no E_i | w) = (1 - P(E_1 | w))^N <= exp(-N P(E_1 | w)) -> 0`. ∎

At the SNRs where the tree-size theorems below are stated
(`rho beta >= (2+eps) log N`), `OPT = f(x*)` w.h.p. Below `2 log N / beta`
the ML point differs from `x*`, but only slightly in value: by
`N^{1 - c/2 + o(1)} = o(N)` at `rho beta = c log N` (part (b)), and by at most
`4 N e^{-0.148 beta rho} + O(log N)` at fixed `rho` (part (c)). This is what the
hard-side theorems need.

### 2.3 Midpoint conflicts disappear above `8 log N`

The midpoint of two distinct vertices is a point of `{-1,0,1}^N` with at
least one zero coordinate, that is, `u = c` with `c in {0,1,2}^N` having at
least one entry 1. So `G^mid_tau` has an edge iff such a `c` has
`F(c) < tau`: midpoint conflicts are exactly "ternary points better than the
threshold". Coordinate by coordinate, a half move of `i` changes `F` by
`2 zeta_i + ||b_i||^2 ~ 2 sqrt(rho beta) g_i + rho beta`, which is negative
iff `g_i < -sqrt(rho beta)/2`; there are about `N Phibar(sqrt(rho beta)/2)`
such coordinates. This suggests the threshold `rho beta = 8 log N`, four
times the ML threshold, and the first-moment bound confirms it.

**Theorem 2.3 (no midpoint conflicts above `8 log N`).** If
`rho beta >= (8 + eps) log N` with `beta >= 1` fixed, then w.h.p. every
`c in {0,1,2}^N` with at least one entry 1 has `F(c) > W = OPT`. Hence, for
every `eps' >= 0`, the midpoint graph `G^mid_{OPT - eps'}` on the vertices has
no edges, and its clique number is 1.

*Proof.* `OPT = W` w.h.p. by Theorem 2.2(a). By Lemma 2.1 with `s = 0`, the
expected number of bad `c` is at most
`sum_{n_1 >= 1, n_2 >= 0} C(N, n_1) C(N - n_1, n_2) (1 + rho(n_1 + 4n_2)/(4N))^{-M/2}`.
Let `n = n_1 + n_2`. If `rho n/N <= x0`, then `x := rho(n_1 + 4n_2)/(4N)
<= x0` and `log(1 + x) >= x(1 - x0/2)`, so the term is at most
`N^{n_1 + n_2} exp(-(beta rho/8)(1 - x0/2)(n_1 + 4 n_2))/(n_1! n_2!)`; with
`beta rho >= (8+eps) log N` and small `x0` this is at most
`N^{-(eps/16) n_1 - 3 n_2}/(n_1! n_2!)`, and these terms sum to `o(1)`.
If `rho n/N > x0`, bound the number of `c` with `n` nonzero entries by
`C(N, n) 2^n` and the factor by `(1 + rho n/(4N))^{-M/2}`; with `t = n/N`
the logarithm of the total is at most
`N[t log(2e/t) - (beta/2) log(1 + rho t/4)] + log N <= -cN` for large `N`,
exactly as in the proof of Theorem 2.2. ∎

The segment graph is not empty in this regime: the segment from `x*` to
`x^{i}` enters `{f < W}` whenever `zeta_i < 0`, which happens for about half
of the coordinates. So midpoint-conflict arguments (cliques or colourings of
`G^mid`) certify nothing above `8 log N`, even though (Section 4) the class
number stays superpolynomial up to `rho = o(N)`. Whether the segment graph's
chromatic number stays bounded above `8 log N` is not analysed; the hard
review found `chi(G^seg) = 2` in most small high-SNR instances.

Sampling the exact single-coordinate law of Lemma 0.1 (Section 7.4) places
the 50% point of "some half move improves on `x*`" at
`rho beta / log N ~ 6.4-6.8` for `N = 10^4 - 10^5`, and the ML one-bit
failure at `~ 1.6-1.8`, consistent with first-order constants 8 and 2 and the
`-log log N` corrections. On real instances (`N = 200, 800`, 20 seeds per
cell), a conflicting pair of half moves without a conflicting single half
move occurred in 2 of 240 instances.

## 3. Condition C1: linear trees need `rho` linear in `N`

Let `theta_c(beta) = 1/(4(2 beta - 1))` (`= 1/4` for square systems).

**Theorem 3.1 (C1 threshold).** Let `beta >= 1`, `eps in (0,1)` and
`theta > 0` be fixed, and `rho = theta N`. (The proofs of (b)–(d) use
`theta N >> log N`: for `u°_j -> 0` in (b), `tau_i max_j s_j -> 0` in (c),
`rho' >> log N` in (d), and `OPT = W` in all three.)

- (a) If `theta >= (1 + eps) theta_c`, then w.h.p. every node with a single
  wrong fixing (`u_i = 2`, everything else free) has bound at least
  `W + (eps/4) N`. So strict C1 holds at `x*`, `x*` is the unique optimum,
  every variable-branching tree has at most `2N + 1` nodes (any branching
  rule; incumbent `OPT` available, or best-bound search), and
  `kappa_{OPT - eps'} <= 2N + 1`.
- (b) If `beta > 1` and `theta <= (1 - eps) theta_c`, then w.h.p. every node
  with a single wrong fixing has bound at most `OPT - (eps/4) N`, where
  `OPT = W`.
- (c) If `theta <= (1 - eps)/(8 beta)` (any `beta >= 1`), then w.h.p. every
  node with a single wrong fixing has bound at most `OPT - c_eps N`.
- (d) (`beta = 1`, with the Hu–Lu input of Corollary 1.6.) If `beta = 1` and
  `theta <= (1 - eps)/4`, then for each fixed index `i`, w.h.p. the node with
  the single wrong fixing `u_i = 2` has bound at most `OPT - (eps/4) N`. So C1
  fails w.h.p.

So the C1 threshold is `rho = (1 + o(1)) N/(4(2beta - 1))`: unconditionally
for `beta > 1`, and for `beta = 1` with the same Hu–Lu input that
Corollary 1.6 uses (part (d), suggested by the easy review). Without that
input, the `beta = 1` threshold lies in `[N/8, N/4]`. Conjecture 3.3 concerns
the stronger "every node fails" form of (b) for `beta = 1`.

In all statements about tree size, "at most `2N+1` nodes" assumes that the
incumbent value `OPT` is available whenever an off-path node is examined, or
best-bound search with strict C1 (Section 0.3). Without this, depth-first
search can dive into an off-path child with nothing to prune against.

The mechanism is visible from Theorem 1.3. Forcing `x_i = -x*_i` adds
`2 b_i` to the residual, which costs `4||b_i||^2 ~ 4 rho beta` at fixed other
coordinates. The other coordinates absorb the fraction `(N-1)/(2M)` of the
new residual `v_i = w + 2 b_i` (Theorem 1.3, since `v_i` is independent of the
other columns), while the root had already absorbed the same fraction of `w`.
The node bound is about `(W + 4 rho beta)(1 - 1/(2beta))`, and C1 needs this
to exceed `W ~ beta N`.

*Proof of (a).* Fix `i` and let `v_i = w + 2 b_i`. Dropping the upper bounds
lowers the node value, so by (0.1) and Theorem 1.3 (with `n = N - 1 <= M`
and `v_i` independent of `B_{-i}`),

```
r_i >= dist^2(v_i, -cone(B_{-i})) = ||v_i||^2 (1 - Y_i),
```

where `Y_i` has the Beta mixture law of Theorem 1.3. By Lemma 0.2 with
`t = sqrt(128 log N/M)` and a union bound over `i`, w.h.p.
`Y_i <= 1/(2beta) + O(sqrt(log N/N))` for all `i`. By Lemma 0.1, (T1) and
(T2), w.h.p. simultaneously for all `i`: `W = M(1 + o(1))`,
`zeta_i >= -2 sqrt(rho beta log N)(1 + o(1))`, and
`||b_i||^2 >= (rho/N)||h_i^perp||^2 = rho beta (1 - o(1))`. Hence
`||v_i||^2 = W + 4 zeta_i + 4||b_i||^2 >= W + 4 rho beta (1 - o(1))`,
because `sqrt(rho log N) = o(rho)` when `rho = theta N`. Then

```
r_i - W >= (W + 4 rho beta(1 - o(1)))(1 - 1/(2beta) - o(1)) - W
        = 2 rho (2beta - 1) - W/(2beta) - o(N) = (N/2)(theta/theta_c - 1) - o(N),
```

which is at least `(eps/2) N - o(N)`. Every vertex other than `x*` lies in some
single-wrong-fixing node, so `f > W` there: `x*` is the unique optimum and
`OPT = W`. The tree bound is the path lemma and the class bound is
Proposition 5.2(b) of the integer-core note (Section 0.3). ∎

*Proof of (b).* We first show that the node NNLS problems are box-inactive.
Apply Lemma 1.5 to `C = B_{-i}` and `v = v_i`: for `j != i`,
`u°_j <= 2(-b_j' r~_{ij})_+ / sigma_min(B_{-i})^2`, where `r~_{ij}` is the
residual of the NNLS problem without columns `i, j`. It depends on `w`, `b_i`
and the columns other than `b_i, b_j`, so it is independent of `b_j`, and
`||r~_{ij}|| <= ||v_i||`. By (T1) and a union bound over the `N(N-1)` pairs,
w.h.p. `|b_j' r~_{ij}| <= sqrt(rho/N)||v_i|| sqrt(6 log N)` for all pairs. By
(T3), `sigma_min(B_{-i}) >= sigma_min(B) >= sqrt(rho)(sqrt(beta) - 1 - o(1))`,
and `||v_i||^2 <= 3 beta N (1 + 4 theta)` w.h.p. Hence

```
u°_j <= 2 sqrt(18 beta (1 + 4theta) log N / (theta N)) (1 + o(1)) / (sqrt(beta) - 1)^2 -> 0,
```

so the upper bounds are inactive and `r_i = ||v_i||^2 (1 - Y_i)` exactly. Now
use the lower tail of Lemma 0.2 (`Y_i >= 1/(2beta) - O(sqrt(log N/N))`) and the
upper bounds `W <= M(1 + o(1))`, `zeta_i <= 2 sqrt(rho beta log N)(1+o(1))`,
`||b_i||^2 <= rho beta(1 + o(1))`:

```
r_i - W <= 2 rho (2beta - 1) - W/(2beta) + o(N) = (N/2)(theta/theta_c - 1) + o(N) <= -(eps/2) N + o(N).
```

Finally `OPT = W` w.h.p. by Theorem 2.2(a). ∎

*Proof of (c).* We use the correlation witness (1.1) at each node. For node
`i`, let `g^(i)_j = h~_j' v_i/||v_i||` (`j != i`), which are iid `N(0,1)`
given `v_i` (Lemma 0.1 with `v_i` in place of `w`), `s_j = (-g^(i)_j)_+`,
`Q_i = ||s||^2`, `X_i = ||H^perp s||^2`. As in the proof of Theorem 1.7(a),

```
r_i <= ||v_i||^2 X_i/(Q_i^2 + X_i) <= ||v_i||^2 (2beta/(1 + 2beta)) (1 + o(1))
```

uniformly in `i` w.h.p., because `Q_i = (N/2)(1 + o(1))` and
`X_i = Q_i (M-1)(1 + o(1))` for all `i` by (T2) and a union bound. The
witness is feasible: its step is `tau_i <= sqrt(N/rho)||v_i||/Q_i =
O(N^{-1/2})` and, by (T1) and a union bound over the `N(N-1)` pairs,
`max_{i,j} s^{(i)}_j <= sqrt(6 log N)` w.h.p., so `tau_i max_j s_j -> 0`. With
`||v_i||^2 <= beta N(1 + 4theta) + o(N)`,
`r_i <= (2beta/(1+2beta)) beta N (1 + 4theta) + o(N)`, which is below
`W - c_eps N = beta N - c_eps N + o(N)` iff `8 beta theta < 1`, with room
`c_eps > 0` when `theta <= (1-eps)/(8beta)`. `OPT = W` by Theorem 2.2(a). ∎

*Proof of (d).* Fix `i`. Since `rho/N = theta`, `b_i = sqrt(theta) h~_i` and
`v_i = w + 2 b_i ~ N(0, (1 + 4theta) I_M)` exactly, independent of
`B_{-i} = sqrt(theta) H~_{-i}`. Put `c^2 = 1 + 4theta` and `xi = v_i/c`. Then

```
r_i = c^2 min{ ||xi + sqrt(rho'/N') H~_{-i} u||^2 : u in [0,2]^{N'} },   N' = N - 1,   rho' = theta (N-1)/(1 + 4theta),
```

which is `c^2` times the root box value, in error coordinates, of an instance
of the model with `N'` unknowns, `M = N' + 1` observations, noise `xi`,
matrix `H' = H~_{-i}` and `x*' = 1`. Let `U` be the largest coefficient of the
NNLS fit of `-xi` on `H~_{-i}/sqrt(N')`. By Corollary 1.4(c), node `i` is
box-inactive iff `U <= 2 sqrt(rho')`. Apply Hu–Lu to the same `(H', xi)` at
`rho_0 = (1+eps) 4 log N'/(2beta' - 1)`, `beta' = M/N' -> 1`; their
hypotheses hold (`delta -> 1 > 1/2`, `sigma^2 log^2 N = log^2 N/rho_0 ->
inf`). So the box decoder succeeds at `rho_0` w.h.p., and Corollary 1.4(d)
gives `U < sqrt(rho_0) = O(sqrt(log N))`. Since `rho' = Theta(N)`, node `i` is
box-inactive w.h.p., and `r_i = ||v_i||^2 (1 - Y_i)`. By Lemma 0.2,
`Y_i >= (N-1)/(2M) - o(1)` w.h.p. (`N - 1` free columns), and `||v_i||^2 = c^2 chi^2_M <= (1 + 4theta) N (1 + o(1))`,
`W >= N(1 - o(1))`. So

```
r_i - W <= (1 + 4theta)(N/2)(1 + o(1)) - N(1 - o(1)) = (N/2)(4theta - 1) + o(N) <= -(eps/2) N + o(N),
```

and `OPT = W` w.h.p. by Theorem 2.2(a). ∎

The single-node reduction also shows what Conjecture 3.3 amounts to: node
`i` is box-inactive iff `U <= 2 sqrt(theta (N-1)/(1 + 4theta))` (at
`theta = 1/4`: `U <= sqrt((N-1)/2)`), where `U` is the largest NNLS
coefficient of a pure-noise fit on `N - 1` Gaussian columns. "Every node
fails" follows, by a union bound, from `P(U > c sqrt N) = o(1/N)` for each
fixed `c > 0`. This tail bound is sufficient but not necessary: the `N` node
events share `w` and all but one column and can be strongly positively
correlated. Hu–Lu's rate (`polylog N/N^{1/5}`) does not give it. The easy review measured `U`
directly: its median grows slowly (3.5, 3.9, 4.1, 4.5, 4.8 for
`N = 100, 200, 400, 800, 1600`), and its sample maximum divided by `sqrt N`
is 0.79, 0.53, 0.30, 0.20, 0.16 (2000 down to 30 samples), against the
threshold 0.71 at `theta = 1/4`.

**Corollary 3.2 (linear trees versus root exactness).** For
`rho >= (1 + eps) N/(4(2beta-1))`, w.h.p. every variable-branching tree with
the box relaxation has at most `2N + 1` nodes, for any rule, when the
incumbent value `OPT` is available as off-path nodes are examined (or with
best-bound search), while the root relaxation is
exact with probability at most `((1 + 2(1 + 4rho)^{-beta/2})/2)^N`
(Theorem 1.2) and has gap about `N/2` (Theorem 1.7). So C1 lies strictly
below root exactness, which never occurs; but the C1 threshold is linear in
`N`, not logarithmic.

**Conjecture 3.3 (square systems, every node).** For `beta = 1` and fixed
`theta > 0`, w.h.p. all `N` single-fixing NNLS problems are box-inactive when
`rho = theta N`. By the single-node reduction above, this is implied by
`P(U > c sqrt N) = o(1/N)` for every fixed `c > 0`. Then Theorem 3.1(b) holds
for `beta = 1`: below `(1-eps) N/4` every single wrong fixing has bound below
`OPT - (eps/4) N`. The threshold itself needs only Theorem 3.1(d); the
"every node" form is used in Conjecture 4.5.

*Evidence.* The largest NNLS coefficient over the single-fixing nodes
decreases with `N` (at `theta = 1/4`: mean 1.62, 1.01, 0.80, 0.56, 0.47 for
`N = 50, 100, 200, 400, 800`, 4 instances and 20–25 nodes each; 14 of 100
nodes exceed 2 at `N = 50`, none from `N = 100` on;
`code/check_node_inactivity.py`, Section 7.2), and in the C1 experiment every
one of the `N` node problems in every instance (`N = 100–800`) was
box-inactive. The
leave-one-out Lemma 1.5 fails for square matrices because
`sigma_min(B) ~ sqrt(rho)/N`.

*Finite-`N` behaviour.* The proofs lose `4 min_i zeta_i ~
-4 sqrt(2 rho beta log N)` in `||v_i||^2`. Keeping this term gives the
second-order prediction: C1 holds iff
`2(2beta - 1)(rho - sqrt(2 rho log N/beta)) >~ N/2`. For `beta = 1`,
`N = 400` this gives `theta ~ 0.35`; for `beta = 2`, `N = 400`,
`theta ~ 0.13`. These match the observed transitions (Section 7.2), which
therefore sit well above the asymptotic `theta_c` at practical sizes.

## 4. Between `log N` and `N`: trees of size `exp(Theta((N/rho) log rho))`

In this section `rho -> inf` and `rho = o(N)` (Theorem 4.3 also covers fixed
`rho >= 71`). Both bounds rest on the exact law of Theorem 1.3 applied to the
node formula (0.1): a node whose wrong fixings form `Wr` and whose free set
has `n` elements has bound at least `||v||^2 (1 - Y)` with
`v = w + 2 B_Wr 1`, `||v||^2 = W + D_Wr`, `D_Wr = f(x^Wr) - W`, and
`Y ~ n/(2M)`. It is pruned (roughly) iff
`D_Wr >= W Y/(1 - Y) ~ beta N n/(2M - n)`: the excess of the vertex `x^Wr` must
pay for the gain that the free coordinates still collect. Since
`D_Wr ~ 4 rho beta |Wr|`, nodes with fewer than about
`N/(4(2beta - 1) rho)` wrong fixings survive.

### 4.1 Upper bound: static variable branching

**Theorem 4.1.** Let `beta >= 1` be fixed, `rho -> inf` and `rho beta <= N`.
Put `L_rho = log(4(2beta - 1) rho)` and

```
kappa_rho = 1 - sqrt(2 L_rho/(rho beta)) - 1/sqrt(rho beta)      (-> 1).
```

Consider variable-branching B&B that branches on the variables in a fixed
order `pi` (chosen independently of the data), is given an incumbent of value
`UB` with `OPT <= UB <= W` (for example `x*` itself), and prunes a node when
its relaxation bound is at least `UB - eps'` for some `eps' >= 0`. Then w.h.p.
the tree has at most

```
1 + 2 sum_{i=1}^{K} C(N, i) <= 1 + 2 (eN/K)^K    nodes,    K = ceil( (1 + o(1)) N / (4 (2beta - 1) kappa_rho rho) ),
```

so `log #nodes <= (1 + o(1)) (N/(4(2beta - 1) rho)) log rho + log(eN) + O(1)`,
for every `rho -> inf` with `rho beta <= N`, including `rho = Theta(N)`. No
condition relating `rho` to the ML threshold is needed.

This improves the first version of the theorem, which had the factor
`kappa_N = 1 - sqrt(2 log N/(rho beta))` in place of `kappa_rho` and hence
needed `rho beta >= (2+eps) log N`; the improvement (using the sum of the `K`
most negative `zeta_i` instead of `K` times the most negative one) was
proposed in the hard review and is re-derived here.

*Proof.* Take `pi` to be the identity. A node at depth `d` fixes
`x_1, ..., x_d`; its wrong fixings `Wr ⊆ [d]` determine it, and its free set
is `{d+1, ..., N}`. The vector `v = w + 2 B_Wr 1` is independent of the free
columns, so its bound is at least `||v||^2 (1 - Y_{d,Wr})` with `Y_{d,Wr}`
distributed as in Theorem 1.3 with `n = N - d <= M`. Since
`K >= N/(4(2beta-1) rho)`, we have `log(N/K) <= L_rho`,
`K/N -> 0`, and `log C(N,K)/N <= (K/N) log(eN/K) -> 0`. Consider the events,
each of probability `1 - o(1)`:

- `W <= M + 2 sqrt(M log N) + 2 log N` (T2);
- `T_K <= K(sqrt(2 log(N/K)) + 1) + sqrt(2K log N)`, where `T_K` is the sum
  of the `K` largest values of `-g_i` (Lemma 0.1). Indeed, for every `t`,
  `T_K <= Kt + sum_i (-g_i - t)_+`, and with `t = sqrt(2 log(N/K))`,
  `N E(Z - t)_+ = N(phi(t) - t Phibar(t)) <= N phi(t)/(1 + t^2) <= K`; so
  `E T_K <= K(t + 1)`. `T_K` is a `sqrt K`-Lipschitz function of `g`, so
  Gaussian concentration gives `T_K <= E T_K + sqrt(2K log N)` with
  probability `>= 1 - 1/N`;
- for all `|Wr| = K`: `s_min(H~_Wr) >= sqrt M - sqrt K - sqrt(2 log C(N,K))
  - sqrt(2 log N)` ((T3) and a union bound);
- for all nodes with `|Wr| = K` (at most `(N+1) C(N,K)` of them):
  `Y_{d,Wr} <= (N-d)/(2M) + 2t'` with
  `t' = sqrt(64 (2 log((N+1) C(N,K)) + log N)/M) -> 0` (Lemma 0.2 and a union
  bound).

On these events, with `a = sqrt(rho/N)||w|| = sqrt(rho beta)(1 + o(1))`, for
`|Wr| = K`,

```
D_Wr = 4 sum_{Wr} zeta_i + 4 ||B_Wr 1||^2 >= -4 a T_K + 4 (rho/N) K s_min(H~_Wr)^2
     >= 4 rho beta K [1 - sqrt(2 L_rho/(rho beta)) - 1/sqrt(rho beta) - sqrt(2 log N/(K rho beta)) - o(1)]
     = 4 rho beta K (kappa_rho - o(1)),
```

because `K rho beta >= beta N/(4(2beta - 1))`, so `2 log N/(K rho beta) -> 0`.
The node is pruned if `||v||^2 (1 - Y) >= W` (then its bound is at least
`W >= UB`), that is, if `D_Wr >= W Y/(1 - Y)`. With `Y <= 1/(2beta) + 2t'`
the right side is at most `beta N (1 + o(1))/(2beta - 1)`, so every node with
`|Wr| = K` is pruned once `K >= (1 + o(1)) N/(4(2beta - 1) kappa_rho rho)`.
So no node with `|Wr| > K` is created, and every branched node has
`|Wr| <= K - 1` and depth `d < N`. Every processed node other than the root is
a child of a branched node, so, by `sum_{d=0}^{N-1} C(d, j) = C(N, j+1)`,

```
#nodes <= 1 + 2 sum_{d<N} sum_{j<=K-1} C(d, j) = 1 + 2 sum_{i=1}^{K} C(N, i) <= 1 + 2 (eN/K)^K .
```

For the second form write `c = N/(4(2beta-1) rho)` (bounded below, since
`rho beta <= N`) and `K <= c(1 + o(1))/kappa_rho + 1`. Then
`K log(eN/K) <= (c(1 + o(1))/kappa_rho) log(4e(2beta-1) kappa_rho rho) + log(eN)`,
and `kappa_rho -> 1` gives `(1 + o(1)) c log rho + log(eN)`. (Counting all
nodes with `|Wr| <= K` instead, as the first version did, loses a factor of
order `N` when `c` is bounded, because of the rounding in `K`.) ∎

*Remarks.*

- The order must not depend on the data: the union bound treats the free
  sets `{d+1, ..., N}` as fixed. Adaptive rules (most fractional, strong
  branching) are covered by the lower bound below but not by this upper bound.
- Without an initial incumbent, best-bound search obtains `x*` at the root
  when the box decoder succeeds (Hu–Lu: `rho >= (1+eps) 4 log N/(2beta - 1)`),
  because rounding the root solution then gives `x*`.
- `kappa_rho` is the loss from coordinates with negative `zeta_i`, whose
  one-bit flips are cheap. It tends to 1 only slowly: at
  `rho beta = 2, 4, 8, 16 log N` (`N = 10^6`, `beta = 1, 2`) the proved factor
  is `kappa_rho = 0.20–0.23, 0.41–0.42, 0.56–0.57, 0.68`, so at practical sizes
  the prefactor `1/kappa_rho` is 1.5–5 (`code/check_revision.py`, part G).
  Comparing the whole proved exponent `K log(eN/K)` with
  `(N/(4(2beta-1) rho)) log rho` gives a larger factor, 2.0–5.6 for
  `beta = 1` and 2.45–8.5 for `beta = 2` at `N = 10^6`, because `log(eN/K)`
  exceeds `log rho` by about `log(4e(2beta-1) kappa_rho)` (closing audit). Numerically (part C) the top-`K` sum is
  about half of `K max_i(-g_i)` at `N = 10^6`: the realized factor
  `1 - T_K/(K sqrt rho)` is 0.53–0.70 for `rho = 2.5–8 log N`, against the old
  `kappa_N = 0.11–0.50`, and the concentration bound on `T_K` held in every
  case.
- At fixed `rho` the theorem gives nothing (`kappa_rho` may be negative); the
  trivial bound `2^{N+1}` then matches the lower bound `exp(Omega(N))` of
  Theorem 4.3 up to the constant in the exponent.

### 4.2 An entropy lemma for concentrated families

**Lemma 4.2.** Let `F` be a family of `k`-subsets of an `n`-set, and let
`p_i` be the fraction of members of `F` that contain `i`. Suppose
`sum_i p_i^2 >= lambda k` with `lambda/2 >= e^2 k/n`. Then

```
log |F| <= n h(k/n) - (lambda k/2) log(n/(ek)),
log( C(n,k)/|F| ) >= (lambda k/2) log(n/(ek)) - (1/2) log(8k).
```

*Proof.* Let `S` be uniform on `F`. By subadditivity of entropy,
`log |F| = H(S) <= sum_i h(p_i)`. With `q = k/n` and `sum_i p_i = k`, the
identity `h(q) - h(p) = d(p||q) + (p - q) log(q/(1-q))` (where
`d(p||q)` is the binary Kullback–Leibler divergence) gives
`sum_i h(p_i) = n h(q) - sum_i d(p_i||q)`. From `log x >= 1 - 1/x`,
`d(p||q) >= phi(p) := p log(p/q) + q - p >= 0`. Put
`L = log(1/(eq)) >= 1`. We claim `phi(p) >= L p (p - lambda/2)` on `[0,1]`.
For `p <= lambda/2` the right side is `<= 0`. On `[lambda/2, 1]` it suffices
that `log(p/q) - 1 >= L(p - lambda/2)`, since `phi(p) >= p(log(p/q) - 1)`; the
left side minus the right side is concave in `p`, equals
`log(lambda/(2q)) - 1 >= 1` at `p = lambda/2` and `L lambda/2 >= 0` at
`p = 1`. Summing, `sum_i d(p_i||q) >= L(sum p_i^2 - (lambda/2) sum p_i) >=
L lambda k/2`. The second inequality follows from (T5). ∎

In words: a family of `k`-sets whose members overlap substantially on
average (`sum p_i^2 >= lambda k` means that two random members share about
`lambda k` elements) is smaller than `C(n,k)` by a factor
`exp((lambda k/2) log(n/(ek)))`. The extremal example is the star of all
`k`-sets containing a fixed `lambda k`-set.

### 4.3 Lower bound: the class number

**Theorem 4.3 (class number).** Let `beta >= 1` be fixed. There are constants
`c_beta, c'_beta, rho_0(beta) > 0` such that, for `rho_0 <= rho <= c'_beta N`
and `0 <= eps' <= rho`, w.h.p.

```
log kappa_{OPT - eps'}  >=  c_beta (N/rho) log(rho) - log(8N).
```

One can take `c_beta = beta p/(64 e^2 (sqrt(beta) + 1)^4)` with
`p = Phi(-1) - Phi(-2) = 0.1359`; for `beta = 1` this is `1.8e-5`,
`rho_0(1) = 71` and `c'_1 ~ 1.4e-4`. For `rho beta >= (2+eps) log N` the
condition `rho >= rho_0` can be dropped.

*What is covered.* By Section 0.3, every convex-piece certificate for the box
relaxation of `f` — variable, general split, multiway or semantic branching,
any rule, any node order, with any cuts in `x` valid for the node's vertices —
has at least `kappa` leaves, and with incumbent-based bound tightening at
least `kappa/(N+1)` nodes. By the weaker-relaxation remark of the integer-core
note (its Remark 1.11), the bound also applies to any relaxation that is
pointwise weaker than the box relaxation, for example the unconstrained
partial-distance bound of sphere decoders. The bound is superpolynomial
whenever `rho = o(N)` (and `rho >= rho_0`), and exponential for fixed
`rho >= rho_0`.

*What is not covered.* (i) Relaxations that use `x_i^2 = 1`, such as the
diagonal-shift (QCR-type) reformulation `f + sum_i d_i (1 - x_i^2)` with
`A'A - diag(d) ⪰ 0`, RLT/McCormick linearizations of products, and the SDP.
These change `phi`, and the class number must be recomputed. For `beta > 1`
the uniform shift `d = lambda_min(A'A) ~ rho (sqrt(beta) - 1)^2` adds
`4d(k - sum p_i^2)` at the barycenters used in the proof, which exceeds their
gain once `rho >~ 130` (`beta = 2`, hard review's estimate); in fact the
shifted relaxation is exact at the root from
`rho = (1+eps) 2 beta log N/(sqrt(beta) - 1)^4` on (Proposition 6.3). For
`beta = 1` the shift is only `~ rho/N^2` and changes nothing to first order.
Solvers may apply such reformulations to binary quadratic problems by
default. (ii) Tolerances `eps'` larger than about `0.25 a k - (W - OPT)`,
that is `~ 1.4e-4 N` for `beta = 1`. A relative gap tolerance such as
`1e-4 OPT ~ 1e-4 beta N` is of this size, and the theorem says nothing for
larger tolerances.

*Finite-`N` content.* The theorem is asymptotic. For `beta = 1` its bound is
positive only for `N >~ 1.7 10^7` (at `rho = 71` or `rho = 4 log N`), exceeds
`10 log N` only for `N >~ 2 10^8`, and at `rho = sqrt N` is positive only for
`N >~ 1.5 10^10`. The ratio between the exponents of Theorems 4.1 and 4.3 is
about `1/(4 c_1 kappa_rho) ~ 1.4 10^4/kappa_rho`, that is `10^4 - 10^5` at
practical `rho`. The practical evidence for large trees is Section 7, not
this theorem.

*Proof.* Condition on `w` and use Lemma 0.1. Let
`T = {i : g_i in [-2, -1]}`, `n' = |T| ~ Bin(N, p)`; w.h.p. `n' >= pN/2`. On
`T`, `a <= -zeta_i <= 2a` with `a = sqrt(rho/N) ||w|| = sqrt(rho beta)(1 + o(1))`.
The matrix `H^perp_T` is independent of `T` given the `g_i`, so by (T3),
w.h.p. `sigma_T := s_max(H^perp_T) <= sqrt(N) sigbar (1 + o(1))` with
`sigbar = sqrt(beta) + 1`. Put

```
lambda_1 = sqrt(beta)/(2 sigbar^2 sqrt(rho)),      k = floor( lambda_1 n'/(2e^2) ),
```

and let `P' = {x^S : S ⊆ T, |S| = k}`, so `|P'| = C(n', k)`.

*Every admissible class meets `P'` in a concentrated family.* Let `I` be a
class with `r(conv I) >= OPT - eps'`, let `F_I = {S : x^S in I ∩ P'}`, `m =
|F_I| >= 1`, and `p_i = |{S in F_I : i in S}|/m`. The barycenter
`xbar = x* - x* ∘ c`, `c = 2p`, lies in `conv I`. By Lemma 0.1,

```
f(xbar) - W = 2 zeta'c + ||B c||^2 = -2X + X^2/W + (rho/N) ||H^perp c||^2,     X = -zeta'c = sum_T c_i |zeta_i| .
```

(The `what`-component of `Bc` is `(zeta'c/||w||) what`; this identity is
checked numerically in `code/check_lemmas.py`, L4.) Since `sum_i c_i = 2k`,
`2ak <= X <= 4ak`, and `X/W <= 4ak/W <= 1/(e^2 sigbar^2)(1 + o(1)) < 0.04`.
So `-2X + X^2/W <= -1.96 X <= -3.92 a k`. Also
`||H^perp c||^2 <= sigma_T^2 ||c||^2 = 4 sigma_T^2 sum p_i^2`. Admissibility
gives `f(xbar) >= OPT - eps' = W - Delta - eps'` with `Delta = W - OPT`, so

```
sum_i p_i^2 >= (3.92 a k - Delta - eps') / (4 rho sigbar^2 (1 + o(1))) .
```

If `Delta + eps' <= 0.5 a k`, this is at least
`k (3.42 sqrt(rho beta)/(4 rho sigbar^2))(1 - o(1)) >= lambda_1 k`.

*Counting.* `k <= lambda_1 n'/(2e^2)` is the hypothesis of Lemma 4.2, so
`log(C(n',k)/m) >= (lambda_1 k/2) log(n'/(ek)) - (1/2) log(8k)`, and by the
counting bound of the integer-core note (its Lemma 1.5(b)),
`log kappa >= (lambda_1 k/2) log(n'/(ek)) - (1/2) log(8k)`. Here
`log(n'/(ek)) >= log(2e/lambda_1) >= (1/2) log rho` and
`lambda_1 k >= lambda_1^2 p N/(4e^2) - lambda_1 = beta p N/(16 e^2 sigbar^4 rho)
- lambda_1`, which gives the stated `c_beta`; the terms `lambda_1 log rho` and
`(1/2) log(8k)` are absorbed in `log(8N)`. We need `k >= 1` and
`eps' <= rho <= 0.25 a k`; both hold for `rho <= c'_beta N` with a small
`c'_beta`.

*The condition on `Delta`.* `k >= lambda_1 p N/(4e^2) - 1`, so
`0.5 a k >= c N` for a constant `c = c(beta) > 0`, while `eps' <= rho = o(N)`.
If `rho beta >= (2+eps) log N`, then `Delta = 0` w.h.p. (Theorem 2.2(a)).
Otherwise Theorem 2.2(c) gives `Delta <= 4N e^{-0.148 beta rho} + 4 log N`,
which is at most `0.25 a k` once
`e^{-0.148 beta rho} <= 0.4 beta p/(64 e^2 sigbar^2)`; for `beta = 1` this
means `rho >= 71`. ∎

*Remarks.*

- The mechanism is the relaxation's ability to spread flips. A class that
  contains many vertices differing from `x*` on descent coordinates contains
  their barycenter, where the linear gain `-2X ~ -4 sqrt(rho beta) k` is paid
  only by the quadratic term `4 rho sum p_i^2`. Unless the class's supports
  overlap heavily (`sum p_i^2 >= lambda k` with `lambda ~ 1/sqrt(rho)`), the
  barycenter undercuts `OPT`. Heavily overlapping families are
  exponentially smaller than `C(n', k)` (Lemma 4.2).
- The argument is not pairwise, and it cannot be: above `8 log N`,
  `G^mid` has no edges (Theorem 2.3) while `kappa` is superpolynomial. This
  gives a natural random family with `omega(G^mid) = 1` and
  `log kappa = Theta((N/rho) log rho)`.
- The constants are far from optimal (Section 4.4). The hard review measured
  the actual overlap threshold at which barycenters cross `W`:
  `sum p_i^2/k ~ 1.4/sqrt(rho beta)`, about 10 times the proof's `lambda_1`.
- The hard review computed exact class numbers on 590 instances with
  `N = 5, 6, 8`: the chain `omega(G^mid) <= omega(G^seg) <= chi(G^seg) <=
  kappa <=` (minimum variable-branching leaves) `<=` (static-order leaves)
  held in all of them, and `kappa > chi(G^seg)` in 36, confirming the
  non-pairwise character of `kappa` at small sizes.

**Corollary 4.4.** Let `beta >= 1` be fixed, `rho -> inf` and
`rho <= c'_beta N`, and give the B&B the incumbent `x*` (or `OPT`). W.h.p.

```
c_beta (N/rho) log rho - O(log N)  <=  log kappa  <=  log (min leaves of a variable-branching certificate)
                                   <=  log (static-order tree)  <=  (1 + o(1)) (N/(4(2beta-1) rho)) log rho + O(log N).
```

So the minimum size of every kind of convex-piece certificate for the box
relaxation, and the size of the simplest B&B, are all
`exp(Theta((N/rho) log rho))`, with constants differing by a factor
`10^4 - 10^5`. At fixed `rho >= 71` both are `exp(Theta(N))` (the upper
bound is trivial there). In particular:

- at `rho = c log N` (the ML, box-decoder and search thresholds all have this
  form) every certificate has `exp(Theta(N log log N/ log N))` leaves:
  superpolynomial but subexponential. This is the order of the
  Jaldén–Ottersten lower bound for sphere decoding up to a factor `log rho`
  in the exponent; their constant (`log(2)/4`) is larger than ours unless
  `log rho >~ 10^4` (Section 8);
- at `rho = N^a`, `0 < a < 1`: `exp(Theta(N^{1-a} log N))`;
- at `rho = theta N`: at most `N^{O(1/theta)}` (Theorem 4.1), at least
  `N^{c_beta/theta - 1}` (Theorem 4.3; informative only for very small
  `theta`), and at most `2N + 1` above `(1+eps) theta_c` (Theorem 3.1, with
  the incumbent or best-bound qualifier).

### 4.4 The sharp constant (conjecture)

The exact law predicts more. For any variable-branching tree and any node
with `|Fx| = d` fixings of which `|Wr| = j` are wrong, the node bound is
about `(W + 4 rho beta j)(1 - (N-d)/(2M))`, independently of which variables
were fixed (Theorem 1.3 applies to every free set). Hence every node at depth
`d` with `j < j_d := (1 - o(1)) N (N-d)/(4 rho (2M - N + d))` wrong fixings
must be branched, and the counting argument of a full binary tree (each
branching creates one child with the same number of wrong fixings and one
with one more) shows that every tree contains at least `C(d, j_d)` nodes at
depth `d`. Maximizing over `d = o(N)` gives the matching constant:

**Conjecture 4.5.** For `beta >= 1` fixed and `log N << rho << N`, the
minimum number of nodes of a variable-branching B&B tree with the box
relaxation (any rule, incumbent given) is
`exp((1 + o(1)) (N/(4(2beta - 1) rho)) log rho)`, the same for every rule to
first order in the exponent.

The upper half is Theorem 4.1. The lower half needs, uniformly over the
`exp(o(N))` nodes of depth `o(N)` with `o(N)` wrong fixings, (i) box
inactivity of the node NNLS problems and (ii) the lower tail of `Y`. For
`beta > 1`, (i) follows from Lemma 1.5 when `rho >> sqrt(N log rho)`, and (ii)
from Lemma 0.2; we have not carried out the bookkeeping, and for
`beta = 1` (i) is open as in Conjecture 3.3.

## 5. Midpoint cliques below `8 log N`

Pairwise conflicts are weaker than the class number here (Section 4.3), but
they have a sharp threshold of their own.

**Theorem 5.1 (midpoint cliques).** Let `beta >= 1` be fixed.

- (a) If `rho beta = c log N` with `0 < c < 8` fixed, then for every
  `delta > 0`, w.h.p. `G^mid_{OPT - eps'}` has a clique of size
  `exp(N^{1 - c/8 - delta})`, for every `0 <= eps' <= rho`, and its clique
  number is at most `exp(N^{1 - c/8 + delta})`.
- (b) If `rho` is fixed and `rho >= rho_1(beta)`, then w.h.p. it has a clique
  of size `e^{c(rho, beta) N}`. Following the proof, the hard review estimates
  `rho_1 ~ 600, 300, 150` for `beta = 1, 2, 4`; Theorem 4.3 already gives
  exponential class numbers from `rho = 71`.
- (c) If `rho beta >= (8+eps) log N`, its clique number is 1 (Theorem 2.3).

*Proof of (a).* Here `c = rho beta/log N`; ternary vectors are denoted `q`.
Condition on `w` (Lemma 0.1) and put `nu = sqrt(rho/N)||w||`
(so `zeta_i = nu g_i`) and `mu = (rho/N)(M - 1)` (so
`||b_i||^2 = mu (1 + o(1))` uniformly). Fix a small `eta > 0` and let

```
T = { i : g_i in [-(1 + 4eta) mu/(2nu), -(1 + 2eta) mu/(2nu)] },   n_T = |T|.
```

Since `mu/nu = sqrt(rho beta)(1 + o(1)) -> inf`, the Mills ratio gives
`P(i in T) = N^{-(1+2eta)^2 c/8 + o(1)}`, so w.h.p.
`n_T = N^{1 - (1+2eta)^2 c/8 + o(1)} -> inf`.

*Code.* Let `m = floor(eta n_T/e^2)`. For a uniformly random `m`-subset `S`
of `T` and a fixed `m`-subset `S0`,
`P(|S ∩ S0| >= eta m) <= C(m, eta m)(m/n_T)^{eta m} <= (e m/(eta n_T))^{eta m}
<= e^{-eta m}`. So the greedy family of `m`-subsets of `T` with pairwise
intersections `< eta m` has at least `e^{eta m}` members; keep the first
`ceil(e^{eta m})`, forming `C`. It depends on the data only through `T`.

*Conflicts.* For distinct `S, S' in C` let `q = 1_S + 1_{S'} in {0,1,2}^N`,
the `u`-coordinates of the midpoint of `x^S` and `x^{S'}`. By Lemma 0.1,

```
F(q) - W = 2 nu sum_i q_i g_i + (rho/N)[(sum_i q_i g_i)^2 + ||H^perp q||^2].
```

On `T`, `2 nu sum q_i g_i <= -(1+2eta) mu sum q_i = -2(1+2eta) mu m`, and
`(rho/N)(sum q_i g_i)^2 <= (1+4eta)^2 mu^2 m^2/W = O(rho^2 m^2/N) = o(mu m)`
because `m = N^{1 - Omega(1)}`. The matrix `H^perp` is independent of `T` and
`C`, and for fixed `q`, `||H^perp q||^2 ~ ||q||^2 chi^2_{M-1}`; by (T2) and a
union bound over the at most `e^{2 eta m + 2}` pairs,
`||H^perp q||^2 <= (M-1)||q||^2 (1 + o(1))` for all pairs. Since
`||q||^2 = 2m + 2|S ∩ S'| <= 2m(1 + eta)`,

```
F(q) - W <= -2(1 + 2eta) mu m + 2(1 + eta) mu m (1 + o(1)) + o(mu m) <= -eta mu m .
```

If `c > 2`, `OPT = W` (Theorem 2.2(a)); if `c <= 2`,
`W - OPT <= N^{1 - c/2 + delta'}` (Theorem 2.2(b)), which is `o(mu m)` because
`mu m = N^{1 - (1+2eta)^2 c/8 + o(1)}` and `(1 + 2eta)^2 < 4`. As
`eps' <= rho = o(mu m)`, every pair in `C` conflicts, and
`|C| >= e^{eta m} = exp(N^{1 - (1+2eta)^2 c/8 + o(1)})`. Let `eta -> 0`.

*Upper bound in (a)* (first-moment argument of the hard review, re-derived).
If two vertices `x^S, x^{S'}` conflict, their midpoint `q = 1_S + 1_{S'}` has
`F(q) < OPT - eps' <= W` and exactly `n_1 = |S Δ S'|` entries equal to 1.
So if w.h.p. no `q in {0,1,2}^N` with `n_1 > D` has `F(q) < W`, all members
of a clique lie within Hamming distance `D` of any one of them, and
`omega <= sum_{j <= D} C(N, j) <= exp(D log(eN/D))`. By Lemma 2.1 and the
split of Theorem 2.3, with `c' = c(1 - x0/2)`, the expected number of
improving `q` with `n_1 = n` in the small regime is at most

```
C(N, n) N^{-c' n/8} sum_{n_2} C(N, n_2) N^{-c' n_2/2} <= (e N^{1 - c'/8}/n)^n exp(N^{1 - c'/2}),
```

and the large regime contributes `e^{-Omega(N)}` as in Theorem 2.3. For
`n >= D := e^2 N^{1 - c'/8}` the first factor is at most `e^{-n}`, so the
total over `n > D` is at most `2 exp(-D + N^{1 - c'/2}) -> 0`, because
`1 - c'/2 < 1 - c'/8`. Hence `omega <= exp(N^{1 - c'/8} O(log N))`; let
`x0 -> 0`. ∎

Numerically (`code/check_revision.py`, part E), the largest `n_1` with a
first-moment count above `10^{-3}` is 3–15 times `N^{1 - c/8}` for
`N = 10^4, 10^5` and `c = 3, 4, 6` (3.0 to 15.1; the `N = 10^5`, `c = 3` cell
hit the loop limit in the first run and was rerun uncapped), consistent with
an `N^{o(1)}` factor.

*Proof of (b).* The same construction with `rho` fixed: now `P(i in T)` is a
positive constant, and we take `m = floor(min(eta n_T/e^2, eps_1 N/rho))`
with `eps_1` small, so that the terms `O(rho m/N)` and the union-bound error
`O(sqrt(eta m/M))` are at most `eta/4`. Then `F(c) - W <= -eta mu m/2` for all
pairs, with `eta mu m/2 >= c_1 N rho e^{-(1 + 2eta)^2 rho beta/8}`. Theorem
2.2(c) gives `W - OPT <= 4 N e^{-0.148 beta rho} + 4 log N`; since
`(1 + 2eta)^2/8 < 0.148` for `eta <= 0.04`, this is `<= eta mu m/4` for
`rho >= rho_1(beta)`. ∎

So for `rho = c log N` the midpoint clique is `exp(N^{1 - c/8 + o(1)})`,
while the class number is `exp(Theta(N log log N/ log N))` (Corollary 4.4),
which is larger for every `c > 0`. Midpoint cliques are the weaker
certificate here, as in the random-CVP analysis of the integer-core note
(its Section 3), and they vanish at `8 log N` while the class number does
not. For the binary problem this sidesteps the scout's concern about Gaussian
bases (integer-core note, Section 3.6(iv)): only `{0, ±2}^N` differences
occur, short lattice vectors play no role, and the box is the constraint that
creates conflicts. The relaxation's gain comes from the tangent cone of the
box at `x*` (Section 1), and the class-number argument counts vertices whose
barycenters fall into that gain. This says nothing about unbounded integer
variables with the unconstrained relaxation: integer-core Conjecture 3.8
remains open.

## 6. Comparison: the SDP relaxation and the eigenvalue shift

The Shor relaxation of `min f` over `{-1,1}^N` is
`min <Q, X>` over `X ⪰ 0`, `diag X = 1`, with
`Q = [[A'A, -A'y], [-y'A, y'y]]` of size `N+1`. It is tighter than the box
relaxation.

**Proposition 6.1 (tightness at `x*`; Jaldén–Martin–Ottersten 2003).** Let
`xt = (x*, 1)`. The matrix `xt xt'` is optimal for the SDP iff

```
A'A + diag(zeta) ⪰ 0,        zeta_i = x*_i a_i'w .
```

(Equivalently `B'B + diag(zeta) ⪰ 0`, a congruent matrix.) If the matrix is
positive definite, `xt xt'` is the unique optimum and `x*` is the unique ML
point.

This is the tightness condition of Jaldén, Martin and Ottersten (ICASSP 2003;
also in Jaldén's thesis), cited in exactly this form by Jiang–Liu–Bao–Jiang
(arXiv 2102.04586, eq. (2.4)). We include the short proof.

*Proof.* Both the SDP and its dual `max sum_i lambda_i` s.t.
`Q - diag(lambda) ⪰ 0` are strictly feasible, so there is no duality gap and
both optima are attained. `xt xt'` is optimal iff some dual feasible `lambda`
satisfies `(Q - diag lambda) xt = 0`, which forces
`lambda_i = (Q xt)_i/xt_i`, that is `lambda_i = -zeta_i` for `i <= N` and
`lambda_{N+1} = y'w`. For `(v, t) in R^{N+1}` put `d = v - t x*`. A direct
expansion (using `y = A x* + w`) gives

```
(v,t)' (Q - diag lambda) (v,t) = ||A d||^2 + sum_i zeta_i d_i^2 ,
```

and `(v, t) -> (d, t)` is a bijection; so `Q - diag(lambda) ⪰ 0` iff
`A'A + diag(zeta) ⪰ 0`. If the matrix is positive definite, the kernel of
`Q - diag(lambda)` is `span(xt)`, every optimal `X` has its range there, and
`X = xt xt'`. ∎

The identity is checked numerically in `code/check_lemmas.py` (L2). The
diagonal of the condition is `||a_i||^2 + zeta_i >= 0`, the one-bit ML
condition; so SDP tightness at `x*` implies that no one-bit flip improves on
`x*`, and it fails w.h.p. for `rho beta <= (2 - eps) log N`
(Theorem 2.2(d)).

**Theorem 6.2 (tall systems).** Let `beta > 1` be fixed. If
`rho >= (1 + eps) 2 beta log N/(sqrt(beta) - 1)^4`, then w.h.p. the SDP is
exact at `x*` (one B&B node, and `x*` is the unique ML point).

*Proof.* `lambda_min(A'A) >= rho (sqrt(beta) - 1 - o(1))^2` by (T3), and
`max_i(-zeta_i) <= sqrt(2 rho beta log N)(1 + o(1))` by Lemma 0.1 and (T1).
So `A'A + diag(zeta)` is positive definite when
`rho (sqrt(beta)-1)^2 > sqrt(2 rho beta log N)(1 + o(1))`. ∎

The sufficient condition `lambda_min(A'A) > max_i(-zeta_i)` is implied by
`lambda_min(H'H) > ||H'w||_inf`-type conditions; it is the BPSK case of the
condition (1.4) of Lu–Liu–Zhang–Zhang (SIOPT 2019) for their enhanced SDRs,
`lambda_min(H^dagger H) sin(pi/M) > ||H^dagger v||_inf` with `M = 2` (per the
easy review; we did not check whether their Theorem 4.5 contains a
`Theta(log N)` statement for fixed `beta > 1`).

The same condition makes a much simpler convex relaxation exact.

**Proposition 6.3 (eigenvalue shift).** Let `0 <= d <= lambda_min(A'A)` and
`f_d(x) = f(x) + d sum_i (1 - x_i^2)`. Then `f_d` is convex, equals `f` on
`{-1,1}^N`, and `x*` minimizes `f_d` over the box iff `zeta_i >= -d` for all
`i`. Let `beta > 1` be fixed and `d = lambda_min(A'A)`.

- (a) If `rho >= (1 + eps) 2 beta log N/(sqrt(beta) - 1)^4`, then w.h.p. the
  box relaxation of `f_d` is exact at the root.
- (b) If `(2 + eps) log N <= rho beta` and
  `rho <= (1 - eps) 2 beta log N/(sqrt(beta) - 1)^4`, then w.h.p. it is not
  exact. So the threshold of (a) is sharp for the shift.

*Proof.* The Hessian of `f_d` is `2(A'A - dI) ⪰ 0`. At `x*`,
`x*_i d_i f_d(x*) = -2 zeta_i - 2d`, and the KKT argument of Proposition 1.1
gives the "iff". (a) follows as in Theorem 6.2. (b) By Bai–Yin,
`lambda_min(A'A)/rho -> (sqrt(beta) - 1)^2`, and given `w` the maximum of the
`N` iid `-g_i` is at least `sqrt(2 log N)(1 - o(1))` w.h.p., so
`max_i(-zeta_i) >= sqrt(2 rho beta log N)(1 - o(1))`. In the stated range
this exceeds `d`, so `x*` does not minimize `f_d` over the box. Since `x*` is
the unique ML point (Theorem 2.2(a)) and `f_d = f` on vertices, no vertex
minimizes `f_d` over the box, and the root bound is below `OPT`. ∎

This is the uniform-diagonal case of the QCR-type perturbations used by MIQP
solvers for binary quadratic programs. The shift is exact only from the
threshold of (a) on, which is far above the SDP's: at `beta = 2` the
recheck's per-instance thresholds have medians `73, 93, 110 log N` for the
shift against `4.6, 4.4, 4.4 log N` for the SDP (`N = 100, 400, 1600`); at
`beta = 4`, 4.5–5.9 against 0.70–0.74. Numerically (`code/check_revision.py`,
part F; `beta = 2`, `N = 200`, 4 instances) the relative root gap of the
shifted relaxation with `d = 0.99 lambda_min(A'A)` is 0.066, 0.034, 0.010 and
`4.7e-4` at `rho = 30, 60, 130, 300` (the recheck found `3.9e-4` with
`d = lambda_min`), and `~1e-13` at `rho = 600`, against 0.232 for the box
relaxation; the exactness condition with `d = lambda_min` holds in 0 of 4
instances at `rho <= 300` and in 4 of 4 at `rho = 600`. So for tall systems
the obstruction of Section 4 is specific to the plain box relaxation, and a
cheap convex reformulation already removes it at `rho = Theta(log N)`. For
square systems `lambda_min(A'A) ~ rho/N^2` and the shift is negligible.

*Exact per-instance threshold.* Write `A'A + diag(zeta) = sqrt(rho)(sqrt(rho)
K + D)` with `K = H'H/N` and `D = diag(x* ∘ H'w)/sqrt(N)` (the value of
`diag(zeta)` at `rho = 1`). So the SDP is exact at `x*` iff
`rho >= rho* = (lambda_max(-D; K))_+^2`, a generalized eigenvalue (as noted in
the easy review). The bisection used in `code/exp_sdp.py` computes the same
quantity; the two agree to `4e-7` relative on 100 instances
(`code/check_revision.py`, part B).

*Heuristic for the tall-system threshold (not proved).* The most negative
`zeta_i`, about `-sqrt(2 rho beta log N)`, acts as a rank-one perturbation of
`A'A`. The perturbed matrix has a negative eigenvalue iff
`|zeta_i| e_i'(A'A)^{-1} e_i > 1`, and
`e_i'(A'A)^{-1} e_i ~ 1/(rho (beta - 1))` (inverse Wishart mean). This
predicts tightness iff `rho > (1 + o(1)) 2 beta log N/(beta - 1)^2`. The
per-instance thresholds (Section 7.5) have medians `c* = rho*/log N` of 4.4
(`beta = 2`, prediction 4), 1.4 (`beta = 3`, prediction 1.5) and 0.70–0.74
(`beta = 4`, prediction 0.89) at `N = 100–1600`. For `beta = 1.5` the
medians are 17–20 against the prediction 12, decreasing slowly with `N`; the
heuristic is loose there. The diagonal (one-bit ML) condition alone gives
medians 0.3–1.6, so for tall systems the SDP becomes exact within a constant
factor of the ML threshold.

*Square systems.* For `beta = 1` the relevant directions are the bottom
eigenvectors of `K` (as the easy review pointed out; the rank-one heuristic of
the first version was the wrong mechanism). For a unit vector `v` with
`v'Dv < 0`, `rho* >= (v'Dv/v'Kv)^2` is necessary. Here
`lambda_min(K) = s_min(H)^2/N ~ N^{-2}`, while for a delocalized `v`,
`v'Dv = sum_i D_ii v_i^2` has size about `sqrt(3/N)`. Some of the bottom few
eigenvectors has `v'Dv < 0`, so `rho* >~ N^3`, with a heavy upper tail
inherited from `s_min(H)^{-4}`. On 20 instances (`N = 100, 400`) the best of
the bottom five eigenvectors gives a lower bound within a factor 4 of `rho*`
in 14 cases, and the medians of `log rho*/log N` are 3.1 and 2.9
(`code/check_revision.py`, part B). This matches the measured medians
`rho* ~ N^{2.8} - N^{3.1}` (`N = 100, 400, 1600`; Section 7.5). So at
logarithmic SNR the square SDP is not exact, in line with Papailiopoulos'
remark that no SDP result gives exact recovery at any logarithmic SNR in the
square model. Nor is it close: at `N = 16–40` and
`rho in {N/4, 2 log N, 4 log N, 8 log N}`, the median relative SDP root gap
`(OPT - SDP)/OPT` is about one half to two thirds of the box gap (our seeds:
0.14–0.37 against 0.38–0.60; the easy review's independent seeds: 0.17–0.44
against 0.36–0.65). The ranges depend on the seeds and are indicative only,
and the SDP gap does not decrease with `N` in this range.

**What this means for B&B.** For tall systems the SDP, and even the
eigenvalue-shifted box relaxation, closes the gap that makes box-relaxation
B&B superpolynomial: at `rho >= (1+eps) 2beta log N/(sqrt(beta)-1)^4` one node
certifies `x*`, while every box-relaxation certificate has
`exp(Omega((N/log N) log log N))` leaves (Corollary 4.4, which rests on
Theorem 4.3). This is a superpolynomial (not exponential) separation between
convex relaxations at the same SNR, in the sense of the program's thesis:
branching cannot compensate for the box relaxation, and strengthening the
relaxation removes the obstruction. For square systems the question is open
(Section 9).

## 7. Computations

All runs use the generator of the scout's `bls.py` (same seeds give the same
instances), Python 3.13, NumPy 2.5, SciPy 1.18, CVXPY 1.9 with Clarabel 0.11,
single-threaded, at most 6 processes. Node relaxations are solved by SciPy's
NNLS, with an upper-bound active-set loop (and BVLS as a last resort) when a
coordinate exceeds 2; every bound used for pruning or for deciding C1 is the
certified Frank–Wolfe bound `F(u) + sum_j min(-g_j u_j, g_j (2 - u_j))` at
the computed point. `code/test_core.py` checks the node solver against the
scout's BVLS solver (40 random nodes, relative difference `4e-16`), the B&B
optimum against brute force (24 instances with `N = 10`, no mismatch), the
active-set loop against BVLS (200 nodes, 186 with active upper bounds,
relative difference `5e-16`), and the certified SDP bound against the SDP
value. `code/check_lemmas.py` checks Proposition 1.1 (300 instances), the
SDP identity of Proposition 6.1, Lemma 1.5 (1200 coordinates), the
barycenter formula of Section 4.3, Lemma 4.2 (5692 extremal two-level
profiles, minimum slack 0.89) and the witness formula (1.1); all pass
(`data/check_lemmas.log`).

### 7.1 Root relaxation

**Table 7.1a.** (root exactness, tiny `N`; 20000 trials per cell)

| beta | N | rho | P(`x*` box minimizer) | `2^-N` | P(vertex minimizer) | bound of Thm 1.2 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 0.2538 | 0.2500 | 0.3571 | 0.8972 |
| 1 | 2 | 4 | 0.2480 | 0.2500 | 0.2783 | 0.5514 |
| 1 | 2 | 16 | 0.2511 | 0.2500 | 0.2595 | 0.3894 |
| 1 | 2 | 64 | 0.2526 | 0.2500 | 0.2545 | 0.3163 |
| 1 | 4 | 1 | 0.0625 | 0.0625 | 0.1002 | 0.8050 |
| 1 | 4 | 4 | 0.0659 | 0.0625 | 0.0698 | 0.3040 |
| 1 | 4 | 16 | 0.0631 | 0.0625 | 0.0635 | 0.1516 |
| 1 | 4 | 64 | 0.0658 | 0.0625 | 0.0658 | 0.1000 |
| 1 | 6 | 1 | 0.0158 | 0.0156 | 0.0273 | 0.7222 |
| 1 | 6 | 4 | 0.0160 | 0.0156 | 0.0169 | 0.1676 |
| 1 | 6 | 16 | 0.0143 | 0.0156 | 0.0143 | 0.0591 |
| 1 | 6 | 64 | 0.0175 | 0.0156 | 0.0175 | 0.0316 |
| 1 | 8 | 1 | 0.0043 | 0.0039 | 0.0076 | 0.6480 |
| 1 | 8 | 4 | 0.0033 | 0.0039 | 0.0035 | 0.0924 |
| 1 | 8 | 16 | 0.0039 | 0.0039 | 0.0039 | 0.0230 |
| 1 | 8 | 64 | 0.0031 | 0.0039 | 0.0031 | 0.0100 |
| 2 | 2 | 1 | 0.2510 | 0.2500 | 0.2772 | 0.4900 |
| 2 | 2 | 4 | 0.2544 | 0.2500 | 0.2571 | 0.3123 |
| 2 | 2 | 16 | 0.2490 | 0.2500 | 0.2492 | 0.2656 |
| 2 | 2 | 64 | 0.2498 | 0.2500 | 0.2498 | 0.2539 |
| 2 | 4 | 1 | 0.0628 | 0.0625 | 0.0696 | 0.2401 |
| 2 | 4 | 4 | 0.0620 | 0.0625 | 0.0621 | 0.0975 |
| 2 | 4 | 16 | 0.0671 | 0.0625 | 0.0671 | 0.0706 |
| 2 | 4 | 64 | 0.0619 | 0.0625 | 0.0619 | 0.0645 |
| 2 | 6 | 1 | 0.0162 | 0.0156 | 0.0175 | 0.1176 |
| 2 | 6 | 4 | 0.0149 | 0.0156 | 0.0149 | 0.0305 |
| 2 | 6 | 16 | 0.0156 | 0.0156 | 0.0156 | 0.0187 |
| 2 | 6 | 64 | 0.0163 | 0.0156 | 0.0163 | 0.0164 |
| 2 | 8 | 1 | 0.0046 | 0.0039 | 0.0051 | 0.0576 |
| 2 | 8 | 4 | 0.0039 | 0.0039 | 0.0039 | 0.0095 |
| 2 | 8 | 16 | 0.0035 | 0.0039 | 0.0035 | 0.0050 |
| 2 | 8 | 64 | 0.0038 | 0.0039 | 0.0038 | 0.0042 |

**Table 7.1b.** (root gain; `rho` in `{2 log N, 4 log N, 8 log N, N/4}`; "instances" is per `rho` value, the column `G = G_inf` counts all four; `G_inf` does not depend on `rho`)

| beta | N | instances | mean G/N | var(G_inf)/N | mean active/N | var(active)/N | G = G_inf | median max u°(1) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 50 | 200 | 0.499 | 1.17 | 0.502 | 0.261 | 799/800 | 3.09 |
| 1 | 200 | 200 | 0.502 | 1.30 | 0.502 | 0.276 | 800/800 | 3.81 |
| 1 | 800 | 40 | 0.497 | 1.18 | 0.495 | 0.236 | 160/160 | 4.42 |
| 2 | 50 | 200 | 0.509 | 1.26 | 0.496 | 0.231 | 800/800 | 1.77 |
| 2 | 200 | 200 | 0.498 | 1.18 | 0.498 | 0.256 | 800/800 | 2.23 |
| 2 | 800 | 40 | 0.506 | 1.81 | 0.500 | 0.362 | 160/160 | 2.48 |

`P(x* box minimizer)` matches `2^{-N}` in every cell, as Proposition 1.1
requires, and vertex minimizers are never more frequent than Theorem 1.2
allows. The root-gain law of Theorem 1.3 and Corollary 1.4 is matched: mean
`N/2`, variance about `5N/4` (the one cell above 1.3 has 40 samples), active
set `Bin(N, 1/2)`. `G = G_inf` in 3519 of 3520 instances (all `rho` from
`2 log N` up): the upper bounds of the box are inactive at the root already at
`2 log N`, in line with the medians of `rho_box = (max u°(1))^2/4`: 2.4, 3.6,
4.9 for `beta = 1` and 0.8, 1.2, 1.5 for `beta = 2` (`N = 50, 200, 800`).

### 7.2 Condition C1

**Table 7.2.** (condition C1 at `x*`; `theta = rho/N`)

| beta | N | theta | theta_c | runs | C1 certified | C1 refuted | predictor | mean `min_i (r_i - W)/N` | mean `r_i/norm(v_i)^2` | law `1-(N-1)/(2M)` | nodes box-inactive |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 0.250 | 0.250 | 8 | 0 | 8 | 0 | -0.257 | 0.528 | 0.505 | 1.00 |
| 1 | 100 | 0.350 | 0.250 | 8 | 1 | 7 | 3 | -0.148 | 0.526 | 0.505 | 1.00 |
| 1 | 100 | 0.500 | 0.250 | 8 | 5 | 3 | 6 | 0.022 | 0.524 | 0.505 | 1.00 |
| 1 | 100 | 0.750 | 0.250 | 8 | 7 | 1 | 8 | 0.306 | 0.522 | 0.505 | 1.00 |
| 1 | 100 | 1.000 | 0.250 | 8 | 8 | 0 | 8 | 0.589 | 0.521 | 0.505 | 1.00 |
| 1 | 100 | 1.500 | 0.250 | 8 | 8 | 0 | 8 | 1.164 | 0.519 | 0.505 | 1.00 |
| 1 | 100 | 2.000 | 0.250 | 8 | 8 | 0 | 8 | 1.736 | 0.519 | 0.505 | 1.00 |
| 1 | 200 | 0.250 | 0.250 | 8 | 0 | 8 | 1 | -0.297 | 0.492 | 0.502 | 1.00 |
| 1 | 200 | 0.350 | 0.250 | 8 | 2 | 6 | 2 | -0.181 | 0.492 | 0.502 | 1.00 |
| 1 | 200 | 0.500 | 0.250 | 8 | 4 | 4 | 6 | 0.000 | 0.492 | 0.502 | 1.00 |
| 1 | 200 | 0.750 | 0.250 | 8 | 8 | 0 | 8 | 0.315 | 0.493 | 0.502 | 1.00 |
| 1 | 200 | 1.000 | 0.250 | 8 | 8 | 0 | 8 | 0.635 | 0.493 | 0.502 | 1.00 |
| 1 | 200 | 1.500 | 0.250 | 8 | 8 | 0 | 8 | 1.284 | 0.494 | 0.502 | 1.00 |
| 1 | 200 | 2.000 | 0.250 | 8 | 8 | 0 | 8 | 1.941 | 0.495 | 0.502 | 1.00 |
| 1 | 400 | 0.250 | 0.250 | 6 | 0 | 6 | 0 | -0.193 | 0.516 | 0.501 | 1.00 |
| 1 | 400 | 0.350 | 0.250 | 6 | 0 | 6 | 5 | -0.051 | 0.515 | 0.501 | 1.00 |
| 1 | 400 | 0.500 | 0.250 | 6 | 6 | 0 | 6 | 0.162 | 0.514 | 0.501 | 1.00 |
| 1 | 400 | 0.750 | 0.250 | 6 | 6 | 0 | 6 | 0.519 | 0.513 | 0.501 | 1.00 |
| 1 | 400 | 1.000 | 0.250 | 6 | 6 | 0 | 6 | 0.878 | 0.512 | 0.501 | 1.00 |
| 1 | 400 | 1.500 | 0.250 | 6 | 6 | 0 | 6 | 1.595 | 0.511 | 0.501 | 1.00 |
| 1 | 400 | 2.000 | 0.250 | 6 | 6 | 0 | 6 | 2.307 | 0.510 | 0.501 | 1.00 |
| 1 | 800 | 0.300 | 0.250 | 4 | 0 | 4 | 0 | -0.135 | 0.495 | 0.501 | 1.00 |
| 1 | 800 | 0.350 | 0.250 | 4 | 1 | 3 | 3 | -0.061 | 0.495 | 0.501 | 1.00 |
| 1 | 800 | 0.400 | 0.250 | 4 | 2 | 2 | 3 | 0.014 | 0.496 | 0.501 | 1.00 |
| 1 | 800 | 0.500 | 0.250 | 4 | 4 | 0 | 4 | 0.162 | 0.496 | 0.501 | 1.00 |
| 2 | 100 | 0.083 | 0.083 | 8 | 0 | 8 | 1 | -0.195 | 0.773 | 0.752 | 1.00 |
| 2 | 100 | 0.120 | 0.083 | 8 | 2 | 6 | 2 | -0.051 | 0.772 | 0.752 | 1.00 |
| 2 | 100 | 0.170 | 0.083 | 8 | 7 | 1 | 7 | 0.150 | 0.771 | 0.752 | 1.00 |
| 2 | 100 | 0.250 | 0.083 | 8 | 8 | 0 | 8 | 0.484 | 0.769 | 0.752 | 1.00 |
| 2 | 100 | 0.350 | 0.083 | 8 | 8 | 0 | 8 | 0.917 | 0.768 | 0.752 | 1.00 |
| 2 | 100 | 0.500 | 0.083 | 8 | 8 | 0 | 8 | 1.582 | 0.767 | 0.752 | 1.00 |
| 2 | 100 | 0.750 | 0.083 | 8 | 8 | 0 | 8 | 2.695 | 0.766 | 0.752 | 1.00 |
| 2 | 200 | 0.083 | 0.083 | 8 | 0 | 8 | 0 | -0.275 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.120 | 0.083 | 8 | 3 | 5 | 3 | -0.122 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.170 | 0.083 | 8 | 4 | 4 | 7 | 0.097 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.250 | 0.083 | 8 | 8 | 0 | 8 | 0.462 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.350 | 0.083 | 8 | 8 | 0 | 8 | 0.928 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.500 | 0.083 | 8 | 8 | 0 | 8 | 1.637 | 0.760 | 0.751 | 1.00 |
| 2 | 200 | 0.750 | 0.083 | 8 | 8 | 0 | 8 | 2.815 | 0.759 | 0.751 | 1.00 |
| 2 | 400 | 0.083 | 0.083 | 6 | 0 | 6 | 0 | -0.219 | 0.749 | 0.751 | 1.00 |
| 2 | 400 | 0.120 | 0.083 | 6 | 2 | 4 | 3 | -0.052 | 0.749 | 0.751 | 1.00 |
| 2 | 400 | 0.170 | 0.083 | 6 | 6 | 0 | 6 | 0.183 | 0.749 | 0.751 | 1.00 |
| 2 | 400 | 0.250 | 0.083 | 6 | 6 | 0 | 6 | 0.566 | 0.750 | 0.751 | 1.00 |
| 2 | 400 | 0.350 | 0.083 | 6 | 6 | 0 | 6 | 1.048 | 0.750 | 0.751 | 1.00 |
| 2 | 400 | 0.500 | 0.083 | 6 | 6 | 0 | 6 | 1.784 | 0.750 | 0.751 | 1.00 |
| 2 | 400 | 0.750 | 0.083 | 6 | 6 | 0 | 6 | 3.013 | 0.751 | 0.751 | 1.00 |
| 2 | 800 | 0.100 | 0.083 | 2 | 0 | 2 | 0 | -0.069 | 0.757 | 0.750 | 1.00 |
| 2 | 800 | 0.120 | 0.083 | 2 | 2 | 0 | 2 | 0.033 | 0.757 | 0.750 | 1.00 |
| 2 | 800 | 0.140 | 0.083 | 2 | 2 | 0 | 2 | 0.135 | 0.757 | 0.750 | 1.00 |

Every instance is decided: C1 is either certified (all `N` certified
single-fixing bounds exceed `f(x*)`) or refuted (some node value is below
`f(x*)`). The node values follow the exact law (cell averages of the
per-instance mean of `r_i/||v_i||^2` are within 0.03 of `1 - (N-1)/(2M)`,
single instances within 0.12), and every node NNLS problem was box-inactive. The observed transition moves down with `N` (for `beta = 1`:
from about `theta = 0.5` at `N = 100, 200` to about `0.4` at `N = 800`; for
`beta = 2`: from about `0.12–0.17` at `N <= 400` to between `0.10` and `0.12`
at `N = 800`), as the second-order prediction of Section 3 says, towards
`theta_c = 0.25` and `0.083`. The column "predictor" counts the
instances where the linearized prediction `min_i ||v_i||^2 (1 - G/W) > W`
holds; it agrees with the exact outcome in 310 of the 330 instances.

The easy review's independent C1 runs (184 instances, `beta in {1, 1.5, 2,
3}`, `N <= 800`, own code and seeds) also found every node problem
box-inactive and node values within 0.12 of the first-order law.

Node inactivity for square systems (evidence for Conjecture 3.3,
`code/check_node_inactivity.py`, `theta = 1/4`, 4 instances, 20–25 nodes
each): the largest single-fixing NNLS coefficient has mean 1.62, 1.01, 0.80,
0.56, 0.47 for `N = 50, 100, 200, 400, 800` (`beta = 1`; 14 of 100 nodes
exceed 2 at `N = 50`, none from `N = 100` on) and 0.76, 0.54, 0.43, 0.35,
0.26 for `beta = 2`.

### 7.3 Tree sizes

**Table 7.3.** (B&B nodes, incumbent `x*`, best-first; geometric mean [min, max])

| beta | N | rho | rho/log N | N/rho | `x*` optimal | maxfrac nodes | static nodes | `(N/(4(2b-1)rho)) log rho` |
|---:|---:|---:|---:|---:|---:|---|---|---:|
| 1 | 32 | 55.5 | 16.0 | 0.6 | 6/6 | 34 [23, 41] | 60 [53, 65] | 0.58 |
| 1 | 32 | 27.7 | 8.0 | 1.2 | 6/6 | 34 [23, 41] | 65 [59, 75] | 0.96 |
| 1 | 32 | 16.0 | 4.6 | 2.0 | 6/6 | 40 [27, 55] | 85 [63, 121] | 1.39 |
| 1 | 32 | 13.9 | 4.0 | 2.3 | 6/6 | 44 [29, 69] | 90 [63, 137] | 1.52 |
| 1 | 32 | 8.0 | 2.3 | 4.0 | 4/6 | 89 [39, 205] | 192 [81, 611] | 2.08 |
| 1 | 32 | 4.0 | 1.2 | 8.0 | 2/6 | 170 [83, 449] | 425 [221, 859] | 2.77 |
| 1 | 32 | 2.0 | 0.6 | 16.0 | 0/6 | 208 [97, 397] | 564 [283, 1695] | 2.77 |
| 1 | 64 | 66.5 | 16.0 | 1.0 | 6/6 | 64 [53, 73] | 127 [125, 129] | 1.01 |
| 1 | 64 | 33.3 | 8.0 | 1.9 | 6/6 | 68 [57, 77] | 135 [125, 163] | 1.69 |
| 1 | 64 | 32.0 | 7.7 | 2.0 | 6/6 | 68 [57, 79] | 137 [125, 163] | 1.73 |
| 1 | 64 | 16.6 | 4.0 | 3.8 | 6/6 | 97 [61, 153] | 246 [129, 417] | 2.70 |
| 1 | 64 | 16.0 | 3.8 | 4.0 | 6/6 | 102 [61, 153] | 268 [129, 467] | 2.77 |
| 1 | 64 | 8.0 | 1.9 | 8.0 | 5/6 | 506 [71, 1601] | 1802 [175, 6875] | 4.16 |
| 1 | 64 | 4.0 | 1.0 | 16.0 | 2/6 | 4328 [217, 17431] | 19068 [929, 82991] | 5.55 |
| 1 | 128 | 77.6 | 16.0 | 1.6 | 6/6 | 128 [115, 145] | 256 [253, 257] | 1.79 |
| 1 | 128 | 64.0 | 13.2 | 2.0 | 6/6 | 132 [117, 157] | 259 [253, 273] | 2.08 |
| 1 | 128 | 38.8 | 8.0 | 3.3 | 6/6 | 157 [123, 291] | 387 [253, 1029] | 3.02 |
| 1 | 128 | 32.0 | 6.6 | 4.0 | 6/6 | 189 [129, 493] | 509 [253, 1767] | 3.47 |
| 1 | 128 | 19.4 | 4.0 | 6.6 | 6/6 | 509 [185, 4455] | 2000 [567, 18041] | 4.89 |
| 1 | 128 | 16.0 | 3.3 | 8.0 | 6/6 | 980 [257, 15691] | 4656 [1193, 63165] | 5.55 |
| 1 | 128 | 8.0 | 1.6 | 16.0 | 2/2 | 5017 [3723, 6761] | 44000 [29547, 65523] | 8.32 |
| 1 | 256 | 128.0 | 23.1 | 2.0 | 4/4 | 257 [253, 265] | 509 [501, 513] | 2.43 |
| 1 | 256 | 88.7 | 16.0 | 2.9 | 4/4 | 267 [261, 277] | 549 [535, 581] | 3.24 |
| 1 | 256 | 64.0 | 11.5 | 4.0 | 4/4 | 320 [293, 335] | 1135 [941, 1497] | 4.16 |
| 1 | 256 | 44.4 | 8.0 | 5.8 | 4/4 | 570 [463, 647] | 4642 [3707, 6051] | 5.47 |
| 1 | 256 | 32.0 | 5.8 | 8.0 | 4/4 | 1774 [1221, 2177] | 21230 [17339, 28129] | 6.93 |
| 1 | 256 | 22.2 | 4.0 | 11.5 | 4/4 | 15765 [9193, 21729] | 100001 [100001, 100001] (4 capped) | 8.94 |
| 1 | 256 | 16.0 | 2.9 | 16.0 | 0/0 | 100001 [100001, 100001] (4 capped) | 100001 [100001, 100001] (4 capped) | 11.09 |
| 2 | 64 | 33.3 | 8.0 | 1.9 | 4/4 | 68 [51, 83] | 126 [123, 129] | 0.56 |
| 2 | 64 | 16.6 | 4.0 | 3.8 | 4/4 | 68 [51, 83] | 126 [123, 129] | 0.90 |
| 2 | 64 | 16.0 | 3.8 | 4.0 | 4/4 | 68 [51, 83] | 126 [123, 129] | 0.92 |
| 2 | 64 | 8.0 | 1.9 | 8.0 | 4/4 | 76 [51, 91] | 159 [123, 189] | 1.39 |
| 2 | 64 | 4.0 | 1.0 | 16.0 | 4/4 | 224 [89, 407] | 725 [305, 1297] | 1.85 |
| 2 | 128 | 38.8 | 8.0 | 3.3 | 4/4 | 130 [123, 133] | 256 [255, 257] | 1.01 |
| 2 | 128 | 32.0 | 6.6 | 4.0 | 4/4 | 130 [123, 133] | 256 [255, 257] | 1.16 |
| 2 | 128 | 19.4 | 4.0 | 6.6 | 4/4 | 132 [125, 137] | 262 [255, 281] | 1.63 |
| 2 | 128 | 16.0 | 3.3 | 8.0 | 4/4 | 139 [129, 149] | 295 [261, 363] | 1.85 |
| 2 | 128 | 8.0 | 1.6 | 16.0 | 4/4 | 352 [251, 471] | 2165 [1217, 4001] | 2.77 |

Observations.

- *C1 regime.* When `rho >~ N/3` (for example `16 log N` at `N <= 128`), the
  static-order tree has `2N + 1` nodes up to a few (a path to depth `N` with
  pruned siblings) and most-fractional branching about `N`. At `N = 256` the
  same SNR `16 log N = 0.35 N` is below the finite-`N` C1 threshold and the
  static tree exceeds `2N + 1` slightly.
- *Fixed `N/rho`.* Theorem 4.1 and Conjecture 4.5 predict trees of size
  about `(N/r)^{r/4}` at `rho = N/r` (`beta = 1`), a polynomial of degree
  `r/4`. From `N = 64` to `256` the static trees grow by factors 4.2
  (`r = 4`: 268 to 1135, degree 1.04) and 11.8 (`r = 8`: 1802 to 21230,
  degree 1.78), close to the predicted degrees 1 and 2.
- *Fixed `rho/log N`.* At `rho = 4 log N` the static trees have 90, 246, 2000
  and more than `10^5` nodes (all 4 runs capped) for `N = 32, 64, 128, 256`,
  and most-fractional trees 44, 97, 509 and 15765; at `rho = 8 log N`, 65,
  135, 387, 4642 (static) and 34, 68, 157, 570 (most fractional). This is
  faster than any fixed power at these sizes, as expected for
  `exp(Theta(N log log N/log N))`, but the range is too short to separate the
  two. Most-fractional branching is 2–10 times smaller than the static order
  at `N <= 128` and up to 12 times at `N = 256`. At `rho = 16 = 2.9 log N`,
  `N = 256`, both rules hit the `10^5`-node cap in all runs.
- *Tall systems* (`beta = 2`) have much smaller trees at the same `rho`, as
  `theta_c` and the exponent `N/(4(2beta - 1)rho)` predict.
- *Sphere decoding on the same instances* (`code/check_revision.py`,
  part D; `beta = 1`, `rho = 4 log N`, 6 seeds): natural-order Fincke–Pohst
  with radius `f(x*)` processes 839, 7937 and 61289 nodes (geometric means) at
  `N = 32, 48, 64`, against 90, 168 and 246 for static-order box B&B. The hard
  review found `2.6 10^6` at `N = 96` and more than `2 10^7` at `N = 128`
  (other seeds). So for square systems the box relaxation changes the growth
  of the node count substantially (Section 8). This compares node counts: a
  sphere-decoder node costs `O(N)`, a box node a bound-constrained
  least-squares solve, and in single-thread Python the sphere decoder was
  faster in wall-clock time at `N = 64` (the recheck measured 0.8 s against
  3.4 s for the six instances).
- *The exact-law predictor.* `code/predict_trees.py` replaces every node
  bound by `f(x^Wr)(1 - (N-d)/(2M))` and counts the static-order tree. On the
  same instances it reproduces the real static tree sizes within a factor
  of about 2 over three orders of magnitude (median ratio real/predicted per
  cell, Table 7.3b). The table excludes capped runs. At `N = 256`,
  `rho = 4 log N`, where all four real static trees exceeded `10^5` nodes, the
  hard review's run of the predictor gave 76885, 50259, 141113 and 56993: it
  underpredicts by at least a factor 1.3–2 in three of four instances,
  consistent with the upward trend of the ratios in the table. The hard review
  also found the node-level error to be a fraction of one wrong fixing
  (360 nodes, `N = 200, 400`).

**Table 7.3b.** (exact-law predictor versus real static-order trees, same instances; runs with a capped B&B or with `x*` not optimal are excluded)

| beta | N | rho tag | runs | real static nodes (geo. mean) | predicted (geo. mean) | median ratio real/pred |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 32 | c16 | 6 | 60 | 65 | 0.97 |
| 1 | 32 | c4 | 6 | 90 | 80 | 1.06 |
| 1 | 32 | c8 | 6 | 65 | 65 | 0.98 |
| 1 | 32 | r2 | 6 | 85 | 73 | 1.03 |
| 1 | 32 | r4 | 4 | 149 | 90 | 1.75 |
| 1 | 32 | r8 | 2 | 294 | 250 | 1.20 |
| 1 | 64 | c16 | 6 | 127 | 129 | 0.98 |
| 1 | 64 | c4 | 6 | 246 | 172 | 1.56 |
| 1 | 64 | c8 | 6 | 135 | 129 | 1.00 |
| 1 | 64 | r16 | 2 | 3155 | 7242 | 0.44 |
| 1 | 64 | r2 | 6 | 137 | 129 | 1.02 |
| 1 | 64 | r4 | 6 | 268 | 182 | 1.66 |
| 1 | 64 | r8 | 5 | 1431 | 832 | 1.91 |
| 1 | 128 | c16 | 6 | 256 | 257 | 1.00 |
| 1 | 128 | c4 | 6 | 2000 | 1144 | 1.09 |
| 1 | 128 | c8 | 6 | 387 | 265 | 1.09 |
| 1 | 128 | r16 | 2 | 44000 | 28385 | 1.65 |
| 1 | 128 | r2 | 6 | 259 | 257 | 1.00 |
| 1 | 128 | r4 | 6 | 509 | 326 | 1.27 |
| 1 | 128 | r8 | 6 | 4656 | 2287 | 1.15 |
| 1 | 256 | c16 | 4 | 549 | 513 | 1.05 |
| 1 | 256 | c8 | 4 | 4642 | 2875 | 1.57 |
| 1 | 256 | r2 | 4 | 509 | 513 | 1.00 |
| 1 | 256 | r4 | 4 | 1135 | 700 | 1.51 |
| 1 | 256 | r8 | 4 | 21230 | 9876 | 2.19 |
| 2 | 64 | c4 | 4 | 126 | 129 | 0.98 |
| 2 | 64 | c8 | 4 | 126 | 129 | 0.98 |
| 2 | 64 | r16 | 4 | 725 | 910 | 0.72 |
| 2 | 64 | r4 | 4 | 126 | 129 | 0.98 |
| 2 | 64 | r8 | 4 | 159 | 175 | 0.90 |
| 2 | 128 | c4 | 4 | 262 | 263 | 1.00 |
| 2 | 128 | c8 | 4 | 256 | 257 | 1.00 |
| 2 | 128 | r16 | 4 | 2165 | 1930 | 1.11 |
| 2 | 128 | r4 | 4 | 256 | 257 | 1.00 |
| 2 | 128 | r8 | 4 | 295 | 295 | 0.98 |

- *Extrapolation (heuristic).* `code/knapsack_predictor.py` evaluates the same
  predictor without cross terms, as a knapsack count, from the exact
  single-coordinate law, up to `N = 10^5` (5 samples per cell, 2 for
  `N >= 3 10^4`). The DP runs in the log domain (a first version normalized by
  the maximum and was corrupted by denormals at `N = 10^5`); it matches
  brute-force enumeration on 6 instances with `N = 12` (`code/test_core.py`).
  Its log tree size approaches
  `(N/(4(2beta - 1) rho)) log rho`: the ratio is 0.88–1.2 for `beta = 1` at
  `N >= 3000` and 1.1–1.4 for `beta = 2` at `N >= 10^4` (except at the
  largest `rho`, where the exponent is small). This checks the asymptotic
  evaluation of the first-order model that motivates Conjecture 4.5 (mean
  `Y`, no box activity, no cross terms); it is not independent evidence that
  real trees, or other rules, follow that constant.

**Table 7.3c.** (knapsack extrapolation of the exact-law predictor; each cell: mean predicted `log(#nodes)` / `(N/(4(2beta-1)rho)) log rho`; tags as in the appendix)

| beta | N | c4 | c8 | r8 | r32 | r128 |
|---:|---:|---|---|---|---|---|
| 1 | 100 | 6.6 / 4.0 | 5.3 / 2.4 | 7.9 / 5.1 | - | - |
| 1 | 300 | 12.7 / 10.3 | 8.7 / 6.3 | 9.4 / 7.2 | - | - |
| 1 | 1000 | 30.9 / 30.0 | 19.5 / 18.2 | 11.8 / 9.7 | 29.3 / 27.5 | - |
| 1 | 3000 | 79.4 / 81.2 | 47.5 / 48.7 | 14.0 / 11.9 | 35.5 / 36.3 | 99.1 / 100.9 |
| 1 | 10000 | 231.2 / 244.7 | 132.1 / 145.9 | 16.4 / 14.3 | 43.6 / 46.0 | 127.2 / 139.5 |
| 1 | 30000 | 624.2 / 676.5 | 357.2 / 401.3 | 18.7 / 16.5 | 51.7 / 54.7 | 155.3 / 174.6 |
| 1 | 100000 | 1902.9 / 2079.1 | 1091.2 / 1227.7 | 22.3 / 18.9 | 60.0 / 64.4 | 188.2 / 213.1 |
| 2 | 100 | 5.4 / 1.3 | 5.3 / 0.8 | 5.4 / 1.7 | - | - |
| 2 | 300 | 7.6 / 3.4 | 6.4 / 2.1 | 6.4 / 2.4 | 12.1 / 6.0 | - |
| 2 | 1000 | 16.2 / 10.0 | 11.3 / 6.1 | 7.6 / 3.2 | 15.1 / 9.2 | 39.9 / 21.9 |
| 2 | 3000 | 37.4 / 27.1 | 23.0 / 16.2 | 8.7 / 4.0 | 18.3 / 12.1 | 47.4 / 33.6 |
| 2 | 10000 | 104.8 / 81.6 | 60.7 / 48.6 | 9.9 / 4.8 | 21.8 / 15.3 | 57.9 / 46.5 |
| 2 | 30000 | 278.3 / 225.5 | 159.0 / 133.8 | 11.0 / 5.5 | 24.9 / 18.2 | 68.2 / 58.2 |
| 2 | 100000 | 844.0 / 693.0 | 474.7 / 409.2 | 12.2 / 6.3 | 28.7 / 21.5 | 79.2 / 71.0 |

  At `rho = 4 log N` the model predicts `e^{80}` nodes at `N = 3000` and
  `e^{620}` at `N = 3 10^4` (heuristic, not a bound): the superpolynomial
  growth of Corollary 4.4 would be invisible at `N <= 256` because
  `(N/rho) log rho` is still small there.

### 7.4 Thresholds from the single-coordinate law

**Table 7.4a.** (single-coordinate law: P(some one-bit flip beats `x*`) / P(some half move beats `x*`); `c = rho beta/log N`)

| beta | N | c=1 | c=1.5 | c=2 | c=2.5 | c=3 | c=4 | c=5 | c=6 | c=7 | c=8 | c=9 | c=10 | c=12 |
|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 100 | 0.76/1.00 | 0.37/1.00 | 0.14/1.00 | 0.05/0.99 | 0.02/0.95 | 0.00/0.80 | 0.00/0.57 | 0.00/0.36 | 0.00/0.23 | 0.00/0.13 | 0.00/0.08 | 0.00/0.05 | 0.00/0.01 |
| 1 | 1000 | 0.98/1.00 | 0.48/1.00 | 0.10/1.00 | 0.01/1.00 | 0.00/1.00 | 0.00/0.98 | 0.00/0.81 | 0.00/0.48 | 0.00/0.21 | 0.00/0.10 | 0.00/0.05 | 0.00/0.02 | 0.00/0.00 |
| 1 | 10000 | 1.00/1.00 | 0.62/1.00 | 0.09/1.00 | 0.01/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/0.97 | 0.00/0.65 | 0.00/0.28 | 0.00/0.08 | 0.00/0.05 | 0.00/0.01 | 0.00/0.00 |
| 1 | 100000 | 1.00/1.00 | 0.84/1.00 | 0.13/1.00 | 0.01/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/0.75 | 0.00/0.39 | 0.00/0.05 | 0.00/0.03 | 0.00/0.00 | 0.00/0.00 |
| 2 | 100 | 0.79/1.00 | 0.36/1.00 | 0.13/1.00 | 0.04/0.99 | 0.01/0.95 | 0.00/0.81 | 0.00/0.57 | 0.00/0.37 | 0.00/0.23 | 0.00/0.13 | 0.00/0.07 | 0.00/0.04 | 0.00/0.02 |
| 2 | 1000 | 0.99/1.00 | 0.46/1.00 | 0.10/1.00 | 0.02/1.00 | 0.00/1.00 | 0.00/0.98 | 0.00/0.78 | 0.00/0.47 | 0.00/0.24 | 0.00/0.10 | 0.00/0.03 | 0.00/0.02 | 0.00/0.00 |
| 2 | 10000 | 1.00/1.00 | 0.60/1.00 | 0.11/1.00 | 0.01/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/0.96 | 0.00/0.67 | 0.00/0.26 | 0.00/0.08 | 0.00/0.03 | 0.00/0.01 | 0.00/0.00 |
| 2 | 100000 | 1.00/1.00 | 0.80/1.00 | 0.09/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/1.00 | 0.00/0.81 | 0.00/0.31 | 0.00/0.15 | 0.00/0.04 | 0.00/0.00 | 0.00/0.00 |

**Table 7.4b.** (real instances, 20 seeds: instances with a single / pair half-move conflict)

| beta | N | c | single | pair | pair without single |
|---:|---:|---:|---:|---:|---:|
| 1 | 200 | 4 | 16 | 16 | 0 |
| 1 | 200 | 6 | 4 | 3 | 0 |
| 1 | 200 | 7 | 1 | 1 | 1 |
| 1 | 200 | 8 | 0 | 0 | 0 |
| 1 | 200 | 9 | 0 | 0 | 0 |
| 1 | 200 | 10 | 0 | 0 | 0 |
| 1 | 800 | 4 | 20 | 20 | 0 |
| 1 | 800 | 6 | 7 | 8 | 1 |
| 1 | 800 | 7 | 5 | 3 | 0 |
| 1 | 800 | 8 | 1 | 1 | 0 |
| 1 | 800 | 9 | 1 | 0 | 0 |
| 1 | 800 | 10 | 0 | 0 | 0 |
| 2 | 200 | 4 | 19 | 16 | 0 |
| 2 | 200 | 6 | 5 | 2 | 0 |
| 2 | 200 | 7 | 4 | 2 | 0 |
| 2 | 200 | 8 | 2 | 1 | 0 |
| 2 | 200 | 9 | 1 | 0 | 0 |
| 2 | 200 | 10 | 1 | 0 | 0 |
| 2 | 800 | 4 | 20 | 20 | 0 |
| 2 | 800 | 6 | 8 | 4 | 0 |
| 2 | 800 | 7 | 4 | 0 | 0 |
| 2 | 800 | 8 | 1 | 0 | 0 |
| 2 | 800 | 9 | 0 | 0 | 0 |
| 2 | 800 | 10 | 0 | 0 | 0 |

### 7.5 SDP relaxation

**Table 7.5a.** (SDP exactness threshold per instance: `c* = rho*/log N`)

| beta | N | instances | median `c*` | [min, max] | median `log(rho*)/log N` | median one-bit (ML) threshold / `log N` | heuristic `2b/(b-1)^2` | proved sufficient `2b/(sqrt b - 1)^4` |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 100 | 40 | 1.18e+05 | [672, 4.27e+12] | 2.87 | 1.34 | - | - |
| 1 | 400 | 40 | 2.51e+07 | [1.19e+05, 3.79e+14] | 3.11 | 1.47 | - | - |
| 1 | 1600 | 10 | 9.03e+07 | [1.05e+07, 4.04e+11] | 2.75 | 1.60 | - | - |
| 1.5 | 100 | 40 | 20.3 | [8.63, 43.2] | 0.99 | 0.90 | 12.00 | 1175.9 |
| 1.5 | 400 | 40 | 17.8 | [11.2, 23.6] | 0.78 | 0.97 | 12.00 | 1175.9 |
| 1.5 | 1600 | 10 | 17.3 | [14.5, 21.1] | 0.66 | 1.15 | 12.00 | 1175.9 |
| 2 | 100 | 40 | 4.62 | [1.62, 10.3] | 0.66 | 0.65 | 4.00 | 135.9 |
| 2 | 400 | 40 | 4.42 | [2.92, 6.53] | 0.55 | 0.72 | 4.00 | 135.9 |
| 2 | 1600 | 10 | 4.38 | [3.32, 5.31] | 0.47 | 0.83 | 4.00 | 135.9 |
| 3 | 100 | 40 | 1.42 | [0.673, 2.84] | 0.41 | 0.54 | 1.50 | 20.9 |
| 3 | 400 | 40 | 1.33 | [0.955, 2.04] | 0.35 | 0.48 | 1.50 | 20.9 |
| 3 | 1600 | 10 | 1.38 | [1.01, 1.91] | 0.31 | 0.51 | 1.50 | 20.9 |
| 4 | 100 | 40 | 0.707 | [0.387, 1.6] | 0.26 | 0.33 | 0.89 | 8.0 |
| 4 | 400 | 40 | 0.744 | [0.561, 1.46] | 0.25 | 0.37 | 0.89 | 8.0 |
| 4 | 1600 | 10 | 0.696 | [0.581, 0.912] | 0.22 | 0.36 | 0.89 | 8.0 |

**Table 7.5b.** (square systems: relative root gaps `(OPT - bound)/OPT`, 6 seeds)

| N | rho | box gap, median | SDP gap, median [max] | SDP exact | `x*` optimal |
|---:|---:|---:|---|---:|---:|
| 16 | 4.0 | 0.376 | 0.1419 [0.3983] | 0/6 | 2/6 |
| 16 | 5.5 | 0.446 | 0.1928 [0.3771] | 0/6 | 2/6 |
| 16 | 11.1 | 0.537 | 0.2394 [0.4961] | 0/6 | 4/6 |
| 16 | 22.2 | 0.577 | 0.2706 [0.3912] | 0/6 | 6/6 |
| 24 | 6.0 | 0.511 | 0.3446 [0.4235] | 0/6 | 0/6 |
| 24 | 6.4 | 0.521 | 0.3529 [0.4218] | 0/6 | 2/6 |
| 24 | 12.7 | 0.601 | 0.3691 [0.5039] | 0/6 | 6/6 |
| 24 | 25.4 | 0.601 | 0.3136 [0.4486] | 0/6 | 6/6 |
| 32 | 6.9 | 0.461 | 0.2848 [0.5133] | 0/6 | 4/6 |
| 32 | 8.0 | 0.492 | 0.3102 [0.4977] | 0/6 | 4/6 |
| 32 | 13.9 | 0.518 | 0.2729 [0.4449] | 0/6 | 6/6 |
| 32 | 27.7 | 0.518 | 0.2020 [0.3842] | 0/6 | 6/6 |
| 40 | 7.4 | 0.409 | 0.2232 [0.3350] | 0/6 | 3/6 |
| 40 | 10.0 | 0.420 | 0.2385 [0.3088] | 0/6 | 5/6 |
| 40 | 14.8 | 0.462 | 0.2367 [0.2947] | 0/6 | 5/6 |
| 40 | 29.5 | 0.471 | 0.1764 [0.2498] | 0/6 | 6/6 |

For tall systems with `beta >= 2` the per-instance SDP threshold `rho*`
concentrates around the heuristic `2 beta log N/(beta - 1)^2` (Section 6),
far below the proved sufficient condition; for `beta = 1.5` the heuristic is
loose. For square systems `log rho*/log N` is about 3. At small `N` the SDP
root gap is about one half to two thirds of the box gap; Table 7.5b uses our
seeds, and the easy review's independent seeds give 0.17–0.23 (`N = 16`) and
0.36–0.44 (`N = 20`), so the ranges are indicative only.

## 8. Literature comparison

Sources were checked as stated; "via review" marks attributions supplied by
the independent reviews that we did not re-read. Searches (2026-09-29): arXiv
API queries `ti:"branch and bound" AND ti:MIMO` (5 hits, all 1-bit precoding,
no node theory), `abs:"branch-and-bound" AND abs:"box relaxation"` (0),
`abs:"sphere decoder" AND abs:"lower bound" AND abs:semidefinite` (0),
`abs:"statistical dimension" AND abs:"nonnegative least squares"` (0),
`ti:box AND ti:relaxation AND ti:MIMO` (3), and title searches for
sphere-decoding complexity. None gave a node-count theorem for
branch-and-bound with the box or SDP relaxation on random binary least
squares. An unsuccessful search does not establish novelty; the conic-geometry
search in particular missed the known results below.

- **Papailiopoulos (arXiv 2609.19405, 16 Sep 2026; PDF read, Sections 1–3,
  11, Appendices A–B).** Same model with `beta = 1`. Theorem 2.1(a): rounded
  LMMSE followed by steepest single-bit descent recovers `x*` with vanishing
  error, uniformly over `x*` and all `rho >= 2 log N`, in `O(N^3)`
  operations; (b): ML fails for `rho <= 2 log N - log log N - s_N` because a
  one-bit neighbour beats `x*`; Remark A.2: ML succeeds for `rho >= 2 log N`.
  His Appendix A attributes first-order ML achievability to Hansen et al.
  (2009) and Hassibi et al. (2014, Lemma IV.2). The paper states that the
  closest prior square-system theorem, for the box relaxation, has threshold
  `4 log N` (this is box *decoding*, Hu–Lu), and that no SDP result gives exact
  block recovery at logarithmic SNR in the square model.
  *Relation.* His result is about search; ours is about certification with
  convex relaxations. For `beta = 1` and every `rho = c log N` with `c > 2`,
  the ML point is `x*` and is found in polynomial time, yet every certificate
  of its optimality for the box relaxation (any branching, any convex pieces,
  with cuts in `x` and incumbent-based tightening) has
  `exp(Theta(N log log N/log N))` leaves (Corollary 4.4); the linear-size
  certificates given by C1 appear only from `rho ~ N/4` on (Theorem 3.1). This
  is a relaxation-specific certification lower bound in a planted model where
  search is easy, not a computational search/certification gap: for
  `beta > 1` the SDP and the eigenvalue-shifted relaxation certify `x*` at
  `rho = O(log N)` (Section 6), and for `beta = 1` it is open whether any
  polynomial-size certificate exists. For `beta > 1`, polynomial-time search
  is covered by the cited results only above the box-decoder threshold
  `4 log N/(2beta - 1)` (Hu–Lu), not between it and the ML threshold
  `2 log N/beta`.
- **Hansen–Hassibi–Dimakis–Xu (GLOBECOM 2009) and Hassibi–Hansen–Dimakis–
  Alshamary–Xu (IEEE TSP 2014, Lemma IV.2)** (via Papailiopoulos and the easy
  review). First-order ML achievability at `rho > 2 log N + f(N)` for
  `beta = 1`: the achievability half of Theorem 2.2 for `beta = 1`. We did not
  check whether they treat `M > N`.
- **Hu–Lu (arXiv 2006.08416; IEEE JSAIT 2020; abstract and Section I read).**
  Box decoder `sign(argmin_{[-1,1]^N} ||y - Ax||^2)` with `A_ij ~ N(0, 1/N)`,
  noise variance `sigma^2`, `delta = M/N > 1/2`: the number of bit errors is
  asymptotically Poisson, and exact recovery holds w.h.p. iff
  `(delta - 1/2)/(2 sigma^2 log N) -> alpha* > 1` (their Proposition 1, under
  `sigma^2 log^2 N` bounded below). In our normalization
  `rho > 4 log N/(2beta - 1)`. We use it as an input to Corollary 1.6 and to
  Theorem 3.1(d) (box inactivity for `beta = 1`). It concerns rounding, not
  exactness of the relaxation: the relaxation is never exact
  (Proposition 1.1, Theorem 1.2).
- **Thrampoulidis–Abbasi–Xu–Hassibi (arXiv 1510.01413; abstract read) and
  Thrampoulidis–Xu–Hassibi (arXiv 1711.11215, IEEE TSP 2018; abstract read).**
  CGMT analysis of the box relaxation at fixed `M/N` and SNR: exact bit error
  rate, within 3 dB of the matched-filter bound for square systems, and the
  empirical distribution of the relaxed solution. The fact that the box
  solution has a constant fraction of interior coordinates is implicit there.
  *Relation.* In the box-inactive regime the root gain has the exact law of
  Theorem 1.3; CGMT would give the fixed-SNR analogue when upper bounds are
  active. The node analysis of Sections 3–4 uses the same law at every node.
- **Conic geometry** (via the easy review). The expected conic intrinsic
  volumes of the cone spanned by `n <= d` iid Gaussian vectors are
  `C(n,k) 2^{-n}`: Hug–Schneider (DCG 2016, Corollaries 4.2–4.3, via the
  Cover–Efron cone), stated as Lemma 5.1 and formula (3.5) of
  Godland–Kabluchko–Thäle (Discrete Analysis 2022, arXiv 2012.06189). The
  master Steiner formula of McCoy–Tropp (DCG 2014) gives the independent
  `chi^2_k`, `chi^2_{d-k}` decomposition, that is, the chi-bar-squared law of
  order-restricted inference (Kudô 1963; Shapiro 1985). Theorem 1.3 is
  therefore known in substance; the note contributes a direct proof, the
  fixed-vector per-face form used at B&B nodes, and the extension of the face
  law to sign-symmetric column laws.
- **Jaldén–Ottersten (IEEE TSP 53(4), 2005; not re-read, checked through
  Papailiopoulos' restatement).** The expected complexity of the Fincke–Pohst
  sphere decoder is exponential in `N` at every fixed SNR; in the present
  normalization their bound reads `C(N) >= 2^{N/(4 rho + 2)} - 1`, which is
  `exp(Theta(N/log N))` at `rho = Theta(log N)`. *Relation.* Theorem 4.3
  gives the same order up to a factor `log rho` in the exponent for a much
  larger class: every certificate for the box relaxation, and, by the
  weaker-relaxation remark, sphere decoders themselves, per instance and
  w.h.p. Its constant is so small that the Jaldén–Ottersten bound is
  numerically stronger unless `log rho >~ 10^4`. The first version of this note
  concluded that "the box relaxation does not change the order of the
  exponent of enumeration". That was wrong for square systems (hard review): a
  lower bound does not bound sphere-decoder complexity from above, and for
  `beta = 1` natural-order Fincke–Pohst with radius `f(x*)` has typical
  exponent of order `N/sqrt(rho)`. Heuristically, fixing the last `k`
  coordinates with `j` of them wrong gives a partial distance of about
  `(1 + 4 rho j/N) chi^2_{M-N+k}`, so for `beta = 1` all partial vectors
  survive up to `k ~ N/(2 sqrt(rho))`; the box relaxation's exponent is
  `(N/rho) log rho` (Theorem 4.1). The measurements of Section 7.3 agree
  (at `N = 64`, `rho = 4 log N`: `6 10^4` against 246 nodes on the same
  instances; node counts, not running time). For `beta > 1` both exponents are heuristically
  `Theta((N/rho) log rho)`, with constants about `1/(4(beta - 1))` and
  `1/(4(2beta - 1))`. Data-dependent orderings (SQRD, V-BLAST) were not
  examined.
- **Hassibi–Vikalo (IEEE TSP 53(8), 2005; from memory and Papailiopoulos'
  summary).** Expected sphere-decoder complexity is polynomial over practical
  ranges of `N` and SNR. Our computations show similar pre-asymptotic
  behaviour for box-relaxation B&B (Section 7.3): at `N <= 256` the exponent
  `(N/rho) log rho` is small.
- **Seethaler–Jaldén–Studer–Bölcskei (arXiv 0905.1215; abstract read).**
  Sphere-decoding complexity on random infinite lattices has a Pareto tail
  with exponent `M - N + 1` (for `M x N` Gaussian bases), not improved by
  lattice reduction. *Relation.* This concerns infinite lattices and fixed
  enumeration; our bounds are for the binary box. The heavy upper tail of the
  square-system SDP threshold (Section 6) also comes from small singular values
  of square Gaussian matrices; we did not relate the two tails precisely.
- **SDP relaxation.** Proposition 6.1 is the tightness condition of
  Jaldén–Martin–Ottersten (ICASSP 2003; via the easy review and
  Jiang–Liu–Bao–Jiang, arXiv 2102.04586, eq. (2.4)). Jaldén–Ottersten (IEEE
  TIT 2008) show that SDR achieves full diversity; Kisialiou–Luo (SIOPT 2010)
  and So (2010) give approximation ratios for the objective;
  Lu–Liu–Zhang–Zhang (SIOPT 2019, arXiv 1710.02048; abstract read) show that
  the conventional SDR is generally not tight for the PSK model and give an
  enhanced SDR that is tight under condition (1.4),
  `lambda_min(H^dagger H) sin(pi/M) > ||H^dagger v||_inf`, whose BPSK case
  implies the sufficient condition of Theorem 6.2 (via the easy review).
  Jiang et al. give necessary and sufficient conditions for the enhanced
  complex SDR. We did not check whether the threshold
  `2 beta log N/(sqrt(beta) - 1)^4`, the heuristic `2 beta log N/(beta - 1)^2`,
  or the square-system scaling `rho* ~ N^3` appear in these papers.
  Stojnic–Vikalo–Hassibi (IEEE TSP 2008, "Speeding up the sphere decoder with
  H-infinity and SDP inspired lower bounds"; from memory) use SDP-type bounds
  inside sphere decoding empirically; we found no node-count analysis.
- **Lower bounds for branch-and-bound on random instances.** Chvátal ("Hard
  knapsack problems", Oper. Res. 1980; via the hard review, not re-read) shows
  that random knapsack instances need `2^{Omega(n)}` nodes for a broad class
  of recursive algorithms. Dey–Dubey–Molinaro (arXiv 2103.09807; abstract
  read by the hard review) give exponential lower bounds for general
  disjunctions on packing, set-cover and TSP instances, including a smoothed
  bound for a Gaussian-perturbed cross-polytope; their positive result
  (arXiv 2007.15192) and Borst–Dadush–Huiberts–Tiwari show polynomial trees
  for random binary IPs with small gaps. Our lower bound is for a planted
  model with a convex quadratic objective and a nonlinear relaxation, where
  the relative root gap stays a constant.
- **Dey–Dubey–Molinaro and Kaibel–Weltge (mechanism).** The midpoint graph is
  the DDM cross-polytope argument with a convex objective; the counting bound
  of Theorem 4.3 is the non-pairwise "each leaf contains few points of a test
  set" argument (DDM's perturbed cross-polytope, Kaibel–Weltge hiding sets),
  here with an entropy estimate for families of `k`-sets with large average
  overlap (Lemma 4.2, elementary; we do not claim it as a contribution). The
  framework is the integer-core note's. The other mechanism named in the
  program, the certificate integral of Bachoc–Cesari–Gerchinovitz, concerns
  spatial branching and is not used.
- **Sibling workstreams.** In sparse regression
  ([`../sparse-regression/phase-transition.md`](../sparse-regression/phase-transition.md))
  the perspective relaxation is exact at the root above `2k log p`, and C1
  holds in a window below. The box relaxation behaves differently because the
  tangent cone of the box at a vertex is a full orthant: the relaxation gains
  `N/2` in every instance by moving all descent coordinates slightly, so C1
  needs each wrong fixing to cost a linear amount. In the integer-core
  random-CVP analysis, conflicts come from lattice points near the target;
  here they come from the box, which sidesteps (but does not resolve) the
  Gaussian-basis question of that note (Section 5).

## 9. What remains open

1. **Square systems, every node** (Conjecture 3.3): box inactivity of all
   single-fixing NNLS problems for `beta = 1`, which would follow from
   `P(U > c sqrt N) = o(1/N)` for the largest pure-noise NNLS coefficient `U`.
   The C1 threshold `N/4` itself follows from Hu–Lu (Theorem 3.1(d)); without
   that input the rigorous window is `[N/8, N/4]`.
2. **Sharp exponent** (Conjecture 4.5): `log(min tree) = (1 + o(1))
   (N/(4(2beta - 1) rho)) log rho` for every variable-branching rule. The
   upper half holds for the static order (Theorem 4.1). The class-number
   constant `c_beta` of Theorem 4.3 is about `10^{-5}`; the measured overlap
   threshold is about 10 times the proof's, and Lemma 4.2 loses a factor 2
   against the star family.
3. **Class number versus split trees.** Here `log kappa` and the static-order
   tree agree up to constants in the exponent, so general disjunctions gain at
   most a constant factor in the exponent over variable branching. Whether
   they gain a constant factor at all is open.
4. **Segment graph.** Whether `chi(G^seg)` stays bounded above `8 log N`
   (the hard review found it usually equal to 2 in small instances).
5. **SDP for square systems.** Is SDP-based B&B polynomial at
   `rho = c log N`, `beta = 1`? The SDP is not exact there (Section 6), and at
   `N <= 40` its relative root gap is about one half to two thirds of the box
   gap and does not decrease with `N`; so it may be superpolynomial too. A
   conflict or class-number analysis for the SDP relaxation (a spectrahedral
   relaxation in the lifted space) is not available. For tall systems, the
   sharp SDP exactness constant (heuristic `2 beta/(beta - 1)^2`) is not proved.
6. **Other relaxations.** Theorem 4.3 covers the box relaxation of `f` and
   weaker ones. Reformulations that use `x_i^2 = 1` (diagonal shifts, RLT, SDP)
   are not covered, and for `beta > 1` the uniform shift is already exact at
   `rho = Theta(log N)` (Proposition 6.3). For `beta = 1`, the effect of
   non-uniform shifts `diag(d)` with `A'A - diag(d) ⪰ 0` is open.
7. **Small SNR.** Theorems 4.3 and 5.1(b) need `rho >= rho_0` (71 for
   `beta = 1` with our constants) because the first-moment bound on
   `W - OPT` is crude. For `rho` below that, exponential trees are expected
   but not proved.
8. **Upper bounds for adaptive rules.** Theorem 4.1 is for a data-independent
   order. Most-fractional branching gave smaller trees than the static order in
   every cell of Table 7.3 where both rules finished (geometric means), but its
   tree size is not analysed.
9. **Linear SNR below C1.** For `rho = theta N` with `c_beta < theta <
   theta_c`, the bounds are `N^{O(1/theta)}` from above and only linear from
   below; whether trees stay `O(N)` somewhat below `theta_c` (C1 fails there,
   but a C1 failure does not force large trees) is open.
10. **Search for `beta > 1` between `2 log N/beta` and `4 log N/(2beta - 1)`.**
    The cited results do not give polynomial-time search there.

## 10. Revision after review (2026-09-29)

Two independent reviews checked this note:
[`../../reviews/mimo-easy-review.md`](../../reviews/mimo-easy-review.md)
(results 1, 2, 3, 5) and
[`../../reviews/mimo-hard-review.md`](../../reviews/mimo-hard-review.md)
(result 4). Neither found a counterexample to a theorem or a gap in a main
proof. Each change below was re-derived before it was made; new checks are in
`code/check_revision.py` (Appendix).

Easy review.

- **R1** Theorem 1.3 is known in substance (Hug–Schneider 2016;
  Godland–Kabluchko–Thäle 2022, Lemma 5.1 and (3.5); McCoy–Tropp 2014;
  chi-bar-squared). Section 1.2 now cites these, presents our proof as a
  self-contained derivation, and states part (a) for any column law invariant
  under single-column sign flips, with the deterministic identity
  `sum_eps 1{face(K_eps) = S} = 1` as its proof. Checked: the identity held in
  200 random configurations, including non-symmetric ones, and the face
  frequencies are uniform for Laplace and correlated Gaussian columns
  (part A). Section 8 and the Summary were changed accordingly.
- **R2** First-order ML achievability at `2 log N` for `beta = 1` is credited
  to Hansen et al. 2009 and Hassibi et al. 2014 (Theorem 2.2, Summary,
  Section 8).
- **R3** Proposition 6.1 is credited to Jaldén–Martin–Ottersten 2003; the
  sufficient condition of Theorem 6.2 is related to Lu et al.'s condition
  (1.4).
- **R4** New Theorem 3.1(d): for `beta = 1`, C1 fails below `(1-eps) N/4`
  given the Hu–Lu input already used in Corollary 1.6. The proof reduces one
  fixed single-fixing node to a root problem at SNR
  `theta(N-1)/(1 + 4theta)` (re-derived in Section 3). Conjecture 3.3 is now
  only the "every node" form, with a sufficient tail condition on the
  largest pure-noise NNLS coefficient and the review's tail data.
- **R5** The qualifier "incumbent `OPT` available when off-path nodes are
  examined, or best-bound search" is now stated wherever `2N+1` is claimed
  (Summary, Section 3, Corollaries 3.2 and 4.4).
- **R6** Theorem 1.7(a) is now stated under its actual feasibility condition
  `rho >= (1+eps) 2beta log N/(1+2beta)^2`, which is implied by the
  hypothesis of (c) for every `beta`.
- **R7** Proof of Theorem 3.1(c): the union bound over `N(N-1)` pairs now
  uses `sqrt(6 log N)`.
- **R8** Summary (3): `W - OPT` is bounded above by `N^{1 - c/2 + o(1)}`, not
  equal to it.
- **R9** The square-system SDP heuristic now uses the bottom eigenvectors of
  `K` (the rank-one heuristic was the wrong mechanism), and the exact
  threshold is written as `rho* = lambda_max(-D; K)_+^2`. Checked: the closed
  form equals our bisection to `4e-7`, and the bottom-five-eigenvector lower
  bound is within a factor 4 of `rho*` in 14 of 20 square instances
  (part B).
- **R10** "Exponential separation" is now "superpolynomial separation", and
  its dependence on Theorem 4.3 is stated.
- **R11** The rank-one heuristic is now described as loose for `beta = 1.5`.
- **R12** The square-system SDP and box gap ranges are described as
  seed-dependent and indicative, with the review's independent values.
- Theorem 2.2(d): the converse now says that it uses conditional independence
  of the one-bit events given `w`, and its hypothesis `rho beta -> inf` is
  replaced by `rho beta >= c0 > 0`.

Hard review.

- **C1, S1** Theorem 4.1 is sharpened: the sum of the `K` most negative
  `zeta_i` replaces `K` times the most negative one. The loss factor becomes
  `kappa_rho = 1 - sqrt(2 log(4(2beta-1) rho)/(rho beta)) - 1/sqrt(rho beta)
  -> 1` for every `rho -> inf`, and no ML condition is needed (the node bound
  is compared with `W >= UB`). Re-derived in Section 4.1 (expectation bound
  `E T_K <= K(sqrt(2 log(N/K)) + 1)` and Lipschitz concentration). Checked:
  the realized factor is 0.53–0.70 against `kappa_N = 0.11–0.50` at
  `N = 10^6`, and the concentration bound held (part C). The range of
  `Theta((N/rho) log rho)` in the Summary and Corollary 4.4 is now
  `rho -> inf`, `rho <= c' N`, plus fixed `rho >= 71` with the trivial upper
  bound.
- **C2, C3** Section 8: "the box relaxation does not change the order of the
  exponent of enumeration" was wrong for square systems. It is replaced by
  the natural-order Fincke–Pohst heuristic (exponent of order `N/sqrt(rho)`)
  and by our own measurement on the same instances: 839, 7937, 61289
  Fincke–Pohst nodes against 90, 168, 246 box static-order nodes at
  `N = 32, 48, 64` (part D). The Jaldén–Ottersten comparison now carries the
  `log rho` factor and the size of the constants.
- **C4** "Pairwise conflicts are blind" is now "midpoint conflicts are blind";
  the segment graph is listed as open.
- **C5** The two-sided midpoint-clique statement is now proved: Theorem
  5.1(a) includes the review's first-moment upper bound, re-derived. Checked:
  the last `n_1` with a non-negligible first moment is 3–15 times
  `N^{1-c/8}` at `N = 10^4, 10^5` (part E).
- **C6** The extrapolation is labeled heuristic in the Summary; Section 7.3
  notes that the predictor underpredicts the capped `N = 256` runs and that
  its agreement with Conjecture 4.5 checks the model, not real trees.
- **C7** Scope: the statements now say "for the box relaxation of `f`", and
  Theorem 4.3 lists what is not covered (reformulations using `x_i^2 = 1`).
  New Proposition 6.3 shows that for `beta > 1` the eigenvalue-shift
  reformulation is root-exact at `rho = Theta(log N)`. Checked: its root gap is
  0.066, 0.034, 0.010 and `4.7e-4` at `rho = 30, 60, 130, 300`, against 0.232
  for the box relaxation, and it is exact at `rho = 600` (`beta = 2`, part F).
  Relative-gap tolerances above `~1.4e-4 N` are excluded explicitly.
- **C8, C9** Theorem 4.3 now states `c'_1 ~ 1.4e-4`, the finite-`N` onset
  (`N ~ 1.7 10^7`), and the ratio `10^4 - 10^5` between the upper and lower
  exponents.
- **C10** The Papailiopoulos parenthetical is restricted to `beta = 1`; for
  `beta > 1` only search above `4 log N/(2beta-1)` is covered. Chvátal 1980
  and the Dey–Dubey–Molinaro smoothed bound are cited, and the gap is
  described as specific to box-relaxation certificates.
- Minor: `rho_1` of Theorem 5.1(b) is given (the review's estimate); Section 8
  notes that Theorem 4.3 applies to sphere decoders via the weaker-relaxation
  remark; the Gaussian-basis remark now says that the binary problem
  sidesteps integer-core Conjecture 3.8.

The tables of Section 7 are unchanged: no reviewed item affects them.

### 10.1 Recheck of the revisions (2026-09-29)

A fresh recheck,
[`../../reviews/mimo-recheck.md`](../../reviews/mimo-recheck.md), found all
five main revisions correct (Theorem 4.1 with the top-`K` sum, Theorem 3.1(d),
Proposition 6.3, the upper half of Theorem 5.1(a), and the Fincke–Pohst
comparison, which it reproduced exactly). Final fixes:

- **F1** The Summary's restatement of Theorem 4.1 now keeps the factor `N+1`
  (without it the sentence is false at `rho = Theta(N)`, where the path to
  `x*` alone has about `N` nodes).
- **F2** The shifted relaxation's gap at `rho = 300` is `4.7e-4` with
  `d = 0.99 lambda_min` (`3.9e-4` with `d = lambda_min`), not 0.000; it is not
  exact in any of the four instances there and exact in all four at
  `rho = 600`. Check part F now prints more digits, adds `rho = 600` and
  counts exact instances.
- **F3** Proposition 6.3 now includes part (b): the shift's threshold
  `2 beta log N/(sqrt(beta) - 1)^4` is sharp (the KKT condition is an iff;
  Bai–Yin and the Gaussian maximum give the converse). The text states that
  the shift becomes exact only from there on, far above the SDP (medians
  `73–110 log N` against `4.4 log N` at `beta = 2`).
- **F4** Conjecture 3.3 and the text after the proof of Theorem 3.1(d) now
  say that the tail bound `P(U > c sqrt N) = o(1/N)` implies the "every node"
  statement; it is not claimed to be equivalent.
- **F5** Theorem 3.1 now fixes `theta > 0` and records where the proofs use
  `theta N >> log N`.
- **F6** The Fincke–Pohst comparison is stated in node counts; the per-node
  costs differ, and in single-thread Python the sphere decoder was faster in
  wall-clock time at `N = 64` (0.8 s against 3.4 s).
- **F7** The `N = 10^5`, `c = 3` cell of check part E hit the loop limit; the
  rerun without the limit gives 20199 (ratio 15.1), so "3–15" stands.
- **F8** The status line now records the reviews.
- **F9** Section 4.1 now quotes the proved factor `kappa_rho = 0.20–0.68` at
  practical sizes (prefactor `1/kappa_rho` = 1.5–5; check part G).
- **F10** In the proof of Theorem 5.1(a) ternary vectors are now denoted `q`,
  so `c` means only `rho beta/log N`.

Closing audit
([`../../reviews/closing-audit-b.md`](../../reviews/closing-audit-b.md),
item 2): all of F1–F10 were confirmed, including Proposition 6.3(b) and the
shifted-relaxation gaps. Two changes followed.

- The displayed bound of Theorem 4.1 did not imply its own log form, nor the
  Summary's `(N+1)`-factor sentence, at `rho = Theta(N)`: rounding `K` up costs
  an extra factor of order `N` when every node with `|Wr| <= K` is counted.
  The proof now counts only children of branched nodes, which have at most
  `K - 1` wrong fixings: `#nodes <= 1 + 2 sum_{i=1}^{K} C(N, i) <= 1 + 2
  (eN/K)^K`. Both the log form and the Summary sentence now follow for every
  `rho -> inf`, `rho beta <= N` (re-derived in the proof).
- F9 wording: 1.5–5 is the prefactor `1/kappa_rho`; the whole proved exponent
  is 2–8.5 times the asymptotic one at `N = 10^6` (recomputed).

## Appendix: code, commands, and what each check establishes

Code (`code/`):

- `core.py`: instance generator (identical to the scout's `bls.py`), node
  relaxation in error coordinates (NNLS, upper-bound active set, BVLS
  fallback) with the certified Frank–Wolfe bound, best-first B&B (`maxfrac`,
  `static`), single-fixing node values, SDP bound (CVXPY/Clarabel, certified
  dual bound) and the SDP certificate eigenvalue.
- `test_core.py`, `check_lemmas.py`: targeted checks (Section 7 preamble; `test_core.py` also checks the knapsack DP against brute force).
- `exp_root.py` (Table 7.1), `exp_c1.py` (Table 7.2),
  `check_node_inactivity.py` (Section 7.2), `exp_trees.py` (Table 7.3),
  `predict_trees.py` (Table 7.3b), `knapsack_predictor.py` (Table 7.3c),
  `exp_thresholds.py` (Table 7.4), `exp_sdp.py` (Table 7.5),
  `summarize.py` (all tables), `check_revision.py` (checks added after review,
  Section 10).

Commands (from `data/`, with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`):

- From `code/`: `python3 test_core.py | tee ../data/test_core.log` and
  `python3 check_lemmas.py | tee ../data/check_lemmas.log`.
- `python3 ../code/exp_root.py root.jsonl`.
- `python3 ../code/exp_c1.py c1.jsonl N beta THETAS SEEDS 2` for
  `N = 100, 200` (8 seeds) and `400` (6 seeds) with
  `THETAS = 0.25,0.35,0.5,0.75,1.0,1.5,2.0` (`beta = 1`) and
  `0.083,0.12,0.17,0.25,0.35,0.5,0.75` (`beta = 2`); `N = 800`:
  `0.3,0.35,0.4,0.5` with 4 seeds (`beta = 1`); for `beta = 2`, seeds 0–1 at
  `theta = 0.1` from an interrupted run of `... 800 2 0.1,0.12,0.14 3 1`, then
  `python3 ../code/exp_c1.py c1.jsonl 800 2 0.12,0.14 2 2`.
- `python3 ../code/check_node_inactivity.py > node_inactivity.log`.
- `python3 ../code/exp_trees.py trees_b1.jsonl 32,64,128 r2,r4,r8,r16,c4,c8,c16 1 6 200000 3`
  (the `N = 128` rows with `r2, r4, r8` were rerun after a solver speed-up,
  which does not change node values; `N = 128`, `r16` has 2 seeds);
  `python3 ../code/exp_trees.py trees_b1_256.jsonl 256 r2,c16,c8,r4,r8,c4,r16 1 4 100000 3`;
  `python3 ../code/exp_trees.py trees_b2.jsonl 64,128 r4,r8,r16,c4,c8 2 4 100000 1`.
  Tags: `rK` means `rho = N/K`, `cK` means `rho = K log N`.
- `python3 ../code/predict_trees.py trees_b1.jsonl trees_b1_256.jsonl trees_b2.jsonl > predict_trees.log`.
- `python3 ../code/knapsack_predictor.py knapsack.jsonl`.
- `python3 ../code/exp_thresholds.py thresholds.jsonl`.
- `python3 ../code/exp_sdp.py sdp.jsonl a` and `python3 ../code/exp_sdp.py sdp.jsonl b`.
- `python3 ../code/summarize.py > tables.txt` prints Tables 7.1–7.5 (7.3b is `predict_trees.log`).
- Revision checks (Section 10), from `code/`:
  `python3 check_revision.py A B C > ../data/check_revision_ABC.log`,
  `python3 check_revision.py D > ../data/check_revision_D.log`,
  `python3 check_revision.py E F G > ../data/check_revision_EFG.log` (rerun
  after the recheck: part E without the loop limit, part F with `rho = 600`
  and an exactness count, new part G).

What the checks establish. Tables 7.1 and 7.2 test the exact laws and the C1
thresholds at finite `N`; every C1 outcome is certified by dual bounds or by a
primal node value. Table 7.3 gives certified B&B tree sizes (pruning only on
certified bounds) for specific rules; they illustrate, but cannot test, the
asymptotic rates. Tables 7.3b–c test the exact-law mechanism against real
trees and extrapolate it; the extrapolation is a heuristic model, not a
certificate. Table 7.4 samples the exact single-coordinate law. Table 7.5
computes exact per-instance SDP tightness thresholds (bisection on a concave
eigenvalue function) and certified SDP bounds. None of the computations is
evidence for the asymptotic constants beyond the trends described.







