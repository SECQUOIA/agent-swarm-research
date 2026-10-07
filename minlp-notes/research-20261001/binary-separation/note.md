# Separating hypermetric, gap-1 and rounded psd inequalities is NP-complete

Date: 2026-10-01; revised 2026-10-03 after review rounds 1–3. Stream:
`binary-separation` of the [October 1 continuation](../PROGRAM.md).
Final status (2026-10-04): reviewed in three rounds; r3 minor fixes applied;
the last revision's fixes checked by the coordinating agent; not refereed.
Complete proofs are in §§3–6; exact-arithmetic checks are in §10.
[Review round 1](reviews/review-r1.md) found
the core mathematics correct and one gap: the strong NP-hardness claims at the
scaled points used numbers of exponential size. The first revision repaired the
gap (Lemma 5, Corollary 3). [Review round 2](reviews/review-r2.md) confirmed
that repair and everything else, except one wrong statement: the note called
the separation of Padberg's clique inequalities open, although its own
construction settles it. The second revision adds that result (Corollary 9)
and a new construction for the cut-form clique families at positive definite
points (Corollary 10); see "Revision after review round 2".
[Review round 3](reviews/review-r3.md) verified Lemma 6 and Corollaries 9 and
10 and requested minor fixes, applied in this revision; see "Revision after
review round 3". The coordinating agent re-derived the new proof step for the
`(q + 3)/(4qN)` maximizers and reran `code/check_r3_violation_maxima.py`;
the values match the formulas. The note has
not been refereed or formalized. Repository sweeps made outside this program
have included its files in commits; this program makes no commits.

## Summary

The [split note](../../research-20260928b/side-results/split-separation-np-complete.md)
(Summary, "Novelty caveat"; §6, "The binary analogue is open"; §8, last
"Limits" bullet) says that the separation complexity of the binary analogue
of split inequalities remains open. The binary analogue consists of the
hypermetric, gap-1 and rounded psd inequalities for max-cut, and the
corresponding Boolean quadric inequalities. As a report of the literature this
was accurate. Every source checked, from Avis and Grishukhin (1993) through
Letchford and Sørensen (2012) and Galli, Kaparis and Letchford (2012) to
Letchford's 2022 survey chapter on the Boolean quadric polytope, calls the
problem open. The searches in §7 found no source that settles it.

This note settles it.

1. **Hypermetric separation is strongly NP-complete** (Theorem 1,
   Corollary 2; proved). Deciding whether a rational distance vector violates
   some hypermetric inequality is NP-complete in the strong sense.
   Equivalently, membership in the hypermetric cone is strongly
   co-NP-complete. This answers problem P1 of Avis and Grishukhin (1993),
   "Is d hypermetric?", about which they wrote: "We are not able to prove
   that P1 is NP-hard". The proof is a short reduction from EXACT COVER BY
   3-SETS (X3C). It uses the same two tools as the split note: the standard
   exact-cover reduction for the closest vector problem, and Kannan's
   embedding. The split note named the obstacle: binary structure forces all
   generators onto one sphere, which turns the test into a Delaunay-type
   test. The obstacle disappears for exact cover, because every 0/1 vector
   lies on the sphere through 0 centered at `½𝟙`.
2. **The hard points pass the usual relaxations** (Corollary 3; proved). The
   hard distance is of negative type with a positive definite Gram matrix.
   For X3C instances with `q ≥ K ≥ 3` sets in a cover, it satisfies all
   triangle inequalities and all hypermetric inequalities of gonality at most
   `2K − 3`; X3C stays strongly NP-complete under this restriction. After
   scaling by `ε = 1/(8n + 2p + 1)` (`n` sets, `p` elements), the
   corresponding Boolean quadric point `X` is positive definite with
   `Xᵢᵢ = X₀ᵢ`, lies in the metric polytope, and satisfies every rounded psd
   inequality with `|σ| ≥ 3`. All its entries are fractions with numerators
   and denominators at most `4(8n + 2p + 1)`. (The original draft scaled by
   `1/(2δᵀM⁻¹δ)`, whose size grows exponentially; the review caught this.)
3. **Consequences for the other classes** (Corollaries 4–6 and 8–10;
   proved). Exact separation is strongly NP-complete for each of the
   following:
   - hypermetric, gap-1, rounded psd and k-gonal (all `k`) inequalities for
     the cut polytope;
   - their Boolean quadric images, namely the hypermetric correlation
     inequalities and the Boros–Hammer inequalities. The Boros–Hammer
     inequalities are the split note's binary split inequalities;
   - Padberg's clique inequalities (10) and cut inequalities (11), and the
     family (12) that contains both (numbering of Letchford 2022). The
     violated inequalities define facets. For the clique inequalities the
     hard point is switched on one variable (Corollary 9). Letchford (2022)
     listed (10)–(13) as having unknown separation complexity and suspected
     that all four are NP-hard; this is now proved for all four;
   - odd clique inequalities in cut form, that is, the Barahona–Mahjoub
     clique inequalities (18) and their switchings; the inequalities (18)
     themselves; and pure hypermetric inequalities. Corollary 5 proved this
     for odd clique and pure hypermetric inequalities at points with
     repeated points. Corollary 10 (new in revision r2) replaces the repeated
     points by nearby distinct points, so the hard points have a positive
     definite Gram matrix here too, and adds (18).

   All these hard points are rational points in the metric polytope and the
   interior of the elliptope (positive definite Boolean quadric form), with
   numerators and denominators bounded by a polynomial in `n + p`. For
   integer QP this strengthens the split note: split separation stays
   strongly NP-hard at positive definite points with binary structure, and
   every violated split has entries in `{0, ±1}`.
4. **Gap inequalities** (§6). Gap-0 separation is NP-complete (Theorem 4;
   proved; strong hardness not shown), but only at non-psd points. Gap-0
   inequalities never cut a psd point, so this result does not matter for
   solvers. For general gap inequalities the decision problem is trivial at
   non-psd points. At psd points it remains open.
5. **What stays easy** (Lemma 3; proved). Triangle, psd and negative type
   inequalities are separable in polynomial time. So are hypermetric
   inequalities at points that are not of negative type, hypermetric
   inequalities of any fixed gonality or fixed support, and hypermetric
   inequalities at points of fixed rank (fixed-parameter tractable).

**Novelty caveat.** No source examined proves any of items 1–4 (§7). The
construction is short and uses standard parts, so lattice experts may regard
it as folklore. An unsuccessful search does not establish novelty. The
hypermetric sources from 1993 to 2012 all state the problem as open, and so
does Letchford's 2022 survey (§7.2, pp. 18–19; §8, p. 20), which also lists
the clique, cut and Boros–Hammer inequalities and the Barahona–Mahjoub clique
inequalities as having unknown separation complexity. The full text of
Deza–Laurent (1997), Chapter 28, was not accessible; only its published
abstract was read.

**Relevance for solvers** (§9). Polynomial-time exact separation of these
classes is impossible unless P = NP. For every class in items 1 and 3, this
holds even at points that strictly satisfy the semidefinite relaxation
(positive definite) and satisfy the triangle inequalities and the
fixed-gonality families. This fits what max-cut codes do. BiqMac uses triangle
inequalities only. BiqBin and MADAM enumerate the triangle inequalities, and
they separate pentagonal and heptagonal inequalities heuristically, although
these families have polynomial size. The result does not say which heuristic
works. At the points of Corollary 3, the maximum violation is exactly
`1/(16n + 4p + 2)` in the Boros–Hammer scale (13), and at all hard points of
this note it is of order `1/(n + p)`. That is polynomially small, but this is
a property of the construction. Small violations are not proved to be
necessary for hardness.

## 1. Forms and inequality classes

Let `V = {0} ∪ W` be a finite set with root `0`, and let `d ∈ ℝ^{E(V)}`. For
`b ∈ ℤ^V` write `σ(b) = Σ_v b_v` and `Q(b, d) = Σ_{u<v} b_u b_v d_uv`. The gap of `b`
is `γ(b) = min{|sᵀb| : s ∈ {±1}^V}`. It has the parity of `σ(b)`, and
`γ(b) ≤ |σ(b)|`. The classes, following Galli–Kaparis–Letchford (GKL 2012,
§2 and Fig. 1), are:

| Class | Vectors `b` | Inequality |
|---|---|---|
| hypermetric | `σ(b) = 1` | `Q(b,d) ≤ 0` |
| negative type | `σ(b) = 0` | `Q(b,d) ≤ 0` |
| psd | `b ∈ ℝ^V` | `Q(b,d) ≤ σ²/4` |
| rounded psd | `σ(b)` odd | `Q(b,d) ≤ (σ² − 1)/4` |
| gap | all `b` | `Q(b,d) ≤ (σ² − γ²)/4` |
| gap-1, gap-0 | `γ(b) = 1`, resp. `0` | as for gap |
| odd clique | `b ∈ {0,±1}^V`, `σ(b)` odd | `Q(b,d) ≤ (σ² − 1)/4` |
| k-gonal (Avis 2003, (1)) | `Σ|b_v| = k` | `Q(b,d) ≤ ⌊σ²/4⌋` |

Triangle inequalities are the hypermetric inequalities with
`b = e_u + e_v − e_w`, and the perimeter inequalities `d_uv + d_uw + d_vw ≤ 2`
are the rounded psd inequalities with `b = e_u + e_v + e_w`. A gap-1
inequality has right-hand side `(σ² − 1)/4`, so it is a rounded psd
inequality. A hypermetric inequality has `γ = 1`. Hence

hypermetric ⊂ gap-1 ⊂ rounded psd.

In the ±1 form `Z = J − 2D`, where `D` is the matrix of `d` with zero diagonal,
the gap inequality reads `bᵀZb ≥ γ(b)²`. The max-cut codes BiqBin and MADAM
call the inequalities `⟨bbᵀ, X⟩ ≥ 1` (`eᵀb` odd) "hypermetric". In the
naming above these are the rounded psd inequalities.

**Correlation form.** Define the symmetric matrix `M = M(d)` on `W` by

`Mᵢᵢ = d₀ᵢ`,  `Mᵢⱼ = (d₀ᵢ + d₀ⱼ − dᵢⱼ)/2`,  and `g_M(z) := zᵀMz − Σᵢ Mᵢᵢzᵢ`.

The map `d ↦ M` is a linear bijection from `ℝ^{E(V)}` onto the symmetric
matrices on `W`. Its inverse is `d₀ᵢ = Mᵢᵢ`, `dᵢⱼ = Mᵢᵢ + Mⱼⱼ − 2Mᵢⱼ`. By
Schoenberg's theorem, `d` is of negative type if and only if `M ⪰ 0`.

**Lemma 0 (proved).** For every `d` and every `z ∈ ℤ^W`, put `b = (1 − Σz, z)`.
Then `Q(b, d) = −g_M(z)`. This gives a bijection between the hypermetric
vectors `b` and `ℤ^W`. So `d` violates a hypermetric inequality if and only if
`g_M(z) < 0` for some `z ∈ ℤ^W`.

*Proof.* Put `S = Σz`, so that `b₀ = 1 − S`. Substitute
`dᵢⱼ = Mᵢᵢ + Mⱼⱼ − 2Mᵢⱼ` and `d₀ᵢ = Mᵢᵢ`:

`Q = (1 − S)Σᵢ zᵢMᵢᵢ + Σᵢ zᵢMᵢᵢ(S − zᵢ) − Σ_{i<j} 2zᵢzⱼMᵢⱼ = Σᵢ zᵢMᵢᵢ − zᵀMz`. ∎

The inequalities `g_M(z) ≥ 0` (`z ∈ ℤ^W`) are the *hypermetric correlation
inequalities*. With `xᵢ = Mᵢᵢ` and `yᵢⱼ = Mᵢⱼ` they read
`Σ bᵢ(bᵢ − 1)xᵢ + 2Σ bᵢbⱼyᵢⱼ ≥ 0` (Letchford–Sørensen 2012, (5), p. 261).
Avis–Grishukhin (1993, end of §4) state the same equivalence with an integer
quadratic form.

**Split form.** Put `δ = diag(M)` and `X(M) = [[1, δᵀ], [δ, M]]`. This is a
Boolean quadric point with binary structure `Xᵢᵢ = X₀ᵢ`. By the split note's
§6 identity, the split `v` (with `u = 2v + e₀`, `σ = −u₀`) is violated at
`X(M)` if and only if `d` violates the rounded psd inequality with
`b = (σ − Σw, w)`. In Boolean quadric form these split inequalities are the
Boros–Hammer inequalities (Boros–Hammer 1993; GKL 2011, (6); Letchford–Sørensen
2012, (8), p. 267). The hypermetric inequalities are the case `|u₀| = 1`. For
`v = (0, −z)`, `q_X(v) = zᵀMz − δᵀz = g_M(z)`.

Geometrically, let `M` be the Gram matrix of `u₁, …, u_r`, and suppose
`0, u₁, …, u_r` lie on a sphere with center `c`. Then `g_M(z) = ‖Σzᵢuᵢ − c‖² − ‖c‖²`.
So a violated hypermetric inequality is a lattice point strictly inside the
circumsphere (Avis–Grishukhin 1993, §1).

## 2. Status in the literature

The table answers step 1 of the task. All quotations were checked against the
saved texts ([manifest](sources/MANIFEST.md)), except the Deza–Laurent entry,
which rests on the publisher's abstract.

| Question | Status before this note | Locator |
|---|---|---|
| Membership in the hypermetric cone ("is `d` hypermetric?") | In co-NP. NP-hardness open. | Avis–Grishukhin 1993, §4: Corollary 6 ("Testing hypermetricity of d is in co-NP") and "We are not able to prove that P1 is NP-hard". Deza–Grishukhin–Laurent 1993, Remark 4.12, p. 51: "It is not known whether testing hypermetricity is NP-hard". Deza–Laurent 1997, Ch. 28, pp. 445–465, abstract: "Although its exact complexity status is not known, there are several results that indicate that it is very likely to be a hard problem." Avis 2003, §1: "Its complexity status is unknown". |
| Separation over all hypermetric inequalities, arbitrary points | Same problem. Its decision version is non-membership. | as above; Letchford–Sørensen 2012, §5.3, p. 269: "the complexity of hypermetric separation is a long-standing open problem"; Letchford 2022, §8, p. 20 (research directions): "Determine whether or not the separation problem for the hypermetric inequalities (23) can be solved in polynomial time." |
| Hypermetric separation at non-negative-type points | Polynomial. I found no explicit statement. It follows from Lemma 3(i), or from the identity `Q(b) = (Q(b+eᵢ) + Q(eᵢ−b))/2` for `σ(b) = 0`, which writes each negative type inequality as the average of two hypermetric ones (Avis 2003, §1, credits this implication to Deza). | Lemma 3(i) |
| Hypermetric separation at psd points, or at points that satisfy the triangle inequalities | No separate statement found. Avis–Grishukhin's instances use distances in `{1, 1+t}`, which satisfy the triangle inequalities, but they control only gonality `≤ 2m+1`. | Avis–Grishukhin 1993, Corollary 10 |
| All `(2m+1)`-gonal hypermetric inequalities, `m` part of the input (also pure) | co-NP-complete | Avis–Grishukhin 1993, §4 (their P2); Avis 2003, §1 (his P1) |
| Smallest gonality of a violated hypermetric inequality | NP-hard | Avis–Grishukhin P3; Avis 2003, P2; Deza–Laurent 1997, Ch. 28, abstract |
| Negative type, k-gonal and gap analogues of these special cases | co-NP-complete or NP-hard, while full negative-type separation is polynomial | Avis 2003, §§1–3 (P1N, P2N, P1K, P2K, P1G, P2G) |
| Rounded psd | Reduces to hypermetric separation. In NP. Complexity unknown. | Letchford–Sørensen 2012, Prop. 19, pp. 268–269; GKL 2012, Theorem 3, Lemma 1, §4, p. 151 |
| Boros–Hammer (BQP) | Reduces to hypermetric correlation separation. Unknown. | Letchford–Sørensen 2012, Prop. 18, p. 268; §6, p. 270: "A major open question is the complexity of separation for the hypermetric correlation inequalities and their variants."; Letchford 2022, §7.2, p. 19: the separation problems for (13), (19), (23) and (25) "are equivalent. That is, either all of them can be solved in polynomial time, or none of them can." |
| Padberg's clique (10) and cut (11) inequalities, and their common generalization (12) (BQP) | Unknown, conjectured NP-hard | Letchford 2022, §4, pp. 8–9 (definitions); §7.2, p. 18: "The complexity of the separation problems for the inequalities (10)–(13) is unknown, but we suspect that they are all NP-hard." |
| Remaining cut-polytope classes (after triangle, odd bicycle wheel, 2-circulant, psd and negative type) | Unknown | Letchford 2022, §7.2, p. 19: "At the time of writing, the complexity of separation is unknown for the remaining inequalities for the cut polytope." In that chapter these include the Barahona–Mahjoub clique inequalities (18) and their switchings, the rounded psd inequalities (19), the hypermetric inequalities (23) and the gap inequalities. |
| Boros–Hammer separation in recent computation (2026) | Solved as a bounded nonconvex integer QP with Gurobi; no complexity statement about the full class | Dey–Jiang–Kazachkov–Lodi–Muñoz, arXiv:2604.00932v1, §4.1.2, p. 16, problem (18) with `wᵢ ∈ [−2, 2]`; p. 4 recalls that Boros and Hammer "developed polynomial-time solvable separation of certain subclasses of BH inequalities" (by minimum spanning trees) |
GKL left separation for the remaining Figure 1 families open and proved a reduction from rounded PSD separation to hypermetric separation.
| odd clique, gap-0 | Unknown | GKL 2012, §4 (same sentence; both appear in Fig. 1) |
| gap | Introduced by Laurent–Poljak; computing `γ(b)` is NP-hard. Finite (doubly exponential) separation algorithm. Checking validity of one given gap inequality is co-NP-complete. | Laurent–Poljak, Eur. J. Combin. 17 (1996) 233–254 (not read); Laurent–Poljak, LIENS-93-27 (1993), printed p. 14 (PDF p. 15): "it is NP-hard to decide whether the gap γ(b) is zero"; GKL 2012, Lemmas 2–3, Theorem 7 |
| triangle, psd, negative type | Polynomial | GKL 2012, §4 |

