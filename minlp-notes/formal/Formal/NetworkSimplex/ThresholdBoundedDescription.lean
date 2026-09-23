import Formal.NetworkSimplex.ThresholdGeneralSourceDescription
import Formal.NetworkSimplex.ThresholdDomainRows

/-! A single fixed finite affine description with determinant-bounded coefficients. -/
namespace NetworkSimplex.Chain.Threshold
open NetworkSimplex.Threshold

abbrev BoundedDescriptionIndex {m : ℕ} {I : Type*} (D : ReductionData m I) :=
  DomainRow m I ⊕ (Bool ⊕ {b : GeneralSourceBranch m I // b.cancels D})

instance {m : ℕ} {I : Type*} [Finite I] (D : ReductionData m I) :
    Finite (BoundedDescriptionIndex D) := by
  classical
  let _ : Fintype I := Fintype.ofFinite I
  let _ := generalSourceBranch_finite (m := m) (I := I)
  unfold BoundedDescriptionIndex
  infer_instance

def boundedDescription {m : ℕ} {I : Type*} (D : ReductionData m I) :
    BoundedDescriptionIndex D → AffineExpression (Coordinate m I) :=
  Sum.elim (domainExpression D) (Sum.elim
    (fun b => if b then simplexExpression else .neg simplexExpression)
    (fun b => b.val.expression D))

theorem boundedDescription_coefficients {m : ℕ} {I : Type*} [DecidableEq I]
    (D : ReductionData m I) (k : BoundedDescriptionIndex D)
    (z : Coordinate m I) (hz : FlowOrProduct z) :
    |(boundedDescription D k).coefficient z| ≤ ((m + 1) * delta01 m : ℕ) := by
  have hd : (1 : ℤ) ≤ ((m + 1) * delta01 m : ℕ) := by
    exact_mod_cast Nat.mul_pos (by omega : 0 < m + 1) (one_le_delta01 m)
  rcases k with r | b | c
  · exact (abs_le.mpr (domainExpression_coefficient D r z)).trans hd
  · cases b
    · change |-simplexExpression.coefficient z| ≤ _
      rw [abs_neg]
      exact (abs_le.mpr (simplexExpression_coefficient_unit z)).trans hd
    · exact (abs_le.mpr (simplexExpression_coefficient_unit z)).trans hd
  · change |(c.val.expression D).coefficient z| ≤ _
    rw [GeneralSourceBranch.expression_coefficient]
    exact c.val.coefficient_bound D z hz

theorem boundedDescription_exact {m L : ℕ} (D E : ReductionData m (Fin L))
    (hc : ∀ i, D.c i 0 = .neither) (hh : D.observedH 0 = false)
    (hpattern : D.c = E.c) (hob : D.observedH = E.observedH) :
    E.graphPoint ∈ convexHull ℝ E.graph ↔
      ∀ k, 0 ≤ (boundedDescription D k).eval (coordinates E E.xb) := by
  have hec : ∀ i, E.c i 0 = .neither := by rw [← hpattern]; exact hc
  have heh : E.observedH 0 = false := by rw [← hob]; exact hh
  have hnormal (r) : D.rowNormal r = E.rowNormal r := by
    cases r <;> simp [ReductionData.rowNormal, hpattern, hob]
  have hcancel (b : GeneralSourceBranch m (Fin L)) : b.cancels D ↔ b.cancels E := by
    simp only [GeneralSourceBranch.cancels, hnormal]
  have heval (b : GeneralSourceBranch m (Fin L)) :
      (b.expression D).eval (coordinates E E.xb) = b.value E :=
    b.expression_eval D E E.xb hpattern hob hec
  rw [general_mem_hull_iff_source_tests E hec heh,
    originalDomain_iff_fixed_domainExpressions D E hpattern hob hec heh]
  constructor
  · rintro ⟨⟨hd, hs⟩, hb⟩ k
    rcases k with r | b | c
    · exact hd r
    · cases b <;> simp [boundedDescription, AffineExpression.eval, hs]
    · change 0 ≤ (c.val.expression D).eval (coordinates E E.xb)
      rw [heval]
      exact hb c.val ((hcancel c.val).mp c.property)
  · intro h
    have hp := h (Sum.inr (Sum.inl true))
    have hn := h (Sum.inr (Sum.inl false))
    change 0 ≤ simplexExpression.eval (coordinates E E.xb) at hp
    change 0 ≤ -simplexExpression.eval (coordinates E E.xb) at hn
    refine ⟨⟨fun r => h (Sum.inl r), by linarith⟩, ?_⟩
    intro b hb
    have ht := h (Sum.inr (Sum.inr ⟨b, (hcancel b).mpr hb⟩))
    change 0 ≤ (b.expression D).eval (coordinates E E.xb) at ht
    simpa only [heval] using ht

end NetworkSimplex.Chain.Threshold
