import Formal.NetworkSimplex.ThresholdSourceGrouping
import Formal.NetworkSimplex.ThresholdSmallCompleteness
import Formal.NetworkSimplex.ThresholdTwoUnit

/-! Exact original-row branch descriptions for one and two explicit labels. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open NetworkSimplex.Threshold

theorem source_branch_nonneg {m n q : ℕ} {I : Type*} (D : ReductionData m I)
    (normal : Fin n → Fin m → ℤ) (weight : Fin q → Fin n → ℤ)
    (hw : ∀ c i, 0 ≤ weight c i)
    (hc : ∀ c j, ∑ i, weight c i * normal i j = 0)
    (c : Fin q) (r : Fin n → ProfileRow m I)
    (hb : ∀ k, weight c k ≠ 0 → normalVector (D.rowNormal (r k)) = normal k)
    (x : Fin m → ℝ) (hx : ∀ r, (D.rowNormal r).value x ≤ D.rowRhs r) :
    0 ≤ ∑ k, (weight c k : ℝ) * D.rowRhs (r k) := by
  have heq : (∑ k, (weight c k : ℝ) * (D.rowNormal (r k)).value x) = 0 := by
    simp_rw [profileNormal_value_eq_dot, Finset.mul_sum]
    rw [Finset.sum_comm]
    have hz (j : Fin m) :
        (∑ k, (weight c k : ℝ) * (normalVector (D.rowNormal (r k)) j : ℝ)) = 0 := by
      have hs : (∑ k, weight c k * normalVector (D.rowNormal (r k)) j) = 0 := by
        calc
          _ = ∑ k, weight c k * normal k j := by
            apply Finset.sum_congr rfl
            intro k _
            by_cases hk : weight c k = 0
            · simp [hk]
            · rw [hb k hk]
          _ = 0 := hc c j
      exact_mod_cast hs
    simp_rw [← mul_assoc, ← Finset.sum_mul, hz, zero_mul]
    simp
  rw [← heq]
  exact Finset.sum_le_sum fun k _ => mul_le_mul_of_nonneg_left (hx (r k)) (by exact_mod_cast hw c k)

def OneBranch {I : Type*} (D : ReductionData 1 I) (_c : Fin 1)
    (r : Fin 2 → ProfileRow 1 I) : Prop :=
  ∀ k, normalVector (D.rowNormal (r k)) = OneStateCircuits.normal k

/-- All nonzero reduced directions occur in the 2-direction library. -/
theorem one_normal_cover (n : ProfileNormal 1) :
    normalVector n = 0 ∨ ∃ i, normalVector n = OneStateCircuits.normal i := by
  revert n
  decide

/-- The complete original-row branch family, with no added box rows. -/
def OneSourceTests {I : Type*} (D : ReductionData 1 I) : Prop :=
  (∀ r, normalVector (D.rowNormal r) = 0 → 0 ≤ D.rowRhs r) ∧
    ∀ c r, OneBranch D c r →
      0 ≤ ∑ k, (OneStateCircuits.weight c k : ℝ) * D.rowRhs (r k)

theorem one_source_tests_iff_profile {I : Type*} [Finite I] (D : ReductionData 1 I) :
    OneSourceTests D ↔ ∃ x, D.ReducedProfile x := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  let _ : Nonempty (ProfileRow 1 I) := ⟨.totalLower⟩
  constructor
  · rintro ⟨hz, hb⟩
    have hc (r : ProfileRow 1 I) :
        (fun j => (normalVector (D.rowNormal r) j : ℝ)) = 0 ∨
          ∃ i, (fun j => (normalVector (D.rowNormal r) j : ℝ)) =
            fun j => (OneStateCircuits.normal i j : ℝ) := by
      rcases one_normal_cover (D.rowNormal r) with h | ⟨i, h⟩
      · left; funext j; simp [h]
      · right; exact ⟨i, by rw [h]⟩
    obtain ⟨x, hx⟩ := source_branches_sufficient
      (fun r j => (normalVector (D.rowNormal r) j : ℝ)) D.rowRhs
      (fun i j => (OneStateCircuits.normal i j : ℝ))
      (fun c i => (OneStateCircuits.weight c i : ℝ)) hc
      (fun rhs ht => (one_partial_feasible_iff rhs).mpr ht)
      (fun r h => hz r (by
        funext j
        have hh : (normalVector (D.rowNormal r) j : ℝ) = 0 := congrFun h j
        exact_mod_cast hh))
      (fun c rows h => hb c rows (by
        intro i
        have hh := h i (by simp [OneStateCircuits.weight])
        funext j
        have hj := congrFun hh j
        exact_mod_cast hj))
    refine ⟨x, (D.rows_iff_reducedProfile x).mp ?_⟩
    intro r
    simpa only [profileNormal_value_eq_dot] using hx r
  · rintro ⟨x, hx⟩
    have hr := (D.rows_iff_reducedProfile x).mpr hx
    refine ⟨?_, fun c rows h => source_branch_nonneg D OneStateCircuits.normal
      OneStateCircuits.weight OneStateCircuits.weight_nonnegative
      OneStateCircuits.normal_cancellation c rows (fun k _ => h k) x hr⟩
    intro r hz
    have hh := hr r
    simpa [profileNormal_value_eq_dot, hz] using hh