**On Dash and rank-1 cuts.** I found no result by Dash on the separation of
hypermetric, gap or binary psd inequalities. The related results I found
concern mixed-integer *linear* rank-1 closures:

- Cook–Dash (2001, §1) contrast the polynomial-time matrix-cut operators with
  the Chvátal closure, for which "the separation problem for P′ is
  NP-complete in general (Eisenbrand 1998)".
- Caprara–Letchford (2003) prove strong NP-completeness of separation for
  split, MIR and binary split cuts of MILPs.
- Dash, Günlük and Lodi state that the MIR closure equals the split closure
  and that its separation problem is NP-hard. Only the abstract was seen,
  through search snippets.
- Dash (ORL 2010) concerns the length of split-cut proofs.

None of these bears directly on the binary QP classes. Dash's thesis page
returned HTTP 403.

## 3. The reduction

Let `S₁, …, Sₙ ⊆ [p]` with `p ≥ 2`, and let `A ∈ {0,1}^{p×n}` be the incidence
matrix (`A_{ei} = 1` if and only if `e ∈ Sᵢ`). The question of EXACT COVER is
whether some `x ∈ {0,1}ⁿ` satisfies `Ax = 𝟙`. Fix a rational `η²` with

`max(p/12, (p−2)/4) ≤ η² < p/4`, for example `η² = (p − 1)/4`.

(The original draft had `p/8` in place of `p/12`. The two windows differ only
for `p ∈ {2, 3}`. Review round 1 pointed out that `p/12` suffices.)

Index a matrix `M` by `1, …, n, g` and set

```
M_ij = 4δ_ij + |S_i ∩ S_j|      M_ig = |S_i|/2      M_gg = p/4 + η²
```

**Lemma 1 (closed form; proved).** `M` is the Gram matrix of
`uᵢ = (2eᵢ, Aᵢ, 0)` and `u_g = (0, ½𝟙_p, η)` in `ℝ^{n+p+1}`, so `M ≻ 0`. For
`x ∈ ℤⁿ`, `k ∈ ℤ` and `y = Ax`,

`g_M(x, k) = 4Σᵢ xᵢ(xᵢ − 1) + Σ_e [y_e² + (k − 1)y_e] + k(k − 1)(p/4 + η²)`.

*Proof.* The inner products are `4δᵢⱼ + AᵢᵀAⱼ`, `½𝟙ᵀAᵢ = |Sᵢ|/2` and
`p/4 + η²`. The vectors are independent because of the blocks `2eᵢ` and
`η ≠ 0`. Next,

`‖Σxᵢuᵢ + k u_g‖² = 4‖x‖² + ‖y + (k/2)𝟙‖² + k²η² = 4‖x‖² + ‖y‖² + kΣy_e + k²p/4 + k²η²`.

The linear part is `Σᵢ xᵢ(4 + |Sᵢ|) + k(p/4 + η²)`. Because `A` is a 0/1
matrix, `Σᵢ xᵢ|Sᵢ| = Σ_e y_e`. Subtracting gives the formula. ∎

The key point is `‖Aᵢ‖² = 𝟙ᵀAᵢ`. Every 0/1 vector lies on the sphere through
`0` centered at `½𝟙`, so the generators automatically lie on one sphere.
That is the binary-structure condition of the split note's §6.

**Theorem 1 (proved).** The vectors `z ∈ ℤ^{n+1}` with `g_M(z) < 0` are exactly
`z = (x, −1)` with `x ∈ {0,1}ⁿ` and `Ax = 𝟙`. For each of them,
`g_M(z) = −(p/2 − 2η²) ∈ [−1, 0)`.

*Proof.* Write `z = (x, k)` and use Lemma 1.

- `k = 0`: `g = 4Σxᵢ(xᵢ−1) + Σ_e y_e(y_e − 1) ≥ 0`, since all entries are integers.
- `k = 1`: `g = 4Σxᵢ(xᵢ−1) + Σ_e y_e² ≥ 0`.
- `k ≥ 2`: each element term is at least `−(k−1)²/4`. So
  `g ≥ −p(k−1)²/4 + k(k−1)(p/4 + η²) = (k−1)(p/4 + kη²) > 0`.
- `k = −m` with `m ≥ 2`: over integers `y`, the element term `y² − (m+1)y`
  is at least `−⌊(m+1)²/4⌋`.
  - For odd `m ≥ 3` this bound is `−(m+1)²/4`, so
    `g ≥ −p(m+1)²/4 + m(m+1)(p/4 + η²) = (m+1)(mη² − p/4) ≥ 0`, because
    `mη² ≥ 3η² ≥ p/4`.
  - For even `m ≥ 2` it is `−m(m+2)/4`, so
    `g ≥ −pm(m+2)/4 + m(m+1)(p/4 + η²) = m((m+1)η² − p/4) ≥ 0`, because
    `(m+1)η² ≥ 3η² ≥ p/4`.
- `k = −1`: `Σ_e(y_e² − 2y_e) = ‖y − 𝟙‖² − p`, so

  `g(x, −1) = 4Σᵢ xᵢ(xᵢ − 1) + ‖Ax − 𝟙‖² − (p/2 − 2η²)`.

  The window gives `0 < p/2 − 2η² ≤ 1`. Both remaining terms are
  nonnegative integers. So `g < 0` exactly when both vanish, that is, when
  `x ∈ {0,1}ⁿ` and `Ax = 𝟙`. Then `g = −(p/2 − 2η²)`. ∎

Both ends of the window are sharp. With `η² ≥ p/4` there are no violators,
even when an exact cover exists. With `0 < η² < p/12`, every exact cover `x`
gives the extra violator `(x, −2)`, because
`g(x, −2) = −2p + 6(p/4 + η²) = 6η² − p/2 < 0`. More generally, any `x ∈ {0,1}ⁿ` with `Ax ∈ {1, 2}ᵖ` gives one,
so violators also appear in some no-instances. An example is `p = 3` with the
sets `{0,1}` and `{1,2}`, and `z = (1, 1, −2)`. The condition
`η² ≥ (p−2)/4` is needed as well: if `η² < (p−2)/4`, any `x ∈ {0,1}ⁿ` with
`‖Ax − 𝟙‖² = 1` has `g(x, −1) = 1 − (p/2 − 2η²) < 0`. The failures at
`η² = p/4` and below `p/12`, and Theorem 1 at the endpoint `η² = p/12`, are
confirmed in §10.

**Corollary 1 (cut form; proved).** Take `η² = (p − 1)/4` and
`V = {0, 1, …, n, g}`. The distance `d = d(M)` is

```
d_0i = 4 + |S_i|      d_0g = (2p − 1)/4      d_ij = 8 + |S_i △ S_j|      d_ig = (2p + 15)/4
```

So `4d` is integral, with entries at most `4p + 32`. The vector `d` violates the
hypermetric inequality of `b` if and only if

`b = (2 − |T|)e₀ + Σ_{i∈T} eᵢ − e_g`

for the index set `T` of an exact cover. In that case `Q(b, d) = 1/2`.

*Proof.* Lemma 0 and Theorem 1, with `b = (1 − Σz, z)` and `z = (𝟙_T, −1)`. ∎

*Example.* Take `p = 3` and the sets `{0,1,2}`, `{0,1}`, `{2}`. Then
`4M = [[28,8,4,6],[8,24,0,4],[4,0,20,2],[6,4,2,5]]`, and the violators are
`(1,0,0,−1)` and `(0,1,1,−1)`, the two exact covers. The script prints this
example. Here the first cover uses one set, so its inequality is a triangle
inequality. Corollary 3 excludes such small covers.

## 4. Complexity

**Lemma 2 (NP membership; proved).** Let `M` be any rational symmetric matrix.
If `g_M(z) < 0` for some `z ∈ ℤ^W`, then such a `z` exists with encoding size
polynomial in that of `M`.

*Proof.* There are three cases.

- **`M` not psd.** Lemma 4 of the split note gives an integral `y` of
  polynomial size with `yᵀMy < 0`. For an integer `t > |δᵀy|/|yᵀMy|`,
  `g_M(ty) = t²yᵀMy − tδᵀy < 0`.
- **`M ⪰ 0` and `δ ∉ range M`.** Then some rational `k ∈ ker M` has `δᵀk ≠ 0`,
  and `k` can be taken from a kernel basis. Scale it to be integral and
  choose the sign so that `δᵀk > 0`. Then `g_M(k) = −δᵀk < 0`.
- **`M ⪰ 0` and `δ = Mw`.** Take `K`, `P = M_{K,·}` and `G = M_KK⁻¹` as in the
  split note's Theorem 2, so that `M = PᵀGP`. Then
  `g_M(z) = ‖Pz − Pw/2‖²_G − ‖Pw/2‖²_G`. A violator has `‖Pz‖_G < ‖Pw‖_G`.
  Hence `y = Pz` satisfies `|yᵢ| ≤ Mᵢᵢ^{1/2}‖Pw‖_G`, and its entries have
  denominators dividing a common denominator of `P`. So `y` has polynomial
  size. The system `Pz = y` has an integral solution, so it has one of
  polynomial size (Hermite normal form; Kannan–Bachem 1979). ∎

Avis–Grishukhin (1993, Corollary 6) obtain co-NP membership of
hypermetricity differently, from a bound on the coefficients of facets.

**Lemma 3 (easy cases; proved).** A violated hypermetric inequality can be
found in polynomial time, or its absence certified, in each of these cases:

- (i) `d` is not of negative type (first case above);
- (ii) `M ⪰ 0` and `δ ∉ range M` (second case above);
- (iii) for each fixed `k`, over the inequalities of gonality at most `k`, by
  enumerating the `O(|V|^k 2^k)` vectors with `Σ|b_v| ≤ k`;
- (iv) for each fixed `t`, over the inequalities with support size at most
  `t`: on each `t`-subset, enumerate all `b` whose coefficients are within the
  Avis–Grishukhin facet bound `g₀(t)`, a constant for fixed `t`.

Moreover, when `M ⪰ 0` has rank `r`, the problem is solvable in time
`r^{O(r)}·poly`. In the third case of Lemma 2 it is exact CVP in the rank-`r`
lattice `Pℤ^W` with target `Pw/2`. Kannan's algorithm solves this as in the
split note's Theorem 3.

**Corollary 2 (proved).** HYP-VIOLATION asks: given a rational `d` on a finite
set `V`, is `Q(b, d) > 0` for some `b ∈ ℤ^V` with `σ(b) = 1`? This problem is
NP-complete in the strong sense, and its search version is NP-hard. Membership
in the hypermetric cone is strongly co-NP-complete.

*Proof.* Membership in NP is Lemma 2. For hardness, Corollary 1 maps an X3C
instance in polynomial time to an integral `4d` with entries `O(p)`. X3C is
strongly NP-complete (Garey–Johnson 1979, [SP2]). ∎

In the X3C instances every violator has gonality exactly `2q − 1`
(Corollary 3(b)). So these instances also give a new proof of
Avis–Grishukhin's P2 for points of negative type.

## 5. Where the hard points lie, and the other classes

**Lemma 5 (size of the scaling; proved).** Take any exact-cover instance with
`p ≥ 2` and `η² = (p − 1)/4`, and let `s = δᵀM⁻¹δ` with `δ = diag(M)`. Then

`maxᵢ Mᵢᵢ ≤ s ≤ 4n + p + 1/(4(p − 1)) < (8n + 2p + 1)/2`.

*Proof.* Let `B` be the matrix with columns `u₁, …, uₙ, u_g` of Lemma 1, so
`M = BᵀB` and `B` has full column rank. Put `c* = (𝟙ₙ, ½𝟙ₚ, γ)` with
`γ = (η² − p/4)/(2η)`. Then `uᵢᵀc* = 2 + |Sᵢ|/2 = Mᵢᵢ/2` and
`u_gᵀc* = p/4 + ηγ = (p/4 + η²)/2 = M_gg/2`, so `δ = 2Bᵀc*`. (Equivalently,
`c*` is equidistant from `0` and all generators: it is the center of a sphere
through them, as in §1.) Let `Π = B(BᵀB)⁻¹Bᵀ` be the orthogonal projection onto
the range of `B`. Then

`s = 4c*ᵀB(BᵀB)⁻¹Bᵀc* = 4‖Πc*‖² ≤ 4‖c*‖² = 4n + p + 4γ²`.

For `η² = (p−1)/4` we get `4γ² = (1/16)/η² = 1/(4(p−1)) ≤ 1/4`. For the lower
bound, Cauchy–Schwarz in the inner product of `M` gives
`Mᵢᵢ² = (eᵢᵀM·M⁻¹δ)² ≤ (eᵢᵀMeᵢ)(δᵀM⁻¹δ) = Mᵢᵢ s`. ∎

The upper bound and its proof come from review round 1. For X3C,
`Mᵢᵢ = 7`, so `s ≥ 7`. The upper bound cannot be improved much in general,
but it is far from tight for some families (computed exactly, §10):

- *Nearly attained (computed exactly).* For `n` singletons `{0}, …, {n−1}`
  with `p = n`, the ratio of `s` to the bound is 0.998, 0.9996, 0.9998 and
  0.99994 for `n = 4, 8, 12, 20` (for `n = 12`: `s = 60.012`, bound `60.023`).
- *Bounded (proved by an exact symbolic computation).* For `n` copies of
  `{0,1,2}` plus `{3,4,5}` (`p = 6`), `M` is positive definite and invariant
  under permutations of the copies, so the unique solution of `Mw = δ` is
  constant on the copies. The remaining 3×3 system, solved symbolically in
  `n`, gives
  `s(n) = 77(193n + 108)/(4(141n + 272))`, which increases to
  `14861/564 ≈ 26.35`. This reproduces the exact values `21.14`, `24.70` and
  `25.49` at `n = 5`, `20` and `40` (closed form and values from review
  round 2, item o3; recomputed in `code/closed_form_s.py`).
- For all triples of `[9]` (`n = 84`), `s/(n + p) = 0.67`.

**Corollary 3 (proved).** Take an X3C instance (`|Sᵢ| = 3`, `p = 3q`, `q ≥ 2`)
and `η² = (p − 1)/4`. Put `N = 8n + 2p + 1`, `ε = 1/N` and
`X(ε) = [[1, εδᵀ], [εδ, εM]]`.

- (a) `d` is of negative type and `M ≻ 0`.
- (b) Every violated hypermetric inequality has gonality exactly `2q − 1`. Its
  support has `q + 2` points, or `q + 1` when `q = 2`. So `d` satisfies every
  hypermetric inequality of gonality at most `2q − 3`. For `q ≥ 3` these
  include all triangle inequalities. For general exact-cover instances, `d`
  satisfies all triangle inequalities if and only if no exact cover uses at
  most two sets.
- (c) `4N·X(ε)` is an integral matrix with entries at most `4N`. So the
  entries of `X(ε)` are fractions whose numerators and denominators are
  bounded by `4N = O(n + p)`. Moreover, `X(ε)` is positive definite,
  `Xᵢᵢ = X₀ᵢ`, `εs < 1/2`, and `X(ε) − θe₀e₀ᵀ ≻ 0` for every `θ ≤ 1/2`, in
  particular for `θ = 1/4`.
- (d) The violated splits of `X(ε)` are exactly `v = (0, −x, 1)` and
  `v = (−1, x, −1)` (coordinates `0, 1..n, g`) for the exact covers `x`, with
  `q_X(v) = −ε/2 = −1/(2N)`. Equivalently, the violated rounded psd
  inequalities of `εd` are exactly the hypermetric inequalities of
  Corollary 1, each violated by `εQ(b, d) = 1/(2N)`. No rounded psd inequality
  with `|σ| ≥ 3` is violated.
- (e) The cut image of `X(ε)` is `εd`. For every `q ≥ 2` it lies in the
  interior of the elliptope (`J − 2εD ≻ 0`), and hence in `(0, 1)^{E(V)}`. If
  no exact cover uses at most two sets (in particular if `q ≥ 3`), `εd` also
  lies in the metric polytope (all triangle and perimeter inequalities).

Parts (c)–(e) hold for every exact-cover instance with `p ≥ 2`, not only for
X3C, because Lemma 5 is general. §10 checks them on random exact-cover
instances.

*Proof.*

- (a) is Lemma 1.
- (b) A violator is `b = (2 − q, x, −1)` with `Σx = q`, because a cover of
  `3q` elements by 3-sets has `q` sets. Its gonality is
  `|2 − q| + q + 1 = 2q − 1`. In general a cover with `m` sets gives gonality
  `2m − 1` for `m ≥ 2`, and 3 for `m = 1`. Triangle inequalities have
  gonality 3.
