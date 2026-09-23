import Formal.NetworkSimplex.ThresholdBalancedHull

/-! The actual chain observations are exactly the forbidden row-label pairs. -/
namespace NetworkSimplex.Chain.Balanced
noncomputable section
variable {N : ℕ}

def forbiddenObservation (S : Fin N → Finset (Fin N))
    (q : {ij : Fin N × Fin N // ij.2 ∉ S ij.1}) : Obs S :=
  observation S q.val.1 q.val.2 q.property

theorem forbiddenObservation_bijective (S : Fin N → Finset (Fin N)) :
    Function.Bijective (forbiddenObservation S) := by
  constructor
  · intro q z h
    apply Subtype.ext
    have hv := congrArg Subtype.val h
    simpa [forbiddenObservation, observation, Chain.a, Prod.ext_iff] using hv
  · rintro ⟨⟨e, j⟩, ho⟩
    rcases e with ⟨i, flag⟩ | z
    · cases flag
      · exact ⟨⟨(i, j), (pattern_observesA S i j).mp ho⟩, rfl⟩
      · exact False.elim (pattern_not_b S i j ho)
    · exact ho.elim

def forbiddenObservationEquiv (S : Fin N → Finset (Fin N)) :
    {ij : Fin N × Fin N // ij.2 ∉ S ij.1} ≃ Obs S :=
  Equiv.ofBijective (forbiddenObservation S) (forbiddenObservation_bijective S)

end
end NetworkSimplex.Chain.Balanced
