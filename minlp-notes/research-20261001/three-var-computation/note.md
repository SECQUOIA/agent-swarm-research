# Selective three-variable family blocks in box-QP relaxations: a computational comparison

Date: work began 2026-10-01 and continued through 2026-10-03. Stream: `three-var-computation` of
the [October 1 continuation](../PROGRAM.md). Final status (2026-10-04):
reviewed in two rounds; r2 minor fixes applied; the last revision's fixes checked
by the coordinating agent (bound arithmetic and closeout checks); not refereed. The [round-2 review](reviews/review-r2.md) confirmed all nine
round-1 fixes and required four new minor fixes, addressed here. "Reviewed" in this program means checked
by another research agent, not journal peer review. This stream was swept into
repository commits made outside this program; this revision makes no commit or git
state change. Code: [code/](code/); raw
outputs: [logs/](logs/); instances: [data/](data/); downloaded sources:
[sources/](sources/MANIFEST.md).

The first author agent of this stream was stopped by an account usage limit on
2026-10-02 at about 00:30 EDT (04:30 UTC) with sections 4 to 8 of this note unwritten.
Its background jobs kept running until 08:47 EDT and finished normally. This version
was written by a second author agent, which checked the earlier outputs (Section 6.1),
kept the valid ones, and ran the missing experiments. Where this note changes an earlier
statement of the first draft, the change is listed in Section 6.2. An author closeout on
2026-10-03 incorporated late outputs and corrected the summary; those revisions are
listed in Section 6.4. The changes after review round 1 are listed in Section 6.5
and were confirmed in round 2. The new revision is listed in Section 6.6;
it has not been independently re-reviewed; the coordinating agent checked its fixes.

## Summary

**Question.** The [publication assessment](../../research-20260925/publication-quadratic-assessment.md)
asked for an experiment comparing, on box-constrained nonconvex QPs, (i) Shor + RLT
(McCormick) + triangle inequalities (`B`), (ii) Khajavirad's disjoint-support LMIs (17)
(`K`), (iii) the Anstreicher–Puges SOC strengthening (14)–(16) (`A`), (iv) (i)–(iii) plus
selectively separated blocks of the three-positive family (`F`, `KAF`; individual cuts
`KAFc`), and (v) the exact Anstreicher–Burer tetrahedral lift per triple (`X`). Does the
selective family help beyond existing relaxations, at lower cost than the exact lift?

**Answer.** The family helps on constructed instances with *triple-level* gaps and is
cheaper there than the exact lift. The natural-instance results are mostly negative,
with the deepest `spar` residues explained by unenforced triangles of `B` itself.
One small gap in the AP variant prevents a blanket claim that these generators have
no triple-level gaps.

- On the BoxQP benchmark, on 18,000 small dense instances from the same generator, and
  on random sparse instances in which every triple has three positive diagonal
  coefficients (`n` up to 3000), the audits mostly place the `B` solution inside the
  three-variable moment hull `QPB3`, up to numerical error. A proved lemma (Lemma 3) then
  bounds what *any* triple-level constraint can add, including the family, the exact
  lift and the Anstreicher–Puges cones. The strict re-audit of `spar090-075-1`,
  first computed by the reviewer and reproduced after round 1, gives a computed
  minimum depth `−8.10·10⁻⁹`, not the exact minimum. The Lemma 3 gain term at
  the computed depths is 0.045% of the safe-bound gap (0.54% with the
  primal-to-safe margin). A triangle residual forces the exact minimum to be at most
  `−1.4164750622436273·10⁻⁸`, giving a gain term of at least about 0.079%
  (0.58% with margin). If the exact minimum is at least `−10⁻⁷`, the term is at
  most about 0.56% (1.05%); if each computed depth overestimates the exact depth
  by at most `10⁻⁷`, the corresponding limits are about 0.60% (1.10%).
  The old 70.01% figure was caused by a triangle of `B` left violated by
  `3.149·10⁻⁶`. These are numerical estimates, not certified bounds; Section 4.1
  distinguishes the strict audit from the original 17 audits and explains their residues.
  Khajavirad's LMIs with auxiliary moments shared between
  triples, which the lemma does not cover, were added to all 19,600 triples of
  `spar050-050-1` and changed the bound by `4·10⁻⁷` against a gap of 1.72. On the
  18,000 `spar`-style small dense instances and on most random sparse instances `B`
  was already tight; the AP variant has one gap among 12,000 instances, relative
  `3.6·10⁻⁶`. It does not reproduce Anstreicher–Puges's 12 gap instances; the negative
  result is limited to this generator (Section 4.2).
- On instances built to have triple-level gaps (hard three-variable objectives;
  disjoint hard triangles joined by bridge edges; hard triangles sharing vertices; up
  to 9000 variables), the family is the decisive ingredient. Family blocks reached the
  exact-lift bound to solver accuracy on every instance; `K` + `A` stopped 0.31 to 3.73
  percentage points of the gap short of it; `KAF` was never better than `F` alone. `F`
  used the smallest SDP among the methods reaching that bound: one 5×5 block per
  violated triple. Logged Clarabel wall-clock solve times on a loaded machine favor
  `F` by factors 1.1 to 14 over `X` (26 s against 201 s at 9000 variables); these
  factors are indicative and vary with load. On chains, most of this advantage
  comes from `X`'s hull-depth selection lifting extra triples (2999 against 1051
  family blocks at `m = 3000`). On cacti, block type accounts for most of the
  advantage: `XF`, the exact lift using family selection, took 2.1 to 5.7 times
  `F`'s solve time within the same run.
  `XF`, the exact lift on family-selected triples, has logged times sometimes up
  to about four times smaller than `F` in separate chain runs. There were 1.02 orientations per
  violated triple on average, so the 24 orientations did not inflate the size.
  Individual family cuts and
  individual exact hull cuts reached the same bound only after many rounds.
- When the hard triangles share edges (2-trees and 3-trees), the triple-level gap
  is mostly absent: tested methods closed at most 0.514% of the gap.

So the constructed-instance evidence supports the family as a cheap replacement for the
exact three-variable lift; completeness remains a conjecture. We found little evidence
of useful gains on natural instances, with the AP exception discussed in Section 4.2.
The largely negative benchmark results agree with Anstreicher
and Puges, who saw no improvement from their constraints on `spar050-050-1` and on
similar gap instances; our audit explains the `spar050-050-1` observation. No solver integration or
branch-and-bound was tested.

**Main results.**

1. *Separation tools* (proved, Section 3): exact family separation by 15 bordered
   systems (Lemma 1); exact hull depth and certified hull cuts (Lemma 2); the
   triple-level gain bound (Lemma 3); a safe dual bound (Section 3.4).
2. *`spar`* (numerical evidence, Section 4.1): `B` is tight (relative gap `< 10⁻⁶`) on 82
   of 99 instances. In the strict re-audit of `spar090-075-1`, the computed minimum
   over 117,480 triples is `−8.10·10⁻⁹`; the gain term at the computed depths is
   0.045% of the gap (0.54% with margin). The exact minimum is at most
   `−1.4164750622436273·10⁻⁸`, so its gain term is at least about 0.079%
   (0.58%). An exact minimum at least `−10⁻⁷` gives limits about 0.56% (1.05%);
   depth overestimation at most `10⁻⁷` gives about 0.60% (1.10%). These
   conditions are not certified. The four original depths below `−10⁻⁶`
   are normalized triangle violations, not evidence of a triple-level gap.
   The other original residues and strict-audit coverage are discussed in Section 4.1.
3. *Small dense* (numerical evidence, Section 4.2): `B` tight on all 18,000 `spar`-style
   instances from this generator. The AP variant has one gap in 12,000 instances,
   relative `3.6·10⁻⁶`; the targeted check
   confirms that `KA` and two family blocks close it, with no extra family gain
   beyond `KA`.
4. *Random sparse plus instances* (numerical evidence, Section 4.3): no triple outside
   `QPB3` beyond numerical error (depth `≥ −3·10⁻⁷`); `B` tight on 13 of 16;
   stored Lemma 3 gain term `≤ 0.033`.
5. *Three variables* (numerical evidence, Section 4.4): on 109 hard objectives, `K` closes
   on average 91% of the gap, `A` 58%, `KA` = `K`, and `F` 100%; one family block per
   objective suffices. 256,556 random points of `B` that satisfy all 24 orientations
   were all inside `QPB3`. **Conjecture 1**: `B` + the 24 orientations = `QPB3`; it
   implies the three-positive completeness conjecture (Conjecture 2.11) of the parallel
   completeness note, using its stated equivalence with the capped moment relaxation.
6. *Constructed instances* (numerical evidence, Section 4.5): as in the second bullet
   above. `F` reaches the exact-lift bound; overlap along edges leaves little
   triple-level gap.
7. *Solver accuracy* (numerical evidence, Section 4.6): Clarabel is accurate to `10⁻⁸` on
   small models and returns `AlmostSolved` on large ones; the exact lift degrades first.
   SCS (`10⁻⁶`) gives the same safe bounds to `1.3·10⁻⁷` on the `m = 300` comparison
   except for the less accurate Clarabel `X` bound; on `m = 1000` it confirms the
   `F`/`X` tie while being much slower (Section 4.6).
   Tabulated bound comparisons use safe dual bounds; primal diagnostics are identified.

**What this means for solvers.** Little, at present. A solver would gain from
three-variable cuts only on problems with triple-level gaps at the nodes it solves,
and we found only one clear example in the natural generators, already closed by `KA`.
On the constructed instances, family blocks use the smallest SDP among methods
consistently reaching the exact-lift bound. Whether this helps after branching remains
untested.


## 1. Setting and notation

