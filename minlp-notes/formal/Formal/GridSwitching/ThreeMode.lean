import Formal.GridSwitching.OneSwitch
import Formal.GridSwitching.Compactness
import Formal.GridSwitching.LinearPrograms

/-!
# SC21: the three-mode one-switch minimax value on the unit grid

This module discharges the obligation SC21 of `topics/17-grid-switching/CLAIMS.md`:
`cor:three-unit-one` of `paper-switching-control/sections/08-finite-grid-one-switch.tex`,
the residue formula for the one-switch minimax value of three modes on the unit grid
`x_j = j` with horizon `T = N`,
```
F^unit_{3,1}(N) = k         if N = 3k,
                = k + 1/2   if N = 3k+1 and k ≥ 1,
                = k + 3/4   if N = 3k+2,
```
together with the one-cell value `F^unit_{3,1}(1) = 2/3` and the closing observation that the
corrections to `N/3` are `0`, `1/6` and `1/12`, hence not a fixed half-cell correction.

The manuscript's proof of the corollary is self-contained: it does not use the general
arbitrary-grid formula `thm:finite-one`, and neither does this module. Everything is built
from the one-switch error formula `D_oneSwitch` of `Formal.GridSwitching.OneSwitch`.

## Contents

* `unitGrid`, `isGrid_unitGrid`: the grid itself.
* `isGridSchedule_oneSwitch`, `exists_oneSwitch_ne_of_isGridSchedule`: grid schedules with two
  activation blocks are exactly the one-switch schedules whose switch time is a grid node.
  Repeated modes are absorbed through `oneSwitch_const` by switching at the origin, so the
  two-distinct-modes normal form is available without loss.
* `gridOPT_one_le_max`, `le_gridOPT_one`: the resulting two-sided description of the grid
  one-switch optimum in terms of the three error terms of `eq:one-switch-error`.
* `omittedMass_three`, `exists_sorted_three`: with three modes the omitted maximum is the
  terminal mass of the remaining mode, and the terminal masses can be sorted.
* `gridOPT_unit_le_of_second_first`: the upper bound of the `N = 3k` case and of `N = 1` —
  use the second-largest terminal mass first up to the node `κ` and the largest one last.
* `gridOPT_unit_le_of_residue`: the upper bound of the two nontrivial residues, the full case
  analysis of `cor:three-unit-one` driven by the six inequalities `eq:residue-inequalities`.
* `le_gridOPT_unit_of_witness`: the lower-bound mechanism shared by both explicit witnesses.
* `witnessRateOne`, `witnessRateTwo` and their inputs: the two explicit witnesses of the
  source, verbatim. The empty pure blocks at `k = 0` are covered: `witnessRateTwo 0` is the
  two-cell input with rates `(1/4, 1/4, 1/2)` and `(1/2, 1/2, 0)`.
* `gridF_unit_three_mod_zero`, `gridF_unit_three_mod_one`, `gridF_unit_three_mod_two`,
  `gridF_unit_three_one`, `gridF_unit_three_cases`: the values.
* `residue_inequalities_mod_one`, `residue_inequalities_mod_two`: `eq:residue-inequalities`
  by direct substitution.
* `gridF_unit_three_correction`, `gridF_unit_three_correction_not_constant`: the closing
  observation.

## Hypotheses added beyond the source

* `k ≥ 1` in the residue-`1` case is in the source; it is genuinely needed, and it enters
  through the fifth residue inequality `3E ≥ 2L` only.
* The residue-`0` and residue-`2` statements are proved for **every** `k ≥ 0`, so they are
  slightly stronger than the corollary, which assumes `N ≥ 2`. For `k = 0` the residue-`0`
  statement degenerates to the empty grid `N = 0` with value `0`.

## Relation to the other modules

Both bounds are proved directly against the defining infimum of `gridOPT` and supremum of
`gridF`, through `gridOPT_le_D` and `le_gridOPT` of `Formal.GridSwitching.Compactness` and
the two `gridF` counterparts `gridOPT_le_gridF` and `gridF_le_of_forall` added here. No
attainment or compactness statement is used, and the general arbitrary-grid formula
`thm:finite-one` is not used.
-/

namespace GridSwitching

open Set

/-! ## The unit grid -/

/-- The unit grid `x_j = j` on `N` cells. Its horizon is `T = N`. -/
def unitGrid (N : ℕ) : Fin (N + 1) → ℝ := fun j => ((j : ℕ) : ℝ)

@[simp] theorem unitGrid_apply {N : ℕ} (j : Fin (N + 1)) :
    unitGrid N j = ((j : ℕ) : ℝ) := rfl

/-- The unit grid on `N` cells is a grid with horizon `N`. -/
theorem isGrid_unitGrid (N : ℕ) : IsGrid (unitGrid N) (N : ℝ) where
  first := by simp [unitGrid]
  last := by simp [unitGrid]
  strictMono := by
    intro a b hab
    simp only [unitGrid]
    exact_mod_cast hab

/-! ## Two missing pieces of the `gridF` interface

`Formal.GridSwitching.Compactness` supplies `gridOPT_le_D`, `le_gridOPT` and
`gridMinimaxSet_bddAbove`; the two one-sided characterizations of `gridF` itself are added
here. -/

/-- A bound valid for every grid-constant input bounds the grid minimax value from above. -/
theorem gridF_le_of_forall {n N : ℕ} {x : Fin (N + 1) → ℝ} {T c : ℝ} {s : ℕ} (hc : 0 ≤ c)
    (h : ∀ A : Fin n → ℝ → ℝ, IsGridConstant x A → gridOPT x A T s ≤ c) :
    gridF x n s T ≤ c := by
  refine Real.sSup_le (fun v hv => ?_) hc
  obtain ⟨A, hA, rfl⟩ := hv
  exact h A hA

/-! ## Grid schedules with one switch -/

/-- A one-switch schedule whose switch time is a grid node is a grid schedule. -/
theorem isGridSchedule_oneSwitch {n N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (p q : Fin n) (m : Fin (N + 1)) : IsGridSchedule x 2 (oneSwitch p q (x m) T) := by
  refine ⟨![p, q], ![0, m, Fin.last N], ?_, rfl, rfl, ?_⟩
  · refine Fin.monotone_iff_le_succ.mpr fun j => ?_
    fin_cases j
    · simp
    · simpa using Fin.le_last m
  · have hxg : (x ∘ ![(0 : Fin (N + 1)), m, Fin.last N]) = ![0, x m, T] := by
      funext j
      fin_cases j
      · simpa using hx.first
      · rfl
      · simpa using hx.last
    rw [oneSwitch, hxg]

/-- Repeating the mode degenerates the one-switch schedule to a constant schedule. -/
theorem oneSwitch_const {n : ℕ} (r : Fin n) (τ T : ℝ) :
    oneSwitch r r τ T = constSchedule r T := by
  funext i t
  rw [oneSwitch_apply]
  change _ = ∑ j : Fin 1, if r = i then min t (![0, T] j.succ) - min t (![0, T] j.castSucc) else 0
  rw [Fin.sum_univ_one]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Fin.succ_zero_eq_one, Fin.castSucc_zero]
  split_ifs <;> ring

