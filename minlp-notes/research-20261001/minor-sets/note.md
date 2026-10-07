# Minor sets: the tangent-edge obstruction for SCIP's outer-product-free sets

Workstream note, research-20261001, stream `minor-sets`. Date: 2026-10-01; revised 2026-10-03
after review round 3 (Section 10). Final status (2026-10-04): reviewed in four rounds;
[round 4](reviews/review-r4.md) verified the r3 fixes; its optional remarks are applied;
the later wording edits are recorded in Section 10.4 and not re-reviewed;
not refereed.
Program: [../PROGRAM.md](../PROGRAM.md). Builds on the
optimal-intersection-cut note
[`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md)
(cited as "sfree"; theorem numbers refer to it). Code in [code/](code/), raw outputs in
[logs/](logs/), sources and manifest in [sources/](sources/). Program files were included in repository commits made outside this program
(e.g. `d91d8d98b`, `f785387a8`, `b59ed1b83`); the program itself makes no commits.
"Reviewed" means checked by another research agent, not journal peer review. Four review rounds
have been done ([reviews/review-r1.md](reviews/review-r1.md),
[reviews/review-r2.md](reviews/review-r2.md) and
[reviews/review-r3.md](reviews/review-r3.md), followed by
[reviews/review-r4.md](reviews/review-r4.md): verified; no major issue).

## Summary

**Question.** The sfree note showed (its Theorem 14) that for a bilinear constraint `w = xy` the
best set of the orbit family, and SCIP's Case-4 completion, can miss the corner bound `z_K`
because of a *tangent edge*. Does the same obstruction occur for the sets SCIP uses for the
implied minor equations `X_{i1j1} X_{i2j2} = X_{i1j2} X_{i2j1}` (homogeneous form of signature
`(2, 2)`; Chmiela–Muñoz–Serrano Case 1; Bienstock–Chen–Muñoz outer-product-free sets)?

**Answer: yes.** The obstruction occurs. Among the certified full-dimensional minor corners,
instances A and S1, the worst instances of the two rational searches (Section 7.4), have larger
gaps than all three certified bilinear instances of the sfree note: orbit ratios about `0.45`
and `0.78` against `0.835`, `0.975` and `0.984`. Instance B, also certified, has orbit ratio
`∈ [0.9219403, 0.9219593]`, between the bilinear values `0.835` and `0.975`; its gap is smaller
than that of the bilinear second rational instance. The 12 rounded adversarial corners and
12 rounded random misses have exact one-sided ratio upper bounds (Section 7);
their lower bounds are numerical. B alone proves exactly that minor gaps are not
uniformly larger than the bilinear gaps. The comparisons use exact brackets: A and S1 come from Theorems 8 and 9,
B from Section 6, and the bilinear values are the sfree family-(A) values, which the
sfree note gives only numerically (it certifies the strict gap exactly) and which this note
brackets exactly through the embedding of Corollary 7. This does not show that minor gaps are
larger in general: the adversarial searches of the two notes impose different non-degeneracy
conditions and are not comparable (Section 7.3), and since every bilinear corner is a
lower-dimensional minor corner (Corollary 7), the worst minor case is at least as bad as the
worst bilinear case anyway. For a minor whose row and column indices `i1, i2, j1, j2` are four
distinct indices (so no entry is diagonal), write the minor as a 2×2 matrix `M` and
`S = {det M = 0}`.

1. *What SCIP uses* (source reading, Section 2). Only `sepa_interminor` builds S-free sets for
   minors. It is off by default (`separating/interminor/freq = -1`) and, even when switched on,
   returns at once unless SCIP is linked with Ipopt, although it never calls Ipopt. The local
   binary (`IPOPT=OFF`) therefore never separates minors; the SCIP 10.0.3 inside PySCIPOpt 6.2.1
   (with Ipopt) does when the separator is enabled. Its set is
   `C_U = {M : sym(U^T M) ⪰ 0}`, where `M̄ = U P` is the polar decomposition of the minor's LP
   value (Proposition 1, proved): this is Bienstock–Chen–Muñoz's set (14a) with their `λ` of
   (17a). On 258 of 258 cuts that SCIP applied in a targeted run, SCIP's cut coincides with the
   intersection cut of `C_U` (largest normalized coefficient difference `4.5·10^-15`;
   computed). By source reading only (not tested), intersection cuts in `nlhdlr_quadratic` (also
   off by default) use the same set for an explicit constraint of this form.
2. *The orbit* (Section 3, proved). Under the automorphisms `M ↦ AMB^T` (and transposition)
   the orbit of SCIP's set is the 3-parameter family `{C_F : det F > 0}`,
   `C_F = {M : sym(F^T M) ⪰ 0}`, of maximal S-free cones. It contains the "point-rule" family
   (SCIP's construction after every change of coordinates; 2 parameters,
   `F^T M̄` symmetric positive definite) and the BCM family (every `λ`; 1 parameter). SCIP's set
   is the unique common member of these two. Unlike the bilinear case there is no completion
   step: the orbit sets are already maximal.
3. *The obstruction occurs* (Section 6). Tangent edges force an orbit set into a one-parameter
   pencil (Lemma 6, proved). On an exact rational, full-dimensional simplicial corner in `R^4`
   (instance A, Theorem 8, certified in exact arithmetic) the corner bound is `z_K = 1`, attained
   only on a tangent edge, and **no orbit set gives more than `9/20`**. Exactly certified
   brackets: orbit `[0.4495347, 0.4495363]`, point rule `[0.1975640, 0.1975643]`, BCM
   `[0.3172917, 0.3172929]`; SCIP's own set gives `0.1358` (50-digit arithmetic). The gap
   persists on a neighbourhood of the data. A second certified corner (instance S1, Theorem 9)
   has a **support-one** minimizer, every edge transversal and strictly positive multipliers,
   and still the orbit gives at most `0.779` (bracket `[0.7780998, 0.7781193]`; SCIP `0.312`).
   Instance B from the tangent-edge search is also certified: orbit
   `[0.9219403, 0.9219593]`, SCIP `0.3250` (Section 6).
   The sfree bilinear counterexamples embed as (lower-dimensional) minor corners (Corollary 7);
   their orbit ratios have exact brackets `[0.9753853, 0.9753864]` (sfree Theorem 14),
   `[0.8347663, 0.8347772]` (its second rational instance) and `[0.9838465, 0.9838468]`
   (its Proposition 16).
4. *Structure* (proved). Consider corner minimizers whose projected rays are linearly
   independent (one always exists). If the LP value of the minor lies in the span of no three
   projected rays, every such minimizer has support at most two, and support two means a tangent
   edge (Proposition 5). Without the independence hypothesis the support bound can fail in
   degenerate cases (duplicated rays). A fixed set such as SCIP's can attain `z_K` only if a
   corner minimizer lies in its 2-dimensional contact cone (Proposition 10). SCIP's choice depends
   on the scaling of the problem variables: rescaling one variable turns a corner where SCIP's
   cut is optimal into one where it gives `2√δ · z_K`, while the point-rule and orbit families,
   which are invariant, stay optimal (Proposition 11).
5. *Numbers* (Section 7; numerical, with exact certificates where stated). On 600 random
   corners with four rays the orbit attains `z_K` in 593 (all 7 misses certified exactly, worst
   ratio `0.775`), the point-rule family in 521, the BCM family in 435, and SCIP's set in 5 (mean
   ratio `0.883`, 10% quantile `0.656`). At 157 McCormick LP vertices of random bipartite
   bilinear programs the orbit attained `z_K` in all, the point-rule family in 152, the BCM
   family in 132, and SCIP's set in 12 (mean ratio 0.922 and 0.931 for the two sizes). An
   adversarial search with all non-degeneracy margins at least 1% drove the orbit ratio to
   `0.200` (ratio bound certified exactly for the rounded corner, which still has all margins at
   least 1%; the multiplier margins are computed numerically, the others exactly); the minimum is
   set by the margin (Section 7.3).
6. *Solver relevance* (Section 7.2; numerical; mostly negative). A better corner bound does not
   by itself give a better LP bound after re-solving. With the orbit set returned by the
   bisection (a max-margin choice among the many optimal sets) the mean fraction of the
   single-minor gap closed was lower than with SCIP's cut (0.70 vs 0.78 and 0.71 vs 0.77; paired
   mean differences `−0.076` and `−0.065`, 95% bootstrap intervals `[−0.117, −0.037]` and
   `[−0.107, −0.025]`). The mean loss is dominated by a minority of corners with large losses:
   the median differences are only `−0.008` and `+0.0005`. For the *typical* corner the loss is
   supported on the 3×3 programs (worse by more than 0.01 in 42 corners, better in 22; sign test
   `p = 0.017`, Wilcoxon signed-rank `p = 0.003`; on 3×3 this rests on the Wilcoxon test,
   with its symmetry caveat, since the adjusted sign test is `0.13`. The Wilcoxon result
   survives Bonferroni over both tests for all eight comparisons, factor 16: `0.049`)
   but not on the 4×4 programs (worse in 33, better in 29;
   sign test `p = 0.70`, Wilcoxon `p = 0.042`, `0.34` adjusted). Choosing instead the optimal
   orbit set nearest to SCIP's set was better than SCIP's cut by more than 0.01 in more corners
   than it was worse (30/16 and 30/10; sign test `p = 0.054` and `0.002`, Wilcoxon `p = 0.001` and
   `0.012`; with factor 16 the 3×3 Wilcoxon and 4×4 sign tests give `0.018` and `0.036`).
   The typical-corner gain on 3×3 rests on Wilcoxon alone, with the symmetry caveat of
   Section 7.2; on 4×4 the sign test supports it. Its *mean* gain is small and not established:
   `+0.022` (interval `[+0.002, +0.045]`) and `+0.006` (interval `[−0.020, +0.029]`, which
   contains 0). So the orbit family is the right *bound* family for minors, and a tie-break toward
   SCIP's set may be worth testing, but this note gives no evidence of a benefit inside SCIP, where
   these cuts are off by default anyway.

**Novelty.** The polar-decomposition description of SCIP's minor set, the orbit and point-rule
families for minors, Lemma 6, Propositions 5, 10, 11 and the certified counterexamples are not in
the sources I read (Section 9). An unsuccessful search does not establish novelty; the search was
small (three web searches; the arXiv API was rate-limited).

---

## 1. Setting and notation

Notation follows the sfree note. An LP vertex `x̄`, simplicial cone `x̄ + R λ`, `λ ≥ 0`, reduced
costs `w > 0`. A minor of the product matrix `X` with rows `i1 ≠ i2` and columns `j1 ≠ j2`, where
`i1, i2, j1, j2` are four distinct indices (so no entry of the minor is diagonal), is written

`M = [[a, b], [c, d]] = [[X_{i1j1}, X_{i1j2}], [X_{i2j1}, X_{i2j2}]]`, coordinates
`s = (a, b, c, d) ∈ R^4`, `det M = ad − bc`.

The minor equation says `M ∈ S := {det = 0}`. The LP value `M̄ = s̄` of the minor has
`det M̄ ≠ 0`; by swapping the columns (as SCIP does) we assume `det M̄ > 0`. The projected rays
are `p_j ∈ R^4` (columns of `P`), the corner set is `X = {λ ≥ 0 : det(s̄ + Pλ) = 0}` and the
corner bound is `z_K(w) = min{w^T λ : λ ∈ X}`. For a closed convex S-free `C ∋ s̄` (interior),
`α_j(C)` is the step length along `p_j` and `z_C(w) = min_j w_j α_j(C)` is its one-cut bound
(sfree §1). By sfree Theorem 1, `sup_C z_C(w) = z_K(w)` over all S-free sets.

`T_z = conv{s̄, s̄ + (z/w_j) p_j : j}` is the simplex of level `z`, `T* = T_{z_K}`. For a 2×2 matrix
`N`, `sym(N) = (N + N^T)/2`; `J = [[0, 1], [−1, 0]]`; `adj(N) = [[n22, −n12], [−n21, n11]]`.
The polar form of `det` is `B(X, Y) = ½ tr(adj(X) Y)`, so `det X = B(X, X)` and
`∇det(X)·Y = 2B(X, Y) = tr(adj(X) Y)`; in coordinates `∇det(s) = (d, −c, −b, a)`.

For four distinct indices the minor is the projection of the set of outer products: the map
`x ↦ (x_{i1}x_{j1}, x_{i1}x_{j2}, x_{i2}x_{j1}, x_{i2}x_{j2})` has image `{u v^T}`, all 2×2
matrices of rank at most one, i.e. exactly `S`. So the minor sets of Bienstock–Chen–Muñoz that
depend only on these four entries are the S-free sets studied here.

## 2. What SCIP 10.0.3 does with minors

Read in `scip/src/scip/sepa_interminor.c`, `sepa_minor.c` and `nlhdlr_quadratic.c` of the SCIP
10.0.3 source (read only; checksums in [sources/MANIFEST.md](sources/MANIFEST.md)).

- **`sepa_interminor`** ("intersection cuts separator to ensure that 2x2 minors of X (= xx')
  have determinant 0") is the only place where SCIP builds S-free sets for minors.
  - *When.* `SEPA_FREQ = -1`: off by default. If enabled, `sepaExeclpMinor` first checks
    `SCIPisIpoptAvailableIpopt()` and returns otherwise ("need routine to compute
    eigenvalues/eigenvectors"), although the eigenvectors are hard-coded and Ipopt is never
    called. Rounds: `maxroundsroot = -1` (unlimited at the root), `maxrounds = 10` per node.
  - *Which minors.* `detectMinors` builds a sparse matrix whose rows and columns are the
    variables `x_i` that have an auxiliary variable for some product `x_i x_k` (product
    expressions with two children, and squares). For every pair of rows `i < j` and every pair of
    shared columns `k < l` it stores the minor `(X_ik, X_il, X_jk, X_jl)`, at most 100000 minors.
    Since the matrix is symmetric each non-principal minor is stored twice (rows/columns
    exchanged; a `TODO` comment says so); both copies give the same set (the polar factor of
    `M̄^T` is `U^T`, and `{M : sym(U^T M) ⪰ 0}` is invariant under this exchange), so the second
    cut is a duplicate. Principal minors (`{i, j} = {k, l}`, where `X_il = X_jk`) and minors with
    one diagonal entry are included.
  - *Which LP points.* Every stored minor with `|det| > feastol` at the LP solution. If
    `det < 0` the columns are swapped.
  - *Which set.* `computeRestrictionToRay` uses the eigen-decomposition of `ad − bc`
    (eigenvalues `±½`, fixed eigenvectors) and the Chmiela et al. Case-1 set
    `{‖ŷ(z)‖ ≤ x̂(z̄)^T x̂(z)/‖x̂(z̄)‖}` with `x̂(M) = ((a+d)/2, (c−b)/2)`,
    `ŷ(M) = ((d−a)/2, (b+c)/2)` (`usebounds = FALSE`, the default). The step length is the
    smallest positive root of a quadratic, corrected by a bisection when the root is slightly
    infeasible. The cut `Σ_j λ_j/α_j ≥ 1` runs over all nonbasic columns and rows. Options, both
    off by default: `usestrengthening` (negative coefficients for rays in the recession cone) and
    `usebounds` (a Case-4-type set that also uses `X_ii ≥ 0` when a diagonal entry of the minor
    has a *negative* LP value). Minimum violation `mincutviol = 10^-4`.
- **`nlhdlr_quadratic`** (intersection cuts off by default: `useintersectioncuts = FALSE`)
  treats a quadratic constraint written explicitly in the model. *Source reading, not tested:* a
  constraint `x_1 x_4 − x_2 x_3 = 0` is a constraint root, which has no auxiliary variable
  (`auxvar = NULL`), so it falls into Case 1 (`w = 0`, `κ = 0`), whose set is the same formula
  with eigenvectors from LAPACK; the set does not depend on the choice of eigenvectors inside an
  eigenspace, so it is again `C_U`. No run checked that `nlhdlr_quadratic` actually produces these
  cuts; the fidelity check below covers `sepa_interminor` only.
- **`sepa_minor`** (on by default, `freq = 10`) is different: for principal minors it adds the
  linear eigenvector cuts `v^T [[1, x, y], [x, xx, xy], [y, xy, yy]] v ≥ 0`. These are not
  intersection cuts and are not studied here.

Checked behaviour (`code/scip_probe.py`, [logs/scip_probe.log](logs/scip_probe.log)): on a 3×3
bipartite bilinear model, default settings give 0 `interminor` calls; with
`separating/interminor/freq = 0`, PySCIPOpt's SCIP (which lists Ipopt 3.14.19 among its external
libraries) calls it once, finds 8 cuts and applies 1; the local binary with the same setting
makes 0 calls (it lists no Ipopt).

**Proposition 1 (SCIP's minor set).** Let `det M̄ > 0` and let `M̄ = U P` be the polar
decomposition (`U ∈ SO(2)`, `P` symmetric positive definite). The Case-1 set
`{‖ŷ(M)‖ ≤ x̂(M̄)^T x̂(M)/‖x̂(M̄)‖}` that `sepa_interminor` builds (formula as transcribed above
from the source) is

`C_U = {M : sym(U^T M) ⪰ 0}`.

It equals Bienstock–Chen–Muñoz's set (14a), `λ_1(a+d) + λ_2(b−c) ≥ ‖(b+c, a−d)‖`, with their
choice (17a) `λ ∝ (ā + d̄, b̄ − c̄)`. If `det M̄ < 0`, SCIP's column swap gives
`{M : sym(W^T M) ⪰ 0}` with `W` the orthogonal polar factor of `M̄` (a reflection).

*Scope of "proved".* The proof below is a proof about this formula. That `sepa_interminor`
implements it rests on source reading and is confirmed by the fidelity check that follows. That
`nlhdlr_quadratic` Case 1 uses the same set for an explicit constraint `x_1x_4 − x_2x_3 = 0` rests
on source reading only and was not tested.

*Proof.* Write `M = x_1 I + x_2 J' + y_1 K + y_2 L` with `J' = [[0, −1], [1, 0]]`,
`K = [[−1, 0], [0, 1]]`, `L = [[0, 1], [1, 0]]`. Then `a = x_1 − y_1`, `b = y_2 − x_2`,
`c = x_2 + y_2`, `d = x_1 + y_1`, so `x̂(M) = (x_1, x_2)`, `ŷ(M) = (y_1, y_2)` and
`det M = ‖x̂‖² − ‖ŷ‖²`. A symmetric 2×2 matrix `N` is PSD iff
`(n_11 + n_22)/2 ≥ ‖((n_11 − n_22)/2, n_12)‖`; for any `N`, `sym(N) ⪰ 0` iff
`x_1(N) ≥ ‖ŷ(N)‖`. Left multiplication by the rotation `R_φ = cos φ I + sin φ J'` maps
`span{I, J'}` and `span{K, L}` to themselves (`J'K = −L`, `J'L = K`) and is an isometry on each,
and `x_1(R_φ^T M) = cos φ x_1(M) + sin φ x_2(M)` (use `J'^2 = −I`). Hence
`C_{R_φ} = {M : (cos φ, sin φ)·x̂(M) ≥ ‖ŷ(M)‖}`, which is SCIP's set for
`(cos φ, sin φ) = x̂(M̄)/‖x̂(M̄)‖`. For this `φ` the `J'`-coordinate of `R_φ^T M̄` is
`cos φ x_2(M̄) − sin φ x_1(M̄) = 0`, so `R_φ^T M̄` is symmetric, with trace `2‖x̂(M̄)‖ > 0` and
determinant `det M̄ > 0`, hence positive definite. By uniqueness of the polar decomposition of an
invertible matrix, `R_φ = U`. BCM's (14a) reads `λ_1 x_1 − λ_2 x_2 ≥ ‖ŷ‖` in these coordinates,
and (17a) gives `(λ_1, −λ_2) ∝ (x_1(M̄), x_2(M̄))`: the same set. For `det M̄ < 0` write
`M̄ = W P` (`W` a reflection), let `Π` swap the columns; then `M̄Π = (WΠ)(Π^T P Π)` is the polar
decomposition of the swapped matrix, and SCIP's set
`{MΠ : sym((WΠ)^T MΠ) ⪰ 0} = {M : sym(W^T M) ⪰ 0}Π`. ∎

*Fidelity check (computed).* `code/scip_fidelity.py` builds random bipartite bilinear models,
switches off all other separators, enables `interminor` at the root, and inserts a Python
separator with priority +1 that records the LP basis and the tableau rows of the minor variables
before `interminor` runs in the same round. From that record it predicts the cut of every
violated minor with the step lengths of `C_U` (`minor_core.step`), assembled in the original
variables exactly as `addColToCut`/`addRowToCut` do, and compares with the LP rows that
`interminor` added (empty name, origin `SEPA`), after normalization. Result: 40 models of size
3×3 and 20 of size 4×4, 258 applied cuts in 273 separation rounds, **258 matched**; largest
difference of normalized coefficients `4.0·10^-15` (3×3) and `4.5·10^-15` (4×4)
([logs/scip_fidelity_3x3.log](logs/scip_fidelity_3x3.log),
[logs/scip_fidelity_4x4.log](logs/scip_fidelity_4x4.log)). In 21 models no separation round took
place (the recorder was never called) and they were skipped. The literal transcription of SCIP's
step-length formula (`minor_core.scip_interminor_step`) agrees with `C_U` to `1.4·10^-13` on 1709
random rays ([logs/test_core.log](logs/test_core.log)).

## 3. S-free sets of a minor and the orbit

**Lemma 2 (S-free sets of a minor).** Let `det M̄ > 0` and `S_≤ = {det ≤ 0}`.

1. For a closed convex `C` with `M̄ ∈ int C`: `C` is S-free ⟺ `C ⊆ {det ≥ 0}` ⟺ `C` is
   `S_≤`-free.
2. Every maximal S-free set with `M̄` in its interior is a closed convex cone.
3. For `w > 0`, the corner bounds for `S` and for `S_≤` coincide.

So the maximal S-free sets of a minor are the maximal homogeneous quadratic-free sets of
Muñoz–Paat–Serrano for the form `det` (signature `(2, 2)`), described by their Theorems 1.1–1.2
as the sets `C_Γ` with `Γ : S^1 → S^1` non-expansive and a convexity condition: an
infinite-dimensional family.

*Proof.* (1) `int C` is convex, hence connected, and `det` is continuous and nonzero on it, so
`det > 0` on `int C` and `C = cl int C ⊆ {det ≥ 0}`. Conversely, `int{det ≥ 0} = {det > 0}`: if
`det M = 0` and `M ≠ 0` then `adj M ≠ 0`; choose `E` with `tr(adj(M)E) < 0`, then
`det(M + εE) = ε tr(adj(M)E) + ε² det E < 0` for small `ε > 0`; if `M = 0` use
`E = diag(1, −1)`. So `C ⊆ {det ≥ 0}` gives `int C ⊆ {det > 0}`, which misses `S` and `S_≤`.
(2) As in Bienstock–Chen–Muñoz, Theorem 15 and Corollary 16 (their `S` is also a cone): if `C` is
S-free and full-dimensional, `K = cl cone(C)` is S-free, because a point `X ∈ int K ∩ S` with
`X ≠ 0` spans a ray inside `S` that is interior to `cone(C)` and hence meets `int C` (their
Lemma 14), and `0 ∈ int K` would give `K = R^4` and such an `X`. By maximality `C = K`.
(3) `S ⊆ S_≤` gives one inequality. If `det(s̄ + Pλ) < 0`, then `τ ↦ det(s̄ + τPλ)` changes sign
on `(0, 1)`, which gives a point of `S` with cost `τ w^T λ < w^T λ`. ∎

**Proposition 3 (orbit and subfamilies).** Let `G_+` be the group of maps `M ↦ AMB^T` and
`M ↦ AM^T B^T` with `A, B ∈ GL_2`, `det A det B > 0`. These maps preserve `S` and `{det > 0}`.

1. For `det F > 0`, `C_F = {M : sym(F^T M) ⪰ 0}` is a maximal S-free closed convex cone, and
   `C_F = C_{F'}` iff `F' = cF` with `c > 0`. The `G_+`-orbit of SCIP's set (of any `C_U`) is
   `{C_F : det F > 0}`, a 3-parameter family.
2. `g(M) = AMB^T` maps `C_F` to `C_{F'}` with `F'^T = B F^T A^{-1}`; transposition maps `C_F` to
   `C_{F^{-1}}`.
3. *(Point rule under all automorphisms.)* The sets obtained by applying SCIP's construction in
   transformed coordinates, `{g^{-1}(C_{U(g M̄)}) : g ∈ G_+}`, are exactly
   `PR(M̄) = {C_F : F^T M̄ symmetric positive definite}`, a 2-parameter family. `PR` is
   equivariant: `g(PR(M̄)) = PR(g M̄)`.
4. *(BCM family.)* `{C_λ : ‖λ‖ = 1} = {C_R : R ∈ SO(2)}` (BCM (14a) for every `λ`), a
   1-parameter family; `{C_R} ∩ PR(M̄) = {C_U}`.
5. Each family is `{C_F : F^T ∈ L, sym(F^T M̄) ≻ 0}` for a linear space `L`: `R^{2×2}` (orbit),
   `{G : G M̄ symmetric}` (point rule), `span{I, J}` (BCM), `R·U^T` (SCIP).

*Proof.* (2) For `N = AMB^T`: `sym(F^T A^{-1} N B^{-T}) ⪰ 0` iff
`v^T F^T A^{-1} N B^{-T} v ≥ 0` for all `v`; with `u = B^{-T} v` this is
`sym(B F^T A^{-1} N) ⪰ 0`. For transposition, `M^T ∈ C_F` iff `v^T M F v ≥ 0` for all `v`; with
`u = Fv`, iff `sym(F^{-T} M) ⪰ 0`.
(1) `C_I = {sym(M) ⪰ 0} = C_λ` with `λ = (1, 0)` (Proposition 1), maximal S-free by Muñoz–Serrano,
"Maximal quadratic-free sets", Math. Program. 192 (2022), Theorem 2.1 as cited by Muñoz–Paat–Serrano
(Theorem 7 of the arXiv version 1911.12341v2, for `{‖x̂‖ ≤ ‖ŷ‖}`-free sets, which suffices by
Lemma 2(1)); also BCM Theorem 23(iv). Elements of `G_+` map maximal
S-free sets to maximal S-free sets. By (2), the orbit of `C_I` is `{C_F : F^T = BA^{-1}}`, i.e.
all `C_F` with `det F > 0` (take `A = aI`, `B = aF^T`, `a > 0`); transposition fixes `C_I`. This is
sfree Lemma 10(2) with positive scalings added, which do not change the cones. `C_U` is in the
orbit, so the orbits coincide. For equality: `⟨FY, M⟩ = ⟨Y, sym(F^T M)⟩` shows
`C_F = (F·PSD)^*` and `C_F^* = F·PSD`; `F·PSD = F'·PSD` forces `G = F^{-1}F'` to map symmetric
matrices to symmetric matrices, so `G = cI`, and `c > 0` since PSD is pointed.
(3) Let `M̄' = g(M̄) = A M̄ B^T` with polar factors `U', P'`. By (2), `g^{-1}(C_{U'}) = C_F` with
`F^T = B^{-1} U'^T A`, and `F^T M̄ = B^{-1} U'^T (A M̄ B^T) B^{-T} = B^{-1} P' B^{-T}`, symmetric
positive definite. Conversely, if `F^T M̄ = P ≻ 0`, take `g(M) = F^T M` (`A = F^T`, `B = I`):
`g(M̄) = P` has polar factor `I`, SCIP's set there is `C_I`, and `g^{-1}(C_I) = C_F`. Transposition
maps `PR(M̄)` to `PR(M̄^T)` (`F^{-T} M̄^T = F^{-T} P F^{-1}`). Equivariance:
`F'^T g(M̄) = B (F^T M̄) B^T` is a congruence. The family is `{P M̄^{-1} : P ≻ 0}` modulo scaling.
(4) By the proof of Proposition 1, `C_{R_φ} = C_λ` with `λ = (cos φ, sin φ)`. A rotation-scaling
`ρR` with `ρ R^T M̄` symmetric positive definite must have `R = ±U` by uniqueness of the polar
decomposition, and both signs give `C_U`.
(5) Restatement of (1), (3), (4) (`span{I, J}` is the set of rotation-scalings). ∎

So SCIP's set has two descriptions: the member of BCM's family selected by the point rule, and the
member of the point-rule family selected by the Euclidean structure of the four minor variables.
The latter is not invariant under `G_+`, for instance under rescaling a problem variable
(Proposition 11).

**Proposition 4 (best set of each family; certificates).** For a family with space `L` and
`z ≥ 0`, `Φ_L(z) = {F^T ∈ L : sym(F^T M̄) ≻ 0, sym(F^T V) ⪰ 0 for every vertex V of T_z}` is a
convex cone that shrinks as `z` grows, and `z_C(w) ≥ z` iff `F^T ∈ Φ_L(z)`. Hence the best
one-cut bound of the family is found by bisection over `z`, each step an SDP with `N + 1` blocks
of size 2 in `dim L ≤ 4` variables. If there are positive definite `Y_V` (one per vertex of `T_z`,
including `s̄`) with `Σ_V tr(G V Y_V) = 0` for every `G` in a basis of `L`, then `Φ_L(z) = ∅`, so
the family's best bound is at most `z`.

*Proof.* `T_z ⊆ C_F` iff its vertices are in `C_F`, which are linear matrix inequalities in `F`.
For `z' < z` the vertices of `T_{z'}` are convex combinations of `s̄` and those of `T_z`. If
`F^T ∈ Φ_L(z)` and the `Y_V` exist, then
`0 = Σ_V tr(F^T V Y_V) = Σ_V ⟨sym(F^T V), Y_V⟩ ≥ ⟨sym(F^T M̄), Y_{M̄}⟩ > 0`, a contradiction. ∎

The certificates of Section 6 are of this form, with rational `Y_V` and exactly checked positive
definiteness; the lower bounds come from explicit rational `F` whose sets contain `T_z`, checked
exactly. Numerically (`code/minor_core.py`) each bisection step solves the always-feasible problem
`max t` s.t. `sym(F^T M̄) ⪰ I`, `sym(F^T V) ⪰ tI`, `t ≤ 1`; the reported value is always the exact
one-cut bound of an explicit `F`, so it is a valid lower bound up to floating point. The scripts
also print a "bisection upper" value (the smallest tested `z` at which the numerical SDP was
judged infeasible). It is not a bound: solver tolerances can put it slightly below the lower value of
an explicit set (instance A: bisection value `0.4495353`, while an explicit set gives
`0.4495357`). Only the exact certificates give upper bounds. The orbit and
point-rule computations are done after the automorphism `M ↦ M̄^{-1} M` (Proposition 3(2) and
equivariance), which maps `s̄` to `I`; the BCM family is computed by a scan over `φ` (7200 grid
points and golden-section refinement).

## 4. Corner minimizers of a minor

**Proposition 5 (support).** Let `S = {det = 0} ⊂ R^4`, `det s̄ > 0`, `w > 0`, and let `λ*` be a
corner minimizer whose support `J` has `P_J` injective (one exists, sfree Lemma 3).

1. `|J| ≤ 3`, and `|J| = 3` only if `s̄ ∈ span{p_j : j ∈ J}`. So if `s̄` lies in the span of no
   three rays, `|J| ≤ 2`.
2. If `|J| = 2`, the minimizer `t*` lies in the relative interior of an edge of `T*` that is
   tangent to the null cone at `t*` (`∇det(t*)·d = 0` for the edge direction `d`), and
   `det d ≥ 0`.

*Proof.* (1) sfree Theorem 4 gives `|J| ≤ ρ = n_+ + n_0 + 1 = 3`. Suppose `|J| = 3`. If
`P_J^T ∇det(t*) = 0`, the second case of that proof gives `det ⪰ 0` on the 3-dimensional space
`span P_J`, impossible for signature `(2, 2)` (the largest PSD subspace has dimension 2). So the
first case holds: `∇det(t*) ≠ 0` (hence `t* ≠ 0`), and `det ⪰ 0` on `V = P_J{δ : w_J^T δ = 0}`,
a 2-dimensional subspace of `T = {v : B(t*, v) = 0}`. Since `det t* = 0`, `t* ∈ T`. Pick `u` with
`B(t*, u) = 1`; `H = span{t*, u}` has signature `(1, 1)`, so `H^⊥` has signature `(1, 1)`, and
`T = span{t*} ⊕ H^⊥`: the form restricted to `T` has radical `span{t*}` and signature `(1, 1)`
modulo it. If `t* ∉ V`, `V` would map injectively onto a 2-dimensional PSD subspace of a form of
signature `(1, 1)`, impossible. So `t* ∈ V`. The face of `T*` containing `t*` has affine hull
`{s̄ + P_J μ : w_J^T μ = z_K}` with direction space `V`; it contains `t*`, hence also
`t* − t* = 0`, so `s̄ = −P_J μ` for some `μ`.
(2) With LICQ, the KKT condition `w_J = −σ P_J^T ∇det(t*)` gives
`∇det(t*)·(p_i/w_i − p_j/w_j) = 0`, and the edge of `T*` through `t*` has direction
`z_K (p_i/w_i − p_j/w_j)`; without LICQ both products are zero. Along the edge,
`det(t* + s d) = s² det d` (as `det t* = 0` and `∇det(t*)·d = 0`), and `det ≥ 0` on `T*`. ∎

This sharpens sfree Theorem 4 for minors: `ρ = 3` is reached only for corners with `s̄` in the span
of three rays. The injectivity hypothesis matters for other minimizers. If a tangent-edge corner
with minimizer support `{1, 2}` gets a duplicate ray `p_3 = p_1`, `w_3 = w_1`, then
`(λ*_1/2) e_1 + λ*_2 e_2 + (λ*_1/2) e_3` is a minimizer with three rays in its support, while for
generic data `s̄` still lies in the span of no three rays (example from the review). Proposition 5
says nothing about such minimizers; it applies to the minimizer with independent projected rays
that always exists.

In the random corners of Section 7.1 (900 corners) supports were 1 or 2 only, and
every support-2 minimizer was on a tangent edge (`|cos| < 10^-6`), as Proposition 5(2) requires.

## 5. Tangent edges are rigid

**Lemma 6 (homogeneous tangent-edge pencil).** Let `M_0 = a_0 b_0^T ≠ 0`, and let `D` satisfy
`tr(adj(M_0) D) = 0` (tangent at `M_0`) and `det D > 0`. Put `G_0 = J adj(D)`,
`G_1 = J adj(M_0)`. Then `G_1 a_0 = 0`, `G_1 M_0 = 0`, `G_0 a_0 = c_0 b_0` with `c_0 ≠ 0`, and
`det(G_0 + κG_1) = det D` for all `κ`. If `F` is invertible and `C_F` contains the segment
`{M_0 + sD : |s| ≤ ε}` for some `ε > 0`, then

`F^T = θ (G_0 + κ G_1)` for some `κ ∈ R` and some `θ` with `θ c_0 > 0`.

*Proof.* For 2×2 matrices, `adj(ab^T) = (Jb)(Ja)^T` and `adj(D) = J^T D^T J`. Hence
`G_1 a_0 = J(Jb_0)(Ja_0)^T a_0 = 0`, `G_1 M_0 = 0`, and
`(Jb_0)^T G_0 a_0 = b_0^T adj(D) a_0 = (Ja_0)^T D (Jb_0) = tr(adj(M_0) D) = 0`, so
`G_0 a_0 ∥ b_0`; `G_0` is invertible, so `c_0 ≠ 0`. `det(D + κM_0) = det D + κ tr(adj(M_0)D)
+ κ² det M_0 = det D` and `J adj(D + κM_0) = G_0 + κG_1` (adj is linear on 2×2 matrices).
Now let `F` be as stated. `M_0 ∈ C_F` gives `sym((F^T a_0) b_0^T) ⪰ 0`, so `F^T a_0 = c b_0` with
`c ≥ 0` (a matrix `sym(r b^T)` with `r ∉ R b` is indefinite), and `c > 0` as `F` is invertible.
Put `Y = sym(F^T D)`, `X(s) = c b_0 b_0^T + sY ⪰ 0` for `|s| ≤ ε`, and `u = Jb_0 ⊥ b_0`. From
`u^T X(s) u = s u^T Y u ≥ 0` for `s = ±ε`, `u^T Y u = 0`; then `X(s)u = 0` (PSD with a zero
diagonal value in direction `u`), so `Yu = 0` and `Y = μ b_0 b_0^T`. Hence
`sym(F^T(D + κM_0)) = 0` with `κ = −μ/c`, i.e. `F^T (D + κM_0) = θ' J`. As `D + κM_0` is
invertible (determinant `det D`), `F^T = θ' J (D + κM_0)^{-1} = (θ'/det D)(G_0 + κG_1)`, and
`c b_0 = F^T a_0 = (θ'/det D) c_0 b_0` fixes the sign. ∎

This is the homogeneous version of sfree Lemma 13 (family (A) part; there is no completion
here). Each further vertex `V` of `T*` restricts `κ` to the interval
`K(V) = {κ : sym((G_0 + κG_1)V) ⪰ 0}` (sign of `θ` absorbed in `G_0, G_1`); if the intervals of
the vertices have empty intersection, no orbit set contains `T*`.

## 6. The obstruction

**Corollary 7 (the bilinear counterexamples are minor counterexamples).** Map a bilinear corner of
the sfree note (`S = {w ≤ xy}`, apex `s̄ = (x̄, ȳ, w̄)`, rays `p_j ∈ R^3`) to the minor corner with
apex `(w̄, x̄, ȳ, 1)` and rays `(p_{j,w}, p_{j,x}, p_{j,y}, 0)`, i.e. `M = [[w, x], [y, h]]`. Then
the minor corner bound equals the bilinear one, and the best orbit bound equals the bilinear
family-(A) bound `z_A`. Hence sfree Theorem 14 (`z_A = 0.97539`), its second rational instance
(`0.83477`) and Proposition 16 (support one, `0.98385`) are minor corners on which the orbit misses
`z_K`. These corners are not full-dimensional (three rays in the hyperplane `h = 0`).

*Proof.* `det M(s, 1) = w − xy`, so the corner sets agree (Lemma 2(3) for `≤` versus `=`). The
corner lies in `H = {h = 1}`, and the step lengths of `C_F` along rays in `H` from a point of `H`
are those of `C_F ∩ H`, the sfree family (A). ∎

Computed check: `code/embed_check.py` gives `0.97539`, `0.83477`, `0.98385` with this stream's code
([logs/embed_check.log](logs/embed_check.log)). The sfree note gives these values numerically and
certifies only the strict gap `z_A < z_K`. `code/certify_embed_brackets.py`
([logs/certify_embed_brackets.log](logs/certify_embed_brackets.log), ALL PASS; added in the
round-2 revision) brackets them exactly on the embedded corners, with the same two certificates
as in Theorem 8 (an explicit rational `F` whose set contains `T_{z_lo}`, and rational positive
definite `Y_V` as in Proposition 4 at `z_up`), after checking exactly that `det` has minimum 0
on `T*`, attained only at `t*`, so `z_K = 1`. The brackets, computed exactly, are
`[0.9753853, 0.9753864]` (Theorem 14), `[0.8347663, 0.8347772]` (second rational instance) and
`[0.9838465, 0.9838468]` (Proposition 16). By Corollary 7 they are also exact brackets of the
sfree family-(A) values.

**Theorem 8 (full-dimensional tangent-edge counterexample).** Let `w = (1, 1, 1, 1)` and, in
coordinates `(a, b, c, d)`,

`s̄ = (0, 5/2, −1/2, −1/2)`, `v_1 = (−5, 3, 4, −4)`, `v_2 = (−8, 12, −8, 8)`,
`v_3 = (−3/2, −4, 2, −7/2)`, `v_4 = (−7/2, −1/2, 3/2, −4)`, rays `p_j = v_j − s̄`

("instance A"). Then:

1. The cone is simplicial and full-dimensional (`det[p_1 … p_4] = −2775/4`), `det s̄ = 5/4`, and
   `z_K = 1`, attained only at `t* = (−6, 6, 0, 0) = (2/3)v_1 + (1/3)v_2`, on the tangent edge
   `[v_1, v_2]` (`d = v_1 − v_2 = (3, −9, 12, −12)`, `∇det(t*)·d = 0`, `det d = 72`). KKT:
   `σ = 1/6`, multipliers `(0, 0, 3/2, 5/2)`; `∇det(t*)·s̄ = 6 > 0`, so by sfree Theorem 1(4)
   some maximal S-free set attains `z_K = 1`.
2. No orbit set contains `T*`. In the pencil of Lemma 6 (`G_0 = [[−12, 3], [12, −9]]`,
   `G_1 = [[0, −6], [0, 6]]`) the `κ`-intervals are `K(s̄) = [6 − √10, 6 + √10]`,
   `K(v_1) = (−∞, 3]`, `K(v_2) = [−3/2, ∞)`,
   `K(v_3) = [−49/6 − 2√106/3, −49/6 + 2√106/3] ≈ [−15.03, −1.30]`,
   `K(v_4) = [−33/10 − 2√118/5, −33/10 + 2√118/5] ≈ [−7.65, 1.05]`; `K(s̄)` is disjoint from
   `K(v_3)` and from `K(v_4)`.
3. `z_orbit ≤ 9/20`: rational positive definite `Y_V` on the vertices of `T_{9/20}` satisfy the
   equations of Proposition 4. With explicit rational sets on the other side, the best bounds of
   the families satisfy (exactly) orbit `∈ [0.4495347, 0.4495363]`, point rule
   `∈ [0.1975640, 0.1975643]`, BCM `∈ [0.3172917, 0.3172929]`, while SCIP's set `C_U` gives
   `0.1358003` (step lengths `0.1358, ∞, 0.1949, 0.3478`; 50-digit arithmetic, numerical).
4. *(Robustness.)* There is a neighbourhood of `(s̄, P, w)` on which `z_orbit ≤ 9/20 < z_K`.

*Proof.* (1)–(3) are checked in exact rational arithmetic by `code/certify_cex.py`
([logs/certify_cex_A.log](logs/certify_cex_A.log), ALL PASS): the minimum of `det` over `T*` is
found by enumerating the 31 faces and solving each face's KKT system exactly (singular faces are
skipped; their minima are attained on lower faces), giving `0` only at `t*`; then
`det > 0` on `T* \ {t*}`, every point of the corner with cost `≤ 1` lies in `T*`, and `z_K = 1`
with the unique minimizer `t*`. The `κ`-intervals are computed with exact algebraic endpoints.
A positive definite certificate at `z = 1` with small denominators is also printed:
`Y_{s̄} = [[237/250, 133/500], [133/500, 57/500]]`, `Y_{v_1} = [[453/1000, 7/20], [7/20, 29/100]]`,
`Y_{v_2} = [[9/100, 11/100], [11/100, 17/100]]`, `Y_{v_3} = [[1/100, 0], [0, 7/50]]`,
`Y_{v_4} = [[1/100, 0], [0, 1/100]]` with `Σ_V V Y_V = 0`; each `Y_V` has positive diagonal and
determinant, which can be checked by hand.
(4) The certificate at `z = 9/20` consists of positive definite `Y_V` solving 4 linear equations
whose coefficient matrix has full row rank 4 (checked exactly) and depends continuously on the
data; for nearby data the projection of `Y` onto the new solution space is still positive
definite, so `z_orbit ≤ 9/20` there (Proposition 4; `T_{9/20}` moves continuously). The corner
bound is continuous at the data: moving slightly beyond `t*` along ray 1 gives `det < 0`
(`∇det(t*)·p_1 = −1/σ < 0`), which survives small perturbations, so `z_K` cannot jump up; and a
sequence of perturbed data with `z_K ≤ 1 − η` would have bounded minimizers converging to a point
of cost `≤ 1 − η` with `det ≤ 0`, contradicting `z_K = 1`. ∎

