import Formal.NetworkSimplex.ThresholdDomainRun
import Formal.NetworkSimplex.ThresholdOracleSize

/-! Bit bounds for the actual domain precheck, including recursive accumulators. -/
namespace NetworkSimplex.Chain.Threshold
open ReciprocalAnchor
namespace RationalData
variable {m L B : ℕ}

/-- The bypass complement is an actual subtraction used while generating margins. -/
theorem domain_bypass_complement_bits {D : RationalData m L} (h : D.InputBits B) :
    RationalBits (1 - D.xh) (B + 2) := by
  simpa only [show 1 + B + 1 = B + 2 by omega] using
    rationalBits_sub rationalBits_one h.xh

theorem domain_arc_complement_bits {D : RationalData m L} (h : D.InputBits B)
    (i : Fin L) : RationalBits (1 - D.xa i) (B + 2) := by
  simpa only [show 1 + B + 1 = B + 2 by omega] using
    rationalBits_sub rationalBits_one (h.xa i)

theorem oppositeFlow_bits {D : RationalData m L} (h : D.InputBits B)
    (i : Fin L) : RationalBits (D.oppositeFlow i) (2 * B + 3) := by
  simpa only [oppositeFlow, show B + 2 + B + 1 = 2 * B + 3 by omega] using
    rationalBits_sub (domain_bypass_complement_bits h) (h.xa i)

theorem oppositeFlow_complement_bits {D : RationalData m L} (h : D.InputBits B)
    (i : Fin L) : RationalBits (1 - D.oppositeFlow i) (2 * B + 5) := by
  simpa only [show 1 + (2 * B + 3) + 1 = 2 * B + 5 by omega] using
    rationalBits_sub rationalBits_one (oppositeFlow_bits h i)

/-- Every rational passed to the nonnegativity checker has a uniform bound,
including zero placeholders for observations that are absent. -/
theorem domainMargins_bits {D : RationalData m L} (h : D.InputBits B) :
    ∀ q ∈ D.domainMargins, RationalBits q (2 * B + 5) := by
  have input {q : ℚ} (hq : RationalBits q B) : RationalBits q (2 * B + 5) :=
    rationalBits_mono hq (by omega)
  have zero : RationalBits (0 : ℚ) (2 * B + 5) :=
    rationalBits_mono rationalBits_zero (by omega)
  have flatten_all (ls : List (List ℚ)) :
      (∀ q ∈ ls.flatten, RationalBits q (2 * B + 5)) ↔
        ∀ l ∈ ls, ∀ q ∈ l, RationalBits q (2 * B + 5) := by
    simp only [List.mem_flatten, forall_exists_index, and_imp]
    constructor
    · intro hh l hl q hq; exact hh q l hl hq
    · intro hh q l hl hq; exact hh l hl q hq
  simp only [domainMargins, List.forall_mem_append, flatten_all,
    List.forall_mem_ofFn_iff, List.forall_mem_cons,
    List.not_mem_nil, false_implies, implies_true, and_true]
  refine ⟨⟨⟨⟨⟨fun j => input (h.weights j), input h.xh,
    rationalBits_mono (domain_bypass_complement_bits h) (by omega)⟩,
    fun i => ⟨input (h.xa i),
      rationalBits_mono (domain_arc_complement_bits h i) (by omega),
      rationalBits_mono (oppositeFlow_bits h i) (by omega),
      oppositeFlow_complement_bits h i⟩⟩, ?_⟩, ?_⟩, ?_⟩
  · intro i j; split_ifs <;> first | exact input (h.u i j) | exact zero
  · intro i j; split_ifs <;> first | exact input (h.v i j) | exact zero
  · intro j; split_ifs <;> first | exact input (h.zh j) | exact zero

/-- Every recursive sum accumulator has this bound: each suffix is a sublist,
and the result also covers every prefix or other partial selection. -/
theorem weightSum_partial_bits {D : RationalData m L} (h : D.InputBits B)
    {part : List ℚ} (hp : part.Sublist (List.ofFn D.weights)) :
    RationalBits (weightSum part).1 (1 + (m + 1) * (B + 1)) := by
  rw [(weightSum_spec part).1]
  apply input_sum_bits h
  · intro q hq
    obtain ⟨j, rfl⟩ := List.mem_ofFn.mp (hp.subset hq)
    exact h.weights j
  · simpa only [List.length_ofFn] using hp.length_le

end RationalData
end NetworkSimplex.Chain.Threshold
