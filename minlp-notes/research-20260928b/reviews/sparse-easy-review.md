# Review of the easy side of `bb-complexity/sparse-regression/phase-transition.md`

Scope: Sections 1–3 and 6 of the note (2026-09-28 version), plus the claims
of Sections 3.5, 7 and the Summary that rest on them. Section 4 (hard side)
is reviewed separately. Reviewer: independent; I did not write the note or its
code. Date: 2026-09-29. My scripts and raw outputs are in
[`sparse-easy/`](sparse-easy/). I did not edit the note and did not commit.

## Verdict

The mathematics of Sections 1–3 is correct as far as I could check. I
re-derived every identity in Sections 1–2 by hand, checked every step of
the proofs of Theorems 3.1 and 3.2, and tested the deterministic statements
numerically. I found no error that affects a theorem. Remark 3.5 is right:
the conflict with Pilanci–Wainwright–El Ghaoui (PWE) is real. I located the
error in PWE's own proof, so it is not a normalization slip in Dong's
restatement. Section 6 reproduces, but one reported result is wrong. At
`p = 3200` (Table 6.3), one of the eight "capped" runs fails C1 exactly. The
note's capping procedure cannot find such failures, because the saturated
witness gives the same bound to every violator. The other 30 capped runs
satisfy C1 exactly. All required corrections are small: qualifiers,
wording, and the Section 6 tables.