A second rational instance from the same search ("instance B", [logs/certify_cex_B.log](logs/certify_cex_B.log),
ALL PASS) has orbit `∈ [0.9219403, 0.9219593]` (`z_orbit ≤ 461/500`), point rule
`∈ [0.3634909, 0.3634912]`, BCM `∈ [0.6528369, 0.6528387]`, SCIP `0.3250`. Its data:
`s̄ = (−3, −5/2, 1/2, −2)`, `v_1 = (1, 1, −7, −4)`, `v_2 = (−1/2, −1/2, −11/2, −7)`,
`v_3 = (1/2, 1, −5/2, 0)`, `v_4 = (−7/2, 4, −7/2, 2)`, `t* = (0, 0, −6, −6)`, `w = 1`.

**Theorem 9 (support one is not enough).** Let `w = (1, 1, 1, 1)` and

`s̄ = (−4, −1, −1/2, −2)`, `v_1 = t* = (3, 3, −3, −3)`, `v_2 = (95/24, 4, −4, −4)`,
`v_3 = (17/3, 6, −3/2, −3/2)`, `v_4 = (41/6, 3, −6, −2)`

("instance S1"). Then `det s̄ = 15/2`, the cone is full-dimensional (`det P = 533/16`), `z_K = 1`
is attained only at the vertex `t* = v_1` (support one), the multipliers of rays 2–4 are
`1/36, 2/9, 1/9 > 0`, and every edge of `T*` at `t*` is transversal:
`∇det(t*)·(v − t*) = 9/2, 1/8, 1, 1/2` for `v = s̄, v_2, v_3, v_4` (cosines with the normal
`0.088, 0.011, 0.037, 0.017`). No orbit set contains `T*`, `z_orbit ≤ 779/1000`, and exactly
orbit `∈ [0.7780998, 0.7781193]`, point rule `∈ [0.4542877, 0.4542880]`, BCM
`∈ [0.4855239, 0.4855241]`; SCIP's set gives `0.3121418` (numerical).

