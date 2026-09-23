import QipmFormal.Coupling.LP
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! # The two sparse exact-center LP witnesses

The coupled center is parameterized by its second primal coordinate `t`, with
`μ = 2*t*(1-t)/(2-3*t)`. This avoids a removable radical singularity at zero.
All matrix inverses below are actual nonsingular matrix inverses.
-/
namespace QipmFormal.Coupling.Witnesses
noncomputable section
open Matrix Filter
open scoped Topology

def coupledA : Matrix (Fin 2) (Fin 3) ℝ := !![1, 1, 0; 0, 1, -1]
def decoupledA : Matrix (Fin 2) (Fin 3) ℝ := !![1, 0, 0; 0, 1, -1]
def rhs : Fin 2 → ℝ := ![1, 0]
def objective : Fin 3 → ℝ := ![0, 1, 1]
def centerParameter (t : ℝ) : ℝ := 2 * t * (1 - t) / (2 - 3 * t)
def coupledX (t : ℝ) : Fin 3 → ℝ := ![1 - t, t, t]
def coupledS (t : ℝ) : Fin 3 → ℝ :=
  ![centerParameter t / (1 - t), centerParameter t / t, centerParameter t / t]
def coupledY (t : ℝ) : Fin 2 → ℝ :=
  ![-centerParameter t / (1 - t), centerParameter t / t - 1]
def decoupledX (μ : ℝ) : Fin 3 → ℝ := ![1, μ, μ]
def decoupledS (μ : ℝ) : Fin 3 → ℝ := ![μ, 1, 1]
def decoupledY (μ : ℝ) : Fin 2 → ℝ := ![-μ, 0]

/-- The normal matrix of the LP, using the actual primal/slack ratio. -/
def normal (A : Matrix (Fin 2) (Fin 3) ℝ) (x s : Fin 3 → ℝ) :=
  normalMatrix A x s

theorem coupled_primal_feasible (t : ℝ) : coupledA *ᵥ coupledX t = rhs := by
  ext i; fin_cases i <;> simp [coupledA, coupledX, rhs, mulVec, dotProduct, Fin.sum_univ_succ]