- (c) The entries of `4N·X(ε)` are `4N`, `4δᵢ = 28`, `4δ_g = 2p − 1`,
  `4Mᵢⱼ = 4|Sᵢ ∩ Sⱼ|` (`i ≠ j`) and `4M_ig = 6`. All are integers at most `4N`.
  By Lemma 5, `εs = s/N < 1/2`. By the Schur complement, for `θ < 1`,
  `X − θe₀e₀ᵀ ≻ 0` if and only if `εM − ε²δδᵀ/(1−θ) ≻ 0`, that is,
  `εs < 1 − θ`. This holds for every `θ ≤ 1/2`, and `θ = 0` gives `X(ε) ≻ 0`.
- (d) A split is violated if and only if `uᵀXu < 1` with `u = 2v + e₀`. If
  `|u₀| ≥ 3`, then `uᵀXu > u₀²/4 ≥ 9/4`, by (c) with `θ = 1/4`. If `|u₀| = 1`,
  the symmetry `v ↦ −v − e₀` reduces to `v = (0, −z)`, where
  `q_X(v) = εg_M(z)`; apply Theorem 1, which gives `g_M(z) = −1/2` at the
  violators. The translation to rounded psd inequalities is the split note's
  §6 identity, with `σ = −u₀`.
- (e) The covariance map is linear, and the map `d ↦ M` is homogeneous, so the
  cut image is `εd`. Let `Z = J − 2εD` on `V = {0} ∪ W`, and let
  `L = [[1, 0], [𝟙, −2I]]`. Using `Xᵢᵢ = X₀ᵢ`, a direct computation gives
  `Z = LX(ε)Lᵀ`: `Z₀ᵢ = 1 − 2X₀ᵢ`, `Zᵢᵢ = 1 − 4X₀ᵢ + 4Xᵢᵢ = 1` and
  `Zᵢⱼ = 1 − 2X₀ᵢ − 2X₀ⱼ + 4Xᵢⱼ = 1 − 2εdᵢⱼ`. Since `L` is invertible and
  `X(ε) ≻ 0` by (c), `Z ≻ 0`. A positive definite matrix with unit diagonal
  has off-diagonal entries in `(−1, 1)`, so `0 < εd_uv < 1` for all `u ≠ v`.
  This uses neither the triangle inequalities nor `q ≥ 3`. Triangle
  inequalities are homogeneous, so (b) applies to `εd`. Perimeter inequalities
  are rounded psd inequalities with `σ = 3`, so (d) applies. ∎

**Corollary 4 (classes; proved).** Each problem below takes a rational
vector `d ∈ ℚ^{E(V)}` (equivalently, through the covariance map, a rational
symmetric `X` with `X₀₀ = 1` and `Xᵢᵢ = X₀ᵢ`) and asks whether `d` violates
some inequality of the class. Each is strongly NP-complete. Hardness holds
even when the input is restricted to the points `εd` of Corollary 3 with
`q ≥ K ≥ 3`. These are rational points in `(0, 1)^{E(V)}` whose numerators
and denominators are `O(n + p)`. Their Boolean quadric forms are positive
definite with `Xᵢᵢ = X₀ᵢ`, and the points lie in the metric polytope and the
elliptope and satisfy every hypermetric inequality up to any fixed gonality.

- (i) hypermetric inequalities (cut form), equivalently hypermetric
  correlation inequalities (Boolean quadric form);
- (ii) gap-1 inequalities;
- (iii) rounded psd inequalities, equivalently Boros–Hammer inequalities, that
  is, the split note's binary split inequalities;
- (iv) k-gonal inequalities over all `k`.

*Proof.* Hardness: by Corollary 3(d), at these points a violated inequality of
any of the four classes exists if and only if a hypermetric one does, that is,
if and only if an exact cover exists:

- hypermetric ⊂ gap-1 ⊂ rounded psd;
- the even-`σ` members of (iv) are psd inequalities and hold at psd points.

The map from X3C instances to `εd` (or `X(ε)`) takes polynomial time, and by
Corollary 3(c) all numbers it produces are bounded by `4N = O(n + p)`. X3C is
strongly NP-complete, so each problem is strongly NP-hard. For class (i)
alone, the integral point `4d` of Corollary 1 also works, because hypermetric
inequalities are homogeneous.

Membership in NP, for every rational input:

- (i) Lemma 2.
- (ii) Suppose `γ(b) = 1`, with `|sᵀb| = 1` for `s ∈ {±1}^V`. Put
  `b′ = ±diag(s)b` with the sign chosen so that `σ(b′) = 1`. In the ±1 form
  `Z = J − 2D`, the gap-1 inequality `bᵀZb ≥ 1` becomes
  `b′ᵀ(diag(s)Z diag(s))b′ ≥ 1`. Now `diag(s)Z diag(s) = J − 2D(d^S)`, where
  `d^S` is the switching of `d` on `S = {v : s_v = −1}` (`d^S_uv = 1 − d_uv`
  if exactly one of `u, v` is in `S`, and `d_uv` otherwise). Since
  `b′ᵀ(J − 2D(d^S))b′ = σ(b′)² − 4Q(b′, d^S)`, the gap-1 inequality is
  violated if and only if `Q(b′, d^S) > 0`, a violated hypermetric
  inequality at `d^S`. Conversely, if `b′` is hypermetric and violated at
  `d^S`, then `b = diag(s)b′` has `|sᵀb| = 1` and odd `σ(b)`, so `γ(b) = 1`.
  So a certificate is `S` together with the Lemma 2 certificate for the
  rational point `d^S`. This argument works for every rational `d`, not only
  for `d ∈ [0,1]^{E(V)}`, the domain of GKL 2012, Lemma 6 (review round 1,
  optional item o3).
- (iii) The split note's Theorem 2, which covers every rational `X`, binary or
  not, through the covariance bijection. GKL 2012, Lemma 1 gives it too.
- (iv) A violation is either a psd violation, which is detectable in
  polynomial time by Lemma 4 of the split note, or a rounded psd violation. ∎

**Corollary 5 (pure hypermetric and odd clique; proved).** Take an X3C instance
with `q ≥ 3`. Add `q − 2` copies `0¹, …, 0^{q−2}` of the point `0`: they are at
distance 0 from `0` and from each other, and at the same distances as `0` from
every other point. Call the result `d′`. Then:

- `d′` violates a hypermetric inequality if and only if an exact cover exists;
- this holds if and only if `d′` violates a *pure* one (`b ∈ {0,±1}^{V′}`),
  for example `b = Σ_{i∈T}eᵢ − e_g − Σⱼ e_{0ʲ}`, with value `1/2`;
- this holds if and only if `εd′` violates an odd clique inequality, with
  `ε = 1/N` and `N = 8n + 2p + 1` as in Corollary 3.

So separation of pure hypermetric inequalities of all gonalities, and of odd
clique inequalities, is strongly NP-complete. Membership in NP is trivial.
The numbers in `d′` and `εd′` are bounded as in Corollaries 1 and 3. The hard
points `εd′` are semimetrics with repeated points: `M′` is psd but singular.

Here "odd clique" is the cut-form family of GKL 2012 (`b ∈ {0,±1}^V` with
`σ(b)` odd, the root included). In Letchford (2022, p. 11 and p. 19) these
are the Barahona–Mahjoub clique inequalities (18) and their switchings.
Without the copies, the violators `(2 − q, 𝟙_T, −1)` have root coefficient
`2 − q ∉ {0, ±1}` for `q ≥ 4`, so the root coefficient must be split among
several points. Cut switching cannot do this, because it changes only the
signs of the coefficients. *Exact* copies are not needed, however: Corollary 10
splits the root coefficient among distinct nearby points and keeps the Gram
matrix positive definite. (The round-1 version of this paragraph said that the
repeated points are needed for this family; that was wrong.) No splitting is
needed for the Boolean quadric `{0, ±1}` families (10)–(12), where the root
plays no role (Corollaries 8 and 9).

*Proof.* Since the copies are metrically identical to `0`, merging them gives
`Q(b′, d′) = Q(b, d)`, where `b₀` is the sum of the coefficients of `0` and its
copies. Merging preserves `σ = 1`. In Boolean quadric form with root `0`, the
copies are variables with zero rows, so `X′(ε) = X(ε) ⊕ 0` and
`X′ − ¼e₀e₀ᵀ ⪰ 0`. Hence no rounded psd inequality with `|σ| ≥ 3` is violated.
Odd clique inequalities with `σ = ±1` are pure hypermetric inequalities. ∎

**Corollary 6 (integer QP; proved).** The split note's SPLIT-SEP stays strongly
NP-complete when restricted to rational positive definite `X` with `X₀₀ = 1`
and `Xᵢᵢ = X₀ᵢ` that satisfy all `4·C(N′,2) + 4·C(N′,3)` Boolean quadric
triangle inequalities, including McCormick. Here `N′ = n + 1` is the number of
variables. The hard inputs are the matrices `X(1/N)` of Corollary 3 with
`q ≥ 3`, whose numerators and denominators are at most `4N = O(n + p)`. The
violated splits, `(0, −x, 1)` and `(−1, x, −1)`, have entries in `{0, ±1}`, so
SPLIT-SEP(`𝒱`) is strongly NP-hard for every family `𝒱` that contains the
vectors with `v₀ = 0` and `vᵢ ∈ {0, ±1}`.

This answers the split note's §8 limit "The hard points need not satisfy
binary structure". That note's Corollary 5 placed hard points inside de
Meijer et al.'s ternary families. Corollary 6 places them inside binary
relaxations.

**Corollary 7 (lattice form; proved).** Consider a rational positive definite
Gram matrix of lattice generators `w₁, …, w_r`. Deciding whether the
circumscribed sphere of the simplex `conv{0, w₁, …, w_r}` has a lattice point
strictly inside is strongly NP-complete. This is a restatement of Theorem 1
through §1. In the no-instances many lattice points lie on the sphere, so
the simplex is generally not itself a Delaunay cell. The decided property is
that the vertices lie on a common empty sphere.

**Lemma 6 (switching one variable; proved; added in revision r2).** Let
`(x, y)` be any point of `ℝ^{W ∪ E(W)}`, let `X` be its moment matrix
(`X₀₀ = 1`, `X₀ᵢ = Xᵢᵢ = xᵢ`, `Xᵢⱼ = yᵢⱼ`), and let `g ∈ W`. Let
`ψ_g(x, y) = (x′, y′)` be the switching on `{g}` (Letchford 2022,
Definition 2, pp. 6–7): `x′_g = 1 − x_g`, `y′_ig = xᵢ − y_ig` for `i ≠ g`, and
all other coordinates unchanged. For a Boros–Hammer datum `(v, s)`
(`v ∈ ℤ^W`, `s ∈ ℤ`; inequality (13) of Corollary 8 below), let `v′` be `v`
with `v_g` negated.

- (i) The moment matrix of `ψ_g(x, y)` is `AXAᵀ`, where `A` is the identity
  matrix except that its row `g` is `e₀ − e_g`. Since `A² = I`, `ψ_g`
  preserves positive definiteness and the property `Xᵢᵢ = X₀ᵢ`.
- (ii) The slack of (13) with data `(v, s)` at `ψ_g(x, y)` equals the slack
  of (13) with data `(v′, s − v_g)` at `(x, y)`.
- (iii) Hence `ψ_g` maps the family (12) onto itself, with equal slacks:
  `(S, T, s)` goes to `(S ∖ {g}, T ∪ {g}, s − 1)` if `g ∈ S`, to
  `(S ∪ {g}, T ∖ {g}, s + 1)` if `g ∈ T`, and to itself otherwise.
- (iv) Under the covariance map, `ψ_g` is the cut switching on `{g}`: the cut
  image of `ψ_g(x, y)` is the cut image of `(x, y)` switched on `{g}`.

*Proof.* Put `û = (−s, v)`. Because `X₀₀ = 1`, `X₀ᵢ = Xᵢᵢ = xᵢ` and
`Xᵢⱼ = yᵢⱼ`, `ûᵀXû` is the linearization of `(vᵀx − s)²`, and
`e₀ᵀXû = vᵀx − s`. So the slack of (13) is
`h_X(v, s) = ûᵀXû − e₀ᵀXû`.

- (i) Rows `0` and `i ≠ g` of `A` are unit vectors, so `AXAᵀ` agrees with `X`
  outside row and column `g`. Moreover
  `(AXAᵀ)_gg = (e₀ − e_g)ᵀX(e₀ − e_g) = 1 − 2x_g + x_g = 1 − x_g`,
  `(AXAᵀ)₀g = 1 − x_g` and `(AXAᵀ)ᵢg = xᵢ − y_ig`. These are the entries of
  the moment matrix of `ψ_g(x, y)`.
- (ii) Only row `g` of `A` differs from a unit vector, so
  `Aᵀû = û + û_g(e₀ − 2e_g) = (−(s − v_g), v′)`, and `e₀ᵀA = e₀ᵀ`. Hence
  `h_{AXAᵀ}(v, s) = (Aᵀû)ᵀX(Aᵀû) − e₀ᵀX(Aᵀû) = h_X(v′, s − v_g)`.
- (iii) Apply (ii) to `v = 𝟙_S − 𝟙_T`; (12) is half of (13) for this `v`.
- (iv) The cut image is `z₀ᵢ = xᵢ`, `zᵢⱼ = xᵢ + xⱼ − 2yᵢⱼ`. After `ψ_g`,
  `z′₀g = 1 − x_g = 1 − z₀g` and
  `z′ᵢg = xᵢ + (1 − x_g) − 2(xᵢ − y_ig) = 1 − zᵢg`; all other `z` are
  unchanged. ∎

All four parts hold at every point, not only in the Boolean quadric
polytope. Since `ψ_g` is an affine involution that maps the Boolean quadric
polytope onto itself (Letchford 2022, Prop. 1, p. 7), it maps facets to
facets. Letchford (2022, p. 9) notes that switching a Boros–Hammer
inequality changes the signs of the switched `vᵢ`; the shift of `s` in (ii)
is not stated there.

**Corollary 8 (Padberg's cut inequalities and Letchford's family (12);
proved; added in revision r1).** Use the Boolean quadric variables `xᵢ`
(`i ∈ W`) and `yᵢⱼ` (`i < j`), and Letchford's (2022, §4, pp. 8–9) numbering:

- (11) Padberg's cut inequalities: for disjoint `S, T ⊆ W`,
  `Σ_{i∈S, j∈T} yᵢⱼ ≤ Σ_{i∈T} xᵢ + Σ_{{i,j}⊆S} yᵢⱼ + Σ_{{i,j}⊆T} yᵢⱼ`;
- (12) for disjoint `S, T ⊆ W` and `s ∈ ℤ`,
  `s Σ_S xᵢ + Σ_{S×T} yᵢⱼ ≤ (s+1) Σ_T xᵢ + Σ_{{i,j}⊆S} yᵢⱼ + Σ_{{i,j}⊆T} yᵢⱼ + s(s+1)/2`.
  This is half the linearization of `(ℓ − s)(ℓ − s − 1) ≥ 0` with
  `ℓ = Σ_S xᵢ − Σ_T xᵢ`. It contains Padberg's clique inequalities (10)
  (`T = ∅`) and the cut inequalities (11) (`s = 0`);
- (13) Boros–Hammer: the linearization of `(vᵀx − s)(vᵀx − s − 1) ≥ 0`,
  `v ∈ ℤ^W`, `s ∈ ℤ`. So (12) is (13) with `v = 𝟙_S − 𝟙_T`.

Each problem takes a rational point `(x, y)` and asks whether it violates
some inequality of the family. Separation of (11) and separation of (12) are
strongly NP-complete. Hardness holds at the points `X(1/N)` of Corollary 3
(`xᵢ = Xᵢᵢ`, `yᵢⱼ = Xᵢⱼ`) for X3C instances with `q ≥ K ≥ 3`. These points lie
in `[0,1]^{W ∪ E(W)}`, are positive definite with `Xᵢᵢ = X₀ᵢ`, and satisfy all
Boolean quadric triangle inequalities, including McCormick. They have no
repeated points. At these points the violated members of (12) are exactly the
inequalities with `S` the index set of an exact cover, `T = {g}` and `s = 0`.
These are cut inequalities (11). Each is violated by `1/(4N)` in the scaling
of (12), and each defines a facet of the Boolean quadric polytope.

*Proof.* In split form (split note, §6) the inequality (13) with data
`(v, s)` is the split inequality of the split vector `(s, −v)`, because
`(s − vᵀx)(s − vᵀx + 1) = (vᵀx − s)(vᵀx − s − 1)`. By Corollary 3(d), the
violated splits at `X(1/N)` are exactly `(0, −x, 1)` and `(−1, x, −1)` for the
exact covers `x`.

- The first is `(s, −v)` with `s = 0` and `v = 𝟙_C − e_g`, where `C` is the
  cover. That is (12) with `S = C`, `T = {g}`, `s = 0`, and so the cut
  inequality (11) `Σ_{i∈C} y_ig ≤ x_g + Σ_{{i,j}⊆C} yᵢⱼ`.
- The second is `(s, −v)` with `s = −1` and `v = e_g − 𝟙_C`. It gives the same
  inequality, since `(ℓ + 1)ℓ = (−ℓ)(−ℓ − 1)`.

