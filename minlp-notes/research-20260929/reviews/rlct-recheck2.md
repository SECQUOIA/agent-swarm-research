# Second recheck of "Real log canonical thresholds and the node complexity of spatial branch-and-bound"

Date: 2026-09-30. Note under review:
`research-20260929/rlct/rlct-node-complexity.md` (cited as [N], with line
numbers of the current file). Earlier rounds: `reviews/rlct-review.md` and
`reviews/rlct-recheck.md` (cited as [R2]). I did not write or review any
earlier material.

Scope: only the second-round changes listed in [N] Section 11.1 (items
R1–R11). Everything else was taken as confirmed by the earlier rounds. The
note was not edited, and nothing was committed. My scripts and logs are in
`research-20260929/reviews/rlct-recheck2-checks/`.

## 0. Verdicts

| Item | Verdict |
|---|---|
| R1: proof of `N_v <= J_v` in Theorem 3.3; `M > 0` in Lemma 3.3a | **correct** |
| R3, R4: sign conditions in Lemma 2.3, the orthant argument with `h^2 <= c' g`, Lin's Proposition 3.4, Summary item 4 | **correct**; two optional clarifications (O1, O2) |
| R5: full integral of Example 4.3(a) | **correct**. I recomputed it by two routes, one of which uses no Laplace transform: 184.678977, 651.747836, 2128.63134 at `1e-4, 1e-6, 1e-8` |
| R6: least-squares vs endpoint slopes | **correct**: 0.7200 (seven points) and 0.7476 |
| R7: Remark 4.1a | **correct and properly labelled** as a sketch, with the three missing pieces |
| R2, R8–R11: consistency | **correct**, with four small wording fixes (W1–W4) |

No finding affects a theorem, a number or a conclusion. W1–W4 are about
reporting: who confirmed what, and which checks were run.

## 1. R1: `N_v <= J_v` and `M > 0`

**The added proof ([N] 476–482).** Every step checks.
- If the corner cell `D` at `v` is not pruned at level `j >= 1`, (U^q) gives
  a witness `y in D` with `m(y) < alpha' q_D(y) - eps <= Lambda_0 s_j^2 - eps`,
  because `q_D <= n s_j^2/4`. Since `D` is the corner cell,
  `|y - v|_inf <= s_j`.
- Lemma 3.2, step 1, needs `y - sigma s_j e_i in X0`. That point lies within
  `2 s_j <= s0` of `v_i`, because `j >= 1`. The one-sided bound
  `sigma ∂_i m(y) <= m(y)/s_j + M s_j/2` holds for every coordinate. It does
  not need the strict inequality in the definition of `I` in Lemma 3.2.
- Lemma 3.2, step 2, with all `n` coordinates moved (`d = 0`), gives
  `m(v) <= (1+n) m(y) + n M s_j^2`: each first-order summand is at most
  `m(y) + M s_j^2/2`, and `(M/2)|v - y|_2^2 <= n M s_j^2/2`.
- `(1+n) Lambda_0 + n M <= ((n+2)^2/4)(Lambda_0 + M) = Lambda_1`, because
  `(n+2)^2/4 - (n+1) = n^2/4 >= 0` and `n <= (n+2)^2/4`.
- The level satisfies `eps < Lambda_0 s_j^2`, so it is one of the `J` levels.
  Hence `N_v <= min(J, J_v)`.

This is exactly the argument that [R2] suggested, and it closes the gap
that [R2] item R1 identified. Corollary 3.4's `C_0` uses
`J_v <= 1 + log2(s0 sqrt(Lambda_1/m(v)))` for non-optimal vertices, and that
bound is right.

*Numerical illustration* (`logs/corner_cells.log`). For `face4d`
(`alpha' = 1.05`, `M = 3`, `Lambda_1 = 36.45`), I tested the corner cell at
each of the 16 vertices at levels 1–30, with `eps = 1e-3, 1e-8, 1e-14`. All
vertices are non-optimal. `N_v` is 1 or 2, and `J_v` is 3 or 4. The
inequality is loose here, as expected.

