# Separating split inequalities for integer quadratic programming is NP-complete

Date: 2026-09-28. Status: complete proofs, re-derived independently from the
first-pass result in the [open-problem sweep](../scouting/open-problem-sweep.md)
(§2.1, §3.1) and the [independent review](../reviews/split-separation-review.md).
The exact-arithmetic checks are in
[`check_split_separation.py`](check_split_separation.py) (§10). The note has not
been refereed or formalized. §9 lists the corrections it makes to the scout
report and the review. A fresh
[final review](../reviews/split-final-review.md) found no mathematical errors,
and a [recheck of Corollaries 3 and 5](../reviews/split-cor5-recheck.md) found
one overstated optimality claim. §11 lists the revisions made in response
(2026-09-29).

## Summary

Split inequalities for integer quadratic programming are the linear
inequalities `⟨v(v+e₀)ᵀ, X⟩ ≥ 0`, `v ∈ ℤⁿ⁺¹`, on the lifted matrix `X ≈ (1,x)(1,x)ᵀ`.
Their separation problem takes a rational symmetric `X*` with `X*₀₀ = 1` and asks
for some `v ∈ ℤⁿ⁺¹` with `⟨v(v+e₀)ᵀ, X*⟩ < 0`. Burer and Letchford asked whether
this can be done in polynomial time. Buchheim and Traversi call NP-hardness a
conjecture of Burer and Letchford, and de Meijer et al. (2026) still call the
question unclear. This note proves the following.

1. Split separation is **NP-complete**. It is NP-complete in the strong sense
   (Theorems 1 and 2, Corollary 1).
2. It stays NP-hard for rational **positive definite** `X*` with `X*₀₀ = 1`.
   It also stays NP-hard when only splits with `v ∈ {0,1}ⁿ⁺¹` are allowed. So
   no polynomial-time algorithm can separate exactly over a bounded-coefficient
   family that contains these 0/1 splits, unless P = NP (Corollary 2).
   Strong NP-hardness also holds at points that satisfy de Meijer et al.'s
   ternary SDP relaxation (4.1) (without linear constraints) and every cut
   family their branch-and-bound separates: triangle (2.1)–(2.2), pair
   (2.3), 1- and 2-index split (4.3) and (4.11)–(4.12), odd-set (4.4) and RLT
   (4.5)–(4.8) inequalities (Corollary 5).
3. Unless P = NP, no polynomial-time algorithm approximates the maximum
   violation within any multiplicative factor. Approximating it within an
   additive error below `1/(N+7)`, for inputs of order `N`, is strongly
   NP-hard (Corollary 3).
4. Some cases are tractable. Non-PSD points are separated in polynomial time
   (Lemma 4). Separation is fixed-parameter tractable in `rank X*` (Theorem 3)
   and polynomial for each fixed support size (Corollary 4). A rank-1 point is
   `X* = ℓ(x)`; it violates a split if and only if `x ∉ ℤⁿ`, and its maximum
   violation is `⌊D²/4⌋/D²`, where `D` is the least common denominator of `x`
   (Theorem 4).

**Novelty caveat.** The lattice core is the standard textbook reduction from
subset sum to the closest vector problem (CVP), combined with Kannan's
embedding. CVP was first shown NP-hard by van Emde Boas (1981). The core is
probably folklore, and this note claims no new lattice result. No source
examined settles split separation (§7). The binary analogue (hypermetric,
gap-1 and rounded psd separation for max-cut) remains open. This note does not
settle it (§6).

## 1. Problem, sources and attribution

Indices run from 0. `e₀` is the first unit vector, `ℓ(x) = (1,x)(1,x)ᵀ`, and
`IQₙ = cl conv{ℓ(x) : x ∈ ℤⁿ}`. A split disjunction `(wᵀx ≤ s) ∨ (wᵀx ≥ s+1)`
with `w ∈ ℤⁿ`, `s ∈ ℤ` gives the valid inequality `(wᵀx − s)(wᵀx − s − 1) ≥ 0`.
With `v = (−s−1, w)`, its linearization is

`q_X(v) := ⟨v(v+e₀)ᵀ, X⟩ = vᵀXv + vᵀXe₀ ≥ 0`.

This is Buchheim–Traversi (B–T) (5)–(6), de Meijer et al. (4.9)–(4.10), and
Burer–Letchford Prop. 11 (up to their sign convention for `s`). Each
`v ∈ ℤⁿ⁺¹` comes from exactly one pair `(w, s)`. The vectors `v` and `−v−e₀`
give the same inequality, since `(w, s) ↦ (−w, −s−1)` describes the same
disjunction. For `w = 0` the value is `s(s+1) ≥ 0`, so trivial splits are
never violated.

**SPLIT-SEP** (B–T problem (7)). *Input:* a rational symmetric matrix `X`
indexed by `0..n` with `X₀₀ = 1`. B–T note that "X* can be an arbitrary
symmetric matrix with X*₀₀ = 1". *Question:* is there `v ∈ ℤⁿ⁺¹` with
`q_X(v) < 0`? The search version asks for such a `v`. For a family
`𝒱 ⊆ ℤⁿ⁺¹`, SPLIT-SEP(`𝒱`) restricts `v` to `𝒱`.

Attribution, checked against the source texts (in the scout folder and in
`reviews/split-separation/sources/`):

- Letchford (IPCO 2010) introduced the inequalities. B–T (p. 8) write: "As
  mentioned by Letchford [11], it is unclear whether the separation of split
  inequalities is an NP-hard problem or not." Letchford's paper itself was not
  checked.
- Burer–Letchford, September 2011 preprint (Optimization Online 2011/09/3172),
  §8: "Another important question is whether the separation problem for the
  split inequalities can be solved in polynomial time." This is a question;
  the preprint states no conjecture. The published version (Math. Program. 143
  (2014) 231–256) was not checked.
- B–T, Optimization Online 2013/07/3953, p. 3: "we agree with the conjecture of
  Burer and Letchford [8] that this separation problem is NP-hard." So B–T
  attribute an NP-hardness conjecture to Burer and Letchford and adopt it. Their
  Theorem 5 handles non-PSD `X*`. The published version (Discrete Optim. 15
  (2015) 1–14) was not checked.
- de Meijer, Piccialli, Sotirov and Sudoso, arXiv:2603.28979v1 (March 2026),
  §4, p. 11: "it is unclear whether the separation of split inequalities is an
  NP-hard problem or not."

The accurate description is therefore: the question posed by Burer and
Letchford, which Buchheim and Traversi state as Burer and Letchford's
conjecture.

## 2. Parity form

**Lemma 1.** Let `X` be symmetric, `v ∈ ℤⁿ⁺¹` and `u = 2v + e₀`. Then

`q_X(v) = (uᵀXu − X₀₀)/4`  and  `q_X(−v−e₀) = q_X(v)`.

The map `v ↦ 2v + e₀` is a bijection from `ℤⁿ⁺¹` onto
`U := e₀ + 2ℤⁿ⁺¹` = {`u ∈ ℤⁿ⁺¹`: `u₀` odd, `uᵢ` even for `i ≥ 1`}. Under this
map, `v ↦ −v−e₀` becomes `u ↦ −u`. Hence the split closure is

`SCₙ = {X : X₀₀ = 1, uᵀXu ≥ 1 for all u ∈ U}`.

Suppose `X = BᵀB` with columns `b₀, …, bₙ ∈ ℝᵈ`, where `B` need not be
rational, and let `L = Bℤⁿ⁺¹`. The columns may be linearly dependent. For
rational `X`, `L` is still discrete, hence a lattice: `‖Bz‖² = zᵀXz ∈ δ⁻¹ℤ`
for a common denominator `δ` of the entries of `X`, so every nonzero point of
`L` has squared norm at least `1/δ`. Then `v` is violated if and only if
`‖b₀ + 2Bv‖ < ‖b₀‖`. So `X ∈ SCₙ` if and only if `b₀` is a shortest vector of
its coset `b₀ + 2L`. Equivalently, `b₀/2` lies in the closed Voronoi cell of
`L`.

