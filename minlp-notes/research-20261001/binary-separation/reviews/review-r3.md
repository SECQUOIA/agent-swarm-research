# Review r3 of the binary-separation note (third round)

Date: 2026-10-03. Reviewer: an independent research agent (adversarial review, not
journal peer review). Object: [`note.md`](../note.md) after the second revision, with
`code/`, `logs/` and `sources/`. My scripts and outputs are in [`r3-work/`](r3-work/).
My code does not import the stream's code. An earlier round-3 reviewer was stopped by a
usage limit and left `r3-work/independent_check_r3.py` (partial, never run to the end)
and an empty `r3-work/independent_check_r3.log`. I did not use or rely on that script;
all round-3 results below come from `r3-work/r3_checks.py` and the reruns listed at the
end.

## Verdict

**Minor fixes.**

The round-2 major issue (R2-M1) is fixed correctly in all places it was raised. The new
material is correct:

- Lemma 6 (switching on one variable, including the shift `s ↦ s − v_g`);
- Corollary 9 (Padberg's clique inequalities (10) are strongly NP-complete to separate,
  at positive definite points with denominators dividing `4N`);
- the remark after Corollary 9 (which clique inequalities map to (18));
- Corollary 10 (odd clique, pure hypermetric and Barahona–Mahjoub clique inequalities
  (18), at points in the interior of the elliptope and in the metric polytope, with
  denominators dividing `8qN`).

I checked every proof step by hand and every quantitative claim by exact computation.
All size bounds are polynomial, so the hardness is strong as claimed. The definitions
used match Letchford (2022), (10)–(13), (18), (19), Definition 2 and Theorem 1, and
GKL (2012), §2 (odd clique). I found one wrong number (§9 states the maximum violation at
the points of Corollary 10 as `(q + 2)/(4qN)`, which holds only for (18) after the
switching) and stale review-status sentences. Neither affects a theorem.

## Issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| R3-m1 | minor | §9, third bullet ("At the points of Corollary 10 it is `(q + 2)/(4q(8n + 2p + 1))` in the cut scale") | The sentence continues "the maximum violation at the points of Corollary 3 is exactly ...", so it states a maximum. That is true only for (18) at `d″`. At `εd̃` the largest violated odd clique (equivalently pure hypermetric) inequality is not `b*`. By Corollary 10(a), a pure violator needs `w ∈ {0, ±1}^m` and root coefficient `2 − q − Σw ∈ {0, ±1}`; with `a` entries `+1` and `k` entries `−1`, this forces `a = 0` and `k ∈ {q − 3, q − 2}`. So the pure violators are `b*` (`k = q − 2`, root 0) and the `m` vectors `(−1, 𝟙_C, −1, −𝟙_m + e_j)` (`k = q − 3`, root `−1`), violated by `ε(1/2 − 2(q − 3)τ²) = (q + 3)/(4qN)`. The largest violated hypermetric (and rounded psd) inequality at `εd̃` has `w ∈ {0, 1}^m` and violation `1/(2N)`. My exact check [D] confirms both maxima on every yes-instance (for example `q = 4`: `4qN·max = 7`, `2N·max = 1`). | Say that the maximum violation is `(q + 2)/(4qN)` for (18) at `d″`, and `(q + 3)/(4qN)` for odd clique and pure hypermetric inequalities at `εd̃` (both still of order `1/(n + p)`, so the Summary sentence "of order `1/(n + p)`" stays true). Optionally list the pure violators in Corollary 10(c) as above; (c) as written ("`b*` gives such an inequality") is correct. |
| R3-m2 | minor | Header (lines 14–16), §8 paragraph after the quoted text, Limits first bullet, §10 intro | These say that Lemma 6 and Corollaries 9 and 10 "have not been re-reviewed" and that Corollary 10 "has only the author's proof and exact checks". After this round that is out of date. | Update the status sentences to cite this review (round 3: Lemma 6, Corollaries 9 and 10 checked; independent exact checks in `reviews/r3-work/`). |
| R3-o1 | optional | §8 quoted paragraph | "Switching the hard points on one variable turns them into facet-defining clique inequalities" says that the points become inequalities. "Replacing the root of the hard instance by several nearby points" describes Corollary 10 loosely: the root stays and `q − 2` points are added near it. | For example: "Switching the hard points on one variable turns the violated cut inequalities into facet-defining clique inequalities" and "adding `q − 2` points close to the root, which keeps the Gram matrix positive definite, ...". |
| R3-o2 | optional | Corollary 10(d), Summary item 3 | Some authors state the Barahona–Mahjoub clique inequalities for every `S`, with right-hand side `⌊|S|²/4⌋`; Letchford (2022, (18)) restricts to odd `|S|`. The even-`|S|` members are psd inequalities (`σ` even), which hold strictly at the interior points `d″`, so the hardness statement holds under either definition. | One sentence would make the statement independent of the convention. |

