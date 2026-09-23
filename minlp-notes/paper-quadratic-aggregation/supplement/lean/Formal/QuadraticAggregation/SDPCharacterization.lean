import Formal.QuadraticAggregation.Headline
import Formal.DAGSpectral.UpperTriangle

/-!
# Exact finite semidefinite tests for a full quadratic hull

The common feasible set consists of nonnegative multipliers of sum one whose
aggregate matrix is positive semidefinite. Testing both signs of every independent matrix
and vector entry detects precisely the nontrivial certificates. These are exact
mathematical optimization statements; no numerical solver is formalized.
-/

open Set
open scoped BigOperators Matrix

namespace QuadraticAggregation.System

variable {n m : ℕ}

/-- The common feasible set of the finite semidefinite optimization tests. -/
def normalizedPSD (D : System n m) : Set (Vec m) :=
  {w | (∀ i, 0 ≤ w i) ∧ (∑ i, w i) = 1 ∧ (D.aggA w).PosSemidef}

/-- An entry of the quadratic or linear aggregate coefficient. -/
abbrev CoefficientIndex (n : ℕ) := {ij : Fin n × Fin n // ij.1 ≤ ij.2} ⊕ Fin n

def coefficientObjective (D : System n m) (k : CoefficientIndex n) (w : Vec m) : ℝ :=
  match k with
  | .inl ij => D.aggA w ij.val.1 ij.val.2
  | .inr i => D.aggB w i

/-- Every objective is linear in the original `m` multiplier variables. -/
theorem coefficientObjective_eq_sum (D : System n m) (k : CoefficientIndex n)
    (w : Vec m) :
    D.coefficientObjective k w = ∑ i, w i *
      (match k with
       | .inl ij => D.A i ij.val.1 ij.val.2
       | .inr j => D.b i j) := by
  rcases k with ⟨⟨i, j⟩, _⟩ | i <;>
    simp [coefficientObjective, aggA, aggB, Matrix.sum_apply, Matrix.smul_apply,
      Finset.sum_apply]

theorem continuous_coefficientObjective (D : System n m) (k : CoefficientIndex n) :
    Continuous (D.coefficientObjective k) := by
  rcases k with ⟨⟨i, j⟩, _⟩ | i
  · exact (continuous_apply j).comp ((continuous_apply i).comp D.continuous_aggA)
  · exact (continuous_apply i).comp D.continuous_aggB

theorem coefficients_zero_iff (D : System n m) (w : Vec m) :
    (∀ k, D.coefficientObjective k w = 0) ↔ D.aggA w = 0 ∧ D.aggB w = 0 := by
  constructor
  · intro h
    constructor
    · ext i j
      by_cases hij : i ≤ j
      · exact h (.inl ⟨(i, j), hij⟩)
      · have hji := h (.inl ⟨(j, i), le_of_not_ge hij⟩)
        change D.aggA w j i = 0 at hji
        rw [(D.aggA_isSymm w).apply] at hji
        exact hji
    · ext i
      exact h (.inr i)
  · rintro ⟨hA, hB⟩ (⟨⟨i, j⟩, _⟩ | i) <;> simp [coefficientObjective, hA, hB]

theorem isCompact_normalizedPSD (D : System n m) : IsCompact D.normalizedPSD := by
  have hclosed : IsClosed {w : Vec m | (D.aggA w).PosSemidef} := by
    have heq : {w : Vec m | (D.aggA w).PosSemidef} =
        ⋂ x : Vec n, {w | 0 ≤ q (D.aggA w) x} := by
      ext w
      simp only [mem_ofPred_eq, mem_iInter]
      rw [Matrix.posSemidef_iff_dotProduct_mulVec]
      have hsym := (Matrix.isHermitian_iff_isSymm).mpr (D.aggA_isSymm w)
      simp only [hsym, true_and, q]
      simp
    rw [heq]
    apply isClosed_iInter
    intro x
    apply isClosed_le continuous_const
    unfold q aggA Matrix.mulVec dotProduct
    fun_prop
  have heq : D.normalizedPSD = stdSimplex ℝ (Fin m) ∩
      {w | (D.aggA w).PosSemidef} := by
    ext w
    simp only [normalizedPSD, stdSimplex, mem_ofPred_eq, mem_inter_iff]
    tauto
  rw [heq]
  exact (isCompact_stdSimplex ℝ (Fin m)).inter_right hclosed

theorem normalizedPSD_ne_zero (D : System n m) {w : Vec m}
    (hw : w ∈ D.normalizedPSD) : w ≠ 0 := by
  intro h
  have := hw.2.1
  simp [h] at this

theorem aggA_smul (D : System n m) (t : ℝ) (w : Vec m) :
    D.aggA (t • w) = t • D.aggA w := by
  simp [aggA, Finset.smul_sum, smul_smul]

theorem aggB_smul (D : System n m) (t : ℝ) (w : Vec m) :
    D.aggB (t • w) = t • D.aggB w := by
  simp [aggB, Finset.smul_sum, smul_smul]

/-- A certificate can always be normalized to the common SDP feasible set. -/
theorem Certificate.exists_normalized {D : System n m} {w : Vec m}
    (hw : D.Certificate w) :
    ∃ v ∈ D.normalizedPSD, D.aggA v ≠ 0 ∨ D.aggB v ≠ 0 := by
  have hpos : 0 < ∑ i, w i := by
    apply Finset.sum_pos'
    · exact fun i _ => hw.1 i
    · by_contra! h
      apply hw.2.1
      ext i
      exact le_antisymm (h i (Finset.mem_univ i)) (hw.1 i)
  let t : ℝ := (∑ i, w i)⁻¹
  have ht : 0 < t := inv_pos.mpr hpos
  refine ⟨t • w, ⟨fun i => mul_nonneg ht.le (hw.1 i), ?_, ?_⟩, ?_⟩
  · simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum]
    exact inv_mul_cancel₀ (ne_of_gt hpos)
  · rw [D.aggA_smul]
    exact hw.2.2.1.smul ht.le
  · rw [D.aggA_smul, D.aggB_smul]
    rcases hw.2.2.2 with hA | hB
    · exact Or.inl (smul_ne_zero (ne_of_gt ht) hA)
    · exact Or.inr (smul_ne_zero (ne_of_gt ht) hB)

