import Formal.CubicGap.Maxima
import Formal.CubicGap.TermwiseFamilyUpper
import Formal.MultilinearGap.Attainment

/-! Exact upper and termwise values for the analytic three-group cubic family. -/
namespace CubicGap
noncomputable section

def analyticCoefficients (m : ℕ) : Fin 6 → ℚ :=
  ![2, 3, 2 * m, 5 * m / 3, 10 * m / 9, m]

def analyticFamily (m : ℕ) := threeFamily m (analyticCoefficients m)
def analyticMeans (m : ℕ) := thresholdThreeMeans m

def analyticTermwiseGap (m : ℕ) : ℝ :=
  termwiseUpperThree m (analyticCoefficients m) -
    termwiseLowerThree m (analyticCoefficients m)

theorem analyticCoefficients_nonneg (m : ℕ) (i : Fin 6) :
    0 ≤ analyticCoefficients m i := by
  fin_cases i <;> dsimp [analyticCoefficients] <;> positivity

theorem analyticCoefficients_pos (m : ℕ) (hm : 0 < m) (i : Fin 6) :
    0 < analyticCoefficients m i := by
  have : (0 : ℚ) < m := by exact_mod_cast hm
  fin_cases i <;> dsimp [analyticCoefficients] <;> positivity

theorem analyticCoefficients_integer (m : ℕ) (hm : 9 ∣ m) (i : Fin 6) :
    ∃ n : ℕ, analyticCoefficients m i = n := by
  obtain ⟨k, rfl⟩ := hm
  fin_cases i
  · exact ⟨2, rfl⟩
  · exact ⟨3, rfl⟩
  · exact ⟨18*k, by simp [analyticCoefficients]; ring⟩
  · exact ⟨15*k, by simp [analyticCoefficients]; ring⟩
  · exact ⟨10*k, by simp [analyticCoefficients]; ring⟩
  · exact ⟨9*k, by simp [analyticCoefficients]⟩

theorem choose_two_real (m : ℕ) :
    (m.choose 2 : ℝ) = (m : ℝ) * (m-1) / 2 := Nat.cast_choose_two ℝ m

theorem choose_three_real (m : ℕ) :
    (m.choose 3 : ℝ) = (m : ℝ) * (m-1) * (m-2) / 6 := by
  have h := Nat.descFactorial_eq_factorial_mul_choose m 3
  have hc : (m.descFactorial 3 : ℝ) = 6 * (m.choose 3 : ℝ) := by
    exact_mod_cast h
  rcases lt_or_ge m 2 with hm | hm
  · interval_cases m <;> norm_num [Nat.choose]
  · rw [show 3 = 2+1 from rfl, Nat.descFactorial_succ, Nat.cast_mul,
      Nat.cast_sub hm, Nat.cast_descFactorial_two] at hc
    norm_num at hc
    nlinarith [hc]

theorem analytic_maximum (m : ℕ) (hm : 0 < m) :
    IsGreatest (envelopeValues (analyticFamily m) (analyticMeans m))
      (orbitUpper m (analyticCoefficients m) : ℝ) :=
  three_maximum m hm _ (analyticCoefficients_nonneg m)

theorem analytic_orbitUpper (m : ℕ) :
    (orbitUpper m (analyticCoefficients m) : ℝ) =
      (167/72 : ℝ) * m^3 - (17/8 : ℝ) * m^2 + m/2 := by
  simp [orbitUpper, analyticCoefficients, Nat.cast_choose_two, choose_three_real]
  ring

theorem analytic_scaled_maximum (m : ℕ) (hm : 0 < m) :
    (18 : ℝ) / m^3 * sSup (envelopeValues (analyticFamily m) (analyticMeans m)) =
      167/4 - 153/(4*m) + 9/m^2 := by
  rw [(analytic_maximum m hm).csSup_eq, analytic_orbitUpper]
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  field_simp
  ring

theorem analytic_termwiseGap (m : ℕ) :
    analyticTermwiseGap m = (161/72 : ℝ)*m^3 - (15/8 : ℝ)*m^2 + m/3 := by
  rw [analyticTermwiseGap, termwiseUpperThree_eq, termwiseLowerThree_eq,
    analytic_orbitUpper]
  simp [orbitLower, analyticCoefficients, choose_three_real]
  ring

theorem analytic_scaled_termwiseGap (m : ℕ) (hm : 0 < m) :
    (18 : ℝ) / m^3 * analyticTermwiseGap m =
      161/4 - 135/(4*m) + 6/m^2 := by
  rw [analytic_termwiseGap]
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast Nat.ne_of_gt hm
  field_simp
  ring

/-- The graph point at the prescribed means gives a strict lower endpoint witness. -/
theorem analytic_value_at_means (m : ℕ) :
    analyticFamily m (analyticMeans m) =
      (373/288 : ℝ)*m^3 - (9/8 : ℝ)*m^2 + (9/32 : ℝ)*m := by
  simp [analyticFamily, analyticMeans, threeFamily, analyticCoefficients,
    thresholdThreeMeans, elementary_const, Fin.ext_iff,
    Nat.cast_choose_two, choose_three_real]
  ring

/-- The denominator in the analytic-family ratio is strictly positive. -/
theorem analytic_hullGap_pos (m : ℕ) (hm : 9 ≤ m) :
    0 < hullGap (analyticFamily m) (analyticMeans m) := by
  have hm0 : 0 < m := by omega
  have hm' : (9 : ℝ) ≤ m := by exact_mod_cast hm
  have hmem : analyticFamily m (analyticMeans m) ∈
      envelopeValues (analyticFamily m) (analyticMeans m) :=
    subset_convexHull ℝ _ ⟨thresholdThreeMeans_mem_cube m, rfl⟩
  have hle : sInf (envelopeValues (analyticFamily m) (analyticMeans m)) ≤
      analyticFamily m (analyticMeans m) :=
    csInf_le (envelopeValues_isCompact _
      (threeFamily_coordinate_affine m (analyticCoefficients m)) _).bddBelow hmem
  rw [hullGap, (analytic_maximum m hm0).csSup_eq]
  rw [analytic_value_at_means] at hle
  rw [analytic_orbitUpper]
  have hp : 0 < (m : ℝ) * (295 * (m : ℝ)^2 - 288*m + 63) := by
    apply mul_pos (by positivity)
    nlinarith [sq_nonneg ((m : ℝ)-1)]
  nlinarith

end
end CubicGap
