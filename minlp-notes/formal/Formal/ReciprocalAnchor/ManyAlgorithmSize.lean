import Formal.ReciprocalAnchor.ManyAlgorithm
import Formal.ReciprocalAnchor.ManyRationalSize

/-! Reduced rational bit bounds for the actual envelope certificate evaluator. -/
namespace ReciprocalAnchor.ManyLeaf

/-- The original line coefficients have linear size in the input bit bound. -/
theorem rationalLines_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) (i : Fin (2 * n + 2)) :
    RationalBits (rationalLines m q w i).intercept (2 * B + 2) ∧
      RationalBits (rationalLines m q w i).negSlope (2 * B + 2) := by
  have hone : RationalBits 1 B := rationalBits_mono rationalBits_one (rationalBits_pos hm)
  have hzero : RationalBits 0 B := rationalBits_mono rationalBits_zero (rationalBits_pos hm)
  unfold rationalLines
  split_ifs
  · exact ⟨rationalBits_mono (hw _) (by omega), rationalBits_mono (hq _) (by omega)⟩
  · exact ⟨rationalBits_mono (rationalBits_sub hm (hw _)) (by omega),
      rationalBits_mono (rationalBits_sub hone (hq _)) (by omega)⟩
  · exact ⟨rationalBits_mono hzero (by omega), rationalBits_mono hzero (by omega)⟩
  · exact ⟨rationalBits_mono hm (by omega), rationalBits_mono hone (by omega)⟩

/-- This bound is on the implemented segment integral, with separate line and knot sizes. -/
theorem rationalSegmentIntegral_bits {l : RationalLine} {a b : ℚ} {B K : ℕ}
    (hi : RationalBits l.intercept B) (hs : RationalBits l.negSlope B)
    (ha : RationalBits a K) (hb : RationalBits b K) :
    RationalBits (rationalSegmentIntegral l a b) (2 * B + 6 * K + 5) := by
  have ha2 : RationalBits (a ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hb2 : RationalBits (b ^ 2) (K + K) := by
    simpa only [pow_two] using rationalBits_mul hb hb
  have htwo : RationalBits 2 2 := by unfold RationalBits; decide
  have hf := rationalBits_mul hi (rationalBits_sub (rationalBits_inv ha2) (rationalBits_inv hb2))
  have hg := rationalBits_mul (rationalBits_mul htwo hs)
    (rationalBits_sub (rationalBits_inv ha) (rationalBits_inv hb))
  unfold rationalSegmentIntegral
  convert rationalBits_sub hf hg using 1
  omega

/-- A certified answer has polynomial size in the input, knot size, and interval count.
This holds even for invalid certificates: the arithmetic evaluator itself has the bound. -/
theorem RationalEnvelopeCertificate.value_bits {n k B K : ℕ}
    (c : RationalEnvelopeCertificate (2 * n + 2) k) {m a : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (hknots : ∀ i, RationalBits (c.knots i) K) :
    RationalBits (c.value m a q w) (5 * B + 5 + k * (4 * B + 6 * K + 10)) := by
  have ha2 : RationalBits (a ^ 2) (B + B) := by
    simpa only [pow_two] using rationalBits_mul ha ha
  have hbase := rationalBits_sub (rationalBits_div rationalBits_one ha)
    (rationalBits_div (rationalBits_sub hm ha) ha2)
  have hpiece (i : Fin k) : RationalBits
      (rationalSegmentIntegral (rationalLines m q w (c.active i))
        (c.knots i.castSucc) (c.knots i.succ)) (4 * B + 6 * K + 9) := by
    obtain ⟨hi, hs⟩ := rationalLines_bits hm hq hw (c.active i)
    convert rationalSegmentIntegral_bits hi hs (hknots i.castSucc) (hknots i.succ) using 1
    omega
  have hsum := rationalBits_finset_sum Finset.univ _ (fun i _ => hpiece i)
  unfold value
  convert rationalBits_add hbase hsum using 1
  simp only [Finset.card_univ, Fintype.card_fin]
  ring

/-- If each knot is an endpoint or an intersection of input lines, it has linear size. -/
theorem rationalLines_intersection_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B) (i j : Fin (2 * n + 2)) :
    RationalBits
      (((rationalLines m q w j).intercept - (rationalLines m q w i).intercept) /
        ((rationalLines m q w j).negSlope - (rationalLines m q w i).negSlope))
      (8 * B + 10) := by
  obtain ⟨hi, hs⟩ := rationalLines_bits hm hq hw i
  obtain ⟨hj, ht⟩ := rationalLines_bits hm hq hw j
  convert rationalBits_div (rationalBits_sub hj hi) (rationalBits_sub ht hs) using 1
  omega

/-- Endpoints and line intersections give a bound polynomial in only the input size
and the number of certificate intervals. -/
theorem RationalEnvelopeCertificate.value_bits_of_input_knots {n k B : ℕ}
    (c : RationalEnvelopeCertificate (2 * n + 2) k) {m a b : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (ha : RationalBits a B) (hb : RationalBits b B)
    (hq : ∀ j, RationalBits (q j) B) (hw : ∀ j, RationalBits (w j) B)
    (hknots : ∀ x, c.knots x = a ∨ c.knots x = b ∨
      ∃ i j, c.knots x =
        ((rationalLines m q w j).intercept - (rationalLines m q w i).intercept) /
        ((rationalLines m q w j).negSlope - (rationalLines m q w i).negSlope)) :
    RationalBits (c.value m a q w) (5 * B + 5 + k * (52 * B + 70)) := by
  have hk (x : Fin (k + 1)) : RationalBits (c.knots x) (8 * B + 10) := by
    rcases hknots x with h | h | ⟨i, j, h⟩
    · rw [h]
      exact rationalBits_mono ha (by omega)
    · rw [h]
      exact rationalBits_mono hb (by omega)
    · rw [h]
      exact rationalLines_intersection_bits hm hq hw i j
  convert c.value_bits hm ha hq hw hk using 1
  ring

end ReciprocalAnchor.ManyLeaf
