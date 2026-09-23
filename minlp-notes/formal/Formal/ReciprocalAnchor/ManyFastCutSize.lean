import Formal.ReciprocalAnchor.ManyFastSeparation

/-! Polynomial bounds on every coefficient of the executable separating cut. -/
namespace ReciprocalAnchor.ManyLeaf

/-- A common actual reduced-numerator and denominator bit bound for all cut coefficients. -/
def RationalAffineForm.Bits {n : ℕ} (F : RationalAffineForm n) (B : ℕ) : Prop :=
  RationalBits F.1 B ∧ RationalBits F.2.1 B ∧
    (∀ j, RationalBits (F.2.2.1 j) B) ∧ ∀ j, RationalBits (F.2.2.2 j) B

theorem RationalAffineForm.Bits.mono {n B C : ℕ} {F : RationalAffineForm n}
    (h : F.Bits B) (hBC : B ≤ C) : F.Bits C :=
  ⟨rationalBits_mono h.1 hBC, rationalBits_mono h.2.1 hBC,
    fun j => rationalBits_mono (h.2.2.1 j) hBC,
    fun j => rationalBits_mono (h.2.2.2 j) hBC⟩

theorem RationalAffineForm.bits_zero (n : ℕ) : (0 : RationalAffineForm n).Bits 1 :=
  ⟨rationalBits_zero, rationalBits_zero, fun _ => rationalBits_zero,
    fun _ => rationalBits_zero⟩

theorem RationalAffineForm.Bits.add {n B C : ℕ} {F G : RationalAffineForm n}
    (hF : F.Bits B) (hG : G.Bits C) : (F + G).Bits (B + C + 1) :=
  ⟨rationalBits_add hF.1 hG.1, rationalBits_add hF.2.1 hG.2.1,
    fun j => rationalBits_add (hF.2.2.1 j) (hG.2.2.1 j),
    fun j => rationalBits_add (hF.2.2.2 j) (hG.2.2.2 j)⟩

theorem RationalAffineForm.bits_list_sum {n B : ℕ} {xs : List (RationalAffineForm n)}
    (h : ∀ F ∈ xs, F.Bits B) : xs.sum.Bits (1 + xs.length * (B + 1)) := by
  induction xs with
  | nil => simpa using bits_zero n
  | cons F xs ih =>
    have hF := h F (by simp)
    have hx := ih (fun G hG => h G (by simp [hG]))
    have hs := hF.add hx
    rw [List.sum_cons, List.length_cons]
    convert hs using 1
    ring

