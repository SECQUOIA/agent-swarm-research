import Formal.MultilinearGap.ExactLaw
import Formal.MultilinearGap.StructuralFactorGaps

/-! Finite mixtures and exact averaging on the cardinality slabs. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {A B I : Type*} [Fintype A] [Fintype B] [Fintype I] [DecidableEq I]

omit [Fintype I] [DecidableEq I] in
theorem finiteMixture_expect (μ : Law A) (ν : A → Law B) (g : B → ℝ) :
    (finiteMixture μ ν).expect g = μ.expect (fun a => (ν a).expect g) := by
  exact expect_finiteMixture μ ν g

omit [Fintype B] in
theorem finiteMixture_hasMeans (μ : Law A) (ν : A → Law (Vertex I))
    (z : A → I → ℝ) (x : I → ℝ) (hz : ∀ a, HasMeans (ν a) (z a))
    (hx : ∀ i, μ.expect (fun a => z a i) = x i) :
    HasMeans (finiteMixture μ ν) x := by
  intro i
  rw [finiteMixture_expect]
  have he : (fun a => (ν a).expect (fun v => vertexPoint v i)) = (fun a => z a i) :=
    funext fun a => hz a i
  rw [he]
  exact hx i

omit [Fintype A] [Fintype B] [Fintype I] [DecidableEq I] in
/-- Consecutive-integer interpolation is affine on each closed unit slab,
including its upper integer endpoint. No convexity is needed for this identity. -/
theorem cardinalityLower_eq_chord_on_slab (φ : ℕ → ℝ) (s : Finset I)
    (x : I → ℝ) (k : ℕ) (hlo : (k : ℝ) ≤ meanSum s x)
    (hhi : meanSum s x ≤ (k : ℝ) + 1) :
    cardinalityLower φ s x =
      φ k + (meanSum s x - k) * (φ (k + 1) - φ k) := by
  have hn : 0 ≤ meanSum s x := le_trans (Nat.cast_nonneg k) hlo
  have hk : k ≤ countFloor s x := (Nat.le_floor_iff hn).mpr hlo
  have hf : countFloor s x ≤ k + 1 := by
    have h := (Nat.floor_le hn).trans hhi
    change ((countFloor s x : ℕ) : ℝ) ≤ (k : ℝ) + 1 at h
    exact_mod_cast h
  rcases (show countFloor s x = k ∨ countFloor s x = k + 1 by omega) with he | he
  · simp only [cardinalityLower, countFrac, he]
    ring
  · have hs : meanSum s x = (k : ℝ) + 1 := by
      have h := Nat.floor_le hn
      change (countFloor s x : ℝ) ≤ meanSum s x at h
      rw [he] at h
      push_cast at h
      linarith
    simp only [cardinalityLower, countFrac, he, hs, Nat.cast_add, Nat.cast_one]
    ring

