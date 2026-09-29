# Review of "Do stronger convexifications move the sparse-regression thresholds?"

Reviewed file:
[`../bb-complexity/sparse-regression/stronger-relaxations/thresholds.md`](../bb-complexity/sparse-regression/stronger-relaxations/thresholds.md)
(cited below as [SR]; its parent note
[`phase-transition.md`](../bb-complexity/sparse-regression/phase-transition.md)
is cited as [PT]). Reviewer: independent adversarial reviewer
(high-dimensional probability, convex relaxations and SDP, sparse regression).
I did not write this material. Date: 2026-09-29. I did not edit the note and
did not commit.

*Status of the note.* The author revised the note while this review was
in progress, working from an interim draft of this file (the note's
"Revision after review" section). The Findings below refer to the text as
first reviewed. The section "Check of the revision" at the end verifies the
revised statements and lists what remains open: the Table 7.3 count in F9
and the regime of the new `gamma -> 0` claim in Section 6.3 (R1).

My scripts and logs are in [`stronger-relaxations/`](stronger-relaxations/).
They use my own cvxpy models and my own enumeration code. The instance
generators mirror the documented generators (`core.instance`,
`exp_mech.make`), which I read. The regenerated instances reproduce the
stored `lam`, `f(S*)` and `OPT` exactly, and the stored perspective and
`SDP1` values to about `1e-9` relative. The only import
of the author's code is in `rv_small.py`, which calls the author's `relax.py`
solely to compare its values with mine.

## Verdict

| Claim | Verdict |
|---|---|
| (1) Definitions of the relaxations and their nesting (Section 1.2, Lemmas 1.2–1.4) | **Correct for the free-sign model, with one factual error and two missing conventions.** The perspective relaxation, `SDP1`, `sdp_r`, the free-sign 2×2 hull and `L_r` are stated faithfully (checked against the arXiv sources of Atamtürk–Gómez, Han–Gómez–Atamtürk, Wei et al. and Dong), and Lemmas 1.2–1.4 are correct. My independent models satisfy `persp <= SDP1 <= sdp_2 <= L_2 <= L_3 <= OPT` and `SDP1 <= zb <= OPT` on all 18 test nodes. **Error:** Han–Gómez–Atamtürk's `OptPairs` is a relaxation for *nonnegative* continuous variables. It is not valid for this model and is not dominated by `L_2` (F1). **Conventions:** `H_T` drops the cardinality constraint, and node relaxations fix only `z`. Both matter outside the theorem's use (F3). |
| (2) Theorem 4.4 and Sections 4.1–4.3, Proposition 3.1 | **Correct.** I checked every step and constant of Lemma 4.1 (i)–(iii), Lemma 4.2, Corollary 4.3, Theorem 4.4 (a)–(e), Lemma 2.5′ and Proposition 3.1. Both directions hold: `R >= g` gives achievability, and `R <= L_r <= P_{eps_p}` gives the converse. A rebuilt Lemma 4.1 point for a five-support mixture passes all 780 pair-hull tests and 535 sampled triple-hull tests. Two controls fail as they should. Only minor slips remain (F5). |
| Remark 4.5 (Shor lift in `(zeta, beta)`, McCormick, lifted cardinality) | **Correct** (moment matrix built explicitly and checked). **But the "local versus non-local" framing is wrong** (F2). The product cones that escape the obstruction are *pairwise* constraints. They are implied by the exact 2×2 hull of the richer lift `(zeta, beta, zeta zeta', zeta beta', beta beta')`. What Theorem 4.4 covers is locality in the `(z, beta, beta beta')` lift. |
| (3) Corollary 4.6 (hard-side cliques for `L_2`) | **Correct as a sketch, and adequately labeled** (in the statement, the proof and the Summary). The uniform bounds on `theta_U` and `q_max` hold. It depends on the node convention of Definition 1.1: a solver that deletes fixed-to-zero columns computes stronger leaf bounds, and the proof does not cover those (F3). It inherits the `OptPairs` sign issue (F1). |
| (4) Section 5: validity of `zb`, Propositions 5.1, 5.3 and Corollary 5.2 | **Correct.** The product cones are valid. Propositions 5.1 and 5.3 and Corollary 5.2 are proved correctly, and my numerical checks pass. **Overstatements:** "`≈ 4 sqrt(|A|/n)` on any support `A`" holds only for `A` independent of `X`. Uniformly over supports of size `s`, the fraction is of order `sqrt(s log(p/s)/n)`, which is `Theta(1)` for `s ≈ k` at `n ≈ 2k log p`. "`zb` can be inexact only through points whose support is large" is not proved (F4). The novelty claim is hedged. It should add that the product cones are 2×2 principal minors of the degree-4 (level-2) moment matrix, and that they are implied by 2×2 hulls in the full lift (F2, F7). |
| (5) Section 6 (BAHSWZ, arXiv 2205.09727) | **The body is accurate against the source** (read in the LaTeX source, Section 3.2, its sparse-regression theorem and the remarks after it): the model, `R_LD(theta)`, LASSO at `R > 2/(1-theta)`, thresholding at `R > 2`, the open recovery problem, and `theta -> 0`. **The Summary misattributes:** "the low-degree analysis ... places the conjectured polynomial-time recovery threshold at `n ≈ 2k log(p/k)`". BAHSWZ say that prior work *suggests* hardness of approximate recovery for `R < 2`. Their low-degree bound supports this only as `theta -> 0`, and they say it does not suggest a sharp recovery bound for larger `theta` (F6). |
| (6) Computations (Section 7) | **Reproduced where checked**, with two tolerance artifacts (F9). At `n = 40`, `p = 100` the perspective relaxation is exact in **2** of 8 runs, not 3. Seed 2006 fails the PWE criterion (ratio 1.0018) and has a relative gap of `1.9e-7`. In Table 7.3, one run counted `zb`-exact (`k = 6`, `alpha = 2`, seed 3002) is undecided at the `1e-5` level. All recounted cells of Tables 7.1–7.3 match. I independently reproduced the `p = 1000` certificate (with the full enumeration of `OPT`), the `p = 3200` restricted values and the full-instance `L_2` certificates, and pure-noise `zb` values (Section 5 below). |

