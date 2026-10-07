# Verification of the PWE discrepancy (Pilanci–Wainwright–El Ghaoui 2015, Theorem 2)

Scope: the claim in [`sparse-easy-review.md`](sparse-easy-review.md), Section 4
("The PWE discrepancy"), and the scripts in [`sparse-easy/`](sparse-easy/)
(`pwe_counterexample.py`, `pwe_check.py`), that Theorem 2 of Pilanci,
Wainwright and El Ghaoui (PWE) is false and that the error sits in Appendix 7.1.
Verifier: independent of the note author and of that reviewer. Date:
2026-09-29. My code and outputs are in [`pwe-verify/`](pwe-verify/). I did not
edit any other file and did not commit.

## Verdict

**Theorem 2 of PWE is false as stated, not merely badly proved.** It fails for
every choice of the constants `c0, c1 > 0`, even if they were allowed to depend
on the instance. The reviewer's reading is correct in substance. The
reviewer's numbers reproduce to the printed precision, except for one relative
gap (`8.66e-7` against `8.62e-7`).

- **The model is not misread.** PWE state the noise model explicitly as
  per-entry `N(0, gamma^2)`, with `X` iid `N(0,1)` and `rho = sqrt n`.
- **The theorem fails for a simple reason.** Fix `d > k`, `w*` and
  `gamma > 0`, and let `n -> inf`. The hypothesis
  `n > c0 (gamma^2 + ||w*_S||^2)/w_min^2 log d` then holds for all large `n`,
  and the claimed probability `1 - 2e^{-c1 n}` tends to 1. But the true
  probability that the relaxation is exact tends to
  `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`. This follows from PWE's own
  Corollary 2 (Section 3 below). For `d = 50`, `k = 5`, `|w*_j| = 1` and
  `gamma = 0.5`, the limit is 0.123. My Monte Carlo decides exactness exactly
  for each instance. With 150 instances per `n`, it gives 0.080, 0.093, 0.113
  and 0.153 for `n` = 500, 2000, 10 000 and 50 000, which corresponds to PWE's
  `c0` from 24 to 2434. The lower-variance conditional estimates are 0.052,
  0.081, 0.104 and 0.114.
- **All three proof defects the reviewer names are real (Section 2).** The
  precise diagnosis is that the two lemmas are proved for different
  normalizations of `U_j`:
  - Under the normalization PWE define, `U_j = X_j'My/(rho n)`, Lemma 1 is
    true but Lemma 2 (34a) is false.
  - Under the normalization the proofs use, `U_j = X_j'My/rho`, Lemma 2 holds
    but Lemma 1 is false.

  Two incorrect steps in the proof of Lemma 1 hide this mismatch:
  `sigma_max(M) <= 1/rho`, and "variance at most `4 gamma^2/rho^2`".
- **The errors are not typos with a correct intended statement under the
  stated model.** No reading of the stated model can make the proof work,
  because the conclusion is false. There is one consistent reading under which
  the published proof goes through almost line by line: noise of **total**
  energy `gamma^2` (iid `N(0, gamma^2/n)` entries), with `U_j = X_j'My/rho` and
  `sigma_max(M) <= 1`. Under that reading the printed variance bound
  `4 gamma^2/rho^2` is valid. I checked this repair at the level of
  the displayed steps of Appendix 7.1, not every constant. Even then, the proof gives the failure
  probability `c exp(-c' n w_min^2/(gamma^2 + ||w*_S||^2))`, not
  `2e^{-c1 n}`. The two agree only when `k` and `gamma/w_min` stay bounded.
- **Adding an SNR assumption does not restore the theorem as stated.** The
  assumption `w_min^2/gamma^2 >= C log d`, proposed by the reviewer and now in
  the note, does not restore the per-entry noise version with its probability
  `1 - 2e^{-c1 n}`. For fixed `d, w*, gamma`, the exactness probability still
  tends to `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`. What the repaired proof
  gives is a failure probability of order
  `d exp(-c w_min^2/gamma^2) + exp(-c' n w_min^2/||w*_S||^2 + log d)`. This
  bound does not decay with `n`.
