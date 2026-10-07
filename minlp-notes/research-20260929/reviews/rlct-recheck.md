# Recheck of the revised note "Real log canonical thresholds and the node complexity of spatial branch-and-bound"

Date: 2026-09-29. Note under review:
`research-20260929/rlct/rlct-node-complexity.md` (cited as [N], with line
numbers of the current file). First review: `reviews/rlct-review.md`.
Background: `research-20260928b/.../instance-dependent-node-complexity.md`
(cited as [CN]), Sections 1, 3 and 6. I did not write or review the earlier
material. The note was not edited and nothing was committed. My scripts and
logs are in `research-20260929/reviews/rlct-recheck-checks/`.

## 0. Verdicts

| Item | Verdict |
|---|---|
| 1. Lemma 3.3a, Corollary 3.4 and Theorem 4.1 without the vertex term; constants `C_0`, `C_1` | **correct**, with two minor fixes (R1, R2) |
| 2. Revised Lemma 2.3 (interior zeros; boundary zeros in orthant coordinates) and its Lin citations | **correct**, with minor fixes (R3, R4) |
| 3. Literal counterexample `x(1-x) + y^4 + z^4 + w^4` | **correct**: RLCTs `(7/4, 1)` and `(3/4, 1)` rederived; `eps^(-3/4)` confirmed with my own bisection code. Two reported numbers are wrong (R5, R6); the conclusion is unaffected |
| 4. Remark 4.1a | first bullet **proved**; `xy + x^3 + y^3` bullet **correct**; the corner-case sketch is honestly labelled, but it has **gaps** beyond "degenerate cases" (R7) |
| 5. Consistency of the summary, status table and Section 8 | **consistent**, with small wording fixes (R8–R11). I found no silently strengthened claim |

No finding invalidates a theorem.

## 1. Lemma 3.3a and the vertex-free Corollary 3.4 and Theorem 4.1

### 1.1 Step-by-step check

**Theorem 3.3 as restated ([N] 440–474).** I rederived the charging argument.
- A non-pruned level-`j` cell `D`, with `j >= 1`, has a witness `y in R_D ⊆ D`
  with `m(y) < Lambda_0 s_j^2 - eps`.
- If Lemma 3.2 projects `y` to a vertex `v`, then `|y - v|_inf < s_j`. Because
  `v` is a grid point, the only closed level-`j` cell containing `y` is the
  corner cell. So each level charges at most one cell to `v`, and that cell is
  not pruned.
- The face part (`6^n` cells per packing point, disjoint `Q_F(z, s_j/2)`,
  `E(Lambda_1 s_j^2) ⊆ {m + eps <= Lambda_2 s_j^2}`, and the geometric sum
  `<= 2 theta^(-d)`) is as confirmed in the first review.

**Lemma 3.3a ([N] 476–508).** Every step checks.
- (a) The descent lemma gives
  `m(y) >= sum_i ∂_i m(v) t_i - (M/2)|t|^2 >= |t|_1 (g - M s_j/2)`, using
  `|t|_2^2 <= s_j |t|_1` on the corner cell. Also `q_D <= s_j |t|_1`.
  Non-pruning under (U^q) gives `z in R_D ⊆ D` with
  `m(z) < alpha' q_D(z) - eps`. Here `z != v`, because at `v` this would read
  `0 < -eps`. Dividing by `|t|_1 > 0` gives `g - M s_j/2 < alpha' s_j`.
- (b) Along the minimizing edge, `m <= g tau + M tau^2/2 <= (3M/2) tau^2` for
  `tau >= g/M`, and `eps <= tau^2` for `tau >= sqrt eps`. Integrating over
  `[rho, s0]` gives the bound. The edge has length `s0` because `X0` is a
  cube.
- (c) The two level counts are `log2(s0(alpha'+M/2)/g)` and
  `1 + log2(s0 sqrt(Lambda_0/eps))`. In each case of `rho`, the smaller one is
  at most `1 + c + log2(s0/rho)`. The case `rho > s0` is handled because the
  last term is then negative. The bound is uniform in `g`, as claimed.