Overall: the main theorem (Theorem 4.4) and its proof are correct, and the
computations support it. The corrections concern scope and framing
(F1–F4, F6), not validity.

## Findings

**F1 (factual; Summary, Section 1.2, Lemma 1.2(d), Corollary 4.6, Section 8).**
`OptPairs` of Han–Gómez–Atamtürk (arXiv 2004.07448) is built for the set
`{(x, y) in {0,1}^n x R^n_+ : y_i (1 - x_i) = 0}`. It uses nonnegative
continuous variables (checked in their source: problem `CQI`, the
`OptPersp` and `Shor` formulations, and `sdppos`). With `b >= 0`, every
point of the lifted hull has a completely positive moment matrix
`[[1, beta'], [beta, B]]`; in particular `B >= 0` entrywise. That hull is
*smaller* than the free-sign `H_T`, and it is not valid for the note's model
with `beta*_i = ±b`. So neither "`L_2` dominates `OptPairs`" nor
"`OptPairs` is below `L_2` (Lemma 1.2(d))" holds as written. The
construction also fails in the nonnegative setting, because its helper
cross-moments `C_m G_F'` have both signs. **Correction:** replace `OptPairs`
by "the free-sign analogue of `OptPairs` (2×2 decompositions using the
free-sign hull of Wei–Atamtürk–Gómez–Küçükyavuz, Proposition 2)". The
disjunctive 2×2 decompositions of Frangioni–Gentile–Hungerford are also
covered once they are adapted to unbounded variables, as Wei et al. note. With
explicit bounds `l <= beta <= u` they use information the model does not have. Keep the
correct statement that Han–Gómez–Atamtürk prove `Shor = OptPersp` in the
nonnegative setting.

**F2 (framing; Summary "Beyond local lifts", Sections 2, 5, 6.3, 9.1).** The
note says that local lifts cannot move the constants and that "any relaxation
that does must use non-local structure, such as the product cones of Section
5". The product cone `U_jm^2 <= Z_jm B_mm` involves one pair `{j, m}`. At
every generating point `(zeta, b)` of the full pairwise lift,
`(zeta_j b_m)^2 = zeta_j zeta_m b_m^2`, so the cone holds with equality there.
The cone is closed and convex, so the exact 2×2 hull of
`{(zeta, b, zeta zeta', zeta b', b b')}` implies it. McCormick on `Z` is also
pairwise. Proposition 5.1 uses only these pairwise constraints and the global
PSD matrix. It does not use `Z 1 <= k z`. So the obstruction is escaped by
*lifting the cross products `zeta_j beta_m`*, not by non-locality. Theorem 4.4 is about locality in the
`(z, beta, beta beta')` lift (plus the Shor/McCormick additions of Remark 4.5).
**Correction:** rename "beyond local lifts" to "beyond the
`(z, beta, beta beta')` lift". Restate Section 6.3 as "must lift the products
`zeta_j beta_m` or use global constraints". Note that `r`-wise hulls in the full
`(zeta, beta)` lift are not covered by Theorem 4.4, and that Proposition 5.1
shows that already `r = 2` escapes the two-coordinate obstruction.

**F3 (conventions; Definition 1.1, Lemma 1.3, Corollary 4.6).**

- *Node relaxations.* `L_r(S0, S1)` imposes the root hulls `H_T` and fixes only
  `z`. A feature `m in S0` therefore keeps a free `B_mm >= 0`, because
  `H_{m} ∩ {z_m = 0} = {(0, 0, B) : B >= 0}`. It can serve as a helper. The exact hull of the *node's* feasible set,
  or a solver that deletes fixed-to-zero columns, has `B_{m.} = 0`. Theorem 4.4 is unaffected. Its converses use only
  the root and nodes `(∅, {j})`, and the construction also lies in the
  node-level hull with `zeta_j = 1` fixed (all generating points used there
  have `zeta_j = 1`). Corollary 4.6, however, bounds leaves of arbitrary
  convex-piece trees. A variable-branching leaf containing both `1_S` and
  `1_T` may have fixed every helper to 0. Under the column-deletion convention
  the proof gives nothing for that leaf. **Correction:** state the convention
  (node bound `= inf_{z in K ∩ Q_v} R(z)` with `R` the root-lifted projected
  function) in Corollary 4.6. Also say that implementations which delete
  fixed columns are not covered.