- **Literature.** I found no erratum. Crossref lists no update to
  DOI 10.1007/s10107-015-0894-1. Pilanci's 2016 PhD thesis repeats the theorem
  and proof unchanged. Dong (arXiv 1603.04572) and Bertsimas–Pauphilet–Van Parys
  (arXiv 1902.06547) cite the theorem as valid. None of the follow-ups I could
  read notes the problem. My search was limited (Section 5).

## 1. Source statements and formulas

I found no arXiv version of PWE (arXiv API author and title queries returned
none). I read the published version from the author-hosted PDF
`http://www.eecs.berkeley.edu/~elghaoui/Pubs/SparseLearningBoolean.pdf`
(Springer typesetting, Math. Program., Ser. B (2015) 151:63–87,
DOI 10.1007/s10107-015-0894-1, "Received: 4 November 2014 / Accepted:
17 February 2015"). I also read Pilanci's thesis (UCB/EECS-2016-147). Page
numbers below are journal pages. I checked the formulas against the page
images, not only the text extraction.

- **Problem (3), p. 65:**
  `P* := min_{w in R^d, ||w||_0 <= k} (1/2) sum_{i=1}^n (<x_i, w> - y_i)^2 + (1/2) rho ||w||_2^2`.
- **Section 3, pp. 69–70:** The authors invoke strong convexity to assert
  uniqueness for the cardinality-constrained problem (1), denote its solution
  by `w* in R^d`, and use `S` for the support of `w*`. In Section 3.1, `w*` instead denotes
  the true regression vector. The overloading does not matter below, because the
  optimal support equals the true support with probability tending to 1.
- **Relaxation (19) and matrix (20), p. 71:**
  `P_IR = min_{u in [0,1]^d, sum u_j <= k} y'((1/rho) X D(u) X' + I_n)^{-1} y`
  and `M := (I_n + rho^{-1} X_S X_S')^{-1}`.
  - Equations (13) and (19) drop the factor 1/2 of (3). This does not affect
    exactness.
- **Corollary 2, p. 71:** The claimed exactness criterion is `P_IR = P*`
  if and only if a scalar `lambda in R_+` separates the two sets of correlations:
  `|X_j' M y| > lambda` for every `j in S`, and
  `|X_j' M y| <= lambda` for every `j notin S`.
- **Model, Section 3.1, p. 72:** The design is `X in R^{n x d}` with
  independent `N(0,1)` entries. Responses follow `y = Xw* + eps`, with
  `eps in R^n` having independent `N(0, gamma^2)` entries. The vector `w*`
  is assumed `k`-sparse; its nonzero magnitudes scale as `1/sqrt k`.
- **Theorem 2, p. 72:** The asserted implication uses the sample-size condition
  `n > c0 (gamma^2 + ||w*_S||_2^2)/w_min^2 log d` and the choice
  `rho = sqrt n`. It claims integrality of the interval relaxation with probability
  at least `1 - 2e^{-c1 n}`, yielding `P_IR = P*`.
  - Neither constant is specified in the theorem. On p. 82, the proof requires
    `c0` to be large enough. Dong likewise states existence of constants `c0`
    and `c1`, without giving their values.
- **Appendix 7.1, p. 81:** The normalization is
  `U_j := X_j'My/(rho n)`, with the decomposition
  `U_j = X_j'MX_S w*_S/(rho n) [=: A_j] + X_j'M eps/(rho n) [=: B_j]`.
  - The proof targets condition (32): `min_{j in S}|U_j| > lambda` and
    `max_{j in S^c}|U_j| < lambda`.
- **Lemma 1 (33), p. 81:**
  `P[max_{j=1..d} |B_j| >= t] <= c1 exp(-c2 n t^2/gamma^2 + log d)`.
- **Lemma 2 (34a), (34b), p. 82:**
  - (34a): `P[min_{j in S}|A_j| < w_min/4] <= c1 exp(-c2 n w_min^2/||w*_S||^2 + log(2k))`.
  - (34b): `P[max_{j in S^c}|A_j| >= w_min/16] <= c3 exp(-c4 n w_min^2/||w*_S||^2 + log(d-k))`.
- **Assembly, p. 82:** Lemma 1 is applied at `t = w_min/16` to obtain
  the high-probability bound `max_j |B_j| <= w_min/16`; the proof then chooses
  `lambda = 5 w_min/32`.
- **Proof of Lemma 1, p. 82 (the disputed step):** Using definition (20) of `M`,
  the authors assert `sigma_max(M) <= rho^{-1}`. Conditional on `E`, they use
  `||MX_j||_2 <= ||X_j||_2 <= 2 sqrt n`, treat `X_j'M eps/rho` as Gaussian,
  and bound its variance by `4 gamma^2/rho^2`. Their resulting tail bound, conditional on `E`, is
  `P[|B_j| > t | E] <= 2e^{-rho^2 t^2/(32 gamma^2)}`.
- **Proof of Lemma 2, pp. 83–85 (the normalization it uses):**
  - p. 83: The proof uses `(1/rho) X_S'MX_S = X_S'(rho I_n + X_S X_S')^{-1} X_S`
    to establish `(1/rho) X_S'MX_S w*_S ≈ w*_S`, then takes `eps = 3/4`.
  - p. 84: For each `j in S^c`, it writes `A_j = (1/rho) X_{S^c}' M X_S w*_S = ...`.
  - p. 85: It treats `A_j` as conditionally Gaussian and gives the variance bound
    `(4/rho^2)||w*_S||_2^2`.

## 2. The proof of Theorem 2: what is wrong, exactly

Let `a_j = X_j'My`. Then `U_j = a_j/(rho n)` as defined on p. 81.

1. **`sigma_max(M) <= 1/rho` is false.** `M = (I + X_S X_S'/rho)^{-1}` has
   eigenvalue 1 on the orthogonal complement of `range(X_S)`, with
   multiplicity `n - k`. On `range(X_S)` its eigenvalues are
   `1/(1 + s_i^2/rho)`, where the `s_i` are the singular values of `X_S`.
   Numerically, `lambda_max(M) = 1.000000000000` with multiplicity 95
   (`n = 100`) and 495 (`n = 500`), against `1/rho = 0.1` and 0.045
   (`pwe_lemmas.out`). The next inequality, `||MX_j|| <= ||X_j||`, uses only
   `sigma_max(M) <= 1` and is correct. The bound `1/rho` is true for
   `(rho I + X_S X_S')^{-1} = M/rho`, which is probably the source of the slip.
2. **The variance claim is false for the variable named.** Conditional on
   `X`, `X_j'M eps/rho ~ N(0, gamma^2 ||MX_j||^2/rho^2)`. On `E`, the variance
   is at most `4 n gamma^2/rho^2 = 4 gamma^2` at `rho = sqrt n`, not
   `4 gamma^2/rho^2`. Numerically, the median over instances of the largest
   conditional variance is 0.28, 0.26 and 0.25 at `n = 500, 5000, 50000` (it
   tends to `gamma^2 = 0.25`), while the printed bound is
   `2e-3` to `2e-5` (`pwe_lemmas.out`). The printed value is what one gets from
   the false bound in step 1: `||MX_j|| <= 2 sqrt n/rho` gives
   `4 n gamma^2/rho^4 = 4 gamma^2/rho^2` at `rho^2 = n`. It is also a valid
   bound if the per-entry noise variance is `gamma^2/n`.
3. **The two lemmas use different normalizations.** Lemma 1's statement and
   Lemma 2's proof cannot both hold under one normalization. Medians over 40
   instances, `d = 50`, `k = 5`, `w_min = 1`, `gamma = 0.5`
   (`pwe_lemmas.out`):

   | `n` | normalization | `min_S |A_j|` (needs `>= 0.25`) | `max_{S^c} |A_j|` (needs `< 0.0625`) | `max_j |B_j|` (needs `< 0.0625`) |
   |---|---|---|---|---|
   | 500 | `1/(rho n)` (as defined) | 0.0019 | 0.00046 | 0.0024 |
   | 5000 | `1/(rho n)` | 0.00020 | 0.000015 | 0.00025 |
   | 50000 | `1/(rho n)` | 0.000020 | 0.0000005 | 0.000026 |
   | 500 | `1/rho` (used in the proofs) | 0.951 | 0.230 | 1.175 |
   | 5000 | `1/rho` | 0.986 | 0.077 | 1.259 |
   | 50000 | `1/rho` | 0.996 | 0.025 | 1.288 |

   - **Under `1/(rho n)`**, Lemma 1 holds with room to spare
     (`Var(B_j | X) <= 4 gamma^2/(n rho^2)`). But (34a) fails, because
     `A_j ≈ w*_j/n`.
   - **Under `1/rho`**, (34a) holds. (34b) holds once `n` is large: its
     median is 0.025 at `n = 50 000`, consistent with a large `c0`. But
     `max_j |B_j| ≈ gamma sqrt(2 log d) ≈ 1.4` for every `n`, so Lemma 1
     fails by a factor of about 20 at the threshold `w_min/16`.

   The final comparison is scale-invariant:
   `min_S |a_j| ≈ sqrt n w_min` against
   `max_{S^c}|a_l| ≈ sqrt n gamma sqrt(2 log d)`. The factor `n` cancels, so
   no normalization can make the noise term negligible as `n` grows.

**Classification.**
- Step 1, taken alone, is a harmless misstatement.
- Steps 2 and 3 are a substantive error. They are what lets the proof conclude
  `max_j |B_j| -> 0` relative to the signal, and that conclusion is false.
- The reviewer's items 1–3 are all correct. The reviewer's summary "the
  variance step in its Lemma 1" is fair. The more precise description is an
  inconsistent normalization between Lemma 1 and Lemma 2, hidden by the two
  incorrect steps in the proof of Lemma 1.

I did not check the proof of Lemma 2 line by line. It has further slips that do
not affect its truth under the `1/rho` normalization:
- `rho I_n` appears where `rho I_k` is meant;
- a factor `n` is missing in `V(rho I + nD^2)^{-1} D^2 V'`;
- the event `{min_i |D_ii|^2 <= n/2}` should be `>=`;
- a union bound is written as `min_j |Y_j| > t`, where `max` is meant.

Its statement under `1/rho` agrees with the table above and with a direct
singular-value argument: `(1/rho) X_S'MX_S` has eigenvalues
`s_i^2/(rho + s_i^2) = 1 - O(1/sqrt n)`.

## 3. Why the theorem itself is false

Fix `d > k`, `w*` with support `S`, and `gamma > 0`. Let `rho = sqrt n` and
`n -> inf`.

1. **The optimal support is `S` with probability tending to 1.** Any `T != S`
   with `|T| = k` misses some `j in S`. Then `f(T) - f(S) = n ||w*_{S\T}||^2 (1 + o_P(1)) -> inf`.
   Here `f(T) = y'M_T y` is the value of the ridge fit on `T`.
2. **The on-support correlations grow like `sqrt n`.** We have
   `X_S'M_S y = rho beta^S`, where `beta^S = (rho I + X_S'X_S)^{-1}X_S'y -> w*`.
   Hence `min_S |a_j|/sqrt n -> w_min`.
3. **The off-support correlations are conditionally Gaussian.** For `l notin S`,
   `X_l` is independent of `(X_S, eps)`. So, given `(X_S, eps)`, the `a_l` are
   iid `N(0, ||r||^2)` with `r = M_S y`. Also `||r||^2/n -> gamma^2`, because
   `M_S` differs from `I` only on a `k`-dimensional subspace, where its
   eigenvalues are `O(1/sqrt n)`, and `||M_S X_S w*|| = O(1)`.
4. **Conclusion.** By Corollary 2, applied at the optimal support,
   `P(P_IR = P*) = E[(1 - 2 Phibar(m0/||r||))^{d-k}] + o(1)`, with
   `m0 = min_S |a_j|`. This tends to `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`.

The hypothesis of Theorem 2 holds for all `n >= n0(c0)`, and
`1 - 2e^{-c1 n} -> 1`. So the theorem fails for every `c0, c1 > 0`.

- Very small instances already fail: `d = 2`, `k = 1`,
  `w* = (1, 0)`, `gamma = 1` gives the limit `1 - 2 Phibar(1) = 0.68`.
- The reviewer's formula `(1 - 2 Phibar(b/gamma))^{p-k} ≈ 0.12` is this limit
  with `d = 50`, `k = 5`, `b/gamma = 2`. The exact value is 0.1230.
- The limit does not need equal magnitudes: only `w_min` enters.

## 4. Independent numerical checks

My code is `pwe-verify/pwe_lib.py`. It is written from the paper and imports
nothing from the reviewer's or the author's code. It uses the paper's model
(`X` iid `N(0,1)`, `eps` iid `N(0, gamma^2)`, `rho = sqrt n`). It computes:

- `P*` by **full enumeration** of all `C(50,5) = 2,118,760` supports, using
  the Gram form. The two best supports are re-evaluated by a direct ridge fit.
- `P_IR` from cvxpy (Clarabel) on the perspective form
  `min ||y - Xw||^2 + rho sum_j w_j^2/u_j` over the capped simplex. This is
  polished by projected gradient on the closed form
  `G(u) = y'(I + X D(u) X'/rho)^{-1} y`.
- A **two-sided bracket** on `P_IR`:
  - the upper bound is `G(u)` at a feasible `u`, evaluated in closed form;
  - the lower bound is the weak-duality value
    `2a'y - a'a - (1/rho) sum of the k largest (X_j'a)^2` at `a = M(u)y`.
- An **elementary certificate of inexactness**. Let `j` be the weakest
  feature in `S` and `l` the strongest feature outside `S`. The feasible point
  `u_t = 1_S - t e_j + t e_l` has `dG/dt(0) = -(a_l^2 - a_j^2)/rho`. So, for
  small `t > 0`, its closed-form value is below `P*` whenever the Corollary 2
  certificate fails. The script takes the minimum over a grid of `t`.

**(a) Direct instances** (`pwe_instances.py`, `pwe_instances.out`). The
parameters are `d = 50`, `k = 5`, `|w*_j| = 1`, `gamma = 0.5`. With
`n = 500, 5000`, PWE's `c0 = 24.3, 243.4`. Seeds `424242+s` regenerate the
reviewer's four instances per `n` (same generation order), and seeds `7000+s`
are fresh.

| `n` | seed | `S_opt = S_true` | cert | `max|a_l|/m0` | `(P* - P_IR)/P*` (bracket) | reviewer |
|---|---|---|---|---|---|---|
| 500 | 424242 | yes | fails | 1.259 | `2.467e-4` | 1.26, `2.47e-4` |
| 500 | 424243 | yes | holds | 0.915 | 0 (to `1e-15`) | 0.91, exact |
| 500 | 424244 | yes | fails | 1.411 | `6.235e-4` | 1.41, `6.23e-4` |
| 500 | 424245 | yes | fails | 1.724 | `3.219e-3` | 1.72, `3.22e-3` |
| 500 | 7000–7003 | yes (4/4) | fails in 3/4 | 0.89–1.34 | `1.0e-4` to `9.9e-4` (3 inexact) | — |
| 5000 | 424242 | yes | holds | 0.984 | 0 | 0.98, exact |
| 5000 | 424243 | yes | fails | 1.111 | `7.843e-6` | 1.11, `7.84e-6` |
| 5000 | 424244 | yes | fails | 1.038 | `8.662e-7` | 1.04, `8.62e-7` |
| 5000 | 424245 | yes | fails | 1.197 | `3.945e-5` | 1.20, `3.94e-5` |
| 5000 | 7000–7003 | yes (4/4) | fails in 4/4 | 1.17–1.56 | `1.7e-5` to `1.8e-4` | — |

In all 16 instances, enumeration confirms that the true support is the unique
optimum. The second-best support value exceeds `P*` by 1.8–3.1 times `P*`. The upper and lower bounds of the bracket agree to 3–4 significant
digits. The explicit swap point `u_t` has a closed-form value below `P*` in
every inexact case. So the relaxation is strictly inexact in 13 of 16
instances, independently of solver tolerances.

The reviewer's eight rows are reproduced digit for digit. The one small
difference is `8.662e-7` against `8.62e-7`: my cvxpy value is `8.63e-7`, and
the polished bracket is `8.662e-7`. The reviewer's conclusion "6 of 8 inexact,
`S*` the unique optimum" is confirmed with a different optimality proof
(enumeration instead of the saturated witness).

**(b) Exactness probability against `n`, per-entry noise**
(`pwe_mc.py entry`, `pwe_mc_entry.out`; 150 instances per row). Exactness is
decided exactly for each instance:
- if the certificate holds at the true support, the relaxation is exact by
  weak duality at `a = M_S y`;
- otherwise, `P*` and `S_opt` come from full enumeration, and Corollary 2 is
  applied at `S_opt`.

The limit is `(1 - 2 Phibar(2))^{45} = 0.1230`.

| `n` | PWE `c0` | P(exact) [95% CI] | P(`S_opt = S_true`) | mean conditional P(cert at `S_true`) | median `m0/sqrt n` | median `max|a_l|/sqrt n` |
|---|---|---|---|---|---|---|
| 500 | 24.3 | 0.080 [0.037, 0.123] | 1.000 | 0.052 | 0.931 | 1.210 |
| 2000 | 97.4 | 0.093 [0.047, 0.140] | 1.000 | 0.081 | 0.965 | 1.198 |
| 10000 | 486.9 | 0.113 [0.063, 0.164] | 1.000 | 0.104 | 0.984 | 1.215 |
| 50000 | 2434.5 | 0.153 [0.096, 0.211] | 1.000 | 0.114 | 0.993 | 1.231 |

The conditional column, `E[(1 - 2 Phibar(m0/||r||))^{d-k}]` over the same
instances, has lower variance than the 0/1 column. At `n = 50 000` the 0/1
estimate is 23/150 = 0.153, and its interval contains the limit 0.123.

The probability does not tend to 1. It rises slowly toward the limit 0.123
from below. Two finite-`n` effects fade as `n` grows: the ridge shrinkage of
`m0` (a factor of about `n/(n + sqrt n)`) and the signal contribution
`||w*||^2/n` to the null variance. The median of `max|a_l|/sqrt n` stays flat
(1.20–1.23), while `m0/sqrt n -> w_min = 1`. So the ratio of the largest null
correlation to the weakest true one does not shrink like
`gamma sqrt(log d/n)/w_min`, as Lemma 1 would imply. In every row,
`S_opt = S_true`.

**(c) Total-energy noise** (`eps` iid `N(0, gamma^2/n)`; `pwe_mc.py total`,
`pwe_mc_total.out`; same `d, k, w*, gamma`, 150 instances per row):

| `n` | PWE `c0` | P(exact) [95% CI] | P(`S_opt = S_true`) | mean conditional P(cert at `S_true`) | median `m0/sqrt n` | median `max|a_l|/sqrt n` |
|---|---|---|---|---|---|---|
| 50 | 2.4 | 0.747 [0.677, 0.816] | 1.000 | 0.766 | 0.822 | 0.713 |
| 100 | 4.9 | 0.993 [0.980, 1.000] | 1.000 | 0.997 | 0.885 | 0.510 |
| 200 | 9.7 | 1.000 (150/150) | 1.000 | 1.000 | 0.922 | 0.366 |
| 500 | 24.3 | 1.000 (150/150) | 1.000 | 1.000 | 0.953 | 0.236 |
| 2000 | 97.4 | 1.000 (150/150) | 1.000 | 1.000 | 0.977 | 0.119 |

Here exactness does tend to 1 once `n` is a few times
`(gamma^2 + ||w*||^2)/w_min^2 log d = 20.5`. This is consistent with Theorem 2
holding in that model. The intervals are Wald intervals. For 150 of 150
successes, the one-sided 95% upper bound on the failure probability is about
0.02 (rule of three).

## 5. Errata, later versions, follow-ups

The WebSearch budget of this session was already exhausted (my first search
was refused), so I used direct fetches instead:
- Crossref: the record for DOI 10.1007/s10107-015-0894-1, and works that
  update it.
- The Semantic Scholar citation list (about 80 citing papers). I scanned the titles.
- arXiv API queries.
- A full-text search of the papers below for their citations of PWE, and a
  reading of those passages.

Findings:

- **Erratum.** Crossref shows no `updated-by` relation and no work that
  updates the DOI. I found none.
- **Later version: Pilanci's PhD thesis** (UCB/EECS-2016-147, 14 August 2016,
  Chapter 6). Theorem 12 (Sect. 6.2.1, printed p. 180) is the same statement.
  The model specifies independent `N(0, gamma)` entries, apparently a
  typo. The proof (Sect. 6.12.1, printed pp. 199–200, Lemmas 31–32) retains
  both the claim `lambda_max(M) <= rho^{-1}` and the variance bound
  `4 gamma^2/rho^2`. So the thesis does not correct the error.