**Corollary 3.4 constants ([N] 510–527).** Recomputed.
- For optimal `v`: `sum_v N_v <= (1+c) #opt + (3M/2+1)^(1/2)/log 2 · sum_v I_{E(v)}`.
- Each edge serves at most its two endpoints, so the second sum is at most
  `2 sum_{edges} I_E`.
- With `Lambda_2^(d/2) <= max(1, Lambda_2^(n/2))`, this gives exactly
  `C_1 = 2^n[2·6^n max(1, Lambda_2^(n/2)) + 2(3M/2+1)^(1/2)/log 2]` and the
  stated `C_0`.
- `C_1` depends only on `n, alpha', M`. `C_0` depends on `s0`, on the values
  of `m` at the non-optimal vertices, and, through `c`, on `n, alpha', M`.
  The stated dependence is right.

**Theorem 4.1 ([N] 621–643).** Inserting Lemma 2.2 into the new Corollary 3.4
gives `c kappa* <= N_opt <= |T_bis| <= C kappa*`, because `kappa* >= 1` for
`eps < 1/e`. The vertex term is no longer needed. Correct.

### 1.2 Cases and attempted counterexamples

- **Sharp vertex (`g > 0`).** By (a), only boundedly many levels are charged.
- **Flat along an edge (`g = 0`).** By (b), `I_E >= c log(1/eps)`, so the
  charged levels, at most `J ≍ log(1/eps)`, are absorbed.
- **Flat along a 2-face or higher face through `v`.** Its edges through `v`
  then have `g = 0`, so this is the previous case. The face's own integral is
  charged separately.
- **Small `g > 0` (a near-flat vertex, or a vertex that is a limit of near-minimizers).**
  The bound is uniform in `g`. I tested `m = delta(x+y) + x^2 + y^2` on
  `[0,1]^2` with `delta = 1e-1 ... 1e-7` and `eps = 1e-4 ... 1e-16`. The
  number of non-pruned corner-cell levels divided by `I_E` stayed in
  0.80–1.27, and bound (c) always held (`logs/vertex_uniform.log`).
- **Nonsmooth objectives.** Lemma 3.3a uses (A1) only through the descent
  lemma. For any continuous `m` with a sharp vertex minimizer, `m >= c|t|`,
  the same pruning argument works directly. For nonsmooth, non-sharp vertex
  minimizers nothing is proved (see R2).

Under (A1) I found no counterexample, and I see no route to one. The
argument covers every vertex configuration, because the only cells charged to
a vertex are corner cells, and their count is controlled by the minimal
inward slope.

**Numerical reproduction with my own code** (`sepbisect.py`, which tabulates
exact per-coordinate node minima; `logs/vertex_bdry_own.txt`):
- `vsharp`: 16 leaves for every `eps` from `1e-2` to `1e-15` with `alpha = 8`,
  and 1 leaf with `alpha = 1`.
- `vflat`: 7, 13, 19, 22, 28, 34, 37, 43, 49, 52, 58, 64, 67, 73 leaves at
  `eps = 1e-2 … 1e-15`.

Both match [N] and `logs/revision_sweep.jsonl` exactly.

### 1.3 Fixes

- **R1 (minor; [N] 444–446).** "`N_v(eps) <= min(J, J_v)`" is true, but the
  proof shows only that the number of cells *charged* to `v` is at most
  `1{m(v) <= Lambda_1 s_j^2}` per level. `N_v` counts every level at which the
  corner cell is not pruned, including cells charged elsewhere. Add one line:
  - the witness `y` in the corner cell has `|y - v|_inf <= s_j`;
  - Lemma 3.2 steps 1–2, applied to all `n` coordinates, give
    `m(v) <= (1+n) m(y) + n M s_j^2 < ((1+n) Lambda_0 + n M) s_j^2 <= Lambda_1 s_j^2`.

  Alternatively, define `N_v` as the number of charged levels.
- **R2 (minor; Section 9 "Vertices", [N] 1212–1214).** "The log gap of
  [CN, Example 3.4] needs a nonsmooth minimizer that is not a vertex of the
  root box." The first half is proved: under (A1), Corollary 3.4 leaves no
  gap. The second half is proved only for sharp vertex minimizers. For
  nonsmooth, non-sharp vertex minimizers nothing is shown. Suggested wording:
  "Under (A1) there is no log gap. [CN, Example 3.4] uses a nonsmooth interior
  minimizer. Sharp vertex minimizers cause no gap for any continuous `f`.
  Other nonsmooth vertex minimizers are not treated." The sentence after
  Corollary 3.4 ([N] 533–535) is already accurate.
