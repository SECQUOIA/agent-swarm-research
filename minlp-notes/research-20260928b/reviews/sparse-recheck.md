# Recheck of the revised sparse-regression note

Reviewed file:
[`../bb-complexity/sparse-regression/phase-transition.md`](../bb-complexity/sparse-regression/phase-transition.md)
(revision of 2026-09-29, after
[`sparse-easy-review.md`](sparse-easy-review.md),
[`sparse-hard-review.md`](sparse-hard-review.md) and
[`pwe-verification.md`](pwe-verification.md)). Reviewer: fresh independent
reviewer (probability, high-dimensional statistics). I had not seen this
material before. Date: 2026-09-29. Scope: the five substantive revisions
listed in the brief. I did not edit the note and did not commit. My scripts
and logs are in [`sparse-recheck/`](sparse-recheck/). They import nothing
from the author's `code/` or from the earlier reviewers' scripts. The
instance generator mirrors the author's documented generator (I read it), and
the match was confirmed on 24 stored instances (`f(S*)` and `lam` agree
exactly).

## Verdict

| Revision | Verdict |
|---|---|
| (1) Theorems 4.3, 4.4: cliques of size `C(p,k)^{c'}` | **Correct.** I checked every step and every error term of the new proof. The new hypothesis `k -> inf` is genuinely used. The constant `c'` the proof gives is small (at most about 0.1; about 0.02 at `x = 1/2`). The Summary and Section 5 omit `k -> inf`. |
| (2) Section 6: Tables 6.1–6.3, seed 1007, `redecide_c1.py` | **Numbers correct; the explanation of the one failure is wrong.** All 39 table cells recount from the data. My own exact decisions agree with the note on 15 of 15 runs, including the seed-1007 failure and its node values. But at seed 1007 **four** forced-in nodes fail (null ranks 1, 5, 6 and 50), and every forced-in bound is within 2.8 of `f(S*)`. The failure is therefore largely the many-violator mechanism, not "a single unusually strong null feature" (F1). The Summary gives a stale C1 onset at `p = 1600` (F2). |
| (3) Theorem 3.1 with total-energy noise `sigma = gamma/sqrt n` | **Correct.** `sigma` enters the proof of Theorem 3.1 only as the note says. Two points of precision: the sentence mixes in Theorem 3.2(b); and with `gamma` fixed, (A) forces `k -> inf`, so the `gamma^2/b^2` term lies inside the `o(1)` (F3). |
| (4) Remark 3.5 and Section 7 (PWE) | **Accurate, respectful, and consistent with the verification report, with four fixable slips.** Items 2–3 of Remark 3.5 write `M_S` for PWE's `M`, which is `M_S^{-1}` in the note's notation. "Approaching 0.123 from below" is contradicted by the quoted 0.153. The total-energy bullet drops the report's caveat. One parenthesis is ambiguous (F4). I reproduced the note's own PWE claim: 19 of 20 instances. |
| (5) Conjecture 5.2 and the Section 5 scalings | **Correct.** The conjecture is now precise. For fixed `gamma` its range of `n` is nonempty only when `delta < (2 - 3 gamma)/(2 - gamma)`, which it should say (F5). All Section 5 scalings check. |

## 1. Hard side: the new proof of Theorems 4.3 and 4.4

I checked the proof in Section 4.3 line by line. Error terms by step:

- **Step 1.** `d(q||rho) = -log(1-rho) + O(q log(1/q))` uniformly on compact
  subsets of `(0,1)`, and `(2/n) log(1/delta) = (2/n) log k -> 0`. Because
  `d(q||.)` is increasing, `rho*` is eventually squeezed between
  `1 - e^{-(x ± eps)}`, so `-log(1 - rho*) -> x`. Correct.
- **Step 2.** At `mu -> 1` and `theta, c' -> 0`, the left side of (*) tends to
  `2x`, and `2x > e^x - 1` on `(0, x0)`. First choose `mu, theta`, then choose
  `c'` below both the (*) bound and `(1-mu) theta`. `eta_0 > 0` is equivalent
  to (*). Correct.
