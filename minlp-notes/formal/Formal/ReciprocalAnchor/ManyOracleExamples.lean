import Formal.ReciprocalAnchor.ManyOracle

/-! Kernel checks of acceptance and each separating-oracle branch. -/
namespace ReciprocalAnchor.ManyLeaf
set_option maxRecDepth 8192

/-- No cut is returned at the exact attainable lower endpoint. -/
theorem oracle_accepts_two_leaf_minimum :
    (separationOracle 1 3 2 (31 / 50) ![2 / 3, 14 / 29] ![5 / 3, 40 / 29]).isNone = true := by
  decide +kernel

/-- The computed lower cut is violated by exactly the known joint-hull gap. -/
theorem oracle_two_leaf_cut_gap :
    ((separationOracle 1 3 2 (3 / 5) ![2 / 3, 14 / 29] ![5 / 3, 40 / 29]).map
      (fun C => C.eval 2 (3 / 5) ![2 / 3, 14 / 29] ![5 / 3, 40 / 29])) = some (1 / 50) := by
  decide +kernel

/-- Mean cuts remain available without any leaf variables. -/
theorem oracle_zero_leaf_mean_cut :
    ((separationOracle (n := 0) 1 3 0 1 Fin.elim0 Fin.elim0).map
      (fun C => C.eval 0 1 Fin.elim0 Fin.elim0)) = some 1 := by
  decide +kernel

/-- The upper reciprocal secant is tested independently of the lower bound. -/
theorem oracle_reciprocal_upper_cut :
    ((separationOracle (n := 0) 1 3 2 1 Fin.elim0 Fin.elim0).map
      (fun C => C.eval 2 1 Fin.elim0 Fin.elim0)) = some 1 := by
  decide +kernel

/-- A leaf-bound violation produces a cut before envelope construction. -/
theorem oracle_leaf_cut :
    ((separationOracle 1 3 2 (1 / 2) ![2] ![2]).map
      (fun C => C.eval 2 (1 / 2) ![2] ![2])) = some 1 := by
  decide +kernel

end ReciprocalAnchor.ManyLeaf
