import Formal.MultilinearGap.StructuralFrequencyCycle
import Formal.MultilinearGap.StructuralFrequencyProduct
import Formal.MultilinearGap.StructuralFrequencyLocal
import Formal.MultilinearGap.StructuralFactorGaps

/-!
# Rounding an explicit disjoint odd-cycle layout

This module consumes combinatorial cycle data, rather than assuming a rounding
inequality. Extracting this layout from arbitrary frequency-two slab vertices is
separate from the finite-law construction here.
-/
namespace MultilinearGap
open CubicGap StructuralFrequencyCycle
noncomputable section

variable {V E C : Type*} [Fintype V] [Fintype E] [Fintype C]
  [DecidableEq V] [DecidableEq E] [DecidableEq C]

/-- Explicit disjoint cycles carrying precisely the fractional coordinates. -/
structure FrequencyCycleLayout (S : V → Finset E) (z : E → ℝ) (C : Type*) where
  size : C → ℕ
  edge : (c : C) → Cycle (size c) → E
  edge_injective : Function.Injective (fun t : (c : C) × Cycle (size c) => edge t.1 t.2)
  row : (c : C) → Cycle (size c) → V
  row_injective : Function.Injective (fun t : (c : C) × Cycle (size c) => row t.1 t.2)
  half : ∀ c i, z (edge c i) = 1 / 2
  integral : ∀ e, (¬ ∃ c i, edge c i = e) → z e = 0 ∨ z e = 1
  incident : ∀ c i e, e ∈ S (row c i) ∧ z e = 1 / 2 ↔
    e = edge c i ∨ e = edge c (i - 1)
  outside : ∀ v, (¬ ∃ c i, row c i = v) → ∀ e ∈ S v, z e = 0 ∨ z e = 1

namespace FrequencyCycleLayout
variable {S : V → Finset E} {z : E → ℝ}
variable (D : FrequencyCycleLayout S z C)

/-- All cycle assignments are drawn jointly; integral edges stay fixed. -/
def vertex (w : (c : C) → Vertex (Cycle (D.size c))) : Vertex E := fun e =>
  if h : ∃ t : (c : C) × Cycle (D.size c), D.edge t.1 t.2 = e then
    w h.choose.1 h.choose.2 else decide (z e = 1)

omit [DecidableEq C] [DecidableEq V] [Fintype E] [Fintype V] in
theorem vertex_edge (w : (c : C) → Vertex (Cycle (D.size c))) (c : C)
    (i : Cycle (D.size c)) : D.vertex w (D.edge c i) = w c i := by
  classical
  unfold vertex
  rw [dif_pos (show ∃ t : (c : C) × Cycle (D.size c), D.edge t.1 t.2 = D.edge c i from
    ⟨⟨c, i⟩, rfl⟩)]
  have he := @D.edge_injective _ ⟨c, i⟩ (Classical.choose_spec
    (show ∃ t : (c : C) × Cycle (D.size c), D.edge t.1 t.2 = D.edge c i from ⟨⟨c, i⟩, rfl⟩))
  exact congrArg (fun t : (c : C) × Cycle (D.size c) => w t.1 t.2) he

omit [DecidableEq C] [DecidableEq V] [Fintype E] [Fintype V] in
theorem vertex_integral (w : (c : C) → Vertex (Cycle (D.size c))) (e : E)
    (he : z e = 0 ∨ z e = 1) : D.vertex w e = decide (z e = 1) := by
  classical
  have hnot : ¬ ∃ t : (c : C) × Cycle (D.size c), D.edge t.1 t.2 = e := by
    rintro ⟨⟨c, i⟩, h⟩
    have hh := D.half c i
    rw [h] at hh
    rcases he with he | he <;> linarith
  simp [vertex, hnot]

/-- Product of the explicit matching/complement laws, pushed to original edges. -/
def law : Law (Vertex E) :=
  (Law.pi fun c => roundingLaw (D.size c)).map D.vertex

omit [DecidableEq V] [Fintype V] in
/-- The assembled law preserves every original edge marginal. -/
theorem law_hasMeans : HasMeans D.law z := by
  classical
  intro e
  rw [law, Law.expect_map]
  by_cases he : ∃ c i, D.edge c i = e
  · obtain ⟨c, i, rfl⟩ := he
    change (Law.pi _).expect (fun w => vertexPoint (D.vertex w) (D.edge c i)) = _
    have hv : (fun w => vertexPoint (D.vertex w) (D.edge c i)) =
        fun w => vertexPoint (w c) i := by
      funext w
      simp only [vertexPoint, vertex_edge]
    rw [hv, Law.expect_pi_coordinate (fun c => roundingLaw (D.size c)) c
      (fun w => vertexPoint w i), roundingLaw_mean, D.half]
  · have hint := D.integral e he
    change (Law.pi _).expect (fun w => vertexPoint (D.vertex w) e) = z e
    have hv : (fun w => vertexPoint (D.vertex w) e) =
        fun _ => (if z e = 1 then (1 : ℝ) else 0) := by
      funext w
      simp only [vertexPoint, vertex_integral D w e hint, decide_eq_true_eq]
    rw [hv, Law.expect_const]
    rcases hint with h | h <;> simp [h]