| Claim | Verdict |
|---|---|
| (F1)–(F4), Lemma 1.1 | Correct. Known results (PWE Thm 1/Cor 1; Xie–Deng for perspective = Boolean relaxation). |
| Lemma 1.2 (path lemma) | Correct as stated. The incumbent/best-bound qualifier is dropped in Cor. 3.3, the Summary, Section 5 and Section 6.1 (C1). |
| Lemma 1.3 | Correct. |
| Lemmas 1.4, 1.5 | Correct (1.5 re-derived and checked numerically). The node version of 1.4 was not re-checked. |
| Lemma 2.1 (witness identity) | Correct (algebra re-derived; numerical error below `4e-15`). |
| Lemma 2.2 | Correct. At the root-optimal dual vector it is exactly Atamtürk–Gómez's Proposition 2 (C2). |
| Proposition 2.3 (saturated witness) | Correct (with `H_V` invertible, as assumed). |
| Corollary 2.4 | Correct (non-strict form; better than PWE's strict one). |
| Lemma 2.5 | Correct. |
| (G1)–(G5), Lemmas 3.6–3.7 | Correct. |
| Theorem 3.1(a)–(c) | Correct. |
| Theorem 3.2(a) | Correct. |
| Theorem 3.2(b) | Correct. One false sentence in the proof ("`N'` grows polynomially"), which is harmless (C3). |
| Theorem 3.2(c) | Correct. "`T = C_eps log p`" is imprecise (C4). |
| Corollary 3.3 | Correct once the incumbent/best-bound qualifier is added (C1). |
| Corollary 3.4 | Correct (asymptotic only). |
| Remark 3.5 (PWE) | The discrepancy is genuine. PWE's Theorem 2 is false for its stated noise model, and the error is in its Appendix 7.1 (Section 4 below). |
| Heuristic 3.8, Section 3.5 | Correct as heuristics. The second-order term that explains the observed thresholds is missing (S1). |
| Tables 6.1–6.3 | 75 of 75 exact author decisions reproduced. The 31 capped runs decided exactly: 30 satisfy C1 and 1 fails (`p = 3200`, seed 1007). Table 6.3, the Summary and Section 6.3 need correction (C5). |
| Tables 6.4–6.5 (light check) | `OPT` reproduced by full enumeration in all 48 runs with `k = 3, 4`. Cliques are consistent. |
| Table 6.6 | Not checked. |
| Section 6.7 | 207 of 232 reproduced independently. All 25 disagreements are on the conservative side. |

## 1. Section 1: model, relaxation, B&B conventions

- **(F1)–(F4).** I re-derived all of them. `f(S) = y'M_S^{-1}y`, the
  residual `r_S = M_S^{-1}y` and `X_S'r_S = lam beta^S` follow from the
  normal equations and the Woodbury identity. (F2) is the generalized-ridge
  identity with `Q = lam diag(z_P)^{-1}`. (F3): `h(a,z) = 2a'y - a'M_z a`
  is maximized at `M_z^{-1}y`. Numerically, the perspective minimum, the
  closed form and `max_a h` agree to `5e-16` (`identities.py`).
- **Lemma 1.1.** Weak duality and the top-`m` bound are correct. Sion's
  theorem applies because the `z`-set is compact and convex. I solved the
  primal SOC model and a separately written dual SOC model (the variational
  form of `top_k`) at 48 nodes (root, removal, forced-in and mixed nodes;
  12 instances). They agree to `7e-8` relative. `L(a)` at the primal
  residual matches the primal value to `6e-9`.
- **Lemma 1.2 (path lemma).** (a) and (b) are correct. Every examined
  off-path node is a child of a path node, so it has exactly one wrong
  fixing, and monotonicity gives its bound. In (b), path-node bounds are
  `<= OPT` and off-path bounds are `> OPT`, so best-bound search finishes
  the path first. The path ends by integrality at the latest when
  `S1 = S°`, because the budget then forces `z = 1_{S°}`. The incumbent
  condition matters. Without an incumbent, and without best-bound search
  (for example, depth-first search that dives into an off-path child
  first), off-path children cannot be pruned and nothing bounds their
  subtrees. Theorem 3.2(a) and the second Summary bullet state the
  qualifier. Corollary 3.3 (first bullet), the "Thresholds in n" Summary
  bullet, Section 5 (second bullet) and Section 6.1 ("linear trees for
  every variable-branching rule") drop it. See C1.
- **Lemma 1.3.** Correct: `k` on-path branchings, `k` pruned siblings and a
  final integral leaf give `2k+1` nodes.
- **Lemma 1.5.** The formula follows from (F2) with `z = 1` on `C` and
  `z = 1/2` on `D`. I re-derived (a) and (b), including the
  parallelogram step. Numerically the formula matches to machine precision.
  (Lemma 1.4 is used on the hard side; I checked only the leaf version,
  which follows directly from convexity.)

## 2. Section 2: deterministic certificates

- **Lemma 2.1.** Expanding `alpha = r - Delta` with `Delta = M_S^{-1}X_V u`
  gives `alpha'M_S alpha = f(S) - 2u'a_V + u'H_V u` and
  `2 alpha'y = 2f(S) - 2u'a_V`, so `h(alpha,1_S) = f(S) - u'H_V u`. Also
  `c_V = a_V - H_V u`, and `M_S^{-2} ⪯ M_S^{-1}` gives
  `||Delta||^2 <= u'H_V u`. All three check numerically (errors `3e-15`,
  `3e-14`, and slack `>= 0`).
- **Lemma 2.2.** Because `M <= m`, the relevant top-`k` and top-`(k-1)` sets
  are the ones the proof names. The three bounds follow. Numerically, `L(alpha)`
  equals the closed form to `1e-15`, and the closed form never exceeds the
  exact node value (24 witnesses, 96 exact node solves). **Attribution:**
  with `alpha` equal to the root-optimal residual, `h(alpha,1_S)` equals `R`
  (with `S` the root's top-`k` set). The bounds then read
  `R + (c_[k]^2 - c_j^2)/lam` and `R + (c_i^2 - c_[k+1]^2)/lam`, which is
  up to notation, Atamtürk–Gómez's safe-screening Proposition 2 for the
  cardinality form (arXiv 2004.08773, read). The note should say so; see
  C2.
- **Proposition 2.3.** Correct, and `c_V = kappa s` holds exactly. The
  proposition assumes `H_V` invertible. In practice this fails when
  `|V| > n - k - 1`. The author's code skips such `kappa` values, and so does
  mine. Numerically, `f(S) - R <= Gamma` always holds.
- **Corollary 2.4.** Both directions are correct. For "only if", a maximizer
  of the concave dual exists because of the `-||a||^2` term, and the saddle
  point forces `alpha* = r` and `1_S` to be a maximizer of `sum z_i a_i^2`.
  The non-strict form is the right one. PWE's Corollary 2 requires a strict
  inequality on `S`, which fails in the (measure-zero) tie case. In 30
  random instances, the certificate agreed with exact root exactness every
  time (8 exact).
- **Lemma 2.5.** I re-derived it line by line: the budget identity
  `k(1+T)/(k-1-T) = (1+T)(1 + (1+T)/(k-1-T))`, the absorption
  `lam b_+^2 T <= kappa sum|w_l|` (which uses `kappa >= lam b_+`),
  `2 sum|w_l| e_l = 2sQ/L`, and `||X_{V'}w||^2 <= s^2 Q/L`. Numerically,
  `g(z)` never exceeded the bound (14 instances).

## 3. Section 3: proof audit

### 3.1 Heuristic sanity checks (the constants)

- **Root exactness.** By Corollary 2.4, the root is exact iff
  `max_{l ∉ S}|a_l| <= m0`. Given `(X_S, w)`, the null correlations are
  exactly iid `N(0, ||r||^2)`, and their maximum is
  `||r|| sqrt(2 log p)(1 + o(1))`. So the root is exact iff
  `(m0/||r||)^2 >~ 2 log p`. Since `m0 ≈ lam b_lam` and `||r|| ≈ omega_lam`,
  this is `tau_lam^2 >= (2 ± eps) log p`. Also
  `tau_lam^2 = A/(n sigma^2 + kA/n) < n/k` exactly for every `lam > 0`
  (with `A = (lam b_lam)^2`), not just up to `1 + o(1)`. This gives the
  threshold `n = 2k log p`. The mechanism is the same as in Wainwright's
  Lasso analysis: the bias part of the residual makes each null correlation
  a Gaussian with variance `(k/n)(lam b)^2`. So the constant 2 is expected.
- **Why `log(p lam/n)` for C1.** Suppose the dual vector caps each
  violator's correlation at `kappa ≈ m0`. The cost is about
  `(|a_l| - kappa)^2/||x_l||^2 ≈ e_l^2/n` per violator, because the
  violators are nearly orthogonal and `H_V ≈ nI`. The margin the cap buys
  is of order `m0^2/lam` (times `zeta`). So the relaxation can absorb about
  `n/lam` violators whose excess is of order `||r||`. The number of nulls
  above `tau` standard units is about `p Phibar(tau)`. Setting
  `p Phibar(tau) ≈ n/lam` gives `tau^2 ≈ 2 log(p lam/n)`. The converse is
  the primal version of the same balance: forcing a null in frees one
  budget unit worth `lam b^2 ≈ m0^2/lam`, and the relaxation spends it on
  violators, gaining `sum e_l^2/n`. Both directions are right at first
  order.
- **Second order (heuristic, useful for Section 6).** Replacing the sum in
  Heuristic 3.8 by its mean, `p Psi(tau) = tau^2 n/lam` with
  `Psi(t) ≈ 4 phi(t)/t^3`, gives
  `tau^2 ≈ 2 log(p lam/n) + 0.93 - 5 log tau^2`. The same computation for
  the saturated witness (optimizing `zeta` gives `zeta tau^2 ≈ 1`) gives
  `tau^2 ≈ 2 log(p lam/n) + 1.55 - 3 log tau^2`. For the ridge rule and sizes
  of Table 6.1:
  - `p = 200`: the formulas give 3.3 (C1) and 5.0 (witness). The observed
    50% points, from Table 6.1's mean `tau^2`, are about 3.3 and 4.8.
  - `p = 1600`: the formulas give 5.0 and 7.7. The observed 50% points are
    about 4.9 and 7.5.

  So the formulas match the observed transitions far better than
  `2 log(p lam/n)` (8.2 and 12.2 at these sizes) does. The `-5 log tau^2`
  term is why "C1 appears at about half of `2 log(p lam/n)`". See S1.

### 3.2 Line-by-line checks

- **(G1)–(G5).** Correct. (G1) uses `Phibar(t) <= e^{-t^2/2}/2`. (G4)
  follows from Bernstein with `x = mu + 3t`. I re-derived the closed form
  of (G5) (completing the square). It matches quadrature to `7e-10`, and
  `m(tau) <= 2 phi(tau)/tau` holds.
- **Lemmas 3.6, 3.7.** Correct (numerical check `4e-16`). The push-through
  identity and `P^perp ⪯ A_i ⪯ I` are right.
- **Theorem 3.2(a).** I checked every step.
  - Events. The conditional independence behind E5–E9 is right. `tau` and
    `kappa` are `(X_S, w)`-measurable. Given the `a_l`, `x_l^perp` is
    independent of `a_l`. `Delta` is fixed given `(X_S, w, (a_l), X_V)`, and
    the `x_l^perp` for `l ∉ S ∪ V` are fresh.
  - The failure-probability count is `11 + 3k` over `p`, and `3k/p <= 3C0/log p`.
  - Step 1: the AM-GM bound on the cross term is right. The leave-one-out
    error `sqrt(k log p/n) lam/n` is `O(log^{-2} p)` only because
    `lam <= n/log^2 p`.
  - Step 3: `H_V ⪰ W'W`, because `M_S^{-1} ⪰ P_{col(X_S)^perp} ⪰ P`.
  - Step 4: both bounds (`gamma_1 = O(n^{-1/4} + log^{-5/2} p) = o(1/log p)`,
    and the three terms of `eta_S`) hold under (A).
  - Step 5: the margin `lam b^2/(3 log p)` follows. The constant is
    conservative; `(2 - o(1)) lam b^2/log p` is available (S4).
- **Theorem 3.1.** (a) and (b) are correct. In (b), `m0/||r||` is at most
  `tau_lam(1 + o(1))`, and `(1 - 2 Phibar(t))^{p-k} -> 0` for
  `t^2 = (2 - eps/2) log p`. (c) is correct. The achievability needs only
  `T = Theta(log p)`; `T ≫ n/k` is not needed.
- **Theorem 3.2(b).** Correct. The choice `s = 3 lam b_+^2 L/Q <= 1`, the
  bounds `T <= 3/delta0 = 48/eps` and `t_l -> 0`, and the constant `4851/eps^2`
  all check out. One sentence is false but harmless: "`N'` grows
  polynomially in `p`". When `n` is polylogarithmic, `N' >= n/log^2 p` is
  only `>= log^4 p`. That is still enough for `t_l -> 0` (C3).
- **Sample-size forms, Corollaries 3.3 and 3.4.** Correct. With
  `k = p^gamma` and `n = alpha k log p`, the parameters lie inside (A). In
  3.2(c), `T` depends on `eps` and on `n/(k Lambda)` through the denominator
  `1 - c k Lambda/n`, not only on `eps` (C4).

### 3.3 How far the theorems are from any computable size

(A) requires `log^6 p <= n <= p`. This is possible only for
`p >= e^17 ≈ 2.4 × 10^7`. Every run in Section 6 lies outside (A), and so does
the fixed-`k` setting of Table 6.1 (`n = O(log p)`). The Section 6.1 sentence
"as the asymptotic threshold predicts (for fixed k, gamma -> 0)" therefore
reads a heuristic trend, not a theorem (C7).

The converse, Theorem 3.2(b), is further away still. At
`tau^2 = (2 - eps) L`, the forced-in gain from violators relative to the
budget price is about `1.6 (p lam/n)^{eps/2}/tau^5` (mean-field, as in
Heuristic 3.8). For `eps = 0.5`, it exceeds 1 only when `p lam/n` is about
`10^17` or larger. The violators involved must also be nearly orthogonal in
`R^n`. The note makes this point only for `lam = sqrt n` (the remark after
Corollary 3.4). It applies to Theorem 3.2(b) and to the second bullet of
Corollary 3.3 in general (S2).

## 4. The PWE discrepancy (Remark 3.5): resolved

I read PWE (Math. Program. 151, 2015, pp. 63–87; author-hosted PDF
`http://www.eecs.berkeley.edu/~elghaoui/Pubs/SparseLearningBoolean.pdf`,
linked from Pilanci's homepage) and Dong (arXiv 1603.04572). I did not keep
copies of either paper in the repository.

- **Normalization.** PWE's problem (3) is
  `(1/2) sum (<x_i,w> - y_i)^2 + (1/2) rho ||w||^2`, so `lam = rho`. Their
  relaxation (19) is `y'(X D(u) X'/rho + I)^{-1} y`, which is the note's `g`.
  Section 3.1 of PWE uses `X` with iid `N(0,1)` entries and noise with
  **iid `N(0, gamma^2)` entries** (per-entry variance). Theorem 2 then claims
  exactness with `rho = sqrt n` when
  `n > c0 (gamma^2 + ||w*||^2)/w_min^2 log d`, with probability
  `>= 1 - 2e^{-c1 n}`. Dong's Theorem 3 restates this faithfully.
- **Where PWE's proof fails (Appendix 7.1).** PWE define
  `U_j = X_j'My/(rho n)` and split it into `A_j + B_j`. Three things go wrong:
  1. Lemma 2 treats `A_j` as `X_j'M X_S w*/rho`, without the `1/n` (it shows
     `(1/rho) X_S'M X_S ≈ I`). So the working normalization is
     `U_j = X_j'My/rho = a_j/rho`.
  2. The proof of Lemma 1 asserts `sigma_max(M) <= 1/rho`. This is false for
     `M = (I + X_S X_S'/rho)^{-1}`, whose largest eigenvalue is 1.
  3. From `||M X_j|| <= 2 sqrt n`, it concludes that `X_j'M eps/rho` has
     variance at most `4 gamma^2/rho^2`. The correct bound is
     `4 n gamma^2/rho^2`, which equals `4 gamma^2` at `rho = sqrt n`.

  With the consistent normalization, `max_j |B_j| ≈ gamma sqrt(2 log d)` does
  not shrink with `n`. The proof then needs `w_min^2/gamma^2 >~ log d`, which
  is exactly the note's Corollary 3.4 conclusion.
- **Counterexample to PWE Theorem 2 as stated** (`pwe_counterexample.py`).
  Take `p = 50`, `k = 5`, `b = 1`, `gamma = 0.5` and `rho = sqrt n`, with
  `n = 500` (PWE's `c0 ≈ 24`) and `n = 5000` (`c0 ≈ 243`). In all 8
  instances, the saturated witness certifies that `S*` is the unique optimum.
  In 6 of them the root value is still strictly below `f(S*) = OPT`. The
  relative gap is `9e-7` to `3e-3`, and Corollary 2.4 confirms the gap
  exactly (the PWE certificate fails). As
  `n -> inf`, the exactness probability tends to
  `(1 - 2 Phibar(b/gamma))^{p-k} ≈ 0.12`, not to 1. So Theorem 2 is false
  for every choice of `c0, c1`.
- **Replication of the note's check** (`pwe_check.py`). I ran my own code
  with different seeds. The certificate held in 0 of 120 instances, with
  median `max|a_l|/m0` of 1.63, 1.53, 2.01, 1.80, 2.30, 2.09 (the note
  reports 1.61, 1.39, 2.02, 1.83, 2.27, 2.13). At `p = 1000` and
  `n = 13816`, the conditional exactness probability is `3e-21`.
- **The note's rescue is right.** With noise of total energy `gamma^2` (per
  entry `gamma/sqrt n`) and `lam = sqrt n`, exactness should switch on at
  `n = c · 2(k + gamma^2/b^2) log p` with `c = 1`. My simulation (`k = 5`,
  `gamma = b = 1`, 200 instances per cell) gives exactness probabilities of
  0.56, 0.57 and 0.59 at `c = 1` for `p = 10^3, 10^5, 10^8`. At `c = 0.85`
  the probability falls with `p` (0.28, 0.19, 0.10), and at `c = 1.2` it
  rises (0.83, 0.91, 0.97). The transition sharpens at `c = 1`, which is
  consistent with `c0 = 2`.
- **Recommendation.** Replace "We could not access the original paper …" with
  the specific finding. PWE's Theorem 2 is false for its stated per-entry
  noise model, because of the variance step in its Lemma 1. It becomes true
  with `c0 = 2` sharp if the noise has total energy `gamma^2`, or if one also
  assumes `w_min^2/gamma^2 >= C log d`. This is a correction to the
  literature and deserves to be stated plainly (C8).

(Side note: Dong's figures do not state the noise level. My noiseless
replication of his setup puts the PWE-certificate transition at
`alpha ≈ 2–3` for `p = 64–512`. That is earlier than his PWG curves, so his
experiments probably include noise. This does not affect the note.)

## 5. My simulations (independent code)

All scripts are in `sparse-easy/`, single-threaded BLAS, at most 6 processes.

1. **Deterministic identities** (`identities.py`, `identities.out`): 40
   random instances. The identities of (F1)–(F3), Lemmas 1.1 (48 nodes),
   2.1, 2.2 (96 exact node comparisons), 2.3, 2.4 (30 instances), 2.5, 3.6,
   3.7 and (G1), (G5) all hold. No violations.
2. **Root threshold at large `p`** (`root_large.py`, `root_large.out`). This
   uses the exact conditional law
   `P(exact | X_S, w) = (1 - 2 Phibar(m0/||r||))^{p-k}`, with `k = 200`,
   `sigma = 0.5`, and `lam` tuned. The table gives `P(root exact)` against
   `alpha`:

   | `p` | 1.6 | 1.8 | 2.0 | 2.2 | 2.5 | 3.0 |
   |---|---|---|---|---|---|---|
   | `10^4` | 0.00 | 0.01 | 0.11 | 0.38 | 0.77 | 0.97 |
   | `10^8` | 0.00 | 0.00 | 0.01 | 0.35 | 0.92 | 1.00 |
   | `10^16` | 0.00 | 0.00 | 0.00 | 0.45 | 0.99 | 1.00 |

   The transition sharpens at `alpha ≈ 2.2–2.3`, and its 50% point drifts
   down slowly. This is consistent with `alpha* -> 2`. The drift is slow
   because `lam/n ≈ 0.15–0.2` is far from `<= 1/log^2 p`: the ratio
   `tau_hat^2/tau_lam^2` is only 0.80, 0.87 and 0.90 at `p = 10^4`, `10^8`
   and `10^16`. The leave-one-out term `sqrt(2 log k)(lam/n)/tau` is the
   cause, and the (A) cap on `lam` is what removes it in the theorem.
3. **Witness (sufficient) C1 threshold at `p` up to `10^9`**
   (`c1_large.py`, `c1_large_summary.out`). Setup: `n = 800`, `k = 10`, an
   exact conditional simulation of the top 400 nulls, and 810 instances.
   The table gives the 50% point of witness certification in `tau_lam^2`:

   | `lam` (`n/lam`) | `p = 10^4` | `10^6` | `10^9` |
   |---|---|---|---|
   | 28.3 (28) | 7.17 | 16.09 | 29.43 |
   | 90 (8.9) | 9.48 | 18.01 | 31.41 |

   Going from `p = 10^4` to `10^6`, the 50% point moves by +8.9 (`lam = 28.3`)
   and +8.5 (`lam = 90`); `2 log(p lam/n)` predicts +9.2. From `10^6` to
   `10^9` it moves by +13.3 and +13.4, against +13.8 predicted. Going from
   `lam = 28.3` to `90`, it moves by +2.31, +1.92 and +1.99 at the three
   values of `p`, against +2.32 predicted; a `log p` threshold would predict
   0. The offset from `2 log(p lam/n)` is between −4.6 and −5.7 and grows
   slowly with `p`, as the second-order term predicts. Root exactness
   reaches 50% at 16.4, 25.1 and 38.5 (`lam = 28.3`), which is about
   `2 log p - 2` to `2 log p - 3`.
   At `lam = 280` (`lam/n = 0.35`, outside the spirit of (A)), `tau_hat`
   departs from `tau_lam`, which confounds the comparison.
4. **Failure side at `n = 800`** (`c1_fail.py`, `c1_fail_summary.out`). This
   is an upper bound: the forced-in node of the top null, restricted to `S`
   plus the top 400 nulls. The bound stays at about `f(S*) + (0.7–1.05) lam b_lam^2`
   down to `tau_lam^2 = 2 log(p lam/n) - 16`, with thousands of nulls above
   `m0`. Failure appears only at `tau_lam^2 ≈ 3–7` (`p = 10^6`, `lam = 90`).
   So at this `n`, the converse mechanism is nowhere near its first-order
   threshold, as Section 3.3 above predicts. Caveat: these are upper bounds
   from a restricted pool.
5. **Exact C1 threshold versus `lam` and `p`** (`c1_lam.py`,
   `c1_lam_summary.out`). Setup: `n = 400`, `k = 10`, `p ∈ {1000, 8000}`,
   `lam ∈ {20, 45, 100}`, 70 instances per cell, with `tau^2` randomized and
   C1 decided exactly by column generation. All 420 runs were decided (355
   satisfy C1, 65 fail). The table gives 50% points in the realized
   `tau_hat^2`, from a logistic fit:

   | `p` | `lam` | exact C1 | witness | root certificate | `2 log(p lam/n)` | second-order heuristic |
   |---|---|---|---|---|---|---|
   | 1000 | 20 | 1.7 | 4.3 | 10.5 | 7.8 | 3.1 |
   | 1000 | 45 | 1.9 | 5.5 | 11.2 | 9.5 | 3.8 |
   | 1000 | 100 | 2.6 | 6.9 | 10.3 | 11.0 | 4.5 |
   | 8000 | 20 | 2.3 | 7.4 | — | 12.0 | 4.9 |
   | 8000 | 45 | 3.8 | 8.5 | — | 13.6 | 5.8 |
   | 8000 | 100 | 4.1 | 9.1 | — | 15.2 | 6.7 |

   I fitted the C1 outcome jointly on `tau_hat^2`, `log lam` and `log p`.
   The 50% contour moves by 0.88 (bootstrap 90% interval [0.69, 1.11]) per
   unit of `log lam` and by 0.63 ([0.51, 0.74]) per unit of `log p`. For the
   witness, the two slopes are 1.29 and 1.35.

   A threshold in `log p` alone would give a `lam` slope of 0. The root
   threshold behaves that way: at `p = 1000` it stays at 10.3–11.2 for all
   three values of `lam`. The C1 and witness thresholds instead move with
   `lam` about as much as with `p`, as a threshold in `log(p lam/n)` requires.
   The slopes are well below the first-order value 2, as the second-order
   heuristic predicts. At these sizes, the transition sits at very small
   `tau^2`, with hundreds of overlapping violators. This is a finite-size
   regime, far from (A).
6. **Re-deciding the note's C1 experiments** (`verify_table61.py`,
   `verify_cg.py`, `compare_author.py`). The instances follow the note's
   generator and seeds. The decision logic is mine: lower bounds from
   `L(a)` on the full node with a growing pool of dual vectors, and upper
   bounds from restricted SOC solves with column generation.
   - All 75 exact author decisions I re-ran agree. The cells are `p = 100`
     (`alpha = 1, 1.25`), `p = 200` (`1.25, 1.5`), `p = 400` (`1, 1.25`), the
     three rows of Table 6.2 with `alpha <= 1.5`, and the non-capped runs at
     `p = 1600`, `alpha = 1.25, 1.5, 1.75`.
   - All 31 capped runs are now decided:
     - `p = 400`, `alpha = 1.25`: 2 of 2 satisfy C1.
     - `p = 800` (Table 6.3): 8 of 8 satisfy C1.
     - `p = 1600`, `alpha = 1.25 / 1.5 / 1.75`: 2 / 5 / 6 satisfy C1.
     - `p = 3200` (Table 6.3): **7 satisfy C1 and seed 1007 fails.**
   - For `p = 3200`, seed 1007, the forced-in node of null `j = 991` has
     exact value 80.286. A full, unrestricted SOC solve gives primal equal
     to dual to 4 digits, against `f(S*) = 82.700`. `S*` has no improving
     one-swap (checked against the 300 most-correlated nulls). The null has
     `|a_j| = 4.76 ||r||`, an event of probability 0.006 among 3195 nulls,
     and the realized `tau^2 = 1.96` is the lowest of the eight. Its own fit
     `a_j^2/(n+lam) = 6.89` nearly cancels the budget price
     `m0^2/lam = 7.16`. This is the finite-size last term of Heuristic 3.8,
     not the asymptotic mechanism of Theorem 3.2(b).
   - **Why capping missed it.** For the saturated witness, every violator
     has `|c_l| = kappa`. The witness bounds of all forced-in violator nodes
     are therefore identical: 521 ties at this seed. The note's
     "40 weakest nodes" were chosen by index order among the tied nodes. So
     "capped" was not evidence for C1 at `p >= 800`.
   - Exact decisions take seconds: at most 110 node solves and 6 s per run
     at `p = 3200`. The cap can be dropped.
   - Section 6.3's direct node solves reproduce: 5.99, 8.47, 8.70 for seed
     1000 and 6.84, 9.22, 9.25 for seed 1003. The root gaps 5.68 and 2.92,
     and the mean root gap 5.38, also reproduce.
7. **Tables 6.4–6.5, light check** (`hard_check.py`, `maxclique_check.py`).
   For all 48 runs with `k = 3, 4`, enumerating all supports reproduces the
   B&B `OPT` to `1.5e-15` relative. My greedy clique on the 300 best supports
   equals the reported clique in 47 runs. In the remaining run (8 reported,
   7 by my greedy search), an exact search finds a clique of size 8 among
   the 600 best supports, and 8 is at most the number of leaves (20).
8. **Heuristic 3.8** (`heuristic38.py`). Re-implemented from the formula, it
   reproduces 207 of 232 runs. All 25 misses predict failure where C1 holds.

## 6. Section 6 claims

- The first-order thresholds of Section 6.1 reproduce:
  `alpha ≈ 2.56, 2.76, 2.94, 3.23` for C1 and 5.06 for the root. The values
  for Table 6.2 (2.33 and 4.45) also reproduce.
- The Table 6.1 entries recompute from the data (`make_tables.py` logic
  plus the dedup in `fill_note.py`).
- Needed changes (C5):
  - Table 6.1, `p = 1600`: C1 holds in 2, 7 and 8 of 8 runs at
    `alpha = 1.25, 1.5, 1.75`. At `alpha = 1.5` there is one failure, as
    before.
  - Table 6.1, `p = 400`, `alpha = 1.25`: 6 of 8.
  - Table 6.3: 8 of 8 at `p = 800`; **7 of 8 at `p = 3200`, with one
    failure**.
  - The Summary bullets "C1 held or passed every tested node up to
    `p = 3200`" (fixed-ridge bullet) and "C1 held (or passed its 40 weakest
    nodes) up to `p = 3200`" (computations bullet) hide a C1 failure in one
    run.
  - Section 6.3's "So C1 still holds for the most dangerous nodes" was
    checked only at seeds 1000 and 1003.
  - Section 6.1's "at `alpha = 1.75` two runs are certified and the other
    six passed" can now read "all eight are certified".
- The scout-data claim holds: 124 C1 runs have 5–55 nodes and none has 1.
  The scout's B&B starts with `S*` and a greedy incumbent and applies a
  rounding heuristic at every node. An exact root would therefore close at
  one node, so more than one node does imply an inexact root, up to its
  `1e-6` tolerance.

## 7. Novelty

Sources I checked:

- PWE: full text, including Appendix 7.1.
- Dong 1603.04572: full text.
- Atamtürk–Gómez, safe screening (2004.08773): statements.
- Xie–Deng (1806.03756): abstract and a text search. It proves
  perspective = Boolean relaxation. Its probability results concern
  randomized rounding, not random designs.
- Bertsimas–Van Parys (1709.10029): abstract. Empirical phase transitions
  only.
- Cifuentes–Li, "spartrahedron" (arXiv 2603.18215): a stronger SDP
  relaxation. It has a deterministic exactness region for sparse ridge
  regression and a Gaussian-noise corollary, but no random-design
  threshold.
- Tan–Wang, screening cut generation (2505.01082): abstract. No
  random-design theory.
- Wainwright's Lasso threshold `2k log(p-k)`: from memory.

The web-search budget was exhausted. I used five additional arXiv API
queries ("perspective relaxation" and recovery; perspective, cardinality
and support recovery; convex relaxation, best subset and tight; mixed
integer, sparse regression and statistical relaxation; rank-one
convexification). They found nothing relevant. Assessment:

- Sections 1–2: (F1)–(F4), Lemma 1.1 and Corollary 2.4 are known (PWE,
  Xie–Deng). Lemma 2.2 at the root dual is Atamtürk–Gómez's Proposition 2.
  The note partly says so. The saturated witness (Proposition 2.3) and the
  explicit forced-in primal point (Lemma 2.5) look new.
- Theorem 3.1: a sharp constant with a converse for exactness of the
  Boolean/perspective relaxation under Gaussian design. I found no prior
  statement, and PWE's only random-design result is incorrect as stated.
  The technique is the Lasso primal–dual-witness argument transplanted to
  the ridge fit, so the novelty is in the result and the correction, not the
  method. Relative to Wainwright, the constant 2 is expected, and the note
  says so.
- Theorem 3.2 and Corollary 3.3: the `log(p lam/n)` threshold for complete
  single-variable probing, and the resulting window
  `2 - gamma < alpha < 2` of linear trees for every variable-branching rule
  (with the qualifier) while the root is inexact. I found no prior version.
  This is the main new contribution of the easy side.
- The note's Section 7 claim that marginal screening needs
  `n > 2(k + sigma^2/b^2) log p` (the `lam -> inf` limit) holds only when
  `log k = o(log p)`. For `k = p^gamma`, interference among the true
  features gives the heuristic `2(1 + sqrt gamma)^2 (k + sigma^2/b^2) log p`.
  Inside (A), `lam <= n/log^2 p` suppresses this interference, which is why
  Theorem 3.1 has no `(1 + sqrt gamma)^2` factor (S3).

## 8. Corrections

Required:

- **C1.** Add "(with the incumbent `OPT` available when off-path nodes are
  examined, or with best-bound node selection)" to Corollary 3.3 (first
  bullet), the "Thresholds in n" Summary bullet, Section 5 (second bullet)
  and Section 6.1 ("Linear trees for every variable-branching rule").
- **C2.** Lemma 2.2 / Lemma 1.1: state that Lemma 2.2 with `alpha` equal to
  the root-optimal residual is Atamtürk–Gómez's Proposition 2 (cardinality
  version).
