import Formal.MultilinearGap.HarmonicGain
import Formal.MultilinearGap.Couplings
import Formal.MultilinearGap.GeneralGaps

namespace MultilinearGap

open CubicGap

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Every positive one-low deficit in the small-marginal branch receives the
sharp harmonic gain from one common law with the prescribed coordinate means. -/
theorem harmonicLaw_sharp_gain (x : I → ℝ) (hx : x ∈ cube I)
    (Λ : ℝ) (hΛ : Real.exp 6 ≤ Λ) (s : Finset I) (r : I) (hr : r ∈ s)
    (hlow : x r ≤ 1 / 2) (hhigh : ∀ i ∈ s.erase r, 1 / 2 < x i)
    (T : ℝ) (hT : 0 < T) (hTu : T ≤ x r) (hTS : T ≤ otherFailures s x r)
    (hcard : ((s.erase r).card : ℝ) ≤ Real.exp (Λ - 1))
    (hsmall : ∀ i ∈ s.erase r, 1 - x i ≤ T / sharpA Λ) :
    sharpH Λ * T ≤ x r - (harmonicLaw x hx (Real.exp (Λ - 1)) (sharp_cutoff_ge_one hΛ)).expect
        (fun v => monomial s (vertexPoint v)) := by
  rw [harmonicLaw_unique_low_deficiency x hx _ _ s r hr hlow hhigh]
  exact sharp_harmonic_gain (s.erase r) (fun i => 1 - x i) hΛ hT hTu (hx r).2 hcard
    (fun i _ => ⟨by linarith [(hx i).2], by linarith [(hx i).1]⟩) hsmall hTS

end
end MultilinearGap
