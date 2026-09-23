import Formal.CubicGap.RoundingIndicators
import Formal.CubicGap.RoundingScalar
import Formal.CubicGap.OrientationRounding
import Formal.CubicGap.BiasedHighRounding

/-! The globally consistent 18:6:7 rounding law and its pair/triple guarantees. -/
namespace CubicGap
open MultilinearGap
noncomputable section

/-- The fixed convex mixture of three finite laws, with weights 18:6:7. -/
def roundingMixture {Ω : Type*} [Fintype Ω] (μ ν ρ : Law Ω) : Law Ω where
  weight w := (18 / 31) * μ.weight w + (6 / 31) * ν.weight w + (7 / 31) * ρ.weight w
  nonneg w := by positivity [μ.nonneg w, ν.nonneg w, ρ.nonneg w]
  mass_one := by
    simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Law.mass_one]
    norm_num

theorem roundingMixture_expect {Ω : Type*} [Fintype Ω] (μ ν ρ : Law Ω) (f : Ω → ℝ) :
    (roundingMixture μ ν ρ).expect f =
      (18 / 31) * μ.expect f + (6 / 31) * ν.expect f + (7 / 31) * ρ.expect f := by
  simp only [Law.expect, roundingMixture, add_mul, mul_assoc,
    Finset.sum_add_distrib, ← Finset.mul_sum]

theorem roundingMixture_deficiency {Ω : Type*} [Fintype Ω]
    (μ ν ρ : Law Ω) (f : Ω → ℝ) (u : ℝ) :
    31 * (u - (roundingMixture μ ν ρ).expect f) =
      18 * (u - μ.expect f) + 6 * (u - ν.expect f) + 7 * (u - ρ.expect f) := by
  rw [roundingMixture_expect]
  ring

variable {I : Type*} [Fintype I] [DecidableEq I]

theorem roundingMixture_hasMeans (μ ν ρ : Law (Vertex I)) (x : I → ℝ)
    (hμ : HasMeans μ x) (hν : HasMeans ν x) (hρ : HasMeans ρ x) :
    HasMeans (roundingMixture μ ν ρ) x := by
  intro i
  rw [roundingMixture_expect, hμ i, hν i, hρ i]
  ring

/-- Every law with the prescribed means has nonnegative monomial deficiency. -/
theorem rounding_deficiency_nonneg (μ : Law (Vertex I)) (x : I → ℝ)
    (hmean : HasMeans μ x) (s : Finset I) (i : I) (hi : i ∈ s) :
    0 ≤ x i - μ.expect (fun v => monomial s (vertexPoint v)) := by
  rw [sub_nonneg, ← hmean i]
  exact μ.expect_mono fun v => monomial_le_coordinate s
    (fun j _ => by simp only [vertexPoint]; split <;> norm_num) hi

/-- Independent Bernoulli sampling preserves all the ambient means. -/
theorem independentRounding_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (bernoulliLaw x hx) x := bernoulliLaw_mean x hx

theorem independentRounding_pair_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (i j : I) (hij : i ≠ j) :
    x i - (bernoulliLaw x hx).expect (fun v => monomial {i,j} (vertexPoint v)) =
      x i * (1 - x j) := by
  rw [bernoulliLaw_expect_monomial]
  simp [monomial, hij]
  ring

theorem independentRounding_triple_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (i j k : I) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    x i - (bernoulliLaw x hx).expect (fun v => monomial {i,j,k} (vertexPoint v)) =
      x i * (1 - x j * x k) := by
  rw [bernoulliLaw_expect_monomial]
  simp [monomial, hij, hik, hjk]
  ring

/-- A single ambient law, fixed independently of all supports and coefficients. -/
def cubicRoundingLaw (x : I → ℝ) (hx : x ∈ cube I) : Law (Vertex I) :=
  roundingMixture (orientationLaw x) (bernoulliLaw x hx) (biasedHighLaw x hx)