All problems are `min f(x) = xᵀHx + gᵀx` over `[0,1]ⁿ`. The `spar` files define
`max ½xᵀQx + cᵀx`; we use `H = −Q/2`, `g = −c`, so the minimum is minus the published
optimum. A *plus* coordinate is one with `H_ii > 0` (Khajavirad's plus loop). Relaxations
live in the moment space `(x, Y)`, `Y` symmetric, with objective `⟨H, Y⟩ + gᵀx`. For a
triple `T = (i,j,k)` let `M_T` be the 4×4 matrix `[1 x_Tᵀ; x_T Y_TT]` and
`QPB3 = conv{[1;x][1;x]ᵀ : x ∈ [0,1]³}`. A *triple-level* constraint is a constraint on
the moments of one triple, possibly with auxiliary variables of its own, that every
`M_T ∈ QPB3` satisfies. The family blocks (iv), the exact lift (v) and the
Anstreicher–Puges constraints (iii) are triple-level. Khajavirad's LMIs (ii) are
triple-level only if their auxiliary moments are not shared between triples (Section 3.3).

## 2. Relaxations, separation, solvers and instances

**Base (i), `B`.** Shor block `[1 xᵀ; x Y] ⪰ 0`, McCormick inequalities for every pair
in the pattern, `Y_ii ≤ x_i`, `0 ≤ x ≤ 1`, and the four triangle inequalities per triple,
added by separation with threshold `10⁻⁶` (`10⁻⁷` in the original audits of Section 4.1,
which allow an earlier stop with small residual violations; `10⁻⁸` without that
early stop in the strict re-audits). For `spar` and the small
dense instances the Shor block is dense, of order
`n+1`, and McCormick covers all pairs. For the sparse instances (random plus, chains,
cacti, hard-triangle k-trees) the pattern is a chordal graph containing the support of
`H`; the Shor condition is imposed on each maximal clique, McCormick on pattern pairs, and
triangle inequalities on the triples inside cliques ("clique triples"). Family blocks,
lifts and cuts are also applied only to clique triples, so no moment outside the pattern
is introduced.

**(ii) `K`.** Khajavirad (arXiv 2601.18545v2, Theorem 3, LMIs (17)) with plus set
`P = T` and empty minus set: 8 level-3 RLT inequalities, 12 order-2 blocks (written as
rotated second-order cones), 6 order-3 PSD blocks; the order-4 block is a principal
submatrix of the Shor block and is omitted. Auxiliary moments (`x_ix_jx_k`, `x_i²x_j`,
`x_i²x_jx_k`) are registered by monomial and therefore *shared* between triples. The
system is valid for every triple (each LMI is a localized moment matrix with a factor
that is nonnegative on the cube), so it is also applied to triples that are not plus.

**(iii) `A`.** Anstreicher–Puges (arXiv 2501.09150v1) equations (14) (eight linear
inequalities in `z = x_ix_jx_k`), (15) (24 switched rotated cones) and (16) (48 switched
and permuted rotated cones). `KA` uses both, with one shared `z` per triple.

**(iv) family `F`.** For a triple, a choice of the `z` coordinate and of complements
`x_a ↦ 1−x_a` (24 orientations), the block `[1 bᵀ; b B−N] ⪰ 0` with six nonnegative
auxiliaries `N` of [the family note](../../research-20260925/three-positive-family-sdp.md),
applied to the switched moments. `KAF` adds family blocks to the converged `KA`
relaxation; `F` adds them to `B`. `KAFc` adds individual family cuts (linear
inequalities, Section 3.1) to `KA` instead of blocks.

**(v) exact lift `X`.** Anstreicher–Burer, Theorem 7 (preprint in
[sources](sources/MANIFEST.md)): for `n ≤ 3` and any triangulation of the cube,
`QPB3 = {Σ_p Ā_p W_p Ā_pᵀ : W_p ∈ DNN₄, Σ_p eᵀW_pe = 1}`. We use the 5-tetrahedron
triangulation (the paper notes that five suffice): five 4×4 DNN blocks and ten linking
equations per triple. `KAX` adds the lift to `KA`; `Xc` adds individual certified hull
cuts (Section 3.2) to `B`; `XF` adds the lift to the triples selected by the family test.

**Selection.** Every method starts from the converged `B` and alternates solve and
separation (triangles are re-separated every round), at most 200 new triples or blocks per
round (1000 for `m = 3000`), at most 25 rounds (10 for `spar`, 15 for `m = 3000`), and
stops when nothing new is violated or the bound stalls (`< 10⁻⁷` relative change over
three rounds), with a time budget of 3600 s per method.
*K, A, KA, X, KAX, Xc*: triples with hull depth `< −10⁻⁶` (Section 3.2), most violated
first; triples with a coordinate within `10⁻⁶` of a bound are skipped (there McCormick
and Shor reduce `M_T` to a pair, where Shor + RLT is exact). *F, KAF, KAFc, XF*: all
clique triples and all 24 orientations, with the exact simplex minimum (Section 3.1)
`< −10⁻⁶`; a block is added only for violated (triple, orientation) pairs, and a cut uses
the minimizing vector. Note that the K, A and X runs use the exact hull test to select
triples. This is a stronger and more expensive selection rule than a solver would use
for these families, and it favors them; its cost is reported as separation time.

**Solvers.** Clarabel 0.11.1 (interior point; gap and feasibility tolerances `10⁻⁸`,
one thread) for the main relaxation runs; the hull-depth oracle uses `10⁻⁹`
([code/hullsep.py](code/hullsep.py), `_settings`), and tighter relaxation
tolerances are stated where used. The strict `spar090-075-1` log records
`solve_tol = 10⁻⁸` ([log](logs/strict_r1_spar090-075-1.out)).
SCS 3.3.1 (first order, `eps_abs = eps_rel = 10⁻⁵`
and `10⁻⁶`) for the accuracy comparison. Both are called directly through a small
modeling layer ([code/conic.py](code/conic.py)). Reference optima: published values for
`spar`; exact face enumeration for `n ≤ 10` ([code/small_dense.py](code/small_dense.py),
`box_min`); Gurobi 13.0.2 (`NonConvex=2`, one thread, `MIPGap=10⁻⁶`, 1800 s) where it
reported either optimality within its tolerance or a time-limit incumbent, combined
with the best value found by a block coordinate descent heuristic with
exact three-variable subproblems ([code/ub_local.py](code/ub_local.py)), started from the
`B` solution and from random points. A heuristic value is only an upper bound on the
minimum, so a gap closure computed with it is a lower estimate of the true closure. All
timings are wall clock (`time.time()` in `conic.py`) on a shared 36-core machine
(load average 12 to 200 from other agents). Methods run sequentially, so load can
change even within one `driver.py` run; the timing ratios are indicative. The
reviewer's quieter rerun of chain `m = 300`, `η = 0.3`, seed 1 reproduced the bounds
but changed `X/F` from 10.9 to 7.5 and `KA/F` from 3.2 to 1.4; the ordering
`F < KA < X` held ([reviewer log](reviews/r1-logs/chain_m300_e0.3_s1.FXKA.out)).
Chain `XF` times come from separate first-draft runs, so comparisons with `F` also
cross runs.

**Instances.**

| family | construction | sizes |
|---|---|---|
| `spar` | BoxQP benchmark (Vandenbussche–Nemhauser, Burer–Vandenbussche, Burer), 99 instances | `n` = 20 to 125, dense or 25–100% density |
| small dense | generator of the `spar` set re-implemented in numpy ([code/small_dense.py](code/small_dense.py)); same distribution, not the same random numbers | `n` = 5 to 10, densities 50, 75, 100%, 1000 seeds each |
| random plus | random k-tree (`k` = 2, 3), every `H_ii` a positive integer in `[1, d]` (`d` = 5 or 50), edge weights integers in `[−50, 50]`, `g` integers in `[−50, 50]` ([code/instances.py](code/instances.py), `plus_instance`) | `n` = 100 to 3000 (and `n` = 30 from the first draft) |
| hard objectives | for `n = 3`: the deepest valid cut separating a random point of `B` from `QPB3` (Lemma 2), used as objective ([code/hardobj.py](code/hardobj.py)); 109 objectives, all with three positive diagonal entries | `n = 3` |
| chain | `m` disjoint triangles, each with a randomly weighted, permuted and slightly perturbed hard objective; consecutive triangles joined by one bridge edge of weight `η·s·N(0,1)` (`η` = 0, 0.3, 1) | `m` = 30 to 3000 (`n` = 90 to 9000) |
| cactus | `m` hard triangles; each new triangle shares one vertex with a random earlier triangle; objectives add on shared vertices ([code/instances.py](code/instances.py), `cactus_instance`) | `m` = 30 to 1000 (`n` = 61 to 2001) |
| hard-triangle k-tree (`ht`) | random k-tree; every clique triangle receives a hard objective; 2% Gaussian noise on all coefficients | `n` = 30 to 1000, `k` = 2, 3 |

The chain, cactus and `ht` instances are constructed to contain triple-level gaps. They
measure what the family can do when such gaps exist; they are not evidence that such
gaps occur in practice.

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

**Lemma 3.** Let `R` be a convex feasible set in moment space containing the moment
vector `y_c` of the uniform distribution on `[0,1]ⁿ`, and let `y* ∈ R`. No containment
relation between `R` and `B` is needed; the applications below use `R = B` or `R = F`.
Let `𝒯`
be a set of triples, `ε ≥ max_{T∈𝒯} max(0, −δ(M_T(y*)))`, and let `R'` be `R` plus any
constraints on the triples of `𝒯` that are satisfied whenever `M_T ∈ QPB3` (allowing
auxiliary variables per triple). Then
`min_{R'} f ≤ (f(y*) + ε f(y_c))/(1+ε) = f(y*) + ε(f(y_c) − f(y*))/(1+ε)`.

*Proof.* `y_ε = (y* + εy_c)/(1+ε)` is feasible for `R` by convexity, and
`M_T(y_ε) = (M_T(y*) + εM_c)/(1+ε) ∈ QPB3` for `T ∈ 𝒯` by Lemma 2 (when `ε` exceeds
`|δ|`, mix the point of Lemma 2 with `M_c`, which stays in `QPB3`). Each per-triple
system is therefore satisfiable at `y_ε`, so `y_ε` is feasible for `R'`. ∎

The lemma holds verbatim for the sparse relaxations of Section 2 (Shor on cliques,
McCormick on pattern pairs, constraints on clique triples): the uniform moments
restricted to the pattern satisfy all their constraints, and `f(y_c) = Σ_i H_ii/3 +
Σ_{i≠j} H_ij/4 + Σ_i g_i/2` because `H` is supported on the pattern.

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

### 4.1 BoxQP benchmark (`spar`)

*Base relaxation on all 99 instances* (numerical evidence;
[code/spar_base.py](code/spar_base.py), [logs/spar_base/](logs/spar_base/), first draft,
triangle tolerance `10⁻⁶`). `B` closes the gap to the published optimum to a relative
gap below `10⁻⁶` (computed with the safe bound) on 82 of the 99 instances and below
`10⁻⁵` on 85. The 14 instances with a larger gap are listed below; they have
`n ≥ 50` and relative gaps from `1.7·10⁻⁵` to `9.4·10⁻³`. The three instances with relative
gap between `10⁻⁶` and `10⁻⁵` were re-solved with triangle tolerance `10⁻⁷` and audited
as well.

*Triple-level audit* (numerical evidence; [code/spar_audit.py](code/spar_audit.py) and,
for `spar050-050-1` and `spar080-050-1`, [code/triple_audit.py](code/triple_audit.py)
of the first draft; [logs/spar_audit/](logs/spar_audit/), [logs/audit/](logs/audit/)).
For every instance with a gap, `B` was re-solved (triangle tolerance `10⁻⁷`) and the hull
depth of *every* triple (`C(n,3)`, up to 317,750 triples) and the family value of every
triple and orientation were computed at the approximate `B` solution. The audit code
can stop with at most 50 new triangles still violated by less than `10⁻⁵`, rather than
enforcing `10⁻⁷` strictly. The following table preserves the original audit results;
it is not the strict re-audit below. It reports the stored Lemma 3 gain term
`ε(f(y_c) − B_primal)/(1+ε)`, divided by `opt − B_safe`, and the recorded residuals.
The triangle column now gives the unthresholded maximum recomputed at each saved
point (15 of 17); the other two were not saved. Original entries `0.0e+00` meant
"nothing above `10⁻⁷`", not zero: recomputed maxima reach `8.642851345719293·10⁻⁸`
at `spar125-075-2`. Ratios at the three instances whose primal value is at or above
the published optimum are labelled "solver accuracy".

| instance | n | B status | gap (opt - B safe) | rel. gap | min depth | triples with depth < -1e-6 | family min | gain term (Lemma 3) | gain term / gap | primal infeasibility | triangle violation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| spar125-075-2 | 125 | AlmostSolved | 97.4664 | 9.39e-03 | -3.3e-07 | 0 | -1.8e-08 | 3.4e-03 | 3.5e-05 | 2.0e-08 | 8.6e-08 |
| spar125-050-1 | 125 | AlmostSolved | 37.4919 | 4.03e-03 | -1.1e-06 | 1 | -2.6e-08 | 1.0e-02 | 2.7e-04 | 5.7e-08 | 2.9e-07 |
| spar100-050-1 | 100 | AlmostSolved | 13.2371 | 2.41e-03 | -1.5e-06 | 1 | -2.9e-08 | 8.6e-03 | 6.5e-04 | 3.5e-08 | 3.7e-07 |
| spar125-075-3 | 125 | AlmostSolved | 15.7517 | 1.63e-03 | -3.9e-09 | 0 | -4.6e-10 | 4.2e-05 | 2.6e-06 | 1.1e-08 | 4.2e-10 |
| spar125-025-1 | 125 | AlmostSolved | 7.2423 | 1.30e-03 | -5.2e-07 | 0 | -1.2e-08 | 2.9e-03 | 4.1e-04 | 2.0e-08 | 1.3e-07 |
| spar100-075-2 | 100 | AlmostSolved | 5.6802 | 8.41e-04 | -1.2e-07 | 0 | -9.1e-09 | 8.9e-04 | 1.6e-04 | 8.7e-09 | 3.6e-08 |
| spar100-050-2 | 100 | AlmostSolved | 4.5228 | 7.71e-04 | -1.4e-06 | 1 | -4.6e-08 | 8.0e-03 | 1.8e-03 | 3.0e-08 | 3.4e-07 |
| spar125-050-2 | 125 | Solved | 3.9435 | 4.70e-04 | -2.6e-09 | 0 | -4.1e-10 | 2.3e-05 | 5.9e-06 | 2.2e-08 | 3.6e-10 |
| spar125-050-3 | 125 | AlmostSolved | 1.6786 | 2.01e-04 | -5.7e-07 | 0 | -9.4e-09 | 5.1e-03 | 3.0e-03 | 1.3e-07 | 1.4e-07 |
| spar100-075-1 | 100 | Solved | 1.4412 | 1.95e-04 | -3.0e-09 | 0 | -3.9e-10 | 2.2e-05 | 1.5e-05 | 2.8e-08 | 3.3e-10 |
| spar090-075-2 | 90 | AlmostSolved | 0.7279 | 1.29e-04 | -1.1e-08 | 0 | -1.6e-09 | 6.5e-05 | 8.9e-05 | 4.7e-09 | 4.3e-09 |
| spar090-075-1 | 90 | AlmostSolved | 0.1083 | 1.73e-05 | -1.3e-05 | 1 | -1.6e-09 | 7.6e-02 | 7.0e-01 | 5.3e-09 | 3.1e-06 |
| spar050-050-3 | 50 | AlmostSolved | 0.0026 | 1.25e-06 | -5.3e-07 | 0 | -3.6e-08 | 1.0e-03 | solver accuracy | 2.8e-08 | 1.3e-07 |
| spar040-050-2 | 40 | AlmostSolved | 0.0004 | 2.93e-07 | -5.1e-08 | 0 | -5.7e-09 | 8.0e-05 | solver accuracy | 7.4e-09 | 2.1e-08 |
| spar050-030-3 | 50 | AlmostSolved | 0.0002 | 1.44e-07 | -7.3e-08 | 0 | -4.5e-09 | 1.1e-04 | solver accuracy | 2.7e-09 | 2.0e-08 |
| spar080-050-1 | 80 | AlmostSolved | 3.8083 | 1.10e-03 | -7.7e-08 | 0 | -4.4e-09 | 2.9e-04 | 7.7e-05 | 7.0e-09 | not recorded |
| spar050-050-1 | 50 | Solved | 1.7196 | 1.43e-03 | -1.0e-09 | 0 | -1.4e-10 | 1.6e-06 | 9.1e-07 | 3.9e-09 | not recorded |

The original minimum depths range from `−1.259445456487625·10⁻⁵`
(`spar090-075-1`) to `−9.97334192433231·10⁻¹⁰` (`spar050-050-1`). The old largest
gain term / gap, `0.7000998651113319` (70.01%), used gain term
`0.07583937923992252` and gap `0.10832651600048848`. It is an artefact of the
early stop: the deepest triple (35, 79, 84, zero-based) violates a triangle of `B`
by `3.149166874182041·10⁻⁶`. A triangle quadratic has uniform mean `1/4`, so its
normalized value is `−4 ×` its violation. The reviewer's independent six-tetrahedron
lift gives this depth to six digits for all four original triples deeper than
`−10⁻⁶` (`spar090-075-1`, `spar100-050-1`, `spar100-050-2`, `spar125-050-1`;
[independent depths](reviews/r1-logs/check_argmin_triples.out)). The stream's approximate
depths are slightly less negative. In 9 of 15 audits with saved points, the deepest
triple is the triple of the most violated triangle; the depth is 0.89 to 1.00 times
`−4 ×` that violation. At triangle-feasible triples, the remaining depths reach
`−2.1·10⁻⁷`, comparable to the original maximum primal infeasibility
`1.330910265919611·10⁻⁷`. These residues do not establish a gap from feasible `B`
to `QPB3`.

The diagonal caps explain much of the bulk residue near `−10⁻⁷`. The cap
quadratic `x_i − x_i²` has uniform mean `1/6`, so a residual `c = Y_ii − x_i > 0`
forces exact depth at most `−6c` on any triple containing that coordinate. At the
original `spar125-050-1` point, all 125 caps are exceeded, by up to
`3.1769669943393364·10⁻⁸`. The most negative cap bound on triangle-feasible
triples is `−1.9061801966036018·10⁻⁷`, against computed minimum
`−2.115115002092672·10⁻⁷`; median computed depth is
`−1.8209418811132055·10⁻⁷`, and 317,740 of 317,750 triples have computed
depth below `−10⁻⁷`. These are residuals of `B` itself.

*Strict re-audit (reviewer-computed and reproduced after round 1).* The reviewer added the violated triangles at
`spar090-075-1` and re-solved until none exceeded `10⁻⁸` (12,020 triangles;
primal infeasibility `2.0244254634099907·10⁻⁹`). Over all 117,480 triples, the computed
minimum depth is `−8.099999618590586·10⁻⁹`, with no computed depth below `−10⁻⁷`.
The gain term evaluated at these computed depths is
`4.877596495809501·10⁻⁵`, or `0.0004504907625087902` of the gap (0.045%). Adding
`B_primal − B_safe` gives `0.00542305494272709` (0.54%). The primal value changes
by less than `10⁻⁹` relative, so the large original ratio came from the depth term,
not a change in the relaxation. Sources: [reviewer strict code](reviews/r1-code/spar090_strict.py),
[strict JSON](reviews/r1-logs/spar090_strict.json),
[strict solve and audit log](reviews/r1-logs/spar090_strict.out). The round-1 revision's fresh
solve and all-triple audit reproduced the primal value, safe bound, computed minimum depth and
gain ratios exactly, in 558.60 s. No strict
audit was rerun after round 2. Its unthresholded maximum triangle violation is
`3.5411876556090682·10⁻⁹`, so the reviewer's logged zero also means below its
`10⁻⁸` separation tolerance. Code: [code/strict_spar_audit.py](code/strict_spar_audit.py);
outputs: [logs/strict_r1/spar090-075-1.json](logs/strict_r1/spar090-075-1.json),
[solve and audit log](logs/strict_r1_spar090-075-1.out).

The computed minimum is provably not the exact minimum at this saved point.
At triple (0, 11, 47), the triangle residual `3.5411876556090682·10⁻⁹`
forces exact depth at most `−1.4164750622436273·10⁻⁸` (about `−1.42·10⁻⁸`).
The stored depths exceed the exact triangle or diagonal-cap upper bounds by more
than `10⁻⁹` on 73,615 triples, by up to `9.674490005331274·10⁻⁸`.
Thus the 0.045% figure is a value at computed depths, not an exact-depth bound.
The gain term formed from the exact minimum is at least
`0.07877888358541404%` of the gap (`0.5760353012942764%` with margin),
or about 0.079% (0.58%). This lower bound is on the gain term in Lemma 3,
not on the improvement achieved by adding constraints.

The upper estimate depends on the assumption. If the exact minimum is at least
`−10⁻⁷`, then `ε ≤ 10⁻⁷` gives at most `0.5561614102731023%`
(`1.0534178279819646%` with margin), about 0.56% (1.05%). If instead every
stored depth overestimates its exact value by at most `10⁻⁷`, the negative
stored minimum must also be included: `ε ≤ 1.0809999961859059·10⁻⁷` gives
`0.6012104775141675%` (`1.0984668952230296%`), about 0.60% (1.10%).
Neither assumption is certified by the saved solver outputs. The round-2
review's 0.56% (1.05%) sensitivity uses `ε = 10⁻⁷`; it does not follow from
an error bound of `10⁻⁷` alone. Recalculation from saved records, without an
SDP solve: [code/r2_fix_checks.py](code/r2_fix_checks.py),
[logs/r2_fix_checks.out](logs/r2_fix_checks.out).

*Strict-audit coverage (round-1 revision).* `spar090-075-1` is the only completed
strict audit. At `spar100-050-1` and `spar100-050-2`, the round-1 revision added all
missing triangles detected above `10⁻⁸` (17 and 24, respectively). No missing
violated triangle remained, but already enforced triangles had residuals
`1.036850683089341·10⁻⁸` and `1.580930453215501·10⁻⁸`. Re-solving at tolerance
`10⁻¹⁰` returned the same points and `AlmostSolved`, so the scripts stopped with
exit 1 before hull-depth auditing; neither is claimed as a strict result. Their
saved base records and failed-run logs are in [logs/strict_r1/](logs/strict_r1/),
[100-050-1 log](logs/strict_r1_spar100-050-1.out) and
[100-050-2 log](logs/strict_r1_spar100-050-2.out).

The `spar125-050-1` attempt was stopped after about ten minutes in its first
solve, with no solved base point or hull depths produced; completing this optional
large audit was too costly for the round-1 revision. It was launched with `timeout 1800`
and stopped by sending `SIGTERM` to its timeout process; exit 143 was recorded and
its child exited. Thus all three other originally deep instances remain unaudited
strictly. Attempt records: [logs/r1_fix_audit_attempts.json](logs/r1_fix_audit_attempts.json).

The 13 original instances outside the four originally deep cases were not
re-audited strictly: `spar125-075-2`,
`spar125-075-3`, `spar125-025-1`, `spar100-075-2`, `spar125-050-2`,
`spar125-050-3`, `spar100-075-1`, `spar090-075-2`, `spar050-050-3`,
`spar040-050-2`, `spar050-030-3`, `spar080-050-1`, `spar050-050-1`. Thus the
strict computed-depth 0.045% figure is an instance-specific finding, not a uniform estimate for
all 17: one strict audit is complete and 16 remain unaudited strictly. Original audit depths and ratios remain numerical diagnostics with the
qualifications below.

On the 13 instances other than `spar090-075-1` with initial relative gap above
`10⁻⁵` (including `spar100-050-1`, `spar100-050-2` and `spar125-050-1`), the original
gain term / gap is at most `0.003035115408843456` (0.304%, `spar125-050-3`). This is
an estimate at the original approximate points, not a uniform strict result. The
three smaller-gap instances `spar040-050-2`, `spar050-030-3`, `spar050-050-3` have
primal values above the published optimum by `5.59315064947441·10⁻⁵`,
`2.4258285520772915·10⁻⁵`, `3.360297760082176·10⁻⁴`, respectively. `B` is tight
there to solver accuracy. Their former ratios 19.17%, 53.77%, 39.22% divide noise
by noise and are not evidence of appreciable triple-level gains.

All these calculations remain numerical evidence, not certified uses of Lemma 3:
the point must be feasible for `B`, including all triangles, and the computed depths
must bound the exact depths from the required side. The gain term starts at the
primal value; comparisons with `B_safe` must add `B_primal − B_safe`. Strict
triangle separation removes the misleading large residue but does not certify
feasibility or one-sided depth accuracy. The original family test selected no
orientation at tolerance `10⁻⁶` on any of the 17. Full-precision original calculations:
[logs/revision_summary.json](logs/revision_summary.json); independent recomputation:
[logs/r1_fix_spar_recompute.out](logs/r1_fix_spar_recompute.out).

*Khajavirad's LMIs with shared moments* (numerical evidence; [code/kall.py](code/kall.py),
[logs/audit/](logs/audit/)). Lemma 3 does not cover `K` when its auxiliary moments are
shared between triples, because then `K` acts as a partial higher-level lift. On
`spar050-050-1` (gap 1.72) we therefore added `K` to all 84 plus triples and,
separately, to all 19,600 triples (117,600 order-3 blocks, 235,200 rotated cones,
80,850 auxiliary moments; 937 s). The primal value moved from −1200.1286743 (`B`) to
−1200.1286740 (plus triples) and −1200.1286739 (all triples), a change of `4·10⁻⁷`
against a gap of 1.72; the safe bound of the large model is lower than that of `B`
(`AlmostSolved`). So even with sharing, the disjoint-support system adds nothing on
this instance.

