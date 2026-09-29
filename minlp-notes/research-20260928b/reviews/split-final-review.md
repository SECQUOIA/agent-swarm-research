# Final review: split separation is NP-complete

Target: [`side-results/split-separation-np-complete.md`](../side-results/split-separation-np-complete.md)
and its script [`side-results/check_split_separation.py`](../side-results/check_split_separation.py).
Date: 2026-09-28. Reviewer: fresh independent adversarial review. I did not write
the note, did not review it before, and did not edit it. My scripts and logs are
in [`split-final/`](split-final/). They share no code with the note's script.

## Verdict

The note is **correct**. I found no mathematical error in any theorem, lemma,
corollary or proof, and every quoted source statement that I could reach
matches its source. The reworked single Gram-matrix reduction with `M = 1`
holds, including every case, strictness, `t ≠ 0` and the threshold `8h² ≥ ‖t‖²`.

The recommended changes are one understatement with practical relevance (§A1:
the X3C hard points also satisfy the ternary pair inequalities) and several
small wording and attribution fixes (§A2–§A7). None of them changes a theorem.

| Claim | Verdict | Notes |
|---|---|---|
| §1 definition of split inequalities and SPLIT-SEP | correct | Matches B–T (5)–(7), de Meijer (4.9)–(4.10), Burer–Letchford Prop. 11 (checked in the local texts). |
| §1 attribution quotes | correct | All five quotes verified verbatim, including B–T p. 3 and p. 8 and de Meijer p. 11. |
| Lemma 1 (parity form, Voronoi reading) | correct | Nit on the word "lattice" (§A5). |
| Lemma 2 (strictly closer point, `M = 1`) | correct | All cases re-derived. The window `n < γ² ≤ n + min(8, M²)` is exact (tested for `M = 1..4` at the top and just above it). The rational `γ` is correct. Wording nit (§A4). |
| Lemma 3 (embedding) | correct | `t ≠ 0` and `8h² ≥ ‖t‖²` are used correctly. The sharpness example is right. Tested on 1,500 random lattices against an independent closest-point enumeration. |
| Theorem 1 (a)–(c) and general `h` | correct | The printed `G` matches the Gram matrix of the stated vectors. Violator set and minimum value confirmed. |
| Corollary 1 (i)–(iii) | correct | Entry bound, denominator, `|supp w| = q + 1` and the promise argument hold. |
| Corollary 2 (0/1 and bounded families) | correct | The reading of de Meijer's multi-index family and of (4.3) under `v ↦ −v−e₀` is right. |
| Corollary 3 (approximation) | correct | The additive bound can be improved to `1/(9(n+1))`. State it in terms of the input order (§A3). |
| Lemma 4 (non-PSD, elimination) | correct | Every step holds, including `(Xz)_K = 0` and the size argument. The remark about B–T's rational-eigenvector assumption is accurate. |
| Theorem 2 (NP membership, three cases) | correct | The PD bound, the singular factorization `X = PᵀGP` with `|wᵢ| < (X_KK)ᵢᵢ^{1/2}`, and the Diophantine step all hold. |
| Theorem 3 (FPT in rank) | correct | The reduction to rank-`r` CVP holds and was tested. The running time rests on Kannan (1987), which I did not re-derive. |
| Corollary 4 (fixed support) | correct | |
| Theorem 4 (rank one) | correct | `gcd(p) = 1`, `q = m(m+D)/D²`, the maximum `⌊D²/4⌋/D²` and form (c) all hold. |
| Remark 1 (placement near `ℓ(0)`) | correct but **understated** | X3C instances satisfy the pair inequalities (2.3) automatically. With `4h² ≥ max(3, n+1)Ĝ` the points also satisfy all of de Meijer's (4.4) (§A1). |
| §6 binary analogue | correct | Identity, GKL/Avis/Avis–Grishukhin quotes and "does not settle max-cut" all hold. |
| §7 priority and novelty | appropriately hedged | One attribution nuance about van Emde Boas (§A6). An optional disambiguation from MILP split cuts is suggested (§A7). |
| §8 solver relevance | correct except one bullet | The "Limits" bullet on pair inequalities should change with §A1. |
| §9 corrections to the scout report and the review | correct | |
| §10 checks | reproduced | `ALL CHECKS PASSED` in 8.1 s. The output matches the table. |

## 1. Line-by-line findings

