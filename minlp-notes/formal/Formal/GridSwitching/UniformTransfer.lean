import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint
import Formal.GridSwitching.Rounding

/-!
# SC24: sharp transfer on a uniform grid

This module proves `thm:sharp-transfer` of
`paper-switching-control/sections/11-transfer-and-coarsening.tex`: on a uniform grid of width
`h`, every finitely switching schedule `W` has a grid schedule `V` with no more activation
blocks and `‖V - W‖_∞ < h`.

The three ingredients are already available.

* `Rounding.exists_supported_rounding`, the rounding lemma in the matrix form that CLAIMS SC24
  states, selects one mode per cell with prefix counts pinned between the floor and the ceiling
  of the fractional prefix masses, supported where the cell occupation is positive. The sources
  derive that lemma from integral network-flow feasibility; here it comes from Hall's marriage
  theorem.
* `Rounding.exists_blockIndex`, `Rounding.isGridSchedule_comp_blockMap` and
  `Rounding.exists_subsequence_blockMap` turn the support property into the block-budget and
  word claims: the word of `V` is the original word with the blocks that no cell selected
  contracted to zero length, equivalently a chronological subsequence of it.
* `Rounding.occupation_cellword_node`, `Rounding.sum_cells_telescope` and
  `Rounding.D_lt_of_nodes` turn the grid-node bounds into the strict uniform bound, using that
  only finitely many node values occur.

Uniformity of the grid is used twice, both times in `exists_blockMap_uniform`. It normalizes
the rows: every row of the occupation matrix is a point of the simplex, so that each cell
supplies one unit of assignment capacity. It also converts counts of selected cells into node
values of the rounded schedule, each selected cell contributing exactly `h`.
-/

namespace GridSwitching

open Set

variable {n N k : ℕ}

/-! ## The uniform grid -/

/-- The uniform grid with `N` cells of width `h`. -/
noncomputable def uniformGrid (N : ℕ) (h : ℝ) : Fin (N + 1) → ℝ := fun q => (q : ℕ) * h

