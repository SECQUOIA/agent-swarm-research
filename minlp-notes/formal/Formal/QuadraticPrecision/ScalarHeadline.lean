import Formal.QuadraticPrecision.PrecisionUpper
import Formal.QuadraticPrecision.LowerPrincipal
import Formal.QuadraticPrecision.LowerNegativeSlice
import Formal.QuadraticPrecision.LowerPositiveSlice
import Formal.QuadraticPrecision.SpectralConvex

/-! Scalar quadratic precision laws for actual original-box lifts. These
statements discharge the structural and construction premises of the general
count arithmetic, for every sufficiently small positive real accuracy. -/
namespace QuadraticPrecision
noncomputable section
variable {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}

theorem scalar_quadratic_graph_rank_law (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) (hr : 0 < H.rank) :
    HasPrecisionRate (fun ε => HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      H.rank ∧
    HasPrecisionRate (fun ε => HasBinaryGraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      H.rank := by
  obtain ⟨c,hc⟩ := graph_rank_lower H hH a l u b hlu hr
  constructor
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp
    · intro ε hε
      exact (quadratic_graph_binary_accuracy hH a l u b hε).toInteger
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp.toInteger
    · intro ε hε
      exact quadratic_graph_binary_accuracy hH a l u b hε

theorem scalar_quadratic_epigraph_inertia_law (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    HasPrecisionRate (fun ε => HasEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      (negativeInertia hH) ∧
    HasPrecisionRate (fun ε => HasBinaryEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      (negativeInertia hH) := by
  obtain ⟨c,hc⟩ := epigraph_negative_inertia_lower H hH a l u b hlu
  constructor
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp
    · intro ε hε
      exact (quadratic_epigraph_binary_accuracy hH a l u b hε).toInteger
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp.toInteger
    · intro ε hε
      exact quadratic_epigraph_binary_accuracy hH a l u b hε

theorem scalar_quadratic_hypograph_inertia_law (hH : H.IsHermitian)
    (a l u : Input n) (b : ℝ) (hlu : ∀ i, l i < u i) :
    HasPrecisionRate (fun ε => HasHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      (positiveInertia hH) ∧
    HasPrecisionRate (fun ε => HasBinaryHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε)
      (positiveInertia hH) := by
  obtain ⟨c,hc⟩ := hypograph_positive_inertia_lower H hH a l u b hlu
  constructor
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp
    · intro ε hε
      exact (quadratic_hypograph_binary_accuracy hH a l u b hε).toInteger
  · apply precisionRate_of_bounds _ _ (precisionWeight hH l u) c (precisionWeight_pos hH l u)
    · intro ε hε _ p hp
      exact hc ε hε p hp.toInteger
    · intro ε hε
      exact quadratic_hypograph_binary_accuracy hH a l u b hε

theorem scalar_quadratic_epigraph_zero_minimum (hH : H.IsHermitian)
    (hz : negativeInertia hH = 0) (a l u : Input n) (b : ℝ) {ε : ℝ} (hε : 0 < ε) :
    IsMinimumCount (HasEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε) 0 ∧
    IsMinimumCount (HasBinaryEpigraphLift (Set.Icc l u) (quadraticPolynomial H a b) ε) 0 := by
  have h := quadratic_epigraph_binary_accuracy hH a l u b hε
  rw [hz, Nat.zero_mul] at h
  exact ⟨⟨h.toInteger, fun _ _ => Nat.zero_le _⟩, ⟨h, fun _ _ => Nat.zero_le _⟩⟩

theorem scalar_quadratic_hypograph_zero_minimum (hH : H.IsHermitian)
    (hz : positiveInertia hH = 0) (a l u : Input n) (b : ℝ) {ε : ℝ} (hε : 0 < ε) :
    IsMinimumCount (HasHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε) 0 ∧
    IsMinimumCount (HasBinaryHypographLift (Set.Icc l u) (quadraticPolynomial H a b) ε) 0 := by
  have h := quadratic_hypograph_binary_accuracy hH a l u b hε
  rw [hz, Nat.zero_mul] at h
  exact ⟨⟨h.toInteger, fun _ _ => Nat.zero_le _⟩, ⟨h, fun _ _ => Nat.zero_le _⟩⟩

/-- Rank zero is the exact affine case, including an empty input dimension. -/
theorem scalar_quadratic_rank_zero_exact (hH : H.IsHermitian) (hz : H.rank = 0)
    (a l u : Input n) (b : ℝ) :
    IsMinimumCount (HasGraphLift (Set.Icc l u) (quadraticPolynomial H a b) 0) 0 ∧
    IsMinimumCount (HasBinaryGraphLift (Set.Icc l u) (quadraticPolynomial H a b) 0) 0 := by
  classical
  let f : Input n →ᵃ[ℝ] ℝ :=
    linearFunctional a + AffineMap.const ℝ _ b
  have heq : quadraticPolynomial H a b = f := by
    funext x
    change contactQuadratic H x + dotProduct a x + b = _
    have h := rank_zero_affine hH hz a x b
    simpa [f, contactQuadratic, dotProduct_comm] using h
  have hu := affine_has_zeroBinary_graph l u f
  rw [← heq] at hu
  exact ⟨⟨hu.toInteger, fun _ _ => Nat.zero_le _⟩, ⟨hu, fun _ _ => Nat.zero_le _⟩⟩

end
end QuadraticPrecision
