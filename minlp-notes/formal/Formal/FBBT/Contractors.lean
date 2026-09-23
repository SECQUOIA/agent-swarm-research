import Mathlib

namespace FBBT

/-- A closed box for the feedback variables `z,w`. -/
structure FeedbackBox where
  lz : ℝ
  lw : ℝ
  uz : ℝ
  uw : ℝ

def FeedbackBox.Mem (B : FeedbackBox) (p : ℝ × ℝ) : Prop :=
  B.lz ≤ p.1 ∧ p.1 ≤ B.uz ∧ B.lw ≤ p.2 ∧ p.2 ≤ B.uw

/-- Exact interval hull, characterized without any numerical algorithm. -/
def IsFeedbackHull (S : Set (ℝ × ℝ)) (B : FeedbackBox) : Prop :=
  (∀ p ∈ S, B.Mem p) ∧
  (∀ D : FeedbackBox, (∀ p ∈ S, D.Mem p) → ∀ p, B.Mem p → D.Mem p)

theorem feedbackHull_mono {S T : Set (ℝ × ℝ)} {B D : FeedbackBox}
    (hB : IsFeedbackHull S B) (hD : IsFeedbackHull T D) (hST : S ⊆ T) :
    ∀ p, B.Mem p → D.Mem p :=
  hB.2 D (fun p hp => hD.1 p (hST hp))

/-- Reachable boxes retain the feasible point `(1,c)` and the lower-bound invariant. -/
structure Good (b c : ℝ) (B : FeedbackBox) : Prop where
  b_pos : 0 < b
  c_pos : 0 < c
  sum_eq : b + c = 1
  lz_nonneg : 0 ≤ B.lz
  lw_nonneg : 0 ≤ B.lw
  lw_le : B.lw ≤ c * B.lz
  lz_le_one : B.lz ≤ 1
  uz_eq : B.uz = 1
  uw_lower : c ≤ B.uw
  uw_upper : B.uw ≤ 1

def initialBox : FeedbackBox := ⟨0, 0, 1, 1⟩
def productUpdate (c : ℝ) (B : FeedbackBox) : FeedbackBox :=
  ⟨B.lz, c * B.lz, 1, c⟩
def affineUpdate (b c : ℝ) (B : FeedbackBox) : FeedbackBox :=
  ⟨max B.lz (b + B.lw), max B.lw (B.lz - b), 1, c⟩

theorem initial_good {b c : ℝ} (hb : 0 < b) (hc : 0 < c) (hs : b + c = 1) :
    Good b c initialBox := by
  constructor <;> simp_all [initialBox]
  linarith

