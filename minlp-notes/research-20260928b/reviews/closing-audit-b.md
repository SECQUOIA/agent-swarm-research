# Closing audit (b): final-round changes in three notes

Date: 2026-09-29. Auditor: fresh independent reviewer; I had not seen these
notes before. Scope: only the final-round changes named in the brief.

1. [`sparse-regression/phase-transition.md`](../bb-complexity/sparse-regression/phase-transition.md),
   subsection "Second round: recheck of the revision".
2. [`binary-least-squares/certification-thresholds.md`](../bb-complexity/binary-least-squares/certification-thresholds.md),
   Section 10.1 (F1–F10).
3. [`spatial-face-exact/face-exact-node-complexity.md`](../bb-complexity/spatial-face-exact/face-exact-node-complexity.md),
   "Second revision" in Section 11.

I did not edit the notes and did not commit. My scripts and logs are in
[`closing-audit-b/`](closing-audit-b/). They import nothing from the notes'
`code/` directories or from earlier reviewers' scripts. Where an instance had
to match the author's, I rewrote the generator from its documented form. The
match is confirmed by stored values: `f(S*) = 82.6998`, `lam = 11` and 521
violators at seed 1007; the box gap 0.232 at `N = 200`.

## Verdict

| Item | Verdict | Corrections |
|---|---|---|
| 1. Sparse regression, second round | **Correct, with one false constant.** My own solver reproduces the seed-1007 node values. Over all 3195 forced-in nodes, exactly the four stated nodes fail. The total-energy remark, the Conjecture 5.2 condition and the PWE remark are correct. | The Summary's "`c'` at most about 0.11 (as `x -> 0`)" is false: the supremum is `3 - 2 sqrt 2 ≈ 0.17`. Three `c'` values are slightly low. "Within 2.75" holds only for the nodes the author solved; over all nodes the bound is 2.79. |
| 2. Binary least squares, F1–F10 | **Correct.** The proof of Proposition 6.3(b) is complete. The gaps of the shifted relaxation reproduce: `4.66e-4` at `rho = 300` (`3.87e-4` with `d = lambda_min`), and exact in 4 of 4 instances at `rho = 600`. The factor `N+1` in the Summary is needed and gives a true statement. | At `rho = Theta(N)`, the log form of Theorem 4.1 (and so the Summary's sentence) does not follow from the theorem's displayed bound. It needs a sharper node count, which I give below. Optional wording change for F9. |
| 3. Face-exact, second revision | **Correct.** I verified every step of Proposition 3.14 by hand and numerically. All kink counts reproduce in exact arithmetic, including the product-score strong-branching row, which the note labels floating point. The tie rule and the coordinate-versus-point remark of Proposition 5.4(d) are correct. | Optional: state the value of `a` for the incumbent counts, and relabel the strong-branching row as exact. |

## 1. Sparse regression (`phase-transition.md`, second round)

### 1.1 Seed 1007 at `p = 3200` (items 1–2 of the round)

**Solver.** `sparse_s1007_audit.py` solves each forced-in node by accelerated
projected gradient (FISTA with backtracking and restarts) on the full
`z in R^3200`. It uses no column generation and no conic solver. Each value
is certified by a bracket:

- the upper bound is `g(z)` at a feasible `z`;
- the lower bound is the dual bound of Lemma 1.1, evaluated on the whole
  node at `a = M_z^{-1} y`.

`sparse_all_nodes.py` runs this for **every** null `j` (3195 nodes, 4
processes). The largest bracket width is `2.3e-5`.

| claim in the note | my value |
|---|---|
| `f(S*) = 82.700`, price `m0^2/lam = 7.16`, `tau^2 = 1.96` | 82.6998, 7.1627, 1.962 |
| 521 violators (203–326 in the other seven seeds) | 521 (203, 216, 292, 294, 301, 319, 326) |
| sat-gain 70.3 (13.8–30.9 in the other seven) | 70.29 (13.8–30.9) |
| realized price 7.2–8.9 at `p = 3200` | 7.16–8.94 |
| `j = 991` (rank 1) fails by 2.414 | bracket `[-2.413676, -2.413675]` |
| `j = 2714` (rank 6) fails by 0.124 (value 82.576) | bracket `[-0.1237754, -0.1237748]` |
| `j = 1453` (rank 5), `j = 2119` (rank 50) fail by 0.454, 0.023 | −0.4538, −0.0229 |
| rank-2 null passes by 0.024 | `j = 895`: `[0.02363, 0.02364]` |
| exactly four failures (ranks 1, 5, 6, 50) | **exactly these four** among all 3195 nodes. The other 3191 are certified above `f(S*)` by the dual bound; no bracket contains 0. |
| seed 1000: ranks 1, 5, weakest give 5.99, 5.87, 8.70 | 5.9939, 5.8687, 8.7007 |

The explanation now in the note is supported by the data: a finite-size
many-violator balance, with the own-fit term deciding which nulls fail.
For every forced-in node, the relaxation recovers at least 61.0% of the
price, so "about 60% ... for every forced-in feature" (Summary, remark after
Corollary 3.4) is accurate.

**Correction (minor).** Section 6.3 and round item 1 say that every solved
forced-in node is within 2.75 of `f(S*)`. This is true for the nodes the
author solved (ranks 1–60, 100, 500, median, weakest). Over all nulls,
however, the largest value is `f(S*) + 2.790` (`j = 2310`, rank 2816), and
931 nodes exceed 2.75. Suggested wording: "every forced-in node is within
2.79 of `f(S*)` (all 3195 solved in an independent check)", or keep 2.75 and
leave the qualifier "we solved" visible.

The code changes to `decide_c1_exact` (round item 3) match the description:
it returns `'undecided'` after `max_solves` and `'C1-nonstrict'` on
tolerance passes. The stored `c1_redecided.jsonl` has at most 109 solves and
empty `notes`. The seed-1007 root gap 9.94 and the other seeds' gaps
2.92–5.68 are stored there and agree with the note.

### 1.2 Hard side: `k -> inf` and the constant `c'` (round item 4)

`k -> inf` now appears in Theorem 4.3 (inherited by 4.4), in the Summary and
in Section 5. The proof uses it: `delta = 1/k`, and the `O(log(p/k))` loss
in the Gilbert–Varshamov step.

The largest `c'` admitted by Steps 2–6 satisfies two constraints:
`c' < (1-mu) theta`, and (*) with `B = 1 + 2 sqrt(c'x) + 2c'x`. For fixed
`(mu, theta)` the largest `c'` has a closed form. I maximized over
`(mu, theta)` with a fine grid plus Nelder–Mead (`cprime_audit.py`):

| `x` | 1e-6 | 1e-3 | 1e-2 | 0.05 | 0.2 | 0.5 | 0.8 | 1.0 | 1.2 |
|---|---|---|---|---|---|---|---|---|---|
| `c'_max` (pure noise) | 0.1712 | 0.1610 | 0.1396 | 0.1059 | 0.0588 | 0.0223 | 0.0068 | 0.00195 | 0.00009 |
| note | | | | 0.106 | 0.058 | 0.022 | 0.0066 | 0.0018 | 0.0001 |
| planted, `kappa_s = K(x)/2` | | | | 0.0208 | 0.0114 | 0.0046 | 0.0015 | 0.00046 | 0.00002 |

**Correction (needed).** The Summary says the `c'` the proof delivers is "at
most about 0.11 (as `x -> 0`)". This is false. As `x -> 0`, `B -> 1` and
`(e^x - 1)/x -> 1`, so (*) becomes `(1+mu)(1-theta) > 1`. The supremum of
`(1-mu) theta` under this constraint is `3 - 2 sqrt 2 ≈ 0.1716`, attained at
`mu = sqrt 2 - 1`, `theta = mu/(1+mu)`. The table confirms the approach
(0.161 at `x = 10^-3`, 0.171 at `10^-6`), which is slow because of the
`sqrt(c'x)` term. Suggested text: "at most `3 - 2 sqrt 2 ≈ 0.17`, approached
only as `x -> 0` (0.106 at `x = 0.05`), about 0.02 at `x = 1/2`, and tending
to 0 as `x -> x0`."

**Minor corrections.**

- Round item 4 lists 0.058, 0.0066 and 0.0018. These are coarse-grid
  underestimates (`check_cprime.py` uses a 99 x 198 grid). The optimized
  values are 0.059, 0.0068 and 0.0020.
- The planted case is 4.1–5.1 times smaller (4.1 at `x = 1.2`), so "about 5
  times smaller" should read "4–5 times smaller".
- Section 5 says "with a small `c'` (Section 4.2)", but Section 4.2 gives no
  values. Either add one sentence there or point to the Summary.

The other constants check: `x0 = 1.2564312`, `2/x0 = 1.5918`,
`K(1/2) = 0.2131`, and `K/(e^x - 1) = 0.816, 0.328, 0.060`. The fixed-`R`
remark `exp(k e(mu,R)(1 - o(1)))` is correct: `e(mu,R) > 0` exactly for
`mu < (R-1)/R`, and `t = O(k) = o(n)` gives `B -> 1`.

### 1.3 Theorem 3.1 total-energy remark (round item 5)

**Correct.** The remark no longer cites Theorem 3.2(b). Its three uses of
`sigma` are the only ones in the proof of Theorem 3.1:

- `omega_lam`;
- the scale-free AM–GM bound on the cross term;
- the leave-one-out term `(sigma/b) sqrt(log p/n)`.

With `lam = sqrt n` and `sigma = gamma/sqrt n`, one gets
`omega^2 = gamma^2 + k b^2 (1 + o(1))`, so
`tau^2 = (1 + o(1)) n b^2/(gamma^2 + k b^2)`.

At the threshold, `n ≈ 2(k + gamma^2/b^2) log p >= log^6 p`. For fixed
`gamma` this forces `k >= log^5 p/2 - O(1)`, so `gamma^2/b^2 = o(k)`, as the
remark says. For `gamma^2 = O(k b^2)`, the error term becomes
`(sigma/b) sqrt(log p/n) = O(sqrt(k log p)/n) -> 0`. The allowance is correct
(it is sufficient; the remark does not claim it is necessary).

Theorem 3.1(c) also survives the extension, although the explicit
`lam = (sigma/b) sqrt(Tn)` would fall below `sqrt n`. Achievability works
with `lam = sqrt n` instead, and the converse `tau^2 < (1 + o(1)) n/k` does
not involve `sigma`.

### 1.4 Conjecture 5.2 (round item 7)

**Correct.** The range `(1+delta)k <= n <= (1-delta) n_IT` is nonempty in the
limit iff `(1+delta)/(1-delta) < 2(1-gamma)/gamma`, that is,
`delta < (2 - 3 gamma)/(2 - gamma)`. Numerically this is 1/3 at
`gamma = 1/2` and 1/7 at `gamma = 0.6`. The quoted `n_IT/k` values 1.54,
1.74 and 1.86 reproduce as 1.537, 1.738 and 1.860.

### 1.5 PWE remark (round item 6)

**Accurate, respectful, and consistent with
[`pwe-verification.md`](pwe-verification.md).** I compared each statement
with the report:

- the model and the statement of Theorem 2, with page numbers;
- the four-step `n -> inf` argument and the limit 0.123;
- `M_S^{-1}` in items 2–3, and "PWE's `M` is our `M_S^{-1}`";
- the normalization mismatch, with Lemma 1 true under `1/(rho n)` and
  Lemma 2 under `1/rho`, and the two incorrect steps;
- the Monte Carlo frequencies 0.080–0.153 (the last interval
  `[0.096, 0.211]` contains 0.123), kept apart from the conditional
  estimates 0.052–0.114;
- "8 of the 16";
- the literature status;
- the report's caveat "at the level of the displayed steps" in the
  total-energy bullet;
- 0.99 tied to `d = 50`, `k = 5`;
- the per-entry repair probability.

The tone is factual, and the remark credits what survives (Corollary 2, the
algorithms, the total-energy reading). One optional point: Section 7's
total-energy sentence cites the report but not its "displayed steps" caveat,
which appears only in Remark 3.5.

## 2. Binary least squares (`certification-thresholds.md`, Section 10.1)

### 2.1 Proposition 6.3(b) (F3): the proof is complete

- `f_d` is convex iff `d <= lambda_min(A'A)` (Hessian `2(A'A - dI)`), and
  `f_d = f` on vertices.
- `x*_i d_i f_d(x*) = -2 zeta_i - 2d`. For a convex function on a box the
  first-order condition is necessary and sufficient, so `x*` minimizes `f_d`
  over the box iff `min_i zeta_i >= -d`.
- (b) Bai–Yin gives `d = lambda_min(A'A) = rho (sqrt beta - 1)^2 (1 + o(1))`.
  Given `w`, the `-g_i` are iid `N(0,1)` (Lemma 0.1), and `||w||^2 = M(1+o(1))`.
  So `max_i(-zeta_i) >= sqrt(2 rho beta log N)(1 - o(1))`. In the stated range
  `d/max(-zeta) <= sqrt(1-eps)(1 + o(1)) < 1`, so `x*` is not a box minimizer
  of `f_d`.
- Given this, `R_d < f_d(x*) = f(x*) = OPT` needs only that `x*` is ML, which
  `rho beta >= (2+eps) log N` provides w.h.p. (Theorem 2.2(a)). The note's
  route through uniqueness is also valid.
- The range in (b) is nonempty for every `beta > 1`, because
  `(sqrt beta - 1)^4 < beta^2`.
- Since the condition `zeta_i >= -d` weakens as `d` grows, `d = lambda_min`
  is the best admissible uniform shift. So (b) rules out every convex
  diagonal shift below the threshold. This could be said in one clause.

**Numbers** (`bls_shift_audit.py T`, 20 seeds). The per-instance threshold
`rho_shift = N (max_i(-x*_i h_i'w))_+^2/lambda_min(H'H)^2` has median
`rho/log N` as follows. The note quotes the recheck's medians.

| `beta` | `N` | this audit | note (recheck) |
|---:|---:|---:|---:|
| 2 | 100 | 75.6 | 73 |
| 2 | 400 | 89.4 | 93 |
| 4 | 100 | 4.5 | 4.5 |
| 4 | 400 | 5.5 | 5.7 |

The asymptotic constants are 135.9 (`beta = 2`) and 8 (`beta = 4`).

### 2.2 Gaps of the shifted relaxation (F2): spot-check of all four instances

`bls_shift_audit.py F` covers `beta = 2`, `N = 200`, seeds 0–3. It uses my
own active-set box-QP solver, not BVLS, and a certified Frank–Wolfe lower
bound. Upper and lower values agree to all printed digits.

- `OPT = W` is certified in every instance, because
  `lambda_min(A'A + diag zeta) > 0` (Proposition 6.1).

| `rho` | median gap, `d = 0.99 lambda_min` | median gap, `d = lambda_min` | exact (`d = lambda_min`) |
|---:|---:|---:|---:|
| 30 | 0.0657 | 0.0647 | 0/4 |
| 60 | 0.0337 | 0.0329 | 0/4 |
| 130 | 0.0104 | 0.0100 | 0/4 |
| 300 | `4.66e-4` (max `5.07e-4`) | `3.87e-4` (max `4.24e-4`) | 0/4 |
| 600 | 0 (to `1e-16`) | 0 | 4/4 |

The box gap is 0.2317 at every `rho`. Every number in F2 and in the Section 6
text reproduces. The note's "`~1e-13` at `rho = 600`" is floating-point noise
in its BVLS path; the value is 0 to rounding.

### 2.3 The factor `N+1` in the Summary (F1)

The factor is needed. At `K = 1` the tree has `2N+1` nodes, which is not
`exp(O(1) log rho)`. With the factor, the Summary's statement is **true**.
However, at `rho = Theta(N)` it does **not** follow from the bound that
Theorem 4.1 displays, and neither does the theorem's own "so
`log #nodes <= (1 + o(1)) (N/(4(2beta-1) rho)) log rho + log(N+1)`".

Write `c = N/(4(2beta-1) rho)`. If `c` stays bounded and is not an integer,
then `K = ceil(c(1+o(1))/kappa_rho) = ceil(c) > c`. The display gives
`log(N+1) + K log(eN/K) ≈ (1 + ceil c) log N`, while the claim is
`(1 + c) log N`.

Example (`bls_count_K.log`): `N = 10^6`, `beta = 1`, `rho = N/6`, `c = 1.5`,
`K = 2`.

| bound | log value |
|---|---:|
| displayed bound | 40.75 |
| Summary form (with `o(1) = 0`) | 31.85 |
| true count (below) | 28.04 |

**Fix (one line).** Nodes with `|Wr| = K` are pruned, so every *branched*
node has `|Wr| <= K-1`. By the hockey-stick identity,

```
#nodes <= 1 + 2 sum_{d<N} sum_{j<=K-1} C(d, j) = 1 + 2 sum_{i=1}^{K} C(N, i) <= 1 + 2 (eN/K)^K .
```

With `K <= c(1+o(1))/kappa_rho + 1`, this gives
`log #nodes <= (1 + o(1)) c log rho + log(eN) + O(1)`. That is the Summary's
`(N+1) exp((1 + o(1)) c log rho)` (the constant is absorbed, since
`c log rho -> inf`). Replace the display, or add this count, so that the
second form and the Summary follow for every `rho -> inf`, `rho beta <= N`.

### 2.4 Other items

- **F4, F5, F6, F8, F10.** The texts are as described.
  - Conjecture 3.3 and the text after (d) say "implied by" and "sufficient
    but not necessary".
  - Theorem 3.1 fixes `theta > 0` and records where `theta N >> log N` is
    used.
  - Summary (6) and Section 7.3 compare node counts, with the wall-clock
    caveat.
  - The status line records the reviews.
  - The proof of Theorem 5.1(a) uses `q` for ternary vectors.
- **F7.** The arithmetic `20199/10^{5(1-3/8)} = 15.1` checks. I did not rerun
  the scan; the recheck did so independently.
- **F9 (optional wording).** The quoted `kappa_rho` values
  (0.20–0.23, 0.41–0.42, 0.56–0.57, 0.68) reproduce (`bls_exponent_G.log`).
  "The proved exponent is 1.5–5 times the asymptotic constant" is right for
  the prefactor `1/kappa_rho` (1.46–4.96). Comparing the whole proved
  exponent `K log(eN/K)` with `(N/(4(2beta-1) rho)) log rho` at `N = 10^6`
  gives a larger factor:
  - 2.0–5.6 for `beta = 1`;
  - 2.45–8.5 for `beta = 2`.

  The reason is that `log(eN/K)` exceeds `log rho` by `log(4e(2beta-1)kappa_rho)`.
  Say "prefactor", or quote the full ratio.

## 3. Face-exact (`face-exact-node-complexity.md`, second revision)

### 3.1 Proposition 3.14: correct

I checked each step by hand. `curved_audit.py` checks them numerically.

- **Convexity and model.** `f = G(D, y) + D y` with
  `G = max_s [-sD - psi(s) y + psi(s) s]`, a maximum of affine functions of
  `(D, y)`, hence of `x`. So `g` is convex and continuous. `phi = x1 y - x2 y - c0 y`
  lives on the path `x1 - y - x2`. There were 0 violations in 20000 midpoint
  tests of `G`.
- **(a) Nonnegativity.** `s = y` gives `f >= 0`. `psi' = -1 - s <= 0` on
  `[-1, 2]`, so `f = 0` on `Sigma` (max `|f|` on `Sigma` was `1e-31`).
- **(a) Growth.** `|delta| <= 1.75` because `D in [-1.75, 0.25]` and
  `psi(y) in [-1.5, 0]`. So `s = y - delta/8 in [-0.22, 1.22]`,
  `|psi'| <= 2.219` there, and `(1 - 2.22/8)/8 = 0.0903 >= 1/12`. The minimum
  of `f/delta^2` is 0.1231 on a grid and 0.1237 on 200000 random points,
  consistent with `>= 0.0833`.
- **(b) Non-transversality.** The normal is `(1, -1, -psi'(y))`, which is
  orthogonal to `(1,1,0)`. `{x1, x2}` is independent in the path graph.
- **(c) Row-slice bound.**
  - The row is an interval of length `ell <= 1` (the `t`-range lies in
    `[0,1]`). Its midpoint `p` has `d_x1, d_x2 >= ell/2`, and `m(p) = 0`.
  - Lemma 2.1(c) on both terms gives `Gamma_C(p) >= ell d_y`. With exact
    McCormick gaps on 20000 random boxes and rows there were no violations
    (minimum ratio 1.000000).
  - `2 int_0^{w/2} min(1, eps/d) dd <= 2eps(1 + ln(1/(2eps)))` for `w <= 1`
    and `eps < 1/2`.
  - `A = 1 - (2P(y0) - P(1))` with `y0 = sqrt(2.5) - 1`. This gives
    `A = 0.614769` in closed form, and the same by quadrature. The Summary's
    0.307 is `A/2`.
- **(d) Bound from Theorem 3.6 with `p = 2`.**
  - Taking `K = S` gives `tau H^2(S) <= max_E W_i W_j`. With `E ⊆ {x1y, x2y}`
    and `alpha <= 1`, the bound is `<= W_y/(9(eps + eta))`.
  - The midpoint argument gives `W_y^2/8 <= 2w`. This is tight: the minimax
    error of a line fitted to `psi` over length `W` is exactly `W^2/16`.
  - `4(12 eta)^{1/4}/(9(eps + eta))` is maximized at `eta = eps/3`, with value
    `(sqrt 2/3) eps^{-3/4} = 0.4714 eps^{-3/4}`.
- **Comparison with the lower bound.** The ratios 1.46, 8.8 and 176 at
  `10^-6`, `10^-10` and `10^-16` reproduce (1.460, 8.837, 175.5). The
  crossover is at `eps = 10^-5.05`, so "from `10^-6` on" is right.

**Optional precision.** Step (d)2 says "`{x1, x2}` carries no bilinear term,
so it cannot satisfy (2.1)". This is immediate for `E_alpha` of
Definition 2.6. Theorem 3.6, however, allows any `E` satisfying (2.1). The
general reason is the recheck's: on a box with `y` at a face, `Gamma_C = 0`
while `d_x1 d_x2 > 0`.

### 3.2 Exact kink counts: all reproduce

`kink_audit.py` computes node bounds in exact `Q(sqrt 2)` arithmetic
(`b = sqrt 2 - 1`), by enumerating the vertices of the subdivision of each
box by `x = a` and the McCormick diagonal. It assumes no closed form. The
closed form `-w_y (a - l_x)(u_x - a)/w_x` agrees with the enumeration on 300
of 300 random boxes. For `a = 1/6`, `eps = 10^-2 ... 10^-8`:

| rule | my exact counts | note |
|---|---|---|
| `LP(1,.2)`, widest, ties to `x` | 13, 39, 167, 547, 1513, 4917, 19537 | same |
| `LP(1,.2)`, widest, ties to `y` | 15, 43, 173, 553, 1521, 4927 | same |
| `LP(1,.2)`, `x` only | 5, 9, 11, 13, 17, 19, 23 | same |
| product-score strong branching, `LP(1,.2)` point | 5, 9, 11, 13, 17, 19, 23 | same (labelled floating point) |
| `LP(1,0)`, `LP(1,.1)`, `INC` | 3 at every `eps` | same |
| `SCIPdef`, widest | 17, 47, 215, 215, 757, 4943, 15327 | same |
| bisection | 21, 61, 253, 765, 2045, 8189, 24573 | same |
| `a = 0.1999`, `LP(1,.2)`, `eps = 10^-4, 10^-6, 10^-8` | 3, 527, 19307 | same |

`k0(0.1999) = 5` checks by hand. **Optional:** the strong-branching row can
be labelled exact. It is the one row the recheck did not reproduce.

### 3.3 Proposition 5.4(d): tie rule and point-versus-coordinate test

**Correct.** With ties to `x`, `INC` takes 3 nodes for both incumbents and
both tests. With ties to `y` it takes:

- 7 nodes for `y* = 1/2` (both tests);
- 7 nodes for `y* = 0` with the coordinate test;
- 17, 49, 193, 513 and 1537 nodes for `y* = 0` with the point test.

The mechanism is as described: the child `[0,1] x [1/2,1]` does not contain
the incumbent. **Optional:** the remark gives no value of `a`. The counts come
from `a = 1/3` in `kink_exact_runs.log`, and I get identical counts at
`a = 1/6`. The count 7 also needs `eps` below `min(y*, 1-y*) a(1-a)`, which
holds on every tested `eps`.

## Commands run (targeted local checks only)

All runs used Python 3.13, NumPy 2.5.1 and SciPy 1.18, from
`research-20260928b/reviews/closing-audit-b/`, with BLAS/OpenMP threads
pinned to 1 and at most 4 processes at once.

```
python3 kink_audit.py > kink_audit.log                       # item 3, exact Q(sqrt2), ~80 s
python3 curved_audit.py > curved_audit.log                   # item 3, Prop. 3.14, ~3 s
python3 bls_shift_audit.py F > bls_shift_F.log               # item 2, shifted gaps, ~2 s
python3 bls_shift_audit.py T > bls_shift_T.log               # item 2, per-instance shift thresholds
python3 bls_shift_audit.py K > bls_count_K.log               # item 2, Theorem 4.1 counting example
python3 bls_shift_audit.py G > bls_exponent_G.log            # item 2, F9 ratios
python3 sparse_s1007_audit.py 1007 2714 > s1007_probe.log    # item 1, first spot check
python3 sparse_all_nodes.py 1007 C 4 s1007_all_C.jsonl       # C = 0..3, 4 processes, ~55 min, all 3195 nodes
python3 sparse_sweep_summary.py > sparse_sweep_summary.log   # item 1, sweep summary and 8-seed statistics
python3 sparse_s1007_audit.py 1000 1873 661 71 > s1000_spot.log
python3 cprime_audit.py > cprime_audit.log                   # item 1, c', constants, Conjecture 5.2
```

The first launch of the all-node sweep, with a tighter tolerance, was stopped
after about 60 nodes and restarted with tolerance `1e-6` (relative) and at
most 4000 iterations. The brackets are certified either way. No
project-wide checks were run, and CI was not inspected.
