# Review of `theory-decomposition/adaptive-matching.md` (graded refinement GR)

Date: 2026-09-30. Independent, adversarial review. I did not write the note.
Scope: the note, its scripts and logs in `theory-decomposition/adaptive2/`,
and the parts of [D] (`decomposition-certificates.md`), [E]
(`extension-adaptive.md`) and [Cov] (`covering-upper-half.md`) that it uses.
My scripts and logs are in
[`adaptive-matching-review-checks/`](adaptive-matching-review-checks/).
Only targeted checks were run. No project-wide verification was run and no
CI results were consulted.

Labels used below. **Checked by hand**: I went through the argument line
by line. **Float-checked**: double-precision computation, not certified.
Nothing here was checked in exact arithmetic or in Lean.

## 1. Verdict

The mathematical core holds. I checked Lemma 1, Theorem 2, Corollary 3,
Corollary 4 and Proposition 6 by hand and found no error that breaks a
stated result. With independent code I reproduced the main computations
exactly. The reproduced runs are GR on the path family for n = 4, 8 and 16,
the θ = 1/4 failure at n = 32, rule `bd` for n = 4..256, and the first tree
runs (Section 7).

Fixes are needed in five places:

1. **Remark 3.3 (trees) overstates the reduction.** One step it lists as
   path-independent is not, and it omits a condition. The slope bound "at
   most `k − 1` bags of `sub(t)` contain a variable of `S_t`" is false on
   trees when `k ≥ 3` and `w ≥ 2`; only the constant changes. More
   important, the induction of Theorem 2 needs a `K` with
   `K_1(γ(K), θ) ≤ K`. That fixed point exists
   for Lemma 1's `K_1`, which grows like `sqrt(γ) + θγ`. It does not follow
   from "the conclusion of Lemma 1 holds with some `K_1(γ, θ)` independent
   of `|T|`". So Conjecture 7 needs a growth condition in `γ`, and "the open
   problem for trees is therefore exactly ..." should be softened
   (Section 4).
2. **The comparison of conditioning in Sections 8.3–8.4 and Summary item 3
   is not supported.** The note calls the `b = 0.88` path (`c_g = 0.02`) and
   the `b = 0.62` tree (`c_g ≥ 0.023`) "similar conditioning". These
   numbers are lower bounds for infinitely large instances. At the tested
   sizes the trees have `c_g ≥ 0.11` (m ≤ 63), while the paths with n ≥ 16
   have `c_g ≤ 0.06`. Also, `c_g` falls with size inside every family:
   about 0.08 → 0.02–0.05 (path, n = 8 → 64) and 0.28 → 0.11 (tree,
   b = 0.62, m = 7 → 63). This confounds three inferences: the
   "chain-length effect" at `b = 0.88`, the "slow growth with m" on trees,
   and "a too-large θ rather than an effect of branching" (Section 7.4).
3. **Several statements in Section 5 and Summary item 4 are heuristics
   presented next to a proved result.** Examples: the min-marginal
   surrogates "carry the global relaxation error that defeats LS", and
   "Lemma 1' imposes the same equal share on the leaves". They should be
   labelled as heuristics. Proposition 6 itself is correct; its scope is
   rule `bd` with the graded split `ψ` and the `w/(2n)` discount in the
   exact-bag model (Section 6).
4. **Missing literature that narrows the novelty claim.** The idea of
   refining a shrinking corridor around the current DP-optimal trajectory
   is old: DDDP (Heidari, Chow, Kokotović and Meredith 1971), Luus's
   iterative dynamic programming, and Munos–Moore variable-resolution DP.
   None of them gives certified lower bounds or a complexity bound. The
   closest locality result, Shin–Anitescu–Zavala (SIAM J. Optim. 2022,
   exponential decay of sensitivity in graph-structured NLPs), is already
   in the continuation's own audit (`literature/decomposition-bb-prior.md`)
   but is not cited. I found no prior result that already gives Theorem 2
   (Section 8).
5. **Scope of the answer.** The answer to [E]'s open problem is positive
   only under the extra hypothesis (S), `∇F(x*) = 0`, and only for paths.
   Theorem 3.4 of [D] needs neither. The proved base is also quadratic in
   `M_a/c_g`, against linear in [D]. The note discloses both, but the
   Summary and "Significance" sections ("closes the gap") should repeat
   (S) and the larger exponent. Exploratory runs (Section 7.5) suggest
   that (S) may be an artifact of the proof: GR localizes at a face
   minimizer with nonzero gradient. This is not a proof.

Smaller points are listed in Section 9.