Hence, at these points, some (11) is violated if and only if some (12) is
violated, if and only if some (13) is violated, if and only if an exact cover
exists. The split value is `−1/(2N)`, and (12) is half the linearized product
with the opposite sign, so the violation of (12) is `1/(4N)`. The numbers are
polynomially bounded by Corollary 3(c), so hardness is strong. The Boolean
quadric triangle inequalities, including McCormick and `yᵢⱼ ≥ 0`, are among
the members of (12) with `|S| + |T| ≤ 3` (Letchford 2022, p. 8). The
violators have `|S| + |T| = q + 1 ≥ 4`, so all members with `|S| + |T| ≤ 3`
hold when `q ≥ 3`.

Membership in NP: for (11) the certificate is `(S, T)`. For (12), fix
`(S, T)`. Then LHS − RHS is `f(s) = −s²/2 + s(ℓ − 1/2) + c` for a constant `c`.
This is a concave quadratic in `s`, and its maximum over the integers is at
`s = ⌊ℓ⌋`. So `(S, T)` is again a certificate. For (13), see Corollary 4(iii).

Facets: Letchford (2022, p. 9) states that (12) defines a facet when
`|S| + |T| ≥ 3` and `1 − |T| ≤ s ≤ |S| − 2`. The violators have `|S| = q ≥ 2`,
`|T| = 1` and `s = 0`. The same conclusion also follows from Padberg's clique
theorem. Switching on `{g}` (`x_g ↦ 1 − x_g`, `y_ig ↦ xᵢ − y_ig`) is an affine
automorphism of the Boolean quadric polytope. By Lemma 6(ii), it relates the
Boros–Hammer data `(v, s)` and `(v′, s − v_g)`, where `v′` is `v` with the
sign of `v_g` changed. So the violator `(𝟙_C − e_g, 0)` is the switching of
the clique inequality (10) with `S′ = C ∪ {g}` and `s′ = 1`.
Padberg showed that (10) defines a facet when `|S′| ≥ 3` and
`1 ≤ s′ ≤ |S′| − 2` (cited as in Letchford 2022, p. 8). Here `|S′| = q + 1 ≥ 3`
and `s′ = 1 ≤ q − 1`. An exact rank computation confirms facetness for
`q = 2, …, 6` in `BQP_{q+1}`, and for `q = 2, 3, 4` with two further unused
variables (§10). ∎

*Remarks.*

- Letchford (2022, §7.2, p. 18) wrote that the complexity of separating
  (10)–(13) "is unknown, but we suspect that they are all NP-hard".
  Corollaries 4(iii) and 8 confirm this for (11), (12) and (13), and
  Corollary 9 below confirms it for Padberg's clique inequalities (10). (The
  round-1 version of this remark said that (10) remains open because its
  vectors `v = 𝟙_S` have only positive entries while the violators here have
  mixed signs. That reason fails, because the input point can be switched;
  review round 2 pointed this out.)
- Letchford's printed facet condition for (11) (p. 8: "They induce facets when
  `|S| ≥ 1` and `|T| ≥ 2`") does not match the printed form of (11) or the
  condition for (12) at `s = 0`, which gives `|S| ≥ 2` and `|T| ≥ 1`. For
  `|S| = 1` and `|T| ≥ 2`, the printed (11) is the sum of the McCormick
  inequalities `y_ij ≤ x_j` (`j ∈ T`) and the inequalities `y_jk ≥ 0`
  (`{j,k} ⊆ T`), so it is not a facet. The exact check in §10 agrees: (11)
  with `(|S|, |T|) = (1, 2)` or `(1, 3)` is not a facet, while `(2, 1)`,
  `(3, 1)` and `(2, 2)` are. The chapter's own remark on p. 8, that (11) with
  `|S| = 2` and `|T| = 1` reduces to the triangle inequality (9), agrees with
  the printed formula. Review round 2 reports that Padberg's cut inequalities
  are commonly cited with `x(S)` instead of `x(T)` on the right-hand side,
  and the printed condition fits that orientation (I did not check Padberg
  1989). In that orientation, (11) with `(|S|, |T|) = (a, b)` is the printed
  (11) with `(b, a)` after renaming, so the exact check shows that it is a
  facet for `(1, 2)`, `(1, 3)` and `(2, 2)`. So either the formula or the
  condition was transposed in the chapter. This does not affect Corollary 8,
  which uses the condition for (12).

**Corollary 9 (Padberg's clique inequalities (10); proved; added in revision
r2).** Padberg's clique inequalities are

`s Σ_{i∈S} xᵢ ≤ Σ_{{i,j}⊆S} yᵢⱼ + s(s+1)/2`  for `S ⊆ W` and `s = 0, …, |S| − 1`

(Letchford 2022, (10), p. 8). They are the members of (12) with `T = ∅`.
Separation of (10) (given a rational point `(x, y)`, is some (10) violated?)
is strongly NP-complete. Hardness holds at the points `P′ = ψ_g(X(1/N))` for
X3C instances with `q ≥ K ≥ 3`, where `X(1/N)` is the point of Corollary 3 and
`ψ_g` is the switching on `{g}` of Lemma 6. These points have the following
properties.

- (a) `P′` agrees with `X(1/N)` except that `x′_g = 1 − (2p − 1)/(4N)` and
  `y′_ig = (4 + |Sᵢ|/2)/N` (`= 22/(4N)` for X3C). It lies in
  `[0,1]^{W ∪ E(W)}`, its moment matrix is positive definite with
  `X′ᵢᵢ = X′₀ᵢ`, and `4N·P′` is integral with entries at most `4N`.
- (b) The violated Boros–Hammer inequalities at `P′` are exactly
  `(v, s) = (𝟙_C + e_g, 1)` and its other form `(−𝟙_C − e_g, −2)`, for the
  exact covers `C`. Hence the violated clique inequalities are exactly those
  with `S′ = C ∪ {g}` and `s′ = 1`, and these are also the only violated
  members of (12). Each is violated by `1/(4N)`.
- (c) `P′` satisfies every Boros–Hammer inequality with `|supp v| ≤ q`, in
  particular all Boolean quadric triangle inequalities, including McCormick.
- (d) The violated clique inequalities define facets of the Boolean quadric
  polytope.
- (e) The cut image of `P′` is `εd` switched on `{g}`. It lies in the
  interior of the elliptope and in the metric polytope, and it satisfies
  every rounded psd inequality of gonality at most `2q − 3`.

*Proof.*

- (a) By Lemma 6(i), the moment matrix of `P′` is `AX(1/N)Aᵀ`. It is
  positive definite with `X′ᵢᵢ = X′₀ᵢ` by Corollary 3(c). The changed entries
  are `1 − εM_gg` with `M_gg = p/4 + (p − 1)/4 = (2p − 1)/4`, and
  `ε(Mᵢᵢ − M_ig) = ε(4 + |Sᵢ| − |Sᵢ|/2)`. All entries lie in `[0, 1]`, since
  `4 + |Sᵢ|/2 < N` and `(2p − 1)/4 < N`. The matrix
  `4N·AXAᵀ = A(4N·X)Aᵀ` is integral because `A` is.
- (b) By Corollary 3(d) and the dictionary in the proof of Corollary 8, the
  violated Boros–Hammer data at `X(1/N)` are exactly `(𝟙_C − e_g, 0)` and
  `(e_g − 𝟙_C, −1)`, with slack `−1/(2N)`. By Lemma 6(ii), `(v, s)` is
  violated at `P′` if and only if `(v′, s − v_g)` is violated at `X(1/N)`,
  with the same slack. Solving `(v′, s − v_g) = (𝟙_C − e_g, 0)` gives
  `v = 𝟙_C + e_g` and `s = 1`. Solving `(v′, s − v_g) = (e_g − 𝟙_C, −1)`
  gives `v = −𝟙_C − e_g` and `s = −2`. Both give the same inequality, because
  `(ℓ − 1)(ℓ − 2) = (−ℓ + 2)(−ℓ + 1)`. A clique inequality is half of (13)
  with `v = 𝟙_S`, so the only violated ones are `S′ = C ∪ {g}` with
  `s′ = 1`, and `s′` lies in the range `0, …, |S′| − 1`. The members of (12)
  are halves of (13) with `v ∈ {0, ±1}^W`, so the same argument applies to
  them. Halving turns the slack `−1/(2N)` into a violation of `1/(4N)`.
- (c) The violators have support `q + 1 ≥ 4`. The triangle inequalities are
  members of (12) with `|S| + |T| ≤ 3` (Letchford 2022, p. 8).
- (d) Here `|S′| = q + 1 ≥ 3` and `1 ≤ s′ ≤ |S′| − 2`, which is Padberg's
  facet condition (cited through Letchford 2022, p. 8). Independently, the
  violator is the image under `ψ_g` of the facet-defining violator of
  Corollary 8, and `ψ_g` maps facets to facets (Lemma 6). An exact rank
  computation confirms facetness for `q = 2, …, 6` (§10).
- (e) Lemma 6(iv) gives the cut image. Cut switching acts on the ±1 form
  `Z = J − 2D` as a congruence `Z ↦ ΣZΣ` with `Σ` diagonal with entries
  `±1`. So it preserves the interior of the elliptope, and it maps each
  rounded psd inequality `b` to the rounded psd inequality `Σb` of the same
  gonality, with the same violation (see the proof of Corollary 10(d)). In
  particular it maps the triangle and perimeter inequalities onto
  themselves. Now apply Corollary 3(b), (d) and (e) to `εd`.

Membership in NP: the certificate is `S`; for each of the `|S|` values of
`s`, the slack is computed directly. Strong hardness follows from (a), since
X3C is strongly NP-complete. ∎

*Remark (relation to (18); proved).* By the split identity of §1 and the
dictionary in the proof of Corollary 8, the cut image of the clique
inequality (10) with data `(S, s)` is the rounded psd inequality with
`b = −(2s + 1 − |S|, 𝟙_S)` (root first), with the same slack up to the factor
`1/2` of (10); §10 checks this identity exactly. This `b` is an inequality
(18) only if `2s + 1 − |S| ∈ {0, 1}`: for odd `|S|` and `s = (|S| − 1)/2` it
is (18) on `S`, which is Letchford's derivation (2022, p. 11), and for even
`|S|` and `s = |S|/2` it is (18) on `S ∪ {0}`. It is an odd clique inequality
only if `|2s + 1 − |S|| ≤ 1`. At `P′`, `S′ = C ∪ {g}` and `s′ = 1` give the
root coefficient `q − 2` in absolute value. So for `q ≥ 3` the violated
clique inequalities of Corollary 9 are not of the form (18), and for `q ≥ 4`
they are not odd clique inequalities. Corollary 9 therefore does not settle
(18); Corollary 10 does. (The round-1 version called (18) "the cut images"
of (10). That was inaccurate, as review round 2 pointed out: (18) comes only
from the subfamilies just described.)

**Corollary 10 (odd clique, pure hypermetric and Barahona–Mahjoub clique
inequalities at positive definite points; proved; added in revision r2).**
Take an X3C instance with `q ≥ 3`, `η² = (p − 1)/4` and `M` as in §3. Put
`m = q − 2`, `τ² = 1/(8q)`, `N = 8n + 2p + 1` and `ε = 1/N`. Add `m` new
indices `o₁, …, o_m`, and let `M̃ = M ⊕ τ²I_m` on `W̃ = W ∪ {o₁, …, o_m}`. Let
`d̃ = d(M̃)` be the corresponding distance on `Ṽ = {0} ∪ W̃`. Explicitly, `d̃`
agrees with `d` on `V`, and

`d̃(0, oⱼ) = τ²`,   `d̃(oⱼ, oₖ) = 2τ²` (`j ≠ k`),   `d̃(oⱼ, u) = d(0, u) + τ²` (`u ∈ W`).

In an `ℓ₂²` representation, `oⱼ` is the point `0` moved by `τ` in a new
orthogonal direction; Corollary 5 is the degenerate case `τ = 0`. Let `d″` be
the switching of `εd̃` on `U = {g, o₁, …, o_m}`. Write vectors `b ∈ ℤ^Ṽ` in
the order (root `0`, the `n` sets, `g`, `o₁, …, o_m`).

- (a) `M̃ ≻ 0`. The hypermetric inequalities violated by `d̃` are exactly
  those with `b = (2 − q − Σw, 𝟙_C, −1, w)`, where `C` is an exact cover and
  `w ∈ ℤ^m` satisfies `Σⱼ wⱼ(wⱼ − 1) < 4q`. Each has gonality at least
  `2q − 1`.
- (b) The Boolean quadric point `X̃(ε) = [[1, εδ̃ᵀ], [εδ̃, εM̃]]`, with
  `δ̃ = diag(M̃)`, is positive definite with `X̃ᵢᵢ = X̃₀ᵢ`, and
  `X̃(ε) − ¼e₀e₀ᵀ ≻ 0`. The matrix `8qN·X̃(ε)` is integral with entries at
  most `8qN`. The cut image `εd̃` lies in `(0, 1)^{E(Ṽ)}`, in the interior of
  the elliptope and in the metric polytope. It violates no rounded psd
  inequality with `|σ| ≥ 3` and none of gonality at most `2q − 3`.
- (c) `εd̃` violates an odd clique inequality if and only if an exact cover
  exists, and if and only if it violates a pure hypermetric inequality. For
  a cover `C`, the vector `b* = (0, 𝟙_C, −1, −𝟙_m)` gives such an
  inequality, violated by `εQ(b*, d̃) = (q + 2)/(4qN)`.
  The pure hypermetric violators for `C` are exactly `b*` and the `m` vectors
  `(−1, 𝟙_C, −1, −𝟙_m + e_j)`, `j = 1, …, m`; the latter maximize the
  violation over both the pure hypermetric and odd clique families, with
  value `(q + 3)/(4qN)`.
- (d) `d″` lies in `(0, 1)^{E(Ṽ)}`, in the interior of the elliptope and in
  the metric polytope; `8qN·d″` is integral, and `d″` satisfies every
  rounded psd inequality of gonality at most `2q − 3`. It violates a
  Barahona–Mahjoub clique inequality (18) if and only if an exact cover
  exists. The violated ones are exactly those with `S = C ∪ U` for the exact
  covers `C`. They have `|S| = 2q − 1` and are violated by `(q + 2)/(4qN)`.
- (e) The violated inequalities of (c) (for `b*`) and of (d) define facets of
  the cut polytope.

Hence separation of the odd clique inequalities in cut form (the inequalities
(18) and their switchings), of the inequalities (18) alone, and of the pure
hypermetric inequalities is strongly NP-complete. This holds even at points in
the interior of the elliptope (equivalently, with positive definite Boolean
quadric form) that lie in the metric polytope and satisfy every rounded psd
inequality up to any fixed gonality (take `q ≥ K`). Membership in NP is
trivial: the certificate is `b` or `S`.

*Proof.*

- (a) `M̃` is block diagonal with positive definite blocks. By Lemma 0,
  hypermetric vectors correspond to `(z, w) ∈ ℤ^{W̃}` through
  `b = (1 − Σz − Σw, z, w)`, and
  `g_M̃(z, w) = g_M(z) + τ² Σⱼ wⱼ(wⱼ − 1)`. The second term is nonnegative
  for integers. So a violator has `g_M(z) < 0`, that is, `z = (𝟙_C, −1)` with
  `g_M(z) = −1/2` by Theorem 1. Then `g_M̃(z, w) < 0` if and only if
  `Σⱼ wⱼ(wⱼ − 1) < 1/(2τ²) = 4q`. Since `|C| = q`, `b₀ = 2 − q − Σw`. The
  gonality is `|2 − q − Σw| + Σⱼ|wⱼ| + q + 1 ≥ (q − 2) + q + 1`, because
  `|2 − q − Σw| + |Σw| ≥ q − 2`.
- (b) `δ̃ = (δ, τ²𝟙_m)`, so `s̃ = δ̃ᵀM̃⁻¹δ̃ = s + mτ²`. By Lemma 5, `εs < 1/2`,
  and `εmτ² = (q − 2)/(8qN) < 1/(8N)`. So `εs̃ < 3/4`, and the Schur
  complement argument of Corollary 3(c) gives `X̃(ε) − θe₀e₀ᵀ ≻ 0` for
  `θ = 0` and `θ = 1/4`. The entries of `εM` have denominators dividing
  `4N`, and `ετ² = 1/(8qN)`; all entries lie in `[0, 1]`. The congruence
  `J − 2εD̃ = LX̃(ε)Lᵀ` of Corollary 3(e) gives the elliptope statement and
  `0 < εd̃ < 1`. Rounded psd inequalities with `|σ| ≥ 3` hold by the argument
  of Corollary 3(d). Those with `σ = ±1` are hypermetric inequalities (up to
  the sign of `b`), so by (a) and homogeneity the violated ones have gonality
  at least `2q − 1`. Triangle inequalities have gonality `3 ≤ 2q − 3`, and
  perimeter inequalities have `σ = 3`.