- **Step 3.** The binomial count gives the failure probability `e^{-M/4}`
  through (G4) with mean `2M`. From `k log(p/k) <= log C(p,k) <= k log(ep/k)`
  and `k/n -> 0`, we get `log(p/k) -> inf` and
  `log C(p,k) = k log(p/k)(1 + O(1/log(p/k)))`. The quantile satisfies
  `t_M^2 = 2 log(p/M) - log log(p/M) - log(4 pi) + o(1)`, and
  `p/M ≈ (p/k)^{1-theta} -> inf`, so the relative error is
  `O(log log(p/k)/log(p/k))`. The result
  `s_U >= (1+mu)(1-theta) x n (1+o(1))` follows. Correct.
- **Step 4.** Both elementary Gilbert–Varshamov (GV) inequalities hold. I
  checked `C(M,k) >= (M/k)^k` and
  `sum_{d<m} C(k,d) C(M-k,d) <= m 2^k (eM/m)^m` on 125 grid points each, with
  no violation. The monotonicity of `(eM/d)^d` for `d < M` is right. The
  losses are `k log 2`, `log m`, `m(1 + log(1/mu))`, and `theta log(p/k)` from
  rounding `m <= mu k + 1`. The last is `o(k log(p/k))` only because
  `k -> inf`, so the new hypothesis is genuinely used here (and in
  `delta = 1/k -> 0`). Correct. The `o(1)` converges slowly. The exact GV
  exponent divided by `(1-mu) theta k log(p/k)` is about 0, 0.32, 0.82 and
  1.03 at `log(p/k) = 10, 30, 100, 1000` (`k = 100`, `mu = 0.8`,
  `theta = 0.1`; `hard_check.log`).
- **Step 5.** Given `(y, c)`, the columns of `X^perp` are iid
  `N(0, I - yhat yhat')`, and `W` and `C'` are `(y, c)`-measurable. So each
  pair statistic is exactly `chi^2_{n-1}`, and the union bound applies. A
  Monte Carlo with data-dependent `W` (top `M`) and a greedy code gave 2400
  pair statistics with mean 59.17 against 59, and a Kolmogorov–Smirnov
  p-value of 0.14. The step
  `t = 2 log|C'| + log k = c' x n (1+o(1))` uses `log k = o(n)`. Correct.
- **Step 6.** The Lemma 4.2 bound decreases in `s_U`, and `2 lam = o(n)`,
  which gives `g(mid) <= OPT - (eta_0 - o(1)) ||y||^2`. The failure
  probability is `2 delta + e^{-M/4} + o(1) -> 0`. Correct.
- **Theorem 4.4.** Conditioning on `(X_{S*}, w)`, using `p - k` candidates,
  `OPT >= (e^{-x} - o(1)) n sigma^2` from Lemma 4.1(b) together with
  `chi^2_{n-k}`, and `||y||^2 = n(sigma^2 + ||beta*||^2)(1+o(1))` give the
  condition `1 + kappa_s < e^{-x}(1 + (1+mu)(1-theta)x/B)`, which tends to
  `e^{-x}(1+2x)`. Correct.

The constants check: `x0 = 1.2564312086`, `2/x0 = 1.5918`, and
`max K = K(1/2) = 0.2131`. `K/(e^x - 1)` is 0.816, 0.328 and 0.060 at
`x = 0.1, 0.5, 1`, and `sqrt(K/x) < 1`.

**How large is `c'`?** The largest `c'` admitted by Steps 2–6 (grid search,
`hard_check.log`) is 0.106, 0.059, 0.022, 0.0067, 0.0020 and `9e-5` at
`x = 0.05, 0.2, 0.5, 0.8, 1.0, 1.2`. It tends to 0 as `x -> x0`. In the
planted case at `kappa_s = K(x)/2` it is 4–5 times smaller for
`x <= 1.2`. The statement
"`C(p,k)^{c'}` for some `c' > 0`" is correct. A reader would benefit from
knowing that the proof gives only a small constant.

**Minor points on the hard side.**

- The Summary ("provided `x < x0`, `k/n -> 0` and `lam = o(n)`") and the
  Section 5 hard-side sentence omit `k -> inf`, which Theorem 4.3 now assumes.
  The hypothesis is automatic for `k = p^gamma`.
- In the remark after the proof, the fixed-`R` clique `exp(k e(mu,R)/2)` is
  correct but weaker than the argument gives. With fixed `R`,
  `t = O(k) = o(n)` and `B -> 1`, so the whole GV code works, giving
  `exp(k e(mu,R)(1 - o(1)))`.