- **C3.** Proof of Theorem 3.2(b): replace "`N'` grows polynomially in `p`" by
  "`N' >= min(mu/2, log^4 p) - 1 -> inf`" (because `n/log^2 p >= log^4 p`).
- **C4.** Theorem 3.2(c): "`T = C_eps log p`" should say
  "`T = Theta_eps(log p)`, depending also on `n/(k log(p/sqrt n))`".
- **C5.** Section 6: update Tables 6.1 (`p = 400` and `1600` rows) and 6.3,
  the Summary computations bullet on `lam = sqrt n`, Section 6.3 and the
  remark after Corollary 3.4 ("C1 holds (Section 6.3)"), per Section 5
  item 6 above. Describe the tie problem of the "capped" procedure, or drop
  the cap (exact column generation is cheap).
- **C6.** Credit Xie–Deng for the equivalence (F2) = (F3) (the perspective
  form equals the Boolean form).
- **C7.** Section 6.1: fixed `k` violates (A) (`n >= log^6 p`). Present the
  "moves up with `p`" observation as consistent with the heuristic, not as
  predicted by the theorems. State that (A) needs `p >= 2.4 × 10^7`.
- **C8.** Remark 3.5 and Section 7 (PWE): replace "could not access" with the
  located error (Section 4 above) and state that PWE's Theorem 2 is false as
  stated.

