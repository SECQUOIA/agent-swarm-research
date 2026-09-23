import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.LiftSmall
import Formal.InfiniteAggregation.HullModel

/-! # A finite semidefinite lift of the infinite-aggregation hull -/

open scoped BigOperators Matrix
open Set
noncomputable section
namespace InfiniteAggregation

/-- The two rows of original variables in the semidefinite lift. -/
def liftRows {r : ℕ} (x : Var r) : Matrix (Fin 2) (Fin r) ℝ :=
  fun i => if i = 0 then x.1 else x.2

/-- A symmetric affine matrix of size `r + 2`; its lower block is the identity. -/
def hullLift {r : ℕ} (x : Var r) (σ : ℝ) :
    Matrix (Fin 2 ⊕ Fin r) (Fin 2 ⊕ Fin r) ℝ :=
  Matrix.fromBlocks !![1, σ; σ, 1] (liftRows x) (liftRows x)ᴴ 1

/-- The Schur complement after eliminating the identity block. -/
def liftSlack {r : ℕ} (x : Var r) (σ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1 - qnorm x.1, σ - dot x.1 x.2; σ - dot x.1 x.2, 1 - qnorm x.2]

theorem lift_schur {r : ℕ} (x : Var r) (σ : ℝ) :
    !![1, σ; σ, 1] - liftRows x * (liftRows x)ᴴ = liftSlack x σ := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [liftRows, liftSlack, Matrix.mul_apply,
      qnorm, dot, dotProduct, mul_comm]

theorem hullLift_posSemidef_schur {r : ℕ} (x : Var r) (σ : ℝ) :
    (hullLift x σ).PosSemidef ↔ (liftSlack x σ).PosSemidef := by
  let _ : Invertible (1 : Matrix (Fin r) (Fin r) ℝ) := invertibleOne
  have h := Matrix.PosDef.fromBlocks₂₂ !![1, σ; σ, 1] (liftRows x)
    (Matrix.PosDef.one (n := Fin r) (R := ℝ))
  simpa only [hullLift, inv_one, Matrix.mul_one, lift_schur] using h

/-- The positive definite Schur criterion when the lower block is the identity. -/
theorem fromBlocks_one_posDef_iff {m n : Type*} [Finite m] [Fintype n]
    [DecidableEq n] (A : Matrix m m ℝ) (B : Matrix m n ℝ) :
    (Matrix.fromBlocks A B Bᴴ 1).PosDef ↔ (A - B * Bᴴ).PosDef := by
  let _ := Fintype.ofFinite m
  let _ : Invertible (1 : Matrix n n ℝ) := invertibleOne
  have hid : (1 : Matrix n n ℝ).IsHermitian := Matrix.PosDef.one.isHermitian
  have hform (x : m → ℝ) (y : n → ℝ) :
      (Sum.elim x y) ⬝ᵥ (Matrix.fromBlocks A B Bᴴ 1 *ᵥ Sum.elim x y) =
        (Bᴴ *ᵥ x + y) ⬝ᵥ (Bᴴ *ᵥ x + y) + x ⬝ᵥ ((A - B * Bᴴ) *ᵥ x) := by
    simpa only [star_trivial, inv_one, Matrix.one_mul, Matrix.mul_one,
      ← Matrix.dotProduct_mulVec, Matrix.one_mulVec] using
      Matrix.schur_complement_eq₂₂ A B x y hid
  have hherm := Matrix.IsHermitian.fromBlocks₂₂ A B hid
  simp only [inv_one, Matrix.mul_one] at hherm
  rw [Matrix.posDef_iff_dotProduct_mulVec, Matrix.posDef_iff_dotProduct_mulVec]
  simp only [star_trivial]
  constructor
  · rintro ⟨hH, hP⟩
    refine ⟨hherm.mp hH, fun x hx => ?_⟩
    have hne : Sum.elim x (-(Bᴴ *ᵥ x)) ≠ 0 := by
      intro h
      apply hx
      funext i
      exact congrFun h (.inl i)
    have h := hP hne
    simpa only [hform, add_neg_cancel, zero_dotProduct, zero_add] using h
  · rintro ⟨hH, hP⟩
    refine ⟨hherm.mpr hH, fun z hz => ?_⟩
    rw [← Sum.elim_comp_inl_inr z, hform]
    by_cases hx : z ∘ Sum.inl = 0
    · simp only [hx, Matrix.mulVec_zero, zero_add, zero_dotProduct, add_zero]
      have hy : z ∘ Sum.inr ≠ 0 := by
        intro hy
        apply hz
        funext i
        cases i with
        | inl i => exact congrFun hx i
        | inr i => exact congrFun hy i
      have h := Matrix.PosDef.one.dotProduct_mulVec_pos hy
      simpa only [star_trivial, Matrix.one_mulVec] using h
    · have hn := Matrix.PosSemidef.one.dotProduct_mulVec_nonneg
        (Bᴴ *ᵥ (z ∘ Sum.inl) + z ∘ Sum.inr)
      simp only [star_trivial, Matrix.one_mulVec] at hn
      exact add_pos_of_nonneg_of_pos hn (hP hx)