*Proof.* `code/certify_supp1_full.py` ([logs/certify_supp1_full.log](logs/certify_supp1_full.log),
ALL PASS), with the same exact checks as for Theorem 8; the certificate at `z = 1` has
`Y_V` with denominators up to `216000`. ∎

As in sfree Proposition 16, the edges at `t*` are nearly tangent (cosines `0.011`–`0.088`); the
gap is larger here (orbit at most `0.7781193` against at least `0.9838465` for sfree
Proposition 16, both exact; see after Corollary 7).

**Proposition 10 (fixed sets miss `z_K` except on a thin set).** Let `C` be a closed convex S-free
set with `s̄ ∈ int C`. If `z_C(w) = z_K(w) < ∞`, then `T* ⊆ C` and every corner minimizer lies in
`C ∩ S`. For `C = C_F` (`det F > 0`), `C_F ∩ S = {F^{-T} b b^T : b ∈ R^2}`, a 2-dimensional cone
inside the 3-dimensional cone of rank-one matrices. In particular, if the unique corner minimizer
lies on ray `j` alone, SCIP's set attains `z_K` only if `x̂(p_j)` is parallel to `x̂(s̄)`, i.e.
`(p_{j,a} + p_{j,d}, p_{j,c} − p_{j,b}) ∥ (ā + d̄, c̄ − b̄)`, a hyperplane condition on the ray.

