# Recheck of the revised "Do stronger convexifications move the sparse-regression thresholds?"

Reviewed file:
[`../bb-complexity/sparse-regression/stronger-relaxations/thresholds.md`](../bb-complexity/sparse-regression/stronger-relaxations/thresholds.md)
(cited as [SR]), revised after
[`stronger-relaxations-review.md`](stronger-relaxations-review.md) (cited as
the review). Scope: the six items listed in the request, all tied to the
"Revision after review" section. Reviewer: fresh independent reviewer
(convex relaxations, high-dimensional probability); I had not seen this
material before. Date: 2026-09-29. I did not edit the note and did not commit.

My scripts and logs are in
[`stronger-relaxations-recheck/`](stronger-relaxations-recheck/). They use my
own cvxpy models, my own copies of the two instance generators (same RNG call
order as `exp_mech.make` and `core.instance`), and my own implementation of
the `SDP1` certificate test. They import nothing from the author's code or the
first review's code; they only read the stored `data/*.jsonl` files.

## Verdicts

| Item | Verdict |
|---|---|
| (1) Weakened hypothesis of Theorem 4.4 (`R <= L_r` only at the root and at the forced-in nodes `(∅, {j})`) | **Correct.** Part (b) uses only the root and part (d) only the nodes `(∅, {j})`; parts (a), (c), (e) use only `R >= g`. At these nodes `S0 = ∅`, so column deletion changes nothing. The exact hull of the node's own set also equals `L_r` there; I checked this analytically and numerically (R3). The node convention after Definition 1.1 is consistent with the theorem and with Corollary 4.6. Two wording slips remain (R2, R3), and one step of (c) needs a clause (N1). |
| (2) Replacing `OptPairs` by free-sign 2×2 decompositions (Wei et al., Proposition 2); Lemma 1.2(d) with `Q_T ⪰ 0` | **Correct.** Proposition 2 of arXiv 2201.00387 is the free-sign hull, as stated (checked in the source). `OptPairs` in arXiv 2004.07448 carries `y >= 0` (checked in the source). Lemma 1.2(d) holds pointwise in `(z, beta)`, so it also covers optimal-decomposition SDPs. Numerically, the Wei et al. value equals my `H_T`-based envelope to `3e-10`, and it is `<= L_2 <= OPT` at 10 of 10 nodes. |
| (3) Reframing "beyond the `(z, beta, beta beta')` lift"; the product cone as a 2×2 minor of the level-2 moment matrix, implied by the exact 2×2 hull of the full lift | **The two facts are correct**, and my numerical checks confirm both. **The conclusion drawn from them is imprecise (R1).** Pairwise full-lift hulls do not defeat the Section 4 construction by themselves. The construction extends to them unless the lifted products `U = E[zeta beta']` also sit in the PSD constraint on the full moment matrix of `(1, zeta, beta)`. "Escaped by lifting the cross products, not by non-locality" and "already `r = 2` escapes" need that qualifier. |
| (4) Corrected F4 statement (about `4 sqrt(s/n)` only for supports independent of `X`; uniformly of order `sqrt(s log(ep/s)/n)`) | **Correct.** The note gives only the union-bound upper bound. The "small only when" and "`Theta(1)`" parts also need a lower bound. A data-dependent support provides one of the same order, as computed below (R6, minor). |
| (5) Attribution to Bandeira–El Alaoui–Hopkins–Schramm–Wein–Zadik (BAHSWZ) | **Accurate against the arXiv source of 2205.09727** (Section 3.2, Theorem `thm:sparse-reg`, the remark "Implications for recovery"). `R_LD` converts exactly to `alpha = 2(1 - sqrt gamma)^2` (`gamma < 1/4`) and `1 - 2 gamma` (`1/4 <= gamma < 1/2`). The approximate-recovery conjecture, the thresholding result, the Arpino reduction and the authors' disclaimer are all stated correctly. The `gamma -> 0` conclusion needs two more caveats, and one parenthetical has a small attribution slip (R4). |
| (6) F9 corrections | **Correct.** Perspective root exact in **2 of 8** at `n = 40`, `p = 100` by the PWE ratio (seed 2006: ratio `1.00181`, solver gap `1.88e-7`). All other perspective cells of Tables 7.1, 7.2 and 7.4 match. My own certificate test agrees with `dong_check.py` and with the solver rule on **73 of 73** rows. Two sentences are slightly inaccurate (R5). |