- *Cardinality.* `H_T` omits `|zeta| <= k`. The note says this changes
  nothing for `r <= k`, which is right. Theorem 4.4 allows any `r_p` with
  `r n log p = o(p)`, which includes `r > k` when `k` is small. Then `L_r` is
  weaker than the exact hull of the cardinality-constrained set on `r`-sets.
  Lemma 1.2(b) also fails for that hull, because it needs the generating point
  `(1_T, w, w w')` with `|T| > k`. For example, with `k = 1` the cardinality
  hull on a pair forces `B_jm = 0`. The theorem as defined is correct. The
  Summary's "exact closed convex hull on every `r`-set" should say "of the
  set without the cardinality constraint (equivalently, for `r <= k`)".

**F4 (overstatements in Section 5 and the Summary).**

- "`zb` loses at most the fraction `(Lambda_max - Lambda_min)/(lam + Lambda_max) ≈ 4 sqrt(|A|/n)` ... on any support `A`". The deterministic bound
  is right. The approximation `4 sqrt(s/n)` holds for a fixed `A`
  independent of `X`. For the minimizing `z` (data-dependent `A`), what matters is the
  worst case over `|A| = s`. By the union bound behind (G3), that worst case is about
  `4 (sqrt s + sqrt(2 s log(ep/s)))/sqrt n`. At `s ≈ k`, `n ≈ 2k log p` this is
  `Theta(1)`, not small. "On any configuration with few coordinates, `zb`
  can lose only a vanishing fraction" therefore needs `s log(ep/s) = o(n)`.
  The note says as much for the pure-noise regime (Section 5, second
  consequence). The Summary and the text after Proposition 5.3 should too.
- After Corollary 5.2: "`zb` can be inexact only through points whose support
  is large enough that `Lambda_A` is small". This is not proved. Proposition 5.3
  allows a gap at a small support whenever
  `frac_A (OPT - f(A)) > 0`. Present it as the heuristic reading of
  Corollary 5.2 and Proposition 5.3.

**F5 (minor slips; none affects a conclusion).**

- Theorem 4.4(b) uses `||x_l||^2 <= nu` for the violator `l in H2`, but
  (E1)–(E3) of Lemma 4.2 concern the helper half. One more union bound with
  (G2) over all features is needed. The same holds for "`||X_F||^2 <= 16n` on (G3), (E2)".
- Remark 4.5, *Constants*: "`eps_p` enters additively as `2 log(1 + eps_p)` in `tau^2`". To first order (Section 2), pricing at `lam(1 + eps)` turns the
  root threshold into `tau^2 = 2 log p/(1 + eps)^2`. That is a factor, or an
  additive shift of about `4 eps log p` in `tau^2`. The stated form looks
  wrong or needs a derivation.
- Section 2: "descent iff `|a_l| > (1 + c) m0`". Section 4.3 proves only the
  "if" direction, and "iff" for a uniformly inflated relaxation is heuristic.
- `c := min(1, eps/12)`: the `min` is redundant for `eps < 1`.
- Tables 7.1–7.2 report "median #viol." as 5, 9, 16, 33, ... For even counts the
  medians are 5.5, 9.5, 16, 33.5, ... (trivial).

**F6 (Section 6 attribution; Summary lines 85–92).** In BAHSWZ (Section 3.2
and the remark "Implications for recovery"): LASSO achieves exact recovery at `m > 2k log n`; thresholding
achieves approximate recovery at `R > 2`; the information-theoretic threshold is `m_inf = o(k log(n/k))`; and "this line of work
suggests the presence of a possible-but-hard regime for approximate recovery
when `0 < R < 2`". Their theorem proves low-degree hardness of *detection* only for
`R < R_LD(theta)`. The authors add that "for larger values of `theta` there
appears to be a detection-recovery gap, so our lower bound ... does not
suggest a sharp recovery lower bound". The body of Section 6 matches this.
The Summary's "The low-degree analysis ... places the conjectured
polynomial-time recovery threshold at `n ≈ 2k log(p/k)`" does not.
**Correction:** "The recovery threshold `n ≈ 2k log(p/k)` is conjectured in the
literature summarized by BAHSWZ. Their low-degree analysis proves detection
hardness below `alpha = 2(1 - sqrt gamma)^2` (`gamma < 1/4`), which tends to 2 as `gamma -> 0`." A
possible strengthening: as `gamma -> 0`, the conditional optimality of the
constant 2 rests on the proven low-degree *detection* bound (plus the
low-degree conjecture and Arpino's reduction from detection to approximate recovery), not only on the recovery conjecture. Also
note that the conjectures concern approximate recovery, while root exactness
is exact recovery. The inference goes in the right direction, but it should be said.

**F7 (novelty and positioning of `zb`).** The hedge is appropriate. Two facts
should be added:

- After reducing by the ideal `beta_m (1 - zeta_m) = 0`, `zeta^2 = zeta`, the product cone is the 2×2 principal minor on the
  monomials `{zeta_j zeta_m, beta_m}` of the degree-4 (level-2) Lasserre moment
  matrix. So `zb` is a sparse, partial level-2 moment relaxation. The term
  "degree-2 SoS/moment relaxation" in Section 6.4 is therefore slightly off.
- The product cones are implied by exact hulls of the full lift with
  switching variables, for example Anstreicher–Burer, "Quadratic optimization with switching variables: the
  convex hull for n = 2" (Math. Program. 2021). I recall that paper from memory; they treat bounded `x`, so check it before citing. Wei et al. cite it for
  disjunctive representations of the free-sign 2×2 hull.

The claim that the analysis of Propositions 5.1 and 5.3 for sparse regression is new looks plausible.

**F8 (reference).** "Zheng–Fan–Sun (SDP to compute the best diagonal
perturbation ...; from memory)". Crossref finds no such paper. The work
meant is almost certainly X. Zheng, X. Sun, D. Li, "Improving the performance
of MIQP solvers for quadratic programs with cardinality and minimum threshold
constraints: a semidefinite program approach", INFORMS J. Comput. 26 (2014).
The earlier source for SDP-computed diagonal perturbations is
Frangioni–Gentile (2007).

