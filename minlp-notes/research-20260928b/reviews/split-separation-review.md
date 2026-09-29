# Review: NP-hardness of separating split inequalities for integer QP

Target: `research-20260928b/scouting/open-problem-sweep.md`, Sections 0.1
(item 1), 2.1 and 3.1, and the scout script
`scouting/open-problem-sweep/split_separation_check.py`. Date: 2026-09-28.
Reviewer: independent adversarial review; I did not write the material and
did not edit the scout report. My scripts, logs and fetched source texts
are in [`split-separation/`](split-separation/). No scout code was reused.

## Verdict summary

| Claim | Verdict | Main point |
|---|---|---|
| Definition and restatement (§0.1 item 1) | correct | Matches Buchheim–Traversi (B–T) (5) and (7), de Meijer et al. (4.10), and Burer–Letchford Prop. 11. |
| Lemma A (lattice form) | correct | Holds for `Y ⪰ 0` with any real factor `Y = BᵀB`. A cleaner form holds for every symmetric `Y` (§2). |
| Lemma B (CLOSER is NP-hard) | correct | Every case checks. `M ≥ 3` can be relaxed to `M² ≥ γ² − n`. The existence of a rational `γ` is true but should be made explicit, or avoided by working with Gram matrices (§3). |
| Lemma C (embedding into `Y ≻ 0`, `Y₀₀ = 1`) | correct | Needs `t ≠ 0` so that `h > 0`. This is Kannan's embedding technique with the target doubled. The threshold `8h² ≥ ‖t‖²` is sharp (§4). |
| Consequence: NP-hard for rational positive definite `Y` | correct | It can be strengthened at no cost: **NP-complete**, **strongly NP-hard**, and NP-hard even for splits with `v ∈ {0,1}ⁿ⁺¹` (§5). |
| "membership not yet proved" | **too cautious** | Membership in NP is short for every rational `Y`, not only PSD `Y` (§5.1). |
| Attack plan item 3 (exact separation for `v ∈ {−1,0,1}ⁿ⁺¹`) | **not possible unless P = NP** | The reduction's violated splits already have 0/1 coefficients (§5.3). Fixed support size is polynomial. |
| Attack plan item 2 (hardness of approximating the maximum violation) | immediate | Any multiplicative approximation separates 0 from a positive value (§5.4). |
| Fixed-rank FPT sketch | correct | Details and a rank-1 closed form are in §6. The observation is routine. |
| Attribution "Burer–Letchford conjecture" | **needs a qualifier** | Their 2011 preprint poses the question without conjecturing NP-hardness. B–T (2013) call it a conjecture of Burer and Letchford. The published 2014 version was not checked. |
| Novelty | MINLP statement new as far as checked; lattice core standard | No source settles split separation. The techniques are van Emde Boas's CVP reduction and Kannan's embedding. I found no explicit statement of the lattice core, but it is probably folklore. The binary analogue (hypermetric or gap-1 separation) is still open and is **not** settled by this reduction (§8). |
| Worth a short note? | yes | A short note is justified if it includes the upgrades in §5 and states the priority caveats (§9). |

Exact checks: 0 mismatches on 590 subset-sum instances under six valid
parameter choices, 1,500 random CLOSER instances (Lemma C) and 400 exact
cover instances. Negative controls fail as predicted when each hypothesis
is violated. Details are in §7.

## 1. Definitions (task 1)

Sources read in full text for the relevant parts:

- B–T, Optimization Online 2013/07/3953, pp. 1–10 (local text in the
  scout folder).
- de Meijer–Piccialli–Sotirov–Sudoso, arXiv:2603.28979v1, §4, pp. 10–12.
- Burer–Letchford, Optimization Online 2011/09/3172. This is the original
  September 2011 preprint, obtained through the Wayback Machine:
  §5.2 Prop. 11, §3.2 and §8.
- Galli–Letchford 2021 (local), eq. (10).