**`M > 0` ([N] 509).** Lemma 3.3a divides by `M` in `rho = max(g/M, sqrt eps)`
and in `c`. The assumption costs nothing, because (A1) with `M` implies (A1)
with any larger `M`. Only the constants change. The credit to review item F1
is now in the lemma ([N] 508).

*Optional (O3), not from the second round.* In the proof of (c) ([N] 538),
"`N_v <= 1 + log2(s0 (alpha' + M/2)/g)`" has a negative right-hand side when
`g > 2 s0 (alpha' + M/2)`, while `N_v = 0` there. The final bound (c) is
still true, because its right-hand side is at least 1, and whenever
`N_v >= 1` the intermediate bound holds. Writing `max(0, ·)` would make the
step literally true.

## 2. R3 and R4: Lemma 2.3

I read the relevant statements in the text of Lin, arXiv:1003.5338v3. This
is the copy [R2] extracted to `/tmp/rlctrecheck/lin.txt`; I read the
statements again myself. They are Theorem 1.3, Proposition 2.5 with the
convention after it, Propositions 3.3 and 3.4, the remark after Corollary
3.5, Lemma 4.1, the proof of Proposition 4.2, and Proposition 4.12.

**The orthant argument ([N] 322–342).** It is correct, and it is Lin's own
proof of Proposition 4.2, carried out on `Omega = X0 ∩ W` instead of a full
neighbourhood.
- Lin's Lemma 4.1 bounds `|h|` by `c sum_{alpha in S} |omega|^alpha`, where
  `S` generates `mon(<h>)`, and it needs no sign condition. Cauchy–Schwarz
  then gives `h^2 <= c|S| g` with `g = sum omega^(2 alpha)`, as in Lin's proof
  of Proposition 4.2.
- Lin's Proposition 3.4 states that if `f, g in A_Omega` (analytic over
  `Omega`) and `0 <= c f <= g` in `Omega` for some `c > 0`, then
  `RLCT_Omega(f) <= RLCT_Omega(g)`. Both `h^2` and `g` are analytic, so it
  applies as stated. This fixes the analyticity point raised in [R2] item R3.
- `g` is even in every coordinate. If `W` is a cube centred at `z`, the zeta
  integral of `g` over a union of `k` closed orthants of `W` is `k 2^(-n)`
  times the integral over `W`. The poles and orders are the same.
- On `W`, the RLCT of the ideal `mon(<h>)` is `(1/l, theta_l)` by Lin's
  Theorem 1.3, with equality for monomial ideals. Lin notes that `I` and
  `mon(I)` have the same Newton polyhedron, which is `P(h)`. For the single
  function `g`, which is the sum of squares of the generators, the pair is
  `(1/(2l), theta_l)`. This is the remark after Lin's Corollary 3.5, which
  [N] cites as Lemma 2.1(e).
- For one function, Lin's RLCT is the pole of `integral |f|^(-z)`. So
  `RLCT_Omega(h^2) = (lambda_z/2, theta_z)`, where `(lambda_z, theta_z)` is
  the box-restricted local RLCT of `|h|` at `z`. The conclusion
  `(lambda_z, theta_z) <= (1/l, theta_l)` follows. The ordering of pairs is
  preserved, because halving `lambda` keeps the order.
- Consistency check on Example 4.3(a): `P = conv{e_1, 4e_2, 4e_3, 4e_4} + R^4_+`
  meets the diagonal at `t = 4/7`, so the bound `7/4` is attained.

**Sign conditions ([N] 289–296).** They are stated per part, as [R2]
requested, and the Example 4.3 remark (`m < 0` for `x < 0`) is in place. All
three statements are true as sufficient conditions.

**Summary item 4 ([N] 63–71).** It now speaks of the local RLCT at an
interior zero `z`, bounded by `1/l`, with equality under positive
compact-face polynomials. It says that the global `lambda` is the minimum of
the local values, and that the boundary case is "guaranteed only" in orthant
coordinates. The deduction that the node exponent is at least `n/2 - 1/l` is
right in general, because `N_opt >= c I_{X0}(eps)` by Theorem 3.1.

