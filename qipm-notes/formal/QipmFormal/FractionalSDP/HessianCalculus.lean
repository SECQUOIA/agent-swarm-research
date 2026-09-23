import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno

namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Topology

/-- The second directional derivative of a log barrier, expressed through the
first two derivatives of its determinant polynomial. -/
theorem neg_log_second_deriv {f f' : ℝ → ℝ} {x d e : ℝ}
    (hfirst : ∀ y, HasDerivAt f (f' y) y)
    (hsecond : HasDerivAt f' e x) (hd : f' x = d) (hne : f x ≠ 0) :
    HasDerivAt (deriv (fun y => -Real.log (f y)))
      (d ^ 2 / f x ^ 2 - e / f x) x := by
  have hformula : deriv (fun y => -Real.log (f y)) =ᶠ[𝓝 x]
      (fun y => -(f' y / f y)) := by
    filter_upwards [(hfirst x).continuousAt.eventually_ne hne] with y hy
    exact ((hfirst y).log hy).neg.deriv
  have h := (hsecond.div (hfirst x) hne).neg
  rw [hd] at h
  convert h.congr_of_eventuallyEq hformula using 1 <;> try rfl
  field_simp
  ring


def cubic (c0 c1 c2 c3 s : ℝ) : ℝ := c0 + c1 * s + c2 * s ^ 2 + c3 * s ^ 3

theorem cubic_hasDerivAt (c0 c1 c2 c3 x : ℝ) :
    HasDerivAt (cubic c0 c1 c2 c3)
      (c1 + 2 * c2 * x + 3 * c3 * x ^ 2) x := by
  convert (((hasDerivAt_const x c0).add ((hasDerivAt_id x).const_mul c1)).add
    (((hasDerivAt_id x).pow 2).const_mul c2)).add
    (((hasDerivAt_id x).pow 3).const_mul c3) using 1 <;> try rfl
  simp only [mul_one, Nat.cast_ofNat, id_eq]
  ring

theorem cubic_second_log (c0 c1 c2 c3 : ℝ) (h0 : c0 ≠ 0) :
    HasDerivAt (deriv (fun s => -Real.log (cubic c0 c1 c2 c3 s)))
      (c1 ^ 2 / c0 ^ 2 - 2 * c2 / c0) 0 := by
  have hs : HasDerivAt (fun x => c1 + 2 * c2 * x + 3 * c3 * x ^ 2)
      (2 * c2) 0 := by
    convert ((hasDerivAt_const 0 c1).add ((hasDerivAt_id 0).const_mul (2 * c2))).add
      (((hasDerivAt_id 0).pow 2).const_mul (3 * c3)) using 1 <;> try rfl
    norm_num
  simpa [cubic] using neg_log_second_deriv (cubic_hasDerivAt c0 c1 c2 c3)
    hs (by simp) (by simpa [cubic] using h0)


/-- Along an affine line, the second ordinary derivative is the quadratic
value of the second Fréchet derivative. -/
theorem line_second_eq_iteratedFDeriv {E : Type*} [NormedAddCommGroup E]
    [NormedSpace ℝ E] {f : E → ℝ} {x : E} (hf : ContDiffAt ℝ 2 f x) (v : E) :
    deriv (deriv (fun s : ℝ => f (x + s • v))) 0 =
      iteratedFDeriv ℝ 2 f x (fun _ => v) := by
  have hline (s : ℝ) : HasDerivAt (fun s : ℝ => x + s • v) v s := by
    simpa using ((hasDerivAt_id s).smul_const v).const_add x
  have hderiv : deriv (fun s : ℝ => x + s • v) = fun _ => v := by
    funext s
    exact (hline s).deriv
  have hc : ContDiffAt ℝ 2 (fun s : ℝ => x + s • v) 0 := by fun_prop
  have hg : ContDiffAt ℝ 2 f (x + (0 : ℝ) • v) := by simpa using hf
  have h := iteratedDeriv_vcomp_two hg hc
  simpa only [Function.comp_def, show 2 = 1 + 1 from rfl, iteratedDeriv_succ,
    iteratedDeriv_one, iteratedDeriv_zero, hderiv, deriv_const, zero_smul, add_zero,
    map_zero] using h

end
end QipmFormal.FractionalSDP