/-- The source-only branch description is exact in the original graph coordinates. -/
theorem one_mem_hull_iff_source_tests {L : ℕ} (D : ReductionData 1 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧ OneSourceTests D := by
  rw [D.mem_hull_iff, one_source_tests_iff_profile]
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => exists_congr fun x => D.rows_iff_reducedProfile x


/-- All nonzero reduced directions occur in the 6-direction library. -/
theorem two_normal_cover (n : ProfileNormal 2) :
    normalVector n = 0 ∨ ∃ i, normalVector n = TwoStateCircuits.normal i := by
  revert n
  decide

/-- The complete original-row branch family, with no added box rows. -/
def TwoSourceTests {I : Type*} (D : ReductionData 2 I) : Prop :=
  (∀ r, normalVector (D.rowNormal r) = 0 → 0 ≤ D.rowRhs r) ∧
    ∀ c r, TwoLabels.TwoBranch D c r →
      0 ≤ ∑ k, (TwoStateCircuits.weight c k : ℝ) * D.rowRhs (r k)

theorem two_source_tests_iff_profile {I : Type*} [Finite I] (D : ReductionData 2 I) :
    TwoSourceTests D ↔ ∃ x, D.ReducedProfile x := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  let _ : Nonempty (ProfileRow 2 I) := ⟨.totalLower⟩
  constructor
  · rintro ⟨hz, hb⟩
    have hc (r : ProfileRow 2 I) :
        (fun j => (normalVector (D.rowNormal r) j : ℝ)) = 0 ∨
          ∃ i, (fun j => (normalVector (D.rowNormal r) j : ℝ)) =
            fun j => (TwoStateCircuits.normal i j : ℝ) := by
      rcases two_normal_cover (D.rowNormal r) with h | ⟨i, h⟩
      · left; funext j; simp [h]
      · right; exact ⟨i, by rw [h]⟩
    obtain ⟨x, hx⟩ := source_branches_sufficient
      (fun r j => (normalVector (D.rowNormal r) j : ℝ)) D.rowRhs
      (fun i j => (TwoStateCircuits.normal i j : ℝ))
      (fun c i => (TwoStateCircuits.weight c i : ℝ)) hc
      (fun rhs ht => (two_partial_feasible_iff rhs).mpr ht)
      (fun r h => hz r (by
        funext j
        have hh : (normalVector (D.rowNormal r) j : ℝ) = 0 := congrFun h j
        exact_mod_cast hh))
      (fun c rows h => hb c rows (by
        intro i hi
        have hh := h i (by exact_mod_cast hi)
        funext j
        have hj := congrFun hh j
        exact_mod_cast hj))
    refine ⟨x, (D.rows_iff_reducedProfile x).mp ?_⟩
    intro r
    simpa only [profileNormal_value_eq_dot] using hx r
  · rintro ⟨x, hx⟩
    have hr := (D.rows_iff_reducedProfile x).mpr hx
    refine ⟨?_, fun c rows h => source_branch_nonneg D TwoStateCircuits.normal
      TwoStateCircuits.weight TwoStateCircuits.weight_nonnegative
      TwoStateCircuits.normal_cancellation c rows h x hr⟩
    intro r hz
    have hh := hr r
    simpa [profileNormal_value_eq_dot, hz] using hh

/-- The source-only branch description is exact in the original graph coordinates. -/
theorem two_mem_hull_iff_source_tests {L : ℕ} (D : ReductionData 2 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧ TwoSourceTests D := by
  rw [D.mem_hull_iff, two_source_tests_iff_profile]
  rw [D.exists_fullProfile_iff_rows hc hh]
  exact and_congr_right fun _ => exists_congr fun x => D.rows_iff_reducedProfile x


end NetworkSimplex.Chain.Threshold