- (c) If `C` is a cover, `b*` is the vector of (a) with `w = −𝟙_m`, for which
  `Σⱼ wⱼ(wⱼ − 1) = 2(q − 2) < 4q`. It has entries in `{0, ±1}` and
  `σ(b*) = 1`, so it is both a pure hypermetric and an odd clique
  inequality, and `Q(b*, d̃) = −g_M̃ = 1/2 − 2(q − 2)τ² = (q + 2)/(4q)`.
  Conversely, a violated odd clique inequality is a violated rounded psd
  inequality, so by (b) it has `σ = ±1`. Then `±b` is a hypermetric
  inequality violated by `d̃`, and (a) gives a cover. Pure hypermetric
  inequalities are odd clique inequalities. For a pure violator, let `a`
  entries of `w` equal `1` and `k` equal `−1`. The root coefficient is
  `2 − q − a + k ∈ {0, ±1}`, so `k − a ≥ q − 3 = m − 1`, while
  `k + a ≤ m`. Thus `a = 0` and `k ∈ {m − 1, m}`, giving exactly the
  listed vectors. For `k = m − 1` the violation is
  `ε(1/2 − 2(q − 3)τ²) = (q + 3)/(4qN)`, larger than that of `b*`.
  By (b), odd clique violators are these vectors and their negatives, with
  equal violations.
- (d) In the ±1 form `Z = J − 2D`, switching on `U` is the congruence
  `Z″ = ΣZ̃Σ`, where `Z̃ = J − 2εD̃` and `Σ = diag(s)` with `s_u = −1` for
  `u ∈ U` and `s_u = 1` otherwise. So `Z″ ≻ 0`, which gives the elliptope
  statement and `0 < d″ < 1`. The entries `εd̃` and `1 − εd̃` have
  denominators dividing `8qN`. A rounded psd inequality reads `bᵀZb ≥ 1`
  with `σ(b)` odd, because `bᵀ(J − 2D)b = σ(b)² − 4Q(b, d)`. The map
  `b ↦ Σb` preserves the parity of `σ`, the support and the set
  `{0, ±1}^Ṽ`, and `(Σb)ᵀZ″(Σb) = bᵀZ̃b`. So `Σb` violates a rounded psd
  inequality at `d″` if and only if `b` violates one at `εd̃`, by the same
  amount. With (b), this gives the gonality statement and the triangle and
  perimeter inequalities (the rounded psd inequalities with `b ∈ {±1}` on
  three points). An inequality (18) is the rounded psd inequality with
  `b = ±𝟙_S`. By (a) and (b), the violated rounded psd inequalities at `d″`
  have vectors `Σb = ±(2 − q − Σw, 𝟙_C, 1, −w)`. Such a vector is of the
  form `±𝟙_S` only if `w ∈ {0, −1}^m` and `2 − q − Σw ∈ {0, 1}`. If `k`
  entries of `w` equal `−1`, the second condition reads `2 − q + k ∈ {0, 1}`.
  Since `k ≤ q − 2`, this forces `k = q − 2`, that is, `w = −𝟙_m` and
  `b₀ = 0`. Then `Σb = ±𝟙_{C∪U}`, and `w = −𝟙_m` satisfies the bound of (a).
  The violation of (18) is
  `Q(𝟙_S, d″) − (|S|² − 1)/4 = (1 − 𝟙_SᵀZ″𝟙_S)/4 = (1 − b*ᵀZ̃b*)/4 = εQ(b*, d̃)`,
  since `Σ𝟙_{C∪U} = b*`.
- (e) The covariance map is a linear bijection that maps the Boolean quadric
  polytope onto the cut polytope (Letchford 2022, Theorem 1, p. 11), so it
  maps facets to facets. Under it, the clique inequality (10) with `|S|` odd
  and `s = (|S| − 1)/2` becomes (18) for a set `S` that does not contain the
  root (Letchford 2022, p. 11). Padberg's condition `1 ≤ s ≤ |S| − 2` holds
  for odd `|S| ≥ 3`. The cut polytope is invariant under permutations of the
  points, so every (18) with odd `|S| ≥ 3` defines a facet; here
  `|S| = 2q − 1 ≥ 5`. The odd clique inequality of `b*` is the switching of
  (18) with `S = C ∪ U` on `U`, and switching maps facets to facets. Exact
  rank computations for `|S| = 3, 5, 7, 9` agree (§10). ∎

*Remarks.*

- Some authors include even-`|S|` sets in the Barahona–Mahjoub clique family,
  with right-hand side `⌊|S|²/4⌋`; those members are psd inequalities and
  hold at `d″` (strictly for nonempty `S`), so the result holds under either
  definition.
- The lift must be small. With `τ² = 1/4` instead of `1/(8q)`, the proof of
  (a) shows that every violator has `w ∈ {0, 1}^m`, because each `wⱼ = −1`
  or `wⱼ ≥ 2` adds at least `2τ² = 1/2`. So `b₀ = 2 − q − Σw ≤ 2 − q`, and
  for `q ≥ 4` no violator is pure. The proof of (b) still applies, because
  `εmτ² = (q − 2)/(4N) < 1/4`. So no odd clique inequality is violated, even
  when an exact cover exists. §10 confirms this control on 10 instances with
  a cover.
- Review round 2 observed that switching Corollary 5's points on `{g}` and
  the exact copies settles (18) at points with repeated points (its exact
  check [H]). Corollary 10(d) is the same switching applied to the lifted
  copies; the switched points have a positive definite Gram matrix.

## 6. Gap-0 and general gap inequalities

Let `x ∈ ℚ^{E(V)}` with `|V| = n`, and let `Z = J − 2X` (unit diagonal). Gap
inequalities read `bᵀZb ≥ γ(b)²`.

**Lemma 4 (proved).** `x` violates a gap-0 inequality if and only if
`Z|_{s⊥}` is not psd for some `s ∈ {±1}ⁿ`. In particular, gap-0 inequalities
never cut a psd point. They are the psd inequalities restricted to vectors `b`
with `γ(b) = 0`.

*Proof.* `γ(b) = 0` means `sᵀb = 0` for some `s`. If `Z|_{s⊥}` is not psd, the
open cone `{b ∈ s⊥ : bᵀZb < 0}` is a nonempty open subset of a rational
subspace, so it contains integral points. The converse is immediate. ∎

**Theorem 4 (gap-0 separation is NP-complete; proved).** Deciding whether a
rational `x` violates a gap-0 inequality is NP-complete. Strong
NP-completeness is not shown.

*Construction.* PARTITION is NP-complete (Karp 1972), and it reduces to
PARTITION with equal cardinalities: append `m` zeros to an instance with `m`
numbers. So start from `c ∈ ℤⁿ_{≥0}` with `n ≥ 4` even and `C = Σc > 0`,
and ask for `s ∈ {±1}ⁿ` with `sᵀc = 0` and `sᵀ𝟙 = 0`. Set:

- `a = c + K𝟙` with `K = 4nC`, and `A₂ = ‖a‖²`;
- `θ_lb = (2(n−1)a_min² − (n+1)a_max²)/((n−1)(n−2))`, which is positive
  because `a_max/a_min ≤ (K + C)/K = 1 + 1/(4n)` and
  `(n+1)(1 + 1/(4n))² < 2(n−1)` for `n ≥ 4`;
- `ν = θ_lb/(A₂a_max²)`;
- `ρᵢ = aᵢ²(1 + νaᵢ²/A₂)` and `Δ = Σρᵢ`;
- for `i ≠ j`, `θᵢⱼ = (ρᵢ + ρⱼ)/(n−2) − Δ/((n−1)(n−2))`;
- `Z = D_a⁻¹ L_θ D_a⁻¹ − ν aaᵀ/A₂`, where `L_θ` is the Laplacian of the
  weights `θ`.

*Proof.*

- **The weights.** `θᵢⱼ ≥ (2(n−1)ρ_min − nρ_max)/((n−1)(n−2)) ≥ θ_lb > 0`,
  because `ρᵢ + ρⱼ ≥ 2ρ_min`, `Δ ≤ nρ_max`, `ρ_min ≥ a_min²` and
  `ρ_max ≤ a_max²(1 + ν) ≤ a_max²(1 + 1/n)`. Here
  `ν ≤ 1/(n(n−1)a_max²)`, because `θ_lb ≤ a_min²/(n−1)` and `A₂ ≥ na_min²`;
  `θ_lb` depends only on `a`, so the definitions are not circular. The row sums of `θ` are exactly
  `ρᵢ`: `Σ_{j≠i} θᵢⱼ = ((n−1)ρᵢ + Δ − ρᵢ)/(n−2) − Δ/(n−2) = ρᵢ`.
- **The point.** `Zᵢᵢ = ρᵢ/aᵢ² − νaᵢ²/A₂ = 1`. `Za = −νa`, because
  `L_θ𝟙 = 0`. So `Z` is the ±1 form of a rational point `x`.
- **Positive part.** For `b ⊥ a`, put `c′ = D_a⁻¹b`. Then
  `Σaᵢ²(c′ᵢ − t)² = ‖b‖² + t²A₂ ≥ ‖b‖²` for every `t`, and
  `L_θ ⪰ nθ_lb(I − 𝟙𝟙ᵀ/n)`. Together these give
  `bᵀZb ≥ (nθ_lb/a_max²)‖b‖²`.
- **(⇐)** If `sᵀa = 0`, then `b = a` has `γ = 0` and `aᵀZa = −νA₂ < 0`.
- **(⇒)** Suppose `sᵀb = 0` and `bᵀZb < 0`. Write `b = ta + b_⊥` with
  `b_⊥ ⊥ a`. Then `bᵀZb = −νt²A₂ + b_⊥ᵀZb_⊥`, so `t ≠ 0` and
  `‖b_⊥‖²/t² < νA₂a_max²/(nθ_lb)`. From `t sᵀa = −sᵀb_⊥`,
  `|sᵀa| ≤ √n‖b_⊥‖/|t| < (νA₂a_max²/θ_lb)^{1/2} = 1`, so `sᵀa = 0`.
- **Back to partition.** Since `|sᵀc| ≤ C < K` and `sᵀ𝟙` is even, `sᵀa = 0`
  holds if and only if `sᵀ𝟙 = 0` and `sᵀc = 0`.
- **Membership in NP.** Guess `s`. Exact elimination on a rational basis of
  `s⊥` (split note, Lemma 4) certifies that `Z|_{s⊥}` is not psd and yields an
  integral `b` of polynomial size. ∎

*Remark (location; proved for `n ≥ 6`, checked for `n ∈ {6, 8}`).* Every
`x_uv = ½ + θ_uv/(2a_ua_v) + νa_ua_v/(2A₂)` lies in `(½, 1)`, so the inequalities
`x_uv ≤ x_uw + x_vw` hold. For the perimeter inequalities use
`θ_uv/(a_ua_v) ≤ θ_uv/a_min² ≤ (2(n−1)(1+ν)r² − n)/((n−1)(n−2))` with
`r = a_max/a_min ≤ 1 + 1/(4n)`, and `ν ≤ 1/(n(n−1)K²)` with `K ≥ 4n`. For
`n ≥ 6` these give `(1+ν)r² ≤ 1 + 0.6/n`, hence `θ_uv/(a_ua_v) < (n − 0.8)/((n−1)(n−2))`,
and `νa_ua_v/A₂ ≤ νr²/n < 0.001/n`. So
`x_uv + x_uw + x_vw < 3/2 + ½(3(n − 0.8)/((n−1)(n−2)) + 0.003/n) < 2`, since
`3(n − 0.8)/((n−1)(n−2)) ≤ 0.78` for `n ≥ 6`. So the gap-0 hard points satisfy all triangle inequalities. They
violate psd only slightly: the smallest eigenvalue is `−ν`.

**General gap inequalities.**

- At a non-psd point some integral `b` has `bᵀZb < 0 ≤ γ(b)²`. So the
  decision version is trivially "yes". Writing down the violated inequality
  needs `γ(b)`, which can be NP-hard to compute (GKL 2012, Lemma 2).
- At psd points the complexity remains open. Theorem 1 does not settle it:
  at the scaled hard points, gap inequalities with `γ ≥ 3` are not
  controlled.
- *Numerical evidence (box search, not a proof).* No violated gap inequality
  was found at `εd` (`ε = 1/(8n + 2p + 1)`) for 48 no-instances with 4–8
  points and coefficients in `[−3,3]` (`[−2,2]` for 8 points). The round-0
  run with `ε = 1/(2s)` gave the same result on the same instances. For at
  most 6 points the outcome already follows from Corollary 3(d) and known
  results (§10, item 4), so only the 21 runs with 7 or 8 points carry
  information.
- In 24 other random no-instances with 7–10 points, `εd` lay in the cut
  polytope (24 of 24, floating-point LP), so no valid inequality at all was
  violated there. This cannot hold for all no-instances unless NP = co-NP.
  If it did, a convex combination of at most `|E(V)| + 1` cuts
  (Carathéodory) would certify that no exact cover exists.

## 7. Comparison with earlier notes and prior work; novelty

**The split note.** The split note proves strong NP-completeness of split
separation by a lattice argument: subset sum or X3C, CVP, and Kannan's
embedding with a doubled target. Its §6 explains why that argument fails in
the binary case: the generators were placed freely, with `⟨b₀, bᵢ⟩ = 0`.
Theorem 1 uses the same tools, but starts from the exact-cover form of CVP
hardness, with basis `[A; 2I]` and target `𝟙`. It adds one generator `u_g`
whose coordinate `η` plays the role of Kannan's embedding coordinate. The
layer analysis over `k` mirrors the split note's case analysis over `m` in
Lemma 2, and the window for `η²` mirrors its threshold for `h²`. The exact
checks reuse the split note's Fincke–Pohst approach.

Other connections:

- The binary points of Corollary 3 let the split note's Theorem 2 serve as
  the NP-membership proof for rounded psd separation.
- The split note's Lemma 4 serves for the non-psd cases.
- Corollary 6 strengthens the split note's Corollary 5 in a different
  direction.

The other starting results of this continuation, the S-free intersection cuts
and the three-variable cube family, do not interact with this note.

**Prior work.**

- *Avis–Grishukhin (1993).* They prove co-NP-completeness for fixed gonality
  `2m+1` with `m` in the input, and NP-hardness of finding the smallest
  violated gonality. Their instances control only gonality at most `2m+1`.
- *Avis (2003).* He shows that the same special-case results hold for
  negative type inequalities, whose separation is polynomial. He reads this
  as casting "some doubt on the evidence that hypermetric separation is
  hard". Theorem 1 resolves that doubt in the direction of hardness.
- *Letchford–Sørensen (2012) and GKL (2012).* They reduce rounded psd and
  Boros–Hammer separation to hypermetric separation. Theorem 1 supplies the
  missing hardness for all of these. GKL's NP-membership results (Lemmas 1
  and 6) complete the NP-completeness statements.
- *Letchford (2022).* This survey chapter is the most recent statement of
  openness that I found (§2 table). It conjectures that separation of
  Padberg's clique and cut inequalities, of their common generalization (12)
  and of the Boros–Hammer inequalities is NP-hard. Corollaries 4(iii), 8 and
  9 prove this for all four families (10)–(13). It also lists the separation
  complexity of the remaining cut-polytope inequalities as unknown, among
  them the Barahona–Mahjoub clique inequalities (18) and their switchings,
  the rounded psd inequalities (19), the hypermetric inequalities (23) and
  the gap inequalities. Corollaries 4 and 10 settle all of these except the
  gap inequalities at psd points.
- *Dey, Jiang, Kazachkov, Lodi and Muñoz (arXiv:2604.00932, April 2026).*
  They separate Boros–Hammer inequalities by solving a nonconvex integer QP
  with Gurobi, with coefficients bounded by 2 in absolute value (§4.1.2,
  p. 16). They make no complexity statement about the full class; on p. 4
  they recall that Boros and Hammer gave polynomial-time separation for
  certain subclasses (by minimum spanning trees). This is consistent with the
  question being treated as open in 2026.
- *Exact-cover form of CVP.* It appears, for example, in Vaikuntanathan's
  2015 lecture notes (Lecture 9, basis `[QA; I]`), which credit the
  exact-set-cover hardness to Goldwasser et al. The Micciancio–Goldwasser
  book was not checked. Kannan (1987) introduced the embedding.

**Novelty.** No source examined proves Theorem 1, Corollaries 4–6 and 8–10,
or Theorem 4. The examined sources are those in the manifest; the arXiv results
for "hypermetric" (20 entries, 2001–2026, titles scanned and three Dutour
Sikirić papers grepped); BiqBin (arXiv:2009.06240) and MADAM
(arXiv:2010.07839); Letchford–Sørensen 2014; Moura–Yaman–Leus (arXiv:2401.01716);
Hosseinian–Butenko (arXiv:1904.12025); and Dutour Sikirić–Schürmann–Vallentin
(arXiv:0804.0036). Several web searches for statements of NP-hardness or
co-NP-completeness of hypermetricity found only the sources in §2. In the
revision I added Letchford (2022) and Dey et al. (2026), both found by the
reviewer. Two web searches for the separation complexity of Padberg's cut and
clique inequalities and of the Boros–Hammer inequalities found no hardness
result. One hit, de Vries–Perscheid (J. Glob. Optim. 84, 2022), was checked
through its abstract page and makes no complexity claim about these
separation problems. In the second revision, two more web searches
(separation complexity of the Barahona–Mahjoub clique inequalities; NP-hardness
of odd clique or hypermetric separation, 2024–2026) returned only result
titles and snippets: the Barahona–Mahjoub paper, Letchford's papers already
in the manifest, odd-cycle separation papers and a 2024 talk on heuristic
rounded psd separation for max-cut. None of the snippets claims a hardness
result for these classes; the full texts were not opened. The reviewer's two
round-2 searches (review round 2, "Literature additions") also found no
earlier resolution.