*Proof.* `uᵀXu = 4vᵀXv + 4vᵀXe₀ + X₀₀`, and `−v−e₀` maps to `−u`. Also
`Bu = b₀ + 2Bv`. Finally, `b₀/2` lies in the Voronoi cell if and only if
`‖b₀/2 − ℓ‖ ≥ ‖b₀/2‖` for all `ℓ ∈ L`, that is, `‖b₀ − 2ℓ‖ ≥ ‖b₀‖`. ∎

## 3. NP-hardness

**0/1 EQUATIONS.** *Input:* `A ∈ ℤ^{p×n}` and `b ∈ ℤᵖ`. *Question:* is there
`x ∈ {0,1}ⁿ` with `Ax = b`? With `p = 1` this is SUBSET SUM, which is
NP-complete (Karp 1972). If `A` is the incidence matrix of 3-element subsets
`S₁, …, Sₙ` of a `3q`-element set and `b = 𝟙`, it is EXACT COVER BY 3-SETS
(X3C), which is NP-complete in the strong sense (Garey–Johnson 1979, [SP2]).
Every X3C solution has exactly `q` ones. Write `Aᵢ` for column `i` of `A`.

**Lemma 2 (a strictly closer lattice point).** Let `(A, b)` be an instance
with `n ≥ 1`, and let `γ > 0` satisfy `n < γ² ≤ n + 1`. In `ℝ^{p+n+1}` define

`cᵢ = (Aᵢ, 2eᵢ, 0)` for `i = 1..n`,  `g = (b, 𝟙, γ)`,  `t = (0, 0, −γ)`.

The vectors `c₁, …, cₙ, g` are linearly independent, and `t ≠ 0`. Let `L` be
their lattice. The points `ℓ ∈ L` with `‖t − ℓ‖ < ‖t‖` are exactly
`ℓ = Σ xᵢcᵢ − g` for `x ∈ {0,1}ⁿ` with `Ax = b`. Each of them lies at squared
distance `n` from `t`.

*Proof.* The blocks `2eᵢ` and the last coordinate of `g` give independence.
Write `ℓ = Σ xᵢcᵢ + (m−1)g` with `x ∈ ℤⁿ` and `m ∈ ℤ`. Then

`F(x, m) := ‖t − ℓ‖² = ‖(1−m)b − Ax‖² + ‖(1−m)𝟙 − 2x‖² + m²γ²`,

to be compared with `‖t‖² = γ²`.

- If `m` is odd, then `F ≥ m²γ² ≥ γ²`.
- If `m` is even and nonzero, every entry of `(1−m)𝟙 − 2x` is odd. So
  `F ≥ n + 4γ² > γ²`.
- If `m = 0`, then `F = ‖b − Ax‖² + ‖𝟙 − 2x‖²`. Every entry of `𝟙 − 2x` is
  odd, and all are `±1` exactly when `x ∈ {0,1}ⁿ`.
  - If `x ∉ {0,1}ⁿ`, then `F ≥ n + 8 > γ²`.
  - If `x ∈ {0,1}ⁿ` and `Ax ≠ b`, then `F ≥ n + 1 ≥ γ²`.
  - If `x ∈ {0,1}ⁿ` and `Ax = b`, then `F = n < γ²`. ∎

*Remarks.* This is the standard textbook subset-sum reduction for CVP,
extended to several rows. Regev's lecture notes (Tel Aviv 2004, Lecture 5,
Theorem 2) use the basis `[a; 2I]`, the target `(s, 𝟙)` and the radius `√n`.
They cite van Emde Boas only for SVP in the ℓ∞ norm. CVP was first shown
NP-hard by van Emde Boas (1981); whether his report uses this construction
was not checked.

The textbook reduction uses the vectors `cᵢ` and the target `t₀ = (b, 𝟙, 0)`.
Here the lattice vector `g` is added at distance `γ` from `t₀`, just above
the textbook threshold `√n`. Translating by `g` turns `t₀` into `t` and puts
the lattice point `0` at exactly the threshold distance `‖t‖ = γ`.

The scout scaled the first block by `M`. The admissible window is then
`n < γ² ≤ n + min(8, M²)`, so `M = 1` already works. Theorem 1 uses only `γ²`, so `γ` need not be rational.
If a rational `γ` is wanted, take `c = ⌊√n⌋ + 1` and `γ = (c + n/c)/2`. Then
`γ² − n = (c² − n)²/(4c²)`, which lies in `(0, 1)` because
`0 < c² − n ≤ 2c − 1`.

**Lemma 3 (embedding).** Let `c₁, …, c_k ∈ ℝᵈ` be linearly independent with
lattice `L`. Let `t ∈ ℝᵈ` with `t ≠ 0`, and let `h ∈ ℝ` satisfy
`8h² ≥ ‖t‖²`, so that `h ≠ 0`. Set

`b₀ = (2t, 2h)`,  `bⱼ = (cⱼ, 0)`,  `B = [b₀, b₁, …, b_k]`,  `X = BᵀB/‖b₀‖²`.

Then `X` is positive definite and `X₀₀ = 1`. Let `ℓ := Σ_{j≥1} vⱼcⱼ`. A split
`v ∈ ℤ^{k+1}` is violated if and only if one of the following holds:

- `v₀ = −1` and `ℓ` is strictly closer to `t` than `0` is;
- `v₀ = 0` and `−ℓ` is strictly closer to `t` than `0` is.

In particular, `X` has a violated split if and only if some point of `L` is
strictly closer to `t` than `0` is. The matrix `X` depends only on `h²` and
the Gram matrix of `(t, c₁, …, c_k)`:

`‖b₀‖²·X = [[4‖t‖² + 4h², 2tᵀC], [2Cᵀt, CᵀC]]`, with `‖b₀‖² = 4‖t‖² + 4h²`.

*Proof.* The last coordinate and the independence of the `cⱼ` make the columns
of `B` independent, so `X ≻ 0`. Also `‖b₀‖² > 0` and `X₀₀ = 1`. For
`u = 2v + e₀`, we have `Bu = 2(u₀t + ℓ, u₀h)`. By Lemma 1, `v` is violated if
and only if

`‖u₀t + ℓ‖² + u₀²h² < ‖t‖² + h²`.

If `|u₀| ≥ 3`, the left side is at least `9h² = h² + 8h² ≥ h² + ‖t‖²`, so
there is no violation. If `u₀ = −1` (`v₀ = −1`), the condition is
`‖t − ℓ‖ < ‖t‖`. If `u₀ = 1` (`v₀ = 0`), it is `‖t − (−ℓ)‖ < ‖t‖`. ∎

*The threshold is sharp.* Suppose `8h² < ‖t‖²` and `3t ∈ L`. The split with
`u₀ = 3` (`v₀ = 1`) and `ℓ = −3t` gives left side `9h² < ‖t‖² + h²`. It is
violated whether or not a closer lattice point exists. Example: `L = ℤ`,
`t = 1/3`. No integer is strictly closer to `1/3` than `0`, yet `h² = 1/81`
gives the violated splits `(1, −1)` and `(−2, 1)`. At `h² = 1/72`
(`8h² = ‖t‖²`) there is none.

*The condition `t ≠ 0`.* With `t = 0` the threshold allows `h = 0`, and then
`b₀ = 0` and `X` is undefined. The scout's choice `h = ‖t‖₁` has exactly this
defect at `t = 0`. For `t = 0` the question "is some lattice point strictly
closer to `t` than `0`?" has the trivial answer "no", so assuming `t ≠ 0` loses
nothing. Kannan's embedding appends the target as an extra basis vector with an
extra coordinate. Lemma 3 does the same with the target doubled. Because `u₀`
is odd, `u₀ = 0` cannot occur.

**Theorem 1 (reduction).** Let `(A, b)` be an instance of 0/1 EQUATIONS.
Index an `(n+2)×(n+2)` integer matrix `G` by `0, 1, …, n, g` (so `g = n+1`),
and for `i, j = 1..n` set

```
G₀₀ = 8(n+1)          G₀ᵢ = 0              G₀g = −2(n+1)
Gᵢⱼ = AᵢᵀAⱼ + 4δᵢⱼ     Gᵢg = Aᵢᵀb + 2       Ggg = ‖b‖² + 2n + 1
```