theorem hullLift_posDef_schur {r : ℕ} (x : Var r) (σ : ℝ) :
    (hullLift x σ).PosDef ↔ (liftSlack x σ).PosDef := by
  rw [hullLift, fromBlocks_one_posDef_iff, lift_schur]

theorem hullLift_affine {r : ℕ} (x y : Var r) (σ τ s t : ℝ) (hst : s + t = 1) :
    hullLift (s • x + t • y) (s * σ + t * τ) =
      s • hullLift x σ + t • hullLift y τ := by
  ext i j
  cases i with
  | inl i =>
    cases j with
    | inl j => fin_cases i <;> fin_cases j <;> simp [hullLift, Matrix.fromBlocks, hst]
    | inr j => fin_cases i <;> simp [hullLift, liftRows, Matrix.fromBlocks]
  | inr i =>
    cases j with
    | inl j => fin_cases j <;> simp [hullLift, liftRows, Matrix.fromBlocks]
    | inr j =>
      change (1 : Matrix (Fin r) (Fin r) ℝ) i j =
        s * (1 : Matrix (Fin r) (Fin r) ℝ) i j + t * (1 : Matrix (Fin r) (Fin r) ℝ) i j
      rw [← add_mul, hst, one_mul]

theorem hullLift_posSemidef_iff {r : ℕ} (x : Var r) (σ : ℝ) :
    (hullLift x σ).PosSemidef ↔
      GramPSD (1 - qnorm x.1) (1 - qnorm x.2) (σ - dot x.1 x.2) := by
  rw [hullLift_posSemidef_schur]
  exact gramMatrix_posSemidef_iff _ _ _

theorem hullLift_posDef_iff {r : ℕ} (x : Var r) (σ : ℝ) :
    (hullLift x σ).PosDef ↔
      0 < 1 - qnorm x.1 ∧ 0 < 1 - qnorm x.2 ∧
        (σ - dot x.1 x.2) ^ 2 < (1 - qnorm x.1) * (1 - qnorm x.2) := by
  rw [hullLift_posDef_schur]
  exact gramMatrix_posDef_iff _ _ _

/-- Eliminate the scalar lift variable, including singular Schur complements. -/
theorem exists_gramPSD_iff (p q c h : ℝ) :
    (∃ σ, h ≤ σ ∧ GramPSD p q (σ - c)) ↔
      0 ≤ p ∧ 0 ≤ q ∧ h ≤ c + Real.sqrt (p * q) := by
  constructor
  · rintro ⟨σ, hσ, hp, hq, hd⟩
    have hs := Real.sq_sqrt (mul_nonneg hp hq)
    have hn := Real.sqrt_nonneg (p * q)
    exact ⟨hp, hq, by nlinarith⟩
  · rintro ⟨hp, hq, hh⟩
    refine ⟨c + Real.sqrt (p * q), hh, hp, hq, ?_⟩
    simpa only [add_sub_cancel_left] using (Real.sq_sqrt (mul_nonneg hp hq)).le