/-- The uniform grid is a grid on the horizon `N * h`. -/
theorem isGrid_uniformGrid {h : ℝ} (hh : 0 < h) :
    IsGrid (uniformGrid N h) ((N : ℝ) * h) := by
  refine ⟨by simp [uniformGrid], by simp [uniformGrid], fun q q' hqq => ?_⟩
  simp only [uniformGrid]
  have : ((q : ℕ) : ℝ) < ((q' : ℕ) : ℝ) := by exact_mod_cast Fin.lt_def.mp hqq
  exact mul_lt_mul_of_pos_right this hh

/-- Every cell of the uniform grid has width `h`. -/
theorem cellLength_uniformGrid {h : ℝ} (j : Fin N) : cellLength (uniformGrid N h) j = h := by
  simp only [cellLength, uniformGrid, Fin.val_succ, Fin.val_castSucc]
  push_cast
  ring

/-! ## The cellwise selection

The selection is `Rounding.exists_supported_rounding` applied to the occupation matrix of the
cells, normalized by the cell width:

  `a j i = (W i (x j.succ) - W i (x j.castSucc)) / h`.

Uniformity of the grid is used twice in `exists_blockMap_uniform`. In `hcellsum` it makes every
row of `a` a point of the simplex, so that each cell supplies one unit of assignment capacity.
In `hVnode` it converts the count of cells selecting a mode before a node into that mode's node
value, `h` times the count. -/

/-- SC24's selection step: a monotone block map into the original word whose cellwise word is
uniformly within `h` of the original schedule. Both public forms of the transfer theorem are
read off from this one construction. -/
private theorem exists_blockMap_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} (hτ : OrderedTimes τ T) :
    ∃ β : Fin N → Fin k, Monotone β ∧
      D (occupation p τ) (occupation (fun j => p (β j)) x) T < h := by
  classical
  have hxm : Monotone x := hx.strictMono.monotone
  have hWcum : IsCumulative (occupation p τ) T := occupation_isCumulative p hτ
  set a : Fin N → Fin n → ℝ :=
    fun j i => (occupation p τ i (x j.succ) - occupation p τ i (x j.castSucc)) / h with hadef
  have haval : ∀ (j : Fin N) (i : Fin n),
      a j i = (occupation p τ i (x j.succ) - occupation p τ i (x j.castSucc)) / h :=
    fun _ _ => rfl
  have hcellsum : ∀ j : Fin N,
      ∑ i, (occupation p τ i (x j.succ) - occupation p τ i (x j.castSucc)) = h := by
    intro j
    have hc := hunif j
    rw [cellLength] at hc
    rw [Finset.sum_sub_distrib, occupation_sum p hτ (x j.succ),
      occupation_sum p hτ (x j.castSucc), min_eq_left (hx.mem_Icc j.succ).2,
      min_eq_right (hx.mem_Icc j.succ).1, min_eq_left (hx.mem_Icc j.castSucc).2,
      min_eq_right (hx.mem_Icc j.castSucc).1]
    linarith
  have ha : ∀ j i, 0 ≤ a j i := by
    intro j i
    rw [haval]
    have hm := occupation_mono (p := p) hτ.mono i (hxm (Fin.castSucc_le_succ j))
    exact div_nonneg (by linarith) hh.le
  have hrow : ∀ j, ∑ i, a j i = 1 := by
    intro j
    simp only [haval]
    rw [← Finset.sum_div, hcellsum j, div_self (ne_of_gt hh)]
  obtain ⟨z, hzsupp, hzcount⟩ := exists_supported_rounding a ha hrow
  have hsupp : ∀ j : Fin N,
      0 < occupation p τ (z j) (x j.succ) - occupation p τ (z j) (x j.castSucc) := by
    intro j
    have hpos := hzsupp j
    rw [haval, div_pos_iff_of_pos_right hh] at hpos
    exact hpos
  choose β hβ1 hβ2 hβ3 using fun j : Fin N =>
    exists_blockIndex hτ.mono (hxm (Fin.castSucc_le_succ j)) (hsupp j)
  have hβmono : Monotone β := blockMap_monotone hxm hτ.mono (fun j => hβ2 j) (fun j => hβ3 j)
  have hzcomp : z = fun j => p (β j) := funext fun j => (hβ1 j).symm
  have hVgrid : IsGridSchedule x k (occupation z x) := by
    rw [hzcomp]
    exact isGridSchedule_comp_blockMap x p hβmono
  refine ⟨β, hβmono, ?_⟩
  rw [← hzcomp]
  refine D_lt_of_nodes hn hx hWcum hVgrid fun q i => ?_
  have hqle : (q : ℕ) ≤ N := Nat.lt_succ_iff.mp q.2
  obtain ⟨hfl, hce⟩ := hzcount (q : ℕ) hqle i
  set Sq : ℝ := ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < (q : ℕ), a j i with hSqdef
  set cq : ℕ :=
    (Finset.univ.filter fun j : Fin N => (j : ℕ) < (q : ℕ) ∧ z j = i).card with hcqdef
  have hSnonneg : 0 ≤ Sq := by
    rw [hSqdef]
    exact Finset.sum_nonneg fun j _ => ha j i
  have hWnode : occupation p τ i (x q) = h * Sq := by
    have hterm : ∀ j : Fin N,
        h * a j i = occupation p τ i (x j.succ) - occupation p τ i (x j.castSucc) := by
      intro j
      rw [haval]
      field_simp
    have htel := sum_cells_telescope (fun q' => occupation p τ i (x q')) q
    rw [hSqdef, Finset.mul_sum, Finset.sum_congr rfl fun j _ => hterm j, htel, hx.first,
      occupation_zero hτ, sub_zero]
  have hVnode : occupation z x i (x q) = h * (cq : ℝ) := by
    rw [occupation_cellword_node hx z i q, Finset.sum_congr rfl fun j _ => hunif j,
      Finset.sum_const, nsmul_eq_mul, hcqdef]
    ring
  have hlow : (cq : ℝ) < Sq + 1 := by
    have h1 : (cq : ℝ) ≤ (⌈Sq⌉₊ : ℝ) := by exact_mod_cast hce
    have h2 := Nat.ceil_lt_add_one hSnonneg
    linarith
  have hhigh : Sq - 1 < (cq : ℝ) := by
    have h1 : (⌊Sq⌋₊ : ℝ) ≤ (cq : ℝ) := by exact_mod_cast hfl
    have h2 := Nat.lt_floor_add_one Sq
    linarith
  rw [hWnode, hVnode, abs_lt]
  constructor
  · nlinarith [mul_pos hh (show (0 : ℝ) < Sq + 1 - (cq : ℝ) by linarith)]
  · nlinarith [mul_pos hh (show (0 : ℝ) < (cq : ℝ) - (Sq - 1) by linarith)]

