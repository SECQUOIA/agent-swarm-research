import Mathlib

namespace InfiniteAggregation

/-- The scalar positive-semidefinite conditions for a symmetric two-by-two matrix. -/
def GramPSD (a b c : ℝ) : Prop := 0 ≤ a ∧ 0 ≤ b ∧ c ^ 2 ≤ a * b

lemma gram_det_nonneg {a b c : ℝ} (h : GramPSD a b c) : 0 ≤ a * b - c ^ 2 :=
  sub_nonneg.mpr h.2.2

/-- The mixed determinant controls the product of the two determinant square roots. -/
lemma gram_det_mixed {a b c p q r : ℝ} (h : GramPSD a b c) (k : GramPSD p q r) :
    2 * (c * r + Real.sqrt (a * b - c ^ 2) * Real.sqrt (p * q - r ^ 2)) ≤
      a * q + b * p := by
  let d := Real.sqrt (a * b - c ^ 2)
  let e := Real.sqrt (p * q - r ^ 2)
  have hd : d ^ 2 = a * b - c ^ 2 := Real.sq_sqrt (gram_det_nonneg h)
  have he : e ^ 2 = p * q - r ^ 2 := Real.sq_sqrt (gram_det_nonneg k)
  have hcs : (c * r + d * e) ^ 2 ≤ (a * b) * (p * q) := by
    nlinarith [sq_nonneg (c * e - d * r)]
  have ham : 4 * ((a * b) * (p * q)) ≤ (a * q + b * p) ^ 2 := by
    nlinarith [sq_nonneg (a * q - b * p)]
  have hn : 0 ≤ a * q + b * p := add_nonneg (mul_nonneg h.1 k.2.1)
    (mul_nonneg h.2.1 k.1)
  change 2 * (c * r + d * e) ≤ a * q + b * p
  nlinarith

lemma gramPSD_add {a b c p q r : ℝ} (h : GramPSD a b c) (k : GramPSD p q r) :
    GramPSD (a + p) (b + q) (c + r) := by
  refine ⟨add_nonneg h.1 k.1, add_nonneg h.2.1 k.2.1, ?_⟩
  have hm := gram_det_mixed h k
  have hn := mul_nonneg (Real.sqrt_nonneg (a * b - c ^ 2))
    (Real.sqrt_nonneg (p * q - r ^ 2))
  nlinarith [h.2.2, k.2.2]

lemma gramPSD_smul {a b c t : ℝ} (h : GramPSD a b c) (ht : 0 ≤ t) :
    GramPSD (t * a) (t * b) (t * c) := by
  refine ⟨mul_nonneg ht h.1, mul_nonneg ht h.2.1, ?_⟩
  nlinarith [mul_nonneg (sq_nonneg t) (gram_det_nonneg h)]

lemma gram_sqrt_det_smul {a b c t : ℝ} (h : GramPSD a b c) (ht : 0 ≤ t) :
    Real.sqrt ((t * a) * (t * b) - (t * c) ^ 2) =
      t * Real.sqrt (a * b - c ^ 2) := by
  have hts := gram_det_nonneg (gramPSD_smul h ht)
  have hd := Real.sq_sqrt (gram_det_nonneg h)
  have he := Real.sq_sqrt hts
  have hn := mul_nonneg ht (Real.sqrt_nonneg (a * b - c ^ 2))
  have hsq : (t * Real.sqrt (a * b - c ^ 2)) ^ 2 =
      (t * a) * (t * b) - (t * c) ^ 2 := by
    rw [mul_pow, hd]
    ring
  nlinarith [Real.sqrt_nonneg ((t * a) * (t * b) - (t * c) ^ 2)]

lemma gram_sqrt_det_add {a b c p q r : ℝ} (h : GramPSD a b c) (k : GramPSD p q r) :
    Real.sqrt (a * b - c ^ 2) + Real.sqrt (p * q - r ^ 2) ≤
      Real.sqrt ((a + p) * (b + q) - (c + r) ^ 2) := by
  have hd := Real.sq_sqrt (gram_det_nonneg h)
  have he := Real.sq_sqrt (gram_det_nonneg k)
  have hf := Real.sq_sqrt (gram_det_nonneg (gramPSD_add h k))
  have hm := gram_det_mixed h k
  nlinarith [Real.sqrt_nonneg (a * b - c ^ 2), Real.sqrt_nonneg (p * q - r ^ 2),
    Real.sqrt_nonneg ((a + p) * (b + q) - (c + r) ^ 2)]

/-- The determinant square root is concave on the two-by-two PSD cone. -/
lemma gram_det_concave {a b c p q r u v : ℝ} (h : GramPSD a b c)
    (k : GramPSD p q r) (hu : 0 ≤ u) (hv : 0 ≤ v) :
    u * Real.sqrt (a * b - c ^ 2) + v * Real.sqrt (p * q - r ^ 2) ≤
      Real.sqrt ((u * a + v * p) * (u * b + v * q) - (u * c + v * r) ^ 2) := by
  have hm := gram_sqrt_det_add (gramPSD_smul h hu) (gramPSD_smul k hv)
  rw [gram_sqrt_det_smul h hu, gram_sqrt_det_smul k hv] at hm
  exact hm

/-- Coordinates of the Gram-image domain cut out by a single homogeneous hyperplane. -/
def hhcCoordinateDomain (h1 h2 h3 s : ℝ) : Set (Fin 4 → ℝ) :=
  {p | GramPSD (p 0) (p 1) (p 2) ∧ 0 ≤ p 3 ∧
    s ^ 2 * p 3 ≤ h1 * p 0 + h2 * p 1 + 2 * h3 * p 2 +
      2 * Real.sqrt (h1 * h2 - h3 ^ 2) * Real.sqrt (p 0 * p 1 - (p 2) ^ 2)}

/-- Concavity of the determinant square root gives convexity of every such domain. -/
theorem convex_hhcCoordinateDomain (h1 h2 h3 s : ℝ) :
    Convex ℝ (hhcCoordinateDomain h1 h2 h3 s) := by
  intro x hx y hy u v hu hv _
  rcases hx with ⟨hx, hxT, hxi⟩
  rcases hy with ⟨hy, hyT, hyi⟩
  change GramPSD (u * x 0 + v * y 0) (u * x 1 + v * y 1)
    (u * x 2 + v * y 2) ∧ 0 ≤ u * x 3 + v * y 3 ∧ _
  refine ⟨gramPSD_add (gramPSD_smul hx hu) (gramPSD_smul hy hv),
    add_nonneg (mul_nonneg hu hxT) (mul_nonneg hv hyT), ?_⟩
  change s ^ 2 * (u * x 3 + v * y 3) ≤
    h1 * (u * x 0 + v * y 0) + h2 * (u * x 1 + v * y 1) +
    2 * h3 * (u * x 2 + v * y 2) +
    2 * Real.sqrt (h1 * h2 - h3 ^ 2) *
      Real.sqrt ((u * x 0 + v * y 0) * (u * x 1 + v * y 1) -
        (u * x 2 + v * y 2) ^ 2)
  have hi := add_le_add (mul_le_mul_of_nonneg_left hxi hu)
    (mul_le_mul_of_nonneg_left hyi hv)
  have hc := mul_le_mul_of_nonneg_left (gram_det_concave hx hy hu hv)
    (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) (Real.sqrt_nonneg (h1 * h2 - h3 ^ 2)))
  nlinarith

end InfiniteAggregation
