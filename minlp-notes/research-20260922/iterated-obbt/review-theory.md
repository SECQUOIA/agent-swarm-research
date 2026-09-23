# Review of theory.md and proofs-12-11.md (iterated OBBT)

Date: 2026-09-23. Reviewer: independent adversarial review (fresh context).
Scope: every statement and proof in `theory.md` (the version that states Theorem 12
with `C^2` hypotheses and links to the full proofs) and in `proofs-12-11.md`, with
`literature.md` and `literature-cluster.md` as context. I did not edit `theory.md`.

## Summary

No claim is wrong. Every mathematical statement checked is correct or correct
after a small fix. The substantive items:

1. **Gap: "exact asymptotic rate".** Section 3 says it "gives the exact
   asymptotic rate", and Section 6 treats observed ratios as estimates of
   `r*(Phi)`. The note proves only an upper bound (any ratio above `r*`). It
   proves a matching lower bound only when `Phi` has an eigenvector `u >> 0`,
   the remainder is zero and `epsilon = 0`. See item 7 for the fix.
2. **Scope: Jacobi rounds.** `T_U` solves all `2n` bound problems on one
   relaxation. Solvers usually tighten variables one at a time and rebuild the
   relaxation after each change (Gauss–Seidel). Upper bounds and stall results
   carry over by monotonicity. The lower-bound remark and the "exact" rate of
   Proposition 7 do not. For `x^2 + y^2 + xy`, sequential rounds contract at
   0.7053 per round, against `rho(1) = 0.7247` for Jacobi rounds.
3. **Proposition 8 can use a non-strict inequality.** With zero remainder,
   `Q(1, ±e_k) <= 0` is enough. For `a = 0.1` the example then stalls from
   `n >= 6`, not `n >= 7`; I confirmed `n = 6` numerically.
4. **Stale text in theory.md after the Theorem 12 update.**
   - Section 3 says conditions for factorable McCormick relaxations are "to be
     worked out".
   - The Section 6 "Open" list still includes "sufficient conditions for (T)".
   - The Theorem 12 sketch still has the bracket "[A complete proof must
     also treat …]".
   - The sketch claims `|h^cv - h| = O(w^3)` when `h'' = 0`. That needs `C^3`,
     but the stated hypothesis is `C^2`, which gives only `o(w^2)`.
5. **Missing standing assumptions.**
   - `phi_B` should be convex and continuous (lower semicontinuous is enough)
     on `B`. This makes `Q(d, .)` convex and continuous. It is needed for "2n
     convex programs" and for `Phi_delta -> Phi` as `delta -> 0`.
   - (R2) for composite McCormick relaxations needs a citation (inclusion
     monotonicity) before Theorem 12 can feed Theorem 4.
6. **Typo:** `rho(1.9) = 0.974838`, so it rounds to 0.9748, not 0.9749.

Theorem 12 and Proposition 11 (full proofs) are correct. I checked every step,
and an independent implementation reproduces the `E`-recursion.

## Verdicts per claim

