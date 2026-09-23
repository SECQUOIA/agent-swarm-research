import Formal.DAGSpectral.EigenCompareTrace

namespace DAGSpectral
open ReciprocalAnchor

def eigenFinishCompareExpr (R δ k l pow : ℚ) : ArithmeticExpr :=
  .op .compare
    (.op .sub (.atom δ) (.op .div (.atom R) (.atom pow)))
    (.op .sub (.op .div (.op .mul (.atom R) (.atom k)) (.atom pow))
      (.op .div (.op .mul (.atom R) (.atom l)) (.atom pow)))

@[simp] theorem eigenFinishCompareExpr_eval (R δ k l pow : ℚ) :
    (eigenFinishCompareExpr R δ k l pow).eval =
      if δ-R/pow ≤ R * k/pow-R * l/pow then 1 else 0 := rfl

@[simp] theorem eigenFinishCompareExpr_operations (R δ k l pow : ℚ) :
    (eigenFinishCompareExpr R δ k l pow).operations = 8 := rfl

theorem eigenFinishCompareExpr_leaves {R δ k l pow : ℚ} {B : ℕ}
    (hR : RationalBits R B) (hδ : RationalBits δ B) (hk : RationalBits k B)
    (hl : RationalBits l B) (hp : RationalBits pow B) :
    (eigenFinishCompareExpr R δ k l pow).leavesBounded B :=
  ⟨⟨hδ,hR,hp⟩,⟨⟨hR,hk⟩,hp⟩,⟨⟨hR,hl⟩,hp⟩⟩

def eigenFinishWithTrace (R δ : ℚ) (k l t : ℕ) : Ordering × List ArithmeticEvent :=
  let pow := (2:ℚ) ^ t
  let gtRun := (eigenFinishCompareExpr R δ k l pow).run
  let ltRun := (eigenFinishCompareExpr R δ l k pow).run
  (if 1 ≤ gtRun.1 then .gt else if 1 ≤ ltRun.1 then .lt else .eq,
    powerTwoTrace t ++ gtRun.2 ++ ltRun.2 ++ [(.compare,1,gtRun.1),(.compare,1,ltRun.1)])

theorem eigenFinishWithTrace_value (R δ : ℚ) (k l t : ℕ) :
    (eigenFinishWithTrace R δ k l t).1 =
      if δ-R/(2:ℚ) ^ t ≤ R * k/(2:ℚ) ^ t-R * l/(2:ℚ) ^ t then .gt
      else if δ-R/(2:ℚ) ^ t ≤ R * l/(2:ℚ) ^ t-R * k/(2:ℚ) ^ t then .lt else .eq := by
  simp only [eigenFinishWithTrace, ArithmeticExpr.run_eq, eigenFinishCompareExpr_eval]
  split_ifs <;> norm_num at *

theorem eigenFinishWithTrace_length (R δ : ℚ) (k l t : ℕ) :
    (eigenFinishWithTrace R δ k l t).2.length = t + 18 := by
  simp [eigenFinishWithTrace, ArithmeticExpr.run_eq, powerTwoTrace_length]

theorem eigenFinishWithTrace_bits {R δ : ℚ} {k l t B : ℕ}
    (hB : 0 < B) (hR : RationalBits R B) (hδ : RationalBits δ B)
    (hk : k < 2 ^ t) (hl : l < 2 ^ t) (hT : 2 * t + 2 ≤ B) :
    ∀ e ∈ (eigenFinishWithTrace R δ k l t).2, eventBits (arithmeticWidth 8 B) e := by
  have hki := rationalBits_mono (rationalBits_nat_of_lt_two_pow hk) (by omega : t + 1 ≤ B)
  have hli := rationalBits_mono (rationalBits_nat_of_lt_two_pow hl) (by omega : t + 1 ≤ B)
  have hp := rationalBits_mono (rationalBits_two_pow t) (by omega : 2 * t + 1 ≤ B)
  have hg := (eigenFinishCompareExpr R δ k l ((2:ℚ) ^ t)).eval_trace_bits
    (eigenFinishCompareExpr_leaves hR hδ hki hli hp)
  have hh := (eigenFinishCompareExpr R δ l k ((2:ℚ) ^ t)).eval_trace_bits
    (eigenFinishCompareExpr_leaves hR hδ hli hki hp)
  simp only [eigenFinishCompareExpr_operations] at hg hh
  have hBK : B ≤ arithmeticWidth 8 B := by
    simpa only [arithmeticWidth_zero] using arithmeticWidth_mono (B := B) (show 0 ≤ 8 by omega)
  intro e he
  simp only [eigenFinishWithTrace, ArithmeticExpr.run_eq, List.mem_append,
    List.mem_cons, List.not_mem_nil, or_false] at he
  rcases he with ((he | he) | he) | (rfl | rfl)
  · exact eventBits_mono (powerTwoTrace_bits t e he) (hT.trans hBK)
  · exact hg.2 e he
  · exact hh.2 e he
  · exact ⟨rationalBits_mono rationalBits_one (hB.trans_le hBK), hg.1⟩
  · exact ⟨rationalBits_mono rationalBits_one (hB.trans_le hBK), hh.1⟩

end DAGSpectral