theorem centerParameter_pos {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    0 < centerParameter t := by
  unfold centerParameter
  apply div_pos
  · exact mul_pos (mul_pos (by norm_num) ht) (by linarith)
  · linarith

theorem coupled_dual_feasible {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    coupledA.transpose *ᵥ coupledY t + coupledS t = objective := by
  have ht0 : t ≠ 0 := ne_of_gt ht
  have h1 : 1 - t ≠ 0 := by linarith
  have h2 : 2 - 3 * t ≠ 0 := by linarith
  have h2' : 2 - t * 3 ≠ 0 := by linarith
  ext i; fin_cases i <;>
    simp [coupledA, coupledY, coupledS, objective, mulVec, dotProduct,
      Fin.sum_univ_succ, centerParameter] <;> field_simp [ht0, h1, h2, h2'] <;> ring

theorem coupled_complementarity {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) (i : Fin 3) :
    coupledX t i * coupledS t i = centerParameter t := by
  have ht0 : t ≠ 0 := ne_of_gt ht
  have h1 : 1 - t ≠ 0 := by linarith
  fin_cases i <;> simp [coupledX, coupledS] <;> field_simp [ht0, h1]

theorem coupled_positive {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) (i : Fin 3) :
    0 < coupledX t i ∧ 0 < coupledS t i := by
  have hμ := centerParameter_pos ht hu
  have h1 : 0 < 1 - t := by linarith
  fin_cases i <;> simp [coupledX, coupledS, ht, h1, div_pos hμ ht, div_pos hμ h1]

theorem decoupled_center (μ : ℝ) :
    decoupledA *ᵥ decoupledX μ = rhs ∧
    decoupledA.transpose *ᵥ decoupledY μ + decoupledS μ = objective ∧
    (∀ i, decoupledX μ i * decoupledS μ i = μ) := by
  constructor
  · ext i; fin_cases i <;> simp [decoupledA, decoupledX, rhs, mulVec, dotProduct,
      Fin.sum_univ_succ]
  constructor
  · ext i; fin_cases i <;> simp [decoupledA, decoupledY, decoupledS, objective,
      mulVec, dotProduct, Fin.sum_univ_succ]
  · intro i; fin_cases i <;> simp [decoupledX, decoupledS]

theorem decoupled_positive {μ : ℝ} (hμ : 0 < μ) (i : Fin 3) :
    0 < decoupledX μ i ∧ 0 < decoupledS μ i := by
  fin_cases i <;> simp [decoupledX, decoupledS, hμ]

def coupledH (a c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a + c, c; c, 2 * c]
def decoupledH (μ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![μ⁻¹, 0; 0, 2 * μ]
def thetaOne (t : ℝ) := (1 - t) ^ 2 / centerParameter t
def theta (t : ℝ) := t ^ 2 / centerParameter t

theorem coupled_normal {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    normal coupledA (coupledX t) (coupledS t) = coupledH (thetaOne t) (theta t) := by
  have ht0 : t ≠ 0 := ne_of_gt ht
  have h1 : 1 - t ≠ 0 := by linarith
  have hμ : centerParameter t ≠ 0 := ne_of_gt (centerParameter_pos ht hu)
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [normal, normalMatrix, coupledA, coupledX, coupledS, coupledH, thetaOne, theta,
      Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_succ] <;> ring_nf <;> simp <;> ring

theorem decoupled_normal {μ : ℝ} (_hμ : μ ≠ 0) :
    normal decoupledA (decoupledX μ) (decoupledS μ) = decoupledH μ := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [normal, normalMatrix, decoupledA, decoupledX, decoupledS, decoupledH,
      Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_succ]
  ring

/-- An explicit inverse, checked by matrix multiplication. -/
theorem coupled_inverse {a c : ℝ} (hc : c ≠ 0) (hd : 2 * a + c ≠ 0) :
    (coupledH a c)⁻¹ =
      !![2 / (2 * a + c), -1 / (2 * a + c); -1 / (2 * a + c), (a + c) / (c * (2 * a + c))] := by
  have hd' : a * 2 + c ≠ 0 := by simpa [mul_comm] using hd
  apply Matrix.inv_eq_right_inv
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [coupledH, Matrix.mul_apply, Fin.sum_univ_succ] <;>
    field_simp [hc, hd] <;> ring

theorem coupled_first_inverse {a c : ℝ} (hc : c ≠ 0) (hd : 2 * a + c ≠ 0) :
    (coupledH a c)⁻¹ *ᵥ rhs = ![2 / (2 * a + c), -1 / (2 * a + c)] := by
  rw [coupled_inverse hc hd]
  ext i; fin_cases i <;> simp [rhs, mulVec, dotProduct, Fin.sum_univ_succ]

theorem coupled_second_inverse {a c : ℝ} (hc : c ≠ 0) (hd : 2 * a + c ≠ 0) :
    (coupledH a c)⁻¹ *ᵥ ((coupledH a c)⁻¹ *ᵥ rhs) =
      ![5 / (2 * a + c) ^ 2, -(a + 3 * c) / (c * (2 * a + c) ^ 2)] := by
  rw [coupled_first_inverse hc hd, coupled_inverse hc hd]
  ext i; fin_cases i <;> simp [mulVec, dotProduct, Fin.sum_univ_succ] <;>
    field_simp [hc, hd] <;> ring

theorem decoupled_inverse {μ : ℝ} (hμ : μ ≠ 0) :
    (decoupledH μ)⁻¹ = !![μ, 0; 0, (2 * μ)⁻¹] := by
  apply Matrix.inv_eq_right_inv
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [decoupledH, Matrix.mul_apply, Fin.sum_univ_succ, hμ]
  field_simp

theorem decoupled_inverse_rhs {μ : ℝ} (hμ : μ ≠ 0) :
    (decoupledH μ)⁻¹ *ᵥ rhs = ![μ, 0] ∧
    (decoupledH μ)⁻¹ *ᵥ ((decoupledH μ)⁻¹ *ᵥ rhs) = ![μ ^ 2, 0] := by
  rw [decoupled_inverse hμ]
  constructor <;> ext i <;> fin_cases i <;>
    simp [rhs, mulVec, dotProduct, Fin.sum_univ_succ, pow_two]


/-- Both constraint maps are onto, the full-row-rank assumption in concrete form. -/
theorem coupled_full_row_rank : Function.Surjective (coupledA.mulVec) := by
  intro v
  refine ⟨![v 0 - v 1, v 1, 0], ?_⟩
  ext i; fin_cases i <;> simp [coupledA, mulVec, dotProduct, Fin.sum_univ_succ]

theorem decoupled_full_row_rank : Function.Surjective (decoupledA.mulVec) := by
  intro v
  refine ⟨![v 0, v 1, 0], ?_⟩
  ext i; fin_cases i <;> simp [decoupledA, mulVec, dotProduct, Fin.sum_univ_succ]

/-- The row/column-two sparsity claim is a finite support count. -/
theorem witness_sparsity :
    (∀ i, (Finset.univ.filter (fun j => coupledA i j ≠ 0)).card ≤ 2) ∧
    (∀ j, (Finset.univ.filter (fun i => coupledA i j ≠ 0)).card ≤ 2) ∧
    (∀ i, (Finset.univ.filter (fun j => decoupledA i j ≠ 0)).card ≤ 2) ∧
    (∀ j, (Finset.univ.filter (fun i => decoupledA i j ≠ 0)).card ≤ 2) := by
  norm_num [coupledA, decoupledA, Fin.forall_fin_succ, Finset.filter_insert,
    Finset.filter_singleton, Fin.univ_succ]
  have h2 (x y z : ℝ) : (![x,y,z] : Fin 3 → ℝ) 2 = z := rfl
  simp only [h2]
  norm_num
  decide

/-- Nonnegative feasible points have nonnegative objective; objective zero forces e₁. -/
theorem coupled_unique_optimum (x : Fin 3 → ℝ)
    (hx : ∀ i, 0 ≤ x i) (hf : coupledA *ᵥ x = rhs) :
    0 ≤ objective ⬝ᵥ x ∧ (objective ⬝ᵥ x = 0 ↔ x = ![1, 0, 0]) := by
  have h0 := congrFun hf 0
  have h1 := congrFun hf 1
  simp [coupledA, rhs, mulVec, dotProduct, Fin.sum_univ_succ] at h0 h1
  have ho : objective ⬝ᵥ x = x 1 + x 2 := by
    simp [objective, dotProduct, Fin.sum_univ_succ]
  rw [ho]
  constructor
  · exact add_nonneg (hx 1) (hx 2)
  · constructor
    · intro hz
      have h2 : x 2 = 0 := by linarith [hx 1, hx 2]
      ext i; fin_cases i <;> simp <;> linarith
    · intro hz; simp [hz]

theorem decoupled_unique_optimum (x : Fin 3 → ℝ)
    (hx : ∀ i, 0 ≤ x i) (hf : decoupledA *ᵥ x = rhs) :
    0 ≤ objective ⬝ᵥ x ∧ (objective ⬝ᵥ x = 0 ↔ x = ![1, 0, 0]) := by
  have h0 := congrFun hf 0
  have h1 := congrFun hf 1
  simp [decoupledA, rhs, mulVec, dotProduct, Fin.sum_univ_succ] at h0 h1
  have ho : objective ⬝ᵥ x = x 1 + x 2 := by
    simp [objective, dotProduct, Fin.sum_univ_succ]
  rw [ho]
  constructor
  · exact add_nonneg (hx 1) (hx 2)
  · constructor
    · intro hz
      have h2 : x 2 = 0 := by linarith [hx 1, hx 2]
      ext i; fin_cases i <;> simp <;> linarith
    · intro hz; simp [hz]

/-- The center parameter satisfies the manuscript's quadratic equation. -/
theorem centerParameter_equation {t : ℝ} (hu : t < 2 / 3) :
    2 * t * (1 - t) = centerParameter t * (2 - 3 * t) := by
  have h : 2 - 3 * t ≠ 0 := by linarith
  simp [centerParameter, h]

/-- The rational parametrization agrees with the displayed radical branch. -/
theorem centerParameter_radical {t : ℝ} (_ht : 0 < t) (hu : t < 2 / 3) :
    t = (2 + 3 * centerParameter t -
      Real.sqrt (4 - 4 * centerParameter t + 9 * (centerParameter t) ^ 2)) / 4 := by
  have he := centerParameter_equation hu
  have hp : 0 < 2 + 3 * centerParameter t - 4 * t := by
    have hr : 2 + 3 * centerParameter t - 4 * t = (6 * t ^ 2 - 8 * t + 4) / (2 - 3 * t) := by
      unfold centerParameter
      have hn : 2 - t * 3 ≠ 0 := by linarith
      have hn' : 2 - 3 * t ≠ 0 := by linarith
      field_simp [hn, hn']
      ring
    rw [hr]
    apply div_pos
    · nlinarith [sq_nonneg (t - 2 / 3)]
    · linarith
  have hs : Real.sqrt (4 - 4 * centerParameter t + 9 * (centerParameter t) ^ 2) =
      2 + 3 * centerParameter t - 4 * t := by
    apply (Real.sqrt_eq_iff_mul_self_eq_of_pos hp).2
    nlinarith [he]
  rw [hs]
  ring

/-- Euclidean norm, rather than the default supremum norm on a function type. -/
def vectorNorm (v : Fin 2 → ℝ) : ℝ := ‖WithLp.toLp 2 v‖

theorem vectorNorm_pair (x y : ℝ) : vectorNorm ![x,y] = Real.sqrt (x ^ 2 + y ^ 2) := by
  simp [vectorNorm, EuclideanSpace.norm_eq, Fin.sum_univ_succ, Real.norm_eq_abs]

theorem coupled_first_norm {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    vectorNorm ((coupledH a c)⁻¹ *ᵥ rhs) = Real.sqrt 5 / (2 * a + c) := by
  have hd : 0 < 2 * a + c := by positivity
  rw [coupled_first_inverse (ne_of_gt hc) (ne_of_gt hd), vectorNorm_pair]
  have hr : (2 / (2 * a + c)) ^ 2 + (-1 / (2 * a + c)) ^ 2 = 5 / (2 * a + c) ^ 2 := by
    field_simp
    ring
  rw [hr, Real.sqrt_div (by norm_num), Real.sqrt_sq (le_of_lt hd)]

theorem coupled_normalized_direction {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    (vectorNorm ((coupledH a c)⁻¹ *ᵥ rhs))⁻¹ • ((coupledH a c)⁻¹ *ᵥ rhs) =
      ![2 / Real.sqrt 5, -1 / Real.sqrt 5] := by
  have hd : 0 < 2 * a + c := by positivity
  rw [coupled_first_norm ha hc, coupled_first_inverse (ne_of_gt hc) (ne_of_gt hd)]
  ext i; fin_cases i <;> simp <;> field_simp


/-- The original radical expression is defined for every positive μ. -/
def paperT (μ : ℝ) : ℝ := (2 + 3 * μ - Real.sqrt (4 - 4 * μ + 9 * μ ^ 2)) / 4

theorem paperT_domain {μ : ℝ} (hμ : 0 < μ) : 0 < paperT μ ∧ paperT μ < 2 / 3 := by
  have hd : 0 ≤ 4 - 4 * μ + 9 * μ ^ 2 := by nlinarith [sq_nonneg (3 * μ - 2 / 3)]
  have hs := Real.sq_sqrt hd
  have hn := Real.sqrt_nonneg (4 - 4 * μ + 9 * μ ^ 2)
  unfold paperT
  constructor
  · have hu : Real.sqrt (4 - 4 * μ + 9 * μ ^ 2) < 2 + 3 * μ := by nlinarith
    linarith
  · have hl : 3 * μ - 2 / 3 < Real.sqrt (4 - 4 * μ + 9 * μ ^ 2) := by nlinarith
    linarith

theorem paperT_parameter {μ : ℝ} (hμ : 0 < μ) : centerParameter (paperT μ) = μ := by
  have hd : 0 ≤ 4 - 4 * μ + 9 * μ ^ 2 := by nlinarith [sq_nonneg (3 * μ - 2 / 3)]
  have hs := Real.sq_sqrt hd
  have he : 2 * paperT μ * (1 - paperT μ) = μ * (2 - 3 * paperT μ) := by
    unfold paperT
    nlinarith
  have hn : 2 - 3 * paperT μ ≠ 0 := by have := (paperT_domain hμ).2; linarith
  unfold centerParameter
  exact (div_eq_iff hn).2 he

theorem paperT_tendsto_zero : Tendsto paperT (𝓝 0) (𝓝 0) := by
  have h : ContinuousAt paperT 0 := by unfold paperT; fun_prop
  convert h.tendsto using 1
  norm_num [paperT, Real.sqrt_eq_iff_eq_sq]

/-- A radical-free expression for t/μ, with its removable singularity resolved. -/
theorem paperT_ratio {μ : ℝ} (hμ : 0 < μ) :
    paperT μ / μ = 4 / (2 + 3 * μ + Real.sqrt (4 - 4 * μ + 9 * μ ^ 2)) := by
  have hd : 0 ≤ 4 - 4 * μ + 9 * μ ^ 2 := by nlinarith [sq_nonneg (3 * μ - 2 / 3)]
  have hs := Real.sq_sqrt hd
  have hn : 2 + 3 * μ + Real.sqrt (4 - 4 * μ + 9 * μ ^ 2) ≠ 0 := by positivity
  unfold paperT
  apply (div_eq_iff (ne_of_gt hμ)).2
  have he : 4 * (1 - μ) + μ ^ 2 * 9 = 4 - 4 * μ + 9 * μ ^ 2 := by ring
  have hs' := hs
  rw [← he] at hs'
  field_simp
  nlinarith only [hs']

/-- The primal and slack center limits identify the strict optimal partition. -/
theorem coupled_center_limits :
    Tendsto coupledX (𝓝 0) (𝓝 ![1,0,0]) ∧
    Tendsto (fun t => ![2 * t / (2 - 3 * t), 2 * (1 - t) / (2 - 3 * t), 2 * (1 - t) / (2 - 3 * t)])
      (𝓝 (0:ℝ)) (𝓝 ![0,1,1]) := by
  constructor
  · have h : ContinuousAt coupledX 0 := by
      apply continuousAt_pi.2
      intro i; fin_cases i <;> dsimp only [coupledX] <;> fun_prop
    simpa [coupledX] using h.tendsto
  · let f := fun t : ℝ => (![2 * t / (2 - 3 * t), 2 * (1 - t) / (2 - 3 * t),
        2 * (1 - t) / (2 - 3 * t)] : Fin 3 → ℝ)
    have h : ContinuousAt f 0 := by
      apply continuousAt_pi.2
      intro i; fin_cases i <;> dsimp only [f] <;> fun_prop (disch := norm_num)
    simpa [f] using h.tendsto

/-- Explicit slacks extend continuously to the strictly complementary limit. -/
theorem coupled_slack_regular {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    coupledS t = ![2 * t / (2 - 3 * t), 2 * (1 - t) / (2 - 3 * t), 2 * (1 - t) / (2 - 3 * t)] := by
  have h1 : 1 - t ≠ 0 := by linarith
  have h2 : 2 - 3 * t ≠ 0 := by linarith
  have h2' : 2 - t * 3 ≠ 0 := by linarith
  ext i; fin_cases i <;> simp [coupledS, centerParameter] <;> field_simp


theorem coupled_second_norm {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    vectorNorm ((coupledH a c)⁻¹ *ᵥ ((coupledH a c)⁻¹ *ᵥ rhs)) =
      Real.sqrt (25 * c ^ 2 + (a + 3 * c) ^ 2) / (c * (2 * a + c) ^ 2) := by
  have hd : 0 < 2 * a + c := by positivity
  have hd' : a * 2 + c ≠ 0 := by linarith
  rw [coupled_second_inverse (ne_of_gt hc) (ne_of_gt hd), vectorNorm_pair]
  have hr : (5 / (2 * a + c) ^ 2) ^ 2 + (-(a + 3 * c) / (c * (2 * a + c) ^ 2)) ^ 2 =
      (25 * c ^ 2 + (a + 3 * c) ^ 2) / (c * (2 * a + c) ^ 2) ^ 2 := by
    field_simp
    ring
  rw [hr, Real.sqrt_div (by positivity), Real.sqrt_sq (by positivity)]

theorem rhs_norm : vectorNorm rhs = 1 := by
  rw [rhs, vectorNorm_pair]
  norm_num

theorem decoupled_inverse_norms {μ : ℝ} (hμ : 0 < μ) :
    vectorNorm ((decoupledH μ)⁻¹ *ᵥ rhs) = μ ∧
    vectorNorm ((decoupledH μ)⁻¹ *ᵥ ((decoupledH μ)⁻¹ *ᵥ rhs)) = μ ^ 2 := by
  rw [(decoupled_inverse_rhs (ne_of_gt hμ)).2,
    (decoupled_inverse_rhs (ne_of_gt hμ)).1]
  simp only [vectorNorm_pair, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
    zero_pow, add_zero]
  constructor
  · exact Real.sqrt_sq (le_of_lt hμ)
  · exact Real.sqrt_sq (sq_nonneg μ)

/-- All dual optimal points, specified by feasibility and objective value zero. -/
theorem coupled_dual_optimal_interval (y : Fin 2 → ℝ) :
    ((∀ i, 0 ≤ objective i - (coupledA.transpose *ᵥ y) i) ∧ rhs ⬝ᵥ y = 0) ↔
    y 0 = 0 ∧ -1 ≤ y 1 ∧ y 1 ≤ 1 := by
  suffices h : (((y 0 ≤ 0 ∧ y 0 + y 1 ≤ 1 ∧ -y 1 ≤ 1) ∧ y 0 = 0) ↔
      y 0 = 0 ∧ -1 ≤ y 1 ∧ y 1 ≤ 1) by
    simpa [coupledA, objective, rhs, mulVec, dotProduct, Fin.sum_univ_succ,
      Fin.forall_fin_succ] using h
  constructor
  · rintro ⟨⟨_, h1, h2⟩, h0⟩
    exact ⟨h0, by linarith, by linarith⟩
  · rintro ⟨h0, hl, hu⟩
    exact ⟨⟨by linarith, by linarith, by linarith⟩, h0⟩

theorem decoupled_dual_optimal_interval (y : Fin 2 → ℝ) :
    ((∀ i, 0 ≤ objective i - (decoupledA.transpose *ᵥ y) i) ∧ rhs ⬝ᵥ y = 0) ↔
    y 0 = 0 ∧ -1 ≤ y 1 ∧ y 1 ≤ 1 := by
  suffices h : (((y 0 ≤ 0 ∧ y 1 ≤ 1 ∧ -y 1 ≤ 1) ∧ y 0 = 0) ↔
      y 0 = 0 ∧ -1 ≤ y 1 ∧ y 1 ≤ 1) by
    simpa [decoupledA, objective, rhs, mulVec, dotProduct, Fin.sum_univ_succ,
      Fin.forall_fin_succ] using h
  constructor
  · rintro ⟨⟨_, h1, h2⟩, h0⟩
    exact ⟨h0, by linarith, by linarith⟩
  · rintro ⟨h0, hl, hu⟩
    exact ⟨⟨by linarith, by linarith, by linarith⟩, h0⟩


/-- Strict complementarity holds at the explicitly identified limiting solution. -/
theorem witness_strict_limit :
    coupledA *ᵥ ![1,0,0] = rhs ∧ decoupledA *ᵥ ![1,0,0] = rhs ∧
    coupledA.transpose *ᵥ ![0,0] + ![0,1,1] = objective ∧
    decoupledA.transpose *ᵥ ![0,0] + ![0,1,1] = objective ∧
    (∀ i : Fin 3, (![1,0,0] : Fin 3 → ℝ) i * (![0,1,1] : Fin 3 → ℝ) i = 0 ∧
      0 < (![1,0,0] : Fin 3 → ℝ) i + (![0,1,1] : Fin 3 → ℝ) i) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simpa [coupledX] using coupled_primal_feasible 0
  · simpa [decoupledX] using (decoupled_center 0).1
  · ext i; fin_cases i <;> simp [coupledA, objective, mulVec, dotProduct,
      Fin.sum_univ_succ]
  · ext i; fin_cases i <;> simp [decoupledA, objective, mulVec, dotProduct,
      Fin.sum_univ_succ]
  · intro i; fin_cases i <;> norm_num

/-- Actual slacks on the radical central path converge to (0,1,1). -/
theorem coupled_slack_limit_mu :
    Tendsto (fun μ => coupledS (paperT μ)) (𝓝[>] 0) (𝓝 ![0,1,1]) := by
  have h := ((coupled_center_limits.2).comp paperT_tendsto_zero).mono_left
    (show 𝓝[>] (0:ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  exact (coupled_slack_regular (paperT_domain hμ).1 (paperT_domain hμ).2).symm

/-- The actual central dual converges to the midpoint of the dual-optimal interval. -/
theorem coupled_dual_limit_mu :
    Tendsto (fun μ => coupledY (paperT μ)) (𝓝[>] 0) (𝓝 ![0,0]) := by
  apply tendsto_pi_nhds.2
  intro i
  have hs := tendsto_pi_nhds.1 coupled_slack_limit_mu
  fin_cases i
  · simpa [coupledY, coupledS, neg_div] using (hs 0).neg
  · simpa [coupledY, coupledS] using (hs 1).sub_const 1


/-- A continuous expression for the second inverse along the center. -/
def secondRegular (t : ℝ) : Fin 2 → ℝ :=
  ![5 * (centerParameter t) ^ 2 / (2 * (1 - t) ^ 2 + t ^ 2) ^ 2,
    -(2 * (1 - t) / (2 - 3 * t)) ^ 2 * ((1 - t) ^ 2 + 3 * t ^ 2) / (2 * (1 - t) ^ 2 + t ^ 2) ^ 2]

theorem coupled_second_regular {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    (coupledH (thetaOne t) (theta t))⁻¹ *ᵥ
      ((coupledH (thetaOne t) (theta t))⁻¹ *ᵥ rhs) = secondRegular t := by
  have hμ := centerParameter_pos ht hu
  have h1 : 0 < 1 - t := by linarith
  have ha : 0 < thetaOne t := by unfold thetaOne; positivity
  have hc : 0 < theta t := by unfold theta; positivity
  have hd : 0 < 2 * thetaOne t + theta t := by positivity
  have h2 : 2 - 3 * t ≠ 0 := by linarith
  have h2' : 2 - t * 3 ≠ 0 := by linarith
  have hd0 : 2 * (1 - t) ^ 2 + t ^ 2 ≠ 0 := by positivity
  rw [coupled_second_inverse (ne_of_gt hc) (ne_of_gt hd)]
  ext i; fin_cases i <;>
    simp [secondRegular, thetaOne, theta, centerParameter] <;> field_simp
  ring

theorem secondRegular_limit : Tendsto secondRegular (𝓝 0) (𝓝 ![0,-1 / 4]) := by
  have h : ContinuousAt secondRegular 0 := by
    apply continuousAt_pi.2
    intro i; fin_cases i <;> dsimp only [secondRegular, centerParameter] <;>
      fun_prop (disch := norm_num)
  convert h.tendsto using 1
  norm_num [secondRegular, centerParameter]

/-- The displayed H⁻²b limit for the actual radical-parameterized normal matrix. -/
theorem coupled_second_limit_mu :
    Tendsto (fun μ =>
      (normal coupledA (coupledX (paperT μ)) (coupledS (paperT μ)))⁻¹ *ᵥ
        ((normal coupledA (coupledX (paperT μ)) (coupledS (paperT μ)))⁻¹ *ᵥ rhs))
      (𝓝[>] 0) (𝓝 ![0,-1 / 4]) := by
  have h := (secondRegular_limit.comp paperT_tendsto_zero).mono_left
    (show 𝓝[>] (0:ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  obtain ⟨ht, hu⟩ := paperT_domain hμ
  rw [coupled_normal ht hu, coupled_second_regular ht hu]
  rfl


/-- The O(μ²) expansion is obtained from a continuous quotient, without Taylor axioms. -/
theorem paperT_error_quotient :
    Tendsto (fun μ => (paperT μ - μ) / μ ^ 2) (𝓝[>] 0) (𝓝 (-1 / 2)) := by
  let f := fun μ : ℝ =>
    -(4 / (2 + 3 * μ + Real.sqrt (4 - 4 * μ + 9 * μ ^ 2))) ^ 2 /
      (2 - 3 * paperT μ)
  have hc : ContinuousAt f 0 := by
    dsimp only [f, paperT]
    fun_prop (disch := norm_num)
  have hzero : f 0 = -1 / 2 := by norm_num [f, paperT, Real.sqrt_eq_iff_eq_sq]
  have ht := hc.tendsto
  rw [hzero] at ht
  have hl := ht.mono_left (show 𝓝[>] (0:ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)
  apply hl.congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  have hp := paperT_domain hμ
  have he := centerParameter_equation hp.2
  rw [paperT_parameter hμ] at he
  have hn : 2 - 3 * paperT μ ≠ 0 := by linarith [hp.2]
  have hμ0 : μ ≠ 0 := ne_of_gt hμ
  have hn' : 2 - paperT μ * 3 ≠ 0 := by linarith [hp.2]
  dsimp only [f]
  rw [← paperT_ratio hμ]
  field_simp [hμ0, hn, hn']
  nlinarith [he]

theorem paperT_quadratic_error :
    Asymptotics.IsBigO (𝓝[>] (0:ℝ)) (fun μ => paperT μ - μ) (fun μ => μ ^ 2) := by
  apply Asymptotics.isBigO_of_div_tendsto_nhds ?_ (-1 / 2) paperT_error_quotient
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  intro hz
  have hpos : 0 < μ ^ 2 := by exact sq_pos_of_pos hμ
  exact False.elim (ne_of_gt hpos hz)

end
end QipmFormal.Coupling.Witnesses
