import Formal.GridSwitching.Compactness
import Formal.GridSwitching.LinearPrograms

/-!
# SC14 and SC15: coverage of the arbitrary-grid one-switch minimax value

This module proves the *necessity* half of the linear-program characterization `eq:grid-LP` of
the one-switch grid minimax value `F = gridF x n 1 T` on an arbitrary grid `x` with `n ≥ 3`
modes: every value below `F` and above the floor `T / 3`, and `F` itself, is the objective of a
feasible point of one of the two families `AllInitialFeasible`, `TwoLargeFeasible` introduced
in `Formal.GridSwitching.LinearPrograms`. Sufficiency is SC12, proved there.

## SC14 at a fixed objective

`exists_feasible_of_lt_gridF`: for `T / 3 < E < F` there are cells `ja ≤ jb` and LP data
`u, v, m` feasible in one of the two families at the objective `E`.

The witness is read off a grid-constant maximizer `A` with `gridOPT x A T 1 = F`
(`exists_gridF_eq`), so that *every* one-switch grid schedule errs by more than `E`. Let `h₁`
carry the largest terminal mass `m_1` and `h₂` the largest mass among the remaining modes.
For `j = 1, 2` the cell `k_j` is the one whose right node is the first grid node at or above
`T - E - m_j` (`exists_cutoff_cells`); `k_1 ≤ k_2` because `m_2 ≤ m_1`, and `k_1` is a genuine
cell because `T - m_1 > E`: otherwise the constant schedule of `h₁` would err by at most `E`.
That last step needs the omitted terminal masses to be bounded by `T - m_1`, which
`D_oneSwitch_zero_le` supplies from the conservation identity; the manuscript compresses this
and the note records it, so it is proved here rather than assumed.

Both switch orders that survive the dominance reduction are then obstructed at their first
eligible grid node: the omitted masses are at most `E` (if `m_2 ≤ E` because every mass other
than `m_1` is; if `m_2 > E` because three modes carry at most `T < 3E` and two of them carry
more than `E` each) and the final deficit is at most `E` by the choice of the cutoff cell, so
the initial deficit exceeds `E`. Averaging the cumulative allocations of the `n - 2` remaining
modes preserves the four properties the source lists: the total sum, nonnegative increments,
the ordering relative to `m_2`, and the initial-deficit inequalities just obtained.

The two upper cutoff inequalities are obtained *strictly* (`exists_cutoff_cells` returns
`x ja.castSucc < T - E - m_1`), which is what makes the limit below legitimate; `LPCommon`
records them in the non-strict form the closed program needs.

## SC14 at the supremum, and SC15

`exists_feasible_gridF`: `F` itself is the objective of a feasible point. For `F > T / 3` this
is the limit step. Instead of extracting a convergent subsequence it is obtained from
closedness of the set of covered objectives: at a fixed pair of cells each family is cut out of
the box `[0, T]^10` by non-strict inequalities between continuous functions
(`isClosed_lpCommonSet`), hence compact, and there are only finitely many pairs of cells and
two families, so `feasibleObjSet` is a finite union of compact sets. It contains the interval
`(T/3, F)` by SC14, hence its closure point `F`.

`exists_twoLargeFeasible_third` is SC15, the boundary case `F = T / 3`: with `c` the first grid
index whose node is at least `T / 3`, the point `a = b = c`, `m_1 = m_2 = T/3`,
`m_3 = (T/3)/(n-2)`, `u_1 = v_1 = u_2 = v_2 = (t_c - T/3)/2`, `u_3 = v_3 = (T/3)/(n-2)` is
feasible in the two-large-modes family. Besides `T/3 ≤ t_c ≤ T` this needs `t_{c-1} ≤ T/3`,
which the manuscript drops; it is the minimality of `c`.

## Hypotheses added beyond the sources

`3 ≤ n` is stated wherever it is used, as in `Formal.GridSwitching.LinearPrograms`.
`IsGrid x T` replaces the source's implicit assumption on the grid data. The two statements
that produce cell indices, `exists_twoLargeFeasible_third` and `exists_feasible_gridF`, assume
`0 < T`: on the degenerate horizon `T = 0` a grid has `N = 0` cells, so `Fin N` is empty and no
pair of cells exists. The fixed-objective statement needs no such hypothesis: its proof derives
`0 < T - E - m_1`, which already forces a positive horizon and hence at least one cell.

Where the manuscript and the note `notes/cia-reopened-finite-grid.md` differ, the note is
followed: it is the note that records the strictness of the upper cutoff inequalities before
the limit, the `max_{i ≠ 1} m_i ≤ T - m_1` step behind `k_1 > 0`, and the condition
`t_{c-1} ≤ E` in the boundary witness.
-/

namespace GridSwitching

open Set

variable {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ}

/-! ## Preliminaries

### The first grid node at or above a level -/

/-- The least index of a grid node that is at least `c`. -/
private noncomputable def firstNode (x : Fin (N + 1) → ℝ) (c : ℝ) : ℕ :=
  sInf {k : ℕ | ∃ h : k < N + 1, c ≤ x ⟨k, h⟩}

/-- Some grid node is at least any level below the horizon, namely the last one. -/
private theorem firstNode_nonempty (hx : IsGrid x T) {c : ℝ} (hc : c ≤ T) :
    {k : ℕ | ∃ h : k < N + 1, c ≤ x ⟨k, h⟩}.Nonempty := by
  refine ⟨N, Nat.lt_succ_self N, ?_⟩
  have : (⟨N, Nat.lt_succ_self N⟩ : Fin (N + 1)) = Fin.last N := rfl
  rw [this, hx.last]
  exact hc

