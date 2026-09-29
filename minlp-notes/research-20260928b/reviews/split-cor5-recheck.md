# Recheck of Corollaries 3 and 5 (split separation note, revision of 2026-09-29)

Date: 2026-09-29. Reviewer: fresh independent reviewer, who had not seen the
material before this recheck.

Scope: only the new substantive claims in
[`split-separation-np-complete.md`](../side-results/split-separation-np-complete.md)
(§11 items 1 and 2):

1. Corollary 5: at X3C points, the de Meijer et al. families.
2. Corollary 3 sharpened: the gap `2/(9(N−1))`, the additive bound, the claim
   that this gap is optimal, and the padding claim.

The note was not edited. My own scripts are in [`split-cor5/`](split-cor5/)
(§4).

## Verdicts

| Claim | Verdict |
|---|---|
| Corollary 5 (i)–(v), the flipped matrix `DXD`, and strong NP-hardness | **Correct.** One minor slip: the displayed formula for `Ĝ` is wrong when `(q, n) = (1, 1)`. The conclusion still holds there (P1). |
| Corollary 5, the source forms of (2.1)–(2.3), (2.5), (4.1), (4.4) and (4.5)–(4.8) | **Correct.** They match arXiv:2603.28979v1 exactly (§1). |
| Corollary 5, the step `C(k,2)/k = ⌊k/2⌋` for (4.4) and sign-flip invariance | **Correct** (§2). |
| Corollary 3, `μ = 2/(9(N−1))` at `h² = (n+1)/8`, and additive error below `1/(9(N−1))` strongly NP-hard | **Correct.** |
| Corollary 3, "within this construction the gap cannot be improved" (and §11 "the largest possible") | **Overstated** (P2). The arithmetic is right for the parameter ranges it names. Those ranges come from two sufficient conditions, and the same construction gives a larger gap: `2/(8N−7)` with `M = 1`, and `2/(N+7)`, about 9 times larger, with the `M = 3` scaling that the note itself mentions. |
| Corollary 3, for padded X3C (`n ≥ 3q`) every `|Xᵢⱼ| ≤ 1` | **Correct.** Padding is needed: at `n = q`, `X_gg > 1` once `q ≥ 8`. |
| §8 wording, "(2.3) the most beneficial of these" | **Minor nit** (P3). |

No error invalidates a stated hardness result.

## 1. Source forms (de Meijer, Piccialli, Sotirov, Sudoso, arXiv:2603.28979v1)

