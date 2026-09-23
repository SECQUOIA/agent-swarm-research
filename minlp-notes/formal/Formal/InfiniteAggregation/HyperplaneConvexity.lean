import Formal.InfiniteAggregation.Hyperplane
import Formal.InfiniteAggregation.GramSupport
import Formal.InfiniteAggregation.GramBound

namespace InfiniteAggregation

/-- Exact Gram-coordinate image of an arbitrary homogeneous hyperplane. -/
theorem homGram_image_kernel {r : ℕ} (hr : 2 ≤ r)
    (l : HomVar r →ₗ[ℝ] ℝ) (p q : Vec r) (s : ℝ)
    (hl : ∀ z, l z = dot p z.1.1 + dot q z.1.2 + s * z.2) :
    homGram '' (LinearMap.ker l : Set (HomVar r)) =
      hhcCoordinateDomain (qnorm p) (qnorm q) (dot p q) s := by
  have hdetH : 0 ≤ qnorm p * qnorm q - (dot p q) ^ 2 :=
    gram_det_nonneg (gramPSD_vectors p q)
  ext g
  constructor
  · rintro ⟨z, hz, rfl⟩
    have hlz : dot p z.1.1 + dot q z.1.2 = -s * z.2 := by
      have hz' : l z = 0 := hz
      rw [hl] at hz'
      linarith
    refine ⟨gramPSD_vectors z.1.1 z.1.2, sq_nonneg z.2, ?_⟩
    have hb := gram_support_upper hr p q z.1.1 z.1.2
    rw [Real.sqrt_mul hdetH, hlz] at hb
    change s ^ 2 * z.2 ^ 2 ≤ qnorm p * qnorm z.1.1 + qnorm q * qnorm z.1.2 +
      2 * dot p q * dot z.1.1 z.1.2 +
      2 * Real.sqrt (qnorm p * qnorm q - (dot p q) ^ 2) *
        Real.sqrt (qnorm z.1.1 * qnorm z.1.2 - (dot z.1.1 z.1.2) ^ 2)
    nlinarith [hb]
  · rintro ⟨hg, hT, hbound⟩
    let t := Real.sqrt (g 3)
    have ht : t ^ 2 = g 3 := Real.sq_sqrt hT
    have hw : (-s * t) ^ 2 ≤ qnorm p * g 0 + qnorm q * g 1 +
        2 * dot p q * g 2 +
        2 * Real.sqrt ((qnorm p * qnorm q - (dot p q) ^ 2) *
          (g 0 * g 1 - (g 2) ^ 2)) := by
      rw [Real.sqrt_mul hdetH]
      nlinarith [hbound]
    obtain ⟨u, v, hu, hv, huv, hwuv⟩ :=
      gram_support_attained hr p q hg.1 hg.2.1 hg.2.2 hw
    refine ⟨((u, v), t), ?_, ?_⟩
    · change l ((u, v), t) = 0
      rw [hl]
      change dot p u + dot q v + s * t = 0
      linarith
    · ext i
      fin_cases i <;> simpa [homGram] using (by assumption)

/-- The three-inequality family has hidden hyperplane convexity in every
ambient vector dimension at least two, including the four-variable example. -/
theorem hhc {r : ℕ} (hr : 2 ≤ r) : HHC r := by
  intro l _
  obtain ⟨p, q, s, hl⟩ := hom_functional_coefficients l
  have himage : homEval '' (LinearMap.ker l : Set (HomVar r)) =
      gramOutput '' hhcCoordinateDomain (qnorm p) (qnorm q) (dot p q) s := by
    rw [← homGram_image_kernel hr l p q s hl, Set.image_image]
    rfl
  rw [himage]
  exact (convex_hhcCoordinateDomain (qnorm p) (qnorm q) (dot p q) s).linear_image gramOutput

end InfiniteAggregation