/-- The node selected by `firstNode` is at least the level. -/
private theorem firstNode_spec (hx : IsGrid x T) {c : ℝ} (hc : c ≤ T) :
    ∃ h : firstNode x c < N + 1, c ≤ x ⟨firstNode x c, h⟩ :=
  Nat.sInf_mem (firstNode_nonempty hx hc)

/-- `firstNode` is at most any index whose node is at least the level. -/
private theorem firstNode_le {c : ℝ} {k : ℕ} (h : k < N + 1) (hk : c ≤ x ⟨k, h⟩) :
    firstNode x c ≤ k :=
  Nat.sInf_le ⟨h, hk⟩

/-- Every node strictly before `firstNode` is strictly below the level. -/
private theorem lt_of_lt_firstNode {c : ℝ} {j : ℕ} (hj : j < firstNode x c) (h : j < N + 1) :
    x ⟨j, h⟩ < c := by
  have hnot : j ∉ {k : ℕ | ∃ h : k < N + 1, c ≤ x ⟨k, h⟩} := Nat.notMem_of_lt_sInf hj
  simp only [Set.mem_ofPred_eq, not_exists, not_le] at hnot
  exact hnot h

/-! ### One-switch schedules, masses and cutoff cells -/

/-- A one-switch schedule whose switch time is a grid node is a two-block grid schedule. -/
private theorem isGridSchedule_oneSwitch_node (hx : IsGrid x T) (p q : Fin n)
    (c : Fin (N + 1)) : IsGridSchedule x 2 (oneSwitch p q (x c) T) := by
  refine ⟨![p, q], ![0, c, Fin.last N], ?_, rfl, rfl, ?_⟩
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    fin_cases j
    · simp
    · simpa using Fin.le_last c
  · have hxg : (x ∘ ![(0 : Fin (N + 1)), c, Fin.last N]) = ![0, x c, T] := by
      funext j
      fin_cases j
      · simpa using hx.first
      · rfl
      · simpa using hx.last
    rw [oneSwitch, hxg]

