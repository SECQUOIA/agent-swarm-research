import Mathlib

/-! Coordinate-section obstructions to descriptions with unit coefficients. -/
namespace NetworkSimplex
open Filter Set
open scoped Topology

/-- A signed unit coefficient, including zero. -/
def UnitCoefficient (x : ℝ) : Prop := x = -1 ∨ x = 0 ∨ x = 1

/-- A row valid near a halfplane boundary and tight at the origin has the
same normal direction, with a nonnegative multiplier. -/
theorem local_halfplane_tight_normal {ε A B : ℝ} (hε : 0 < ε)
    (hvalid : ∀ u v : ℝ, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      0 ≤ A * u + B * v) : A = 2 * B ∧ 0 ≤ B := by
  have hp := hvalid (ε / 4) (-ε / 2) (by rw [abs_of_pos (by positivity)]; linarith)
    (by rw [abs_of_neg (by linarith)]; linarith) (by ring_nf; rfl)
  have hm := hvalid (-ε / 4) (ε / 2) (by rw [abs_of_neg (by linarith)]; linarith)
    (by rw [abs_of_pos (by positivity)]; linarith) (by ring_nf; rfl)
  have hi := hvalid 0 (ε / 2) (by simpa) (by rw [abs_of_pos (by positivity)]; linarith)
    (by positivity)
  constructor
  · nlinarith
  · nlinarith

/-- Every nonconstant tight valid row has a strictly positive normal multiplier. -/
theorem local_halfplane_tight_positive_multiple {ε A B : ℝ} (hε : 0 < ε)
    (hne : A ≠ 0 ∨ B ≠ 0)
    (hvalid : ∀ u v : ℝ, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      0 ≤ A * u + B * v) : ∃ t : ℝ, 0 < t ∧ A = 2 * t ∧ B = t := by
  have hn := local_halfplane_tight_normal hε hvalid
  refine ⟨B, ?_, hn.1, rfl⟩
  rcases hne with hA | hB
  · exact lt_of_le_of_ne hn.2 (by intro hz; apply hA; linarith)
  · exact lt_of_le_of_ne hn.2 (Ne.symm hB)

/-- A tight row with signed unit coefficients cannot support this boundary. -/
theorem local_halfplane_tight_unit_zero {ε A B : ℝ} (hε : 0 < ε)
    (hA : UnitCoefficient A) (hB : UnitCoefficient B)
    (hvalid : ∀ u v : ℝ, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      0 ≤ A * u + B * v) : A = 0 ∧ B = 0 := by
  have hn := local_halfplane_tight_normal hε hvalid
  rcases hA with hA | hA | hA <;> rcases hB with hB | hB | hB <;> constructor <;> linarith

/-- An affine equation valid throughout the local section vanishes identically
on the coordinate plane. Consequently equations cannot change its two normals. -/
theorem local_halfplane_equation_zero {ε A B c : ℝ} (hε : 0 < ε)
    (hvalid : ∀ u v : ℝ, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      c + A * u + B * v = 0) : A = 0 ∧ B = 0 ∧ c = 0 := by
  have h0 := hvalid 0 0 (by simpa) (by simpa) (by norm_num)
  have hu := hvalid (ε / 2) 0 (by rw [abs_of_pos (by positivity)]; linarith)
    (by simpa) (by positivity)
  have hv := hvalid 0 (ε / 2) (by simpa) (by rw [abs_of_pos (by positivity)]; linarith)
    (by positivity)
  constructor
  · nlinarith
  constructor <;> nlinarith

/-- Every valid signed-unit row also accepts a fixed point on the wrong side.
The same point works for all rows, so even an infinite family cannot suffice. -/
theorem local_halfplane_unit_row_accepts_exterior {ε A B c : ℝ} (hε : 0 < ε)
    (hA : UnitCoefficient A) (hB : UnitCoefficient B)
    (hvalid : ∀ u v : ℝ, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      0 ≤ c + A * u + B * v) : 0 ≤ c + A * (-ε / 8) + B * 0 := by
  have h0 := hvalid 0 0 (by simpa) (by simpa) (by norm_num)
  have hp := hvalid (ε / 4) (-ε / 2) (by rw [abs_of_pos (by positivity)]; linarith)
    (by rw [abs_of_neg (by linarith)]; linarith) (by ring_nf; rfl)
  have hm := hvalid (-ε / 4) (ε / 2) (by rw [abs_of_neg (by linarith)]; linarith)
    (by rw [abs_of_pos (by positivity)]; linarith) (by ring_nf; rfl)
  rcases hA with hA | hA | hA <;> rcases hB with hB | hB | hB <;>
    simp only [hA, hB] at * <;> nlinarith

