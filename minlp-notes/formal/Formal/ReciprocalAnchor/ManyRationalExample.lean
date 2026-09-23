import Formal.ReciprocalAnchor.ManyAlgorithm

/-! Exact rational evaluation of the two-leaf counterexample. -/
namespace ReciprocalAnchor.ManyLeaf
set_option maxRecDepth 4096

/-- Three pieces suffice; the final zero piece has no contribution. -/
def twoLeafCertificate : RationalEnvelopeCertificate 6 3 where
  knots := fun i => if i.val = 0 then 1 else if i.val = 1 then 25 / 16
    else if i.val = 2 then 20 / 7 else 3
  active := fun i => if i.val = 0 then 0 else if i.val = 1 then 1 else 4

theorem twoLeafCertificate_valid :
    twoLeafCertificate.Valid (rationalLines 2 ![2 / 3, 14 / 29] ![5 / 3, 40 / 29]) 1 3 := by
  decide +kernel

theorem twoLeafCertificate_value :
    twoLeafCertificate.value 2 1 ![2 / 3, 14 / 29] ![5 / 3, 40 / 29] = 31 / 50 := by
  decide +kernel

/-- The rational computation equals the full continuous-support integral. -/
theorem twoLeaf_lowerMoment :
    lowerMoment 1 3 2 ![2 / 3, 14 / 29] ![5 / 3, 40 / 29] = (31 / 50 : ℝ) := by
  have h := RationalEnvelopeCertificate.value_eq_lowerMoment
    (n := 2) twoLeafCertificate_valid (by norm_num)
  rw [twoLeafCertificate_value] at h
  have hq : (fun j : Fin 2 => ((![2 / 3, 14 / 29] j : ℚ) : ℝ)) =
      (![2 / 3, 14 / 29] : Fin 2 → ℝ) := by
    funext j; fin_cases j <;> norm_num
  have hw : (fun j : Fin 2 => ((![5 / 3, 40 / 29] j : ℚ) : ℝ)) =
      (![5 / 3, 40 / 29] : Fin 2 → ℝ) := by
    funext j; fin_cases j <;> norm_num
  simpa only [hq, hw, Rat.cast_ofNat, Rat.cast_one, Rat.cast_div] using h.symm

theorem twoLeaf_gap :
    lowerMoment 1 3 2 ![2 / 3, 14 / 29] ![5 / 3, 40 / 29] - (3 / 5 : ℝ) = 1 / 50 := by
  rw [twoLeaf_lowerMoment]
  norm_num

end ReciprocalAnchor.ManyLeaf