- Section 4.4, single conflicting pair. For `|C'| = 2`, no GV bound is needed:
  two disjoint `k`-subsets of `W` exist once `M >= 2k`. With `M = 2k`, my
  evaluation certifies a pair at `p = 10^{5.5}` also for
  `lam = sqrt(n log p)` (`k = 2`, `alpha = 2048`), and at `p = 10^5` for
  `lam = 0`. So the quoted `10^{5.5}`/`10^6` values are grid- and
  GV-specific, as the note partly says. At such small `M`, the event
  "at least `M` exceedances" fails with probability up to `e^{-M/4}` (0.37 at
  `M = 4`, 0.14 at `M = 8`). This probability is not included in "certified".
  None of this changes the conclusion that the proof is vacuous at practical
  sizes.

## 2. Section 6: tables, the seed-1007 failure, and the re-decision code

**Tables.** `tables_check.py` recounts Tables 6.1–6.3 from the stored run
files. It uses its own deduplication and replaces the 31 capped runs by
`c1_redecided.jsonl`. It compares runs, the PWE certificate, the witness, C1,
mean `tau^2` and mean root gap. All 39 printed cells match.

**Own exact decisions** (`redecide_sample.py`, `rc_common.py`). My decider
uses its own closed-form `L(a)` on all `p` single fixings, over a growing pool
of dual vectors. Node relaxations are solved by column generation on a cvxpy
perspective SOCP (Clarabel), a model independent of the author's hand-built
one. Decisions are certified only by closed forms:

- "fail" means a feasible `z` with `g(z) < f(S*)(1 - 1e-7)`;
- "C1" means every single-fixing lower bound is `>= f(S*)(1 + 1e-9)`.

| run | note | mine |
|---|---|---|
| `p = 3200`, `sqrt n`, seeds 1007 / 1001 / 1004 (redecided) | fail / C1 / C1 | fail / C1 / C1 |
| `p = 1600`, `alpha = 1.25`, seeds 1004, 1006 (redecided) | C1, C1 | C1, C1 |
| `p = 1600`, `alpha = 1.5`, seed 1003 (redecided); seed 1004 (exact) | C1; fail | C1; fail |
| `p = 1600`, `alpha = 1.25`, seed 1002 (exact) | fail | fail |
| `p = 800`, `sqrt n`, seed 1002 (lowest `tau^2`, redecided) | C1 | C1 |
| `p = 400`, `alpha = 1.25`, seed 1005 (redecided) | C1 | C1 |
| Table 6.2 `alpha = 1`, seeds 1001 / 1004 (exact) | C1 / fail | C1 / fail |
| `p = 200`, `alpha = 1.25`, seeds 1001 / 1005 (exact) | fail / C1 | fail / C1 |
| `p = 100`, `alpha = 1`, seed 1007 (exact) | fail | fail |

The runs agree 15 of 15, and no node was left undecided. cvxpy sometimes
warned "solution may be inaccurate" on restricted solves. This does not
affect the decisions, which rest on the closed-form bounds.

**Seed 1007 numbers** (`p3200_s1007.log`, `s1007_socp.log`). All
reproduce:

- `f(S*) = 82.6998`;
- forced-in `j = 991`: 80.2862;
- forced-in `j = 2714`: 82.5761.

Column generation to convergence and a full, unrestricted dual SOCP (a
different formulation) agree to 4 digits. Also reproduced:
`|a_991| = 4.758 ||r||` (probability 0.0062 among 3195 nulls),
`a_991^2/(n + lam) = 6.887`, `m0^2/lam = 7.163` and `tau^2 = 1.962`. For
seeds 1000 and 1003 I get root gaps 5.678 and 2.920, and forced-in margins
5.994, 8.470, 8.701 and 6.838, 9.221, 9.255 (the note prints 9.26 for the
last).

**F1 (the explanation of the failure is wrong).** The note says the failure
"comes from a single unusually strong null feature, not from the asymptotic
mechanism". It also says "this is the last term of Heuristic 3.8, not the
many-violator mechanism behind Corollary 3.4". The Summary says it is "due to
a few unusually strong null features". Solving every forced-in node that the
dual pool cannot certify (`count_failures.py`, 504 exact solves) shows that
at seed 1007 exactly **four** forced-in nodes fail:

| null rank by `abs(a_j)` | `j` | `abs(a_j)/norm(r)` | node value minus `f(S*)` |
|---:|---:|---:|---:|
| 1 | 991 | 4.76 | −2.414 |
| 5 | 1453 | 3.21 | −0.454 |
| 6 | 2714 | 3.20 | −0.124 |
| 50 | 2119 | 2.49 | −0.023 |

The null of rank 2 passes by only +0.024. The nulls of ranks 5, 6 and 50 are
ordinary: rank 50 of 3195 corresponds to `abs(Z) ≈ 2.5`. The decisive fact is
the margin of *every* forced-in node (`s1007_margins.log`). With a price
`m0^2/lam` of 7.16 at seed 1007 and 8.94 at seed 1000, the margins are:

| null rank | 1 | 10 | 100 | 500 | median | weakest |
|---|---:|---:|---:|---:|---:|---:|
| seed 1007 | −2.41 | 0.80 | 2.05 | 1.93 | 2.76 | 2.75 |
| seed 1000 | 5.99 | 6.03 | 7.41 | 8.32 | 8.68 | 8.70 |

At seed 1007, forcing in even the weakest null (own fit 0) costs only 2.75 of
the 7.16 price. The relaxation recovers about 4.4 by spreading the freed
budget over the violators. At seed 1000 it recovers only 0.24. Seed 1007 also
has the most violators (521) and the largest root gap (9.94) of the eight
runs; the others have 203–326 violators and root gaps 2.9–5.7. So the failure
combines the many-violator (budget-spreading) mechanism, which is strongly
active here, with the own fit of a few moderately strong nulls. It is not yet
the asymptotic regime, in which the violators' gain alone exceeds the price
for almost every null. But it is not a single-feature fluke either.

Suggested text for Section 6.3, adaptable to the remark after Corollary 3.4
and to the Summary:

> "At seed 1007 the realized `tau^2 = 1.96` is the lowest of the eight runs.
> It has the most violators (521) and the largest root gap (9.9). Every
> forced-in node is within 2.8 of `f(S*)` (against 5.9–8.7 at seed 1000), so
> the violators recover about 60% of the budget price `m0^2/lam = 7.16` for
> any forced-in null. Four nulls (ranks 1, 5, 6 and 50 by `abs(a_j)`) then
> fail, the strongest (`j = 991`) by 2.41. This is the finite-size form of the
> many-violator balance of Heuristic 3.8, including its own-fit term. It is
> not yet the asymptotic regime of Corollary 3.4, where the violators alone
> outweigh the price for almost every null."

The sentence "So at `p/sqrt n ≈ 290` ... the asymptotic Corollary 3.4 is still
not visible" should be softened accordingly: at seed 1007 its mechanism is
already visible.

**F2 (stale numbers).**

- The Summary says C1 held in every run from `alpha ≈` "2.0 (`p = 1600`)" on.
  Table 6.1 and Section 6.1 give 1.75 (8 of 8 at `alpha = 1.75` and 2.0).
- Heuristic 3.8 says that at `lam = sqrt n`, `p = 3200`, the additive gain
  "gives 14–31, while the exact root gap is 3–6". This holds for seven seeds.
  At seed 1007 the values are 70.3 and 9.9 (`p3200_satgain.log`).
- Section 6.3 says the price of forcing a feature in "is about
  `lam b^2 = sqrt n ≈ 11`". The realized price `m0^2/lam` at `p = 3200` is
  7.2–8.9. The nominal value is fine if it is labeled nominal.

**`redecide_c1.py` / `decide_c1_exact` (code review).** The procedure is
sound: lower bounds are weak-duality values on the full node, and failures
are feasible restricted primal values. Two latent issues were not triggered
in the stored runs:

1. If `max_solves` (5000) is exhausted, the returned status stays `'C1'`.
   The stored runs used at most 109 solves.
2. A node that converges within tolerance to `f(S*)` (`'passtol'`) counts as
   a pass. That establishes non-strict C1, not uniqueness of `S*`. All 31
   stored runs have empty `notes`, so every "C1" is strict.