/-- Three distinct modes carry together at most the whole horizon. -/
private theorem triple_mass_le {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    {i j k : Fin n} (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    masses A T i + masses A T j + masses A T k ≤ T := by
  classical
  have hsub : ({i, j, k} : Finset (Fin n)) ⊆ Finset.univ := Finset.subset_univ _
  have hsum : ∑ l ∈ ({i, j, k} : Finset (Fin n)), A l T ≤ ∑ l, A l T :=
    Finset.sum_le_sum_of_subset_of_nonneg hsub fun l _ _ => hA.nonneg l ⟨hT, le_rfl⟩
  rw [hA.conservation T ⟨hT, le_rfl⟩] at hsum
  rwa [Finset.sum_insert (by simp [hij, hik]), Finset.sum_pair hjk, ← add_assoc] at hsum

/-- The cell whose right node is the first grid node at or above a positive level, together
with the corresponding cell for a second, larger level. Both cells exist because the level is
positive and at most the horizon, and the first cell is not to the right of the second.

The upper inequalities are strict: this is the form in which the cutoff constraints are first
obtained, before the limit of SC14 is taken. -/
private theorem exists_cutoff_cells (hx : IsGrid x T) {c₁ c₂ : ℝ} (hc₀ : 0 < c₁)
    (hc₁₂ : c₁ ≤ c₂) (hc₂ : c₂ ≤ T) :
    ∃ ja jb : Fin N, (ja : ℕ) ≤ (jb : ℕ) ∧
      c₁ ≤ x ja.succ ∧ x ja.castSucc < c₁ ∧ c₂ ≤ x jb.succ ∧ x jb.castSucc < c₂ := by
  obtain ⟨h₂lt, h₂le⟩ := firstNode_spec hx hc₂
  obtain ⟨h₁lt, h₁le⟩ := firstNode_spec hx (hc₁₂.trans hc₂)
  have hmono : firstNode x c₁ ≤ firstNode x c₂ :=
    firstNode_le h₂lt (hc₁₂.trans h₂le)
  have hpos : 0 < firstNode x c₁ := by
    rcases Nat.eq_zero_or_pos (firstNode x c₁) with h0 | h
    · exfalso
      have hzero : (⟨firstNode x c₁, h₁lt⟩ : Fin (N + 1)) = 0 := Fin.ext (by simpa using h0)
      rw [hzero, hx.first] at h₁le
      linarith
    · exact h
  have hja : firstNode x c₁ - 1 < N := by omega
  have hjb : firstNode x c₂ - 1 < N := by omega
  refine ⟨⟨firstNode x c₁ - 1, hja⟩, ⟨firstNode x c₂ - 1, hjb⟩,
    by simpa using Nat.sub_le_sub_right hmono 1, ?_, ?_, ?_, ?_⟩
  · have : (⟨firstNode x c₁ - 1, hja⟩ : Fin N).succ = ⟨firstNode x c₁, h₁lt⟩ :=
      Fin.ext (by simp; omega)
    rw [this]; exact h₁le
  · have hcast : (⟨firstNode x c₁ - 1, hja⟩ : Fin N).castSucc
        = ⟨firstNode x c₁ - 1, by omega⟩ := Fin.ext (by simp)
    rw [hcast]
    exact lt_of_lt_firstNode (by omega) _
  · have : (⟨firstNode x c₂ - 1, hjb⟩ : Fin N).succ = ⟨firstNode x c₂, h₂lt⟩ :=
      Fin.ext (by simp; omega)
    rw [this]; exact h₂le
  · have hcast : (⟨firstNode x c₂ - 1, hjb⟩ : Fin N).castSucc
        = ⟨firstNode x c₂ - 1, by omega⟩ := Fin.ext (by simp)
    rw [hcast]
    exact lt_of_lt_firstNode (by omega) _

/-- The cell whose right node is the first grid node at or above a positive level. -/
private theorem exists_cutoff_cell (hx : IsGrid x T) {c : ℝ} (hc₀ : 0 < c) (hc : c ≤ T) :
    ∃ j : Fin N, c ≤ x j.succ ∧ x j.castSucc < c := by
  obtain ⟨ja, -, -, h1, h2, -, -⟩ := exists_cutoff_cells hx hc₀ (le_refl c) hc
  exact ⟨ja, h1, h2⟩

/-- If the largest terminal mass leaves at most `E` unallocated, then the constant schedule of
that mode has error at most `E`.

This is the step the manuscript compresses: the omitted terminal masses are bounded not by the
largest mass but by `T - m_1`, because any other mode and the largest mode together allocate at
most the horizon. -/
private theorem D_oneSwitch_zero_le {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    {E : ℝ} {f r : Fin n} (hE0 : 0 ≤ E) (hle : T - masses A T f ≤ E) (hr : r ≠ f) :
    D A (oneSwitch r f 0 T) T ≤ E := by
  rw [D_oneSwitch hA hr le_rfl hT]
  refine max_le (omittedMass_le hE0 fun i _ hif => ?_) (max_le ?_ ?_)
  · have hpair := hA.pair_le hif ⟨hT, le_rfl⟩
    simp only [masses] at hle ⊢
    linarith
  · simp only [initialDeficit, hA.initial r]
    linarith
  · simp only [finalDeficit]
    linarith

/-! ## SC14: coverage at a fixed objective -/

/-- SC14, the fixed-`E` half. Let `F = gridF x n 1 T` be the one-switch grid minimax value of a
grid `x` with `n ≥ 3` modes. Every value `E` strictly between the floor `T / 3` and `F` is the
objective of a feasible point of one of the two linear-program families of `eq:grid-LP`.

The witness is read off a grid-constant maximizer `A`: the two distinguished states are the
cumulative allocations of the two modes of largest terminal mass, and the bulk state is the
average of the remaining `n - 2` modes. The two cell indices are the cells whose right nodes
are the first grid nodes at or above `T - E - m_1` and `T - E - m_2`. -/
theorem exists_feasible_of_lt_gridF (hn : 3 ≤ n) (hx : IsGrid x T) {E : ℝ}
    (hE₀ : T / 3 < E) (hE : E < gridF x n 1 T) :
    ∃ (ja jb : Fin N) (u v m : Fin 3 → ℝ), (ja : ℕ) ≤ (jb : ℕ) ∧
      (AllInitialFeasible n x T ja jb u v m E ∨ TwoLargeFeasible n x T ja jb u v m E) := by
  classical
  have h0n : 0 < n := by omega
  have hT : (0 : ℝ) ≤ T := hx.horizon_nonneg
  have hE0 : (0 : ℝ) ≤ E := by linarith
  have hnR : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hw2 : (0 : ℝ) < (n : ℝ) - 2 := by linarith
  -- a grid-constant maximizer
  obtain ⟨A, hAgc, hFA⟩ := exists_gridF_eq h0n hx 1
  have hA : IsCumulative A T := by
    obtain ⟨r, hr, rfl⟩ := hAgc
    exact gridCumulative_isCumulative hx.orderedTimes hr
  have hcomp : ∀ (p q : Fin n) (c : Fin (N + 1)), E < D A (oneSwitch p q (x c) T) T := by
    intro p q c
    refine lt_of_lt_of_le ?_
      (gridOPT_le_D h0n hx hA hT (isGridSchedule_oneSwitch_node hx p q c))
    rw [← hFA]
    exact hE
  -- the two largest terminal masses
  obtain ⟨h₁, -, hh₁⟩ := Finset.exists_max_image (Finset.univ : Finset (Fin n)) (masses A T)
    ⟨⟨0, h0n⟩, Finset.mem_univ _⟩
  have hnonempty : (Finset.univ.erase h₁).Nonempty := by
    rw [← Finset.card_pos, Finset.card_erase_of_mem (Finset.mem_univ h₁), Finset.card_univ,
      Fintype.card_fin]
    omega
  obtain ⟨h₂, hh₂mem, hh₂⟩ :=
    Finset.exists_max_image (Finset.univ.erase h₁) (masses A T) hnonempty
  have h21 : h₂ ≠ h₁ := (Finset.mem_erase.mp hh₂mem).1
  have hother : ∀ i : Fin n, i ≠ h₁ → masses A T i ≤ masses A T h₂ :=
    fun i hi => hh₂ i (Finset.mem_erase.mpr ⟨hi, Finset.mem_univ i⟩)
  have h21mass : masses A T h₂ ≤ masses A T h₁ := hh₁ h₂ (Finset.mem_univ _)
  have hm2nonneg : (0 : ℝ) ≤ masses A T h₂ := hA.nonneg h₂ ⟨hT, le_rfl⟩
  -- the first cutoff index is positive
  have hpos : 0 < T - E - masses A T h₁ := by
    by_contra hcon
    push Not at hcon
    obtain ⟨r, hr⟩ := Fintype.exists_ne_of_one_lt_card (by rw [Fintype.card_fin]; omega) h₁
    have hlt := hcomp r h₁ 0
    rw [hx.first] at hlt
    exact absurd (D_oneSwitch_zero_le hA hT hE0 (by linarith) hr) (not_le.mpr hlt)
  obtain ⟨ja, jb, hjab, hAl, hAu, hBl, hBu⟩ :=
    exists_cutoff_cells (c₂ := T - E - masses A T h₂) hx hpos (by linarith) (by linarith)
  have htaIcc : x ja.succ ∈ Icc (0 : ℝ) T := hx.mem_Icc ja.succ
  have htbIcc : x jb.succ ∈ Icc (0 : ℝ) T := hx.mem_Icc jb.succ
  have htab : x ja.succ ≤ x jb.succ := by
    refine hx.strictMono.monotone ?_
    rw [Fin.le_def]
    simpa using hjab
  -- the obstruction estimate at a grid node
  have hdeficit : ∀ (p f : Fin n) (c : Fin (N + 1)), p ≠ f → omittedMass A T p f ≤ E →
      T - masses A T f - x c ≤ E → A p (x c) + E ≤ x c := by
    intro p f c hpf hom hfin
    have h := hcomp p f c
    rw [D_oneSwitch hA hpf (hx.mem_Icc c).1 (hx.mem_Icc c).2] at h
    by_contra hcon
    push Not at hcon
    have hmax : max (omittedMass A T p f)
        (max (initialDeficit A p (x c)) (finalDeficit A T f (x c))) ≤ E := by
      refine max_le hom (max_le ?_ ?_)
      · simp only [initialDeficit]
        linarith
      · simp only [finalDeficit]
        linarith
    linarith
  -- the omitted masses of the two surviving orders are at most `E`
  have hthird : ∀ i : Fin n, i ≠ h₁ → i ≠ h₂ → masses A T i ≤ E := by
    intro i hi1 hi2
    by_cases hcase : masses A T h₂ ≤ E
    · exact (hother i hi1).trans hcase
    · push Not at hcase
      have h3 := triple_mass_le hA hT hi1 hi2 (Ne.symm h21)
      linarith
  have hdefA2 : A h₂ (x ja.succ) + E ≤ x ja.succ :=
    hdeficit h₂ h₁ ja.succ h21 (omittedMass_le hE0 fun i hi2 hi1 => hthird i hi1 hi2)
      (by linarith)
  have hdefB1 : A h₁ (x jb.succ) + E ≤ x jb.succ :=
    hdeficit h₁ h₂ jb.succ (Ne.symm h21) (omittedMass_le hE0 fun i hi1 hi2 => hthird i hi1 hi2)
      (by linarith)
  -- the bulk modes and the averaged state vector
  obtain ⟨S, hSdef⟩ : ∃ S : Finset (Fin n), S = (Finset.univ.erase h₁).erase h₂ := ⟨_, rfl⟩
  have hSmem : ∀ i ∈ S, i ≠ h₁ ∧ i ≠ h₂ := by
    intro i hi
    rw [hSdef, Finset.mem_erase, Finset.mem_erase] at hi
    exact ⟨hi.2.1, hi.1⟩
  have hScard : (S.card : ℝ) = (n : ℝ) - 2 := by
    have hcardN : S.card = n - 2 := by
      rw [hSdef, Finset.card_erase_of_mem (Finset.mem_erase.mpr ⟨h21, Finset.mem_univ _⟩),
        Finset.card_erase_of_mem (Finset.mem_univ h₁), Finset.card_univ, Fintype.card_fin]
      omega
    rw [hcardN, Nat.cast_sub (by omega : 2 ≤ n)]
    norm_num
  have hSsum : ∀ t : ℝ, A h₁ t + A h₂ t + ∑ i ∈ S, A i t = ∑ i, A i t := by
    intro t
    have e1 : ∑ i ∈ S, A i t + A h₂ t = ∑ i ∈ Finset.univ.erase h₁, A i t := by
      rw [hSdef]
      exact Finset.sum_erase_add _ _ (Finset.mem_erase.mpr ⟨h21, Finset.mem_univ _⟩)
    have e2 : ∑ i ∈ Finset.univ.erase h₁, A i t + A h₁ t = ∑ i, A i t :=
      Finset.sum_erase_add _ _ (Finset.mem_univ h₁)
    linarith
  obtain ⟨st, hst0, hst1, hst2⟩ : ∃ st : ℝ → Fin 3 → ℝ, (∀ t, st t 0 = A h₁ t) ∧
      (∀ t, st t 1 = A h₂ t) ∧ (∀ t, st t 2 = (∑ i ∈ S, A i t) / ((n : ℝ) - 2)) :=
    ⟨fun t => ![A h₁ t, A h₂ t, (∑ i ∈ S, A i t) / ((n : ℝ) - 2)], fun _ => rfl, fun _ => rfl,
      fun _ => rfl⟩
  have hst0T : st T 0 = masses A T h₁ := hst0 T
  have hst1T : st T 1 = masses A T h₂ := hst1 T
  have hstW : ∀ t ∈ Icc (0 : ℝ) T, lpWeighted n (st t) = t := by
    intro t ht
    have hcancel : ((n : ℝ) - 2) * ((∑ i ∈ S, A i t) / ((n : ℝ) - 2)) = ∑ i ∈ S, A i t := by
      field_simp
    rw [lpWeighted_eq, hst0, hst1, hst2, hcancel, hSsum t, hA.conservation t ht]
  have hstnn : ∀ t ∈ Icc (0 : ℝ) T, ∀ j, 0 ≤ st t j := by
    intro t ht j
    have e0 : (0 : ℝ) ≤ st t 0 := by rw [hst0]; exact hA.nonneg h₁ ht
    have e1 : (0 : ℝ) ≤ st t 1 := by rw [hst1]; exact hA.nonneg h₂ ht
    have e2 : (0 : ℝ) ≤ st t 2 := by
      rw [hst2]
      exact div_nonneg (Finset.sum_nonneg fun i _ => hA.nonneg i ht) hw2.le
    fin_cases j <;> assumption
  have hstmono : ∀ s t : ℝ, 0 ≤ s → s ≤ t → t ≤ T → ∀ j, st s j ≤ st t j := by
    intro s t hs hst htT j
    have e0 : st s 0 ≤ st t 0 := by rw [hst0, hst0]; exact hA.mono h₁ s t hs hst htT
    have e1 : st s 1 ≤ st t 1 := by rw [hst1, hst1]; exact hA.mono h₂ s t hs hst htT
    have e2 : st s 2 ≤ st t 2 := by
      rw [hst2, hst2]
      exact div_le_div_of_nonneg_right
        (Finset.sum_le_sum fun i _ => hA.mono i s t hs hst htT) hw2.le
    fin_cases j <;> assumption
  have hm21 : st T 2 ≤ st T 1 := by
    have hsum : ∑ i ∈ S, A i T ≤ ((n : ℝ) - 2) * A h₂ T := by
      have h := Finset.sum_le_sum (f := fun i => A i T) (g := fun _ => A h₂ T)
        (fun i hi => hother i (hSmem i hi).1)
      rw [Finset.sum_const, nsmul_eq_mul, hScard] at h
      exact h
    rw [hst1, hst2, div_le_iff₀ hw2]
    linarith
  -- the common constraint block
  have hcommon : LPCommon n x T ja jb (st (x ja.succ)) (st (x jb.succ)) (st T) E :=
    { u_nonneg := hstnn _ htaIcc
      u_le_v := hstmono _ _ htaIcc.1 htab htbIcc.2
      v_le_m := hstmono _ _ htbIcc.1 htbIcc.2 le_rfl
      m_one_le_m_zero := by rw [hst0T, hst1T]; exact h21mass
      m_two_le_m_one := hm21
      horizon_third_le := hE₀.le
      weighted_u := hstW _ htaIcc
      weighted_v := hstW _ htbIcc
      weighted_m := hstW T ⟨hT, le_rfl⟩
      cutoff_a_lower := by rw [hst0T]; linarith
      cutoff_a_upper := by rw [hst0T]; linarith
      cutoff_b_lower := by rw [hst1T]; linarith
      cutoff_b_upper := by rw [hst1T]; linarith
      deficit_a := by rw [hst1]; exact hdefA2
      deficit_b := by rw [hst0]; exact hdefB1 }
  refine ⟨ja, jb, st (x ja.succ), st (x jb.succ), st T, hjab, ?_⟩
  by_cases hcase : masses A T h₂ ≤ E
  · -- at most one terminal mass exceeds `E`: every initial mode is obstructed
    refine Or.inl ⟨hcommon, ?_⟩
    have hbulk : ∀ i ∈ S, A i (x ja.succ) + E ≤ x ja.succ := by
      intro i hi
      refine hdeficit i h₁ ja.succ (hSmem i hi).1
        (omittedMass_le hE0 fun k _ hk1 => ?_) (by linarith)
      exact (hother k hk1).trans hcase
    have hsum : ∑ i ∈ S, A i (x ja.succ) ≤ ((n : ℝ) - 2) * (x ja.succ - E) := by
      have h := Finset.sum_le_sum (f := fun i => A i (x ja.succ))
        (g := fun _ => x ja.succ - E) (fun i hi => by linarith [hbulk i hi])
      rw [Finset.sum_const, nsmul_eq_mul, hScard] at h
      exact h
    rw [hst2, div_add' _ _ _ (ne_of_gt hw2), div_le_iff₀ hw2]
    linarith
  · -- two terminal masses exceed `E`
    push Not at hcase
    exact Or.inr ⟨hcommon, by rw [hst1T]; linarith⟩

/-! ## SC15: the boundary case `F = T / 3` -/

/-- SC15: the explicit two-large-modes point at the objective `T / 3`. With `c` the first grid
index whose node is at least `T / 3`, the cell `c` carries the feasible point
`m_1 = m_2 = T / 3`, `m_3 = (T/3)/(n-2)`, `u_1 = v_1 = u_2 = v_2 = (t_c - T/3)/2` and
`u_3 = v_3 = (T/3)/(n-2)`.

Besides `T/3 ≤ t_c ≤ T` the verification needs `t_{c-1} ≤ T/3`, which the manuscript drops; it
is the minimality of `c` and is supplied by `exists_cutoff_cell`. A positive horizon is
required: on `T = 0` the grid has no cells at all. -/
theorem exists_twoLargeFeasible_third (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    ∃ (jc : Fin N) (u v m : Fin 3 → ℝ), TwoLargeFeasible n x T jc jc u v m (T / 3) := by
  have hnR : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have hnw : (0 : ℝ) < (n : ℝ) - 2 := by linarith
  have hne : ((n : ℝ) - 2) ≠ 0 := ne_of_gt hnw
  obtain ⟨jc, hlow, hupp⟩ := exists_cutoff_cell hx (by linarith : (0 : ℝ) < T / 3) (by linarith)
  have hXT : x jc.succ ≤ T := (hx.mem_Icc jc.succ).2
  obtain ⟨w, hw0, hw1, hw2⟩ : ∃ w : Fin 3 → ℝ, w 0 = (x jc.succ - T / 3) / 2 ∧
      w 1 = (x jc.succ - T / 3) / 2 ∧ w 2 = T / 3 / ((n : ℝ) - 2) :=
    ⟨![(x jc.succ - T / 3) / 2, (x jc.succ - T / 3) / 2, T / 3 / ((n : ℝ) - 2)], rfl, rfl, rfl⟩
  obtain ⟨mm, hm0, hm1, hm2⟩ : ∃ mm : Fin 3 → ℝ, mm 0 = T / 3 ∧ mm 1 = T / 3 ∧
      mm 2 = T / 3 / ((n : ℝ) - 2) :=
    ⟨![T / 3, T / 3, T / 3 / ((n : ℝ) - 2)], rfl, rfl, rfl⟩
  have hwm : ∀ j, w j ≤ mm j := by
    have e0 : w 0 ≤ mm 0 := by rw [hw0, hm0]; linarith
    have e1 : w 1 ≤ mm 1 := by rw [hw1, hm1]; linarith
    have e2 : w 2 ≤ mm 2 := by rw [hw2, hm2]
    intro j
    fin_cases j <;> assumption
  have hwnn : ∀ j, 0 ≤ w j := by
    have e0 : (0 : ℝ) ≤ w 0 := by rw [hw0]; linarith
    have e1 : (0 : ℝ) ≤ w 1 := by rw [hw1]; linarith
    have e2 : (0 : ℝ) ≤ w 2 := by
      rw [hw2]
      exact div_nonneg (by linarith) hnw.le
    intro j
    fin_cases j <;> assumption
  refine ⟨jc, w, w, mm, ⟨⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩, ?_⟩⟩
  · exact hwnn
  · exact fun _ => le_rfl
  · exact hwm
  · rw [hm0, hm1]
  · rw [hm1, hm2]
    exact div_le_self (by linarith) (by linarith)
  · exact le_rfl
  · rw [lpWeighted_eq, hw0, hw1, hw2]
    field_simp
    ring
  · rw [lpWeighted_eq, hw0, hw1, hw2]
    field_simp
    ring
  · rw [lpWeighted_eq, hm0, hm1, hm2]
    field_simp
    ring
  · rw [hm0]; linarith
  · rw [hm0]; linarith
  · rw [hm1]; linarith
  · rw [hm1]; linarith
  · rw [hw1]; linarith
  · rw [hw0]; linarith
  · rw [hm1]

/-! ## SC14: the limit

The feasible set of either family at a fixed pair of cells is a compact subset of a
ten-dimensional space: it is cut out of a box by non-strict inequalities between continuous
functions. Since there are only finitely many pairs of cells and two families, the set of
attainable objective values is a finite union of compact sets, hence closed, and it therefore
contains the supremum `F` of the values it covers. -/

/-- The data `(u, v, m, E)` of a point of `eq:grid-LP`. -/
private abbrev LPPoint : Type := (Fin 3 → ℝ) × (Fin 3 → ℝ) × (Fin 3 → ℝ) × ℝ

/-- The common constraint block of `eq:grid-LP` as a subset of `LPPoint`. -/
private def lpCommonSet (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    Set LPPoint :=
  {p | LPCommon n x T ja jb p.1 p.2.1 p.2.2.1 p.2.2.2}

/-- The all-initial-modes family as a subset of `LPPoint`. -/
private def allInitialSet (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    Set LPPoint :=
  {p | AllInitialFeasible n x T ja jb p.1 p.2.1 p.2.2.1 p.2.2.2}

/-- The two-large-modes family as a subset of `LPPoint`. -/
private def twoLargeSet (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    Set LPPoint :=
  {p | TwoLargeFeasible n x T ja jb p.1 p.2.1 p.2.2.1 p.2.2.2}

/-- The weighted sum is continuous in the state vector. -/
private theorem continuous_lpWeighted (n : ℕ) : Continuous (lpWeighted n) := by
  unfold lpWeighted
  exact continuous_finsetSum _ fun j _ => continuous_const.mul (continuous_apply j)

/-- The common constraint block is closed: every constraint is a non-strict inequality between
continuous functions. -/
private theorem isClosed_lpCommonSet (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    IsClosed (lpCommonSet n x T ja jb) := by
  refine isClosed_of_closure_subset fun p hp => ?_
  have key : ∀ f g : LPPoint → ℝ, Continuous f → Continuous g →
      (∀ q ∈ lpCommonSet n x T ja jb, f q ≤ g q) → f p ≤ g p :=
    fun f g hf hg h => (isClosed_le hf hg).closure_subset_iff.mpr h hp
  have c1 : ∀ j : Fin 3, Continuous fun q : LPPoint => q.1 j := fun _ => by fun_prop
  have c2 : ∀ j : Fin 3, Continuous fun q : LPPoint => q.2.1 j := fun _ => by fun_prop
  have c3 : ∀ j : Fin 3, Continuous fun q : LPPoint => q.2.2.1 j := fun _ => by fun_prop
  have cE : Continuous fun q : LPPoint => q.2.2.2 := by fun_prop
  have cW1 : Continuous fun q : LPPoint => lpWeighted n q.1 :=
    (continuous_lpWeighted n).comp continuous_fst
  have cW2 : Continuous fun q : LPPoint => lpWeighted n q.2.1 :=
    (continuous_lpWeighted n).comp (continuous_fst.comp continuous_snd)
  have cW3 : Continuous fun q : LPPoint => lpWeighted n q.2.2.1 :=
    (continuous_lpWeighted n).comp (continuous_fst.comp (continuous_snd.comp continuous_snd))
  exact
    { u_nonneg := fun j =>
        key _ _ continuous_const (c1 j) fun q hq => hq.u_nonneg j
      u_le_v := fun j => key _ _ (c1 j) (c2 j) fun q hq => hq.u_le_v j
      v_le_m := fun j => key _ _ (c2 j) (c3 j) fun q hq => hq.v_le_m j
      m_one_le_m_zero := key _ _ (c3 1) (c3 0) fun q hq => hq.m_one_le_m_zero
      m_two_le_m_one := key _ _ (c3 2) (c3 1) fun q hq => hq.m_two_le_m_one
      horizon_third_le := key _ _ continuous_const cE fun q hq => hq.horizon_third_le
      weighted_u := le_antisymm
        (key _ _ cW1 continuous_const fun q hq => hq.weighted_u.le)
        (key _ _ continuous_const cW1 fun q hq => hq.weighted_u.ge)
      weighted_v := le_antisymm
        (key _ _ cW2 continuous_const fun q hq => hq.weighted_v.le)
        (key _ _ continuous_const cW2 fun q hq => hq.weighted_v.ge)
      weighted_m := le_antisymm
        (key _ _ cW3 continuous_const fun q hq => hq.weighted_m.le)
        (key _ _ continuous_const cW3 fun q hq => hq.weighted_m.ge)
      cutoff_a_lower := key _ _ continuous_const (cE.add (c3 0)) fun q hq => hq.cutoff_a_lower
      cutoff_a_upper := key _ _ (cE.add (c3 0)) continuous_const fun q hq => hq.cutoff_a_upper
      cutoff_b_lower := key _ _ continuous_const (cE.add (c3 1)) fun q hq => hq.cutoff_b_lower
      cutoff_b_upper := key _ _ (cE.add (c3 1)) continuous_const fun q hq => hq.cutoff_b_upper
      deficit_a := key _ _ ((c1 1).add cE) continuous_const fun q hq => hq.deficit_a
      deficit_b := key _ _ ((c2 0).add cE) continuous_const fun q hq => hq.deficit_b }

/-- Every coordinate of a nonnegative state vector is bounded by its weighted sum. -/
private theorem lpState_le (hn : 3 ≤ n) {f : Fin 3 → ℝ} (hf : ∀ j, 0 ≤ f j) {c : ℝ}
    (hw : lpWeighted n f = c) (j : Fin 3) : f j ≤ c := by
  have hnR : (3 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  rw [lpWeighted_eq] at hw
  have hprod : 0 ≤ ((n : ℝ) - 2) * f 2 := mul_nonneg (by linarith) (hf 2)
  have hbig : f 2 ≤ ((n : ℝ) - 2) * f 2 := by nlinarith [hf 2]
  have e0 : f 0 ≤ c := by linarith [hf 1]
  have e1 : f 1 ≤ c := by linarith [hf 0]
  have e2 : f 2 ≤ c := by linarith [hf 0, hf 1]
  fin_cases j <;> assumption

/-- Every point of the common constraint block has all its coordinates in `[0, T]`. -/
private theorem lpCommonSet_subset_Icc (hn : 3 ≤ n) (hx : IsGrid x T) (ja jb : Fin N) :
    lpCommonSet n x T ja jb ⊆
      Icc (0 : LPPoint)
        ((fun _ => T : Fin 3 → ℝ), (fun _ => T : Fin 3 → ℝ), (fun _ => T : Fin 3 → ℝ), T) := by
  intro p hp
  have hc : LPCommon n x T ja jb p.1 p.2.1 p.2.2.1 p.2.2.2 := hp
  have hT : (0 : ℝ) ≤ T := hx.horizon_nonneg
  have hE0 : (0 : ℝ) ≤ p.2.2.2 := le_trans (by linarith) hc.horizon_third_le
  have hja : x ja.succ ≤ T := (hx.mem_Icc ja.succ).2
  have hjb : x jb.succ ≤ T := (hx.mem_Icc jb.succ).2
  have hu : ∀ j, p.1 j ≤ T := fun j => (lpState_le hn hc.u_nonneg hc.weighted_u j).trans hja
  have hvnn : ∀ j, 0 ≤ p.2.1 j := fun j => (hc.u_nonneg j).trans (hc.u_le_v j)
  have hv : ∀ j, p.2.1 j ≤ T := fun j => (lpState_le hn hvnn hc.weighted_v j).trans hjb
  have hmnn : ∀ j, 0 ≤ p.2.2.1 j := fun j => (hvnn j).trans (hc.v_le_m j)
  have hm : ∀ j, p.2.2.1 j ≤ T := fun j => lpState_le hn hmnn hc.weighted_m j
  have hE : p.2.2.2 ≤ T := by
    have h1 := hc.deficit_a
    have h2 := hc.u_nonneg 1
    linarith
  exact ⟨⟨hc.u_nonneg, hvnn, hmnn, hE0⟩, ⟨hu, hv, hm, hE⟩⟩

/-- The common constraint block is compact. -/
private theorem isCompact_lpCommonSet (hn : 3 ≤ n) (hx : IsGrid x T) (ja jb : Fin N) :
    IsCompact (lpCommonSet n x T ja jb) :=
  IsCompact.of_isClosed_subset isCompact_Icc (isClosed_lpCommonSet n x T ja jb)
    (lpCommonSet_subset_Icc hn hx ja jb)

/-- The all-initial-modes family is the common block cut by one more closed constraint. -/
private theorem allInitialSet_eq (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    allInitialSet n x T ja jb =
      lpCommonSet n x T ja jb ∩ {p : LPPoint | p.1 2 + p.2.2.2 ≤ x ja.succ} := by
  ext p
  exact ⟨fun h => ⟨h.common, h.deficit_a_bulk⟩, fun h => ⟨h.1, h.2⟩⟩

/-- The two-large-modes family is the common block cut by one more closed constraint. -/
private theorem twoLargeSet_eq (n : ℕ) (x : Fin (N + 1) → ℝ) (T : ℝ) (ja jb : Fin N) :
    twoLargeSet n x T ja jb =
      lpCommonSet n x T ja jb ∩ {p : LPPoint | p.2.2.2 ≤ p.2.2.1 1} := by
  ext p
  exact ⟨fun h => ⟨h.common, h.E_le_m_one⟩, fun h => ⟨h.1, h.2⟩⟩

/-- The all-initial-modes family is compact. -/
private theorem isCompact_allInitialSet (hn : 3 ≤ n) (hx : IsGrid x T) (ja jb : Fin N) :
    IsCompact (allInitialSet n x T ja jb) := by
  rw [allInitialSet_eq]
  exact (isCompact_lpCommonSet hn hx ja jb).inter_right
    (isClosed_le (by fun_prop) continuous_const)

/-- The two-large-modes family is compact. -/
private theorem isCompact_twoLargeSet (hn : 3 ≤ n) (hx : IsGrid x T) (ja jb : Fin N) :
    IsCompact (twoLargeSet n x T ja jb) := by
  rw [twoLargeSet_eq]
  exact (isCompact_lpCommonSet hn hx ja jb).inter_right (isClosed_le (by fun_prop) (by fun_prop))

/-- The set of objective values covered by the two families. -/
private def feasibleObjSet (n : ℕ) {N : ℕ} (x : Fin (N + 1) → ℝ) (T : ℝ) : Set ℝ :=
  {E | ∃ (ja jb : Fin N) (u v m : Fin 3 → ℝ),
    AllInitialFeasible n x T ja jb u v m E ∨ TwoLargeFeasible n x T ja jb u v m E}

/-- There are finitely many pairs of cells and two families, so the set of covered objective
values is a finite union of compact sets and hence closed. -/
private theorem isClosed_feasibleObjSet (hn : 3 ≤ n) (hx : IsGrid x T) :
    IsClosed (feasibleObjSet n x T) := by
  have hEq : feasibleObjSet n x T =
      (⋃ c : Fin N × Fin N, (fun p : LPPoint => p.2.2.2) '' allInitialSet n x T c.1 c.2) ∪
        (⋃ c : Fin N × Fin N, (fun p : LPPoint => p.2.2.2) '' twoLargeSet n x T c.1 c.2) := by
    ext E
    constructor
    · rintro ⟨ja, jb, u, v, m, h | h⟩
      · exact Or.inl (Set.mem_iUnion.mpr ⟨(ja, jb), ⟨(u, v, m, E), h, rfl⟩⟩)
      · exact Or.inr (Set.mem_iUnion.mpr ⟨(ja, jb), ⟨(u, v, m, E), h, rfl⟩⟩)
    · rintro (h | h)
      · obtain ⟨c, q, hq, rfl⟩ := Set.mem_iUnion.mp h
        exact ⟨c.1, c.2, q.1, q.2.1, q.2.2.1, Or.inl hq⟩
      · obtain ⟨c, q, hq, rfl⟩ := Set.mem_iUnion.mp h
        exact ⟨c.1, c.2, q.1, q.2.1, q.2.2.1, Or.inr hq⟩
  rw [hEq]
  exact IsClosed.union
    (isClosed_iUnion_of_finite fun c =>
      ((isCompact_allInitialSet hn hx c.1 c.2).image (by fun_prop)).isClosed)
    (isClosed_iUnion_of_finite fun c =>
      ((isCompact_twoLargeSet hn hx c.1 c.2).image (by fun_prop)).isClosed)

/-- SC14 and SC15 together: the one-switch grid minimax value `F` is itself the objective of a
feasible point of one of the two families of `eq:grid-LP`.

For `F > T / 3` this is the limit half of SC14: the covered objective values form a closed set
containing the whole interval `(T/3, F)`. For `F = T / 3` it is the explicit boundary witness
of SC15. A positive horizon is required, since on `T = 0` the grid has no cells. -/
theorem exists_feasible_gridF (hn : 3 ≤ n) (hx : IsGrid x T) (hT : 0 < T) :
    ∃ (ja jb : Fin N) (u v m : Fin 3 → ℝ), (ja : ℕ) ≤ (jb : ℕ) ∧
      (AllInitialFeasible n x T ja jb u v m (gridF x n 1 T) ∨
        TwoLargeFeasible n x T ja jb u v m (gridF x n 1 T)) := by
  have hmem : gridF x n 1 T ∈ feasibleObjSet n x T := by
    rcases eq_or_lt_of_le (third_le_gridF hn hx) with heq | hlt
    · obtain ⟨jc, u, v, m, h⟩ := exists_twoLargeFeasible_third hn hx hT
      exact ⟨jc, jc, u, v, m, Or.inr (heq ▸ h)⟩
    · have hsub : Ioo (T / 3) (gridF x n 1 T) ⊆ feasibleObjSet n x T := by
        intro E hE
        obtain ⟨ja, jb, u, v, m, -, h⟩ := exists_feasible_of_lt_gridF hn hx hE.1 hE.2
        exact ⟨ja, jb, u, v, m, h⟩
      refine (isClosed_feasibleObjSet hn hx).closure_subset_iff.mpr hsub ?_
      rw [closure_Ioo (ne_of_lt hlt)]
      exact ⟨hlt.le, le_rfl⟩
  obtain ⟨ja, jb, u, v, m, h⟩ := hmem
  refine ⟨ja, jb, u, v, m, ?_, h⟩
  rcases h with h | h
  · exact LPCommon.index_le hn hx h.common
  · exact LPCommon.index_le hn hx h.common

end GridSwitching
