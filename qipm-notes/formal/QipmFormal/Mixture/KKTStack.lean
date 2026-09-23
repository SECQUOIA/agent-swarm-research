import QipmFormal.Mixture.KKT
import QipmFormal.Mixture.Augmentation

/-!
# The literal nonnegative KKT stack

The columns are primal variables, positive multipliers, negative multipliers,
and dual slacks. The rows are primal feasibility and stationarity. Each raw
input-dependent coefficient appears once in the primal block and twice in the
two multiplier blocks.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators
variable {R C I : Type*}

abbrev KKTColumn (R C : Type*) := C ⊕ (R ⊕ (R ⊕ C))

def kktMatrix [DecidableEq C] (A : R → C → ℝ) : (R ⊕ C) → KKTColumn R C → ℝ
  | Sum.inl r, Sum.inl j => A r j
  | Sum.inl _, Sum.inr _ => 0
  | Sum.inr _, Sum.inl _ => 0
  | Sum.inr j, Sum.inr (Sum.inl r) => A r j
  | Sum.inr j, Sum.inr (Sum.inr (Sum.inl r)) => -A r j
  | Sum.inr j, Sum.inr (Sum.inr (Sum.inr q)) => if j = q then 1 else 0

def kktWitness (x : C → ℝ) (y : R → ℝ) (s : C → ℝ) : KKTColumn R C → ℝ
  | Sum.inl j => x j
  | Sum.inr (Sum.inl r) => max (y r) 0
  | Sum.inr (Sum.inr (Sum.inl r)) => max (-y r) 0
  | Sum.inr (Sum.inr (Sum.inr j)) => s j

theorem split_multiplier_difference (y : ℝ) : max y 0 - max (-y) 0 = y := by
  rcases le_total 0 y with h | h
  · simp [max_eq_left h, max_eq_right (neg_nonpos.mpr h)]
  · simp [max_eq_right h, max_eq_left (neg_nonneg.mpr h)]

theorem kktWitness_nonnegative (x : C → ℝ) (y : R → ℝ) (s : C → ℝ)
    (hx : ∀ j, 0 ≤ x j) (hs : ∀ j, 0 ≤ s j) :
    ∀ j, 0 ≤ kktWitness x y s j := by
  intro j
  rcases j with j | (r | (r | j))
  · exact hx j
  · exact le_max_right _ _
  · exact le_max_right _ _
  · exact hs j

theorem kktWitness_height (x : C → ℝ) (y : R → ℝ) (s : C → ℝ) (H : ℝ)
    (hH : 0 ≤ H) (hx : ∀ j, |x j| ≤ H) (hy : ∀ r, |y r| ≤ H)
    (hs : ∀ j, |s j| ≤ H) : ∀ j, |kktWitness x y s j| ≤ H := by
  intro j
  rcases j with j | (r | (r | j))
  · exact hx j
  · simp only [kktWitness, abs_of_nonneg (le_max_right (y r) (0 : ℝ))]
    exact max_le ((le_abs_self _).trans (hy r)) hH
  · simp only [kktWitness, abs_of_nonneg (le_max_right (-y r) (0 : ℝ))]
    exact max_le ((neg_le_abs _).trans (hy r)) hH
  · exact hs j