*Comparison with the first draft.* The first draft ran all methods on `spar050-050-1`
([logs/spar050-050-1.out](logs/spar050-050-1.out)): no triple was selected by any
method, and every bound equals `B`. This agrees with the audit.

### 4.2 Small dense instances (`n = 5` to `10`)

Anstreicher and Puges found that the gaps of PSD+RLT+TRI on small instances are rare but,
when present, are usually closed by their constraints. We generated 18,000 instances
with the `spar` generator (re-implemented; `n = 5,…,10`; densities 50, 75, 100%; 1000
seeds each; [code/small_dense.py](code/small_dense.py),
[logs/small_dense/](logs/small_dense/)) and computed the exact optimum by face
enumeration. Result (numerical evidence): `B` was tight on all 18,000 (largest
`opt − B` over primal values `1.3·10⁻⁹` relative; largest `opt − B_safe` `2.3·10⁻⁷`
relative). Since the enumerated value is the value of a feasible point and `B_safe` is a valid
lower bound, the small difference also certifies (numerically) that the enumeration
found the optimum. No relaxation can improve on `B` for these instances.

The AP variant implements our reading of Anstreicher–Puges: the linear coefficients
are zero with probability `1 − density/100`, and the objective has no factor `½` on
the quadratic term. Our generator applies the density mask to the diagonal as well
as the off-diagonal coefficients. The paper describes `Q_ij`, `i < j`; we include
the diagonal because its non-integer optima require nonzero square terms. This choice
and the numpy random generator may differ from the paper's generator. All 12 queued
runs completed (12,000 instances; `n = 5,…,10`,
densities 50 and 75%, 1000 seeds each). There is one gap, at `n = 9`, density 75%,
seed 586 ([logs/small_dense/ap_n9_d75.jsonl](logs/small_dense/ap_n9_d75.jsonl)):
enumerated optimum `−289`, `B_primal = −289.0010386740493`,
`B_safe = −289.001039752854` (relative gap `3.597760740527601·10⁻⁶`). The original
full-family solves all returned `AlmostSolved`; `K_safe = −289.00000036298496`,
while `X_safe = −289.0028154139053` was below `B_safe` despite its near-optimal
primal value. The negative closure of that `X` safe bound reflects solver accuracy,
not a weaker exact relaxation.

This does not reproduce Anstreicher–Puges's Table 5: their 12 gap instances at
densities 50–85 have absolute gaps 0.03–0.8, whereas our single gap is about
`1.04·10⁻³` (relative `3.6·10⁻⁶`). The reviewer probed 12,000 AP-variant
instances (`n = 8, 10`; densities 50, 60, 70, 75, 80, 85; 1000 seeds each) and found
no gap above `10⁻⁵` relative ([probe code](reviews/r1-code/ap_density_probe.py),
[n = 8 output](reviews/r1-logs/ap_density_probe_n8.out),
[n = 10 output](reviews/r1-logs/ap_density_probe_n10.out)). That probe is a primal
screen, not a safe-bound audit. Density alone does not explain the mismatch. The
negative small-instance result holds for this generator, not for the paper's
unavailable instances or all random box QPs.

A targeted check of this single instance (Clarabel tolerance `10⁻¹⁰`, all 336
triangles) reproduced `B` with primal infeasibility `2.384940582044447·10⁻¹⁰`.
Among its 84 triples, two have depth below `−10⁻⁶`; minimum depth
`−0.005934413270057131`, minimum family value `−0.0006831265770813472`.
Selective separation adds two triples for `K`, `A`, `KA`, `X`, or two family blocks
for `F`, and each method needs one added-block solve. Final safe bounds:

| method | safe bound | fraction of `opt − B_safe` closed |
|---|---|---|
| K | -289.00000128 | 0.9988 |
| A | -289.00000246 | 0.9976 |
| KA | -289.00000033 | 0.9997 |
| F | -289.00000059 | 0.9994 |
| KAF | -289.00000033 | 0.9997 |
| X | -289.00004517 | 0.9566 |

All returned `AlmostSolved`; differences among `K`, `A`, `KA` and `F` are unresolved
at this accuracy, and the `X` primal value is slightly above the optimum with a looser
safe bound. `KAF` adds no family block at the `KA` point. This is numerical evidence
of a natural-generator triple-level gap, already closed by the existing methods;
it supplies no evidence of an additional family gain beyond `KA`. Code and outputs:
[code/ap_gap_audit.py](code/ap_gap_audit.py),
[logs/ap_gap_audit.json](logs/ap_gap_audit.json),
[logs/ap_gap_methods.jsonl](logs/ap_gap_methods.jsonl).

### 4.3 Random sparse instances with positive diagonals

These are the instances the task asked for: sparse, with every diagonal entry positive,
so every clique triple has three positive diagonal coefficients. Sixteen instances
(`n` = 100 to 3000, 2-trees and 3-trees, `d` = 5 and 50), plus the 18 instances with
`n = 30` of the first draft ([logs/explore_grid_n30.txt](logs/explore_grid_n30.txt):
dense, 2-tree and 3-tree supports, `d` = 5, 20, 50; Gurobi optimum; `B` was tight on
all 18). Audit at the `B` solution (numerical evidence;
[code/sparse_audit.py](code/sparse_audit.py), [logs/sparse_audit/](logs/sparse_audit/));
`U` is the best value of [code/ub_local.py](code/ub_local.py) started from the `B`
solution and from random points ([logs/ub2/](logs/ub2/)).

