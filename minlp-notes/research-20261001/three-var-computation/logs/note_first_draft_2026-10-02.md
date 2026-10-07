# Selective three-variable family blocks in box-QP relaxations: a computational comparison

Date: 2026-10-01 (runs finished 2026-10-02). Stream: `three-var-computation` of the
[October 1 continuation](../PROGRAM.md). Status: research note by the stream author;
not yet reviewed. "Reviewed" in this program means checked by another research agent.
Nothing here has been committed. Code: [code/](code/); raw outputs: [logs/](logs/);
instances: [data/](data/); downloaded sources: [sources/](sources/MANIFEST.md).

## Summary

**Question.** The [publication assessment](../../research-20260925/publication-quadratic-assessment.md)
asked for an experiment comparing, on box-constrained nonconvex QPs, (i) Shor + RLT
(McCormick) + triangle inequalities, (ii) Khajavirad's disjoint-support LMIs (17),
(iii) the Anstreicher–Puges SOC strengthening (14)–(16), (iv) (i)–(iii) plus selectively
separated blocks of the three-positive family of
[the family note](../../research-20260925/three-positive-family-sdp.md), and (v) the exact
Anstreicher–Burer tetrahedral DNN lift per triple. Does the selective family help beyond
existing relaxations, at lower cost than the exact lift?

**Answer in one paragraph.** It depends entirely on whether the instance has a
*triple-level* gap, and standard and generic random instances almost never have one.
On the BoxQP benchmark (`spar*`), the base relaxation (i) is tight up to numerical
accuracy on SPAR_TIGHT of the SPAR_TOTAL instances solved; on the gap instances
SPAR_GAP_LIST, no triple of the base solution lies outside the three-variable moment
hull, so no triple-level constraint (ii)–(v) can raise the bound by more than
SPAR_IMPROVE_MAX (proved perturbation bound, evaluated numerically). The same holds for
generic random instances. When a triple-level gap exists (instances built from "hard"
three-variable objectives), the family is the decisive ingredient: one family block per
violated triple closes the triple-level gap completely (to solver accuracy), (ii) closes
about 91% (three variables) or 98.5–99.7% (chains), (iii) closes 26–85%, and (ii)+(iii)
is never better than (ii) alone. The family blocks reach the bound of the exact lift at a
fraction of its cost: on chain instances with 30 to 3000 triangles the family method used
one 5×5 block per violated triangle, 4–8 times less solve time than the exact lift, and
at the largest sizes it gave the best validated (safe) bound of all methods because the
exact lift's larger SDPs were solved less accurately. Individual family cuts and
individual exact-hull cuts reach the same bound only after many rounds.

**Main results** (labels as required by the program; details in the sections cited).

1. *Exact separation tools* (proved, Section 3). (a) For a 4×4 matrix, enumerating the
   15 supports with bordered KKT systems computes `min_{v∈Δ} vᵀAv` exactly; this gives the
   most violated sum-normalized family cut, so individual cuts need no completely positive
   decomposition. (b) A 5-tetrahedron SDP computes the depth of a triple moment matrix
   outside the cube moment hull `QPB3` and a valid cut with a certified constant shift.
   (c) If every triple moment matrix of a base solution has depth at least `−ε`, then
   *any* family of constraints valid for `QPB3` on all triples raises the bound by at most
   `ε(f(y_c)−f(y*))/(1+ε)`, where `y_c` is the uniform-distribution moment point.
   (d) A Jansson-style safe dual bound, valid for every feasible point of the model as built.
2. *Standard BoxQP* (numerical evidence, Section 4.1). Base relaxation (i) with dense Shor
   block: relative gap below `10⁻⁵` on SPAR_TIGHT of SPAR_TOTAL instances; the exceptions are
   SPAR_GAP_LIST. On each exception the minimum triple depth at the base solution is
   SPAR_DEPTHS, so every triple-level method gains at most SPAR_IMPROVE_MAX, while the gap is
   SPAR_GAPS. Running all methods on `spar050-050-1` confirmed no change at all.