theorem Good.product_good {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    Good b c (productUpdate c B) := by
  constructor
  · exact h.b_pos
  · exact h.c_pos
  · exact h.sum_eq
  · exact h.lz_nonneg
  · exact mul_nonneg h.c_pos.le h.lz_nonneg
  · exact le_rfl
  · exact h.lz_le_one
  · rfl
  · exact le_rfl
  · dsimp [productUpdate]; linarith [h.sum_eq, h.b_pos]

theorem Good.affine_lz_le {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    (affineUpdate b c B).lz ≤ b + c * B.lz := by
  dsimp [affineUpdate]
  apply max_le
  · nlinarith [h.b_pos, h.sum_eq, h.lz_le_one]
  · linarith [h.lw_le]

theorem Good.affine_good {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    Good b c (affineUpdate b c B) := by
  have hc : c ≤ 1 := by linarith [h.sum_eq, h.b_pos]
  have hlw : B.lw ≤ c := le_trans h.lw_le (by nlinarith [h.c_pos, h.lz_le_one])
  have hz : B.lz ≤ max B.lz (b+B.lw) := le_max_left _ _
  constructor
  · exact h.b_pos
  · exact h.c_pos
  · exact h.sum_eq
  · exact le_trans h.lz_nonneg hz
  · exact le_trans h.lw_nonneg (le_max_left _ _)
  · dsimp [affineUpdate]
    apply max_le
    · exact le_trans h.lw_le (mul_le_mul_of_nonneg_left hz h.c_pos.le)
    · have hm := mul_le_mul_of_nonneg_left hz h.c_pos.le
      nlinarith [h.b_pos, h.sum_eq, h.lz_le_one]
  · dsimp [affineUpdate]; exact max_le h.lz_le_one (by linarith [h.sum_eq])
  · rfl
  · exact le_rfl
  · exact hc

/-- The product primitive computes the exact simultaneous hull, including reverse propagation. -/
theorem Good.product_hull {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    IsFeedbackHull {p | B.Mem p ∧ p.2 = c * p.1} (productUpdate c B) := by
  have hlo : B.Mem (B.lz, c * B.lz) := by
    refine ⟨le_rfl, ?_, h.lw_le, ?_⟩
    · simpa [h.uz_eq] using h.lz_le_one
    · nlinarith [h.c_pos, h.lz_le_one, h.uw_lower]
  have hhi : B.Mem (1,c) := by
    refine ⟨h.lz_le_one, ?_, ?_, h.uw_lower⟩
    · rw [h.uz_eq]
    · nlinarith [h.lw_le, h.c_pos, h.lz_le_one]
  constructor
  · rintro ⟨z,w⟩ ⟨hp, heq⟩
    rcases hp with ⟨hzlo,hzhi,hwlo,hwhi⟩
    dsimp [FeedbackBox.Mem, productUpdate] at *
    refine ⟨hzlo, ?_, ?_, ?_⟩
    · simpa [h.uz_eq] using hzhi
    · nlinarith [h.c_pos]
    · rw [h.uz_eq] at hzhi; nlinarith [h.c_pos]
  · intro D hD p hp
    have hdlo := hD (B.lz, c*B.lz) ⟨hlo,rfl⟩
    have hdhi := hD (1,c) ⟨hhi,by simp⟩
    dsimp [FeedbackBox.Mem, productUpdate] at *
    exact ⟨le_trans hdlo.1 hp.1, le_trans hp.2.1 hdhi.2.1,
      le_trans hdlo.2.2.1 hp.2.2.1, le_trans hp.2.2.2 hdhi.2.2.2⟩

/-- The affine primitive computes both variable bounds from the same input box. -/
theorem Good.affine_hull {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    IsFeedbackHull {p | B.Mem p ∧ p.1 = b + p.2} (affineUpdate b c B) := by
  let z := max B.lz (b+B.lw)
  let w := max B.lw (B.lz-b)
  have hwz : z = b+w := by
    dsimp [z,w]
    rcases le_total B.lz (b+B.lw) with hh|hh
    · rw [max_eq_right hh, max_eq_left (by linarith : B.lz-b ≤ B.lw)]
    · rw [max_eq_left hh, max_eq_right (by linarith : B.lw ≤ B.lz-b)]
      ring
  have hzw : z ≤ 1 := (h.affine_good).lz_le_one
  have hwc : w ≤ c := by linarith [h.sum_eq]
  have hlo : B.Mem (z,w) := by
    exact ⟨le_max_left _ _, by simpa [h.uz_eq] using hzw,
      le_max_left _ _, le_trans hwc h.uw_lower⟩
  have hhi : B.Mem (1,c) := by
    refine ⟨h.lz_le_one, by rw [h.uz_eq], ?_, h.uw_lower⟩
    nlinarith [h.lw_le,h.c_pos,h.lz_le_one]
  constructor
  · rintro ⟨x,y⟩ ⟨hp, heq⟩
    rcases hp with ⟨hxlo,hxhi,hylo,hyhi⟩
    dsimp [FeedbackBox.Mem, affineUpdate] at *
    refine ⟨max_le hxlo (by linarith), ?_, max_le hylo (by linarith), ?_⟩
    · simpa [h.uz_eq] using hxhi
    · rw [h.uz_eq] at hxhi; linarith [h.sum_eq]
  · intro D hD p hp
    have hdlo := hD (z,w) ⟨hlo,hwz⟩
    have hdhi := hD (1,c) ⟨hhi,h.sum_eq.symm⟩
    dsimp [FeedbackBox.Mem, affineUpdate, z, w] at *
    exact ⟨le_trans hdlo.1 hp.1, le_trans hp.2.1 hdhi.2.1,
      le_trans hdlo.2.2.1 hp.2.2.1, le_trans hp.2.2.2 hdhi.2.2.2⟩

theorem Good.feasible {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    B.Mem (1,c) := by
  refine ⟨h.lz_le_one, by rw [h.uz_eq], ?_, h.uw_lower⟩
  nlinarith [h.lw_le, h.c_pos, h.lz_le_one]

theorem Good.product_contracting {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    ∀ p, (productUpdate c B).Mem p → B.Mem p :=
  h.product_hull.2 B (fun _ hp => hp.1)

theorem Good.affine_contracting {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    ∀ p, (affineUpdate b c B).Mem p → B.Mem p :=
  h.affine_hull.2 B (fun _ hp => hp.1)

theorem product_lz_eq (c : ℝ) (B : FeedbackBox) :
    (productUpdate c B).lz = B.lz := rfl

theorem Good.product_lw_mono {b c : ℝ} {B : FeedbackBox} (h : Good b c B) :
    B.lw ≤ (productUpdate c B).lw := h.lw_le

theorem affine_lz_mono (b c : ℝ) (B : FeedbackBox) :
    B.lz ≤ (affineUpdate b c B).lz := le_max_left _ _

theorem affine_lw_mono (b c : ℝ) (B : FeedbackBox) :
    B.lw ≤ (affineUpdate b c B).lw := le_max_left _ _

theorem affine_forward (b c : ℝ) (B : FeedbackBox) :
    b+B.lw ≤ (affineUpdate b c B).lz := le_max_right _ _

theorem affine_reverse (b c : ℝ) (B : FeedbackBox) :
    B.lz-b ≤ (affineUpdate b c B).lw := le_max_right _ _

end FBBT
