import Formal.NetworkSimplex.ThresholdGeneralSection
import Formal.NetworkSimplex.Disaggregation

/-! Affine descriptions restricted to two individual original product coordinates. -/
namespace NetworkSimplex
open scoped BigOperators
noncomputable section

variable {E J O : Type*} [Fintype E] [Fintype J] [Fintype O] [DecidableEq O]

structure AffineRow (E J O : Type*) where
  constant : ℝ
  flow : E → ℝ
  weight : J → ℝ
  product : O → ℝ

def AffineRow.eval (r : AffineRow E J O) (p : Point E J O) : ℝ :=
  r.constant + (∑ e, r.flow e * p.1 e) +
    (∑ j, r.weight j * p.2.1 j) + ∑ o, r.product o * p.2.2 o

/-- Change exactly two unscaled product coordinates and keep all others fixed. -/
def productSlice (p : Point E J O) (oU oV : O) (u v : ℝ) : Point E J O :=
  (p.1, p.2.1, fun o => p.2.2 o + (if o = oU then u else 0) + (if o = oV then v else 0))

theorem AffineRow.eval_productSlice (r : AffineRow E J O) (p : Point E J O)
    (oU oV : O) (u v : ℝ) :
    r.eval (productSlice p oU oV u v) = r.eval p + r.product oU * u + r.product oV * v := by
  unfold AffineRow.eval productSlice
  simp only [mul_add, Finset.sum_add_distrib, mul_ite, mul_zero]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
  ring

/-- The forced coefficients are original coordinate coefficients, with no rescaling. -/
theorem finite_description_product_ratio {ι κ : Type*} [Finite ι]
    (S : Set (Point E J O)) (p : Point E J O) (oU oV : O)
    {ε α β : ℝ} (hε : 0 < ε) (hα : 0 < α) (hβ : 0 < β)
    (hslice : ∀ u v, |u| < ε → |v| < ε →
      (productSlice p oU oV u v ∈ S ↔ 0 ≤ α * u + β * v))
    (rows : ι → AffineRow E J O) (eqs : κ → AffineRow E J O)
    (hd : ∀ q, q ∈ S ↔ (∀ i, 0 ≤ (rows i).eval q) ∧ (∀ j, (eqs j).eval q = 0)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ (rows i).eval p = 0 ∧
      (rows i).product oU = t * α ∧ (rows i).product oV = t * β := by
  apply local_halfplane_description_normal hε hα hβ
    (fun i => (rows i).product oU) (fun i => (rows i).product oV)
    (fun i => (rows i).eval p) (fun j => (eqs j).product oU)
    (fun j => (eqs j).product oV) (fun j => (eqs j).eval p)
  intro u v hu hv
  have h := hslice u v hu hv
  rw [hd] at h
  simpa only [AffineRow.eval_productSlice] using h

theorem valid_equation_product_coefficients (S : Set (Point E J O)) (p : Point E J O)
    (oU oV : O) {ε α β : ℝ} (hε : 0 < ε) (hα : 0 < α) (hβ : 0 < β)
    (hslice : ∀ u v, |u| < ε → |v| < ε →
      (productSlice p oU oV u v ∈ S ↔ 0 ≤ α * u + β * v))
    (r : AffineRow E J O) (hr : ∀ q ∈ S, r.eval q = 0) :
    r.product oU = 0 ∧ r.product oV = 0 := by
  have he := local_halfplane_equation_normal hε hα hβ (A := r.product oU)
    (B := r.product oV) (c := r.eval p) (by
      intro u v hu hv hedge
      rw [← r.eval_productSlice]
      exact hr _ ((hslice u v hu hv).mpr hedge))
  exact ⟨he.1, he.2.1⟩

end
end NetworkSimplex