/-- Absence of nontrivial certificates is exactly triviality of every PSD
nonnegative aggregation, including the zero multiplier. -/
theorem no_certificate_iff_trivial (D : System n m) :
    (¬ ∃ w, D.Certificate w) ↔
      ∀ w, (∀ i, 0 ≤ w i) → (D.aggA w).PosSemidef →
        D.aggA w = 0 ∧ D.aggB w = 0 := by
  constructor
  · intro h w hw hpsd
    by_cases hw0 : w = 0
    · simp [hw0]
    · by_contra! hne
      exact h ⟨w, hw, hw0, hpsd, by tauto⟩
  · intro h ⟨w, hw, _, hpsd, hne⟩
    obtain ⟨hA, hB⟩ := h w hw hpsd
    exact hne.elim (fun h => h hA) (fun h => h hB)

/-- The normalized coefficient tests are equivalent to absence of certificates. -/
theorem no_certificate_iff_normalized_zero (D : System n m) :
    (¬ ∃ w, D.Certificate w) ↔
      ∀ w ∈ D.normalizedPSD, ∀ k, D.coefficientObjective k w = 0 := by
  constructor
  · intro h w hw
    apply (D.coefficients_zero_iff w).mpr
    by_contra! hne
    exact h ⟨w, hw.1, D.normalizedPSD_ne_zero hw, hw.2.2, by tauto⟩
  · intro h ⟨w, hw⟩
    obtain ⟨v, hv, hne⟩ := hw.exists_normalized
    obtain ⟨hA, hB⟩ := (D.coefficients_zero_iff v).mp (h v hv)
    exact hne.elim (fun h => h hA) (fun h => h hB)

/-- Each of the signed linear objectives attains its maximum when feasible. -/
theorem signed_objective_attains (D : System n m) (k : CoefficientIndex n)
    (s : ℝ) (hne : D.normalizedPSD.Nonempty) :
    ∃ v, IsGreatest ((fun w => s * D.coefficientObjective k w) '' D.normalizedPSD) v := by
  exact (D.isCompact_normalizedPSD.image
    (continuous_const.mul (D.continuous_coefficientObjective k))).exists_isGreatest
      (hne.image _)

/-- An exact SDP decision condition: infeasibility, or zero attained maximum for
both signs of every coefficient objective. -/
def SDPTestsZero (D : System n m) : Prop :=
  D.normalizedPSD = ∅ ∨
    ∀ k : CoefficientIndex n,
      IsGreatest (D.coefficientObjective k '' D.normalizedPSD) 0 ∧
      IsGreatest ((fun w => -D.coefficientObjective k w) '' D.normalizedPSD) 0

theorem sdpTestsZero_iff_no_certificate (D : System n m) :
    D.SDPTestsZero ↔ ¬ ∃ w, D.Certificate w := by
  rw [D.no_certificate_iff_normalized_zero]
  constructor
  · rintro (hempty | h) w hw k
    · simp [hempty] at hw
    · have hle := (h k).1.2 ⟨w, hw, rfl⟩
      have hneg := (h k).2.2 ⟨w, hw, rfl⟩
      exact le_antisymm hle (by linarith)
  · intro h
    by_cases hempty : D.normalizedPSD = ∅
    · exact Or.inl hempty
    · right
      obtain ⟨w, hw⟩ := Set.nonempty_iff_ne_empty.mpr hempty
      intro k
      constructor
      · refine ⟨⟨w, hw, h w hw k⟩, ?_⟩
        rintro _ ⟨v, hv, rfl⟩
        exact (h v hv k).le
      · refine ⟨⟨w, hw, by simp [h w hw k]⟩, ?_⟩
        rintro _ ⟨v, hv, rfl⟩
        simp [h v hv k]

/-- The source uses both signs of each independent matrix and vector entry. -/
theorem signed_objective_count (n : ℕ) :
    2 * Fintype.card (CoefficientIndex n) = n * (n + 1) + 2 * n := by
  have hc : Fintype.card {ij : Fin n × Fin n // ij.1 ≤ ij.2} =
      n * (n + 1) / 2 := by
    rw [← Fintype.card_congr (DAGSpectral.upperCoordEquiv n), DAGSpectral.card_upperCoord]
  change 2 * (Fintype.card (_ ⊕ _)) = _
  rw [Fintype.card_sum, hc, Fintype.card_fin]
  have heven : 2 ∣ n * (n + 1) := Nat.two_dvd_mul_add_one n
  omega

/-- Corollary 3, with exact feasibility and attained objective values. -/
theorem full_hull_iff_sdpTestsZero (D : System n m)
    (hS : D.feasible.Nonempty) (hHC : D.AsymptoticHC) :
    convexHull ℝ D.feasible = Set.univ ↔ D.SDPTestsZero := by
  rw [D.sdpTestsZero_iff_no_certificate, ← D.proper_hull_iff_certificate hS hHC]
  exact not_not.symm

end QuadraticAggregation.System