Suggested:

- **S1.** Add the second-order balance
  `tau^2 ≈ 2 log(p lam/n) + 0.93 - 5 log tau^2` (C1) and
  `2 log(p lam/n) + 1.55 - 3 log tau^2` (witness) to Heuristic 3.8 or
  Section 3.5. It explains the size of the finite-`p` gap in Tables
  6.1–6.3.
- **S2.** After Corollary 3.4, say that the converse (Theorem 3.2(b)) needs
  `p lam/n` astronomically large for any fixed `eps`, and this holds for any
  `lam`, not only for `lam = sqrt n`.
- **S3.** Qualify the marginal-screening remark in Section 7 (Section 7
  above).
- **S4.** Theorem 3.2(a): Step 5 gives more than it states. Since
  `Gamma = o((m^2 - M^2)/lam)` and `m^2 - M^2 >= 2 zeta m0^2 (1 - o(1))`, every
  single wrong fixing has bound at least `OPT + (2 - o(1)) lam b^2/log p`, not
  just `OPT + lam b^2/(3 log p)`.

## 9. Not checked

- Section 4 and Conjecture 5.2 (separate review), Question 5.1, and the
  Section 5 heuristic.
- Table 6.6 (branching rules). It needs exact `OPT` at `p = 100, 200`,
  `k = 6, 8`, which I did not compute.