The definition agrees in all four sources. For `v ∈ ℤⁿ⁺¹` with
`v = (−s−1, w)`, the split disjunction `(wᵀx ≤ s) ∨ (wᵀx ≥ s+1)` gives the
valid inequality `(wᵀx − s)(wᵀx − s − 1) ≥ 0`. Linearized, this is
`⟨v(v+e₀)ᵀ, X⟩ ≥ 0` (B–T (5), de Meijer (4.10)). This is identical to
Galli–Letchford (10), `wᵀYw ≥ (2s+1)wᵀx − s(s+1)`. The separation problem
is B–T (7): given rational symmetric `X*` with `X*₀₀ = 1`, find
`v ∈ ℤⁿ⁺¹` with `vᵀX*v + vᵀX*e₀ < 0`. B–T state explicitly that "X* can be
an arbitrary symmetric matrix with X*₀₀ = 1". The scout's restatement is
exact.

Status in the sources:

- B–T p. 3: "we agree with the conjecture of Burer and Letchford [8] that
  this separation problem is NP-hard."
- B–T p. 8: "As mentioned by Letchford [11], it is unclear whether the
  separation of split inequalities is an NP-hard problem or not."
- Burer–Letchford 2011 preprint, §8: "Another important question is
  whether the separation problem for the split inequalities can be solved
  in polynomial time." In this version it is a question, not a conjecture.
  The same paper notes (§3.2) that the CVP is strongly NP-hard, so the
  authors knew that convex integer QP is hard.
- de Meijer et al. p. 11: "it is unclear whether the separation of split
  inequalities is an NP-hard problem or not."

## 2. Lemma A

For every symmetric `Y` and `v ∈ ℤⁿ⁺¹`,

`q(v) := ⟨v(v+e₀)ᵀ, Y⟩ = vᵀYv + vᵀYe₀ = ¼[(2v+e₀)ᵀY(2v+e₀) − Y₀₀]`,

and `q(v) = q(−v−e₀)`. Hence the split closure is

`SC = {Y : uᵀYu ≥ Y₀₀ for all u ∈ e₀ + 2ℤⁿ⁺¹}`.

This is the matrix form of "(odd integer)² ≥ 1". If `Y = BᵀB`, this gives
Lemma A: `q(v) = ‖Bv + b₀/2‖² − ‖b₀/2‖²`. So a split is violated if and only
if some lattice point is strictly closer to `−b₀/2` than 0 is. Equivalently,
`b₀` is not a shortest vector of its coset `b₀ + 2L`, where `L = Bℤⁿ⁺¹`. In
Voronoi terms, `b₀/2` lies outside the Voronoi cell of `L`, so `b₀` is not
even weakly Voronoi-relevant. All identities were checked exactly on 300
random rational instances.

Correction: say "for `Y ⪰ 0`". The factor `B` may be irrational; the lemma
does not need it to be rational.

## 3. Lemma B, line by line

The setting is subset sum with `a ∈ ℤⁿ₊` and target `s`. The lattice
basis is `b_i = (M a_i, 2e_i, 0)` and `g = (M s, 𝟙, γ)`, with target
`t₀ = (M s, 𝟙, 0)`. For `P(x,k) = Σ x_i b_i + k g`,

`‖t₀ − P‖² = M²((1−k)s − aᵀx)² + ‖(1−k)𝟙 − 2x‖² + k²γ²`.

This identity is correct. The cases:

- **k = 0.** The middle term is a sum of odd squares, so it is at least
  `n`, with equality if and only if `x ∈ {0,1}ⁿ`. If `x ∉ {0,1}ⁿ`, some
  odd square is at least 9, so the value is at least `n + 8`. If
  `x ∈ {0,1}ⁿ` and `aᵀx ≠ s`, the first term is at least `M²`. Correct.
- **k even, k ≠ 0.** `1 − k` is odd, so the middle term is at least `n`,
  and `k²γ² ≥ 4γ²`. The value is at least `n + 4γ² > γ²`. Correct.