/-- The fixed contribution to a factor's selected-edge count. -/
def integralCount (_D : FrequencyCycleLayout S z C) (v : V) : ℕ :=
  ((S v).filter fun e => z e = 1).card

omit [DecidableEq C] [DecidableEq V] [Fintype C] [Fintype E] [Fintype V] in
private theorem row_support (c : C) (i : Cycle (D.size c)) :
    S (D.row c i) = insert (D.edge c i) (insert (D.edge c (i-1))
      ((S (D.row c i)).filter fun e => z e ≠ 1 / 2)) := by
  classical
  ext e
  simp only [Finset.mem_insert, Finset.mem_filter]
  constructor
  · intro he
    by_cases hh : z e = 1 / 2
    · exact (D.incident c i e).mp ⟨he, hh⟩ |>.imp_right Or.inl
    · exact Or.inr (Or.inr ⟨he, hh⟩)
  · rintro (rfl | rfl | ⟨he, _⟩)
    · exact ((D.incident c i _).mpr (Or.inl rfl)).1
    · exact ((D.incident c i _).mpr (Or.inr rfl)).1
    · exact he

omit [Fintype E] in
private theorem countOn_insert {a : E} {s : Finset E} (ha : a ∉ s) (f : Vertex E) :
    countOn (insert a s) f = (if f a then 1 else 0) + countOn s f := by
  classical
  rw [countOn, Finset.filter_insert]
  split_ifs with h
  · simp [Finset.card_insert_of_notMem (fun hh => ha (Finset.mem_filter.mp hh).1),
      countOn, Nat.add_comm]
  · simp [countOn]

omit [DecidableEq C] [DecidableEq V] [Fintype E] [Fintype V] in
private theorem countOn_nonfractional (w : (c : C) → Vertex (Cycle (D.size c))) (v : V) :
    countOn ((S v).filter fun e => z e ≠ 1 / 2) (D.vertex w) = D.integralCount v := by
  classical
  unfold countOn integralCount
  congr 1
  ext e
  simp only [Finset.mem_filter]
  have hint (hh : z e ≠ 1 / 2) : z e = 0 ∨ z e = 1 := by
    apply D.integral e
    rintro ⟨c, i, rfl⟩
    exact hh (D.half c i)
  constructor
  · rintro ⟨⟨he, hh⟩, hv⟩
    rw [D.vertex_integral w e (hint hh)] at hv
    exact ⟨he, of_decide_eq_true hv⟩
  · rintro ⟨he, hz⟩
    refine ⟨⟨he, by rw [hz]; norm_num⟩, ?_⟩
    rw [D.vertex_integral w e (Or.inr hz)]
    simp [hz]

omit [DecidableEq C] [DecidableEq V] [Fintype E] [Fintype V] in
/-- A cycle factor's count is the fixed integral part plus its two cycle edges. -/
theorem countOn_row (w : (c : C) → Vertex (Cycle (D.size c))) (c : C)
    (i : Cycle (D.size c)) :
    countOn (S (D.row c i)) (D.vertex w) =
      D.integralCount (D.row c i) + incidentCount (w c) i := by
  classical
  have hid : i ≠ i - 1 := by
    intro hi
    have hh := support_card (D.size c) i
    simp only [support, ← hi, Finset.insert_eq_of_mem (Finset.mem_singleton_self i),
      Finset.card_singleton] at hh
    omega
  have heid : D.edge c i ≠ D.edge c (i - 1) := by
    intro h
    have hh := @D.edge_injective ⟨c, i⟩ ⟨c, i-1⟩ h
    have hidx : i = i - 1 := by simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and] using hh
    exact hid hidx
  have hnot (j : Cycle (D.size c)) :
      D.edge c j ∉ (S (D.row c i)).filter (fun e => z e ≠ 1 / 2) := by
    simp [D.half c j]
  rw [D.row_support c i, countOn_insert (by
      intro hh
      rcases Finset.mem_insert.mp hh with h | h
      · exact heid h
      · exact hnot i h),
    countOn_insert (hnot (i-1)), D.countOn_nonfractional,
    D.vertex_edge, D.vertex_edge, incidentCount]
  omega

