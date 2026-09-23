import Formal.QuadraticPrecision.LowerPullback
import Formal.QuadraticPrecision.ContactVolume
open scoped Matrix
namespace QuadraticPrecision
noncomputable def quadraticPolynomial {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (a : Fin d → ℝ) (b : ℝ) (x : Fin d → ℝ) : ℝ :=
  contactQuadratic M x + a ⬝ᵥ x + b

theorem quadratic_midpoint {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (a : Fin d → ℝ) (b : ℝ) (x y : Fin d → ℝ) :
    (quadraticPolynomial M a b x + quadraticPolynomial M a b y)/2 -
      quadraticPolynomial M a b ((1/2:ℝ) • x+(1/2:ℝ) • y) =
        contactQuadratic M (x-y)/4 := by
  simp only [quadraticPolynomial, contactQuadratic, Matrix.mulVec_add,
    Matrix.mulVec_smul, Matrix.mulVec_sub, add_dotProduct, dotProduct_add,
    smul_dotProduct, dotProduct_smul, sub_dotProduct, dotProduct_sub]
  ring

theorem continuous_quadraticPolynomial {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (a : Fin d → ℝ) (b : ℝ) : Continuous (quadraticPolynomial M a b) := by
  unfold quadraticPolynomial contactQuadratic Matrix.mulVec dotProduct
  fun_prop

theorem graph_quadratic_parity_cover {d p : ℕ} {D : Set (Input d)}
    (hD : IsCompact D) (M : Matrix (Fin d) (Fin d) ℝ) (a : Fin d → ℝ) (b ε : ℝ)
    (h : HasGraphLift D (quadraticPolynomial M a b) ε p) :
    ∃ S : ParityCode p → Set (Input d), (∀ α, IsCompact (S α)) ∧
      (∀ α, S α ⊆ D) ∧ (D ⊆ ⋃ α, S α) ∧
      ∀ α, ∀ x ∈ S α, ∀ y ∈ S α, |contactQuadratic M (x-y)| ≤ 4*ε := by
  obtain ⟨q,L,hL⟩ := h
  obtain ⟨S,hc,hs,hcover,he⟩ := L.graph_compact_parity_cover hD
    (continuous_quadraticPolynomial M a b) hL
  refine ⟨S,hc,hs,hcover,?_⟩
  intro α x hx y hy
  have hh := he α x hx y hy
  rw [quadratic_midpoint, abs_div] at hh
  norm_num at hh
  linarith

theorem epigraph_quadratic_parity_cover {d p : ℕ} {D : Set (Input d)}
    (hD : IsCompact D) (M : Matrix (Fin d) (Fin d) ℝ) (a : Fin d → ℝ) (b ε : ℝ)
    (h : HasEpigraphLift D (quadraticPolynomial M a b) ε p) :
    ∃ S : ParityCode p → Set (Input d), (∀ α, IsCompact (S α)) ∧
      (∀ α, S α ⊆ D) ∧ (D ⊆ ⋃ α, S α) ∧
      ∀ α, ∀ x ∈ S α, ∀ y ∈ S α, -contactQuadratic M (x-y) ≤ 4*ε := by
  obtain ⟨q,L,hL⟩ := h
  obtain ⟨S,hc,hs,hcover,he⟩ := L.epigraph_compact_parity_cover hD
    (continuous_quadraticPolynomial M a b) hL
  refine ⟨S,hc,hs,hcover,?_⟩
  intro α x hx y hy
  have hh := he α x hx y hy
  have hi := quadratic_midpoint M a b x y
  linarith
end QuadraticPrecision
