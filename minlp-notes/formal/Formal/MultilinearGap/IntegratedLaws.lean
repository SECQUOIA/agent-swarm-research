import Formal.CubicGap.Hull
import Formal.CubicGap.Polynomial

/-! Finite Bernoulli laws and their mixtures over the unit interval. -/

namespace MultilinearGap

open CubicGap MeasureTheory

noncomputable section

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Independent Bernoulli coordinates with prescribed success probabilities. -/
def bernoulliLaw (x : I → ℝ) (hx : x ∈ cube I) : Law (Vertex I) where
  weight v := ∏ i, if v i then x i else 1 - x i
  nonneg v := Finset.prod_nonneg fun i _ => by
    cases v i <;> simp only [Bool.false_eq_true, ↓reduceIte]
    · exact sub_nonneg.mpr (hx i).2
    · exact (hx i).1
  mass_one := by
    rw [← Fintype.prod_sum (fun i (b : Bool) => if b then x i else 1 - x i)]
    simp

/-- Tensor products of coordinate observables factor under independence. -/
theorem bernoulliLaw_expect_prod (x : I → ℝ) (hx : x ∈ cube I)
    (g : I → Bool → ℝ) :
    (bernoulliLaw x hx).expect (fun v => ∏ i, g i (v i)) =
      ∏ i, ((1 - x i) * g i false + x i * g i true) := by
  simp only [Law.expect, bernoulliLaw, ← Finset.prod_mul_distrib]
  rw [← Fintype.prod_sum (fun i (b : Bool) => (if b then x i else 1 - x i) * g i b)]
  simp [add_comm]

@[simp] theorem bernoulliLaw_expect_monomial (x : I → ℝ) (hx : x ∈ cube I)
    (s : Finset I) :
    (bernoulliLaw x hx).expect (fun v => monomial s (vertexPoint v)) =
      monomial s x := by
  have hprod (v : Vertex I) : monomial s (vertexPoint v) =
      ∏ i, if i ∈ s then vertexPoint v i else 1 := by
    simp [monomial, Finset.prod_ite_mem]
  simp_rw [hprod]
  change (bernoulliLaw x hx).expect
    (fun v => ∏ i, (fun i b => if i ∈ s then (if b then (1 : ℝ) else 0) else 1) i (v i)) = _
  rw [bernoulliLaw_expect_prod x hx
    (fun i b => if i ∈ s then (if b then (1 : ℝ) else 0) else 1)]
  have hfactor (i : I) :
      (1 - x i) * (if i ∈ s then vertexPoint (fun _ => false) i else 1) +
      x i * (if i ∈ s then vertexPoint (fun _ => true) i else 1) =
      if i ∈ s then x i else 1 := by
    by_cases hi : i ∈ s <;> simp [hi, vertexPoint]
  simp only [vertexPoint] at hfactor
  simp_rw [hfactor]
  simp [monomial, Finset.prod_ite_mem]

@[simp] theorem bernoulliLaw_mean (x : I → ℝ) (hx : x ∈ cube I) (i : I) :
    (bernoulliLaw x hx).expect (fun v => vertexPoint v i) = x i := by
  simpa [monomial] using bernoulliLaw_expect_monomial x hx {i}

variable {Ω : Type*} [Fintype Ω]

/-- Average finite probability laws over a uniform parameter in the unit interval. -/
def integratedLaw (μ : ℝ → Law Ω)
    (hμ : ∀ w, IntervalIntegrable (fun t => (μ t).weight w) volume 0 1) : Law Ω where
  weight w := ∫ t in (0 : ℝ)..1, (μ t).weight w
  nonneg w := intervalIntegral.integral_nonneg_of_forall (by norm_num) fun t => (μ t).nonneg w
  mass_one := by
    rw [← intervalIntegral.integral_finsetSum (fun w _ => hμ w)]
    simp only [Law.mass_one]
    norm_num

/-- Finite expectations commute with integration of the weights. -/
theorem integratedLaw_expect (μ : ℝ → Law Ω)
    (hμ : ∀ w, IntervalIntegrable (fun t => (μ t).weight w) volume 0 1)
    (f : Ω → ℝ) :
    (integratedLaw μ hμ).expect f = ∫ t in (0 : ℝ)..1, (μ t).expect f := by
  simp only [Law.expect, integratedLaw]
  rw [intervalIntegral.integral_finsetSum (fun w _ => (hμ w).mul_const (f w))]
  simp [intervalIntegral.integral_mul_const]

/-- A measurable function with values in the unit interval is integrable there. -/
theorem intervalIntegrable_of_mem_unitInterval (f : ℝ → ℝ) (hf : Measurable f)
    (hbound : ∀ t, f t ∈ Set.Icc (0 : ℝ) 1) :
    IntervalIntegrable f volume 0 1 := by
  apply (intervalIntegrable_const (c := (1 : ℝ))).mono_fun hf.aestronglyMeasurable
  exact Filter.Eventually.of_forall fun t => by
    simpa [Real.norm_eq_abs, abs_of_nonneg (hbound t).1] using (hbound t).2

/-- Measurable coordinate probabilities produce integrable Bernoulli weights. -/
theorem bernoulliLaw_weight_integrable (p : ℝ → I → ℝ)
    (hp : ∀ t, p t ∈ cube I) (hm : ∀ i, Measurable (fun t => p t i))
    (v : Vertex I) :
    IntervalIntegrable (fun t => (bernoulliLaw (p t) (hp t)).weight v) volume 0 1 := by
  apply intervalIntegrable_of_mem_unitInterval
  · apply Finset.measurable_prod
    intro i _
    cases v i <;> simp only [Bool.false_eq_true, ↓reduceIte]
    · exact measurable_const.sub (hm i)
    · exact hm i
  · intro t
    refine ⟨(bernoulliLaw (p t) (hp t)).nonneg v, ?_⟩
    exact (Finset.single_le_sum (fun w _ => (bernoulliLaw (p t) (hp t)).nonneg w)
      (Finset.mem_univ v)).trans_eq (bernoulliLaw (p t) (hp t)).mass_one

/-- A mixture of independent coordinate samples with a common uniform parameter. -/
def integratedBernoulli (p : ℝ → I → ℝ) (hp : ∀ t, p t ∈ cube I)
    (hm : ∀ i, Measurable (fun t => p t i)) : Law (Vertex I) :=
  integratedLaw (fun t => bernoulliLaw (p t) (hp t))
    (bernoulliLaw_weight_integrable p hp hm)

@[simp] theorem integratedBernoulli_mean (p : ℝ → I → ℝ)
    (hp : ∀ t, p t ∈ cube I) (hm : ∀ i, Measurable (fun t => p t i)) (i : I) :
    (integratedBernoulli p hp hm).expect (fun v => vertexPoint v i) =
      ∫ t in (0 : ℝ)..1, p t i := by
  rw [integratedBernoulli, integratedLaw_expect]
  simp

@[simp] theorem integratedBernoulli_expect_monomial (p : ℝ → I → ℝ)
    (hp : ∀ t, p t ∈ cube I) (hm : ∀ i, Measurable (fun t => p t i)) (s : Finset I) :
    (integratedBernoulli p hp hm).expect (fun v => monomial s (vertexPoint v)) =
      ∫ t in (0 : ℝ)..1, monomial s (p t) := by
  rw [integratedBernoulli, integratedLaw_expect]
  simp

end
end MultilinearGap
