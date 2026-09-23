import Formal.ReciprocalAnchor.ManyFastAtoms
import Formal.ReciprocalAnchor.ManyFastEvaluation
import Formal.ReciprocalAnchor.ManyFastLawGeometry

/-! The actual finite rational slope-jump law produced by the fast envelope algorithm. -/
namespace ReciprocalAnchor.ManyLeaf.FastEnvelope

/-- The producer has no real comparison or noncomputable choice. -/
def fastLaw {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) : List Atom :=
  (buildAtoms (sourceLines m q w)).1

theorem fastLaw_length {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) :
    (fastLaw m q w).length ≤ 2 * n + 1 := by
  have h := buildAtoms_length (sourceLines m q w)
  simpa [sourceLines, fastLaw] using h

theorem fastLaw_cost {n : ℕ} (m : ℚ) (q w : Fin n → ℚ) :
    (buildAtoms (sourceLines m q w)).2 ≤ (2 * n + 2) * ((2 * n + 2).log2 + 31) := by
  simpa [sourceLines] using buildAtoms_cost (sourceLines m q w)

theorem fastLaw_positive {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    {z : Atom} (hz : z ∈ fastLaw m q w) : 0 < z.mass :=
  slopeAtoms_positive _ (buildStack_good _) hz

/-- Exterior lines fix total mass and mean, and make the hinge reconstruction
exactly the original envelope. -/
theorem slopeAtoms_law_of_outer (rest : List Line) (m : ℚ)
    (hg : Good ((⟨0, 0⟩ : Line) :: rest))
    (hlast : rest.getLastD ⟨0, 0⟩ = ⟨-1, m⟩) :
    ((slopeAtoms ((⟨0, 0⟩ : Line) :: rest)).map Atom.mass).sum = 1 ∧
    ((slopeAtoms ((⟨0, 0⟩ : Line) :: rest)).map (fun z => z.mass * z.location)).sum = m ∧
    ∀ x : ℝ, atomCall (slopeAtoms ((⟨0, 0⟩ : Line) :: rest)) x =
      valueReal ((⟨0, 0⟩ : Line) :: rest) x := by
  refine ⟨?_, ?_, ?_⟩
  · rw [slopeAtoms_mass_sum, hlast]
    norm_num
  · rw [slopeAtoms_mean _ _ hg, hlast]
    norm_num
  · intro x
    rw [peak_valueReal _ (by simp), slopeAtoms_call hg x]
    simp only [Line.evalReal, Rat.cast_zero, zero_mul, zero_add]
    exact (max_eq_left (atomCall_nonneg _
      (fun z hz => (slopeAtoms_positive _ hg hz).le) x)).symm

theorem fastLaw_moments_call {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    ((fastLaw m q w).map Atom.mass).sum = 1 ∧
    ((fastLaw m q w).map (fun z => z.mass * z.location)).sum = m ∧
    ∀ x : ℝ, atomCall (fastLaw m q w) x =
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) x := by
  have hne : (buildStack (sourceLines m q w)).1 ≠ [] :=
    buildStack_nonempty _ (List.ne_nil_of_mem (sourceLines_zero m q w))
  cases hs : (buildStack (sourceLines m q w)).1 with
  | nil => exact False.elim (hne hs)
  | cons c rest =>
    have hc := sourceStack_head_zero h hs
    subst c
    have hl : rest.getLastD ⟨0, 0⟩ = ⟨-1, m⟩ := by
      simpa only [List.getLast_eq_getLastD, List.getLastD_cons] using sourceStack_last_mean h hs
    have hg : Good ((⟨0, 0⟩ : Line) :: rest) := hs ▸ buildStack_good _
    obtain ⟨ht, hm, he⟩ := slopeAtoms_law_of_outer rest m hg hl
    have hdef : fastLaw m q w = slopeAtoms ((⟨0, 0⟩ : Line) :: rest) := by
      simp only [fastLaw, buildAtoms, hs]
    rw [hdef]
    refine ⟨ht, hm, ?_⟩
    intro x
    rw [he, ← hs, buildStack_valueReal, sourceLines_valueReal]

theorem fastLaw_real_total {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    ((fastLaw m q w).map (fun z => (z.mass : ℝ))).sum = 1 := by
  have ht := (fastLaw_moments_call h).1
  have he := congrArg (fun z : ℚ => (z : ℝ)) ht
  simpa only [Rat.cast_list_sum, List.map_map, Function.comp_def, Rat.cast_one] using he

theorem fastLaw_real_mean {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    ((fastLaw m q w).map (fun z => (z.mass : ℝ) * z.location)).sum = (m : ℝ) := by
  have hm := (fastLaw_moments_call h).2.1
  have he := congrArg (fun z : ℚ => (z : ℝ)) hm
  simpa only [Rat.cast_list_sum, List.map_map, Function.comp_def, Rat.cast_mul] using he

theorem fastLaw_support {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    {z : Atom} (hz : z ∈ fastLaw m q w) : a ≤ z.location ∧ z.location ≤ b := by
  have he := (fastLaw_moments_call h).2.2
  have hleft : atomCall (fastLaw m q w) (a : ℝ) = (m : ℝ) - a :=
    (he a).trans (envelope_left h le_rfl)
  have hright : atomCall (fastLaw m q w) (b : ℝ) = 0 :=
    (he b).trans (envelope_right h le_rfl)
  have hb := atom_support _ (fun z hz => fastLaw_positive m q w hz)
    (fastLaw_real_total h) (fastLaw_real_mean h) hleft hright hz
  exact_mod_cast hb

open scoped BigOperators

def fastLawMass {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    (i : Fin (fastLaw m q w).length) : ℚ := ((fastLaw m q w).get i).mass

def fastLawLocation {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    (i : Fin (fastLaw m q w).length) : ℚ := ((fastLaw m q w).get i).location

theorem sum_get_map {α M : Type*} [AddCommMonoid M] (xs : List α) (f : α → M) :
    (∑ i : Fin xs.length, f (xs.get i)) = (xs.map f).sum := by
  rw [← List.sum_ofFn]
  change (List.ofFn (f ∘ xs.get)).sum = _
  rw [← List.map_ofFn, List.ofFn_get]

theorem fastLawMass_pos {n : ℕ} (m : ℚ) (q w : Fin n → ℚ)
    (i : Fin (fastLaw m q w).length) : 0 < fastLawMass m q w i :=
  fastLaw_positive m q w ((fastLaw m q w).get_mem i)

theorem fastLawMass_total {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    ∑ i, fastLawMass m q w i = 1 := by
  simpa only [fastLawMass, sum_get_map] using (fastLaw_moments_call h).1

theorem fastLawLocation_mean {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    ∑ i, fastLawMass m q w i * fastLawLocation m q w i = m := by
  change (∑ i, (fun z : Atom => z.mass * z.location) ((fastLaw m q w).get i)) = m
  rw [sum_get_map (fastLaw m q w) (fun z : Atom => z.mass * z.location)]
  exact (fastLaw_moments_call h).2.1

theorem fastLawLocation_bounds {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)))
    (i : Fin (fastLaw m q w).length) : a ≤ fastLawLocation m q w i ∧
      fastLawLocation m q w i ≤ b :=
  fastLaw_support h ((fastLaw m q w).get_mem i)

/-- The real interpretation of the computed rational arrays. Only the coercion
to the real-number specification is noncomputable; the arrays are executable. -/
noncomputable def fastLawAsLaw {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    Law (a : ℝ) (b : ℝ) where
  size := (fastLaw m q w).length
  mass i := fastLawMass m q w i
  location i := fastLawLocation m q w i
  nonneg i := by exact_mod_cast (fastLawMass_pos m q w i).le
  total := by exact_mod_cast fastLawMass_total h
  bounds i := by exact_mod_cast fastLawLocation_bounds h i

theorem fastLawAsLaw_mean {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) :
    (fastLawAsLaw h).mean = (m : ℝ) := by
  change ∑ i, (fastLawMass m q w i : ℝ) * fastLawLocation m q w i = _
  exact_mod_cast fastLawLocation_mean h

theorem fastLawAsLaw_call {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) (x : ℝ) :
    (fastLawAsLaw h).call x =
      envelope (m : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) x := by
  change (∑ i, (fastLawMass m q w i : ℝ) * max ((fastLawLocation m q w i : ℝ) - x) 0) = _
  change (∑ i, (fun z : Atom => (z.mass : ℝ) * max ((z.location : ℝ) - x) 0)
    ((fastLaw m q w).get i)) = _
  rw [sum_get_map (fastLaw m q w)
    (fun z : Atom => (z.mass : ℝ) * max ((z.location : ℝ) - x) 0)]
  exact (fastLaw_moments_call h).2.2 x

theorem fastLawAsLaw_reciprocal {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) (ha : 0 < a) :
    (fastLawAsLaw h).reciprocal =
      lowerMoment (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) := by
  rw [Law.reciprocal_eq_call_integral _ (by exact_mod_cast ha) (h.1.trans h.2.1),
    fastLawAsLaw_mean]
  simp only [fastLawAsLaw_call, lowerMoment]

theorem fastLaw_reciprocal_eq_fastLowerMoment {n : ℕ} {a b m : ℚ} {q w : Fin n → ℚ}
    (h : LinearBounds (a : ℝ) b m (fun j => (q j : ℝ)) (fun j => (w j : ℝ))) (ha : 0 < a) :
    (∑ i, fastLawMass m q w i / fastLawLocation m q w i) = fastLowerMoment a b m q w := by
  have he := (fastLawAsLaw_reciprocal h ha).trans
    (fastLowerMoment_eq ha (by exact_mod_cast h.1.trans h.2.1)).symm
  change (∑ i, (fastLawMass m q w i : ℝ) / fastLawLocation m q w i) = _ at he
  exact_mod_cast he

end ReciprocalAnchor.ManyLeaf.FastEnvelope
