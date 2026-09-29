# Scout report: S-free sets and intersection cuts for nonconvex MINLP/QCQP

Area: `s-free-intersection-cuts`. Date: 2026-09-28.
Scratch files, scripts and outputs: `research-20260928b/scouting/s-free-intersection-cuts/`.

## Summary

Maximal quadratic-free sets are now fully characterized by non-expansive maps
`Γ` (Muñoz–Paat–Serrano, Math. Program. 2025, and arXiv:2605.30602, May 2026).
The implementation in SCIP still uses only one fixed member of this family per
cut. It uses a constant `Γ`, with the direction `λ` fixed by the LP point and
the eigenvalue coordinates. SCIP 10 still ships these cuts disabled. I found no
work on *which* maximal quadratic-free set to use, and no work on how well any
family approximates the best possible intersection cut.

First-pass results obtained here:

- **Exactness.** The best bound from a single intersection cut equals the
  corner bound `z_K(w) = inf{w^T λ : λ in K ∩ S}` (Lemma 1, standard). For
  constraints on `k` variables, `z_K` is attained on `≤ rank`-ray sub-cones
  (Lemma 2). It is computable with `O(N^{⌊k/2⌋})` closed-form subproblems
  (Prop. 3).
- **Hardness.** `z_K` is NP-hard to compute when `k` is part of the input
  (Prop. 4, a reduction from the standard quadratic program).
- **SCIP's set can be arbitrarily bad.** SCIP's set can be arbitrarily worse
  than another constant-`Γ` set (Prop. 5). Even the closure of *all*
  constant-`Γ` sets has approximation factor `→ 0` against the corner hull,
  already in `R^2` with two rays (Prop. 6). An oblique split, a non-constant
  `Γ` set, is optimal in that example.
- **The transformation choice is the `Γ` choice.** The oblique split is a
  Lorentz-boost image of SCIP's own set. For quadratic forms with one negative
  (or one positive) eigenvalue after homogenization, the images of the
  Muñoz–Serrano sets under the automorphism group of the form are *exactly* all
  maximal sets (Prop. 7, homogeneous case). This answers Muñoz–Serrano's open
  question on "the role of transformations" in that signature.
- **Numerics.** Optimizing over that orbit (7 parameters for bilinear `w = xy`)
  reached at least 97% of the exact corner bound in all 62 tested bilinear
  corners (3, 6 and 10 rays). Every instance re-run with more restarts reached
  the exact bound (within `10^-4`). SCIP's set got 74–91% on average, and as
  little as 8%.

Recommended direction: **optimal selection and approximation theory for
maximal quadratic-free sets** (OQ1). Score **6/10**. The math is tractable and
the question is stated-open. The solver payoff is real but moderate, because
cut density, SCIP's reason for disabling the cuts, is not addressed directly.

---

## 1. Frontier map

Notation. `S = {s in R^k : q(s) = s^T Q s + b^T s + c ≤ 0}`, with `q`
indefinite. An LP vertex `x̄` has simplicial cone `K = x̄ + R·R^N_+`. `q` reads
the `k` coordinates `x_Q`. `P := R_Q in R^{k×N}` holds the projected rays
`p_j`, and `s̄ = x̄_Q` with `q(s̄) > 0`. An S-free `C` with `s̄ in int C`
gives the cut `Σ_j λ_j/α_j ≥ 1`, where `α_j = sup{t : s̄ + t p_j in C}`.
The reduced costs are `w_j = c^T r_j ≥ 0`. After one cut, the LP bound over the
cone rises by `z_C(w) = min_{α_j<∞} w_j α_j`.

### 1.1 Characterization of maximal quadratic-free sets