**F9 (tolerances in Section 7).**

- *Perspective relaxation.* At `n = 40`, `p = 100`, seed 2006: `max|a_l|/m0 = 1.0018`, so
  the root is inexact by PT Corollary 2.4. My own perspective solve gives the
  gap `8.2e-6` (relative `1.9e-7`), which the `1e-6` rule counts as exact.
  Table 7.2 and the Summary ("8 of 8 runs, against 3") should say 2, or
  state the tolerance. The perspective relaxation has an exact decision
  (the PWE ratio), so use it.
- *`zb`.* Two stored `zb` values exceed `OPT`: by `3.0e-6` (k = 3, alpha = 1, seed 3000, SCS
  `1e-7`) and by `3.3e-5` (k = 6, alpha = 2, seed 3002, SCS `1e-6`). The one-sided rule counts both
  as exact. I re-solved the second run with Clarabel (`rv_zbcheck.py`). Clarabel stops with status
  `optimal_inaccurate` at `zb = OPT(1 - 3.8e-5)`. So this run is undecided at the `1e-5` level: one
  inaccurate solver is above `OPT` and the other below. It belongs in the "unclear" column, not
  the "exact" one. Table 7.3 should then read, for `k = 6`, `alpha = 2`: 1 exact, 2 inexact, 1 unclear.
  The totals should read 40 exact, 28 inexact, 3 unclear, and the Summary's "exact in 41 of 71" should change to match. Use a
  two-sided rule, or report solver status, for SCS values. The qualitative conclusions do not change.
- *`SDP1`.* Dong's Theorem 2 gives an exact root-exactness test without
  solving the SDP: bisection on the scalar and one PSD test (Dong, Section 3.1). It would make the `SDP1`
  counts rigorous.

## 1. Relaxations and nesting (item 1)

Checked against the arXiv LaTeX sources:

- **Atamtürk–Gómez 1901.10334** (`eq:sdpr`). `sdp_r` has
  `0 <= w_T <= min(1, e'z_T)` and `[[w_T, beta_T'], [beta_T, B_T]] ⪰ 0` for all `|T| <= r`,
  together with `B ⪰ beta beta'` and `e'z <= k`. It is an extended SDP of the optimal
  rank-one decomposition. `sdp_1` is the optimal perspective relaxation. The
  note's description is faithful. (Formula numbers were not checked.)
- **Han–Gómez–Atamtürk 2004.07448.** Theorem 1 (`thm:equivalence`) is
  `Shor = OptPersp` for `CQI` with `y >= 0`. `OptPairs` (`sdppos`) is also for `y >= 0` (F1).
- **Wei–Atamtürk–Gómez–Küçükyavuz 2201.00387**, Proposition 2
  (`prop:2x2extended`): the free-sign hull of `X_{2×2}`. Faithful.
- **Dong 1603.04572**, Theorem 2 (`thm:dualcert`). It is an
  if-and-only-if certificate with `d~ >= 0`,
  `rho^{-1} X'X + I - D(d~) ⪰ 0`, equality on `S`, and inequality off `S`. Proposition
  3.1(a) is its sufficiency half with `mu = rho d~`, written with `min_S`
  instead of equality. This is equivalent, since lowering `mu_i` on `S`
  keeps `Q ⪰ diag(mu)`.

Lemma 1.2:

- (a)–(c) are correct.
- (b)'s limit argument uses the generating point `(1_T, v/sqrt eps, v v'/eps)`, which is valid because `H_T` has no cardinality constraint (F3).
- (d): the `sdp_r` set is closed, being the projection along the compact coordinate
  `w`, and convex, since `min(1, 1'z)` is concave. It contains all generating points.
  The decomposition bound follows from the definition of the closed convex
  envelope.

Lemma 1.3 is correct. Lemma 1.4 is correct: `K(S0, S1)` is integral because the
constraint matrix is TU, and `E xi xi' = beta beta' + D` with `tr D = pi`.

Numerically (`rv_small.py`; 6 instances with `n = 5..8`, `p = 8..10`, `k = 2, 3`, noise, weak signal and planted signal; nodes: the root, one forced-in node and
one removal node; `OPT` by enumeration):

- no order or validity violation among perspective, `SDP1`, `sdp_2`, `L_2`, `L_3`, `zb`, and `zb` without product cones;
- exact nodes: perspective 0/18, `SDP1` 2/18, `sdp_2` 11/18, `L_2` 13/18, `L_3` 14/18, `zb` without product cones 8/18, `zb` 18/18;
- the author's `relax.py` (`sdp1`, `sdp2`, `L2`, `zb`) agrees with my models to within `2.9e-6`.

The author's disjunctive `L2` model is the correct closed hull (its recession
block is redundant but harmless).

## 2. Theorem 4.4 and its ingredients (item 2)

**Lemma 4.1.** I re-derived each identity.

- `X G = X_F G_F + X_{Z1} C = 0` and `X_{Z1} K = 0`, so `<X'X, E> = 0`.
- `tr E = (1+sigma) pi + ||C||_F^2 + tr K`.
- `||C||_F^2 = (1+sigma) tr(Y' W^{-1} Y)`.
- Hull constraints: Lemma 1.4 on `T' = T ∩ F`, zero extension, and PSD augmentation reduce each
  constraint to `Xi_M ⪰ 0`, where `E_FF - D = sigma D`, `E_MF = C_M G_F'` and
  `E_MM = C_M C_M' + K_MM`.
- (i): `K_MM ⪰ kappa(1 - eta) I` gives the Schur condition.
- (ii): `K_mm >= (1 - q_m)^2 Lambda_m = ||C_m||^2/sigma`, and then
  `||C_m||^2 (1+sigma) D/(||C_m||^2 (1 + 1/sigma)) = sigma D`. Also
  `tr K = sum_m (1 - q_m) Lambda_m`.
- (iii): with `sigma = 0` and `K = 0`, only the diagonal cones remain, and they hold.

Numerically (`rv_construction.py`: `n = 6`, `p = 40`, `k = 3`; `z` is a random
mixture of **five** 3-subsets of a 7-set, not the two-point mixture used in [SR]):

- (a) global PSD (min eigenvalue `-6e-17`); `<X'X, E> = -2e-15`; identity (o) exact to `1e-10`;
- (b) the (ii) point lies in `H_T` for **all 780 pairs** (independent disjunctive
  SDP; worst margin `-1.4e-9`);
- (c) the (i) point with `r = 3` lies in `H_T` for all 35 triples inside `F` and for 500
  sampled mixed triples (worst margin `-1.1e-9`);
- (d) controls: with `K = 0`, 38 of 70 tested pairs fail (margin `-5.7e-3`), and the pairs-only
  point fails 3 of 200 triples. So the null-space component `K` is necessary, and
  the `r`-dependence of `kappa` in (i) is real;
- (e) Remark 4.5: the explicit moment matrix of `(1, zeta, beta)` is PSD (min eigenvalue
  `-2e-15`), with `diag Z = z`, `diag U = beta`, McCormick and `Z 1 <= k z` exact. It
  violates 231 of 1560 product cones (max violation `1.6e-2`), as the note says;
- (f) the solved `L_2` root (2.309) is below `Phi` at the point (29.38). This is
  consistent: at `n/p = 0.15` the construction is expensive (`theta_F = 0.59`).

**Lemma 4.2 and Corollary 4.3.**

- (E1) is (G3) with `t = 2 sqrt(log p)`.
- (E3) is Laurent–Massart for `x'Ax`, using `||A||_F, ||A|| <= tr A`, with `x_m` independent of `W_{-m}` and of the
  `G_H`-measurable `Y`.
- Sherman–Morrison gives `||C_m|| <= sqrt(1+sigma) ||x_m' W_{-m}^{-1} Y||`, and Weyl gives
  `lambda_min(W_{-m}) >= w_- - nu`.
- These give `tr K = O((r-1) n log p pi/(sigma p))` and `||C||_F^2 = O(n pi/p)`, so
  `eps_p = O(sqrt(r n log p/p))` with `sigma_p = sqrt(r n log p/p)`. Correct.

**Theorem 4.4.**

- (a), (c): `R >= g` node by node, and `R <= OPT` by validity. Correct.
- (b) measurability: `S*`, `m0`, `i`, the maximizer `l in H2` and the mixture are
  `G_{H1}`-measurable, and `F ∩ H1 = ∅`.
- (b) algebra: I re-derived
  `P_ebar = f(S) - 2 s a_l + s^2(||x_l||^2 + lam) + lam(1 + ebar)[beta_i^2 t0/(1-t0) + s^2(1-t0)/t0]`
  and, with `s = t0 a_l/(lam(1 + ebar))`, the bracket bound.
