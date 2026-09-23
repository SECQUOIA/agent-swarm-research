import Formal.ReciprocalAnchor.ManyEnvelopeLaw
import Formal.ReciprocalAnchor.ManyGeometry
import Formal.ReciprocalAnchor.ManyActiveCount
import Formal.ReciprocalAnchor.ManyLawCompress

/-! Removing zero jumps gives the sharp input-line bound on the number of atoms. -/
namespace ReciprocalAnchor.ManyLeaf

theorem SlopeJumpData.compressed_size_le {ι : Type*} [Fintype ι]
    {N : ℕ} {m a b : ℝ} (D : SlopeJumpData N m) (d : ι → ℝ)
    (hb : ∀ i < N, a ≤ D.knot i ∧ D.knot i ≤ b)
    (hinput : ∀ k : Fin (N + 1), ∃ i, D.slope k = d i) :
    (D.toLaw hb).compress.size ≤ Fintype.card ι - 1 := by
  classical
  let p : Fin (N + 1) → ℝ := fun k => D.slope k
  have hp : Monotone p := Fin.monotone_iff_le_succ.mpr (fun i => D.slope_mono i i.isLt)
  rw [Law.compress_size]
  have heq : (Finset.univ.filter fun i : Fin N => 0 < (D.toLaw hb).mass i) =
      slopeJumps p := by
    ext i
    simp [SlopeJumpData.toLaw, SlopeJumpData.mass, slopeJumps, p, sub_pos]
  change (Finset.univ.filter fun i : Fin N => 0 < (D.toLaw hb).mass i).card ≤ _
  rw [heq]
  exact slopeJumps_card_le p hp d hinput

/-- The two exterior slopes already occur among the input lines. -/
theorem AffinePartition.exists_small_law {ι : Type*} [Fintype ι] [Nonempty ι]
    {c d : ι → ℝ} {a b : ℝ} (P : AffinePartition c d a b) (m : ℝ)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0)
    (hleft : ∃ i, d i = -1) (hright : ∃ i, d i = 0) :
    ∃ μ : Law a b, μ.size ≤ Fintype.card ι - 1 ∧
      μ.mean = m ∧ μ.call = affineEnvelope c d := by
  let D := P.slopeData m hl hr
  have hb : ∀ i < P.size + 1, a ≤ D.knot i ∧ D.knot i ≤ b := by
    intro i hi
    change a ≤ P.natKnot i ∧ P.natKnot i ≤ b
    rw [P.natKnot_fin ⟨i, hi⟩]
    exact P.knot_bounds ⟨i, hi⟩
  have hinput : ∀ k : Fin (P.size + 1 + 1), ∃ i, D.slope k = d i := by
    intro k
    change ∃ i, P.padded d (-1) 0 k = d i
    unfold AffinePartition.padded
    split_ifs with hzero hmid
    · obtain ⟨i, hi⟩ := hleft
      exact ⟨i, hi.symm⟩
    · exact ⟨_, rfl⟩
    · obtain ⟨i, hi⟩ := hright
      exact ⟨i, hi.symm⟩
  let μ := D.toLaw hb
  refine ⟨μ.compress, D.compressed_size_le d hb hinput, ?_, ?_⟩
  · exact μ.compress_mean.trans (D.toLaw_mean hb)
  · funext s
    exact (μ.compress_call s).trans ((D.toLaw_call hb s).trans
      (congrFun (P.slopeData_call m hl hr) s))

/-- The existence theorem constructs its own partition from the input lines. -/
theorem affineEnvelope_exists_small_law {ι : Type*} [Fintype ι] [Nonempty ι]
    (c d : ι → ℝ) {a b m : ℝ} (hab : a < b)
    (hl : ∀ s ≤ a, affineEnvelope c d s = m - s)
    (hr : ∀ s, b ≤ s → affineEnvelope c d s = 0)
    (hleft : ∃ i, d i = -1) (hright : ∃ i, d i = 0) :
    ∃ μ : Law a b, μ.size ≤ Fintype.card ι - 1 ∧
      μ.mean = m ∧ μ.call = affineEnvelope c d := by
  obtain ⟨P⟩ := exists_affinePartition c d hab
  exact P.exists_small_law m hl hr hleft hright

/-- The least call envelope for `n` leaves has at most `2n+1` atoms. -/
theorem envelope_exists_small_law {n : ℕ} {a b m : ℝ} {q w : Fin n → ℝ}
    (hab : a < b) (h : LinearBounds a b m q w) :
    ∃ μ : Law a b, μ.size ≤ 2 * n + 1 ∧ μ.mean = m ∧ μ.call = envelope m q w := by
  have hl : ∀ s ≤ a, affineEnvelope (lineIntercept m q w) (lineSlope m q w) s = m - s := by
    intro s hs
    rw [← envelope_eq_affineEnvelope]
    exact envelope_left h hs
  have hr : ∀ s, b ≤ s → affineEnvelope (lineIntercept m q w) (lineSlope m q w) s = 0 := by
    intro s hs
    rw [← envelope_eq_affineEnvelope]
    exact envelope_right h hs
  obtain ⟨μ, hsize, hm, hc⟩ := affineEnvelope_exists_small_law
    (lineIntercept m q w) (lineSlope m q w) hab hl hr
    ⟨⟨2 * n + 1, by omega⟩, lineSlope_neg_one m q w⟩
    ⟨⟨2 * n, by omega⟩, lineSlope_zero m q w⟩
  refine ⟨μ, ?_, hm, hc.trans (envelope_eq_affineEnvelope m q w).symm⟩
  simpa using hsize

end ReciprocalAnchor.ManyLeaf