| Result | Assumptions | Conclusion | Source (checked) |
|---|---|---|---|
| Muñoz–Serrano, "Maximal quadratic-free sets" | `S = {q ≤ 0}`, one quadratic; homogenize and diagonalize to `Q_h = {‖x‖ ≤ ‖y‖}` or `Q_g = Q_h ∩ {a^T x + d^T y = −1}` | First maximal sets: `C_λ = {‖y‖ ≤ λ^T x}` and `φ`-sets for `Q_g`. §6 shows the set obtained "heavily depends on the choice of T" and leaves that open. §7 lists open items: the role of transformations, a comparison with Bienstock et al., and new families. | arXiv:1911.12341 (full text: §6 Example 9, §7); Math. Program. 192 (2022) |
| Muñoz–Paat–Serrano, homogeneous case | `Q_h`, full-dimensional sets | Every maximal set is `C_Γ = {Γ(β)^T x ≥ β^T y ∀β ∈ D^m}` (Thm 1.1). It is maximal iff `Γ` is non-expansive and `0 ∉ conv{(Γ(β), −β)}` (Thm 1.2). Polyhedrality is characterized by isometric covers (Thm 1.3). General-S criterion via exposing sequences (Thm 1.4). Maximal polyhedra can have arbitrarily many facets (Ex. 2.4). §8: characterizing which point sets define maximal Q-free polyhedra is "an important follow-up question". | arXiv:2211.05185 (intro, Thms 1.1–1.4, Examples 2.1–2.4, §8); Math. Program. 210 (2025) 641–668 |
| Muñoz–Paat–Serrano, inhomogeneous case | `Q_g`, `max{‖a‖, ‖d‖} = 1` | Every maximal set is `C_Γ^G ∩ H`, with `G = {β : a^T Γ(β) + d^T β ≤ 0}` (Thm 2). If `‖a‖ ≤ ‖d‖`: maximal iff `a ≠ Γ(−d)` (Thm 4). If `‖d‖ < ‖a‖`: maximal iff `G = D^m` (Thm 5). This "completes a characterization of all maximal quadratic-free sets". The paper states that prior implementations used "only one family". There is no explicit open-problem section. | arXiv:2605.30602 v1 (full text read: §1–2, Thm statements, end matter) |
| Bienstock–Chen–Muñoz, outer-product-free (OPF) sets | `S` = symmetric rank-one PSD matrices (lifted polynomial optimization) | Full-dimensional maximal OPF sets are cones (Thm 4.3). The halfspace `⟨A, X⟩ ≥ 0` is maximal iff `A` is NSD (Thm 4.7). 2×2 PSD cones are maximal (Thm 4.10). Full classification only in `S^{2×2}` (Thm 4.15). Other families exist for `n ≥ 3` (Props 4.17–4.18, "open avenues"). Oracle ball cuts converge in Hausdorff distance for the *non-local* closure `P \ int B` (Thm 3.3/3.4); that separation is NP-hard. | local KB `bienstock2020-outer-product-free-sets-for` (fulltext §3, §4, §7) |

### 1.2 Implementation, strengthening and the solver state

- Chmiela–Muñoz–Serrano, "On the implementation and strengthening of
  intersection cuts for QCQPs". Checked in ZIB Report 20-29; published as
  Math. Program. 197 (2023) 549–586.
  - They give explicit maximal sets for Cases 1–4. Case 4 covers linear terms
    in zero-eigenvalue directions, as in `w = xy`.
  - The set always uses `λ = x̂(s̄)/‖x̂(s̄)‖` in eigenvalue coordinates.
    Remark 3 says other factorizations "can potentially lead to other maximal
    quadratic-free sets", but only the eigenvalue decomposition is used.
  - Cuts are closed-form, with Glover negative-edge strengthening.
  - On MINLPLib they close about 8% more gap on average (12% on affected
    instances). Strengthening is slightly negative because of density.
  - Final remarks call for "careful handling of the density … special cut
    selection rules".
- Chmiela–Muñoz–Serrano, "Monoidal strengthening and unique lifting in
  MIQCPs", Math. Program. B 210 (2025) 189–222.
  - Integer *nonbasic* variables are lifted by monoidal strengthening.
  - Unique lifting holds, so the integer coefficients are optimal.
  - Only the abstract and metadata were checked; the Springer full text was not
    accessible.
- SCIP 10.0, checked locally through PySCIPOpt parameters:
  - `nlhdlr/quadratic/useintersectioncuts = False` (off by default);
  - `usemonoidal = True`, `usestrengthening = False`,
    `useboundsasrays = False`, `sparsifycuts = False`;
  - no option to choose the set.

  The SCIP 8/9 rationale, "not clear yet how to decide when it will be
  beneficial", and in-house probe D are in
  `research-20260922/scouting/brainstorm2-solvercore.md`. Probe D: +7.6 pp mean
  root gap, total node ratio 0.974, per-instance swings of 10–600× both ways.
- Related constructions:
  - Serrano, factorable MINLP via concave underestimators (arXiv:1812.03073;
    listing only).
  - Fischetti–Monaci bilinear-free sets, EJOR 2020 (cited in MPS; not read).
    They are built from bound disjunctions and are not maximal.
  - Xu–D'Ambrosio–Liberti–Haddad-Vanier, signomial cutting planes, SIOPT 35
    (2025), arXiv:2212.02857 (listing only).
  - Xu–Liberti, submodular maximization through intersection cuts,
    arXiv:2302.14020 (listing only).
  - Xu–Pokutta, joint-range inequalities, arXiv:2608.03318. From the local KB
    summary: they compute the hull of a *two-quadratic* 2-D joint range
    intersected with a two-row simplicial cone, and a four-ray intersection cut
    that excludes the punctured `Δ = 0` cases.

### 1.3 General S-free and intersection-cut theory used here

- Balas (1971) introduced intersection cuts for the lattice; Tuy (1964) for
  reverse-convex sets (concavity cuts).
- Conforti–Cornuéjols–Daniilidis–Lemaréchal–Malick, MOR 2015: cut-generating
  functions and S-free sets. Cited in MPS; not re-read.