No major issues.

## Status of round-2 items

| Item | Status | Evidence |
|---|---|---|
| R2-M1 (Padberg clique (10) called open; (18) "cut images") | **Fixed.** | Corollary 9 states and proves the result; it is correct (below and check [B]). The six places listed in review r2 now say the right thing: remarks after Corollary 8 (first bullet), §7 Letchford bullet, §8 paragraph, Limits, Open questions (old 3 and 4 removed, with a pointer to Corollaries 9 and 10), Summary item 3. A grep for "remain(s) open", "still open", "unknown" and "cut images" finds only literature quotations, historical correction lists and the gap-inequality question. The "cut images" sentence is replaced by the remark after Corollary 9, which is correct (check [C]). The (18) result for repeated points from review r2 is credited in the remarks after Corollary 10 and superseded by Corollary 10(d). |
| o1 (shift of `s` attributed to Letchford p. 9) | Adopted correctly. | Lemma 6(ii) proves it; Letchford p. 9 indeed states only "change the sign of `vᵢ`". |
| o2 (Dey et al. "no complexity statement") | Adopted correctly. | §2 table and §7. |
| o3 (`s` bounded) | Adopted correctly. | Closed form after Lemma 5; `code/closed_form_s.py` rerun, output identical to the log. |
| o4 (Letchford's facet condition for (11)) | Adopted, with the caveat that Padberg 1989 was not read. | Remarks after Corollary 8. |
| o5 (odd clique vs pure hypermetric) | Adopted correctly. | Summary item 3 lists them separately. |

## Detailed check of the new material

### Lemma 6

- (i) Row `g` of `A` is `e₀ − e_g`, so `(AXAᵀ)_gg = X₀₀ − 2X₀g + X_gg = 1 − x_g`,
  `(AXAᵀ)₀g = 1 − x_g`, `(AXAᵀ)ᵢg = xᵢ − y_ig`, and all other entries are unchanged. This
  is the moment matrix of Letchford's switching `ψ_{{g}}` (Definition 2, pp. 6–7; for a
  one-element set the third bullet of the definition is void). `A² = I`, so `A` is
  invertible and positive definiteness is preserved.
- (ii) With `û = (−s, v)`, `ûᵀXû` is the linearization of `(vᵀx − s)²` and
  `e₀ᵀXû = vᵀx − s`, so `h_X(v, s)` is exactly RHS − LHS of (13) (not halved).
  `Aᵀû = û + v_g(e₀ − 2e_g) = (−(s − v_g), v′)` and `e₀ᵀA = e₀ᵀ`. Correct.
- (iii) and (iv): correct; the `(S, T, s)` correspondence is the right one for (12) as
  printed on p. 9, and the cut image switches exactly the edges `0g` and `ig`.
- Checks: [A] on 300 random rational points (not psd), including (iii) evaluated with
  the printed formula (12) and (iv); [A′] the identity (ii) symbolically (SymPy) for
  generic `x, y, v, s` with four variables.

### Corollary 9

- (a) `x′_g = 1 − εM_gg = 1 − (2p − 1)/(4N)`, `y′_ig = ε(Mᵢᵢ − M_ig) = (4 + |Sᵢ|/2)/N`
  (`22/(4N)` for X3C). `A` is integral, so `4N·A X Aᵀ` is integral; all entries are in
  `[0, 1]`. Correct.
- (b) Dictionary: split `(s, −v)`. Corollary 3(d) gives the violated splits
  `(0, −x, 1)` and `(−1, x, −1)`, that is the Boros–Hammer data `(𝟙_C − e_g, 0)` and
  `(e_g − 𝟙_C, −1)` with slack `−1/(2N)`. Solving Lemma 6(ii) gives
  `(𝟙_C + e_g, 1)` and `(−𝟙_C − e_g, −2)`, which are the same inequality. (10) with data
  `(S, s)` is half of (13) with `v = 𝟙_S` (I re-expanded it), so the only violated (10)
  is `S′ = C ∪ {g}`, `s′ = 1`, violated by `1/(4N)`; `s′ = 1` lies in `0, …, |S′| − 1`.
  Correct, and the argument is complete, because Corollary 3(d) lists all violated
  splits over all integers.