- **Dong, arXiv 1603.04572** ("On the exact recovery of sparse signals via
  conic relaxations"). Theorem 3 restates PWE's result faithfully (same noise
  model, `rho = sqrt n`, probability `1 - 2e^{-c1 n}`). The abstract relies on
  it by asserting that PWE's sufficient conditions transfer to Dong's
  relaxation, including recovery guarantees for Gaussian designs.
  There is no correction.
- **Bertsimas–Pauphilet–Van Parys, arXiv 1902.06547.** They quote PWE's
  Proposition 1 and cite reference 40, Theorem 2, for a high-probability
  uniqueness guarantee when the covariates `X_j` are independent.
  They take the theorem as valid.
- **Xie–Deng, arXiv 1806.03756.** They cite PWE only for randomized rounding
  (PWE Theorem 3), not for Theorem 2.
- **Atamtürk–Gómez, safe screening, arXiv 2004.08773.** They cite PWE's
  Proposition 1 and describe PWE's analysis of relaxation strength and
  conditions for exactness. There is no correction.
- **Other papers.** Atamtürk–Gómez–Han (1901.10334), Dong–Chen–Linderoth
  (1510.06083), the survey of Tillmann et al. (2106.09606) and 2203.02607 cite
  PWE only for the relaxation. Cifuentes–Li (2603.18215) does not cite PWE.