**Optional clarifications.**
- **O1 ([N] 294–296 and 322–326).** The orthant argument does not use
  `h >= 0` on `X0`. Lemma 4.1 bounds `|h|`, `h^2 >= 0` holds automatically,
  and the note's convention is that the RLCTs of `h` are those of `|h|`.
  The condition is harmless, because `m = f - f* >= 0` on `X0` always, but
  "needs" suggests more than is used. Similarly, the route cited for (b),
  sos-nondegeneracy of `<h>` through Lin's Propositions 4.3 and 4.5(3),
  needs only that each `h_gamma` has no zero on the torus. The sign
  hypothesis in (b) is therefore also sufficient but not used. Nothing needs
  to change. If desired, write "is stated for" instead of "needs".
- **O2 ([N] 328).** "A small closed cube `W` around `z`" should be centred at
  `z`, which the evenness step needs. It should also be small enough that
  Lemma 4.1 holds on `W`, that `X0 ∩ W` is a union of orthants of `W`, and
  that `RLCT_{X0∩W}(h^2)` is the local value at `z`, in Lin's convention after
  Proposition 2.5. All of this is implicit in "small".

## 3. R5: the Example 4.3(a) integrals, recomputed independently

`I_full(eps) = integral_{X0} (m + eps)^(-2)` and
`I_face(eps) = integral_{[-0.4,0.5]^3} (S + eps)^(-3/2)`, with
`S = y^4 + z^4 + w^4`. Script: `face4d_integrals2.py`. Log:
`logs/face4d_integrals2.log`.

**Route B (no Laplace transform, Dawson function or incomplete gamma).**
- The `x`-integral in closed form: with `A = sqrt(1/4 + c)`,
  `F(c) = integral_0^0.9 (x(1-x) + c)^(-2) dx = 0.2/(A^2(0.09+c)) + 0.25/(A^2 c) + [ln((A+0.4)/(A-0.4)) + ln((A+0.5)^2/c)]/(4A^3)`.
  This form has no cancellation. It agrees with adaptive quadrature to
  `2e-16` at `c = 1e-2, 1e-6, 1e-10`.
- The cube is handled by a tensor-product composite Gauss–Legendre rule.
  Each coordinate is folded to `[0, 0.5]` (weight 2 on `[0, 0.4]`, weight 1
  on `[0.4, 0.5]`), with panels geometric in `eps^(1/4)`.
- Order 16 and order 24 with twice as many panels agree to about `1e-15`.
  A deliberately coarse order-6 rule differs by about `1e-8`, which shows
  that the rule is resolving the integrand.

**Route A (Laplace transform, written independently in mpmath, 25 digits).**
`I_full = integral_0^inf s e^(-s eps) H(s) G(s)^3 ds`, with `H` in the
`erfi` form
`H(s) = sqrt(pi)/(2 sqrt s) e^(-s/4)[erfi(sqrt(s)/2) + erfi(0.4 sqrt s)]`,
not the Dawson form used in [N].

| `eps` | route B | route A | [N] |
|---|---|---|---|
| `1e-4` | 184.678977 | 184.678977094 | 184.679 / 184.68 |
| `1e-6` | 651.747836 | 651.747836465 | 651.748 / 651.75 |
| `1e-8` | 2128.63134 | 2128.63134258 | 2128.63 |

The two routes agree to `2e-15`. Every half-decade value in the `I_full`
and `I_face` columns of `rlct/logs/revision_checks.log`, from `1e-2` to
`1e-10`, agrees with route B to all printed digits.

**Asymptotics.**
- The leading constants are `8 Gamma(5/4)^3 Gamma(1/4) = 21.599033` (full)
  and `8 Gamma(5/4)^3 Gamma(3/4)/Gamma(3/2) = 8.237437` (face).
- `I_full eps^(1/4)/21.599033` is 0.95421, 0.98552 and 0.99542 at `1e-6`,
  `1e-8` and `1e-10`. [N] gives 0.954, 0.986 and 0.995.
- `I_face eps^(3/4)/8.237437` is 0.999992 at `1e-8`. [N] gives 0.99999.
- The secant slope over the half decade ending at `1e-8` is 0.2543 (full)
  and 0.7500 (face). The derivative slope is 0.2537. The full slopes are
  0.2640, 0.2543 and 0.2513 at `1e-6`, `1e-8` and `1e-10`, so they decrease
  to `1/4` from above. [N]'s "0.254 at `1e-8`, tends to `1/4` from above" is
  right.

