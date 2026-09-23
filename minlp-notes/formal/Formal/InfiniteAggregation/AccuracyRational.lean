import Formal.InfiniteAggregation.Good

/-! Exact integer coefficients and binary encoding size for the rational mesh. -/

noncomputable section
namespace InfiniteAggregation

def rationalLeftCoeff (m j : ℕ) : Fin 3 → ℕ := ![m ^ 2, j ^ 2, 2 * m * j]
def rationalRightCoeff (m j : ℕ) : Fin 3 → ℕ := ![j ^ 2, m ^ 2, 2 * m * j]
def rationalLeft (m j : ℕ) : Weight := fun i => rationalLeftCoeff m j i
def rationalRight (m j : ℕ) : Weight := fun i => rationalRightCoeff m j i

/-- The diagonal ray is counted once. -/
def rationalCuts (m : ℕ) : Finset Weight :=
  (Finset.range (m + 1)).image (rationalLeft m) ∪
    (Finset.range m).image (rationalRight m)

theorem rationalLeft_formula (m j : ℕ) :
    rationalLeft m j = ![(m : ℝ)^2, (j : ℝ)^2, 2 * m * j] := by
  ext i; fin_cases i <;> simp [rationalLeft, rationalLeftCoeff]

theorem rationalRight_formula (m j : ℕ) :
    rationalRight m j = ![(j : ℝ)^2, (m : ℝ)^2, 2 * m * j] := by
  ext i; fin_cases i <;> simp [rationalRight, rationalRightCoeff]

theorem rationalLeft_goodCone (m j : ℕ) : GoodCone (rationalLeft m j) := by
  constructor
  · intro i; exact Nat.cast_nonneg _
  · rw [rationalLeft_formula]
    change (2 * (m : ℝ) * j)^2 ≤ 4 * (m : ℝ)^2 * (j : ℝ)^2
    nlinarith [sq_nonneg ((m : ℝ) * j)]

theorem rationalRight_goodCone (m j : ℕ) : GoodCone (rationalRight m j) := by
  constructor
  · intro i; exact Nat.cast_nonneg _
  · rw [rationalRight_formula]
    change (2 * (m : ℝ) * j)^2 ≤ 4 * (j : ℝ)^2 * (m : ℝ)^2
    nlinarith [sq_nonneg ((m : ℝ) * j)]

theorem rationalLeft_ne_zero {m : ℕ} (hm : 0 < m) (j : ℕ) :
    rationalLeft m j ≠ 0 := by
  intro h
  have := congrFun h 0
  simp [rationalLeft, rationalLeftCoeff] at this
  omega

theorem rationalRight_ne_zero {m : ℕ} (hm : 0 < m) (j : ℕ) :
    rationalRight m j ≠ 0 := by
  intro h
  have := congrFun h 1
  simp [rationalRight, rationalRightCoeff] at this
  omega

theorem rationalLeft_injective {m : ℕ} (hm : 0 < m) :
    Function.Injective (rationalLeft m) := by
  intro j k h
  have hh := congrFun h 2
  simp [rationalLeft, rationalLeftCoeff] at hh
  omega

theorem rationalRight_injective {m : ℕ} (hm : 0 < m) :
    Function.Injective (rationalRight m) := by
  intro j k h
  have hh := congrFun h 2
  simp [rationalRight, rationalRightCoeff] at hh
  omega

theorem rationalCuts_card {m : ℕ} (hm : 0 < m) :
    (rationalCuts m).card = 2 * m + 1 := by
  have hd : Disjoint ((Finset.range (m + 1)).image (rationalLeft m))
      ((Finset.range m).image (rationalRight m)) := by
    apply Finset.disjoint_left.mpr
    intro w hw hv
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hw
    obtain ⟨k, hk, heq⟩ := Finset.mem_image.mp hv
    have hk' := Finset.mem_range.mp hk
    have heq' := congrFun heq 0
    have hh : k = m := by
      simpa [rationalLeft, rationalRight, rationalLeftCoeff, rationalRightCoeff] using heq'
    omega
  simp only [rationalCuts, Finset.card_union_of_disjoint hd,
    Finset.card_image_of_injective _ (rationalLeft_injective hm),
    Finset.card_image_of_injective _ (rationalRight_injective hm), Finset.card_range]
  omega

theorem rationalCuts_good {r m : ℕ} (hr : 2 ≤ r) (hm : 0 < m)
    {w : Weight} (hw : w ∈ rationalCuts m) : Good r w := by
  apply (good_iff_goodCone hr w).mpr
  rcases Finset.mem_union.mp hw with hl | hr
  · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hl
    exact ⟨rationalLeft_goodCone m j, rationalLeft_ne_zero hm j⟩
  · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hr
    exact ⟨rationalRight_goodCone m j, rationalRight_ne_zero hm j⟩

