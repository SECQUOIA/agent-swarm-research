import Formal.NetworkSimplex.ThresholdFlowRepresentative
import Formal.NetworkSimplex.ThresholdProductCoefficients
import Formal.NetworkSimplex.ThresholdSourceGrouping
import Formal.NetworkSimplex.ThresholdDomainRows

/-! A finite original-coordinate unit description, fixed across all queries of one pattern. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
variable {I : Type*} [DecidableEq I]

/-- State-weight coefficients are unrestricted; every flow/product coefficient is unit. -/
def UnitFlowProducts {m : ℕ} (e : AffineExpression (Coordinate m I)) : Prop :=
  ∀ z, FlowOrProduct z → -1 ≤ e.coefficient z ∧ e.coefficient z ≤ 1

/-- Each actual three-label branch has a unit affine representative, obtained using
zero or one actual gadget balance equation. -/
theorem exists_unit_representative (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r) :
    ∃ e : AffineExpression (Coordinate 3 I),
      (e = circuitExpression D c r ∨
        ∃ i s, e = balanceRepair (circuitExpression D c r) i s) ∧
      (∀ x, (∀ i, (balanceExpression i).eval x = 0) →
        e.eval x = (circuitExpression D c r).eval x) ∧ UnitFlowProducts e := by
  obtain ⟨e, hshape, heval, hflow, hnon⟩ := exists_unit_flow_representative D hr
  refine ⟨e, hshape, heval, fun z hz => ?_⟩
  cases z with
  | bypassFlow => exact hflow.1
  | aFlow i => exact hflow.2.1 i
  | bFlow i => exact hflow.2.2 i
  | aProduct i j =>
    rw [hnon (.aProduct i j) trivial]
    exact threeBranch_aProduct_unit D c r hr i j
  | bProduct i j =>
    rw [hnon (.bProduct i j) trivial]
    exact threeBranch_bProduct_unit D c r hr i j
  | bypassProduct j =>
    rw [hnon (.bypassProduct j) trivial]
    exact threeBranch_bypassProduct_unit D c r hr j
  | weight j => exact False.elim hz

