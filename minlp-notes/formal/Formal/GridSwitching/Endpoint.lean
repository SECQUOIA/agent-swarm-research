import Formal.GridSwitching.Model

/-!
# SC05 and SC06: endpoint monotonicity, cell averaging, and grid domination

This module proves the two tier-1 obligations of `topics/17-grid-switching/CLAIMS.md` that
turn the definitions of `Formal.GridSwitching.Model` into usable tools.

* SC05 (`lem:endpoint`). On an activation block the discrepancy of the *selected* mode is
  nonincreasing and every other discrepancy is nondecreasing
  (`antitoneOn_selected_discrepancy`, `monotoneOn_other_discrepancy`). The proof does not use
  the derivative argument of the source: on its own block the occupation of the selected mode
  grows exactly like elapsed time (`occupation_selected_increment`) and the occupation of
  every other mode is constant (`occupation_other_const`), so the monotonicity follows from
  `IsCumulative.mono` and `IsCumulative.lipschitz` alone.

  The consequence the rest of the package uses is that both errors are determined by the
  block endpoints. It is packaged as the sandwich `exists_switchTime_sandwich` and as the two
  characterizations `D_le_iff_switchTimes` and `Dminus_le_iff_switchTimes`, together with
  their grid specializations `gridSchedule_D_le_iff` and `gridSchedule_Dminus_le_iff`, which
  quantify over *grid nodes* and hold for an arbitrary relaxed input, in particular for one
  that varies inside cells.

* SC06 (the paragraph after `lem:endpoint` and `eq:minimax-grid-domination`). The cell
  average `cellAverageInput` of an input is grid constant, agrees with the input at every
  grid node (`cellAverageInput_node`), and therefore preserves the error of every grid
  schedule (`D_cellAverageInput`, `Dminus_cellAverageInput`) and the grid instance optima
  (`gridOPT_cellAverageInput`, `gridOPTminus_cellAverageInput`). Combined with the
  restriction inequalities `OPT_le_gridOPT` and `OPTminus_le_gridOPTminus`, this gives
  `eq:minimax-grid-domination`: `F_le_gridF` and `Gminus_le_gridGminus`.

**Limitation, recorded deliberately.** Cell averaging preserves the *grid* instance optimum
only. It does **not** preserve the continuous instance optimum `OPT`, because a schedule with
switch times off the grid can exploit the variation of the input inside a cell, and nothing
in this module claims otherwise. The only comparison proved between a continuous and a grid
optimum is the restriction inequality `OPT_le_gridOPT`, which holds for a *fixed* input and
in the direction `OPT ≤ gridOPT`; the reverse-direction transfer estimate is a separate
obligation (SC25) and is not proved here.

Hypotheses added beyond the sources: `0 < n` wherever a nonnegativity or nonemptiness
statement about the error suprema and infima is needed (with no modes the error sets are
empty and the Lean-total `sSup`/`sInf` conventions take over), and `0 < k` for the one-sided
block budget, which the sources leave implicit by assuming at least one activation block.
-/

namespace GridSwitching

open Set

/-! ## SC05: endpoint monotonicity -/

/-- Telescoping sum over the block index. This repeats a `private` lemma of
`Formal.GridSwitching.Model`, which is not exported. -/
private theorem sum_succ_sub_castSucc' {k : ℕ} (f : Fin (k + 1) → ℝ) :
    ∑ j : Fin k, (f j.succ - f j.castSucc) = f (Fin.last k) - f 0 := by
  induction k with
  | zero => simp
  | succ k ih =>
    have h := ih fun m : Fin (k + 1) => f m.castSucc
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.succ_castSucc] at h ⊢
    rw [h]
    simp only [Fin.succ_last, Fin.castSucc_zero]
    ring