- (Cosmetic.) Lemma 3.3a divides by `M`. State `M > 0`; this loses nothing,
  because `M` can be increased.

## 2. Revised Lemma 2.3

I downloaded arXiv:1003.5338v3 myself, extracted it with `pdftotext`, and
read Sections 3–4. I also used WebFetch for the arXiv abstract page: the
paper is J. Algebraic Statistics 8(1), 2017, and v3 is dated 2017-02-13.

**What Lin states (verified in the text).**
- *Theorem 1.3.* For `I` finitely generated and 0 in the **interior** of
  `Omega`, `RLCT_{Omega_0}(I; omega^tau) <= (1/l_tau, theta_tau)`. Equality
  holds if `I` is monomial or sos-nondegenerate.
- *Proof of Theorem 1.3.* Equality comes from Proposition 4.5, Theorem 4.8
  and Theorem 4.10. The inequality comes from Propositions 4.2 and 4.12.
- *Lemma 4.1.* `|f| <= c sum_{alpha in S} |omega|^alpha` on a small
  neighbourhood, where `S` generates `mon(<f>)`.
- *Proposition 4.3.* `I_gamma = <f_{1,gamma}, ..., f_{r,gamma}>` for compact
  faces.
- *Proposition 4.5.* sos-nondegeneracy is equivalent to (3):
  `V(I_gamma) ∩ (R*)^d = ∅` for all compact faces.
- *Proposition 3.4.* `0 <= c f <= g` with `f, g in A_Omega` implies
  `RLCT(f) <= RLCT(g)`.
- *Proposition 3.3.* The full-neighbourhood value is at most the
  boundary-restricted value.
- *Convention.* The RLCT of a set of functions is the pole of
  `∫(sum f_i^2)^(-z/2)`. So for one function `h >= 0` it is the pole of
  `∫ h^(-z)`, and `RLCT(<h>) = RLCT(h)`. `P(<h>) = P(h)`.
- *Lin's nondegeneracy.* "Singular" means `f_gamma = ∂f_gamma = 0`.

**(a), interior zeros ([N] 294–302).** Correct. At `z in int X0` the
box-restricted and full values agree, and Lemma 2.1(d) gives
`lambda <= lambda_z <= 1/l`.

**Counterexample at boundary zeros ([N] 303–309).** Correct. I rederived it
by hand.
- Near 0 the box is `{u >= |v|}`, and `dx dy = du dv/2`.
- The `(u,v)`-area of `{u^2 + v^4 <= t, |v| <= u}` is `t - O(t^(3/2))`.
- So `V(t) = t/2 (1 + o(1))`, the box RLCT is `(1, 1)`, and `1/l = 3/4` in
  `(u, v)`.
- Since `m >= 0` on `R^2`, Corollary 4.2(ii) applies, and the count is
  `log(1/eps)`.

**Orthant case ([N] 309–319).** Correct.
- Lemma 4.1 needs no sign condition.
- `sum_{alpha in S} omega^(2 alpha)` is even in every coordinate. So on a
  sign-symmetric neighbourhood its zeta integral over a union of `k`
  orthants is `k 2^(-n)` times the full one, with the same poles and orders.
- The full value is `(1/l, theta_l)` by Theorem 1.3 with equality for the
  monomial ideal `mon(<h>)`, whose polyhedron is `P(h)`.
- Comparison then gives the bound.
- Consistency check on Example 4.3(a): in box coordinates,
  `P = conv{e_1, 4e_2, 4e_3, 4e_4} + R^4_+` meets the diagonal at `4/7`.
  This gives `1/l = 7/4 = lambda`, so the bound is attained.

**(b) ([N] 321–338).** Correct.
- The citation route through Propositions 4.3 and 4.5(3) and Theorem 1.3 is
  valid for `<h>`. Theorem 1.3 applies Theorems 4.8 and 4.10 to `h^2`, whose
  face polynomials `h_gamma^2` have no torus zeros.