| Claim (as submitted) | Review status |
|---|---|
| Lemma 1 (paths, (QG), (L^{1,1}), (U^q), (S)) | **Confirmed** (checked by hand). It also holds when touching pairs are omitted, and it does not use dyadic boxes. |
| Theorem 2 (GR on paths) | **Confirmed** (checked by hand). Constants are as stated but numerically vacuous: on the path family θ* ≈ 8e-8 and the base ≈ 9e9 (Section 3.3). |
| Corollary 3 (dovetailing) | **Confirmed**, with two clarifications (Section 3.4). |
| Remark 3.3 (trees, conditional) | **Needs correction** (item 1). |
| Corollary 4 (Conjecture A.7 on paths) | **Confirmed** under (S), (M) and LS's slope rule. Change "explains" to "is consistent with". |
| Proposition 6 (lower bound for `bd`) | **Confirmed** (checked by hand; `bd` counts reproduced exactly, float). The surrounding heuristics need labels. |
| Sketch for trees with `L` leaves | A sketch, correctly labelled. Not checked beyond the boundary-edge count, which is right. |
| Computations | **Reproduced** where I re-ran them (exact match). Interpretations in 8.3–8.4 need revision (item 2). |
| Reading (R1) without (QG): open | Agreed. |

## 2. Lemma 1 (sup-norm localization on paths)

Checked by hand, step by step. Each check below names the step and the
fact that makes it work.

- *(1.1) and (E1)–(E4).* (1.1) follows from Lemma 1.5 and Lemma 3.2 of [D].
  `σ_t` comes out with the right sign, and `err_t ∈ [0, (α'A/4) w(B)^2]`
  by (U^q). (E1) holds because `D_t` and `(B_{t−1})_{S_t}` intersect.
  (E2) is a telescoping sum over at most `k − 1` edges inside
  `[t − k + 1, t]`. In (E3), on a path `V_t \ S_t` has `l_i = t`, so the
  two points differ only on `S_t`. The Taylor split gives
  `M_a (w+1)(ρ_t Δ_t + 1.5 Δ_t^2)`. (E4) is direct.
- *Step 1 (window).* (U1) holds by construction: `[a − k, a + k − 1]` is
  `[a0 − 2k, a0 − 1]`. (U2): a gap between consecutive heavy bags has at
  most `2k − 1` light bags, and the two buffers have `k` each, so there are
  at most `2k|H_U|` light bags. (U3): `J_L ∩ J_R = ∅` because `|U| ≥ 2k + 1`
  when both ends are interior. The variables of heavy bags lie in `I`
  because `T_i ⊂ [s − k + 1, s + k − 1] ⊂ [a + 1, b − 1]`.
- *Step 2 (repair).* The assignment depends only on the variable, so
  copies agree on every edge in `(a, b]`. Edge `a` keeps `D_a` (it contains
  `z^a_{S_a}`) and the unchanged `B_{a−1}`. Edge `b + 1` keeps `D_{b+1}`,
  which contains `z^{b+1}_{S_{b+1}} = z'^b_{S_{b+1}}`. The consistent point
  is right: for `i ∈ J_R`, `l_i ∈ [b − k + 2, b] ⊂ U`, so `x'_i = z^{b+1}_i`.
  For `i ∈ J_L`, `l_i < a`, so `x'_i = x_i`.
- *Step 3 (gain).* Bags that contain `I` contain only `I ∪ J`, so `x_O`
  may be replaced by `x*_O`. (QG) and the (S)-bound
  `F(x* + δ) − f* ≤ (k M_a/2)|δ|^2` give the first inequality.
  `|F(x̂) − F(x')|` is bounded bag by bag over the `2k − 2` bags that
  contain `J_R`. In those bags both points stay within `η ρ` of `x*`; the
  `J_L` bags do not overlap them because `b − a ≥ 2k`. For a heavy bag,
  `Δ_s ≤ η ρ/2` by `K ≥ 32k^2/η` and `θ ≤ η/(8k)`, so
  `|x_i − x*_i| ≥ ρ_s/2`. Each variable serves at most `k` bags.
- *Step 4 (costs).* `T_t(c')` vanishes in `U` except on `[a, a + k − 2]`.
  The bags `[b + 1, b + k − 1]` change only through `x'_{J_R}`. `C2` has the
  four terms listed, and `δ ≤ η/(8k)` gives
  `C2 ≤ M_a(w+1)(k+1)η^2 ρ^2 = (c_g/(16k)) ρ^2`. In `C1`, Young's
  inequality and `θ ≤ 1/(12(k−1))` (implied by `θ ≤ 1/(32k^2)`) give the
  displayed bound. The bound `S_U ≤ 3k^2 Σ_H` counts lights as
  `(2k|H_U| + k − 1) η^2 ρ^2 ≤ (3k − 1) Σ_H`. The Young constant in `C3` is
  right, and `Σ_{[a, b+1]} ρ_u^2 ≤ (2k + 2) Σ_H`.
- *Step 5.* The coefficients sum to `1/48 + 3/72 = 1/16` (times `c_g/k`).
  The `|U| W^2` terms are absorbed by `K^2 ≥ 16k(2k+1)Q/η^2`. The net gain
  is `≥ (c_g/(16k)) Σ_H > 0`.