- (b) constants: `sqrt((2 - eps/2)/(2 - eps)) >= 1 + 15 eps/128 > 1 + 3 eps/32 > 1 + eps/12`,
  `(1 + c/4)/(1 - c/8) <= 1 + c/2` for `c <= 2`, and
  `(1 + c/2)/(1 + c)^2 <= 1/(1 + c) <= 1 - c/2` for `c <= 1`. The bracket is at least `c/8`. Correct.
- (d), Lemma 2.5′: I re-derived it line by line. The `(1+ebar)` factor lands on both
  `kappa sum|w_l|` terms, which gives `-2 sum|w_l|(|a_l| - (1 + ebar) kappa)`.
- (d), the mixture: it is on `S ∪ V'` with budget exactly `k - 1`, so `D` vanishes at `j`
  and `Y` is common to all `j` in the half.
- (d), constants: `e'_l >= (delta0/2) kappa`,
  `T <= 6/delta0 = 96/eps`, and `2(1 + 96/eps)^2 + 1 + 96/eps <= 18915/eps^2 <= 20000/eps^2`.
  The final `(1 + eps/32)(3/2) - 3 < -1`. Correct.
- (e) follows. So both directions of the sharp thresholds hold for every `R` between `g` and `L_r`.

**Proposition 3.1.**

- (a) is the weak-duality argument. The key identity `v = c - (Q - D_mu) beta^S`
  gives `mu_i beta^S_i` on `S` and `a_l` off `S`. Correct.
- (b): the dual is `max sum mu_i d_i` subject to `Q ⪰ diag(mu)`, and
  `mu_i <= 1/(Q^{-1})_ii = lam + x_i'(I + X_{-i} X_{-i}'/lam)^{-1} x_i`. Correct.
- (c) is correct. The stated probability `1 - 2/p` is conservative (`1 - 2/p^2` holds).

Numerically (`rv_props.py`, 9 instances with `z` fixed): `SDP1(z) <= g_delta(z)` and
`SDP1(z) <= P + lam theta_F pi` held in every case (see Section 5 below for the log).

## 3. Corollary 4.6 (item 3)

The steps are as described:

- the midpoint is the two-point mixture;
- Lemma 4.1(ii) with `F = U`, `Z1 = [p] \ U` gives `L_2(mid) <= ||y - X beta||^2 + (2 + e2) lam ||beta||^2`;
- `theta_U <= ||X_U||^2/(lambda_min(XX') - ||X_U||^2)` uniformly over `|U| <= 2k`;
- `q_max <= max_m ||x_m||^2/lambda_min(W) = O(n/p)`;
- `p/n -> inf` in the regime `k log(p/k) ≍ n`, `k = o(n)`;
- PT's proof uses the penalty only through `lam = o(n)`.

The union bound for `||X_U||` omits the `log(1/delta)` term, and failure
probabilities are not tallied. These are the "error terms not written out".
The label "corollary with proof sketch" is adequate. The two substantive caveats are F3 (node
convention) and F1 (`OptPairs`).

## 4. Section 5 (item 4)

- *Validity.* `E[zeta_j xi_m] = E[zeta_j zeta_m xi_m]`, so Cauchy–Schwarz gives
  `E[zeta_j zeta_m] E[xi_m^2]`. Integer points satisfy the cones with equality.
  `Z 1 <= k z` is `E[zeta_j |T|] <= k z_j`. Correct.
- *Proposition 5.1.*
  - `beta_m = 0` and `U_jm = 0` off `A` (2×2 minor, McCormick `Z_jm <= z_m`, product cone), so `u_m ⊥ w_j`.
  - `<u_j, w_j> = beta_j(1 - z_j)` and `||w_j||^2 = z_j(1 - z_j)`.
  - Projecting onto `span{w_j}` gives `<Q, Gram(u)> >= (lam + Lambda_A) sum_F beta_j^2 (1/z_j - 1)`.
  - Correct. Only pairwise constraints and the global PSD are used (F2).
- *Corollary 5.2.* The weak-duality bound with `a = r_S` gives exactly the stated
  expression. The first-order form and the `(1 + Lambda/lam) m0` threshold are correct.
- *Proposition 5.3.* `F_{Lambda_+}(beta) >= OPT_v` follows from the node-feasible mixture, since
  `<X'X + lam I, D> <= (Lambda_+ + lam) tr D`. The interpolation
  `F_{Lambda_-} = s F_{Lambda_+} + (1-s) G` and `G >= f(A)` finish the proof. Correct.
  The Gaussian approximation needs the uniformity caveat (F4).
- *Numerics* (`rv_props.py`). `zb(z) >= g_{Lambda_-/lam}(z)` (Proposition 5.1), both
  Proposition 5.3 bounds, and `zb(z) >= SDP1(z)` held on all 9 fixed-`z`
  instances. On the small instances `zb` was exact at 18 of 18 nodes, and `zb`
  without the product cones at 8 of 18. So the cones are what make `zb` strong.

## 5. Computations I reproduced (item 6)

All runs used my own models, Clarabel (tolerance `1e-10`), BLAS/Rayon threads
pinned to 1, and at most 4 processes.