| # | Claim | Verdict |
|---|---|---|
| 1 | Setting, OBBT operator `T_U` | correct with fix (closed hull; Jacobi scope) |
| 2 | Lemma 1 | correct |
| 3 | Proposition 2 | correct |
| 4 | Proposition 3 (and "no contraction at a = 1") | correct |
| 5 | Assumption (T) and its consequences | correct with fix (domain; convexity/continuity; stale sentence) |
| 6 | Tangent maps `Phi_c`: monotone, 1-homogeneous, `Phi(d) <= d`, scaling law | correct (minor: `sup`, convention for `c < 0`) |
| 7 | Definition and interpretation of `r*(Phi)` | definition correct; "exact rate" claim is a gap; "`r* <= 1` up to slack" should be "`r* <= 1`" |
| 8 | Theorem 4 (incl. domain condition, iterates `B_k` strictly inside the gauge box) | correct |
| 9 | Corollary 5 | correct |
| 10 | Theorem 6 | correct with minor completion |
| 11 | Lower-bound remark | correct (Jacobi rounds only) |
| 12 | Section 4: zero remainder, translation invariance | correct with fix (`H_ii >= 0`) |
| 13 | Proposition 7 (formula, symmetry, independence of box shape) | correct with fixes (0.9748; domain remark; sense of "rate") |
| 14 | Proposition 8 and scaled version | correct; can be strengthened to `<=` |
| 15 | Example (strongly convex, `a(n-1)(n-2)/2 > 1`) | correct; with `<=` it becomes `>= 1` (`n >= 6` for `a = 0.1`) |
| 16 | Theorem 12 (statement in theory.md, proof in proofs-12-11.md) | correct; theory.md sketch has stale text |
| 17 | Corollary 9 | correct with minor fixes |
| 18 | Lemma 10 | correct (cite (R2) for the gap statement) |
| 19 | Proposition 11 and its proof (Lemma B1) | correct with minor fix (domain in choice of `wbar`) |
| 20 | Section 6 practical rule | heuristic; add caveats |

## Details

### 1. Setting and `T_U`

- Define the box hull as the smallest *closed* box, so that Lemma 1(c) works
  with compact boxes. Otherwise the sublevel set must be closed, which needs
  `phi_B` to be lsc.
- "One round of OBBT with exact LP/convex solves computes `T_U(B)`" is true for
  *Jacobi* rounds: all `2n` problems are solved on the relaxation built for `B`.
  Sequential rounds (Gauss–Seidel), which rebuild the relaxation after each
  variable, give boxes contained in `T_U(B)` by Lemma 1(b). So every upper
  bound (Propositions 2, 3 and 11, Theorem 4, Corollaries 5 and 9) and every
  stall result (Theorem 6, Proposition 8) transfers. Lower bounds do not.
  Measured with the exact solver (below), from `[-1,1.3] x [-1.2,1]`:
  - `a = 1`: Jacobi 0.724745, sequential 0.705323 per round;
  - `a = 1.9`: Jacobi 0.974835, sequential 0.974670.

  Add one sentence stating that the rate results are for Jacobi rounds.

### 2. Lemma 1

Correct. (a) uses (R1). (b) uses (R2): the set whose hull is taken shrinks.
(c) needs `x* in X ∩ B_0` and `f* <= U`.

### 3. Proposition 2

Correct. From `w_{k+1} <= (2 tau/kappa) w_k^2 + 2 epsilon/kappa`:

- if `w_k <= kappa/(4 tau)`, then `w_{k+1} <= w_k/2 + 2 epsilon/kappa`, so
  `limsup w_k <= 4 epsilon/kappa`;
- under the stated smallness condition, the level `4 epsilon/kappa` is
  invariant.

The vertex example is correct for box-constrained problems, where `X = R^n`
so that the growth holds on all of `B`.

### 4. Proposition 3

Correct. The ratio is at most `2 sqrt(tau/mu)`. The fixed point satisfies
`w^2 (1 - 4 tau/mu) = 4 epsilon/mu`, which gives the stated floor. For
`x^2 + y^2 + xy`:

- `mu = min_{||x||_inf = 1} f = f(1, -1/2) = 3/4`;
- `tau = 1/4`, the McCormick gap `w^2/4` times `a = 1`.

Since `tau > mu/4 = 3/16`, the claim "predicts no contraction" is right.

### 5. Assumption (T) and its consequences

- Homogeneity is correct: `x* + w D(lambda d) = x* + (w lambda) D(d)`. Divide
  by `w^2` and let `w -> 0`, using `K = {d, lambda d}`.
- `Q(d, 0) <= 0` is correct. It needs `x* in X`, so that (R1) applies at `x*`.
- Monotonicity in `d` is correct by (R2).
- **Fix (domain).** (T), and the monotonicity consequence, need
  `x* + w D(d) ⊆ B_0` for small `w`, or relaxations defined on boxes that
  leave `B_0`. For interior `x*` this is automatic. State it.