**Hidden dependences checked.**

- *Touching pairs.* Configurations of Lemma 1.5 include leaf–cell pairs
  that only touch. GR's code includes them: closed tests on dyadic edges
  that are exact in binary. The lemma also survives a DP that omits
  touching pairs (allowed by the remark after Lemma 1.3 of [D]). Choose the
  repaired boxes as the boxes that contain `z'^s + ε v` for a generic small
  `v`. On the coordinates `J_L` and `J_R`, which are disjoint, `v` points
  into `int D_a` and `int D_{b+1}`. The copies stay `z'^s`, and every pair
  of `c'` then has interiors that meet. (Reviewer's argument, short and
  elementary.)
- *Dyadic boxes.* Lemma 1 does not use them, as the note says.
- *Exact bag minima.* The lemma assumes an exact minimizing configuration,
  as [D] and [E] do. Reviewer's sketch: if each (leaf, cell) program is
  solved to absolute accuracy `τ`, then `c` and `c'` differ only on `U` and
  at the two boundary edges. So the computed configuration is within
  `2(|U| + 2)τ` of beating `c'`. Since `|U| ≤ (2k+1)|H_U|`, this slack is
  absorbed like the `|U| W^2` terms if `τ ≤ const · W^2`. Localization is
  therefore robust to subproblem errors of order `W_j^2`; this was not
  written out.
- *A computed illustration that the θ-condition matters.* In
  `logs/gr_theta_n32.log` (θ = 1/4), at stage 7 the graded invariant holds
  with respect to the true `x*` (`gviol = 0`) and yet `zloc = 64`. The
  hypothesis (W_θ) holds there, but θ is above the lemma's threshold. I
  reproduced this with independent code (Section 7.1).

## 3. Theorem 2 and Corollary 3

### 3.1 Validity of output certificates

In exact arithmetic every certificate GR outputs is valid, whatever the
hypotheses. Lemma 1.3 of [D] holds for any partitions and slopes with
maximal `β`, and `UBD` is a value of `F`. So the stop test gives
`f* − ε ≤ UBD − ε ≤ l_r ≤ f*` and `UBD ≤ f* + ε`. Neither (M) nor (S) is
needed for validity.

In the floating-point code, `solve` returns the objective at an approximate
minimizer, which is an upper estimate of each subproblem minimum. The
computed `l_r` is therefore not a rigorous bound. The note says this
("illustrations, not certified values"). In my independent runs:

- the relaxed value of the reconstructed configuration equals `l_r` to
  within `4.3e-14` in absolute terms (`|l_r|` reaches 79 at early stages);
- the configuration constraints hold;
- `l_r ≤ f*` at every stage.

### 3.2 The proof

Checked by hand.

- *(a) Slopes.* On a path the bags of `sub(t)` that contain a variable of
  `S_t` are `[t, t + k − 2]`, which is `k − 1` bags. So
  `ν_t ≤ (k−1) M_a sqrt(w+1)|x^{(j−1)} − x*|_∞ ≤ γ(K*) M_a W_j`.
- *(a) Localization.* `16k(2k+1) Q(γ(K*), θ)` splits as stated. The last
  term equals `c_θ θ^2 κ^2 K*^2` exactly, and the three parts sum to at
  most `η^2 K*^2`. So `K_1 ≤ K*`.
- *(a) Grading.* The step needs `R ≥ K*`. Cells use the child copy
  `z^t_{S_t}`, consistent with G for cells.
- *(b), (c).* The bounds follow from (E1)–(E4), `F(x) ≥ f*`, the (S)-bound
  for `UBD`, and `n ≤ (w+1)N`.
- *(d).* "No box wider than `W_j` is split" needs `R ≥ 3K*` and
  `|z_j − z_{j−1}| ≤ 3K* W_j`. All boxes at stage `j` have width at least
  `W_j`, so split boxes have width exactly `W_j`. The per-coordinate count
  `2(R + 1/θ) + 2` is right. The bound "processed `≤ (j* + 1)` times final
  size" is right.

The output is a Definition 1.2 certificate (one slope per separator,
Section 3 child bounds, maximal `β`). Its size counts leaves plus cells,
as in [D].

### 3.3 Size of the constants (float, `adaptive-matching-review-checks/constants.py`)

On the path family of Theorem 4.1 of [D] the constants are:

| Quantity | Value |
|---|---|
| `κ = M_a/c_g` | 28 |
| `a` | 8 |
| `θ_1` | 1.7e-6 |
| `θ_2` | 8.2e-8 |
| `θ*` | ≈ 2^-23.5 |
| `K*` | 7.3e8 |
| `R = 3K*` | 2.2e9 |
| base `4R + 4/θ + 4` | 8.8e9 |
| `K_1(0, 0)` (Corollary 4) | 1.8e6 |

