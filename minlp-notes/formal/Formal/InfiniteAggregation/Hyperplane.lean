import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.GramConcavity

noncomputable section

namespace InfiniteAggregation

open Matrix

/-- Every homogeneous functional has two vector coefficients and one scalar coefficient. -/
theorem hom_functional_coefficients {r : ℕ} (l : HomVar r →ₗ[ℝ] ℝ) :
    ∃ p q : Vec r, ∃ s : ℝ, ∀ z : HomVar r,
      l z = dot p z.1.1 + dot q z.1.2 + s * z.2 := by
  let lu : Vec r →ₗ[ℝ] ℝ := l.comp
    ((LinearMap.inl ℝ (Var r) ℝ).comp (LinearMap.inl ℝ (Vec r) (Vec r)))
  let lv : Vec r →ₗ[ℝ] ℝ := l.comp
    ((LinearMap.inl ℝ (Var r) ℝ).comp (LinearMap.inr ℝ (Vec r) (Vec r)))
  let p : Vec r := fun i => lu (fun j => if i = j then 1 else 0)
  let q : Vec r := fun i => lv (fun j => if i = j then 1 else 0)
  refine ⟨p, q, l ((0, 0), 1), ?_⟩
  intro ⟨⟨u, v⟩, t⟩
  have hlu : l ((u, 0), 0) = dot p u := by
    change lu u = dot p u
    rw [LinearMap.pi_apply_eq_sum_univ]
    simp only [dot, dotProduct, smul_eq_mul, p, mul_comm]
  have hlv : l ((0, v), 0) = dot q v := by
    change lv v = dot q v
    rw [LinearMap.pi_apply_eq_sum_univ]
    simp only [dot, dotProduct, smul_eq_mul, q, mul_comm]
  have ht : l ((0, 0), t) = l ((0, 0), 1) * t := by
    have hz : ((0, 0), t) = t • (((0, 0), 1) : HomVar r) := by simp
    rw [hz, map_smul]
    simp [mul_comm]
  have hz : (((u, v), t) : HomVar r) = ((u, 0), 0) + ((0, v), 0) + ((0, 0), t) := by
    simp
  rw [hz, map_add, map_add, hlu, hlv, ht]
  simp

/-- The three homogeneous quadratic values are a linear image of Gram coordinates. -/
def gramOutput : (Fin 4 → ℝ) →ₗ[ℝ] Weight where
  toFun g := ![g 0 - g 3, g 1 - g 3, g 3 / 2 - g 2]
  map_add' g h := by
    ext i
    fin_cases i <;> simp <;> ring
  map_smul' a g := by
    ext i
    fin_cases i <;> simp <;> ring

/-- Gram coordinates before applying the linear output map. -/
def homGram {r : ℕ} (z : HomVar r) : Fin 4 → ℝ :=
  ![qnorm z.1.1, qnorm z.1.2, dot z.1.1 z.1.2, z.2 ^ 2]

theorem gramOutput_homGram {r : ℕ} (z : HomVar r) :
    gramOutput (homGram z) = homEval z := by
  rfl

end InfiniteAggregation