3. *Generic random instances* (numerical evidence, Section 4.2). Among 40,825 random
   three-variable objectives (four distributions), exactly one had a gap for (i); (ii), (iii)
   and the family each closed it. Eighteen random 30-variable instances with positive
   diagonals (dense, 2-tree and 3-tree supports): (i) was tight in all.
4. *Hard three-variable objectives* (numerical evidence, Section 4.3). For 109 objectives
   defined as the deepest `QPB3` cut at random points of (i): closure by (ii) mean 0.908
   (min 0.767), (iii) mean 0.577, (ii)+(iii) identical to (ii), family (all 24 orientations)
   1.0000 for all 109 (largest shortfall against the exact value `5.5·10⁻⁹`). With
   separation, exactly one orientation was violated at the base solution in every case and
   the single added block closed the whole gap; individual family cuts reached a median
   closure 0.9933 (min 0.9774) after 29 rounds. On 2,289 perturbed objectives and on
   POINTS_TESTED random points of (i) that satisfy all 24 family orientations, no case with
   the family weaker than the exact hull was found.
5. *Conjecture* (Section 4.3). Shor + RLT + triangle inequalities + the 24 orientations of
   the family describe `QPB3` exactly. This is consistent with, and slightly stronger
   than, Conjecture 2.9 of the parallel (unreviewed)
   [`three-var-completeness`](../three-var-completeness/note.md) note, which uses the
   disjoint-support cone instead of Shor + RLT + triangles.
6. *Chain instances* (numerical evidence, Section 4.4). Instances with `m` disjoint hard
   triangles linked by bridge edges (`n = 3m` up to 9000). Family blocks (method F) matched
   the exact-lift bound to solver accuracy on all CHAIN_COUNT instances, with one 5×5 block
   per violated triangle; the lift (method X) needed five 4×4 DNN blocks per triangle and,
   with its own hull-test selection, lifted far more triangles at larger sizes. Solve times
   at `m = 300, 1000, 3000`: F 2.3 s, 8.1 s, 26 s; X 25 s, 111 s, 201 s; (ii)+(iii) 7.3 s,
   32 s, 152 s. XF_SENTENCE
7. *Solver accuracy* (numerical evidence, Section 4.5). Clarabel (tolerance `10⁻⁸`) is
   accurate to about `10⁻⁸` relative on small models but returns `AlmostSolved` on models
   with more than a few thousand cones; safe bounds then differ from the primal objective
   by up to `5·10⁻⁵` relative. SCS_SENTENCE Every comparison stated as a difference in this
   note uses safe bounds; differences below the safe-bound slack are reported as ties.

**What this means for solvers.** The selective family is a cheap and complete-looking
replacement for the exact three-variable lift *when triple-level gaps exist*. On the
standard benchmark and on generic random instances they essentially do not, so neither
the family nor any other triple-level constraint would help there. No solver
implementation (SCIP or otherwise) was tested; nothing here shows a branch-and-bound
speedup.

## 1. Setting and notation

