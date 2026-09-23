import Formal.NetworkSimplex.Chain

/-! A balanced-incidence family with unbounded coefficient ratios. -/
namespace NetworkSimplex.Chain.ThresholdStarFamily
open Matrix
open scoped BigOperators

/-- Label zero is the last label in the paper; the other `k` labels are successors. -/
def allowed (k : ℕ) (i j : Fin (k + 1)) : Prop :=
  if i = 0 then j ≠ 0 else j = 0 ∨ j = i

instance (k : ℕ) (i j : Fin (k + 1)) : Decidable (allowed k i j) := by
  unfold allowed
  infer_instance

def incidenceMatrix (k : ℕ) : Matrix (Fin (k + 1)) (Fin (k + 1)) ℝ :=
  fun i j => if allowed k i j then 1 else 0

def balancingWeight (k : ℕ) (i : Fin (k + 1)) : ℝ :=
  if i = 0 then (k : ℝ) - 1 else 1

@[simp] theorem allowed_zero (k : ℕ) (j : Fin (k + 1)) : allowed k 0 j ↔ j ≠ 0 := by
  simp [allowed]

@[simp] theorem allowed_succ (k : ℕ) (i : Fin k) (j : Fin (k + 1)) :
    allowed k i.succ j ↔ j = 0 ∨ j = i.succ := by
  simp [allowed]

@[simp] theorem matrix_zero (k : ℕ) (x : Fin (k + 1) → ℝ) :
    (incidenceMatrix k *ᵥ x) 0 = ∑ i : Fin k, x i.succ := by
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_succ, incidenceMatrix]

@[simp] theorem matrix_succ (k : ℕ) (x : Fin (k + 1) → ℝ) (i : Fin k) :
    (incidenceMatrix k *ᵥ x) i.succ = x 0 + x i.succ := by
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_succ, incidenceMatrix,
    ite_mul]

theorem kernel_zero {k : ℕ} (hk : 0 < k) (x : Fin (k + 1) → ℝ)
    (hx : incidenceMatrix k *ᵥ x = 0) : x = 0 := by
  have h0 := congrFun hx 0
  simp only [matrix_zero, Pi.zero_apply] at h0
  have hi : ∀ i : Fin k, x i.succ = -x 0 := by
    intro i
    have h := congrFun hx i.succ
    simp only [matrix_succ, Pi.zero_apply] at h
    linarith
  simp_rw [hi] at h0
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at h0
  have hkR : (0 : ℝ) < k := by exact_mod_cast hk
  have hx0 : x 0 = 0 := by nlinarith
  funext i
  refine Fin.cases hx0 (fun j => ?_) i
  simp [hi, hx0]

theorem matrix_injective {k : ℕ} (hk : 0 < k) :
    Function.Injective (fun x => incidenceMatrix k *ᵥ x) := by
  intro x y hxy
  dsimp only at hxy
  have h := kernel_zero hk (x - y) (by rw [Matrix.mulVec_sub, hxy, sub_self])
  exact sub_eq_zero.mp h

theorem matrix_isUnit {k : ℕ} (hk : 0 < k) : IsUnit (incidenceMatrix k) :=
  Matrix.mulVec_injective_iff_isUnit.mp (matrix_injective hk)

theorem weight_positive {k : ℕ} (hk : 2 ≤ k) (i : Fin (k + 1)) :
    0 < balancingWeight k i := by
  unfold balancingWeight
  split_ifs
  · have hkR : (2 : ℝ) ≤ k := by exact_mod_cast hk
    linarith
  · norm_num

/-- Every column has the same positive weighted sum. -/
theorem balanced (k : ℕ) (j : Fin (k + 1)) :
    ∑ i, balancingWeight k i * incidenceMatrix k i j = k := by
  refine Fin.cases ?_ (fun j => ?_) j
  · simp [Fin.sum_univ_succ, balancingWeight, incidenceMatrix]
  · simp [Fin.sum_univ_succ, balancingWeight, incidenceMatrix]

theorem row_nonempty {k : ℕ} (hk : 0 < k) (i : Fin (k + 1)) :
    ∃ j, allowed k i j := by
  refine Fin.cases ?_ (fun i => ?_) i
  · exact ⟨(⟨0, hk⟩ : Fin k).succ, by simp⟩
  · exact ⟨0, by simp⟩

