import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint

/-!
# The common refinement of two grids: exact coarse data for nonaligned grids

This module supplies the **correctness** content of the coarse-data construction inside the
proof of `thm:certified-coarsening` in
`paper-switching-control/sections/11-transfer-and-coarsening.tex`:

> For piecewise-constant input, traverse the sorted input and coarse endpoints together. On
> each segment of their common refinement, add its length times the known input rate to the
> current coarse mass. [...] This integration preserves the original `A_i(jh)`; merely
> grouping whole fine cells would be incorrect for nonaligned grids.

`topics/17-grid-switching/CLAIMS.md` excludes counted bit-cost models, but records that "the
verified content of an algorithmic claim is its correctness, termination and exact
arithmetic-operation or size recursions". Accordingly this module formalizes

* the **correctness** of the traversal: `gridCumulative_coarseNode_eq_refinementSum`;
* the **size recursion**: `card_refinementNodes_le` and `exists_commonRefinement`, giving a
  common refinement with at most `M + Nf - 1` cells;
* the **justification of the caveat**: `wholeCellSum_ne_gridCumulative`, a nonaligned instance
  on which grouping whole fine cells returns the wrong coarse value.

The operation count `O(n(N+M))` itself, the arithmetic bound `eq:coarsening-complexity`, and
the polynomial bit-complexity assertion remain excluded.

## Structure of the correctness argument

`gridCumulative_refine` is the mathematical heart: refining a grid-constant input to *any*
finer grid, with each refinement cell carrying the rate of the fine cell that contains it,
leaves the cumulative allocation unchanged at every time. Its proof reduces, via the monotone
index embedding of `exists_gridEmbedding`, to the purely combinatorial telescoping identity
`sum_refine_weighted`: the index intervals cut out by the embedding partition the refinement
cells, and each group telescopes to the corresponding coarse increment.

`gridCumulative_node_eq_prefixSum` then observes that at a *node* of the refinement the
clipping in `gridCumulative` disappears, so the value is the plain running sum of cell length
times rate — the "current coarse mass" the traversal maintains. Combining the two at the
coarse nodes gives the headline statement, with no alignment hypothesis anywhere.

`exists_fineCell` and `exists_refinementRates` show the construction is well defined: every
refinement cell lies in a unique cell of the fine grid, so "the known input rate on the
segment" exists and the refined rates again form a rate matrix. Together with
`exists_commonRefinement` this makes the headline theorem non-vacuous for every pair of grids
on a horizon of positive length.
-/

namespace GridSwitching

open Set

variable {n : ℕ}

/-! ## Index bookkeeping over a monotone embedding -/

/-- Telescoping over a half-open index interval. -/
private theorem refinement_sum_Ico_telescope (F : ℕ → ℝ) {a b : ℕ} (hab : a ≤ b) :
    ∑ c ∈ Finset.Ico a b, (F (c + 1) - F c) = F b - F a := by
  have h1 := Finset.sum_Ico_consecutive (fun c => F (c + 1) - F c) (Nat.zero_le a) hab
  simp only [← Finset.range_eq_Ico] at h1
  rw [Finset.sum_range_sub F a, Finset.sum_range_sub F b] at h1
  linarith

/-- The index intervals cut out by a monotone `E` with `E 0 = 0` and `E Nf = K` partition
`range K`. -/
private theorem sum_range_partition (g : ℕ → ℝ) {Nf K : ℕ} (E : ℕ → ℕ) (hE : Monotone E)
    (hE0 : E 0 = 0) (hEN : E Nf = K) :
    ∑ j ∈ Finset.range Nf, ∑ c ∈ Finset.Ico (E j) (E (j + 1)), g c
      = ∑ c ∈ Finset.range K, g c := by
  have key : ∀ j : ℕ, ∑ c ∈ Finset.Ico (E j) (E (j + 1)), g c
      = (∑ c ∈ Finset.range (E (j + 1)), g c) - ∑ c ∈ Finset.range (E j), g c := by
    intro j
    have h := Finset.sum_Ico_consecutive g (Nat.zero_le (E j)) (hE (Nat.le_succ j))
    simp only [← Finset.range_eq_Ico] at h
    linarith
  simp only [key]
  rw [Finset.sum_range_sub (fun m => ∑ c ∈ Finset.range (E m), g c) Nf, hE0, hEN]
  simp