The stored failing node for seed 1007 is `j = 2714`. The note headlines
`j = 991`. Both are valid failures.

## 3. Theorem 3.1 with total-energy noise

I went through every occurrence of `sigma` in the proof of Theorem 3.1:
Step 1 of Section 3.3, and Sections 3.4(a) and (b).

- `||r||^2 = ||v||^2 + 2 sigma v'M^{-1}w + sigma^2 ||M^{-1}w||^2`. Here
  `||v||^2` has no `sigma`, the last term is `n sigma^2 (1 + O(theta_n))` by
  E2 (relative error, any `sigma`), and the cross term is bounded by the
  scale-free inequality
  `2 sigma ||v|| sqrt(2 log p) <= sqrt(2 log p/n)(n sigma^2 + ||v||^2)`. So
  `||r||^2 = (1 + O(theta_n)) omega_lam^2` for every `sigma >= 0`, and the
  lower bound used in 3.1(b) holds as well.
- The leave-one-out term `(sigma/b) sqrt(log p/n)` in `eta_1` only shrinks as
  `sigma -> 0`.
- The null correlations are exactly `N(0, ||r||^2)` given `(X_S, w)`, and the
  event probabilities do not depend on `sigma`.

So Theorem 3.1(a)–(c) hold with `sigma = gamma/sqrt n`. With `lam = sqrt n`,
`tau_lam^2 = (1 + O(n^{-1/2})) n b^2/(gamma^2 + k b^2)`, which gives the
stated `n >= (2+o(1))(k + gamma^2/b^2) log p`. A simulation with the exact
conditional law of the null maximum (`total_energy.py`; `k = 20`;
`p = 10^6, 10^12`; far outside (A)) gives `tau_hat^2/tau_lam^2` between 0.93
and 0.99. The exactness probability is 0.00–0.03, 0.67–0.75 and 0.99–1.00 at
`c = 0.8, 1, 1.25` in `n = c · 2(k + gamma^2/b^2) log p`, both for
`gamma^2/b^2 = 0.25` and for `gamma^2/b^2 = k`.

**F3 (precision).**

1. The sentence "Theorem 3.1 assumes fixed `sigma`. Its proof uses `sigma`
   only through ... and the lower bound on `tau'` in Theorem 3.2(b)" mixes
   the two theorems: the proof of Theorem 3.1 does not use Theorem 3.2(b).
   Say "the proofs of Theorems 3.1 and 3.2", or drop the 3.2(b) item. If the
   extension is meant to cover Theorem 3.2 too, note that the explicit ridge
   of Theorem 3.2(c), `lam = (sigma/b) sqrt(T n) = (gamma/b) sqrt T`, falls
   below `sqrt n` and so leaves (A). `lam = sqrt n` works instead, because
   then `tau_lam^2 = (1 + o(1)) n/k`.
2. With `gamma`, `b` fixed, (A) (`n >= log^6 p`) together with
   `n ≈ 2(k + gamma^2/b^2) log p` forces `k -> inf`. The `gamma^2/b^2` term is
   then `o(k)`, so "identifies the sharp constant `c0 = 2`" really concerns the
   `k` term only. The proof also allows `gamma^2 = O(k b^2)`: then
   `sigma = O(sqrt(k/n)) -> 0` and every error term still vanishes. The
   simulation above shows the coefficient 2 on `gamma^2` at finite size. The
   note should either allow `gamma` to grow like this, or say that for fixed
   `gamma` the noise term lies inside the `o(1)`.
3. "Has not been independently checked" can now cite this recheck.

## 4. Remark 3.5 and Section 7 (PWE)

I compared each statement with [`pwe-verification.md`](pwe-verification.md):

- the model, the statement of Theorem 2 and the page numbers;
- the four-step `n -> inf` argument and the limit 0.123;
- the normalization mismatch, with Lemma 1 true under `1/(rho n)` and Lemma 2
  true under `1/rho`;
- the two incorrect steps: `sigma_max(M) <= 1/rho` and the variance
  `4 gamma^2/rho^2`;
- scale invariance;
- the literature status: Crossref, thesis Theorem 12 on p. 180 with the proof
  on pp. 199–200, Dong's Theorem 3, and Bertsimas–Pauphilet–Van Parys;
- the per-entry repair and its probability.