/-- A block different from `j` contributes the same amount of occupied time at every instant
of block `j`: earlier blocks are already complete, later blocks have not started. -/
private theorem block_term_const {k : ℕ} {τ : Fin (k + 1) → ℝ} (hτ : Monotone τ)
    {j j' : Fin k} (hne : j' ≠ j) {s t : ℝ} (hs : τ j.castSucc ≤ s) (hst : s ≤ t)
    (ht : t ≤ τ j.succ) :
    min t (τ j'.succ) - min t (τ j'.castSucc) =
      min s (τ j'.succ) - min s (τ j'.castSucc) := by
  have hcs : τ j'.castSucc ≤ τ j'.succ := hτ (Fin.castSucc_le_succ j')
  rcases lt_trichotomy j' j with h | h | h
  · have hle : τ j'.succ ≤ τ j.castSucc := by
      refine hτ ?_
      simp only [Fin.le_def, Fin.val_succ, Fin.val_castSucc]
      omega
    have h1 : τ j'.succ ≤ s := hle.trans hs
    rw [min_eq_right (h1.trans hst), min_eq_right (hcs.trans (h1.trans hst)),
      min_eq_right h1, min_eq_right (hcs.trans h1)]
  · exact absurd h hne
  · have hge : τ j.succ ≤ τ j'.castSucc := by
      refine hτ ?_
      simp only [Fin.le_def, Fin.val_succ, Fin.val_castSucc]
      omega
    have h1 : t ≤ τ j'.castSucc := ht.trans hge
    rw [min_eq_left (h1.trans hcs), min_eq_left h1, min_eq_left (hst.trans (h1.trans hcs)),
      min_eq_left (hst.trans h1)]
    ring

/-- SC05, first ingredient: on its own block the occupation of the selected mode increases
exactly like elapsed time. -/
theorem occupation_selected_increment {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) (j : Fin k) {s t : ℝ} (hs : τ j.castSucc ≤ s) (hst : s ≤ t)
    (ht : t ≤ τ j.succ) :
    occupation p τ (p j) t - occupation p τ (p j) s = t - s := by
  simp only [occupation]
  rw [← Finset.sum_sub_distrib, Finset.sum_eq_single j]
  · have hif : ∀ a b : ℝ, (if p j = p j then a else b) = a := fun _ _ => if_pos rfl
    rw [hif, hif, min_eq_left ht, min_eq_right (hs.trans hst), min_eq_left (hst.trans ht),
      min_eq_right hs]
    ring
  · intro j' _ hne
    split_ifs with hp
    · rw [block_term_const hτ hne hs hst ht]
      ring
    · ring
  · intro hj
    exact absurd (Finset.mem_univ j) hj

/-- SC05, second ingredient: on a block the occupation of every mode other than the selected
one is constant. -/
theorem occupation_other_const {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    (hτ : Monotone τ) (j : Fin k) {i : Fin n} (hi : i ≠ p j) {s t : ℝ}
    (hs : τ j.castSucc ≤ s) (hst : s ≤ t) (ht : t ≤ τ j.succ) :
    occupation p τ i t = occupation p τ i s := by
  simp only [occupation]
  refine Finset.sum_congr rfl fun j' _ => ?_
  split_ifs with hp
  · have hne : j' ≠ j := by
      rintro rfl
      exact hi hp.symm
    exact block_term_const hτ hne hs hst ht
  · rfl

/-- Every switch time lies on the horizon. -/
theorem OrderedTimes.mem_Icc {k : ℕ} {τ : Fin (k + 1) → ℝ} {T : ℝ} (hτ : OrderedTimes τ T)
    (m : Fin (k + 1)) : τ m ∈ Icc (0 : ℝ) T :=
  ⟨hτ.nonneg m, by rw [← hτ.last]; exact hτ.mono (Fin.le_last m)⟩

/-- SC05, selected mode: on the `j`-th activation block the discrepancy of the selected mode
`p j` is nonincreasing. -/
theorem antitoneOn_selected_discrepancy {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (j : Fin k) :
    AntitoneOn (fun t => A (p j) t - occupation p τ (p j) t)
      (Icc (τ j.castSucc) (τ j.succ)) := by
  intro s hs t ht hst
  have h0 : (0 : ℝ) ≤ s := (hτ.nonneg j.castSucc).trans hs.1
  have hT : t ≤ T := ht.2.trans (hτ.mem_Icc j.succ).2
  have hlip := hA.lipschitz (p j) s t h0 hst hT
  have hocc := occupation_selected_increment p hτ.mono j hs.1 hst ht.2
  simp only
  linarith

/-- SC05, unselected modes: on the `j`-th activation block every discrepancy other than that
of the selected mode is nondecreasing. -/
theorem monotoneOn_other_discrepancy {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (j : Fin k)
    {i : Fin n} (hi : i ≠ p j) :
    MonotoneOn (fun t => A i t - occupation p τ i t) (Icc (τ j.castSucc) (τ j.succ)) := by
  intro s hs t ht hst
  have h0 : (0 : ℝ) ≤ s := (hτ.nonneg j.castSucc).trans hs.1
  have hT : t ≤ T := ht.2.trans (hτ.mem_Icc j.succ).2
  have hmono := hA.mono i s t h0 hst hT
  have hocc := occupation_other_const p hτ.mono j hi hs.1 hst ht.2
  simp only
  linarith

/-- Every time of the horizon lies in some activation block, provided there is one. -/
private theorem exists_block :
    ∀ (k : ℕ) (τ : Fin (k + 2) → ℝ), Monotone τ → ∀ t : ℝ, τ 0 ≤ t →
      t ≤ τ (Fin.last (k + 1)) → ∃ j : Fin (k + 1), τ j.castSucc ≤ t ∧ t ≤ τ j.succ := by
  intro k
  induction k with
  | zero =>
    intro τ _ t h0 hl
    exact ⟨0, by simpa using h0, by simpa using hl⟩
  | succ k ih =>
    intro τ hτ t h0 hl
    rcases le_total t (τ 1) with h | h
    · exact ⟨0, by simpa using h0, by simpa using h⟩
    · have htail : Monotone (Fin.tail τ) := fun a b hab => hτ (Fin.succ_le_succ_iff.mpr hab)
      have hstart : Fin.tail τ 0 ≤ t := h
      have hend : t ≤ Fin.tail τ (Fin.last (k + 1)) := by
        have hrw : Fin.tail τ (Fin.last (k + 1)) = τ (Fin.last (k + 2)) :=
          congrArg τ (Fin.succ_last _)
        rw [hrw]
        exact hl
      obtain ⟨j0, hj1, hj2⟩ := ih (Fin.tail τ) htail t hstart hend
      refine ⟨j0.succ, ?_, hj2⟩
      have hrw : τ (j0.succ).castSucc = Fin.tail τ j0.castSucc :=
        congrArg τ (Fin.succ_castSucc _).symm
      rw [hrw]
      exact hj1

/-- SC05, the form the package uses: at every time of the horizon a discrepancy is sandwiched
between its values at two switch times. Together with `antitoneOn_selected_discrepancy` and
`monotoneOn_other_discrepancy` this is the statement that both errors are determined by the
activation-block endpoints. -/
theorem exists_switchTime_sandwich {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (i : Fin n)
    {t : ℝ} (ht : t ∈ Icc (0 : ℝ) T) :
    ∃ m₁ m₂ : Fin (k + 1),
      A i (τ m₁) - occupation p τ i (τ m₁) ≤ A i t - occupation p τ i t ∧
      A i t - occupation p τ i t ≤ A i (τ m₂) - occupation p τ i (τ m₂) := by
  cases k with
  | zero =>
    have hT : T ≤ 0 := by
      have h1 : τ (Fin.last 0) ≤ τ 0 := hτ.mono (by simp)
      rwa [hτ.last, hτ.first] at h1
    have htz : t = 0 := le_antisymm (ht.2.trans hT) ht.1
    refine ⟨0, 0, ?_, ?_⟩ <;> rw [hτ.first, htz]
  | succ k =>
    obtain ⟨j, hj1, hj2⟩ := exists_block k τ hτ.mono t (by rw [hτ.first]; exact ht.1)
      (by rw [hτ.last]; exact ht.2)
    have hmemA : τ j.castSucc ∈ Icc (τ j.castSucc) (τ j.succ) :=
      ⟨le_rfl, hτ.mono (Fin.castSucc_le_succ j)⟩
    have hmemB : τ j.succ ∈ Icc (τ j.castSucc) (τ j.succ) :=
      ⟨hτ.mono (Fin.castSucc_le_succ j), le_rfl⟩
    by_cases hi : i = p j
    · subst hi
      have hanti := antitoneOn_selected_discrepancy p hτ hA j
      exact ⟨j.succ, j.castSucc, hanti ⟨hj1, hj2⟩ hmemB hj2, hanti hmemA ⟨hj1, hj2⟩ hj1⟩
    · have hmono := monotoneOn_other_discrepancy p hτ hA j hi
      exact ⟨j.castSucc, j.succ, hmono hmemA ⟨hj1, hj2⟩ hj1, hmono ⟨hj1, hj2⟩ hmemB hj2⟩

/-- SC05 for the full error: a schedule's error is at most `c` exactly when each discrepancy
is at most `c` at each switch time. The input is an arbitrary element of the cumulative
class; nothing is assumed about its behaviour between switch times. -/
theorem D_le_iff_switchTimes {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ} {T : ℝ}
    (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {c : ℝ}
    (hc : 0 ≤ c) :
    D A (occupation p τ) T ≤ c ↔
      ∀ (m : Fin (k + 1)) (i : Fin n), |A i (τ m) - occupation p τ i (τ m)| ≤ c := by
  constructor
  · exact fun h m i => (le_D hA (occupation_isCumulative p hτ) i (hτ.mem_Icc m)).trans h
  · intro h
    refine D_le hc fun i t ht => ?_
    obtain ⟨m₁, m₂, h₁, h₂⟩ := exists_switchTime_sandwich p hτ hA i ht
    have hb₁ := abs_le.mp (h m₁ i)
    have hb₂ := abs_le.mp (h m₂ i)
    rw [abs_le]
    constructor <;> linarith

/-- SC05 for the one-sided error. -/
theorem Dminus_le_iff_switchTimes {n k : ℕ} (p : Fin k → Fin n) {τ : Fin (k + 1) → ℝ}
    {T : ℝ} (hτ : OrderedTimes τ T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {c : ℝ}
    (hc : 0 ≤ c) :
    Dminus A (occupation p τ) T ≤ c ↔
      ∀ (m : Fin (k + 1)) (i : Fin n), occupation p τ i (τ m) - A i (τ m) ≤ c := by
  constructor
  · intro h m i
    exact (le_csSup (lowerErrorSet_bddAbove hA (occupation_isCumulative p hτ))
      ⟨i, τ m, hτ.mem_Icc m, rfl⟩).trans h
  · intro h
    refine Real.sSup_le (fun e he => ?_) hc
    obtain ⟨i, t, ht, rfl⟩ := he
    obtain ⟨m₁, -, h₁, -⟩ := exists_switchTime_sandwich p hτ hA i ht
    linarith [h m₁ i]

/-! ### The grid specialization of SC05 -/

/-- Every grid node lies on the horizon. -/
theorem IsGrid.mem_Icc {N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (q : Fin (N + 1)) : x q ∈ Icc (0 : ℝ) T :=
  ⟨by rw [← hx.first]; exact hx.strictMono.monotone (Fin.zero_le q),
    by rw [← hx.last]; exact hx.strictMono.monotone (Fin.le_last q)⟩

/-- The horizon of a grid is nonnegative. -/
theorem IsGrid.horizon_nonneg {N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T) :
    0 ≤ T := by
  rw [← hx.first, ← hx.last]
  exact hx.strictMono.monotone (Fin.zero_le _)

/-- SC05 on a grid: the full error of a *grid* schedule is determined by the values at the
grid nodes, even when the relaxed input varies inside the cells. -/
theorem gridSchedule_D_le_iff {n N k : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x k W) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) {c : ℝ} (hc : 0 ≤ c) :
    D A W T ≤ c ↔ ∀ (q : Fin (N + 1)) (i : Fin n), |A i (x q) - W i (x q)| ≤ c := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  have hxg : OrderedTimes (x ∘ g) T :=
    ⟨by simp only [Function.comp_apply, hg0, hx.first],
      by simp only [Function.comp_apply, hgl, hx.last], hx.strictMono.monotone.comp hg⟩
  constructor
  · intro h q i
    exact (le_D hA (occupation_isCumulative p hxg) i (hx.mem_Icc q)).trans h
  · intro h
    rw [D_le_iff_switchTimes p hxg hA hc]
    exact fun m i => h (g m) i

/-- SC05 on a grid, one-sided version. -/
theorem gridSchedule_Dminus_le_iff {n N k : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x k W) {A : Fin n → ℝ → ℝ}
    (hA : IsCumulative A T) {c : ℝ} (hc : 0 ≤ c) :
    Dminus A W T ≤ c ↔ ∀ (q : Fin (N + 1)) (i : Fin n), W i (x q) - A i (x q) ≤ c := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  have hxg : OrderedTimes (x ∘ g) T :=
    ⟨by simp only [Function.comp_apply, hg0, hx.first],
      by simp only [Function.comp_apply, hgl, hx.last], hx.strictMono.monotone.comp hg⟩
  constructor
  · intro h q i
    exact (le_csSup (lowerErrorSet_bddAbove hA (occupation_isCumulative p hxg))
      ⟨i, x q, hx.mem_Icc q, rfl⟩).trans h
  · intro h
    rw [Dminus_le_iff_switchTimes p hxg hA hc]
    exact fun m i => h (g m) i

/-! ## SC06: cell averaging and minimax grid domination -/

/-- The cell-average rate matrix of an input: on cell `j` every mode runs at its average rate
across that cell. -/
noncomputable def cellAverage {n N : ℕ} (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ)
    (j : Fin N) (i : Fin n) : ℝ :=
  (A i (x j.succ) - A i (x j.castSucc)) / cellLength x j

/-- SC06, first part: the cell averages of a cumulative input form a rate matrix. -/
theorem isRateMatrix_cellAverage {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) : IsRateMatrix (cellAverage x A) where
  nonneg j i := by
    refine div_nonneg (sub_nonneg.mpr ?_) (hx.cellLength_pos j).le
    exact hA.mono i _ _ (hx.mem_Icc j.castSucc).1
      (hx.strictMono.monotone (Fin.castSucc_le_succ j)) (hx.mem_Icc j.succ).2
  conservation j := by
    simp only [cellAverage]
    rw [← Finset.sum_div, Finset.sum_sub_distrib, hA.conservation _ (hx.mem_Icc j.succ),
      hA.conservation _ (hx.mem_Icc j.castSucc)]
    exact div_self (hx.cellLength_pos j).ne'

/-- The cell average of an input: the grid-constant input that runs at the input's average
rate on each cell. -/
noncomputable def cellAverageInput {n N : ℕ} (x : Fin (N + 1) → ℝ) (A : Fin n → ℝ → ℝ) :
    Fin n → ℝ → ℝ :=
  gridCumulative x (cellAverage x A)

/-- The cell average is a grid-constant input. -/
theorem isGridConstant_cellAverageInput {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    IsGridConstant x (cellAverageInput x A) :=
  ⟨cellAverage x A, isRateMatrix_cellAverage hx hA, rfl⟩

/-- The cell average lies in the cumulative class. -/
theorem isCumulative_cellAverageInput {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) :
    IsCumulative (cellAverageInput x A) T :=
  gridCumulative_isCumulative hx.orderedTimes (isRateMatrix_cellAverage hx hA)

/-- SC06, second part: cell averaging preserves every grid node value of the input. -/
theorem cellAverageInput_node {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (i : Fin n) (q : Fin (N + 1)) :
    cellAverageInput x A i (x q) = A i (x q) := by
  have key : ∀ j : Fin N,
      cellAverage x A j i * (min (x q) (x j.succ) - min (x q) (x j.castSucc)) =
        A i (x (min q j.succ)) - A i (x (min q j.castSucc)) := by
    intro j
    rcases Nat.lt_or_ge (j : ℕ) (q : ℕ) with hjq | hqj
    · have hq1 : j.succ ≤ (q : Fin (N + 1)) := by
        simp only [Fin.le_def, Fin.val_succ]
        omega
      have hq2 : j.castSucc ≤ (q : Fin (N + 1)) := by
        simp only [Fin.le_def, Fin.val_castSucc]
        omega
      have hx1 : x j.succ ≤ x q := hx.strictMono.monotone hq1
      have hx2 : x j.castSucc ≤ x q := hx.strictMono.monotone hq2
      rw [min_eq_right hq1, min_eq_right hq2, min_eq_right hx1, min_eq_right hx2,
        cellAverage]
      exact div_mul_cancel₀ _ (hx.cellLength_pos j).ne'
    · have hq1 : (q : Fin (N + 1)) ≤ j.succ := by
        simp only [Fin.le_def, Fin.val_succ]
        omega
      have hq2 : (q : Fin (N + 1)) ≤ j.castSucc := by
        simp only [Fin.le_def, Fin.val_castSucc]
        omega
      have hx1 : x q ≤ x j.succ := hx.strictMono.monotone hq1
      have hx2 : x q ≤ x j.castSucc := hx.strictMono.monotone hq2
      rw [min_eq_left hq1, min_eq_left hq2, min_eq_left hx1, min_eq_left hx2]
      ring
  simp only [cellAverageInput, gridCumulative]
  rw [Finset.sum_congr rfl fun j _ => key j,
    sum_succ_sub_castSucc' fun m => A i (x (min q m)),
    min_eq_left (Fin.le_last q), min_eq_right (Fin.zero_le q), hx.first, hA.initial, sub_zero]

/-- SC06, third part: cell averaging preserves the full error of every grid schedule. This is
where SC05 does the work: the error of a grid schedule only sees the grid nodes, and the cell
average agrees with the input there. -/
theorem D_cellAverageInput {n N k : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {W : Fin n → ℝ → ℝ}
    (hW : IsGridSchedule x k W) : D A W T = D (cellAverageInput x A) W T := by
  have hWc : IsCumulative W T := (hW.isSchedule hx).isCumulative
  have hAc := isCumulative_cellAverageInput hx hA
  refine le_antisymm ?_ ?_
  · rw [gridSchedule_D_le_iff hx hW hA (D_nonneg hn hAc hWc hx.horizon_nonneg)]
    intro q i
    rw [← cellAverageInput_node hx hA i q]
    exact le_D hAc hWc i (hx.mem_Icc q)
  · rw [gridSchedule_D_le_iff hx hW hAc (D_nonneg hn hA hWc hx.horizon_nonneg)]
    intro q i
    rw [cellAverageInput_node hx hA i q]
    exact le_D hA hWc i (hx.mem_Icc q)

/-- SC06, one-sided version: cell averaging preserves the one-sided error of every grid
schedule. -/
theorem Dminus_cellAverageInput {n N k : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {W : Fin n → ℝ → ℝ}
    (hW : IsGridSchedule x k W) : Dminus A W T = Dminus (cellAverageInput x A) W T := by
  have hWc : IsCumulative W T := (hW.isSchedule hx).isCumulative
  have hAc := isCumulative_cellAverageInput hx hA
  refine le_antisymm ?_ ?_
  · rw [gridSchedule_Dminus_le_iff hx hW hA (Dminus_nonneg hn hAc hWc hx.horizon_nonneg)]
    intro q i
    rw [← cellAverageInput_node hx hA i q]
    exact le_csSup (lowerErrorSet_bddAbove hAc hWc) ⟨i, x q, hx.mem_Icc q, rfl⟩
  · rw [gridSchedule_Dminus_le_iff hx hW hAc (Dminus_nonneg hn hA hWc hx.horizon_nonneg)]
    intro q i
    rw [cellAverageInput_node hx hA i q]
    exact le_csSup (lowerErrorSet_bddAbove hA hWc) ⟨i, x q, hx.mem_Icc q, rfl⟩

/-- SC06: cell averaging preserves the grid instance optimum. -/
theorem gridOPT_cellAverageInput {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s = gridOPT x (cellAverageInput x A) T s := by
  have hset : gridScheduleErrorSet x A T (s + 1) =
      gridScheduleErrorSet x (cellAverageInput x A) T (s + 1) := by
    ext e
    constructor
    · rintro ⟨W, hW, rfl⟩
      exact ⟨W, hW, D_cellAverageInput hn hx hA hW⟩
    · rintro ⟨W, hW, rfl⟩
      exact ⟨W, hW, (D_cellAverageInput hn hx hA hW).symm⟩
  rw [gridOPT, gridOPT, hset]

/-- SC06, one-sided version: cell averaging preserves the one-sided grid instance optimum. -/
theorem gridOPTminus_cellAverageInput {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (k : ℕ) :
    gridOPTminus x A T k = gridOPTminus x (cellAverageInput x A) T k := by
  have hset : gridScheduleLowerErrorSet x A T k =
      gridScheduleLowerErrorSet x (cellAverageInput x A) T k := by
    ext e
    constructor
    · rintro ⟨W, hW, rfl⟩
      exact ⟨W, hW, Dminus_cellAverageInput hn hx hA hW⟩
    · rintro ⟨W, hW, rfl⟩
      exact ⟨W, hW, (Dminus_cellAverageInput hn hx hA hW).symm⟩
  rw [gridOPTminus, gridOPTminus, hset]

/-! ### Restriction inequalities and the minimax comparison -/

/-- Every positive block budget admits at least one grid schedule: activate a single mode on
all of `[0, T]` using grid nodes only. -/
theorem exists_isGridSchedule {n N : ℕ} (hn : 0 < n) (x : Fin (N + 1) → ℝ) {k : ℕ}
    (hk : 0 < k) : ∃ W : Fin n → ℝ → ℝ, IsGridSchedule x k W := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hk.ne'
  refine ⟨occupation (fun _ => ⟨0, hn⟩)
    (x ∘ fun m : Fin (k + 2) => if m = 0 then 0 else Fin.last N),
    fun _ => ⟨0, hn⟩, fun m => if m = 0 then 0 else Fin.last N, ?_, ?_, ?_, rfl⟩
  · intro a b hab
    dsimp only
    by_cases ha : a = 0
    · rw [if_pos ha]
      exact Fin.zero_le _
    · have hb : b ≠ 0 := by
        rintro rfl
        exact ha (le_antisymm hab (Fin.zero_le a))
      rw [if_neg ha, if_neg hb]
  · simp
  · have hlast : (Fin.last (k + 1) : Fin (k + 2)) ≠ 0 :=
      Fin.ne_of_val_ne (by simp)
    simp only [if_neg hlast]

/-- The set of full errors of schedules is bounded below by zero. -/
theorem bddBelow_scheduleErrorSet {n : ℕ} (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) : BddBelow (scheduleErrorSet A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact D_nonneg hn hA hW.isCumulative hT

/-- The set of one-sided errors of schedules is bounded below by zero. -/
theorem bddBelow_scheduleLowerErrorSet {n : ℕ} (hn : 0 < n) {A : Fin n → ℝ → ℝ} {T : ℝ}
    (hA : IsCumulative A T) (hT : 0 ≤ T) (k : ℕ) :
    BddBelow (scheduleLowerErrorSet A T k) := by
  refine ⟨0, ?_⟩
  rintro e ⟨W, hW, rfl⟩
  exact Dminus_nonneg hn hA hW.isCumulative hT

/-- Restricting the switch times to grid nodes can only increase the instance optimum. -/
theorem OPT_le_gridOPT {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) : OPT A T s ≤ gridOPT x A T s := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x (Nat.succ_pos s)
  refine csInf_le_csInf (bddBelow_scheduleErrorSet hn hA hx.horizon_nonneg _)
    ⟨D A W T, W, hW, rfl⟩ ?_
  rintro e ⟨V, hV, rfl⟩
  exact ⟨V, hV.isSchedule hx, rfl⟩

/-- Restricting the switch times to grid nodes can only increase the one-sided instance
optimum. -/
theorem OPTminus_le_gridOPTminus {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {k : ℕ} (hk : 0 < k) :
    OPTminus A T k ≤ gridOPTminus x A T k := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x hk
  refine csInf_le_csInf (bddBelow_scheduleLowerErrorSet hn hA hx.horizon_nonneg _)
    ⟨Dminus A W T, W, hW, rfl⟩ ?_
  rintro e ⟨V, hV, rfl⟩
  exact ⟨V, hV.isSchedule hx, rfl⟩

/-- Every full error of two cumulative allocations is at most the horizon. -/
theorem D_le_horizon {n : ℕ} {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) : D A W T ≤ T :=
  D_le hT fun i t ht => (errorSet_mem_Icc hA hW ⟨i, t, ht, rfl⟩).2

/-- Every one-sided error of two cumulative allocations is at most the horizon. -/
theorem Dminus_le_horizon {n : ℕ} {A W : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    (hW : IsCumulative W T) (hT : 0 ≤ T) : Dminus A W T ≤ T := by
  refine Real.sSup_le (fun e he => ?_) hT
  obtain ⟨i, t, ht, rfl⟩ := he
  linarith [hW.le_self i ht, hA.nonneg i ht, ht.2]

/-- The grid instance optimum never exceeds the horizon. -/
theorem gridOPT_le_horizon {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) (s : ℕ) :
    gridOPT x A T s ≤ T := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x (Nat.succ_pos s)
  refine le_trans (csInf_le ⟨0, ?_⟩ ⟨W, hW, rfl⟩) ?_
  · rintro e ⟨V, hV, rfl⟩
    exact D_nonneg hn hA (hV.isSchedule hx).isCumulative hx.horizon_nonneg
  · exact D_le_horizon hA (hW.isSchedule hx).isCumulative hx.horizon_nonneg

/-- The one-sided grid instance optimum never exceeds the horizon. -/
theorem gridOPTminus_le_horizon {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {k : ℕ} (hk : 0 < k) :
    gridOPTminus x A T k ≤ T := by
  obtain ⟨W, hW⟩ := exists_isGridSchedule hn x hk
  refine le_trans (csInf_le ⟨0, ?_⟩ ⟨W, hW, rfl⟩) ?_
  · rintro e ⟨V, hV, rfl⟩
    exact Dminus_nonneg hn hA (hV.isSchedule hx).isCumulative hx.horizon_nonneg
  · exact Dminus_le_horizon hA (hW.isSchedule hx).isCumulative hx.horizon_nonneg

/-- SC06, the conclusion `eq:minimax-grid-domination`: the continuous minimax value is
dominated by the grid minimax value on every grid.

Note the role of averaging: `gridF` maximizes only over grid-constant inputs, so an arbitrary
cumulative input must first be replaced by its cell average, which by
`gridOPT_cellAverageInput` has the same grid instance optimum. -/
theorem F_le_gridF {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (s : ℕ) : F n s T ≤ gridF x n s T := by
  have hbdd : BddAbove {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧
      v = gridOPT x A T s} := by
    refine ⟨T, ?_⟩
    rintro v ⟨A, ⟨r, hr, rfl⟩, rfl⟩
    exact gridOPT_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) s
  refine csSup_le ⟨OPT (constSchedule ⟨0, hn⟩ T) T s, constSchedule ⟨0, hn⟩ T,
    (isSchedule_constSchedule hx.horizon_nonneg _).isCumulative, rfl⟩ ?_
  rintro v ⟨A, hA, rfl⟩
  refine (OPT_le_gridOPT hn hx hA s).trans ?_
  rw [gridOPT_cellAverageInput hn hx hA s]
  exact le_csSup hbdd ⟨cellAverageInput x A, isGridConstant_cellAverageInput hx hA, rfl⟩

/-- SC06, the one-sided analogue of `eq:minimax-grid-domination`. -/
theorem Gminus_le_gridGminus {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {k : ℕ} (hk : 0 < k) : Gminus n k T ≤ gridGminus x n k T := by
  have hbdd : BddAbove {v : ℝ | ∃ A : Fin n → ℝ → ℝ, IsGridConstant x A ∧
      v = gridOPTminus x A T k} := by
    refine ⟨T, ?_⟩
    rintro v ⟨A, ⟨r, hr, rfl⟩, rfl⟩
    exact gridOPTminus_le_horizon hn hx (gridCumulative_isCumulative hx.orderedTimes hr) hk
  refine csSup_le ⟨OPTminus (constSchedule ⟨0, hn⟩ T) T k, constSchedule ⟨0, hn⟩ T,
    (isSchedule_constSchedule hx.horizon_nonneg _).isCumulative, rfl⟩ ?_
  rintro v ⟨A, hA, rfl⟩
  refine (OPTminus_le_gridOPTminus hn hx hA hk).trans ?_
  rw [gridOPTminus_cellAverageInput hn hx hA k]
  exact le_csSup hbdd ⟨cellAverageInput x A, isGridConstant_cellAverageInput hx hA, rfl⟩

end GridSwitching