Overall: the revision fixes what the review asked for, and the weakened
Theorem 4.4 is correct as stated. One point of substance remains (R1). It
concerns scope and framing, not the theorems: the frontier that Section 5
identifies is "lifted products **inside** the global PSD matrix", not
"pairwise hulls of the full lift".

## Problems

**R1 (item 3; framing, moderate).** The pairwise full-lift hulls do not by
themselves escape the Section 4 obstruction. Take the Lemma 4.1 point
`(z, beta, B)` and complete it in the full lift with `Z, U` taken from the
random-support mixture on `F`, and `Z_jm = U_jm = U_mj = 0` for helpers `m`.
Call this point P2.

- For every pair `T`, the mixture restricted to `T` is a genuine distribution. The remainder `B_T - E[xi xi']_T` is a PSD recession term of the `(1,1)` pattern with weight 0. Lemma 4.1 proves exactly that this remainder is PSD. So P2 lies in the exact 2×2 hull of the full lift for **every** pair, and it satisfies all product cones and McCormick inequalities.
- The PSD constraint on `[[1, beta'], [beta, B]]` holds, and `Phi` is unchanged.
- The same argument with Lemma 4.1(i) handles `r`-sets. So Theorem 4.4's proof also covers `r`-wise hulls of the full lift combined with PSD only on `(1, beta, B)`.

What P2 violates is the PSD constraint on the full moment matrix
`Y = [[1, z', beta'], [z, Z, U], [beta, U', B]]`. Remark 4.5's completion
(point P1) satisfies that PSD constraint but violates the product cones.
`rc_fulllift.py` (`n = 6`, `p = 40`) shows:

- P2: every one of the 780 pair remainders is PSD (smallest eigenvalue `-6e-31`); `[[1, beta'], [beta, B]] ⪰ 0`; product-cone violation 0; `lambda_min(Y) = -4.9e-2`.
- P1: `lambda_min(Y) = -1.9e-10`; product-cone violation `6.5e-4`.

