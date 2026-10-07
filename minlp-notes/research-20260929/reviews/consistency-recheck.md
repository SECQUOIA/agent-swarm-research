# Recheck: second-round revision of the consistency-relaxations note

Date: 2026-09-30. Note rechecked:
[`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
("the note"), mainly Section 12 ("Revision after review") and the passages it
changed. Review it answers:
[`consistency-review.md`](consistency-review.md) ("the review"). Recheck
scripts and logs: [`consistency-recheck-checks/`](consistency-recheck-checks/).

I did not write or previously review the note. I recomputed every number
named in the task with my own code. I did not reuse the author's LP or the
review's grid Remez, except where stated (the tree check reruns the
author's script in a scratch copy).

## Verdict

**Fixes needed, all small; no proof is wrong.** The revision makes every
correction the review asked for, and every number I recomputed is right.
But the revision also adds one claim that is false by the note's own data,
leaves one flawed step in the new hp argument, and wipes one of its own
evidence logs. Details:

- **Correct as revised.** The quadratic-example limit (about 0.279), the
  factors 7.9 and 11.8 with their finite-`R` ratios, and the hp value
  `1.6468e-10` all check out. So do the `a + b >= 0` step of Theorem 2.1,
  the de Farias–Van Roy identification, the Korda–Magron–Ríos-Zertuche
  Lemma 11 citation, the Corollary 5.5 tiling and its `16^{k/2}` factor,
  the conjecture labels, the solver-rule warnings, the E4 band-element
  interval, and the tree tables of Section 7.4.
- **Silent strengthening (must fix).** The revision says the lower end of
  Theorem 3.1 "is attained exactly *only* in trivial cases, such as one
  edge". The review said only that it *is* attained in trivial cases. The
  stronger claim is false by the note's own random tree instances (T3).
  There the lower end is attained in 515 of 900 cases, and in 93 of them
  both per-edge distances are positive.
- **Flawed step (should fix).** The new elementary argument for unaligned
  hp says that after bisection, the non-kink cells are at "a fixed relative
  distance from the kink". For dyadic bisection this is false: for the
  note's own kink `c0 = 1/sqrt 7` the relative distance falls to 0.047 at
  level 4. The status labels of this argument also disagree across
  sections.
- **Lost evidence (must fix).** `check_revision.py` imports `check_tree.py`,
  which opens `logs/check_tree.log` in write mode at import time. Running
  the revision script therefore emptied the tree log. The file is now 0
  bytes, so Section 7.4 and the Summary's "247 of 900" have no log.
  Rerunning the script in a scratch copy reproduces every number, so only
  the file needs restoring.
- **Inaccurate literature description (should fix).** The revised
  description of Alfonsi et al. is still inaccurate in one respect. Their
  `O(1/N^2)` rates are proved only for the costs `|x - y|` and
  `|x - y|^2`, under regularity conditions on the marginals. The Taylor
  argument for `C^{1,1}` costs is a heuristic, which they call "a rough
  calculation". The review's own description had the same imprecision.
- **Minor.** Several wording and presentation points (list below).

## 1. Items the task asked me to verify

### 1.1 Quadratic example: `n^2 gap`, limit about 0.279

`gap = 2 E_n((y_+)^2) = E_n(y|y|)`, because `(y_+)^2 = (y^2 + y|y|)/2`
and `y^2` is in `P_n` for `n >= 2`.

**Method.** `q1_remez_rates.py` runs a Remez exchange in the odd Chebyshev
basis on `(0, 1]`. Unlike a grid Remez, it refines every extremum by
bounded scalar optimization. The two columns below are the levelled error
on an alternating reference (a de la Vallée Poussin lower bound, up to
rounding) and the largest error found (an upper estimate).

| `n` | `E_n(y|y|)` lower | upper | `n^2 gap` | difference |
|---|---|---|---|---|
| 64 | 7.0317641645e-05 | 7.0317641646e-05 | 0.288021 | |
| 128 | 1.7308216189e-05 | 1.7308216189e-05 | 0.283578 | 0.004443 |
| 256 | 4.2934606360e-06 | 4.2934606370e-06 | 0.281376 | 0.002202 |
| 512 | 1.0691853682e-06 | 1.0691853690e-06 | 0.280281 | 0.001096 |
| 1024 | 2.6677508769e-07 | 2.6677508880e-07 | 0.279734 | 0.000547 |

- The note's values 0.28802, 0.28358 and 0.28138 (Sections 5.4, 7.1 and
  12) agree with mine to all printed digits. So do the review's R3 values
  for `n = 64..512`.
- Successive differences shrink by factors 0.4955, 0.4977 and 0.4988, so
  the correction is of order `1/n`.
- Extrapolated limit:
  - 0.27919 (Aitken) and 0.27919 (fit `K + a/n + b/n^2`), both on the
    last three values `n = 256, 512, 1024`;
  - 0.27921 (Aitken) from the note's three values `n = 64, 128, 256`
    alone.
- "About 0.279" and "about `0.070/R^2`" (`0.2792/4 = 0.0698`) are right.
- The label "extrapolated" is accurate: the limit is not proved.

### 1.2 Improvement factors 7.9 and 11.8

I checked the explicit bounds of [S] in the September 28 notes:

- `quadratic-sharpness.md`, (10): `-rho_r >= 2/(27 pi (2r+2)^2)`;
- `affine-recourse-rate-boundary.md`, (8)–(9): `-rho_r >= 2 E_{2r} >= 1/(9 pi (r+1))`.

**Asymptotic ratios.**

- Affine recourse: `2 E_{2R}(|y|) ~ beta/R`, so the ratio tends to
  `9 pi beta = 7.922`, using the Varga–Carpenter value
  `beta = 0.2801694990`. The limit is Bernstein's theorem; only the
  finite-`R` ratios are numerical.
- Quadratic example: `(K/4)/(1/(54 pi)) = 13.5 pi K`, which is 11.84 for
  `K = 0.2792`.

**Finite-`R` ratios** from my Remez values:

| `R` | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|
| affine recourse | 11.472 | 9.808 | 8.890 | 8.412 | 8.168 |
| quadratic | 42.193 | 23.536 | 16.948 | 14.223 | 12.991 |

The note's rounded values (11.5, 9.8, 8.9, 8.4, 8.2 and 42, 23.5, 16.9,
14.2, 13.0) match.

**Attribution.** The attribution to [S] Propositions 1 and 2 is right.
[S] proves the identities `v_n = -2 E_n(h)` and `eta_n = -2 E_n`, and the
inequality `-rho_r >= 2 E_{2r}` follows from them.

- Wording: the Summary says "both identities `-rho_R >= 2 E_{2R}`". The
  displayed relation is an inequality derived from the identities. This
  is harmless.
- The labels "asymptotic and numerical, not certified" appear in the
  Summary, Section 5.4, the status table and Section 10.

### 1.3 hp value at `p = 12`

`q2_hp_aligned.py` runs a 40-digit mpmath Remez with golden-section
extremum refinement on the cells `[-1, c0]` and `[c0, 1]`.

| `p` | `N` | per-cell `E_p` | gap = `2 max_D E_p` |
|---|---|---|---|
| 4 | 10 | 3.087175e-3, 5.1755455e-5 | 6.17435e-3 |
| 8 | 18 | 1.2122666e-6, 8.1219415e-10 | 2.4245331e-6 |
| 12 | 26 | 8.2341948e-11, 2.247994e-15 | **1.646839e-10** |

- The lower and upper values agree to the printed digits, so `1.6468e-10`
  is confirmed.
- The note's `1.65e-10` (Summary, Section 7.5, Section 12) is right.
- `check_revision.py` gives the same value as a grid-LP lower estimate. Its
  own upper bound, from the Chebyshev interpolant, is looser (`1.94e-10`).
  The note correctly says the value "agrees with the review's Remez
  bracket" rather than claiming the LP certifies it.

### 1.4 Gui–Babuška replaced by an elementary argument and DeVore–Scherer

**What is fine.**

- Gui–Babuška is now cited only for singularities at mesh nodes in the
  energy norm (Sections 5.5 and 8). That matches their 1986 papers, whose
  model singularity `x^alpha` sits at a node.
- The self-contradictory sentence is gone. The new text says that grading
  needs the approximate kink location.
- DeVore–Scherer, "Variable knot, variable degree spline approximation to
  `x^beta`", *Quantitative Approximation* (Bonn 1979), Academic Press
  1980, exists; I confirmed it at the bibliographic level. I did not
  check its contents, including which norm it uses. The note correctly
  labels the citation "bibliographic level".

**Problem (should fix).** The elementary argument in Section 5.5 says:

> after `m` bisections ... the other cells are analytic at a fixed relative
> distance from the kink, so they need degree `O(m)`.

- For dyadic bisection this is false in general. The distance from the
  kink to the sibling cell discarded at level `j`, divided by that cell's
  half-width, depends on the binary digits of the kink location, and it
  can be arbitrarily small.
- For the note's kink `c0 = 1/sqrt 7` I computed this ratio for
  `j = 1..15` (`q4_bisection_distances.py`): it is 0.047 at level 4 (cell `[0.25, 0.375]`) and 0.071 at
  level 11. Those cells have Bernstein-ellipse parameters `rho` of about
  1.36 and 1.46, instead of 2.6–5.6 on the other levels.
- Section 7.2 of the note already mentions that the node 0.375 is next to
  the kink.
- The claim is true for a geometric mesh built around a known kink
  location (cells `[c0 + sigma^{j+1}, c0 + sigma^j]`), which is the
  review's `sigma^m` form. It is also true if the argument assumes that
  the relative distances stay bounded below.
- **Fix:** state the argument for a geometric mesh around an approximately
  known kink, or add that assumption. Keep the dyadic numbers as numerical
  evidence.

**Inconsistent status labels.** Three places describe this argument
differently:

- Section 5.5: "an elementary argument gives `exp(-b sqrt(N))`";
- status table: "elementary argument sketched";
- Section 10: "Unaligned rates are cited, not proved in this setting".

Use one label ("sketch") in all three. The Summary's "behaves like
`exp(-b sqrt(N))`" should say that this is numerical plus a sketch.

### 1.5 Korda–Magron–Ríos-Zertuche, Lemma 11

I read arXiv 2303.14824. Only v1 exists; its text is
`/tmp/recheck/kmr.txt`, not kept.

- **Lemma 11** is the splitting lemma. For `f = f_1 + ... + f_l >= eps` on
  `S(g)` it gives `f = h_1 + ... + h_l` with `h_j >= eta`, with degree
  bounds.
- **Proof, case `l = 2`.** It defines
  `g(x) = min_y f_2(x, y) - eps/2` on the separator. It shows
  `f_1 + g >= eps/2` and `f_2 - g >= eps/2`. Theorem 10 (a Jackson-type
  bound) then gives a polynomial `p_2` with
  `||g - p_2||_inf <= eps/2 - eta`, and the lemma sets
  `h_1 = f_1 + p_2` and `h_2 = f_2 - p_2`.
- The note's description (Sections 8 and 12) is accurate: a one-sided
  value function shifted into the widened band, Jackson approximation, the
  sufficiency direction only.

Two refinements:

- KMR state that Lemma 11 is "a version of [4, Lemma 3]", where [4] is
  Grimm–Netzer–Schweighofer, *Arch. Math.* 89 (2007). The qualitative
  positive-width sufficiency form is therefore older, and KMR's
  contribution is the quantitative version. Section 8 lists GNS
  separately, but the novelty list ("known in substance") credits the form
  only to KMR. Credit it as "GNS 2007, Lemma 3; quantitative version in
  KMR, Lemma 11". I took the GNS attribution from KMR's text and did not
  read GNS.
- The published version is Math. Program. 209 (2025), pp. 435–473
  (DOI 10.1007/s10107-024-02071-6), found by web search. I could not
  access it, so I did not check whether the lemma keeps the number 11
  there. The note cites the arXiv numbering, which is correct.

### 1.6 Path case and the de Farias–Van Roy approximate-LP bound

The identification is correct in substance.

- Take a path rooted at one end. The DP split `psi_e = U_e` is then the
  stage cost-to-go.
- The ALP constraints `J_t(s_{t-1}) <= F_t(s_{t-1}, y_t, s_t) + J_{t+1}(s_t)`
  over all bag points say exactly that every bag of the split has infimum
  at least 0.
- When the constants are in each `Phi_t`, the per-bag constants `m_t` of
  the split relaxation can be absorbed into the `J_t`. So the ALP optimum
  equals `rho(Phi)`.
- Shifting the best approximants by constants gives
  `gap <= 2 sum_e dist(U_e, Phi_e)`. This is the undiscounted,
  finite-horizon form of `2/(1 - alpha) min_r ||J* - Phi r||_inf`. With a
  point-mass state-relevance weight, the weighted 1-norm error of the ALP
  is the gap.

The note uses the hedged wording "known in substance", and it keeps as new
only the infimum over all exact splits, the `2 max_e` lower bound and the
counterexample. That is appropriate. The quoted OR 2003 bound, with the constant function
in the span, matches the standard statement. I did not reopen the OR paper;
the first review read the secondary source the note cites.

### 1.7 Corollary 5.5: tiling and the `16^{k/2}` factor

I checked it against [D, Lemma 3.1]. That lemma gives, for a box with sides
at most `s0`, at most `(J+1)(4/theta)^k` boxes with
`J = ceil(log2(s0/h))`. Each box is either a central cube of side `h` or
has width at most `theta dist_inf(B, p)`.

**Correct.**

- *Cube and ball.* The cube `Q(s*, rho_0/sqrt k)` has corners at Euclidean
  distance `rho_0`, so it lies in the ball where `U_e` has an
  `M`-Lipschitz gradient.
- *Central cubes.* `r^2 = k h^2/4 = eps/M`, so Proposition 5.4(c) gives
  `g_D <= eps`.
- *Shell cubes.* `M r^2 <= M k theta^2 d^2/4 <= c d^2 <= w_min`, because
  `theta^2 <= 4c/(Mk)`.
- *Outside `Q`.* `w >= c rho_0^2/k`. For a cube of diameter at most
  `c rho_0^2/(2kG)`,
  `sup_D L - inf_D U <= G diam - c rho_0^2/k < 0`.
- *Factor.* `theta > (1/2) sqrt(4c/(Mk))` gives `4/theta < 4 sqrt(Mk/c)`,
  so `(4/theta)^k <= (16 M k/c)^{k/2}`. The factor `16^{k/2} = 4^k` is
  right.
- *Levels.* `log2(s0/h) = (1/2) log2(1/eps) + O(1)`.

**Minor fixes.**

- **`s0` is not defined** in Corollary 5.5, and it is used for two
  different boxes. In `log2(s0/h)` it must be the side of `Q`, that is
  `2 rho_0/sqrt k`. In the outer term `O((G s0 k^{3/2}/(c rho_0^2))^k)` it
  must be the side of `X_e`.
- **Edge case of `theta`.** `theta` is a power of 1/2 with exponent at
  least 0, so `theta <= 1`. If `c > Mk`, then `theta = 1`, and
  `4/theta <= 4 sqrt(Mk/c)` fails. In the `k >= 2` case nothing links `c`
  to `M`, because `L`'s curvature is not bounded by `M`. Write
  `max(16 M k/c, 16)^{k/2}`, or assume `c <= Mk`. Also, "largest power of
  1/2 below" should read "at most".
- **Stale constant.** The comparison paragraph after the proof still says
  "The base is `(M k/c)^{k/2}` per separator". Change it to
  `(16 M k/c)^{k/2}`, or to "`(C M k/c)^{k/2}`" with `C = 16` here.

### 1.8 Theorem 2.1: the `a + b >= 0` step

Correct. For any `phi`:

- `a + b = sup(phi - U) + sup(L - phi) >= sup(L - U) = f* - inf(U + V) = 0`,
  using `f* = inf_s (U + V)(s)`, which follows from the definitions and
  the projection hypothesis.
- No pinch point is needed.
- Shifting by a constant keeps `a + b`, so both `a` and `b` can be made
  nonnegative.
- The clipped `psi` lies in `[L, U]`, because `w >= 0`.
- `phi - psi` takes values in `[-b, a]`.

The remark "`rho(Phi) = rho(Phi + R)`, so the constants hypothesis costs
nothing" is also correct: on a tree, a constant added to `phi_e` enters one
bag with each sign.

### 1.9 Conjecture labels

The limit `n gap -> 2 beta` for `c > 0` is called a conjecture, or
"plausible, but a conjecture", in all five places: the Summary (C),
Section 5.4 ("Conjecture ... The data do not show the limit"), Section 7.1,
the status table and Section 10. The heuristic is labelled as such.

**Caveat worth one clause.** The heuristic is weak. The band width `c s^2`
exceeds the error scale `1/n` once `|s| >~ 1/sqrt(c n)`, so outside a
shrinking neighbourhood of 0 the band is not negligible. The limit may
therefore be smaller than `2 beta`.

- The data are consistent with either outcome. For `c = 0.5`, `n gap`
  rises by about 0.025 per doubling, up to 0.486 at `n = 128`.
- At `n = 128` the fine-grid upper estimates are loose: 0.50, 0.48 and
  0.53 for `c = 0.5, 2, 8`. The values 0.49, 0.42 and 0.33 quoted in
  Section 5.4 are therefore lower estimates, and the text should say so.

### 1.10 Solver-rule warnings

Present and adequate:

- Summary (E) says "heuristic" and flags edge-by-edge use with the original
  bands as unsafe (Proposition 3.3).
- Section 6 has "Adaptive rule (heuristic)" with the paragraphs
  "Justified parts", "Heuristic" and "Unsafe on trees".
- The status table and Section 10 repeat the warning.

**One overstatement.** The Summary says decisions "must use the reduced
bands of Corollary 3.4 or the joint dual marginals".

- Only the reduced-band route is backed by a result. Corollary 3.4 gives
  `gap <= sum_e Delta_e`, so bounding each reduced bracket bounds the gap.
- The dual-marginal route is a suggestion that has not been tested.
- Computing a reduced band also needs the parent-side value function of
  the reduced problem, which is a global computation.
- Suggested wording: "should use the reduced bands of Corollary 3.4 (which
  bound the gap by Corollary 3.4 but need parent-side value functions) or,
  untested, the joint dual marginals".

### 1.11 Other numbers the revision relies on

**E4 band element.** Let `q = T - kappa (s - 0.3)^2`.

- `q >= L` iff `kappa <= 1.5`.
- For `s >= -0.5`, `U - T = -(s - 0.3)^2`, so `q <= U` iff `kappa >= 1`.
- For `s < -0.5`, `U - q = (kappa - 1)s^2 + (1.6 - 0.6 kappa)s + 0.41 + 0.09 kappa`.
  This is increasing on `[-1, -0.5]` for `kappa` near 1.3, so the binding
  point is `s = -1`, which gives `kappa >= 2.19/1.69 = 1.29586`.
- So the interval `[1.296, 1.5]` is correct.

**T1, T2, T3.** I reran `check_tree.py` in a scratch copy (see Section 2.2).

- T1 table, `n = 4` and `n = 8`: identical.
- T2: gap 1 against per-edge values 0.2 and 0.2.
- T3: "`Q > gap` in 249 cases (largest excess 1.7646); per-edge sum below
  the gap in 247 cases".

The Summary's 247 is the note's own experiment; the review's 280 comes from
a different experiment. The note's T1 values at `K = 100` from
`check_revision.log` (1.0008 and 1.0132 on 161 and 321 points) match the
log.

## 2. Problems found

### 2.1 Silent strengthening: "the lower end is attained exactly only in trivial cases" (must fix)

**Where.** The Summary (B), line 63–64, and the Remarks after
Proposition 3.3, line 525–526, say:

> It is attained exactly only in trivial cases such as one edge.

**Source.** The review (F6) wrote: "It is attained exactly in trivial
cases, such as one edge." That sentence claims attainment exists. The
revision turned it into an "only" claim, which the note does not prove.

**The note's own T3 data contradict it.** `q3_tree_lower_end.py` reruns
T3 with the same seed and the author's LPs. In 515 of 900 cases,
`gap = max_e 2 dist(Phi_e, Band_e)` to `1e-7`. In 93 of those, both
per-edge distances exceed `1e-4`, so the sum is strictly larger. Examples:

| trial | degree | gap | `2 dist_1` | `2 dist_2` |
|---|---|---|---|---|
| 1 | 1 | 1.0625980404 | 0.6405989891 | 1.0625980404 |
| 2 | 0 | 1.4297860847 | 0.3156535776 | 1.4297860847 |
| 5 | 1 | 0.6974898338 | 0.2054318915 | 0.6974898338 |

These are finite instances, but the note itself uses them to test
Theorem 3.1. In the continuum, the lower end is also attained whenever the
other edges carry classes rich enough to contain the relevant reduced band
elements. The proof of Theorem 3.1 attains it exactly with the full class.

**Fix.** Replace the sentence with: "In T1 the lower end is approached as
`K -> inf` and not attained at finite `K` (numerically). In other instances
it is attained: in 515 of the 900 T3 cases, 93 of them with both per-edge
distances positive." A one-line proof of the T1 limit can be added:

- take `phi_1 = phi_2 = p`, the best approximant;
- let `g = |s| + p`, with Lipschitz constant `Lip(g)`;
- then the middle bag is at least `inf_d (-Lip(g)|d| + K d^2) = -Lip(g)^2/(4K)`;
- so `gap <= 2 E_n + Lip(g)^2/(4K) -> 2 E_n`.

The note's "At finite `K` the gap stays above `2 E_n`" is numerical only;
the proof gives only `>=`.

**Related wording in the review.** The review said that "in the continuum"
the `K = 100` ratio is 1.0025. That is also a grid value: its `r2_tree.py`
uses a 201-point grid. The note's 321-point grid, which contains the
161-point grid, gives 1.0132. Grid gaps are lower estimates of the
continuum gap here, because `f* = 0` is attained on the grid. So the
continuum ratio is at least about 1.013. The note's "grid values are lower
estimates" is the correct reading.

### 2.2 The revision emptied `logs/check_tree.log` (must fix)

- `check_tree.py` executes `out = open("logs/check_tree.log", "w")` at
  module level.
- `check_revision.py` runs `import check_tree as CT`.
- Running `check_revision.py` at 04:10 therefore truncated the tree log.
  It is now 0 bytes; its timestamp matches `check_revision.log`.
- Section 11 still describes it as `logs/check_tree.log (run twice; second
  run added the per-edge count)`.

**Evidence.** I ran `check_tree.py` in a scratch copy
(`/tmp/recheck/tc/`, not in the repository). Every number in Section 7.4
and the Summary's 247 were reproduced. I copied that log to
[`consistency-recheck-checks/logs/check_tree_rerun_scratch.log`](consistency-recheck-checks/logs/check_tree_rerun_scratch.log)
as evidence. I did not modify the author's files.

**Fix.**

1. Move the `open(...)` into `if __name__ == "__main__":`, or open the file
   lazily in `log()`.
2. Rerun `python3 check_tree.py`, which takes a few minutes.
3. Say in Section 11 that the log was regenerated.

### 2.3 Unaligned hp argument (should fix)

See Section 1.4: the "fixed relative distance" step and the inconsistent
status labels.

### 2.4 Description of Alfonsi et al. (should fix)

I read Section 5 of arXiv 1905.05663.

**What the paper says.**

- Proposition 5.1 (piecewise constants, `K`-Lipschitz cost,
  `I^N <= I <= I^N + K/N`) is as the note says.
- Section 5.2 introduces the piecewise-affine test functions. It then
  gives "a rough calculation" of "why considering these test functions
  *may* lead to a convergence rate of `O(1/N^2)` when `c` is `C^1` with a
  Lipschitz gradient", and adds that "such kind of a result is not
  obvious".
- The `O(1/N^2)` rates they prove are Propositions 5.7 and 5.9 and
  Corollary 5.8/5.10:
  - for `W_1`, that is `c = |x - y|`, which is *not* smooth, under
    bounded densities and finitely many sign changes of `F_mu - F_nu`;
  - for `W_2^2`, under bounded densities.
- They are proved through cumulative distribution functions, not through
  a Taylor expansion of the cost.

**What the note says.** Section 8 says that "the `O(1/N^2)` rate ... comes
from a first-order Taylor expansion of a cost that is `C^1` with Lipschitz
gradient; so their rates come from the regularity of the cost". This
overstates the paper: the Taylor argument is their heuristic, and the
proved rates also depend on the regularity of the marginals. The review's
own wording had the same imprecision.

**What stands.** The correction that the review asked for stands: the
rates do not come from approximating Kantorovich potentials.

**Suggested wording.** "Proposition 5.1 gives `O(1/N)` for piecewise
constants and Lipschitz costs. For piecewise-affine test functions a Taylor
heuristic suggests `O(1/N^2)` for `C^{1,1}` costs; the proved `O(1/N^2)`
rates are for `W_1` and `W_2` under regularity conditions on the
marginals."

### 2.5 Minor points

1. **Summary (D), "Polynomials".** "On boxes they exist under an
   interior-pinch hypothesis (Ilmanen–Bernard insertion; Proposition 4.3 is
   a sketch)" states existence as a fact.
   - Proposition 4.3 is a sketch.
   - It also assumes `w_e >= delta_0 > 0` on `∂X_e` and Lipschitz `U`, `V`.
   - Suggested: "they would exist under an interior-pinch and open-boundary
     hypothesis if the sketch of Proposition 4.3 is completed".
2. **Proposition 1.3(2) for cellwise classes.** The text defers the
   lsc-envelope extension to "the review sketches why", and the status
   table lists it without a "sketch" label. Either copy the three-line
   argument into the note or label it a sketch. The argument: lsc hulls
   have the same affine minorants and infima, and Sion's theorem needs only
   lower semicontinuity in the measures.
3. **"Loose by factors of 30 to 70".** This comes from the review. In the
   review's own R3 data, for `2 <= n <= 32`, the ratio of the LP gap to
   `1/(30(3+c)n)` ranges from 18 (`c = 8`, `n = 2`) to 72 (`c = 8`,
   `n = 32`). At `n = 1` it is 105–330. Say "about 20 to 70 for
   `2 <= n <= 32`".
4. **Summary (D), piecewise-affine cells.** The shell count is stated
   without the `k >= 2` hypothesis of a `C^{1,1}` `U_e` near `s*`. The
   status table has it.
5. **Corollary 5.5.** The `s0`, `theta` and stale-constant points of
   Section 1.7.

## 3. Was anything else silently strengthened?

I compared each item of Section 12 with the review's request and with the
changed text.

**Only one change goes beyond the review:** the lower-end "only" claim of
Section 2.1.

**Everything else is as strong as the review allowed, or weaker:**

- "explains" is restricted to the lower bounds;
- Corollary 5.7 is called "derived from [S]" and claims a band element per
  `n`;
- `N` is called a proxy throughout;
- Lemma 4.2 is marked classical;
- the novelty list is shortened, and "an unsuccessful search does not
  establish novelty" is kept;
- the curvature-jump entry now correctly states that `O(n^-2)` is proved
  (the review's own observation).

**New sentences not requested by the review,** all plausible and hedged:

- "When the band has zero width ... hp is cheaper" (Proposition 5.9) and
  "On a zero-width band like this one, hp is also cheaper in cost"
  (Section 6). Both are asymptotic comparisons of `eps^{-1/2}` cells
  against polylogarithmic blocks. They are reasonable, but they are
  asymptotic statements, not measured costs.
- "Grid-LP values below about `1e-9` ... are lower estimates"
  (Section 7.5). This is correct and appropriately cautious.

## 4. Commands run (targeted checks only)

Run in `research-20260929/reviews/consistency-recheck-checks/` with
`OMP_NUM_THREADS=1`, unless stated otherwise:

```
python3 q1_remez_rates.py      # logs/q1_remez_rates.log; E_n(|x|) to n=256, E_n(x|x|) to n=1024, ratios; 651 s
python3 q2_hp_aligned.py       # logs/q2_hp_aligned.log; 40-digit Remez, p = 4, 8, 12; 16 s
# in a scratch copy /tmp/recheck/tc of theory-consistency/ (so the author's logs are untouched):
python3 check_tree.py          # -> consistency-recheck-checks/logs/check_tree_rerun_scratch.log
python3 .../q3_tree_lower_end.py   # logs/q3_tree_lower_end.log; attainment of the tree lower end in T3
python3 q4_bisection_distances.py  # logs/q4_bisection_distances.log; relative kink distances under dyadic bisection (Section 1.4)
```

**Sources read.**

- arXiv 2303.14824 (KMR), full text of v1, Lemma 11 and its proof;
- arXiv 1905.05663 (Alfonsi et al.), Section 5;
- the September 28 notes `quadratic-sharpness.md` and
  `affine-recourse-rate-boundary.md` (bounds (4), (9), (10) and (8));
- [D, Lemma 3.1] in `theory-decomposition/decomposition-certificates.md`;
- web searches for the published KMR reference and for DeVore–Scherer (the
  latter at the bibliographic level only).

**Not done:**

- no project-wide verification and no CI inspection;
- no edits to the note, its scripts or its logs;
- no commits.