- **Fix (standing assumption).** Add "(R3) `phi_B` is convex and continuous on
  `B`", which McCormick and alphaBB satisfy. Then `Q(d, .)` is a uniform limit
  of convex continuous functions on `D(d)`, so it is convex and continuous.
  Two places use this without saying so:
  - "each `Phi_c(d)` is computed by `2n` convex programs" (Section 4);
  - `Phi_delta(1) -> Phi(1)` as `delta -> 0` (proof of Proposition 7).

  In general, `Phi_delta(u)` decreases to the hull shape of
  `∩_delta {Q(u, .) <= delta} = {Q(u, .) <= 0}` only when that sublevel set is
  closed, that is, when `Q(u, .)` is lsc.
- **Stale:** "conditions for factorable McCormick relaxations are to be worked
  out". Theorem 12 now gives them. Replace the sentence with a pointer to
  Theorem 12.

### 6. Tangent maps

All four properties are correct. Let `S_c(d) = {xi in D(d) : Q(d, xi) <= c}`.

- **Monotone.** For `d <= d'`: `D(d) ⊆ D(d')` and
  `Q(d', xi) <= Q(d, xi)`, so `S_c(d) ⊆ S_c(d')`.
- **Homogeneous.** Substitute `xi = t eta`: `Q(t d, t eta) = t^2 Q(d, eta)`.
  This gives `S_c(t d) = t S_{c/t^2}(d)`, which is both 1-homogeneity
  (`c = 0`) and the scaling law.
- **`Phi(d) <= d`.** Holds because `S ⊆ D(d)`.

Minor fixes:

- Use `sup`/`inf` in the definition, or assume (R3).
- For `c < 0` the set can be empty, and then the "shape" is undefined. Give a
  convention, since `proofs-12-11.md` B.2 uses `Phi^F_{-delta}`.

### 7. `r*(Phi)`: gap in the "exact rate" interpretation

- The definition is fine.
- "`r* <= 1` up to the slack `delta`" should read "`r* <= 1`". Since
  `Phi_delta(u) <= u` for every `delta`, `lambda = 1` is always admissible.
- Under (R3), `r*` equals the Collatz–Wielandt number of `Phi = Phi_0`:
  `cw(Phi) = inf {lambda : Phi(u) <= lambda u for some u >> 0}`. Proof: if
  `Phi(u) <= lambda u` and `lambda' > lambda`, then `Phi_delta(u) <= lambda' u`
  for small `delta`, by the lsc argument of item 5.
- **What is proved.**
  - With zero remainder and `epsilon = 0`, the iterates from `x* + D(d_0)` are
    exactly `x* + D(Phi^k(d_0))`. Their rate is therefore the Bonsall radius
    `r_B(Phi) = lim_k ||Phi^k(d_0)||^{1/k}`.
  - `r_B(Phi)` is the same for every `d_0 >> 0`: sandwich `d_0` between
    multiples of `u`, then use monotonicity and homogeneity.
  - Always `r_B <= cw = r*`, which is Corollary 5.
  - Equality `r_B = r*` is proved only when there is an eigenvector
    `Phi(u) = rho u` with `u >> 0` (the lower-bound remark).
- **What is not proved.** In general, equality needs a nonlinear
  Perron–Frobenius theorem: `cw = r_B` for continuous, order-preserving,
  homogeneous maps on `R^N_+` (Lemmens and Nussbaum, *Nonlinear
  Perron–Frobenius Theory*, 2012, Ch. 5; check the exact theorem). It also
  needs continuity of `Phi`, which the note does not establish.
- **Fix.** Replace "Section 3 gives the exact asymptotic rate" with: "Section 3
  gives an upper bound `r*(Phi)` on the rate. The bound is exact when `Phi`
  has a positive eigenvector (the lower-bound remark), for example in
  Proposition 7."
- Section 6's "power-iteration estimate of `r*`" is an estimate of `r_B`.

### 8. Theorem 4