- **`p = 1000` certificate** (`rv_p1000.py`, instance `n = 30`, `k = 3`, seed 1).
  - Full enumeration of the 166 million triples (10 s) confirms `OPT = f(S*) = 34.96921938`.
  - My own Lemma 4.1(ii) point (violator `l` in `H2`, helpers `H1`, ratio 1.99) has
    `<X'X, E> = -5e-17` and a global PSD min eigenvalue of `-2e-16` (scaled).
  - The Schur sufficient condition holds on all 1,992 `Z1 × F` pairs, and exact hull membership holds on 60 sampled pairs.
    Pairs inside `F` or inside `Z1` are covered by Lemma 1.4 and Lemma 1.2(b). So the point is in `L_2`.
  - `Phi - f(S*) = -0.454`. The note reports `-0.123` from a coarser grid; both certify that
    the `L_2` root, and hence `sdp_2` and `SDP1`, is inexact on an instance where `S*` is optimal.
- **`n = 40`, `p = 100`** (`rv_nested.py`, seeds 2000–2007).
  - `OPT = f(S*)` by enumeration in all 8.
  - My `SDP1` is within `2e-8` of `OPT` in all 8 (exact).
  - Perspective exact in 2 of 8 by PWE (seeds 2005, 2007). Seed 2006 is within `1e-6` but provably inexact (F9).
  - My `sdp_2` equals `OPT` within `1.4e-6` relative on seeds 2000, 2002 and 2006 (numerically exact, slightly above `OPT`).
    Seed 2002 is the run with 3 violators and a perspective gap of `0.35%`.
  - Seed 2002, `zb` (my vectorized model, SCS `eps = 1e-8`): `OPT + 1.4e-7` (exact).
    A Clarabel attempt at `p = 100` used over 20 GB and was stopped. The scalar and vectorized `zb` models agree to `3e-7` relative on 3 small instances.
- **`n = 40`, `p = 3200`**, restricted to `S*` and the top 60 nulls (`rv_nested.py`, seeds 2000, 2001, 2003, 2004).
  - My perspective and `SDP1` values match the stored ones to `1e-8`.
  - My `sdp_2` equals `f(S*)` within `1.2e-6` relative (exact up to solver accuracy).
  - On the **full** instance, my own Lemma 4.1(ii) bound gives `L_2 root - f(S*) = -0.0180, -0.910, -0.100, -0.0064`
    (`h = 1`, `eps2 = 0.33–0.40`), matching the note. It certifies inexactness wherever `S*` is optimal.
    Optimality of `S*` at `p = 3200` rests on the author's C1 decider, which I did not rerun.
- **Pure noise** (`rv_noise.py`; instances of Table 7.3 regenerated; `OPT` recomputed by full enumeration, which matched
  the stored `OPT` in all 7 runs; `zb` solved with my own model and Clarabel). Relative gaps `(OPT - zb)/OPT`, stored → mine:

  | `k` | `alpha` | seed | stored `zb` gap (solver) | my `zb` gap (Clarabel) |
  |---:|---:|---:|---:|---:|
  | 4 | 1 | 3000 | `4.4e-7` (SCS `1e-7`) | `-4.1e-8` |
  | 4 | 1 | 3002 | `8.05e-3` (SCS `1e-7`) | `8.05e-3` |
  | 5 | 1 | 3002 | `5.25e-3` | `5.25e-3` |
  | 5 | 2 | 3000 | `6.40e-3` | `6.40e-3` |
  | 5 | 2 | 3001 | `1.034e-2` | `1.034e-2` |
  | 6 | 1 | 3002 | `9.31e-4` (SCS `1e-6`) | `9.38e-4` |
  | 6 | 2 | 3002 | `-3.3e-5` (SCS `1e-6`; counted **exact**) | `+3.8e-5` (**unclear** band) |

  The `SDP1` gaps also match (for example `7.77e-2` at `k = 4`, seed 3002). So the `zb`
  inexactness at `k >= 4` is real, not a solver artifact. The last row shows that
  the SCS value overshot `OPT`. With Clarabel the run falls in the note's
  "unclear" band `(1e-6, 1e-4]`. See F9 and `rv_zbcheck.log`.
- **Table recount** (`rv_tables.py`, my own logic on the stored data).
  - Tables 7.1–7.3 match cell by cell, except the median-violator rounding (F5) and the perspective count at `p = 100` (F9).
  - `zb`: 41 exact, 28 inexact, 2 unclear, 71 runs.
  - The perspective-to-`zb` gap ratio has min 2.9, median 14.3 and max 403, as stated.

## Unchecked items