/-- The finite family consists of scalar zero rows and actual circuit branches. -/
abbrev UnitDescriptionIndex (D : ReductionData 3 I) :=
  {r : ProfileRow 3 I // normalVector (D.rowNormal r) = 0} ⊕
    (Σ c : Fin 16, {r : Fin 11 → ProfileRow 3 I // ThreeBranch D c r})

instance [Finite I] (D : ReductionData 3 I) : Finite (UnitDescriptionIndex D) := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  unfold UnitDescriptionIndex
  infer_instance

omit [DecidableEq I] in
private theorem rowNormal_eq_of_pattern_eq (D E : ReductionData 3 I)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (r : ProfileRow 3 I) :
    D.rowNormal r = E.rowNormal r := by
  cases r <;> simp [ReductionData.rowNormal, hc, hh]

omit [DecidableEq I] in
private theorem threeBranch_pattern_iff (D E : ReductionData 3 I)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) : ThreeBranch D c r ↔ ThreeBranch E c r := by
  simp only [ThreeBranch, rowNormal_eq_of_pattern_eq D E hc hh]

/-- Fixing the observation pattern fixes one finite unit inequality family that is
exact for every original-coordinate query. Original-domain checks remain separate. -/
theorem exists_finite_unit_description {L : ℕ} (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : UnitDescriptionIndex D → AffineExpression (Coordinate 3 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E : ReductionData 3 (Fin L), D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔ E.OriginalDomain ∧
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  classical
  have hex (c : Fin 16) (r : Fin 11 → ProfileRow 3 (Fin L)) (hr : ThreeBranch D c r) :=
    exists_unit_representative D hr
  let branchCut (c : Fin 16) (r : Fin 11 → ProfileRow 3 (Fin L)) (hr : ThreeBranch D c r) :=
    (hex c r hr).choose
  have hbranch (c : Fin 16) (r : Fin 11 → ProfileRow 3 (Fin L)) (hr : ThreeBranch D c r) :=
    (hex c r hr).choose_spec
  let cuts : UnitDescriptionIndex D → AffineExpression (Coordinate 3 (Fin L)) :=
    Sum.elim (fun r => rowExpression D r.val) (fun p => branchCut p.1 p.2.val p.2.property)
  refine ⟨cuts, ?_, ?_⟩
  · intro k
    cases k with
    | inl r => exact fun z hz => row_flow_product_unit D r.val z hz
    | inr p => exact (hbranch p.1 p.2.val p.2.property).2.2
  · intro E hclasses hbypass
    have hec : ∀ i, E.c i 0 = .neither := by rw [← hclasses]; exact hc
    have heh : E.observedH 0 = false := by rw [← hbypass]; exact hh
    have hbal (i : Fin L) : (balanceExpression i).eval (coordinates E E.xb) = 0 := by
      apply balanceExpression_eval
      simp [ReductionData.xb]
    have hrow (r : ProfileRow 3 (Fin L)) :
        (rowExpression D r).eval (coordinates E E.xb) = E.rowRhs r :=
      rowExpression_eval_other D E E.xb hclasses hbypass hec r
    have hcut (c : Fin 16) (r : Fin 11 → ProfileRow 3 (Fin L)) (hr : ThreeBranch D c r) :
        (branchCut c r hr).eval (coordinates E E.xb) =
          ∑ k, (ThreeStateCircuits.weight c k : ℝ) * E.rowRhs (r k) := by
      rw [(hbranch c r hr).2.1 _ hbal, circuitExpression_eval]
      simp only [hrow]
    rw [three_mem_hull_iff_source_tests E hec heh]
    apply and_congr_right
    intro _
    constructor
    · rintro ⟨hz, hb⟩ k
      cases k with
      | inl r =>
        change 0 ≤ (rowExpression D r.val).eval (coordinates E E.xb)
        rw [hrow]
        exact hz r.val (by rw [← rowNormal_eq_of_pattern_eq D E hclasses hbypass]; exact r.property)
      | inr p =>
        change 0 ≤ (branchCut p.1 p.2.val p.2.property).eval (coordinates E E.xb)
        rw [hcut p.1 p.2.val p.2.property]
        exact hb p.1 p.2.val ((threeBranch_pattern_iff D E hclasses hbypass _ _).mp p.2.property)
    · intro hall
      refine ⟨?_, ?_⟩
      · intro r hr
        have hrD : normalVector (D.rowNormal r) = 0 := by
          rw [rowNormal_eq_of_pattern_eq D E hclasses hbypass]; exact hr
        have hh' := hall (Sum.inl ⟨r, hrD⟩)
        change 0 ≤ (rowExpression D r).eval (coordinates E E.xb) at hh'
        simpa only [hrow] using hh'
      · intro c r hr
        have hrD := (threeBranch_pattern_iff D E hclasses hbypass c r).mpr hr
        have hh' := hall (Sum.inr ⟨c, r, hrD⟩)
        change 0 ≤ (branchCut c r hrD).eval (coordinates E E.xb) at hh'
        simpa only [hcut c r hrD] using hh'

/-- Original-domain margins, the two sides of the simplex equality, and the
repaired source family form one finite index type. -/
abbrev FullUnitDescriptionIndex (D : ReductionData 3 I) :=
  DomainRow 3 I ⊕ (Bool ⊕ UnitDescriptionIndex D)

instance [Finite I] (D : ReductionData 3 I) : Finite (FullUnitDescriptionIndex D) := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  unfold FullUnitDescriptionIndex
  infer_instance

/-- The complete hull has one finite affine unit description in the original
coordinates, including domain checks. No profile variable remains. -/
theorem exists_full_finite_unit_description {L : ℕ} (D : ReductionData 3 (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false) :
    ∃ cuts : FullUnitDescriptionIndex D → AffineExpression (Coordinate 3 (Fin L)),
      (∀ k, UnitFlowProducts (cuts k)) ∧
      (∀ E : ReductionData 3 (Fin L), D.c = E.c → D.observedH = E.observedH →
        (E.graphPoint ∈ convexHull ℝ E.graph ↔
          ∀ k, 0 ≤ (cuts k).eval (coordinates E E.xb))) := by
  obtain ⟨profileCuts, hunit, hexact⟩ := exists_finite_unit_description D hc hh
  let cuts : FullUnitDescriptionIndex D → AffineExpression (Coordinate 3 (Fin L)) :=
    Sum.elim (domainExpression D) (Sum.elim
      (fun b => if b then simplexExpression else .neg simplexExpression) profileCuts)
  refine ⟨cuts, ?_, ?_⟩
  · intro k z hz
    rcases k with r | b | p
    · exact domainExpression_coefficient D r z
    · cases b
      · change -1 ≤ -simplexExpression.coefficient z ∧ -simplexExpression.coefficient z ≤ 1
        have hu := simplexExpression_coefficient_unit z
        omega
      · exact simplexExpression_coefficient_unit z
    · exact hunit p z hz
  · intro E hpattern hobserved
    have hec : ∀ i, E.c i 0 = .neither := by rw [← hpattern]; exact hc
    have heh : E.observedH 0 = false := by rw [← hobserved]; exact hh
    rw [hexact E hpattern hobserved,
      originalDomain_iff_fixed_domainExpressions D E hpattern hobserved hec heh]
    constructor
    · rintro ⟨⟨hd, hs⟩, hp⟩ k
      rcases k with r | b | p
      · exact hd r
      · cases b <;> simp [cuts, AffineExpression.eval, hs]
      · exact hp p
    · intro h
      have hpos := h (Sum.inr (Sum.inl true))
      have hneg := h (Sum.inr (Sum.inl false))
      change 0 ≤ simplexExpression.eval (coordinates E E.xb) at hpos
      change 0 ≤ -simplexExpression.eval (coordinates E E.xb) at hneg
      exact ⟨⟨fun r => h (Sum.inl r), by linarith⟩, fun p => h (Sum.inr (Sum.inr p))⟩

end NetworkSimplex.Chain.Threshold
