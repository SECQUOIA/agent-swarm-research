import QipmFormal.ScalarCert.Eval
import QipmFormal.ScalarCert.Tail
import QipmFormal.ScalarCert.Algebraic

/-!
# Rational enclosures for `Y`

Bridges the scaled-integer evaluator of `Eval.lean` to the analytic bounds of
`Tail.lean`, giving two-sided rational bounds on `Y z` for rational `z`.
-/

namespace QipmFormal.ScalarCert

open Real Finset

/-- One factor of `z` pulled out of the series. -/
lemma sum_term_eq (z : ℝ) (n : ℕ) :
    ∑ k ∈ range n, term z k
      = z * ∑ i ∈ range n, ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i) := by
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro k _
  rw [term, cast_cnum_div_cden]
  ring

/-- Lower bound for `Y z` from the floor evaluator. -/
theorem Y_ge_accLo {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (k : ℕ) :
    z * ((accLo (a * a) (b * b) s 0 k : ℝ) / (s : ℝ)) ≤ Y z := by
  have hb : (0:ℕ) < b := ha.trans hab
  have hzpos : 0 < z := by
    rw [hz]; exact div_pos (by exact_mod_cast ha) (by exact_mod_cast hb)
  have hz1 : z < 1 := by
    rw [hz, div_lt_one (by exact_mod_cast hb)]; exact_mod_cast hab
  have habs : |z| < 1 := by rwa [abs_of_pos hzpos]
  calc z * ((accLo (a * a) (b * b) s 0 k : ℝ) / (s : ℝ))
      ≤ z * ∑ i ∈ range (k + 1), ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i) := by
        exact mul_le_mul_of_nonneg_left (accLo_le₀ hz ha hab hs k) hzpos.le
    _ = ∑ i ∈ range (k + 1), term z i := (sum_term_eq z (k + 1)).symm
    _ ≤ Y z := partial_le_Y hzpos.le habs _

/-- Upper bound for `Y z` from the ceiling evaluator plus the tail estimate. -/
theorem Y_le_accHi {a b s : ℕ} {z : ℝ} (hz : z = (a : ℝ) / (b : ℝ))
    (ha : 0 < a) (hab : a < b) (hs : 0 < s) (k : ℕ) :
    Y z ≤ z * ((accHi (a * a) (b * b) s 0 k : ℝ) / (s : ℝ))
        + 2 * z ^ (2 * (k + 1) + 1) / ((2 * ((k : ℝ) + 1) + 1) * (1 - z ^ 2)) := by
  have hb : (0:ℕ) < b := ha.trans hab
  have hzpos : 0 < z := by
    rw [hz]; exact div_pos (by exact_mod_cast ha) (by exact_mod_cast hb)
  have hz1 : z < 1 := by
    rw [hz, div_lt_one (by exact_mod_cast hb)]; exact_mod_cast hab
  have hmain := Y_le_partial_add_tail hzpos hz1 (k + 1)
  have hbridge : ∑ i ∈ range (k + 1), term z i
      = z * ∑ i ∈ range (k + 1), ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i) :=
    sum_term_eq z (k + 1)
  have hHi : z * ∑ i ∈ range (k + 1), ((cnum i : ℝ) / (cden i : ℝ)) * z ^ (2 * i)
      ≤ z * ((accHi (a * a) (b * b) s 0 k : ℝ) / (s : ℝ)) :=
    mul_le_mul_of_nonneg_left (le_accHi₀ hz ha hab hs k) hzpos.le
  have hcast : ((k : ℝ) + 1) = ((k + 1 : ℕ) : ℝ) := by push_cast; ring
  rw [hcast]
  linarith [hmain, hbridge ▸ hHi]

end QipmFormal.ScalarCert