| instance | n | clique triples | B (safe) | U | U − B | rel. | min depth | max gain (Lemma 3) | B time (s) |
|---|---|---|---|---|---|---|---|---|---|
| plus_n100_k2_pp1_d50_s1 | 100 | 98 | -2647.0216 | -2647.0216 | 0.0000 | 6.5e-09 | -4.1e-08 | 1.3e-04 | 0.1 |
| plus_n100_k2_pp1_d5_s1 | 100 | 98 | -3950.8500 | -3950.8500 | 0.0000 | 4.2e-09 | -4.0e-08 | 1.5e-04 | 0.1 |
| plus_n100_k3_pp1_d50_s1 | 100 | 292 | -3020.3041 | -3020.3041 | 0.0000 | 4.2e-09 | -5.7e-08 | 2.0e-04 | 0.2 |
| plus_n100_k3_pp1_d5_s1 | 100 | 292 | -4326.0000 | -4326.0000 | 0.0000 | 5.0e-09 | -1.8e-07 | 7.1e-04 | 0.2 |
| plus_n300_k2_pp1_d50_s1 | 300 | 298 | -5306.5887 | -5306.5887 | 0.0000 | 1.2e-09 | -4.4e-10 | 3.9e-06 | 0.4 |
| plus_n300_k2_pp1_d5_s1 | 300 | 298 | -8371.3750 | -8371.3750 | 0.0000 | 1.5e-09 | -8.5e-09 | 8.2e-05 | 0.6 |
| plus_n300_k3_pp1_d50_s1 | 300 | 892 | -7367.0468 | -7367.0468 | 0.0000 | 4.2e-09 | -8.4e-08 | 9.2e-04 | 0.6 |
| plus_n300_k3_pp1_d5_s1 | 300 | 892 | -10205.5834 | -10205.5833 | 0.0000 | 2.7e-09 | -8.0e-08 | 9.2e-04 | 0.6 |
| plus_n1000_k2_pp1_d50_s1 | 1000 | 998 | -22888.0116 | -22887.8585 | 0.1530 | 6.7e-06 | -3.0e-07 | 9.1e-03 | 2.4 |
| plus_n1000_k2_pp1_d5_s1 | 1000 | 998 | -35145.6751 | -35145.6750 | 0.0001 | 1.7e-09 | -2.7e-07 | 9.3e-03 | 1.5 |
| plus_n1000_k3_pp1_d50_s1 | 1000 | 2992 | -31390.9489 | -31390.9488 | 0.0001 | 4.3e-09 | -9.1e-08 | 3.5e-03 | 5.8 |
| plus_n1000_k3_pp1_d5_s1 | 1000 | 2992 | -42981.6710 | -42981.6708 | 0.0002 | 4.3e-09 | -1.8e-07 | 7.8e-03 | 7.6 |
| plus_n3000_k2_pp1_d50_s1 | 3000 | 2998 | -63895.5147 | -63895.1268 | 0.3879 | 6.1e-06 | -1.2e-07 | 1.1e-02 | 23.7 |
| plus_n3000_k2_pp1_d5_s1 | 3000 | 2998 | -96110.7378 | -96110.7375 | 0.0003 | 3.2e-09 | -2.6e-07 | 2.6e-02 | 11.3 |
| plus_n3000_k3_pp1_d50_s1 | 3000 | 8992 | -86449.8360 | -86449.7042 | 0.1318 | 1.5e-06 | -2.4e-07 | 2.6e-02 | 29.5 |
| plus_n3000_k3_pp1_d5_s1 | 3000 | 8992 | -120597.0087 | -120597.0083 | 0.0004 | 3.1e-09 | -2.7e-07 | 3.3e-02 | 21.3 |

Result (numerical evidence). On every instance the minimum hull depth over all clique
triples is at least `−3·10⁻⁷`, so no triple is outside `QPB3` beyond solver accuracy, and
the stored Lemma 3 gain term for any triple-level constraint (family, exact lift,
Anstreicher–Puges) is at most `0.033`, subject to feasibility and depth accuracy (on bounds of size `10⁴` to `10⁵`). On thirteen of the
sixteen instances `B` is also tight against the heuristic value `U` (relative gap below
`10⁻⁸`, which is the solver accuracy). On the other three (`d = 50`, `n ≥ 1000`) the
difference `U − B` is 0.13 to 0.39 (relative `1.5·10⁻⁶` to `6.7·10⁻⁶`); it may be a true gap or a
weakness of the heuristic. The stored Lemma 3 gain terms are respectively 5.97%,
2.82% and 19.88% of these three gaps, subject to numerical feasibility and depth
accuracy; the draft's phrase "a few percent" was too small for the third instance.
The family separation found no violated orientation on any of these
instances, so methods F, KAF and XF would add nothing; we did not run the full method
comparison on them.

### 4.4 Three variables (`n = 3`)

For `n = 3`, `X` is exact, so every gap below is measured against the true minimum.
All constraint families are added in full (4 triangles, `K`, `A`, all 24 family
orientations). Clarabel tolerance `10⁻¹⁰`.

*Random objectives* (numerical evidence; [code/n3_study.py](code/n3_study.py), logs in
[logs/n3/](logs/n3/), summary [logs/n3_random_summary.txt](logs/n3_random_summary.txt)).
Four distributions: Gaussian `H` with `|H_ii|` (plus), Gaussian `H` (mixed), plus with
the stationary point placed inside the cube (centered), and integer data in the style of
`spar` with positive diagonal. Of 40,825 objectives (11,684 + 11,938 + 11,466 + 5,737),
exactly one had the primal diagnostic `X − B > 10⁻⁶·max(1,|X|)` (relative gap `8.5·10⁻³`, centered
distribution); `K`, `A`, `KA`, `F` and `KAF` each closed it completely. The runs were
stopped by the first author when the sample counts were large enough; the counts are what
had finished.

*Hard objectives* (numerical evidence; [code/n3_hard.py](code/n3_hard.py),
[code/hardobj.py](code/hardobj.py), pool [data/pool_hard3.jsonl](data/pool_hard3.jsonl),
summary [logs/n3_pool_summary.txt](logs/n3_pool_summary.txt)). A hard objective is the
optimal `C` of the depth problem (Lemma 2) at a random point of `B` with depth `< −10⁻⁴`;
by construction it is a worst case for `B`. All 109 pool objectives have three positive
diagonal entries. Primal gap `X − B`: median 0.072, range 0.0069 to 0.12 (the objectives are
normalized by `⟨C, M_c⟩ = 1`). The following closures use safe bounds throughout:
`(method_safe − B_safe)/(X_safe − B_safe)`; `X_safe` approximates the exact reference.

| method | mean | median | min |
|---|---|---|---|
| `K` | 0.908 | 0.918 | 0.767 |
| `A` | 0.577 | 0.581 | 0.262 |
| `KA` | 0.908 | 0.918 | 0.767 |
| `F` (24 orientations) | 1.0000 | 1.0000 | 1.0000 |
| `KAF` | 1.0000 | 1.0000 | 0.9999 |

The minimum safe closures are `0.9999826604704566` (`F`) and `0.999912428316144`
(`KAF`); the means and medians agree with the earlier primal table at the displayed
precision. A separate primal diagnostic: the largest amount by which `F` falls
below the exact reference is `5.5·10⁻⁹` (safe bound
of `X` minus the primal value of `F`), which is below the solver accuracy. `KA` equals
`K` on all 109 objectives.

*Selective separation (primal diagnostics)* ([code/n3_selective.py](code/n3_selective.py), summary by
[code/summarize_selective.py](code/summarize_selective.py)). Starting from `B` and adding
a block only for violated orientations, exactly one orientation was violated at the `B`
solution for each of the 109 objectives, and that single block closed the whole gap in
one round (largest shortfall against `X`: `−5·10⁻¹¹`, i.e. none). Adding instead the
single most violated family *cut* per violated orientation and round closed a median
0.38 of the gap after one round (min 0.054) and a median 0.9933 (min 0.9774) after 29
rounds; no objective converged within the 30-round limit.

