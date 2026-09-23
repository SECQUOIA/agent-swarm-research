import Formal.NetworkSimplex.ThresholdOneUnit
import Formal.NetworkSimplex.ThresholdUnitDescription

/-! Finite original-coordinate unit descriptions for the smaller circuit libraries.

Queries use the balanced chain coordinates `xb = 1 - xh - xa`. Unit bounds apply
to flow and product coefficients; state-weight coefficients are unrestricted.
-/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators

/-- A finite source-only branch family together with all original-domain margins. -/
abbrev SmallFullIndex {m n q L : ℕ} (D : ReductionData m (Fin L))
    (branch : ReductionData m (Fin L) → Fin q → (Fin n → ProfileRow m (Fin L)) → Prop) :=
  DomainRow m (Fin L) ⊕ (Bool ⊕
    ({r : ProfileRow m (Fin L) // normalVector (D.rowNormal r) = 0} ⊕
      (Σ c : Fin q, {r : Fin n → ProfileRow m (Fin L) // branch D c r})))

instance {m n q L : ℕ} (D : ReductionData m (Fin L))
    (branch : ReductionData m (Fin L) → Fin q → (Fin n → ProfileRow m (Fin L)) → Prop) :
    Finite (SmallFullIndex D branch) := by
  classical
  unfold SmallFullIndex
  infer_instance

private theorem rowNormal_pattern {m L : ℕ} (D E : ReductionData m (Fin L))
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (r : ProfileRow m (Fin L)) :
    D.rowNormal r = E.rowNormal r := by
  cases r <;> simp [ReductionData.rowNormal, hc, hh]

/-- Assemble a literal unit branch library and the domain inequalities into a
single fixed finite family, uniformly for all queries with this observation pattern. -/
theorem small_full_description {m n q L : ℕ} (D : ReductionData m (Fin L))
    (branch : ReductionData m (Fin L) → Fin q → (Fin n → ProfileRow m (Fin L)) → Prop)
    (weight : Fin q → Fin n → ℤ)
    (expr : ReductionData m (Fin L) → Fin q → (Fin n → ProfileRow m (Fin L)) →
      AffineExpression (Coordinate m (Fin L)))
    (hpattern : ∀ E, D.c = E.c → D.observedH = E.observedH →
      ∀ c r, branch D c r ↔ branch E c r)
    (hunit : ∀ c r, branch D c r → UnitFlowProducts (expr D c r))
    (heval : ∀ E, D.c = E.c → D.observedH = E.observedH →
      (∀ i, E.c i 0 = .neither) → ∀ c r,
      (expr D c r).eval (coordinates E E.xb) = ∑ k, (weight c k : ℝ) * E.rowRhs (r k))
    (hexact : ∀ E, (∀ i, E.c i 0 = .neither) → E.observedH 0 = false →
      (E.graphPoint ∈ convexHull ℝ E.graph ↔ E.OriginalDomain ∧
        (∀ r, normalVector (E.rowNormal r) = 0 → 0 ≤ E.rowRhs r) ∧
        ∀ c r, branch E c r → 0 ≤ ∑ k, (weight c k : ℝ) * E.rowRhs (r k)))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : SmallFullIndex D branch → AffineExpression (Coordinate m (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E, D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  let cuts : SmallFullIndex D branch → AffineExpression (Coordinate m (Fin L)) :=
    Sum.elim (domainExpression D) (Sum.elim
      (fun b => if b then simplexExpression else .neg simplexExpression)
      (Sum.elim (fun r => rowExpression D r.val) (fun p => expr D p.1 p.2.val)))
  refine ⟨cuts, ?_, ?_⟩
  · intro k z hz
    rcases k with d | b | r | p
    · exact domainExpression_coefficient D d z
    · cases b
      · change -1 ≤ -simplexExpression.coefficient z ∧ -simplexExpression.coefficient z ≤ 1
        have hu := simplexExpression_coefficient_unit z
        omega
      · exact simplexExpression_coefficient_unit z
    · exact row_flow_product_unit D r.val z hz
    · exact hunit p.1 p.2.val p.2.property z hz
  · intro E hp ho
    have hec : ∀ i, E.c i 0 = .neither := by rw [← hp]; exact hc
    have heh : E.observedH 0 = false := by rw [← ho]; exact hh
    have hrow (r : ProfileRow m (Fin L)) := rowExpression_eval_other D E E.xb hp ho hec r
    rw [hexact E hec heh, originalDomain_iff_fixed_domainExpressions D E hp ho hec heh]
    constructor
    · rintro ⟨⟨hd, hs⟩, hz, hb⟩ k
      rcases k with d | b | r | p
      · exact hd d
      · cases b <;> simp [cuts, AffineExpression.eval, hs]
      · change 0 ≤ (rowExpression D r.val).eval (coordinates E E.xb)
        rw [hrow]
        exact hz r.val (by rw [← rowNormal_pattern D E hp ho]; exact r.property)
      · change 0 ≤ (expr D p.1 p.2.val).eval (coordinates E E.xb)
        rw [heval E hp ho hec]
        exact hb p.1 p.2.val ((hpattern E hp ho _ _).mp p.2.property)
    · intro h
      have hpos := h (Sum.inr (Sum.inl true))
      have hneg := h (Sum.inr (Sum.inl false))
      change 0 ≤ simplexExpression.eval (coordinates E E.xb) at hpos
      change 0 ≤ -simplexExpression.eval (coordinates E E.xb) at hneg
      refine ⟨⟨fun d => h (Sum.inl d), by linarith⟩, ?_, ?_⟩
      · intro r hr
        have hrD : normalVector (D.rowNormal r) = 0 := by
          rw [rowNormal_pattern D E hp ho]; exact hr
        have hzero := h (Sum.inr (Sum.inr (Sum.inl ⟨r, hrD⟩)))
        change 0 ≤ (rowExpression D r).eval (coordinates E E.xb) at hzero
        simpa only [hrow] using hzero
      · intro c r hr
        have hrD := (hpattern E hp ho c r).mpr hr
        have hb := h (Sum.inr (Sum.inr (Sum.inr ⟨c, r, hrD⟩)))
        change 0 ≤ (expr D c r).eval (coordinates E E.xb) at hb
        simpa only [heval E hp ho hec] using hb

/-- All five actual two-label branches, together with the domain rows, give a
complete finite unit description in the original flow/product coordinates. -/
theorem two_exists_full_finite_unit_description {L : ℕ} (D : ReductionData 2 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : SmallFullIndex D TwoLabels.TwoBranch →
        AffineExpression (Coordinate 2 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E, D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  apply small_full_description D TwoLabels.TwoBranch TwoStateCircuits.weight
    TwoLabels.circuitExpression
  · intro E hp ho c r
    simp only [TwoLabels.TwoBranch, rowNormal_pattern D E hp ho]
  · exact fun c r hr z hz => TwoLabels.circuitExpression_unit D c r hr z hz
  · intro E hp ho hec c r
    have he : TwoLabels.circuitExpression D c r = TwoLabels.circuitExpression E c r := by
      simp only [TwoLabels.circuitExpression, rowExpression_eq_of_pattern_eq D E hp ho]
    rw [he]
    exact TwoLabels.circuitExpression_eval E c r E.xb hec
  · exact fun E hec heh => two_mem_hull_iff_source_tests E hec heh
  · exact hc
  · exact hh

/-- The actual one-label branch, together with the domain rows, give a
complete finite unit description in the original flow/product coordinates. -/
theorem one_exists_full_finite_unit_description {L : ℕ} (D : ReductionData 1 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : SmallFullIndex D OneBranch →
        AffineExpression (Coordinate 1 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E, D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  apply small_full_description D OneBranch OneStateCircuits.weight
    OneLabels.circuitExpression
  · intro E hp ho c r
    simp only [OneBranch, rowNormal_pattern D E hp ho]
  · exact fun c r hr z hz => OneLabels.circuitExpression_unit D c r hr z hz
  · intro E hp ho hec c r
    have he : OneLabels.circuitExpression D c r = OneLabels.circuitExpression E c r := by
      simp only [OneLabels.circuitExpression, rowExpression_eq_of_pattern_eq D E hp ho]
    rw [he]
    exact OneLabels.circuitExpression_eval E c r E.xb hec
  · exact fun E hec heh => one_mem_hull_iff_source_tests E hec heh
  · exact hc
  · exact hh

/-- With no explicit labels, every profile direction is zero. -/
theorem zero_mem_hull_iff_source_tests {L : ℕ} (D : ReductionData 0 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    D.graphPoint ∈ convexHull ℝ D.graph ↔ D.OriginalDomain ∧
      (∀ r, normalVector (D.rowNormal r) = 0 → 0 ≤ D.rowRhs r) := by
  rw [D.mem_hull_iff, D.exists_fullProfile_iff_rows hc hh]
  apply and_congr_right
  intro _
  constructor
  · rintro ⟨x, hx⟩ r _
    simpa [profileNormal_value_eq_dot] using hx r
  · intro h
    refine ⟨fun j => Fin.elim0 j, fun r => ?_⟩
    have hz : normalVector (D.rowNormal r) = 0 := by
      funext j
      exact Fin.elim0 j
    simpa [profileNormal_value_eq_dot] using h r hz

/-- The zero-label boundary also has a full finite original-coordinate unit
family. There are no circuit branches; the scalar source rows suffice. -/
theorem zero_exists_full_finite_unit_description {L : ℕ} (D : ReductionData 0 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : SmallFullIndex D
        (fun (_ : ReductionData 0 (Fin L)) (_ : Fin 0)
          (_ : Fin 0 → ProfileRow 0 (Fin L)) => False) →
        AffineExpression (Coordinate 0 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E, D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  apply small_full_description D _ (fun _ _ => 0) (fun _ _ _ => .constant 0)
  · intro E hp ho c
    exact Fin.elim0 c
  · intro c
    exact Fin.elim0 c
  · intro E hp ho hec c
    exact Fin.elim0 c
  · intro E hec heh
    simpa using zero_mem_hull_iff_source_tests E hec heh
  · exact hc
  · exact hh

end NetworkSimplex.Chain.Threshold
