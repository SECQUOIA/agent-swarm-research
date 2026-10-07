# Review: `covering-upper-half.md` (graded exact splits and the upper half for one-dimensional separators)

Date: 2026-09-30. Note checked:
[`../theory-decomposition/covering-upper-half.md`](../theory-decomposition/covering-upper-half.md)
(draft, not reviewed before), with its scripts and logs in
[`../theory-decomposition/covering/`](../theory-decomposition/covering/). Definitions
were checked against [`decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
([D]: Definition 1.2, Lemmas 1.1, 1.3–1.5, Theorem 2.5, Conjecture 3.7),
[`extension-adaptive.md`](../theory-decomposition/extension-adaptive.md)
([E]: Sections B.1–B.6) and
[`consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
([K]: Section 0, Theorems 2.1, 3.1, Propositions 2.3, 3.3, 5.4, Corollary 3.4,
Lemmas 4.1, 4.2).

I did not write the note. I did not edit it or any root file, and I committed nothing.
My scripts and logs are in
[`covering-upper-half-review-checks/`](covering-upper-half-review-checks/). All runs were
single-threaded (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`). They are
targeted checks of this note only. I ran no project-wide verification and did not
consult CI.

## Verdict: fixes needed (minor)

**The mathematics holds.** I checked every proof step of Lemma 0, (F1)–(F2),
Theorem 1(a)–(c), Theorem 1', Lemma 2, Theorem 3 (validity and count) and
Proposition 4 against the definitions of [D], [E] and [K]. I found no gap. The
equality part of Proposition 5 is also correct. Its sufficient condition is correct,
but it relies on a leafwise version of Theorem 1' that the note asserts without
writing out (item 7 below).

**The numerics reproduce.** I reran four of the author's five scripts. Their
output is identical to the author's logs, apart from timing fields. The fifth
(`check_naive_failure.py`) I reproduced at `m = 257` with independent code. My own
code confirms the theorems on families the author did not test:

- bags with private variables;
- two-dimensional separators;
- bags with three children;
- R3 on two branching trees;
- the per-edge plateau on grids up to `m = 2049` (the note stops at 257).

**Settled claims.** Given this, the note's central claim stands, with the scope it
states: in the exact-bag model, the separator-cell upper half holds for trees with
one-dimensional separators. The certificate case in reading (R1) remains open, as
the note says.

**What needs fixing.** Several side claims are wrong or imprecise. None of them
changes a theorem.

1. **Lemma 2: "the constant 8 is loose by about 4" is wrong.** An explicit family
   reaches ratio 1/2. The constant can be lowered at most to 4, not to about 2
   (item R1).
2. **"Per-edge control of cell placement fails" (heading of Section 5, Summary item
   5) is contradicted by Theorem 3.** Rule R3 is itself a per-edge placement rule.
   What fails is placement driven by one-edge *band brackets* (item R2).
3. **Remark 1.2 understates the sharpness of Theorem 1.** Two alternating
   perturbations show that on the chain of copies, *every* exact split needs
   discount `c <= 1/(2n)`, not only `c <= 1/n`. So the factor `1/(2n)` of Theorem 1
   is optimal there. An LP confirms the value (item R3).
4. **Section 6, per-level admissibility sketch: one intermediate inequality is
   false** for `m(x) < eps/2`. The conclusion is still true (item R4).
5. **Proposition 4, "What it shows": two statements are too broad.** The reduced
   function is concave only on `|s1| <= 1 - beta/kappa`. For `kappa = 2 beta`, which
   the proposition allows, the reduced band has zero width near 0 (item R5).
6. **Section 7.4: "does not decrease when the tolerance is lowered" is too broad.**
   It holds in the ten failing settings (decrease at most about 4%), not in all 20
   (item R6).
7. **Proposition 5 needs a short lemma.** It applies Theorem 1' to a *leafwise*
   relaxation, where the split is two-valued at cell boundaries and the bag errors
   depend on the leaf. The extension is straightforward but should be stated
   (item R7).

## 1. Proof checks

### Setting, (F1), (F2)

(F1) is correct. With `x_{V_t} = z` fixed, running intersection makes the child
subtrees depend only on `z_{S_u}` and the outside bags only on `z_{S_t}` (a variable
of `V_t` seen outside `sub(t)` lies in `S_t`, [D] Section 1.1). So
`W_t = V_t + F_t + sum_u U_u - f* = w_t + g_t`. (F2) is immediate.

### Lemma 0

Correct. The induction `U_t^phi = Ubar_t - sum_{u in sub(t), u != t} c_u` follows by
substituting `phi_u = U_u^phi - delta_u - c_u` for the children and using the DP
decomposition of `Ubar_t`. The root infimum is
`inf_x [F - sum delta] - sum_{t != r} c_t`, and adding the non-root bag minima `c_t`
gives `rho = inf_x [F - sum delta]`. The relaxed version is the same computation with
`F~`. The one-edge remark (`delta - w = L - phi + sup(phi - U)`) reproduces the band
identity. Checked by brute-force enumeration with relaxed bags, private variables and
2D separators: error `5.3e-15` over 600 instances (`indep_trees.py`).

### Theorem 1

- *Step 1* is the per-bag rewriting `F_t^phi = g_t - sum_u eps_u + eps_t` (root: `f* + g_r - sum_u eps_u`). It is correct.
- *Step 2:* the coefficients `theta_u + D` and `1 - theta_t + D` are nonnegative, because `theta_t <= (2n-1)/(2n)`. Each `w` is at most `W_t` by (F2). The identity `theta_t = sum_{u in ch(t)} (theta_u + D) + D` follows from `E_t = sum_u (E_u + 1)`. At the root, `sum_{u in ch(r)} (theta_u + D) = sum_u (E_u + 1)/n = 1`. The telescoping over edges is correct.
- *(a)* follows from `inf w_t = 0`.
- *(c)*: `D <= theta_t <= 1 - D` puts the sliver inside the band, and the cellwise balancing is as in [K] Proposition 2.3.
- The proof uses no property of the separator dimension; my checks include 2D separators.

Numerically, `indep_trees.py` ran 600 random decompositions: 168 with a 2D separator,
32 with a bag of three children, all with private variables. The graded split is
exact to `1.8e-15`. There were 0 violations in 7,200 random perturbations. The
median ratio gap/bound is 0.81 and the maximum 1.0000. An adversarial hill-climb on
`gap(psi + r) - bound(r)` reached at most `6e-15` in 200 runs. With the discount
raised to `1.5/(2n)`, the hill-climb broke the bound in 198 of 200 runs, so the
discount matters on random instances too.

### Theorem 1'

Correct. The coefficient of `W_t` is
`sum_u (theta'_u + D') + 2D' - theta'_t = 0`, because
`theta'_t = (3E_t + 2)D' = sum_u (3E_u + 3)D' + 2D'`. At the root it is
`3nD' + D' - 1 = 0`. Also `theta'_t <= (3n-1)/(3n+1)`. My check: 0 violations in
1,800 checks with bag errors on full bag tables, including private variables. The
bag-projection margins were computed by enumeration.

### Lemma 2

Both claims are correct.

- *Claim 1.* The second difference of `U_c` is at least `-2w(c) - 2Mh^2`, by semiconvexity of `L` and `L <= U` at `c +- h`. The integral representation and the monotonicity of `U_c'` give `(h/2) Delta_U <= 2w(c) + 2Mh^2`, and similarly for `L`.
- *Claim 2.* The chord bound `r Delta/2` and the quadratic term `(M/2) r^2` are correct, though loose: the combination `(1-theta)Delta_U + theta Delta_L` could replace the sum.

Numerical check (`indep_lemma2.py`, a construction different from the author's):
concave piecewise-linear plus quadratic for `U`, convex piecewise-linear plus
quadratic for `L`, with the ordering shift computed exactly. Claim 1 held in 60,000
random cases with maximum ratio 0.4255. Claim 2 held in 6,000 cases with maximum
ratio 0.9995, so claim 2 is nearly tight. See R1 for the constant.

### Theorem 3

Correct.

- *Validity.* For an interior cell, `c_m in D`, `h = 8nr` and `dist(D, ∂I) >= 8nr` give `[c_m - h, c_m + h] ⊂ I` and `D ⊂ [c_m - h/2, c_m + h/2]`. Lemma 2 gives `osc <= w_min/(2n) + (32n + 1/2) M r^2`. The sliver bracket subtracts `w_min/(2n)` twice, so `g <= B(D)`. The near-boundary bound `Delta_U + Delta_L <= 4G + 4Mr` is correct.
- *Count.* `eta_j = (64n^2 + n) M r_j^2 - 2 eps`. The level count `J_e` follows from `2^j < l sqrt((64n^2+n)M/(8 eps))`. `sqrt(64n^2 + n) <= 8n + 1/16` holds, and a closed interval of length `x` cell lengths meets at most `floor(x) + 2 = 8n + 2` closed cells. There are `4n` near-boundary cells per end, and `r_j > rho_e` is forced. All correct.
- One consequence the note does not state: since `g_{e,D} <= B(D)` holds for *every* dyadic cell, the bound-driven rule `bd` refines only cells that R3 also refines. Its partition is a coarsening of R3's, so Theorem 3's count bound applies to `bd` as well. Section 9 ("no a-priori count of its own beyond Theorem 3") could say this explicitly.

Independent numerical check (`indep_thm3.py`). I used my own "copy tree" family:
tables `kappa (s_t - y_t)^2 + u_t(y_t)`, where all children of `t` share the
separator `y_t`. The unaries have flat valleys, concave kinks and opposite tilts.
`M_e` comes from Lemma 4.1 of [K] (sums over the bags containing the separator);
`G_e` is 1.02 times the largest grid slope. Instances:

- a tree with a bag of two children (`n = 4`);
- a star whose root has three children (`n = 4`);
- a path with two flat valleys (`n = 5`).

Each ran at `eps = 1e-2, 1e-3` and `m = 8193, 16385`:

| instance, eps | R3 cells per edge | Theorem 3 bound per edge | gap of explicit split | `bd` total cells, gap | B.4 total cells, gap |
|---|---|---|---|---|---|
| branch, 1e-2 | 490, 835, 855, 496 | 3477, 5279, 5279, 3477 | `9.9e-9` | 21, `4.0e-3` | 188, `9.0e-7` |
| branch, 1e-3 | 1123, 1604, 1619, 1198 | 5817, 9353, 9385, 6633 | `3.9e-10` | 37, `3.5e-4` | 307, `6.2e-8` |
| star, 1e-2 | 878, 873, 866, 501 | 6059, 6027, 6027, 4157 | `6.6e-10` | 11, `4.6e-3` | 209, `1.5e-7` |
| star, 1e-3 | 1853, 1848, 1841, 1384 | 14689, 14689, 14657, 10305 | `3.4e-11` | 32, `6.7e-4` | 454, `2.6e-11` |
| path, 1e-2 | 823, 892, 882, 886, 907 | 4639, 5101, 5101, 5141, 5141 | `1.8e-7` | 49, `3.7e-3` | 226, `5.2e-5` |
| path, 1e-3 | 1334, 1363, 1337, 1345, 1381 | 6185, 6689 (×4) | `1.9e-8` | 75, `4.4e-4` | 302, `3.8e-6` |

(Values at `m = 8193`. The cell counts are identical at `m = 16385`, and R3 was
never grid-limited at either size; at `m = 1025` it is, which is why fine grids are
needed.) The per-level form of the counting step held at every level, on every edge
and in every run: interior splits at level `j` were at most
`(8n+2) N_inf({w <= eta_j}, 2 sqrt((eps + eta_j)/M_e))`, near-boundary splits at most
`8n`, and those only at levels with `r_j > rho_e`. The B.4 column gives the gap of
the graded split with cell-bracket minimizers on B.4's cells. This upper-bounds
`gap(PA)` on those cells, so B.4 edge by edge also reached the tolerance here. That
is consistent with the note's open question, not an answer to it.

### Proposition 4

Correct.

- `F = 2b s1^2 + kappa(s1 - s2)^2 + b s2^2 >= 0`.
- `U_1 = kappa b/(kappa + b) s1^2`, with the minimizer interior since `|s2| <= |s1|`.
- `V_2 = (2b kappa/(2b + kappa) - b) s2^2 >= 0` iff `kappa >= 2b`.
- The evaluation of the middle bag at `s1 = s2 = +-1` bounds `rho(Aff) <= -b`.

`indep_prop4.py` computes the closed forms to `5e-6` on a 1601-point grid. It then
maximizes `rho` over both slopes with Nelder–Mead from 30 starts. The maximum is
exactly `-b` for `(b, kappa) = (1, 10), (1, 2), (0.1, 10), (0.5, 3)`.

### Proposition 5

The equality claim is correct. For fixed slopes, any intercepts can be raised
bottom-up until each cell's leafwise minimum is 0. This never lowers `rho~`, because
the parent's leaves gain at least the child's minimum. It ends at the maximal `beta`
of Lemma 1.5 of [D], where `rho~ = l_r`. The sufficient condition is also correct:
the separator terms give `n · eps/(2n)`, and the bag terms give
`(n+1) · eps/(2(n+1))`, using `err_{t,B} <= alpha' A_t w(B)^2/4 <= D' min_B W_t + eps/(2(n+1))`.
See R7 for what is missing. The note correctly limits the result to certificates
with (LC)/(CM) checked only on pairs whose interiors meet. As [D] Section 1.4 says,
such certificates are valid but are not Definition 1.2. The note flags the drift
across touching cells as unhandled, which is accurate.

## 2. Required fixes

**R1. Lemma 2, sharpness of the constant (Summary item 3 area, Section 3 remarks,
Section 7.2, the author's summary).** The note says the largest observed ratio is
0.274, "so the constant 8 is loose by about 4". The following family reaches 1/2.

- Take `I = [-1, 1]`, `c = 0`, `h = 1`, `delta > 0`.
- Let `U(s) = -J (s - p)_+` with `p = 1/2 - delta`. It is concave, hence `M`-semiconcave.
- Let `L(s) = J (q - s)_+ - J(1/2 + delta)` with `q = -1/2 + delta`. It is convex, hence `M`-semiconvex.
- Then `L <= U` on `I` (equality at `s = +-1`), `w(0) = J(1/2 + delta)`, and `Delta_U = Delta_L = J + M` on `[-1/2, 1/2]`.
- So the ratio is `(2J + 2M)/(8J(1/2 + delta) + 8M)`, which tends to 1/2 as `M, delta -> 0`.

Hence in any bound `Delta_U + Delta_L <= a w(c)/h + b M h`, the coefficient `a`
must be at least 4. The note's constant 8 is off by at most a factor 2.
Differential evolution over two-piece families reaches 0.4971, and random cases
reach 0.4255 (`indep_lemma2.py`, `logs/indep_lemma2.log`). Replace "loose by about
4" / "about 4 times too large" with "at most a factor 2 too large: an explicit family
reaches ratio 1/2". The 0.274 figure is correct for the author's random family and
can stay as an observation.

**R2. "Per-edge control of cell placement fails" (Summary item 5 heading, Section 5
heading and "What it shows", Section 9).** Rule R3 decides where to cut edge `e`
from `w_e`, `M_e`, `G_e`, `n` and `eps` alone. So Theorem 3 *is* a per-edge
placement rule that works. The same holds for `bd`, whose sliver depends only on
`U_e`, `L_e`, `E_e` and `n`, and for the B.4 rule in all tests. Proposition 4 shows
something narrower: placement driven by the one-edge *band bracket*
`inf_l [sup(l - U_e) + sup(L_e - l)]` fails, because that bracket is `<= 0` wherever
the original band contains an affine function.

The sentence "So a joint exact split is needed, not only a joint choice of values on
per-edge cells" is also misleading. On the naive cells, the LP computes the *best
joint* choice of values and still fails. On R3's cells, per-edge placement plus the
graded values succeed. The failure is in the placement criterion, not in the
per-edge nature of the placement or in the choice of values. Suggested wording:
"Cell placement by one-edge band brackets fails. Placement by margin and curvature
(R3, B.4) or by the sliver bracket of Theorem 1 works, and is still decided edge by
edge."

**R3. Remark 1.2, Status table row "Remark 1.2", Section 9: the discount `1/(2n)`
is optimal on the chain of copies for every exact split.** Take the chain with
copies enforced (the limit of the note's near-copies): root `s^2`, middle bags
forcing `s_t = s_{t+1}`, leaf 0. Then `U_e = 0`, `L_e = -s^2` and `w_e = s^2`.

1. *Setup.* A bound of the form of Theorem 1(b) with discount `c` around an exact split `psi` makes `psi + r` exact whenever `|r_e| <= c w_e`, since all brackets are then `<= 0`.
2. *Exactness criterion.* With copies enforced, the bag functions are functions of one variable `s` and sum to `s^2`. So a split is exact iff every bag function attains its minimum at `s = 0`.
3. *Two patterns.* Take `r^A_e = (-1)^e c s^2` and `r^B = -r^A`. For each middle bag `t`, one of the two patterns adds `-2c s^2`. So the normalized bag function `Delta_t` of `psi` (minus its value at 0) satisfies `Delta_t(s) >= 2c s^2`. Likewise, the normalized root satisfies `R(s) >= c s^2`, and the normalized leaf `Q(s) >= c s^2`.
4. *Conclusion.* `R + sum_t Delta_t + Q = s^2`. Hence `s^2 >= (c + 2c(n-1) + c) s^2 = 2cn s^2`, so `c <= 1/(2n)`.

Theorem 1 attains `c = 1/(2n)`. `indep_chain.py` confirms this with an LP over all
splits on a 21-point grid with `P = 1e3`, where the copies are exact on the grid.
The largest `c` for which some `psi` makes `psi`, `psi + c r^A` and `psi + c r^B`
all exact is exactly `1/(2n)` for `n = 2, 3, 4, 6, 8`. With `psi` and `psi + c r^A`
only it is `1/n`, which is the note's sketch value. The note can therefore state:
"the discount `1/(2n)` in bounds of the form of Theorem 1(b) is optimal, over all
exact splits, on the chain of copies (proof above)". That replaces a sketch with a
short proof. It says nothing about whether cell *counts* need the factor, which
stays open, as the note says.

**R4. Section 6, "Per-level versus uniform admissibility" (sketch).** The chain
`eps + eta_j <= eps + 2 max(m(x), eps) <= 2(eps + m(x))` fails at its second step
when `m(x) < eps/2`: for `m = 0` it reads `3 eps <= 2 eps`. The correct intermediate
bound is `eta_j <= max(2 m(x), eps)`. For `j >= 1`, `eta_j = 2 eta_{j-1} < 2m(x)`;
for `j = 0`, `eta_0 = eps`. This gives `eps + eta_j <= 2(eps + m(x))`, so the
conclusion stands.

**R5. Proposition 4, "What it shows".**

- "the reduced function `U'_1(s1) = min_{s2}[kappa(s1 - s2)^2 - beta s2^2]` is concave" holds only for `|s1| <= 1 - beta/kappa`. Beyond that, the box constraint `s2 = +-1` is active and `U'_1 = kappa(|s1| - 1)^2 - beta` is convex. Confirmed on the grid, for example concave on `[-0.899, 0.899]` for `(1, 10)`.
- "The reduced band still has width of order `s1^2`" holds for `kappa > 2 beta`: near 0 the width is `beta(kappa - 2beta)/(kappa - beta) s1^2`. For `kappa = 2 beta`, which the proposition allows, the width is 0 near 0 (grid value `1.4e-17` on `|s| <= 0.2` for `(1, 2)`).
- The conclusion "contains no affine function" is right in all cases: the one-cell affine bracket of the reduced band equals `beta` (`indep_prop4.py`).

**R6. Section 7.4 and Summary.** "It does not decrease when the per-edge tolerance
is lowered from `eps/n` to `eps/n^2`" is stated for the naive rule in general. In the
author's log it fails for three settings. At `eps = 1e-2` and `m = 257`:

- `n = 2`: `6.64e-3 -> 4.15e-4`;
- `n = 3`: `4.37e-3 -> 3.87e-3`;
- `n = 4`: `3.43e-3 -> 2.52e-3`.

In the ten settings that miss the tolerance, the decrease is at most about 4%. Please
restrict the sentence to those settings. My fine-grid runs support keeping the
plateau claim itself (see "Checks run").

**R7. Proposition 5: state the leafwise Theorem 1'.** The proof applies Theorem 1'
to a relaxation where bag `t`'s value is an infimum over pairs `(B, z in B)`. There,
the error `err_{t,B}` depends on the leaf, and each separator function is evaluated
on the *closed* cell containing the leaf's projection, so it is two-valued on cell
boundaries. Theorem 1' as stated has single-valued `err_t` and `phi`. The
extension holds because Steps 1–2 are pointwise in `(B, z)`. The bound becomes

`sum_e [max_D sup_{cl D}(r_{e,D} - D' w_e) + max_D sup_{cl D}(-r_{e,D} - D' w_e)] + sum_t sup_{B, z in B} [err_{t,B}(z) - D' W_t(z)]`.

This should be written as a one-line lemma, rather than left inside "each cell's
affine piece is used on the closed cell".

**Trivial.** Remark 1.1 says the grading "makes the weight decrease from the root to
the leaves by `1/n` per edge". That is exact on paths. On trees the decrease from
`t` to a child `u` is `(E_t - E_u)/n >= 1/n`.

## 3. Optional suggestions

- **Link to the certificate lower bound (my sketch, not checked beyond the
  argument).** Assume the gap weights of the child bag `t(e)` include the separator,
  `S_e ⊂ K_{t(e)}`, and let `M = max_e M_e`. Then
  `N_inf(pi_{S_e} E(eta), 2 sqrt((eps+eta)/M)) <= ceil(sqrt(M/alpha)) N_inf(pi_{K_t} E(eta), 2 sqrt((eps+eta)/alpha))`.
  The bag-by-bag form of Theorem 2.5 of [D] (as used in the proof of Proposition
  B.1 of [E]) gives `|L_t| >= 2^{-|K_t|} sup_eta N_inf(pi_{K_t} E(eta), ...)`, and
  each bag has one parent edge. So `sum_e N_e <= ceil(sqrt(M/alpha)) 2^{w+1} N_dec(eps)`.
  With Theorem 3, the exact-bag separator-cell count is at most
  `O(|T| log) ceil(sqrt(M/alpha)) 2^{w+1} N_dec(eps)`. This would make the
  parenthetical in "What this settles" precise.
- State that `bd` inherits Theorem 3's count (Section 1, Theorem 3 above).

## 4. Checks run

All commands were run from `reviews/covering-upper-half-review-checks/` unless noted,
single-threaded. These are targeted checks. CI was not consulted, and no CI result is
reported here.

| Command | Log | Result |
|---|---|---|
| author: `python3 check_graded_split.py` (in `theory-decomposition/covering/`) | `logs/rerun_check_graded_split.log` | identical to the author's log |
| author: `python3 check_kink_concentration.py` | `logs/rerun_check_kink_concentration.log` | identical |
| author: `python3 check_prop4.py` | `logs/rerun_check_prop4.log` | identical (apart from timing lines) |
| author: `python3 run_paths.py 16385 257` | `logs/rerun_run_paths.log` | identical to the author's log apart from timing fields (the table of Section 7.3) |
| `python3 indep_trees.py` | `logs/indep_trees.log` | Lemma 0 (exact `3.6e-15`, relaxed `5.3e-15`), Theorem 1 (0 of 7,200; adversarial max `6e-15`), Theorem 1' (0 of 1,800); discount `1.5/(2n)` broken in 198 of 200; reversed grading non-exact in 138 of 146 paths; `phi = L` non-exact in 235 of 235 branching trees |
| `python3 indep_chain.py` | `logs/indep_chain.log` | graded split with `r = -c w`: gap `c - 1/(2n)` (for example 0.1875 at `n = 8`, `c = 1/4`); largest admissible discount over all exact splits `1/(2n)` (two patterns) and `1/n` (one pattern) |
| `python3 indep_lemma2.py` | `logs/indep_lemma2.log` | claim 1 max ratio 0.4255 (random), 0.4971 (adversarial), edge-kink family 0.4999; claim 2 max ratio 0.9995 |
| `python3 indep_thm3.py 8193`, `... 16385` | `logs/indep_thm3_m8193.log`, `logs/indep_thm3_m16385.log` | table above; R3 gap `<= 2.1e-7`, bounds and per-level counting step hold, never grid-limited |
| `python3 indep_prop4.py` | `logs/indep_prop4.log` | `rho(Aff) = -b` exactly in four cases; reduced-band statements as in R5 |
| `python3 indep_naive.py 257` | `logs/indep_naive_m257.log` | reproduces the author's `m = 257` rows exactly (cells and LP gaps) with an independent cutting-plane LP; `bd` and B.4 LP gaps `<= 8.3e-8` |
| `python3 indep_naive.py 513 1025 2049` | `logs/indep_naive_fine.log` | plateau persists: `n = 6`: `1.22e-2–1.27e-2`, `n = 8`: `2.33e-2–2.36e-2` at every grid and both tolerances |

On the plateau: the note computed the LP only on grids with `m <= 257` and says so.
My runs rule out a coarse-grid artifact up to `m = 2049`. For `n = 8` and
`eps = 1e-3`, the LP gap on the naive cells is `2.29e-2`, `2.33e-2`, `2.35e-2`,
`2.36e-2` at `m = 257, 513, 1025, 2049`. These are still grid computations, not
continuum values.

Scope of my checks: finite grids, floating point, HiGHS. The Theorem 3 check applies
a continuum rule to grid problems. Its semiconcavity constants are analytic upper
bounds (Lemma 4.1 of [K]), while `G_e` is a grid estimate inflated by 2%.

## 5. Claim-by-claim status

| Claim (author's list) | Verdict |
|---|---|
| Lemma 0 | correct; confirmed with relaxed bags, private variables, 2D separators |
| Theorem 1 (exact graded split, discounted sandwich, cellwise form, `n = 1`) | correct; confirmed; the discount is optimal on the chain for every exact split (R3) |
| Theorem 1' | correct; confirmed; its leafwise use in Proposition 5 needs a stated lemma (R7) |
| Lemma 2 | correct; "loose by about 4" wrong, at most 2 (R1) |
| Theorem 3 | correct (validity and count); confirmed on branching trees and a path with independent code |
| Proposition 4 | correct; confirmed; two descriptive statements too broad (R5); plateau reproduced and persists to `m = 2049`; "does not decrease" to be restricted (R6); the "per-edge placement fails" framing to be corrected (R2) |
| Proposition 5 | equality correct; sufficient condition correct given R7; size estimate is a sketch, correctly labelled; R1 reading of Conjecture B.5 open, correctly stated |
| Numerical claims (B.4 edge by edge, bd 0.7–2.2 cells per covering number, sup-norm 2.6–22 times more, `phi = L` non-exact 238/238) | reproduced from the author's logs and reruns. My instances: B.4 and bd reach `eps` in every run; `phi = L` non-exact 235/235 |

## 6. Literature and novelty

The note's novelty statement is suitably qualified: two short searches, and "does not
establish novelty". I ran two more short web searches.

- **Quantitative Ilmanen / semiconcave–semiconvex bounds.** The search returned generalizations of Ilmanen's lemma to other moduli and to Hilbert and superreflexive spaces (Kryštof, *Comment. Math. Univ. Carolin.* 59(2), 2018, and 62(4), 2021; I saw only the abstracts in the search results). As described there, they are qualitative (existence of a `C^{1,omega}` function in between). I found no interval form like Lemma 2. The pointwise computation behind Lemma 2 is the one used in standard proofs of Lemma 4.2 of [K] and of Ilmanen's lemma, so Lemma 2 is best described as an aggregated one-dimensional form of a standard estimate. The note's wording ("quantitative, one-dimensional form of pinch regularity") is consistent with that.
- **Reparametrizations and splits.** I found lecture notes on reparametrizations, TRW literature, and N. Ruozzi and S. Tatikonda, "Message-passing algorithms: reparameterizations and splittings" (arXiv:1002.3239). The last is relevant background for Lemma 0 and the split viewpoint. The note does not cite it; adding it to Section 8 would help. None of these sources contained the monotone grading or the discounted sandwich.

This does not establish novelty either.