- The limit formula for `h_gamma >= 0` needs `beta` in the interior of the
  normal cone of a compact face. Such `beta` has all entries positive, so
  `s^beta y -> 0`.
- The step "zero of a nonnegative polynomial ⇒ singular point in Lin's
  sense" is right.

**Remark after (b) ([N] 340–351).** Correct.
- In the chart `x = mu_1 mu_2`, `y = mu_2`, `x + y = mu_2(mu_1 + 1)`. The
  unit `g` of Lin's Theorem 4.10 proof vanishes at `mu_1 = -1`, so the claimed
  value `(2, 1)` fails, while the true value is `(1, 1)`.
- Lin's Remark 4.6 acknowledges that `x + y` is nondegenerate as a function
  but not sos-nondegenerate as an ideal.

**Fixes.**
- **R3 (minor; [N] 284 and 309–319).** The hypothesis of Lemma 2.3 is
  "`h >= 0` near 0". The orthant argument needs `h >= 0` only on `X0` near
  `z`, and that is the relevant case: in Example 4.3, `m < 0` for `x < 0`.
  Say so in the orthant bullet. Also, Lin's Proposition 3.4 is stated for
  analytic `f, g`, while `(sum omega^(2 alpha))^(1/2)` is not analytic.
  Compare `h^2 <= c sum omega^(2 alpha)` instead and halve, or say that the
  Laplace-integral comparison is used directly.
- **R4 (wording; Summary item 4, [N] 59–65).**
  - "`lambda <= 1/l`. Equality holds when …" mixes the global `lambda` with
    the local RLCT at the zero. Equality is for the local value at that zero.
    The global `lambda` is the minimum over zeros.
  - "this holds only in coordinates in which …" would read better as "is
    guaranteed only in coordinates in which …". In other coordinates it can
    fail, but it need not.

## 3. The literal counterexample (Example 4.3(a))

### 3.1 RLCTs, derived independently

**Full box.** On `[0, 0.9]`, `x/10 <= x(1-x) <= x`. So
`{x <= t/2} x {S <= t/2} ⊆ E(t) ⊆ {x <= 10t} x {S <= t}`, with
`S = y^4 + z^4 + w^4`.
- Since 0 is interior to `[-0.4, 0.5]^3`,
  `vol{S <= t} = t^(3/4) vol{S <= 1}` for small `t`.
- Hence `c_1 t^(7/4) <= V(t) <= c_2 t^(7/4)`, which forces
  `(lambda, theta) = (7/4, 1)`.
- As a cross-check, Lin's Proposition 3.7 gives `(1 + 3·1/4, 1)`.
- `7/4 < n/2 = 2`, so the conjecture predicts `eps^(-1/4)`.

**Face `x = 0`.** `S` is separable with RLCT `(3/4, 1)` and `d = 3`, so
`I_face ≍ eps^(-3/4)`.
- Exact leading term: `c_Z = (2 Gamma(5/4))^3`, so
  `I_face ~ 8 Gamma(5/4)^3 Gamma(3/4)/Gamma(3/2) · eps^(-3/4) = 8.237437 eps^(-3/4)`.
- My computed `I_face eps^(3/4)` is 8.235379 at `1e-6` and 8.237071 at `1e-7`.

**Other faces.** The only zero is the origin. A face contains it only if it
fixes nothing except `x = 0`. So every other face has `min m > 0`, and
Theorem 4.1 gives `N_opt ≍ |T_bis| ≍ eps^(-3/4)`.

**Hypotheses.**
- `X0` is a cube of side 0.9.
- Exact alphaBB with `alpha = 1.05 >= 1` is a valid convex underestimator,
  because the Hessian of `f_B` is `diag(2alpha - 2, 12y^2 + 2alpha, …)`.
- `f` is a polynomial, so the conjecture's hypotheses hold.

**The simpler instance** `x(1-x)` on `[0,0.9]^3`.
- `V(t) ≍ t`, so the RLCT is `(1, 1)` with `1 < 3/2`.
- The face `x = 0` has `m ≡ 0`, so `I_F = 0.81/eps` and Theorem 3.1 gives
  `(2 alpha/pi^2) 0.81 eps^(-1)`.