/-- Every coefficient of an exact interval cut has size linear in its two endpoints. -/
theorem segmentForm_bits {n K : ℕ} (i : Fin (2 * n + 2)) {a b : ℚ}
    (ha : RationalBits a K) (hb : RationalBits b K) :
    (segmentForm i a b).Bits (4 * K + 3) := by
  have ha2 : RationalBits (a ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hb2 : RationalBits (b ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul hb hb
  have hA : RationalBits ((a ^ 2)⁻¹ - (b ^ 2)⁻¹) (4 * K + 3) :=
    rationalBits_mono (rationalBits_sub (rationalBits_inv ha2) (rationalBits_inv hb2)) (by omega)
  have htwo : RationalBits 2 2 := by unfold RationalBits; decide
  have hB : RationalBits (2 * (a⁻¹ - b⁻¹)) (4 * K + 3) :=
    rationalBits_mono (rationalBits_mul htwo
      (rationalBits_sub (rationalBits_inv ha) (rationalBits_inv hb))) (by omega)
  have hAn := rationalBits_neg hA
  have hBn := rationalBits_neg hB
  have hzero : RationalBits 0 (4 * K + 3) := rationalBits_mono rationalBits_zero (by omega)
  unfold segmentForm RationalAffineForm.Bits
  split_ifs <;> simp only [Prod.fst_zero, Prod.snd_zero, Pi.zero_apply]
  · exact ⟨hzero, hzero, fun j => by split_ifs <;> assumption,
      fun j => by split_ifs <;> assumption⟩
  · exact ⟨hBn, hA, fun j => by split_ifs <;> assumption,
      fun j => by split_ifs <;> assumption⟩
  · exact ⟨hzero, hzero, fun _ => hzero, fun _ => hzero⟩
  · exact ⟨hBn, hA, fun _ => hzero, fun _ => hzero⟩

/-- Scalar intermediates used to compute every interval cut coefficient. -/
def segmentFormTrace (a b : ℚ) : List ℚ :=
  [0, 2, a, b, a ^ 2, b ^ 2, (a ^ 2)⁻¹, (b ^ 2)⁻¹,
    (a ^ 2)⁻¹ - (b ^ 2)⁻¹, -((a ^ 2)⁻¹ - (b ^ 2)⁻¹),
    a⁻¹, b⁻¹, a⁻¹ - b⁻¹, 2 * (a⁻¹ - b⁻¹), -(2 * (a⁻¹ - b⁻¹))]

theorem segmentFormTrace_bits {a b : ℚ} {K : ℕ}
    (ha : RationalBits a K) (hb : RationalBits b K) :
    ∀ x ∈ segmentFormTrace a b, RationalBits x (4 * K + 3) := by
  have ht : RationalBits 2 2 := by unfold RationalBits; decide
  have ha2 : RationalBits (a ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hb2 : RationalBits (b ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul hb hb
  have hA := rationalBits_sub (rationalBits_inv ha2) (rationalBits_inv hb2)
  have hd := rationalBits_sub (rationalBits_inv ha) (rationalBits_inv hb)
  have hB := rationalBits_mul ht hd
  simp only [segmentFormTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_zero (by omega), rationalBits_mono ht (by omega),
    rationalBits_mono ha (by omega), rationalBits_mono hb (by omega),
    rationalBits_mono ha2 (by omega), rationalBits_mono hb2 (by omega),
    rationalBits_mono (rationalBits_inv ha2) (by omega),
    rationalBits_mono (rationalBits_inv hb2) (by omega), rationalBits_mono hA (by omega),
    rationalBits_mono (rationalBits_neg hA) (by omega),
    rationalBits_mono (rationalBits_inv ha) (by omega),
    rationalBits_mono (rationalBits_inv hb) (by omega), rationalBits_mono hd (by omega),
    rationalBits_mono hB (by omega), rationalBits_mono (rationalBits_neg hB) (by omega)⟩

/-- Scalar intermediates of the affine tangent coefficient tuple. -/
def tangentFormTrace (a : ℚ) : List ℚ :=
  [0, 1, a, a ^ 2, 1 / a, a / a ^ 2, 1 / a + a / a ^ 2, 1 / a ^ 2, -(1 / a ^ 2)]

theorem tangentFormTrace_bits {a : ℚ} {B : ℕ} (ha : RationalBits a B) :
    ∀ x ∈ tangentFormTrace a, RationalBits x (4 * B + 2) := by
  have ha2 : RationalBits (a ^ 2) (B + B) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hr := rationalBits_div rationalBits_one ha
  have hs := rationalBits_div ha ha2
  have ht := rationalBits_div rationalBits_one ha2
  simp only [tangentFormTrace, List.forall_mem_cons, List.mem_nil_iff, false_implies,
    forall_const, and_true]
  exact ⟨rationalBits_mono rationalBits_zero (by omega),
    rationalBits_mono rationalBits_one (by omega), rationalBits_mono ha (by omega),
    rationalBits_mono ha2 (by omega), rationalBits_mono hr (by omega),
    rationalBits_mono hs (by omega), rationalBits_mono (rationalBits_add hr hs) (by omega),
    rationalBits_mono ht (by omega), rationalBits_mono (rationalBits_neg ht) (by omega)⟩

namespace FastEnvelope

/-- Every partial sum of the extracted cut has polynomial-size coefficients. -/
theorem fastCut_partial_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (ss : List Segment) (hss : ss.Sublist (buildSegments (sourceLines m q w) a b).1) :
    RationalAffineForm.Bits
      (((1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) : RationalAffineForm n) +
        (ss.map fun s => segmentForm (sourceIndex m q w s.active) s.lo s.hi).sum)
      (4 * B + 4 + (2 * n + 2) * (32 * B + 44)) := by
  have ha2 : RationalBits (a ^ 2) (B + B) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hconstant : RationalBits (1 / a + a / a ^ 2) (4 * B + 2) := by
    convert rationalBits_add (rationalBits_div rationalBits_one ha)
      (rationalBits_div ha ha2) using 1
    omega
  have hmean : RationalBits (-(1 / a ^ 2)) (4 * B + 2) :=
    rationalBits_mono (rationalBits_neg (rationalBits_div rationalBits_one ha2)) (by omega)
  have hzero : RationalBits 0 (4 * B + 2) := rationalBits_mono rationalBits_zero (by omega)
  have htangent : RationalAffineForm.Bits
      ((1 / a + a / a ^ 2, -(1 / a ^ 2), 0, 0) : RationalAffineForm n)
      (4 * B + 2) := ⟨hconstant, hmean, fun _ => hzero, fun _ => hzero⟩
  have hpiece (s : Segment) (hs : s ∈ ss) :
      (segmentForm (sourceIndex m q w s.active) s.lo s.hi).Bits (32 * B + 43) := by
    have hk := segments_knots (sourceLines m q w) (buildStack (sourceLines m q w)).1
      a b a b (fun _ h => buildStack_members _ h) (Or.inl rfl) (Or.inr (Or.inl rfl)) (hss.subset hs)
    convert segmentForm_bits (sourceIndex m q w s.active)
      (hk.1.bits hm ha hb hq hw) (hk.2.bits hm ha hb hq hw) using 1
    omega
  have hforms (F : RationalAffineForm n)
      (hF : F ∈ ss.map fun s => segmentForm (sourceIndex m q w s.active) s.lo s.hi) :
      F.Bits (32 * B + 43) := by
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hF
    exact hpiece s hs
  have hsum := RationalAffineForm.bits_list_sum hforms
  have hout := htangent.add hsum
  apply hout.mono
  simp only [List.length_map]
  have hlen : ss.length ≤ 2 * n + 2 := by
    simpa only [sourceLines, List.length_ofFn] using
      hss.length_le.trans (buildSegments_length (sourceLines m q w) a b)
  have hmul := Nat.mul_le_mul_right (32 * B + 44) hlen
  nlinarith

/-- The actual extracted cut has polynomial-size coefficients without semantic hypotheses. -/
theorem fastCut_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B) :
    (fastCut a b m q w).Bits (4 * B + 4 + (2 * n + 2) * (32 * B + 44)) :=
  fastCut_partial_bits hm ha hb hq hw _ (List.Sublist.refl _)

end FastEnvelope
end ReciprocalAnchor.ManyLeaf