*Search for a gap between `F` and `X`* (numerical evidence;
[code/n3_perturb.py](code/n3_perturb.py), [logs/n3_perturb.jsonl](logs/n3_perturb.jsonl);
[code/n3_probe_family_hull.py](code/n3_probe_family_hull.py),
[logs/n3_probe_family_hull.json](logs/n3_probe_family_hull.json)). (a) The 109 pool
objectives and 2,180 Gaussian perturbations of them (relative size 0.03, 0.1, 0.3, 1;
five each), 2,289 objectives with zero to three positive diagonal entries: the gap of
`F` (primal) against the safe value of `X` never exceeded `10⁻⁶` (largest `−7.7·10⁻¹⁰`, i.e. `F`
was never below `X` beyond the solver's slack). (b) 800,000 sampled points
`(x, Y = xxᵀ + GGᵀ)`, of which 256,640 satisfy McCormick and the triangle inequalities
(so they are points of `B` for `n = 3`) and 256,556 also satisfy all 24 family
orientations (simplex minimum `≥ −10⁻⁹`): the hull depth of every one of them was at
least `−6.4·10⁻⁸`, so none was found outside `QPB3`.

**Conjecture 1** (consistent with all of the above). Shor + McCormick + `Y_ii ≤ x_i` +
the four triangle inequalities + the 24 orientations of the family describe `QPB3`
exactly. Conjecture 1 implies the three-positive completeness conjecture
(Conjecture 2.11) of the parallel
[`three-var-completeness`](../three-var-completeness/note.md) note, which uses the 27
localizing matrices of the disjoint-support system plus the family LMIs in its
relaxation `R`. The needed containment is for `R ∩ {Y_ii ≤ x_i}`: the 27 matrices
do not themselves imply the diagonal caps. They contain the Shor block and imply
McCormick and the level-3 RLT inequalities
`w_{A,B} ≥ 0`, and the triangle inequalities follow from level-3 RLT (for example
`1 − Σx_i + ΣY_ij − z ≥ 0` and `z ≥ 0`). Thus
`QPB3 ⊆ R ∩ {Y_ii ≤ x_i} ⊆ B + the 24 family orientations`. If Conjecture 1 holds,
both containments are equalities. Conjecture 2.11 explicitly states its equivalence
with `QPB3 = R ∩ {Y_ii ≤ x_i}`, so the implication uses that equivalence, whose
completeness note was independently reviewed in round 1 (minor fixes), including
Proposition 2.2 and Corollary 2.4, which give this equivalence. Its
[round-2 confirmation](../three-var-completeness/reviews/review-r2.md) confirmed all
round-1 fixes; the resulting minor fixes were applied and checked by the coordinating agent. Random sampling of this kind
cannot prove completeness; it can only fail to find a counterexample.

### 4.5 Instances constructed to have triple-level gaps

Logs: [logs/chain/](logs/chain/), [logs/cactus/](logs/cactus/), [logs/ht/](logs/ht/);
full per-method tables (bound, closure, rounds, solve and separation time, blocks, model
size): [logs/table_chain.md](logs/table_chain.md),
[logs/table_cactus.md](logs/table_cactus.md), [logs/table_ht.md](logs/table_ht.md)
(`python method_table.py chain|cactus|ht`). The compact tables below
(`python compact_table.py chain|cactus|ht`) give, per instance, the best known value `U`
("opt.; tol." if Gurobi reported optimality within `MIPGap=10⁻⁶`, otherwise a feasible value, so the closure is a
lower estimate), the fraction of `U − B` closed by the safe bound of each method, the
cumulative Clarabel wall-clock solve time of the method's own rounds (KAF includes its KA stage),
the total PSD dimension `Σ k(k+1)/2`, and the number of family blocks and lifted triples.
All numbers are numerical evidence.

**Chains** (disjoint hard triangles joined by bridge edges).

| instance | U | closed KA | closed KAF | closed F | closed XF | closed X | time KA / F / X (s) | PSD dim KA / F / X | blocks F / X |
|---|---|---|---|---|---|---|---|---|---|
| chain_m30_e0.3_s1 | -81.476817 | 0.9999 | 0.9999 | 0.9999 | 0.9999 | 0.9999 | 0.21 / 0.03 / 0.14 | 906 / 654 / 1074 | 12 / 12 |
| chain_m30_e0.3_s2 | -60.326000 | 0.9883 | 0.9978 | 0.9978 | 0.9978 | 0.9978 | 0.47 / 0.14 / 0.48 | 1122 / 744 / 1374 | 18 / 18 |
| chain_m30_e0_s1 | -73.724758 | 0.9965 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.31 / 0.05 / 0.14 | 1266 / 804 / 1574 | 22 / 22 |
| chain_m30_e0_s2 | -52.864171 | 0.9853 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.36 / 0.08 / 0.11 | 1374 / 849 / 1724 | 25 / 25 |
| chain_m30_e1_s1 | -101.834130 | 0.9999 | 0.9999 | 0.9999 | 0.9999 | 0.9999 | 0.13 / 0.10 / 0.11 | 762 / 594 / 874 | 8 / 8 |
| chain_m30_e1_s2 | -82.266863 | 0.9829 | 0.9967 | 0.9967 | 0.9967 | 0.9967 | 0.46 / 0.20 / 0.58 | 942 / 669 / 1124 | 13 / 13 |
| chain_m100_e0.3_s1 | -226.807491 | 0.9445 | 0.9508 | 0.9508 | 0.9508 | 0.9508 | 1.23 / 0.16 / 0.45 | 3070 / 2209 / 3644 | 41 / 41 |
| chain_m100_e0.3_s2 | -212.961804 | 0.9994 | 0.9994 | 0.9994 | 0.9993 | 0.9994 | 1.09 / 0.38 / 0.64 | 2818 / 2074 / 3444 | 32 / 37 |
| chain_m100_e0_s1 | -190.599924 (opt.; tol.) | 0.9956 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.48 / 0.47 / 2.17 | 4402 / 2764 / 5494 | 78 / 78 |
| chain_m100_e1_s1 | -321.795455 | 0.8336 | 0.8381 | 0.8381 | 0.8381 | 0.8381 | 1.80 / 0.18 / 0.48 | 2422 / 1924 / 2744 | 22 / 23 |
| chain_m300_e0.3_s1 | -745.188950 | 0.8577 | 0.8607 | 0.8608 | 0.8607 | 0.8597 | 7.29 / 2.25 / 24.62 | 8862 / 6444 / 15944 | 110 / 223 |
| chain_m300_e0.3_s2 | -667.032313 | 0.8398 | 0.8445 | 0.8445 | 0.8445 | 0.8445 | 5.28 / 1.35 / 2.83 | 9006 / 6414 / 10644 | 108 / 117 |
| chain_m300_e0_s1 | -637.026970 | 0.9944 | 1.0000 | 1.0000 | 0.9994 | 0.9999 | 20.71 / 1.69 / 16.64 | 13362 / 8274 / 17894 | 232 / 262 |
| chain_m300_e1_s1 | -1034.156948 | 0.7348 | 0.7407 | 0.7407 | 0.7407 | 0.7406 | 11.56 / 0.59 / 8.44 | 7098 / 5664 / 8494 | 58 / 74 |
| chain_m1000_e0.3_s1 | -2501.417645 | 0.8985 | 0.9020 | 0.9021 | 0.9009 | 0.8950 | 32.03 / 8.13 / 110.62 | 30394 / 21184 / 65844 | 346 / 997 |
| chain_m3000_e0.3_s1 | -7608.806143 | 0.8847 | 0.8888 | 0.8889 | 0.8853 | 0.8807 | 152.46 / 26.20 / 201.36 | 91914 / 63759 / 197944 | 1051 / 2999 |

**Cacti** (hard triangles sharing vertices).

| instance | U | closed KA | closed KAF | closed F | closed XF | closed X | time KA / F / X (s) | PSD dim KA / F / X | blocks F / X |
|---|---|---|---|---|---|---|---|---|---|
| cactus_m30_s1 | -52.217577 | 0.8345 | 0.8718 | 0.8718 | 0.8718 | 0.8718 | 0.37 / 0.04 / 0.14 | 1272 / 705 / 1650 | 27 / 27 |
| cactus_m30_s2 | -65.845764 | 0.9204 | 0.9249 | 0.9249 | 0.9249 | 0.9244 | 0.48 / 0.05 / 0.42 | 1272 / 705 / 1750 | 27 / 29 |
| cactus_m100_s1 | -191.163294 | 0.7947 | 0.8018 | 0.8018 | 0.8017 | 0.8016 | 4.01 / 0.49 / 2.22 | 4132 / 2425 / 5500 | 95 / 90 |
| cactus_m100_s2 | -206.353843 | 0.7798 | 0.7893 | 0.7893 | 0.7892 | 0.7890 | 1.10 / 0.21 / 1.56 | 3772 / 2155 / 5950 | 77 / 99 |
| cactus_m300_s1 | -627.770669 | 0.7440 | 0.7501 | 0.7501 | 0.7497 | 0.7489 | 21.10 / 2.13 / 11.71 | 11352 / 6525 / 17200 | 235 / 284 |
| cactus_m300_s2 | -574.058465 | 0.7626 | 0.7738 | 0.7739 | 0.7738 | 0.7738 | 13.45 / 2.43 / 10.18 | 11352 / 6495 / 14650 | 233 / 233 |
| cactus_m1000_s1 | -2162.700175 | 0.7135 | 0.7207 | 0.7208 | 0.7182 | 0.7181 | 103.30 / 19.37 / 97.19 | 39376 / 22075 / 59850 | 805 / 997 |
| cactus_m1000_s2 | -2066.903378 | 0.6709 | 0.6788 | 0.6788 | 0.6776 | 0.6763 | 110.47 / 20.47 / 57.92 | 38692 / 21955 / 59650 | 797 / 993 |

**Hard-triangle k-trees** (`ht`; every triangle of a 2-tree or 3-tree carries a hard
objective, so triangles share edges). Closure of `U − B`, with `U` the best value of
Gurobi (1800 s) and the heuristic:

| instance | U | closed KA | closed KAF | closed F | closed XF | closed X | time KA / F / X (s) | PSD dim KA / F / X | blocks F / X |
|---|---|---|---|---|---|---|---|---|---|
| ht_plus_n30_k2_s1 | -55.137802 (opt.; tol.) | 0.0045 | 0.0045 | 0.0047 | 0.0047 | 0.0048 | 0.06 / 0.02 / 0.03 | 388 / 310 / 430 | 2 / 3 |
| ht_plus_n30_k3_s1 | -154.026450 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.00 / 0.00 | 405 / 405 / 405 | 0 / 0 |
| ht_plus_n60_k2_s1 | -147.786499 | 0.0046 | 0.0049 | 0.0051 | 0.0046 | 0.0041 | 0.11 / 0.06 / 0.35 | 796 / 640 / 1430 | 4 / 17 |
| ht_plus_n60_k3_s1 | -440.338625 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.00 / 0.00 | 855 / 855 / 855 | 0 / 0 |
| ht_plus_n300_k2_s1 | -786.842993 | 0.0000 | 0.0000 | -0.0000 | 0.0000 | 0.0000 | 0.35 / 0.28 / 0.37 | 3088 / 3025 / 3130 | 3 / 3 |
| ht_plus_n300_k3_s1 | -3501.161573 | 0.0011 | 0.0011 | 0.0012 | 0.0012 | -0.1017 | 2.06 / 1.55 / 67.99 | 4779 / 4545 / 35155 | 6 / 614 |
| ht_plus_n1000_k2_s1 | -4457.847891 | 0.0033 | 0.0033 | 0.0035 | 0.0036 | 0.0036 | 6.07 / 1.64 / 3.41 | 10160 / 9995 / 10080 | 1 / 2 |
| ht_plus_n1000_k3_s1 | -22099.914927 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.00 / 0.00 | 14955 / 14955 / 14955 | 0 / 0 |

The six late Gurobi references completed on 2026-10-02, 20:46–21:54
([logs/gurobi2/](logs/gurobi2/)). Bounds below are Gurobi's reported reference
bounds, not the projected conic safe bounds used elsewhere. Five runs reached their
1800 s limit; `ht_plus_n30_k2_s1` met the requested optimality tolerance. In particular,
its reported lower and upper bounds still differ by `5.513752·10⁻⁵`, so the table's
optimality label does not mean an exact certificate.

| instance | Gurobi incumbent | Gurobi lower bound | reported gap | status |
|---|---|---|---|---|
| ht_plus_n30_k2_s1 | -55.13780213003 | -55.13785726755 | 0.0001% | optimal within tolerance |
| ht_plus_n30_k3_s1 | -154.0264503119 | -154.0512998625 | 0.0161% | time limit |
| ht_plus_n60_k2_s1 | -147.7864990906 | -147.8216750225 | 0.0238% | time limit |
| ht_plus_n60_k3_s1 | -440.3386246553 | -440.3977414182 | 0.0134% | time limit |
| cactus_m30_s1 | -52.21757694301 | -52.33151352166 | 0.2182% | time limit |
| cactus_m30_s2 | -65.84576361975 | -65.86344484313 | 0.0269% | time limit |

The cactus incumbents replace `−52.203202` and `−65.683216` as `U`; the `F` closures
rise from 0.8615 and 0.7578 to 0.8718 and 0.9249. The four `ht` values do not change
the displayed closures, but the new optimality label is now retained. The completed
eight-start heuristic output also supplies `U = −2066.9033784534336` for
`cactus_m1000_s2`, whose previous row said `n/a`.

Findings.

1. *When the triples are disjoint or share only vertices, the family is the decisive
   ingredient and uses the smallest SDP.* On all 16 chains and 8 cacti, `F` (Shor + RLT +
   triangles + family blocks) reached the bound of the exact lift `X` to solver
   accuracy (largest relative difference of primal values `5.6·10⁻⁶`, at `m = 3000`, where
   `X` itself was solved less accurately). `KA` (Khajavirad + Anstreicher–Puges) stopped
   short: the family added 0.31 to 3.73 percentage points of `U − B_safe` beyond `KA` on the
   instances where `KA` was not already at the triple-level bound, which is consistent
   with the `n = 3` result that `K` closes about 91% of a triple gap and `F` closes all
   of it. `KAF` never beat `F` by more than solver accuracy, so on these instances `K` and
   `A` are redundant once the family is present.
2. *Cost.* `F` reached the triple-level bound with the smallest SDP, and less logged
   wall-clock solve time than `X`: at `m = 300, 1000, 3000` chains, 2.3, 8.1 and 26 s against 25, 111 and 201 s
   for `X` and 7.3, 32 and 152 s for `KA` (which does not reach the bound). These times
   are indicative because the shared machine's load varies; the reviewer's `m = 300`
   rerun changed `X/F` from 10.9 to 7.5 and `KA/F` from 3.2 to 1.4 while retaining
`F < KA < X` (Section 2). The `F` SDP is
   also the smallest: one 5×5 block (15 PSD entries) and six auxiliaries per violated
   triple, against five 4×4 DNN blocks (50 PSD entries, 30 nonnegativity constraints and
   ten equations) per lifted triple. The number of family blocks was about the number
   of violated triples: one orientation per triple almost always sufficed: over all separation rounds of all
   `F` runs on chains, cacti and `ht`, 7,598 violated (triple, orientation) pairs were
   found on 7,459 violated triples (1.02 per triple). `XF` (exact lift on the
   family-selected triples) reached the same bound with fewer lifted triples than `X`,
   at 0.23 to 2.05 times the wall-clock solve time of `F` on chains and 2.1 to 5.7
   times on cacti. Chain `XF` and `F` times are from separate runs: the logged
   `XF` time is sometimes up to about four times smaller, but the ratio also reflects
   changing load. On chains, most of `F`'s cost advantage over `X` comes from selection:
   the hull-depth
   selection used by `X`, `KA` and `Xc` lifted more triples than necessary at large `m`
   (2999 of 3000 at `m = 3000`, against 1051 family blocks), because at inaccurate
   intermediate points many triples have depth slightly below `−10⁻⁶`.
   On cacti, `F`, `XF` and `X` were run in the same driver invocation. There,
   `XF/F` is 2.1 to 5.7, so block type accounts for most of the advantage over
   `X`. These methods use the same family selection rule, but their successive
   iterates can select slightly different sets of triples. Raw-log recomputation
   gives `log(X/XF)/log(X/F)` from 0.65 to 1.26 on chains with `m ≥ 300`,
   and from `−0.14` to 0.47 on cacti; these indicative ratios support the
   distinction ([logs/r2_fix_checks.out](logs/r2_fix_checks.out)).
3. *Individual cuts.* Individual family cuts (`KAFc`) and individual exact hull cuts
   (`Xc`) reached the triple-level bound to 4 or 5 digits but needed 7 to 26 rounds and
   more time than the blocks; on the larger instances they stopped at the round or stall
   limits slightly below the block bound.
4. *Overlap removes the triple-level gap.* On the `ht` instances, built from the same
   hard objectives but with triangles sharing edges, the comparison runs selected
   only 0 to 7 triples at the `B` point by hull depth `< −10⁻⁶` (seven at
   `ht_plus_n300_k3_s1`; its separately solved base audit counted six). These are
   numerical detections of triples outside `QPB3`. The tested methods closed at most 0.514% of
   `U − B` (maximum 0.51365%, often 0%). The gap of these instances is mostly beyond
   triples: summing hard
   objectives over overlapping triangles produces objectives whose `B` solution is
   (almost) inside the three-variable hull of every triple. This is the same behavior as
   on `spar` (Section 4.1).
5. *Remaining gap.* On chains with `η = 0` the problem separates into independent
   triangles, so the triple-level bound is the optimum; `F` closed 1.0000 of the gap
   there (Gurobi optimality tolerance met for `m = 100`). With bridges (`η > 0`) and
   in cacti, the remaining fraction varies from below 0.1% to about 32%; for the two
   `m = 30` cacti it is now about 12.8% and 7.6%. These differences combine the
   remaining relaxation gap, heuristic error in `U`, and conic solver error. The
   final-point audits below limit further gains from constraints on all triples for
   the audited instances, subject to their numerical feasibility assumptions.

*Audit of the final family point* (numerical evidence;
[code/chain_audit.py](code/chain_audit.py), [logs/audit/](logs/audit/)). After `F`
converged, the deepest triple was at hull depth `−2.8·10⁻⁶`, `−8.1·10⁻⁶`, `−7.2·10⁻⁶`
(chains `m = 300, 1000, 3000`, `η = 0.3`), `−2.1·10⁻⁶` (cactus `m = 300`, seed 1),
`−5.2·10⁻⁶` and `−1.3·10⁻⁵` (`ht` `n = 300`, `k = 3` and `n = 1000`, `k = 2`). The
smallest family value at these points ranges from `−1.85·10⁻⁷` to `−9.55·10⁻⁷`, just inside the
separation tolerance `10⁻⁶`; at the deepest triple the ratio depth/family value (7 to 19) is in the range seen at
the rational counterexample point of 2026-09-25 (13), where the two quantities use
different normalizations. The saved cactus `m = 300` deepest triple
(185, 549, 550) has computed depth `−2.1382460870843015·10⁻⁶` and triangle
residual `5.349710845425903·10⁻⁷`, whose normalized bound is
`−2.1398843381703614·10⁻⁶`. They differ by `1.638251086059886·10⁻⁹`, so
the depth agrees numerically with a triangle residual of `B`; they are not
exactly equal. These residues reflect separation tolerance or base feasibility
residuals and are not counterexamples to Conjecture 1. The stored Lemma 3 gain terms at the final `F`
primal points are 0.0012, 0.011, 0.029 (chains), 0.0006 (cactus), 0.013 and 0.043
(`ht`). They estimate gains from the exact lift on *all clique triples* starting at
`F_primal`, not `F_safe`. Comparisons with `F_safe` must add `F_primal − F_safe`;
the resulting estimates are respectively 0.00120, 0.01124, 0.03027, 0.00071,
0.01334 and 0.04326. They require feasibility of the audited `F` points (recorded
primal infeasibility `2.97·10⁻⁹` to `5.30·10⁻⁸`) and one-sided bounds on the exact
depths. Some saved worst triples still violate triangles (for example `5.35·10⁻⁷`
at cactus `m = 300`), so these are numerical estimates, not certified gain bounds.
The `m = 3000` audit re-solved `F` separately (921 blocks); its margin and estimates
refer to that point, not the 1051-block comparison-table point.

### 4.6 Solver accuracy, safe bounds and size limits

*Clarabel* (tolerance `10⁻⁸`). On models with up to a few thousand cones it usually
returns `Solved`, and the safe bound agrees with the primal value to about `10⁻⁸`
relative. On larger models (chains with `m ≥ 300`, cacti with `m ≥ 100`, `spar` with
`n ≥ 80`) it often returns `AlmostSolved`; the safe bound is then up to `5·10⁻⁵`
relative below the primal value, and more for the exact lift on many triples (for
example `X` at `m = 3000`: primal −7613.25, safe −7613.66; `X` on `ht` `n = 300`,
`k = 3` after 614 lifted triples: primal −3503.429, safe −3503.668, primal infeasibility
up to `6·10⁻⁶`). The `X` runs degrade fastest because each lifted triple adds five DNN
blocks and ten equations that tie the lifted variables to the original moments; the
family block adds one block and no equations. Tabulated bound comparisons use safe
bounds; primal diagnostics are identified, and Lemma 3 estimates start at the audited
primal points. Differences smaller than
the gap between primal value and safe bound are reported as ties.

*SCS* (first order) on chain `m = 300`, `η = 0.3`, seed 1, methods `F`, `KA`, `KAF`,
`X` ([logs/scs/](logs/scs/)):

| method | Clarabel safe bound | SCS `10⁻⁵` safe | SCS `10⁻⁶` safe | Clarabel solve time (s) | SCS `10⁻⁶` solve time (s) |
|---|---|---|---|---|---|
| B | -749.007954 | -749.007980 | -749.007954 | 1.73 | 114.9 |
| F | -745.720718 | -745.720697 | -745.720706 | 2.25 | 148.9 |
| KA | -745.732582 | -745.732568 | -745.732520 | 7.29 | 221.6 |
| KAF | -745.720796 | -745.720759 | -745.720697 | 7.57 | 442.0 |
| X | -745.724924 | -745.720729 | -745.720714 | 24.62 | 109.2 |

Times are wall clock for the method's own solve rounds (for KAF without its KA stage),
subject to the changing-load caveat in Section 2. With
`eps = 10⁻⁶`, SCS's safe bounds agree with Clarabel's to `1.3·10⁻⁷` relative for `B`,
`F`, `KA` and `KAF`, and are slightly tighter; for `X` the SCS safe bound is 0.004
higher, because Clarabel's last `X` solve ended `AlmostSolved` with a loose dual. Each
SCS solve took 50 to 290 s. Cumulative method-round solve time at `m = 300`
was 4.4 times Clarabel’s for `X`, and about 30 to 66 times for `F`, `KA` and `KAF`.
SCS confirms the ranking: `F`, `KAF` and `X` tie, and `KA` is lower by 0.012.

The queued `m = 1000`, `η = 0.3`, seed 1 SCS comparison also completed
([logs/scs/chain_m1000_e0.3_s1_scs1e-6.jsonl](logs/scs/chain_m1000_e0.3_s1_scs1e-6.jsonl)).
At `eps = 10⁻⁶`, final safe bounds are `−2502.697709` (`F`) and `−2502.697835`
(`X`), a difference `0.000126` (`5.05·10⁻⁸` relative). Clarabel gives
`−2502.697859` (`F`) and the looser `−2502.791210` (`X`); its `X` primal value
`−2502.685743` is above both SCS primal values (about `−2502.697675`), so the
large-model `X` accuracy caveat matters. SCS's method-round solve times are 774.78 s
(`F`) and 1857.10 s (`X`), versus Clarabel's 8.13 s and 110.62 s, excluding the
shared `B` stage. The SCS run confirms the `F`/`X` bound tie; the original summary's
uniform "20 to 200 times slower" claim is too broad (`X` is 4.4 times slower at
`m = 300` and 16.8 times slower here).

*Size limits.* The largest models solved were the `m = 3000` chains (`n = 9000`): `X`
with 2999 lifted triangles (180,000 variables, 18,000 4×4 blocks) took 201 s of Clarabel
wall-clock solve time over five rounds; `KA` with 102,000 second-order cones took 152 s;
`F` took 26 s. These are loaded-machine observations.
These limits come from our implementation as much as from the solvers: the modeling
layer stores `H` as a dense `n×n` array (for `n = 30,000` this is 7 GB per copy), so the
planned `m = 10,000` chain was not attempted. Clarabel itself showed no sign of failing
at `n = 9000`; the cost of the dense `spar` relaxations is dominated by the single dense
Shor block of order `n + 1` (about 900 s per solve at `n = 125` with 15,000 to 20,000
triangle inequalities on this machine).

## 5. Comparison with earlier notes and prior work

**Earlier notes of this project.**

- The [family note](../../research-20260925/three-positive-family-sdp.md) proved
  validity and exact compact enforcement of the family and asked for "a comparison
  between adding selected family blocks, generating individual cuts, and imposing the
  established six-simplex lift". Sections 4.4 to 4.6 give that comparison. Its
  statement that the Anstreicher–Burer lift implies every family cut is consistent with
  all runs (no method ever exceeded `X` beyond solver accuracy).
- The [publication assessment](../../research-20260925/publication-quadratic-assessment.md)
  warned that "up to 24 orientations can cost more than the exact six-block
  comparator". In the runs, separation almost never needed more than one orientation
  per triple: exactly one orientation was violated for each of the 109 hard
  three-variable objectives, and on the constructed instances the number of family
  blocks was about the number of violated triples (Section 4.5). The warning is correct
  as a worst case; it did not bind here. The assessment's "no present theorem implies a
  runtime or total-size advantage" remains true: the advantage reported here is
  empirical and limited to instances with triple-level gaps.
- The lift needs only five tetrahedra (Anstreicher–Burer use six and remark
  that a triangulation with five tetrahedra is also known), not six. The earlier notes say "six"; this is
  not an error, since any triangulation works, but five blocks is the cheaper comparator
  and is the one used here.
- The parallel [`three-var-completeness`](../three-var-completeness/note.md) note,
  reviewed in two rounds, with the final minor fixes applied and checked by
  the coordinating agent, conjectures completeness of its disjoint-support
  system plus the family;
  Conjecture 1 here implies its three-positive completeness conjecture
  (Conjecture 2.11), through `R ∩ {Y_ii ≤ x_i}` and the equivalence stated there
  (Section 4.4).

**Prior work** (read from the local copies listed in [sources](sources/MANIFEST.md);
statements about papers that we did not read are marked as second-hand).

- Anstreicher and Puges (arXiv 2501.09150v1, Section 5) report that PSD+RLT+TRI is tight
  on all but one of the 54 basic `spar` instances (citing Anstreicher, Math. Prog. 136,
  2012; second-hand), that adding their ETRI and SOC constraints gave no improvement on
  the exception `spar050-050-1` or on the occasional gap instances of similar size that
  they generated, and that these constraints did close the gap on most small instances
  with `5 ≤ n ≤ 10`. Our benchmark results agree with the lack of improvement, but
  our small-instance generator does not reproduce their 12 gap instances (absolute
  gaps 0.03–0.8). Our 18,000 `spar`-style small instances were tight; the AP variant,
  which includes the diagonal, had one much smaller gap (relative `3.6·10⁻⁶`)
  closed by their constraints. The reviewer's additional 12,000-instance density
  probe found no gap above `10⁻⁵` relative (Section 4.2). The negative result is
  limited to this generator. The audit explains the lack of improvement on
  `spar050-050-1`: minimum depth `−9.97·10⁻¹⁰`, stored Lemma 3 gain term about
  `9.06·10⁻⁷` of the safe-bound gap. For the other audited instances up to `n = 125`,
  the family test selects no block at tolerance `10⁻⁶`, but the feasibility residuals
  limit certified claims. The strict `spar090-075-1` re-audit explains its old 70.01%
  ratio as an unenforced triangle, while the three small-gap ratios are numerical
  noise (Section 4.1).
- Khajavirad (arXiv 2601.18545v2) introduced the LMIs (17) and studies when they are
  exact for structured sparse problems. We used only the case `|P| = 3`, `M = ∅`.
- Anstreicher and Burer (2007 preprint; Math. Prog. 124, 2010) give the exact lift used
  as method `X`. Burer and Letchford (SIAM J. Optim. 2009; second-hand through
  Anstreicher–Puges) showed that PSD+RLT+TRI does not describe `QPB3`.
- We did not find, in the sources read for this stream, a computational comparison of
  per-triple exact lifts with selectively separated partial descriptions on instances
  with many triples. This is a statement about our reading, not a novelty claim; no
  systematic literature search was done in this stream (the
  [`intersection-literature`](../intersection-literature/) stream covers a different
  topic).

## 6. Checks actually run

All checks are targeted to this stream; no project-wide verification and no CI
inspection was done. Commands are run from `code/` with `OMP_NUM_THREADS=1` unless
stated; the batch files are in `code/` and the job lists in `data/tmp/queue_*.txt`.

### 6.1 Validation of the first draft's outputs (second author, 2026-10-02)

- Transcript of the first author parsed (last tool calls and outputs) to recover its
  commands; the commands quoted below for first-draft runs come from it.
- `python test_basic.py` → PASS family identity (sympy), PASS family nonnegative at 480
  rank-one cube points, counterexample point: family violation `−7.21·10⁻⁴`, hull depth
  `−9.22·10⁻³`; PASS rank-one depth `≥ −10⁻⁷`; depth at `M_c` = 1.0000000000000002; PASS
  triangulations. `python test_counterexample.py` → on the counterexample objective,
  `A` −0.125, `KA` −0.0281, `F`, `KAF`, `X` 0 (exact value 0).
- New: `python check_validity.py 2000 1` → all `K` and `A` constraints on two overlapping
  triples, evaluated at 2000 random finite mixtures of cube points (some coordinates at
  0 or 1), have largest violation `2.4·10⁻¹⁵`. This checks validity of our
  implementation of (17) and (14)–(16), including shared auxiliary moments.
- Implementation of `K` and `A` re-read against the local copies of the papers
  (Khajavirad Theorem 3; Anstreicher–Puges (14)–(16)): it matches.
- Code versions. `relax.py`, `conic.py`, `hullsep.py` were last changed before any
  reported run (2026-10-01 23:08). `driver.py` was changed at 00:29 on 2026-10-02 (the
  triangle loop now counts only new triangles); the chain runs before that time could
  re-solve when an already present triangle was reported violated again. Only 2 of the 727
  records of the chain logs are affected (both in `chain_m300_e0.3_s1`); bounds are unaffected
  (they are bounds of valid relaxations), round counts and times slightly.
- `spar_base`: 99 of 99 instances complete (the background job of the first author
  finished at 08:47). `chain`: 16 instances complete for all listed methods; `xf_*`: 15
  complete; SCS: both then-available runs complete; Gurobi: 6 earlier runs, 1 met the
  optimality tolerance
  (`chain_m100_e0_s1`), one (`chain_m300_e0.3_s1`) killed by the first author.
- The `ub_local.py` values of the first draft are reproduced exactly by the rewritten
  version 2 (`chain_m30_e0.3_s1`: −81.47681666562326; `chain_m100_e0.3_s1`:
  −226.80749111089995 vs −226.80749111089997).
- `summarize_n3hard.py`, `summarize_n3_random.py`, `summarize_selective.py` re-run: the
  numbers of Section 4.4 are their outputs.

### 6.2 Corrections to the first draft and to earlier notes

- First draft: "the paper notes five suffice". Anstreicher–Burer use six tetrahedra and
  remark that a five-tetrahedron triangulation is also known. Either is valid.
- First draft: "individual family cuts reached a median closure 0.9933 after 29 rounds".
  Correct, but none of the 109 runs converged; all stopped at the 30-round limit.
- First draft: "4–8 times less solve time than the exact lift" on chains. With all runs,
  the ratio of `X` to `F` solve time is 1.1 to 14 (1.1 to 4.7 at `m = 30`, 1.7 to 4.6 at
  `m = 100`, 2.1 to 14 at `m = 300`, 14 at `m = 1000`, 7.7 at `m = 3000`).
- First draft: Conjecture "slightly stronger than Conjecture 2.9" (the old numbering).
  The corrected implication is to the three-positive completeness conjecture
  (Conjecture 2.11), using the capped relaxation (Section 4.4).
- First draft, closure values relative to `U` on chains with `m ≥ 300`: the heuristic
  values used then were weaker; with version 2 of `ub_local.py` started from the `B`
  point, `U` improved for `m = 300` (`η = 1`) and `m = 3000`, so the closures in Section
  4.5 are higher than in the first draft's table.
- Earlier notes (family note, assessment): the "six-block" exact comparator can be
  replaced by five blocks; the assessment's warning that 24 orientations could cost more
  than the lift did not bind in any run (1.02 orientations per violated triple). No
  mathematical statement of the earlier notes is contradicted.

### 6.3 Commands for the reported numbers

Run from `code/`. Outcomes are summarized in the sections cited; raw outputs are in the
listed log files. "First draft" marks runs of the first author (2026-10-01/02), recovered
from its transcript.

| what | command | outcome |
|---|---|---|
| unit checks | `python test_basic.py`; `python test_counterexample.py`; `python check_validity.py 2000 1` | all pass (Section 6.1) |
| `spar` base, 99 instances (first draft) | `python spar_base.py <name> ../logs/spar_base/<name>.json` via `run_spar_rest.sh` and the first author's xargs loop | 99 complete; 82 with relative gap `< 10⁻⁶` |
| `spar` audits | `./run_spar_audit.sh` (5 parallel, `timeout 21600` each; `spar_audit.py`); first draft: `python triple_audit.py spar050-050-1 …`, `… spar080-050-1 …` | Section 4.1 table |
| `spar` table | `python audit_table.py spar` | Section 4.1 |
| `K` on all triples | `python kall.py spar050-050-1 {plus,all} ../logs/audit/kall_spar050-050-1_<kind>.json` | no change (Section 4.1) |
| `spar050-050-1`, all methods (first draft) | `python driver.py --boxqp ../sources/BoxQP_instances-master/basic/spar050-050-1.in --methods K,A,KA,KAF,KAFc,F,X,KAX,Xc --log ../logs/spar050-050-1.jsonl --max_rounds 10 --cap 500` | all bounds equal `B` |
| small dense | `python small_dense.py <n> <d> 1 1000 ../logs/small_dense/n<n>_d<d>.jsonl` (`queue_small.txt`), AP variant with extra argument `ap` (`queue_late.txt`); summary `python summarize_small.py [glob]` | Section 4.2 |
| random plus instances | `python make_plus.py <n> <k> 1 <d> 1`; `./run_sparse_audit.sh` (`sparse_audit.py`); `python audit_table.py sparse` | Section 4.3 |
| upper bounds | `python ub_local.py ../data/<t>.json <starts> 1 ../logs/sparse_audit/<t>.json.base.npz > ../logs/ub2/<t>.json` (`make_ub_queue.py`, `queue_ub.txt`, `queue_late.txt`); first draft: `run_ub_xf.sh` (`logs/ub/`) | used as `U` |
| Gurobi | `python gurobi_solve.py ../data/<t>.lp 1800 1 ../logs/gurobi2/<t>.log` (`queue_late.txt`); first draft: `../logs/gurobi/` | six late results complete: one optimal within tolerance, five time limits; reference bounds in Section 4.5; every queued Gurobi solve ran |
| `n = 3` studies (first draft) | `python n3_study.py <dist> <N> <seed> ../logs/n3/<dist>_s<seed>.jsonl` (8 runs, stopped by the first author); `python n3_hard.py {plus,any} 150 <seed> ../logs/n3hard/…` (seeds 11–14, stopped; pool = concatenation); `python n3_selective.py ../data/pool_hard3.jsonl ../logs/n3_selective.jsonl`; `python n3_perturb.py ../data/pool_hard3.jsonl ../logs/n3_perturb.jsonl <seed>`; `python n3_probe_family_hull.py 40 20000 11 ../logs/n3_probe_family_hull.json` | Section 4.4; summaries `summarize_n3hard.py`, `summarize_n3_random.py`, `summarize_selective.py` |
| chains (first draft) | `python make_chain.py <m> <eta> <seed>`; `python driver.py --json ../data/<t>.json --methods K,A,KA,KAF,KAFc,F,X,KAX,Xc --log ../logs/chain/<t>.jsonl --max_rounds 25` (`m = 1000`: `K,KA,KAF,F,X,KAX`; `m = 3000`: `F,K,KA,KAF,X,KAX --max_rounds 15 --cap 1000`); `XF`: `run_ub_xf.sh`, and for `m = 3000` `queue_late.txt` | Section 4.5 |
| cacti, `ht` | `python make_cactus.py <m> <seed>`; `python make_ht.py plus <n> <k> 1`; `python driver.py --json … --methods K,A,KA,KAF,KAFc,F,XF,X,KAX,Xc --log ../logs/{cactus,ht}/<t>.jsonl --max_rounds 25` (`queue_driver.txt`; `m = 1000`, `n = 1000`: `K,A,KA,KAF,F,XF,X`) | Section 4.5 |
| tables | `python method_table.py {chain,cactus,ht} > ../logs/table_<dir>.md`; `python compact_table.py {chain,cactus,ht}` | Section 4.5 |
| audits of the final `F` point | `python chain_audit.py ../data/<t>.json ../logs/audit/<t>.json` | Section 4.5 |
| SCS | `python driver.py --json ../data/chain_m300_e0.3_s1.json --methods F,KA,KAF,X --solver scs --scs_eps {1e-5,1e-6} …` (first draft); `… chain_m1000_e0.3_s1.json --methods F,X --solver scs --scs_eps 1e-6 --max_rounds 10 --time_budget 3000` | all three runs complete; Section 4.6 |

### 6.4 Author closeout (2026-10-03; before review round 1)

The changes below were made within this stream only. Sections 6.1–6.3 record earlier
runs; the commands in the table below are the closeout commands. This section records
what the closeout said before review; its interpretations of the 70.01% ratio and
`XF` cost are superseded by Sections 4.1, 4.5, 6.5 and 6.6. No large experiment
was rerun, no CI was inspected, and no git state was changed.

- Filled every placeholder: the two Summary ratios, the minimum-depth range, the
  count of audited instances, the full `spar` table, the AP Summary and results, and
  the `m = 1000` SCS paragraph. `revision_summary.py` retains full-precision sources
  and calculations in [logs/revision_summary.json](logs/revision_summary.json).
- Corrected the interpretation of Lemma 3. The maximum stored gain term / gap is
  70.01%, not a uniformly negligible fraction. Its feasibility assumption is not
  certified by these floating-point outputs; four audits have depths below `−10⁻⁶`
  and recorded triangle violations. The primal-to-safe-bound margin must also be
  included when comparing with `B_safe`. Updated the Summary, Sections 2, 4.1, 5 and
  7 accordingly. Fixed `audit_table.py` to exclude triangle checkpoint JSON files
  (its first closeout invocation failed on those files) and report feasibility
  residuals; the regenerated table then succeeded.
- Incorporated all six late Gurobi references, checked `.log` against `.res`, and
  regenerated all three full and compact method tables. `chain_table.gurobi_ref`
  now reads both `gurobi/` and `gurobi2/`; `compact_table.py` retains the tolerance
  qualification on optimality. The two `m = 30` cactus `U` values improved;
  `ht_plus_n30_k2_s1` now carries the optimality label. Added the six reference lower
  bounds and gaps in Section 4.5. Filled the missing `cactus_m1000_s2` value from its
  completed eight-start heuristic output, and updated the remaining-gap discussion.
- Parsed all five `data/tmp/queue_*.txt` files and their outputs: none of their
  output files is missing; all requested small-dense seeds, heuristic starts and
  driver methods have outputs. All six queued Gurobi solves ran and completed with
  a final status. The earlier `chain_m300_e0.3_s1` Gurobi run was started but killed
  by the first author and still has no final reference summary; it was not rerun.
  The unqueued `m = 10,000` chain remains unattempted for the memory reason in
  Section 4.6. The queue logs contain no detailed exit-status ledger, so completion
  was checked from the result files rather than inferred from `MASTER_DONE`.
- Summarized all 12,000 AP-variant instances and checked the sole gap at `n = 9`,
  density 75%, seed 586. This one-instance computation confirms two violated
  triples; two selective family blocks close the gap, while `KA` already closes it
  and `KAF` adds no block. Updated every blanket claim that natural instances have
  no triple-level gaps; no extra family gain beyond `KA` is established here.
- Corrected the sparse gap ratios to 5.97%, 2.82% and 19.88%, the maximum `ht` closure
  to 0.514%, and the SCS speed comparisons. The completed `m = 1000` SCS outputs
  confirm the `F`/`X` tie and show the looser Clarabel `X` bound. Qualified the cost
  claim: `F` has the smallest SDP and is faster than `X` on the constructed runs;
  `XF` can be slightly faster than `F` on some chains. Completeness remains a
  conjecture and the note remains not yet reviewed.

All commands below ran from `code/` with `OMP_NUM_THREADS=1`; the one-instance solve
also set `OPENBLAS_NUM_THREADS=1`. At most four foreground processes were used.

| what | closeout command | outcome |
|---|---|---|
| raw-output summary and queue audit | `timeout 60 python revision_summary.py > ../logs/revision_summary.out` | 17 `spar` audits; six Gurobi `.log`/`.res` pairs agree; 18,000 and 12,000 small-dense records; no missing queued output |
| AP batch summary, read-only | `timeout 60 python summarize_small.py '../logs/small_dense/ap_*.jsonl'` | 12,000 records; one gap; old `X_safe` below `B_safe` reflects inaccurate dual |
| single AP gap check | `timeout 300 python ap_gap_audit.py > ../logs/ap_gap_audit.out 2>&1` | completed in under one second; reproduced `B`, audited all 84 triples, compared six selective methods; outputs in `logs/ap_gap_*` |
| `spar` table | `timeout 60 python audit_table.py spar > ../logs/table_spar.md` | 17 rows with gain ratios and residuals; succeeds after checkpoint filtering fix |
| method tables | `timeout 60 python method_table.py <dir> > ../logs/table_<dir>.md` for `chain`, `cactus`, `ht` | all regenerated from existing logs and current best `U` |
| compact tables | `timeout 60 python compact_table.py <dir> > ../logs/table_<dir>_compact.md` for `chain`, `cactus`, `ht` | all regenerated and inserted verbatim into Section 4.5 |
| final targeted document checks | `timeout 60 python verify_closeout.py` | all pass; an initial padded-zero comparison in this new check was corrected to accept the logged precision |
| process check (from stream directory) | `pgrep -af three-var-computation` | exit 1, no matching process; no stream experiment remains |


### 6.5 Revision after review round 1

The [round-1 review](reviews/review-r1.md) required minor fixes, with issue 1 required
before verification. This revision addressed all nine issues, which the
round-2 review confirmed. Its headline precision and cost interpretation are
superseded by Section 6.6. Only this stream's note, code and author logs were edited;
the review sources and result records were read without changes. A reviewer-code
import created `reviews/r1-code/__pycache__/lift_depth.cpython-313.pyc`; that generated
cache and its empty directory were removed, and subsequent checks disabled bytecode
writes. No commit, index or branch operation,
project-wide check or CI inspection was performed.

| review issue | change and evidence |
|---|---|
| 1: misleading `spar` headline | "At most 70.01%" → strict `spar090-075-1` gain term at computed depths 0.045% of the gap, 0.54% including the primal-to-safe margin; computed minimum depth `−8.10·10⁻⁹`. A fresh solve and all-triple audit reproduce the reviewer's computation exactly; Section 6.6 corrects its precision. The original deepest depths are normalized triangle residuals; the 9-of-15 correspondence and four independent lift checks are explained. The 19.17%, 53.77%, 39.22% small-gap ratios are relabelled as solver accuracy. Strict attempts and remaining coverage are explicit in Section 4.1; Summary, Main result 2, Limits and Open questions now agree. |
| 2: thresholded triangle zeros | `0.0e+00` → recomputed unthresholded maxima at all 15 saved original points, up to `8.642851345719293·10⁻⁸` among the old zero entries. The two unsaved points remain "not recorded". `audit_table.py` now regenerates this reporting. The strict reviewer's zero means below `10⁻⁸`; this revision reports its actual maximum `3.5411876556090682·10⁻⁹`. |
| 3: completeness reference and containment | Conjecture 2.9 → the three-positive completeness conjecture (Conjecture 2.11). `R` → `R ∩ {Y_ii ≤ x_i}` in the containment argument, using the equivalence stated in the completeness note, reviewed in round 1 (minor fixes) and revised; round 2 confirms those fixes and requests a minor reporting fix. The localizing matrices do not imply the diagonal caps. Summary and Sections 4.4–5 use the corrected reference. |
| 4: AP generator mismatch | "Consistent with those observations" → our generator does not reproduce the paper's 12 gap instances (absolute gaps 0.03–0.8). State that the generator includes the diagonal, the single gap is about `1.04·10⁻³` (relative `3.6·10⁻⁶`), and the reviewer's 12,000-instance density probe found no gap above `10⁻⁵` relative. Negative results are limited to this generator. The local paper's Section 5 and Table 5 were checked. |
| 5: timing interpretation | "Comparable within one run" and "only ratios within one run are meaningful" → wall clock under changing load, with indicative ratios even within a run. Give the reviewer's `m = 300` rerun: `X/F` 10.9 → 7.5, `KA/F` 3.2 → 1.4, ordering `F < KA < X` retained. Identify chain `XF` times as separate runs. Summary, timing claims and Limits carry these qualifications. |
| 6: numerical claims and cost mechanism | `KA` shortfall 0.26–3.7 → 0.31–3.73 percentage points; chain `XF/F` 0.8–1.6 → 0.23–2.05 (logged `XF` times can be about four times smaller); cacti 2.1–5.7. `ht` comparison-base triple count 0–6 → 0–7, with the separate six-triple audit distinguished. Remaining gap about 35% → about 32%. Minimum family values `−1.6·10⁻⁷`–`−9.6·10⁻⁷` → `−1.85·10⁻⁷`–`−9.55·10⁻⁷`. Maximum original `spar` primal infeasibility `1.34·10⁻⁷` → `1.33·10⁻⁷`. The added selection explanation is corrected in Section 6.6: it holds for chains; block type dominates on cacti. Raw-log recomputations are recorded below. |
| 7: `n = 3` closures | Primal table → safe table using `(method_safe − B_safe)/(X_safe − B_safe)`. Minimum closures are `0.9999826604704566` (`F`) and `0.999912428316144` (`KAF`); the latter displays as 0.9999. Remaining primal diagnostics in Section 4.4 are labelled. |
| 8: Lemma 3 and final-family gains | Ambiguous `R ⊇ B` → convex feasible set `R` containing `y_c`, with `y* ∈ R`; no relation with `B` is needed. Section 4.5 distinguishes gain terms from the audited primal values and gain estimates against safe bounds, adds the primal-to-safe margins, and states feasibility and one-sided depth qualifications. It also distinguishes the separate `m = 3000` audit point from the comparison run. |
| 9: double negative | "No queued Gurobi solve never ran" → "every queued Gurobi solve ran". |
| header and status | "Nothing here has been committed" → the stream was swept into repository commits outside this program; this revision performs no git operation. "Not yet reviewed" → "revised after review round 1; not re-reviewed". Section 6.4 is explicitly a historical closeout, superseded where this review corrected it. |

All revision computations use `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and `timeout`;
subsequent checks also use `PYTHONDONTWRITEBYTECODE=1`.
The strict runs used at most three simultaneous audit processes; other numerical
checks occupied at most one additional process. No large experiment outside the four
affected `spar` audits was rerun. The following commands are from the stream directory
unless stated; outputs are author records under `logs/`, not writes to `reviews/`.

| check | command actually run | outcome |
|---|---|---|
| strict `spar090-075-1` | `timeout 1800 python code/strict_spar_audit.py spar090-075-1 > logs/strict_r1_spar090-075-1.out 2>&1` | exit 0, 558.60 s; every triple audited, reviewer result reproduced exactly; actual triangle maximum `3.54·10⁻⁹` |
| strict `spar100-050-1` attempt | `timeout 1800 python code/strict_spar_audit.py spar100-050-1 > logs/strict_r1_spar100-050-1.out 2>&1` | exit 1 after three solves: all detected missing triangles enforced, but existing triangles still violate `10⁻⁸`; maximum `1.036850683089341·10⁻⁸` even at solver tolerance `10⁻¹⁰`. Base point saved; no strict hull audit claimed. |
| strict `spar100-050-2` attempt | `timeout 1800 python code/strict_spar_audit.py spar100-050-2 > logs/strict_r1_spar100-050-2.out 2>&1` | exit 1 after three solves: all detected missing triangles enforced, but maximum `1.580930453215501·10⁻⁸` on existing triangles even at solver tolerance `10⁻¹⁰`. Base point saved; no strict hull audit claimed. |
| strict `spar125-050-1` attempt | `timeout 1800 python code/strict_spar_audit.py spar125-050-1 > logs/strict_r1_spar125-050-1.out 2>&1`; then `kill -TERM 128516` (this attempt's timeout PID) | stopped after about ten minutes in the first solve because of cost; exit 143; no solved base or depth result. Child process exited. |
| original `spar` quantities | `timeout 120 python reviews/r1-code/spar_recompute.py > logs/r1_fix_spar_recompute.out` | exit 0; 99 base runs, 17 audits, small-gap noise, triangle/depth correspondence and exact maximum infeasibility reproduced |
| independent original deepest-triple depths | `timeout 120 python reviews/r1-code/check_argmin_triples.py > logs/r1_fix_argmin_triples.out` | exit 0; four six-tetrahedron lift depths agree with `−4 ×` the violated triangle to six digits |
| constructed and sparse tables, timing ranges, SCS and Gurobi references | `timeout 120 python reviews/r1-code/tables_recompute.py > logs/r1_fix_tables_recompute.out` | exit 0; all 32 compact rows agree; corrected shortfall, timing and remaining-gap ranges reproduced; saved Gurobi solutions satisfy the box and match their JSON objectives |
| original `n = 3` table diagnostic | `timeout 120 python reviews/r1-code/n3_pool_recompute.py > logs/r1_fix_n3_pool_recompute.out` | exit 0; confirms the original table used primal values and reports agreeing safe closures against the primal exact-lift reference |
| safe `n = 3` table and remaining corrected numbers | `timeout 60 python code/r1_fix_numbers.py > logs/r1_fix_numbers.out` | exit 0; closures against `X_safe`, family minima, six final-family margins, comparison-run `ht` count seven, original `spar` maximum infeasibility, all 117,480 fresh strict depths equal to the reviewer records bit for bit, and the 9-of-15 triangle correspondence reproduced |
| regenerate `spar` table (from `code/`) | `timeout 60 python audit_table.py spar > ../logs/table_spar.md` | exit 0; 17 rows, unthresholded triangle maxima and three solver-accuracy ratio labels. An initial invocation with paths relative to the stream directory was issued from `code/` and failed at shell redirection before Python ran; corrected as shown. |
| targeted document check (from `code/`) | `timeout 120 python verify_closeout.py > ../logs/r1_fix_verify_closeout.out` | exit 0; five PASS lines: status and placeholders, generated tables and late references, queued-output counts, AP table, and local links. The final revision was checked with the same command. |
| final process checks | `pgrep -af three-var-computation`; `pgrep -af '[s]trict_spar_audit.py'` | both exit 1 with no matches; all four audit sessions have exited, including the interrupted `spar125-050-1` child. No background process remains. |

Full-precision checks are in [logs/r1_fix_numbers.out](logs/r1_fix_numbers.out),
[logs/r1_fix_tables_recompute.out](logs/r1_fix_tables_recompute.out) and
[logs/r1_fix_spar_recompute.out](logs/r1_fix_spar_recompute.out). A confirming reviewer
should check the strict-audit coverage and provenance in Section 4.1, the capped
containment and stated equivalence in Section 4.4, and the safe-bound margins in
Section 4.5. The constructed-instance tables and bound conclusions are unchanged.

### 6.6 Revision after review round 2

The [round-2 review](reviews/review-r2.md) confirmed all nine round-1 fixes
and found four new minor issues. This revision addresses them and is **not
re-reviewed**. It reads the review code and logs, including the stored probe
triples, and recomputes the affected quantities from saved stream records.
No strict audit or SDP solve was rerun. Only this stream's note, code and
author logs were edited; review files were left unchanged. No commit or git
state change, project-wide verification or CI inspection was performed.

| issue | old → new wording and evidence |
|---|---|
| 1: headline precision | "Minimum depth `−8.10·10⁻⁹`; gain term 0.045%" → "Computed minimum depth `−8.10·10⁻⁹`; gain term at computed depths 0.045% (0.54% with margin)." The triangle at (0, 11, 47) forces exact minimum at most `−1.4164750622436273·10⁻⁸`, so the exact-depth gain term is at least about 0.079% (0.58%). Stored depths exceed exact triangle/cap bounds by more than `10⁻⁹` on 73,615 triples, by up to `9.674490005331274·10⁻⁸`. The 0.56% (1.05%) upper sensitivity assumes exact minimum at least `−10⁻⁷`; a stored-depth error bound of `10⁻⁷` instead gives about 0.60% (1.10%). Summary, Main result 2 and Section 4.1 state the assumptions. |
| 2: cost mechanism | "Most of `F`'s advantage over `X` comes from selection" → "On chains, most comes from selection; on cacti, block type accounts for most." Raw solve logs give cactus `XF/F` from `2.1022312444865916` to `5.685618325760023`, within the same driver run. `XF` and `F` use the same selection rule; their iterates can select different triples. Summary, Section 4.5 and Limits agree. |
| 3: two sets of 13 | "The other 13 original instances" → "The 13 original instances outside the four originally deep cases." "On the other 13 instances" → "On the 13 instances other than `spar090-075-1` with initial relative gap above `10⁻⁵`", explicitly including the other three originally deep cases. The saved 17 audit records reproduce both sets. |
| 4: completeness status | "Unreviewed" → "Reviewed in round 1 (minor fixes) and revised; round 2 confirms those fixes and requests a minor reporting fix." Both completeness review reports were read. Round 1 checked the cited equivalence (Proposition 2.2 and Corollary 2.4); neither round found an error in a proved statement. Sections 4.4, 5 and 6.5 use the updated status. |
| optional residue explanations | Section 4.1 now gives the normalized cap residual and its agreement with the bulk original `spar125-050-1` depths. Section 4.5 gives the cactus final-point triangle residual and the `1.638251086059886·10⁻⁹` difference from its computed depth; numerical agreement is verified, exact equality is not. |
| header and provenance | "Revised after review round 1; not re-reviewed" → "Revised after review round 2; not re-reviewed." The round-1 revision is now identified as confirmed, with its headline precision and cost interpretation superseded here. |

Commands ran in the foreground with `OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`, `PYTHONDONTWRITEBYTECODE=1`, an explicit `timeout`,
and no solver invocation. Paths below are relative to the stream directory.

| targeted check | command actually run | outcome |
|---|---|---|
| saved-depth bounds, gain sensitivity, raw timing ratios, two sets of 13, optional residues | `timeout 60 python code/r2_fix_checks.py > logs/r2_fix_checks.out 2>&1` | exit 0; PASS, all affected quantities reproduced without solving an SDP. The initial run exited 1 because the optional cactus equality check demanded agreement within `10⁻¹¹`; the saved values differ by `1.638·10⁻⁹`. The check now verifies agreement within 0.1% and logs the difference. Initial output is retained in `logs/r2_fix_checks_initial.out`. |
| note consistency and local links (from `code/`) | `timeout 60 python verify_closeout.py > ../logs/r2_fix_verify_closeout.out 2>&1` | exit 0; five PASS lines. Its status check now requires the round-2 revision header. Existing tables and local links agree. |

Verification code: [code/r2_fix_checks.py](code/r2_fix_checks.py). Full-precision
output: [logs/r2_fix_checks.out](logs/r2_fix_checks.out); document check:
[logs/r2_fix_verify_closeout.out](logs/r2_fix_verify_closeout.out). A confirming
reviewer should check the two different upper-sensitivity assumptions and the
distinction between a lower bound on the Lemma 3 gain term and a lower bound
on actual improvement. No background process was started or left running.

## 7. Limits

- All bound comparisons are numerical. The safe bound is careful floating point
  (projection of the dual onto the cone plus a priori rounding terms), not interval
  arithmetic. Hull depths and family values used for selection and in Lemma 3 are
  computed in floating point: hull depths use Clarabel at tolerance `10⁻⁹`
  (`hullsep.py`), while family values use the simplex-minimum calculation
  (`relax.py`, `stqp_min`). The main relaxation tolerance is `10⁻⁸`
  (`conic.py`; Section 2). Lemma 3 is applied to a
  numerical relaxation solution with recorded primal infeasibility (up to `1.33·10⁻⁷`
  in the original `spar` audits). The strict `spar090-075-1` re-audit removes the
  large triangle residue; feasibility, one-sided depth accuracy and the
  primal-to-safe-bound margin still limit numerical uses in Sections 4.1 and 4.5.
- No counterexample or exact certificate was needed for the conclusions, so nothing was
  certified in rational arithmetic in this stream; the rational certificate of the
  2026-09-25 counterexample is reused through `test_basic.py`.
- The instances with triple-level gaps (hard `n = 3` objectives, chains, cacti) are
  constructed for this purpose. The AP variant supplies one natural-generator
  triple-level gap among 12,000 instances (relative `3.6·10⁻⁶`), already closed by
  `KA`. Other natural families gave mostly negative results. The deepest original
  `spar` residues are normalized triangle violations of `B`; strict coverage and
  remaining accuracy caveats are stated in Section 4.1.
  We did not find or test a practical problem class where the family helps beyond `KA`.
- `U` is the best heuristic or Gurobi feasible value, except for published `spar`
  optima and face enumeration on small dense instances. Gurobi reported optimality
  within its tolerance for `chain_m100_e0_s1`, `ht_plus_n30_k2_s1` and the first
  draft’s `n = 30` grid. The feasible `U` still gives a lower estimate of true gap
  closure when its value is above the optimum; the reported Gurobi tolerance does
  not make it an exact certificate.
- Selection for `K`, `A`, `X` uses the exact hull test, which favors these methods and
  costs separation time that is reported separately. A solver would use cheaper rules.
- Timings are wall clock on a shared machine with varying load. Ratios are indicative
  even within a run, since methods execute sequentially. The reviewer's `m = 300`
  rerun changed `X/F` from 10.9 to 7.5 and `KA/F` from 3.2 to 1.4, while preserving
  `F < KA < X`. Chain `XF/F` comparisons cross separate first-draft runs. Most of
  `F`'s advantage over `X` on chains comes from `X` lifting extra triples under its
  selection rule. On cacti, block type accounts for most of the advantage:
  family-selected exact lifts took 2.1 to 5.7 times `F`'s solve time within the
  same run, with slightly different selected sets at successive iterates.
- `K` was tested only with `|P| = 3` and `M = ∅`; Khajavirad's systems with larger plus
  sets or nonempty minus sets were not tested. The shared-moment test of `K` on all
  triples was done on one instance (`spar050-050-1`).
- The modeling layer stores `H` densely, which limited the sparse instances to
  `n ≤ 9000`. Larger SCS runs than `m = 1000` were not attempted.
- No branch-and-bound or solver integration was tested; nothing here measures a
  speedup of a global solver. The relaxations were compared at the root only.
- The small dense generator re-implements the `spar` generator with numpy random
  numbers; the instances are not the published ones, and Anstreicher–Puges's small
  instances are not public. Our AP variant includes the diagonal and does not
  reproduce their 12 gap instances; the reviewer's density probe did not resolve
  the generator mismatch.

## 8. Open questions

1. Prove or refute Conjecture 1 (Shor + McCormick + `Y_ii ≤ x_i` + triangles + the 24 family
   orientations describe `QPB3`). It would make the family an exact replacement for the
   tetrahedral lift.
2. Is there a practical problem class where triple-level gaps persist beyond `KA`?
   The AP exception has a triple-level gap closed by `KA`; on the other natural
   families the audits are mostly negative. The large original `spar` depths were
   triangle residuals, and the strict `spar090-075-1` result is much smaller; the
   remaining qualifications concern audit coverage and numerical accuracy (Section 4.1).
   A theorem explaining this behavior (for example for overlapping
   triangles) would also be useful.
3. Branch-and-bound nodes change the box and may create triple-level gaps that the root
   does not have. Does the family help inside a branch-and-bound tree, where branching
   on a variable makes three-variable terms more prominent?
4. A cheaper selection rule than the hull test for `K`, `A`, `X`, and a rule that decides
   when triple-level separation is worth running at all (the audit of Lemma 3 costs one
   small SDP per triple).
