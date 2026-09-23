import Formal.ReciprocalAnchor.ManyFastEvaluation
import Formal.ReciprocalAnchor.ManyAlgorithmSize

/-! Polynomial reduced-rational size bounds for the executable sort/stack evaluator. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- An active line is retained from the input even for reversed clipping endpoints. -/
theorem segments_active_mem (stack : List Line) (lo hi : ℚ)
    {s : Segment} (hs : s ∈ segments stack lo hi) : s.active ∈ stack := by
  induction stack, lo, hi using segments.induct with
  | case1 => simp [segments] at hs
  | case2 c lo hi =>
    simp only [segments, List.mem_singleton] at hs
    subst s
    simp
  | case3 c d rest lo hi t h =>
    dsimp only [t] at *
    simp only [segments, h, ↓reduceIte, List.mem_singleton] at hs
    subst s
    simp
  | case4 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte] at hs
    exact List.mem_cons_of_mem _ (ih hs)
  | case5 c d rest lo hi t h h' ih =>
    dsimp only [t] at *
    simp only [segments, h, h', ↓reduceIte, List.mem_cons] at hs
    rcases hs with rfl | hs
    · simp
    · exact List.mem_cons_of_mem _ (ih hs)

theorem sourceLines_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) {l : Line} (hl : l ∈ sourceLines m q w) :
    RationalBits l.intercept (2 * B + 2) ∧ RationalBits l.slope (2 * B + 2) := by
  obtain ⟨i, rfl⟩ := List.mem_ofFn.mp hl
  obtain ⟨hi, hs⟩ := rationalLines_bits hm hq hw i
  exact ⟨hi, rationalBits_neg hs⟩

theorem cross_bits {a b : Line} {B : ℕ}
    (ha : RationalBits a.intercept B ∧ RationalBits a.slope B)
    (hb : RationalBits b.intercept B ∧ RationalBits b.slope B) :
    RationalBits (cross a b) (4 * B + 2) := by
  unfold cross
  convert rationalBits_div (rationalBits_sub ha.1 hb.1) (rationalBits_sub hb.2 ha.2) using 1
  omega

/-- Source endpoints and intersections have linear size in the original input. -/
theorem SourceKnot.bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (ht : SourceKnot (sourceLines m q w) a b t) : RationalBits t (8 * B + 10) := by
  rcases ht with rfl | rfl | ⟨u, hu, v, hv, rfl⟩
  · exact rationalBits_mono ha (by omega)
  · exact rationalBits_mono hb (by omega)
  · convert cross_bits (sourceLines_bits hm hq hw hu) (sourceLines_bits hm hq hw hv) using 1
    omega

/-- Every actual emitted integral has linear bit size, without certificate hypotheses. -/
theorem buildSegments_integral_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {s : Segment} (hs : s ∈ (buildSegments (sourceLines m q w) a b).1) :
    RationalBits s.integral (52 * B + 69) := by
  have hmem := buildStack_members _ (segments_active_mem _ _ _ hs)
  obtain ⟨hi, hsl⟩ := sourceLines_bits hm hq hw hmem
  have hk := segments_knots (sourceLines m q w) (buildStack (sourceLines m q w)).1
    a b a b (fun _ h => buildStack_members _ h) (Or.inl rfl) (Or.inr (Or.inl rfl)) hs
  have hlo := hk.1.bits hm ha hb hq hw
  have hhi := hk.2.bits hm ha hb hq hw
  unfold Segment.integral
  convert rationalSegmentIntegral_bits (l := ⟨s.active.intercept, -s.active.slope⟩)
    hi (rationalBits_neg hsl) hlo hhi using 1
  omega

/-- The result of the executable producer/evaluator has a polynomial bit bound in
only the number of leaves and the original input size. No validity assumptions are needed. -/
theorem fastLowerMoment_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B) :
    RationalBits (fastLowerMoment a b m q w)
      (5 * B + 5 + (2 * n + 2) * (52 * B + 70)) := by
  have ha2 : RationalBits (a ^ 2) (B + B) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hbase := rationalBits_sub (rationalBits_div rationalBits_one ha)
    (rationalBits_div (rationalBits_sub hm ha) ha2)
  let ss := (buildSegments (sourceLines m q w) a b).1
  have hs (v : ℚ) (hv : v ∈ ss.map Segment.integral) : RationalBits v (52 * B + 69) := by
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hv
    exact buildSegments_integral_bits hm ha hb hq hw hs
  have hsum := rationalBits_list_sum hs
  have hl : ss.length ≤ 2 * n + 2 := by
    simpa only [ss, sourceLines, List.length_ofFn] using
      buildSegments_length (sourceLines m q w) a b
  have hlen : (ss.map Segment.integral).length = ss.length := List.length_map _
  have hout := rationalBits_add hbase hsum
  change RationalBits (fastLowerMoment a b m q w) _ at hout
  apply rationalBits_mono hout
  rw [hlen]
  have hm' := Nat.mul_le_mul_right (52 * B + 70) hl
  nlinarith

/-- Every partial sum of produced integrals obeys the same polynomial size bound. -/
theorem buildSegments_partial_sum_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (ss : List Segment) (hss : ss.Sublist (buildSegments (sourceLines m q w) a b).1) :
    RationalBits (ss.map Segment.integral).sum (1 + (2 * n + 2) * (52 * B + 70)) := by
  have hs (v : ℚ) (hv : v ∈ ss.map Segment.integral) : RationalBits v (52 * B + 69) := by
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hv
    exact buildSegments_integral_bits hm ha hb hq hw (hss.subset hs)
  have hlen : ss.length ≤ 2 * n + 2 := by
    have hbnd := hss.length_le.trans (buildSegments_length (sourceLines m q w) a b)
    simpa only [sourceLines, List.length_ofFn] using hbnd
  apply rationalBits_mono (rationalBits_list_sum hs)
  simp only [List.length_map]
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ hlen) 1

/-- The products compared by the stack's exact redundancy test have linear bit size. -/
theorem redundant_test_bits {a b c : Line} {B : ℕ}
    (ha : RationalBits a.intercept B ∧ RationalBits a.slope B)
    (hb : RationalBits b.intercept B ∧ RationalBits b.slope B)
    (hc : RationalBits c.intercept B ∧ RationalBits c.slope B) :
    RationalBits (b.intercept * (c.slope - a.slope)) (3 * B + 1) ∧
    RationalBits (a.intercept * (c.slope - b.slope) +
      c.intercept * (b.slope - a.slope)) (6 * B + 3) := by
  constructor
  · convert rationalBits_mul hb.1 (rationalBits_sub hc.2 ha.2) using 1
    omega
  · convert rationalBits_add (rationalBits_mul ha.1 (rationalBits_sub hc.2 hb.2))
      (rationalBits_mul hc.1 (rationalBits_sub hb.2 ha.2)) using 1
    omega

end ReciprocalAnchor.ManyLeaf.FastEnvelope