- Cornuéjols–Wolsey–Yıldız, "Sufficiency of cut-generating functions", Math.
  Program. 152 (2015). Search snippet only.
- Averkov–Basu–Paat, "Approximation of corner polyhedra with families of
  intersection cuts", SIOPT 2018, arXiv:1705.02015 (abstract). Lattice-free
  sets with `≤ i` facets approximate the `n`-row corner polyhedron within a
  constant factor iff `i > 2^{n−1}`. This is the direct MILP precedent for
  OQ1(b).
- Poirrier–Yu, depth of cutting planes, arXiv:1903.05304 (abstract). Depth of
  corner-polyhedron cuts in closed form.
- Cornuéjols–Patil, hereditary property of closures, arXiv:2609.02038 (local
  KB summary). Hereditary faces for `L`-closures `R_L(K) = ∩ conv(K \ int L)`.
- Concavity-cut convergence. Porembski, JOGO 2001 ("Finitely convergent
  cutting planes for concave minimization") states that "it has not been
  possible to either prove or disprove the finite convergence of a pure cutting
  plane algorithm for concave minimization based solely on these cutting
  planes". Zwart (Oper. Res. 1973) gave counterexamples for Tuy's conical
  algorithm. Porembski 2004 adds cone adaptation for forced depth. All three
  were seen as search snippets only.

### 1.4 What is not known (after this search)

- Which maximal quadratic-free set gives the best cut for a given vertex and
  cone. No selection rule and no complexity result.
- How well any restricted family approximates the best cut. No quadratic
  analog of Averkov–Basu–Paat.
- Maximal S-free sets for two or more quadratics, for `S ∩ box`, or for
  mixed-integer quadratic `S`. Only special cases exist: `S≤0` (quadratic plus
  one homogeneous linear inequality), 2×2 OPF, and the Xu–Pokutta 2-D range.
- Convergence of the practical loop "LP vertex → intersection cut → re-solve"
  for quadratic `S`. BCM's convergence theorem is for the non-local, NP-hard
  ball closure.

### 1.5 Sources examined

| Source | What was checked |
|---|---|
| arXiv:2605.30602 (PDF → `sources/2605.30602*.txt`) | Abstract, §1 theorems 1–5, §2.1 reduction, Lemmas 1–3, end matter and references |
| arXiv:2211.05185 (PDF → `sources/2211.05185*.txt`) | §1 contributions (Thms 1.1–1.4, Cor 1.1), §2 examples, §8 future work |
| arXiv:1911.12341 (PDF → `sources/1911*.txt`) | §3 set `C_λ`, §5 conjecture remarks, §6 transformation dependence (Example 9), §7 future work |
| ZIB Report 20-29 (Chmiela–Muñoz–Serrano; PDF → `sources/chmiela2020.txt`) | §1–3 constructions (Cases 1–4), §4 coefficient formulas, §5 computations, §6 final remarks |
| Math. Program. 210 (2025) 189–222 (monoidal) | Abstract and metadata only (web search, ZIB OPUS); full text inaccessible |
| KB `bienstock2020-outer-product-free-sets-for` | fulltext §2–5, §7 (theorem list, convergence Thms 3.3/3.4, OPF classification) |
| KB `xu2026-joint-range-inequalities-for-nonconvex` | paper.md summary |
| KB `cornuejols2026-a-hereditary-property-of-cutting` | paper.md summary |
| KB `andersen2013-…`, `modaresi2016-…`, `kazachkov2025-monoidal-…` | Titles and index entries only (not read) |
| In-house `research-20260922/scouting/scout_area1_cuts.md`, `scout_literature.md` (Q3), `brainstorm2-solvercore.md` (T2, probe D), `notes/candidate-directions-2026-09-05.md` (#12) | Prior in-house scouting of this area; not developed since |
| arXiv:1705.02015, 1903.05304, 1701.06692 | Abstracts via arXiv API |
| arXiv API searches | `abs:"S-free" AND cat:math.OC`, `abs:"intersection cuts" AND abs:quadratic`, `abs:"intersection cut" AND abs:nonconvex`, `abs:"monoidal strengthening"`, `ti:"free sets"`, `abs:"quadratic-free"`, `abs:"intersection cuts" AND abs:"corner"`, `abs:"concavity cuts"`, `abs:"intersection cut" AND abs:bilinear` |
| Web search | Chmiela et al. versions; maximal S-free 2025–26; S-free polynomial; closure/strength; two-quadratic S-free; sufficiency of CGFs; concavity-cut convergence (Porembski, Zwart) |
| SCIP 10.0 via PySCIPOpt | `nlhdlr/quadratic/*` parameters and defaults |

Search limits:

- The shared web-search budget (200 calls) ran out during this scouting. The
  later novelty checks used only the arXiv API and the local KB.
- Springer full texts were blocked.
- An unsuccessful search does not establish novelty.

---

## 2. Open questions

### OQ1 (recommended). Optimal selection among maximal quadratic-free sets, and approximation by restricted families

Precise statement. Fix `S = {q ≤ 0} ⊂ R^k`, `s̄ ∉ S`, rays
`P ∈ R^{k×N}`, and costs `w ∈ R^N_{>0}`.

- **(a) Orbit sufficiency.** Let `(n, m)` be the signature of the homogenized
  form. Let `O` be the family of sets `{s : ‖(L u)_y‖ ≤ λ^T (L u)_x}`, where
  `u = u(s, 1)` are Sylvester coordinates, `L ∈ O(n, m)` and `λ ∈ D^n`.
  This family is exactly "the Muñoz–Serrano set under every admissible
  transformation `T`". Is `sup_{C ∈ O} z_C(w) = z_K(w)` for all `P` and `w`?
  Equivalently, do the cuts from `O` describe the dominant of the corner hull
  `cl(conv(K ∩ S) + R^N_+)`? For which signatures?
- **(b) Approximation factor.** This is the quadratic analog of
  Averkov–Basu–Paat. For a family `F` of maximal quadratic-free sets in `R^k`,
  let `ρ_k(F) = inf z_F(w)/z_K(w)`, where `z_F` is the bound of the `F`-closure
  and the infimum runs over all quadratics, points, ray sets and `w ≥ 0`.
  Which natural finite-parameter families have `ρ_k(F) > 0`?
- **(c) Algorithms.** Find exact or approximate separation of the best cut
  under a practical criterion (bound, efficacy, sparsity) for small `k`, and
  test it in SCIP.

Evidence that it is open:

- Muñoz–Serrano 2022 §6–7 leave "the role of different transformations"
  explicitly open.
- MPS 2025 §8 leaves the polyhedral case open.
- MPS 2026 notes that implementations use "only one family".
- Chmiela et al. use one fixed `λ` and the eigenvalue decomposition.
- SCIP 10 has no selection option.
- The arXiv API searches above found no selection or approximation paper for
  quadratic S-free sets. The web-search budget ran out before a Google-Scholar
  citation sweep of MPS 2025/2026 was possible, and the MPS group calls this a
  "new avenue", so concurrent work is a real risk.

### OQ2. Maximal S-free sets for several quadratics or bounded quadratic sets

Characterize full-dimensional maximal S-free sets for any of:

- `S = {q1 ≤ 0, q2 ≤ 0}`;
- `S = {q ≤ 0} ∩ [l, u]`;
- `S = {(x, y, w) : w = xy, (x, y) ∈ box}`.

The goal is an analog of MPS's `Γ` description, for example as intersections of
`C_Γ`-type pieces.

Evidence open:

- Only `S≤0` (Muñoz–Serrano Remark / Chmiela §3.1), the 2×2 OPF case, and the
  Xu–Pokutta projected two-quadratic range exist.
- Fischetti–Monaci bilinear-free sets are not maximal.

Caveat: Lemmas 1–2 below make the *best cut* computable for small `k` without
any characterization. So OQ2's value is cheap closed-form cuts and structure.
In random McCormick LPs (E3), making the corner bound-aware changed the bound
by more than 0.1 of the gap in only 1 of 47 instances.

### OQ3. Convergence of pure intersection-cut loops

Let `P` be a polytope and `S = {q ≤ 0}`. Consider the loop "optimal LP vertex
→ one intersection cut from a maximal quadratic-free set (simplicial cone) →
re-solve". Does the LP value converge to `min{c^T x : x ∈ conv(P ∩ S)}`?

- (i) for SCIP's rule;
- (ii) for the bound-optimal rule;
- (iii) for every rule?

Evidence open:

- BCM prove convergence only for the non-local ball closure.
- For reverse-convex `S` (the unique maximal set, i.e. Tuy cuts), finite
  convergence of the pure cutting-plane method was neither proved nor
  disproved as of Porembski 2001. I found no later resolution; this search was
  weak.

In E4, 11 random instances in `R^2` and `R^3` all converged, in at most 39
rounds, with no stalling. A negative answer would need a Zwart-type flat-cone
construction.

### OQ4. Mixed-integer quadratic S-free sets

Characterize maximal S-free sets for `S = {s ∈ Z^p × R^{k−p} : q(s) ≤ 0}`,
where integrality is on the *basic* or structural variables that `q` reads.
Monoidal strengthening covers only integer *nonbasic* rays.

Lemma 2 still applies when the integrality is on the `q`-variables. So for
small `k`, the best cut is again a small-dimensional mixed-integer QCQP oracle.

---

## 3. First-pass mathematics on OQ1

### 3.1 Structural lemmas (proved; elementary)

**Lemma 1 (single-cut bound equals corner bound).** Assume `w > 0`. Then
`sup{z_C(w) : C S-free, s̄ ∈ int C} = z_K(w) := inf{w^T λ : λ ≥ 0, q(s̄ + Pλ) ≤ 0}`.
Maximal sets dominate, so the supremum may be taken over maximal quadratic-free
sets. It is attained only in the limit in some tangential cases.

*Proof.* `≤` is validity. For `≥`, let `z = z_K(w) < ∞` and `ε > 0`. The set
`T_ε = s̄ + P{λ ≥ 0 : w^T λ ≤ (1 − ε) z}` is compact and convex, and it misses
`S`. So some `δ`-neighbourhood `C_ε` is S-free and contains `s̄` in its
interior. Each ray satisfies `α_j ≥ (1 − ε) z / w_j`, hence
`z_{C_ε}(w) ≥ (1 − ε) z`. By Zorn's lemma `C_ε` lies in a maximal S-free set.
∎

The same argument gives the plain intersection-cut closure at `x̄`:
`cl(conv X + R^N_+)`, with `X := K ∩ S` in `λ`-space. This is the finite-ray,
closed-`S` form of Balas/CCDLM sufficiency and is likely folklore. The
zero-reduced-cost case needs recession handling.

**Lemma 2 (few-ray support).** Let `T ⊂ R^k` be closed and
`X = {λ ≥ 0 : s̄ + Pλ ∈ T}`. Then
`conv X = conv(∪_{|J| ≤ r} X_J) + {d ≥ 0 : Pd = 0}`, where `r = rank P` and
`X_J = X ∩ {λ_{J^c} = 0}`. In particular `z_K(w) = min_{|J| ≤ r} z_{K_J}(w_J)`.

*Proof.* For `λ ∈ X`, the polyhedron `{λ' ≥ 0 : Pλ' = Pλ}` lies inside `X`.
Its vertices have support at most `r` (Minkowski–Weyl). ∎

This mirrors the MILP fact that corner-polyhedron vertices use at most
(number of rows) rays.

**Proposition 3 (fixed `k` is polynomial).** Let `y_v` range over the vertices
of `{y ∈ R^k : P^T y ≤ w}`. Then

`z_K(w) = min over v of min{ y_v^T z : z ∈ cone{p_j : p_j^T y_v = w_j}, q(s̄ + z) ≤ 0 }`.

- There are `O(N^{⌊k/2⌋})` vertices by the upper bound theorem; at most
  `2N − 4` for `k = 3`.
- Each piece is a `k`-dimensional problem: a linear objective over a
  simplicial cone with one quadratic constraint. This assumes `rank P = k`
  (otherwise reduce), and degenerate cells are triangulated. Each piece is
  solved in closed form by `2^k` face-KKT systems.
- The same oracle separates over the corner hull, so efficacy-optimal cuts are
  polynomial for fixed `k` (ellipsoid or row generation).
- The implemented exact routine `sfree.corner_bound` (support enumeration)
  agrees with SCIP global solves to `5·10^-7` relative on 40 instances
  (`test_sfree.py`).

**Proposition 4 (NP-hard for general `k`).** Take `K = R^k_+`, `s̄ = 0`,
`q(s) = μ − s^T A_G s` (Chmiela Case 2) and `w = 1`. Then

`z_K(1) = sqrt(μ / max_{Δ} s^T A_G s) = sqrt(μ ω(G) / (ω(G) − 1))`

by Motzkin–Straus. So computing the best single-cut bound over all maximal
quadratic-free sets decides clique number and is NP-hard.

### 3.2 The implemented family is not enough (proved on explicit families)

**Proposition 5 (SCIP's `λ` can be arbitrarily bad inside its own family).**
Let `S = {y^2 ≥ x^2 + 1}`, `x̄ = (x0, 0)`, rays `(−1, 0)` and `(0, 1)`, and
`w = (ε, 1)`.

- SCIP's set (a wedge tangent at `x = x0`) gives `z = ε(x0 + 1/x0)`, when
  this is below `sqrt(x0^2 + 1)`.
- The horizontal strip `|y| ≤ 1` (constant `Γ`, `λ = (0, 1)`) gives `1`.
- `z_K ≥ 1`.

Check (E8): `x0 = 1000`, `ε = 10^-6` gives SCIP `0.001`, strip `1`,
`z_K = 1.001`.

**Proposition 6 (the whole constant-`Γ` family has approximation factor 0).**
Let `S = {y^2 ≥ x^2 + 1}`, `s̄ = 0`, `r = sqrt(1 + a^2)`, rays
`r1 = (a, r)` and `r2 → −r1` (pointed perturbation), and `w = (1, 1)`.

- Every constant-`Γ` (symmetric-wedge) set `{|y| ≤ (u x + 1)/sqrt(1 + u^2)}`
  gives the cut `(r s_u − ua) λ1 + (r s_u + ua) λ2 ≥ 1`, with
  `s_u = sqrt(1 + u^2)`.
- All these cuts contain the point `(1/(2r), 1/(2r))`, so the closure bound is
  `≤ 1/r`.
- The oblique split `{|ry − ax| ≤ 1}` is S-free, because
  `cosh(s − t) ≥ 1` in hyperbolic coordinates. It exits both rays exactly at
  their first S-points and gives bound `1 = z_K`.
- Its `Γ` is non-constant (`Γ(1) ≠ Γ(−1)`), and it is the Lorentz-boost image
  (`cosh s = r`, `sinh s = −a`) of SCIP's strip.

Check (E10), closure of 20,001 symmetric sets:

| `a` | `z_K` | Split bound | Symmetric closure |
|---|---|---|---|
| 10 | 0.981 | 0.980 | 0.0995 (≈ `1/r`) |
| 100 | 0.845 | 0.833 | 0.0100 (≈ `1/r`) |

At `a = 100` the fixed perturbation `η = 10^-3` shrinks `z_K`; a smaller `η`
restores it to about 1.

**Proposition 7 (transformations = `Γ` when one eigenvalue sign is simple;
homogeneous case).** For `Q_h ⊂ R^n × R` (`m = 1`, `n ≥ 2`), every
full-dimensional maximal `Q_h`-free set is `L(C_λ)` for some orthochronous
Lorentz transformation `L ∈ SO^+(n, 1)`.

*Proof.* By MPS Thm 1.2, a maximal set is `C_Γ` with `Γ(1) ≠ −Γ(−1)`. Its two
normals `(Γ(1), −1)` and `(Γ(−1), 1)` are a past and a future null vector.
`SO^+(n, 1)` acts on the projectivized null cone `S^{n−1}` as the Möbius group,
which is 2-transitive, and it preserves time orientation. So some `L` sends the
normals of `C_λ` (the points `−λ` and `λ`) to positive multiples of those of
`C_Γ` (the points `−Γ(1)` and `Γ(−1)`). ∎

For `n = 1` (any `m`), every maximal set has constant `Γ`:

- for `m ≥ 2`, `Γ` is a continuous map from a connected sphere to `{±1}`, so it
  is constant;
- for `m = 1`, maximality forces `Γ(1) = Γ(−1)`.

So in signatures `(n, 1)` and `(1, m)`, the "choice of transformation" of
Muñoz–Serrano §6 is the same as the "choice of `Γ`". These signatures include
all nondegenerate homogenized 2-variable quadratics.

The extension to the inhomogeneous slices (MPS 2026 Thms 4–5, dropped
inequalities `G ≠ D^m`) is not yet checked. The 2-D hyperbolic case is
consistent: a boost shifts the tangency parameter of the upper branch by `+s`
and of the lower branch by `−s`, so symmetric wedges reach every asymmetric
wedge.

### 3.3 Computations

All values are ratios to the exact corner bound `z_K(w)`, i.e. the fraction of
the best possible single-cut bound. Instances are random; see the scripts for
the generators.

| Experiment | Setting | SCIP set | Best constant `λ` | Full family or orbit |
|---|---|---|---|---|
| E1 (`exp1_ratio.py`) | general `k = 2, 3, 4`, `N = k … 8`; bilinear `k = 3`; about 300 instances per row | mean 0.85–0.91, median 0.95–0.99, 10% quantile 0.47–0.72, below 0.5 in 2–11% | — | — |
| E2 (`exp2_bestlambda.py`) | 40 per row | mean 0.85–0.90 | mean 0.93–0.99; min 0.007 (k=2), 0.15 (bilinear n=3) | — |
| E6/E7 (`exp6_asym2d.py`, `exp7_sym_worst.py`) | 2-D hyperbolic, 1,200 instances | — | mean 0.953, 1% quantile 0.26, min 0.0019 | asymmetric (full) family: mean 0.9986, 1% quantile 0.975 (grid-limited) |
| E9 (`exp9_family_closure.py`) | *closures*, 2-D, 400 instances | — | symmetric closure: mean 0.94, 1% quantile 0.22, min 0.077 | full closure: min 0.986 |
| E12 (`exp12_orbit.py`) | bilinear `N = 3`, 25 instances | mean 0.744, min 0.076 | 0.880 (min 0.19) | orbit `O(2,2) × λ`: mean 0.9988, min 0.972 |
| E12b (`exp12b_orbit_more.py`) | bilinear `N = 6`; general `k = 3`, `N = 4` | 0.876 / 0.900 | 0.948 / 0.960 | 0.9988 / 0.9989 |
| E12c/d (`exp12c_worst_retry.py`, `exp12d_more_rays.py`) | 3 worst E12b bilinear instances with 150 restarts; 2-var `N = 3` (20); bilinear `N = 10` (12), 60 restarts | 0.88 / 0.91 (min 0.38 / 0.48) | — | **1.000 in every instance run here** (the 0.969 case was an optimizer failure). E12 `N = 3` instances were not re-run. |
| E3 (`exp3_bilinear_lp.py`) | McCormick LPs (4 vars, 4 products, 3 random rows), HiGHS basis; 47 usable of 150; fraction of the single-constraint gap `z1 − z_LP` | mean 0.72, median 0.86 | — | corner (best cut): mean 0.78, **median 1.00**; bound-aware corner 0.79 |

What the computations add:

- For bilinear `w = xy` and 2-variable quadratics, a 3–7-parameter search over
  transformations got within 3% of the exact best cut in every tested corner.
  It got to within `10^-4` whenever enough restarts were used. This is the
  numerical basis of the *orbit sufficiency conjecture* (OQ1a) for signature
  (2,2).
- For bound-type criteria, "bound-exact for all `w`" is equivalent to "the
  orbit closure equals the corner-hull dominant", because the dominant is
  determined by its support in all directions `w ≥ 0`.
- In LP-embedded bilinear instances, the best single cut closes the whole
  single-constraint gap in more than half the instances. SCIP's cut leaves a
  median of 14% of that gap.

Supporting checks:

- `exp11_rank2.py` verifies closure facts. The non-local S-free closure of a
  polytope equals `conv(P ∩ S)` for every closed `S`: a localized
  `(P ∩ {a^T x ≥ b''}) + εB` is S-free. The Balas cone closure at rank 1 does
  not equal it, even for reverse-convex `S` in `R^2`. On the triangle
  `(0,2), (±½, 0)` with the unit disk, the rank-1 closure has vertex
  `X = (0, 0.768)` below the hull chord at height 0.966. Rank 2 reaches the
  hull.
- `exp4_loop.py`: pure loops (SCIP-type cuts) converged on all 11 random
  instances.

### 3.4 Attack plan for OQ1

1. **Signature (n,1) and (1,m), complete.** Extend Prop. 7 through
   homogenization. Handle MPS 2026 Thm 4 (dropped inequalities; possibly
   limits of orbit sets) and Chmiela Case 4 (`h ≠ 0`, zero-eigenvalue linear
   part). Target theorem: for these signatures, optimizing Muñoz–Serrano's
   transformation `T` over the Lorentz group attains every intersection cut.
2. **Signature (2,2), the bilinear core.**
   - Use `O(2,2) ≈ SL2 × SL2` acting on rank-one 2×2 matrices, the null cone.
     Orbit sets correspond to "Möbius graphs" in `RP^1 × RP^1`. General
     maximal sets are non-expansive circle maps (MPS).
   - A bound-optimal cut needs a set that contains an S-free simplex and is
     tangent at one point `λ*`. Prove a *one-point interpolation lemma* for
     Möbius graphs, or find a counterexample.
   - To search for counterexamples, maximize `z_K − orbit` with global
     optimizers over instances. The E12 infrastructure exists.
3. **Approximation-factor classification (OQ1b).**
   - `ρ_2(constant Γ) = 0` (Prop. 6).
   - `ρ(orbit) = 1` for `m = 1` (Prop. 7), modulo step 1.
   - Decide `(2,2)`, then general `(n, m)`. Candidate negative example: facets
     touching `S` at more than `dim O(n,m)` independent tangency points,
     possible when `N` is large.
4. **Algorithm and solver test (OQ1c).**
   - Exact corner bound for `k ≤ 3` via Prop. 3: `O(N)` closed-form pieces
     after a 2-D subdivision.
   - Efficacy- and sparsity-aware selection by row generation over the corner
     hull, preferring sets whose recession cone contains many projected rays
     (zero coefficients).
   - Prototype as a PySCIPOpt separator, then as a patch to `nlhdlr_quadratic`.
   - Measure root gap, cuts per round, nonzeros and nodes on MINLPLib/QPLIB
     against SCIP 10 with `useintersectioncuts` on and off (3 seeds).

### 3.5 Difficulty and risk

**Proved here.**

- Lemmas 1–2 and Props 3–7 are short and elementary.
- Individually their novelty is modest. Lemmas 1–2 are MILP folklore
  transposed. Prop. 7 follows from MPS plus the 2-transitivity of the Möbius
  group.
- The value lies in the combination and in the explicit negative results
  (Props 5–6).

**Hard parts.**

- Orbit sufficiency for (2,2) (1–3 months; may be false for some ray
  configurations).
- A general-signature classification.
- A convincing solver gain.

**Risks.**

1. The MPS/Chmiela group may already be working on selection. They call the
   characterization a "new avenue".
2. Average per-cut gains over SCIP are about 10–25% of the best single-cut bound.
   The large losses are in the tail; typical losses are small.
3. Density, SCIP's stated reason for disabling the cuts, is not solved by
   better selection. It may be eased by needing fewer rounds (E3 medians) and
   by sparsity-aware choice, but that is unproven.
4. The in-house probe showed that root-gap gains do not predict node savings.

**Effort.**

- Steps 1 and 3 (partial): 2–4 weeks.
- Step 4 prototype and benchmark: 2–4 weeks.
- Step 2: uncertain.

---

## 4. Significance

**Proved consequences (this report, first pass).**

- The best intersection cut from any maximal quadratic-free set is NP-hard to
  compute in general.
- It is polynomial for fixed `k`, and it is attained on `≤ rank`-ray
  sub-corners.
- SCIP's fixed set, and the closure of the whole constant-`Γ` family, can be
  arbitrarily worse than the best cut.
- For one negative (or positive) eigenvalue after homogenization, choosing the
  transformation (Lorentz group) is the same as choosing `Γ`, homogeneous
  case.
- The non-local S-free closure of a polytope is exact for any closed `S`. The
  cone-based closure is not exact at rank 1, even in the plane.

**Plausible.**

- A selection routine (orbit search or exact `k ≤ 3` corner separation) would
  raise the per-cut bound from about 0.74–0.91 to about 1.0 of the best
  possible single cut on bilinear and 2–3-variable constraints.
- In the median McCormick-LP instance, one round would close the whole
  single-constraint gap instead of 86%.
- Needing fewer rounds would mean fewer dense cuts, which bears on SCIP's
  density objection.

**Speculative.**

- Turning quadratic intersection cuts on by default.
- Node reductions.
- The Lemma 2 oracle view extending best-cut separation to small-`k` blocks
  with any closed `T`: signomials, exponentials, bilinear graphs with bounds,
  mixed-integer `q`-variables. That extension would skip explicit maximal-set
  characterizations.

**What practical value would still require.**

- An efficient selection criterion that trades depth against density.
- An implementation inside the nonlinear handler.
- Benchmark evidence on node counts, not only root gap.

---

## 5. Recommendation

Pursue OQ1: optimal selection among maximal quadratic-free sets, framed as
(i) orbit sufficiency and (ii) an Averkov–Basu–Paat-type approximation theory
for quadratic corner hulls, with an exact small-`k` separator as the
computational arm.

The question is stated-open in the source papers (Muñoz–Serrano §6–7; MPS
2025 §8, 2026). It is directly actionable in SCIP, and first-pass work already
gives clean results:

- NP-hardness vs fixed-`k` polynomiality;
- an unbounded-factor negative result for the implemented family;
- a Lorentz-orbit theorem in signature (n,1);
- strong numerical evidence that a 7-parameter orbit search attains the exact
  best cut for bilinear constraints.

The main theorem at stake, orbit sufficiency for signature (2,2) or a
classification of approximating families, is well posed and of moderate
difficulty. The solver payoff is real but bounded: better cuts per round, not a
fix for density.

**Score: 6/10** (significance 5, feasibility 7, originality 6).

OQ3 (loop convergence, tied to Tuy's open problem) has higher originality but
low feasibility. OQ2 and OQ4 are harder, and their cut value is partly
captured by the Lemma 2 oracle.

---

## Reproducibility and checks run

All commands ran from
`research-20260928b/scouting/s-free-intersection-cuts/`. Python 3.13, numpy,
scipy, HiGHS (`highspy`), SCIP 10 through PySCIPOpt. These are targeted
checks only; no project-wide checks were run.

- `python3 test_sfree.py`: 0 S-freeness violations for the implemented
  Chmiela Case 1–4 sets (300 sets × 2,000 samples). Exact corner bound vs SCIP:
  max relative difference `5.3e-7` on 40 instances.
- `python3 exp1_ratio.py` → `exp1_ratio.json`.
- `python3 exp2_bestlambda.py` → `exp2_bestlambda.json`.
- `python3 exp3_bilinear_lp.py 11 150` → `exp3_bilinear_lp_11.json`. A small
  run with seed 3 → `exp3_bilinear_lp_3.json`.
- `python3 exp4_loop.py 5 2 12`, `python3 exp4_loop.py 6 3 12` →
  `exp4_loop_k2_s5.json`, `exp4_loop_k3_s6.json`.
- `python3 exp5_worst.py`, `python3 exp5b_inspect.py`: worst SCIP ratios
  (down to 0.003) with no S-hit on either ray.
- `python3 exp6_asym2d.py`, `python3 exp7_sym_worst.py`,
  `python3 exp9_family_closure.py`, `python3 exp9b_worst_geometry.py`.
- `python3 exp8_explicit.py` (Prop. 5), `python3 exp10_split_family.py`
  (Prop. 6), `python3 exp11_rank2.py` (rank-2 closure example).
- `python3 exp12_orbit.py 31`, `python3 exp12b_orbit_more.py`,
  `python3 exp12c_worst_retry.py`, `python3 exp12d_more_rays.py` →
  `exp12*.json`.

Caveats on the numerics:

- Grid and Nelder–Mead optimizations give lower bounds on the best achievable
  family bound.
- The E12 "orbit" sets are homogeneous Muñoz–Serrano sets sliced at `ζ = 1`.
  They are S-free but not necessarily maximal, so orbit results are
  conservative.
- Random instance generators are not representative of MINLPLib.