/-- Every grid schedule with two activation blocks is a one-switch schedule between two
distinct modes whose switch time is a grid node. Repeated modes are absorbed by switching at
the origin. -/
theorem exists_oneSwitch_ne_of_isGridSchedule {n N : ℕ} (hn : 1 < n) {x : Fin (N + 1) → ℝ}
    {T : ℝ} (hx : IsGrid x T) {W : Fin n → ℝ → ℝ} (hW : IsGridSchedule x 2 W) :
    ∃ (p q : Fin n) (m : Fin (N + 1)), p ≠ q ∧ W = oneSwitch p q (x m) T := by
  obtain ⟨p, g, hg, hg0, hgl, rfl⟩ := hW
  have hxg : (x ∘ g) = ![0, x (g 1), T] := by
    funext j
    fin_cases j
    · change x (g 0) = 0
      rw [hg0, hx.first]
    · rfl
    · change x (g 2) = T
      rw [show (2 : Fin 3) = Fin.last 2 from rfl, hgl, hx.last]
  have hp : p = ![p 0, p 1] := by
    funext j
    fin_cases j <;> rfl
  have hocc : occupation p (x ∘ g) = oneSwitch (p 0) (p 1) (x (g 1)) T := by
    rw [oneSwitch, hxg]
    exact congrArg (fun w => occupation w ![0, x (g 1), T]) hp
  by_cases hpq : p 0 = p 1
  · obtain ⟨r, hr⟩ := Fintype.exists_ne_of_one_lt_card (by simpa using hn) (p 0)
    refine ⟨r, p 0, 0, hr, ?_⟩
    rw [hocc, ← hpq, oneSwitch_const, hx.first, oneSwitch_zero]
  · exact ⟨p 0, p 1, g 1, hpq, hocc⟩