- Tables 6.4–6.5 for `k >= 5`.
- The node version of Lemma 1.4 (incumbent-based reductions; it depends on
  the earlier review).
- Wainwright, Gamarnik–Zadik, Hazimeh–Mazumder–Saab and
  Argyriou–Foygel–Srebro (from memory only).
- Whether the second-order formulas of S1 can be made rigorous.
- Whether C1 can hold for `lam < sqrt n` or `lam > n/log^2 p`. The theorems
  and the "optimizing over `lam`" statements cover only (A). The heuristics
  above suggest (A) contains the optimum.

## 10. Commands run (targeted, local; CI not inspected)

From `research-20260928b/reviews/sparse-easy/`, all with
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`:

```
python3 identities.py > identities.out
python3 pwe_check.py > pwe_check.out
python3 pwe_counterexample.py > pwe_counterexample.out
python3 root_large.py > root_large.out
python3 c1_large.py c1_large.jsonl 5;  python3 summ_c1_large.py > c1_large_summary.out
python3 c1_fail.py c1_fail.jsonl;      python3 summ_c1_fail.py > c1_fail_summary.out
python3 c1_lam.py c1_lam.jsonl 5;      python3 summ_c1_lam.py > c1_lam_summary.out
python3 verify_table61.py P ALPHA      (P, ALPHA) = (100, 1.0), (100, 1.25), (200, 1.25), (400, 1.0)
python3 verify_cg.py 3200 5 sqrtn 3.0 1000,...,1007   (also 800 5 sqrtn 3.0; 1600 8 1.5 {1.25,1.5,1.75};
                                                        400 8 1.5 1.25; 400 20 1.5 {1.0,1.25,1.5}; 200 8 1.5 1.5)
python3 compare_author.py > compare_author.out
python3 inspect_p3200_s1007.py
python3 heuristic38.py > heuristic38.out
python3 hard_check.py;  python3 maxclique_check.py
```

These are targeted checks of the reviewed material only. No project-wide
checks were run, and CI results were not consulted.