All of these match. The tone is factual. The note states plainly that the
theorem is false as stated and credits what survives: Corollary 2, the
algorithms, and the total-energy reading. I consider it respectful.
"Hidden by two incorrect steps" follows the report's wording; "masked" would
sound more neutral, but this is optional.

I reproduced the note's own evidence with independent code (`pwe_recheck.py`,
same seeds `700+s`). In 19 of 20 instances, strict C1 certifies that `S*` is
the unique optimum, and the root value is certified below `f(S*)`. The
relative gaps range from `4.2e-6` to `1.4e-3`. The exception is `n = 5000`,
seed 3, where the certificate holds and the root is exact. The limit
`(1 - 2 Phibar(2))^45` is 0.1230. All of this is as stated.

**F4 (slips).**

1. **Notation.** In "Why the statement is false", items 2–3 write
   `X_S'M_S y = rho beta^S` and `a_l = x_l'M_S y`. In the note's notation
   (Section 1.2), `M_S = I + X_S X_S'/lam`, so these must read `M_S^{-1}`. The
   `M` of "Where the proof goes wrong" is PWE's `(I + X_S X_S'/rho)^{-1}`.
   Add "(PWE's `M` is our `M_S^{-1}`)" there and in Section 7.
2. "Its Monte Carlo exactness probabilities are 0.080, 0.093, 0.113 and 0.153
   ..., approaching 0.123 from below." The last value is above 0.123. The
   report's "from below" refers to the conditional estimates 0.052, 0.081,
   0.104 and 0.114. Quote those, or say "consistent with the limit 0.123 (the
   last 95% interval, [0.096, 0.211], contains it)".
3. **Total-energy bullet.** The report checked the repair "at the level of the
   displayed steps of Appendix 7.1, not every constant". Keep that qualifier
   after "PWE's argument goes through". The Monte Carlo figure "0.99 or more
   from `n ≈ 5 (gamma^2 + ||w*||^2)/w_min^2 log d`" is for `d = 50`, `k = 5`
   only; say so.
4. "finds the relaxation strictly inexact in 13 of 16 instances (8 of which
   regenerate the easy-side review's instances)". The "8" refers to the 16
   instances, not to the 13. Suggested: "(8 of the 16 regenerate ...)". In
   Section 7, "the asymptotic regime (A)" should read "(A) with `sigma`
   replaced by `gamma/sqrt n`", since (A) fixes `sigma`.

## 5. Conjecture 5.2 and the Section 5 scalings

- **Section 5 scalings.** For `k = p^gamma`:
  - `log(p/sqrt n) = (1 - gamma/2 + o(1)) log p`, so the C1 threshold is
    `alpha = 2 - gamma`;
  - `x = 2(1-gamma)/alpha`, so the hard-side condition is
    `alpha > 1.5918(1 - gamma)`;
  - at fixed `b/sigma`, the total SNR diverges;
  - `n_IT/(k log p) ≈ 2(1-gamma)/(gamma log p)`: for `gamma = 1/2`, 0.167,
    0.094 and 0.051 at `p = 10^4, 10^8, 10^16`, against the first-order
    values 0.217, 0.109 and 0.054;
  - `alpha_IT ≈ 0.2` at the scout's sizes: 0.24 at `k = 10` and 0.17 at
    `k = 20`.

  All correct (`conj52.log`).
- **Conjecture 5.2.** The statement is now precise (`lam` range, `eps = 0`,
  lower limit `(1+delta)k`, `gamma < 2/3`). The "what is missing" bullets are
  correct:
  - `x >= (1 - o(1)) log(1 + k b^2/sigma^2) -> inf`;
  - `k/n >= k/n_IT -> gamma/(2(1-gamma))`;
  - the needed explained fraction is `1 - O(1/kappa_s)`, against
    `1 - 1/(1 + (1+mu)x)` for the construction;
  - (b) rather than (a) is the natural criterion.

**F5.** "(a nonempty range for large `p`, because `n_IT/k -> 2(1-gamma)/gamma > 1`)"
is true only for `delta < (2 - 3 gamma)/(2 - gamma)`. The bound is 1/3 at
`gamma = 1/2`, 1/7 at `gamma = 0.6`, and tends to 0 as `gamma -> 2/3`. For
larger `delta` the conjecture is vacuous, not false. Add the condition, or
quantify as "for every sufficiently small `delta > 0`". The limit is
approached slowly: `n_IT/k` is 1.54, 1.74 and 1.86 at `p = 10^4, 10^8, 10^16`
for `gamma = 1/2`, `b/sigma = 2`.

## Requested changes

1. **(F1, needed)** Rewrite the explanation of the seed-1007 failure in
   Section 6.3, in the remark after Corollary 3.4 ("a single unusually strong
   null feature"), and in the Summary ("a few unusually strong null
   features"). Four nodes fail (ranks 1, 5, 6 and 50), and every forced-in
   bound is within 2.8 of `f(S*)`. See the suggested text in Section 2.
   Soften "Corollary 3.4 is still not visible".
2. **(F2)** Summary: change "2.0 (`p = 1600`)" to "1.75". Heuristic 3.8:
   "14–31 ... 3–6" should mention seed 1007 (70 and 9.9). Label
   `lam b^2 ≈ 11` as the nominal price, or give the realized 7.2–8.9.
3. **(F4)** Remark 3.5: `M_S` becomes `M_S^{-1}` in items 2–3, and state that
   PWE's `M` is our `M_S^{-1}`. Fix "from below"; keep the report's caveat on
   the total-energy repair; attach `d = 50`, `k = 5` to the 0.99 figure;
   disambiguate "8 of which". Section 7: "(A) with `sigma = gamma/sqrt n`".
4. **(F3)** Extension of Theorem 3.1: do not cite Theorem 3.2(b) as part of
   Theorem 3.1's proof. Say that for fixed `gamma` the `gamma^2/b^2` term lies
   inside the `o(1)`, or allow `gamma^2 = O(k b^2)`, which the proof
   supports.
5. **(F5)** Conjecture 5.2: require `delta < (2 - 3 gamma)/(2 - gamma)`.
6. **(Minor)** Add `k -> inf` to the hard-side hypotheses in the Summary and
   Section 5. Optionally report that the proof's `c'` is small (at most about
   0.1). Optionally drop the `/2` in the fixed-`R` remark. Optionally note the
   `e^{-M/4}` term and the GV-free pair in Section 4.4.