- (c) The violators have support `q + 1`; the Boolean quadric triangle family consists
  of members of (12) with `|S| + |T| ≤ 3`. Correct for `q ≥ 3`.
- (d) `|S′| = q + 1 ≥ 3`, `1 ≤ 1 ≤ q − 1`: Padberg's condition as printed on p. 8.
  Correct.
- (e) Cut switching is the congruence `Z ↦ ΣZΣ`; it preserves the elliptope interior,
  the metric polytope and the gonality of rounded psd inequalities. Correct.
- NP membership and strong hardness: correct (entries bounded by `4N`).
- Check [B]: 40 X3C instances (`q ∈ {3, 4}`, 27 with a cover, some with two covers).
  Complete enumeration of all violated Boros–Hammer data at `P′` (my own Fincke–Pohst
  over `(û − e₀/2)ᵀX(û − e₀/2) < 1/4`), all (10) and all (12) evaluated with the printed
  formulas, the triangle family, the cut image, and a complete enumeration of all
  violated rounded psd inequalities of the cut image in cut space (gonality `2q − 1`
  only). 0 failures.

### Remark after Corollary 9

Expanding with `tᵢ = 1 − 2xᵢ`, `t₀ = 1` gives
`(vᵀx − s)(vᵀx − s − 1) = ((b̂ᵀt)² − 1)/4` with `b̂ = (2s + 1 − σ(v), v)`, so the cut
image of (10) is the rounded psd inequality of `±(2s + 1 − |S|, 𝟙_S)`, as stated. The
conditions for (18) (on `S` for odd `|S|`, on `S ∪ {0}` for even `|S|`) and for odd
clique (`|2s + 1 − |S|| ≤ 1`) are correct, and so is the conclusion that the violators of
Corollary 9 have root coefficient of absolute value `q − 2`. Check [C]: 300 random points.

### Corollary 10

- The explicit `d̃` follows from `d(M̃)`: `d̃(0, oⱼ) = τ²`, `d̃(oⱼ, oₖ) = 2τ²`,
  `d̃(oⱼ, u) = M_uu + τ²`. The `ℓ₂²` picture is right.
- (a) `g_M̃(z, w) = g_M(z) + τ²Σwⱼ(wⱼ − 1)`; the second term is a nonnegative multiple of
  `τ²`, so violators need `g_M(z) = −1/2` and `Σw(w − 1) < 1/(2τ²) = 4q`. The gonality
  bound uses `|2 − q − Σw| + |Σw| ≥ q − 2`. Correct.
- (b) `s̃ = s + mτ²` (block-diagonal `M̃`), `εmτ² = (q − 2)/(8qN) < 1/(8N)`, so
  `εs̃ < 1/2 + 1/(8N) < 3/4`; the Schur complement gives `X̃ − θe₀e₀ᵀ ≻ 0` for
  `θ ∈ {0, 1/4}`. The entries of `εM` have denominators dividing `4N` and
  `ετ² = 1/(8qN)`, so `8qN·X̃` is integral with entries at most `8qN`, polynomial in
  `n + p`. The congruence `J − 2εD̃ = LX̃Lᵀ` needs only `X̃ᵢᵢ = X̃₀ᵢ`, which holds. The
  `|σ| ≥ 3` argument and the gonality statement are correct.
- (c) `b* = (0, 𝟙_C, −1, −𝟙_m)` has `σ = 1`, `Σw(w − 1) = 2(q − 2) < 4q`, and
  `Q(b*, d̃) = 1/2 − 2(q − 2)/(8q) = (q + 2)/(4q)`. The converse direction (violated odd
  clique ⇒ rounded psd with `σ = ±1` ⇒ hypermetric ⇒ cover) is correct. GKL (2012, §2)
  define odd clique inequalities by `b ∈ {0, ±1}ⁿ`, `σ(b)` odd; these are exactly the
  switchings of (18), since a `{0, ±1}` vector with odd `σ` has odd support. So
  "odd clique in cut form = (18) and their switchings" is right.
