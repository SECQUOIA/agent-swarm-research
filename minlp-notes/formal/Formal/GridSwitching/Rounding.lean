import Mathlib
import Formal.GridSwitching.Model
import Formal.GridSwitching.Endpoint

/-!
# Supported rounding: assembling a grid schedule from a monotone block map

This module contains the combinatorial core shared by the two transfer results of
`topics/17-grid-switching/CLAIMS.md`, SC24 and SC27.

A transfer construction selects one mode `y j` per grid cell `j`. Two things must then be
proved about the resulting cellwise word `y : Fin N → Fin n`: that its cumulative occupation
is close to the original schedule (an analytic statement, proved separately for each transfer
result), and that it uses no more activation blocks than the original word (a combinatorial
statement, proved here once and for all).

The combinatorial statement is organized around a *block map* `β : Fin N → Fin k` sending each
grid cell to an index of the original word, with `y = p ∘ β`. Two facts are proved.

* `exists_blockIndex`: if the original schedule occupies mode `i` for a positive amount of time
  on a cell, some original block carries mode `i` and overlaps the cell in positive length.
  This is the support hypothesis of the sources, in the form the chronology argument needs.
* `monotone_of_overlap`: cell-overlapping blocks are chronologically ordered, so *any* choice of
  an overlapping block per cell is automatically monotone. No minimality rule is needed.
* `isGridSchedule_of_comp`: if `β` is monotone then `occupation (p ∘ β) x` is a grid schedule
  with the *same* block budget `k` as the original word. Its word is literally the original
  word `p`, with the blocks not selected by any cell contracted to zero length; merging
  adjacent equal labels is then the already available `Model.isSchedule_of_card_positiveBlocks`
  and is not needed for the budget claim.

Nothing in this module refers to the number of modes, so both transfer results can use it.
-/

namespace GridSwitching

open Finset

variable {n N k : ℕ}

/-! ## Grid indices attached to a block map -/

/-- The number of grid cells that the block map `β` assigns to an original block of index
below `m`. As `m` runs over `0, 1, ..., k` these counts are the grid indices at which the
transferred schedule switches blocks. -/
def blockCellCount (β : Fin N → Fin k) (m : ℕ) : ℕ :=
  (Finset.univ.filter fun j : Fin N => (β j : ℕ) < m).card

theorem blockCellCount_le (β : Fin N → Fin k) (m : ℕ) : blockCellCount β m ≤ N := by
  simpa [blockCellCount] using card_filter_le (Finset.univ : Finset (Fin N))
    fun j => (β j : ℕ) < m

theorem blockCellCount_mono (β : Fin N → Fin k) : Monotone (blockCellCount β) := by
  intro m m' hm
  refine card_le_card fun j hj => ?_
  simp only [Finset.mem_filter_univ] at hj ⊢
  exact hj.trans_le hm

@[simp] theorem blockCellCount_zero (β : Fin N → Fin k) : blockCellCount β 0 = 0 := by
  simp [blockCellCount]

theorem blockCellCount_of_le (β : Fin N → Fin k) {m : ℕ} (hm : k ≤ m) :
    blockCellCount β m = N := by
  have h : (Finset.univ.filter fun j : Fin N => (β j : ℕ) < m) = Finset.univ :=
    Finset.filter_true_of_mem fun j _ => (β j).2.trans_le hm
  rw [blockCellCount, h, card_univ, Fintype.card_fin]

/-- The characteristic property of `blockCellCount` for a monotone block map: cell `j` belongs
to a block of index below `m` exactly when `j` is below the `m`-th count. -/
theorem lt_blockCellCount_iff {β : Fin N → Fin k} (hβ : Monotone β) (j : Fin N) (m : ℕ) :
    (j : ℕ) < blockCellCount β m ↔ (β j : ℕ) < m := by
  constructor
  · intro hlt
    by_contra hcon
    have hcon' : m ≤ (β j : ℕ) := by omega
    have hcard : (Finset.univ.filter fun j' : Fin N => (β j' : ℕ) < m).card
        ≤ (Finset.range (j : ℕ)).card := by
      refine card_le_card_of_injOn (fun j' => (j' : ℕ)) (fun j' hj' => ?_)
        (fun a _ b _ hab => Fin.ext hab)
      simp only [Finset.mem_coe, Finset.mem_filter_univ] at hj'
      simp only [Finset.mem_coe, Finset.mem_range]
      by_contra hge
      have hmono : (β j : ℕ) ≤ (β j' : ℕ) := Fin.le_def.mp (hβ (Fin.le_def.mpr (by omega)))
      omega
    rw [Finset.card_range] at hcard
    rw [blockCellCount] at hlt
    omega
  · intro hlt
    have hcard : (Finset.range ((j : ℕ) + 1)).card
        ≤ (Finset.univ.filter fun j' : Fin N => (β j' : ℕ) < m).card := by
      refine card_le_card_of_injOn
        (fun u => (⟨min u (j : ℕ), lt_of_le_of_lt (min_le_right _ _) j.2⟩ : Fin N))
        (fun u hu => ?_) (fun a ha b hb hab => ?_)
      · simp only [Finset.mem_coe, Finset.mem_range] at hu
        simp only [Finset.mem_coe, Finset.mem_filter_univ]
        refine lt_of_le_of_lt ?_ hlt
        exact Fin.le_def.mp (hβ (Fin.le_def.mpr (min_le_right _ _)))
      · simp only [Finset.mem_coe, Finset.mem_range] at ha hb
        have h := Fin.mk.inj_iff.mp hab
        omega
    rw [Finset.card_range] at hcard
    rw [blockCellCount]
    omega

/-- The grid index at which the transferred schedule enters the `m`-th original block. -/
def blockNode (β : Fin N → Fin k) (m : ℕ) : Fin (N + 1) :=
  ⟨blockCellCount β m, Nat.lt_succ_of_le (blockCellCount_le β m)⟩

/-! ## Assembling the transferred schedule -/

/-- Telescoping a difference over a range of cell indices. -/
private theorem sum_Ico_telescope (f : ℕ → ℝ) {u v : ℕ} (huv : u ≤ v) :
    ∑ w ∈ Finset.Ico u v, (f (w + 1) - f w) = f v - f u := by
  induction v, huv using Nat.le_induction with
  | base => simp
  | succ v hv ih => rw [Finset.sum_Ico_succ_top hv, ih]; ring