/-- A finite affine description of the local section must have a nonconstant
active row. Its normal is a strictly positive multiple of the section normal.
Valid equations may be included, with no bound on their number. -/
theorem local_halfplane_description_positive_multiple {ι κ : Type*} [Finite ι]
    {ε : ℝ} (hε : 0 < ε) (A B c : ι → ℝ) (D E f : κ → ℝ)
    (hd : ∀ u v : ℝ, |u| < ε → |v| < ε →
      ((∀ i, 0 ≤ c i + A i * u + B i * v) ∧
        (∀ j, f j + D j * u + E j * v = 0) ↔ 0 ≤ 2 * u + v)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ c i = 0 ∧ A i = 2 * t ∧ B i = t := by
  have hrow : ∀ i u v, |u| < ε → |v| < ε → 0 ≤ 2 * u + v →
      0 ≤ c i + A i * u + B i * v :=
    fun i u v hu hv hh => ((hd u v hu hv).mpr hh).1 i
  have hc : ∀ i, 0 ≤ c i := by
    intro i
    simpa using hrow i 0 0 (by simpa) (by simpa) (by norm_num)
  have heq : ∀ j, D j = 0 ∧ E j = 0 ∧ f j = 0 := by
    intro j
    exact local_halfplane_equation_zero hε
      (fun u v hu hv hh => ((hd u v hu hv).mpr hh).2 j)
  have hactive : ∃ i, c i = 0 ∧ (A i ≠ 0 ∨ B i ≠ 0) := by
    by_contra hn
    have hz : ∀ i, c i = 0 → A i = 0 ∧ B i = 0 := by
      intro i hi
      by_contra hAB
      exact hn ⟨i, hi, by simpa only [not_and_or, not_not] using hAB⟩
    have hev : ∀ᶠ t : ℝ in 𝓝 0, ∀ i, 0 ≤ c i + A i * (-t) + B i * 0 := by
      apply eventually_all.mpr
      intro i
      by_cases hi : c i = 0
      · have hzi := hz i hi
        simp [hi, hzi.1, hzi.2]
      · have hci : 0 < c i := lt_of_le_of_ne (hc i) (Ne.symm hi)
        have hcont : ContinuousAt (fun t : ℝ => c i + A i * (-t) + B i * 0) 0 := by
          fun_prop
        have hp := hcont.eventually (eventually_gt_nhds (show
          (0 : ℝ) < c i + A i * (-0) + B i * 0 by simpa using hci))
        exact hp.mono (fun _ ht => ht.le)
    have hev' : ∀ᶠ t : ℝ in 𝓝[>] 0,
        (∀ i, 0 ≤ c i + A i * (-t) + B i * 0) ∧ 0 < t ∧ t < ε := by
      filter_upwards [hev.filter_mono nhdsWithin_le_nhds,
        self_mem_nhdsWithin, (eventually_lt_nhds hε).filter_mono nhdsWithin_le_nhds]
        with t ht ht0 htε
      exact ⟨ht, ht0, htε⟩
    obtain ⟨t, ht, ht0, htε⟩ := hev'.exists
    have hbad := (hd (-t) 0 (by simpa [abs_of_pos ht0] using htε) (by simpa)).mp
      ⟨ht, fun j => by simp [(heq j).1, (heq j).2.1, (heq j).2.2]⟩
    linarith
  obtain ⟨i, hci, hi⟩ := hactive
  obtain ⟨t, ht, hAt, hBt⟩ := local_halfplane_tight_positive_multiple hε hi
    (fun u v hu hv hh => by simpa [hci] using hrow i u v hu hv hh)
  exact ⟨i, t, ht, hci, hAt, hBt⟩

/-- No family of affine signed-unit inequalities, together with any valid affine
equations, gives the section `2u + v ≥ 0` locally. Indices need not be finite. -/
theorem local_halfplane_not_unit_description {ι κ : Type*} {ε : ℝ} (hε : 0 < ε)
    (A B c : ι → ℝ) (D E f : κ → ℝ)
    (hA : ∀ i, UnitCoefficient (A i)) (hB : ∀ i, UnitCoefficient (B i)) :
    ¬ (∀ u v : ℝ, |u| < ε → |v| < ε →
      ((∀ i, 0 ≤ c i + A i * u + B i * v) ∧
        (∀ j, f j + D j * u + E j * v = 0) ↔ 0 ≤ 2 * u + v)) := by
  intro hd
  have hi : ∀ i, 0 ≤ c i + A i * (-ε / 8) + B i * 0 := by
    intro i
    apply local_halfplane_unit_row_accepts_exterior hε (hA i) (hB i)
    intro u v hu hv hh
    exact ((hd u v hu hv).mpr hh).1 i
  have he : ∀ j, f j + D j * (-ε / 8) + E j * 0 = 0 := by
    intro j
    have hz := local_halfplane_equation_zero hε (A := D j) (B := E j) (c := f j)
      (fun u v hu hv hh => ((hd u v hu hv).mpr hh).2 j)
    simp [hz.1, hz.2.1, hz.2.2]
  have hn := (hd (-ε / 8) 0
    (by rw [abs_of_neg (by linarith)]; linarith) (by simpa)).mp ⟨hi, he⟩
  linarith

end NetworkSimplex
