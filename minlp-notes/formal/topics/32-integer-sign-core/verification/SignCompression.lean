import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import Lean.Util.CollectAxioms

/-! Local algebraic verification for integer-sign circuit compilation.
This file does not define circuits, a compiler, or a complexity model. -/

namespace IntegerSignCore

noncomputable section

def compress (M x : ℝ) : ℝ := 2 * M * x / (M + x ^ 2)

theorem denominator_pos {M : ℝ} (hM : 0 < M) (x : ℝ) :
    0 < M + x ^ 2 := by positivity

theorem compress_pos_iff {M x : ℝ} (hM : 0 < M) :
    0 < compress M x ↔ 0 < x := by
  unfold compress
  rw [div_pos_iff_of_pos_right (denominator_pos hM x)]
  exact mul_pos_iff_of_pos_left (by positivity)

theorem compress_abs {M x : ℝ} (hM : 0 < M) :
    |compress M x| = compress M |x| := by
  simp [compress, abs_div, abs_mul, abs_of_pos hM,
    abs_of_pos (denominator_pos hM x), sq_abs]

theorem compress_lower {M t : ℝ} (ht : 1 ≤ t) (htM : t ≤ M) :
    1 ≤ compress M t := by
  have hM : 0 < M := by linarith
  apply (le_div_iff₀ (denominator_pos hM t)).2
  have h₁ := mul_nonneg (sub_nonneg.mpr ht) (sub_nonneg.mpr htM)
  have h₂ := mul_nonneg (show 0 ≤ M - 1 by linarith) (show 0 ≤ t by linarith)
  nlinarith

theorem compress_sq_upper {M x : ℝ} (hM : 0 < M) :
    (compress M x) ^ 2 ≤ M := by
  unfold compress
  rw [div_pow]
  apply (div_le_iff₀ (sq_pos_of_pos (denominator_pos hM x))).2
  have h := mul_nonneg (le_of_lt hM) (sq_nonneg (M - x ^ 2))
  nlinarith

/-- The square bound is the nonnegative form of the square-root bound. -/
theorem compress_range {M x : ℝ} (hlo : 1 ≤ |x|) (hhi : |x| ≤ M) :
    1 ≤ |compress M x| ∧ (compress M x) ^ 2 ≤ M := by
  have hM : 0 < M := by linarith
  constructor
  · rw [compress_abs hM]
    exact compress_lower hlo hhi
  · exact compress_sq_upper hM

theorem compress_square_step {M x : ℝ} (hM : 1 ≤ M)
    (hlo : 1 ≤ |x|) (hhi : |x| ≤ M ^ 2) :
    1 ≤ |compress (M ^ 2) x| ∧ |compress (M ^ 2) x| ≤ M := by
  have hr := compress_range hlo hhi
  constructor
  · exact hr.1
  · have hsq : |compress (M ^ 2) x| ^ 2 ≤ M ^ 2 := by simpa only [sq_abs] using hr.2
    have hn := abs_nonneg (compress (M ^ 2) x)
    nlinarith

def Normalized (u : ℝ) : Prop := (-2 ≤ u ∧ u ≤ -1) ∨ (1 ≤ u ∧ u ≤ 2)

def normalize (x : ℝ) : ℝ := compress 4 (compress 16 x)

theorem normalize_range {x : ℝ} (hlo : 1 ≤ |x|) (hhi : |x| ≤ 16) :
    Normalized (normalize x) := by
  have h₀ := compress_square_step (M := 4) (x := x) (by norm_num) hlo (by norm_num; exact hhi)
  have h₁ := compress_square_step (M := 2) (x := compress 16 x)
    (by norm_num) (by norm_num at h₀; exact h₀.1) (by norm_num at h₀; norm_num; exact h₀.2)
  norm_num at h₁
  change 1 ≤ |normalize x| ∧ |normalize x| ≤ 2 at h₁
  by_cases h : 0 ≤ normalize x
  · right
    simpa only [abs_of_nonneg h] using h₁
  · left
    rw [abs_of_neg (lt_of_not_ge h)] at h₁
    constructor <;> linarith [h₁.1, h₁.2]

theorem normalize_pos_iff (x : ℝ) : 0 < normalize x ↔ 0 < x := by
  unfold normalize
  rw [compress_pos_iff (by norm_num : (0 : ℝ) < 4),
    compress_pos_iff (by norm_num : (0 : ℝ) < 16)]

def andGate (u v : ℝ) : ℝ := 2 * (u + v) - 3
def orGate (u v : ℝ) : ℝ := 2 * (u + v) + 3

