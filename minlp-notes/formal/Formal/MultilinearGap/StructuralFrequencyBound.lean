import Formal.MultilinearGap.StructuralFrequencyRounding
import Formal.MultilinearGap.StructuralAveraging

/-! Cardinality-gap bounds obtained from explicit odd-cycle slab layouts. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {V E A : Type*} [Fintype V] [Fintype E] [Fintype A]
  [DecidableEq E]

/-- Combine exact slab averaging with the cycle laws. The extraction of layouts
from frequency-two extreme points is a separate combinatorial theorem. -/
theorem cardinality_gap_of_cycle_layouts
    (S : V → Finset E) (φ : V → ℕ → ℝ)
    (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (μ : Law A) (z : A → E → ℝ) (hz : ∀ a, z a ∈ cube E)
    (x : E → ℝ) (hx : x ∈ cube E)
    (hmean : ∀ e, μ.expect (fun a => z a e) = x e)
    (hslab : ∀ a v, (countFloor (S v) x : ℝ) ≤ meanSum (S v) (z a) ∧
      meanSum (S v) (z a) ≤ (countFloor (S v) x : ℝ) + 1)
    (C : A → Type*) [∀ a, Finite (C a)]
    (D : ∀ a, FrequencyCycleLayout S (z a) (C a))
    (η : ℝ) (hη : 0 ≤ η)
    (hlen : ∀ a c, 1 / (2 * ((D a).size c : ℝ) + 3) ≤ η) :
    (1 - η) * (∑ v, hullGap (f v) x) ≤ hullGap (factorSum f) x := by
  classical
  let (a : A) : Fintype (C a) := Fintype.ofFinite (C a)
  exact cardinality_gap_of_slab_rounding f hf S φ hφ hv μ z hz x hx hmean hslab
    (fun a => (D a).law) (fun a => (D a).law_hasMeans) η hη
    (fun a => (D a).law_cardinality_loss (hz a) φ hφ f hf hv η hη (hlen a))

/-- Every odd cycle has length at least three, yielding the sharp 3/2 factor. -/
theorem cardinality_gap_three_halves_of_cycle_layouts
    (S : V → Finset E) (φ : V → ℕ → ℝ)
    (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (μ : Law A) (z : A → E → ℝ) (hz : ∀ a, z a ∈ cube E)
    (x : E → ℝ) (hx : x ∈ cube E)
    (hmean : ∀ e, μ.expect (fun a => z a e) = x e)
    (hslab : ∀ a v, (countFloor (S v) x : ℝ) ≤ meanSum (S v) (z a) ∧
      meanSum (S v) (z a) ≤ (countFloor (S v) x : ℝ) + 1)
    (C : A → Type*) [∀ a, Finite (C a)]
    (D : ∀ a, FrequencyCycleLayout S (z a) (C a)) :
    (∑ v, hullGap (f v) x) ≤ (3 / 2 : ℝ) * hullGap (factorSum f) x := by
  have h := cardinality_gap_of_cycle_layouts S φ hφ f hf hv μ z hz x hx hmean hslab
    C D (1/3) (by norm_num) (fun a c => by
      apply div_le_div_of_nonneg_left (by norm_num) (by norm_num)
      have := Nat.cast_nonneg (α := ℝ) ((D a).size c)
      linarith)
  linarith


/-- A lower bound on every odd-cycle length gives its corresponding sharp
odd-girth factor. The combinatorial girth certificate supplies `hlen`. -/
theorem cardinality_gap_girth_of_cycle_layouts
    (S : V → Finset E) (φ : V → ℕ → ℝ)
    (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (μ : Law A) (z : A → E → ℝ) (hz : ∀ a, z a ∈ cube E)
    (x : E → ℝ) (hx : x ∈ cube E)
    (hmean : ∀ e, μ.expect (fun a => z a e) = x e)
    (hslab : ∀ a v, (countFloor (S v) x : ℝ) ≤ meanSum (S v) (z a) ∧
      meanSum (S v) (z a) ≤ (countFloor (S v) x : ℝ) + 1)
    (C : A → Type*) [∀ a, Finite (C a)]
    (D : ∀ a, FrequencyCycleLayout S (z a) (C a))
    (g : ℝ) (hg : 1 < g) (hlen : ∀ a c, g ≤ 2 * ((D a).size c : ℝ) + 3) :
    (∑ v, hullGap (f v) x) ≤ g / (g - 1) * hullGap (factorSum f) x := by
  have hg0 : 0 < g := by linarith
  have h := cardinality_gap_of_cycle_layouts S φ hφ f hf hv μ z hz x hx hmean hslab
    C D (1/g) (by positivity) (fun a c =>
      div_le_div_of_nonneg_left (by norm_num) hg0 (hlen a c))
  have hmul := mul_le_mul_of_nonneg_left h hg0.le
  have hid : g * (1 - 1 / g) = g - 1 := by field_simp
  rw [← mul_assoc, hid] at hmul
  rw [div_mul_eq_mul_div]
  exact (le_div_iff₀ (show 0 < g-1 by linarith)).mpr (by nlinarith)

end
end MultilinearGap
