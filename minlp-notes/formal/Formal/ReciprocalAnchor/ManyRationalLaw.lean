import Formal.ReciprocalAnchor.ManyEnvelopeLaw

/-! Rational envelope partitions yield finite laws with rational atoms and masses. -/
namespace ReciprocalAnchor.ManyLeaf
namespace AffinePartition

variable {ι : Type*} [Fintype ι] [Nonempty ι] {c d : ι → ℚ} {a b : ℚ}
    (P : AffinePartition c d a b)

/-- A rational partition remains an envelope partition at every real threshold.
Endpoint domination of affine lines proves the real interpolation assertion. -/
noncomputable def castRat :
    AffinePartition (fun i ↦ (c i : ℝ)) (fun i ↦ (d i : ℝ)) (a : ℝ) (b : ℝ) where
  size := P.size
  pos := P.pos
  knot i := (P.knot i : ℝ)
  strict := by
    intro i j hij
    change (P.knot i : ℝ) < (P.knot j : ℝ)
    exact_mod_cast P.strict hij
  first := by exact_mod_cast P.first
  last := by exact_mod_cast P.last
  active := P.active
  agrees := by
    intro i s hs
    apply (affineEnvelope_eq_iff _ _ _ _).mpr
    intro j
    have h0 := (affineEnvelope_eq_iff c d (P.active i) _).mp
      (P.agrees i (P.knot i.castSucc) ⟨le_rfl,
        P.strict.monotone (by change i.val ≤ i.val + 1; omega)⟩) j
    have h1 := (affineEnvelope_eq_iff c d (P.active i) _).mp
      (P.agrees i (P.knot i.succ) ⟨
        P.strict.monotone (by change i.val ≤ i.val + 1; omega), le_rfl⟩) j
    have h0r : (c j : ℝ) + (d j : ℝ) * (P.knot i.castSucc : ℝ) ≤
        (c (P.active i) : ℝ) + (d (P.active i) : ℝ) * (P.knot i.castSucc : ℝ) := by
      exact_mod_cast h0
    have h1r : (c j : ℝ) + (d j : ℝ) * (P.knot i.succ : ℝ) ≤
        (c (P.active i) : ℝ) + (d (P.active i) : ℝ) * (P.knot i.succ : ℝ) := by
      exact_mod_cast h1
    have hlt : (P.knot i.castSucc : ℝ) < (P.knot i.succ : ℝ) := by
      exact_mod_cast P.strict (show i.castSucc < i.succ from by simp)
    have hh0 := mul_nonneg (sub_nonneg.mpr h0r) (sub_nonneg.mpr hs.2)
    have hh1 := mul_nonneg (sub_nonneg.mpr h1r) (sub_nonneg.mpr hs.1)
    nlinarith

/-- Each padded coefficient in the cast partition is rational. -/
theorem castRat_padded_rational (v : ι → ℚ) (l r : ℚ) (i : ℕ) :
    ∃ q : ℚ, P.castRat.padded (fun j ↦ (v j : ℝ)) (l : ℝ) (r : ℝ) i = (q : ℝ) := by
  unfold padded
  split_ifs with h0 hi
  · exact ⟨l, rfl⟩
  · exact ⟨v (P.active ⟨i - 1, by simpa [castRat] using (show i - 1 < P.castRat.size by
        have := P.pos; dsimp [castRat] at *; omega)⟩), rfl⟩
  · exact ⟨r, rfl⟩

theorem castRat_natKnot_rational (i : ℕ) :
    ∃ q : ℚ, P.castRat.natKnot i = (q : ℝ) := by
  unfold natKnot
  split_ifs with hi
  · exact ⟨P.knot ⟨i, hi⟩, rfl⟩
  · exact ⟨b, rfl⟩

include P in
/-- Rational input coefficients admit an exact rational finite common-factor
law. The exterior identities identify its support interval and mean. -/
theorem exists_rational_law (m : ℚ)
    (hl : ∀ s ≤ (a : ℝ),
      affineEnvelope (fun i ↦ (c i : ℝ)) (fun i ↦ (d i : ℝ)) s = (m : ℝ) - s)
    (hr : ∀ s, (b : ℝ) ≤ s →
      affineEnvelope (fun i ↦ (c i : ℝ)) (fun i ↦ (d i : ℝ)) s = 0) :
    ∃ μ : Law (a : ℝ) (b : ℝ), μ.mean = (m : ℝ) ∧
      μ.call = affineEnvelope (fun i ↦ (c i : ℝ)) (fun i ↦ (d i : ℝ)) ∧
      ∀ i, ∃ p x : ℚ, μ.mass i = (p : ℝ) ∧ μ.location i = (x : ℝ) := by
  let D := P.castRat.slopeData (m : ℝ) hl hr
  have hb : ∀ i < P.size + 1, (a : ℝ) ≤ D.knot i ∧ D.knot i ≤ (b : ℝ) := by
    intro i hi
    change (a : ℝ) ≤ P.castRat.natKnot i ∧ P.castRat.natKnot i ≤ (b : ℝ)
    rw [P.castRat.natKnot_fin ⟨i, hi⟩]
    exact P.castRat.knot_bounds ⟨i, hi⟩
  refine ⟨D.toLaw hb, D.toLaw_mean hb, ?_, ?_⟩
  · funext s
    exact (D.toLaw_call hb s).trans (congrFun (P.castRat.slopeData_call (m : ℝ) hl hr) s)
  · intro i
    obtain ⟨p1, hp1⟩ := P.castRat_padded_rational d (-1) 0 (i.val + 1)
    obtain ⟨p0, hp0⟩ := P.castRat_padded_rational d (-1) 0 i.val
    obtain ⟨x, hx⟩ := P.castRat_natKnot_rational i.val
    refine ⟨p1 - p0, x, ?_, hx⟩
    change P.castRat.padded (fun j ↦ (d j : ℝ)) (-1) 0 (i.val + 1) -
      P.castRat.padded (fun j ↦ (d j : ℝ)) (-1) 0 i.val = ((p1 - p0 : ℚ) : ℝ)
    norm_cast at hp1 hp0 ⊢
    rw [hp1, hp0, Rat.cast_sub]

end AffinePartition
end ReciprocalAnchor.ManyLeaf