theorem and_gate_ranges {u v : ℝ} (hu : Normalized u) (hv : Normalized v) :
    (-11 ≤ andGate u v ∧ andGate u v ≤ -1) ∨
      (1 ≤ andGate u v ∧ andGate u v ≤ 5) := by
  rcases hu with ⟨hu₀, hu₁⟩ | ⟨hu₀, hu₁⟩ <;>
    rcases hv with ⟨hv₀, hv₁⟩ | ⟨hv₀, hv₁⟩
  all_goals
    unfold andGate
    first | (left; constructor <;> linarith) | (right; constructor <;> linarith)

theorem or_gate_ranges {u v : ℝ} (hu : Normalized u) (hv : Normalized v) :
    (-5 ≤ orGate u v ∧ orGate u v ≤ -1) ∨
      (1 ≤ orGate u v ∧ orGate u v ≤ 11) := by
  rcases hu with ⟨hu₀, hu₁⟩ | ⟨hu₀, hu₁⟩ <;>
    rcases hv with ⟨hv₀, hv₁⟩ | ⟨hv₀, hv₁⟩
  all_goals
    unfold orGate
    first | (left; constructor <;> linarith) | (right; constructor <;> linarith)

theorem and_gate_pos_iff {u v : ℝ} (hu : Normalized u) (hv : Normalized v) :
    0 < andGate u v ↔ 0 < u ∧ 0 < v := by
  rcases hu with ⟨hu₀, hu₁⟩ | ⟨hu₀, hu₁⟩ <;>
    rcases hv with ⟨hv₀, hv₁⟩ | ⟨hv₀, hv₁⟩
  all_goals
    unfold andGate
    constructor
    · intro h
      constructor <;> linarith
    · rintro ⟨h₀, h₁⟩
      linarith

theorem or_gate_pos_iff {u v : ℝ} (hu : Normalized u) (hv : Normalized v) :
    0 < orGate u v ↔ 0 < u ∨ 0 < v := by
  rcases hu with ⟨hu₀, hu₁⟩ | ⟨hu₀, hu₁⟩ <;>
    rcases hv with ⟨hv₀, hv₁⟩ | ⟨hv₀, hv₁⟩
  all_goals
    unfold orGate
    constructor
    · intro h
      first | (left; linarith) | (right; linarith)
    · rintro (h | h) <;> linarith

theorem pair_denominator_pos {M P Q : ℝ} (hM : 0 < M) (hQ : 0 < Q) :
    0 < M * Q ^ 2 + P ^ 2 := by positivity

theorem pair_compress_identity {M P Q : ℝ} (hM : 0 < M) (hQ : 0 < Q) :
    compress M (P / Q) = (2 * M * P * Q) / (M * Q ^ 2 + P ^ 2) := by
  have hD := pair_denominator_pos (P := P) hM hQ
  have hE := denominator_pos hM (P / Q)
  unfold compress
  field_simp

def refine (t : ℝ) : ℝ := 2 * t / (1 + t ^ 2)

theorem refine_range {t : ℝ} (ht : 1 ≤ t) (ht₂ : t ≤ 2) :
    (4 : ℝ) / 5 ≤ refine t ∧ refine t ≤ 1 := by
  have hd : 0 < 1 + t ^ 2 := by positivity
  constructor
  · apply (le_div_iff₀ hd).2
    have h := mul_nonneg (show 0 ≤ t - 1 by linarith) (show 0 ≤ 2 - t by linarith)
    nlinarith
  · apply (div_le_iff₀ hd).2
    nlinarith [sq_nonneg (t - 1)]

theorem refine_error_identity (t : ℝ) :
    1 - refine t = (1 - t) ^ 2 / (1 + t ^ 2) := by
  have hd : 0 < 1 + t ^ 2 := by positivity
  unfold refine
  field_simp
  ring

theorem refine_error_bound (t : ℝ) :
    0 ≤ 1 - refine t ∧ 1 - refine t ≤ (1 - t) ^ 2 := by
  rw [refine_error_identity]
  have hd : 0 < 1 + t ^ 2 := by positivity
  constructor
  · positivity
  · apply (div_le_iff₀ hd).2
    nlinarith [mul_nonneg (sq_nonneg (1 - t)) (sq_nonneg t)]

theorem positive_threshold_margin {v w : ℝ} (hv : 1 ≤ v)
    (herr : |w - v| ≤ (1 : ℝ) / 4) : 1 ≤ 4 * w - 2 := by
  rcases abs_le.mp herr with ⟨h₀, h₁⟩
  linarith

theorem nonpositive_threshold_margin {v w : ℝ} (hv : v ≤ 0)
    (herr : |w - v| ≤ (1 : ℝ) / 4) : 4 * w - 2 ≤ -1 := by
  rcases abs_le.mp herr with ⟨h₀, h₁⟩
  linarith