Not checked:

- Deza–Laurent 1997, full text (§28.3 and p. 454, cited by Avis 2003);
- Deza–Grishukhin, "Voronoi L-decomposition of PSD_n and the hypermetric
  correlation cone";
- Laurent–Poljak 1996 (the gap paper); Boros–Hammer 1993; Avis–Umemoto 2003;
  Giandomenico–Letchford 2006; Erdahl 1992;
- Dash's thesis; the Micciancio–Goldwasser book.

Because the proof is short and uses standard parts, it may be known to
specialists. The defensible claim is: "not found in the sources checked; the
sources from 1993 to 2022 state it as open, the latest being Letchford's 2022
survey".

## 8. Corrected status for a paper, and corrections to earlier notes

**Paragraph for a discussion section.**

> For binary problems the corresponding inequalities are the rounded psd
> inequalities for the cut polytope (Boros–Hammer inequalities in Boolean
> quadric form), which contain the gap-1 and hypermetric inequalities
> (Galli–Kaparis–Letchford 2012, §2; Letchford–Sørensen 2012, (8)–(10)).
> Rounded psd separation reduces to hypermetric separation
> (Letchford–Sørensen 2012, Prop. 19). The complexity of hypermetric
> separation was stated as open by Avis–Grishukhin (1993, §4), Deza,
> Grishukhin and Laurent (1993, Remark 4.12), Deza–Laurent (1997, Ch. 28),
> Avis (2003, §1), Letchford–Sørensen (2012, p. 269), Galli–Kaparis–Letchford
> (2012, §4, p. 151) and Letchford (2022, §7.2 and §8). Letchford (2022,
> §7.2, pp. 18–19) also lists as unknown the separation complexity of
> Padberg's clique and cut inequalities, of their common generalization and
> of the Boros–Hammer inequalities, which he suspects to be NP-hard, and of
> the remaining cut-polytope inequalities, including the Barahona–Mahjoub
> clique inequalities and their switchings. A reduction from exact cover by
> 3-sets shows that hypermetric separation is strongly NP-complete: deciding
> whether a rational distance violates a hypermetric inequality is strongly
> NP-complete, equivalently membership in the hypermetric cone is strongly
> co-NP-complete. This holds even for distances of negative type with
> positive definite Gram matrix that satisfy all triangle inequalities and
> all hypermetric inequalities of bounded gonality. After scaling by
> `1/(8n + 2p + 1)`, the hard points are positive definite Boolean quadric
> points (`Xᵢᵢ = X₀ᵢ`) in the metric polytope, with numbers of polynomial
> size. So separation of rounded psd, gap-1 and Boros–Hammer inequalities,
> of Padberg's cut inequalities and of their generalization (12) of
> Letchford (2022) is strongly NP-complete as well, and at these points the
> violated inequalities are facet-defining cut inequalities. Switching the
> hard points on one variable turns the violated cut inequalities into
> facet-defining clique inequalities, so separation of Padberg's clique
> inequalities is strongly NP-complete too. Adding `q − 2` points close to the root of the hard
> instance, which keeps the Gram matrix positive definite, gives the same for
> pure hypermetric inequalities, for odd clique inequalities (the
> Barahona–Mahjoub clique inequalities and their switchings) and, after a
> switching, for the Barahona–Mahjoub clique inequalities themselves. Gap-0
> separation is NP-complete but only at non-psd points, where psd separation
> already finds a cut. The complexity of separating general gap inequalities
> at psd points remains open.

This paragraph rests on this note's proofs. Review round 1 checked the core
proofs and found the strong-hardness gap that Lemma 5 closes. Review round 2
confirmed Lemma 5, Corollaries 3–6 and Corollary 8, and proved the clique
result itself (its item R2-M1, written up here as Corollary 9).
[Review round 3](reviews/review-r3.md) verified Lemma 6 and Corollaries 9 and
10, with independent exact checks in `reviews/r3-work/`. Its minor fixes
are applied in this revision; it has not been independently re-reviewed, but its
fixes were checked by the coordinating agent.

**Corrections to the split note**
(`research-20260928b/side-results/split-separation-np-complete.md`).

1. Summary ("Novelty caveat"), §6 ("The binary analogue is open") and §8
   (last "Limits" bullet): the statement was a correct report of the sources
   cited, but it is now superseded. Hypermetric, gap-1 and rounded psd
   separation are strongly NP-complete (Corollary 4), also at binary points
   inside the psd and triangle relaxations (Corollaries 3, 6 and 8).
2. §6, "These are the rounded psd inequalities of Galli–Kaparis–Letchford":
   imprecise attribution. GKL list them with five earlier references
   (GKL 2012, §2: Avis 2003; Avis–Umemoto 2003; Deza–Laurent 1997;
   Giandomenico–Letchford 2006; Letchford–Sørensen 2012), and the name
   "rounded psd" is used in Letchford–Sørensen 2012, (10). In Boolean quadric
   form the binary split inequalities are the Boros–Hammer inequalities
   (Boros–Hammer 1993; GKL 2011, (6); Letchford–Sørensen 2012, (8)).
3. §6, "GKL also note that rounded psd separation reduces to hypermetric
   separation": correct, but the reduction is Letchford–Sørensen's (2012,
   Prop. 19). GKL state it as their Theorem 3.
4. §6 cites the GKL 2011 preprint. The published version (Oper. Res. Lett. 40
   (2012), §4, p. 151) contains the same sentence. For a paper's
   bibliography, note that GKL 2012 cite Laurent–Poljak's "Gap inequalities
   for the cut polytope" as SIAM J. Matrix Anal. 17 (1996) 530–547. Crossref
   gives Eur. J. Combin. 17 (1996) 233–254 (DOI 10.1006/eujc.1996.0020) for
   that title. Crossref assigns SIAM J. Matrix Anal. Appl. 17 (1996) 530–547
   to Laurent–Poljak's "On the facial structure of the set of correlation
   matrices" (DOI 10.1137/0617031).
5. §6, "This note therefore does **not** settle the binary (max-cut) case":
   true for that construction. The Delaunay obstruction it describes is not
   intrinsic. Exact cover meets it (Lemma 1).
6. §6 and §7, "The post-2012 hypermetric literature was not searched": now
   searched (§7). No resolution was found before this note. The latest
   statement of openness found is Letchford (2022).

The same supersession applies to
[split-separation-review.md](../../research-20260928b/reviews/split-separation-review.md),
§8.3 ("The binary analogue, which is still open"). The quotations checked in
[split-final-review.md](../../research-20260928b/reviews/split-final-review.md)
(table row "§6 binary analogue") remain correct as quotations.

## 9. Relevance for solvers

- **Exact separation is out of reach.** Unless P = NP, no polynomial-time
  algorithm separates exactly over hypermetric, gap-1, rounded psd,
  Boros–Hammer, Padberg clique or cut inequalities, the family (12), odd
  clique inequalities, or Barahona–Mahjoub clique inequalities (18). For all
  of these, this holds even at points that strictly satisfy the SDP relaxation
  (positive definite), satisfy all triangle inequalities, and in cut form
  satisfy all rounded psd inequalities up to any fixed gonality
  (Corollaries 4 and 8–10).
- **Bounded families are what can be separated exactly.** BiqMac adds
  triangle inequalities only (as described in MADAM, p. 3). BiqBin
  (arXiv:2009.06240v2, §3, pp. 7–8) and MADAM (arXiv:2010.07839v2, §2, p. 5)
  enumerate the `4·C(n,3)` triangle inequalities, but separate pentagonal and
  heptagonal inequalities (`b ∈ {0,±1}` with 5 or 7 nonzeros) heuristically,
  by simulated annealing on a quadratic assignment formulation. They do so
  although these families have polynomial size, because enumerating them is
  too slow. GKL use heuristics for gap inequalities, and Dey et al. (2026)
  solve Boros–Hammer separation as a bounded integer QP with Gurobi.
  Bounding the gonality or the support makes the problem polynomial
  (Lemma 3). This fits those choices. It says nothing about which heuristic
  performs well.
- **The violations at the hard points are small.** With `ε = 1/(8n + 2p + 1)`
  the maximum violation at the points of Corollary 3 is exactly
  `1/(16n + 4p + 2)` in the Boros–Hammer scale (13), and `1/(32n + 8p + 4)`
  in the scale of (10)–(12) (Corollaries 8 and 9). When an exact cover exists,
  the maximum violation in the cut scale at the points of Corollary 10 is
  `(q + 2)/(4qN)` for (18) at the switched point `d″`,
  `(q + 3)/(4qN)` for odd clique and pure hypermetric inequalities at
  `εd̃`, and `1/(2N)` for hypermetric inequalities at `εd̃`, where
  `N = 8n + 2p + 1`. The odd clique and pure hypermetric maximum is attained
  by the `m` vectors `(−1, 𝟙_C, −1, −𝟙_m + e_j)` for each cover `C`
  (and their negatives for odd clique). The hypermetric maximum is attained
  exactly when `w ∈ {0, 1}^m` in Corollary 10(a), since each term
  `w_j(w_j − 1)` is nonnegative and vanishes exactly for `w_j ∈ {0, 1}`.
  The rounded psd maximum at `εd̃` is also `1/(2N)` by Corollary 10(b).
  All these maxima are of order `1/(n + p)`; exact checks are recorded in
  §10, item 10. A fixed violation tolerance may hide them. This is a property
  of the construction, not a proved lower limit. The argument allows any `ε` with
  `εs < 3/4` (Corollary 3(c) and (d)), which gives violations up to about
  `3/(8s)`. For some families `s` stays bounded as `n` grows (proved for one
  family by the closed form after Lemma 5), so there the violation could be
  made larger. The original draft
  claimed a violation of `Θ(1/(n + p))` for `ε = 1/(2s)`. That was not
  proved, and it fails when `s` stays bounded. The proved bounds for that
  scaling are `1/(16n + 4p + 1) ≤ 1/(4s) ≤ 1/28`.
- **Gap-0 hardness has no practical consequence**, because psd separation
  dominates it.
- **General MINLP solvers.** Nothing was measured. In particular I did not
  check whether SCIP 10.0 separates any of these classes, so no claim is made
  about SCIP.

## 10. Checks actually run

Targeted checks only; no project-wide verification, CI not inspected. All
commands were run from `research-20261001/binary-separation/`, with at most
two processes at a time and each under a `timeout` wall-clock limit in the
revision. `OMP_NUM_THREADS=1` was set for the round-3 revision check, and
SCIP ran single-threaded. The raw outputs of the revision runs
(2026-10-02 and 2026-10-03) are in `logs/`. The round-0 outputs (2026-10-01)
and version of the main script are kept in `logs/r0/`, and the round-1 outputs
and script version in `logs/r1/`. The reviewers' reruns and independent checks
are in `reviews/r1-work/`, `reviews/r2-work/` and `reviews/r3-work/` and are
not repeated here. [Review round 3](reviews/review-r3.md) verified Lemma 6
and Corollaries 9 and 10; its independent exact code and log are
[`r3_checks.py`](reviews/r3-work/r3_checks.py) and
[`r3_checks.log`](reviews/r3-work/r3_checks.log). Its minor fixes are applied
in this revision; it has not been independently re-reviewed, but its fixes were
checked by the coordinating agent.

1. `timeout 900 python3 code/check_binary_separation.py` →
   `logs/check_binary_separation.log`, `ALL CHECKS PASSED`, 21 s (revision r2
   run, 2026-10-02). Standard library only, exact `Fraction` arithmetic.
   Violator sets are complete: Fincke–Pohst enumeration over an exact `LDLᵀ`
   of the ellipsoid `g_M(z) < 0`, or of `uᵀXu < 1` with `u₀` odd and the other
   `uᵢ` even. The checks of each revision run after those of the previous
   rounds, so earlier random instances are unchanged. A diff against
   `logs/r0/check_binary_separation.log` shows that revision r1 changed only
   the binary-point line, the example's `ε` and the timing, plus new lines. A
   diff against `logs/r1/check_binary_separation.log` (the r1 run, kept with
   the r1 version of the script in `logs/r1/`) shows that revision r2 changed
   nothing except the timing and added the seven lines of the rows marked
   "r2" below. Rows marked "r1" were added in revision r1.

   | Check | Instances | Result |
   |---|---|---|
   | Lemma 1 closed form | 300 random (instance, `η²`, `x ∈ [−3,3]ⁿ`, `k ∈ [−4,4]`) | 0 mismatches |
   | Theorem 1, exact cover, `p = 2..6`, `η² = (p−1)/4` | 200 (153 with a cover), `n ≤ 7` | violators = exact covers, value `−1/2`: 0 failures |
   | Theorem 1, `p = 4..6`, `η² = (p−2)/4` | 200 (130 with a cover) | value `−1`: 0 failures |
   | Theorem 1, X3C `q = 2` / `q = 3` / `q = 3` with `η² = (p−2)/4` | 200 (115) / 120 (68) / 120 (51) | 0 failures |
   | Cut form: `Q(b,d) = −g_M(z)` (20 random `b` each); `4d` integral; triangle inequalities hold iff no cover uses ≤ 2 sets | 200 | 0 failures |
   | Binary point `X(ε)`, `ε = 1/(8n+2p+1)` (revised): `εs < 1/2`, `4N·X` integral, PD, `Xᵢᵢ = X₀ᵢ`, `X − e₀e₀ᵀ/4` PD, all violated splits (every odd `u₀`) = the hypermetric ones from covers, value `−1/(2N)`, cut image `= εd ∈ [0,1]`, `J − 2εD` PD (elliptope), perimeter holds, triangle holds iff no small cover | 80 (59 with a cover; 53 with a cover of ≤ 2 sets, where triangle inequalities fail) | 0 failures |
   | Gonality and support of violators (X3C) | 95 violators, `q ∈ {2,3}` | gonality `2q−1`: 0 failures |
   | Pure violators with `q − 2` copies of `0` | 31 (X3C, `q ∈ {3,4}`) | `b ∈ {0,±1}`, `Q = 1/2`, triangle holds: 0 failures |
   | Control `η² = p/4` | 60 instances with a cover | no violators in all 60 (expected) |
   | Control `η² = p/16`, doubled instances | 40 | a violator with `k ≤ −2` in all 40 (expected) |
   | *r1:* Lemma 5: `Bᵀc* = δ/2`, `max Mᵢᵢ ≤ s ≤ 4n + p + 1/(4(p−1)) = 4‖c*‖²`, `εs < 1/2` | 81: 36 X3C with `q ≤ 10`, `n ≤ 31`; 40 random exact cover, `p ≤ 8`; 5 structured families (`n` copies of `{0,1,2}` plus `{3,4,5}` for `n = 5, 20, 40`; all triples of `[6]` and of `[9]`) | 0 failures. Example of the round-0 size problem: at `q = 10`, `n = 22`, `ε = 1/(2s)` has 19/21 digits (numerator/denominator), while the new `ε` is `1/237` |
   | *r1:* window endpoint `η² = p/12`, `p ∈ {2,3}` | 100 (96 with a cover) | Theorem 1 holds: 0 failures |
   | *r1:* control `η² = p/12 − 1/100` | 40 with a cover; the no-instance `{0,1}, {1,2}` | extra violators `(x, −2)` in 40 of 40; `(1,1,−2)` violates in the no-instance (expected) |
   | *r1:* Corollary 8: all violated (12) at `X(1/N)`, by complete enumeration over all ordered disjoint `(S, T)` and all integers `s`; all violated (11) directly | 60 (37 with a cover; X3C `q = 2, 3, 4` and random exact cover) | violated (12) = `{(cover, {g}, 0), ({g}, cover, −1)}` with violation `1/(4N)`; violated (11) = `{(cover, {g})}`: 0 failures |
   | *r1:* facets, by exact affine rank of the tight 0/1 points | (12) with `(|S|,|T|,s) = (q,1,0)` in `BQP_{q+1}`, `q = 2..6`, and in `BQP_{q+3}`, `q = 2..4`; (11) with `(|S|,|T|) ∈ {(2,1),(3,1),(2,2),(1,2),(1,3)}` | facets in all (12) cases; (11) is a facet for `(2,1)`, `(3,1)` and `(2,2)`, and not for `(1,2)` and `(1,3)` (as expected) |
   | *r2:* Lemma 6: slack of `(v, s)` at the switched point = slack of `(v′, s − v_g)` at the point; switched moment matrix `= AXAᵀ` | 300 random rational points (up to 6 variables, not necessarily psd), `v ∈ [−3,3]^k`, `s ∈ [−4,4]` | 0 failures |
   | *r2:* Corollary 9 at `P′ = ψ_g(X(1/N))`: `P′ = AXAᵀ`, PD, `X′ᵢᵢ = X′₀ᵢ`, in `[0,1]`, `4N·P′` integral; **all** violated Boros–Hammer inequalities (complete split enumeration, every integer `(v, s)`); all violated (12) (all disjoint `S, T`, all integers `s`); all violated (10) (all `S`, `s = 0..|S|−1`); triangle family; cut image `= εd` switched on `g`, elliptope interior | 60 (33 with a cover, 19 with a cover of ≤ 2 sets; X3C `q = 2, 3, 4` and random exact cover) | violated Boros–Hammer data = `{(𝟙_C + e_g, 1), (−𝟙_C − e_g, −2)}` with slack `−1/(2N)`; violated (12) = `{(C ∪ g, ∅, 1), (∅, C ∪ g, −2)}`, violation `1/(4N)`; violated (10) = `{(C ∪ g, 1)}`; triangle family holds iff no cover uses ≤ 2 sets: 0 failures |
   | *r2:* facets of the violated (10), by exact affine rank | `(|S|, s) = (q+1, 1)` in `BQP_{q+1}`, `q = 2..6`, and in `BQP_{q+3}`, `q = 2..4` | facets in all 8 cases |
   | *r2:* Corollary 10 (lifted copies, `τ² = 1/(8q)`, `ε = 1/N`): `M̃` PD; **all** hypermetric violators of `d̃` = `(1_C, −1, w)` with `Σw(w−1) < 4q`, gonality `≥ 2q − 1`; `X̃(ε)` and `X̃ − e₀e₀ᵀ/4` PD, `8qN·X̃` integral, `εs̃ = ε(s + mτ²) < 3/4`; all violated rounded psd inequalities of `εd̃` (complete split enumeration) have `σ = ±1`; violated odd clique inequalities nonempty iff a cover exists, `b*` violated by `(q+2)/(4qN)`; brute force over all `b ∈ {0,±1}^Ṽ` agrees; `εd̃` in `(0,1)`, metric polytope, elliptope interior; after switching on `{g, o_j}`: all violated (18) (all odd `S`) = `{C ∪ U}` with violation `(q+2)/(4qN)`, switched point in `(0,1)`, metric polytope, elliptope interior | 60 X3C (`q = 3`: 30, `q = 4`: 20, `q = 5`: 10; 34 with a cover); brute force on the 47 instances with `|Ṽ| ≤ 9`; `|S| ∈ {5, 7, 9}` occurred | 0 failures |
   | *r2:* control for Corollary 10 with `τ² = 1/4` | 10 X3C instances with a planted cover, `q ∈ {4, 5}` | hypermetric violators exist, but no odd clique inequality is violated in 10 of 10 (expected) |
   | *r2:* facets of (18), by exact affine rank of the tight cuts | `|S| = 3` in `CUT_3`, `CUT_4`; `|S| = 5` in `CUT_5..CUT_7`; `|S| = 7` in `CUT_7`, `CUT_8`; `|S| = 9` in `CUT_9` | facets in all 8 cases |
   | *r2:* cut image of a clique inequality (remark after Corollary 9): slack of (13) with `v = 𝟙_S` = slack of the rounded psd inequality `b = −(2s + 1 − |S|, 𝟙_S)` of the cut image | 300 random rational points (not necessarily psd), random `S`, `s ∈ [−2, |S| + 1]` | 0 failures |

   The round-0 run (2026-10-01, `logs/r0/check_binary_separation.log`, 22 s)
   used `ε = 1/(2s)` and passed the same table without the new rows. An
   earlier round-0 run reported failures in two checks. Both came from wrong
   expectations in the script, not from the construction:
   - it expected triangle inequalities to hold always, but they fail exactly
     when a cover uses at most 2 sets, as Corollary 3(b) now states;
   - it used `ε = 8/(9s)`, for which `X − e₀e₀ᵀ/9` is singular, so a
     positive-definiteness test failed.

   During the revision, the first version of the facet check used the wrong
   rank criterion (`dim + 1` instead of `dim`) and reported "not a facet" for
   every case, including the triangle inequality. After the criterion was
   corrected, the results matched the analytic expectations. The log shows
   only the corrected run.