Let `X = G/(8(n+1))`. Then:

- (a) `X` is rational and positive definite, `X₀₀ = 1`, and `X` is computable
  in polynomial time.
- (b) The violated splits of `X` are exactly `v = (0, −x, 1)` and
  `v = (−1, x, −1)` (coordinates ordered `0, 1..n, g`), for `x ∈ {0,1}ⁿ` with
  `Ax = b`. The two vectors for the same `x` describe the same inequality.
- (c) If `Ax = b` has a 0/1 solution, then `min_v q_X(v) = −1/(8(n+1))`.

More generally, choose any rational `h² ≥ (n+1)/8`, replace `G₀₀` by
`4(n+1) + 4h²`, and divide by the new `G₀₀`. Then (a) and (b) still hold, and
the minimum in (c) becomes `−1/(4(n+1+h²))`.

*Proof.* Apply Lemma 2 with `γ² = n+1` and Lemma 3 to its basis
`(c₁, …, cₙ, g)`, its target `t` and `h² = n+1`. The threshold holds because
`8h² ≥ γ² = ‖t‖²`. The resulting vectors are

`b₀ = (0, 0, −2γ, 2h)`,  `bᵢ = (Aᵢ, 2eᵢ, 0, 0)`,  `b_g = (b, 𝟙, γ, 0)`.

Their Gram matrix is `G`, because `γ` and `h` appear only as
`γ² = h² = n+1`. Also `X = G/‖b₀‖²`. Part (a) is Lemma 3.

For (b), write `ℓ = Σ vᵢcᵢ + v_g g`. By Lemma 3, `v` is violated if and only
if either `v₀ = −1` and `ℓ` is strictly closer to `t` than `0`, or `v₀ = 0`
and `−ℓ` is. By Lemma 2, the first case means `(v₁..vₙ, v_g) = (x, −1)`, and
the second means `(v₁..vₙ, v_g) = (−x, 1)`, for a solution `x`.

For (c), the violators have `‖Bu‖² = 4(n + h²)`, by Lemma 2 and the proof of
Lemma 3. So
`q = (‖Bu‖²/‖b₀‖² − 1)/4 = (n − γ²)/(4(γ² + h²))`.
The general-`h` statement follows in the same way. ∎

**Corollary 1.**

- (i) SPLIT-SEP and its search version are NP-hard, even for rational positive
  definite `X` with `X₀₀ = 1`. This follows from SUBSET SUM.
- (ii) They are NP-hard in the strong sense. For X3C instances, every entry of
  `G` is an integer of absolute value at most `max(8(n+1), 3q + 2n + 1)`, and
  the common denominator is `8(n+1)`.
- (iii) *Promise version.* For X3C instances, every violated split has
  `|supp w| = q + 1`. Hence, for each fixed `k`, SPLIT-SEP stays NP-hard under
  the promise that every split with `|supp w| ≤ k` is satisfied. X3C restricted
  to `q ≥ k` is still NP-complete, because instances with `q < k` can be solved
  by enumeration in `O(nᵏ)` time.

**Corollary 2 (0/1 and bounded-coefficient splits).** Let
`D = diag(1, −1, …, −1, 1)` and `X′ = DXD`. Then `X′` is rational and positive
definite with `X′₀₀ = 1`. Because `De₀ = e₀`, `q_{X′}(v) = q_X(Dv)`. So the
violated splits of `X′` are exactly `(0, x, 1)` and `(−1, −x, −1)` for the
solutions `x`.

For each order `N` of the input matrix, let `𝒱` be a family of split vectors
in `ℤᴺ` that contains every 0/1 vector with `v₀ = 0`. For the instances
`X′` (order `N = n + 2`), `X′` has a violated split in `𝒱` if `Ax = b` is
solvable, and has no violated split at all otherwise. So SPLIT-SEP(`𝒱`) is
NP-hard, in the strong sense via X3C, for each of these families:

- `{0,1}ᴺ`, `{−1,0,1}ᴺ`, or `{−K, …, K}ᴺ` for any fixed `K ≥ 1`;
- the multi-index family `{v : v₀ = 0, vᵢ ∈ {0, ±1}}` that de Meijer et al.
  extend "to three or more indices" after their (4.11). Their (4.3) splits
  have `v₀ = −1`; under `v ↦ −v−e₀` these become `v₀ = 0`.

For each such family, membership in NP is trivial, so the restricted problem
is NP-complete. Exact polynomial-time separation over a bounded-coefficient
family containing these splits is impossible unless P = NP. A fixed bound on
the support, by contrast, gives a polynomial problem (Corollary 4).

**Corollary 3 (approximation).** Let
`μ(X) := max{0, sup_v (−q_X(v))}`. It is `+∞` for non-PSD `X` and is attained
for `X ≻ 0`. Let `N` be the order of the input matrix. Modify Theorem 1 by
scaling the first block by `M = 3` and taking `γ² = n + 8` and `h² = 1`. The
vectors are

`b₀ = (0, 0, −2γ, 2)`,  `bᵢ = (3Aᵢ, 2eᵢ, 0, 0)`,  `b_g = (3b, 𝟙, γ, 0)`,

and their Gram matrix is the integer matrix

```
G₀₀ = 4n + 36          G₀ᵢ = 0               G₀g = −2(n+8)
Gᵢⱼ = 9AᵢᵀAⱼ + 4δᵢⱼ     Gᵢg = 9Aᵢᵀb + 2       Ggg = 9‖b‖² + 2n + 8
```

Then `X = G/G₀₀` is rational and positive definite, `X₀₀ = 1`, and its
violated splits are exactly those of Theorem 1(b). Here `N = n + 2`, so
`μ(X) = 0` if `Ax = b` has no 0/1 solution, and otherwise

`μ(X) = 2/(n+9) = 2/(N+7)`.

Hence, unless P = NP, and in the strong sense via X3C:

- for no `ρ ≥ 1`, even one depending on the input, does a polynomial-time
  algorithm approximate `μ` within a factor `ρ`;
- no polynomial-time algorithm approximates `μ` within an additive error below
  `1/(N+7)`.

*Proof.* There are three steps.

1. **Lemma 2 with `M = 3`.** Set `cᵢ = (3Aᵢ, 2eᵢ, 0)`, `g = (3b, 𝟙, γ)` and
   `t = (0, 0, −γ)`. The formula for `F` gains the factor 9:
   `F(x, m) = 9‖(1−m)b − Ax‖² + ‖(1−m)𝟙 − 2x‖² + m²γ²`. The cases of Lemma 2
   go through with `γ² = n + 8`:
   - binary non-solutions give `F ≥ n + 9 > γ²`;
   - non-binary `x` with `m = 0` give `F ≥ n + 8 = γ²`;
   - the cases `m ≠ 0` are unchanged.

   So the points strictly closer to `t` than `0` are again `Σ xᵢcᵢ − g` for
   the solutions `x`, at squared distance `n`.
2. **A sharper threshold for this lattice.** Lemma 3's proof reduces
   violation to `‖u₀t + ℓ‖² + u₀²h² < γ² + h²`, with `u₀ = 2v₀ + 1` odd and
   `ℓ = Σ xᵢcᵢ + kg`. The last coordinate of `u₀t + ℓ` is `(k − u₀)γ`.
   - If `k ≠ u₀`, then `‖u₀t + ℓ‖² ≥ γ²`, and there is no violation.
   - If `k = u₀`, the parity block `2x + u₀𝟙` has only odd entries, so
     `‖u₀t + ℓ‖² ≥ n`. A violation then needs `(u₀² − 1)h² < γ² − n`.

   For `|u₀| ≥ 3` this is excluded whenever `8h² ≥ γ² − n`, here `h² ≥ 1`.
   The cases `u₀ = ±1` do not involve `h`, and positive definiteness needs
   only `h ≠ 0`. So Lemma 3's conclusion holds with `h² = 1`, although the
   generic threshold `8h² ≥ ‖t‖² = γ²` fails.
3. **The value.** For the violators, `‖u₀t + ℓ‖² = n`, so
   `q = (n − γ²)/(4(γ² + h²)) = −8/(4(n + 9)) = −2/(n+9)`.

