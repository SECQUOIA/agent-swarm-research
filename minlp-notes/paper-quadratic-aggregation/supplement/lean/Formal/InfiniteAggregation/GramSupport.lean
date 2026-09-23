import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.GramFrame

namespace InfiniteAggregation

/-- Every scalar between the extrema of a linear functional on the unit circle
is attained. The formula also covers the zero functional. -/
theorem circle_linear_surjective {A B w : ℝ} (hw : w ^ 2 ≤ A ^ 2 + B ^ 2) :
    ∃ x y : ℝ, x ^ 2 + y ^ 2 = 1 ∧ A * x + B * y = w := by
  by_cases hz : A ^ 2 + B ^ 2 = 0
  · have hA : A = 0 := by nlinarith [sq_nonneg B]
    have hB : B = 0 := by nlinarith [sq_nonneg A]
    have hw0 : w = 0 := by nlinarith [sq_nonneg w]
    exact ⟨1, 0, by norm_num, by simp [hA, hB, hw0]⟩
  · let d := A ^ 2 + B ^ 2
    have hd : 0 < d := lt_of_le_of_ne (by dsimp [d]; positivity) (Ne.symm hz)
    let z := Real.sqrt (d - w ^ 2)
    have hz2 : z ^ 2 = d - w ^ 2 := Real.sq_sqrt (by dsimp [d]; linarith)
    refine ⟨(A * w - B * z) / d, (B * w + A * z) / d, ?_, ?_⟩
    · field_simp
      dsimp [d] at *
      nlinarith [sq_nonneg (A * w - B * z), sq_nonneg (B * w + A * z)]
    · field_simp
      dsimp [d]
      ring

/-- Rotation of a two-column Gram factor gives every value allowed by its
linear-functional amplitude. -/
theorem rotation_gram_surjective {P Q R d k l w : ℝ}
    (hw : w ^ 2 ≤ (P * d + Q * k + R * l) ^ 2 + (R * k - Q * l) ^ 2) :
    ∃ u₁ u₂ v₁ v₂ : ℝ,
      u₁ ^ 2 + u₂ ^ 2 = d ^ 2 ∧
      v₁ ^ 2 + v₂ ^ 2 = k ^ 2 + l ^ 2 ∧
      u₁ * v₁ + u₂ * v₂ = d * k ∧
      P * u₁ + Q * v₁ + R * v₂ = w := by
  obtain ⟨x, y, hxy, hwxy⟩ := circle_linear_surjective hw
  refine ⟨d * x, d * y, k * x - l * y, k * y + l * x, ?_, ?_, ?_, ?_⟩
  · nlinarith [congrArg (fun z : ℝ => d ^ 2 * z) hxy]
  · nlinarith [congrArg (fun z : ℝ => (k ^ 2 + l ^ 2) * z) hxy]
  · nlinarith [congrArg (fun z : ℝ => (d * k) * z) hxy]
  · nlinarith [hwxy]

/-- Constructive two-dimensional support formula, including singular Gram
matrices and zero linear functionals. -/
theorem scalar_gram_support {P Q R a b c w : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hc : c ^ 2 ≤ a * b)
    (hw : w ^ 2 ≤ P ^ 2 * a + (Q ^ 2 + R ^ 2) * b + 2 * P * Q * c +
      2 * P * R * Real.sqrt (a * b - c ^ 2)) :
    ∃ u₁ u₂ v₁ v₂ : ℝ,
      u₁ ^ 2 + u₂ ^ 2 = a ∧
      v₁ ^ 2 + v₂ ^ 2 = b ∧
      u₁ * v₁ + u₂ * v₂ = c ∧
      P * u₁ + Q * v₁ + R * v₂ = w := by
  by_cases ha0 : a = 0
  · have hc0 : c = 0 := by nlinarith [sq_nonneg c]
    have hs : (Real.sqrt b) ^ 2 = b := Real.sq_sqrt hb
    have hw' : w ^ 2 ≤ (Q * Real.sqrt b) ^ 2 + (R * Real.sqrt b) ^ 2 := by
      simpa [ha0, hc0, mul_pow, hs, add_mul] using hw
    obtain ⟨x, y, hxy, hwxy⟩ := circle_linear_surjective hw'
    refine ⟨0, 0, Real.sqrt b * x, Real.sqrt b * y, by simp [ha0], ?_,
      by simp [hc0], ?_⟩
    · nlinarith [congrArg (fun z : ℝ => b * z) hxy]
    · nlinarith [hwxy]
  · have hap : 0 < a := lt_of_le_of_ne ha (Ne.symm ha0)
    let d := Real.sqrt a
    let k := c / d
    let l := Real.sqrt (a * b - c ^ 2) / d
    have hd : 0 < d := Real.sqrt_pos.2 hap
    have hd2 : d ^ 2 = a := Real.sq_sqrt ha
    have hl2 : (Real.sqrt (a * b - c ^ 2)) ^ 2 = a * b - c ^ 2 :=
      Real.sq_sqrt (by linarith)
    have hdk : d * k = c := by dsimp [k]; field_simp
    have hdl : d * l = Real.sqrt (a * b - c ^ 2) := by dsimp [l]; field_simp
    have hkl : k ^ 2 + l ^ 2 = b := by
      dsimp [k, l]
      field_simp
      nlinarith
    have hw' : w ^ 2 ≤ (P * d + Q * k + R * l) ^ 2 + (R * k - Q * l) ^ 2 := by
      have heq : (P * d + Q * k + R * l) ^ 2 + (R * k - Q * l) ^ 2 =
          P ^ 2 * a + (Q ^ 2 + R ^ 2) * b + 2 * P * Q * c +
            2 * P * R * Real.sqrt (a * b - c ^ 2) := by
        rw [← hdl, ← hd2, ← hkl, ← hdk]
        ring
      rwa [heq]
    obtain ⟨u₁, u₂, v₁, v₂, hu, hv, huv, hwuv⟩ := rotation_gram_surjective hw'
    exact ⟨u₁, u₂, v₁, v₂, hu.trans hd2, hv.trans hkl, huv.trans hdk, hwuv⟩