The runs use θ = 1/8 and R = 4 (base 52) and observe localization 3. The
theorem is an asymptotic statement about the form `|T| C^{w+1} log`; it
says nothing quantitative at these sizes. The note says the constants are
"far from" practice; I recommend giving these numbers.

The orders are as stated, with one exception: my count gives
`1/θ* = O(k^4 w^{1.5} κ^{1.5} + k^{1.5} sqrt(a))`, not `k^{4.5}`. The note's
O-bound is still a valid upper bound.

Unlike [D], the base is quadratic in `κ`: `K* = Θ(k^5 w^2 κ^2)`, coming from
the slope-lag feedback through `γ(K*)`. [D] has `1/θ = O(k sqrt(...) κ)`.
"The form of Theorem 3.4 with a larger polynomial" is accurate, but the
exponent of the condition number doubles; the Summary should say so.

### 3.4 Corollary 3

Correct, with two clarifications.

- *Budget.* The box budget `2^r` must be enforced during a refinement,
  aborting at the first split past the budget. A run with wrong `μ` can
  split wide boxes repeatedly within one stage, so a check after the
  refinement could overshoot by more than the budget. The proof implicitly
  assumes the abort.
- *Stage cap.* The inequality `j* ≤ λ_ε + ceil((1/2) log2(C_term N)) + 1`
  in fact holds without the `+1`. That leaves room for counting stages
  0..j*, so the cap works under either reading of "at most
  `r + λ_ε` stages".

Note also that `C_term` depends on θ only through `(1 + θK*)`, so its
value at `μ*` is bounded by its value at θ*. The final O-expression is
right.

## 4. Remark 3.3 (trees): needs correction

The remark says that (E1)–(E4), the slope bound, the grading, the
termination and the count hold for every rooted tree decomposition, so
that Theorem 2 holds for trees "whenever the conclusion of Lemma 1 holds
(with some `K_1(γ, θ)` independent of `|T|`)".

1. **The slope bound.** The remark says "at most `k − 1` bags of `sub(t)`
   contain a variable of `S_t`". This is false on trees with `k ≥ 3` and
   `w ≥ 2`. Example: `V_p = {1, 2}`, `V_t = {1, 2, 3}`, with children
   `u1 = {1, 3, 5}` and `u2 = {2, 3, 6}`. Then `k = 3`, but the bags `t`,
   `u1`, `u2` of `sub(t)` all contain a variable of `S_t = {1, 2}`. A
   correct bound is coordinatewise: `|λ_{t,i}(x) − λ_{t,i}(x*)| ≤ (k−1) M_a sqrt(w+1)|x − x*|_∞`,
   hence `ν_t ≤ (k−1) M_a sqrt(w(w+1))|x − x*|_∞`. Only the constant in
   `γ(K)` changes.
2. **The fixed point.** Theorem 2(a) is an induction that needs a `K*` with
   `K_1(γ(K*), θ) ≤ K*`, where `γ(K) = c·K` (`c = 2k sqrt(w+1)` on paths).
   For Lemma 1, `K_1(γ, θ)^2` is affine in `γ` plus a `θ^2 γ^2` term, which
   `θ ≤ θ_2` absorbs, so a fixed point exists. A tree version of the
   localization conclusion with, say, `K_1(γ, θ) ≥ γ/c` for all θ would
   satisfy the remark's hypothesis, yet the induction would fail. So
   Remark 3.3 and Conjecture 7 need a growth condition in `γ`. Examples:
   `K_1(γ, θ) ≤ A_0 + A_1 sqrt(γ) + A_2 θ γ`, or simply "there is `K` with
   `K_1(c K, θ) ≤ K` for all `θ ≤ θ_0`". Alternatively, state
   Conjecture 7 for slopes within `γ M_a W` with an explicit
   sublinear dependence.
3. "The open problem for trees is therefore exactly the sup-norm
   localization" should read "the remaining step of this approach is ...".
   Localization is sufficient for this route, given item 2, but not shown
   necessary for the open problem.

The other items of the remark do hold on trees, with `ρ̂_t` taken over
ancestors within `k − 1` generations. They are (E1), (E2), (E3) (on trees
`V_t \ S_t` has `top(i) = t`), (E4), the grading and the count.

## 5. Corollary 4 (Conjecture A.7 on paths)

Correct. At a failed sublevel of LS, Lemma A.2 of [E] (which needs (M))
puts every box of the minimizing configuration at level `i`. So (W_θ) holds
with `θ = 0` and `W = s_i`. The slope induction over passes is right, and
`K_1(γ, 0)^2` is affine in `γ`, so `K_LS` exists.

As Corollary 4 notes, the conjecture as stated in [E] has no slope
hypothesis; the result proves it with LS's slope rule plus (S). In fact
Lemma 1 with `θ = 0` gives it for any certificate whose live boxes have
side at most `s` and whose slope errors are at most `γ M_a s`.