theorem kktMatrix_residual_primal [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (b : R → ℝ) (c x s : C → ℝ) (y : R → ℝ) (r : R) :
    residual (kktMatrix A) (kktWitness x y s) (Sum.elim b c) (Sum.inl r) =
      residual A x b r := by
  simp [residual, Fintype.sum_sum_type, kktMatrix, kktWitness]

theorem kktMatrix_residual_dual [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (b : R → ℝ) (c x s : C → ℝ) (y : R → ℝ) (j : C) :
    residual (kktMatrix A) (kktWitness x y s) (Sum.elim b c) (Sum.inr j) =
      stationarity A y s c j := by
  simp only [residual, Fintype.sum_sum_type, kktMatrix, kktWitness, Sum.elim_inr,
    zero_mul, Finset.sum_const_zero, zero_add, stationarity]
  simp only [ite_mul, one_mul, zero_mul]
  rw [← add_assoc, ← Finset.sum_add_distrib]
  congr 2
  · apply Finset.sum_congr rfl
    intro r _
    calc
      _ = A r j * (max (y r) 0 - max (-y r) 0) := by ring
      _ = A r j * y r := by rw [split_multiplier_difference]
  · simp

theorem kktMatrix_bound [DecidableEq C] (A : R → C → ℝ) (B : ℝ)
    (hA : ∀ r j, |A r j| ≤ B) : ∀ r j, |kktMatrix A r j| ≤ max B 1 := by
  intro r j
  rcases r with r | q <;> rcases j with j | (r' | (r' | j))
  all_goals simp only [kktMatrix, abs_zero, abs_neg]
  all_goals first
  | exact (hA _ _).trans (le_max_left _ _)
  | exact (by norm_num : (0 : ℝ) ≤ 1).trans (le_max_right _ _)
  | split_ifs <;> simp only [abs_one, abs_zero]
    · exact le_max_right _ _
    · exact (by norm_num : (0 : ℝ) ≤ 1).trans (le_max_right _ _)

theorem kktMatrix_support_primal [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (r : R) :
    rowSupportCount (kktMatrix A (Sum.inl r)) = rowSupportCount (A r) := by
  simp [rowSupportCount, Fintype.sum_sum_type, kktMatrix]
  congr 1

theorem kktMatrix_support_dual [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (j : C) :
    rowSupportCount (kktMatrix A (Sum.inr j)) =
      2 * rowSupportCount (fun r => A r j) + 1 := by
  simp only [rowSupportCount, Fintype.sum_sum_type, kktMatrix, neg_eq_zero]
  simp only [↓reduceIte, Finset.sum_const_zero, ite_eq_right_iff, one_ne_zero, imp_false,
    ite_not, Finset.sum_ite_eq, Finset.mem_univ, zero_add]
  rw [two_mul, ← add_assoc]
  congr 2

theorem kktMatrix_sparsity [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (sr sc : ℕ)
    (hr : ∀ r, rowSupportCount (A r) ≤ sr)
    (hc : ∀ j, rowSupportCount (fun r => A r j) ≤ sc) :
    ∀ q, rowSupportCount (kktMatrix A q) ≤ max sr (2 * sc + 1) := by
  intro q
  cases q with
  | inl r => exact (kktMatrix_support_primal A r ▸ hr r).trans (le_max_left _ _)
  | inr j => rw [kktMatrix_support_dual]; have := hc j; omega

/-- Only the primal and two multiplier blocks contain dependent coefficients. -/
def kktDependent [Fintype R] [DecidableEq C] (D : R → Finset C) :
    (R ⊕ C) → Finset (KKTColumn R C)
  | Sum.inl r => (D r).disjSum ∅
  | Sum.inr j => (∅ : Finset C).disjSum
      ((transposePositions D j).disjSum ((transposePositions D j).disjSum ∅))

theorem kktDependent_card_primal [Fintype R] [DecidableEq C]
    (D : R → Finset C) (r : R) : (kktDependent D (Sum.inl r)).card = (D r).card := by
  simp [kktDependent]

theorem kktDependent_card_dual [Fintype R] [DecidableEq C]
    (D : R → Finset C) (j : C) :
    (kktDependent D (Sum.inr j)).card = 2 * (transposePositions D j).card := by
  simp [kktDependent, two_mul]

theorem transposePositions_card_sum [Fintype R] [Fintype C] [DecidableEq C]
    (D : R → Finset C) : ∑ j, (transposePositions D j).card = ∑ r, (D r).card := by
  classical
  simp only [transposePositions, Finset.card_eq_sum_ones, Finset.sum_filter]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro r _
  rw [← Finset.sum_filter]
  simp

theorem kktDependent_incidence [Fintype R] [Fintype C] [DecidableEq C]
    (D : R → Finset C) : totalIncidence (kktDependent D) = 3 * totalIncidence D := by
  simp only [totalIncidence, Fintype.sum_sum_type, kktDependent_card_primal,
    kktDependent_card_dual, ← Finset.mul_sum, transposePositions_card_sum]
  omega

def kktLabel (label : R → C → I) (defaultBit : I) : (R ⊕ C) → KKTColumn R C → I
  | Sum.inl r, Sum.inl j => label r j
  | Sum.inl _, Sum.inr _ => defaultBit
  | Sum.inr _, Sum.inl _ => defaultBit
  | Sum.inr j, Sum.inr (Sum.inl r) => label r j
  | Sum.inr j, Sum.inr (Sum.inr (Sum.inl r)) => label r j
  | Sum.inr _, Sum.inr (Sum.inr (Sum.inr _)) => defaultBit

theorem kktMatrix_locality [Fintype R] [DecidableEq C]
    (A : R → C → ℝ) (A' : I → R → C → ℝ) (D : R → Finset C)
    (label : R → C → I) (defaultBit : I)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    ∀ i r j, j ∉ kktDependent D r ∨ kktLabel label defaultBit r j ≠ i →
      kktMatrix (A' i) r j = kktMatrix A r j := by
  intro i r j h
  rcases r with r | q <;> rcases j with j | (r' | (r' | j))
  all_goals simp only [kktMatrix]
  all_goals first
  | rfl
  | apply hlocal; simpa [kktDependent, kktLabel, transposePositions] using h
  | congr 1; apply hlocal; simpa [kktDependent, kktLabel, transposePositions] using h

theorem kktDependent_sparsity [Fintype R] [DecidableEq C]
    (D : R → Finset C) (sr sc : ℕ)
    (hr : ∀ r, (D r).card ≤ sr)
    (hc : ∀ j, (transposePositions D j).card ≤ sc) :
    ∀ q, (kktDependent D q).card ≤ max sr (2 * sc + 1) := by
  intro q
  cases q with
  | inl r => rw [kktDependent_card_primal]; exact (hr r).trans (le_max_left _ _)
  | inr j => rw [kktDependent_card_dual]; have := hc j; omega

/-- Splitting and stacking realizes the same squared Euclidean residual. -/
theorem kktMatrix_sqNorm [Fintype R] [Fintype C] [DecidableEq C]
    (A : R → C → ℝ) (b : R → ℝ) (c x s : C → ℝ) (y : R → ℝ) :
    sqNorm (residual (kktMatrix A) (kktWitness x y s) (Sum.elim b c)) =
      kktSqResidual A b c x y s := by
  simp only [sqNorm, Fintype.sum_sum_type, kktMatrix_residual_primal,
    kktMatrix_residual_dual, kktSqResidual]

/-- Averaging split multipliers recovers the average signed multiplier. -/
theorem split_multiplier_mix_difference [Fintype I]
    (w : I → ℝ) (y : I → R → ℝ) (r : R) :
    mix w (fun i r => max (y i r) 0) r -
      mix w (fun i r => max (-y i r) 0) r = mix w y r := by
  simp only [mix, ← Finset.sum_sub_distrib, ← mul_sub, split_multiplier_difference]

end
end QipmFormal.Mixture