/-! ## SC24 -/

/-- SC24 (`thm:sharp-transfer`), with the word claim as the sources state it: the transferred
schedule is the occupation of a **chronological subsequence** `p ∘ σ` of the original block
word, `σ` strictly monotone, with at most `c ≤ k` blocks and switch times at grid nodes, and
its discrepancy is strictly below `h`. -/
theorem exists_subsequence_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} (hτ : OrderedTimes τ T) :
    ∃ (c : ℕ) (σ : Fin c → Fin k) (g : Fin (c + 1) → Fin (N + 1)),
      StrictMono σ ∧ c ≤ k ∧ Monotone g ∧ g 0 = 0 ∧ g (Fin.last c) = Fin.last N ∧
        D (occupation p τ) (occupation (fun m => p (σ m)) (x ∘ g)) T < h := by
  obtain ⟨β, hβmono, hD⟩ := exists_blockMap_uniform hn hx hh hunif p hτ
  obtain ⟨c, σ, g, hσ, hck, hg, hg0, hgl, -, -, heq⟩ := exists_subsequence_blockMap x p hβmono
  exact ⟨c, σ, g, hσ, hck, hg, hg0, hgl, heq ▸ hD⟩

/-- SC24 (`thm:sharp-transfer`), with the block boundaries explicit: on a uniform grid of width
`h` the transferred schedule keeps the **original word** `p` and only moves the block
boundaries to grid nodes, some blocks possibly being contracted to zero length. Deleting those
is `exists_subsequence_uniform`. The discrepancy is strictly below `h`. -/
theorem exists_blockNodes_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} (hτ : OrderedTimes τ T) :
    ∃ g : Fin (k + 1) → Fin (N + 1), Monotone g ∧ g 0 = 0 ∧ g (Fin.last k) = Fin.last N ∧
      D (occupation p τ) (occupation p (x ∘ g)) T < h := by
  obtain ⟨β, hβmono, hD⟩ := exists_blockMap_uniform hn hx hh hunif p hτ
  refine ⟨fun m => blockNode β (m : ℕ), blockNode_monotone β, blockNode_zero β,
    blockNode_last β, ?_⟩
  rw [← occupation_comp_blockMap x p hβmono]
  exact hD

/-- SC24 (`thm:sharp-transfer`): on a uniform grid of width `h`, every schedule with `k`
activation blocks has a grid schedule with the same block budget, hence no more switches, whose
discrepancy is strictly below `h`. -/
theorem exists_isGridSchedule_uniform (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T h : ℝ}
    (hx : IsGrid x T) (hh : 0 < h) (hunif : ∀ j : Fin N, cellLength x j = h)
    {W : Fin n → ℝ → ℝ} (hW : IsSchedule k T W) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule x k V ∧ D W V T < h := by
  obtain ⟨p, τ, hτ, rfl⟩ := hW
  obtain ⟨g, hgmono, hg0, hgl, hD⟩ := exists_blockNodes_uniform hn hx hh hunif p hτ
  exact ⟨occupation p (x ∘ g), ⟨p, g, hgmono, hg0, hgl, rfl⟩, hD⟩

/-- SC24 on the uniform grid itself: the hypotheses of `exists_isGridSchedule_uniform` are met
by `uniformGrid`, so the transfer statement is not vacuous. -/
theorem exists_isGridSchedule_uniformGrid (hn : 0 < n) {h : ℝ} (hh : 0 < h)
    {W : Fin n → ℝ → ℝ} (hW : IsSchedule k ((N : ℝ) * h) W) :
    ∃ V : Fin n → ℝ → ℝ, IsGridSchedule (uniformGrid N h) k V ∧ D W V ((N : ℝ) * h) < h :=
  exists_isGridSchedule_uniform hn (isGrid_uniformGrid hh) hh
    (fun j => cellLength_uniformGrid j) hW

end GridSwitching