Proposition 5.1's proof uses both ingredients: `U_jm = 0` from the cone, then
Gram vectors of the full `Y`. Section 5 ("uses the global PSD constraint and
pairwise constraints only") is therefore accurate. The Summary ("escaped by
lifting the cross products `zeta_j beta_m`, not by non-locality"; "already
`r = 2` escapes its obstruction") and Remark 4.5 ("Proposition 5.1 shows that
already `r = 2` escapes") are not. **Suggested fix:** "escaped by lifting the
products `zeta_j beta_m` into the PSD moment matrix of `(1, zeta, beta)`.
Pairwise hulls of the full lift with PSD only on `(1, beta, B)` are still
defeated by the construction." Also state that the relaxation meant by "`r`-wise hulls in
the full lift" in Remark 4.5 and Section 9.1 includes the PSD constraint on the full moment
matrix. Section 6.3's necessary condition ("must lift the products ... or use
global constraints") remains true.

**R2 (item 1; wording).** In the Summary's "Mechanism", the line "at every node
`R <= ||y - X beta||^2 + lam ||beta||^2 + lam (1 + eps_p) pi`" reuses `R`. The
Summary has just defined `R` as any relaxation bounded by `L_r` only at the root
and forced-in nodes. The bound is proved for `L_r`, `L_2` and `SDP1` in the
root-lifted node convention, at nodes containing `z` (Lemma 4.1, Corollary
4.3). It is not proved for a column-deleting `R` at nodes with `S0 ≠ ∅`. Replace `R` by
`L_r` (root-lifted convention).

**R3 (item 1; minor).**

- The node-convention paragraph puts "solvers that delete fixed-to-zero columns, or the exact hull of the node's own feasible set" under one alternative convention and says that Theorem 4.4 does not depend on the choice. At a forced-in node, the face `H_T ∩ {z_j = 1}` equals the closed hull of the generating points with `zeta_j = 1`. Any vanishing weight on `zeta_j = 0` points contributes only a PSD recession term with zero row `j`, and points with `zeta_j = 1` generate that term too (Lemma 1.2(b)). So the node's own hull coincides with `L_r(∅, {j})`, provided the cardinality constraint is dropped inside `H_T` or `r <= k`. For `r > k`, the node's own cardinality-constrained hull is stronger (the note's own first convention). One clause would make this explicit.
- The Summary's sentence on Corollary 4.6 omits the node-convention caveat that the corollary now states.

**R4 (item 5; minor).** In Section 6.3 and the Summary: "when `log k = o(log p)` [as
`gamma -> 0`], the constant 2 is optimal for every polynomial relaxation,
conditionally on the low-degree conjecture".

- BAHSWZ's theorem is for fixed `theta in (0,1)`. The correct form is a limit: for every `alpha < 2` there is `gamma_0 > 0` with `2(1 - sqrt gamma)^2 > alpha` for all fixed `gamma < gamma_0`. The regime `log k = o(log p)` itself is not covered.
- The conclusion also rests on the model transfer that Section 6.1 calls heuristic (binary versus `±b` signals, BAHSWZ's normalization with `sigma^2 = o(k)`). Section 6.3 and the Summary drop that caveat. Add "and on the heuristic model transfer of Section 6.1".
- *Nit.* In the Summary, "(thresholding works there)" is BAHSWZ's own theorem (their approximate-recovery section), not part of "the literature summarized by BAHSWZ".

**R5 (item 6; minor).**

- Section 7 says: "Two stored `zb` values exceed `OPT` by `3.0e-6` and `3.3e-5` ..., and one `sdp_2` value by `1.5e-6`". `rc_exceed.py` finds six stored values above `OPT` by more than `1e-6` relative. They are `zb` `3.3e-5` and `3.0e-6` (Table 7.3), `sdp_2` `2.0e-6` (cmp, `alpha = 1.5`, seed 1006), `zb` `1.9e-6` (cmp, `alpha = 2`, seed 1000), `sdp_2` `1.5e-6` (`n = 40`, `p = 100`, seed 2005) and `sdp_2` `1.3e-6` (cmp, `alpha = 1.5`, seed 1004). The conclusion ("about `1e-5` relative"; qualitative results unchanged) stands. The list should be complete, or should say "for example".
- "It agrees with the solver rule ... on all 73 rows where `SDP1` was solved" should say "on all 73 rows of Tables 7.1, 7.2 and 7.4". `SDP1` was also solved on the 71 rows of Table 7.3, which were not checked by the certificate. There the smallest gap is `1.6e-2`, so the solver rule is safe.
- One of the 73 agreements is close to the threshold: cmp, `alpha = 2`, seed 1007 has solver gap `1.07e-6` against the `1e-6` rule. The certificate is clearly negative there (scaled `max_t h = -1.5e-4`), so the classification "inexact" is right.

**R6 (item 4; minor).**

- The union-bound expression `4 (sqrt s + sqrt(2 s log(ep/s)))/sqrt n` is an upper bound on the worst case, not an estimate of it. "Small only when `s log(ep/s) = o(n)`" and "`Theta(1)` at `s ≈ k`, `n ≈ 2k log p`" also need a lower bound. A lower bound of the same order is easy. Take a column `j0` together with the `s - 1` columns most correlated with it. This gives `X_A'X_A ≈ n I` plus an arrow with entries of size `sqrt(2 n log(p/s))`, so the fraction is at least about `2 sqrt(2 (s-1) log(p/s)/n)`.
- `rc_frac.py` gives, at `n = 2000`, `p = 10^4`, `s = 2, 5, 10, 20`: fixed `A` 0.05, 0.15, 0.22, 0.31; data-dependent `A` 0.17, 0.32, 0.41, 0.50.
- At `s = k`, `n = round(2k log p)`, `p = 20000`, `k = 5`–40: fixed `A` 0.47–0.58; data-dependent `A` about 0.80 in every case, so `Theta(1)`.
- `4 sqrt(s/n)` is the large-`s` edge asymptotic. For small `s` it overestimates, for example 0.126 against an observed 0.053 at `s = 2`. "About" covers this.
- The Summary writes `log(p/s)` and Section 5 writes `log(ep/s)`. The difference is harmless.

**N1 (item 1; exposition nit).** Theorem 4.4(c) cites PT Lemma 1.2, whose proof
uses monotone node bounds ("adding fixings shrinks the feasible set"). A
general `R` under the new hypothesis need not be monotone. The conclusion still
holds: for an off-path node `v`, `R(v) >= g(v) >= g`-bound of its single wrong
fixing `> OPT` by PT 3.2(a). The best-bound variant also uses validity of `R`
(path nodes have bound `<= OPT`), which "relaxation" implies. The proof of (a), (c)
("the `R` bounds are at least the perspective bounds at every node") contains
the idea. One clause in (c) would close the gap.

## Details

### (1) Theorem 4.4 with the weakened hypothesis

I traced every use of `R` in the proof.

- *(a), (c).* These use only `R >= min_z g` at the relevant nodes, and validity at the root (`R <= L_r(∅,∅) <= f(S*)`). For (c), see N1.
- *(b).* This uses `R(∅,∅) <= L_r(∅,∅) <= P_ebar(z, beta)` (Corollary 4.3). Here `z` is in the root, the helper half `H1` is disjoint from `F = S* ∪ {l}`, and nothing is fixed. So only the root is used.
- *(d).* This uses `R(∅,{j}) <= L_r(∅,{j}) <= P_ebar(z, beta)` for the point of Lemma 2.5′. That point has `z_j = 1`, `F = S ∪ V' ∪ {j}`, helpers in the other half, and `S0 = ∅`. The failure of C1 needs only one forced-in node with bound `< OPT`. So only forced-in nodes are used.
- *(e)* follows from (a)–(d). The `SDP1` sentence rests on Proposition 3.1, which is separate.
- *Lemma 4.1* is stated "for every node containing `z`" under the root-lifted convention. At the root and at `(∅, {j})` no column is fixed. So column deletion gives the same relaxation there, and the parenthetical "solvers that delete fixed-to-zero columns are covered" is right.

*Node convention* (`rc_node.py`, 6 instances with `n = 5`, `p = 8`, `k = 2`, my disjunctive `L_2`):

- (A) At the forced-in node, "root hulls + `z_j = 1`" and "hull of the node's own set" (patterns with `zeta_j = 0` removed on pairs containing `j`) agree to `3.9e-7` relative, which is Clarabel's accuracy on these runs.
- (B) At the removal node `({m}, ∅)`, the root-hull value is at most the column-deleted value and is strictly smaller in 4 of 6 instances, by up to `8.8e-3` relative. So `m` does act as a helper, as the convention paragraph says.
- (C) No value exceeds the node's enumerated optimum by more than `3.9e-7` relative.

Corollary 4.6's statement now carries the convention and says that
column-deleting implementations are not covered. That is consistent with (B).

### (2) Free-sign 2×2 decompositions and Lemma 1.2(d)

- *Sources* (arXiv LaTeX, downloaded and read, then deleted).
  - Wei–Atamtürk–Gómez–Küçükyavuz, `prop:2x2extended`: `clconv` of `{t >= d1 x1^2 - 2 x1 x2 + d2 x2^2, x ∘ (1 - z) = 0}` with free `x` and `d1 d2 > 1`, which covers every strictly convex 2×2 form after scaling and a sign flip. The rank-one case is Atamtürk–Gómez. Their text also says that Frangioni–Gentile–Hungerford's bounded disjunctive formulation "can be easily adapted to the case with no bounds", as the note states.
  - Han–Gómez–Atamtürk: `OptPairs` (`\sdppos`) has `y >= 0` in every formulation. Their Theorem 1 (`thm:equivalence`) is Shor = OptPersp for their problem `(QI)`.
- *Lemma 1.2(d).* For an `L_2`-feasible `(z, beta, B)` and any decomposition, `beta'R beta <= <R, B>` and `f_{Q_T}(z_T, beta_T) <= <Q_T, B_T>`. Because this holds pointwise, the bound also covers "max over decompositions" SDPs. `Q_T ⪰ 0` is needed for the envelope to be meaningful; the inequality itself does not use it. The nesting claims in the Summary, Section 1.2, Section 8 and Corollary 4.6 are consistent with this.
- *Numerics* (`rc_decomp.py`: 5 instances with `n = 5`, `p = 7`, `k = 2`, every pair used; root and one forced-in node).
  - Wei et al.'s formula, after my scaling, equals my disjunctive `H_T` envelope to `3.1e-10` relative, so I read Proposition 2 correctly.
  - `V_W <= L_2 <= OPT` holds in all 10 cases (largest violation `1.5e-8`, which is solver accuracy).
  - In 3 of 5 instances the free-sign optimum has `beta_a beta_b < 0`. It therefore lies outside every nonnegative lifted hull, where `B >= 0` entrywise. This is a concrete example of why `OptPairs` is invalid here.

### (3) Product cones, the full lift and the level-2 moment matrix

- *Implied by the full-lift 2×2 hull.* At generating points `(zeta_j b_m)^2 = zeta_j zeta_m b_m^2`, and the cone is closed and convex. `rc_moment.py` (b) goes further: over my disjunctive full-lift pair hull with `z`, `Z_ab` and `B_bb` fixed, `max U_ab = sqrt(Z_ab B_bb)` to 9 digits (three cases, including `Z_ab = 0 ⇒ U_ab = 0`). So for these data the cone is the exact projection of the pair hull onto the coordinates `(U_ab, Z_ab, B_bb)`.
- *Level-2 minor.* On random finite distributions satisfying `beta_m (1 - zeta_m) = 0`, the raw degree-4 moments satisfy `E[(zeta_j zeta_m)^2] = Z_jm` and `E[zeta_j zeta_m beta_m] = U_jm` exactly, and the 2×2 minor is PSD (`rc_moment.py` (a)). The Summary's "2×2 principal minors of the level-2 moment matrix" is correct with the ideal reduction that Section 5 states.
- *Scope.* See R1.

### (4) Proposition 5.3's fraction

The corrected statements in the Summary, after Proposition 5.3, and in Question
5.4 are right. See R6 for the missing lower bound and the numbers.

### (5) BAHSWZ (arXiv 2205.09727, read in the LaTeX source)

- Their Definition: `n` features, `m` samples, binary `u`, `Y = (k + sigma^2)^{-1/2}(Xu + W)`, `sigma^2 = o(k)`, and `m = R k log(n/k) = R(1 - theta) k log n`. So `alpha = R(1 - gamma)`.
- `R_LD = 2(1 - sqrt theta)/(1 + sqrt theta)` for `theta < 1/4` converts to `alpha = 2(1 - sqrt gamma)^2`. `R_LD = (1 - 2 theta)/(1 - theta)` for `1/4 <= theta < 1/2` converts to `alpha = 1 - 2 gamma`. Both conversions are exact.
- Part (a) is "no degree-`o(k)` polynomial weakly separates"; part (b) gives a polynomial-time strong detector above the threshold.
- "This line of work suggests the presence of a possible-but-hard regime for approximate recovery when `0 < R < 2`" matches the note's attribution. "Polynomial-time reduction from strong detection to approximate recovery [Arpino, MSc thesis, ETH 2021]" matches the note's "Arpino's reduction" and its direction.
- "For larger values of `theta` ... our lower bound ... does not suggest a sharp recovery lower bound" matches the note.
- `lim_{theta -> 0} R_LD = 2`, "essentially tight", matches.
- See R4 for the remaining caveats.

### (6) Computations

`rc_pwe_dong.py` regenerates every stored row of Tables 7.1, 7.2 and 7.4.

- It reproduces `lam` and `f(S*)` (to `1e-9` relative) and the stored PWE ratio (identical).
- It recounts the perspective-exact cells: n20 1, 0, 0, 0, 0, 0, 0; n40 2, 1, 0, 0, 0, 0; cmp 0, 0, 0. All match the tables. The only row where the PWE rule and the `1e-6` rule disagree is seed 2006 at `n = 40`, `p = 100`.
- My `SDP1` test maximizes the concave function `h(t) = lambda_min(Q - diag(mu(t)))`, with `mu_i = t/b_i^2` on `T` and `a_l^2/t` off `T`. This is a different parametrization and optimizer from `dong_check.py`. It agrees with `dong_check.py` and with the solver rule on 32/32, 21/21 and 20/20 rows. On the five near-threshold rows printed in the log, the stored `dong_minf` equals minus my `max h` to about three digits. `SDP1`-exact counts: 3, 0, 0, 0 (n20); 8, 6, 0 (n40); 0, 1, 3 (cmp). All match.

## Commands (targeted checks only; no project-wide checks; CI not inspected)

Run from `reviews/stronger-relaxations-recheck/`. Every script pins
BLAS/OpenMP/Rayon threads to 1 before importing NumPy. At most 3 processes ran
at once.

- `python3 rc_pwe_dong.py > rc_pwe_dong.log` (37 s)
- `python3 rc_node.py > rc_node.log` (9 s)
- `python3 rc_decomp.py > rc_decomp.log` (7 s)
- `python3 rc_moment.py > rc_moment.log` (1 s)
- `python3 rc_fulllift.py > rc_fulllift.log` (1 s)
- `python3 rc_frac.py > rc_frac.log` (4 s)
- `python3 rc_exceed.py > rc_exceed.log` (under 1 s)

Literature: I downloaded the arXiv sources of 2205.09727, 2201.00387 and
2004.07448 with `curl`, read the sections cited above, and deleted the files
afterwards.

## Not rechecked

- Parts of the note outside the six items, which the first review covers: Lemma 4.2, Corollary 4.3 constants, Proposition 3.1, and the `p = 3200` and `p = 1000` certificates.
- Anstreicher–Burer (2021), which the note cites from memory.
- Whether Arpino's reduction transfers to the note's `±b` model.