Correct, including the point the coordinator asked about. The iterates `B_k`
are subsets of `x* + w_k D(u)`, not equal to it. The proof bounds `T_U` on the
enclosing box `x* + w_k D(u)` and uses Lemma 1(b):
`T_U(B_k) ⊆ T_U(x* + w_k D(u))`. That comparison needs (R2) for the pair of
boxes, so the enclosing box must lie in the domain. The condition
`x* + wbar D(u) ⊆ B_0` with `w_k <= w_0 <= wbar` ensures this.

- The inclusion `B_k ⊆ x* + w_k D(u)` is itself the induction hypothesis.
  Once `w_k < sqrt(2 epsilon/delta)`, Lemma 1(a) keeps later iterates inside,
  so (b) follows.
- Minor: "so `x*` is interior in the directions where `u > 0`". Since
  `u >> 0`, Theorem 4 requires an interior `x*`. Boundary minimizers are the
  subject of Proposition 11. Say so.
- Remark: with zero remainder and `epsilon = 0`, no `delta` is needed.
  `T(x* + w D(u)) = x* + w D(Phi(u))` exactly.

### 9. Corollary 5

Correct. Take `lambda' in [r*, lambda)` from the definition of the infimum.
Every box of small width that contains `x*` lies in some `x* + w_0 D(u)`, with
`w_0 <= width / min(u)`.

### 10. Theorem 6

Correct. One step is missing. Coordinates with `v_i^± = 0` also need the hull
to reach 0. This holds because `x*` lies in the sublevel set:
`phi_B(x*) <= f* <= U` by (R1). Add this sentence.

With zero remainder, `Q(v, xi) <= 0` at the witnesses is enough; `-delta` is
not needed. The stall width can be stated as `w max_i (v_i^- + v_i^+)`.

### 11. Lower-bound remark

Correct for Jacobi rounds (see item 1).

### 12. Section 4

- **Zero remainder.** On `x* + w D(d)`, each McCormick piece of
  `y_i y_j` evaluated at `y = w xi` is `w^2` times the piece on `D(d)` at `xi`.
  So `phi = f* + w^2 Q(d, xi)` exactly.
- **Translation invariance.** Checked. With `x = c + y` and `l = c + l'`:
  `l_j x_i + l_i x_j - l_i l_j = c_i c_j + c_j y_i + c_i y_j + (l'_j y_i + l'_i y_j - l'_i l'_j)`.
  Both pieces receive the same affine terms, so the max commutes with the
  translation. The same holds for the overestimator.
- **Fix.** State `H_ii >= 0`. For `H_ii < 0` a solver uses the secant, not
  the term itself. This still gives zero remainder, but a different `Q`: the
  secant `(H_ii/2)((d_i^+ - d_i^-) xi_i + d_i^- d_i^+)` replaces
  `H_ii xi_i^2/2`. The convex-program claim and Proposition 8's formula assume
  `H_ii >= 0`.
- If `X = R^n`, an interior global minimizer forces `H` to be PSD. Indefinite
  `H` requires a nontrivial `X`. Worth one sentence.

### 13. Proposition 7

**Algebra.** Verified.

- On `[-1,1]^2` the underestimator is `|xi_1 + xi_2| - 1`.
- For `|t| <= a/2` the minimizing `s` is 0, giving `Q_min = 2t^2 - a`. For
  `t > a/2` it is `s = t - a/2`, giving `Q_min = t^2 + a t - a^2/4 - a`.
- `Q_min` is continuous at `a/2`, where both formulas give `a^2/2 - a`, and
  increasing for `t > 0`. So the largest feasible `t` is the positive root
  `rho(a)`.
- `rho > a/2` if and only if `a < 2`. `rho <= 1` if and only if `a^2 <= 4`.
  `xi_2 = -a/2` lies in `[-1, 1]`.
- `Q(1, .)` is invariant under swapping the coordinates and under
  `xi -> -xi`, so `Phi(1) = rho 1`.
- `rho` is increasing: `(2a+2)^2 > 2a^2 + 4a`.
- The case `a < 0` maps to `|a|` under `xi_2 -> -xi_2`, which preserves the cube.

