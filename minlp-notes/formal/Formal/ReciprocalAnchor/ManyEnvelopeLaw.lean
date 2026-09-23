import Formal.ReciprocalAnchor.ManyEnvelope
import Formal.ReciprocalAnchor.ManySlopeJumps

/-! Reconstruction of an affine envelope as a bounded finite probability law. -/
namespace ReciprocalAnchor.ManyLeaf

namespace AffinePartition

variable {ι : Type*} [Fintype ι] [Nonempty ι] {c d : ι → ℝ} {a b : ℝ}
    (P : AffinePartition c d a b)

/-- Pad a list of active coefficients by the two exterior coefficients. -/
def padded (v : ι → ℝ) (left right : ℝ) (i : ℕ) : ℝ :=
  if h0 : i = 0 then left else if hi : i ≤ P.size then v (P.active ⟨i - 1, by omega⟩)
  else right

@[simp] theorem padded_zero (v : ι → ℝ) (left right : ℝ) :
    P.padded v left right 0 = left := by simp [padded]

@[simp] theorem padded_last (v : ι → ℝ) (left right : ℝ) :
    P.padded v left right (P.size + 1) = right := by simp [padded]

@[simp] theorem padded_succ (v : ι → ℝ) (left right : ℝ) (i : Fin P.size) :
    P.padded v left right (i.val + 1) = v (P.active i) := by
  simp [padded, Nat.succ_le_iff.mpr i.isLt]

def natKnot (i : ℕ) : ℝ := if hi : i < P.size + 1 then P.knot ⟨i, hi⟩ else b

@[simp] theorem natKnot_fin (i : Fin (P.size + 1)) :
    P.natKnot i.val = P.knot i := by simp [natKnot, i.isLt]

theorem knot_bounds (i : Fin (P.size + 1)) : a ≤ P.knot i ∧ P.knot i ≤ b := by
  constructor
  · exact P.first.symm.trans_le (P.strict.monotone (Fin.zero_le i))
  · exact (P.strict.monotone (Fin.le_last i)).trans_eq P.last

theorem piece_left (i : Fin P.size) :
    affineEnvelope c d (P.knot i.castSucc) =
      c (P.active i) + d (P.active i) * P.knot i.castSucc :=
  P.agrees i _ ⟨le_rfl, P.strict.monotone (by change i.val ≤ i.val + 1; omega)⟩

theorem piece_right (i : Fin P.size) :
    affineEnvelope c d (P.knot i.succ) =
      c (P.active i) + d (P.active i) * P.knot i.succ :=
  P.agrees i _ ⟨P.strict.monotone (by change i.val ≤ i.val + 1; omega), le_rfl⟩

theorem first_slope (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s) :
    -1 ≤ d (P.active ⟨0, P.pos⟩) := by
  have h0 := P.piece_left ⟨0, P.pos⟩
  have he : P.knot (⟨0, P.pos⟩ : Fin P.size).castSucc = a := P.first
  rw [he, hl a le_rfl] at h0
  have h1 := affine_le_envelope c d (P.active ⟨0, P.pos⟩) (a - 1)
  rw [hl (a - 1) (by linarith)] at h1
  nlinarith

theorem last_slope (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0) :
    d (P.active ⟨P.size - 1, by have := P.pos; omega⟩) ≤ 0 := by
  let i : Fin P.size := ⟨P.size - 1, by have := P.pos; omega⟩
  have hi : i.succ = Fin.last P.size := by apply Fin.ext; dsimp [i]; have := P.pos; omega
  have h0 := P.piece_right i
  rw [hi, P.last, hr b le_rfl] at h0
  have h1 := affine_le_envelope c d (P.active i) (b + 1)
  rw [hr (b + 1) (by linarith)] at h1
  dsimp [i] at *
  nlinarith

theorem consecutive_slopes (i : ℕ) (hi : i + 1 < P.size) :
    d (P.active ⟨i, by omega⟩) ≤ d (P.active ⟨i + 1, hi⟩) := by
  apply active_slopes_ordered c d
    (P.strict (show (⟨i, by omega⟩ : Fin (P.size + 1)) < ⟨i + 1, by omega⟩ from by
      simp)) (P.piece_left ⟨i, by omega⟩) (P.piece_left ⟨i + 1, hi⟩)

