import Formal.NetworkSimplex.ThresholdBoundedDescription
import Formal.NetworkSimplex.ThresholdUnitDescription

/-! The affine descriptions with independently supplied original b-arc coordinates. -/
namespace NetworkSimplex.Chain.Threshold

/-- Balance equations recover the eliminated b-flow coordinates exactly. -/
theorem oppositeFlow_eq_of_balance {m L : ℕ} (D : ReductionData m (Fin L))
    (xb : Fin L → ℝ) (hb : ∀ i, D.xa i + xb i + D.xh = 1) : xb = D.xb := by
  funext i
  dsimp [ReductionData.xb]
  linarith [hb i]

/-- The general description evaluates literal original-coordinate rows. The only
parameterization equation is the original unit-flow balance at each gadget. -/
theorem boundedDescription_ambient {m L : ℕ} (D E : ReductionData m (Fin L))
    (xb : Fin L → ℝ) (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hpattern : D.c = E.c) (hob : D.observedH = E.observedH)
    (hb : ∀ i, E.xa i + xb i + E.xh = 1) :
    chainPoint E.c E.u E.v E.weights E.xa xb E.xh
      (fun j => E.observedH j = true) E.zh ∈ convexHull ℝ E.graph ↔
      ∀ k, 0 ≤ (boundedDescription D k).eval (coordinates E xb) := by
  rw [oppositeFlow_eq_of_balance E xb hb]
  exact boundedDescription_exact D E hc hh hpattern hob

/-- The three-label finite unit family works on arbitrary original flow
coordinates after adjoining the actual gadget balance equations. -/
theorem exists_unit_ambient_description {L : ℕ} (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : FullUnitDescriptionIndex D → AffineExpression (Coordinate 3 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E : ReductionData 3 (Fin L), ∀ xb : Fin L → ℝ,
        D.c = E.c → D.observedH = E.observedH →
        (∀ i, E.xa i + xb i + E.xh = 1) →
        (chainPoint E.c E.u E.v E.weights E.xa xb E.xh
          (fun j => E.observedH j = true) E.zh ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E xb))) := by
  obtain ⟨cuts, hu, he⟩ := exists_full_finite_unit_description D hc hh
  refine ⟨cuts, hu, ?_⟩
  intro E xb hp ho hb
  rw [oppositeFlow_eq_of_balance E xb hb]
  exact he E hp ho

/-- Both signs of every balance equation have unit flow/product coefficients. -/
theorem balanceExpression_unit {m : ℕ} {I : Type*} [DecidableEq I]
    (i : I) (z : Coordinate m I) :
    -1 ≤ (balanceExpression i).coefficient z ∧ (balanceExpression i).coefficient z ≤ 1 := by
  cases z <;> simp [balanceExpression, AffineExpression.coefficient] <;>
    split_ifs <;> norm_num

end NetworkSimplex.Chain.Threshold
