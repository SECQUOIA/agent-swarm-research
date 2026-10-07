# Matching Theorem 3.4 without knowing `x*`: graded refinement around the minimizing configuration

Date: 2026-09-30. Extension of Part A of
[`extension-adaptive.md`](extension-adaptive.md) (its Section D, "the main
open problem of Part A"). Status: **revised after review rounds 1 and 2**
([`../reviews/adaptive-matching-review.md`](../reviews/adaptive-matching-review.md),
[`../reviews/adaptive-matching-confirm-r1.md`](../reviews/adaptive-matching-confirm-r1.md));
the changes are listed in "Revision after review" at the end. Proofs are
complete where the status table says "proved". Computations are
floating-point illustrations, not certified counts. Scripts and logs are in
[`adaptive2/`](adaptive2/).

Cited notes:

- [D] [`decomposition-certificates.md`](decomposition-certificates.md)
  (Definition 1.2, Lemmas 1.3–1.5, Lemma 3.2 and identity (3.1),
  Theorem 3.4, Remark 3.6, Section 5.4);
- [E] [`extension-adaptive.md`](extension-adaptive.md) (algorithm LS,
  Lemmas A.2–A.4, Theorem A.5, Proposition A.6, Conjecture A.7, algorithm
  RC, Section B.1, Conjecture B.5, Section D);
- [Cov] [`covering-upper-half.md`](covering-upper-half.md) (exact-bag model,
  Lemma 0, Theorem 1, Lemma 1', Proposition 1.3, rule `bd` of
  Corollary 3.2, Proposition 5);
- the reviews of these notes in [`../reviews/`](../reviews/)
  (`decomposition-review.md`, `decomposition-recheck.md`,
  `decomposition-adaptive-review.md` and its confirmations,
  `covering-upper-half-review.md` and its confirmations), and the reviews of
  this note, `adaptive-matching-review.md` (round 1) and
  `adaptive-matching-confirm-r1.md` (round 2).

Notation is that of [D] and [E]: bags `V_t`, separators `S_t`, `|T|` bags,
width `w` (so `|V_t| <= w + 1`, `|S_t| <= w`), `k = max_i |T_i|`, (QG) with
`x*` and `c_g`, (L^{1,1}) with `M_a`, (U^q) with `alpha'` and `A`,
configurations and their value (Lemma 1.5 of [D]), consistent points and
slopes `lambda_t(x)` (Lemma 3.2 of [D]).

**October 2 update.** The unrestricted branching-tree property `(Loc_T)`
below is false: a [finite-certificate counterexample](../../research-20261002/tree-localization/counterexample.md),
[independently reviewed](../../research-20261002/reviews/tree-localization-adversary.md),
has fixed branching, width, conditioning and factor constants, exact slopes,
and `theta=0`, yet every minimizing configuration has an unbounded
root-distance-to-mesh ratio as the tree grows. The optional
branching-versus-conditioning restriction in Conjecture 7, and localization
only for GR-reachable partitions, remain open. A
[different shared-grid algorithm](../../research-20261002/geometric-dp/theorem.md)
obtains a conditioning-dependent polylogarithmic accuracy bound on arbitrary
decomposition trees, also with boundary minimizers. Its certificate format
and logarithmic power differ from Theorem 2 here.

## Summary

**Question** ([E], Section D). Is there an algorithm that knows neither `x*`
nor the problem constants, uses no local solver, and needs
`|T| C^{w+1} polylog(|T|/eps)` boxes under the hypotheses of Theorem 3.4 of
[D]? Algorithm LS of [E] needs `|T| (C sqrt|T|)^{w+1} log(|T|/eps)`
(Theorem A.5), and the factor `|T|^{(w+1)/2}` is real for LS
(Proposition A.6).

**Answer.**

1. **Yes for path decompositions under the extra hypothesis (S)**
   `∇F(x*) = 0` (for example when `x*` is interior); the decomposition tree
   `T` is a path, with any width `w` and any `k`. Theorem 3.4 of [D] needs
   neither (S) nor a path (but needs `x*`). The algorithm is GR
   (Section 3). At stage `j` it has a core width `W_j = s0 2^{-j}`. It runs
   the dynamic program of Lemma 1.5 of [D] once, takes a minimizing
   configuration, and refines, in every bag, the
   leaves (and the cells of the bag's separator) near that bag's copy: boxes
   within sup-distance `R W_j` of the copy get width `W_{j+1}`, and widths
   grow at the rate `theta` beyond. Slopes are the gradients `lambda(x)` at
   the previous consistent point, and the incumbent is the best value of
   `F` at consistent points. GR uses no pruning, no min-marginals, no
   monotone relaxations (M), no knowledge of `x*` and no local solver.

   **Theorem 2 (proved).** If `theta <= theta*` and `R >= 3 K*` (explicit
   constants that depend only on `k`, `w`, `M_a/c_g` and `alpha' A/c_g`), GR
   stops after at most `j* + 1` stages,
   `j* = max(0, ceil(log2(s0 sqrt(C_term |T|/eps))))`, with a certificate
   proving tolerance `eps` and an incumbent within `eps` of `f*`. It
   creates at most `2 |T| j* (4R + 4/theta + 4)^{w+1}` boxes and runs the
   dynamic program `j* + 1` times. So the count is
   `|T| C^{w+1} log(|T|/eps)` with `C = poly(k, w, M_a/c_g, alpha' A/c_g)`,
   the form of Theorem 3.4 of [D], but with a larger polynomial: the
   proved base is quadratic in `M_a/c_g` (`K* = Theta(k^5 w^2 kappa^2)`
   for bounded `alpha' A/c_g`), while the base of Theorem 3.4 of [D] is
   linear in `M_a/c_g`. The constants are far from practice: on the path
   family of Section 8.1, `theta* ≈ 8.2e-8` and the base
   `4R + 4/theta + 4` is about `8.8e9`; the computations use `theta = 1/8`,
   `R = 4`, base 52.
   **Corollary 3 (proved):** unknown constants cost one more logarithmic
   factor, by running GR with `theta = 2^-mu`, `R = 2^mu` for
   `mu = 1, 2, ...` under doubling budgets (the box budget is checked before
   every split, so a run aborts as soon as it would exceed its budget).

2. **The key step is a localization lemma (Lemma 1, proved for path
   decompositions).** Let a minimizing configuration have leaves and cells
   of width at most `W + theta` times their sup-distance to `x*`. Then every
   bag copy of it lies within sup-distance `K W` of `x*`, with `K`
   independent of `|T|`. The proof is a local exchange: on a window of bags
   around a far bag, replace the configuration by `x*`; quadratic growth
   pays for the replacement, and on a path the window has only two boundary
   edges.

   **Corollary 4: Conjecture A.7 of [E] holds for path decompositions**
   (under `∇F(x*) = 0`, with LS's slope rule). At a failed sublevel of LS
   the minimizing configuration consists of boxes of side `s_i`, so
   Lemma 1 applies with `theta = 0`. So in LS the minimizing configuration
   is localized to `O(s_i)`, while the set of live boxes is not
   (Proposition A.6). GR refines only around the minimizing configuration.

3. **Branching trees: open.** Apart from a constant in the slope bound,
   Lemma 1 is the only step of Theorem 2 that uses the path structure. For a
   tree decomposition (still with (S)), Theorem 2 holds once a localization
   property with a fixed point in the slope error holds (property (Loc_T) of
   Remark 3.3); a localization bound `K_1(gamma, theta)` that is independent
   of `|T|` but has no growth condition in the slope error `gamma` is not
   enough, because GR's slope errors grow with the localization radius. The proof of
   Lemma 1 fails on trees because a window of bags can have many boundary
   edges (Section 6). A sketch (not proved) extends it to decomposition
   trees with `L` leaves; with GR's lagged slopes the fixed point then gives
   a base of order `L`, so the count would beat LS only for
   `L = o(sqrt|T|)` (the first version claimed `sqrt(L)` and an
   interpolation between Theorem 2 and LS; that ignored the fixed point and
   is withdrawn). On a binary-tree family (`b = 0.55`, up to 127 vertices;
   the two runs with 127 vertices were stopped by hand about three stages
   before their stop, to limit computation) GR keeps the localization ratio
   at 4 with `c = 0`, and the split count per bag per stage constant. With
   random linear terms the ratio rises slowly with the size (3.4 to 4.9 for
   7 to 63 vertices, 5.3 in the first ten stages with 127). In every tested
   family the conditioning gets worse with the size (Sections 8.3–8.4), so
   these runs do not separate size from conditioning. With the conditioning held
   fixed (`0.9 - |b| rho(A)/2 = 0.141`) and `theta = 1/8`, the tree ratio is
   5 for 7 and 15 vertices and 10–18 for 31 and 63 vertices, while the path
   family, whose `c_g` is between 0.100 and 0.119 at `n = 256`, keeps ratio
   3 at `theta = 1/8` up to `n = 256`. So at these sizes the tree family
   needs a smaller `theta` than the path family at comparable conditioning;
   the tree
   decomposition also has `k = 3` instead of 2, so this does not isolate
   branching. (The first version compared the trees with a `b = 0.88` path
   as "similar conditioning" and concluded that the tree data reflect a
   too-large `theta` rather than branching; that comparison used
   infinite-size bounds on `c_g`, and the conclusion is withdrawn.) I state
   localization on trees as Conjecture 7.

4. **Rule `bd` does not match (Proposition 6, lower bound proved).**
   Rule `bd` of [Cov] refines a separator cell while the cell bracket of
   Theorem 1 of [Cov] exceeds `eps/n`. Even in the exact-bag model, with
   exact value functions, on the strongly convex quadratic path
   `F = sum_t s_t^2 + b sum_t s_t s_{t+1}` (one-dimensional separators
   `s_t`) it needs at least `c n^{3/2} log(1/eps)` cells. The scope of the
   proof is rule `bd` as defined in [Cov] on this path: the graded split
   `psi` and the discount `w_e/(2n)` of Theorem 1 of [Cov], exact value
   functions, one-dimensional separators, separator cells counted. Cells
   graded at a constant ratio, with a split built from the reduced value
   functions, certify the same tolerance with 72–96 cells per edge for
   `n <= 256` (`b = 0.8`, `eps = 1e-6`; computed), while `bd` uses
   `9.4 sqrt(n)` per edge, 152 at `n = 256`. In the proof the loss comes from
   the discount `w_e/(2n)`: it shares the margin equally among the edges,
   which costs `sqrt(n)` cells per edge per halving (proved for
   one-dimensional separators). *Conjecture, not proved:* for separators of
   dimension `w >= 2` the cost is `sqrt(n)` per separator dimension, that is
   `n^{w/2}` cells per edge per halving. *Heuristics, not proved:* this is
   the same loss as LS; Lemma 1' of [Cov] imposes the same equal share on
   the leaves; and the brackets need the exact value
   functions, whose computable surrogates (min-marginals) should carry the
   global relaxation error that makes LS pay `|T|^{(w+1)/2}` (Section 5). So
   I took a different route: localization.

5. **Reading (R1) of the covering upper half for certificates: not
   settled.** Under (QG) it was already known for certificates ([E],
   Section B.1, from Theorem 3.4 of [D]); Theorem 2 makes it algorithmic for
   path decompositions with (S) (`∇F(x*) = 0`). Without (QG) there is no
   point to localize, and nothing here applies (Section 7).

**Numerical checks** (Section 8; floating point, path family of
Theorem 4.1 of [D] unless stated):

- With `c = 0` and learned slopes and incumbent, GR with `theta = 1/8`,
  `R = 4` needs 12.1k–17.1k boxes per bag for `n = 4, ..., 256` at
  `eps = 1e-4`. Per bag it grows only through the index of the stopping
  stage (11 to 14, that is, 12 to 15 dynamic-program runs). Per stage at
  most 639 leaves per bag are split (bound 676).
- At `n = 64`, `eps = 1e-4`, GR (`theta = 1/8`) ends with 0.97M boxes and
  processes 4.7M; LS ends with 2.20M and processes 36.4M. At `n = 64`,
  `eps = 1e-6`, GR ends with 1.42M boxes, LS with exact slopes and exact
  incumbent with 2.40M, and the shell certificate of [D] centred at `x*`
  has 2.35M.
- Localization: `max_t |z^t - x*_{V_t}|_inf = 3.000 W_j` at every late
  stage for `c = 0` (all `n`, both tolerances), and 3.1–5.7 `W_j` with
  random linear terms (`n = 8, 16, 32`).
- `theta = 1/4` fails at `n = 32`: the minimizing configuration jumps to
  `704 W_j` from `x*` and the gap stalls; `theta = 1/8, 1/16, 1/32` work.
  On the path with `b = 0.88`, `theta = 1/8, 1/16, 1/32` lose
  localization at `n = 8, 16, 64` respectively; there `c_g` falls with `n`
  (lower bound 0.073 at `n = 8`, 0.035 at 16, 0.021 at 64), so these runs
  mix chain length and conditioning. With the conditioning held fixed,
  `theta = 1/16` keeps ratio 3 for `n = 8, ..., 64` at `c_g` lower bound
  0.073, but at lower bound 0.035 it works for `n = 8` and fails for
  `n = 16`. So both conditioning and chain length matter in the tested
  range, and an `n`-independent threshold was not observed at the worse
  conditioning (Theorem 2 guarantees one only below its tiny `theta*`).
  With `R = 12 >= 3 * 3`, no box wider than `W_j` is ever split, as the
  proof of Theorem 2 predicts.
- Boundary minimizers (exploratory, not covered by Theorem 2): with a
  vertex minimizer and with a face minimizer (`∇F(x*) ≠ 0`) GR stops and
  the ratio stays at most 0.64 and 3.18 (`n = 8, 16`). This suggests, but
  does not prove, that (S) is an artifact of the proof.
- Binary trees and the bracket rule: items 3 and 4 above.

**Significance and novelty.** For path decompositions, and under the extra
hypothesis (S) (`∇F(x*) = 0`), this gives an algorithm with the form of
Theorem 3.4 of [D] (a certificate built around a known `x*`): the algorithm
needs `|T| C^{w+1} log(|T|/eps)` boxes without knowing `x*`. Its proved
base is larger: quadratic in `M_a/c_g` instead of linear, with numerically
vacuous constants on the tested family (Section 3.2). Theorem 3.4 of [D]
needs neither (S) nor a path. The mechanism is not pruning but
localization: the minimizing configuration of the relaxed dynamic program
points to `x*` to the accuracy of the current core width, in every bag, so
the algorithm can grade its partitions as if it knew `x*`. Refining
shrinking neighbourhoods of the current dynamic-programming-optimal
trajectory is an old idea: discrete differential dynamic programming
(Heidari et al. 1971) and Luus's iterative dynamic programming do this, and
Munos and Moore (2002) refine dynamic-programming discretizations
adaptively. From the abstracts I read, these methods give neither certified
lower bounds nor complexity bounds. The closest locality result I found is
Shin, Anitescu and Zavala (SIAM J. Optim. 2022): exponential decay of
sensitivity in graph-structured NLPs, a local statement about exact
solutions (Section 9). I did not find the localization lemma for relaxed
decomposition dynamic programs, a certificate-producing algorithm with this
instance-dependent count, or a lower bound like Proposition 6. The searches
were short and at the level of abstracts and search snippets; they do not
establish novelty.

## Status

| Item | Content | Status |
|---|---|---|
| Lemma 1 | sup-norm localization of minimizing configurations whose boxes have width `<= W + theta dist(box, x*)` (path decompositions, `∇F(x*) = 0`) | proved |
| Theorem 2 | algorithm GR: certificate proving `eps` with at most `2\|T\| j* (4R + 4/theta + 4)^{w+1}` boxes created, `j* = O(log(\|T\|/eps))` | proved (path decompositions, with (S) `∇F(x*) = 0`) |
| Corollary 3 | unknown constants: dovetailing over `theta = 2^-mu`, `R = 2^mu`, box budget checked before every split; one more logarithmic factor | proved (budget enforcement made explicit after review) |
| Remark 3.3 | any tree decomposition: Theorem 2 holds if property (Loc_T) (localization with a fixed point in the slope error) holds; tree slope bound corrected | proved (conditional; corrected after review) |
| Corollary 4 | Conjecture A.7 of [E] for path decompositions | proved (under `∇F(x*) = 0`) |
| Proposition 6 | rule `bd` of [Cov] (graded split `psi`, discount `w_e/(2n)`, exact value functions) needs `>= c n^{3/2} log(1/eps)` cells on a strongly convex quadratic path with one-dimensional separators (exact-bag model) | proved (one-dimensional separators only); graded alternative with `O(log(n/eps))` cells per edge computed for `n <= 256` |
| Section 6, trees with `L` leaves | at fixed slope error, Lemma 1 with `K_1 = O(sqrt(L))`; with GR's lagged slopes the fixed point gives `K_T = O(L)`, hence `\|T\| (C L)^{w+1} log(\|T\|/eps)` | sketch (conclusion corrected after review) |
| Conjecture 7 | (Loc_T) for tree decompositions with bounded branching | unrestricted form disproved by the October 2 update; the version with an additional branching/conditioning restriction remains open |
| Reading (R1) of the covering upper half, certificates, without (QG) | | open |

## 1. Setting

### 1.1 Path decompositions

Throughout Sections 1–4:

- `X0` is a cube of side `s0` (for a box, rescale the coordinates; this
  changes `M_a` and `c_g`). Leaves of bag `t` are dyadic cubes in the
  coordinates `V_t`, cells of `S_t` dyadic cubes in the coordinates `S_t`,
  as in LS ([E], Section 0). (Lemma 1 itself does not need dyadic boxes.)
- The decomposition tree is a path: bags `1, ..., N` (`N = |T|`), root `1`,
  parent of `t` is `t - 1`. By running intersection each variable `i` lies in
  an interval of bags `T_i = [l_i, r_i]` with `r_i - l_i + 1 <= k`. The
  separator of bag `t >= 2` is `S_t = V_t ∩ V_{t-1}`, and `|S_t| <= w` (no
  bag is contained in its parent, as in [D]). I assume `k >= 2`.
- Hypotheses: (QG), (L^{1,1}), (U^q) as in Theorem 3.4 of [D], and

  **(S)** `∇F(x*) = 0`, which holds when `x*` is interior.

  (S) and (L^{1,1}) give `F(x* + delta) - f* <= (k M_a/2) |delta|^2` for
  `x* + delta in X0`: subtract `∇F(x*) delta = sum_t ∇a_t(x*) delta_{V_t}`
  and use that each variable lies in at most `k` bags. With (QG) this
  forces `c_g <= k M_a/2`.
- Write `kappa = M_a/c_g` (so `kappa >= 2/k`) and `a = alpha' A/c_g`.

Fix partitions, slopes `lambdâ_t` (`t >= 2`) and maximal `beta`, so that the
root bound `l_r` is the minimum of the value `Phi` over configurations
(Lemma 1.5 of [D]). A configuration `c` consists of leaves `B_t ∋ z^t` and
cells `D_t ∋ z^t_{S_t}` (`t >= 2`) with `D_t ∩ (B_{t-1})_{S_t} ≠ ∅`. Put

- `rho_t = |z^t - x*_{V_t}|_inf` (deviation of the copy of bag `t`),
  `rhô_t = max { rho_u : t - k + 1 <= u <= t }`;
- `d_t = |z^t_{S_t} - z^{t-1}_{S_t}|_inf` (drift on edge `t`);
- the consistent point `x`, `x_i = z^{l_i}_i`, and
  `Delta_t = |z^t - x_{V_t}|_inf`;
- `nu_t = |lambdâ_t - lambda_t(x*)|_2`, the slope error on edge `t`.

### 1.2 The value of a configuration

By Lemma 1.5 of [D],
`Phi(c) = sum_t f_{t,B_t}(z^t) + sum_{t >= 2} lambdâ_t^T (z^{t-1}_{S_t} - z^t_{S_t})`,
where `f_{t,B} = sum_{c at t} f_{c,B_c}`. Lemma 3.2 of [D] with `x° = x*`
(identity (3.1) there) gives, for every configuration,

```
Phi(c) = F(x) + sum_t T_t(c) - sum_t err_t(c) + sum_{t >= 2} sigma_t(c),                    (1.1)
T_t(c)     = a_t(z^t) - a_t(x_{V_t}) - ∇a_t(x*_{V_t})^T (z^t - x_{V_t}),
err_t(c)   = a_t(z^t) - f_{t,B_t}(z^t)  in [0, (alpha' A/4) w(B_t)^2],
sigma_t(c) = (lambdâ_t - lambda_t(x*))^T (z^{t-1}_{S_t} - z^t_{S_t}).
```

### 1.3 Elementary bounds

Say that a box `Y` (leaf of bag `t` or cell of `S_t`) satisfies **(W_theta)**
if `w(Y) <= W + theta dist_inf(Y, x*)` (distance to `x*_{V_t}`, resp.
`x*_{S_t}`). If all leaves and cells of `c` satisfy (W_theta), then:

- **(E1)** `d_t <= 2W + theta (rho_t + rho_{t-1})`. *Proof:* `D_t` contains
  `z^t_{S_t}` and meets `(B_{t-1})_{S_t}`, which contains `z^{t-1}_{S_t}`; so
  `d_t <= w(D_t) + w(B_{t-1})`, and `dist(D_t, x*) <= rho_t`,
  `dist(B_{t-1}, x*) <= rho_{t-1}`.
- **(E2)** `Delta_t <= 2(k-1)(W + theta rhô_t)`. *Proof:* for `i in V_t`,
  `z^t_i - x_i = sum_{u = l_i + 1}^{t} (z^u_i - z^{u-1}_i)`, at most `k - 1`
  terms, each at most `d_u` with `u, u - 1 in [t - k + 1, t]`.
- **(E3)** `|T_t(c)| <= M_a (w+1)(rho_t Delta_t + (3/2) Delta_t^2)`.
  *Proof:* `z^t` and `x_{V_t}` differ only in the `<= w` coordinates of
  `S_t` (for `i in V_t \ S_t`, `l_i = t`), so
  `|z^t - x_{V_t}|_2 <= sqrt(w) Delta_t`, and
  `|x_{V_t} - x*_{V_t}|_2 <= sqrt(w+1)(rho_t + Delta_t)`. Split `T_t` into
  the Taylor remainder at `x_{V_t}` and
  `(∇a_t(x_{V_t}) - ∇a_t(x*))^T (z^t - x_{V_t})`.
- **(E4)** `err_t(c) <= (alpha' A/4)(W + theta rho_t)^2` and
  `|sigma_t(c)| <= nu_t sqrt(w) d_t`.

## 2. Localization of minimizing configurations

Put

```
eta    = (16 k (k+1)(w+1) kappa)^{-1/2},
theta_1 = min{ 1/(32 k^2),  eta/(8k),  1/(648 k^4 (w+1) kappa),  1/(k^{3/2} sqrt(108 a)) },
Q(gamma, theta) = (w+1)(k-1)^2 kappa (144 k^3 (w+1) kappa + 12) + a/2 + 2 gamma kappa sqrt(w)
                  + 288 k (k+1) w gamma^2 theta^2 kappa^2,
K_1(gamma, theta) = max{ 32 k^2/eta,  sqrt(16 k (2k+1) Q(gamma, theta))/eta }.
```

(If `a = 0` the last term of `theta_1` is absent.)

**Lemma 1 (sup-norm localization on path decompositions).** Assume the
setting of Section 1.1 with (QG), (L^{1,1}), (U^q) and (S). Let a
certificate (any partitions, slopes `lambdâ`, maximal `beta`) have per-edge
slope errors `nu_t <= gamma M_a W` for some `W > 0` and `gamma >= 0`. Let
`c` be a minimizing configuration (`Phi(c) = l_r`), and suppose that all its
leaves and cells satisfy (W_theta) with `0 <= theta <= theta_1`. Then

```
rho_t = |z^t - x*_{V_t}|_inf <= K_1(gamma, theta) W     for every bag t.
```

The hypothesis concerns only the boxes of `c`, not the whole partition.

*Proof.* Let `rho = max_t rho_t = rho_{t0}` and suppose `rho > K W` with
`K = K_1(gamma, theta)`. I construct a configuration `c'` of the same
certificate with `Phi(c') < Phi(c)`, which contradicts minimality.

*Step 1 (window).* Call bag `t` heavy if `rho_t > eta rho`, light otherwise;
`t0` is heavy. Let `U0 = [a0, b0]` be the smallest interval that contains
`t0`, has heavy endpoints, and has no heavy bag in `[a0 - 2k, a0 - 1]` or in
`[b0 + 1, b0 + 2k]` (start from `[t0, t0]` and extend to any heavy bag within
distance `2k`). Put `U = [a, b] = [max(1, a0 - k), min(N, b0 + k)]`. Then:

- (U1) the bags of `[a - k, a + k - 1] ∩ [1, N]` (if `a > 1`) and of
  `[b - k + 1, b + k] ∩ [1, N]` (if `b < N`) are light;
- (U2) the heavy bags of `U` lie in `[a0, b0]`; `U` has at most
  `2k |H_U|` light bags, where `H_U` is the set of its heavy bags, so
  `|U| <= (2k+1)|H_U|`;
- (U3) let `I = {i : T_i ⊂ U}`, `J_L = S_a` if `a > 1` (else empty) and
  `J_R = S_{b+1}` if `b < N` (else empty). Every variable of a bag of `U`
  lies in `I ∪ J_L ∪ J_R`. `J_L ∩ J_R = ∅`, because a common variable would
  lie in all bags of `[a - 1, b + 1]`, more than `2k + 2 > k` bags. Every
  variable of a heavy bag `s` of `U` lies in `I`, because
  `T_i ⊂ [s - k + 1, s + k - 1] ⊂ [a + 1, b - 1]` (or reaches an end of the
  path).

*Step 2 (repair).* Define `c'` equal to `c` outside `U`. For `s in U` put
`z'^s_i = x*_i` (`i in I`), `z'^s_i = z^a_i` (`i in J_L`), and
`z'^s_i = z^{b+1}_i` (`i in J_R`); let `B'_s` be any leaf of `L_s` that
contains `z'^s`; for `a < s <= b` let `D'_s` be a cell of `P_s` that contains
`z'^s_{S_s}`; keep `D_a` if `a > 1`. This is a configuration:

- on an edge `s in (a, b]` the two copies coincide (every variable of `S_s`
  gets the same value in both bags), so `D'_s` meets `(B'_{s-1})_{S_s}`;
- on edge `a`, `z'^a_{S_a} = z^a_{S_a} in D_a`, and `D_a` meets the unchanged
  `(B_{a-1})_{S_a}`;
- on edge `b + 1`, `z'^b_{S_{b+1}} = z^{b+1}_{S_{b+1}} in D_{b+1}`, which
  therefore meets `(B'_b)_{S_{b+1}}`.

Only the boxes of `c'` inside `U` are new. Their widths do not matter: they
enter only through `err_s(c') >= 0`, which lowers `Phi(c')`.

The consistent point `x'` of `c'` equals `x` except that `x'_I = x*_I` and
`x'_i = z^{b+1}_i` for `i in J_R`. By (U1), every variable of `J_L ∪ J_R`
has its top bag `l_i` in a light bag, so `|x_i - x*_i| <= eta rho` there. By
(E1) and (U1), every drift on the edges `[a - k + 2, a]` and
`[b - k + 3, b + 1]` is at most `2W + 2 theta eta rho`. Write
`delta rho = (k-1)(2W + 2 theta eta rho)`; since `rho > KW`,
`delta <= 2(k-1)(1/K + theta eta)`.

*Step 3 (gain).* By (1.1) for `c` and `c'`,

```
Phi(c) - Phi(c') = [F(x) - F(x')] + sum_t [T_t(c) - T_t(c')] - sum_t [err_t(c) - err_t(c')] + sum_t [sigma_t(c) - sigma_t(c')].
```

Let `x̂` be `x` with `x_I` replaced by `x*_I`. The bags that contain
variables of `I` are bags of `U`, and these contain only variables of
`I ∪ J` (`J = J_L ∪ J_R`). So
`F(x) - F(x̂) = F(x_I, x_J, x*_O) - F(x*_I, x_J, x*_O)` (`O` = the other
variables). By (QG) the first term is at least
`f* + c_g (|x_I - x*_I|^2 + |x_J - x*_J|^2)`, and by (S) the second is at
most `f* + (k M_a/2)|x_J - x*_J|^2`. With `|J| <= 2w`,

```
F(x) - F(x̂) >= c_g |x_I - x*_I|^2 - k w M_a eta^2 rho^2.
```

`x̂` and `x'` differ only on `J_R`, by at most `delta rho` per coordinate,
inside the `2k - 2` bags `[b - k + 2, b + k - 1]`, where both points deviate
from `x*` by at most `eta rho` in sup norm. Subtracting
`∇F(x*)(x̂ - x') = 0` and using (L^{1,1}) bag by bag,
`|F(x̂) - F(x')| <= (2k - 2) M_a (w+1) eta delta rho^2`.

For a heavy bag `s` of `U`, take `i` with `|z^s_i - x*_i| = rho_s`. By (E2),
`|x_i - z^s_i| <= Delta_s <= 2(k-1)(W + theta rho) <= eta rho/2`, using
`K >= 32 k^2/eta` and `theta <= eta/(8k)`. So `|x_i - x*_i| >= rho_s/2`, and
`i in I` by (U3). A variable serves at most `k` bags, so

```
c_g |x_I - x*_I|^2 >= (c_g/(4k)) Sigma_H,       Sigma_H := sum_{s in H_U} rho_s^2   (>= rho^2).
```

*Step 4 (costs).* The other terms:

- `T_t(c')` vanishes for `t in U` except on `[a, a + k - 2]`, where `z'^t`
  and `x'_{V_t}` differ only on `J_L`, by at most `delta rho`, and
  `x'_{V_t}` deviates from `x*` by at most `eta rho`; so
  `|T_t(c')| <= M_a (w+1)(eta delta + delta^2/2) rho^2` there. For
  `t in [b + 1, b + k - 1]`, `T_t(c) - T_t(c') = a_t(x'_{V_t}) - a_t(x_{V_t}) - ∇a_t(x*)^T (x'_{V_t} - x_{V_t})`,
  which is at most `M_a (w+1) eta delta rho^2` in absolute value. All other
  `T_t` are unchanged.
- `err_t(c') >= 0`, so the error terms contribute at least
  `- sum_{s in U} err_s(c)`.
- `sigma_t(c') = 0` on the edges `(a, b + 1]` (zero drift), and the other
  `sigma_t` are unchanged. So the slope terms contribute at least
  `- gamma M_a W sqrt(w) sum_{t in (a, b+1]} d_t(c)`.

Collect `C2` (boundary terms):
`C2 <= M_a (w+1) rho^2 [k eta^2 + 4(k-1) eta delta + (k-1) delta^2/2]`.
With `K >= 32 k^2/eta` and `theta <= 1/(32 k^2)`, `delta <= eta/(8k)`, so
`C2 <= M_a (w+1)(k+1) eta^2 rho^2 = (c_g/(16k)) rho^2 <= (c_g/(16k)) Sigma_H`.

`C1 = sum_{s in U} (|T_s(c)| + err_s(c))`. By (E2), (E3) and (E4), with
`rho_s <= rhô_s` and Young's inequality
`2(k-1) W rhô_s <= eps1 rhô_s^2 + (k-1)^2 W^2/eps1`,
`eps1 = 1/(144 k^3 (w+1) kappa)`, and `theta <= 1/(12(k-1))`:

```
C1 <= M_a (w+1) [ (eps1 + 3(k-1) theta) S_U + (k-1)^2 (1/eps1 + 12) |U| W^2 ] + (alpha' A/2)(|U| W^2 + theta^2 S_U),
```

where `S_U = sum_{s in U} rhô_s^2 <= k sum_{u in [a-k+1, b]} rho_u^2 <= 3 k^2 Sigma_H`
(by (U1), (U2), each light bag contributes at most `eta^2 rho^2`, and
`|H_U| eta^2 rho^2 <= Sigma_H`, `eta^2 rho^2 <= Sigma_H`).

`C3 = gamma M_a W sqrt(w) sum_{t in (a, b+1]} d_t(c) <= 2 gamma M_a sqrt(w) |U| W^2 + 2 gamma theta M_a sqrt(w) W sum_{u in [a, b+1]} rho_u`
by (E1). With `2 gamma theta M_a sqrt(w) W rho_u <= (c_g/(144 k(k+1))) rho_u^2 + 144 k(k+1) w gamma^2 theta^2 kappa M_a W^2`
and `sum_{u in [a, b+1]} rho_u^2 <= (2k+2) Sigma_H`:
`C3 <= (c_g/(72k)) Sigma_H + [2 gamma sqrt(w) + 288 k(k+1) w gamma^2 theta^2 kappa] M_a |U| W^2`.

*Step 5 (conclusion).* The coefficients of `Sigma_H` in `C1 + C3` are at
most

- `3k^2 M_a (w+1) eps1 = c_g/(48k)`;
- `9 k^2 (k-1)(w+1) M_a theta <= c_g/(72k)` (by
  `theta <= 1/(648 k^4 (w+1) kappa)`);
- `(3/2) k^2 alpha' A theta^2 <= c_g/(72k)` (by
  `theta <= 1/(k^{3/2} sqrt(108 a))`);
- `c_g/(72k)` from `C3`;

in total at most `c_g/(16k)`. The terms in `|U| W^2` add up to
`c_g Q(gamma, theta) |U| W^2`, and by (U2) and `rho > KW`,
`|U| W^2 <= (2k+1) |H_U| W^2 < (2k+1) Sigma_H/(eta^2 K^2)`; since
`K^2 >= 16 k(2k+1) Q/eta^2`, they are at most `(c_g/(16k)) Sigma_H`. Hence

```
Phi(c) - Phi(c') >= (c_g/(4k) - 3 c_g/(16k)) Sigma_H = (c_g/(16k)) Sigma_H > 0. □
```

*Remarks.*

- **Why paths.** The splicing cost `C2` is paid by the gain of the single
  far bag `t0`, because the window has two boundary edges. On a tree a
  window of heavy bags can have a boundary edge for almost every bag in it;
  then `C2` is of order `k w M_a eta^2 rho^2` per boundary edge, while each
  heavy bag only guarantees a gain of order `(c_g/k) eta^2 rho^2`; their
  ratio `k^2 w M_a/c_g` is at least `2kw > 1` (because `c_g <= k M_a/2`), so
  the argument fails (Section 6).
- **Constants.** They are crude. In orders of magnitude,
  `1/theta_1 = O(k^4 w kappa + k^{3/2} sqrt(a))` and
  `K_1(gamma, theta) = O(k^{4.5} w^{1.5} kappa^{1.5} + k^2 sqrt(w kappa a) + k^2 w^{3/4} kappa sqrt(gamma) + k^3 w gamma theta kappa^{1.5})`.
  On the path family of Section 8.1, `K_1(0, 0) ≈ 1.8e6`
  (`logs/constants_gr.log`). The computations show localization within
  `3`–`6` core widths when `theta` is small enough (Section 8).
- **(S) is used** in Step 3 twice (`F(x* + delta) - f* <= (k M_a/2)|delta|^2`
  and `∇F(x*)(x̂ - x') = 0`). At a boundary minimizer the splicing cost has
  a first-order term `∇_J F(x*)(x_J - x*_J)`, which this argument does not
  control.

## 3. Algorithm GR

### 3.1 The algorithm

Input: `F` with a path decomposition (Sections 3.1–3.3 also make sense for
any tree decomposition), per-factor relaxations, `eps > 0`, a starting
point `x^(-1) in X0`, parameters `theta = 2^-mu` and `R > 0`. Incumbent
`UBD = F(x^(-1))`. Start with one leaf per bag and one cell per separator
(the whole boxes).

For stages `j = 0, 1, 2, ...`, with `W_j = s0 2^{-j}`:

1. *Slopes.* `lambdâ = lambda(x^(j-1))` (Lemma 3.2 of [D]).
2. *One dynamic program.* Compute the maximal `beta` of Lemma 1.5 of [D],
   the root bound `l_r` and a minimizing configuration `c_j` (copies
   `z^t_j`, consistent point `x^(j)`).
3. *Incumbent and stop.* `UBD := min(UBD, F(x^(j)))`. If
   `l_r >= UBD - eps`, stop and output the certificate and the incumbent.
4. *Graded refinement around `c_j`.* In every bag `t`, split (into the
   `2^{|V_t|}` dyadic children) every leaf `B` with
   `w(B) > max(W_{j+1}, theta (dist_inf(B, z^t_j) - R W_j)_+)`, and every
   cell `D` of `S_t` with
   `w(D) > max(W_{j+1}, theta (dist_inf(D, z^t_{j,S_t}) - R W_j)_+)`,
   repeatedly, until no box qualifies.

GR uses function values, factor gradients at computed points, and the
convex programs of the dynamic program. It uses no min-marginals, no pruning
test, no monotonicity (M), no knowledge of `x*` or of the constants (other
than `theta` and `R`, removed in Corollary 3), and no local solver. The
partition only gets finer; slopes may change from stage to stage without
restarting, because the validity of a certificate (Lemma 1.3 of [D]) holds
for any slopes.

### 3.2 Analysis

Define, with `theta_1` and `K_1` of Section 2,

```
gamma(K)  = 2 k sqrt(w+1) K,
c_theta   = 18432 k^4 (2k+1)(k+1) w (w+1),        theta_2 = eta/(2 kappa sqrt(c_theta)),
Q_0       = (w+1)(k-1)^2 kappa (144 k^3 (w+1) kappa + 12) + a/2,
K*        = max{ 32 k^2/eta,  sqrt(128 k (2k+1) Q_0/3)/eta,  (512/3) k^2 (2k+1) kappa sqrt(w(w+1))/eta^2 },
theta*    = min{ theta_1, theta_2 },
D*        = 2(k-1)(1 + theta K*),
C_term    = M_a (w+1)(K* D* + 1.5 D*^2) + (alpha' A/4)(1 + theta K*)^2 + 2 gamma(K*) M_a sqrt(w)(1 + theta K*)
            + (k M_a/2)(w+1) K*^2.
```

**Theorem 2 (GR on path decompositions).** Assume the setting of
Section 1.1 with (QG), (L^{1,1}), (U^q) and (S), and run GR with
`theta <= theta*` and `R >= 3 K*`. Then:

(a) at every stage `j` that runs, the leaves and cells satisfy
`w <= max(W_j, theta dist_inf(box, x*))` (property **G(W_j, theta)**), the
slopes have per-edge errors `nu_t <= gamma(K*) M_a W_j`, and every bag copy
of the minimizing configuration has `rho_t <= K* W_j`;

(b) GR stops at a stage `j <= j* = max(0, ceil(log2(s0 sqrt(C_term N/eps))))`;

(c) the output certificate proves tolerance `eps`
(`f* - eps <= UBD - eps <= l_r <= f*`), and `UBD <= f* + eps`;

(d) GR creates at most `2 N j* (4R + 4/theta + 4)^{w+1}` boxes (so the final
certificate has at most `2N (1 + j* (4R + 4/theta + 4)^{w+1})` leaves and
cells), runs the dynamic program at most `j* + 1` times, and processes at
most `(j* + 1)` times the final size in total.

*Proof.* (a) By induction on `j`.

- *Slopes.* At stage 0, `|x^(-1) - x*|_inf <= s0 = W_0`. At stage
  `j >= 1`, the consistent point takes each coordinate from a copy
  (`x_i = z^{l_i}_i`), so by the induction hypothesis
  `|x^(j-1) - x*|_inf <= max_t rho_t <= K* W_{j-1} = 2 K* W_j`. The edge-`t`
  slope involves the gradients of at most `k - 1` bags (those of `sub(t)`
  that contain a variable of `S_t`), so
  `nu_t <= (k-1) M_a sqrt(w+1) |x^(j-1) - x*|_inf <= gamma(K*) M_a W_j`
  (at stage 0, `nu_t <= (k-1) sqrt(w+1) M_a W_0 <= gamma(K*) M_a W_0`).
- *Localization.* The boxes of the minimizing configuration satisfy
  G(W_j, theta), hence (W_theta) with `W = W_j`. `K_1` increases with
  `gamma` and `theta`. With `gamma = gamma(K*)`, the last term of
  `16 k(2k+1) Q(gamma, theta)` equals `c_theta theta^2 kappa^2 K*^2`, which is
  at most `eta^2 K*^2/4` because `theta <= theta_2`; the terms
  `16 k(2k+1) Q_0` and `16 k(2k+1) 2 gamma kappa sqrt(w) = 64 k^2 (2k+1) kappa sqrt(w(w+1)) K*`
  are at most `(3/8) eta^2 K*^2` each by the definition of `K*`. So
  `K_1(gamma(K*), theta) <= K*`, and Lemma 1 gives `rho_t <= K* W_j`.
- *Grading.* After step 4, every box `Y` of bag `t` either was split or
  satisfies `w(Y) <= max(W_{j+1}, theta (dist(Y, z^t_j) - R W_j)_+)`, and
  `dist(Y, z^t_j) - R W_j <= dist(Y, x*) + K* W_j - R W_j <= dist(Y, x*)`.
  New boxes satisfy the same test when the loop ends. So G(W_{j+1}, theta)
  holds at stage `j + 1`. At stage 0 it holds trivially.

(b), (c) At stage `j`, let `c` be the minimizing configuration. By (a), (E1)
and (E2), `rho_t <= K* W_j`, `Delta_t <= D* W_j`, `d_t <= 2(1 + theta K*) W_j`
and `w(B_t) <= (1 + theta K*) W_j`. By (1.1), `F(x) >= f*` and (E3), (E4),
`l_r = Phi(c) >= f* - N W_j^2 [M_a (w+1)(K* D* + 1.5 D*^2) + (alpha' A/4)(1 + theta K*)^2 + 2 gamma(K*) M_a sqrt(w)(1 + theta K*)]`.
By (S), `UBD <= F(x^(j)) <= f* + (k M_a/2)|x^(j) - x*|_2^2 <= f* + (k M_a/2)(w+1) N K*^2 W_j^2`
(`|x^(j) - x*|_inf <= K* W_j` as above, and `n <= (w+1) N`). So `UBD - l_r <= C_term N W_j^2`, and the stop test
succeeds once `C_term N W_j^2 <= eps`, that is, at stage `j*` at the latest.
At the stop, `l_r >= UBD - eps >= f* - eps`, `l_r <= f*` (Lemma 1.3 of [D]),
and `UBD <= l_r + eps <= f* + eps`.

(d) Consider the refinement after stage `j < j*`.

- *No box wider than `W_j` is split.* For `j = 0` all boxes have width
  `W_0`. For `j >= 1`, a box `Y` of width `>= 2 W_j` survived the previous
  refinement, so `w(Y) <= theta (dist(Y, z_{j-1}) - R W_{j-1})`. Both copies
  are within `K* W_{j-1}` and `K* W_j` of `x*`, so
  `|z_j - z_{j-1}|_inf <= 3 K* W_j`, and with `R >= 3 K*`,
  `theta (dist(Y, z_j) - R W_j) >= theta (dist(Y, z_{j-1}) - 3K* W_j - R W_j) >= theta (dist(Y, z_{j-1}) - R W_{j-1}) >= w(Y)`.
  So `Y` is not split. Children of split boxes have width `W_{j+1}` and are
  not split either.
- *Count.* So every split box is a dyadic cube of side `W_j` with
  `theta (dist(Y, z^t_j) - R W_j) < W_j`, i.e. within sup-distance
  `(R + 1/theta) W_j` of the copy. In each coordinate at most
  `2(R + 1/theta) + 2` aligned intervals of length `W_j` meet an interval of
  radius `(R + 1/theta) W_j`. So at most `(2R + 2/theta + 2)^{|V_t|}` leaves
  of bag `t` and `(2R + 2/theta + 2)^{|S_t|}` cells of `S_t` are split, and
  each split creates `2^{|V_t|}` (resp. `2^{|S_t|}`) boxes. Sum over the
  `N` bags, the `N - 1` separators and the `j*` refinements. □

*Comparison with Theorem 3.4 of [D].* The count has the same form,
`|T| C^{w+1} log(|T|/eps)`. The base here is
`4R + 4/theta + 4 = O(K* + 1/theta*)`, a polynomial in `k`, `w`, `kappa`, `a`
of higher degree than the `O(k sqrt(K_1 (1+Delta) w) M_a/c_g + ...)` of
[D]. Orders: `K* = Theta(k^5 w^2 kappa^2 + k^2 sqrt(w kappa a))` (the term
`k^{4.5} w^{1.5} kappa^{1.5}` is dominated because `k kappa >= 2`), and
`1/theta* = O(k^4 w kappa (1 + sqrt(w kappa)) + k^{1.5} sqrt(a))`, which is
`O(k^4 w^{1.5} kappa^{1.5} + k^{1.5} sqrt(a))` when `w kappa >= 1`. (The
first version wrote `k^{4.5}` for `1/theta*`; that bound is valid, because
`k^4 w kappa <= k^{4.5} w kappa^{1.5}` when `kappa >= 2/k`, but looser.)
So the base is quadratic in `kappa = M_a/c_g`, while the base of
Theorem 3.4 of [D] is linear in `M_a/c_g`. The square comes from the slope
lag: GR's slope errors are proportional to the previous localization radius
(`gamma(K*)` is linear in `K*`), and the fixed point `K_1(gamma(K*), theta) <= K*`
forces the term in `1/eta^2` of `K*`. The constants are numerically vacuous
on the path family of Section 8.1 (`k = 2`, `w = 1`, `kappa = 28`, `a = 8`;
`logs/constants_gr.log`, float): `theta* ≈ 8.2e-8 ≈ 2^-23.5`,
`K* ≈ 7.3e8`, `R = 3K* ≈ 2.2e9` and base `≈ 8.8e9`, while the computations
use `theta = 1/8`, `R = 4` (base 52) and observe localization 3. The theorem
is a statement about the form of the count, not about its size at these
parameters. Theorem 2 needs (S) and a path; Theorem 3.4 needs neither, but
needs `x*`.

### 3.3 Unknown constants, and trees

**Corollary 3 (dovetailing).** Let `lambda_eps = max(0, ceil(log2(s0/sqrt(eps))))`
(known to the algorithm). Run, for rounds `r = 1, 2, ...` and
`mu = 1, ..., r`, GR with `theta = 2^-mu` and `R = 2^mu`, each time from the
initial partition, for at most `r + lambda_eps` stages (stage indices
`0, ..., r + lambda_eps - 1`) and at most `2^r` created boxes. The box
budget is enforced during the refinement: before every split the run checks
that its created boxes plus the children of that split stay within `2^r`,
and aborts otherwise. Stop at the first run that stops by its own test, and
output its certificate and incumbent. Under the hypotheses of Theorem 2 this stops
with a certificate proving `eps` and an incumbent within `eps` of `f*`. Let
`mu*` be the least `mu` with `2^-mu <= theta*` and `2^mu >= 3 K*`, `B*` the
bound of Theorem 2(d) at `mu*`, and
`r* = max(mu*, ceil(log2 B*), ceil((1/2) log2(C_term N)) + 1)`. Then the
total number of boxes created is at most
`sum_{r <= r*} r 2^r <= 2 r* 2^{r*}`, which is
`O(N C^{w+1} log(N/eps) log(N C^{w+1} log(N/eps)))`, and the number of
dynamic-program runs is at most `r*^2 (r* + lambda_eps)`.

*Proof.* Any run that stops outputs a valid certificate: `l_r` is a valid
lower bound for any partitions and slopes (Lemma 1.3 of [D]) and `UBD` is a
value of `F`; the stop test gives the two claims. By Theorem 2(b) and
`ceil(x + y) <= ceil(x) + ceil(y)`,
`j* <= lambda_eps + ceil((1/2) log2(C_term N)) <= lambda_eps + r* - 1`
(if the argument of the outer `ceil` in `j*` is not positive, `j* = 0`), so
in round `r*` the run with `mu*` satisfies the hypotheses of Theorem 2,
reaches its stopping stage `j* <= r* + lambda_eps - 1` within its stage
cap, and creates at most `B* <= 2^{r*}` boxes, so it is never aborted. Every
run creates at most `2^r` boxes, because the budget is checked before each
split. This matters: a run with a wrong `mu` may split boxes far wider than
`W_j` and create up to about `N 2^{(j+1)(w+1)}` boxes in a single
refinement, so a check made only after the refinement could overshoot the
budget by far more than `2^r`. Each round has `r` runs. (Without the stage
cap a run with a wrong `mu` still creates at least `N` boxes per stage,
because the leaf containing each copy has width at least `W_j > W_{j+1}`
and is split; so the box budget alone also bounds the number of stages, by
`2^r/N + 1`.) □

**Remark 3.3 (trees; corrected after review).** In the proof of Theorem 2
the path structure is used in Lemma 1 and, through a constant, in the slope
bound. On a rooted tree decomposition:

- (E1)–(E4) hold, with `rhô_t` the maximum of `rho_u` over `t` and its
  ancestors within `k - 1` generations: in (E2) the path from `top(i)` to
  `t` has at most `k - 1` edges, and in (E3) the variables of `V_t \ S_t`
  have `top(i) = t`.
- *The slope bound needs a different constant.* On a path the bags of
  `sub(t)` that contain a variable of `S_t` are `t, ..., t + k - 2`. On a
  tree there can be more than `k - 1` of them. Example (`k = 3`, `w = 2`):
  `V_p = {1, 2}`, `V_t = {1, 2, 3}`, children of `t` with bags `{1, 3, 5}`
  and `{2, 3, 6}`; all three bags of `sub(t)` meet `S_t = {1, 2}`. The
  bound holds coordinatewise: for `i in S_t`, `lambda_{t,i}` sums
  `∂_i a_s` over the at most `k - 1` bags of `sub(t) ∩ T_i` (Lemma 3.2 of
  [D]), so `|lambda_{t,i}(x) - lambda_{t,i}(x*)| <= (k-1) M_a sqrt(w+1) |x - x*|_inf`
  and `nu_t <= (k-1) M_a sqrt(w(w+1)) |x - x*|_inf`. In Theorem 2,
  `gamma(K)` becomes `gamma_T(K) = 2(k-1) sqrt(w(w+1)) K`.
- The grading, the termination (b)–(c) (with (S)) and the count (d) do not
  use the path structure.

The induction of Theorem 2(a) needs a fixed point, not just a localization
constant independent of `|T|`. The property it uses is:

**(Loc_T)** There are `K_T >= 1/2` and `theta_T > 0`, depending only on `k`,
`w`, `kappa`, `a` (and possibly the branching), such that for every
`W > 0`, every certificate with per-edge slope errors
`nu_t <= gamma_T(K_T) M_a W`, and every minimizing configuration whose
leaves and cells satisfy (W_theta) with `theta <= theta_T`, all bags have
`rho_t <= K_T W`.

(`K_T >= 1/2` covers stage 0, where `nu_t <= (k-1) sqrt(w(w+1)) M_a W_0`.)
**For any tree decomposition with (QG), (L^{1,1}), (U^q) and (S), if
(Loc_T) holds, then Theorem 2 and Corollary 3 hold** with `K*`, `theta*`
and `gamma(K*)` replaced by `K_T`, `theta_T` and `gamma_T(K_T)`
(`R >= 3 K_T`, and `C_term` with the same replacements). The proof is that
of Theorem 2 with these replacements.

A localization bound `rho_t <= K_1(gamma, theta) W` with `K_1` independent
of `|T|` does not imply (Loc_T). For example `K_1(gamma, theta) = 1 + gamma`
has no fixed point, because `gamma_T(K) >= 2 sqrt(2) K > K`. A sufficient
growth condition is the form that Lemma 1 has on paths:
`K_1(gamma, theta) <= A_0 + A_1 sqrt(gamma) + A_2 theta gamma` for
`theta <= theta_0`. Then (Loc_T) holds with
`theta_T = min(theta_0, 1/(2 A_2 c_T))` and
`K_T = max(1/2, 4 A_0, 16 A_1^2 c_T)`, where `c_T = 2(k-1) sqrt(w(w+1))`:
the last term is at most `K_T/2`, and the first two at most `K_T/4` each.
So the remaining step of this route for trees is (Loc_T) (Conjecture 7).
It is sufficient for the route; it is not shown to be necessary for the
open problem of [E].

**Remark 3.4 (cost of the convex programs).** As for the shell
certificates of [D] and for LS, the dynamic program solves one convex
program per (leaf, cell) pair. In the computations the pairs are 2.8–4.8
times the leaves, growing slowly with `n` and the number of stages. I have
not bounded this ratio; the "one program per leaf" variant of the review of
[D] (Section 4 of [D]) would remove it at the price of larger drifts in
(E1).

**Remark 3.5 (relation to RC).** Algorithm RC of [E] rebuilt shell
partitions around the current consistent point at every round. GR differs
in three ways: per-bag centres (the copies `z^t_j`), cumulative refinement
(boxes are never merged again), and the margin `R W_j`. Lemma 1 applies to
any partition whose minimizing configuration has graded boxes, so an
induction like Theorem 2's may also cover RC with small enough `theta`. I
have not done this, and I did not investigate why RC with `theta = 1/16`
failed on the random instances of [E] while GR with `theta = 1/16` works on
them (Section 8.2).

## 4. Consequence for LS: Conjecture A.7 on paths

**Corollary 4.** Assume the setting of Section 1.1 with (QG), (L^{1,1}),
(U^q), (S), and (M) for LS. At every sublevel `i` of every pass of LS whose
stop test fails, the minimizing configuration satisfies
`rho_t <= K_LS s_i` for all `t`, and so its consistent point (whose
coordinates are copies) satisfies `|x^cons - x*|_inf <= K_LS s_i`, where
`K_LS` depends only on `k`, `w`, `kappa` and `a`. With exact slopes
(`lambdâ = lambda(x*)`), `K_LS = K_1(0, 0)`.

*Proof.* At a failed sublevel the minimizing configuration has value
`l_r < UBD - eps`, so by Lemma A.2 of [E] all its leaves and cells have
level `i`, i.e. side `s_i`; they satisfy (W_theta) with `W = s_i`,
`theta = 0`. With exact slopes Lemma 1 applies with `gamma = 0`. With LS's
slopes `lambda(x^(p-1))`: in pass `p`, `x^(p-1)` is the consistent point at
the failed sublevel `p - 1` of pass `p - 1`, so by induction over passes
`|x^(p-1) - x*|_inf <= K s_{p-1} = 2 K s_p <= 2 K s_i` for `i <= p`. Then
`nu_t <= 2(k-1) sqrt(w+1) K M_a s_i`, i.e. `gamma <= 2(k-1) sqrt(w+1) K`.
Pass 0 runs only sublevel 0, where `gamma <= (k-1) sqrt(w+1)`. Since
`K_1(gamma, 0)^2` is the maximum of a constant and an affine function of
`gamma`, the inequality `K >= K_1(2(k-1) sqrt(w+1) K, 0)` holds for all
large `K`; take the least such `K >= 1` as `K_LS`. □

This is Conjecture A.7 of [E] for path decompositions, with the additional
hypothesis (S) (the conjecture allowed "possibly an additional hypothesis").
It is consistent with the computations of [E], but it does not explain
their size: on that family the proof constants are `K_1(0, 0) ≈ 1.8e6`
(exact slopes) and `K_LS ≈ 1.4e8` (LS's slopes; `logs/constants_gr.log`),
while `|x^cons - x*|_inf/s_i` was exactly 4, 5, 6, 6, 6 for
`n = 4, ..., 64` with exact slopes in [E]. In
the last pass of LS at `n = 64` here (`logs/ls_scaling_n64_eps1e-4.log`)
the ratio at the failed sublevels is at most 8: 8 at sublevel 4, 6 at
sublevels 5–10 and 3 at sublevels 11–12 (and 3 at the stopping sublevel
13).

*What this says about LS.* Proposition A.6 of [E] showed that the *live*
boxes of LS at level `i` fill a cube of half-side of order `sqrt(n) s_i`
around `x*`. Corollary 4 shows that the *minimizing* configuration stays
within `O(s_i)`. LS refines every live box; GR refines only around the
minimizing configuration and never consults the global threshold
`UBD - eps` except to stop. The difference between the two sets is the
factor `|T|^{(w+1)/2}`.

## 5. Why rule `bd` does not match

The route suggested for this task was to drive refinement by the certified
cell brackets of [Cov] (rule `bd`), with min-marginal pruning and leaf
refinement for the bag errors (Lemma 1' of [Cov]). Two obstacles; the
first is a heuristic argument, the second is proved for a quadratic path
family with one-dimensional separators (Proposition 6):

1. **The brackets need the exact value functions (heuristic, not
   proved).** The sliver of
   Theorem 1 of [Cov] is built from `U_e` and `L_e`. In the certificate
   model the algorithm has only relaxed versions: `beta_{t,D}` (the subtree
   side, minus the subtree's relaxation errors) and `out(D)` of Lemma A.1 of
   [E] (the other side, minus the other bags' relaxation errors). Their
   sum is the min-marginal `MM(D)`, which carries the relaxation error of
   all bags, of order `|T| s^2` at width `s`. I expect this to be the same
   global error that makes LS pay `|T|^{(w+1)/2}` (Section A.5 of [E]); I
   have not proved that a bracket rule built on these surrogates must pay
   it.
2. **Even with exact value functions, the discount `w_e/(2n)` costs
   `sqrt(n)` cells per edge per halving (proved for rule `bd` on a
   quadratic path with one-dimensional separators).** Proposition 6. For
   separators of dimension `w >= 2`, a cost of `sqrt(n)` per separator
   dimension (`n^{w/2}` cells per edge per halving) is a conjecture, not
   proved.

**Proposition 6 (rule `bd` under quadratic growth).** Consider the exact-bag
model of [Cov] on the path with separators `s_1, ..., s_n in [-1, 1]`, root
bag `s_1^2`, bag `t` (`1 <= t <= n-1`) `b s_t s_{t+1} + s_{t+1}^2`, leaf bag
`0`, with `0 < |b| < 1`. So `F = sum_t s_t^2 + b sum_t s_t s_{t+1}`, `x* = 0`,
`f* = 0`, and (QG) holds with `c_g = 1 - |b|`. Let `q_t = w_t(1)` (the
separator margin is `w_t(s) = q_t s^2`). For `n >= 25`, every edge
`t <= (n+1)/2` and every `eps <= q_t/4`, the final partition of rule `bd`
(Corollary 3.2 of [Cov], tolerance `eps/n`) on edge `t` has at least

```
floor((1/2) log2(q_t/eps)) * sqrt((n-5)/2)/12   cells.
```

Hence `bd` uses at least `c n^{3/2} log(1/eps)` cells in total (`c > 0`
depending only on `b`).

*Scope.* The proposition is about rule `bd` exactly as defined in [Cov]:
the graded split `psi` and the discount `w_e/(2n)` of Theorem 1 of [Cov],
exact value functions (so it is a lower bound for an idealized rule), and
separator cells counted. It is proved for the quadratic path above (any
`n >= 25` and `0 < |b| < 1`), whose separators are one-dimensional (each
separator is the single variable `s_t`, and cells are intervals). It does not cover other splits or
discounts (see "An open variant" below), and it does not cover separators
of dimension `w >= 2`; there, a cost of `sqrt(n)` per separator dimension
is a conjecture.

*Proof.* The value functions are quadratic: `U_t(s) = u_t s^2` with
`u_n = 0`, `u_t = -b^2/(4(1 + u_{t+1})) in [-b^2/2, 0]`, and
`V_t(s) = v_t s^2` with `v_1 = 1`, `v_{t+1} = 1 - b^2/(4 v_t)`. So
`w_t = q_t s^2` with `q_t = u_t + v_t >= c_g > 0`. The graded split of
Theorem 1 of [Cov] is `psi_t = U_t - theta_t w_t = p_t s^2` with
`theta_t = (2(n - t) + 1)/(2n)` (edge `t` has `n - t` edges below it) and
`p_t = u_t - theta_t q_t`. Since `u_t <= 0`, `|p_t| >= theta_t q_t`, and for
`t <= (n+1)/2`, `theta_t >= 1/2`.

*Lower bound on the bracket.* Let `D = [d - r, d + r]` and `l` affine. Put
`A = l - psi - w/(2n)` and `B = psi - w/(2n) - l`. If `p_t < 0`, use
`sup_D A >= (A(d - r) + A(d + r))/2` and `sup_D B >= B(d)` (if `p_t > 0`,
the other way round); the affine parts cancel, and

```
g(D) >= |p_t| r^2 - (q_t/(2n)) (2 d^2 + r^2).
```

*Size of final cells.* A final cell has `g(D) <= eps/n`, so
`r^2 (n |p_t| - q_t/2) <= q_t d^2 + eps`, i.e.
`K_t r^2 <= d^2 + eps/q_t` with `K_t = (n|p_t| - q_t/2)/q_t >= (n-1)/2`.

*Counting.* Let `rho = 2^-i` with `rho >= sqrt(eps/q_t)`. A final cell that
meets `[rho, 2 rho]` has `|d| <= 2 rho + r`, so
`K_t r^2 <= (2 rho + r)^2 + rho^2 <= 9 rho^2 + 2 r^2` and
`r <= 3 rho/sqrt(K_t - 2)`. Cells covering an interval of length `rho` then
number at least `sqrt(K_t - 2)/6`. There are `I = floor((1/2) log2(q_t/eps))`
such ranges `[2^-i, 2^{1-i}]`, `i = 1..I`. If `K_t > 11` a cell meets at most
two of them: a cell meeting ranges `i` and `i + 2` contains range `i + 1`, so
`r >= 2^{-i}/4`, while meeting range `i + 2` forces
`r <= 3 * 2^{-i-2}/sqrt(K_t - 2) < 2^{-i}/4`. So the cells number at least
`I sqrt(K_t - 2)/12 >= I sqrt((n - 5)/2)/12`, and `K_t > 11` holds for
`n >= 25`. Summing over the `>= n/2` edges `t <= (n+1)/2`, with
`q_t >= 1 - |b|`, gives the total. □

*The comparison side (computed, not proved).* In this instance every bag is
affine in its parent separator, so the reduced value function of Lemma 0 of
[Cov] is concave, and taking each cell piece as the chord of the reduced
value function (built bottom-up) makes every non-root bag minimum exactly
0. With cells graded at ratio `1/4` around `0` and a core of side `h`,
`(n/4) |u| h^2 <= eps/2`, `check_bd_qg.py` computes the split gap from
closed-form bag minima (in double precision): at most `0.13 eps` for
`n = 4, ..., 256` (`b = 0.8`, `eps = 1e-6`), with 72–96 cells per edge,
against `bd`'s 16.2–152.4 cells per edge (`9.4 sqrt(n)` from `n = 16`). The
proven lower bound is satisfied with a ratio of at least 13 on all edges it
covers. A single cell per edge does not work: the chord sagittas at `x*`
add up along the chain (gap about `0.2 (n-1)` in a first run, by Lemma 0 of
[Cov] at `x = 0`).

*Bag errors (heuristic, not proved).* Lemma 1' of [Cov] asks
`err_{t,B} <= W_t/(3n+1) + eps/(2(n+1))` on every leaf. Under (QG), if
`W_t(z)` grows like `c |z - x*|^2` (an assumption about the margin, not
shown here), a leaf at distance `rho` may have width only of order
`rho sqrt(c/(n alpha' A))`: grading ratio `~ 1/sqrt(n)`, hence
`(C sqrt(n))^{w+1}` leaves per bag per halving, the count of LS
(Theorem A.5 of [E]). This suggests that the sufficient conditions of [Cov]
are of the equal-share type, as [Cov] itself notes for reading (R2); I have
not proved a lower bound for leaves.

*An open variant.* Proposition 1.3 of [Cov] shows that a discount
`c w_e` with `c > 1/(2n)` is impossible for bounds of the form of its
Theorem 1(b) on the chain of copies. Under (QG) its necessary condition
(1.1), `2c sum_e w_e(x_{S_e}) <= m(x)`, allows `c` of order
`c_g/(k M_a)`, independent of `n`. Whether some exact split admits such a
discount under (QG), so that a bracket rule could match Theorem 3.4, is
open.

## 6. Branching trees

**Where the proof breaks.** Lemma 1 repairs the minimizing configuration on
a window of bags around the farthest bag. On a path the window has two
boundary edges, and the splicing cost (`C2`, of order
`k w M_a eta^2 rho^2`) is paid by the gain of the farthest bag alone. On a
tree with branching, a connected window can have up to `(Delta - 1)|U| + 2`
boundary edges. The gain per heavy bag is only of order
`(c_g/k) eta^2 rho^2`, while the cost per boundary edge is of order
`k w M_a eta^2 rho^2 >= 2 w c_g eta^2 rho^2` (because `c_g <= k M_a/2`). So
a window whose bags all sit just above the threshold `eta rho` and have
many boundary edges cannot be paid. Choosing the
threshold, or the window, differently did not help in my attempts: a
"ring" argument over dyadic thresholds fails in the same way, and repairing
whole subtrees loses the background deficits that the minimizing
configuration exploits in every bag.

**Trees with few leaves (sketch, not proved).** Let the decomposition tree
have `L` leaves and branching at most `Delta`. A connected window `U` has at
most `L + 1` boundary edges, because every component of `T \ U` contains a
leaf of `T` or the root. Build the window as in Step 1 of Lemma 1 from the
heavy bags, with buffers of `k` light bags on the far side of every boundary
edge (so the buffers contain at most `Delta^{2k}` bags per heavy bag), and
repair as in Step 2: the boundary edge to the parent of the window's top
bag is treated like edge `a`, and every boundary edge to a child outside the
window like edge `b + 1`. The splicing cost then has `L + 1` terms of the
size of `C2`, and it is paid by the far bag alone if `eta^2` is smaller by
a factor `L + 1`; the light-bag counts gain factors `Delta^{2k}`. If the
bookkeeping goes through, then at a fixed slope-error level `gamma` Lemma 1
holds with `K_1 = O(sqrt(L))` times a constant depending on `k`, `w`,
`Delta`, `kappa`, `a`, `gamma`, and the `theta`-condition becomes
`theta = O(1/sqrt(L))`. GR, however, needs the fixed point (Loc_T) of
Remark 3.3, with slope errors proportional to the localization radius. In
the fixed point the term of `K_1^2` that is linear in `gamma` is divided by
`eta^2`, which is now smaller by the factor `L + 1`; this is the analogue
of the term in `1/eta^2` of `K*`. So the sketch would give `K_T = O(L)`
and `theta_T = O(1/sqrt(L))`, hence `|T| (C L)^{w+1} log(|T|/eps)` boxes.
For a path (`L = 1`) this is Theorem 2; it beats LS
(`|T| (C sqrt|T|)^{w+1} log(|T|/eps)`, Theorem A.5 of [E]) only when
`L = o(sqrt|T|)`. With exact slopes (`gamma = 0`) the base would be
`O(sqrt(L))`, but GR does not have exact slopes. *Correction after review:*
the first version concluded `|T| (C sqrt(L))^{w+1} log(|T|/eps)` for GR and
called it an interpolation between Theorem 2 and LS; that ignored the fixed
point and is withdrawn. I have not written the sketch out.

**A heuristic.** For a quadratic `F` with Hessian `H`, small deviations of
the minimizing configuration respond to the relaxation deficits roughly
like `H^{-1} f` with `|f|_inf` of order `alpha' W`. On a path, `H` is banded
and well conditioned, so `H^{-1}` decays exponentially with graph distance
and `|H^{-1}|_{inf -> inf}` is bounded independently of `n` (Demko–Moss–Smith
type bounds; see Bickel and Lindner, Lemma 2.1,
[[bickel2012-approximating-the-inverse-of-banded]] p.3). On a tree with
branching, exponential decay in graph distance competes with the
exponential growth of balls, and the sum of a row of `H^{-1}` can grow with
the depth when the conditioning is poor relative to the branching. This
suggests that localization on trees may need a condition linking `M_a/c_g`
to the branching, or may hold with a constant growing slowly with the
depth. It is not a proof in either direction: the minimizing configuration
is not a linear response (the deficits are bounded and box-dependent).

**Conjecture 7 (restated after review).** For tree decompositions with
bounded branching `Delta`, property (Loc_T) of Remark 3.3 holds with `K_T`
and `theta_T` depending only on `k`, `w`, `Delta`, `M_a/c_g` and
`alpha' A/c_g`, possibly under a condition on `Delta` relative to
`M_a/c_g`. A sufficient form: the conclusion of Lemma 1 holds on such trees
with `K_1(gamma, theta) <= A_0 + A_1 sqrt(gamma) + A_2 theta gamma` for
`theta <= theta_0`, where `A_0`, `A_1`, `A_2`, `theta_0` depend only on the
same quantities. (The first version asked only for a `K_1(gamma, theta)`
independent of `|T|`, which does not give the fixed point that Theorem 2
needs.)

**Status update (2026-10-02).** The claim without the optional extra
branching/conditioning restriction is disproved by the finite-certificate
counterexample linked at the start of this note. The conditional theorem of
Remark 3.3 is unaffected. The text below records the earlier numerical
evidence; those experiments did not decide the conjecture.

By Remark 3.3, Conjecture 7 would give Theorem 2 for such trees. The
computations of Section 8.4 measure localization along GR's own runs, which
is the quantity (Loc_T) bounds. On the binary-tree family they show ratio
exactly 4 with `c = 0` and `b = 0.55` (`m <= 127`), a slow growth with the
size under random linear terms, and, at `theta = 1/8` with the conditioning
held fixed, a jump from 5 (`m = 7, 15`) to 10–18 (`m = 31, 63`) that stays
bounded in the stages run. In all tree families tested the conditioning
also changes with the size, unless held fixed, and the decomposition has
`k = 3`; the data do not separate the effects of size, conditioning, `k`
and branching, and they neither support nor refute Conjecture 7.

## 7. Reading (R1) of the covering upper half

Conjecture B.5 of [E] asks, in reading (R1), for
`N_dec(eps) <= C^{w+1} poly(|T|) log(1/eps) sup_eta Phi_2(eps, eta)` with
the degree of the polynomial independent of `w`.

- *Under (QG)* this was known for certificates ([E], Section B.1:
  `Phi_2 >= |T| 2^{-(w+1)}` and Theorem 3.4 of [D]). Theorem 2 makes it
  algorithmic for path decompositions with (S): GR finds a certificate with
  `|T| C^{w+1} log(|T|/eps) <= (2C)^{w+1} log(|T|/eps) sup_eta Phi_2` boxes,
  without knowing `x*`.
- *Without (QG)* nothing here applies. GR localizes a minimizer; on
  degenerate near-optimal sets (the staircase family of Theorem B.2 of [E],
  flat blocks) there is no point to localize, and the pointwise allocation
  of Theorem B.3 of [E] must be realized by leaves, which is open step (1)
  of Section 6 of [Cov]. I made no progress on that.

## 8. Numerical checks

All computations are in double precision with `OMP_NUM_THREADS=1`. The
dynamic program, the relaxation and the convex subproblems (nested
bisection, 60 steps) are those of `../adaptive/ls_lib.py` ([E]); GR adds the
minimizing-configuration copies and the graded refinement
(`adaptive2/gr_lib.py`). Leaves and cells are dyadic, so box edges are
exact in binary floating point and the intersection tests need no
widening. The numbers illustrate the statements; they are not certified
counts. "Created" counts boxes produced by splits, "processed" the
partition sizes summed over all dynamic-program runs, "size" the final
leaves plus cells. `zloc = max_t |z^t - x*_{V_t}|_inf/W_j` for the
minimizing configuration of stage `j`.

### 8.1 The path family, `c = 0` (`x* = 0`)

Family of Theorem 4.1 of [D]: `b = 0.8`, `kappa = 0.1`, alphaBB with
`alpha = 0.4` on the bilinear factors, `X0 = [-1,1]^n`, bags `{t, t+1}`
(`k = 2`, `w = 1`). GR starts at `x^(-1) = 0.5 (1, ..., 1)`, so it learns
slopes and incumbent, as LS with restarts does in [E].

`eps = 1e-4`, `R = 4` (`logs/gr_zero_eps1e-4_theta8.log`,
`logs/gr_zero_eps1e-4.log`):

| n | GR `theta = 1/8`: stop stage, size (per bag) | created | processed | GR `theta = 1/16`: size (per bag) | LS of [E]: size (per bag) | LS processed | shells of [D] at `x*` |
|---|---|---|---|---|---|---|---|
| 4 | 11, 36,337 (12,112) | 48,676 | 138,768 | 87,348 (29,116) | 2,841 (947) | 61,701 | 64,976 |
| 8 | 12, 95,938 (13,705) | 128,696 | 414,820 | 236,311 (33,759) | 21,473 (3,068) | 505,380 | 173,608 |
| 16 | 12, 204,010 (13,601) | 273,832 | 883,120 | 504,131 (33,609) | 136,187 (9,079) | 2,299,137 | 372,312 |
| 32 | 13, 475,657 (15,344) | 638,588 | 2,295,377 | 1,191,898 (38,448) | 459,928 (14,836) | 10,190,068 | 865,912 |
| 64 | 13, 965,017 (15,318) | 1,295,740 | 4,657,937 | 2,419,834 (38,410) | 2,195,591 (34,851) | 36,423,324 | 1,760,056 |
| 128 | 14, 2,170,456 (17,090) | 2,914,352 | 11,553,513 | – | – | – | – |
| 256 | 14, 4,356,184 (17,083) | 5,849,392 | 23,189,481 | – | – | – | – |

The LS column for `n <= 32` is from `../adaptive/logs/scaling_eps1e-4.log`;
`n = 64` was run here (`logs/ls_scaling_n64_eps1e-4.log`, 274 s; LS
splits up to `32.9 n` leaves per bag per level). The shell column is from
Section 5.4 of [D] (`theta = 1/16`).

`eps = 1e-6`, `R = 4` (`logs/gr_zero_eps1e-6_theta8.log`,
`logs/gr_zero_eps1e-6.log`), against the exact-slope LS runs of [E], which
start at `x*` and so also have the exact incumbent
(`../adaptive/logs/oracle_eps1e-6.log`), and the shells of [D]:

| n | GR `theta = 1/8`: stop stage, size (per bag) | GR `theta = 1/16`: size (per bag) | LS, exact slopes: size (per bag) | shells of [D] |
|---|---|---|---|---|
| 4 | 14, 53,032 (17,677) | 132,507 (44,169) | 2,914 (971) | 92,816 |
| 8 | 15, 134,035 (19,148) | 340,216 (48,602) | 29,228 (4,175) | 238,696 |
| 16 | 16, 311,878 (20,792) | 799,327 (53,288) | 153,584 (10,239) | 511,896 |
| 32 | 16, 642,166 (20,715) | 1,648,279 (53,170) | 632,586 (20,406) | 1,154,488 |
| 64 | 17, 1,415,317 (22,465) | – | 2,397,460 (38,055) | 2,346,616 |
| 128 | 17, 2,850,613 (22,446) | – | – | – |

Observations.

- **Per-bag size is flat in `n`.** It changes only with the index of the
  stopping stage (one fewer than the number of dynamic-program runs), which
  grows by about one per factor 4 in `n` (the stop needs
  `C_term N W_j^2 <= eps`). Per stage at most 639 leaves per bag are split
  at `theta = 1/8` and 1,711 at `theta = 1/16`, in every run; the bound of
  Theorem 2(d), `(2R + 2/theta + 2)^2`, is 676 and 1,764. LS's per-bag size
  grows linearly in `n`, as Proposition A.6 of [E] predicts. GR with
  `theta = 1/8` is about as large as LS with exact slopes at `n = 32`
  (`eps = 1e-6`: 642,166 against 632,586) and smaller from `n = 64`; at
  `n = 64`, `eps = 1e-4`, it processes 7.8 times fewer boxes than LS with
  learned slopes.
- **Localization.** `zloc = 3.000` at every stage from `j = 3` on, for all
  `n` and both tolerances; the consistent point is at `3 W_j` too. The
  graded invariant G(W_j, theta) with respect to the true `x*` holds in
  every run (0 violations).
- **The gap.** `f* - l_r` is about `17 (n-1) W_j^2` at the late stages
  (`13.7` at `n = 4`, `17.1` at `n = 256`). This is 70 times the
  `0.24 (n-1) h^2` of the shells of [D] centred at `x*` with exact slopes:
  the slope error is about `11.3 W_j` per edge, because the slopes come from
  the previous consistent point, which lags at `3 W_{j-1}`. It costs about
  three extra stages.
- **Pairs.** (Leaf, cell) pairs per leaf: 2.8–4.8, rising slowly with `n`
  and the number of stages (Remark 3.4).
- **Wide splits.** With `R = 4 < 3 * 3`, boxes wider than `W_j` are split
  (`wide` in the logs: 315–21,672 per run, at most 0.71% of the number of
  created boxes).
  With `R = 12` (`n = 16`, `theta = 1/16`, `logs/gr_R_checks.log`) none is,
  as the proof of Theorem 2(d) predicts, and at most 3,192 leaves per bag
  per stage are split (bound 3,364); the final size grows to 915,776.

### 8.2 Random linear terms

`c ~ U(-0.2, 0.2)^n`, seeds 0 and 1, `x^(-1) = 0`, `eps = 1e-4`,
`theta = 1/16` (`logs/gr_random_eps1e-4.log` with `R = 4`,
`logs/gr_R_checks.log` with `R = 8`). `x*` and `f*` are computed as in [E]
(grid dynamic program, then L-BFGS-B); they are used only for the
diagnostics, not by GR.

| n | seed | GR `R = 4`: size (per bag) | max zloc | G violations | GR `R = 8`: size | G violations | LS of [E] | oracle pass of [E] |
|---|---|---|---|---|---|---|---|---|
| 8 | 0 | 239,101 (34,157) | 4.06 | 33 | 323,911 | 0 | 22,559 | 19,590 |
| 8 | 1 | 243,702 (34,815) | 5.01 | 99 | 326,792 | 0 | 25,225 | 22,075 |
| 16 | 0 | 507,092 (33,806) | 4.01 | 0 | 689,344 | 0 | 147,538 | 114,215 |
| 16 | 1 | 523,701 (34,913) | 5.73 | 264 | 700,196 | 0 | 165,598 | 111,980 |
| 32 | 0 | 1,201,682 (38,764) | 4.01 | 0 | 1,640,392 | 0 | – | – |
| 32 | 1 | 1,228,915 (39,642) | 5.41 | 264 | 1,657,611 | 0 | – | – |

Localization stays within 3.1–5.7 `W_j` from stage 3 on, independently of
`n`. With
`R = 4` the margin is smaller than the localization radius for seed 1, the
graded invariant fails for up to 264 boxes, and GR still stops at the same
stage; with `R = 8 >= zloc` the invariant holds everywhere. The RC
runs of [E] on the same instances (`theta = 1/16`) did not converge.

### 8.3 The condition on `theta`

`n = 32`, `c = 0`, `eps = 1e-4`, `R = 4`, capped at stage 12
(`logs/gr_theta_n32.log`; without the cap the `theta = 1/8` run stops at
stage 13):

- `theta = 1/4`: up to stage 6 the run is identical to the others
  (`zloc = 3`); at stage 7 the minimizing configuration jumps away from
  `x*` (`zloc` 64, then 128, 176, 320, 320, 704 at stages 8–12), the graded
  invariant fails for about 2,200 boxes, the slope error grows to
  `827 W_j`, and the gap stays between 0.42 and 3.7 (0.434 at stage 12,
  against `1.24e-4` for the smaller `theta`). The run does not converge
  within the cap.
- `theta = 1/8, 1/16, 1/32`: `zloc = 3` at every stage, identical gaps
  (`1.24e-4` at stage 12), and 639, 1,711 and 5,391 leaves split per bag
  per stage.

So some upper bound on `theta`, as in Theorem 2, is needed (at stage 7 of
the `theta = 1/4` run the graded invariant still holds with respect to `x*`,
yet the ratio is 64), although the observed threshold is far above the
proof's `theta*`. The shell
certificates of [D] at `theta = 1/8` fail for `n > 16` (Remark 3.6 of [D]),
while GR at `theta = 1/8` works up to `n = 256`. A plausible reason, not
checked: a dyadic box of GR with `w <= theta (dist - R W)` has ratio
between `theta/2` and `theta`, while the shell boxes at the inner edge of
each level have ratio exactly `theta`.

**A worse-conditioned path.** `logs/gr_path_b088_eps1e-3.log`
repeats GR on the path family with `b = 0.88`, `c = 0`, `eps = 1e-3`,
`R = 4`. With `theta = 1/8`, localization fails already at `n = 8`:
`zloc = 3` up to stage 6, then 64, 128, 112, 240, ... up to 704, the slope
error rises to `2,026 W_j`, and the run stops only at stage 16 with 370,015
boxes (52,859 per bag). At `n = 16` it fails from stage 6 (`zloc` up to
1,280 by stage 14); I stopped that run by hand after stage 15. With
`theta = 1/16` it works at `n = 8` (`zloc = 3`, stops at stage 10, 167,041
boxes) but loses localization at `n = 16` from stage 8 (`zloc` 128–368;
stopped by hand after stage 12). With `theta = 1/32` the ratio is 3 at
every stage for `n = 8`, 16 and 32 (446,710, 1,192,021 and 2,461,117 boxes,
stopping at stages 10, 11 and 11), but at `n = 64` it jumps from stage 6 on
(`zloc` 32, 64, 20, 44, 512 at stages 6–10; the run, at 5.1M leaves, was
stopped by hand after stage 10).

*Conditioning changes with `n` (corrected after review).* The first version
called this path "`c_g = 0.02`, five times smaller" and explained the
dependence on `n` by the chain-length effect of Remark 3.6 of [D] alone. `0.02 = 0.9 - 0.88` is the lower bound
`0.9 - |b| rho(A)/2` for an infinitely long path. At the tested sizes
(`logs/cg_by_size.log`; lower bound from the spectral radius, upper bound
from feasible points, float):

| path | `n = 8` | `n = 16` | `n = 32` | `n = 64` | `n = 256` |
|---|---|---|---|---|---|
| `b = 0.88`: `c_g` in | [0.073, 0.090] | [0.035, 0.047] | [0.024, 0.031] | [0.021, 0.025] | – |
| `b = 0.8`: `c_g` in | [0.148, 0.164] | – | – | [0.101, 0.105] | [0.100, 0.119] |

So `c_g` falls by a factor of about 3.5 from `n = 8` to `n = 64` at
`b = 0.88`, and the
`b = 0.88` runs mix chain length and conditioning. To separate them I held
the lower bound `0.9 - |b| rho(A)/2` fixed by adjusting `b` with `n`
(`run_fixed_cg.py`, `c = 0`, `eps = 1e-3`, `R = 4`, `theta = 1/16`;
`logs/fixedcg_path_c073_theta16.log`, `logs/fixedcg_path_c035_theta16.log`):

| lower bound held fixed | `n` (`b`) | `c_g` in | `zloc` from stage 3 | stop stage, size |
|---|---|---|---|---|
| 0.073 | 8 (0.88, the run above) | [0.073, 0.090] | 3 | 10, 167,041 |
| 0.073 | 16 (0.8413) | [0.073, 0.085] | 3 | 11, 430,332 |
| 0.073 | 32 (0.8307) | [0.073, 0.080] | 3 | 11, 887,644 |
| 0.073 | 64 (0.8279) | [0.073, 0.077] | 3 | 12, 2,111,051 |
| 0.035 | 8 (0.9205) | [0.035, 0.052] | 3 | 10, 167,041 |
| 0.035 | 16 (0.88, the run above) | [0.035, 0.047] | 128–368 from stage 8 | stopped by hand |

(The two `n = 8` runs have the same partitions because the copies of the
minimizing configuration sit at the same dyadic points; their bounds
differ.) At lower bound 0.073, `theta = 1/16` keeps ratio 3 for
`n = 8, ..., 64`, consistent with a threshold independent of `n` at fixed
conditioning. At lower bound 0.035 it works for `n = 8` and fails for
`n = 16`. So in the tested range both conditioning and chain length
matter: at the worse conditioning a `theta` above the threshold can look
fine on a short chain, as in Remark 3.6 of [D]. Theorem 2 guarantees an
`n`-independent threshold only below its `theta*` (Section 3.2), far
smaller than anything run; the computations do not establish the
practical threshold at `b = 0.88`. That the admissible `theta` is smaller
for worse conditioning agrees with the form of the condition in Theorem 2
(`theta*` is a power of `c_g/M_a`).

### 8.4 Binary trees (branching decompositions)

`adaptive2/tree_gr.py`. Graph: complete binary tree on `m` vertices,
`F = sum_v (x_v^2 - 0.1 x_v^4 + c_v x_v) + b sum_{v >= 1} x_{p(v)} x_v` on
`[-1,1]^m`. Decomposition: one bag `{p(v), v}` per non-root vertex; the bag
of `v` is a child of the bag of `p(v)` (the second child of the root vertex
hangs below the first), so separators are one variable, `w = 1`, `k = 3`,
and bags have up to 2 children (the root bag 3). Same relaxation as for the
path family. For `c = 0`, (QG) holds at `x* = 0` with
`c_g >= 0.9 - |b| rho(A)/2`, where `rho(A) < 2 sqrt(2)` is the spectral
radius of the tree's adjacency matrix. The size-independent bounds
`0.9 - sqrt(2)|b|` (0.122 for `b = 0.55`, 0.023 for `b = 0.62`) quoted in
the first version are far below the values at the tested sizes
(`logs/cg_by_size.log`, float):

| tree | `m = 7` | `m = 15` | `m = 31` | `m = 63` | `m = 127` |
|---|---|---|---|---|---|
| `b = 0.55`: `c_g` in | [0.350, 0.368] | [0.271, 0.301] | [0.226, 0.258] | [0.199, 0.236] | [0.181, 0.220] |
| `b = 0.62`: `c_g` in | [0.280, 0.298] | [0.191, 0.221] | [0.141, 0.173] | [0.110, 0.147] | – |

As on the `b = 0.88` path, `c_g` falls with the size, here by a factor of
about 1.6–1.8 (`b = 0.55`) and 2–2.5 (`b = 0.62`) from `m = 7` to
`m = 63`.

`check_tree_dp.py` (`logs/check_tree_dp.log`, rerun after review) compares
the convex-subproblem solver with an `801 x 801` grid on 200 random
sub-boxes (bisection value never above the grid minimum) and checks, for
`m = 7, 15` (random `c`, `b = 0.55`) over nine stages: (2) `l_r <= f*`, and
the unrelaxed value of the minimizing configuration is at least `l_r` (a
weak test: it holds for any configuration whose relaxed value is at least
`l_r`); and (3), added after review, the relaxed value of the
reconstructed minimizing configuration, recomputed from its leaves, copies
and slopes, equals `l_r` to within `8.9e-16`, and the configuration
constraints hold (each copy in its leaf, each separator copy in its cell,
each cell meeting the parent leaf; 0 violations). The first version
described check (2) as confirming that the configuration value is
consistent, which overstated it.

`b = 0.55`, `R = 4` (`c = 0`) or `R = 8` (random `c`, seed 0),
`theta = 1/16`, `eps = 1e-4` (`logs/tree_zero_eps1e-4.log`,
`logs/tree_random_eps1e-4.log`):

| m (bags) | `c = 0`, `R = 4`: stop stage, size (per bag) | split per bag per stage (max) | `zloc`, stages `>= 3` | random `c`, `R = 8`: stop stage, size (per bag) | split (max) | `zloc`, stages `>= 3` |
|---|---|---|---|---|---|---|
| 7 (6) | 10, 145,840 (24,307) | 1,751 | 3.0 | 10, 194,688 (32,448) | 2,393 | 2.6–3.4 |
| 15 (14) | 11, 422,780 (30,199) | 1,788 | 4.0 | 11, 557,807 (39,843) | 2,434 | 3.4–4.0 |
| 31 (30) | 12, 1,076,091 (35,870) | 1,788 | 4.0 | 12, 1,421,235 (47,374) | 2,434 | 4.0–4.5 |
| 63 (62) | 12, 2,228,411 (35,942) | 1,788 | 4.0 | 12, 2,933,846 (47,320) | 2,434 | 4.0–4.9 |
| 127 (126) | stopped after stage 10 (3,146,970 leaves; gap `2.0e-3`) | 1,788 | 4.0 | stopped after stage 9 (3,207,474 leaves; gap `6.7e-3`) | 2,475 | 4.1–5.3 |

With `c = 0` the localization ratio is exactly 4 at every stage from 3 on for
`m >= 15` (3 for `m = 7`), and the split count per bag per stage is
constant; size per bag grows only with the index of the stopping stage, as
on paths.
(With `R = 4 < 3 * 4` some wider boxes are split, which is why 1,788 slightly
exceeds the path bound 1,764.) With random linear terms
(`c ~ U(-0.2, 0.2)^m`, seed 0; `x*` from a 2001-point grid dynamic program
on the tree followed by L-BFGS-B, interior, `|∇F(x*)|_inf <= 5e-9`; its
global optimality is not certified) the largest ratio rises slowly with
`m`: 3.4, 4.0, 4.5, 4.9 for `m = 7, 15, 31, 63`, and 5.3 over the first ten
stages at `m = 127`. The local constant at `x*` falls at the same time:
half the smallest Hessian eigenvalue at the computed `x*` (an upper bound on
`c_g`) is 0.44, 0.36, 0.32, 0.29, 0.27 for `m = 7, ..., 127`
(`logs/cg_by_size.log`). So this growth cannot be attributed to branching;
the first version contrasted it with the paths, which suggested a
branching effect, and that reading is withdrawn. On the random-`c` paths of
Section 8.2 the local constant also falls (0.22–0.24 at `n = 8`, 0.16–0.19
at `n = 32`) and the ratio did not grow. These data cannot tell a bounded constant from a slow (for example
logarithmic) growth, nor separate size from conditioning.

`b = 0.62`, `c = 0`, `eps = 1e-3`, `R = 4`
(`logs/tree_zero_b062_eps1e-3.log`, `logs/tree_zero_b062_eps1e-3_theta16.log`):

| m | `theta = 1/8`: stop stage, size (per bag) | `zloc` at stages 3, 4, 5, ... | `theta = 1/16`: stop stage, size (per bag) | `zloc` at stages 3, 4, 5, ... |
|---|---|---|---|---|
| 7 | 9, 52,807 (8,801) | 4 throughout | 9, 117,330 (19,555) | 4 throughout |
| 15 | 10, 154,216 (11,015) | 4 throughout | 10, 351,652 (25,118) | 4 throughout |
| 31 | 11, 474,845 (15,828) | 4, 6, 16, 10, 12, 14, 10, 12, 14 | 10, 761,689 (25,390) | 4, 6, 5, 5, 5, 5, 5, 5 |
| 63 | 12, 1,197,823 (19,320) | 4, 8, 16, 12, 16, 12, 16, 12, 16, 12 | 11, 1,988,528 (32,073) | 4, 8, 6, 6, 6, 6, 6, 6, 6 |

At `theta = 1/8` the ratio jumps to 10–16 from `m = 31` on and then stays
bounded (it oscillates between 12 and 16 at `m = 63`); the runs still stop,
with a gap constant of about 26–29 instead of 3–5. At `theta = 1/16` it stays
within 4–6 up to `m = 31` and 4–8 at `m = 63` (6 from stage 5 on), and the
runs stop with gap constants 3–7.

*Comparison with paths (corrected after review).* The first version
compared these trees with the `b = 0.88` path as "similar conditioning"
(0.023 against 0.02) and concluded that the tree behaviour at
`theta = 1/8` reflects a too-large `theta` rather than an effect of
branching. Both numbers were infinite-size bounds. At the tested sizes the
`b = 0.62` trees that lose localization have `c_g >= 0.141` (`m = 31`) and
`>= 0.110` (`m = 63`), while the `b = 0.88` paths have `c_g <= 0.047` for
`n >= 16`; the comparison and its conclusion are withdrawn.

To separate size from conditioning I reran the tree at `theta = 1/8` with
`0.9 - |b| rho(A)/2` held at 0.141, its value for `b = 0.62`, `m = 31`
(`run_fixed_cg.py`, `c = 0`, `eps = 1e-3`, `R = 4`;
`logs/fixedcg_tree_c141_theta8.log`, `logs/fixedcg_tree_c141_theta8_m63.log`):

| m (`b`) | `c_g` in | `zloc` at stages 3, 4, 5, ... | stop stage, size (per bag) | gap constant, last stages |
|---|---|---|---|---|
| 7 (0.7593) | [0.141, 0.159] | 4, then 5 throughout | 9, 54,647 (9,108) | 6.1 |
| 15 (0.6637) | [0.141, 0.171] | 4, then 5 throughout | 10, 158,516 (11,323) | 5.9 |
| 31 (0.62, the run above) | [0.141, 0.173] | 4, 6, 16, 10, 12, 14, 10, 12, 14 | 11, 474,845 (15,828) | 26–29 |
| 63 (0.5960) | [0.141, 0.178] | 4, 6, 16, 10, 12, 14, 12, 10, 18, 10 | 12, 1,148,609 (18,526) | 20–27 |

At fixed conditioning the tree ratio at `theta = 1/8` is 5 up to `m = 15`
and jumps to 10–18 from `m = 31` on; the runs still stop. So on the tree,
too, the admissible `theta` depends on the size at fixed conditioning (in
this range). For comparison, the path family with `b = 0.8`, whose `c_g`
lies between 0.100 and 0.119 at `n = 256` (worse than these trees), keeps
ratio 3 at `theta = 1/8` up to `n = 256` (Section 8.1). So at these sizes
the tree family needs a smaller `theta` than the path family at comparable
conditioning. This does not isolate branching: the tree decomposition has
`k = 3` (paths `k = 2`), the proof's `theta*` falls like `k^{-4}`, and no
`k = 3` path decomposition was run. A tree run at `theta = 1/32` was not
done (too costly here).

### 8.5 Rule `bd` under quadratic growth (`check_bd_qg.py`, `logs/check_bd_qg.log`)

Quadratic path of Proposition 6, `b = 0.8`, `eps = 1e-6`. Brackets are
computed to floating-point accuracy (closed-form maxima of quadratics on
intervals, 200 golden-section steps on the convex function of the slope);
the comparison split's gap uses closed-form bag minima. All in double
precision, not exact arithmetic.

| n | `bd` cells | per edge | per edge `/sqrt(n)` | min over covered edges of cells/bound (smallest bound) | graded cells per edge | gap/eps of the graded split |
|---|---|---|---|---|---|---|
| 4 | 65 | 16.2 | 8.12 | – (`K_t <= 11`) | 72 | 0.033 |
| 8 | 191 | 23.9 | 8.44 | – | 72 | 0.099 |
| 16 | 595 | 37.2 | 9.30 | 14.2 (2.5) | 80 | 0.059 |
| 32 | 1,697 | 53.0 | 9.37 | 14.3 (3.7) | 80 | 0.127 |
| 64 | 4,825 | 75.4 | 9.42 | 13.3 (5.4) | 88 | 0.066 |
| 128 | 13,655 | 106.7 | 9.43 | 13.3 (7.7) | 88 | 0.133 |
| 256 | 39,017 | 152.4 | 9.53 | 13.6 (10.9) | 96 | 0.067 |

`bd` grows like `9.4 sqrt(n)` cells per edge; the graded split like
`log(n/eps)`. Every non-root bag minimum of the graded split is 0 to
`3e-17`.

## 9. Literature and novelty

Examined:

- the notes [D], [E], [Cov] and their reviews, which already discuss
  Berenguel et al. (2013), Zhang–Sun (2022), the min-marginal computation on
  junction trees, and Ruozzi–Tatikonda;
- the local literature folder: Bickel and Lindner, "Approximating the
  inverse of banded matrices by banded matrices with applications to
  probability and statistics", Theory Probab. Appl. 56 (2012)
  ([[bickel2012-approximating-the-inverse-of-banded]] p.3, Lemma 2.1: a
  self-adjoint positive definite `k`-banded operator with spectrum in
  `[m, M]` has an inverse approximable by bandwidth `nk`; the error bound
  `m^{-1}((kappa-1)/(kappa+1))^{n+1}` is as recorded in the local read note,
  because the extracted text drops the display), and the summary of Benzi, Boito and
  Razouk, SIAM Review 2013 (only the existing read note of
  [[benzi2013-decay-properties-of-spectral-projectors]], which records
  size-independent decay under bounded degree and bounded condition number;
  I did not reread the paper); both are used only for the heuristic of
  Section 6;
- web searches (short):
  - P. Rebeschini and S. Tatikonda, "Locality in network optimization",
    arXiv:1509.06246 (abstract page only, through a summarizing web fetch): sensitivity of optimal points to
    local perturbations decays with graph distance for min-cost network
    flow, and localized reoptimization exploits it. Lemma 1 is a statement
    of the same kind (a far deviation of the minimizing configuration is
    not optimal), for relaxed dynamic programs on path decompositions and
    in sup norm, proved by a local exchange instead of a sensitivity
    analysis;
  - M. Sanchez, D. Allouche, S. de Givry and T. Schiex, "Russian doll
    search with tree decomposition", IJCAI 2009 (pages 1–2 read): in
    decomposition-based branch and bound for graphical models "the locality
    of bounds induced by decomposition often hampers the practical effects
    ... because subproblems are often uselessly solved to optimality"; they
    pass global bounds into subproblems. This is the discrete counterpart of
    the trade-off between LS (global thresholds) and GR (no thresholds,
    localization);
  - adaptive finite element methods with optimal complexity (Binev,
    Dahmen and DeVore, Numer. Math. 2004; Stevenson, Found. Comput. Math.
    2007; Cascón, Kreuzer, Nochetto and Siebert, SIAM J. Numer. Anal.
    2008), checked at the bibliographic level through search-result
    snippets only (no paper opened). GR builds graded partitions around an
    estimated singular point, as adaptive meshes do around singularities;
    its analysis is much simpler because the "singularity" is a single
    point that the algorithm localizes, and no marking strategy is needed.
- added after review (the review named these sources; I checked the
  bibliographic data and abstracts myself, through web searches and
  summarizing fetches; no paper was read in full):
  - S. Shin, M. Anitescu and V. M. Zavala, "Exponential decay of
    sensitivity in graph-structured nonlinear programs", SIAM J. Optim.
    32(2) (2022) 1156–1183, doi:10.1137/21M1391079, arXiv:2101.03067
    (abstract page; pages and DOI checked against Crossref in round 2, the
    first revision gave wrong pages). Under the
    strong second-order sufficient condition and LICQ, the sensitivity of
    the primal-dual solution at one node to a data perturbation at another
    node decays exponentially with their graph distance. It is also
    recorded in the continuation's audit
    (`../literature/decomposition-bb-prior.md`). It is the closest
    locality result I know to Lemma 1, but it is local (near a regular
    solution) and about exact NLP solutions, while Lemma 1 is a global
    exchange statement about minimizers of relaxed decomposition dynamic
    programs. (The review cites arXiv:2101.06350; that is the related
    Shin–Zavala paper "Controllability and observability imply exponential
    decay of sensitivity in dynamic optimization".)
  - M. Heidari, V. T. Chow, P. V. Kokotović and D. D. Meredith, "Discrete
    differential dynamic programming approach to water resources systems
    optimization", Water Resour. Res. 7(2) (1971) 273–282 (abstract, from a
    bibliographic record): start from a trial trajectory, apply Bellman's
    recursion in a neighbourhood ("corridor") of it, and iterate with the
    improved trajectory.
  - R. Luus, *Iterative Dynamic Programming*, Chapman & Hall/CRC, 2000
    (search-result snippets only): dynamic programming on grids around the
    best control policy of the previous pass, with the region reduced by a
    factor at each pass.
  - R. Munos and A. Moore, "Variable resolution discretization in optimal
    control", Machine Learning 49 (2002) 291–323 (abstract): cells of a
    dynamic-programming discretization are split top-down by local and
    non-local criteria (influence, variance).

Assessment. The mechanism of GR (one dynamic program per stage, refining
shrinking neighbourhoods of the current dynamic-programming-optimal
trajectory) has clear precursors in discrete differential dynamic
programming and iterative dynamic programming, and adaptive splitting of
dynamic-programming cells appears in Munos–Moore. From the abstracts and
snippets I read, these methods give neither certified lower bounds nor
complexity bounds (I did not check this in the full papers). What I did not
find: sup-norm localization of minimizing configurations of relaxed
decomposition dynamic programs (Lemma 1), a certificate-producing algorithm
with the instance-dependent count `|T| C^{w+1} log(|T|/eps)` (Theorem 2), or
a lower bound like Proposition 6 for bracket-driven refinement. Lemma 1 is
an exchange argument of a familiar type; Theorem 2 is a consequence within
the program's model. The searches were short and at the level of abstracts
and snippets; this does not establish novelty.

## 10. Limitations and open problems

- **Trees with branching** (Conjecture 7). The proof of Lemma 1 needs a
  window with boundedly many boundary edges. Remark 3.3 reduces the tree
  case to the localization property (Loc_T), which includes a fixed point
  in the slope error; a localization constant independent of `|T|` alone is
  not enough.
- **(S).** Boundary minimizers are not covered (Section 2, remarks).
  Theorem 3.4 of [D] covers them with `x*` known. Exploratory runs
  (`logs/probe_boundary.log`; path family with a vertex minimizer and with
  a face minimizer, `∇F(x*) ≠ 0`, `n = 8, 16`; the review's runs reached
  `n = 32` for the face case) localize as in the interior case (ratio at
  most 0.64 and 3.18) and stop. This suggests, but does not prove, that
  (S) is an artifact of the proof.
- **Constants.** `theta*` and `K*` are far from the computed values: on
  the path family `theta* ≈ 8.2e-8` and base `≈ 8.8e9`, against
  `theta = 1/8`, base 52 and localization `3`–`6 W_j` in the computations.
  The proof's base is a polynomial of high degree in `k`, `w`, `M_a/c_g`,
  quadratic in `M_a/c_g` (linear in [D]); I have not tried to lower it. The slope lag (slopes from the previous stage) costs a factor
  of about 70 in the gap constant on the path family; a second dynamic
  program per stage with refreshed slopes would likely remove most of it
  (not tried).
- **Cost measure.** Boxes and dynamic-program runs are counted; (leaf,
  cell) pairs are 2.8–4.8 times the leaves in the computations but are not
  bounded (Remark 3.4).
- **Reading (R1) without (QG):** open (Section 7).
- **Exact-bag splits under (QG):** is there an exact split with a discount
  independent of `n`, so that a bracket rule could match Theorem 3.4
  (end of Section 5)?
- **The `theta` threshold in practice.** For `b = 0.8` (`c_g >= 0.100` at
  all tested sizes, about 0.10 to 0.12 at `n = 256`), `theta = 1/8` works up
  to `n = 256`. For `b = 0.88` every tested `theta` (down to `1/32`) failed for
  some `n <= 64`, but `c_g` falls with `n` there (from at least 0.073 at
  `n = 8` to at most 0.025 at `n = 64`). With the conditioning held fixed,
  `theta = 1/16` worked for `n = 8, ..., 64` at `c_g >= 0.073`, and at
  `c_g` lower bound 0.035 it worked for `n = 8` and failed for `n = 16`
  (Section 8.3). Smaller `theta` and longer chains at fixed conditioning
  were not tested. Theorem 2 guarantees a threshold independent of `n`, but
  its `theta*` is far smaller than anything run.
- **Computations** are on the path family (`w = 1`, `k = 2`, `n <= 256`),
  random linear terms (`n <= 32`), the path with `b = 0.88` and paths with
  the conditioning held fixed (`n <= 64`), binary trees (`m <= 127`; `k = 3`)
  and one quadratic path in the exact-bag model. No `k >= 3` path
  decomposition was run, so the tree computations do not separate
  branching from `k`.

## 11. Commands run

All from `research-20260929/theory-decomposition/adaptive2/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, Python 3.13,
NumPy 2.5.1, SciPy 1.18.0. Targeted checks of this note only; no
project-wide verification was run and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 run_gr.py zero 4 64 1e-4 16 4` | `logs/gr_zero_eps1e-4.log` | Section 8.1, `theta = 1/16`: per bag 29k–38k, 1,711 leaves split per bag per stage, `zloc = 3` |
| `python3 run_gr.py zero 4 32 1e-6 16 4` | `logs/gr_zero_eps1e-6.log` | Section 8.1, `eps = 1e-6`, `theta = 1/16` |
| `python3 run_gr.py zero 4 256 1e-4 8 4` | `logs/gr_zero_eps1e-4_theta8.log` | Section 8.1, `theta = 1/8`, `n = 4..256`: per bag 12.1k–17.1k, at most 639 split per bag per stage |
| `python3 run_gr.py zero 4 128 1e-6 8 4` | `logs/gr_zero_eps1e-6_theta8.log` | Section 8.1, `eps = 1e-6`, `theta = 1/8`, `n <= 128` |
| `python3 run_gr.py theta 32 1e-4 4` | `logs/gr_theta_n32.log` | Section 8.3: `theta = 1/4` loses localization; `1/8, 1/16, 1/32` keep `zloc = 3` (12-stage cap) |
| `for n in 8 16 32; do python3 run_gr.py random $n 1e-4 16 4; done` | `logs/gr_random_eps1e-4.log` | Section 8.2, `R = 4`: `zloc` 3.1–5.7 from stage 3 on, up to 264 boxes violate the graded invariant |
| `python3 run_gr.py zero 16 16 1e-4 16 12; for n in 8 16 32; do python3 run_gr.py random $n 1e-4 16 8; done` | `logs/gr_R_checks.log` | `R = 12`: no wide split; `R = 8`: no violation of the graded invariant |
| `python3 run_ls_single.py scaling 64 1e-4` (LS of [E], unchanged `ls_lib.py`) | `logs/ls_scaling_n64_eps1e-4.log` | LS at `n = 64`: size 2,195,591, processed 36,423,324, up to `32.9 n` split per bag per level, `\|x^cons - x*\|_inf = 3 s_i` at the last sublevels |
| `python3 check_bd_qg.py 1e-6` | `logs/check_bd_qg.log` | Proposition 6 and Section 8.5: `bd` uses `9.4 sqrt(n)` cells per edge; bound holds with ratio `>= 13`; graded split gap `<= 0.13 eps` with 72–96 cells per edge |
| `python3 check_tree_dp.py` (first version; the log was overwritten by the rerun below, with identical lines for checks (1)–(2)) | `logs/check_tree_dp.log` | tree DP: solver never above an `801 x 801` grid minimum (200 boxes); `l_r <= f*`; unrelaxed configuration value `>= l_r` (a weak test; first described as "configuration value consistent") |
| `python3 tree_gr.py zero 7 127 1e-4 16 4 0.55` (the queued second command, `theta = 1/8` up to `m = 255`, was cancelled before it started, to limit computation) | `logs/tree_zero_eps1e-4.log` | Section 8.4, `b = 0.55`, `c = 0`: `zloc = 4` for `m >= 15`, 1,788 split per bag per stage; the `m = 127` run was stopped by hand (kill of its process id) after stage 10 |
| `python3 tree_gr.py random 7 127 1e-4 16 8 0.55` | `logs/tree_random_eps1e-4.log` | Section 8.4, random `c`: `zloc` 3.4, 4.0, 4.5, 4.9 for `m = 7..63`; the `m = 127` run was stopped by hand after stage 9 (`zloc` up to 5.3). A first run with a diagnostic bug was discarded (below) |
| `python3 tree_gr.py zero 7 63 1e-3 8 4 0.62` | `logs/tree_zero_b062_eps1e-3.log` | Section 8.4, `b = 0.62`, `theta = 1/8`: `zloc` 4 for `m <= 15`, 10–16 for `m = 31, 63`; all runs stop |
| `python3 tree_gr.py zero 7 63 1e-3 16 4 0.62` | `logs/tree_zero_b062_eps1e-3_theta16.log` | Section 8.4, `b = 0.62`, `theta = 1/16`: `zloc` 4–6 for `m <= 31`, 4–8 for `m = 63`; all runs stop |
| `python3 run_gr_b.py 0.88 8 1e-3; python3 run_gr_b.py 0.88 16 1e-3` (run from an identical copy at `/tmp/path_b.py`) | `logs/gr_path_b088_eps1e-3.log` | Section 8.3: localization lost at `theta = 1/8` (`n = 8, 16`) and at `theta = 1/16` (`n = 16`); `theta = 1/16` works at `n = 8`. The two `n = 16` runs were stopped by hand (kill of their process ids) after stages 15 and 12; a comment line appended to the log to say so was overwritten by the still-running job |
| `python3 run_gr_b.py 0.88 32 1e-3` | `logs/gr_path_b088_eps1e-3_theta32.log` | Section 8.3, `b = 0.88`, `theta = 1/32`: `zloc = 3` for `n = 8, 16, 32`; at `n = 64` localization is lost from stage 6, and the run (5.1M leaves) was stopped by hand after stage 10 |
| `python3 summarize_logs.py` | `logs/summarize_logs.log` | per-stage `zloc` and sizes quoted in Sections 8.3–8.4 (its parser attaches the stages of the two `b = 0.88` runs stopped by hand to the next run; Section 8.3 quotes them from the raw log) |

Added after review (same environment, targeted checks only):

| Command | Log | Result |
|---|---|---|
| `python3 constants_gr.py` | `logs/constants_gr.log` | path family: `theta* ≈ 8.19e-8` (`2^-23.5`), `K* ≈ 7.27e8`, `R = 3K* ≈ 2.18e9`, base `≈ 8.77e9`; `K_1(gamma(K*), theta*)/K* = 0.79 <= 1`; `K_1(0, 0) ≈ 1.76e6`, `K_LS ≈ 1.36e8`; exponents of `k` in `K*` and `1/theta*` about 5 and 4 (`kappa = 100`), of `kappa` 2 and 1.5 |
| `python3 cg_by_size.py` | `logs/cg_by_size.log` | size-dependent `c_g` bounds of all test families (Sections 8.3–8.4), local constants at `x*` for the random-`c` instances, couplings for fixed conditioning |
| `python3 check_tree_dp.py` (after adding check (3); `tree_gr.dp_min` now also returns the leaf and cell indices of the minimizing configuration, with no change to the computation) | `logs/check_tree_dp.log` | checks (1)–(2) as before (identical lines); check (3): relaxed value of the minimizing configuration equals `l_r` within `8.9e-16`, 0 constraint violations |
| `python3 run_fixed_cg.py path 16 1e-3 16 16:0.841253 32:0.830691 64:0.827896` | `logs/fixedcg_path_c073_theta16.log` | `c_g >= 0.073` fixed, `theta = 1/16`: `zloc = 3` from stage 3, stop stages 11, 11, 12 (110 s for `n = 64`) |
| `python3 run_fixed_cg.py path 16 1e-3 16 8:0.920531` | `logs/fixedcg_path_c035_theta16.log` | `c_g >= 0.035` fixed, `n = 8`, `theta = 1/16`: `zloc = 3`, stop stage 10 |
| `python3 run_fixed_cg.py tree 8 1e-3 14 7:0.759342 15:0.663689` | `logs/fixedcg_tree_c141_theta8.log` | `c_g >= 0.141` fixed, `theta = 1/8`: `zloc = 5` from stage 4, stop stages 9 and 10 |
| `python3 run_fixed_cg.py tree 8 1e-3 14 63:0.595954` | `logs/fixedcg_tree_c141_theta8_m63.log` | same, `m = 63`: `zloc` 4, 6, 16, 10, 12, 14, 12, 10, 18, 10 at stages 3–12, stop stage 12 (591 s) |
| `python3 probe_boundary.py` | `logs/probe_boundary.log` | vertex minimizer (`n = 8, 16`): stop stages 7, 8, `zloc <= 0.64`; face minimizer (`n = 8, 16`): stop stages 11, 12, `zloc <= 3.18`; reproduces the review's figures for these sizes |

The four `run_fixed_cg.py` commands ran in parallel, each under `timeout`
(1800–3600 s); none hit its limit or its stage cap.

Added after review round 2 (same environment plus
`PYTHONDONTWRITEBYTECODE=1`, targeted checks only):

| Command | Log | Result |
|---|---|---|
| `curl -s https://api.crossref.org/works/10.1137/21M1391079` (parsed with a one-line Python filter) | – (not kept) | SIAM J. Optim. 32(2), pages 1156–1183, issued 2022-05-31, authors Shin, Anitescu, Zavala, title as cited |
| `curl -sL https://export.arxiv.org/abs/2101.03067` (title and `citation_doi` extracted with `grep`) | – (not kept) | title "Exponential Decay of Sensitivity in Graph-Structured Nonlinear Programs", DOI 10.1137/21M1391079 |
| `timeout 1200 python3 check_bd_qg.py 1e-6` (325 s) | written to `/tmp`, compared with `diff` | byte-identical to `logs/check_bd_qg.log` |

Not kept: a smoke run of `gr_lib.py` (`n = 4, 8, 16`, `theta = 1/16`, before the
`wide` counter was added; same sizes as `logs/gr_zero_eps1e-4.log`); a first
run of `tree_gr.py random` whose `zloc` used the wrong parent vertex for bag
2 (a diagnostic bug, fixed before the logged run; refinement and bounds were
not affected); two first versions of `check_bd_qg.py` whose comparison split
was wrong (chords of the original instead of the reduced value functions,
then a single cell on edges `2..n`; the second gave a gap of about
`0.2 (n-1)`, Section 5).

## Revision after review

### Round 1

Round 1 review: [`../reviews/adaptive-matching-review.md`](../reviews/adaptive-matching-review.md).
I checked each point myself before changing the note. "By hand" means I
redid the argument; computations are in double precision (not exact
arithmetic) and are listed in Section 11 under "Added after review". No
Lean was used: the corrected statements are short inequalities, and a
formal proof would not strengthen a key finite lemma here.

1. **Remark 3.3 (trees): two gaps; corrected.**
   - *Slope bound.* The claim "at most `k - 1` bags of `sub(t)` contain a
     variable of `S_t`" can fail on trees with `k >= 3` and `w >= 2`.
     Checked by hand on the review's
     example: `V_p = {1, 2}`, `V_t = {1, 2, 3}`, children `{1, 3, 5}` and
     `{2, 3, 6}` is a valid tree decomposition (each `T_i` is connected),
     with `k = 3`, `w = 2`, and all three bags of `sub(t)` meet
     `S_t = {1, 2}`. From the definition of `lambda_t` (Lemma 3.2 of [D]) the
     bound holds coordinatewise, giving
     `nu_t <= (k-1) M_a sqrt(w(w+1)) |x - x*|_inf`; only the constant in
     `gamma` changes (`gamma_T`). On paths the original bound is right (the
     bags are `t, ..., t + k - 2`).
   - *Fixed point.* The induction of Theorem 2(a) needs
     `K_1(gamma(K), theta) <= K`, which a `|T|`-independent `K_1` does not
     give (`K_1 = 1 + gamma` has no fixed point because
     `gamma_T(K) > K`). Remark 3.3 now states the property it needs,
     (Loc_T), and a sufficient growth condition with explicit `K_T` and
     `theta_T` (checked by hand). On the path family, Lemma 1's constants
     satisfy the fixed point with ratio `K_1(gamma(K*), theta*)/K* = 0.79`
     (`constants_gr.py`). "The open problem for trees is therefore exactly
     ..." now reads "the remaining step of this route ... sufficient, not
     shown necessary". Conjecture 7, Summary item 3, Section 10 and the
     status table are restated accordingly.
   - *Consequence found while fixing this.* The sketch for trees with `L`
     leaves (Section 6) concluded `|T| (C sqrt(L))^{w+1} log(|T|/eps)` for GR
     and called it an interpolation between Theorem 2 and LS. With the
     fixed point, the term of `K_1^2` linear in `gamma` is divided by
     `eta^2`, which the sketch shrinks by `L + 1`, so the sketch gives
     `K_T = O(L)` and base `O(L)`: it beats LS only for `L = o(sqrt|T|)`.
     The old conclusion is withdrawn (it would hold only at a fixed slope
     error, for example with exact slopes). This is still a sketch.

2. **Conditioning comparisons in Sections 8.3–8.4 and Summary item 3:
   withdrawn and replaced.** I computed `c_g` bounds at the tested sizes
   (`cg_by_size.py`: lower bound `0.9 - |b| rho(A)/2`, upper bound from
   feasible points). They confirm the review: the `b = 0.62` trees that lose
   localization have `c_g >= 0.141` (`m = 31`) and `>= 0.110` (`m = 63`),
   the `b = 0.88` paths have `c_g <= 0.047` for `n >= 16`, and `c_g` falls
   with the size in every family (by about 3.5 times on the `b = 0.88`
   path from `n = 8` to 64, about 2–2.5 times on the `b = 0.62` trees and
   1.6–1.8 times on the `b = 0.55` trees from `m = 7` to 63). Withdrawn:
   "similar conditioning", "too-large `theta` rather than an effect of
   branching", the explanation of the `b = 0.88` pattern by chain length
   alone, and the contrast that suggested a branching cause
   for the slow growth of the random-`c` tree ratio (the local constant at
   `x*` falls from 0.44 to 0.29 over `m = 7..63`). New runs with the
   conditioning held fixed (`run_fixed_cg.py`, four runs, about 15 min of
   computation in total):
   - path, `theta = 1/16`, `c_g >= 0.073`: ratio 3 for `n = 8, ..., 64`;
   - path, `theta = 1/16`, `c_g >= 0.035`: works for `n = 8`, while the
     earlier `n = 16` run at the same lower bound failed;
   - tree, `theta = 1/8`, `c_g >= 0.141`: ratio 5 for `m = 7, 15`, 10–18
     for `m = 31, 63` (the `m = 31` point is the earlier `b = 0.62` run).
   So in the tested range the admissible `theta` depends on size even at
   fixed conditioning (path at the worse conditioning, tree), and not at
   `c_g >= 0.073` on the path up to `n = 64`. At comparable conditioning
   the trees need a smaller `theta` than the `b = 0.8` path, but the tree
   decomposition has `k = 3`, so branching is not isolated. These results
   are stated in Sections 8.3, 8.4, the Summary and Section 10.

3. **Heuristics labelled; heading renamed; scope of Proposition 6
   stated.** Summary item 4, Section 5 item 1 and the "Bag errors"
   paragraph now say which statements are heuristic (the min-marginal
   surrogates "carry the global relaxation error that defeats LS", "Lemma 1'
   imposes the same equal share", the leaf-count estimate under an assumed
   quadratic margin). The heading is "Why rule `bd` does not match". A
   *Scope* paragraph after Proposition 6 says it covers rule `bd` exactly as
   in [Cov] (graded split `psi`, discount `w_e/(2n)`, exact value functions,
   separator cells). Checked against Theorem 1 and Corollary 3.2 of [Cov].
   The proposition itself is unchanged (the review confirmed it by hand and
   reproduced the `bd` counts).

4. **Literature: precursors added and the novelty claim narrowed.** Added
   Shin–Anitescu–Zavala (SIAM J. Optim. 32(2) 2022, 1156–1183,
   doi:10.1137/21M1391079, arXiv:2101.03067; this entry first gave the
   wrong pages 1110–1136, corrected in round 2, item 10), discrete
   differential dynamic programming (Heidari, Chow, Kokotović and Meredith
   1971), Luus's iterative dynamic programming (book, 2000) and
   Munos–Moore (2002), with access levels (abstracts, bibliographic records
   and search snippets; I checked the bibliographic data myself, but missed
   the wrong pages of Shin–Anitescu–Zavala). The review gives
   arXiv:2101.06350 for Shin–Anitescu–Zavala; that is the related
   Shin–Zavala paper, and the note cites 2101.03067 (as does the
   continuation's audit). The Significance paragraph and Section 9
   now credit the refine-around-the-current-DP-optimum mechanism to these
   precursors and confine the claim to the localization lemma for relaxed
   decomposition dynamic programs, the certificate-producing algorithm with
   the instance-dependent count, and Proposition 6. No prior result giving
   Theorem 2 was found; the search was short and snippet-level and does not
   establish novelty.

5. **Scope of the answer.** Summary item 1, the Significance paragraph and
   the comparison in Section 3.2 now state (S) and the path restriction
   next to the claim, and that the proved base is quadratic in `M_a/c_g`
   (`K* = Theta(k^5 w^2 kappa^2)` for bounded `a`), against linear in [D].
   "Closes the gap" is gone. Numbers on the path family, recomputed with my
   own script from the note's formulas (`constants_gr.py`):
   `theta* ≈ 8.2e-8`, `K* ≈ 7.3e8`, base `≈ 8.8e9` (practice:
   `theta = 1/8`, base 52); they match the review. The exploratory
   boundary-minimizer runs were repeated for `n = 8, 16`
   (`probe_boundary.py`; same figures as the review); the note now says
   they suggest, without proving, that (S) is a proof artifact.

6. **Corollary 3: budget enforced during refinement.** The algorithm now
   checks the box budget before every split and aborts at the first split
   that would exceed it; the proof explains why a check after the
   refinement is not enough (a run with a wrong `mu` can create about
   `N 2^{(j+1)(w+1)}` boxes in one refinement). Checked by hand. While
   checking, I also tightened the stage-cap step:
   `j* <= lambda_eps + ceil((1/2) log2(C_term N))` (the first version had
   `+ 1`), so the stopping stage `j*` lies within the cap of
   `r* + lambda_eps` stages (indices `0, ..., r* + lambda_eps - 1`); the
   first version's bound left an off-by-one under that reading.

7. **Corollary 4: "explains" replaced by "is consistent with".** The proof
   constants on that family are `K_1(0, 0) ≈ 1.8e6` and `K_LS ≈ 1.4e8`
   (`constants_gr.py`), far above the observed ratios 4–6.

8. **`check_tree_dp.py` check (2): description corrected and check
   strengthened.** Confirmed by reading the script that check (2) only
   tests "unrelaxed value `>= l_r`". Added check (3): the relaxed value of
   the reconstructed minimizing configuration, recomputed from its leaves,
   copies and slopes, and the configuration constraints. For this,
   `tree_gr.dp_min` now also returns the leaf and cell indices (no change
   to the computation; the fixed-conditioning tree runs used the version
   before this change). Rerun: `|Phi - l_r| <= 8.9e-16`, 0 violations,
   and checks (1)–(2) reproduce their earlier lines exactly. Section 8.4
   and Section 11 describe the checks as they are.

9. **Minor points.**
   - "3.2–5.7" is now "3.1–5.7 from stage 3 on" (checked in
     `logs/gr_random_eps1e-4.log`: minimum 3.118 at `n = 8`, seed 0,
     stage 7; maximum 5.728 at `n = 16`, seed 1, stage 8).
   - Stage counts are now called the index of the stopping stage (one fewer
     than the number of dynamic-program runs; checked against the
     `stages=` field of the SUMMARY lines, which is the last stage index),
     in the Summary, the tables of Sections 8.1 and 8.4 and the text.
   - The LS ratio at `n = 64` is now quoted over the failed sublevels of the
     last pass: 8 at sublevel 4, 6 at sublevels 5–10, 3 at 11–12 (checked in
     `logs/ls_scaling_n64_eps1e-4.log`).
   - Order of `1/theta*`: now `O(k^4 w kappa (1 + sqrt(w kappa)) + k^{1.5} sqrt(a))`.
     The review's `k^4` is right when `w kappa >= 1`. When `w kappa < 1`
     (possible, since only `kappa >= 2/k` is known) the `theta_1` term
     `1/(648 k^4 (w+1) kappa)` can bind (`constants_gr.py`: at `k = 32`,
     `w = 1`, `kappa = 2/k` it does). The first version's `k^{4.5}` is a
     valid but looser bound.

Not changed: Lemma 1, Theorem 2 for paths, Proposition 6 and their proofs
(the review confirmed them by hand, and my checks above found nothing
against them); the `b = 0.55` tree tables and all earlier logs.

### Round 2

Confirmation review:
[`../reviews/adaptive-matching-confirm-r1.md`](../reviews/adaptive-matching-confirm-r1.md).
It found all nine round-1 points fixed and raised three text-only problems.
I checked each one myself before changing the note. All three were right.
No proof, statement of a result or computation changed; the commands are in
Section 11 under "Added after review round 2".

10. **Shin–Anitescu–Zavala: wrong pages; corrected and DOI added.** The note
    gave SIAM J. Optim. 32(2) (2022) 1110–1136. I queried Crossref for DOI
    10.1137/21M1391079: pages 1156–1183, volume 32, issue 2, issued
    2022-05-31, same title and authors. The arXiv abstract page of
    2101.03067 has the same title and gives this DOI. So the pages were
    wrong (the round-1 entry said the bibliographic data were checked; for
    this paper the check missed the pages). Section 9 and Revision item 4
    now give pages 1156–1183 and the DOI; item 4 keeps the wrong pages,
    marked as corrected, so the record shows what changed. Title, authors,
    volume, issue, year and the arXiv number were right and are unchanged.
11. **Proposition 6: claim narrowed to one-dimensional separators.** Summary
    item 4 said the discount "costs `sqrt(n)` per separator dimension per
    halving", and Section 5 item 2 said "`sqrt(n)` per separator dimension
    (proved for rule `bd`)". I reread the proof: every separator is a single
    variable `s_t`, cells are intervals `[d - r, d + r]`, and the counting
    step gives at least `sqrt(K_t - 2)/12 >= sqrt((n - 5)/2)/12` cells per
    dyadic range `[2^-i, 2^{1-i}]` on each covered edge. So what is proved
    is `sqrt(n)` cells per edge per halving, for one-dimensional separators.
    Nothing in the proof covers boxes in two or more separator coordinates.
    Changed: Summary item 4 and Section 5 item 2 now say "per edge per
    halving (proved for one-dimensional separators)" and state "`sqrt(n)`
    per separator dimension (`n^{w/2}` cells per edge per halving) for
    `w >= 2`" as a conjecture; the *Scope* paragraph, the opening of
    Section 5 and the status-table row now say that the proof covers the
    quadratic path family of Proposition 6, whose separators are
    one-dimensional. The proposition, its
    proof and the numbers are unchanged; I reran `check_bd_qg.py 1e-6`, and
    its output is byte-identical to `logs/check_bd_qg.log` (Section 8.5). I
    did not try to prove the higher-dimensional case.
12. **Theorem 2: (S) added to the two restatements that omitted it.**
    Summary item 5 now says "algorithmic for path decompositions with (S)
    (`∇F(x*) = 0`)", and the status-table row for Theorem 2 says "proved
    (path decompositions, with (S) `∇F(x*) = 0`)". Checked against the
    statement of Theorem 2 in Section 3, which assumes the setting of
    Section 1.1, including (S). I searched the note for the other mentions
    of Theorem 2. The other restatements of its scope (Summary item 1, the
    Significance paragraph, Section 3.2, Remark 3.3, Section 7) already name
    (S). Summary item 3, which restates Remark 3.3 for trees, did not; it
    now says "For a tree decomposition (still with (S))" (not raised by the
    review; found during this search). The remaining mentions are proof
    steps, numerical comparisons, the literature assessment and the round-1
    revision record ("Theorem 2 for paths" in the "Not changed" line, left
    as written), which restate no scope beyond what their context gives.