- (d) `Σb` preserves parity, support and `{0, ±1}`, and `(Σb)ᵀZ″(Σb) = bᵀZ̃b`. The
  case analysis that forces `w = −𝟙_m` and root coefficient 0 is correct (the `−`
  sign case gives the same conditions). `|S| = 2q − 1`, violation `(q + 2)/(4qN)`.
  Correct. Denominators of `d″` divide `8qN`.
- (e) The covariance map is a linear bijection of `BQP_n` onto `CUT_{n+1}` (Letchford
  2022, Theorem 1, p. 11), (10) with odd `|S|` and `s = (|S| − 1)/2` maps to (18)
  (p. 11), Padberg's condition holds for odd `|S| ≥ 3`, and the cut polytope is invariant
  under permutation and switching. Correct. The facet claim covers `b*` and (18) only;
  it does not claim that the other pure violators define facets, which is fine.
- The remark on `τ² = 1/4` is correct for `q ≥ 4`. For `q = 3` a pure violator still
  exists (`w = 0`, root coefficient `−1`); the remark is stated for `q ≥ 4`, so this is
  consistent (my control [E] confirms both cases).
- Check [D]: 37 X3C instances (`q = 3`: 20, `q = 4`: 14, `q = 5`: 3). Explicit `d̃`
  formulas equal `d(M̃)`; complete enumeration of hypermetric violators of `d̃` equals
  the predicted set; complete enumeration of all violated rounded psd inequalities of
  `εd̃` in cut space equals `±` that set (`σ = ±1`, gonality `≥ 2q − 1`); odd clique
  violated iff a cover exists, with `b*` violated by `(q + 2)/(4qN)`; the pure violators
  are exactly `b*` and the `m` vectors above; brute force over `{0, ±1}^Ṽ` where
  `|Ṽ| ≤ 9`; `d″` in `(0, 1)`, metric polytope, elliptope interior, `8qN`-integral; the
  violated (18) at `d″` are exactly `C ∪ U`, both from the complete enumeration and from
  a direct sum over all odd subsets. Results in the "Checks" section.

### Literature and definitions

- Letchford (2022), checked in `sources/letchford2022-qubo-chapter.txt`: (10) and
  Padberg's facet condition (p. 8), (11) (p. 8), (12) and its facet condition and the
  remark on switching Boros–Hammer inequalities (p. 9), Definition 2 and Proposition 1
  (pp. 6–7), Theorem 1, (18) with `|S|` odd, (19) (p. 11), facets of `CUT_n` as
  switchings (p. 16), "(10)–(13) ... unknown, but we suspect that they are all NP-hard"
  (p. 18), "unknown for the remaining inequalities for the cut polytope" and the
  heuristic for "(18) and their switchings" (p. 19). All quoted and used correctly.
- GKL (2012), §2: odd clique as above; §4 "unknown" sentence. Used correctly.
- Letchford–Sørensen (2012): not used by the new material beyond what earlier rounds
  checked.
- One web search ("clique inequalities" "cut polytope" separation NP-hard Padberg
  Boolean quadric) found no earlier hardness result for (10), (18) or odd clique
  separation. Together with the author's and the round-2 searches this supports the
  hedged novelty statement; it does not establish novelty.

### Consistency of the earlier, already reviewed material

- Summary: items 1–5 match the corollaries; "Corollaries 4–6 and 8–10" is right; the
  statement that all hard points lie in the elliptope interior is right for the hard
  points used for each class (Corollary 5's singular points are superseded by
  Corollary 10 for the classes they served).
- Numbering and cross-references: Lemma 6 refers forward to (13) "of Corollary 8 below"
  and Corollary 9(e) forward to the proof of Corollary 10(d); both targets exist and say
  what is cited. Lemma 4 sits in §6 after Lemmas 5 and 6 (unchanged since round 1; not
  an error).
- §10 r2 rows match `logs/check_binary_separation.log` line by line (60 instances, 33
  and 19 for Corollary 9; 60 instances, 34 with a cover, brute force on 47, `|S| ∈ {5,
  7, 9}` for Corollary 10; control 10 of 10; facets of (18) in 8 cases).
- Limits: the eigenvalue bound `λ_min(X̃(1/N)) ≤ ετ² = 1/(8qN)` is right (unit vector
  `e_{oⱼ}`).

## Checks run by the reviewer

All commands from `research-20261001/binary-separation/`, with `OMP_NUM_THREADS=1`, a
`timeout`, and at most two processes at a time. Outputs in `reviews/r3-work/`.