/-- The full support interval of a prescribed two-vector Gram fiber is attained
in every ambient dimension at least two. -/
theorem gram_support_attained {r : ℕ} (hr : 2 ≤ r) (p q : Vec r)
    {a b c w : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : c ^ 2 ≤ a * b)
    (hw : w ^ 2 ≤ qnorm p * a + qnorm q * b + 2 * dot p q * c +
      2 * Real.sqrt ((qnorm p * qnorm q - (dot p q) ^ 2) * (a * b - c ^ 2))) :
    ∃ u v : Vec r, qnorm u = a ∧ qnorm v = b ∧ dot u v = c ∧
      dot p u + dot q v = w := by
  obtain ⟨e, f, P, Q, R, he, hf, hef, hP, hR, hp, hq⟩ := exists_gram_frame hr p q
  have hfe : dot f e = 0 := by rw [dot_comm]; exact hef
  have he' : dot e e = 1 := he
  have hf' : dot f f = 1 := hf
  have hef' : dot e f = 0 := hef
  have hnP : qnorm p = P ^ 2 := by
    rw [hp, qnorm_smul]
    change P ^ 2 * dot e e = _
    rw [he']; ring
  have hnQ : qnorm q = Q ^ 2 + R ^ 2 := by
    simp only [hq, qnorm, dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, he', hf', hef', hfe]
    ring
  have hPQ : dot p q = P * Q := by
    simp only [hp, hq, dot_smul_left, dot_add_right, dot_smul_right, he', hef']
    ring
  have hsqrt : Real.sqrt ((qnorm p * qnorm q - (dot p q) ^ 2) * (a * b - c ^ 2)) =
      P * R * Real.sqrt (a * b - c ^ 2) := by
    rw [hnP, hnQ, hPQ]
    have heq : (P ^ 2 * (Q ^ 2 + R ^ 2) - (P * Q) ^ 2) * (a * b - c ^ 2) =
        (P * R) ^ 2 * (a * b - c ^ 2) := by ring
    rw [heq, Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (mul_nonneg hP hR)]
  rw [hsqrt, hnP, hnQ, hPQ] at hw
  have hw' : w ^ 2 ≤ P ^ 2 * a + (Q ^ 2 + R ^ 2) * b + 2 * P * Q * c +
      2 * P * R * Real.sqrt (a * b - c ^ 2) := by nlinarith only [hw]
  obtain ⟨u₁, u₂, v₁, v₂, hu, hv, huv, hwuv⟩ := scalar_gram_support ha hb hc hw'
  refine ⟨u₁ • e + u₂ • f, v₁ • e + v₂ • f, ?_, ?_, ?_, ?_⟩
  · simp only [qnorm, dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, he', hf', hef', hfe]
    nlinarith only [hu]
  · simp only [qnorm, dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, he', hf', hef', hfe]
    nlinarith only [hv]
  · simp only [dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, he', hf', hef', hfe]
    nlinarith only [huv]
  · simp only [hp, hq, dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, he', hf', hef', hfe]
    nlinarith only [hwuv]

end InfiniteAggregation
