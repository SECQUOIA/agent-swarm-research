import Formal.GridSwitching.ThreeMode
import Formal.GridSwitching.Elimination

/-!
# SC22 and SC23: the two numeric guard examples of the arbitrary-grid section

This module discharges the obligations SC22 and SC23 of
`topics/17-grid-switching/CLAIMS.md`. Both are concrete numeric instances that guard
`thm:finite-one` of `paper-switching-control/sections/08-finite-grid-one-switch.tex`: the
first shows that neither of the two families of inputs one might guess to be extremal is
extremal, the second shows that the upper-bound formula `U_ab` cannot be truncated.

## SC22: `ex:five-nine`

`gridF_unit_five_nine`: `F^unit_{5,1}(9) = 17/5`.

* `fiveNineRate`, `fiveNineInput`: the extremizer of the source, verbatim — on `[0, 4]`
  mode `1` runs at `2/5` and each of modes `2, …, 5` at `3/20`, on `[4, 5]` mode `1` runs at
  `0` and each of the others at `1/4`, on `[5, 9]` mode `1` runs at `1/4` and each of the
  others at `3/16`. Its terminal masses are `(13/5, 8/5, 8/5, 8/5, 8/5)`
  (`fiveNineInput_mass_zero`, `fiveNineInput_mass_ne`).
* `le_gridOPT_fiveNine`: the lower bound. Every `p → 1` with `p ≠ 1` has final deficit at
  least `17/5` at every grid node `τ ≤ 3` and initial deficit at least `4 - 3/5 = 17/5` at
  every grid node `τ ≥ 4`; for `1 → 2` the cutoff sits between `4` and `5`, with final
  deficit `17/5` at `4` and initial deficit `5 - 8/5 = 17/5` at `5`. Dominance is already
  built into `le_gridOPT_one`, which reduces every two-block grid schedule to a one-switch
  schedule between two distinct modes at a grid node.
* `gridOPT_unit9_five_le`: the source's short independent upper bound, valid for **every**
  cumulative input, not only the grid-constant ones. Sort the masses; if `m_1 ≥ 13/5`, use
  `2 → 1` at time `3`; otherwise `m_2 ≥ (9 - m_1)/4 > 8/5`, and at time `4` one starts in a
  mode with `A_p(4) ≥ 4/5` and finishes in a largest-mass mode `q ≠ p`.
* `gridOPT_uniformFive`, `gridF_unit_three_nine`, `gridF_unit_five_nine_exceeds`: the two
  comparisons that are the point of the example. The uniform five-mode input on this grid
  has one-switch optimum exactly `16/5`, the three-mode worst case on the same grid is
  exactly `3` (SC21 at `N = 3 · 3`), and both are strictly below `17/5`. So neither the
  uniform inputs nor the three-mode worst cases exhaust the five-mode adversary.

## SC23: the nonuniform admissibility witness

For `n = 9` and the five-cell grid `(0, 19/2, 61/6, 265/24, 481/24, 2669/120)` with
`T = 2669/120`:

* `nonuniform_exact_max`: the exact first-family maximum `max U_ab` over admissible pairs is
  `2593/270`, attained at `(a, b) = (3, 3)`.
* `nonuniform_trunc_max`: the truncated formula that retains only the two upper bounds
  `((n-2)A + B)/n` and `((n-1)T - P - (n-1)Q)/n` of `U` has maximum `2077/216`, attained at
  `(a, b) = (1, 4)`.
* `pairU_le_pairUtrunc`: truncation is a genuine relaxation at every pair, so any strict
  increase is caused by a discarded condition.
* `pairU_zero_three`, `nonuniform_binding_discarded_term`: at the pair `(1, 4)` the minimum
  defining `U_ab` is attained at the discarded leading term `A = t_1 = 19/2`, and that value is
  strictly below the truncated bound, so the discarded condition `U ≤ A` is the binding one.
* `nonuniform_truncation_not_redundant`: since `2593/270 < 2077/216`, the discarded
  conditions of `U` are **not** redundant — dropping them strictly increases the value of the
  formula, already at the single pair `(1, 4)`, where the discarded term `A = t_1 = 19/2`
  is the binding one.

Both numbers of the source were recomputed from the definitions before being stated, and
both are correct.

## Conventions

Pairs `(a, b)` with `1 ≤ a ≤ b ≤ N` are indexed here by `a b : Fin 5` standing for the
source's `a - 1`, `b - 1`, so that `A = t_{a+1}`, `P = t_a` in the Lean indexing. The grid
itself is a function of a natural index, with the horizon repeated beyond the last node; only
the indices `0, …, 5` are ever used.

