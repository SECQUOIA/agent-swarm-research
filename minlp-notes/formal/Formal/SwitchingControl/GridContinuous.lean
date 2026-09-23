import Formal.SwitchingControl.ResultsCore
import Formal.SwitchingControl.ContinuousGrid

/-! Endpoint certificates control the full time interval for arbitrary grid words. -/
namespace SwitchingControl.GridContinuous

open SwitchingControl.ContinuousGrid

/-- Cumulative occupation inside a unit cell: completed-cell counts plus the
elapsed time assigned to the cell's active mode. -/
def cellOccupation (w : Finite.Word) (j : Fin w.length) (i : Fin 3) (t : ℝ) : ℝ :=
  Finite.countPrefix w j.val i + if w[j] = i then t - j.val else 0

/-- Adding a cell increments precisely its active mode's count. -/
theorem countPrefix_succ (w : Finite.Word) (j : Fin w.length) (i : Fin 3) :
    Finite.countPrefix w (j.val + 1) i =
      Finite.countPrefix w j.val i + if w[j] = i then 1 else 0 := by
  unfold Finite.countPrefix
  rw [List.take_succ_eq_append_getElem j.isLt, List.count_append]
  simp only [List.count_singleton]
  split_ifs <;> simp_all

/-- Each cell starts at its preceding integer cumulative count. -/
theorem cellOccupation_left (w : Finite.Word) (j : Fin w.length) (i : Fin 3) :
    cellOccupation w j i j.val = Finite.countPrefix w j.val i := by
  simp [cellOccupation]

/-- Each cell ends at its following integer cumulative count. -/
theorem cellOccupation_right (w : Finite.Word) (j : Fin w.length) (i : Fin 3) :
    cellOccupation w j i (j.val + 1) = Finite.countPrefix w (j.val + 1) i := by
  rw [countPrefix_succ]
  simp only [cellOccupation, Nat.cast_add, Nat.cast_ite, Nat.cast_one, Nat.cast_zero]
  congr 1
  split_ifs <;> ring

/-- Adjacent cell descriptions give the same occupation at their common boundary. -/
theorem cellOccupation_consistent (w : Finite.Word) (j k : Fin w.length)
    (hjk : k.val = j.val + 1) (i : Fin 3) :
    cellOccupation w j i k.val = cellOccupation w k i k.val := by
  rw [cellOccupation_left]
  have hh : (k.val : ℝ) = j.val + 1 := by exact_mod_cast hjk
  rw [hh, cellOccupation_right, hjk]

/-- A positive-length unit grid covers every point in its continuous horizon. -/
theorem cell_cover {n : ℕ} (hn : 0 < n) (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) n) :
    ∃ j : Fin n, t ∈ Set.Icc (j.val : ℝ) (j.val + 1) := by
  by_cases heq : t = n
  · refine ⟨⟨n - 1, by omega⟩, ?_⟩
    have hn' : ((n - 1 : ℕ) : ℝ) + 1 = n := by exact_mod_cast Nat.sub_add_cancel hn
    simp only [Set.mem_Icc]
    constructor <;> linarith
  · have hlt : t < n := lt_of_le_of_ne ht.2 heq
    have hj : ⌊t⌋₊ < n := (Nat.floor_lt ht.1).mpr hlt
    exact ⟨⟨⌊t⌋₊, hj⟩, Nat.floor_le ht.1, (Nat.lt_floor_add_one t).le⟩