1. `timeout 900 python3 code/check_binary_separation.py` →
   `reviews/r3-work/rerun_r3_check_binary_separation.log`: `ALL CHECKS PASSED`, 14.4 s;
   identical to `logs/check_binary_separation.log` apart from the timing lines.
2. `timeout 300 python3 code/closed_form_s.py` → `rerun_r3_closed_form_s.log`:
   identical to `logs/closed_form_s.log` (plus timing).
3. `timeout 300 python3 code/scip_crosscheck.py` → `rerun_r3_scip.log` and
   `timeout 600 python3 code/probe_cutcone.py` → `rerun_r3_cutcone.log`: identical to
   the logs apart from timing lines.
4. `timeout 1800 python3 -u reviews/r3-work/r3_checks.py` → `r3-work/r3_checks.log`
   (progress lines in `r3_checks.progress`). My own exact code (Fractions; SymPy only
   for [A′]):
   `REVIEWER R3 CHECKS PASSED`, 758 s, 0 failures in every block:
   - [A] Lemma 6 (i)–(iv) on 300 random rational points (up to 6 variables), 1500
     `(v, s)` pairs, the (12) correspondence with the printed formula, and the cut
     switching; [A′] Lemma 6(ii) symbolically for generic `x, y, v, s` (4 variables);
   - [B] Corollary 9 on 40 X3C instances (`q ∈ {3, 4}`, 27 with a cover), as described
     above;
   - [C] the remark after Corollary 9 on 300 random points, and the (18) subfamily
     conditions for `|S| ≤ 8`;
   - [D] Corollary 10 on 37 X3C instances (`q = 3, 4, 5`: 20, 14, 3; 26 with a cover);
     brute force over `{0, ±1}^Ṽ` on the 18 instances with `|Ṽ| ≤ 9`; violated (18) of
     sizes 5, 7 and 9; and the maximum violations used in R3-m1: `4qN·max = q + 3` for
     odd clique and `2N·max = 1` for all rounded psd inequalities at `εd̃`, on every
     yes-instance;
   - [E] control `τ² = 1/4` on 10 X3C instances with a planted cover (`q = 3, 4, 5`):
     rounded psd inequalities are violated, no odd clique inequality is violated for
     `q ≥ 4`, and one still is for `q = 3`;
   - [F] facets by exact affine rank of the tight 0/1 points: (10) with
     `(|S|, s) = (q + 1, 1)` in `BQP_{q+1}` for `q = 3, 4, 5` and with one unused
     variable for `q = 3, 4`; (18) with `|S| = 5` in `CUT_5..CUT_7`, `|S| = 7` in
     `CUT_7, CUT_8`, `|S| = 9` in `CUT_9`; and `b*` itself on two actual Corollary 10
     instances (`CUT_7`, `CUT_8`). All facets.

   The enumerations are mine: all integer `y` with `(y − c)ᵀG(y − c) < R` by `LDLᵀ`
   Fincke–Pohst, with exact filtering. Violated rounded psd inequalities are enumerated
   directly in cut space (`bᵀ(J − 2D)b < 1` over the odd-`σ` vectors
   `b = (2k + 1 − Σb_W, b_W)`), so they do not rely on the split identity that the
   note's own checks use. The run was limited to 3 instances with `q = 5` because each
   takes about 5 minutes in my exact code.
5. Literature: page-split reads of `sources/letchford2022-qubo-chapter.txt` (pp. 6–12,
   16–20) and `sources/gkl2012-gap-ineqs-complexity.txt` (§2, §4); one WebSearch (item
   above).

`code/probe_gap.py` and `code/check_gap0.py` were not rerun: they test material that
did not change in revision r2 and were reproduced in rounds 1 and 2.

Three earlier runs of my own script were stopped by me and are not reported as
results. The first had a wrong ellipsoid center in my Boros–Hammer enumeration (my bug:
the center is `e₀/2`, not `X⁻¹e₀/2`; the script's own non-violator assertions caught
it). The next two were too slow for `q = 5` with 8 instances; I then reordered the
enumeration coordinates (narrowest range first) and reduced `q = 5` to 3 instances.
None of these runs touched the stream's files. `r3-work/rerun_check_binary_separation.log`
is from the interrupted earlier round-3 reviewer; my rerun is
`rerun_r3_check_binary_separation.log`. At the end no process of mine was running
(`ps` check).