Nothing in this module uses the general formula `thm:finite-one`; SC22 is proved directly
from the one-switch error formula through `le_gridOPT_one` and `gridOPT_one_le_max` of
`Formal.GridSwitching.ThreeMode`, and SC23 is a statement about the closed-form data `L`,
`U` and `Admissible` of `Formal.GridSwitching.Elimination` alone.
-/

namespace GridSwitching.Examples

open Set

/-! ## The unit grid with nine cells -/

/-- The unit grid on nine cells, with the horizon written as the numeral `9 : ℝ`. -/
theorem isGrid_unit9 : IsGrid (unitGrid 9) (9 : ℝ) := by
  simpa using isGrid_unitGrid 9

/-- Every node of the nine-cell unit grid is a natural number at most `9`. -/
private theorem node_le (m : Fin 10) : (m : ℕ) ≤ 9 := Nat.lt_succ_iff.mp m.isLt

/-- Three distinct modes never jointly occupy more than the elapsed time. -/
private theorem triple_le {n : ℕ} {A : Fin n → ℝ → ℝ} {T : ℝ} (hA : IsCumulative A T)
    {a b c : Fin n} (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) {t : ℝ}
    (ht : t ∈ Icc (0 : ℝ) T) : A a t + A b t + A c t ≤ t := by
  have hsum : ∑ i ∈ ({a, b, c} : Finset (Fin n)), A i t ≤ ∑ i, A i t :=
    Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun i _ _ => hA.nonneg i ht
  rw [hA.conservation t ht] at hsum
  rwa [Finset.sum_insert (by simp [hab, hac]), Finset.sum_insert (by simp [hbc]),
    Finset.sum_singleton, ← add_assoc] at hsum

/-- One competing pair at one node of the nine-cell unit grid bounds the five-mode one-switch
optimum, once the three terms of `eq:one-switch-error` are bounded. -/
private theorem gridOPT_unit9_le_of_candidate {A : Fin 5 → ℝ → ℝ} (hA : IsCumulative A (9 : ℝ))
    {p q : Fin 5} (hpq : p ≠ q) {j : ℕ} (hj : j ≤ 9) {E : ℝ} (hE : 0 ≤ E)
    (h1 : ∀ i : Fin 5, i ≠ p → i ≠ q → A i 9 ≤ E)
    (h2 : (j : ℝ) - A p (j : ℝ) ≤ E)
    (h3 : 9 - A q 9 - (j : ℝ) ≤ E) :
    gridOPT (unitGrid 9) A (9 : ℝ) 1 ≤ E := by
  have hm : unitGrid 9 ⟨j, Nat.lt_succ_of_le hj⟩ = (j : ℝ) := rfl
  refine (gridOPT_one_le_max (by norm_num) isGrid_unit9 hA hpq
    ⟨j, Nat.lt_succ_of_le hj⟩).trans ?_
  rw [hm]
  exact max_le (omittedMass_le hE h1) (max_le h2 h3)

/-! ## SC22, upper bound

The short independent argument of `ex:five-nine`. It uses no grid constancy: it holds for
every cumulative input on the nine-cell unit grid. -/

/-- SC22, upper bound: every cumulative five-mode input on the nine-cell unit grid admits a
one-switch grid schedule of error at most `17/5`.

