import Formal.ReciprocalAnchor.ManyEnvelopeBound
import Formal.ReciprocalAnchor.ManyRationalLaw

/-! Rational slope-jump laws retain exact atom provenance after compression. -/
namespace ReciprocalAnchor.ManyLeaf

/-- Removing zero atoms preserves any predicate on each remaining atom. -/
theorem Law.compress_forall {a b : ℝ} (μ : Law a b) (P : ℝ → ℝ → Prop)
    (h : ∀ i, P (μ.mass i) (μ.location i)) :
    ∀ i, P (μ.compress.mass i) (μ.compress.location i) := by
  classical
  intro i
  exact h ((Fintype.equivFin μ.PositiveIndex).symm i)

/-- The compact rational law has masses equal to differences of input slopes
and locations equal to knots of the explicitly constructed rational partition. -/
theorem AffinePartition.exists_small_rational_law
    {ι : Type*} [Fintype ι] [Nonempty ι] {c d : ι → ℚ} {a b : ℚ}
    (P : AffinePartition c d a b) (m : ℚ)
    (hl : ∀ s ≤ (a : ℝ),
      affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) s = (m : ℝ) - s)
    (hr : ∀ s, (b : ℝ) ≤ s →
      affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) s = 0)
    (hleft : ∃ i, d i = -1) (hright : ∃ i, d i = 0) :
    ∃ μ : Law (a : ℝ) (b : ℝ), μ.size ≤ Fintype.card ι - 1 ∧ μ.mean = (m : ℝ) ∧
      μ.call = affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) ∧
      ∀ i, ∃ j k : ι, ∃ l : Fin (P.size + 1),
        μ.mass i = ((d j - d k : ℚ) : ℝ) ∧ μ.location i = (P.knot l : ℝ) := by
  let D := P.castRat.slopeData (m : ℝ) hl hr
  have hb : ∀ i < P.size + 1, (a : ℝ) ≤ D.knot i ∧ D.knot i ≤ (b : ℝ) := by
    intro i hi
    change (a : ℝ) ≤ P.castRat.natKnot i ∧ P.castRat.natKnot i ≤ (b : ℝ)
    rw [P.castRat.natKnot_fin ⟨i, hi⟩]
    exact P.castRat.knot_bounds ⟨i, hi⟩
  have hinput : ∀ k : Fin (P.size + 1 + 1), ∃ i, D.slope k = (d i : ℝ) := by
    intro k
    change ∃ i, P.castRat.padded (fun i => (d i : ℝ)) (-1) 0 k = (d i : ℝ)
    unfold AffinePartition.padded
    split_ifs with hzero hmid
    · obtain ⟨i, hi⟩ := hleft
      exact ⟨i, by simp [hi]⟩
    · exact ⟨_, rfl⟩
    · obtain ⟨i, hi⟩ := hright
      exact ⟨i, by simp [hi]⟩
  let μ := D.toLaw hb
  refine ⟨μ.compress, D.compressed_size_le (fun i => (d i : ℝ)) hb hinput, ?_, ?_, ?_⟩
  · exact μ.compress_mean.trans (D.toLaw_mean hb)
  · funext s
    exact (μ.compress_call s).trans ((D.toLaw_call hb s).trans
      (congrFun (P.castRat.slopeData_call (m : ℝ) hl hr) s))
  · apply μ.compress_forall (fun mass location => ∃ j k : ι, ∃ l : Fin (P.size + 1),
      mass = ((d j - d k : ℚ) : ℝ) ∧ location = (P.knot l : ℝ))
    intro i
    obtain ⟨j, hj⟩ := hinput i.succ
    obtain ⟨k, hk⟩ := hinput i.castSucc
    refine ⟨j, k, i, ?_, ?_⟩
    · change D.slope (i.val + 1) - D.slope i.val = ((d j - d k : ℚ) : ℝ)
      rw [show D.slope (i.val + 1) = (d j : ℝ) from hj,
        show D.slope i.val = (d k : ℝ) from hk, Rat.cast_sub]
    · change P.castRat.natKnot i.val = (P.knot i : ℝ)
      exact P.castRat.natKnot_fin i

end ReciprocalAnchor.ManyLeaf
