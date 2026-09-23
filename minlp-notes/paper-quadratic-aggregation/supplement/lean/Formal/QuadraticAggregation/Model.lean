import Mathlib

/-!
# Quadratic systems and aggregation certificates

The variables and coefficients are real and finite dimensional. Hidden hyperplane
convexity is expressed using kernels of nonzero linear functionals. Asymptotic
hyperplane convexity uses arbitrarily large parameters; this is equivalent to the
increasing-sequence formulation in the source note.
-/

open scoped BigOperators Matrix
open Set Filter

namespace QuadraticAggregation

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

/-- Evaluation of a matrix quadratic form. -/
def q {n : ℕ} (A : Mat n) (x : Vec n) : ℝ := x ⬝ᵥ (A *ᵥ x)

structure System (n m : ℕ) where
  A : Fin m → Mat n
  symmetric : ∀ i, (A i).IsSymm
  b : Fin m → Vec n
  c : Fin m → ℝ

variable {n m : ℕ}

namespace System

def eval (D : System n m) (x : Vec n) (i : Fin m) : ℝ :=
  q (D.A i) x + 2 * (D.b i ⬝ᵥ x) + D.c i

def homEval (D : System n m) (z : Vec n × ℝ) (i : Fin m) : ℝ :=
  q (D.A i) z.1 + 2 * z.2 * (D.b i ⬝ᵥ z.1) + D.c i * z.2 ^ 2

def feasible (D : System n m) : Set (Vec n) := {x | ∀ i, D.eval x i < 0}

def closedFeasible (D : System n m) : Set (Vec n) := {x | ∀ i, D.eval x i ≤ 0}

def homFeasible (D : System n m) : Set (Vec n × ℝ) := {z | ∀ i, D.homEval z i < 0}

def aggA (D : System n m) (w : Vec m) : Mat n := ∑ i, w i • D.A i

def aggB (D : System n m) (w : Vec m) : Vec n := ∑ i, w i • D.b i

def aggC (D : System n m) (w : Vec m) : ℝ := ∑ i, w i * D.c i

/-- A nonzero nonnegative aggregation with positive semidefinite quadratic part
and a nonconstant aggregate polynomial. -/
def Certificate (D : System n m) (w : Vec m) : Prop :=
  (∀ i, 0 ≤ w i) ∧ w ≠ 0 ∧ (D.aggA w).PosSemidef ∧
    (D.aggA w ≠ 0 ∨ D.aggB w ≠ 0)

end System

/-- The sweeping hyperplane with normal `α` and parameter `s`. -/
def hyperplane (α : Vec n) (s : ℝ) : Set (Vec n × ℝ) :=
  {z | α ⬝ᵥ z.1 = s * z.2}

namespace System

def HHC (D : System n m) : Prop :=
  ∀ l : (Vec n × ℝ) →ₗ[ℝ] ℝ, l ≠ 0 →
    Convex ℝ (D.homEval '' (LinearMap.ker l : Set (Vec n × ℝ)))

def AsymptoticHC (D : System n m) : Prop :=
  ∀ α : Vec n, α ≠ 0 → ∀ R : ℝ, ∃ s : ℝ, R < s ∧
    Convex ℝ (D.homEval '' hyperplane α s)

@[simp] theorem homEval_one (D : System n m) (x : Vec n) :
    D.homEval (x, 1) = D.eval x := by
  ext i
  simp [homEval, eval]

@[simp] theorem homEval_zero (D : System n m) (x : Vec n) (i : Fin m) :
    D.homEval (x, 0) i = q (D.A i) x := by simp [homEval]

@[simp] theorem homEval_origin (D : System n m) : D.homEval (0, 0) = 0 := by
  ext i
  simp [homEval, q]

@[simp] theorem aggA_zero (D : System n m) : D.aggA 0 = 0 := by simp [aggA]
@[simp] theorem aggB_zero (D : System n m) : D.aggB 0 = 0 := by simp [aggB]
@[simp] theorem aggC_zero (D : System n m) : D.aggC 0 = 0 := by simp [aggC]

theorem continuous_eval (D : System n m) : Continuous D.eval := by
  unfold eval q Matrix.mulVec dotProduct
  fun_prop

theorem continuous_homEval (D : System n m) : Continuous D.homEval := by
  unfold homEval q Matrix.mulVec dotProduct
  fun_prop

