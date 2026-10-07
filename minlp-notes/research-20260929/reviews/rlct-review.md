# Referee report: "Real log canonical thresholds and the node complexity of spatial branch-and-bound"

Date: 2026-09-29. Note under review:
`research-20260929/rlct/rlct-node-complexity.md` (cited as [N]). Background:
`research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`
(cited as [CN]). The note was not edited. Nothing was committed. Referee
scripts and logs are in `research-20260929/reviews/rlct-review-checks/`.

## 0. Verdicts at a glance

| Claim | Verdict |
|---|---|
| Theorem 3.1 (face lower bound) | correct |
| Lemma 3.2 (projection to a face, fatness) | correct |
| Theorem 3.3 (bisection without (QD)) | correct |
| Corollary 3.4 (two-sided characterization) | inequalities correct; **the interpretation of the vertex term is false** (F1); the constants statement needs a fix (m2) |
| Lemma 3.5, Proposition 3.6 | correct; Proposition 3.6 needs `t_0 <= s0^2/4` (m1) |
| Lemma 2.1 (Lin asymptotics on faces) | correct; hypotheses match Lin's Section 2 |
| Lemma 2.2 | correct |
| Lemma 2.3 | (a) correct at interior zeros; **the consequence "at any zero, in any analytic coordinates" is false at boundary zeros** (F2). (b) correct; the citation should be rerouted (m4) |
| Lemma 2.4 (`lambda = n/2` iff nondegenerate) | correct |
| Theorem 4.1 | correct as stated; the `log(1/eps) #(optimal vertices)` term can be dropped (F1) |
| Corollary 4.2 | correct |
| Example 4.3 as a refutation of the conjecture | computation correct, but **not a literal counterexample**: `lambda = 5/4 > n/2`, which is outside the conjecture's hypothesis. Literal counterexamples exist and are given below (F3) |
| Section 5 worked examples | correct (all four RLCTs, multiplicities and leading constants recomputed; bisection counts reproduced exactly) |
| Summary item 2, example `xy + x^3 + y^3` | the volume asymptotic is correct, but the example is **misleading**: its edges give `eps^(-1/6)`, which dominates the face's `log^2` (F4) |
| Proposition 6.1, 6.2 | correct (6.1 conditional on Aoyagi–Watanabe as reported by Drton–Plummer, which I checked) |
| Theorem 7.1, Propositions 7.2, 7.3 | correct, except that the integral form in 7.2(c) for `k < 2` is proved only under (A2) (m3) |
| `y^2` and `x^4 + y^4` have `e_3 = 1/3` and `1/6` | correct |
| Remark 7.4 | correct (Bachoc et al. Theorem 3 checked) |
| Section 8 novelty | appropriately hedged; one precedent should be added (m8) |

## 1. Major findings

### F1. The `log(1/eps)` term at optimal vertices of `X0` is removable. The claim that it "is real" is false.