2. `timeout 300 python3 code/scip_crosscheck.py` → `logs/scip_crosscheck.log`,
   4.4 s (revision r2 rerun; output identical to the round-0 and round-1 logs
   apart from timing; the r1 log is kept in `logs/r1/`). PySCIPOpt 6.2.1 / SCIP 10.0 (Python 3.13.11, NumPy 2.5.1),
   floating point, independent of the exact code. It minimizes
   `zᵀ(4M)z − diag(4M)ᵀz` over integers in a box that provably contains all
   violators, for 24 X3C instances (`q ∈ {3,4}`). The optimum was `−2` exactly
   when a cover exists and 0 otherwise: 0 disagreements. This is an exact
   integer optimization check. It does not involve SCIP's cutting planes, so
   whether SCIP generates any cuts is irrelevant here. The script does not use
   `ε`; it was rerun only to confirm that it still runs against the revised
   module, to which revision r2 only appended functions.
3. `python3 code/check_gap0.py` → `logs/check_gap0.log`, `ALL CHECKS PASSED`,
   34 s (round 0 only; not rerun in either revision, because Theorem 4 and
   the script are unchanged and the script does not import the revised module;
   the reviewers' reruns in rounds 1 and 2 were identical apart from
   timing). Theorem 4 on 40
   instances (`n ∈ {6, 8}`, 31 yes-instances):
   - `Zᵢᵢ = 1`, `Za = −νa`, `θ ≥ θ_lb > 0`, and `Z` is not psd;
   - for every `s ∈ {±1}ⁿ`, `Z|_{s⊥}` is not psd ⇔ `sᵀa = 0` ⇔ `s` is a balanced
     partition;
   - `x ∈ [0,1]` with all triangle inequalities.

   All tests were exact (psd by exact elimination). A one-directional
   sanity check of Lemma 4 on 200 random `Z` (`n = 3, 4`) found 0 box
   witnesses without an `s`-certificate.