theorem cubicRoundingLaw_hasMeans (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (cubicRoundingLaw x hx) x :=
  roundingMixture_hasMeans _ _ _ x (orientationLaw_hasMeans x hx)
    (independentRounding_hasMeans x hx) (biasedHighLaw_hasMeans x hx)

theorem cubicRoundingLaw_expect (x : I → ℝ) (hx : x ∈ cube I) (f : Vertex I → ℝ) :
    (cubicRoundingLaw x hx).expect f =
      (18 / 31) * (orientationLaw x).expect f +
      (6 / 31) * (bernoulliLaw x hx).expect f +
      (7 / 31) * (biasedHighLaw x hx).expect f :=
  roundingMixture_expect _ _ _ _

theorem cubicRoundingLaw_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (f : Vertex I → ℝ) (u : ℝ) :
    31 * (u - (cubicRoundingLaw x hx).expect f) =
      18 * (u - (orientationLaw x).expect f) +
      6 * (u - (bernoulliLaw x hx).expect f) +
      7 * (u - (biasedHighLaw x hx).expect f) :=
  roundingMixture_deficiency _ _ _ _ _

/-- The fixed global law supplies the uniform deficiency fraction for every sorted pair. -/
theorem cubicRoundingLaw_pair_deficiency_lower (x : I → ℝ) (hx : x ∈ cube I)
    (i j : I) (hij : i ≠ j) (huv : x i ≤ x j) :
    12 * min (x i) (1 - x j) ≤
      31 * (x i - (cubicRoundingLaw x hx).expect
        (fun v => monomial {i,j} (vertexPoint v))) := by
  rw [cubicRoundingLaw_deficiency]
  have hO : x i - (orientationLaw x).expect
      (fun v => monomial {i,j} (vertexPoint v)) = min (x i) (1-x j)/2 := by
    rw [orientationLaw_expect_pair x i j hij, orientation_integral_pair (hx i) (hx j) huv]
    ring
  have hI := independentRounding_pair_deficiency x hx i j hij
  have hB0 := rounding_deficiency_nonneg (biasedHighLaw x hx) x
    (biasedHighLaw_hasMeans x hx) {i,j} i (by simp)
  have hI0 := rounding_deficiency_nonneg (bernoulliLaw x hx) x
    (independentRounding_hasMeans x hx) {i,j} i (by simp)
  have ht : 0 ≤ min (x i) (1-x j) := le_min (hx i).1 (by linarith [(hx j).2])
  by_cases hvl : x j ≤ 1/2
  · have htval : min (x i) (1-x j) = x i := min_eq_left (by linarith)
    apply rounding_bilinear_low_mixture
    · exact hO.ge
    · rw [hI, htval]
      nlinarith [mul_nonneg (hx i).1 (show 0 ≤ 1/2-x j by linarith)]
    · exact hB0
  · by_cases hul : x i ≤ 1/2
    · apply rounding_bilinear_mixed_uniform _ _ _ _ ht hO.ge hI0
      rw [biasedHighLaw_expect_pair x hx hij,
        integral_biasedHigh_pair_one_low (hx i) (hx j) hul (lt_of_not_ge hvl)]
      have h := rounding_bilinear_one_low (x i) (1-x j) (by linarith [(hx j).2])
      linarith
    · have htval : min (x i) (1-x j) = 1-x j := min_eq_right (by linarith)
      apply rounding_bilinear_high_uniform _ _ _ _ ht hO.ge
      · rw [hI, htval]
        nlinarith [mul_nonneg (show 0 ≤ x i-1/2 by linarith)
          (show 0 ≤ 1-x j by linarith [(hx j).2])]
      · rw [htval, biasedHighLaw_expect_pair x hx hij,
          integral_biasedHigh_pair_high (hx i) (hx j) huv (lt_of_not_ge hul)]
        linarith

/-- The fixed global law supplies the uniform deficiency fraction for every sorted triple. -/
theorem cubicRoundingLaw_triple_deficiency_lower (x : I → ℝ) (hx : x ∈ cube I)
    (i j k : I) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k)
    (huv : x i ≤ x j) (hvw : x j ≤ x k) :
    12 * min (x i) (2 - x j - x k) ≤
      31 * (x i - (cubicRoundingLaw x hx).expect
        (fun v => monomial {i,j,k} (vertexPoint v))) := by
  rw [cubicRoundingLaw_deficiency]
  have hI := independentRounding_triple_deficiency x hx i j k hij hik hjk
  have hB0 := rounding_deficiency_nonneg (biasedHighLaw x hx) x
    (biasedHighLaw_hasMeans x hx) {i,j,k} i (by simp)
  have hI0 := rounding_deficiency_nonneg (bernoulliLaw x hx) x
    (independentRounding_hasMeans x hx) {i,j,k} i (by simp)
  by_cases hvl : x j ≤ 1/2
  · rw [min_eq_left (by linarith [(hx k).2] : x i ≤ 2-x j-x k)]
    apply rounding_two_low_mixture
    · rw [orientationLaw_expect_triple x i j k hij hik hjk]
      have h := orientation_integral_two_low (hx i) (hx j) (hx k) huv hvl
      linarith
    · rw [hI]
      exact rounding_two_low_independent (x i) (x j) (x k) (hx i).1 (hx j).1 hvl (hx k).2
    · exact hB0
  · have hsum : 2-x j-x k = (1-x j)+(1-x k) := by ring
    rw [hsum]
    by_cases hul : x i ≤ 1/2
    · apply rounding_one_low_mixture _ _ _ _ _ _ (hx i).1
        (by linarith [(hx k).2]) (by linarith)
      · rw [orientationLaw_expect_triple x i j k hij hik hjk,
          orientation_integral_one_low (hx i) (hx j) (hx k) hul (lt_of_not_ge hvl) hvw]
        linarith
      · exact hI0
      · rw [biasedHighLaw_expect_triple x hx hij hik hjk,
          integral_biasedHigh_triple_one_low (hx i) (hx j) (hx k) hvw hul (lt_of_not_ge hvl)]
        linarith
    · apply rounding_high_mixture
      · rw [orientationLaw_expect_triple x i j k hij hik hjk,
          orientation_integral_all_high (hx i) (hx j) (hx k) (lt_of_not_ge hul) huv hvw]
        have h := rounding_high_orientation (x i) (1-x j) (1-x k) (by linarith)
        linarith
      · rw [hI]
        have h := rounding_high_independent (x i) (1-x j) (1-x k)
          (by linarith) (hx i).2 (by linarith [(hx j).2]) (by linarith)
          (by linarith [(hx k).2]) (by linarith)
        nlinarith
      · rw [biasedHighLaw_expect_triple x hx hij hik hjk,
          integral_biasedHigh_triple_high (hx i) (hx j) (hx k) huv hvw (lt_of_not_ge hul)]
        have h := rounding_high_orientation (x i) (1-x j) (1-x k) (by linarith)
        linarith

end
end CubicGap