*Proof.* `z_C = min_j w_j α_j = z_K` gives `α_j ≥ z_K/w_j`, so the vertices of `T*` and hence `T*`
lie in `C`. A rank-one `ab^T` lies in `C_F` iff `F^T a ∈ R_+ b` (Lemma 6's argument), i.e.
`ab^T = F^{-T}(μb)b^T`. For `F = U`: `t* = s̄ + t p_j ∈ U·{bb^T}` makes `U^T t*` symmetric; as
`U^T s̄` is symmetric and `t > 0`, `U^T p_j` is symmetric, i.e. its `J'`-coordinate
`−sin φ x_1(p_j) + cos φ x_2(p_j)` vanishes (proof of Proposition 1). ∎

So exact attainment by SCIP's set is exceptional (heuristically of measure zero; I did not
formalize the genericity for support-two minimizers). Near the hyperplane the deficit is small
(the boundaries of `C_U` and `S` touch along the contact cone), which explains why 5 of 600 random
corners attain `z_K` within `10^-5` (Section 7.1).

**Proposition 11 (SCIP's choice depends on variable scaling).** For `0 < δ ≤ 1/4` let
`s̄ = diag(1, δ) = (1, 0, 0, δ)`, `p_1 = E_12 = (0, 1, 0, 0)`, `p_2 = −E_11`, `p_3 = −δE_22`,
`p_4 = −δE_21`, `w = 1`. Then:

1. `z_K = 1` (minimizers `e_2` and `e_3`);
2. SCIP's set is `C_I` and `z_SCIP = 2√δ`;
3. `C_F` with `F^T = diag(1, 1/δ)` belongs to the point-rule family and gives `z = 1 = z_K`;
4. every BCM set gives at most `((16 + 2√73)/3)√δ < 11.1√δ` (numerically the best is `≈ 4√δ`);
5. this corner is the image of the corner `s̄' = I`, rays `E_12, −E_11, −E_22, −E_21` (on which
   SCIP's set `C_I` gives `z_K = 1`) under `M ↦ diag(1, δ)M`, i.e. under the substitution
   `x_{i2} = δ x'_{i2}` of one problem variable.

*Proof.* (1) `det(s̄ + Pλ) = δ[(1 − λ_2)(1 − λ_3) + λ_1λ_4]`; it is `≤ 0` only if `λ_2 ≥ 1` or
`λ_3 ≥ 1`, and `λ = e_2` gives `0`. (2) `s̄` is symmetric positive definite, so `U = I`. Along
`p_1`, `sym(s̄ + tE_12) = [[1, t/2], [t/2, δ]]` is PSD iff `t ≤ 2√δ`; along `p_2`, `p_3` the steps
are 1; along `p_4`, `[[1, −δt/2], [−δt/2, δ]]` gives `2/√δ`. (3) `F^T s̄ = I`; the four step lengths
of `C_F` are `2, 1, 1, 2`. (4) For `F^T = [[c, s], [−s, c]]`, `c > 0`, the condition
`sym(F^T s̄) ≻ 0` is `c²δ > s²(1−δ)²/4`, so `|u| < 2√δ/(1 − δ) ≤ (8/3)√δ` for `u = s/c`. PSD of
`sym(F^T(s̄ + tE_12))` gives `(t − u(1−δ))² ≤ 4(δ − tu)`. If `u ≥ 0` this gives
`t ≤ u(1−δ) + 2√δ < 4√δ`; if `u < 0`, `t² ≤ 4δ + 4t|u|`, so `t ≤ 2|u| + 2√(u² + δ)
< ((16 + 2√73)/3)√δ`. (5) The map `g(M) = diag(1, δ)M` sends the primed corner to this one; by
Proposition 3(2) (`A = diag(1, δ)`, `B = I`) it sends SCIP's set `C_I` at `s̄' = I` to `C_F` with
`F^T = diag(1, 1/δ)`, which therefore attains `z_K` here, while SCIP's set at the image apex
`diag(1, δ)` is again `C_I`. ∎

Computed check (`code/scaling_example.py`, [logs/scaling_example.log](logs/scaling_example.log)):
for `δ = 10^-1, …, 10^-6`, `z_K = 1`, SCIP `= 2√δ`, point rule `=` orbit `= 1`, BCM
`0.885, 0.365, 0.123, 0.0396, 0.0126, 0.0040` (`≈ 4√δ` for small `δ`).

So the point-rule and orbit families, which are invariant under `G_+`, do not depend on how the
problem variables are scaled, while SCIP's set and the BCM family do. This is the minor analogue
of sfree Proposition 6, with an explicit mechanism (variable scaling).

## 7. How often, and how large

All values in this section are targeted local computations (commands in Section 11), not CI
results. "Attains" means ratio `≥ 1 − 10^-5`. Ratios are certified lower bounds from explicit
sets (exact one-cut bounds of an explicit `F`, floating point).

### 7.1 Random corners

`code/exp_random.py`: `s̄ ~ N(0, I_4)` conditioned on `det s̄ > 0`, rays `p_j ~ N(0, I_4)`,
`w_j ~ U(0.2, 2)` ([logs/exp_random_N4_a.jsonl](logs/exp_random_N4_a.jsonl),
`…_N4_b.jsonl`, `…_N8.jsonl`; summary [logs/analysis.log](logs/analysis.log)).

| | `N = 4` (600 corners) | `N = 8` (300 corners) |
| --- | --- | --- |
| minimizer support 1 / 2 / 3 | 499 / 101 / 0 | 268 / 32 / 0 |
| orbit attains `z_K` | 593 (support 1: 496 of 499; support 2: 97 of 101) | 295 (267 of 268; 28 of 32) |
| point rule attains | 521 (support 2: 59 of 101) | 274 (support 2: 20 of 32) |
| BCM attains | 435 (support 2: 1 of 101) | 240 (support 2: 0 of 32) |
| SCIP's set attains | 5 (support 2: 0) | 6 (support 2: 0) |
| SCIP ratio mean / median / 10% quantile / min | 0.883 / 0.963 / 0.656 / 0.091 | 0.936 / 0.978 / 0.815 / 0.401 |
| BCM ratio mean / 10% quantile / min | 0.974 / 0.927 / 0.316 | 0.992 / 0.987 / 0.680 |
| point-rule ratio mean / 10% quantile / min | 0.978 / 0.990 / 0.141 | 0.993 / 1.000 / 0.583 |
| orbit misses, ratios | 0.775, 0.982, 0.985, 0.995, 0.996, 0.997, 0.99994 | 0.973, 0.995, 0.9992, 0.9996, 0.9999 |

All 12 orbit misses are certified exactly (`code/verify_misses.py`,
[logs/verify_misses.log](logs/verify_misses.log)): after rounding apex and rays (scaled to
`w = 1`) to denominators `10^6`, `z_K ≥ z_lo` is proved by `det > 0` on `T_{z_lo}` and
`z_orbit ≤ z_up` by a rational dual certificate, and `z_up/z_lo < 1` in every case (largest
`0.99994`). On random corners the orbit misses `z_K` rarely (about 1–2%), both on support-one and
on support-two corners, while SCIP's set almost never attains it.

### 7.2 LP corners

`code/exp_lp.py`: random bipartite bilinear programs with `x ∈ R^p`, `y ∈ R^q`
(`(p, q) = (3, 3)` and `(4, 4)`), lower bounds `U(−1, 0.5)`, widths `U(0.5, 2)`, a variable
`X_ik` for every product `x_i y_k` with its four McCormick inequalities, 3 (resp. 4) random
linear rows over `(x, y)`, and a random objective over all variables; HiGHS optimal basis, the
most violated minor (largest `|det|`, at least `10^-4`), projected basis cone. LP helpers are reused from the sfree
note (`exp_mccormick.py`). Besides the one-cut ratios, the LP over the McCormick polytope is
re-solved with each family's best cut, and the gain is reported as a fraction of the single-minor
gap `z_1 − z_LP`, `z_1 = min{c^T x : x ∈ P, det M = 0}` (SCIP, all solved to optimality).
"orbit-near-SCIP" is the orbit set closest to SCIP's set (Frobenius distance of `F^T` to `cU^T`)
among those attaining the orbit bound; it shows how much the choice among optimal sets matters.

| | 3×3 programs (86 corners) | 4×4 programs (71 corners) |
| --- | --- | --- |
| violated minors per LP vertex (mean) | 6.7 | 25.0 |
| orbit attains `z_K` | 86 | 71 |
| point rule attains | 83 | 69 |
| BCM attains | 73 | 59 |
| SCIP's set attains | 5 | 7 |
| SCIP ratio mean / median / 10% quantile / min | 0.922 / 0.983 / 0.785 / 0.104 | 0.931 / 0.980 / 0.787 / 0.424 |
| BCM ratio mean / 10% quantile / min | 0.981 / 0.991 / 0.175 | 0.989 / 0.980 / 0.811 |
| point-rule ratio mean / 10% quantile / min | 0.988 / 1.000 / 0.207 | 0.998 / 1.000 / 0.825 |
| `z_K` as fraction of the single-minor gap, mean / median | 0.525 / 0.446 | 0.509 / 0.470 |
| LP re-solve, fraction of gap (mean / median): SCIP's cut | 0.778 / 0.857 | 0.771 / 0.802 |
| BCM best set | 0.787 / 0.890 | 0.751 / 0.765 |
| point-rule best set | 0.763 / 0.851 | 0.754 / 0.808 |
| orbit best set, max-margin choice | 0.702 / 0.767 | 0.706 / 0.751 |
| orbit best set nearest to SCIP's | 0.800 / 0.888 | 0.777 / 0.835 |
| corner-optimal cut `w^T λ ≥ z_K` | 0.525 / 0.446 | 0.509 / 0.470 |
| orbit (max-margin) vs SCIP: better / worse by more than 0.01 | 22 / 42 | 29 / 33 |
| orbit nearest to SCIP vs SCIP: better / worse by more than 0.01 | 30 / 16 | 30 / 10 |

Paired differences of the LP re-solve fractions (family minus SCIP's cut, per corner;
`code/analyze.py`, [logs/analysis_rev3.log](logs/analysis_rev3.log)). The interval is a 95% percentile
bootstrap interval for the mean (10000 resamples, seed 0). The sign test is the exact two-sided
test on the corners whose difference exceeds 0.01 in absolute value. The Wilcoxon signed-rank test
is two-sided, on all differences (added in the round-2 revision). In parentheses: the p-value
after a Bonferroni adjustment for the eight comparisons made (four families, two sizes),
separately for each test. The Wilcoxon p-values are scipy's defaults: one zero difference per
comparison is dropped, and at these sample sizes the normal approximation is used; the exact
null distribution gives p-values within 0.003 of these and changes no statement below. The
Wilcoxon test is valid under the null hypothesis that the differences are symmetric about 0.
These differences are skewed (means and medians differ), so a small Wilcoxon p-value can reflect
asymmetry as well as a shift. On 3×3 the typical-corner claims below rest on Wilcoxon alone,
with this symmetry caveat; neither adjusted sign test rejects. Choosing whichever of the
two tests rejects adds a second multiplicity. The updated log also gives factor-16
Bonferroni values, covering both tests for all eight comparisons: the nearest-to-SCIP
3×3 Wilcoxon and 4×4 sign tests remain below 0.05 (`0.018`, `0.036`), as does the 3×3
max-margin Wilcoxon test (`0.049`). These are numerical evidence with the stated caveat.

| Comparison | Size | Mean | 95% interval | Median | Better / worse | Sign test p (adj.) | Wilcoxon p (adj.) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| orbit, max-margin choice | 3×3 | −0.076 | [−0.117, −0.037] | −0.008 | 22 / 42 | 0.017 (0.13) | 0.003 (0.025) |
| orbit, max-margin choice | 4×4 | −0.065 | [−0.107, −0.025] | +0.0005 | 29 / 33 | 0.70 (1) | 0.042 (0.34) |
| orbit nearest to SCIP's | 3×3 | +0.022 | [+0.002, +0.045] | +0.004 | 30 / 16 | 0.054 (0.43) | 0.001 (0.009) |
| orbit nearest to SCIP's | 4×4 | +0.006 | [−0.020, +0.029] | +0.002 | 30 / 10 | 0.002 (0.018) | 0.012 (0.099) |
| BCM best set | 3×3 | +0.010 | [−0.017, +0.035] | +0.002 | 31 / 21 | 0.21 (1) | 0.037 (0.30) |
| BCM best set | 4×4 | −0.020 | [−0.052, +0.008] | +0.0005 | 25 / 22 | 0.77 (1) | 0.97 (1) |
| point-rule best set | 3×3 | −0.015 | [−0.045, +0.015] | +0.002 | 34 / 31 | 0.80 (1) | 0.91 (1) |
| point-rule best set | 4×4 | −0.017 | [−0.050, +0.014] | +0.004 | 33 / 27 | 0.52 (1) | 0.91 (1) |

Both reviewers computed these statistics with independent code
([reviews/r1-logs/rev_lpstats.log](reviews/r1-logs/rev_lpstats.log),
[reviews/r2-logs/r2_lpstats.log](reviews/r2-logs/r2_lpstats.log)). The means, counts and sign-test
p-values agree, and so do the medians and the Wilcoxon p-values of the second review. The
interval ends differ from the note's by at most 0.0013 (round 1) and 0.0010 (round 2), because
the bootstrap resamples differ.

No corner had a zero reduced cost among the rays that move the minor, and every single-minor
problem was solved to optimality. "Max-margin choice" is the set the bisection returns: for `z`
just below `z_K` it maximizes the smallest eigenvalue of `sym(F^T V)` over the vertices of `T_z`,
after the normalization `sym(F^T M̄) ⪰ I` in the coordinates where `M̄ = I`.

- On these LP corners the orbit always attains `z_K`; SCIP's set attains it in 12 of 157 corners
  and loses 7–8% of `z_K` on average (more than 20% in about one corner in ten).
- After re-solving the LP, the choice among the many sets that attain `z_K` matters more than
  attaining `z_K`. I separate the mean from the typical corner.
  - *Max-margin optimal set.* In mean it closes less of the gap than SCIP's set (both intervals
    exclude 0), and the mean loss is dominated by a minority of corners with large losses (the
    medians are near 0: `−0.008`, `+0.0005`). For the typical corner the loss is supported on 3×3
    (22/42; Wilcoxon `p = 0.003`, `0.025` adjusted; sign test `p = 0.017`, `0.13` adjusted) but not
    on 4×4 (29/33; sign test `p = 0.70`; Wilcoxon `p = 0.042`, `0.34` adjusted).
    On 3×3 this rests on Wilcoxon alone with the symmetry caveat above; its factor-16
    value is `0.049`.
  - *Optimal set nearest SCIP's.* For the typical corner it is better than SCIP's set: better by
    more than 0.01 in more corners than worse (30/16 and 30/10), and for each size one of the two
    tests stays below 0.05 even after factor-16 adjustment (3×3: Wilcoxon `0.018`; 4×4:
    sign test `0.036`). On 3×3 the claim rests on Wilcoxon alone, with its symmetry caveat;
    on 4×4 the sign test supports it. Its mean gain is small (`+0.022` and
    `+0.006`) and not established: for 4×4 the interval contains 0, and for 3×3 it only just
    excludes 0 (lower end `+0.002`), with no multiplicity adjustment.
  - *Best BCM and point-rule sets.* Not distinguishable from SCIP's set in these data: no
    interval excludes 0 and no adjusted p-value is below 0.05 (the smallest unadjusted one,
    Wilcoxon `0.037` for BCM on 3×3, becomes `0.30`).

  This agrees with sfree §9.2 (re-solving changes the picture) and is not evidence of a
  solver-level benefit. These are single cuts on small random programs; several rounds inside
  SCIP were not tested.

### 7.3 Adversarial corners

`code/adversarial.py`: Nelder–Mead over full-dimensional tangent-edge corners (22 parameters,
`w = 1`), starting from corners of the search in 7.4, minimizing the orbit ratio subject to
non-degeneracy margins `≥ m` (`m = 0.01` and `0.05`), all invariant under `G_+`: no ray within
relative discriminant `m` of grazing the null cone, multipliers of the two off-edge rays `≥ m`, second-order
margin along the edge, and the apex away from the null cone relative to the rays (definitions in
the docstring).

*Margin 0.01* (10 restarts: with seed 1 the four worst search corners and two random ones, of
which two violated the margins and were skipped; with seed 2 six random search corners;
[logs/adversarial_m01_s1.jsonl](logs/adversarial_m01_s1.jsonl),
[logs/adversarial_m01_s2.jsonl](logs/adversarial_m01_s2.jsonl)). Final orbit ratios: 0.2003,
0.2004, 0.3984, 0.5984, 0.6329, 0.7074, 0.7193, 0.7518, 0.7543, 0.9185. In every run the smallest
margin at the end equals the imposed one (0.0100–0.0109); in the two best runs it is the grazing
margin of the rays. So the search stops at the boundary of the allowed region and the values
measure the margin, not an intrinsic minimum. All ten final corners were rounded to rationals
(denominator `10^4`) and certified with `code/certify_ratio.py`
([logs/certify_ratio_adv_m01_s1.log](logs/certify_ratio_adv_m01_s1.log),
[logs/certify_ratio_adv_m01_s2.log](logs/certify_ratio_adv_m01_s2.log)): `z_K ≥ z_lo` exactly
(`det > 0` on `T_{z_lo}`) and `z_orbit ≤ z_up` by a rational dual certificate, giving exact ratio
upper bounds 0.20033, 0.20040, 0.39837, 0.59843, 0.63288, 0.70745, 0.71933, 0.75183, 0.75436,
0.91850. Rounding does not break the margin condition: recomputed for the rounded corners
(`code/rounded_margins.py`, an implementation independent of `adversarial.py`;
[logs/rounded_margins_adv_m01_s1.log](logs/rounded_margins_adv_m01_s1.log),
[logs/rounded_margins_adv_m01_s2.log](logs/rounded_margins_adv_m01_s2.log)), the smallest margin
of each of the ten certified corners lies between `0.01001` and `0.01087`, and the minimizer of
each rounded corner still has support `{1, 2}`. The grazing, second-order and apex margins are
computed exactly; the multiplier margins depend on the numerically computed minimizer. On the
float corners the same code reproduces the logged margins to `2.5·10^-14`.

*Margin 0.05* (seed 1, eight starts, six of them violating the margins;
[logs/adversarial_m05_s1.jsonl](logs/adversarial_m05_s1.jsonl)): final ratios 0.3264 (from the
start that reached 0.2004 with margin 0.01) and 0.8458; in both the active margin is the apex
margin (0.0501, 0.0546). Exact ratio upper bounds after rounding: 0.32638 and 0.84583
([logs/certify_ratio_adv_m05_s1.log](logs/certify_ratio_adv_m05_s1.log)); the rounded corners have
smallest margins `0.05008` and `0.05456`
([logs/rounded_margins_adv_m05_s1.log](logs/rounded_margins_adv_m05_s1.log)). So the attainable
ratio grows with the margin, consistent with (but not proof of) the ratio tending to 0 only as
the corner degenerates.

*No comparison with the bilinear search.* The sfree note's adversarial search for the bilinear
family (A) (its §8.6) reached `0.4526` with rays at least 1% from grazing and a vertex violation
`q(s̄)/max|P|² ≈ 9·10^-4`, and a numerical `0.028` with rays 1% from grazing and the vertex almost
on `∂S` (`q(s̄)/max|P|² ≈ 10^-7`). Its only margin was the ray-grazing margin (the same formula
as here, applied to its quadratic; `sfree/code/adversarial_ratio.py`), with `q(s̄) > 10^-6`. It
imposed no margin on the apex, the multipliers or the second-order condition, and it reached its
lowest value (`0.028`) by letting the apex approach `∂S`, which the apex margin here forbids. The
two searches are therefore not comparable, and the numbers here do not show that minor corners
have lower ratios than bilinear corners. In any case, by Corollary 7 every bilinear corner is a
(lower-dimensional) minor corner, so the worst minor ratio is at most the worst bilinear ratio. The values here are heuristic upper bounds on the worst case; they
suggest, but do not prove, that no constant ratio holds without a non-degeneracy condition (open
question 2).

### 7.4 Searches for rational counterexamples

- `code/search_cex.py` (four seeds, 200000 trials each; [logs/search_cex_*.log](logs/)): of 1487
  constructed rational tangent-edge corners with `z_K = 1` (biased construction: integer rank-one
  `t*`, half-integer tangent `D`), 354 had disjoint `κ`-intervals on a grid `|κ| ≤ 200`; their
  orbit ratios range from `0.4495` to `1` (quantiles 10%/50%/90%: `0.890`, `0.988`, `0.9998`;
  13 had ratio `≥ 0.99999`, where the intervals presumably meet outside the grid). Instances A
  and B come from this search.
- `code/search_supp1.py` (20000 trials; [logs/search_supp1_7.log](logs/search_supp1_7.log)): of
  717 constructed support-one corners with nearly tangent edges, 89 had orbit ratio `< 1 − 10^-4`,
  the worst `0.778` (instance S1).

## 8. Other minors

- *Principal minors* (`{i1, i2} = {j1, j2}`, so `b = c` is one variable). On the 3-dimensional
  space `{b = c}`, `det = ad − b²` has signature `(1, 2)`. If `det M̄ > 0` and `ā + d̄ > 0`,
  the component of `{det > 0}` containing `M̄` is the open positive definite cone, which is
  convex; every S-free set containing `M̄` in its interior lies in its closure, the PSD cone,
  which is S-free. So the PSD cone is the unique maximal set, SCIP's set restricted to `{b = c}`
  is this cone (`U = I`), and SCIP's cut attains `sup_C z_C = z_K` (sfree Theorem 1(2)–(3);
  proved). The case `ā + d̄ < 0` is the same with the negative semidefinite cone (`U = −I`).
  If `det M̄ < 0` the form `b² − ad` has signature `(2, 1)`; by sfree Theorem 8(1) the orbit is
  then all maximal sets, while SCIP uses one point-rule set (not studied here). Taking
  `X_ii, X_jj ≥ 0` into account, the relevant set is the cone of rank-one PSD matrices, and the
  maximal free sets containing an indefinite `M̄` are halfspaces `⟨A, X⟩ ≥ 0` with `A` NSD (BCM
  Theorem 27). The intersection cut of such a halfspace is dominated, on the cone, by the valid
  linear inequality `⟨A, X⟩ ≤ 0`. Writing `−A = μ_1 g_1 g_1^T + μ_2 g_2 g_2^T` with `μ_i ≥ 0`, this
  inequality is a nonnegative combination of at most two inequalities `g_i^T X g_i ≥ 0`, which
  are of the type `sepa_minor` uses (with `v_0 = 0`). `sepa_minor` takes its vectors from
  eigenvectors of the augmented 3×3 matrix at the LP point, so it does not necessarily separate
  these particular inequalities.
- *One diagonal entry* (e.g. `a = X_ii`). The projection of `{xx^T}` onto the four entries has
  closure `{det = 0, a ≥ 0}` (proved by the substitution `x_i = √a`, `x_l = b/√a`,
  `x_j = c/√a` for `a > 0` and a limit for `a = 0`). This set is smaller than `S`, so it has
  larger free sets; BCM Theorem 23 shows that `C_λ` is then maximal only for special `λ`, and
  Chmiela et al. use the Case-4-type enlargement (`usebounds`, off by default, and in SCIP 10 only
  used when the diagonal LP value is negative). The analysis above applies to `S = {det = 0}`; for
  these minors the relevant corner bound is at least as large, so the ratios of SCIP's set to it
  can only be smaller. Not studied further.

## 9. Relation to earlier notes and prior work

**Earlier notes.**

- *sfree note.* §10.2 left open whether the tangent-edge obstruction also occurs for the minor
  sets. It does (Theorems 8, 9), and Corollary 7 shows that the bilinear counterexamples
  (Theorem 14, the second rational instance of §8.5, Proposition 16) are the special case of
  minor corners lying in a hyperplane. Instances A and S1, the worst instances of the two
  rational searches (Section 7.4), have larger gaps than all three certified bilinear
  instances: orbit ratios at most `0.4495363` and
  `0.7781193` against at least `0.8347663`, `0.9753853` and `0.9838465` (all exact; the bilinear
  brackets are computed here, after Corollary 7, because sfree gives these values numerically and
  certifies only the strict gap). Instance B, also certified, has orbit ratio
  `[0.9219403, 0.9219593]`, between the bilinear values `0.835` and `0.975`; its gap is smaller
  than that of the bilinear second rational instance. The 12 rounded adversarial corners and
  12 rounded random misses have exact one-sided ratio upper bounds (Section 7);
  their lower bounds are numerical. B alone proves exactly that there is no uniform
  ordering of minor gaps above the bilinear gaps. The comparison for A and S1 is about those selected instances,
  not about the worst cases (Section 7.3). In the homogeneous minor case there is no
  maximal completion (family (B)): the orbit sets are already maximal, so the obstruction is
  purely one of the orbit. Lemma 6 is sfree Lemma 13 without slicing; Proposition 5 sharpens sfree
  Theorem 4 (`ρ = 3`) for minors; Proposition 11 is the minor analogue of sfree Proposition 6; the
  point-rule family of Proposition 3(3) is the homogeneous analogue of sfree §6.1.
- *Corrections to earlier notes.* None needed. Two precisions. (a) sfree §10.2 says the sets `C_F`
  are "related to" the outer-product-free sets that Chmiela et al. identify with their minor sets.
  By Proposition 1 and Proposition 3(4), BCM's sets (14a) are exactly the rotation members `C_R`
  of the orbit, and SCIP's minor set is the member `C_U` (polar factor). (b) The sfree family-(A)
  values `0.97539` (Theorem 14), `0.83477` (second rational instance, §8.5) and `0.98385`
  (Proposition 16) are numerical there. The exact brackets after Corollary 7 agree with them: the
  first and third brackets fix all five decimals given, and the second,
  `[0.8347663, 0.8347772]`, fixes four decimals and contains `0.83477`.

**Prior work** (sources in [sources/MANIFEST.md](sources/MANIFEST.md)).

- *Bienstock–Chen–Muñoz* (Math. Program. 183, 2020, arXiv:1610.04604v7): sets (14a)/(14b) from
  2×2 submatrices (Lemma 22), maximality for every unit `λ` when no entry is diagonal
  (Theorem 23(iv)), the choice (17a) of `λ` (Lemma 24), with the remark that it is "best in a
  violation sense, and may not translate to finding the deepest cut", and the characterization of
  maximal outer-product-free sets in `S^{2×2}` (Theorem 27). Proposition 1 identifies (17a) with
  the polar decomposition; Propositions 10, 11 and Theorems 8, 9 quantify their remark.
- *Chmiela–Muñoz–Serrano* (Math. Program. 197, 2023; ZIB Report 20-29), §3.1: the implied minor
  equations are treated as Case 1 and the resulting set "is exactly one of the maximal
  outer-product-free sets constructed by Bienstock et al."; for a diagonal entry they use the
  Case-4-type set. In their experiments (MINLPLib, 587 instances) the best setting, ICUTS+MINOR-B,
  closed on average 8% more of the gap than SCIP's default, mostly because of ICUTS, with a
  "non-negligible" contribution of the minor cuts. They do not discuss the choice of `λ` for
  minors.
- *Muñoz–Paat–Serrano* (Math. Program. 2025, arXiv:2211.05185): every full-dimensional maximal
  homogeneous quadratic-free set is `C_Γ`, characterized by Theorem 1.2; for `det` this is the
  infinite-dimensional family of Lemma 2, of which the orbit is a 3-dimensional part.
- *Muñoz–Serrano*, "Maximal quadratic-free sets" (Math. Program. 192, 2022; arXiv:1911.12341):
  the set `C_λ` and its maximality (Theorem 2.1 of the journal version as cited by
  Muñoz–Paat–Serrano; Theorem 7 of arXiv v2, which I read); the role of transformations left
  open.

**Novelty assessment.** In the sources above I did not find: the polar-decomposition form of
SCIP's minor set, the description of the orbit and point-rule families for minors, the
homogeneous pencil lemma, the support statement of Proposition 5, the variable-scaling
dependence (Proposition 11), the contact-cone statement (Proposition 10), or certified
counterexamples. The techniques are those of the sfree note. My search was small (three web
searches; the arXiv API was rate-limited; no citation search), so these are not novelty claims.

## 10. Revisions after review

### 10.1 Revision after review round 1 (2026-10-02)

Review: [reviews/review-r1.md](reviews/review-r1.md), verdict "minor fixes", no major issue. The
reviewer checked every proof, re-ran the exact certificates and parts of the experiments, and
recomputed the main numbers with independent code (in `reviews/r1-code/`). No proof needed
repair and no number changed. The changes are to wording, labels and uncertainty statements.

| Issue | Handling |
| --- | --- |
| Minor 1: no process-hygiene statement; commands without `timeout` | Added the process-hygiene section (now Section 11.5). It says that the original runs had no `timeout` wrapper and how each was bounded instead (fixed counts, iteration caps, SCIP time or node limits), that outputs are flushed per record and the scripts are deterministic given their arguments, and that no background process is left. All revision commands ran under `timeout` (Section 11.2). Added a line to Limits. |
| Minor 2: "with larger gaps" and the comparison with the bilinear adversarial search not supported | Headline changed to "yes", with the narrower supported statement: the selected certified instances A and S1 (0.45, 0.78), the worst instances of the two rational searches, have larger gaps than all three certified bilinear instances (0.835, 0.975 and 0.984). Round 2 corrected the bilinear list; round 3 names A and S1 explicitly and includes certified instance B, whose ratio `[0.9219403, 0.9219593]` gives a smaller gap than the bilinear second rational instance (Section 10.3). The other certified corners are listed in Section 7. The sentence "reach lower ratios under comparable margins" in Section 7.3 is withdrawn and replaced by a paragraph that quotes both sfree numbers (`0.4526` with vertex violation `≈ 9·10^-4`; numerical `0.028` with the vertex almost on `∂S`), explains that the sfree search imposed only the ray-grazing margin (no apex, multiplier or second-order margin), and notes that by Corollary 7 the worst minor ratio is at most the worst bilinear ratio. Section 9 qualified in the same way. |
| Minor 3: Summary item 4 drops the hypothesis "`P_J` injective" of Proposition 5 | Summary item 4 now states the hypothesis (minimizers with linearly independent projected rays; one always exists) and says that the bound can fail otherwise. Added the reviewer's duplicated-ray example after Proposition 5. Proposition 5 itself was already correctly stated. |
| Minor 4: LP re-solve comparisons without uncertainty | Added paired statistics to `code/analyze.py` (bootstrap 95% interval of the mean, median, exact sign test) and regenerated `logs/analysis.log`; the values agree with the reviewer's independent computation. Added the table to Section 7.2 and rewrote the conclusions there and in Summary item 6. Changed claims: the gain of the orbit set nearest SCIP's is now "suggested, not established" (for 4×4 the interval of the mean contains 0; refined in round 2, Section 10.2: typical-corner gain fairly well supported, mean gain not established); the loss of the max-margin set holds in mean (both intervals exclude 0) but is dominated by a minority of corners with large losses (medians near 0; better/worse 22/42 on 3×3, but 29/33 on 4×4). |
| Minor 5: Proposition 1, labelled proved, includes `nlhdlr_quadratic` Case 1 | Proposition 1 now states a proof about the Case-1 formula of `sepa_interminor`, with a "scope of proved" paragraph: that `sepa_interminor` implements it rests on source reading and the fidelity check; that `nlhdlr_quadratic` uses the same set rests on source reading only and was not tested. Same label in Summary item 1, Section 2 and Limits; new open question 6. |
| Optional 1: stale theorem numbers in code docstrings | Fixed in `minor_core.py`, `certify_cex.py`, `certify_supp1_full.py`, `scaling_example.py`, `embed_check.py`, `test_core.py`, `cert_lib.py` (comments and docstrings only). Re-ran `certify_cex.py` (instance A), `certify_supp1_full.py`, `embed_check.py` and `scaling_example.py`: outputs identical to the original logs (Section 11.2). |
| Optional 2: `certify_ratio.py` docstring promises margins it does not print | Docstring corrected. New script `code/rounded_margins.py` recomputes the margins of the rounded corners independently of `adversarial.py`: all ten 1% corners keep margins `≥ 0.01001`, the two 5% corners `≥ 0.05008` (Section 7.3, Summary item 5). This agrees with the reviewer's check. |
| Optional 3: "four distinct entries/variables" also covers one-diagonal minors | Summary and Section 1 now say "four distinct indices (so no entry is diagonal)". |
| Optional 4: Section 8, `⟨A, X⟩ ≤ 0` is a combination of up to two inequalities `g^T X g ≥ 0`, and `sepa_minor` need not separate it | Section 8 reworded as suggested. |
| Optional 5: the printed "bisection upper" value is not a bound | Section 3 (after Proposition 4) now says so, with the instance-A example. |
| Optional 6: "Theorem 2.1 of their homogeneous paper" | Replaced by the full reference (Muñoz–Serrano, "Maximal quadratic-free sets", Math. Program. 192 (2022), Theorem 2.1 as cited by Muñoz–Paat–Serrano; Theorem 7 of arXiv v2, checked in the text) in the proof of Proposition 3 and in Section 9. |

Also corrected, not raised by the review: the header said "Nothing here has been committed",
but an earlier version of this note is in the repository history (committed outside this
stream).

Not changed: all theorems, proofs, certificates and experimental numbers other than the added
statistics and margins.

### 10.2 Revision after review round 2 (2026-10-02)

Review: [reviews/review-r2.md](reviews/review-r2.md), verdict "minor fixes", no major issue. The
reviewer found four of the five round-1 minor issues fixed and all six optional items handled,
re-verified instances A and S1, the LP statistics and the rounded adversarial margins with
independent code (in `reviews/r2-code/`), and reran one SCIP fidelity smoke test (13 of 13 cuts
matched). One minor issue and five optional items remained.

| Issue | Handling |
| --- | --- |
| Minor 1: the headline comparison with the bilinear case lists only two of the three certified bilinear instances (it omits sfree's second rational instance, `z_A = 0.83477`); the sfree values are numerical | Fixed in the Summary ("Answer" and item 3), Section 9 and the round-1 table above: the comparison now lists all three instances, `0.835`, `0.975` and `0.984`. The comparison holds for A and S1 (`0.45, 0.78 < 0.835`), selected as the worst instances of the two rational searches; it does not hold for all certified minor instances. Round 3 adds certified B, whose ratio `[0.9219403, 0.9219593]` lies between the bilinear values `0.835` and `0.975`, and points to the other certified corners in Section 7 (Section 10.3). Beyond the wording fix, the new script `code/certify_embed_brackets.py` brackets the orbit bound of the three embedded bilinear corners exactly (`[0.9753853, 0.9753864]`, `[0.8347663, 0.8347772]`, `[0.9838465, 0.9838468]`; text after Corollary 7). By Corollary 7 these are exact brackets of the sfree family-(A) values. So the comparison is now exact on both sides: the certified upper bounds for A and S1, `9/20` and `779/1000`, lie below the smallest bilinear lower bound `0.8347663`, which the script checks. The sentence after Theorem 9 now compares exact bounds (`≤ 0.7781193` against `≥ 0.9838465`). Section 9 records, as a precision to the sfree note (not a correction), that these brackets agree with its numerical values. |
| Optional 1: the second S1 cosine is `0.010525`, which rounds to `0.011` | Theorem 9 and the paragraph after it now say `0.011` and `0.011`–`0.088` (recomputed exactly, Section 11.3). |
| Optional 2: "differ only in the fourth decimal" is wrong | Section 7.2 now says that the interval ends differ from the note's by at most `0.0013` (round 1) and `0.0010` (round 2), because the bootstrap resamples differ (computed from the three logs, Section 11.3). The second figure is larger than the review's "at most `0.0005`": the largest difference is the 4×4 point-rule lower end, `−0.050798` against `−0.0498`. |
| Optional 3: separate "typical corner" from "mean"; add Bonferroni and Wilcoxon | `code/analyze.py` now also prints the two-sided Wilcoxon signed-rank p-value and the Bonferroni-adjusted p-values (factor 8) of both tests; the values equal the reviewer's `r2_lpstats.log`. The table in Section 7.2 has the new columns, and the Wilcoxon test carries a caveat (it assumes differences symmetric about 0 under the null hypothesis, and these differences are skewed; scipy's default normal approximation is reported, and the exact test changes no statement). Section 7.2 and Summary item 6 now state typical-corner and mean results separately. Round 2 described the nearest-to-SCIP typical-corner gain as "fairly well supported"; round 3 states explicitly that the 3×3 claim rests on Wilcoxon alone with its symmetry caveat and checks factor 16 over both tests (Section 10.3). The mean gain remains unestablished. For the max-margin set, a typical-corner loss is supported on 3×3 (Wilcoxon `0.025` adjusted) but not on 4×4 (`0.34` adjusted), and the mean loss is unchanged. For BCM and the point rule, no adjusted p-value is below 0.05. |
| Optional 4: in Summary item 5, "certified exactly" might seem to cover the multiplier margins | Summary item 5 now says that the ratio bound is certified exactly and that the multiplier margins are computed numerically, the other margins exactly. |
| Optional 5: the `minor_core.py` docstring still says "four distinct entries" | Changed to "four distinct indices (so no entry of the minor is diagonal)". All scripts compile, and `certify_supp1_full.py`, which imports `minor_core.py`, reproduces its log byte for byte (Section 11.3). |

Not changed: all theorems, proofs, certificates and experimental numbers. New: the exact brackets
of the embedded bilinear instances, and the Wilcoxon and Bonferroni-adjusted statistics.

### 10.3 Revision after review round 3 (2026-10-03)

Review: [reviews/review-r3.md](reviews/review-r3.md), verdict "minor fixes",
one minor issue and two optional items. Round 4 verified this revision;
its optional one-sided-certificate clarification is applied in the Summary, Section 9 and Limits.

- **Minor 1 (selective minor comparison).** The Summary, Section 9 and the historical
  revision tables now name A and S1 as the worst instances of the two rational searches,
  include certified B (`[0.9219403, 0.9219593]`), and point to the 12 rounded adversarial
  corners and 12 rounded random misses. Only A and S1 are claimed to have larger gaps
  than all three certified bilinear instances; B has a smaller gap than the bilinear
  second rational instance. No uniform ordering or worst-case comparison is claimed.
- **Optional 1 (cost-one check and printed certificates).**
  `code/certify_embed_brackets.py` now checks exact nonnegative ray weights of cost 1
  for each `t*`: `(1/2, 1/2, 0)`, `(6/7, 1/7, 0)`, `(1, 0, 0)`.
  It prints the rational lower `F^T` and upper `Y_v` certificates and exits nonzero
  on a failed check. All three existing brackets reproduce (Section 11.4).
- **Optional 2 (Wilcoxon reliance and second multiplicity).** The Summary, Section 7.2
  and Limits say that the 3×3 typical-corner claims rest on Wilcoxon alone, with its
  symmetry caveat. `code/analyze.py` now also prints factor-16 Bonferroni values for
  both tests across all eight comparisons. The nearest-to-SCIP 3×3 Wilcoxon and
  4×4 sign tests give `0.018`, `0.036`; the 3×3 max-margin Wilcoxon gives `0.049`.
  Underlying numbers and proofs are unchanged.

### 10.4 Wording after review round 4 (2026-10-04)

[Round 4](reviews/review-r4.md) verified the round-3 revision. Its optional
clarification is applied in the Summary, Section 9 and Limits: B alone
gives the exact comparison that excludes a uniform ordering of minor and
bilinear gaps. The 24 rounded corners have exact one-sided upper
certificates and numerical lower values, not two-sided exact brackets.
These wording edits were checked by the coordinating agent and have not
been independently re-reviewed.

## 11. Checks actually run

All commands from `research-20261001/minor-sets/code/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`; Python 3.13, numpy 2.5.1,
scipy 1.18.0, cvxpy 1.9.3 (Clarabel, SCS), sympy 1.14.0, mpmath, highspy, PySCIPOpt 6.2.1
(SCIP 10.0.3 with Ipopt 3.14.19). Targeted checks only; no project-wide checks were run and CI was
not consulted. Warnings of cvxpy ("solution may be inaccurate") were filtered from the logs.

### 11.1 Original runs (2026-10-01)

| Command | What it checks | Outcome (log in `logs/`) |
| --- | --- | --- |
| `python3 scip_probe.py` | default parameters; `interminor` calls with defaults, with `freq 0` in PySCIPOpt, and in the local binary | `scip_probe.log`: defaults `freq -1`, `usebounds`/`usestrengthening` off; PySCIPOpt default 0 calls, `freq 0` 1 call / 8 found / 1 applied; binary 0 calls |
| `python3 scip_fidelity.py 1 5` | smoke test of the fidelity check | console: 19 of 19 applied cuts matched (not logged) |
| `python3 scip_fidelity.py 11 40 3 3`; `python3 scip_fidelity.py 12 20 4 4` | SCIP's applied `interminor` cuts vs predicted `C_U` cuts (Proposition 1) | `scip_fidelity_3x3.log`: 143 of 143 matched, max diff `4.0e-15`, 14 models without a separation round; `scip_fidelity_4x4.log`: 115 of 115, `4.5e-15`, 7 skipped |
| `python3 test_core.py 0` | SCIP's literal step formula vs `C_U`; `z_K` vs SCIP global solves; family nesting | `test_core.log`: `1.44e-13` over 1709 rays; 40 corners, max rel. diff `1.46e-6`; 0 nesting violations in 15 corners |
| `python3 search_cex.py 1 20000` (exploratory, console); `python3 search_cex.py S 200000`, `S = 2, 3, 4, 5` | rational tangent-edge corners with disjoint `κ`-intervals | `search_cex_S.log`: 1487 valid corners, 354 with disjoint intervals, worst orbit ratio `0.4495` |
| `python3 certify_cex.py` | Theorem 8 (instance A), exact | `certify_cex_A.log`: ALL PASS; orbit `[0.4495347, 0.4495363]`, `z_orbit ≤ 9/20` |
| `python3 certify_cex.py '<instance B JSON>'` (JSON in Section 6 and in `certify_cex_B.log`) | instance B, exact | `certify_cex_B.log`: ALL PASS; orbit `[0.9219403, 0.9219593]`, `z_orbit ≤ 461/500` |
| `python3 search_supp1.py 7 20000` | rational support-one corners where the orbit misses `z_K` | `search_supp1_7.log`: 717 valid, 89 with orbit `< 1 − 10^-4`, worst `0.778` |
| `python3 certify_supp1_full.py` | Theorem 9 (instance S1), exact | `certify_supp1_full.log`: ALL PASS; orbit `[0.7780998, 0.7781193]`, `z_orbit ≤ 779/1000` |
| `python3 embed_check.py` | Corollary 7 | `embed_check.log`: `0.97539`, `0.83477`, `0.98385` as in the sfree note |
| `python3 scaling_example.py` | Proposition 11 | `scaling_example.log`: SCIP `= 2√δ`, point rule `=` orbit `= 1`, BCM `≈ 4√δ` |
| `python3 exp_random.py 101 300 4 ../logs/exp_random_N4_a.jsonl`; `python3 exp_random.py 102 300 4 ../logs/exp_random_N4_b.jsonl`; `python3 exp_random.py 103 300 8 ../logs/exp_random_N8.jsonl` | random corners (Section 7.1) | 600 and 300 corners; orbit attains in 593 and 295; `analysis.log` |
| `python3 verify_misses.py exp_random_N4_a.jsonl exp_random_N4_b.jsonl exp_random_N8.jsonl` (paths under `../logs/`) | exact certificates for the 12 random orbit misses | `verify_misses.log`: all 12 certified, largest `z_up/z_lo = 0.99994` |
| `python3 check_prop10.py ../logs/exp_random_N4_a.jsonl ../logs/exp_random_N4_b.jsonl` | Proposition 10 on support-one random corners | `check_prop10.log`: the 5 corners where SCIP attains `z_K` have angles `0.24°–1.34°` between `x̂(p_j)` and `x̂(s̄)` (median over all 499: `34.7°`) |
| `python3 exp_lp.py 31 200 3 3 3 ../logs/exp_lp_3x3.jsonl`; `python3 exp_lp.py 41 120 4 4 4 ../logs/exp_lp_4x4.jsonl` | LP corners and LP re-solve (Section 7.2) | 86 and 71 corners, all single-minor problems optimal; orbit attains `z_K` in all; `analysis.log` |
| `python3 adversarial.py 1 6 0.01 ../logs/adversarial_m01_s1.jsonl`; `python3 adversarial.py 2 6 0.01 ../logs/adversarial_m01_s2.jsonl`; `python3 adversarial.py 1 8 0.05 ../logs/adversarial_m05_s1.jsonl` | adversarial search (Section 7.3) | margin 0.01: 10 restarts, best `0.2003`; margin 0.05: 2 valid restarts, `0.3264`, `0.8458` |
| `python3 certify_ratio.py ../logs/adversarial_m01_s1.jsonl` (also `…_m01_s2.jsonl`, `…_m05_s1.jsonl`; first run on the single best record from `/tmp`) | exact ratio bounds for the rounded adversarial corners | `certify_ratio_adv_m01_s1.log`, `…_m01_s2.log`, `…_m05_s1.log`: all 12 certified, smallest bound `0.20033` |
| `python3 analyze.py > ../logs/analysis.log` | summary tables | `analysis.log` (regenerated twice on 2026-10-02, see 11.2 and 11.3) |

Earlier runs of `exp_random.py` and `exp_lp.py` with a first version of the bisection (which
treated a solver exception as infeasibility) are kept in `logs/old_solver/` and are not used; the
final runs use the corrected solver. Exploratory smoke tests wrote to `/tmp` and are not reported.

### 11.2 Runs of the round-1 revision (2026-10-02)

Every Python computation below ran under `timeout` (the `grep` lookups and a first `py_compile`
call, which takes seconds, did not), with at most 4 processes at a time (in fact at most 2).

| Command | What it checks | Outcome |
| --- | --- | --- |
| `timeout 120 python3 -m py_compile *.py` (final run, after all edits) | the docstring and comment edits of optional item 1 and the new or changed scripts | all files compile |
| `timeout 300 python3 analyze.py > ../logs/analysis.log` | paired LP re-solve statistics (minor issue 4), added to `analyze.py` | `analysis.log`: a `diff` against the previous log shows only the 10 added lines (two headers, eight rows of the table in Section 7.2); every other line is unchanged |
| Inline `timeout 120 python3 -c ...` over `logs/exp_lp_*.jsonl` (same bootstrap, six decimals) | rounding of the values quoted in Sections 7.2 and the Summary | console only; values as quoted |
| `timeout 600 python3 rounded_margins.py ../logs/adversarial_S.jsonl > ../logs/rounded_margins_adv_S.log`, `S = m01_s1, m01_s2, m05_s1` | margins of the rounded, certified adversarial corners (optional item 2) | ten 1% corners: smallest margins `0.01001`–`0.01087`; two 5% corners: `0.05008`, `0.05456`; all rounded minimizers have support `{1, 2}`; float margins reproduce the logged ones to `2.5e-14` |
| `timeout 1800 python3 certify_cex.py > ../logs/rerun_r1/certify_cex_A.log` | instance A after the docstring edits of `certify_cex.py` and `cert_lib.py` | ALL PASS; identical to `logs/certify_cex_A.log` (cvxpy warnings went to a separate `.err` file) |
| `timeout 1800 python3 certify_supp1_full.py > ../logs/rerun_r1/certify_supp1_full.log` | instance S1 after the same edits | ALL PASS; identical to `logs/certify_supp1_full.log`; 22 s. A first attempt, started in the background together with instance A, never started (its wrapper shell exited first) and left no process; the foreground run replaced it |
| `timeout 600 python3 embed_check.py > ../logs/rerun_r1/embed_check.log 2>&1` | Corollary 7 after the docstring edit | identical to `logs/embed_check.log` apart from one cvxpy warning line |
| `timeout 900 python3 scaling_example.py > ../logs/rerun_r1/scaling_example.log 2>&1` | Proposition 11 after the docstring edit | identical to `logs/scaling_example.log` |
| `grep` in `research-20260928b/scouting/s-free-intersection-cuts/sources/1911.plain.txt` and `2211.05185.plain.txt` | the Muñoz–Serrano reference (optional item 6) | arXiv v2 Theorem 7 proves `C_λ` maximal `{‖x‖ ≤ ‖y‖}`-free; Muñoz–Paat–Serrano cite it as [24, Theorem 2.1], [24] = Math. Program. 192, 229–270 (2022) |
| `grep`/`sed` over `research-20260928b/sfree/code/adversarial_ratio.py` and sfree §8.6 | the description of the sfree adversarial search in Section 7.3 (minor issue 2) | its only margin is a ray-grazing margin of the same form as here, plus `q(s̄) > 1e-6`; numbers `0.4526` and `0.028` as quoted |
| Process check over `/proc/*/cwd` | no process left in the stream directory | none found, at the start and at the end of the revision |

Not re-run in the revision: the experiments of Sections 7.1–7.4 and the remaining exact
certificates; their code did not change except for docstrings, and the reviewer reproduced them
(Section 10).

### 11.3 Runs of the round-2 revision (2026-10-02)

Every Python computation below ran under `timeout`, in the foreground, one process at a time; no
background process was started. cvxpy warnings went to `.err` files in `logs/rerun_r2/`.

| Command | What it checks | Outcome |
| --- | --- | --- |
| Process check over `/proc/*/cwd` (start of the revision) | no process left in the stream directory | none found |
| `timeout 300 python3 analyze.py > ../logs/analysis.log` (run after each of two edits of `paired()`; final version reported) | Wilcoxon and Bonferroni-adjusted p-values (optional item 3) | exit 0; `diff` against the log of the round-1 revision: only the 10 lines of the paired-statistics block changed (two headers, eight rows). In each row the mean, interval, median, counts and sign-test p are unchanged, and the Wilcoxon p-value and both adjusted p-values are appended. The Wilcoxon values equal `reviews/r2-logs/r2_lpstats.log` |
| `timeout 1200 python3 certify_embed_brackets.py > ../logs/certify_embed_brackets.log 2> ../logs/rerun_r2/certify_embed_brackets.err` | exact brackets of the orbit (= family (A)) bound of the three embedded sfree instances; comparison with the minor instances (minor issue 1) | ALL PASS; `z_K = 1` exactly for all three; brackets `[0.9753853, 0.9753864]`, `[0.8347663, 0.8347772]`, `[0.9838465, 0.9838468]`; `9/20, 779/1000 < 0.8347663` |
| `timeout 120 python3 -c "import py_compile, glob; ..."` (all `code/*.py`, bytecode to `/tmp`) | the docstring edit of `minor_core.py`, the edits of `analyze.py`, the new script | 21 files compile |
| `timeout 1800 python3 certify_supp1_full.py > ../logs/rerun_r2/certify_supp1_full.log 2> ../logs/rerun_r2/certify_supp1_full.err` | instance S1 after the docstring edit of `minor_core.py` (optional item 5) | ALL PASS; byte-identical to `logs/certify_supp1_full.log`; 15.5 s |
| Inline `timeout 120 python3 -c ...` over `logs/exp_lp_*.jsonl` (`scipy.stats.wilcoxon` with the default, `method='approx'` and `method='exact'` on the nonzero differences) | which Wilcoxon variant `analyze.py` reports, and whether it matters | default = normal approximation (scipy 1.18.0), one zero difference per comparison; exact p-values within 0.003 (e.g. `0.00096` instead of `0.00112` for the 3×3 nearest-to-SCIP comparison, `0.0118` instead of `0.0124` for 4×4); no conclusion changes |
| Inline `timeout 60 python3 -c ...` (exact `∇det(t*)·(v − t*)` for S1, then cosines in floating point) | the S1 cosines (optional item 1) | `9/2, 1/8, 1, 1/2`; cosines `0.088235, 0.010525, 0.036711, 0.016769` |
| Inline `timeout 60 python3 -c ...` (parses the bootstrap intervals in `logs/analysis.log`, `reviews/r1-logs/rev_lpstats.log`, `reviews/r2-logs/r2_lpstats.log`) | the size of the interval differences (optional item 2) | largest difference of interval ends `0.0013` (round 1) and `0.0010` (round 2) |
| `grep`/`sed` over sfree Summary, §8.5 and Proposition 16 (`research-20260928b/sfree/optimal-intersection-cuts.md`) | status of the sfree values `0.97539`, `0.83477`, `0.98385` (minor issue 1) | all three numerical; strict gap `z_A < z_K` proved (Theorem 14, Proposition 16) or certified by disjoint `κ`-intervals (second instance) |
| Process check over `/proc/*/cwd` and `ps` (end of the revision) | no process left in the stream directory | none found (the only matching `analyze.py` jobs belong to another stream's directory and were not started by me) |

Not re-run in this revision: the experiments of Sections 7.1–7.4, the SCIP checks and the
other exact certificates. Their code did not change (apart from the `minor_core.py` docstring),
and the reviewers reproduced them (Section 10).

### 11.4 Runs of the round-3 revision (2026-10-03)

Commands below used `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1`, with paths relative to the working directories stated.
Only existing records and certificates were analyzed; no experiments or CI checks ran.

| Working directory / command | Outcome |
| --- | --- |
| `code/`: `timeout 120 python3 certify_embed_brackets.py > ../logs/certify_embed_brackets_rev3.log 2> ../logs/certify_embed_brackets_rev3.stderr` | Exit 0, ALL PASS; all three cost-one checks and existing brackets reproduce; rational certificates printed. Two numerical SDP accuracy warnings are retained in stderr; the final certificates are checked exactly. |
| `code/`: `timeout 120 python3 analyze.py > ../logs/analysis_rev3.log` | Exit 0; existing numerical results unchanged, with factor-16 values added. |
| `reviews/r3-code/`: `timeout 120 python3 r3_lpstats.py ../../logs .. > ../../logs/lpstats_rev3_confirmation.log` | Exit 0; the unchanged independent reviewer script confirms the factor-16 values from the raw records. This rerun is not a new independent review of the revision. |
| Repository root: inline `timeout 60 python3` log comparison | PASS: `analysis_rev3.log` differs from `analysis.log` only by eight factor-16 additions and two explanatory labels; all existing numbers unchanged (`logs/check_analysis_rev3.log`). |
| Repository root: inline `timeout 60 python3` using `compile()` on the changed scripts | Both `analyze.py` and `certify_embed_brackets.py` compile; no bytecode written. |
| Repository root: `GIT_OPTIONAL_LOCKS=0 git diff --check -- research-20261001/minor-sets research-20261001/multiround` | Exit 0, no whitespace errors; read-only check. |
| Repository root: inline `timeout 60 python3` scan of Python command lines and `/proc/*/cwd` | PASS: no revision analysis or certificate process remains in either stream (`logs/process_check_rev3.log`). |

### 11.5 Process hygiene

- *Original runs (2026-10-01).* They were started without a `timeout` wrapper, contrary to the
  process rule; each was bounded by construction instead. The scripts have fixed numbers of
  trials, corners, records or restarts (`exp_random.py` draws until it has the requested number
  of corners, rejecting apex draws with `det s̄ ≤ 0` and corners with infinite `z_K`, which ends
  with probability 1; the three runs needed 560–670 draws for 300 corners each). The bisection
  has a fixed number of steps; `adversarial.py` caps Nelder–Mead at `maxiter = 700` per start;
  every SCIP solve has a 60 s time limit (`exp_lp.py`, `test_core.py`) or a node limit of 1
  (`scip_probe.py`, `scip_fidelity.py`, which also caps the root rounds at 5). The jsonl outputs
  and the printed records are flushed after every record, so an interrupted run keeps its
  finished records. The scripts do not resume by themselves, but they are seeded, and every rerun
  so far (the reviewer's partial rerun of `exp_lp.py`, the certificate reruns of the review and
  of this revision) reproduced the logged records exactly, so a rerun with the same arguments
  should regenerate the same records.
- *Revision runs (2026-10-02).* All Python computations under `timeout` (Sections 11.2 and 11.3).
  In the round-2 revision every run was in the foreground, one at a time.
- *Round-3 revision (2026-10-03).* All computations used `timeout` and one BLAS/OpenMP
  thread. No background job was launched; all foreground jobs finished.
- *Background processes.* No process of this stream was running when either revision began (the
  reviewers also found none). The only background job of the round-1 revision (the instance A
  certificate; the S1 part never started) finished. The round-2 revision started no background
  process. I checked `/proc/*/cwd` before returning: no process runs in the stream directory.

## 12. Limits

- The fidelity check covers random bipartite bilinear models at the root with other separators
  off; it does not cover principal minors, `usebounds`, `usestrengthening`, or nodes. SCIP's
  safeguarding bisection in `computeRoot` was not modelled; the match to `4.5·10^-15` shows that
  it did not change any applied cut in these runs.
- The statement that `nlhdlr_quadratic` uses `C_U` for an explicit constraint
  `x_1x_4 − x_2x_3 = 0` rests on source reading only; no run tested it.
- Numerical family bounds are certified lower bounds (explicit sets) in floating point; "attains"
  uses the tolerance `10^-5`. Exact two-sided certificates exist for instances A, B, S1
  and the three embedded sfree instances (orbit brackets). The 12 adversarial corners
  and 12 random misses, rounded to rationals, have exact one-sided ratio upper bounds;
  their lower bounds from explicit sets are numerical.
- The frequencies of Section 7.1 (orbit misses in about 1–2% of random corners) depend on the
  Gaussian generator; the searches of Section 7.4 use biased constructions and say nothing about
  frequencies.
- The LP experiments use small random bipartite bilinear programs, the most violated minor and
  one cut; no MINLPLib or QPLIB instances and no experiments inside SCIP's cutting loop. The
  LP-re-solve comparison depends on how ties among optimal sets are broken (Section 7.2). The
  samples are small (86 and 71 corners) and the differences are skewed (means and medians differ),
  so the 3×3 typical-corner gain and loss claims rest on Wilcoxon alone, with its null
  hypothesis of symmetry about 0; the adjusted sign tests do not reject there. Both claims
  survive factor-16 Bonferroni adjustment over both tests for all eight comparisons, but
  this adjustment does not remove the symmetry caveat. The 4×4 nearest-to-SCIP claim is
  supported by the sign test. The bootstrap intervals are not adjusted.
- The original runs had no `timeout` wrapper (Section 11.5); they were bounded by construction.
- The adversarial minimum is set by the imposed margins and is a heuristic upper bound on the
  worst ratio, not a lower bound.
- Minors with diagonal entries are discussed only briefly (Section 8); the support statement
  (Proposition 5) uses `S = {det = 0}`.
- Genericity in Proposition 10 is heuristic beyond the support-one case.
- The literature search was small; see Section 9.

## 13. Open questions

1. Is there a quantitative non-degeneracy condition on the optimal simplex under which the orbit
   attains `z_K` for minors (the minor version of the sfree open question)? Instance S1 shows that
   transversality alone is not enough.
2. Is the worst-case orbit ratio bounded away from 0 under the invariant margins of Section 7.3?
   The search reached `0.20` with two rays on the 1% margin.
3. Which tie-breaking rule among the sets attaining `z_K` gives good LP bounds after re-solving,
   and does any of them beat SCIP's point-rule set over several rounds inside SCIP?
4. Is the closure of the orbit family's cuts exact for minors (the Averkov–Basu–Paat-type
   question of the sfree note)?
5. For minors with a diagonal entry, which family of maximal `{det = 0, a ≥ 0}`-free sets
   attains the corresponding corner bound?
6. Does `nlhdlr_quadratic`, with intersection cuts switched on, produce exactly the `C_U` cuts
   for an explicit constraint `x_1x_4 − x_2x_3 = 0`, as the source reading says (Section 2)?
