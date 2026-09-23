import Mathlib

namespace QuadraticPrecision

/-- A direction satisfying all tight rows is feasible for a short positive step. -/
theorem finite_rows_small_step {ι : Type*} [Finite ι] (r d : ι → ℝ)
    (hr : ∀ i, r i ≤ 0) (hd : ∀ i, r i = 0 → d i ≤ 0) :
    ∃ δ : ℝ, 0 < δ ∧ ∀ i, r i + δ * d i ≤ 0 := by
  classical
  let := Fintype.ofFinite ι
  have h : ∀ s : Finset ι, ∃ δ : ℝ, 0 < δ ∧
      ∀ η : ℝ, 0 ≤ η → η ≤ δ → ∀ i ∈ s, r i + η * d i ≤ 0 := by
    intro s
    induction s using Finset.induction_on with
    | empty => exact ⟨1, by norm_num, by simp⟩
    | @insert i s hi ih =>
      obtain ⟨δ, hδ, hs⟩ := ih
      by_cases hri : r i = 0
      · refine ⟨δ, hδ, ?_⟩
        intro η hη hηδ j hj
        rcases Finset.mem_insert.mp hj with hji | hj
        · subst j
          simpa [hri] using mul_nonpos_of_nonneg_of_nonpos hη (hd i hri)
        · exact hs η hη hηδ j hj
      · have hneg : r i < 0 := lt_of_le_of_ne (hr i) hri
        refine ⟨min δ (-r i / (|d i| + 1)), lt_min hδ
          (div_pos (neg_pos.mpr hneg) (by positivity)), ?_⟩
        intro η hη hηδ j hj
        rcases Finset.mem_insert.mp hj with hji | hj
        · subst j
          have hηbound : η * (|d i| + 1) ≤ -r i :=
            (le_div_iff₀ (by positivity)).mp (hηδ.trans (min_le_right _ _))
          have hmul := mul_le_mul_of_nonneg_left (le_abs_self (d i)) hη
          nlinarith
        · exact hs η hη (hηδ.trans (min_le_left _ _)) j hj
  obtain ⟨δ, hδ, hs⟩ := h Finset.univ
  exact ⟨δ, hδ, fun i => hs δ hδ.le le_rfl i (Finset.mem_univ i)⟩

/-- Equal active patterns of minimum-height lifts force the square contact bound.
The hypotheses describe the numerical rows and heights of a local feasible
perturbation. This lemma needs no claim about projected facets or their count. -/
theorem square_contact_of_active_rows {ι : Type*} [Finite ι]
    (r s u : ι → ℝ) (a b ta tb ε : ℝ)
    (hr : ∀ i, r i ≤ 0) (hu : ∀ i, u i ≤ 0)
    (hactive : ∀ i, r i = 0 → s i = 0)
    (hmin : ∀ δ : ℝ, 0 < δ →
      (∀ i, r i + δ * (u i - (r i + s i)/2) ≤ 0) →
      ta ≤ ta + δ * (((a+b)/2) ^ 2 - (ta+tb)/2))
    (ha : a^2 - ε ≤ ta) (hb : b^2 - ε ≤ tb) :
    (a-b) ^ 2 ≤ 4*ε := by
  obtain ⟨δ, hδ, hrows⟩ := finite_rows_small_step r
    (fun i => u i - (r i + s i)/2) hr (by
      intro i hi
      simp only [hi, hactive i hi, add_zero, zero_div, sub_zero]
      exact hu i)
  have h := hmin δ hδ hrows
  have hc : (ta+tb)/2 ≤ ((a+b)/2) ^ 2 := by
    nlinarith
  nlinarith [sq_nonneg (a-b)]

/-- Evaluate an affine row along the contact perturbation. -/
theorem affine_contact_step {V : Type*} [AddCommGroup V] [Module ℝ V]
    (f : V →ᵃ[ℝ] ℝ) (p q z : V) (δ : ℝ) :
    f (p + δ • (z - ((1/2:ℝ) • p + (1/2:ℝ) • q))) =
      f p + δ * (f z - (f p + f q) / 2) := by
  rw [f.decomp]
  simp only [Pi.add_apply, map_add, map_sub, map_smul, smul_eq_mul]
  ring

/-- Actual finite affine systems: two minimum lifts sharing an active pattern
cannot be farther apart than the square-root error scale. Equalities are
unrestricted and do not contribute to the number of active patterns. -/
theorem square_contact_of_minimum_lifts
    {V ι κ : Type*} [AddCommGroup V] [Module ℝ V] [Finite ι]
    (row : ι → V →ᵃ[ℝ] ℝ) (eqn : κ → V →ᵃ[ℝ] ℝ)
    (X T : V →ᵃ[ℝ] ℝ) (p q z : V) (ε : ℝ)
    (hp : ∀ i, row i p ≤ 0) (hz : ∀ i, row i z ≤ 0)
    (hep : ∀ k, eqn k p = 0) (heq : ∀ k, eqn k q = 0)
    (hez : ∀ k, eqn k z = 0)
    (hactive : ∀ i, row i p = 0 → row i q = 0)
    (hXz : X z = (X p + X q) / 2) (hTz : T z = (X z) ^ 2)
    (hmin : ∀ v, (∀ i, row i v ≤ 0) → (∀ k, eqn k v = 0) →
      X v = X p → T p ≤ T v)
    (hloP : (X p) ^ 2 - ε ≤ T p) (hloQ : (X q) ^ 2 - ε ≤ T q) :
    (X p - X q) ^ 2 ≤ 4*ε := by
  apply square_contact_of_active_rows (fun i => row i p) (fun i => row i q)
    (fun i => row i z) (X p) (X q) (T p) (T q) ε hp hz hactive _ hloP hloQ
  intro δ _ hrows
  let v := p + δ • (z - ((1/2:ℝ) • p + (1/2:ℝ) • q))
  have h := hmin v (by simpa only [v, affine_contact_step] using hrows)
    (by intro k; simp only [v, affine_contact_step, hep, heq, hez]; ring)
    (by simp only [v, affine_contact_step, hXz, sub_self, mul_zero, add_zero])
  simpa only [v, affine_contact_step, hTz, hXz] using h

end QuadraticPrecision
