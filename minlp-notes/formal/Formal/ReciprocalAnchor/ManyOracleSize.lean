import Formal.ReciprocalAnchor.ManyOracle
import Formal.ReciprocalAnchor.ManyFastCutSize

/-! Polynomial bounds for every coefficient returned by either oracle branch. -/
namespace ReciprocalAnchor.ManyLeaf

/-- Actual reduced-rational bit bounds for the entire returned affine inequality. -/
def RationalAffineCut.Bits {n : ℕ} (C : RationalAffineCut n) (B : ℕ) : Prop :=
  RationalBits C.offset B ∧ RationalBits C.mean B ∧ RationalBits C.reciprocal B ∧
    (∀ j, RationalBits (C.leafQ j) B) ∧ ∀ j, RationalBits (C.leafW j) B

theorem RationalAffineCut.Bits.mono {n B D : ℕ} {C : RationalAffineCut n}
    (h : C.Bits B) (hBD : B ≤ D) : C.Bits D :=
  ⟨rationalBits_mono h.1 hBD, rationalBits_mono h.2.1 hBD,
    rationalBits_mono h.2.2.1 hBD, fun j => rationalBits_mono (h.2.2.2.1 j) hBD,
    fun j => rationalBits_mono (h.2.2.2.2 j) hBD⟩

private theorem single_bits {n B : ℕ} (j : Fin n) {r : ℚ}
    (hr : RationalBits r B) (h0 : RationalBits 0 B) :
    ∀ k : Fin n, RationalBits ((Pi.single j r : Fin n → ℚ) k) B := by
  intro k
  simp only [Pi.single_apply]
  split_ifs <;> assumption

/-- The finite affine cuts contain only input endpoints and elementary combinations. -/
theorem linearCuts_bits {n B : ℕ} {a b : ℚ}
    (ha : RationalBits a B) (hb : RationalBits b B) {C : RationalAffineCut n}
    (hC : C ∈ linearCuts a b) : C.Bits (2 * B + 2) := by
  have h0 : RationalBits 0 (2 * B + 2) := rationalBits_mono rationalBits_zero (by omega)
  have h1 : RationalBits 1 (2 * B + 2) := rationalBits_mono rationalBits_one (by omega)
  have hn1 := rationalBits_neg h1
  have ha' := rationalBits_mono ha (show B ≤ 2 * B + 2 by omega)
  have hb' := rationalBits_mono hb (show B ≤ 2 * B + 2 by omega)
  have hna := rationalBits_neg ha'
  have hnb := rationalBits_neg hb'
  have hab := rationalBits_mono (rationalBits_neg (rationalBits_add ha hb))
    (show B + B + 1 ≤ 2 * B + 2 by omega)
  have hprod := rationalBits_mono (rationalBits_mul ha hb)
    (show B + B ≤ 2 * B + 2 by omega)
  rcases List.mem_append.mp hC with hC | hC
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl
    · exact ⟨ha', hn1, h0, fun _ => h0, fun _ => h0⟩
    · exact ⟨hnb, h1, h0, fun _ => h0, fun _ => h0⟩
    · exact ⟨hab, h1, hprod, fun _ => h0, fun _ => h0⟩
  · obtain ⟨cs, hcs, hC⟩ := List.mem_flatten.mp hC
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp hcs
    simp only [leafCuts, List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl | rfl | rfl | rfl
    · exact ⟨h0, h0, h0, single_bits j hn1 h0, fun _ => h0⟩
    · exact ⟨hn1, h0, h0, single_bits j h1 h0, fun _ => h0⟩
    · exact ⟨h0, h0, h0, single_bits j ha' h0, single_bits j hn1 h0⟩
    · exact ⟨h0, h0, h0, single_bits j hnb h0, single_bits j h1 h0⟩
    · exact ⟨ha', hn1, h0, single_bits j hna h0, single_bits j h1 h0⟩
    · exact ⟨hnb, h1, h0, single_bits j hb' h0, single_bits j hn1 h0⟩

/-- Adding the reciprocal coefficient `-1` preserves the fast-cut size bound. -/
theorem lowerMomentCut_bits {n B : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B) :
    (lowerMomentCut a b m q w).Bits (4 * B + 4 + (2 * n + 2) * (32 * B + 44)) := by
  obtain ⟨h0, h1, hq', hw'⟩ := FastEnvelope.fastCut_bits hm ha hb hq hw
  exact ⟨h0, h1, rationalBits_mono (rationalBits_neg rationalBits_one) (by omega), hq', hw'⟩

/-- Every actual output of the total oracle has polynomial-size rational coefficients.
No feasibility or endpoint-order premise is needed for this representation bound. -/
theorem separationOracle_bits {n B : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    {C : RationalAffineCut n} (h : separationOracle a b m t q w = some C) :
    C.Bits (4 * B + 4 + (2 * n + 2) * (32 * B + 44)) := by
  unfold separationOracle at h
  cases he : findLinearViolation a b m t q w with
  | some D =>
    simp only [he] at h
    cases Option.some.inj h
    exact (linearCuts_bits ha hb (List.mem_of_find?_eq_some he)).mono (by omega)
  | none =>
    simp only [he] at h
    split_ifs at h
    cases Option.some.inj h
    exact lowerMomentCut_bits hm ha hb hq hw

end ReciprocalAnchor.ManyLeaf