theorem rationalLeftCoeff_le {m j : ℕ} (hj : j ≤ m) (i : Fin 3) :
    rationalLeftCoeff m j i ≤ 2 * m ^ 2 := by
  fin_cases i <;> simp [rationalLeftCoeff] <;> nlinarith

theorem rationalRightCoeff_le {m j : ℕ} (hj : j ≤ m) (i : Fin 3) :
    rationalRightCoeff m j i ≤ 2 * m ^ 2 := by
  fin_cases i <;> simp [rationalRightCoeff] <;> nlinarith

/-- A genuine binary length bound, including the zero coefficient. -/
theorem coefficient_size_bound {N m c : ℕ} (hm : m ≤ N) (hc : c ≤ 2 * m ^ 2) :
    Nat.size c ≤ 2 * Nat.size N + 1 := by
  apply Nat.size_le.mpr
  have hN := Nat.lt_size_self N
  have hpow : 2 ^ (2 * Nat.size N + 1) = 2 * (2 ^ Nat.size N) ^ 2 := by
    rw [pow_add, show 2 * Nat.size N = Nat.size N * 2 by omega, pow_mul]; ring
  rw [hpow]
  nlinarith

theorem coefficient_log_bound {N m c : ℕ} (hm : m ≤ N) (hc : c ≤ 2 * m ^ 2) :
    Nat.size c ≤ 2 * Nat.log 2 N + 3 := by
  have hsize : Nat.size N ≤ Nat.log 2 N + 1 :=
    Nat.size_le.mpr (Nat.lt_pow_succ_log_self (by decide : 1 < 2) N)
  have := coefficient_size_bound hm hc
  omega

def rationalMeshSize (N : ℕ) : ℕ := (N - 1) / 2

theorem rationalMeshSize_pos {N : ℕ} (hN : 3 ≤ N) : 0 < rationalMeshSize N := by
  unfold rationalMeshSize; omega

theorem rationalMeshSize_le (N : ℕ) : rationalMeshSize N ≤ N := by
  unfold rationalMeshSize; omega

theorem rationalCuts_budget {N : ℕ} (hN : 3 ≤ N) :
    (rationalCuts (rationalMeshSize N)).card = 2 * rationalMeshSize N + 1 ∧
      (rationalCuts (rationalMeshSize N)).card ≤ N := by
  rw [rationalCuts_card (rationalMeshSize_pos hN)]
  unfold rationalMeshSize; omega

theorem rational_coefficients_bit_bound {N j : ℕ} (hj : j ≤ rationalMeshSize N)
    (i : Fin 3) :
    Nat.size (rationalLeftCoeff (rationalMeshSize N) j i) ≤ 2 * Nat.size N + 1 ∧
    Nat.size (rationalRightCoeff (rationalMeshSize N) j i) ≤ 2 * Nat.size N + 1 :=
  ⟨coefficient_size_bound (rationalMeshSize_le N) (rationalLeftCoeff_le hj i),
    coefficient_size_bound (rationalMeshSize_le N) (rationalRightCoeff_le hj i)⟩

theorem rationalCuts_integer_encoding {N : ℕ} {w : Weight}
    (hw : w ∈ rationalCuts (rationalMeshSize N)) :
    ∃ c : Fin 3 → ℕ, w = (fun i => (c i : ℝ)) ∧
      ∀ i, c i ≤ 2 * (rationalMeshSize N) ^ 2 ∧ Nat.size (c i) ≤ 2 * Nat.size N + 1 := by
  rcases Finset.mem_union.mp hw with hl | hr
  · obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hl
    have hj' : j ≤ rationalMeshSize N := by simpa using hj
    refine ⟨rationalLeftCoeff (rationalMeshSize N) j, rfl, fun i => ?_⟩
    exact ⟨rationalLeftCoeff_le hj' i, (rational_coefficients_bit_bound hj' i).1⟩
  · obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hr
    have hj' : j ≤ rationalMeshSize N := Nat.le_of_lt (Finset.mem_range.mp hj)
    refine ⟨rationalRightCoeff (rationalMeshSize N) j, rfl, fun i => ?_⟩
    exact ⟨rationalRightCoeff_le hj' i, (rational_coefficients_bit_bound hj' i).2⟩

