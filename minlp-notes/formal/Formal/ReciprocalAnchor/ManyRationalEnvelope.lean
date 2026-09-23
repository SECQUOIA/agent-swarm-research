import Formal.ReciprocalAnchor.ManyEnvelope
import Formal.ReciprocalAnchor.ManyAlgorithm

/-! Rational envelope certificates always exist; their breakpoints and active lines
are obtained from the finite pair-intersection construction. -/
namespace ReciprocalAnchor.ManyLeaf

/-- The producer covers arbitrary rational input lines, including ties and parallels. -/
theorem exists_rationalEnvelopeCertificate_with_provenance {n : ℕ} (hn : 0 < n)
    (lines : Fin n → RationalLine) {a b : ℚ} (hab : a < b) :
    ∃ k : ℕ, ∃ C : RationalEnvelopeCertificate n k, 0 < k ∧ C.Valid lines a b ∧
      k ≤ n ^ 2 + 1 ∧ ∀ x, C.knots x = a ∨ C.knots x = b ∨
        ∃ i j, C.knots x = ((lines j).intercept - (lines i).intercept) /
          ((lines j).negSlope - (lines i).negSlope) := by
  let : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  let c : Fin n → ℚ := fun i => (lines i).intercept
  let d : Fin n → ℚ := fun i => -(lines i).negSlope
  obtain ⟨P, hprov, hsize⟩ := exists_affinePartition_with_provenance c d hab
  let C : RationalEnvelopeCertificate n P.size := ⟨P.knot, P.active⟩
  refine ⟨P.size, C, P.pos, ⟨P.first, P.last, ?_⟩, by simpa using hsize, ?_⟩
  · intro i
    have horder : P.knot i.castSucc ≤ P.knot i.succ := P.strict.monotone (Fin.castSucc_le_succ i)
    refine ⟨horder, ?_⟩
    intro j
    have hl := (affineEnvelope_eq_iff c d (P.active i) (P.knot i.castSucc)).mp
      (P.agrees i _ ⟨le_rfl, horder⟩) j
    have hr := (affineEnvelope_eq_iff c d (P.active i) (P.knot i.succ)).mp
      (P.agrees i _ ⟨horder, le_rfl⟩) j
    constructor
    · simpa [C, c, d, RationalLine.eval, sub_eq_add_neg] using hl
    · simpa [C, c, d, RationalLine.eval, sub_eq_add_neg] using hr
  · intro x
    rcases hprov x with h | h | ⟨i, j, h⟩
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
    · right; right
      refine ⟨i, j, ?_⟩
      simpa [C, c, d, sub_eq_add_neg, add_comm] using h

/-- Arbitrary rational input lines admit a valid rational envelope certificate. -/
theorem exists_rationalEnvelopeCertificate {n : ℕ} (hn : 0 < n)
    (lines : Fin n → RationalLine) {a b : ℚ} (hab : a < b) :
    ∃ k : ℕ, ∃ C : RationalEnvelopeCertificate n k, 0 < k ∧ C.Valid lines a b := by
  obtain ⟨k, C, hk, hv, _, _⟩ := exists_rationalEnvelopeCertificate_with_provenance hn lines hab
  exact ⟨k, C, hk, hv⟩

end ReciprocalAnchor.ManyLeaf
