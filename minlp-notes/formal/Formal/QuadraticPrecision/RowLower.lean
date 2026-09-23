import Formal.QuadraticPrecision.RowLowerCounting
import Formal.QuadraticPrecision.PolyhedronAffine

namespace QuadraticPrecision

/-- Finite affine equality constraints do not prevent minimum attainment and
need not be counted as inequalities in the separate row-complexity theorem. -/
theorem affine_minimum_with_equalities {V ι κ : Type*}
    [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V] [Finite ι] [Finite κ]
    (row : ι → V →ᵃ[ℝ] ℝ) (eqn : κ → V →ᵃ[ℝ] ℝ) (T : V →ᵃ[ℝ] ℝ)
    (hfeas : ∃ v, (∀ i, row i v ≤ 0) ∧ ∀ k, eqn k v = 0)
    (hlower : ∃ L, ∀ v, (∀ i, row i v ≤ 0) → (∀ k, eqn k v = 0) → L ≤ T v) :
    ∃ v, (∀ i, row i v ≤ 0) ∧ (∀ k, eqn k v = 0) ∧
      ∀ w, (∀ i, row i w ≤ 0) → (∀ k, eqn k w = 0) → T v ≤ T w := by
  let rows : ι ⊕ (κ ⊕ κ) → V →ᵃ[ℝ] ℝ :=
    Sum.elim row (Sum.elim eqn (fun k => -eqn k))
  have hrows (v : V) : (∀ i, rows i v ≤ 0) ↔
      (∀ i, row i v ≤ 0) ∧ (∀ k, eqn k v = 0) := by
    constructor
    · intro h
      refine ⟨fun i => h (.inl i), fun k => le_antisymm (h (.inr (.inl k))) ?_⟩
      have hh := h (.inr (.inr k))
      change -eqn k v ≤ 0 at hh
      linarith
    · rintro ⟨hr, he⟩ i
      rcases i with i | k
      · exact hr i
      · rcases k with k | k <;> simp [rows, he]
  obtain ⟨v, hv, hmin⟩ := affine_minimum rows T (by
    obtain ⟨v, hv⟩ := hfeas
    exact ⟨v, (hrows v).mpr hv⟩) (by
      obtain ⟨L, hL⟩ := hlower
      exact ⟨L, fun v hv => hL v ((hrows v).mp hv).1 ((hrows v).mp hv).2⟩)
  exact ⟨v, ((hrows v).mp hv).1, ((hrows v).mp hv).2,
    fun w hw hew => hmin w ((hrows w).mpr ⟨hw, hew⟩)⟩

/-- Every finite linear extended formulation containing the square graph on
`[0,1]` and lying above `x² - ε` needs exponentially many active row patterns.
The auxiliary space is any finite-dimensional real space. Finite equalities,
lineality and unbounded auxiliary fibers are all allowed. -/
theorem square_epigraph_row_lower_bound_algebraic
    {V κ : Type*} [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V] [Finite κ]
    (M : ℕ) (row : Fin M → V →ᵃ[ℝ] ℝ) (eqn : κ → V →ᵃ[ℝ] ℝ)
    (X T : V →ᵃ[ℝ] ℝ) (ε : ℝ)
    (hgraph : ∀ x ∈ Set.Icc (0 : ℝ) 1, ∃ z,
      (∀ i, row i z ≤ 0) ∧ (∀ k, eqn k z = 0) ∧ X z = x ∧ T z = x ^ 2)
    (hlower : ∀ p, (∀ i, row i p ≤ 0) → (∀ k, eqn k p = 0) →
      X p ∈ Set.Icc (0 : ℝ) 1 → (X p) ^ 2 - ε ≤ T p) :
    1 ≤ 4 * ε * ((2 : ℝ) ^ M) ^ 2 := by
  apply square_row_bound_of_attainment M row eqn X T ε hgraph hlower
  intro x hx
  let eqs : κ ⊕ Unit → V →ᵃ[ℝ] ℝ :=
    Sum.elim eqn (fun _ => X - AffineMap.const ℝ V x)
  have heqs (v : V) : (∀ k, eqs k v = 0) ↔ (∀ k, eqn k v = 0) ∧ X v = x := by
    simp [eqs, sub_eq_zero]
  obtain ⟨v, hv, hev, hmin⟩ := affine_minimum_with_equalities row eqs T (by
    obtain ⟨z, hz, hez, hXz, _⟩ := hgraph x hx
    exact ⟨z, hz, (heqs z).mpr ⟨hez, hXz⟩⟩) (by
      refine ⟨x ^ 2 - ε, fun v hv hev => ?_⟩
      obtain ⟨he, hX⟩ := (heqs v).mp hev
      simpa only [hX] using hlower v hv he (by simpa only [hX] using hx))
  obtain ⟨he, hX⟩ := (heqs v).mp hev
  exact ⟨v, hv, he, hX, fun w hw hew hXw =>
    hmin w hw ((heqs w).mpr ⟨hew, hXw⟩)⟩

/-- The paper's logarithmic lower bound on inequality rows for a square-epigraph
finite LP approximation. Only inequalities are counted, not equality rows. -/
theorem square_epigraph_row_lower_bound
    {V κ : Type*} [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V] [Finite κ]
    (M : ℕ) (row : Fin M → V →ᵃ[ℝ] ℝ) (eqn : κ → V →ᵃ[ℝ] ℝ)
    (X T : V →ᵃ[ℝ] ℝ) {ε : ℝ} (hε : 0 < ε)
    (hgraph : ∀ x ∈ Set.Icc (0 : ℝ) 1, ∃ z,
      (∀ i, row i z ≤ 0) ∧ (∀ k, eqn k z = 0) ∧ X z = x ∧ T z = x ^ 2)
    (hlower : ∀ p, (∀ i, row i p ≤ 0) → (∀ k, eqn k p = 0) →
      X p ∈ Set.Icc (0 : ℝ) 1 → (X p) ^ 2 - ε ≤ T p) :
    (1/2 : ℝ) * Real.logb 2 (1/ε) - 1 ≤ M :=
  row_log_lower_bound M hε
    (square_epigraph_row_lower_bound_algebraic M row eqn X T ε hgraph hlower)

end QuadraticPrecision
