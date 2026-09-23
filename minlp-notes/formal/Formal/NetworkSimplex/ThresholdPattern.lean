import Formal.NetworkSimplex.ThresholdRows

/-! Fixed observation patterns determine the symbolic profile rows and their normals. -/
namespace NetworkSimplex.Chain.Threshold

variable {m : ℕ} {I : Type*}

theorem residualExpression_pattern_eq (D E : ReductionData m I)
    (hc : D.c = E.c) (i : I) : residualExpression D i = residualExpression E i := by
  simp only [residualExpression, hc]

theorem rowNormal_pattern_eq (D E : ReductionData m I)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) (r : ProfileRow m I) :
    D.rowNormal r = E.rowNormal r := by
  cases r <;> simp only [ReductionData.rowNormal, hc, hh]

/-- A branch fixes actual source rows by pattern, independently of numerical query values. -/
theorem ThreeBranch.pattern_transfer (D E : ReductionData 3 I)
    (c : Fin 16) (r : Fin 11 → ProfileRow 3 I) (hbranch : ThreeBranch D c r)
    (hc : D.c = E.c) (hh : D.observedH = E.observedH) : ThreeBranch E c r := by
  intro k hk
  rw [← rowNormal_pattern_eq D E hc hh]
  exact hbranch k hk

end NetworkSimplex.Chain.Threshold
