import Formal.NetworkSimplex.ThresholdDomainOracle

/-! Arithmetic and comparison bounds for the executable original-domain separator. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
namespace RationalData
variable {m L : ℕ}

/-- Every domain margin takes at most four rational arithmetic operations,
including reconstruction of an opposite-flow coordinate. -/
theorem domainExpressionRat_ops_le (D : RationalData m L) (r : DomainRow m (Fin L)) :
    domainEvalOps (D.domainExpressionRat r) ≤ 4 := by
  cases r <;> simp only [domainExpressionRat] <;> (try split_ifs) <;>
    simp [domainEvalOps]

/-- Each list node in the literal affine sum contributes one addition. -/
theorem domainEvalOps_sumList (es : List (AffineExpression (Coordinate m (Fin L)))) :
    domainEvalOps (AffineExpression.sumList es) = (es.map domainEvalOps).sum + es.length := by
  induction es with
  | nil => rfl
  | cons e es ih => simp [AffineExpression.sumList, domainEvalOps, ih]; omega

theorem domainEvalOps_sum {n : ℕ} (f : Fin n → AffineExpression (Coordinate m (Fin L))) :
    domainEvalOps (AffineExpression.sum f) = (List.ofFn fun j => domainEvalOps (f j)).sum + n := by
  simp [AffineExpression.sum, domainEvalOps_sumList, List.map_ofFn, Function.comp_def]

/-- Simplex equality sums the input weights and subtracts one. -/
theorem simplexExpression_ops :
    domainEvalOps (simplexExpression : AffineExpression (Coordinate m (Fin L))) = m + 2 := by
  simp [simplexExpression, domainEvalOps, domainEvalOps_sum]

theorem domainOracle_charge_eq (D : RationalData m L) :
    D.domainOracle.2 = (domainTags m L).length +
      ((domainTags m L).map fun r => domainEvalOps (D.domainExpressionRat r)).sum + 2 * m + 7 := by
  have he (e : AffineExpression (Coordinate m (Fin L))) :
      (D.domainEvalRun e).2 = domainEvalOps e := (domainEvalRun_spec D e).2
  simp only [domainOracle, negativeCutRun_charge, domainCutValues, List.length_map,
    List.map_map]
  simp [domainCutTags, domainCutExpression, he, domainEvalOps, simplexExpression_ops,
    List.map_map, Function.comp_def]
  omega

/-- The bound includes both evaluation arithmetic and one rational comparison
per generated candidate. Indexing and allocation are outside this arithmetic model. -/
theorem domainOracle_charge_le (D : RationalData m L) :
    D.domainOracle.2 ≤ 5 * (domainTags m L).length + 2 * m + 7 := by
  have hs (rs : List (DomainRow m (Fin L))) :
      (rs.map fun r => domainEvalOps (D.domainExpressionRat r)).sum ≤ 4 * rs.length := by
    induction rs with
    | nil => simp
    | cons r rs ih =>
      have hr := domainExpressionRat_ops_le D r
      simp only [List.map_cons, List.sum_cons, List.length_cons]
      omega
  rw [domainOracle_charge_eq]
  have h := hs (domainTags m L)
  omega

/-- An explicit polynomial bound for the actual public separator's counter. -/
theorem domainSeparator_charge_le (D : RationalData m L) :
    D.domainSeparator.2 ≤ 10 * m * L + 20 * L + 12 * m + 22 := by
  have h := domainOracle_charge_le D
  rw [domainTags_length] at h
  change D.domainOracle.2 ≤ _
  nlinarith

end RationalData
end NetworkSimplex.Chain.Threshold