Sort the terminal masses. If the largest is at least `13/5`, the order "second largest, then
largest" switching at time `3` has initial deficit at most `3`, omitted masses at most `3`,
and final deficit `6 - m_1 ≤ 17/5`. Otherwise the second largest exceeds `8/5`, and at time
`4` one starts in a mode with `A_p(4) ≥ 4/5` and finishes in a largest-mass mode `q ≠ p`:
the initial deficit is at most `16/5`, the final deficit is below `17/5`, and the omitted
masses are below `13/5`. -/
theorem gridOPT_unit9_five_le {A : Fin 5 → ℝ → ℝ} (hA : IsCumulative A (9 : ℝ)) :
    gridOPT (unitGrid 9) A (9 : ℝ) 1 ≤ 17 / 5 := by
  have hmem9 : (9 : ℝ) ∈ Icc (0 : ℝ) 9 := ⟨by norm_num, le_rfl⟩
  have hmem4 : (4 : ℝ) ∈ Icc (0 : ℝ) 9 := ⟨by norm_num, by norm_num⟩
  have hmem3 : (3 : ℝ) ∈ Icc (0 : ℝ) 9 := ⟨by norm_num, by norm_num⟩
  have hsum9 : ∑ i, A i 9 = 9 := hA.conservation 9 hmem9
  have hsum4 : ∑ i, A i 4 = 4 := hA.conservation 4 hmem4
  obtain ⟨h1, hh1⟩ := Finite.exists_max fun i : Fin 5 => A i 9
  have hne : (Finset.univ.erase h1).Nonempty := by
    rw [← Finset.card_pos, Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ,
      Fintype.card_fin]
    norm_num
  obtain ⟨h2, hh2mem, hh2⟩ :=
    Finset.exists_max_image (Finset.univ.erase h1) (fun i : Fin 5 => A i 9) hne
  have hh21 : h2 ≠ h1 := (Finset.mem_erase.mp hh2mem).1
  have hmax9 : (9 : ℝ) ≤ 5 * A h1 9 := by
    have h := Finset.sum_le_card_nsmul Finset.univ (fun i : Fin 5 => A i 9) (A h1 9)
      fun i _ => hh1 i
    simpa [hsum9, Finset.card_univ, nsmul_eq_mul] using h
  have hsum_erase : ∑ i ∈ Finset.univ.erase h1, A i 9 = 9 - A h1 9 := by
    have h := Finset.sum_erase_add Finset.univ (fun i : Fin 5 => A i 9) (Finset.mem_univ h1)
    simp only [hsum9] at h
    linarith
  have h2bound : 9 - A h1 9 ≤ 4 * A h2 9 := by
    have h := Finset.sum_le_card_nsmul (Finset.univ.erase h1) (fun i : Fin 5 => A i 9)
      (A h2 9) fun i hi => hh2 i hi
    rw [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, Fintype.card_fin] at h
    simp only [nsmul_eq_mul] at h
    rw [hsum_erase] at h
    norm_num at h
    linarith
  rcases le_or_gt (13 / 5 : ℝ) (A h1 9) with hcase | hcase
  · -- The largest mass is at least `13/5`: use "second largest, then largest" at time `3`.
    refine gridOPT_unit9_le_of_candidate hA hh21 (j := 3) (by norm_num) (by norm_num)
      ?_ ?_ ?_
    · intro i hi2 hi1
      have ht := triple_le hA (Ne.symm hh21) (Ne.symm hi1) (Ne.symm hi2) hmem9
      have hle1 : A i 9 ≤ A h1 9 := hh1 i
      have hle2 : A i 9 ≤ A h2 9 :=
        hh2 i (Finset.mem_erase.mpr ⟨hi1, Finset.mem_univ i⟩)
      linarith
    · have h0 : 0 ≤ A h2 3 := hA.nonneg h2 hmem3
      push_cast
      linarith
    · push_cast
      linarith
  · -- The largest mass is below `13/5`: switch at time `4`.
    obtain ⟨p, hp⟩ := Finite.exists_max fun i : Fin 5 => A i 4
    have hp45 : (4 : ℝ) / 5 ≤ A p 4 := by
      have h := Finset.sum_le_card_nsmul Finset.univ (fun i : Fin 5 => A i 4) (A p 4)
        fun i _ => hp i
      simp only [Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at h
      rw [hsum4] at h
      norm_num at h
      linarith
    by_cases hph : p = h1
    · -- The busiest mode at time `4` is the largest-mass mode: finish in the second largest.
      have hp4 : (4 : ℝ) / 5 ≤ A h1 4 := hph ▸ hp45
      refine gridOPT_unit9_le_of_candidate hA (Ne.symm hh21) (j := 4) (by norm_num)
        (by norm_num) ?_ ?_ ?_
      · intro i hi1 _
        have := hh1 i
        linarith
      · push_cast
        linarith
      · push_cast
        linarith
    · -- Otherwise finish in the largest-mass mode.
      refine gridOPT_unit9_le_of_candidate hA hph (j := 4) (by norm_num) (by norm_num)
        ?_ ?_ ?_
      · intro i _ _
        have := hh1 i
        linarith
      · push_cast
        linarith
      · push_cast
        linarith

/-! ## SC22, the extremizer of `ex:five-nine` -/

/-- The rate of mode `1` in the extremizer of `ex:five-nine`: `2/5` on `[0, 4]`, `0` on
`[4, 5]` and `1/4` on `[5, 9]`. -/
noncomputable def fiveNineRateBig (j : ℕ) : ℝ :=
  if j < 4 then 2 / 5 else if j = 4 then 0 else 1 / 4

/-- The common rate of each of modes `2, …, 5` in the extremizer of `ex:five-nine`: `3/20` on
`[0, 4]`, `1/4` on `[4, 5]` and `3/16` on `[5, 9]`. -/
noncomputable def fiveNineRateSmall (j : ℕ) : ℝ :=
  if j < 4 then 3 / 20 else if j = 4 then 1 / 4 else 3 / 16

/-- The rate matrix of the extremizer of `ex:five-nine`, as a function of the natural cell
index. -/
noncomputable def fiveNineRate (j : ℕ) (i : Fin 5) : ℝ :=
  if i = 0 then fiveNineRateBig j else fiveNineRateSmall j

theorem isRateMatrix_fiveNine :
    IsRateMatrix fun (j : Fin 9) (i : Fin 5) => fiveNineRate (j : ℕ) i where
  nonneg j i := by
    simp only [fiveNineRate, fiveNineRateBig, fiveNineRateSmall]
    split_ifs <;> norm_num
  conservation j := by
    have hsum : ∀ c d : ℝ, (∑ i : Fin 5, if i = 0 then c else d) = c + 4 * d := by
      intro c d
      have e0 : (if (0 : Fin 5) = 0 then c else d) = c := if_pos rfl
      have e1 : (if (1 : Fin 5) = 0 then c else d) = d := if_neg (by decide)
      have e2 : (if (2 : Fin 5) = 0 then c else d) = d := if_neg (by decide)
      have e3 : (if (3 : Fin 5) = 0 then c else d) = d := if_neg (by decide)
      have e4 : (if (4 : Fin 5) = 0 then c else d) = d := if_neg (by decide)
      rw [Fin.sum_univ_five, e0, e1, e2, e3, e4]
      ring
    simp only [fiveNineRate, hsum, fiveNineRateBig, fiveNineRateSmall]
    split_ifs <;> norm_num

/-- The extremizer of `ex:five-nine`. -/
noncomputable def fiveNineInput : Fin 5 → ℝ → ℝ :=
  gridCumulative (unitGrid 9) fun (j : Fin 9) (i : Fin 5) => fiveNineRate (j : ℕ) i

theorem isGridConstant_fiveNineInput : IsGridConstant (unitGrid 9) fiveNineInput :=
  ⟨_, isRateMatrix_fiveNine, rfl⟩

theorem isCumulative_fiveNineInput : IsCumulative fiveNineInput (9 : ℝ) :=
  gridCumulative_isCumulative isGrid_unit9.orderedTimes isRateMatrix_fiveNine

/-- The cumulative allocation of the extremizer at an integer time is the partial sum of the
cell rates. -/
theorem fiveNineInput_node {M : ℕ} (hM : M ≤ 9) (i : Fin 5) :
    fiveNineInput i (M : ℝ) = ∑ j ∈ Finset.range M, fiveNineRate j i :=
  gridCumulative_unitGrid_nat fiveNineRate i hM

theorem fiveNineInput_zero_five : fiveNineInput 0 (5 : ℝ) = 8 / 5 := by
  have h := fiveNineInput_node (M := 5) (by norm_num) 0
  rw [show ((5 : ℕ) : ℝ) = (5 : ℝ) by norm_num] at h
  rw [h]
  norm_num [Finset.sum_range_succ, fiveNineRate, fiveNineRateBig]

theorem fiveNineInput_four_of_ne {i : Fin 5} (hi : i ≠ 0) : fiveNineInput i (4 : ℝ) = 3 / 5 := by
  have h := fiveNineInput_node (M := 4) (by norm_num) i
  rw [show ((4 : ℕ) : ℝ) = (4 : ℝ) by norm_num] at h
  rw [h]
  norm_num [Finset.sum_range_succ, fiveNineRate, fiveNineRateSmall, hi]

/-- The terminal mass of mode `1` is `13/5`. -/
theorem fiveNineInput_mass_zero : fiveNineInput 0 (9 : ℝ) = 13 / 5 := by
  have h := fiveNineInput_node (M := 9) (by norm_num) 0
  rw [show ((9 : ℕ) : ℝ) = (9 : ℝ) by norm_num] at h
  rw [h]
  norm_num [Finset.sum_range_succ, fiveNineRate, fiveNineRateBig]

/-- Each of the terminal masses of modes `2, …, 5` is `8/5`. -/
theorem fiveNineInput_mass_ne {i : Fin 5} (hi : i ≠ 0) : fiveNineInput i (9 : ℝ) = 8 / 5 := by
  have h := fiveNineInput_node (M := 9) (by norm_num) i
  rw [show ((9 : ℕ) : ℝ) = (9 : ℝ) by norm_num] at h
  rw [h]
  norm_num [Finset.sum_range_succ, fiveNineRate, fiveNineRateSmall, hi]

/-! ## SC22, lower bound -/

/-- SC22, lower bound: against the extremizer of `ex:five-nine` every two-block grid schedule
has error at least `17/5`.

Every `p → 1` with `p ≠ 1` has final deficit `32/5 - τ ≥ 17/5` at the grid nodes `τ ≤ 3` and
initial deficit at least `4 - 3/5 = 17/5` at the grid nodes `τ ≥ 4`. For a final mode other
than `1` the final deficit is `37/5 - τ ≥ 17/5` at the nodes `τ ≤ 4`, while at the nodes
`τ ≥ 5` the initial deficit is at least `5 - 8/5 = 17/5` when the initial mode is `1` and at
least `17/5` otherwise. -/
theorem le_gridOPT_fiveNine :
    (17 / 5 : ℝ) ≤ gridOPT (unitGrid 9) fiveNineInput (9 : ℝ) 1 := by
  refine le_gridOPT_one (by norm_num) isGrid_unit9 isCumulative_fiveNineInput ?_
  intro p q m hpq
  have hnode : unitGrid 9 m = ((m : ℕ) : ℝ) := rfl
  have hm9 : ((m : ℕ) : ℝ) ≤ 9 := by exact_mod_cast node_le m
  have hm0 : (0 : ℝ) ≤ ((m : ℕ) : ℝ) := Nat.cast_nonneg _
  rw [hnode]
  -- the initial deficit of a mode other than `1` at every node `τ ≥ 4`
  have hbig : ∀ r : Fin 5, r ≠ 0 → 4 ≤ (m : ℕ) →
      (17 / 5 : ℝ) ≤ initialDeficit fiveNineInput r ((m : ℕ) : ℝ) := by
    intro r hr h4
    have h4' : (4 : ℝ) ≤ ((m : ℕ) : ℝ) := by exact_mod_cast h4
    have hmono := initialDeficit_mono isCumulative_fiveNineInput r
      (by norm_num : (0 : ℝ) ≤ 4) h4' hm9
    have hval : initialDeficit fiveNineInput r (4 : ℝ) = 17 / 5 := by
      simp only [initialDeficit, fiveNineInput_four_of_ne hr]
      norm_num
    linarith [hval ▸ hmono]
  by_cases hq : q = 0
  · subst hq
    rcases le_or_gt (m : ℕ) 3 with h | h
    · refine le_max_of_le_right (le_max_of_le_right ?_)
      have h3 : ((m : ℕ) : ℝ) ≤ 3 := by exact_mod_cast h
      simp only [finalDeficit, masses, fiveNineInput_mass_zero]
      linarith
    · exact le_max_of_le_right (le_max_of_le_left (hbig p hpq (by omega)))
  · rcases le_or_gt (m : ℕ) 4 with h | h
    · refine le_max_of_le_right (le_max_of_le_right ?_)
      have h4 : ((m : ℕ) : ℝ) ≤ 4 := by exact_mod_cast h
      simp only [finalDeficit, masses, fiveNineInput_mass_ne hq]
      linarith
    · refine le_max_of_le_right (le_max_of_le_left ?_)
      by_cases hp : p = 0
      · subst hp
        have h5 : (5 : ℝ) ≤ ((m : ℕ) : ℝ) := by
          have : 5 ≤ (m : ℕ) := by omega
          exact_mod_cast this
        have hmono := initialDeficit_mono isCumulative_fiveNineInput 0
          (by norm_num : (0 : ℝ) ≤ 5) h5 hm9
        have hval : initialDeficit fiveNineInput 0 (5 : ℝ) = 17 / 5 := by
          simp only [initialDeficit, fiveNineInput_zero_five]
          norm_num
        linarith [hval ▸ hmono]
      · exact hbig p hp (by omega)

/-! ## SC22, the value -/

/-- **SC22**, `ex:five-nine`: the five-mode one-switch minimax value on the nine-cell unit
grid is `17/5`. -/
theorem gridF_unit_five_nine : gridF (unitGrid 9) 5 1 (9 : ℝ) = 17 / 5 := by
  refine le_antisymm (gridF_le_of_forall (by norm_num) fun A hA => ?_) ?_
  · obtain ⟨r, hr, rfl⟩ := hA
    exact gridOPT_unit9_five_le
      (gridCumulative_isCumulative isGrid_unit9.orderedTimes hr)
  · exact le_gridOPT_fiveNine.trans
      (gridOPT_le_gridF (by norm_num) isGrid_unit9 isGridConstant_fiveNineInput 1)

/-! ## SC22, the two comparisons

The point of `ex:five-nine` is that the value `17/5` exceeds both quantities that a proposed
reduction to two families of inputs would predict: the value `16/5` of the uniform
five-mode input on the same grid, and the three-mode worst case `3` on the same grid. -/

/-- The uniform five-mode rate matrix on the nine-cell unit grid. -/
noncomputable def uniformFiveRate : Fin 9 → Fin 5 → ℝ := fun _ _ => 1 / 5

theorem isRateMatrix_uniformFive : IsRateMatrix uniformFiveRate where
  nonneg _ _ := by norm_num [uniformFiveRate]
  conservation _ := by norm_num [uniformFiveRate, Fin.sum_univ_five]

/-- The uniform five-mode input on the nine-cell unit grid. -/
noncomputable def uniformFiveInput : Fin 5 → ℝ → ℝ :=
  gridCumulative (unitGrid 9) uniformFiveRate

theorem isGridConstant_uniformFiveInput : IsGridConstant (unitGrid 9) uniformFiveInput :=
  ⟨_, isRateMatrix_uniformFive, rfl⟩

theorem isCumulative_uniformFiveInput : IsCumulative uniformFiveInput (9 : ℝ) :=
  gridCumulative_isCumulative isGrid_unit9.orderedTimes isRateMatrix_uniformFive

theorem uniformFiveInput_node {M : ℕ} (hM : M ≤ 9) (i : Fin 5) :
    uniformFiveInput i (M : ℝ) = (M : ℝ) / 5 := by
  have h := gridCumulative_unitGrid_nat (fun (_ : ℕ) (_ : Fin 5) => (1 : ℝ) / 5) i hM
  rw [show uniformFiveInput i (M : ℝ) =
      gridCumulative (unitGrid 9) (fun (j : Fin 9) => (fun (_ : ℕ) (_ : Fin 5) =>
        (1 : ℝ) / 5) (j : ℕ)) i (M : ℝ) from rfl, h]
  rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
  ring

/-- Each mode of the uniform five-mode input has accumulated a fifth of the elapsed time at
every grid node. -/
theorem uniformFiveInput_at (m : Fin 10) (i : Fin 5) :
    uniformFiveInput i ((m : ℕ) : ℝ) = ((m : ℕ) : ℝ) / 5 :=
  uniformFiveInput_node (node_le m) i

theorem uniformFiveInput_mass (i : Fin 5) : uniformFiveInput i (9 : ℝ) = 9 / 5 := by
  have h := uniformFiveInput_node (M := 9) (by norm_num) i
  rwa [show ((9 : ℕ) : ℝ) = (9 : ℝ) by norm_num] at h

theorem uniformFiveInput_four (i : Fin 5) : uniformFiveInput i (4 : ℝ) = 4 / 5 := by
  have h := uniformFiveInput_node (M := 4) (by norm_num) i
  rwa [show ((4 : ℕ) : ℝ) = (4 : ℝ) by norm_num] at h

/-- The uniform five-mode input on the nine-cell unit grid has one-switch grid optimum
exactly `16/5`: switching at time `4` balances the initial deficit `4 - 4/5` against the
final deficit `9 - 9/5 - 4`, and no node does better. -/
theorem gridOPT_uniformFive :
    gridOPT (unitGrid 9) uniformFiveInput (9 : ℝ) 1 = 16 / 5 := by
  refine le_antisymm ?_ ?_
  · refine gridOPT_unit9_le_of_candidate isCumulative_uniformFiveInput
      (p := 0) (q := 1) (by decide) (j := 4) (by norm_num) (by norm_num) ?_ ?_ ?_
    · intro i _ _
      rw [uniformFiveInput_mass i]
      norm_num
    · rw [show ((4 : ℕ) : ℝ) = (4 : ℝ) by norm_num, uniformFiveInput_four]
      norm_num
    · rw [show ((4 : ℕ) : ℝ) = (4 : ℝ) by norm_num, uniformFiveInput_mass]
      norm_num
  · refine le_gridOPT_one (by norm_num) isGrid_unit9 isCumulative_uniformFiveInput ?_
    intro p q m _
    have hnode : unitGrid 9 m = ((m : ℕ) : ℝ) := rfl
    rw [hnode]
    rcases le_or_gt (m : ℕ) 4 with h | h
    · refine le_max_of_le_right (le_max_of_le_right ?_)
      have h4 : ((m : ℕ) : ℝ) ≤ 4 := by exact_mod_cast h
      simp only [finalDeficit, masses, uniformFiveInput_mass]
      linarith
    · refine le_max_of_le_right (le_max_of_le_left ?_)
      have h5 : (5 : ℝ) ≤ ((m : ℕ) : ℝ) := by
        have : 5 ≤ (m : ℕ) := by omega
        exact_mod_cast this
      simp only [initialDeficit, uniformFiveInput_at m p]
      linarith

/-- SC21 at `N = 3 · 3`: the three-mode worst case on the nine-cell unit grid is `3`. -/
theorem gridF_unit_three_nine : gridF (unitGrid 9) 3 1 (9 : ℝ) = 3 := by
  have h := gridF_unit_three_mod_zero 3
  norm_num at h
  exact h

/-- **SC22**, the point of `ex:five-nine`: the value `17/5` strictly exceeds both the value
`16/5` of the uniform five-mode input on the same grid and the three-mode worst case `3` on
the same grid. Neither of those two families of inputs is worst, so the proposed reduction to
them fails. -/
theorem gridF_unit_five_nine_exceeds :
    gridOPT (unitGrid 9) uniformFiveInput (9 : ℝ) 1 < gridF (unitGrid 9) 5 1 (9 : ℝ) ∧
      gridF (unitGrid 9) 3 1 (9 : ℝ) < gridF (unitGrid 9) 5 1 (9 : ℝ) := by
  rw [gridF_unit_five_nine, gridOPT_uniformFive, gridF_unit_three_nine]
  norm_num

/-! ## SC23: the nonuniform admissibility witness

The grid `(0, 19/2, 61/6, 265/24, 481/24, 2669/120)` of the closing paragraph of Section 8,
with `n = 9` and `T = 2669/120`. -/

/-- The six-point nonuniform grid of the closing paragraph, as a function of the node index.
Only the indices `0, …, 5` are used; the value beyond the last node is the horizon. -/
noncomputable def nonuniformGrid : ℕ → ℝ := fun j =>
  if j = 0 then 0 else if j = 1 then 19 / 2 else if j = 2 then 61 / 6
  else if j = 3 then 265 / 24 else if j = 4 then 481 / 24 else 2669 / 120

/-- The horizon `T = t_5 = 2669/120`. -/
noncomputable def nonuniformHorizon : ℝ := 2669 / 120

theorem nonuniformHorizon_eq : nonuniformHorizon = nonuniformGrid 5 := by
  norm_num [nonuniformHorizon, nonuniformGrid]

/-- `A = t_{a+1}` for the pair index `a : Fin 5`, which stands for the source's `a - 1`. -/
noncomputable def pairA (a : Fin 5) : ℝ := nonuniformGrid ((a : ℕ) + 1)

/-- `P = t_a` for the pair index `a : Fin 5`. -/
noncomputable def pairP (a : Fin 5) : ℝ := nonuniformGrid (a : ℕ)

/-- `L_ab` of `eq:grid-L` on this grid. -/
noncomputable def pairL (a b : Fin 5) : ℝ :=
  L 9 nonuniformHorizon (pairA a) (pairA b)

/-- `U_ab` of `eq:grid-U` on this grid. -/
noncomputable def pairU (a b : Fin 5) : ℝ :=
  U 9 nonuniformHorizon (pairA a) (pairA b) (pairP a) (pairP b)

/-- The truncated upper bound: only the two terms `((n-2)A + B)/n` and
`((n-1)T - P - (n-1)Q)/n` of `U` are retained, all others discarded. -/
noncomputable def pairUtrunc (a b : Fin 5) : ℝ :=
  min (((9 - 2) * pairA a + pairA b) / 9)
    (((9 - 1) * nonuniformHorizon - pairP a - (9 - 1) * pairP b) / 9)

/-- Truncation is a genuine relaxation: discarding terms of the `min` can only raise the
bound, so `U_ab ≤ U^trunc_ab` at every pair. Any strict inequality below therefore comes from
a discarded condition, not from a change of formula. -/
theorem pairU_le_pairUtrunc (a b : Fin 5) : pairU a b ≤ pairUtrunc a b := by
  rw [pairU, pairUtrunc, U]
  exact le_min ((min_le_right _ _).trans (min_le_left _ _))
    ((min_le_right _ _).trans ((min_le_right _ _).trans
      ((min_le_right _ _).trans (min_le_left _ _))))

/-- Admissibility of `eq:grid-admissible` for the pair `(a, b)`. -/
def pairAdmissible (a b : Fin 5) : Prop :=
  a ≤ b ∧ Admissible 9 nonuniformHorizon (pairA a) (pairA b) ∧ pairL a b ≤ pairU a b

/-- Admissibility of `eq:grid-admissible` with the truncated upper bound in place of `U`. -/
def pairAdmissibleTrunc (a b : Fin 5) : Prop :=
  a ≤ b ∧ Admissible 9 nonuniformHorizon (pairA a) (pairA b) ∧ pairL a b ≤ pairUtrunc a b

/-- **SC23**, exact value: the first-family maximum `max U_ab` over admissible pairs of this
grid is exactly `2593/270`, attained at `(a, b) = (3, 3)` in the source's indexing. -/
theorem nonuniform_exact_max :
    pairAdmissible 2 2 ∧ pairU 2 2 = 2593 / 270 ∧
      ∀ a b : Fin 5, pairAdmissible a b → pairU a b ≤ 2593 / 270 := by
  refine ⟨?_, ?_, ?_⟩
  · refine ⟨le_rfl, ?_, ?_⟩ <;>
      norm_num [Admissible, pairL, pairU, pairA, pairP, nonuniformHorizon, nonuniformGrid,
        L, U, min_def, max_def]
  · norm_num [pairU, pairA, pairP, nonuniformHorizon, nonuniformGrid, U, min_def]
  · intro a b
    fin_cases a <;> fin_cases b <;>
      norm_num [pairAdmissible, Admissible, pairL, pairU, pairA, pairP, nonuniformHorizon,
        nonuniformGrid, L, U, min_def, max_def]

/-- **SC23**, truncated value: dropping every term of `U` except `((n-2)A + B)/n` and
`((n-1)T - P - (n-1)Q)/n` raises the first-family maximum to `2077/216`, attained at
`(a, b) = (1, 4)` in the source's indexing. -/
theorem nonuniform_trunc_max :
    pairAdmissibleTrunc 0 3 ∧ pairUtrunc 0 3 = 2077 / 216 ∧
      ∀ a b : Fin 5, pairAdmissibleTrunc a b → pairUtrunc a b ≤ 2077 / 216 := by
  refine ⟨?_, ?_, ?_⟩
  · refine ⟨by decide, ?_, ?_⟩ <;>
      norm_num [Admissible, pairL, pairUtrunc, pairA, pairP, nonuniformHorizon,
        nonuniformGrid, L, min_def, max_def]
  · norm_num [pairUtrunc, pairA, pairP, nonuniformHorizon, nonuniformGrid, min_def]
  · intro a b
    fin_cases a <;> fin_cases b <;>
      norm_num [pairAdmissibleTrunc, Admissible, pairL, pairUtrunc, pairA, pairP,
        nonuniformHorizon, nonuniformGrid, L, min_def, max_def] <;>
      try decide

/-- **SC23**, the point of the example: the conditions of `U` that the proposed
simplification discards are **not** redundant.

At the admissible pair `(a, b) = (1, 4)` the discarded term `A = t_1 = 19/2` is the binding
one, so the truncated bound strictly exceeds `U_ab` there; consequently the truncated maximum
`2077/216` strictly exceeds the exact first-family maximum `2593/270`, and the simplified
formula is not a valid substitute. -/
theorem nonuniform_truncation_not_redundant :
    pairAdmissible 0 3 ∧ pairU 0 3 < pairUtrunc 0 3 ∧ (2593 / 270 : ℝ) < 2077 / 216 := by
  refine ⟨⟨by decide, ?_, ?_⟩, ?_, by norm_num⟩ <;>
    norm_num [Admissible, pairL, pairU, pairUtrunc, pairA, pairP, nonuniformHorizon,
      nonuniformGrid, L, U, min_def, max_def]

/-- The discarded leading term of `U` at the pair `(a, b) = (1, 4)`: it is `A = t_1`, the
first node of the grid. -/
theorem pairA_zero : pairA 0 = 19 / 2 := by
  norm_num [pairA, nonuniformGrid]

/-- **SC23**, the value of `U` at the pair `(a, b) = (1, 4)`. -/
theorem pairU_zero_three : pairU 0 3 = 19 / 2 := by
  norm_num [pairU, pairA, pairP, nonuniformHorizon, nonuniformGrid, U, min_def, max_def]

/-- **SC23**, identification of the binding discarded term. At the admissible pair
`(a, b) = (1, 4)` the minimum defining `U_ab` is attained at its leading term `A = t_1 = 19/2`,
which is one of the terms the proposed simplification discards, and that value is strictly
below the truncated bound. So the strict increase recorded by
`nonuniform_truncation_not_redundant` is caused by the discarded condition `U ≤ A`. -/
theorem nonuniform_binding_discarded_term :
    pairU 0 3 = pairA 0 ∧ pairA 0 = 19 / 2 ∧ pairA 0 < pairUtrunc 0 3 := by
  refine ⟨?_, pairA_zero, ?_⟩ <;>
    norm_num [pairU, pairUtrunc, pairA, pairP, nonuniformHorizon, nonuniformGrid, U, min_def,
      max_def]

end GridSwitching.Examples