### 1.1 Definitions and attribution (§1)

- `v = (−s−1, w)` gives `(1,x)ᵀv · (1,x)ᵀ(v+e₀) = (wᵀx−s−1)(wᵀx−s)`. The
  linearization is `vᵀXv + vᵀXe₀`. The map `(w,s) ↦ (−w,−s−1)` is
  `v ↦ −v−e₀`. For `w = 0` the value is `s(s+1) ≥ 0`. All correct.
- Quotes verified against
  `scouting/open-problem-sweep/buchheim-traversi-oo2013-3953.txt` (p. 3 "we
  agree with the conjecture of Burer and Letchford [8] …"; p. 8 "As mentioned
  by Letchford [11] …"; "X* can be an arbitrary symmetric matrix with
  X*00 = 1"; [11] is Letchford IPCO 2010). I also checked
  `reviews/split-separation/sources/burer-letchford-oo2011-3172.txt` (§8
  question; Prop. 11 uses the disjunction `vᵀx ≤ −s−1 ∨ vᵀx ≥ −s`, so the sign
  convention differs as the note says) and
  `scouting/open-problem-sweep/2603.28979.txt` (p. 11 "it is unclear …").
- The attribution sentence ("the question posed by Burer and Letchford,
  which Buchheim and Traversi state as Burer and Letchford's conjecture") is
  accurate for the texts available.

### 1.2 Lemma 1

`uᵀXu = 4vᵀXv + 4vᵀXe₀ + X₀₀`, `v ↦ −v−e₀` becomes `u ↦ −u`, and
`Bu = b₀ + 2Bv`. The Voronoi equivalence follows by `ℓ ↦ −ℓ`. Correct.

### 1.3 Lemma 2

`t − ℓ = ((1−m)b − Ax, (1−m)𝟙 − 2x, −mγ)`, so the formula for `F(x,m)` is
right. The cases:

- `m` odd: `F ≥ γ²`.
- `m` even and nonzero: `F ≥ n + 4γ² > γ²`.
- `m = 0` and `x ∉ {0,1}ⁿ`: `F ≥ n + 8 > n + 1 ≥ γ²`.
- `m = 0`, `x` binary and `Ax ≠ b`: `F ≥ n + 1 ≥ γ²`.
- `m = 0`, `x` binary and `Ax = b`: `F = n < γ²`.

All cases are correct, and the strict and non-strict inequalities are in the
right places.

The remark's window `n < γ² ≤ n + min(8, M²)` is exact. At `γ² = n + min(8, M²)`
there are 0 mismatches for `M = 1, 2, 3, 4`. At `γ² = n + min(8, M²) + 1/100`
there are 109 to 137 mismatches out of 300.

The rational `γ` is also right: `γ² − n = (c² − n)²/(4c²)` and
`0 < c² − n ≤ 2c − 1`, so `γ² − n ∈ (0, 1)`. I checked this exactly for
`n ≤ 20000`, for 299 perfect squares and for 50 values near `10¹²`. The
rational-`γ` route, run end to end with explicit rational vectors and `h = γ`,
also gives the predicted violators.

### 1.4 Lemma 3

- Independence and `X ≻ 0` hold.
- `Bu = 2(u₀t + ℓ, u₀h)` holds.
- For `|u₀| ≥ 3`, the left side is at least `9h² ≥ ‖t‖² + h²`.
- For `u₀ = ∓1`, the condition is exactly the CLOSER condition for `±ℓ`.
- The Gram formula holds.
- The sharpness example holds: no violator at `h² = 1/72`, and the violators
  `(1,−1)` and `(−2,1)` at `h² = 1/81`.
- The `t = 0` discussion is right: `h = ‖t‖₁` gives `b₀ = 0`.

Random test: I used 1,500 lattices (`d ≤ 4`, `k ≤ d`, integer bases, rational
`t ≠ 0`), each at three values of `h²` (`‖t‖²/8`, `‖t‖²/8 + 1/7`, `5‖t‖²`). The
violated set equals `{(−1,z), (0,−z) : ‖t − Cz‖ < ‖t‖}` in every case. The
closer points were enumerated around the least-squares centre, without using
Lemmas 1 or 3.

Below the threshold (`h² = ‖t‖²/80`), 724 of 1,500 instances gain extra
violators. Every extra violator has `v₀ ∉ {0, −1}`, which is exactly the
failure mode the note describes.

### 1.5 Theorem 1

I wrote out the Gram matrix of `b₀ = (0,0,−2γ,2h)`, `bᵢ = (Aᵢ,2eᵢ,0,0)` and
`b_g = (b,𝟙,γ,0)` for general `γ²` and `h²`. It equals the printed table at
`γ² = h² = n+1`: `G₀₀ = 8(n+1)`, `G₀g = −2(n+1)`, `Gᵢg = Aᵢᵀb + 2` and
`G_gg = ‖b‖² + 2n + 1`.

- (a) holds.
- (b) holds: `(v₁..vₙ, v_g) = (x, −1)` for `v₀ = −1`, and `(−x, 1)` for
  `v₀ = 0`.
- (c) holds: `q = (n − γ²)/(4(γ² + h²)) = −1/(8(n+1))`, and every violator
  has this same value.
- The general-`h` version holds, with `−1/(4(n+1+h²))`.

Independent tests, with 0 failures:

| Instances | Count | Oracle |
|---|---|---|
| Subset sum with `aᵢ ∈ −6..9` (zeros and negatives), `n ≤ 5` | 400 | Fincke–Pohst |
| 0/1 equations with 1–4 rows, entries `−4..4` | 300 | Fincke–Pohst |
| Subset sum, cross-checked with the Cauchy–Schwarz box of Theorem 2 | 120 | box, provably complete |
| Hand-picked edge cases (`n = 1`, `s = 0`, `b = 0`, zero and duplicate columns, multiple solutions) | 16 | box |
| `h² ∈ {(n+1)/8, 7(n+1)/3, 10⁶(n+1)}` | 250 each | Fincke–Pohst |

Negative control: `h² = (n+1)/200` gives 40 of 250 mismatches, as expected.
At `h² = (n+1)/9` there are 0 mismatches. This is consistent, because the
threshold is only sufficient.

### 1.6 Corollaries 1–3

- **1(ii).** For X3C, `Gᵢⱼ = |Sᵢ ∩ Sⱼ| + 4δᵢⱼ ≤ 7`, `Gᵢg = 5` and
  `G_gg = 3q + 2n + 1`, so the stated bound and the denominator `8(n+1)` hold.
  Test: 150 random instances with `q ∈ {2,3,4}` and repeated sets allowed. The
  largest entry was 88 = 8·11. All checks held: the violated set, the bound,
  `|supp w| = q + 1`, the flipped 0/1 violators `(0,x,1)`, the
  `{v₀ = 0, vᵢ ∈ {0,±1}}` family, and `μ`.
- **1(iii).** The promise argument and the `O(nᵏ)` enumeration for `q < k`
  are correct.
- **2.** `q_{DXD}(v) = q_X(Dv)` because `De₀ = e₀`. The source check confirms
  that de Meijer's (4.11)–(4.12) come from `v₀ = 0`, `vᵢ, vⱼ ∈ {±1}`, and that
  (4.3) comes from `v₀ = −1`, `vᵢ = ±1`. So the note's description of the
  "three or more indices" family is accurate.
- **3.** Both bullets are correct. See §A3 for an optional sharpening.

### 1.7 Lemma 4 and Theorem 2

- **Lemma 4.** Step 2 gives `zᵀSz = 2Sᵢⱼzᵢ + Sⱼⱼ = −1`. The Schur-complement
  extension preserves the value. By induction over the pivots, the extension
  gives `(Xz)_K = 0`, so `z_K = −X_KK⁻¹X_{K,R}z_R` and Cramer's rule bounds the
  size. `N = ⌊|β|/|α|⌋ + 1` gives `N|α| > |β|`, so `q(Nz) < 0`. Such a split
  automatically has `w ≠ 0`.
- **Lemma 4, tests.** I implemented steps 1–4 with a different index order
  (largest pivot first, last zero-diagonal pair first). On 158 non-PSD and 314
  PSD matrices (random, Gram, near-PSD perturbations and hand-made matrices
  with zero diagonal entries and zero rows), every property held:
  - non-PSD: the certificate, `(Xz)_K = 0`, and `Nz` violated;
  - PSD: `|K| = rank X` (rank computed independently), `X_KK ≻ 0`, and
    `X = PᵀGP`.
- **B–T remark.** B–T's Algorithm 1 is stated "if v ∈ Q^{n+1} is an
  eigenvector". The proof of their Theorem 5 says the eigenvector "can be
  computed in polynomial time and its encoding length is polynomial". The
  note's "small gap" is a fair description.
- **Theorem 2.**
  - PD case: `|uᵢ| ≤ ((X⁻¹)ᵢᵢ uᵀXu)^{1/2}`. On 70 violators there were 0
    violations of the bound.
  - Singular case: `X = PᵀGP` with `P = X_{K,·}` and `G = X_KK⁻¹`. The bound
    `|wᵢ| < (X_KK)ᵢᵢ^{1/2}`, the denominators of `w`, and
    `2Py = w − Pe₀ ⇒ u′ = e₀ + 2y′` with `Pu′ = w` all hold. The bound held
    on every violator found in the tests below.

### 1.8 Theorem 3 and Corollary 4

`w₀ᵀGw₀ = X₀₀ = 1`, and `uᵀXu = ‖w₀ + 2Pv‖²_G`, so the reduction is right.

Test: 224 singular PSD matrices of rank 1–3 with `N ≤ 5`. The steps were:

1. build `P` and `G`;
2. compute an HNF basis `W = PT` with my own column HNF;
3. enumerate every `z` with `‖Wz + w₀/2‖²_G < 1/4`.

Soundness: every `v = Tz` is violated. Completeness: every violator found by
brute force over `|vᵢ| ≤ 3` in the original coordinates maps to an enumerated
`z`. The reduced minimum is never above the box minimum. There were 0
failures.

The `r^{O(r)}` and `2^{O(r²)}` running times are standard citations. I did not
re-derive them.

### 1.9 Theorem 4

`gcd(p) = 1`, and the prime-power argument is correct. `q = m(m+D)/D²`, the
minimizer is `m = −⌊D/2⌋`, and the maximum violation is
`⌊D/2⌋⌈D/2⌉/D² = ⌊D²/4⌋/D²`. The elementary split for a fractional coordinate
is violated. In (c), `κ` is an integer because `p` is primitive.

Test: 300 random `ℓ(x)` with brute force over a box that provably contains a
minimizer. 0 failures.

### 1.10 Remark 1 and §6

- **Remark 1.** Entries of `X(h) − ℓ(0)` are below `Ĝ/(4h²)`, and the slack
  argument holds. On 400 random `(A′, ε)` there were 0 failures. The choice
  `4h² = 3Ĝ` gives entries below `1/3`, which implies de Meijer's (2.1)–(2.2),
  (4.5)–(4.8) and `diag ≤ 1`. `G_gg − |G₀g| = ‖b‖² − 1`, and the `b = 0`
  counterexample is real (`a = (1,2)`, `s = 0`: `X_gg = 5/24 < 1/4`). The
  inequality forms were checked against the source text lines for
  (2.1)–(2.3), (4.1) and (4.5)–(4.8).

  Test: 475 subset-sum instances with `s ≠ 0` and 60 X3C instances. There
  were 0 failures, and the violated set was unchanged. `ℓ(0)` is even an
  exposed point of `IQₙ`: `Σᵢ≥1 Xᵢᵢ` is 0 there and positive elsewhere on
  `IQₙ`.
- **§6.** The identity holds on 500 random matrices with `Xᵢᵢ = X₀ᵢ`. The
  affine-span claim holds: the binary `ℓ(x)` span dimension `n + C(n,2)` for
  `n ≤ 5`. The switching and "rounded psd" statements match GKL (rounded psd:
  "σ(b) is odd, and the right-hand side … replaced with ⌊σ(b)²/4⌋"; "even if
  Theorem 3 implies that rounded psd separation can be reduced to
  hypermetric separation"). The Avis 2003 ("Its complexity status is
  unknown") and Avis–Grishukhin ("We are not able to prove that P1 is
  NP-hard", where P1 is hypermetricity testing) quotes match. The
  sphere/Delaunay explanation of why the reduction does not reach the binary
  case is correct.

## 2. Recommended changes

### A1. The hard points also satisfy the pair inequalities (Remark 1, §8)

This is an understatement, not an error, but it matters for §8.

The note says the pair inequalities `|Xᵢⱼ| ≤ Xᵢᵢ` (de Meijer (2.3)) "can
fail", and §8 says the hard points "need not satisfy … the ternary pair
inequalities". Both statements are true for subset-sum instances. However,
**every X3C instance satisfies (2.3)** for every `h`. For `i ≠ j` in
`{1..n, g}`:

- `|Gᵢⱼ| = |Sᵢ ∩ Sⱼ| ≤ 3 < 7 = Gᵢᵢ`;
- `|Gᵢg| = 5 ≤ min(Gᵢᵢ, G_gg) = min(7, 3q + 2n + 1)`.

(2.3) compares entries of the same matrix, so the scaling by `G₀₀` does not
matter.

Measured: (2.3) fails on 368 of 475 subset-sum instances but on 0 of 60 X3C
instances. So strong NP-hardness holds at positive definite points that
satisfy, at the same time, de Meijer's (4.1) without linear constraints, the
triangle inequalities (2.1)–(2.2), the pair inequalities (2.3) and the RLT
inequalities (4.5)–(4.8). That is, the points lie in their `M` set (2.5) as
well.

Taking `4h² ≥ max(3, n+1)·Ĝ` also makes every entry of `X − ℓ(0)` smaller
than `min(1/3, 1/(n+1))`. Then all generalized triangle inequalities (4.4)
hold as well, since for `|S| = k` odd, `C(k,2)/k = ⌊k/2⌋`. This was checked
with `4h² = (n+1)Ĝ` on 85 instances with `n + 1 ≤ 7`.

de Meijer et al. report (2.3) as the most beneficial class. So the
correct §8 "Limits" bullet is: the hard points need not satisfy binary
structure, while via X3C they can be made to satisfy all of (4.1) without
linear constraints, (2.1)–(2.3), (4.4) and (4.5)–(4.8).

### A2. Remark 1 slack bound (nit)

Say `h² ≥ max((n+1)/8, ‖A′‖₁Ĝ/(4ε))`, so that the violated set is visibly
preserved. This is implicit in "the general-`h` form" but easy to miss.

### A3. Corollary 3 additive bound (optional)

- **State it in terms of the input.** `n` is Theorem 1's `n`. For an input of
  order `N`, the bound reads `1/(16(N−1))`.
- **It can be sharpened.** Within the admissible parameters (`γ² ≤ n+1`,
  `8h² ≥ γ²`), the gap `(γ² − n)/(4(γ² + h²))` is largest at `γ² = n+1`,
  `h² = (n+1)/8`, where it equals `2/(9(n+1))`. This was checked on 100
  instances. So additive error below `1/(9(n+1))` is already hard.
- **Normalization.** For nontrivial X3C instances (`n ≥ q`), every entry of
  `X` lies in `[−1, 1]`, so the additive statement is not an artifact of huge
  entries. This is worth one clause.

### A4. Lemma 2 remark wording (nit)

"with the lattice point `g` placed at exactly the threshold distance `‖t‖`"
describes the untranslated picture, with target `(b, 𝟙, 0)`. In the note's own
frame (target `t = (0,0,−γ)`), the lattice point at distance `‖t‖` is `0`
(`m = 1`, `x = 0`), and `g` is at distance `(‖b‖² + n + 4γ²)^{1/2}`. Suggested
wording: "with the lattice point `g` at distance `γ` from the textbook target
`(b, 𝟙, 0)`; translating by `g` gives `t` and puts `0` at the threshold."

### A5. Lemma 1 "lattice" (nit)

`L = Bℤⁿ⁺¹` is generated by possibly dependent columns. For rational `X` it is
still discrete, because `‖Bz‖² = zᵀXz ∈ δ⁻¹ℤ`. One clause would make the
Voronoi-cell language exact.

### A6. van Emde Boas attribution (low severity; not fully verified)

The note calls Lemma 2 "van Emde Boas's (1981) subset-sum reduction for CVP".
The `[a; 2I]`, `[s; 𝟙]`, `r = √n` reduction is the textbook proof.

- Regev's 2004 lecture notes (Tel Aviv, "complexity.pdf", Theorem 2) present
  it without attributing it to van Emde Boas, and cite van Emde Boas for
  ℓ∞-SVP.
- The 1981 report's title refers to a partition problem.

I could not access the 1981 report or Micciancio–Goldwasser. Safer wording:
"the standard subset-sum reduction for CVP (textbook form, e.g.
Micciancio–Goldwasser Ch. 3; CVP was first shown NP-hard by van Emde Boas
1981)". The same applies to the Summary's novelty caveat.

### A7. Disambiguation from MILP split cuts (optional)

Readers may recall that separating split cuts for MILP is NP-hard (Caprara and
Letchford, Math. Program. 2003). That is a different problem, as B–T also
stress. One sentence in §7 would prevent the confusion. I cite this from
memory and did not re-check it in this review.

## 3. The note's script

I read `check_split_separation.py` in full and reran it. It prints
`ALL CHECKS PASSED` in 8.1 s, with output identical to the §10 table: 680
subset-sum instances (391 solvable), 147 negative-control mismatches, 300
multi-row instances, 200 X3C instances (largest entry 64), 104/182 for
Lemma 4, 610 location instances.

Its enumerator is complete. It eliminates the last variable first, enumerates
`u₀` first, uses strict pruning `t < rem`, and filters parity correctly. The
rank-one check is exhaustive over residues, so its "best" is the true minimum.
Its location check tests the same inequality forms as the source.

Its coverage is narrower than mine: subset-sum values are positive only, X3C
has `q ≤ 3` and no repeated sets, and there is no singular-PSD or FPT test.
The claims themselves hold on the wider coverage.

## 4. Checks actually run

These are targeted checks only. No project-wide verification was run, and CI
was not inspected. All scripts use exact `fractions.Fraction` arithmetic and
the standard library only. Commands were run from
`research-20260928b/reviews/split-final/`, except the first.

| Command | Result |
|---|---|
| `python3 research-20260928b/side-results/check_split_separation.py` (from the repository root) | `ALL CHECKS PASSED`, 8.1 s |
| `python3 check_reduction.py` → `check_reduction.log` | `ALL OK`. Oracle cross-check: Fincke–Pohst in both orders equals the Cauchy–Schwarz box on 149 PD matrices. Theorem 1 and Corollaries 1–3 hold on subset sum, multi-row and X3C instances. The γ window and the `h` threshold behave as expected, including the negative controls. |
| `python3 check_lemma3.py` → `check_lemma3.log` | `ALL OK`, about 26 s |
| `python3 check_membership_rank.py` → `check_membership_rank.log` | `ALL OK`, about 96 s. Lemma 4; Theorem 2 in the PD and singular cases; Theorem 3 soundness and completeness against brute force. |
| `python3 check_misc.py` → `check_misc.log` | `ALL OK`, about 15 s. Theorem 4, Remark 1 including the pair-inequality observation and (4.4), §6 identity, rational `γ`. |
| `python3 check_window_M.py` → `check_window_M.log` | `ALL OK`. The window `n < γ² ≤ n + min(8, M²)` is exact for `M = 1..4`. |

Source checks used the local texts in `scouting/open-problem-sweep/` (B–T,
de Meijer et al.) and `reviews/split-separation/sources/` (Burer–Letchford
2011, GKL 2011, Avis 2003, Avis–Grishukhin 1993). The WebSearch quota was
exhausted, so the literature check was limited to OpenAlex citing-work lists:

- B–T 2014/2015: 6 works;
- Letchford 2010: 4 works;
- Burer–Letchford 2012/2014: 10 works.

I read titles only. None suggests a complexity result for split separation.

## 5. What remains unchecked

- **Sources not reached:** Letchford's IPCO 2010 paper; the published
  versions of Burer–Letchford (2014) and B–T (2015); van Emde Boas (1981);
  Micciancio–Goldwasser; Kannan (1987); Kannan–Bachem (1979); Edmonds (1967);
  Schrijver's chapter references; Deza–Laurent; Caprara–Letchford (2003).
- **Literature:** the post-2012 hypermetric literature, and full texts of the
  citing works. Whether the Voronoi-cell or CVP-verification hardness appears
  explicitly somewhere, which the note calls "probably folklore", is still
  open.
- **Running-time claims:** the `r^{O(r)}` (Kannan) and `2^{O(r²)}`
  (LLL + Fincke–Pohst) bounds in Theorem 3 are accepted by citation. My test
  covers only the reduction to rank-`r` CVP.
- **Polynomial-size claims:** the bounds in Lemma 4 and Theorem 2 are verified
  by proof reading only. The tests check the structural identities they rely
  on, not bit lengths.
- **Scale of the tests:** all numerical checks are finite and small (orders up
  to 12). They support the proofs; they do not replace them.