- **k odd.** The value is at least `k²γ² ≥ γ²`. Equality needs `k = ±1`:
  `k = 1, x = 0`, or `k = −1, x = 𝟙` when `aᵀ𝟙 = 2s`. Neither is strict.
  Correct.
- **Conclusion.** The minimum is `n < γ²` if the instance is solvable. It
  is at least `min(n + 8, n + M², γ²) ≥ γ²` otherwise. The lattice point
  `g` is at distance exactly `γ`. Translating by `g ∈ L` gives
  `t = (0, 0, −γ)` with `‖t‖ = γ`. Correct.
- **Strictness.** The reduction needs `γ² > n` (solutions strictly closer)
  and `M² ≥ γ² − n` and `γ² ≤ n + 8` (non-solutions not strictly closer).
  The stated `M ≥ 3` is sufficient because `M² ≥ 9 > 8`. It is not
  necessary: `M = 1` works with `γ² = n + 1`, and this was checked
  exactly (§7).
- **Existence of γ.** The claim is true, but the report gives no
  construction. One explicit choice: `c = ⌊√n⌋ + 1` and
  `γ = (c + n/c)/2`. Then `γ² − n = (c² − n)²/(4c²) ∈ (0, 9/4]`. A simpler
  route avoids rational `γ` entirely. Output the Gram matrix, which
  involves only `γ²` and `h²`. For example, take `γ² = n + 1` and
  `h² = γ²`. Then `Y = G / (8(n+1))` with `G` an integer matrix. This is
  what my scripts do.
- **Encoding size.** The entries are `M²a_ia_j + 4δ_ij`, `M²a_is + 2` and
  `M²s² + n + γ²`, all of polynomial bit length. This gives weak
  NP-hardness, because subset sum is only weakly NP-hard. §5.2 gives the
  strong version.
- **Independence.** `g` is the only vector with a nonzero `γ` coordinate,
  and the `2e_i` blocks make the `b_i` independent. So `C` is a basis, as
  CLOSER requires.

## 4. Lemma C, line by line

- `b₀ = (2t, 2h)` and `b_j = (c_j, 0)`, with `Y = BᵀB/‖b₀‖²`. Then
  `Y₀₀ = 1`. `Y` is rational when `C`, `t` and `h` are rational (or when
  only `h²` is rational, in the Gram form).
- **Positive definiteness** needs linearly independent `c_j` (true, since
  `C` is a basis) and `h ≠ 0`. The choice `h = ‖t‖₁` is positive only
  for `t ≠ 0`. The instance from Lemma B has `t ≠ 0`. The general lemma
  should state `t ≠ 0`; CLOSER with `t = 0` is trivially "no".
- `Bv + b₀/2 = ((2v₀+1)t + ℓ, (2v₀+1)h)` with `ℓ = Σ_{j≥1} v_j c_j`.
  Correct. Dividing by `‖b₀‖²` does not change the sign of `q`, because
  `q` is linear in `Y`.
- **|2v₀+1| ≥ 3.** The squared norm is at least
  `9h² ≥ ‖t‖² + h² = ‖b₀/2‖²`, so there is no violation. Correct. The
  boundary `8h² = ‖t‖²` still works, and my check confirms it. The
  threshold is sharp. If `8h² < ‖t‖²`, the lemma fails whenever `3t ∈ L`
  and CLOSER is "no": take `v₀ = 1` and `ℓ = −3t`. For example, with
  `L = ℤ` and `t = 1/3`, CLOSER is "no", but `h² = ‖t‖²/9` produces a
  violated split.
- **2v₀+1 = ±1.** The condition becomes `‖±t + ℓ‖ < ‖t‖`. Since `−ℓ ∈ L`,
  both signs are equivalent to CLOSER. Correct.
- **Known technique.** Appending the (doubled) target as a new basis
  vector with an extra coordinate is Kannan's embedding. The parity of
  `u₀ = 2v₀ + 1` rules out `u₀ = 0`. This is why the problem stays a CVP
  (which is deterministically NP-hard) rather than an SVP, for which
  deterministic NP-hardness in ℓ₂ is still open.