theorem isOpen_feasible (D : System n m) : IsOpen D.feasible := by
  change IsOpen {x | ∀ i, D.eval x i < 0}
  simp only [Set.ofPred_forall]
  exact isOpen_iInter_of_finite fun i => isOpen_lt ((continuous_apply i).comp D.continuous_eval)
    continuous_const

theorem continuous_aggA (D : System n m) : Continuous D.aggA := by unfold aggA; fun_prop

theorem continuous_aggB (D : System n m) : Continuous D.aggB := by unfold aggB; fun_prop

theorem continuous_aggC (D : System n m) : Continuous D.aggC := by unfold aggC; fun_prop

theorem aggA_isSymm (D : System n m) (w : Vec m) : (D.aggA w).IsSymm := by
  apply Matrix.IsSymm.ext
  intro i j
  simp only [aggA, Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro k hk
  rw [(D.symmetric k).apply]

theorem agg_q (D : System n m) (w : Vec m) (x : Vec n) :
    q (D.aggA w) x = ∑ i, w i * q (D.A i) x := by
  simp [q, aggA, Matrix.sum_mulVec, Matrix.smul_mulVec, dotProduct_sum,
    dotProduct_smul]

theorem agg_dot (D : System n m) (w : Vec m) (x : Vec n) :
    D.aggB w ⬝ᵥ x = ∑ i, w i * (D.b i ⬝ᵥ x) := by
  simp [aggB, sum_dotProduct, smul_dotProduct]

theorem agg_eval (D : System n m) (w : Vec m) (x : Vec n) :
    ∑ i, w i * D.eval x i = q (D.aggA w) x + 2 * (D.aggB w ⬝ᵥ x) + D.aggC w := by
  rw [agg_q, agg_dot]
  simp only [eval, aggC, mul_add, Finset.sum_add_distrib, Finset.mul_sum]
  congr 1
  congr 1
  apply Finset.sum_congr rfl
  intro i hi
  ring

theorem agg_homEval (D : System n m) (w : Vec m) (z : Vec n × ℝ) :
    ∑ i, w i * D.homEval z i =
      q (D.aggA w) z.1 + 2 * z.2 * (D.aggB w ⬝ᵥ z.1) + D.aggC w * z.2 ^ 2 := by
  rw [agg_q, agg_dot]
  simp only [homEval, aggC, mul_add, Finset.sum_add_distrib, Finset.mul_sum,
    Finset.sum_mul]
  congr 1
  · congr 1
    apply Finset.sum_congr rfl
    intro i hi
    ring
  · apply Finset.sum_congr rfl
    intro i hi
    ring

theorem agg_eval_neg (D : System n m) {w : Vec m} (hw : ∀ i, 0 ≤ w i)
    (hw0 : w ≠ 0) {x : Vec n} (hx : x ∈ D.feasible) :
    ∑ i, w i * D.eval x i < 0 := by
  have hpos : ∃ i, 0 < w i := by
    by_contra! h
    apply hw0
    ext i
    exact le_antisymm (h i) (hw i)
  obtain ⟨i, hi⟩ := hpos
  exact Finset.sum_neg' (fun j _ => mul_nonpos_of_nonneg_of_nonpos (hw j) (hx j).le)
    ⟨i, Finset.mem_univ _, mul_neg_of_pos_of_neg hi (hx i)⟩

theorem trivial_aggC_neg (D : System n m) {w : Vec m} (hw : ∀ i, 0 ≤ w i)
    (hw0 : w ≠ 0) (hA : D.aggA w = 0) (hB : D.aggB w = 0)
    (hS : D.feasible.Nonempty) : D.aggC w < 0 := by
  obtain ⟨x, hx⟩ := hS
  have h := D.agg_eval_neg hw hw0 hx
  rw [D.agg_eval, hA, hB] at h
  simpa [q] using h

end System

/-- Linear functional defining a sweeping hyperplane. -/
def hyperplaneLinear (α : Vec n) (s : ℝ) : (Vec n × ℝ) →ₗ[ℝ] ℝ where
  toFun z := α ⬝ᵥ z.1 - s * z.2
  map_add' z w := by simp [dotProduct_add, mul_add]; ring
  map_smul' r z := by simp [dotProduct_smul]; ring

theorem hyperplaneLinear_ne_zero {α : Vec n} (hα : α ≠ 0) (s : ℝ) :
    hyperplaneLinear α s ≠ 0 := by
  intro h
  apply hα
  ext i
  have hi := LinearMap.congr_fun h (Pi.single i 1, 0)
  simpa [hyperplaneLinear, dotProduct_single] using hi

@[simp] theorem ker_hyperplaneLinear (α : Vec n) (s : ℝ) :
    (LinearMap.ker (hyperplaneLinear α s) : Set (Vec n × ℝ)) = hyperplane α s := by
  ext z
  simp [hyperplaneLinear, hyperplane, sub_eq_zero]

theorem System.HHC.asymptoticHC {D : System n m} (h : D.HHC) : D.AsymptoticHC := by
  intro α hα R
  refine ⟨R + 1, by linarith, ?_⟩
  simpa using h (hyperplaneLinear α (R + 1)) (hyperplaneLinear_ne_zero hα (R + 1))

end QuadraticAggregation

namespace QuadraticAggregation

open scoped BigOperators Matrix
open Set Filter

variable {n m : ℕ}

@[simp] theorem q_zero (A : Mat n) : q A 0 = 0 := by simp [q]
@[simp] theorem q_zero_matrix (x : Vec n) : q (0 : Mat n) x = 0 := by simp [q]

theorem q_smul (A : Mat n) (t : ℝ) (x : Vec n) :
    q A (t • x) = t ^ 2 * q A x := by
  simp [q, Matrix.mulVec_smul, smul_dotProduct, dotProduct_smul]
  ring

theorem q_add (A : Mat n) (hA : A.IsSymm) (x y : Vec n) :
    q A (x + y) = q A x + 2 * (x ⬝ᵥ (A *ᵥ y)) + q A y := by
  have hsym : y ⬝ᵥ (A *ᵥ x) = x ⬝ᵥ (A *ᵥ y) := by
    simpa only [hA.eq] using (Matrix.dotProduct_transpose_mulVec A x y).symm
  simp only [q, Matrix.mulVec_add, add_dotProduct, dotProduct_add]
  rw [hsym]
  ring

theorem System.eval_add_smul (D : System n m) (x v : Vec n) (t : ℝ) (i : Fin m) :
    D.eval (x + t • v) i =
      t ^ 2 * q (D.A i) v + 2 * t * (x ⬝ᵥ (D.A i *ᵥ v) + D.b i ⬝ᵥ v) + D.eval x i := by
  simp only [System.eval, q_add (D.A i) (D.symmetric i), q_smul,
    Matrix.mulVec_smul, dotProduct_smul, dotProduct_add]
  simp only [smul_eq_mul]
  ring

theorem System.homEval_smul (D : System n m) (z : Vec n × ℝ) (t : ℝ) :
    D.homEval (t • z) = t ^ 2 • D.homEval z := by
  ext i
  simp only [System.homEval, Prod.smul_fst, Prod.smul_snd, q_smul, dotProduct_smul,
    Pi.smul_apply, smul_eq_mul]
  ring

theorem System.homEval_eq_sq_mul_eval (D : System n m) (x : Vec n) {t : ℝ}
    (ht : t ≠ 0) (i : Fin m) :
    D.homEval (x, t) i = t ^ 2 * D.eval (t⁻¹ • x) i := by
  simp only [System.homEval, System.eval, q_smul, dotProduct_smul, smul_eq_mul]
  field_simp

theorem System.dehomogenize_mem (D : System n m) {x : Vec n} {t : ℝ}
    (ht : t ≠ 0) (hz : (x, t) ∈ D.homFeasible) : t⁻¹ • x ∈ D.feasible := by
  intro i
  have h := hz i
  rw [D.homEval_eq_sq_mul_eval x ht] at h
  exact neg_of_mul_neg_right h (sq_nonneg t)

theorem dot_dehomogenize {α x : Vec n} {s t : ℝ}
    (ht : t ≠ 0) (h : (x, t) ∈ hyperplane α s) : α ⬝ᵥ (t⁻¹ • x) = s := by
  change α ⬝ᵥ x = s * t at h
  rw [dotProduct_smul, smul_eq_mul, h]
  field_simp

end QuadraticAggregation