Correct.

### 3.2 My own bisection code

`sepbisect.py` is written from scratch; I did not reuse the authors' or the
first reviewer's scripts.
- **Model.** Exact alphaBB, `UBD = f* = 0`, uniform `2^n`-ary refinement,
  and pruning iff `LB >= -eps`.
- **Node bounds.** Because `f_B` is separable, `LB` is a sum of
  one-dimensional convex minima. These are computed by 80-step bisection on
  the monotone derivative and tabulated per level.
- **Near-ties.** Every near-tie with `|LB + eps| < 1e-10` is re-decided in
  60-digit `mpmath`.

**Results** (`logs/face4d_own.jsonl`, 25 values `eps = 10^(-k/4)`, from `1e-1` to `1e-7`):
- Leaves are 136, 1066, 7531, 49996, 184936, 1317301 and 8361361 at
  `eps = 1e-1, …, 1e-7`. They match [N]'s 136 … 1,317,301 and the first
  review's 8,361,361 exactly.
- 1281 near-ties were rechecked in `mpmath`, with 0 flips.
- Leaves divided by the Theorem 3.1 face bound stay in **22.2–48.1** over all
  25 values (a factor of 2.17). [N] says 22–48.
- `leaves · eps^(3/4)` stays in 24–51.
- `leaves · eps^(1/4)` grows from 76.5 to 41,657 between `1e-1` and `1e-6`, a
  factor of **545** ([N]: about 540). It reaches 148,688 at `1e-7`.
- Least-squares slopes of `log(leaves)`: 0.741 over `[1e-6, 1e-3]` on the
  quarter-decade grid, 0.740 over `[1e-7, 1e-4]`, and 0.762 over
  `[1e-7, 1e-1]`.

The conjecture's `eps^(-1/4)` is clearly refuted. The count follows
`eps^(-3/4)`.

The `bdry` illustration is also reproduced: 73, 232 and 7651 leaves at
`1e-4`, `1e-6` and `1e-12`, with 0 flips. Its full two-dimensional integral,
computed with the inner integral in closed form, is 8.284388 at `1e-12`, as
in [N].

### 3.3 Two wrong numbers

- **R5 (numerical error; [N] 723–726, Section 10 item F3, `logs/revision_checks.log`).**
  The `I_full` column in `revision_checks.log` is wrong for `eps <= 1e-4`, and
  so is the sentence "the full four-dimensional integral grows only with slope
  0.24".
  - *Cause.* `H(s) = ∫_0^0.9 e^(-s x(1-x)) dx` is computed by `quad` with a
    single breakpoint at `1/s`. For `s >= 1e6` the part beyond `1/s` is lost,
    so `H(s)·s = 0.6321 = 1 - e^(-1)` instead of 1 (`logs/H_diagnosis.log`).
  - *Correct values.* I used two independent routes: the closed form
    `h(s) = s^(-1/2)[D(sqrt(s)/2) + e^(-0.09 s) D(0.4 sqrt(s))]` with Dawson's
    function `D`, and an outer-`x` quadrature of a Laplace-transformed inner
    integral. The routes agree to about `1e-16`.

    | `eps` | log value | correct value |
    |---|---|---|
    | `1e-4` | 181.67 | 184.679 |
    | `1e-6` | 495.71 | 651.748 |
    | `1e-8` | 1429.5 | 2128.631 |

  - *Asymptotics.* The leading term is
    `8 Gamma(5/4)^3 Gamma(1/4) eps^(-1/4) = 21.599 eps^(-1/4)`. The ratio to it
    is 0.954, 0.986 and 0.995 at `1e-6`, `1e-8` and `1e-10`.
  - *Local slopes.* 0.262, 0.254 and 0.251 at `1e-6`, `1e-8` and `1e-10`. They
    approach `1/4` from above, not from 0.24 below.
  - *Fix.* Fix `H` in `revision_checks.py`, regenerate the log, and change the
    sentence to "slope about 0.25 (0.254 at `eps = 1e-8`)". The qualitative
    point, `eps^(-1/4)` against `eps^(-3/4)`, is unaffected.
  - The `I_face` column is right. My values agree with it to all printed
    digits and were cross-checked by direct cubature to `3e-14`.