theorem padded_slope_mono (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0)
    (i : ℕ) (hi : i < P.size + 1) :
    P.padded d (-1) 0 i ≤ P.padded d (-1) 0 (i + 1) := by
  by_cases h0 : i = 0
  · subst i
    simpa only [padded_zero, P.padded_succ d (-1) 0 ⟨0, P.pos⟩] using P.first_slope m hl
  by_cases hn : i = P.size
  · subst i
    have hp : P.size - 1 + 1 = P.size := by have := P.pos; omega
    rw [padded_last, ← hp, P.padded_succ d (-1) 0 ⟨P.size - 1, by have := P.pos; omega⟩]
    exact P.last_slope hr
  have hi' : i < P.size := by omega
  have hp : i - 1 + 1 = i := by omega
  have hh := P.consecutive_slopes (i - 1) (by omega)
  simpa only [hp, ← P.padded_succ d (-1) 0 ⟨i - 1, by omega⟩,
    P.padded_succ d (-1) 0 ⟨i, hi'⟩] using hh

theorem padded_continuous (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0)
    (i : ℕ) (hi : i < P.size + 1) :
    P.padded c m 0 (i + 1) + P.padded d (-1) 0 (i + 1) * P.natKnot i =
      P.padded c m 0 i + P.padded d (-1) 0 i * P.natKnot i := by
  by_cases h0 : i = 0
  · subst i
    have h := P.piece_left ⟨0, P.pos⟩
    have hx : P.natKnot 0 = a := by
      exact (P.natKnot_fin (0 : Fin (P.size + 1))).trans P.first
    have he : P.knot (⟨0, P.pos⟩ : Fin P.size).castSucc = a := P.first
    rw [he, hl a le_rfl] at h
    simpa only [padded_zero, P.padded_succ c m 0 ⟨0, P.pos⟩,
      P.padded_succ d (-1) 0 ⟨0, P.pos⟩, hx, neg_one_mul, sub_eq_add_neg] using h.symm
  by_cases hn : i = P.size
  · subst i
    let j : Fin P.size := ⟨P.size - 1, by have := P.pos; omega⟩
    have hj : j.val + 1 = P.size := by dsimp [j]; have := P.pos; omega
    have hx : P.natKnot P.size = b := by
      exact (P.natKnot_fin (Fin.last P.size)).trans P.last
    have he : j.succ = Fin.last P.size := by apply Fin.ext; exact hj
    have h := P.piece_right j
    rw [he, P.last, hr b le_rfl] at h
    rw [padded_last, padded_last, hx, ← hj, P.padded_succ c m 0 j,
      P.padded_succ d (-1) 0 j]
    simpa using h
  have hi' : i < P.size := by omega
  let j : Fin P.size := ⟨i - 1, by omega⟩
  let k : Fin P.size := ⟨i, hi'⟩
  have hj : j.val + 1 = i := by dsimp [j]; omega
  have he : j.succ = k.castSucc := by apply Fin.ext; exact hj
  have hx : P.natKnot i = P.knot k.castSucc := P.natKnot_fin k.castSucc
  have h1 := P.piece_right j
  have h2 := P.piece_left k
  rw [he] at h1
  rw [show i + 1 = k.val + 1 from rfl, P.padded_succ c m 0 k,
    P.padded_succ d (-1) 0 k, hx, ← hj, P.padded_succ c m 0 j,
    P.padded_succ d (-1) 0 j]
  exact h2.symm.trans h1

noncomputable def slopeData (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0) : SlopeJumpData (P.size + 1) m where
  knot := P.natKnot
  intercept := P.padded c m 0
  slope := P.padded d (-1) 0
  slope_first := P.padded_zero d (-1) 0
  slope_last := P.padded_last d (-1) 0
  intercept_first := P.padded_zero c m 0
  intercept_last := P.padded_last c m 0
  slope_mono := P.padded_slope_mono m hl hr
  continuous_at := P.padded_continuous m hl hr

theorem slopeData_call (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0) :
    (P.slopeData m hl hr).call = affineEnvelope c d := by
  apply SlopeJumpData.call_eq_of_pieces
  intro s
  by_cases hsa : s ≤ a
  · refine ⟨0, by omega, ?_, ?_, ?_⟩
    · intro i hi; omega
    · intro i _ hi
      exact hsa.trans (by
        change a ≤ P.natKnot i
        rw [P.natKnot_fin ⟨i, hi⟩]
        exact (P.knot_bounds ⟨i, hi⟩).1)
    · simpa [slopeData, sub_eq_add_neg] using hl s hsa
  by_cases hbs : b ≤ s
  · refine ⟨P.size + 1, le_rfl, ?_, ?_, ?_⟩
    · intro i hi
      apply le_trans _ hbs
      change P.natKnot i ≤ b
      rw [P.natKnot_fin ⟨i, hi⟩]
      exact (P.knot_bounds ⟨i, hi⟩).2
    · intro i hi hi'; omega
    · simpa [slopeData] using hr s hbs
  obtain ⟨j, hj⟩ := P.covers ⟨le_of_not_ge hsa, le_of_not_ge hbs⟩
  refine ⟨j.val + 1, by have := j.isLt; omega, ?_, ?_, ?_⟩
  · intro i hi
    change P.natKnot i ≤ s
    have hi' : i < P.size + 1 := by have := j.isLt; omega
    rw [P.natKnot_fin ⟨i, hi'⟩]
    exact (P.strict.monotone (show (⟨i, hi'⟩ : Fin (P.size + 1)) ≤ j.castSucc by
      simp only [Fin.le_def, Fin.val_castSucc]; omega)).trans hj.1
  · intro i hi hi'
    change s ≤ P.natKnot i
    rw [P.natKnot_fin ⟨i, hi'⟩]
    exact hj.2.trans (P.strict.monotone
      (show j.succ ≤ (⟨i, hi'⟩ : Fin (P.size + 1)) from hi))
  · simpa only [slopeData, P.padded_succ c m 0 j, P.padded_succ d (-1) 0 j] using
      P.agrees j s hj

include P in
/-- The envelope is exactly the call function of a finite bounded probability
law, whose mean is the left exterior intercept. -/
theorem exists_law (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0) :
    ∃ μ : Law a b, μ.mean = m ∧ μ.call = affineEnvelope c d := by
  let D := P.slopeData m hl hr
  have hb : ∀ i < P.size + 1, a ≤ D.knot i ∧ D.knot i ≤ b := by
    intro i hi
    change a ≤ P.natKnot i ∧ P.natKnot i ≤ b
    rw [P.natKnot_fin ⟨i, hi⟩]
    exact P.knot_bounds ⟨i, hi⟩
  refine ⟨D.toLaw hb, D.toLaw_mean hb, ?_⟩
  funext s
  exact (D.toLaw_call hb s).trans (congrFun (P.slopeData_call m hl hr) s)

end AffinePartition
end ReciprocalAnchor.ManyLeaf
