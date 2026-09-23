import Formal.NetworkSimplex.ThresholdBalancedHull

/-! Terminal original-coordinate coefficient ratios for balanced incidence. -/
namespace NetworkSimplex.Chain.Balanced
open scoped BigOperators
noncomputable section

/-- Exactly the incidence, balancing, and chosen-coordinate hypotheses of the construction. -/
structure SectionData (N : ℕ) where
  S : Fin N → Finset (Fin N)
  alpha : Fin N → ℝ
  beta : ℝ
  a : ℝ
  invertible : IsUnit (incidenceMatrix S).det
  nonempty : ∀ i, (S i).Nonempty
  proper : ∀ i, S i ≠ Finset.univ
  positive : ∀ i, 0 < alpha i
  beta_pos : 0 < beta
  a_pos : 0 < a
  scale : (N : ℝ) * a = 1 / 2
  balance : ∀ j, ∑ i, alpha i * incidenceMatrix S i j = beta
  r : Fin N
  s : Fin N
  jr : Fin N
  js : Fin N
  distinct : r ≠ s
  r_forbidden : jr ∉ S r
  s_forbidden : js ∉ S s

variable {N : ℕ}

def SectionData.radius (D : SectionData N) : ℝ :=
  epsilon D.a (D.alpha D.r / D.alpha D.s) (inverseSize (incidenceMatrix D.S))

def SectionData.origin (D : SectionData N) := sectionPoint D.S D.a D.r D.s D.jr D.js 0 0

def SectionData.oU (D : SectionData N) := observation D.S D.r D.jr D.r_forbidden

def SectionData.oV (D : SectionData N) := observation D.S D.s D.js D.s_forbidden

theorem SectionData.radius_pos (D : SectionData N) : 0 < D.radius :=
  epsilon_pos D.a_pos (div_pos (D.positive D.r) (D.positive D.s)) (norm_nonneg _)

theorem SectionData.coordinates_distinct (D : SectionData N) : D.oU ≠ D.oV :=
  observation_ne D.S D.distinct D.jr D.js D.r_forbidden D.s_forbidden

/-- The section changes two original products without changing their scale or other coordinates. -/
theorem SectionData.slice_iff (D : SectionData N) {u v : ℝ}
    (hu : |u| < D.radius) (hv : |v| < D.radius) :
    productSlice D.origin D.oU D.oV u v ∈ convexHull ℝ (originalGraph D.S) ↔
      0 ≤ D.alpha D.r * u + D.alpha D.s * v := by
  dsimp only [SectionData.origin, SectionData.oU, SectionData.oV]
  rw [← sectionPoint_eq_productSlice D.S D.a D.r D.s D.jr D.js
    D.r_forbidden D.s_forbidden]
  exact section_hull_iff D.S D.invertible D.nonempty D.alpha D.positive D.beta_pos
    D.a_pos D.scale D.balance D.distinct D.jr D.js D.r_forbidden D.s_forbidden hu hv

/-- Every finite description contains the claimed positive product-coefficient ratio. -/
theorem SectionData.finite_description_ratio (D : SectionData N) {ι κ : Type*} [Finite ι]
    (rows : ι → AffineRow (ChainArc N) (Fin N) (Obs D.S))
    (eqs : κ → AffineRow (ChainArc N) (Fin N) (Obs D.S))
    (hd : ∀ q, q ∈ convexHull ℝ (originalGraph D.S) ↔
      (∀ i, 0 ≤ (rows i).eval q) ∧ (∀ j, (eqs j).eval q = 0)) :
    ∃ i, ∃ t : ℝ, 0 < t ∧ (rows i).eval D.origin = 0 ∧
      (rows i).product D.oU = t * D.alpha D.r ∧
      (rows i).product D.oV = t * D.alpha D.s :=
  finite_description_product_ratio _ D.origin D.oU D.oV D.radius_pos
    (D.positive D.r) (D.positive D.s) (fun _ _ => D.slice_iff) rows eqs hd

/-- Adding any valid affine equation cannot alter the two forced coefficients. -/
theorem SectionData.equation_coefficients (D : SectionData N)
    (r : AffineRow (ChainArc N) (Fin N) (Obs D.S))
    (hr : ∀ q ∈ convexHull ℝ (originalGraph D.S), r.eval q = 0) :
    r.product D.oU = 0 ∧ r.product D.oV = 0 :=
  valid_equation_product_coefficients _ D.origin D.oU D.oV D.radius_pos
    (D.positive D.r) (D.positive D.s) (fun _ _ => D.slice_iff) r hr

/-- The actual hull section has two-dimensional interior. -/
theorem SectionData.section_interior (D : SectionData N) :
    (interior {p : ℝ × ℝ |
      productSlice D.origin D.oU D.oV p.1 p.2 ∈ convexHull ℝ (originalGraph D.S)}).Nonempty := by
  apply (local_halfplane_nonempty_interior D.radius_pos (D.positive D.r)
    (D.positive D.s)).mono
  apply interior_mono
  intro p hp
  exact (D.slice_iff hp.1 hp.2.1).mpr hp.2.2

/-- Both gadget arcs have the strict domain bounds required by the stated section. -/
theorem SectionData.flow_margins (D : SectionData N) (i : Fin N) :
    0 < aggregate D.S D.a i ∧ aggregate D.S D.a i < 1 / 2 ∧
      0 < 1 / 2 - aggregate D.S D.a i ∧ 1 / 2 - aggregate D.S D.a i < 1 / 2 := by
  have h := aggregate_bounds D.S D.a_pos D.scale D.nonempty D.proper i
  exact ⟨h.1, h.2, by linarith, by linarith⟩

end
end NetworkSimplex.Chain.Balanced