The Gram entries follow as in Theorem 1. For X3C they are integers bounded by
`O(n + q)`, which gives strong NP-hardness. ∎

*Remarks.*

- The same sharper threshold with `M = 1` and `γ² = n + 1` allows
  `h² = 1/8`, which gives the gap `2/(8n+9) = 2/(8N−7)`. This also shows that
  Theorem 1 holds for every `h² ≥ 1/8`.
- The sharper threshold can be tight. With `M = 1` and three copies of a
  3-element universe (`q = 1`, `A = 𝟙𝟙ᵀ`), `h² = 1/9` creates extra
  violators with `|u₀| = 3`, while `h² = 1/8` does not.
- Within this family of parameters, the gap equals
  `2(γ² − n)/(9γ² − n)` at `h² = (γ² − n)/8`. This increases with `γ²`, and
  the case analysis caps `γ² − n` at 8. The two conditions used, however,
  are sufficient, not necessary. This note makes no claim that `2/(N+7)` is
  the best achievable gap. Whether a constant additive gap is NP-hard is not
  settled here.
- The additive gap is not an artifact of large entries. For X3C instances
  with `n ≥ 14q`, every entry of `X` lies in `[−1, 1]`. The condition can be
  arranged by repeating a set, which does not change the answer. Indeed,
  `G₀₀ = 4n + 36`, while `G_gg = 27q + 2n + 8 ≤ 4n + 36` when `27q ≤ 2n + 28`.
  The other entries are at most `max(31, 29, 27, 2n + 16) ≤ 4n + 36`.
- The corollary says nothing about violations normalized by the size of `v`.

## 4. NP membership and non-PSD points

**Lemma 4 (non-PSD points).** A polynomial-time algorithm does one of two
things for a rational symmetric `X`:

- it certifies `X ⪰ 0` and returns an index set `K` with `X_KK ≻ 0` and
  `|K| = rank X`; or
- it returns a rational `z` of polynomial size with `zᵀXz < 0`.

In the second case, scale `z` to be integral and set `α = zᵀXz < 0`,
`β = zᵀXe₀` and `N = ⌊|β|/|α|⌋ + 1`. Then the split `v = Nz` is violated:
`q_X(Nz) = N(Nα + β) < 0`.

*Proof.* Run symmetric Gaussian elimination with diagonal pivots on the
current Schur complement `S`, which starts as `X`.

1. If some `Sᵢᵢ < 0`, return `eᵢ`.
2. If some `Sᵢᵢ = 0` and `Sᵢⱼ ≠ 0`, return `z` with `zⱼ = 1` and
   `zᵢ = −(Sⱼⱼ + 1)/(2Sᵢⱼ)`. Then `zᵀSz = −1`.
3. Otherwise, if some `Sᵢᵢ > 0`, pivot on it. `S ⪰ 0` if and only if its Schur
   complement `S′ ⪰ 0`. A vector `z′` for `S′` extends to `z` by
   `zᵢ = −S_{i,R}z′/Sᵢᵢ`, and then `zᵀSz = z′ᵀS′z′`.
4. If `S = 0`, then `X ⪰ 0`, and the set `K` of pivots has `X_KK ≻ 0` and
   `|K| = rank X`.

After pivots `K`, the entries of `S` are ratios of minors of `X` (Edmonds
1967; Schrijver 1986, Ch. 3). The returned `z` satisfies `(Xz)_K = 0`. So
`z_K = −X_KK⁻¹X_{K,R}z_R`, where `z_R` has at most two nonzero entries of
polynomial size. By Cramer's rule, `z` has polynomial size. ∎

This also closes a small gap in the proof of B–T's Theorem 5, which says that
an eigenvector for a negative eigenvalue "has polynomial encoding length".
Eigenvectors of rational matrices are generally irrational.

**Theorem 2 (NP membership).** If a rational symmetric `X` with `X₀₀ = 1` has a
violated split, then it has one whose encoding size is polynomial in that of
`X`. Hence SPLIT-SEP is in NP. By Theorem 1 it is NP-complete, also when the
input is restricted to positive definite matrices.

*Proof.* There are three cases.

- **`X` not PSD.** Use Lemma 4.
- **`X ≻ 0`.** Let `v` be violated and `u = 2v + e₀`, so `uᵀXu < 1`. By
  Cauchy–Schwarz for the inner product `aᵀXb`,
  `|uᵢ| = |(X⁻¹eᵢ)ᵀXu| ≤ ((X⁻¹)ᵢᵢ · uᵀXu)^{1/2} < (X⁻¹)ᵢᵢ^{1/2}`. Each
  `(X⁻¹)ᵢᵢ` is a ratio of minors of `X`.
- **`X ⪰ 0` singular, of rank `r`.** Take `K` from Lemma 4 and set
  `P := X_{K,·}` and `G := X_KK⁻¹ ≻ 0`. The Schur complement of `X_KK` in `X`
  is 0, so `X = PᵀGP`. If `u ∈ U` has `uᵀXu < 1`, then `w := Pu` satisfies
  `wᵀGw < 1`. Hence `|wᵢ| < ((G⁻¹)ᵢᵢ)^{1/2} = (X_KK)ᵢᵢ^{1/2}`. Since `u` is
  integral, every entry of `w` has a denominator dividing a common denominator
  of `P`, so `w` has polynomial size. The
  linear Diophantine system `2Py = w − Pe₀` has the integral solution `y = v`.
  Such systems are solvable in polynomial time via the Hermite normal form
  (Kannan–Bachem 1979; Schrijver 1986, Ch. 5), so the system has a solution
  `y′` of polynomial size. Then `u′ = e₀ + 2y′` has `Pu′ = w`, so
  `u′ᵀXu′ = wᵀGw < 1`. ∎

## 5. Fixed rank and fixed support

**Theorem 3 (FPT in the rank).** Let `X` be a rational symmetric matrix with
`X₀₀ = 1` and `r = rank X`. The search version of SPLIT-SEP can be solved in
time `f(r)·poly(size of X)`, with `f(r) = r^{O(r)}`.

*Proof.* If `X` is not PSD, use Lemma 4. Otherwise take `K`, `P` and `G` as in
Theorem 2 and set `w₀ := Pe₀ = X_{K,0}`. Then `w₀ᵀGw₀ = X₀₀ = 1`. For
`u = e₀ + 2v`,

`uᵀXu = ‖w₀ + 2Pv‖²_G`, where `‖y‖²_G := yᵀGy`.

So a split is violated if and only if some `w` in the lattice `Λ := Pℤⁿ⁺¹`
satisfies `‖w + w₀/2‖_G < ‖w₀/2‖_G = 1/2`. Here `Λ` has rank `r`. The Hermite
normal form of `δP`, where `δ` is a common denominator, gives in polynomial
time a basis `W = PT` of `Λ` with `T ∈ ℤ^{(n+1)×r}`. The problem becomes exact
CVP in dimension `r`: is `min_{z∈ℤʳ} ‖Wz + w₀/2‖²_G < 1/4`? Kannan's
algorithm (1987) solves this in `r^{O(r)}·poly` time. It needs only inner
products, so it can run in exact rational arithmetic on the Gram matrix
`WᵀGW`. LLL reduction on the Gram matrix followed by Fincke–Pohst enumeration
gives the weaker `f(r) = 2^{O(r²)}`. Any `z` with value `< 1/4` yields the
violated split `v = Tz`. ∎

The matrices of Theorem 1 have full rank `n + 2`, so Theorem 3 does not
contradict them. For fixed `n` the problem is polynomial, since `r ≤ n + 1`.

**Corollary 4 (fixed support).** For each fixed `k`, SPLIT-SEP restricted to
splits with `|supp w| ≤ k` is polynomial, with no bound on the coefficients.
For each `T ⊆ {1..n}` with `|T| ≤ k`, apply Theorem 3 to the principal
submatrix on `{0} ∪ T`, which has rank at most `k + 1`. This takes `O(nᵏ)`
calls. Together with Corollary 1(iii), this shows that the hardness comes from
unbounded support.