/-- The combinatorial core of refinement invariance: a weighted telescoping sum over the cells
of a refinement equals the corresponding sum over the cells of the coarser family, provided
each refinement cell carries the weight of the coarse cell containing it. -/
private theorem sum_refine_weighted {Nf K : ℕ} (e : Fin (Nf + 1) → Fin (K + 1))
    (hemono : Monotone e) (he0 : e 0 = 0) (hel : e (Fin.last Nf) = Fin.last K)
    (a : Fin Nf → ℝ) (b : Fin K → ℝ) (Φ : Fin (K + 1) → ℝ)
    (hab : ∀ (j : Fin Nf) (c : Fin K), (e j.castSucc : ℕ) ≤ (c : ℕ) →
      (c : ℕ) < (e j.succ : ℕ) → b c = a j) :
    ∑ c : Fin K, b c * (Φ c.succ - Φ c.castSucc)
      = ∑ j : Fin Nf, a j * (Φ (e j.succ) - Φ (e j.castSucc)) := by
  classical
  set E : ℕ → ℕ := fun m => (e ⟨min m Nf, by omega⟩ : ℕ) with hEdef
  set P : ℕ → ℝ := fun m => Φ ⟨min m K, by omega⟩ with hPdef
  set B : ℕ → ℝ := fun c => if h : c < K then b ⟨c, h⟩ else 0 with hBdef
  set Av : ℕ → ℝ := fun j => if h : j < Nf then a ⟨j, h⟩ else 0 with hAvdef
  have hEmono : Monotone E := by
    intro p q hpq
    exact hemono (by simp only [Fin.mk_le_mk]; omega)
  have hE0 : E 0 = 0 := by simp [hEdef, he0]
  have hEN : E Nf = K := by
    have hlast : (⟨min Nf Nf, by omega⟩ : Fin (Nf + 1)) = Fin.last Nf :=
      Fin.ext (by simp [Fin.last])
    simp only [hEdef, hlast, hel, Fin.val_last]
  have hEle : ∀ m, E m ≤ K := fun m => Nat.lt_succ_iff.mp (e _).isLt
  -- the left-hand side as a sum over `Finset.range K`
  have hL : ∑ c : Fin K, b c * (Φ c.succ - Φ c.castSucc)
      = ∑ c ∈ Finset.range K, B c * (P (c + 1) - P c) := by
    rw [← Fin.sum_univ_eq_sum_range (fun c => B c * (P (c + 1) - P c)) K]
    refine Finset.sum_congr rfl fun c _ => ?_
    have hcK : (c : ℕ) < K := c.isLt
    have hb : B (c : ℕ) = b c := by simp only [hBdef, dif_pos c.isLt, Fin.eta]
    have h1 : P ((c : ℕ) + 1) = Φ c.succ := by
      simp only [hPdef]
      congr 1
      refine Fin.ext ?_
      simp only [Fin.val_succ]
      omega
    have h2 : P (c : ℕ) = Φ c.castSucc := by
      simp only [hPdef]
      congr 1
      refine Fin.ext ?_
      simp only [Fin.val_castSucc]
      omega
    rw [hb, h1, h2]
  -- the right-hand side as a sum over `Finset.range Nf`
  have hR : ∑ j : Fin Nf, a j * (Φ (e j.succ) - Φ (e j.castSucc))
      = ∑ j ∈ Finset.range Nf, Av j * (P (E (j + 1)) - P (E j)) := by
    rw [← Fin.sum_univ_eq_sum_range (fun j => Av j * (P (E (j + 1)) - P (E j))) Nf]
    refine Finset.sum_congr rfl fun j _ => ?_
    have hjN : (j : ℕ) < Nf := j.isLt
    have ha : Av (j : ℕ) = a j := by simp only [hAvdef, dif_pos j.isLt, Fin.eta]
    have hs : E ((j : ℕ) + 1) = (e j.succ : ℕ) := by
      simp only [hEdef]
      congr 2
      refine Fin.ext ?_
      simp only [Fin.val_succ]
      omega
    have hc : E (j : ℕ) = (e j.castSucc : ℕ) := by
      simp only [hEdef]
      congr 2
      refine Fin.ext ?_
      simp only [Fin.val_castSucc]
      omega
    have h1 : P (E ((j : ℕ) + 1)) = Φ (e j.succ) := by
      rw [hs]
      simp only [hPdef]
      congr 1
      refine Fin.ext ?_
      have := Nat.lt_succ_iff.mp (e j.succ).isLt
      simp only []
      omega
    have h2 : P (E (j : ℕ)) = Φ (e j.castSucc) := by
      rw [hc]
      simp only [hPdef]
      congr 1
      refine Fin.ext ?_
      have := Nat.lt_succ_iff.mp (e j.castSucc).isLt
      simp only []
      omega
    rw [ha, h1, h2]
  rw [hL, hR]
  have hstep : ∀ j ∈ Finset.range Nf, Av j * (P (E (j + 1)) - P (E j))
      = ∑ c ∈ Finset.Ico (E j) (E (j + 1)), B c * (P (c + 1) - P c) := by
    intro j hj
    rw [Finset.mem_range] at hj
    rw [← refinement_sum_Ico_telescope P (hEmono (Nat.le_succ j)), Finset.mul_sum]
    refine Finset.sum_congr rfl fun c hc => ?_
    rw [Finset.mem_Ico] at hc
    have hcK : c < K := lt_of_lt_of_le hc.2 (hEle (j + 1))
    have hEj : E j = (e (⟨j, hj⟩ : Fin Nf).castSucc : ℕ) := by
      simp only [hEdef]
      congr 2
      refine Fin.ext ?_
      simp only [Fin.val_castSucc]
      omega
    have hEj1 : E (j + 1) = (e (⟨j, hj⟩ : Fin Nf).succ : ℕ) := by
      simp only [hEdef]
      congr 2
      refine Fin.ext ?_
      simp only [Fin.val_succ]
      omega
    have hBc : B c = b ⟨c, hcK⟩ := by simp only [hBdef, dif_pos hcK]
    have hAvj : Av j = a ⟨j, hj⟩ := by simp only [hAvdef, dif_pos hj]
    rw [hBc, hAvj]
    congr 1
    refine (hab ⟨j, hj⟩ ⟨c, hcK⟩ ?_ ?_).symm
    · rw [← hEj]; exact hc.1
    · rw [← hEj1]; exact hc.2
  rw [Finset.sum_congr rfl hstep]
  exact (sum_range_partition (fun c => B c * (P (c + 1) - P c)) E hEmono hE0 hEN).symm