"It explains the computations of [E]" (line 646) is too strong. The proof
constant `K_1(0, 0) ≈ 1.8e6` on that family does not explain the observed
ratios 4–6. "Is consistent with" is accurate.

## 6. Proposition 6 (rule `bd` under quadratic growth)

**Checked by hand.**

- The Riccati coefficients are right. I confirmed them against a direct
  Schur-complement computation (difference `≤ 2e-16`).
- `p_t < 0` and `|p_t| ≥ θ_t q_t ≥ q_t/2` for `t ≤ (n+1)/2`.
- The bracket bound `g(D) ≥ |p| r^2 − (q/(2n))(2d^2 + r^2)` follows from
  "sup ≥ average of the endpoint values" for the convex part and "sup ≥
  midpoint value" for the concave part; the affine parts cancel.
- The final-cell inequality, `K_t ≥ (n−1)/2`, the per-range count
  `sqrt(K_t − 2)/6`, the "at most two ranges per cell" argument (needs
  `K_t > 11`), and the total are right.

**Float-checked, independent code** (`my_bd_check.py`, log
`my_bd_check.log`):

- Bracket by Brent search over the slope; Riccati values replaced by linear
  algebra.
- Total `bd` cells for n = 4, 8, ..., 256 are 65, 191, 595, 1,697, 4,825,
  13,655 and 39,017, identical to `logs/check_bd_qg.log`.
- The bracket inequality of the proof holds on every cell tested (minimum
  margin 0 to 6e-17).
- On edges `t ≤ (n+1)/2` the cell counts exceed the proposition's bound
  (stated with `sqrt((n − 5)/2)`) by factors 21.8, 20.6, 17.7 and 18.1 for
  n = 32..256. The note's factor 13 refers to the variant with
  `sqrt(K_t − 2)`; both are consistent.

I did not recompute the graded comparison split (72–96 cells per edge, gap
`≤ 0.13 ε`). I read its code: the chords of the concave reduced value
functions make every non-root bag minimum 0, and the root minimum is a
convex quadratic per cell. The construction is right by inspection.

**Scope.** The lower bound is for rule `bd` exactly as defined in [Cov]:
the graded split `ψ`, the `w/(2n)` discount, exact value functions, and
counting separator cells only. Since it uses exact value functions, it is
a lower bound for an idealized rule, which is the right direction for
ruling that rule out. It does not cover other splits, as the "open
variant" paragraph says.

Several sentences around it are heuristic arguments, not proofs, and
should be labelled:

- Summary item 4, lines 115–119: "Lemma 1' of [Cov] imposes the same equal
  share on the leaves", and the min-marginal surrogates "carry the global
  relaxation error that defeats LS".
- Section 5 item 1.
- The "Bag errors" paragraph.

The heading "The bracket route does not match" should read "Rule `bd`
does not match".

## 7. Computations

### 7.1 Path family: independent re-implementation (exact reproduction)

`my_gr_path.py` shares no code with the authors' scripts:

- convex subproblems by golden-section search on `z1`, with `z2` in closed
  form or by projected Newton for the last bag;
- brute-force closed-interval leaf–cell pairing;
- its own DP and configuration reconstruction;
- an exact re-evaluation of `Φ(c)`.

| Run | Final size | Stop stage | Processed | Wide splits | Max split per bag per stage | zloc |
|---|---|---|---|---|---|---|
| n = 4, ε = 1e-4, θ = 1/8, R = 4 | 36,337 | 11 | 138,768 | 315 | 639 | 3.000 |
| n = 8 | 95,938 | 12 | 414,820 | 630 | 639 | 3.000 |
| n = 16 | 204,010 | 12 | 883,120 | 1,134 | 639 | 3.000 |
| n = 32, θ = 1/4, capped at 12 stages | not done (348,466 leaves at stage 12) | – | 1,291,762 | 59,837 | 795 | up to 704 |

All of these, and the per-stage `l_r` and `UBD`, are identical to the
authors' logs (`gr_zero_eps1e-4_theta8.log`, `gr_theta_n32.log`). For
θ = 1/4 the jump at stage 7 (`zloc = 64`) and the gap of 0.434 at stage 12
are reproduced. In every stage of every run:

- the configuration constraints hold;
- `|Φ(c) − l_r| ≤ 4.3e-14` (`|l_r|` reaches 79 at stage 0);
- `l_r ≤ f*`.

### 7.2 Logged figures

Every figure I compared in the note's tables matches the logs:

- Sections 8.1, 8.2 and 8.4: all table entries, the SUMMARY sizes, and
  `created`/`processed`;
- Section 8.3: the per-stage zloc sequences, including the hand-stopped
  runs;
- the LS and shell figures, against `../adaptive/logs/*.log` and
  Section 5.4 of [D];
- `processed` (GR) and `total_boxes` (LS) measure the same thing: the sum
  of partition sizes over all DP runs.

Small inaccuracies:

- "3.2–5.7 `W_j`" (line 935): the late-stage minimum in
  `gr_random_eps1e-4.log` is 3.12 (n = 8, seed 0), so 3.1–5.7.
- The "stages" column and "11 to 14" are the index of the stopping stage;
  the number of DP runs is one more. Say "stops at stage j".
- The quoted "3.00 at the last sublevels of LS at n = 64" is right, but the
  same log has 6.00 at sublevels 5–10 and 8.00 at sublevel 4. Quote the
  range.

### 7.3 Tree code

I read `tree_gr.py`. The bag tree, separators, factor assignment, slopes
(`λ_v = b x_v`) and the fixed `zloc` diagnostic (parent vertex `(v−1)//2`,
so 0 for bag 2) are all right.

`check_tree_dp.py` check (2) only verifies that the *unrelaxed* value of
the minimizing configuration is at least `l_r`. Since the relaxation errors
are nonnegative, this holds for any configuration whose relaxed value is at
least `l_r`, so it is a weak test. It does not verify that the
configuration's relaxed value equals `l_r`.
Line 1178 ("configuration value consistent") and lines 998–1003 overstate
it.

My `my_tree_dp.py` reuses only the authors' partition storage and
refinement. It has its own bag solver, DP, reconstruction, exact `Φ(c)`
re-evaluation, and `x*` by 40-start L-BFGS-B. Results, against the logs
(`tree_zero_eps1e-4.log`, `tree_random_eps1e-4.log`):

- **c = 0, m = 7** (θ = 1/16, R = 4, b = 0.55): stages 0–9 are identical
  (leaves, cells, `l_r`, `UBD`, `zloc = 3` from stage 3). My 1500 s time
  limit stopped the run during the stopping stage 10.
- **c = 0, m = 15**, capped at stage 6: stages 0–6 are identical, with
  `zloc = 4` from stage 3. The consistent point is at `2 W_j`; only the
  copies are at `4 W_j`.
- **random c, m = 7** (R = 8): `x*` agrees with the authors' to `8.9e-10`
  (same `f*`). Stages 0–7 are identical (`zloc` 0.086, 0.831, 2.349, 3.303,
  3.395, 3.211, 2.579, 2.843). The run ended at stage 8 when I stopped the
  queued jobs, to limit computation.

In every computed stage, `|Φ(c) − l_r| ≤ 3.6e-15`, the configuration
constraints hold, and `l_r ≤ f*`. So the tree DP, the reconstruction of the
minimizing configuration and the `zloc` diagnostic are confirmed for the
early stages. The later stages and m ≥ 31 were not re-run.

### 7.4 Conditioning is not held fixed (float, `cg_sizes.py`, `cg_sizes.log`)

On `[−1, 1]`, `x^2 − 0.1x^4 ≥ 0.9x^2`, so `c_g ≥ 0.9 − |b| ρ(A)/2`, where
`ρ(A)` is the spectral radius of the graph's adjacency matrix. An upper
bound comes from the bottom eigenvector of `A`. At the tested sizes:

| Instance | `c_g` range |
|---|---|
| path b = 0.88, n = 8 | [0.073, 0.096] |
| path b = 0.88, n = 16 | [0.035, 0.059] |
| path b = 0.88, n = 32 | [0.024, 0.049] |
| path b = 0.88, n = 64 | [0.021, 0.046] |
| tree b = 0.62, m = 7 | [0.28, 0.30] |
| tree b = 0.62, m = 15 | [0.19, 0.22] |
| tree b = 0.62, m = 31 | [0.14, 0.18] |
| tree b = 0.62, m = 63 | [0.11, 0.16] |
| tree b = 0.55, m = 7 | [0.35, 0.37] |
| tree b = 0.55, m = 63 | [0.20, 0.24] |
| tree b = 0.55, m = 127 | [0.18, 0.23] |
| path b = 0.8, n = 8 | [0.148, 0.171] |
| path b = 0.8, n = 256 | [0.100, 0.125] |

Consequences:

- The `b = 0.62` trees that lose localization (m = 31, 63; `c_g ≥ 0.11`)
  are better conditioned than the `b = 0.88` paths (`c_g ≤ 0.06` for
  n ≥ 16). "A path with similar conditioning" (lines 99, 1046) and the
  conclusion "a too-large θ rather than an effect of branching" (lines
  101, 1050) are not supported by these runs.
- Within each family `c_g` falls with size, by a factor of about 1.5–4. Since `θ*` is
  a power of `c_g/M_a`, a threshold that falls with n at `b = 0.88` is what
  one expects even if the true threshold is n-independent at *fixed*
  `c_g`. These runs therefore do not test n-independence; the note's
  "the computations do not establish the threshold" is correct, but its
  explanation by "the chain-length effect of Remark 3.6 of [D]" is only
  one of two candidate causes.
