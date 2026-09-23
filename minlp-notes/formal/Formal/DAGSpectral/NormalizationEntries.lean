import Formal.DAGSpectral.NormalizationData
import Formal.DAGSpectral.PSDEntries

namespace DAGSpectral
noncomputable section
open Matrix
open scoped Matrix

namespace NormalizationTrials
variable {p m M : ℕ}

theorem accepted_atom_entry_bound (D : FactorData p m M) (s : Finset (Fin M))
    (o : Option (Fin m)) (h : acceptsAtom D.vector D.weight s (D.atom o))
    (i j : Fin s.card) :
    |(transform D.vector D.weight s * D.atom o *
      (transform D.vector D.weight s)ᵀ) i j| ≤ 4 * p := by
  exact normalized_abs_entry_le_four_p (D.atom o) (atom_real_psd D o)
    (transform D.vector D.weight s) h.2 i j

end NormalizationTrials
end
end DAGSpectral
