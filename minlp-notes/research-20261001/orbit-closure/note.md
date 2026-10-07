# Closures of orbit-family intersection cuts for `w = xy` at one corner

Stream `orbit-closure`, research-20261001 (see [`../PROGRAM.md`](../PROGRAM.md)).
Dates: work began 2026-10-01 and continued on 2026-10-02. A first author run
was interrupted by a usage limit on 2026-10-02; one of its background jobs (the
BP certificate) was later stopped at the user's request
([`CLOSEOUT.md`](CLOSEOUT.md)). This note continues from that state; Section 11
says which earlier outputs were reused and how they were checked. Code is in
[`code/`](code/), raw outputs in [`logs/`](logs/), downloaded sources in
[`sources/`](sources/) ([manifest](sources/MANIFEST.md)). The note builds on the
sfree note
[`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md)
("the sfree note"; its numbering is used when it is cited) and uses results
of the sibling stream [`../ratio-bound/note.md`](../ratio-bound/note.md)
("the ratio-bound note"). Repository commits made outside this program have
included this stream's files; this revision makes no commits or git-state
changes. Final status (2026-10-04): reviewed in two rounds;
[round 2](reviews/review-r2.md) minor fixes applied; the last revision's fixes
checked by the coordinating agent; not refereed. Round 2 confirmed all twelve
round-1 fixes. The coordinating agent reran all certificates, verifiers, tests
and the r2 reviewer's probes, including the λ̂ checks and Theorem 11(c) display fix.
"Reviewed" means checked by another research agent.

## Summary

**Question.** Fix one corner (an LP vertex `s̄` with projected rays
`p_1, …, p_N`) and the bilinear set `S = {w ≤ xy}`. Each set of a family gives
an intersection cut `a^T λ ≥ 1`. Is the closure of all these cuts, the
intersection of the cut halfspaces, equal to the dominant of the corner hull,
`D = cl(conv X + R^N_+)`? Equivalently: is the closure bound `z_cl(w)` equal to
the corner bound `z_K(w)` for every cost vector `w > 0`? The sfree note showed
that the best single cut can miss `z_K` (Theorem 14) and left the closure open.
The families are (A) the sliced orbit sets `C_F`, (B) their maximal completions
(SCIP's Case-4 construction under every transformation and every `λ`), and (BP)
the completions that SCIP's rule `λ = x̂(Ts̄)/‖x̂(Ts̄)‖` produces under every
transformation.

**Main answer: no, for all three families.** At the corner of sfree Theorem 14
(a simplicial cone in `R^3`, three rays) the closures of (A), (B) and (BP) are
all strictly larger than `D`. The answer does not depend on numerics:

1. *Exact certificates* (Theorem 9; computed exactly and checked by a
   separate verifier by the same author, tested on specified mutations). The point
   `(67/250, 41/100, 151/500)`, with coordinate sum `49/50`, lies in the closure
   of (B), hence in that of (A). The point `(51/350, 0, 17/150)`, with sum
   `136/525 ≈ 0.259`, lies in the closure of (BP). Every point of `D` satisfies
   `λ_1 + λ_2 + λ_3 ≥ 1`. So in the direction `w = (1, 1, 1)`:
   `0.97538 ≤ z_cl,A ≤ z_cl,B ≤ 0.98` and `0.2539 ≤ z_cl,BP ≤ 0.2591`, while
   `z_K = 1`. Numerically the closures of (A) and (B) equal their best single
   cut to `10^-7` (about `0.9753854`). The closure of (BP) equals its best
   single cut `16/63 ≈ 0.2540`, and SCIP's own set gives `0.0896`.
2. *Why exactness fails* (Theorem 2, Proposition 3, Corollary 4; proved). An
   exact closure can use only cuts that are tight at every corner minimizer, and
   on a smooth face such cuts agree with `w/z_K` on the support of the
   minimizer. Hence, if at most one ray is outside that support, **the closure
   is exact in direction `w` if and only if the best single cut is**. For three
   rays this holds in every direction whose minimizer uses two rays. Together
   with sfree Theorem 14(3) this already proves the main answer without any
   certificate. This is an exactness analogue of the Averkov–Basu–Paat
   "one-for-all" theorem.
3. *Constant factors* (Theorem 11, Proposition 13, Corollary 14; proved unless
   marked). The approximation factor of a closure at a fixed corner is
   `ρ = sup_w z_K(w)/z_cl(w)`.
   - (BP) has `ρ = ∞` already at the Theorem 14 corner: every (BP) set has
     `a_1 ≥ 7/2`, so `(2/7, 0, 0)` lies in its closure, while
     `z_K(ε, 1, 1) ≥ 367/759` for every `ε > 0`.
   - At the *W-corner* (a simplicial cone in `R^4` whose rays project to
     `e_x, −e_y, e_w, −e_w` at `s̄ = (1, −1, 1)`, with `D = {λ_4 ≥ 2}`), (A) and
     (BP) have `ρ = ∞`, while (B) is exact. For (BP) the infimum of
     `a_1 + a_2` is exactly `(√2 − 1)/2`, attained by SCIP's own set.
   - (A) and (B) at the Theorem 14 corner: `1.1166 ≤ ρ` (certified), and
     `ρ ≈ 1.128` numerically, attained at a support-two direction where the
     closure equals the best single cut.
   - If every ray meets `S`, every family has `ρ ≤ max_j t_j/α_j(C)` for any of
     its sets `C`. Over all corners, (B) has no uniform factor even with the
     vertex fixed (from ratio-bound Theorem B and Proposition 5).
4. *Single cuts versus closures* (Lemma 1, Proposition 5, Proposition 10). The
   closure equals the best single cut in every direction if and only if the
   up-set of cut vectors is convex. In general `z_1 ≥ z_cl/N`. In a support-two
   direction the two gaps vanish together (Corollary 4), but the closure can
   still be larger (numerically by up to `0.084` of `z_K`, family (B)). In the
   support-one direction of the sfree Proposition 16 corner the closure is
   strictly better than every single cut and still not exact, both certified:
   `z_1,A ≤ 0.9839 < 0.99536 ≤ z_cl,A ≤ 0.999 < 1 = z_K`.
5. *Proposition 9 of the sfree note* (Section 8; numerical evidence). At one
   corner, all S-free sets together give `D` (sfree Theorem 1(5)), so the
   orbit-closure gap is caused only by restricting the family. As in
   Proposition 9, re-basing at the new LP vertex removes it in examples: one
   best orbit cut per round reaches `z_K` after 3 cuts at the Theorem 14 corner
   and after 2 at the Proposition 16 corner, in 5 of the 6 instances tried.

**Solver relevance** is limited. Quadratic intersection cuts are off by default
in SCIP 10. The W-corner is closed at once by bound propagation in a solver.
The statements concern cut families at one LP vertex, not solver performance.

**Novelty.** I found no prior statement of these results. Three targeted web
searches (Section 10) and the sibling literature audit found no work on
closures of quadratic-free families. An unsuccessful search does not establish
novelty.

---

## 1. Setting and notation

As in the sfree note (Sections 1 and 8). `S = {(x, y, w) : w ≤ xy}`,
`q(s) = w − xy`, `M(s) = [[w, x], [y, 1]]` (so `det M(s) = q(s)`),
`M_0(p) = [[p_w, p_x], [p_y, 0]]` (the linear part), `E = [[1, 0], [0, 0]]`,
`J = [[0, 1], [−1, 0]]`, `sym(A) = (A + A^T)/2`. The corner is `s̄` with
`q(s̄) > 0` and projected rays `p_1, …, p_N` (columns of `P`); the rays of the
LP cone are linearly independent, their projections need not be (the W-corner
of Section 6 has four projected rays in `R^3`).

- `X = {λ ≥ 0 : q(s̄ + Pλ) ≤ 0}`, `D = cl(conv X + R^N_+)`,
  `z_K(w) = inf{w^T λ : λ ∈ X}`.
- For a closed convex S-free set `C` with `s̄ ∈ int C`: `α_j(C)` is the step to
  the boundary along `p_j` and `a_j(C) = 1/α_j(C)` (`0` if `α_j = ∞`). The cut
  `a(C)^T λ ≥ 1` is valid for `X` (sfree Section 1).
- For a family `𝓕` of such sets: the cut vectors `V = {a(C) : C ∈ 𝓕}`, the
  closure `Cl_𝓕 = {λ ≥ 0 : a^T λ ≥ 1 for all a ∈ V}`, the closure bound
  `z_cl(w) = inf{w^T λ : λ ∈ Cl_𝓕}`, and the single-cut bound
  `z_1(w) = sup_{C ∈ 𝓕} min_j w_j α_j(C)`. Always
  `z_1(w) ≤ z_cl(w) ≤ z_K(w)` and `D ⊆ Cl_𝓕`.
- The approximation factor of `𝓕` at this corner is
  `ρ_𝓕 = inf{α ≥ 1 : Cl_𝓕 ⊆ (1/α) D} = sup_{w > 0} z_K(w)/z_cl(w)`.
  This is the Averkov–Basu–Paat functional for one ray matrix. Their `ρ_f`
  (Section 2 of arXiv:1705.02015, read in [`sources/`](sources/)) also takes
  the supremum over all ray matrices with the vertex `f` fixed.

`Cl_𝓕 = D` if and only if `z_cl(w) = z_K(w)` for every `w > 0`. Both sets are
closed, convex and contain their sums with `R^N_+`. A point of `Cl_𝓕 \ D` can
be strictly separated from `D` by some `u ≥ 0`, and `u + ε1 > 0` still
separates it for small `ε`.

## 2. Closures of cut families

The results of this section hold for every family of closed convex S-free
sets containing `s̄` in their interior, and for every closed `S`, except
Proposition 3, which uses `S = {g ≤ 0}` with a `C^1` function on the corner.
Put `V̂ = cl(conv V + R^N_+)`.

**Lemma 1 (closure bound and single-cut bound).** Let `z > 0`.
(a) For `w ≥ 0`: `z_cl(w) ≥ z` if and only if `w/z ∈ V̂`.
(b) For `w > 0`: `z_1(w) ≥ z` if and only if `w/z ∈ cl(V + R^N_+)`.
(c) `z_1(w) = z_cl(w)` for every `w > 0` if and only if `cl(V + R^N_+)` is
convex.

*Proof.* (a) Every `a ∈ conv V + R^N_+` satisfies `a^T λ ≥ 1` on `Cl_𝓕`
(`λ ≥ 0`), and so does every limit; so `w/z ∈ V̂` gives `w^T λ ≥ z` on the
closure. Conversely, if `w/z ∉ V̂`, separate strictly: `μ^T (w/z) < β ≤ μ^T a`
for all `a ∈ V̂`. Since `V̂ + R^N_+ = V̂`, `μ ≥ 0`; since `μ^T(w/z) ≥ 0`, `β > 0`.
Then `λ := μ/β ∈ Cl_𝓕` and `w^T λ < z`.
(b) `min_j w_j α_j(C) ≥ z` means `a(C) ≤ w/z`. So `z_1(w) ≥ z` if and only if
for every `ε > 0` some `a ∈ V` satisfies `a ≤ w/((1 − ε) z)`. If
`w/z = lim (a_n + d_n)` with `a_n ∈ V`, `d_n ≥ 0`, then
`a_n ≤ w/((1 − ε) z)` for large `n` because `w > 0`; the converse is immediate.
(c) If `cl(V + R^N_+)` is convex, it equals `V̂`, and (a), (b) agree. If
`z_1 = z_cl` on `R^N_{>0}`, then every point of `V̂` with positive coordinates
lies in `cl(V + R^N_+)` (take `w` equal to the point and `z = 1`). The other
points of `V̂` are limits of such points. ∎

So the closure helps beyond single cuts exactly where the up-set of cut vectors
fails to be convex.

**Theorem 2 (exactness uses only tight limit cuts).** Let `w > 0` and
`z = z_K(w) ∈ (0, ∞)`. Then `z_cl(w) = z` if and only if there are
`m ≤ N` vectors `a^(1), …, a^(m) ∈ cl V` and weights `θ_i > 0`, `Σ θ_i = 1`,
with `Σ θ_i a^(i) ≤ w/z`. In that case `a^(i)T λ* = 1` for every `i` and every
minimizer `λ*` of `w^T λ` over `X`, and `(w/z − Σ θ_i a^(i))^T λ* = 0`.

*Proof.* "If": `Σ θ_i a^(i) ∈ V̂`, so `w/z ∈ V̂`; apply Lemma 1(a). "Only if":
by Lemma 1(a), `w/z = lim b_n` with
`b_n = Σ_{i ≤ N+1} θ_{n,i} a_{n,i} + d_n` (Carathéodory), `a_{n,i} ∈ V`,
`d_n ≥ 0`. All terms are nonnegative and `b_n` is bounded, so after passing to
a subsequence `θ_{n,i} → θ_i`; if `θ_i > 0`, then `a_{n,i}` is bounded and
converges to `a^(i) ∈ cl V`. Dropping the terms with `θ_i = 0` (they are
nonnegative), `w/z ≥ Σ_{θ_i > 0} θ_i a^(i)` with `Σ θ_i = 1`. Limits of valid
cuts are valid, so at a minimizer `λ*` (it exists, sfree Theorem 1(1)):
`1 = w^T λ*/z ≥ Σ θ_i a^(i)T λ* ≥ Σ θ_i = 1`. Hence every `a^(i)T λ* = 1` and
the slack is orthogonal to `λ*`. All `a^(i)` lie in the hyperplane
`{a : a^T λ* = 1}` (`λ* ≠ 0` since `z > 0`), so Carathéodory in that
`(N − 1)`-dimensional affine space reduces the number of points to `N`. ∎

**Proposition 3 (tight cuts on a smooth face).** Let `S = {s : g̃(s) ≤ 0}` with
`g̃ ∈ C^1`, `w > 0`, `z = z_K(w) ∈ (0, ∞)`, `λ*` a minimizer with support `J`,
and `g(λ) = g̃(s̄ + Pλ)`. If `∇_J g(λ*) ≠ 0`, then every `a ∈ R^N` with
`a^T λ ≥ 1` on `X` and `a^T λ* = 1` satisfies `a_J = w_J/z`.

*Proof.* `g(λ*) = 0`: otherwise `(1 − ε)λ* ∈ X` has smaller cost. By the
implicit function theorem, near `λ*` the set `{λ : λ_{J^c} = 0, g(λ) = 0}` is a
`C^1` hypersurface of the face, with normal `∇_J g(λ*)`. Its points near `λ*`
have `λ_J > 0`, so they lie in `X`. For every `d ∈ R^J` with
`∇_J g(λ*)^T d = 0` there is a curve `λ(s)` in it with `λ(0) = λ*` and
`λ'(0) = d`. Since `a^T λ(s) ≥ 1 = a^T λ*` for both signs of `s`,
`a_J^T d = 0`. So `a_J = κ_a ∇_J g(λ*)`. The same holds for `w/z` (it is tight
at `λ*` and valid), `w_J/z = κ_w ∇_J g(λ*)`. Finally
`κ_a ∇_J g^T λ*_J = a^T λ* = 1 = κ_w ∇_J g^T λ*_J` gives `κ_a = κ_w`. ∎

**Corollary 4 (one-for-all exactness).** Under the hypotheses of Proposition 3,
if `|J^c| ≤ 1`, then `z_cl(w) = z_K(w)` if and only if `z_1(w) = z_K(w)`.

*Proof.* Suppose `z_cl(w) = z`. Theorem 2 gives tight `a^(i) ∈ cl V`, and
Proposition 3 gives `a^(i)_J = w_J/z`. If `J^c = ∅`, then `a^(1) = w/z`. If
`J^c = {k}`, then `Σ θ_i a^(i)_k ≤ w_k/z` forces `a^(i)_k ≤ w_k/z` for some
`i`, so `a^(i) ≤ w/z`. By Lemma 1(b), `z_1(w) ≥ z`. ∎

*For `w ≤ xy` with three rays spanning `R^3`.* Minimizers use at most two rays
(sfree Theorem 4, `ρ = 2`). If one uses two rays, then
`∇_J g(λ*) = P_J^T ∇q(t*) ≠ 0` (proof of sfree Theorem 11: `P_J^T ∇q(t*) = 0`
forces `|J| = 1`). So **in every direction `w > 0` with a support-two minimizer,
the closure of any family is exact if and only if its best single cut is**. In
support-one directions `|J^c| = 2`, and the closure can be strictly better
(Proposition 10).

**Proposition 5 (single cuts lose at most a factor `N`).** For every family and
every `w > 0` with `z_cl(w) ∈ (0, ∞)`: `z_1(w) ≥ z_cl(w)/N`.

*Proof.* Let `z = z_cl(w)`. By Lemma 1(a), `w/z ∈ V̂` and `w/z' ∉ V̂` for
`z' > z`, so `w/z` lies on the boundary of `V̂`. Let `μ ≥ 0`, `μ ≠ 0`, support
`V̂` there. As in Theorem 2, `w/z ≥ Σ θ_i a^(i)` with `a^(i) ∈ cl V`. Then
`μ^T a^(i) ≥ μ^T w/z ≥ Σ θ_i μ^T a^(i)`, so all `a^(i)` lie in the hyperplane
`{μ^T a = μ^T w/z}`, and `μ^T w/z > 0`. Carathéodory there leaves at most `N`
points, so some `θ_i ≥ 1/N`. Then `a^(i) ≤ w/(zθ_i) ≤ N w/z`, and Lemma 1(b)
gives `z_1(w) ≥ z/N`. ∎

The factor `N` is attained by abstract families: for `V = {e_1, …, e_N}`,
`z_1(1) = 1` and `z_cl(1) = N`. In the orbit families the largest ratio
`z_cl/z_1` observed is `1.119` (Section 7).

## 3. The families, and three facts used by the certificates

For a `2 × 2` matrix `F`, `C_F = {s : sym(F^T M(s)) ⪰ 0}`. The sliced orbit is
family **(A)**: `C_F` with `det F > 0` (sfree Lemma 10). Family **(B)** consists
of the maximal completions `B_F = cl(C_F + R_+ e_w)` (sfree Lemma 10(4)). A set
is used only if `s̄` is in its interior. Parametrize by
`X = F^T M(s̄)` (`F` is recovered as `F^T = X M(s̄)^{-1}`, positive multiples
give the same set), `S = sym(X)`, `c = (X_12 − X_21)/2`. With
`N_p = M(s̄)^{-1} M_0(p)`, `N_j = N_{p_j}`, `m = M(s̄)^{-1} e_1`:

`A(s) := sym(F^T M(s))`, `A(s̄ + μ p) = S + μ sym(X N_p)`,
`Z := sym(F^T E) = sym(X m e_1^T)`, `v^T Z v = (v^T X m) v_1`.

**Family (BP), SCIP's point rule.** Muñoz–Serrano and Chmiela–Muñoz–Serrano
take `λ = x̂(Ts̄)/‖x̂(Ts̄)‖` for the transformation `T` they use. For
`C_λ = C_I` (`λ = e_1` in the Sylvester coordinates of sfree Lemma 10(2)) the
rule says that `M(s̄)` is symmetric with positive trace. An automorphism
`M ↦ A M B^T` (`det A det B = 1`) has preimage `C_F` of `C_I`, with
`F^T = B^{-1} A`.
The rule at the image point says that `Y = A M(s̄) B^T` is symmetric with
positive trace; then `det Y = q(s̄) > 0`, so `Y ≻ 0` and
`F^T M(s̄) = B^{-1} Y B^{-T} ≻ 0`. Every `S ≻ 0` arises this way. So the sets the
rule produces under all transformations are the `C_F` with `X = S` symmetric
positive definite, a two-parameter subfamily of the three-parameter orbit
(transpositions fix `C_I`). **(BP)** is their completions (SCIP's Case 4), and
**(P)** the uncompleted ones. SCIP's own set is one member of (BP):
`F^T = R_θ` with `(sin θ, cos θ) = x̂(s̄)/‖x̂(s̄)‖`,
`x̂ = ((x − y)/2, (w + 1)/2)` (ratio-bound Lemma S). For each of the three
corners used here I checked numerically that `R_θ M(s̄)` is symmetric positive
definite (`aux_facts.py`, Section 12, item 13). Since `C_F ⊆ B_F`, (B) cuts
dominate (A) cuts with the same `F`, and (BP), (P) are subfamilies of (B), (A).
So `Cl_B ⊆ Cl_A ⊆ Cl_P` and `Cl_B ⊆ Cl_BP ⊆ Cl_P`.

**Lemma 6 (basic facts).**
(a) *(Kept vectors.)* For every `F`, every `s ∈ B_F` and every `v` with
`v^T Z v ≥ 0`: `v^T A(s) v ≥ 0`.
(b) For invertible `F`: `s̄ ∈ int C_F` if and only if `S ≻ 0`.
(c) `e_w` is a recession direction of every `B_F`, so `a_j = 0` for rays that
are positive multiples of `e_w`.

*Proof.* (a) `s = lim (c_n + t_n e_w)` with `c_n ∈ C_F`, `t_n ≥ 0`, and
`A(c + t e_w) = A(c) + t Z`, so `v^T A(c_n + t_n e_w) v ≥ t_n v^T Z v ≥ 0`.
(b) If `A(s̄) ⪰ 0` is singular with kernel `v`, then
`v^T A(s̄ + d) v = d_w (Fv)_1 v_1 + d_x (Fv)_1 v_2 + d_y (Fv)_2 v_1`.
This vanishes for all `d` only if `Fv = 0`, or `v_1 = 0` and
`F_12 = F_22 = 0`. Both are impossible for invertible `F`. So some direction
makes `v^T A v < 0`, and `s̄` is on the boundary.
(c) By construction. ∎

**Lemma 7 (completions lie in a half-space of parameters).** Let
`u = (1, −ȳ)`. If `det F > 0` and `s̄ ∈ int B_F`, then `u^T S u > 0`.

*Proof.* Since `int B_F ≠ ∅`, `C_F ≠ ∅`. This implies `int C_F ≠ ∅`:
the affine image of `s ↦ sym(F^T M(s))` is either all of `Sym_2`
or a plane. In the plane case,
a nonzero kernel element has `M_0(d) = t F^{-T} J`, so `(F^{-T} J)_22 = 0`.
If the affine image contained the cone apex `0`, then `M(s) = t F^{-T} J`,
contradicting `M(s)_22 = 1`. Thus the image plane misses the apex. A plane
meeting the PSD cone but missing its apex cannot support the cone, so it
meets the positive definite cone. Its preimage has nonempty interior.
Now `int B_F = int(C_F + R_+ e_w) = int C_F + R_{>0} e_w` (relative
interiors add for convex sets with nonempty interior), so
`s_τ = s̄ − τ e_w ∈ int C_F` for some `τ > 0`. With `X_τ = F^T M(s_τ)`,
`sym(X_τ) ≻ 0` by Lemma 6(b), so `det X_τ > 0`. Since
`det X_τ = det F · q(s_τ)`, we get `q_τ := q(s̄) − τ > 0`. Now
`X = F^T (M(s_τ) + τE) = X_τ + τ f e_1^T` with
`f = F^T e_1 = X_τ M(s_τ)^{-1} e_1 = X_τ u/q_τ`. So
`u^T X u = u^T sym(X_τ) u (1 + τ/q_τ) > 0`. ∎

(For `det F < 0` the same computation gives `u^T S u < 0`. Such `F` are not in
the family, and the half-space `u^T S u > 0` excludes them; this removed the
obstacle met by the first run's sector certificates, Section 11.)

**Lemma 8 (kept-boundary bound for (BP)).** Let `X = S ≻ 0` be symmetric and
`v = J S m`. Then `v^T Z v = 0` (`v` is kept), `v^T S v = det(S) · m^T S m`,
and `−v^T S N_j v = det(S) L_j(S)` for a linear form `L_j`. Consequently
`a_j(B_F) ≥ L_j(S)/(m^T S m)` whenever this is positive.

*Proof.* `v^T S m = −(Sm)^T J (Sm) = 0`. For every symmetric `2 × 2`
matrix `S`, `S J^T S = −det(S) J`. Hence, with `v = JSm`,
`−v^T S N_j v = det(S) m^T J N_j J S m`, so
`L_j(S) = m^T J N_j J S m` is linear in `S` for every `N_j`.
Also `J^T S J = adj(S)` gives
`v^T S v = m^T S adj(S) S m = det(S) m^T S m`.
These identities are checked symbolically for general `S`, `m` and `N_j`
in `check_review_r1.py`. Then for
`s̄ + μ p_j ∈ B_F`, Lemma 6(a) gives
`det(S) (m^T S m − μ L_j(S)) ≥ 0`, so `α_j ≤ m^T S m / L_j(S)`. ∎

The bound in Lemma 8 holds on the whole family, including near singular `S`,
where fixed test vectors fail. At the Theorem 14 corner,
`L_1 = −8b/3`, `L_2 = 8b/3`, `L_3 = 10b/9` and `m^T S m = 4a/9`, for
`S = [[a, b], [b, c]]`.

## 4. The Theorem 14 corner: no closure is exact

The corner of sfree Theorem 14: `s̄ = (−9/2, 0, 3/2)`; rays `p_j = v_j − s̄`
to `v_1 = (−1, −6, 18)`, `v_2 = (−5, 6, −18)`, `v_3 = (0, 5/2, 5/2)`; three
linearly independent rays in `R^3`. Here `z_K(1, 1, 1) = 1`, attained only at
`λ* = (1/2, 1/2, 0)` on the tangent edge `[v_1, v_2]` (sfree Theorem 14(1),
exact). So `D ⊆ {λ_1 + λ_2 + λ_3 ≥ 1}`. Rays 1 and 2 never meet `S`; ray 3
meets it at step `6/5`.

**Theorem 9.** At this corner:
(a) `λ̂_B = (67/250, 41/100, 151/500) ∈ Cl_B ⊆ Cl_A`, and also
`(27, 41, 30)/99 ∈ Cl_B`.
(b) `λ̂_BP = (51/350, 0, 17/150) ∈ Cl_BP ⊆ Cl_P`, and also
`(1/5, 0, 1/6) ∈ Cl_BP`.
(c) Hence `Cl_A, Cl_B, Cl_BP, Cl_P ≠ D`, separated by `λ_1 + λ_2 + λ_3 ≥ 1`.
In the direction `w = (1, 1, 1)`:
`0.97538 ≤ z_1,A ≤ z_cl,A ≤ z_cl,B ≤ 49/50 = 0.98`,
`0.97538 ≤ z_1,B ≤ z_cl,B`, and
`2539/10000 ≤ z_1,BP ≤ z_cl,BP ≤ 136/525 ≈ 0.25905`.

*Proof.* (c) follows from (a), (b), the bounds `z_1 ≤ z_cl`, and the
inclusions of Section 3. The lower bound `0.97538` rounds down the certified
orbit-set value `0.9753853514` of sfree Theorem 14(3). The lower bound
`2539/10000` is an explicit rational (BP) set with all three steps `≥ 2539/10000`. Each membership
`s̄ + μ p_j ∈ B_F` is shown by a rational `τ_j ≥ 0` with
`S + μ sym(S N_j) − τ_j Z ⪰ 0`, checked exactly (`bp_lower.py`).
(a) and (b) are certified by the box certificates of Section 9.1
(`box_cert.py`). Every leaf is checked again by `verify_box_cert.py` with
separate code:

| point | family | sum | leaves (cut / excluded / skipped) | time |
|---|---|---|---|---|
| `(67/250, 41/100, 151/500)` | B | `49/50` | 8070 / 2253 / 0 | 68.6 s |
| `(3/11, 41/99, 10/33)` | B | `98/99` | 2530 / 725 / 0 | 20.9 s |
| `(51/350, 0, 17/150)` | BP | `136/525` | 420 / 0 / 6 | 1.5 s |
| `(1/5, 0, 1/6)` | BP | `11/30` | 33 / 0 / 5 | 0.1 s |

The first run's SDP certificate `(3/11, 41/99, 10/33) ∈ Cl_A` (25 pieces,
Section 9.2) was re-verified. It is implied by the second row, since
`Cl_B ⊆ Cl_A`. ∎

*Proof without certificates.* The minimizer for `w = (1, 1, 1)` has support
`{1, 2}` and `P_J^T ∇q(t*) = (−3/2, −3/2) ≠ 0`. By Corollary 4, exactness of
any closure in this direction would give a family whose best single cut
attains `z_K = 1`. Sfree Theorem 14(3) shows `z_B < 1`, and (A), (BP) are
weaker. So `z_cl(1, 1, 1) < 1` for (A), (B), (BP) and (P). This argument gives
no point and no gap.

**Numbers** (numerical evidence: cut generation with a heuristic pricing
search, `closure_survey.py`, `closure_survey_B.py`; the closure values are LP
values over exact cuts, and the second value is the LP value divided by the
best pricing value found):

| family | best single cut | closure | |
|---|---|---|---|
| A | 0.9753854 | 0.9753853 / 0.9753854 | certified `[0.97538, 0.98]` |
| B | 0.9753854 | 0.9753854 / 0.9753855 | certified `[0.97538, 0.98]` |
| BP (SCIP's rule, completed) | 0.2539683 (`= 16/63`) | 0.2539683 | certified `[0.2539, 0.25905]` |
| P (SCIP's rule, uncompleted) | 0.2218359 | 0.2218358 / 0.2218359 | |
| SCIP's own set | 0.0896 | — | |

In this direction the closures of (A) and (B) do not improve their best
single cut (to `10^-7`). The best (A) cut is objective-parallel
(`α_1 = α_2 = α_3 ≈ 0.97539`). The best (BP) cut has `α_1 = α_3 = 16/63`,
and the closure minimizer `(1/7, 0, 1/9)` lies on its face. Why (BP) is so weak
is explained by Theorem 11(a): every (BP) set excludes `s̄ + (2/7) p_1`.

## 5. A support-one direction: the closure helps but is not exact

The corner of sfree Proposition 16: `s̄ = (−2, 3, 2)`, rays to `v_1 = (0, 0, 0)`,
`v_2 = (6, −2, 1/4)`, `v_3 = (1, −5/2, 1/2)`. For `w = (1, 1, 1)`,
`z_K = 1` is attained only at `λ* = e_1` (support one; edges at `t*`
transversal).

**Proposition 10.** At this corner, in direction `w = (1, 1, 1)`:
`0.9838 ≤ z_1,A ≤ 0.9839 < 0.9953611 ≤ z_cl,A ≤ 999/1000 < 1 = z_K`.

*Proof.* The single-cut bracket is from the recheck of the sfree note
(`prop16_exact.py`: exact dual certificates at `T_z`, `z = 9839/10000`, and an
explicit rational set at `z = 4919/5000`). I reran it from a copy; it gives
ALL PASS (Section 12). The upper bound on the closure is the first run's SDP
certificate `(24/25, 1/100, 29/1000) ∈ Cl_A` (92 pieces, re-verified). For the
lower bound, `closure_lower.py` takes the 60 orbit sets found by cut
generation and rounds them to rationals. For every ray it certifies a rational
`μ_ij ≤ α_j` exactly (`sym(X_i (I + μ_ij N_j)) ⪰ 0`, `sym(X_i) ≻ 0`). It then
solves the LP `min{1^T λ : λ ≥ 0, Σ_j λ_j/μ_ij ≥ 1 ∀i}` exactly by
enumerating vertices. Its value is approximately `0.9953612`; the exact
rational is in the log and in [`logs/revision-r1/closure_lower_prop16_cuts.json`](logs/revision-r1/closure_lower_prop16_cuts.json),
which saves all 60 rational `X_i` and `μ_ij`. The `--verify` mode rechecks their
exact membership conditions and enumerates the LP vertices without rerunning
numerical cut generation. ∎

So here the closure is strictly better than every single cut, by about
`0.0115`, and still not exact. For (B) the numbers are the same (single
`0.98385`, heuristic; closure `0.9953622`). A (B) box certificate for
`(24/25, 1/100, 29/1000)` was started. Its pricing margin is only `0.35%`, and
the first-order box bound needed too many boxes: I stopped it after 676 s with
247,393 boxes processed and 171,528 queued
([`logs/boxcert_prop16_B.json.gz`](logs/boxcert_prop16_B.json.gz), resumable
after decompressing to a JSON file and using that file as `OUT.json` with
`--resume`). So (B) non-exactness in this direction is numerical evidence
only. (B) non-exactness itself is proved at the Theorem 14 corner.

## 6. Constant factors

### 6.1 Statements

**Theorem 11.**
(a) *(BP at the Theorem 14 corner: `ρ_BP = ∞`.)* Every (BP) set has
`a_1 ≥ 7/2`, so `(2/7, 0, 0) ∈ Cl_BP ⊆ Cl_P`. Every `λ ∈ X` satisfies
`λ_2 + λ_3 ≥ 367/759`. Hence for `w_ε = (ε, 1, 1)`:
`z_cl,BP(w_ε) ≤ 2ε/7` and `z_K(w_ε) ≥ 367/759`, and
`ρ_BP ≥ (367/759)·7/(2ε) → ∞`. Numerically `z_K(w_ε) → 0.48842`, and
`inf_BP a_1 = 7/2` is attained.

At the **W-corner**, `s̄ = (1, −1, 1)` (`q(s̄) = 2`), with rays `r_1 = e_x`,
`r_2 = −e_y`, `r_3 = e_w + e_z`, `r_4 = −e_w + e_z` of a simplicial cone in
`R^4` (variables `x, y, w, z`; the constraint involves `x, y, w` only). The
projected rays are `e_x, −e_y, e_w, −e_w`, and `D = {λ ∈ R^4_+ : λ_4 ≥ 2}`,
`z_K(w) = 2 w_4`:

(b) *(A: `ρ_A = ∞`.)* Every orbit set with `s̄` in its interior has
`a_1 + a_2 + a_3 > 1/20`. So `(20, 20, 20, 0) ∈ Cl_A`, and for
`w_ε = (ε, ε, ε, 1)`: `z_cl,A(w_ε) ≤ 60ε` while `z_K(w_ε) = 2`. With
ratio-bound Theorem A, `(2 − √2)ε ≤ z_1,A(w_ε) ≤ z_cl,A(w_ε) ≤ 60ε`.
(c) *(BP: `ρ_BP = ∞`, with the exact constant.)* For every `S ≻ 0`,
`a_1 + a_2 ≥ (√2 − 1)/2`, with equality if and only if `S` is a multiple of
`I`, and `a_3 = 0`. So `(t, t, 0, 0) ∈ Cl_BP` if and only if
`t ≥ 2(√2 + 1)`, and `z_cl,BP(w_ε) ≤ 4(√2 + 1)ε`. SCIP's own set at this vertex is `S = I`, the
member attaining the infimum. Its cut is
`((√2 − 1)/4)(λ_1 + λ_2) + ((√2 + 1)/4) λ_4 ≥ 1`.
(d) *(B: exact.)* The set `B_F` with `F^T = J^T` is
`{x ≥ 0, y ≤ 0, w ≥ 1 − 2√(−xy)}`. It contains `s̄` in its interior and has
cut vector `(0, 0, 0, 1/2)`. So `Cl_B = D`.

*Proof.* (a) `m = (2/3, 0)`. The vector `e_1` is kept
(`v^T Z v = 2a/3 ≥ 0`); with `−e_1^T S N_1 e_1 = 7a + 6b` it gives
`a_1 ≥ 7 + 6b/a`. Lemma 8 gives `a_1 ≥ −6b/a`. And
`max(7 + 6ρ, −6ρ) ≥ 7/2` for every real `ρ`. For `X`: the rational orbit set
printed in [`logs/thm14_factor.log`](logs/thm14_factor.log) has
`sym(X) ≻ 0`, `sym(X N_1) ⪰ 0` (so `p_1` is a recession direction and
`α_1 = ∞`) and `sym(X) + (367/759) sym(X N_j) ⪰ 0` for `j = 2, 3`, all
checked exactly. Its cut gives `λ_2/α_2 + λ_3/α_3 ≥ 1` on `X`, with
`α_2, α_3 ≥ 367/759` (`thm14_factor.py`).
(b) `X = {λ ≥ 0 : λ_4 ≥ 2 + λ_1 + λ_2 + λ_1λ_2 + λ_3}` (expand `q`); it lies
in `{λ_4 ≥ 2}` and contains `(0, 0, 0, 2)`, which gives `D`. For the cut
vectors, use the dual certificate of Lemma 16 with the integer matrices
`Y_1 = [[141, −63], [−63, 29]]`, `Y_2 = [[4, 67], [67, 1322]]`,
`Y_3 = [[31, −132], [−132, 565]]`, `Y_4 = 0`. They are PSD (determinants
`120, 799, 91`), and `R = −M(s̄)^{-1} Σ_j M_0(p_j) Y_j = [[14, 18], [18, 85]]`.
`R − Y_j/20` is PSD with positive trace for `j = 1, 2, 3`, and so is `R`.
So `Q(a) = R − Σ a_j Y_j` is PSD and nonzero on
`{a ≥ 0 : 20(a_1 + a_2 + a_3) ≤ 1}`. By Lemma 16 no orbit set has a cut vector
there. The lower bound: ratio-bound Theorem A gives `z_A/z_K ≥ 1/((1 + √2)D)`
with depth `D = √2/ε` for `w_ε`.
(c) Here `m = 𝟙/2` (`𝟙 = (1, 1)`), and with `⟨x, y⟩ = x^T S y` the identities
(checked symbolically in `verify_wcorner.py`) are
`v^T Z v = ½⟨𝟙, v⟩ v_1`, `v^T S N_1 v = ½ v_2 ⟨𝟙, v⟩`,
`v^T S N_2 v = ½ v_1 ⟨(1, −1), v⟩`. By Lemma 6(a), every kept `v` gives a
lower bound `a_j ≥ −v^T S N_j v / v^T S v`.
- Ray 1, `v = (s, −1)`, `s ≥ 0`:
  `a_1 ≥ f_1(s) = ((a + b)s − (b + c))/(2(as² − 2bs + c))`.
- Ray 2, `v = (1, t)` with `⟨𝟙, v⟩ ≥ 0`:
  `a_2 ≥ f_2(t) = ((c − b)t − (a − b))/(2(a + 2bt + ct²))`.
- The kept-boundary vector `u = JS𝟙` gives `a_2 ≥ −(b + c)/(a + 2b + c)`.

On the full lines the maxima are
`G_1 = (√(a(a + 2b + c)/det S) − 1)/4` at
`s* = (a(b + c) + √(a det S (a + 2b + c)))/(a(a + b))` (when `a + b > 0`),
and `G_2 = (√(c(a − 2b + c)/det S) − 1)/4` at the mirror point `t*`.

Cases, with `S = [[a, b], [b, c]] ≻ 0`:
- *`a + b ≤ 0`.* Then `b + c > 0` and `c > a`. The restriction for ray 2 is
  `t ≥ t_K = −(a + b)/(b + c)`. One checks `t_K < (a − b)/(c − b) < t*`, so
  `a_2 ≥ G_2`. From `b² ≥ a²` and `−2b ≥ 2a`:
  `c(a − 2b + c)/det ≥ c(3a + c)/(a(c − a)) ≥ 9`, since
  `c(3a + c) − 9a(c − a) = (c − 3a)² ≥ 0`. So `a_2 ≥ 1/2`.
- *`c ≤ b`.* Symmetrically `s* ≥ 0`, `a_1 ≥ G_1 ≥ 1/2`.
- *`a + b > 0`, `c > b`, both maximizers admissible.*
  `4(G_1 + G_2) + 2 = (√(a·𝟙S𝟙) + √(c·𝟙'S𝟙'))/√det` with `𝟙' = (1, −1)`.
  By AM–GM this is `≥ 2 (ac (a + 2b + c)(a − 2b + c))^{1/4}/√det`. And
  `ac((a + c)² − 4b²) − 4 det² = ac(a − c)² + 4b² det ≥ 0`. So
  `G_1 + G_2 ≥ (√2 − 1)/2`, with equality only for `a = c`, `b = 0`.
- *Ray 1 not admissible* (`s* < 0`, which needs `b + c < 0` and
  `b²(2a + 2b + c) > a²c`). Then `a_1 ≥ f_1(0) = −(b + c)/(2c)` and
  `a_2 ≥ −(b + c)/(a + 2b + c)`. With `a = 1`, `β = −b`, these conditions mean
  `β² < c < 2β²/(1 + β)`, and the sum is
  `> (1 − β)/(4β) + β ≥ 3/4`.
- *Ray 1 admissible, ray 2 not.* This needs `b + c < 0` (if `b + c ≥ 0`, the
  restriction is `t ≥ t_K` with `t_K < 0 < t*`). With `a = 1`, `β = −b`, put
  `N(t) = (c + β)t − (1 + β)` and `D(t) = 1 − 2βt + ct²`, so
  `f_2'(t) = (N'D − ND')(t)/(2D(t)²)`. The numerator satisfies
  `(N'D − ND')(t_K)(β − c)² = (c − β²) h(β, c)`,
  `h = c² − (β + 3)c + 2β² + β`. The denominator `2D(t_K)²` is positive
  because `S ≻ 0`; also `c − β² = det S > 0` and `c < β` in this case.
  Thus `f_2'(t_K)` has the sign of `h`, and inadmissibility means `h > 0`, i.e.
  `c < c_−(β)` (the smaller root). Admissibility of ray 1 means
  `c ≥ 2β²/(1 + β)`. Since `h` decreases in `c`, both hold only if
  `h(β, 2β²/(1 + β)) > 0`, i.e. `β(β − 1)(4β² + β − 1) > 0`, i.e.
  `β < (√17 − 1)/8 < 2/5`. Also `h(β, c_1) = c_1² − β² ≤ 0` for
  `c_1 = β(3β + 1)/(β + 3)`, so `c < c_1`. This gives
  `(1 − 2β + c)/(c − β²) > (3 − β)/(β(1 + β))`. So
  `a_1 ≥ G_1 > (√((3 − β)/(β(1 + β))) − 1)/4 ≥ (√(65/14) − 1)/4 > 0.2886`.

In every case `a_1 + a_2 ≥ (√2 − 1)/2`. `a_3 = 0` by Lemma 6(c). Equality at
`S = I` (both maximizers admissible, `s* = t* = 1 + √2`) uses that the
kept-inequality description of `B_F` is exact (sfree Lemma 10(4)). It is
confirmed numerically: on 20,000 random `S`, the minimum is `0.207114`, near
`S = I`, against `(√2 − 1)/2 ≈ 0.207107` (`verify_wcorner.py`). SCIP: `x̂(s̄) = (1, 1)`,
so `θ = π/4` and `R_θ M(s̄) = √2 I`.
(d) `sym(J^T M(s)) = [[−y, (w − 1)/2], [(w − 1)/2, x]]`, so
`C_F = {x ≥ 0, y ≤ 0, |w − 1| ≤ 2√(−xy)}`, `det J^T = 1`. Its upward closure
is S-free: with `r = √(−xy)`, `w − xy ≥ 1 − 2r + r² = (1 − r)² ≥ 0`. From `s̄`
the rays `e_x, −e_y, e_w` stay in it, and `−e_w` leaves at step 2. So its cut
is `λ_4/2 ≥ 1`, and `Cl_B ⊆ {λ ≥ 0 : λ_4 ≥ 2} = D ⊆ Cl_B`. ∎

*Why (A) fails at the W-corner (Lemma 12, proved; explanation only).* No sliced
orbit set `C_F ∩ H` with `det F > 0` has both `e_w` and `e_x` (or `e_w` and
`−e_y`) as recession directions. Proof: S-freeness gives `d_x d_y ≤ 0` on the
recession cone `K' = {d : sym(F^T M_0(d)) ⪰ 0}`. Perturbing `e_x + σ e_w` by
`+δ e_y` violates this, so `cone{e_x, e_w}` lies in the boundary of `K'`. If
`d ↦ sym(F^T M_0(d))` is injective, `K'` is linearly isomorphic to the `2 × 2`
PSD cone, whose boundary contains no two-dimensional cone. Otherwise a kernel
vector `ℓ ≠ 0` lies in the lineality space. Then `e_x + tℓ ∈ K'` for all real
`t` forces `ℓ_y = 0`, and `q(c + tℓ) ≥ 0` for all `t` and all interior `c`
forces `ℓ_x = ℓ_w = 0`. The (B) set of (d) has all three directions, but it is
not a point-rule set (`J^T M(s̄) = [[1, −1], [1, 1]]` is not symmetric).

**Proposition 13 (finite factor when every ray meets `S`).** If every ray
meets `S` (first-hit steps `t_j < ∞`), then for every family and every member
`C`: `ρ_𝓕 ≤ max_j t_j/α_j(C)`.

*Proof.* The first-hit points lie in `X`, so `z_K(w) ≤ min_j w_j t_j`, while
`z_cl(w) ≥ min_j w_j α_j(C) ≥ min_j(α_j/t_j) min_j w_j t_j`. ∎

Neither the W-corner nor the Theorem 14 corner satisfies this: rays 1 and 2 of
the Theorem 14 corner miss `S`, and there (BP) has `ρ = ∞`.

**Corollary 14 (no uniform factor for (B), even with the vertex fixed).** For
the ratio-bound Theorem B corners (vertex `(0, 0, ε)`, three rays, unit
costs), the proved ratio-bound Theorem B(5) gives `z_1,B/z_K → 0` as
`ε → 0`. Proposition 5 gives `z_cl,B/z_K ≤ 3 z_1,B/z_K → 0`.
The automorphism
`(x, y, w) ↦ (x/√ε, y/√ε, w/ε)` maps these corners to corners with the fixed
vertex `(0, 0, 1)` and preserves all ratios. So for `f = (0, 0, 1)` the
Averkov–Basu–Paat functional `ρ_f` of (B) against all S-free sets is infinite.
Since `z_cl,A ≤ z_cl,B`, the same conclusion holds for (A).

The computer-assisted ratio-bound Theorem B2(1) adds the explicit rate:
`z_1,B/z_K ≤ 137√ε/z_0` for every `ε ∈ (0, 1)`, where
`z_0 = z_K = (1 + √(1 + 4ε))/2`. Hence
`z_cl,A/z_K ≤ z_cl,B/z_K ≤ 411√ε/z_0`. Only this rate relies on B2(1)
and inherits its review status.

### 6.2 Families (A) and (B) at the Theorem 14 corner

Numerical scan (`factor_scan.py`, `factor_edge.py`; LMI bisection for the best
orbit cut, so these are upper estimates of the closure factor). Over 291 grid
directions and 297 directions on the edges of the simplex, `z_K/z_1,A` has
median `1.0`, 90% quantile `1.010`, and maximum `1.1283` at
`w ≈ (0.55, 0, 0.45)`, a support-two direction (`λ_K = (0.472, 0.639, 0)`).
On the edges `w_1 = 0` and `w_3 = 0` the maxima are `1.0011` and `1.0000`.
In the worst direction the closures equal the best single cut:
`z_cl,A = 0.2301778`, `z_cl,B = 0.2301778`, `z_1,A = 0.2301768`,
`z_K = 0.2596998` (`closure_at.py`; ratio `1.12826` for both). A certified
lower bound on the factor in this direction: `q > 0` on the simplex
`{λ ≥ 0 : w^T λ ≤ 649/2500}` for `w = (11/20, 10^-6, 9/20)`, by exact face
enumeration (`zk_lower.py`), so `z_K(w) ≥ 0.2596`. And
`(2211, 8805, 2464)/10000 ∈ Cl_B` (box certificate, 5518 cut and 1543 excluded
leaves, verified), so `z_cl,B(w) ≤ 0.2324859`. Hence
**`ρ_A ≥ ρ_B ≥ 1.1166` (certified) and `ρ_A, ρ_B ≈ 1.128` (numerical)**. I did
not prove that `ρ_A` or `ρ_B` is finite at this corner. The scan, which
includes directions within `10^-6` of every edge, found no growth.

### 6.3 Comparison with Averkov–Basu–Paat

ABP (SIOPT 28, 2018; arXiv:1705.02015, Theorem 5) prove for lattice-free sets:
a family's closure approximates an `L`-cut within a constant factor, uniformly
over all ray matrices, only if a single member does ("one-for-all"; no synergy
of cuts). Corollary 4 is an analogue for **exactness** at one corner and one
direction. It needs `|J^c| ≤ 1` and a smooth active face, and it can fail in
support-one directions (Proposition 10: there the closure is strictly better
than every single cut). Theorem 11(a)–(c) give infinite factors **at a fixed
ray matrix**. This is stronger than ABP's uniform `ρ_f = ∞`, and it happens
because some rays miss `S` (Proposition 13). ABP's Theorem 5 assumes
polyhedral `L` with boundedly many facets and an `f`-closed family; neither
the corner hull nor the orbit families fit those hypotheses directly, and I did
not try to transfer their proof.

## 7. Single-cut gaps versus closure gaps

The survey instances of the first run (all `w = (1, 1, 1)`, `z_K = 1`;
numerical, `logs/closure_survey_*.jsonl`). "Gain" is closure minus single cut.
The instance `adv8_3` (vertex nearly on `∂S`) is omitted: its single-cut value
disagrees with the sfree note (0.0268 here, 0.0280 there), and I regard it as
numerically unreliable.

| instance | support | A: single → closure | B: single → closure | P | BP: single → closure |
|---|---|---|---|---|---|
| thm14 | 2 | 0.97539 → 0.97539 | 0.97539 → 0.97539 | 0.2218 | 0.2540 → 0.2540 |
| bigA | 2 | 0.83477 → 0.83477 | 0.83477 → 0.83477 | 0.3431 | 0.3431 → 0.3431 |
| adv8_1 | 2 | 0.6224 → 0.6354 | 0.7078 → 0.7921 | 0.3532 | 0.4238 → 0.4479 |
| adv8_4 | 2 | 0.4526 → 0.5065 | 0.4526 → 0.5065 | 0.1199 | 0.1693 → 0.1693 |
| prop16 | 1 | 0.98385 → 0.99536 | 0.98385 → 0.99536 | 0.3986 | 0.4272 → 0.4272 |
| prop16_v2_1 | 1 | 0.99923 → 0.99967 | — | 0.4228 | — |
| prop16_v8 | 1 | 0.98765 → 0.99574 | — | 0.3358 | — |
| supp1_1074 | 1 | 0.99311 → 0.99311 | 0.99311 → 0.99311 | 0.7706 | 0.7934 → 0.7934 |
| supp1_3437 | 1 | 0.99525 → 0.99525 | — | 0.5800 | — |
| supp1_4580 | 1 | 0.99062 → 0.99062 | — | 0.9422 | — |
| supp1_5512 | 1 | 0.99829 → 0.99873 | 0.99832 → 0.99874 | 0.3742 | 0.3910 → 0.3910 |

The (B) single-cut values are heuristic lower bounds (sampling and
Nelder–Mead); P values are single = closure in every row.

What this shows:
- *Exactness.* In support-two rows exactness of the closure and of single cuts
  coincide (Corollary 4; here neither is exact). In support-one rows the
  closure never became exact when single cuts were not. Whether it can is open.
- *Size.* The closure gain is `0` to `0.084`, never more than a factor `1.12`
  (Proposition 5 allows `3`). The gain is not tied to the support: it is `0`
  at thm14 and bigA (support two) and `0.054`/`0.084` at adv8_4/adv8_1
  (support two). One-for-all holds quantitatively at some corners and not at
  others.
- *Point-rule families.* For (P) and (BP) the closure equals the best single
  cut in 17 of 18 cases (11 P and 7 BP values; exception: adv8_1, BP). So
  their up-sets of cut vectors looked convex near the optimum. I have no explanation; (P) and (BP)
  are two-parameter families.
- *Constant factors.* Proposition 5 says that the factor of single cuts is at
  most `N` times that of the closure. So at a fixed corner, single-cut factors
  and closure factors are finite or infinite together; Theorem 11 gives
  corners where both are infinite.

## 8. Relation to Proposition 9 of the sfree note

Proposition 9 shows that intersection cuts tied to LP bases need more than one
round, even when every single cut is optimal, and that a second round (at the
new vertex) closes the gap. For `w ≤ xy` at one corner, all S-free sets
together give `D` (sfree Theorem 1(5)); the closure gap of Theorem 9 comes only
from restricting the family. Does re-basing remove it? `loop_rank2.py`
(numerical evidence) works in the λ-space of the corner. Each round takes the
LP optimum `v` over `{λ ≥ 0}` and the cuts so far, and forms the corner at `v`
(three tight constraints `Gλ ≥ h`, new rays `P G^{-1}`, reduced costs
`G^{-T} w`). It adds the best orbit cut (family (A), LMI bisection) for that
corner, mapped back to λ-space. Cuts from later corners are valid for `X`
because each new cone contains the current polyhedron.

| instance | `z_K` | LP bound after 1, 2, 3, … cuts | cuts to reach `z_K` |
|---|---|---|---|
| thm14 | 1 | 0.97539, 0.98097, 1.0 | 3 (the next vertex is `λ*`, with `q = 0`) |
| prop16 | 1 | 0.98385, 1.0 | 2 |
| supp1_5512 | 1 | 0.99829, 1.0 | 2 |
| bigA | 1 | 0.83477, 0.87574, 0.94583, 0.98023, 0.98023, 1.0 | 6 |
| adv8_4 | 1 | 0.45263, 0.47486, 0.47981, 0.71275, 0.71275, 0.72135, 0.72306, 1.0 | 8 |
| adv8_1 | 1 | 0.6224, …, 0.91713 (stalled) | not reached in 12 rounds |

Rounds with zero reduced costs add almost nothing (the corner bound at such a
vertex is 0), as in sfree Section 9.3. So the bilinear picture matches
Proposition 9 in these examples. The rank-1 orbit closure at the vertex is
not `D`, but the cuts of the next rounds, taken at new vertices with new rays,
reach the corner bound. At the Theorem 14 corner three single orbit cuts
already do better than the closure of all orbit cuts at `s̄`. This is evidence
from six instances in one direction, not a convergence result. The
`multiround` stream treats multi-round rules in general.

## 9. Certificates

### 9.1 Box certificates (families B and BP)

**Lemma 15.** Let `λ̂ ∈ R^N_+`, and let the parameters `X(t)` of a family
depend affinely on `t` in an axis-parallel box. Suppose that for each ray `j`
in a set `R` a rational
vector `v_j` satisfies, at every vertex of the box, `v_j^T X N_E v_j ≥ 0`
(kept) and `n_j := −v_j^T X N_j v_j > 0`. Put
`μ_j = max_vertices v_j^T X v_j / n_j`. Then every member in the box with `s̄`
in `B_F` has `α_j ≤ μ_j`. If `Σ_{j ∈ R} λ̂_j/μ_j ≥ 1` (with Lemma 8 bounds
allowed in place of `1/μ_j` for (BP)), every member in the box satisfies
`a^T λ̂ ≥ 1`. If instead some kept `v` has `v^T X v < 0` at every vertex, no
member of the family lies in the box.

*Proof.* For `μ > μ_j`, `v_j^T A(s̄ + μ p_j) v_j = v^T X v − μ n_j` is affine in
`X` and negative at every vertex, hence on the box. By Lemma 6(a),
`s̄ + μ p_j ∉ B_F`. Exclusion is the same argument at `s̄`. ∎

*Domains.* (BP): `X = S`, trace one, a disk; one chart with skipped boxes that
miss the open disk (exact test). (B): by Lemma 7, members have
`t_1 := u^T S u > 0`. With `U = [u, e_2]`, `U^T X U = [[t_1, t_2], [t_3, t_4]]`,
and the charts are the seven facets `t_i = ±1` of `[−1, 1]^4` with `t_1 ≥ 0`.
They contain a positive multiple of every such `X`. Boxes are bisected along
their longest side; test vectors are chosen in floating point and every
condition is checked exactly.

`verify_box_cert.py` rebuilds the charts and the bisection trees and checks
every leaf with separate code by the same author (it recomputes `N_j`, `N_E`,
`m`, the Lemma 8 forms by its own polynomial division, and the exact disk
test). It returns a nonzero status on failure. Each listed ray must have a canonical in-range
key and appear exactly once across the fixed-vector and kept-boundary bounds;
unlisted rays contribute zero (`λ̂ ≥ 0` is checked). The verifier also checks
that `λ̂` has exactly one entry per ray. Duplicate JSON keys are rejected.
`test_verify_box_cert.py` checks rejection of specified mutations: point
scaled by `9/10`, a leaf removed, status incomplete, a test vector changed,
a cut leaf relabelled "skip", a box moved,
an exclusion vector replaced, `s̄` changed, kept-boundary rays dropped, the
chart kind changed, ray-key aliases, repeated rays, overlap between bound
types, out-of-range keys, duplicate literal JSON keys, negative or missing or
extra point coordinates, and both reviewers' false-point probes.
All 56 tested mutations are rejected, and both original
certificates are accepted. These finite tests do not prove rejection of every
possible corruption. Review round 1 found the duplicate-ray soundness hole;
the revised verifier rejects the reviewer's probe (Section 12).

*Two observations that made this work.* The first run's (B) search failed for
two reasons. It used `F`-independent certificates over sectors of first rows of
`F`, and it did not exclude sets with `det F < 0`. Lemma 7 removes the second
problem, and per-box primal test vectors replace the first. In the (BP) disk,
fixed test vectors cannot work in boxes that cross the boundary of the disk,
because the window of valid test vectors shrinks to a point at singular `S`.
The kept-boundary vector of Lemma 8 depends on `S` and covers these boxes.
At the W-corner one boundary point (`S ∝ (1, −1)(1, −1)^T`, where `JS𝟙 = 0`)
still defeats the box method. There the result rests on the analytic proof of
Theorem 11(c). A diagnostic run of the first box version (disk chart, before
these fixes) is kept in
[`logs/diag_boxcert_wcorner_BP_diskchart_v0.json.gz`](logs/diag_boxcert_wcorner_BP_diskchart_v0.json.gz).

### 9.2 SDP certificates (family A; first run)

**Lemma 16.** Let `Π` be a polytope of nonnegative cut vectors, and let
`I_0` index coordinates fixed at zero on `Π`. Suppose there are symmetric PSD
matrices `Y_j`, with `Y_j = 0` for `j ∈ I_0`, such that
`R = −M(s̄)^{-1} Σ_j M_0(p_j) Y_j` is symmetric and `Q(a) = R − Σ_j a_j Y_j` is
PSD with positive trace at every vertex of `Π`. Then no orbit set with `s̄` in
its interior has cut vector in `Π + cone{e_j : j ∈ I_0}`. Thus coordinates
with zero multipliers may range freely over `R_+`; for the simplex certificates,
`I_0 = {j : λ̂_j = 0}`.

*Proof.* `Q` is affine, so its PSD and positive-trace conditions extend from
the vertices to `Π`. It is unchanged along the added coordinates because
`Y_j = 0` there. With `A_0 = S ≻ 0` (Lemma 6(b)) and
`A_j = sym(F^T M_0(p_j))`, the cut vector satisfies `a_j A_0 + A_j ⪰ 0`
(for `a_j = 0` this is the recession condition). So
`0 ≤ Σ_j ⟨a_j A_0 + A_j, Y_j⟩ = ⟨A_0, Σ a_j Y_j⟩ − tr(F^T M(s̄) R) = −⟨A_0, Q(a)⟩`.
This is negative for `Q ⪰ 0`, `Q ≠ 0`. ∎

`certify_closure_point.py` covers `{a ≥ 0 : λ̂^T a ≤ 1}` by bisected simplices
with such certificates, including free nonnegative coordinates when `λ̂_j = 0`.
`verify_closure_cert.py` re-checks them and returns a nonzero status on failure.
Before constructing the simplex, it checks that `λ̂ ≥ 0` and that `λ̂` has
exactly one entry per ray.
Outside pruning uses `instance.xpoints`, checks each point lies in `X`, and
requires zero entries on the free coordinates before using vertex inequalities.
I re-verified the three (A) certificates of the first run: Theorem 14 corner
(25 pieces), Proposition 16 corner (92 pieces), and W-corner (1 piece).

## 10. Prior work and novelty

- *Sfree note.* This note answers its open question (Summary, item "Open";
  §10.2): the closure of the orbit family is not exact for bilinear
  constraints, and neither is the closure of the completions or of the point
  rule. The scout's OQ1(a) claimed that single-cut exactness for all `w` is
  equivalent to closure exactness. The sfree note kept only one direction.
  Corollary 4 gives the converse in directions with `|J^c| ≤ 1`, and
  Proposition 10 shows that in support-one directions the closure can be
  strictly better, though not exact in the cases examined.
- *Ratio-bound note (same continuation).* I use its Lemma S (SCIP's set as an
  orbit member), Theorem A (single-cut lower bound by depth) and Theorems B
  and B2 (single-cut ratio → 0, with the computer-assisted rate in B2).
  Theorem 11(a) adds that SCIP's family stays bad even as a closure, at a
  fixed corner.
- *Averkov–Basu–Paat* (SIOPT 28 (2018) 904–929; arXiv:1705.02015v1, read in
  full for Sections 1–2). See Section 6.3.
- *Muñoz–Serrano (2022), Muñoz–Paat–Serrano (2025, 2026), Chmiela–Muñoz–Serrano
  (2023).* These define the sets, the completion and the point rule; read
  through the sfree note and its sources, not re-read here.
- *Cut-generating functions.* The closure of all S-free sets at one vertex
  equals `D` (sfree Theorem 1(5); Kılınç-Karzan–Steffy 2016 Cor. 2, per the
  sibling stream [`../intersection-literature/note.md`](../intersection-literature/note.md)).
  The present results concern proper subfamilies.
- *Search.* 2026-10-02, web search: "closure of intersection cuts family
  maximal quadratic-free sets bilinear constant factor approximation";
  "one-for-all Averkov Basu Paat closure intersection cuts S-free sets
  nonconvex quadratic"; "intersection cut closure nonconvex quadratic
  programming strength closure maximal S-free 2025 2026 arXiv". The hits were
  the known Muñoz–Serrano, MPS and ABP papers and seminar pages; none discusses
  closures of quadratic-free families. The intersection-literature stream's
  larger citation search (2026-10-01) found no work on choosing among maximal
  quadratic-free sets. This is an unsuccessful search; it does not establish
  novelty. Risk: the MPS group studies these families actively, and
  concurrent work is plausible.

## 11. Status of the earlier run, and corrections

Reused and re-checked outputs of the first run (2026-10-01/02):
- the three (A) SDP certificates (re-verified, Section 9.2);
- the survey logs `closure_survey_a.jsonl`, `closure_survey_b.jsonl`,
  `closure_survey_B.jsonl`. They were produced with `orbit_lib.cut_A`,
  `cut_B_fast` and `closure.py`. Later edits to these files added families and
  did not change the (A)/(P) code paths used by the surveys. `cut_B_fast` was
  validated against a fine angular grid to `10^-5` in that run, and here
  against the closed forms of Theorem 11(c) to `3·10^-14`
  (`aux_bp_regions.py`, Section 12). They are numerical evidence only.
- `loop_rank2.py` (written but not run then; run here).

Not reused: the (B) sector certificate runs (`closure_cert_thm14_B*.log`,
stopped incomplete) and the BP triangle run (`closure_cert_wcorner_BP.log`,
stopped at the user's request, see [`CLOSEOUT.md`](CLOSEOUT.md)). The
CLOSEOUT asked not to rerun the BP experiment unchanged. It was not rerun.
Its claim, `(6, 6, 0, 0) ∈ Cl_BP` at the W-corner, is now proved analytically
in sharper form (Theorem 11(c): `(t, t, 0, 0) ∈ Cl_BP` iff `t ≥ 2(√2 + 1)`).

Corrections and qualifications:
- *Sfree note, Summary "Open" and §10.2:* "whether the closure of the orbit
  family is exact is open". It is not exact (Theorem 9). This also holds for
  the completions (B) and the point rule (BP).
- *Sfree note, §8.6:* the adversarial instance with the vertex nearly on `∂S`
  (`adv8_3` here) gives single-cut value `0.0268` with the first run's
  bisection, against `0.0280` (Clarabel) in the sfree note. Both are inside the
  range the sfree note already called numerically ill-posed. I did not use it.
- *First run's intermediate claims* (from its transcript; treated with
  suspicion): "(B) needs sector-dependent certificates and is out of reach".
  Superseded by Lemma 7 and Section 9.1. "(BP) at the W-corner: `inf(a_1 + a_2) ≈ 0.2071`".
  Confirmed and proved exactly. "The closure equals the single cut at thm14".
  Confirmed numerically and bracketed (Theorem 9(c)).
- `certify_closure_point.py`: its docstring referred to lemma numbers of a
  draft that was never written. A header now points to Lemma 16 and says which
  parts are superseded.

### 11.1 Revision after review round 1

Revised on 2026-10-03 to address all twelve issues in
[`reviews/review-r1.md`](reviews/review-r1.md). The main answer remains no for
(A), (B) and (BP). Review round 2 confirmed all twelve fixes. The numbers below
are the review's issue numbers; result numbers are those of this revised note.

1. **Duplicate rays in the box verifier.** The verifier now requires canonical
   in-range ray keys and counts each listed ray exactly once across `v` and
   `kb`. It rejects repeated entries, aliases, overlap between bound types,
   and duplicate literal JSON keys. All five completed certificates pass;
   all 33 tested mutations fail. The reviewer's doubled-ray false certificate
   now exits 1. The note calls this separate code by the same author and
   describes the finite mutation tests, rather than claiming independence or
   rejection of every corruption. Section 13 records the soundness-hole history.
2. **Rounded certified bounds.** Every certified `0.97539` lower endpoint is
   now `0.97538`, below the certified `0.9753853514`. Proposition 10 uses
   `0.9953611`, below its exact LP value `0.995361184…`; rounded values in the
   proof and checks table are labelled approximate. The arithmetic audit also
   checks the other rounded certified endpoints and the factor lower bound.
   In Theorem 11, the rounded W-corner cut is replaced by its exact coefficients,
   and the case (v) bound is written `> 0.2886` rather than as a rounded equality.
3. **Section 7 count.** The count is 17 of 18: 11 P values and 7 BP values,
   with only adv8_1 BP differing. The audit counts the displayed table entries.
4. **Lemma 7 interior.** The proof now explains why a nonempty sliced `C_F`
   has nonempty interior: the image is all of `Sym_2` or a plane missing the
   PSD cone's apex. The image-plane criterion is checked symbolically.
5. **Lemma 8 general proof.** The proof uses `S J^T S = −det(S) J` to derive
   `L_j(S) = m^T J N_j J S m` for every instance. Symbolic checks cover general
   `S`, `m`, `N_j` and reproduce all three Theorem 14 forms.
6. **Closure verifier pruning.** Outside pruning requires `x_j = 0` on every
   free coordinate (`λ̂_j = 0`). Producer and verifier now use
   `instance.xpoints` consistently; previously the producer kept seeds there
   but wrote its generated list at the top level. The producer also avoids
   pruning with points positive on free coordinates. The three current closure
   certificates pass. The legacy 25-piece certificate has identical instance
   and piece data; it also passes after its wrapper is converted to the current
   format in `logs/revision-r1/`. Targeted regressions accept valid pruning and
   reject both an invalid instance point and pruning on a free coordinate.
7. **Lemma 16 unbounded domain.** The statement includes nonnegative unbounded
   coordinates with zero multipliers; the proof explains that `Q` is unchanged
   along them. This covers Theorem 11(b), where `Y_4 = 0`.
8. **BP transformation.** Section 3 now says that `C_F` is the preimage of
   `C_I` when `F^T = B^{-1}A`.
9. **Numbering.** The former Lemma 14, Proposition 12 and Corollary 13 are now
   Lemma 12, Proposition 13 and Corollary 14, in order of appearance. All note
   references are updated.
10. **Explicit rate.** Corollary 14 cites ratio-bound Theorem B2(1), labels it
    computer-assisted, and states `z_cl,B/z_K ≤ 411√ε/z_0` for `ε ∈ (0, 1)`.
    The theorem statement and domain were checked against the sibling note;
    the same rate holds for (A).
11. **Saved Proposition 10 cuts.** A `timeout 1800` regeneration saved all 60
    rational sets, certified steps, exact LP value and minimizing point in
    [`logs/revision-r1/closure_lower_prop16_cuts.json`](logs/revision-r1/closure_lower_prop16_cuts.json).
    Its exact value matches the original log. A new `--verify` mode rechecks
    this data without numerical generation; it passes. Section 13 records
    the original missing-data limitation and this correction.
12. **Resume instructions.** Section 5 says to decompress the gzipped
    checkpoint first and use the JSON as `OUT.json` with `--resume`. No stopped
    search was resumed.

The header also replaces the false uncommitted-work claim with the history of
repository commits made outside the program, and marks this revision as
awaiting confirmation. All edits are within `orbit-closure/`; review files
are unchanged. No commits or git-state changes were made. The stopped
Proposition 16 (B) box search and BP triangle search were not run. Section 12
records the revision checks and their logs.

### 11.2 Revision after review round 2

Revised on 2026-10-03 to address N1, N2, O1 and O2 in
[`reviews/review-r2.md`](reviews/review-r2.md). This revision has not been
re-reviewed. The main answer and all certified values are unchanged.

1. **N1: closure-point domain.** Both verifiers now reject `λ̂` unless it
   has exactly one nonnegative entry per ray, before using any coordinate.
   The tests include negative entries on unlisted or inactive rays, missing
   entries, and extra entries of either sign. The box tests also include all
   round-2 box probes; the closure tests retain the reviewer's invalid
   pruning probe. All five completed box certificates and all four closure
   certificates, including the repacked legacy certificate, pass. The 56 box
   mutations are rejected and all 14 closure regression checks pass.
   Rerunning the unchanged round-2 probe script rejects every invalid input
   sent to a current verifier. Its historical `HEAD` verifier still accepts
   unsound pruning; that comparison does not test this revision.
2. **N2: derivative numerator.** Theorem 11(c), case (v), now states the
   identity for `N'D − ND'` and explains why `2D(t_K)² > 0`.
   The sign conclusion is unchanged. `verify_wcorner.py` labels the
   numerator correctly and checks both the numerator identity and the exact
   derivative symbolically; all 30 W-corner checks pass.
3. **O1: qualitative factor versus rate.** Corollary 14 now derives
   `ρ_f = ∞` for (B) and (A) from the proved ratio-bound Theorem B(5) and
   Proposition 5. The computer-assisted B2(1) supplies only the explicit
   `411√ε/z_0` rate. Both sibling statements were read; Section 13 now
   limits the computer-assisted dependence to that rate.
4. **O2: section pointer.** The `loop_rank2.py` docstring now points to
   Section 8. The numerical loop was not rerun for this text correction.

All edits are within `orbit-closure/`; review files are unchanged. No commits
or git-state changes were made. The stopped Proposition 16 (B) box search
and BP triangle search were not run. Section 12 records the commands and logs.

## 12. Checks actually run

All commands were run from `orbit-closure/code/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` unless stated. These are targeted
checks only; no project-wide checks were run and CI was not consulted.

| # | Command | Outcome |
|---|---|---|
| 1 | `python3 verify_closure_cert.py ../logs/closure_cert_{thm14_A,prop16_A,wcorner_A_A}.json` | ALL PASS for each (25, 92, 1 pieces); `logs/verify_closure_cert_*.log` |
| 2 | `python3 box_cert.py thm14 B ../logs/boxcert_thm14_B.json --time 3000 --ckpt 60` | complete: 2530 cut, 725 excluded, 20.9 s |
| 3 | `python3 box_cert.py thm14t B ../logs/boxcert_thm14t_B.json --time 3000 --ckpt 60` | complete: 8070 cut, 2253 excluded, 68.6 s |
| 4 | `python3 box_cert.py thm14 BP ../logs/boxcert_thm14_BP.json --bpchart u` and `… thm14t BP … --bpchart u` | complete: 33 cut / 5 skipped; 420 cut / 6 skipped |
| 5 | `python3 box_cert.py thm14w B ../logs/boxcert_thm14w_B.json --time 3000 --ckpt 60` | complete: 5518 cut, 1543 excluded, 39.6 s |
| 6 | `python3 verify_box_cert.py ../logs/boxcert_{thm14_B,thm14t_B,thm14_BP,thm14t_BP,thm14w_B}.json` | ALL PASS for each; `logs/verify_boxcert_*.log` |
| 7 | `python3 test_verify_box_cert.py ../logs/boxcert_thm14_B.json ../logs/boxcert_thm14_BP.json` | 16 of 16 mutations rejected, both originals accepted; `logs/test_verify_box_cert.log`. A first version wrongly expected `e_2` to be an invalid exclusion vector; it is a valid one, and the test was changed to use `e_1` |
| 8 | `python3 box_cert.py prop16 B ../logs/boxcert_prop16_B.json --time 3000 --ckpt 60` | stopped by me after 676 s (margin 0.35%, queue growing); incomplete; checkpoint gzipped |
| 9 | `python3 verify_wcorner.py` | ALL PASS (29 checks) after fixing two errors in the script itself: the set of (d) is `F^T = J^T`, not `J`, and a floating `a_3 = 5.5·10^-13` needed a tolerance; `logs/verify_wcorner.log` |
| 10 | `python3 thm14_factor.py` | ALL PASS: `a_1 ≥ 7/2` identities; exact orbit set with `p_1` recessive and `α_2, α_3 ≥ 367/759`; numerical `inf_BP a_1 = 3.49999995`; `logs/thm14_factor.log` |
| 11 | `python3 bp_lower.py` | PASS: `z_1,BP(1,1,1) ≥ 2539/10000`; `logs/bp_lower.log` |
| 12 | `python3 closure_lower.py` | PASS: exact LP lower bound `≈ 0.9953612 > 0.9839`; `logs/closure_lower_prop16.log` |
| 13 | `python3 aux_facts.py` | first hits `t = (∞, ∞, 6/5)` (thm14), `(∞, ∞, ∞, 2)` (W-corner); SCIP's `R_θ M(s̄)` symmetric PD at all three corners; SCIP bounds `0.0896` (thm14), `0.3177` (prop16, matches sfree's `0.318`) |
| 14 | `python3 /tmp/oc/prop16_exact_copy.py` (an unmodified copy of `../../research-20260928b/reviews/sfree-recheck/prop16_exact.py`, run outside the earlier directory so that nothing there is written) | ALL PASS: bracket `0.9838 ≤ z_1,A ≤ 0.9839` |
| 15 | `python3 factor_scan.py 20 ../logs/factor_scan_thm14.jsonl --time 3000`; `python3 factor_edge.py ../logs/factor_edge_thm14.jsonl` | 291 + 297 directions; max `z_K/z_1,A = 1.1283` |
| 16 | `python3 closure_at.py A 0.55 0.000001 0.45`; same with `B` | `z_cl = 0.2301778` (both), ratio `1.12826`; `logs/closure_at_thm14_*_w2zero.json` |
| 17 | `python3 zk_lower.py` | PASS: exact `min q = 6480592821/4840070400112 > 0` on `T_{649/2500}`; `logs/zk_lower_thm14w.log` |
| 18 | `for i in thm14 bigA prop16 adv8_1 adv8_4 supp1_5512; do python3 loop_rank2.py $i 12 single; done` (900 s limit each) | Section 8 table; `logs/loop_rank2_single_*.jsonl` |
| 19 | `python3 aux_price_check.py`, `aux_price16.py`, `aux_pricew.py`, `aux_factor14.py`, `aux_bp_regions.py` (numerical pricing and closed-form checks; first run from `/tmp`, then rerun from `code/` with logs `logs/aux_*.log`) | margins `1.0047` (thm14t B), `1.0149` (thm14 B), `1.0200` (thm14t BP), `1.0035` (prop16), `1.0100` (thm14w); `inf a_1` over BP `3.5`; closed forms vs `cut_B_fast` max relative difference `3.4·10^-14` |
| 20 | `sha256sum logs/closure_cert_wcorner_BP.log` | `a67b695e…aa41`, as in CLOSEOUT (the file had been gzipped by mistake and was restored) |

Revision checks on 2026-10-03 used
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`.
Commands below are from `code/` unless stated; each certificate in a loop
was checked by a separate invocation. Logs are in
[`logs/revision-r1/`](logs/revision-r1/). These are local targeted checks,
not CI checks. No stopped search was rerun.

| # | Command | Outcome |
|---|---|---|
| 21 | `for cert in thm14_B thm14t_B thm14_BP thm14t_BP thm14w_B; do timeout 180 python3 verify_box_cert.py ../logs/boxcert_$cert.json; done` | All five completed certificates: ALL PASS, exit 0; leaf counts unchanged; `verify_box_*.log` |
| 22 | `for cert in thm14_A prop16_A wcorner_A_A; do timeout 180 python3 verify_closure_cert.py ../logs/closure_cert_$cert.json; done` | All three current certificates: ALL PASS, exit 0; 25, 92, 1 pieces; `verify_closure_*.log` |
| 23 | `timeout 600 python3 test_verify_box_cert.py ../logs/boxcert_thm14_B.json ../logs/boxcert_thm14_BP.json` | Originals accepted; 33 of 33 mutations rejected, exit 0; `test_verify_box.log` |
| 24 | `timeout 180 python3 ../reviews/r1-code/probe_verifier_duplicates.py` | Probe script exit 0; both verifier subprocesses exit 1 (21 failures without duplicates, 33 with duplicates); `probe_verifier_duplicates.log` |
| 25 | `timeout 180 python3 test_verify_closure_cert.py ../logs/closure_cert_prop16_A.json ../logs/closure_cert_wcorner_A_A.json` | Valid outside piece accepted; invalid point and inactive-coordinate pruning rejected; producer guard passes; exit 0; `test_verify_closure.log` |
| 26 | `timeout 1800 python3 closure_lower.py --save ../logs/revision-r1/closure_lower_prop16_cuts.json` | 60 rational cuts saved; exact LP value identical to the original, approximately `0.9953612`; exit 0; `closure_lower_save.log` |
| 27 | `timeout 180 python3 closure_lower.py --verify ../logs/revision-r1/closure_lower_prop16_cuts.json` | All 60 rational sets and steps rechecked; exact LP value and minimizing point match; exit 0; `closure_lower_verify.log` |
| 28 | `timeout 60 python3 check_review_r1.py` | General Lemma 8 identities, Lemma 7 plane criterion, rounded endpoints, table count, B2 rate/domain and result numbering: ALL PASS, exit 0; `check_review_r1.log` |
| 29 | Python conversion of `old_closure_cert_thm14_v1.json` to the current wrapper (asserting its instance and 25 pieces equal `closure_cert_thm14_A.json`), then `timeout 180 python3 verify_closure_cert.py ../logs/revision-r1/closure_cert_thm14_legacy_repacked.json` | Legacy data unchanged; ALL PASS, exit 0; `verify_closure_legacy.log` |
| 30 | `git diff --no-ext-diff --check -- research-20261001/orbit-closure` (from repository root) | Scoped whitespace check passes, exit 0 |
| 31 | `timeout 30 python3` with an inline scan of `/proc/*/cmdline` for Python processes running this stream's computation scripts | No matching computation running; exit 0 |

Round-2 revision checks on 2026-10-03 used
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`.
Commands ran from `code/` unless stated, with at most four concurrent Python
computations. Logs are in [`logs/revision-r2/`](logs/revision-r2/).
These are targeted local checks; no CI checks were run or consulted.
Only completed certificates were replayed; neither stopped search was run.

| # | Command | Outcome |
|---|---|---|
| 32 | `for cert in thm14_B thm14t_B thm14_BP thm14t_BP thm14w_B; do timeout 300 python3 verify_box_cert.py ../logs/boxcert_$cert.json; done` | All five completed box certificates: ALL PASS, exit 0; leaf counts unchanged; `verify_box_*.log` |
| 33 | `for cert in thm14_A prop16_A wcorner_A_A; do timeout 300 python3 verify_closure_cert.py ../logs/closure_cert_$cert.json; done`; `timeout 300 python3 verify_closure_cert.py ../logs/revision-r1/closure_cert_thm14_legacy_repacked.json` | All four closure certificates: ALL PASS, exit 0; 25, 92, 1, 25 pieces, no pruned pieces; `verify_closure_*.log` |
| 34 | `timeout 600 python3 test_verify_box_cert.py ../logs/boxcert_thm14_B.json ../logs/boxcert_thm14_BP.json` | Both originals accepted; 56 of 56 mutations rejected, exit 0. All sign/length mutations exit 1. The unchanged B skip-label mutation rejects by exception (exit 2); `test_verify_box.log` |
| 35 | `timeout 300 python3 test_verify_closure_cert.py ../logs/closure_cert_prop16_A.json ../logs/closure_cert_wcorner_A_A.json` | All 14 regression checks pass, exit 0; includes both originals, sign/length checks, pruning probes and producer guard; `test_verify_closure.log` |
| 36 | `timeout 600 python3 ../reviews/r2-code/probe_r2_verifiers.py` | Script exit 0; original accepted and all 18 invalid current-verifier probes rejected. Only the historical `HEAD` verifier accepts unsound pruning (the script's sole unexpected result); `probe_r2_verifiers.log` |
| 37 | `timeout 900 python3 verify_wcorner.py` | All 30 checks pass, exit 0; numerator identity and exact derivative checked symbolically; `verify_wcorner.log` |
| 38 | `timeout 600 python3 ../reviews/r2-code/indep_math_r2.py`; `timeout 120 python3 check_review_r1.py` | Both ALL PASS, exit 0; reviewer C1b/C1c confirm the corrected algebra, and the round-1 note audit still passes; `indep_math_r2.log`, `check_review_r1.log` |
| 39 | `timeout 900 python3 closure_lower.py --verify ../logs/revision-r1/closure_lower_prop16_cuts.json` | All 60 saved cuts certified; exact LP value and minimizing point unchanged, exit 0; `closure_lower_verify.log` |
| 40 | `timeout 300 python3 ../reviews/r1-code/probe_verifier_duplicates.py` | Script exit 0; false point and doubled-ray point both rejected with verifier exit 1; `probe_verifier_duplicates.log` |
| 41 | `timeout 30 rg -n -A 18 '^\*\*Theorem B\.' ../../ratio-bound/note.md`; `timeout 30 rg -n -A 7 '^\*\*Theorem B2 ' ../../ratio-bound/note.md` | Both exit 0; B(5) gives the qualitative limit and B2(1) gives the computer-assisted rate for every `ε ∈ (0, 1)`; source statements and proofs read; `ratio_bound_statements.log` |
| 42 | `timeout 30 head -n 3 loop_rank2.py` | Exit 0; docstring points to Section 8; `loop_rank2_docstring.log` |
| 43 | `timeout 30 python3` with an inline audit of the round-2 probe log and `/proc/*/cmdline` | Confirms the sole unexpected result is the historical `HEAD` comparison; no stream computation running, exit 0; `final_audit.log` |
| 44 | `timeout 30 git diff --no-ext-diff --check -- research-20261001/orbit-closure` (repository root) | Scoped whitespace check passes, exit 0; `diff_check.log` |

Background processes: every job was started with `timeout` and an internal
time limit; the box certificates checkpoint every 60 s and resume with
`--resume` after decompression if the checkpoint is gzipped. Before returning
I checked that none of this stream's processes were running; none were
(Section 15).

## 13. Limits

- The constant-factor values for (A) and (B) at the Theorem 14 corner
  (`≈ 1.128`) come from grids and floating-point LMI bisection. Only the lower
  bound `1.1166` is certified, and finiteness is not proved.
- The (B) result at the Proposition 16 corner is numerical (incomplete
  certificate). The (B) single-cut values in Section 7 are heuristic lower
  bounds.
- Section 7 has 11 instances, all in direction `(1, 1, 1)`. Section 8 has 6
  instances, one rule, one direction, and the LP is the corner alone.
- Theorem 11(c) uses sfree Lemma 10(4) (exactness of the kept-inequality
  description) only for the equality case. The lower bound
  `a_1 + a_2 ≥ (√2 − 1)/2` uses only Lemma 6(a). Some algebraic steps are
  checked by sympy rather than written out; the sympy checks are part of
  `verify_wcorner.py`.
- Only Corollary 14's explicit rate depends on the ratio-bound note's
  computer-assisted Theorem B2(1) and inherits its review status.
  Its qualitative `ρ_f = ∞` conclusion uses the proved Theorem B(5).
- The infinite factors at the W-corner and at the Theorem 14 corner come from
  rays that never meet `S`. In a solver, bound propagation removes the W-corner
  at once. I did not run SCIP on these corners, and no solver claim is made.
- The P/BP "single equals closure" observation (Section 7) is unexplained.
- Review round 1 exposed a duplicate-ray soundness hole in the original box
  verifier. It did not affect the saved certificates. The revised separate
  verifier passes those certificates and rejects the specified mutations and
  the reviewer's false-certificate probe; round 2 confirmed that fix.
  Round 2 found the missing sign and length checks on `λ̂` in both verifiers.
  These checks are now added, with regressions; no saved certificate was
  affected. This round-2 revision has not been independently re-reviewed;
  its fixes were checked by the coordinating agent.
- Proposition 10 originally did not save its 60 rational cuts. They are now
  saved with exact steps and the LP result in `logs/revision-r1/`; `--verify`
  reproduces the bound without numerical cut generation. This replay is by the
  same author and does not replace a confirming review.

## 14. Open questions

1. Is there a corner and a support-one direction where the closure of (A) or
   (B) is exact while no single cut is? (Corollary 4 rules this out in
   support-two directions.)
2. Is the factor `ρ_B` finite at every corner, or at every corner whose rays
   all meet `S` for some ray subset? At the Theorem 14 corner, are `ρ_A` and
   `ρ_B` finite (numerically `≈ 1.128`)?
3. Why do the point-rule families (P, BP) have closure equal to their best
   single cut in almost every tested direction?
4. Does re-basing (Section 8) always reach `z_K` at one corner in finitely many
   rounds when the reduced costs stay positive? (adv8_1 stalled at zero reduced
   costs.)
5. A second-order (Bernstein) bound in Lemma 15 would certify tight cases such
   as the (B) closure at the Proposition 16 corner (margin `0.35%`).

## 15. Process hygiene

All long computations ran under `timeout` with internal wall-clock limits
(`--time`); the box certificates wrote atomic checkpoints every 60 s and can
resume (`--resume`, after decompression for a gzipped checkpoint). At most
four processes of this stream ran at once. The Proposition 16 (B) certificate was stopped by me (SIGTERM) after 676 s; its
last checkpoint is kept. At the end of the work I checked with
`ps -eo pid,args | grep -E "box_cert|closure_|loop_rank2|factor_|thm14_factor|bp_lower|zk_lower"`
that no process of this stream was running. The check, run on 2026-10-02
after the last computation, found none. The first run's jobs had already been
stopped (CLOSEOUT.md). The 2026-10-03 revision used at most three concurrent
Python computations, each under `timeout`, with `OMP_NUM_THREADS=1`. No search
was resumed. A final process check found no revision computation running.
The round-2 revision also used `OMP_NUM_THREADS=1` and `timeout` for every
computation, with at most four concurrent Python processes. Neither stopped
search was run, and the final process scan found no stream computation running.
