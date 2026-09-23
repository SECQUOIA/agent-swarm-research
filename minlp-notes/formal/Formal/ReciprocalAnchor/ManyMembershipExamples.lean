import Formal.ReciprocalAnchor.ManyMembership

/-! Kernel evaluation of the complete rational membership checker. -/
namespace ReciprocalAnchor.ManyLeaf
set_option maxRecDepth 8192

theorem membership_exact_two_leaf_minimum :
    rationalMembership 1 3 2 (31 / 50) ![2 / 3, 14 / 29] ![5 / 3, 40 / 29] = true := by
  decide +kernel

theorem membership_rejects_separate_hull_candidate :
    rationalMembership 1 3 2 (3 / 5) ![2 / 3, 14 / 29] ![5 / 3, 40 / 29] = false := by
  decide +kernel

theorem membership_zero_leaves :
    rationalMembership (n := 0) 1 3 2 (1 / 2) Fin.elim0 Fin.elim0 = true := by
  decide +kernel

theorem membership_zero_leaves_rejects_mean :
    rationalMembership (n := 0) 1 3 0 1 Fin.elim0 Fin.elim0 = false := by
  decide +kernel

end ReciprocalAnchor.ManyLeaf