I checked the local text
(`scouting/open-problem-sweep/2603.28979.txt`, which keeps the PDF labels)
against the arXiv HTML (https://arxiv.org/html/2603.28979v1). The HTML numbers
equations consecutively: (1)–(3), (14), (17) and (18)–(21) there are the
PDF's (2.1)–(2.3), (4.1), (4.4) and (4.5)–(4.8). In the notation of the
source, where `x` and `X` are the variable parts:

- (2.1)–(2.2): for `1 ≤ i < j < k ≤ n`, the four inequalities
  `Xij + Xik + Xjk ≥ −1`, `−Xij + Xik − Xjk ≥ −1`, `Xij − Xik − Xjk ≥ −1` and
  `−Xij − Xik + Xjk ≥ −1`. These are the four patterns `sᵢsⱼ` for
  `s ∈ {±1}³` up to a global sign.
- (2.3): `Xij ≤ Xii` and `Xij ≥ −Xii` for all `i, j ∈ [n]`, `i ≠ j`. This is
  the same as the note's `|Yᵢⱼ| ≤ Yᵢᵢ` for all ordered pairs `i ≠ j`.
- (2.5): `Mₙ = {X ∈ Sⁿ : (2.1)–(2.3), Xii ≤ 1}`.
- (4.1): the linear constraints `aᵢᵀx = bᵢ`, `diag(X) ≥ x`, `diag(X) ≥ −x`,
  `diag(X) ≤ 𝟙`, and `[[1, xᵀ], [x, X]] ⪰ 0`. Without the linear constraints,
  this is the note's (i).
- (4.4): `Σ_{i,j∈S, i<j} vᵢvⱼXij ≥ ⌈−|S|/2⌉` for `S ⊆ [n]` with `|S|` odd and
  `vᵢ ∈ {±1}`. The PDF text extraction loses the bracket glyphs, so I took
  the ceiling from the HTML. For odd `|S|`, `⌈−|S|/2⌉ = −⌊|S|/2⌋`, as the
  note writes.
- (4.5)–(4.8): `Xij + xi + xj ≥ −1`, `Xij − xi − xj ≥ −1`,
  `−Xij + xi − xj ≥ −1` and `−Xij − xi + xj ≥ −1` for `i < j`. These are
  exactly `sᵢsⱼXij + sᵢxᵢ + sⱼxⱼ ≥ −1` for `s = (1,1), (−1,−1), (1,−1),
  (−1,1)`, as in the note's (v).

The note's variable set is `{1, …, n, g}`, of size `n + 1`. Its `Y` is the
source's `X`, and `Y ∈ M_{n+1}` follows from (ii), (iii) and `Yᵢᵢ ≤ 1`.

## 2. Corollary 5: the proof

I checked each step by hand. My script also checks the conclusions directly
(§4).

- **Entries of `G`.** For X3C, `Gᵢⱼ = |Sᵢ ∩ Sⱼ| ∈ [0, 3]` for `i ≠ j` (the
  value 3 occurs for repeated sets), `Gᵢᵢ = 7`, `Gᵢg = 5`,
  `G_gg = 3q + 2n + 1`, `G₀ᵢ = 0` and `G₀g = −2(n+1)`. All are confirmed on
  every instance.
- **(iii) for every `h`.** Off-diagonal entries of `G` are at most `5` in
  absolute value, and diagonal entries are at least `min(7, 3q + 2n + 1) ≥ 6`.
  (2.3) compares entries of one matrix, so the positive factor `1/G₀₀` does
  not matter. This holds for every `h² ≥ 0`, even below the Theorem 1
  threshold (checked at `h² ∈ {0, 1/100, (n+1)/8, n+1, 10⁶}`).
- **The `ε` bound.** `4h² ≥ max(3, n+1)Ĝ` gives `Ĝ/(4h²) ≤ min(1/3, 1/(n+1))`.
  The inequality `|Gᵢⱼ|/(4(n+1) + 4h²) < Ĝ/(4h²)` is strict because
  `4(n+1) > 0`. `h² ≥ (3/2)(n+1) ≥ (n+1)/8` follows from `Ĝ ≥ 2(n+1)`.
- **(i).** `X ≻ 0` by Theorem 1(a). `Yᵢᵢ > 0 = xᵢ` for `i ≤ n`, and
  `G_gg − |G₀g| = 3q − 1 > 0`, so `Y_gg > |x_g|`. `Yᵢᵢ < 1/3 ≤ 1`.
- **(ii) and (v).** Each side is a sum of three terms, each below `1/3` in
  absolute value. In (v) the terms `xᵢ = Xᵢ₀` have `(i, 0) ≠ (0, 0)`, so the
  bound applies to them too.
- **(iv).** For odd `k = |S| ≥ 3`, `k ≤ n + 1` gives `ε ≤ 1/k`, and each of
  the `C(k,2)` terms is strictly above `−ε`. So the sum exceeds
  `−C(k,2)/k = −(k−1)/2`, and `(k−1)/2 = ⌊k/2⌋` because `k` is odd. For
  `k = 1` the inequality is `0 ≥ 0`. The step is correct.
- **Sign flips.** For `σ ∈ {±1}^{vars}`, the map `x ↦ σ∘x`, `Y ↦ σσᵀ∘Y` is a
  congruence, so it preserves PSD. It preserves `diag(Y)` and `|x|`, and it
  permutes the sign vectors `s` in (2.1)–(2.2), (4.4) and (4.5)–(4.8). (2.3)
  involves only `|Yᵢⱼ|`. So all five families are invariant. For `DXD`,
  `x` does not change, since `xᵢ = 0` for `i ≤ n` and `D_gg = 1`. Checked on
  every `σ` for `n + 1 ≤ 5` (1,924 flipped matrices).
- **Strong NP-hardness.** `G₀₀ = 4(n+1) + max(3, n+1)Ĝ` is an integer of size
  `O(n(n+q))`. All entries are polynomially bounded, and X3C is strongly
  NP-complete. Correct.

**P1 (minor): the formula for `Ĝ`.** The note states
`Ĝ = max(3q + 2n + 1, 2(n+1))`. This leaves out the diagonal entry
`Gᵢᵢ = 7`. The proof says only `G_gg ≥ 6`. For `(q, n) = (1, 1)` the true
value is `Ĝ = 7`, while the formula gives 6. The script found this on the one
such instance. The conclusion survives, because the `4(n+1)` term in `G₀₀`
gives slack: `X₁₁ = 7/26 < 1/3` at `4h² = 18`. The script checked all
properties with both values of `Ĝ`. Two further points:

- The term `2(n+1)` is redundant, since `3q + 2n + 1 > 2(n+1)` for `q ≥ 1`.
- Suggested fix: write `Ĝ = max(7, 3q + 2n + 1)`, which equals `3q + 2n + 1`
  unless `q = n = 1`.

The note's own script computes `Ĝ` from the matrix and uses only
`q ∈ {2, 3}`, so it could not catch this.

**Optional strengthening.** Corollary 1(iii) says every violated split has
`|supp w| = q + 1`. So for `q ≥ 2` the points also satisfy the 1- and
2-index splits (4.3) and (4.11)–(4.12). Together with (2.3), this means every
family that de Meijer et al. separate exactly (their §6.2) is satisfied, not
only the families listed in Corollary 5.

## 3. Corollary 3

**Gap and additive bound: correct.** With `γ² = n + 1` and `h² = (n+1)/8`,
all violators have `q = −1/(4(n+1+h²)) = −2/(9(n+1))`. Here `N = n + 2`, so
the gap is `2/(9(N−1))`. An algorithm with additive error `δ < 1/(9(N−1))`
separates `μ = 0` from `μ = 2/(9(N−1))` by thresholding at half the gap. The
instances keep polynomially bounded numerators and denominators
(`2G₀₀ = 9(n+1)`), so the hardness is strong. This was confirmed by complete
enumeration on 45 padded X3C instances, 28 of them with a cover.

**Padding: correct.**

- If `n ≥ 3q`, the off-`(0,0)` entries of `G` are at most
  `max(7, 3q + 2n + 1, 2(n+1)) ≤ 3n + 1 < 9(n+1)/2 = G₀₀`. The largest value
  observed was `28/45`.
- Repeating a set does not change whether an exact cover exists, because two
  copies of a nonempty set cannot both be used.
- The condition matters. At `n = q`,
  `X_gg = (5q + 1)/(9(q+1)/2) > 1` exactly when `q ≥ 8`. The final review's
  A3 claim that "`n ≥ q` suffices" is therefore false for `q ≥ 8`. The note
  correctly uses `n ≥ 3q`.

**P2 (substantive wording issue): "the gap cannot be improved".** The note
maximizes `(γ² − n)/(4(γ² + h²))` over `γ² ≤ n + 1` and `8h² ≥ γ²`. That
calculation is correct. But both constraints are sufficient conditions, not
limits of the construction:

1. **Lemma 3's threshold `8h² ≥ ‖t‖²` is generic.** It is sharp only when
   `3t ∈ L` or similar. For the lattice of Lemma 2, take odd `u₀` with
   `|u₀| ≥ 3` and `ℓ = Σxᵢcᵢ + kg`. Then `u₀t + ℓ` has last coordinate
   `(k − u₀)γ`.
   - If `k ≠ u₀`, its squared norm is at least `γ²`, so there is no
     violation.
   - If `k = u₀`, the block `2x + u₀𝟙` has only odd entries, so the squared
     norm is at least `n`.

   So a violation with `|u₀| ≥ 3` needs `(u₀² − 1)h² < γ² − n`, and
   **`8h² ≥ γ² − n` suffices**. With `γ² = n + 1`, this allows `h² = 1/8`,
   and the gap becomes `1/(4(n + 1 + 1/8)) = 2/(8n+9) = 2/(8N−7)`. That
   exceeds `2/(9(N−1))` for `N ≥ 3`; the ratio tends to `9/8`.
   - Checked on 40 X3C instances and 80 general 0/1-equation instances: the
     violated set is exactly Theorem 1(b).
   - The refined threshold is sharp. With three copies of the universe
     (`q = 1`, `A𝟙 = 3·𝟙`), `h² = 1/9` gives spurious violators with
     `|u₀| = 3`, and `h² = 1/8` gives none.
2. **`γ² ≤ n + 1` comes from `M = 1`.** The note's own Lemma 2 remark says
   that scaling the first block by `M` widens the window to
   `n < γ² ≤ n + min(8, M²)`. I rechecked that case analysis: non-binary `x`
   gives `F ≥ n + 8`, and binary non-solutions give `F ≥ n + M²`. With
   `M = 3` and `γ² = n + 8`:
   - at Lemma 3's generic `h² = γ²/8`, the gap is `16/(9(n+8))`;
   - at the refined `h² = (γ² − n)/8 = 1`, the gap is
     `2/(n+9) = 2/(N+7)`.

   Checked on 40 X3C instances (23 with a cover) and the 80 general
   instances: the violated set is exactly Theorem 1(b), and the gaps are as
   stated. `M = 3` is a constant, so strong NP-hardness is kept.

   With `M = 3`, `G₀₀ = 4n + 36`, `G_gg = 27q + 2n + 8`, `Gᵢᵢ = 31`,
   `Gᵢg = 29`, `Gᵢⱼ ≤ 27` and `|G₀g| = 2(n+8)`. So every `|Xᵢⱼ| ≤ 1` exactly
   when `27q ≤ 2n + 28`, which padding to `n ≥ 14q` ensures. Checked with
   full enumeration at `(q, n) = (1, 2)` and `(2, 13)`, and by entries only
   at `(3, 27)`.

   Under the same refined threshold, the gap `2(γ² − n)/(9γ² − n)` increases
   with `γ²`, so `2/(n+9)` is the best value this family of parameters gives.

So additive error below `1/(N+7)` is strongly NP-hard, which is about
9 times the note's `1/(9(N−1))` for large `N`. Corollary 3's stated bounds
remain true, since they are weaker. The sentence "Within this construction
the gap cannot be improved" and §11's "largest possible within this
construction" should be qualified, for example as "largest under Lemma 2 with
`M = 1` and Lemma 3's generic threshold". Alternatively, Corollary 3 could
adopt `2/(N+7)`, with the two-line `|u₀| ≥ 3` argument above added for Lemma
2's lattice.

## 4. Scripts and checks run

Standard library only, exact `Fraction` arithmetic. The scripts were written
independently of `side-results/check_split_separation.py`. I read that script
but did not import it.

- `split-cor5/lib.py` provides the helpers:
  - the Gram construction for general `M`, `γ²` and `h²`;
  - a complete Fincke–Pohst enumeration of all `u ∈ e₀ + 2ℤᴺ` with
    `uᵀXu < 1`, over an exact `LDLᵀ` factorization;
  - an independent brute box search, with the box from `(X⁻¹)ᵢᵢ`;
  - each de Meijer family written out separately from the source text.
- `split-cor5/cor5_check.py`, run with
  `python3 research-20260928b/reviews/split-cor5/cor5_check.py` (about
  3 min). Output is in `cor5_check.log`. It prints `COR5 CHECKS PASSED`.
  - Liveness: five probes, each flagging exactly its family. The (4.4) probe
    (unit diagonal, off-diagonal `−6/25` on five variables) is positive
    definite. The note's probe (`−3/10`) is not PSD (eigenvalue
    `1.3 − 1.5 < 0`); that is harmless for a checker probe.
  - 255 X3C instances (`q ∈ {1, 2, 3}`, `n ≤ 8`, 135 with a cover), checked
    at `4h² = max(3, n+1)Ĝ` with both the true `Ĝ` and the formula `Ĝ`:
    - `X ≻ 0` and `X₀₀ = 1`;
    - the violated set is Theorem 1(b);
    - `X` and `DXD` satisfy (4.1), (2.1)–(2.3), (4.4) (all odd `S`, all
      signs) and (4.5)–(4.8);
    - the 0/1 violators of `DXD` are exactly `(0, x, 1)`;
    - the largest `max|Xᵢⱼ| / min(1/3, 1/(n+1))` is `13/15`.
  - Smallest slacks: (2.1)–(2.2) 0.778; (2.3) 0.0074; (4.1) 0.0185;
    (4.5)–(4.8) 0.654; (4.4) exactly 0, from `|S| = 1`.
  - Informational: on these instances (4.4) also holds with only
    `4h² = 3Ĝ`.
- `split-cor5/cor3_check.py`, run with
  `python3 -u research-20260928b/reviews/split-cor5/cor3_check.py` (about
  5 s). Output is in `cor3_check.log`. It prints `COR3 CHECKS PASSED`.
  Parts A–D are as described in §3, plus these:
  - the enumerator matched the brute box search on 68 positive definite
    matrices;
  - the gap formula `(γ² − n)/(4(γ² + h²))` was confirmed in 27
    `(γ², h²)` cases.
- An inline computation, logged in `split-cor5/padding_and_ratios.log`,
  checked:
  - the `n = q` padding threshold `q ≥ 8`;
  - the entry bound under `n ≥ 3q` for all `q < 60`;
  - the gap ratios.

These are targeted checks only. No project-wide verification was run, and CI
was not inspected.

## 5. Other remarks

**P3 (nit, §8).** "de Meijer et al. report the pair inequalities (2.3) as
the most beneficial of these." The source's sentence (§4, after the
description of `IQ¹₃`) compares the 31 facets of `IQ¹₃` imposed on 3×3
principal submatrices. RLT and odd-set inequalities were not part of that
comparison. Suggested wording: "the most beneficial of the `IQ¹₃` facets".