omit [Fintype B] [Fintype I] [DecidableEq I] in
/-- A mixture staying in the mean's cardinality slab preserves the lower
endpoint exactly, rather than merely satisfying Jensen's inequality. -/
theorem cardinalityLower_average (φ : ℕ → ℝ) (s : Finset I)
    (μ : Law A) (z : A → I → ℝ) (x : I → ℝ) (hx : x ∈ cube I)
    (hmean : ∀ i, μ.expect (fun a => z a i) = x i)
    (hslab : ∀ a, (countFloor s x : ℝ) ≤ meanSum s (z a) ∧
      meanSum s (z a) ≤ (countFloor s x : ℝ) + 1) :
    μ.expect (fun a => cardinalityLower φ s (z a)) = cardinalityLower φ s x := by
  have hm : μ.expect (fun a => meanSum s (z a)) = meanSum s x := by
    simp only [meanSum, Law.expect, Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun i _ => hmean i
  have he a := cardinalityLower_eq_chord_on_slab φ s (z a) (countFloor s x)
    (hslab a).1 (hslab a).2
  simp_rw [he]
  rw [Law.expect_add, Law.expect_const, Law.expect_mul_const, Law.expect_sub,
    hm, Law.expect_const]
  exact (cardinalityLower_eq_chord_on_slab φ s x (countFloor s x)
    (countFloor_le hx) (Nat.lt_floor_add_one _).le).symm

omit [Fintype B] [Fintype I] in
/-- Upper graph-hull endpoints satisfy the required concavity averaging. -/
theorem upperEnvelope_average_le [Finite I] (f : (I → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (μ : Law A) (z : A → I → ℝ) (hz : ∀ a, z a ∈ cube I)
    (x : I → ℝ) (hmean : ∀ i, μ.expect (fun a => z a i) = x i) :
    μ.expect (fun a => sSup (envelopeValues f (z a))) ≤ sSup (envelopeValues f x) := by
  have h := (cube_concave_envelope f hf).1.le_map_sum
    (fun a (_ : a ∈ Finset.univ) => μ.nonneg a) μ.mass_one (fun a _ => hz a)
  have hb : (∑ a, μ.weight a • z a) = x := by
    funext i
    simpa [Law.expect, Finset.sum_apply] using hmean i
  rw [hb] at h
  exact h

variable {J : Type*} [Fintype J]

omit [Fintype B] in
/-- The expected sum of local cardinality gaps cannot exceed its value at the
mean when every support count stays in that mean's adjacent-count slab. -/
theorem cardinalityGaps_average_le
    (f : J → (I → ℝ) → ℝ) (hf : ∀ j, SeparatelyAffine (f j))
    (support : J → Finset I) (φ : J → ℕ → ℝ)
    (hφ : ∀ j, ConvexCountTable (φ j) (support j).card)
    (hv : ∀ j v, f j (vertexPoint v) = φ j (countOn (support j) v))
    (μ : Law A) (z : A → I → ℝ) (hz : ∀ a, z a ∈ cube I)
    (x : I → ℝ) (hx : x ∈ cube I)
    (hmean : ∀ i, μ.expect (fun a => z a i) = x i)
    (hslab : ∀ a j, (countFloor (support j) x : ℝ) ≤ meanSum (support j) (z a) ∧
      meanSum (support j) (z a) ≤ (countFloor (support j) x : ℝ) + 1) :
    μ.expect (fun a => ∑ j, hullGap (f j) (z a)) ≤ ∑ j, hullGap (f j) x := by
  rw [Law.expect_sum]
  apply Finset.sum_le_sum
  intro j _
  have hu := upperEnvelope_average_le (f j) (hf j) μ z hz x hmean
  have hl := cardinalityLower_average (φ j) (support j) μ z x hx hmean
    (fun a => hslab a j)
  have hi a := (cardinality_minimum (φ j) (support j) (hφ j) (f j) (hf j)
    (hv j) (z a) (hz a)).csInf_eq
  have hi' := (cardinality_minimum (φ j) (support j) (hφ j) (f j) (hf j)
    (hv j) x hx).csInf_eq
  simp only [hullGap, hi, hi', Law.expect_sub]
  rw [hl]
  linarith

omit [Fintype B] in
/-- Assemble local rounding losses after a degree-slab decomposition. The
rounding laws and slab decomposition remain explicit inputs of this lemma. -/
theorem cardinality_gap_of_slab_rounding
    (f : J → (I → ℝ) → ℝ) (hf : ∀ j, SeparatelyAffine (f j))
    (support : J → Finset I) (φ : J → ℕ → ℝ)
    (hφ : ∀ j, ConvexCountTable (φ j) (support j).card)
    (hv : ∀ j v, f j (vertexPoint v) = φ j (countOn (support j) v))
    (μ : Law A) (z : A → I → ℝ) (hz : ∀ a, z a ∈ cube I)
    (x : I → ℝ) (hx : x ∈ cube I)
    (hmean : ∀ i, μ.expect (fun a => z a i) = x i)
    (hslab : ∀ a j, (countFloor (support j) x : ℝ) ≤ meanSum (support j) (z a) ∧
      meanSum (support j) (z a) ≤ (countFloor (support j) x : ℝ) + 1)
    (ν : A → Law (Vertex I)) (hν : ∀ a, HasMeans (ν a) (z a))
    (η : ℝ) (hη : 0 ≤ η)
    (hloss : ∀ a, (ν a).expect (fun v => factorSum f (vertexPoint v)) ≤
      (∑ j, cardinalityLower (φ j) (support j) (z a)) +
        η * ∑ j, hullGap (f j) (z a)) :
    (1 - η) * (∑ j, hullGap (f j) x) ≤ hullGap (factorSum f) x := by
  have hupper := factorSum_maximum f hf x (thresholdLaw x) (thresholdLaw_hasMeans x hx)
    (fun j => by
      simpa only [hv] using cardinality_maximum (φ j) (support j) (hφ j)
        (f j) (hf j) (hv j) x hx)
  have hlow : μ.expect (fun a => ∑ j, cardinalityLower (φ j) (support j) (z a)) =
      ∑ j, cardinalityLower (φ j) (support j) x := by
    rw [Law.expect_sum]
    exact Finset.sum_congr rfl fun j _ => cardinalityLower_average (φ j) (support j)
      μ z x hx hmean (fun a => hslab a j)
  have havg := cardinalityGaps_average_le f hf support φ hφ hv μ z hz x hx hmean hslab
  have hround := μ.expect_mono hloss
  rw [Law.expect_add, Law.expect_const_mul, hlow] at hround
  have hround' := hround.trans (add_le_add_right (mul_le_mul_of_nonneg_left havg hη) _)
  apply factorSum_gap_of_law f hf x hupper (finiteMixture μ ν)
    (finiteMixture_hasMeans μ ν z x hν hmean) (1 - η)
  rw [finiteMixture_expect]
  have hid : (∑ j, hullGap (f j) x) =
      (∑ j, sSup (envelopeValues (f j) x)) -
        ∑ j, cardinalityLower (φ j) (support j) x := by
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun j _ => by
      rw [hullGap, (cardinality_minimum (φ j) (support j) (hφ j)
        (f j) (hf j) (hv j) x hx).csInf_eq]
  nlinarith

end
end MultilinearGap