**Rate independent of the initial box: correct.** Any box with 0 in its
interior satisfies `x* + w D(1) ⊆ B ⊆ x* + W D(1)`. By monotonicity and the
cube eigenvector, `w rho^k <= half-width_k <= W rho^k`. So
`w_k = Theta(rho^k)`, and in particular `w_k^{1/k} -> rho`.

Numerically (exact solver, 400 rounds, four boxes, including very lopsided
ones such as `[-3, 0.02] x [-0.01, 5]`):

- the per-round ratio converges to `rho(a)` to 6–8 digits for
  `a = 0.5, 1, 1.5, 1.9, -1`;
- the transients are long near `a = 2`: from lopsided boxes the ratio at
  `k = 10` is 0.94–0.95 for `a = 1.9`, against `rho = 0.9748`.

That the per-round ratio converges is observed, not proved. The proof gives
`Theta(rho^k)`, so state the rate in that sense.

**Observation.** The eigenvector is not unique. Translated cubes
`[-c, 1-c]^2` satisfy `Phi(d) = rho d` for `c` in about `[0.41, 0.5]` at
`a = 1` (checked at `c = 0.45`). Asymmetric starts converge to such shapes,
for example `[-0.46, 0.54]^2`, which matches the author's B.4 observation.

**Fixes.**

- (a) `rho(1.9) = 0.974838`, so write 0.9748, not 0.9749.
- (b) The upper bound compares the iterates with the cube `x* + W D(1)`,
  which may extend beyond `B_0`. This is harmless here because McCormick
  relaxations are defined on every box, but it formally violates Theorem 4's
  domain condition. Say so, or argue directly.
- (c) With zero remainder and `epsilon = 0`, the limit
  `Phi_delta -> Phi` is unnecessary: `T(x* + w D(1)) = x* + rho w D(1)`
  exactly.
- (d) Add the Jacobi scope (item 1).

### 14–15. Proposition 8 and the example

**Correct.** Checks:

- The formula for `Q(1, ±e_k)` is right.
- The scaled version with `H' = S H S` is right: McCormick estimators scale
  by `h_i h_j` under `xi_i = h_i eta_i`.
- The example's arithmetic is right:
  `1 + a(n-1) < a n(n-1)/2` if and only if `a(n-1)(n-2)/2 > 1`.
- Strong convexity is right: the eigenvalues are `2 - a` and `2 + a(n-1)`.

**Strengthening.** Theorem 6 is not needed. `phi_B(x* ± w e_k) = f* + w^2 Q(1, ±e_k) <= f* <= U`
already holds when `Q(1, ±e_k) <= 0`. So the row condition may use `<=`, and
the example becomes `a(n-1)(n-2)/2 >= 1`. For `a = 0.1` this means
`n >= 6`, where the margin is exactly 0.

Numerical checks (Clarabel on the tangent problem):

- The many-term example gives `n = 3, a = 0.5`: `Phi(1) = 0.822876 · 1`
  (the note says 0.8229). The cases `n = 5, 6, 7, 10` all give `Phi(1) = 1`.
- Random `H`, cube: 48 of 48 instances satisfying the row condition stall.
- 5 of 12 violating instances also stall, so the condition is sufficient but
  not necessary. The note never claims necessity.
- Scaled version: 26 random instances with random half-widths all stall.

### 16. Theorem 12

**Correct.** I checked the proof in `proofs-12-11.md` line by line:

- **Lemmas A1–A5** are correct. In A3 the comparison is with the quadratic
  model, which handles `h'' = 0` and sign changes under `C^2`.
- **Product rule.** It matches Mitsos–Chachuat–Barton (2009). The identities
  `b^L α + a^L β - a^L b^L = αβ - (α - a^L)(β - b^L)` and the three others
  are verified.
- **Sign selections.** `α1` and `β1` use the same `ã` because `b^L` and `b^U`
  have the sign of `b*` for small `w`. When `b* = 0`, Lemma A5 bounds the cost
  by `O(w^3)`.
