import Formal.ReciprocalAnchor.ManyFastCutSize

/-! Bit bounds for intermediate rational values in the executable envelope evaluator. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- All rational operands and intermediate results of the actual segment formula. -/
def Segment.arithmeticTrace (s : Segment) : List ℚ :=
  let a := s.lo
  let b := s.hi
  let i := s.active.intercept
  let t := -s.active.slope
  [a, b, i, t, 2, a ^ 2, b ^ 2, (a ^ 2)⁻¹, (b ^ 2)⁻¹,
    (a ^ 2)⁻¹ - (b ^ 2)⁻¹, i * ((a ^ 2)⁻¹ - (b ^ 2)⁻¹),
    a⁻¹, b⁻¹, a⁻¹ - b⁻¹, 2 * t, 2 * t * (a⁻¹ - b⁻¹), s.integral]

theorem Segment.arithmeticTrace_bits {s : Segment} {C K : ℕ}
    (hi : RationalBits s.active.intercept C) (ht : RationalBits s.active.slope C)
    (ha : RationalBits s.lo K) (hb : RationalBits s.hi K) :
    ∀ x ∈ s.arithmeticTrace, RationalBits x (2 * C + 6 * K + 5) := by
  have htwo : RationalBits 2 2 := by unfold RationalBits; decide
  have ha2 : RationalBits (s.lo ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hb2 : RationalBits (s.hi ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul hb hb
  have hA := rationalBits_sub (rationalBits_inv ha2) (rationalBits_inv hb2)
  have hB := rationalBits_sub (rationalBits_inv ha) (rationalBits_inv hb)
  have hfirst := rationalBits_mul hi hA
  have ht' := rationalBits_neg ht
  have htwot := rationalBits_mul htwo ht'
  have hsecond := rationalBits_mul htwot hB
  have hresult : RationalBits s.integral (2 * C + 6 * K + 5) :=
    rationalSegmentIntegral_bits (l := ⟨s.active.intercept, -s.active.slope⟩) hi ht' ha hb
  simp only [arithmeticTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono ha (by omega), rationalBits_mono hb (by omega),
    rationalBits_mono hi (by omega), rationalBits_mono ht' (by omega),
    rationalBits_mono htwo (by omega), rationalBits_mono ha2 (by omega),
    rationalBits_mono hb2 (by omega), rationalBits_mono (rationalBits_inv ha2) (by omega),
    rationalBits_mono (rationalBits_inv hb2) (by omega), rationalBits_mono hA (by omega),
    rationalBits_mono hfirst (by omega), rationalBits_mono (rationalBits_inv ha) (by omega),
    rationalBits_mono (rationalBits_inv hb) (by omega), rationalBits_mono hB (by omega),
    rationalBits_mono htwot (by omega), rationalBits_mono hsecond (by omega), hresult⟩

/-- The tangent setup's operands and intermediate results, including its final value. -/
def setupTrace (a m : ℚ) : List ℚ :=
  [1, a, m, a ^ 2, m - a, 1 / a, (m - a) / a ^ 2, 1 / a - (m - a) / a ^ 2]

theorem setupTrace_bits {a m : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hm : RationalBits m B) :
    ∀ x ∈ setupTrace a m, RationalBits x (5 * B + 3) := by
  have ha2 : RationalBits (a ^ 2) (B + B) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hd := rationalBits_sub hm ha
  have hr := rationalBits_div rationalBits_one ha
  have hs := rationalBits_div hd ha2
  simp only [setupTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_one (by omega), rationalBits_mono ha (by omega),
    rationalBits_mono hm (by omega), rationalBits_mono ha2 (by omega),
    rationalBits_mono hd (by omega), rationalBits_mono hr (by omega),
    rationalBits_mono hs (by omega), rationalBits_mono (rationalBits_sub hr hs) (by omega)⟩

/-- Intersection computation retains the original line coefficients. -/
def crossTrace (a b : Line) : List ℚ :=
  [a.intercept, b.intercept, a.slope, b.slope,
    a.intercept - b.intercept, b.slope - a.slope, cross a b]

theorem crossTrace_bits {a b : Line} {C : ℕ}
    (ha : RationalBits a.intercept C ∧ RationalBits a.slope C)
    (hb : RationalBits b.intercept C ∧ RationalBits b.slope C) :
    ∀ x ∈ crossTrace a b, RationalBits x (4 * C + 2) := by
  simp only [crossTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono ha.1 (by omega), rationalBits_mono hb.1 (by omega),
    rationalBits_mono ha.2 (by omega), rationalBits_mono hb.2 (by omega),
    rationalBits_mono (rationalBits_sub ha.1 hb.1) (by omega),
    rationalBits_mono (rationalBits_sub hb.2 ha.2) (by omega), cross_bits ha hb⟩

/-- All coefficients, differences, products and the sum in the actual redundancy test. -/
def redundantTrace (a b c : Line) : List ℚ :=
  [a.intercept, b.intercept, c.intercept, a.slope, b.slope, c.slope,
    c.slope - a.slope, c.slope - b.slope, b.slope - a.slope,
    b.intercept * (c.slope - a.slope), a.intercept * (c.slope - b.slope),
    c.intercept * (b.slope - a.slope),
    a.intercept * (c.slope - b.slope) + c.intercept * (b.slope - a.slope)]

theorem redundantTrace_bits {a b c : Line} {C : ℕ}
    (ha : RationalBits a.intercept C ∧ RationalBits a.slope C)
    (hb : RationalBits b.intercept C ∧ RationalBits b.slope C)
    (hc : RationalBits c.intercept C ∧ RationalBits c.slope C) :
    ∀ x ∈ redundantTrace a b c, RationalBits x (6 * C + 3) := by
  have hd1 := rationalBits_sub hc.2 ha.2
  have hd2 := rationalBits_sub hc.2 hb.2
  have hd3 := rationalBits_sub hb.2 ha.2
  have hp1 := rationalBits_mul hb.1 hd1
  have hp2 := rationalBits_mul ha.1 hd2
  have hp3 := rationalBits_mul hc.1 hd3
  simp only [redundantTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono ha.1 (by omega), rationalBits_mono hb.1 (by omega),
    rationalBits_mono hc.1 (by omega), rationalBits_mono ha.2 (by omega),
    rationalBits_mono hb.2 (by omega), rationalBits_mono hc.2 (by omega),
    rationalBits_mono hd1 (by omega), rationalBits_mono hd2 (by omega),
    rationalBits_mono hd3 (by omega), rationalBits_mono hp1 (by omega),
    rationalBits_mono hp2 (by omega), rationalBits_mono hp3 (by omega),
    rationalBits_mono (rationalBits_add hp2 hp3) (by omega)⟩

/-- One common polynomial bound for all rational operands and accumulated values. -/
def evaluatorBits (n B : ℕ) : ℕ := 5 * B + 5 + (2 * n + 2) * (52 * B + 70)

theorem evaluatorBits_lower (n B : ℕ) : 52 * B + 69 ≤ evaluatorBits n B := by
  unfold evaluatorBits
  nlinarith

/-- Every arithmetic intermediate in every actual emitted segment satisfies the common bound. -/
theorem buildSegments_operand_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {s : Segment} (hs : s ∈ (buildSegments (sourceLines m q w) a b).1)
    {x : ℚ} (hx : x ∈ s.arithmeticTrace) : RationalBits x (evaluatorBits n B) := by
  have hmem := buildStack_members _ (segments_active_mem _ _ _ hs)
  obtain ⟨hi, ht⟩ := sourceLines_bits hm hq hw hmem
  have hk := segments_knots (sourceLines m q w) (buildStack (sourceLines m q w)).1
    a b a b (fun _ h => buildStack_members _ h) (Or.inl rfl) (Or.inr (Or.inl rfl)) hs
  have h := s.arithmeticTrace_bits hi ht (hk.1.bits hm ha hb hq hw)
    (hk.2.bits hm ha hb hq hw) x hx
  apply rationalBits_mono h
  have := evaluatorBits_lower n B
  omega

/-- Every setup intermediate satisfies the same width bound. -/
theorem setup_operand_bits {n B : ℕ} {a m : ℚ}
    (ha : RationalBits a B) (hm : RationalBits m B) {x : ℚ} (hx : x ∈ setupTrace a m) :
    RationalBits x (evaluatorBits n B) := by
  apply rationalBits_mono (setupTrace_bits ha hm x hx)
  have := evaluatorBits_lower n B
  omega

/-- Any original pair can be intersected within the common width bound. -/
theorem source_cross_operand_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) {u v : Line}
    (hu : u ∈ sourceLines m q w) (hv : v ∈ sourceLines m q w)
    {x : ℚ} (hx : x ∈ crossTrace u v) : RationalBits x (evaluatorBits n B) := by
  apply rationalBits_mono (crossTrace_bits (sourceLines_bits hm hq hw hu)
    (sourceLines_bits hm hq hw hv) x hx)
  have := evaluatorBits_lower n B
  omega

/-- Any original triple's redundancy test fits in the common width bound. -/
theorem source_redundant_operand_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) {u v z : Line}
    (hu : u ∈ sourceLines m q w) (hv : v ∈ sourceLines m q w)
    (hz : z ∈ sourceLines m q w) {x : ℚ} (hx : x ∈ redundantTrace u v z) :
    RationalBits x (evaluatorBits n B) := by
  apply rationalBits_mono (redundantTrace_bits (sourceLines_bits hm hq hw hu)
    (sourceLines_bits hm hq hw hv) (sourceLines_bits hm hq hw hz) x hx)
  have := evaluatorBits_lower n B
  omega

/-- Rational values formed while creating the source lines for one leaf. -/
def inputTrace (m q w : ℚ) : List ℚ :=
  [0, 1, m, q, w, 1 - q, m - w, -q, -(1 - q), -1]

theorem inputTrace_bits {m q w : ℚ} {B : ℕ}
    (hm : RationalBits m B) (hq : RationalBits q B) (hw : RationalBits w B) :
    ∀ x ∈ inputTrace m q w, RationalBits x (2 * B + 1) := by
  have ho : RationalBits 1 B := rationalBits_mono rationalBits_one (rationalBits_pos hm)
  have hz : RationalBits 0 B := rationalBits_mono rationalBits_zero (rationalBits_pos hm)
  have hd1 := rationalBits_sub ho hq
  have hd2 := rationalBits_sub hm hw
  simp only [inputTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono hz (by omega), rationalBits_mono ho (by omega),
    rationalBits_mono hm (by omega), rationalBits_mono hq (by omega),
    rationalBits_mono hw (by omega), rationalBits_mono hd1 (by omega),
    rationalBits_mono hd2 (by omega), rationalBits_mono (rationalBits_neg hq) (by omega),
    rationalBits_mono (rationalBits_neg hd1) (by omega),
    rationalBits_mono (rationalBits_neg ho) (by omega)⟩

theorem input_operand_bits {n B : ℕ} {m q w : ℚ}
    (hm : RationalBits m B) (hq : RationalBits q B) (hw : RationalBits w B)
    {x : ℚ} (hx : x ∈ inputTrace m q w) : RationalBits x (evaluatorBits n B) := by
  apply rationalBits_mono (inputTrace_bits hm hq hw x hx)
  have := evaluatorBits_lower n B
  omega

/-- Sorting and deduplication compare only original coefficients. -/
theorem source_coefficient_operand_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) {u : Line} (hu : u ∈ sourceLines m q w) :
    RationalBits u.intercept (evaluatorBits n B) ∧ RationalBits u.slope (evaluatorBits n B) := by
  obtain ⟨hi, hs⟩ := sourceLines_bits hm hq hw hu
  have hle : 2 * B + 2 ≤ evaluatorBits n B := by
    have := evaluatorBits_lower n B
    omega
  exact ⟨rationalBits_mono hi hle, rationalBits_mono hs hle⟩

/-- Every accumulating partial sum, not only the final returned value, fits the width. -/
theorem accumulation_operand_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (ss : List Segment) (hss : ss.Sublist (buildSegments (sourceLines m q w) a b).1) :
    RationalBits (ss.map Segment.integral).sum (evaluatorBits n B) := by
  apply rationalBits_mono (buildSegments_partial_sum_bits hm ha hb hq hw ss hss)
  unfold evaluatorBits
  omega

end ReciprocalAnchor.ManyLeaf.FastEnvelope