- **Not read.** "Learning sparse group models through Boolean relaxation"
  (ICLR 2023). OpenReview refused automated download. It may reuse PWE's
  argument, but I did not check.

Assessment: in every source I could read, Theorem 2 is either restated as
valid or not discussed. I found no published correction. Because of the
limited search, I cannot exclude an unpublished or informal correction.

## 6. Recommended wording for the repository notes

The note already contains an updated Remark 3.5 ("an error in the PWE Gaussian
theorem") and an updated Section 7 entry. Their account of the proof error is
accurate. Four points should be tightened.

1. **Drop "Alternatively, the theorem holds if one adds
   `w_min^2/gamma^2 >= C log d`."** This is false for the theorem as stated.
   With per-entry noise and fixed `d, w*, gamma`, the exactness probability
   tends to `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`, not to 1. Suggested text:
   "Under per-entry noise, an extra assumption `w_min^2/gamma^2 >= C log d`
   (with `C` large) repairs the argument, but the conclusion then holds with
   probability at least `1 - c d^{-c'} - c exp(-c'' n w_min^2/||w*||^2)`, not
   `1 - 2e^{-c1 n}`. Some assumption of this kind is necessary, since for fixed
   `d, w*, gamma` the exactness probability tends to
   `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`."
2. **Qualify "It becomes correct if the noise vector has total energy
   `gamma^2` ... their condition with the sharp constant `c0 = 2`."**
   Theorem 3.1 is asymptotic. It holds in regime (A), with `p -> inf`, equal
   magnitudes `|beta*_j| = b`, and fixed `sigma`. Its use with
   `sigma = gamma/sqrt n` is the author's extension, which I did not verify.
   Theorem 3.1 therefore does not prove PWE's non-asymptotic statement with
   probability `1 - 2e^{-c1 n}`. Suggested text: "With noise of total energy
   `gamma^2` (iid `N(0, gamma^2/n)` entries), PWE's own argument goes through
   once `U_j` is normalized by `rho` instead of `rho n` and
   `sigma_max(M) <= 1` is used; the printed variance bound `4 gamma^2/rho^2`
   is then valid. This gives their sample-size condition with an unspecified
   `c0` and failure probability `c exp(-c' n w_min^2/(gamma^2 + ||w*||^2))`, which is
   `e^{-c1 n}` only for bounded `k` and `gamma/w_min`. In regime (A) and for
   equal magnitudes, Theorem 3.1 (extended to `sigma = gamma/sqrt n` as above)
   identifies the sharp threshold `n = (2 + o(1))(k + gamma^2/b^2) log p`."
   Apply the same change to the Section 7 sentence "With total noise energy
   `gamma^2` instead, our Theorem 3.1 proves it with the sharp constant
   `c0 = 2`".
3. **Describe the error as a normalization mismatch.** Section 7 says
   "Remark 3.5 locates the error in their Lemma 1". Suggested text: "the two
   lemmas of their Appendix 7.1 are proved for different normalizations of
   `U_j` (Lemma 1 is true for `X_j'My/(rho n)`, Lemma 2 for `X_j'My/rho`); the
   mismatch is hidden by two incorrect steps in the proof of Lemma 1
   (`sigma_max(M) <= 1/rho`, and variance `4 gamma^2/rho^2` instead of
   `4 n gamma^2/rho^2`)."
4. **Base the falsity claim on the elementary argument.** Remark 3.5 first
   derives the conflict from Theorem 3.1(b) and Corollary 3.4. These are
   asymptotic in regime (A), which requires `n <= p`. The self-contained
   argument appears only later, as the `n -> inf` bullet, and it omits the step
   that the optimal support equals `S*` w.h.p. Lead with that argument.
   Suggested text: "For fixed
   `d, k, w*, gamma > 0` and `n -> inf`, the optimal support is `S*` w.h.p.,
   `min_{S*}|a_j|/sqrt n -> w_min`, and the null `a_l` are conditionally iid
   `N(0, ||r||^2)` with `||r||^2/n -> gamma^2`; by PWE's Corollary 2 the
   exactness probability tends to `(1 - 2 Phibar(w_min/gamma))^{d-k} < 1`,
   while the hypothesis of Theorem 2 holds for all large `n` and
   `1 - 2e^{-c1 n} -> 1`."

Also in the Summary: "This makes the Pilanci–Wainwright–El Ghaoui (PWE)
exactness condition explicit, with the sharp constant 2" suggests that the
note sharpens a correct PWE theorem. Suggested text: "This gives the sharp
constant 2 in the sample-size scaling `n ≍ k log p` that PWE's Theorem 2 aims
at (PWE's theorem itself, with `rho = sqrt n` and per-entry noise, is false as
stated; Remark 3.5)."

The remaining statements are accurate as written:
- PWE's Corollary 2 (the note's Corollary 2.4) and their algorithms are
  unaffected;
- Dong restates the theorem faithfully;
- the theorem is "false for every choice of `c0` and `c1`";
- the location of the errors in Appendix 7.1 is right.

## 7. Commands run (targeted, local)

From `research-20260928b/reviews/pwe-verify/`, with
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`, at most two processes at a time:

```
python3 pwe_instances.py > pwe_instances.out     # 16 instances, ~2 min
python3 pwe_lemmas.py > pwe_lemmas.out           # normalization table, eigenvalue check
python3 pwe_mc.py entry 150 500,2000,10000,50000 > pwe_mc_entry.out
python3 pwe_mc.py total 150 50,100,200,500,2000 > pwe_mc_total.out
```

Only these targeted checks were run. No project-wide checks were run, and CI
was not consulted. I kept the downloaded papers in `/tmp` and not in the
repository.