theorem refine_odd (t : ℝ) : refine (-t) = -refine t := by
  simp [refine, neg_div]

theorem refine_signed_error {t s : ℝ} (hs : s ^ 2 = 1) :
    refine t - s = -s * (t - s) ^ 2 / (1 + t ^ 2) := by
  have hd : 0 < 1 + t ^ 2 := by positivity
  have hs₃ : s ^ 3 = s := by nlinarith [congrArg (fun x : ℝ => s * x) hs]
  unfold refine
  field_simp
  nlinarith [congrArg (fun x : ℝ => 2 * t * x) hs]

theorem refine_signed_error_bound {t s : ℝ} (hs : s ^ 2 = 1) :
    |refine t - s| ≤ |t - s| ^ 2 := by
  have hd : 0 < 1 + t ^ 2 := by positivity
  have hsabs : |s| = 1 := by
    rcases (sq_eq_one_iff).mp hs with h | h <;> simp [h]
  rw [refine_signed_error hs]
  simp only [abs_div, abs_mul, abs_neg, hsabs, one_mul, abs_sq,
    abs_of_pos hd, sq_abs]
  apply (div_le_iff₀ hd).2
  nlinarith [mul_nonneg (sq_nonneg (t - s)) (sq_nonneg t)]

def refineIter (t : ℝ) : ℕ → ℝ
  | 0 => t
  | r + 1 => refine (refineIter t r)

theorem refine_iter_error {t s : ℝ} (hs : s ^ 2 = 1) (r : ℕ) :
    |refineIter t r - s| ≤ |t - s| ^ (2 ^ r) := by
  induction r with
  | zero => simp [refineIter]
  | succ r ih =>
    calc
      |refineIter t (r + 1) - s| ≤ |refineIter t r - s| ^ 2 :=
        refine_signed_error_bound hs
      _ ≤ (|t - s| ^ (2 ^ r)) ^ 2 := by
        have h := abs_nonneg (refineIter t r - s)
        nlinarith
      _ = |t - s| ^ (2 ^ (r + 1)) := by rw [← pow_mul, pow_succ]

theorem product_error {a b a' b' B δ : ℝ}
    (hδ : 0 ≤ δ) (ha : |a| ≤ B) (hb : |b| ≤ B)
    (he : |a' - a| ≤ δ) (hf : |b' - b| ≤ δ) :
    |a' * b' - a * b| ≤ 2 * B * δ + δ ^ 2 := by
  have hB : 0 ≤ B := le_trans (abs_nonneg a) ha
  calc
    |a' * b' - a * b| =
        |(a' - a) * b + a * (b' - b) + (a' - a) * (b' - b)| := by congr 1; ring
    _ ≤ |(a' - a) * b + a * (b' - b)| + |(a' - a) * (b' - b)| := abs_add_le _ _
    _ ≤ (|(a' - a) * b| + |a * (b' - b)|) + |(a' - a) * (b' - b)| :=
      add_le_add (abs_add_le _ _) le_rfl
    _ = |a' - a| * |b| + |a| * |b' - b| + |a' - a| * |b' - b| := by
      simp only [abs_mul]
    _ ≤ δ * B + B * δ + δ * δ :=
      add_le_add
        (add_le_add (mul_le_mul he hb (abs_nonneg b) hδ)
          (mul_le_mul ha hf (abs_nonneg (b' - b)) hB))
        (mul_le_mul he hf (abs_nonneg (b' - b)) hδ)
    _ = 2 * B * δ + δ ^ 2 := by ring

theorem product_error_linear {a b a' b' B δ : ℝ}
    (hB : 1 ≤ B) (hδ : 0 ≤ δ) (hδ₁ : δ ≤ 1)
    (ha : |a| ≤ B) (hb : |b| ≤ B)
    (he : |a' - a| ≤ δ) (hf : |b' - b| ≤ δ) :
    |a' * b' - a * b| ≤ (3 * B) * δ := by
  have hp := product_error hδ ha hb he hf
  have h₀ := mul_nonneg hδ (sub_nonneg.mpr hδ₁)
  have h₁ := mul_nonneg (sub_nonneg.mpr hB) hδ
  nlinarith

end

end IntegerSignCore

/- Audit every declaration in this namespace, including auxiliary ones. -/
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let names ← env.constants.foldM (init := #[]) fun names name _ => do
    return if (`IntegerSignCore).isPrefixOf name then names.push name else names
  if names.isEmpty then throwError "empty integer-sign core audit"
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  for name in names do
    for ax in (← Lean.collectAxioms name) do
      unless allowed.contains ax do throwError "{name} depends on disallowed axiom {ax}"
  logInfo m!"PASS: audited {names.size} integer-sign core declarations."