/-- Every grid node lies between the origin and the horizon. -/
theorem node_mem_Icc {N : ℕ} {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    (m : Fin (N + 1)) : 0 ≤ x m ∧ x m ≤ T :=
  ⟨by rw [← hx.first]; exact hx.strictMono.monotone (Fin.zero_le m),
    by rw [← hx.last]; exact hx.strictMono.monotone (Fin.le_last m)⟩

/-- Upper bound on the one-switch grid optimum from one competing pair and one grid node. -/
theorem gridOPT_one_le_max {n N : ℕ} (hn : 0 < n) {x : Fin (N + 1) → ℝ} {T : ℝ}
    (hx : IsGrid x T) {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {p q : Fin n} (hpq : p ≠ q)
    (m : Fin (N + 1)) :
    gridOPT x A T 1 ≤
      max (omittedMass A T p q)
        (max (initialDeficit A p (x m)) (finalDeficit A T q (x m))) := by
  obtain ⟨h0, hT⟩ := node_mem_Icc hx m
  have h := gridOPT_le_D hn hx hA (h0.trans hT) (isGridSchedule_oneSwitch hx p q m)
  rwa [D_oneSwitch hA hpq h0 hT] at h

/-- Lower bound on the one-switch grid optimum: it suffices to beat every ordered pair of
distinct modes at every grid node. -/
theorem le_gridOPT_one {n N : ℕ} (hn : 1 < n) {x : Fin (N + 1) → ℝ} {T : ℝ} (hx : IsGrid x T)
    {A : Fin n → ℝ → ℝ} (hA : IsCumulative A T) {c : ℝ}
    (h : ∀ (p q : Fin n) (m : Fin (N + 1)), p ≠ q →
      c ≤ max (omittedMass A T p q)
        (max (initialDeficit A p (x m)) (finalDeficit A T q (x m)))) :
    c ≤ gridOPT x A T 1 := by
  refine le_gridOPT (by omega) fun W hW => ?_
  obtain ⟨p, q, m, hpq, rfl⟩ := exists_oneSwitch_ne_of_isGridSchedule hn hx hW
  obtain ⟨h0, hT⟩ := node_mem_Icc hx m
  rw [D_oneSwitch hA hpq h0 hT]
  exact h p q m hpq

/-! ## Three modes: the omitted mass and the sorted terminal masses -/

/-- In `Fin 3` the mode outside a pair of distinct modes is unique. -/
private theorem third_of_three :
    ∀ p q r i : Fin 3, p ≠ q → r ≠ p → r ≠ q → i ≠ p → i ≠ q → i = r := by decide

/-- With three modes the omitted maximum of `lem:one-switch-error` is the terminal mass of
the remaining mode. -/
theorem omittedMass_three {A : Fin 3 → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T) (hT : 0 ≤ T)
    {p q r : Fin 3} (hpq : p ≠ q) (hrp : r ≠ p) (hrq : r ≠ q) :
    omittedMass A T p q = masses A T r := by
  refine le_antisymm (omittedMass_le (hA.nonneg r ⟨hT, le_rfl⟩) fun i hip hiq => ?_)
    (masses_le_omittedMass hrp hrq)
  rw [third_of_three p q r i hpq hrp hrq hip hiq]

/-- Three real values can be labelled in nonincreasing order by distinct indices. -/
private theorem exists_sorted_three (f : Fin 3 → ℝ) :
    ∃ a b c : Fin 3, a ≠ b ∧ a ≠ c ∧ b ≠ c ∧ f c ≤ f b ∧ f b ≤ f a := by
  rcases le_total (f 0) (f 1) with h01 | h01 <;>
    rcases le_total (f 1) (f 2) with h12 | h12 <;>
      rcases le_total (f 0) (f 2) with h02 | h02
  · exact ⟨2, 1, 0, by decide, by decide, by decide, h01, h12⟩
  · exact ⟨2, 1, 0, by decide, by decide, by decide, h01, h12⟩
  · exact ⟨1, 2, 0, by decide, by decide, by decide, h02, h12⟩
  · exact ⟨1, 0, 2, by decide, by decide, by decide, h02, h01⟩
  · exact ⟨2, 0, 1, by decide, by decide, by decide, h01, h02⟩
  · exact ⟨0, 2, 1, by decide, by decide, by decide, h12, h02⟩
  · exact ⟨0, 1, 2, by decide, by decide, by decide, h12, h01⟩
  · exact ⟨0, 1, 2, by decide, by decide, by decide, h12, h01⟩

/-- Three distinct indices of `Fin 3` exhaust a sum over the modes. -/
private theorem sum_three_of_distinct {a b c : Fin 3} (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c)
    (f : Fin 3 → ℝ) : f a + f b + f c = ∑ i, f i := by
  have hset : ({a, b, c} : Finset (Fin 3)) = Finset.univ := by
    refine Finset.eq_univ_of_card _ ?_
    rw [Finset.card_insert_of_notMem (by simp [hab, hac]),
      Finset.card_insert_of_notMem (by simp [hbc]), Finset.card_singleton, Fintype.card_fin]
  rw [← hset, Finset.sum_insert (by simp [hab, hac]), Finset.sum_insert (by simp [hbc]),
    Finset.sum_singleton]
  ring

/-! ## One candidate pair on the unit grid -/

/-- A single competing pair `p → q` at a single grid node bounds the unit-grid one-switch
optimum, once the three terms of `eq:one-switch-error` are bounded: the omitted terminal mass
`A r N`, the initial deficit `j - A p j`, and the final deficit `N - A q N - j`. -/
theorem gridOPT_unit_le_of_candidate {N : ℕ} {A : Fin 3 → ℝ → ℝ} (hA : IsCumulative A (N : ℝ))
    {p q r : Fin 3} (hpq : p ≠ q) (hrp : r ≠ p) (hrq : r ≠ q) (j : ℕ) (hj : j ≤ N) {E : ℝ}
    (h1 : A r (N : ℝ) ≤ E) (h2 : (j : ℝ) - A p (j : ℝ) ≤ E)
    (h3 : (N : ℝ) - A q (N : ℝ) - (j : ℝ) ≤ E) :
    gridOPT (unitGrid N) A (N : ℝ) 1 ≤ E := by
  have hm : unitGrid N ⟨j, Nat.lt_succ_of_le hj⟩ = (j : ℝ) := rfl
  refine (gridOPT_one_le_max (by norm_num) (isGrid_unitGrid N) hA hpq
    ⟨j, Nat.lt_succ_of_le hj⟩).trans ?_
  rw [omittedMass_three hA (Nat.cast_nonneg N) hpq hrp hrq, hm]
  exact max_le h1 (max_le h2 h3)

/-! ## The upper bound for the residue `N = 3k`, and for `N = 1`

Following `cor:three-unit-one`: use the second-largest terminal mass first, up to the node
`κ`, and the largest terminal mass last. -/

/-- Upper bound from the schedule "second-largest mass first until the node `κ`, largest mass
last". The three hypotheses are `E ≥ N/3`, `κ ≤ E` and `2N/3 - κ ≤ E`. -/
theorem gridOPT_unit_le_of_second_first {N : ℕ} {A : Fin 3 → ℝ → ℝ}
    (hA : IsCumulative A (N : ℝ)) (kn : ℕ) (hk : kn ≤ N) {E : ℝ}
    (e1 : (N : ℝ) ≤ 3 * E) (e2 : (kn : ℝ) ≤ E) (e3 : 2 * (N : ℝ) ≤ 3 * ((kn : ℝ) + E)) :
    gridOPT (unitGrid N) A (N : ℝ) 1 ≤ E := by
  have hT0 : (0 : ℝ) ≤ (N : ℝ) := Nat.cast_nonneg N
  have hk0 : (0 : ℝ) ≤ (kn : ℝ) := Nat.cast_nonneg kn
  have hkT : (kn : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hk
  obtain ⟨a, b, c, hab, hac, hbc, hcb, hba⟩ := exists_sorted_three fun i => A i (N : ℝ)
  have hcb' : A c (N : ℝ) ≤ A b (N : ℝ) := hcb
  have hba' : A b (N : ℝ) ≤ A a (N : ℝ) := hba
  have hsumN : A a (N : ℝ) + A b (N : ℝ) + A c (N : ℝ) = (N : ℝ) := by
    rw [sum_three_of_distinct hab hac hbc fun i => A i (N : ℝ)]
    exact hA.conservation _ ⟨hT0, le_rfl⟩
  have hbk0 : 0 ≤ A b (kn : ℝ) := hA.nonneg b ⟨hk0, hkT⟩
  refine gridOPT_unit_le_of_candidate hA (Ne.symm hab) (Ne.symm hbc) (Ne.symm hac) kn hk
    ?_ ?_ ?_
  · linarith
  · linarith
  · linarith

/-! ## The upper bound for the residues `N = 3k+1` and `N = 3k+2`

This is the case analysis of `cor:three-unit-one`, driven by the six inequalities of
`eq:residue-inequalities` at the node `L` together with the node `κ`. -/

/-- SC21, upper bound. If `E`, the node `L` and the node `κ` satisfy the six inequalities of
`eq:residue-inequalities` (here written `N ≤ 3E`, `N - L ≤ 2E`, `N + L ≤ 4E`,
`2N ≤ 3(E + L)`, `2L ≤ 3E`, `2N ≤ 3E + κ + 2L`) together with `κ ≤ E`, then every cumulative
input on the unit grid admits a one-switch grid schedule of error at most `E`. -/
theorem gridOPT_unit_le_of_residue {N : ℕ} {A : Fin 3 → ℝ → ℝ} (hA : IsCumulative A (N : ℝ))
    {kn Ln : ℕ} (hk : kn ≤ N) (hL : Ln ≤ N) {E : ℝ}
    (e1 : (N : ℝ) ≤ 3 * E) (e2 : (N : ℝ) - (Ln : ℝ) ≤ 2 * E)
    (e3 : (N : ℝ) + (Ln : ℝ) ≤ 4 * E) (e4 : 2 * (N : ℝ) ≤ 3 * (E + (Ln : ℝ)))
    (e5 : 2 * (Ln : ℝ) ≤ 3 * E) (e6 : 2 * (N : ℝ) ≤ 3 * E + (kn : ℝ) + 2 * (Ln : ℝ))
    (e7 : (kn : ℝ) ≤ E) :
    gridOPT (unitGrid N) A (N : ℝ) 1 ≤ E := by
  have hT0 : (0 : ℝ) ≤ (N : ℝ) := Nat.cast_nonneg N
  have hL0 : (0 : ℝ) ≤ (Ln : ℝ) := Nat.cast_nonneg Ln
  have hLT : (Ln : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hL
  have hk0 : (0 : ℝ) ≤ (kn : ℝ) := Nat.cast_nonneg kn
  have hkT : (kn : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hk
  have hLmem : (Ln : ℝ) ∈ Icc (0 : ℝ) (N : ℝ) := ⟨hL0, hLT⟩
  obtain ⟨a, b, c, hab, hac, hbc, hcb, hba⟩ := exists_sorted_three fun i => A i (N : ℝ)
  have hcb' : A c (N : ℝ) ≤ A b (N : ℝ) := hcb
  have hba' : A b (N : ℝ) ≤ A a (N : ℝ) := hba
  have hsumN : A a (N : ℝ) + A b (N : ℝ) + A c (N : ℝ) = (N : ℝ) := by
    rw [sum_three_of_distinct hab hac hbc fun i => A i (N : ℝ)]
    exact hA.conservation _ ⟨hT0, le_rfl⟩
  have hsumL : A a (Ln : ℝ) + A b (Ln : ℝ) + A c (Ln : ℝ) = (Ln : ℝ) := by
    rw [sum_three_of_distinct hab hac hbc fun i => A i (Ln : ℝ)]
    exact hA.conservation _ hLmem
  have hcLN : A c (Ln : ℝ) ≤ A c (N : ℝ) := hA.mono c _ _ hL0 hLT le_rfl
  have hmcE : A c (N : ℝ) ≤ E := by linarith
  by_cases hcase : E < A b (N : ℝ)
  · -- Two terminal masses exceed `E`; their allocations at `L` sum to more than `2(L - E)`.
    have haE : E < A a (N : ℝ) := lt_of_lt_of_le hcase hba'
    have hkey : 2 * ((Ln : ℝ) - E) < A a (Ln : ℝ) + A b (Ln : ℝ) := by linarith
    rcases lt_or_ge ((Ln : ℝ) - E) (A a (Ln : ℝ)) with h | h
    · exact gridOPT_unit_le_of_candidate hA hab (Ne.symm hac) (Ne.symm hbc) Ln hL hmcE
        (by linarith) (by linarith)
    · exact gridOPT_unit_le_of_candidate hA (Ne.symm hab) (Ne.symm hbc) (Ne.symm hac) Ln hL
        hmcE (by linarith) (by linarith)
  · -- At most one terminal mass exceeds `E`.
    have hbE : A b (N : ℝ) ≤ E := not_lt.mp hcase
    by_cases h21 : (N : ℝ) - E - (kn : ℝ) ≤ A a (N : ℝ)
    · -- The order `b → a` at the node `κ` works.
      have hbk0 : 0 ≤ A b (kn : ℝ) := hA.nonneg b ⟨hk0, hkT⟩
      exact gridOPT_unit_le_of_candidate hA (Ne.symm hab) (Ne.symm hbc) (Ne.symm hac) kn hk
        hmcE (by linarith) (by linarith)
    · replace h21 : A a (N : ℝ) < (N : ℝ) - E - (kn : ℝ) := not_le.mp h21
      have hma : (N : ℝ) ≤ 3 * A a (N : ℝ) := by linarith
      have he4 : 2 * (N : ℝ) ≤ 3 * (E + (Ln : ℝ)) := e4
      have hfa : (N : ℝ) - A a (N : ℝ) - (Ln : ℝ) ≤ E := by linarith
      rcases le_or_gt ((Ln : ℝ) - E) (A b (Ln : ℝ)) with h | hb
      · exact gridOPT_unit_le_of_candidate hA (Ne.symm hab) (Ne.symm hbc) (Ne.symm hac) Ln hL
          hmcE (by linarith) hfa
      · rcases le_or_gt ((Ln : ℝ) - E) (A c (Ln : ℝ)) with h | hc
        · exact gridOPT_unit_le_of_candidate hA (Ne.symm hac) hbc (Ne.symm hab) Ln hL hbE
            (by linarith) hfa
        · -- Both small modes are behind at `L`, so the largest mode is ahead there.
          have hAaL : 2 * E - (Ln : ℝ) < A a (Ln : ℝ) := by linarith
          have hmb : (N : ℝ) - E - (Ln : ℝ) < A b (N : ℝ) := by linarith
          exact gridOPT_unit_le_of_candidate hA hab (Ne.symm hac) (Ne.symm hbc) Ln hL hmcE
            (by linarith) (by linarith)

/-! ## Grid-constant inputs on the unit grid

A grid-constant input on the unit grid is described by a rate function of the *natural*
cell index; its cumulative allocation at an integer time is the partial sum of the rates. -/

/-- Cumulative allocation of a unit-grid input at an integer time. -/
theorem gridCumulative_unitGrid_nat {n N : ℕ} (R : ℕ → Fin n → ℝ) (i : Fin n) {M : ℕ}
    (hM : M ≤ N) :
    gridCumulative (unitGrid N) (fun j : Fin N => R (j : ℕ)) i (M : ℝ)
      = ∑ j ∈ Finset.range M, R j i := by
  have hterm : ∀ j : Fin N,
      R (j : ℕ) i * (min (M : ℝ) (unitGrid N j.succ) - min (M : ℝ) (unitGrid N j.castSucc))
        = if (j : ℕ) < M then R (j : ℕ) i else 0 := by
    intro j
    have h1 : unitGrid N j.succ = ((j : ℕ) : ℝ) + 1 := by
      simp [unitGrid]
    have h2 : unitGrid N j.castSucc = ((j : ℕ) : ℝ) := by
      simp [unitGrid]
    rw [h1, h2]
    by_cases h : (j : ℕ) < M
    · have hj1 : ((j : ℕ) : ℝ) + 1 ≤ (M : ℝ) := by exact_mod_cast h
      rw [if_pos h, min_eq_right hj1, min_eq_right (by linarith : ((j : ℕ) : ℝ) ≤ (M : ℝ))]
      ring
    · have hj0 : (M : ℝ) ≤ ((j : ℕ) : ℝ) := by exact_mod_cast Nat.le_of_not_lt h
      rw [if_neg h, min_eq_left hj0, min_eq_left (by linarith : (M : ℝ) ≤ ((j : ℕ) : ℝ) + 1)]
      ring
  rw [gridCumulative, Finset.sum_congr rfl fun j _ => hterm j,
    Fin.sum_univ_eq_sum_range (fun j => if j < M then R j i else 0) N,
    ← Finset.sum_subset
      (show Finset.range M ⊆ Finset.range N from fun j hj =>
        Finset.mem_range.mpr ((Finset.mem_range.mp hj).trans_le hM))
      (fun j _ hj => if_neg (by simpa using hj))]
  exact Finset.sum_congr rfl fun j hj => if_pos (Finset.mem_range.mp hj)

/-! ## The uniform input, and the residue `N = 3k` -/

/-- The uniform three-mode rate matrix. -/
noncomputable def uniformThree (N : ℕ) : Fin N → Fin 3 → ℝ := fun _ _ => 1 / 3

theorem isRateMatrix_uniformThree (N : ℕ) : IsRateMatrix (uniformThree N) where
  nonneg _ _ := by norm_num [uniformThree]
  conservation _ := by norm_num [uniformThree, Fin.sum_univ_three]

/-- The uniform input on the unit grid. -/
noncomputable def uniformInput (N : ℕ) : Fin 3 → ℝ → ℝ :=
  gridCumulative (unitGrid N) (uniformThree N)

theorem isGridConstant_uniformInput (N : ℕ) :
    IsGridConstant (unitGrid N) (uniformInput N) :=
  ⟨uniformThree N, isRateMatrix_uniformThree N, rfl⟩

theorem isCumulative_uniformInput (N : ℕ) : IsCumulative (uniformInput N) (N : ℝ) :=
  gridCumulative_isCumulative (isGrid_unitGrid N).orderedTimes (isRateMatrix_uniformThree N)

/-- Every mode of the uniform input has accumulated a third of the elapsed time. -/
theorem uniformInput_apply {N : ℕ} (i : Fin 3) {t : ℝ} (ht : t ∈ Icc (0 : ℝ) (N : ℝ)) :
    uniformInput N i t = t / 3 := by
  have hcons := (isCumulative_uniformInput N).conservation t ht
  have hconst : ∀ i' : Fin 3, uniformInput N i' t = uniformInput N i t := fun _ => rfl
  rw [Finset.sum_congr rfl fun i' _ => hconst i', Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at hcons
  norm_num at hcons
  linarith

/-- Two distinct modes of `Fin 3` leave a third one. -/
private theorem exists_third : ∀ p q : Fin 3, p ≠ q → ∃ r : Fin 3, r ≠ p ∧ r ≠ q := by decide

/-- Lower bound for the residue `N = 3k`: against the uniform input every one-switch grid
schedule omits a mode of terminal mass `N / 3`. -/
theorem le_gridOPT_uniformInput (N : ℕ) :
    (N : ℝ) / 3 ≤ gridOPT (unitGrid N) (uniformInput N) (N : ℝ) 1 := by
  refine le_gridOPT_one (by norm_num) (isGrid_unitGrid N) (isCumulative_uniformInput N) ?_
  rintro p q m hpq
  obtain ⟨r, hrp, hrq⟩ := exists_third p q hpq
  refine le_max_of_le_left ?_
  have h := masses_le_omittedMass (A := uniformInput N) (T := (N : ℝ)) hrp hrq
  rwa [show masses (uniformInput N) (N : ℝ) r = (N : ℝ) / 3 from
    uniformInput_apply r ⟨Nat.cast_nonneg N, le_rfl⟩] at h

/-- Lower bound for `N = 1`: against the uniform input, a grid switch at the origin leaves a
final deficit `2/3` and a grid switch at the horizon leaves an initial deficit `2/3`. This is
`prop:no-switch` at `n = 3`, in the form the one-switch value needs. -/
theorem le_gridOPT_uniformInput_one :
    (2 : ℝ) / 3 ≤ gridOPT (unitGrid 1) (uniformInput 1) ((1 : ℕ) : ℝ) 1 := by
  have hmass : ∀ i : Fin 3, uniformInput 1 i (1 : ℝ) = 1 / 3 := fun i =>
    uniformInput_apply i ⟨by norm_num, by norm_num⟩
  refine le_gridOPT_one (by norm_num) (isGrid_unitGrid 1) (isCumulative_uniformInput 1) ?_
  rintro p q m -
  fin_cases m
  · refine le_max_of_le_right (le_max_of_le_right ?_)
    simp only [finalDeficit, masses, unitGrid_apply]
    norm_num [hmass q]
  · refine le_max_of_le_right (le_max_of_le_left ?_)
    simp only [initialDeficit, unitGrid_apply]
    norm_num [hmass p]

/-! ## SC21 for the residue `N = 3k` and for `N = 1` -/

/-- SC21, `eq:three-unit-one` for `N = 3k`: the value is `k`. -/
theorem gridF_unit_three_mod_zero (k : ℕ) :
    gridF (unitGrid (3 * k)) 3 1 ((3 * k : ℕ) : ℝ) = (k : ℝ) := by
  refine le_antisymm (gridF_le_of_forall (Nat.cast_nonneg k) fun A hA => ?_) ?_
  · obtain ⟨r, hr, rfl⟩ := hA
    refine gridOPT_unit_le_of_second_first
      (gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes hr) k (by omega) ?_ ?_ ?_ <;>
      · push_cast
        linarith
  · have h := (le_gridOPT_uniformInput (3 * k)).trans
      (gridOPT_le_gridF (by norm_num) (isGrid_unitGrid (3 * k))
        (isGridConstant_uniformInput (3 * k)) 1)
    have hcast : ((3 * k : ℕ) : ℝ) / 3 = (k : ℝ) := by
      push_cast
      ring
    rwa [hcast] at h

/-- SC21, the one-cell value: `F^unit_{3,1}(1) = 2/3`, which is `prop:no-switch` at
`n = 3`. -/
theorem gridF_unit_three_one : gridF (unitGrid 1) 3 1 (1 : ℝ) = 2 / 3 := by
  have hone : ((1 : ℕ) : ℝ) = (1 : ℝ) := Nat.cast_one
  rw [← hone]
  refine le_antisymm (gridF_le_of_forall (by norm_num) fun A hA => ?_) ?_
  · obtain ⟨r, hr, rfl⟩ := hA
    refine gridOPT_unit_le_of_second_first
      (gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes hr) 0 (by omega) ?_ ?_ ?_ <;>
      · push_cast
        norm_num
  · exact le_gridOPT_uniformInput_one.trans
      (gridOPT_le_gridF (by norm_num) (isGrid_unitGrid 1) (isGridConstant_uniformInput 1) 1)

/-! ## The lower-bound mechanism of the two nontrivial residues

In both witnesses the two selected modes are `0` and `1`; they carry terminal mass `E` and
allocation `L - E` at the node `L`. Omitting either gives error at least `E`; an early switch
leaves a final deficit at least `E`; a late switch leaves an initial deficit at least `E`. -/

/-- SC21, lower bound. If modes `0` and `1` both have terminal mass `E` and both have
allocation `L - E` at the node `L`, and `2E + L ≤ N + 1`, then every one-switch grid schedule
has error at least `E`. -/
theorem le_gridOPT_unit_of_witness {N : ℕ} {A : Fin 3 → ℝ → ℝ} (hA : IsCumulative A (N : ℝ))
    {Ln : ℕ} {E : ℝ} (hm0 : A 0 (N : ℝ) = E) (hm1 : A 1 (N : ℝ) = E)
    (h0L : A 0 ((Ln : ℕ) : ℝ) = ((Ln : ℕ) : ℝ) - E)
    (h1L : A 1 ((Ln : ℕ) : ℝ) = ((Ln : ℕ) : ℝ) - E)
    (hearly : 2 * E + ((Ln : ℕ) : ℝ) ≤ (N : ℝ) + 1) :
    E ≤ gridOPT (unitGrid N) A (N : ℝ) 1 := by
  have hL0 : (0 : ℝ) ≤ ((Ln : ℕ) : ℝ) := Nat.cast_nonneg Ln
  refine le_gridOPT_one (by norm_num) (isGrid_unitGrid N) hA ?_
  rintro p q m -
  have hjN : (m : ℕ) ≤ N := Nat.lt_succ_iff.mp m.isLt
  have hgrid : unitGrid N m = ((m : ℕ) : ℝ) := rfl
  have main : ∀ p' q' : Fin 3, A q' (N : ℝ) = E → A p' ((Ln : ℕ) : ℝ) = ((Ln : ℕ) : ℝ) - E →
      E ≤ max (initialDeficit A p' (unitGrid N m))
        (finalDeficit A (N : ℝ) q' (unitGrid N m)) := by
    intro p' q' hq' hp'
    rcases lt_or_ge (m : ℕ) Ln with hlt | hge
    · refine le_max_of_le_right ?_
      have hj : ((m : ℕ) : ℝ) + 1 ≤ ((Ln : ℕ) : ℝ) := by exact_mod_cast hlt
      simp only [finalDeficit, masses, hgrid, hq']
      linarith
    · refine le_max_of_le_left ?_
      have hle : ((Ln : ℕ) : ℝ) ≤ ((m : ℕ) : ℝ) := by exact_mod_cast hge
      have hmN : ((m : ℕ) : ℝ) ≤ (N : ℝ) := by exact_mod_cast hjN
      have hmono := initialDeficit_mono hA p' hL0 hle hmN
      simp only [initialDeficit, hp'] at hmono
      simp only [initialDeficit, hgrid]
      linarith
  by_cases hz : p = 0 ∨ q = 0
  · by_cases ho : p = 1 ∨ q = 1
    · rcases hz with hp0 | hq0
      · have hq1 : q = 1 := by
          rcases ho with h | h
          · exact absurd (hp0.symm.trans h) (by decide)
          · exact h
        subst hp0
        subst hq1
        exact le_max_of_le_right (main 0 1 hm1 h0L)
      · have hp1 : p = 1 := by
          rcases ho with h | h
          · exact h
          · exact absurd (hq0.symm.trans h) (by decide)
        subst hq0
        subst hp1
        exact le_max_of_le_right (main 1 0 hm0 h1L)
    · obtain ⟨hx1, hx2⟩ := not_or.mp ho
      refine le_max_of_le_left ?_
      rw [← hm1]
      exact masses_le_omittedMass (Ne.symm hx1) (Ne.symm hx2)
  · obtain ⟨hx1, hx2⟩ := not_or.mp hz
    refine le_max_of_le_left ?_
    rw [← hm0]
    exact masses_le_omittedMass (Ne.symm hx1) (Ne.symm hx2)

/-! ## Block sums -/

private theorem sum_range_of_const {a : ℕ} (f : ℕ → ℝ) (c : ℝ) (h : ∀ j, j < a → f j = c) :
    ∑ j ∈ Finset.range a, f j = (a : ℝ) * c := by
  rw [Finset.sum_congr rfl fun j hj => h j (Finset.mem_range.mp hj), Finset.sum_const,
    Finset.card_range, nsmul_eq_mul]

private theorem sum_Ico_of_const {a b : ℕ} (f : ℕ → ℝ) (c : ℝ) (e : ℕ) (he : b - a = e)
    (h : ∀ j, a ≤ j → j < b → f j = c) : ∑ j ∈ Finset.Ico a b, f j = (e : ℝ) * c := by
  rw [Finset.sum_congr rfl fun j hj =>
      h j (Finset.mem_Ico.mp hj).1 (Finset.mem_Ico.mp hj).2,
    Finset.sum_const, Nat.card_Ico, he, nsmul_eq_mul]

private theorem sum_range_split (f : ℕ → ℝ) {a b c d : ℕ} (hab : a ≤ b) (hbc : b ≤ c)
    (hcd : c ≤ d) :
    ∑ j ∈ Finset.range d, f j =
      (∑ j ∈ Finset.range a, f j) + (∑ j ∈ Finset.Ico a b, f j)
        + (∑ j ∈ Finset.Ico b c, f j) + (∑ j ∈ Finset.Ico c d, f j) := by
  simp only [Finset.range_eq_Ico]
  rw [← Finset.sum_Ico_consecutive f (Nat.zero_le c) hcd,
    ← Finset.sum_Ico_consecutive f (Nat.zero_le b) hbc,
    ← Finset.sum_Ico_consecutive f (Nat.zero_le a) hab]

/-! ## The witness for `N = 3k+1` -/

/-- The `N = 3k+1` witness of `cor:three-unit-one`: `k` pure cells of mode `2`, one cell with
rates `(1/2, 1/2, 0)`, then `k` pure cells of mode `0` and `k` pure cells of mode `1`. -/
noncomputable def witnessRateOne (k j : ℕ) (i : Fin 3) : ℝ :=
  if j < k then ![0, 0, 1] i
  else if j = k then ![1 / 2, 1 / 2, 0] i
  else if j < 2 * k + 1 then ![1, 0, 0] i
  else ![0, 1, 0] i

theorem isRateMatrix_witnessRateOne (k N : ℕ) :
    IsRateMatrix (fun j : Fin N => witnessRateOne k (j : ℕ)) where
  nonneg j i := by
    simp only [witnessRateOne]
    split_ifs <;> fin_cases i <;> simp
  conservation j := by
    rw [Fin.sum_univ_three]
    simp only [witnessRateOne]
    split_ifs <;> norm_num [Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons]

/-- Allocation of modes `0` and `1` up to the node `L = k + 1`. -/
private theorem witnessOne_sum_node (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    ∑ j ∈ Finset.range (k + 1), witnessRateOne k j i = 1 / 2 := by
  rw [Finset.sum_range_succ,
    sum_range_of_const (fun j => witnessRateOne k j i) (![0, 0, 1] i)
      (fun j hj => by simp only [witnessRateOne]; rw [if_pos hj])]
  rcases hi with rfl | rfl <;> norm_num [witnessRateOne]

/-- Terminal masses of modes `0` and `1`. -/
private theorem witnessOne_sum_top (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    ∑ j ∈ Finset.range (3 * k + 1), witnessRateOne k j i = (k : ℝ) + 1 / 2 := by
  have h1 : ∑ j ∈ Finset.Ico (k + 1) (2 * k + 1), witnessRateOne k j i
      = (k : ℝ) * ![1, 0, 0] i :=
    sum_Ico_of_const _ _ k (by omega) fun j hj1 hj2 => by
      simp only [witnessRateOne]
      rw [if_neg (by omega), if_neg (by omega), if_pos hj2]
  have h2 : ∑ j ∈ Finset.Ico (2 * k + 1) (3 * k + 1), witnessRateOne k j i
      = (k : ℝ) * ![0, 1, 0] i :=
    sum_Ico_of_const _ _ k (by omega) fun j hj1 _ => by
      simp only [witnessRateOne]
      rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]
  have h3 : ∑ j ∈ Finset.Ico (3 * k + 1) (3 * k + 1), witnessRateOne k j i = 0 := by simp
  rw [sum_range_split (fun j => witnessRateOne k j i) (a := k + 1) (b := 2 * k + 1)
      (c := 3 * k + 1) (by omega) (by omega) (le_refl _),
    witnessOne_sum_node k hi, h1, h2, h3]
  rcases hi with rfl | rfl <;> norm_num <;> ring

/-- The `N = 3k+1` witness input. -/
noncomputable def witnessOneInput (k : ℕ) : Fin 3 → ℝ → ℝ :=
  gridCumulative (unitGrid (3 * k + 1)) fun j : Fin (3 * k + 1) => witnessRateOne k (j : ℕ)

theorem isGridConstant_witnessOneInput (k : ℕ) :
    IsGridConstant (unitGrid (3 * k + 1)) (witnessOneInput k) :=
  ⟨_, isRateMatrix_witnessRateOne k _, rfl⟩

theorem isCumulative_witnessOneInput (k : ℕ) :
    IsCumulative (witnessOneInput k) ((3 * k + 1 : ℕ) : ℝ) :=
  gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes
    (isRateMatrix_witnessRateOne k _)

/-- Both selected modes of the `N = 3k+1` witness have terminal mass `E = k + 1/2`. -/
theorem witnessOneInput_top (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    witnessOneInput k i ((3 * k + 1 : ℕ) : ℝ) = (k : ℝ) + 1 / 2 := by
  rw [witnessOneInput, gridCumulative_unitGrid_nat _ _ (le_refl (3 * k + 1)),
    witnessOne_sum_top k hi]

/-- Both selected modes of the `N = 3k+1` witness have allocation `1/2 = L - E` at the node
`L = k + 1`. -/
theorem witnessOneInput_node (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    witnessOneInput k i ((k + 1 : ℕ) : ℝ) = 1 / 2 := by
  rw [witnessOneInput, gridCumulative_unitGrid_nat _ _ (by omega : k + 1 ≤ 3 * k + 1),
    witnessOne_sum_node k hi]

/-! ## SC21 for the residue `N = 3k+1` -/

/-- The six inequalities `eq:residue-inequalities` for `N = 3k+1`, `E = k + 1/2`,
`L = k + 1`, `κ = k`, verified by direct substitution. The fifth one, `3E ≥ 2L`, is where
`k ≥ 1` is needed. -/
theorem residue_inequalities_mod_one {k : ℕ} (hk : 1 ≤ k) :
    ((3 * k + 1 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 1 / 2) ∧
      ((3 * k + 1 : ℕ) : ℝ) - ((k + 1 : ℕ) : ℝ) ≤ 2 * ((k : ℝ) + 1 / 2) ∧
      ((3 * k + 1 : ℕ) : ℝ) + ((k + 1 : ℕ) : ℝ) ≤ 4 * ((k : ℝ) + 1 / 2) ∧
      2 * ((3 * k + 1 : ℕ) : ℝ) ≤ 3 * (((k : ℝ) + 1 / 2) + ((k + 1 : ℕ) : ℝ)) ∧
      2 * ((k + 1 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 1 / 2) ∧
      2 * ((3 * k + 1 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 1 / 2) + (k : ℝ) + 2 * ((k + 1 : ℕ) : ℝ) := by
  have hk' : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · push_cast
      linarith

/-- SC21, `eq:three-unit-one` for `N = 3k+1` with `k ≥ 1`: the value is `k + 1/2`. -/
theorem gridF_unit_three_mod_one {k : ℕ} (hk : 1 ≤ k) :
    gridF (unitGrid (3 * k + 1)) 3 1 ((3 * k + 1 : ℕ) : ℝ) = (k : ℝ) + 1 / 2 := by
  obtain ⟨d1, d2, d3, d4, d5, d6⟩ := residue_inequalities_mod_one hk
  refine le_antisymm (gridF_le_of_forall (by positivity) fun A hA => ?_) ?_
  · obtain ⟨r, hr, rfl⟩ := hA
    exact gridOPT_unit_le_of_residue
      (gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes hr)
      (kn := k) (Ln := k + 1) (by omega) (by omega) d1 d2 d3 d4 d5 d6 (by linarith)
  · refine le_trans ?_ (gridOPT_le_gridF (by norm_num) (isGrid_unitGrid _)
      (isGridConstant_witnessOneInput k) 1)
    refine le_gridOPT_unit_of_witness (isCumulative_witnessOneInput k) (Ln := k + 1)
      (witnessOneInput_top k (Or.inl rfl)) (witnessOneInput_top k (Or.inr rfl)) ?_ ?_ ?_
    · rw [witnessOneInput_node k (Or.inl rfl)]
      push_cast
      ring
    · rw [witnessOneInput_node k (Or.inr rfl)]
      push_cast
      ring
    · push_cast
      linarith

/-! ## The witness for `N = 3k+2` -/

/-- The `N = 3k+2` witness of `cor:three-unit-one`: the mixed cell of the previous witness is
replaced by `(1/4, 1/4, 1/2)` and one final cell with rates `(1/2, 1/2, 0)` is appended. -/
noncomputable def witnessRateTwo (k j : ℕ) (i : Fin 3) : ℝ :=
  if j < k then ![0, 0, 1] i
  else if j = k then ![1 / 4, 1 / 4, 1 / 2] i
  else if j < 2 * k + 1 then ![1, 0, 0] i
  else if j < 3 * k + 1 then ![0, 1, 0] i
  else ![1 / 2, 1 / 2, 0] i

theorem isRateMatrix_witnessRateTwo (k N : ℕ) :
    IsRateMatrix (fun j : Fin N => witnessRateTwo k (j : ℕ)) where
  nonneg j i := by
    simp only [witnessRateTwo]
    split_ifs <;> fin_cases i <;> simp
  conservation j := by
    rw [Fin.sum_univ_three]
    simp only [witnessRateTwo]
    split_ifs <;> norm_num [Matrix.cons_val_two, Matrix.tail_cons, Matrix.head_cons]

/-- Allocation of modes `0` and `1` up to the node `L = k + 1`. -/
private theorem witnessTwo_sum_node (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    ∑ j ∈ Finset.range (k + 1), witnessRateTwo k j i = 1 / 4 := by
  rw [Finset.sum_range_succ,
    sum_range_of_const (fun j => witnessRateTwo k j i) (![0, 0, 1] i)
      (fun j hj => by simp only [witnessRateTwo]; rw [if_pos hj])]
  rcases hi with rfl | rfl <;> norm_num [witnessRateTwo]

/-- Terminal masses of modes `0` and `1`. -/
private theorem witnessTwo_sum_top (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    ∑ j ∈ Finset.range (3 * k + 2), witnessRateTwo k j i = (k : ℝ) + 3 / 4 := by
  have h1 : ∑ j ∈ Finset.Ico (k + 1) (2 * k + 1), witnessRateTwo k j i
      = (k : ℝ) * ![1, 0, 0] i :=
    sum_Ico_of_const _ _ k (by omega) fun j hj1 hj2 => by
      simp only [witnessRateTwo]
      rw [if_neg (by omega), if_neg (by omega), if_pos hj2]
  have h2 : ∑ j ∈ Finset.Ico (2 * k + 1) (3 * k + 1), witnessRateTwo k j i
      = (k : ℝ) * ![0, 1, 0] i :=
    sum_Ico_of_const _ _ k (by omega) fun j hj1 hj2 => by
      simp only [witnessRateTwo]
      rw [if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos hj2]
  have h3 : ∑ j ∈ Finset.Ico (3 * k + 1) (3 * k + 2), witnessRateTwo k j i
      = ((1 : ℕ) : ℝ) * ![1 / 2, 1 / 2, 0] i :=
    sum_Ico_of_const _ _ 1 (by omega) fun j hj1 _ => by
      simp only [witnessRateTwo]
      rw [if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega)]
  rw [sum_range_split (fun j => witnessRateTwo k j i) (a := k + 1) (b := 2 * k + 1)
      (c := 3 * k + 1) (by omega) (by omega) (by omega),
    witnessTwo_sum_node k hi, h1, h2, h3]
  rcases hi with rfl | rfl <;> norm_num <;> ring

/-- The `N = 3k+2` witness input. -/
noncomputable def witnessTwoInput (k : ℕ) : Fin 3 → ℝ → ℝ :=
  gridCumulative (unitGrid (3 * k + 2)) fun j : Fin (3 * k + 2) => witnessRateTwo k (j : ℕ)

theorem isGridConstant_witnessTwoInput (k : ℕ) :
    IsGridConstant (unitGrid (3 * k + 2)) (witnessTwoInput k) :=
  ⟨_, isRateMatrix_witnessRateTwo k _, rfl⟩

theorem isCumulative_witnessTwoInput (k : ℕ) :
    IsCumulative (witnessTwoInput k) ((3 * k + 2 : ℕ) : ℝ) :=
  gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes
    (isRateMatrix_witnessRateTwo k _)

/-- Both selected modes of the `N = 3k+2` witness have terminal mass `E = k + 3/4`. -/
theorem witnessTwoInput_top (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    witnessTwoInput k i ((3 * k + 2 : ℕ) : ℝ) = (k : ℝ) + 3 / 4 := by
  rw [witnessTwoInput, gridCumulative_unitGrid_nat _ _ (le_refl (3 * k + 2)),
    witnessTwo_sum_top k hi]

/-- Both selected modes of the `N = 3k+2` witness have allocation `1/4 = L - E` at the node
`L = k + 1`. -/
theorem witnessTwoInput_node (k : ℕ) {i : Fin 3} (hi : i = 0 ∨ i = 1) :
    witnessTwoInput k i ((k + 1 : ℕ) : ℝ) = 1 / 4 := by
  rw [witnessTwoInput, gridCumulative_unitGrid_nat _ _ (by omega : k + 1 ≤ 3 * k + 2),
    witnessTwo_sum_node k hi]

/-! ## SC21 for the residue `N = 3k+2` -/

/-- The six inequalities `eq:residue-inequalities` for `N = 3k+2`, `E = k + 3/4`,
`L = k + 1`, `κ = k`, verified by direct substitution. Here `k = 0` is allowed. -/
theorem residue_inequalities_mod_two (k : ℕ) :
    ((3 * k + 2 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 3 / 4) ∧
      ((3 * k + 2 : ℕ) : ℝ) - ((k + 1 : ℕ) : ℝ) ≤ 2 * ((k : ℝ) + 3 / 4) ∧
      ((3 * k + 2 : ℕ) : ℝ) + ((k + 1 : ℕ) : ℝ) ≤ 4 * ((k : ℝ) + 3 / 4) ∧
      2 * ((3 * k + 2 : ℕ) : ℝ) ≤ 3 * (((k : ℝ) + 3 / 4) + ((k + 1 : ℕ) : ℝ)) ∧
      2 * ((k + 1 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 3 / 4) ∧
      2 * ((3 * k + 2 : ℕ) : ℝ) ≤ 3 * ((k : ℝ) + 3 / 4) + (k : ℝ) + 2 * ((k + 1 : ℕ) : ℝ) := by
  have hk' : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · push_cast
      linarith

/-- SC21, `eq:three-unit-one` for `N = 3k+2`, including `k = 0`, where the two pure blocks of
the witness are empty: the value is `k + 3/4`. -/
theorem gridF_unit_three_mod_two (k : ℕ) :
    gridF (unitGrid (3 * k + 2)) 3 1 ((3 * k + 2 : ℕ) : ℝ) = (k : ℝ) + 3 / 4 := by
  obtain ⟨d1, d2, d3, d4, d5, d6⟩ := residue_inequalities_mod_two k
  refine le_antisymm (gridF_le_of_forall (by positivity) fun A hA => ?_) ?_
  · obtain ⟨r, hr, rfl⟩ := hA
    exact gridOPT_unit_le_of_residue
      (gridCumulative_isCumulative (isGrid_unitGrid _).orderedTimes hr)
      (kn := k) (Ln := k + 1) (by omega) (by omega) d1 d2 d3 d4 d5 d6 (by linarith)
  · refine le_trans ?_ (gridOPT_le_gridF (by norm_num) (isGrid_unitGrid _)
      (isGridConstant_witnessTwoInput k) 1)
    refine le_gridOPT_unit_of_witness (isCumulative_witnessTwoInput k) (Ln := k + 1)
      (witnessTwoInput_top k (Or.inl rfl)) (witnessTwoInput_top k (Or.inr rfl)) ?_ ?_ ?_
    · rw [witnessTwoInput_node k (Or.inl rfl)]
      push_cast
      ring
    · rw [witnessTwoInput_node k (Or.inr rfl)]
      push_cast
      ring
    · push_cast
      linarith

/-! ## The residue formula and the closing observation -/

/-- SC21, `eq:three-unit-one` collected in one statement. The residue `1` needs `k ≥ 1`; the
excluded case `N = 1` is `gridF_unit_three_one`. -/
theorem gridF_unit_three_cases (N k : ℕ) :
    (N = 3 * k → gridF (unitGrid N) 3 1 (N : ℝ) = (k : ℝ)) ∧
      (N = 3 * k + 1 → 1 ≤ k → gridF (unitGrid N) 3 1 (N : ℝ) = (k : ℝ) + 1 / 2) ∧
      (N = 3 * k + 2 → gridF (unitGrid N) 3 1 (N : ℝ) = (k : ℝ) + 3 / 4) :=
  ⟨by rintro rfl; exact gridF_unit_three_mod_zero k,
    by rintro rfl hk; exact gridF_unit_three_mod_one hk,
    by rintro rfl; exact gridF_unit_three_mod_two k⟩

/-- The closing observation after `cor:three-unit-one`: the corrections to `N/3` are `0`,
`1/6` and `1/12` for the three residues. -/
theorem gridF_unit_three_correction {k : ℕ} (hk : 1 ≤ k) :
    gridF (unitGrid (3 * k)) 3 1 ((3 * k : ℕ) : ℝ) - ((3 * k : ℕ) : ℝ) / 3 = 0 ∧
      gridF (unitGrid (3 * k + 1)) 3 1 ((3 * k + 1 : ℕ) : ℝ)
        - ((3 * k + 1 : ℕ) : ℝ) / 3 = 1 / 6 ∧
      gridF (unitGrid (3 * k + 2)) 3 1 ((3 * k + 2 : ℕ) : ℝ)
        - ((3 * k + 2 : ℕ) : ℝ) / 3 = 1 / 12 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [gridF_unit_three_mod_zero k]
    push_cast
    ring
  · rw [gridF_unit_three_mod_one hk]
    push_cast
    ring
  · rw [gridF_unit_three_mod_two k]
    push_cast
    ring

/-- The three corrections are pairwise distinct, so they are **not** a fixed half-cell
correction: no single constant `c` satisfies `F^unit_{3,1}(N) = N/3 + c` for all `N ≥ 2`. -/
theorem gridF_unit_three_correction_not_constant :
    ¬ ∃ c : ℝ, (0 : ℝ) = c ∧ (1 / 6 : ℝ) = c ∧ (1 / 12 : ℝ) = c := by
  rintro ⟨c, rfl, h, -⟩
  norm_num at h

end GridSwitching