- The slow growth of the tree ratio with random `c` (3.4 → 4.9 for
  m = 7 → 63) coincides with `c_g` falling by about 1.5–1.8×. It cannot be
  attributed to branching. The bounds above are for `c = 0`. With random
  `c`, `|x*|_∞ ≤ 0.24`, so the diagonal of the Hessian at `x*` is at least
  `2 − 1.2 · 0.24^2 ≈ 1.93`, and half its smallest eigenvalue is at least
  `0.965 − |b|ρ(A)/2`: 0.415 at m = 7 and 0.264 at m = 63. Local
  curvature follows the same trend (reviewer's estimate).

A family with size-independent conditioning would separate the effects,
for example by scaling `b` with `ρ(A)` so that `0.9 − |b|ρ(A)/2` is fixed.

### 7.5 Exploratory test of hypothesis (S)

These runs use the authors' `gr_lib.run_gr` for speed, so they are
exploratory and not an independent reproduction. Scripts:
`boundary_test.py`, `face_test.py`; logs: `boundary_test_C3.5.log`,
`face_test_C3.5_0.5.log`.

- **Vertex minimizer.** With `c_i = 3.5`, `x* = (−1, ..., −1)` and the
  gradient is in `[0.3, 1.1]`, so (S) fails. GR stops at stages 7 and 8
  (n = 8, 16) with `zloc ≤ 0.65`.
- **Face minimizer.** With `c_i = 3.5` (even `i`) and `0.5` (odd `i`), the
  even coordinates sit at −1 with gradient 2.37–2.85, and the odd ones are
  interior at 0.591. GR stops for n = 8, 16 and 32 at stages 11, 12 and 13,
  and `zloc ≤ 3.18` at every stage, the same for all n.

So on these instances GR behaves as in the interior case. This suggests,
but does not prove, that (S) is an artifact of the proof (the first-order
splicing term). The note's limitation is stated accurately; a remark that
the computations do not show the limitation would help.

## 8. Literature and novelty

Examined for this review:

- the continuation's audit `literature/decomposition-bb-prior.md` (local,
  read in the relevant sections). It covers Robertson–Cheng–Scott (JOGO 91,
  2025), MUSE-BB (Langiu et al., JOGO 92, 2025), Cao–Zavala (JOGO 75,
  2019), Kannan (thesis 2018), Li–Grossmann, Zhang–Sun (Math. Prog. 2022),
  and Shin–Anitescu–Zavala (2022). From that audit, Robertson–Cheng–Scott,
  MUSE-BB, Cao–Zavala and Kannan are two-stage (star) methods with
  convergence or convergence-order results and no node-count theorem of
  this kind. Zhang–Sun gives worst-case `T(1 + 2LDT/ε)^d` iterations, not
  an instance-dependent `log(1/ε)` bound;
- web searches (search-result snippets and abstracts only; no paper read
  in full):
  - Shin, Anitescu, Zavala, "Exponential decay of sensitivity in
    graph-structured nonlinear programs", SIAM J. Optim. 2022
    (arXiv:2101.06350; abstract via ANL and optimization-online pages).
    Under SSOSC and LICQ, the sensitivity of the solution at one node to a
    perturbation at another decays exponentially with graph distance.
    This is the closest published locality result to Lemma 1. It is local
    (near a regular solution) and about exact NLP solutions; Lemma 1 is a
    global exchange statement for minimizers of relaxed decomposition DPs.
    The note should cite it next to Rebeschini–Tatikonda.
  - Heidari, Chow, Kokotović, Meredith, "Discrete differential dynamic
    programming approach to water resources systems optimization", Water
    Resour. Res. 7(2):273–282, 1971 (abstract). It runs DP in a corridor
    around a trial trajectory and iterates with new corridors.
  - R. Luus, iterative dynamic programming (book, CRC 2000; IFAC
    proceedings abstract). It uses grids around the best trajectory of the
    previous pass, with the region reduced by a factor each pass.
  - Munos and Moore, "Variable resolution discretization in optimal
    control", Machine Learning 49(2):291–323, 2002 (abstract). It refines
    cells of a DP discretization by local and non-local criteria.
  - Searches for adaptive decomposition B&B complexity under quadratic
    growth, and for "spatial branch and bound" with "tree decomposition"
    and complexity, found nothing that gives Theorem 2.

**Assessment.** The *mechanism* of GR (one DP per stage, refining
geometrically shrinking neighbourhoods of the current DP-optimal
trajectory) has clear precursors in DDDP and IDP. Those are heuristics
without lower-bound certificates or complexity bounds. (That DDDP returns
local solutions in general is my background knowledge, not checked in a
source.) What I did not find elsewhere:

- a sup-norm localization lemma for minimizers of *relaxed* (Lagrangian,
  convex-relaxation) decomposition DPs under (QG);
- a certificate-producing algorithm with an instance-dependent
  `|T| C^{w+1} log(|T|/ε)` count;
- a lower bound like Proposition 6.