/-- The cumulative occupation of the cellwise word `p ∘ β` is the cumulative occupation of the
original word `p` with switch times at the block nodes of `β`. -/
theorem occupation_comp_blockMap (x : Fin (N + 1) → ℝ) (p : Fin k → Fin n)
    {β : Fin N → Fin k} (hβ : Monotone β) :
    occupation (fun j => p (β j)) x
      = occupation p (x ∘ fun m : Fin (k + 1) => blockNode β (m : ℕ)) := by
  funext i t
  set X : ℕ → ℝ := fun u => min t (x ⟨min u N, Nat.lt_succ_of_le (min_le_right _ _)⟩) with hXdef
  have hXcast : ∀ j : Fin N, X (j : ℕ) = min t (x j.castSucc) := by
    intro j
    simp only [hXdef]
    congr 2
    exact Fin.ext (by simp)
  have hXsucc : ∀ j : Fin N, X ((j : ℕ) + 1) = min t (x j.succ) := by
    intro j
    simp only [hXdef]
    congr 2
    exact Fin.ext (by simp)
  have hXnode : ∀ m : ℕ, X (blockCellCount β m) = min t (x (blockNode β m)) := by
    intro m
    simp only [hXdef, blockNode]
    congr 2
    exact Fin.ext (by simpa using Nat.min_eq_left (blockCellCount_le β m))
  have hcond : ∀ (m : Fin k) (j : Fin N), (β j = m) ↔
      (blockCellCount β (m : ℕ) ≤ (j : ℕ) ∧ (j : ℕ) < blockCellCount β ((m : ℕ) + 1)) := by
    intro m j
    have h1 := lt_blockCellCount_iff hβ j (m : ℕ)
    have h2 := lt_blockCellCount_iff hβ j ((m : ℕ) + 1)
    rw [Fin.ext_iff]
    omega
  have hfiber : ∀ m : Fin k,
      ∑ j ∈ Finset.univ.filter fun j : Fin N => β j = m, (X ((j : ℕ) + 1) - X (j : ℕ))
        = X (blockCellCount β ((m : ℕ) + 1)) - X (blockCellCount β (m : ℕ)) := by
    intro m
    have hle : blockCellCount β ((m : ℕ) + 1) ≤ N := blockCellCount_le β _
    calc ∑ j ∈ Finset.univ.filter fun j : Fin N => β j = m, (X ((j : ℕ) + 1) - X (j : ℕ))
        = ∑ j : Fin N, if blockCellCount β (m : ℕ) ≤ (j : ℕ) ∧
            (j : ℕ) < blockCellCount β ((m : ℕ) + 1) then X ((j : ℕ) + 1) - X (j : ℕ) else 0 := by
          rw [Finset.sum_filter]
          exact Finset.sum_congr rfl fun j _ => if_congr (hcond m j) rfl rfl
      _ = ∑ u ∈ Finset.range N, if blockCellCount β (m : ℕ) ≤ u ∧
            u < blockCellCount β ((m : ℕ) + 1) then X (u + 1) - X u else 0 :=
          Fin.sum_univ_eq_sum_range (fun u => if blockCellCount β (m : ℕ) ≤ u ∧
            u < blockCellCount β ((m : ℕ) + 1) then X (u + 1) - X u else 0) N
      _ = ∑ u ∈ Finset.Ico (blockCellCount β (m : ℕ)) (blockCellCount β ((m : ℕ) + 1)),
            (X (u + 1) - X u) := by
          rw [← Finset.sum_filter]
          refine Finset.sum_congr (Finset.ext fun u => ?_) fun _ _ => rfl
          simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
          omega
      _ = X (blockCellCount β ((m : ℕ) + 1)) - X (blockCellCount β (m : ℕ)) :=
          sum_Ico_telescope X (blockCellCount_mono β (by omega))
  have hleft : occupation (fun j => p (β j)) x i t
      = ∑ j : Fin N, if p (β j) = i then X ((j : ℕ) + 1) - X (j : ℕ) else 0 := by
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [hXcast j, hXsucc j]
  rw [hleft, ← Finset.sum_fiberwise Finset.univ β
    fun j => if p (β j) = i then X ((j : ℕ) + 1) - X (j : ℕ) else 0]
  refine Finset.sum_congr rfl fun m _ => ?_
  have hterm : ∑ j ∈ Finset.univ.filter fun j : Fin N => β j = m,
      (if p (β j) = i then X ((j : ℕ) + 1) - X (j : ℕ) else 0)
      = ∑ j ∈ Finset.univ.filter fun j : Fin N => β j = m,
      (if p m = i then X ((j : ℕ) + 1) - X (j : ℕ) else 0) := by
    refine Finset.sum_congr rfl fun j hj => ?_
    rw [(Finset.mem_filter.mp hj).2]
  rw [hterm]
  by_cases hpm : p m = i
  · simp only [if_pos hpm]
    rw [hfiber m, hXnode, hXnode]
    simp
  · simp [hpm]

/-- Block nodes are ordered by block index. -/
theorem blockNode_monotone (β : Fin N → Fin k) :
    Monotone fun m : Fin (k + 1) => blockNode β (m : ℕ) := fun _ _ hmm =>
  Fin.le_def.mpr (blockCellCount_mono β (Fin.le_def.mp hmm))

/-- The first block starts at the first grid node. -/
theorem blockNode_zero (β : Fin N → Fin k) : blockNode β ((0 : Fin (k + 1)) : ℕ) = 0 :=
  Fin.ext (by simp [blockNode])

/-- The last block ends at the last grid node. -/
theorem blockNode_last (β : Fin N → Fin k) :
    blockNode β ((Fin.last k : Fin (k + 1)) : ℕ) = Fin.last N :=
  Fin.ext (by simp [blockNode, blockCellCount_of_le β (le_refl k)])

/-- SC24 and SC27, switch budget: a cellwise word induced by a monotone block map into the
original word is a grid schedule with the same block budget, hence with no more switches. -/
theorem isGridSchedule_comp_blockMap (x : Fin (N + 1) → ℝ) (p : Fin k → Fin n)
    {β : Fin N → Fin k} (hβ : Monotone β) :
    IsGridSchedule x k (occupation (fun j => p (β j)) x) :=
  ⟨p, fun m => blockNode β (m : ℕ), blockNode_monotone β, blockNode_zero β, blockNode_last β,
    occupation_comp_blockMap x p hβ⟩

/-! ## The transferred word is a chronological subsequence

`isGridSchedule_comp_blockMap` keeps the original word `p` and contracts the blocks that no cell
selected to zero length. Deleting those blocks is what the sources describe as passing to a
chronological subsequence, and `exists_subsequence_blockMap` says exactly that: the transferred
schedule is the occupation of `p ∘ σ` for a **strictly monotone** index map `σ : Fin c → Fin k`,
with `c ≤ k` blocks and switch times at grid nodes. A strictly monotone index map is precisely
the statement that `p ∘ σ` is a subsequence of `p` taken in chronological order; every block of
`p ∘ σ` is selected by at least one cell, so none of them is spurious. Merging adjacent equal
labels, which `Model.occupation_merge` shows does not change the occupation, can only shorten
the word further and is therefore not needed for the budget claim. -/