## 5. Consequences and upgrades

### 5.1 NP membership (the report says "not yet proved")

Membership is short, for all rational symmetric `Y` with `Y₀₀ = 1`.

- **Y ≻ 0.** A violating `v` gives `u = 2v + e₀` with `uᵀYu < 1`. Hence
  `u_i² ≤ (Y⁻¹)_ii`, which has polynomial encoding size (Cramer's rule).
  So `v` itself is a polynomial-size certificate.
- **Y not PSD.** Symmetric Gaussian elimination finds, in polynomial time,
  a rational `z` of polynomial size with `zᵀYz < 0`. Scale `z` to an
  integer vector and take `v = Nz` with `N > |zᵀYe₀|/|zᵀYz|`. This also
  repairs a small gap in B–T's proof of their Theorem 5, which says that
  an eigenvector "has polynomial encoding length". Eigenvectors of
  rational matrices are generally irrational.
- **Y ⪰ 0 singular.** Use `Y = PᵀGP` as in §6. A violating `u` gives
  `w = Pu` with `wᵀGw < 1`. So `w` is bounded, lies in a lattice with
  bounded denominators, and has polynomial size. The system
  `u ∈ e₀ + 2ℤⁿ⁺¹, Pu = w` has an integer solution, so it has one of
  polynomial size (Schrijver, *Theory of Linear and Integer Programming*,
  Cor. 5.3c).

Therefore split separation is **NP-complete**, and it stays NP-complete
for positive definite input.

### 5.2 Strong NP-hardness (report: future work)

Replace subset sum with exact cover by 3-sets. The universe is `U` with
`|U| = 3q` and the sets are `S_1, …, S_m`. Take `b_j = (Mχ_{S_j}, 2e_j, 0)`,
`g = (M𝟙_U, 𝟙_m, γ)` and `γ² = m + 1`. The case analysis of §3 carries
over line by line. Only the first term changes, to
`M²‖(1−k)𝟙_U − Σ x_jχ_{S_j}‖²`. All Gram entries are integers bounded by
`O(m + q)`, over the common denominator `8(m+1)`. So the problem is
strongly NP-hard. This was checked exactly on 400 random instances with
`q ∈ {2, 3}` and `m ≤ 7`.

### 5.3 Restricted families

In a solvable instance, the violated splits are exactly `(−1, x, −1)` and
`(0, −x, 1)`, one pair for each solution `x`. Each pair defines the same
inequality under `v ↦ −v − e₀`. This was checked exactly on all 590
instances.

- After flipping the signs of the basis vectors `b_i`, the violated split
  becomes `v = (0, x, 1) ∈ {0,1}ⁿ⁺²`. So separation restricted to
  0/1-coefficient splits of unbounded support is NP-hard.
- This family is the one de Meijer et al. extend "to three or more
  indices" after (4.11). Attack plan item 3 ("exact separation for
  `v ∈ {−1,0,1}ⁿ⁺¹`") is therefore impossible unless P = NP.
- What *is* polynomial is a fixed support size `k`: enumerate the `O(nᵏ)`
  supports and solve a `(k+1)`-dimensional integer QP (Lenstra/Kannan) or
  apply the non-PSD argument.
- The bounded-support promise version (§3.1 "padding") follows directly.
  Subset sum stays NP-hard when every solution has exactly `n/2` ones, via
  the standard offset `a_i + N`, `s + (n/2)N`. Then every violated `v` has
  support `n/2 + 2`.

### 5.4 Approximation

In "no" instances the maximum violation is 0; in "yes" instances it is
positive. So no multiplicative approximation of the maximum violation is
possible unless P = NP. Additive versions depend on the scaling and are
not meaningful without a normalization.

### 5.5 Location of hard instances

As `h → ∞`, `Y → e₀e₀ᵀ = ℓ(0)`, while the set of violated splits does not
change. So hard instances can be placed arbitrarily close to a vertex of
`IQₙ`. There they satisfy any finite family of valid inequalities that
hold strictly at `ℓ(0)`, for example McCormick/RLT inequalities for boxes
with `l < 0 < u`, ternary triangle inequalities, and `Yᵢᵢ ≤ 1`. The
report's remark "other RLT or triangle constraints are not controlled" is
too pessimistic for such constraints. Constraints that are tight at
`ℓ(0)` are genuinely not controlled. Examples are McCormick inequalities
with `l = 0`, and the binary equality `diag(Y) = Y₀,·`, which fails
because `Y₀ᵢ = 0 < Yᵢᵢ` for the `b_i`.

## 6. Fixed-rank sketch

Each step is correct.

- `q(v + z) = q(v)` for `z ∈ ker Y`.
- For rational `Y ⪰ 0` of rank `r`, take `P` as `r` independent rows of
  `Y` and `G = (PPᵀ)⁻¹PYPᵀ(PPᵀ)⁻¹`. Then `Y = PᵀGP` with `G` rational and
  positive definite. Checked exactly on 100 random instances.
- `Λ = Pℤⁿ⁺¹` is a rank-`r` lattice, and a basis comes from a Hermite
  normal form in polynomial time.
- With `w₀ = Pe₀`, a split is violated if and only if
  `∃ w ∈ Λ: ‖w + w₀/2‖_G < ‖w₀/2‖_G`. This is exact CVP in dimension `r`
  under a rational form. It can be solved exactly with rational Gram
  arithmetic in `r^{O(r)}·poly` time (Kannan) or `2^{O(r)}·poly` time
  (Micciancio–Voulgaris).

Add that non-PSD input is handled in polynomial time (§5.1), so the whole
problem is FPT in `rank(Y)`. There is also a closed form for rank 1: if
`Y = ppᵀ/p₀²` with `p ∈ ℤⁿ⁺¹`, a split is violated if and only if
`|p₀| ≥ 2·gcd(p)`. This follows because `q = m(m + p₀)/p₀²` with
`m ∈ gcd(p)ℤ`. I checked the reduced rank-`r` test against a direct box
search on 300 random instances of rank 1–2, and it agreed on all of them.
The observation is routine: it is the usual reduction of a convex integer
QP of rank `r` to an `r`-dimensional lattice problem.

## 7. Computational checks (independent, exact)

All arithmetic uses `fractions.Fraction`. The separation oracle is
**complete**, not a box search. It enumerates every `u ∈ e₀ + 2ℤⁿ⁺¹` with
`uᵀYu < Y₀₀` by exact Fincke–Pohst enumeration over a rational `LDLᵀ`
factorization (`exact_lattice.py`). The oracle was itself cross-checked
against a provably sufficient box `|u_i| ≤ √(Y₀₀(Y⁻¹)_ii)` on 148 random
positive definite matrices.

| Check | Instances | Result |
|---|---|---|
| Identities of §2 and Lemma A | 300 random rational | all hold |
| Scout's instances `a = (3,5,7)` | 8 | reproduced exactly: minimum violation `−1/32` for `s ∈ {8, 10, 15}`, no violation otherwise |
| Lemmas B+C with `M = 3`, `γ² = n+1`, `h² = γ²` | 590 (`n ≤ 4`; all multisets `a ∈ {1..5}ⁿ` for `n ≤ 3`, 60 random with `n = 4`; `s` from 0 to `Σa + 1`) | 0 mismatches; violated set = predicted set; minimum `q = (n − γ²)/(4γ² + 4h²)` |
| Same, with `γ² = n+8`; `γ² = n+1/7` and `8h² = γ²`; `h² = 1000γ²`; `M = 2, γ² = n+4`; `M = 1, γ² = n+1` | 590 each | 0 mismatches |
| Negative controls: `γ² = n`; `γ² = n+9`; `M = 2, γ² = n+8`; `h² = γ²/100` | 590 each | 315, 144, 243 and 44 mismatches, as expected. `h² = γ²/9` happened to give 0, which is consistent because the condition is only sufficient. |
| Lemma C alone, random `C` (1–3 vectors in `ℤ^{1..3}`), rational `t` | 1,500 (1,151 yes / 349 no) | 0 mismatches for `h = ‖t‖₁` and for `8h² = ‖t‖²`; every violator has `v₀ ∈ {0, −1}`; `h² = ‖t‖²/80` gives 61 mismatches |
| Exact cover by 3-sets (strong variant) | 400 (74 yes) | 0 mismatches; largest Gram entry 96 |
| 0/1 splits (§5.3) | 590 | the violated 0/1 splits are exactly `(0, x, 1)` for solutions `x` |
| Fixed rank: `Y = PᵀGP`; reduced CVP versus box search; rank-1 closed form | 100; 300 | all agree |

## 8. Novelty and priority (task 3)

### 8.1 The MINLP question

No source examined settles it.

- de Meijer et al. (March 2026) still call it unclear.
- Semantic Scholar lists 12 citing papers for B–T 2015, 5 for Letchford
  2010 and 3 for Burer–Letchford 2014; the last list is known to be
  incomplete. None of the titles suggests a complexity result.
- I checked the text of Park–Boyd (arXiv:1510.06421), Wang–Alidaee
  (arXiv:2409.14176) and Galli–Letchford 2021 (local). Galli–Letchford
  refers to B–T for separation and gives no complexity result.

### 8.2 The lattice core

CLOSER is the complement of membership in the closed Voronoi cell. It is
also "CVP verification" with the candidate 0. Its NP-hardness follows from
the textbook subset-sum proof of CVP hardness (van Emde Boas 1981;
Micciancio–Goldwasser, Thm 3.1) by adding a lattice point exactly at the
threshold distance. Lemma C is Kannan's embedding.

The form actually needed for split separation is narrower: "is a given
basis vector `b₀` a shortest vector of `b₀ + 2L`", that is, weak Voronoi
relevance. I found no explicit hardness statement for either form in:

- Dutour Sikirić–Schürmann–Vallentin, arXiv:0804.0036 (#P-hardness of
  counting Voronoi vertices only);
- Hunkenschröder–Reuland–Schymura, arXiv:1811.08532;
- Bonifas–Dadush, arXiv:1412.6168;
- Micciancio–Voulgaris, ECCC TR10-014;
- Micciancio's UCSD CSE 206A lecture notes (sp14 and fa17);
- Kreuzer–Nipkow, arXiv:2306.08375 (an Isabelle formalization of the
  CVP/SVP ℓ∞ reductions; a possible template for the formalization plan).

The core is probably folklore, and a note should say so and cite the
standard techniques. It should not claim a new lattice result.

### 8.3 The binary analogue, which is still open

For points with binary structure (`Yᵢᵢ = Y₀ᵢ`), the covariance map sends
the split `(w, s)` to the cut-polytope inequality
`Σ bᵢbⱼdᵢⱼ ≤ (σ² − 1)/4` with `b = (σ − Σw, w)` and odd `σ = 2s + 1`. This
is Avis's k-gonal inequality (1) with odd `σ`. Splits with `v₀ ∈ {0, −1}`
(`σ = ±1`) are exactly the hypermetric inequalities. The family also
contains the gap-1 inequalities, which are the switchings of the
hypermetric inequalities. The complexity of hypermetric and gap-1
separation is stated as unknown by:

- Avis–Grishukhin 1993: "We are not able to prove that P1 is NP-hard";
- Avis 2003: "Its complexity status is unknown";
- Galli–Kaparis–Letchford 2011/2012: "the complexity of separation for
  the remaining inequalities … is unknown".

Geometrically, hypermetric separation asks whether the circumsphere of a
lattice simplex is empty. That is a Delaunay test, in which all basis
vectors lie on the sphere. General split separation asks whether the
sphere with diameter `[0, −b₀]` is empty, with no condition on the other
basis vectors. The reduction here uses exactly that freedom, since
`Y₀ᵢ = 0 < Yᵢᵢ`. So it does **not** settle the max-cut question.

A note should say this, both to avoid overclaiming and because an
extension to the binary case would be a much stronger result. I did not
search the post-2012 hypermetric literature.

### 8.4 What could not be checked

- The WebSearch quota was exhausted. DuckDuckGo blocked automated queries
  after the first one, and Semantic Scholar rate-limited some calls.
- Not reached: Letchford's IPCO 2010 paper; the published versions of
  Burer–Letchford (Math. Program. 2014) and B–T (Discrete Optim. 2015);
  the Micciancio–Goldwasser book; Deza–Laurent (1997) §28; Agrell et
  al. 2002; Guruswami–Micciancio–Regev 2005; Montenegro's 2017 thesis.
- The claim "Burer–Letchford conjectured NP-hardness" therefore rests on
  B–T's wording. The 2011 preprint only asks the question.

## 9. Does the result deserve a short note?

Yes, as a short note, for example in Operations Research Letters or as a
Discrete Optimization short communication. Recommended content:

1. The parity reformulation `SC = {Y : min_{u ∈ e₀+2ℤⁿ⁺¹} uᵀYu ≥ Y₀₀}`
   and its geometric reading (weak Voronoi relevance of `b₀`).
2. NP-completeness in general, strong NP-hardness for positive definite
   `Y`, and NP-hardness for 0/1 splits of unbounded support. This last
   point bears directly on the multi-index split families used in
   practice.
3. Polynomial time for non-PSD input, fixed support, and fixed rank (FPT),
   with the rank-1 closed form.
4. The priority paragraph of §8, including the open binary analogue.

The contribution is a clean answer to a question posed three or four
times since 2010. Its technical depth and solver impact are modest. The
main value for solvers is §5.3: exact separation of `{0, ±1}` multi-index
splits is intractable in general, so heuristic or bounded-support
separation is justified.

## 10. Corrections to apply to the scout report

1. §3.1 "Likely answer": replace "membership not yet proved" with the
   §5.1 argument; the problem is NP-complete.
2. Lemma A: add "for `Y ⪰ 0`"; optionally add the parity identity.
3. Lemma B: give an explicit `γ` (§3) or switch to the Gram form. State
   the actual condition `M² ≥ γ² − n`.
4. Lemma C: add `t ≠ 0`.
5. Attack plan item 3: exact separation over `v ∈ {−1,0,1}ⁿ⁺¹` is
   NP-hard (§5.3). Replace it with "fixed support size" and "fixed rank".
6. Attack plan items 1–2: strong NP-hardness, NP membership, the
   bounded-support promise and multiplicative inapproximability are done
   (§5).
7. §2.1 and §0.1: qualify the attribution. Burer–Letchford (2011
   preprint) posed the question, and B–T (2013) attribute an NP-hardness
   conjecture to them.
8. §2.1 "Caution": add the open binary analogue (§8.3).
9. §3.1 "Other RLT or triangle constraints are not controlled": refine as
   in §5.5.

## Checks actually run

These are targeted checks only. No project-wide verification was run and
CI was not inspected.

- `python3 check_reduction.py` in `reviews/split-separation/`: about 9 s.
  Output is in `check_reduction.log`.
- `python3 check_lemmaC_x3c_rank.py`: about 60 s. Uses `sympy` for rank
  and the Hermite normal form. Output is in `check_lemmaC_x3c_rank.log`.
- `python3 check_restricted_families.py`: output is in
  `check_restricted_families.log`.
- The scout's `python3 split_separation_check.py` was rerun and its output
  matches §3.1 of the report.
- Source texts fetched for this review (Burer–Letchford 2011 preprint,
  Galli–Kaparis–Letchford 2011 preprint, Avis 2003, Avis–Grishukhin 1993)
  are saved in `split-separation/sources/`.