7. **(Optional)** `redecide_c1.py`: return `'undecided'` when `max_solves` is
   exhausted, and report `'passtol'` nodes separately from strict passes.

## Not checked

- Revisions outside the brief: the attributions (item 2), the Theorem 3.2
  margin (item 3), the second-order formulas of Heuristic 3.8 and their fit
  (item 6), and Section 6.5 and Tables 6.4–6.6.
- The PWE paper itself. I relied on the verification report for the paper's
  text and page numbers.
- Section 4.4's full grid. I evaluated only the single-pair points quoted in
  the revision.

## Commands run (targeted local checks only; no project-wide checks; CI not consulted)

From `research-20260928b/reviews/sparse-recheck/`:

```
python3 test_rc.py                      > test_rc.log        # solver self-tests; generator matches 24 stored instances
python3 p3200_nodes.py 1007             > p3200_s1007.log
python3 p3200_nodes.py 1000 1003        > p3200_s1000_1003.log
python3 redecide_sample.py redecide_sample.jsonl 4   (log: redecide_sample.log, redecide_sample.clean.log)
python3 count_failures.py 3200 5 121 sqrtn 1007      > count_failures_p3200_s1007.log
python3 s1007_margins.py                > s1007_margins.log
python3 s1007_socp.py                   > s1007_socp.log
python3 p3200_satgain.py                > p3200_satgain.log
python3 tables_check.py                 > tables_check.log
python3 pwe_recheck.py                  > pwe_recheck.log
python3 hard_check.py                   > hard_check.log
python3 total_energy.py                 > total_energy.log
python3 conj52.py                       > conj52.log
```

CPU. All scripts pin the BLAS/OpenMP thread counts to 1, and at most four
worker processes ran at once. There was one exception. The first two
`p3200_nodes.py` runs and the first two `test_rc.py` runs imported NumPy
before pinning the threads. They briefly used multithreaded BLAS, above the
6-core budget: about 10–20 s of wall time for each `p3200_nodes.py` run and
about 1 s for each `test_rc.py` run. Both scripts were fixed before any
further run.