theorem row_proper {k : ℕ} (hk : 2 ≤ k) (i : Fin (k + 1)) :
    ∃ j, ¬ allowed k i j := by
  refine Fin.cases ?_ (fun i => ?_) i
  · exact ⟨0, by simp⟩
  · let z : Fin k := ⟨0, by omega⟩
    let o : Fin k := ⟨1, by omega⟩
    by_cases hi : i = z
    · refine ⟨o.succ, ?_⟩
      simp [allowed, hi, z, o]
    · refine ⟨z.succ, ?_⟩
      simp [Ne.symm hi]

/-- The large normal coordinate divided by any remaining one is `k - 1`. -/
theorem weight_ratio {k : ℕ} (i : Fin k) :
    balancingWeight k 0 = ((k : ℝ) - 1) * balancingWeight k i.succ := by
  simp [balancingWeight]


/-- Finset presentation used by the general balanced-incidence construction. -/
def S (k : ℕ) (i : Fin (k + 1)) : Finset (Fin (k + 1)) :=
  Finset.univ.filter (allowed k i)

@[simp] theorem mem_S (k : ℕ) (i j : Fin (k + 1)) : j ∈ S k i ↔ allowed k i j := by
  simp [S]

theorem matrix_eq_finset (k : ℕ) : incidenceMatrix k =
    (fun i j => if j ∈ S k i then (1 : ℝ) else 0) := by
  ext i j
  simp [incidenceMatrix]

theorem det_isUnit {k : ℕ} (hk : 0 < k) : IsUnit (incidenceMatrix k).det :=
  (Matrix.isUnit_iff_isUnit_det _).mp (matrix_isUnit hk)

theorem S_nonempty {k : ℕ} (hk : 0 < k) (i : Fin (k + 1)) : (S k i).Nonempty := by
  simpa only [Finset.Nonempty, mem_S] using row_nonempty hk i

theorem S_proper {k : ℕ} (hk : 2 ≤ k) (i : Fin (k + 1)) : S k i ≠ Finset.univ := by
  obtain ⟨j, hj⟩ := row_proper hk i
  intro he
  exact hj ((mem_S k i j).mp (by simp [he]))

theorem S_zero_card (k : ℕ) : (S k 0).card = k := by
  have he : S k 0 = Finset.univ.erase 0 := by ext j; simp
  rw [he, Finset.card_erase_of_mem (Finset.mem_univ _)]
  simp

theorem S_succ (k : ℕ) (i : Fin k) : S k i.succ = {0, i.succ} := by
  ext j
  simp

theorem S_succ_card (k : ℕ) (i : Fin k) : (S k i.succ).card = 2 := by
  rw [S_succ]
  simp [Ne.symm (Fin.succ_ne_zero i)]

/-- Exactly the forbidden row-label pairs are observed. -/
def Observations (k : ℕ) := {ij : Fin (k + 1) × Fin (k + 1) // ij.2 ∉ S k ij.1}

instance (k : ℕ) : Fintype (Observations k) := by unfold Observations; infer_instance

/-- One forbidden label in the first row, and `k-1` in every remaining row. -/
theorem observations_card (k : ℕ) : Fintype.card (Observations k) = 1 + k * (k - 1) := by
  let e : Observations k ≃ (i : Fin (k + 1)) × {j : Fin (k + 1) // j ∉ S k i} :=
    { toFun := fun x => ⟨x.val.1, ⟨x.val.2, x.property⟩⟩
      invFun := fun x => ⟨(x.1, x.2.val), x.2.property⟩
      left_inv := fun _ => rfl
      right_inv := fun _ => rfl }
  rw [Fintype.card_congr e, Fintype.card_sigma, Fin.sum_univ_succ]
  simp only [Fintype.card_subtype_compl, Fintype.card_fin,
    Fintype.card_coe, S_zero_card, S_succ_card]
  simp

/-- Counts for the actual chain with `k+1` gadgets and states. -/
theorem graph_counts (k : ℕ) :
    Fintype.card (Fin (k + 2)) = k + 2 ∧
    Fintype.card (ChainArc (k + 1)) = 2 * k + 3 ∧
    Fintype.card (Fin (k + 1)) = k + 1 := by
  simp [ChainArc]
  omega

end NetworkSimplex.Chain.ThresholdStarFamily