4. `timeout 600 python3 code/probe_gap.py 3`,
   `timeout 900 python3 code/probe_gap.py 3 5 5 30` and
   `timeout 900 python3 code/probe_gap.py 2 6 6 20` → `logs/probe_gap_B3.log`,
   `logs/probe_gap_B3_n5.log`, `logs/probe_gap_B2_n6.log` (revision r1 reruns
   at the new `ε`; rerun again in revision r2, run two at a time, 1.4 s, 20 s
   and 11 s, with output identical to the r1 logs in `logs/r1/` apart from
   timing). These are exact integer box searches.
   - 27 no-instances with 4–6 points (box `[−3,3]`): 0 violated gap
     inequalities.
   - 12 with 7 points (box `[−3,3]`): 0.
   - 9 with 8 points (box `[−2,2]`): 0.

   The instances and counts are the same as in round 0 (`logs/r0/`). For at
   most 6 points the outcome carries no information. By Corollary 3(d), at a
   no-instance `εd` satisfies all gap-1 inequalities, and these include all
   switchings of hypermetric inequalities. For `|V| ≤ 6` the cut cone equals
   the hypermetric cone (Deza–Dutour Sikirić 2015, p. 1: "CUT_n = HYP_n only
   for 3 ≤ n ≤ 6"). Every facet of the cut polytope is a switching of a facet
   of the cut cone (Letchford 2022, p. 16). So `εd` lies in the cut polytope
   and satisfies every gap inequality. (Review round 1, optional item o2,
   suggested that only `|V| ≤ 5` is implied, using Letchford–Sørensen's
   Prop. 19. That proposition gives a sufficient condition; the switching
   argument covers `|V| = 6` as well. The sentence was therefore kept, with
   this explanation added.)
5. `timeout 600 python3 code/probe_cutcone.py` → `logs/probe_cutcone.log`,
   1.2 s (revision r1 rerun at the new `ε`; rerun in revision r2 with output
   identical to the r1 log apart from timing). Floating-point HiGHS LP through SciPy
   1.18.0. In all 24 no-instances with 7–10 points, `d` lies in the cut cone
   and `εd` in the cut polytope (minimum `ε·Σλ` between 0.34 and 0.46; 0.52 to
   0.56 at the round-0 `ε`). The instances and memberships are the same as in
   round 0. See §6 for why this cannot hold in general unless NP = co-NP.
6. Literature, round 0: the downloads and `pdftotext` extractions listed in
   [sources/MANIFEST.md](sources/MANIFEST.md); greps of those texts for the
   quoted sentences; `pdftotext -f 3 -l 3` on the GKL 2012 PDF to confirm the
   page (p. 151) of the "unknown" sentence; and the page markers of
   Letchford–Sørensen 2012 (pp. 261, 267–270), Deza–Grishukhin–Laurent 1993
   (p. 51) and Laurent–Poljak LIENS-93-27 (printed p. 14); Crossref API queries
   for the bibliographic data of Deza–Laurent Ch. 28, Avis 2003 and the two
   Laurent–Poljak 1996 papers.
7. Literature, revision: `curl` downloads of Letchford 2022, BiqBin, MADAM
   and Dey et al. 2026 into `sources/`. Their sha256 values equal the
   reviewer's. `pdftotext -layout` and page-numbered greps located every
   quotation and locator used above: Letchford 2022, pp. 8–9, 11, 16 and
   18–20; BiqBin pp. 7–8; MADAM pp. 3 and 5; Dey et al. pp. 4–5 and 16;
   Deza–Dutour Sikirić 2015, p. 1; Letchford–Sørensen 2012, Prop. 19, p. 269.
   Two WebSearch queries (separation complexity of Padberg's cut and clique
   inequalities and of the Boros–Hammer inequalities) and one WebFetch (the
   abstract page of de Vries–Perscheid 2022) found no hardness result for
   these classes.
8. Revision r2, additional commands:
   - `timeout 300 python3 code/closed_form_s.py` → `logs/closed_form_s.log`
     (SymPy 1.14.0, Python 3.13.11, and the exact module). It solves the symmetric 3×3 system
     symbolically and prints
     `s(n) = 77(193n + 108)/(4(141n + 272))`, limit `14861/564 = 26.349…`,
     and agreement with the exact `Fraction` values for
     `n = 1, 2, 5, 20, 40, 100` (all `True`). For `n` singletons with
     `p = n`, the ratio of `s` to the Lemma 5 bound is 0.99786, 0.99957,
     0.99982 and 0.99994 for `n = 4, 8, 12, 20`.
   - Page-numbered `awk` greps of `sources/arxiv-2604.00932.txt` (the Dey et
     al. quotation is on p. 4) and of `sources/letchford2022-qubo-chapter.txt`
     (Theorem 1, the covariance map, p. 11; (18), p. 11; switching, pp. 6–7
     and 9; (10)–(12), pp. 8–9; §7.2, pp. 18–19).
   - Two WebSearch queries: `Barahona Mahjoub clique inequalities cut
     polytope separation problem complexity NP-hard` and `"odd clique"
     inequalities max-cut separation NP-hard OR "NP-complete" hypermetric
     2024 OR 2025 OR 2026`. The result titles and snippets showed no
     hardness result for these classes (§7); no full text was opened.
9. Processes: every job of both revisions ran in the foreground or as a waited
   subshell, under `timeout`, at most two at a time, and finished before the
   note was finalized. In revision r1 a final `pgrep -af "python3 code/"`
   showed only jobs of the `split-practice` stream. In revision r2 the final
   scan (`pgrep -x python3` with `readlink /proc/PID/cwd`, and
   `pgrep -af` for this stream's script names) found no process whose working
   directory is this stream's directory and no running job of this stream's
   scripts. Jobs of other streams (for example `exp_splitloop.py`,
   `exp_hard.py`, `exp_separate.py`) were running and were not touched. No job
   of this stream was left running.
10. Revision after round 3 (2026-10-03):
    `OMP_NUM_THREADS=1 timeout 120 python3 -B -u code/check_r3_violation_maxima.py`
    → [`logs/check_r3_violation_maxima.log`](logs/check_r3_violation_maxima.log),
    `ALL R3 VIOLATION CHECKS PASSED`, exit 0. The script builds cut distances
    directly and uses exact integer and `Fraction` arithmetic. Complete
    hypermetric ellipsoid enumeration, brute force over all `{0, ±1}` odd
    clique vectors and all subsets at `d″` confirm the three maxima in §9
    on 7 X3C instances (`q = 3, 4, 5`; 4 yes, including one with two covers,
    and 3 no). It also confirms the maximizing vectors, the value for `b*`,
    and strict satisfaction of every nonempty even-set clique inequality
    at `d″`. This foreground check finished; no background process was used.

## Limits

- The proofs are mine, except where credited. Review round 1 checked the
  round-0 proofs and found them correct apart from the strong-hardness gap.
  Review round 2 confirmed the repair (Lemma 5, Corollaries 3–6) and
  Corollary 8. [Review round 3](reviews/review-r3.md) verified Lemma 6,
  Corollary 9 (whose argument is the round-2 reviewer's) and Corollary 10,
  with independent exact checks in `reviews/r3-work/`. Its minor fixes are
  applied in this revision; it has not been independently re-reviewed, but its
  fixes were checked by the coordinating agent.
  Nothing has been refereed or formalized.
- The finite checks confirm the constructions on small instances. Complete
  violator enumerations use at most 8 sets and `p ≤ 15`; the bound of Lemma 5
  was checked up to `n = 84` and `p = 30`; facetness was checked in `BQP_N`
  for `N ≤ 7` and in `CUT_n` for `n ≤ 9`. The checks do not replace the
  proofs.
- Gap-0 hardness is from PARTITION, so it is only weak NP-hardness.
- General gap separation at psd points is not settled.
- All hard points are positive definite but close to the boundary of the psd
  cone in absolute terms. For a unit vector `w` with `wᵀMw = λ_min(M)`, the
  vector `(0, w)` gives `λ_min(X(1/N)) ≤ λ_min(M)/N ≤ 7/N` for X3C, and the
  lifted copies give `λ_min(X̃(1/N)) ≤ τ²/N = 1/(8qN)`. Nothing is claimed for
  points whose smallest eigenvalue is bounded below by a constant.
- At the hard points the violation is polynomially small (for example
  exactly `1/(16n + 4p + 2)` in the Boros–Hammer scale at the points of
  Corollary 3). Whether hardness persists for violations bounded below by a
  constant is not known.
- The facet claims in Corollaries 8–10 rest on Padberg's clique facet
  theorem (Padberg 1989, cited through Letchford 2022, p. 8, not re-read),
  switching and the covariance map, and on exact checks for small sizes.
- The novelty search is limited (§7). The Deza–Laurent chapter, Dash's
  thesis and several older papers were not read.
- Nothing was measured on solvers.

## Open questions

1. Is separation of general gap inequalities NP-hard at psd points? Is it in
   NP? GKL give only a doubly exponential algorithm.
2. Is gap-0 separation strongly NP-hard?
3. Is it NP-hard to approximate the normalized maximum violation, for example
   within a constant additive gap at elliptope points? The split note's
   Corollary 3 gives an additive gap of order `1/N` for general splits. Here
   the violation is `Θ(1/(n + p))` for the chosen scaling, but the largest
   admissible scaling gives violations up to about `3/(8s)`, and `s` can stay
   bounded (closed form after Lemma 5). So the construction alone does not
   decide this.
4. Do the hardness results persist at points whose Boolean quadric moment
   matrix has smallest eigenvalue bounded below by a positive constant? All
   hard points here have smallest eigenvalue `O(1/N)` (Limits).
5. Can the hard points be made to satisfy all gap inequalities with `γ ≥ 3`?
   That would settle question 1. They cannot all lie in the cut polytope
   unless NP = co-NP (§6).

The round-1 open questions 3 (odd clique separation at points with positive
definite Gram matrix) and 4 (Padberg's clique inequalities (10) and the
Barahona–Mahjoub clique inequalities (18)) are answered by Corollaries 10
and 9 (see "Revision after review round 2").

## Revision after review round 1 (2026-10-02)

Review: [reviews/review-r1.md](reviews/review-r1.md) (verdict: major problems,
one major and four minor issues, four optional items). An earlier fix attempt
on 2026-10-02 was interrupted by a usage limit after only reading files; it
changed nothing on disk, so this revision started from the round-0 state. The
round-0 logs and the round-0 version of `code/check_binary_separation.py` are
kept in `logs/r0/`.

| Item | Issue | How it was handled |
|---|---|---|
| M1 (major) | Strong NP-hardness at the scaled points was not established: `ε = 1/(2δᵀM⁻¹δ)` has numerators and denominators of exponential size, so the claims for gap-1, rounded psd/Boros–Hammer, k-gonal, odd clique and binary SPLIT-SEP rested on an unproved size bound. | **Fixed.** The scaling is now `ε = 1/N`, `N = 8n + 2p + 1`. New Lemma 5 proves `s ≤ 4n + p + 1/(4(p−1)) < N/2` (the reviewer's argument, written out) and `s ≥ maxᵢ Mᵢᵢ`. Corollary 3(c) now states that `4N·X(ε)` is integral with entries at most `4N`. The proofs of Corollaries 4, 5, 6 and the new Corollary 8 cite this bound. The exact checks were rerun at the new `ε`, and a new check verifies Lemma 5 on 81 instances (§10, item 1). The probes were rerun at the new `ε` with unchanged outcomes (§10, items 4–5). Theorem 1, Corollary 2 and plain NP-completeness were not affected. |
| m1 | The claimed violation `Θ(1/(n + p))` was unproved and fails when `s` stays bounded. | **Fixed (claim withdrawn and replaced).** With the new `ε` the violation is exactly `1/(16n + 4p + 2)` (proved, Corollary 3(d)). For the old scaling the proved bounds are `1/(16n + 4p + 1) ≤ 1/(4s) ≤ 1/28`. Summary, §9, Limits and open question 5 were corrected. They now say that small violations are a property of the construction, not a proved necessity. |
| m2 | The proof of `εd ∈ [0,1]` in Corollary 3(e) used triangle inequalities, which hold only when no cover uses ≤ 2 sets. | **Fixed.** New proof: `J − 2εD = LX(ε)Lᵀ` with an explicit invertible `L`, so `J − 2εD ≻ 0`, and unit diagonal gives `0 < εd < 1` for every `q ≥ 2`. The elliptope statement no longer needs `q ≥ 3`. The exact check confirms the box at 53 instances that have a cover of at most two sets (§10, item 1). |
| m3 | Letchford's 2022 survey chapter, the latest statement of openness, was missing; the note also did not state that its own Theorem 1 settles Padberg's cut inequalities (11) and the family (12) without repeated points. | **Fixed.** Letchford (2022) was downloaded to `sources/` and its statements (pp. 18–20) were added to §2, §7, §8 and the Summary. New Corollary 8 (proved) states strong NP-completeness of separation for (11) and (12) at the positive definite points of Corollary 3. At these points the violated members of (12) are exactly the facet-defining cut inequalities with `S` a cover, `T = {g}`, `s = 0`. A complete enumeration check (60 instances) and an exact facet check were added. The repeated-points caveat is now limited to the cut-form odd clique family (remark after Corollary 5; open questions 3–4). Dey et al. (2026) are cited in §2, §7 and §9. While checking the source I found that Letchford's printed facet condition for (11) does not match the printed (11). This is recorded in the remarks after Corollary 8, with a proof and an exact check. |
| m4 | §9 said that BiqMac, BiqBin and MADAM separate pentagonal and heptagonal inequalities by enumeration. | **Fixed.** §9 and the Summary now say: BiqMac adds triangle inequalities only; BiqBin and MADAM enumerate triangle inequalities and separate pentagonal and heptagonal inequalities heuristically (simulated annealing), with page locators checked in the downloaded texts. |
| o1 (optional) | The lower window endpoint `p/8` can be relaxed to the sharp `p/12`. | **Adopted.** Theorem 1 now uses `max(p/12, (p−2)/4) ≤ η² < p/4`. The `k ≤ −2` case of the proof uses the integer minimum `−⌊(m+1)²/4⌋`. The note now proves that both endpoints are sharp, and a new exact check covers `η² = p/12` and `η² = p/12 − 1/100`. |
| o2 (optional) | §10 item 4: for at most 6 points only `|V| ≤ 5` would follow from known results. | **Not adopted, with reason.** For `|V| ≤ 6`, `CUT = HYP` (Deza–Dutour Sikirić 2015, p. 1). Every facet of the cut polytope is a switching of a facet of the cut cone (Letchford 2022, p. 16). Switchings of hypermetric inequalities are gap-1 inequalities, which `εd` satisfies at no-instances by Corollary 3(d). So the 6-point runs are uninformative as stated. The argument is now written out in §10, item 4 and referred to in §6. |
| o3 (optional) | Corollary 4 should state the input domain. | **Adopted.** Corollary 4 now takes arbitrary rational `d`, and its proof gives NP membership of gap-1 separation for every rational input (switching plus Lemma 2), beyond GKL's `[0,1]^E`. |
| o4 (optional) | `sources/MANIFEST.md` listed arXiv:1503.04554 under one author. | **Fixed.** Authors are M. Deza and M. Dutour Sikirić. |

**Corrections to the round-0 version of this note** (2026-10-01):

1. Strong NP-completeness of gap-1, rounded psd, Boros–Hammer, k-gonal, odd
   clique and binary SPLIT-SEP was claimed with the scaling `1/(2δᵀM⁻¹δ)`,
   for which it was not proved. It now holds with `1/(8n + 2p + 1)`
   (Lemma 5, Corollary 3).
2. "The violation is `Θ(1/(n + p))`" is withdrawn (see m1).
3. "`εd ∈ [0,1]`" and the elliptope statement now hold for all `q ≥ 2`, with
   a correct proof (see m2).
4. "The window is needed", with lower endpoint `p/8`, overstated the role of
   `p/8`; the sharp endpoint is `p/12` (see o1).
5. The description of BiqMac, BiqBin and MADAM was wrong (see m4).
6. "All hypermetric sources through 2012 state it as open" is replaced by "the
   sources from 1993 to 2022 state it as open".

**Checks rerun for this revision** (details in §10):
`code/check_binary_separation.py` (all checks, including the new ones),
`code/probe_gap.py` (three runs), `code/probe_cutcone.py` and
`code/scip_crosscheck.py`. `code/check_gap0.py` was not rerun, because it is
unaffected. Every revision run had a `timeout` limit, at most two ran at once,
and no background process was left running.

## Revision after review round 2 (2026-10-02)

Review: [reviews/review-r2.md](reviews/review-r2.md) (verdict: major problems,
one major issue, no minor issues, five optional items). The reviewer confirmed
all round-1 fixes and reproduced all logs. Before this revision, the round-1
version of `code/check_binary_separation.py` and the round-1 logs were copied
to `logs/r1/`.

| Item | Issue | How it was handled |
|---|---|---|
| R2-M1 (major) | The note said in six places that separation of Padberg's clique inequalities (10) is open, because the violators have mixed signs. Switching the hard point on `g` settles it. The same trick on Corollary 5's points settles (18) at points with repeated points. Calling (18) "the cut images" of (10) is inaccurate. | **Fixed, and extended.** New Lemma 6 (proved) states and proves the switching rule, including the shift of `s`. New Corollary 9 (proved) is the reviewer's result, written out: separation of (10) is strongly NP-complete at the switched points `ψ_g(X(1/N))`, which are positive definite, lie in `[0,1]`, satisfy all Boolean quadric triangle inequalities and have denominators dividing `4N`; the violated (10) are exactly `S′ = C ∪ {g}`, `s′ = 1`, and define facets. New Corollary 10 (proved) goes beyond the review: it replaces the exact copies of Corollary 5 by lifted copies (Gram block `τ²I`, `τ² = 1/(8q)`). This gives strong NP-completeness for odd clique, pure hypermetric and, after switching, Barahona–Mahjoub clique inequalities (18) at points in the interior of the elliptope and in the metric polytope, so the repeated points are not needed. This answers the round-1 open question 3 as well. The six places were rewritten: remarks after Corollary 8 (first bullet), §7 Letchford bullet, §8 discussion paragraph, Limits, Open questions (old 3 and 4 removed and answered), and the results list returned with this revision. The "cut images" sentence was corrected in the remark after Corollary 9. The Summary (item 3 and solver paragraph) and §9 now include the clique families. New exact checks (§10, item 1, rows "r2"): the switching identity (300 random points), Corollary 9 with complete enumeration of all violated Boros–Hammer, (12) and (10) inequalities (60 instances), facets of the violated (10), Corollary 10 with complete enumeration and a brute-force cross-check (60 instances), a control with `τ² = 1/4`, facets of (18), and the cut-image identity for clique inequalities used in the remark after Corollary 9. All passed. The reviewer's description of (18) as coming from (10) with `|S|` odd and `s = (|S| − 1)/2` is exact for sets `S` without the root; (18) on sets containing the root comes from (10) with `|S|` even and `s = |S|/2` (remark after Corollary 9). |
| o1 (optional) | The shift `s ↦ s − v_g` was attributed to Letchford (2022, p. 9), which states only the sign change. | **Adopted.** Lemma 6(ii) proves it; Corollary 8 now cites Lemma 6, and the text after Lemma 6 says what p. 9 contains. |
| o2 (optional) | "No complexity statement" for Dey et al. (2026) overstates the source. | **Adopted.** §2 table and §7 now say "no complexity statement about the full class" and quote p. 4 on Boros and Hammer's polynomial-time separation of subclasses. |
| o3 (optional) | "`s` stays bounded (Lemma 5 and §10)" was not proved; Lemma 5 gives only an upper bound. | **Adopted.** The remark after Lemma 5 now gives the closed form `s(n) = 77(193n + 108)/(4(141n + 272)) → 14861/564`, proved by an exact symbolic computation (`code/closed_form_s.py`), and states that the bound is nearly attained by singleton families. §9 and open question 3 refer to it. |
| o4 (optional) | The remark on Letchford's facet condition for (11) could add the chapter's own p. 8 remark and the commonly cited orientation of Padberg's cut inequalities. | **Adopted**, with the caveat that Padberg (1989) was not checked. |
| o5 (optional) | "odd clique inequalities in cut form, that is, pure hypermetric inequalities" conflates two families. | **Adopted.** Summary item 3 now lists odd clique, (18) and pure hypermetric inequalities separately. |

**Corrections to the round-1 version of this note** (2026-10-02, first
revision):

1. "Padberg's clique inequalities (10) remain open", with the reason that
   their vectors have only positive entries (remarks after Corollary 8, §7,
   §8, Limits, open question 4): wrong. Corollary 9 settles them.
2. "The same holds for their cut images, the Barahona–Mahjoub clique
   inequalities (18)": wrong twice. (18) comes only from the subfamilies of
   (10) with `2s + 1 − |S| ∈ {0, 1}` (remark after Corollary 9), and (18) is
   now settled by Corollary 10.
3. "The repeated points are needed for this family" (remark after
   Corollary 5): wrong. Corollary 10 uses distinct points with a positive
   definite Gram matrix.
4. Open question 3 said "with positive definite Gram matrix, that is, without
   repeated points". These are not equivalent: a positive definite Gram
   matrix excludes repeated points, but points without repeated points can
   have a singular Gram matrix (for `J − 2D`, for example, two points at
   distance 1). At the points of Corollary 10 both `M̃` and `J − 2εD̃` are
   positive definite.
5. Summary item 3: "odd clique inequalities in cut form, that is, pure
   hypermetric inequalities" conflated two families (o5).
6. Corollary 8 attributed the shift of `s` under switching to Letchford
   (2022, p. 9) (o1).
7. "`s` stays bounded (Lemma 5 and §10)" cited an upper bound for a
   boundedness claim (o3).

**Checks rerun for this revision** (details in §10):
`code/check_binary_separation.py` (all checks; the round-2 checks are
appended, and the earlier output is unchanged apart from timing),
`code/closed_form_s.py` (new), `code/probe_gap.py` (three runs),
`code/probe_cutcone.py` and `code/scip_crosscheck.py` (outputs identical to
round 1 apart from timing). `code/check_gap0.py` was not rerun, because it is
unaffected. Every run had a `timeout` limit, at most two ran at once, and no
background process was left running (§10, item 9).

## Revision after review round 3 (2026-10-03)

Review: [reviews/review-r3.md](reviews/review-r3.md) (verdict: minor fixes,
no major issues). The reviewer verified Lemma 6, Corollaries 9 and 10 and
their quantitative claims, except the maximum stated in §9. The reviewer's
independent exact code and log are in `reviews/r3-work/`. This revision
applies the fixes below and has not itself been re-reviewed.

| Item | Issue | How it was handled |
|---|---|---|
| R3-m1 | §9 gave `(q + 2)/(4qN)` as the maximum at all Corollary 10 points. | **Fixed.** §9 now distinguishes `(18)` at `d″`, with maximum `(q + 2)/(4qN)`, from odd clique and pure hypermetric inequalities at `εd̃`, with maximum `(q + 3)/(4qN)`, and hypermetric inequalities there, with maximum `1/(2N)` (also the rounded psd maximum). Corollary 10(c) and its proof list the `m` maximizing pure vectors per cover, `(−1, 𝟙_C, −1, −𝟙_m + e_j)`. `b*` still has its stated value. The Summary's "of order `1/(n + p)`" remains correct. Exact checks on 7 X3C instances are saved in `code/check_r3_violation_maxima.py` and `logs/check_r3_violation_maxima.log` (§10, item 10). |
| R3-m2 | The header, §8, Limits and §10 omitted round 3 or said the new material had not been re-reviewed. | **Fixed.** All four now record that round 3 verified Lemma 6 and Corollaries 9 and 10, that its minor fixes are applied here, and that this revision itself has not been re-reviewed. They cite the review and its independent checks. |
| R3-o1 | §8 said switching turns points into inequalities and described the root as replaced. | **Adopted.** Switching turns the violated cut inequalities into facet-defining clique inequalities; `q − 2` points are added close to the root, which remains. |
| R3-o2 | The Barahona–Mahjoub clique family can also include even-`|S|` sets. | **Adopted.** The remarks after Corollary 10 explain that these are psd inequalities and hold at `d″`, so the result holds under either definition. The exact check exhausts even subsets as well. |
| Commit status | The program's statement that nothing in the continuation is committed became false after repository sweeps outside the program. | **Corrected within this stream.** The header records that outside sweeps included program files in commits and that this program makes no commits. `PROGRAM.md` is outside this revision's edit scope and was left unchanged. No commits, staging or branch changes were made for this revision. |

**Check run for this revision:** the exact script in §10, item 10 passed
with `OMP_NUM_THREADS=1` and a `timeout`, in the foreground. Only targeted
checks were run; no project-wide verification or CI inspection was done.
Review files were read and left unchanged.
`OMP_NUM_THREADS=1 GIT_OPTIONAL_LOCKS=0 timeout 10 git diff --check -- .`
also passed from this stream's directory (exit 0).

## References

- D. Avis, On the complexity of testing hypermetric, negative type, k-gonal
  and gap inequalities, in: Discrete and Computational Geometry (JCDCG 2002),
  LNCS 2866 (2003) 51–59.
- D. Avis, V. P. Grishukhin, A bound on the k-gonality of facets of the
  hypermetric cone and related complexity problems, Comput. Geom. 2 (1993)
  241–254.
- F. Barahona, A. R. Mahjoub, On the cut polytope, Math. Program. 36 (1986)
  157–173 (not read; cited through Letchford 2022, [7]).
- E. Boros, P. L. Hammer, Cut-polytopes, Boolean quadric polytopes and
  nonnegative quadratic pseudo-Boolean functions, Math. Oper. Res. 18 (1993)
  245–253 (not read; cited through GKL 2011).
- A. Caprara, A. N. Letchford, On the separation of split cuts and related
  inequalities, Math. Program. 94 (2003) 279–294.
- W. Cook, S. Dash, On the matrix-cut rank of polyhedra, Math. Oper. Res. 26
  (2001) 19–30.
- M. Deza, V. P. Grishukhin, M. Laurent, Hypermetrics in geometry of numbers,
  LIENS-93-4 (1993).
- M. Deza, M. Dutour Sikirić, The hypermetric cone on 8 vertices and some
  generalizations, arXiv:1503.04554v1 (2015).
- S. S. Dey, N. Jiang, A. M. Kazachkov, A. Lodi, G. Muñoz, Chvátal–Gomory
  rounding of eigenvector inequalities for QCQPs, arXiv:2604.00932v1 (2026).
- N. Gusmeroli, T. Hrga, B. Lužar, J. Povh, M. Siebenhofer, A. Wiegele,
  BiqBin: a parallel branch-and-bound solver for binary quadratic problems
  with linear constraints, arXiv:2009.06240v2 (2021).
- T. Hrga, J. Povh, MADAM: a parallel exact solver for max-cut based on
  semidefinite programming and ADMM, arXiv:2010.07839v2 (2021).
- M. Deza, M. Laurent, Geometry of Cuts and Metrics, Springer (1997), Ch. 28,
  pp. 445–465 (abstract only).
- M. Laurent, S. Poljak, Gap inequalities for the cut polytope, European J.
  Combin. 17 (1996) 233–254 (not read; bibliographic data from Crossref).
- M. Laurent, S. Poljak, On a positive semidefinite relaxation of the cut
  polytope, LIENS-93-27 (1993); Linear Algebra Appl. 223/224 (1995) 439–461.
- L. Galli, K. Kaparis, A. N. Letchford, Gap inequalities for non-convex
  mixed-integer quadratic programs, Oper. Res. Lett. 39 (2011) 297–300.
- L. Galli, K. Kaparis, A. N. Letchford, Complexity results for the gap
  inequalities for the max-cut problem, Oper. Res. Lett. 40 (2012) 149–152.
- L. Galli, K. Kaparis, A. N. Letchford, Gap inequalities for the max-cut
  problem: a cutting-plane algorithm, ISCO 2012, LNCS 7422, 178–188.
- M. R. Garey, D. S. Johnson, Computers and Intractability (1979), [SP2]
  (not re-read here; cited as in the split note).
- R. Kannan, Minkowski's convex body theorem and integer programming, Math.
  Oper. Res. 12 (1987).
- R. Kannan, A. Bachem, Polynomial algorithms for computing the Smith and
  Hermite normal forms of an integer matrix, SIAM J. Comput. 8 (1979).
- R. M. Karp, Reducibility among combinatorial problems (1972).
- A. N. Letchford, The Boolean quadric polytope, in: A. P. Punnen (ed.), The
  Quadratic Unconstrained Binary Optimization Problem, Springer (2022)
  97–120 (accepted manuscript read; page numbers in this note are manuscript
  pages).
- A. N. Letchford, M. M. Sørensen, Binary positive semidefinite matrices and
  associated integer polytopes, Math. Program. 131 (2012) 253–271.
- A. N. Letchford, M. M. Sørensen, A new separation algorithm for the Boolean
  quadric and cut polytopes, Discrete Optim. 14 (2014) 61–71.
- M. W. Padberg, The Boolean quadric polytope: some characteristics, facets
  and relatives, Math. Program. 45 (1989) 139–172 (not read; cited through
  Letchford 2022, [53]).
- V. Vaikuntanathan, Lattices lecture notes, MIT 6.876, Fall 2015, Lectures 9
  and 10.
- Split note: `research-20260928b/side-results/split-separation-np-complete.md`.