/-- Eliminate the scalar lift variable in the positive definite case. -/
theorem exists_gramPD_iff (p q c h : ℝ) :
    (∃ σ, h < σ ∧ 0 < p ∧ 0 < q ∧ (σ - c) ^ 2 < p * q) ↔
      0 < p ∧ 0 < q ∧ h < c + Real.sqrt (p * q) := by
  constructor
  · rintro ⟨σ, hσ, hp, hq, hd⟩
    have hs := Real.sq_sqrt (mul_pos hp hq).le
    have hn := Real.sqrt_nonneg (p * q)
    exact ⟨hp, hq, by nlinarith⟩
  · rintro ⟨hp, hq, hh⟩
    have hs := Real.sqrt_pos.mpr (mul_pos hp hq)
    obtain ⟨σ, hlo, hhi⟩ := exists_between (max_lt hh (lt_add_of_pos_right c hs))
    refine ⟨σ, (le_max_left h c).trans_lt hlo, hp, hq, ?_⟩
    have hc : c < σ := (le_max_right h c).trans_lt hlo
    have he := Real.sq_sqrt (mul_pos hp hq).le
    nlinarith

/-- The closed formula is exactly the projection of one affine PSD constraint. -/
theorem mem_closedRegion_iff_lift {r : ℕ} (x : Var r) :
    x ∈ closedRegion r ↔ ∃ σ : ℝ, 1 / 2 ≤ σ ∧ (hullLift x σ).PosSemidef := by
  simp only [hullLift_posSemidef_iff, exists_gramPSD_iff, closedRegion, Set.mem_ofPred_eq]
  constructor <;> rintro ⟨h₁, h₂, h₃⟩ <;> exact ⟨by linarith, by linarith, h₃⟩

/-- The open formula is exactly the projection of the strict affine lift. -/
theorem mem_hullRegion_iff_lift {r : ℕ} (x : Var r) :
    x ∈ hullRegion r ↔ ∃ σ : ℝ, 1 / 2 < σ ∧ (hullLift x σ).PosDef := by
  simp only [hullLift_posDef_iff, exists_gramPD_iff, hullRegion, Set.mem_ofPred_eq]
  constructor <;> rintro ⟨h₁, h₂, h₃⟩ <;> exact ⟨by linarith, by linarith, h₃⟩

theorem convex_closedRegion {r : ℕ} : Convex ℝ (closedRegion r) := by
  intro x hx y hy s t hs ht hst
  obtain ⟨σ, hσ, hX⟩ := (mem_closedRegion_iff_lift x).mp hx
  obtain ⟨τ, hτ, hY⟩ := (mem_closedRegion_iff_lift y).mp hy
  apply (mem_closedRegion_iff_lift _).mpr
  refine ⟨s * σ + t * τ, ?_, ?_⟩
  · nlinarith [mul_nonneg hs (sub_nonneg.mpr hσ), mul_nonneg ht (sub_nonneg.mpr hτ)]
  · rw [hullLift_affine x y σ τ s t hst]
    exact (hX.smul hs).add (hY.smul ht)

theorem convex_hullRegion {r : ℕ} : Convex ℝ (hullRegion r) := by
  intro x hx y hy s t hs ht hst
  obtain ⟨σ, hσ, hX⟩ := (mem_hullRegion_iff_lift x).mp hx
  obtain ⟨τ, hτ, hY⟩ := (mem_hullRegion_iff_lift y).mp hy
  apply (mem_hullRegion_iff_lift _).mpr
  refine ⟨s * σ + t * τ, ?_, ?_⟩
  · have h := add_lt_add_of_lt_of_le (show 1 / 2 < min σ τ from lt_min hσ hτ)
      (show (0 : ℝ) ≤ 0 from le_refl _)
    have h1 := mul_nonneg hs (sub_nonneg.mpr (min_le_left σ τ))
    have h2 := mul_nonneg ht (sub_nonneg.mpr (min_le_right σ τ))
    nlinarith
  · rw [hullLift_affine x y σ τ s t hst]
    rcases eq_or_lt_of_le hs with hzero | hpos
    · have hs0 : s = 0 := hzero.symm
      have ht1 : t = 1 := by linarith
      simpa [hs0, ht1] using hY
    · exact (hX.smul hpos).add_posSemidef (hY.posSemidef.smul ht)

end InfiniteAggregation