**Where.** Summary item 3 (`+ log(1/eps)·#(optimal vertices)`); Corollary 3.4
and the sentence after it ("That is the known log gap of bisection at vertex
minimizers [CN, Example 3.4, Remark 6.9], and it is real"); Theorem 4.1; the
"Vertices" bullet of Section 9 ("This is known and attained [CN, Example 3.4]").

**Why the cited evidence does not apply.** [CN, Example 3.4] is
`f = 2|y - a| - (y - a)^2` with `a = 1/3`. It is an *interior*, non-dyadic,
*non-`C^1`* sharp minimizer. [CN, Remark 6.9] needs a minimizer coordinate in
the middle part of its dyadic cell. A vertex of `X0` is a vertex of every dyadic
cell that contains it, so Remark 6.9 never applies there. Under (A1), sharp
minimizers can occur only at vertices of `X0`. At an interior point of a face,
`m|_F` is `C^{1,1}` with a critical point, so `m|_F <= M t^2/2`.

**Proof that the term can be absorbed.** Let `v` be a vertex with `m(v) = 0`.
Use inward coordinates `t = y - v >= 0`, and let
`g = min_i ∂_{e_i} m(v) >= 0` over the inward edge directions.

- *The only cube charged to `v` is the corner cube.* In the proof of Theorem
  3.3, a cube `D` is charged to the vertex `v` only if its witness `y` has
  `|y - v|_inf < s_j`. The only level-`j` cell containing such a `y` is the
  corner cell `D_j = v + [0, s_j]^n`, and it is non-pruned.
- *Case `g > 0`.* On `D_j`,
  `m(y) >= g|t|_1 - (M/2)|t|_2^2 >= |t|_1 (g - M s_j/2)` and
  `q_{D_j}(y) <= s_j |t|_1`. Non-pruning under (U^q) needs
  `m(y) < alpha' q_{D_j}(y) - eps`. That forces `s_j > g/(alpha' + M/2)`.
  So at most `1 + log2(s0 (alpha' + M/2)/g)` levels are charged, independent
  of `eps`.
- *Case `g` small or zero.* Along the edge `e` attaining `g`,
  `m(v + t e) <= g t + M t^2/2 <= (3M/2) t^2` for `t >= g/M`. So
  `I_edge(eps) >= c(M) min(log(s0 M/g), log(s0/sqrt(eps))) - C`, and the
  charged count `min(J, 1 + log2(...))` is at most `C(n, alpha', M, s0)(1 + I_edge(eps))`.

Hence `|T_bis| <= C_0 + C(n, alpha', M, s0) sum_{F: d>=1} I_F(eps)`, with no
vertex term. The dependence on `s0` comes only from additive `log s0` terms. So `N_opt ≍ |T_bis| ≍ max(1, max_F I_F)` holds with **no** bisection
exception under (A1). In Theorem 4.1 the upper bound is `C kappa*(eps)`.

**Numerical confirmation** (`logs/vertex_tests.jsonl`, exact node bounds):
- `m = x + y - 0.4(x^2 + y^2)` on `[0,1]^2`, `alpha = 8`: optimal vertex with
  `g = 1`. There are **16 leaves for every `eps` from `1e-2` to `1e-15`**, and
  only levels 0–2 have non-pruned cubes.
- `m = x - 0.4x^2 + y^2` (`g = 0` along the edge `x = 0`): the leaf count grows
  like `log(1/eps)` (7, 19, 28, 37, 49, 58, 73 at `eps = 1e-2 … 1e-15`). This
  matches `I_edge ≍ log(1/eps)`, so the log is already in `max_F I_F`.

**Fix.** Drop the vertex term from Summary item 3, Corollary 3.4 and Theorem
4.1, or keep it only as a proof artefact. Delete "it is real" and the Section 9
bullet. No dependence on `g` remains. `C_0` still depends on `s0` and on the
values of `m` at non-optimal vertices (m2).

### F2. Lemma 2.3(a)'s consequence fails at boundary zeros.

**Where.** Lemma 2.3(a): "the exponent `n/2 - lambda` of Corollary 4.2 is at
least `n/2 - 1/l`, for the Newton distance `l` computed in **any** analytic
coordinates at **any** zero". The same claim is in Summary item 4.

**The gap.** Lin's Theorem 1.3 bounds the *full-neighbourhood* local RLCT. The
global `lambda` is the minimum of the *box-restricted* local RLCTs, which are
**at least** the full-neighbourhood values at boundary points (Lin, Proposition
3.3). So the inequality runs the wrong way at boundary zeros. The zeros can lie
on `∂X0` exactly in Corollary 4.2(ii).

**Counterexample.** Take `m = (x+y)^2 + (x-y)^4 >= 0` on `R^2` and
`X0 = [0,1]^2`, so Corollary 4.2(ii) applies. The only zero is the corner 0.
- In the analytic coordinates `u = x + y`, `v = x - y`, `m = u^2 + v^4`, so
  `1/l = 3/4`.
- On the box, `V(t) = t/2 (1 + o(1))`. The script gives `V/t = 0.4990, 0.5000, 0.5000` at
  `t = 1e-2, 1e-4, 1e-6` (`logs/constants_check.log`, item 5). So
  `(lambda, theta) = (1, 1) = (n/2, 1)`.
- The edges carry `m = y^2 + y^4`, with `lambda = 1/2` and a log.

So `N_opt ≍ log(1/eps)`, while the claimed bound gives exponent
`>= 1 - 3/4 = 1/4`.

**Fix.** Restrict the consequence to zeros in `int X0`, or to coordinates in
which `X0` is locally a union of coordinate orthants at the zero. Monomial
majorants are sign-symmetric (Lin, Lemma 6.1), so the bound survives there.

### F3. Example 4.3 does not refute the conjecture as stated. Literal counterexamples do exist.

The conjecture assumes `lambda < n/2`. In Example 4.3, `lambda = 5/4 > 1 = n/2`,
so the conjecture says nothing. The note's "stated with this RLCT, would
predict a bounded count" is an extrapolation. The failure the note describes
is real, and it also occurs inside the conjecture's hypothesis:

- *Trivial case.* Take `n = 3`, `f = x(1-x)` on `[0,0.9]^3`. Then
  `RLCT_{X0} = (1, 1)`, so `lambda < 3/2` and the conjecture predicts
  `eps^(-1/2)`. The face `x = 0` has `m ≡ 0`, so Theorem 3.1 with `d = 2` gives
  `N_opt >= (2 alpha/pi^2) 0.81 eps^(-1)`.
- *Isolated minimizer.* Take `n = 4`,
  `m = x(1-x) + y^4 + z^4 + w^4` on `[0,0.9] x [-0.4,0.5]^3`, with
  `alpha = 1.05`.
  - Full dimension: `(lambda, theta) = (1 + 3/4, 1) = (7/4, 1)`, with
    `7/4 < 2 = n/2`. The conjecture predicts `eps^(-1/4)`.
  - Face `x = 0`: `(3/4, 1)`, so Theorem 4.1 gives `eps^(3/4 - 3/2) = eps^(-3/4)`.
  - Numerically (`logs/face4d.log`), the leaves are 136 → 8,361,361 over
    `eps = 1e-1 … 1e-7`, and `leaves·eps^(3/4)` stays in 24–50.
  - `leaves·eps^(1/4)` grows by a factor of about 2000.
  - Leaves over the Theorem 3.1 face lower bound stay in 22–47.

**Fix.** Present one of these as the counterexample to the literal conjecture.
Keep Example 4.3 as an illustration.

### F4. The `xy + x^3 + y^3` example in Summary item 2 does not exhibit `log^theta` node counts.

The stated volume asymptotic is right. The script gives
`V(t) = (1/3) t log(1/t) + (1/3) t + o(t)`, with
`(V - t log(1/t)/3)/t -> 0.333`, and so `I_F ~ (1/6) log^2(1/eps)`.

But on `X0 = [0,a]^2` the edges carry `m = x^3` and `m = y^3`, with
`lambda_edge = 1/3 < 1/2`. So `I_edge ≍ eps^(-1/6)`: `I_edge·eps^(1/6)` tends
to 2.80. Theorem 4.1 therefore gives `N_opt ≍ eps^(-1/6)`, not `log^2`.

In 2D this seems forced. `V ~ t log(1/t)` at a corner needs arms along the axes
where `m(x, 0) = o(x^2)`, and then the edge has `lambda < 1/2`. I do not know an
instance in which a `lambda_F = d_F/2`, `theta_F >= 2` face governs `N_opt`.

**Fix.** Qualify the example, or remove "and gives `log^theta`".

## 2. Claim-by-claim review

### 2.1 Section 3: Theorem 3.1, Lemma 3.2, Theorem 3.3, Corollary 3.4 (claim 1)

**Theorem 3.1: correct.** I checked every step.
- If `C` meets `F`, each fixed coordinate `b_i` is an endpoint of `[l_i,u_i]`,
  so `a_i^C = 0` on `F ∩ C`.
- `F ∩ C = {b_I} x prod_{i notin I} [l_i,u_i]` is full-dimensional in `F`.
- AM–GM followed by the arcsine integral gives `(pi^2/(alpha d))^(d/2)` per box.
- Summing over the cover gives the bound.

**Lemma 3.2: correct.** I rederived each step.
- Step 1 needs `s <= s0/2` and a cube `X0`; both are assumed. It uses
  `m >= 0` only on `X0`.
- Step 2 splits each summand by the sign of `sigma ∂_i m`, and each is at most
  `m(y) + M s^2/2`.
- Step 3 uses both points `y' ± s e_i`, which lie in `X0` because the
  coordinates `i notin I` have margin `>= s`.
- The final constants follow from
  `(1+d)(1+n-d) <= ((n+2)/2)^2` and `(1+d)(n-d)+d = (1+d)(1+n-d) - 1`.
- Random stress test (20,000 points and radii per dimension, `n = 2, 4`, biased
  toward faces): the largest ratio of `m(z)` to the bound is 0.66
  (`logs/lemma32_random.log`).

**Theorem 3.3: correct.** Details checked:
- The witness `y` comes from (U^q).
- Lemma 3.2 is applied with `s = s_j`, which is valid for `j >= 1`.
- For each face, the cubes `Q_F(z, s_j/2)` in the maximal packing are disjoint
  in `F`.
- Each charged `D` lies in `Q(z, 3 s_j)`, which holds at most `6^n` cells.
- The Fubini sum is `sum_{s_j >= theta} s_j^(-d) <= 2 theta^(-d)`.
- `E(Lambda_1 s_j^2) ⊆ {m + eps <= Lambda_2 s_j^2}` because `eps < Lambda_0 s_j^2`.

No (QD) is used, and `m >= 0` is used only on `X0`. The fatness argument is
sound.

**Corollary 3.4: the inequalities are correct.** Three remarks:
- **(F1)** The vertex term is removable, and "it is real" is false.
- **(m2)** "Within factors depending only on `n, alpha, alpha', M`" is not what
  is proved. The additive `C_0` depends on `s0` and, through
  `J_v ≈ log2(s0 sqrt(Lambda_1/m(v)))`, on the values of `m` at non-optimal
  vertices. It is absorbed by the `max(1, ·)` lower bound only with an
  instance-dependent factor. Nothing depends on `eps` except `J`, which F1
  removes.
- The `(R2)` counterexample `m = x + y` along an edge is right.

**Lemma 3.5: correct.** It has two gradient cases, `|g| <= sqrt(2 M m)` and
`|g| <= 4m/delta`, with the constants as stated. The (QD) failure example is
right.

**Proposition 3.6: correct after one fix (m1).**
- The claim "`X0` contains a cube `C_z` of side `s` with vertex `z`" needs
  `s <= s0/2`. At the centre of `X0` no such cube fits when `s > s0/2`. So
  `t_0 = min(M r^2/2, s0^2/4)`.
- The layer-cake constants check out: `[0, eps]` gives
  `4^d (d/2)(K_1+1)^(n/2)`, `[eps, t_0]` gives `4^d (d/n) 2^((n-d)/2) K_1^(n/2)`
  (using `K_1 >= 1`), and the tail is `H^d(F) t_0^(-d/2)`.
- The vertex bound `(n/2) 2^(-n/2-1) K_1^(-n/2) log(t_0/eps)` is correct.

### 2.2 Section 2: Lemmas 2.1–2.4 (claim 2)

I downloaded Lin, arXiv:1003.5338v3, and read Sections 1–4.

**Lemma 2.1: correct.**
- *Hypotheses.* Lin's Section 2 standing hypotheses are:
  `Omega = {g_1 >= 0, ..., g_l >= 0}` compact semianalytic; `f` and the `g_i`
  nonconstant; `f in A_Omega`, meaning analytic at each point of `Omega`; and a
  nearly analytic amplitude. A box face in its own coordinates, with affine
  `g_i`, satisfies all of them. Boundary zeros are covered by Lemma 2.4's
  simultaneous resolution of `f, phi, g_i`.
- Corollary 2.6 is (a).
- Theorem 2.10 with formula (12) gives
  `c_{lambda,theta} = (-1)^theta Gamma(lambda) d_{lambda,theta}/(theta-1)!`.
  This matches (b).
- Proposition 2.5 and Proposition 3.2(c) are (d).
- Example 2.8 checks out: `xy^2` has threshold 2/3 on `{0<=x<=y}` and 1/2 on
  `{0<=y<=x}`.
- Proposition 3.3, Corollary 3.5 with the remark after it, and Proposition 3.7
  are as quoted.
- (c) is Karamata's Tauberian theorem at 0 for the nondecreasing `V`, with
  `c_V = c_Z/Gamma(1+lambda)`. It is correct.
- Caveat: Lin's Theorem 2.10 proof is a formal Mellin/Laplace inversion ("≈").
  The rigorous leading term is standard through the chart decomposition, as
  the note says.

**Lemma 2.2: correct.**
- (i): the dominating function `u^(a-lambda-1) e^(-u) (2 + log(2+u))^(theta-1)`
  is valid for `eps <= 1/e`.
- (ii): the three-range argument is sound.
- (iii) is immediate.
- Spot check: for a nondegenerate 1D minimum the formula reproduces
  `sqrt(2/h) log(1/eps)`.

**Lemma 2.3.**
- (a) The inequality `RLCT_0(h) <= (1/l, theta_l)` is Lin's Theorem 1.3, proved
  through Propositions 4.2 and 4.12. `P(<h>) = P(h)` holds by Lin's definition.
  Its use at arbitrary zeros is wrong at boundary zeros (F2).
- (b) The statement is correct. The equivalence "positive face polynomials ⇔
  no singular zero on the torus" for nonnegative `h` is right, because a zero
  of a nonnegative polynomial is critical.
- **(m4)** Lin's Theorems 4.8–4.9, as literally stated, are false for `x + y`.
  Lin's nondegeneracy only excludes singular points, and Theorem 4.10's proof
  assumes `g(mu) != 0`. The note's own remark shows this, and Lin's Remark 4.6
  hints at it. For nonnegative `h`, the cleaner citation is Theorem 1.3
  (equality for sos-nondegenerate ideals) with Propositions 4.3 and 4.5(3):
  `<h>` is sos-nondegenerate iff `h_gamma` has no zero on the torus.
  Recommend citing that route.

**Lemma 2.4: correct.**
- The degenerate direction gives `V >= c t^((n-1)/2 + 1/3)`, hence
  `lambda <= n/2 - 1/6`.
- A non-isolated minimizer has a kernel direction.
- The Laplace constant `(2 pi)^(n/2) det(H)^(-1/2)` is right.
- The "`lambda = n/2` iff nondegenerate" part holds, as stated, only for
  interior minimizers. At box boundaries a degenerate zero can still give
  `lambda = n/2`; for example `(x+y)^2 + ...` at a corner. The note correctly
  restricts this to case (i).

### 2.3 Section 4: Theorem 4.1, Corollary 4.2, Example 4.3 (claim 3)

**Theorem 4.1: correct.** The case analysis of `kappa_F` from Lemma 2.2 is
right, including `m|_F ≡ 0`. The constants depend on `f` and `eps_0`, not on
`eps`. The vertex term is superfluous (F1).

**Corollary 4.2: correct.**
- Under (i), the proper faces have bounded `I_F`.
- Under (ii), Proposition 3.6 needs fix m1. Its `lambda <= n/2` argument, using
  the orthant piece of the ball around a boundary critical zero, is right.
- The explicit constants follow from Theorem 3.3 and Lemma 2.2(i). The
  constant ratio `2·12^n (pi^2 Lambda_2/(alpha n))^(n/2)` is right.

**Example 4.3.**
- `x/10 <= x(1-x) <= x` on `[0, 0.9]` gives `V ≍ t^(5/4)`.
- The edge `x = 0` has RLCT `(1/4, 1)`, and the other faces have `m > 0`.
- The conclusion `N_opt ≍ |T_bis| ≍ eps^(-1/4)` is correct.
- My independent bisection reproduces every leaf count in the note's sweep (below).
- It is not a literal counterexample to the conjecture (F3).

### 2.4 Section 5: worked examples (claim 4)

**RLCTs recomputed by hand.**
- `x^2 y^2`: `P = (2,2) + R^2_+`, `l = 2`, vertex, codimension 2, so
  `(1/2, 2)`. The box volume is exactly
  `V(t) = 4 tau(1 + log(ab/tau))` with `tau = sqrt t`. So `c_V = 2`, and the
  integral constant is `c_V Gamma(3/2) Gamma(1/2) = pi`, matching the fit
  3.14016.
- `(x^2 - y^3)^2`: weights `(1/2, 1/3)` give `lct(x^2 - y^3) = 5/6`, hence
  `(5/12, 1)`. The Newton distance is `12/5`, so `1/l = 5/12`, and `m` is
  Newton-degenerate. For `x^2 - y^3` itself, `l = 6/5 > 1`.
  - I recomputed `A = area{|u^2 - v^3| <= 1}` by integrating in `u`, which is
    the transverse direction: `A = 7.962236`, against the note's 7.962229.
  - The cusp's `V(t)/t^(5/12)` on its box increases 6.35, 7.22, 7.62, 7.80 at
    `t = 1e-6 … 1e-18`, toward `A`.
  - The exponent `7/12` is correct.
- `x^2 y^2 + z^4`: the edge `conv{(2,2,0),(0,0,4)}` meets the diagonal at
  `4/3` in its relative interior, and the face polynomial is positive on the
  torus. So `(3/4, 2)`, with `c_V = 2 K_4` and constant 4.44288.
- `x^2 + y^4`: `(3/4, 1)`, exponent `1/4`.
- The convexity thresholds are valid.
  - `xy2` has the exact threshold 1.69.
  - `cusp` has true threshold 0.753. The note's 2.72 is a valid, conservative
    "analytic bound".
- The auxiliary claims hold: `(x - y)^2` has `l = 1` and `lambda = 1/2`, and
  Lin's Remark 4.13 is as quoted.

**Independent bisection re-implementation** (`indep_bisect.py`). It uses the
same model (exact alphaBB, `UBD = f*`, uniform `2^n`-ary refinement), but with
different node solvers:
- closed-form or Cardano minimization per coordinate for the separable
  instances;
- for `xy2`, closed-form minimization in `x` and golden-section search on the
  convex marginal in `y`.

Result (`logs/indep_bisect_vs_note.log`): **all 111 runs match the note's leaf
counts exactly** — `sep24` 37/37, `bdry` 45/45 and `xy2` 29/29, down to
`eps = 1e-10`, `1e-12` and `1e-8`. There was one near-tie within `1e-10`
relative, and it made no difference. This confirms Table 5.2 and the
`leaves/LB` ranges.

### 2.5 Sections 6 and 7 (claim 5)

**Proposition 6.1: correct, given `lambda_AW`.**
- The scaling argument (`K(tA,tB) = t^4 K`) is right: the RLCT on a ball is
  independent of the radius and equals the minimum over the zero set, and a
  box sandwiched between two balls has the same RLCT.
- I checked Drton–Plummer, arXiv:1309.0911, Example 2.2 and Table 1. The values
  `3/2, 7/2; 3, 9/2, 6; 9/2, 11/2, 13/2, 15/2` and "multiplicity 1 unless
  `i = 3`, `j = 0`" match the note.
- The recalled Aoyagi–Watanabe formula reproduces them.
- From memory, not from their paper: Aoyagi–Watanabe's multiplicity is 2 when
  `M + H + N + r` is odd in the balanced case. That gives `theta = 2` exactly
  at `(H, r) = (3, 0)`, which is consistent with Drton–Plummer's statement.
- The `r = H` Morse–Bott rows are right: the normal rank is `H(M+N-H)`. The
  box-boundary effects are, as the note says, not re-verified.

**Proposition 6.2: correct.**
- I checked the three bounds on `F(x)` for `|x| <= C rho`
  (`2.2/eps`, `pi/(|x| sqrt eps)`, and `8.8/delta^2` when `|x| <= delta/2.6`).
- The tail expansion `pi/(|x| sqrt eps) + O(x^(-2))` holds for `|x| >= C rho`
  with `C >= 2/b`.
- The constants of Theorems 3.1/3.3 and Proposition 3.6 are uniform in `delta`:
  vertex values are `>= (0.81 - delta_0)^2`, and `alpha` can be chosen uniformly.
- Minor: "≍ `eps^(-1/2) log(1/max(eps, delta^2))`" needs `delta_0 < 1` and
  `eps <= eps_0 < 1`, or should be written with `1 + log`.
- The freeze constant `pi log(1/delta^2) + 0.99` matches the log.

Conjecture 6.3 is labelled as a sketch, and I did not assess it further.

**Theorem 7.1: correct.**
- (a) is the covering argument under (G^k).
- (b) uses the witness `m(y) < tau s_j^k - eps`, the 3^n cells met by a cube of
  side `s_j`, and a rescaling by `max(1, ceil(2(tau/alpha)^(1/k)))^n`.
- (c) uses `ceil(2^(1/k)) = 2`.

**Proposition 7.2.**
- (a), (b) and (d) are correct:
  - fatness at radius `r` gives `(1+n) eta + n M r^2`;
  - the two-sided `psi_k` bounds are right;
  - `(n/k - lambda)_+ <= e_k <= (n - 2 lambda)/k`.
- (c) is correct under (A2) for `lambda < n/k`.
- **(m3)** The parenthetical "(the last equivalence under (A2))" suggests that
  `N_opt ≍ |T_bis| ≍ integral (m+eps)^(-n/k)` holds for `C^{1,1}` `m` without
  analyticity. For `k < 2` only the upper bound by the integral is proved. The
  lower bound comes from `eta = eps`, `N_opt ≳ eps^(-n/k) V(eps)`, and (G^k)
  gives no integral bound, since `delta_C^(-n)` is not integrable at vertices.
  For `k = 2`, Theorem 3.1 supplies it. Restate the claim.

**Proposition 7.3: correct.**
- (a) matches Bubeck et al. 2011, Example 3, which I checked: dimension
  `(1/b - 1/a) D` for `f = 1 - ||x||^a` and `ell' = ||x - y||^b`.
- (b) is correct.
- For (c) I computed the exponents by hand, independently of the scripts:
  - `y^2`: `E(eta)` is a strip of width `2 sqrt(eta)`, thinner than the
    scale `eta^(1/3)`, so `psi_3 ≍ eta^(-1/3)` and `e_3 = 1/3`.
  - `x^4 + y^4`: `E(eta)` is a ball of radius `≍ eta^(1/4)`, so
    `psi_3 ≍ (eta^(1/4)/eta^(1/3))^2 = eta^(-1/6)` and `e_3 = 1/6`.
  - `x^2 y^2`: the arms give `eta^(-1/3)`; the central region gives only
    `eta^(-1/6) log`. So `e_3 = 1/3`.
  - At `k = 4` the exponents are `1/4, 0, 1/4`.
  - All three functions have `lambda = 1/2`. The claim that the exponent is
    not a function of `(lambda, theta)` for `k > 2` is correct.
- Minor (m5): `y^2` on the box has a minimizing segment that meets `∂X0`.
  Proposition 7.3(b), which assumes a compact manifold without boundary in
  `int X0`, does not apply verbatim. The direct computation above suffices.

**Remark 7.4: correct.** I checked arXiv:2102.01977, Theorem 3. The lower
bound is `c_d (1 - Lip(f)/L)^d/(1 + log2(eps0/eps))` times the integral, and
the upper bound is `C_d` times the integral. Assumption 4 holds for a cube.
Evaluating the integral by Lemma 2.2(i) with `a = d` and `lambda <= d/2` gives
exponent `d - lambda`, with log powers `theta - 2` to `theta - 1`.

### 2.6 Section 8: literature and novelty (claim 6)

**Checked directly:**
- Lin, Drton–Plummer, Bachoc–Cesari–Gerchinovitz and Bubeck et al. (above).
- Kannan–Barton 2017, from the repository's full text
  `literature/papers/kannan2017-the-cluster-problem-in-constrained`.

**Searches (2026-09-29):**
- "near-optimality dimension" with "log canonical threshold", "Newton
  polyhedron" or "learning coefficient";
- Lipschitz bandit or global optimization with "real log canonical threshold";
- branch-and-bound "cluster problem" with degenerate minimum, Łojasiewicz,
  Newton polyhedron or "log canonical".

None found a paper that links node, bandit or certified complexity to RLCTs or
Newton polyhedra. For Potfer–Perchet (arXiv:2605.29748), a summarizer reading of
the HTML reported no mention of analytic functions, Łojasiewicz exponents,
RLCTs or Newton polyhedra. I did not read the full text.

**Qualifications I recommend:**
- **(m8)** Kannan–Barton 2017 is a precedent for the face mechanism, not only
  for the order-`k` hierarchy. Their Lemma 10 and Corollary 4 show that when
  `f` grows linearly along `grad f(x*)` at a constrained minimizer, the
  fixed-width cluster estimate drops from `n_x` to `n_x - 1` dimensions. That
  is the mechanism of Example 4.3, in upper-estimate, fixed-width form. [CN]
  cites Kannan–Barton for the linear-growth case in Section 7.1, after Theorem
  7.1, and for the infeasible-side mechanism. The note's table cites them only
  for Remark 4, item 3.
- The RLCT step (Section 4) evaluates known integral characterizations (CN,
  Theorems 3.1 and 3.5; BCG Theorem 3) with standard Laplace/Mellin
  asymptotics. The note says so ("modest"), and I agree. The main new
  technical content is Lemma 3.2 and Theorem 3.3, the face projection that
  removes (QD). F1 strengthens it further.
- Random-search folklore relates the level-set exponent
  `P(f(X) - f* <= t) ~ c t^alpha` to complexity (Zhigljavsky; extreme-value
  estimation of `alpha`). For analytic `f`, `alpha` is the RLCT. The note
  lists this as not examined. That is acceptable, but the novelty sentence for
  "the RLCT form" should say that the identification of volume exponents with
  RLCTs is classical (Watanabe; Arnold–Gusein-Zade–Varchenko). Only its
  insertion into node-count characterizations is claimed.

## 3. Minor corrections

- (m1) Proposition 3.6: set `t_0 = min(M r^2/2, s0^2/4)`.
- (m2) Corollary 3.4: say that `C_0` depends on `s0` and on `min m(v)` over
  non-optimal vertices, together with `n, alpha', M`.
- (m3) Proposition 7.2(c): the integral form for `k < 2` is proved only under
  (A2). For `C^{1,1}` `m` state only the upper bound.
- (m4) Lemma 2.3(b): cite Lin, Theorem 1.3 (sos-nondegenerate case) with
  Propositions 4.3 and 4.5(3), instead of Theorems 4.8–4.9.
- (m5) Proposition 7.3(c): `y^2` is not covered by 7.3(b) verbatim; cite the
  direct computation.
- (m6) Proposition 6.2: add `delta_0 < 1` and `eps_0 < 1`, or write
  `1 + log(...)`.
- (m7) Summary item 4 inherits F2: add "at interior zeros".
- (m8) Section 8: add Kannan–Barton 2017, Lemma 10 and Corollary 4.

## 4. What I checked myself and what I took on trust

**Checked myself:**
- Every step of Theorem 3.1, Lemma 3.2, Theorem 3.3, Corollary 3.4, Lemma 3.5,
  Proposition 3.6, Lemma 2.2, Lemma 2.4, Theorem 4.1, Corollary 4.2, Example 4.3,
  Proposition 6.2, Theorem 7.1, Propositions 7.2 and 7.3, and Remark 7.4.
- The hypotheses and statements of Lin's results used in Lemmas 2.1 and 2.3,
  against the arXiv text.
- The RLCTs, multiplicities and leading constants of the Section 5 examples.
- The Drton–Plummer table.
- Bubeck et al. Example 3 and BCG Theorem 3.
- Exact reproduction of 111 bisection runs.
- F1–F4, analytically and numerically.

**Taken on trust:**
- The rigour of Lin's Theorem 2.10 and Theorem 1.3 as published. For the
  former, only the chart-decomposition route the note mentions.
- Aoyagi–Watanabe's formula itself (not read). The `r = H` rows at the box
  boundary.
- The completeness of the literature search. No search establishes novelty.
- The full texts of the 2026 arXiv papers (not read).

## 5. Commands run

These are targeted checks only. No project-wide verification was run and CI
was not inspected. All referee scripts are in
`research-20260929/reviews/rlct-review-checks/`, and were run from that
directory.

- `curl -sL -o lin.pdf https://arxiv.org/pdf/1003.5338 && pdftotext -layout lin.pdf lin.txt`,
  and the same for `2102.01977` (BCG), `1309.0911` (Drton–Plummer) and
  `1001.4475` (Bubeck et al.), in `/tmp/rlctrev`. Then `sed` and `grep` on the
  text.
- `python3 indep_bisect.py sep24` → 37/37 leaf counts match the note.
- `python3 indep_bisect.py bdry` → 45/45 match.
- `python3 indep_bisect.py xy2` → 29/29 match.
  - All three outputs are in `logs/indep_bisect_vs_note.log`.
- `python3 indep_bisect.py vertex_sharp_a8 2 30` and
  `python3 indep_bisect.py vertex_flat 2 30` → `logs/vertex_tests.jsonl` (F1).
- `python3 indep_bisect.py face4d 2 14`, then `python3 face4d_analyze.py`
  → `logs/face4d.jsonl`, `logs/face4d.log` (F3).
- `python3 constants_check.py` → `logs/constants_check.log`. It covers:
  - `A_cusp`, and the cusp `V/t^(5/12)`;
  - the closed-form `x^2 y^2` volume;
  - `xy + x^3 + y^3` and its edges (F4);
  - `(x+y)^2 + (x-y)^4` (F2);
  - the Hessian thresholds.
- `python3 lemma32_random.py` → `logs/lemma32_random.log` (maximum ratio 0.66).
- The note's own logs were read, not regenerated: `analyze_sweep.log`,
  `integrals.log`, `fit_constants.log`, `order_k_counts.log`,
  `check_rrr_formula.log`, `check_node_bounds.log`.

These floating-point checks illustrate the claims. They are not certified
counts.
