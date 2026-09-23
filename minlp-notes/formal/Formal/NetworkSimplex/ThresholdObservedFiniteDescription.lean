import Formal.NetworkSimplex.ThresholdObservedCoefficients
import Formal.NetworkSimplex.ThresholdSmallDescription

/-! Complete finite unit descriptions after observed-label compression and pullback. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
noncomputable section
variable {m L : ℕ}

/-- A fixed finite family describes every real point of the same observation
pattern, including the complete original simplex constraints. -/
def FiniteUnitDescription (D : ReductionData m (Fin L)) : Prop :=
  ∃ n : ℕ, ∃ cuts : Fin n → AffineExpression (Coordinate m (Fin L)),
    (∀ k, UnitFlowProducts (cuts k)) ∧
    ∀ E : ReductionData m (Fin L), D.c = E.c → D.observedH = E.observedH →
      (E.graphPoint ∈ convexHull ℝ E.graph ↔
        ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))

/-- Reindexing a finite family does not change its inequalities or coefficients. -/
theorem finiteUnitDescription_of_family (D : ReductionData m (Fin L))
    {κ : Type*} [Finite κ] (cuts : κ → AffineExpression (Coordinate m (Fin L)))
    (hunit : ∀ k, UnitFlowProducts (cuts k))
    (hexact : ∀ E : ReductionData m (Fin L), D.c = E.c → D.observedH = E.observedH →
      (E.graphPoint ∈ convexHull ℝ E.graph ↔
        ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) :
    FiniteUnitDescription D := by
  let _ := Fintype.ofFinite κ
  let e := Fintype.equivFin κ
  refine ⟨Fintype.card κ, fun k => cuts (e.symm k), fun k => hunit (e.symm k), ?_⟩
  intro E hc hh
  rw [hexact E hc hh]
  exact e.symm.surjective.forall

/-- The already verified zero-, one-, two-, and three-label descriptions can
all be used through the same finite-index interface. -/
theorem small_finiteUnitDescription (D : ReductionData m (Fin L)) (hm : m ≤ 3)
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    FiniteUnitDescription D := by
  interval_cases m
  · obtain ⟨cuts, hu, he⟩ := zero_exists_full_finite_unit_description D hc hh
    exact finiteUnitDescription_of_family D cuts hu he
  · obtain ⟨cuts, hu, he⟩ := one_exists_full_finite_unit_description D hc hh
    exact finiteUnitDescription_of_family D cuts hu he
  · obtain ⟨cuts, hu, he⟩ := two_exists_full_finite_unit_description D hc hh
    exact finiteUnitDescription_of_family D cuts hu he
  · obtain ⟨cuts, hu, he⟩ := exists_full_finite_unit_description D hc hh
    exact finiteUnitDescription_of_family D cuts hu he

/-- Pull back a complete compressed family and append every original weight
nonnegativity inequality and both sides of the original simplex equality. -/
theorem observedPullback_finiteUnitDescription (D : ReductionData m (Fin L))
    (J : Finset (Fin m)) (hJ : D.CoversObservations J)
    (hcompressed : FiniteUnitDescription (D.compressObserved J)) :
    FiniteUnitDescription D := by
  obtain ⟨n, cuts, hu, he⟩ := hcompressed
  let family : Fin n ⊕ (Fin (m + 1) ⊕ Bool) →
      AffineExpression (Coordinate m (Fin L)) :=
    Sum.elim (fun k => observedPullback J (cuts k))
      (Sum.elim (fun j => .variable (.weight j))
        (fun b => if b then simplexExpression else .neg simplexExpression))
  apply finiteUnitDescription_of_family D family
  · intro k z hz
    rcases k with k | j | b
    · exact observedPullback_unit J (cuts k) (hu k) z hz
    · exact domainExpression_coefficient D (.weightLower j) z
    · cases b
      · change -1 ≤ -simplexExpression.coefficient z ∧ -simplexExpression.coefficient z ≤ 1
        have hb := simplexExpression_coefficient_unit z
        omega
      · exact simplexExpression_coefficient_unit z
  · intro E hc hh
    have hJE := hJ.of_pattern_eq hc hh
    have hp := D.compressObserved_pattern_eq E J hc hh
    rw [E.compressObserved_hull_iff J hJE, he (E.compressObserved J) hp.1 hp.2]
    constructor
    · rintro ⟨hw, hcuts⟩ k
      rcases k with k | j | b
      · change 0 ≤ (observedPullback J (cuts k)).eval (coordinates E E.xb)
        rw [observedPullback_eval]
        exact hcuts k
      · exact hw.1 j
      · have hs : simplexExpression.eval (coordinates E E.xb) = 0 := by
          rw [simplexExpression_eval, hw.2, sub_self]
        cases b <;> simp [family, AffineExpression.eval, hs]
    · intro hall
      have hp := hall (Sum.inr (Sum.inr true))
      have hn := hall (Sum.inr (Sum.inr false))
      change 0 ≤ simplexExpression.eval (coordinates E E.xb) at hp
      change 0 ≤ -simplexExpression.eval (coordinates E E.xb) at hn
      refine ⟨⟨fun j => hall (Sum.inr (Sum.inl j)), ?_⟩, ?_⟩
      · rw [simplexExpression_eval] at hp hn
        linarith
      · intro k
        have hk := hall (Sum.inl k)
        change 0 ≤ (observedPullback J (cuts k)).eval (coordinates E E.xb) at hk
        simpa only [observedPullback_eval] using hk

/-- At most three structurally observed explicit labels suffice, irrespective
of the number of additional unused labels or their zero/positive weights. -/
theorem observed_at_most_three_finite_unit_description
    (D : ReductionData m (Fin L)) (J : Finset (Fin m))
    (hJ : D.CoversObservations J) (hcard : J.card ≤ 3) :
    FiniteUnitDescription D := by
  apply observedPullback_finiteUnitDescription D J hJ
  exact small_finiteUnitDescription (D.compressObserved J) hcard (fun _ => rfl) rfl

end
end NetworkSimplex.Chain.Threshold