/-- Endpoint certificates control every time inside every cell of any word.
This uses only the cumulative increment bounds, allowing measurable input rates. -/
theorem word_endpoints_bound (w : Finite.Word) {A : Fin 3 → ℝ → ℝ}
    (hA : ValidCumulative A w.length) {E : ℝ} (hE : 0 ≤ E)
    (he : ∀ j : Fin w.length, ∀ i,
      |A i (j.val + 1) - (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ E) :
    ∀ j : Fin w.length, ∀ i : Fin 3, ∀ t ∈ Set.Icc (j.val : ℝ) (j.val + 1),
      |A i t - cellOccupation w j i t| ≤ E := by
  intro j i t ht
  have hleft : |A i j.val - (Finite.countPrefix w j.val i : ℝ)| ≤ E := by
    by_cases hj : j.val = 0
    · simpa [hj, hA.initial, Finite.countPrefix] using hE
    · have hk : j.val - 1 + 1 = j.val := by omega
      have hk' : ((j.val - 1 : ℕ) : ℝ) + 1 = j.val := by exact_mod_cast hk
      simpa only [hk, hk'] using he ⟨j.val - 1, by omega⟩ i
  have hright : |A i (j.val + 1) - cellOccupation w j i (j.val + 1)| ≤ E := by
    simpa only [cellOccupation_right] using he j i
  have hb : (j.val : ℝ) + 1 ≤ w.length := by exact_mod_cast j.isLt
  have hh := Continuous.endpoint_bound (A i) w.length j.val (j.val + 1) t
    (Finite.countPrefix w j.val i) E (decide (w[j] = i)) (hA.increments i)
    (by positivity) ht.1 ht.2 hb hleft
  simp only [Bool.decide_iff] at hh
  exact hh hright

/-- Any endpoint upper theorem yields a full-time bound with the same word
and switch budget, for every cumulative relaxed input. -/
theorem grid_upper_of_endpoint {n budget : ℕ} {E : ℝ} (hE : 0 ≤ E)
    (hgrid : ∀ B : Profile n, ValidProfile B → HasSchedule B budget E)
    (A : Fin 3 → ℝ → ℝ) (hA : ValidCumulative A n) :
    ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
      ∀ j : Fin w.length, ∀ i : Fin 3, ∀ t ∈ Set.Icc (j.val : ℝ) (j.val + 1),
        |A i t - cellOccupation w j i t| ≤ E := by
  obtain ⟨w, hw, hsw, he⟩ := hgrid (sample A) (sample_valid hA)
  refine ⟨w, hw, hsw, word_endpoints_bound w (hw.symm ▸ hA) hE ?_⟩
  intro j i
  exact he ⟨j.val, by rw [← hw]; exact j.isLt⟩ i

/-- The general grid upper bound applies directly to measurable simplex rates. -/
theorem measurable_grid_upper_of_endpoint {n budget : ℕ} {E : ℝ} (hE : 0 ≤ E)
    (hgrid : ∀ B : Profile n, ValidProfile B → HasSchedule B budget E)
    (α : Fin 3 → ℝ → ℝ) (hα : Measurable.SimplexRates α n) :
    ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
      ∀ j : Fin w.length, ∀ i : Fin 3, ∀ t ∈ Set.Icc (j.val : ℝ) (j.val + 1),
        |Measurable.cumulative α i t - cellOccupation w j i t| ≤ E :=
  grid_upper_of_endpoint hE hgrid _ (measurable_valid hα)

/-- Positive time normalization preserves the cumulative class for any grid size. -/
theorem normalize_grid_valid {n : ℕ} {A : Fin 3 → ℝ → ℝ} {Δ : ℝ}
    (hΔ : 0 < Δ) (hA : ValidCumulative A (n * Δ)) :
    ValidCumulative (fun i t => A i (Δ * t) / Δ) n := by
  constructor
  · intro i
    simp [hA.initial]
  · intro i s t hs hst ht
    have h := (hA.increments i) (Δ * s) (Δ * t) (mul_nonneg hΔ.le hs)
      (mul_le_mul_of_nonneg_left hst hΔ.le) (by nlinarith)
    rw [← sub_div]
    constructor
    · exact div_nonneg h.1 hΔ.le
    · apply (div_le_iff₀ hΔ).mpr
      nlinarith [h.2]
  · intro t ht
    rw [← Finset.sum_div, hA.conservation (Δ * t)
      ⟨mul_nonneg hΔ.le ht.1, by nlinarith [ht.2]⟩]
    field_simp

/-- Physical occupation in a cell of positive length `Δ`. -/
noncomputable def scaledCellOccupation (w : Finite.Word) (j : Fin w.length) (i : Fin 3)
    (Δ t : ℝ) : ℝ := Δ * cellOccupation w j i (t / Δ)

/-- The scaled expression assigns exactly unit slope to the active mode. -/
theorem scaledCellOccupation_eq (w : Finite.Word) (j : Fin w.length) (i : Fin 3)
    {Δ : ℝ} (hΔ : 0 < Δ) (t : ℝ) :
    scaledCellOccupation w j i Δ t =
      Δ * Finite.countPrefix w j.val i + if w[j] = i then t - Δ * j.val else 0 := by
  unfold scaledCellOccupation cellOccupation
  split_ifs
  · field_simp
  · ring

/-- The physical right endpoint equals the scaled integer prefix count. -/
theorem scaledCellOccupation_right (w : Finite.Word) (j : Fin w.length) (i : Fin 3)
    {Δ : ℝ} (hΔ : 0 < Δ) :
    scaledCellOccupation w j i Δ (Δ * (j.val + 1)) =
      Δ * (Finite.countPrefix w (j.val + 1) i : ℝ) := by
  have heq : Δ * (j.val + 1) / Δ = j.val + 1 := by field_simp
  simp only [scaledCellOccupation, heq, cellOccupation_right]

/-- Positive-length cells cover their entire scaled continuous horizon. -/
theorem scaled_cell_cover {n : ℕ} (hn : 0 < n) {Δ : ℝ} (hΔ : 0 < Δ)
    (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) (n * Δ)) :
    ∃ j : Fin n, t ∈ Set.Icc (Δ * j.val) (Δ * (j.val + 1)) := by
  have ht' : t / Δ ∈ Set.Icc (0 : ℝ) n :=
    ⟨div_nonneg ht.1 hΔ.le, (div_le_iff₀ hΔ).mpr ht.2⟩
  obtain ⟨j, hj⟩ := cell_cover hn (t / Δ) ht'
  refine ⟨j, ?_, ?_⟩
  · have h := (le_div_iff₀ hΔ).mp hj.1
    nlinarith
  · have h := (div_le_iff₀ hΔ).mp hj.2
    nlinarith

/-- Every endpoint upper theorem gives its full-time scaled grid bound. -/
theorem scaled_grid_upper_of_endpoint {n budget : ℕ} {E Δ : ℝ}
    (hE : 0 ≤ E) (hΔ : 0 < Δ)
    (hgrid : ∀ B : Profile n, ValidProfile B → HasSchedule B budget E)
    (A : Fin 3 → ℝ → ℝ) (hA : ValidCumulative A (n * Δ)) :
    ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
      ∀ j : Fin w.length, ∀ i : Fin 3,
        ∀ t ∈ Set.Icc (Δ * j.val) (Δ * (j.val + 1)),
          |A i t - scaledCellOccupation w j i Δ t| ≤ Δ * E := by
  obtain ⟨w, hw, hs, he⟩ := grid_upper_of_endpoint hE hgrid _ (normalize_grid_valid hΔ hA)
  refine ⟨w, hw, hs, ?_⟩
  intro j i t ht
  have ht' : t / Δ ∈ Set.Icc (j.val : ℝ) (j.val + 1) := by
    constructor
    · apply (le_div_iff₀ hΔ).mpr
      nlinarith [ht.1]
    · apply (div_le_iff₀ hΔ).mpr
      nlinarith [ht.2]
  have hh := mul_le_mul_of_nonneg_left (he j i (t / Δ) ht') hΔ.le
  have hcancel : Δ * (t / Δ) = t := by field_simp
  simp only [hcancel] at hh
  have heq : |A i t - scaledCellOccupation w j i Δ t| =
      Δ * |A i t / Δ - cellOccupation w j i (t / Δ)| := by
    unfold scaledCellOccupation
    calc
      |A i t - Δ * cellOccupation w j i (t / Δ)| =
          |Δ * (A i t / Δ - cellOccupation w j i (t / Δ))| := by
        congr 1
        field_simp
      _ = _ := by rw [abs_mul, abs_of_pos hΔ]
  rwa [heq]

/-- The scaled full-time bound holds directly for every measurable relaxed input. -/
theorem scaled_measurable_grid_upper_of_endpoint {n budget : ℕ} {E Δ : ℝ}
    (hE : 0 ≤ E) (hΔ : 0 < Δ)
    (hgrid : ∀ B : Profile n, ValidProfile B → HasSchedule B budget E)
    (α : Fin 3 → ℝ → ℝ) (hα : Measurable.SimplexRates α (n * Δ)) :
    ∃ w : Finite.Word, w.length = n ∧ Finite.switches w ≤ budget ∧
      ∀ j : Fin w.length, ∀ i : Fin 3,
        ∀ t ∈ Set.Icc (Δ * j.val) (Δ * (j.val + 1)),
          |Measurable.cumulative α i t - scaledCellOccupation w j i Δ t| ≤ Δ * E :=
  scaled_grid_upper_of_endpoint hE hΔ hgrid _ (measurable_valid hα)

end SwitchingControl.GridContinuous