- **R6 (reporting; [N] 729 and Table 5.2, line 840).** "The slope over
  `[1e-6, 1e-3]` is 0.748" is the **two-endpoint** slope. Table 5.2 defines
  the slope as the least-squares slope over the last three decades. On the
  note's own half-decade grid (seven points) that is **0.720**; on my
  quarter-decade grid it is 0.741. Report the least-squares value, or say
  that the reported value is an endpoint slope. Dyadic oscillation, up to a
  factor of 1.5, explains the spread. The conclusion is unaffected.

## 4. Remark 4.1a: what is proved and what is sketched

- **Proved: `theta_F = 1` when all zeros of `m|_F` lie in the relative interior of `F`.**
  Lemma 2.4's proof transfers to `F`, with `m|_F` analytic in its affine hull
  and its zeros critical in `F`.
  - A singular Hessian gives `V_F(t) >= c t^((d-1)/2 + 1/3)`, so
    `lambda_F < d/2`.
  - Otherwise the zeros are finitely many and nondegenerate. The Laplace
    method then gives `theta_F = 1`.
- **Verified: the `xy + x^3 + y^3` example.**
  - My own log-scale quadrature (`logs/remark41a_check.log`) gives
    `(V - (1/3) t log(1/t))/t = 0.33333` for `t = 1e-8 … 1e-12`.
  - `V/(t log(1/t)) = 0.3478` at `1e-10`, against [N]'s 0.348.
  - The edge integral satisfies `eps^(1/6) I = 2.784` at `1e-12` and 2.800 at
    `1e-16`. The limit is `Gamma(1/3) Gamma(1/6)/(3 Gamma(1/2)) = 2.80436`.
- **Sketch (Newton-nondegenerate corner).** The case logic is right:
  - axis order greater than 2 gives an edge exponent `1/k - 1/2 < 0`, which
    dominates any `log^theta`;
  - axis order 1, with the others at most 2, gives
    `l <= 2/(d+1) < 2/d`;
  - all axis orders equal to 2 gives the facet
    `P ∩ {sum x_i = 2} ⊇ conv{2e_i}` of codimension 1, which contains
    `(2/d, …, 2/d)` in its relative interior, so `theta = 1`.

  The sketch is honestly labelled. **R7: its gaps go beyond "degenerate cases".**
  1. It needs an **orthant** version of Lemma 2.3(b):
     `lambda = 1/l` and `theta = theta_l` on `R^d_{>=0}` when the face
     polynomials are positive on `(R_{>0})^d`. Lemma 2.3(b) is a
     full-neighbourhood statement for `h >= 0` near 0, and Lin's Theorem 1.3
     assumes 0 is interior. With a linear term (axis order 1), `m` is not
     `>= 0` on a full neighbourhood. Its face polynomials cannot be positive on
     the whole torus, so Lemma 2.3(b) does not apply as stated. The orthant
     version is standard toric bookkeeping but is not in the note.
  2. It covers zeros at corners of `F` only. Zeros in the relative interior
     of a proper face of `F` of positive dimension are not treated.
  3. "And there are no linear terms" is redundant: all axis orders equal to 2
     already excludes every degree-1 monomial.

  The status-table entry "no governing instance known; open" is consistent
  with this. It could add "relative-interior case proved; corner case
  sketched".

## 5. Consistency and claim strength

- **Summary items 1–3, the status table and Section 8** match the corrected
  statements. I found no silently strengthened claim. Two changes do add
  claims, and both are disclosed with proofs:
  - the new "no log loss at vertices" claim (Lemma 3.3a, status table, Section
    8 novelty list);
  - the orthant extension of Lemma 2.3(a).

  Lemma 3.3a's argument originates in review item F1. The status table credits
  this; Lemma 3.3a itself does not.
- **R8 (Summary item 3, [N] 53–56).** "bisection is within a constant factor
  of `N_opt`" is right if "constant" means independent of `eps`. The constant
  depends on `s0` and on `min{m(v) : m(v) > 0}` (Corollary 3.4, [N] 522–526).
  Name this dependence, as the corollary does.
