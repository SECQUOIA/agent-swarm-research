import Mathlib
noncomputable section
namespace QuadraticPrecision

def squarePrefix : (L : ℕ) → (Fin L → ℝ) → ℝ
  | 0, _ => 0
  | L + 1, b => b 0 / 2 + squarePrefix L (fun i => b i.succ) / 2

def squareWidth (L : ℕ) : ℝ := (1 / 2 : ℝ) ^ L

def BinaryDigits {L : ℕ} (b : Fin L → ℝ) : Prop := ∀ i, b i = 0 ∨ b i = 1

@[simp] theorem squarePrefix_zero (b : Fin 0 → ℝ) : squarePrefix 0 b = 0 := rfl
@[simp] theorem squarePrefix_succ (L : ℕ) (b : Fin (L + 1) → ℝ) :
    squarePrefix (L + 1) b = b 0 / 2 + squarePrefix L (fun i => b i.succ) / 2 := rfl

theorem squareWidth_pos (L : ℕ) : 0 < squareWidth L := by unfold squareWidth; positivity
theorem squareWidth_le_one (L : ℕ) : squareWidth L ≤ 1 := by
  exact pow_le_one₀ (by norm_num) (by norm_num)
theorem squareWidth_succ (L : ℕ) : squareWidth (L + 1) = squareWidth L / 2 := by
  simp [squareWidth, pow_succ, div_eq_mul_inv]

theorem squarePrefix_mul (L : ℕ) (b : Fin L → ℝ) (x : ℝ) :
    squarePrefix L (fun i => b i * x) = squarePrefix L b * x := by
  induction L with
  | zero => simp
  | succ L ih => simp only [squarePrefix_succ, ih]; ring

theorem squarePrefix_add (L : ℕ) (b c : Fin L → ℝ) :
    squarePrefix L (b+c) = squarePrefix L b + squarePrefix L c := by
  induction L with
  | zero => simp
  | succ L ih =>
    change (b 0+c 0)/2 + squarePrefix L ((fun i => b i.succ)+(fun i => c i.succ))/2 = _
    rw [ih]
    simp only [squarePrefix_succ]
    ring

/-- Includes the right endpoint and the empty prefix. -/
theorem exists_squarePrefix (L : ℕ) (y : ℝ) (hy : y ∈ Set.Icc (0 : ℝ) 1) :
    ∃ b : Fin L → ℝ, ∃ r : ℝ, BinaryDigits b ∧ r ∈ Set.Icc 0 (squareWidth L) ∧
      y = squarePrefix L b + r := by
  induction L generalizing y with
  | zero => exact ⟨Fin.elim0, y, by simp [BinaryDigits], hy, by simp⟩
  | succ L ih =>
    by_cases h : y ≤ 1/2
    · obtain ⟨b,r,hb,hr,he⟩ := ih (2*y) ⟨by linarith [hy.1], by linarith⟩
      refine ⟨Fin.cons 0 b, r/2, ?_, ?_, ?_⟩
      · intro i; refine Fin.cases ?_ (fun j => ?_) i
        · exact Or.inl rfl
        · exact hb j
      · rw [squareWidth_succ]; exact ⟨by linarith [hr.1], by linarith [hr.2]⟩
      · simp [squarePrefix]; linarith
    · obtain ⟨b,r,hb,hr,he⟩ := ih (2*y-1) ⟨by linarith, by linarith [hy.2]⟩
      refine ⟨Fin.cons 1 b, r/2, ?_, ?_, ?_⟩
      · intro i; refine Fin.cases ?_ (fun j => ?_) i
        · exact Or.inr rfl
        · exact hb j
      · rw [squareWidth_succ]; exact ⟨by linarith [hr.1], by linarith [hr.2]⟩
      · simp [squarePrefix]; linarith

def BinaryProductRows (U b u v : ℝ) : Prop :=
  0 ≤ v ∧ v ≤ U*b ∧ v ≤ u ∧ u-U*(1-b) ≤ v

theorem binaryProductRows_exact {U b u v : ℝ} (hb : b = 0 ∨ b = 1)
    (h : BinaryProductRows U b u v) : v = b*u := by
  rcases hb with rfl | rfl <;> unfold BinaryProductRows at h <;> simp_all <;>
    linarith [h.1,h.2.1,h.2.2.1,h.2.2.2]

theorem binaryProductRows_graph {U b u : ℝ} (hb : b = 0 ∨ b = 1)
    (hu : u ∈ Set.Icc 0 U) : BinaryProductRows U b u (b*u) := by
  rcases hb with rfl | rfl <;> simp [BinaryProductRows] <;> constructor <;> linarith [hu.1,hu.2]

def SquareTriangle (h r q : ℝ) : Prop := 0 ≤ q ∧ 2*h*r-h^2 ≤ q ∧ q ≤ h*r

theorem squareTriangle_graph {h r : ℝ} (hr : r ∈ Set.Icc 0 h) :
    SquareTriangle h r (r^2) := by
  refine ⟨sq_nonneg _, ?_, ?_⟩
  · nlinarith [sq_nonneg (h-r)]
  · nlinarith [mul_nonneg hr.1 (sub_nonneg.mpr hr.2)]

theorem squareTriangle_error {h r q : ℝ} (hr : r ∈ Set.Icc 0 h)
    (hq : SquareTriangle h r q) : |q-r^2| ≤ h^2/4 := by
  rw [abs_le]
  unfold SquareTriangle at hq
  constructor
  · by_cases hh : r ≤ h/2
    · nlinarith [mul_nonneg hr.1 (by linarith : 0 ≤ h/2-r)]
    · nlinarith [mul_nonneg (sub_nonneg.mpr hr.2) (by linarith : 0 ≤ r-h/2)]
  · nlinarith [sq_nonneg (r-h/2)]
end QuadraticPrecision