/-! ## Monotone index embeddings between nested grids -/

/-- If the nodes of the grid `x` are among the nodes of the grid `y` on the same horizon, the
inclusion of nodes is realized by a monotone index embedding matching the endpoints. Nothing
beyond the node inclusion is assumed: monotonicity comes from both grids being strictly
increasing and the endpoint conditions from the shared horizon. -/
theorem exists_gridEmbedding {M Nf : ℕ} {x : Fin (M + 1) → ℝ} {y : Fin (Nf + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) (hy : IsGrid y T) (hsub : Set.range x ⊆ Set.range y) :
    ∃ e : Fin (M + 1) → Fin (Nf + 1), Monotone e ∧ e 0 = 0 ∧
      e (Fin.last M) = Fin.last Nf ∧ ∀ q, y (e q) = x q := by
  classical
  choose e he using fun q : Fin (M + 1) => hsub (Set.mem_range_self q)
  refine ⟨e, ?_, ?_, ?_, he⟩
  · intro p q hpq
    have : y (e p) ≤ y (e q) := by
      rw [he p, he q]
      exact hx.strictMono.monotone hpq
    exact hy.strictMono.le_iff_le.mp this
  · refine hy.strictMono.injective ?_
    rw [he 0, hx.first, hy.first]
  · refine hy.strictMono.injective ?_
    rw [he (Fin.last M), hx.last, hy.last]

/-! ## Refinement invariance of a grid-constant input

The exact statement of the algorithm in the proof of `thm:certified-coarsening`: on each
segment of the common refinement, the input runs at the *known* rate of the fine cell that
contains the segment, and summing length times rate over those segments reproduces the fine
cumulative values exactly. No alignment between the two grids is assumed anywhere. -/

/-- Refining a grid-constant input to any finer grid, with each refinement cell carrying the
rate of the fine cell that contains it, changes nothing: the two cumulative allocations are
equal at every time. -/
theorem gridCumulative_refine {Nf K : ℕ} {y : Fin (Nf + 1) → ℝ} {z : Fin (K + 1) → ℝ} {T : ℝ}
    (hy : IsGrid y T) (hz : IsGrid z T) (hsub : Set.range y ⊆ Set.range z)
    {r : Fin Nf → Fin n → ℝ} {ρ : Fin K → Fin n → ℝ}
    (hρ : ∀ (c : Fin K) (j : Fin Nf), y j.castSucc ≤ z c.castSucc → z c.succ ≤ y j.succ →
      ρ c = r j) (i : Fin n) (t : ℝ) :
    gridCumulative z ρ i t = gridCumulative y r i t := by
  obtain ⟨e, hemono, he0, hel, hey⟩ := exists_gridEmbedding hy hz hsub
  have hyz : ∀ m, y m = z (e m) := fun m => (hey m).symm
  have key := sum_refine_weighted e hemono he0 hel (fun j => r j i) (fun c => ρ c i)
    (fun m => min t (z m)) ?_
  · have hgy : gridCumulative y r i t
        = ∑ j : Fin Nf, r j i * (min t (z (e j.succ)) - min t (z (e j.castSucc))) := by
      simp only [gridCumulative]
      exact Finset.sum_congr rfl fun j _ => by rw [hyz j.succ, hyz j.castSucc]
    rw [hgy]
    simpa only [gridCumulative] using key
  · intro j c hle hlt
    have h1 : y j.castSucc ≤ z c.castSucc := by
      rw [hyz]
      refine hz.strictMono.monotone ?_
      simp only [Fin.le_def, Fin.val_castSucc]
      omega
    have h2 : z c.succ ≤ y j.succ := by
      rw [hyz]
      refine hz.strictMono.monotone ?_
      simp only [Fin.le_def, Fin.val_succ]
      omega
    rw [hρ c j h1 h2]

/-- At a node of a grid, the clipping in `gridCumulative` disappears and the cumulative value
is the plain prefix sum of cell length times rate. This is the "current coarse mass"
maintained by the traversal. -/
theorem gridCumulative_node_eq_prefixSum {K : ℕ} {z : Fin (K + 1) → ℝ} {T : ℝ}
    (hz : IsGrid z T) (ρ : Fin K → Fin n → ℝ) (i : Fin n) (m : Fin (K + 1)) :
    gridCumulative z ρ i (z m)
      = ∑ c ∈ Finset.univ.filter (fun c : Fin K => (c : ℕ) < (m : ℕ)),
          ρ c i * cellLength z c := by
  classical
  simp only [gridCumulative]
  rw [← Finset.sum_filter_add_sum_filter_not Finset.univ
    (fun c : Fin K => (c : ℕ) < (m : ℕ))]
  have hzero : ∑ c ∈ Finset.univ.filter (fun c : Fin K => ¬ (c : ℕ) < (m : ℕ)),
      ρ c i * (min (z m) (z c.succ) - min (z m) (z c.castSucc)) = 0 := by
    refine Finset.sum_eq_zero fun c hc => ?_
    rw [Finset.mem_filter, not_lt] at hc
    have hmc : z m ≤ z c.castSucc := by
      refine hz.strictMono.monotone ?_
      simp only [Fin.le_def, Fin.val_castSucc]
      exact hc.2
    have hms : z m ≤ z c.succ := by
      refine hz.strictMono.monotone ?_
      simp only [Fin.le_def, Fin.val_succ]
      omega
    rw [min_eq_left hmc, min_eq_left hms, sub_self, mul_zero]
  rw [hzero, add_zero]
  refine Finset.sum_congr rfl fun c hc => ?_
  rw [Finset.mem_filter] at hc
  have hcm : z c.castSucc ≤ z m := by
    refine hz.strictMono.monotone ?_
    simp only [Fin.le_def, Fin.val_castSucc]
    omega
  have hsm : z c.succ ≤ z m := by
    refine hz.strictMono.monotone ?_
    simp only [Fin.le_def, Fin.val_succ]
    omega
  rw [min_eq_right hcm, min_eq_right hsm, cellLength]

/-- **The correctness content of the coarse-data construction.** Let `A = gridCumulative y r`
be a grid-constant input on a fine grid `y`, let `x` be an arbitrary coarse grid on the same
horizon with **no alignment assumption**, and let `z` be any common refinement of the two,
carrying on each of its cells the rate of the fine cell containing it. Then every coarse node
`x q` sits at some refinement node `z (g q)`, and the exact coarse cumulative value
`A i (x q)` is the sum, over the refinement segments to the left of that node, of the segment
length times the known input rate on the segment. -/
theorem gridCumulative_coarseNode_eq_refinementSum {M Nf K : ℕ} {x : Fin (M + 1) → ℝ}
    {y : Fin (Nf + 1) → ℝ} {z : Fin (K + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) (hy : IsGrid y T)
    (hz : IsGrid z T) (hyz : Set.range y ⊆ Set.range z) (hxz : Set.range x ⊆ Set.range z)
    {r : Fin Nf → Fin n → ℝ} {ρ : Fin K → Fin n → ℝ}
    (hρ : ∀ (c : Fin K) (j : Fin Nf), y j.castSucc ≤ z c.castSucc → z c.succ ≤ y j.succ →
      ρ c = r j) :
    ∃ g : Fin (M + 1) → Fin (K + 1), (∀ q, z (g q) = x q) ∧
      ∀ (i : Fin n) (q : Fin (M + 1)), gridCumulative y r i (x q)
        = ∑ c ∈ Finset.univ.filter (fun c : Fin K => (c : ℕ) < (g q : ℕ)),
            ρ c i * cellLength z c := by
  obtain ⟨g, _, _, _, hg⟩ := exists_gridEmbedding hx hz hxz
  refine ⟨g, hg, fun i q => ?_⟩
  rw [← hg q, ← gridCumulative_refine hy hz hyz hρ i (z (g q)),
    gridCumulative_node_eq_prefixSum hz ρ i (g q)]

/-! ## The refinement rate matrix exists

The hypothesis `hρ` of `gridCumulative_refine` is not vacuous: every refinement cell lies in a
unique cell of the coarser grid, so "the known input rate on the segment" is well defined and
the refined rates again form a rate matrix. -/

/-- Two cells of a grid cannot both contain a nondegenerate interval. -/
private theorem fineCell_unique {Nf K : ℕ} {y : Fin (Nf + 1) → ℝ} {z : Fin (K + 1) → ℝ}
    {T : ℝ} (hy : IsGrid y T) (hz : IsGrid z T) (c : Fin K) {j j' : Fin Nf}
    (h1 : y j.castSucc ≤ z c.castSucc) (h2 : z c.succ ≤ y j.succ)
    (h1' : y j'.castSucc ≤ z c.castSucc) (h2' : z c.succ ≤ y j'.succ) : j = j' := by
  have hc : z c.castSucc < z c.succ := hz.strictMono (Fin.castSucc_lt_succ (i := c))
  rcases lt_trichotomy j j' with hlt | heq | hgt
  · exfalso
    have hstep : y j.succ ≤ y j'.castSucc := by
      refine hy.strictMono.monotone ?_
      have : (j : ℕ) < (j' : ℕ) := hlt
      simp only [Fin.le_def, Fin.val_succ, Fin.val_castSucc]
      omega
    linarith
  · exact heq
  · exfalso
    have hstep : y j'.succ ≤ y j.castSucc := by
      refine hy.strictMono.monotone ?_
      have : (j' : ℕ) < (j : ℕ) := hgt
      simp only [Fin.le_def, Fin.val_succ, Fin.val_castSucc]
      omega
    linarith

/-- Every cell of a refinement is contained in a cell of the coarser grid. -/
theorem exists_fineCell {Nf K : ℕ} {y : Fin (Nf + 1) → ℝ} {z : Fin (K + 1) → ℝ} {T : ℝ}
    (hy : IsGrid y T) (hz : IsGrid z T) (hsub : Set.range y ⊆ Set.range z) (c : Fin K) :
    ∃ j : Fin Nf, y j.castSucc ≤ z c.castSucc ∧ z c.succ ≤ y j.succ := by
  classical
  obtain ⟨e, hemono, he0, hel, hey⟩ := exists_gridEmbedding hy hz hsub
  have hcK : (c : ℕ) < K := c.isLt
  have hNf : 0 < Nf := by
    rcases Nat.eq_zero_or_pos Nf with hz0 | hpos
    · exfalso
      subst hz0
      have hl : (Fin.last 0 : Fin 1) = 0 := rfl
      rw [hl, he0] at hel
      have : (0 : ℕ) = K := congrArg Fin.val hel
      omega
    · exact hpos
  set F : Finset (Fin Nf) :=
    Finset.univ.filter (fun j : Fin Nf => (e j.castSucc : ℕ) ≤ (c : ℕ)) with hF
  have hmem0 : (⟨0, hNf⟩ : Fin Nf) ∈ F := by
    have hcast : (⟨0, hNf⟩ : Fin Nf).castSucc = 0 := Fin.ext (by simp)
    simp only [hF, Finset.mem_filter, Finset.mem_univ, true_and, hcast, he0]
    simp
  have hne : F.Nonempty := ⟨_, hmem0⟩
  set j0 : Fin Nf := F.max' hne with hj0
  have hj0mem : j0 ∈ F := F.max'_mem hne
  have hj0le : (e j0.castSucc : ℕ) ≤ (c : ℕ) := by
    simpa [hF] using hj0mem
  have hj0lt : (c : ℕ) < (e j0.succ : ℕ) := by
    by_contra hcon
    rw [not_lt] at hcon
    rcases Nat.lt_or_ge ((j0 : ℕ) + 1) Nf with hlt | hge
    · have hj1 : ((⟨(j0 : ℕ) + 1, hlt⟩ : Fin Nf)).castSucc = j0.succ := Fin.ext (by simp)
      have hmem1 : (⟨(j0 : ℕ) + 1, hlt⟩ : Fin Nf) ∈ F := by
        simp only [hF, Finset.mem_filter, Finset.mem_univ, true_and, hj1]
        exact hcon
      have := F.le_max' _ hmem1
      have : (j0 : ℕ) + 1 ≤ (j0 : ℕ) := this
      omega
    · have hlast : j0.succ = Fin.last Nf := Fin.ext (by simp; omega)
      rw [hlast, hel] at hcon
      simp only [Fin.val_last] at hcon
      omega
  refine ⟨j0, ?_, ?_⟩
  · rw [← hey j0.castSucc]
    refine hz.strictMono.monotone ?_
    simp only [Fin.le_def, Fin.val_castSucc]
    exact hj0le
  · rw [← hey j0.succ]
    refine hz.strictMono.monotone ?_
    simp only [Fin.le_def, Fin.val_succ]
    omega

/-- The refined rate matrix: each refinement cell carries the rate of the fine cell containing
it. This is the "known input rate" of the traversal, and it is again a rate matrix. -/
theorem exists_refinementRates {Nf K : ℕ} {y : Fin (Nf + 1) → ℝ} {z : Fin (K + 1) → ℝ}
    {T : ℝ} (hy : IsGrid y T) (hz : IsGrid z T) (hsub : Set.range y ⊆ Set.range z)
    {r : Fin Nf → Fin n → ℝ} (hr : IsRateMatrix r) :
    ∃ ρ : Fin K → Fin n → ℝ, IsRateMatrix ρ ∧
      ∀ (c : Fin K) (j : Fin Nf), y j.castSucc ≤ z c.castSucc → z c.succ ≤ y j.succ →
        ρ c = r j := by
  classical
  choose jm hjm1 hjm2 using exists_fineCell hy hz hsub
  refine ⟨fun c => r (jm c),
    ⟨fun c i => hr.nonneg _ i, fun c => hr.conservation _⟩, fun c j h1 h2 => ?_⟩
  change r (jm c) = r j
  rw [fineCell_unique hy hz c (hjm1 c) (hjm2 c) h1 h2]

/-! ## The common refinement and its size

The size recursion of the source: merging an `M`-cell and an `Nf`-cell grid on the same
horizon produces a common refinement with at most `M + Nf - 1` cells, because the two node
sets share at least the two endpoints. -/

/-- The nodes of the common refinement of two grids: the union of their node sets. -/
noncomputable def refinementNodes {M Nf : ℕ} (x : Fin (M + 1) → ℝ) (y : Fin (Nf + 1) → ℝ) :
    Finset ℝ :=
  Finset.univ.image x ∪ Finset.univ.image y

theorem mem_refinementNodes {M Nf : ℕ} {x : Fin (M + 1) → ℝ} {y : Fin (Nf + 1) → ℝ}
    {a : ℝ} : a ∈ refinementNodes x y ↔ (∃ q, x q = a) ∨ ∃ j, y j = a := by
  simp [refinementNodes]

/-- The size recursion: the common refinement of an `M`-cell and an `Nf`-cell grid on a
horizon of positive length has at most `M + Nf` nodes, hence at most `M + Nf - 1` cells. -/
theorem card_refinementNodes_le {M Nf : ℕ} {x : Fin (M + 1) → ℝ} {y : Fin (Nf + 1) → ℝ}
    {T : ℝ} (hx : IsGrid x T) (hy : IsGrid y T) (hT : 0 < T) :
    (refinementNodes x y).card ≤ M + Nf := by
  classical
  have hxc : (Finset.univ.image x).card = M + 1 := by
    rw [Finset.card_image_of_injective _ hx.strictMono.injective, Finset.card_univ,
      Fintype.card_fin]
  have hyc : (Finset.univ.image y).card = Nf + 1 := by
    rw [Finset.card_image_of_injective _ hy.strictMono.injective, Finset.card_univ,
      Fintype.card_fin]
  have hsub : ({0, T} : Finset ℝ) ⊆ Finset.univ.image x ∩ Finset.univ.image y := by
    intro a ha
    simp only [Finset.mem_insert, Finset.mem_singleton] at ha
    refine Finset.mem_inter.mpr ⟨?_, ?_⟩ <;> rcases ha with rfl | rfl
    · exact Finset.mem_image.mpr ⟨0, Finset.mem_univ _, hx.first⟩
    · exact Finset.mem_image.mpr ⟨Fin.last M, Finset.mem_univ _, hx.last⟩
    · exact Finset.mem_image.mpr ⟨0, Finset.mem_univ _, hy.first⟩
    · exact Finset.mem_image.mpr ⟨Fin.last Nf, Finset.mem_univ _, hy.last⟩
  have hpair : ({0, T} : Finset ℝ).card = 2 := by
    rw [Finset.card_insert_of_notMem (by simp [hT.ne]), Finset.card_singleton]
  have hinter : 2 ≤ (Finset.univ.image x ∩ Finset.univ.image y).card := by
    rw [← hpair]
    exact Finset.card_le_card hsub
  have hunion := Finset.card_union_add_card_inter
    (Finset.univ.image x) (Finset.univ.image y)
  rw [hxc, hyc] at hunion
  simp only [refinementNodes]
  omega

/-- The common refinement of two grids on the same horizon exists as a grid, contains all the
nodes of both, and has at most `M + Nf - 1` cells. No alignment is assumed. -/
theorem exists_commonRefinement {M Nf : ℕ} {x : Fin (M + 1) → ℝ} {y : Fin (Nf + 1) → ℝ}
    {T : ℝ} (hx : IsGrid x T) (hy : IsGrid y T) (hT : 0 < T) :
    ∃ (K : ℕ) (z : Fin (K + 1) → ℝ), IsGrid z T ∧ Set.range x ⊆ Set.range z ∧
      Set.range y ⊆ Set.range z ∧ K + 1 ≤ M + Nf ∧ K ≤ M + Nf - 1 := by
  classical
  set S : Finset ℝ := refinementNodes x y with hS
  have hxmem : ∀ q, x q ∈ S := fun q =>
    mem_refinementNodes.mpr (Or.inl ⟨q, rfl⟩)
  have hymem : ∀ j, y j ∈ S := fun j =>
    mem_refinementNodes.mpr (Or.inr ⟨j, rfl⟩)
  have hIcc : ∀ a ∈ S, a ∈ Icc (0 : ℝ) T := by
    intro a ha
    rcases mem_refinementNodes.mp ha with ⟨q, rfl⟩ | ⟨j, rfl⟩
    · exact hx.mem_Icc q
    · exact hy.mem_Icc j
  have h0 : (0 : ℝ) ∈ S := hx.first ▸ hxmem 0
  have hTmem : T ∈ S := hx.last ▸ hxmem (Fin.last M)
  have hpos : 0 < S.card := Finset.card_pos.mpr ⟨0, h0⟩
  obtain ⟨K, hK⟩ : ∃ K, S.card = K + 1 := ⟨S.card - 1, by omega⟩
  have hcard := card_refinementNodes_le hx hy hT
  rw [← hS, hK] at hcard
  refine ⟨K, fun c => S.orderEmbOfFin hK c, ⟨?_, ?_, (S.orderEmbOfFin hK).strictMono⟩,
    ?_, ?_, hcard, by omega⟩
  · have hz := Finset.orderEmbOfFin_zero hK (Nat.succ_pos K)
    have hidx : (⟨0, Nat.succ_pos K⟩ : Fin (K + 1)) = 0 := Fin.ext (by simp)
    rw [hidx] at hz
    rw [hz]
    refine le_antisymm (Finset.min'_le _ _ h0) (Finset.le_min' _ _ _ fun a ha => ?_)
    exact (hIcc a ha).1
  · have hz := Finset.orderEmbOfFin_last hK (Nat.succ_pos K)
    have hidx : (⟨K + 1 - 1, by omega⟩ : Fin (K + 1)) = Fin.last K := Fin.ext (by simp)
    rw [hidx] at hz
    rw [hz]
    refine le_antisymm (Finset.max'_le _ _ _ fun a ha => (hIcc a ha).2)
      (Finset.le_max' _ _ hTmem)
  · intro a ha
    obtain ⟨q, rfl⟩ := ha
    rw [Finset.range_orderEmbOfFin S hK]
    exact hxmem q
  · intro a ha
    obtain ⟨j, rfl⟩ := ha
    rw [Finset.range_orderEmbOfFin S hK]
    exact hymem j

/-! ## The nonaligned-grid caveat

The proof of `thm:certified-coarsening` warns that forming the coarse masses by "merely
grouping whole fine cells would be incorrect for nonaligned grids". The warning is justified
rather than merely repeated: `wholeCellSum` below is that naive rule, and
`wholeCellSum_ne_gridCumulative` exhibits a nonaligned instance on which it returns the wrong
coarse value. -/

/-- The naive rule the source warns against: build the coarse mass at time `t` by adding up
the whole fine cells that end at or before `t`, discarding the fine cell straddling `t`. -/
noncomputable def wholeCellSum {Nf : ℕ} (y : Fin (Nf + 1) → ℝ) (r : Fin Nf → Fin n → ℝ)
    (i : Fin n) (t : ℝ) : ℝ :=
  ∑ j : Fin Nf, if y j.succ ≤ t then r j i * cellLength y j else 0

/-- The fine grid `0 < 1 < 2` of the nonaligned example. -/
noncomputable def nonalignedFine : Fin 3 → ℝ := ![0, 1, 2]

/-- Its rates: mode `0` throughout the first fine cell, mode `1` throughout the second. -/
noncomputable def nonalignedRates : Fin 2 → Fin 2 → ℝ := ![![1, 0], ![0, 1]]

/-- The coarse grid `0 < 1/2 < 2`; its interior node `1/2` is not a fine node. -/
noncomputable def nonalignedCoarse : Fin 3 → ℝ := ![0, 1 / 2, 2]

/-- The fine grid of the nonaligned example is a grid on the horizon `2`. -/
theorem isGrid_nonalignedFine : IsGrid nonalignedFine 2 := by
  refine ⟨rfl, rfl, Fin.strictMono_iff_lt_succ.mpr fun i => ?_⟩
  fin_cases i
  · change (0 : ℝ) < 1
    norm_num
  · change (1 : ℝ) < 2
    norm_num

/-- The coarse grid of the nonaligned example is a grid on the same horizon. -/
theorem isGrid_nonalignedCoarse : IsGrid nonalignedCoarse 2 := by
  refine ⟨rfl, rfl, Fin.strictMono_iff_lt_succ.mpr fun i => ?_⟩
  fin_cases i
  · change (0 : ℝ) < 1 / 2
    norm_num
  · change (1 : ℝ) / 2 < 2
    norm_num

/-- Its rates form a rate matrix. -/
theorem isRateMatrix_nonalignedRates : IsRateMatrix nonalignedRates := by
  constructor
  · intro j i
    fin_cases j <;> fin_cases i <;> norm_num [nonalignedRates]
  · intro j
    fin_cases j <;> simp [nonalignedRates, Fin.sum_univ_two]

/-- The grids really are nonaligned: the interior coarse node is not a node of the fine
grid. -/
theorem nonalignedCoarse_one_notMem_range : nonalignedCoarse 1 ∉ Set.range nonalignedFine := by
  rintro ⟨j, hj⟩
  fin_cases j <;> norm_num [nonalignedFine, nonalignedCoarse] at hj

/-- The exact coarse cumulative value at the nonaligned coarse node is `1/2`. -/
theorem gridCumulative_nonaligned :
    gridCumulative nonalignedFine nonalignedRates 0 (nonalignedCoarse 1) = 1 / 2 := by
  norm_num [gridCumulative, nonalignedFine, nonalignedCoarse, nonalignedRates,
    Fin.sum_univ_two, min_def]

/-- Grouping whole fine cells returns `0` there, discarding the half of the first fine cell
that lies to the left of the coarse node. -/
theorem wholeCellSum_nonaligned :
    wholeCellSum nonalignedFine nonalignedRates 0 (nonalignedCoarse 1) = 0 := by
  norm_num [wholeCellSum, cellLength, nonalignedFine, nonalignedCoarse, nonalignedRates,
    Fin.sum_univ_two]

/-- **The source's caveat is justified.** On a nonaligned pair of grids, grouping whole fine
cells gives the wrong coarse cumulative value; only a sum over the segments of the common
refinement, as in `gridCumulative_coarseNode_eq_refinementSum`, is correct. -/
theorem wholeCellSum_ne_gridCumulative :
    wholeCellSum nonalignedFine nonalignedRates 0 (nonalignedCoarse 1) ≠
      gridCumulative nonalignedFine nonalignedRates 0 (nonalignedCoarse 1) := by
  rw [wholeCellSum_nonaligned, gridCumulative_nonaligned]
  norm_num

end GridSwitching
