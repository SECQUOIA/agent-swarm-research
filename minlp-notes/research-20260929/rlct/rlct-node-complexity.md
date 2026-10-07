# Real log canonical thresholds and the node complexity of spatial branch-and-bound

Date: 2026-09-29. Status: revised after an independent review
([`reviews/rlct-review.md`](../reviews/rlct-review.md)) and a recheck of the
revision ([`reviews/rlct-recheck.md`](../reviews/rlct-recheck.md)). A second
recheck ([`reviews/rlct-recheck2.md`](../reviews/rlct-recheck2.md)) found the
second-round edits (Section 11.1) correct and raised four wording points
(W1–W4) and two optional clarifications, which the root applied on
2026-09-30 (Section 11.2, not rechecked). Section 11
lists all changes. Builds on the constrained
note [`research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`](../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md),
cited below as **[CN]** with its numbering (for example [CN, Theorem 3.1]).
Computations are floating-point illustrations, not certified counts. Scripts
and logs are in this directory.

## Summary

**Question.** For `f` real analytic near the box `X0` and `m = f - f* >= 0`
on `X0`, let `(lambda, theta)` be the real log canonical threshold (RLCT) of
`m` on `X0` and its multiplicity, so that
`vol{y in X0 : m(y) <= t} ~ c t^lambda (log 1/t)^(theta-1)`. The conjecture
was: under (G^pt_alpha) and (U^q_alpha'),
`N_opt(eps) = Theta(eps^(lambda - n/2) (log 1/eps)^(theta-1))` when
`lambda < n/2`.

**Answer.**

1. **True for interior minimizers, and more generally when `m >= 0` on a
   neighbourhood of `X0`** (Corollary 4.2). Then
   `N_opt(eps) ≍ |T_bis| ≍ eps^(lambda-n/2) (log 1/eps)^(theta-1)` for
   `lambda < n/2`, where `T_bis` is uniform dyadic bisection. Bisection pays
   **no extra log factor**. With interior minimizers the leading constants are
   explicit:
   `(alpha n/pi^2)^(n/2) L(eps)(1+o(1)) <= N_opt <= |T_bis| <= 2·12^n Lambda_2^(n/2) L(eps)(1+o(1))`,
   with `L(eps) = c_V Gamma(1+lambda) Gamma(n/2-lambda)/Gamma(n/2) · eps^(lambda-n/2) (log 1/eps)^(theta-1)`.
   Here `c_V` is the volume constant above and `Lambda_2` depends only on
   `n`, `alpha'` and the Hessian bound of `f`.
2. **The case `lambda = n/2`.** With interior minimizers, `lambda <= n/2`
   always. Equality holds exactly when all minimizers are nondegenerate (so
   finitely many), and then `theta = 1` and
   `N_opt ≍ |T_bis| ≍ log(1/eps)` (Lemma 2.4). The integral has the explicit
   asymptotic `sum_k (2 pi)^(n/2) det(H_k)^(-1/2) log(1/eps)/Gamma(n/2)`.
   On a face `F` of the box (item 3), `lambda_F = d/2` with `theta_F >= 2`
   can occur, for example `xy + x^3 + y^3` at a corner of a 2-face, where
   `V(t) ~ (1/3) t log(1/t)`. But there the edges carry `x^3` and give the
   larger count `eps^(-1/6)`. We know no instance in which such a face
   governs the count (Remark 4.1a).
3. **False in general for minimizers on the boundary.** For
   `m = x(1-x) + y^4 + z^4 + w^4` on `[0,0.9] x [-0.4,0.5]^3`, the RLCT on
   `X0` is `(7/4, 1)`, with `7/4 < n/2 = 2`. The conjecture predicts
   `eps^(-1/4)`, but `N_opt ≍ |T_bis| ≍ eps^(-3/4)`, carried by the face
   `x = 0` (Example 4.3). The corrected statement
   replaces the single RLCT by the **maximum over the faces of the box** of
   `eps^(lambda_F - d_F/2) (log 1/eps)^(theta_F - 1)`. Here
   `(lambda_F, theta_F)` is the RLCT of `m` restricted to the face `F` of dimension
   `d_F` (Theorem 4.1). This rests on a new box-face characterization
   (Corollary 3.4), valid for every `C^{1,1}` objective with no analyticity:
   `max(1, max_F I_F(eps)) ≲ N_opt ≤ |T_bis| ≲ 1 + sum_F I_F(eps)`,
   with `I_F(eps) = integral_F (m+eps)^(-d_F/2)`. So bisection is within a
   factor of `N_opt` that does not depend on `eps`, with no log loss even at
   minimizers at vertices of the box. The factor depends on the instance:
   on `n`, `alpha`, `alpha'`, the Hessian bound `M`, the side `s0`, and the
   smallest value of `m` at non-optimal vertices of the box. The upper bound needs no quadratic-doubling (QD)
   condition. It uses a one-sided gradient inequality that holds on the
   closed box (Lemma 3.2).
4. **Newton polyhedra (Section 5).** Let `l` be the Newton distance of `m`
   at a zero `z in int X0`, in any analytic coordinates. The local RLCT at `z`
   is at most `1/l`, with equality when every compact-face polynomial is
   positive on the torus (Lin 2017, Theorem 1.3 with Propositions 4.3 and
   4.5; Varchenko 1976). The global `lambda` is the minimum of the local
   values, so the node exponent is at least `n/2 - 1/l`. At a zero on `∂X0`
   the bound is guaranteed only in coordinates in which the box is locally a
   union of coordinate orthants (Lemma 2.3(a)); in other coordinates it can
   fail. Worked examples:

   | `m` | RLCT | node exponent |
   |---|---|---|
   | `x^2 y^2` | `(1/2, 2)` | `eps^(-1/2) log(1/eps)` |
   | `(x^2 - y^3)^2` | `(5/12, 1)` | `eps^(-7/12)`: the cusp adds `1/12` to the curve's `1/2` |
   | `x^2 y^2 + z^4` | `(3/4, 2)` | `eps^(-3/4) log(1/eps)` |
   | `x^2 + y^4` | `(3/4, 1)` | `eps^(-1/4)`: the separable row of [CN, 3.8] |

   In bisection runs, the fitted slopes (after dividing by the predicted log
   factor) match these exponents to within 0.021, and the ratio of leaves to
   the proved lower bound varies by at most a factor 2.2 over 5–11 decades.
   Fits of the integrals reproduce the predicted leading constants to 3–5
   significant digits.
5. **Singular learning theory (Section 6).** Take exact-data least squares
   for reduced-rank regression with true rank 0, over a box containing the
   origin. The node exponent is `n/2 - lambda`, with `lambda` the
   Aoyagi–Watanabe learning coefficient. For example, it is `15/2` for
   `N = 5` responses, `M = 3` covariates and model rank 3 (`n = 24`). For
   the scalar toy `m = S(ab - delta)^2`,
   `N_opt ≍ |T_bis| ≍ eps^(-1/2) (1 + log(1/max(eps, delta^2)))` uniformly in
   `delta`. The log factor, caused by the singularity, freezes below the
   noise scale. The general noisy two-regime picture is a sketch only.
6. **Higher-order relaxations (Section 7).** With a gap of order `k`, the
   covering scale is `(eps + eta)^(1/k)`. Theorem 7.1 proves the analogue of
   [CN, Theorem 6.3]. Sublevel sets are fat at scale `eta^(1/2)`, but not at
   `eta^(1/k)` for `k > 2`.
   - For `k <= 2`, the exponent is `n/k - lambda` (the volume law).
   - For `k > 2`, the exponent is only bounded between `(n/k - lambda)_+` and
     `(n - 2 lambda)/k`, and it is **not** a function of `(lambda, theta)`:
     `y^2` and `x^4 + y^4` both have `lambda = 1/2`, but exponents `1/3` and
     `1/6` at `k = 3`.
   - At an isolated minimizer with growth order `q`, order `k >= q` removes
     the polynomial growth. For `k >= 2`, a Morse–Bott set of dimension `p`
     gives `Theta(eps^(-p/k))`.

   The "order `k >= q` suffices" part is essentially in Kannan–Barton (2017,
   Remark 4, item 3) and in Du–Kearfott (1994, Remark 2), as sufficient
   conditions.
   The homogeneous formula `n(1/k - 1/q)_+` is Bubeck et al. (2011,
   Example 3).
7. **Literature (Section 8).** No source was found that links
   branch-and-bound, Lipschitz or bandit complexity to RLCTs or Newton
   polyhedra. The closest are:
   - Neumaier (2004, Section 15), whose volume heuristic, fed with the RLCT,
     gives the `k = 2` exponent;
   - Bachoc–Cesari–Gerchinovitz (2021), whose integral, evaluated by Lemma 2.2,
     gives exponent `n - lambda` for certified Lipschitz optimization of
     analytic functions (Remark 7.4);
   - singular-learning-theory work on volume scaling (Lau et al.).

   An unsuccessful search does not establish novelty.

### Status

| Item | Content | Status |
|---|---|---|
| Lemma 2.1 | Laplace and volume asymptotics on compact semianalytic sets | cited (Lin 2017, Cor. 2.6, Thm 2.10; Karamata), hypotheses checked for box faces |
| Lemma 2.2 | `integral (m+eps)^(-a)` from the RLCT, all three regimes | proved |
| Lemma 2.3 | Newton-polyhedron bound, and equality for nonnegative `m` | cited (Lin 2017, Theorem 1.3, Propositions 3.4, 4.3, 4.5); positivity reformulation and the orthant case at boundary zeros proved; recheck confirmed; second-round clarifications (sign conditions, squares) checked in `reviews/rlct-recheck2.md` |
| Lemma 2.4 | interior case: `lambda <= n/2`, equality iff nondegenerate, then `theta = 1` | proved |
| Theorem 3.1 | face lower bound `(alpha d/pi^2)^(d/2) I_F(eps)` | proved |
| Lemma 3.2, Theorem 3.3 | projection to a face; bisection bound without (QD) | proved. Lemma 3.2 was review-confirmed. Theorem 3.3 was review-confirmed in its earlier form and restated per F1; the recheck confirmed the restated form; the added `N_v <= J_v` step was checked in `reviews/rlct-recheck2.md` |
| Lemma 3.3a | optimal vertices add no log factor | proved in the revision (argument from review item F1); recheck confirmed |
| Corollary 3.4 | two-sided box-face characterization (`C^{1,1}`), no vertex term | proved; vertex term removed in the revision; recheck confirmed the constants |
| Lemma 3.5 | (QD) holds for interior minimizers; [CN, Lemma 3.6] needs `m >= 0` beyond `X0` | proved |
| Proposition 3.6 | faces are dominated when `m >= 0` near `X0` | proved |
| Theorem 4.1, Corollary 4.2 | RLCT form; the conjecture under (i) or (ii) | proved (given Lemma 2.1). Corollary 4.2 was review-confirmed. Theorem 4.1 was review-confirmed in its earlier form and restated without the vertex term; the recheck confirmed the restated form |
| Remark 4.1a | `lambda_F = d/2`, `theta_F >= 2` faces | open: no governing instance known. The relative-interior case is proved; the Newton-nondegenerate corner case is only sketched |
| Example 4.3 | literal counterexample (`lambda = 7/4 < n/2 = 2`); 2D illustration | proved; numerics agree (counterexample adopted from the review and re-verified) |
| Section 5 examples | four RLCTs and exponents | proved; numerics agree |
| Proposition 6.1 | reduced-rank regression, true rank 0 | proved, with `lambda` taken from Aoyagi–Watanabe as reported by Drton–Plummer |
| Proposition 6.2 | noisy scalar toy, uniform in `delta` | proved; numerics agree |
| Conjecture 6.3 | general noisy two-regime behaviour | sketch |
| Theorem 7.1 | order-`k` covering law | proved |
| Proposition 7.2 | fatness; exponent bounds; volume law for `k <= 2` | proved; for `k < 2` the two-sided integral form needs (A2) |
| Proposition 7.3 | isolated (Łojasiewicz) and Morse–Bott formulas for order `k` | proved (Morse–Bott part as a sketch reusing [CN, Theorem 7.2]) |
| Remark 7.4 | Bachoc et al. integral in RLCT form | proved (evaluation of their integral) |

## 1. Setting

As in [CN, Sections 1 and 3], unconstrained: the feasible set is `X0`.
- `X0` is a cube of side `s0`.
- `m = f - f*`, with `f* = min_{X0} f`, so `m >= 0` on `X0`.
- `E(t) = {y in X0 : m(y) <= t}` and `V(t) = vol E(t)`.
- A **face** `F` of `X0` of dimension `d` fixes `n - d` coordinates at bounds:
  `F = {y in X0 : y_i = b_i, i in I}`, with `b_i in {L_i, U_i}` and
  `|I| = n - d`. `X0` itself is a face (`d = n`), and there are `3^n` faces.
  `sigma` is `d`-dimensional Lebesgue measure on `F`, and
  `I_F(eps) = integral_F (m + eps)^(-d/2) dsigma`.
- Hypotheses on the relaxation: (G^pt_alpha) or (G^LB_alpha), and
  (U^q_alpha'), exactly as in [CN, Section 1.4]. Exact alphaBB,
  `f_B = f - alpha q_B` with `alpha` at least half the most negative Hessian
  eigenvalue, satisfies both with `alpha' = alpha`.
- `N_opt(eps)` is the least size of a certificate. `T_bis` is the uniform
  `2^n`-ary dyadic refinement with `UBD = f*`. Level `j` has cubes of side
  `s_j = s0 2^(-j)`, and `|T_bis| = 1 + 2^n #(non-pruned cubes)`
  [CN, Theorem 3.3].
- (A1) `grad f` is `M`-Lipschitz on `X0` in the Euclidean norm.
  (A2) `f` is real analytic on a neighbourhood of `X0`. (A2) implies (A1).
  Sections 3 and 7 use only (A1).

**RLCT.** For a compact semianalytic set `Omega` and a nonnegative real
analytic `h` with a zero in `Omega`, `RLCT_Omega(h) = (lambda, theta)`
denotes the smallest pole and its order of `zeta(z) = integral_Omega h^(-z)`.
This is Lin's convention (Lin 2017, Section 2). Pairs are ordered so that
`(lambda1, theta1) < (lambda2, theta2)` if `lambda1 < lambda2`, or
`lambda1 = lambda2` and `theta1 > theta2`; smaller means more singular. If
`h ≡ 0` on `Omega`, set `(lambda, theta) = (0, 1)`. If `h > 0` on `Omega`,
set `lambda = inf`.

## 2. Analytic input

**Lemma 2.1 (asymptotics on compact semianalytic sets).** Let
`Omega = {x in R^d : g_1(x) >= 0, ..., g_l(x) >= 0}` be compact, with `g_i`
nonconstant and real analytic. Let `h` be nonconstant and real analytic on a
neighbourhood of `Omega`, with `h >= 0` on `Omega` and `h(x0) = 0` for some
`x0 in Omega`. Let `(lambda, theta) = RLCT_Omega(h)`. Then:

(a) `zeta` continues meromorphically to `C`. Its poles are positive
rationals, so `(lambda, theta)` exists (Lin 2017, Corollary 2.6).

(b) `Z(N) = integral_Omega e^(-N h) = c_Z N^(-lambda) (log N)^(theta-1) (1 + o(1))`
as `N -> inf`, with `c_Z > 0` (Lin 2017, Theorem 2.10). The leading
coefficient is `(-1)^theta Gamma(lambda) d_{lambda,theta}/(theta-1)!` by
Lin's formula (12), where `d_{lambda,theta} != 0` is the top Laurent
coefficient. It is positive because `Z > 0`.

(c) `V_h(t) = vol{x in Omega : h(x) <= t} = c_V t^lambda (log 1/t)^(theta-1) (1 + o(1))`
with `c_V = c_Z/Gamma(1+lambda)`. This follows from (b), since
`Z(N) = integral_0^inf e^(-Nt) dV_h(t)` and `V_h` is nondecreasing, by
Karamata's Tauberian theorem at the origin (Bingham–Goldie–Teugels,
*Regular Variation*, 1987, Section 1.7, Theorem 1.7.1 and its version at 0).

(d) `RLCT_Omega(h) = min_{x in Omega} RLCT_{Omega_x}(h)` over small
neighbourhoods `Omega_x` of `x` in `Omega`, and only zeros of `h` matter
(Lin 2017, Propositions 2.5 and 3.2(c)). At a boundary point the local value
depends on `Omega` (Lin, Example 2.8: `xy^2` has threshold `2/3` or `1/2` on
the two halves of a corner). It is at least the value on a full
neighbourhood (Lin, Proposition 3.3).

(e) If `c1 h <= h' <= c2 h` on `Omega`, then `RLCT(h) = RLCT(h')` (Lin,
Corollary 3.5). If `h = sum_i g_i^2` and the ideal `<g_1, ..., g_r>` has
RLCT `(lambda_I, theta)`, then `RLCT(h) = (lambda_I/2, theta)` (Lin,
remark after Corollary 3.5). For ideals in disjoint variables,
`RLCT(I_X + I_Y) = (lambda_X + lambda_Y, theta_X + theta_Y - 1)` (Lin,
Proposition 3.7).

*Hypotheses checked for the use below.*
- Each face `F` of `X0`, in its own `d` coordinates, is
  `{y : y_i - L_i >= 0, U_i - y_i >= 0}`. It is compact and semianalytic, with
  nonconstant affine `g_i`.
- `m|_F` is real analytic on a neighbourhood of `F` in its affine hull,
  because `f` is analytic near `X0`.
- Minimizers on the boundary are allowed. The simultaneous resolution of `h`
  and the `g_i` (Lin, Lemma 2.4) handles the boundary.

So the box boundary is covered. What changes at boundary minimizers is not
the asymptotics of the `n`-dimensional integral, but which integral governs
the node count (Sections 3–4). Lin's Theorem 2.10 derives (b) through a
Mellin inversion. The same leading term follows from his Lemma 2.4 chart
decomposition, because on each orthant chart the integrand is a monomial
times functions bounded above and below. That suffices for all two-sided
(`≍`) statements below. Exact constants use (b) as stated.

**Lemma 2.2 (the node integral from the RLCT).** In the setting of Lemma
2.1, let `a > 0` and `I_a(eps) = integral_Omega (h + eps)^(-a)`. As
`eps -> 0`:

(i) if `a > lambda`, `I_a(eps) = c_Z Gamma(a - lambda)/Gamma(a) · eps^(lambda - a) (log 1/eps)^(theta-1) (1 + o(1))`;

(ii) if `a = lambda`, `I_a(eps) = c_Z/(theta Gamma(a)) · (log 1/eps)^theta (1 + o(1))`;

(iii) if `a < lambda`, `I_a(0) = integral_Omega h^(-a) < inf` and `I_a(eps)` increases to it.

In (i), `c_Z Gamma(a-lambda)/Gamma(a) = c_V Gamma(1+lambda) Gamma(a-lambda)/Gamma(a)`.

*Proof.* The Gamma integral `(h + eps)^(-a) = Gamma(a)^(-1) integral_0^inf s^(a-1) e^(-s(h+eps)) ds`
and Tonelli give

```
I_a(eps) = Gamma(a)^(-1) integral_0^inf s^(a-1) e^(-s eps) Z(s) ds.
```

By Lemma 2.1(b) and `Z <= vol(Omega)`, there is `C` with
`Z(s) <= C s^(-lambda) (1 + log(2+s))^(theta-1)` for all `s > 0`.

(i) Substitute `s = u/eps`:
`I_a = Gamma(a)^(-1) eps^(-a) integral_0^inf u^(a-1) e^(-u) Z(u/eps) du`.
- For fixed `u > 0`,
  `Z(u/eps)/(c_Z eps^lambda u^(-lambda) (log 1/eps)^(theta-1)) -> 1`,
  because `log(u/eps)/log(1/eps) -> 1`.
- For `eps <= 1/e`, `2 + u/eps <= (2+u)/eps`, so
  `log(2 + u/eps) <= log(1/eps)(1 + log(2+u))`. The ratio is therefore at
  most `(C/c_Z)(2 + log(2+u))^(theta-1)`.
- The dominating function `u^(a-lambda-1) e^(-u) (2 + log(2+u))^(theta-1)`
  is integrable because `a > lambda`.

Dominated convergence gives `integral u^(a-lambda-1) e^(-u) du = Gamma(a - lambda)`.

(ii) The part `s <= S` is bounded. For `s >= S(delta)`,
`Z(s) = c_Z s^(-a) (log s)^(theta-1)(1 + r(s))` with `|r| <= delta`. It
remains to show
`integral_S^inf s^(-1) (log s)^(theta-1) e^(-s eps) ds = (log 1/eps)^theta/theta (1 + o(1))`.
- On `[S, 1/(K eps)]` the factor `e^(-s eps)` lies in `[e^(-1/K), 1]`.
- On `[K/eps, inf)` the integral is `O(e^(-K) (log 1/eps)^(theta-1))`.
- The middle part `[1/(K eps), K/eps]` contributes
  `O(log K (log 1/eps)^(theta-1))`.

Let `eps -> 0`, then `K -> inf` and `delta -> 0`.

(iii) `integral_Omega h^(-a) = Gamma(a)^(-1) integral_0^inf s^(a-1) Z(s) ds < inf`,
because `s^(a-1-lambda)(log s)^(theta-1)` is integrable at infinity.
Monotone convergence gives the rest. □

This is the only place where analyticity enters. Everything in Sections 3
and 7 is about `C^{1,1}` functions and integrals like `I_a`.

**Lemma 2.3 (Newton polyhedra).** Let `h` be real analytic near
`0 in R^n` with `h(0) = 0`. Its RLCTs are those of `|h|`, which is Lin's
convention for the ideal `<h>`. Sign conditions are stated where they are
used:
- (a) needs none;
- the boundary-zero consequence of (a) is stated for `h >= 0` on `X0` near
  the zero (the argument does not use the sign);
- (b) is stated for `h >= 0` on a full neighbourhood of 0 (the cited route
  needs only that each compact-face polynomial has no zero on the torus).

In given analytic coordinates:
- `P(h)` is the Newton polyhedron (convex hull of `alpha + R^n_{>=0}` over
  the exponents `alpha` present in `h`);
- `l` is the Newton distance, the least `t` with `(t, ..., t) in P(h)`;
- `theta_l` is the codimension of the smallest face of `P(h)` that contains
  `(l, ..., l)`.

Then:

(a) `RLCT_0(h) <= (1/l, theta_l)` in the order above. In particular
`lambda_0 <= 1/l` (Lin 2017, Theorem 1.3 for the ideal `<h>`, whose Newton
polyhedron is `P(h)` and whose RLCT is that of `|h|`). This bounds the RLCT
on a **full** neighbourhood of 0.

*Consequence for the node exponent.* The global `lambda` is at most each
box-restricted local RLCT (Lemma 2.1(d)). At a zero `z in int X0` the
box-restricted and full-neighbourhood values agree, so the exponent
`n/2 - lambda` of Corollary 4.2 is at least `n/2 - 1/l`, for `l` computed in
any analytic coordinates at `z`. At a zero `z in ∂X0` the box-restricted
value can be larger (Lin, Proposition 3.3), and the bound can fail. Example:
`m = (x+y)^2 + (x-y)^4` on `[0,1]^2`. In the coordinates `u = x+y`,
`v = x-y`, `m = u^2 + v^4`, so `1/l = 3/4`. But the box is
`{u >= |v|}` near 0, `V(t) = t/2 (1 + o(1))`, and the box RLCT is `(1, 1)`
(`logs/revision_checks.log`). The count is `log(1/eps)`, not
`eps^(-1/4)`. The bound does hold at `z in ∂X0` in analytic coordinates `omega`
centred at `z` in which `X0` is, near `z`, a union of closed coordinate
orthants (for example, the box coordinates), provided `h >= 0` on `X0` near
`z`. The function need not be nonnegative outside `X0`; in Example 4.3,
`m < 0` for `x < 0`. The argument:
- Lin's Lemma 4.1 gives `|h| <= c sum_{alpha in S} |omega^alpha|` on a small
  closed cube `W` centred at `z`, where the `omega^alpha` generate the monomial
  ideal of `h`. By Cauchy–Schwarz,
  `h^2 <= c' g` with `g = sum_{alpha in S} omega^(2 alpha)`. Both `h^2` and
  `g` are analytic.
- `g` is even in every coordinate, so its zeta integral over a union of `k`
  orthants of `W` is `k 2^(-n)` times the integral over `W`. Its RLCT on
  `Omega = X0 ∩ W` therefore equals that on `W`, which is `(1/(2l), theta_l)`.
  This uses Lin's Theorem 1.3 with equality for the monomial ideal
  (Proposition 4.12), whose polyhedron is `P(h)`, and the halving of
  Lemma 2.1(e).
- Lin's Proposition 3.4 on `Omega` gives
  `RLCT_Omega(h^2) <= (1/(2l), theta_l)`. Since
  `RLCT_Omega(h^2) = (lambda_z/2, theta_z)`, where `(lambda_z, theta_z)` is
  the box-restricted RLCT of `h` at `z`, this gives
  `(lambda_z, theta_z) <= (1/l, theta_l)`.

(b) Equality `RLCT_0(h) = (1/l, theta_l)` holds if `h_gamma > 0` on the torus
`(R \ {0})^n` for every compact face `gamma` of `P(h)`, where
`h_gamma = sum_{alpha in gamma} c_alpha y^alpha`. Citation route: by Lin's
Propositions 4.3 and 4.5(3), this condition says exactly that the ideal
`<h>` is sos-nondegenerate. Lin's Theorem 1.3 then gives equality for `<h>`,
whose RLCT is that of `h`. The underlying toric computation is Varchenko's
(1976; Arnold–Gusein-Zade–Varchenko, Vol. II, Section 8.3). For nonnegative
`h`, positivity is also equivalent to Lin's nondegeneracy ("`h_gamma` has no
singular point in the torus"):
- `h_gamma(y) = lim_{s -> 0} s^(-<beta, alpha_gamma>) h(s^beta_1 y_1, ..., s^beta_n y_n)`
  for `beta` in the interior of the normal cone of `gamma`, so `h_gamma >= 0`;
- a zero of a nonnegative polynomial is a critical point, hence a singular
  point.

If `h = sum g_i^2` and the ideal `<g_i>` is sos-nondegenerate (Lin,
Proposition 4.5(3)), then `RLCT_0(h) = (1/(2 l_I), theta)` with `l_I` the
distance of `P(<g_i>)` (Lin, Theorem 1.3 and Lemma 2.1(e)). Monomial ideals
are sos-nondegenerate (Lin, Proposition 4.12).

*Remark (why nonnegativity matters, and why we do not cite Lin's Theorems
4.8–4.9 directly).* Lin's Theorems 4.8–4.9, read literally for sign-changing
functions, would give `RLCT_0(x + y) = (2, 1)`, since
`l = 1/2`. The true value is `(1, 1)`, because `x + y` is a smooth
coordinate. The strict transform of `{x + y = 0}` meets the exceptional
fibre of the toric modification and contributes the candidate pole `1`.
Varchenko's oscillatory-integral theorem assumes `l > 1`, which excludes
this case. For nonnegative `h`
with positive compact-face polynomials, every point of the fibre
`rho^(-1)(0)` lies on divisors of compact faces, where `h_gamma > 0`. So
`h∘rho` is a monomial times a unit near the fibre, and the issue does not
arise. We use Lemma 2.3(b) only for functions that are nonnegative near
the zero.

**Lemma 2.4 (interior minimizers).** Assume (A2) and that every global
minimizer lies in `int X0`. Let `(lambda, theta) = RLCT_{X0}(m)`. Then
`lambda <= n/2`. Moreover `lambda = n/2` iff every minimizer has a
nonsingular Hessian. In that case the minimizers are finitely many,
`theta = 1`, and `c_Z = sum_k (2 pi)^(n/2) det(H_k)^(-1/2)`.

*Proof.* Let `y0` be a minimizer, so `grad m(y0) = 0` and
`H = hess m(y0) >= 0`.
- Taylor's theorem gives `m(y0 + h) <= C|h|^2` near 0, so
  `V(t) >= c t^(n/2)`. Since `Z(N) >= e^(-1) V(1/N)`, Lemma 2.1(b) gives
  `lambda <= n/2`. The same inequality is used in the next step.
- Suppose `Hv = 0` with `|v| = 1`. Write `h = w + s v` with `w ⊥ v`. Then
  `m(y0 + h) = (1/2) w^T H w + O(|h|^3) <= C(|w|^2 + |s|^3)`. So `E(t)`
  contains `{|w| <= c t^(1/2), |s| <= c t^(1/3)}`,
  `V(t) >= c t^((n-1)/2 + 1/3)` and `lambda < n/2`.
- A non-isolated minimizer is degenerate: a limit direction of nearby
  minimizers is in the kernel. So if all Hessians are nonsingular, the
  minimizers are isolated, and finitely many by compactness.
- The Laplace method then gives
  `Z(N) = sum_k (2 pi/N)^(n/2) det(H_k)^(-1/2) (1 + o(1))`. □

## 3. A box-face characterization for `C^{1,1}` objectives

**Theorem 3.1 (face lower bound).** Let `P` be `alpha`-valid on `X0`. Examples
are any certificate under (G^LB_alpha), or the leaf-and-piece family of any
run in [CN, Lemma 2.1] under (G^pt_alpha). Then for every face `F` of
dimension `d >= 1` and every `eps > 0`,

```
|P| >= (alpha d/pi^2)^(d/2) I_F(eps).
```

*Proof.* Let `C = prod [l_i, u_i] in P` meet `F`. For `i in I`, the bound
`b_i` is an endpoint of `[L_i, U_i]` and lies in `[l_i, u_i]`, so it is an
endpoint of `[l_i, u_i]`. Hence `a_i^C(y) = 0` for `y in F ∩ C` and
`i in I`, and `q_C(y) = sum_{i notin I} a_i^C(y_i)`.
- (V) at `y in F ∩ C` gives
  `m(y) + eps >= alpha q_C(y) >= alpha d (prod_{i notin I} a_i^C)^(1/d)`.
- The set `F ∩ C = {b_I} x prod_{i notin I}[l_i, u_i]` is a product, so the
  arcsine integral [CN, Theorem 3.1, step 3] gives
  `integral_{F∩C} (m+eps)^(-d/2) <= (alpha d)^(-d/2) pi^d`.
- The sets `F ∩ C`, `C in P`, cover `F`. Sum over them. □

For `d = n` this is [CN, Theorem 3.1]. For lower-dimensional faces it is
[CN, Theorem 4.5(i)] for an affine coordinate stratum, with the better
constant `(alpha d/pi^2)^(d/2)` and a two-line proof.

**Lemma 3.2 (projection to a face, and fatness).** Assume (A1). Let
`0 < s <= s0/2` and `y in X0`.
- Let `I = {i : min(y_i - L_i, U_i - y_i) < s}`, and `b_i` the nearer
  endpoint for `i in I`.
- Let `F` be the face fixing `y_I = b_I`, of dimension `d = n - |I|`, and
  `y' = (b_I, y_{I^c})`.

Then `|y - y'|_inf < s`. The `d`-dimensional cube
`Q_F(y', s) = {z in F : |z - y'|_inf <= s}` lies in `F`, and on it

```
m(z) <= (1+d)(1+n-d) m(y) + [(1+d)(n-d) + d] M s^2 <= ((n+2)^2/4) (m(y) + M s^2).
```

*Proof.* The descent lemma
`m(b) <= m(a) + grad m(a)·(b-a) + (M/2)|b-a|^2` holds for `a, b in X0`,
because `X0` is convex. Only `m >= 0` **on `X0`** is used.

1. *One-sided derivative bound.* Let `i in I` with `y_i != b_i`, and
   `sigma = sign(b_i - y_i)`. The far endpoint is at distance at least
   `s0 - s >= s`, so `y - sigma s e_i in X0`. Then
   `0 <= m(y - sigma s e_i) <= m(y) - s sigma ∂_i m(y) + M s^2/2`, hence
   `sigma ∂_i m(y) <= m(y)/s + M s/2`.
2. *Move to the face.* The first-order term of `m(y') - m(y)` is
   `sum_{i in I} ∂_i m(y)(b_i - y_i) = sum_{i in I} sigma ∂_i m(y) |b_i - y_i|`.
   Each summand is at most `m(y) + M s^2/2` by step 1. With
   `|y' - y|_2^2 <= |I| s^2`, this gives
   `m(y') <= (1 + n - d) m(y) + (n - d) M s^2`.
3. *Fatness inside the face.* For `i notin I`, both `y' ± s e_i` lie in
   `X0`, so `|∂_i m(y')| <= m(y')/s + M s/2`. For `z in Q_F(y', s)`,
   `m(z) <= m(y') + d(m(y') + M s^2/2) + (M/2) d s^2 = (1+d) m(y') + d M s^2`.
4. Combine steps 2 and 3. Both coefficients are at most
   `(1+d)(1+n-d) <= ((n+2)/2)^2`. □

For `d = n` this is the fatness statement
`E(eta) + Q(0, c sqrt(eta/M)) ⊆ E(C eta)` at interior points. It is the
two-sided form of the gradient inequality `|grad m|^2 <= 2 M m`. Lemma 3.2
needs `m >= 0` only on `X0`. At boundary points it pays for the missing room
by moving to a face.

**Theorem 3.3 (bisection without a doubling condition).** Assume (A1) and
(U^q_alpha'). Put `Lambda_0 = alpha' n/4`,
`Lambda_1 = ((n+2)^2/4)(Lambda_0 + M)`, `Lambda_2 = Lambda_0 + Lambda_1`,
`J = #{j >= 0 : Lambda_0 s_j^2 > eps}` and
`J_v = #{j >= 1 : m(v) <= Lambda_1 s_j^2}` for a vertex `v`. For a vertex
`v`, let `N_v(eps)` be the number of levels `j >= 1` at which the level-`j`
cell with corner `v` is not pruned. Then `N_v(eps) <= min(J, J_v)`, and

```
|T_bis| <= 1 + 2^n + 2^n [ 2·6^n sum_{F : d >= 1} Lambda_2^(d/2) I_F(eps) + sum_{v vertex} N_v(eps) ].
```

*Proof of `N_v <= J_v`.* Suppose the corner cell at `v` is not pruned at
level `j`. Its witness `y` has `m(y) < Lambda_0 s_j^2` and
`|y - v|_inf <= s_j`. Apply steps 1–2 of Lemma 3.2 to all `n` coordinates,
moving `y` to `v`. This gives
`m(v) <= (1+n) m(y) + n M s_j^2 < ((1+n) Lambda_0 + n M) s_j^2 <= Lambda_1 s_j^2`.
So level `j` is counted in `J_v`, and it is `< J` because
`eps < Lambda_0 s_j^2`.

*Proof of the bound.* Let `D` be a non-pruned level-`j` cube with `j >= 1`.

1. As in [CN, Theorem 3.5, step 1], some `y in D` has
   `m(y) < Lambda_0 s_j^2 - eps`. Hence `eps < Lambda_0 s_j^2`.
2. Apply Lemma 3.2 with `s = s_j`. This gives a face `F` and a point `y'`
   with `|y - y'|_inf < s_j` and `Q_F(y', s_j) ⊆ F ∩ E(Lambda_1 s_j^2)`.
3. For each face `F`, let `Z` be a maximal subset of the points `y'` produced
   at level `j` with pairwise sup-distance `> s_j`.
   - For `d >= 1`, the cubes `Q_F(z, s_j/2)`, `z in Z`, have disjoint
     relative interiors and lie in `F ∩ E(Lambda_1 s_j^2)`. So
     `|Z| <= s_j^(-d) H^d(F ∩ E(Lambda_1 s_j^2))`.
   - For a vertex, `|Z| <= 1{m(v) <= Lambda_1 s_j^2}`.
4. For `d >= 1`, each `D` lies in `Q(z, 3 s_j)` for some `z in Z`, and such
   a cube contains at most `6^n` closed level-`j` cells. For a vertex `v`,
   the witness satisfies `|y - v|_inf < s_j`. Since `v` is a grid point, the
   only closed level-`j` cell containing `y` is the corner cell at `v`. So
   each level charges at most one cell to `v`, and only when the corner cell
   is not pruned.
5. Summing over `j` with `eps < Lambda_0 s_j^2`, use
   `E(Lambda_1 s_j^2) ⊆ {m + eps <= Lambda_2 s_j^2}` and the Fubini
   computation of [CN, Theorem 3.5, steps 3–4]:
   `sum_j s_j^(-d) H^d(F ∩ {m + eps <= Lambda_2 s_j^2}) <= 2 Lambda_2^(d/2) I_F(eps)`.
6. Level 0 has at most one cube, and `|T_bis| = 1 + 2^n #(non-pruned)`. □

**Lemma 3.3a (optimal vertices add no log factor).** The argument is from
review item F1. Assume (A1) with `M > 0` (increasing `M` loses nothing) and
(U^q_alpha'), and let `v` be a vertex with `m(v) = 0`.
- Let `g >= 0` be the smallest inward derivative of `m` at `v` along the `n`
  edges of `X0` at `v`, and `E` an edge attaining it.
- Put `rho = max(g/M, sqrt eps)`.

Then:

(a) the corner cell at `v` of side `s_j` is pruned whenever
`s_j <= g/(alpha' + M/2)`;

(b) `I_E(eps) >= (3M/2 + 1)^(-1/2) log(s0/rho)` when `rho <= s0`;

(c) `N_v(eps) <= 1 + c + (3M/2 + 1)^(1/2) I_E(eps)/log 2`, with
`c = max(0, log2 sqrt(Lambda_0), log2((alpha' + M/2)/M))`. This bound does
not depend on `g`.

*Proof.*
- (a) Use inward coordinates `t = y - v >= 0` on the corner cell `D`.
  - The descent lemma gives
    `m(y) >= g |t|_1 - (M/2)|t|_2^2 >= |t|_1 (g - M s_j/2)`, using
    `|t|_2^2 <= s_j |t|_1`.
  - Also `q_D(y) = sum t_i (s_j - t_i) <= s_j |t|_1`.
  - If `D` is not pruned, (U^q) gives some `y in D` with
    `m(y) < alpha' q_D(y) - eps`. Here `t != 0`, since `m(v) = 0`. Hence
    `g - M s_j/2 < alpha' s_j`.
- (b) Along `E`, `m(v + tau e) <= g tau + M tau^2/2 <= (3M/2) tau^2` for
  `tau >= g/M`. Also `eps <= tau^2` for `tau >= sqrt eps`. Integrate
  `(m + eps)^(-1/2) >= (3M/2 + 1)^(-1/2)/tau` over `[rho, s0]`.
- (c) By (a), `N_v <= 1 + log2(s0 (alpha' + M/2)/g)`. Always
  `N_v <= J <= 1 + log2(s0 sqrt(Lambda_0/eps))`. Taking the better of the two
  bounds gives `N_v <= 1 + c + log2(s0/rho)`. If `rho > s0` the last term is
  negative. Otherwise use (b). □

**Corollary 3.4 (two-sided characterization).** Under (A1), (G^LB_alpha)
and (U^q_alpha'), for all `eps > 0`,

```
max{ 1, max_{F: d>=1} (alpha d/pi^2)^(d/2) I_F(eps) }  <=  N_opt(eps)  <=  |T_bis|  <=  C_0 + C_1 sum_{F: d>=1} I_F(eps),
```

with:
- `C_1 = 2^n [ 2·6^n max(1, Lambda_2^(n/2)) + 2 (3M/2+1)^(1/2)/log 2 ]`. The
  factor 2 in the second term is there because an edge has two vertices;
- `C_0 = 1 + 2^n + 2^n [ sum_{v : m(v) > 0} J_v + (1 + c) #{optimal vertices} ]`.

`C_1` depends only on `n`, `alpha'` and `M`. `C_0` depends also on `s0` and,
through `J_v <= 1 + log2(s0 sqrt(Lambda_1/m(v)))`, on the values of `m` at
non-optimal vertices. Since there are `3^n` faces, it follows that
`N_opt ≍ |T_bis| ≍ max(1, max_F I_F(eps))`, with constants depending on
`n, alpha, alpha', M, s0` and `min{m(v) : m(v) > 0}`. There is no
`log(1/eps)` exception at vertex minimizers of `X0`.

The first version of this note kept a term `12^n J #{optimal vertices}` and
called it "real". That was wrong. [CN, Example 3.4] has a non-`C^1` minimizer
in the interior, and [CN, Remark 6.9] needs a coordinate in the middle part
of its dyadic cell. A vertex of `X0` is a vertex of every dyadic cell that
contains it. The log loss of bisection in [CN] remains for sharp minimizers
that are not vertices of the root box, which requires a nonsmooth objective
or constraints.

Numerically (`logs/revision_sweep.jsonl`):
- For `m = x + y - 0.4(x^2 + y^2)` on `[0,1]^2` (`g = 1`), bisection has 16
  leaves for every `eps` from `1e-2` to `1e-15` with `alpha = alpha' = 8`,
  and one leaf with `alpha = 1`. Lemma 3.3a(a) allows at most 4.07 and 1.49
  charged levels respectively.
- For `m = x - 0.4 x^2 + y^2` (`g = 0` along the edge `x = 0`, where
  `m = y^2`), the leaves grow like `log(1/eps)`: 7, 19, 28, 37, 49, 58, 73 at
  `eps = 1e-2, 1e-4, ..., 1e-12, 1e-15`. That log is already in
  `I_E(eps) ≍ log(1/eps)`.

Both runs reproduce the reviewer's independent counts exactly.

*Relation to [CN].* Corollary 3.4 is [CN, Theorem 6.7] for the stratification
of the box by its faces. But it needs neither (QD) nor [CN]'s (R2), which
fails along faces near sharp vertices. For example, along an edge where
`m = x + y`, `m(0,h+s) = h + s` is not `<= K(h + s^2)` uniformly.

**Lemma 3.5 ((QD) at interior minimizers).** [CN, Lemma 3.6] requires `m >= 0`
on `X0 + B(0, G/M)`. That fails whenever `f` drops below `f*` just outside
`X0`, which is typical when the box constraint is not artificial. A local
version holds.
- Assume (A1), and that the minimizer set `M*` lies in `int X0` at distance
  `delta` from `∂X0`.
- Let `c_0 = min{m(y) : dist(y, M*) >= delta/2} > 0`,
  `m_max = max m` and `D = diam X0`.

Then (QD) `m(x) <= K(m(y) + |x-y|_inf^2)` holds with
`K = max(m_max/c_0, 2 + 4D/delta, nM)`.

*Proof.* If `m(y) >= c_0`, then `m(x) <= (m_max/c_0) m(y)`. Otherwise
`B(y, delta/2) ⊆ X0`, so `m >= 0` there, and the descent step gives
`|grad m(y)| <= max(sqrt(2M m(y)), 4 m(y)/delta)`. The descent lemma along
`[y, x]` then gives either `m(x) <= 2 m(y) + M|x-y|^2` or
`m(x) <= (1 + 4D/delta) m(y) + (M/2)|x-y|^2`. □

(QD) fails at boundary minimizers with nonzero gradient: for
`m = x(1-x) + y^4`, `x = (2h, 0)` and `y = (0, 0)`, it would need
`2h(1-2h) <= 4K h^2`. So [CN, Theorem 3.5] applies to interior minimizers
through Lemma 3.5, and Theorem 3.3 covers the rest.

**Proposition 3.6 (faces do not matter when `m >= 0` beyond the box).**
Assume `grad m` is `M`-Lipschitz and `m >= 0` on `X0 + B_2(0, r)`. Put
`K_1 = 1 + sqrt(2Mn) + Mn/2` and `t_0 = min(M r^2/2, s0^2/4)`. Then for every
face of dimension `d < n` and every `eps > 0`,

```
I_F(eps) <= H^d(F) t_0^(-d/2) + 4^d [ (d/2)(K_1+1)^(n/2) + (d/n) 2^((n-d)/2) K_1^(n/2) ] I_{X0}(eps).
```

Also, if a vertex is optimal, then `I_{X0}(eps) >= c log(1/eps)`. Hence
`N_opt ≍ |T_bis| ≍ 1 + I_{X0}(eps)`.

*Proof.* Let `t <= t_0`, `s = sqrt t`, and let `Z` be a maximal subset of
`F ∩ E(t)` with pairwise sup-distance `> 2s`. Then
`H^d(F ∩ E(t)) <= |Z| (4s)^d`.

For `z in Z`, the ball `B(z, r)` lies in the set where `m >= 0`.
- If `|grad m(z)| > Mr`, a step of length `r` would give
  `|grad m(z)| < 2t/r <= Mr`, a contradiction. So the step
  `grad m(z)/M` is admissible and `|grad m(z)| <= sqrt(2Mt)`.
- `X0` contains a cube `C_z` of side `s` with vertex `z`, because
  `s <= s0/2`. On it
  `m <= t + sqrt(2Mt) sqrt(n) s + (M/2) n s^2 = K_1 t`.
- The cubes `C_z` have disjoint interiors.

Hence

```
V(K_1 t) >= |Z| s^n >= 4^(-d) t^((n-d)/2) H^d(F ∩ E(t)).
```

Insert this into the layer-cake formula
`I_F(eps) = (d/2) integral_0^inf (t+eps)^(-d/2-1) H^d(F ∩ E(t)) dt`, split at
`eps` and `t_0`:
- On `[0, eps]`, the integral is at most `eps^(-d/2) H^d(F ∩ E(eps))`. Use
  `I_{X0}(eps) >= ((K_1+1) eps)^(-n/2) V(K_1 eps)`.
- On `[eps, t_0]`, use `t >= (t+eps)/2` and substitute `tau = K_1 t`.
- On `[t_0, inf)`, the integral is at most `H^d(F) t_0^(-d/2)`.

For an optimal vertex, `V(K_1 t) >= t^(n/2)`, so
`I_{X0}(eps) >= (n/2) 2^(-n/2-1) K_1^(-n/2) log(t_0/eps)`. □

## 4. The RLCT form of the characterization

**Theorem 4.1.** Assume (A2), (G^LB_alpha) and (U^q_alpha').
- For each face `F` (including `X0`) of dimension `d >= 1` with
  `min_F m = 0`, let `(lambda_F, theta_F) = RLCT_F(m|_F)`. Put
  `kappa_F(eps) = eps^(lambda_F - d/2) (log 1/eps)^(theta_F - 1)` if
  `lambda_F < d/2`, `(log 1/eps)^theta_F` if `lambda_F = d/2`, and `1` if
  `lambda_F > d/2`.
- If `min_F m > 0`, put `kappa_F = 1`.
- Let `kappa*(eps) = max_F kappa_F(eps)`.

Then there are `eps_0, c, C > 0`, depending on `f, alpha, alpha', n, s0`,
such that for `0 < eps <= eps_0`

```
c kappa*(eps)  <=  N_opt(eps)  <=  |T_bis|  <=  C kappa*(eps).
```

*Proof.* By Lemma 2.2 with `Omega = F` and `a = d/2`,
`I_F(eps) ≍ kappa_F(eps)`. If `m|_F ≡ 0`, then
`I_F = H^d(F) eps^(-d/2)`. If `min_F m > 0`, `I_F` is bounded. Insert into
Corollary 3.4. □

(The first version had an extra `log(1/eps) #{optimal vertices}` in the
upper bound. Lemma 3.3a removes it.)

**Remark 4.1a (faces with `lambda_F = d/2` and `theta_F >= 2`).** Theorem 4.1
allows `kappa_F = (log 1/eps)^theta_F` with `theta_F >= 2`, but we know no
instance in which such a face governs `N_opt`.
- If all zeros of `m|_F` lie in the relative interior of `F`, the proof of
  Lemma 2.4 applied on `F` gives `theta_F = 1` whenever `lambda_F = d/2`.
- `xy + x^3 + y^3` on a corner of a 2-face has `(lambda_F, theta_F) = (1, 2)`:
  `V(t) = (1/3) t log(1/t) + O(t)`, and numerically the ratio to
  `t log(1/t)` decreases toward `1/3` (0.348 at `t = 1e-10`). But its edges
  carry `x^3` and `y^3`, with `integral (x^3 + eps)^(-1/2) ≍ eps^(-1/6)`
  (`logs/revision_checks.log`). So the edges govern.
- *Sketch, not a proof: a zero at a corner of `F`, with `m|_F`
  Newton-nondegenerate on the orthant.* An edge with axis order `k > 2` has
  exponent `1/2 - 1/k > 0`, which dominates any `log^theta`. So the edges are
  harmless only if every axis order is at most 2.
  - If some axis order is 1, the diagonal meets `P` at `l <= 2/(d+1) < 2/d`,
    so `lambda_F = 1/l > d/2`.
  - If all axis orders are 2, then every monomial has degree at least 2, and
    the simplex `conv{2 e_i}` lies in the face `P ∩ {sum alpha_i = 2}`. That
    face contains `(2/d, ..., 2/d)` in its relative interior and has
    codimension 1, so `theta_F = 1`.

  Missing pieces:
  1. The steps "`lambda_F = 1/l`" and "`theta_F = theta_l`" need an
     **orthant** version of Lemma 2.3(b): equality on `R^d_{>=0}` when the
     face polynomials are positive on `(R_{>0})^d`. Lemma 2.3(b) and Lin's
     Theorem 1.3 are full-neighbourhood statements. With a linear term, `m`
     is not nonnegative on a full neighbourhood. The orthant version is
     standard toric bookkeeping, but it is not written out here.
  2. Zeros in the relative interior of a proper face of `F` of positive
     dimension are not treated.
  3. Newton-degenerate cases are not covered.

**Corollary 4.2 (the conjecture).** Assume (A2), (G^LB_alpha) and
(U^q_alpha'), and **either**
- (i) every global minimizer lies in `int X0`, **or**
- (ii) `m >= 0` on a neighbourhood `X0 + B(0, r)`. This holds, for example,
  for least squares, where `m >= 0` on `R^n`.

Let `(lambda, theta) = RLCT_{X0}(m)`. Then `lambda <= n/2`, and:

- if `lambda < n/2`: `N_opt(eps) ≍ |T_bis| ≍ eps^(lambda - n/2) (log 1/eps)^(theta - 1)`;
- if `lambda = n/2`: `N_opt(eps) ≍ |T_bis| ≍ (log 1/eps)^theta`. Under (i),
  this happens iff all minimizers are nondegenerate, and then `theta = 1`
  (Lemma 2.4).

Under (i) the constants are explicit. With
`L(eps) = c_V Gamma(1+lambda) Gamma(n/2 - lambda)/Gamma(n/2) · eps^(lambda-n/2) (log 1/eps)^(theta-1)`
and `lambda < n/2`,

```
(alpha n/pi^2)^(n/2) L(eps) (1 + o(1))  <=  N_opt(eps)  <=  |T_bis|  <=  2·12^n Lambda_2^(n/2) L(eps) (1 + o(1)).
```

For `lambda = n/2` under (i), replace `L` by
`sum_k (2 pi)^(n/2) det(H_k)^(-1/2) log(1/eps)/Gamma(n/2)`.

*Proof.*
- Under (i), `m` is bounded below by a positive constant on `∂X0`. So every
  proper face has bounded `I_F`, and no vertex is optimal. Apply Theorem
  3.1 with `d = n`, Theorem 3.3 and Lemma 2.2(i), (ii).
- Under (ii), Proposition 3.6 bounds every proper face integral by
  `C(1 + I_{X0})`.
- `lambda <= n/2`: under (i) this is Lemma 2.4. Under (ii), every zero `z`
  is a critical point of `m` on an open set, so `m <= C|y - z|^2` near `z`.
  The box contains an orthant piece of each small ball around `z`, so
  `V(t) >= c t^(n/2)`, and `Z(N) >= e^(-1) V(1/N)` gives `lambda <= n/2`. □

The ratio of the two constants under (i) is `2·12^n (pi^2 Lambda_2/(alpha n))^(n/2)`.
It is independent of `eps`, `lambda` and `theta`, but exponential in `n` and
far from tight. The computations below show ratios of leaves to the lower
bound of 4–19.

**Example 4.3 (the conjecture fails at boundary minimizers).**

*(a) A literal counterexample.* This one was proposed by the reviewer and is
re-verified here. Take
`f = m = x(1-x) + y^4 + z^4 + w^4` on `X0 = [0, 0.9] x [-0.4, 0.5]^3`
(`n = 4`), with exact alphaBB and `alpha = alpha' = 1.05`. The Hessian is
`diag(-2, 12y^2, 12z^2, 12w^2)`, so `alpha >= 1` suffices.
- *Minimizer.* The unique minimizer `0` lies on the face `x = 0`.
- *Full-dimensional RLCT.* Since `x/10 <= x(1-x) <= x` on `[0, 0.9]`,
  `{x <= t/2, y^4 + z^4 + w^4 <= t/2} ⊆ E(t) ⊆ {x <= 10t, y^4 + z^4 + w^4 <= t}`.
  So `V(t) ≍ t · t^(3/4)` and `RLCT_{X0}(m) = (7/4, 1)`. Here
  `7/4 < n/2 = 2`, so the conjecture applies and predicts
  `N_opt ≍ eps^(7/4 - 2) = eps^(-1/4)`.
- *Face `x = 0`* (`d = 3`). Here `m = y^4 + z^4 + w^4`, with RLCT
  `(3/4, 1)`. Theorem 3.1 gives
  `N_opt >= (3 alpha/pi^2)^(3/2) I_face(eps) ≍ eps^(3/4 - 3/2) = eps^(-3/4)`.
- *Other faces.* Every other face has `min m > 0`, so Theorem 4.1 gives
  `N_opt ≍ |T_bis| ≍ eps^(-3/4)`.
- *Integrals* (`logs/revision_checks.log`, computed as one-dimensional
  Laplace-transform integrals).
  - `I_face` has local slope 0.7500 at `eps = 1e-8`. Its ratio to the leading
    term `8 Gamma(5/4)^3 Gamma(3/4)/Gamma(3/2) eps^(-3/4)` is 0.99999 there.
  - The full four-dimensional integral grows like `21.599 eps^(-1/4)`. Its
    values are 184.68, 651.75 and 2128.63 at `eps = 1e-4, 1e-6, 1e-8`. The
    local slope, 0.254 at `1e-8`, tends to `1/4` from above.
  - The full integral was computed three ways: `H` in closed form (Dawson
    function), `H` by split quadrature, and with `x` outside. All three
    agree. The first revision reported smaller values (1429.5 at `1e-8`) and
    a slope 0.24, because of a quadrature bug in `H` (Section 11.1).
- *Bisection* (`logs/revision_sweep.jsonl`, `eps = 1e-1 ... 1e-6`). The
  leaves are 136 … 1,317,301, matching the reviewer's independent code
  exactly. Over `[1e-6, 1e-3]`, the least-squares slope of `log(leaves)` on
  the half-decade grid (seven points) is 0.720, and the two-endpoint slope is
  0.748. Dyadic oscillation, up to a factor of about 1.5, explains the
  difference. Leaves divided by the face lower bound stay in 22–48, while
  `leaves · eps^(1/4)` grows by a factor of about 540.

A simpler instance of the same failure: `f = x(1-x)` on `[0, 0.9]^3` has
`RLCT_{X0} = (1, 1)`, with `1 < 3/2`, so the conjecture predicts
`eps^(-1/2)`. But the face `x = 0` has `m ≡ 0`, which gives
`N_opt >= (2 alpha/pi^2) 0.81 eps^(-1)`.

*(b) A two-dimensional illustration* (instance `bdry`, outside the
conjecture's hypothesis). Take `f = m = x(1-x) + y^4` on
`X0 = [0, 0.9] x [-0.4, 0.5]`, with `alpha = alpha' = 1.05`.
- *Full-dimensional RLCT.* As in (a), `V(t) ≍ t^(5/4)`. So
  `RLCT_{X0}(m) = (5/4, 1)`, with `lambda > n/2 = 1`. The full-dimensional
  integral stays bounded; it is 8.28 at `eps = 1e-12`
  (`logs/integrals.log`). The conjecture says nothing here, because it
  assumes `lambda <= n/2`.
- *Edge `x = 0`.* The RLCT of `y^4` there is `(1/4, 1)`, so
  `N_opt ≍ |T_bis| ≍ eps^(-1/4)`.
- *Bisection.* 7651 leaves at `eps = 1e-12`. The slope over
  `[1e-12, 1e-9]` is 0.245, and leaves divided by the edge lower bound stay
  in 3.4–7.4 over 11 decades (Section 5).

The mechanism in both cases is that of [CN, Section 8.2]: `m` grows linearly
into the interior, so the boundary stratum carries the count. Kannan and
Barton (2017, Lemma 10 and Corollary 4) found the upper-estimate,
fixed-width form of this mechanism. When `f` grows linearly along
`grad f(x*)` at a constrained minimizer, their cluster estimate loses one
dimension (Section 8).

## 5. Newton polyhedra and worked examples

**Recovering the rate table [CN, 3.8] (interior minimizers).**
- *Separable growth.* Let `c sum |t_i|^(q_i) <= m <= C sum |t_i|^(q_i)`
  with even `q_i`. By Lemma 2.1(e) and Lin's Proposition 3.7, the RLCT is
  `(sum 1/q_i, 1)`. Equivalently, `P(sum t_i^(q_i))` is the simplex with
  vertices `q_i e_i`; it is nondegenerate, and the diagonal meets it at
  `l = 1/sum(1/q_i)` in the relative interior of the facet, so `theta = 1`.
  The exponent is `n/2 - sum 1/q_i`, and all `q_i = 2` gives `log`. For odd
  or non-integer `q_i`, compute `V(t)` directly by scaling. It is
  `≍ t^(sum 1/q_i)`.
- *Morse–Bott.* In adapted coordinates `m ≍ sum_{i <= n-p} t_i^2`, so the
  RLCT is `((n-p)/2, 1)` and the exponent is `p/2`.
- *Nondegenerate points.* `(n/2, 1)`, giving `log(1/eps)` (Lemma 2.4).

**Table 5.1 (examples; exact alphaBB; `alpha` from analytic Hessian bounds,
see `instances.py`).**

| instance | `m` | `X0` | `alpha` | RLCT `(lambda, theta)` | derivation | predicted `N_opt`, `|T_bis|` |
|---|---|---|---|---|---|---|
| `xy2` | `x^2 y^2` | `[-0.9,1.3]^2` | 1.7745 | `(1/2, 2)` | `<xy>` monomial: `P = (1,1) + R^2_+`, `l_I = 1` at a vertex (codim 2), so `(1, 2)` for the ideal and `(1/2, 2)` for `m`. Points `(a, 0)`, `a != 0`, have `(1/2, 1)`, and the minimum in Lin's order is at 0 | `eps^(-1/2) log(1/eps)` |
| `cusp` | `(x^2 - y^3)^2` | `[-0.45,0.65]^2` | 2.856 | `(5/12, 1)` | quasi-homogeneous: `x = tau^(1/2) u`, `y = tau^(1/3) v` with `tau = sqrt t` give `V(t) = t^(5/12) area{|u^2 - v^3| <= 1, ...}`, and the area increases to `A = 7.9622 < inf` | `eps^(-7/12)` |
| `xy2z4` | `x^2 y^2 + z^4` | `[-0.9,1.3]^3` | 1.7745 | `(3/4, 2)` | `<xy, z^2>` monomial: `P = conv{(1,1,0),(0,0,2)} + R^3_+`. The diagonal meets it at `t = 2/3`, inside the edge exposed by `beta = (1,1,1)` (codim 2), giving `(3/2, 2)` and `(3/4, 2)`. Axis points have `(3/4, 1)` | `eps^(-3/4) log(1/eps)` |
| `sep24` | `x^2 + y^4` | `[-0.9,1.3]^2` | 1 | `(3/4, 1)` | separable | `eps^(-1/4)` |
| `bdry` | `x(1-x) + y^4` | `[0,0.9]x[-0.4,0.5]` | 1.05 | `X0`: `(5/4, 1)`; edge `x=0`: `(1/4, 1)` | Example 4.3 | `eps^(-1/4)` (edge) |

Two points about these examples.
- *The cusp raises the exponent above half the dimension of the optimal
  set.* The optimal set of `cusp` is a curve, so [CN, Corollary 6.5] would
  suggest `1/2`. But (QG) fails at the cusp: at `(0, y)`, `m = y^6` while
  `dist^2 ≍ y^3`. The exponent is `7/12`.
  - The heuristic: the tube `|g| <= sqrt(eps)`, `g = x^2 - y^3`, has width
    `sqrt(eps)/|grad g| ≍ sqrt(eps)/|s|^3` at the curve point
    `(s^3, s^2)`. Along the curve it contributes `eps^(-1/2) ds/|s|^2`, down
    to the scale `|s| ≍ eps^(1/12)` where the two branches merge.
  - `m` is degenerate for its Newton polyhedron (`m_gamma = (x^2 - y^3)^2`
    has singular zeros on the torus), so Lemma 2.3(b) does not apply. Still,
    the bound `lambda <= 1/l = 5/12` of Lemma 2.3(a) is attained. For
    `g = x^2 - y^3` itself, `l = 6/5 > 1` and `lambda(|g|) = 5/6`, which is
    Varchenko's remote case.
- *Coordinates matter.* `(x - y)^2` has `l = 1` but `lambda = 1/2`. Lin's
  Remark 4.13: `(x + y)^2 + y^4` has RLCT `(3/4, 1)`, while its principal
  part `(x+y)^2` has `(1/2, 1)`. The Newton bound is sharp only in good
  coordinates, as for any use of Lemma 2.3.

**Numerical checks.** Node bounds are computed by batched accelerated
projected gradient on the convex node problem, with a Frank–Wolfe
certificate as a valid lower bound (`bisect_bb.py`).
- *Node bounds.* Against the best of 5 L-BFGS-B runs on 150 random boxes per
  instance, the certified lower bound never exceeds the reference by more
  than `4.4e-16`. The upper bound is never below it by more than `5.6e-17`.
  The relative gap is at most `5.5e-12` (`logs/check_node_bounds.log`). No
  node was left undecided in any run.
- *Leading constants of the integrals* (`logs/fit_constants.log`).

  | instance | fitted leading constant | prediction (Lemma 2.2(i)) |
  |---|---|---|
  | `cusp`, fit `a eps^(-7/12) + b eps^(-1/2) + c` | `a = 10.79023` | `A Gamma(17/12) Gamma(7/12) = 10.79020` |
  | `xy2`, fit of `I sqrt(eps)` against `log(1/eps)` | 3.14016 | `pi` |
  | `xy2z4`, fit of `I eps^(3/4)` against `log(1/eps)` | 4.44266 | `2 K4 Gamma(7/4) Gamma(3/4)/Gamma(3/2) = 4.44288`, with `K4 = integral_{-1}^1 sqrt(1-w^4) dw` |

  The cusp needs the second term because the next pole is at `1/2`, from
  the smooth part of the curve: the relative correction is
  `eps^(1/12) ≈ 0.26` at `1e-7`.

**Table 5.2 (bisection leaves; `logs/analyze_sweep.log`; `eps = 10^(-k/4)`).**
- "LB" is Theorem 3.1: `d = n` for the first four rows, the edge `x = 0`
  (`d = 1`) for `bdry`.
- The slope is the least-squares slope of `log(leaves)` against `log(1/eps)`
  over the last three decades. For `theta = 2`, the second number is the
  slope after dividing by `log(1/eps)`.
- Leaves oscillate by factors up to 1.5 with the position of `eps` relative
  to dyadic levels.

| instance | leaves at `eps = 1e-4 / 1e-6 / finest` | finest `eps` | slope | predicted | leaves/LB, all `eps` |
|---|---|---|---|---|---|
| `xy2` | 5707 / 82321 / 1281379 | `1e-8` | 0.559; 0.491 | 0.5 (+ log) | 4.4–7.1 |
| `cusp` | 5104 / 91507 / 5801155 | `1e-9` | 0.595 | 0.5833 | 3.8–6.7 |
| `xy2z4` | 188462 / 13165678 | `1e-6` | 0.828; 0.729 | 0.75 (+ log) | 10.3–18.7 |
| `sep24` | 184 / 559 / 6001 | `1e-10` | 0.251 | 0.25 | 7.0–9.7 |
| `bdry` | 73 / 232 / 7651 | `1e-12` | 0.245 | 0.25 | 3.4–7.4 (edge LB) |
| `face4d` (revision) | 49996 / 1317301 | `1e-6` | 0.720 (seven half-decade points; the endpoint slope is 0.748) | 0.75 (face `x = 0`; the conjecture predicts 0.25) | 22–48 (face LB, `d = 3`) |

In every row the ratio of leaves to the proved lower bound varies by at
most a factor 2.2 over 5–11 decades, as Corollary 4.2 and Theorem 4.1
predict. The raw
slopes for `xy2` and `xy2z4` lie above the exponent by about
`1/log(1/eps)`, which is the log factor. The cusp slope exceeds `7/12`
because of the negative `eps^(-1/2)` correction found in the fit.

## 6. Singular learning theory

**6.1 Exact data.** Consider reduced-rank regression
`y = B A x` with `A in R^(H x M)` and `B in R^(N x H)`, so `n = H(M+N)`
parameters. Take noiseless data `y_k = pi0 x_k` with
`S = sum_k x_k x_k^T > 0`. The least-squares objective is
`f(A, B) = tr((BA - pi0) S (BA - pi0)^T)`, with `f* = 0`, and

```
lambda_min(S) ||BA - pi0||_F^2  <=  m(A,B)  <=  lambda_max(S) ||BA - pi0||_F^2.
```

By Lemma 2.1(e), `m` has the RLCT of `K = ||BA - pi0||_F^2` on every compact
set. `K` is, up to the factor 1/2, the Kullback–Leibler divergence of the
Gaussian model with identity covariances that Aoyagi and Watanabe (2005)
analyse. See Drton–Plummer (2017, Example 2.2), who report their learning
coefficient `lambda(M, N, H, r)` and multiplicity.

**Proposition 6.1.** Let `pi0 = 0` (true rank `r = 0`), and let `X0` be a cube
containing the origin in its interior. Then `RLCT_{X0}(m)` equals the
learning coefficient `(lambda_AW, theta_AW)` at `r = 0`, and under exact
alphaBB (or any scheme with (G^LB_alpha) and (U^q_alpha'))

```
N_opt(eps) ≍ |T_bis| ≍ eps^(lambda_AW - H(M+N)/2) (log 1/eps)^(theta_AW - 1).
```

*Proof.*
- `K(tA, tB) = t^4 K(A, B)`. So scaling maps a neighbourhood of any point
  to a neighbourhood of a point with the same local RLCT. The RLCT over a
  ball `B(0, rho)` is therefore independent of `rho`, and it equals the
  minimum over all points of the zero set.
- `X0` lies between two such balls, so `RLCT_{X0} = RLCT_{B(0,rho)}`.
- `m >= 0` on `R^n`, so Corollary 4.2(ii) applies. □

We take `lambda_AW` to be the RLCT of `K` for a prior that is smooth and
positive on a neighbourhood of the origin, as in Drton–Plummer's
description. We did not check Aoyagi–Watanabe's exact assumptions on the
parameter set; by the scaling argument, any compact set containing a
neighbourhood of the origin gives the same value.

We did not re-derive `lambda_AW`. We use the formula as recalled below and
checked it against all nine entries of Drton–Plummer's Table 1
(`N = 5`, `M = 3`; `logs/check_rrr_formula.log`). Let `s = M + H + N + r`.
In the case `N + r <= M + H`, `M + r <= N + H`, `H + r <= M + N`:
`lambda = [2(H+r)(M+N) - (M-N)^2 - (H+r)^2 + (1 if s is odd else 0)]/8`.
Otherwise `lambda = (HM - Hr + Nr)/2` if `M + H < N + r`,
`(HN - Hr + Mr)/2` if `N + H < M + r`, and `MN/2` if `M + N < H + r`.
For multiplicities we only use Drton–Plummer's statement for `N = 5`,
`M = 3`: `theta = 1` except `(H, r) = (3, 0)`, where `theta = 2`.

| `H` (`n = 8H`) | `r` | `lambda` | node exponent `n/2 - lambda` |
|---|---|---|---|
| 1 | 0 | 3/2 | 5/2 |
| 2 | 0 | 3 | 5 |
| 3 | 0 | 9/2 | 15/2, with a `log(1/eps)` factor (`theta = 2`) |
| 1, 2, 3 | `r = H` | `H(8-H)/2` | `H^2/2`: the `GL(H)` orbit, Morse–Bott with `p = H^2` |

For `r = H` the zero set is a smooth, non-compact `GL(H)` orbit that meets
`∂X0`. Corollary 4.2(ii) still applies because `m >= 0` on `R^n`. That the
box-restricted RLCT equals `H(M+N-H)/2` is standard for Morse–Bott zero sets;
this row is not re-verified here. The rows with `0 < r < H` would need the
local analysis at the most singular points of the fibre; they are not
claimed.

The smallest case `M = N = H = 1`, `r = 0` is `m = S a^2 b^2`, the instance
`xy2`: `(1/2, 2)`, and `eps^(-1/2) log(1/eps)` nodes. The identifiable model
`y = beta x` needs `Theta(log 1/eps)`.

**6.2 Noisy data.** For `y = abx + noise`,
`f(a,b) = S(ab - delta)^2 + const`, where `delta` is the least-squares
coefficient. With true coefficient 0, `delta ≍ sigma/sqrt(S)`. So
`m = S(ab - delta)^2`, whose zero set is the hyperbola `ab = delta`.

**Proposition 6.2.** Let `X0` be a cube containing the origin in its
interior, and fix `alpha` and `alpha'`. Uniformly in `delta in [0, delta_0]`
and `0 < eps <= eps_0`, with `delta_0 < 1` and `eps_0 < 1` fixed and small
enough that `m > 0` at the vertices,

```
N_opt(eps) ≍ |T_bis| ≍ eps^(-1/2) (1 + log(1/max(eps, delta^2))).
```

*Proof.* Theorem 3.1, Theorem 3.3 and Proposition 3.6 hold with constants
uniform in `delta`. `M` is bounded, and `m >= 0` on `R^2`. Take
`X0 = [-0.9, 1.3]^2`; other cubes change only the constants. With `a = 0.9`
and `b = 1.3`, the inner integral is
`F(x) = integral dy/((xy - delta)^2 + eps) = |atan((bx - delta)/sqrt eps) - atan((-ax - delta)/sqrt eps)|/(|x| sqrt eps)`.
Let `rho = max(delta, sqrt eps)`.
- For `|x| <= C rho`: `F <= 2.2/eps` and `F <= pi/(|x| sqrt eps)`
  always, and `F <= 8.8/delta^2` when `|x| <= delta/2.6`. The contribution
  is `O(eps^(-1/2))`.
- For `|x| >= C rho`: `F = pi/(|x| sqrt eps) + O(x^(-2))`, and the error
  integrates to `O(1/rho)`.

So `I(eps) = (pi/sqrt eps)(log(1/rho^2) + O(1))`. □

Numerically, `I(eps) sqrt(eps)` freezes for `eps << delta^2` (`logs/integrals.log`):

| `eps` | `delta = 0` | `delta = 1e-3` | `delta = 1e-2` |
|---|---|---|---|
| 1e-4 | 29.96 | 29.93 | 27.78 |
| 1e-6 | 44.39 | 42.22 | 29.89 |
| 1e-8 | 58.86 | 44.36 | 29.92 |

The freeze values match `pi log(1/delta^2) + 0.99`. Bisection leaves times
`sqrt(eps)` behave the same way: they grow from about 57 to 128 between
`1e-4` and `1e-8` for `delta = 0`, and stay in 50–68 for `eps <= 1e-4` when
`delta = 1e-2` (`logs/analyze_sweep.log`, last table). The exponent stays
`1/2`, because the model remains non-identifiable along the hyperbola
(`p = 1`). Only the singular log factor disappears below the noise scale.

**Conjecture 6.3 (two regimes; sketch only).** For noisy least squares
`m_N = L_N - min L_N` in a singular model, the near-optimal sets `E(eta)`
behave as follows:
- for `eta >> sigma^2/N_data`, they resemble the exact-data sets, because
  the noise term `2<xi, g(w)>/N_data` is `O(sqrt(K(w)/N_data))`. Then
  `N_opt` grows with exponent `n/2 - lambda(r)`;
- for `eta << sigma^2/N_data`, they resemble the noisy minimizer set. For
  reduced-rank regression with generic noise this is plausibly the
  `GL(H)` orbit of the reduced-rank estimate, Morse–Bott with `p = H^2`.
  Then the exponent is `H^2/2`.

Proposition 6.2 is the case `M = N = H = 1`. A proof would need uniform
control of the empirical process (Watanabe's standard form), a check of the
Morse–Bott property of the noisy fit, and the handling of a non-compact
orbit cut by `∂X0`. None of this is done here.

## 7. Higher-order relaxations

**Hypotheses.** Let `delta_B(y) = max_i d_i(y)`, the sup-distance from `y` to
the nearest vertex of `B`.
- (G^k_alpha): `LB(B) <= f(y) - alpha delta_B(y)^k` for every box `B` and
  `y in B`.
- (U^k_tau): `f_B >= f - tau w(B)^k` on `B`.

For `k = 2`, (G^pt_alpha) implies (G^2_alpha), since
`q_B >= sum d_i^2 >= delta_B^2`, and (U^q_alpha') implies
(U^2_{alpha' n/4}). For `k = 1` these are [CN, Section 8.4].

Two model examples:
- a vertex-vanishing gap `alpha sum_i a_i(y)^(k/2)`;
- the worst case of an order-`k` bound, `f_B = f - alpha w(B)^k`, which is
  the "sharp" case of Wechsung et al. (2014, Lemma 1).

Taylor models of order `k - 1` satisfy (U^k). They satisfy (G^k) only when
their remainder enclosure is sharp in this sense, so (G^k) is a modelling
assumption.

**Theorem 7.1 (order-`k` covering law).** Let
`Phi^(k)(eps) = sup_{eta >= 0} N_inf(E(eta), 2((eps+eta)/alpha)^(1/k))`.

(a) Under (G^k_alpha), `N_opt(eps) >= 2^(-n) Phi^(k)(eps)`.

(b) Under (U^k_tau), with `J_k = #{j : tau s_j^k > eps}`:
`|T_bis| <= 1 + 2^n sum_{j: tau s_j^k > eps} N_j(E(tau s_j^k - eps)) <= 1 + 6^n max(1, ceil(2(tau/alpha)^(1/k)))^n J_k Phi^(k)(eps)`.

(c) Within a factor `2^n`, `Phi^(k)(eps)` is the running supremum over
`eta >= eps` of `psi_k(eta) = N_inf(E(eta), 2(eta/alpha)^(1/k))`.

*Proof.*
- (a) For `y in E(eta) ∩ C` with `C` in a certificate,
  `alpha delta_C(y)^k <= m(y) + eps <= eta + eps`. So `y` lies within
  `((eps+eta)/alpha)^(1/k)` of a vertex of `C`, and the `2^n |P|` cubes
  around vertices cover `E(eta)` [CN, Theorem 4.6].
- (b) A non-pruned level-`j` cube contains `y` with
  `m(y) < tau s_j^k - eps`. A cube of side `s_j` meets at most `3^n`
  level-`j` cells, and
  `s_j = 2((eps + t)/alpha)^(1/k) · (1/2)(alpha/tau)^(1/k)` for
  `t = tau s_j^k - eps`. Change the covering scale [CN, Theorem 6.3].
- (c) As in [CN, Remark 6.3a], using `ceil(2^(1/k)) = 2`. □

**Proposition 7.2 (fatness only at scale `sqrt(eta)`).** Assume (A1) and
interior minimizers, and let `eta` be small. Part (c) also assumes
(G^k_alpha) and (U^k_tau).

(a) If `Q(y, r) ⊆ X0`, then `m <= (1+n) m(y) + n M r^2` on `Q(y, r)`
(Lemma 3.2 with `d = n`). So `E(eta) + Q(0, r) ⊆ E((1+n) eta + n M r^2)`.
This is `E(C eta)` when `r ≍ eta^(1/2)`, but only `E(C eta^(2/k))` when
`r ≍ eta^(1/k)` with `k > 2`.

(b) Consequently, with `r = (eta/alpha)^(1/k)`:

```
2^(-n) r^(-n) V(eta)  <=  psi_k(eta)  <=  r^(-n) V((1+n) eta + n M r^2/4).
```

(c) *Volume law for `k <= 2`.* If `k <= 2`, then `r^2 <= C eta`. Summing
the level counts `N_j <= s_j^(-n) V(C s_j^k)` directly, without passing
through `Phi`, gives the following for `C^{1,1}` `m`:

```
c eps^(-n/k) V(eps)  <=  N_opt(eps)  <=  |T_bis|  <=  C (1 + integral_{X0} (m + eps)^(-n/k)).
```

Under (A2) with `lambda < n/k`, both sides are
`≍ eps^(lambda - n/k) (log 1/eps)^(theta-1)` (Lemma 2.1(c) and Lemma 2.2(i)).
For `C^{1,1}` `m` without analyticity, the lower bound is only the volume
form. (G^k) gives no integral lower bound for `k < 2`, because
`delta_C^(-n)` is not integrable near the vertices of `C`. For `k = 2` under
(G^pt), Theorem 3.1 supplies the integral lower bound.

(d) *For `k > 2` the RLCT does not determine the exponent.* Let
`e_k = limsup log psi_k(eta)/log(1/eta)`. Then
`(n/k - lambda)_+ <= e_k <= (n - 2 lambda)/k`. Both ends are attained
(Proposition 7.3), and the gap `lambda(1 - 2/k)` is positive for
`lambda > 0`.

*Proof of (b)–(c).*
- (b) The lower bound is volume counting. For the upper bound, take a
  maximal subset of `E(eta)` with sup-separation `> r`. The cubes of radius
  `r/2` around its points are disjoint and lie in
  `E((1+n) eta + n M r^2/4)`.
- (c) By (a), every level-`j` cell meeting `E(tau s_j^k)` lies in
  `E(C s_j^k)`. The Fubini computation of Theorem 3.3 then gives
  `sum_j s_j^(-n) V(C s_j^k) <= C' integral (m+eps)^(-n/k)`. The lower bound
  is Theorem 7.1(a) with `eta = eps` and (b). Under (A2), evaluate both sides
  with Lemmas 2.1(c) and 2.2. □

For `k = 1`, (c) gives `eps^(lambda - n)`. This is consistent with
[CN, Theorem 8.2(c)–(d)]: `n/2` at nondegenerate points and `(n+p)/2` at
Morse–Bott sets.

**Proposition 7.3 (order-`k` examples).** Assume (U^k_tau) and (G^k_alpha).

(a) *Isolated minimizer, Łojasiewicz growth.* If `m(y) >= c |y - y*|^q` near
`y*` and `m` is bounded away from 0 elsewhere, then `psi_k` is bounded for
`k >= q`. So `1 <= N_opt <= |T_bis| = O(log 1/eps)`. For analytic `m` with an
isolated zero, such a `q` exists by the Łojasiewicz inequality (Łojasiewicz
1959). If also `m <= C sum |t_i|^(q_i)` and `m >= c sum |t_i|^(q_i)` in
suitable coordinates, then `e_k = sum_i (1/k - 1/q_i)_+`. This attains the
lower end of 7.2(d) when all `q_i >= k`. With all `q_i = q`, this is Bubeck
et al. (2011, Example 3): near-optimality dimension `(1/b - 1/a) D`.

(b) *Morse–Bott set of dimension `p >= 1`* (compact, `C^2`, without
boundary, in `int X0`, with (QG)). For `k >= 2`,
`N_opt ≍ |T_bis| ≍ eps^(-p/k)`, with no log, which attains the upper end
`(n - 2 lambda)/k = p/k`.
- Lower bound: Theorem 7.1(a) with `eta = 0` and `N_inf(M*, delta) ≍ delta^(-p)`.
- Upper bound: `E(tau s^k)` lies in the tube of radius
  `sqrt(tau s^k/c_g) <= C s`. So `N_j(E) <= C N_j(M*) <= C s_j^(-p)`
  [CN, Theorem 7.2, upper-bound steps], and the geometric sum is dominated
  by its last term.

(c) *Same `lambda`, different exponents.* In `n = 2`, take `y^2` (a line of
minimizers), `x^4 + y^4` (isolated) and `x^2 y^2` (crossing lines). All
three have `lambda = 1/2`, so `e_2 = 1/2` for all three. For `k = 3`:
`e_3 = 1/3, 1/6, 1/3`. For `k = 4`: `1/4, 0, 1/4`.

These values come from direct computation of `psi_k`, not from (a) and (b).
The minimizing segment of `y^2` meets `∂X0`, so (b) does not apply verbatim.
- `y^2`: `E(eta)` is a strip of width `2 sqrt(eta)`, below the scale
  `eta^(1/k)`, so `psi_k ≍ eta^(-1/k)`.
- `x^4 + y^4`: `E(eta)` is a ball of radius `≍ eta^(1/4)`, so
  `psi_k ≍ max(1, eta^(1/4 - 1/k))^2`.
- `x^2 y^2`: the arms `|y| <= sqrt(eta)/|x|` give `≍ eta^(-1/k)`, and the
  centre gives less.

*Check (c)* (`order_k_counts.py`, `logs/order_k_counts.log`). The script
counts the level-`j` cells of `[-0.9,1.3]^2` meeting `E(s_j^k)`, in exact
arithmetic on cell minima. The table gives the local slopes of
`log N_j` against `log(1/s_j)` for `j = 6..14`; the prediction is `k e_k`.

| `k` | `y^2` | `x^4 + y^4` | `x^2 y^2` |
|---|---|---|---|
| 2 | 1.000 (pred. 1) | 0.83–0.99 (pred. 1) | 1.16 → 1.09 (pred. 1, plus log) |
| 3 | 1.000 (pred. 1) | 0.29–0.51, mean ≈ 0.43 (pred. 0.5) | 0.59–1.26, → 0.94 (pred. 1) |
| 4 | 1.000 (pred. 1) | 0 (`N_j = 9`; pred. 0) | → 0.999 (pred. 1) |

**Remark 7.4 (certified Lipschitz optimization).** Bachoc, Cesari and
Gerchinovitz (2021, Theorem 3) show that the optimal certified sample
complexity lies between two bounds:
- below: `c_d (1 - Lip(f)/L)^d/(1 + log2(eps0/eps)) · integral_X dx/(f(x*) - f(x) + eps)^d`;
- above: `C_d` times the same integral.

This holds under their Assumption 4, which a box satisfies. For `f` analytic
on a neighbourhood of a box `X` of dimension `d`, Lemma 2.2(i) with `a = d`
evaluates this integral as `≍ eps^(lambda - d) (log 1/eps)^(theta-1)`, where
`(lambda, theta)` is the RLCT of the gap on `X`. Here `lambda <= d/2 < d`
for interior maximizers. So the certified Lipschitz complexity of analytic
functions has exponent `d - lambda`, with log powers between `theta - 2` and
`theta - 1`. This is the same exponent as Proposition 7.2(c) with `k = 1`.
We did not find this remark in their paper, which does not discuss analytic
or degenerate functions.

## 8. Literature

**Sources examined.** Where a source was only partly read, the table says so.

| Source | How examined | What it says that is relevant | Relation |
|---|---|---|---|
| Kearfott, Du, "The cluster problem in global optimization: the univariate case", Computing Suppl. 9 (1992) | full preprint (reliable-computing.org `uniclust.pdf`) | Remark 2: if `f''(x*) = 0`, "there may exist a severe cluster when α < 3". Conclusion 3: "When f′(x∗) = f′′(x∗) = 0, use an interval extension of order at least 3". Remark 3: an endpoint minimizer with `f' != 0` needs only order 1 | the qualitative "degenerate needs higher order" idea, in 1D, as upper-bound analysis. For quartic growth order 3 still gives `eps^(-1/12)` (Proposition 7.3(a)), so order 4 is needed for a bounded count |
| Du, Kearfott, JOGO 5 (1994) | local full text | Remark 2: if the Hessian is not positive definite, "we need to have a better interval extension (at least of order 3)". Conclusion 3: "a higher order extension may be necessary". Remark 1: bounds are upper bounds, "not a precise value" | same idea, multivariate, nondegenerate analysis only |
| Neumaier, Acta Numerica (2004), Section 15 | local full text | volume heuristic "const √((2Δ)^n)/(ε^n √det G)" boxes, for box diameter `ε` and accuracy `Δ = K ε^(s+1)`; "In case of nonisolated solution sets, some clustering seems unavoidable" | with the sublevel volume replaced by its RLCT asymptotic, the heuristic gives exponent `n/k - lambda`. That is right for `k <= 2` (Proposition 7.2(c)) and can be wrong for `k > 2` (7.2(d)) |
| Wechsung, Schaber, Barton, JOGO 58 (2014) | local full text, Section 2 | covering of `B = {f - f* <= eps}` by boxes of width `delta = (eps/K)^(1/beta)`; nondegenerate Hessian assumed (Assumption 1) | the scale law `eps^(1/k)` in fixed-width, upper-estimate form, for nondegenerate minima only. Theorem 7.1 is its multi-scale, two-sided version for adaptive trees |
| Kannan, Barton, JOGO 69 (2017) | local full text, Section 3 (Lemmas 8 and 10, Remark 4, Corollary 4) | Remark 4, item 3: a "hierarchy of conditions", "with the condition for third-order convergence ... amounting to the third-order Taylor expansion of f growing faster than cubically ..., and so on". Lemma 10 and Corollary 4: when `f` grows linearly along `grad f(x*)`, the fixed-width box estimate scales as `O(eps^((n_x - 1)(1/2 - 1/beta*)))` instead of `O(eps^(n_x (1/2 - 1/beta*)))` | the sufficiency direction of Proposition 7.3(a) is essentially stated here. Corollary 4 is the upper-estimate, fixed-width precedent for the face mechanism of Example 4.3 (added in the revision). New here: lower bounds for adaptive trees, degenerate and non-isolated sets, the face-by-face RLCT form, and the failure of volume counting for `k > 2` |
| Lin, "Ideal-theoretic strategies for asymptotic approximation of marginal likelihood integrals", J. Algebraic Statistics 8 (2017), arXiv:1003.5338 | arXiv PDF, Sections 1–4 | compact semianalytic `Omega`; Theorem 2.10; Propositions 2.5, 3.2–3.7; Lemma 4.1; Propositions 4.2–4.5, 4.12; Theorems 1.3, 4.8–4.10; Remark 4.13 | the analytic input of Section 2. Theorem numbers are those of the arXiv version read. Lemma 2.3 cites Theorem 1.3 with Propositions 4.3 and 4.5 rather than Theorems 4.8–4.9, whose literal statement fails for sign-changing functions (remark after Lemma 2.3) |
| Drton, Plummer, JRSS-B (2017), arXiv:1309.0911 | arXiv PDF, Example 2.2, Table 1 | Aoyagi–Watanabe reduced-rank-regression learning coefficients for `N = 5`, `M = 3`, and multiplicities | source of the `lambda` values used in Section 6 (Aoyagi–Watanabe 2005 was not read directly) |
| Bachoc, Cesari, Gerchinovitz, NeurIPS 2021, arXiv:2102.01977 | arXiv PDF, Theorem 3 and Section 5 | certified Lipschitz complexity `≍ integral dx/(f* - f + eps)^d` up to logs; no analytic or RLCT discussion | Remark 7.4 |
| Bubeck, Munos, Stoltz, Szepesvári, JMLR 2011 ("X-armed bandits"), arXiv:1001.4475 | arXiv PDF, Definition 5, Example 3 | `f = 1 - ||x||^a`, `ell' = ||.||^b`: near-optimality dimension `(1/b - 1/a) D` | the homogeneous isolated case of Proposition 7.3(a) |
| Potfer, Perchet, "Instance-dependent stochastic Lipschitz bandit", arXiv:2605.29748 (May 2026) | abstract only | regret "that adapt to the local growth of level sets"; positive-dimensional maximizers | related level-set viewpoint; no RLCT mentioned in the abstract |
| Grulha, "On the divisorial geometry of volume asymptotics of sublevel sets", arXiv:2606.30171 (June 2026) | abstract only | sublevel volume expansions and poles of local zeta functions | pure singularity theory; no optimization |
| Lau, Furman, Wang, Murfet, Wei, "The local learning coefficient", arXiv:2308.12108 (AISTATS 2025) | search snippets only | the learning coefficient as the volume-scaling exponent of near-optimal parameters ("basin broadness") | same volume exponent; no branch-and-bound |
| Watanabe, *Algebraic Geometry and Statistical Learning Theory* (2009); Varchenko (1976); Arnold–Gusein-Zade–Varchenko, Vol. II | not read here; cited through Lin | original sources for Lemmas 2.1 and 2.3 | |

**Searches.** Web searches, all 2026-09-29:
- `"log canonical threshold" branch and bound global optimization complexity`;
- `"near-optimality dimension" "log canonical threshold" OR "Newton polyhedron" OR "learning coefficient"`;
- `"real log canonical threshold" "global optimization" OR "branch-and-bound" OR "bandit"`;
- cluster problem and degenerate minimizer;
- Newton polyhedron with interval or branch-and-bound;
- X-armed bandits with degenerate maximizers;
- Zhigljavsky random search and level-set measure;
- one extended search on certified or Lipschitz complexity via RLCT, Newton polyhedra or sublevel-set exponents.

None returned a paper that links branch-and-bound, cluster, Lipschitz or
bandit complexity to RLCTs or Newton polyhedra.

The local library (1187 papers) was grepped for "log canonical",
"Newton polyhedr/polytope", "learning coefficient", "Varchenko" and "zeta
function". The 11 hits concern Newton polytopes in SOS/SONC certificates
and polytope theory, not node complexity.

**What is claimed as new, as far as this bounded search found.**
- Theorem 3.3, Lemma 3.3a and Corollary 3.4: a two-sided box-face
  characterization of `N_opt` and bisection for `C^{1,1}` objectives, with no
  doubling condition and no log loss at vertices.
- The RLCT form (Theorem 4.1 and Corollary 4.2), including the
  boundary-face correction and Example 4.3. Kannan–Barton (2017,
  Corollary 4) is the fixed-width precedent for the face mechanism.
- The exponent `n/2 - lambda` for exact-data least squares in singular
  models (Proposition 6.1), and the exact noisy toy (Proposition 6.2).
- For order-`k` gaps: lower bounds for adaptive trees, the volume law for
  `k <= 2`, and the non-determination by the RLCT for `k > 2`
  (Theorem 7.1, Propositions 7.2 and 7.3(c)).
- Remark 7.4.

The mathematical content of Section 4 is modest. It evaluates the integrals
of [CN] and of Theorem 3.3 with standard asymptotics. The analytic geometry
is entirely from the literature. In particular, identifying sublevel-volume
exponents with RLCTs is classical (Arnold–Gusein-Zade–Varchenko; Watanabe
2009). Only its use in node-count characterizations is claimed here. The main
new technical content is Lemma 3.2, Theorem 3.3 and Lemma 3.3a: projecting to
faces removes (QD) and the vertex log.

**Not examined.** Aoyagi–Watanabe (2005) directly; Watanabe (2009); the
interval-analysis literature beyond the cluster papers above (Ratschek–Rokne,
Csendes–Ratz, Schöbel–Scholz); Zhigljavsky's random-search books. Uniform
random search needs about `1/V(eps) ≍ eps^(-lambda)` samples to hit `E(eps)`,
so the RLCT enters there trivially. Whether this is stated in terms of RLCTs
was not checked. The full texts of the 2026 arXiv papers were not read.

## 9. Limitations and open questions

- **Constants.** The upper constants (`12^n Lambda_2^(n/2)`) are exponential
  in `n`. They are far above the observed ratios of leaves to the lower
  bound: 3.4–19 for the other instances of Table 5.2, and 22–48 for `face4d`. The lower constant has the
  AM–GM loss of [CN, Theorem 3.1].
- **Constraints.** Everything here is for box-constrained problems. With
  constraints, faces become the strata of [CN, Section 4]. The analogue of
  Lemma 3.2 on curved strata, and RLCTs on semianalytic strata, are open.
- **Analyticity** is used only in Lemma 2.2. For `C^{1,1}` functions,
  Corollary 3.4 holds with the integrals `I_F`, which need not have
  power-log asymptotics.
- **Vertices.** Under (A1), bisection has no log gap against `N_opt`,
  including at optimal vertices of `X0` (Lemma 3.3a, Corollary 3.4).
  [CN, Example 3.4] uses a nonsmooth interior minimizer. Sharp vertex
  minimizers (`m >= c|y - v|`) cause no gap for any continuous `f`, by the
  pruning argument of Lemma 3.3a(a). Nonsmooth vertex minimizers that are
  not sharp are not treated.
- **Noisy SLT** (Conjecture 6.3) and the reduced-rank rows with `0 < r < H`
  are not proved.
- **Order `k > 2`.** Proposition 7.2(d) gives only bounds. Is there an
  algebraic invariant, such as the RLCT of an anisotropic sublevel family or
  a "Minkowski-sausage" threshold, that gives `e_k`? In Newton-nondegenerate
  cases one might expect a formula in terms of the Newton polyhedron
  truncated at slope `k`. This was not attempted.
- **Numerics.** These are floating-point computations of an idealized
  uniform bisection with exact alphaBB and `UBD = f*`. They are not solver
  runs and not certified counts.

## 10. Checks run

All commands were run from `research-20260929/rlct/` (Python 3, NumPy 2.5.1,
SciPy 1.18.0). They are targeted checks for this note only. No project-wide
verification was run, CI was not inspected, and nothing was committed.

- `python3 check_node_bounds.py > logs/check_node_bounds.log`: the batched
  node bounds against L-BFGS-B on 900 random boxes. Largest `lb - ref` was
  `4.4e-16`, largest `ref - ub` was `5.6e-17`, and the largest relative gap
  was `5.5e-12`.
- `python3 integrals.py > logs/integrals.log` (SciPy quadrature warnings
  filtered): the integrals `I_F(eps)`, the Theorem 3.1 lower bounds, local
  slopes and ratios to the Lemma 2.2 leading terms. Ratios at the finest
  `eps`: `xy2` 1.017, `sep24` 0.992, `xy2z4` 1.086, `bdry` edge 0.999, and
  `cusp` 0.81 (slow second pole). Also the `(xy - delta)^2` table of
  Section 6.
- `python3 fit_constants.py > logs/fit_constants.log`: the leading-constant
  fits of Section 5.
- `./run_sweep.sh` (231 bisection runs, `eps = 10^(-k/4)`, 16 parallel
  processes; output `logs/sweep.jsonl`), then
  `python3 analyze_sweep.py > logs/analyze_sweep.log`: Table 5.2 and the
  noisy-toy table. Every run had 0 undecided nodes.
- `python3 check_rrr_formula.py > logs/check_rrr_formula.log`: the
  reduced-rank formula against Drton–Plummer Table 1. All 9 entries match.
- `python3 order_k_counts.py > logs/order_k_counts.log`: the order-`k`
  level counts of Proposition 7.3(c).

Added in the revision (Section 11), also run from `research-20260929/rlct/`:
- `./run_revision.sh` (output `logs/revision_sweep.jsonl`): bisection for
  `vsharp` (`alpha = 1` and `8`), `vflat` and `rot`, with
  `eps = 1e-2 ... 1e-15`, and for `face4d` with `eps = 1e-1 ... 1e-6`.
  There were 0 undecided nodes. The counts are quoted after Corollary 3.4,
  in Example 4.3 and in Section 11.
- `python3 -W ignore revision_checks.py > logs/revision_checks.log` (the
  flag suppresses SciPy warnings; the same command as in Section 11.1). It
  covers:
  - F1: the level bound of Lemma 3.3a;
  - F2: `V(t)/t` for `(x+y)^2 + (x-y)^4` on `[0,1]^2`, which gives
    0.49901, 0.50000, 0.50000, 0.50000 at `t = 1e-2 ... 1e-8`, and its edge
    integral;
  - F3: the face and full integrals of `face4d`, as Laplace-transform
    integrals. The face slope is 0.7500, and the face lower bounds agree with
    the reviewer's to all printed digits. The full integral is 2128.63 at
    `1e-8` with slope 0.254; this was regenerated after the `H` quadrature
    was fixed (recheck item R5); the Dawson and split-quadrature routes
    agree at every `eps`, and the third route, run at `1e-8`, agrees there;
  - F4: the `x^3` edge integral, where `eps^(1/6) I` equals 2.784 at
    `1e-12`, tending to 2.804.

These checks illustrate the numbered statements. Every theorem rests on its
written proof.

## 11. Revision after review

The [review](../reviews/rlct-review.md) confirmed the core results. Its
checks reproduced all 111 bisection counts it compared, and it listed four
findings and eight minor points. Each was rechecked here before it was
adopted.

1. **F1: the vertex log term.** The review said it can be removed. Rechecked
   as follows.
   - The proof of Theorem 3.3 charges a cell to a vertex only if the witness
     lies within `s_j` of it. That cell is the corner cell, so at most one
     cell is charged per level.
   - The level bound and the edge-integral bound are Lemma 3.3a, reproved
     here with explicit constants. The same bound appears in
     `logs/revision_checks.log`.
   - Numerically, my own bisection reproduces the reviewer's counts exactly:
     16 constant leaves at a sharp vertex, and `log(1/eps)` growth when
     `g = 0`.

   Changes: Theorem 3.3 is restated with `N_v`, Lemma 3.3a is new, and
   Corollary 3.4, Theorem 4.1, Summary item 3 and the Section 9 bullet are
   corrected. The sentence "and it is real" is withdrawn.
2. **F2: Lemma 2.3(a) at boundary zeros.** Rechecked on
   `(x+y)^2 + (x-y)^4` on `[0,1]^2`:
   - `V(t)/t -> 1/2`, so the box RLCT is `(1, 1)` although `1/l = 3/4` in
     rotated coordinates;
   - bisection has 3 leaves per level, 73 leaves at `eps = 1e-15`, which is
     logarithmic growth.

   The consequence is now restricted to interior zeros, or to boundary zeros
   in coordinates where the box is locally a union of orthants. That case is
   proved with Lin's Lemma 4.1 majorant, whose monomial sum of squares is
   sign-symmetric. Summary item 4 is updated.
3. **F3: Example 4.3 was not a literal counterexample.** Correct: its
   `lambda = 5/4` exceeds `n/2`. Example 4.3(a) now uses the reviewer's
   four-dimensional instance. Its RLCT `(7/4, 1)` and the face RLCT
   `(3/4, 1)` were re-derived by sandwiching `E(t)`. The face integral was
   recomputed by an independent method (Laplace transform), and bisection
   was rerun with my code; the leaf counts match the reviewer's exactly.
   The 2D instance is kept as Example 4.3(b), an illustration outside the
   conjecture. The simpler failure `x(1-x)` on `[0,0.9]^3` was also added.
   Summary item 3 is updated.
4. **F4: `xy + x^3 + y^3`.** Correct: the edge integral grows like
   `eps^(-1/6)`, confirmed numerically, and this dominates the face's
   `log^2`. Summary item 2 now says so. Remark 4.1a records the following:
   - no known instance where a `lambda_F = d/2`, `theta_F >= 2` face
     governs;
   - `theta_F = 1` for zeros in the relative interior of `F`;
   - a sketch for the Newton-nondegenerate corner case.
5. **Minor points.**
   - (m1) Proposition 3.6: `t_0 = min(M r^2/2, s0^2/4)`. A cube of side `s`
     with a given vertex fits in `X0` only for `s <= s0/2`.
   - (m2) Corollary 3.4 now states that `C_0` depends on `s0` and on `m` at
     non-optimal vertices. `C_1` was also corrected; it is a sum, because
     edge integrals enter twice.
   - (m3) Proposition 7.2(c): for `C^{1,1}` `m` only the volume-form lower
     bound holds. The integral form is stated under (A2).
   - (m4) Lemma 2.3(b) now cites Lin's Theorem 1.3 with Propositions 4.3 and
     4.5.
   - (m5) Proposition 7.3(c) now uses a direct computation, because `y^2` has
     a minimizing segment that meets `∂X0`.
   - (m6) Proposition 6.2: `1 + log`, with `delta_0, eps_0 < 1`.
   - (m7) Summary item 4: interior zeros.
   - (m8) Kannan–Barton (2017), Lemma 10 and Corollary 4, are added as the
     fixed-width precedent for the face mechanism. They were checked in the
     local full text. The novelty paragraph now says that the RLCT–volume
     identification is classical.

Not changed: the reviewer's remark that Aoyagi–Watanabe's multiplicity is 2
for odd `M + H + N + r` in the balanced case was given from memory. It is
consistent with Drton–Plummer for `N = 5`, `M = 3`, but the note still uses
only Drton–Plummer's statement.

### 11.1 Second round, after the recheck

The [recheck](../reviews/rlct-recheck.md) found no broken theorem. It listed
eleven items, R1–R11. Each was checked before it was adopted.

1. **R1: `N_v <= J_v`.** The claim in Theorem 3.3 lacked a proof. The added
   proof applies steps 1–2 of Lemma 3.2 to all coordinates:
   `m(v) <= (1+n) m(y) + n M s_j^2 <= Lambda_1 s_j^2`, using
   `(n+2)^2/4 >= n+1`. Lemma 3.3a now credits review item F1 and assumes
   `M > 0`.
2. **R2: Section 9, "Vertices".** The bullet now says only what is proved:
   - no log gap under (A1);
   - no gap at sharp vertex minimizers for continuous `f`;
   - nonsmooth vertex minimizers that are not sharp are not treated.
3. **R3 and R4: Lemma 2.3.**
   - The sign conditions are now stated per part: none for (a), `h >= 0` on
     `X0` near the zero for the orthant case, and nonnegativity near 0 for
     (b).
   - The orthant argument now compares `h^2 <= c' sum omega^(2 alpha)`. Both
     sides are analytic, so Lin's Proposition 3.4 applies as stated, and the
     result is halved.
   - Summary item 4 now separates the local RLCT at a zero from the global
     `lambda`, and says "guaranteed only".
4. **R5: the full integral in Example 4.3(a) was wrong.** Confirmed.
   - *Cause.* `H(s) = integral_0^0.9 e^(-s x(1-x)) dx` was computed by one
     `quad` call with a breakpoint at `1/s`. For `s >= 1e6`, `s H(s)` came out
     as 0.6321 instead of 1. I rechecked this independently.
   - *Fix.* `H` now uses the closed form
     `s^(-1/2)[D(sqrt(s)/2) + e^(-0.09 s) D(0.4 sqrt(s))]`, with `D` the
     Dawson function. `revision_checks.py` also computes the full integral
     with `H` by a geometrically split quadrature, and by a third route with
     `x` outside and the cube inside by its Laplace transform.
   - *Agreement.* The Dawson and split-quadrature routes agree at every
     `eps` (184.679, 651.748 and 2128.63 at `1e-4, 1e-6, 1e-8`), matching
     the recheck; the third route, run at `1e-8` only, agrees there. The
     three routes share `laplace_integral` and the incomplete-gamma `G`, so
     they are not independent of each other; the second recheck confirmed
     the values by two routes of its own.
   - *Asymptotics.* The ratio to the leading term `21.599 eps^(-1/4)` is
     0.954, 0.986 and 0.995 at `1e-6`, `1e-8` and `1e-10`. The local slope,
     0.254 at `1e-8`, tends to `1/4` from above.
   - The log, Example 4.3(a) and Section 10 are updated. The conclusion,
     `eps^(-3/4)` against the conjectured `eps^(-1/4)`, is unchanged.
5. **R6: slopes.** On the half-decade grid, the least-squares slope over
   `[1e-6, 1e-3]` is 0.720, recomputed from `logs/revision_sweep.jsonl`. The
   two-endpoint slope is 0.748. Both are now reported, in Example 4.3(a) and
   Table 5.2.
6. **R7: Remark 4.1a.** The corner case is labelled as a sketch. It now lists
   three missing pieces:
   - an orthant version of Lemma 2.3(b);
   - zeros in the relative interior of proper faces of `F`;
   - Newton-degenerate cases.

   The redundant "no linear terms" is removed.
7. **R8–R11: consistency.**
   - Summary item 3 states the instance dependence of the bisection factor.
   - The status table no longer says "review confirmed" for restated
     results without saying which form was confirmed.
   - Section 9 has the current leaf-ratio ranges: 3.4–19 for the other
     instances, and 22–48 for `face4d`.
   - Section 10 has the corrected integral.

Checks for this round, run from `research-20260929/rlct/`:
- `python3 -W ignore revision_checks.py > logs/revision_checks.log`: three
  routes for the full integral agree, and the face values are unchanged;
- a least-squares slope computation on `logs/revision_sweep.jsonl`, which
  gives 0.720 (seven points) and an endpoint slope of 0.748.

No bisection run changed.

### 11.2 Root edits after the second recheck (2026-09-30)

The second recheck ([`reviews/rlct-recheck2.md`](../reviews/rlct-recheck2.md))
found every second-round change correct, confirmed the Example 4.3(a)
integrals by two routes of its own, and raised four wording points and two
optional clarifications. Each was checked against the text and the logs
before the text was changed. No theorem, number or conclusion changes.

1. **W1.** The header and the status rows of Lemma 2.3 and Theorem 3.3 now
   say that the second-round clarifications were checked in the second
   recheck, not in the first.
2. **W2.** The three-route agreement is stated as it was run: the Dawson
   and split-quadrature routes at every `eps`, the third route at `1e-8`
   only, with the shared components named (Section 10, F3, and
   Section 11.1, R5).
3. **W3.** "After the recheck fixed the `H` quadrature" became "after the
   `H` quadrature was fixed (recheck item R5)".
4. **W4.** Section 10 records the same command as Section 11.1,
   `python3 -W ignore revision_checks.py`; Section 9 and Section 11.1 say
   "3.4–19 for the other instances of Table 5.2".
5. **O1, O2 (optional).** Lemma 2.3 now says "is stated for" instead of
   "needs" for the sign conditions, and the cube `W` is centred at `z`.
6. **Not applied: O3** (a `max(0, ·)` in the proof of Lemma 3.3a(c)); the
   recheck notes that the final bound is true as written.
