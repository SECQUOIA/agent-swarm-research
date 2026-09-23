import Mathlib

/-! Finite probability laws and their exact relation to convex hulls. -/

namespace CubicGap

structure Law (ι : Type*) [Fintype ι] where
  weight : ι → ℝ
  nonneg : ∀ i, 0 ≤ weight i
  mass_one : ∑ i, weight i = 1

namespace Law

variable {ι κ : Type*} [Fintype ι] [Fintype κ]

def expect (μ : Law ι) (f : ι → ℝ) : ℝ := ∑ i, μ.weight i * f i

def barycenter {E : Type*} [AddCommGroup E] [Module ℝ E]
    (μ : Law ι) (f : ι → E) : E := ∑ i, μ.weight i • f i

noncomputable def point (i : ι) : Law ι := by
  classical
  exact { weight := fun j => if j = i then 1 else 0
          nonneg := fun j => by split_ifs <;> norm_num
          mass_one := by simp }

noncomputable def mix (μ ν : Law ι) (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hab : a + b = 1) : Law ι where
  weight i := a * μ.weight i + b * ν.weight i
  nonneg i := add_nonneg (mul_nonneg ha (μ.nonneg i)) (mul_nonneg hb (ν.nonneg i))
  mass_one := by simp [Finset.sum_add_distrib, ← Finset.mul_sum, μ.mass_one, ν.mass_one, hab]

noncomputable def map (μ : Law ι) (f : ι → κ) : Law κ := by
  classical
  exact { weight := fun k => ∑ i, if f i = k then μ.weight i else 0
          nonneg := fun k => Finset.sum_nonneg fun i _ => by
            split_ifs
            · exact μ.nonneg i
            · exact le_rfl
          mass_one := by rw [Finset.sum_comm]; simpa using μ.mass_one }

@[simp] theorem expect_map (μ : Law ι) (f : ι → κ) (g : κ → ℝ) :
    (μ.map f).expect g = μ.expect (g ∘ f) := by
  classical
  simp only [expect, map, Finset.sum_mul]
  rw [Finset.sum_comm]
  congr 1
  funext i
  simp [ite_mul]

noncomputable def prod (μ : Law ι) (ν : Law κ) : Law (ι × κ) where
  weight i := μ.weight i.1 * ν.weight i.2
  nonneg i := mul_nonneg (μ.nonneg i.1) (ν.nonneg i.2)
  mass_one := by simp [Fintype.sum_prod_type, ← Finset.mul_sum, μ.mass_one, ν.mass_one]

@[simp] theorem expect_prod (μ : Law ι) (ν : Law κ) (f : ι × κ → ℝ) :
    (μ.prod ν).expect f = μ.expect (fun i => ν.expect (fun j => f (i, j))) := by
  simp [expect, prod, Fintype.sum_prod_type, Finset.mul_sum, mul_assoc]

noncomputable def uniform (ι : Type*) [Fintype ι] [Nonempty ι] : Law ι where
  weight _ := (Fintype.card ι : ℝ)⁻¹
  nonneg _ := inv_nonneg.mpr (Nat.cast_nonneg _)
  mass_one := by simp [Fintype.card_ne_zero]

@[simp] theorem expect_uniform [Nonempty ι] (f : ι → ℝ) :
    (uniform ι).expect f = (∑ i, f i) / Fintype.card ι := by
  simp only [expect, uniform, div_eq_mul_inv]
  rw [← Finset.mul_sum, mul_comm]

@[simp] theorem barycenter_point {E : Type*} [AddCommGroup E] [Module ℝ E]
    (i : ι) (f : ι → E) : (point i).barycenter f = f i := by
  classical
  simp [barycenter, point, ite_smul]

@[simp] theorem barycenter_mix {E : Type*} [AddCommGroup E] [Module ℝ E]
    (μ ν : Law ι) (a b : ℝ) (ha hb hab) (f : ι → E) :
    (mix μ ν a b ha hb hab).barycenter f = a • μ.barycenter f + b • ν.barycenter f := by
  simp [barycenter, mix, add_smul, mul_smul, Finset.sum_add_distrib, Finset.smul_sum]

/-- Finite laws describe the whole convex hull, including repeated points. -/
theorem mem_convexHull_range_iff {E : Type*} [AddCommGroup E] [Module ℝ E]
    (f : ι → E) (x : E) :
    x ∈ convexHull ℝ (Set.range f) ↔ ∃ μ : Law ι, μ.barycenter f = x := by
  constructor
  · intro hx
    apply convexHull_min (t := {x | ∃ μ : Law ι, μ.barycenter f = x}) ?_ ?_ hx
    · rintro _ ⟨i, rfl⟩
      exact ⟨point i, barycenter_point i f⟩
    · rintro x ⟨μ, rfl⟩ y ⟨ν, rfl⟩ a b ha hb hab
      exact ⟨mix μ ν a b ha hb hab, barycenter_mix μ ν a b ha hb hab f⟩
  · rintro ⟨μ, rfl⟩
    exact mem_convexHull_of_exists_fintype μ.weight f μ.nonneg μ.mass_one
      (fun i => Set.mem_range_self i) rfl

end Law

abbrev Vertex (I : Type*) := I → Bool

def vertexPoint {I : Type*} (v : Vertex I) (i : I) : ℝ := if v i then 1 else 0

def vertexGraph {I : Type*} (f : (I → ℝ) → ℝ) : Set ((I → ℝ) × ℝ) :=
  Set.range fun v : Vertex I => (vertexPoint v, f (vertexPoint v))

/-- A vertical slice of the graph hull is exactly the set of objectives attainable
by laws with the specified singleton means. -/
theorem mem_vertexGraph_hull_iff {I : Type*} [Fintype I] [DecidableEq I]
    (f : (I → ℝ) → ℝ) (x : I → ℝ) (z : ℝ) :
    (x, z) ∈ convexHull ℝ (vertexGraph f) ↔
      ∃ μ : Law (Vertex I), (∀ i, μ.expect (fun v => vertexPoint v i) = x i) ∧
        μ.expect (fun v => f (vertexPoint v)) = z := by
  rw [vertexGraph, Law.mem_convexHull_range_iff]
  constructor
  · rintro ⟨μ, hμ⟩
    refine ⟨μ, ?_, ?_⟩
    · intro i
      have h := congrArg (fun p => p.1 i) hμ
      simpa [Law.barycenter, Law.expect, Prod.fst_sum, Finset.sum_apply] using h
    · have h := congrArg Prod.snd hμ
      simpa [Law.barycenter, Law.expect, Prod.snd_sum] using h
  · rintro ⟨μ, hmean, hobj⟩
    refine ⟨μ, ?_⟩
    apply Prod.ext
    · ext i
      simpa [Law.barycenter, Law.expect, Prod.fst_sum, Finset.sum_apply] using hmean i
    · simpa [Law.barycenter, Law.expect, Prod.snd_sum] using hobj

end CubicGap
