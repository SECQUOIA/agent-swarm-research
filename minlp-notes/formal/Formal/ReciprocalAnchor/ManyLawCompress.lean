import Formal.ReciprocalAnchor.ManyModel

/-! Removing zero-mass atoms preserves every finite expectation. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators
noncomputable section

/-- The atom indices with positive mass. -/
abbrev Law.PositiveIndex {a b : ℝ} (μ : Law a b) := {i : Fin μ.size // 0 < μ.mass i}

/-- Zero-mass atoms contribute nothing to an expectation. -/
theorem Law.sum_positive {a b : ℝ} (μ : Law a b) (f : Fin μ.size → ℝ) :
    (∑ i : μ.PositiveIndex, μ.mass i * f i) = ∑ i, μ.mass i * f i := by
  classical
  have hz : (∑ i : {i : Fin μ.size // ¬0 < μ.mass i}, μ.mass i * f i) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    have h : μ.mass i = 0 := le_antisymm (not_lt.mp i.property) (μ.nonneg i)
    simp [h]
  simpa only [hz, add_zero] using
    Fintype.sum_subtype_add_sum_subtype (fun i => 0 < μ.mass i) (fun i => μ.mass i * f i)

/-- A law represented using only its positive-mass atoms. -/
def Law.compress {a b : ℝ} (μ : Law a b) : Law a b := by
  classical
  let e := (Fintype.equivFin μ.PositiveIndex).symm
  exact {
    size := Fintype.card μ.PositiveIndex
    mass := fun i => μ.mass (e i)
    location := fun i => μ.location (e i)
    nonneg := fun i => μ.nonneg (e i)
    total := by
      rw [e.sum_comp (fun i : μ.PositiveIndex => μ.mass i)]
      simpa using (μ.sum_positive (fun _ => 1)).trans (by simpa using μ.total)
    bounds := fun i => μ.bounds (e i)
  }

theorem Law.compress_size {a b : ℝ} (μ : Law a b) :
    μ.compress.size = (Finset.univ.filter fun i => 0 < μ.mass i).card := by
  classical
  exact Fintype.card_subtype (fun i : Fin μ.size => 0 < μ.mass i)

theorem Law.compress_mass_pos {a b : ℝ} (μ : Law a b) (i : Fin μ.compress.size) :
    0 < μ.compress.mass i := by
  exact ((Fintype.equivFin μ.PositiveIndex).symm i).property

/-- Compression preserves the expectation of every function of location. -/
theorem Law.compress_expectation {a b : ℝ} (μ : Law a b) (f : ℝ → ℝ) :
    (∑ i, μ.compress.mass i * f (μ.compress.location i)) =
      ∑ i, μ.mass i * f (μ.location i) := by
  classical
  change (∑ i, μ.mass ((Fintype.equivFin μ.PositiveIndex).symm i) *
    f (μ.location ((Fintype.equivFin μ.PositiveIndex).symm i))) = _
  rw [(Fintype.equivFin μ.PositiveIndex).symm.sum_comp
    (fun i : μ.PositiveIndex => μ.mass i * f (μ.location i))]
  exact μ.sum_positive (fun i => f (μ.location i))

theorem Law.compress_mean {a b : ℝ} (μ : Law a b) : μ.compress.mean = μ.mean :=
  μ.compress_expectation id

theorem Law.compress_call {a b : ℝ} (μ : Law a b) (s : ℝ) :
    μ.compress.call s = μ.call s :=
  μ.compress_expectation (fun x => max (x - s) 0)

theorem Law.compress_reciprocal {a b : ℝ} (μ : Law a b) :
    μ.compress.reciprocal = μ.reciprocal := by
  simpa only [Law.reciprocal, div_eq_mul_inv] using μ.compress_expectation Inv.inv

end
end ReciprocalAnchor.ManyLeaf