**Theorem 4 (rank one, closed form).** Every rank-1 symmetric `X` with
`X₀₀ = 1` equals `ℓ(x)` with `x = (X₁₀, …, Xₙ₀) ∈ ℚⁿ`. Let `D` be the least
common denominator of `x₁, …, xₙ` and `p = D·(1, x) ∈ ℤⁿ⁺¹`. Then
`gcd(p) = 1`, and for every `v ∈ ℤⁿ⁺¹`, with `m = pᵀv`,

`q_X(v) = m(m + D)/D²`.

Consequently:

- (a) `X` violates a split if and only if `x ∉ ℤⁿ`, that is, `D ≥ 2`. If
  `xᵢ ∉ ℤ`, the elementary split `xᵢ ≤ ⌊xᵢ⌋ ∨ xᵢ ≥ ⌈xᵢ⌉` is violated.
- (b) The maximum violation is `⌊D/2⌋⌈D/2⌉/D² = ⌊D²/4⌋/D² ≤ 1/4`. It is
  attained by any `v` with `pᵀv = −⌊D/2⌋`, which the extended Euclidean
  algorithm finds.
- (c) This is equivalent to the review's form: for any integer vector `p′` with
  `X = p′p′ᵀ/p′₀²`, `X` violates a split if and only if `|p′₀| ≥ 2·gcd(p′)`.

*Proof.* Write `X = λyyᵀ`. Then `λy₀² = X₀₀ = 1`, so `X = X_{·0}X_{0·} = ℓ(x)`.
With `c = (1, x) = p/D`, `q = (cᵀv)² + cᵀv = m(m + D)/D²`.

To see `gcd(p) = 1`, write `xⱼ = aⱼ/dⱼ` in lowest terms. If a prime `π` divides
`D`, it divides some `dⱼ` to the same power as it divides `D`. Then
`Dxⱼ = (D/dⱼ)aⱼ` is not divisible by `π`. So `m` ranges over all of `ℤ`.
`m(m + D) < 0` holds exactly for `−D < m < 0`, which is possible if and only if
`D ≥ 2`. The minimum over integers is at `m = −⌊D/2⌋`.

For (c): `p′ = κp`, and `κ` is an integer because `p` is primitive. So
`gcd(p′) = |κ|` and `|p′₀| = |κ|·D`. ∎

## 6. Where the hard instances lie; the binary analogue

**Remark 1 (hard points near ℓ(0)).** In the general-`h` form of Theorem 1,
the entries of `G` other than `G₀₀` do not depend on `h`. As `h → ∞`,
`X(h) → e₀e₀ᵀ = ℓ(0)`, an extreme point of `IQₙ`, while the set of violated
splits stays the same.

Quantitatively, let `Ĝ := max_{(i,j)≠(0,0)} |Gᵢⱼ|`. Every entry of
`X(h) − ℓ(0)` then has absolute value below `Ĝ/(4h²)`. Consider any valid
inequality `⟨A′, X⟩ ≥ β` that holds at `ℓ(0)` with slack `ε > 0`. `X(h)`
satisfies it, and keeps the violated set of Theorem 1(b), once
`h² ≥ max((n+1)/8, ‖A′‖₁Ĝ/(4ε))`. This bound is polynomial. Since
`Ĝ ≥ |G₀g| = 2(n+1)`, any condition of the form `4h² ≥ cĜ` with `c ≥ 3`
already implies `h² ≥ (n+1)/8`.

For example, `4h² ≥ 3Ĝ` makes those entries smaller than `1/3` in absolute
value. Then `X` satisfies `Xᵢᵢ ≤ 1`, the triangle inequalities (2.1)–(2.2) of
de Meijer et al., and their RLT inequalities (4.5)–(4.8). If also `b ≠ 0`,
then `diag(X) ≥ ±x` holds, since `G_gg − |G₀g| = ‖b‖² − 1`. So `X` is
feasible for their basic ternary SDP relaxation (4.1) without linear
constraints.

Inequalities that are tight at `ℓ(0)` are not controlled by this argument:

- The binary condition `Xᵢᵢ = X₀ᵢ` fails, since `X₀ᵢ = 0 < Xᵢᵢ` for
  `i ∈ [n]`.
- For subset-sum instances, the ternary pair inequalities `|Xᵢⱼ| ≤ Xᵢᵢ` (de
  Meijer (2.3)) often fail. For `a = (1, 6)`, `X₁₂ = 1/4 > X₁₁ = 5/24`. In the
  script they fail on 458 of 610 subset-sum instances. For X3C instances they
  always hold (Corollary 5).

The violation is `1/(4(n+1+h²))`, so it shrinks as the point moves toward
`ℓ(0)`.

