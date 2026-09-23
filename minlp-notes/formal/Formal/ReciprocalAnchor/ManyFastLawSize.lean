import Formal.ReciprocalAnchor.ManyFastAtoms
import Formal.ReciprocalAnchor.ManyFastSize

/-! Size bounds for the rational atoms actually emitted by the fast envelope. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- Every emitted atom uses two retained input lines, without an existential
partition or a supplied rational-law certificate. -/
theorem buildAtoms_bits {n B : ℕ} {m : ℚ} {q w : Fin n → ℚ}
    (hm : RationalBits m B) (hq : ∀ j, RationalBits (q j) B)
    (hw : ∀ j, RationalBits (w j) B)
    {z : Atom} (hz : z ∈ (buildAtoms (sourceLines m q w)).1) :
    RationalBits z.mass (4 * B + 5) ∧ RationalBits z.location (8 * B + 10) := by
  obtain ⟨c, hc, d, hd, he⟩ := slopeAtoms_provenance _ hz
  have hcB := sourceLines_bits hm hq hw (buildStack_members _ hc)
  have hdB := sourceLines_bits hm hq hw (buildStack_members _ hd)
  rw [he.1, he.2]
  constructor
  · convert rationalBits_sub hcB.2 hdB.2 using 1; omega
  · convert cross_bits hdB hcB using 1; omega

end ReciprocalAnchor.ManyLeaf.FastEnvelope
