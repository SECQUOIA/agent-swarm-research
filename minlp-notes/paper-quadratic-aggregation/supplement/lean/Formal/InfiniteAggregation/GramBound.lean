import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.GramConcavity
import Formal.InfiniteAggregation.GramFrame

namespace InfiniteAggregation

open Matrix

lemma gramPSD_vectors {r : ℕ} (u v : Vec r) : GramPSD (qnorm u) (qnorm v) (dot u v) := by
  refine ⟨qnorm_nonneg u, qnorm_nonneg v, ?_⟩
  simpa [qnorm, dot, dotProduct, sq] using
    Finset.sum_mul_sq_le_sq_mul_sq Finset.univ u v

private lemma residual_dot {r : ℕ} (e f u v : Vec r)
    (he : dot e e = 1) (hf : dot f f = 1) (hef : dot e f = 0) :
    dot (u - (dot e u) • e - (dot f u) • f)
      (v - (dot e v) • e - (dot f v) • f) =
      dot u v - dot e u * dot e v - dot f u * dot f v := by
  simp only [dot, sub_dotProduct, dotProduct_sub, smul_dotProduct, dotProduct_smul,
    smul_eq_mul]
  change e ⬝ᵥ e = 1 at he
  change f ⬝ᵥ f = 1 at hf
  change e ⬝ᵥ f = 0 at hef
  rw [he, hf, hef, dotProduct_comm f e, hef, dotProduct_comm u e,
    dotProduct_comm u f]
  ring

/-- A two-frame trace estimate, including components outside the frame. -/
theorem frame_trace_bound {r : ℕ} (e f u v : Vec r)
    (he : dot e e = 1) (hf : dot f f = 1) (hef : dot e f = 0) :
    (dot e u + dot f v) ^ 2 ≤ qnorm u + qnorm v +
      2 * Real.sqrt (qnorm u * qnorm v - (dot u v) ^ 2) := by
  let x := dot e u
  let y := dot f u
  let z := dot e v
  let w := dot f v
  have hp : GramPSD (x ^ 2 + y ^ 2) (z ^ 2 + w ^ 2) (x * z + y * w) := by
    refine ⟨by positivity, by positivity, ?_⟩
    nlinarith [sq_nonneg (x * w - y * z)]
  have hr := gramPSD_vectors (u - x • e - y • f) (v - z • e - w • f)
  have hru : qnorm (u - x • e - y • f) = qnorm u - x ^ 2 - y ^ 2 := by
    simpa only [qnorm, x, y, sq] using residual_dot e f u u he hf hef
  have hrv : qnorm (v - z • e - w • f) = qnorm v - z ^ 2 - w ^ 2 := by
    simpa only [qnorm, z, w, sq] using residual_dot e f v v he hf hef
  have hrc : dot (u - x • e - y • f) (v - z • e - w • f) =
      dot u v - x * z - y * w := residual_dot e f u v he hf hef
  rw [hru, hrv, hrc] at hr
  have hsum := gram_sqrt_det_add hp hr
  have haa : x ^ 2 + y ^ 2 + (qnorm u - x ^ 2 - y ^ 2) = qnorm u := by ring
  have hbb : z ^ 2 + w ^ 2 + (qnorm v - z ^ 2 - w ^ 2) = qnorm v := by ring
  have hcc : x * z + y * w + (dot u v - x * z - y * w) = dot u v := by ring
  rw [haa, hbb, hcc] at hsum
  have hdet : (x ^ 2 + y ^ 2) * (z ^ 2 + w ^ 2) - (x * z + y * w) ^ 2 =
      (x * w - y * z) ^ 2 := by ring
  rw [hdet, Real.sqrt_sq_eq_abs] at hsum
  have hle := le_abs_self (x * w - y * z)
  have hnn := Real.sqrt_nonneg
    ((qnorm u - x ^ 2 - y ^ 2) * (qnorm v - z ^ 2 - w ^ 2) -
      (dot u v - x * z - y * w) ^ 2)
  change (x + w) ^ 2 ≤ _
  nlinarith [hr.1, hr.2.1, sq_nonneg (y - z)]

/-- The support function of the two-column Gram fibre has this universal upper bound. -/
theorem gram_support_upper {r : ℕ} (hr : 2 ≤ r) (p q u v : Vec r) :
    (dot p u + dot q v) ^ 2 ≤
      qnorm p * qnorm u + qnorm q * qnorm v + 2 * dot p q * dot u v +
        2 * Real.sqrt ((qnorm p * qnorm q - (dot p q) ^ 2) *
          (qnorm u * qnorm v - (dot u v) ^ 2)) := by
  obtain ⟨e, f, P, Q, R, he, hf, hef, _, _, hp, hq⟩ := exists_gram_frame hr p q
  have he' : dot e e = 1 := he
  have hf' : dot f f = 1 := hf
  have hef' : dot e f = 0 := hef
  have hne : qnorm e = 1 := he
  have hnf : qnorm f = 1 := hf
  have hb := frame_trace_bound e f (P • u + Q • v) (R • v) he' hf' hef'
  have hlin : dot e (P • u + Q • v) + dot f (R • v) = dot p u + dot q v := by
    rw [hp, hq]
    simp only [dot_add_left, dot_add_right, dot_smul_left, dot_smul_right]
    ring
  have hquad : qnorm (P • u + Q • v) + qnorm (R • v) =
      qnorm p * qnorm u + qnorm q * qnorm v + 2 * dot p q * dot u v := by
    rw [hp, hq]
    simp only [qnorm_add, qnorm_smul, dot_add_right, dot_smul_left,
      dot_smul_right, hne, hnf, he', hef']
    ring
  have hdet : qnorm (P • u + Q • v) * qnorm (R • v) -
      (dot (P • u + Q • v) (R • v)) ^ 2 =
      (qnorm p * qnorm q - (dot p q) ^ 2) *
        (qnorm u * qnorm v - (dot u v) ^ 2) := by
    rw [hp, hq]
    simp only [qnorm_add, qnorm_smul, dot_add_left, dot_add_right, dot_smul_left,
      dot_smul_right, hne, hnf, he', hef']
    rw [show dot v v = qnorm v from rfl]
    ring
  rw [hlin, hquad, hdet] at hb
  exact hb

end InfiniteAggregation
