import Formal.NetworkSimplex.ThresholdOriginalObstruction
import Formal.NetworkSimplex.ThresholdExtension

/-! The four-label obstruction persists with any number of unused explicit labels. -/
namespace NetworkSimplex.Chain.ThresholdObstruction
open scoped BigOperators
noncomputable section

/-- Every additional explicit label has zero weight; retained coordinates are unchanged. -/
def extendedSectionPoint (k : ℕ) (U V : ℝ) := finZeroExtendPoint k (sectionPoint U V)

def extendedObstructionGraph (k : ℕ) :=
  OriginalGraph (incidence 4) (demand 4) (fun _ => 1)
    (fun o : Obs => o.val.1)
    (finSumFinEquiv ∘ Sum.inl ∘ (fun o : Obs => o.val.2) : Obs → Fin (4 + k))

theorem extended_section_sum_one (k : ℕ) (U V : ℝ) :
    ∑ j, (extendedSectionPoint k U V).2.1 j = 1 := by
  simp [extendedSectionPoint, finZeroExtendPoint, relabelPoint, Equiv.sum_comp,
    zeroExtendPoint, Fintype.sum_sum_type, sectionPoint, chainPoint]

/-- The same unscaled pair of original product coordinates gives the same local section. -/
theorem extended_section_original_hull_iff (k : ℕ) {U V : ℝ} (h : Near U V) :
    extendedSectionPoint k U V ∈ convexHull ℝ (extendedObstructionGraph k) ↔
      3/32 ≤ 2 * U + V := by
  unfold extendedObstructionGraph
  rw [original_hull_iff_full_of_sum_one _ _ _ _ _ _ (extended_section_sum_one k U V)]
  change finZeroExtendPoint k (sectionPoint U V) ∈ _ ↔ _
  rw [finZeroExtend_mem_hull_iff]
  exact section_hull_iff h

/-- An arbitrary affine row in the larger original coordinate space. -/
structure ExtendedRow (k : ℕ) where
  constant : ℝ
  flow : ChainArc 4 → ℝ
  weight : Fin (4 + k) → ℝ
  product : Obs → ℝ

def ExtendedRow.eval {k : ℕ} (r : ExtendedRow k)
    (p : OriginalPoint (ChainArc 4) Obs (4 + k)) : ℝ :=
  r.constant + (∑ e, r.flow e * p.1 e) +
    (∑ j, r.weight j * p.2.1 j) + ∑ o, r.product o * p.2.2 o

/-- Fixing the extra labels does not change either free product coefficient. -/
theorem ExtendedRow.eval_section {k : ℕ} (r : ExtendedRow k) (u v : ℝ) :
    r.eval (extendedSectionPoint k (1/32 + u) (1/32 + v)) =
      r.eval (extendedSectionPoint k (1/32) (1/32)) +
        r.product obsU * u + r.product obsV * v := by
  unfold ExtendedRow.eval extendedSectionPoint finZeroExtendPoint relabelPoint zeroExtendPoint
  simp_rw [section_product]
  simp only [mul_add, Finset.sum_add_distrib, mul_ite, mul_zero]
  simp only [Finset.sum_ite_eq', Finset.mem_univ, ↓reduceIte]
  simp only [add_assoc]
  rfl

/-- Additional unused explicit labels cannot restore a unit-product description. -/
theorem no_extended_unit_description (k : ℕ) {ι κ : Type*} (rows : ι → ExtendedRow k)
    (eqs : κ → ExtendedRow k) (hunit : ∀ i o, UnitCoefficient ((rows i).product o)) :
    ¬ (∀ p, p ∈ convexHull ℝ (extendedObstructionGraph k) ↔
      (∀ i, 0 ≤ (rows i).eval p) ∧ (∀ j, (eqs j).eval p = 0)) := by
  intro hd
  apply local_halfplane_not_unit_description (ε := (1/128 : ℝ)) (by norm_num)
    (fun i => (rows i).product obsU) (fun i => (rows i).product obsV)
    (fun i => (rows i).eval (extendedSectionPoint k (1/32) (1/32)))
    (fun j => (eqs j).product obsU) (fun j => (eqs j).product obsV)
    (fun j => (eqs j).eval (extendedSectionPoint k (1/32) (1/32)))
    (fun i => hunit i _) (fun i => hunit i _)
  intro u v hu hv
  have hn : Near (1/32 + u) (1/32 + v) := by simpa [Near] using And.intro hu hv
  have hh := extended_section_original_hull_iff k hn
  rw [hd] at hh
  simp only [ExtendedRow.eval_section] at hh
  exact hh.trans (by constructor <;> intro h <;> linarith)

/-- Finite descriptions still require ratio two on the same original products. -/
theorem extended_finite_description_ratio (k : ℕ) {ι κ : Type*} [Finite ι]
    (rows : ι → ExtendedRow k) (eqs : κ → ExtendedRow k)
    (h : ∀ p, p ∈ convexHull ℝ (extendedObstructionGraph k) ↔
      (∀ i, 0 ≤ (rows i).eval p) ∧ (∀ j, (eqs j).eval p = 0)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ (rows i).product obsU = 2 * t ∧
      (rows i).product obsV = t := by
  have hd := local_halfplane_description_positive_multiple (ε := (1/128 : ℝ)) (by norm_num)
    (fun i => (rows i).product obsU) (fun i => (rows i).product obsV)
    (fun i => (rows i).eval (extendedSectionPoint k (1/32) (1/32)))
    (fun j => (eqs j).product obsU) (fun j => (eqs j).product obsV)
    (fun j => (eqs j).eval (extendedSectionPoint k (1/32) (1/32))) (by
      intro u v hu hv
      have hn : Near (1/32 + u) (1/32 + v) := by simpa [Near] using And.intro hu hv
      have hh := extended_section_original_hull_iff k hn
      rw [h] at hh
      simp only [ExtendedRow.eval_section] at hh
      exact hh.trans (by constructor <;> intro h <;> linarith))
  obtain ⟨i, t, ht, _, hU, hV⟩ := hd
  exact ⟨i, t, ht, hU, hV⟩

end
end NetworkSimplex.Chain.ThresholdObstruction