/-- SC24's word claim: the cellwise word of a monotone block map is the occupation of a
chronological subsequence `p ∘ σ` of the original word, with switch times at grid nodes. -/
theorem exists_subsequence_blockMap (x : Fin (N + 1) → ℝ) (p : Fin k → Fin n)
    {β : Fin N → Fin k} (hβ : Monotone β) :
    ∃ (c : ℕ) (σ : Fin c → Fin k) (g : Fin (c + 1) → Fin (N + 1)),
      StrictMono σ ∧ c ≤ k ∧ Monotone g ∧ g 0 = 0 ∧ g (Fin.last c) = Fin.last N ∧
        (∀ j : Fin N, ∃ m : Fin c, σ m = β j) ∧ (∀ m : Fin c, ∃ j : Fin N, β j = σ m) ∧
        occupation (fun j => p (β j)) x = occupation (fun m => p (σ m)) (x ∘ g) := by
  classical
  set U : Finset (Fin k) := Finset.image β Finset.univ with hU
  set σ : Fin U.card → Fin k := ⇑(U.orderEmbOfFin rfl) with hσdef
  have hσmono : StrictMono σ := (U.orderEmbOfFin rfl).strictMono
  have hrange : ∀ j : Fin N, ∃ m : Fin U.card, σ m = β j := by
    intro j
    have hmem : β j ∈ U := Finset.mem_image.mpr ⟨j, Finset.mem_univ j, rfl⟩
    have hr : β j ∈ Set.range σ := by
      rw [hσdef, Finset.range_orderEmbOfFin]
      exact hmem
    exact hr
  choose γ hγ using hrange
  have hγmono : Monotone γ := by
    intro j j' hjj
    have h1 : σ (γ j) ≤ σ (γ j') := by
      rw [hγ j, hγ j']
      exact hβ hjj
    exact hσmono.le_iff_le.mp h1
  have hused : ∀ m : Fin U.card, ∃ j : Fin N, β j = σ m := by
    intro m
    have hmem : σ m ∈ U := by
      rw [hσdef]
      exact U.orderEmbOfFin_mem rfl m
    obtain ⟨j, -, hj⟩ := Finset.mem_image.mp (hU ▸ hmem)
    exact ⟨j, hj⟩
  refine ⟨U.card, σ, fun m => blockNode γ (m : ℕ), hσmono, ?_, blockNode_monotone γ,
    blockNode_zero γ, blockNode_last γ, fun j => ⟨γ j, hγ j⟩, hused, ?_⟩
  · calc U.card ≤ (Finset.univ : Finset (Fin k)).card :=
          Finset.card_le_card (Finset.subset_univ U)
      _ = k := by simp
  · have hcomp : (fun j => p (β j)) = fun j => (fun m => p (σ m)) (γ j) := by
      funext j
      change p (β j) = p (σ (γ j))
      rw [hγ j]
    rw [hcomp]
    exact occupation_comp_blockMap x (fun m => p (σ m)) hγmono

/-! ## Support and chronology -/

/-- Positive occupation of a mode over a time interval is carried by a block of that mode which
overlaps the interval in positive length. This is the support statement the chronological
argument of `thm:sharp-transfer` needs. -/
theorem exists_blockIndex {p : Fin k → Fin n} {τ : Fin (k + 1) → ℝ} (hτ : Monotone τ)
    {i : Fin n} {a b : ℝ} (hab : a ≤ b)
    (hpos : 0 < occupation p τ i b - occupation p τ i a) :
    ∃ m : Fin k, p m = i ∧ τ m.castSucc < b ∧ a < τ m.succ := by
  by_contra hcon
  push Not at hcon
  have hle : occupation p τ i b - occupation p τ i a ≤ 0 := by
    simp only [occupation, ← Finset.sum_sub_distrib]
    refine Finset.sum_nonpos fun m _ => ?_
    by_cases hpm : p m = i
    · simp only [if_pos hpm]
      have hmono : τ m.castSucc ≤ τ m.succ := hτ (Fin.castSucc_le_succ m)
      rcases le_or_gt b (τ m.castSucc) with hb | hb
      · rw [min_eq_left hb, min_eq_left (hb.trans hmono), min_eq_left (hab.trans hb),
          min_eq_left ((hab.trans hb).trans hmono)]
        ring_nf
        exact le_refl 0
      · have ha : τ m.succ ≤ a := hcon m hpm hb
        rw [min_eq_right (ha.trans hab), min_eq_right ((hmono.trans ha).trans hab),
          min_eq_right ha, min_eq_right (hmono.trans ha)]
        ring_nf
        exact le_refl 0
    · simp [hpm]
  linarith

/-- Chronology: blocks overlapping the cells of a grid in positive length are ordered exactly as
the cells are, so *every* choice of an overlapping block per cell is a monotone block map. -/
theorem blockMap_monotone {x : Fin (N + 1) → ℝ} (hx : Monotone x) {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) {β : Fin N → Fin k}
    (h1 : ∀ j : Fin N, τ (β j).castSucc < x j.succ)
    (h2 : ∀ j : Fin N, x j.castSucc < τ (β j).succ) :
    Monotone β := by
  intro j j' hjj
  by_contra hcon
  push Not at hcon
  have hjlt : j < j' := by
    rcases eq_or_lt_of_le hjj with rfl | h
    · exact absurd hcon (lt_irrefl _)
    · exact h
  have hτle : τ (β j').succ ≤ τ (β j).castSucc :=
    hτ (Fin.le_def.mpr (by simpa using Fin.lt_def.mp hcon))
  have hxle : x j.succ ≤ x j'.castSucc :=
    hx (Fin.le_def.mpr (by simpa using Fin.lt_def.mp hjlt))
  linarith [h1 j, h2 j']

/-! ## Unit-interval clamping

The rounding lemma below is proved by a counting argument on the "mass line" of each mode: the
cumulative mass of mode `i` is a subinterval of `[0, R i]`, cell `u` occupies the segment
between two consecutive cumulative values, and the integral tokens of mode `i` are the unit
intervals `[r-1, r]` for `1 ≤ r ≤ R i`. `unitClamp r x` is the part of `[0, x]` lying in the
`r`-th unit interval, measured from `r - 1`. -/

/-- `x` clamped into the `r`-th unit interval `[r - 1, r]`. -/
private noncomputable def unitClamp (r : ℕ) (x : ℝ) : ℝ := min (max x ((r : ℝ) - 1)) r

private theorem unitClamp_mono (r : ℕ) {x y : ℝ} (h : x ≤ y) : unitClamp r x ≤ unitClamp r y :=
  min_le_min (max_le_max h (le_refl _)) (le_refl _)

private theorem unitClamp_le (r : ℕ) (x : ℝ) : unitClamp r x ≤ r := min_le_right _ _

private theorem le_unitClamp (r : ℕ) {x : ℝ} (hr : 1 ≤ r) : (r : ℝ) - 1 ≤ unitClamp r x := by
  refine le_min (le_max_right _ _) ?_
  have : (1 : ℝ) ≤ r := by exact_mod_cast hr
  linarith

/-- Summing the clamps over all unit intervals recovers the mass, capped at `R`. -/
private theorem sum_unitClamp (R : ℕ) {x : ℝ} (hx : 0 ≤ x) :
    ∑ r ∈ Finset.Icc 1 R, (unitClamp r x - ((r : ℝ) - 1)) = min x R := by
  induction R with
  | zero => simpa using (min_eq_right hx).symm
  | succ R ih =>
    rw [Finset.sum_Icc_succ_top (by omega), ih]
    simp only [unitClamp, min_def, max_def]
    push_cast
    split_ifs <;> linarith

/-- Summing the clamped increments over all unit intervals recovers the increment. -/
private theorem sum_unitClamp_sub (R : ℕ) {x y : ℝ} (hx : 0 ≤ x) (hxy : x ≤ y) (hy : y ≤ R) :
    ∑ r ∈ Finset.Icc 1 R, (unitClamp r y - unitClamp r x) = y - x := by
  have h : ∀ z : ℝ, 0 ≤ z → ∑ r ∈ Finset.Icc 1 R, (unitClamp r z - ((r : ℝ) - 1)) = min z R :=
    fun z hz => sum_unitClamp R hz
  have hsub : ∑ r ∈ Finset.Icc 1 R, (unitClamp r y - unitClamp r x)
      = (∑ r ∈ Finset.Icc 1 R, (unitClamp r y - ((r : ℝ) - 1)))
        - ∑ r ∈ Finset.Icc 1 R, (unitClamp r x - ((r : ℝ) - 1)) := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun r _ => by ring
  rw [hsub, h y (hx.trans hxy), h x hx, min_eq_left hy, min_eq_left (hxy.trans hy)]

/-! ## SC24, combinatorial core: supported integral prefix rounding

`exists_prefix_rounding` is the rounding lemma the sources obtain from integral network-flow
feasibility. It is proved here from Hall's marriage theorem instead, which the pinned Mathlib
does provide.

The bipartite graph matches cells to *tokens*: token `(i, r)` is the `r`-th unit interval of
mode `i`'s mass line, and cell `u` is joined to it when the segment of the mass line that cell
`u` contributes to mode `i` meets that unit interval in positive length. Hall's condition is
verified by a mass count: for a set `C` of cells, the mass `C` contributes to mode `i` is at
most the number of tokens of mode `i` that `C` meets, because a single token can absorb at most
one unit of mass; summing over modes gives exactly `#C`. The token count is arranged to equal
the cell count, so Hall's injection is a bijection, and that is what forces the lower prefix
bounds as well as the upper ones. -/

/-- **Supported integral prefix rounding.** Let `P u i` be the cumulative mass of mode `i` after
`u` of `M` cells: it starts at zero, is nondecreasing, gains exactly one unit of total mass per
cell, and ends at an integer `R i` for every mode. Then one mode `y u` can be selected per cell
so that the selected mode has positive mass on its cell, and every prefix count is the floor or
the ceiling of the corresponding cumulative mass. -/
theorem exists_prefix_rounding {n M : ℕ} (P : ℕ → Fin n → ℝ) (R : Fin n → ℕ)
    (hP0 : ∀ i, P 0 i = 0) (hPmono : ∀ i, Monotone fun u => P u i)
    (hPstep : ∀ u, u < M → ∑ i, (P (u + 1) i - P u i) = 1)
    (hPlast : ∀ i, P M i = (R i : ℝ)) :
    ∃ y : Fin M → Fin n, (∀ u : Fin M, P (u : ℕ) (y u) < P ((u : ℕ) + 1) (y u)) ∧
      ∀ k ≤ M, ∀ i : Fin n,
        ⌊P k i⌋₊ ≤ (Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧ y u = i).card ∧
        (Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧ y u = i).card ≤ ⌈P k i⌉₊ := by
  classical
  have hPnonneg : ∀ u i, 0 ≤ P u i := by
    intro u i
    rw [← hP0 i]
    exact hPmono i (Nat.zero_le u)
  have hPle : ∀ u i, u ≤ M → P u i ≤ (R i : ℝ) := by
    intro u i h
    rw [← hPlast i]
    exact hPmono i h
  have hprefix : ∀ u, u ≤ M → ∑ i, P u i = (u : ℝ) := by
    intro u
    induction u with
    | zero => intro _; simp [hP0]
    | succ u ih =>
      intro hu
      have h1 := hPstep u (by omega)
      have h2 := ih (by omega)
      rw [Finset.sum_sub_distrib] at h1
      push_cast
      linarith
  have hRsum : (∑ i, R i) = M := by
    have hM := hprefix M le_rfl
    simp only [hPlast] at hM
    have hcast : ((∑ i, R i : ℕ) : ℝ) = (M : ℝ) := by push_cast; exact hM
    exact_mod_cast hcast
  set Tok : Finset ((_ : Fin n) × ℕ) := Finset.univ.sigma fun i => Finset.Icc 1 (R i) with hTok
  have hcardTok : Tok.card = M := by
    rw [hTok, Finset.card_sigma]
    simpa [Nat.card_Icc] using hRsum
  set ov : Fin M → Fin n → ℕ → ℝ :=
    fun u i r => unitClamp r (P ((u : ℕ) + 1) i) - unitClamp r (P (u : ℕ) i) with hovdef
  have hov_nonneg : ∀ u i r, 0 ≤ ov u i r := fun u i r =>
    sub_nonneg.mpr (unitClamp_mono r (hPmono i (Nat.le_succ _)))
  have hov_sum_r : ∀ (u : Fin M) (i : Fin n),
      ∑ r ∈ Finset.Icc 1 (R i), ov u i r = P ((u : ℕ) + 1) i - P (u : ℕ) i := fun u i =>
    sum_unitClamp_sub (R i) (hPnonneg _ i) (hPmono i (Nat.le_succ _)) (hPle _ i u.2)
  have hov_sum_u : ∀ (i : Fin n) (r : ℕ) (C : Finset (Fin M)), 1 ≤ r →
      ∑ u ∈ C, ov u i r ≤ 1 := by
    intro i r C hr
    have hle : ∑ u ∈ C, ov u i r ≤ ∑ u : Fin M, ov u i r :=
      Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ C) fun u _ _ => hov_nonneg u i r
    have htel : ∑ u : Fin M, ov u i r = unitClamp r (P M i) - unitClamp r (P 0 i) := by
      simp only [hovdef]
      rw [Fin.sum_univ_eq_sum_range
        (fun u => unitClamp r (P (u + 1) i) - unitClamp r (P u i)) M]
      exact Finset.sum_range_sub (fun u => unitClamp r (P u i)) M
    have h1 : unitClamp r (P M i) ≤ r := unitClamp_le r _
    have h2 : (r : ℝ) - 1 ≤ unitClamp r (P 0 i) := le_unitClamp r hr
    rw [htel] at hle
    linarith
  set tokOf : Fin M → Finset ((_ : Fin n) × ℕ) :=
    fun u => Finset.univ.sigma fun i => (Finset.Icc 1 (R i)).filter fun r => 0 < ov u i r
    with htokOf
  have hHall : ∀ C : Finset (Fin M), C.card ≤ (C.biUnion tokOf).card := by
    intro C
    set Adj : Fin n → Finset ℕ :=
      fun i => (Finset.Icc 1 (R i)).filter fun r => ∃ u ∈ C, 0 < ov u i r with hAdj
    have hbi : C.biUnion tokOf = Finset.univ.sigma Adj := by
      ext z
      simp only [Finset.mem_biUnion, htokOf, hAdj, Finset.mem_sigma, Finset.mem_filter,
        Finset.mem_univ, true_and]
      constructor
      · rintro ⟨u, huC, hz1, hz2⟩
        exact ⟨hz1, u, huC, hz2⟩
      · rintro ⟨hz1, u, huC, hz2⟩
        exact ⟨u, huC, hz1, hz2⟩
    rw [hbi, Finset.card_sigma]
    have key : (C.card : ℝ) ≤ ((∑ i, (Adj i).card : ℕ) : ℝ) := by
      have e1 : (C.card : ℝ) = ∑ u ∈ C, ∑ i, (P ((u : ℕ) + 1) i - P (u : ℕ) i) := by
        rw [Finset.sum_congr rfl fun (u : Fin M) _ => hPstep (u : ℕ) u.isLt]
        simp
      have e2 : ∑ u ∈ C, ∑ i, (P ((u : ℕ) + 1) i - P (u : ℕ) i)
          = ∑ i, ∑ u ∈ C, ∑ r ∈ Finset.Icc 1 (R i), ov u i r := by
        rw [Finset.sum_comm]
        exact Finset.sum_congr rfl fun i _ =>
          Finset.sum_congr rfl fun u _ => (hov_sum_r u i).symm
      rw [e1, e2]
      push_cast
      refine Finset.sum_le_sum fun i _ => ?_
      rw [Finset.sum_comm]
      have hsplit := Finset.sum_filter_add_sum_filter_not (Finset.Icc 1 (R i))
        (fun r => ∃ u ∈ C, 0 < ov u i r) fun r => ∑ u ∈ C, ov u i r
      have hzero : ∑ r ∈ (Finset.Icc 1 (R i)).filter (fun r => ¬∃ u ∈ C, 0 < ov u i r),
          ∑ u ∈ C, ov u i r = 0 := by
        refine Finset.sum_eq_zero fun r hr => ?_
        refine Finset.sum_eq_zero fun u hu => ?_
        have hnot := (Finset.mem_filter.mp hr).2
        push Not at hnot
        exact le_antisymm (hnot u hu) (hov_nonneg u i r)
      have hbound : ∑ r ∈ Adj i, ∑ u ∈ C, ov u i r ≤ ((Adj i).card : ℝ) := by
        calc ∑ r ∈ Adj i, ∑ u ∈ C, ov u i r ≤ ∑ _r ∈ Adj i, (1 : ℝ) := by
              refine Finset.sum_le_sum fun r hr => ?_
              exact hov_sum_u i r C (Finset.mem_Icc.mp (Finset.mem_filter.mp hr).1).1
          _ = ((Adj i).card : ℝ) := by simp
      rw [← hsplit, hzero, add_zero]
      exact hbound
    exact_mod_cast key
  obtain ⟨f, hfinj, hfmem⟩ :=
    (Finset.all_card_le_biUnion_card_iff_existsInjective' tokOf).mp hHall
  set y : Fin M → Fin n := fun u => (f u).1 with hydef
  have hfprop : ∀ u : Fin M, 1 ≤ (f u).2 ∧ (f u).2 ≤ R (y u) ∧ 0 < ov u (y u) (f u).2 := by
    intro u
    have h := hfmem u
    simp only [htokOf, Finset.mem_sigma, Finset.mem_filter, Finset.mem_univ, true_and,
      Finset.mem_Icc] at h
    exact ⟨h.1.1, h.1.2, h.2⟩
  have hsupp : ∀ u : Fin M, P (u : ℕ) (y u) < P ((u : ℕ) + 1) (y u) := by
    intro u
    obtain ⟨-, -, hpos⟩ := hfprop u
    by_contra hcon
    push Not at hcon
    simp only [hovdef] at hpos
    linarith [unitClamp_mono (f u).2 hcon]
  have hlow : ∀ u : Fin M, P (u : ℕ) (y u) < ((f u).2 : ℝ) := by
    intro u
    obtain ⟨hr1, -, hpos⟩ := hfprop u
    by_contra hcon
    push Not at hcon
    have heq : unitClamp (f u).2 (P (u : ℕ) (y u)) = ((f u).2 : ℝ) :=
      le_antisymm (unitClamp_le _ _) (le_min (le_max_of_le_left hcon) (le_refl _))
    have h2 := unitClamp_le (f u).2 (P ((u : ℕ) + 1) (y u))
    simp only [hovdef] at hpos
    linarith
  have hhigh : ∀ u : Fin M, ((f u).2 : ℝ) - 1 < P ((u : ℕ) + 1) (y u) := by
    intro u
    obtain ⟨hr1, -, hpos⟩ := hfprop u
    have hr1' : (1 : ℝ) ≤ ((f u).2 : ℝ) := by exact_mod_cast hr1
    by_contra hcon
    push Not at hcon
    have heq : unitClamp (f u).2 (P ((u : ℕ) + 1) (y u)) = ((f u).2 : ℝ) - 1 := by
      rw [unitClamp, max_eq_right hcon, min_eq_left (by linarith)]
    have h2 := le_unitClamp (f u).2 (x := P (u : ℕ) (y u)) hr1
    simp only [hovdef] at hpos
    linarith
  have himg : Finset.image f Finset.univ = Tok := by
    refine Finset.eq_of_subset_of_card_le (fun z hz => ?_) ?_
    · obtain ⟨u, -, rfl⟩ := Finset.mem_image.mp hz
      obtain ⟨h1, h2, -⟩ := hfprop u
      simp only [hTok, Finset.mem_sigma, Finset.mem_univ, true_and, Finset.mem_Icc]
      exact ⟨h1, h2⟩
    · rw [Finset.card_image_of_injective _ hfinj, Finset.card_univ, Fintype.card_fin, hcardTok]
  refine ⟨y, hsupp, fun k hk i => ⟨?_, ?_⟩⟩
  · -- lower bound: every low token of mode `i` is used by a cell before `k`
    have hsub : Finset.Icc 1 ⌊P k i⌋₊ ⊆
        (Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧ y u = i).image fun u => (f u).2 := by
      intro r hr
      obtain ⟨hr1, hr2⟩ := Finset.mem_Icc.mp hr
      have hrR : r ≤ R i := by
        refine le_trans hr2 ?_
        have : ⌊P k i⌋₊ ≤ ⌊(R i : ℝ)⌋₊ := Nat.floor_le_floor (hPle k i hk)
        simpa using this
      have hzmem : (⟨i, r⟩ : (_ : Fin n) × ℕ) ∈ Tok := by
        simp only [hTok, Finset.mem_sigma, Finset.mem_univ, true_and, Finset.mem_Icc]
        exact ⟨hr1, hrR⟩
      rw [← himg] at hzmem
      obtain ⟨u, -, hfu⟩ := Finset.mem_image.mp hzmem
      have hyu : y u = i := by
        simp only [hydef]
        rw [hfu]
      have hr' : (f u).2 = r := by rw [hfu]
      have hult : (u : ℕ) < k := by
        by_contra hcon
        push Not at hcon
        have h1 : P k i ≤ P (u : ℕ) i := hPmono i hcon
        have h2 := hlow u
        rw [hyu, hr'] at h2
        have h3 : (r : ℝ) ≤ P k i := by
          refine le_trans ?_ (Nat.floor_le (hPnonneg k i))
          exact_mod_cast hr2
        linarith
      refine Finset.mem_image.mpr ⟨u, ?_, hr'⟩
      simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      exact ⟨hult, hyu⟩
    have h1 := Finset.card_le_card hsub
    have h2 := Finset.card_image_le (s := Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧
      y u = i) (f := fun u => (f u).2)
    simp only [Nat.card_Icc] at h1
    omega
  · -- upper bound: the tokens used before `k` are low tokens
    have hmaps : ∀ u ∈ (Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧ y u = i),
        (f u).2 ∈ Finset.Icc 1 ⌈P k i⌉₊ := by
      intro u hu
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hu
      obtain ⟨hr1, -, -⟩ := hfprop u
      refine Finset.mem_Icc.mpr ⟨hr1, ?_⟩
      have h1 := hhigh u
      rw [hu.2] at h1
      have h2 : P ((u : ℕ) + 1) i ≤ P k i := hPmono i (by omega)
      have h3 : (((f u).2 - 1 : ℕ) : ℝ) < P k i := by
        rw [Nat.cast_sub hr1]
        push_cast
        linarith
      have h4 : (f u).2 - 1 < ⌈P k i⌉₊ := Nat.lt_ceil.mpr h3
      omega
    have hinj : Set.InjOn (fun u => (f u).2)
        ((Finset.univ.filter fun u : Fin M => (u : ℕ) < k ∧ y u = i) : Finset (Fin M)) := by
      intro a ha b hb hab
      simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_univ, true_and] at ha hb
      have ha2 : (f a).1 = i := by simpa only [hydef] using ha.2
      have hb2 : (f b).1 = i := by simpa only [hydef] using hb.2
      refine hfinj (Sigma.ext ?_ ?_)
      · rw [ha2, hb2]
      · simpa using hab
    have := Finset.card_le_card_of_injOn (fun u => (f u).2) hmaps hinj
    simpa [Nat.card_Icc] using this

/-! ## Grid-node evaluation and strict error bounds -/

/-- At a grid node, the occupation of a cellwise grid word is the total length of the earlier
cells carrying the given mode. -/
theorem occupation_cellword_node {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (y : Fin N → Fin n) (i : Fin n) (q : Fin (N + 1)) :
    occupation y x i (x q)
      = ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < (q : ℕ) ∧ y j = i, cellLength x j := by
  rw [Finset.sum_filter, occupation]
  refine Finset.sum_congr rfl fun j _ => ?_
  rcases lt_or_ge (j : ℕ) (q : ℕ) with hj | hj
  · have h1 : x j.succ ≤ x q :=
      hx.strictMono.monotone (Fin.le_def.mpr (by simpa using hj))
    have h2 : x j.castSucc ≤ x q :=
      hx.strictMono.monotone (Fin.le_def.mpr (by simpa using hj.le))
    rw [min_eq_right h1, min_eq_right h2]
    by_cases hy : y j = i
    · rw [if_pos hy, if_pos (⟨hj, hy⟩ : (j : ℕ) < (q : ℕ) ∧ y j = i), cellLength]
    · have hneg : ¬((j : ℕ) < (q : ℕ) ∧ y j = i) := fun hc => hy hc.2
      rw [if_neg hy, if_neg hneg]
  · have h2 : x q ≤ x j.castSucc :=
      hx.strictMono.monotone (Fin.le_def.mpr (by simpa using hj))
    have h1 : x q ≤ x j.succ := h2.trans (hx.strictMono.monotone (Fin.castSucc_le_succ j))
    have hneg : ¬((j : ℕ) < (q : ℕ) ∧ y j = i) := fun hc => absurd hc.1 (Nat.not_lt.mpr hj)
    rw [min_eq_left h1, min_eq_left h2, if_neg hneg]
    simp

/-- A strict error bound at every grid node is a strict error bound on the whole horizon: the
node values form a finite set, so their maximum is still strictly below the bound. -/
theorem D_lt_of_nodes (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {W V : Fin n → ℝ → ℝ} (hW : IsCumulative W T) (hV : IsGridSchedule x k V) {b : ℝ}
    (h : ∀ (q : Fin (N + 1)) (i : Fin n), |W i (x q) - V i (x q)| < b) : D W V T < b := by
  classical
  set E : Finset ℝ :=
    Finset.image (fun z : Fin (N + 1) × Fin n => |W z.2 (x z.1) - V z.2 (x z.1)|) Finset.univ
    with hE
  have hne : E.Nonempty := by
    refine ⟨|W ⟨0, hn⟩ (x 0) - V ⟨0, hn⟩ (x 0)|, ?_⟩
    exact Finset.mem_image.mpr ⟨(0, ⟨0, hn⟩), Finset.mem_univ _, rfl⟩
  have hmem := E.max'_mem hne
  obtain ⟨z, -, hz⟩ := Finset.mem_image.mp hmem
  have hmax0 : 0 ≤ E.max' hne := hz ▸ abs_nonneg _
  have hle : D W V T ≤ E.max' hne := by
    rw [gridSchedule_D_le_iff hx hV hW hmax0]
    intro q i
    exact Finset.le_max' E _ (Finset.mem_image.mpr ⟨(q, i), Finset.mem_univ _, rfl⟩)
  exact lt_of_le_of_lt hle (hz ▸ h z.1 z.2)

/-! ## Saturated grid nodes

Both transfer constructions run a recursion over all of `ℕ`, so the grid nodes are extended by
saturation at the last node: beyond the last cell all occupations and cell lengths vanish. -/

/-- The grid node of index `u`, saturated at the last node. -/
def satNode (N u : ℕ) : Fin (N + 1) := ⟨min u N, Nat.lt_succ_of_le (min_le_right _ _)⟩

/-- The saturated node at a cell index is that cell's left endpoint. -/
theorem satNode_castSucc (j : Fin N) : satNode N (j : ℕ) = j.castSucc :=
  Fin.ext (by simp [satNode])

/-- The saturated node one past a cell index is that cell's right endpoint. -/
theorem satNode_succ (j : Fin N) : satNode N ((j : ℕ) + 1) = j.succ :=
  Fin.ext (by simp [satNode])

/-- Saturation does nothing to an index that is already a node index. -/
theorem satNode_coe (q : Fin (N + 1)) : satNode N (q : ℕ) = q :=
  Fin.ext (by simp [satNode, Nat.min_eq_left (Nat.lt_succ_iff.mp q.2)])

/-- Saturated nodes are ordered by their index. -/
theorem satNode_mono : Monotone (satNode N) := fun _ _ huv =>
  Fin.le_def.mpr (by simpa [satNode] using min_le_min huv (le_refl N))

/-- Past the last cell the saturated node is the last node. -/
theorem satNode_of_le {u : ℕ} (h : N ≤ u) : satNode N u = Fin.last N :=
  Fin.ext (by simp [satNode, Nat.min_eq_right h])


/-- Telescoping a difference of node values over the cells before a node. -/
theorem sum_cells_telescope (F : Fin (N + 1) → ℝ) (q : Fin (N + 1)) :
    ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < (q : ℕ), (F j.succ - F j.castSucc)
      = F q - F 0 := by
  calc ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < (q : ℕ), (F j.succ - F j.castSucc)
      = ∑ j : Fin N, if (j : ℕ) < (q : ℕ) then
          F (satNode N ((j : ℕ) + 1)) - F (satNode N (j : ℕ)) else 0 := by
        rw [Finset.sum_filter]
        exact Finset.sum_congr rfl fun j _ => by rw [satNode_castSucc, satNode_succ]
    _ = ∑ u ∈ Finset.range N, if u < (q : ℕ) then
          F (satNode N (u + 1)) - F (satNode N u) else 0 :=
        Fin.sum_univ_eq_sum_range (fun u => if u < (q : ℕ) then
          F (satNode N (u + 1)) - F (satNode N u) else 0) N
    _ = ∑ u ∈ Finset.Ico 0 (q : ℕ), (F (satNode N (u + 1)) - F (satNode N u)) := by
        rw [← Finset.sum_filter]
        refine Finset.sum_congr (Finset.ext fun u => ?_) fun _ _ => rfl
        have hq : (q : ℕ) ≤ N := Nat.lt_succ_iff.mp q.2
        simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_Ico]
        omega
    _ = F (satNode N (q : ℕ)) - F (satNode N 0) :=
        sum_Ico_telescope (fun u => F (satNode N u)) (Nat.zero_le _)
    _ = F q - F 0 := by
        rw [satNode_coe q, show satNode N 0 = 0 from Fin.ext (by simp [satNode])]

/-- Counting selected cells before a grid node does not depend on whether the cells are indexed
by the grid or by the extended cell range used in the rounding lemma. -/
theorem card_filter_embed {M : ℕ} (hNM : N ≤ M) (y : Fin M → Fin n) {j : ℕ}
    (hj : j ≤ N) (i : Fin n) :
    (Finset.univ.filter fun c : Fin N =>
        (c : ℕ) < j ∧ y ⟨c, lt_of_lt_of_le c.2 hNM⟩ = i).card
      = (Finset.univ.filter fun u : Fin M => (u : ℕ) < j ∧ y u = i).card := by
  refine Finset.card_nbij (fun c : Fin N => (⟨c, lt_of_lt_of_le c.2 hNM⟩ : Fin M))
    (fun c hc => ?_) (fun a _ b _ hab => ?_) (fun u hu => ?_)
  · simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_univ, true_and] at hc ⊢
    exact hc
  · exact Fin.ext (by simpa using congrArg Fin.val hab)
  · simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_univ, true_and] at hu
    refine ⟨⟨(u : ℕ), by omega⟩, ?_, ?_⟩
    · simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_univ, true_and]
      exact ⟨hu.1, by simpa using hu.2⟩
    · exact Fin.ext rfl


/-! ## SC24, the rounding lemma in matrix form

`exists_prefix_rounding` asks the cumulative masses to end at integers. The form used by the
sources starts instead from a matrix of cell occupations whose rows are points of the simplex,
and its column sums need not be integral. The two are reconciled by padding: append
`Q = (∑ i, ⌈m i⌉) - N` fictitious cells, each carrying the rate vector `(⌈m i⌉ - m i) / Q`, so
that every column sum becomes an integer while every row still sums to one. Restricting the
selection back to the first `N` cells is harmless, because a fictitious cell carries only mass
lying above every prefix mass of a real cell. -/

/-- **SC24's combinatorial core, matrix form.** Let `a j i ≥ 0` with `∑ i, a j i = 1` for every
cell `j`, and let `S k i = ∑_{j < k} a j i`. There is a selection `y` of one mode per cell,
supported where the cell occupation is positive, whose prefix counts satisfy
`⌊S k i⌋ ≤ #{j < k | y j = i} ≤ ⌈S k i⌉`. The floors and ceilings are the natural-number ones,
which agree with the integer ones because every `S k i` is nonnegative. -/
theorem exists_supported_rounding (a : Fin N → Fin n → ℝ) (ha : ∀ j i, 0 ≤ a j i)
    (hrow : ∀ j, ∑ i, a j i = 1) :
    ∃ y : Fin N → Fin n, (∀ j, 0 < a j (y j)) ∧
      ∀ k ≤ N, ∀ i : Fin n,
        ⌊∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < k, a j i⌋₊
            ≤ (Finset.univ.filter fun j : Fin N => (j : ℕ) < k ∧ y j = i).card ∧
          (Finset.univ.filter fun j : Fin N => (j : ℕ) < k ∧ y j = i).card
            ≤ ⌈∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < k, a j i⌉₊ := by
  classical
  set Sp : ℕ → Fin n → ℝ :=
    fun u i => ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < u, a j i with hSpdef
  have hSpval : ∀ u i, Sp u i
      = ∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < u, a j i := fun _ _ => rfl
  have hSp0 : ∀ i, Sp 0 i = 0 := by
    intro i
    rw [hSpval]
    refine Finset.sum_eq_zero fun j hj => ?_
    simp only [Finset.mem_filter_univ] at hj
    exact absurd hj (Nat.not_lt_zero _)
  have hSpmono : ∀ i, Monotone fun u => Sp u i := by
    intro i u v huv
    simp only [hSpval]
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun j hj => ?_) fun j _ _ => ha j i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hj ⊢
    omega
  have hSpstep : ∀ (u : ℕ) (hu : u < N) (i : Fin n),
      Sp (u + 1) i - Sp u i = a ⟨u, hu⟩ i := by
    intro u hu i
    have hins : (Finset.univ.filter fun j : Fin N => (j : ℕ) < u + 1)
        = insert (⟨u, hu⟩ : Fin N) (Finset.univ.filter fun j : Fin N => (j : ℕ) < u) := by
      ext j
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert, Fin.ext_iff]
      omega
    have hnot : (⟨u, hu⟩ : Fin N) ∉ Finset.univ.filter fun j : Fin N => (j : ℕ) < u := by
      simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      omega
    rw [hSpval, hSpval, hins, Finset.sum_insert hnot]
    ring
  have hmsum : ∑ i, Sp N i = (N : ℝ) := by
    have hfull : (Finset.univ.filter fun j : Fin N => (j : ℕ) < N) = Finset.univ :=
      Finset.filter_true_of_mem fun j _ => j.2
    simp only [hSpval, hfull]
    rw [Finset.sum_comm]
    simp [hrow]
  set Rc : Fin n → ℕ := fun i => ⌈Sp N i⌉₊ with hRcdef
  set qq : Fin n → ℝ := fun i => (Rc i : ℝ) - Sp N i with hqqdef
  have hqq_nonneg : ∀ i, 0 ≤ qq i := fun i => sub_nonneg.mpr (Nat.le_ceil _)
  have hRcge : N ≤ ∑ i, Rc i := by
    have hle : (N : ℝ) ≤ ((∑ i, Rc i : ℕ) : ℝ) := by
      rw [← hmsum]
      push_cast
      exact Finset.sum_le_sum fun i _ => Nat.le_ceil _
    exact_mod_cast hle
  set Q : ℕ := (∑ i, Rc i) - N with hQdef
  have hQreal : (Q : ℝ) = ∑ i, qq i := by
    simp only [hqqdef, Finset.sum_sub_distrib, hmsum, hQdef]
    rw [Nat.cast_sub hRcge]
    push_cast
    ring
  have hQmul : ∀ i, qq i * ((Q : ℝ) / (Q : ℝ)) = qq i := by
    intro i
    rcases Nat.eq_zero_or_pos Q with hQ0 | hQpos
    · have hzero : qq i = 0 := by
        have hsum0 : ∑ i', qq i' = 0 := by rw [← hQreal, hQ0]; simp
        have hle := Finset.single_le_sum (f := qq) (fun i' _ => hqq_nonneg i') (Finset.mem_univ i)
        linarith [hqq_nonneg i]
      rw [hzero]
      simp
    · have hne : (Q : ℝ) ≠ 0 := by positivity
      rw [div_self hne, mul_one]
  set M : ℕ := N + Q with hMdef
  set P : ℕ → Fin n → ℝ :=
    fun u i => Sp (min u N) i + ((u - min u N : ℕ) : ℝ) * (qq i / (Q : ℝ)) with hPdef
  have hPval : ∀ u i, P u i
      = Sp (min u N) i + ((u - min u N : ℕ) : ℝ) * (qq i / (Q : ℝ)) := fun _ _ => rfl
  have hPnode : ∀ u, u ≤ N → ∀ i, P u i = Sp u i := by
    intro u hu i
    rw [hPval u i, Nat.min_eq_left hu, Nat.sub_self]
    simp
  have hP0 : ∀ i, P 0 i = 0 := by
    intro i
    rw [hPnode 0 (Nat.zero_le N) i, hSp0 i]
  have hPmono : ∀ i, Monotone fun u => P u i := by
    intro i u v huv
    simp only [hPval]
    have h1 : Sp (min u N) i ≤ Sp (min v N) i := hSpmono i (by omega)
    have h2 : ((u - min u N : ℕ) : ℝ) ≤ ((v - min v N : ℕ) : ℝ) := by
      have hnat : (u - min u N : ℕ) ≤ (v - min v N : ℕ) := by omega
      exact_mod_cast hnat
    have h3 : 0 ≤ qq i / (Q : ℝ) := div_nonneg (hqq_nonneg i) (Nat.cast_nonneg Q)
    have h4 := mul_le_mul_of_nonneg_right h2 h3
    linarith
  have hPstep : ∀ u, u < M → ∑ i, (P (u + 1) i - P u i) = 1 := by
    intro u hu
    rcases lt_or_ge u N with hlt | hge
    · have e1 : ∀ i, P (u + 1) i - P u i = a ⟨u, hlt⟩ i := by
        intro i
        rw [hPnode (u + 1) (by omega) i, hPnode u (by omega) i, hSpstep u hlt i]
      rw [Finset.sum_congr rfl fun i _ => e1 i]
      exact hrow ⟨u, hlt⟩
    · have hQpos : 0 < Q := by omega
      have hQne : (Q : ℝ) ≠ 0 := by positivity
      have e1 : ∀ i, P (u + 1) i - P u i = qq i / (Q : ℝ) := by
        intro i
        rw [hPval (u + 1) i, hPval u i, Nat.min_eq_right hge,
          Nat.min_eq_right (by omega : N ≤ u + 1)]
        have hcast : ((u + 1 - N : ℕ) : ℝ) = ((u - N : ℕ) : ℝ) + 1 := by
          have hnat : (u + 1 - N : ℕ) = (u - N : ℕ) + 1 := by omega
          rw [hnat]
          push_cast
          ring
        rw [hcast]
        ring
      rw [Finset.sum_congr rfl fun i _ => e1 i, ← Finset.sum_div, ← hQreal]
      field_simp
  have hPlast : ∀ i, P M i = (Rc i : ℝ) := by
    intro i
    have hmin : min M N = N := by omega
    have hsub : (M - N : ℕ) = Q := by omega
    rw [hPval M i, hmin, hsub, ← mul_div_assoc, mul_comm ((Q : ℝ)) (qq i), mul_div_assoc,
      hQmul i]
    simp only [hqqdef]
    ring
  obtain ⟨y, hysupp, hycount⟩ := exists_prefix_rounding P Rc hP0 hPmono hPstep hPlast
  have hNM : N ≤ M := by omega
  refine ⟨fun c => y ⟨c, lt_of_lt_of_le c.2 hNM⟩, fun c => ?_, fun k hk i => ?_⟩
  · have hs := hysupp ⟨c, lt_of_lt_of_le c.2 hNM⟩
    rw [hPnode (c : ℕ) (le_of_lt c.2), hPnode ((c : ℕ) + 1) c.2] at hs
    have he := hSpstep (c : ℕ) c.2 (y ⟨(c : ℕ), lt_of_lt_of_le c.2 hNM⟩)
    have hc : (⟨(c : ℕ), c.2⟩ : Fin N) = c := Fin.ext rfl
    rw [hc] at he
    linarith
  · have hgoal := hycount k (le_trans hk hNM) i
    rw [hPnode k hk i, hSpval k i] at hgoal
    rw [card_filter_embed hNM y hk i]
    exact hgoal