omit [DecidableEq C] [DecidableEq V] [Fintype E] [Fintype V] in
/-- Factors off the cycles keep their integral count in every outcome. -/
theorem countOn_outside (w : (c : C) → Vertex (Cycle (D.size c))) (v : V)
    (hv : ¬ ∃ c i, D.row c i = v) :
    countOn (S v) (D.vertex w) = D.integralCount v := by
  classical
  unfold countOn integralCount
  congr 1
  apply Finset.filter_congr
  intro e he
  rw [D.vertex_integral w e (D.outside v hv e he)]
  simp

omit [DecidableEq V] [Fintype V] in
/-- Exact cardinality rounding at each cycle factor, for any sequence. -/
theorem law_cardinality_row (c : C) (i : Cycle (D.size c)) (φ : ℕ → ℝ) :
    D.law.expect (fun f => φ (countOn (S (D.row c i)) f)) =
      φ (D.integralCount (D.row c i) + 1) +
      ((φ (D.integralCount (D.row c i)) + φ (D.integralCount (D.row c i) + 2)) / 2 -
        φ (D.integralCount (D.row c i) + 1)) / (2 * (D.size c : ℝ) + 3) := by
  classical
  rw [law, Law.expect_map]
  change (Law.pi _).expect (fun w => φ (countOn (S (D.row c i)) (D.vertex w))) = _
  simp_rw [D.countOn_row]
  rw [Law.expect_pi_coordinate (fun c => roundingLaw (D.size c)) c
    (fun w => φ (D.integralCount (D.row c i) + incidentCount w i)),
    roundingLaw_incidentCount]

omit [DecidableEq V] [Fintype V] in
theorem law_cardinality_outside (v : V) (hv : ¬ ∃ c i, D.row c i = v) (φ : ℕ → ℝ) :
    D.law.expect (fun f => φ (countOn (S v) f)) = φ (D.integralCount v) := by
  classical
  rw [law, Law.expect_map]
  change (Law.pi _).expect (fun w => φ (countOn (S v) (D.vertex w))) = _
  simp_rw [D.countOn_outside _ v hv]
  exact Law.expect_const _ _


omit [DecidableEq C] [DecidableEq E] [DecidableEq V] [Fintype C] [Fintype E] [Fintype V] in
/-- The two half edges at a cycle factor are distinct. -/
theorem row_edges_ne (c : C) (i : Cycle (D.size c)) :
    D.edge c i ≠ D.edge c (i - 1) := by
  classical
  intro h
  have hh := @D.edge_injective ⟨c, i⟩ ⟨c, i-1⟩ h
  have hi : i = i - 1 := by simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and] using hh
  have hc := support_card (D.size c) i
  simp only [support, ← hi, Finset.insert_eq_of_mem (Finset.mem_singleton_self i),
    Finset.card_singleton] at hc
  omega

omit [DecidableEq C] [DecidableEq V] [Fintype C] [Fintype E] [Fintype V] in
/-- All other edges of a cycle factor are integral. -/
theorem row_rest_integral (c : C) (i : Cycle (D.size c)) :
    ∀ e ∈ halfIntegralRest (S (D.row c i)) (D.edge c i) (D.edge c (i-1)),
      z e = 0 ∨ z e = 1 := by
  classical
  intro e he
  simp only [halfIntegralRest, Finset.mem_erase] at he
  apply D.integral e
  rintro ⟨d, j, hed⟩
  have hh : z e = 1 / 2 := by rw [← hed]; exact D.half d j
  rcases (D.incident c i e).mp ⟨he.2.2, hh⟩ with h | h
  · exact he.2.1 h
  · exact he.1 h

omit [DecidableEq C] [DecidableEq V] [Fintype C] [Fintype E] [Fintype V] in
/-- Deleting the half edges does not change the integral count. -/
theorem integralOnes_row_rest (c : C) (i : Cycle (D.size c)) :
    integralOnes (halfIntegralRest (S (D.row c i)) (D.edge c i) (D.edge c (i-1))) z =
      D.integralCount (D.row c i) := by
  classical
  unfold integralOnes integralCount
  congr 1
  ext e
  simp only [halfIntegralRest, Finset.mem_filter, Finset.mem_erase]
  constructor
  · tauto
  · rintro ⟨he, hz⟩
    refine ⟨⟨?_, ?_, he⟩, hz⟩
    · intro h
      have := D.half c (i-1)
      rw [← h, hz] at this
      norm_num at this
    · intro h
      have := D.half c i
      rw [← h, hz] at this
      norm_num at this