**The diagnosis.** I reproduced the old failure. One `quad` call with a
single breakpoint at `1/s` gives `s H(s) = 0.63212` at `s = 1e6` and `1e8`,
and 1.00020 at `1e4`. The closed form gives `1 + O(1/s)`. [N]'s account of
the cause is accurate.

**Wording point W2 ([N] 1439–1440).** "All three routes agree to the printed
digits: 184.679, 651.748 and 2128.63 at `1e-4, 1e-6, 1e-8`." In
`revision_checks.log`, the third route (`x` outside) was run only at `1e-8`.
The first two routes appear at every `eps`. Also, all three routes share
`laplace_integral` and the incomplete-gamma `G`, so they are not independent
of each other. Suggested wording: "The Dawson and split-quadrature routes
agree at every `eps`; the third route, run at `1e-8`, agrees there." The
values themselves are confirmed by route B above.

## 4. R6: slopes

Script: `face4d_slopes2.py`, which reads `rlct/logs/revision_sweep.jsonl`.
Log: `logs/face4d_slopes2.log`.
- The half-decade grid on `[1e-6, 1e-3]` has seven points, with leaves
  7531, 20371, 49996, 109201, 184936, 502336 and 1317301.
- The least-squares slope of `log(leaves)` against `log(1/eps)` is
  **0.7200**. The two-endpoint slope is **0.7476**. This matches [N] 781–783,
  Table 5.2 ([N] 894) and Section 11.1.
- Leaves divided by the face lower bound, from the face bounds in
  `revision_checks.log`: 29.8, 33.1, 33.9, 31.1, 22.2, 25.4 and 28.1 on this
  range, a spread of 1.53. Over the whole run they lie in 22.2–47.5. [N]'s
  "up to a factor of about 1.5" and "22–48" are right.
- `leaves · eps^(1/4)` grows from 76.5 to 41,657, a factor of 544.7. [N]
  says "about 540".

Table 5.2 defines the slope as the least-squares slope over the last three
decades, and the `face4d` row now reports that value and labels the
endpoint slope. This is consistent.

## 5. R7: Remark 4.1a ([N] 678–708)

- The corner case is headed "*Sketch, not a proof*". The status table
  ([N] 139) says "the Newton-nondegenerate corner case is only sketched".
- The three missing pieces from [R2] are listed: the orthant version of
  Lemma 2.3(b), zeros in the relative interior of proper faces of `F`, and
  Newton-degenerate cases.
- "No linear terms" is gone. The replacement sentence is right: all axis
  orders equal to 2 exclude every degree-1 monomial, because degree-1
  monomials are pure `x_i`. Together with `m(z) = 0`, every monomial then
  has degree at least 2. So `{sum alpha_i = 2}` supports `P`, and
  `P ∩ {sum alpha_i = 2} = conv{2 e_i}` is a facet containing
  `(2/d, ..., 2/d)` in its relative interior. This gives `theta_l = 1`.
- The axis-order-1 bullet is right: `conv{e_1, 2e_2, ..., 2e_d}` contains
  `(2/(d+1)) (1, ..., 1)`. It concludes `lambda_F = 1/l`, which relies on
  missing piece 1, and the remark says so.
- One case is not listed, as a remark only. If `m ≡ 0` along an edge of `F`
  (infinite axis order), that edge gives `eps^(-1/2)`, which also dominates.
  It fits under "edges govern", so nothing needs to change.

## 6. Consistency items (R2, R8–R11)

- **R2, Section 9 "Vertices" ([N] 1267–1273).** It now says what is proved
  and what is not. The sharp-vertex claim for continuous `f` is right as a
  statement about the corner cells at `v`. If `m >= c|t|_1` near `v`, then
  non-pruning under (U^q) forces `c < alpha' s_j`, so only boundedly many
  levels are charged.
- **R8, Summary item 3 ([N] 56–60).** It lists the dependence of the factor
  on `n, alpha, alpha', M, s0` and the smallest `m` at non-optimal vertices.
  This matches Corollary 3.4 ([N] 551–560).
- **R10, Section 9 "Constants" ([N] 1257–1260).** The ranges are right:
  3.4–19 without `face4d`, and 22–48 for `face4d`.