**Corollary 5 (hard points inside de Meijer et al.'s ternary relaxation).**
Take an X3C instance `(A, 𝟙)` with `n` sets and universe size `3q`, and the
matrix `X = X(h)` of Theorem 1 in the general-`h` form. Write `x` and `Y` for
the parts of `X` indexed by the variables `{1, …, n, g}`, that is,
`xᵢ = Xᵢ₀` and `Y = X` restricted to those indices. Then
`Ĝ = max(7, 3q + 2n + 1)`, which equals `3q + 2n + 1` unless `q = n = 1`.
Suppose `4h² ≥ max(3, n+1)·Ĝ`. Then `X` is
positive definite with `X₀₀ = 1`, its violated splits are those of
Theorem 1(b), and `X` satisfies all of the following:

- (i) (4.1) without linear constraints: `X ⪰ 0` and
  `|x| ≤ diag(Y) ≤ 1`;
- (ii) the triangle inequalities (2.1)–(2.2);
- (iii) the pair inequalities (2.3): `|Yᵢⱼ| ≤ Yᵢᵢ` for all `i ≠ j`. These
  hold for every `h`;
- (iv) the odd-set inequalities (4.4):
  `Σ_{i<j∈S} vᵢvⱼYᵢⱼ ≥ −⌊|S|/2⌋` for every `S` of odd size and every
  `v ∈ {±1}^S`;
- (v) the RLT inequalities (4.5)–(4.8):
  `sᵢsⱼYᵢⱼ + sᵢxᵢ + sⱼxⱼ ≥ −1` for all `s ∈ {±1}²`.

In particular `Y` lies in their set `M_{n+1}` (2.5). All five families are
invariant under changing the signs of variables, so the flipped matrix `DXD`
of Corollary 2 satisfies them too.

If `q ≥ 2`, then `X` and `DXD` also satisfy the 1- and 2-index split
inequalities (4.3) and (4.11)–(4.12). The reason is that every violated split
has `|supp w| = q + 1 ≥ 3` (Corollary 1(iii)), while these inequalities are
splits with `|supp w| ≤ 2`. X3C with `q ≥ 2` is still strongly NP-complete.
So the points satisfy every cut family used in de Meijer et al.'s
branch-and-bound (their §5–§6): triangle, RLT, the split inequalities
(4.11)–(4.12), the non-standard split inequalities (2.3) and the odd-set
inequalities (4.4). Their basic relaxation (4.1) is satisfied as well. Hence split separation, and split
separation over 0/1 splits, is strongly NP-hard even at positive definite
points that satisfy all of (4.1) without linear constraints, (2.1)–(2.3),
(4.4) and (4.5)–(4.8).

*Proof.* The entries of `G` other than `G₀₀` do not depend on `h`. For
`i ≠ j` among the sets, `Gᵢⱼ = |Sᵢ ∩ Sⱼ| ∈ [0, 3]` and `Gᵢᵢ = 7`. Also
`Gᵢg = |Sᵢ| + 2 = 5`, `G_gg = 3q + 2n + 1 ≥ 6`, `G₀ᵢ = 0` and
`G₀g = −2(n+1)`. Since `3q + 2n + 1 > 2(n+1)`, this gives
`Ĝ = max(7, 3q + 2n + 1)`.

- Since `Ĝ ≥ 2(n+1)`, the assumption gives `h² ≥ (3/2)(n+1) ≥ (n+1)/8`, so
  Theorem 1 applies.
- (iii) For `i ≠ j` in `{1..n, g}`, `|Gᵢⱼ| ≤ 5 ≤ min(Gᵢᵢ, Gⱼⱼ)`. Dividing by
  `G₀₀ > 0` gives (2.3), for every `h`.
- For `(i, j) ≠ (0, 0)`,
  `|Xᵢⱼ| = |Gᵢⱼ|/(4(n+1) + 4h²) < Ĝ/(4h²) ≤ ε := min(1/3, 1/(n+1))`.
- (i) `X ⪰ 0` by Theorem 1(a), and `Yᵢᵢ < 1/3`. For `i ≤ n`, `xᵢ = 0`. At
  `g`, `G_gg − |G₀g| = 3q − 1 > 0`.
- (ii) and (v) Each left side is a sum of three terms of absolute value below
  `1/3`, so it exceeds `−1`.
- (iv) Let `|S| = k` be odd. For `k = 1` the inequality reads `0 ≥ 0`. For
  `k ≥ 3`, `k ≤ n + 1` because `S ⊆ {1..n, g}`, so
  `Σ_{i<j∈S} vᵢvⱼYᵢⱼ > −C(k,2)·ε ≥ −C(k,2)/k = −(k−1)/2 = −⌊k/2⌋`.
- *Strong NP-hardness.* Choose `4h² = max(3, n+1)·Ĝ`. Then
  `G₀₀ = 4(n+1) + max(3, n+1)·Ĝ` is an integer of size `O(n(n + q))`, and
  every entry of `G` is polynomially bounded. X3C is strongly NP-complete. ∎

At the smallest admissible choice `4h² = max(3, n+1)·Ĝ`, the violation is
`1/(4(n+1+h²)) = Θ(1/(n(n+q)))`. It is small, but only polynomially small.

**The binary analogue is open.** Consider `X` with `Xᵢᵢ = X₀ᵢ` for all
`i ∈ [n]`, as in relaxations of binary QP with `diag(X) = x`. Use the
covariance map `d₀ᵢ = X₀ᵢ`, `dᵢⱼ = Xᵢᵢ + Xⱼⱼ − 2Xᵢⱼ`. It turns the split
inequality for `(w, s)` into

`Σ_{0≤i<j≤n} bᵢbⱼdᵢⱼ ≤ (σ² − 1)/4`, with `σ = 2s + 1`,
`b = (σ − Σw, w)` and `Σb = σ`.

*Proof.* Both sides are affine in `X` on
`{X : X₀₀ = 1, Xᵢᵢ = X₀ᵢ}`, and the points `ℓ(x)` with `x ∈ {0,1}ⁿ` affinely
span this set. At `ℓ(x)` with `S = {i : xᵢ = 1}`, the left side is
`b(S)(σ − b(S))` with `b(S) = wᵀx`, which gives equality with the split. ∎

These are the rounded psd inequalities of Galli–Kaparis–Letchford (GKL): odd
`σ(b)`, right-hand side `⌊σ(b)²/4⌋`. The case `σ = ±1` (`v₀ ∈ {0, −1}`) gives
the hypermetric inequalities, and the family also contains the gap-1
inequalities. Their separation complexity is stated as unknown in the
following sources:

- Avis–Grishukhin 1993: "We are not able to prove that P1 is NP-hard".
- Avis 2003: "Its complexity status is unknown".
- GKL 2011 preprint: "the complexity of separation for the remaining
  inequalities … is unknown". GKL also note that rounded psd separation
  reduces to hypermetric separation.

In the lattice picture of Lemma 1, a violated split is a lattice point
strictly inside the sphere with diameter `[0, −b₀]`. Binary structure, that is
`‖bᵢ‖² = ⟨b₀, bᵢ⟩`, forces every `−bᵢ` onto that sphere, which makes the test a
Delaunay-type test. The reduction instead places the `bᵢ` freely
(`⟨b₀, bᵢ⟩ = 0`). This note therefore does **not** settle the binary
(max-cut) case. The post-2012 hypermetric literature was not searched.

## 7. Priority and novelty

- **The MINLP question.** No source examined settles it. de Meijer et al.
  (March 2026) still call it unclear. The review scanned the titles of the
  papers that Semantic Scholar lists as citing B–T 2015 (12), Letchford 2010
  (5) and Burer–Letchford 2014 (3; this list is known to be incomplete). No
  title suggests a complexity result. It also read the relevant parts of
  Park–Boyd (arXiv:1510.06421), Wang–Alidaee (arXiv:2409.14176) and
  Galli–Letchford 2021, which give no complexity result.
- **The lattice core is standard.** Lemma 2 is the standard textbook
  subset-sum reduction for CVP, with one extra lattice vector that puts `0`
  at the threshold distance. It appears in Regev's lecture notes (2004,
  Lecture 5, Thm 2), which I checked, and is presumably in
  Micciancio–Goldwasser (2002, Ch. 3), which I did not check. CVP was first
  shown NP-hard by van Emde Boas (1981). Whether his report uses this
  particular construction is unverified. Lemma 3 is Kannan's (1987) embedding
  with a doubled target. Lemma 1 is the
  classical criterion "`b₀/2` lies in the Voronoi cell if and only if `b₀` is
  shortest in `b₀ + 2L`". So the NP-hard lattice problem behind the result is
  deciding whether `b₀/2` lies outside the closed Voronoi cell, or
  equivalently CVP verification with candidate `0`.
- **No explicit statement found.** The review found no explicit hardness
  statement of this form in Dutour Sikirić–Schürmann–Vallentin
  (arXiv:0804.0036), Hunkenschröder–Reuland–Schymura (arXiv:1811.08532),
  Bonifas–Dadush (arXiv:1412.6168), Micciancio–Voulgaris (ECCC TR10-014), or
  Micciancio's lecture notes. It is nevertheless probably folklore.
- **Not the MILP result.** Caprara and Letchford (2003) showed that
  separating split cuts for mixed-integer *linear* programs is NP-hard. That
  is a different problem. MILP split cuts come from a split disjunction
  combined with a polyhedron. The split inequalities here are quadratic in
  `x` and valid for `IQₙ` without any constraint set, as Burer–Letchford
  (2011, §5.2) and B–T (§3) point out. Neither hardness result implies the
  other. For Caprara–Letchford I checked only the bibliographic record; their
  result is cited from memory.
- **What the note contributes.** The contribution is the link to the MINLP
  question. On the MINLP side it adds hardness for positive definite `X` with
  `X₀₀ = 1`, hardness for 0/1 splits, strong NP-hardness, NP membership, and
  the tractable cases in rank, support and non-PSD input.
- **Not checked.** Letchford's IPCO 2010 paper; the published versions of
  Burer–Letchford (2014) and B–T (2015); the Micciancio–Goldwasser book
  itself; Deza–Laurent (1997); the post-2012 hypermetric literature.

## 8. Relevance for solvers

Split inequalities cut the SDP relaxation `{X ⪰ 0, X₀₀ = 1}` of integer QP
strictly below the PSD cone (B–T Lemma 5: `SCₙ ≠ Sₙ⁺`). They are used in
SDP-based branch-and-bound. B–T separate them exactly at PSD points with a
convex integer-QP solver (Buchheim–Caprara–Lodi), and at non-PSD points by
eigenvector rounding. de Meijer et al. separate the 1- and 2-index
`{0, ±1}` families by enumeration in their ternary QP solver.

What the results imply:

- **Exact separation at PSD points is worst-case superpolynomial unless
  P = NP.** This holds even at positive definite points with one hidden 0/1
  violator. It was already known that B–T's tool, convex integer QP, solves an
  NP-hard problem class. The new information is that the separation problem
  itself is hard.
- **The hardness survives de Meijer et al.'s cut families.** By
  Corollary 5, it holds in the strong sense at points that already satisfy
  their basic relaxation (4.1) for unconstrained problems. The points also
  satisfy every family their branch-and-bound separates: triangle, RLT,
  1- and 2-index split, pair (2.3) and odd-set (4.4) inequalities. Among the
  facets of `IQ¹₃` imposed on 3×3 principal submatrices, de Meijer et al.
  found the pair inequalities (2.3) the most beneficial. So passing all of
  these families does not make exact split separation easier. Their exact
  split separation is polynomial only because it is restricted to one or two
  indices.