- **R9 (status table, [N] 127 and 132).** "review confirmed" is attached to
  Theorem 3.3 and Theorem 4.1. Both were restated in the revision (the `N_v`
  form, and the removed vertex term). The first review endorsed the change,
  but did not check these texts. Say "earlier form review-confirmed; restated
  per F1".
- **R10 (Section 9 "Constants", [N] 1203–1205).** "the observed ratios of
  4–19" is outdated. Table 5.2 now contains `face4d` at 22–48 and `bdry` at
  3.4–7.4. The sentence after Corollary 4.2 ([N] 702–703) concerns the
  interior instances and remains accurate.
- **R11 (Section 10, F3 bullet, [N] 1265–1267).** This bullet inherits R5.

## 6. What I checked myself and what I took on trust

**Checked myself.**
- Every step of Lemma 3.3a, of the restated Theorem 3.3 (including the
  missing `N_v <= J_v` argument, R1), of Corollary 3.4 and its constants, and
  of Theorem 4.1.
- The revised Lemma 2.3(a) and (b) and the remark after it, against the text
  of Lin v3: Theorem 1.3 and its proof, Lemma 4.1, Propositions 3.3, 3.4,
  4.2, 4.3, 4.5 and 4.12, Theorems 4.8–4.10, and Remark 4.6.
- The boundary counterexample `(x+y)^2 + (x-y)^4`, by hand.
- The RLCTs `(7/4, 1)` and `(3/4, 1)`, and the leading constants of both
  integrals.
- The `face4d`, `bdry`, `vsharp` and `vflat` bisection counts, with my own
  code.
- The `face4d` integrals, by two methods each. `I_full` was also checked by
  a closed form.
- Remark 4.1a's first bullet, and the `xy + x^3 + y^3` asymptotics.
- The consistency items in Section 5.

**Taken on trust.**
- The correctness of Lin's Theorems 1.3, 4.8 and 4.10 in the sos-nondegenerate
  case as published.
- Lemma 2.1 (unchanged; checked in the first review).
- Everything in Sections 5–8 that the revision did not touch.
- The authors' remaining logs, which I read but did not regenerate.

## 7. Commands run

These were targeted checks only. No project-wide verification was run, CI
was not inspected, and nothing was committed. All commands below were run
from `research-20260929/reviews/rlct-recheck-checks/` unless a path is
given.

- `curl -sL -o lin.pdf https://arxiv.org/pdf/1003.5338v3 && pdftotext -layout lin.pdf lin.txt`
  (in `/tmp/rlctrecheck`), then `sed` and `grep` on the text. WebFetch was
  used on `https://arxiv.org/abs/1003.5338` for the version and journal data.
- `python3 sepbisect.py face4d 1.05 <25 values 10^(-k/4), k=4..28>` →
  `logs/face4d_own.jsonl`. This took about 11 seconds.
- `python3 -W ignore face4d_integrals.py` → `logs/face4d_integrals.log`. It
  contains the integrals, face and full lower bounds, ratios, slopes, and the
  Laplace-versus-cubature and closed-form-`h`-versus-quadrature checks.
- `face4d_full_check.py`, run through `runpy` → `logs/face4d_full_check.log`
  (the second route for `I_full`).
- A slope computation → `logs/face4d_slopes.log`.
- `python3 sepbisect.py vsharp 8 …; vsharp 1 …; vflat 1 …` over
  `eps = 1e-2 … 1e-15`, and `bdry 1.05` at six values of `eps` →
  `logs/vertex_bdry_own.jsonl` and `.txt`.
- `python3 vertex_uniform.py` → `logs/vertex_uniform.log` (uniformity of
  Lemma 3.3a in `g`).
- `python3 remark41a_check.py` → `logs/remark41a_check.log`.
- An inline script → `logs/bdry_full_integral.log`.
- An inline script importing `rlct/revision_checks.py` →
  `logs/H_diagnosis.log`. This is the only use of the authors' code, and it
  was used only to diagnose R5.

These are floating-point illustrations, not certified counts. The pruning
decisions near ties were confirmed in 60-digit arithmetic.