/-! ## SC24, negative control: the prefix bounds are not implied by support feasibility

`exists_supported_rounding` produces a selection satisfying two conditions at once: the support
condition `0 < a j (y j)` and the prefix bounds. The result below separates them, showing that
the prefix bounds are genuine extra content of the lemma rather than a consequence of respecting
supports. -/

/-- **SC24, negative control.** There are data `a` satisfying both hypotheses of
`exists_supported_rounding` (`0 ≤ a j i` and `∑ i, a j i = 1`) together with a selection `y`
satisfying its support condition `∀ j, 0 < a j (y j)` whose prefix counts violate one of its
prefix bounds. The witness is `n = 2`, `N = 3`, every row equal to `(2/5, 3/5)`, and `y`
constantly mode `1`: all three cells select mode `1`, while
`⌈∑ j with j < 3, a j 1⌉₊ = ⌈9/5⌉₊ = 2`, so the ceiling bound fails at `k = 3`, `i = 1`.

Consequently the conclusion of `exists_supported_rounding` is strictly stronger than its support
condition, and no argument can obtain the prefix bounds from support feasibility alone.

This is a control on the *statement*. It does **not** refute any particular greedy rule: nothing
here says that a rule which also tracks the prefix counts must fail. -/
theorem exists_supported_not_prefix_bounded :
    ∃ (n N : ℕ) (a : Fin N → Fin n → ℝ) (y : Fin N → Fin n) (k : ℕ) (i : Fin n),
      (∀ j i', 0 ≤ a j i') ∧ (∀ j, ∑ i', a j i' = 1) ∧ (∀ j, 0 < a j (y j)) ∧ k ≤ N ∧
        ¬ ((Finset.univ.filter fun j : Fin N => (j : ℕ) < k ∧ y j = i).card
            ≤ ⌈∑ j ∈ Finset.univ.filter fun j : Fin N => (j : ℕ) < k, a j i⌉₊) := by
  classical
  refine ⟨2, 3, fun _ i' => if i' = 0 then 2 / 5 else 3 / 5, fun _ => 1, 3, 1,
    fun j i' => ?_, fun j => ?_, fun j => ?_, le_rfl, ?_⟩
  · dsimp only
    split <;> norm_num
  · rw [Fin.sum_univ_two]
    norm_num
  · norm_num
  · have hfil : (Finset.univ.filter fun j : Fin 3 => (j : ℕ) < 3) = Finset.univ :=
      Finset.filter_true_of_mem fun j _ => j.2
    have hcard : (Finset.univ.filter fun j : Fin 3 =>
        (j : ℕ) < 3 ∧ (fun _ : Fin 3 => (1 : Fin 2)) j = 1).card = 3 := by decide
    have hsum : (∑ _j ∈ Finset.univ.filter fun j : Fin 3 => (j : ℕ) < 3,
        (if (1 : Fin 2) = 0 then (2 : ℝ) / 5 else 3 / 5)) = 9 / 5 := by
      rw [hfil]
      norm_num
    have hceil : ⌈(9 : ℝ) / 5⌉₊ = 2 := by norm_num
    rw [hcard, hsum, hceil]
    norm_num

end GridSwitching