- **Heuristics or restricted families are necessary** for guaranteed
  polynomial time. Bounding the coefficients does not help (Corollary 2).
  Bounding the support does (Corollary 4), and so does low rank (Theorem 3).
  This supports de Meijer et al.'s choice of exhaustive small-support
  families. It gives no guidance on which heuristic performs well.
- **Fixed-rank points are separable exactly.** A point of rank `r` costs
  `r^{O(r)}·poly` time. A rank-1 point is separated by any fractional
  coordinate, and Theorem 4 gives the most violated split. Whether relaxation
  optima in practice have low rank depends on the instance. Interior-point
  solutions typically have the largest rank on the optimal face.
- **Non-PSD points are easy.** B–T's Theorem 5 states this. Lemma 4 supplies a
  rational certificate and a violated split directly.

Limits:

- The hardness is a worst-case statement. It does not predict solver
  performance.
- The hard points need not satisfy binary structure (`diag(X) = x`).
  Through X3C with `q ≥ 2`, they can be made to satisfy all of de Meijer et
  al.'s (4.1) without linear constraints, (2.1)–(2.3), (4.3), (4.4),
  (4.5)–(4.8) and (4.11)–(4.12) (Corollary 5). Other valid ternary
  inequalities are not controlled, for example the remaining facets of
  `IQ¹₃` that de Meijer et al. list. Inequalities that are tight at `ℓ(0)` are
  not controlled either.
- At these points the violation is only polynomially small,
  `Θ(1/(n(n+q)))`. A solver with a fixed violation tolerance may ignore such
  cuts.
- For Boolean-quadric-type relaxations of binary problems, the corresponding
  separation problem (rounded psd, hypermetric, gap-1) remains open (§6).

## 9. Corrections to the scout report and the review

To the scout report (§2.1, §3.1):

1. **Attribution.** "Burer–Letchford conjectured NP-hardness" should read:
   they posed the question, and B–T attribute an NP-hardness conjecture to
   them (§1). The review found this, and I confirmed it from the preprint
   text.
2. **Membership.** "Membership not yet proved" is superseded. The problem is
   in NP for every rational symmetric input (Theorem 2).
3. **Lemma B.** It asserted the existence of a rational `γ` without a
   construction. It is now given explicitly, or avoided by the Gram route
   (Lemma 2 remarks). `M ≥ 3` is not needed; `M = 1` works with
   `n < γ² ≤ n + 1`.
4. **Lemma C.** It needs `t ≠ 0`, as the review noted. The defect is worse
   than a loss of positive definiteness: with `h = ‖t‖₁` and `t = 0`, `b₀ = 0`
   and the scout's `Y = BᵀB/‖b₀‖²` is undefined.
5. **Padding.** The unfinished "padding" promise version is replaced by X3C,
   where every violated split has `|supp w| = q + 1` (Corollary 1(iii)).
6. **Attack plan item 3.** Exact separation over `{−1,0,1}ⁿ⁺¹` is NP-hard
   (Corollary 2), as the review found.
7. **Other constraints.** "Other RLT or triangle constraints are not
   controlled" is too pessimistic; Remark 1 gives the refinement.

To the review:

1. **§3.** The explicit `γ = (c + n/c)/2` satisfies `γ² − n ∈ (0, 1)`, not
   only `(0, 9/4]`. The stated bound is correct but loose. The sharper bound
   lets the rational-`γ` route work with `M = 1`.
2. **§5.3.** The bullet saying "every violated `v` has support `n/2 + 2`" is
   imprecise. `(0, −x, 1)` has `n/2 + 1` nonzeros and `(−1, x, −1)` has
   `n/2 + 2`. The split's `w` has `n/2 + 1` nonzeros in both cases. The
   subset-sum offset also relies, without saying so, on the NP-hardness of
   subset sum with a prescribed number of ones. That variant is NP-hard, but
   the note uses X3C instead, where every solution automatically has `q`
   ones.
3. **§8.2.** It cites "Micciancio–Goldwasser, Thm 3.1", but §8.4 lists the
   book as not reached. The theorem number is unverified, so the note cites
   only the chapter.
4. **§5.1.** The pointer to Schrijver Cor. 5.3c was not rechecked. The note
   instead relies on the polynomial-time solvability of linear Diophantine
   systems (Hermite normal form), which gives the same bound.
5. **§5.5.** "Vertex of `IQₙ`": `IQₙ` is not a polytope, and `ℓ(0)` is an
   extreme point.
6. **§6.** The factorization `G = (PPᵀ)⁻¹PXPᵀ(PPᵀ)⁻¹` is correct. The note
   uses the simpler `P = X_{K,·}`, `G = X_KK⁻¹` that the elimination of
   Lemma 4 provides.

New in this note, beyond the review:

- The reduction is stated for general 0/1 EQUATIONS, which covers subset sum
  and X3C in one proof. It is checked with `M = 1` on multi-row and X3C
  instances.
- The rank-1 form "violated if and only if `x ∉ ℤⁿ`", with the maximum
  violation `⌊D²/4⌋/D²`.
- An explicit additive gap, now `2/(N+7)` (Corollary 3).
- The quantitative placement near `ℓ(0)` against the ternary relaxation of de
  Meijer et al.
- The identification of the binary image with GKL's rounded psd inequalities.

No error was found in the core proofs of the scout report or the review.

## 10. Checks actually run

These are targeted checks only. No project-wide verification was run, and CI
was not inspected. The command, rerun from the repository root on 2026-09-29
after both revisions (§11), was:

```text
python3 research-20260928b/side-results/check_split_separation.py
```

It uses only the standard library, with exact `fractions.Fraction` arithmetic,
and took about 16 s. For positive definite `X` the set of violated splits is
computed completely, by Fincke–Pohst enumeration of all `u ∈ e₀ + 2ℤᴺ` with
`uᵀXu < X₀₀` over an exact `LDLᵀ` factorization. It is not a box search. The
script prints `ALL CHECKS PASSED`.

In every Theorem 1 row, the script checks that `X ≻ 0`, `X₀₀ = 1`, the set of
violated splits, the minimum of `q`, and the 0/1 violators of the flipped
matrix `DXD` (Corollary 2). At `h² = n+1` it also checks the explicit matrix
`G`. Output summary:

| Check | Instances | Result |
|---|---|---|
| Lemma 1 identities | 300 random rational symmetric `X` | all hold |
| Scout instances `a = (3,5,7)` | 8 values of `s` | violators exactly `(0,−x,1)`, `(−1,x,−1)` for `s ∈ {8, 10, 15}`, minimum `q = −1/32`; none otherwise |
| Theorem 1, subset sum, `h² = n+1` | 680 (all sorted `a ∈ {1..5}ⁿ`, `n ≤ 3`; all sorted `a ∈ {1..3}⁴`; `s = 0..Σa+1`), 391 solvable | 0 mismatches |
| Same, `h² = (n+1)/8` (boundary `8h² = ‖t‖²`) and `h² = 1000(n+1)` | 680 each | 0 mismatches |
| Negative control, `h² = (n+1)/100` | 680 | 147 mismatches, as expected |
| Theorem 1, 0/1 equations with 2–3 rows, entries in `−2..2` | 300 (163 solvable) | 0 mismatches |
| Theorem 1, X3C, `q ∈ {2,3}` | 200 (98 with a cover) | 0 mismatches; every violated `w` has support `q+1`; largest Gram entry 64 |
| Corollary 3, `M = 3`, `γ² = n+8`, `h² = 1` | 680 subset sum, 300 multi-row, 60 X3C | violated set as in Theorem 1; gap exactly `2/(n+9)`: 0 failures |
| Corollary 3 remark, `M = 1`, `γ² = n+1`, `h² = 1/8` | 680 subset sum, 60 X3C | violated set as in Theorem 1; gap exactly `2/(8n+9)`: 0 failures |
| Sharper threshold is tight | `M = 1`, three copies of a 3-element universe | exact at `h² = 1/8`; extra violators at `h² = 1/9` |
| Corollary 3 padding, `M = 3`, `n = 14q` | X3C with `q = 1, 2, 3`; full enumeration at `q = 1` | every `|Xᵢⱼ| ≤ 1`; violated set as in Theorem 1 at `q = 1`: 0 failures |
| Lemma 3 threshold, `L = ℤ`, `t = 1/3` | 1 | no violator at `8h² = ‖t‖²`; violators `(1,−1)`, `(−2,1)` at `h² = ‖t‖²/9` |
| Lemma 4 | 104 non-PSD, 177 PSD | every certificate valid; every PSD report confirmed by all principal minors |
| Theorem 4 | 400 random `ℓ(x)` | identity `q = m(m+D)/D²`, maximum violation, and both criteria: 0 failures |
| Remark 1, `4h² = 3Ĝ` | 610 subset-sum instances with `s ≠ 0` | violated set unchanged; (4.1), (2.1)–(2.2), (4.5)–(4.8) hold: 0 failures; pair inequalities (2.3) fail on 458 (e.g. `a = (1, 6)`) |
| Corollary 5, `4h² = max(3, n+1)·Ĝ` | 100 X3C, `q ∈ {1,2,3}` (64 with a cover; 11 with `n = 1`, including `(q, n) = (1, 1)`) | `Ĝ = max(7, 3q+2n+1)`; violated set as in Theorem 1; `X` and `DXD` satisfy (4.1), (2.1)–(2.3), (4.4), (4.5)–(4.8); (2.3) also holds at `h² = n+1`; for `q ≥ 2` no violated split has `|supp w| ≤ 2`: 0 failures |
| Corollary 5, checker liveness | 1 positive definite probe (unit diagonal, off-diagonal `−6/25` on five variables) | flagged as violating only (4.4), as intended |
| §6 identity | 1,000 random `X` with `Xᵢᵢ = X₀ᵢ` | split = rounded psd inequality: 0 failures |