The note's novelty sentence should name the precursors and confine the
claim to the certified, complexity part. My searches were short and
snippet-level; they do not establish novelty.

## 9. Requested changes (priority order)

1. Remark 3.3, Conjecture 7, and Summary item 3:
   - fix the tree slope bound;
   - add the growth condition in `γ` (or the fixed-point condition);
   - soften "exactly" (Section 4).
2. Sections 8.3 and 8.4, and Summary item 3: replace the
   infinite-size `c_g` values by size-dependent ones (or bounds), withdraw
   "similar conditioning" and the branching-versus-θ conclusion, and say
   that `c_g` decreases with size in all tested families (Section 7.4).
3. Summary items 1 and 4, "Significance", and Section 3.2: state (S) next
   to "closes the gap"; say that the base is quadratic in `M_a/c_g`
   (against linear in [D]); give the numeric `θ*`, `K*` on the path family.
4. Label as heuristic: Summary item 4 lines 115–119, Section 5 item 1, and
   the "Bag errors" paragraph. Rename the heading to "Rule `bd` does not
   match".
5. Section 9: add Shin–Anitescu–Zavala (2022), DDDP (1971), Luus's IDP and
   Munos–Moore (2002), with access levels, and narrow the novelty
   sentence.
6. Corollary 3: say that the box budget is enforced during refinement.
7. Corollary 4: change "explains" to "is consistent with".
8. Section 8.4 and command table: describe `check_tree_dp.py` check (2) as
   it is, or strengthen it to re-evaluate the relaxed `Φ(c)`.
9. Minor:
   - "3.1–5.7" (line 935);
   - "stops at stage j" for the stage counts;
   - the LS sublevel ratios (3, 6 and 8, not only 3);
   - `1/θ*` order `k^4` (optional).

## 10. What I did not check

- The sketch for trees with `L` leaves, beyond the count of boundary
  edges, which is correct.
- The graded comparison split of Section 8.5 numerically (read only).
- `k ≥ 3` path decompositions; none were run by the author either.
- The `b = 0.62` tree runs and the `b = 0.88` path runs, which I compared
  with their logs but did not re-run.

## 11. Commands run (targeted checks only)

All from `research-20260929/reviews/adaptive-matching-review-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, Python 3.13,
NumPy 2.5.1, SciPy 1.18.0, on a shared machine with load around 35.

| Command | Log | Result |
|---|---|---|
| `python3 my_gr_path.py zero 4 1e-4 8 4` | `my_gr_n4_eps1e-4_theta8.log` | identical to the authors' log (Section 7.1) |
| `python3 my_gr_path.py zero 8 1e-4 8 4; python3 my_gr_path.py zero 16 1e-4 8 4` | `my_gr_n8_eps1e-4_theta8.log`, `my_gr_n16_eps1e-4_theta8.log` | identical |
| `python3 my_gr_path.py zero 32 1e-4 4 4 0.8 12` | `my_gr_n32_theta4_cap12.log` | θ = 1/4 failure reproduced exactly |
| `python3 my_bd_check.py 1e-6 4 8 16 32 64 128 256` | `my_bd_check.log` | `bd` counts identical; proof inequality holds on all cells |
| `python3 constants.py` | `constants.log` | θ* ≈ 8.2e-8, K* ≈ 7.3e8, base ≈ 8.8e9 |
| `python3 cg_sizes.py` | `cg_sizes.log` | Section 7.4 |
| `python3 boundary_test.py 3.5 8 4 1e-4 8 16` | `boundary_test_C3.5.log` | vertex minimizer: GR converges, zloc ≤ 0.65 |
| `python3 face_test.py 3.5 0.5 8 4 1e-4 8 16 32` | `face_test_C3.5_0.5.log` | face minimizer: GR converges, zloc ≤ 3.18 for all n |
| `python3 my_tree_dp.py zero 7 1e-4 16 4 0.55 40` (time limit 1500 s) | `my_tree_zero_m7.log` | stages 0–9 identical to the authors' log; stopped by the time limit in stage 10 |
| `python3 my_tree_dp.py random 7 1e-4 16 8 0.55 40` | `my_tree_random_m7.log` | stages 0–7 identical; stopped at stage 8 (queued job cancelled by PID, with a queued full `m = 15` run) |
| `python3 my_tree_dp.py zero 15 1e-4 16 4 0.55 6` | `my_tree_zero_m15_cap6.log` | stages 0–6 identical, `zloc = 4` |

Not kept: a first `my_gr_path.py` attempt with a nested golden search for
the last bag (too slow; killed by PID before it printed anything). A first
`face_test.py` run with `c_odd = 0` gave a degenerate minimizer (odd
coordinates at +1 with zero derivative) and a wrong gradient printout; its
log was deleted. GR converged there too (zloc ≤ 4). My imports created
`theory-decomposition/adaptive2/__pycache__/`, which I removed.