- **`(P_k)` for products.** The argument is valid: `(ã, b̃)` lies within
  `o(w^2)` of `Π`, and `M` is Lipschitz with constant `O(1)`.
- **Univariate rule.** `z^min = a^L` by Lemma A4. `mid = max(cv_a, a^L)` by
  Lemma A1, and `(P_a)` makes the clip `o(w^2)`. This closes the gap that the
  sketch in theory.md leaves open.
- **Concave side and E formulas.** Both are consistent.
- **Consistency with Section 4.** At `x* = 0`, `xi_i xi_j - E` is the
  McCormick piece.

**Independent check.** `code/review_checks/exp_thm12.py` is my own composite
McCormick code (MCB product rule, `exp` with the `mid` rule, scaling, sums) and
my own recursion. I ran it on:

- `exp(x) y` at three points, including `b* = 0` and all values 0;
- `x y z` at two points, including zero factors;
- `exp(-x y) z` at two points;
- `exp(exp(x) y - x)` at two points, which has a nested `mid` with `h' > 0`.

On 300 random shapes per `w`, with zero extents and face points included,
`max |(cv - v)/w^2 + E^cv|` and the `cc` counterpart fall by about 10 per
decade: for example 3.3e-1, 2.3e-2, 3.1e-3 at `w = 1e-1, 1e-2, 1e-3`. This is
consistent with `O(w)`.

**Fixes in theory.md.**

- (a) The sketch's "if `h''(a*) = 0`, `|h^cv - h| = O(w^3)`" needs `C^3`.
  Under the stated `C^2` hypothesis it is `o(w^2)`.
- (b) Delete the bracket "[A complete proof must also treat …]", or say
  that the full proof handles it.
- (c) Section 6 "Open: sufficient conditions for (T) for factorable McCormick
  relaxations" is now answered for composite McCormick. Keep only the lifted
  (auxiliary-variable) case open.
- (d) Using Theorem 12 inside Theorem 4 or Proposition 11 also needs (R1) and
  (R2) for composite McCormick. (R2) is inclusion monotonicity, a known
  property, but it should be cited; Scott, Stuber and Barton, "Generalized
  McCormick relaxations", JOGO 2011, is the likely source (verify).
- (e) Proof remark 5 ("`phi_B >= f - C w(B)^2`") is proved only for boxes
  `x* + w D(d)` with `d` in a compact set, which are boxes containing `x*`.
  That is enough here.

### 17. Corollary 9

**Correct.** `B_inf ⊆ x* + w D(u)` with `w^2 = 2 epsilon/delta`, by Theorem
4(b). (R2) gives `L(B_inf) >= min_{D(u)} phi_{B'}`. Minor fixes:

- (a) With `wbar` chosen as in Theorem 4, the remainder is at most
  `delta w^2/2 = epsilon`. So the explicit bound
  `L(B_inf) >= f* - (2G/delta + 1) epsilon` holds; `o(epsilon)` is not needed.
- (b) The sharp case inherits Proposition 2's condition: some iterate must
  have `w <= kappa/(4 tau)`. State it.
- (c) "Matches Castro (2023)" should read "is consistent with".

Numerically (exact solver, iterated to the fixed point, `epsilon = 1e-2` to
`1e-10`):

| Objective | `(f* - L(B_inf))/epsilon` | final width | notes |
|---|---|---|---|
| `x^2 + y^2 + xy` | 1.33333 | `2.3094 sqrt(epsilon)` | predicted `a/(1 - a^2/4) = 4/3`; `2/sqrt(1 - a^2/4)` |
| `x^2 + y^2 + 1.9 xy` | 19.487 | `6.405 sqrt(epsilon)` | matches the same formulas |
| `e^x - 1 - x + y^2 + xy` (nonzero remainder) | 2.855 → 2.82843 (`2 sqrt(2)`) | `4.000 sqrt(epsilon)` | |

In every case the limit box is symmetric even from the asymmetric start.
Rounds grow like `log(1/epsilon)`.