These finite checks confirm the constructions and identities on small
instances. They do not replace the proofs.

## 11. Revision after final review

The [final review](../reviews/split-final-review.md) found no mathematical
error. Changes made on 2026-09-29 in response:

1. **Main strengthening (review A1).** New Corollary 5, with a proof: X3C
   points satisfy de Meijer et al.'s pair inequalities (2.3) for every `h`.
   With `4h² ≥ max(3, n+1)·Ĝ` they also satisfy (4.1) without linear
   constraints, (2.1)–(2.2), the odd-set inequalities (4.4) and the RLT
   inequalities (4.5)–(4.8). The same holds for the flipped matrix `DXD`. So
   strong NP-hardness, including over 0/1 splits, holds at such points. Also
   updated: the Summary, Remark 1 (pair inequalities fail only for subset
   sum) and §8 (a new implication bullet and a corrected "Limits" bullet).
   The script gained the `[Corollary 5]` check and a liveness probe for its
   constraint checker.
2. **Corollary 3 (A3).** The additive bound was restated in the input order
   `N`. It was first sharpened to a gap of `2/(9(N−1))`, which the second
   round below superseded.
3. **Attribution of Lemma 2 (A6).** It is now called the standard textbook
   reduction. I checked Regev's 2004 notes (Lecture 5, Thm 2), which do not
   attribute it to van Emde Boas. The van Emde Boas attribution of this
   particular construction is marked unverified, in the Summary, the
   Lemma 2 remarks and §7.
4. **Nits (A2, A4, A5, A7).**
   - The Lemma 2 remark now says that `g` lies at distance `γ` from the
     textbook target, and that translation puts `0` at the threshold.
   - The Remark 1 slack bound now includes `h² ≥ (n+1)/8`.
   - Lemma 1 now explains why `L` is discrete for rational `X`.
   - §7 now separates this result from the MILP split-cut hardness of
     Caprara–Letchford (2003). Only its bibliographic record was checked.
5. **Script.** The flip check (Corollary 2) now runs at every `h`, not only
   `h² = n+1`. The command was rerun; §10 records the output.

Second round, after the
[recheck of Corollaries 3 and 5](../reviews/split-cor5-recheck.md), which
found Corollary 5 correct (2026-09-29):

1. **Corollary 3, optimality claim withdrawn (P2).** The first round said
   "within this construction the gap cannot be improved" and "the largest
   possible". Both were overstated, because the maximization used two
   sufficient conditions as if they were limits. I verified the recheck's
   counterexamples:
   - for Lemma 2's lattice, `8h² ≥ γ² − n` suffices in place of
     `8h² ≥ ‖t‖²`, by a two-line argument now in the proof;
   - with `M = 1` this gives `2/(8N−7)`;
   - with `M = 3`, `γ² = n + 8` and `h² = 1` it gives `2/(N+7)`.

   Corollary 3 now states and proves the gap `2/(N+7)`, so additive error
   below `1/(N+7)` is strongly NP-hard. It makes no optimality claim. The
   padding condition for entries in `[−1, 1]` became `n ≥ 14q`. The script
   checks the new gap, the `M = 1` variant, the tightness of the sharper
   threshold and the padding.
2. **Formula for `Ĝ` (P1).** `Ĝ = max(7, 3q + 2n + 1)`. The earlier
   `max(3q + 2n + 1, 2(n+1))` was wrong at `(q, n) = (1, 1)`, where
   `Ĝ = 7`; the conclusion was unaffected. The script now asserts the
   formula and includes that case.
3. **Wording in §8 (P3).** de Meijer et al. found the pair inequalities
   (2.3) the most beneficial of the `IQ¹₃` facets imposed on 3×3 principal
   submatrices, not of all their families.
4. **Optional strengthening, adopted.** For `q ≥ 2`, the Corollary 5 points
   also satisfy the 1- and 2-index splits (4.3) and (4.11)–(4.12). So they
   satisfy every cut family of de Meijer et al.'s branch-and-bound. This was
   added to Corollary 5, the Summary and §8, and is checked in the script.
   The liveness probe is now positive definite, as the recheck suggested.

## References

- D. Avis, On the complexity of testing hypermetric, negative type, k-gonal and
  gap inequalities (2003).
- D. Avis, V. P. Grishukhin, A bound on the k-gonality of facets of the
  hypermetric cone and related complexity problems, Comput. Geom. (1993).
- C. Buchheim, A. Caprara, A. Lodi, An effective branch-and-bound algorithm
  for convex quadratic integer programming, IPCO 2010.
- C. Buchheim, E. Traversi, On the separation of split inequalities for
  non-convex quadratic integer programming, Optimization Online 2013/07/3953;
  Discrete Optim. 15 (2015) 1–14.
- S. Burer, A. N. Letchford, Unbounded convex sets for non-convex mixed-integer
  quadratic programming, Optimization Online 2011/09/3172; Math. Program. 143
  (2014) 231–256.
- A. Caprara, A. N. Letchford, On the separation of split cuts and related
  inequalities, Math. Program. 94 (2003) 279–294.
- F. de Meijer, V. Piccialli, R. Sotirov, A. M. Sudoso, Beyond binarity:
  semidefinite programming for ternary quadratic problems, arXiv:2603.28979
  (2026).
- J. Edmonds, Systems of distinct representatives and linear algebra, J. Res.
  NBS 71B (1967).
- L. Galli, K. Kaparis, A. N. Letchford, Complexity results for the gap
  inequalities for the max-cut problem, Optimization Online 2011/3104.
- M. R. Garey, D. S. Johnson, Computers and Intractability (1979).
- R. Kannan, Minkowski's convex body theorem and integer programming, Math.
  Oper. Res. 12 (1987).
- R. Kannan, A. Bachem, Polynomial algorithms for computing the Smith and
  Hermite normal forms of an integer matrix, SIAM J. Comput. 8 (1979).
- R. M. Karp, Reducibility among combinatorial problems (1972).
- A. N. Letchford, Integer quadratic quasi-polyhedra, IPCO 2010, LNCS 6080,
  258–270.
- D. Micciancio, S. Goldwasser, Complexity of Lattice Problems (2002).
- O. Regev, Lattices in Computer Science, lecture notes, Tel Aviv University,
  Fall 2004, Lecture 5 (Some basic complexity results), Theorem 2.
- A. Schrijver, Theory of Linear and Integer Programming (1986).
- P. van Emde Boas, Another NP-complete partition problem and the complexity of
  computing short vectors in a lattice, Report 81-04, University of Amsterdam
  (1981).