theorem rationalCuts_log_encoding {N : ℕ} {w : Weight}
    (hw : w ∈ rationalCuts (rationalMeshSize N)) :
    ∃ c : Fin 3 → ℕ, w = (fun i => (c i : ℝ)) ∧
      ∀ i, c i ≤ 2 * (rationalMeshSize N)^2 ∧ Nat.size (c i) ≤ 2 * Nat.log 2 N + 3 := by
  obtain ⟨c, hc, hb⟩ := rationalCuts_integer_encoding hw
  exact ⟨c, hc, fun i => ⟨(hb i).1,
    coefficient_log_bound (rationalMeshSize_le N) (hb i).1⟩⟩

theorem rationalLeft_mem {m j : ℕ} (hj : j ≤ m) : rationalLeft m j ∈ rationalCuts m := by
  apply Finset.mem_union_left
  exact Finset.mem_image.mpr ⟨j, Finset.mem_range.mpr (by omega), rfl⟩

theorem rationalRight_mem {m j : ℕ} (hj : j ≤ m) : rationalRight m j ∈ rationalCuts m := by
  by_cases h : j = m
  · subst j
    have heq : rationalRight m m = rationalLeft m m := by
      rw [rationalRight_formula, rationalLeft_formula]
    rw [heq]
    exact rationalLeft_mem le_rfl
  · apply Finset.mem_union_right
    exact Finset.mem_image.mpr ⟨j, Finset.mem_range.mpr (by omega), rfl⟩

theorem rationalCuts_endpoints (m : ℕ) :
    rationalLeft m 0 ∈ rationalCuts m ∧ rationalRight m 0 ∈ rationalCuts m :=
  ⟨rationalLeft_mem (Nat.zero_le _), rationalRight_mem (Nat.zero_le _)⟩

/-- Distinct listed cuts also lie on distinct positive rays. -/
theorem rationalCuts_ray_unique {m : ℕ} (hm : 0 < m) {w v : Weight}
    (hw : w ∈ rationalCuts m) (hv : v ∈ rationalCuts m) {a : ℝ}
    (ha : 0 < a) (heq : w = a • v) : w = v := by
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have hms : (0 : ℝ) < (m : ℝ)^2 := sq_pos_of_pos hmR
  rcases Finset.mem_union.mp hw with hl | hr <;>
    rcases Finset.mem_union.mp hv with vl | vr
  · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hl
    obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp vl
    have h := congrFun heq 0
    simp only [rationalLeft_formula, Pi.smul_apply, smul_eq_mul,
      Matrix.cons_val_zero] at h
    have : a = 1 := by nlinarith
    simpa [this] using heq
  · obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hl
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp vr
    have hjR : (j : ℝ) ≤ m := by exact_mod_cast (Nat.le_of_lt_succ (Finset.mem_range.mp hj))
    have hkR : (k : ℝ) < m := by exact_mod_cast (Finset.mem_range.mp hk)
    have h0 := congrFun heq 0
    have h1 := congrFun heq 1
    simp only [rationalLeft_formula, rationalRight_formula, Pi.smul_apply,
      smul_eq_mul, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    have hs : (j : ℝ)^2 ≤ (m : ℝ)^2 := by nlinarith [Nat.cast_nonneg (α := ℝ) j]
    have ht : (k : ℝ)^2 < (m : ℝ)^2 := by nlinarith [Nat.cast_nonneg (α := ℝ) k]
    have := mul_lt_mul_of_pos_left ht ha
    exfalso; nlinarith
  · obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hr
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp vl
    have hjR : (j : ℝ) < m := by exact_mod_cast (Finset.mem_range.mp hj)
    have hkR : (k : ℝ) ≤ m := by exact_mod_cast (Nat.le_of_lt_succ (Finset.mem_range.mp hk))
    have h0 := congrFun heq 0
    have h1 := congrFun heq 1
    simp only [rationalLeft_formula, rationalRight_formula, Pi.smul_apply,
      smul_eq_mul, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    have hs : (j : ℝ)^2 < (m : ℝ)^2 := by nlinarith [Nat.cast_nonneg (α := ℝ) j]
    have ht : (k : ℝ)^2 ≤ (m : ℝ)^2 := by nlinarith [Nat.cast_nonneg (α := ℝ) k]
    have := mul_le_mul_of_nonneg_left ht ha.le
    exfalso; nlinarith
  · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hr
    obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp vr
    have h := congrFun heq 1
    simp only [rationalRight_formula, Pi.smul_apply, smul_eq_mul,
      Matrix.cons_val_one, Matrix.cons_val_zero] at h
    have : a = 1 := by nlinarith
    simpa [this] using heq

end InfiniteAggregation
