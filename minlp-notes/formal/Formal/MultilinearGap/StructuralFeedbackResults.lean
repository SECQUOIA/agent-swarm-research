import Formal.MultilinearGap.StructuralFeedbackAssembly

/-! Unit-cube specialization in the existing weighted termwise-gap notation. -/
namespace MultilinearGap
open CubicGap
noncomputable section

theorem feedback_cube_gap_bound {I : Type*} [Fintype I] [DecidableEq I]
    (F : Finset I) (S : Finset (Finset I))
    (hf : (feedbackIncidence F S).IsAcyclic)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I) :
    weightedTermwiseGap S a x ≤ (2 : ℝ) ^ F.card * hullGap (supportPolynomial S a) x := by
  have hbox : x ∈ coordinateBox (fun _ => 0) (fun _ => 1) := hx
  have h := feedback_variable_gap_bound F S hf a ha (fun _ => 0) (fun _ => 1)
    (by simp) (by simp) x hbox
  have he (f : (I → ℝ) → ℝ) :
      boxHullGap (fun _ => 0) (fun _ => 1) f x = hullGap f x := by
    have hh := boxHullGap_eq_of_mem (fun _ : I => (0 : ℝ)) (fun _ => (1 : ℝ))
      (by simp) f x hx
    have hp (p : I → ℝ) : MultilinearGap.boxPoint (fun _ => 0) (fun _ => 1) p = p := by
      funext i
      simp [MultilinearGap.boxPoint]
    simpa only [hp] using hh
  simpa only [boxTermwiseGap, weightedTermwiseGap, he] using h

end
end MultilinearGap