- **R11, Section 10 F3 ([N] 1323–1327).** The numbers are corrected.

**Wording fixes.**
- **W1 (status table, [N] 130 and 133; header, [N] 5–7).** The table says
  "recheck confirmed (sign conditions and squares clarified)" for Lemma 2.3,
  and "the recheck confirmed the restated form, with the `N_v <= J_v` step
  added" for Theorem 3.3. [R2] proposed these changes but did not see the
  revised text. The header does disclose that Section 11.1 was not
  re-reviewed. Now that this recheck has checked both texts, the root agent
  can say, for example, "recheck confirmed; second-round clarifications
  checked in `reviews/rlct-recheck2.md`", and update the header sentence.
- **W2** is in Section 3 above. The three-route agreement was checked at
  `1e-8` only.
- **W3 ([N] 1326).** "Regenerated after the recheck fixed the `H`
  quadrature": the recheck diagnosed the bug, and the note's revision fixed
  it. Suggested wording: "after the `H` quadrature was fixed (recheck item
  R5)".
- **W4 ([N] 1317 vs 1466; [N] 1259).**
  - Section 10 records `python3 revision_checks.py > logs/revision_checks.log`
    "(SciPy warning lines filtered)", while Section 11.1 records
    `python3 -W ignore revision_checks.py`. One command should be recorded.
  - Also, "3.4–19 for the instances of Table 5.2, and 22–48 for `face4d`"
    should say "the other instances", because `face4d` is itself a row of
    Table 5.2.

I found no silently strengthened claim among the second-round edits.

## 7. What I checked myself and what I took on trust

**Checked myself.**
- Every step of the added `N_v <= J_v` proof, the constant inequality, and
  the role of `M > 0`.
- The orthant argument and the sign conditions of Lemma 2.3, against Lin's
  text: Theorem 1.3, Proposition 2.5 and the convention after it,
  Propositions 3.3 and 3.4, the remark after Corollary 3.5, Lemma 4.1, the
  proof of Proposition 4.2, and Proposition 4.12.
- The full and face integrals of Example 4.3(a), by two routes of my own:
  - route B uses no Laplace transform and no special functions except `log`;
  - route A uses the `erfi` form of `H`, in 25-digit arithmetic.
- The leading constants, ratios and slopes.
- The old `H` failure.
- The LS and endpoint slopes, the leaf-ratio ranges and the `eps^(1/4)`
  growth, all from the note's own `revision_sweep.jsonl`.
- The corner-cell counts `N_v` against `J_v` for `face4d`.
- The logic of Remark 4.1a's sketch bullets.
- The consistency items R2 and R8–R11.

**Taken on trust.**
- The bisection counts in `revision_sweep.jsonl`. They were reproduced
  independently in [R2], and I did not rerun bisection.
- Lin's Theorem 1.3, as published.
- Everything outside the second-round changes.

## 8. Commands run

These were targeted checks only. No project-wide verification was run, CI
was not inspected, and nothing was committed. All commands were run
single-threaded from `research-20260929/reviews/rlct-recheck2-checks/`,
unless noted otherwise.

- `python3 face4d_slopes2.py > logs/face4d_slopes2.log` (under a second).
- `OMP_NUM_THREADS=1 python3 -W ignore face4d_integrals2.py > logs/face4d_integrals2.log`
  (1 min 54 s wall time; `logs/face4d_integrals2.time`). An earlier run of
  the same script had two defects. Its `F(c)` check used an inadequate
  `quad` at `c = 1e-10`, and its derivative slopes had the wrong sign. I
  fixed both and reran. The integral values did not change.
- `OMP_NUM_THREADS=1 python3 corner_cells.py > logs/corner_cells.log`.
- An inline Python command in `/tmp` reproducing `s H(s)` from the old
  single-breakpoint `quad` against the Dawson closed form at
  `s = 1e4, 1e6, 1e8`. The output is quoted in Section 3 and is not logged.
- `grep` and `sed` on `/tmp/rlctrecheck/lin.txt`, the Lin v3 text extracted
  by [R2], and on [N].

These are floating-point checks. The integrals agree across two independent
routes to about `1e-15`, relative to their size.