omit [DecidableEq C] [DecidableEq E] [DecidableEq V] [Fintype C] [Fintype E] [Fintype V] in
/-- Exact lower endpoint at a cycle row. -/
theorem cardinalityLower_row (c : C) (i : Cycle (D.size c)) (φ : ℕ → ℝ) :
    cardinalityLower φ (S (D.row c i)) z = φ (D.integralCount (D.row c i) + 1) := by
  classical
  rw [cardinalityLower_two_halves φ _ z (D.edge c i) (D.edge c (i-1))
    ((D.incident c i _).mpr (Or.inl rfl)).1
    ((D.incident c i _).mpr (Or.inr rfl)).1 (D.row_edges_ne c i)
    (D.half c i) (D.half c (i-1)) (D.row_rest_integral c i),
    D.integralOnes_row_rest]

omit [DecidableEq C] [DecidableEq V] [Fintype C] [Fintype V] in
/-- The row's scalar gap is exactly its discrete midpoint curvature. -/
theorem hullGap_row (hz : z ∈ cube E) (c : C) (i : Cycle (D.size c))
    (φ : ℕ → ℝ) (hφ : ConvexCountTable φ (S (D.row c i)).card)
    (f : (E → ℝ) → ℝ) (hf : SeparatelyAffine f)
    (hv : ∀ v, f (vertexPoint v) = φ (countOn (S (D.row c i)) v)) :
    hullGap f z =
      (φ (D.integralCount (D.row c i)) + φ (D.integralCount (D.row c i) + 2)) / 2 -
        φ (D.integralCount (D.row c i) + 1) := by
  classical
  rw [hullGap, (cardinality_minimum φ _ hφ f hf hv z hz).csInf_eq,
    (cardinality_maximum φ _ hφ f hf hv z hz).csSup_eq,
    thresholdLaw_cardinality_two_halves φ _ z hz (D.edge c i) (D.edge c (i-1))
      ((D.incident c i _).mpr (Or.inl rfl)).1
      ((D.incident c i _).mpr (Or.inr rfl)).1 (D.row_edges_ne c i)
      (D.half c i) (D.half c (i-1)) (D.row_rest_integral c i),
    D.integralOnes_row_rest, D.cardinalityLower_row]

omit [DecidableEq V] in
/-- The matching/complement law loses at most the reciprocal cycle length
of each factor's actual scalar graph-hull gap. -/
theorem law_cardinality_loss (hz : z ∈ cube E)
    (φ : V → ℕ → ℝ) (hφ : ∀ v, ConvexCountTable (φ v) (S v).card)
    (f : V → (E → ℝ) → ℝ) (hf : ∀ v, SeparatelyAffine (f v))
    (hv : ∀ v w, f v (vertexPoint w) = φ v (countOn (S v) w))
    (η : ℝ) (hη : 0 ≤ η)
    (hlen : ∀ c, 1 / (2 * (D.size c : ℝ) + 3) ≤ η) :
    D.law.expect (fun w => factorSum f (vertexPoint w)) ≤
      (∑ v, cardinalityLower (φ v) (S v) z) + η * ∑ v, hullGap (f v) z := by
  classical
  rw [expect_factorSum, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro v _
  have hg : 0 ≤ hullGap (f v) z := by
    have hmin := cardinality_minimum (φ v) (S v) (hφ v) (f v) (hf v) (hv v) z hz
    have hmax := cardinality_maximum (φ v) (S v) (hφ v) (f v) (hf v) (hv v) z hz
    rw [hullGap, hmin.csInf_eq, hmax.csSup_eq]
    exact sub_nonneg.mpr (hmin.2 hmax.1)
  simp only [hv]
  by_cases hvrow : ∃ c i, D.row c i = v
  · obtain ⟨c, i, rfl⟩ := hvrow
    rw [D.law_cardinality_row, D.cardinalityLower_row]
    rw [← D.hullGap_row hz c i (φ _) (hφ _) (f _) (hf _) (hv _)]
    have hb := mul_le_mul_of_nonneg_right (hlen c) hg
    simpa only [one_div, div_eq_mul_inv, mul_comm, one_mul, add_comm] using add_le_add_left hb
      (φ (D.row c i) (D.integralCount (D.row c i) + 1))
  · rw [D.law_cardinality_outside v hvrow,
      cardinalityLower_integral (φ v) (S v) z (D.outside v hvrow)]
    change φ v (D.integralCount v) ≤ φ v (D.integralCount v) + η * hullGap (f v) z
    exact le_add_of_nonneg_right (mul_nonneg hη hg)

end FrequencyCycleLayout
end
end MultilinearGap
