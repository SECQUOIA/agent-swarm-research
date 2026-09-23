import Formal.NetworkSimplex.ThresholdOriginalObstruction

/-! Counts and balanced incidence data for the four-label counterexample. -/
namespace NetworkSimplex.Chain.ThresholdObstruction
open scoped BigOperators

/-- The observation pattern contains exactly the seven stated products. -/
theorem observation_count : Fintype.card Obs = 7 := by
  classical
  change Fintype.card {o : ChainArc 4 × Fin 4 // Selected classes (fun _ => False) o} = 7
  rw [Fintype.card_subtype]
  apply Nat.cast_injective (R := ℝ)
  rw [← Finset.sum_boole]
  simp only [Fintype.sum_prod_type, Fintype.sum_sum_type, Fintype.sum_bool,
    Fin.sum_univ_succ]
  simpa [Selected, classes, observesA, observesB, Matrix.cons_val, reduceCtorEq] using
    (show (1 : ℝ) + (1 + 1 + (1 + 1 + (1 + 1))) = 7 by norm_num)

theorem vertex_count : Fintype.card (Fin 5) = 5 := by decide

theorem arc_count : Fintype.card (ChainArc 4) = 9 := by decide

/-- The allowed-set incidence rows used in the paper. -/
def incidenceRows : Matrix (Fin 4) (Fin 4) ℝ :=
  ![![1, 1, 1, 0], ![1, 0, 0, 1], ![0, 1, 0, 1], ![0, 0, 1, 1]]

theorem incidence_kernel_zero (d : Fin 4 → ℝ)
    (h : incidenceRows.mulVec d = 0) : d = 0 := by
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  have h2 := congrFun h 2
  have h3 := congrFun h 3
  simp [incidenceRows, Matrix.mulVec, dotProduct, Fin.sum_univ_four] at h0 h1 h2 h3
  ext j
  fin_cases j <;> simp <;> linarith

/-- The displayed four-by-four matrix is invertible over the reals. -/
theorem incidence_invertible : IsUnit incidenceRows := by
  apply Matrix.mulVec_injective_iff_isUnit.mp
  intro x y hxy
  have h := incidence_kernel_zero (x - y) (by rw [Matrix.mulVec_sub, hxy, sub_self])
  exact sub_eq_zero.mp h

theorem incidence_balanced :
    incidenceRows.transpose.mulVec ![2, 1, 1, 1] = fun _ => (3 : ℝ) := by
  ext j
  fin_cases j <;> norm_num [incidenceRows, Matrix.transpose, Matrix.mulVec,
    dotProduct, Fin.sum_univ_succ]

end NetworkSimplex.Chain.ThresholdObstruction