### 18. Lemma 10

Correct. The last claim uses (R2) as well:
`B_inf ⊇ H := hull{x*, x**}` implies
`L(B_inf) <= inf_H phi_{B_inf} <= inf_H phi_H = L(H)`. Cite (R2) in the proof.

### 19. Proposition 11 (theory.md statement) and Part B of proofs-12-11.md

**Correct.** Lemma B1 (i)–(iv) is verified:

- The sup-distance between `(d, xi)` and `(iota(d_F), iota(xi_F))` is at most
  `|d_A^+|`, because `0 <= xi_A <= d_A^+`.
- (iii) uses `g_i xi_i <= g^T xi` with every term nonnegative.
- (iv) uses the minimizer of `Q^F` and `t <= d_i^+`.

The induction in B.3 is verified:

- `G_0 <= G_M`, because `iota(u_F)` is admissible.
- `sigma_{k+1} <= C_sigma w^_k <= sigmabar`.
- Step `k_eps` uses (iii), which does not need `epsilon <= delta w^2/2`.
- The constant `(2 + 2 G_M/delta)` in (c) is correct.

Minor fixes:

- (a) The choice of `wbar` must also ensure `x* + wbar D(d) ⊆ B_0` for
  `d in K'`, that is, `x*_i + wbar M' <= u_i` in the active coordinates and
  interiority in `F`. Alternatively, note that the relaxations are defined on
  boxes beyond `B_0`.
- (b) theory.md says "ratio close to `lambda`". The proof gives exactly
  `lambda` after the first step. Harmonize.

The predicted stall constants (`2.3094 sqrt(epsilon)` free,
`(1 + a/(1 - a^2/4)) epsilon = 2.333 epsilon` active) agree with my 2D
computation of the same reduced tangent problem.

### 20. Section 6

Add caveats to the stopping rule:

- From asymmetric boxes the early ratios are *below* the asymptotic rate. For
  example, 0.699 at `k = 10` against 0.7247 for `a = 1`, and 0.94 against
  0.975 for `a = 1.9`.
- A ratio near 1 can mean slow contraction (`r*` close to 1), not only a stall
  or the `sqrt(epsilon)` floor.
- The rates are for Jacobi rounds.

The branch-and-bound bullet is a conjecture; label it as one.

## Numerical checks (reviewer's own code, `code/review_checks/`)

- `obbt2d.py` is an exact OBBT solver for two-variable objectives
  `e1(x1) + e2(x2) + a x1 x2` with McCormick on `x1 x2`. It uses no conic
  solver. For a fixed coordinate, the inner minimum of the max of the two
  McCormick pieces is found in closed form, because the pieces differ by an
  affine function. Bounds are then found by bisection to double precision.
  The zero-remainder quadratic case is rescaled exactly every round.
- `exp_rate.py`: Proposition 7 rates from four boxes, five values of `a`
  (item 13).
- `exp_cor9.py`: Theorem 4(b) floor and Corollary 9 gap for `epsilon > 0`
  (item 17).
- `exp_gauss_seidel.py`: Jacobi versus sequential rounds (item 1).
- `exp_rowcond.py`: many-term example, random-`H` row condition, and the
  scaled row condition, with Clarabel at tolerance 1e-10 (items 14–15).
- `exp_thm12.py`: independent composite McCormick and `E`-recursion
  (item 16).

Commands run (targeted only, from `code/review_checks/`):

```
~/miniconda3/envs/minlp-notes/bin/python exp_rate.py
~/miniconda3/envs/minlp-notes/bin/python exp_cor9.py
~/miniconda3/envs/minlp-notes/bin/python exp_rowcond.py
~/miniconda3/envs/minlp-notes/bin/python exp_thm12.py
~/miniconda3/envs/minlp-notes/bin/python exp_gauss_seidel.py
```

plus a one-off check of `Phi` on translated cubes `[-c, 1-c]^2` (item 13). No
project-wide verification was run. I did not check the literature
attributions against the sources; I used `literature*.md` as given.