- The C1 decisions behind Table 7.4 (`SDP1` and `sdp_2` at the weakest failing nodes) and the "C1 fails for `L_2` (cert.)" column.
- `OPT = f(S*)` at `p = 3200` (the author's perspective C1 decider).
- The `p = 2560` enumerations.
- Equation numbering in the cited papers.
- The Dong–Chen–Linderoth duality statement ("by duality it equals the best diagonal split"), from memory.
- Anstreicher–Burer (F7), cited from memory.
- Dong's experiment sizes ("p = 64–512"; I read only his Section 3 text).
- Whether other literature (for example Bertsimas–Van Parys on phase transitions) contains random-design thresholds for these SDPs. Web search was unavailable to me beyond Crossref and the arXiv API.

## Commands (targeted checks only; no project-wide checks, CI not inspected)

From `reviews/stronger-relaxations/`:

- `python3 rv_small.py 6 > rv_small.log`
- `python3 rv_construction.py > rv_construction.log`
- `python3 rv_p1000.py > rv_p1000.log`
- `python3 rv_nested.py {p100|r3200} SEED` (jobs in `rv_nested_jobs.txt`, 4 workers) `> rv_nested.log`
- `python3 rv_noise.py k alpha seed >> rv_noise.log` (jobs in `rv_jobs2.txt`)
- `python3 rv_props.py > rv_props.log`
- `python3 rv_tables.py > rv_tables.log`
- `python3 rv_zbcheck.py > rv_zbcheck.log` (the disputed pure-noise run)
- `python3 rv_dong.py > rv_dong.log` (revision check: Dong's exact `SDP1` test)
- `SDP2=1 python3 rv_nested.py p100 2002` and `ZB=1 ZBSOLVER=SCS python3 rv_nested.py p100 2002` (appended to `rv_nested.log`)

*CPU note.* In my first launches, `rv_construction.py` (about 1 min), `rv_p1000.py` (about 1 min) and a
first batch of `rv_nested.py` (4 processes, about 2 min, up to about 6 threads each)
imported NumPy before the thread pin took effect. I killed the batch, moved
the pin to the top of every script, and regenerated all logs single-threaded.
I also stopped a Clarabel `zb` solve at `p = 100` (over 20 GB) and used SCS for it instead.

## Check of the revision (note as of 07:42, 2026-09-29)

I re-read every revised passage against the findings above.

| Finding | Status in the revised note |
|---|---|
| F1 `OptPairs` | **Fixed correctly** (Summary, Section 1.2, Lemma 1.2(d) now with `Q_T ⪰ 0`, Corollary 4.6, Sections 7.3, 8). |
| F2 and F7 framing, positioning | **Fixed correctly.** I checked the new "Where `zb` sits" paragraph: generating-point identity, closedness of the cone, stability under PSD recession, and the level-2 minor. The Remark 4.5 addition is right: `E[zeta_j beta_m] = 0` for `z_m = 0` follows from the product cone and `Z_jm <= z_m`. |
| F3 conventions | **Fixed correctly.** The weakened hypothesis of Theorem 4.4 (`R >= g` at every node; `R <= L_r` only at the root and at `(∅, {j})`) is sufficient. (a) and (c) need only `R >= g`: every off-path node `v` has `R(v) >= g(v) >=` the perspective bound of its single wrong fixing, because the perspective bounds are monotone. (b) and (d) use only those nodes, where no column is fixed to zero. An optional addition: for `r <= k`, the construction also lies in the node-level exact hulls with `zeta_j = 1`, so those solvers are covered too. |
| F4 | **Fixed correctly.** The uniform formula matches. The heuristic reading is labeled. |
| F5 | **Fixed correctly.** The new statement that the absolute shift `4 eps_p log p` vanishes only if `r n log^3 p = o(p)` is right. Section 2's first-order converse along the failure direction follows from the Corollary 5.2 computation with `lam' = lam(1+c)`. |
| F6 | **Fixed, with one new overreach (R1).** |
| F8 | Fixed. |
| F9 | **Partly fixed.** The perspective count (2 of 8) and the Dong-based `SDP1` decisions are fixed. My own implementation of Dong's test (`rv_dong.py`) agrees with the solver rule on all 53 nested rows (32 at `n = 20`, 21 at `n = 40`), as the revision reports. I did not rerun the 20 `cmp` rows. **Still open:** Table 7.3 still counts `k = 6`, `alpha = 2`, seed 3002 as `zb`-exact, and the text still says "41 of 71 ... unclear in 2". The two solvers disagree in sign at `|gap| ≈ 3.5e-5`, and Clarabel reports `optimal_inaccurate`. The row should read 1 exact, 2 inexact, 1 unclear, and the totals 40, 28 and 3 (Summary, Section 7.4). |

**R1 (Section 6.3, new text).** "So when `log k = o(log p)`, the constant 2 is
optimal for every polynomial relaxation, conditionally on the low-degree
conjecture ... the recovery conjecture is not needed." BAHSWZ's theorem is
stated for fixed `theta in (0, 1)`, so `log k = o(log p)` (`theta = 0`) lies
outside it. What their result supports is a limit statement. For every
`delta > 0` there is `gamma_0 > 0` such that, for each fixed
`gamma in (0, gamma_0)`, degree-`o(k)` polynomials fail to detect below
`alpha = 2 - delta`. By Arpino's reduction, and conditionally on the
low-degree conjecture, no polynomial-time algorithm then achieves
approximate recovery there. A root-exact relaxation with a unique optimum
is such an algorithm. The binary-signal and `sigma^2 = o(k)` caveats of
Section 6.1 still apply. My F6 suggested this strengthening without the
regime qualifier; the note should state it as the `gamma -> 0` limit.