All problems are `min f(x) = xᵀHx + gᵀx` over `[0,1]ⁿ`. The `spar` files define
`max ½xᵀQx + cᵀx`; we use `H = −Q/2`, `g = −c`, so the minimum is minus the published
optimum. A *plus* coordinate is one with `H_ii > 0` (Khajavirad's plus loop). Relaxations
live in the moment space `(x, Y)`, `Y` symmetric, with objective `⟨H, Y⟩ + gᵀx`. For a
triple `T = (i,j,k)` let `M_T` be the 4×4 matrix `[1 x_Tᵀ; x_T Y_TT]` and
`QPB3 = conv{[1;x][1;x]ᵀ : x ∈ [0,1]³}`.

## 2. Relaxations, separation and solvers

**Base (i), `B`.** Shor block `[1 xᵀ; x Y] ⪰ 0`, McCormick inequalities for every pair
in the pattern, `Y_ii ≤ x_i`, `0 ≤ x ≤ 1`, and the four triangle inequalities per triple,
added by separation (violation `> 10⁻⁶`, at most 2000 new per round for chains and 5000 for
`spar`) until none is violated. For `spar` instances the Shor block is dense, of order
`n+1`, and McCormick covers all pairs. For chain instances the pattern is the chordal
support graph; the Shor condition is imposed on each maximal clique (triangles and bridge
edges), McCormick on pattern pairs, triangle inequalities on the triangles.

**(ii) `K`.** Khajavirad (arXiv 2601.18545v2, Theorem 3, LMIs (17)) with plus set
`P = T` and empty minus set: 8 level-3 RLT inequalities, 12 order-2 blocks (written as
rotated second-order cones), 6 order-3 PSD blocks; the order-4 block is a principal
submatrix of the Shor block and is omitted. Auxiliary moments (`x_ix_jx_k`, `x_i²x_j`,
`x_i²x_jx_k`) are registered by monomial and therefore *shared* between triples.

**(iii) `A`.** Anstreicher–Puges (arXiv 2501.09150v1) equations (14) (eight linear
inequalities in `z = x_ix_jx_k`), (15) (24 switched rotated cones) and (16) (48 switched
and permuted rotated cones). `KA` uses both, with one shared `z` per triple.

**(iv) family `F`.** For a triple, a choice of the `z` coordinate and of complements
`x_a ↦ 1−x_a` (24 orientations), the block `[1 bᵀ; b B−N] ⪰ 0` with six nonnegative
auxiliaries `N` of [the family note](../../research-20260925/three-positive-family-sdp.md),
applied to the switched moments. `KAF` adds family blocks to the converged `KA`
relaxation; `F` adds them to `B`. `KAFc` adds individual family cuts instead of blocks.

**(v) exact lift `X`.** Anstreicher–Burer, Theorem 7 (preprint in
[sources](sources/MANIFEST.md)): for `n ≤ 3` and any triangulation of the cube,
`QPB3 = {Σ_p Ā_p W_p Ā_pᵀ : W_p ∈ DNN₄, Σ_p eᵀW_pe = 1}`. We use the 5-tetrahedron
triangulation (the paper notes five suffice): five 4×4 DNN blocks and ten linking
equations per triple. `KAX` adds the lift to `KA`; `Xc` adds individual hull cuts
(Section 3.2) to `B`; `XF` adds the lift to the triples selected by the family test.

**Selection.** Every method starts from the converged `B` and alternates solve and
separation (triangles are re-separated every round), at most 200 new triples or blocks per
round (1000 for `m = 3000`), at most 25 rounds (10 for `spar`), and stops when nothing new
is violated or the bound stalls (`< 10⁻⁷` relative change over three rounds).
*K, A, KA, X, KAX, Xc*: triples with hull depth `< −10⁻⁶` (Section 3.2), most violated
first; triples with a coordinate within `10⁻⁶` of a bound are skipped (there McCormick
and Shor reduce `M_T` to a pair, where Shor + RLT is exact). *F, KAF, KAFc, XF*: all
triples in the pattern and all 24 orientations, with the exact simplex minimum
(Section 3.1) `< −10⁻⁶`; a block is added only for violated (triple, orientation) pairs,
and a cut uses the minimizing vector.

**Solvers.** Clarabel 0.11.1 (interior point; gap and feasibility tolerances `10⁻⁸`,
one thread) for all main runs; SCS 3.3.1 (first order, `eps_abs = eps_rel = 10⁻⁵`
and `10⁻⁶`) for the accuracy comparison. Both are called directly through a small
modeling layer ([code/conic.py](code/conic.py)). Reference optima: published values for
`spar`; Gurobi 13.0.2 (`NonConvex=2`, one thread, `MIPGap=10⁻⁶`, 1800 s) and a block
coordinate descent heuristic with exact three-variable subproblems
([code/ub_local.py](code/ub_local.py)) for chains. All timings were taken on a shared
36-core machine with load average near 200 (other agents); they are comparable within a
run of `driver.py` but not reproducible in absolute terms.

## 3. Separation tools and validation (proved)

### 3.1 Exact family separation

For an orientation, the family is violated at `(x, Y)` exactly when `A = B − bbᵀ` is not
copositive ([family note](../../research-20260925/three-positive-family-sdp.md), Theorem),
that is, when `μ(A) := min{vᵀAv : v ≥ 0, Σv = 1} < 0`. A minimizer `v` gives the most
violated sum-normalized family cut, with parameters `(d₁,d₂,d₃,k) = v` and `h = −bᵀv`,
of value `μ(A)`.

**Lemma 1.** For a symmetric 4×4 matrix `A` and nonempty `S ⊆ {1,…,4}`, let `K_S` be the
bordered matrix `[A_SS 1; 1ᵀ 0]`. Then `μ(A)` is the minimum of `v_SᵀA_SSv_S` over all
`S` such that `K_S` is nonsingular and the solution of `K_S(v_S, ν) = (0, 1)` has
`v_S ≥ 0`.

*Proof.* Every listed candidate is feasible, so the minimum over candidates is at least
`μ(A)`. Conversely, let `v*` be a minimizer with the smallest support `S`. It lies in the
relative interior of the face `Δ_S`, so first-order optimality in the affine hull of the
face gives `A_SSv*_S = λ1` for some `λ`; hence `(v*_S, −λ)` solves the bordered system.
If `K_S` is nonsingular the solution is unique, so `v*` is a candidate. If `K_S` is
singular there is `(d, ν) ≠ 0` with `A_SSd + ν1 = 0` and `1ᵀd = 0`; then `d ≠ 0`. Along
`v*_S + td`, which stays in the affine hull of the face, the objective changes by
`2t dᵀA_SSv*_S + t² dᵀA_SSd = 2tλ·1ᵀd − t²ν·1ᵀd = 0`. Moving along `±d` until a
coordinate reaches zero gives a minimizer with smaller support, a contradiction. ∎

The implementation ([code/relax.py](code/relax.py), `stqp_min`) evaluates the 15
supports in floating point, skipping nearly singular `K_S`; a cut is valid for *any*
`v ≥ 0`, so floating-point error affects only which cut is found, never validity.

### 3.2 Exact hull depth and certified hull cuts

**Lemma 2.** Let `Ā_p` (`p = 1,…,5`) be the vertex matrices of a triangulation of the
cube and `M_c` the moment matrix of the uniform distribution on `[0,1]³`. Define
`δ(M) = min{⟨C, M⟩ : Ā_pᵀCĀ_p − N_p ⪰ 0, N_p ≥ 0 with zero diagonal, ⟨C, M_c⟩ = 1}`.
Then the feasible `C` are exactly the matrices of quadratics `q_C(x) = [1 xᵀ]C[1; x]`
that are nonnegative on the cube with `⟨C, M_c⟩ = 1`, and `δ(M) < 0` if and only if
`M ∉ QPB3` (for `M` with `M₀₀ = 1`). Moreover `(M + |δ|M_c)/(1+|δ|) ∈ QPB3` whenever
`δ = δ(M) < 0`.

*Proof.* A point of tetrahedron `p` is `Ā_pλ` with `λ` in the simplex, so
`q_C ≥ 0` on the cube iff each `Ā_pᵀCĀ_p` is copositive, iff (Diananda's theorem,
`COP₄ = PSD₄ + N₄`) it is PSD plus entrywise nonnegative; a nonnegative diagonal part can
be moved into the PSD part. `QPB3` is a compact convex set, so by the bipolar theorem
`M ∈ QPB3` iff `⟨C, M⟩ ≥ 0` for all cube-nonnegative `C`; since `M_c` is in the interior
of `QPB3`, every nonzero such `C` has `⟨C, M_c⟩ > 0` and can be normalized. If `δ < 0`
then `⟨C, M + |δ|M_c⟩ ≥ δ + |δ| = 0` for every normalized `C`, which gives the last
claim. ∎

For the cut extracted from an approximate optimal `C` we add the constant
`s = max(0, −min_p μ(Ā_pᵀCĀ_p))` (Lemma 1 on each tetrahedron); `q_C + s ≥ 0` on the
cube holds exactly whenever the five values `μ` are computed exactly, and up to
floating-point error otherwise ([code/hullsep.py](code/hullsep.py), `certify_cut`).
The test suite checks `δ(M_c) = 1`, `δ ≥ −10⁻⁷` at random rank-one cube points, and
`δ < 0` at the counterexample point of 2026-09-25 ([code/test_basic.py](code/test_basic.py)).

### 3.3 A bound on what triple-level constraints can gain

**Lemma 3.** Let `y*` be feasible for a relaxation `R ⊇ B` whose constraints are convex
and satisfied by the moment vector `y_c` of the uniform distribution on `[0,1]ⁿ`. Let `𝒯`
be a set of triples, `ε ≥ max_{T∈𝒯} max(0, −δ(M_T(y*)))`, and let `R'` be `R` plus any
constraints on the triples of `𝒯` that are satisfied whenever `M_T ∈ QPB3` (allowing
auxiliary variables per triple). Then
`min_{R'} f ≤ (f(y*) + ε f(y_c))/(1+ε) = f(y*) + ε(f(y_c) − f(y*))/(1+ε)`.

*Proof.* `y_ε = (y* + εy_c)/(1+ε)` is feasible for `R` by convexity, and
`M_T(y_ε) = (M_T(y*) + εM_c)/(1+ε) ∈ QPB3` for `T ∈ 𝒯` by Lemma 2 (when `ε` exceeds
`|δ|`, mix the point of Lemma 2 with `M_c`, which stays in `QPB3`). Each per-triple
system is therefore satisfiable at `y_ε`, so `y_ε` is feasible for `R'`. ∎

This covers the family (no auxiliaries), the exact lift (auxiliaries by Theorem 7),
(14)–(16) (auxiliary `z` = the trilinear moment of a representing measure) and Khajavirad's
system *with unshared auxiliaries*. It does not cover `K` as implemented, whose auxiliary
moments `x_i²x_j` are shared between triples; with sharing, `K` is not a purely
triple-level constraint. Applying Lemma 3 to a numerically computed `y*` assumes that
`y*` is feasible; Clarabel's reported primal infeasibility is listed with each use.

### 3.4 Safe dual bounds

Clarabel and SCS solve `min qᵀx` s.t. `Ax + s = b`, `s ∈ K`. For any `z' ∈ K*` and every
feasible `x` with `lo ≤ x ≤ hi`, `qᵀx ≥ −bᵀz' + Σ_i min(r_ilo_i, r_ihi_i)` with
`r = q + Aᵀz'` (weak duality). We take `z'` to be the solver's dual projected onto `K*`
(eigenvalue clipping plus a shift of `64k·2.2·10⁻¹⁶·‖Z‖` for an order-`k` block, cone
projection for second-order cones) and subtract a priori rounding bounds
(`10⁻¹⁴·(|A|ᵀ|z'| + |q|)` per component). All model variables are moments of points of
the cube or auxiliaries with explicit bounds (`N ∈ [0,3]` is implied by the block, but is
also stated explicitly; tetrahedron weights lie in `[0,1]` by the normalization), so the
bound is valid for every feasible point of the model as built. This is careful floating
point, not interval arithmetic. "Safe bound" below always means this number.

## 4. Results

RESULTS_PLACEHOLDER

## 5. Comparison with earlier notes and prior work

COMPARISON_PLACEHOLDER

## 6. Checks actually run

CHECKS_PLACEHOLDER

## 7. Limits

LIMITS_PLACEHOLDER

## 8. Open questions

OPEN_PLACEHOLDER
